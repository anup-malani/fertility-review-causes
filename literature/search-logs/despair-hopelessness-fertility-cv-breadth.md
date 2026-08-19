# D.3.c — CV over query breadth (B1)

10-fold CV, seed 733. Gold **247** records (243 B_ONLY, 4 A_ONLY, 0 BOTH); negatives **10,313** (the rest of the Tier B frame). Title-only matching, a conservative lower bound.

## The selection rule is not the inherited one

B1 normally picks breadth at the knee of the recall-versus-budget curve. **This chapter maximises recall instead, and lets the screen carry the routing.** A4 established that precision cannot be bought with vocabulary here: mining the frame for terms separating the primary-anchor neighbourhood from the walls' produced **0** terms in `MECHANISM_AND_OUTCOME`, **0** mechanism terms in the forty strongest discriminators, and a *negative* z for `despair` itself. Wall 1 separates two mechanisms over the same treatment and the same outcome, and a title cannot see a mechanism. Precision spent on this query buys only work the screen must redo.

For comparison the inherited knee rule would have chosen **n_out=10, n_trt=10** (recall 14.6%, frame precision 16.5%); the rule applied here chooses **n_out=10, n_trt=10** (recall 14.6%, frame precision 16.5%).

## The denominator is provenance-defined

A3's spec defines Tier B as the snowball-*relevant* set. This chapter's Tier B is the raw one-hop neighbourhood, because 150 deliberately did not filter the forward fetch by topic — filtering it would have pruned the frame by distance from the query being measured. No relevance determination exists yet, so the gold is: Tier A's empirical primary-cell anchors, plus Tier B records **reached by a primary-cell anchor** and **carrying a fertility-outcome term**.

**The criterion is applied to the TITLE only**, matching the title-only convention. A first run applied it to title and abstract while still matching on title, which put records into the denominator that no title-matching query could reach; recall came out at 11.2% and the misses were dominated by the outcome block failing on records whose fertility outcome is named only in the abstract. A further **68** primary-neighbourhood records carry a fertility-outcome term in their abstract but not their title. They are excluded from the denominator and reported here instead: they are the measured cost of the title-only convention on this frame, and they are unreachable by any title query, however broad.

**Consequence, stated rather than glossed: the OUTCOME block's recall is near 1 by construction and is not informative.** The informative quantity is the TREATMENT block's recall. Outcome-block misses are still counted below, because a non-zero miss rate on a block that ought to be tautological means the backbone is incomplete — which is a real finding about the backbone, not about the query.

## Frontier

| n_out | n_trt | recall | Recall(B_only) | frame matched | frame precision |
|---|---|---|---|---|---|
| 0 | 0 | 8.1% | 7.0% | 147 | 13.6% |
| 0 | 3 | 11.7% | 10.7% | 172 | 18.6% |
| 0 | 6 | 13.0% | 11.9% | 176 | 18.2% |
| 0 | 10 | 13.8% | 12.8% | 203 | 17.2% |
| 0 | 15 | 13.8% | 12.8% | 203 | 17.2% |
| 0 | 20 | 13.8% | 12.8% | 203 | 17.2% |
| 0 | 30 | 13.8% | 12.8% | 203 | 17.2% |
| 0 | 45 | 13.8% | 12.8% | 203 | 17.2% |
| 3 | 0 | 8.1% | 7.0% | 147 | 13.6% |
| 3 | 3 | 11.7% | 10.7% | 172 | 18.6% |
| 3 | 6 | 13.0% | 11.9% | 176 | 18.2% |
| 3 | 10 | 13.8% | 12.8% | 203 | 17.2% |
| 3 | 15 | 13.8% | 12.8% | 203 | 17.2% |
| 3 | 20 | 13.8% | 12.8% | 203 | 17.2% |
| 3 | 30 | 13.8% | 12.8% | 203 | 17.2% |
| 3 | 45 | 13.8% | 12.8% | 203 | 17.2% |
| 6 | 0 | 8.1% | 7.0% | 147 | 13.6% |
| 6 | 3 | 11.7% | 10.7% | 172 | 18.6% |
| 6 | 6 | 13.0% | 11.9% | 176 | 18.2% |
| 6 | 10 | 13.8% | 12.8% | 203 | 17.2% |
| 6 | 15 | 13.8% | 12.8% | 203 | 17.2% |
| 6 | 20 | 13.8% | 12.8% | 203 | 17.2% |
| 6 | 30 | 13.8% | 12.8% | 203 | 17.2% |
| 6 | 45 | 13.8% | 12.8% | 203 | 17.2% |
| 10 | 0 | 8.5% | 7.4% | 164 | 12.8% |
| 10 | 3 | 12.6% | 11.5% | 192 | 17.7% |
| 10 | 6 | 13.8% | 12.8% | 196 | 17.3% |
| 10 | 10 | 14.6% | 13.6% | 224 | 16.5% **<- chosen** |
| 10 | 15 | 14.6% | 13.6% | 224 | 16.5% |
| 10 | 20 | 14.6% | 13.6% | 224 | 16.5% |
| 10 | 30 | 14.6% | 13.6% | 224 | 16.5% |
| 10 | 45 | 14.6% | 13.6% | 224 | 16.5% |
| 15 | 0 | 8.5% | 7.4% | 166 | 12.7% |
| 15 | 3 | 12.6% | 11.5% | 194 | 17.5% |
| 15 | 6 | 13.8% | 12.8% | 198 | 17.2% |
| 15 | 10 | 14.6% | 13.6% | 226 | 16.4% |
| 15 | 15 | 14.6% | 13.6% | 226 | 16.4% |
| 15 | 20 | 14.6% | 13.6% | 226 | 16.4% |
| 15 | 30 | 14.6% | 13.6% | 226 | 16.4% |
| 15 | 45 | 14.6% | 13.6% | 226 | 16.4% |
| 20 | 0 | 8.5% | 7.4% | 166 | 12.7% |
| 20 | 3 | 12.6% | 11.5% | 194 | 17.5% |
| 20 | 6 | 13.8% | 12.8% | 198 | 17.2% |
| 20 | 10 | 14.6% | 13.6% | 226 | 16.4% |
| 20 | 15 | 14.6% | 13.6% | 226 | 16.4% |
| 20 | 20 | 14.6% | 13.6% | 226 | 16.4% |
| 20 | 30 | 14.6% | 13.6% | 226 | 16.4% |
| 20 | 45 | 14.6% | 13.6% | 226 | 16.4% |

## Where the misses are, at the chosen setting

- treatment block only: **205**
- outcome block only: **0**
- both blocks: **6**

## Cluster credit at the chosen setting

`credit` counts gold papers a cluster fired on; `sole` counts those it was the ONLY cluster to fire on — the papers that would be lost if the cluster were dropped.

| cluster | credit | sole |
|---|---|---|
| `MECHANISM` | 3 | 3 |
| `DECLINE_CHRONIC` | 5 | 5 |
| `OPPORTUNITY_INEQUALITY` | 11 | 11 |
| `UNCERTAINTY_GENERIC` | 17 | 17 |

## The conjunction is the binding constraint, not the breadth

At the chosen setting the outcome block misses **0** gold records and the treatment block misses **205**, out of 247. The backbone is complete; the conjunction is what fails. **83% of primary-neighbourhood fertility papers name no treatment or mechanism in their title at all.** Widening breadth does not fix this — the grid shows recall flat across the whole treatment range — because the missing information is not in the field being matched.

The cluster-credit table says the same thing from the other side: `MECHANISM`, the hypothesis's own construct, fires on **3** gold papers, while `UNCERTAINTY_GENERIC` — the *neighbouring hypothesis's* vocabulary — fires on **17**. The most productive treatment cluster available to this chapter belongs to C.5.a.

### The outcome-only arm

So the recall-first rule, followed to its endpoint, drops the treatment conjunction:

| design | gold matched | frame matched | frame precision |
|---|---|---|---|
| conjunction (n_out=10, n_trt=10) | 37 / 247 | 224 | 16.5% |
| **outcome-only** (n_out=10) | 247 / 247 | 1,184 | 20.9% |

**The conjunction is not a recall-precision trade-off. It is strictly dominated.** It loses 210 of 247 gold records (85%) AND has lower precision — 16.5% against 20.9%. Requiring a treatment term admits proportionally more of the frame's decoy clouds than of its gold, because decline, inequality and uncertainty vocabulary saturates the neighbourhoods of Case & Deaton and the China Syndrome, which are precisely the seeds whose clouds carry no fertility quantity. The conjunction's only remaining effect is a 81% smaller pull, which is not a benefit when it is the wrong records that remain.

**Outcome-only recall on this gold is ~1 by construction** — the gold is defined by a title outcome term and the backbone covers those terms — so it is not quoted as an achievement. What the arm establishes is the dominance above, which does not depend on that construction: the gold cost and the precision comparison are both measured against the same denominator.

**Recommendation: outcome-only, with the routing done entirely at the screen.** A conjunction that discards four in five of the records it is meant to find, in exchange for precision under 20%, is not buying precision — it is sampling. And the sampling is not neutral: it keeps the records whose treatment is *named in the title*, which selects for the reduced-form decline and uncertainty literatures and against the measured-mechanism studies this chapter's primary cell is made of.

## The screening load this implies — the deliverable

At the chosen breadth the query fires on **224** of the 10,560 frame records, at **16.5%** precision against the provenance-defined gold. The frame is a one-hop citation neighbourhood, not the database, so this is a *ratio* to carry forward rather than an absolute count — the production run's true yield is measured when the query is executed.

**What the budget conversation needs from B1 is this ratio, not the query.** Recall-first breadth means the screen inherits the precision problem by design. Sizing screening capacity from this ratio is the intended use of this table; treating the chosen row as a well-tuned query is not.

