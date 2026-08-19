# D.3.c — discriminative terms (A4)

Fightin'-Words weighted log-odds (informative Dirichlet prior, z-scored) over **title and abstract**: **541** positives against **10,048** negatives. Higher z = more discriminative of the primary-anchor neighbourhood.

**The label is citation provenance, not vocabulary.** A positive is a Tier B record reached by at least one PRIMARY-cell anchor; a negative is reached only by anchors sitting across a boundary wall. Nothing in that partition reads the record's text. Labelling by the despair-and-fertility co-occurrence instead would have mined the words used to draw the line — which in a chapter whose primary cell IS a co-occurrence is not a subtle circularity but the whole result.

**The contrast is relevant-versus-near-miss.** Every negative already passed the citation frame, so this measures precision at fixed recall; the z scores are not comparable to a relevant-versus-random-corpus ranking. B1 recomputes fold-locally so the CV recall estimate stays uncircular.

Abstracts present for **7,140 of 10,589** frame records (67%); mining titles alone would measure which literature writes its mechanism into its title, which is a fact about house style.

Candidate terms (positive count >= 4): **2,341**

| block | terms |
|---|---|
| `MECHANISM_AND_OUTCOME` | 0 |
| `MECHANISM` | 4 |
| `OUTCOME` | 119 |
| `TREATMENT_AND_OUTCOME` | 2 |
| `TREATMENT` | 24 |
| `REVERSE_WALL5` | 0 |
| `MORTALITY_WALL4` | 4 |
| `OTHER` | 2188 |


## `MECHANISM` — top by z

| term | z | log-odds | pos | neg |
|---|---|---|---|---|
| anomie | 5.25 | 2.72 | 7 | 8 |
| optimistic | 2.63 | 1.47 | 4 | 16 |
| future orientation | 0.7 | 9.94 | 6 | 0 |
| despair | -4.44 | -1.9 | 5 | 635 |

## `OUTCOME` — top by z

| term | z | log-odds | pos | neg |
|---|---|---|---|---|
| fertility | 38.17 | 1.48 | 832 | 3324 |
| fertility intentions | 25.9 | 2.51 | 182 | 257 |
| childbearing | 24.56 | 2.11 | 200 | 422 |
| childless | 13.68 | 2.36 | 54 | 88 |
| birth | 13.57 | 1.23 | 145 | 736 |
| childbearing intentions | 13.14 | 3.92 | 44 | 15 |
| childlessness | 12.34 | 2.31 | 45 | 77 |
| births | 11.06 | 1.39 | 78 | 338 |
| parity | 9.19 | 1.8 | 35 | 100 |
| fertility behavior | 8.71 | 2.46 | 21 | 31 |
| nonmarital | 8.45 | 2.74 | 18 | 20 |
| fertility fertility | 8.15 | 2.69 | 17 | 20 |
| birth control | 8.12 | 3.67 | 16 | 7 |
| term fertility | 7.98 | 2.41 | 18 | 28 |
| fertility intention | 7.81 | 2.21 | 19 | 36 |

## `TREATMENT_AND_OUTCOME` — top by z

| term | z | log-odds | pos | neg |
|---|---|---|---|---|
| inequality fertility | 4.5 | 3.76 | 5 | 2 |
| uncertainty fertility | 1.69 | 0.8 | 5 | 39 |

## `TREATMENT` — top by z

| term | z | log-odds | pos | neg |
|---|---|---|---|---|
| income inequality | 7.13 | 1.07 | 52 | 311 |
| economic uncertainty | 6.53 | 1.46 | 25 | 101 |
| economic inequality | 4.93 | 1.36 | 16 | 71 |
| inequality insecurity | 4.49 | 4.79 | 7 | 1 |
| tail inequality | 4.11 | 3.14 | 4 | 3 |
| neighborhood poverty | 4.08 | 4.45 | 5 | 1 |
| inequality social | 3.92 | 2.63 | 4 | 5 |
| uncertainty reduction | 3.79 | 4.23 | 4 | 1 |
| inequality measures | 3.53 | 2.16 | 4 | 8 |
| uncertainty | 3.28 | 0.49 | 48 | 511 |
| uncertainties | 2.59 | 1.15 | 6 | 33 |
| inequality | 2.25 | 0.21 | 123 | 1745 |
| wage inequality | 1.87 | 0.5 | 15 | 158 |
| poverty | 1.59 | 0.3 | 30 | 388 |
| great recession | 1.16 | 0.28 | 19 | 252 |

## `MORTALITY_WALL4` — top by z

| term | z | log-odds | pos | neg |
|---|---|---|---|---|
| avoidable mortality | 4.11 | 3.14 | 4 | 3 |
| cause mortality | -0.53 | -0.27 | 4 | 92 |
| life expectancy | -4.53 | -1.66 | 7 | 684 |
| mortality | -8.27 | -1.37 | 35 | 2508 |

## `OTHER` — top by z

| term | z | log-odds | pos | neg |
|---|---|---|---|---|
| intentions | 38.54 | 2.84 | 365 | 370 |
| child | 24.67 | 2.04 | 211 | 477 |
| family | 22.94 | 1.59 | 265 | 935 |
| children | 22.36 | 1.69 | 230 | 740 |
| women | 17.29 | 1.02 | 330 | 2068 |
| europe | 16.44 | 1.57 | 140 | 507 |
| behaviour | 16.18 | 2.47 | 72 | 105 |
| families | 15.64 | 2.05 | 84 | 187 |
| intention | 15.49 | 2.56 | 64 | 86 |
| hungary | 14.42 | 3.21 | 49 | 34 |
| motherhood | 13.21 | 2.42 | 49 | 75 |
| intended | 13.04 | 2.58 | 45 | 59 |
| teenage | 13.01 | 3.17 | 40 | 29 |
| social | 12.87 | 0.77 | 310 | 2496 |
| reproductive | 12.55 | 1.66 | 74 | 243 |

---

## Does any vocabulary separate the primary cell from the walls?

This is the question A4 was run to answer, and the scope's declaration that Wall 1 is unenforceable at title and abstract stands or falls on it.

**Of the 40 strongest discriminators, 0 carry mechanism vocabulary.**

None. Every one of the forty strongest discriminators is topic, treatment or outcome vocabulary.

### The words the hypothesis is named after

| term | z | pos | neg |
|---|---|---|---|
| `despair` | **-4.44** | 5 | 635 |
| `anomie` | **5.25** | 7 | 8 |

**`despair` is NEGATIVELY discriminative: z -4.44, 5 occurrences in the primary-anchor neighbourhood against 635 in the walls'.** The word this hypothesis is named for is a marker of the literature it must be separated FROM — the deaths-of-despair mortality corpus — and putting it in a production query would pull the search toward the largest decoy cloud the chapter faces (Wall 4) and away from its primary cell. The one precise mechanism term the frame offers is `future orientation` (z 0.7, 6 positive occurrences and 0 negative), which is perfectly precise and far too rare to carry a query.


**And the strongest non-topic discriminators are place names**: `europe` (z 16.44), `hungary` (z 14.42), `poland` (z 11.45). The positive class is the post-communist anomie family, so what most distinguishes the primary neighbourhood from the walls is WHERE its studies were done. A query fitted on this would learn to retrieve Central European demography rather than despair research — which is Call 5's transportability problem appearing inside the query itself, before any synthesis decision is taken.


**Read this against what the walls need.** A term that separates the primary neighbourhood by naming its TOPIC — fertility, intentions, a country, a survey — retrieves the right literature and does nothing to route within it. Only mechanism vocabulary can do Wall 1's work, because Wall 1 is the distinction between a despair mechanism and an uncertainty mechanism over the same treatment and the same outcome. The count above is therefore the measurement, not the term list itself.

