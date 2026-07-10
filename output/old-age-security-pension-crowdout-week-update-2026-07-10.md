# OAS pilot — week update

**Date:** 2026-07-10
**From:** Shravan
**To:** Anup Malani · **Cc:** Alexandra
**Re:** End-to-end run, gold-integrity finding, head-to-head comparison, and a 16-study extractable set

---

## Headline

We completed the clean end-to-end run (critique point 3), and running it whole surfaced a real problem the component checks structurally could not catch. So this week changed more than "one more run": we now have an honest recall number, a mandatory new data-integrity gate, a signed 40-study pool, and a 16-study extractable set — plus the head-to-head method comparison (critique point 2) written up on all four dimensions you asked for.

## What changed since last week

Last week we shipped the GACS methodology write-up, its evaluation, the 44-study PDF/DOI deliverable, and the estimand gate. Those were validated **in components**. This week we ran the pipeline start-to-finish for the first time, and the first live OpenAlex pull exposed that the frozen gold's Tier-B recall denominator was roughly **40% ghost citations** — hallucinated snowball titles, built out of our own query vocabulary, that return zero results in any real search. This is exactly the "validated in parts, not end-to-end" concern: neither the cross-validation (which never checks existence) nor the tag audit (which checks routing, not existence) could have caught it. Only a live search did.

We handled it honestly:

- De-ghosted the gold for free against the live corpus + Crossref, rebuilt it, and re-graded. **Honest end-to-end estimand-filtered Recall(B) = 80.6%, which passes the pre-registered 0.80 gate.** Two intermediate numbers were retracted en route — an 82.5% that was ghost-inflated, and a 76.5% poisoned by an API rate-limit bug. 80.6% is the number that stands.
- Durable fix: an **existence-verification gate is now mandatory in gold construction** — no anchor enters a recall denominator without a resolved, live DOI. This carries to every future chapter.

## From screen to a signed pool

The LLM screen produced tiered corpora and a 61-study estimand-ready set. Shravan ran the **RA gate** (a signed pass), which confirmed **40 studies** and cleared the uncertain queue.

## Head-to-head comparison of the three searchers' sets

Critique point 2: the assignment was a three-way race of the search methods on **false-negative rate, false-positive rate, cost, and replicability** — and the synthesis had delivered a merged method instead. We ran the race. Two caveats set the terms:

1. **Only one of the three sets survives as frozen data.** Anup's Tier-1 is committed and reproducible. Alexandra's query-clustering outputs (a live-OpenAlex prototype in gitignored `temp/`) and an independent gold-anchored production run **do not exist** as delivered. That two of three "independent deliveries" cannot be reproduced is itself the first finding.
2. **So each method is run as a reproducible rule over the common 8,087-paper corpus**, not its as-delivered set. Alexandra's is a labeled *reconstruction* of her lexical-triage principle — read it as "a method like hers," not as her.

| Dimension | Anup (evidence-score) | Gold-anchored | Alexandra *(reconstructed)* |
|---|---|---|---|
| **False negatives** (recall of the 10 estimand-identifying studies) | **9/10 (90%)** | 7/10 (70%) | 7/10 (70%) |
| **False positives** (off-cell rate among *tagged empirical* Tier-1 papers) | **27%** | 56% | 57% |
| **Cost** | Only at-scale run: ~6,400 screened, ~542 LLM-scored; OpenAlex budget exhausted twice | Gold build + 10-fold CV + snowball; ~tens of $ LLM; OpenAlex the binding cost | ~900 records; hit OpenAlex 429s + multi-hour `Retry-After` |
| **Replicability** | **Reproducible** (corpus + scores committed) | **Reproducible** (committed build steps; production query not yet run end-to-end) | **Not reproducible** (outputs + script gone; row reconstructed) |

Three findings:

- **Convergence is weaker than claimed.** All three Tier-1 sets agree on only **8 of 200** papers (pairwise Jaccard 0.07–0.13). "Three routes, one spine" overstates the paper-level overlap.
- **The load-bearing result: search choice is second-order to the estimand gate.** *Every* method admits 27–57% off-cell empirics into Tier-1 — no search rule (evidence quality, channel convergence, or lexical match) is estimand-precise on its own. Whichever search wins, the point-1 estimand gate is what turns the output into a pooling set. That shared downstream gap — not convergence — is the strongest argument for the harmonized pipeline. (Anup's rule is the most precise of the three at 27%, because `compositeScore` folds in a centrality term.)
- **Replicability is the sharpest real differentiator.** Only committed methods can be re-run; Alexandra's could not, which is why her row had to be reconstructed at all — a concrete instance of the "no oral tradition" bar failing, and an argument for freezing every method's corpus before any future bake-off.

*Full detail and reproduction: `output/old-age-security-pension-crowdout-method-comparison.md` (`37_method_comparison.py`). Ground truth was the 10-study estimand-ready set; off-cell rates are over the tagged subset only — directional, not exact.*

## Stage-2 "fine" filter, built and run

We built the fine filter to do the three jobs we scoped — dedup, de-hallucination (existence), and target-parameter identification — reusing the vetted pieces. Running it made the binding constraint obvious: **full-text PDF acquisition, not search.** Under a deliberately loose working definition of *extractable* (a fertility effect size + a sample size N; the GRADE rating and pooling machinery are deliberately deferred), the pool now stands at:

- **16 of 40 extractable (10 gold)** — up from 8, after a library pull of the 9 paywalled gold papers.
- **4** have full text but no usable estimate — two are theory/descriptive; two are Bismarck-era papers whose regression tables are withheld or lack a reported N.
- **20** still need a PDF — the next acquisition queue.

(The true distinct denominator is **39**: one no-DOI record is a typo-titled duplicate of a paper already in the set.) Two data-quality catches also went in: one PDF on file turned out to be the wrong document entirely, and one extraction pass had mistagged a marriage elasticity as a fertility effect — both corrected.

## Where this leaves us / next steps

The OAS pilot now sits on a defensible, reproducible pipeline with a signed 40-study pool and a 16-study extractable set. The clear next lever is acquiring the **20 outstanding PDFs** (mostly paywalled, a few needing DOI resolution), after which we resume the deferred track: GRADE ratings, the causal/association split, and pooling. We did not start a second hypothesis this week — the ghost-citation detour was worth doing properly on OAS first.
