# C.2.b — Rising Direct Costs of Children

**Category:** Economic · Cost of Children
**Primary mechanism:** Rising out-of-pocket expenditure required per child raises the price of a child, so households buy fewer.
**Cross-references:** C.2.a (childcare price) · C.2.c (housing) · C.2.d (net-of-transfer price) · C.2.e (the mother's time) · C.3.a (the child's productive value) · C.3.b (compulsory schooling) · C.3.d (chosen quality) · D.2.d (the norm defining what a child requires) · A.1 (mortality expectations)
**Status:** TICK-079 · drafted 2026-09-03 · **not PI-reviewed** · written on 10 of 16 wanted full texts (63%)

---

## 1. The claim

This chapter explores the effect of the direct out-of-pocket cost of a child on the total fertility rate — the number of children a woman would have over her life at current birth rates.

### 1.1 In plain terms

In plain terms: children cost money to raise — school fees, doctor's visits, clothes, all the things a family has to buy for a child and not for itself — and if those things get more expensive, families have fewer children.

That is an ordinary piece of household reasoning, and it is worth saying what would make it wrong. It would be wrong if the things that got more expensive were things parents *choose* to buy rather than things a child requires; a family that spends more on each child because it decided to have fewer is not a family responding to a price. It would also be wrong if the money cost is small next to what a child costs in a parent's time and career, which is a different chapter's subject.

### 1.2 The technical claim

The parameter this chapter estimates is the change in completed fertility caused by an exogenous change in the price of the goods and services a child requires, measured in children per unit proportional change in that price.

**The margin is intensive, not extensive.** The claim is about how many children a household has, not about whether it has any; the two studies that identify it cleanly measure completed family size and the probability of a *further* birth, both movements along the number of children rather than into or out of parenthood.

Three restrictions are carried from the search scope and they do most of the work. The exposure is a **price faced**, not an **expenditure observed** (§2). It is the price of *child-specific goods and services* — schooling outlays, child health costs, child-specific consumption — and not of childcare (C.2.a), housing (C.2.c), the mother's time (C.2.e) or the child's chosen quality (C.3.d). And "required" is load-bearing: an outlay a household elects is a quantity, not a price.

---

## 2. Theoretical mechanism

In the standard household model a child enters the budget constraint at a price, and a rise in that price reduces the quantity demanded, income held constant. C.2.b is that comparative static applied to the money cost of a child.

**The identity/behaviour split is the whole difficulty here, and it runs the opposite way from most chapters.** Spending per child is quantity chosen times price faced, and fertility and quantity-per-child are chosen together. A household with two children spends more per child than an otherwise identical household with five, because the same budget divides fewer ways and because the parents who chose two were choosing intensity. So the correlation between expenditure per child and fertility is negative **under any quantity–quality model, with no price change anywhere**. The canonical cost-of-a-child series are outputs of exactly that identity: USDA's *Expenditures on Children by Families* is computed from household budgets *conditional on family size and income*. Regressing fertility on such a series recovers the budget constraint that generated it.

**The naive estimator, and the direction it is wrong in.** The naive estimator regresses fertility on observed expenditure per child. It is biased *toward* the hypothesis: the budget identity alone delivers a negative coefficient, so a naive estimate will find the predicted effect whether or not any price has moved. Every study in §6 is included precisely because it does not use that estimator, and the 99 records in `COST_SERIES_MEASUREMENT` are held out of the primary cell for the same reason.

What would make the hypothesis wrong, then, is not an absence of correlation — the correlation is guaranteed. It would be wrong if exogenous movements in the price of required child goods left fertility unmoved, or moved it the other way. Two mechanisms would produce the latter, and both appear in the evidence below. A cheaper child-specific good can raise the *return* to investing in a child, inducing substitution toward fewer, better-invested children (C.3.d). And a cheaper child *health* good can lower expected child mortality, which reduces the births held as insurance (A.1). Both are price effects, and neither is this chapter's.

### 2.1 Attrition ledger: from the price measured to the price faced

The template requires an attrition ledger for any mechanism stated as a rate or an identity. C.2.b's is neither — it is a behavioural price response — so the usual conception-to-survival ledger does not apply. The analogous ledger for a price mechanism runs between the price that is *counted* and the price a household actually *faces*, and it matters because §8 computes a share from an index.

| stage | question | C.2.b |
|---|---|---|
| list price → price faced | is the counted price the one the household pays? | CPI prices a service at list; public provision, subsidy and insurance mean most households pay far less. Sign: the index **overstates** the price level and probably its rise |
| price faced → required outlay | is the priced good required, or elected? | college tuition and private K-12 dominate the index's rise and are substantially chosen. Sign: **overstates** the required component |
| required outlay → cost of a child | is the good child-specific? | medical care is priced for all ages, not children. Sign: **dilutes**, direction ambiguous |
| this chapter's price → the full price of a child | is the measured bundle the whole cost? | childcare, housing and the mother's time are excluded by scope §3. Sign: **understates** the total cost of a child, though not this chapter's parameter |

**Three of the four entries point the same way**: the index overstates the price of a required child-specific good. That is a bias *toward* the hypothesis in §8, and it is one of the two candidate explanations for the post-1978 over-prediction in §8.3.

---

## 3. Search strategy

Frozen at `literature/search-logs/child-cost-direct-search-scope.md` before any query, with nine walls, thirteen estimand cells and eight required tags. Reproducible end to end from `source/build/goldset/317`–`327` and `source/build/318`, `source/analysis/c2b_demographic_significance.py`.

**The query is a set of seven arms, not one query.** The fee-abolition literature is indexed in a policy-evaluation vocabulary — "user fees", "fee abolition", "tuition-free" — sharing almost nothing with the economics-of-fertility vocabulary that reaches the cost-of-children literature. Union primary recall was **13 of 14** anchors (93%) at a deduplicated frame of 963 records.

**Two walls were declared unenforceable at the screen in advance, and both were right to be.**

*Wall 4, C.2.e's time cost.* "Cost of children" is the shared phrase of this chapter and of the child-penalty literature. In the free-seed harvest, 17 of 130 records were the latter — including **5 of the 6** returned by "cost of childbearing". The separation was therefore built into the exposure axis rather than left to the screen. At full screen the boundary cell held **67 records against the primary cell's 21**: C.2.e's literature is three times this chapter's *inside this chapter's own frame*.

*Wall 1, C.3.d's chosen quality.* Quantity–quality vocabulary shares nothing with "cost of children", so the arm was calibrated but excluded from the screened union — a wall that does not leak does not need retrieving. The wall still bites at synthesis (§7), just not at retrieval.

**The boundary ruling that decided the chapter** was made against a specific prediction. Scope §16.2, written from titles alone, predicted that fee-abolition studies would identify through the mother's own schooling rather than the price of her children, and required a `channel` tag on every record entering the schooling cell. At full text the prediction held **three times out of three** (§6).

**The homonym was measured, not assumed.** "Cost of children" returns 740 records unrestricted, 206 of which intersect the paediatric cost-of-illness vocabulary; inside the fertility-restricted frame the residue is **10**. The outcome axis separates the two literatures unaided, and no screen rule was spent on it.

---

## 4. PRISMA flow

| stage | n |
|---|---|
| deduplicated union frame | 963 records |
| free seeds recovered from neighbouring chapters' pools | 130 |
| anchors resolved | 32 of 32 (zero ghost citations) |
| screen universe after injection | **1,061 records** |
| title/abstract screened | 1,061 (100%) |
| primary cell | 21 records = **16 studies** |
| full text retrieved | **10 of 16 studies (63%)** |
| extracted | 9 records = 8 studies (twins counted once) |
| admitted after the full-text channel ruling | **6 records = 6 studies** |
| of which cleanly in a C.2.b cell **and** correctly signed | **3** |

Three features change how the rest should be read.

**The screen could not be truncated.** A five-stratum depth probe spaced across the citation-ranked universe returned primary counts of **[1, 1, 0, 0, 2]** head to tail. The curve is flat, and the single cleanest primary record sat in the *last* stratum. A citation-ordered partial pass would have missed both the kibbutz privatisation and the Ghana scholarship trial. Prevalence in the probe was 4/150 = 2.7% (Wilson 95% CI 1.0–6.7%), projecting 11–71 for the universe; the full pass found 21, inside the interval.

**The largest non-excluded cell is not an effect literature.** `COST_SERIES_MEASUREMENT` holds **99 records** against the primary cell's 21 — five times as many. This frame is dominated by work measuring what a child costs rather than estimating what that cost does to fertility. That is §2's identity appearing as a population statistic, and it is the single most useful description of the field.

**Retrieval, not screening, is the binding constraint.** The automated ceiling was 17 of 62 studies across all tiers; PMC was probed and measured **empty**, as it was for C.6.a. Seven priority studies were retrieved by hand and installed by matching the DOI printed inside each document.

---

## 5. The ideal design

### 5.1 The ideal estimand

The change in completed fertility caused by an exogenous, unanticipated, permanent change in the money price of goods and services a child *requires* — holding household income, the price of the mother's time, the price of childcare and housing, and the chosen level of investment per child fixed — in a population within the phenomenon's window.

### 5.2 The design that would identify it

A policy that changes the out-of-pocket price of a required child-specific good for some households and not others, for reasons unrelated to their fertility intentions, with the change large enough to move behaviour, no simultaneous change in the quality of the good, no accompanying transfer, and completed-fertility follow-up. The comparison must be between households facing different prices for their *next* child, not between women with different amounts of their own schooling.

### 5.3 Distance from the ideal

| study | distance from the ideal design |
|---|---|
| Ebenstein, Hazan & Simhon (kibbutz) | closest. A genuine change in who pays, exogenous variation in its size across communities, completed fertility. Fails on: the treatment is extreme (0→100% of cost), and members select into and out of privatising kibbutzim |
| Burlando & Bbaale (Uganda UPE) | close on identification, far on setting. The price of the *next* child differs by household composition, exactly as the ideal requires. Fails on: fee cut bundled with a class-size rise, and TFR ~6.2 |
| Wanamaker (emancipation) | careful design on a price the chapter only half owns: a shadow price net of the child's productive value |
| Ito & Tanaka (South Africa) | well identified for *its* estimand; the price and the return-to-quality move together, so it does not identify this one |
| Winegarden & Murray (Europe 1875–1913) | far. Five-country ecological time series with a simulated counterfactual; insurance coverage proxies the price |
| Xia (Sierra Leone) | far. The paper's own channel is revised mortality expectations, and the outcome is *desired* fertility |

---

## 6. Included studies

| study | setting | design | exposure | direction | outcome | effect | channel | risk of bias |
|---|---|---|---|---|---|---|---|---|
| Burlando & Bbaale 2021 | Uganda, UPE 1997 | DiD on household composition × policy | fees waived for ≤4 children, so a 5th still cost money | FALL | realized | **−4.2pp** on another birth within 46 months (8% of mean) | PRICE_OF_CHILD | MODERATE |
| Ebenstein, Hazan & Simhon 2015 | Israeli kibbutzim, post-1996 | variation in the rise in cost-sharing across kibbutzim | collective → parental cost of children | **RISE** | realized | **−0.59 children** lifetime (~20% of a 3-child mean) | PRICE_OF_CHILD | MODERATE |
| Winegarden & Murray 2004 | 5 European countries, 1875–1913 | time series + simulated counterfactual | health-insurance coverage | FALL | realized | insurance **retarded** the decline in marital fertility | PRICE_OF_CHILD | SERIOUS |
| Ito & Tanaka 2018 | South Africa, MCH fee abolition | DiD on facility availability × timing | maternal and child health user fees | FALL | realized | **−27 to −32%** fertility | PRICE_OF_CHILD | SERIOUS |
| Wanamaker 2014 | US South, 1850–1870 | household panel, slaveholding shocks | shadow price of own children | **RISE** | realized | strong negative price–fertility relation | PRICE_OF_CHILD | MODERATE |
| Xia 2022 | Sierra Leone, FHCI 2010 | DiD on birth timing × transport cost | health user fees for under-fives | FALL | **desired** | significant fall in desired fertility | BOTH_UNSEPARATED | CRITICAL for this estimand |

**Routed out at full text — the channel ruling.** Uganda's 1997 UPE appears in this pool many times, and it identifies two different things depending on who is compared with whom. Burlando & Bbaale exploit the fact that fees were waived for up to four children per household, so a mother with four or more primary-age children faced an unchanged price for her *next* child while a mother with fewer faced a lower one. That contrast isolates the price of a child. Keats (2018) uses the same reform as a discontinuity in the *woman's own schooling*, with mechanisms of contraceptive use before first pregnancy and delayed marriage; Wakano & Yamada (2025) instrument female years of education with the *termination* of Kenya's UPE; Duflo, Dupas & Kremer (2021) randomise scholarships that pay for the recipient's own secondary education. All three estimate an education effect and **all three route out**. Burlando & Bbaale say so themselves: the UPE literature "cannot separate the roles of reducing monetary costs to schooling, improvements in access, changes in desired fertility levels, or changes in the opportunity cost of fertility for mothers."

**Estimator disagreement.** There is no disagreement to resolve, because there is nothing to pool. Stratified on cell × outcome level × direction — the strata scope §12 forbids pooling across — the largest stratum contains **two** studies. Stage 9 therefore resolves to narrative synthesis, and no pooled elasticity exists.

**The disagreement that does exist is about sign, and it is informative.** Three studies find a higher price of children going with lower fertility (Burlando, Ebenstein, Wanamaker). One finds a *lower* price of children going with *lower* fertility, and its authors attribute this to quantity–quality substitution (Ito & Tanaka). One finds a lower price slowing rather than causing the decline (Winegarden). These are not contradictory estimates of one parameter; they are estimates of different parameters that the vocabulary of "the cost of children" makes look alike.

---

## 7. Quantitative synthesis

### 7.1 The answer in plain terms

When something a child needs genuinely gets more expensive — and when you can be sure it is the price that changed, not the family's ambitions for the child — families do have fewer children. Two good studies show this, one in Israeli communities that stopped paying for members' children collectively, and one in Uganda where school fees were waived for the first four children in a family but not the fifth.

But the same evidence will not carry the weight the hypothesis needs. Only one of these studies is from a rich country in the period the hypothesis is about. And when you look at what actually happened to the price of raising a child in the United States over the last sixty years, the answer does not fit either: on the broadest measure available for the whole period, the real price barely moved, while births fell by more than a third.

### 7.2 The estimate

No pooled estimate is reportable. The two cleanly identified estimates are **−0.59 children** in lifetime fertility for a shift from full collective subsidy to full private cost (Israel, SDT window), and **−4.2 percentage points** in the probability of a further birth within 46 months for households whose marginal child lost a fee exemption (Uganda, high-fertility setting). They share a sign and nothing else — different outcomes, different populations, different magnitudes of treatment, and no basis for averaging.

Read as an arc elasticity, the kibbutz result is about **−0.2**: roughly a 20% fall in fertility for a change that moved parents from paying nothing to paying everything. It is used below as an **upper bound**, for three reasons stated by the authors or visible in the design — they warn the elasticity "may not be constant"; a 0→100% cost shift is not the marginal price change a price index measures; and it is one moderate-risk study of an unusual population.

---

## 8. Demographic significance

**The phenomenon to be explained is measured in whole children; this mechanism offers percentage changes in a relative price, convertible into children only through an elasticity of which this chapter has exactly one estimate.**

That units check is the reason the section below is short on arithmetic and long on caveats. The mechanism and the phenomenon are commensurable in principle — unlike, say, a bounded multiplier against a whole-child decline — so a share is computable. But every share passes through a single number taken from a single study of an extreme treatment, and the honest output is a bound, not an estimate.

Denominator throughout: the **change** in US TFR over the window the exposure series covers, from `output/tables/child-cost-direct-price-index.csv`, built in `source/build/318_c2b_child_price_index.py` from BLS CPI components (via DBnomics) deflated by all-items CPI, and World Bank TFR. Numerator, denominator, source and window are given at each share.

### 8.1 Pre-modern variation

For pre-modern variation, the verdict is **NOT ASSESSED**, because HYPOTHESES-v5 §C.2.b registers this hypothesis against FDT and SDT only and no pre-modern cell was screened.

Were it assessed, the sign would be positive-for-the-hypothesis: Wanamaker's antebellum evidence, which straddles the PM/FDT boundary, finds fertility falling as the net price of own children rises. That record is jointly claimed with C.3.a and cannot be allocated here.

### 8.2 First Demographic Transition

For the FDT, the verdict is **NOT ASSESSED**, because no price series for child-specific goods exists for 1870–1965 and the share therefore cannot be computed, not because the cell is empty.

The cell is not empty — it holds Winegarden & Murray, and one jointly-claimed record — and this is a data absence rather than a literature absence. It should be recorded as such and not softened into NEGLIGIBLE.

**The sign, if it could be assessed, would run against the hypothesis as a cause of the FDT.** Winegarden & Murray find that early health insurance, by lowering the cost of bearing and rearing children, **retarded** the secular decline in marital fertility. In the one FDT-window study this chapter has, the mechanism is a brake on the transition, not an engine of it. A chapter arguing that rising child costs caused the FDT would have to explain why the best available FDT evidence has the cost of children *falling* and the fall *slowing* the decline.

### 8.3 Second Demographic Transition

For the SDT, the verdict is **MINOR**, because on the only price series covering the whole window the real price of child-specific goods rose 10.9% against a 36.8% fall in fertility, which at an upper-bound elasticity of −0.2 accounts for 13% of the decline.

The arithmetic, checkable inline. Numerator: −0.2 × (+10.9%) = **−2.2%** implied fertility change, or −4.7% when the elasticity is applied decade by decade and summed rather than end to end. Denominator: US TFR 2.56 (1967) → 1.62 (2023) = **−36.8%**. Source: `child-cost-direct-price-index.csv`, `long_run_1967_equal` arm — educational books and supplies, medical care, and apparel, deflated by all-items CPI. Window: 1967–2023, which is the whole SDT window the series can reach; BLS publishes no education price series before 1967 and no tuition series before 1977-12. Share: **6% endpoint, 13% timing-aware**. Band: **MINOR**.

**Three things qualify that number, and the second is the most important finding in the chapter.**

*The arms disagree, and the disagreement is diagnostic.* Adding tuition to the index raises the implied share to 190–365% over 1978–2023 — above 100%, which the review treats as a diagnostic of a wrong denominator. Here the denominator was checked and matches the window. What the impossible share identifies instead is an inconsistency between the elasticity and the exposure measure: **after 1978 the education-bearing price arms rose 79–205% in real terms while US fertility fell only 8.1%.** The mechanism does not under-predict there; it over-predicts by two to four times. Either the index overstates the price parents actually face — likely, since what carries it is college tuition and a K-12 series priced off *private* schooling, neither of which is the required outlay most parents meet — or the kibbutz elasticity does not transport. Both cannot hold, and neither helps the hypothesis.

*Strip education out and the sign flips.* The `without_education` arm — medical care and apparel — **fell 16.6%** in real terms, implying fertility should have risen. The component carrying every favourable number is college tuition, which scope ruling 2 assigns largely to C.3.d as *chosen quality* rather than to C.2.b as a required price.

*The timing is wrong in the ordinary sense too.* Decade by decade, weighting by absolute movement in TFR, **63% of the movement in US fertility since 1967 runs against the mechanism**. The 1970s alone are 46% of all movement: TFR fell 2.48 → 1.84 while the real price of children fell 13.3%. The 1980s are another 17%, with fertility *rising* as prices rose 21%.

**No banded share exceeds 100%.** The only share banded in this chapter is the 13% in §8.3. The 190–365% figures are reported as a diagnostic and explicitly not banded, and the reason they are impossible is identified in the text rather than left for a reader to notice.

**Endogeneity check.** The exposure is a consumer price index and is not plausibly caused by the fertility decline it is being used to explain, with one exception worth naming: per-pupil schooling prices are shaped by cohort size, which is a function of past fertility. That channel is small in a CPI, which prices a service rather than dividing a budget by a shrinking cohort, and is not netted out here.

---

## 9. GRADE

| phenomenon | rating | downgrades |
|---|---|---|
| Pre-modern | **No evidence** | out of registry scope; no cell was screened. Would require a PM-window study of an exogenous change in the price of child-specific goods |
| FDT | **VERY LOW** | risk of bias (the one direct study is a five-country ecological time series, SERIOUS); imprecision (n=1 plus one jointly-claimed record); indirectness (insurance coverage proxies the price) |
| SDT | **VERY LOW** | imprecision (n=1: a single study, in Israeli kibbutzim); indirectness (an extreme 0→100% treatment in an unusual population, extrapolated to marginal price changes); inconsistency (the macro exposure series contradicts the micro estimate in two incompatible directions, §8.3) |

No rating is higher than VERY LOW and none of the six admitted studies is at LOW risk of bias. **The chapter has no low-risk estimate of its own parameter.**

---

## 10. Verdict

**Rising direct costs of children are a real mechanism with a correctly signed effect, and they cannot carry the Second Demographic Transition. On the only price series covering the whole period, the real price of the goods a child requires rose about 11% while American fertility fell 37% — worth roughly 13% of the decline at an elasticity that is deliberately generous. The number to carry away is 13%.**

Two qualifications belong in the same breath. First, that 13% is an upper bound built on one study: a natural experiment in Israeli kibbutzim that moved parents from paying nothing for their children to paying everything, which is not the kind of price change any rich-country household has faced. Second, the price of children did not move the way the story requires. It *fell* through the 1970s, the decade in which American fertility fell fastest, and rose through the 1980s, when fertility recovered. Sixty-three per cent of the decade-to-decade movement in US fertility since 1967 runs against the mechanism.

The one component that did rise steeply is college tuition — and a family's spending on university is close to the definition of an investment a household chooses rather than a price it must meet, which puts it in C.3.d's territory rather than this chapter's. Strip education out and the measured price of children *fell*, implying fertility should have risen.

For the First Demographic Transition the position is stranger and worth stating plainly: the best available study finds the mechanism working as a **brake** on the transition rather than a cause of it, with cheaper children slowing the decline in marital fertility across five European countries between 1875 and 1913.

---

## 11. Open questions

**PI calls.**

1. **Residual or total?** §3 rules C.2.b the residual after childcare, housing, the mother's time, chosen quality and transfers. The alternative makes this chapter's estimate a function of five unfinished chapters. The ruling generalises: C.2.f and C.3.f have the same shape.
2. **Caldwell 1976 is now the seminal citation of four chapters** (C.2.b, C.3.a, C.3.b, D.1.b). Not a defect, but a shared seminal citation was the evidence that a wall was broken on C.2.c.
3. **The symmetry assumption.** The registered claim is about a price *rise*; most clean shocks are falls. This is now less pressing than at stage 2 — the kibbutz privatisation, the UPE termination and slave emancipation are all rises — but two of those three route elsewhere.
4. **New: the elasticity/index inconsistency (§8.3).** Post-1978 over-prediction by 2–4× is a substantive result about measurement, not a nuisance. Whether the review wants a general rule for what to do when a macro exposure series and a micro elasticity are mutually incompatible is a protocol-level question.

**Retrieval priorities.** Six tier-1 studies remain, of which two are proxy jobs: `10.1111/padr.12538` (tuition-free policy and early childbearing) and `10.1007/s10834-006-9037-4` (college tuition and fertility in Taiwan). Four are browser jobs on hosts that refuse `curl` but are not paywalled. The full queue is at `literature/search-logs/child-cost-direct-retrieval-priority.md`.

**Studies that do not exist and should.** There is no study of an exogenous change in the price of a *required* child-specific good in a rich country during the SDT. Every rich-country price movement in this chapter is either a chosen investment (tuition) or measured on a population that is not the general one (private-school K-12). The single most valuable addition would be a policy that changed the out-of-pocket price of a universally required child good — school meals, uniforms, compulsory materials, paediatric co-payments — differentially across households in an OECD country, with completed-fertility follow-up.

---

## 12. References

Burlando, A. & Bbaale, E. (2021). Fertility Responses to Schooling Costs: Evidence from Uganda's Universal Primary Education Policy. *Economic Development and Cultural Change*. `10.1086/713938`
Duflo, E., Dupas, P. & Kremer, M. (2021). The Impact of Free Secondary Education: Experimental Evidence from Ghana. NBER WP 28937. *(routed out)*
Ebenstein, A., Hazan, M. & Simhon, A. (2015). Changing the Cost of Children and Fertility: Evidence from the Israeli Kibbutz. *The Economic Journal*.
Ito, T. & Tanaka, S. (2018). Abolishing user fees, fertility choice, and educational attainment. *Journal of Development Economics*. `10.1016/j.jdeveco.2017.09.006`
Keats, A. (2018). Women's schooling, fertility, and child health outcomes: Evidence from Uganda's free primary education program. *Journal of Development Economics*. `10.1016/j.jdeveco.2018.07.002` *(routed out)*
Wakano, A. & Yamada, H. (2025). The impact of terminating universal primary education on fertility: Evidence from Kenya. *International Journal of Educational Development*. `10.1016/j.ijedudev.2025.103361` *(routed out)*
Wanamaker, M. H. (2014). Fertility and the Price of Children: Evidence from Slavery and Slave Emancipation. *The Journal of Economic History*. `10.1017/s0022050714000850`
Winegarden, C. R. & Murray, J. E. (2004). Effects of early health-insurance programs on European mortality and fertility trends. *Social Science & Medicine*. `10.1016/s0277-9536(03)00403-9`
Xia, F. (2022). Infant Mortality and Desired Fertility: The Case of the Free Health Care Initiative in Sierra Leone. *The Journal of Development Studies*. `10.1080/00220388.2022.2081501`

---

## Provenance and standing caveats

**This chapter is written on 10 of 16 wanted full texts (63%).**

**The findings that would survive full retrieval are the channel ruling, the units contradiction in §8.3, and the FDT sign; the findings that might not are the count of cleanly-identified studies and the MINOR band on SDT.** The channel ruling held three times out of three at full text and the six outstanding studies include four more fee-abolition papers that the same ruling is likely to route out. The §8.3 contradiction is a property of the price index and the single available elasticity, and no additional study changes it unless it supplies a competing SDT-window elasticity. The MINOR band is the vulnerable finding: it rests on one elasticity, and a second SDT-window estimate — the Taiwanese tuition study is the nearest candidate — could move the band in either direction.

**Numbers taken from abstracts rather than full text:** none. Every effect in §6 is read from the full text. The six unretrieved tier-1 studies contribute no numbers to this chapter and are excluded from every count in §4 below the retrieval row.

**Objections over which this chapter was written.** The routing of Keats, Wakano & Yamada and Duflo, Dupas & Kremer out of the primary cell is a judgement about what their designs identify, made against the papers' own framing in two of the three cases. A reader who thinks fee abolition should count as a price change regardless of the identifying contrast would have a larger and differently-signed schooling cell. The re-celling of Wanamaker to a jointly-claimed cell is likewise contestable: her price is a genuine price, but it is net of the child's productive value, which the review assigns to C.3.a.

**Stage 11 is incomplete.** GRADE ratings here are the assessment of one rater. PROTOCOL §5 requires three independent raters and that requirement is open.
