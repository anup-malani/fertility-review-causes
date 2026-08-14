# A4 Tier A / Tier B citation frame — microplastics-pfas-reproductive (B.6)

**Tier A: 32 verified anchors** (6 empirical primary-cell, the causal recall denominator — the three channel-1 systematic reviews sit in a primary cell but are excluded from that count, because a review estimates nothing and counting it would flatter every recall figure downstream).

**Tier B frame: 14,561 deduplicated records** — 3,234 found by more than one seed, 8,691 carrying an abstract (60%).

**Records depending ONLY on a routing-decoy seed: 1,849** (13%). Under the inherited rule these would not exist, because decoys were never forward-cited. They are retained, and `seed_ids` provenance lets Recall(B) be recomputed without them as a sensitivity check.

**Failed requests: 0** — listed at the foot. A failed request is not an empty result, and the frame is smaller than the index by exactly the amount those failures cost.

## Per-seed yield

Both fractions are SEED-SELECTION DIAGNOSTICS computed after retrieval. Neither is applied as a filter on the frame: filtering the forward fetch by topic vocabulary would prune Tier B by distance from the production query and make Recall(B) circular.

`on-topic` = share of the forward cloud carrying any fertility-quantity term. `animal >=` = share visibly non-human, and it is a **lower bound** — a study counts only when it names its organism in the title or abstract, and human-cell in-vitro work is not counted here at all (that is Wall 6). Read it as a floor on how hard Wall 5 will bite.

| seed | cell | back | fwd | fwd total | truncated | on-topic | animal >= |
|---|---|---|---|---|---|---|---|
| Plasticenta: First evidence of microplastics in human plac | `DETECTION_TISSUE` | 37 | 2000 | 3294 | **yes** | 2.6% | 19.1% |
| Discovery and quantification of plastic particle pollution | `DETECTION_TISSUE` | 45 | 2000 | 3713 | **yes** | 2.5% | 19.5% |
| Half-Life of Serum Elimination of Perfluorooctanesulfonate | `PARAMETER_PHARMACOKINETIC` | 20 | 2000 | 2012 | **yes** | 5.0% | 21.6% |
| Detection of Various Microplastics in Human Stool | `DETECTION_TISSUE` | 30 | 1895 | 1895 | no | 2.4% | 21.5% |
| Oyster reproduction is affected by exposure to polystyrene | `OFF_ANIMAL` | 70 | 1794 | 1794 | no | 3.6% | 41.5% |
| Temporal trends in sperm count: a systematic review and me | `OUTCOME_TREND_UNATTRIBUTED` | 229 | 1346 | 1346 | no | 77.2% | 16.2% |
| Trends in Exposure to Polyfluoroalkyl Chemicals in the U.S | `PARAMETER_EXPOSURE` | 22 | 767 | 767 | no | 6.4% | 12.9% |
| Detection and characterization of microplastics in the hum | `DETECTION_TISSUE` | 37 | 462 | 462 | no | 15.4% | 21.6% |
| The Minderoo-Monaco Commission on Plastics and Human Healt | `PARAMETER_EXPOSURE` | 1297 | 445 | 445 | no | 2.7% | 6.3% |
| Perfluorinated Alkyl Acids in Blood Serum from Primiparous | `PARAMETER_PHARMACOKINETIC` | 36 | 412 | 412 | no | 5.1% | 11.9% |
| Do Perfluoroalkyl Compounds Impair Human Semen Quality? | `SEMEN_PARAMETER` | 35 | 396 | 396 | no | 27.3% | 15.4% |
| Perfluoroalkyl and polyfluoroalkyl substances (PFAS) and t | `OVARIAN_PARAMETER` | 195 | 392 | 392 | no | 14.3% | 16.3% |
| Maternal levels of perfluorinated chemicals and subfecundi | `PRIMARY_EXPOSURE_TO_FERTILITY` | 29 | 381 | 381 | no | 23.9% | 12.9% |
| Per- and poly-fluoroalkyl substances (PFAS) and female rep | `PARAMETER_PHARMACOKINETIC` | 237 | 329 | 329 | no | 10.6% | 10.0% |
| Microplastic presence in dog and human testis and its pote | `DETECTION_TISSUE` | 25 | 218 | 218 | no | 13.8% | 20.2% |
| Determinants of plasma concentrations of perfluoroalkyl su | `PARAMETER_PHARMACOKINETIC` | 60 | 196 | 196 | no | 20.9% | 7.7% |
| Maternal exposure to perfluorinated chemicals and reduced  | `PRIMARY_EXPOSURE_TO_FERTILITY` | 43 | 181 | 181 | no | 35.4% | 15.5% |
| Perfluoroalkyl and polyfluoroalkyl substances and measures | `PRIMARY_EXPOSURE_TO_FERTILITY` | 60 | 166 | 166 | no | 23.5% | 8.4% |
| Exposure to perfluorinated compounds and human semen quali | `SEMEN_PARAMETER` | 28 | 161 | 161 | no | 46.6% | 20.5% |
| Endocrine Disruption of Androgenic Activity by Perfluoroal | `ENDOCRINE_MECHANISM` | 51 | 151 | 151 | no | 23.2% | 13.9% |
| Perfluorinated Compounds and Subfecundity in Pregnant Wome | `PRIMARY_EXPOSURE_TO_FERTILITY` | 27 | 138 | 138 | no | 30.4% | 7.2% |
| First evidence of microplastics in human ovarian follicula | `DETECTION_TISSUE` | 63 | 116 | 116 | no | 19.0% | 19.0% |
| Nontargeted identification of per- and polyfluoroalkyl sub | `DETECTION_TISSUE` | 53 | 108 | 108 | no | 14.8% | 22.2% |
| Relationship of Perfluorooctanoic Acid Exposure to Pregnan | `OFF_PREGNANCY_SAFETY` | 21 | 107 | 107 | no | 12.1% | 5.6% |
| Perfluoroalkyl substances (PFAS) in drinking water and ris | `PRIMARY_HIGH_EXPOSURE` | 55 | 85 | 85 | no | 22.4% | 8.2% |
| The Role of Peroxisome Proliferator-Activated Receptor Gam | `OFF_LEGACY_EDC_B2` | 77 | 83 | 83 | no | 10.8% | 14.5% |
| Association between perfluorinated compounds and time to p | `PRIMARY_EXPOSURE_TO_FERTILITY` | 29 | 81 | 81 | no | 44.4% | 8.6% |
| Association between chemical mixtures and female fertility | `MIXTURE_UNSEPARABLE` | 57 | 73 | 73 | no | 50.7% | 15.1% |
| The effects of perfluoroalkyl and polyfluoroalkyl substanc | `PRIMARY_EXPOSURE_TO_FERTILITY` | 54 | 66 | 66 | no | 22.7% | 12.1% |
| Persistent organic pollutants and couple fecundability: a  | `PRIMARY_EXPOSURE_TO_FERTILITY` | 144 | 57 | 57 | no | 24.6% | 8.8% |
| Reducing exposure to high levels of perfluorinated compoun | `OFF_PREGNANCY_SAFETY` | 37 | 53 | 53 | no | 24.5% | 5.7% |
| Perfluoroalkyl acids and time to pregnancy revisited: An u | `PRIMARY_EXPOSURE_TO_FERTILITY` | 26 | 39 | 39 | no | 30.8% | 7.7% |

## Truncation

3 seed(s) hit the 2,000-record forward cap and are reported here rather than silently truncated — a bounded pull that is not stated reads as complete coverage:
- **Plasticenta: First evidence of microplastics in human plac** (`DETECTION_TISSUE`): pulled 2,000 of 3,294 citing works, on-topic 2.6% — **1,294 unpulled, an estimated 34 on-topic records not seen.**
- **Discovery and quantification of plastic particle pollution** (`DETECTION_TISSUE`): pulled 2,000 of 3,713 citing works, on-topic 2.5% — **1,713 unpulled, an estimated 42 on-topic records not seen.**
- **Half-Life of Serum Elimination of Perfluorooctanesulfonate** (`PARAMETER_PHARMACOKINETIC`): pulled 2,000 of 2,012 citing works, on-topic 5.0% — **12 unpulled, an estimated 1 on-topic records not seen.**

**Estimated on-topic records lost to the cap in total: ~76**, against a frame of 14,561. All three truncated seeds are low-yield (2.5-5% on-topic), so the cap fell where it costs least — but the estimate assumes the unpulled tail resembles the pulled head, and a cursor-paged truncation cannot guarantee that. Raise the cap and re-run if any of these seeds later turns out to matter for recall.
