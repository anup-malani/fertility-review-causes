#!/usr/bin/env python3
r"""
107_d1a_miss_decomposition.py — D.1.a. Is the residual recall gap a query hole or an index gap?

WHY. The v2 pull lifted Recall(A-only) 78.9 -> 94.7 and both-channels 91.7 -> 100, and recovered all
three Tier-1 natural experiments. Recall(B-only) moved only 80.8 -> 82.4 and sits ~10 points under
A6b's cross-validated 92.1%. Before spending another repair round on the query, the gap has to be
split, because the two halves have opposite implications:

  QUERY HOLE  — the work is in OpenAlex and the query does not reach it. Fixable, and a reason to
                iterate on the vocabulary.
  INDEX GAP   — the work is not in OpenAlex at all. NOT fixable by any query, and it is a ceiling:
                Recall(B-only) cannot exceed 100% minus this share no matter what we search for.

Getting this backwards in either direction is expensive. Treating an index gap as a query hole buys
endless query rounds that cannot work; treating a query hole as an index gap writes a false
limitation into §10 and stops looking.

THE TEST IS FREE. Entity lookup by DOI costs $0 under OpenAlex's usage pricing, so every missed gold
record with a DOI can be checked directly. This is the same pricing fact that retracted the
"OpenAlex canon resolution is dead" claim.

This chapter has already hit a non-Anglo-European indexing gap five separate times -- the AJRH
unregistered DOI, the NOT_INDEXED regional reviews, Dutch-language Lesthaeghe and van de Kaa 1986,
the Crossref backfill residue, and the book-review leads. If the residue here is the same material,
that is the sixth appearance and it belongs in §10 next to the geographic-skew limitation rather
than in another query round.

Usage:  python3 107_d1a_miss_decomposition.py [--query v2]
Output: literature/search-logs/{slug}-miss-decomposition.{json,md}
"""
import json, os, re, subprocess, sys, time, urllib.parse
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import importlib.util

SLUG = "postmaterialism-individualism-secularization"
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
LOGS = os.path.join(ROOT, "literature", "search-logs")
SUF = "-v2" if "--query" in sys.argv and sys.argv[sys.argv.index("--query") + 1] == "v2" else ""
CORPUS = os.path.join(LOGS, f"{SLUG}-live-corpus{SUF}.json")
OUT_JSON = os.path.join(LOGS, f"{SLUG}-miss-decomposition.json")
OUT_MD = os.path.join(LOGS, f"{SLUG}-miss-decomposition.md")
CACHE = os.path.join(HERE, "d1a_miss_decomp_cache.json")

KEY = os.environ.get("OPENALEX_API_KEY", "").strip()
UA = "fertility-review/1.0 (mailto:shravanh@uchicago.edu)"

_spec = importlib.util.spec_from_file_location("cv", os.path.join(HERE, "101_d1a_cv_breadth.py"))
cv = importlib.util.module_from_spec(_spec)
sys.modules["cv"] = cv
_spec.loader.exec_module(cv)


def load_cache():
    if os.path.exists(CACHE):
        with open(CACHE) as fh:
            return json.load(fh)
    return {}


def doi_lookup(doi, cache):
    """Free entity lookup. Returns the OpenAlex title, or None if the work is not indexed."""
    if doi in cache:
        return cache[doi]
    p = {"select": "id,title,publication_year,type,language"}
    if KEY:
        p["api_key"] = KEY
    url = f"https://api.openalex.org/works/https://doi.org/{doi}?" + urllib.parse.urlencode(p)
    r = subprocess.run(["curl", "-s", "-m", "45", "-A", UA, url], capture_output=True, text=True)
    try:
        d = json.loads(r.stdout)
    except Exception:
        return "__ERROR__"
    # A refusal is not an absence. Only an explicit not-found counts as "not indexed".
    if d.get("error"):
        msg = str(d.get("message", "")).lower()
        if "not found" in msg or "does not exist" in str(d.get("error")).lower():
            val = None
        else:
            return "__ERROR__"
    else:
        val = d.get("title") or ""
    cache[doi] = val
    with open(CACHE, "w") as fh:
        json.dump(cache, fh)
    time.sleep(0.1)
    return val


def main():
    cache = load_cache()
    corp = json.load(open(CORPUS))
    recs = corp["records"]
    got_titles = {cv.norm(r["title"])[:70] for r in recs if r.get("title")}
    got_dois = {r["doi"] for r in recs if r.get("doi")}

    tier_b = {r["title_key"]: r for r in
              json.load(open(os.path.join(LOGS, f"{SLUG}-tier-b-frame.json"))) if r.get("title_key")}
    gold, _, _ = cv.load()

    misses = []
    for g in gold:
        t = cv.norm(g["title"])[:70]
        rec = tier_b.get(cv.norm(g["title"])[:120]) or {}
        doi = rec.get("doi")
        if t in got_titles or (doi and doi in got_dois):
            continue
        misses.append({"title": g["title"], "tier": g["tier"], "doi": doi,
                       "resolution": g.get("resolution") or rec.get("resolution")})

    def title_probe(title):
        """Billed title search, for records with no DOI. Existence test only, never a retrieval test.

        The no-DOI class is 90% of the misses here, so leaving it untested makes the whole
        decomposition vacuous -- and reporting a ceiling computed as though the untested records did
        not exist is worse than reporting nothing. A billed search is $0.001; sixty of them is six
        cents.

        Matching is deliberately conservative and asymmetric. A confident title match means the work
        IS indexed, which is a real finding. Anything short of that is `UNCONFIRMED`, never
        `INDEX_GAP` -- `95_` already recorded that a Jaccard gate false-negatives on subtitle drops
        (Hagestad and Call scored 0.43 against a 0.55 bar with both surnames and the year matching),
        so a weak similarity score is not evidence a paper does not exist.
        """
        # v2 of this probe. v1 built `filter=title.search:<title>` with the title ALREADY
        # url-quoted and then handed the whole thing to urlencode -- double-encoding it -- and it
        # also pushed the title's commas into a filter string where the comma is the AND separator.
        # The result was a probe that found almost nothing and returned 61 "probable index gaps",
        # including "Changing Attitudes toward Marriage and Children in Six Countries", which
        # OpenAlex holds under that exact title. A hand spot-check of four records caught it; the
        # count on its own looked entirely plausible.
        # `search` is used rather than `title.search` because this is an EXISTENCE test, and a
        # forgiving matcher failing toward "it exists" is the safe direction here: it can only ever
        # move a record out of the index-gap class, which is the class that would otherwise become a
        # permanent limitation in §10.
        key = "t2::" + cv.norm(title)[:80]
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
        want = set(cv.norm(title).split()) if hasattr(cv.norm(title), "split") else set()
        want = set(cv.norm(title)[:200].split())
        best = None
        for w in (d.get("results") or []):
            got = set(cv.norm(w.get("title") or "")[:200].split())
            if not got or not want:
                continue
            # containment of the shorter token set in the longer -- survives subtitle drops
            ov = len(want & got) / max(1, min(len(want), len(got)))
            if ov >= 0.85:
                best = w.get("title")
                break
        cache[key] = best
        with open(CACHE, "w") as fh:
            json.dump(cache, fh)
        time.sleep(0.12)
        return best

    # A THIRD CLASS THE FIRST TWO RUNS CONFLATED WITH INDEX GAPS. A3 recorded that 27 of 495 Tier-B
    # "titles" are entire citation strings, because Crossref reference lists carry an `unstructured`
    # field that `93_`/`96_` fall back to. Such a record CANNOT match by title no matter what is
    # indexed -- the stored title is a bibliography line, not a title -- so counting it as an index
    # gap attributes a defect in our own gold set to OpenAlex's coverage. Visible in the residue as
    # the same work appearing twice: "Report on analysis of ESS data..." classified QUERY_HOLE, and
    # "Liefbroer, A. C., & Merz, E.-M. (2009). Report on analysis of ESS data..." classified as a
    # probable gap. One work, two gold rows, one of them malformed.
    CITATION_MARKS = [
        re.compile(r"\(\s*(19|20)\d{2}\s*\)"),            # a year in parentheses
        re.compile(r"^[A-Z][a-z]+,\s*[A-Z]\.\s*"),        # "Liefbroer, A. C., ..."
        re.compile(r"\s&\s"),                              # ampersand between authors
        re.compile(r"^(?:[A-Z]{1,3}\s+[A-Z][a-z]+\s+){2,}"),   # "B Arpino G Esping-Andersen ..."
        re.compile(r"\bdoi:\s*10\.", re.I),
        re.compile(r"\bpp\.\s*\d+", re.I),
    ]

    def looks_like_citation(t):
        return any(rx.search(t) for rx in CITATION_MARKS)

    classified, errs = [], 0
    for m in misses:
        if looks_like_citation(m["title"]):
            m["verdict"] = "GOLD_DEFECT_CITATION_STRING"
        elif not m["doi"]:
            probe = title_probe(m["title"])
            if probe == "__ERROR__":
                m["verdict"] = "UNCONFIRMED"; errs += 1
            elif probe:
                m["verdict"] = "QUERY_HOLE"; m["openalex_title"] = probe
                m["evidence"] = "no DOI; matched by title probe"
            else:
                # Not found by title either. Stated as PROBABLE, not proven: an unindexed title and
                # a title our normaliser cannot match look identical from here.
                m["verdict"] = "INDEX_GAP_PROBABLE"
        else:
            oa_title = doi_lookup(m["doi"], cache)
            if oa_title == "__ERROR__":
                m["verdict"] = "UNCONFIRMED"          # never counted as either half
                errs += 1
            elif oa_title is None:
                m["verdict"] = "INDEX_GAP"
            else:
                m["verdict"] = "QUERY_HOLE"
                m["openalex_title"] = oa_title
        classified.append(m)

    tally = Counter(m["verdict"] for m in classified)
    n_gold = len(gold)
    n_miss = len(classified)
    # THE CEILING IS A BOUND, NOT A NUMBER. The first version computed it from confirmed INDEX_GAP
    # alone and printed "100.0%" while 61 of 68 misses had never been tested at all -- a ceiling
    # derived by treating untested records as though they did not exist. The unresolved classes sit
    # between the two bounds and are reported as width rather than resolved by assumption.
    unresolved = tally["UNCONFIRMED"] + tally["NO_DOI_UNTESTABLE"] \
        + tally["GOLD_DEFECT_CITATION_STRING"]
    hard_gap = tally["INDEX_GAP"] + tally["INDEX_GAP_PROBABLE"]
    ceil_hi = 100 * (1 - tally["INDEX_GAP"] / n_gold) if n_gold else None
    ceil_lo = 100 * (1 - (hard_gap + unresolved) / n_gold) if n_gold else None

    out = {"slug": SLUG, "corpus": os.path.basename(CORPUS), "gold_n": n_gold,
           "misses": n_miss, "tally": dict(tally), "unconfirmed": errs,
           "recall_ceiling_pct_range": [round(ceil_lo, 1) if ceil_lo else None,
                                       round(ceil_hi, 1) if ceil_hi else None],
           "records": classified}
    json.dump(out, open(OUT_JSON, "w"), indent=1)

    L = ["# D.1.a — why the remaining gold is missing: query hole or index gap?", "",
         "The v2 pull recovered all three Tier-1 natural experiments and took Recall(A-only) to "
         "94.7% and both-channels to 100%, but Recall(B-only) moved only 80.8 → 82.4. **Before "
         "another repair round, the residue has to be split**, because the halves point opposite "
         "ways: a query hole is fixable and argues for iterating, an index gap is a ceiling no query "
         "can pass and belongs in §10.", "",
         "Entity lookup by DOI is **free** under OpenAlex's pricing, so every missed record carrying "
         "a DOI is checked directly. A provider refusal is recorded as `UNCONFIRMED` and counted as "
         "neither half — a refusal is not an absence.", "",
         f"- gold records: **{n_gold}**",
         f"- missing from the corpus: **{n_miss}**",
         f"- **INDEX_GAP** (not in OpenAlex at all — unfixable by any query): "
         f"**{tally['INDEX_GAP']}**",
         f"- **QUERY_HOLE** (in OpenAlex, query did not reach it — fixable): "
         f"**{tally['QUERY_HOLE']}**",
         f"- **INDEX_GAP_PROBABLE** (no DOI, and no title match either): "
         f"**{tally['INDEX_GAP_PROBABLE']}**",
         f"- **GOLD_DEFECT** (the stored 'title' is a citation string — cannot match by title, and "
         f"is a defect in our gold set rather than in OpenAlex): "
         f"**{tally['GOLD_DEFECT_CITATION_STRING']}**",
         f"- unconfirmed (provider refused): {tally['UNCONFIRMED']}", ""]
    if ceil_hi is not None:
        L += [f"**Recall ceiling: between {ceil_lo:.1f}% and {ceil_hi:.1f}%.** Reported as a bound "
              f"rather than a number, because {unresolved} record(s) could not be tested either way "
              f"and the width IS the uncertainty. Treating untested records as present would give a "
              f"falsely clean ceiling.", ""]
    for verdict, heading, note in [
        ("QUERY_HOLE", "Query holes — in OpenAlex, not retrieved",
         "These are the addressable ones. The OpenAlex title is shown because it is what the query "
         "would have had to match, and it is often not the title the gold set stored."),
        ("INDEX_GAP", "Index gaps — not in OpenAlex",
         "Not reachable by any query against this provider. If these are book chapters, "
         "dissertations, regional and non-English work, this is the sixth appearance of the "
         "indexing gap this chapter has documented, and it belongs in §10."),
        ("INDEX_GAP_PROBABLE", "Probably not indexed — no DOI and no title match",
         "Stated as PROBABLE and never as proven: an unindexed title and a title our normaliser "
         "cannot match look identical from here."),
        ("GOLD_DEFECT_CITATION_STRING", "Gold-set defects — the stored title is a citation string",
         "A3 found 27 of these; they cannot match by title however complete the index is. They "
         "depress measured Recall(B-only) without saying anything about coverage, and they should be "
         "repaired in the gold set rather than chased in the query."),
        ("UNCONFIRMED", "Unconfirmed — the provider refused",
         "A refusal is not an absence. Counted as neither half."),
    ]:
        rows = [m for m in classified if m["verdict"] == verdict]
        if not rows:
            continue
        L += [f"## {heading} — {len(rows)}", "", f"*{note}*", ""]
        for m in rows[:40]:
            L.append(f"- {m['title'][:120]}")
            if m.get("openalex_title") and cv.norm(m["openalex_title"])[:60] != \
                    cv.norm(m["title"])[:60]:
                L.append(f"  - OpenAlex holds it as: *{m['openalex_title'][:120]}*")
        if len(rows) > 40:
            L.append(f"- … and {len(rows) - 40} more")
        L.append("")
    open(OUT_MD, "w").write("\n".join(L) + "\n")
    print(f"gold {n_gold} | misses {n_miss} | index_gap {tally['INDEX_GAP']} | "
          f"index_gap_probable {tally['INDEX_GAP_PROBABLE']} | query_hole {tally['QUERY_HOLE']} | "
          f"unconfirmed {errs}", file=sys.stderr)
    if ceil_hi is not None:
        print(f"recall ceiling between {ceil_lo:.1f}% and {ceil_hi:.1f}%", file=sys.stderr)
    print(f"wrote {OUT_JSON}\nwrote {OUT_MD}", file=sys.stderr)


if __name__ == "__main__":
    main()
