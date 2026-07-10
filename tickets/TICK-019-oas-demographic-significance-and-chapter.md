# TICK-019: OAS demographic significance and hybrid chapter draft
**Status:** blocked
**Assigned:** any
**Parallel-safe:** no
**Blocks:** none
**Blocked by:** TICK-020; demographic-significance macro pass
**Touches:** output/tables/old-age-security-pension-crowdout-demographic-significance.csv, output/chapters/old-age-security-pension-crowdout.md

## Description

Compute demographic significance for PM/FDT/SDT and draft the OAS hybrid JEL/Cochrane chapter using
`output/chapters/hybrid-chapter-template.md`.

## Acceptance criteria
- [ ] Demographic-significance table exists for PM, FDT, and SDT.
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
