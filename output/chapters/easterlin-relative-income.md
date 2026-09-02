# Chapter C.6.a: Easterlin Relative Income and Cohort Size

**Category:** Economic · **Primary mechanism:** A generation that is large relative to the one ahead of it is crowded in the labour market, earns little against the standard it grew up with, and has fewer children — producing fertility cycles rather than a trend. · **Cross-references:** C.1.a (income), C.5.a (economic uncertainty), C.7.a (marriage market), A.9 (age structure), C.2.e (female wage — the named rival). None of these is listed in HYPOTHESES-v5; see §11, PI Call 2. · **Status:** TICK-078, drafted 2026-09-02, **not PI-reviewed**. Written on **34 of 156 wanted full texts (22%)**.

---

## 1. The claim

**This chapter explores the effect of relative cohort size on the total fertility rate.**

### 1.1 In plain terms

**In plain terms: people decide whether they can afford children by comparing what they earn to the way of life they were raised in, so a crowded generation that cannot match its parents' standard has fewer children — and because small generations then raise children in comfort, the next generation has more, and family size swings back and forth instead of simply falling.**

Two ideas are doing the work, and they are separable. The first is that what counts is not how much money young adults have but how much they have *compared with the household they grew up in*. Somebody earning a modest wage who was raised modestly may feel comfortably off; somebody earning the same wage who was raised in plenty may feel poor. The second is that the size of a generation determines its fortunes: when a lot of people are born at once, they compete with each other for jobs and housing all their lives, so they earn less than the generation before them did.

Put together, these produce a swing. A small generation does well, feels prosperous, has many children — and those many children become a large generation that does badly, feels poor, and has few children. Those few children then become a small generation, and the swing repeats. The claim is not that family size falls; it is that it oscillates, roughly on the length of a human generation.

### 1.2 The technical statement

**The parameter this chapter estimates is the change in fertility caused by an exogenous change in a cohort's earnings prospects measured against the consumption standard of the household that raised it, measured in births per woman per unit of the relative-income ratio.**

Two features of that sentence organise everything below. The benchmark is *cohort-specific* — it is the parental household's standard, not the national average and not the cohort's own past. And the exposure that is supposed to move it, relative cohort size, is the outcome's own history: the number of 25-year-olds today is the number of births twenty-five years ago. The hypothesis is therefore a difference equation, not a treatment effect, and §2 sets out what that costs.

---

## 2. Theoretical mechanism

The mechanism has three links, and they are of different kinds.

**Link 1 is labour economics.** A large birth cohort entering the labour market crowds it, depressing its own relative wages and raising its unemployment. This is a well-studied and largely uncontested relationship, and it has nothing to do with fertility.

**Link 2 is the hypothesis proper.** Earnings *relative to the aspirations formed in the parental household* determine childbearing. This is a behavioural claim about preference formation, and it is the only link that can be false in a way that matters here.

**Link 3 closes the loop.** Today's births are tomorrow's cohort size, twenty to thirty years on. This link is mechanical and is not in dispute.

**The identity/behaviour split.** Link 3 is an identity — it cannot fail. Link 1 is close to one in a full-employment economy. **Only link 2 is behavioural, and only link 2 can be tested.** A chapter that counted all three links' literatures together would report a large and well-evidenced body while saying nothing about the mechanism, and §4 shows how nearly that happened.

**What would make the hypothesis wrong.** Three things, in increasing severity. If earnings relative to the parental standard do not predict childbearing once other things are held constant, link 2 fails and the mechanism is empty. If the feedback from cohort size to fertility is real but too weak to sustain an oscillation, then the reduced-form claim survives but the *cycling* claim — the distinctive part — does not; the system converges instead of swinging. And if fertility keeps falling through a period when the mechanism predicts a recovery, the mechanism is not merely weak but wrong-signed for that period.

---

## 3. Search strategy

Reproducible from `literature/search-logs/easterlin-relative-income-search-scope.md` and scripts `304`–`316` in `source/build/goldset/`.

**Five queries, not one.** A single exposure axis calibrated against the anchor set plateaued at 15 of 21, and the misses clustered by estimand cell rather than scattering: every rival-model record is a Butz–Ward paper that never uses Easterlin's vocabulary, and the marriage-boundary records pair a cohort-size exposure with a marriage outcome. The production search is therefore five arm-specific queries — `easterlin`, `cohort-size`, `cycle`, `rival`, `marriage-boundary` — recalling **18 of 20** primary anchors at a deduplicated frame of **683** records.

**Walls, and their enforceability.** Six walls were frozen before searching. C.6.a owns variation in relative cohort size and cohort-relative earnings; C.1.a owns absolute income; C.5.a owns aggregate shocks common to all cohorts; C.7.a owns marriage-market composition; A.10 owns the sex ratio; A.9 owns mechanical age-structure effects on crude rates. **Wall 3 was declared partly unenforceable in advance:** where cohort growth acts *through* a marriage squeeze the estimate is jointly claimed by C.6.a and C.7.a and cannot be allocated. Those records are tagged `MIXED_COHORT_MARRIAGE`, reported, and never pooled — the device C.2.c established for `MIXED_PRICE_CREDIT`.

**Three homonyms cost real frame, and two were only found by stratifying the pulled corpus.** "Fertility cycles" means the *menstrual* cycle in most of the indexed literature (177 records, no gold). "Population cycles" is ecology's term for vole and predator–prey dynamics. And "relative income" anchors three unrelated literatures — this hypothesis, Duesenberry's consumption function, and the Easterlin *paradox* in subjective well-being — of which only the third is separated by a fertility outcome axis.

**Boundary rulings.** Against C.5.a: a recession is an aggregate shock and is C.5.a's; cohort size is cohort-specific by construction and is ours. Against C.2.e: Butz–Ward is the *named rival*, and studies running the two models against each other are kept as the most informative records the search can find rather than walled out.

---

## 4. PRISMA flow

| stage | n | |
|---|---|---|
| Records identified, five arm queries (deduplicated) | 683 | |
| Records from other chapters' pools (free seeds) | 131 | a genuinely separate channel |
| Cold-start anchors injected | 31 | 5 not reachable by any query |
| **Screen universe** | **798** | |
| Removed by deterministic prescreen | 89 | 6 rules, each recall-checked; 31/31 gold retained |
| **Title/abstract screened** | **709** | 100% of the universe |
| Routed to a primary cell | 141 | 19.9% yield |
| Retained in a context cell (`LINK1_LABOUR`, `THEORY`, `BOOM_ALTERNATIVE`) | 152 | |
| Full texts wanted (primary + Wall 3 boundary) | 156 | |
| **Full texts retrieved** | **34** | **22%** |
| **Extracted** | **34** | of which **6 could not be read** — scans with no text layer |

**Three features change how this chapter should be read.**

*The retrieval fraction is 22%, and it is not evenly spread.* `CYCLE_TEST` is 9 of 46; `RIVAL_TEST` 7 of 29; `RELATIVE_INCOME_FERTILITY` 4 of 29. The cell that gates the argument, `BENCHMARK_MEASURED`, is **4 of 5** — deliberately, because retrieval was prioritised on which cell could change the verdict rather than on citation counts.

*Six retrieved records cannot be read at all.* They are scans without a text layer and are recorded with `NOT EXTRACTED` in every field, so no later stage can mistake a retrieved-but-unread record for an absence. One of them is Macunovich (2000), the strongest pro-hypothesis global claim in the literature.

*The screen sensitivity was measured blind.* The 31 resolved anchors sat in the screening sheets unmarked; the ingest script is the first place they are identified. **31 of 31 were retained.**

---

## 5. The ideal design

### 5.1 The ideal estimand

Among women entering the labour market in a defined country and period, the effect on **completed cohort fertility** of a one-standard-deviation increase in **the ratio of the woman's own household income at ages 20–29 to her parental household's income when she was aged 10–16**, holding absolute income, prices, and the local marriage market fixed, measured in **births per woman per unit ratio**, observed to age 45.

### 5.2 The design that would identify it

**Source of variation:** a shock to cohort size that is not itself a product of the previous generation's fertility choices. Enumerated before searching: policy-created cohort discontinuities (Romania's Decree 770 produced a step change in a single year; China's one-child cohorts reach the labour market as an engineered deficit), war-driven birth deficits, famine cohorts, epidemic mortality, and — the cleanest and least used — **immigration waves that change the size of a labour-market entry cohort without changing anyone's birth cohort.**

**Comparison group:** adjacent birth cohorts in the same country unaffected by the discontinuity, or same-cohort individuals in regions where the shock did not bind.

**Falsifiable identifying assumption:** the shock changed cohort size at labour-market entry and did not otherwise affect the childbearing of those cohorts — testable by pre-trends in cohorts born just before the discontinuity.

**Estimating equation:** completed fertility regressed on the instrumented relative-income ratio with birth-cohort and region fixed effects, on linked administrative data with parental income observed directly, requiring a panel spanning at least the affected cohorts' full reproductive lives.

### 5.3 Distance from the ideal

| study | exposure | outcome | horizon | assignment | overall |
|---|---|---|---|---|---|
| Behrman & Taubman 1989 | **exact** (income, two generations) | completed family size | good | observational, selection-corrected | **closest on exposure** |
| Hill 2014 | close (childhood-era benchmark constructed) | any birth | partial | cohort + state fixed effects | **closest on assignment** |
| Comolli 2021 | close (occupational prestige vs parents') | first birth | partial | observational | near |
| Pampel 1993 | far (cohort size only) | TFR | n/a | cross-national panel | far |
| Jeon & Shields 2005, Xiao & Shields 2014, Norberg 2015 | far | TFR | n/a | country panel | far |
| Butz & Ward 1979, Macunovich 1993/1996/2011 | far (proxied) | period rates | n/a | aggregate time series | far |
| Wachter 1991, Lee 1974 | n/a (dynamic-systems) | births | n/a | model-implied | different question |

**No study matches the ideal.** Not one included record uses an exogenous shock to cohort size. The gap is stated in the verdict.

---

## 6. Included studies

34 extracted records in `extraction/easterlin-relative-income.csv`; 28 carry a readable estimate or result.

| cell | n | of which readable | character of the body |
|---|---|---|---|
| `BENCHMARK_MEASURED` | 4 | 4 | 3 distinct studies; **they disagree** |
| `RIVAL_TEST` | 7 | 6 | head-to-heads, no consensus winner |
| `CYCLE_TEST` | 9 | 7 | 2 formal, 3 empirical, 2 theory-only |
| `COHORT_SIZE_FERTILITY` | 7 | 6 | cross-national panels |
| `RELATIVE_INCOME_FERTILITY` | 4 | 1 | 3 unreadable — the thinnest readable cell |
| `MIXED_COHORT_MARRIAGE` | 3 | 2 | Wall 3, unallocated |

**Estimator disagreement, resolved rather than averaged.** The included estimates disagree, and the disagreement is structured rather than random.

*The naive estimator here is a bivariate regression of a fertility series on a contemporaneous cohort-size series.* Its bias direction is knowable in advance and is upward in absolute magnitude: relative cohort size at *t* is a deterministic function of births at *t*−25, so part of any measured association is the identity in link 3 rather than the behaviour in link 2. Every aggregate time-series study in this body carries that bias.

*Three disagreements, resolved:*

**(i) Benchmark measured versus proxied.** Behrman and Taubman (1989) observe income for two generations — the only study in the pool that measures Easterlin's benchmark as Easterlin specified it — and find parents' income entering at **−0.032 (t = 1.5)**, own income *not* positively significant, R² = 0.04, concluding that the test **favours the Becker formulation**. Comolli (2021), measuring occupational prestige against the parental household's on PSID event-history data, finds the opposite sign: **HR 1.17\*\*\*–1.27\*\*\***, attenuating to non-significance in younger cohorts. These do not average. They differ in exposure (income versus occupational prestige), in outcome (completed family size versus first-birth hazard) and in period, and the pooling rule forbids combining them.

**(ii) Sign robustness.** Hill (2014) is the most identified design in the pool — microdata, a constructed childhood-era benchmark, birth-cohort and birth-state fixed effects added stepwise — and its central result is that **the sign is not robust**: the coefficient runs from **−0.068\*\*\*** through **+0.127\*\*\*** and **+0.265\*\*\*** to **+0.364\*\*\*** as fixed effects are added, and flips within a single panel. Where the best-identified study finds the sign depends on the specification, a pooled point estimate from worse-identified studies is not a summary of anything.

**(iii) A sign convention that would have corrupted the pool.** Pampel (1993) defines relative cohort size as **prime-age over young** — the inverse of the young-over-prime ratio used elsewhere in this literature and in this chapter's own computation. His **+1.87\*\*\*** is therefore *consistent* with the hypothesis's negative prediction. Pooling it unre-oriented would have flipped the sign of the pooled estimate. Every cohort-size row in the extraction table now records its ratio direction explicitly.

---

## 7. Quantitative synthesis

### 7.1 The answer in plain terms

The idea works for the period it was invented to explain, and stops working afterwards. When the large post-war generation reached adulthood in the late 1960s and 1970s, it was indeed crowded, and family size did indeed fall — sharply, and in almost every rich country at once. But the story does not stop there. It predicts that the *small* generation which followed should have found life easier and had more children again. That generation reached adulthood in the 1980s and 1990s, and family size did not go back up. It kept falling. In every one of the eighteen countries examined here, the recovery the idea requires simply never happened.

And when researchers have looked hardest — using detailed records of individual families rather than national averages — the relationship has not held steady. In the single most careful study in this body, whether the effect appears positive or negative depends on which statistical controls are used. The only study that measured what the idea actually says matters, comparing families' incomes across two generations directly, found no support for it and concluded a rival explanation fitted better.

### 7.2 The estimate

**No pooled estimate is reported, and the reason is a finding rather than a limitation.** Applying the pre-registered pooling rule — stratify by link, exposure distance, outcome level and phenomenon, *then* apply the ≥3 test — no stratum reaches three poolable effects. The `BENCHMARK_MEASURED` stratum contains three distinct studies measuring three different exposures on two different outcomes. The `COHORT_SIZE_FERTILITY` stratum mixes ratio directions and country coverages. `CYCLE_TEST` estimates are model-implied dynamic properties, not effects, and scope §2 forbids pooling them with reduced-form estimates in any case.

What the body does support, stated as directions rather than a magnitude:

- **The reduced-form association exists in aggregate data and is well documented.** Pampel (1993) across 18 countries, 1951–1986; Macunovich across US series repeatedly; Jeon and Shields for the US, 1913–2001.
- **It is institutionally moderated.** Pampel's country-specific effects run from **+3.10\*\*\*** (Canada) to **−0.813\*\*** (Denmark), and the interaction with social security spending is significant (+0.019\*\*, +0.018\*, +0.010\*). The effect is not a constant of nature.
- **It weakens or disappears in later data and under stronger specifications.** Norberg (2015) finds the headline **−0.563\*\*** collapsing to **−0.005 (SE 0.009)** once country × cohort interactions are added. Xiao and Shields (2014) find it "holds but the effect is weak" in Latin America. Hirosima (2000) concludes the effect "did not exist" in Japan's decline, attributing onset to a period shock. Jeon and Shields note the predicted recovery "is much smaller than earlier studies predicted."
- **The cycling claim specifically is not supported.** Wachter (1991) asks whether feedback models capable of generating the cycles are dynamically possible, comparing estimated response strengths against the threshold needed to sustain oscillations of non-zero amplitude. The title states the finding: the cycles are elusive.
- **A rival explains the same phenomenon without the mechanism.** Jones and Schoonbroodt (2016) generate boom and bust endogenously from Depression-era income shocks in a dynastic model with no aspiration mechanism at all, calibrating a 1–1.7% TFR response per 1% productivity deviation.

---

## 8. Demographic significance

**The phenomenon to be explained is measured in births per woman lost across a transition; this mechanism offers an oscillation in the ratio of young to prime-age adults that returns to within a fraction of its own amplitude of where it began.**

That sentence, written before the literature was read, anticipated most of what follows. A driver that ends a window where it started has nothing left over to explain a permanent level shift. The question is then entirely about *sub-windows*: does the exposure move the right way across the parts of the transition where the fertility fall actually happened?

That question is answered from data rather than from the literature. `source/build/306_c6a_cohort_size_series.py` pulls World Bank age structure and fertility for 18 countries, 1960–2024, and derives relative cohort size as population aged 20–29 over population aged 30–64. **The hypothesis requires d(TFR)/d(RCS) < 0, so to explain a fall it needs relative cohort size to have risen.**

| window | countries moving as the mechanism requires |
|---|---|
| 1965–1980 | **14 of 18** |
| 1980–present | **0 of 18** |
| full SDT window | **0 of 18** |

And the decline is not evenly distributed across those windows. The median country took **75%** of its total 1965-to-present fertility fall during **1965–1980** — the sub-window where the mechanism works. In 15 of 18 countries more than half the fall occurred there.

### 8.1 Pre-modern

**For pre-modern variation, the verdict is NOT ASSESSED, because the mechanism requires a labour market with cohort-varying entry wages and a measurable parental consumption standard, and no included study addresses a pre-modern population.**

The search did not exclude pre-modern settings; the cell is empty because the literature is. One record touches it (population cycles at Penrith, 1557–1812) and was routed to the theory stream.

### 8.2 First Demographic Transition

**For the FDT, the verdict is NOT ASSESSED, because the mechanism's own best case is a fertility *rise* — the post-war baby boom — and the FDT denominator is a *fall*, so numerator and denominator do not share a sign, let alone units.**

This is the ruling frozen at scope §6, and it is uncomfortable by design. PROTOCOL §2 classifies a study window by replacement status, and US boom-era windows sit above 2.1 throughout, so the rule returns FDT-like for exactly the evidence the hypothesis is proudest of. **The review has no category for a fertility increase.** This chapter reports the boom-era body under the FDT|SDT hinge with an explicit direction flag and refers the classification question to the PI (§11, PI Call 1).

### 8.3 Second Demographic Transition

**For the SDT, the verdict is MINOR, because relative cohort size moved as the mechanism requires across the sub-window carrying a median 75% of the decline, but the mechanism's distinctive prediction — a fertility recovery once the small post-bust cohorts came of age — failed in 18 of 18 countries, and no elasticity survives the best-identified study's fixed-effects test to convert direction into a share.**

The arithmetic, with every term named:

- **Numerator:** not computable. Route A (decomposition share) requires a transportable d(TFR)/d(RCS), and Hill (2014) shows the sign itself is specification-dependent. No share is reported, and none should be.
- **Route B, slope sufficiency: PARTIAL.** Direction is correct for 1965–1980 in 14 of 18 countries and incorrect thereafter in 18 of 18. Denominator: the fall in TFR from 1965 to 2024, median −1.06 births per woman across the 18 countries, source World Bank `SP.DYN.TFRT.IN`, window 1965–2024.
- **Route C, R² benchmarks: reported but not used to band.** Within-country R² of TFR on relative cohort size, 1965–2024, exceeds 0.15 in 6 of 18 countries — and **all 6 do so with the correlation running against the hypothesis** (Japan R² = 0.71 at r = +0.84). In the 1965–80 sub-window the correctly signed correlations are very strong (US r = −0.98), but two monotone series over fifteen annual observations will correlate at that level whatever the mechanism, so this is not evidence and is not banded.

**MINOR rather than SUBSTANTIAL** because the direction result is shared with any co-trending series and the mechanism's one distinctive, falsifiable prediction failed everywhere. **MINOR rather than NEGLIGIBLE** because NEGLIGIBLE asserts a computed share below 5%, and no share was computed.

---

## 9. GRADE

| phenomenon | rating | downgrades named |
|---|---|---|
| Pre-modern | **No evidence** | Cell empty. To earn a rating there would have to exist at least one study relating cohort structure to fertility in a pre-1870 population with a measurable parental living standard. |
| FDT | **No evidence** for the FDT as a decline | The boom-era body is real but answers a different question (a rise), which is indirectness so complete that it is not a downgrade but a different cell. |
| SDT | **VERY LOW** | Starting point LOW (observational). −1 **inconsistency**: country-specific effects include significant positives and significant negatives (Pampel), and the best-identified study's sign flips with fixed effects (Hill). −1 **risk of bias**: aggregate time series dominate, and the exposure is mechanically a lagged function of the outcome. Not further downgraded for imprecision (the aggregate estimates are precise) or publication bias (not assessable at this retrieval fraction). |

The SDT rating is about **causal credibility**, not about size. A VERY LOW rating beside a MINOR significance verdict is coherent: the body is consistent with a real contribution to the early SDT decline and cannot establish one.

---

## 10. Verdict

Easterlin's hypothesis explains the period it was built to explain and fails on the period that followed.

The mechanism says that a large generation, crowded in the labour market and unable to match the standard it was raised in, will have fewer children — and that the small generation which follows will have more, so that family size swings rather than falls. The first half of that prediction fits: relative cohort size rose and fertility fell across 1965–1980 in 14 of 18 rich countries, and the median country took **75%** of its entire post-1965 fertility decline in exactly that window. The second half does not fit anywhere. As the small post-bust cohorts reached adulthood after 1980, the mechanism required fertility to recover. **In 0 of 18 countries did it recover.** Fertility kept falling, and relative cohort size fell with it — the wrong direction for the mechanism, in every country, for forty years.

**The number to carry away is 0 of 18.** It is the failure of the mechanism's own distinctive prediction, and it is what separates this hypothesis from a general claim that young people's economic prospects matter.

Two further findings sharpen this. The only study that measured what the hypothesis says matters — incomes observed across two generations — found no support and concluded a rival account fitted better. And the most carefully identified study in the body finds the sign of the effect depends on which fixed effects are included, which means the literature has not established a parameter that could be carried anywhere.

No study in this body uses an exogenous shock to cohort size. The hypothesis has been tested for sixty years almost entirely on the correlation between a country's age structure and its birth rate — two series in which one is arithmetically built from the other's past. That gap, not the sign of any coefficient, is the reason the causal rating is VERY LOW.

---

## 11. Open questions

**PI Call 1 — protocol-level.** PROTOCOL §2's replacement-status rule classifies a fertility *rise* as FDT-like, because it keys on TFR level rather than direction. C.6.a is the first hypothesis in the review whose central evidence is an increase, and C.2.d and D.1.d will follow. Should the review carry a fourth classification for recoveries and booms, or report such windows inside the adjacent phenomenon with a direction flag? This chapter takes the second course.

**PI Call 2 — registry edit, flagged not made.** HYPOTHESES-v5 gives C.6.a `cross-ref: --`. On the walls actually needed it should read C.1.a, C.5.a, C.7.a, A.9 and C.2.e.

**PI Call 3 — protocol-level, and it outlives this chapter.** PROTOCOL §4.2's third demsig route is "conditional R² ≥ 0.15", and **R² is sign-blind**. Six of 18 countries clear that threshold here and all six do so with the correlation running *against* the hypothesis. Read literally, the criterion would certify C.6.a as demographically significant on the strength of evidence refuting it. This chapter attached a sign condition locally; §4.2 should carry one generally.

**Retrieval priorities.** The chapter is at 22%. In order: (i) *Subjective relative affluence and expected family size* (1985) — the last unretrieved `BENCHMARK_MEASURED` record, no DOI, needs ILL; (ii) **OCR for the six retrieved-but-unreadable scans**, above all Macunovich (2000), the strongest pro-hypothesis global claim, currently unread; (iii) the full NBER volume of Easterlin (1962) — the open file contains only the foreword, so the founding statement is unread; (iv) the remaining 37 `CYCLE_TEST` records, since that cell carries the distinctive claim on 9 of 46.

**Studies that do not exist and should.** No study exploits an exogenous shock to cohort size to estimate a fertility response. The designs are available and enumerated in §5.2 — Romania's Decree 770 cohorts reaching the labour market, and immigration waves that change entry-cohort size without changing anyone's birth cohort. The second is the cleanest instrument in demography that nobody appears to have used for this question.

---

## 12. References

Full bibliographic detail in `extraction/easterlin-relative-income.csv` (34 records with OpenAlex ids and DOIs) and `literature/search-logs/easterlin-relative-income-cold-start-anchors.json` (31 resolved anchors).

Principal works relied on: Behrman & Taubman (1989, *Demography*); Butz & Ward (1979, *AER* 69(3):318–328); Comolli (2021, *Advances in Life Course Research*); Diebolt & Doliger (2005); Elder (1981, *Journal of Family History*); Hill (2014); Hirosima (2000); Jeon & Shields (2005, *J Popul Econ*; 2008, IZA DP 3587); Jones & Schoonbroodt (2016, NBER WP 16596); Lee (1974, *Demography*); Macunovich (1993; 1996, *PDR*; 2011, IZA DP 5885); Mavropoulos & Panagiotidis (2022); Norberg (2015); Pampel (1993, *ASR* 58(4):496–514); Suzuki (2019); Wachter (1991, *Population Studies* 45(1):109–135); Xiao & Shields (2014).

---

## Provenance and standing caveats

**This chapter is written on 34 of 156 wanted full texts (22%).**

**The findings that would survive full retrieval are the 0-of-18 failure of the post-1980 recovery, the absence of any design using exogenous variation in cohort size, and the sign-robustness failure in the best-identified study; the findings that might not are the characterisation of the `BENCHMARK_MEASURED` cell as internally contested, which rests on three studies, and the claim that no stratum reaches three poolable effects, which is a property of a 22% sample as much as of the literature.**

**Six retrieved records could not be read at all** — scans with no text layer — and are recorded with `NOT EXTRACTED` in every field rather than as absences: Macunovich (2000), *Countercyclical Fertility in Canada* (1991), Grossbard-Shechtman & Granger (1998), *The Origins of the Fertility Transition in Rural Japan* (1981), *Relative and Potential Income and Fertility* (1982), and the Latvian trajectory analysis (2024). Macunovich (2000) is the most consequential: it is the strongest global statement of the hypothesis and this chapter has not read it.

**Numbers taken from OCR'd scans rather than clean text** are flagged in the extraction table and require RA verification beyond the protocol's random 10%. One is actively suspect: **Macunovich (1996)'s main relative-income coefficient reads −0.65 (t = 6.2) in the extracted table while the paper argues relative income raises fertility.** That magnitude is marked unusable pending a human read and is not used anywhere above.

**No number in §8 comes from the literature.** The sign test, the window shares and the R² benchmarks are computed from World Bank series by `source/build/306_c6a_cohort_size_series.py` and are reproducible independently of any retrieval decision.

**GRADE was rated by one rater.** PROTOCOL requires three. Stage 11 is therefore partial.

**No objection was recorded against writing this chapter at 22% retrieval.** The gate set at the retrieval stage was that extraction should not begin until the `BENCHMARK_MEASURED` cell was resolved; it stands at 4 of 5, with the fifth requiring ILL, and the chapter was written on that basis at Shravan's instruction.
