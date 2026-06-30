# Canonical Search Workflow — Gold-Anchored Clustered Search (GACS)

**Status:** initial draft (2026-06-30) — for RA/PI review, not frozen

**Synthesis author:** Shravan (RA), harmonizing the three independently-developed team methods

**Scope:** the per-hypothesis discovery → screening → tiering pipeline for every chapter of the
Fertility-Explanations Systematic Review. Designed to be **generalizable** across hypotheses, not
OAS-specific. Old-age-security / pension-crowdout (C.3.c) is the worked pilot.

---

## 1. The convergence claim

Three team members independently designed search methods for the OAS pilot, from three starting
points, and **converged on the same architecture.** Alexandra's closing synthesis (her
`*-query-clustering-method.md` §8) is almost verbatim the spine agreed on 2026-06-28:

> Gold set defines what must be recovered. Query clusters define where and how to search.
> Cross-validation chooses cluster/query breadth under a fixed budget. LLM/RA screening decides
> inclusion, with theory papers routed to theory synthesis and empirical papers routed to
> meta-analysis.

That convergence is this document's central methodological warrant: three people, three routes, one
spine. The task is therefore not to reconcile rival pipelines but to **document the one pipeline
they all point to, and wire each person's distinct contribution into the leg it hardens.**

## 2. Framing and attribution

**Anup's end-to-end pipeline is the load-bearing skeleton.** It is the only one of the three that
ran at scale (6,400 screened, ~542 RELEVANT) and produced the baseline corpus the other two operate
on. The two RAs did not build rival spines; each deepened one leg of Anup's pipeline.

| Pipeline leg | Origin (Anup) | Hardened by |
|---|---|---|
| Keyword discovery | single broad relevance-ranked query | **Alexandra** — vocabulary clustering + anchor-guided budget allocation |
| Citation snowball | 1-hop snowball | **Shravan** — orthogonal recall auditor + Tier-B feeder, saturation stop |
| Measurement | (trusted `compositeScore` ranking) | **Shravan** — frozen DOI-keyed gold set, 10-fold CV, recall estimation |
| LLM inclusion | Sonnet prioritization → `compositeScore` | two-stage Haiku→Sonnet→RA funnel |
| Output tiers | `compositeScore` T1/T2/T3 | **Shravan** — channel-convergence tiers, commensurable signals |
| Data hygiene | — | **Shravan** — DOI re-keying, phase-2 snowball DOI-shuffle fix, propose→verify→adjudicate resolver |

The genuinely new objects neither Anup nor a single-query baseline had: the **gold set as an explicit
measurement instrument**, **CV-tuned breadth**, the **clustering structure**, the **data-hygiene
fixes**, and the **commensurable tiering**.

## 3. The pipeline

Five phases plus a cross-cutting substrate. Every stage is DOI-keyed.

### Phase A — Build the instrument (once per hypothesis)

**A1. Intake.** State the hypothesis as `cause → effect` with a short mechanism description.

**A2. Decompose into axes and clusters.** The query is a Boolean of two **conceptual axes**:

```
( effect-axis )  AND  ( cause-axis )
```

with **AND across axes, OR within each axis** (the A1 algebra). Concretely:

- **Effect axis** = a **constant core** (`fertility, births, total fertility rate, family size,
  completed fertility, parity, number of children`), built once for the whole review, **plus a
  per-hypothesis mechanism-flavored extension.** The effect cluster is *not* strictly constant: how
  a paper names the outcome is mechanism-dependent (the OAS literature says *value of children,
  children as old-age support, number of sons*, not *fertility/births*), and a strictly constant
  effect cluster reproduces the Part-4 "fertility block binds" recall miss. The salient effect facet
  also shifts by target phenomenon (tempo/postponement for the SDT, marital-stopping for the FDT,
  natural-fertility spacing for pre-modern).
- **Cause axis** = a disjunction of **vocabulary sub-clusters**, swapped per hypothesis (for OAS:
  formal pensions / social-security-PAYG / OAS-motive / children-as-support / intergenerational
  transfers).

*Within* each cluster, optimize for **recall** — include ambiguous-but-common terms — because
precision comes from the cross-axis AND, not from per-term specificity. Each cluster = a
high-precision **core** (always in) + a **breadth extension** tuned by CV (Phase B).

**Granularity (how many sub-clusters):** the split unit is the **vocabulary family**, not the
mechanism. This generalizes a mechanism rule: it reduces to one-per-mechanism when mechanisms have
distinct vocabularies, splits further when one mechanism sprawls across vocabularies (OAS), and
merges when distinct mechanisms share vocabulary. Distinctness is measured by **retrieval/anchor
overlap in the gold set** (Jaccard on retrieved sets); merge two candidate families past an overlap
threshold. **Stop** adding families when a new one recovers no new gold anchor **and** adds
negligible unique candidate volume (the volume floor guards against thin-gold under-splitting). The
count is data-derived, not hard-coded — Alexandra's five is a hand-estimate; applied rigorously OAS
plausibly collapses to 3–4. *(Open: run the overlap test on the existing gold to settle the OAS
number empirically.)*

**A3. Gold-set construction (the measurement spine).** A frozen, DOI-keyed gold set:

- **Tier A** = empirical core (`evidenceType` + `identification` meeting the bar) + theory canon,
  **kept separate** (theory is not counted as empirical recall).
- **Tier B** = an *unbiased* orthogonally-sourced sample (def-1): take the snowball-relevant set
  whole; do not filter for keyword-absence.
- **Resolution:** gold/measurement-set resolution uses the **title-keyed unbiased** method —
  unresolvable (dead/drift) papers are kept title-keyed, never dropped, so the recall denominator is
  not biased toward findable papers.
- **Freeze** on RA sign-off.

**Cold-start bootstrap.** A new hypothesis has no Anup baseline corpus to mine the gold from, and a
gold mined from a single search is captive to that search's blind spots (the recall yardstick would
be circular). So the gold is built from **multiple deliberately-orthogonal channels, cheapest-first:**

1. **Prior meta-analyses / systematic-review included-study lists** → empirical anchors *by external
   authority* (no search, no screening). The privileged seed. *(Leakage wall: a meta-analysis's
   search-strings feed terms, its included-studies feed anchors — never the same study to both.)*
2. **Top-down theory/canon enumeration** (Opus seeds, causal-direction-checked) → theory canon +
   classic empirical anchors, resolved via the C2 guard.
3. **Citation snowball from the (1)+(2) seeds** → the orthogonal recall channel and Tier-B feeder.
4. **Only if the gold is still below the CV floor:** Anup's broad single-query search + a structured
   LLM/RA screen (must emit `evidenceType` + `identification`). This is the permanent job of Anup's
   fallback mode — the last, most expensive channel.

Bootstrap cost scales with how well-studied the hypothesis is (a hypothesis with prior meta-analyses
may never need channel 4). **Metric integrity:** Tier B must come from channels 1–3, never channel
4, or Recall(B) is circular. Channels 2–3 are a generalization of Shravan's hybrid top-down→snowball
experiment, whose true home is the bootstrap gold-builder rather than production.

**A4. Term population.** External **core** = theory papers + meta-analyses + prior-review strings
(leakage-free). Recall **extension** = fold-local gold-mined discriminative terms (Fightin'-Words
log-odds). The fold-local discipline is mandatory: a new RA must not mine query terms and measure
recall on the same papers.

### Phase B — Calibrate

**B1. Cross-validation.** 10-fold CV over the per-cluster breadth vector picks breadth on the
**recall/budget frontier**, and **the CV is also the budget allocator** across clusters (the
heuristic cluster-scoring allocator is retired). Output = the production query.

### Phase C — Search

**C1. Clustered keyword search** under the CV-chosen budget; **union** across clusters; **DOI-first**
production resolution with the C2 title guard.

**C2. Citation snowball** from cluster-balanced seeds — the orthogonal recall auditor and Tier-B
feeder. **Saturation stop:** marginal new-relevant **yield per unit budget** (diminishing returns on
the scarce OpenAlex resource), measured **per cluster**, requiring **K consecutive** sub-threshold
rounds. Gold-anchor recovery **calibrates** the threshold (verify held-out anchors the snowball did
not plant were recovered; loosen if it stopped too early) but is **not** the live stop — that would
be circular, since the snowball feeds Tier B. **Forward** citations get a harder cap than backward
references and are gated to topic-specific seeds (forward on general theory anchors explodes).

**C3. Dedup + union** (DOI → normalized title).

### Phase D — Screen (three sieves of rising cost + a human gate)

- **D1 — deterministic rank (free):** orders records (Alexandra's features + channel provenance
  G/K/S/V) and imposes a budget cutoff. Semantically blind. **Orthogonal-channel papers
  (snowball/gold, weak keyword signal) bypass the D1 cutoff** and go straight to Haiku — the cutoff
  applies within the keyword channel only, or the term-match would drop exactly the orthogonal-recall
  papers the architecture exists to catch.
- **D2a — Haiku (cheap):** semantic **recall-preserving** filter — when in doubt, pass up. A Haiku
  false-negative is unrecoverable, so calibrate it against the frozen gold (require recall ≈ 1.0);
  do not drop title-only papers for a missing abstract.
- **D2b — Sonnet (expensive):** **precision** judge + structured extraction (`evidenceType`,
  `identification`, mechanism/cluster tag, `compositeScore`). Runs only on Haiku survivors.
- **RA — verdict gate** on boundary cases. The RA verdict is the inclusion decision; the three
  deterministic signals only feed it.

**Adaptive depth:** large candidate pool → `D1 → Haiku → Sonnet → RA`; small pool → skip Haiku
(`D1 → Sonnet → RA`), since Haiku cannot earn its fixed overhead on a small pool. The cascade is a
cost-*control*, roughly halving LLM spend versus running Sonnet on everything (~tens of dollars per
hypothesis). The binding costs are the OpenAlex budget (→ substrate cache) and RA time (→ minimize
the uncertain band), not the LLM.

### Phase E — Output

**E1. Tier assignment** — verdict-gated, convergence-tiered:

- The RA/Sonnet **verdict gates**: RELEVANT → T1/T2 eligible, UNCERTAIN → T3, NOT_RELEVANT →
  excluded.
- **T1 Core** = gold-member **OR** found by multiple channels (keyword ∧ snowball).
- **T2** = relevant via a single channel.
- **T3** = the uncertain recall net (retained, not included).
- **`compositeScore` = the intra-tier sort** (pure Sonnet output, *not* blended with the
  deterministic rank). It is demoted from Anup's tier-*definer* (T1 ≥ 7) to the intra-tier sorter;
  channel-convergence is the tier basis and the RA verdict is the gate.
- **Gold ranks above K∩S** within T1 because gold is a *verification* signal (frozen, RA-signed,
  curated) while K∩S is a *discovery/corroboration* signal — categorically different, so channel
  independence is irrelevant to the ordering. K∩S need not be independent; it stays in T1 as honest
  correlated corroboration (still stronger than single-channel, still verdict-gated).
- **Meta-analysis-ready subset** = (T1 ∪ T2) ∩ empirical-meeting-the-evidence-bar.

**E2. Routing — two non-exclusive streams.** Sonnet's tag routes each paper: **empirical →
meta-analysis / effect-size stream; theory → JEL theory-section stream;** both if both. This is the
same split as the gold's Tier A (empirical core vs theory canon).

**E3. Recall report.** Recall(B) primary (def-1 unbiased); Recall(A) on the keyword-reachable core;
**A − B as the inflation diagnostic** (is the query inflated toward keyword-sourced papers?); the
hard-tail conditional ceiling as a **bound** (optimistic, since Tier B's snowball was seeded off the
keyword set); per-cluster miss diagnostics (feed query revision); empirical-vs-theory recall
separately; budget spent.

### Substrate (every stage)

DOI-keying throughout; the C2 title-match machinery; **persistent cache at the project level** (a
record pulled for one hypothesis is reused by the next — cuts total OpenAlex budget as hypotheses
accumulate); **resumable stage outputs**; **a hard per-run budget cap with graceful fail-and-resume**
(prevents the multi-hour `Retry-After` sleep); polite request scheduling; bounded retry/backoff;
separate **dry-run vs production** modes.

## 4. The unifying stop principle

Every "when to stop" decision in the workflow is the **same rule**: *stop when marginal gold-anchor /
new-relevant recovery → 0, subject to a volume-or-K floor against noise.* It governs the granularity
split (A2), the bootstrap (A3), the Haiku recall calibration (D2a), and the snowball saturation (C2).
State it once; reference it everywhere.

## 5. The C2 title-match machinery

Title matching underlies anchor resolution everywhere. Raw title Jaccard is the weak link — a
topic-homogeneous corpus inflates it, short titles swing wildly, and subtitle/punctuation/translation
variance breaks it. The standard:

- **Normalize titles** first (strip subtitle, fold case/punctuation/diacritics, `&→and`).
- Use **TF-IDF cosine**, not raw Jaccard (down-weights the ambient topic vocabulary).
- Add an **author-surname + year secondary gate**.
- Keep the context-dependent threshold: **J ≥ 0.80 when selecting from blind search, J ≥ 0.50 when
  verifying a proposed DOI** — and **verify against independent metadata (Crossref), never an
  unconfirmed corpus title** (the phase-2 shuffle means a stored title can be the wrong paper).

## 6. Decision ledger (contradictions resolved)

| Item | Resolution |
|---|---|
| C1 — budget allocator | CV on the recall/budget frontier (heuristic cluster-scoring retired) |
| C2 — title match | normalize → TF-IDF cosine → author+year gate; 0.80-select / 0.50-verify; verify vs independent metadata |
| C3 — resolution policy | **production** = Alexandra DOI-first + guard; **gold/measurement** = title-keyed unbiased (def-1 preserved) |
| A1 — query algebra | AND across axes, OR within each axis |
| A2 — tier signals | `compositeScore` / relevant-maybe-not / G-K-S-V are three deterministic *signals* feeding one shared LLM+RA *verdict*; none is the verdict |
| A3 — discovery philosophy | measure/structure the search (cluster + CV); Anup's single trusted query = fallback/bootstrap mode |

**Commensurability dissolves under unification.** In the legacy OAS corpus, three people ran
separately, so their outputs needed reconciling (`compositeScore` ↔ relevant/maybe/not ↔ G/K/S/V).
The unified pipeline emits those as **four fields on one record** (D1 label = Alexandra's
relevant/maybe/not; D2 `compositeScore` = Anup's; provenance G/K/S/V = Shravan's; + the RA verdict),
so there is nothing to reconcile for future hypotheses. The Task-A commensurability mapping survives
only as a **one-time migration** for the legacy OAS corpus (and as a dev tool when A/B-ing methods).

## 7. Open items

- **Overlap test** on the existing gold to settle the OAS sub-cluster count (5 vs 3–4) empirically.
- **Parameters to fit:** CV breadth grid; snowball saturation thresholds (per-cluster yield-per-budget,
  K, forward vs backward caps); D1 budget cutoff; Haiku recall-calibration threshold; cluster-merge
  overlap threshold; bootstrap gold-size floor.
- **Part-4-full** (from Task A): wire the real `openalex_universe()` budget, add abstract matching,
  finalize the hard-tail bound, refit on full gold, produce the production query, promote the pipeline
  to `.claude/workflows/`.
- **Legacy migration** script: fold the existing OAS corpus into the unified tier scheme.
- **PI data-hygiene ticket:** re-key the corpus on DOI; fix the phase-2 snowball DOI-shuffle.

## 8. Provenance

- Method notes harmonized: `*-gold-anchored-keyword-method.md` (Shravan), `*-query-clustering-method.md`
  (Alexandra), `*-hybrid-discovery-method.md` (Shravan), Anup's prioritized corpus + `compositeScore`
  tiers.
- Task-A build (the gold-anchored engine this workflow wraps): `source/build/goldset/`,
  `*-gold-set-build-log.md`, Parts 1–4.
- This synthesis: drafted 2026-06-30 from the Task-B design workshop.
