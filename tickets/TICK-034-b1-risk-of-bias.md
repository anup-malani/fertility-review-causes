# TICK-034: B.1 risk-of-bias assessment
**Status:** done
**Assigned:** any
**Parallel-safe:** yes (with TICK-035)
**Blocks:** TICK-036
**Blocked by:** TICK-033
**Touches:** extraction/evolutionary-sex-drive-contraceptive-decoupling-risk-of-bias.csv

## Description

Assess risk of bias for each extracted study across confounding, selection, and identification
credibility. The dominant risk in the status-and-reproduction stream is confounding: traits that raise
status also correlate with education, location, and preferences that move fertility independently.
Cross-population comparisons between contraceptive and non-contraceptive societies carry the added risk
that the two society types differ on many dimensions beyond contraception.

## Acceptance criteria
- [x] One row per extracted study with confounding, selection, and identification ratings.
- [x] Cross-population (contraceptive vs non-contraceptive) comparisons flagged for the many-differences risk.
- [x] Observational status-fertility associations distinguished from any quasi-experimental estimate.
- [x] Overall risk field populated (low / moderate / serious) with a one-line rationale.

## Log
- 2026-07-25 (Claude): 5 rows in `extraction/…-risk-of-bias.csv`, one per extracted study, over the
  full nine-domain schema plus `cross_population`, `overall`, `rationale`, and `ra_verified`.
  **Ratings: 4 of 5 serious, 1 moderate** (von Rueden W2507848855). The serious ratings are driven by
  the confounding domain, as anticipated: these are observational status-fertility associations with no
  quasi-experimental variation anywhere in the extracted set. This is the input that caps the GRADE
  rating downstream, and it should be read alongside the k=1 leave-one-out fragility noted in TICK-037.
