# Chapter C.2.c: Housing Costs and Space Constraints

**Category:** Economic (Cost of Children)
**Primary mechanism:** Housing is a lumpy, priced input to child-rearing, so a rise in its price raises the implicit cost of an additional child — but the same rise is a capital gain to those who already own, and the two effects carry opposite signs.
**Cross-references:** C.3.e (Credit Constraints) · A.23 (Co-Residence) · C.2.b (Direct Costs of Children) · C.2.g (Urbanization) · C.1.a (Income Effect) · A.7 (Marriage Timing) · A.11 (Tempo)
**Status:** RA draft, 2026-07-31 (TICK-055). Not yet PI-reviewed.

---

## 1. The claim

Higher house prices and rents raise the price of the space input to child-rearing and thereby reduce fertility. The claim as stated in HYPOTHESES-v5 is about a *net* effect, and that is the first thing this chapter has to take apart: a price rise is a **cost** to renters and to prospective buyers, and a **wealth gain** to existing owners. The two groups respond in opposite directions, so any population-level elasticity is a tenure-composition-weighted average whose weight is the local homeownership rate — not a behavioural parameter, and not transportable between settings.

The chapter therefore estimates two quantities rather than one: the **cost-channel elasticity** among those who must pay the higher price, and the **wealth-channel elasticity** among those who already own.

## 2. Theoretical mechanism

Children require space, and space is bought in large, indivisible units. In the standard cost-of-children framing, a rise in the price of housing raises the shadow price of an additional child and reduces demand for children, with the strength of the effect governed by the substitutability of housing for other inputs to child quality.

That account is incomplete in a way that matters empirically. Housing is not only an input; it is the principal asset most households hold. For an owner, a price rise is an increase in net worth and, through home equity, in borrowing capacity. If children are a normal good — the C.1.a baseline — the wealth effect pushes fertility up. The observable net effect is therefore the sum of a negative price effect on non-owners and a positive wealth effect on owners, and its sign depends on who is in the population.

A third group is neither, and turns out to be decisive in the settings with the sharpest price growth: **prospective buyers**, who do not yet own but must purchase in order to form the household in which children are raised. For them a price rise is pure cost, unrelieved by any offsetting gain, regardless of how high the aggregate ownership rate is.

## 3. Search strategy

Gold-anchored clustered search (`canonical-search-workflow.md`), documented in full at `literature/search-logs/housing-costs-*`.

**Boundary rule (Shravan, 2026-07-31).** Three neighbouring hypotheses overlap this one, and they are separated by *what varies*, not by the mechanism an author narrates: **C.2.c owns variation in housing prices; C.3.e owns variation in liquidity and credit; A.23 owns variation in co-residence, whatever drives it.** This rule did real work — it resolved a paper listed as *seminal for both* C.2.c and C.3.e in the master list, and it later routed a strong PNAS study out of this chapter (§5).

**Period.** HYPOTHESES-v5 scopes C.2.c to the SDT. FDT-era evidence is admitted (Shravan, 2026-07-31) and the `phenomena` field should be formally updated by the PI; the search found a housing-and-fertility literature reaching back to the 1930s.

**Two vocabulary families, deliberately searched separately.** Economics says *house prices, housing wealth, home equity, real estate*; demography and housing studies say *homeownership, housing tenure, housing type, housing career*. They surface different papers, not the same papers renamed.

## 4. PRISMA flow

| Stage | n |
|---|---|
| Cold-start anchors (existence-verified) | 25 |
| Citation snowball, 5 rounds (3 targeted + 2 mechanical confirming) | 10,915 records |
| Housing-treatment **and** fertility-outcome core | 256 |
| After normalized-title dedup | **241** |
| RA gate: provisionally primary | 108 |
| RA gate: survived as primary | 78 |
| Identification confirmed at full text | **8** (from 15 assessed) |
| Contributing effect estimates | **5** |

Two features of this funnel are worth stating rather than hiding.

**Channel 1 of the cold-start bootstrap is empty.** No systematic review or meta-analysis of housing → fertility exists. Four probe forms were run; the only adjacent review is of housing prices and *health*, and its sole contact with this literature is one paper included for birth-weight outcomes. A large literature has never been formally synthesised.

**The relevance filter was wrong three times**, each caught by reading a random sample of what it admitted and never by the counts. Bare substrings matched **hous**ehold, **hous**ework, Hou**ston**, pa**rent**, cur**rent**, diffe**rent**, psychometric **propert**ies, medical **residen**ts, and **home**land — 351 false positives in total. Every error over-admitted, which held the snowball's saturation statistic above its stopping floor and briefly produced a false conclusion that the stop rule itself was broken. A relevance filter that over-admits does not look like an error; it looks like more work to do.

## 5. Included studies

Eight studies have identification that survives reading the full text. Seven contribute an effect; one is recommended for exclusion.

| Study | Setting | Design | Channel | Elasticity | RoB |
|---|---|---|---|---|---|
| Ang et al. 2024 | China | Regression discontinuity + placebo | wealth | **+0.18** | **LOW** |
| Dettling & Kearney 2014 | US MSAs | IV: supply elasticity | wealth / cost | **+0.81 / −0.39** | MODERATE |
| Daysal, Lovenheim, Siersbæk & Wasser 2021 | Denmark | IV: first-home price + registers | wealth | **+0.23** | MODERATE |
| Liu & Zhang 2024 | China | DiD: purchase restrictions | cost (prospective buyers) | **−0.82** | MODERATE |
| Clark, Yi & Zhang 2020 | China | IV + city FE | aggregate | −0.94 pp per 1% | SERIOUS |
| Clark & Ferrer 2019 | Canada | IV: initial-area prices | aggregate | +2.0% to +11.8% odds | SERIOUS |
| Li 2024 | Global, 1870–2012 | IV: construction costs, land prices | aggregate | −0.030 births/woman per +10% | SERIOUS |
| *Housing Purchase Restriction 2021* | China | DiD | aggregate | *units undefined* | **CRITICAL — exclude** |

Elasticities are % change in fertility per 1% change in the price or wealth measure, computed at each study's own sample mean, with every baseline read from that study's own descriptive-statistics table (`housing-costs-effects-harmonised.csv`).

**Risk of bias concentrates where the scope predicted it would: the exclusion restriction.** Three of the six studies with an instrument are rated serious or critical on that domain alone. The first stages are strong; the problem is that supply elasticity, construction costs, land prices and initial-area prices all plausibly affect fertility through channels other than house prices. In the Canadian study the IV estimate is roughly six times the OLS estimate, a gap large enough to suggest a weak or invalid instrument rather than the removal of attenuation bias.

**One study was routed out of the chapter on the boundary rule.** A 2026 *PNAS* cohort-DiD study of a Chinese housing-provident-fund reform is a strong design with a clear positive fertility effect — but the reform "expanded access by lowering down payment ratios, reducing interest rates, and raising loan ceilings." Credit terms vary; house prices do not. It belongs to C.3.e and has been flagged to that chapter.

**One study was routed out because it does not measure fertility.** *Homes and husbands for all* estimates the effect of post-war US building permits on **marriage** — every estimating table has marriage as the dependent variable. Its widely quotable claim that housing supply "can account for 10 percent of the rise in birth rates" is the author's decomposition applied to a marriage estimate, not an estimated fertility effect. It is retained as mechanism evidence and cross-referenced to A.7.

## 6. Quantitative synthesis

**No forest plot is presented, and that is a deliberate choice.** The pooling rule bars combining the two tenure channels, bars combining price with rent or affordability measures, and bars combining outcome levels. What survives is three wealth-channel elasticities and two cost-channel elasticities. A pooled point estimate resting on two or three studies would convey a precision the evidence does not have; the structured table above carries more information.

**The central finding is that the sign prediction holds.** Three independent wealth-channel estimates are positive (+0.81, +0.23, +0.18) and two independent cost-channel estimates are negative (−0.39, −0.82). They come from four countries and four designs — IV on supply elasticity, IV on first-home prices with population registers, regression discontinuity, and policy difference-in-differences — and two of those designs postdate the framing of the hypothesis. This is the chapter's most secure result.

**The aggregate sign then behaves as composition predicts.** Net effects are positive in the US and Canada and negative in China and the global panel.

**The Chinese case initially looks like a counterexample and is not.** Urban Chinese homeownership is nominally very high, so an owner-versus-renter reading predicts a positive net effect, and the estimates are firmly negative. The binding group there is prospective buyers: young couples who must purchase in order to marry, for whom a price rise is pure cost whatever the aggregate ownership rate.

**Two cautions on magnitude.** Dettling & Kearney is the outlier on both sides — its owner elasticity is three to four times the Danish and Chinese estimates — and it is also the most-cited study in this literature, so a reader anchored on the US result will overestimate the wealth channel. And every conversion from a per-dollar effect to an elasticity assumes local linearity; Dettling & Kearney state that assumption explicitly, and it is imposed rather than tested.

## 7. Demographic significance

The protocol asks for a decomposition share, a slope-sufficiency judgement, and R² benchmarks. **The decomposition share and R² benchmarks cannot be computed: `data/raw/` is empty and the review has no macro panel yet.** That is a repository-level gap affecting every chapter, not a C.2.c finding. What follows is a scale check with stated inputs, in the manner of the old-age-security chapter.

### 7.1 Pre-modern
No evidence. The pre-modern analogue of this mechanism — household formation requiring a niche, a holding, a dwelling — is real, but it currently lives inside A.7 and the European Marriage Pattern. **Not assessable.**

### 7.2 FDT
One identified estimate, and it is the weakest-identified in the pool. Li (2024) finds −0.030 births per woman per 10% real house price rise. Real house prices roughly tripled across the long run in the countries covered; applied linearly that implies on the order of −0.6 births against an observed decline of two to three births, or roughly a fifth of the transition.

**The arithmetic clears the protocol's 10% threshold; the evidence does not support leaning on it.** The estimate rests on a single study whose instruments — construction costs and land prices — are its critical weakness, land prices being close to the same object as house prices rather than an external shifter. **Verdict: not established.** The honest statement is that the long-run relationship is documented and not identified.

### 7.3 SDT
Two anchors point in different directions, and the difference is informative.

**Where prices grew fastest, the effect is demographically significant.** Liu & Zhang estimate that China's purchase-restriction-era price growth produced roughly 2.46 million fewer births, about **10.4% of the aggregate birth reduction** in the post-treatment period — at the protocol's threshold, from the study's own decomposition.

**For the broader Western SDT decline it is insufficient.** Dettling & Kearney's own calculation implies the 1997–2006 US boom raised births by about 9%; US TFR over that window rose about 4%. But the sustained post-2007 US fertility decline of roughly 19% coincides with real house prices that fell and then recovered, netting to little over the period. A mechanism whose net effect is near zero cannot account for a fifth of the fertility level.

**Verdict: demographically significant in high-price-growth Asian settings; insufficient as an explanation of the Western SDT decline.**

## 8. GRADE rating

| Phenomenon | Rating | Justification |
|---|---|---|
| Pre-modern | **No evidence** | No studies. Mechanism lives in A.7. |
| FDT | **Very low** | One estimate, exclusion restriction rated critical, 1870–2012 price series with severe measurement heterogeneity. |
| SDT | **Low** | Consistent signs across four countries and four designs, one study at low risk of bias — but only five contributing estimates, exclusion restrictions serious in three of six instrumented studies, tenure splits available in only three studies, and severe geographic concentration. |

The SDT rating is *low* rather than *very low* because of the sign consistency across independent designs, and does not reach *moderate* because the quantity the chapter most wants — a transportable elasticity by tenure — rests on three studies whose estimates span a factor of four.

## 9. Verdict

| Phenomenon | Causal credibility | Demographically significant? |
|---|---|---|
| Pre-modern | No evidence | Not assessable |
| FDT | Very low | Not established |
| SDT | Low | **Yes** in high-price-growth Asian settings; **no** for the Western SDT decline |

## 10. Open questions and recommended studies

1. **A rent-identified estimate with credible exogeneity.** The scope identified rent as the cleanest test — no wealth offset, no endogenous tenure split — and after full screening **the rent stratum contains no quasi-experimental study at all**. A rent shock with a defensible design would be the single most valuable addition to this literature.
2. **Tenure splits.** Only three of eight studies report one, and the pooling rule's primary targets depend on it. Reporting effects separately for owners, renters and prospective buyers should be a default, not a robustness check.
3. **Better instruments.** The binding constraint is the exclusion restriction, not the first stage. Land prices instrumenting house prices is close to circular.
4. **Prospective buyers as a distinct group.** The Chinese evidence suggests this is where the cost channel actually binds. No study identifies it directly.
5. **Tempo versus quantum.** Almost nothing in the pool addresses whether housing costs postpone births or reduce completed fertility. If the effect is mostly postponement, the demographic significance verdict shrinks sharply. Cross-reference A.11.
6. **Whether most of this literature belongs to another hypothesis.** The large demography literature on housing and fertility studies tenure, housing type, and residential mobility rather than prices. Under the boundary rule it routes to A.23 or to mechanism and context. That is a finding about the field: **the housing-and-fertility literature is mostly not about the price of housing.**

## 11. References

Effect estimates and full bibliographic detail: `extraction/housing-costs-effects.csv`, `extraction/housing-costs-effects-harmonised.csv`, `extraction/housing-costs-study-extraction.csv`, `extraction/housing-costs-risk-of-bias.csv`. Search and screening record: `literature/search-logs/housing-costs-*`.

---

### Provenance and standing caveats

- **Scope and rulings:** `literature/search-logs/housing-costs-search-scope.md`
- **Evidence-base posture (Shravan, 2026-07-31):** a thin price-variation evidence base is an acceptable outcome; the obligation is to *report* the shrinkage, not to engineer around it. This chapter's §4 and §10.6 discharge that.
- **Retrieval:** 30 of 78 gated studies retrieved; **the identified core is complete at 15/15**, so the central estimates are not retrieval-bound. The 48 outstanding are the associational stratum.
- **Not independently verified:** all screening, gating, extraction and risk-of-bias ratings in this chapter are single-reader. `ra_verified = no` throughout.
- **Preprint reliance:** Daysal et al. was read in its NBER working-paper version; the headline estimate was reconciled against the published *Journal of Public Economics* abstract and matches. Subsidiary specifications were not reconciled. Liu & Zhang exists only as an SSRN preprint.
