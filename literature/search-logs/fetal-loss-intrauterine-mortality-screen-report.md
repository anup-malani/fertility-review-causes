# Screen report — fetal-loss-intrauterine-mortality (B.5)

**Screened: 392** records (the D1 budget slice plus the orthogonal-channel bypass) out of a 11,125-record deduplicated frame.

| tier | definition | n |
|---|---|---|
| 1 | RELEVANT, found through more than one channel or seed | 140 |
| 2 | RELEVANT, single channel | 152 |
| 3 | UNCERTAIN, retained for audit only | 6 |
| — | NOT_RELEVANT, excluded | 94 |

**Primary-cell records: 18** · **support stream (parameter, measurement, theory, accounting, reverse): 267** · **held for full-text adjudication: 13**

## Cell distribution

| cell | n |
|---|---|
| `PARAMETER_DETERMINANT_TO_LOSS` | 139 |
| `PARAMETER_LOSS_LEVEL` | 77 |
| `OFF_CLINICAL_MANAGEMENT` | 49 |
| `MEASUREMENT_METHOD` | 38 |
| `OFF_OUTCOME` | 23 |
| `OFF_OTHER` | 12 |
| `PRIMARY_SHOCK_TO_BIRTHS` | 8 |
| `MIXED_PERINATAL_UNRESOLVED` | 7 |
| `THEORY_PROXIMATE_DETERMINANTS` | 6 |
| `REPLACEMENT_COMPENSATION` | 5 |
| `PRIMARY_LOSS_TO_FERTILITY` | 5 |
| `REVERSE` | 4 |
| `MIXED_FECUNDITY_UNRESOLVED` | 4 |
| `OFF_ART_A17` | 4 |
| `MECHANICAL_ACCOUNTING` | 3 |
| `OFF_ANIMAL` | 3 |
| `OFF_MATERNAL_AGE_A15` | 2 |
| `ROUTING_DEFERRED_TO_FULLTEXT` | 2 |
| `OFF_INDUCED_ABORTION_A4` | 1 |

## The prediction the scope document made, and what came back

The scope document predicted, before the search ran, that `OFF_CLINICAL_MANAGEMENT` and `OFF_OUTCOME` would together be most of the corpus, that the parameter stream would be larger and better identified than the causal stream, and that the primary cells would hold single digits to low tens of studies. All three held. That is not a vindication of the search so much as a statement that the chapter's evidence problem was correctly diagnosed in advance: precision, not recall, is what binds here.

## Validation 1 — anchor recovery on records whose answer was known

Four A3 anchors reappear inside Tier B as cited works: the three monographs the resolver refused (it could not distinguish them from their own reviews) and one version duplicate. Their correct routing is known independently, so they are a live test of the screen.

| record | expected cell | screened cell | agree |
|---|---|---|---|
| `W1672120424` | `THEORY_PROXIMATE_DETERMINANTS` | `THEORY_PROXIMATE_DETERMINANTS` | yes |
| `W1999725017` | `THEORY_PROXIMATE_DETERMINANTS` | `THEORY_PROXIMATE_DETERMINANTS` | yes |
| `W2093319181` | `THEORY_PROXIMATE_DETERMINANTS` | `THEORY_PROXIMATE_DETERMINANTS` | yes |
| `W45210384` | `PARAMETER_LOSS_LEVEL` | `PARAMETER_LOSS_LEVEL` | yes |

The citation frame recovered what the anchor resolver could not. Wood 1994, Leridon 1977 and Bongaarts & Potter 1983 all failed A3's book gate — correctly, since every same-title record there was a review — and all three are present in Tier B because the works that cite them are. The theory canon is therefore intact despite four unresolved anchors, and the OpenAlex ids recovered here should be written back into the anchor file rather than left as an open gap.

## Validation 2 — decoy containment

12 screened records depend only on a routing-decoy seed. Of those, **6 (50%) were routed away** as NOT_RELEVANT. The decoys were forward-cited like every other seed, per the D.2.d correction, so their neighbourhoods entered the frame by design; the walls then had to do the work of excluding them, and this figure is how much work they did.

## What the screen deliberately did not decide

No record carries an estimand level. `ACCOUNTING_SHARE` versus `BEHAVIORAL_NET` is a modelling fact that abstracts of decomposition papers do not state, and it is the field that decides poolability, so it is set at full-text extraction and nowhere earlier. Records whose routing turned on Wall 2 or Wall 5 without the margin being named took `ROUTING_DEFERRED_TO_FULLTEXT` rather than a substantive off-cell.

## Next

`extraction/fetal-loss-intrauterine-mortality-ra-gate.csv` carries the 31 records a human must adjudicate: every primary-cell record plus everything held at a MIXED or DEFERRED cell. The RA verdict is the inclusion decision; the three deterministic signals only feed it.
