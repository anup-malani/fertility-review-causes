#!/usr/bin/env python3
"""
225 — A.23: does the production frame miss what the snowball already found?

TICK-075. The frame and the snowball pool were built by independent channels --
a boolean query over OpenAlex, and citation traversal from 33 gated anchors -- and
they overlap by only 8.1% of the frame (127 of 1,570). That is a recall question
the 12-record gold set is too small to answer.

This is the stronger test: take the snowball pool's records that LOOK on-topic on
their titles, and ask how many of them the production query fails to reach. Gold
recall says "no known miss" on 12 partly non-independent anchors; this says how
many plausible records a 3,793-record independent channel found that the query
does not.

A miss here is not automatically a query defect -- a pool record can be off-cell,
or can lack an abstract so that the query has only a title to match on. The output
separates those cases instead of reporting one number.

Usage: python3 source/build/goldset/225_a23_frame_recall_vs_pool.py
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
LOGS = ROOT / "literature" / "search-logs"
POOL = LOGS / "co-residence-parents-household-delay-snowball-pool.json"
FRAME = LOGS / "co-residence-parents-household-delay-frame.json"
OUT = LOGS / "co-residence-parents-household-delay-frame-recall.json"

ARRANGEMENT = re.compile(
    r"co-?resid\w*|living with (?:their |her |his )?parents?|liv\w* at home|"
    r"parental (?:home|nest)|leav\w* (?:the )?(?:parental |family )?(?:home|nest)|"
    r"home-?leaving|nest-?leav|boomerang|residential (?:independence|autonomy)|"
    r"household formation|independent household|multigenerational|three-?generation|"
    r"extended household|stem family|parents?-in-law|in-laws|patrilocal|"
    r"living arrangement|household structure|household composition", re.I)
FERT = re.compile(
    r"fertilit|childbear|child-?bearing|first birth|second birth|birth rate|"
    r"parenthood|childless|family size|number of children|birth intention|"
    r"fertility intention|tfr\b", re.I)


def main():
    pool = json.loads(POOL.read_text())
    frame_doc = json.loads(FRAME.read_text())
    frame = frame_doc["records"]
    in_frame = {r["openalex"] for r in frame}

    # pool records that look on-topic on the title alone
    candidates = [r for r in pool
                  if ARRANGEMENT.search(r["title"] or "") and FERT.search(r["title"] or "")]
    missed = [r for r in candidates if r["openalex"] not in in_frame]
    reached = len(candidates) - len(missed)

    # why might a candidate be missed? separate the diagnosable cases.
    def why(r):
        t = r["title"] or ""
        # the query matches title AND abstract; a pool record has no abstract here,
        # so a title-only phrasing outside the cause axis is the usual reason.
        if not ARRANGEMENT.search(t):
            return "no_arrangement_in_title"
        axis_terms = re.compile(
            r"co-?resid|living with parents|living at home|parental home|leaving home|"
            r"leaving the parental home|home leaving|nest leaving|residential independence|"
            r"boomerang|household formation|independent household|multigenerational household|"
            r"three-generation household|extended household|stem family|parents-in-law|"
            r"grandparental childcare|grandparent childcare|intergenerational coresidence|"
            r"intergenerational co-residence|living with in-laws|patrilocal", re.I)
        if not axis_terms.search(t):
            return "arrangement_worded_outside_the_axis"
        return "in_axis_but_not_retrieved"

    buckets = {}
    for r in missed:
        buckets.setdefault(why(r), []).append(r)

    print(f"snowball pool                    {len(pool)}")
    print(f"  looks on-topic on title alone  {len(candidates)}")
    print(f"  reached by the frame           {reached}")
    print(f"  MISSED by the frame            {len(missed)}"
          f"   ({round(100 * len(missed) / max(1, len(candidates)), 1)}%)")
    print()
    for k, v in sorted(buckets.items(), key=lambda kv: -len(kv[1])):
        print(f"  {k:38s} {len(v)}")
        for r in sorted(v, key=lambda x: -(x["cited_by"] or 0))[:8]:
            print(f"      {r['year']} [{(r['cited_by'] or 0):>4}] {(r['title'] or '')[:70]}")
        print()

    OUT.write_text(json.dumps({
        "meta": {
            "ticket": "TICK-075",
            "test": "Independent-channel recall: what does the snowball pool contain that the "
                    "production query does not reach? Stronger than the 12-record gold set.",
            "pool_size": len(pool), "frame_size": len(frame),
            "on_topic_by_title_in_pool": len(candidates),
            "reached": reached, "missed": len(missed),
            "miss_rate_pct": round(100 * len(missed) / max(1, len(candidates)), 1),
            "caveat": "A pool record carries a title and no abstract, so 'missed' includes records "
                      "the query would match on an abstract it never saw. This is an upper bound on "
                      "the query's true miss rate, not an estimate of it.",
        },
        "missed_by_reason": {k: [{"doi": r["doi"], "title": r["title"], "year": r["year"],
                                  "cited_by": r["cited_by"], "n_seeds": r["n_seeds"]}
                                 for r in sorted(v, key=lambda x: -(x["cited_by"] or 0))]
                             for k, v in buckets.items()},
    }, indent=1))
    print(f"wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
