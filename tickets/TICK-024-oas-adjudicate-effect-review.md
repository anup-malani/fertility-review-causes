# TICK-024: OAS adjudicate effect extraction review
**Status:** done
**Assigned:** Codex
**Parallel-safe:** no
**Blocks:** none
**Blocked by:** none
**Touches:** extraction/old-age-security-pension-crowdout-effects.csv, output/*effect-extraction-review.csv, output/tables/old-age-security-pension-crowdout-*.csv, source/analysis/oas_meta_pipeline.py

## Description

Adjudicate the completed OAS effect extraction RA review. The review added two previously missed
test statistics for the Han/Tao/Wang/Zhang LTCI estimates.

## Acceptance criteria
- [x] The two Han t-statistics are recorded as test statistics, not reported standard errors.
- [x] Harmonization can derive standard errors from coefficient/test-statistic pairs where valid.
- [x] Generated effect review and harmonized/meta-analysis outputs are regenerated.
- [x] Tests cover derived standard errors from test statistics.

## Log
- 2026-07-10 Codex: Adjudicated the two Han Table 2 values as t-statistics, added explicit
  test-statistic fields, derived the childbirth-row harmonized SE from coefficient/t-statistic,
  and regenerated the effect review and harmonized output.
