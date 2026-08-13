# Screening rubric — antidepressants-ssri-subfecundity (B.7)

Title/abstract screen over the D1 worklist. The screener sees title, venue, year, type, and a truncated abstract, and does NOT see the D1 score or the discovery channel — a screener who can see the blind sieve's rank will anchor on it, which would collapse two independent sieves into one.

## What the screen decides

For each record emit `{id, verdict, cell, note?}` where `verdict` is one of `RELEVANT` / `UNCERTAIN` / `NOT_RELEVANT` and `cell` is one of the cells below.

**The screen assigns a routing cell only.** It does not assign the estimand level (`HAZARD_DECREMENT` vs `TEMPO_ADJUSTED_QUANTUM`) and it does not assign the indication design; both are methods facts, set at full-text extraction.

**Route on what is measured, and on whether the medication is the variation.** B.7 owns a drug whose name appears as a covariate in enormous literatures that estimate something else. A record naming an antidepressant is not thereby a B.7 record: ask what quantity the estimate is of, and whether antidepressant exposure is what moves.

**Check species on every record.** Do not infer it from the topic. On the reconnaissance probes the aquatic-ecotoxicology literature outranked the human work on this chapter's own fecundity vocabulary, so `OFF_ANIMAL` is the default reading of an unqualified claim that antidepressants reduce fecundity, not an afterthought.

**Defer rather than guess.** Where routing turns on Wall 1 — whether the estimate separates the medication from the indication — and the abstract does not say, use `MIXED_INDICATION_UNRESOLVED`. An exclusion an abstract could not support is a silent false negative, and on this hypothesis the design is what decides whether a study speaks to it at all.

## Cells

| cell | definition |
|---|---|
| `PRIMARY_MEDICATION_TO_FERTILITY` | Antidepressant exposure -> a FERTILITY quantity: births, completed parity, TFR, time-to-pregnancy, fecundability. |
| `PRIMARY_MALE_FECUNDITY` | Antidepressant exposure -> a measured MALE fertility outcome (pregnancies achieved, TTP), not a semen parameter. |
| `LINK1_MEDICATION_TO_SEXUAL_FUNCTION` | Antidepressant exposure -> desire, arousal, orgasm, sexual dysfunction incidence. Abundant; earns no primary credit. |
| `LINK2_FUNCTION_TO_COITAL_FREQUENCY` | Sexual dysfunction or desire -> frequency of intercourse. The chain's weakest measured joint. |
| `LINK3_COITAL_TO_CONCEPTION` | Coital frequency -> conception hazard or fecundability. Borrowed from A.14; no recall credit. |
| `ENDOCRINE_MECHANISM` | Antidepressant exposure -> prolactin, gonadotropins, testosterone, or semen parameters. Mechanism, not fertility. |
| `PARAMETER_PREVALENCE` | Exposure prevalence, dispensing volume, duration of use, by age and sex. Feeds demographic significance. |
| `PARAMETER_HAZARD_CLINICAL` | Antidepressant exposure in a fertility-clinic population -> cycle conception or live birth. Selection-flagged. |
| `PARAMETER_DETERMINANT_TO_LOSS` | Antidepressant exposure -> fetal loss, NO fertility outcome. Cross-filed to B.5; neither chapter's recall. |
| `INDICATION_BASELINE_D3A` | Depression/anxiety/psychiatric diagnosis -> fertility, with no medication contrast. D.3.a's, and B.7's counterfactual. |
| `MEASUREMENT_ASCERTAINMENT` | How sexual dysfunction or exposure is ascertained: spontaneous report vs direct questioning, prescription vs adherence. |
| `THEORY_SEROTONERGIC` | Formal or physiological account of serotonergic action on sexual motivation. |
| `ADJACENT_PSYCHOTROPIC` | Antipsychotics, mood stabilisers, anticonvulsants -> any reproductive outcome. Retained, never pooled. |
| `OFF_PREGNANCY_SAFETY` | Sample conditioned on pregnancy; outcome is a property of a birth that occurred (defects, preterm, birth weight, autism, neonatal). Wall 4; expected largest cell. |
| `OFF_ART_A17` | Antidepressant exposure in ART where the estimand is treatment success. Wall 5. |
| `OFF_FETAL_LOSS_B5` | Antidepressant exposure -> fetal loss WITH a fertility consequence estimated. B.5 claims it. |
| `OFF_ENVIRONMENTAL_B2B6` | Environmental antidepressant contamination as the exposure route. Wall 8. |
| `OFF_CLINICAL_MANAGEMENT` | Treating antidepressant-induced sexual dysfunction: bupropion augmentation, sildenafil, drug switching. |
| `OFF_ANIMAL` | Non-human exposure -- fish, invertebrates, rodents, livestock. Wall 7, and the default occupant of this vocabulary. |
| `OFF_OUTCOME` | Antidepressant exposure -> a non-fertility, non-sexual outcome. |
| `MIXED_INDICATION_UNRESOLVED` | Medicated vs general population with the indication not handled, or the abstract silent on how. Held for full text. |
| `ROUTING_DEFERRED_TO_FULLTEXT` | Routing turns on Wall 1's design question and the abstract does not name the design. |
| `REVERSE` | Low desire, subfecundity, or childlessness raising the probability of diagnosis or prescription. |
| `OFF_OTHER` | A non-B.7 fertility determinant with no sibling-hypothesis home. |
| `INSUFFICIENT_INFO` | Cannot be routed on the visible record. Pairs only with UNCERTAIN. |

## Verdict convention

- `RELEVANT` — the record belongs to a primary, parameter, measurement, theory, or context cell. Parameter/measurement/theory records are RELEVANT and are separated downstream; they earn no empirical recall credit.
- `UNCERTAIN` — routing or eligibility genuinely unclear on the visible record. Pairs with `INSUFFICIENT_INFO` or with a MIXED/DEFERRED cell.
- `NOT_RELEVANT` — an `OFF_*` cell, including the very large pregnancy-safety, clinical-management and non-human literatures.

## Batches

7 batches of up to 60 records, 420 records total, abstracts truncated to 60 words.
