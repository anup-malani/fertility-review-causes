# Canonical Search Workflow — Gold-Anchored Clustered Search (GACS)

**Status:** finalized (2026-07-03) — for RA/PI review and external readers

**Synthesis author:** Shravan (RA), harmonizing the three independently-developed team methods

**Companion:** `canonical-search-workflow-evaluation.md` — how GACS performs on the pilot, with the
recall numbers, costs, and limitations. This document specifies *what the method is*; the companion
evaluates *how well it works*.

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

That convergence is this document's central methodological warrant: three people, three routes, one
spine. The task is therefore not to reconcile rival pipelines but to **document the one pipeline they
all point to, and wire each person's distinct contribution into the leg it hardens.**

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
  empirical recall.
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
  on the papers Haiku passed.
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
- **The meta-analysis-ready subset** = (Tier 1 ∪ Tier 2) ∩ the empirical papers that clear the
  evidence bar.

**E2. Routing — two non-exclusive streams.** Sonnet's tag routes each paper: **empirical papers → the
meta-analysis / effect-size stream; theory papers → the JEL theory-section stream;** both streams if a
paper is both. This is the same empirical-core/theory-canon split the gold's Tier A already makes.

**E3. Recall report.** Report **Recall(B)** — recall against the unbiased Tier B — as the primary,
honest figure; **Recall(A)** on the keyword-reachable empirical core; and the **gap Recall(A) −
Recall(B)** as a diagnostic for whether the query is inflated toward keyword-sourced papers. Also
report the hard-tail conditional ceiling (recall on the Tier-B papers the two-axis query misses on
title, recovered via abstract match) as a **bound** — an optimistic one, because Tier B's snowball was
seeded off the keyword set. Finally, report per-cluster miss diagnostics (which feed query revision),
empirical-versus-theory recall separately, and the budget spent. (The pilot's actual numbers are in
the companion evaluation.)

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

**Commensurability dissolves under unification.** In the legacy old-age-security corpus, three people
ran their methods separately, so their outputs had to be reconciled — the relevance score against the
relevant/maybe/not label against the discovery channel. The unified pipeline emits all of these as
**four fields on one record**: the deterministic label (Alexandra's relevant/maybe/not), the relevance
score (Anup's/Sonnet's `compositeScore`), the discovery-channel provenance — gold, keyword, snowball,
verdict — (Shravan's), plus the RA verdict. So there is nothing to reconcile for future hypotheses. The
old cross-method mapping survives only as a **one-time migration** for the legacy corpus (and as a
developer tool when A/B-testing methods).

## 7. Open items

- **Overlap test** on the existing gold, to settle the pilot's sub-cluster count (five versus three or
  four) empirically.
- **Parameters still to fit:** the cross-validation breadth grid; the snowball saturation thresholds
  (per-cluster yield-per-budget, the consecutive-round count, and the forward-versus-backward caps);
  the D1 budget cutoff; the Haiku recall-calibration threshold; the cluster-merge overlap threshold;
  and the bootstrap gold-size floor.
- **Full calibration run** (the "Part-4-full" task): wire in the real OpenAlex universe-size budget,
  add abstract matching, finalize the hard-tail bound, refit on the frozen gold, produce the
  production query, and promote the pipeline to `.claude/workflows/`.
- **Legacy migration** script: fold the existing old-age-security corpus into the unified tier scheme.
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
- This synthesis: drafted 2026-06-30 from the Task-B design workshop; finalized 2026-07-03.
