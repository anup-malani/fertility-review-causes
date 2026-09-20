# Cold-start anchor log — population age structure and demographic momentum (A.9)

**Hypothesis:** A.9, slug `population-age-structure-momentum`
**Run:** 2026-09-20, Shravan (TICK-089)
**Artifact:** `population-age-structure-momentum-cold-start-anchors.json` — 17 records, **all 17
existence-verified (FOUND)**; 15 identity-verified. Every record resolved live against OpenAlex; **no
DOI was asserted from memory** (the standing rule from the 2026-07-08 OAS ghost-gold run, reinforced by
the A.10 warning that Keyfitz 1971 is exactly the citation an LLM fabricates fluently).
**Scope doc:** `population-age-structure-momentum-search-scope.md` (DRAFT, not frozen)
**Frame probe:** `population-age-structure-momentum-frame-probe.md` (momentum core ≈192, working frame ≈502)

---

## 1. Headline: channel 1 is empty, and — as for C.2.c and D.3.b — that is a finding

**No systematic review or meta-analysis of population age structure / demographic momentum → fertility
exists.** OpenAlex `("population momentum" OR "demographic momentum") AND fertility, type:review`
returns **1** record, and it is off-topic (a 2025 climate-policy mainstreaming review,
`10.1080/14693062.2025.2527852`); the age-structure-decomposition review query returns **0**. The
near-miss is kept in the JSON as `channel1_SR_nearmiss` so the audit shows the channel was worked.

This is the *third* hypothesis in a row to find channel 1 empty (D.3.b too new, C.2.c never
synthesised, A.9 now). But A.9's reason is the deepest and is the chapter's thesis, not an accident of
timing: **A.9 is an accounting identity, not an effect literature.** There is nothing to systematically
review because there is no body of *causal-effect* studies — there is a body of *decomposition and
projection arithmetic*. Channel 1's emptiness is the first confirmation of the scope's non-effect-estimand
framing (and of TICK-080 item 6/7, which A.9 instantiates).

## 2. Channel 2 (canon): 12 verified anchors, and the empirical primary cell is nearly empty

Verified and kept (identity_verified = true), by cell:

- **Momentum theory / formal (`MOMENTUM_THEORY`, 7):** Keyfitz 1971 (v5 seminal, the founding
  momentum-factor derivation), Krishnamoorthy–Potter–Pickard 1981, Frejka 1973, Kim & Schoen 1997,
  Schoen & Kim 1991, Preston–Heuveline–Guillot 2001 (textbook: standardization/decomposition + stable
  population), Kitagawa 1955 (the rate-vs-composition decomposition method itself).
- **Momentum with a births/growth interpretation (`PRIMARY_MOMENTUM`, 3):** Bongaarts & Bulatao 1999
  (v5 seminal), Lutz–O'Neill–Scherbov 2003 (v5 seminal; negative SDT momentum), Blue & Espenshade 2011.
  **All three carry an OFF_OUTCOME_POP tension** — their headline outcome is population growth/size, and
  only the momentum *component* is A.9's. Extract the component, not the total (scope Wall 3).
- **Exposure determinant (`EXPOSURE_DETERMINANT`, 2, context):** Chesnais 1990 (the transition builds
  the age structure), Coale 1956 (fertility, not mortality, drives age composition — the A.1/A.9 seam).
- **Empirical birth-rate/count decomposition (`PRIMARY_COMPOSITION_BIRTHS`, 1):** Preston & Guillot
  ("Population dynamics in an age of declining fertility"). OpenAlex metadata is drifted (dates it 2009,
  source "Archined"; true venue Genus, ~1997) — **kept keyed on title + both authors** per the
  drifted-identifier rule, not dropped.

**The single most important observation for the chapter:** the cell that would carry a meta-analysis —
empirical decompositions of a *crude birth rate or birth count* into composition and rate components —
has **one** anchor. The literature is overwhelmingly (a) formal momentum theory and (b) population-size
projection. This is the scope's prediction confirmed at the anchor stage: **`empty-cell-is-the-result`
is live for A.9's identified/empirical cell**, and the chapter is a theory-plus-decomposition synthesis,
not a pooled effect estimate.

### Two candidates dropped by the existence gate (recorded, not asserted)

- **"On the correspondence between fertility and population momentum" (Espenshade et al., ~2011).** Did
  not resolve to any OpenAlex record under several title variants. Rather than assert a possibly
  mis-remembered citation, it is **dropped**; the momentum-theory slot it would have filled is covered
  by the verified Krishnamoorthy–Potter–Pickard 1981. This is the ghost gate working as intended.
- **Das Gupta 1993, "Standardization and Decomposition of Rates: A User's Manual."** A real US Census
  Bureau report but with no OpenAlex/DOI record (a P23 current-population report). Not anchored; the
  decomposition-method slot is held by the verified Kitagawa 1955. Noted here as known method canon.

## 3. Decoys (routing tests; not in the empirical recall denominator)

Per the scope, the anchor set deliberately carries off-cell decoys so the eventual query is tested on
**routing**, which is A.9's binding constraint (not retrieval):

- `OFF_TEMPO_A11` — Bongaarts & Feeney 1998, "On the quantum and tempo of fertility." If a query pulls
  this into A.9's core, the cause axis is too loose (Wall 1). The frame probe already measured 136
  tempo-overlap records in-frame.
- `OFF_OUTCOME_POP` — Lutz–Sanderson–Scherbov 2008, "The coming acceleration of global population
  ageing." Outcome is ageing/size, not a birth rate (Wall 3); the largest expected off-cell class.
- `OFF_OTHER` (homonym) — the ecology "age structure" literature (Caswell, matrix population models).
  The 32,363-record unrestricted `age structure` contamination the frame probe flagged; a real off-topic
  record that a bare `age structure` term would flood the screen with.

## 4. Gold is far below the ≥30 empirical-anchor CV floor — and that is correct here

GACS sets a ≥30 empirical-anchor floor before fold-local term mining and cross-validation are
trustworthy. A.9 has **one** empirical primary-cell anchor. Under GACS this would trigger channel 4
(Anup's broad single-query search + structured screen). For A.9 the honest reading is different: the
floor is not reachable because the empirical effect literature does not exist, not because the search is
thin. Consequences for stage 3:

- **No fold-local CV term mining.** With a one-item empirical cell there is nothing to cross-validate.
  The production cause axis is set from the **frame-probe vocabulary** (momentum-specific terms; generic
  `age structure`/`age composition` admitted only under a decomposition/CBR gate), not learned from gold.
- **The production run's job is coverage of the decomposition/momentum literature, then routing**, so
  the ~500-record working frame is screened primarily to (a) find any additional empirical CBR/births
  decompositions and (b) route the momentum-theory and population-size majority to the theory stream and
  `OFF_OUTCOME_POP`. Expect the empirical pool to stay in single digits.

## 5. Next (channel 3, not yet run)

Citation snowball from the channel-2 seeds (backward refs + capped forward cites on the topic-specific
momentum anchors, not the broad theory ones) → the orthogonal Tier-B frame, existence-gated on the same
rule. To run at stage 3 once the scope is frozen (pending the two PI escalations and the Wall 1 second
read). Snowball off Keyfitz 1971 and Preston–Heuveline–Guillot must be forward-capped hard — both are
broad-theory anchors and will explode (the GACS forward-citation caution).
