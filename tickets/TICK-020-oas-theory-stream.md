# TICK-020: OAS theory stream for JEL-style mechanism section
**Status:** open
**Assigned:** any
**Parallel-safe:** yes
**Blocks:** TICK-019
**Blocked by:** none
**Touches:** extraction/old-age-security-pension-crowdout-theory-sources.csv, output/chapters/old-age-security-pension-crowdout.md, literature/pdfs/old-age-security-pension-crowdout-theory/

## Description

Build the theory/mechanism corpus needed for the JEL-style section of the OAS/pension-crowdout
chapter. This is separate from the empirical meta-analysis set. Theory papers explain why children
can serve as old-age security, why pensions or social insurance can crowd out fertility demand, and
how PAYG/social-security systems interact with endogenous fertility.

## Acceptance criteria
- [ ] Theory-source table contains canonical foundational and formal-model sources.
- [ ] Each row has a mechanism role and use-in-chapter field.
- [ ] Published/version-of-record sources are preferred where available.
- [ ] Missing or book/chapter-only sources are marked `TITLE_KEY` or `needs_manual` rather than forced into DOI workflows.
- [ ] Chapter mechanism section cites theory sources separately from empirical effect evidence.
- [ ] Output committed.

## Log
<!-- Append completion note here when done. -->
- 2026-07-03: Created after noting OAS full-text set only covered empirical papers; initial theory-source table seeded from `old-age-security-pension-crowdout-canon-resolved.json`.
