# LLM screen — tiers + estimand-ready pooling set — diffusion-of-fertility-control

Screened the full Tier-B frame (3,524 candidates) blind on title+abstract under the A.3 six-wall rubric (Haiku, GACS D2a), then joined verdicts back to discovery provenance. 3,524 scored (full coverage; 0 missing).

## Verdicts

- RELEVANT 330 · UNCERTAIN 818 · NOT_RELEVANT 2376

## Tiers

- **Tier 1** (relevant, both-channel corroborated): 27
- **Tier 2** (relevant, single-channel): 303
- **Tier 3** (uncertain): 818
- excluded (not relevant): 2376

Estimand cells among RELEVANT: PRIMARY_SOCIAL_EXPOSURE 145, PRIMARY_SPATIAL_DIFFUSION 70, DIFFUSION_THEORY 57, PRIMARY_LEGITIMATION_SPREAD 25, PRIMARY_CULTURAL_BOUNDARY_CONTENT 19, PRINCETON_CANON 14

## The pooling set and the identified/descriptive split

The pooling set is RELEVANT ∩ a PRIMARY cell ∩ non-review, non-theory evidence, deduplicated
(version-of-record over preprint/working-paper twin). A.3's binding question is not topic
coverage but *identification*: whether a design separates social diffusion from a common
economic/cultural shock hitting neighbours at once (the reflection problem). So the set is
split on `identification_of_diffusion`, never combined into one number.

- **Pooling set (distinct): 252** → `diffusion-of-fertility-control-estimand-ready.json`
  - by cell: PRIMARY_SOCIAL_EXPOSURE 139, PRIMARY_SPATIAL_DIFFUSION 70, PRIMARY_LEGITIMATION_SPREAD 24, PRIMARY_CULTURAL_BOUNDARY_CONTENT 19
- **Identified core** (SEPARATES_FROM_COMMON_SHOCK): **44**
- **Descriptive residual** (DESCRIPTIVE_RESIDUAL_ONLY): **194**
- reviews holding a primary cell (excluded from the pool on evidence_type): 2
- **Theory stream** (RELEVANT/UNCERTAIN ∩ DIFFUSION_THEORY or PRINCETON_CANON): **113 distinct** → `diffusion-of-fertility-control-theory-stream.json` — SEPARATE; not empirical recall.
  - by cell: DIFFUSION_THEORY 86, PRINCETON_CANON 27

### The scope's predicted thin identified core, realized

Descriptive residual 194 vs identified core 44 (4.4x the identified core). The A1 scope predicted A.3's evidence would be rich in descriptive Princeton-style residual and thin on designs that identify contagion apart from a common shock. That asymmetry is the load-bearing caveat for the whole hypothesis and is reported, not smoothed away.

## Required audit logs

### (1) Routing decoys
- `Soap Operas and Fertility: Evidence from Brazil` → **NOT_RELEVANT / OFF_CHANNEL_A20**
- `Soap Operas and Fertility: Evidence from Brazil` → **NOT_RELEVANT / OFF_CHANNEL_A20**
- `Culture: An Empirical Investigation of Beliefs, Work, and Fertility` → **NOT_RELEVANT / OFF_VERTICAL_A19**
- `The Power of TV: Cable Television and Women's Status in India` → **NOT_RELEVANT / OFF_CHANNEL_A20**
- `The Power of the Pill: Oral Contraceptives and Women's Career and Marr` → **NOT_RELEVANT / OFF_TECHNOLOGY_A2**

Route-away volume overall: OFF_CHANNEL_A20 55 (→A.20), OFF_TECHNOLOGY_A2 28 (→A.2), OFF_STIGMA_LEVEL_A6 18 (→A.6), OFF_VERTICAL_A19 43 (→A.19), OFF_PROGRAM_A5 133 (→A.5), OFF_VALUE_D1 258 (→D.1), OFF_OTHER 689, OFF_OUTCOME 193, REVERSE 5.

### (2) Title-only ceiling
933 of 3,524 frame candidates (26.5%) are title-only. The screen marked 683 records `INSUFFICIENT_INFO`; these are the RA gate / full-text resolution queue.

### (3) Rubric-conformance
- cell values outside the taxonomy: 0

## Caveats

- Verdicts are AUTOMATED (Haiku D2a recall filter). The Sonnet precision pass (D2b) and RA sign-off on the boundary/UNCERTAIN papers are the remaining steps before any pooled estimate.
- Tier 1 rests on both-channel (backward+forward) corroboration, not frozen gold membership.
- This screen tiers the CORPUS; it does not measure search recall. Recall is graded separately against the frozen gold after the production query is fit.
- Wall 1 (A.3 vs A.20 channels) is the highest-cost misroute; the RA gate should sample `diffusion_channel=MASS_MEDIA` and the OFF_CHANNEL_A20 rows first.
- Distinct counts dedup by DOI-then-normalized-title, version-of-record preferred.
