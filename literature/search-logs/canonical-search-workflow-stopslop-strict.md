# Canonical Search Workflow: Gold-Anchored Clustered Search (GACS)

> STRICT-LITERAL demonstration copy. Every adverb removed, every passive forced active, no Overall-Goal tiebreaker. Compare against `canonical-search-workflow-stopslop.md` (judgment-applied) and the original. This copy trades precision for rule-compliance on purpose.

**Status:** We revised this on 2026-07-06 to incorporate the PI critique. We validated the design in components but have not adopted it. It still needs a clean end-to-end run, a gold freeze, and an estimand-gated re-measurement. This document specifies the revised design, not the review's canonical search. Section 7 itemizes and sequences the remaining work.

**Synthesis author:** Shravan (RA), who harmonizes the three team methods.

**Companions:**
- `canonical-search-workflow-evaluation.md` reports how GACS performs on the pilot, with the recall numbers, costs, and limitations. This document specifies what the method is; that one evaluates how well it works.
- `canonical-search-workflow-pi-critique.md` holds Anup's review of the 2026-07-03 draft. This revision responds to it point by point. Section 9 is the changelog that maps each critique to what changed.
- `canonical-search-workflow-estimand-gate.md` implements the estimand-and-mechanism gate, the fix for the PI's first critique. It documents the pilot output set that collapses from 40 to 10 and the corrected gold-anchor scorecard. Build step `source/build/goldset/34_estimand_gate.py`.

**Scope:** the per-hypothesis discovery, screening, and tiering pipeline for every chapter of the Fertility-Explanations Systematic Review. The pipeline generalizes across hypotheses rather than fitting any one. Old-age-security / pension-crowdout of fertility (chapter C.3.c) is the worked pilot.

---

## 1. The convergence claim

Three team members designed search methods for the old-age-security pilot. They started from three different places and converged on the same architecture. Alexandra's closing synthesis (her method note, §8) states the spine the team agreed on:

> Gold set defines what must be recovered. Query clusters define where and how to search. Cross-validation chooses cluster/query breadth under a fixed budget. LLM/RA screening decides inclusion, and routes theory papers to theory synthesis and empirical papers to meta-analysis.

That convergence is an observation: three people, three routes, one spine. It is an observation, not a measurement, and it does not discharge the comparison the assignment asked for. The original task raced the three methods on false-negative rate, false-positive rate, cost, and replicability, and ended in a recommendation: the best single method, an amalgam, or a weighted average. Asserting that the routes converge may hold, but it does not show the paper-for-paper disagreement between the three delivered Tier-1 sets.

We have now run the comparison (§7.1, `37_method_comparison.py`), and it does not support the strong reading. The three Tier-1 sets agree on 8 of 200 papers (pairwise Jaccard 0.07–0.13). Convergence at the level of a shared architecture holds, and this document builds on it. Convergence at the level of the selected papers does not, so "three routes, one spine" describes the pipeline shape, not the output. The comparison also showed that one of the three sets survives as frozen data, which is part of why the team could assert convergence but could not show it.

The constructive task here has two parts. First, document the one pipeline the three routes point to, and wire each person's contribution into the leg it hardens. Second, report the comparison (§7.1) that tests the convergence claim rather than assuming it.

## 2. Framing and attribution

Anup's end-to-end pipeline is the load-bearing skeleton. It is the one of the three that ran at scale (Anup screened 6,400 papers, judged ~542 relevant) and produced the baseline corpus the other two build on. The two RAs did not build rival pipelines. Each deepened one leg of Anup's.

| Pipeline leg | Origin (Anup) | Hardened by |
|---|---|---|
| Keyword discovery | single broad relevance-ranked query | **Alexandra**: vocabulary clustering + budget allocation that the gold anchors guide |
| Citation snowball | one-hop snowball | **Shravan**: an orthogonal recall auditor and gold feeder, with a saturation stop |
| Measurement | (a single trusted relevance ranking) | **Shravan**: a frozen, DOI-keyed gold set, 10-fold cross-validation, and a defensible recall estimate |
| LLM inclusion | Sonnet prioritization → a relevance score | a staged Haiku → Sonnet → RA funnel |
| Output tiers | relevance-score cutoffs (T1/T2/T3) | **Shravan**: tiers based on how many channels found a paper, with commensurable signals |
| Data hygiene | (none) | **Shravan**: DOI re-keying, a fix for a snowball DOI-shuffle bug, and a propose→verify→adjudicate resolver |

Five objects are new that neither Anup's baseline nor a single-query search had: the gold set as an explicit measurement instrument, cross-validation-tuned breadth, the clustering structure, the data-hygiene fixes, and the channel-based tiering.

## 3. The pipeline

Five phases run on a cross-cutting substrate. Every stage keys records on their DOI.

### Phase A: Build the instrument (once per hypothesis)

**A1. Intake.** State the hypothesis as `cause → effect` with a short description of the mechanism.

**A2. Decompose into axes and clusters.** The query is a Boolean of two conceptual axes:

```
( effect-axis )  AND  ( cause-axis )
```

Join AND across the two axes, OR within each axis. The parts:

- **Effect axis** is a constant core (`fertility, births, total fertility rate, family size, completed fertility, parity, number of children`), built once for the whole review, plus a per-hypothesis, mechanism-flavored extension. The effect cluster is not constant, because how a paper names the outcome depends on the mechanism: the old-age-security literature says *value of children, children as old-age support, number of sons*, not *fertility/births*. A constant effect cluster reproduces a recall miss we observed on the pilot (see the evaluation, §2). The salient effect facet also shifts with the target phenomenon: postponement/tempo for the Second Demographic Transition, marital-stopping for the First, natural-fertility spacing for the pre-modern era.
- **Cause axis** is a disjunction (OR) of vocabulary sub-clusters, swapped per hypothesis. For old-age security these are formal pensions, social-security (pay-as-you-go), the old-age-security motive, children-as-support, and intergenerational transfers.

Within each cluster, optimize for recall by including ambiguous-but-common terms, because the cross-axis AND supplies precision rather than the individual terms. Each cluster is a high-precision core (always included) plus a breadth extension that cross-validation tunes (Phase B).

**Granularity: how many sub-clusters.** You split on the vocabulary family, not the mechanism. This generalizes a simpler "one cluster per mechanism" rule: it reduces to that rule when mechanisms have distinct vocabularies, splits further when one mechanism sprawls across several vocabularies (as old-age security does), and merges when distinct mechanisms share vocabulary. Measure distinctness by how much two candidate families overlap in the gold papers they retrieve (the Jaccard overlap of their retrieved sets), and merge two families once that overlap passes a threshold. Stop adding families when a new one recovers no new gold paper and adds negligible unique candidate volume; the volume floor guards against over-splitting when the gold is thin. The data derive the final count rather than fixing it in advance: Alexandra's five clusters were a hand-estimate, and old-age security may collapse to three or four. *(Open item: run the overlap test on the existing gold to settle the pilot's number.)*

**A3. Gold-set construction (the measurement spine).** A frozen, DOI-keyed set of anchor studies the query must recover:

- **Tier A** is an empirical core (studies whose evidence type and identification strategy clear the quality bar) plus the theory canon, and the gold keeps them separate, because theory papers do not count toward empirical recall. Each empirical anchor also carries an estimand-cell tag: the `cause → effect` the study identifies, recorded as (outcome, mechanism/channel, causal direction). Topical membership and estimand membership are not the same set. On the pilot this mattered: of the 14 primary-cell gold anchors, seven identify something other than the old-age-security → fertility effect. Four measure a different outcome (child schooling, parental survival, maternal labor supply, child height), two run through the grandparental-childcare channel (opposite in sign, and central to the Second Transition), and one runs reverse-direction (the study instruments fertility to test the mechanism). A gold that covers the topic but mixes estimands makes recall against it a measure of topic coverage, not of estimand coverage. The tag builds the estimand-filtered gold the recall report needs (§E3) without discarding the topical anchors, which stay useful for the broader coverage figure and route the off-cell papers to their own chapters and to the theory stream.
- **Tier B** is an unbiased, sourced sample: take the snowball-relevant set whole, without filtering for keyword-absence. We call this the "unbiased-sample" definition of Tier B. Tier B is a fair yardstick for recall because no one curated it to match the query.
- **Resolution.** Resolve gold papers to canonical records by title, and keep papers whose identifiers are dead or have drifted, keyed on title. Never drop them, because dropping them biases the recall denominator toward easy-to-find papers.
- **Freeze** the set on RA sign-off.

**Cold-start bootstrap.** A brand-new hypothesis has no Anup baseline corpus to mine the gold from, and a gold built from a single search inherits that search's blind spots, so the recall yardstick would be circular. Assemble the gold from orthogonal channels, cheapest first:

1. **Prior meta-analyses and systematic-review included-study lists** give empirical anchors by external authority, and need no search and no screening. This is the privileged seed. *(Leakage wall: a meta-analysis's search strings may feed query terms, and its included studies may feed anchors, but never the same study to both, or you test the query on papers it was built from.)*
2. **Top-down theory/canon enumeration** (Opus generates seeds, and someone checks each for causal direction) gives the theory canon plus classic empirical anchors, resolved through the title-matching guard (§5).
3. **Citation snowball from the channel-1 and channel-2 seeds** gives the orthogonal recall channel and the feeder for Tier B.
4. **Anup's broad single-query search plus a structured LLM/RA screen**, used if the gold is still below the cross-validation floor. The screen must emit an evidence type and identification field. This is the permanent job of Anup's fallback mode, the last and most expensive channel.

Bootstrap cost scales with how well the field has studied the hypothesis; a hypothesis with prior meta-analyses may never need channel 4. **Metric integrity:** draw Tier B from channels 1–3, never channel 4, or you measure the query against papers its own search produced and Recall(B) becomes circular. Channels 2–3 generalize Shravan's earlier hybrid top-down→snowball experiment, whose true home is the bootstrap gold-builder rather than production search.

**A4. Term population.** The external core terms come from theory papers, meta-analyses, and prior published review search strings, all leakage-free. The recall extension terms come from the training fold's gold using weighted log-odds (the Monroe–Colaresi–Quinn "Fightin' Words" method): the terms that best distinguish relevant gold papers from near-miss irrelevant ones. The fold-local discipline is mandatory. Harvest terms from the training fold's gold, and measure recall on the held-out fold. A new RA must never mine query terms and measure recall on the same papers.

### Phase B: Calibrate

**B1. Cross-validation.** A 10-fold cross-validation over the per-cluster breadth settings picks breadth on the recall-versus-budget frontier, and the same cross-validation allocates budget across clusters (this replaces the earlier heuristic cluster-scoring allocator). The output is the production query.

### Phase C: Search

**C1. Clustered keyword search** under the cross-validation-chosen budget. Take the union across clusters, and resolve records DOI-first, with the title-matching guard (§5) as a check.

**C2. Citation snowball** from cluster-balanced seeds, which serves as the orthogonal recall auditor and the feeder for Tier B. **Saturation stop:** keep snowballing until the marginal yield of new relevant papers per unit of budget spent falls below a threshold (diminishing returns on the scarce OpenAlex budget). Measure the yield per cluster, because clusters saturate at different rates, and require several consecutive rounds below threshold rather than one lumpy dip. Recovery of held-out gold anchors calibrates the threshold: check that the snowball still recovered anchors it did not itself plant, and loosen the stop if it quit too early. Gold recovery is not the live stop signal, because the snowball feeds Tier B and a live signal would be circular. Forward citations get a harder cap than backward references and stay restricted to topic-specific seeds, because forward citations on broad theory anchors explode the candidate set.

**C3. Deduplicate and union** by DOI, then by normalized title.

### Phase D: Screen (three sieves of rising cost, plus a human gate)

- **D1: deterministic ranking (free).** This stage orders records by a term-match score (Alexandra's deterministic features) together with each paper's discovery channel, then applies a budget cutoff. The stage does not read meaning. Papers found through an orthogonal channel (snowball or gold, with a weak keyword signal) bypass the D1 cutoff and go straight to Haiku. The cutoff applies within the keyword channel, or the dumb term-match would discard the orthogonal-recall papers the whole architecture exists to catch.
- **D2a: Haiku (cheap).** A semantic, recall-preserving filter that passes the paper up in doubt. A Haiku false-negative is unrecoverable, so calibrate Haiku against the frozen gold and require its recall to reach ≈ 1.0. Do not drop a title-only paper because it lacks an abstract.
- **D2b: Sonnet (expensive).** A precision judge plus structured extraction (evidence type, identification strategy, mechanism/cluster tag, and a relevance score, `compositeScore`). It runs on the papers Haiku passed. The evidence-type, identification, and mechanism/cluster fields are not descriptive metadata; they are the inputs to the estimand-and-mechanism gate at E1. So Sonnet must emit them for every passed paper, in a form the gold anchors' estimand-cell tags match: the outcome the paper measures, the mechanism/channel it runs through, and the causal direction, so the gate can test each candidate for membership in the chapter's primary estimand cell. The RA calibrates this automated gate: on the pilot's 40 studies, judging blind on title+abstract, it scored 100% precision / 80% recall on the primary-vs-off-cell decision (zero false positives; the two misses were borderline estimands the RA gate catches). See `canonical-search-workflow-estimand-gate.md` and `35b_score_estimand_calibration.py`.
- **RA: the verdict gate** on boundary cases. The RA verdict is the inclusion decision; the three deterministic signals feed it.

**Adaptive depth.** With a large candidate pool, run the full `D1 → Haiku → Sonnet → RA` cascade. With a small pool, skip Haiku (`D1 → Sonnet → RA`), because Haiku cannot earn its fixed overhead on a small pool. The cascade controls cost: Haiku recall-filters so that Sonnet runs on survivors, which halves LLM spend versus running Sonnet on everything (landing at tens of dollars per hypothesis). The binding costs are the OpenAlex budget (the substrate cache addresses it) and RA time (a narrower uncertain band addresses it), not the LLM.

### Phase E: Output

**E1. Tier assignment** gates on the verdict and tiers by channel agreement:

- The RA/Sonnet verdict gates the paper: RELEVANT makes it eligible for Tier 1/2, UNCERTAIN sends it to Tier 3, NOT-RELEVANT excludes it.
- **Tier 1 (core)** is a gold-set member OR a paper that more than one channel found (keyword and snowball).
- **Tier 2** is relevant, but one channel found it.
- **Tier 3** is the uncertain recall net, retained for auditing, not included in the review.
- **The relevance score (`compositeScore`) sorts within a tier**, and does not define the tier. It is Sonnet's output, and the pipeline does not blend it with the deterministic term-match score. In Anup's baseline the score defined the top tier (T1 ≥ 7); here it drops to an intra-tier sort, with channel agreement as the tier basis and the RA verdict as the gate.
- **Gold papers rank above keyword-and-snowball agreement** within Tier 1, because gold membership verifies (frozen, RA-signed, curated) while multi-channel agreement corroborates through discovery. These differ in kind, so whether the channels are independent does not bear on the ordering. Keyword-and-snowball agreement need not be independent; it stays in Tier 1 as honest correlated corroboration, stronger than single-channel and still verdict-gated.
- **The meta-analysis-ready subset has two nested definitions, reported apart.**
  - **Meta-analysis-ready** = (Tier 1 ∪ Tier 2) ∩ the empirical papers that clear the evidence bar. This is the coverage set: every empirical paper on the hypothesis's topic that passed the verdict. On the pilot this was 44 studies.
  - **Estimand-ready (the pooling set)** = the topical set ∩ the estimand-and-mechanism gate. These are papers whose Sonnet-extracted outcome, mechanism/channel, and causal direction match the chapter's primary estimand cell (for the pilot: old-age-security motive → fertility, forward direction). This is the set that can share a pooled estimate. On the pilot the topical 44 collapses to ten once the gate applies (the RA inclusion pass marked 10 RETRIEVE / 30 EXCLUDE of 40 DOI-resolved studies, nine in the primary causal cell). Papers on a different outcome, a different channel (grandparental childcare, opposite sign), or the reverse direction are real, and the pipeline keeps them for their cells, but they cannot pool with the primary motive.

  Estimand precision, not topic coverage, is the review's binding constraint, so the estimand-ready set is the operative output for meta-analysis. The pipeline reports the topical set alongside it as the coverage denominator and to feed the off-cell chapters. *(The gate is implemented and runs on the pilot: `source/build/goldset/34_estimand_gate.py`, documented in `canonical-search-workflow-estimand-gate.md`, taking 40 topical reviewed studies to 10 estimand-ready. The remaining piece is the estimand-gated recall re-grade against an estimand-filtered Tier B; see §7, move 3.)*

**E2. Routing: two non-exclusive streams.** Sonnet's tag routes each paper: empirical papers to the meta-analysis / effect-size stream, theory papers to the JEL theory-section stream, both streams if a paper is both. This is the same empirical-core/theory-canon split the gold's Tier A makes.

**E3. Recall report.** Report recall at two targets, because the method can recover a topic well while under-recovering the estimand:

- **Topical recall** against the full gold. Report Recall(B) (recall against the unbiased Tier B) as the primary honest figure, Recall(A) on the keyword-reachable empirical core, and the gap Recall(A) − Recall(B) as a diagnostic for whether the query tilts toward keyword-sourced papers.
- **Estimand-filtered recall** against the estimand-filtered gold (the primary-cell papers, per the A3 tag). This figure answers the review's question: did we recover the studies that identify the effect the chapter is about? We measured it (`36a`/`36b`, report `{slug}-estimand-recall-regrade.md`): we estimand-tagged all 247 Tier-B papers and re-ran the CV with the query fixed and the denominator partitioned by cell. Tier B turns out to hold 65% theory models and 23% empirical primary-cell. Re-based on the primary cell, topical Recall(B) rises from 72.5% to estimand-filtered 82.5% (88% on high-confidence tags). The number moves up, because the recall the query was losing sat in the theory/off-cell tail, not in the papers that identify the effect. So the pilot's 72% understated recall of the target while the "44 meta-analysis-ready" overstated the usable set: recall was never the binding constraint, the definition of the target was.

Also report the hard-tail conditional ceiling (recall on the Tier-B papers the two-axis query misses on title, recovered via abstract match) as a bound. It is an optimistic bound, because the snowball seeded Tier B off the keyword set, so Tier B is not orthogonal and Recall(B) inherits a residual keyword bias it cannot escape. State this wherever you quote the number; the independent adjudicated inclusion set of §7.1 is the non-circular check. Finally, report per-cluster miss diagnostics (which feed query revision), empirical-versus-theory recall apart, and the budget spent.

**Benchmark.** A Cochrane-style systematic review targets near-complete recall of the eligible literature, so a search stage that concedes ~28% has not reached benchmark. The pilot's ~72% is a title-only, un-frozen, dry-run lower bound and will move: up with abstract matching, and in both directions once the gold freezes. It is not a final performance figure. The adoption bar this document holds itself to is estimand-filtered Recall(B), measured against a frozen gold on one clean end-to-end run, with an explicit target set before the run (§7, moves 2–3). (The companion evaluation reports the pilot's numbers.)

### Substrate (every stage)

The substrate keys on DOI throughout and runs the title-matching machinery of §5. It provides a persistent cache at the project level (the next hypothesis reuses a record the pipeline pulled for one hypothesis, cutting total OpenAlex budget as hypotheses accumulate), resumable stage outputs, a hard per-run budget cap with graceful fail-and-resume (which prevents the multi-hour `Retry-After` sleep when a rate limit hits), polite request scheduling, bounded retry/backoff, and separate dry-run and production modes.

## 4. The unifying stop principle

Every "when do we stop?" decision in the workflow follows the same rule: stop when the marginal recovery of new gold anchors or new relevant papers approaches zero, subject to a volume-or-count floor that guards against noise. It governs the granularity split (Phase A2), the cold-start bootstrap (A3), the Haiku recall calibration (D2a), and the snowball saturation stop (C2). State it once, reference it everywhere.

## 5. Title-matching machinery

Title matching underlies anchor resolution everywhere in the pipeline, so it needs to hold up. The naive approach, counting shared words between two titles (the Jaccard overlap), is the weak link: a topic-homogeneous corpus inflates it, short titles swing it, and subtitle, punctuation, and translation differences break it. The standard we use:

- **Normalize titles first.** Strip the subtitle, fold case, punctuation, and diacritics, and expand `& → and`.
- **Compare with TF-IDF cosine similarity**, not raw word overlap, which down-weights the ambient topic vocabulary that every paper in the corpus shares.
- **Add an author-surname + year secondary gate.**
- **Keep the context-dependent threshold.** Require a high similarity (≈ 0.80) when you select a match from a blind search, but a looser one (≈ 0.50) when you verify an already-proposed DOI. Always verify against independent metadata (Crossref), never against an unconfirmed corpus title, because a stored title can itself be the wrong paper (see the DOI-shuffle bug in the evaluation, §5).

## 6. Decision ledger (contradictions resolved)

The team's three methods disagreed on six points. We resolved each as follows; the codes are handles for cross-reference, not required reading.

| Item | Resolution |
|---|---|
| **C1: budget allocator** | Cross-validation on the recall/budget frontier (we retire the heuristic cluster-scoring allocator). |
| **C2: title matching** | Normalize → TF-IDF cosine → author+year gate; ≈0.80 to select, ≈0.50 to verify; always verify against independent metadata. |
| **C3: resolution policy** | Production search resolves DOI-first with a guard; the gold/measurement set resolves by title, and keeps unresolvable papers so the recall denominator stays unbiased. |
| **A1: query algebra** | AND across the two axes, OR within each axis. |
| **A2: the three signals** | The relevance score, the relevant/maybe/not label, and the discovery-channel provenance are three deterministic signals that feed one shared LLM+RA verdict; none of them is the verdict. |
| **A3: discovery philosophy** | Measure and structure the search (clustering + cross-validation); Anup's single trusted query is the fallback/bootstrap mode. |

**Commensurability under unification, with a caveat.** For future hypotheses the pipeline runs, the three signals are no longer three people's separate corpora but four fields on one record: the deterministic label (Alexandra's relevant/maybe/not), the relevance score (Anup's/Sonnet's `compositeScore`), the discovery-channel provenance (gold, keyword, snowball), and the RA verdict. So for new hypotheses nothing remains to reconcile. The caveat the earlier draft glossed: this unification does not answer the comparison question on the legacy corpus, where three people did run apart. The pipeline will emit commensurable fields going forward as a property of the design, but that is not evidence that the three legacy methods agreed. The old cross-method mapping survives as more than a formality. It is both the one-time migration for the legacy corpus and the substrate for the head-to-head comparison in §7.1, because each legacy paper's three method-of-origin memberships are the disagreement matrix that comparison needs.

## 7. Open items: the road to adoption

The PI's review (companion critique) sets the bar: GACS is a promising design shown in parts, not yet the review's adopted search. Five moves, in priority order, close the gap. The first three run in sequence; §7.1 and §7.2 specify the two the earlier draft left implicit.

1. **Run the head-to-head comparison the assignment asked for.** *(Done, `37_method_comparison.py`, §7.1.)* Weak convergence (Jaccard 0.07–0.13), FN 9/10 vs 7/10 vs 7/10, off-cell-empirical 27–57% across all three, and one set (Anup's) survives as frozen data. Residual: it re-grades on the demo corpus with reconstructed rules, not three frozen independent runs, which a clean end-to-end run (move 2) plus corpus-freezing would fix.
2. **Freeze the gold, then do one clean end-to-end production run.** The RA adjudicates the 52 Tier-B UNCERTAINs and signs off Tier A, then the pipeline runs gold-freeze → tuned query → fresh screen → tiers once, end to end, with the real OpenAlex budget wired in. This replaces the three component stand-ins (the CV dry run, the legacy tier demonstration, the Phase-E migration) with a single number chain.
3. **Measure estimand-filtered recall, not topical recall alone.** *(Done.)* The gate is implemented (`34_estimand_gate.py`; output set 40 → 10, 7 of 15 anchors off-cell), the RA calibrates the automated gate (100% precision / 80% recall, blind; `35a`/`35b`) so it runs on hypotheses with no RA pass, and we estimand-tagged Tier B and re-graded the recall (`36a`/`36b`): topical Recall(B) 72.5% → estimand-filtered 82.5%, with Tier B revealed as 65% theory / 23% empirical primary-cell. See `canonical-search-workflow-estimand-gate.md`. **The audit closes the residual** (`39a`/`39b`, `{slug}-estimand-tag-audit.md`): an independent blind second reader re-tagged a 129-of-247 audit (a census of all 99 abstract-bearing papers + 30 title-only), double-screening the Tier-B tags, and the RA adjudicated the group-level disagreements. On the adjudicable stratum, the auto tagger agrees with the adjudication on 93% (kappa 0.84), leaks zero THEORY→PRIMARY (0/67, so the theory routing the PI flagged hides no empirical estimate) and scores PRIMARY precision 9/11 (the two misses are off-cell empirics the gate over-admitted, so correcting them tightens the pooling set). Estimand Recall(B) holds to <1pp (82.5% → 81.8% audit-corrected; envelope 81.8–83.0%). This closes the PI's first critique.
4. **Fit every parameter and write the defaults down** (§7.2), then hand the pipeline to a second RA to run without the author present. If they reproduce a run from the written defaults, we have met the "no oral tradition" bar.
5. **Replicate on a second hypothesis**, a well-studied one with prior meta-analyses, to exercise the cold-start bootstrap (§A3) and convert "designed to generalize" into "generalizes."

### 7.1 Head-to-head comparison (run: `37_method_comparison.py`, report `{slug}-method-comparison.md`)

The three methods raced against the 10-study estimand-ready ground truth on the disagreement matrix, false-negative rate, false-positive rate, cost, and replicability. **First finding, before any metric: one of the three sets survives as frozen data**, Anup's. Alexandra's live-OpenAlex prototype outputs (and script) are gone; Shravan's gold-anchored production query never ran apart (`tiers.json` is the unified tiering the team demonstrated on Anup's corpus). So each method operationalizes as a reproducible rule over the common 8,087-paper corpus. Anup's and the gold-anchored rules are faithful; Alexandra's is a labeled reconstruction of her lexical-triage principle. Results:

- **Convergence is weak.** The three Tier-1 sets agree on 8 of 200 papers (pairwise Jaccard 0.07–0.13), so "three routes, one spine" overstates the paper-level overlap.
- **FN (recall of the 10 effect-identifying studies):** Anup 9/10, gold-anchored 7/10, Alexandra 7/10. The gold rule's extra misses are single-channel truth papers that route to its Tier-2 by design, a boundary artifact rather than method-level loss.
- **FP:** raw FP is degenerate (~90% for all); the meaningful off-cell-empirical rate is Anup 27%, gold-anchored 56%, Alexandra 57%. Every method admits 27–57% off-cell empirics into Tier-1.
- **Replicability** is the sharpest real differentiator: the committed methods alone can re-run.

The recommendation the assignment asked for: no search rule reaches estimand precision on its own (the off-cell finding), so the harmonized pipeline earns its value not by making the methods converge but by sharing the same downstream gap, which the point-1 estimand gate closes whichever search wins. Freeze every method's corpus before any future bake-off (the reason Alexandra's needed a reconstruction). The report gives full numbers, caveats, and the demo-corpus limitations.

### 7.2 Parameter defaults (proposed: fit and confirm in the clean run)

Every knob gets a written default and a one-line justification, so a user can run the pipeline without its author. The defaults stay provisional until the clean run (move 2) confirms them; the point is a written starting value, not a blank to fill from memory.

| Parameter | Proposed default | Justification |
|---|---|---|
| CV breadth grid (Nf, Np) | {0, 10, 20, 30, 40} | Pilot CV saturated at N ≈ 20–30; the grid brackets it. |
| CV folds | 10 | Standard; used in the pilot; enough folds given ~50 empirical anchors. |
| Cluster-merge overlap threshold | Jaccard ≥ 0.6 on retrieved gold sets | Merges near-synonymous families without collapsing distinct ones. **Run** (`38`): on the frozen gold, no family pair reaches 0.6. The expected formal-pensions ≈ SS/PAYG merge does not hold (Jaccard 0.29, overlap coef 0.45), so the five stay distinct (see below). |
| Snowball saturation: yield floor | < 1 new relevant / 50 records pulled | Diminishing-returns cutoff on the scarce OpenAlex budget. |
| Snowball saturation: consecutive rounds | 2 rounds below floor | Guards against a single lumpy dip. |
| Forward-citation cap | topic-specific seeds, ≤ 1 hop | Forward citations explode on broad theory anchors; 7 of 8 pilot ghosts were forward. |
| Backward-citation depth | all backward refs, ≤ 1 hop | Cheaper and cleaner than forward (the pilot's one backward ghost was real). |
| D1 keyword budget cutoff | top ~2× the expected include count | Bounds the LLM/RA funnel; orthogonal-channel papers bypass it (see D1). |
| Haiku recall calibration | recall ≥ 0.98 vs. frozen gold | Haiku false-negatives are unrecoverable; near-1.0 required. |
| Bootstrap gold-size floor | ≥ 30 empirical anchors before CV | Below this the fold-local term mining gets too noisy (pilot gold ≈ 31 empirical). |

**Cluster count: overlap test run** (`38_cluster_overlap.py`, `{slug}-cluster-overlap.md`). We expected the five hand-estimated cause-axis families to collapse to three or four; on the frozen gold they do not. Under the §7.2 rule (Jaccard ≥ 0.6 on retrieved gold sets) no pair merges, so the count is five. The closest pair, formal-pensions × SS/PAYG, is the one §7.2 assumed near-synonymous, but it shares 29% of its combined retrieval (Jaccard 0.29, overlap coefficient 0.45); the count would fall to four if the merge bar relaxed to ≈0.25. So the hand-estimated "≈" overstated the overlap: the families pull different papers and each earns its own search budget. (Caveat: 56/303 gold anchors and 148/247 Tier B are title-only; abstracts could nudge a borderline pair, though not the block structure.)

### 7.3 Remaining engineering / hygiene items

- **Full calibration run** (the "Part-4-full" task): wire in the real OpenAlex universe-size budget, add abstract matching, finalize the hard-tail bound, refit on the frozen gold, produce the production query, and promote the pipeline to `.claude/workflows/`. This is the engine for move 2.
- **Legacy migration** script: fold the existing old-age-security corpus into the unified tier scheme, also the substrate for the §7.1 comparison.
- **PI data-hygiene ticket:** re-key the corpus on DOI; fix the snowball DOI-shuffle bug; and, new from the pilot, add an abstract-or-live-DOI gate plus a harder forward-citation cap on Tier B, to keep ghost citations out of the gold (see the evaluation, §5).

## 8. Provenance

- Method notes harmonized here: `*-gold-anchored-keyword-method.md` (Shravan), `*-query-clustering-method.md` (Alexandra), `*-hybrid-discovery-method.md` (Shravan), and Anup's prioritized corpus with its relevance-score tiers.
- The Task-A build (the gold-anchored engine this workflow wraps): `source/build/goldset/`, `*-gold-set-build-log.md`, Parts 1–4.
- Companion evaluation of this method on the pilot: `canonical-search-workflow-evaluation.md`.
- This synthesis: drafted 2026-06-30 from the Task-B design workshop; finalized 2026-07-03; revised 2026-07-06 to incorporate the PI critique (see §9).

## 9. Changelog: response to the PI critique (2026-07-06)

This revision responds to `canonical-search-workflow-pi-critique.md`. Each of the PI's seven concerns maps to what changed. We concede two and fix them in the method now; we concede the rest and convert them into sequenced, specified open items (§7), because they need a run this revision does not perform.

| # | PI critique | Response in this revision |
|---|---|---|
| 1 | Optimizes topical recall; the binding constraint is estimand precision (44 → ~10 under the estimand). | **We concede this and add AND implement the gate.** Estimand-cell tags on gold anchors (A3), estimand fields required from Sonnet (D2b), an estimand-ready pooling set distinct from the topical set (E1), estimand-filtered recall as a reported target (E3). We now run it on the pilot: `34_estimand_gate.py`, write-up `canonical-search-workflow-estimand-gate.md`, output set 40 → 10, corrected scorecard 7 of 15 anchors off-cell (reconciles with the PI's "7 of 14"). The RA calibrates the automated gate (100% precision / 80% recall, blind; `35a`/`35b`), so it runs on hypotheses with no RA pass. We re-grade the recall (`36a`/`36b`): topical Recall(B) 72.5% → estimand-filtered 82.5%, Tier B holding 65% theory / 23% empirical primary-cell. And blind double-screening now spot-audits the automated Tier-B tags (`39a`/`39b`, `{slug}-estimand-tag-audit.md`): 93% agreement / kappa 0.84 on the abstract census, zero THEORY→PRIMARY leakage, recall holds to <1pp. **Critique #1 closed:** recall of the target was never the constraint, the target's definition was, and the tags behind it hold up under audit. |
| 2 | Answered a different question: a synthesized 4th method, not the assigned head-to-head; convergence asserted, not shown. | **We concede this and now run it** (`37_method_comparison.py`, §7.1). Disagreement matrix + FN + FP + cost + replicability vs the 10-study truth. Convergence is weak (agree on 8/200, Jaccard 0.07–0.13); FN 9/10 (Anup) vs 7/10 (gold, Tier-1 boundary) vs 7/10 (Alexandra); off-cell-empirical 27–57% across all three; one set (Anup's) survives as frozen data. Search choice is second-order to the estimand gate. |
| 3 | Validated in components, not end to end; we cannot make the decision yet. | **We concede this.** The status line now reads "validated in components, pending a clean run"; the single end-to-end run is §7, move 2. |
| 4 | 72% is both low (vs. Cochrane near-complete) and soft (dry run, un-frozen, title-only). | **We concede this.** E3 adds an explicit benchmark paragraph: 72% is a title-only lower bound, near-complete recall is the target, and the adoption bar is estimand-filtered Recall(B) on a frozen gold with a pre-set target. |
| 5 | Circularity acknowledged but not escaped: the snowball seeded Tier B off the keyword set. | **We concede this and state it at point of use.** E3 now flags the residual keyword bias in Recall(B) wherever you quote the number; §7.1's independent adjudicated inclusion set is the non-circular check. |
| 6 | Too complex for anyone but its author; unset knobs = oral tradition. | **We address this.** §7.2 gives a parameter-defaults table (default + one-line justification per knob), and §7, move 4 hands the pipeline to a second RA as the replicability test. The one knob still hand-estimated, the cluster count, we now run (`38_cluster_overlap.py`): the five cause-axis families stay five under the merge rule (no pair reaches Jaccard 0.6; the assumed formal-pensions ≈ SS/PAYG merge fails at 0.29). |
| 7 | One hypothesis; generalization (the property most needed) untested. | **We concede this.** §7, move 5 keeps second-hypothesis replication (well-studied, with prior meta-analyses) to exercise the cold-start bootstrap. |

**Kept at the PI's recommendation:** the frozen-gold instrument, fold-local discriminative-term mining, channel-convergence tiering, and the data-hygiene fixes. The PI endorsed all four as contributions to carry into every chapter, and we change none here.
