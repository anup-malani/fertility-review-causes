# TICK-051: D.3.b two-track synthesis (stated intention and realized fertility, never pooled together)
**Status:** done — pipeline built and run; **pool REFUSED on the realized track for independence, stated track not yet extracted**
**Assigned:** any
**Parallel-safe:** yes (with TICK-050)
**Blocks:** TICK-052
**Blocked by:** TICK-049
**Touches:** source/analysis/d3b_meta_pipeline.py, source/analysis/test_d3b_meta_pipeline.py, output/tables/climate-anxiety-eco-doomerism-meta-analysis-summary.csv, output/figures/

## Description

Build `d3b_meta_pipeline.py` off `b1_meta_pipeline.py` (itself off `oas_meta_pipeline.py`) and run two
separate random-effects syntheses that are never combined into a single estimate. The prohibition is a
frozen A1 scope decision, and the reason is substantive: the well-populated measure of what people
*say* must not be allowed to stand in for the nearly-absent measure of what they *do*.

**Track 1, stated intention (k up to 62).** This is the only cell large enough for real moderator
analysis, and one moderator matters more than the rest. The contrast between estimates that adjust for
political orientation, education, and religiosity and those that do not is the chapter's central
empirical test: if the association collapses under adjustment, the literature is measuring D.1.a
postmaterialism and this chapter's mechanism is not identified in it. That contrast should be
pre-specified here rather than discovered. Secondary moderators: instrument type (validated
climate-anxiety scale / single-item worry / environmental identity), population (student / general),
and publication year, since 39 of 62 studies are 2024 or later and the recent wave may differ
systematically from the earlier one.

**Track 2, realized fertility (k ≤ 6 clean).** Eight studies, less the formal growth model and the
air-pollution study if TICK-047 sets them aside. This clears the project's conservative ≥3-study rule
but will be fragile, so report leave-one-out alongside the pooled estimate — B.1's pooled result turned
on k=1 in one channel and the fragility was only visible because leave-one-out was run.

Two things to expect and report rather than treat as failures. Exposure measures may not harmonize onto
a common metric at all, in which case the honest output is a structured summary labelled as such, not a
pooled number. And the confounding structure here is uniform rather than idiosyncratic — every
observational study faces the same political-and-educational confound — so heterogeneity will not
average it away and a tight pooled estimate is not evidence that the confound is absent.

## Acceptance criteria
- [ ] `d3b_meta_pipeline.py` with a test file, mirroring the B.1/OAS pipeline structure.
- [ ] Two pooled estimates with SE, 95% CI, and heterogeneity (I², τ²), written to separate rows/files
      with no combined estimate anywhere in the output.
- [ ] Adjusted-vs-unadjusted moderator analysis on the stated track, pre-specified, reported whichever
      way it comes out.
- [ ] Instrument-type, population, and year moderators on the stated track.
- [ ] Leave-one-out on the realized track.
- [ ] Publication-bias check (funnel + Egger) on the stated track only; k is too small on the realized
      track and attempting it there should be recorded as declined, with the reason.
- [ ] The conservative pooling rule honored (same outcome family, harmonized metric, ≥3 independent
      studies); anything looser labelled a summary, not a structural estimate.
- [ ] Forest plot per track via `source/analysis/b1_forest_plot.py` or a D.3.b adaptation.

## Log
- 2026-07-27 (Claude): `source/analysis/d3b_meta_pipeline.py` + 13 unit tests (all
  passing). Outputs in `output/tables/climate-anxiety-eco-doomerism-{realized-summary,
  pooling-decision,synthesis-report}.{csv,md}`.

  **The pipeline's defining behaviour is that it evaluates the conservative rule and
  refuses to pool when the rule is not met, recording why.** A synthesis script that emits
  a pooled number whenever it has two rows is exactly how a chapter reports a structural
  estimate it has not earned, so the refusal path carries more tests than the happy path.

  **Realized track: 2 poolable rows, 2 studies, 1 independent data source → POOL REFUSED.**
  Golovina & Jokela and Peters et al. are both GSOEP; counting them as two would
  double-count one German panel. Jylhä is a different estimand (OLS on number of children,
  not a hazard ratio) and not harmonisable. Weychert reports no interval at all. The AEA
  study was never retrieved. **This is a refusal to pool, not a failed pool**, and Section 6
  must say so in those terms rather than describe a forest plot that does not exist.

  **The pre-specified central test is not estimable.** The adjusted-versus-unadjusted
  contrast this ticket pre-specified cannot be estimated with 3 independent sources of which
  1 adjusts for political attitudes. Recorded in the output as not-estimable rather than
  dropped, so the pre-specification is not quietly abandoned.

  **Stated track: recorded as NOT YET EXTRACTED rather than omitted**, so the absence of a
  pooled estimate cannot be misread as evidence weighed and found wanting.

  Independence is encoded as a `DATA_SOURCE` map rather than inferred, so adding a study
  requires an explicit statement about which panel it uses.
- 2026-07-27 (Claude): opened.
