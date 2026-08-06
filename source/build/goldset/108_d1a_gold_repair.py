#!/usr/bin/env python3
r"""
108_d1a_gold_repair.py — D.1.a. Repair gold rows whose "title" is an entire citation string, then
re-measure recall against the v2 corpus.

THE DEFECT. `107_` found that 24 of the 68 gold records missing from the v2 corpus have a stored
title that is a whole bibliography line -- "van de Kaa, D. J. (2001). Postmodern fertility
preferences: From changing value orientation to new behavior. Population and Development Review, 27,
290-331." Crossref reference lists carry an `unstructured` field when the publisher deposited a
formatted reference, and `93_`/`96_` fall back to it. A3 found 27 such rows and did not fully repair
them. Such a record CANNOT match by title however complete the index is, so it depresses measured
Recall(B-only) while saying nothing whatever about coverage.

THE ONE DESIGN DECISION THAT MATTERS, AND GETTING IT WRONG WOULD RIG THE RESULT.

Titles are extracted by PARSING THE STRING ONLY. The obvious alternative -- search each citation
string against OpenAlex and adopt the title of the best match -- is far more accurate per record and
is disqualified: it repairs only the rows OpenAlex can confirm, so the repaired gold set becomes a
set of works OpenAlex is known to hold, and the recall it then measures is guaranteed to rise. The
measurement would be an artifact of its own repair. Parsing is provider-independent, so a work whose
title we recover but which OpenAlex does not hold correctly STAYS a miss.

Provider lookup still happens, but only AFTER the repair and only to label confidence and to refresh
the index-gap decomposition. It never decides a title and never removes a row.

CONSERVATIVE BY CONSTRUCTION. A row is repaired only when the citation has a clear year marker to
anchor on. Everything else is left exactly as it is and reported as UNREPAIRED -- it stays a miss,
which is the honest outcome. This chapter acquired a 40%-ghost Tier B on the OAS run by relaxing a
match threshold to lift a recovery rate; a low repair rate is the correct outcome when the strings
genuinely cannot be parsed.

DUPLICATES ARE THE SECOND HALF OF THE JOB. Repairing a citation string frequently reveals a row the
gold set already holds in clean form -- "Report on analysis of ESS data..." exists both ways -- and
A6a already found 95 of 495 Tier-B rows were duplicates for the same underlying reason. Merging is
therefore part of the repair, and the recall denominator moves as a result. That is reported rather
than absorbed.

Usage:  python3 108_d1a_gold_repair.py [--query v2]
Output: literature/search-logs/{slug}-tier-b-frame-repaired.json
        literature/search-logs/{slug}-gold-repair.md
"""
import json, os, re, subprocess, sys, time, unicodedata, urllib.parse
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import importlib.util

SLUG = "postmaterialism-individualism-secularization"
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
LOGS = os.path.join(ROOT, "literature", "search-logs")
SUF = "-v2" if "--query" in sys.argv and sys.argv[sys.argv.index("--query") + 1] == "v2" else ""
CORPUS = os.path.join(LOGS, f"{SLUG}-live-corpus{SUF}.json")
TIER_B = os.path.join(LOGS, f"{SLUG}-tier-b-frame.json")
OUT_FRAME = os.path.join(LOGS, f"{SLUG}-tier-b-frame-repaired.json")
OUT_MD = os.path.join(LOGS, f"{SLUG}-gold-repair.md")
CACHE = os.path.join(HERE, "d1a_gold_repair_cache.json")

KEY = os.environ.get("OPENALEX_API_KEY", "").strip()
UA = "fertility-review/1.0 (mailto:shravanh@uchicago.edu)"

_spec = importlib.util.spec_from_file_location("cv", os.path.join(HERE, "101_d1a_cv_breadth.py"))
cv = importlib.util.module_from_spec(_spec)
sys.modules["cv"] = cv
_spec.loader.exec_module(cv)

CITATION_MARKS = [
    re.compile(r"\(\s*(19|20)\d{2}\s*\)"),
    re.compile(r"^[A-Z][a-z]+,\s*[A-Z]\.\s*"),
    re.compile(r"\s&\s"),
    re.compile(r"^(?:[A-Z]{1,3}\s+[A-Z][a-z]+\s+){2,}"),
    re.compile(r"\bdoi:\s*10\.", re.I),
    re.compile(r"\bpp\.\s*\d+", re.I),
]

# Anchors that mark the END of the author block and the START of the title. Ordered most to least
# reliable; the first that matches wins.
YEAR_ANCHORS = [
    re.compile(r"\(\s*(?:19|20)\d{2}[a-z]?\s*\)\s*[.,]?\s*"),      # "(2001). "
    re.compile(r"(?<![\w(])(?:19|20)\d{2}[a-z]?\.\s+"),            # "Westoff, C. F. 2015. "
]

# Things that terminate a title. A venue usually follows the first sentence break.
# THE DIGIT CLASS IS LOAD-BEARING. The first version required a letter before the terminating period,
# so a title ending in a year did not terminate: "Modes of production secularization and the pace of
# the fertility decline in Western Europe 1870-1930." ran on into its editor block and came out as
# "...1870-1930. In A. J." -- a title that would never match anything. Caught by reading the
# repairs, not by the repair rate, which looked fine at 23 of 24.
TITLE_END = re.compile(r"(?<=[a-z0-9\)\]\?])\.\s+(?=[A-Z\[])|\.\s*$")

MIN_TITLE_WORDS = 3


def looks_like_citation(t):
    return any(rx.search(t or "") for rx in CITATION_MARKS)


def extract_title(cite):
    """Parse a title out of a formatted reference. Returns (title, method) or (None, reason)."""
    s = re.sub(r"\s+", " ", (cite or "").strip())
    for rx in YEAR_ANCHORS:
        m = rx.search(s)
        if not m:
            continue
        rest = s[m.end():].strip()
        if not rest:
            continue
        end = TITLE_END.search(rest)
        title = (rest[:end.start() + 1] if end else rest).strip()
        title = title.rstrip(" .,;")
        # A bracketed translation appended to a non-English title is part of the record, not a venue.
        title = re.sub(r"\s*\[[^\]]{0,200}\]\s*$", "", title).strip()
        if len(title.split()) >= MIN_TITLE_WORDS and not re.fullmatch(r"[\d\W]+", title):
            return title, "year-anchored"
    return None, "no year anchor -- left unrepaired"


def load_cache():
    if os.path.exists(CACHE):
        with open(CACHE) as fh:
            return json.load(fh)
    return {}


def oa_exists(title, cache):
    """Confidence label ONLY. Never decides a title, never removes a row."""
    key = cv.norm(title)[:80]
    if key in cache:
        return cache[key]
    p = {"search": title[:150], "per-page": 5, "select": "id,title"}
    if KEY:
        p["api_key"] = KEY
    url = "https://api.openalex.org/works?" + urllib.parse.urlencode(p)
    r = subprocess.run(["curl", "-s", "-m", "45", "-A", UA, url], capture_output=True, text=True)
    try:
        d = json.loads(r.stdout)
    except Exception:
        return "__ERROR__"
    if d.get("error"):
        return "__ERROR__"
    want = set(cv.norm(title)[:200].split())
    best = None
    for w in (d.get("results") or []):
        got = set(cv.norm(w.get("title") or "")[:200].split())
        if got and want and len(want & got) / max(1, min(len(want), len(got))) >= 0.85:
            best = w.get("title")
            break
    cache[key] = best
    with open(CACHE, "w") as fh:
        json.dump(cache, fh)
    time.sleep(0.12)
    return best


def recall_against(corpus_recs, rows_by_tier):
    got_t = {cv.norm(r["title"])[:70] for r in corpus_recs if r.get("title")}
    got_d = {r["doi"] for r in corpus_recs if r.get("doi")}
    hit = {}
    for tier, rows in rows_by_tier.items():
        n = ok = 0
        for title, doi in rows:
            n += 1
            if cv.norm(title)[:70] in got_t or (doi and doi in got_d):
                ok += 1
        hit[tier] = (ok, n, round(100 * ok / n, 1) if n else None)
    return hit


def main():
    cache = load_cache()
    corpus = json.load(open(CORPUS))["records"]
    tier_b = json.load(open(TIER_B))

    repairs, unrepaired = [], []
    for r in tier_b:
        t = r.get("title") or ""
        if not t or not looks_like_citation(t):
            continue
        new, how = extract_title(t)
        if new:
            repairs.append({"row": r, "old": t, "new": new, "method": how})
        else:
            unrepaired.append({"row": r, "old": t, "reason": how})

    # Apply repairs to a COPY. The frozen frame is never mutated in place.
    repaired_rows, applied = [], {}
    for r in tier_b:
        rr = dict(r)
        repaired_rows.append(rr)
        applied[id(r)] = rr
    for rep in repairs:
        rr = applied[id(rep["row"])]
        rr["title"] = rep["new"]
        rr["title_key"] = cv.norm(rep["new"])[:120]
        rr["_repaired_from_citation_string"] = rep["old"]

    # Merge duplicates the repair exposed.
    seen, deduped, merged = {}, [], []
    for rr in repaired_rows:
        k = cv.norm(rr.get("title") or "")[:70]
        if not k:
            deduped.append(rr); continue
        if k in seen:
            merged.append({"kept": seen[k].get("title"), "dropped": rr.get("title"),
                           "was_repaired": "_repaired_from_citation_string" in rr})
            if not seen[k].get("doi") and rr.get("doi"):
                seen[k]["doi"] = rr["doi"]
            continue
        seen[k] = rr
        deduped.append(rr)
    json.dump(deduped, open(OUT_FRAME, "w"), indent=1)

    # ---- re-measure --------------------------------------------------------------------------
    before = recall_against(corpus, {"B_ONLY": [(r.get("title") or "", r.get("doi"))
                                                for r in tier_b if r.get("title")]})
    after = recall_against(corpus, {"B_ONLY": [(r.get("title") or "", r.get("doi"))
                                               for r in deduped if r.get("title")]})

    # Confidence labels only -- computed after the repair, and they change nothing above.
    conf = Counter()
    for rep in repairs:
        v = oa_exists(rep["new"], cache)
        rep["oa"] = None if v == "__ERROR__" else v
        conf["unconfirmed" if v == "__ERROR__" else ("in_openalex" if v else "not_in_openalex")] += 1

    # ---- the like-for-like number ------------------------------------------------------------
    # `103_` reports A_ONLY / B_ONLY / BOTH off `cv.load()`, which drops Tier-B rows that overlap
    # Tier A and dedupes on the normalised title. The raw Tier-B figures above are NOT on that basis,
    # so quoting them next to the 82.4% headline would be comparing two different denominators.
    # cv.load()'s construction is replicated here against the repaired frame to get a number that is
    # actually comparable.
    def cvstyle(frame):
        """cv.load()'s partition, but with a DOI join that actually works.

        `103_` resolves each gold row's DOI by looking it up in the Tier-B frame under
        `norm(title)[:120]`. That join is broken in both directions and every recall figure this
        chapter has published rests on it:

          - **64 of 400 Tier-B rows carry a stale `title_key`** that no longer equals
            `norm(current title)`, because `98_` set the key from the raw snowball title and
            enrichment then rewrote the title to the provider's canonical form -- the A6a defect,
            still live. 60 of those 64 have a DOI that the lookup therefore never finds, so those
            rows fall back to title-only matching and are scored as misses when a DOI would have
            matched them.
          - **Tier A's own `doi` field is never consulted at all**, though all 48 rows carry one.
            A Tier-A row is only credited a DOI if its normalised title happens to collide with a
            Tier-B key, which is arbitrary.

        Each row's own `doi` field is used here instead. That is not a refinement; it is the join
        the measurement was always supposed to make.
        """
        tier_a = json.load(open(os.path.join(LOGS, f"{SLUG}-tier-a.json")))
        bkeys = {r["title_key"] for r in frame if r.get("title_key")}
        bkeys |= {cv.norm(r["title"])[:120] for r in frame if r.get("title")}
        out, seen = [], set()
        for r in tier_a:
            if r.get("role") != "EMPIRICAL" or not r.get("title"):
                continue
            k = cv.norm(r["title"])[:70]
            if k in seen:
                continue
            seen.add(k)
            in_b = (r.get("title_key") in bkeys) or (cv.norm(r["title"])[:120] in bkeys)
            out.append((r["title"], r.get("doi"), "BOTH" if in_b else "A_ONLY"))
        akeys = {cv.norm(t)[:70] for t, _, _ in out}
        for r in frame:
            if not r.get("title"):
                continue
            k = cv.norm(r["title"])[:70]
            if k in seen or k in akeys:
                continue
            seen.add(k)
            out.append((r["title"], r.get("doi"), "B_ONLY"))
        tiers = {}
        for title, doi, tier in out:
            tiers.setdefault(tier, []).append((title, doi))
        return recall_against(corpus, tiers)

    cv_before, cv_after = cvstyle(tier_b), cvstyle(deduped)

    def weighted(h):
        tot = sum(v[1] for v in h.values())
        return round(sum(v[0] for v in h.values()) / tot * 100, 1) if tot else None, tot

    w_before, n_before = weighted(cv_before)
    w_after, n_after = weighted(cv_after)

    b_before, b_after = before["B_ONLY"], after["B_ONLY"]
    L = ["# D.1.a — gold-set repair: citation strings, and what they were costing", "",
         "`107_` found that 24 of the 68 gold records missing from the v2 corpus store an entire "
         "bibliography line where a title belongs — Crossref's `unstructured` field, which "
         "`93_`/`96_` fall back to. A3 found 27 of these and did not fully repair them. **Such a row "
         "cannot match by title however complete the index is, so it depresses measured "
         "Recall(B-only) while saying nothing about coverage.**", "",
         "## The decision that would have rigged this", "",
         "Titles are extracted **by parsing the string only**. The obvious alternative — search each "
         "citation against OpenAlex and adopt the best match's title — is more accurate per record "
         "and is disqualified: it repairs only the rows OpenAlex can confirm, so the repaired gold "
         "becomes a set of works OpenAlex is known to hold and the recall it then measures is "
         "*guaranteed* to rise. **The measurement would be an artifact of its own repair.** Parsing "
         "is provider-independent, so a work whose title we recover but which OpenAlex does not hold "
         "correctly stays a miss. Provider lookup runs afterwards and only labels confidence.", "",
         f"- citation-string rows found in Tier B: **{len(repairs) + len(unrepaired)}**",
         f"- repaired: **{len(repairs)}**",
         f"- left unrepaired (no year anchor — still counted as misses): **{len(unrepaired)}**",
         f"- duplicates the repair exposed and merged: **{len(merged)}**",
         f"- Tier-B rows: {len(tier_b)} → **{len(deduped)}**", "",
         "## Re-measured recall against the v2 corpus", "",
         "| gold set | matched | n | Recall(B-only) |", "|---|---|---|---|",
         f"| as frozen | {b_before[0]} | {b_before[1]} | {b_before[2]}% |",
         f"| **repaired** | **{b_after[0]}** | **{b_after[1]}** | **{b_after[2]}%** |", "",
         "### On the same basis as the headline recall figures", "",
         "`103_` reports A-only / B-only / both off `cv.load()`, which drops Tier-B rows overlapping "
         "Tier A and dedupes on the normalised title. The raw Tier-B table above is **not** that "
         "basis, so this is the comparable one.", "",
         "| tier | before | after |", "|---|---|---|"]
    for t in ("A_ONLY", "B_ONLY", "BOTH"):
        bb, aa = cv_before.get(t), cv_after.get(t)
        if bb and aa:
            L.append(f"| {t} | {bb[2]}% (n={bb[1]}) | **{aa[2]}%** (n={aa[1]}) |")
    L += [f"| **weighted** | {w_before}% (n={n_before}) | **{w_after}%** (n={n_after}) |", "",
         f"**The denominator moved as well as the numerator** ({b_before[1]} → {b_after[1]}), because "
         f"merging duplicates removes rows. A recall figure that moved only because rows were "
         f"deleted would be meaningless, so both are shown.", "",
         "## Confidence labels — computed AFTER the repair, and they decided nothing", "",
         f"- repaired title found in OpenAlex: **{conf['in_openalex']}**",
         f"- repaired title not found: **{conf['not_in_openalex']}** — these stay misses, correctly",
         f"- unconfirmed (provider refused): {conf['unconfirmed']}", "",
         "## Every repair, for reading", ""]
    for rep in repairs:
        L.append(f"- **{rep['new'][:110]}**")
        L.append(f"  - from: `{rep['old'][:150]}`")
        if rep.get("oa") and cv.norm(rep["oa"])[:60] != cv.norm(rep["new"])[:60]:
            L.append(f"  - OpenAlex holds: *{rep['oa'][:110]}*")
    if unrepaired:
        L += ["", "## Left unrepaired — no year anchor to parse from", "",
              "Left exactly as found and still counted as misses. A low repair rate is the correct "
              "outcome when the strings cannot be parsed; relaxing the rule to lift it is how the "
              "OAS run acquired a 40%-ghost Tier B.", ""]
        L += [f"- `{u['old'][:150]}`" for u in unrepaired]
    if merged:
        L += ["", "## Duplicates exposed by the repair", ""]
        L += [f"- kept *{m['kept'][:90]}* / dropped *{(m['dropped'] or '')[:90]}*" for m in merged]
    open(OUT_MD, "w").write("\n".join(L) + "\n")

    print(f"citation rows {len(repairs) + len(unrepaired)} | repaired {len(repairs)} | "
          f"unrepaired {len(unrepaired)} | merged {len(merged)}", file=sys.stderr)
    print(f"raw TierB {b_before[2]}% (n={b_before[1]}) -> {b_after[2]}% (n={b_after[1]})",
          file=sys.stderr)
    for t in ("A_ONLY", "B_ONLY", "BOTH"):
        if t in cv_before:
            print(f"  {t:8s} {cv_before[t][2]}% (n={cv_before[t][1]}) -> "
                  f"{cv_after[t][2]}% (n={cv_after[t][1]})", file=sys.stderr)
    print(f"  WEIGHTED {w_before}% (n={n_before}) -> {w_after}% (n={n_after})", file=sys.stderr)
    print(f"wrote {OUT_FRAME}\nwrote {OUT_MD}", file=sys.stderr)


if __name__ == "__main__":
    main()
