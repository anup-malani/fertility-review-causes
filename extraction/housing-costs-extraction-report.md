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

---

# Extraction pass 2 — effect sizes

**Run:** 2026-07-31 · **Output:** `extraction/housing-costs-effects.csv` (13 effect rows, 10 studies)

Every figure was read from **the paper's own text**, never from another paper's citation of it. That
discipline immediately caught a live error: the 2021 HPR proceedings paper cites Dettling & Kearney as
**"6 percent"**, where D&K's own text says **5 percent**. Extracting from literature reviews would have
propagated it into our pooled estimate.

## 1. The substantive result: the tenure-conditional sign prediction holds

The scope doc's central claim — that a house-price rise is a *cost* to renters and prospective buyers
and a *wealth gain* to owners, so the two channels carry opposite signs — is borne out across
independent settings and designs:

| Channel | Study | Estimate |
|---|---|---|
| **Wealth (owners)** | Dettling & Kearney (US, IV) | **+5.0%** per +$10,000 |
| | Daysal et al. (Denmark) | +1.28–2.11% per +$12,000 *(blocked, preprint)* |
| | Ang et al. (China, RD) | **+0.18%** per +1% housing wealth |
| | PNAS 2026 (China, DiD) | **+2.73 pp** (+20.8% over baseline) |
| **Cost (non-owners / prospective buyers)** | Dettling & Kearney (US, IV) | **−2.4%** per +$10,000 |
| | Liu & Zhang (China, HPR) | **−0.88 births/1,000** per +10% |

**Four independent wealth-channel estimates are positive; both cost-channel estimates are negative.**
Two of the four come from designs (RD, cohort DiD) that did not exist when the pooling rule was
written. This is the strongest support the chapter has for the rule, and it should be reported as a
finding rather than assumed.

**The aggregate sign then behaves as the composition account predicts.** Net effects are positive in
the US (+0.8% at mean ownership) and Canada (+2.0% to +11.8% odds), and negative in China
(−0.94 pp per 1%) and the global panel (−0.030 births/woman per +10%).

**The apparent China anomaly resolves into the scope's own third category.** Urban Chinese
homeownership is nominally very high, so a naive owner-vs-renter reading predicts a positive net
effect; the estimates are firmly negative. The resolution is that the binding group is neither owners
nor renters but **prospective buyers** — young couples who must purchase to marry. For them a price
rise is pure cost regardless of the aggregate ownership rate. The scope listed prospective buyers with
renters on the cost side; China is the setting where that grouping earns its keep, and the chapter
should say so explicitly rather than reporting an unexplained sign flip.

## 2. Only four effects are poolable

| Poolable | n |
|---|---|
| **yes** | **4** |
| no — not tenure-split | 3 |
| no — composition-weighted net | 1 |
| no — quantile-varying | 1 |
| blocked (preprint twin) | 1 |
| blocked (quality) | 1 |
| blocked (unreadable scan) | 1 |

**From a 241-record frame: four poolable effect estimates**, two per channel — and the two within each
channel are in incompatible units ($10,000 levels vs percentage elasticities vs births per 1,000).
Harmonisation to a common elasticity is required before anything is pooled, and with n=2 per channel a
formal meta-analysis is not obviously the right instrument. **A structured evidence table with the
signs, magnitudes and settings laid out may be more honest than a forest plot with two points on it.**
That is a recommendation for the synthesis stage, not a decision taken here.

## 3. One recommended demotion

**`Housing Purchase Restriction and Birth Rates` (2021) should leave the identified core.** It is a
conference-proceedings paper (Atlantis Press, not peer-reviewed); its reported effect is "birth rates
dropped roughly 5.45 unit" with the unit never defined; the authors describe their own coefficients as
"unlikely and ambiguous" and close by asking readers to "replicate our results… to draw a more
accurate and unbiased result". It also carries the misquoted D&K figure. **Recommend regrading it out
of QUASI_EXP**, which would take the identified core from 9 to 8.

## 4. Open items

- **Daysal et al.** — reconcile the preprint against the published *JPubE* version before its estimate
  is usable.
- **PNAS 2026** — treatment is a credit-easing reform; the price-vs-credit boundary call (C.2.c vs
  C.3.e) is still open and it is one of the four wealth-channel estimates, so the call matters.
- **The Korean rent study** — still unreadable; it is the only policy-assigned-rent design.
- **Harmonisation** — convert all estimates to a common elasticity before any pooling.
