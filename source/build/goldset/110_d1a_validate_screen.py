#!/usr/bin/env python3
r"""
110_d1a_validate_screen.py — D.1.a. Validate screen verdicts, and score the calibration batches.

Two jobs, deliberately in one place so a verdict file can never be accepted by one standard and
scored by another.

(1) VALIDATION — fail-closed. Every verdict file must cover exactly its batch's paperIds, in order,
    with every required field present and every enumerated field inside its allowed set. The allowed
    estimand cells are PARSED FROM THE COMMITTED RUBRIC rather than restated here, so a cell renamed
    in the rubric cannot silently pass validation against a stale copy in a script.

(2) CALIBRATION SCORING — against `{slug}-screen-calibration-key.json`, which the screen never sees.

WHAT THE CALIBRATION ACTUALLY TESTS, AND WHAT IT CANNOT.

The decisive check is the DECOYS. Ten Tier-A anchors sit exactly on the boundaries the rubric says
will be tested -- gender-role attitudes (D.2.a), mass-media exposure (D.1.b / A.20), and religion
against *contraceptive use* rather than fertility (OFF_OUTCOME). Each must route AWAY. A screen that
admits them is mis-calibrated in the direction that costs the chapter, and finding that out costs two
batches instead of three hundred and ninety.

It CANNOT test whether `RELEVANT` verdicts are correct in the way the chapter finally needs, because
three of the scope's routing tests turn on the treatment instrument's item content, which titles and
abstracts do not state. The rubric binds those to `UNCERTAIN` + `needs_full_text`. So a high
UNCERTAIN rate on the empirical anchors is COMPLIANCE, not failure, and this script reports it as
such rather than scoring it as an error. Scoring it as an error would push a screener toward exactly
the confident-verdict-without-basis failure D.3.b already committed.

Usage:
  python3 110_d1a_validate_screen.py --calib          # validate + score the calibration batches
  python3 110_d1a_validate_screen.py --all            # validate every verdict file present
Output: literature/search-logs/{slug}-screen-calibration-report.md   (with --calib)
"""
import json, re, sys
from collections import Counter
from pathlib import Path

SLUG = "postmaterialism-individualism-secularization"
HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
LOGS = REPO / "literature" / "search-logs"
SCREEN = REPO / "temp" / "screen" / SLUG
OUT_MD = LOGS / f"{SLUG}-screen-calibration-report.md"

VERDICTS = {"RELEVANT", "UNCERTAIN", "NOT_RELEVANT"}
PAIRS = {"S1", "S2", "S3", "S4", "S5", "MULTIPLE", "NA"}
YES_NO = {"yes", "no", "unclear"}
EVIDENCE = {"quasi-experimental", "observational", "structural", "theory", "review",
            "descriptive", "other"}
TIERS = {"1", "2", "3", "4", "unclear"}
REQUIRED = ["paperId", "verdict", "estimand_cell", "pair", "treatment", "outcome",
            "outcome_is_fertility", "treatment_is_measured_value", "evidence_type",
            "design_tier_guess", "needs_full_text", "reason"]


def allowed_cells():
    """Parse the cell names out of the committed rubric's tables.

    Restating them in this file would create a second source of truth that drifts the moment the
    rubric is edited -- and the rubric is the artifact under version control that a reader will
    check against.
    """
    txt = (LOGS / f"{SLUG}-screen-rubric.md").read_text()
    # LOWERCASE IS REQUIRED IN THE CHARACTER CLASS. The first version matched `[A-Z][A-Z0-9_]+`,
    # which silently dropped every cell carrying a chapter suffix -- OFF_EXPOSURE_D1b,
    # OFF_STATUS_D1c, OFF_GENDER_D2a, OFF_PARTNERSHIP_D2b, OFF_PARENTING_D2d,
    # OFF_ECOLOGICAL_FEAR_D3b -- because of the lowercase letter. Those are precisely the cells the
    # decoys must route to, so a screener answering CORRECTLY would have been failed as invalid.
    # The staleness guard below passed at 20 cells while six were missing, which is why it now
    # checks a named sample rather than a count.
    cells = set(re.findall(r"^\|\s*`([A-Z][A-Za-z0-9_]+)`\s*\|", txt, re.M))
    must = {"PRIMARY_SECULAR_S3", "OFF_GENDER_D2a", "OFF_EXPOSURE_D1b", "OFF_OUTCOME",
            "INSUFFICIENT_INFO", "REVERSE"}
    if not must <= cells:
        raise SystemExit(f"rubric parse is stale -- missing {sorted(must - cells)}")
    return cells


def validate_payload(rows, batch, cells, label):
    """Validate an IN-MEMORY payload against its batch. Shared with the runner so that nothing is
    ever written to disk before it has passed the same checks a re-read would apply."""
    errs = []
    if not isinstance(rows, list):
        return [f"{label}: top level must be a JSON array"]
    want = [r["paperId"] for r in batch]
    got = [r.get("paperId") for r in rows if isinstance(r, dict)]
    if got != want:
        missing, extra = set(want) - set(got), set(got) - set(want)
        # NAME THEM. The first live failure reported only "missing=1, extra=1", which is unactionable
        # -- the batch was discarded and nothing said which id had been mangled. With the ids named
        # it was immediately obvious that the screener was mis-transcribing 44-character hex strings,
        # which is what motivated the short positional ids.
        detail = ""
        if missing or extra:
            detail = (f"; missing={sorted(missing)[:5]} extra={sorted(extra)[:5]}")
        elif len(got) == len(want):
            first = next((i for i, (a, b) in enumerate(zip(got, want)) if a != b), None)
            detail = f"; same ids, wrong order (first at index {first})"
        errs.append(f"{label}: id mismatch (n={len(got)} vs {len(want)}{detail})")
    for i, r in enumerate(rows):
        if not isinstance(r, dict):
            errs.append(f"{label}[{i}]: not an object"); continue
        loc = f"{label}[{i}] {r.get('paperId')}"
        for f in REQUIRED:
            if f not in r:
                errs.append(f"{loc}: missing field '{f}'")
        if r.get("verdict") not in VERDICTS:
            errs.append(f"{loc}: verdict {r.get('verdict')!r}")
        if r.get("estimand_cell") not in cells:
            errs.append(f"{loc}: estimand_cell {r.get('estimand_cell')!r}")
        if r.get("pair") not in PAIRS:
            errs.append(f"{loc}: pair {r.get('pair')!r}")
        for f in ("outcome_is_fertility", "treatment_is_measured_value"):
            if str(r.get(f)).lower() not in YES_NO:
                errs.append(f"{loc}: {f} {r.get(f)!r}")
        if r.get("evidence_type") not in EVIDENCE:
            errs.append(f"{loc}: evidence_type {r.get('evidence_type')!r}")
        if str(r.get("design_tier_guess")) not in TIERS:
            errs.append(f"{loc}: design_tier_guess {r.get('design_tier_guess')!r}")
        # The rubric's own consistency rules, enforced rather than trusted.
        if r.get("verdict") == "UNCERTAIN" and not str(r.get("needs_full_text") or "").strip():
            errs.append(f"{loc}: UNCERTAIN with empty needs_full_text")
        if r.get("estimand_cell") == "INSUFFICIENT_INFO" and r.get("verdict") != "UNCERTAIN":
            errs.append(f"{loc}: INSUFFICIENT_INFO pairs only with UNCERTAIN")
        # THE VERDICT MUST AGREE WITH THE SCREEN'S OWN ROUTING ANSWERS.
        # The rubric defines RELEVANT as precisely "the regressor is a measured value orientation of
        # D.1.a content AND the dependent variable is fertility" -- which is exactly what the two
        # routing fields record. Recording them separately was meant to let a disagreement be traced
        # to which question was answered wrong; it also makes the verdict checkable for free.
        # It is not hypothetical: the first clean calibration produced 3 of 22 RELEVANT verdicts
        # that contradicted their own answers, including a decoy marked RELEVANT with
        # `outcome_is_fertility: no` and cell VALUE_CONSTRUCT, whose definition is that the value
        # measure IS the dependent variable. Enforcing the rubric's own definition catches that
        # class without anyone reading a single title.
        if r.get("verdict") == "RELEVANT" and not (
                str(r.get("outcome_is_fertility")).lower() == "yes"
                and str(r.get("treatment_is_measured_value")).lower() == "yes"):
            errs.append(f"{loc}: RELEVANT contradicts its own routing answers "
                        f"(outcome_is_fertility={r.get('outcome_is_fertility')!r}, "
                        f"treatment_is_measured_value={r.get('treatment_is_measured_value')!r})")
    return errs


def validate_file(batch_path, verdict_path, cells):
    """Return (rows, errors). Errors are fatal; a partially valid file is not usable."""
    batch = json.loads(batch_path.read_text())
    try:
        rows = json.loads(verdict_path.read_text())
    except Exception as e:
        return [], [f"{verdict_path.name}: unparseable ({e})"]
    return rows, validate_payload(rows, batch, cells, verdict_path.name)


def main():
    cells = allowed_cells()
    man = json.loads((LOGS / f"{SLUG}-screen-manifest.json").read_text())
    kind = "calib" if "--calib" in sys.argv else None
    entries = [m for m in man["manifest"] if kind is None or m["kind"] == kind]

    rows, errs, present = [], [], 0
    for m in entries:
        vp = REPO / m["output"]
        if not vp.exists():
            continue
        present += 1
        r, e = validate_file(REPO / m["input"], vp, cells)
        rows += r; errs += e

    if present == 0:
        print(f"no verdict files present for {kind or 'any'} batches yet.\n"
              f"expected e.g. {entries[0]['output']}", file=sys.stderr)
        sys.exit(3)
    print(f"{present}/{len(entries)} verdict files present, {len(rows)} verdicts, "
          f"{len(errs)} validation errors", file=sys.stderr)
    for e in errs[:25]:
        print("  " + e, file=sys.stderr)
    if errs:
        print("VALIDATION FAILED -- verdicts not usable", file=sys.stderr)
        sys.exit(1)
    if "--calib" not in sys.argv:
        return

    # ---- calibration scoring -----------------------------------------------------------------
    key = {k["paperId"]: k for k in
           json.loads((LOGS / f"{SLUG}-screen-calibration-key.json").read_text())}
    by_id = {r["paperId"]: r for r in rows}
    decoys = [k for k in key.values() if k["expect_route_away"]]
    dec_ok, dec_bad = [], []
    for k in decoys:
        v = by_id.get(k["paperId"])
        if not v:
            continue
        if v["verdict"] == "RELEVANT":
            dec_bad.append((k, v))
        else:
            dec_ok.append((k, v))

    emp = [k for k in key.values() if k["role"] == "EMPIRICAL"]
    emp_v = Counter(by_id[k["paperId"]]["verdict"] for k in emp if k["paperId"] in by_id)
    emp_rejected = [(k, by_id[k["paperId"]]) for k in emp
                    if k["paperId"] in by_id and by_id[k["paperId"]]["verdict"] == "NOT_RELEVANT"]
    pair_ok = sum(1 for k in emp if k["paperId"] in by_id
                  and by_id[k["paperId"]]["pair"] == k["pair"])
    pair_n = sum(1 for k in emp if k["paperId"] in by_id and k["pair"] in PAIRS)

    L = ["# D.1.a — screen calibration against the pre-labelled Tier-A anchors", "",
         "48 hand-built anchors with known `role`, `pair` and `design_tier`, blinded and shuffled "
         "into the same batch format as production. The screen never sees the key.", "",
         f"- verdicts scored: **{len(rows)}**", "",
         "## The decisive check — do the 10 decoys route away?", "",
         "These sit exactly on the boundaries the rubric says will be tested: gender-role attitudes "
         "(D.2.a), mass-media exposure (D.1.b / A.20), and religion against *contraceptive use* "
         "rather than fertility (`OFF_OUTCOME`). **Each must NOT be `RELEVANT`.**", "",
         f"- routed away correctly: **{len(dec_ok)}/{len(decoys)}**",
         f"- **admitted as RELEVANT (failures): {len(dec_bad)}**", ""]
    if dec_bad:
        L += ["| decoy | verdict | cell | reason |", "|---|---|---|---|"]
        L += [f"| {k['title'][:70]} | {v['verdict']} | `{v['estimand_cell']}` | "
              f"{str(v.get('reason'))[:80]} |" for k, v in dec_bad]
        L += ["", "> **A decoy admitted as RELEVANT is a mis-calibration in the direction that "
              "costs the chapter.** Fix the rubric or the screener before authorising production.", ""]
    else:
        L += ["> All decoys routed away. This is the check worth having run before 390 batches.", ""]

    L += ["", "## Empirical anchors — verdict distribution", "",
          "**A high `UNCERTAIN` rate here is compliance, not failure.** Three of the scope's routing "
          "tests turn on the treatment instrument's item content, which titles and abstracts do not "
          "state, and the rubric binds those to `UNCERTAIN` + `needs_full_text`. Scoring UNCERTAIN "
          "as an error would push a screener toward the confident-verdict-without-basis failure "
          "D.3.b already committed.", "",
          f"- RELEVANT {emp_v['RELEVANT']} · UNCERTAIN {emp_v['UNCERTAIN']} · "
          f"NOT_RELEVANT {emp_v['NOT_RELEVANT']} (of {len(emp)} empirical anchors)",
          f"- pair agreement where the screen committed to one: **{pair_ok}/{pair_n}**", ""]
    if emp_rejected:
        L += ["### Empirical anchors the screen REJECTED outright — read every one", "",
              "A known-empirical anchor called `NOT_RELEVANT` is the expensive error: an `UNCERTAIN` "
              "costs one full-text read, a wrong `NOT_RELEVANT` costs the study.", ""]
        L += [f"- **{k['title'][:100]}** → `{v['estimand_cell']}` — {str(v.get('reason'))[:110]}"
              for k, v in emp_rejected]
        L += [""]
    OUT_MD.write_text("\n".join(L) + "\n")
    print(f"decoys routed away {len(dec_ok)}/{len(decoys)}; "
          f"empirical anchors rejected outright {len(emp_rejected)}", file=sys.stderr)
    print(f"wrote {OUT_MD}", file=sys.stderr)
    if dec_bad:
        sys.exit(2)


if __name__ == "__main__":
    main()
