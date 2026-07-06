# Canonical Search Workflow — Gold-Anchored Clustered Search (GACS)

**Status:** revised 2026-07-06, incorporating the PI critique — *validated in components, pending a
clean end-to-end run, a gold freeze, and an estimand-gated re-measurement.* This is the revised
design, not yet the review's adopted canonical search; the remaining work is itemized and sequenced
in §7.

**Synthesis author:** Shravan (RA), harmonizing the three independently-developed team methods

**Companions:**
- `canonical-search-workflow-evaluation.md` — how GACS performs on the pilot, with the recall
  numbers, costs, and limitations. This document specifies *what the method is*; that one evaluates
  *how well it works*.
- `canonical-search-workflow-pi-critique.md` — Anup's review of the 2026-07-03 draft. This revision
  responds to it point by point; **§9 is the changelog** mapping each critique to what changed.
- `canonical-search-workflow-estimand-gate.md` — the implementation of the estimand-and-mechanism gate
  (the fix for the PI's first critique): the pilot's output set collapsing 40 → 10 and the corrected
  gold-anchor scorecard. Build step `source/build/goldset/34_estimand_gate.py`.

**Scope:** the per-hypothesis discovery → screening → tiering pipeline for every chapter of the
Fertility-Explanations Systematic Review. Designed to be **generalizable** across hypotheses, not
specific to any one. Old-age-security / pension-crowdout of fertility (chapter C.3.c) is the worked
pilot.

---

## 1. The convergence claim

Three team members independently designed search methods for the old-age-security pilot, starting
from three different places, and **converged on the same architecture.** Alexandra's closing
synthesis (her method note, §8) is almost verbatim the spine the team agreed on:

> Gold set defines what must be recovered. Query clusters define where and how to search.
> Cross-validation chooses cluster/query breadth under a fixed budget. LLM/RA screening decides
> inclusion, with theory papers routed to theory synthesis and empirical papers routed to
> meta-analysis.

That convergence is a real and useful observation: three people, three routes, one spine. But it is
an *observation, not a measurement,* and it does not discharge the comparison the assignment asked
for. The original task was a head-to-head race of the three methods on false-negative rate,
false-positive rate, cost, and replicability, ending in a recommendation — the best single method, an
amalgam, or a weighted average. Asserting that the routes converge is convenient and may well be true,
but it is not the same as *showing* the paper-for-paper disagreement between the three delivered
Tier-1 sets. That comparison is still owed; the data to run it retrospectively already exist (the
three legacy OAS Tier-1 sets), and it is scheduled — its protocol is specified in §7.1. Until it is
run, treat convergence as a hypothesis this document builds on, not a settled result. The constructive
task here is therefore twofold: **document the one pipeline the three routes point to, wiring each
person's contribution into the leg it hardens — and specify the comparison that will test the
convergence claim rather than assume it.**

## 2. Framing and attribution

**Anup's end-to-end pipeline is the load-bearing skeleton.** It is the only one of the three that
ran at scale (6,400 papers screened, ~542 judged relevant) and produced the baseline corpus the
other two build on. The two RAs did not build rival pipelines; each deepened one leg of Anup's.

| Pipeline leg | Origin (Anup) | Hardened by |
|---|---|---|
| Keyword discovery | single broad relevance-ranked query | **Alexandra** — vocabulary clustering + budget allocation guided by the gold anchors |
| Citation snowball | one-hop snowball | **Shravan** — an orthogonal recall auditor and gold feeder, with a saturation stop |
| Measurement | (a single trusted relevance ranking) | **Shravan** — a frozen, DOI-keyed gold set, 10-fold cross-validation, and a defensible recall estimate |
| LLM inclusion | Sonnet prioritization → a relevance score | a staged Haiku → Sonnet → RA funnel |
| Output tiers | relevance-score cutoffs (T1/T2/T3) | **Shravan** — tiers based on how many channels found a paper, with commensurable signals |
| Data hygiene | — | **Shravan** — DOI re-keying, a fix for a snowball DOI-shuffle bug, and a propose→verify→adjudicate resolver |

The genuinely new objects that neither Anup's baseline nor a single-query search had: the **gold set
as an explicit measurement instrument**, **cross-validation-tuned breadth**, the **clustering
structure**, the **data-hygiene fixes**, and the **channel-based tiering**.

## 3. The pipeline

Five phases plus a cross-cutting substrate. Every stage keys records on their DOI.

### Phase A — Build the instrument (once per hypothesis)

**A1. Intake.** State the hypothesis as `cause → effect` with a short description of the mechanism.

**A2. Decompose into axes and clusters.** The query is a Boolean of two **conceptual axes**:

```
( effect-axis )  AND  ( cause-axis )
```

joined **AND across the two axes, OR within each axis.** Concretely:

- **Effect axis** = a **constant core** (`fertility, births, total fertility rate, family size,
  completed fertility, parity, number of children`), built once for the whole review, **plus a
  per-hypothesis, mechanism-flavored extension.** The effect cluster is *not* strictly constant: how
  a paper names the outcome depends on the mechanism (the old-age-security literature says *value of
  children, children as old-age support, number of sons*, not *fertility/births*), and a strictly
  constant effect cluster reproduces a recall miss we observed on the pilot (see the evaluation, §2).
  The salient effect facet also shifts with the target phenomenon — postponement/tempo for the Second
  Demographic Transition, marital-stopping for the First, natural-fertility spacing for the pre-modern
  era.
- **Cause axis** = a disjunction (OR) of **vocabulary sub-clusters**, swapped per hypothesis. For
  old-age security these are: formal pensions / social-security (pay-as-you-go) / the old-age-security
  motive / children-as-support / intergenerational transfers.

*Within* each cluster, optimize for **recall** — include ambiguous-but-common terms — because
precision comes from the cross-axis AND, not from making individual terms specific. Each cluster is a
high-precision **core** (always included) plus a **breadth extension** tuned by cross-validation
(Phase B).

**Granularity — how many sub-clusters.** The unit you split on is the **vocabulary family**, not the
mechanism. This generalizes a simpler "one cluster per mechanism" rule: it reduces to that rule when
mechanisms have distinct vocabularies, splits further when one mechanism sprawls across several
vocabularies (as old-age security does), and merges when distinct mechanisms share vocabulary.
Distinctness is measured by **how much two candidate families overlap in the papers they retrieve
from the gold set** (the Jaccard overlap of their retrieved sets); merge two families once that
overlap passes a threshold. **Stop** adding families when a new one recovers no new gold paper **and**
adds negligible unique candidate volume — the volume floor guards against over-splitting when the gold
is thin. The final count is derived from the data, not fixed in advance: Alexandra's five clusters
were a hand-estimate; applied rigorously, old-age security plausibly collapses to three or four.
*(Open item: run the overlap test on the existing gold to settle the pilot's number empirically.)*

**A3. Gold-set construction (the measurement spine).** A frozen, DOI-keyed set of anchor studies the
query must be able to recover:

- **Tier A** = an empirical core (studies whose evidence type and identification strategy clear the
  quality bar) plus the theory canon, **kept separate** — theory papers are not counted toward
  empirical recall. **Each empirical anchor also carries an estimand-cell tag** — the `cause → effect`
  the study actually identifies, recorded as (outcome, mechanism/channel, causal direction) — because
  topical membership and estimand membership are not the same set. On the pilot this mattered: of the
  14 primary-cell gold anchors, seven identify something *other* than the old-age-security → fertility
  effect — four on a different outcome (child schooling, parental survival, maternal labor supply,
  child height), two through the grandparental-childcare channel (opposite in sign, and as it turns out
  central to the Second Transition), and one reverse-direction (fertility instrumented to test the
  mechanism). A gold that is topically relevant but estimand-heterogeneous makes recall against it a
  measure of *topic* coverage, not of *estimand* coverage. The tag lets us build the
  **estimand-filtered gold** the recall report needs (§E3) without discarding the topical anchors,
  which stay useful for the broader coverage figure and for routing the off-cell papers to their own
  chapters and to the theory stream.
- **Tier B** = an **unbiased, orthogonally-sourced sample**: take the snowball-relevant set *whole*,
  without filtering for keyword-absence. (We call this the "unbiased-sample" definition of Tier B; the
  point is that Tier B is a fair yardstick for recall precisely because it was *not* curated to match
  the query.)
- **Resolution.** Gold papers are resolved to canonical records by **title**, and papers whose
  identifiers are dead or have drifted are **kept, keyed on title** — never dropped. Dropping them
  would bias the recall denominator toward easy-to-find papers.
- **Freeze** the set on RA sign-off.

**Cold-start bootstrap.** A brand-new hypothesis has no Anup baseline corpus to mine the gold from,
and a gold built from a *single* search is captive to that search's blind spots — the recall yardstick
would be circular. So the gold is assembled from **multiple deliberately-orthogonal channels,
cheapest first:**

1. **Prior meta-analyses and systematic-review included-study lists** → empirical anchors *by external
   authority*, requiring no search and no screening. This is the privileged seed. *(Leakage wall: a
   meta-analysis's search strings may feed query terms, and its included studies may feed anchors, but
   never the same study to both — otherwise the query is tested on papers it was built from.)*
2. **Top-down theory/canon enumeration** (Opus-generated seeds, each checked for causal direction) →
   the theory canon plus classic empirical anchors, resolved through the title-matching guard (§5).
3. **Citation snowball from the channel-1 and channel-2 seeds** → the orthogonal recall channel and
   the feeder for Tier B.
4. **Only if the gold is still below the cross-validation floor:** Anup's broad single-query search
   plus a structured LLM/RA screen (which must emit an evidence type and identification field). This
   is the permanent job of Anup's fallback mode — the last and most expensive channel.

Bootstrap cost scales with how well-studied the hypothesis is; a hypothesis with prior meta-analyses
may never need channel 4. **Metric integrity:** Tier B must be drawn from channels 1–3, never channel
4 — otherwise the query would be measured against papers its own search produced, and Recall(B) would
be circular. Channels 2–3 are a generalization of Shravan's earlier hybrid top-down→snowball
experiment, whose true home turns out to be the bootstrap gold-builder rather than production search.

**A4. Term population.** The external **core** terms come from theory papers, meta-analyses, and prior
published review search strings (all leakage-free). The recall **extension** terms are mined
*fold-locally* from the gold using weighted log-odds (the Monroe–Colaresi–Quinn "Fightin' Words"
method) — i.e. the terms that best distinguish relevant gold papers from near-miss irrelevant ones.
The fold-local discipline is mandatory: terms are harvested only from the training fold's gold, and
recall is measured on the held-out fold. A new RA must never mine query terms and measure recall on
the same papers.

### Phase B — Calibrate

**B1. Cross-validation.** A 10-fold cross-validation over the per-cluster breadth settings picks
breadth on the **recall-versus-budget frontier**, and the same cross-validation **allocates budget
across clusters** (this replaces the earlier heuristic cluster-scoring allocator). The output is the
production query.

### Phase C — Search

**C1. Clustered keyword search** under the cross-validation-chosen budget; take the **union** across
clusters; resolve records **DOI-first**, with the title-matching guard (§5) as a check.

**C2. Citation snowball** from cluster-balanced seeds — the orthogonal recall auditor and the feeder
for Tier B. **Saturation stop:** keep snowballing until the marginal yield of *new relevant papers
per unit of budget spent* falls below a threshold (diminishing returns on the scarce OpenAlex budget),
measured **per cluster** (clusters saturate at different rates) and requiring **several consecutive
rounds** below threshold, not one lumpy dip. Recovery of held-out gold anchors is used to
**calibrate** the threshold (check that anchors the snowball did *not* itself plant were still
recovered; loosen the stop if it quit too early) — but gold recovery is **not** the live stop signal,
because the snowball feeds Tier B and using it live would be circular. **Forward** citations get a
harder cap than backward references and are restricted to topic-specific seeds — running forward
citations on broad theory anchors explodes the candidate set.

**C3. Deduplicate and union** (by DOI, then by normalized title).

### Phase D — Screen (three sieves of rising cost, plus a human gate)

- **D1 — deterministic ranking (free).** Orders records by a term-match score (Alexandra's
  deterministic features) together with each paper's discovery channel, and applies a budget cutoff.
  This stage is semantically blind. **Papers found through an orthogonal channel (snowball or gold,
  with a weak keyword signal) bypass the D1 cutoff** and go straight to Haiku — the cutoff applies
  *within the keyword channel only*, or the dumb term-match would discard exactly the
  orthogonal-recall papers the whole architecture exists to catch.
- **D2a — Haiku (cheap).** A semantic, **recall-preserving** filter: when in doubt, pass the paper up.
  A Haiku false-negative is unrecoverable, so calibrate Haiku against the frozen gold and require its
  recall to be ≈ 1.0. Do not drop a title-only paper just because it lacks an abstract.
- **D2b — Sonnet (expensive).** A **precision** judge plus structured extraction (evidence type,
  identification strategy, mechanism/cluster tag, and a relevance score, `compositeScore`). Runs only
  on the papers Haiku passed. The evidence-type, identification, and mechanism/cluster fields are not
  merely descriptive metadata — they are the **inputs to the estimand-and-mechanism gate** at E1. So
  Sonnet must emit them for *every* passed paper, in a form comparable to the gold anchors'
  estimand-cell tags: the outcome the paper measures, the mechanism/channel it runs through, and the
  causal direction, so each candidate can be tested for membership in the chapter's primary estimand
  cell. This automated gate is **calibrated against the RA**: on the pilot's 40 studies, judging blind
  on title+abstract, it scored **100% precision / 80% recall** on the primary-vs-off-cell decision
  (zero false positives; the two misses were borderline estimands the RA gate is there to catch). See
  `canonical-search-workflow-estimand-gate.md` and `35b_score_estimand_calibration.py`.
- **RA — the verdict gate** on boundary cases. The RA verdict *is* the inclusion decision; the three
  deterministic signals only feed it.

**Adaptive depth.** With a large candidate pool, run the full `D1 → Haiku → Sonnet → RA` cascade; with
a small pool, skip Haiku (`D1 → Sonnet → RA`), since Haiku cannot earn its fixed overhead on a small
pool. The cascade is a cost-*control*: Haiku recall-filters so that Sonnet runs only on survivors,
which roughly halves LLM spend versus running Sonnet on everything (landing at ~tens of dollars per
hypothesis). The binding costs are the OpenAlex budget (addressed by the substrate cache) and RA time
(addressed by minimizing the uncertain band) — not the LLM.

### Phase E — Output

**E1. Tier assignment** — gated by the verdict, tiered by channel agreement:

- The RA/Sonnet **verdict gates** the paper: RELEVANT → eligible for Tier 1/2, UNCERTAIN → Tier 3,
  NOT-RELEVANT → excluded.
- **Tier 1 (core)** = a gold-set member **OR** a paper found by more than one channel (keyword *and*
  snowball).
- **Tier 2** = relevant, but found through a single channel.
- **Tier 3** = the uncertain recall net (retained for auditing, not included in the review).
- **The relevance score (`compositeScore`) is the sort *within* a tier**, not the definition of the
  tier. It is Sonnet's output, deliberately *not* blended with the deterministic term-match score. In
  Anup's baseline the score *defined* the top tier (T1 ≥ 7); here it is demoted to an intra-tier sort,
  with channel agreement as the tier basis and the RA verdict as the gate.
- **Gold papers rank above keyword-and-snowball agreement** within Tier 1, because gold membership is
  a *verification* signal (frozen, RA-signed, curated) while multi-channel agreement is a
  *discovery/corroboration* signal — categorically different, so whether the channels are statistically
  independent is irrelevant to the ordering. Keyword-and-snowball agreement need not be independent; it
  stays in Tier 1 as honest correlated corroboration — stronger than single-channel, still
  verdict-gated.
- **The meta-analysis-ready subset — two nested definitions, reported separately.**
  - **Topically meta-analysis-ready** = (Tier 1 ∪ Tier 2) ∩ the empirical papers that clear the
    evidence bar. This is the *coverage* set: every empirical paper on the hypothesis's topic that
    passed the verdict. On the pilot this was 44 studies.
  - **Estimand-ready (the pooling set)** = the topical set ∩ the **estimand-and-mechanism gate** —
    papers whose Sonnet-extracted outcome, mechanism/channel, and causal direction match the chapter's
    primary estimand cell (for the pilot: old-age-security motive → fertility, forward direction). This
    is the set that can actually share a pooled estimate. On the pilot the topical 44 collapses to
    roughly ten once the gate applies (the RA inclusion pass marked 10 RETRIEVE / 30 EXCLUDE of 40
    DOI-resolved studies, nine in the primary causal cell). Papers on a different outcome, a different
    channel (grandparental childcare, opposite sign), or the reverse direction are real and are kept
    for *their* cells, but they cannot pool with the primary motive.

  The **binding constraint of the review is estimand precision, not topic coverage**, so the
  estimand-ready set is the operative output for meta-analysis; the topical set is reported alongside
  it as the coverage denominator and to feed the off-cell chapters. *(The gate is **implemented and run
  on the pilot** — `source/build/goldset/34_estimand_gate.py`, documented in
  `canonical-search-workflow-estimand-gate.md`: 40 topical reviewed studies → 10 estimand-ready. The
  remaining piece is the estimand-gated **recall** re-grade against an estimand-filtered Tier B — see
  §7, move 3.)*

**E2. Routing — two non-exclusive streams.** Sonnet's tag routes each paper: **empirical papers → the
meta-analysis / effect-size stream; theory papers → the JEL theory-section stream;** both streams if a
paper is both. This is the same empirical-core/theory-canon split the gold's Tier A already makes.

**E3. Recall report.** Report recall at **two targets**, because the method can recover a topic well
while under-recovering the estimand:

- **Topical recall** — against the full (topically-defined) gold. Report **Recall(B)** (recall against
  the unbiased Tier B) as the primary honest figure, **Recall(A)** on the keyword-reachable empirical
  core, and the **gap Recall(A) − Recall(B)** as a diagnostic for whether the query is inflated toward
  keyword-sourced papers.
- **Estimand-filtered recall** — against the estimand-filtered gold (the primary-cell papers only, per
  the A3 tag). This is the figure that answers the review's actual question: *did we recover the studies
  that identify the effect the chapter is about?* **Measured** (`36a`/`36b`, report
  `{slug}-estimand-recall-regrade.md`): all 247 Tier-B papers were estimand-tagged and the CV re-run
  with the query fixed and the denominator partitioned by cell. Tier B turns out to be **65% theory
  models and only 23% empirical primary-cell**; re-based on the primary cell, **topical Recall(B) 72.5%
  → estimand-filtered 82.5%** (88% on high-confidence tags) — the number moves *up*, because the recall
  the query was losing sat in the theory/off-cell tail, not in the papers that identify the effect. So
  the pilot's 72% *understated* recall of the target while the "44 meta-analysis-ready" *overstated* the
  usable set: recall was never the binding constraint — the definition of the target was.

Also report the hard-tail conditional ceiling (recall on the Tier-B papers the two-axis query misses
on title, recovered via abstract match) as a **bound** — an optimistic one, because Tier B's snowball
was seeded off the keyword set, so Tier B is **not fully orthogonal** and Recall(B) inherits a residual
keyword bias it cannot fully escape (state this wherever the number is quoted; the non-circular check
is the independent adjudicated inclusion set of §7.1). Finally, report per-cluster miss diagnostics
(which feed query revision), empirical-versus-theory recall separately, and the budget spent.

**Benchmark.** A Cochrane-style systematic review targets near-complete recall of the eligible
literature, so a search stage that concedes ~28% is not yet at benchmark. The pilot's ~72% is a
*title-only, un-frozen, dry-run lower bound* and is expected to move — up with abstract matching, and
in both directions once the gold freezes — not a final performance figure. The adoption bar this
document holds itself to: **estimand-filtered Recall(B), measured against a frozen gold on one clean
end-to-end run, with an explicit target set before the run** (§7, moves 2–3). (The pilot's actual
numbers are in the companion evaluation.)

### Substrate (every stage)

DOI-keying throughout; the title-matching machinery of §5; a **persistent cache at the project level**
(a record pulled for one hypothesis is reused by the next, cutting total OpenAlex budget as hypotheses
accumulate); **resumable stage outputs**; **a hard per-run budget cap with graceful fail-and-resume**
(which prevents the multi-hour `Retry-After` sleep when a rate limit hits); polite request scheduling;
bounded retry/backoff; and separate **dry-run and production** modes.

## 4. The unifying stop principle

Every "when do we stop?" decision in the workflow is the **same rule**: *stop when the marginal
recovery of new gold anchors / new relevant papers approaches zero, subject to a volume-or-count floor
that guards against noise.* It governs the granularity split (Phase A2), the cold-start bootstrap
(A3), the Haiku recall calibration (D2a), and the snowball saturation stop (C2). State it once,
reference it everywhere.

## 5. Title-matching machinery

Title matching underlies anchor resolution everywhere in the pipeline, so it needs to be robust. The
naive approach — counting shared words between two titles (the Jaccard overlap) — is the weak link: a
topic-homogeneous corpus inflates it, short titles swing it wildly, and subtitle, punctuation, and
translation differences break it. The standard we use:

- **Normalize titles first** — strip the subtitle, fold case, punctuation, and diacritics, and expand
  `& → and`.
- Compare with **TF-IDF cosine similarity**, not raw word overlap — this down-weights the ambient
  topic vocabulary that every paper in the corpus shares.
- Add an **author-surname + year secondary gate.**
- Keep the context-dependent threshold: require a **high similarity (≈ 0.80) when selecting a match
  from a blind search**, but a **looser one (≈ 0.50) when verifying an already-proposed DOI** — and
  always **verify against independent metadata (Crossref), never against an unconfirmed corpus title**,
  because a stored title can itself be the wrong paper (see the DOI-shuffle bug in the evaluation, §5).

## 6. Decision ledger (contradictions resolved)

The team's three methods disagreed on six points. Each was resolved as follows; the codes are handles
for cross-reference, not required reading.

| Item | Resolution |
|---|---|
| **C1 — budget allocator** | Cross-validation on the recall/budget frontier (the heuristic cluster-scoring allocator is retired). |
| **C2 — title matching** | Normalize → TF-IDF cosine → author+year gate; ≈0.80 to select, ≈0.50 to verify; always verify against independent metadata. |
| **C3 — resolution policy** | **Production** search resolves DOI-first with a guard; the **gold/measurement** set resolves by title, keeping unresolvable papers so the recall denominator stays unbiased. |
| **A1 — query algebra** | AND across the two axes, OR within each axis. |
| **A2 — the three signals** | The relevance score, the relevant/maybe/not label, and the discovery-channel provenance are three deterministic *signals* that feed one shared LLM+RA *verdict*; none of them *is* the verdict. |
| **A3 — discovery philosophy** | Measure and structure the search (clustering + cross-validation); Anup's single trusted query is the fallback/bootstrap mode. |

**Commensurability under unification — with a caveat.** For *future* hypotheses run through the
unified pipeline, the three signals are no longer three people's separate corpora but **four fields on
one record**: the deterministic label (Alexandra's relevant/maybe/not), the relevance score
(Anup's/Sonnet's `compositeScore`), the discovery-channel provenance — gold, keyword, snowball — and
the RA verdict. So for new hypotheses there is nothing to *reconcile*. The caveat the earlier draft
glossed: this unification does not retroactively answer the comparison question on the *legacy* corpus,
where three people genuinely did run separately. That the pipeline *will* emit commensurable fields
going forward is a property of the design; it is not evidence that the three legacy methods agreed. The
old cross-method mapping therefore survives as more than a formality — it is both the **one-time
migration** for the legacy corpus *and* the substrate for the head-to-head comparison in §7.1 (each
legacy paper's three method-of-origin memberships are exactly the disagreement matrix that comparison
needs).

## 7. Open items — the road to adoption

The PI's review (companion critique) sets the bar: GACS is a promising design shown in parts, not yet
the review's adopted search. Five moves, in priority order, close the gap. The first three are
sequenced; §7.1 and §7.2 specify concretely the two the earlier draft left implicit.

1. **Run the head-to-head comparison the assignment asked for** — retrospective, on the legacy OAS
   corpus. Protocol in §7.1. This is the actual owed deliverable, and the data already exist.
2. **Freeze the gold, then do one clean end-to-end production run.** RA-adjudicate the 52 Tier-B
   UNCERTAINs and sign off Tier A, then run gold-freeze → tuned query → fresh screen → tiers *once*,
   end to end, with the real OpenAlex budget wired in — replacing the three component stand-ins (the CV
   dry run, the legacy tier demonstration, the Phase-E migration) with a single number chain.
3. **Measure estimand-filtered recall, not just topical recall.** *(Done.)* The gate is implemented
   (`34_estimand_gate.py`; output set 40 → 10, 7 of 15 anchors off-cell), the automated gate is
   calibrated against the RA (100% precision / 80% recall, blind; `35a`/`35b`) so it runs on hypotheses
   with no RA pass, and Tier B has been estimand-tagged and the recall **re-graded** (`36a`/`36b`):
   topical Recall(B) 72.5% → estimand-filtered **82.5%**, with Tier B revealed as 65% theory / 23%
   empirical primary-cell. See `canonical-search-workflow-estimand-gate.md`. **Residual:** the Tier-B
   tags are automated, not RA-signed — a spot audit of the theory routing would harden the 82.5%. This
   closes the PI's first critique.
4. **Fit every parameter and write the defaults down** (§7.2), then hand the pipeline to a second RA to
   run without the author present. If they can reproduce a run from the written defaults, the "no oral
   tradition" bar is met.
5. **Replicate on a second hypothesis** — ideally a well-studied one with prior meta-analyses — to
   exercise the cold-start bootstrap (§A3) and convert "designed to generalize" into "generalizes."

### 7.1 Head-to-head comparison protocol (owed deliverable)

Take the three independently-delivered Tier-1 sets on the legacy OAS corpus and report, against a
single **adjudicated inclusion set** (the RA-signed Cell-A verdicts):

- **Disagreement matrix** — pairwise overlap of the three Tier-1 sets, paper by paper (Jaccard plus
  the raw shared/unique counts), so the convergence claim of §1 is *shown*, not asserted.
- **False-negative rate** per method — adjudicated-included papers the method missed.
- **False-positive rate** per method — method Tier-1 papers the adjudication excluded.
- **Cost** per method — OpenAlex budget and LLM spend.
- **Replicability** per method — can a second RA reproduce the set from the written spec?

Then recommend the best single method, an amalgam, or a weighted average — the question the assignment
posed. GACS is the amalgam candidate; this comparison is what earns it (or doesn't) the canonical slot,
rather than the convergence assertion standing in for the test. *(The revision author intends to run
this once the pipeline is finalized.)*

### 7.2 Parameter defaults (proposed — fit and confirm in the clean run)

Every knob gets a written default and a one-line justification, so the pipeline is runnable without its
author. Defaults are provisional until the clean run (move 2) confirms them; the point is that there is
a written starting value, not a blank to be filled from memory.

| Parameter | Proposed default | Justification |
|---|---|---|
| CV breadth grid (Nf, Np) | {0, 10, 20, 30, 40} | Pilot CV saturated at N ≈ 20–30; the grid brackets it. |
| CV folds | 10 | Standard; used in the pilot; enough folds given ~50 empirical anchors. |
| Cluster-merge overlap threshold | Jaccard ≥ 0.6 on retrieved gold sets | Merges near-synonymous families (pilot: formal-pensions ≈ SS/PAYG) without collapsing distinct ones. |
| Snowball saturation — yield floor | < 1 new relevant / 50 records pulled | Diminishing-returns cutoff on the scarce OpenAlex budget. |
| Snowball saturation — consecutive rounds | 2 rounds below floor | Guards against a single lumpy dip. |
| Forward-citation cap | topic-specific seeds only, ≤ 1 hop | Forward citations explode on broad theory anchors; 7 of 8 pilot ghosts were forward. |
| Backward-citation depth | all backward refs, ≤ 1 hop | Cheaper and cleaner than forward (the pilot's one backward ghost was real). |
| D1 keyword budget cutoff | top ~2× the expected include count | Bounds the LLM/RA funnel; orthogonal-channel papers bypass it (see D1). |
| Haiku recall calibration | recall ≥ 0.98 vs. frozen gold | Haiku false-negatives are unrecoverable; near-1.0 required. |
| Bootstrap gold-size floor | ≥ 30 empirical anchors before CV | Below this the fold-local term mining is too noisy (pilot gold ≈ 31 empirical). |

*(Still open: the sub-cluster **overlap test** on the existing gold, to settle the pilot's cluster
count — five hand-estimated versus three or four empirically.)*

### 7.3 Remaining engineering / hygiene items

- **Full calibration run** (the "Part-4-full" task): wire in the real OpenAlex universe-size budget,
  add abstract matching, finalize the hard-tail bound, refit on the frozen gold, produce the production
  query, and promote the pipeline to `.claude/workflows/`. This *is* the engine for move 2.
- **Legacy migration** script: fold the existing old-age-security corpus into the unified tier scheme —
  also the substrate for the §7.1 comparison.
- **PI data-hygiene ticket:** re-key the corpus on DOI; fix the snowball DOI-shuffle bug; and — new,
  from the pilot — add an *abstract-or-live-DOI* gate plus a harder forward-citation cap on Tier B, to
  keep ghost citations out of the gold (see the evaluation, §5).

## 8. Provenance

- Method notes harmonized here: `*-gold-anchored-keyword-method.md` (Shravan),
  `*-query-clustering-method.md` (Alexandra), `*-hybrid-discovery-method.md` (Shravan), and Anup's
  prioritized corpus with its relevance-score tiers.
- The Task-A build (the gold-anchored engine this workflow wraps): `source/build/goldset/`,
  `*-gold-set-build-log.md`, Parts 1–4.
- Companion evaluation of this method on the pilot: `canonical-search-workflow-evaluation.md`.
- This synthesis: drafted 2026-06-30 from the Task-B design workshop; finalized 2026-07-03; revised
  2026-07-06 to incorporate the PI critique (see §9).

## 9. Changelog — response to the PI critique (2026-07-06)

This revision responds to `canonical-search-workflow-pi-critique.md`. Each of the PI's seven concerns
is mapped to what changed. Two are conceded and fixed in the method now; the rest are conceded and
converted into sequenced, specified open items (§7), because they require a run this revision does not
itself perform.

| # | PI critique | Response in this revision |
|---|---|---|
| 1 | Optimizes topical recall; the binding constraint is estimand precision (44 → ~10 under the estimand). | **Conceded; gate added AND implemented.** Estimand-cell tags on gold anchors (A3), estimand fields required from Sonnet (D2b), an **estimand-ready pooling set** distinct from the topical set (E1), **estimand-filtered recall** as a reported target (E3). Now *run* on the pilot — `34_estimand_gate.py`, write-up `canonical-search-workflow-estimand-gate.md`: output set 40 → 10; corrected scorecard 7 of 15 anchors off-cell (reconciles with the PI's "7 of 14"). The automated gate is calibrated against the RA (100% precision / 80% recall, blind; `35a`/`35b`), so it runs on hypotheses with no RA pass. And the recall is **re-graded** (`36a`/`36b`): topical Recall(B) 72.5% → estimand-filtered 82.5%, Tier B being 65% theory / 23% empirical primary-cell. **Critique #1 closed** — recall of the target was never the constraint; the target's definition was. |
| 2 | Answered a different question — a synthesized 4th method, not the assigned head-to-head; convergence asserted, not shown. | **Conceded.** §1 downgrades convergence from "warrant" to "hypothesis"; the **comparison protocol** (disagreement matrix + FP/FN + cost + replicability) is specified in §7.1 as the owed deliverable and is scheduled to run. |
| 3 | Validated in components, not end to end; the decision can't be made yet. | **Conceded.** Status line reframed to "validated in components, pending a clean run"; the single end-to-end run is §7, move 2. |
| 4 | 72% is both low (vs. Cochrane near-complete) and soft (dry run, un-frozen, title-only). | **Conceded.** E3 adds an explicit **benchmark** paragraph: 72% is a title-only lower bound, near-complete recall is the target, and the adoption bar is estimand-filtered Recall(B) on a frozen gold with a pre-set target. |
| 5 | Circularity acknowledged but not escaped — Tier B's snowball was seeded off the keyword set. | **Conceded, stated at point of use.** E3 now flags the residual keyword bias in Recall(B) wherever the number is quoted; §7.1's independent adjudicated inclusion set is the non-circular check. |
| 6 | Too complex for anyone but its author; unset knobs = oral tradition. | **Addressed.** §7.2 gives a **parameter-defaults table** (default + one-line justification per knob), and §7, move 4 hands the pipeline to a second RA as the replicability test. |
| 7 | One hypothesis; generalization (the property most needed) untested. | **Conceded.** §7, move 5 keeps second-hypothesis replication (well-studied, with prior meta-analyses) to exercise the cold-start bootstrap. |

**Kept at the PI's recommendation:** the frozen-gold instrument, fold-local discriminative-term mining,
channel-convergence tiering, and the data-hygiene fixes — the PI endorsed all four as contributions to
carry into every chapter, and none is changed here.
