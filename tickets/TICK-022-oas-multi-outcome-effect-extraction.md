# TICK-022: OAS multi-outcome effect extraction
**Status:** done
**Assigned:** Codex
**Parallel-safe:** no
**Blocks:** TICK-019
**Blocked by:** none
**Touches:** extraction/old-age-security-pension-crowdout-effects.csv, output/*effect-extraction-review.csv, output/tables/old-age-security-pension-crowdout-*.csv, output/figures/old-age-security-pension-crowdout-evidence-map.csv, output/chapters/old-age-security-pension-crowdout.md

## Description

Expand the OAS effect extraction table from one main estimate per paper to one row per relevant
outcome-estimate pair where the PDF reports multiple quantitative fertility outcomes.

## Acceptance criteria
- [x] Papers with multiple relevant fertility outcomes have separate effect rows.
- [x] Each new numeric row has a PDF page/table/figure locator and extraction note.
- [x] `outcome_name` preserves the paper-visible variable wording.
- [x] `outcome_family` remains a harmonization bucket, not a replacement outcome label.
- [x] Generated review, harmonized, summary-of-findings, and evidence-map outputs are regenerated.
- [x] Chapter text notes the multi-outcome row convention.

## Log
- 2026-07-10 Codex: Added separate rows for additional reported outcomes in Danzer/Zyska,
  Rossi/Godard, Billari/Galasso, Han/Tao/Wang/Zhang, Shen/Zheng/Yang, and Galofre-Vila;
  regenerated the RA review sheet and downstream harmonized/meta-analysis/evidence-map outputs.
