# LLM screen — tiers + estimand-ready pooling sets — climate-anxiety-eco-doomerism

Screened the full Tier-B frame (1,170 candidates) blind on title+abstract under **rubric v2**, then joined verdicts back to discovery provenance. 1,170 scored (full coverage; 0 missing).

## Verdicts

- RELEVANT 224 · UNCERTAIN 125 · NOT_RELEVANT 821

## Tiers

- **Tier 1** (relevant, both-channel corroborated): 19
- **Tier 2** (relevant, single-channel): 205
- **Tier 3** (uncertain): 125
- excluded (not relevant): 821

Estimand cells among RELEVANT: ECO_ETHICS_THEORY 84, ANXIETY_CONSTRUCT 61, PRIMARY_ECO_PESSIMISM 49, PRIMARY_HABITABILITY_FEAR 19, PRIMARY_CARBON_ETHICS 7, DESIRE_INDEPENDENCE 4

## The deliverables

The A1 scope's frozen decision 2 forbids pooling across outcome levels, so there are **two**
pooling sets and deliberately no combined file. Both are first-class primary synthesis; the
stated-intention set carries the standing caveat that it measures intention, not behaviour.

- **Stated-intention pool** (RELEVANT ∩ primary cell ∩ non-review ∩ stated/both): **64 distinct** → `climate-anxiety-eco-doomerism-estimand-ready-stated.json`
  - by cell: PRIMARY_ECO_PESSIMISM 36, PRIMARY_HABITABILITY_FEAR 18, PRIMARY_CARBON_ETHICS 6, DESIRE_INDEPENDENCE 4
- **Realized-fertility pool** (same ∩ realized/both): **9 distinct** → `climate-anxiety-eco-doomerism-estimand-ready-realized.json`
  - by cell: PRIMARY_ECO_PESSIMISM 8, PRIMARY_CARBON_ETHICS 1
- **Theory stream** (RELEVANT/UNCERTAIN ∩ ANXIETY_CONSTRUCT or ECO_ETHICS_THEORY): **145 distinct** → `climate-anxiety-eco-doomerism-theory-stream.json` — SEPARATE; does NOT count toward empirical recall.
  - by cell: ECO_ETHICS_THEORY 84, ANXIETY_CONSTRUCT 61
- Reviews holding a primary cell (excluded from pooling on `evidence_type`, per rubric v2 rule 5): 7

### The scope's predicted asymmetry, realized

Theory stream 145 distinct vs stated-intention pool 64 distinct (2.3x the empirical core), and a realized-fertility pool of **9**. Outcome levels across the poolable primary set: STATED_INTENTION_OR_ATTITUDE 61, REALIZED_FERTILITY 6, BOTH 3, NA 2.

The A1 scope predicted a literature rich on stated belief and intention and near-empty on realized fertility. That prediction is confirmed here, and the realized-fertility thinness is the load-bearing caveat for the whole hypothesis: if that pool is small enough, D.3.b's evidence base speaks to what people *say* about childbearing under ecological dread and only marginally to what they *do*. This is a finding to report, not a search failure — and it is why the two pools are never combined.

## Required audit logs

### (1) Routing decoys
Anchors are excluded from the citation frame by work ID, so decoy routing is mostly not directly testable at screen. One exception survived: a duplicate OpenAlex record of a decoy carries a distinct work ID and so entered the frame, giving one live route-away test.

- `Where are the Babies? Labor Market Conditions and Fertility in Europe` → **NOT_RELEVANT / OFF_ECON_C5a**

Route-away volume overall: OFF_POSTMATERIALIST_D1a 50 (→D.1.a), OFF_CLINICAL_D3a 1 (→D.3.a), OFF_ECON_C5a 33 (→C.5.a), OFF_OTHER 188, OFF_OUTCOME 124, REVERSE 13.

### (2) Title-only ceiling
327 of 1,170 frame candidates (27.9%) are title-only. The screen marked 122 records `INSUFFICIENT_INFO`; these are the natural RA gate and full-text-resolution queue. Under rubric v1 these records were being assigned substantive cells they had not earned, which inflated the theory stream — the v2 cell exists to stop that.

### (3) Rubric-conformance violations
- cell values outside the v2 taxonomy: 0
- pairing-constraint violations (NA without NOT_RELEVANT, or INSUFFICIENT_INFO without UNCERTAIN): 0

## Caveats

- Verdicts are AUTOMATED. The pooling sets are automated pooling candidates; RA sign-off on the boundary and UNCERTAIN papers is the remaining human step (the RA gate).
- Tier 1 rests on both-channel (backward+forward) corroboration, not frozen gold membership.
- This screen tiers the CORPUS; it does not measure search recall. Recall is measured separately downstream (production query vs the frozen gold), after which the §7.2 overlap test runs.
- The three boundary walls were applied by an automated screener. The D.1.a confound (left politics, education, secularism predict both climate concern and low fertility) is the central identification threat AND the Wall 1 routing rule — so Wall 1 misroutes are the error mode with the largest downstream cost, and the RA gate should sample them first.
- Distinct counts dedup by DOI-then-normalized-title.
