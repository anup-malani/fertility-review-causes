# TICK-019: OAS demographic significance and hybrid chapter draft
**Status:** blocked
**Assigned:** any
**Parallel-safe:** no
**Blocks:** none
**Blocked by:** TICK-020; Cell C slope scaling; final GRADE/RA review
**Touches:** output/tables/old-age-security-pension-crowdout-demographic-significance.csv, output/chapters/old-age-security-pension-crowdout.md

## Description

Compute demographic significance for PM/FDT/SDT and draft the OAS hybrid JEL/Cochrane chapter using
`output/chapters/hybrid-chapter-template.md`.

## Acceptance criteria
- [x] Demographic-significance table exists for PM, FDT, and SDT.
- [ ] GRADE/summary-of-findings table exists.
- [ ] Chapter draft follows the hybrid template.
- [ ] Claims trace to extraction, risk-of-bias, meta-analysis, or theory sources.
- [ ] RA readability check queue is created.

## Log
<!-- Append completion note here when done. -->
- 2026-07-09: Added `output/chapters/old-age-security-pension-crowdout.md` as a first chapter
  draft at the user's request, using Anup's PI v4 review, the 2026-07-05 meeting summary, and
  current extraction tables. Ticket remains blocked for formal completion until TICK-018 supplies
  effect harmonization, risk-of-bias, demographic-significance, and final GRADE outputs.
- 2026-07-09: Chapter updated with quantitative synthesis outputs and reproducibility appendix
  links. TICK-018 is now complete, but this ticket remains open because the demographic-significance
  table and theory-stream dependency are not complete.
- 2026-07-11: TFR-based target-period classification now exists at
  `output/tables/old-age-security-pension-crowdout-tfr-transition-classification.csv`, using the
  replacement-status rule documented in
  `decisions/2026-07-11-tfr-replacement-transition-classification.md`. This is a prerequisite for
  the full demographic-significance table, not a substitute for slope-sufficiency calculations.
- 2026-07-11: Demographic-significance table now exists at
  `output/tables/old-age-security-pension-crowdout-demographic-significance.csv`. Verdicts:
  PM insufficient direct evidence; FDT partial; SDT classic OAS not significant/contextual; SDT
  grandparental childcare pending Cell C extraction. Ticket remains open for theory stream,
  Cell C extraction, final GRADE/summary adjudication, and RA readability check.
- 2026-07-11: Cell C grandparental-childcare extraction completed for Eibich-Siedler 2020,
  Ilciukas 2023, and Akyol-Atalay 2025. The SDT grandparental-childcare row now reports
  `partial_pending_slope_scaling` with positive direction after orienting effects to greater
  grandparent availability. Ticket remains open for theory stream, Cell C slope scaling, final
  GRADE/summary adjudication, and RA readability check.
- 2026-07-11: Added noob-readable Cell C slope-scaling output at
  `output/tables/old-age-security-pension-crowdout-cell-c-slope-scaling.csv` and interpretation
  note at `output/old-age-security-pension-crowdout-cell-c-slope-scaling.md`. This orients all 8
  Cell C effect rows to greater grandparent availability and marks them as not coefficient-pooled
  because treatment scales differ. Ticket remains open for formal slope-sufficiency comparison
  against observed SDT fertility changes, final GRADE/summary adjudication, and RA readability
  check.
- 2026-07-11: Added Cell C slope-sufficiency screen at
  `output/tables/old-age-security-pension-crowdout-cell-c-slope-sufficiency.csv` and note at
  `output/old-age-security-pension-crowdout-cell-c-slope-sufficiency.md`. Six rows are large
  relative to observed TFR declines in the Netherlands and Australia windows; Germany is marked
  not applicable because its study window has no observed TFR decline. Ticket remains open for
  chapter integration, final GRADE/summary adjudication, and RA readability check.
- 2026-07-11: Integrated the noob-facing meta-analysis into
  `output/chapters/old-age-security-pension-crowdout.md` and added generated GRADE verdicts at
  `output/tables/old-age-security-pension-crowdout-grade-verdicts.csv`. The chapter now states
  Cell A is structured quantitative narrative and Cell C is separate SDT structured quantitative
  synthesis with slope-screening support. Ticket remains open for RA/PI risk-of-bias verification
  and readability review.
