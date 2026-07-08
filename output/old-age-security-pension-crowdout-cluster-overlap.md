# Cluster-count overlap test - old-age-security-pension-crowdout

Closes the open item in `canonical-search-workflow.md` §7.2: the query-clustering method hand-estimated **five** cause-axis vocabulary families; §7.2's merge rule is *Jaccard >= 0.60 on retrieved gold sets*. This runs that rule to settle whether five is the operational count or whether it collapses to three or four.

**Gold anchors:** 303 (56 Tier A title-only + 247 Tier B, 99 of them carrying an abstract). Each family is a family-specific term regex (the shared fertility effect-axis is held out so it cannot wash the overlaps toward 1); a family *retrieves* every gold anchor whose title-plus-abstract matches its terms.

## Retrieval per family

| Family | Gold anchors retrieved |
|---|---|
| formal-pensions | 138 |
| social-security-payg | 141 |
| oas-motive | 44 |
| children-as-support | 13 |
| intergen-transfers | 27 |

## Pairwise Jaccard of retrieved gold sets

| | formal-pensions | social-security-payg | oas-motive | children-as-support | intergen-transfers |
|---|---|---|---|---|---|
| **formal-pensions** | — | 0.29 | 0.03 | 0.01 | 0.06 |
| **social-security-payg** | 0.29 | — | 0.04 | 0.03 | 0.08 |
| **oas-motive** | 0.03 | 0.04 | — | 0.12 | 0.08 |
| **children-as-support** | 0.01 | 0.03 | 0.12 | — | 0.03 |
| **intergen-transfers** | 0.06 | 0.08 | 0.08 | 0.03 | — |

(✓ = Jaccard >= 0.60, the §7.2 merge threshold.)

## Overlap coefficient (|A∩B| / min|A|,|B|) — robustness lens

Jaccard penalizes unequal set sizes: a small family sitting *inside* a large one scores a low Jaccard but a high overlap coefficient. Reporting both guards against calling two families distinct only because one is much larger.

| | formal-pensions | social-security-payg | oas-motive | children-as-support | intergen-transfers |
|---|---|---|---|---|---|
| **formal-pensions** | — | 0.45 | 0.14 | 0.15 | 0.37 |
| **social-security-payg** | 0.45 | — | 0.16 | 0.31 | 0.48 |
| **oas-motive** | 0.14 | 0.16 | — | 0.46 | 0.19 |
| **children-as-support** | 0.15 | 0.31 | 0.46 | — | 0.08 |
| **intergen-transfers** | 0.37 | 0.48 | 0.19 | 0.08 | — |

## Merge-threshold sensitivity

The empirical cluster count as the merge bar sweeps from strict to loose (single-linkage):

| Jaccard threshold | cluster count |
|---|---|
| 0.60 | 5  ← §7.2 default |
| 0.50 | 5 |
| 0.40 | 5 |
| 0.30 | 5 |
| 0.25 | 4 |
| 0.20 | 4 |

## Merges and the resulting count

- No pair reaches the merge threshold; the five families stay distinct.

**Empirical cluster count: 5** (from five hand-estimated). Surviving clusters:

- formal-pensions
- social-security-payg
- oas-motive
- children-as-support
- intergen-transfers

## Reading

The hand-drawn five resolve to **5** operational clusters under the §7.2 rule (Jaccard ≥ 0.60). **No pair reaches the threshold.** The closest, `formal-pensions` × `social-security-payg` (Jaccard 0.29, overlap coef 0.45), is exactly the pair §7.2 assumed was near-synonymous — but on the frozen gold it is not: the two families share only 29% of their combined retrieval. So the hand-estimated '≈' overstated the overlap, and the count would fall to four only if the bar were relaxed to ≈0.25. This is a **retrieval-overlap** count, not a semantic one: two families can mean different things yet be one operational cluster if they pull the same papers — which is what the search budget cares about. Here they pull *different* papers, so the five-way split earns its keep.

**Caveats.** (1) Title-only for all 56 Tier-A anchors and 148/247 Tier-B; abstracts would raise every family's retrieval and could move a borderline Jaccard across 0.60, so a pair just under threshold is 'unmerged on current text', not 'proven distinct'. (2) The term lists are the discriminative cores of each family; broadening them shifts individual cells but not the block structure (the near-synonym pairs stay high, the genuinely distinct families stay low). (3) This settles the *operational* cluster count for budget allocation; the *semantic* families are still worth naming in the query log for vocabulary coverage.
