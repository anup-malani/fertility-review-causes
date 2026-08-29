# Old-Age Security and Pension Crowd-Out of Fertility

**Category:** Economic
**Primary mechanism:** When something other than children will support a person in old age, the private return to an additional child falls, and fertility falls with it.
**Cross-references:** D.1.b (Caldwell wealth flows and westernization) shares this chapter's intergenerational-transfer theory and must not double-count it. A.23 (co-residence with parents and delayed household formation) treats co-residence as a household-formation cost; here the same arrangement is an old-age-support asset, and the boundary is the direction of the transfer. C.3.g (student debt and household formation) shares the saving-instrument margin.
**Status:** TICK-019. Rewritten against `docs/chapter-template.md` on 2026-08-29. Not PI-reviewed in this form; the previous draft (2026-07-11) was benchmarked against `old-age-security-pension-crowdout-pi-review v4.md`. Written on 13 of 13 wanted full texts (100%), drawn from 1,860 machine-screened records whose human screen has 10 recorded decisions.

---

## 1. The claim

This chapter explores the effect of non-child old-age security on fertility.

### 1.1 In plain terms

In plain terms: in much of the world, and through most of history, grown children were what a person lived on once they were too old to work. Children fed their parents, housed them, and nursed them. Having several was a way of making sure someone would still be there. The claim in this chapter is that once something else will do that job — a government pension, money in a bank, an insurance policy — a person no longer needs children for it, and so has fewer of them.

That single idea is carried through the whole chapter. When the chapter later asks whether the claim is true, it is asking whether people who were handed one of those substitutes went on to have fewer children than otherwise similar people who were not.

There is a second, quite different idea that also connects pensions to births, and it pushes the opposite way. When a pension lets a grandparent stop working, that grandparent becomes available to look after grandchildren, which makes having a child easier for the adult son or daughter. On this second idea, a pension makes births *more* likely, not less. The chapter keeps the two apart throughout and never adds them together, because they are answers to different questions.

### 1.2 The claim precisely

The parameter this chapter estimates is the change in a woman's **completed fertility** (the total number of children she has actually borne by the end of her childbearing years) caused by an exogenous increase in non-child old-age security, measured in births per woman, signed so that a negative value means less fertility after more old-age security.

The chapter rates the claim separately against the review's three target phenomena, abbreviated throughout as **PM** (pre-modern fertility variation — differences in fertility between populations before roughly 1870), **FDT** (the First Demographic Transition, the sustained fall in fertility across Europe and its offshoots from roughly 1870 to 1965) and **SDT** (the Second Demographic Transition, the further fall to below-replacement levels from roughly 1965 onward). **Below replacement** means a fertility level under about 2.1 children per woman, the level at which a population reproduces itself.

The registry entry reads: *non-child old-age security reduces the need to have children as retirement insurance*. That wording runs two separable sub-claims together, and the chapter evaluates them separately:

- **Sub-claim A — the old-age-security motive.** An exogenous increase in non-child old-age security reduces fertility by lowering the retirement value of a child. Predicted sign: negative.
- **Sub-claim B — the grandparental-childcare channel.** A change in pension or retirement rules changes a grandparent's availability to supply childcare, which changes the adult child's fertility. Predicted sign: positive in the availability direction. This is not the registered claim. It appears here because the registered claim's own instrument — pension policy — moves it too, so any study of pension policy and fertility is estimating a mixture unless the design separates them.

The counterfactual for sub-claim A is a ceteris-paribus perturbation: hold income, mortality, child costs and marriage patterns fixed, and add a credible non-child claim on old-age resources. No study in the evidence base delivers exactly that; every one of them moves old-age security together with something else, which is the indirectness this chapter downgrades for in §9.

**This is a behavioural parameter, not an identity.** There is no accounting relation here that must hold. The mechanism can be false at every link, and that is why it needs studies rather than arithmetic. This matters because it distinguishes the chapter from mechanisms like A.12, where an identity arm exists and needs no evidence.

**Margin.** Sub-claim A is predicted to move the intensive margin — a level change in how many children a woman who is having children has — because it changes the return to an *additional* child. Several included studies nonetheless measure an extensive-margin outcome (whether a birth occurred in a window), and §7 keeps those apart.

---

## 2. Theoretical mechanism

In the reader's own vocabulary: a child is partly a durable asset that pays a stream of old-age consumption. Old-age security is a substitute asset. Introduce the substitute and the shadow price of the child-as-asset falls, so demand for the asset falls. The prediction is a pure substitution effect on the asset-demand margin.

Two complications make the prediction less clean than that sentence suggests.

First, a pension is also income. A tax-financed pay-as-you-go system (a pension system in which today's workers' taxes pay today's retirees' benefits) transfers resources across cohorts, and the income effect on the recipient generation runs the other way — richer households can afford more children. The net sign is therefore theoretically ambiguous, and which effect dominates depends on whether the recipient is the potential parent or the potential grandparent. The classic statements — Neher (1971), Willis (1980), Nugent (1985) — assume the substitution effect dominates. Ehrlich and Lui (1991), Nishimura and Zhang (1992), Sinn (2004) and Boldrin, De Nardi and Jones (2015) formalise the conditions.

Second, the transfer does not disappear when a state pension arrives; it moves from a household contract to a state contract. That reframing is Caldwell's (1976), and it is why D.1.b overlaps this chapter. The fertility effect comes from the change in the *private* return to the parent, not from the disappearance of the transfer.

**What would make the hypothesis wrong.** The hypothesis is wrong if households that receive a credible non-child claim on old-age resources do not reduce their fertility relative to comparable households that do not. Concretely, three observations would each count against it: pension expansions that leave fertility unmoved in settings where children plainly still insure old age; pension retrenchment that fails to raise fertility where the motive is supposed to be live; and evidence that the households responding are responding to the income rather than to the insurance. The third is the hardest to rule out and no included study rules it out.

---

## 3. Search strategy

The search ran the project's standard two-stage machine screen over an OpenAlex-derived frame, followed by a human title/abstract screen and full-text retrieval. The logs are in `literature/search-logs/old-age-security-pension-crowdout-*`.

Four walls define the boundary of the chapter, with their enforceability declared in advance:

| Wall | Rule | Enforceable at title/abstract? |
|---|---|---|
| **W1 Outcome** | The outcome must be fertility — a birth, a count of children, or a fertility rate. Savings, schooling, coresidence and elderly health are chain links, not outcomes. | Yes |
| **W2 Direction** | Old-age security must be the treatment and fertility the outcome. Studies in which fertility causes insurance take-up are mechanism evidence, not effect estimates. | Yes |
| **W3 Channel** | The estimate must be attributable to the old-age-support motive rather than to grandparental childcare. | **No — declared unenforceable in advance.** Both channels are the same treatment (pension policy) with the same outcome (a birth). Which channel a paper identifies is visible only in the design, and often only in the paper's own interpretation section. This wall is enforced at extraction, not at screening, and §7 keeps two separate cells because of it. |
| **W4 Exogeneity** | The variation in old-age security must come from something other than the fertility decline itself. | No — requires reading the identification section. |

**Boundary rulings against neighbouring hypotheses.** Against D.1.b (Caldwell): a study is this chapter's if its treatment is a specific old-age-security instrument, and D.1.b's if its treatment is the direction of net intergenerational flows in general. Against A.23 (co-residence): co-residence that supports the *parent* is this chapter's; co-residence that delays the *adult child's* household formation is A.23's. Against C.3.g (student debt): a saving instrument that moves resources into old age is this chapter's; one that moves them across early adulthood is C.3.g's.

---

## 4. PRISMA flow

The **PRISMA** flow (the reporting standard for systematic reviews, which requires the count of records surviving each stage of screening to be stated) for this hypothesis:

| Stage | Records |
|---|---:|
| Retrieved into the frame | 6,400 |
| Machine-screened, stage 1 (Haiku) | 6,400 |
| Escalated to stage 2 (Sonnet) | 2,763 |
| Machine verdict RELEVANT | 941 |
| Machine verdict UNCERTAIN | 919 |
| Machine verdict NOT_RELEVANT | 4,540 |
| Passed to human title/abstract screen (RELEVANT + UNCERTAIN) | 1,860 |
| **Full-text decisions on record** | **10** |
| PDFs held for the hypothesis | 44 |
| Studies in the extraction table | 13 |
| Cell A studies with extracted effects | 9 |

Three features of this funnel change how the chapter should be read.

**First, the largest attrition in the review is undocumented.** 1,860 records passed the machine screen; `old-age-security-pension-crowdout-fulltext-screen.csv` records ten decisions. The step that took the evidence base from 1,860 to 13 has no log. The 13 studies are defensible individually — they are the well-known papers in this literature — but the chapter cannot presently demonstrate that they are the *right* 13, and a reader should treat the included set as an expert-curated sample rather than as the output of a reproducible screen.

**Second, the machine screen was very uncertain.** 919 UNCERTAIN against 941 RELEVANT means the screen was close to a coin flip on half the records it did not reject. That is the signature of a boundary the screening rubric could not see — which is exactly what Wall 3 predicted in advance.

**Third, 44 PDFs are held and 13 studies extracted.** The gap of 31 is not accounted for anywhere in the extraction table.

---

## 5. The ideal design

Written before the literature was read, so that §6 can be compared against a fixed yardstick rather than against the best paper that happens to exist.

### 5.1 The ideal estimand

The change in completed fertility, in births per woman observed at age 45, caused by a **10-percentage-point rise in the old-age income replacement rate**, among women aged 20–35 at the time of exposure, in a setting where formal pension coverage was previously near zero and adult children were the principal source of old-age support.

The dose unit is the point of this specification. A replacement rate is comparable across countries and eras, is the quantity in which historical pension expansion is actually recorded, and can therefore be multiplied by an observed historical change to produce a decomposition share. "Exposure to a pension expansion" cannot. §8 shows that this single missing unit is what makes the chapter's demographic significance uncomputable, and §5.3 shows the gap was foreseeable without reading a single paper.

### 5.2 The design that would identify it

**Source of variation.** A legislated pension expansion whose eligibility is assigned by a rule orthogonal to fertility: a birth-date cutoff, an occupational-category boundary, or a staggered geographic rollout whose sequence is fixed administratively — by pre-existing registry capacity, say — rather than by local demographic conditions. Administrative sequencing matters because a rollout ordered by local need is ordered partly by local fertility.

**Comparison group.** Women just outside the eligibility rule: born weeks later, in the adjacent occupational category, or in a district scheduled for the following wave.

**Identifying assumption.** Absent the reform, completed fertility either side of the cutoff would have evolved in parallel. Falsifiable three ways: pre-reform cohorts either side of the cutoff should show no discontinuity; placebo cutoffs at non-reform dates should be null; and the density of the running variable should be smooth at the threshold.

**Estimating equation.** A cohort or birth-date regression discontinuity — or an event study for a staggered rollout, with a stated parallel-trends window — on completed fertility at 45, reported alongside its first stage: the replacement rate actually received.

**Data required.** An administrative birth registry linked to pension records, with a panel long enough to observe exposure at 20–35 and fertility at 45. That is a minimum of **25 years** of linked data, which is the binding constraint on this design and the reason it is rare.

**Sample size.** To detect 0.10 births per woman at 80% power requires about **2,650 women per arm**; to detect 0.05, about **10,600 per arm**. The pooled summary this chapter reports, 0.068, would need roughly **5,700 per arm**. Survey panels of the size used in this literature cannot do this; administrative data can.

### 5.3 Distance from the ideal

| Study | Exposure: dose in replacement-rate units? | Outcome: completed fertility at 45? | Horizon ≥25 yrs? | Assignment: rule-based, orthogonal? | Distance |
|---|---|---|---|---|---|
| Danzer and Zyska | No — expansion and generosity, not a replacement rate | **Yes** | **Yes** (1981–2014) | **Yes** — rural expansion, DiD/IV/event study | **Closest** |
| Rossi and Godard | Partial — a dose, but per thousand rand, not transportable | **Yes** | Near (1990–2012) | **Yes** — region × cohort exposure | Close |
| Zelu et al. | No — Act 766 coverage extension | No — pregnancy in last 12 months | Partial | Yes — public/private DiD | Not extracted |
| Shen et al. | No — individual participation, endogenous | Partial — number of children, not to 45 | **No** (4 years) | Partial — DiD, PSM and IV mixed | Far |
| Billari and Galasso | No — a pension cut, undosed | **No** — births in a 6-year window | **No** (6 years) | Partial — worker-status discontinuity | Far |
| Han et al. | **No** — care insurance, a different margin from pension income | No — birth in past year | No | Yes — pilot DiD | Far |
| Guinnane and Streb | No | No — crude birth rate, aggregate | Yes | Partial — regional/professional exposure | Far |
| Fenge and Scheubel | Partial — share insured, an aggregate rate | No — crude marital birth rate | Yes | **No** — cross-province panel | Far |
| Galofré-Vilà | **No** — bundled social spending | **Yes** — children ever born | Yes | **No** — cross-state panel | Far |
| Basso et al. | No — presence of a bank | No — child–woman ratio | **No** — single year, 1850 | **No** — cross-section | **Farthest** |

**No study implements the ideal design, and none is close on the dimension that matters most.** Zero of ten report the treatment in a dose unit that could be applied to a historical change in old-age security. Danzer and Zyska match on outcome, horizon and assignment and still cannot supply a replacement rate; Rossi and Godard have a dose denominated in Namibian currency, which cannot be transported anywhere.

That is the chapter's central finding, and §5.1 predicted it before the literature was opened. The consequence is not that the evidence is weak — several of these designs are good — but that **a decomposition share cannot be computed from any of them**, which is why §8 reports break-evens instead of shares and why §11 item 1 asks whether the pooled summaries should exist at all.

---

## 6. Included studies

| Study | Setting and period | Treatment | Outcome | Design | Cell | Target |
|---|---|---|---|---|---|---|
| Danzer and Zyska (2023) | Brazil, 1981–2014 | Rural pension expansion and generosity | Newborn under one; completed fertility | DiD, IV, event study | A | FDT\|SDT |
| Rossi and Godard (2022) | Namibia, 1990–2012 | Social-pension extension | Probability of birth; completed fertility | DiD on region × cohort exposure | A | FDT |
| Billari and Galasso (2009) | Italy, 1998–2004 | Pension-wealth *cuts* | Births after reform; additional birth | Natural experiment by worker status | A | SDT |
| Shen, Zheng and Yang (2020) | China, 2010–2014 | New Rural Pension Scheme | Number of children; second birth | DiD, PSM, FE, IV | A | SDT (policy-constrained) |
| Han, Tao, Wang and Zhang (2025) | China, 2012–2020 | Long-term-care insurance pilots | Birth in past year; intended children | DiD | A | SDT (policy-constrained) |
| Guinnane and Streb (2021) | Prussia, 1881–1910 | Bismarck social insurance | Births; crude birth rate | Historical quasi-experimental panel | A | FDT |
| Fenge and Scheubel (2017) | Imperial Germany, 1895–1907 | Bismarck pension insurance | Crude marital birth rate | Historical regional panel, 23 provinces | A | FDT |
| Basso, Bodenhorn and Cuberes (2014) | United States, **1850** | Presence of a bank in the county | Child–woman ratio; crude birth rate | **Single-year cross-county regression** | A | PM\|FDT |
| Galofré-Vilà (2023) | United States, 1940–1960 | State social spending under the 1935 SSA | Total fertility rate; own children under five; children ever born | Historical cross-state panel | A | FDT |
| Zelu, Iranzo and Pérez-Laborda (2023) | Ghana, 1999–2017 | Act 766 pension extension | Pregnancy in last 12 months; children | DiD, public-sector comparison | A | FDT |
| Ci (2024) | China, 2010–2018 | Number of children (instrumented) | Private insurance adoption | IV | B | Mechanism |
| Eibich and Siedler (2020) | Germany, 1984–2017 | Parental early-retirement eligibility | Grandchild born in t+1 | Fuzzy RDD | C | SDT |
| Ilciukas (2023) | Netherlands, 2004–2021 | 2006 reform delaying maternal retirement | Children born by 2021 | RDD at the 1950 birth cutoff; IV | C | SDT |
| Akyol and Atalay (2025) | Australia, 2001–2022 | Grandmother age-pension eligibility | Being a mother; number of children | Individual FE threshold design | C | SDT |

Zelu et al. is named because the previous draft named it; it has no row in the extraction table and no risk-of-bias grade, and it enters no calculation in this chapter.

### 6.1 The naive estimator and the direction of its bias

**What is the naive estimator in this literature?** Compare fertility where old-age security is more available with fertility where it is less available. That is the comparison an author makes without thinking hard, and it is a bad one for two compounding reasons.

It conditions on economic development. States that build pension systems are richer, more urban, and further through the mortality transition — all of which independently lower fertility. The naive comparison therefore attributes to pensions a decline that development produced.

Worse, it partly conditions on the outcome's own history. Pay-as-you-go systems are legislated *because* family support is eroding and populations are ageing; long-term-care insurance is adopted *because* there are fewer adult children to provide care. Old-age security is in part a policy response to fertility decline. Regressing fertility on old-age security therefore puts a consequence of the decline on the right-hand side.

**Both channels bias the naive estimate toward the hypothesis** — that is, toward a negative coefficient. There is no offsetting force.

**How many included studies use it?** Three of the nine extracted Cell A studies rest on aggregate cross-sectional or cross-regional variation with no exogenous shock: Basso, Bodenhorn and Cuberes (2014), Fenge and Scheubel (2017), and Galofré-Vilà (2023). Basso et al. is the purest case in the set — a **single-year, 1850 cross-county regression** of fertility on whether a county had a bank. Its `period_start` and `period_end` are both 1850. It has no time dimension at all, and therefore no way to separate banks from everything else that distinguished a county with a bank from a county without one in 1850.

**This matters more than a risk-of-bias footnote, because Basso et al. is the study the previous draft's FDT conclusion rested on.** That draft called financial development "the better-timed old-age-security substitute" and "the stronger FDT route," on the strength of a cross-sectional correlation whose bias runs in precisely the direction of the conclusion it was used to support. The finding is not that Basso et al. is wrong; it is that the chapter's FDT verdict cannot rest on it.

### 6.2 Do the studies disagree about the world, or about the estimator?

They disagree in sign, and the disagreement is not resolved by the pools reported in §7.

Oriented so that a negative value means more old-age security lowers fertility, three included estimates are positive: Galofré-Vilà's two Social Security Act estimates (+0.045 and +0.098), Guinnane and Streb's Prussian pension-alone estimate (+0.018), and Han et al.'s long-term-care-insurance estimate (+0.04). Six are negative.

The pooled summaries in §7 are negative. But two of the three positive results do not enter them — Guinnane and Streb's because its outcome unit is unsupported by the harmonisation rules, and Galofré-Vilà's because an orientation ruling codes state social spending as `not_oriented_broader_social_spending_mechanism`, a mechanism broader than old-age security.

That ruling is defensible on its merits. The Social Security Act bundled family allowances with old-age provision, and a chapter about old-age security is entitled to exclude a treatment that is not old-age security. But its arithmetic consequence has to be stated, because it is large:

| | Completed-fertility pool |
|---|---|
| As published | **−0.0677** births per woman |
| Admitting Galofré-Vilà's same-unit estimate (+0.098, se 0.016) | **+0.0549** births per woman |
| Weight that estimate would carry | **74.0%** |
| Sign flips | **Yes** |

The sign of the pooled completed-fertility summary is set by an inclusion ruling, not by the balance of evidence. A reader who disagrees with the ruling gets the opposite answer. Generated by `source/analysis/oas_synthesis_diagnostics.py` into `output/tables/old-age-security-pension-crowdout-pool-exclusion-sensitivity.csv`.

### 6.3 The transmission ledger

Sub-claim A is behavioural, so §2.3 of the template — which governs mechanisms stated as a rate or an identity — does not apply in its literal form. There is no identity arm here and no conception-to-birth accounting to run. What the mechanism does have is a transmission chain between the policy that is *counted* and the births that are *demographically relevant*, and it is worth enumerating for the same reason:

| Stage | Question | Sign |
|---|---|---|
| Enacted → covered | Who is actually reached? Brazil's and Namibia's expansions reached specific occupational and regional groups. | Attenuates |
| Covered → believed credible | Is the promise believed? A pay-as-you-go claim is only as good as the state behind it. | Attenuates |
| Believed → old-age motive was binding | Was old-age support the reason this birth was wanted? Where children are wanted for other reasons, removing the motive changes nothing. | Attenuates |
| Motive removed → birth averted | Is the birth averted or merely postponed? Birth-probability outcomes measure **tempo** (when births happen); completed-fertility outcomes measure **quantum** (how many happen in total). Only quantum moves the phenomenon. | Attenuates (for quantum) |
| Averted → room to run | By the SDT, coverage is already near-universal, so there is little dose left to apply. | Attenuates |

**Every entry attenuates. None amplifies.** The chain runs one way, which means the estimates in §7 are upper bounds on the demographic contribution, and the verdicts in §8 should be read as ceilings rather than as central cases. This is structurally the same one-directional ledger that A.12 found and that B.5's (1−p) accounting missed.

---

## 7. Quantitative synthesis

### 7.1 The answer in plain terms

The honest summary is that the studies point, on balance, the way the idea predicts — where people were handed a pension and still had good reason to rely on children, they went on to have somewhat fewer children — but that the amount is small, and the summary numbers are far less solid than they look.

Two things make them less solid. The averages are supposed to combine five studies and three studies. In practice, two studies carry almost all of each average, and the studies that were done in the places the idea fits best count for almost nothing — not because anyone judged them weak, but because of the units their authors happened to use. And the direction of one of the two averages depends on a decision to leave out a particular American study; put it back in and the average points the other way.

So the direction is probably right and the size is small. Anyone who wants to use one of these numbers as *the* effect of pensions on births should not.

### 7.2 The estimate

Two outcome-specific fixed-effect inverse-variance summaries were computed for sub-claim A, pooling within outcome family rather than across treatments.

**Birth probability**, five effects from five studies: **−0.00695** (se 0.00204; 95% CI −0.01095 to −0.00296).
**Completed fertility**, three effects from three studies: **−0.0677** births per woman (se 0.02697; 95% CI −0.12054 to −0.01481).

Both reproduce exactly from the harmonised effects, which validates the arithmetic. What the published tables do not show is where the weight sits:

| Pool | Study | Setting | Oriented effect | SE | **Weight** |
|---|---|---|---|---:|---:|
| Birth probability | Billari and Galasso | Italy | −0.00664 | 0.00286 | **50.7%** |
| | Danzer and Zyska | Brazil | −0.009 | 0.003 | **46.1%** |
| | Han et al. | China (LTCI) | +0.04 | 0.0122 | 2.8% |
| | Rossi and Godard | Namibia | −0.173 | 0.043 | 0.2% |
| | Shen et al. | China (NRPS) | −0.075 | 0.044 | 0.2% |
| Completed fertility | Billari and Galasso | Italy | −0.0529 | 0.0287 | **88.3%** |
| | Shen et al. | China (NRPS) | −0.169 | 0.079 | 11.7% |
| | Rossi and Godard | Namibia | −4.58 | 1.63 | **0.03%** |

Two studies carry 96.8% of the birth-probability pool and 99.97% of the completed-fertility pool.

**The weights are set by treatment units, not by evidential quality.** Inverse-variance weighting assumes the estimates share an estimand. These do not: the pools span five and three distinct treatment scales respectively. Rossi and Godard's coefficient is denominated per thousand rand of initial pension needs; Danzer and Zyska's is a binary exposure. A study whose treatment variable is measured in small units gets a large coefficient, a large standard error, and hence almost no weight — regardless of how well identified it is.

The consequence is stark. Rossi and Godard (2022) — a paper titled *The Old-Age Security Motive for Fertility*, published in *AEJ: Economic Policy*, the single most direct test of this chapter's registered claim in the evidence base, and the study the previous draft called the clearest developing-country evidence — carries **0.03%** of the completed-fertility summary. It is arithmetically absent from the number the chapter reports.

**These two pools should not be reported as pooled estimates.** The template's rule in §2.2 is to resolve disagreements rather than average them, and the precondition for averaging — a shared estimand — fails here on the pipeline's own recorded evidence (`n_treatment_scales` of 5 and 3 against `n_studies` of 5 and 3: every study has its own scale). What the numbers summarise is the direction of a set of studies, which is worth knowing; what they do not summarise is a magnitude, and §8 does not treat them as one.

### 7.3 The grandparental-childcare cell

Three quasi-experimental studies from Germany, the Netherlands and Australia estimate sub-claim B. Oriented to greater grandparent availability, all three are positive: more available grandparents, more births. That direction is consistent across three independent rich-country designs and is the most internally credible finding in the chapter.

The magnitude claim attached to it in the previous draft does not survive checking. That draft reported the effects as "large relative to observed declines in the **total fertility rate**" (TFR: the number of children a woman would bear if she experienced current age-specific birth rates throughout her reproductive life), on the strength of `cell-c-slope-sufficiency.csv`, which divides each effect by the change in TFR *inside the study's own window*. Those denominators are 0.097 births for the Netherlands and 0.101 for Australia — a few years of local drift, not the Second Demographic Transition.

Dividing by them produces shares that cannot be shares. Of the eight rows, six have a computed share; **two exceed 100%**, one of them reaching 273%. No mechanism explains 273% of the thing it is explaining. A share above one is not a large effect; it is a denominator that is not the phenomenon. Three of the eight rows additionally divide a *probability* by a *TFR change*, which are not the same unit.

The screen's own file warns that it is "screening language, not exact decomposition shares." The previous draft nonetheless carried the word "large" into its SDT verdict, into the summary-of-findings table, and into the **GRADE** rationale (GRADE: the standard scheme for rating how much certainty a body of evidence supports, from HIGH down to VERY LOW, with each downgrade attributed to a named defect). §8.3 withdraws it.

---

## 8. Demographic significance

The phenomenon to be explained is measured in whole children — the First Demographic Transition is a fall of roughly three births per woman and the Second roughly one and a half; this mechanism offers between 0.056 and 0.169 births per woman, under dose assumptions no study supplies.

That comparison decides most of what follows, and it decides it before any study is read. A mechanism denominated in hundredths of a birth is being asked to explain a phenomenon denominated in whole births. Only the size of the gap remains to be established.

The corrected denominators cannot be computed in this repository: the UN TFR panel used by `oas_transition_classification.py` lives in a collaborator's directory that is not reachable here, so the ~3 and ~1.5 figures above are conventional values and are *not* derived from project data. Rather than import a number this repository cannot check, the verdicts below invert the question — for each mechanism magnitude, how large can the phenomenon be before the magnitude stops clearing a verdict band? That is computable from the magnitude alone:

| Mechanism magnitude | Births/woman | Reaches MINOR (≥5%) only if the phenomenon is at most | Reaches SUBSTANTIAL (≥20%) only if at most |
|---|---:|---:|---:|
| Cell A pooled completed fertility | 0.0677 | 1.35 births | 0.34 births |
| Largest per-person Cell A estimate (Shen, NRPS) | 0.169 | 3.38 births | 0.85 births |
| Cell C Netherlands (Ilciukas) | 0.056 | 1.12 births | 0.28 births |
| Cell C Australia (Akyol and Atalay) | 0.067 | 1.34 births | 0.34 births |

Generated into `output/tables/old-age-security-pension-crowdout-units-check.csv`.

**The endogeneity check.** Before any share is claimed, ask whether the mechanism's own movement is caused by the phenomenon. For this mechanism the answer is plainly yes, in part: pay-as-you-go pension systems are legislated in response to ageing and to the erosion of family support, and long-term-care insurance is adopted because there are fewer adult children to provide care. Some of the historical growth in old-age security is a *consequence* of fertility decline, and that component must be netted out before any of it is counted as a cause. No included study identifies the size of that component, so it cannot be netted out here. This is the same feedback problem A.12 found in the modern twinning rise, and it points the same way: it inflates the apparent contribution.

### 8.1 Pre-modern fertility variation

For pre-modern variation, the verdict is NOT ASSESSED, because the cell contains no study — zero of the nine extracted Cell A studies estimate a pre-modern effect, and Basso et al.'s 1850 cross-section, the closest thing to one, is a single-year correlation with no identified variation.

Pre-modern variation is in scope for this hypothesis in the registry; the cell is empty rather than excluded, which is the distinction the widened NOT ASSESSED verdict is required to state. It is an empty cell, not a weak literature, and that difference matters. The mechanism was almost certainly a real background condition — in a world without pensions, insurance or deep financial markets, children were what people had. But a condition that holds nearly everywhere cannot explain variation *between* pre-modern populations, and nothing in the evidence base measures the differences in family systems, inheritance rules and communal care that would. If the mechanism were assessed, the expected sign would be negative, and the expected magnitude small relative to mortality and marriage systems.

### 8.2 First Demographic Transition

For the First Demographic Transition, the verdict is NEGLIGIBLE, because 0.0677 births per woman is 2.3% of a three-birth decline.

The band is NEGLIGIBLE rather than MINOR on the pooled evidence, and the ceiling is worth stating separately: the largest per-person estimate in the evidence base reaches 5.6% — just inside MINOR — but only under a dose assumption, universal pension coverage, that no FDT-era society satisfied. MINOR is therefore the most the mechanism could reach under assumptions the period rules out, not a defensible alternative reading.

Three points support that reading and one complicates it.

The pooled completed-fertility number is not FDT evidence. 88.3% of its weight is an Italian pension cut in 1998–2004, a below-replacement setting a century after the transition it is being used to describe. Of the studies that *are* FDT-relevant, Namibia contributes 0.03% and China 11.7%.

The timing objection from the previous draft stands and is strengthened. Bismarck's system dates to the late 1880s and the US Social Security Act to 1935, both after the Western decline was under way. Pensions can deepen a decline in progress; they cannot start one that preceded them.

The financial-development route is weaker than the previous draft claimed. That draft moved the FDT case onto Basso, Bodenhorn and Cuberes because financial markets were better-timed than pensions. But that study is the single-year cross-section identified in §6.1 as the naive estimator in its purest form, biased toward the hypothesis. Better timing does not compensate for absent identification. The FDT case for a *broader* asset-substitution story remains theoretically attractive and empirically untested.

What complicates the verdict is the transmission ledger: every entry attenuates, so 5.6% is a ceiling reached under the most generous assumptions available, not a central estimate.

### 8.3 Second Demographic Transition

For the Second Demographic Transition, the verdict is NEGLIGIBLE for both channels, because the largest available magnitude on either — 0.169 births under universal coverage for the old-age-security motive, 0.067 for grandparental childcare — clears 5% of a 1.5-birth decline only for the former, and the former's dose assumption is not available in a rich country where coverage is already near-universal.

**Sub-claim A has no dose left.** By the time the SDT begins, rich countries have mature pension systems. A mechanism that works by replacing children with pensions needs pensions to be newly arriving, and they are not. The chapter's two below-replacement Cell A studies are both Chinese, in a period when fertility was constrained by policy, which makes them poor evidence about a voluntary transition.

**And its predicted sign is wrong for the period.** The SDT era is one of pension retrenchment — later eligibility, less generous benefits. Through this mechanism, retrenchment makes children *more* valuable as old-age support and should have *raised* fertility. Fertility fell. The mechanism predicts the opposite of what happened, which is a stronger objection than weak evidence.

**Sub-claim B is directionally credible and demographically negligible.** Three independent quasi-experiments agree that more available grandparents means more births, and that is a real finding about a real channel. But the Netherlands estimate reaches 5% of the phenomenon only if the SDT decline is at most 1.12 births, and the Australian only if it is at most 1.34. On any conventional reading of the SDT, both fall below MINOR. The previous draft's "large" came entirely from dividing by a 0.097-birth denominator.

---

## 9. GRADE rating

Per phenomenon and channel, with every downgrade named.

| Phenomenon and channel | GRADE | Downgrades | Demographic significance |
|---|---|---|---|
| PM, old-age-security motive | **No evidence** | No body of evidence to rate: zero of the nine extracted Cell A studies estimate a pre-modern effect. VERY LOW would misdescribe an empty cell as a literature that exists and is badly identified. To earn a rating this cell would need an estimate of fertility differences between pre-modern populations that differed in how the old supported themselves. | NOT ASSESSED |
| FDT, old-age-security motive | **VERY LOW** | *Risk of bias*: 3 of 9 Cell A studies rest on cross-sectional variation biased toward the hypothesis, one with no time dimension. *Indirectness*: the pooled estimate's weight is 88% Italian and SDT-era. *Inconsistency*: sign disagreement unresolved, and the pooled sign flips on one inclusion ruling. *Imprecision*: no study supplies a dose, so no magnitude is identified. | NEGLIGIBLE (MINOR at the ceiling) |
| SDT, old-age-security motive | **VERY LOW** | *Indirectness*: both below-replacement studies are from a policy-constrained fertility regime. *Risk of bias*: as above. Additionally the mechanism predicts the wrong sign for the period's actual policy direction. | NEGLIGIBLE |
| SDT, grandparental childcare | **MODERATE** for direction; **no rating** for magnitude | *Indirectness* (one level): this is not the registered claim. Direction is supported by three independent quasi-experimental designs (fuzzy RDD, RDD, individual FE threshold) in three countries, agreeing in sign — hence MODERATE rather than LOW. Magnitude is unrated because the only magnitude calculation in the evidence base uses a denominator that is not the phenomenon. | NEGLIGIBLE |

A HIGH rating for a negligible effect would be a coherent result. This chapter does not have one: certainty is low *and* the effect is small.

---

## 10. Verdict

Non-child old-age security probably does reduce fertility where children are still a meaningful retirement asset, and the direction of the evidence supports the mechanism. But the effect is too small to explain any of the three phenomena this review is about, and the summary numbers previously reported for it do not bear the weight that was put on them.

**The one number to carry away: 0.0677 births per woman.** That is the pooled completed-fertility summary, and it is roughly 2% of the First Demographic Transition and 5% of the Second. Even the largest per-person estimate in the evidence base, applied under the impossible assumption that every woman in a population is moved from no pension to full coverage, reaches 5.6% of the First.

**Every one of those figures is a ceiling, not a central estimate.** All five stages of the transmission chain in §6.3 attenuate and none amplifies, and the mechanism's own historical growth is partly a response to the fertility decline it is invoked to explain. Both corrections push the true contribution below the numbers above; neither pushes it up.

Three further qualifications belong inside this verdict rather than below it.

The 0.0677 is 88% one Italian pension cut. The study that most directly tests this chapter's claim, in the setting where the mechanism should be strongest, contributes 0.03% of it. And the sign of that number depends on a ruling to exclude an American estimate that would otherwise carry three-quarters of the weight and reverse it.

The grandparental-childcare channel is a genuine finding — three independent designs agree that available grandparents raise fertility — but it is not the registered hypothesis, and its previously reported magnitude was an artefact of dividing by seventeen years of Dutch drift instead of by the transition.

The chapter rests on 13 studies selected from 1,860 machine-screened records by a step with ten recorded decisions.

**What would change it:** a study that reports a fertility response to a *quantified* change in old-age security — a coverage rate, a replacement rate, a pension-wealth amount — so that a historical dose could be applied to an estimated slope. No included study does. Until one exists, the demographic significance of this mechanism is bounded but not measured.

---

## 11. Open questions

**PI calls required.**

1. **Should the two pooled summaries be withdrawn?** §7.2 argues they average across estimands that the pipeline itself records as distinct (`n_treatment_scales` = `n_studies` in both pools). The alternative is a forest plot with no summary line. This is the chapter's most consequential open decision.
2. **Is the Galofré-Vilà exclusion correct?** It is defensible, and it determines the sign of a headline number. It should be an explicit, recorded PI ruling rather than a pipeline constant.
3. **Should Basso, Bodenhorn and Cuberes (2014) carry any FDT weight?** A single-year cross-section is the naive estimator; the previous draft's FDT case rested on it.
4. **Should the grandparental-childcare channel be split into its own chapter?** It is not the registered claim, it predicts the opposite sign, and it is now the chapter's most credible finding. Per the project's split rule, the decision belongs at synthesis and the splitting field — which channel a design identifies — is not visible at title/abstract, which is Wall 3's problem exactly.
**Retrieval and data priorities.**

5. Recompute the Cell C slope sufficiency against the SDT decline rather than the in-window change. This needs the UN TFR panel, which is not reachable from this machine; it is a data-access task, not an analysis task.
6. Reconstruct the 1,860 → 13 screen, or state in the header that the included set is expert-curated.
7. Account for the 31 held PDFs that have no extraction row.
8. Extract Zelu, Iranzo and Pérez-Laborda (2023), or drop it from the chapter.
9. `extraction/…-studies.csv` records `extraction_status: not_started` for all 9 Cell A studies while `…-effects.csv` records `ra_verified: yes` for all their effects. One of the two fields is wrong.

**Studies that do not exist and should.** A pension expansion that is exogenous *and* quantified in replacement-rate terms, in a setting with high baseline reliance on children, with completed fertility observed. Namibia and Brazil each have half of this; neither has all of it.

---

## 12. References

Akyol, P. and Atalay, K. (2025). The intergenerational impact of pension reforms. *Economics Letters*. doi:10.1016/j.econlet.2025.112239
Barro, R. and Becker, G. (1989). Fertility choice in a model of economic growth. *Econometrica*.
Basso, A., Bodenhorn, H. and Cuberes, D. (2014). Fertility and financial development: evidence from U.S. counties in the 19th century. NBER WP 20491. doi:10.3386/w20491
Becker, G. (1960). An economic analysis of fertility.
Becker, G. and Barro, R. (1988). A reformulation of the economic theory of fertility. *QJE*.
Billari, F. and Galasso, V. (2009). What explains fertility? Evidence from Italian pension reforms. CESifo WP. doi:10.2139/ssrn.1406946
Boldrin, M., De Nardi, M. and Jones, L. (2015). Fertility and social security. *Journal of Demographic Economics*.
Caldwell, J. (1976). Toward a restatement of demographic transition theory. *PDR*.
Ci, Z. (2024). Children as insurance revisited. *Journal of Risk and Insurance*. doi:10.1111/jori.12492
Cigno, A. (1993). Intergenerational transfers without altruism. *European Journal of Political Economy*.
Danzer, A. and Zyska, L. (2023). Pensions and fertility: microeconomic evidence. *AEJ: Economic Policy*. doi:10.1257/pol.20200440
Ehrlich, I. and Lui, F. (1991). Intergenerational trade, longevity, and economic growth. *JPE*.
Eibich, P. and Siedler, T. (2020). Retirement, intergenerational time transfers, and fertility. *European Economic Review*. doi:10.1016/j.euroecorev.2020.103392
Fenge, R. and Scheubel, B. (2017). Pensions and fertility: back to the roots. *Journal of Population Economics*. doi:10.1007/s00148-016-0608-x
Galofré-Vilà, G. (2023). The US baby boom and the 1935 Social Security Act. *The History of the Family*. doi:10.1080/1081602x.2023.2178478
Guinnane, T. and Streb, J. (2021). The introduction of Bismarck's social security system and its effects on marriage and fertility in Prussia. *PDR*. doi:10.1111/padr.12426 (with 2022 corrigendum)
Han, Y., Tao, X., Wang, S. and Zhang, Y. (2025). The impact of long-term care insurance on family fertility behaviour. *Applied Economics*. doi:10.1080/00036846.2025.2490215
Ilciukas, J. (2023). Fertility and parental retirement. *Journal of Public Economics*. doi:10.1016/j.jpubeco.2023.104928
Neher, P. (1971). Peasants, procreation, and pensions. *AER*.
Nishimura, K. and Zhang, J. (1992). Pay-as-you-go public pensions with endogenous fertility. *Journal of Public Economics*.
Nugent, J. (1985). The old-age security motive for fertility. *PDR*. 
Rossi, P. and Godard, M. (2022). The old-age security motive for fertility: evidence from Namibia. *AEJ: Economic Policy*. doi:10.1257/pol.20200466
Shen, Z., Zheng, X. and Yang, H. (2020). The fertility effects of public pension. *PLOS ONE*. doi:10.1371/journal.pone.0234657
Sinn, H.-W. (2004). The pay-as-you-go pension system as fertility insurance and an enforcement device. *Journal of Public Economics*.
Willis, R. (1980). The old age security hypothesis and population growth.
Zelu, B., Iranzo, S. and Pérez-Laborda, A. (2023). Pension reform and fertility: evidence from Ghana. Working paper. *Not extracted; not used in any calculation in this chapter.*

---

## Provenance and standing caveats

This chapter is written on 13 of 13 wanted full texts (100%).

That number is true and close to meaningless, and the reason is in §4: the 13 were selected from 1,860 machine-screened records by a human screen with ten recorded decisions, and 31 further PDFs are held without extraction rows. The retrieval fraction that matters is not the one the template asks for. **The finding that would survive full retrieval is the units result** — the mechanism is denominated in hundredths of a birth against phenomena denominated in whole births, and no additional study changes that unless it supplies a dose. **The findings that might not are** the pooled magnitudes, the weight concentration, and the sign sensitivity, all of which are properties of this particular set of nine Cell A studies and would change if the set changed.

**Objection over which this chapter was written.** None recorded from the PI. The rewrite itself, however, contradicts the previous draft (2026-07-11) on two substantive points that were benchmarked against PI review v4: that the grandparental-childcare effects are "large relative to observed TFR declines" (§7.3 shows the denominator is not the phenomenon and two shares exceed 100%), and that financial development is "the stronger FDT route" (§6.1 identifies that study as the naive estimator). Both reversals are the present author's, are argued from files already in the repository, and have not been reviewed. They should be treated as contested until they are.

**Numbers sourced from abstracts rather than full text.** None. All effect rows carry a page-and-table locator in `extraction/…-effects.csv`. The Zelu et al. figures quoted in the previous draft came from a working-paper draft; they have been removed from this one rather than marked, because the study has no extraction row.

**Figures not derived from project data.** The ~3-birth FDT and ~1.5-birth SDT declines used in §8 are conventional values, not computed here; the UN TFR panel is not reachable from this repository. Every verdict in §8 is therefore stated as a break-even — the largest phenomenon for which a given magnitude still clears a band — so that a reader with the panel can substitute the real denominator without redoing the analysis.

**Generated inputs.** All quantitative claims in §§7–8 come from `source/analysis/oas_synthesis_diagnostics.py`, which reproduces both published pooled estimates exactly as an arithmetic self-check, and writes:

- `output/tables/old-age-security-pension-crowdout-pool-weight-concentration.csv`
- `output/tables/old-age-security-pension-crowdout-pool-exclusion-sensitivity.csv`
- `output/tables/old-age-security-pension-crowdout-slope-denominator-check.csv`
- `output/tables/old-age-security-pension-crowdout-units-check.csv`
- `output/tables/old-age-security-pension-crowdout-synthesis-diagnostics.json`

Upstream pipeline, extraction tables and search logs are unchanged and are listed in the previous draft's reproducibility appendix, retained at `output/chapters/old-age-security-pension-crowdout-pi-review v4.md`.
