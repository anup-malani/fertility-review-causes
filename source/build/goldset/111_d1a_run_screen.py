#!/usr/bin/env python3
r"""
111_d1a_run_screen.py — D.1.a. Run blinded screening batches through an explicitly chosen model.

Mirrors `60_run_child_labor_screen.py`. Resumable and fail-closed by design:

  - MODEL EXECUTION IS EXPLICIT. There is no default command. The operator passes one after
    `--command`, and only after authorising that runner. A screen that starts itself is a screen
    nobody costed.
  - NOTHING IS WRITTEN BEFORE IT VALIDATES. The payload is checked in memory by `110_`'s
    `validate_payload` -- the same function a later re-read uses -- and only then written by atomic
    rename. A half-written or half-valid verdict file can never appear on disk.
  - IT STOPS ON THE FIRST FAILURE. A timeout, a non-zero exit, unparseable JSON or a schema error
    ends the run rather than skipping the batch. A screen that quietly skips what it could not do
    reports a corpus as screened when part of it was not -- the truncated-pull failure in a
    different costume, which this chapter has met repeatedly.
  - A VALID EXISTING VERDICT IS NEVER RE-RUN without `--force`, so resuming costs only what failed.

Usage:
  python3 111_d1a_run_screen.py --kind calib --command claude -p     # calibration first
  python3 111_d1a_run_screen.py --kind batch --batches 1-10 --command claude -p
  python3 111_d1a_run_screen.py --kind calib --audit                 # readiness, no model call

Output: temp/screen/{slug}/verdict_{kind}_NNN.json
        literature/search-logs/{slug}-screen-execution-log.json   (non-secret)
"""
import argparse, importlib.util, json, os, re, subprocess, sys, tempfile, time
from datetime import datetime, timezone
from pathlib import Path

SLUG = "postmaterialism-individualism-secularization"
HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
LOGS = REPO / "literature" / "search-logs"
SCREEN = REPO / "temp" / "screen" / SLUG
RUN_LOG = LOGS / f"{SLUG}-screen-execution-log.json"

INSTRUCTION = (
    "\n\n## Batch to screen\n\n{batch}\n\n"
    "Return ONLY a JSON array, one object per paper, in the SAME ORDER as the input, with exactly "
    "the fields the rubric's `Required output` section specifies. No prose, no code fence, no "
    "commentary before or after the array.\n"
)


def load_validator():
    spec = importlib.util.spec_from_file_location(
        "d1a_screen_validator", HERE / "110_d1a_validate_screen.py")
    m = importlib.util.module_from_spec(spec)
    sys.argv = [sys.argv[0]]          # the validator inspects argv; keep ours out of it
    spec.loader.exec_module(m)
    return m


def strip_code_fence(text):
    t = (text or "").strip()
    m = re.search(r"```(?:json)?\s*(.*?)```", t, re.S)
    if m:
        t = m.group(1).strip()
    # Some runners prepend a line of prose; fall back to the outermost array.
    if not t.startswith("["):
        i, j = t.find("["), t.rfind("]")
        if i != -1 and j > i:
            t = t[i:j + 1]
    return t


def atomic_write_json(path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=str(path.parent), suffix=".tmp")
    try:
        with os.fdopen(fd, "w") as fh:
            json.dump(payload, fh, indent=2, ensure_ascii=False)
        os.replace(tmp, path)
    except Exception:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise


def parse_range(spec, available):
    if not spec:
        return set(available)
    out = set()
    for part in spec.split(","):
        part = part.strip()
        if "-" in part:
            a, b = part.split("-", 1)
            out |= set(range(int(a), int(b) + 1))
        elif part:
            out.add(int(part))
    return out & set(available)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kind", choices=["calib", "batch"], required=True)
    ap.add_argument("--batches", default="")
    ap.add_argument("--timeout", type=int, default=900)
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--audit", action="store_true")
    ap.add_argument("--command", nargs=argparse.REMAINDER, default=[])
    args = ap.parse_args()

    validator = load_validator()
    cells = validator.allowed_cells()
    man = json.loads((LOGS / f"{SLUG}-screen-manifest.json").read_text())
    rubric = (SCREEN / "RUBRIC.md").read_text()

    entries = [m for m in man["manifest"] if m["kind"] == args.kind]
    selected = parse_range(args.batches, [m["batch"] for m in entries])
    todo = []
    for m in entries:
        if m["batch"] not in selected:
            continue
        out = REPO / m["output"]
        valid = False
        if out.exists():
            _, errs = validator.validate_file(REPO / m["input"], out, cells)
            valid = not errs
        todo.append((m, valid))

    n_valid = sum(1 for _, v in todo if v)
    print(f"{args.kind}: {len(todo)} selected, {n_valid} already valid, "
          f"{len(todo) - n_valid} to run", file=sys.stderr)
    if args.audit:
        print("audit only -- no model invoked", file=sys.stderr)
        return
    if not args.command:
        raise SystemExit(
            "no --command given. Model execution is explicit here: pass the runner you have "
            "authorised, e.g. --command claude -p")

    run = {"started_utc": datetime.now(timezone.utc).isoformat(), "kind": args.kind,
           "command_head": args.command[0], "command_args": args.command[1:],
           "rubric_sha256": man["rubric_sha256"], "results": []}
    log = json.loads(RUN_LOG.read_text()) if RUN_LOG.exists() else []
    failed = False
    for m, valid in todo:
        n = m["batch"]
        if valid and not args.force:
            run["results"].append({"batch": n, "status": "skipped_valid"})
            continue
        inputs = json.loads((REPO / m["input"]).read_text())
        prompt = rubric + INSTRUCTION.format(
            batch=json.dumps(inputs, indent=2, ensure_ascii=False))
        t0 = time.monotonic()
        try:
            res = subprocess.run(args.command, input=prompt, text=True,
                                 capture_output=True, timeout=args.timeout)
        except subprocess.TimeoutExpired:
            run["results"].append({"batch": n, "status": "timeout", "seconds": args.timeout})
            print(f"{args.kind} {n:03d}: TIMEOUT", file=sys.stderr); failed = True; break
        secs = round(time.monotonic() - t0, 2)
        if res.returncode != 0:
            run["results"].append({"batch": n, "status": "model_error", "seconds": secs,
                                   "returncode": res.returncode,
                                   "stderr_tail": res.stderr[-800:]})
            print(f"{args.kind} {n:03d}: model exit {res.returncode}", file=sys.stderr)
            failed = True; break
        try:
            payload = json.loads(strip_code_fence(res.stdout))
        except json.JSONDecodeError as e:
            run["results"].append({"batch": n, "status": "invalid_json", "seconds": secs,
                                   "error": str(e), "stdout_head": res.stdout[:800]})
            print(f"{args.kind} {n:03d}: invalid JSON", file=sys.stderr); failed = True; break
        errs = validator.validate_payload(payload, inputs, cells, f"{args.kind} {n:03d}")
        if errs:
            run["results"].append({"batch": n, "status": "schema_error", "seconds": secs,
                                   "errors": errs[:20]})
            print(f"{args.kind} {n:03d}: {len(errs)} validation errors", file=sys.stderr)
            for e in errs[:8]:
                print("    " + e, file=sys.stderr)
            failed = True; break
        atomic_write_json(REPO / m["output"], payload)
        run["results"].append({"batch": n, "status": "written_valid", "seconds": secs})
        print(f"{args.kind} {n:03d}: ok ({secs}s, {len(payload)} verdicts)", file=sys.stderr)

    run["finished_utc"] = datetime.now(timezone.utc).isoformat()
    run["failed"] = failed
    log.append(run)
    RUN_LOG.write_text(json.dumps(log, indent=2, ensure_ascii=False))
    written = sum(1 for r in run["results"] if r["status"] == "written_valid")
    print(f"wrote {written} verdict file(s); log -> {RUN_LOG.name}", file=sys.stderr)
    if failed:
        print("RUN STOPPED ON FAILURE -- fix and re-run; valid batches are not repeated",
              file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
