# Screening rubric — fetal-loss-intrauterine-mortality (B.5)

Title/abstract screen over the D1 worklist. The screener sees title, venue, year, type, and a truncated abstract, and does NOT see the D1 score or the discovery channel — a screener who can see the blind sieve's rank will anchor on it, which would collapse two independent sieves into one.

## What the screen decides

For each record emit `{id, verdict, cell, note?}` where `verdict` is one of `RELEVANT` / `UNCERTAIN` / `NOT_RELEVANT` and `cell` is one of the cells below.

**The screen assigns a routing cell only.** It does not assign the estimand level (`ACCOUNTING_SHARE` vs `BEHAVIORAL_NET`); that is a modeling fact that abstracts of decomposition papers rarely state, and it is set at full-text extraction.

**Route on the margin the estimate bites at, not on the disease, exposure, or population.** B.5 owns survival conditional on conception. Infection, nutrition, and maternal health are B.5's drivers AND other chapters' treatments, so the organism or exposure never routes the paper; the measured outcome does.

**Defer rather than guess.** Where routing turns on Wall 2 (conception vs survival margin) or Wall 5 (maternal age as the identifying variation) and the abstract does not name the margin, use `ROUTING_DEFERRED_TO_FULLTEXT`. An `OFF_*` label assigned on an abstract that could not support it is a silent false negative.

## Cells

| cell | definition |
|---|---|
| `PRIMARY_LOSS_TO_FERTILITY` | Variation in fetal-loss/stillbirth rates -> live-birth fertility (completed parity, TFR, births per woman). |
| `PRIMARY_SHOCK_TO_BIRTHS` | An exogenous shock (famine, epidemic, disease-control campaign) whose effect on BIRTHS runs through intrauterine survival. |
| `REPLACEMENT_COMPENSATION` | Effect of a loss on the interval to next conception, subsequent parity, or reproductive compensation. |
| `MECHANICAL_ACCOUNTING` | A loss rate entered into a proximate-determinants or projection model to imply births. |
| `PARAMETER_LOSS_LEVEL` | The level, trend, age gradient, or gestational distribution of loss. No fertility outcome. |
| `PARAMETER_DETERMINANT_TO_LOSS` | A determinant (nutrition, infection, exposure, maternal health) -> loss. No fertility outcome. |
| `MEASUREMENT_METHOD` | Reporting quality, recall bias, misclassification, or definitional comparability of loss/stillbirth data. |
| `THEORY_PROXIMATE_DETERMINANTS` | Formal or theoretical treatment of intrauterine mortality inside a fertility model. |
| `SDT_AGE_COMPOSITION_CONTEXT` | Postponement-driven loss variation in the SDT era. Context only, never pooled. |
| `OFF_CHILD_MORTALITY_A1` | Infant/neonatal/child mortality -> fertility. Post-natal, so A.1's. |
| `OFF_STERILITY_B3` | Infection or disease acting on CONCEPTION: sterility, infertility prevalence, time-to-pregnancy. |
| `OFF_INDUCED_ABORTION_A4` | Deliberate termination, abortion access or law. |
| `OFF_MATERNAL_AGE_A15` | Maternal age or childbearing timing IS the identifying variation. |
| `OFF_ART_A17` | Loss measured inside ART/IVF cycles where the estimand is treatment success. |
| `OFF_DETERMINANT_CHAPTER` | Determinant -> a reproductive margin OTHER than intrauterine survival (B.2/B.4/B.6/B.7). |
| `OFF_OUTCOME` | Loss as a determinant of a NON-fertility outcome: maternal mental health, later child health, obstetric risk. |
| `OFF_CLINICAL_MANAGEMENT` | Diagnosis, prevention, or treatment of recurrent pregnancy loss or stillbirth. Expected to be the largest cell. |
| `OFF_ANIMAL` | Non-human embryonic or fetal mortality. Wall 7. |
| `MIXED_PERINATAL_UNRESOLVED` | Perinatal composite spanning the live-birth boundary, components not separable. |
| `MIXED_FECUNDITY_UNRESOLVED` | Conception and survival margins both present, neither decomposed. |
| `ROUTING_DEFERRED_TO_FULLTEXT` | Routing turns on Wall 2 or Wall 5 and the abstract does not name the margin. |
| `REVERSE` | Fertility, parity, or birth spacing affecting LOSS risk (the direction B.5 does not claim). |
| `OFF_OTHER` | A non-B.5 fertility determinant with no sibling-hypothesis home. |
| `INSUFFICIENT_INFO` | Cannot be routed on the visible record. Pairs only with UNCERTAIN. |

## Verdict convention

- `RELEVANT` — the record belongs to a primary, parameter, measurement, theory, or context cell. Parameter/measurement/theory records are RELEVANT and are separated downstream; they earn no empirical recall credit.
- `UNCERTAIN` — routing or eligibility genuinely unclear on the visible record. Pairs with `INSUFFICIENT_INFO` or with a MIXED/DEFERRED cell.
- `NOT_RELEVANT` — an `OFF_*` cell, including the large clinical-management and non-human literatures.

## Batches

8 batches of up to 49 records, 392 records total, abstracts truncated to 60 words.
