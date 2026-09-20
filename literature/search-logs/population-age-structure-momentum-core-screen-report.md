# Core-first screen — A.9 population age structure and demographic momentum

**Run:** 2026-09-20, Shravan (TICK-089). **Set:** the 62 highest-prior records — the plausibly-primary
cells (MOMENTUM / PRIMARY_COMPOSITION / age-structure-ambiguous) plus the 21 multi-channel
(keyword ∩ Tier-B) Tier-1 candidates, from `…-screen-worklist.json` and `…-snowball-tierb.json`.
Screened on **title + abstract** (46 of 62 had abstracts). Verdicts in
`…-core-screen-results.json`. This is the "screen the core first" pass agreed 2026-09-20, to test the
`empty-cell-is-the-result` expectation before committing to the full ~700-record screen.

## Result

| Verdict | n |
|---|---:|
| RELEVANT_PRIMARY (A.9 empirical: age-structure→CBR/births decomposition) | **2** |
| UNCERTAIN (decomposition, route needs full text) | 1 |
| RELEVANT_THEORY (formal momentum theory → JEL theory stream) | 37 |
| OFF (routed elsewhere / homonym / population-growth outcome) | 22 |

## The empirical A.9 cell is ~2 studies — `empty-cell-is-the-result` confirmed

The only unambiguous A.9 primary study in the highest-prior 62 records is **"Study the Effect of
Population Age Structure Changes on the Crude Birth Rate in China" (2014)** — it decomposes CBR change
into an age-structure contribution share for China 1949–2011, which is exactly A.9's
`PRIMARY_COMPOSITION_CBR` estimand. **"Declining number of births in China: a decomposition analysis"
(2021)** is very likely the same age-structure-vs-rate split on birth counts (`PRIMARY_COMPOSITION_BIRTHS`),
to confirm at full text. That is the empirical cell: **two studies, both China.**

## The load-bearing routing finding: "fertility decomposition" ≠ "age-structure decomposition"

Most of the "decomposition of fertility" papers the keyword axis pulled are **not A.9** — they
decompose fertility into *other* components and route to sibling chapters:

- **Bongaarts proximate determinants** (marriage, contraception, postpartum infecundability, abortion):
  Nigeria 2026, Upper Egypt 2006 → A.2 / A.5 / A.7 / A.13. **OFF for A.9.**
- **Union / partnership composition:** "Fewer Couples, Fewer Births" 2026, Bulgaria/Russia unions 2007
  → A.7 (marriage). **OFF for A.9.**
- **Fertility-preference disparities** (Oaxaca by residence/wealth): Ethiopia 2024 → not an age
  structure and not a birth rate. **OFF.**

A.9 owns **only** the split of a birth *rate/count* into an age-*structure* (composition) component and
an age-specific-*rate* component. This distinction is now the chapter's central screening rule and
should be enforced at full-text screen for any residual "decomposition" hit.

## The momentum literature is real but is theory + population-growth, not birth-rate composition

37 records are formal population-momentum theory (pseudostable populations, gradual-transition momentum,
spatial/stochastic momentum, stable/nonstable decompositions) → the **JEL theory stream**. Where
momentum papers are empirical (Korea 2015, China 2017, Korea 2018), their **outcome is future
population size/growth**, not a birth rate → `OFF_OUTCOME_POP` (Wall 3). Homonyms present and correctly
excluded: momentum in wildlife/vertebrate management, "inequality momentum," and literal soil/pesticide
"decomposition."

## Bottom line and recommendation on the full pass

Four signals (frame probe → empty channel 1 → channel-2/3 anchors → production pull) already pointed
here; the core screen now **confirms it against the actual highest-prior records**: A.9's empirical
primary cell is **~2 studies**, so stage 9 is **narrative synthesis, not meta-analysis**, and the
demographic-significance verdict rests on those two decompositions plus the accounting/momentum theory
(near-determinate: composition large for the CBR, zero by construction for period TFR and CCF).

**Recommendation:** the full ~700-record pass is very unlikely to move the verdict — it would mainly
populate the theory stream and off-cell routing. Its only value is (a) PRISMA recall completeness and
(b) catching a hidden age-structure CBR/births decomposition in the tail. Options: (i) accept the core
result and do a **targeted recall check** (screen only the ~9 remaining "decomposition"-titled records
in the full worklist + the Tier-B FERT_OTHER, not all 700); (ii) run the full pass for a complete PRISMA
count; (iii) proceed to full-text retrieval of the 2–3 primary candidates and draft on the
`empty-cell` finding. Flagged for a decision.
