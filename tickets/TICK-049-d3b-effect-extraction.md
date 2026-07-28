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

**3a. THE WALL 1 MEASURE-CONTENT FIELD (folded in from the gate, RA decision 2026-07-27).**
Record, per study, **what the exposure variable actually contains**, and classify it:
`ecological_fear` / `eco_ethical_concern` / `environmental_values_or_behaviour` /
`mixed` / `unclear`. A study whose exposure is `environmental_values_or_behaviour` is
measuring D.1.a's construct and does not belong in a D.3.b pool.

This field exists because the TICK-047 gate found that **two of the eight
realized-fertility studies fail Wall 1 on measure content**, and that the failure is
invisible to any title-and-abstract screen:

- Traylor & Chae — support for government spending on the environment; the paper names
  Inglehart postmaterialist values theory in its own keywords.
- Ivanova & Rüttenauer — an index of seven pro-environmental household habits: TV
  standby, switching off lights, tap running while brushing teeth, own shopping bag.

Both describe themselves in the abstract as studying environmental concern and
fertility, accurately, in language indistinguishable from a genuine D.3.b study. Wall 1
turns on what the exposure *contains*, which lives in the measures section, so no rubric
rewrite reaches it and no screening pass can catch it. **The gate originally planned a
stratum B sample of the 50 records routed OUT to D.1.a; that tests false exclusions,
which is the direction that is not failing. Stratum B is therefore folded into this
ticket as a per-study extraction field (RA decision, Shravan, 2026-07-27), covering the
direction that is failing: D.1.a studies retained IN the D.3.b pools.**

**Report the bleed-in rate; do not just filter on it.** The share of the retrieved
literature that measures environmental values rather than ecological dread is a finding
about the field, not merely a cleaning step, and TICK-053 should state it. The scope
decision that a smaller, thinner chapter is the correct outcome for a deliberately
narrow hypothesis (Shravan, 2026-07-27, and consistent with the Wall 2 decision of
2026-07-25) governs how the shrinkage is *interpreted* — it is not a reason to leave the
shrinkage unreported.

**3b. Record whether the estimate adjusts for the D.1.a confound.** A boolean-plus-detail field for
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
- [ ] Wall 1 measure-content field populated on every row, with the exposure's actual item
      content quoted or summarised — not just the authors' label for it. A study
      classified `environmental_values_or_behaviour` is routed to D.1.a, not pooled.
- [ ] The Wall 1 bleed-in rate computed over the extracted set and handed to TICK-053 as
      a reportable finding.
- [ ] D.1.a-confound adjustment field populated on every row.
- [ ] Every value second-reader verified before it is marked poolable; the verification pass is logged,
      not assumed.
- [ ] Ambiguous estimates flagged `needs_pi = yes` rather than guessed.

## Log
- 2026-07-27 (Claude, figure/table read): **the two blocked estimates are now recovered, and
  reading them corrected the first pass twice — once against the chapter, once against me.**
  Method: `pdftoppm -r 400` on the figure pages, rotated, then read visually;
  `pdftotext -layout` for Jylhä's Table 1. Both are cheap and should be the default
  next time an estimate is reported as figure-only.

  **Golovina & Jokela, now read off Figures 1 and 2 with CIs:**

  | Estimate | Sample | Model | HR (95% CI) |
  |---|---|---|---|
  | Climate-change worry, very worried | Total | 2 (fully adj.) | **0.82 (0.75, 0.90)** |
  | Climate-change worry, very worried | Childless | 2 | **0.86 (0.79, 0.94)** |
  | Climate-change worry, very worried | Childless | 1 (min. adj.) | 0.86 (0.73, 1.01) — n.s. |
  | Environmental-protection worry, very worried | Total | 2 | 0.85 (0.78, 0.94) |

  **CORRECTION 1 — against the chapter.** The chapter quotes "16 percent" for the childless
  sample, taken from the paper's abstract via the screen record. Figure 2 gives HR 0.86,
  i.e. **14 percent**. The paper's abstract and its own figure disagree. Quote the figure
  value with its CI and flag the mismatch at TICK-053.

  **CORRECTION 2 — against my own earlier extraction, and it reverses a finding I reported.**
  I had recorded from the abstract that economic worry (25%) dominated climate worry (16%)
  in the same sample, and called it the cleanest Wall 3 benchmark in the review pointing
  *against* D.3.b. The abstract's 25% is the **minimally adjusted** Model 1 (HR 0.72). In
  the **fully adjusted** Model 2, economic worry is **not significant** — childless 0.94
  (0.86, 1.04), total 0.93 (0.85, 1.02) — while climate worry **is** significant in both.
  Correctly stated, this study finds ecological worry associated with lower fertility where
  personal economic worry is not. That favours D.3.b over C.5.a and is the opposite of what
  I reported before reading the figures.

  **Jylhä et al., Table 1 extracted — climate worry is a clean null on all three outcomes:**
  number of children b=−0.01 (p=0.45), general ideal family size b=−0.03 (p=0.10), fertility
  intentions b=0.00 (p=0.87). This also corrects my first pass, which had recorded the
  bivariate r=−0.04 (p<0.001); the multivariate coefficient is null. Overpopulation worry
  b=−0.11 (p=0.00) and future-generations worry b=**+0.12** (p=0.00) — opposite-signed
  channels. The general-worries index is itself null (b=−0.05, p=0.06), so this study offers
  no ecological-vs-general discrimination in either direction.

  **Status: 15 rows, 8 poolable (up from 0), 5 with confidence intervals.** What is still
  missing before TICK-051: CIs/SEs for the Jylhä coefficients, the Peters body coefficients,
  and the Weychert CI. `gol_04` — climate worry not surviving adjustment for the summary of
  all other worries — is unchanged by any of this and remains the single most consequential
  row in the table.
- 2026-07-27 (Claude): **first pass on the realized track — 11 effect rows over 4 studies,
  and ZERO are currently poolable.** Tables:
  `extraction/climate-anxiety-eco-doomerism-{studies,effects-realized}.csv`.

  **Not one estimate in the realized stratum has a recoverable confidence interval.** Of
  11 rows: 8 are text statements, 2 are text statements whose actual estimate lives in a
  FIGURE that the text layer cannot recover (Golovina & Jokela's Figures 1 and 2), and 1
  is a table value reached through text. The two headline numbers the chapter already
  quotes — 18% and 16% — are **derived** from prose ("the likelihood ... was 18 percent
  lower"), not transcribed from a table. HR 0.82 and 0.84 are my arithmetic on those
  sentences. That is precisely the failure B.1 caught at second-reader verification (a
  number quoted from prose rather than read off a table), so both rows are `needs_pi`
  and `poolable=no`.

  **Three substantive findings that change what the chapter can conclude.**

  1. **The load-bearing study fails its own ecological-specificity test.** Golovina &
     Jokela: "After adjusting the models for the summary score of all other worries
     except the worry of interest, only worries about own health, crime in Germany, and
     immigration to Germany remained statistically significant." Climate change did not
     survive. The one realized study that beats the D.1.a confound by design fails the
     Wall 2 discrimination internally — its climate effect is not separable from general
     worry. Also: in the childless sample over the full 1984–2020 span the climate
     association is not significant at all; the 16% is the 2009–2020 window only.
  2. **Two of the four are nulls, and one estimate runs the wrong way.** Peters et al.
     (the reverse-causality design the chapter calls its most valuable) finds no
     significant relationship except for pre-1970 cohorts. Jylhä et al. is a null by the
     authors' own conclusion — and within it, worry about *future generations* is
     **positively** associated with number of children (r=+0.06, b=+0.12, p=0.00) while
     overpopulation worry is negative. Pooling those two channels would average
     opposite-signed mechanisms.
  3. **The one large effect is a subgroup interaction in a preprint.** Weychert et al.
     RR=0.38 holds only for high news exposure among the pro-environmental; the paper
     reports no significant effect across political orientation.

  **Independence problem for TICK-051:** Golovina & Jokela and Peters et al. both use
  GSOEP. They are not independent draws and must not be pooled as if they were. That
  leaves at most 3 independent realized samples (GSOEP, Swedish GGS, UKHLS).

  **Wall 1 measure-content field populated on all 6 studies** (the 3a requirement). One
  `mixed` in the realized track (Weychert — media exposure, not expressed dread) and one
  in the stated track (Saha — the operative item is carbon-ethics).

  **Second-reader verification is NOT done.** This is a first pass by one reader and the
  schema's mandatory per-value check is outstanding. Nothing here may enter a pool.
- 2026-07-27 (Claude): opened.
