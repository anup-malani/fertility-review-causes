# Cluster-count overlap test (section 7.2) - climate-anxiety-eco-doomerism

The binding retrieval-overlap test, now run on the frozen gold. A2 fixed **five** provisional cause-axis families; the section 7.2 merge rule is *Jaccard >= 0.60 on retrieved gold sets*. This settles whether five is the operational count or collapses.

**Gold:** 234 papers (RELEVANT screen verdicts + Tier-A seeds), 200 with abstracts. Each family is a CAUSE-side term regex; the shared fertility/reproductive/intention EFFECT axis is held out so it cannot wash overlaps toward 1. A family *retrieves* every gold paper whose title+abstract matches its terms.

Theory records are included here, unlike the recall work in steps 79 and 80. This test is about cause-axis vocabulary structure rather than empirical recall, and the theory stream is a genuine part of that axis.

## Retrieval per family

| Family | Gold retrieved |
|---|---|
| climate-anxiety-construct | 87 |
| habitability-future-fear | 13 |
| carbon-ethics-antinatalism | 63 |
| eco-doom-pessimism | 15 |
| reproductive-decision-motivation | 50 |

## Pairwise Jaccard of retrieved gold sets

| | climate-anxiety-construct | habitability-future-fear | carbon-ethics-antinatalism | eco-doom-pessimism | reproductive-decision-motivation |
|---|---|---|---|---|---|
| **climate-anxiety-construct** | - | 0.09 | 0.06 | 0.04 | 0.21 |
| **habitability-future-fear** | 0.09 | - | 0.06 | 0.17 | 0.09 |
| **carbon-ethics-antinatalism** | 0.06 | 0.06 | - | 0.07 | 0.12 |
| **eco-doom-pessimism** | 0.04 | 0.17 | 0.07 | - | 0.10 |
| **reproductive-decision-motivation** | 0.21 | 0.09 | 0.12 | 0.10 | - |

(merge = Jaccard >= 0.60, the section 7.2 threshold.)

## Overlap coefficient (intersection over min set size) - robustness lens

| | climate-anxiety-construct | habitability-future-fear | carbon-ethics-antinatalism | eco-doom-pessimism | reproductive-decision-motivation |
|---|---|---|---|---|---|
| **climate-anxiety-construct** | - | 0.62 | 0.13 | 0.27 | 0.48 |
| **habitability-future-fear** | 0.62 | - | 0.31 | 0.31 | 0.38 |
| **carbon-ethics-antinatalism** | 0.13 | 0.31 | - | 0.33 | 0.24 |
| **eco-doom-pessimism** | 0.27 | 0.31 | 0.33 | - | 0.40 |
| **reproductive-decision-motivation** | 0.48 | 0.38 | 0.24 | 0.40 | - |

## Merge-threshold sensitivity

| Jaccard threshold | cluster count |
|---|---|
| 0.60 | 5  <- section 7.2 default |
| 0.50 | 5 |
| 0.40 | 5 |
| 0.30 | 5 |
| 0.25 | 5 |
| 0.20 | 4 |

## Merges and resulting count

- No pair reaches the merge threshold; the five families stay distinct.

**Empirical cluster count: 5** (from five hand-estimated). Surviving clusters:

- climate-anxiety-construct
- habitability-future-fear
- carbon-ethics-antinatalism
- eco-doom-pessimism
- reproductive-decision-motivation

## A2's design-time predictions, scored

A2 predicted the affective-dread TRIPLE would merge and that `carbon-ethics-antinatalism` would stay distinct, giving an honest expectation of **3** operational clusters.

| A2 prediction | test | outcome |
|---|---|---|
| triple (anxiety, habitability, eco-doom) merges | all three pairwise Jaccards >= 0.60 | FALSIFIED (climate-anxiety-construct x eco-doom-pessimism = 0.04; climate-anxiety-construct x habitability-future-fear = 0.09; eco-doom-pessimism x habitability-future-fear = 0.17) |
| `carbon-ethics-antinatalism` stays distinct | max Jaccard against any other family | CONFIRMED (max 0.12) |
| operational count = 3 | empirical count | FALSIFIED (got 5) |

## Reading

The A2 five resolve to **5** operational clusters under the section 7.2 rule (Jaccard >= 0.60). The closest pair is `climate-anxiety-construct` x `reproductive-decision-motivation` (Jaccard 0.21, overlap 0.48).

This is a retrieval-overlap count, not a semantic one. Two families can mean different things and still be one operational cluster if they pull the same papers; where they pull different papers, the split earns its keep for search-budget allocation.

**Caveats.** (1) Retrieval is on title+abstract, and the 34 title-only gold papers under-retrieve, so a borderline pair may read as 'unmerged on current text'. (2) Term lists are discriminative cores; broadening them shifts cell membership but not the block structure. (3) This is the *operational* count for budget allocation; the semantic families remain worth naming for vocabulary coverage.
