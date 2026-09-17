# Chapter: Reduction in Stigma Around Contraception and Abortion

**Category:** Proximate (HYPOTHESES-v5.md §A.6)
**Primary mechanism:** A fall in the social cost of being known to control fertility lets couples who already want fewer children act on that want, so births fall without any change in desired family size.
**Cross-references:** A.2 (contraceptive technology) · A.3 (diffusion of fertility control) · A.4 (abortion access) · A.5 (family-planning programmes) · D.1.a (postmaterialism and secularisation) · D.2.b (marriage and family norms) · B.5 (fetal loss, clinical homonym)
**Status:** Draft, TICK-087, 2026-09-17. **Not PI-reviewed. §9 GRADE is provisional on one rater of the three PROTOCOL §5.1 requires.** Eight PI calls were put and answered during scoping; one further question, raised by the single admissible study, is open (§11). Written on 24 of 39 wanted full texts (62%).

---

## 1. The claim

**This chapter explores the effect of the social cost of being known to control fertility on realized fertility.**

### 1.1 In plain terms

**In plain terms: when people stop being judged for using birth control, the ones who already wanted fewer children can finally have fewer children.**

The idea is that there are two different reasons a couple might have a big family. The first is that they want one. The second is that they want a small one but cannot safely act on it — because the pharmacist knows their mother, because a husband would take offence, because the village would talk. The second couple has what demographers call *unmet need*: they want to stop having children and are not doing the thing that would stop it.

If that is what is happening, then nothing has to change about what people want for fertility to fall. What has to change is what it costs them socially to act. Take away the disapproval and the births that were never wanted stop happening. That is the whole claim, and it is why the hypothesis is interesting: it says fertility can fall without anybody's preferences changing at all.

The rival explanations say the opposite in different ways. One says the method had to get cheaper or better (the pill arrives). One says the law had to change (abortion is legalised). One says a clinic had to open (a programme arrives). One says people simply came to want fewer children (values shifted). This chapter is about none of those. It is about the case where the method exists, the law permits it, the clinic is open, the couple already wants to stop — and they still do not, because of what other people would think.

### 1.2 The technical statement

**The parameter this chapter estimates is the change in realized fertility caused by an exogenous fall in the social cost of using fertility control, measured in births per woman.**

The estimand holds four things fixed, each corresponding to a neighbouring hypothesis: contraceptive technology and its price (A.2), the legal status of abortion (A.4), programme supply and information (A.5), and the content of the underlying value system (D.1.a). What varies is the *social* price of use, not the market price, the legal price, the access price, or the desire.

Two rulings, frozen before the literature was read, decide what counts.

**Ruling 1 — the exposure is the social price of use, not the availability of the method.** The arrival of the pill in a country both lowered its price and changed what using it meant. A study identifying the technology shock is A.2's even if it reports an attitude change as a mediator; a study identifying a norm shock with method availability unchanged is A.6's.

**Ruling 2 — the outcome is realized fertility, and contraceptive use is a link, not a substitute.** This is the ruling that decides whether the chapter exists, and §4 shows what it costs. A.6's mechanism runs *through* use, so the literature overwhelmingly takes use as its dependent variable. Accepting use as the parameter would silently import Bongaarts' use-to-fertility conversion — which belongs to A.2 and A.13 and carries its own contested parameters — and report it as A.6's effect.

One extension was ruled in during scoping and matters throughout. The registry's object is "contraception and abortion", but the PI ruled that norms about **premarital sex and out-of-wedlock childbearing** also fall inside A.6's exposure, with contraception as the response to them rather than the thing disapproved of. That ruling is load-bearing: it is the reason the chapter's only admissible study is admissible.

## 2. Theoretical mechanism

In the household's problem, stigma is a shadow price. A couple choosing whether to use a method compares the benefit of avoiding a birth against the full cost of use — the money price, the effort, the health cost, and a social cost that is paid only if the use becomes known. Destigmatisation lowers that last term. Demand for control rises, and births fall, at unchanged desired family size and unchanged method price.

**The margin.** The treatment is *intensive* — a level change in the social cost of use, not its
presence or absence. The behavioural response is *extensive* — a couple uses a method or does not.
The outcome is *intensive* again: a level of births per woman. The chapter's parameter therefore
compounds an intensive treatment with an extensive response, which is why a dose unit (§5.1) is
required rather than a treated/untreated contrast, and why studies reporting only "stigma present
versus absent" cannot populate it.

**The identity and the behaviour are separable here, and the separation is the whole empirical problem.** The identity is Bongaarts': births are a function of exposure, contraceptive use and effectiveness, and fetal loss. Stigma enters nowhere in that identity. It enters only through the *behavioural* equation that determines use. So A.6 is a claim about one input to an accounting identity owned by other chapters, and its effect on births is the product of two links: stigma to use, and use to births. This chapter owns the first link's effect on the final outcome. It does not own, and must not re-estimate, the second.

**What would make the hypothesis wrong.** Three observable behaviours would falsify it, and one of them turns out to be documented.

1. *Latent demand does not exist.* If couples reporting unmet need do not in fact want to stop — if the survey item measures ambivalence rather than suppressed demand — then removing stigma releases nothing. The Casterline and Bongaarts literature on the meaning of unmet need is the live version of this objection.
2. *Stigma binds on the wrong margin.* If disapproval falls on *fertility control* but the binding constraint is access or partner consent, destigmatisation moves nothing.
3. *The sign is not signed.* This is the documented one. Stigma attaches to at least two different objects, and they push in opposite directions. Stigma of *contraception* lowers use and raises births. Stigma of *premarital sex* can **raise** contraceptive use, because a woman having sex she would be judged for has a reason to avoid the pregnancy that would reveal it. McLoughlin Brooks and Weitzman (2022) name this the "contraceptive work-around" and find it in a weekly panel. A study that does not separate the two objects can recover either sign, and pooling across them averages a positive and a negative effect of two different constructs. This is why `stigma_object` is a required tag and why the synthesis never pools across it.

## 3. Search strategy

Reproducible from `source/build/goldset/404`–`425` with logs in `literature/search-logs/`. The frame frozen at scoping was **withdrawn** before production, and the reason is worth stating because it generalises.

**The withdrawn frame.** Scoping selected this hypothesis on a frame of 668 records — stigma vocabulary AND a contraception object AND a fertility outcome. That frame reaches **0 of 15** resolved canonical anchors. It is not a narrow frame; it is the wrong instrument. Diagnosis: A.6's construct spans two literatures that do not share vocabulary. The **demographic** canon (Cleland and Wilson 1987; Bongaarts and Watkins 1996; Bongaarts and Bruce 1995; Casterline 2000; Sedgh 2014) satisfies the object and outcome blocks and fails the stigma block — it says *unmet need*, *reasons for non-use*, *opposition*. The **stigma** canon (Kumar 2009; Norris 2011; Cockrill 2013; Link and Phelan 2001) satisfies the stigma block and fails the outcome block — it never mentions fertility. Their vocabulary intersection is 20 records, and 14 of 15 anchors have abstracts, so this is not an indexing artefact.

**Three arms, pulled separately and deduplicated by id**, since an AND-containing arm cannot be OR'd into a union:

| arm | definition | records |
|---|---|---|
| A | compound-stigma phrases × contraception object | 472 |
| B | opposition and unmet-need vocabulary × contraception object | 6,549 |
| A ∪ B (inclusion–exclusion, A∩B = 20) | | 7,001 |
| C | stigma vocabulary × **behaviour** object (premarital sex, out-of-wedlock) | 1,222 |

**The fertility-outcome restriction was moved from retrieval to screening.** Requiring a fertility word at retrieval costs ARM B two of nine reachable demographic anchors and ARM A four of six. Ruling 2 is instead enforced at the screen through the `outcome_level` tag. Keeping it in the query deleted the literature before a human saw it.

**Citation snowball is the primary channel, not the supplement.** Six anchors are unreachable by any arm of any spelling — including Cleland and Wilson 1987, Bongaarts and Watkins 1996 and Lesthaeghe 1983, which are also unreachable by A.3's own block, because they are broad theoretical papers whose abstracts carry no operational vocabulary. Round-1 snowball from 15 resolved anchors yielded 2,815 candidates. **Recall is 9 of 15 and that is the reported ceiling**, not a number to be improved by adding terms: the six misses fail for reasons term choice cannot fix. Both of the chapter's best-designed link records — Ragan 2012 and McLoughlin Brooks and Weitzman 2022 — arrived by citation and are reachable by no arm at all.

**Walls, measured from both sides** (overlap; share of our frame; share of theirs):

| wall | rule — separated by *what varies* | overlap | ours | theirs |
|---|---|---|---|---|
| A.2 | market price and availability vs **social price of use** | 60 | 9.0% | 1.1% |
| A.3 | whether the idea has **arrived** vs whether it is **acceptable** | 2 | 0.3% | 0.4% |
| A.4 | what the **law permits** vs what the community **tolerates** | 57 | 8.5% | 2.7% |
| A.5 | supply, information, subsidy vs **social cost of use** | 81 | 12.1% | 1.4% |
| D.1.a | what people **value** vs what they can be **seen doing** | 6 | 0.9% | 0.4% |
| B.5 | spontaneous pregnancy loss — clinical homonym | 51 | 7.6% | 0.3% |

**A.5 was declared a bundle rather than a wall, in advance.** Family-planning programmes routinely include destigmatisation as a designed component, so programme studies were admitted pending inspection rather than routed out — Yeatman and Sennott (2024) make the same acceptability-versus-accessibility distinction independently. §4 reports what the inspection found.

**The small overlaps are not reassurance.** A.6 and A.3 share **two of A.6's four registered seminals** while overlapping on two records of vocabulary: the vocabularies part and the construct does not. All `MIXED_*` routings were adjudicated at full text on the mechanism, never on the title. Homonym contamination inside the frozen frame was substantial and is routed to its own cells: HIV and sexual-health stigma 148 records (22%), mental-illness stigma 92 (14%).

**Two boundary rulings were made against neighbours and both are consequential.** Norms about premarital sex and out-of-wedlock childbearing are **inside** A.6 (no `MIXED_NORM_MARRIAGE` cell, no D.2.b wall). And a nonmarital-birth **ratio** is not an admissible outcome while a nonmarital-birth **rate** is — see §5.1.

## 4. PRISMA flow

| stage | n | note |
|---|---|---|
| Frozen frame (withdrawn) | 668 | reached 0 of 15 anchors |
| Anchors resolved | 15 of 20 | author-and-year verified |
| Snowball round 1 | 2,815 | forward citations object-filtered, removing 77% overall and 99% of Link and Phelan's 8,624 |
| ARM C, new after dedup | 1,214 | |
| Screened | **166** | all four exhaustive strata plus ARM C's |
| Full texts wanted | 39 | |
| Full texts read | **24 (62%)** | 2 open-access, 9 by proxy, 2 only after OCR |
| `PRIMARY_NORM_FERTILITY` | **1** | |
| `LINK_NORM_USE` | 28 | |

**Three features of this funnel change how the chapter should be read.**

*First, the identified-design share is 1.8%.* Twelve of 668 frame records carry an identified-design marker against 189 carrying qualitative markers. This frame retrieves a measurement and advocacy tradition — stigma scales, service-delivery studies, qualitative accounts of provider attitudes — not an identification literature.

*Second, the registered outcome is nearly absent.* Fifty-eight in-frame records carry realized-fertility vocabulary. Meanwhile 479 records of stigma-and-object take **contraceptive use** as the dependent variable, of which 357 — 74.5% — are invisible to any fertility-framed search. A.6's mechanism runs through use, so a fertility-framed search retrieves the minority of its own literature.

*Third, the citation structure agrees with the vocabulary.* Only **8** of 2,815 snowball candidates cite both canons, and they are a textbook, the ICPD Programme of Action, two conceptual frameworks, three qualitative studies and one scale-validation paper. Zero identified designs, zero fertility outcomes. The two literatures barely speak to each other even by citation.

*And the A.5 bundle closed at its strongest record.* Twelve of 25 programme studies were read; none separately doses a norm component alongside a fertility outcome. The decisive one is Matlab (Phillips, Hossain and Arends-Kuenning 1996) — the canonical community-based family-planning quasi-experiment with a demographic outcome, and the one design that could plausibly have dosed a norm apart from the programme. Norm vocabulary appears 9 times in 12,390 words, and its only substantive occurrence narrates "the role of outreach in fostering new ideas, norms, and behaviour" as a mechanism, never as a variable.

## 5. The ideal design

### 5.1 The ideal estimand

A population in which contraceptive methods are available at unchanged price, abortion law is unchanged, no programme enters or exits, and desired family size is measured and stable. Into it arrives an exogenous shock to the social cost of *using* fertility control — a religious authority's ruling, a media campaign changing perceived approval, a cohort discontinuity in reported acceptability — that does not also change access, law, supply or desires. The estimand is the resulting change in completed cohort fertility, in births per woman, with the dose measured as a percentage-point change in the share of non-users citing opposition or religious prohibition as their main reason for non-use.

**Why the dose unit is that and not a stigma scale.** Stigma scales are study-specific, so a pooled standardised effect averages instruments measuring different constructs. The opposition item is a repeated, cross-nationally harmonised DHS series available across roughly ninety countries from the mid-1980s. It is the only candidate that is both a measure of social cost and available as a time series.

**A nonmarital-birth ratio is not an admissible outcome; a nonmarital-birth rate is.** A ratio (nonmarital births ÷ all births) is a composition: it can move with fertility unchanged, and cannot be recovered as a level without the total-birth denominator and the female population. A rate (nonmarital births per 1,000 unmarried women) is a genuine fertility rate for a subpopulation and enters the general fertility rate additively, weighted by the unmarried share. This distinction admits exactly one study into §6 and excludes several near-misses.

### 5.2 The design that would identify it

A difference-in-differences or event study on a norm shock with a credible comparison population, with access, law, supply and desired family size all measured and shown flat; completed cohort fertility as the outcome; and the dose reported in the §5.1 unit so the elasticity is transportable. Reverse causation must be addressed head-on rather than controlled for, because it is structural here: falling fertility *normalises* fertility control, so stigma and fertility are mutually determined over exactly the period of interest. A design without an exogenous norm shock is not weakly identified; it is unidentified.

### 5.3 Distance from the ideal

| study | cell | design | outcome | dose in §5.1 unit | distance from ideal |
|---|---|---|---|---|---|
| Kelly and Cutright 1983 | **primary** | multivariate regression on annual change, 1911–74 | age-specific illegitimacy rates per 1,000 unmarried women | derivable, not reported | **Far.** No exogenous shock; a national time series with no comparison population; reverse causation unaddressed; the norm measured is pressure to marry, not pressure not to control fertility |
| Wolff et al. 2000 | link | cross-sectional, couples matched | unmet need and method mix | **reported** (15% of unmet need attributable) | Far on outcome — no fertility outcome, which the authors say themselves would need a prospective study |
| McLoughlin Brooks and Weitzman 2022 | link | weekly panel, 39,806 person-weeks, mediation | weekly intercourse, hormonal use, condom use | derivable | Closest design in the chapter; wrong outcome |
| Ragan 2012 | link | community panel with fixed effects | Pill demand per woman 16–40 | not reported | Wrong outcome; exposure is historical out-of-wedlock norms |
| Rajan 2014 | link | multilevel logit, three NFHS waves | contraceptive use (spacing, stopping) | not reported | Wrong outcome; exposure is community norms |

**No study in this literature is close to the ideal design.** The best-identified are on the wrong outcome; the one on a convertible outcome is far on identification.

## 6. Included studies

**One study is admissible to the primary cell.**

| study | design | exposure | outcome | result |
|---|---|---|---|---|
| Kelly, W. R. and Cutright, P. (1983), *Sociological Focus* 16(2) | multivariate regression on annual change, Sweden 1911–1974, by five-year age group | a measure of **normative pressure to legitimate by marriage** births conceived out of wedlock, dosed separately from sexual activity, birth-control practice and women's status | **age-specific illegitimacy rates per 1,000 unmarried women** | the legitimation measure is significant for all age groups except teenagers; R² for annual change 34% (teens) to 66% (ages 20–24 and 25–29) |

**Twenty-eight studies are admissible as link evidence** (`LINK_NORM_USE`): the effect of a normative exposure on contraceptive or abortion use, which is A.6's first link and not A.6's parameter. The strongest four are in §5.3. Sixty-five are context (`CONTEXT_STIGMA_MEASURE`) — the stigma-measurement canon, two conceptual frameworks, and two theory papers whose mechanism is exactly A.6's (Prettner and Strulik 2017; Fernández-Villaverde, Greenwood and Guner 2010).

### Estimator disagreement

**The naive estimator, and which way it is wrong.** The naive approach is a cross-sectional
regression of fertility on reported stigma or reported opposition. Its bias direction is knowable
and is *upward in magnitude*: falling fertility normalises fertility control, so low-fertility
populations report less stigma for reasons that have nothing to do with stigma causing the low
fertility, and the two are mutually determined over exactly the period of interest. Twenty-four of
the 28 link records are of this form. The chapter therefore does not average them against the one
quasi-temporal estimate; it reports them separately as a link and says the naive estimate is an
upper bound on magnitude.

There is no estimator disagreement to analyse in the primary cell, because there is one estimate. That absence is itself the finding, and it has a specific shape worth stating: **the chapter failed to find a study with A.6's exposure and A.6's outcome from both directions.** Records with the right exposure (Wolff; McLoughlin Brooks and Weitzman; Ragan; Rajan) have a use outcome. Records with the right outcome (Yüceşahin and Özgür 2008 on provincial Turkish TFR; Kramer et al. 2021 on Maya fertility across 90 years) have no normative exposure at all — Yüceşahin's regressors are illiteracy, ethnicity shares, female employment, child mortality and GDP; Kramer's exposure is family-planning adoption, with "norms" appearing only in discussion. Two independent near-misses, failing on opposite sides of the same conjunction.

## 7. Quantitative synthesis

### 7.1 The answer in plain terms

**One study, from Sweden, covering 1911 to 1974, measures something close to what this chapter is about and finds it matters.** It is a study of births to unmarried women, and what it measures is how much pressure there was to marry when an unmarried woman got pregnant. Where that pressure was strong, fewer births were recorded as happening outside marriage. That effect is statistically solid and it holds for every age group except teenagers.

But there are two problems with reading it as an answer to this chapter's question. The first is that pressure-to-marry is not quite the same thing as being judged for using birth control — it is a push toward a wedding, not a push away from contraception. The second is more serious: if a couple marries because of that pressure, the baby still arrives. It is simply counted as a marital birth rather than a nonmarital one. So the study may be measuring a change in the *label* on a birth rather than in whether the birth happens — and this chapter is about whether it happens.

Everything else that has been found measures whether people *use* birth control, not whether they end up with fewer children. That is a real finding about a real link in the chain, and there are twenty-eight studies of it. But it is not the same number, and converting one to the other would require multiplying by a parameter this chapter does not own.

### 7.2 The estimate

**No pooled estimate is reported, and the pooling rule pre-registered that outcome.** The rule stratifies before counting poolable effects and requires three per stratum: `PRIMARY × FDT` has one, `PRIMARY × SDT` has none. The prediction written down before screening was that both would contain fewer than three and that stratum 1 would most likely be empty; the first held and the second was wrong by one record.

The single primary estimate is reported as found and not converted. Kelly and Cutright's legitimation coefficient is significant at all ages except teenagers, with annual-change R² between 34% and 66%. It is **not** transformed into births per woman, for two reasons. The transformation requires the unmarried share by age by year, which the paper does not report; and, more fundamentally, the exposure's interpretation is contested (§11, open question 1), so a converted number would carry a spurious precision about a quantity whose meaning is unsettled.

`LINK_NORM_USE` is poolable in principle at 28 records but is **not pooled**, on two grounds. Pooling across `stigma_object` would average a positive and a negative effect of two different constructs (§2). And the stratum's effects are not commensurable: Wolff reports a share-of-unmet-need attributable to partner opposition, Ragan a coefficient on Pill demand per woman, McLoughlin Brooks and Weitzman weekly odds ratios on three separate behaviours. A narrative synthesis of the link is the honest form, and the link's headline number is Wolff's: partner opposition accounts for roughly **15%** of unmet need overall in Uganda — 20% urban, 12% rural. **This is a study-window share of *unmet need*, not of a fertility change**: numerator, unmet need attributable to partner opposition; denominator, total reported unmet need in the 1995–96 Uganda NRO sample. It is not convertible into a share of any fertility decline and is deliberately not banded against one, per `PROTOCOL.md` §4.2.1 — the denominator there must be a *change* over the phenomenon's full window, and no such denominator exists for this quantity.

## 8. Demographic significance

**The phenomenon to be explained is measured in whole children; this mechanism offers regression coefficients on a rate that applies only to the unmarried minority of women, denominated in births per 1,000 unmarried women.**

That sentence does most of the work, and it was written before the estimate existed. The First Demographic Transition is a fall of roughly three children per woman. The only admissible estimate is a coefficient on nonmarital births per unmarried woman in one country, over a period when nonmarital births were a small share of all Swedish births. Even taken at face value and even granting the contested interpretation, the mechanism is denominated in a quantity that cannot add up to the phenomenon. No study could have changed that, which is why the sentence comes before the arithmetic.

### 8.0 The attrition ledger

A.6's mechanism is stated as an effect on a rate, so the attrition between the event that is
*counted* and the quantity that is *demographically relevant* is enumerated before any arithmetic.

| stage | question | A.6 | sign |
|---|---|---|---|
| reported → experienced stigma | is the measured exposure the real one? | stigma is self-reported by the treated; a woman who has internalised destigmatisation reports less of it *and* uses contraception | **overstates** |
| stigma → use | the behavioural link this chapter owns | attenuated by everything else that binds — access, partner consent, ambivalence | overstates |
| use → averted conception | is a user a non-conceiver? | method effectiveness and imperfect use; A.2's parameter, not A.6's | overstates |
| averted conception → averted birth | is an averted conception an averted birth? | abortion substitution (A.4) and fetal loss (B.5) sit between them | indeterminate |
| counted nonmarital birth → birth occurred | is the counted unit the demographic unit? | legitimation by marriage moves a birth between categories without preventing it | **overstates** |
| realised → registered | is the measured rate the underlying rate? | historical under-registration of illegitimate births | understates |

**The entries do not all run the same way**, so there is no single known direction to report in the
verdict — unlike A.12, where four same-signed entries let the chapter state a bias direction. Here
four entries overstate, one understates and one is indeterminate. The fifth row is the one that
matters most, because it is not a bias on the estimate but a question about what the estimate is
(§11, open question 1).

### 8.1 Pre-modern

**For pre-modern variation, the verdict is NOT ASSESSED, because the phenomenon is not registered for this hypothesis and is excluded by the claim rather than by convenience** — A.6 concerns control within unions, while the pre-modern reading of premarital-sex and illegitimacy norms belongs to D.2.b and A.7.

### 8.2 First Demographic Transition

**For the FDT, the verdict is NOT ASSESSED, because the single admissible estimate is denominated in a subpopulation rate whose conversion to a fertility level is contested, and no dose series exists before the mid-1980s to run a counterfactual.**

The three routes fail in specific, nameable ways. **R1 (sign)** is the only one satisfied: there is one signed, significant estimate. **R2 (elasticity)** fails because the estimate is not reported in the §5.1 dose unit and cannot be converted without the unmarried share by age by year. **R3 (counterfactual)** fails outright and by construction: the DHS opposition series begins in the mid-1980s, two decades after Kelly and Cutright's window closes, so the historical phenomenon has no dose series at all.

This is not "weak evidence". It is a route failure, and naming which route failed is the point of reporting it this way.

### 8.3 Second Demographic Transition

**For the SDT, the verdict is NOT ASSESSED, because no record in 166 screened has both A.6's exposure and a fertility outcome in the SDT window, and the dose series exists only where the phenomenon does not.**

The second clause is the durable problem and it is worth stating plainly, because it will recur for any norm hypothesis. The DHS opposition item — the only harmonised dose series for this construct — runs in low- and middle-income countries, which are mostly still completing their first transition. The OECD, where the SDT fertility decline of interest happened, has no such series. **The dose is measured where the phenomenon is not.** The two worlds must not be pooled, and neither can carry the verdict alone.

## 9. GRADE rating

Rated per phenomenon against `PROTOCOL.md` §4.1, which fixes the bands by design class. **The
starting level is read off the design, not assumed**, and that matters here: §4.1's **Low** band is
defined as "cross-sectional or panel with controls, no clear identification". The absence of an
identification strategy is therefore *already priced into the starting level*, and downgrading again
for "no exogenous shock" would double-count it. Only defects beyond that are taken.

### 9.1 First Demographic Transition — the only cell with evidence

Body of evidence: one study (Kelly and Cutright 1983), a multivariate regression on annual change in
a national time series with controls and no identification strategy.

**Starting level: Low.** It is a panel/time-series with controls and no clear identification, which
is §4.1's Low band verbatim. It is not Moderate: there is no IV, DiD, RD or event study, and no
second setting. It is not yet Very low: the mechanism is not speculative and the estimate is not
merely correlational — the legitimation measure is dosed separately from three named alternatives
and enters a multivariate specification.

| domain | assessment | downgrade |
|---|---|---|
| **Risk of bias (body as a whole)** | Structural, bidirectional reverse causation over exactly the estimation window: falling fertility normalises fertility control, so the exposure is partly an outcome. This is **beyond** the generic non-identification already priced into Low, because the direction of confounding is known and runs both ways rather than being merely unaddressed. | **−1** |
| **Indirectness** | The exposure is pressure to *legitimate by marriage*, not the social cost of controlling fertility; the outcome may be a recomposition of births between marital and nonmarital rather than a change in their number. On both sides the evidence answers a neighbouring question — D.2.b's — rather than A.6's. | **−1** |
| **Imprecision** | The estimate is significant at all ages but is not reported in §5.1's dose unit and cannot be converted without the age-specific unmarried share. Precision *in the chapter's units* is therefore unknown rather than wide. Recorded, **not** taken as a separate downgrade, because the floor is already reached and stacking a third downgrade would imply a distinction the band structure cannot express. | 0 (noted) |
| **Inconsistency** | **Unassessable.** One study; no replication exists to be consistent or inconsistent with. Not a downgrade, and not silently omitted either — a single-study body cannot earn or lose on this domain. | n/a |
| **Publication bias** | **Unassessable, and probably the wrong frame.** With n = 1 no funnel or selection test is possible. More importantly the chapter's pattern — 1.8% identified-design share, 8 of 2,815 citation bridges, no study pairing A.6's exposure with A.6's outcome from either direction — is an absence of *research*, not suppression of *results*. Naming it publication bias would misattribute a gap in a research agenda to a gap in a publication record. | n/a |

**Low − 2, floored at the bottom band: VERY LOW.**

### 9.2 Pre-modern and Second Demographic Transition — empty cells

| phenomenon | rating | what would have to exist to earn a rating |
|---|---|---|
| PM | **No evidence** | A pre-modern population with measured variation in the social cost of fertility control *within unions* and a fertility outcome. The registry does not open PM for A.6 and the claim excludes it: pre-modern illegitimacy and premarital-sex norms are D.2.b's and A.7's. |
| SDT | **No evidence** | One study, post-1965, pairing a normative exposure with a fertility level. None of 166 screened records does. The 28 link records are SDT-heavy but all have use outcomes; the one primary record closes in 1974. |

**`No evidence`, not `VERY LOW`.** VERY LOW rates a body that exists and is badly identified. These
cells contain nothing, and rating them VERY LOW would make it look as though the question had been
investigated and answered poorly rather than not investigated. Each pairs with NOT ASSESSED in §8.

### 9.3 The link stratum, rated separately

`LINK_NORM_USE` is **not** this chapter's parameter and its rating must not be read as the
chapter's verdict. It is rated because §7.2 reports it and an unrated reported body invites
misreading.

Body: 28 studies of a normative exposure on contraceptive or abortion use. Twenty-four are
cross-sectional with controls; the ceiling is one weekly longitudinal panel with a mediation design
(McLoughlin Brooks and Weitzman 2022, 39,806 person-weeks) and one community fixed-effects panel
(Ragan 2012).

**Starting level: Low** — §4.1's band for panel and cross-sectional designs with controls.

| domain | assessment | downgrade |
|---|---|---|
| **Risk of bias** | Common-method bias in 24 of 28: exposure and outcome are self-reported by the same respondent in the same instrument, and a woman who has internalised destigmatisation reports less stigma *and* reports more use. The bias runs in the direction of the hypothesis. The D.3.b instrument added a common-method-bias domain for this reason and this chapter inherits it. | **−1** |
| **Inconsistency** | Apparent sign disagreement across studies is **explained, not unexplained**: stigma of contraception lowers use while stigma of premarital sex raises it (§2). GRADE does not downgrade for heterogeneity that stratification resolves, and the synthesis refuses to pool across `stigma_object`. No downgrade. | 0 |
| **Indirectness** | None *for the link*. These studies measure exactly the stigma→use relationship they are being rated on. The indirectness is to the *chapter's* parameter, which is handled by not pooling them into it rather than by downgrading them here. | 0 |

**Low − 1: VERY LOW for the body.** Stated with one qualification that carries information the band
alone loses: rated on the two best-designed records alone — the weekly panel and the community
fixed-effects panel, neither of which has the common-method problem in the same form — the link
stratum would be **LOW**. The body is dragged down by two dozen cross-sectional self-reports, not by
its ceiling.

### 9.4 Rater independence — the requirement is unmet

`PROTOCOL.md` §5.1 step 11 requires **three independent raters**. This section is the work of
**one**, and the same reader made every screening and full-text call it rests on. Simulating two
further raters would produce agreement by construction and is not done, for the same reason the
adversarial re-read in the screen log is labelled a self-check rather than a second opinion.

A judgment-blinded rating sheet is at
`output/stigma-reduction-contraception-abortion-grade-rater-sheet.csv`: it carries the design facts,
the study list and the domain prompts, with **every rating and downgrade withheld**, for Alexandra
and Anup to complete independently. Until two further ratings exist, §9 is **provisional** and the
chapter's status line says so.

## 10. Verdict

**The hypothesis that destigmatising contraception and abortion lowered fertility is, on the evidence that exists, unevaluated rather than supported or refuted — and the reason is that the study it requires has not been done.**

A search over three arms and a citation snowball, screening 166 records and reading 24 full texts, found exactly **one** study pairing a normative exposure with a convertible fertility outcome: a 1983 regression on Swedish nonmarital birth rates, 1911–1974, whose exposure is pressure to marry rather than pressure not to contracept, and whose outcome may describe how a birth is labelled rather than whether it occurs. It is graded **VERY LOW** for the First Demographic Transition — Low by design class, downgraded once for structural reverse causation and once for indirectness of both exposure and outcome. The pre-modern and Second Demographic Transition cells are **No evidence**, paired with NOT ASSESSED demographic significance: not a body of evidence judged poor, but no body at all.

The one number to carry away is not an effect size. It is **58 of 668** — numerator: records carrying realized-fertility vocabulary; denominator: the 668-record frozen retrieval frame as measured by `404` on 2026-09-17; window: the frame, not a phenomenon — against 479 records taking contraceptive use instead. It is a statement about a literature's attention, **not a demographic-significance share**, and it is not banded as one. A.6 is well evidenced at a link it does not own — twenty-eight studies of normative barriers to contraceptive *use*, the best of them finding that partner opposition accounts for about 15% of unmet need — and essentially unevidenced at the link it does. Wolff and colleagues said as much in 2000: answering this chapter's question "would require a prospective study over time to observe the fertility outcomes of disagreement." Nothing in this review has done it.

That is a finding about a literature, not a finding about the world. Destigmatisation may well have mattered. This chapter cannot say, and can say precisely why.

## 11. Open questions

**1. Is Kelly and Cutright's estimate a fertility effect or a recomposition?** The single primary record turns on this. Its outcome — age-specific illegitimacy rates per 1,000 unmarried women — is convertible in form, satisfying the admissibility test. But its exposure is pressure to *legitimate by marriage*, which acts on whether a conception becomes a marital or a nonmarital birth. If the marriage happens and the birth follows, total fertility is unchanged and only the label moves. **This is the chapter's most consequential open question**: resolved one way the primary cell holds one VERY LOW record, resolved the other it is empty and §10's verdict changes from "one study, very low" to "no study". Recommendation: request the age-specific unmarried-share series and test whether the fitted legitimation effect survives aggregation to the general fertility rate. If it does not, reclassify to `OFF_COMPOSITION`.

**2. Three independent GRADE raters are required and one was used.** §9 is provisional on this. A judgment-blinded sheet with every rating, downgrade and starting level withheld is at `output/stigma-reduction-contraception-abortion-grade-rater-sheet.csv`, with the instrument and the evidence facts in `output/stigma-reduction-contraception-abortion-grade-evidence-brief.md`. Raters should not read §9 first. Disagreements are to be resolved rather than averaged, with the reason recorded beside the final band.

**3. An independent second read is owed.** The same reader made every screening call. A judgment-blinded sheet with first-pass cells withheld is at `output/stigma-reduction-contraception-abortion-second-review-sheet.csv`. Adversarial self-re-reading of five flagged records changed two of them, which is evidence the exercise finds things and also evidence it is not a substitute for independence.

**4. Fifteen wanted full texts are unretrieved (38%).** The four that would change something: *Female Sexual Attitudes and the Rise of Illegitimacy* (1981) and *Illegitimate Births and Bridal Pregnancy* (2008), both call-8 candidates whose outcome measure is unknown; *Adolescent background and fertility norms* (1990), whose exposure is explicitly fertility norms and whose "early childbearing" outcome may be a level; and *Barriers to family planning service use among the urban poor in Pakistan* (2005), from the tradition that doses opposition routinely.

**5. The sampled tail is unread.** 240 records across the low-prior strata of the frozen arms and ARM C's `C4`/`C5`/`C6` were sampled rather than read. The sample bounds the chance the flagger misrouted a primary-cell study out of the exhaustive strata; that bound is not yet computed.

**6. Version copies inflate every count over ARM C.** *From Shame to Game* appears six times under four title variants; Ragan appears at least four times under three titles. TICK-084 treats version-pair splitting as a resolver defect; this chapter shows it is also a counting defect that misstates frame sizes.

**7. Studies that do not exist and should.** The prospective design Wolff and colleagues named: a cohort in which partner or community opposition is measured at baseline and completed fertility is observed, with method availability held fixed. Second, any design exploiting a religious authority's ruling on contraception as a norm shock with access unchanged — the cleanest available instrument for A.6's exposure and, as far as this review found, unused. Third, a study separating stigma of contraception from stigma of premarital sex within one population, which §2's sign problem makes necessary before any pooling is defensible.

## 12. References

Bongaarts, J. and Bruce, J. (1995). The causes of unmet need for contraception and the social content of services. *Studies in Family Planning* 26(2).
Bongaarts, J. and Watkins, S. C. (1996). Social interactions and contemporary fertility transitions. *Population and Development Review* 22(4).
Caldwell, J. C. (1999). The delayed Western fertility decline: an examination of English-speaking countries. *Population and Development Review* 25(3).
Casterline, J. B. and Sinding, S. W. (2000). Unmet need for family planning in developing countries and implications for population policy. *Population and Development Review* 26(4).
Cleland, J. and Wilson, C. (1987). Demand theories of the fertility transition: an iconoclastic view. *Population Studies* 41(1).
Cockrill, K. et al. (2013). The stigma of having an abortion: development of a scale. *Perspectives on Sexual and Reproductive Health* 45(2).
Fernández-Villaverde, J., Greenwood, J. and Guner, N. (2010). From shame to game in one hundred years. NBER Working Paper 15677.
**Kelly, W. R. and Cutright, P. (1983). A time series analysis of Swedish illegitimacy rates, 1911–1974. *Sociological Focus* 16(2), 79–93.**
Kramer, K. L., Hackman, J., Schacht, R. and Davis, H. E. (2021). Effects of family planning on fertility behaviour across the demographic transition. *Scientific Reports* 11.
Kumar, A., Hessini, L. and Mitchell, E. M. H. (2009). Conceptualising abortion stigma. *Culture, Health and Sexuality* 11(6).
Link, B. G. and Phelan, J. C. (2001). Conceptualizing stigma. *Annual Review of Sociology* 27.
McLoughlin Brooks, I. H. and Weitzman, A. (2022). Religiosity and young unmarried women's sexual and contraceptive behavior. *Demography* 59(3).
Norris, A. et al. (2011). Abortion stigma: a reconceptualization. *Women's Health Issues* 21(3).
Phillips, J. F., Hossain, M. B. and Arends-Kuenning, M. (1996). The long-term demographic role of community-based family planning in rural Bangladesh. *Studies in Family Planning* 27(4).
Prettner, K. and Strulik, H. (2017). It's a sin — contraceptive use, religious beliefs, and long-run economic development. *Review of Development Economics* 21(3).
Ragan, K. S. (2012). Sex and the single girl: cultural persistence and the pill. Working paper, Stockholm School of Economics.
Rajan, S. (2014). *Essays on fertility and fertility preferences in India.* PhD thesis, Duke University.
Sedgh, G., Ashford, L. S. and Hussain, R. (2016). Unmet need for contraception in developing countries. Guttmacher Institute.
Wolff, B., Blanc, A. K. and Ssekamatte-Ssebuliba, J. (2000). The role of couple negotiation in unmet need for contraception and the decision to stop childbearing in Uganda. *Studies in Family Planning* 31(2).
Yeatman, S. and Sennott, C. (2024). Fertility desires and contraceptive transition. *Population and Development Review* 50(3).
Yüceşahin, M. M. and Özgür, E. M. (2008). Regional fertility differences in Turkey. *Population, Space and Place* 14(2).

---

## Provenance and standing caveats

**This chapter is written on 24 of 39 wanted full texts (62%).**

**The findings that would survive full retrieval are the structural ones — the two-literature split, the 1.8% identified-design share, the 58-of-668 outcome scarcity, the 8-of-2,815 bridge count, and the failure of R3 for want of a pre-1985 dose series; the findings that might not are the count of the primary cell and therefore §10's verdict, since four of the fifteen unretrieved records are call-8 or A.5 candidates whose outcome measure is unknown.**

**An objection over which this chapter is written.** The scoping recommendation was to redefine A.6 around the literature that turned out to be reachable — "normative and opposition-based barriers to contraceptive use" — which would have made the 28 link records the primary cell and given the chapter a real evidence base. The PI rejected it: *"It's better to report an honest output given our pre-registered plan than to change it given findings related to evidence."* The ruling is right and the recommendation was a form of outcome-driven scope change. The chapter is written on the registered claim, and the redefinition survives only as a future-research note.

**Numbers taken from abstracts rather than full text.** All frame sizes, overlaps and marker shares in §§3–4 are OpenAlex title-and-abstract record counts, asserted against the diagnostic JSONs by `406`. Of the 166 screened records, 24 were read in full; the remaining 142 were screened on title, flags and a 300-character abstract snippet. **For batch 2 (the 152 records of `S4_FERT_NODESIGN`), the `cell` and `note` fields are read decisions but `estimator_class`, `stigma_object` and `stigma_bearer` are script-derived from flags and titles and carry no evidential weight.** One record was reclassified during the second read after its note was found to assert a design and a measurement scale that had not in fact been read; the correction is recorded in the screen log and the lesson is that any note in this chapter reading like a claim about a paper's design should be treated as unverified unless the record appears in the 24.

**Two records rest on OCR.** Caldwell 1999 and Wolff et al. 2000 arrived as page images and were OCR'd at 548 and 821 words per page against a 531 calibration — ample for screening, but Wiley's vertical watermark interleaves with body text and two-column pages mix across line breaks. **Any quotation from those two must be checked against the PDF before publication**, including Wolff's sentence quoted in §10.
