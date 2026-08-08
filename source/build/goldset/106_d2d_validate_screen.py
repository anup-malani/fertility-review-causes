#!/usr/bin/env python3
"""
106_d2d_validate_screen.py — D.2.d blinded title/abstract screen validator.

Fail-closed, mirroring `98_d1b_validate_screen.py`. The runner (step 107) imports `validate_batch` and
refuses to keep a batch that does not pass, so a malformed or truncated model response is never
written as a verdict.

Two hard-won rules are inherited rather than rediscovered, both from D.1.b:

  * **A verdict and a cell answer different questions.** The verdict says whether the paper belongs to
    D.2.d; the cell says where it DOES belong. `NOT_RELEVANT` + `OFF_QQ_C3d` is the correct disposition
    for a quantity-quality paper, not a contradiction — that pairing is how C.3.d receives it. D.1.b's
    first validator carried child-labor's "NOT_RELEVANT must use cell NA" rule, whose taxonomy had no
    sibling routers, and rejected 22 of 40 correct verdicts on batch 1. A fail-closed validator that is
    itself wrong does not merely miss errors, it manufactures them and discards good work.
  * **Reviews are allowed on primary cells.** A systematic review of the core estimand takes the
    matching PRIMARY cell with `evidence_type: review`; only theory and mechanism are excluded. This
    rubric says so explicitly at v1 (it was a D.3.b wave-1 defect), so a validator forbidding it would
    contradict the instrument it is enforcing.

D.2.d-specific consistency rules, each encoding a scope decision:

  * `ROUTING_DEFERRED_TO_FULLTEXT` and `MIXED_NORM_UNRESOLVED` pair ONLY with `UNCERTAIN`. These are
    the enforceability cells: four of the six walls cannot be adjudicated from an abstract, and a
    deferred routing call that carried `RELEVANT` or `NOT_RELEVANT` would assert exactly the judgement
    the cell exists to withhold.
  * The three theory/context cells take `RELEVANT` and cannot carry an empirical evidence type. They
    have no fertility estimand by definition and are separated downstream; they do not count toward
    empirical recall.
  * `FDT_SENTIMENTALIZATION_CONTEXT` cannot carry a non-NA outcome level. It is scope call 1: FDT
    material is context and is never pooled, so it must not acquire a poolable outcome level.

Direction of causation is NOT enforced as a schema error. The rubric prefers `UNCERTAIN` over a primary
cell when direction is unestablished, but a paper can legitimately report a primary estimate with
`direction_established: unclear`, and rejecting those would manufacture errors in exactly the way
described above. It is counted and surfaced for the wave-1 audit instead.

Usage:
  python3 106_d2d_validate_screen.py --audit          # report progress and errors, write nothing
  python3 106_d2d_validate_screen.py                  # fail-closed full check
"""
import argparse, hashlib, json, sys
from collections import Counter
from pathlib import Path

SLUG = "child-centeredness-intensive-parenting"
HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
LOGS = REPO / "literature" / "search-logs"

VERDICTS = {"RELEVANT", "UNCERTAIN", "NOT_RELEVANT"}
PRIMARY = {"PRIMARY_NORM_EXPOSURE", "PRIMARY_TIME_INTENSITY",
           "PRIMARY_PERCEIVED_STANDARD", "COST_INDEPENDENCE"}
THEORY = {"PARENTING_NORM_THEORY", "PARENTING_NORM_CONSTRUCT", "FDT_SENTIMENTALIZATION_CONTEXT"}
OFF = {"OFF_QQ_C3d", "OFF_INEQUALITY_C2f", "OFF_DIRECT_COST_C2b", "OFF_TIMECOST_C2e",
       "OFF_CHILDCARE_C2a", "OFF_GENDER_D2a", "OFF_OTHER", "OFF_OUTCOME"}
DEFERRED = {"ROUTING_DEFERRED_TO_FULLTEXT", "MIXED_NORM_UNRESOLVED", "INSUFFICIENT_INFO"}
ARGUMENT_CELLS = {"PARENTING_NORM_THEORY", "FDT_SENTIMENTALIZATION_CONTEXT"}
OTHER_CELLS = DEFERRED | {"REVERSE", "NA"}
CELLS = PRIMARY | THEORY | OFF | OTHER_CELLS
# Six cells are mixed-case (OFF_QQ_C3d, OFF_INEQUALITY_C2f, OFF_DIRECT_COST_C2b, OFF_TIMECOST_C2e,
# OFF_CHILDCARE_C2a, OFF_GENDER_D2a). Normalize case-INSENSITIVELY back to canonical spelling:
# uppercasing instead silently fails taxonomy validation and dumps every sibling-routed paper into NA.
# Inherited from D.3.b, where it was found the hard way.
CANON = {c.upper(): c for c in CELLS}

LEVELS = {"STATED_INTENTION_OR_ATTITUDE", "REALIZED_FERTILITY", "BOTH", "NA"}
MEASURES = {"attitude scale", "time use", "perceived standard", "policy/media exposure",
            "inferred, not measured", "n/a"}
DIRECTION = {"yes", "no", "unclear"}
EVIDENCE = {"quasi-experimental", "observational", "structural", "theory", "review",
            "qualitative", "mechanism", "other"}
EMPIRICAL_EV = {"quasi-experimental", "observational", "structural", "qualitative"}
REQUIRED = {"paperId", "verdict", "estimand_cell", "outcome_level", "norm_measure",
            "variation_source", "treatment", "outcome", "direction_established",
            "evidence_type", "reason"}


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate_record(record, expected_id, loc):
    errors = []
    if not isinstance(record, dict):
        return [f"{loc}: verdict must be an object"], None
    missing = sorted(REQUIRED - set(record))
    if missing:
        return [f"{loc}: missing fields {missing}"], None
    if record.get("paperId") != expected_id:
        errors.append(f"{loc}: paperId/order mismatch: expected {expected_id!r}, "
                      f"got {record.get('paperId')!r}")
    verdict = str(record.get("verdict", "")).upper()
    cell = CANON.get(str(record.get("estimand_cell", "")).upper(), record.get("estimand_cell"))
    level = str(record.get("outcome_level", "")).upper()
    ev = record.get("evidence_type")
    direction = record.get("direction_established")

    if verdict not in VERDICTS:
        errors.append(f"{loc}: invalid verdict {verdict!r}")
    if cell not in CELLS:
        errors.append(f"{loc}: invalid estimand_cell {record.get('estimand_cell')!r}")
    if level not in LEVELS:
        errors.append(f"{loc}: invalid outcome_level {record.get('outcome_level')!r}")
    if str(record.get("norm_measure", "")).lower() not in MEASURES:
        errors.append(f"{loc}: invalid norm_measure {record.get('norm_measure')!r}")
    if direction not in DIRECTION:
        errors.append(f"{loc}: invalid direction_established {direction!r}")
    if ev not in EVIDENCE:
        errors.append(f"{loc}: invalid evidence_type {ev!r}")

    # --- consistency rules, each one a scope decision ---
    if cell == "NA" and verdict != "NOT_RELEVANT":
        errors.append(f"{loc}: cell NA pairs only with NOT_RELEVANT")
    if verdict == "NOT_RELEVANT" and cell not in (OFF | {"NA", "REVERSE"}):
        errors.append(f"{loc}: NOT_RELEVANT must carry an OFF_* routing cell, REVERSE, or NA "
                      f"(got {cell!r})")
    if verdict == "RELEVANT" and cell in OFF:
        errors.append(f"{loc}: an OFF_* cell means the paper belongs to a sibling chapter; "
                      "its verdict here is NOT_RELEVANT")
    if cell in DEFERRED and verdict != "UNCERTAIN":
        errors.append(f"{loc}: {cell} pairs only with UNCERTAIN — it exists to withhold exactly the "
                      "judgement a RELEVANT/NOT_RELEVANT verdict would assert")
    if cell in PRIMARY and level == "NA":
        errors.append(f"{loc}: a primary cell requires a non-NA outcome_level")
    if cell in PRIMARY and ev in {"theory", "mechanism"}:
        errors.append(f"{loc}: primary cell requires an empirical estimate (reviews ARE allowed)")
    # WAVE-1 FIX (2026-08-08). Two rules here were wrong and the gate caught both on batch 1.
    #
    # (a) The no-empirical-evidence rule applied to all three THEORY cells, but
    #     PARENTING_NORM_CONSTRUCT is DEFINED in the rubric as "prevalence, trends, class gradients"
    #     — observational empirical work by construction. Batch 1 record 20 (parenting intensity by
    #     race/ethnicity, no fertility outcome) is a correct PARENTING_NORM_CONSTRUCT + observational
    #     call that this rule rejected. The constraint belongs only on the two argumentative cells.
    if cell in ARGUMENT_CELLS and ev in {"quasi-experimental", "observational"}:
        errors.append(f"{loc}: {cell} is an argument, not an estimate; it cannot carry {ev} "
                      "(PARENTING_NORM_CONSTRUCT is the cell for measured norms)")
    # (b) Forcing RELEVANT on theory cells compels a screener who cannot tell whether a theory paper
    #     belongs to assert that it does. Batch 1 record 7 took UNCERTAIN because norm-vs-investment
    #     content was not separable in the abstract — the honest answer. UNCERTAIN is now allowed;
    #     NOT_RELEVANT still is not, because a theory paper that does not belong takes an OFF_* cell.
    if cell in THEORY and verdict == "NOT_RELEVANT":
        errors.append(f"{loc}: a theory/context paper that does not belong takes an OFF_* cell, "
                      "not NOT_RELEVANT with a theory cell")
    if cell == "FDT_SENTIMENTALIZATION_CONTEXT" and level != "NA":
        errors.append(f"{loc}: FDT context is never pooled (scope call 1); outcome_level must be NA")
    for field in ("treatment", "outcome", "reason"):
        if not str(record.get(field) or "").strip():
            errors.append(f"{loc}: {field} must be non-empty")

    # Soft signal for the wave-1 audit, deliberately NOT an error. See module docstring.
    soft = None
    if cell in PRIMARY and direction != "yes":
        soft = "primary_cell_direction_not_established"
    return errors, soft


def validate_batch(batch_path, verdict_payload):
    """Used by the runner (step 107) to decide whether to keep a model response.

    `verdict_payload` may be a parsed JSON array (the runner's case, checked BEFORE anything is
    written to disk) or a path to a verdict file (this module's own --audit case). Returns
    (errors, normalized_records, soft_flags). Normalization canonicalizes cell spelling and
    upper-cases the enum fields, so downstream steps never see case variants.
    """
    batch = json.loads(Path(batch_path).read_text())
    if isinstance(verdict_payload, (str, Path)):
        try:
            verdict_payload = json.loads(Path(verdict_payload).read_text())
        except Exception as e:
            return [f"{verdict_payload}: unreadable ({e})"], [], []
    if not isinstance(verdict_payload, list):
        return [f"{batch_path}: response must be a JSON array"], [], []
    if len(verdict_payload) != len(batch):
        return [f"{batch_path}: expected {len(batch)} verdicts, got {len(verdict_payload)}"], [], []
    errors, out, softs = [], [], []
    for i, (row, rec) in enumerate(zip(batch, verdict_payload)):
        errs, soft = validate_record(rec, row["paperId"], f"{Path(batch_path).name}[{i}]")
        errors.extend(errs)
        if soft:
            softs.append(soft)
        if not errs:
            rec = dict(rec)
            rec["estimand_cell"] = CANON.get(str(rec["estimand_cell"]).upper(), rec["estimand_cell"])
            rec["verdict"] = str(rec["verdict"]).upper()
            rec["outcome_level"] = str(rec["outcome_level"]).upper()
            out.append(rec)
    return errors, out, softs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--audit", action="store_true")
    args = ap.parse_args()
    man = json.loads((LOGS / f"{SLUG}-screen-manifest.json").read_text())
    done, missing, all_errors, all_softs, cells, verdicts_c = 0, [], [], [], Counter(), Counter()
    for entry in man["manifest"]:
        vp = REPO / entry["output"]
        if not vp.exists():
            missing.append(entry["batch"]); continue
        errs, _norm, softs = validate_batch(REPO / entry["input"], vp)
        all_errors.extend(errs); all_softs.extend(softs)
        if not errs:
            done += 1
            for r in json.loads(vp.read_text()):
                cells[CANON.get(str(r.get("estimand_cell", "")).upper(), r.get("estimand_cell"))] += 1
                verdicts_c[str(r.get("verdict", "")).upper()] += 1
    print(f"batches: {len(man['manifest'])} | valid verdicts: {done} | missing: {len(missing)}")
    if verdicts_c:
        print("verdicts:", dict(verdicts_c))
        print("cells:", dict(cells.most_common()))
    if all_softs:
        print(f"soft flags (not errors): {dict(Counter(all_softs))}")
    if all_errors:
        print(f"\n{len(all_errors)} ERRORS:")
        for e in all_errors[:40]:
            print("  -", e)
    if args.audit:
        return
    if all_errors or missing:
        sys.exit(f"FAIL-CLOSED: {len(all_errors)} errors, {len(missing)} batches missing")
    print("all batches present and valid")


if __name__ == "__main__":
    main()
