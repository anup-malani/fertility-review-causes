# D.1.a — discriminative terms (GACS A6a)

Fightin'-Words weighted log-odds (informative Dirichlet prior, z-scored) over **titles**: Tier B + Tier-A empirical anchors (**526** positives) against the snowball's non-relevant residue plus the ten purpose-built decoys (**9972** negatives). Higher z = more discriminative of the on-pair class.

**The contrast is relevant-versus-near-miss, not relevant-versus-random-database.** Every negative already passed the citation frame, so what is measured is precision at fixed recall. A6b recomputes this fold-locally so the CV recall estimate stays uncircular.

**The treatment side is five clusters, not one block** (Ruling 1): the five pairs are estimated separately and never pooled, and a single mined cause block would be ranked by whichever pair dominates the frame — which is S3, at 23 of 31 empirical anchors. Splitting keeps the budget allocation an explicit A6b decision rather than an artifact of frame composition.

Candidate terms (gold count >= 3): **525**

| block | terms |
|---|---|
| `OUTCOME` | 79 |
| `GENERIC_VALUES` | 20 |
| `S1_POSTMATERIALISM` | 5 |
| `S2_INDIVIDUALISM` | 2 |
| `S3_SECULARIZATION` | 44 |
| `S4_CHILDLESSNESS_NORM` | 0 |
| `S5_CONSUMERISM` | 0 |
| `BOTH` | 11 |
| `MULTI_PAIR` | 0 |
| `AMBIGUOUS_MATERIALISM` | 0 |
| `OTHER` | 364 |

Terms flagged as clinical/veterinary collision: **0** — see the exclusion note below.


## `OUTCOME` — top by z

| term | z | log-odds | gold | neg |
|---|---|---|---|---|
| fertility | 28.58 | 1.49 | 438 | 1929 |
| marital fertility | 9.86 | 2.67 | 24 | 31 |
| childbearing | 9.61 | 1.44 | 53 | 238 |
| fertility change | 8.69 | 3.18 | 17 | 13 |
| fertility intentions | 8.35 | 1.65 | 32 | 116 |
| fertility united | 7.59 | 2.73 | 14 | 17 |
| influence fertility | 7.58 | 3.53 | 13 | 7 |
| theories fertility | 5.84 | 2.48 | 9 | 14 |
| fertility behavior | 5.65 | 2.14 | 10 | 22 |
| fertility sub | 5.55 | 3.07 | 7 | 6 |
| children fertility | 5.23 | 4.15 | 7 | 2 |
| fertility europe | 5.19 | 1.78 | 11 | 35 |
| fertility ideals | 5.0 | 2.76 | 6 | 7 |
| fertility related | 4.94 | 4.0 | 6 | 2 |
| attitudes fertility | 4.93 | 5.07 | 9 | 1 |
| fertility behaviour | 4.85 | 2.23 | 7 | 14 |
| fertility western | 4.6 | 3.82 | 5 | 2 |
| childlessness | 4.56 | 1.14 | 18 | 110 |
| fertility decline | 4.43 | 1.1 | 18 | 114 |
| fertility childbearing | 4.22 | 3.2 | 4 | 3 |

## `GENERIC_VALUES` — top by z

| term | z | log-odds | gold | neg |
|---|---|---|---|---|
| cultural | 11.76 | 1.51 | 73 | 305 |
| attitudes | 11.08 | 1.56 | 62 | 248 |
| norms | 9.13 | 1.98 | 29 | 75 |
| value children | 8.65 | 2.17 | 23 | 49 |
| value | 8.37 | 1.54 | 36 | 146 |
| gender attitudes | 6.76 | 2.31 | 13 | 24 |
| second demographic | 6.36 | 1.29 | 28 | 146 |
| ideals | 5.18 | 2.03 | 9 | 22 |
| changing value | 5.13 | 3.6 | 6 | 3 |
| attitude | 5.13 | 1.87 | 10 | 29 |
| preferences | 4.26 | 1.13 | 16 | 99 |
| ideals intentions | 3.87 | 4.28 | 4 | 1 |
| beliefs | 3.53 | 1.19 | 10 | 58 |
| values | 3.52 | 0.72 | 25 | 236 |
| ideal number | 3.5 | 4.0 | 3 | 1 |
| belief | 2.2 | 1.04 | 5 | 34 |
| culture | 2.11 | 0.57 | 14 | 155 |
| ideal | 1.75 | 0.91 | 4 | 31 |
| preference | 1.4 | 0.72 | 4 | 38 |
| preferences changing | 1.2 | 8.13 | 4 | 0 |

## `S1_POSTMATERIALISM` — top by z

| term | z | log-odds | gold | neg |
|---|---|---|---|---|
| ideational | 4.1 | 2.23 | 5 | 10 |
| value orientation | 3.92 | 2.52 | 4 | 6 |
| postmodern | 2.63 | 1.44 | 4 | 18 |
| value orientations | 1.73 | 1.05 | 3 | 20 |
| modernization | -0.01 | -0.01 | 3 | 62 |

## `S2_INDIVIDUALISM` — top by z

| term | z | log-odds | gold | neg |
|---|---|---|---|---|
| autonomy | 6.28 | 2.58 | 10 | 14 |
| female autonomy | 1.34 | 8.13 | 5 | 0 |

## `S3_SECULARIZATION` — top by z

| term | z | log-odds | gold | neg |
|---|---|---|---|---|
| religion | 16.64 | 1.61 | 132 | 503 |
| religiosity | 11.79 | 1.88 | 52 | 149 |
| affiliation | 9.55 | 2.97 | 21 | 20 |
| religious affiliation | 8.95 | 3.24 | 18 | 13 |
| religious | 7.96 | 1.05 | 64 | 432 |
| religiousness | 7.51 | 3.68 | 13 | 6 |
| muslim | 4.16 | 1.23 | 13 | 72 |
| religious groups | 4.04 | 2.7 | 4 | 5 |
| relationship religion | 4.04 | 2.7 | 4 | 5 |
| religion education | 3.87 | 4.28 | 4 | 1 |
| religion determinant | 3.79 | 2.36 | 4 | 7 |
| muslims | 3.58 | 1.83 | 5 | 15 |
| parental religiosity | 3.5 | 4.0 | 3 | 1 |
| influence religious | 3.5 | 4.0 | 3 | 1 |
| religion religiosity | 3.47 | 2.63 | 3 | 4 |
| influence religion | 3.47 | 2.63 | 3 | 4 |
| christian muslim | 3.32 | 2.41 | 3 | 5 |
| religions | 3.27 | 1.33 | 7 | 35 |
| muslim non | 3.18 | 2.23 | 3 | 6 |
| non muslim | 3.18 | 2.23 | 3 | 6 |

## `BOTH` — top by z

| term | z | log-odds | gold | neg |
|---|---|---|---|---|
| voluntary childlessness | 6.47 | 2.49 | 11 | 17 |
| fertility preferences | 5.58 | 1.96 | 11 | 29 |
| religion fertility | 4.25 | 8.13 | 50 | 0 |
| postmodern fertility | 4.19 | 3.6 | 4 | 2 |
| fertility religion | 2.62 | 8.13 | 19 | 0 |
| religiosity fertility | 2.33 | 8.13 | 15 | 0 |
| religiousness fertility | 1.9 | 8.13 | 10 | 0 |
| affiliation fertility | 1.47 | 8.13 | 6 | 0 |
| fertility muslim | 1.2 | 8.13 | 4 | 0 |
| autonomy fertility | 1.2 | 8.13 | 4 | 0 |
| secularity fertility | 1.04 | 8.13 | 3 | 0 |

## `OTHER` — top by z

| term | z | log-odds | gold | neg |
|---|---|---|---|---|
| intentions | 7.6 | 1.33 | 38 | 191 |
| influence | 7.03 | 1.4 | 30 | 141 |
| marital | 6.83 | 1.38 | 29 | 139 |
| children | 6.39 | 0.96 | 48 | 353 |
| cultural dynamics | 6.3 | 4.1 | 10 | 3 |
| economic theories | 6.23 | 3.72 | 9 | 4 |
| voluntary | 5.45 | 1.89 | 11 | 31 |
| cross cultural | 5.19 | 1.68 | 12 | 42 |
| behaviour | 5.14 | 1.27 | 19 | 102 |
| demographic transition | 5.04 | 0.94 | 31 | 232 |
| dynamics economic | 4.93 | 5.07 | 9 | 1 |
| second | 4.91 | 0.93 | 30 | 227 |
| theories | 4.88 | 1.42 | 14 | 64 |
| decline | 4.74 | 0.93 | 28 | 212 |
| roles | 4.68 | 1.65 | 10 | 36 |
| related | 4.66 | 1.47 | 12 | 52 |
| female | 4.64 | 1.24 | 16 | 88 |
| united states | 4.45 | 0.91 | 26 | 202 |
| 1860 | 4.44 | 2.58 | 5 | 7 |
| 1985 | 4.38 | 1.75 | 8 | 26 |

---

## What the block counts mean

**Three of the five pairs have no mineable query vocabulary in this frame, and two have literally none.**

| pair | discriminative terms | strongest term |
|---|---|---|
| `S1_POSTMATERIALISM` | **5** | `ideational` (z 4.1) |
| `S2_INDIVIDUALISM` | **2** | `autonomy` (z 6.28) |
| `S3_SECULARIZATION` | **44** | `religion` (z 16.64) |
| `S4_CHILDLESSNESS_NORM` | **0** | — |
| `S5_CONSUMERISM` | **0** | — |

S3 carries 44 terms topping out at z 16.64; S1's best term reaches 4.1. This is the scope's 'expected shape of the evidence' confirmed by an independent measurement, and it is stronger than the scope predicted.

**Consequence for A6b, and it is the same move D.3.b made for its rare cells.** A query built only on mined terms would be an S3 query with a generic-values annex: S1 and S2 would be reachable only through `GENERIC_VALUES` plus the outcome axis, and S4 and S5 not at all. S4 and S5 therefore need **forced a-priori backbones** rather than mined expansions, exactly as D.3.b forced its carbon-ethics cluster because it was 'conceptually central and empirically rare, so it is forced in rather than left to the mined ranking, which would never surface it.'

### S4 is degenerate, and the term ranker demonstrates it mechanically

Ruling 2 pre-registered the degenerate-pair rule: when the treatment measure and the outcome measure are the same construct, there is no pair. S4's vocabulary is that rule made visible — **every childlessness term in the ranked set classifies as `OUTCOME` or `BOTH`, and none as a pure treatment term**, because there is no S4 treatment word that is not also the outcome word:

- `voluntary childlessness` → `BOTH` (z 6.47, gold 11)
- `childlessness` → `OUTCOME` (z 4.56, gold 18)
- `childlessness europe` → `OUTCOME` (z 2.9, gold 3)
- `attitudes childlessness` → `OUTCOME` (z 1.2, gold 4)
- `childlessness united` → `OUTCOME` (z 1.2, gold 4)
- `childless` → `OUTCOME` (z 0.07, gold 3)

A pre-registered ruling confirmed by an independent measurement is worth more than either alone, and this belongs in the chapter's methods section.

### Perfectly separating conjunctions

Terms with **zero** occurrences in 9,972 negatives and five or more in the positives. These are the outcome × treatment bigrams, and they are why the production query is a conjunction rather than a union of two term lists:

- `religion fertility` — gold 50, neg 0
- `fertility religion` — gold 19, neg 0
- `religiosity fertility` — gold 15, neg 0
- `religion influence` — gold 11, neg 0
- `religiousness fertility` — gold 10, neg 0
- `religion religiousness` — gold 9, neg 0
- `attitudes childbearing` — gold 8, neg 0
- `fertility norms` — gold 7, neg 0
- `spain 1985` — gold 7, neg 0
- `religion spain` — gold 7, neg 0
- `1985 1999` — gold 7, neg 0
- `values fertility` — gold 6, neg 0

**Not all of these are real, and the list shows its own tell.** `spain 1985`, `1985 1999` and `religion spain` separate perfectly at gold 7 because they come from one study's citation neighbourhood, not because they are query vocabulary — perfect separation at a low gold count is the signature of a single-cluster artifact rather than of a discriminating term. This is precisely why A6a's ranking is **not** the production query: A6b re-mines fold-locally and measures recall on held-out folds, where a term carried by one study in the training fold earns nothing on the papers it has never seen.


## Clinical and veterinary collision — candidates to EXCLUDE at A6c

Logged three times in the probes: *fertility* reads as IVF, *birth* as birth weight, *reproduction* as livestock, and OpenAlex stemming matched *individualism* to "individualiSED dosing of follitropin delta". These are terms the mining surfaced that belong in a NOT clause, not a query block.

**None — and the zero is the finding, not a clean bill of health.**

The frame is a citation neighbourhood around value-and-fertility work, so it never contained the clinical literature in the first place; there was nothing for the miner to flag. **An exclusion cannot be learned for contamination the training frame does not contain.** The collision is real — it was logged three times in the `89_`/`90_` probes, which pulled from the open database rather than from a citation frame — and it will appear the moment the production query runs against that database. The NOT clause at A6c must therefore be specified *a priori* from the probe evidence, and this section is the record that the mining could not and did not supply it.
