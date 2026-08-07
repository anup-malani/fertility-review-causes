#!/usr/bin/env python3
"""
98_d1b_validate_screen.py — D.1.b blinded title/abstract screen validator.

Fail-closed by design, mirroring `59_child_labor_validate_screen.py`. Every manifest batch and every
verdict must be present and valid before anything downstream treats the screen as complete. The runner
(step 99) imports `validate_batch` and refuses to keep a batch that does not pass, so a malformed or
truncated model response is never written as a verdict.

The consistency rules below are not cosmetic. Each one encodes a frozen decision from the A1 scope, and
each is a rule the screen would otherwise be free to violate silently:

  * NOT_RELEVANT <-> NA is the invariant that keeps the cell counts interpretable.
  * INSUFFICIENT_INFO and MECHANISM_UNRESOLVED_SCHOOLING may pair ONLY with UNCERTAIN. The second is
    scope call 2: a reduced-form schooling estimate that decomposes no mechanism is not evidence for
    this chapter, and letting it carry a RELEVANT verdict would put it one careless join away from the
    pooling set.
  * A primary cell requires a non-NA outcome level and an empirical evidence type. Both walls exist
    because the chapter's outcome levels are never pooled together and its pool is never theory.
  * HISTORICAL_WESTERN_FDT forces OFF_OTHER. That is scope call 1: the historical Western transition is
    the source of the diffused package, not a case of it.
  * shared_with A.20 is allowed ONLY on the media cell, because the dual-home rule is confined to Wall 3.

Usage:
  python3 98_d1b_validate_screen.py --audit          # report progress and errors, write nothing
  python3 98_d1b_validate_screen.py                  # fail-closed full check
"""
import argparse, hashlib, json, sys
from collections import Counter
from pathlib import Path

SLUG = "caldwell-wealth-flows-westernization"
HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
LOGS = REPO / "literature" / "search-logs"

VERDICTS = {"RELEVANT", "UNCERTAIN", "NOT_RELEVANT"}
PRIMARY = {"PRIMARY_DI_BELIEF", "PRIMARY_SCHOOLING_IDEATIONAL",
           "PRIMARY_MEDIA_WESTERN_MODEL", "PRIMARY_WESTERN_CONTACT",
           "DIFFUSION_INDEPENDENT_OF_STRUCTURE"}
THEORY = {"DI_THEORY"}
OFF = {"OFF_WEALTH_FLOWS_C3f", "OFF_POSTMATERIALIST_D1a", "OFF_DIFFUSION_CHANNEL_A20",
       "OFF_FERTILITY_CONTROL_A3", "OFF_FEMALE_AUTONOMY_D2a", "OFF_SCHOOLING_ECONOMIC",
       "OFF_CULTURAL_EVOLUTION_D1c", "OFF_OTHER", "OFF_OUTCOME"}
OTHER_CELLS = {"MECHANISM_UNRESOLVED_SCHOOLING", "REVERSE", "INSUFFICIENT_INFO", "NA"}
CELLS = PRIMARY | THEORY | OFF | OTHER_CELLS
# Three cells are mixed-case (OFF_WEALTH_FLOWS_C3f, OFF_POSTMATERIALIST_D1a, OFF_CULTURAL_EVOLUTION_D1c).
# Normalize case-INSENSITIVELY back to canonical spelling: uppercasing instead silently fails taxonomy
# validation and dumps every sibling-routed paper into NA. This bug is inherited from D.3.b, where it
# was found the hard way; the comment is kept so the next chapter does not rediscover it.
CANON = {c.upper(): c for c in CELLS}

LEVELS = {"REALIZED_FERTILITY", "STATED_INTENTION_OR_IDEAL", "FAMILY_FORMATION_BEHAVIOUR",
          "MULTIPLE", "NA"}
ERAS = {"DIFFUSED_FDT", "SDT", "HISTORICAL_WESTERN_FDT", "NA"}
HELD = {"yes", "no", "unclear"}
SHARED = {"A.20", "none"}
EVIDENCE = {"quasi-experimental", "observational", "structural", "theory", "review", "mechanism", "other"}
NON_EMPIRICAL = {"theory", "review", "mechanism"}
REQUIRED = {"paperId", "verdict", "estimand_cell", "outcome_level", "shared_with", "treatment",
            "outcome", "structural_change_held_fixed", "setting_era", "evidence_type", "reason"}


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate_record(record, expected_id, loc):
    errors = []
    if not isinstance(record, dict):
        return [f"{loc}: verdict must be an object"]
    missing = sorted(REQUIRED - set(record))
    if missing:
        errors.append(f"{loc}: missing fields {missing}")
        return errors
    if record.get("paperId") != expected_id:
        errors.append(f"{loc}: paperId/order mismatch: expected {expected_id!r}, got {record.get('paperId')!r}")
    verdict = str(record.get("verdict", "")).upper()
    cell = CANON.get(str(record.get("estimand_cell", "")).upper(), record.get("estimand_cell"))
    level = str(record.get("outcome_level", "")).upper()
    era = str(record.get("setting_era", "")).upper()
    ev = record.get("evidence_type")

    if verdict not in VERDICTS:
        errors.append(f"{loc}: invalid verdict {verdict!r}")
    if cell not in CELLS:
        errors.append(f"{loc}: invalid estimand_cell {record.get('estimand_cell')!r}")
    if level not in LEVELS:
        errors.append(f"{loc}: invalid outcome_level {record.get('outcome_level')!r}")
    if era not in ERAS:
        errors.append(f"{loc}: invalid setting_era {record.get('setting_era')!r}")
    if record.get("structural_change_held_fixed") not in HELD:
        errors.append(f"{loc}: invalid structural_change_held_fixed {record.get('structural_change_held_fixed')!r}")
    if record.get("shared_with") not in SHARED:
        errors.append(f"{loc}: invalid shared_with {record.get('shared_with')!r}")
    if ev not in EVIDENCE:
        errors.append(f"{loc}: invalid evidence_type {ev!r}")

    # --- consistency rules, each one a frozen scope decision ---
    # A verdict and a cell answer different questions. The verdict says whether the paper belongs to
    # D.1.b; the cell says where it DOES belong. So NOT_RELEVANT + OFF_WEALTH_FLOWS_C3f is the correct
    # disposition for a wealth-flows paper, not a contradiction — that pairing is how the sibling
    # chapter receives it.
    #
    # The first version of this validator carried child-labor's rule, "NOT_RELEVANT must use cell NA",
    # whose taxonomy had no sibling routers. On batch 1 it rejected 22 of 40 correct verdicts. The
    # model was right and the validator was wrong, which is the failure mode a fail-closed validator
    # makes expensive: it does not merely miss errors, it manufactures them and discards good work.
    if cell == "NA" and verdict != "NOT_RELEVANT":
        errors.append(f"{loc}: cell NA pairs only with NOT_RELEVANT")
    if verdict == "NOT_RELEVANT" and cell not in (OFF | {"NA", "REVERSE"}):
        errors.append(f"{loc}: NOT_RELEVANT must carry an OFF_* routing cell, REVERSE, or NA "
                      f"(got {cell!r})")
    if verdict == "RELEVANT" and cell in OFF:
        errors.append(f"{loc}: an OFF_* cell means the paper belongs to a sibling chapter; "
                      "its verdict here is NOT_RELEVANT")
    if cell in {"INSUFFICIENT_INFO", "MECHANISM_UNRESOLVED_SCHOOLING"} and verdict != "UNCERTAIN":
        errors.append(f"{loc}: {cell} pairs only with UNCERTAIN (scope call 2 for the schooling cell)")
    if cell in PRIMARY and level == "NA":
        errors.append(f"{loc}: a primary cell requires a non-NA outcome_level")
    if cell in PRIMARY and ev in NON_EMPIRICAL and ev != "review":
        errors.append(f"{loc}: primary cell requires an empirical estimate (reviews allowed, rule 5)")
    # The real constraint on the theory cell is that it is NOT an empirical estimate — not that it
    # carries one of three particular labels. Ethnographic and conceptual pieces legitimately come
    # back as "mechanism" or "other", and rejecting those (as the first version did, on batch 5)
    # forces the screener to choose between a wrong cell and a wrong evidence type.
    if cell in THEORY and ev in {"quasi-experimental", "observational"}:
        errors.append(f"{loc}: DI_THEORY cannot carry an empirical evidence_type ({ev})")
    if era == "HISTORICAL_WESTERN_FDT" and cell != "OFF_OTHER":
        errors.append(f"{loc}: HISTORICAL_WESTERN_FDT routes to OFF_OTHER (scope call 1)")
    if record.get("shared_with") == "A.20" and cell != "PRIMARY_MEDIA_WESTERN_MODEL":
        errors.append(f"{loc}: shared_with A.20 is confined to the media cell (Wall 3)")
    if cell in PRIMARY and era == "NA":
        errors.append(f"{loc}: a primary cell requires a setting_era (rule 7)")
    for field in ("treatment", "outcome", "reason"):
        if not isinstance(record.get(field), str) or not record.get(field, "").strip():
            errors.append(f"{loc}: {field} must be a nonblank string")
    return errors


def validate_batch(batch_path, verdict_payload):
    """Used by the runner (step 99) to decide whether to keep a model response.
    Returns (errors, normalized_records)."""
    batch = json.loads(Path(batch_path).read_text())
    if not isinstance(verdict_payload, list):
        return [f"{batch_path}: response must be a JSON array"], []
    if len(verdict_payload) != len(batch):
        return [f"{batch_path}: expected {len(batch)} verdicts, got {len(verdict_payload)}"], []
    errors, out = [], []
    for i, (row, rec) in enumerate(zip(batch, verdict_payload)):
        errs = validate_record(rec, row["paperId"], f"{Path(batch_path).name}[{i}]")
        errors.extend(errs)
        if not errs:
            rec = dict(rec)
            rec["estimand_cell"] = CANON.get(str(rec["estimand_cell"]).upper(), rec["estimand_cell"])
            rec["verdict"] = str(rec["verdict"]).upper()
            rec["outcome_level"] = str(rec["outcome_level"]).upper()
            rec["setting_era"] = str(rec["setting_era"]).upper()
            out.append(rec)
    return errors, out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--audit", action="store_true", help="report status and errors; exit 0 while incomplete")
    args = ap.parse_args()

    manifest = json.loads((LOGS / f"{SLUG}-screen-manifest.json").read_text())
    src = REPO / manifest["source"]
    errors, present, cells, verdicts, missing = [], 0, Counter(), Counter(), []
    if sha256(src) != manifest["source_sha256"]:
        errors.append("citation-frame checksum differs from the screen manifest")
    if sha256(LOGS / f"{SLUG}-screen-rubric.md") != manifest["rubric_sha256"]:
        errors.append("rubric checksum differs from the screen manifest: batches were cut against "
                      "a different rubric than the one now on disk")

    for entry in manifest["manifest"]:
        vp = REPO / entry["output"]
        if not vp.exists():
            missing.append(entry["batch"]); continue
        try:
            payload = json.loads(vp.read_text())
        except json.JSONDecodeError as e:
            errors.append(f"batch {entry['batch']}: unparseable verdict file ({e})"); continue
        errs, ok = validate_batch(REPO / entry["input"], payload)
        errors.extend(errs)
        present += 1
        for r in ok:
            cells[r["estimand_cell"]] += 1
            verdicts[r["verdict"]] += 1

    total = manifest["batches"]
    print(f"batches {present}/{total} present; missing {len(missing)}; errors {len(errors)}")
    if verdicts:
        print("verdicts:", dict(verdicts.most_common()))
        print("cells:", dict(cells.most_common()))
    for e in errors[:25]:
        print("  ERR", e)
    if missing[:12]:
        print("  missing batches:", missing[:12], "..." if len(missing) > 12 else "")
    if args.audit:
        return 0
    if missing or errors:
        print("FAIL-CLOSED: screen is not complete and valid", file=sys.stderr)
        return 1
    print("screen complete and valid")
    return 0


if __name__ == "__main__":
    sys.exit(main())
