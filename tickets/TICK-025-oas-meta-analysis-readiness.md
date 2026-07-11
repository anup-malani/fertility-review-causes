# TICK-025: OAS meta-analysis readiness analysis
**Status:** done
**Assigned:** Codex
**Parallel-safe:** no
**Blocks:** TICK-019
**Blocked by:** none
**Touches:** source/analysis/oas_meta_pipeline.py, source/analysis/test_oas_meta_pipeline.py, output/tables/old-age-security-pension-crowdout-*.csv, output/chapters/old-age-security-pension-crowdout.md

## Description

Generate a post-RA meta-analysis readiness table for the OAS chapter. The table should summarize
candidate outcome families, effect directions, uncertainty availability, and the remaining blockers
to valid pooling.

## Acceptance criteria
- [x] Readiness output is generated from the harmonized effects table.
- [x] Output separates screening-only inverse-variance calculations from valid pooled estimates.
- [x] Chapter quantitative-synthesis text reflects the post-RA extraction status.
- [x] Tests cover readiness grouping and screening-only calculations.

## Log
- 2026-07-11 Codex: Added the meta-analysis readiness table, screening-only inverse-variance
  diagnostics, chapter text explaining why these are not valid pooled estimates, and tests.
