# A4 Tier A / Tier B citation frame — fetal-loss-intrauterine-mortality (B.5)

**Tier A: 25 verified anchors** (8 empirical primary-cell or replacement, the causal recall denominator).

**Tier B frame: 11,504 deduplicated records** — 1,203 found by more than one seed, 8,437 carrying an abstract (73%).

**Records depending ONLY on a routing-decoy seed: 1,888** (16%). Under the inherited rule these would not exist, because decoys were never forward-cited. They are retained, and `seed_ids` provenance lets Recall(B) be recomputed without them as a sensitivity check.

**Failed requests: 0** — listed at the foot. A failed request is not an empty result, and the frame is smaller than the index by exactly the amount those failures cost.

## Per-seed yield

On-topic fraction is a SEED-SELECTION DIAGNOSTIC computed after retrieval. It is never applied as a filter on the frame: filtering the forward fetch by topic vocabulary would prune Tier B by distance from the production query and make Recall(B) circular.

| seed | cell | back | fwd | fwd total | truncated | on-topic |
|---|---|---|---|---|---|---|
| Incidence of Early Loss of Pregnancy | `PARAMETER_LOSS_LEVEL` | 28 | 1200 | 2332 | **yes** | 45.1% |
| Maternal age and fetal loss: population based register lin | `PARAMETER_LOSS_LEVEL` | 24 | 1200 | 1681 | **yes** | 53.6% |
| Miscarriage matters: the epidemiological, physical, psycho | `PARAMETER_LOSS_LEVEL` | 117 | 1200 | 1464 | **yes** | 43.8% |
| Stillbirths: rates, risk factors, and acceleration towards | `PARAMETER_DETERMINANT_TO_LOSS` | 70 | 1200 | 1711 | **yes** | 71.6% |
| A Framework for Analyzing the Proximate Determinants of Fe | `THEORY_PROXIMATE_DETERMINANTS` | 0 | 1200 | 1323 | **yes** | 70.5% |
| National, regional, and worldwide estimates of stillbirth  | `PARAMETER_LOSS_LEVEL` | 33 | 1023 | 1023 | no | 72.3% |
| ESHRE guideline: recurrent pregnancy loss | `OFF_CLINICAL_MANAGEMENT` | 143 | 990 | 990 | no | 46.5% |
| Conception to ongoing pregnancy: the 'black box' of early  | `PARAMETER_LOSS_LEVEL` | 138 | 782 | 782 | no | 41.3% |
| Age and Infertility | `OFF_MATERNAL_AGE_A15` | 35 | 697 | 697 | no | 67.9% |
| Estimates of human fertility and pregnancy loss | `PARAMETER_LOSS_LEVEL` | 14 | 580 | 580 | no | 46.6% |
| The role of infection in miscarriage | `PARAMETER_DETERMINANT_TO_LOSS` | 207 | 442 | 442 | no | 36.9% |
| The hypothesis of reproductive compensation and its assump | `REPLACEMENT_COMPENSATION` | 56 | 190 | 190 | no | 44.2% |
| Embryonic Mortality in Farm Animals | `OFF_ANIMAL` | 0 | 166 | 166 | no | 40.4% |
| Infertility in sub-Saharan Africa: Estimates and Implicati | `OFF_STERILITY_B3` | 0 | 135 | 135 | no | 74.8% |
| Famine, Maternal Nutrition and Infant Mortality: A Re-exam | `PRIMARY_SHOCK_TO_BIRTHS` | 1 | 123 | 123 | no | 32.5% |
| Famine, social disruption, and involuntary fetal loss: Evi | `PRIMARY_SHOCK_TO_BIRTHS` | 85 | 122 | 122 | no | 35.2% |
| Inbreeding Effects on Fertility in Humans: Evidence for Re | `REPLACEMENT_COMPENSATION` | 26 | 120 | 120 | no | 47.5% |
| Short-Term Birth Sequelae of the 1918-1920 Influenza Pande | `PRIMARY_SHOCK_TO_BIRTHS` | 28 | 89 | 89 | no | 71.9% |
| Collecting Data on Pregnancy Loss: A Review of Evidence fr | `MEASUREMENT_METHOD` | 39 | 71 | 71 | no | 69.0% |
| The Effects of Intrauterine Malnutrition on Birth and Fert | `PRIMARY_SHOCK_TO_BIRTHS` | 56 | 54 | 54 | no | 44.4% |
| The effects of family planning and other factors on fertil | `MECHANICAL_ACCOUNTING` | 24 | 51 | 51 | no | 74.5% |
| Death before Birth: Fetal Health and Mortality in Historic | `PARAMETER_LOSS_LEVEL` | 0 | 38 | 38 | no | 50.0% |
| Excess risk of stillbirth during the 1918-1920 influenza p | `PRIMARY_SHOCK_TO_BIRTHS` | 4 | 33 | 33 | no | 57.6% |
| Abortion Legalization in Uruguay: Effects on Adolescent Fe | `OFF_INDUCED_ABORTION_A4` | 43 | 13 | 13 | no | 69.2% |
| Pregnancy Wastage among Married Women in South Korea | `PRIMARY_LOSS_TO_FERTILITY` | 18 | 8 | 8 | no | 87.5% |

## Truncation

5 seed(s) hit the 1,200-record forward cap and are reported here rather than silently truncated — a bounded pull that is not stated reads as complete coverage:
- **Incidence of Early Loss of Pregnancy** (`PARAMETER_LOSS_LEVEL`): pulled 1,200 of 2,332 citing works, on-topic 45.1%.
- **Maternal age and fetal loss: population based register lin** (`PARAMETER_LOSS_LEVEL`): pulled 1,200 of 1,681 citing works, on-topic 53.6%.
- **Miscarriage matters: the epidemiological, physical, psycho** (`PARAMETER_LOSS_LEVEL`): pulled 1,200 of 1,464 citing works, on-topic 43.8%.
- **Stillbirths: rates, risk factors, and acceleration towards** (`PARAMETER_DETERMINANT_TO_LOSS`): pulled 1,200 of 1,711 citing works, on-topic 71.6%.
- **A Framework for Analyzing the Proximate Determinants of Fe** (`THEORY_PROXIMATE_DETERMINANTS`): pulled 1,200 of 1,323 citing works, on-topic 70.5%.
