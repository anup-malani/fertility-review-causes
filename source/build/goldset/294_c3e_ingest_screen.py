#!/usr/bin/env python3
"""294 — C.3.e: ingest the 349-record screen, validate it, emit the routed table. TICK-077.

Validation is the point of this script, not the tabulation. Three checks, each of which has
caught a real defect on an earlier chapter:

  1. EVERY VERDICT ID MUST EXIST IN THE SHEET. A verdict for a record that was never on the
     sheet is a typo or a copied id from another stratum, and it would silently add a study to
     the evidence base that nobody screened.
  2. EVERY SHEET RECORD MUST BE ACCOUNTED FOR. Records not explicitly routed are recorded as
     `OFF_OTHER_read_not_routed` -- an explicit residual, not an absence. The screen's own
     denominator has to be visible or the yield cannot be reported honestly.
  3. NO ID IN TWO CELLS. A record routed twice is a contradiction, not a judgement call.

Emits `extraction/credit-constraints-screen.csv` -- the routed table the next stage consumes.

Usage: python3 294_c3e_ingest_screen.py
"""
import csv, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
LOGS = ROOT / "literature" / "search-logs"
SHEET = json.loads((LOGS / "credit-constraints-screen-sheet.json").read_text())
V = json.loads((ROOT / "temp" / "c3e_verdicts.json").read_text())
OUTCSV = ROOT / "extraction" / "credit-constraints-screen.csv"
OUTJSON = LOGS / "credit-constraints-screen-results.json"

by_id, stratum_of = {}, {}
for strat, rows in SHEET.items():
    for r in rows:
        by_id[r["openalex"]] = r
        stratum_of[r["openalex"]] = strat

errors = []
seen = {}
for cell, items in V.items():
    for oid, note in items.items():
        if oid not in by_id:
            errors.append(f"VERDICT FOR A RECORD NOT ON THE SHEET: {oid} ({cell})")
        if oid in seen:
            errors.append(f"ROUTED TWICE: {oid} -> {seen[oid]} and {cell}")
        seen[oid] = cell

if errors:
    print("VALIDATION ERRORS")
    for e in errors:
        print("  " + e)

rows = []
for oid, r in by_id.items():
    cell = seen.get(oid, "OFF_OTHER_read_not_routed")
    note = V.get(cell, {}).get(oid, "") if cell in V else "read at title/abstract; no C.3.e estimand"
    arm = {"PRIMARY_SAVE_INSURE": "S", "PRIMARY_BORROW_TERMS": "B",
           "PRIMARY_COMPOSITE_ACCESS": "composite"}.get(cell, "")
    rows.append({"openalex": oid, "doi": r.get("doi") or "", "year": r.get("year") or "",
                 "title": r.get("title") or "", "venue": r.get("venue") or "",
                 "stratum": stratum_of[oid], "cell": cell, "arm": arm,
                 "screened_by": "Shravan/Claude", "screened_on": "2026-09-01", "note": note})
rows.sort(key=lambda x: (x["cell"], -(x["year"] or 0)))

OUTCSV.parent.mkdir(parents=True, exist_ok=True)
with OUTCSV.open("w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    w.writeheader()
    w.writerows(rows)

from collections import Counter
cells = Counter(r["cell"] for r in rows)
by_strat = {}
for r in rows:
    d = by_strat.setdefault(r["stratum"], {"n": 0, "routed": 0})
    d["n"] += 1
    if r["cell"] != "OFF_OTHER_read_not_routed":
        d["routed"] += 1
primary = sum(v for k, v in cells.items() if k.startswith("PRIMARY_"))

summary = {"screened": len(rows), "validation_errors": errors,
           "cells": dict(cells.most_common()),
           "primary_pool_total": primary,
           "yield_by_stratum": {k: {**v, "routed_share": round(v["routed"] / v["n"], 3)}
                                for k, v in by_strat.items()},
           "probe_predicted": {"both_channels": "~23%", "snowball_r2_only": "~4%"}}
OUTJSON.write_text(json.dumps({"summary": summary, "rows": rows}, indent=1))
print(json.dumps(summary, indent=1))
print(f"\nwrote {OUTCSV.relative_to(ROOT)}")
