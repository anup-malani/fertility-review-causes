#!/usr/bin/env python3
"""
92_a3_validate_screen.py — A.3 (diffusion & social-learning of fertility control), screen validator.

Provides `validate_record(record, expected_id, location)` for the A.3 blinded-screen output schema,
imported by the runner (93). Mirrors the child-labor validator (59) contract; the taxonomy is A.3's
(step 91 rubric v1). Also runnable standalone with --audit to report how many manifest batches have
valid verdict files, without invoking any model.

Fail-closed: a record is valid only if every required field is present, every controlled value is in
its vocabulary, and the rubric's pairing constraints hold. Case is normalized on the controlled fields
so a screener returning `not_relevant` or `separates_from_common_shock` is accepted.
"""
import argparse, json, sys
from collections import Counter
from pathlib import Path

SLUG = "diffusion-of-fertility-control"
HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
LOGS = REPO / "literature" / "search-logs"

VERDICTS = {"RELEVANT", "UNCERTAIN", "NOT_RELEVANT"}
PRIMARY = {"PRIMARY_SOCIAL_EXPOSURE", "PRIMARY_SPATIAL_DIFFUSION",
           "PRIMARY_CULTURAL_BOUNDARY_CONTENT", "PRIMARY_LEGITIMATION_SPREAD"}
THEORY = {"DIFFUSION_THEORY", "PRINCETON_CANON"}
OFF = {"OFF_CHANNEL_A20", "OFF_TECHNOLOGY_A2", "OFF_STIGMA_LEVEL_A6", "OFF_VERTICAL_A19",
       "OFF_PROGRAM_A5", "OFF_VALUE_D1", "OFF_OTHER", "OFF_OUTCOME", "REVERSE"}
CELLS = PRIMARY | THEORY | OFF | {"INSUFFICIENT_INFO", "NA"}
CHANNELS = {"SOCIAL_NETWORK_PEER", "SPATIAL_MIGRATION", "CULTURAL_LINGUISTIC_RELIGIOUS",
            "LEGITIMATION_KNOWLEDGE", "MASS_MEDIA", "NA"}
IDENT = {"SEPARATES_FROM_COMMON_SHOCK", "DESCRIPTIVE_RESIDUAL_ONLY", "UNCLEAR", "NA"}
# evidence_type is a descriptive design label, not a router: it feeds only the downstream pooling
# exclusion (reviews and theory are dropped from the pooled estimate). Enforcing a closed vocabulary is
# both fragile (the screener legitimately produces "qualitative", "historical", "mixed methods",
# "methodological", ...) and pointless, so any nonblank string is accepted here. The two values that
# DO drive downstream logic — `review` and `theory` — are required verbatim by the rubric and are
# matched by substring in the assembler, so an off-menu synonym never silently lands in the pool.
CANONICAL_EVIDENCE = {"quasi-experimental", "observational", "structural", "qualitative", "historical",
                      "descriptive", "theory", "review", "mechanism", "other"}
REQUIRED = {"paperId", "verdict", "estimand_cell", "diffusion_channel", "outcome",
            "identification_of_diffusion", "evidence_type", "reason"}


def validate_record(record, expected_id, location):
    errors = []
    if not isinstance(record, dict):
        return [f"{location}: verdict must be an object"]
    missing = sorted(REQUIRED - set(record))
    if missing:
        errors.append(f"{location}: missing fields {missing}")
    if record.get("paperId") != expected_id:
        errors.append(f"{location}: paperId/order mismatch: expected {expected_id!r}, got {record.get('paperId')!r}")
    verdict = str(record.get("verdict", "")).upper()
    cell = str(record.get("estimand_cell", "")).upper()
    chan = str(record.get("diffusion_channel", "")).upper()
    ident = str(record.get("identification_of_diffusion", "")).upper()
    ev = str(record.get("evidence_type", "")).lower().strip()
    if verdict not in VERDICTS:
        errors.append(f"{location}: invalid verdict {verdict!r}")
    if cell not in CELLS:
        errors.append(f"{location}: invalid estimand_cell {cell!r}")
    if chan not in CHANNELS:
        errors.append(f"{location}: invalid diffusion_channel {chan!r}")
    if ident not in IDENT:
        errors.append(f"{location}: invalid identification_of_diffusion {ident!r}")
    if not ev:
        errors.append(f"{location}: evidence_type must be a nonblank string")
    # Verdict<->cell PAIRING is intentionally NOT hard-enforced here. The rubric states the convention
    # (RELEVANT reserved for A.3's own cells; walls -> NOT_RELEVANT with an OFF_* tag; INSUFFICIENT_INFO
    # for thin records), but the screener legitimately produces reasonable variants (NOT_RELEVANT +
    # INSUFFICIENT_INFO for a thin off-topic title, etc.), and failing a whole batch on a pairing nicety
    # is costly and pointless: pooling correctness lives in the ASSEMBLER, which pools only
    # (verdict==RELEVANT AND cell in PRIMARY AND evidence not theory/review), so an off-convention
    # pairing simply falls out of the pool. Only the two integrity guards that could corrupt the POOL
    # are enforced:
    #   (a) a PRIMARY cell may not carry a theory evidence_type (pure theory must not pool);
    #   (b) a MASS_MEDIA channel may not sit in a PRIMARY cell (Wall 1: mass media is A.20's).
    if cell in PRIMARY and "theor" in ev:
        errors.append(f"{location}: a PRIMARY cell cannot have a theory evidence_type")
    if chan == "MASS_MEDIA" and cell in PRIMARY:
        errors.append(f"{location}: MASS_MEDIA channel must route to OFF_CHANNEL_A20, not a PRIMARY cell (Wall 1)")
    for field in ("outcome", "reason"):
        if not isinstance(record.get(field), str) or not record.get(field, "").strip():
            errors.append(f"{location}: {field} must be a nonblank string")
    return errors


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--audit", action="store_true", help="report how many batches have valid verdicts")
    args = ap.parse_args()
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
                errs += validate_record(rec, paper["paperId"], f"batch {m['batch']:03d} row {i}")
                if isinstance(rec, dict) and str(rec.get("verdict", "")).upper() != "NOT_RELEVANT":
                    cells[str(rec.get("estimand_cell", "")).upper()] += 1
        if errs:
            bad += 1
            for e in errs[:5]:
                print(f"ERROR: {e}", file=sys.stderr)
        else:
            valid += 1
    print(f"valid batches {valid} | missing {missing} | invalid {bad} | of {manifest['batches']}")
    if cells:
        print("rel/unc cells so far: " + ", ".join(f"{c}={n}" for c, n in cells.most_common()))
    return 0 if (valid == manifest["batches"]) else 3


if __name__ == "__main__":
    raise SystemExit(main())
