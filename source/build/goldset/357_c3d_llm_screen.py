#!/usr/bin/env python3
"""357 — run the C.3.d title/abstract screen as a batched, reproducible LLM pass.

WHY THIS EXISTS. The screen was begun by hand (270 verdicts in
`extraction/quantity-quality-tradeoff-screen-verdicts.csv`). Hand screening produces an artifact
that cannot be re-run, re-derived, or audited: CLAUDE.md's production standard is "no manual steps
between raw data and final output", and a hand screen is exactly such a step. It also cannot be
checked for DRIFT -- records screened hours apart, under different surrounding context, with no way
to detect that the thresholds moved -- and it cannot support a genuine second rater, because
"independent" would mean the same reader re-reading their own work.

Measured cost for the 2,986 unscreened records at 40 records/request: ~0.54M input tokens and
~0.16M output tokens, i.e. $6.81 on Claude Opus 5 standard and $3.40 on the Batch API. Sonnet 5 is
$1.36 batched, Haiku 4.5 $0.68. Opus 5 is the default here because the routing calls are subtle --
scope §8 wall 2 turns on whose human capital the return accrues to, which is a mechanism reading and
not a vocabulary match.

DESIGN RULES, each from a defect this repository has already paid for.

* **A refusal is never a verdict.** `refusals-read-as-zeros`: a failed request recorded as "not
  found" manufactures confident negatives. Errors go to a separate errors file and those records
  stay UNSCREENED, so a re-run picks them up.
* **Every emitted row comes back with a verdict**, including the obvious excludes, or sensitivity
  has no denominator (`a-positives-only-screen-cannot-measure-sensitivity`). The script verifies
  the model returned a row for every id it was sent and re-queues any it did not.
* **Blinded.** No gold flag, no provenance, no arm membership is sent. The arm predicts the
  DIRECTION, which is scope §2's ruling (`blinded-screen-audits-the-anchors`).
* **Resumable and idempotent.** Verdicts are appended per batch, and the run skips ids already in
  the CSV. `stage-output-must-survive-rerun`: run every stage twice and compare.
* **The hand-screened 270 are kept and marked.** They are not silently overwritten: a `rater`
  column distinguishes them, and 358 reports agreement between the two raters on the overlap, which
  is the closest thing to a second-rater check this chapter has.

Usage:
  python3 source/build/goldset/357_c3d_llm_screen.py --dry-run     # cost + batch plan, no calls
  python3 source/build/goldset/357_c3d_llm_screen.py --limit 200   # screen 200 records
  python3 source/build/goldset/357_c3d_llm_screen.py               # screen everything left

Requires ANTHROPIC_API_KEY in the environment or in .env, and the `anthropic` package.
"""
import argparse
import csv
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
LOGS = ROOT / "literature" / "search-logs"
EXTR = ROOT / "extraction"
UNIVERSE = LOGS / "quantity-quality-tradeoff-screen-universe.json"
RUBRIC = LOGS / "quantity-quality-tradeoff-screen-rubric.md"
VERDICTS = EXTR / "quantity-quality-tradeoff-screen-verdicts.csv"
ERRORS = EXTR / "quantity-quality-tradeoff-screen-errors.jsonl"

MODEL = "claude-opus-5"
PER_REQUEST = 40
ABSTRACT_CHARS = 460
FIELDS = ["screen_id", "direction", "cell", "design", "wall_risk", "outcome_object",
          "title_only", "confidence", "note"]

CELLS = ["RETURN_FERTILITY", "SHOCK_FERTILITY", "QQ_SUBSTITUTION", "MIXED_RETURN_POSITION",
         "MIXED_CHILD_PARENT_RETURN", "MIXED_RETURN_INCOME", "RETURN_ASSOCIATION",
         "PERCEIVED_RETURN", "THEORY", "OFF_TOPIC", "OFF_OTHER", "UNCLEAR"]
DIRECTIONS = ["FORWARD", "BACKWARD", "BOTH", "NA"]
DESIGNS = ["RCT", "IV", "DID", "RDD", "EVENT_STUDY", "NATURAL_EXPERIMENT", "PANEL_FE",
           "CROSS_SECTION", "CALIBRATION", "DESCRIPTIVE", "REVIEW", "UNCLEAR", "NA"]
OUTCOME_OBJECTS = ["FERTILITY", "INVESTMENT_PER_CHILD", "CHILD_ATTAINMENT", "OTHER", "NA"]
WALLS = ["W1_POSITION", "W2_PARENT_RETURN", "W4_INCOME", "W5_A12_TWINNING", "W6_MORTALITY",
         "W7_SCHOOLING_LAW"]

SCHEMA = {
    "type": "object",
    "properties": {
        "verdicts": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "screen_id": {"type": "string"},
                    "direction": {"type": "string", "enum": DIRECTIONS},
                    "cell": {"type": "string", "enum": CELLS},
                    "design": {"type": "string", "enum": DESIGNS},
                    "wall_risk": {"type": "array", "items": {"type": "string", "enum": WALLS}},
                    "outcome_object": {"type": "string", "enum": OUTCOME_OBJECTS},
                    "title_only": {"type": "boolean"},
                    "confidence": {"type": "string", "enum": ["HIGH", "MED", "LOW"]},
                    "note": {"type": "string"},
                },
                "required": ["screen_id", "direction", "cell", "design", "wall_risk",
                             "outcome_object", "title_only", "confidence", "note"],
                "additionalProperties": False,
            },
        }
    },
    "required": ["verdicts"],
    "additionalProperties": False,
}


def load_key():
    k = os.environ.get("ANTHROPIC_API_KEY")
    if k:
        return k
    env = ROOT / ".env"
    if env.exists():
        for line in env.read_text().splitlines():
            if line.startswith("ANTHROPIC_API_KEY="):
                return line.split("=", 1)[1].strip().strip('"') or None
    return None


def already_screened():
    if not VERDICTS.exists():
        return set()
    with VERDICTS.open() as f:
        return {r["screen_id"] for r in csv.DictReader(f)}


def rows_to_screen():
    recs = json.loads(UNIVERSE.read_text())["records"]
    done = already_screened()
    out = []
    for i, r in enumerate(recs):
        sid = f"C3D{i:04d}"
        if sid in done:
            continue
        ab = (r.get("abstract") or "").strip()
        out.append({
            "screen_id": sid,
            "title": r.get("title") or "(untitled)",
            "year": r.get("year"),
            "venue": r.get("venue") or "no venue",
            "type": r.get("type"),
            "cited_by": r.get("cited_by"),
            # Blinded: `arms` and `provenance` are deliberately NOT included.
            "abstract": (ab[:ABSTRACT_CHARS] + "…") if len(ab) > ABSTRACT_CHARS else ab,
            "title_only": not bool(ab),
        })
    return out


def render(batch):
    parts = []
    for r in batch:
        parts.append(
            f"### {r['screen_id']}\n"
            f"TITLE: {r['title']}\n"
            f"YEAR: {r['year']} | VENUE: {r['venue']} | TYPE: {r['type']} | "
            f"CITED: {r['cited_by']}\n"
            f"ABSTRACT: {r['abstract'] or '**NO ABSTRACT — title-only judgement**'}\n")
    return "\n".join(parts)


SYSTEM = """You are screening titles and abstracts for a Cochrane-style systematic review of \
explanations for fertility decline. Apply the rubric below exactly.

Return a verdict for EVERY record you are given, including the obvious excludes. A missing row \
makes the screen's sensitivity uncomputable. Do not skip, do not summarise, do not editorialise.

Set title_only=true whenever the record shows no abstract, and prefer UNCLEAR over a confident \
cell in that case.

{rubric}"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--limit", type=int)
    ap.add_argument("--model", default=MODEL)
    ap.add_argument("--per-request", type=int, default=PER_REQUEST)
    a = ap.parse_args()

    todo = rows_to_screen()
    if a.limit:
        todo = todo[:a.limit]
    batches = [todo[i:i + a.per_request] for i in range(0, len(todo), a.per_request)]
    rubric = RUBRIC.read_text()
    est_in = sum(len(SYSTEM.format(rubric=rubric)) + len(render(b)) for b in batches) / 3.8
    est_out = len(todo) * 55
    price = {"claude-opus-5": (5.0, 25.0), "claude-sonnet-5": (2.0, 10.0),
             "claude-haiku-4-5": (1.0, 5.0)}.get(a.model, (5.0, 25.0))
    cost = est_in / 1e6 * price[0] + est_out / 1e6 * price[1]
    print(f"{len(todo)} records to screen in {len(batches)} requests of {a.per_request}")
    print(f"  est input ~{est_in/1e6:.3f}M tok, output ~{est_out/1e6:.3f}M tok")
    print(f"  est cost on {a.model}: ${cost:.2f} standard")
    if a.dry_run:
        print("\n--dry-run: no API calls made")
        return 0

    key = load_key()
    if not key:
        sys.exit("no ANTHROPIC_API_KEY in the environment or .env — refusing to proceed.\n"
                 "This script spends money; it will not guess at a credential.")
    try:
        import anthropic
    except ImportError:
        sys.exit("the `anthropic` package is not installed: pip install anthropic")

    client = anthropic.Anthropic(api_key=key)
    new = VERDICTS.exists()
    fh = VERDICTS.open("a", newline="")
    w = csv.DictWriter(fh, fieldnames=FIELDS + ["rater"])
    if not new:
        w.writeheader()

    n_ok = n_err = 0
    for bi, batch in enumerate(batches):
        ids = {r["screen_id"] for r in batch}
        try:
            resp = client.messages.create(
                model=a.model, max_tokens=16000,
                system=[{"type": "text", "text": SYSTEM.format(rubric=rubric),
                         "cache_control": {"type": "ephemeral"}}],
                output_config={"format": {"type": "json_schema", "schema": SCHEMA}},
                messages=[{"role": "user",
                           "content": f"Screen these {len(batch)} records:\n\n{render(batch)}"}],
            )
            if resp.stop_reason == "refusal":
                raise RuntimeError(f"refusal: {getattr(resp, 'stop_details', None)}")
            payload = json.loads("".join(b.text for b in resp.content if b.type == "text"))
            got = {v["screen_id"]: v for v in payload["verdicts"]}
        except Exception as e:                                   # noqa: BLE001
            # A refusal or a transport error is NOT a verdict. The ids stay unscreened and a
            # re-run picks them up (`refusals-read-as-zeros`, `a-partial-run-must-write-nothing`).
            n_err += 1
            with ERRORS.open("a") as ef:
                ef.write(json.dumps({"batch": bi, "ids": sorted(ids),
                                     "error": f"{type(e).__name__}: {e}"[:500]}) + "\n")
            print(f"  batch {bi:>3}  ERROR {type(e).__name__} — {len(ids)} records left unscreened",
                  file=sys.stderr)
            continue

        missing = ids - set(got)
        for sid in sorted(ids & set(got)):
            v = got[sid]
            w.writerow({"screen_id": sid, "direction": v["direction"], "cell": v["cell"],
                        "design": v["design"], "wall_risk": ";".join(v["wall_risk"]),
                        "outcome_object": v["outcome_object"],
                        "title_only": str(v["title_only"]).lower(),
                        "confidence": v["confidence"],
                        "note": v["note"].replace("\n", " ")[:300], "rater": "llm"})
        fh.flush()
        n_ok += len(ids) - len(missing)
        if missing:
            # Recorded, not silently dropped: an unreturned id is an unscreened record.
            with ERRORS.open("a") as ef:
                ef.write(json.dumps({"batch": bi, "ids": sorted(missing),
                                     "error": "model returned no verdict for these ids"}) + "\n")
        print(f"  batch {bi:>3}/{len(batches)}  {len(ids) - len(missing)}/{len(ids)} verdicts"
              + (f"  ({len(missing)} MISSING, left unscreened)" if missing else ""))

    fh.close()
    print(f"\n{n_ok} verdicts written, {n_err} batches errored.")
    if n_err or ERRORS.exists():
        print(f"errors in {ERRORS.name} — those records are UNSCREENED, not excluded. Re-run to "
              "pick them up.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
