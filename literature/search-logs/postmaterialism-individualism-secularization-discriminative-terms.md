# D.1.a — discriminative terms (GACS A6a)

Fightin'-Words weighted log-odds (informative Dirichlet prior, z-scored) over **titles**: Tier B + Tier-A empirical anchors (**431** positives) against the snowball's non-relevant residue plus the ten purpose-built decoys (**9972** negatives). Higher z = more discriminative of the on-pair class.

**The contrast is relevant-versus-near-miss, not relevant-versus-random-database.** Every negative already passed the citation frame, so what is measured is precision at fixed recall. A6b recomputes this fold-locally so the CV recall estimate stays uncircular.

**The treatment side is five clusters, not one block** (Ruling 1): the five pairs are estimated separately and never pooled, and a single mined cause block would be ranked by whichever pair dominates the frame — which is S3, at 23 of 31 empirical anchors. Splitting keeps the budget allocation an explicit A6b decision rather than an artifact of frame composition.

Candidate terms (gold count >= 3): **377**

| block | terms |
|---|---|
| `OUTCOME` | 54 |
| `GENERIC_VALUES` | 19 |
| `S1_POSTMATERIALISM` | 5 |
| `S2_INDIVIDUALISM` | 2 |
| `S3_SECULARIZATION` | 28 |
| `S4_CHILDLESSNESS_NORM` | 0 |
| `S5_CONSUMERISM` | 0 |
| `BOTH` | 9 |
| `MULTI_PAIR` | 0 |
| `AMBIGUOUS_MATERIALISM` | 0 |
| `OTHER` | 260 |

Terms flagged as clinical/veterinary collision: **0** — see the exclusion note below.


## `OUTCOME` — top by z

| term | z | log-odds | gold | neg |
|---|---|---|---|---|
| fertility | 24.33 | 1.4 | 346 | 1929 |
| childbearing | 9.51 | 1.48 | 48 | 238 |
| fertility intentions | 7.68 | 1.62 | 27 | 116 |
| marital fertility | 7.49 | 2.34 | 15 | 31 |
| fertility united | 6.39 | 2.53 | 10 | 17 |
| fertility change | 6.24 | 2.69 | 9 | 13 |
| fertility behavior | 5.53 | 2.17 | 9 | 22 |
| children fertility | 5.41 | 4.29 | 7 | 2 |
| fertility behaviour | 5.16 | 2.37 | 7 | 14 |
| fertility related | 5.12 | 4.14 | 6 | 2 |
| attitudes fertility | 5.06 | 5.21 | 9 | 1 |
| influence fertility | 4.68 | 2.72 | 5 | 7 |
| fertility childbearing | 4.4 | 3.34 | 4 | 3 |
| birth cohorts | 4.34 | 3.05 | 4 | 4 |
| reproductive behavior | 4.15 | 2.19 | 5 | 12 |
| fertility sub | 4.14 | 2.65 | 4 | 6 |
| childlessness | 4.09 | 1.1 | 15 | 110 |
| low fertility | 4.05 | 0.93 | 20 | 175 |
| birth | 4.02 | 0.9 | 21 | 190 |
| fertility decline | 3.97 | 1.07 | 15 | 114 |

## `GENERIC_VALUES` — top by z

| term | z | log-odds | gold | neg |
|---|---|---|---|---|
| attitudes | 11.11 | 1.61 | 57 | 248 |
| cultural | 9.73 | 1.39 | 56 | 305 |
| norms | 9.49 | 2.08 | 28 | 75 |
| value | 8.11 | 1.56 | 32 | 146 |
| value children | 7.91 | 2.12 | 19 | 49 |
| gender attitudes | 6.32 | 2.28 | 11 | 24 |
| changing value | 5.33 | 3.74 | 6 | 3 |
| second demographic | 5.04 | 1.15 | 21 | 146 |
| preferences | 4.78 | 1.27 | 16 | 99 |
| attitude | 4.52 | 1.79 | 8 | 29 |
| beliefs | 3.94 | 1.33 | 10 | 58 |
| values | 3.94 | 0.82 | 24 | 236 |
| ideals | 3.89 | 1.77 | 6 | 22 |
| ideal number | 3.62 | 4.14 | 3 | 1 |
| culture | 2.62 | 0.71 | 14 | 155 |
| ideal | 2.02 | 1.05 | 4 | 31 |
| belief | 1.86 | 0.96 | 4 | 34 |
| preferences changing | 1.22 | 8.26 | 4 | 0 |
| preference | 1.0 | 0.58 | 3 | 38 |

## `S1_POSTMATERIALISM` — top by z

| term | z | log-odds | gold | neg |
|---|---|---|---|---|
| value orientation | 4.14 | 2.65 | 4 | 6 |
| ideational | 3.66 | 2.15 | 4 | 10 |
| postmodern | 2.88 | 1.57 | 4 | 18 |
| value orientations | 1.96 | 1.19 | 3 | 20 |
| modernization | 0.24 | 0.13 | 3 | 62 |

## `S2_INDIVIDUALISM` — top by z

| term | z | log-odds | gold | neg |
|---|---|---|---|---|
| autonomy | 5.68 | 2.5 | 8 | 14 |
| female autonomy | 1.06 | 8.26 | 3 | 0 |

## `S3_SECULARIZATION` — top by z

| term | z | log-odds | gold | neg |
|---|---|---|---|---|
| religion | 11.87 | 1.35 | 88 | 503 |
| religiosity | 10.47 | 1.81 | 42 | 149 |
| affiliation | 8.83 | 2.9 | 17 | 20 |
| religious affiliation | 8.17 | 3.13 | 14 | 13 |
| religious | 7.42 | 1.04 | 55 | 432 |
| religiousness | 4.77 | 2.87 | 5 | 6 |
| religious groups | 4.25 | 2.83 | 4 | 5 |
| religion religiosity | 3.65 | 2.77 | 3 | 4 |
| influence religion | 3.65 | 2.77 | 3 | 4 |
| parental religiosity | 3.62 | 4.14 | 3 | 1 |
| religion education | 3.62 | 4.14 | 3 | 1 |
| relationship religion | 3.51 | 2.55 | 3 | 5 |
| catholics | 3.34 | 1.64 | 5 | 21 |
| secularization | 3.16 | 0.99 | 11 | 91 |
| religiosit | 3.11 | 2.09 | 3 | 8 |
| religions | 3.04 | 1.32 | 6 | 35 |
| muslim | 2.49 | 0.91 | 8 | 72 |
| muslims | 2.36 | 1.47 | 3 | 15 |
| faith | 2.34 | 1.09 | 5 | 37 |
| islam | 1.37 | 0.81 | 3 | 30 |

## `BOTH` — top by z

| term | z | log-odds | gold | neg |
|---|---|---|---|---|
| fertility preferences | 5.98 | 2.1 | 11 | 29 |
| voluntary childlessness | 5.93 | 2.43 | 9 | 17 |
| postmodern fertility | 4.35 | 3.74 | 4 | 2 |
| religion fertility | 3.62 | 8.26 | 35 | 0 |
| religiosity fertility | 2.21 | 8.26 | 13 | 0 |
| fertility religion | 1.94 | 8.26 | 10 | 0 |
| affiliation fertility | 1.22 | 8.26 | 4 | 0 |
| fertility muslim | 1.22 | 8.26 | 4 | 0 |
| religiousness fertility | 1.06 | 8.26 | 3 | 0 |

## `OTHER` — top by z

| term | z | log-odds | gold | neg |
|---|---|---|---|---|
| intentions | 6.42 | 1.24 | 30 | 191 |
| children | 6.31 | 1.0 | 43 | 353 |
| roles | 5.07 | 1.79 | 10 | 36 |
| marital | 4.92 | 1.15 | 20 | 139 |
| voluntary | 4.9 | 1.84 | 9 | 31 |
| influence | 4.87 | 1.14 | 20 | 141 |
| behaviour | 4.68 | 1.24 | 16 | 102 |
| iranian women | 4.35 | 3.74 | 4 | 2 |
| intentions chinese | 4.34 | 3.05 | 4 | 4 |
| behavior | 4.09 | 0.94 | 20 | 173 |
| 1930 | 4.05 | 2.11 | 5 | 13 |
| disentangling | 4.02 | 2.5 | 4 | 7 |
| demographic transition | 4.02 | 0.84 | 24 | 232 |
| 1860 | 4.02 | 2.5 | 4 | 7 |
| stockholm | 3.9 | 2.37 | 4 | 8 |
| cultural factors | 3.9 | 2.37 | 4 | 8 |
| decline | 3.86 | 0.84 | 22 | 212 |
| conservative | 3.85 | 1.97 | 5 | 15 |
| second | 3.84 | 0.82 | 23 | 227 |
| cultural comparison | 3.81 | 3.46 | 3 | 2 |

---

## What the block counts mean

**Three of the five pairs have no mineable query vocabulary in this frame, and two have literally none.**

| pair | discriminative terms | strongest term |
|---|---|---|
| `S1_POSTMATERIALISM` | **5** | `value orientation` (z 4.14) |
| `S2_INDIVIDUALISM` | **2** | `autonomy` (z 5.68) |
| `S3_SECULARIZATION` | **28** | `religion` (z 11.87) |
| `S4_CHILDLESSNESS_NORM` | **0** | — |
| `S5_CONSUMERISM` | **0** | — |

S3 carries 28 terms topping out at z 11.87; S1's best term reaches 4.14. This is the scope's 'expected shape of the evidence' confirmed by an independent measurement, and it is stronger than the scope predicted.

**Consequence for A6b, and it is the same move D.3.b made for its rare cells.** A query built only on mined terms would be an S3 query with a generic-values annex: S1 and S2 would be reachable only through `GENERIC_VALUES` plus the outcome axis, and S4 and S5 not at all. S4 and S5 therefore need **forced a-priori backbones** rather than mined expansions, exactly as D.3.b forced its carbon-ethics cluster because it was 'conceptually central and empirically rare, so it is forced in rather than left to the mined ranking, which would never surface it.'

### S4 is degenerate, and the term ranker demonstrates it mechanically

Ruling 2 pre-registered the degenerate-pair rule: when the treatment measure and the outcome measure are the same construct, there is no pair. S4's vocabulary is that rule made visible — **every childlessness term in the ranked set classifies as `OUTCOME` or `BOTH`, and none as a pure treatment term**, because there is no S4 treatment word that is not also the outcome word:

- `voluntary childlessness` → `BOTH` (z 5.93, gold 9)
- `childlessness` → `OUTCOME` (z 4.09, gold 15)
- `attitudes childlessness` → `OUTCOME` (z 1.06, gold 3)
- `childlessness united` → `OUTCOME` (z 1.06, gold 3)
- `childless` → `OUTCOME` (z 0.32, gold 3)

A pre-registered ruling confirmed by an independent measurement is worth more than either alone, and this belongs in the chapter's methods section.

### Perfectly separating conjunctions

Terms with **zero** occurrences in 9,972 negatives and five or more in the positives. These are the outcome × treatment bigrams, and they are why the production query is a conjunction rather than a union of two term lists:

- `religion fertility` — gold 35, neg 0
- `religiosity fertility` — gold 13, neg 0
- `fertility religion` — gold 10, neg 0
- `fertility norms` — gold 7, neg 0
- `attitudes childbearing` — gold 7, neg 0
- `values fertility` — gold 6, neg 0
- `norms fertility` — gold 5, neg 0

**Not all of these are real, and the list shows its own tell.** `spain 1985`, `1985 1999` and `religion spain` separate perfectly at gold 7 because they come from one study's citation neighbourhood, not because they are query vocabulary — perfect separation at a low gold count is the signature of a single-cluster artifact rather than of a discriminating term. This is precisely why A6a's ranking is **not** the production query: A6b re-mines fold-locally and measures recall on held-out folds, where a term carried by one study in the training fold earns nothing on the papers it has never seen.


## Clinical and veterinary collision — candidates to EXCLUDE at A6c

Logged three times in the probes: *fertility* reads as IVF, *birth* as birth weight, *reproduction* as livestock, and OpenAlex stemming matched *individualism* to "individualiSED dosing of follitropin delta". These are terms the mining surfaced that belong in a NOT clause, not a query block.

**None — and the zero is the finding, not a clean bill of health.**

The frame is a citation neighbourhood around value-and-fertility work, so it never contained the clinical literature in the first place; there was nothing for the miner to flag. **An exclusion cannot be learned for contamination the training frame does not contain.** The collision is real — it was logged three times in the `89_`/`90_` probes, which pulled from the open database rather than from a citation frame — and it will appear the moment the production query runs against that database. The NOT clause at A6c must therefore be specified *a priori* from the probe evidence, and this section is the record that the mining could not and did not supply it.
