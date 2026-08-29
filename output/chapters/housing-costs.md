# Housing Costs and Space Constraints

**Category:** Economic (cost of children)
**Primary mechanism:** Housing is a lumpy, priced input to child-rearing, so a rise in its price raises the implicit cost of an additional child — but the same rise is a capital gain to those who already own, and the two effects carry opposite signs.
**Cross-references:** C.3.e credit constraints (owns variation in liquidity and credit terms) · A.23 co-residence (owns variation in co-residence, whatever drives it) · C.2.b direct costs of children · C.2.g urbanization · C.1.a income effect · A.7 marriage timing · A.11 tempo.
**Status:** TICK-055. Rewritten against `docs/chapter-template.md` on 2026-08-29; previous draft 2026-07-31. Not PI-reviewed. All screening, gating, extraction and risk-of-bias ratings are single-reader (`ra_verified = no` throughout). Written on 30 of 78 wanted full texts (38%), but the identified core is complete at 15 of 15.

---

## 1. The claim

This chapter explores the effect of housing prices on fertility.

### 1.1 In plain terms

In plain terms: children need somewhere to live, and space costs money. The claim is that when houses and flats get more expensive, people have fewer children, because the room a child would need has become something they cannot afford.

The complication is that a rise in house prices is not bad news for everybody. If you already own your home, it has just become more valuable — you are richer, and richer people tend to have more children, not fewer. If you are renting, or still saving to buy, the same rise is pure bad news. So the same event pushes two groups in opposite directions, and what happens to a whole country depends on how many people are in each group.

That means there is no single answer to "does expensive housing reduce births". There is one answer for people who must pay the higher price and a different one, with the opposite sign, for people who already own. This chapter estimates both, and then shows that adding them up is harder than it looks, because a third group — people who own nothing yet but must buy before they can start a family — gets counted on the wrong side.

### 1.2 The claim precisely

The parameter this chapter estimates is twofold: the **cost-channel elasticity**, the percentage change in fertility per one percent rise in the price of housing among those who must pay it, and the **wealth-channel elasticity**, the same quantity among those who already own. Both are measured as percent per percent, signed so that a negative value means fewer births.

The chapter rates the claim against **PM** (pre-modern fertility variation, before roughly 1870), **FDT** (the First Demographic Transition, roughly 1870–1965) and **SDT** (the Second Demographic Transition, roughly 1965 onward). `HYPOTHESES-v5` scopes this hypothesis to the SDT; FDT-era evidence was admitted by RA ruling on 2026-07-31 and the `phenomena` field still needs a formal PI update.

**This mechanism has an identity arm and a behavioural arm, and separating them is the whole chapter.**

- **The identity arm needs no study and cannot be false.** The population elasticity is a weighted average of the channel elasticities, with the weights being population shares: η_pop = w·η_wealth + (1−w)·η_cost. This is arithmetic. It follows that **the aggregate elasticity is not a behavioural parameter at all** — it is a composition statistic, and it changes when the ownership rate changes even if no household's behaviour changes at all. Reporting it as though it were transportable is the characteristic error in this literature.
- **The behavioural arm is where the hypothesis can be wrong:** the two channel elasticities themselves.

§7.3 shows what happens when the identity is taken seriously: it does not merely fail to pin the aggregate down, it makes a sign prediction that the evidence contradicts — which locates the error precisely.

**The counterfactual** is a ceteris-paribus perturbation: hold income, credit terms, local labour demand and household composition fixed, and raise the price of housing. Credit terms are the hard one, because the policies that move house prices usually move borrowing conditions too; that is the boundary with C.3.e.

**Margin.** The mechanism is predicted to move both margins — whether to have a child at all, and how many — but the evidence measures birth rates and birth probabilities, not completed fertility, so §8 cannot distinguish postponement from reduction. Open question 5.

---

## 2. Theoretical mechanism

In the reader's own vocabulary: housing is an input to child-rearing bought in large indivisible units, so a price rise raises the shadow price of an additional child, with the strength of the response governed by how substitutable space is for other inputs to child quality. That is a standard cost-of-children argument and it predicts a negative elasticity.

It is incomplete in a way that matters empirically. Housing is not only an input; it is the principal asset most households hold. For an owner, a price rise raises net worth and, through home equity, borrowing capacity. If children are a normal good — the C.1.a baseline — the wealth effect pushes fertility up. The net observable effect is the sum of a negative price effect on non-owners and a positive wealth effect on owners.

A third group is neither, and turns out to be decisive wherever prices grow fastest: **prospective buyers**, who do not yet own but must purchase in order to form the household in which children are raised. For them a price rise is pure cost, unrelieved by any offsetting gain, *regardless of how high the aggregate ownership rate is*. This group is the chapter's central analytical object and, as §7.3 shows, conventional homeownership statistics hide it by counting its members as owners.

**What would make the hypothesis wrong.** The cost channel is wrong if renters and prospective buyers facing exogenous price rises do not reduce fertility. The wealth channel is wrong if owners facing the same rise do not increase it. Both have been tested; §6 reports that both survive. What has *not* been established is any transportable aggregate.

---

## 3. Search strategy

Gold-anchored clustered search (`canonical-search-workflow.md`), documented at `literature/search-logs/housing-costs-*`.

| Wall | Rule | Enforceable at title/abstract? |
|---|---|---|
| **W1 Treatment** | The variation must be in **housing prices or rents**. Variation in liquidity, down-payment ratios, interest rates or loan ceilings is C.3.e's. Variation in co-residence is A.23's. | Partially — an abstract often narrates a mechanism the paper does not identify |
| **W2 Outcome** | The outcome must be a birth or a fertility rate, not marriage, household formation or tenure. | Yes |
| **W3 Tenure split** | Whether a study identifies the cost channel, the wealth channel, or only their composite. | **No — declared unenforceable in advance.** Visible only in the specification, and §6.1 shows only three of eight studies report it. |

**The boundary rule that did the work (Shravan, 2026-07-31):** neighbouring hypotheses are separated by *what varies*, not by the mechanism an author narrates. **C.2.c owns variation in housing prices; C.3.e owns variation in liquidity and credit; A.23 owns variation in co-residence.** This resolved a paper listed as seminal for both C.2.c and C.3.e in the master list, and later routed a strong 2026 *PNAS* study out of this chapter (§6).

**Two vocabulary families were searched separately, deliberately.** Economics says *house prices, housing wealth, home equity, real estate*; demography and housing studies say *homeownership, housing tenure, housing type, housing career*. They surface different papers, not the same papers renamed.

---

## 4. PRISMA flow

| Stage | Records |
|---|---:|
| Cold-start anchors (existence-verified) | 25 |
| Citation snowball, 5 rounds (3 targeted + 2 mechanical confirming) | 10,915 |
| Housing-treatment **and** fertility-outcome core | 256 |
| After normalized-title dedup | 241 |
| RA gate: provisionally primary | 108 |
| RA gate: survived as primary | 78 |
| Full texts retrieved | 30 |
| Identification confirmed at full text | **8** (of 15 assessed) |
| Contributing effect estimates | **5** |

Three features of this funnel change how the chapter should be read.

**First, no systematic review of housing and fertility exists.** Channel 1 of the cold-start bootstrap came back empty across four probe forms; the only adjacent review is of housing prices and *health*, touching this literature through one paper included for birth-weight outcomes. A large literature has never been formally synthesised, which removes the external-authority anchor source this review normally leans on.

**Second, the relevance filter was wrong three times, and the counts never showed it.** Bare substrings matched **hous**ehold, **hous**ework, Hou**ston**, pa**rent**, cur**rent**, diffe**rent**, psychometric **propert**ies, medical **residen**ts and **home**land — 351 false positives. Every error over-admitted, which held the snowball's saturation statistic above its stopping floor and briefly produced a false conclusion that the stop rule was broken. Each was caught by reading a random sample of what the filter admitted, never by the counts. **A filter that over-admits does not look like an error; it looks like more work to do.**

**Third, retrieval is 30 of 78 but the identified core is complete at 15 of 15.** The 48 outstanding studies are the associational stratum. The central estimates are therefore not retrieval-bound, which is unusual in this review and worth stating positively.

---

## 5. The ideal design

Written before the literature was read, so that §6 can be compared against a fixed yardstick rather than against the best paper that happens to exist.

### 5.1 The ideal estimand

The percentage change in **completed fertility** caused by a one percent exogenous rise in the local price of housing, **estimated separately for three groups**: existing owners, renters with no purchase intention, and prospective buyers. Reported for women aged 20–40 at exposure and followed to age 45.

Two features of this specification are doing work. The **three-way** split is not a refinement of the usual owner/renter split; §7.3 shows the two-way split makes a false sign prediction, so the third group is required for the identity to hold. And **completed fertility** rather than a birth rate is required because a price shock that postpones births looks identical to one that prevents them in any short window — the distinction that decided the tempo chapter.

### 5.2 The design that would identify it

**Source of variation.** An exogenous shift in local housing prices that does not simultaneously move credit terms, local labour demand or household composition. The cleanest candidate is a **rent shock** — a rent-control change, a large exogenous supply addition, or a shift-share exposure to national price movements interacted with pre-determined local supply constraints — because rent carries no wealth offset and no endogenous tenure split.

**Comparison group.** Households in otherwise similar local markets not exposed to the shift, with tenure status measured **before** the shock so that the price change cannot itself reassign people between groups.

**Identifying assumption.** The shift is uncorrelated with local fertility determinants conditional on controls. Falsifiable: pre-trends in fertility by exposure; placebo outcomes such as fertility among households who neither rent nor intend to buy; and an explicit test that credit terms did not move with prices.

**Estimating equation.** A difference-in-differences or shift-share IV on log fertility, fully interacted with baseline tenure status, so the three channel elasticities come from one specification and one sample rather than from three literatures.

**Data required.** Household panel with pre-shock tenure and purchase intentions, linked to birth records, with a horizon long enough to reach completed fertility — 20 years or more.

**Sample size.** Elasticities in this literature run 0.18 to 0.82; detecting the small end within a tenure cell needs a panel in the tens of thousands, which is why the credible studies here use administrative registers.

**What the ideal design deliberately excludes.** Instrumenting house prices with **land prices** is not the ideal design: land price is close to the same object as house price rather than an external shifter, and §6.1 rates that exclusion restriction critical.

### 5.3 Distance from the ideal

| Study | Exposure: price, not credit? | Tenure split? | Outcome: completed fertility? | Assignment | Distance |
|---|---|---|---|---|---|
| **Dettling and Kearney 2014** | Yes | **Yes — both channels** | No — birth rates | IV on supply elasticity; exclusion restriction contested | **Closest** |
| Daysal et al. 2021 | Yes | Wealth only | No — register births | IV on first-home price + registers | Close |
| Ang et al. 2024 | Yes | Wealth only | No | **RD with placebo — the strongest design here** | Close |
| Liu and Zhang 2024 | Yes | **Cost, prospective buyers** | No — birth rate | DiD on purchase restrictions | Close on the decisive group |
| Clark, Yi and Zhang 2020 | Yes | No — aggregate | No | IV + city FE; exclusion restriction serious | Far |
| Clark and Ferrer 2019 | Yes | No — aggregate | No | IV on initial-area prices; IV ≈ 6× OLS | Far |
| Li 2024 | Yes | No — aggregate | No | IV on construction costs and **land prices** | Far — the excluded instrument |
| *Housing Purchase Restriction 2021* | Yes | No | No | DiD, units undefined | **Excluded — critical** |

**No study implements the ideal design, and the two gaps are systematic rather than incidental.**

**Not one of the eight measures completed fertility.** Every estimate is a birth rate or a birth probability in a short window, so the entire chapter is silent on whether housing costs postpone births or prevent them. That is not a limitation of any one study; it is a property of the whole literature, and it caps how much §8 can claim.

**Only three of eight report a tenure split**, and no single study reports all three groups. The three-way split the identity requires is assembled across four countries and four designs, which is why §6.2's sign result is secure and §6.3's magnitude is not.

**And the rent stratum — the cleanest available test — contains no quasi-experimental study at all.** After full screening, the design §5.2 names as ideal has never been run. That is the single most valuable addition this literature could receive, and it is open question 1.

---

## 6. Included studies

| Study | Setting | Design | Channel | Elasticity | Risk of bias |
|---|---|---|---|---|---|
| Ang et al. 2024 | China | RD + placebo | wealth | **+0.18** | **LOW** |
| Dettling and Kearney 2014 | US MSAs | IV: supply elasticity | wealth / cost | **+0.81 / −0.39** | MODERATE |
| Daysal, Lovenheim, Siersbæk and Wasser 2021 | Denmark | IV: first-home price + registers | wealth | **+0.23** | MODERATE |
| Liu and Zhang 2024 | China | DiD: purchase restrictions | cost (prospective buyers) | **−0.82** | MODERATE |
| Clark, Yi and Zhang 2020 | China | IV + city FE | aggregate | −0.94 pp per 1% | SERIOUS |
| Clark and Ferrer 2019 | Canada | IV: initial-area prices | aggregate | +2.0% to +11.8% odds | SERIOUS |
| Li 2024 | Global, 1870–2012 | IV: construction costs, land prices | aggregate | −0.030 births/woman per +10% | SERIOUS |
| *Housing Purchase Restriction 2021* | China | DiD | aggregate | *units undefined* | **CRITICAL — exclude** |

Elasticities are percent change in fertility per one percent change in the price or wealth measure, computed at each study's own sample mean with every baseline read from that study's own descriptive-statistics table (`extraction/housing-costs-effects-harmonised.csv`).

Two studies were routed out on the boundary rule and one on the outcome. A 2026 *PNAS* cohort-DiD of a Chinese housing-provident-fund reform is a strong design with a clear positive fertility effect, but the reform "expanded access by lowering down payment ratios, reducing interest rates, and raising loan ceilings" — credit terms vary, prices do not. It belongs to C.3.e. And *Homes and husbands for all* estimates post-war US building permits on **marriage**: every estimating table has marriage as the dependent variable, and its quotable claim that housing supply "can account for 10 percent of the rise in birth rates" is the author's decomposition applied to a marriage estimate, not an estimated fertility effect. Retained as mechanism evidence, cross-referenced to A.7.

### 6.1 The naive estimator and the direction of its bias

**What is the naive estimator here?** Regress local fertility on local house prices.

It is confounded in both directions at once, which is unusual and worth stating. Places with high house prices are places with strong labour demand, high female wages and high costs of living — all of which independently depress fertility, biasing the naive estimate **negative**. But house prices also rise where incomes rise, and income raises fertility through C.1.a, biasing it **positive**. And the largest problem is simultaneity: household formation drives housing demand, so fertility causes prices as surely as prices cause fertility. The Mankiw–Weil literature exists precisely to estimate the reverse arrow, and the search routed six such papers out on direction.

The net sign of the naive bias is therefore not predictable, which is the honest statement and the reason every credible study here instruments.

**How many included studies use it? None outright** — all eight have a design. But **the exclusion restriction is where the risk concentrates**, exactly as the scope predicted: three of six instrumented studies are rated serious or critical on that domain alone. First stages are strong; the problem is that supply elasticity, construction costs, land prices and initial-area prices all plausibly affect fertility through channels other than house prices. In the Canadian study the IV estimate is roughly **six times** the OLS estimate, a gap better explained by a weak or invalid instrument than by the removal of attenuation bias.

### 6.2 Do the studies disagree? No — and that is the chapter's most secure result

The literature looks contradictory in the aggregate and is not. Once estimates are sorted by channel, the disagreement disappears entirely:

- **Wealth channel: +0.81, +0.23, +0.18.** All positive. Three countries, three designs.
- **Cost channel: −0.39, −0.82.** Both negative. Two countries, two designs.

Five independent estimates, four countries, four design classes — IV on supply elasticity, IV on first-home prices with population registers, regression discontinuity with placebo, and policy difference-in-differences — and **two of those designs postdate the framing of the hypothesis**, so the sign prediction was not fitted to them. Nothing crosses zero in the wrong direction.

This is a rare case in this review where the correct synthesis is neither to pool nor to resolve a disagreement, but simply to sort. The apparent conflict in the aggregate literature is a composition artefact, and §7.3 shows exactly how it arises.

### 6.3 The transmission ledger

| Stage | Question | Sign |
|---|---|---|
| Price rises → household faces it | Owners face a gain, not a cost; the sign depends on who | **Splits** |
| Faces it → adjusts space demand | Is space substitutable for other inputs? | Attenuates |
| Adjusts space → adjusts fertility | Or adjusts location, tenure, or co-residence instead (A.23) | Attenuates |
| Birth foregone → foregone for life | **Not measured by any of the eight studies** | **Unknown** |
| Aggregate → the phenomenon | Has the mechanism's own movement been large enough for long enough? | Setting-specific |

The fourth row is this chapter's binding gap and it is unlike the others in this review: it is not that the entries all attenuate, nor that some reverse, but that **one link has never been measured at all**. Every included study observes a birth rate in a window. None follows a cohort to completion. Until one does, the chapter cannot say whether housing costs prevent births or move them.

---

## 7. Quantitative synthesis

### 7.1 The answer in plain terms

Sorting the studies by who was actually affected makes a messy literature tidy. Every study that looked at people who already owned their home found that rising prices led to *more* children. Every study that looked at people who had to pay the higher price found *fewer*. Five studies, four countries, four different ways of doing the sums, and none of them breaks the pattern.

What cannot be done is add them together to get an answer for a whole country. That total depends on how many people are in each group, and the numbers are far enough apart that the split which would make the total come out at zero could be anywhere between a third of households owning and four-fifths owning. Almost every rich country sits inside that range, so the arithmetic cannot even tell us the direction for a given country, let alone the size.

And there is a puzzle that turns out to be the most useful thing in the chapter. China has very high home ownership, so the sums say rising prices should mean more children there. They mean fewer. The reason is that the ownership figure counts young couples who are saving to buy as though they already owned — and for them a price rise is nothing but bad news.

### 7.2 The estimate

**No forest plot is presented, and that is a decision rather than a failure.** The pooling rule bars combining the two channels, bars combining price with rent or affordability measures, and bars combining outcome levels. What survives is three wealth-channel and two cost-channel elasticities. A pooled point resting on two or three studies would convey precision the evidence does not have.

**Channel estimates.** Wealth: +0.81 (US), +0.23 (Denmark), +0.18 (China). Cost: −0.39 (US non-owners), −0.82 (Chinese prospective buyers).

**Two cautions on magnitude.** Dettling and Kearney is the outlier on both sides — its owner elasticity is three to four times the Danish and Chinese estimates — *and* it is the most-cited study in this literature, so a reader anchored on the US result will overestimate the wealth channel. And every conversion from a per-dollar effect to an elasticity assumes local linearity; Dettling and Kearney state that assumption explicitly, and it is imposed rather than tested.

### 7.3 What the identity does, and where it breaks

Applying the composition identity from §1.2 to the extracted estimates produces two results, both generated into `output/tables/housing-costs-composition-breakeven.csv`.

**First: the break-even ownership share is not pinned down, so the aggregate sign is undetermined.** Across the six pairings of one wealth estimate with one cost estimate, the owner share at which the net elasticity crosses zero ranges from **32.4% to 82.0%** — a spread of **49.6 percentage points**. Every developed country's ownership rate lies inside that interval. The aggregate elasticity is therefore not merely non-transportable in magnitude; **its sign is undetermined by the current evidence for essentially any real population.**

**Second, and more useful: the two-group identity makes a sign prediction that the data refute.** Taking urban Chinese ownership at roughly 90%, the identity predicts a **positive** net elasticity under all six pairings, from +0.08 to +0.69. The Chinese estimates are firmly **negative**.

An identity cannot be false, so the error is in the weights — and locating it is the chapter's contribution. **Conventional homeownership statistics count prospective buyers as owners.** A young couple who must purchase before marrying appears in the ownership rate, or in the household of parents who own, while facing a price rise as pure cost with no offsetting gain. The two-group split misassigns exactly the group in which the cost channel binds hardest, and it misassigns them in the settings with the fastest price growth, where they are most numerous.

This is why §5.1 specifies a **three-way** split. It is not a refinement; without it the identity gives the wrong sign.

---

## 8. Demographic significance

The phenomenon to be explained is measured in whole children — the FDT is a fall of roughly three births per woman and the SDT roughly one and a half; this mechanism offers an elasticity whose sign at the population level is undetermined across the plausible range of ownership rates, and no estimate at all in units of completed fertility.

The protocol asks for a decomposition share, a slope-sufficiency judgement and R² benchmarks. **The decomposition share and R² benchmarks cannot be computed: `data/raw/` is empty and the review has no macro panel.** That is a repository-level gap affecting every chapter, not a finding about housing. What follows is a scale check with stated inputs.

**The endogeneity check bites hard here, harder than in most chapters.** Housing prices are driven by household formation, which is itself downstream of fertility and marriage decisions. A mechanism whose own movement is caused by the phenomenon cannot have its full movement counted as a cause of it, and no included study nets out the reverse arrow. The Mankiw–Weil literature estimating that arrow was routed out of this chapter on direction, which means the chapter has excluded from view the evidence that would bound its own endogeneity.

### 8.1 Pre-modern fertility variation

For pre-modern variation, the verdict is NOT ASSESSED, because the cell is in scope and empty — no included study estimates a pre-modern effect.

The pre-modern analogue is real: household formation required a niche, a holding, a dwelling. But it currently lives inside A.7 and the European Marriage Pattern rather than here, and the boundary between "the price of housing" and "the availability of a household slot" has not been ruled on. Were it assessed, the expected sign would be negative.

### 8.2 First Demographic Transition

For the First Demographic Transition, the verdict is NOT ASSESSED, because the single available estimate rests on an instrument this chapter rates critical, and an arithmetic that clears a threshold on one such estimate does not establish a share.

The arithmetic is worth showing, because it is what a less careful chapter would report as a finding. Li (2024) gives −0.030 births per woman per 10% real price rise; real house prices roughly tripled across the long run in the covered countries; applied linearly that implies about −0.6 births against an observed decline of two to three, or roughly a fifth of the transition. **That clears the protocol's 10% threshold and should not be leaned on.** The instrument set is construction costs and **land prices**, and land price is close to the same object as house price rather than an external shifter — §5.2 excludes exactly this instrument from the ideal design. The honest statement is that the long-run relationship is documented and not identified.

### 8.3 Second Demographic Transition

For the Second Demographic Transition, the verdict is NOT ASSESSED, because the only decomposition in the evidence base is computed against its own study window rather than against the transition, and `PROTOCOL.md` §4.2.1 forbids assigning a band on a study-window share.

The two anchors point in different directions, and the difference is the informative part — but neither can be banded.

**Where prices grew fastest, the study-level decomposition is substantial and its denominator is not the phenomenon.** Liu and Zhang estimate that China's purchase-restriction-era price growth produced roughly 2.46 million fewer births, about **10.4% of the aggregate birth reduction over their post-treatment window**, from the study's own decomposition. That is a share of a few years of Chinese births, not of the Second Demographic Transition, and the two differ by a large and uncomputed factor. Converting it requires a Chinese completed-fertility series the repository does not hold. **Labelled and not banded**, per §4.2.1.

**For the Western SDT the mechanism's own movement nets to near zero, which is a finding and not a share.** Dettling and Kearney's own calculation implies the 1997–2006 US boom raised births by about 9% over that window, against a US TFR that rose about 4%. But the sustained post-2007 US decline of roughly 19% coincides with real house prices that fell and then recovered, netting to little across the period. A mechanism whose net movement over the phenomenon's window is approximately zero contributes approximately nothing to it, regardless of its elasticity. This is a slope-sufficiency judgement rather than a decomposition, and on it the mechanism is **insufficient** for the Western decline.

**NOT ASSESSED here is a statement about the arithmetic available, not about the evidence.** The channel elasticities are the best-identified quantities in this chapter (§9 rates them MODERATE). What is missing is a denominator: no study decomposes a housing effect against a full transition, and §7.3 shows that even with one, the aggregate elasticity would be a composition statistic rather than a transportable parameter. Anyone quoting a single number for "the effect of housing costs on fertility" has quoted a property of a population, not of a mechanism.

---

## 9. GRADE rating

**GRADE** is the standard scheme for rating how much certainty a body of evidence supports, from HIGH down to VERY LOW, with every downgrade attributed to a named defect.

| Phenomenon | GRADE | Downgrades | Demographic significance |
|---|---|---|---|
| PM | **No evidence** | No body of evidence to rate; the mechanism's pre-modern analogue sits in A.7. | NOT ASSESSED |
| FDT | **VERY LOW** | *Risk of bias*: one estimate, exclusion restriction rated critical. *Indirectness*: 1870–2012 price series with severe measurement heterogeneity. *Imprecision*: a single study. | NOT ASSESSED |
| SDT, **channel signs** | **MODERATE** | Five independent estimates, four countries, four design classes, one at LOW risk of bias, all consistent in sign, two designs postdating the hypothesis. Downgraded one level for *risk of bias* in the exclusion restrictions of three of six instrumented studies. Not downgraded for inconsistency: sorted by channel, there is none. | — |
| SDT, **aggregate elasticity** | **VERY LOW** | *Indirectness*: the aggregate is a composition statistic, not a behavioural parameter. *Imprecision*: §7.3 shows the break-even ownership share spans 49.6 points, so the sign is undetermined for real populations. *Inconsistency*: the two-group identity mispredicts the Chinese sign. | NOT ASSESSED |

Splitting the SDT row is the chapter's structure in miniature, and it is the reverse of the usual pattern: **moderate confidence in the two behavioural parameters, very low confidence in the aggregate built from them.** The uncertainty is not in the studies. It is in the composition.

---

## 10. Verdict

Housing costs move fertility in opposite directions for different people, and the evidence on that is good. Every study of people who already own finds rising prices raise fertility; every study of people who must pay finds the reverse. Five estimates, four countries, four designs, no exceptions.

**The one number to carry away: the break-even ownership rate lies somewhere between 32% and 82%.** That is the share of owners at which the two channels cancel, and the interval is wide enough to contain every developed country. It follows that there is no such thing as "the" effect of housing costs on fertility at the population level — the aggregate elasticity is a composition statistic that changes with the ownership rate even when no household changes its behaviour.

Three qualifications belong inside this verdict.

The two-group owner/renter split, which is how this literature is usually summarised, predicts the wrong sign for China under every pairing of the extracted estimates. The resolution is that conventional ownership statistics count prospective buyers as owners, and for them a price rise is pure cost. Any aggregate built on the two-group split is built on a misclassification of the group in which the effect binds hardest.

Not one of the eight studies measures completed fertility. The chapter cannot distinguish postponed births from prevented ones, and if the effect is mostly postponement the demographic verdict shrinks sharply.

The demographic significance is NOT ASSESSED, and that is an arithmetic limit rather than an evidential one. The only decomposition available — about a tenth of the birth reduction in China's high-price-growth window — is measured against a few years of Chinese births rather than against the transition, and cannot be banded. Over the Western SDT the mechanism's own net movement has been near zero, so on slope sufficiency it is insufficient there.

**What would change it:** a rent shock with a credible design, reporting effects separately for owners, renters and prospective buyers, followed to completed fertility. After full screening the rent stratum contains **no quasi-experimental study at all**, so this is not a refinement of existing work but a literature that does not exist.

---

## 11. Open questions

**PI calls required.**

1. **Should the `phenomena` field be formally widened to admit FDT evidence?** `HYPOTHESES-v5` scopes C.2.c to the SDT; the RA admitted FDT-era evidence on 2026-07-31 and the registry has not been updated.
2. **Where is the boundary with A.7 on the pre-modern cell?** The niche/holding/dwelling mechanism is real and currently sits in A.7. Either C.2.c's PM cell is genuinely out of scope, or A.7 is holding evidence that belongs here.
3. **Does routing the Mankiw–Weil reverse-direction literature out of this chapter leave the endogeneity unbounded?** §8 notes the chapter has excluded from view the evidence that would bound its own reverse-causality problem.

**Evidence and extraction priorities.**

4. **A rent-identified estimate with credible exogeneity** — the single most valuable addition, and currently absent entirely.
5. **Tenure splits should be a default, not a robustness check.** Only three of eight studies report one and none reports all three groups.
6. **Better instruments.** The binding constraint is the exclusion restriction, not the first stage. Land prices instrumenting house prices is close to circular.
7. **Prospective buyers as a directly identified group.** §7.3 shows this is where the cost channel binds; no study identifies it directly.
8. **Tempo versus quantum.** Nothing in the pool addresses whether housing costs postpone or prevent births. Cross-reference A.11.
9. **Independent verification.** All screening, gating, extraction and risk-of-bias ratings are single-reader.

**Studies that do not exist and should.** The design in §5.2, in full: a rent shock, three-way tenure split measured pre-shock, one specification, followed to completed fertility.

**A finding about the field.** The large demography literature on housing and fertility studies tenure, housing type and residential mobility rather than prices, and under the boundary rule most of it routes to A.23 or to mechanism and context. **The housing-and-fertility literature is mostly not about the price of housing.**

---

## 12. References

Effect estimates and full bibliographic detail: `extraction/housing-costs-effects.csv`, `extraction/housing-costs-effects-harmonised.csv`, `extraction/housing-costs-study-extraction.csv`, `extraction/housing-costs-risk-of-bias.csv`. Search and screening record: `literature/search-logs/housing-costs-*`.

---

## Provenance and standing caveats

This chapter is written on 30 of 78 wanted full texts (38%).

That figure understates the chapter's evidential position rather than overstating it, which is unusual in this review. **The finding that would survive full retrieval is the channel-sign result**: the identified core is complete at 15 of 15 assessed, the 48 outstanding studies are the associational stratum, and associational studies cannot overturn a sign established by four quasi-experimental designs. **The findings that might not are the magnitudes** — three wealth estimates spanning a factor of four — and consequently the break-even interval in §7.3, which would narrow if the spread narrowed.

**Objection over which this chapter was written.** None recorded from the PI. The evidence-base posture was set by the RA on 2026-07-31: a thin price-variation evidence base is an acceptable outcome, and the obligation is to *report* the shrinkage rather than engineer around it. §4 and open question 9 discharge that. This rewrite changes the previous draft's SDT verdict from "demographically significant in high-price-growth Asian settings; insufficient for the Western SDT" to **NOT ASSESSED**. The change is not a downgrade of the evidence but an application of `PROTOCOL.md` §4.2.1: the 10.4% figure the previous draft leaned on is a share of Liu and Zhang's own post-treatment window, not of the transition, and a study-window share cannot carry a band. The slope-sufficiency judgement for the Western decline — insufficient, because the mechanism's own net movement is near zero — is unchanged. §7.3 is new and unreviewed.

**Numbers sourced from abstracts rather than full text.** Daysal et al. was read in its NBER working-paper version; the headline estimate was reconciled against the published *Journal of Public Economics* abstract and matches. Subsidiary specifications were not reconciled. Liu and Zhang exists only as an SSRN preprint.

**Not independently verified.** All screening, gating, extraction and risk-of-bias ratings are single-reader; `ra_verified = no` throughout.

**Figures not derived from project data.** The ownership shares used to read the break-evens in §7.3 (US 65%, Denmark 60%, Canada 67%, urban China 90%) are conventional reference figures, not computed here — `data/raw/` holds no macro panel. They affect only which side of a break-even a country falls on, not the break-even interval itself, which is computed entirely from the extracted elasticities. The FDT and SDT decline magnitudes in §8 are likewise conventional.

**Generated inputs.** §7.3 is computed by `source/analysis/c2c_composition_identity.py` into `output/tables/housing-costs-composition-breakeven.csv` and `housing-costs-composition-identity.json`.
