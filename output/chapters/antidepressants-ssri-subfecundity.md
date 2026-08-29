# Antidepressants and SSRI Subfecundity

**Category:** Biological
**Primary mechanism:** SSRIs impair sexual desire and function; impaired sexual function reduces intercourse; reduced intercourse reduces conception — so rising antidepressant prescribing lowers fertility without anyone wanting fewer children.
**Cross-references:** A.14 coital frequency and biological exposure (which owns link 3 of this chapter's chain) · D.3.a the mental-health epidemic (which owns the *condition* rather than its treatment, and whose effect on fertility is larger and better measured than this chapter's) · B.5 fetal loss (whose recuperation argument this chapter reuses from the opposite direction).
**Status:** TICK-066. Rewritten against `docs/chapter-template.md` on 2026-08-29; previous draft 2026-08-12. Demographic significance is computed and tested. Written on 6 of 20 wanted full texts (30%), of which 3 are extracted.

---

## 1. The claim

This chapter explores the effect of antidepressant use on fertility.

### 1.1 In plain terms

In plain terms: antidepressants very often reduce sexual desire and make sex harder. A lot more people take them than used to. The claim is that these two facts together have lowered the birth rate — people are having less sex, so fewer babies are being conceived, and nobody had to decide to have a smaller family.

The first fact is not in doubt. The drugs do this, it has been shown in careful trials, and the number of people taking them has risen steeply.

The trouble is getting from there to fewer babies, and it takes two more steps. Does having less desire actually mean having less sex? And does having less sex actually mean fewer children? Almost nobody has measured the first of those. And the second turns out to work against the idea: for couples trying to conceive, what matters is having sex at the right few days of the month, not how often — so a couple can have a good deal less sex and conceive just as fast.

There is also a timing problem that no amount of evidence can fix. The medicine most of this is about went on sale in 1988. By then, two thirds of the fall in birth rates being explained had already happened.

### 1.2 The claim precisely

The parameter this chapter estimates is the change in **completed fertility**, in births per woman, caused by antidepressant exposure, **after whatever recuperation follows discontinuation**, signed so that a negative value means fewer births.

The chapter is scoped to the **SDT** (the Second Demographic Transition, roughly 1965 onward), and within it to the **post-1988** period. **PM** (pre-modern) and **FDT** (the First Demographic Transition, roughly 1870–1965) have no cell: the exposure did not exist, and though tricyclics date from the 1950s, prescribing volumes were negligible and the period closes in 1965.

**The claim is a chain of three links, and the chapter's job is to price each step rather than assert the product:**

> antidepressant use → sexual dysfunction → reduced coital frequency → reduced conception

**B.7's structural difficulty is the mirror image of B.5's.** B.5 was defined by a *channel* whose drivers all belonged to other chapters. **B.7 is defined by a *treatment* — a specific, precisely dated, well-measured pharmaceutical exposure — whose *outcome* belongs to another chapter.** The medication's proximate effect is on sexual function; sexual function's effect on conception is A.14's; and the fertility quantity this review cares about sits two links further down. What B.7 owns is the drug and the first link.

**This is a behavioural parameter, and it has a deflator that behaves like an identity.** Write $p$ for the share of reproductive-age person-time under exposure and $\delta$ for the proportional reduction in the conception hazard while exposed. The product $p\delta$ is the share of conceptions displaced during exposure — **but a conception not achieved this month is not a birth forgone. It is a birth postponed**, and where the reproductive span does not bind it is recovered after discontinuation. At the central estimate a current user's per-cycle conception probability falls from 0.20 to 0.17, lengthening the mean wait by **0.88 months per attempt**. Two attempts cost about 1.8 months of a span running roughly 25 years.

Every estimate therefore carries an estimand level: **`HAZARD_DECREMENT`** (the effect on the per-cycle hazard or time-to-pregnancy — an input, not a fertility quantity, and an upper bound reported only as one) and **`TEMPO_ADJUSTED_QUANTUM`** (the effect on completed fertility after recuperation — the quantity the demographic-significance verdict requires). **The two are never pooled.**

**One channel escapes the deflator entirely**: exposure that changes whether a union forms or persists removes births rather than postponing them. **It is not deflated by recuperation, and it is the one for which the chapter has no evidence whatever.**

**Margin.** Predicted on the extensive margin of conception per cycle, which is why the deflator matters: a hazard decrement is a timing effect unless the span binds.

**The sign is not established, and v5's claim text assumes it.** Antidepressants impair sexual function and also treat a condition that impairs fertility through several channels. **The net effect of medicating an indicated person could run either way.** The screen turned up records pointing the other way: sexual function improving as depressive symptoms fall under escitalopram; psychiatric intervention raising pregnancy rates in infertile couples; imipramine restoring antegrade ejaculation; paroxetine improving sperm quality in a depressed animal model; and, in the one identified human estimate, **a point estimate above 1 for non-SSRI antidepressants.**

---

## 2. Theoretical mechanism

The claim is pharmacological and behavioural at once. SSRIs block serotonin reuptake; elevated serotonin damps the dopaminergic reward circuitry driving sexual motivation and interferes with the autonomic processes underlying orgasm. **These effects are not in dispute. What is in dispute is whether they aggregate into a fertility effect.**

| Link | Proposition | Records located | Best evidence | Rating |
|---|---|---|---|---|
| **1** | Antidepressant use → sexual dysfunction | **71** | Double-blind placebo-controlled fixed-dose trials on ejaculation; a prospective multicentre incidence study of 1,022 outpatients using direct questioning | **MODERATE** |
| **2** | Sexual dysfunction → reduced coital frequency | **1** | An interpretive-phenomenological interview study of **nine women**, plus one mediation proportion (0.17) computed for *depression* rather than for medication | **VERY LOW** |
| **3** | Reduced coital frequency → reduced conception | **12** | Day-specific conception probabilities; joint models of intercourse behaviour and fecundability | **MODERATE — and it cuts against the claim** |

**A chain is no stronger than its weakest link, and the composite claim therefore rates far below link 1.** This matters practically: a chapter that rated the evidence it *has* rather than the evidence the claim *needs* would return a confident rating for a proposition nobody disputes and would tell a reader nothing about fertility.

**Link 3 argues against the hypothesis rather than for it.** Conception probability per cycle is close to flat above two or three well-timed acts of intercourse, and for couples trying to conceive the binding behavioural factor is **timing, not frequency**. A desire decrement must therefore be very large before it moves the conception hazard at all in the population that is trying. Where B.7 could still bite is on people *not* deliberately trying — whether a partnership forms, persists, or produces an unplanned conception — and **that is a different mechanism from the one the hypothesis states**, with no evidence behind it.

**What would make the hypothesis wrong.** It is wrong if the desire decrement does not translate into reduced intercourse (link 2, unmeasured); if reduced intercourse does not reduce conception at realistic frequencies (link 3, which says it largely does not); or if the medication's decrement is offset by treating the indication. **All three are live.**

---

## 3. Search strategy

Reproducible from `source/build/goldset/123_b7_recon_probe.py` through `131_b7_extract_retrieved.py`. Eight boundary walls and the estimand taxonomy were **written and frozen before the search ran**.

**A 54-probe reconnaissance pass established the shape of the problem in advance** (zero failed requests, so zero-hit counts are genuine absences). Antidepressants paired with pregnancy return roughly 5,650 records; **paired with any fertility-rate term, 48** — and every one of the most-cited among those 48 is a pregnancy-safety study that happens to use the phrase "birth rate". **The seam is not thin; it is close to absent.** Probes for aggregate antidepressant-and-births work returned 35 records with nothing on topic.

**Twenty-four anchors through four gates**: existence, version-of-record, book-canon, and a **shadow-record gate built for this chapter**. A shadow record is a real, separately-indexed work whose title is the target title plus a leading qualifier — `Editorial Comment to X`, `Faculty Opinions recommendation of X`, `Re: X`, `Expression of Concern: X` — and **it defeats the other three gates by construction**. Five fired. The sharpest case: neither index copy of the 1,022-patient incidence study carries a DOI, while the Faculty Opinions comment on it does, **so a DOI-preferring resolver without this gate would anchor the study to a one-paragraph post-publication note.** One shadow was an Expression of Concern on a highly cited mechanism study, carried forward as an integrity flag rather than discarded.

**The on-topic diagnostic is the chapter's thesis stated as a number.** The share of each seed's citation cloud carrying any fertility quantity runs **51–68% for the primary and mechanism seeds and 0.7–2.1% for the link-1 seeds.** The enormous literature establishing that antidepressants impair sexual function almost never touches fertility.

---

## 4. PRISMA flow

| Stage | Records |
|---|---:|
| Cold-start anchors sourced / verified | 24 / 22 (2 carry no DOI by nature) |
| One-hop citation frame | 7,174 |
| After collapsing version duplicates | 6,798 |
| **Screened at title and abstract** | **420** |
| — excluded (`OFF_*`) | 219 |
| — retained, multi-channel (tier 1) | 116 |
| — retained, single-channel (tier 2) | 79 |
| — uncertain, retained for audit (tier 3) | 6 |
| **Primary cell** | **20** |
| Link-support stream (links 1–3) | 84 |
| Mechanism, parameter, baseline, measurement, theory | 92 |
| Held for full-text adjudication | 5 |
| **Full text obtained, primary cell** | **6 of 20** |
| **Studies extracted** | **3** |

Three features change how the chapter should be read.

**First, the residual is characterised rather than implied.** 6,378 records went unscreened, of which **5,457 carry no fertility-axis term at all.**

**Second, both records held for full-text adjudication resolve *out*, and neither could have been settled from its abstract.** The vilazodone comparison is in **male rats**; the paternal-SSRI cohort of 13,547 exposed children measures outcomes **in the offspring**. The first is instructive: its abstract describes a comparison of antidepressants on sexual behaviour — precisely the link-1 evidence this chapter is short of — **and a screen that inferred species from topic would have admitted it.**

**Third, fourteen primary-cell records remain unretrieved** and are recorded as pending in the risk-of-bias table rather than omitted from it.

---

## 5. The ideal design

Written before the literature was read, so §6 can be measured against a fixed yardstick.

### 5.1 The ideal estimand

The change in **completed fertility**, in births per woman, caused by antidepressant exposure among **women** of reproductive age, **holding the indication fixed** — that is, comparing medicated to unmedicated people with the same underlying depression — and **observed past discontinuation** so that recuperation is measured rather than assumed.

Three clauses carry it. *Holding the indication fixed* is the boundary against D.3.a and the domain on which every retrieved study fails. *Women* because the hypothesis locates the population effect there and the only identified estimate is male. *Past discontinuation* because §1.2 shows the hazard decrement is a timing effect unless the span binds, so a design ending at conception measures `HAZARD_DECREMENT` and not the estimand.

### 5.2 The design that would identify it

**Source of variation.** Something that moves prescribing without moving depression. Three candidates: a **formulary or reimbursement change** making one drug class cheaper; **prescriber-preference variation** — the physician a patient happens to see — used as an instrument, the standard design in pharmacoepidemiology; or a **guideline change** shifting first-line treatment for a defined severity band.

**Comparison group.** People with the same diagnosis and severity, unexposed or exposed to a comparator drug. **An active comparator is the minimum**, because unmedicated depression is not a valid counterfactual.

**Identifying assumption.** The instrument moves exposure and not severity. Falsifiable: balance on pre-period severity scores and healthcare utilisation; a placebo on conditions the drug does not treat.

**Estimating equation.** A two-stage design on **completed fertility at 45**, with the per-cycle hazard reported as a first stage, and **a specification distinguishing postponement from foregone births** by following exposed cohorts past discontinuation.

**Data required.** Prescription registry linked to birth registry with diagnosis and severity, followed to completed fertility — which the Nordic registers can supply.

**Sample size.** With ~6% exposed person-time and an FR near 0.85, detecting a `TEMPO_ADJUSTED_QUANTUM` effect requires population-register scale. This is not a survey-cohort question.

**What the ideal design excludes.** A large registry study of medicated versus unmedicated women adjusted for age, income and education — **however large.** The adjustment set does not contain the reason for the prescription. **Sample size is close to uninformative about study worth in this chapter**, and the extraction and risk-of-bias stages are built to say so.

### 5.3 Distance from the ideal

| Study | Indication held fixed? | Outcome a birth? | Women? | Past discontinuation? | Distance |
|---|---|---|---|---|---|
| **Yland et al. 2022** | **Partly** — adjusts for depressive symptoms | Fecundability, not births | **No — 2,398 men** | No | **Closest, and the only one adjusting for the indication** |
| Alsabhan et al. 2024 | No | No — semen parameters | No | No | Far |
| Gong et al. 2026 | No | No — reporting signal | No | No | Far |
| The 71 link-1 records | Trials, so yes | **No — sexual function** | Mixed | n/a | Wrong outcome by design |
| The single link-2 record | n/a | No — nine interviews | Yes | n/a | **The chain's weakest link, and this is all of it** |

**No study implements the ideal design, and the gap is specific: not one study estimates a fertility outcome in women with the indication held fixed.**

**Every retrieved estimate is Serious or Critical on ROBINS-I, and the binding domain is the same in all of them.** Nobody has an active comparator, a within-person contrast, or an instrument for prescribing, so **the medication cannot be separated from the reason it was prescribed.** This is not a criticism of any individual study; it is the state of the literature.

**And the literature says so itself.** Yland and colleagues state in their own introduction that no studies had evaluated the relationship between psychotropic medication use and directly measured fertility outcomes — **an independent confirmation, from inside the literature, of what the screen found from outside it.**

---

## 6. Included studies

Three studies extracted, five effect rows.

| Study | Design | Country | Exposure | Outcome | Effect | RoB |
|---|---|---|---|---|---|---|
| Yland et al. 2022 | Prospective preconception cohort, 2,398 men, 2013–2020 | US/Canada | Current SSRI use (4.3%) | Fecundability | **FR 0.85 [0.65, 1.12]** | Serious |
| Yland et al. 2022 | Same cohort | US/Canada | Other antidepressants (2.0%) | Fecundability | **FR 1.03 [0.71, 1.48]** | Serious |
| Yland et al. 2022 | Mediation within cohort | US/Canada | Depressive symptoms | Share mediated by intercourse frequency | 0.17 | Serious |
| Alsabhan et al. 2024 | Retrospective clinic comparison, 29 exposed | Saudi Arabia | SSRI use | Sperm liquefaction, motility, viscosity, count | Null on all four (p = 0.10 / 0.17 / 0.16 / 0.069) | Critical |
| Gong et al. 2026 | Pharmacovigilance disproportionality, FAERS + EudraVigilance | International | Multiple drugs | Male-infertility reporting signal | Signal present; magnitude not estimable | Critical |

Restricting Yland to the incident attempt period attenuates the SSRI estimate to **0.91 [0.66, 1.26]**.

### 6.1 The naive estimator

**What is the naive estimator?** Compare fertility between people taking antidepressants and people not taking them.

**It is confounded by the indication, and the confounding is larger than the effect being sought.** In the Norwegian population register, depression through the reproductive period corresponds to completed fertility of **1.34 births per woman against 1.60** for women with none of the disorders studied, and **0.90 against 1.41** for men. **B.7's claim is that the drug adds a decrement on top of that.** The only estimate of the addition is an interval spanning the null.

The bias runs toward the hypothesis and it is not small: the untreated comparison group differs on the exact characteristic that independently lowers fertility.

**How many included studies escape it? None.** One adjusts for depressive symptoms, which is the best available and is not an active comparator.

### 6.2 The transmission ledger

| Stage | Question | Sign |
|---|---|---|
| Prescribed → exposed person-time | ~6% of reproductive-age person-time | Attenuates |
| Exposed → sexual dysfunction | Link 1, well established | **Holds** |
| Dysfunction → less intercourse | Link 2 | **One record: nine interviews** |
| Less intercourse → fewer conceptions | Link 3: hazard is flat above 2–3 well-timed acts; timing dominates frequency | **Attenuates severely; may be zero** |
| Conception delayed → birth forgone | Only where the span binds; 0.88 months per attempt against ~25 years | **Attenuates to near zero** |
| Indication treated → fertility rises | The offsetting channel | **May reverse** |

Every stage after link 1 either attenuates severely, is unmeasured, or may reverse.

---

## 7. Quantitative synthesis

### 7.1 The answer in plain terms

There is one study in the world that measures whether taking these drugs is followed by having fewer children while also accounting for the depression itself. It followed 2,398 men trying to conceive. It found they took somewhat longer, but the range of possibilities it could not rule out includes no effect at all — and for the non-SSRI drugs the best guess pointed the other way.

That is the whole quantitative basis of the hypothesis. One study, one country, one sex, and a range that includes zero.

The step in the middle of the argument — that less desire means less sex — has been studied once, in an interview study of nine women.

### 7.2 The estimate

**No pooling.** `PROTOCOL.md` §5.9 directs meta-analysis at three or more studies with extractable effects, and **the count is met only by counting rows rather than studies.** A fecundability ratio, a set of semen-parameter p-values and a pharmacovigilance signal share no estimand, no outcome scale and no population. A pooled figure would have no referent.

**The single identified estimate is FR 0.85 [0.65, 1.12].** It includes the null.

**Publication-bias diagnostics cannot be computed on one estimate.** What can be said is qualitative and points one way: the positive semen-parameter findings come from small clinical series, the largest null the search located sits in a general urology journal, and the one systematically collected fertility estimate spans the null.

---

## 8. Demographic significance

The phenomenon to be explained is measured in whole children — the post-1988 OECD decline is 0.537 births per woman; this mechanism offers, after recuperation, about 0.0004 births per woman.

Computed by `source/analysis/b7_demographic_significance.py` (20 tests passing).

**The timing wall comes first, because it bounds everything after it — and it is a `PROTOCOL.md` §4.2.1 denominator question.**

| Quantity | Value |
|---|---|
| OECD TFR, 1965 | 3.134 |
| OECD TFR, 1988 (fluoxetine market entry) | 2.014 |
| OECD TFR, 2024 | 1.478 |
| Total decline | 1.656 births (52.9%) |
| **Share complete before the exposure existed** | **67.6%** |
| **Decline available to B.7** | **0.537 births (26.7%)** |

**Two thirds of the decline this hypothesis is assigned to explain was over before its cause existed.** §4.2.1 requires the denominator to be the phenomenon's full window — but for a late-arriving exposure, the full SDT window credits the hypothesis with variation that predates its own existence. **This chapter uses the post-1988 denominator and reports the full-window figure alongside**, which is the more demanding choice: the smaller denominator makes any given effect look *larger*. **The problem generalises to every late-arriving exposure in this review** and is raised as PI call 1 rather than settled here.

At central parameters — 6.0% of reproductive-age person-time exposed, FR = 0.85, and a recuperation deflator τ = 0.024 **derived from a slack model rather than assumed**:

| Level | Share of births | Share of the post-1988 decline |
|---|---|---|
| `HAZARD_DECREMENT` (no recuperation) | 0.90% of conceptions | **3.4%** |
| **`TEMPO_ADJUSTED_QUANTUM`** (the verdict) | 0.02% of births | **0.08%** |

**The most favourable reading, computed rather than dismissed.** A negative verdict is worth nothing unless the corner of the parameter space most favouring the hypothesis has been calculated and stated. Taking the highest plausible exposure prevalence (13%), the strong end of an interval that includes the null (FR = 0.65), and assuming a delayed conception is simply a lost birth, the share reaches **17.1%**. **The hypothesis crosses into significance only if all three are granted at once**, and the argument against the third is the same one B.5 makes against reading $(1-p)$ as an effect on completed fertility — which does not depend on the other two.

**The endogeneity check** is unusually clean: antidepressant prescribing is not plausibly caused by the fertility decline, so the feedback problem afflicting most chapters does not arise here.

**What the computation cannot do.** The effect size is one interval from one cohort of 2,398 men, and it includes the null. **The arithmetic is robust; the input is not.** No female-side fecundability estimate adjusted for the indication was located anywhere in the frame, **so the parameter carrying this entire computation is male and is being applied to a population effect the hypothesis locates in women.** Slope sufficiency is "insufficient" and the conditional R² benchmark is not computable: there is no panel of antidepressant prevalence against TFR, because nobody has built one.

### 8.1 Pre-modern fertility variation

For pre-modern variation, the verdict is NOT ASSESSED, because the phenomenon is out of scope for this hypothesis in the registry: the exposure did not exist.

### 8.2 First Demographic Transition

For the First Demographic Transition, the verdict is NOT ASSESSED, on the same ground. Tricyclics date from the 1950s, but prescribing volumes were negligible and the period closes in 1965.

### 8.3 Second Demographic Transition

For the Second Demographic Transition, the verdict is NEGLIGIBLE, because the tempo-adjusted effect is 0.08% of the post-1988 decline, and even the no-recuperation upper bound is 3.4%.

Two things qualify it, in opposite directions. **The most favourable corner of the parameter space reaches 17.1%**, which is MINOR — but it requires the highest plausible prevalence, the strong end of an interval containing the null, *and* the assumption that a delayed conception is a lost birth, simultaneously. And **the input is one male cohort**, so the precision of 0.08% is spurious even though the arithmetic is not.

---

## 9. GRADE rating

Assigned to the **composite claim** — that antidepressant exposure reduces fertility — with the three links rated separately so a reader can see where the chain breaks. **Rating link 1 and reporting that rating would credit the hypothesis with the quality of evidence for a proposition it does not need to establish.**

| Target | GRADE | Downgrades | Demographic significance |
|---|---|---|---|
| PM | **No evidence** | Out of scope in the registry; the exposure did not exist. | NOT ASSESSED |
| FDT | **No evidence** | Same. | NOT ASSESSED |
| Link 1 (drug → dysfunction) | **MODERATE** | Placebo-controlled fixed-dose trials and a prospective multicentre incidence study. Not the claim. | n/a |
| **Link 2 (dysfunction → intercourse)** | **VERY LOW** | **One record: nine interviews.** The mediation proportion available is for depression, not medication. | n/a |
| Link 3 (intercourse → conception) | **MODERATE**, and it cuts against | Well established that timing dominates frequency above 2–3 well-timed acts. | n/a |
| **SDT, composite claim** | **VERY LOW** | *Imprecision*: one estimate, spanning the null, from one cohort. *Indirectness* (two levels): male, and fecundability rather than births. *Risk of bias*: every retrieved study Serious or Critical, all binding on confounding by indication. *Inconsistency*: the non-SSRI point estimate is above 1. | NEGLIGIBLE |

---

## 10. Verdict

Antidepressants demonstrably impair sexual function, prevalence has risen a great deal, and **the inference from those two facts to a population fertility effect is where the hypothesis fails.** It fails at a specific joint, for a measurable reason, and not for want of looking.

**The one number to carry away: one.** That is the number of records in the entire frame speaking to link 2 of the three-link chain — a qualitative interview study of nine women. **The step the hypothesis actually needs is the one nobody has measured.**

Three qualifications belong inside this verdict.

**Two thirds of the decline was over before the cause existed.** Fluoxetine reached the US market in 1988, by which point OECD fertility had already fallen from 3.13 to 2.01. Against the post-1988 remainder, the tempo-adjusted contribution is **0.08%**.

**The single identified fertility estimate includes the null**, comes from 2,398 men, and is being applied to a population effect the hypothesis locates in women. No female-side estimate adjusted for the indication exists anywhere in the frame.

**The condition has a larger effect than the medication and is measured far better.** Depression through the reproductive period corresponds to 1.34 births per woman against 1.60, and 0.90 against 1.41 for men. The claim is that the drug adds a decrement on top of that; the only estimate of the addition spans zero.

**What would change it:** the design in §5.2 — prescriber-preference or formulary variation, an active comparator, women, completed fertility, followed past discontinuation. The Nordic registers can supply the data. Failing that, **even a single well-designed study of link 2** would tell us more than the 71 link-1 records already do.

---

## 11. Open questions

**PI calls required.**

1. **What denominator applies to a late-arriving exposure?** 67.6% of the SDT decline predates fluoxetine. Scoring against the full window credits the hypothesis with variation predating its cause; scoring against the post-1988 remainder uses a smaller denominator that flatters any effect. This chapter does the latter and reports both. **It generalises to every late-arriving exposure in the review and belongs in `PROTOCOL.md` §4.2.1.**
2. **Should the union-formation channel be scoped in?** Exposure that changes whether a partnership forms removes births rather than postponing them, escapes the recuperation deflator entirely, and has no evidence behind it. It is a different mechanism from the one v5 states.
3. **The Expression of Concern** flagged by the shadow-record gate on a highly cited mechanism study is carried as an integrity flag and needs a ruling.

**Evidence and retrieval priorities.**

4. **Any study of link 2.** The chain's weakest link has one record.
5. **A female-side fecundability estimate adjusted for the indication.** The entire computation currently rests on a male parameter.
6. Retrieve the 14 outstanding primary-cell records; extend the screen past 420 of 6,798.
7. Build the antidepressant-prevalence-against-TFR panel that would make the R² benchmark computable. Nobody has one.

**Studies that do not exist and should.** The design in §5.2. Also, and more cheaply: a single mediation study measuring whether SSRI-induced dysfunction actually reduces intercourse frequency, in more than nine people.

---

## 12. References

Works named above are identified by DOI in `literature/search-logs/antidepressants-ssri-subfecundity-cold-start-anchors.json` and the screen tier files; extracted studies in `extraction/antidepressants-ssri-subfecundity-effects.csv`.

---

## Provenance and standing caveats

This chapter is written on 6 of 20 wanted full texts (30%), of which 3 are extracted.

**The findings that would survive full retrieval are the structural ones**: the timing wall (67.6% predates the exposure), the chain's shape (71 records on link 1, one on link 2), and the on-topic diagnostic (0.7–2.1% of link-1 citation clouds carry any fertility quantity against 51–68% for the primary seeds). None depends on which of the remaining 14 records is read. **The finding that might not is the magnitude**, which rests on one interval from one male cohort; a female-side estimate adjusted for the indication could move it substantially in either direction, and none exists.

**Objection over which this chapter was written.** None recorded from the PI. Three calls are open, one of which — the denominator for a late-arriving exposure — determines how §8.3 should be read.

**Numbers sourced from abstracts rather than full text.** The 14 unretrieved primary-cell records are characterised by abstract only and are recorded as pending in the risk-of-bias table rather than omitted from it. Both records held for full-text adjudication resolved *out* on retrieval, and neither could have been settled from its abstract.

**Figures not derived from project data.** The OECD TFR series in §8 is quoted from OECD published figures rather than computed here.

**A method result worth carrying to other chapters.** The **shadow-record gate** — rejecting `Editorial Comment to X`, `Faculty Opinions recommendation of X`, `Re: X`, `Expression of Concern: X` — fired five times and defeats existence, version-of-record and book-canon gates by construction. In the sharpest case the target study carries no DOI in either index copy while the Faculty Opinions comment on it does, so a DOI-preferring resolver would have anchored a 1,022-patient incidence study to a one-paragraph note.

**Generated inputs.** `source/analysis/b7_demographic_significance.py` (20 tests passing) → `output/tables/antidepressants-ssri-subfecundity-demographic-significance.md`. Extraction, risk of bias, RA gate, routing resolutions and retrieval logs in `extraction/antidepressants-ssri-subfecundity-*`. Scope, walls and estimand taxonomy frozen before the search in `literature/search-logs/antidepressants-ssri-subfecundity-search-scope.md`. Pipeline `source/build/goldset/123_b7_*` through `131_b7_*`.
