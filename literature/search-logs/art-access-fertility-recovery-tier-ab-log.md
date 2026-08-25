# A4 Tier A / Tier B citation frame — art-access-fertility-recovery (A.17)

**Tier A: 22 seeding anchors** — 6 arm-1 (accounting), 6 arm-2 (access), plus exposure-series, P6 and routing-decoy seeds.

**The two arms' recall denominators are reported separately and are never summed.** Arm 1 counts ART births and is an UPPER BOUND on the registry claim; arm 2 estimates the response to access and is a lower one. A single recall figure across both would be a recall figure for no estimand at all.

**Tier B frame: 7,589 deduplicated records** — 645 found by more than one seed, 5,065 carrying an abstract (67%).

**Records depending ONLY on a routing-decoy seed: 2,754** (36%). `seed_ids` provenance is retained on every Tier B record so Recall(B) can be recomputed without them.

**Failed requests: 0** — listed at the foot. A failed request is not an empty result, and the frame is smaller than the index by exactly what those failures cost.

## The strict-vocabulary ruling, re-tested at scale

The scope ruled that the diagnostic vocabulary and the retrieval vocabulary are separate objects — the strict population vocabulary scores the clinical decoy cloud at 0.1% but loses the canon. **That ruling rested on eight hand-picked works, which is the same eight that motivated it.** A fix verified on the cases that motivated it is verified against nothing, so it is re-measured here on every anchor and every frame record.

**On the anchors' own records:**

| Vocabulary | Empirical anchors reached | of 12 |
|---|---|---|
| LOOSE (retrieval) | 12 | 100% |
| STRICT (diagnostic) | 4 | 33% |

**On the frame:**

| Vocabulary | Tier B records carrying it | Primary cell (ACCESS x outcome) |
|---|---|---|
| LOOSE | 4,221 (55.6%) | 148 |
| STRICT | 145 (1.9%) | 2 |

## Wall 5, measured

The scope declares Wall 5 unenforceable at title/abstract: 'fertility preservation' does not say whether the indication was oncological or elective, and v5's claim names elective egg freezing while the literature is overwhelmingly oncological. Across the **910 preservation records in the frame**:

| Indication named in title/abstract | n | share |
|---|---|---|
| Oncological only | 693 | 76.2% |
| Elective only | 46 | 5.1% |
| Both | 19 | 2.1% |
| **NEITHER — the unenforceable population** | **152** | **16.7%** |

The last row is the number that decides whether Wall 5 is a screen rule or a full-text routing rule. A small share means the wall can be enforced at title/abstract after all and the scope over-declared; a large one means every such record costs a full-text read and the scope was right to say so in advance rather than discover it at extraction.

## Is the arm-1 / arm-2 split really invisible?

The scope declares that whether a paper COUNTS ART births or ESTIMATES a response to access is decided in the methods section and cannot be screened. If that holds, identification vocabulary should be about as sparse in arm-1 neighbourhoods as in arm-2 ones.

| | records reachable | carries identification language | carries counting language |
|---|---|---|---|
| Arm 1 (accounting) seeds | 1,051 | 1.4% | 3.9% |
| Arm 2 (access) seeds | 484 | 5.6% | 6.0% |

A large gap in the identification column means the split is PARTLY visible and the screen can carry some of the routing load; a small one confirms the scope and the routing stays a full-text decision. Reported either way, including against the scope, which is the only reason to measure it.

## Per-seed yield

Every fraction is a SEED-SELECTION DIAGNOSTIC computed after retrieval. None is applied as a filter: filtering the forward fetch by topic vocabulary would prune Tier B by distance from the production query and make Recall(B) circular.

`art` = ART/treatment vocabulary. `acc` = an ACCESS exposure. **`loose`** and **`strict`** are the two outcome vocabularies. **`PRIM`** = ACCESS and a LOOSE outcome; **`sPRIM`** the same under STRICT. `id` and `cnt` are the arm-2 and arm-1 shapes. `clin`, `safe`, `mult` and `etio` measure Walls 1, 2, 3 and 4. All are LOWER BOUNDS.

| seed | cell | back | fwd | total | trunc | art | acc | loose | strict | **PRIM** | n | **sPRIM** | n | id | cnt | clin | safe | mult | etio |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| International Committee for Monitoring Assisted Re | `EXPOSURE_SERIES` | 6 | 1835 | 1835 | no | 44.3% | 2.3% | 60.2% | 0.3% | **1.7%** | 31 | **0.0%** | 0 | 5.1% | 1.5% | 18.4% | 7.4% | 3.4% | 7.0% |
| Fertility Preservation for Patients With Cancer: A | `OFF_ONCOFERTILITY` | 108 | 1608 | 1608 | no | 11.8% | 1.6% | 69.3% | 0.4% | **1.4%** | 23 | **0.0%** | 0 | 1.5% | 1.6% | 11.7% | 1.5% | 0.2% | 0.7% |
| Perinatal outcome of singletons and twins after as | `OFF_SAFETY` | 41 | 1097 | 1097 | no | 72.7% | 1.5% | 33.1% | 0.4% | **1.0%** | 11 | **0.0%** | 0 | 4.0% | 5.1% | 10.5% | 47.3% | 30.4% | 0.5% |
| ART in Europe, 2014: results generated from Europe | `EXPOSURE_SERIES` | 21 | 631 | 631 | no | 72.6% | 1.7% | 42.2% | 1.0% | **0.6%** | 4 | **0.0%** | 0 | 2.2% | 3.8% | 34.7% | 17.1% | 11.6% | 1.4% |
| Assisted Reproductive Technology Surveillance - Un | `EXPOSURE_SERIES` | 71 | 524 | 524 | no | 66.0% | 2.5% | 41.0% | 0.2% | **1.9%** | 10 | **0.0%** | 0 | 2.5% | 5.9% | 17.4% | 25.2% | 20.8% | 0.8% |
| Can assisted reproduction technology compensate fo | `P4_POSTPONEMENT_RECOVERY` | 29 | 519 | 519 | no | 33.3% | 1.0% | 59.0% | 10.6% | **1.0%** | 5 | **0.2%** | 1 | 1.3% | 4.4% | 10.2% | 5.4% | 2.3% | 2.1% |
| Fertility awareness and parenting attitudes among  | `P6_INDUCED_POSTPONEMENT` | 35 | 284 | 284 | no | 26.4% | 1.8% | 82.7% | 8.5% | **1.4%** | 4 | **0.0%** | 0 | 2.8% | 0.7% | 6.3% | 0.7% | 0.4% | 1.4% |
| Health disparities and infertility: impacts of sta | `P1_MANDATE` | 14 | 215 | 215 | no | 48.4% | 19.5% | 68.4% | 1.9% | **14.4%** | 31 | **0.0%** | 0 | 2.8% | 2.3% | 1.4% | 1.4% | 5.6% | 4.7% |
| The impact of a decline in fecundity and of pregna | `P4_POSTPONEMENT_RECOVERY` | 58 | 151 | 151 | no | 27.8% | 2.0% | 63.6% | 13.9% | **2.0%** | 3 | **0.0%** | 0 | 1.3% | 6.0% | 3.3% | 4.0% | 3.3% | 7.9% |
| Realizing a desired family size: when should coupl | `P4_POSTPONEMENT_RECOVERY` | 38 | 144 | 144 | no | 27.1% | 2.8% | 68.8% | 11.1% | **2.8%** | 4 | **0.7%** | 1 | 2.8% | 4.2% | 8.3% | 4.2% | 2.1% | 0.7% |
| Insurance mandates and trends in infertility treat | `P1_MANDATE` | 10 | 132 | 132 | no | 69.7% | 28.0% | 64.4% | 1.5% | **18.9%** | 25 | **0.0%** | 0 | 2.3% | 10.6% | 4.5% | 15.9% | 20.5% | 1.5% |
| The effect of postponement of first motherhood on  | `P4_POSTPONEMENT_RECOVERY` | 32 | 131 | 131 | no | 21.4% | 2.3% | 72.5% | 12.2% | **2.3%** | 3 | **0.0%** | 0 | 2.3% | 6.1% | 3.8% | 3.1% | 2.3% | 0.0% |
| Assisted Reproductive Technology in Europe: Usage  | `EXPOSURE_SERIES` | 53 | 124 | 124 | no | 58.1% | 9.7% | 46.8% | 2.4% | **8.1%** | 10 | **0.0%** | 0 | 0.0% | 5.6% | 1.6% | 3.2% | 3.2% | 0.0% |
| Attitudes toward parenthood and awareness of ferti | `P6_INDUCED_POSTPONEMENT` | 18 | 120 | 120 | no | 23.3% | 2.5% | 84.2% | 12.5% | **1.7%** | 2 | **0.0%** | 0 | 1.7% | 0.8% | 8.3% | 0.8% | 0.0% | 1.7% |
| The effects of insurance mandates on choices and o | `P1_MANDATE` | 28 | 91 | 91 | no | 81.3% | 29.7% | 72.5% | 5.5% | **22.0%** | 20 | **1.1%** | 1 | 7.7% | 18.7% | 7.7% | 17.6% | 25.3% | 1.1% |
| The Contribution of Assisted Reproduction to Compl | `P3_ART_SHARE` | 37 | 71 | 71 | no | 42.3% | 2.8% | 74.6% | 23.9% | **2.8%** | 2 | **0.0%** | 0 | 0.0% | 15.5% | 0.0% | 2.8% | 1.4% | 1.4% |
| The contribution of assisted reproductive technolo | `P3_ART_SHARE` | 36 | 34 | 34 | no | 61.8% | 17.6% | 82.4% | 26.5% | **17.6%** | 6 | **2.9%** | 1 | 0.0% | 20.6% | 0.0% | 5.9% | 0.0% | 0.0% |
| Infertility Insurance Mandates and Fertility | `P1_MANDATE` | 13 | 34 | 34 | no | 67.6% | 50.0% | 82.4% | 8.8% | **47.1%** | 16 | **5.9%** | 2 | 11.8% | 5.9% | 0.0% | 0.0% | 11.8% | 0.0% |
| Infertility Insurance Mandates and Multiple Births | `ROUTE_TO_A12` | 39 | 31 | 31 | no | 64.5% | 25.8% | 58.1% | 6.5% | **16.1%** | 5 | **3.2%** | 1 | 22.6% | 6.5% | 3.2% | 12.9% | 3.2% | 0.0% |
| Elective single embryo transfer versus double embr | `OFF_CLINICAL` | 0 | 24 | 24 | no | 87.5% | 8.3% | 41.7% | 0.0% | **4.2%** | 1 | **0.0%** | 0 | 8.3% | 8.3% | 20.8% | 20.8% | 58.3% | 0.0% |
| Coverage of infertility treatment and fertility ou | `P1_MANDATE` | 34 | 20 | 20 | no | 65.0% | 20.0% | 70.0% | 15.0% | **20.0%** | 4 | **5.0%** | 1 | 20.0% | 15.0% | 5.0% | 0.0% | 5.0% | 0.0% |
| The Economics of Infertility: Evidence from Reprod | `P1_MANDATE` | 60 | 7 | 7 | no | 42.9% | 0.0% | 57.1% | 14.3% | **0.0%** | 0 | **0.0%** | 0 | 14.3% | 14.3% | 0.0% | 0.0% | 0.0% | 0.0% |
## DOI-less seed recovery

A DOI-less anchor cannot seed, so each got ONE recovery attempt gated by first-author agreement, with the type restriction inverted rather than dropped. A.17's one DOI-less anchor is the deliberate negative control from A3 — the `Anonymous`-authored eSET title — and it SHOULD fail to recover.

| anchor | book? | recovered | record | cites |
|---|---|---|---|---|
| Elective single embryo transfer and multiple birth rates | no | no | no non-bookish record with first-author agreement | — |

## Truncation

No seed was truncated; the frame is a complete one-hop neighbourhood of the verified anchors.

## Findings

- **THE LOOSE-FRAME RULING IS CONFIRMED, AND THE EIGHT-CASE CHECK UNDERSTATED THE PROBLEM.** `186_` found the strict vocabulary losing 5 of 8 hand-picked works. Measured on every empirical anchor and the whole frame: the strict vocabulary reaches **4 of 12 anchors** (loose reaches all 12), and finds **2 primary-cell records in a 7,589-record frame** against loose's 148. A strict frame would have lost 8 anchors and returned a primary cell of essentially nothing. The scope was not over-corrected off a small sample; the small sample was the optimistic end.
- **The two largest arm-2 clouds are where it is starkest.** The Bitler & Schmidt and Henne & Bundorf neighbourhoods carry population vocabulary at 68% and 64% loose against **2% strict**, and their strict primary cells are ZERO. The economics-of-access literature does not use demographers' words for demographers' quantities, and a frame built on those words does not merely rank it low — it does not contain it.
- **Wall 5 is 83% enforceable at title/abstract, not unenforceable.** Of 910 preservation records, 693 (76%) name an oncological indication and 46 (5%) name an elective one. **152 (17%) name neither** — that residue is the full-text routing cost, and it is a sixth of the population rather than all of it. The scope's blanket declaration should be narrowed to the residue: the wall IS a screen rule, with an `INSUFFICIENT_INFO` bucket sized at about one record in six.
- **And the elective cell is small enough to change PI call 2.** Only 46 records in the entire frame name an elective indication without an oncological one. v5's claim names egg freezing; the literature that could speak to it at a population level is roughly fifty records before screening. That is a finding for the call, not an argument against making it — but it should be made knowing the cell is likely to come back near-empty.
- **The arm-1/arm-2 split is partly visible after all, in one direction only.** Identification vocabulary runs 1.4% in arm-1 neighbourhoods against 5.6% in arm-2 ones — a 3.9x ratio — while counting vocabulary is nearly flat (3.9% against 6.0%). So identification language is a usable POSITIVE signal: a record carrying it is disproportionately arm 2. It is not a filter — 94% of arm-2's own neighbourhood carries none of it, so its absence means nothing. **The scope was right that the split cannot be screened OUT and wrong that it is invisible.** The screen gets a routing PRIOR it did not expect to have; the routing decision still happens at full text.
- **The frame is complete and unbounded.** No seed truncated, 0 requests failed, and the empirical seeds took an uncapped pull. 2,754 of 7,589 records (36%) depend only on a routing-decoy seed and can be removed from any recall computation via `seed_ids`.
- **The negative control did not recover.** The `Anonymous`-authored eSET title, carried from A3 as a deliberate under-specified candidate, found no non-bookish record with first-author agreement. The recovery path did not invent a seed for it.

