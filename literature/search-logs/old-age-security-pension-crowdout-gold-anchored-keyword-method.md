# Gold-Anchored Keyword Search with Cross-Validated Recall (v2 method)

**Date:** 2026-06-26 · **Author:** Shravan (RA), with Claude Code
**Hypothesis:** old-age-security / pension-crowdout (C.3.c) — pilot for the project search pipeline
**Status:** design spec. Supersedes the citation-snowball discovery experiment
(`old-age-security-pension-crowdout-hybrid-discovery-method.md`) as the *primary* discovery method.
Not yet implemented.

---

## 1. Why this replaces the citation-first method

The hybrid top-down→snowball→filter method plateaued at **~30% recall** of the baseline relevant
set after two rounds, and the autopsy showed the ceiling is *structural*: OpenAlex's citation graph
genuinely does not connect some canonical papers (Children-as-Retirement-Saving, Austria, Chile,
China). Two properties of that ceiling made it unacceptable:

1. **Unmeasurable** — recall could only be guessed by benchmarking against a baseline corpus we
   don't fully trust.
2. **Unbuyable** — you cannot move it without better citation edges, which we don't control.

This method swaps that for a **keyword-lexical** approach whose recall ceiling is, by contrast:

1. **Measurable** — via relative recall against a quasi-gold-standard (QGS) set, and
2. **Buyable** — adding synonyms/term-variants to a query block raises recall directly.

We are not eliminating a recall ceiling; keyword search has its own, from vocabulary mismatch. We are
trading an opaque, fixed ceiling for a visible, movable one. That is the whole case for the pivot.

## 2. Method overview

```
Gold set (QGS), DOI-keyed, stratified, two provenance tiers (§3)
        │
        ├── External term backbone (published review search strings) ── leakage-free, fixed every fold
        │
        ▼
k-fold CV (k=10) over the gold set:
   train fold ──► mechanical term extraction (discriminative ranking vs. on-disk negatives, §5)
              ──► Boolean query = backbone  +  gold-mined expansion at breadth N (§4)
   held-out fold ──► measure recall + per-block miss diagnostics (§6)
        │
        ▼
Tune the per-block breadth VECTOR to maximize CV held-out recall
   subject to universe size ≤ screening budget K   (budget-allocation problem, §4)
        │
        ▼
Refit at chosen breadth on the FULL gold set ──► single production query
        │
        ▼
Run production query ──► existing two-stage LLM screen (Haiku → Sonnet) pays for high recall
        │
        ▼
Report: powered relative-recall on Tier A; ceiling probe/estimate on Tier B (§7)
```

## 3. The gold set (QGS)

The load-bearing component. Construction rules:

- **DOI-keyed, never W-ID.** OpenAlex merges works and reassigns W-IDs; W-ID joins silently
  mis-match. (Project-wide finding from the snowball autopsy.)
- **Stratified for *representativeness*, not for per-stratum estimates.** Span theory / each
  natural-experiment setting / each era so aggregate recall generalizes. Do **not** attempt
  per-stratum recall numbers — at gold-set sizes of 60–100, a stratum holds ~10 papers and its
  recall SE is ~±11% (1 SE); per-stratum recall is unpowered. Stratification ensures coverage,
  the diagnostics live at the *block* level (§6).
- **Target size 80–100; 60 is the quotable floor.** At p≈0.85 true recall, aggregate CV recall has
  1-SE ≈ ±4.6% at n=60, ±3.6% at n=100. Below 60 the estimate is not quotable.

### Two provenance tiers — the central correctness rule

> **A gold set drawn from the output of search method X cannot measure method X's recall ceiling.**

The on-disk PI relevant set (`*-prioritized.json`) contains **44 distinct strong-identification
empirical studies** — deep enough to fill an empirical quota. But that set is the output of the PI's
*keyword* screen. Validating a *new keyword* query against it is circular: keyword-missed
(vocabulary-disconnected) papers are absent by construction, so relative recall against it is blind to
the exact ceiling we want to measure. So we split the gold set by provenance:

- **Tier A — bulk / powered.** Sourced from the on-disk 44 + canon + anchor related-work
  (Danzer–Zyska, Boldrin–De Nardi–Jones, Cigno–Werding, Fenge–Scheubel). Powers the headline
  relative-recall number. **Optimistic by construction** (keyword-findable by provenance).
- **Tier B — adversarial / keyword-disconnected.** Sourced by a mechanism *orthogonal to keywords* —
  the citation snowball (now repurposed from discovery engine to independent auditor) and prior
  reviews' own snowballed inclusions. Seeds: the snowball's confirmed-relevant-but-keyword-absent
  papers (Child Support & Endogenous Fertility 2017; How Pension Systems Influence Fertility 2009;
  Mixing Bismarck 2009; Cigno–Werding) and its hard misses (Chile, China, Austria,
  REStud Children-as-Retirement-Saving).

**Recall(A) − Recall(B) is the vocabulary-bias correction — measured, not assumed.**

**The binding scarce resource is Tier B.** We currently have ~9 keyword-disconnected papers — enough
to *probe* the ceiling, not to *estimate* it. The recommended path (§8) is to grow Tier B via an
orthogonal-discovery pass *before* building folds, so the correction becomes an estimate rather than a
hand-wave. A v1 fallback that ships with a probe-only Tier B is documented in §8.

## 4. The tunable knob: per-block breadth as a budget-allocation problem

- **Boolean structure: 2 blocks**, conjoined: `(fertility/childbearing terms) AND (pension/social-
  security/old-age terms)`. Keep it 2-block: every additional AND-ed block multiplies miss
  probability. Buy recall *within* blocks via synonymy, not via more blocks.
- **Knob = per-block breadth vector** (N_fertility, N_pension), **not a scalar.** A global N
  over-spends precision on the easy block (everyone says "fertility"/"childbearing") and starves the
  hard one (pension / social security / old-age insurance / superannuation / provident fund /
  retirement transfer …). Under an AND, a gold paper is missed if *any one* block fails, so recall
  leaks per-block and the blocks don't leak equally.
- **Constraint: fixed screening budget**, universe size ≤ K. Because recall and universe are both
  monotone increasing in each N, the budget binds — so the real problem is not "how big a query" but
  **allocate a fixed query budget across blocks to maximize cross-validated held-out recall.** This is
  the synthesis of the two design choices (breadth knob + fixed budget) into one constrained
  optimization, and it is the defensible thing to report.
- **Vocabulary-independent recall levers** (raise the ceiling the allocation works under, still
  lexical): truncation/wildcards and spelling variants baked into every block (`fertilit*`,
  `pension*`, `old[- ]age`, plurals, US/UK); and OR-in OpenAlex concept/topic tags as an extra recall
  block that catches papers the index tagged "fertility" even when the author's phrasing never says
  it.

## 5. Term sourcing — split by leakage

- **External backbone (leakage-free, fixed in every fold):** terms from the *published search
  strings* of prior systematic reviews/meta-analyses. These never touch held-out gold labels, so they
  are exempt from fold discipline and do work for free.
- **Gold-mined expansion (CV-disciplined, fold-local):** uni/bigrams harvested from the *training
  fold's* gold papers only. The breadth knob N controls how much of this expansion bolts onto the
  backbone. CV then measures the *marginal* recall contribution of the gold-mined expansion — exactly
  the quantity being tuned, with no circularity.
- **Discriminative ranking, not raw frequency.** Rank candidate terms by how much they separate
  gold-positive from the **4,540 on-disk screened NOT_RELEVANT papers** (log-odds / "fightin'-words"),
  not by tf-idf alone. This buys precision at fixed recall → under a fixed budget, stretches the
  budget into more affordable recall. Caveat to state in the writeup: those negatives already passed
  the PI's keyword filter, so the separation learned is relevant-vs-near-miss — which is the
  discrimination we want, but it is not a random-database negative.

## 6. Cross-validation

- **k = 10, not quarters.** With a 60–100 gold set, a single held-out quarter (15 papers) has 1-SE
  ≈ ±9% — noise. 10-fold trains each query on ~90% of the gold set, so each fold's query is close to
  the full-set production query → the CV recall is a less biased estimate of what we actually ship.
  Cost is only more OpenAlex query runs (cheap).
- **Report aggregate + per-block recall only.** Never per-stratum (unpowered, §3).
- **Per-block miss diagnostics drive the allocation.** For each held-out miss, record *which block
  failed to match it*. This converts an opaque recall number into an action ("losing 8 of 15 misses on
  the pension block → move breadth budget there"). Powered to catch a gross block gap (9/60 vs 2/60),
  not to fine-tune (5 vs 8 is within noise).
- **Deliverable ≠ any fold-query.** CV chooses the breadth vector; the production query is refit on
  the **full** gold set at that breadth. Quote the CV held-out recall as the honest estimate of the
  production query's out-of-sample recall.

## 7. Honesty mechanisms

- **Frozen validation core.** As screening surfaces obviously-relevant papers not in the gold set,
  fold them only into a growing *development* pool — never into a frozen *validation* core. If the
  validation set co-evolves with the query, the recall estimate inflates.
- **Relative recall is an upper bound conditioned on gold-set coverage.** It cannot certify recall on
  a literature the gold set itself misses. State this.
- **Tier B = ceiling probe (or estimate if grown).** Recall on Tier A is the headline; recall on
  Tier B bounds the true keyword ceiling. With Tier B small, the ceiling is *bounded, not pinned*.

## 8. Build order and the Tier-B decision

**Recommended (grow Tier B first):** the entire reason for the pivot was to stop having an unmeasured
recall ceiling. A v1 that ships with a probe-only Tier B reproduces that gap on the keyword side. So
before building folds, run an orthogonal-discovery pass aimed specifically at keyword-disconnected
relevant papers — prior reviews' included lists run through *their* queries + a targeted snowball off
the 44 — until Tier B is large enough that Recall(A) − Recall(B) is an estimate, not a hand-wave.

**v1 fallback (probe-only):** if appetite/time is limited, build the gold set now, report powered
relative-recall on Tier A plus a Tier-B ceiling *probe*, with the explicit "ceiling bounded, not
pinned" caveat. Treat Tier-B growth as v2.

Build steps:
1. Assemble Tier A (DOI-keyed, stratified, empirical quota from the on-disk 44 + canon).
2. Assemble/grow Tier B (orthogonal source).
3. Freeze the validation core; designate the development pool.
4. Build the external backbone from prior-review search strings.
5. Implement mechanical term extraction (discriminative ranking vs. on-disk negatives).
6. Implement 10-fold CV over the breadth-vector grid with the budget constraint + miss diagnostics.
7. Pick breadth vector at the recall/budget frontier; refit on full gold set → production query.
8. Run production query → existing two-stage LLM screen.
9. Report Recall(A), Recall(B), per-block diagnostics, and the bias correction.

## 9. Open items / limitations

- **Tier B is the binding scarce resource**, not empirical-study count (44 available).
- **No dedicated OAS systematic review exists** to lift a PRISMA included-list from — Bergsvik et al.
  (2021, *PDR*, 35 studies) covers leave/childcare/health/transfers, **not pensions.** The Tier-A
  backbone and seeds come from anchor related-work + the on-disk set instead.
- **Corrupted baseline records** exist (e.g. `W2014516694` labelled "A Fiscal Theory of Social
  Security and Family Size" resolves to a theology paper). Audit independent of search method.
- Database coverage is OpenAlex-only for now; part of any residual ceiling may be DB coverage, not
  query.

## 10. Provenance

Scoping evidence and the deduped empirical-stratum extraction: session scratchpad
`gold-set-seam-scoping.md`. Anchor sources consulted: Danzer–Zyska (2023, AEJ:Policy / IZA DP13048);
PLOS One NRPS-China (2020); Bergsvik et al. (2021, *PDR*); Wikipedia old-age-security-hypothesis
canon. On-disk corpus: `old-age-security-pension-crowdout-prioritized.json` (542 tiered RELEVANT,
44 distinct strong-identification empirical).
