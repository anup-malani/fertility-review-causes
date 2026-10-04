#!/usr/bin/env python3
"""Run the C.3.a (mode of production) blinded screening batches through an explicitly chosen model command.

Adapts 60_run_child_labor_screen.py: only the slug and the validator module path change.

The runner is resumable and fail-closed. It never uses a shell, never overwrites a valid
existing verdict unless --force is supplied, validates every response before an atomic
rename, and records a non-secret execution log. Model execution is deliberately explicit:
pass a command after ``--command`` only after the operator has authorized that runner.

Examples (operator chooses one; do not run both on the same screen):
  python3 93_c3a_run_screen.py --command claude -p
  python3 93_c3a_run_screen.py --batches 1-3 --command claude -p

Use ``--audit`` to inspect readiness without invoking a model.
"""

import argparse
import importlib.util
import json
import os
import re
import signal
import subprocess
import sys
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

SLUG = "agricultural-mode-of-production"
HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
LOGS = REPO / "literature" / "search-logs"
SCREEN = REPO / "temp" / "screen" / SLUG
RUN_LOG = LOGS / f"{SLUG}-screen-execution-log.json"


def load_validator():
    path = HERE / "92_c3a_validate_screen.py"
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


def extract_json_array(text):
    """Tolerantly recover the verdict array. `claude -p` frequently prepends a prose preamble
    ("Based on the rubric, here is my screening...") before the array, so requiring the whole stdout
    to be clean JSON fails most batches. Try, in order: a clean fence/body; a fenced ```json array
    anywhere; the span from the first '[' to the last ']'. Raises ValueError if none parse."""
    try:
        return json.loads(strip_code_fence(text))
    except json.JSONDecodeError:
        pass
    m = re.search(r"```(?:json)?\s*(\[.*\])\s*```", text, flags=re.DOTALL | re.IGNORECASE)
    if m:
        try:
            return json.loads(m.group(1))
        except json.JSONDecodeError:
            pass
    i, j = text.find("["), text.rfind("]")
    if i != -1 and j > i:
        return json.loads(text[i:j + 1])  # may raise JSONDecodeError on a truncated array
    raise ValueError("no JSON array found in model output")


def run_model(command, prompt, timeout, cwd):
    """Run the model with a HARD timeout. subprocess.run(timeout=) only SIGKILLs the direct child, so
    if `claude` spawns a grandchild that inherits the stdout pipe, communicate() deadlocks waiting for
    EOF even after the child dies (the 17-min hang observed on the first run). Launch the child in its
    own session (process group) and kill the WHOLE group on timeout, then drain.

    Returns (returncode, stdout, stderr, timed_out). returncode is None on timeout.
    """
    proc = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, text=True, cwd=cwd, start_new_session=True)
    try:
        out, err = proc.communicate(input=prompt, timeout=timeout)
        return proc.returncode, out, err, False
    except subprocess.TimeoutExpired:
        try:
            os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
        except (ProcessLookupError, PermissionError):
            pass
        try:
            proc.communicate(timeout=30)
        except Exception:
            pass
        return None, "", "", True


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
    parser.add_argument("--timeout", type=int, default=240,
                        help="seconds per batch before killing the model process group (default 240)")
    parser.add_argument("--retries", type=int, default=4, help="model attempts per batch (default 4)")
    parser.add_argument("--workers", type=int, default=1,
                        help="concurrent batches / model subprocesses (default 1; batches are independent)")
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

    def process_batch(item, inputs, output):
        """Screen one batch, with retries. Self-contained (own subprocess + own verdict file), so it is
        safe to run many of these concurrently in a thread pool. Returns a result dict."""
        number = item["batch"]
        prompt = (rubric + "\n\n## Batch to screen\n\n" +
                  json.dumps(inputs, indent=2, ensure_ascii=False) +
                  "\n\nOutput ONLY the JSON array — no preamble, no prose, no explanation, no code "
                  "fence. One object per paper, in the same order. Your first character must be "
                  "'[' and your last must be ']'.\n")
        # The nested `claude -p` is intermittently flaky: a prose preamble (handled by the tolerant
        # parser), an occasional dropped item (count/schema mismatch), or a hang (killpg timeout).
        # Retry up to args.retries times; a persistently-failing batch is recorded and left for a later
        # re-run (the assembler 92 is fail-closed, so a missing batch never enters the gold).
        attempts = []
        for attempt in range(1, args.retries + 1):
            started = time.monotonic()
            # Neutral cwd: keep the nested model out of the project dir (settings/hook noise).
            returncode, stdout, stderr, timed_out = run_model(
                command, prompt, args.timeout, tempfile.gettempdir())
            seconds = round(time.monotonic() - started, 2)
            if timed_out:
                attempts.append({"attempt": attempt, "status": "timeout", "seconds": seconds})
                print(f"batch {number:03d} try {attempt}: TIMEOUT (killed group)", file=sys.stderr)
                continue
            if returncode != 0:
                attempts.append({"attempt": attempt, "status": "model_error",
                                 "returncode": returncode, "seconds": seconds,
                                 "stderr_tail": stderr[-500:]})
                print(f"batch {number:03d} try {attempt}: model exit {returncode}", file=sys.stderr)
                continue
            try:
                payload = extract_json_array(stdout)
            except (json.JSONDecodeError, ValueError) as exc:
                attempts.append({"attempt": attempt, "status": "invalid_json",
                                 "seconds": seconds, "error": str(exc)})
                print(f"batch {number:03d} try {attempt}: invalid JSON", file=sys.stderr)
                continue
            errors = validate_payload(payload, inputs, validator, f"batch {number:03d}")
            if errors:
                attempts.append({"attempt": attempt, "status": "schema_error",
                                 "seconds": seconds, "errors": errors[:8]})
                print(f"batch {number:03d} try {attempt}: {len(errors)} validation errors", file=sys.stderr)
                continue
            atomic_write_json(output, payload)
            print(f"batch {number:03d}: valid ({seconds:.1f}s, try {attempt})")
            return {"batch": number, "status": "written_valid", "seconds": seconds, "attempts": attempt}
        print(f"batch {number:03d}: FAILED after {args.retries} tries — continuing", file=sys.stderr)
        return {"batch": number, "status": "failed_after_retries", "attempts": attempts}

    pending = [(item, inputs, output) for item, inputs, output, valid in statuses
               if not valid or args.force]
    for item, _, _, valid in statuses:
        if valid and not args.force:
            run["results"].append({"batch": item["batch"], "status": "skipped_valid"})
    print(f"running {len(pending)} batches with {args.workers} worker(s)")
    failed = False
    try:
        if args.workers <= 1:
            for item, inputs, output in pending:
                res = process_batch(item, inputs, output)
                run["results"].append(res)
                failed = failed or res["status"] != "written_valid"
        else:
            with ThreadPoolExecutor(max_workers=args.workers) as pool:
                futures = {pool.submit(process_batch, item, inputs, output): item["batch"]
                           for item, inputs, output in pending}
                for fut in as_completed(futures):
                    res = fut.result()
                    run["results"].append(res)
                    failed = failed or res["status"] != "written_valid"
    finally:
        run["finished_utc"] = datetime.now(timezone.utc).isoformat()
        run["results"].sort(key=lambda r: r["batch"])
        log["runs"].append(run)
        save_log(log)
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
