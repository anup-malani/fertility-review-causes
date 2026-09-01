#!/usr/bin/env python3
"""286 — C.3.e: outcome scan over the eight hand-retrieved full texts. TICK-077.

Runs the SAME scanner as 281 (bibliography cut, context emitted not counted, table and
outcome-list contexts flagged separately) over the PDFs installed by 284. The scanner was
already validated on positive controls in 282, so a zero here is a property of the document.

Two questions, and they are different:
  - the four remaining PROBES: does a fertility or birth variable appear on the left-hand side
    of any estimate? This closes the "6 of 10" bound.
  - the four BOUNDARY-SPANNING candidates: they plainly do estimate fertility. The question for
    them is narrower and is asked in 287.

Usage: python3 286_c3e_handoff_scan.py
"""
import importlib.util, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
LOGS = ROOT / "literature" / "search-logs"
GOLD = ROOT / "source" / "build" / "goldset"

spec = importlib.util.spec_from_file_location("m281", GOLD / "281_c3e_probe_outcome_scan.py")
m = importlib.util.module_from_spec(spec)
sys.modules["m281"] = m
spec.loader.exec_module(m)

inst = json.loads((LOGS / "credit-constraints-handoff-install.json").read_text())
m.RET = {"records": [{"key": i["key"], "fetched_path": i["installed"]}
                     for i in inst["installed"] if i["installed"]]}
m.OUT = LOGS / "credit-constraints-handoff-outcome-scan.json"
m.main()
