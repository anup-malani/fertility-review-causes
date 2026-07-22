# TICK-035: B.1 status-fertility meta-analysis (moderated by contraceptive availability)
**Status:** open
**Assigned:** any
**Parallel-safe:** yes (with TICK-034)
**Blocks:** TICK-036
**Blocked by:** TICK-033
**Touches:** source/analysis/b1_meta_pipeline.py, output/tables/evolutionary-sex-drive-contraceptive-decoupling-meta-analysis-summary.csv

## Description

The chapter's accepted quantitative core (Shravan, 2026-07-22). Pool the association between a status or
wealth measure and the number of children across the status-and-reproduction studies, and let the
pooled association vary by whether the population had access to modern contraception and by sex. Adapt
`source/analysis/oas_meta_pipeline.py` (random-effects, harmonization, conservative same-outcome rule).
Harmonize associations to a common effect metric (Fisher-z on r, or standardized beta) before pooling.

Prediction under test: the association is positive where contraception is absent (e.g. von Rueden and
Jaeggi's nonindustrial societies), and attenuated or reversed where it is present, more so for women
than for men. Lidborg et al. (2020, 2022) already pool part of this cell (male dimorphism to fitness)
and should be cited as an external benchmark, not silently re-derived.

## Acceptance criteria
- [ ] `b1_meta_pipeline.py` with a test file, mirroring the OAS pipeline structure.
- [ ] Random-effects pooled association with SE, 95% CI, and a heterogeneity statistic.
- [ ] Moderator analysis by contraceptive availability and by sex.
- [ ] The conservative pooling rule (same outcome family, harmonized metric, >= 3 independent studies) is honored; anything looser is labeled a summary, not a structural estimate.
- [ ] Result written back into Section 6 of the chapter, replacing the pending paragraph.

## Log
<!-- Append completion note here when done. -->
