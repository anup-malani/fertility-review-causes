# Status-fertility meta-analysis — prototype note (TICK-033/035)

**Status:** PROTOTYPE on partial data (20/95 PDFs retrieved; 10/52 status-and-reproduction). Numbers
below are illustrative of the machinery, not the chapter's finding. The pooled estimate for Section 6
lands only after the full-text extraction completes (missing DOIs in
`extraction/{slug}-missing-pdf-dois.txt`, retrieval via Zotero + UChicago).

## What this delivers

- **`source/analysis/b1_meta_pipeline.py`** — the reusable pooling pipeline. Harmonizes correlation-type
  effects to the Fisher-z metric, pools with DerSimonian-Laird random effects, back-transforms to r with
  a 95% CI, and reports subgroup pools by contraceptive availability and by sex. Honors the conservative
  rule: no pool is reported below 3 independent studies.
- **`source/analysis/test_b1_meta_pipeline.py`** — 10 unit tests, all passing. The random-effects fixtures
  use hand-computed inputs (e.g. z=[0.2,0.4], v=[0.01,0.01] -> Q=2.0, tau^2=0.01, pooled z=0.3, I^2=50%),
  so the math is checked against values worked by hand, not the code's own output.
- **`extraction/{slug}-effects.csv`** — the effect table (schema per `extraction/schema.md`). One row is
  fully extracted; the rest document what each retrieved PDF contains, with page locators, for the RA pass.

## The one fully-extracted effect (real)

von Rueden & Jaeggi 2016 (PNAS): male status -> reproductive success, **Zr = 0.19, 95% CI 0.09-0.31**,
k=288 associations across 46 studies in 33 nonindustrial societies. The authors restricted to
nonindustrial societies precisely to limit contraception, so this is a clean **contraception-absent**
anchor. It is itself a meta-analysis, coded `evidence_type=meta_analytic`.

## Directions extracted, effect sizes pending table extraction

- Zhang & Santtila (China CGSS, contraception **present**): status **positive** for men's number of
  children, **negative** for women's (Table 2, p7). The sex-specific reversal the hypothesis predicts.
- Hopcroft 2018 (US SIPP, present): income **positive** (u-shaped) for men's number of children (Table 5).

These carry `needs_pi=yes`; the exact coefficients sit in tables that need RA extraction (pypdf text does
not parse them reliably, and they are not guessed here).

## Run result (honest)

`poolable now: 1 | pending extraction: 4`. Every pool reports "insufficient (<3 studies); reported not
pooled." The pipeline is proven by the unit tests; the real run reflects the real partial data. When the
Zotero retrieval fills the status-and-reproduction stream and the RA extracts the table coefficients, the
same command produces the moderated pooled estimate for the chapter's Section 6.

## The test the pooled result will run

Prediction: pooled r positive where contraception is absent (von Rueden anchors this), attenuated or
reversed where present, more so for women than men (Zhang's negative female coefficient is the leading
edge). The moderator columns `contraceptive_availability` and `sex` in the effects CSV drive exactly that
subgroup contrast.
