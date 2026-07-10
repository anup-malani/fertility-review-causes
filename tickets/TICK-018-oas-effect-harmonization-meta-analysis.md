# TICK-018: OAS effect harmonization and meta-analysis
**Status:** done
**Assigned:** any
**Parallel-safe:** no
**Blocks:** TICK-019
**Blocked by:** TICK-016, TICK-017
**Touches:** docs/meta-analysis-effect-size-harmonization.md, source/analysis/, output/tables/, output/figures/

## Description

Harmonize OAS effect estimates into comparable fertility units where possible and run quantitative
synthesis or structured narrative synthesis according to `docs/meta-analysis-effect-size-harmonization.md`.

## Acceptance criteria
- [ ] Harmonized-effects table exists.
- [ ] Poolable groups are explicitly defined.
- [ ] Non-poolable estimates are retained with reasons.
- [ ] Forest plots or structured evidence maps are generated.
- [ ] Sensitivity analyses are documented.

## Log
<!-- Append completion note here when done. -->
- 2026-07-09: Harmonized-effects table, meta-analysis summary, summary-of-findings table, and
  evidence-map data generated. Current synthesis is quantitative but not pooled: all 10 rows are
  retained as `not_poolable` because treatment scale, follow-up window, and sign orientation are
  not yet compatible enough for cross-study pooling.
