# Pre-registration — estimand-filtered Recall(B) target for the clean end-to-end run

**Registered:** 2026-07-08, by Shravan (RA), **before** the CV refit on the frozen gold is run.
**Purpose:** the canonical workflow's adoption bar (§7.2 benchmark; §7 move 2) requires an explicit
recall target set *before* the clean run, so the run is a genuine test rather than a number read off
after the fact. This file is committed ahead of `42_cv_refit_frozen.py` producing any result.

## What is being measured

The clean run refits the production query on the **frozen gold** (Tier A = 56, Tier B = 257, frozen
2026-07-08, manifest `…-gold-freeze-manifest.json`), selects breadth `(N_f, N_p)` on the CV
recall/budget frontier, and reports recall at two targets against the frozen Tier B. The
**PRIMARY-cell denominator is 57** and is unchanged by the freeze (all 10 promotions were THEORY/OFF).

## Pre-registered targets

| Metric | Pre-registered bar | Rationale |
|---|---|---|
| **Estimand-filtered Recall(B)** (PRIMARY) | **≥ 0.80** | The adoption metric. Must reproduce / not regress from the audited **81.8%** (envelope 81.8–83.0%) now that the gold is frozen and the query is refit rather than fixed at N=30. |
| Topical Recall(B) (secondary) | ≥ 0.72 | Reproduce the pilot's 72.5% topical figure as a sanity check on the refit. |
| Recall(A) − Recall(B) gap | reported, no bar | Diagnostic for keyword-inflation; not a pass/fail metric. |
| Cochrane near-complete (stretch) | 0.90 | The direction of travel, **explicitly not** the pass bar for this title-only pilot run. |

## Decision rule (committed before the result)

- **Estimand-filtered Recall(B) ≥ 0.80** at the CV-frontier breadth → the frozen refit confirms the
  audited recall; GACS clears its own recall adoption bar. Search remains one leg — the estimand gate,
  not recall, is the binding precision constraint (the §7.1 head-to-head finding stands).
- **< 0.80** → treat as a regression from the audited 81.8%; do **not** adopt on this run. Diagnose
  (breadth grid too coarse, frozen-gold refit shifting mined terms, or a denominator artifact from the
  10 promotions) before a second attempt.

## Scope / what this run does and does not include

- **In scope today (on-disk, no external dependency):** CV refit on the frozen gold → production query
  → estimand-filtered Recall(B) vs this target. This is the number chain the adoption bar names.
- **Deferred (live OpenAlex, budget-gated — "Part-4-full"):** replacing `openalex_universe()` (still a
  stub in `22_cv_breadth.py`) with the real universe pull for the production corpus and the real
  universe-size budget denominator. Separable from the recall metric above; scheduled as its own step
  so a daily-cap hit cannot invalidate the frozen-gold recall result.
