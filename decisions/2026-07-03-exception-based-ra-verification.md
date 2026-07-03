# Decision: Exception-based RA verification sheets

**Date:** 2026-07-03
**Author:** Alexandra Zhou + Codex session
**Status:** Active — applies to study-level and effect-level extraction for every hypothesis
**Review trigger:** Revisit after the OAS/pension-crowdout pilot completes extraction and one RA
verification pass.

## Context

After title/abstract review and PDF retrieval, the pipeline creates structured extraction outputs
that drive full-text inclusion, external-validity judgments, effect harmonization, risk of bias,
GRADE, and chapter prose. These tables contain many fields. Requiring RAs to type `APPROVED` or
`VERIFIED` in every field creates busywork and increases the chance of accidental edits to values
that were already correct.

The OAS pilot also introduced transportability/external-validity coding. Those fields are
judgment-based, so they need human review, but the review process must stay fast enough to repeat
across many hypotheses.

## Decision

Use reviewer-facing verification sheets with adjacent value/review columns for every characteristic
that needs human review:

```text
{characteristic}
{characteristic}_ra_decision
{characteristic}_ra_notes
```

Blank `{characteristic}_ra_decision` means the reviewer approves the extracted value by default.
RAs only mark fields that are wrong, ambiguous, or should be excluded.

Valid nonblank decisions:

- `FIX` — value is wrong; corrected value or instruction goes in `{characteristic}_ra_notes`.
- `UNSURE_PI` — reviewer cannot adjudicate; PI decision required.
- `EXCLUDE` — value or estimate should not be used for synthesis.

This convention applies to:

- Study-level review sheets, e.g. `output/{slug}-study-extraction-review.csv`.
- Effect-level review sheets, e.g. `output/{slug}-effect-extraction-review.csv` or
  `output/{slug}-effect-extraction-review-template.csv`.

The compact source-of-truth extraction tables remain under `extraction/`. Reviewer-facing sheets
may duplicate columns under `output/` to make checking faster.

## Rationale

- **Field-level accountability:** every characteristic can be checked independently without
  collapsing the review into one global row decision.
- **Low RA burden:** blank means approved, so reviewers only spend time on exceptions.
- **Better audit trail:** disagreements are tied to the exact field that needs correction.
- **Reusable format:** the same convention works for bibliographic identity, study design,
  external validity, numeric estimates, source locations, and harmonization choices.

## Required workflow

1. The agent pre-fills source-of-truth extraction tables under `extraction/`.
2. The agent generates reviewer-facing sheets under `output/` with adjacent RA decision and notes
   columns.
3. The RA reviews values against the PDF and marks only fields needing action.
4. The agent applies `FIX` decisions back to source-of-truth tables, routes `UNSURE_PI` fields to
   the PI, and excludes fields or estimates marked `EXCLUDE`.
5. Harmonization, meta-analysis, GRADE, and chapter drafting use only approved or corrected values.

## Risks

- **Silent approval if a reviewer skips a row.** Mitigate by requiring reviewers to record completion
  in the ticket log or session log after reviewing a sheet.
- **Overwide CSVs.** Adjacent review columns can make sheets wide. This is acceptable for audit
  clarity; if needed, create separate study-level, effect-level, and risk-of-bias review sheets.
- **Decision spelling drift.** Mitigate by documenting valid labels in `extraction/schema.md` and
  RA-facing instructions.
