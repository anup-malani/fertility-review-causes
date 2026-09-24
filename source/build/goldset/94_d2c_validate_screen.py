#!/usr/bin/env python3
"""
94_d2c_validate_screen.py — D.2.c (son preference), screen validator.

Provides `validate_record(record, expected_id, location)` for the D.2.c blinded-screen output schema,
imported by the runner (95). Mirrors 94_a14 / the C.2.h validator (57) contract; the taxonomy is D.2.c's
(step 93 rubric v1). Fail-closed on structure and controlled vocabularies; the verdict<->cell pairing is a
rubric convention, not hard-enforced here, because pooling correctness lives in the assembler (96), which
pools only (verdict==RELEVANT AND cell in PRIMARY AND evidence not theory/review).
"""
import argparse, json, sys
from collections import Counter
from pathlib import Path

SLUG = "son-preference-cultural"
HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
LOGS = REPO / "literature" / "search-logs"

VERDICTS = {"RELEVANT", "UNCERTAIN", "NOT_RELEVANT"}
PRIMARY = {"PRIMARY_DIFFERENTIAL_STOPPING", "PRIMARY_SEXSEL_SUBSTITUTION", "PRIMARY_NORM_INTENSITY"}
MECHTHEORY = {"MECHANISM_PREFERENCE_ONLY", "THEORY"}
OFF = {"OFF_ADULT_SEX_RATIO", "OFF_ABORTION_GENERAL", "OFF_PARITY_STOPPING", "OFF_OLD_AGE_SECURITY",
       "OFF_GENDER_EQUITY", "OFF_CHILD_MORTALITY", "OFF_OUTCOME", "OFF_OTHER", "REVERSE"}
CELLS = PRIMARY | MECHTHEORY | OFF | {"INSUFFICIENT_INFO", "NA"}
SUBMECH = {"STOPPING", "SEXSEL_ABORTION", "NORM_INTENSITY", "MORTALITY_INTERACTION", "NA"}
IDENT = {"NATURAL_EXPERIMENT", "REVEALED_STOPPING", "ASSOCIATIONAL_ONLY", "UNCLEAR", "NA"}
REQUIRED = {"id", "verdict", "estimand_cell", "sub_mechanism", "outcome", "identification",
            "evidence_type", "reason"}


def validate_record(record, expected_id, location):
    errors = []
    if not isinstance(record, dict):
        return [f"{location}: verdict must be an object"]
    missing = sorted(REQUIRED - set(record))
    if missing:
        errors.append(f"{location}: missing fields {missing}")
    if record.get("id") != expected_id:
        errors.append(f"{location}: id/order mismatch: expected {expected_id!r}, got {record.get('id')!r}")
    verdict = str(record.get("verdict", "")).upper()
    cell = str(record.get("estimand_cell", "")).upper()
    sub = str(record.get("sub_mechanism", "")).upper()
    ident = str(record.get("identification", "")).upper()
    ev = str(record.get("evidence_type", "")).lower().strip()
    if verdict not in VERDICTS:
        errors.append(f"{location}: invalid verdict {verdict!r}")
    if cell not in CELLS:
        errors.append(f"{location}: invalid estimand_cell {cell!r}")
    if sub not in SUBMECH:
        errors.append(f"{location}: invalid sub_mechanism {sub!r}")
    if ident not in IDENT:
        errors.append(f"{location}: invalid identification {ident!r}")
    if not ev:
        errors.append(f"{location}: evidence_type must be a nonblank string")
    if cell == "INSUFFICIENT_INFO" and verdict != "UNCERTAIN":
        errors.append(f"{location}: INSUFFICIENT_INFO pairs only with UNCERTAIN")
    for field in ("outcome", "reason"):
        if not isinstance(record.get(field), str) or not record.get(field, "").strip():
            errors.append(f"{location}: {field} must be a nonblank string")
    return errors


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--audit", action="store_true")
    ap.parse_args()
    manifest = json.loads((LOGS / f"{SLUG}-screen-manifest.json").read_text())
    valid = missing = bad = 0
    cells = Counter()
    for m in manifest["manifest"]:
        out = REPO / m["output"]
        inp = json.loads((REPO / m["input"]).read_text())
        if not out.exists():
            missing += 1
            continue
        try:
            arr = json.loads(out.read_text())
        except json.JSONDecodeError:
            bad += 1
            continue
        errs = []
        if not isinstance(arr, list) or len(arr) != len(inp):
            errs.append(f"batch {m['batch']:03d}: count mismatch")
        else:
            for i, (rec, paper) in enumerate(zip(arr, inp), 1):
                errs += validate_record(rec, paper["id"], f"batch {m['batch']:03d} row {i}")
                if isinstance(rec, dict) and str(rec.get("verdict", "")).upper() != "NOT_RELEVANT":
                    cells[str(rec.get("estimand_cell", "")).upper()] += 1
        if errs:
            bad += 1
            for e in errs[:5]:
                print(f"ERROR: {e}", file=sys.stderr)
        else:
            valid += 1
    print(f"valid batches {valid}, missing {missing}, bad {bad}")
    if cells:
        print("non-NOT_RELEVANT cell tally:", dict(cells.most_common()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
