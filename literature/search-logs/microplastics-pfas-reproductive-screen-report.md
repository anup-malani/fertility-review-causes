# Screen report — microplastics-pfas-reproductive (B.6)

**Screened: 920** records — the D1 budget slice plus the both-axes completeness bypass — out of a 14,296-record deduplicated frame.

| tier | definition | n |
|---|---|---|
| 1 | RELEVANT, found through more than one channel or seed | 279 |
| 2 | RELEVANT, single channel | 154 |
| 3 | UNCERTAIN, retained for audit only | 25 |
| — | NOT_RELEVANT, excluded | 462 |

**Primary-cell records: 30** · **fertility-INPUT records (semen, ovarian): 70** · **support stream: 302** · **held for full-text adjudication: 56**

## The two families, counted

This is the chapter's central result and it is a count rather than an estimate. Call 1 split B.6 into two chapters on the argument that its halves have incompatible evidence bases. The screen measures that argument.

| cell group | pfas | plastic | both | none/unclear |
|---|---|---|---|---|
| PRIMARY (a fertility quantity) | 19 | 10 | 1 | 0 |
| INPUT (semen / ovarian parameter) | 62 | 7 | 0 | 1 |

## Cell distribution

| cell | n |
|---|---|
| `OFF_ANIMAL` | 174 |
| `OFF_OUTCOME` | 118 |
| `PARAMETER_EXPOSURE` | 98 |
| `PARAMETER_PHARMACOKINETIC` | 68 |
| `OFF_OTHER` | 50 |
| `MECHANISM_INVITRO` | 46 |
| `OFF_PREGNANCY_SAFETY` | 46 |
| `OFF_ENVIRONMENTAL_FATE` | 44 |
| `OVARIAN_PARAMETER` | 42 |
| `MIXTURE_UNSEPARABLE` | 31 |
| `SEMEN_PARAMETER` | 28 |
| `DETECTION_TISSUE` | 28 |
| `MEASUREMENT_METHOD` | 25 |
| `PRIMARY_EXPOSURE_TO_FERTILITY` | 24 |
| `INSUFFICIENT_INFO` | 24 |
| `OUTCOME_TREND_UNATTRIBUTED` | 23 |
| `OFF_LEGACY_EDC_B2` | 17 |
| `OFF_ART_A17` | 13 |
| `PARAMETER_DETERMINANT_TO_LOSS` | 9 |
| `PRIMARY_MALE_FECUNDITY` | 6 |
| `REVERSE` | 5 |
| `ROUTING_DEFERRED_TO_FULLTEXT` | 1 |

## Validation 1 — anchor recovery on records whose answer was known


| record | expected cell | screened cell | agree |
|---|---|---|---|
| `W2908713169` | `PRIMARY_EXPOSURE_TO_FERTILITY` | `PRIMARY_EXPOSURE_TO_FERTILITY` | yes |
| `W2315733616` | `PRIMARY_EXPOSURE_TO_FERTILITY` | `PRIMARY_EXPOSURE_TO_FERTILITY` | yes |
| `W2329639071` | `OFF_ANIMAL` | `OFF_ANIMAL` | yes |
| `W4309099580` | `OUTCOME_TREND_UNATTRIBUTED` | `OUTCOME_TREND_UNATTRIBUTED` | yes |

## Validation 2 — decoy containment

51 screened records depend on a routing-decoy seed alone. The screen routed **45 of them away** (88%). A screen that admitted a decoy's neighbourhood wholesale would not be enforcing the walls; one that rejected all of it would mean the decoys were badly chosen, since a decoy sits beside the boundary cases the walls exist to adjudicate.

## Validation 3 — chemical-family agreement, D1 versus the blind screener

D1 assigned the family deterministically from the named compound. The screener assigned it independently, without seeing D1's tag. They agree on **857 of 920 records (93%)**.

| D1 tag | screener | n |
|---|---|---|
| `pfas` | `pfas` | 484  |
| `plastic` | `plastic` | 285  |
| `none` | `none` | 81  |
| `pfas` | `unclear` | 30  ← disagree |
| `pfas` | `both` | 10  ← disagree |
| `both` | `both` | 7  |
| `plastic` | `both` | 7  ← disagree |
| `none` | `unclear` | 6  ← disagree |
| `plastic` | `unclear` | 4  ← disagree |
| `both` | `unclear` | 3  ← disagree |
| `plastic` | `none` | 2  ← disagree |
| `pfas` | `none` | 1  ← disagree |

## Validation 4 — shadow records inside Tier B

**10 screened records carry a shadow qualifier in their title.** The A3 gate protects the ANCHOR set; nothing protected Tier B, and the D1 title-collapse groups on the full normalised title, so a record titled *'Reviewer #2 (Public Review): X'* does not collapse onto *X*. Each of these is a separately-DOI'd row that an extraction stage would otherwise count as a study.

| qualifier shape | n |
|---|---|
| `peer-review-n` | 4 |
| `reviewer-public-review` | 3 |
| `retraction` | 1 |
| `comment-on` | 1 |
| `author-response` | 1 |

The two open-peer-review shapes — `reviewer-public-review` and `peer-review-n` — are new here and are the highest-multiplicity ones seen in any chapter: one eLife paper occupies six rows in this frame and one PeerJ review occupies four. They belong in `SHADOW_QUALIFIERS` in the A3 resolver, and the title-collapse in D1 should strip a leading qualifier before grouping.

Records:

- `author-response` — Author Response: Microplastics are present in women’s and cows’ follicular fluid and polystyrene  (W4380323250, tier 0)
- `comment-on` — Comment on: “Microplastic presence in dog and human testis and its potential association with sp  (W4403920235, tier 0)
- `peer-review-n` — Peer Review #1 of "Harmful effects of the microplastic pollution on animal health: a literature   (W4283118244, tier 0)
- `peer-review-n` — Peer Review #3 of "Harmful effects of the microplastic pollution on animal health: a literature   (W4283120283, tier 0)
- `peer-review-n` — Peer Review #1 of "Harmful effects of the microplastic pollution on animal health: a literature   (W4283121128, tier 0)
- `peer-review-n` — Peer Review #2 of "Harmful effects of the microplastic pollution on animal health: a literature   (W4283121386, tier 0)
- `retraction` — RETRACTED: Prenatal and early postnatal exposure to perfluoroalkyl substances and bone mineral c  (W4285603631, tier 0)
- `reviewer-public-review` — Reviewer #1 (Public Review): Microplastics are present in women’s and cows’ follicular fluid and  (W4380354200, tier 0)
- `reviewer-public-review` — Reviewer #2 (Public Review): Microplastics are present in women’s and cows’ follicular fluid and  (W4380360316, tier 0)
- `reviewer-public-review` — Reviewer #3 (Public Review): Microplastics are present in women’s and cows’ follicular fluid and  (W4380368739, tier 0)
