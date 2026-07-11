# TICK-029: OAS demographic-significance table
**Status:** done
**Assigned:** Codex
**Parallel-safe:** no
**Blocks:** TICK-019
**Blocked by:** none
**Touches:** source/analysis/oas_meta_pipeline.py, source/analysis/test_oas_meta_pipeline.py, output/tables/old-age-security-pension-crowdout-demographic-significance.csv, output/chapters/old-age-security-pension-crowdout.md

## Description

Generate the OAS demographic-significance table Anup needs for the hybrid Cochrane/JEL chapter.
Use the TFR transition classification, oriented effect evidence, and conservative no-pooling rule
to produce PM/FDT/SDT verdict rows. Keep Cell C grandparental childcare separate and mark it as
not yet quantified until the Cell C papers are extracted.

## Acceptance criteria
- [x] `output/tables/old-age-security-pension-crowdout-demographic-significance.csv` exists.
- [x] Table has rows for PM, FDT, SDT classic OAS, and SDT grandparental childcare.
- [x] FDT/SDT rows use TFR transition classification and oriented effect evidence.
- [x] Verdicts distinguish causal credibility from demographic significance.
- [x] Chapter and reproducibility appendix reference the demographic-significance table.
- [x] Tests cover the table generator.

## Log
<!-- Append completion note here when done. -->
- 2026-07-11 Codex: Added demographic-significance generator to the OAS pipeline, created
  `output/tables/old-age-security-pension-crowdout-demographic-significance.csv`, and updated the
  chapter and summary-of-findings language. The table concludes: PM insufficient direct evidence,
  FDT partial, SDT classic OAS not significant/contextual, and SDT grandparental childcare pending
  Cell C extraction.
