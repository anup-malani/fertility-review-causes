# Extraction pass 1 — design confirmation (C.2.c)

**Run:** 2026-07-31, Shravan (TICK-055)
**Input:** the 15 identified PDFs · **Output:** `extraction/housing-costs-study-extraction.csv`
**Scope:** design, treatment type, tenure split, outcome level, period. **Effect sizes are not in this
pass** — design and routing had to settle first, because two records leave the primary pool and one
grade decides the FDT cell.

---

## 1. The headline: the identified core is 9, not 15

The `id_strength` labels were assigned from titles and abstracts and flagged as provisional. Reading
the full texts moves six of them.

| Confirmed grade | n |
|---|---|
| **QUASI_EXP** | **9** |
| WEAK_QUASI | 2 |
| ASSOCIATIONAL | 2 |
| ROUTED_OUT (no fertility outcome) | 1 |
| UNREADABLE (image-only scan) | 1 |

A `WEAK_QUASI` grade was added rather than forcing borderline designs into either neighbour: a
propensity-score match is selection on observables, and a before/after structural break has no control
group. Both are attempts at exogenous variation that do not isolate it, and folding them either way
would misstate the evidence base.

**The confirmed nine:** Dettling & Kearney (IV, supply elasticity); Daysal et al. (first-home price as
instrument, Danish registers); Clark, Yi & Zhang (IV, China); Li 2024 (IV: construction costs and land
prices, global 1870–2012); Ang et al. (RD + placebo); the PNAS 2026 HPF-reform cohort DiD; Liu & Zhang
(house purchase restrictions); Clark & Ferrer (IV, Canada); and the 2021 HPR difference-in-differences.

## 2. Three corrections that change the chapter

**(a) `Homes and husbands for all` has no fertility outcome — it leaves the primary pool.**
Every estimating table in the paper has **marriage** as the dependent variable: *Effect of Building
Permits on Marriage*, *…on Marriage Licenses*, *…on Probability of Marriage*. The widely-quotable
sentence — that housing supply growth "can account for 10 percent of the rise in birth rates between
1930 and 1950 through the channel of increased marriage rates" — is the author's **decomposition**
applied to a marriage estimate, not an estimated fertility effect. Under the scope's own rules it is
`HOUSING_ONLY_MECHANISM`, cross-referenced to A.7.

The decomposition is still worth having, as an attributed input to §7 demographic significance. It is
not a study in the pooled set.

**(b) So the FDT cell now rests on Li 2024 alone.** The gold-freeze proposal called Li's grade "the
single most consequential unconfirmed judgement in the chapter" and set out two ways it could fall.
Neither happened — but the other FDT study did. Li **survives** confirmation: house prices are
instrumented with construction costs and land prices in a dynamic panel, which is a genuine
identification strategy. The result is the mirror image of what was flagged: the contested study held
and the clear one fell.

**One study is now the entire identified FDT evidence base.** A GRADE above *very low* is not
defensible on n=1, and the chapter must say so.

**(c) Yi & Zhang (2010) is a time-series association, not a quasi-experiment.** The paper contains no
instrument anywhere; identification is a cointegration / error-correction model on aggregate annual
Hong Kong series. It was the oldest study in the identified set and its demotion removes the only
pre-2013 SDT identification. Wijk (2024, Dutch) is demoted on the same basis — area and individual
fixed effects, no instrument and no policy shock.

## 3. What the confirmed nine look like as an evidence base

- **Tenure split present in only three** — Dettling & Kearney, Clark & Ferrer, and (with tenure
  categories rather than a split) Lin et al. The pooling rule's primary targets are the two
  tenure-specific channels, so **the rule can currently be executed on three studies, one of which is
  `WEAK_QUASI`.**
- **Treatment is `price` in seven of nine.** One is housing wealth (the RD), one an
  ownership-stimulating policy.
- **Geographic concentration is severe:** four of nine are China. With the US (2), Canada, Denmark and
  the global panel, that is the whole set.
- **The PNAS 2026 study sits on the C.3.e boundary** — its treatment is a housing-provident-fund
  *credit-easing* reform. Under the price-variation ruling, credit terms route to C.3.e. Whether it
  belongs here at all is an extraction-time call, flagged in the table rather than settled silently.

## 4. Two blockers carried forward

1. **The Korean public-rental-housing paper cannot be graded** — 21-page image-only scan, no text
   layer, Korean language. It is the only policy-assigned-rent design in the pool, so it cannot be
   dropped for convenience. Needs OCR + translation.
2. **Daysal et al. is still the preprint twin.** No number may be extracted until reconciled against
   the published *JPubE* version.

## 5. Next

Effect-size extraction on the confirmed nine, with the scope's required per-effect fields (sign
oriented per the pooling rule, baseline ownership rate, parity, tempo-vs-quantum). Expect the poolable
set to be smaller still: the pooling rule bars combining the two tenure channels, bars combining price
with rent or affordability, and bars combining outcome levels.
