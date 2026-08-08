#!/usr/bin/env python3
"""
107_d2d_run_screen.py — run the D.2.d blinded title/abstract screen batches through an explicit runner.

Mirror of `99_d1b_run_screen.py`. Resumable and fail-closed: never uses a shell, never overwrites a
valid existing verdict unless --force, validates every response against step 106 BEFORE an atomic
rename, and records a non-secret execution log. Model execution is deliberately explicit — the
operator names the runner command, this script does not choose one.

  python3 107_d2d_run_screen.py --audit                      # readiness only, no model calls
  python3 107_d2d_run_screen.py --batches 1-5 --command claude -p    # WAVE 1, then stop and audit
  python3 107_d2d_run_screen.py --command claude -p          # every outstanding batch

WAVE GATE. Run batches 1-5 first and audit before spending the remaining 71. D.3.b's wave-1 audit
found four cell-level defects across 200 records and would have propagated them through 25 more
batches. Three of those defects are pre-fixed in this rubric at v1, which is a reason to expect a
cleaner wave 1 — not a reason to skip it. The point of a gate is that it can only help if it is shut.

The screen is BLINDED: batches carry paperId, title, year and abstract, nothing else. Discovery
channel, DOI, authors, venue, citation count, seed provenance and gold status were stripped at step
105 and must not be reintroduced here. That matters more on this chapter than earlier ones, because
41% of the frame is decoy-seeded and a screener able to see seed provenance would have a standing hint
to route exactly those records away.

A failed batch leaves no verdict file, so a re-run picks it up. That is the resumability contract, and
it is why the validator runs BEFORE the rename rather than after: a half-parsed response that gets
written and then found invalid is indistinguishable, on the next run, from a batch nobody has done.

Retrying is on the OUTPUT CONTRACT, never on the answer. The retry criterion is schema compliance and
record count; the prompt is byte-identical across attempts and no verdict is ever re-requested because
its content was unwelcome.
"""
import argparse, importlib.util, json, os, re, subprocess, sys, tempfile, time
from datetime import datetime, timezone
from pathlib import Path

SLUG = "child-centeredness-intensive-parenting"
HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
LOGS = REPO / "literature" / "search-logs"
SCREEN = REPO / "temp" / "screen" / SLUG
RUN_LOG = LOGS / f"{SLUG}-screen-execution-log.json"
QUARANTINE = SCREEN / "rejected"


def load_validator():
    spec = importlib.util.spec_from_file_location(
        "d2d_screen_validator", HERE / "106_d2d_validate_screen.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def parse_batch_spec(value, available):
    if not value:
        return available
    picked = set()
    for part in value.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            lo, hi = part.split("-", 1)
            picked.update(range(int(lo), int(hi) + 1))
        else:
            picked.add(int(part))
    return [b for b in available if b in picked]


PROMPT_HEAD = """You are screening records for a Cochrane-style systematic review, blind.

Apply the rubric below EXACTLY. Do not use outside knowledge about any paper. Judge only the title,
year, and abstract supplied. Return ONE JSON array, in input order, with exactly one object per input
record and no other text — no preamble, no markdown fence, no trailing commentary.

===== RUBRIC =====
{rubric}
===== END RUBRIC =====

===== RECORDS ({n}) =====
{records}
===== END RECORDS =====

Return the JSON array of {n} objects now."""


def extract_json_array(text):
    """Models sometimes wrap the array in a fence or add a sentence. Recover the array rather than
    failing the batch, but never 'repair' its contents — a truncated array must fail validation."""
    t = text.strip()
    fence = re.search(r"```(?:json)?\s*(.+?)```", t, re.S)
    if fence:
        t = fence.group(1).strip()
    start, end = t.find("["), t.rfind("]")
    if start == -1 or end == -1 or end < start:
        raise ValueError("no JSON array found in response")
    return json.loads(t[start:end + 1])


def atomic_write(path, payload):
    fd, tmp = tempfile.mkstemp(dir=str(path.parent), suffix=".tmp")
    with os.fdopen(fd, "w") as fh:
        json.dump(payload, fh, indent=2, ensure_ascii=False)
    os.replace(tmp, path)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--audit", action="store_true")
    ap.add_argument("--batches", default="")
    ap.add_argument("--force", action="store_true", help="redo batches that already have valid verdicts")
    ap.add_argument("--sleep", type=float, default=2.0)
    ap.add_argument("--retries", type=int, default=3,
                    help="attempts per batch; a fast non-zero exit is usually a concurrency limit "
                         "rather than a content problem")
    ap.add_argument("--command", nargs=argparse.REMAINDER,
                    help="runner command, e.g. --command claude -p (must be last)")
    args = ap.parse_args()

    validator = load_validator()
    manifest = json.loads((LOGS / f"{SLUG}-screen-manifest.json").read_text())
    rubric = (SCREEN / "RUBRIC.md").read_text()
    entries = {e["batch"]: e for e in manifest["manifest"]}
    todo = []
    for b in sorted(entries):
        vp = REPO / entries[b]["output"]
        if vp.exists() and not args.force:
            try:
                errs, _norm, _soft = validator.validate_batch(
                    REPO / entries[b]["input"], json.loads(vp.read_text()))
                if not errs:
                    continue
            except Exception:
                pass
        todo.append(b)
    todo = parse_batch_spec(args.batches, todo)

    print(f"{len(entries)} batches total; {len(todo)} outstanding")
    if args.audit or not args.command:
        if not args.audit:
            print("no --command given; nothing run (this is the fail-closed default)", file=sys.stderr)
        print("outstanding:", todo[:20], "..." if len(todo) > 20 else "")
        return 0

    log = json.loads(RUN_LOG.read_text()) if RUN_LOG.exists() else {"slug": SLUG, "runs": []}
    ok = fail = 0
    for b in todo:
        entry = entries[b]
        batch_path = REPO / entry["input"]
        records = json.loads(batch_path.read_text())
        prompt = PROMPT_HEAD.format(rubric=rubric, n=len(records),
                                    records=json.dumps(records, indent=1, ensure_ascii=False))
        t0 = time.time()
        last, normalized, softs = None, None, []
        try:
            for attempt in range(args.retries):
                proc = subprocess.run(list(args.command) + [prompt], capture_output=True,
                                      text=True, timeout=900)
                if proc.returncode != 0 or not proc.stdout.strip():
                    last = (f"runner exit {proc.returncode}: "
                            f"{(proc.stderr or proc.stdout or '<no output>').strip()[:200]}")
                else:
                    try:
                        payload = extract_json_array(proc.stdout)
                        errs, normalized, softs = validator.validate_batch(batch_path, payload)
                        if not errs:
                            break
                        last = f"{len(errs)} validation errors; first: {errs[0]}"
                        normalized = None
                    except Exception as pe:
                        last = f"unparseable response: {pe}"
                        normalized = None
                if attempt < args.retries - 1:
                    time.sleep(10 * (attempt + 1))
        except subprocess.TimeoutExpired:
            last, normalized = "timeout after 900s", None

        # QUARANTINE. A rejected response is the raw material of the wave-1 audit: the audit exists to
        # find rubric defects, and a rubric defect shows up precisely as a verdict the validator
        # refuses. Discarding it — as the inherited runner does — leaves the audit with an error
        # string and nothing to inspect, and makes "is the rubric wrong or is the screener wrong?"
        # unanswerable without paying for the batch again. Quarantined files are NEVER read by any
        # downstream step; they are diagnostic only, and live outside the verdict namespace so they
        # cannot be mistaken for verdicts.
        if normalized is None and 'proc' in dir() and getattr(proc, "stdout", ""):
            QUARANTINE.mkdir(parents=True, exist_ok=True)
            (QUARANTINE / f"rejected_{b:03d}.txt").write_text(
                f"# batch {b} rejected: {last}\n# NOT a verdict file. Diagnostic only.\n\n"
                + proc.stdout)

        dt = round(time.time() - t0, 1)
        if normalized:
            atomic_write(REPO / entry["output"], normalized)
            ok += 1
            print(f"  batch {b:03d}: OK ({len(normalized)} verdicts, {dt}s)"
                  + (f" [{len(softs)} soft flags]" if softs else ""))
            status = "ok"
        else:
            fail += 1
            print(f"  batch {b:03d}: FAIL ({dt}s) {last}", file=sys.stderr)
            status = "fail"
        log["runs"].append({
            "batch": b, "status": status, "seconds": dt,
            "n_records": len(records), "n_soft_flags": len(softs),
            "error": None if status == "ok" else last,
            "rejected_response": (None if status == "ok"
                                  else f"temp/screen/{SLUG}/rejected/rejected_{b:03d}.txt"),
            # The command is recorded WITHOUT its arguments-as-prompt, which would embed the whole
            # rubric and every abstract in the log for each batch.
            "command": (args.command or [None])[0],
            "at": datetime.now(timezone.utc).isoformat(timespec="seconds")})
        RUN_LOG.write_text(json.dumps(log, indent=2, ensure_ascii=False))
        time.sleep(args.sleep)

    print(f"\ndone: {ok} ok, {fail} failed")
    if fail:
        print("failed batches leave no verdict file; re-run to retry them", file=sys.stderr)
    return 1 if fail and not ok else 0


if __name__ == "__main__":
    sys.exit(main())
