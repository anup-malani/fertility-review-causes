# TICK-049: D.3.b effect extraction (two tables, never combined)
**Status:** open
**Assigned:** any
**Parallel-safe:** no
**Blocks:** TICK-050, TICK-051
**Blocked by:** TICK-047, TICK-048
**Touches:** extraction/climate-anxiety-eco-doomerism-studies.csv, extraction/climate-anxiety-eco-doomerism-effects-stated.csv, extraction/climate-anxiety-eco-doomerism-effects-realized.csv, extraction/schema.md

## Description

Extract study-level and estimate-level data from the retrieved full texts, adapting the OAS/B.1 schema
(`extraction/schema.md`, `source/analysis/oas_meta_pipeline.py` column set). The primary effect is the
association between an ecological-fear measure and either a fertility intention or a realized birth.

**Two effect tables, never merged.** A1 scope decision 2 forbids pooling across outcome levels, which
is why the frozen screen produced two pooling files and deliberately no combined one. The separation
has to hold at extraction, not just at synthesis — one table with an `outcome_level` column invites
exactly the pooling the decision forbids.

Three D.3.b-specific requirements beyond the inherited schema:

**1. Carry `desire_for_children_held_fixed` through from the screen records.** It already exists on
every record in the frozen pooling sets. It is the field that separates D.3.b from D.1.a, exactly as
`holds_desire_fixed` separates B.1 from A.2 — and in B.1 that column was never added to the extraction
schema, so TICK-042 closed with the boundary unrecorded and the acceptance criterion vacuously
satisfied. Add it before the first row is written.

**2. Record the instrument, because these exposures are not commensurable.** Climate-anxiety scales,
single-item worry questions, and environmental-identity measures are different instruments on different
scales. Record instrument name, item count, response scale, and direction per estimate, and decide
convertibility to a common metric **per study at extraction time**, flagging non-convertible estimates
`needs_pi` rather than forcing them onto a shared scale at pooling time. Harmonization here is a
substantive decision, not a mechanical one, and the chapter's §6 already says so.

**3. Record whether the estimate adjusts for the D.1.a confound.** A boolean-plus-detail field for
adjustment on political orientation, education, and religiosity/secularism. This is not a routine
covariate list: the contrast between adjusted and unadjusted estimates is the chapter's central
empirical test of whether it is measuring D.3.b or D.1.a, and TICK-051 pools on it as a moderator.

**Second-reader verification is mandatory, not optional.** B.1's hard-won lesson: automated
extraction's `poolable` flag over-claims. Per-value second-reader verification caught F-statistics
coded as *r* and a number quoted from a cited paper rather than from the study itself. Nothing enters a
pool without it.

## Acceptance criteria
- [ ] Study-level table: one row per included empirical study with setting, period, population
      (student / general / other), sample size, and design.
- [ ] Two effect-level tables (stated, realized) with effect, SE or CI, n, and page/table locator.
- [ ] `desire_for_children_held_fixed` populated on every row, carried from the screen record and
      confirmed against full text.
- [ ] Instrument fields populated on every row; convertibility decided per study; non-convertible
      estimates flagged `needs_pi`.
- [ ] D.1.a-confound adjustment field populated on every row.
- [ ] Every value second-reader verified before it is marked poolable; the verification pass is logged,
      not assumed.
- [ ] Ambiguous estimates flagged `needs_pi = yes` rather than guessed.

## Log
- 2026-07-27 (Claude): opened.
