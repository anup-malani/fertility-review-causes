# Part 3 — Term sourcing (split by leakage) · 2026-06-29

Implements method spec §5. Two **deliberately separate** artifacts (merging them would break the
leakage discipline that makes the CV recall estimate honest):

1. **External backbone (leakage-free, FIXED in every CV fold)** — terms from *published* prior-review
   search strings. Never touch held-out gold labels, so they do work for free in every fold.
2. **Gold-mined expansion (CV-disciplined, FOLD-LOCAL)** — discriminative terms harvested from
   gold-positive titles. The breadth knob N controls how much of this bolts onto the backbone; CV
   measures its *marginal* recall contribution (Part 4). The extractor is built and validated here;
   it is RUN fold-locally in Part 4 (here it is run on the full gold set only to expose the
   landscape + sanity-check the machinery).

## 3a — External backbone  (`*-external-backbone.json`)

- **Fertility block: 12 terms**, well-sourced, mostly verbatim from the Bergsvik/Fauske/Hart and
  Thomas et al. fertility-review strings (`fertilit*`, `birth-rate*`, `total/cohort/completed/
  lifetime fertility`, `parity progression`, `childbear*`, `number of children`).
- **Pension / old-age-security block: 31 terms** — the **thin block** (no dedicated OAS–fertility
  review exists). Anchored on a **verbatim** social-protection review string (Perera et al. 2022,
  Campbell) — `pension*`, `social pension*`, `old age pension`, `old age security`, `social
  security`, `social insurance`, `provident fund`, `superannuation`, `annuities`,
  `(non-)contributory`, `cash transfer*`, … — plus a retirement-health review (Tomaz 2024) and
  OAS-motive author-keywords/JEL H55 controlled vocabulary.
- **5 sources**, each with DOI + the exact appendix/section. Process note: Bergsvik's full string
  isn't in the article — it lives in the companion protocol (SocArXiv `t8vsg`), retrieved via OSF.
- **Caveat:** the social-protection origin makes the pension block *broad* (it includes `health
  insurance`, `cash transfer`, `social safety net`) — high recall but some off-topic pull under the
  2-block AND. The breadth-vector CV (Part 4) decides which to keep.

## 3b — Discriminative extraction  (`21_discriminative_terms.py`, `*-discriminative-terms.{json,md}`)

- **Method:** Monroe et al. "Fightin' Words" — weighted log-odds-ratio with an informative
  Dirichlet prior, z-scored (variance-stabilized so rare terms don't dominate). NOT raw tf-idf.
- **Contrast:** gold-positive titles (303 = Tier A 56 + Tier B core 247) vs the **4,537 on-disk
  NOT_RELEVANT** titles. Titles only (negatives have no on-disk abstracts → same footing).
- **Result:** 193 ranked candidate terms (30 fertility / 35 pension-OAS / 9 both / 119 context).
  Top by z: `fertility` 18.3, `security` 15.1, `endogenous` 15.1, `old age` 12.2, `age security`
  11.3, `social security` 11.2, `endogenous fertility` 11.2, `pensions` 10.2, `intergenerational`
  7.4, `payg` 6.3, `security fertility` 5.9 (19 gold / 1 neg).
- **Caveat (spec §5):** the negatives already passed the PI keyword filter, so the contrast is
  relevant-vs-NEAR-MISS (precision-at-fixed-recall discrimination), not relevant-vs-random-DB.

## Backbone × expansion — what gold-mining adds

Of the 22 high-z (z≥4) fertility/pension/both terms, ~10 are already covered by backbone
wildcards; the genuine **gaps the gold-mined expansion contributes** are the OAS *theory*
vocabulary the policy-review backbone lacks: **`intergenerational` / `intergenerational
transfers` / `transfers`, `payg` (pay-as-you-go), `value of children`, broader `child*`**. This is
the buyable marginal recall the breadth knob exists to purchase — and it is exactly what Part-4 CV
will quantify.

## Handoff to Part 4

- 2-block Boolean: `(fertility block) AND (pension/old-age-security block)` (spec §4).
- Backbone fixed every fold; expansion = top-N discriminative terms mined from the **training
  fold's** gold only, at per-block breadth (N_fertility, N_pension).
- 10-fold CV over the breadth-vector grid, universe ≤ screening budget K; per-block miss
  diagnostics; refit on full gold at the chosen breadth → production query.
