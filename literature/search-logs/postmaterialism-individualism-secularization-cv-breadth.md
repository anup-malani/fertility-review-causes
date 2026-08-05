# D.1.a — CV over per-cluster query breadth (GACS A6b)

10-fold CV, seed 733, over **412** gold titles against 173,220 negative tokens. Query = **(OUTCOME) AND (any of six treatment clusters)**; a paper is recalled iff its title matches the outcome block and at least one treatment cluster. Terms are re-mined from the training folds only.

| | breadth (outcome, treatment) | recall | Recall(A-only) | **Recall(B-only)** |
|---|---|---|---|---|
| best recall | (20, 15) | **92.5%** | 89.5% | **92.4%** |
| chosen (frontier) | (20, 10) | **92.2%** | 89.5% | **92.1%** |

Gold splits 19 A-only / 381 B-only / 12 found by both channels. **Recall(B-only) is the number that carries weight**: Tier A is keyword-sourced, so the 12 records both channels reached are partly keyword-sourced and are excluded from it.

## Where the misses are

| miss type | n |
|---|---|
| outcome block | 18 |
| treatment block | 13 |
| both blocks | 1 |

## Recall by pair (Tier-A anchors, hand-assigned)

| pair | n | recall |
|---|---|---|
| `S1_POSTMATERIALISM` | 5 | 80% |
| `S2_INDIVIDUALISM` | 1 | 100% |
| `S3_SECULARIZATION` | 23 | 100% |
| `S5_CONSUMERISM` | 2 | 50% |

Tier-1 design anchors (the natural experiments, the chapter's highest-value stratum): **100%** of 3.

## Which cluster earns the recall

`credit` counts gold papers a cluster matched; `sole` counts those **no other cluster matched**, which is what the cluster is actually worth.

| cluster | credit | sole credit |
|---|---|---|
| `S1_POSTMATERIALISM` | 13 | **3** |
| `S2_INDIVIDUALISM` | 10 | **7** |
| `S3_SECULARIZATION` | 173 | **149** |
| `S4_CHILDLESSNESS_NORM` | 12 | **0** |
| `S5_CONSUMERISM` | 1 | **1** |
| `GENERIC_VALUES` | 218 | **176** |

---

## Reading these numbers honestly

**The backbone was repaired after the first CV read its own misses, and that makes Recall(A-only) partly fitted.** The first run scored 90.8% overall on 68.4% Recall(A-only), and inspecting the misses found four omissions from *a-priori scope* vocabulary rather than four discoveries in the data: `baby boom` (which was costing a Tier-1 natural experiment), `reproductive success`, `postindustrial`, and the whole non-English outcome vocabulary that Ruling 4 had already admitted to scope. Repairing them is correcting an incomplete definition, not fitting to gold — but the repairs were *informed by* A-only misses, so Recall(A-only) is no longer an out-of-sample number and should not be quoted as one.

**Recall(B-only) is the number that carries weight, and its behaviour is the reassuring part.** It moved 91.6% → 92.1%, half a point, while Recall(A-only) moved 68.4% → 89.5%. A repair that gamed the metric would have lifted both. One that fixed real gaps in a vocabulary the orthogonal channel was already reaching by other routes lifts mainly the channel whose misses motivated it, which is what happened.

**All three Tier-1 design anchors are now retrieved** — the natural experiments are the chapter's highest-value stratum and the only studies that can support a rating above Very Low, so a query that missed one of three would have been unusable regardless of its headline recall.

## What each cluster is actually worth

**`GENERIC_VALUES` carries more sole credit than S3** (176 against 149), which is the single most consequential number here. The pair-unspecific value vocabulary — `cultural`, `attitudes`, `value of children` — retrieves more gold that nothing else reaches than the pair that dominates the entire literature. A query built only from pair-specific clusters would have been an S3 query and would have lost roughly a third of the frame.

**S4 earns zero sole credit and S5 earns one.** The forced backbones return almost nothing on the current gold, which is exactly what A6a predicted from their zero mined terms. They are kept anyway, and the justification is prospective rather than measured: the gold is a citation frame around a literature that barely studies these two pairs, so their absence from it is the finding, not evidence that the backbone is useless against the open database. **This is a cost that should be re-examined at A6c** against live universe counts — if the S4 and S5 clusters retrieve nothing there either, they are buying coverage of a literature that does not exist, and the chapter should say so.


## Full grid

| n_out | n_trt | recall | Recall(B-only) |
|---|---|---|---|
| 0 | 0 | 82.0% | 81.6% |
| 0 | 3 | 89.1% | 88.7% |
| 0 | 6 | 90.0% | 89.8% |
| 0 | 10 | 91.0% | 90.8% |
| 0 | 15 | 91.3% | 91.1% |
| 0 | 20 | 91.3% | 91.1% |
| 0 | 30 | 91.3% | 91.1% |
| 0 | 45 | 91.3% | 91.1% |
| 3 | 0 | 82.0% | 81.6% |
| 3 | 3 | 89.1% | 88.7% |
| 3 | 6 | 90.0% | 89.8% |
| 3 | 10 | 91.0% | 90.8% |
| 3 | 15 | 91.3% | 91.1% |
| 3 | 20 | 91.3% | 91.1% |
| 3 | 30 | 91.3% | 91.1% |
| 3 | 45 | 91.3% | 91.1% |
| 6 | 0 | 82.0% | 81.6% |
| 6 | 3 | 89.1% | 88.7% |
| 6 | 6 | 90.0% | 89.8% |
| 6 | 10 | 91.0% | 90.8% |
| 6 | 15 | 91.3% | 91.1% |
| 6 | 20 | 91.3% | 91.1% |
| 6 | 30 | 91.3% | 91.1% |
| 6 | 45 | 91.3% | 91.1% |
| 10 | 0 | 82.0% | 81.6% |
| 10 | 3 | 89.1% | 88.7% |
| 10 | 6 | 90.0% | 89.8% |
| 10 | 10 | 91.0% | 90.8% |
| 10 | 15 | 91.3% | 91.1% |
| 10 | 20 | 91.3% | 91.1% |
| 10 | 30 | 91.3% | 91.1% |
| 10 | 45 | 91.3% | 91.1% |
| 15 | 0 | 82.0% | 81.6% |
| 15 | 3 | 89.1% | 88.7% |
| 15 | 6 | 90.0% | 89.8% |
| 15 | 10 | 91.0% | 90.8% |
| 15 | 15 | 91.3% | 91.1% |
| 15 | 20 | 91.3% | 91.1% |
| 15 | 30 | 91.3% | 91.1% |
| 15 | 45 | 91.3% | 91.1% |
| 20 | 0 | 83.2% | 82.9% |
| 20 | 3 | 90.3% | 90.0% |
| 20 | 6 | 91.3% | 91.1% |
| 20 | 10 | 92.2% | 92.1% |
| 20 | 15 | 92.5% | 92.4% |
| 20 | 20 | 92.5% | 92.4% |
| 20 | 30 | 92.5% | 92.4% |
| 20 | 45 | 92.5% | 92.4% |
