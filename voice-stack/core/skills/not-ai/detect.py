#!/usr/bin/env python3
"""
not-ai detector — run a draft through an AI-writing detector and report the
overall AI score plus the specific sentences the detector flagged.

Stdlib only (urllib). No pip install required.

Providers (pick automatically by which API key is set, or force with --provider):
  - pangram  : POST https://text.external-api.pangram.com/task   (header x-api-key)
               Most accurate (UChicago-validated). Returns fraction_ai (0..1)
               and per-sentence segments. Async: returns a task_id you poll.
  - gptzero  : POST https://api.gptzero.me/v2/predict/text        (header x-api-key)
               Synchronous; free tier available. Returns documents[].sentences[]
               with highlight_sentence_for_ai + generated_prob.

Usage:
  export PANGRAM_API_KEY=...      # or GPTZERO_API_KEY=...
  python3 detect.py DRAFT.md
  python3 detect.py DRAFT.md --json
  python3 detect.py DRAFT.md --provider gptzero --threshold 0.5 --sentence-threshold 0.5

Exit codes:
  0  PASS  (overall score < threshold AND no sentence over sentence-threshold)
  1  FAIL  (detector flags remain — feed the flagged sentences to the rewrite loop)
  2  usage/config error (no API key, bad args, network error)

Output (human): a summary line + a numbered list of flagged sentences.
Output (--json): {provider, overall_ai_score, threshold, sentence_threshold,
                  passed, flagged_sentences:[{text, score}]}
"""

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request

PANGRAM_URL = "https://text.external-api.pangram.com/task"
GPTZERO_URL = "https://api.gptzero.me/v2/predict/text"


def _post(url, payload, headers, timeout=60):
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def _get(url, headers, timeout=60):
    req = urllib.request.Request(url, headers=headers, method="GET")
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def detect_gptzero(text, key, sentence_threshold):
    """Synchronous. Returns (overall_ai_score, [(sentence, score), ...])."""
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "x-api-key": key,
    }
    resp = _post(GPTZERO_URL, {"document": text}, headers)
    doc = (resp.get("documents") or [{}])[0]
    overall = doc.get("average_generated_prob")
    if overall is None:
        cp = doc.get("class_probabilities") or {}
        overall = cp.get("ai", cp.get("generated", 0.0))
    flagged = []
    for s in doc.get("sentences", []) or []:
        score = s.get("generated_prob", 0.0)
        if s.get("highlight_sentence_for_ai") or score >= sentence_threshold:
            flagged.append((s.get("sentence", "").strip(), round(float(score), 3), "AI"))
    return float(overall or 0.0), flagged


def detect_pangram(text, key, sentence_threshold, poll_seconds=2, max_polls=30):
    """Async task model. Returns (overall_ai_score, [(sentence, score), ...]).

    The POST returns either the result directly (fraction_ai present) or a
    task_id to poll. The poll URL below is best-effort; confirm against
    docs.pangram.com/api-reference if Pangram changes it.
    """
    headers = {"Content-Type": "application/json", "x-api-key": key}
    resp = _post(PANGRAM_URL, {"text": text, "public_dashboard_link": False}, headers)

    if "fraction_ai" not in resp and resp.get("task_id"):
        task_id = resp["task_id"]
        for _ in range(max_polls):
            time.sleep(poll_seconds)
            try:
                resp = _get(f"{PANGRAM_URL}/{task_id}", headers)
            except urllib.error.HTTPError:
                resp = _get(f"{PANGRAM_URL}?task_id={task_id}", headers)
            stage = resp.get("stage", "")
            if stage in ("STAGE_SUCCESS", "STAGE_FAILED") or "fraction_ai" in resp:
                break

    # Pangram splits the text into "windows" and reports three fractions that
    # sum to 1: fraction_human, fraction_ai (fully AI), fraction_ai_assisted.
    # Use 1 - fraction_human so AI-*assisted* prose (what a model edit produces)
    # is caught, not just fully-AI text.
    fraction_human = resp.get("fraction_human")
    if fraction_human is None:
        overall = float(resp.get("fraction_ai", 0.0) or 0.0)
    else:
        overall = 1.0 - float(fraction_human)
    flagged = []
    for w in resp.get("windows", []) or []:
        text_seg = (w.get("text") or "").strip()
        score = float(w.get("ai_assistance_score", 0.0) or 0.0)
        label = w.get("label", "") or ""
        is_ai = score >= sentence_threshold or ("AI" in label and "Human" not in label)
        if is_ai and text_seg:
            flagged.append((text_seg, round(score, 3), label or "AI"))
    return overall, flagged


def main():
    ap = argparse.ArgumentParser(description="Run a draft through an AI-writing detector.")
    ap.add_argument("file", help="Path to the draft (markdown/text). Use - for stdin.")
    ap.add_argument("--provider", choices=["auto", "pangram", "gptzero"], default="auto")
    ap.add_argument("--threshold", type=float, default=0.50,
                    help="Overall AI-score pass ceiling (default 0.50).")
    ap.add_argument("--sentence-threshold", type=float, default=0.50,
                    help="Per-sentence flag floor (default 0.50).")
    ap.add_argument("--json", action="store_true", help="Emit JSON instead of a human summary.")
    args = ap.parse_args()

    if args.file == "-":
        text = sys.stdin.read()
    else:
        try:
            with open(args.file, "r", encoding="utf-8") as fh:
                text = fh.read()
        except OSError as exc:
            print(f"[not-ai] cannot read {args.file}: {exc}", file=sys.stderr)
            return 2

    text = text.strip()
    if not text:
        print("[not-ai] empty input.", file=sys.stderr)
        return 2

    pangram_key = os.environ.get("PANGRAM_API_KEY")
    gptzero_key = os.environ.get("GPTZERO_API_KEY")

    provider = args.provider
    if provider == "auto":
        provider = "pangram" if pangram_key else ("gptzero" if gptzero_key else None)
    if provider is None:
        print("[not-ai] No API key found. Set PANGRAM_API_KEY (preferred) or "
              "GPTZERO_API_KEY, or run the browser / LLM-critic fallback in SKILL.md.",
              file=sys.stderr)
        return 2

    try:
        if provider == "pangram":
            if not pangram_key:
                print("[not-ai] PANGRAM_API_KEY not set.", file=sys.stderr)
                return 2
            overall, flagged = detect_pangram(text, pangram_key, args.sentence_threshold)
        else:
            if not gptzero_key:
                print("[not-ai] GPTZERO_API_KEY not set.", file=sys.stderr)
                return 2
            overall, flagged = detect_gptzero(text, gptzero_key, args.sentence_threshold)
    except urllib.error.HTTPError as exc:
        print(f"[not-ai] {provider} API error {exc.code}: {exc.reason}", file=sys.stderr)
        return 2
    except (urllib.error.URLError, TimeoutError) as exc:
        print(f"[not-ai] network error: {exc}", file=sys.stderr)
        return 2

    passed = overall < args.threshold and not flagged

    if args.json:
        print(json.dumps({
            "provider": provider,
            "overall_ai_score": round(overall, 4),
            "threshold": args.threshold,
            "sentence_threshold": args.sentence_threshold,
            "passed": passed,
            "flagged_spans": [{"text": t, "score": s, "label": lab} for t, s, lab in flagged],
        }, indent=2))
    else:
        verdict = "PASS" if passed else "FAIL"
        print(f"[not-ai] provider={provider}  overall_ai_score={overall:.3f}  "
              f"threshold={args.threshold}  -> {verdict}")
        if flagged:
            print(f"[not-ai] {len(flagged)} flagged span(s):")
            for i, (t, s, lab) in enumerate(flagged, 1):
                print(f"  {i:>2}. ({s:.2f} {lab}) {t}")
        else:
            print("[not-ai] no individual spans flagged.")

    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
