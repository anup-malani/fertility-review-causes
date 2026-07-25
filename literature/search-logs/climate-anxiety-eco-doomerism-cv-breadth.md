# A6b CV - breadth-vector - climate-anxiety-eco-doomerism

10-fold CV, title-only matching (conservative lower bound). Query = (EFFECT) AND (CAUSE), each = fixed backbone union top-N fold-local gold-mined terms. CAUSE backbone carries the FORCED climate-affect and carbon-ethics cluster, this chapter's analogue of B.1's design (b).

**Theory is excluded from gold.** ECO_ETHICS_THEORY and ANXIETY_CONSTRUCT form a separate stream and do not count toward empirical recall. That exclusion is large here, since theory outnumbers the empirical core more than two to one; counting it would flatter recall.

- gold = 82 (A 10 keyword-seeds, B 72 screen-relevant-empirical); rare value-added core = 14; realized-fertility outcomes = 9
- negatives (budget proxy) = 819
- **backbone-only recall (Nf=Np=0): 40.2%** [Rec(A) 60.0% / Rec(B) 37.5% -> bias +22.5%] (miss effect 9, cause 33, both 7; rare-core 0.2857, realized-fertility 0.1111)
- **best grid point: Nf=3, Np=45 -> CV recall 64.6%** [Rec(A) 80.0% / Rec(B) 62.5% -> bias +17.5%; rare-core 0.5714, realized-fertility 0.6667]

> Recall(B) is the honest primary metric (unbiased orthogonal sample); Recall(A) minus Recall(B) is the vocabulary-bias diagnostic. rare-core recall checks whether the forced cause backbone rescues DESIRE_INDEPENDENCE and PRIMARY_CARBON_ETHICS. realized-fertility recall checks whether the query can see the only stratum that could ever support a realized-fertility pool.

## Recall surface (CV held-out recall by breadth vector)

| Nf \\ Np | 0 | 3 | 6 | 10 | 15 | 20 | 30 | 45 | 60 | 80 |
|---|---|---|---|---|---|---|---|---|---|---|
| **0** | 40% | 50% | 51% | 56% | 60% | 61% | 62% | 63% | 63% | 63% |
| **3** | 41% | 51% | 52% | 57% | 61% | 62% | 63% | 65% | 65% | 65% |
| **6** | 41% | 51% | 52% | 57% | 61% | 62% | 63% | 65% | 65% | 65% |
| **10** | 41% | 51% | 52% | 57% | 61% | 62% | 63% | 65% | 65% | 65% |
| **15** | 41% | 51% | 52% | 57% | 61% | 62% | 63% | 65% | 65% | 65% |
| **20** | 41% | 51% | 52% | 57% | 61% | 62% | 63% | 65% | 65% | 65% |
| **30** | 41% | 51% | 52% | 57% | 61% | 62% | 63% | 65% | 65% | 65% |
| **45** | 41% | 51% | 52% | 57% | 61% | 62% | 63% | 65% | 65% | 65% |
| **60** | 41% | 51% | 52% | 57% | 61% | 62% | 63% | 65% | 65% | 65% |
| **80** | 41% | 51% | 52% | 57% | 61% | 62% | 63% | 65% | 65% | 65% |

## Recall / budget frontier (top-8 recall; neg_matched = on-disk budget proxy)

| Nf | Np | recall | Rec(A) | Rec(B) | A-B | rare-core | realized | miss-eff | miss-cause | miss-both | neg-matched |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 3 | 45 | 64.6% | 80% | 62% | +18% | 0.5714 | 0.6667 | 12 | 14 | 3 | 34 |
| 3 | 60 | 64.6% | 80% | 62% | +18% | 0.5714 | 0.6667 | 12 | 14 | 3 | 34 |
| 3 | 80 | 64.6% | 80% | 62% | +18% | 0.5714 | 0.6667 | 12 | 14 | 3 | 34 |
| 6 | 45 | 64.6% | 80% | 62% | +18% | 0.5714 | 0.6667 | 12 | 14 | 3 | 34 |
| 6 | 60 | 64.6% | 80% | 62% | +18% | 0.5714 | 0.6667 | 12 | 14 | 3 | 34 |
| 6 | 80 | 64.6% | 80% | 62% | +18% | 0.5714 | 0.6667 | 12 | 14 | 3 | 34 |
| 10 | 45 | 64.6% | 80% | 62% | +18% | 0.5714 | 0.6667 | 12 | 14 | 3 | 34 |
| 10 | 60 | 64.6% | 80% | 62% | +18% | 0.5714 | 0.6667 | 12 | 14 | 3 | 34 |

## Reading

- If held-out misses concentrate on ONE block, move breadth there (the section 6 allocation signal).
- rare-core recall isolates whether the forced cause backbone is doing its job. If it stays high while mined breadth grows, the forced cluster succeeded without the mined terms crowding it out.
- realized-fertility recall is the D.3.b-specific check. The whole frame holds 9 such records, so this number is noisy by construction; read it as a structural signal, not an estimate.
- Production query (A6c) = refit on FULL gold at the chosen (Nf,Np); quote CV recall as the honest out-of-sample estimate. Real budget = OpenAlex universe count (A6c live search).
