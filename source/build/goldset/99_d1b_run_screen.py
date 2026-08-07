#!/usr/bin/env python3
"""
99_d1b_run_screen.py — run the D.1.b blinded title/abstract screen batches through an explicit runner.

Mirror of `60_run_child_labor_screen.py`. Resumable and fail-closed: never uses a shell, never
overwrites a valid existing verdict unless --force, validates every response against step 98 before an
atomic rename, and records a non-secret execution log. Model execution is deliberately explicit — the
operator names the runner command, this script does not choose one.

  python3 99_d1b_run_screen.py --audit                     # readiness only, no model calls
  python3 99_d1b_run_screen.py --command claude -p         # run every outstanding batch
  python3 99_d1b_run_screen.py --batches 1-5 --command claude -p

The screen is BLINDED: batches carry paperId, title, year, abstract and nothing else. Discovery
channel, DOI, authors, venue, citation count, and gold status were stripped at step 97 and must not be
reintroduced here — the whole point is that a screener cannot infer a verdict from where a paper came
from.

A failed batch leaves no verdict file, so a re-run picks it up. That is the resumability contract, and
it is why the validator runs BEFORE the rename rather than after: a half-parsed response that gets
written and then found invalid is indistinguishable, on the next run, from a batch nobody has done.
"""
import argparse, importlib.util, json, os, re, subprocess, sys, tempfile, time
from datetime import datetime, timezone
from pathlib import Path

SLUG = "caldwell-wealth-flows-westernization"
HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
LOGS = REPO / "literature" / "search-logs"
SCREEN = REPO / "temp" / "screen" / SLUG
RUN_LOG = LOGS / f"{SLUG}-screen-execution-log.json"


def load_validator():
    spec = importlib.util.spec_from_file_location(
        "d1b_screen_validator", HERE / "98_d1b_validate_screen.py")
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
    start = t.find("[")
    end = t.rfind("]")
    if start == -1 or end == -1 or end < start:
        raise ValueError("no JSON array found in response")
    return json.loads(t[start:end + 1])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--audit", action="store_true")
    ap.add_argument("--batches", default="")
    ap.add_argument("--force", action="store_true", help="redo batches that already have valid verdicts")
    ap.add_argument("--sleep", type=float, default=2.0)
    ap.add_argument("--retries", type=int, default=3,
                    help="attempts per batch before giving up; a fast non-zero exit is "
                         "usually a concurrency limit rather than a content problem")
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
                errs, _ = validator.validate_batch(REPO / entries[b]["input"], json.loads(vp.read_text()))
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
        try:
            # Retry with backoff. Running five runners concurrently made the CLI return exit 1 in
            # under two seconds for 92 of 125 batches — a concurrency limit, not a content problem,
            # and indistinguishable from a real failure without a retry. A fast non-zero exit is
            # almost always transient; a slow one is usually not, so the backoff is generous.
            # One attempt budget covering BOTH failure modes, because both are transient in the same
            # way: a runner exit-1 under concurrency, and a response that drops a record or violates
            # a schema rule. Retrying a schema failure is not cherry-picking a verdict — the retry
            # criterion is compliance with the output contract, never agreement with a desired
            # answer, and the prompt is byte-identical across attempts.
            last, normalized = None, None
            for attempt in range(args.retries):
                proc = subprocess.run(list(args.command) + [prompt], capture_output=True, text=True,
                                      timeout=900)
                if proc.returncode != 0 or not proc.stdout.strip():
                    last = (f"runner exit {proc.returncode}: "
                            f"{(proc.stderr or proc.stdout or '<no output>').strip()[:200]}")
                else:
                    try:
                        payload = extract_json_array(proc.stdout)
                        errs, normalized = validator.validate_batch(batch_path, payload)
                        if not errs:
                            break
                        last = f"{len(errs)} validation errors; first: {errs[0]}"
                        normalized = None
                    except Exception as pe:
                        last = f"unparseable response: {pe}"
                        normalized = None
                if attempt < args.retries - 1:
                    time.sleep(10 * (attempt + 1))
            if normalized is None:
                raise RuntimeError(last or "runner produced no usable output")
            # Atomic rename only after validation passes.
            with tempfile.NamedTemporaryFile("w", dir=str(SCREEN), delete=False,
                                             suffix=".tmp", encoding="utf-8") as fh:
                json.dump(normalized, fh, indent=2, ensure_ascii=False)
                tmp = fh.name
            os.replace(tmp, REPO / entry["output"])
            ok += 1
            status, detail = "ok", ""
        except Exception as e:
            fail += 1
            status, detail = "fail", str(e)[:300]
        dt = round(time.time() - t0, 1)
        print(f"  batch {b:03d} [{status}] {dt}s {detail}")
        log["runs"].append({"batch": b, "status": status, "seconds": dt,
                            "at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                            "runner": " ".join(args.command), "detail": detail})
        RUN_LOG.write_text(json.dumps(log, indent=2))
        time.sleep(args.sleep)
    print(f"done: {ok} ok, {fail} failed")
    return 0 if fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
