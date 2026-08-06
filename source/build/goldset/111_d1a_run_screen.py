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
    # RETRY, BUT NEVER SKIP. A batch that fails validation is retried a few times and then STOPS the
    # run. Skipping past failures would be worse than useless for a yield sample: the observed
    # failures correlate with record type -- title-only records were dropping `reason` -- so
    # discarding failed batches would bias the estimate toward records that carry abstracts, which
    # are exactly the ones more likely to be judged RELEVANT. A transient omission deserves a retry;
    # a systematic one must still halt.
    ap.add_argument("--retries", type=int, default=2)
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--audit", action="store_true")
    ap.add_argument("--command", nargs=argparse.REMAINDER, default=[])
    args = ap.parse_args()

    validator = load_validator()
    cells = validator.allowed_cells()
    man = json.loads((LOGS / f"{SLUG}-screen-manifest.json").read_text())
    rubric = (SCREEN / "RUBRIC.md").read_text()

    # A VERDICT IS ONLY "VALID" IF IT WAS PRODUCED UNDER THE CURRENT RUBRIC.
    # Validity used to mean "parses and matches the schema", so editing the rubric left every
    # existing verdict looking fine and the runner skipped them all -- silently mixing verdicts from
    # two different rubrics in one screen. That is the stale-cache failure this session already fixed
    # in 103_'s page cache and 106_'s membership cache; third instance, same shape. The execution log
    # records which rubric each batch was screened under, and a batch screened under a different one
    # is stale by definition.
    rubric_sha = man["rubric_sha256"]
    prior = {}
    if RUN_LOG.exists():
        for run in json.loads(RUN_LOG.read_text()):
            for r in run.get("results", []):
                if r.get("status") == "written_valid":
                    prior[(run.get("kind"), r["batch"])] = run.get("rubric_sha256")

    entries = [m for m in man["manifest"] if m["kind"] == args.kind]
    selected = parse_range(args.batches, [m["batch"] for m in entries])
    todo, stale = [], 0
    for m in entries:
        if m["batch"] not in selected:
            continue
        out = REPO / m["output"]
        valid = False
        if out.exists():
            _, errs = validator.validate_file(REPO / m["input"], out, cells)
            valid = not errs
            if valid and prior.get((args.kind, m["batch"])) not in (rubric_sha, None):
                valid = False
                stale += 1
        todo.append((m, valid))
    if stale:
        print(f"  {stale} verdict file(s) were screened under a different rubric -- re-running them",
              file=sys.stderr)

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
        payload, last = None, None
        for attempt in range(1, args.retries + 2):
            t0 = time.monotonic()
            try:
                res = subprocess.run(args.command, input=prompt, text=True,
                                     capture_output=True, timeout=args.timeout)
            except subprocess.TimeoutExpired:
                last = {"status": "timeout", "seconds": args.timeout, "attempt": attempt}
                continue
            secs = round(time.monotonic() - t0, 2)
            if res.returncode != 0:
                last = {"status": "model_error", "seconds": secs, "attempt": attempt,
                        "returncode": res.returncode, "stderr_tail": res.stderr[-800:]}
                continue
            try:
                cand = json.loads(strip_code_fence(res.stdout))
            except json.JSONDecodeError as e:
                last = {"status": "invalid_json", "seconds": secs, "attempt": attempt,
                        "error": str(e), "stdout_head": res.stdout[:600]}
                continue
            errs = validator.validate_payload(cand, inputs, cells, f"{args.kind} {n:03d}")
            if errs:
                last = {"status": "schema_error", "seconds": secs, "attempt": attempt,
                        "errors": errs[:20]}
                print(f"{args.kind} {n:03d}: attempt {attempt} -> {len(errs)} validation errors",
                      file=sys.stderr)
                for e in errs[:4]:
                    print("    " + e, file=sys.stderr)
                continue
            payload, last = cand, {"status": "written_valid", "seconds": secs, "attempt": attempt}
            break
        if payload is None:
            run["results"].append({"batch": n, **last})
            print(f"{args.kind} {n:03d}: FAILED after {args.retries + 1} attempts "
                  f"({last['status']})", file=sys.stderr)
            failed = True
            break
        atomic_write_json(REPO / m["output"], payload)
        run["results"].append({"batch": n, **last})
        print(f"{args.kind} {n:03d}: ok ({last['seconds']}s, {len(payload)} verdicts, "
              f"attempt {last['attempt']})", file=sys.stderr)

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
