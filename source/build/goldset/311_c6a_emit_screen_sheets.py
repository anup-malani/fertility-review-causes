#!/usr/bin/env python3
"""311 — C.6.a: emit stratified screening sheets. TICK-078.

Stable, ordered, keyed by OpenAlex id so the verdicts file can be checked back record by record --
an unmatched or missing id is a defect, not a judgement call (the 294 validation on C.3.e).

Anchors are NOT marked. They are hidden controls, and a sheet that flags them measures a screen that
already knows the answer.

Usage: python3 source/build/goldset/311_c6a_emit_screen_sheets.py [--chars N]
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
LOGS = ROOT / "literature" / "search-logs"
CHARS = int(sys.argv[sys.argv.index("--chars") + 1]) if "--chars" in sys.argv else 220

U = json.loads((LOGS / "easterlin-relative-income-screen-universe.json").read_text())
PS = json.loads((LOGS / "easterlin-relative-income-prescreen.json").read_text())
surv = set(PS["survivor_ids"])


def stratum(r):
    p = [x for x in r["provenance"] if x != "anchor"]
    arms = [x.split(":")[1] for x in p if x.startswith("arm:")]
    if len(arms) >= 2:
        return "multi_arm"
    if len(arms) == 1:
        return f"arm_only_{arms[0]}"
    return "free_seed_only" if "free_seed" in p else "anchor_only"


sheets = {}
for r in U["records"]:
    if r["openalex"] not in surv:
        continue
    s = stratum(r)
    sheets.setdefault(s, []).append({
        "openalex": r["openalex"], "year": r["year"], "title": r["title"],
        "venue": r["venue"], "cited_by": r["cited_by"],
        "abstract": (r["abstract"] or "")[:CHARS]})

for s in sheets:
    sheets[s].sort(key=lambda x: (-(x["cited_by"] or 0), x["openalex"]))

out = LOGS / "easterlin-relative-income-screen-sheet.json"
out.write_text(json.dumps(sheets, indent=1) + "\n")
for s, rows in sorted(sheets.items(), key=lambda kv: -len(kv[1])):
    print(f"  {s:28} {len(rows)}")
print(f"total {sum(len(v) for v in sheets.values())} -> {out.name}")
