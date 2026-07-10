# TICK-023: OAS effect review sheet source columns
**Status:** done
**Assigned:** Codex
**Parallel-safe:** no
**Blocks:** none
**Blocked by:** none
**Touches:** source/analysis/oas_meta_pipeline.py, source/analysis/test_oas_meta_pipeline.py, output/old-age-security-pension-crowdout-effect-extraction-review.csv, RA-PLAYBOOK.md, extraction/schema.md

## Description

Revise the OAS effect extraction review sheet so each reviewed characteristic keeps its RA
decision column but replaces the RA notes column with a concise source/location column.

## Acceptance criteria
- [x] Review sheet has `{field}`, `{field}_ra_decision`, and `{field}_source` columns.
- [x] Review sheet has no `{field}_ra_notes` columns.
- [x] Source cells briefly indicate where the extracted value came from.
- [x] Existing RA decision cells are preserved when regenerating the sheet.
- [x] RA instructions document that blank decision cells mean approved and corrections go in the value cell.

## Log
- 2026-07-10 Codex: Replaced effect-review RA notes columns with source locator columns,
  regenerated the OAS effect review sheet/template, and updated RA/schema design docs.
