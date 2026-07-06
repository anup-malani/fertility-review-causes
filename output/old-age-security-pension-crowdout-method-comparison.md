# Head-to-head method comparison - old-age-security-pension-crowdout

The PI's critique #2: the assignment was a three-way race of the search methods on false-negative rate, false-positive rate, cost, and replicability - and the synthesis delivered a merged method instead. This runs the race. **Two caveats set the terms:**

1. **Only one of the three sets survives as frozen data.** Anup's Tier-1 is committed and reproducible; Alexandra's query-clustering outputs (live-OpenAlex prototype, gitignored `temp/`) and Shravan's independent gold-anchored production run **do not exist** - the gold-anchored query never ran on its own; `tiers.json` is the unified tiering demonstrated on Anup's corpus. That two of three 'independent deliveries' cannot be produced is itself the first finding, and part of why the convergence claim could be asserted but not shown.
2. **So each method is a reproducible RULE over the common 8,087-paper corpus, not its as-delivered set.** Anup's and the gold-anchored rules are faithful (they are the methods' own tier rules). **Alexandra's is a labeled reconstruction** of her lexical-triage principle (keyword-reachable + both-axis lexical match, ranked, top-87 = her delivered size), not her lost output - read it as 'a method like hers', not as her.

## The three Tier-1 sets (rules)

| Method | Selection rule over the corpus | Tier-1 size |
|---|---|---|
| **Anup** | `compositeScore >= 7` (evidence-quality tiering) | 69 |
| **Gold-anchored** | `in_gold` OR (K&S channel & RELEVANT & HIGH-confidence) | 83 |
| **Alexandra** *(reconstructed)* | keyword-reachable & both axes lexically present, top-87 by lexical score | 87 |

## 1. Disagreement matrix (does 'convergence' hold, paper for paper?)

| Pair | shared | only-A | only-B | Jaccard |
|---|---|---|---|---|
| Anup vs Gold-anchored | 18 | 51 | 65 | 0.13 |
| Anup vs Alexandra | 10 | 59 | 77 | 0.07 |
| Gold-anchored vs Alexandra | 19 | 64 | 68 | 0.13 |

**All three agree on only 8 papers; their union is 200.** Pairwise Jaccard runs low, so the sets are *not* near-identical - the 'three routes, one spine' convergence is weaker than asserted, at least at the Tier-1 boundary. (Caveat: the low overlap is partly mechanical - the three rules key on different signals by construction: evidence quality vs channel-convergence vs lexical match.)

## 2. False negatives - does the method find the 10 studies that identify the effect?

Ground truth = the 10 estimand-ready studies (the papers that actually identify OAS -> fertility). FN = truth studies the Tier-1 set misses (recovery is version-variant-robust, matched by DOI or title).

| Method | recovered | missed (FN) | recall of truth |
|---|---|---|---|
| Anup | 9/10 | 1 | 90% |
| Gold-anchored | 7/10 | 3 | 70% |
| Alexandra | 7/10 | 3 | 70% |

- **Anup** misses: The US baby boom and the 1935 Social Security
- **Gold-anchored** misses: Pensions and Fertility: Evidence from Germany; Fertility and Financial Development: Evidence; The US baby boom and the 1935 Social Security
- **Alexandra** misses: The impact of long-term care insurance on fam; Pensions and Fertility: Evidence from Germany; The US baby boom and the 1935 Social Security

**Read these as Tier-1-boundary misses, not method-level misses.** The gold-anchored *rule* here is the narrow high-precision core (gold OR K&S convergence); in the full design a single-channel RELEVANT paper routes to **Tier-2**, still inside meta-analysis-ready. Its two extra misses are exactly single-channel truth papers - *Germany* is snowball-only (channel S) and *Financial Development* is keyword-only (channel K) - so they sit in that method's Tier-2, not lost. Likewise Alexandra's *LTC insurance* miss is a reconstruction artifact: 'long-term care insurance' is semantically old-age security but not lexically a backbone pension term, so my two-axis lexical proxy drops it (her real 5-cluster vocab might not). Anup's evidence-score rule recovers 9/10 because its centrality dimension already leans toward the estimand.

## 3. False positives - two definitions, side by side

Raw FP (any Tier-1 paper outside the 10-study truth) is **degenerate**: Tier-1 legitimately holds theory and topical papers, so every method scores ~90%+ 'FP'. The meaningful measure is off-cell-empirical: of a method's Tier-1 papers that are *empirical* (per the estimand tags), how many identify the wrong estimand. Coverage = how many Tier-1 papers carry an estimand tag at all (the tags cover the reviewed-40 + Tier-B-247, not the whole corpus).

| Method | raw FP | off-cell / empirical (tagged) | off-cell rate | tag coverage |
|---|---|---|---|---|
| Anup | 49/69 (71%) | 8/30 | 27% | 36/69 |
| Gold-anchored | 73/83 (88%) | 14/25 | 56% | 58/83 |
| Alexandra | 79/87 (91%) | 8/14 | 57% | 23/87 |

**The load-bearing finding:** *every* method's Tier-1 carries a large off-cell-empirical rate (27-57% of its tagged empirical papers identify the wrong estimand). No search rule - evidence quality, channel convergence, or lexical match - is estimand-precise on its own. That is exactly the gap the point-1 estimand gate closes, and it closes it *downstream of whichever search method wins*. Anup's rule is the most estimand-precise of the three here (27%), because `compositeScore` folds in a centrality term; channel-convergence and lexical matching (56-57%) do not. (Coverage caveat: off-cell rates are over the tagged subset only - 23-58 of each Tier-1 - so read them as indicative, not exact.)

## 4. Cost and replicability (from the pilot record)

| Method | cost | replicability |
|---|---|---|
| **Anup** | the only at-scale run: ~6,400 screened, ~542 LLM-scored; OpenAlex budget exhausted twice | **Reproducible** - corpus + scores committed (`prioritized.json`). |
| **Gold-anchored** | gold build + 10-fold CV + snowball; ~tens of $ LLM; OpenAlex the binding cost | **Reproducible** - committed build steps (`goldset/`), though the production query has not run end-to-end. |
| **Alexandra** | ~900 requested records; hit OpenAlex 429s + a multi-hour `Retry-After` | **Not reproducible** - live-API prototype, outputs + script gone; this row is a reconstruction. |

## Bottom line

1. **Convergence is weaker than claimed.** All three Tier-1 sets agree on only 8 of 200 papers (pairwise Jaccard 0.07-0.13). 'Three routes, one spine' overstates the paper-level overlap; the rules key on different signals and pull genuinely different sets.
2. **No single method dominates, but the ranking is not what the synthesis implied.** On this corpus Anup's plain evidence-score rule has both the best truth-recall (9/10) and the best estimand precision (27% off-cell) at the Tier-1 boundary. The gold-anchored rule's lower Tier-1 recall (7/10) is largely a boundary artifact - its single-channel truth papers route to Tier-2 - but its *higher* off-cell rate (56%) is real: channel convergence buys corroboration, not estimand precision.
3. **The unifying finding: search choice is second-order to the estimand gate.** Every method admits 27-57% off-cell empirics into Tier-1. Whichever search wins, the point-1 estimand gate is what makes the output a pooling set. This is the strongest argument for the harmonized pipeline - not that the methods converge, but that they share the same downstream gap.
4. **Replicability is the sharpest real differentiator.** Only the committed methods can be re-run; Alexandra's cannot - outputs and script are gone, which is why her row had to be reconstructed at all. That is a concrete failure of the project's 'no oral tradition' bar, and it argues for freezing every method's corpus before any future bake-off.

*Reproducible via `37_method_comparison.py`. Alexandra's row is a labeled reconstruction; treat its numbers as illustrative of a lexical-triage method, not as her delivery. The whole comparison inherits the demo `tiers.json` snapshot's gold-flag and version-variant imperfections - directional, not exact.*
