#!/usr/bin/env python3
"""
212 — A.23 seed harvest from the finished C.2.c (housing costs) artifacts.

TICK-075. C.2.c's search-scope ruling (2026-07-31) sends every record whose treatment
is the LIVING ARRANGEMENT itself, with no price variation, out of C.2.c and into A.23.
Those records were found, screened and abstract-fetched at C.2.c's expense; they are
hand-sourced seeds for this chapter and belong in its evidence base from the start
(the Tier-A-anchors-are-studies lesson from D.2.d).

Three sources, kept separate so provenance stays visible:
  1. C.2.c's screened frame, records carrying a provisional_cell that routes here.
  2. C.2.c's cold-start anchor set, same test.
  3. C.2.c's raw snowball pool (10,915 records), mined on A.23's exposure vocabulary.
     This is the wide channel; it is NOT pre-screened and its precision is measured
     below rather than assumed.

Output: literature/search-logs/co-residence-parents-household-delay-c2c-seed-harvest.json
        plus a counts summary on stdout.

Usage: python3 source/build/goldset/212_a23_harvest_c2c_seeds.py
"""
import json
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
LOGS = ROOT / "literature" / "search-logs"
OUT = LOGS / "co-residence-parents-household-delay-c2c-seed-harvest.json"

# Cells C.2.c defined that route to, or adjoin, A.23.
ROUTED_CELLS = {"OFF_LIVING_ARRANGEMENT_A23", "HOUSING_ONLY_MECHANISM"}

# --- vocabulary -------------------------------------------------------------
# The exposure axis is a LIVING ARRANGEMENT, and it is named as often with a verb
# ("left the parental home", "young adults living with parents") as with a noun
# phrase, so the patterns are deliberately verb-tolerant. This is the A.24 lesson:
# a noun-phrase-only exposure axis silently misses the verb-phrased half.
EXPOSURE = [
    r"co-?resid",              # coresidence, co-residing, coresident
    r"living with (?:their |her |his )?parents?",
    r"liv(?:e|es|ing|ed) at home",
    r"parental (?:home|nest|household)",
    r"leav(?:e|es|ing|ing the)? (?:the )?(?:parental |family )?(?:home|nest)",
    r"home-?leaving",
    r"nest-?leav",
    r"boomerang",
    r"returning home",
    r"residential (?:independence|autonomy)",
    r"leaving home",
    r"multigenerational (?:household|living|famil)",
    r"intergenerational (?:household|co-?resid)",
    r"extended (?:family )?household",
    r"household formation",
    r"independent (?:household|living)",
    r"transition to adulthood",
    r"young adults? (?:still )?(?:liv|resid|stay)",
]
# The outcome axis. Kept separate so each axis can be scored alone — the
# anchored-vocabulary lesson: never trust a block of terms you have not scored
# term by term.
OUTCOME = [
    r"fertilit",
    r"childbear",
    r"child-?bearing",
    r"first birth",
    r"birth rate",
    r"transition to parenthood",
    r"parenthood",
    r"union formation",
    r"partnership formation",
    r"family formation",
    r"marriage timing",
    r"age at marriage",
    r"tfr\b",
]
# The homonym this chapter has to live with: "co-residence with parents" is also
# the standard term for an ADULT CHILD HOUSING AN ELDERLY PARENT — a large
# gerontology and long-term-care literature with the same words and the opposite
# direction of dependency. Flagged, not dropped, so the scope can size it.
ELDERCARE = [
    r"elder(?:ly|care)",
    r"older parents?",
    r"ageing|aging",
    r"long-?term care",
    r"caregiv",
    r"dementia",
    r"widow",
    r"filial",
    r"old-?age support",
    r"nursing home",
]

EXPOSURE_RE = [(p, re.compile(p, re.I)) for p in EXPOSURE]
OUTCOME_RE = [(p, re.compile(p, re.I)) for p in OUTCOME]
ELDERCARE_RE = [(p, re.compile(p, re.I)) for p in ELDERCARE]


def fold(s):
    """NFKD fold that keeps latin letters instead of shattering them to spaces.

    The norm() defect logged on D.1.a turned Speder into 'der'; here accented
    European author and place names are common, so the fold translitera[te]s.
    """
    if not s:
        return ""
    s = unicodedata.normalize("NFKD", s)
    return "".join(c for c in s if not unicodedata.combining(c)).lower()


def hits(text, patterns):
    return [p for p, rx in patterns if rx.search(text)]


def classify(rec):
    text = fold(" ".join(str(rec.get(k) or "") for k in ("title", "abstract")))
    ex = hits(text, EXPOSURE_RE)
    ou = hits(text, OUTCOME_RE)
    el = hits(text, ELDERCARE_RE)
    return ex, ou, el


def load(name):
    p = LOGS / name
    if not p.exists():
        print(f"  [missing] {name}", file=sys.stderr)
        return []
    return json.load(p.open())


def main():
    out = {"routed": [], "anchors": [], "mined": []}
    term_counts = {p: 0 for p in EXPOSURE}

    # --- source 1: C.2.c's screened frame, on the routing label ---------------
    frame = load("housing-costs-screen-pass2.json")
    for r in frame:
        if r.get("provisional_cell") in ROUTED_CELLS:
            ex, ou, el = classify(r)
            out["routed"].append({
                "openalex": r.get("openalex"), "doi": r.get("doi"),
                "title": r.get("title"), "year": r.get("year"),
                "venue": r.get("venue"), "cited_by": r.get("cited_by"),
                "c2c_cell": r.get("provisional_cell"),
                "c2c_prescreen_rule": r.get("prescreen_rule"),
                "exposure_terms": ex, "outcome_terms": ou, "eldercare_terms": el,
                "provenance": "c2c_screened_frame_routed",
            })

    # --- source 2: C.2.c's verified cold-start anchors ------------------------
    for a in load("housing-costs-cold-start-anchors.json"):
        if a.get("provisional_cell") in ROUTED_CELLS:
            out["anchors"].append({
                "title": a.get("title"), "doi": a.get("doi"), "year": a.get("year"),
                "container": a.get("container"), "existence": a.get("existence"),
                "c2c_cell": a.get("provisional_cell"),
                "provenance": "c2c_cold_start_anchor_routed",
            })

    # --- source 3: the raw snowball pool, mined on vocabulary -----------------
    # The pool is TITLE-ONLY: 0 of 10,915 records carry an abstract. Requiring a hit
    # on BOTH axes therefore tests whether one title happens to name the living
    # arrangement AND a fertility outcome, which almost no title does — it returned 6.
    # Mine on the exposure axis alone and record whether the outcome is also visible;
    # an absent outcome word in a title is not evidence of an absent outcome.
    pool = load("housing-costs-snowball-pool.json")
    seen = {r["openalex"] for r in out["routed"] if r.get("openalex")}
    for r in pool:
        ex, ou, el = classify(r)
        for p in ex:
            term_counts[p] += 1
        if not ex:
            continue
        if r.get("openalex") in seen:
            continue
        out["mined"].append({
            "openalex": r.get("openalex"), "doi": r.get("doi"),
            "title": r.get("title"), "year": r.get("year"),
            "venue": r.get("venue"), "cited_by": r.get("cited_by"),
            "n_seeds": r.get("n_seeds"),
            "c2c_provisional_relevance": r.get("provisional_relevance"),
            "exposure_terms": ex, "outcome_terms": ou, "eldercare_terms": el,
            "outcome_in_title": bool(ou),
            "eldercare_flag": bool(el),
            "provenance": "c2c_snowball_pool_mined",
        })

    out["mined"].sort(key=lambda r: (not r["outcome_in_title"], -(r.get("cited_by") or 0)))

    meta = {
        "ticket": "TICK-075",
        "hypothesis": "A.23 co-residence-parents-household-delay",
        "source_pool_size": len(pool),
        "source_frame_size": len(frame),
        "counts": {k: len(v) for k, v in out.items()},
        "mined_with_outcome_word_in_title": sum(1 for r in out["mined"] if r["outcome_in_title"]),
        "eldercare_flagged_in_mined": sum(1 for r in out["mined"] if r["eldercare_flag"]),
        "exposure_term_yield_over_full_pool": term_counts,
    }
    OUT.write_text(json.dumps({"meta": meta, **out}, indent=1))

    print(f"pool={len(pool)}  frame={len(frame)}")
    for k, v in out.items():
        print(f"  {k:8s} {len(v)}")
    print(f"  mined carrying an outcome word in the title: {meta['mined_with_outcome_word_in_title']}")
    print(f"  eldercare-flagged within mined: {meta['eldercare_flagged_in_mined']}")
    print("\nexposure term yield over the full 10.9k pool (term-by-term, not the block):")
    for p, n in sorted(term_counts.items(), key=lambda kv: -kv[1]):
        print(f"  {n:6d}  {p}")
    print(f"\nwrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
