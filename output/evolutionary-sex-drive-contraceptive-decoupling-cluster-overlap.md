# Cluster-count overlap test (§7.2) — evolutionary-sex-drive-contraceptive-decoupling

The binding retrieval-overlap test, now run on the frozen gold (A2 gave only the design-time conceptual read). A2 fixed **five** provisional cause-axis families; §7.2's merge rule is *Jaccard >= 0.60 on retrieved gold sets*. This settles whether five is the operational count or collapses to three/four.

**Gold:** 162 papers (RELEVANT screen verdicts + Tier-A seeds), 127 with abstracts. Each family = a CAUSE-side term regex (the shared fertility/reproductive EFFECT axis is held out so it cannot wash overlaps toward 1); a family *retrieves* every gold paper whose title+abstract matches its terms.

## Retrieval per family

| Family | Gold retrieved |
|---|---|
| evolutionary-biosocial-theory | 79 |
| proximate-ultimate | 63 |
| decoupling-severing | 13 |
| childbearing-motivation | 50 |
| contraception-as-technology | 39 |

## Pairwise Jaccard of retrieved gold sets

| | evolutionary-biosocial-theory | proximate-ultimate | decoupling-severing | childbearing-motivation | contraception-as-technology |
|---|---|---|---|---|---|
| **evolutionary-biosocial-theory** | — | 0.33 | 0.10 | 0.14 | 0.18 |
| **proximate-ultimate** | 0.33 | — | 0.10 | 0.10 | 0.11 |
| **decoupling-severing** | 0.10 | 0.10 | — | 0.09 | 0.08 |
| **childbearing-motivation** | 0.14 | 0.10 | 0.09 | — | 0.17 |
| **contraception-as-technology** | 0.18 | 0.11 | 0.08 | 0.17 | — |

(✓ = Jaccard >= 0.60, the §7.2 merge threshold.)

## Overlap coefficient (|A∩B| / min|A|,|B|) — robustness lens

| | evolutionary-biosocial-theory | proximate-ultimate | decoupling-severing | childbearing-motivation | contraception-as-technology |
|---|---|---|---|---|---|
| **evolutionary-biosocial-theory** | — | 0.56 | 0.62 | 0.32 | 0.46 |
| **proximate-ultimate** | 0.56 | — | 0.54 | 0.20 | 0.26 |
| **decoupling-severing** | 0.62 | 0.54 | — | 0.38 | 0.31 |
| **childbearing-motivation** | 0.32 | 0.20 | 0.38 | — | 0.33 |
| **contraception-as-technology** | 0.46 | 0.26 | 0.31 | 0.33 | — |

## Merge-threshold sensitivity

| Jaccard threshold | cluster count |
|---|---|
| 0.60 | 5  ← §7.2 default |
| 0.50 | 5 |
| 0.40 | 5 |
| 0.30 | 4 |
| 0.25 | 4 |
| 0.20 | 4 |

## Merges and resulting count

- No pair reaches the merge threshold; the five families stay distinct.

**Empirical cluster count: 5** (from five hand-estimated). Surviving clusters:

- evolutionary-biosocial-theory
- proximate-ultimate
- decoupling-severing
- childbearing-motivation
- contraception-as-technology

## Reading

The A2 five resolve to **5** operational clusters under the §7.2 rule (Jaccard ≥ 0.60). The closest pair is `evolutionary-biosocial-theory` × `proximate-ultimate` (Jaccard 0.33, overlap 0.56). This is a retrieval-overlap count, not a semantic one: two families can mean different things yet be one operational cluster if they pull the same papers. Where they pull different papers, the split earns its keep for search-budget allocation.

**Caveats.** (1) Retrieval is on title+abstract; the 35 title-only gold papers under-retrieve, so a borderline pair may be 'unmerged on current text'. (2) Term lists are discriminative cores; broadening shifts cells but not the block structure. (3) This is the *operational* count for budget; the semantic families remain worth naming for vocabulary coverage.
