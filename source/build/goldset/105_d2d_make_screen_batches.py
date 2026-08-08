#!/usr/bin/env python3
"""
105_d2d_make_screen_batches.py — D.2.d (child-centered intensive parenting), stage A5 input.

Prepare the Tier-B frame for blinded title/abstract LLM screening. Mirror of
`97_d1b_make_screen_batches.py`, including both of its departures from D.3.b, which apply here for the
same reasons:

DEPARTURE 1 — abstract-bearing records are screened; title-only records are NOT.
  A record with no abstract that does not state its estimand verbatim in the title CANNOT be routed,
  and the rubric says so. Sending it to a model buys a verdict the policy already determines. The
  title-only records are written to their own file, pre-assigned UNCERTAIN / INSUFFICIENT_INFO by the
  rubric's own rule, and carried into the corpus rather than dropped. They remain in every denominator.

  **This is a deliberate coverage limit and it is reported as one.** The screen report must state how
  many frame records were never model-screened, because a reader who sees a screened count against a
  larger frame is entitled to know which is the denominator. If the RA gate later finds primary-cell
  papers hiding in the title-only stratum, the fix is to resolve abstracts for that stratum and screen
  it, not to leave the gap unstated.

DEPARTURE 2 — no D1 deterministic pre-rank. GACS D1 orders records by term-match score and applies a
  budget cutoff *within the keyword channel only*, so orthogonally-discovered papers bypass it. This
  frame is entirely citation-sourced: every record arrived by backward reference or forward citation,
  so every record is an orthogonal-channel record and would bypass a D1 cutoff by the rule's own logic.
  Recorded so its absence reads as a decision rather than an omission.

BATCH_SIZE = 25, not D.3.b's 40, inherited from D.1.b: at 40 its runner's first live batch returned 39
  of 40 verdicts, because a rubric demanding eleven fields per record pushes a 40-record response long
  enough to drop the tail. This rubric also demands eleven fields, so the same limit applies. The
  validator would catch it — that is what fail-closed is for — but rediscovering it costs a run.

WAVE GATING. This script writes all batches; it does not run them. Per D.3.b's wave-1 audit, run the
  first five batches ONLY, audit the verdicts for rubric defects, and do not spend the remainder until
  that audit passes. D.3.b's wave 1 found four cell-level defects across 200 records and five
  screeners; three of those are already fixed in this rubric at v1, which is a reason to expect a
  cleaner wave 1, not a reason to skip it.

The rubric is NOT duplicated into this script. The A1 rubric file is the single source of truth and
this script only copies it into the batch directory — embedding it as a string constant would make the
script the source of truth and silently overwrite later edits to the committed rubric.

Blinding is the point of the stage: records are deterministically shuffled and stripped of DOI,
authors, venue, citation count, discovery channel, seed provenance, and gold status, so a screener
cannot infer a verdict from where a paper came from. That matters more here than on earlier chapters,
because 41% of this frame is decoy-seeded and a screener who could see seed provenance would have a
standing hint to route those records away.

Inputs : literature/search-logs/{slug}-tier-b-frame.json
         literature/search-logs/{slug}-screen-rubric.md   (single source of truth, written at A1)
Outputs: temp/screen/{slug}/batch_NNN.json, RUBRIC.md
         literature/search-logs/{slug}-screen-manifest.json
         literature/search-logs/{slug}-title-only-stratum.json
"""
import hashlib, json, random
from pathlib import Path

SLUG = "child-centeredness-intensive-parenting"
SEED = 1064  # D.2.d — TICK-064
BATCH_SIZE = 25
MIN_ABSTRACT_CHARS = 30   # same threshold the A4 frame log uses for "usable abstract"
HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
LOGS = REPO / "literature" / "search-logs"
SCREEN = REPO / "temp" / "screen" / SLUG
SCREEN.mkdir(parents=True, exist_ok=True)
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

    # The title-only stratum, pre-assigned by the rubric's own title-only rule. Carried into the
    # corpus, counted in every denominator, and NOT sent to a model. Field set matches the D.2.d
    # rubric's output contract so this stratum concatenates with model verdicts without reshaping.
    (LOGS / f"{SLUG}-title-only-stratum.json").write_text(json.dumps(
        [{"paperId": r["paperId"], "title": r.get("title") or "", "year": r.get("year"),
          "verdict": "UNCERTAIN", "estimand_cell": "INSUFFICIENT_INFO", "outcome_level": "NA",
          "norm_measure": "n/a", "variation_source": "not stated",
          "treatment": "n/a", "outcome": "n/a", "direction_established": "unclear",
          "evidence_type": "other",
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
        "wave_gate": ("Run batches 1-5 only, then audit before spending the remainder. D.3.b's wave-1 "
                      "audit found four cell-level defects across 200 records; three are pre-fixed in "
                      "this rubric at v1."),
        "d1_prerank": ("not run: the frame is entirely citation-sourced, so every record is an "
                       "orthogonal-channel record that D1's own rule exempts from its cutoff"),
        "blinded_fields": ["doi", "authors", "venue", "cited_by_count",
                           "discovery_channels", "seed_ids", "gold_status"],
        "coverage_verified": True, "manifest": manifest}
    (LOGS / f"{SLUG}-screen-manifest.json").write_text(json.dumps(committed, indent=2, ensure_ascii=False))
    print(f"frame {len(records)} = model-screened {len(screenable)} + title-only {len(title_only)}; "
          f"{len(manifest)} blinded batches of <= {BATCH_SIZE}; coverage verified")
    print(f"WAVE GATE: run batches 1-5 ({min(5,len(manifest))*BATCH_SIZE} records) and audit before "
          f"spending the other {max(0,len(manifest)-5)} batches.")


if __name__ == "__main__":
    main()
