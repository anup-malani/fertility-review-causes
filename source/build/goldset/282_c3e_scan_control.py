#!/usr/bin/env python3
"""282 — C.3.e: positive control for the probe outcome scan. TICK-077.

281 returned ZERO fertility outcomes in all six retrieved probe full texts. A detector that
fires on nothing is indistinguishable from a broken detector, so before that null is reported
it is run against documents KNOWN to estimate a fertility outcome. If the control lights up
and the probes stay dark, the null is about the probes. If the control is dark too, the null
is about the scanner.

Controls are drawn from this chapter's own Arm B anchors -- papers whose titles announce a
fertility outcome -- and are retrieved and scanned through exactly the same code path.

Usage: python3 282_c3e_scan_control.py
"""
import json, importlib.util, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
GOLD = ROOT / "source" / "build" / "goldset"
LOGS = ROOT / "literature" / "search-logs"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    sys.modules[name] = m
    spec.loader.exec_module(m)
    return m


ret = load("m280", GOLD / "280_c3e_probe_retrieval.py")
scan = load("m281", GOLD / "281_c3e_probe_outcome_scan.py")

CONTROLS = ["pitt-1999-credit-programs", "cumming-2023-monetary-policy-birth-rates",
            "babies-of-mortgage-deregulation", "dettling-2014-house-prices-birth-rates",
            "pnas-2026-provident-fund"]

ret.TARGETS = CONTROLS
ret.OUT = LOGS / "credit-constraints-control-retrieval.json"
ret.main()

scan.RET = json.loads(ret.OUT.read_text())
scan.OUT = LOGS / "credit-constraints-control-outcome-scan.json"
scan.main()
