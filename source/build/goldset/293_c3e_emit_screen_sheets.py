#!/usr/bin/env python3
"""293 — C.3.e: emit screening sheets for the two dense strata. TICK-077.

The depth probe (292) put `both_channels` at ~23% yield and `snowball_r2_only` at ~4%, against
~6% for `frame_only` and ~1% for `snowball_r1_only`. These two strata are 349 records for an
estimated ~28 of the relevant set, so they are screened first and in full.

Emits a stable, ordered sheet keyed by openalex id so the verdicts file can be checked back
against it record by record -- an unmatched or missing id is a defect, not a judgement call.

Usage: python3 293_c3e_emit_screen_sheets.py [--stratum NAME] [--chars N]
"""
import json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
LOGS = ROOT / "literature" / "search-logs"
OUT = LOGS / "credit-constraints-screen-sheet.json"

args = sys.argv
CHARS = int(args[args.index("--chars") + 1]) if "--chars" in args else 200
ONLY = args[args.index("--stratum") + 1] if "--stratum" in args else None

U = json.loads((LOGS / "credit-constraints-screen-universe.json").read_text())
PS = json.loads((LOGS / "credit-constraints-prescreen.json").read_text())
accepted = set(PS["accepted_rules"])

import re
AGRO = re.compile(r"soil fertilit|fertiliz|fertilis|crop yield|agronom|nitrogen|"
                  r"livestock|cattle|poultry|maize|wheat yield", re.I)
VET = re.compile(r"\b(cow|sow|bovine|porcine|dairy herd|broiler)\b", re.I)
NON_STUDY = {"dataset", "peer-review", "paratext", "editorial", "erratum", "letter", "retraction"}


def text(r):
    return ((r.get("title") or "") + " . " + (r.get("abstract") or "")).lower()


def survives(r):
    if AGRO.search(text(r)) or VET.search(text(r)):
        return False
    return (r.get("type") or "").lower() not in NON_STUDY


def stratum(r):
    p = set(r["provenance"])
    if any(x.startswith("hand_") for x in p):
        return "hand_sourced"
    disc = {x for x in p if not x.startswith("hand_")}
    if "frame" in disc and len(disc) > 1:
        return "both_channels"
    if "frame" in disc:
        return "frame_only"
    if "snowball_r2" in disc:
        return "snowball_r2_only"
    return "snowball_r1_only"


sheets = {}
for r in U["records"]:
    if not survives(r):
        continue
    s = stratum(r)
    if s not in ("both_channels", "snowball_r2_only"):
        continue
    sheets.setdefault(s, []).append(r)

for k in sheets:
    sheets[k].sort(key=lambda r: (r.get("year") or 0, r["openalex"]))

OUT.write_text(json.dumps({k: [{"openalex": r["openalex"], "title": r.get("title"),
                                "year": r.get("year"), "venue": r.get("venue"),
                                "doi": r.get("doi"),
                                "abstract": (r.get("abstract") or "")}
                               for r in v] for k, v in sheets.items()}, indent=1))
for k, v in sheets.items():
    print(f"{k}: {len(v)} records")
    if ONLY and k != ONLY:
        continue
    for i, r in enumerate(v, 1):
        ab = " ".join((r.get("abstract") or "").split())[:CHARS]
        print(f"{i:3d}|{r['openalex']}|[{r.get('year')}] {(r.get('title') or '')[:88]}")
        print(f"    {(r.get('venue') or 'n/a')[:46]} :: {ab}")
