#!/usr/bin/env python3
"""Run the TICK-031 blinded screening batches through an explicitly chosen model command.

The runner is resumable and fail-closed. It never uses a shell, never overwrites a valid
existing verdict unless --force is supplied, validates every response before an atomic
rename, and records a non-secret execution log. Model execution is deliberately explicit:
pass a command after ``--command`` only after the operator has authorized that runner.

Examples (operator chooses one; do not run both on the same screen):
  python3 60_run_child_labor_screen.py --command claude -p
  python3 60_run_child_labor_screen.py --batches 1-3 --command claude -p

Use ``--audit`` to inspect readiness without invoking a model.
"""

import argparse
import importlib.util
import json
import os
import re
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path

SLUG = "child-labor-laws-and-schooling"
HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
LOGS = REPO / "literature" / "search-logs"
SCREEN = REPO / "temp" / "screen" / SLUG
RUN_LOG = LOGS / f"{SLUG}-screen-execution-log.json"


def load_validator():
    path = HERE / "59_child_labor_validate_screen.py"
    spec = importlib.util.spec_from_file_location("screen_validator", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def parse_batch_spec(value, available):
    if not value:
        return set(available)
    chosen = set()
    for part in value.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            left, right = part.split("-", 1)
            chosen.update(range(int(left), int(right) + 1))
        else:
            chosen.add(int(part))
    unknown = chosen - set(available)
    if unknown:
        raise SystemExit(f"unknown batch numbers: {sorted(unknown)}")
    return chosen


def strip_code_fence(text):
    text = text.strip()
    match = re.fullmatch(r"```(?:json)?\s*(.*?)\s*```", text, flags=re.DOTALL | re.IGNORECASE)
    return match.group(1).strip() if match else text


def validate_payload(payload, inputs, validator, label):
    errors = []
    if not isinstance(payload, list):
        return [f"{label}: model output is not a JSON array"]
    if len(payload) != len(inputs):
        return [f"{label}: expected {len(inputs)} verdicts, got {len(payload)}"]
    for index, (record, paper) in enumerate(zip(payload, inputs), start=1):
        errors.extend(validator.validate_record(record, paper["paperId"], f"{label} row {index}"))
    return errors


def existing_valid(path, inputs, validator, label):
    if not path.exists():
        return False
    try:
        payload = json.loads(path.read_text())
    except json.JSONDecodeError:
        return False
    return not validate_payload(payload, inputs, validator, label)


def atomic_write_json(path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=path.name + ".", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(fd, "w") as handle:
            json.dump(payload, handle, indent=2, ensure_ascii=False)
            handle.write("\n")
        os.replace(temporary, path)
    except Exception:
        try:
            os.unlink(temporary)
        except FileNotFoundError:
            pass
        raise


def load_log():
    if not RUN_LOG.exists():
        return {"slug": SLUG, "runs": []}
    return json.loads(RUN_LOG.read_text())


def save_log(log):
    RUN_LOG.write_text(json.dumps(log, indent=2, ensure_ascii=False) + "\n")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--audit", action="store_true", help="show batch readiness; invoke nothing")
    parser.add_argument("--batches", help="comma/range selection, e.g. 1-3,8")
    parser.add_argument("--force", action="store_true", help="replace already-valid selected outputs")
    parser.add_argument("--timeout", type=int, default=900, help="seconds per batch (default 900)")
    parser.add_argument("--command", nargs=argparse.REMAINDER,
                        help="authorized model argv, e.g. --command claude -p")
    args = parser.parse_args()

    manifest = json.loads((LOGS / f"{SLUG}-screen-manifest.json").read_text())
    validator = load_validator()
    available = [item["batch"] for item in manifest["manifest"]]
    selected = parse_batch_spec(args.batches, available)
    statuses = []
    for item in manifest["manifest"]:
        if item["batch"] not in selected:
            continue
        inputs = json.loads((REPO / item["input"]).read_text())
        output = REPO / item["output"]
        valid = existing_valid(output, inputs, validator, f"batch {item['batch']:03d}")
        statuses.append((item, inputs, output, valid))
    ready = sum(valid for _, _, _, valid in statuses)
    print(f"selected {len(statuses)} batches; valid existing {ready}; pending {len(statuses) - ready}")
    if args.audit:
        for item, _, output, valid in statuses:
            print(f"batch {item['batch']:03d}: {'VALID' if valid else 'PENDING'} -> {output.relative_to(REPO)}")
        return 0

    command = list(args.command or [])
    if command and command[0] == "--":
        command = command[1:]
    if not command:
        print("No model invoked. Supply an explicitly authorized argv after --command.", file=sys.stderr)
        return 2
    rubric = (LOGS / f"{SLUG}-screen-rubric.md").read_text()
    run = {
        "started_utc": datetime.now(timezone.utc).isoformat(),
        "command_executable": Path(command[0]).name,
        "command_args": command[1:],
        "selected_batches": sorted(selected),
        "force": args.force,
        "results": [],
    }
    log = load_log()
    failed = False
    try:
        for item, inputs, output, valid in statuses:
            number = item["batch"]
            if valid and not args.force:
                run["results"].append({"batch": number, "status": "skipped_valid"})
                continue
            prompt = (rubric + "\n\n## Batch to screen\n\n" +
                      json.dumps(inputs, indent=2, ensure_ascii=False) +
                      "\n\nReturn only the required JSON array in the same order.\n")
            started = time.monotonic()
            try:
                result = subprocess.run(command, input=prompt, text=True, capture_output=True,
                                        timeout=args.timeout)
            except subprocess.TimeoutExpired:
                run["results"].append({"batch": number, "status": "timeout", "seconds": args.timeout})
                print(f"batch {number:03d}: TIMEOUT", file=sys.stderr)
                failed = True
                break
            seconds = round(time.monotonic() - started, 2)
            if result.returncode != 0:
                run["results"].append({"batch": number, "status": "model_error",
                                       "returncode": result.returncode, "seconds": seconds,
                                       "stderr_tail": result.stderr[-1000:],
                                       "stdout_tail": result.stdout[-1000:]})
                print(f"batch {number:03d}: model exit {result.returncode}", file=sys.stderr)
                failed = True
                break
            try:
                payload = json.loads(strip_code_fence(result.stdout))
            except json.JSONDecodeError as exc:
                run["results"].append({"batch": number, "status": "invalid_json",
                                       "seconds": seconds, "error": str(exc)})
                print(f"batch {number:03d}: invalid JSON", file=sys.stderr)
                failed = True
                break
            errors = validate_payload(payload, inputs, validator, f"batch {number:03d}")
            if errors:
                run["results"].append({"batch": number, "status": "schema_error",
                                       "seconds": seconds, "errors": errors[:20]})
                print(f"batch {number:03d}: {len(errors)} validation errors", file=sys.stderr)
                failed = True
                break
            atomic_write_json(output, payload)
            run["results"].append({"batch": number, "status": "written_valid", "seconds": seconds})
            print(f"batch {number:03d}: valid ({seconds:.1f}s)")
    finally:
        run["finished_utc"] = datetime.now(timezone.utc).isoformat()
        log["runs"].append(run)
        save_log(log)
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
