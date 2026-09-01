#!/usr/bin/env python3
"""301 — C.3.e: poolability. TICK-077.

PROTOCOL §5 stage 9 asks for meta-analysis if there are >=3 extractable effects and a narrative
synthesis otherwise. The rule this chapter applies, from its own scope memo:

  APPLY THE >=3 TEST AFTER STRATIFICATION, NEVER BEFORE.

The strata are forced by Ruling 1 and by what the extraction has since shown:
  * ARM — S / B / composite. Arms are never pooled with each other: disjoint settings, disjoint
    literatures, opposite predicted signs.
  * OUTCOME_LEVEL — realized / desired / intention. On this chapter the same exposure has produced
    OPPOSITE SIGNS at different levels inside a single randomised experiment, so pooling across
    levels would average a null against a positive and report a number describing neither.
  * ESTIMATOR compatibility — an identified quasi-experiment and an aggregate GMM panel are not the
    same estimand. A hazard ratio beside a mean is not a pool.

It also reports what a naive pool would have looked like, because the gap between the two is the
argument for stratifying.

Usage: python3 301_c3e_poolability.py
"""
import csv, json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
rows = list(csv.DictReader((ROOT / "extraction" / "credit-constraints-effects.csv").open()))
OUT = ROOT / "literature" / "search-logs" / "credit-constraints-poolability.json"

strata = defaultdict(list)
for r in rows:
    strata[(r["arm"], r["OUTCOME_LEVEL"], "identified" if r["identified"] == "YES" else "unidentified")].append(r)

print(f"{len(rows)} effect rows from {len({r['openalex'] for r in rows})} studies\n")
print(f"{'ARM':10s} {'OUTCOME':10s} {'ID':13s} {'effects':>7s} {'studies':>7s}  poolable?")
report = []
for k in sorted(strata):
    v = strata[k]
    n_st = len({r["openalex"] for r in v})
    # the >=3 test counts STUDIES, not effect rows: two rows from one paper are one study
    poolable = n_st >= 3
    est = {r["estimator_class"] for r in v}
    homog = len(est) == 1
    verdict = ("POOL" if poolable and homog else
               f"no — {n_st} studies" if not poolable else
               f"no — {len(est)} estimator classes: {', '.join(sorted(est))}")
    print(f"{k[0] or '-':10s} {k[1]:10s} {k[2]:13s} {len(v):7d} {n_st:7d}  {verdict}")
    report.append({"arm": k[0], "outcome_level": k[1], "identified": k[2],
                   "effects": len(v), "studies": n_st, "estimator_classes": sorted(est),
                   "poolable": bool(poolable and homog), "verdict": verdict})

naive_studies = len({r["openalex"] for r in rows})
print(f"\nNAIVE POOL (no stratification): {len(rows)} effects, {naive_studies} studies "
      f"-> would 'qualify' for meta-analysis")
print("STRATIFIED: not one stratum qualifies." if not any(x["poolable"] for x in report)
      else "STRATIFIED: some strata qualify.")
OUT.write_text(json.dumps({"strata": report, "naive_studies": naive_studies,
                           "any_poolable": any(x["poolable"] for x in report)}, indent=1))
print(f"\nwritten: {OUT.name}")
