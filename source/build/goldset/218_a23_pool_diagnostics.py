#!/usr/bin/env python3
"""
218 — A.23 snowball pool diagnostics, round 1.

TICK-075. Measures the round-1 pool rather than describing it. Three questions:

  1. What did the DECOY seeds contribute? The standing rule says seed them forward
     as well as backward, on the evidence that decoy clouds run far more on-topic
     than a theory canon. That claim is measured here for this chapter, not assumed.
  2. How does the pool split between the two configurations of Ruling 1? A frame
     that reaches only the extended-household arm would reproduce the imbalance
     already found in anchor sourcing rather than testing it.
  3. Which seeds were truncated by the forward cap, and what does that cost? A
     capped pull sorted by citation count is the high-citation HEAD, not a sample.
     No silent caps: what was dropped is printed.

On-topic is scored on TITLE ONLY, because that is all the pool carries. It is a
floor on the true rate, not an estimate of it, and is labelled as such.

Usage: python3 source/build/goldset/218_a23_pool_diagnostics.py
"""
import json
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
LOGS = ROOT / "literature" / "search-logs"
POOL = LOGS / "co-residence-parents-household-delay-snowball-pool.json"
ANCHORS = LOGS / "co-residence-parents-household-delay-cold-start-anchors.json"
OUT = LOGS / "co-residence-parents-household-delay-pool-diagnostics.json"

PRELAUNCH = re.compile(
    r"co-?resid|living with (?:their )?parents?|liv\w* at home|parental (?:home|nest)|"
    r"leav\w* (?:the )?(?:parental |family )?(?:home|nest)|home-?leaving|nest-?leav|"
    r"boomerang|residential (?:independence|autonomy)|household formation|"
    r"transition to adulthood|young adults?", re.I)
EXTENDED = re.compile(
    r"multigenerational|three-?generation|extended (?:family )?household|stem family|"
    r"parents?-in-law|in-laws|grandparent|grandmother|grandfather|grandchild|"
    r"patrilocal|virilocal|intergenerational co-?resid", re.I)
FERT = re.compile(
    r"fertilit|childbear|child-?bearing|first birth|second birth|birth rate|"
    r"parenthood|childless|family size|number of children|tfr\b", re.I)
ELDER = re.compile(
    r"elder|older (?:adults?|people|parents?)|ag(?:e)?ing|long-?term care|caregiv|"
    r"dementia|widow|filial|nursing home|frail", re.I)


def main():
    pool = json.loads(POOL.read_text())
    anchors = json.loads(ANCHORS.read_text())["anchors"]
    decoy_dois = {a["doi"] for a in anchors if a["provenance_channel"] == "decoy"}
    prelaunch_dois = {a["doi"] for a in anchors if a["provisional_cell"] == "PRIMARY_PRELAUNCH"}
    extended_dois = {a["doi"] for a in anchors if a["provisional_cell"] == "PRIMARY_EXTENDED_COUPLE"}

    def seeds_of(r):
        return set(r["seeds_backward"]) | set(r["seeds_forward"])

    groups = {
        "all": pool,
        "decoy_only": [r for r in pool if seeds_of(r) and seeds_of(r) <= decoy_dois],
        "non_decoy": [r for r in pool if seeds_of(r) - decoy_dois],
        "multi_seed_2plus": [r for r in pool if r["n_seeds"] >= 2],
        "from_prelaunch_seeds": [r for r in pool if seeds_of(r) & prelaunch_dois],
        "from_extended_seeds": [r for r in pool if seeds_of(r) & extended_dois],
    }

    def score(recs):
        n = len(recs) or 1
        pre = sum(1 for r in recs if PRELAUNCH.search(r["title"] or ""))
        ext = sum(1 for r in recs if EXTENDED.search(r["title"] or ""))
        fer = sum(1 for r in recs if FERT.search(r["title"] or ""))
        on = sum(1 for r in recs
                 if (PRELAUNCH.search(r["title"] or "") or EXTENDED.search(r["title"] or ""))
                 and FERT.search(r["title"] or ""))
        eld = sum(1 for r in recs if ELDER.search(r["title"] or ""))
        return {
            "n": len(recs),
            "exposure_prelaunch_pct": round(100 * pre / n, 1),
            "exposure_extended_pct": round(100 * ext / n, 1),
            "fertility_outcome_pct": round(100 * fer / n, 1),
            "on_topic_both_axes_pct": round(100 * on / n, 1),
            "eldercare_vocab_pct": round(100 * eld / n, 1),
        }

    diag = {k: score(v) for k, v in groups.items()}

    print(f"{'group':22s} {'n':>6} {'pre%':>6} {'ext%':>6} {'fert%':>6} {'both%':>6} {'eld%':>6}")
    for k, v in diag.items():
        print(f"{k:22s} {v['n']:>6} {v['exposure_prelaunch_pct']:>6} "
              f"{v['exposure_extended_pct']:>6} {v['fertility_outcome_pct']:>6} "
              f"{v['on_topic_both_axes_pct']:>6} {v['eldercare_vocab_pct']:>6}")

    # --- what the forward cap cost -----------------------------------------
    round1 = json.loads((LOGS / "co-residence-parents-household-delay-snowball-round1.json").read_text())
    capped = [
        {"doi": "10.2307/2807972", "citations": 1359, "pulled": 200, "note": "Reher 1998 — theory/Wall-3 decoy"},
        {"doi": "10.1353/foc.0.0038", "citations": 469, "pulled": 200, "note": "Furstenberg 2010 — narrative review"},
        {"doi": "10.1002/ijpg.231", "citations": 253, "pulled": 200, "note": "Leaving Home in Europe — link-1 anchor"},
        {"doi": "10.2307/353569", "citations": 202, "pulled": 200, "note": "filial responsibility — elder-support decoy"},
    ]
    dropped = sum(c["citations"] - c["pulled"] for c in capped)
    print(f"\nforward cap: 4 of 30 seeds truncated, {dropped} citing works not pulled")
    for c in capped:
        print(f"  {c['doi']:26s} {c['pulled']}/{c['citations']}  {c['note']}")

    top = sorted(pool, key=lambda r: (-r["n_seeds"], -(r["cited_by"] or 0)))[:20]
    print("\nmost-seeded records (the pool's centre):")
    for r in top:
        print(f"  s={r['n_seeds']:2d} [{(r['cited_by'] or 0):>5}] {r['year']} {(r['title'] or '')[:74]}")

    OUT.write_text(json.dumps({
        "meta": {
            "ticket": "TICK-075", "round": 1, "pool_size": len(pool),
            "scoring": "TITLE ONLY — the pool carries no abstracts, so every percentage "
                       "here is a FLOOR on the true rate, not an estimate of it.",
            "forward_cap_cost": {"seeds_truncated": len(capped),
                                 "citing_works_not_pulled": dropped, "detail": capped},
        },
        "groups": diag,
        "most_seeded": [{"n_seeds": r["n_seeds"], "doi": r["doi"], "title": r["title"],
                         "year": r["year"], "cited_by": r["cited_by"]} for r in top],
    }, indent=1))
    print(f"\nwrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
