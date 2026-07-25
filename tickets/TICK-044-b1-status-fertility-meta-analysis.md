# TICK-044: B.1 status-fertility meta-analysis (moderated by contraceptive availability)
**Status:** done
**Assigned:** any
**Parallel-safe:** yes (with TICK-043)
**Blocks:** TICK-045
**Blocked by:** TICK-042
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
- [x] `b1_meta_pipeline.py` with a test file, mirroring the OAS pipeline structure.
- [x] Random-effects pooled association with SE, 95% CI, and a heterogeneity statistic.
- [x] Moderator analysis by contraceptive availability and by sex.
- [x] The conservative pooling rule (same outcome family, harmonized metric, >= 3 independent studies) is honored; anything looser is labeled a summary, not a structural estimate.
- [x] Result written back into Section 6 of the chapter, replacing the pending paragraph.

## Log
- 2026-07-25 (Claude): pipeline run on the closed extraction set (17 effects, 5 studies). Results in
  `output/tables/…-meta-analysis-summary.csv`:

  | group | k_eff | k_stud | pooled r | 95% CI | I2 |
  |---|---|---|---|---|---|
  | overall | 8 | 5 | 0.0059 | -0.0579, 0.0697 | 99.8% |
  | contraception absent | 1 | 1 | *insufficient (<3); reported not pooled* | | |
  | contraception present | 7 | 4 | -0.0135 | -0.0803, 0.0535 | 99.8% |
  | female | 3 | 3 | -0.1275 | -0.2118, -0.0414 | 96.5% |
  | male | 5 | 5 | 0.0854 | 0.0302, 0.1400 | 96.7% |

  **Three cautions that belong with any use of these numbers.** (1) The sex split is the only cell with
  a CI excluding zero, and it is the predicted sign pattern — but I2 is 96-97% in both cells, so the
  pooled point estimate is a location summary for a very heterogeneous set, not a structural parameter.
  (2) The headline moderator test — absent versus present contraception — **could not be run**: only one
  study has a contraception-absent population, so the conservative rule correctly refused to pool it.
  The contrast the hypothesis actually predicts therefore remains untested at k=1 (this is DECISION 3 in
  the TICK-046 PI packet). (3) Leave-one-out shows significance in each sex cell rests on a single
  study. The chapter's "consistent direction, not a precise magnitude" wording is the defensible claim.
- 2026-07-22 (Claude, prototype): built `source/analysis/b1_meta_pipeline.py` (Fisher-z harmonization, DerSimonian-Laird random effects, back-transform to r, subgroup pools by contraceptive_availability and sex, conservative >=3-study rule) + `test_b1_meta_pipeline.py` (10 tests, all pass; RE math checked against hand-computed fixtures). Ran on the real effects CSV: `poolable now: 1 | pending extraction: 4` -> every pool correctly "insufficient (<3 studies); reported not pooled". Output `output/tables/…-meta-analysis-summary.csv`; note `output/…-meta-analysis-prototype.md`. Pipeline proven by tests; pooled Section-6 estimate lands when extraction completes. Lidborg 2020/2022 stays an external benchmark (dimorphism != status), not pooled in.

