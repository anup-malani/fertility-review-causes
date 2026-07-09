# LLM screen — tiers + estimand-ready pooling set — old-age-security-pension-crowdout

Screened the D1 pool (1100 papers) with per-paper relevance + estimand extraction, then applied the estimand gate. 1087 scored; ⚠️ 13 unscored, 0 batches missing.

## Verdicts

- RELEVANT 330 · UNCERTAIN 88 · NOT_RELEVANT 669

## Tiers  (raw records → distinct after title-dedup)

- **Tier 1** (relevant, gold-corroborated): 116 → **104 distinct**
- **Tier 2** (relevant, single-channel): 214 → **201 distinct**
- **Tier 3** (uncertain net): 88
- excluded (not relevant): 669

## Meta-analysis sets (the deliverable)

- **Topical meta-analysis-ready** (T1∪T2 ∩ empirical): 181 → **166 distinct**
- **Estimand-ready pooling set** (topical ∩ PRIMARY cell): 69 → **61 distinct** → `old-age-security-pension-crowdout-estimand-ready-set.json`

The corpus carries preprint/published near-duplicates (multiple OpenAlex IDs per paper); the distinct counts dedup by normalized title. Full dedup (DOI→title clustering, the Thursday 'fine filter') will refine these slightly.

Estimand cells within T1∪T2: THEORY 159, OFF 102, PRIMARY 69

## Screen vs gold (sanity check)

- gold PRIMARY anchors present in the pool: 10
- of those, screen also called PRIMARY (RELEVANT/UNCERTAIN): 7 (70%) — automated gate vs curated gold agreement

## Caveats

- Tier 1 rests on gold membership (no fresh snowball channel was run on this corpus), so multi-channel corroboration is not yet a T1 basis here.
- Automated verdicts (RA gate still pending): the estimand-ready set is the *automated* pooling candidate; RA sign-off on the boundary/UNCERTAIN papers is the remaining human step.
- Recall of the effect-identifying literature is the separately-measured 80.6% (rebuilt gold); this screen assigns the *corpus* to tiers and does not re-measure recall.
