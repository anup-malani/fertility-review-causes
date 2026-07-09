# End-to-end run — honest summary (2026-07-08)

The clean end-to-end result on the old-age-security / pension-crowdout pilot, after the live run
exposed and we cleaned a ghost-contamination problem in the gold. Every number here is on a **real,
existence-verified gold** and reproducible from `source/build/goldset/`.

## The number

**Estimand-filtered Recall(B) = 80.6% (25/31)** — on the rebuilt, floor-clearing gold — **PASSES**
the pre-registered ≥ 0.80 bar. Topical Recall(B) 67.8%. This is the adoption metric, and it is the
end-to-end number for the *search/recall* half of the pipeline.

## How we got here (and what was corrected)

| Stage | Result |
|---|---|
| Freeze gold (Tier A 56, Tier B 257) | done |
| Pre-register target (≥0.80) before any number | done |
| First on-disk recall | 82.5% — **retracted** (gold contained ghosts) |
| Live OpenAlex pull | 11,463 real records (universe 11,738) |
| **Ghost finding** | frozen Tier B was ~40% fabricated snowball citations |
| De-ghost (corpus + Crossref, zero OpenAlex budget) | Tier B 257→152; **105 confirmed ghosts**; PRIMARY 57→21 |
| Rebuild (Crossref-gated canon enumeration) | +25 verified real anchors → **PRIMARY 31 (clears the ≥30 floor)** |
| **Clean recall on rebuilt gold** | **80.6% (25/31) — PASS** |

Two intermediate numbers were **retracted** and are preserved in `retracted-2026-07-08/`: the 82.5%
(ghost-inflated) and a 76.5% (a de-ghost run poisoned by an OpenAlex rate-limit that my verifier
initially misread as absence — fixed; see the RETRACTION). The 80.6% is on the clean gold and is the
one to cite.

## What this establishes

1. **The search method (GACS) recovers the real primary-cell literature at ~81%** on a verified gold —
   above the pre-registered bar, though still short of Cochrane near-complete (the residual is the
   quirky-titled canon the snowball, not the keyword query, is meant to catch).
2. **The gold's ghost contamination is real, quantified (~40% of Tier B, ~60% of PRIMARY), and cleaned.**
   The durable method fix: an existence-verification gate on gold construction — no anchor in the recall
   denominator without a resolved live DOI (or corpus/Crossref confirmation). This carries to every chapter.

## What is NOT yet done — the screen

The corpus → tier counts → estimand-ready pooling set requires the LLM screen
(D1 → Haiku → Sonnet → estimand gate → tiers). **D1 is done** (`49`): the 11,463 corpus is ranked and
cut to a **1,100-paper LLM pool** (118 gold + top ~1,000 by term-richness; 995 with abstracts). The
Haiku/Sonnet screen over that pool is the remaining step; it is a multi-agent operation and has not
been run. Until it does, we have the recall number but not the final tier counts or the pooling-set
size, and the RA verdict gate remains pending.

## Bottom line

We have a **defensible end-to-end recall number (80.6%, gate passed) on a clean gold** — the metric the
adoption decision turns on — plus a quantified, corrected gold-integrity finding. The tier/pooling
output is one scoped screen away.
