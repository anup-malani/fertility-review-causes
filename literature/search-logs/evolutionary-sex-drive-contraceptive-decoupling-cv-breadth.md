# A6b CV — breadth-vector — evolutionary-sex-drive-contraceptive-decoupling

10-fold CV, title-only matching (conservative lower bound). Query = (EFFECT) AND (CAUSE), each = fixed backbone ∪ top-N fold-local gold-mined terms. CAUSE backbone carries the FORCED decoupling/contraception cluster (design (b)).

- gold = 118 (A 10 keyword-seeds, B 108 screen-relevant-empirical); rare decoupling/desire core = 13
- negatives (budget proxy) = 4435
- **backbone-only recall (Nf=Np=0): 7.6%** [Rec(A) 10.0% / Rec(B) 7.4% → bias +2.6%] (miss effect 8, cause 71, both 30; rare-core recall 0.2308)
- **best grid point: Nf=0, Np=20 → CV recall 42.4%** [Rec(A) 40.0% / Rec(B) 42.6% → bias -2.6%; rare-core recall 0.2308]

> Recall(B) is the honest primary metric (unbiased orthogonal sample); Recall(A)−Recall(B) is the vocabulary-bias diagnostic. rare-core recall checks whether the forced (b) backbone rescues the PRIMARY_DECOUPLING/DESIRE cells.

## Recall surface (CV held-out recall by breadth vector)

| Nf \\ Np | 0 | 3 | 6 | 10 | 15 | 20 | 30 |
|---|---|---|---|---|---|---|---|
| **0** | 8% | 30% | 31% | 35% | 36% | 42% | 42% |
| **3** | 8% | 30% | 31% | 35% | 36% | 42% | 42% |
| **6** | 8% | 30% | 31% | 35% | 36% | 42% | 42% |
| **10** | 8% | 30% | 31% | 35% | 36% | 42% | 42% |
| **15** | 8% | 30% | 31% | 35% | 36% | 42% | 42% |
| **20** | 8% | 30% | 31% | 35% | 36% | 42% | 42% |
| **30** | 8% | 30% | 31% | 35% | 36% | 42% | 42% |

## Recall / budget frontier (top-8 recall; neg_matched = on-disk budget proxy)

| Nf | Np | recall | Rec(A) | Rec(B) | A−B | rare-core | miss-eff | miss-cause | miss-both | neg-matched |
|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 20 | 42.4% | 40% | 43% | -3% | 0.2308 | 22 | 30 | 16 | 163 |
| 0 | 30 | 42.4% | 40% | 43% | -3% | 0.2308 | 25 | 30 | 13 | 179 |
| 3 | 20 | 42.4% | 40% | 43% | -3% | 0.2308 | 22 | 30 | 16 | 163 |
| 3 | 30 | 42.4% | 40% | 43% | -3% | 0.2308 | 25 | 30 | 13 | 179 |
| 6 | 20 | 42.4% | 40% | 43% | -3% | 0.2308 | 22 | 30 | 16 | 163 |
| 6 | 30 | 42.4% | 40% | 43% | -3% | 0.2308 | 25 | 30 | 13 | 179 |
| 10 | 20 | 42.4% | 40% | 43% | -3% | 0.2308 | 22 | 30 | 16 | 163 |
| 10 | 30 | 42.4% | 40% | 43% | -3% | 0.2308 | 25 | 30 | 13 | 179 |

## Reading

- If held-out misses concentrate on ONE block, move breadth there (the §6 allocation signal).
- rare-core recall isolates whether the forced (b) decoupling backbone is doing its job; if it stays high while mined breadth grows, (b) succeeded without the mined terms crowding it out.
- Production query (A6c) = refit on FULL gold at the chosen (Nf,Np); quote CV recall as the honest out-of-sample estimate. Real budget = OpenAlex universe count (A6c live search).
