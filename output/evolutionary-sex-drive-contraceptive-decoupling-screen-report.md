# LLM screen — tiers + estimand-ready pooling set — evolutionary-sex-drive-contraceptive-decoupling

Screened the full Tier-B frame (4,900 candidates) blind on title+abstract, then joined verdicts back to discovery provenance. 4,900 scored (full coverage; 0 missing).

## Verdicts

- RELEVANT 152 · UNCERTAIN 311 · NOT_RELEVANT 4437

## Tiers

- **Tier 1** (relevant, both-channel corroborated): 15
- **Tier 2** (relevant, single-channel): 137
- **Tier 3** (uncertain): 311
- excluded (not relevant): 4437

Estimand cells among RELEVANT: PROXIMATE_ULTIMATE 54, THEORY 48, MOTIVATION_DISTINCTNESS 37, PRIMARY_DECOUPLING 11, PRIMARY_DESIRE_INDEPENDENCE 1, CULTURAL_NORMALIZATION 1

## The deliverables

- **Estimand-ready empirical pooling set** (RELEVANT ∩ primary-empirical cell ∩ non-theory): 95 raw → **95 distinct** → `evolutionary-sex-drive-contraceptive-decoupling-estimand-ready-set.json`
  - by cell: PROXIMATE_ULTIMATE 52, MOTIVATION_DISTINCTNESS 32, PRIMARY_DECOUPLING 10, PRIMARY_DESIRE_INDEPENDENCE 1
- **Theory stream** (RELEVANT/UNCERTAIN ∩ THEORY): 173 raw → **173 distinct** → `evolutionary-sex-drive-contraceptive-decoupling-theory-stream.json` — SEPARATE; does NOT count toward empirical recall.

### The scope's predicted asymmetry, realized
The theory stream (173 distinct) is comparable to or larger than the empirical pooling set (95 distinct), and within the empirical set the direct decoupling / desire-independence core (PRIMARY_DECOUPLING 10 + PRIMARY_DESIRE_INDEPENDENCE 1) is far smaller than the proximate-ultimate dissociation literature (PROXIMATE_ULTIMATE 52). This is the A1-predicted asymmetry (rich theory / status-fertility tests, thin direct decoupling empirics) — a finding to report, not a search failure.

## Required audit logs

### (1) Contraception-tech precision tax — realized
Candidates reachable ONLY via the contraception-tech seeds (Goldin-Katz + Bailey): 1,511. The screen routed **280 to off/route-away cells** (131 to OFF_EXPOSURE_A2 → A.2), and only **11 to a primary-empirical cell**. The A4 audit predicted this stratum (32% keyword-on-topic) would be a precision tax carried for recall; the screen paid it and walled it off from the pooling set rather than promoting it.

### (2) Title-only ceiling
1,789 of 4,900 frame candidates (36.5%) are title-only. UNCERTAIN concentrates here; these are the natural RA-gate and full-text-resolution queue.

### (3) Routing outcome / decoys
The two anchor routing decoys (Pritchett → A.2, Wilcox → A.4) are NOT in the frame (anchors are excluded from the citation frame), so decoy routing is not directly testable at screen. It is validated instead by the realized route-away volume: OFF_EXPOSURE_A2 202 (→A.2), TEMPO_EXPOSURE 16 (→A.4), CULTURAL_NORMALIZATION 18 (→D.1.a) — the A.2/labor cloud routed to off-cells, not into the primary estimand.

## Caveats

- Verdicts are AUTOMATED. The estimand-ready set is the automated pooling candidate; RA sign-off on the boundary/UNCERTAIN papers is the remaining human step (the RA gate).
- Tier 1 rests on both-channel (backward+forward) corroboration, not a frozen gold membership.
- This screen tiers the CORPUS; it does not measure search recall. Recall is measured separately downstream (production query vs the frozen gold), after which the §7.2 overlap test runs.
- Distinct counts dedup by DOI-then-normalized-title; the fine filter refines further.
