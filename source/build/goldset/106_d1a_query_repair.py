#!/usr/bin/env python3
r"""
106_d1a_query_repair.py — D.1.a. Expand the frozen query's wildcards into verified real terms.

WHAT IS BEING REPAIRED. `105_d1a_stem_audit.py` established that 24 of the frozen query's 45
wildcard terms retrieve almost nothing once the star is stripped, and that two more (`secular*`,
`religio*`) return healthy counts while failing to match the very inflections they were written for.
The consequence is measured, not hypothetical: two of the chapter's three Tier-1 natural experiments
are absent from the C1 corpus.

A6c already specified this fix -- "the compiled query must be emitted with wildcards expanded before
C1 consumes it" -- and it was not enforced. This script enforces it.

THE EXPANSIONS ARE HARVESTED, NOT INVENTED. Writing out the variants by hand would repeat the
mistake that caused this: someone deciding from intuition what an index will match. Candidates come
from three sources and every one is then verified against a live count.

  1. THE GOLD TITLES. Tier A + Tier B, ~412 works assembled by citation snowball and independent of
     this query. This is the load-bearing source precisely because it is query-independent -- it
     contains the vocabulary of papers the query MISSED.
  2. The live corpus titles. Large, but biased by construction: it was retrieved BY the broken
     query, so it under-represents exactly the words at issue. Used as a supplement, never alone.
  3. Rule-based English suffixes, to catch forms absent from both corpora.

VERIFICATION IS TWO-SIDED, BECAUSE A COUNT ALONE MISSES THE `secular` CASE. Every candidate gets a
live count. Then the assembled v2 query is tested CONJUNCTIVELY against the DOIs of the papers v1
missed -- `filter=doi:<doi>,title.search:<outcome block>,title.search:<cluster block>` -- which is
the production filter itself with a DOI pinned to it. One request per paper per cluster, and it
answers the only question that matters: does the repaired query actually retrieve the study?

THE ACCEPTANCE GATE. Both missing Tier-1 papers must be retrieved by v2, and the negative control
must stay retrieved. The script exits nonzero otherwise and v2 must not be pulled.

Usage:
  python3 106_d1a_query_repair.py           # cached; re-run is free
  python3 106_d1a_query_repair.py --refresh

Output: literature/search-logs/{slug}-production-query-v2.json   (C1 consumes this)
        literature/search-logs/{slug}-query-repair.md
"""
import json, os, re, subprocess, sys, time, unicodedata, urllib.parse
from collections import Counter

SLUG = "postmaterialism-individualism-secularization"
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
LOGS = os.path.join(ROOT, "literature", "search-logs")
PQ = os.path.join(LOGS, f"{SLUG}-production-query.json")
CORPUS = os.path.join(LOGS, f"{SLUG}-live-corpus.json")
OUT_PQ = os.path.join(LOGS, f"{SLUG}-production-query-v2.json")
OUT_MD = os.path.join(LOGS, f"{SLUG}-query-repair.md")
CACHE = os.path.join(HERE, "d1a_query_repair_cache.json")

KEY = os.environ.get("OPENALEX_API_KEY", "").strip()
UA = "fertility-review/1.0 (mailto:shravanh@uchicago.edu)"

MIN_COUNT = 5          # a variant retrieving fewer than this buys nothing and costs query length
MAX_PER_STEM = 8       # cap expansions so a single stem cannot blow up the filter's byte length
URL_CEILING = 4000     # A6c hit HTTP 400 at 5,309 bytes on S2; stay well inside any such limit

SUFFIXES = ["", "s", "es", "ed", "ing", "ism", "ist", "ists", "ity", "ies", "ly", "ous", "ness",
            "ation", "ations", "ization", "izations", "isation", "isations", "ize", "ise",
            "ized", "ised", "izing", "ising", "ive", "ative", "al", "ally", "ic", "ical"]

# The papers v1 missed, with the DOI that proves they are in OpenAlex, plus one retrieved control.
ACCEPTANCE = [
    ("10.1016/j.ssresearch.2026.103371", "Secularization and low fertility", True),
    ("10.1007/s00148-025-01092-5", "Religiously inspired baby boom: Georgia", True),
    ("10.1086/696193", "Political Islam, Marriage and Fertility (control, was retrieved)", True),
]


def fold(s):
    s = unicodedata.normalize("NFKD", s or "")
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"<[^>]+>", " ", s).lower()


def words(titles):
    c = Counter()
    for t in titles:
        c.update(re.findall(r"[a-z]+(?:-[a-z]+)*", fold(t)))
    return c


def load_cache():
    if os.path.exists(CACHE) and "--refresh" not in sys.argv:
        with open(CACHE) as fh:
            return json.load(fh)
    return {}


class BudgetExhausted(Exception):
    """OpenAlex refused on budget. It is NOT a count of zero and must never become one."""


def oa_count(params, cache, ck):
    """Live count, or raise. NEVER returns a number it did not measure.

    The first version returned None on any failure and the callers coerced it to 0 -- so a budget
    refusal was recorded as "this term retrieves nothing" and, worse, as "the acceptance paper is not
    retrieved". The whole run then reported three gate FAILURES including the negative control that
    v1 demonstrably retrieved. That is a refusal read as a measurement, which is the exact failure
    this chapter has now documented six times, committed here in the script written to fix the
    sixth. Budget exhaustion stops the run; nothing downstream is allowed to see a fabricated zero.
    """
    if ck in cache:
        return cache[ck]
    p = dict(params)
    if KEY:
        p["api_key"] = KEY
    url = "https://api.openalex.org/works?" + urllib.parse.urlencode(p)
    r = subprocess.run(["curl", "-s", "-m", "45", "-A", UA, url], capture_output=True, text=True)
    try:
        d = json.loads(r.stdout)
    except Exception:
        raise BudgetExhausted(f"unparseable response for {ck}: {r.stdout[:160]}") from None
    if d.get("error"):
        raise BudgetExhausted(f"{d.get('error')}: {str(d.get('message'))[:160]}")
    n = (d.get("meta") or {}).get("count")
    if n is None:
        raise BudgetExhausted(f"no count in response for {ck}")
    cache[ck] = n
    with open(CACHE, "w") as fh:
        json.dump(cache, fh)
    time.sleep(0.12)
    return n


MAX_TESTED = 14        # candidates actually sent per stem; each costs $0.001 against a $1/day budget


def candidates(term, vocab):
    """Expansions for one wildcard term. The star is always on the final word.

    Ranked before it is truncated, because the budget is real: forms OBSERVED in the gold and corpus
    titles are tested first and rule-generated forms only fill the remainder. The first version
    tested every candidate and spent the whole daily allowance on ~1,500 requests.
    """
    head, _, tail = term.rpartition(" ")
    stem = re.sub(r"[*?]", "", tail).strip().lower()
    if not stem:
        return []
    # Keep them short-ish: a 20-letter word starting with `secular` is not a variant of it.
    observed = sorted({w for w in vocab
                       if w.startswith(stem) and len(w) <= len(stem) + 8}, key=len)
    generated = [stem + s for s in SUFFIXES if stem + s not in observed]
    ranked, seen = [], set()
    for w in observed + generated:
        if w not in seen:
            seen.add(w); ranked.append(w)
    return [(head + " " + w).strip() for w in ranked[:MAX_TESTED]]


def main():
    if not KEY:
        print("OPENALEX_API_KEY not set -- requests will be refused.", file=sys.stderr)
        sys.exit(1)
    cache = load_cache()
    pq = json.load(open(PQ))

    gold_titles = []
    for f in (f"{SLUG}-tier-a.json", f"{SLUG}-tier-b-frame.json"):
        for r in json.load(open(os.path.join(LOGS, f))):
            if r.get("title"):
                gold_titles.append(r["title"])
    corpus_titles = [r["title"] for r in json.load(open(CORPUS))["records"] if r.get("title")]
    vocab = set(words(gold_titles)) | {w for w, n in words(corpus_titles).items() if n >= 2}
    print(f"  vocabulary: {len(gold_titles)} gold titles, {len(corpus_titles)} corpus titles -> "
          f"{len(vocab)} distinct words", file=sys.stderr)

    groups = {"OUTCOME": pq["outcome_terms"], **pq["treatment_clusters"]}
    repaired, report = {}, []
    try:
      for g, terms in groups.items():
        kept_terms, seen = [], set()
        for t in sorted(set(terms)):
            if "*" not in t:
                n = oa_count({"filter": f"title.search:{t}", "per-page": 1, "select": "id"},
                             cache, f"c::{t}")
                # A plain term that retrieves nothing is dead too; the audit only looked at stems.
                if n >= MIN_COUNT:
                    if t not in seen:
                        kept_terms.append(t); seen.add(t)
                else:
                    report.append({"cluster": g, "original": t, "kind": "plain",
                                   "kept": [], "dropped": [(t, n)]})
                continue
            cands = candidates(t, vocab)
            scored = []
            for c in cands:
                scored.append((c, oa_count({"filter": f"title.search:{c}", "per-page": 1,
                                            "select": "id"}, cache, f"c::{c}")))
            good = sorted([x for x in scored if x[1] >= MIN_COUNT],
                          key=lambda x: -x[1])[:MAX_PER_STEM]
            bad = [x for x in scored if x[1] < MIN_COUNT]
            for c, _ in good:
                if c not in seen:
                    kept_terms.append(c); seen.add(c)
            report.append({"cluster": g, "original": t, "kind": "wildcard",
                           "kept": good, "dropped": bad})
        repaired[g] = kept_terms
    except BudgetExhausted as e:
        # Stop rather than emit a query built from fabricated zeros. Every measured count is already
        # cached, so resuming after the midnight-UTC reset costs only what was never measured.
        print(f"\nBUDGET EXHAUSTED mid-repair: {e}\n"
              f"  {len(cache)} counts cached and safe. NOTHING was written -- v2 is not emitted from "
              f"a partial measurement.\n  Re-run after the reset; cached lookups cost nothing.",
              file=sys.stderr)
        sys.exit(2)

    out_terms = repaired.pop("OUTCOME")
    v2 = {**pq, "stage": "A6c-repaired", "version": "v2",
          "repaired_from": os.path.basename(PQ),
          "repair_note": ("Wildcards expanded into live-verified variants. v1 stripped the star and "
                          "sent a bare stem, which retrieved almost nothing for 24 of 45 terms."),
          "outcome_terms": out_terms, "treatment_clusters": repaired}

    # ---- acceptance: does v2 actually retrieve the papers v1 missed? ------------------------
    ob = "|".join(sorted({t.lower() for t in out_terms}))
    gates, url_lens = [], {}
    try:
      for doi, label, must in ACCEPTANCE:
        hit_in = []
        for c, terms in repaired.items():
            tb = "|".join(sorted({t.lower() for t in terms}))
            filt = f"doi:{doi},title.search:{ob},title.search:{tb}"
            n = oa_count({"filter": filt, "per-page": 1, "select": "id"}, cache, f"m::{doi}::{c}")
            url_lens[c] = len(f"title.search:{ob},title.search:{tb}")
            if n == 1:
                hit_in.append(c)
        gates.append({"doi": doi, "paper": label, "required": must,
                      "retrieved_by": hit_in, "pass": bool(hit_in) == must})
    except BudgetExhausted as e:
        print(f"\nBUDGET EXHAUSTED during the acceptance gate: {e}\n"
              f"  v2 is NOT written. An unverified query must not reach C1 -- an unrun gate is not a "
              f"passed gate.\n  Re-run after the reset; cached lookups cost nothing.", file=sys.stderr)
        sys.exit(2)

    v2["acceptance"] = gates
    v2["filter_bytes"] = url_lens
    json.dump(v2, open(OUT_PQ, "w"), indent=1)

    n_wild = sum(1 for r in report if r["kind"] == "wildcard")
    n_added = sum(len(r["kept"]) for r in report if r["kind"] == "wildcard")
    n_dead_plain = sum(1 for r in report if r["kind"] == "plain")
    failed = [g for g in gates if not g["pass"]]
    oversize = {c: n for c, n in url_lens.items() if n > URL_CEILING}

    L = ["# D.1.a — production query repair (v1 → v2)", "",
         "`105_` established that 24 of v1's 45 wildcard terms retrieve almost nothing once the star "
         "is stripped, and that `secular` and `religio` return healthy counts while failing to match "
         "the inflections they were written for. Two of the chapter's three Tier-1 natural "
         "experiments are absent from the C1 corpus as a result. A6c already specified this fix and "
         "it was not enforced.", "",
         "**The expansions are harvested, not invented.** Candidates come from the **gold titles** "
         "(Tier A + Tier B, query-independent, and therefore containing the vocabulary of the papers "
         "the query missed), the live corpus titles, and rule-based English suffixes. Every "
         "candidate is then verified against a live count, and the assembled query is verified "
         "conjunctively against the DOIs of the papers v1 missed.", "",
         f"- wildcard terms expanded: **{n_wild}**",
         f"- live-verified variants added: **{n_added}**",
         f"- plain (non-wildcard) terms dropped as dead: **{n_dead_plain}**",
         f"- outcome terms: {len(pq['outcome_terms'])} → **{len(out_terms)}**", "",
         "| cluster | v1 terms | v2 terms |", "|---|---|---|"]
    for c in repaired:
        L.append(f"| `{c}` | {len(set(pq['treatment_clusters'][c]))} | **{len(repaired[c])}** |")

    L += ["", "## Acceptance gate — does v2 retrieve what v1 missed?", "",
          "The production filter itself with a DOI pinned to it: "
          "`filter=doi:<doi>,title.search:<outcome>,title.search:<cluster>`. This is the only test "
          "that answers the question; a count per term does not.", "",
          "| paper | retrieved by | verdict |", "|---|---|---|"]
    for g in gates:
        L.append(f"| {g['paper']} | {', '.join(f'`{c}`' for c in g['retrieved_by']) or '—'} | "
                 f"{'**PASS**' if g['pass'] else '**FAIL**'} |")
    if failed:
        L += ["", "> **GATE FAILED — v2 must not be pulled.** "
              f"{len(failed)} acceptance paper(s) still unretrieved.", ""]
    if oversize:
        L += ["", f"> ⚠ filter length over {URL_CEILING} bytes for {list(oversize)} — A6c hit "
              "HTTP 400 at 5,309 bytes on Semantic Scholar; check OpenAlex accepts these.", ""]

    L += ["", "## Per-term repair", "",
          "`dropped` variants retrieved fewer than "
          f"{MIN_COUNT} records and would only lengthen the filter.", ""]
    for r in report:
        if r["kind"] == "plain":
            L.append(f"- **DEAD PLAIN TERM** `{r['cluster']}` / `{r['original']}` "
                     f"— count {r['dropped'][0][1]}, removed")
    L += [""]
    for r in report:
        if r["kind"] != "wildcard":
            continue
        kept = ", ".join(f"`{c}` ({n:,})" for c, n in r["kept"]) or "**nothing survived**"
        L.append(f"- `{r['cluster']}` / `{r['original']}` → {kept}")
    open(OUT_MD, "w").write("\n".join(L) + "\n")

    print(f"expanded {n_wild} wildcards -> {n_added} verified variants; "
          f"dead plain terms removed: {n_dead_plain}", file=sys.stderr)
    for g in gates:
        print(f"  gate {'PASS' if g['pass'] else 'FAIL'}: {g['paper']} "
              f"-> {g['retrieved_by'] or 'NOT RETRIEVED'}", file=sys.stderr)
    print(f"wrote {OUT_PQ}\nwrote {OUT_MD}", file=sys.stderr)
    if failed:
        print("ACCEPTANCE GATE FAILED -- do not pull v2", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
