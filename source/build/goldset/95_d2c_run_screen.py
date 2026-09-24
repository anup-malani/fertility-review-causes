#!/usr/bin/env python3
"""Run the D.2.c (son-preference-cultural) blinded screening batches through a chosen model.

Mirror of the C.2.h runner (58): resumable and fail-closed. It never uses a shell, never overwrites a
valid existing verdict unless --force is supplied, validates every response with
57_c2h_validate_screen.validate_record before an atomic rename, and records a non-secret execution log.
Screen with a cheap recall-preserving model (Haiku), per GACS D2a. The model argv is passed explicitly
after --command only once the operator has authorized the run.

Examples:
  python3 95_d2c_run_screen.py --audit
  python3 95_d2c_run_screen.py --batches 1-3 --command claude -p --model claude-haiku-4-5-20251001
  python3 95_d2c_run_screen.py --command claude -p --model claude-haiku-4-5-20251001
"""
import argparse, importlib.util, json, os, re, subprocess, sys, tempfile, time
from datetime import datetime, timezone
from pathlib import Path

SLUG = "son-preference-cultural"
HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
LOGS = REPO / "literature" / "search-logs"
SCREEN = REPO / "temp" / "screen" / SLUG


def run_log_path(suffix=""):
    return LOGS / f"{SLUG}-screen-execution-log{('-' + suffix) if suffix else ''}.json"


def load_validator():
    path = HERE / "94_d2c_validate_screen.py"
    spec = importlib.util.spec_from_file_location("d2c_screen_validator", path)
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
    fence = re.search(r"```(?:json)?\s*(.*?)\s*```", text, flags=re.DOTALL | re.IGNORECASE)
    if fence:
        return fence.group(1).strip()
    i, j = text.find("["), text.rfind("]")
    if 0 <= i < j:
        return text[i:j + 1]
    return text


def validate_payload(payload, inputs, validator, label):
    if not isinstance(payload, list):
        return [f"{label}: model output is not a JSON array"]
    if len(payload) != len(inputs):
        return [f"{label}: expected {len(inputs)} verdicts, got {len(payload)}"]
    errors = []
    for index, (record, paper) in enumerate(zip(payload, inputs), start=1):
        errors.extend(validator.validate_record(record, paper["id"], f"{label} row {index}"))
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


def load_log(path):
    if not path.exists():
        return {"slug": SLUG, "runs": []}
    return json.loads(path.read_text())


def save_log(path, log):
    path.write_text(json.dumps(log, indent=2, ensure_ascii=False) + "\n")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--audit", action="store_true", help="show batch readiness; invoke nothing")
    parser.add_argument("--batches", help="comma/range selection, e.g. 1-3,8")
    parser.add_argument("--force", action="store_true", help="replace already-valid selected outputs")
    parser.add_argument("--timeout", type=int, default=900, help="seconds per batch (default 900)")
    parser.add_argument("--retries", type=int, default=2, help="re-asks before fail-closed (default 2)")
    parser.add_argument("--log-suffix", default="", help="per-worker suffix so parallel runs don't clobber")
    parser.add_argument("--command", nargs=argparse.REMAINDER,
                        help="authorized model argv, e.g. --command claude -p --model claude-haiku-4-5-20251001")
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
            print(f"batch {item['batch']:03d}: {'VALID' if valid else 'PENDING'}")
        return 0

    command = list(args.command or [])
    if command and command[0] == "--":
        command = command[1:]
    if not command:
        print("No model invoked. Supply an authorized argv after --command.", file=sys.stderr)
        return 2
    rubric = (LOGS / f"{SLUG}-screen-rubric.md").read_text()
    run = {"started_utc": datetime.now(timezone.utc).isoformat(),
           "command_executable": Path(command[0]).name, "command_args": command[1:],
           "selected_batches": sorted(selected), "force": args.force, "results": []}
    rlog = run_log_path(args.log_suffix)
    log = load_log(rlog)
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
            outcome, last = None, None
            for attempt in range(args.retries + 1):
                started = time.monotonic()
                try:
                    result = subprocess.run(command, input=prompt, text=True, capture_output=True,
                                            timeout=args.timeout)
                except subprocess.TimeoutExpired:
                    last = {"batch": number, "status": "timeout", "seconds": args.timeout, "attempt": attempt + 1}
                    continue
                seconds = round(time.monotonic() - started, 2)
                if result.returncode != 0:
                    last = {"batch": number, "status": "model_error", "returncode": result.returncode,
                            "seconds": seconds, "attempt": attempt + 1,
                            "stderr_tail": result.stderr[-1000:], "stdout_tail": result.stdout[-1000:]}
                    continue
                try:
                    payload = json.loads(strip_code_fence(result.stdout))
                except json.JSONDecodeError as exc:
                    last = {"batch": number, "status": "invalid_json", "seconds": seconds,
                            "attempt": attempt + 1, "error": str(exc)}
                    continue
                errors = validate_payload(payload, inputs, validator, f"batch {number:03d}")
                if errors:
                    last = {"batch": number, "status": "schema_error", "seconds": seconds,
                            "attempt": attempt + 1, "errors": errors[:20]}
                    continue
                atomic_write_json(output, payload)
                outcome = {"batch": number, "status": "written_valid", "seconds": seconds,
                           "attempts": attempt + 1}
                break
            if outcome is not None:
                run["results"].append(outcome)
                print(f"batch {number:03d}: valid ({outcome['seconds']:.1f}s, attempt {outcome['attempts']})")
            else:
                run["results"].append(last)
                print(f"batch {number:03d}: {last['status']} after {args.retries + 1} attempts", file=sys.stderr)
                failed = True
                break
    finally:
        run["finished_utc"] = datetime.now(timezone.utc).isoformat()
        log["runs"].append(run)
        save_log(rlog, log)
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
