#!/usr/bin/env python3
"""312 — C.6.a: ingest screen verdicts, validate, report yield and blind sensitivity. TICK-078.

Validation is the point of this script, not the tabulation. Four checks, each of which has caught a
real defect on an earlier chapter:

  1. EVERY VERDICT ID MUST EXIST IN A SHEET. A verdict for a record never on a sheet is a typo or an
     id copied from another stratum, and it would add a study nobody screened to the evidence base.
  2. NO ID IN TWO CELLS. A record routed twice is a contradiction, not a judgement call.
  3. EVERY SCREENED STRATUM MUST BE FULLY ACCOUNTED FOR. A stratum is either fully routed or listed
     as unscreened; a partially routed stratum reported as complete makes the denominator a fiction.
  4. SENSITIVITY IS MEASURED ON HIDDEN GOLD. The anchors are in the sheets unmarked; this script is
     the first place they are identified. A screen graded on records it knew were gold measures
     nothing (`a-positives-only-screen-cannot-measure-sensitivity`).

Usage: python3 source/build/goldset/312_c6a_ingest_screen.py
"""
import csv
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
LOGS = ROOT / "literature" / "search-logs"
SHEET = json.loads((LOGS / "easterlin-relative-income-screen-sheet.json").read_text())
V = json.loads((ROOT / "temp" / "c6a_verdicts.json").read_text())
ANCH = json.loads((LOGS / "easterlin-relative-income-cold-start-anchors.json").read_text())
OUTCSV = ROOT / "extraction" / "easterlin-relative-income-screen.csv"
OUTJSON = LOGS / "easterlin-relative-income-screen-results.json"

PRIMARY = {"RELATIVE_INCOME_FERTILITY", "COHORT_SIZE_FERTILITY", "BENCHMARK_MEASURED",
           "CYCLE_TEST", "RIVAL_TEST", "INSTITUTIONAL_MODERATION"}
# BOOM_ALTERNATIVE was added to the rubric DURING the screen, at the free_seed stratum, when it
# became clear that a large class of records -- competing explanations of the baby boom itself
# (WWII female labour supply, household technology, war debt, mortgages, influenza) -- had no cell.
# They are not evidence about Easterlin's mechanism, but they are evidence about how much of the
# mechanism's own best case is already spoken for, which is a scope §5 demsig input. Forcing them to
# OFF_OTHER would have discarded exactly the records the demographic-significance step needs.
# The four strata screened before it existed are re-checked in 313.
KEPT = PRIMARY | {"LINK1_LABOUR", "MIXED_COHORT_MARRIAGE", "THEORY", "BOOM_ALTERNATIVE"}

by_id, stratum_of = {}, {}
for strat, rows in SHEET.items():
    for r in rows:
        by_id[r["openalex"]] = r
        stratum_of[r["openalex"]] = strat

gold = {}
for a in ANCH:
    oid = (a.get("top_candidate") or {}).get("oa_id")
    if oid:
        gold[oid.rsplit("/", 1)[-1]] = a

errors, seen = [], {}
for cell, items in V.items():
    for oid, note in items.items():
        if oid not in by_id:
            errors.append(f"VERDICT FOR A RECORD NOT ON ANY SHEET: {oid} ({cell})")
        if oid in seen:
            errors.append(f"ROUTED TWICE: {oid} -> {seen[oid]} and {cell}")
        seen[oid] = cell

# Which strata were screened, and were they screened completely?
strat_total = Counter(stratum_of.values())
strat_done = Counter(stratum_of[o] for o in seen if o in stratum_of)
complete, partial, unscreened = [], [], []
for s, n in strat_total.items():
    d = strat_done.get(s, 0)
    (complete if d == n else partial if d else unscreened).append((s, d, n))
for s, d, n in partial:
    errors.append(f"STRATUM PARTIALLY SCREENED: {s} {d}/{n} — either finish it or record it as a "
                  f"sample with its own denominator")

print("VALIDATION")
if errors:
    for e in errors:
        print("  ✗ " + e)
else:
    print("  ✓ every verdict id is on a sheet; no id routed twice; "
          "every started stratum finished")

screened_n = len(seen)
print(f"\nSCREENED {screened_n} of {sum(strat_total.values())} "
      f"({100*screened_n/sum(strat_total.values()):.0f}%)")
for s, d, n in sorted(complete):
    print(f"  complete   {s:28} {n}")
for s, d, n in sorted(unscreened):
    print(f"  UNSCREENED {s:28} {n}")

cells = Counter(seen.values())
print("\nCELLS")
for c, n in cells.most_common():
    mark = "*" if c in PRIMARY else (" " if c in KEPT else "-")
    print(f" {mark} {c:28} {n}")
kept = sum(n for c, n in cells.items() if c in KEPT)
prim = sum(n for c, n in cells.items() if c in PRIMARY)
print(f"\nyield: {prim}/{screened_n} primary ({100*prim/screened_n:.1f}%), "
      f"{kept}/{screened_n} kept in some cell ({100*kept/screened_n:.1f}%)")

# Blind sensitivity, on the anchors that fell in a screened stratum.
seen_gold = {g: seen[g] for g in gold if g in seen}
gold_kept = {g: c for g, c in seen_gold.items() if c in KEPT}
print(f"\nBLIND SENSITIVITY: {len(seen_gold)} anchors were in the screened strata, unmarked. "
      f"{len(gold_kept)} kept ({100*len(gold_kept)/len(seen_gold):.0f}%)" if seen_gold else "")
for g, c in sorted(seen_gold.items(), key=lambda kv: kv[1]):
    flag = "" if c in KEPT else "   <-- ROUTED OUT, read this back"
    print(f"    {c:28} {gold[g]['key']}{flag}")

OUTCSV.parent.mkdir(parents=True, exist_ok=True)
with OUTCSV.open("w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["openalex", "cell", "stratum", "year", "title", "venue", "cited_by",
                "is_anchor", "note"])
    for oid, cell in sorted(seen.items(), key=lambda kv: kv[1]):
        r = by_id.get(oid, {})
        w.writerow([oid, cell, stratum_of.get(oid, ""), r.get("year"), r.get("title"),
                    r.get("venue"), r.get("cited_by"), "yes" if oid in gold else "",
                    V[cell][oid]])

OUTJSON.write_text(json.dumps({
    "screened": screened_n, "universe": sum(strat_total.values()), "errors": errors,
    "complete_strata": [s for s, _, _ in complete],
    "unscreened_strata": {s: n for s, _, n in unscreened},
    "cells": dict(cells), "primary": prim, "kept": kept,
    "blind_sensitivity": {"anchors_in_screened_strata": len(seen_gold),
                          "kept": len(gold_kept),
                          "routed_out": {gold[g]["key"]: c for g, c in seen_gold.items()
                                         if c not in KEPT}}}, indent=1) + "\n")
print(f"\nwritten: {OUTCSV.relative_to(ROOT)} and {OUTJSON.name}")
