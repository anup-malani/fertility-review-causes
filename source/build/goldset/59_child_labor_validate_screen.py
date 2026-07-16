#!/usr/bin/env python3
"""Validate and assemble the blinded TICK-031 title/abstract screen.

Default behavior is fail-closed: all manifest batches and all 1,255 verdicts must be
present and valid before deliverables are written. ``--audit`` reports progress and
errors without writing screened outputs; ``--allow-incomplete`` writes a clearly marked
partial diagnostic only and must never be used as the frozen Tier-B gold.
"""

import argparse
import csv
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

SLUG = "child-labor-laws-and-schooling"
HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
LOGS = REPO / "literature" / "search-logs"
OUTPUT = REPO / "output"

VERDICTS = {"RELEVANT", "UNCERTAIN", "NOT_RELEVANT"}
CELLS = {
    "PRIMARY_CL_QUANTUM", "PRIMARY_CS_QUANTUM", "PRIMARY_JOINT_QUANTUM", "TEMPO",
    "THEORY", "OFF_OUTCOME", "OFF_EXPOSURE", "MODE_PRODUCTION", "REVERSE", "NA",
}
DIRECTIONS = {"forward", "reverse", "n/a"}
EVIDENCE = {"quasi-experimental", "observational", "structural", "theory", "review", "mechanism", "other"}
REQUIRED = {"paperId", "verdict", "estimand_cell", "treatment", "outcome", "direction", "evidence_type", "reason"}
PRIMARY = {"PRIMARY_CL_QUANTUM", "PRIMARY_CS_QUANTUM", "PRIMARY_JOINT_QUANTUM"}


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate_record(record, expected_id, location):
    errors = []
    if not isinstance(record, dict):
        return [f"{location}: verdict must be an object"]
    missing = sorted(REQUIRED - set(record))
    if missing:
        errors.append(f"{location}: missing fields {missing}")
    pid = record.get("paperId")
    if pid != expected_id:
        errors.append(f"{location}: paperId/order mismatch: expected {expected_id!r}, got {pid!r}")
    verdict = str(record.get("verdict", "")).upper()
    cell = str(record.get("estimand_cell", "")).upper()
    if verdict not in VERDICTS:
        errors.append(f"{location}: invalid verdict {verdict!r}")
    if cell not in CELLS:
        errors.append(f"{location}: invalid estimand_cell {cell!r}")
    if record.get("direction") not in DIRECTIONS:
        errors.append(f"{location}: invalid direction {record.get('direction')!r}")
    if record.get("evidence_type") not in EVIDENCE:
        errors.append(f"{location}: invalid evidence_type {record.get('evidence_type')!r}")
    if verdict == "NOT_RELEVANT" and cell != "NA":
        errors.append(f"{location}: NOT_RELEVANT must use cell NA")
    if verdict != "NOT_RELEVANT" and cell == "NA":
        errors.append(f"{location}: RELEVANT/UNCERTAIN cannot use cell NA")
    if cell in PRIMARY | {"TEMPO"} and record.get("direction") != "forward":
        errors.append(f"{location}: PRIMARY/TEMPO must have forward direction")
    if cell == "REVERSE" and record.get("direction") != "reverse":
        errors.append(f"{location}: REVERSE must have reverse direction")
    if cell == "THEORY" and record.get("evidence_type") not in {"theory", "structural"}:
        errors.append(f"{location}: THEORY requires theory or structural evidence_type")
    if cell in PRIMARY and record.get("evidence_type") in {"theory", "review", "mechanism"}:
        errors.append(f"{location}: PRIMARY must be an empirical effect estimate")
    for field in ("treatment", "outcome", "reason"):
        if not isinstance(record.get(field), str) or not record.get(field, "").strip():
            errors.append(f"{location}: {field} must be a nonblank string")
    return errors


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--audit", action="store_true", help="report status/errors; never write deliverables")
    parser.add_argument("--allow-incomplete", action="store_true", help="write partial diagnostic, visibly marked")
    args = parser.parse_args()

    manifest_path = LOGS / f"{SLUG}-screen-manifest.json"
    manifest = json.loads(manifest_path.read_text())
    source_path = REPO / manifest["source"]
    errors, warnings, verdicts, missing_batches = [], [], {}, []

    if sha256(source_path) != manifest["source_sha256"]:
        errors.append("citation-frame checksum differs from the screen manifest")
    source = json.loads(source_path.read_text())
    source_by_id = {row["paperId"]: row for row in source}
    if len(source_by_id) != manifest["records"]:
        errors.append("citation-frame count/uniqueness differs from manifest")

    for item in manifest["manifest"]:
        input_path = REPO / item["input"]
        output_path = REPO / item["output"]
        label = f"batch {item['batch']:03d}"
        if not input_path.exists():
            errors.append(f"{label}: input batch missing; rerun step 58")
            continue
        if sha256(input_path) != item["input_sha256"]:
            errors.append(f"{label}: input checksum changed after blinding")
        inputs = json.loads(input_path.read_text())
        if len(inputs) != item["n"]:
            errors.append(f"{label}: input count differs from manifest")
        if not output_path.exists():
            missing_batches.append(item["batch"])
            continue
        try:
            output = json.loads(output_path.read_text())
        except json.JSONDecodeError as exc:
            errors.append(f"{label}: invalid JSON: {exc}")
            continue
        if not isinstance(output, list) or len(output) != len(inputs):
            errors.append(f"{label}: expected {len(inputs)} ordered verdicts, found "
                          f"{len(output) if isinstance(output, list) else 'non-list'}")
            continue
        for index, (paper, verdict) in enumerate(zip(inputs, output), start=1):
            pid = paper["paperId"]
            errors.extend(validate_record(verdict, pid, f"{label} row {index}"))
            if pid in verdicts:
                errors.append(f"{label} row {index}: duplicate verdict for {pid}")
            else:
                normalized = dict(verdict) if isinstance(verdict, dict) else {}
                normalized["verdict"] = str(normalized.get("verdict", "")).upper()
                normalized["estimand_cell"] = str(normalized.get("estimand_cell", "")).upper()
                verdicts[pid] = normalized

    unknown = sorted(set(verdicts) - set(source_by_id))
    unscored = sorted(set(source_by_id) - set(verdicts))
    if unknown:
        errors.append(f"{len(unknown)} verdict IDs are absent from the citation frame")
    if missing_batches:
        warnings.append(f"{len(missing_batches)} missing verdict batches")
    if unscored:
        warnings.append(f"{len(unscored)} records have no verdict")

    complete = not errors and not missing_batches and not unscored and len(verdicts) == manifest["records"]
    counts = Counter(v.get("verdict") for v in verdicts.values())
    cells = Counter(v.get("estimand_cell") for v in verdicts.values() if v.get("verdict") != "NOT_RELEVANT")
    print(f"validated verdicts: {len(verdicts)}/{manifest['records']} | "
          f"batches: {manifest['batches'] - len(missing_batches)}/{manifest['batches']} | complete={complete}")
    if counts:
        print("verdicts: " + ", ".join(f"{key}={value}" for key, value in sorted(counts.items())))
    for warning in warnings:
        print(f"WARNING: {warning}", file=sys.stderr)
    for error in errors[:50]:
        print(f"ERROR: {error}", file=sys.stderr)
    if len(errors) > 50:
        print(f"ERROR: ... {len(errors) - 50} additional errors", file=sys.stderr)

    if args.audit:
        return 0 if complete else 3
    if not complete and not args.allow_incomplete:
        print("Refusing to write screened outputs: use --audit for progress or complete/fix verdicts.", file=sys.stderr)
        return 2

    rows = []
    for paper in source:
        verdict = verdicts.get(paper["paperId"])
        if verdict is None:
            continue
        rows.append({**paper, "screen": verdict})
    suffix = "screened" if complete else "screened-PARTIAL-NOT-FOR-GOLD"
    json_path = LOGS / f"{SLUG}-{suffix}.json"
    json_path.write_text(json.dumps(rows, indent=2, ensure_ascii=False))

    review_path = OUTPUT / f"{SLUG}-screen-review.csv"
    review_path.parent.mkdir(parents=True, exist_ok=True)
    with review_path.open("w", newline="") as handle:
        fields = ["paperId", "doi", "title", "year", "verdict", "estimand_cell", "evidence_type",
                  "treatment", "outcome", "direction", "reason", "ra_decision", "ra_note"]
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            screen = row["screen"]
            writer.writerow({key: row.get(key, screen.get(key, "")) for key in fields})

    report = [
        f"# Citation-frame screen — {SLUG}", "",
        f"- status: **{'COMPLETE' if complete else 'PARTIAL — NOT FOR GOLD/RECALL'}**",
        f"- validated records: {len(rows):,} / {manifest['records']:,}",
        f"- validated batches: {manifest['batches'] - len(missing_batches)} / {manifest['batches']}",
        f"- schema/consistency errors: {len(errors)}", "",
        "## Verdicts", "",
    ]
    report += [f"- {key}: {value}" for key, value in sorted(counts.items())]
    report += ["", "## Relevant/uncertain estimand cells", ""]
    report += [f"- {key}: {value}" for key, value in cells.most_common()]
    report += ["", "## Human gate", "",
               "The CSV review sheet is exception-based: leave `ra_decision` blank to approve; use "
               "`FIX`, `EXCLUDE`, or `UNSURE_PI` for rows needing action. A complete automated screen "
               "is still not a frozen gold set until RA adjudication/sign-off."]
    (LOGS / f"{SLUG}-screen-report.md").write_text("\n".join(report) + "\n")
    print(f"wrote {json_path.relative_to(REPO)}, {review_path.relative_to(REPO)}, and screen report")
    return 0 if complete else 4


if __name__ == "__main__":
    raise SystemExit(main())
