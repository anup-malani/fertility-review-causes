# TICK-021: Derive OAS target-period relevance from verified study windows
**Status:** done
**Assigned:** any
**Parallel-safe:** yes
**Blocks:** TICK-018
**Blocked by:** TICK-016
**Touches:** extraction/old-age-security-pension-crowdout-studies.csv, output/old-age-security-pension-crowdout-study-extraction-review.csv, source/analysis/ or source/build/

## Description

After the RA finishes verifying `country_or_region`, `period_start`, and `period_end` for the OAS
study extraction sheet, derive `period_target_relevance` automatically from country/region fertility
levels over the verified study window.

Use country-year fertility data where available. Prefer the treatment or policy exposure year when it
is narrower than the full sample window; otherwise use the verified sample start/end years. Route
ambiguous or multi-country cases for human review instead of forcing a label.

## Acceptance criteria
- [ ] A reproducible script or documented procedure derives `period_target_relevance`.
- [ ] The derivation uses verified country/region and study-window fields as inputs.
- [ ] Ambiguous cases are flagged rather than silently classified.
- [ ] Derived labels are written back to the source extraction table or a derived review output.
- [ ] The rule is documented for reuse on future hypotheses.

## Log
<!-- Append completion note here when done. -->
- 2026-07-09: Derived target-period labels from RA-verified country/region and study windows.
  Added `source/analysis/derive_oas_target_period_relevance.py`, wrote
  `extraction/old-age-security-pension-crowdout-target-period-relevance.csv`, and updated
  `period_target_relevance` in `extraction/old-age-security-pension-crowdout-studies.csv`.
  China and non-fertility mechanism rows are flagged for human caution in the audit output.
