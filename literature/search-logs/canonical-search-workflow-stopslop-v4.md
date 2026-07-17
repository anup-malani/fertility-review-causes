# Canonical Search Workflow: Gold-Anchored Clustered Search (GACS)

**Status:** Revised 2026-07-06 to answer the PI critique. Validated in parts, not yet adopted: it still needs one clean end-to-end run, a frozen gold, and an estimand-gated re-measurement. This document specifies the revised design, not the review's canonical search; §7 sequences the remaining work.

**Synthesis author:** Shravan (RA), harmonizing the three team methods.

**Companions:**
- `canonical-search-workflow-evaluation.md` reports how GACS performs on the pilot: recall numbers, costs, limits. This document says what the method is; that one says how well it works.
- `canonical-search-workflow-pi-critique.md` is Anup's review of the 2026-07-03 draft. §9 maps each critique to a change.
- `canonical-search-workflow-estimand-gate.md` implements the estimand-and-mechanism gate, the fix for the PI's first critique (`source/build/goldset/34_estimand_gate.py`).

**Scope:** the per-hypothesis discovery, screening, and tiering pipeline for every chapter of the Fertility-Explanations Systematic Review. It generalizes across hypotheses rather than fitting one. Old-age-security / pension-crowdout of fertility (chapter C.3.c) is the worked pilot.

---

## 1. The agreement claim

Three team members independently designed search methods for the old-age-security pilot, starting from three places and landing on one architecture. Alexandra's synthesis states the shared spine almost verbatim: the gold set defines what must be recovered, query clusters define where to search, cross-validation chooses breadth under a fixed budget, and LLM/RA screening decides inclusion, routing theory papers to theory synthesis and empirical papers to meta-analysis.

Three people, three routes, one spine: an observation, not a measurement. It does not discharge the comparison the assignment asked for, a paper-for-paper race of the three methods toward a recommendation. Saying the routes agree on shape does not show the disagreement between the three delivered Tier-1 sets. That comparison has now run (§7.1): the sets share only 8 of 200 papers, and only one survives as frozen data. Agreement on architecture holds and this document builds on it; agreement on selected papers does not. §2–6 document the one pipeline the three routes point to; §7.1 tests the claim rather than assuming it.

## 2. Framing and attribution

Anup's end-to-end pipeline is the load-bearing skeleton, the only one that ran at scale (6,400 papers screened, ~542 judged relevant) and produced the baseline corpus the other two build on. The two RAs did not build rival pipelines; each deepened one leg of Anup's.

| Pipeline leg | Origin (Anup) | Hardened by |
|---|---|---|
| Keyword discovery | single broad relevance-ranked query | **Alexandra**: vocabulary clustering + budget allocation guided by the gold anchors |
| Citation snowball | one-hop snowball | **Shravan**: a recall checker searching by citation links, not keywords, so it finds papers the keyword search misses; plus a gold feeder and a saturation stop |
| Measurement | a single trusted relevance ranking | **Shravan**: a frozen, DOI-keyed gold set, 10-fold cross-validation, a defensible recall estimate |
| LLM inclusion | Sonnet prioritization → a relevance score | a staged Haiku → Sonnet → RA funnel |
| Output tiers | relevance-score cutoffs (T1/T2/T3) | **Shravan**: tiers by how many channels found a paper, all signals on one scale |
| Data hygiene | none | **Shravan**: DOI re-keying, a snowball DOI-shuffle fix, a propose→verify→resolve pass |

## 3. The pipeline

Five phases run on a shared substrate. Every stage keys records on their DOI.

### Phase A: Build the instrument (once per hypothesis)

**A1. Intake.** State the hypothesis as `cause → effect` with a short mechanism description.

**A2. Decompose into axes and clusters.** The query is a Boolean of two conceptual axes, AND across them, OR within each:

```
( effect-axis )  AND  ( cause-axis )
```

- **Effect axis:** a constant core (`fertility, births, total fertility rate, family size, completed fertility, parity, number of children`), built once for the review, plus a per-hypothesis mechanism-flavored extension. The core is not strictly constant, because how a paper names the outcome depends on the mechanism: the old-age-security literature says *value of children, children as old-age support, number of sons*, not *fertility/births*. A strictly constant effect cluster reproduces a recall miss we saw on the pilot. The salient facet also shifts with the target phenomenon.
- **Cause axis:** an OR of vocabulary sub-clusters, swapped per hypothesis. For old-age security: formal pensions, social-security (pay-as-you-go), the old-age-security motive, children-as-support, and intergenerational transfers.

Within each cluster, include ambiguous-but-common terms for recall, because precision comes from the cross-axis AND, not from specific terms. Each cluster is a high-precision core plus a breadth extension tuned by cross-validation.

**Granularity.** Split on the vocabulary family, not the mechanism: split when one mechanism sprawls across several vocabularies (as old-age security does), merge when distinct mechanisms share vocabulary. Measure distinctness by the Jaccard overlap of the gold papers two families retrieve (the share of their combined retrieved set held in common), and merge once it passes a threshold. Stop adding families when a new one recovers no new gold paper. The data set the final count: Alexandra's five clusters were a hand-estimate, settled empirically in §7.2.

**A3. Gold-set construction (the measurement spine).** A frozen, DOI-keyed set of anchor studies the query must recover:

- **Tier A:** an empirical core (studies whose evidence type and identification strategy clear the quality bar) plus the theory canon, kept separate, because theory papers do not count toward empirical recall. Each empirical anchor carries an estimand-cell tag: the `cause → effect` the study identifies, as (outcome, mechanism/channel, causal direction). Topical and estimand membership differ. On the pilot, of the 14 primary-cell anchors, seven identify something other than old-age-security → fertility: a different outcome, the grandparental-childcare channel (opposite sign), or the reverse direction. A topically relevant but estimand-heterogeneous gold measures topic coverage, not estimand coverage. The tag builds the estimand-filtered gold §E3 needs without discarding the topical anchors, which stay useful for the coverage figure and for routing off-cell papers to their chapters.
- **Tier B:** an unbiased sample drawn through a different discovery channel than the keyword query (the citation snowball), so the query's blind spots do not shape it. Take the snowball-relevant set whole, without filtering for keyword-absence. It is a fair yardstick precisely because no one curated it to match the query.
- **Resolution:** resolve gold papers to canonical records by title, and keep papers whose identifiers are dead or drifted, keyed on title. Dropping them biases the recall denominator toward easy-to-find papers.
- **Freeze** the set on RA sign-off.

**Cold-start bootstrap.** A brand-new hypothesis has no Anup baseline to mine, and a gold built from a single search inherits that search's blind spots, making the recall yardstick circular. Assemble the gold from non-overlapping channels, cheapest first: (1) prior meta-analyses and review included-study lists, the privileged seed, needing no search *(leakage wall: a study may feed query terms or anchors, never both)*; (2) top-down theory/canon enumeration (Opus seeds, each direction-checked), resolved through §5; (3) citation snowball from the channel-1/2 seeds, independent of the keyword search, feeding Tier B; (4) Anup's broad query plus a structured LLM/RA screen, only if the gold is still below the CV floor. **Metric integrity:** draw Tier B from channels 1–3, never channel 4, or Recall(B) is circular. Channels 2–3 generalize Shravan's earlier top-down→snowball experiment, whose home is the bootstrap gold-builder, not production search.

**A4. Term population.** External core terms come from theory papers, meta-analyses, and prior published review search strings, all leakage-free. Recall extension terms come fold-locally from the gold using weighted log-odds (the Monroe–Colaresi–Quinn "Fightin' Words" method): the terms best distinguishing relevant gold from near-miss irrelevant papers. The fold-local discipline is mandatory: harvest terms only from the training fold, measure recall on the held-out fold, never both on the same papers.

### Phase B: Calibrate

**B1. Cross-validation.** A 10-fold cross-validation over per-cluster breadth settings picks breadth on the recall-versus-budget frontier and allocates budget across clusters (replacing the earlier heuristic allocator). The output is the production query.

### Phase C: Search

**C1. Clustered keyword search** under the CV-chosen budget. Union across clusters, resolve DOI-first with the title-matching guard (§5).

**C2. Citation snowball** from cluster-balanced seeds, the independent recall checker: it finds papers by citation links rather than keywords, catching what the keyword search misses, and feeds Tier B. **Saturation stop:** snowball until the marginal yield of new relevant papers per unit budget falls below a threshold. Measure yield per cluster, since clusters saturate at different rates, and require several consecutive rounds below threshold, not one dip. Held-out gold anchors calibrate the threshold. Gold recovery is not the live stop signal, because the snowball feeds Tier B and using it live would be circular. Forward citations get a harder cap than backward references (§7.2).

**C3. Deduplicate and union** by DOI, then by normalized title.

### Phase D: Screen (three sieves of rising cost, plus a human gate)

- **D1: deterministic ranking (free).** Order records by a term-match score (Alexandra's deterministic features) plus each paper's discovery channel, then apply a budget cutoff. The stage is blind to meaning. Papers found through a non-keyword channel (snowball or gold, weak keyword signal) bypass the cutoff straight to Haiku. The cutoff applies within the keyword channel only, or the term-match discards exactly the papers the non-keyword channels found.
- **D2a: Haiku (cheap).** A meaning-aware, recall-preserving filter that passes the paper up when in doubt. A Haiku false-negative is unrecoverable, so calibrate against the frozen gold to recall ≈ 1.0. Do not drop a title-only paper for lacking an abstract.
- **D2b: Sonnet (expensive).** A precision judge plus structured extraction (evidence type, identification strategy, mechanism/cluster tag, relevance score `compositeScore`), run only on papers Haiku passed. These fields feed the estimand gate at E1, so Sonnet emits them for every passed paper in the anchors' (outcome, mechanism/channel, causal direction) form, letting the gate test each candidate for the primary cell. The RA calibrates this gate against the pilot (100% precision / 80% recall, blind; §7, move 3; `35b`).
- **RA: the verdict gate** on boundary cases. The RA verdict is the inclusion decision; the three deterministic signals only feed it.

**Adaptive depth.** With a large candidate pool, run the full `D1 → Haiku → Sonnet → RA` cascade; with a small pool, skip Haiku, which cannot earn its fixed overhead there. Haiku recall-filters so Sonnet runs only on survivors, roughly halving LLM spend (~tens of dollars per hypothesis). The binding costs are the OpenAlex budget and RA time, not the LLM.

### Phase E: Output

**E1. Tier assignment** gates on the verdict, then tiers by channel agreement:

- The RA/Sonnet verdict gates the paper: RELEVANT is eligible for Tier 1/2, UNCERTAIN goes to Tier 3, NOT-RELEVANT excludes it.
- **Tier 1 (core):** a gold-set member OR a paper found by more than one channel (keyword and snowball).
- **Tier 2:** relevant, found through a single channel.
- **Tier 3:** the uncertain recall net, kept for auditing, not included in the review.
- **The relevance score sorts within a tier**, and does not define it. Sonnet's `compositeScore` is deliberately not blended with the term-match score; channel agreement is the tier basis, the RA verdict the gate. (Anup's baseline instead defined the top tier as score ≥ 7.)
- **Gold papers rank above keyword-and-snowball agreement** within Tier 1: gold membership is a verification signal (frozen, RA-signed) while multi-channel agreement is a discovery signal, so channel independence does not affect the ordering. Keyword-and-snowball agreement stays in Tier 1 as correlated corroboration, stronger than single-channel and still verdict-gated.
- **The meta-analysis-ready subset has two nested definitions, reported separately.**
  - **Topically ready** = (Tier 1 ∪ Tier 2) ∩ the empirical papers that clear the evidence bar: every empirical paper on the topic that passed the verdict. On the pilot, 44 studies.
  - **Estimand-ready (the pooling set)** = the topical set ∩ the estimand gate: papers whose Sonnet-extracted outcome, mechanism/channel, and causal direction match the chapter's primary cell (for the pilot, old-age-security motive → fertility, forward). On the pilot the topical 44 collapses to roughly ten (the RA pass marked 10 RETRIEVE / 30 EXCLUDE of 40 DOI-resolved studies, nine in the primary cell). Off-cell papers are kept for their own cells but cannot pool with the primary motive.

  The review's binding constraint is estimand precision, so the estimand-ready set is the operative output; the topical set reports alongside it as the coverage denominator and to feed off-cell chapters.

**E2. Routing: two non-exclusive streams.** Sonnet's tag routes empirical papers to the meta-analysis / effect-size stream, theory papers to the JEL theory stream, both if a paper is both. This is the empirical-core/theory-canon split the gold's Tier A already makes.

**E3. Recall report.** Report recall at two targets, because the method can recover a topic well while under-recovering the estimand:

- **Topical recall** against the full topical gold: Recall(B) against the unbiased Tier B as the primary figure, Recall(A) on the keyword-reachable core, and the gap Recall(A) − Recall(B) as a diagnostic for query inflation toward keyword-sourced papers.
- **Estimand-filtered recall** against the primary-cell gold (per the A3 tag): did we recover the studies that identify the effect the chapter is about? Measured (`36a`/`36b`): all 247 Tier-B papers estimand-tagged, the CV re-run with the query fixed and the denominator split by cell. Tier B is 65% theory models and only 23% empirical primary-cell. Re-based on the primary cell, topical Recall(B) rises from 72.5% to estimand-filtered 82.5% (88% on high-confidence tags), because the recall the query lost sat in the theory/off-cell tail, not in the papers that identify the effect. The pilot's 72% understated recall of the target; the target's definition, not recall, was the binding constraint.

Also report the hard-tail conditional ceiling (recall on Tier-B papers missed on title, recovered via abstract match) as an optimistic bound: Tier B's snowball was seeded off the keyword set, so Recall(B) inherits a residual keyword bias, flagged wherever quoted; the non-circular check is §7.1's adjudicated inclusion set. Also report per-cluster miss diagnostics, empirical-versus-theory recall separately, and budget spent.

**Benchmark.** A Cochrane-style review targets near-complete recall, so a search conceding ~28% is not yet at benchmark. The pilot's ~72% is a title-only, un-frozen, dry-run lower bound, expected to move once the gold freezes. The adoption bar is estimand-filtered Recall(B) against a frozen gold on one clean end-to-end run, with a target set before the run (§7, moves 2–3).

### Substrate (every stage)

The substrate keys on DOI throughout and runs the §5 title-matching. It provides a project-level persistent cache (records reused across hypotheses, cutting OpenAlex budget), resumable stage outputs, a hard per-run budget cap with graceful fail-and-resume, polite scheduling, bounded retry/backoff, and separate dry-run and production modes.

## 4. The unifying stop principle

One rule governs every "when do we stop?" decision: stop when the marginal recovery of new gold anchors or relevant papers approaches zero, subject to a volume floor against noise (A2, A3, C2, D2a).

## 5. Title-matching machinery

Title matching underlies anchor resolution everywhere. The naive approach, counting shared words between two titles (the Jaccard overlap), is the weak link: a topic-homogeneous corpus inflates it, short titles swing it, and subtitle, punctuation, and translation differences break it. The standard:

- **Normalize first:** strip the subtitle, fold case, punctuation, and diacritics, expand `& → and`.
- **Compare with TF-IDF cosine similarity**, not raw word overlap, down-weighting the ambient vocabulary every paper shares, with an author-surname + year secondary gate.
- **Context-dependent threshold:** ≈ 0.80 to select a match from a blind search, ≈ 0.50 to verify an already-proposed DOI. Always verify against independent metadata (Crossref), never an unconfirmed corpus title, because a stored title can itself be the wrong paper (the DOI-shuffle bug, evaluation §5).

## 6. Decision ledger (contradictions resolved)

The three methods disagreed on six points, resolved as follows:

| Item | Resolution |
|---|---|
| **C1: budget allocator** | Cross-validation on the recall/budget frontier (heuristic allocator retired). |
| **C2: title matching** | Normalize → TF-IDF cosine → author+year gate; ≈0.80 to select, ≈0.50 to verify; verify against independent metadata. |
| **C3: resolution policy** | Production resolves DOI-first with a guard; the gold set resolves by title, keeping unresolvable papers so the denominator stays unbiased. |
| **A1: query algebra** | AND across the two axes, OR within each axis. |
| **A2: the three signals** | Relevance score, relevant/maybe/not label, and discovery-channel origin are three deterministic signals feeding one LLM+RA verdict; none is the verdict. |
| **A3: discovery philosophy** | Measure and structure the search; Anup's single trusted query is the fallback/bootstrap mode. |

For future hypotheses the three signals are four fields on one record, so nothing needs reconciling. This does not retroactively answer the comparison on the legacy corpus, where three people ran separately; the old cross-method mapping survives as the legacy migration and the substrate for §7.1, since each legacy paper's method-of-origin memberships are the disagreement matrix that comparison needs.

## 7. Open items: the road to adoption

GACS is a promising design shown in parts, not yet the review's adopted search. Five moves close the gap, in priority order; the first three are sequenced.

1. **Run the head-to-head comparison** the assignment asked for. *(Done, §7.1.)*
2. **Freeze the gold, then do one clean end-to-end production run.** RA-adjudicate the 52 Tier-B UNCERTAINs and sign off Tier A, then run gold-freeze → tuned query → fresh screen → tiers once, end to end, with the OpenAlex budget wired in. This replaces three component stand-ins with a single number chain.
3. **Measure estimand-filtered recall, not just topical recall.** *(Done.)* Gate implemented (`34_estimand_gate.py`; 40 → 10, 7 of 15 anchors off-cell); the RA calibrates the automated gate (100% precision / 80% recall, blind; `35a`/`35b`) so it runs on hypotheses with no RA pass; Tier B estimand-tagged and recall re-graded (`36a`/`36b`; the numbers are in E3). **The audit closes the residual** (`39a`/`39b`): an independent blind reader re-tagged 129 of 247 papers (all 99 abstract-bearing + 30 title-only) and the RA resolved the disagreements. On the adjudicable stratum, auto agrees on 93% (kappa 0.84), with zero THEORY→PRIMARY leakage (0/67) and PRIMARY precision 9/11. Estimand Recall(B) is stable to <1pp (82.5% → 81.8% audit-corrected; envelope 81.8–83.0%).
4. **Fit every parameter and write the defaults down** (§7.2), then hand the pipeline to a second RA to run without the author present. Reproducing a run from the written defaults meets the "no oral tradition" bar.
5. **Replicate on a second hypothesis**, ideally a well-studied one with prior meta-analyses, to exercise the cold-start bootstrap (§A3).

### 7.1 Head-to-head comparison (`37_method_comparison.py`)

The three methods raced against the 10-study estimand-ready ground truth on the disagreement matrix, false-negative rate, false-positive rate, cost, and replicability. **First finding, before any metric: only Anup's set survives as frozen data.** Alexandra's prototype and Shravan's gold-anchored query never ran independently. So each method operationalizes as a reproducible rule over the common 8,087-paper corpus; Anup's and the gold-anchored rules are faithful, Alexandra's is a labeled reconstruction. Results:

- **Agreement is weak:** the three Tier-1 sets share only 8 of 200 papers (pairwise Jaccard 0.07–0.13), so "three routes, one spine" overstates the paper-level overlap.
- **FN (recall of the 10 effect-identifying studies):** Anup 9/10, gold-anchored 7/10, Alexandra 7/10. The gold rule's extra misses are single-channel truth papers routed to its Tier-2 by design, a boundary artifact.
- **FP:** raw FP is uninformative (near 90% for every method); the meaningful off-cell-empirical rate is Anup 27%, gold-anchored 56%, Alexandra 57%.
- **Replicability** is the sharpest differentiator: only the committed methods can be re-run.

The recommendation: no search rule is estimand-precise on its own, so the pipeline's value is not that the methods agree but that they share the same downstream gap, which the estimand gate closes regardless of which search wins. Freeze every method's corpus before any future bake-off.

### 7.2 Parameter defaults (proposed: fit and confirm in the clean run)

Every knob gets a written default and a one-line justification, so the pipeline is runnable without its author. Defaults are provisional until the clean run (move 2) confirms them.

| Parameter | Proposed default | Justification |
|---|---|---|
| CV breadth grid (Nf, Np) | {0, 10, 20, 30, 40} | Pilot CV saturated at N ≈ 20–30; the grid brackets it. |
| CV folds | 10 | Standard; enough given ~50 empirical anchors. |
| Cluster-merge overlap threshold | Jaccard ≥ 0.6 on retrieved gold sets | Merges near-synonymous families without collapsing distinct ones (run `38`: no pair reaches 0.6; see below). |
| Snowball yield floor | < 1 new relevant / 50 records pulled | Diminishing-returns cutoff on the scarce OpenAlex budget. |
| Snowball consecutive rounds | 2 rounds below floor | Guards against a single lumpy dip. |
| Forward-citation cap | topic-specific seeds only, ≤ 1 hop | Forward citations explode on broad theory anchors; 7 of 8 pilot ghosts were forward. |
| Backward-citation depth | all backward refs, ≤ 1 hop | Cheaper and cleaner than forward (the pilot's one backward ghost was valid). |
| D1 keyword budget cutoff | top ~2× the expected include count | Bounds the LLM/RA funnel; non-keyword channels bypass it. |
| Haiku recall calibration | recall ≥ 0.98 vs. frozen gold | Haiku false-negatives are unrecoverable. |
| Bootstrap gold-size floor | ≥ 30 empirical anchors before CV | Below this the fold-local term mining is too noisy (pilot gold ≈ 31 empirical). |

**Cluster count.** The five hand-estimated cause-axis families were expected to collapse to three or four; on the frozen gold they do not (`38_cluster_overlap.py`). No pair reaches Jaccard 0.6, so the count is five. The closest pair, formal-pensions × SS/PAYG, shares only 29% of its combined retrieval (Jaccard 0.29); the count would fall to four only if the merge bar relaxed to ≈0.25. Each family earns its own budget. (Caveat: 56/303 gold anchors and 148/247 Tier B are title-only; abstracts could nudge a borderline pair, not the block structure.)

### 7.3 Remaining engineering / hygiene items

- **Full calibration run** ("Part-4-full", the engine for move 2): wire in the OpenAlex budget, add abstract matching, finalize the hard-tail bound, refit on the frozen gold, produce the production query, promote to `.claude/workflows/`.
- **Legacy migration:** fold the old-age-security corpus into the unified tier scheme (also the substrate for §7.1).
- **PI data-hygiene ticket:** re-key on DOI; fix the snowball DOI-shuffle bug; add an abstract-or-live-DOI gate and a harder forward-citation cap on Tier B.

## 8. Provenance

Method notes harmonized here: `*-gold-anchored-keyword-method.md` (Shravan), `*-query-clustering-method.md` (Alexandra), `*-hybrid-discovery-method.md` (Shravan), and Anup's prioritized corpus. Task-A build: `source/build/goldset/`, `*-gold-set-build-log.md`, Parts 1–4. Drafted 2026-06-30 from the Task-B workshop; finalized 2026-07-03; revised 2026-07-06.

## 9. Changelog: response to the PI critique (2026-07-06)

Each of the PI's seven concerns maps to a change. Concerns 1 and 2 are conceded and fixed now (the numbers are in §7 and §7.1); the rest are conceded and converted into sequenced open items (§7).

| # | PI critique | Response |
|---|---|---|
| 1 | Optimizes topical recall; the binding constraint is estimand precision (44 → ~10) | Conceded, fixed: the estimand gate runs through A3/D2b/E1/E3, calibrated and audited on the pilot (§7, move 3). Recall of the target was never the constraint, its definition was. |
| 2 | A synthesized 4th method, not the assigned head-to-head | Conceded and run (§7.1); search choice matters less than the estimand gate. |
| 3 | Validated in components, not end to end | Conceded; §7, move 2 (one clean run). |
| 4 | 72% is both low and soft | Conceded; E3 benchmark paragraph sets the adoption bar as estimand-filtered Recall(B) on a frozen gold. |
| 5 | Circularity not escaped: Tier B seeded off the keyword set | Conceded; E3 flags the residual bias, §7.1's adjudicated set is the non-circular check. |
| 6 | Too complex; unset knobs = oral tradition | §7.2 defaults table + move 4 (second-RA test); cluster count now run (`38`), the five families stay five. |
| 7 | One hypothesis; generalization untested | Conceded; move 5. |

**Kept at the PI's recommendation:** the frozen-gold instrument, fold-local discriminative-term mining, channel-agreement tiering, and the data-hygiene fixes. All four carry into every chapter unchanged.
