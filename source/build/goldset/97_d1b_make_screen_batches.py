#!/usr/bin/env python3
"""
97_d1b_make_screen_batches.py — D.1.b (cultural westernization / developmental idealism), stage A5 input.

Prepare the Tier-B frame for blinded title/abstract LLM screening. Mirror of `75_d3b_make_screen_batches.py`
with two departures, both consequences of this frame being four times the size of D.3.b's.

DEPARTURE 1 — the abstract-bearing records are screened; the title-only records are NOT.
  D.3.b screened its whole 1,170-record frame and let the rubric's title-only policy route abstract-less
  records to UNCERTAIN / INSUFFICIENT_INFO. That policy is right, but at this scale it means paying for
  1,578 model calls whose answer is already determined by the policy: a record with no abstract that does
  not state its estimand verbatim in the title CANNOT be routed, and the rubric says so.

  So this script splits the frame. The 3,123 abstract-bearing records are batched for screening. The
  title-only records are written to a separate file, pre-assigned UNCERTAIN / INSUFFICIENT_INFO by the
  rubric's own rule, and carried into the corpus rather than dropped. They remain part of the frame and
  part of every denominator; they are simply not sent to a model to be told what the rubric already says.

  **This is a deliberate coverage limit and it is reported as one, not silently absorbed.** The screen
  report must state that 1,578 records (34% of the frame) were never model-screened, because a reader
  who sees "3,123 screened" and a 4,701-record frame is entitled to know which is the denominator. If
  the RA gate later finds primary-cell papers hiding in the title-only stratum, the fix is to resolve
  abstracts for that stratum and screen it, not to leave the gap unstated.

DEPARTURE 2 — no D1 deterministic pre-rank, because there is no keyword channel to rank within.
  GACS D1 orders records by term-match score and applies a budget cutoff *within the keyword channel
  only*, precisely so that orthogonally-discovered papers bypass it. This frame is entirely
  citation-sourced: every record arrived by backward reference or forward citation, so every record is
  an orthogonal-channel record and every one would bypass a D1 cutoff by the rule's own logic. Running
  D1 here would either do nothing or, if misapplied to the whole frame, discard exactly the papers the
  architecture exists to catch. Recorded here so its absence reads as a decision rather than an omission.

Blinding is unchanged and is the point of the stage: records are deterministically shuffled and stripped
of DOI, authors, venue, citation count, discovery channel, seed provenance, and gold status, so the
screener cannot infer a verdict from where a paper came from. A committed manifest records paths and
SHA-256; batch payloads live in temp/ and are reproducible from the committed frame.

The eight routing decoys must surface as route-away — Kaplan 1994 -> OFF_WEALTH_FLOWS_C3f, Surkyn &
Lesthaeghe 2004 -> OFF_POSTMATERIALIST_D1a, Kohler et al. 2001 -> OFF_DIFFUSION_CHANNEL_A20, Cleland &
Wilson 1987 -> OFF_FERTILITY_CONTROL_A3, Upadhyay et al. 2014 -> OFF_FEMALE_AUTONOMY_D2a, Osili & Long
2007 -> MECHANISM_UNRESOLVED_SCHOOLING, Colleran et al. 2014 -> OFF_CULTURAL_EVOLUTION_D1c, and Coale &
Watkins 1986 -> OFF_OTHER — as the routing check. Note the decoys are ANCHORS, so they are not in the
Tier-B frame; the check applies to whatever near-neighbours of theirs the frame contains.

Inputs : literature/search-logs/{slug}-tier-b-frame.json
         literature/search-logs/{slug}-screen-rubric.md   (single source of truth, written at A1)
Outputs: temp/screen/{slug}/batch_NNN.json, RUBRIC.md
         literature/search-logs/{slug}-screen-manifest.json
         literature/search-logs/{slug}-title-only-stratum.json
"""
import hashlib, json, random
from pathlib import Path

SLUG = "caldwell-wealth-flows-westernization"
SEED = 1063  # D.1.b — TICK-063
BATCH_SIZE = 25
MIN_ABSTRACT_CHARS = 30   # same threshold the A4 frame log uses for "usable abstract"
# 25, not D.3.b's 40. At 40 the runner's first live batch came back with 39 of 40 verdicts: this
# rubric demands eleven fields per record, so a 40-record batch pushes the response long enough that
# the tail gets dropped. The validator caught it (that is what fail-closed is for), but a silent
# retry loop at 40 would burn two and a half minutes per attempt to rediscover the same limit.
HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
LOGS = REPO / "literature" / "search-logs"
SCREEN = REPO / "temp" / "screen" / SLUG
SCREEN.mkdir(parents=True, exist_ok=True)

# The rubric is NOT duplicated into this script. D.3.b embedded it as a string constant and wrote it
# out, which makes the script the source of truth and the committed rubric a copy; any later edit to
# the rubric file is then silently overwritten on the next batching run. Here the A1 rubric file is the
# source of truth and this script only copies it into the batch directory.
RUBRIC_PATH = LOGS / f"{SLUG}-screen-rubric.md"


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    source = LOGS / f"{SLUG}-tier-b-frame.json"
    records = json.loads(source.read_text())
    ids = [r.get("paperId") for r in records]
    if any(not v for v in ids) or len(ids) != len(set(ids)):
        raise SystemExit("frame must have unique, nonblank paperId values")
    if not RUBRIC_PATH.exists():
        raise SystemExit(f"rubric missing: {RUBRIC_PATH}")
    rubric = RUBRIC_PATH.read_text()

    def has_abstract(r):
        return len((r.get("abstract") or "").strip()) >= MIN_ABSTRACT_CHARS

    screenable = [r for r in records if has_abstract(r)]
    title_only = [r for r in records if not has_abstract(r)]

    # The title-only stratum, pre-assigned by the rubric's own title-only rule. Carried into the corpus,
    # counted in every denominator, and NOT sent to a model.
    (LOGS / f"{SLUG}-title-only-stratum.json").write_text(json.dumps(
        [{"paperId": r["paperId"], "title": r.get("title") or "", "year": r.get("year"),
          "verdict": "UNCERTAIN", "estimand_cell": "INSUFFICIENT_INFO", "outcome_level": "NA",
          "shared_with": "none", "treatment": "n/a", "outcome": "n/a",
          "structural_change_held_fixed": "unclear", "setting_era": "NA", "evidence_type": "other",
          "reason": "no abstract in the frame; rubric title-only policy assigns INSUFFICIENT_INFO "
                    "rather than a cell the record has not earned",
          "assigned_by": "rubric_title_only_policy_not_model"}
         for r in title_only], indent=2, ensure_ascii=False))

    shuffled = list(screenable)
    random.Random(SEED).shuffle(shuffled)
    (SCREEN / "RUBRIC.md").write_text(rubric)
    manifest, assigned = [], []
    for start in range(0, len(shuffled), BATCH_SIZE):
        number = start // BATCH_SIZE + 1
        batch = []
        for row in shuffled[start:start + BATCH_SIZE]:
            batch.append({
                "paperId": row["paperId"],
                "title": row.get("title") or "",
                "year": row.get("year"),
                "abstract": (row.get("abstract") or "")[:3500],
            })
            assigned.append(row["paperId"])
        ip = SCREEN / f"batch_{number:03d}.json"
        ip.write_text(json.dumps(batch, indent=2, ensure_ascii=False))
        manifest.append({"batch": number, "n": len(batch),
                         "input": str(ip.relative_to(REPO)), "input_sha256": sha256(ip),
                         "output": str((SCREEN / f"verdict_{number:03d}.json").relative_to(REPO))})
    if len(assigned) != len(screenable) or set(assigned) != {r["paperId"] for r in screenable}:
        raise SystemExit("batch coverage invariant failed")
    if len(screenable) + len(title_only) != len(records):
        raise SystemExit("stratum split lost records")

    committed = {
        "slug": SLUG, "stage": "blinded_title_abstract_screen_input",
        "source": str(source.relative_to(REPO)), "source_sha256": sha256(source),
        "rubric_sha256": sha256(RUBRIC_PATH),
        "seed": SEED, "batch_size": BATCH_SIZE,
        "frame_records": len(records),
        "model_screened_records": len(screenable),
        "title_only_records_not_model_screened": len(title_only),
        "min_abstract_chars": MIN_ABSTRACT_CHARS,
        "batches": len(manifest),
        "coverage_note": (f"{len(title_only)} of {len(records)} frame records "
                          f"({100*len(title_only)/len(records):.0f}%) have no abstract and were assigned "
                          "UNCERTAIN / INSUFFICIENT_INFO by the rubric's title-only policy without a "
                          "model call. They remain in the corpus and in every denominator. Report this "
                          "wherever the screened count is quoted."),
        "d1_prerank": ("not run: the frame is entirely citation-sourced, so every record is an "
                       "orthogonal-channel record that D1's own rule exempts from its cutoff"),
        "blinded_fields": ["doi", "authors", "venue", "cited_by_count",
                           "discovery_channels", "seed_ids", "gold_status"],
        "coverage_verified": True, "manifest": manifest}
    (LOGS / f"{SLUG}-screen-manifest.json").write_text(json.dumps(committed, indent=2, ensure_ascii=False))
    print(f"frame {len(records)} = model-screened {len(screenable)} + title-only {len(title_only)}; "
          f"{len(manifest)} blinded batches of <= {BATCH_SIZE}; coverage verified")


if __name__ == "__main__":
    main()
