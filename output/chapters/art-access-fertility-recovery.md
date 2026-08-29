# A.17 — Assisted Reproductive Technology Access

**Category:** Proximate causes
**Primary mechanism:** Availability and affordability of ART (IVF, ICSI, egg freezing) allows births that age-related fecundity decline would otherwise have prevented, partially recovering postponed fertility.
**Cross-references:** A.15 (Maternal Age and Fecundity Decline — the loss this mechanism repairs) · A.12 (Twinning — owns the multiplier; this chapter owns the deliveries) · A.11 (Tempo Effects) · C.2.a (Childcare Cost) · B.2/B.4/B.6/B.7 (why subfecundity rose — this chapter begins after the diagnosis)
**Status:** INTERIM DRAFT — TICK-072, 2026-08-25. Not PI-reviewed. **Written on 33 of 131 wanted full texts (25%).** See the provenance block; several findings below are explicitly gated on retrieval that has not happened.

---

## 1. The claim

### 1.1 In plain terms

In plain terms: people have been having children later, and fertility falls off with age. IVF and related treatments exist to help when that has become difficult. The claim is that they are winning some of those births back — that the birth rate would be lower still without them.

The obvious way to check is to count how many babies are born through fertility treatment and call that the contribution. Two things are wrong with that number, and both are the whole of this chapter.

**Some of those babies would have arrived anyway.** Not everyone who has treatment needed it to conceive; some couples would have succeeded on their own, later or with more time. Counting every treatment baby as *saved by* treatment assumes the alternative was none, and nobody has checked how often that is true.

**And the availability of treatment may be part of why people waited.** If it is widely known that there is a way to have a child later, the reason to hurry weakens. Some of the difficulty that treatment is solving is difficulty its own existence helped create. **A remedy that repairs a problem it partly caused is contributing less than its output suggests** — and conceivably nothing at all, if the waiting it encourages costs more births than the treatment recovers.

This chapter asks what the treatment is actually worth, and finds that the research counting treatment babies and the research measuring what would have happened otherwise are two separate literatures that cite each other and never join up.

### 1.2 The claim precisely

**This chapter explores the effect of access to assisted reproductive technology on the total fertility rate.**

HYPOTHESES-v5 §A.17 states it as: *"Availability and affordability of ART (IVF, ICSI, egg freezing) partially offsets age-related fecundity decline and enables completion of postponed fertility, raising TFR relative to the counterfactual without ART."* The registry adds that the quantitative contribution is small — under 5% of births in most OECD countries — **but growing**.

**The parameter this chapter estimates is the number of births that occur because ART is available and would not have occurred otherwise, measured as a contribution to the total fertility rate — children per woman.** (The *total fertility rate*, or TFR, is the number of children a woman would bear if she experienced current age-specific birth rates throughout her life.)

The claim decomposes into two sub-claims that require completely different evidence and must never be pooled:

| | Sub-claim | Evidence type | What it bounds |
|---|---|---|---|
| **Arm 1** | ART-conceived births are a measurable share of all births, and that share is a contribution to the TFR | National registries and vital statistics; simulation | The contribution **from above** |
| **Arm 2** | Expanding ART *access* raises births | Insurance mandates, public funding reforms, price variation | The contribution **from below** |

Arm 1 answers *how many births are ART births*. That is not the claim. The claim is about a counterfactual — births *relative to the counterfactual without ART* — and the share equals the effect only if no ART birth would have occurred otherwise. Arm 2 answers *what one more unit of access buys*, which is closer but still not the claim: a subsidy moves the price for an inframarginal user, not the technology's existence.

**The two arms bracket the registered quantity. They are not two estimates of it.** This chapter reports the bracket.

---

## 2. Theoretical mechanism

The reader's economics vocabulary carries almost all of this.

**The upstream problem is a deadline.** Female fecundity — the monthly probability of conception — falls steeply after the early thirties. Postponing childbearing therefore converts an intention into a lottery, and some intended births never happen. That is A.15's territory and this chapter takes it as given.

**ART is a technology that relaxes a constraint, and its value depends entirely on how binding the constraint was.** In the reader's terms: if biology is the binding constraint on realized fertility, relaxing it raises output roughly one-for-one. If the binding constraint is something else — the cost of children, partnership, housing, career timing — then relaxing the biological constraint moves the outcome very little, because a different constraint binds first. **The size of A.17's effect is therefore not a fact about medicine. It is a fact about which constraint binds.**

Three features of this structure decide how the chapter must be read.

**It is an extensive-margin mechanism operating on a selected population.** ART acts on whether a birth happens at all, among people who have already tried and failed. It does not change desired family size. So the ceiling on the mechanism is the size of the population whose *intended* births are blocked by fecundity — not the size of the population using ART, which includes people who would have conceived anyway and excludes people who would benefit but do not access it.

**There is a feedback, and it runs the wrong way for the hypothesis.** ART demand is generated by postponement. Women seek treatment because they started late. Any offset the technology provides is therefore partly a consequence of the very decline it is claimed to offset, and a component that exists only because the decline occurred cannot be evidence against the decline's cause. A.12 met the identical structure — a quarter of the modern twinning rise is driven by delayed childbearing — and had to net it out. Here the feedback is not a component of the demand; it is most of the demand.

**And there is a behavioural channel that could make the sign ambiguous.** If people believe ART can undo age-related decline, the perceived cost of postponing falls, and some postpone who otherwise would not. Should that channel be large, the technology's net contribution is smaller than its throughput and could in principle be negative. This is the remedy generating part of the problem it treats. Section 7.3 reports what is actually known about it, which is more than the scope expected and less than the mechanism requires.

**What would make the hypothesis wrong.** Not a finding that ART births are few — they are few and the registry says so. The hypothesis is wrong if the births it produces would substantially have occurred anyway, or if the availability of the technology causes enough additional postponement to offset its own repairs.

---

## 3. Search strategy

Full detail in `literature/search-logs/art-access-fertility-recovery-search-scope.md`. Three rulings shaped it.

**The boundary with A.12 was inherited, not drawn.** A.12's scope-freeze had already ruled that ART live births decompose as `D_ART × (1 + m_ART)`, with **A.17 owning the deliveries and A.12 owning the multiple-birth multiplier**. The split is additively separable, so the two chapters sum without double-counting. The operational rule is **route by outcome, not by topic**: an insurance-mandate paper whose estimated outcome is the multiple-birth rate is A.12's, however much it looks like this chapter's. Papers reporting both are extracted by both, on different rows.

**The retrieval vocabulary and the diagnostic vocabulary are different objects, and this chapter is the first in the series to say so.** A strict population-only vocabulary ("total fertility rate", "completed fertility", "cohort fertility") scores the 204,210-record clinical decoy cloud at **0.1%** contamination — excellent as a measuring instrument. Used to *draw the frame* it reaches **4 of 12 empirical anchors and finds 2 primary-cell records in a 7,589-record frame**, against the loose vocabulary's 12 and 148. In the two largest access-literature clouds, population vocabulary runs 68% and 64% loose against **2% strict**, with strict primary cells of zero. The economics of access does not use demographers' words for demographers' quantities. **The frame is therefore drawn loose and the decoy is removed by screening, not by querying.**

**Two walls were declared unenforceable in advance; measurement narrowed both.** Wall 5 (medical versus elective fertility preservation) was declared unenforceable at title/abstract. Measured, the preservation population is 76% oncological, 5% elective and 17% naming neither — and reading that residue showed most of it is not ambiguous but *medical for a non-oncological reason*: Turner syndrome, sickle cell, cystic fibrosis, BRCA carriage, transplant conditioning, gender-affirming care. **The wall was cut on the wrong axis.** The real structure is medical versus elective, with medical splitting further. Similarly, the arm-1/arm-2 split was declared invisible at title/abstract; the screen resolved it for **85.6%** of records, leaving a defined full-text queue rather than an unbounded one.

---

## 4. PRISMA flow

| Stage | n |
|---|---|
| Tier-A anchors resolved and existence-verified | 21 of 23 |
| Tier-B one-hop citation frame (complete, no truncation, zero failed requests) | 7,589 |
| After collapsing version duplicates | 7,313 |
| Screening worklist (budget slice + four bypasses) | 1,020 |
| Title/abstract screened | 1,020 |
| RELEVANT / UNCERTAIN / NOT_RELEVANT | 192 / 212 / 616 |
| Wanted for full text (7 jobs, triaged by role) | 131 |
| **Retrieved** | **33** |
| Full-text screened | 33 |

**Three features of this funnel change how the chapter should be read.**

**The retrieval fraction is 25% and the failure is not paywalls.** The open-access ceiling was 76%. Of the 98 failures, **67 had an open URL in hand and the fetch returned HTML** — verified by hand across three publishers, all returning 403 even with a browser user-agent string. That is bot defence, not authentication: those 67 are downloadable by anyone with a browser. Only 31 records genuinely require institutional access.

**The job that matters most is the one least retrieved.** Retrieval was triaged into seven jobs by *role* rather than by cell, because the records that decide this chapter's headline number share no cell — they sit in P4, in OFF_OTHER, and in Wall 2's neighbourhood, and what they have in common is that each measures births among the *untreated*. That is job A1, and **it is 2 of 14 in hand.**

**The bypasses were measured, and the cheapest won.** The elective-preservation bypass returned 34.8% relevant and placed 56.5% of its records in an A.17 cell — the best rate in the worklist, on the cell reconnaissance suggested would be empty. The arm-2 bypass returned 4.3% on 23 records; it earned its place as insurance rather than yield, since missing an identified estimate is unrecoverable.

---

## 5. The ideal design

Written before the literature was read, so §6 can be compared against a fixed yardstick rather than against the best paper that happens to exist.

### 5.1 The ideal estimand

The change in completed cohort fertility, in children per woman, caused by **the availability of ART in a population** — not by one more unit of subsidy, and not the share of births that are ART births — **net of any postponement the availability itself induced.**

Three clauses, and the literature satisfies none of them.

*Availability, not subsidy.* Arm 2's insurance-mandate designs move a price for people who already live in a world with ART. They estimate the elasticity of use with respect to cost, which is a different parameter from the technology's existence.

*Completed cohort fertility, not a birth share.* Arm 1's registry share answers *how many births are ART births*, which equals the effect only if no ART birth would have occurred otherwise.

*Net of induced postponement.* This is the clause that makes the estimand hard rather than merely unmeasured, and §7.3 reports it is the largest correction and is unquantified.

### 5.2 The design that would identify it

**Source of variation.** Staggered, population-level arrival or withdrawal of ART availability that is **not** a price change: the initial diffusion of IVF across countries after 1978; a regulatory ban or its reversal — Italy's Law 40 and its partial annulment, Costa Rica's prohibition and the Inter-American Court ruling that ended it, Germany's and Switzerland's restrictions; or the opening of the first clinic in a region.

**Comparison group.** Comparable populations without access in the same period, with the pre-period fertility trajectory observed.

**Identifying assumption.** The regulatory change moved access and did not accompany a change in fertility norms or in the economic conditions driving postponement. Falsifiable: pre-trends in the age schedule of fertility; and, critically, **a test on the postponement margin itself** — if mean age at first birth moves with the availability change, the induced-postponement channel is live and must be netted out rather than assumed away.

**Estimating equation.** Completed cohort fertility on availability, with the age schedule of births reported alongside so the postponement channel is visible; and, separately, the ART birth share, so the counterfactual gap between share and effect can be estimated rather than assumed.

**Data required.** Cohort fertility to completion in populations spanning an availability change, with an ART registry. **Italy's Law 40 episode has all of this**, and the Costa Rican prohibition is the cleanest on-off switch in the world.

**Sample size.** National populations; not a constraint.

**What the ideal design excludes.** Registry shares presented as contributions, which assume the counterfactual is zero. Insurance-mandate designs presented as estimates of ART's contribution rather than of its price elasticity. And any design that measures the birth outcome without the age schedule, which cannot see the induced-postponement channel at all.

### 5.3 Distance from the ideal

| Design family | Availability, not price? | Counterfactual estimated? | Induced postponement netted? | Distance |
|---|---|---|---|---|
| **Arm 1** — registry shares (Czechia, Italy, Australia, Denmark, US) | Neither; descriptive | **No — assumed zero** | No | **Bounds from above** |
| **Arm 2** — insurance mandates and funding reforms | **No — price** | Partly, within the design | No | **Bounds from below** |
| **Regulatory on-off switches** (Italy Law 40, Costa Rica) | **Yes** | **Would be** | **Testable** | **The ideal — and unused for fertility** |

**No study implements the ideal design, and the two arms that exist bracket the estimand rather than estimating it.** Arm 1 answers how many births are ART births; Arm 2 answers what one more unit of access buys. **The registered quantity is between them and is estimated by neither.**

**The design that would close it exists as a natural experiment nobody has used for this outcome.** Italy's Law 40 sharply restricted ART in 2004 and was partly annulled in 2009 and 2014; Costa Rica prohibited IVF outright from 2000 until a 2012 Inter-American Court ruling forced its return. **These are population-level, staggered, non-price changes in availability** — exactly §5.2 — and the fertility literature has not exploited them. They have been studied extensively as questions in law and bioethics.

**And no design in either arm reports the age schedule alongside the birth outcome**, which is what would make the induced-postponement channel visible. That is why §7.3's largest correction has a known direction and no magnitude.

---

## 6. Included studies

33 full texts: **14 arm 1** (counting), **11 arm 2** (access estimates), 8 neither. Full table in `extraction/art-access-fertility-recovery-fulltext-screened.json`; risk of bias per study in `extraction/art-access-fertility-recovery-risk-of-bias.csv`.

### 6.1 The naive estimator in this literature, and what it conditions on

The template requires this check explicitly, and here it has an unusually clean answer.

**The naive estimator is subtraction.** An author with a national registry computes non-ART births as total births minus ART births, calls the difference the counterfactual, and reports the gap as ART's contribution. It requires no comparison group and no identification strategy, and it is what most of this literature does.

**What it conditions on is treatment receipt** — and treatment receipt is selected on exactly the outcome. People reach ART because they have already tried and failed to conceive, which means the comparison implicit in the subtraction is between people whose fecundity is known to be impaired and a counterfactual in which those same people have zero further births. **The direction of the bias is upward, without ambiguity.** Some couples who receive ART would have conceived spontaneously; the literature that measures how many is a real literature, and the literature that computes the shares does not use it.

**Nine of the 14 arm-1 records in hand use the naive estimator.** Four confront the counterfactual.

### 6.2 The exhibit

The Czech contribution study (*Scientific Reports*, 2023) is worth quoting because it is not a case of ignorance, which would be less interesting.

It builds a `TFR_nonART` series by pure subtraction — stated as its equation (1) — and concludes that **"without ART the TFR would have stood at just 1.65 instead of 1.71 in 2020."** It also concedes, in a single clause, that *"the albeit low overestimation of the number of ART births due to the possibility that some women became pregnant via sexual intercourse following ART cannot be excluded"*, and cites for it a five-year follow-up of couples who **discontinued** ICSI treatment.

The words *spontaneous*, *discontinued*, and that author's name appear **zero times in the body of the paper**. The overestimate is called "low" and never given a number.

**The counterfactual literature is known to the accounting literature, cited by it, characterised without measurement, and not used.** That is the chapter's central observation about the state of the field, and it required reading the full text — no abstract contains it.

---

## 7. Quantitative synthesis

### 7.1 The answer in plain terms

**ART produces a real but small number of births, the published figures for that number are upper bounds, and nobody has estimated the correction.**

Across the five national settings where a share and a fertility series can both be had, ART accounts for somewhere between **2.7% and 11.8%** of the fertility decline since 1965 — the low end in the United States, the high end in Czechia, and the difference is mostly how much access each country funds. Every one of those figures assumes that no ART birth would have happened otherwise.

The access literature, which is better identified, is consistent with a small effect and cannot yet measure it, for a reason that is itself a finding: **in the United States the policy everyone studies does not bind on most of the people it is named for.**

### 7.2 The estimate

**No pooled estimate is reported, and this is a ruling rather than a shortfall.** The two arms do not estimate the same parameter. Pooling a tabulated share with a policy elasticity would produce a number that is an estimate of nothing, and the template's rule — resolve disagreements, do not average them — applies before the disagreement appears.

**Arm 1, the upper bound.** ART-conceived births run at 1.3–2.0% of births in the United States, 3.7–3.9% of the TFR in Italy, up to 3.8% of births in Czechia, 4.2% of births in Denmark (2004), and 6.7% of births in Australia (2017). The Australian figure splits as **4.8% ART and 1.9% ovulation induction**, which matters: ovulation induction is invisible to ART registries, so registry-based shares understate medically assisted reproduction by roughly a quarter.

**Arm 2, the lower bound, and the reason it is not zero-informative.** Eleven access records are in hand, spanning US state mandates, Quebec, Ontario, Australia's 2010 Medicare reduction, Russia's 2014 insurance inclusion, and Israel. Two results stand out.

*Israel, under unlimited publicly funded access.* The proportion of women aged 40–44 undergoing IVF rose between 2011 and 2014, and **age-specific birth rates did not substantially change**, while live births *per treatment* fell. Expanding treatment at the ages where fecundity is lowest moved the aggregate not at all. This is the single most informative access record in the frame, and it points against the registry claim.

*The United States, where the treatment is not the treatment.* **65% of US workers are insured through self-insured employers who are exempt from state mandates under ERISA, and only 41% of self-insured employers in mandate states cover IVF.** Every estimate treating "state mandate" as the exposure is measuring a policy that fails to bind for most of the workforce. The attenuation is toward zero by construction, so **a small or null US mandate effect is not evidence that access does not matter** — it is evidence that the instrument is weak. This is a risk-of-bias domain for the entire cell and it does not appear in the papers themselves.

*And a first stage nobody is looking at.* Three economics papers — an *AER* 2017 study, a *Journal of Human Resources* 2008 study, a *Journal of Population Economics* 2017 study — use IVF treatment success as an instrument for childbearing in order to estimate effects on women's careers. The *AER* paper states the exclusion restriction as "treatment success exclusively affects labor earnings through its first-stage impact on fertility." **Their first stages are A.17's parameter**, estimated on administrative data with clean identification, and reported as a nuisance quantity on the way to a labour-economics result. A.12 met the identical structure in the twin-instrument literature. Those first stages have not yet been extracted and they are the most promising unexploited evidence in this chapter.

### 7.3 The behavioural channel, which is better measured than expected and still weak

The scope predicted this channel would be measured on the belief side and unmeasured on the behaviour side. That was too pessimistic, and the correction matters.

Beliefs are well documented: adults substantially overestimate ART's success rates; the misperception has a documented supply side in media coverage; and a *Fertility and Sterility* paper is titled, in as many words, *"A persistent misperception: assisted reproductive technology can reverse the aged biological clock."*

The behaviour link has now been tested directly. A 2026 *European Journal of Population* study asks whether confidence in ART's ability to help women conceive in their thirties predicts delayed fertility intentions in the US. It finds that women 35+ with positive views are *less* likely to abandon their intentions; that women in their thirties confident in ART are more likely to postpone — **but that this key finding is not statistically significant**; and that positive perceptions do *not* encourage postponement before the thirties, contradicting the authors' own first hypothesis. Their summary is "a possible but weak mediating pathway."

**The verdict is therefore "measured and weak", not "unmeasured".** That is a stronger and more defensible position, and it means the sign-ambiguity worry in §2 does not currently bite.

Separately, and bounding the damage rather than the mechanism: in Austria, up to 70% of women expressing a firm short-term intention at ages 30–32 had a child within four years, while **almost no woman aged 42–45 did.**

---

## 8. Demographic significance

**The phenomenon to be explained is measured in whole children per woman; this mechanism offers a share of births running between about 1% and 7%.**

On A.12 a units check of this shape ended the chapter: a multiplier bounded between 1.01 and 1.05 cannot explain something denominated in whole children, and no study could have changed that. **It does not end this one.** A few percent of a TFR is not nothing when the decline to be explained is around one child. A.17 has to do the arithmetic A.12 could skip — which is the difference between a mechanism that is the wrong size and a mechanism that is merely small.

Arithmetic, per country: `TFR_without = TFR_observed × (1 − s)`, and the offset is the contribution divided by the decline that would have occurred without ART, from a 1965 baseline. TFR from World Bank `SP.DYN.TFRT.IN`; shares from the retrieved full texts.

| Country | Year | Share | of | TFR 1965 | TFR obs | TFR without | Contribution | Decline without ART | **Offset** | Verdict |
|---|---|---|---|---|---|---|---|---|---|---|
| Czechia | 2020 | 3.4% | TFR | 2.18 | 1.74 | 1.681 | +0.059 | 0.499 | **11.8%** | MINOR |
| Australia | 2017 | 6.7% | births | 2.977 | 1.741 | 1.624 | +0.117 | 1.353 | **8.6%** | MINOR |
| Denmark | 2004 | 4.2% | births | 2.61 | 1.78 | 1.705 | +0.075 | 0.905 | **8.3%** | MINOR |
| Italy | 2023 | 3.9% | TFR | 2.6 | 1.21 | 1.163 | +0.047 | 1.437 | **3.3%** | NEGLIGIBLE |
| United States | 2019 | 2.0% | births | 2.913 | 1.706 | 1.672 | +0.034 | 1.241 | **2.7%** | NEGLIGIBLE |

Czechia is the only case where a retrieved paper reports the with-and-without pair itself — **1.71 with ART against 1.65 without**. Against the same 1965 baseline of 2.18 that is an offset of **11.3%**, against this table's reconstruction of **11.8%**. The two agree to within half a percentage point, which is the point of computing both: the reconstruction can be trusted for the four countries where no paper states the pair.

**A denominator warning the table cannot fix.** Three shares are shares *of births* and two are shares *of the TFR*, and they are not the same quantity. Converting a birth share into a TFR contribution assumes ART is spread evenly across the age schedule. It is not: the Italian data show ART at 3.7% of the TFR overall and **16% among the oldest mothers**. A flat birth share therefore biases the contribution *upward* — the same direction as the counterfactual error. The two errors compound; neither offsets the other.

**And the endogeneity check, which is the largest correction and is unquantified.** ART demand is generated by postponement. Part of every figure in that table exists only because the decline occurred, and a feedback of a decline is not evidence against its cause. **No study in hand decomposes the share into an induced-by-postponement part and an independent part.** The correction's magnitude is unknown; its direction is not.

### 8.1 Pre-modern

**For pre-modern variation, the verdict is NOT ASSESSED, because the technology did not exist.** This is an absence of the exposure, not an absence of evidence. Had it existed the sign would be positive.

### 8.2 First Demographic Transition

**For the FDT, the verdict is NOT ASSESSED, because the technology did not exist.** The first IVF birth was in 1978, thirteen years after the FDT window closes.

### 8.3 Second Demographic Transition

**For the SDT, the verdict is MINOR, because ART's contribution runs between 2.7% and 11.8% of the observed decline across the five settings measured — and every one of those figures is an upper bound before the counterfactual and postponement-feedback corrections are applied.**

The verdict is stated at the top of the range deliberately. The band boundary between NEGLIGIBLE and MINOR is 5%, the range straddles it, and reporting the favourable end is the honest way to write a bound: if the mechanism is small even when measured generously, that conclusion is robust to the corrections not yet made.

**One clause of the registry entry is contradicted rather than merely unsupported.** v5 states the contribution is small "but growing". The only projection in hand — Italy to 2050 — has the MAR share essentially **flat, 3.9% rising to 4.3%**, with the paper noting that population ageing alone has a negligible effect. One country is not a refutation, but it is the opposite of the registry's direction and it should not be reported as agreement.

---

## 9. GRADE rating

Per phenomenon, not per chapter. **Rated by one rater**; PROTOCOL §6 requires three independent raters and that requirement is open (§11).

| Phenomenon | Rating | Reasoning |
|---|---|---|
| **Pre-modern** | **NOT ASSESSED** | The technology did not exist. |
| **FDT** | **NOT ASSESSED** | The technology did not exist. |
| **SDT** | **LOW** | Downgraded three steps from the observational starting point. |

**Risk of bias in the body as a whole — down one.** Arm 1's dominant domain fails on 9 of 14 records: the share is reported as an effect. The postponement-feedback domain fails on **all** of them — not a criticism of any single paper but a property of the literature. Arm 2's treatment definition is attenuated by construction wherever the exposure is a US state mandate.

**Indirectness — down one.** The registered estimand is births relative to a counterfactual without ART. Arm 1 measures a share; 8 of 11 arm-2 records measure utilisation rather than births. **Neither arm measures the registered quantity directly**, and the arm that comes closest — the untreated-subfertile comparison — is the arm with 2 of 14 records retrieved.

**Imprecision — down one.** Five country-settings carry the entire demographic-significance arithmetic, and the offset range across them spans the boundary between NEGLIGIBLE and MINOR. A range that straddles its own verdict band is imprecise in the sense GRADE means.

**Not downgraded for inconsistency** — the shares agree closely once the denominator is handled, and the spread tracks access regime. **Not downgraded for publication bias**, which this chapter cannot assess: a tabulated share has no null hypothesis to fail to reject.

**What a HIGH rating would have required is not more studies but a different one:** a comparison of births among subfertile people who did and did not receive treatment, at population scale, with selection into treatment handled. The frame contains the ingredients — untreated-prognosis models, dropout cohorts, discontinuation follow-ups — and nobody has assembled them into an estimate of ART's population contribution.

---

## 10. Verdict

**ART raises fertility, and by less than its own accounting suggests.**

Across five countries, ART-conceived births offset between 2.7% and 11.8% of the total fertility decline since 1965 — under 3% in the United States, around 12% in Czechia, with the spread driven mainly by how much treatment each country funds. **The verdict for the Second Demographic Transition is MINOR**, and it is stated at the generous end of the range on purpose, because every figure in it is an upper bound: nine of the fourteen accounting studies in hand treat every ART birth as one that would not otherwise have occurred, and none nets out the part of ART demand that postponement itself created.

The one number to carry away is **about a tenth, at most, of the fertility decline in the country that funds treatment most generously — and under a thirtieth in the United States.** ART is a real mechanism operating on a real constraint. It is not a candidate explanation for the Second Demographic Transition, and the registry's clause that its contribution is growing is contradicted by the only projection retrieved.

The most useful thing found in this chapter is not a number. It is that **the literature which counts ART births and the literature which measures what happens to untreated couples cite each other and do not connect.** One paper concedes the problem in a clause, cites the contrary evidence, calls the overestimate "low" without measuring it, and subtracts anyway. Closing that gap requires no new data collection — only a study that puts the two existing literatures in the same equation.

---

## 11. Open questions

**PI calls carried from the scope, still open.**

1. **Does the chapter report arm 1 at all, given that it is a bound and not an estimate?** Drafted as yes, both arms, each labelled. Reporting only arm 2 discards the one well-measured quantity; reporting only arm 1 states an upper bound as an effect, which is the error B.5 shipped.
2. **Is elective egg freezing in scope?** Measured: ~46–49 records in the whole frame name an elective indication, and the decisive one — a 10–15 year return-rate follow-up — is blocked-but-open and not in hand. **No verdict on P5 is offered.**
3. **Cross-border reproductive care.** Registries count treatments by clinic country and births by residence country. The Czech paper explicitly excludes cross-border mothers; others do not say. Unresolved and it moves small-country shares in a known direction.
4. **The demographic-significance denominator** — ART births over all births, or ART's contribution to the TFR. §8 shows these differ materially because ART concentrates at older ages. A ruling is needed and A.12's arm must use the same one.
5. **Rate v5's claim as written, or amend the registry?** Drafted as written, following the D.3.c and A.12 precedent, with the "growing" clause reported as contradicted.

**Retrieval priorities, in order of damage.**

1. **Job A1, the counterfactual set — 2 of 14.** Everything in §7.1 and §10 is conditional on it. Eleven of the twelve missing are blocked-but-open: a browser, not a proxy.
2. **The three IVF-instrument first stages.** The best-identified estimates of this chapter's own parameter, currently reported as nuisance quantities in labour-economics papers.
3. **The 10–15 year egg-freezing return-rate study**, without which P5 has no verdict.

**Studies that do not exist and should.**

- **A population-scale comparison of births among treated and untreated subfertile couples**, with selection handled. The inputs exist; nobody has assembled them.
- **A decomposition of ART uptake into a postponement-induced component and an independent one.** Until this exists, every offset figure in this chapter and in A.12's ART arm is uncorrected for its own largest known bias.
- **A US access study whose exposure is employer coverage rather than state mandate.** Two thirds of the workforce is invisible to the mandate literature.

---

## 12. References

Full bibliography in `extraction/art-access-fertility-recovery-fulltext-screened.json` (33 full texts) and `literature/search-logs/art-access-fertility-recovery-cold-start-anchors.json` (21 verified anchors). Key records cited above: Lundborg, Plug & Rasmussen (*AER* 2017); Bitler & Schmidt (NBER 2011); Bundorf, Henne & Baker (NBER 2007); Dupree et al. (*J. Assist. Reprod. Genet.* 2025); Myers (*Israel J. Health Policy Res.* 2016); Šprocha et al. (*Scientific Reports* 2023); Burgio et al. (*PLoS ONE* 2026); Lazzari, Gray & Chambers (*Demographic Research* 2021); Sobotka et al. (*PDR* 2008); Leridon (*Human Reproduction* 2004); Habbema et al. (*Human Reproduction* 2015).

---

## Provenance and standing caveats

**This chapter is written on 33 of 131 wanted full texts (25%).**

**The findings that would survive full retrieval are** the units result (ART's contribution is a few percent of a TFR against a decline of about one child); the direction of the counterfactual bias (upward, unambiguously); the ERISA attenuation of every US mandate estimate; and the observation that the counting literature cites the counterfactual literature without using it. **The findings that might not are** the exact offset range 2.7%–11.8% (five settings, and the arm-1 evidence base could triple); the "measured and weak" verdict on the behavioural channel, which currently rests on one study; and the absence of any verdict on elective egg freezing, which is an artifact of retrieval rather than of the literature.

**Numbers taken from abstracts rather than full text:** the Denmark 4.2% share (quoted inside a retrieved NBER paper, not read in the original) and the Ukraine 1.6% share (English abstract of a Russian-language paper).

**The objection over which this chapter is written.** A reader may reasonably say that 33 of 131 is too thin to write on at all. The counter is that the chapter's central claim is about the *structure* of the literature — that it computes shares without counterfactuals — and that claim is established by the papers in hand rather than by their number; a further hundred accounting studies using the same estimator would strengthen it, not overturn it. The claims that genuinely need the missing retrieval are flagged inline, and the verdict is stated at the generous end of its range so that the corrections not yet made can only move it downward.

**Retrieval status:** 67 of the 98 missing records are blocked-but-open — an open-access URL exists and publisher bot defence blocks scripted access. A browser and no institutional access clears them. 31 need a library proxy. The paste-ready list is at `extraction/art-access-fertility-recovery-blocked-but-open.txt`.
