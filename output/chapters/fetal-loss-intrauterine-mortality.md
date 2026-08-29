# Fetal Loss and Intrauterine Mortality

**Category:** Biological
**Primary mechanism:** A share of conceptions never reaches live birth, so a fall in intrauterine mortality raises live births at an unchanged conception rate — a biological determinant of fertility requiring no change in what anyone wants.
**Cross-references:** A.4 induced abortion (which owns deliberate termination and contaminates every measured "spontaneous" loss series where abortion is restricted) · A.11 tempo and A.15 (which own the age-composition channel, and to which the SDT cell is scoped out) · maternal health, infection and nutrition chapters, each of which owns one of this mechanism's named drivers.
**Status:** TICK-065. Rewritten against `docs/chapter-template.md` on 2026-08-29; previous draft 2026-08-11. Demographic significance is complete, tested and reproducible; the RA title/abstract gate is unsigned, GRADE deviates from the three-rater protocol, and four scope calls are open with the PI. Written on 2 of 51 wanted full texts (4%).

---

## 1. The claim

This chapter explores the effect of intrauterine mortality on the number of children a woman bears.

### 1.1 In plain terms

In plain terms: not every pregnancy ends in a baby. A substantial share end early, often before the woman knows she is pregnant, and some end late. That share was much higher in the past and in poorer places, and it has fallen a great deal over the last century and a half. The claim is that this by itself changed how many children women ended up with — no one had to want anything different.

The obvious way to work out how much is to say: if a quarter of pregnancies used to be lost and now a tenth are, then for the same number of pregnancies you get about a fifth more babies. That calculation is wrong, and understanding why is most of this chapter.

A woman does not get one pregnancy and see whether it works. She has many years in which to try. A pregnancy that fails costs her the months she was carrying it, some weeks to recover, and some more months before she conceives again — perhaps nine months in total. **It costs her time, not a child.** Whether that lost time costs her a child depends entirely on whether she runs out of years before she runs out of wanting children. A woman bearing children until her body stops can never get those months back. A woman who wanted three and has three by thirty simply tries again and ends up with three either way.

So the same fall in pregnancy loss does a great deal in one kind of society and almost nothing in another, and it is the kind of society, not the loss rate, that decides.

### 1.2 The claim precisely

The parameter this chapter estimates is the change in **completed fertility**, in births per woman, caused by a change in the probability that an established pregnancy is lost, **after whatever replacement behaviour the population actually performs**, signed so that a fall in loss raises births.

The chapter is scoped to **PM** (pre-modern fertility variation, before roughly 1870) and **FDT** (the First Demographic Transition, roughly 1870–1965). There is no **SDT** cell: the age-composition channel is A.11's and A.15's (Call 2).

**This mechanism has an identity arm and a behavioural arm, and separating them is the whole chapter.**

**The identity arm cannot be false and is not the effect.** Write $B$ for live births, $C$ for conceptions and $p$ for the probability a conception is lost. For a single conception, $B = C(1-p)$. This is the form in which the hypothesis is usually asserted, and **it is an upper bound no population attains.**

**The behavioural arm is where the hypothesis can be wrong**, and it runs through time rather than through births. Over a reproductive career the mean closed birth interval decomposes additively, in the tradition from Sheps and Menken (1973) through Bongaarts (1978) and Bongaarts and Potter (1983):

$$BI = i + w + g + TA(p), \qquad TA(p) = \frac{p}{1-p}\,(g_L + r + w)$$

where $i$ is postpartum infecundability, $w$ the waiting time to conception, $g$ gestation, $g_L$ the gestation elapsed at a loss and $r$ the recovery period. **The expected number of losses per live birth is $p/(1-p)$, not $p$**: at a 25% loss rate a woman expects one loss for every three live births, and each costs her roughly eight to eleven months rather than a child.

**Whether that lost time costs a birth depends on which constraint binds, and this is the mechanism rather than a modelling convenience:**

- **Where the reproductive span binds** — uncontrolled fertility, early and near-continuous exposure, childbearing until fecundity ends — lost time cannot be recovered and the effect is real, though far smaller than $(1-p)$ implies.
- **Where a parity target binds** — a desired family size reached well before the span runs out — the couple replaces the loss and completed fertility is unchanged. The loss changes the *timing* of births, not their number.

**This predicts that B.5's effect is largest in pre-modern populations and decays to nothing under controlled fertility, and it is testable.** Every estimate is tagged `ACCOUNTING_SHARE` for the mechanical calculation or `BEHAVIORAL_NET` for the effect after replacement. **The two are never combined**, and the second is the quantity `PROTOCOL.md` §4.2 asks for.

**Margin.** Intensive, and only where the span binds.

**Why this chapter routes differently from every other in the review.** B.5 is defined by a **channel**, not a treatment. Its named drivers — maternal health, infection, nutrition — are each owned or bordered by another chapter, and its outcome is the review's common outcome. What B.5 owns is the segment of the reproductive process between conception and delivery. A study belongs here when the quantity doing the causal work is **survival of an established pregnancy**, whatever moves it. Applying the source-of-variation rule used elsewhere would empty the chapter, since every one of its drivers is another chapter's treatment.

---

## 2. Theoretical mechanism

The mechanism is in §1.2, because here the identity *is* the theory. What remains is the three identification problems, in order of severity, each of which was named before the search ran and each of which then appeared in the first studies retrieved.

**Reverse causation runs through parity and spacing, and it runs the wrong way.** Higher parity and shorter birth intervals raise loss risk, and a woman with more pregnancies has had more opportunities to record a loss. **A raw cross-sectional association between measured loss and completed fertility is therefore contaminated toward a positive sign** — more births produce more recorded losses. **A positive raw correlation is a warning about the design, not evidence for the hypothesis.** Two screened studies attack this directly, including an Egyptian analysis titled, flatly, "High fertility does not cause spontaneous intrauterine fetal loss".

**Loss is partly a selection mechanism.** Over half of early miscarriages carry chromosomal abnormalities. **Averted loss does not convert one-for-one into a surviving birth**, because part of what is averted would have failed later or produced a non-viable outcome. A 1996 study conditioning on *chromosomally normal* spontaneous abortion is the design that separates selection-driven from environmentally driven loss; it is rare.

**The measurement problem is first-order.** Retrospective pregnancy histories omit losses non-randomly — worse for early losses, for losses further in the past, and for less-educated respondents — and **because women with more births have more recent and more salient reproductive histories, reporting quality correlates with the outcome.** Where induced abortion is illegal or stigmatised it is reported as spontaneous. And a "loss rate" means nothing without its gestational window: clinically recognised loss from six weeks is a different quantity from total post-implantation loss, which Wilcox and colleagues put near **31%** by hCG assay in 1988, which differs again from stillbirth defined at 20, 22, 24 or 28 weeks. National definitions differ on exactly those thresholds; Quebec's change to its fetal-mortality definition is the cleanest natural experiment on the point.

**Both problems are largest in exactly the pre-modern and transitional settings that carry this chapter's two live cells.** The demographic literature has known this since Leridon's 1976 reconsideration and Casterline's 1989 World Fertility Survey review, and a 2023 analysis of 157 surveys across 53 countries now supplies quantified adjustment procedures.

**What would make the hypothesis wrong.** It is wrong if falls in intrauterine mortality leave completed fertility unchanged even where the span binds — which the Hutterite consanguinity evidence suggests happens through compensating conceptions — or if the whole measured association is reporting artefact and parity-driven reverse causation.

---

## 3. Search strategy

A reconnaissance probe ran **before** the scope was fixed: 35 OpenAlex queries, zero failed requests, so its zero-hit counts are genuine absences rather than errors. It established that the demographic seam is thin inside a very large clinical literature, and **the scope was written against that measurement rather than against an expectation.**

| Wall | Rule | Enforceable at title/abstract? |
|---|---|---|
| **W1 The live-birth boundary** | The quantity doing causal work must be survival of an established pregnancy. | Partially |
| **W2 Estimand level** | `ACCOUNTING_SHARE` and `BEHAVIORAL_NET` are never combined. | **No** — visible only in the method |
| **W3 Outcome** | The outcome must be births or completed parity, not loss itself. | **No — and this is the wall that fires most.** Several strong designs estimate the shock's effect on *loss* and infer the birth consequence. |
| **W4 Spontaneous vs induced** | Induced termination is A.4's. | **No** — and §6.1 shows it fires on the chapter's only headline estimate |

**Thirty-one cold-start anchors, twenty-five verified** through three gates: existence, version-of-record, and a **book-canon gate**. The book gate earned its place: five of this canon's works are monographs and every one returns its own reviews, and for Leridon 1977, Sheps and Menken 1973 and Preston 1978 the review records credit **the books' own authors**, so an author check passes and only the review-shape test rejects. Three resolver defects were found by auditing its **refusals** rather than its acceptances: a Crossref/OpenAlex type-vocabulary mismatch silently penalising every OpenAlex record by 90 points, a missing-author state ranked neutral, and an ISBN check digit misread as a chapter ordinal.

**Citation frame:** one hop backward and forward from verified anchors, 11,504 records deduplicated to 11,125. Routing decoys were forward-cited like every other seed, following the D.2.d finding that a decoy's neighbourhood is where boundary cases live; **1,888 frame records (16%) exist only because of that, and the decoy clouds ran 68–75% on-topic, at or above the theory canon.**

**Two validations were run rather than asserted.** Four records whose correct routing was known independently — the three monographs the anchor resolver refused, plus one version duplicate — reappeared inside the frame as cited works and **the screen routed all four correctly**, recovering Wood 1994, Leridon 1977 and Bongaarts and Potter 1983, so the theory canon is intact despite four unresolved anchors. Separately, of twelve screened records depending only on a decoy seed, six were routed away.

---

## 4. PRISMA flow

| Stage | Records |
|---|---:|
| Cold-start anchors sourced / verified | 31 / 25 |
| Citation frame, deduplicated | 11,125 |
| Deterministic two-axis rank → **semantic screen** | **392** (top 340 by score + 52 orthogonal-channel bypasses) |
| **Unread by budget** | **10,733** |
| Primary cells | **17** (18 before the Valente duplicate collapsed) |
| Parameter stream | ~200 |
| Measurement stream | ~40 |
| Theory and accounting | ~12 |
| Held for full text | 13 |
| Excluded | 94 |
| **Full texts retrieved and extracted** | **2 of 51** |

Three features of this funnel change how the chapter should be read.

**First, the scarcity was predicted and then confirmed.** `"fetal loss" AND "natural fertility"` returns three records; `"stillbirth" AND "fertility decline"` returns sixteen. Against that, the clinical literature on miscarriage and stillbirth runs to thousands. **The evidence is abundant on how much loss there is and what causes it, and nearly silent on what it does to the number of children a woman ends up with.**

**Second, the parameter stream is larger and better identified than the causal stream, which inverts the usual pattern in this review** — and has a consequence for how the chapter is read: **the demographic-significance computation in §8 rests on firmer ground than the GRADE rating in §9 does.** The parameter stream is deliberately not credited toward GRADE (Call 4), and the two are reported separately so a reader does not lend the causal claim the precision of the loss-rate literature.

**Third, the screen is budget-bounded at 392 of 11,125 and 10,733 records went unread.** The residual is characterised in the D1 log; most carries no term from one or both axes. Extending the screen is the obvious next increment.

---

## 5. The ideal design

Written before the literature was read, so §6 can be measured against a fixed yardstick.

### 5.1 The ideal estimand

The change in **completed cohort fertility**, in births per woman at the end of the reproductive span, caused by an exogenous reduction in the probability that a clinically recognised pregnancy is lost — **estimated separately in a span-binding and a target-binding population using the same design.**

The paired estimation is the specification, and it is unusual. §1.2 predicts a substantial effect in the first population and **approximately zero** in the second. A single estimate in either population alone is consistent with the mechanism and with its absence; **only the contrast tests the mechanism as stated.**

### 5.2 The design that would identify it

**Source of variation.** An exogenous shock to intrauterine survival that does not independently move the desire for children or the conception rate: a famine, an epidemic, a conflict-casualty shock, or a public-health intervention against a loss-causing infection.

**Comparison group.** Cohorts or districts unexposed, matched on pre-shock fertility trajectory.

**Identifying assumption.** The shock moved pregnancy survival and did not move conception intentions. **This is the hard one and it is the documented weak point**: the published exchange over whether the 1919–20 natality decline reflects influenza-induced miscarriage or wartime behaviour is exactly this assumption in dispute. Falsifiable by comparing responses across shocks whose *behavioural* salience differs while their *biological* action does not — a nineteenth-century influenza epidemic against COVID.

**Estimating equation.** An event study on **completed cohort fertility**, with the loss rate as a reported first stage, run separately by fertility regime and interacted with it.

**Data required.** Individual pregnancy histories with losses recorded prospectively — not retrospectively, given §2 — linked to completed fertility, spanning a shock, in two populations of different regime. Historical parish reconstitution supplies one side; the Nordic registries supply the other.

**Sample size.** The predicted effect is a few percent of completed fertility; detecting 0.1 births per woman needs roughly 2,650 per arm, and the regime interaction needs that in each.

**What the ideal design excludes.** Any estimate that stops at **loss** rather than carrying through to births — §6.2 shows this is where most of the good designs stop. And any exposure series contaminated by induced abortion, which is A.4's estimand and, per §6.1, is most of the largest component of this chapter's only headline number.

### 5.3 Distance from the ideal

| Study or group | Outcome is births, not loss? | Exogenous shock? | Completed fertility? | Regime contrast? | Distance |
|---|---|---|---|---|---|
| **Danish registry, 458,475 women to 45** | **Yes — completed family size** | No — observational | **Yes** | **Target-binding only** | **Half the ideal design, and the half where the prediction is ~zero** |
| Hutterite consanguinity | Yes | No | Yes | Span-binding only | The other half; finds compensation absorbs loss |
| Swedish 1844 cousin-marriage legalisation | Yes | **Yes** | Yes | Span-binding | Close on design, narrow on exposure |
| Swiss 1871–2022, four pandemics | Yes — general fertility rate | **Yes, repeated** | No — period rate | No | **Closest to a replication design** |
| Famine studies (China, Bangladesh, Dutch Hunger Winter) | Mixed | **Yes** | No | No | Strong exposure, wrong estimand |
| Valente 2015 (Nepal conflict) | **No — loss is the outcome** | **Yes** | No | No | **Best-identified loss estimate in the corpus; wrong margin** |
| Mourchid and Bakass 2022 (Morocco) | Yes | No | Potential fertility | No | **`ACCOUNTING_SHARE` by construction** |

**No study implements the ideal design, and the gap is precisely located: not one study estimates the regime contrast that the mechanism turns on.** The Danish registry observes the target-binding population where the prediction says the effect should be near zero; the Hutterite and Swedish consanguinity designs observe span-binding populations. **The two halves exist in different literatures and have never been put in one design.**

**And the recurring weakness across the strongest designs is that they are strong on the exposure and weak on the estimand.** Several identify the shock's effect on *loss* and infer the birth consequence rather than estimating it. Valente is the sharpest example: the best-identified estimate in the corpus, and its outcome is miscarriage.

---

## 6. Included studies

Two studies retrieved and extracted; the rest of this section describes designs located from abstracts and is deliberately not a results section.

### 6.1 The two extracted studies

**The one published estimate of this chapter's headline quantity is an accounting share.** Mourchid and Bakass (2022) estimate that intrauterine mortality reduces Moroccan potential fertility by **9.4%**, or 0.23 children per woman, using 2009–10 survey data and a gestational-age life table. It is the only located study estimating B.5's primary estimand directly. **But their potential-fertility measure is built by adding fetal deaths to live births**: a lost conception is counted as a forgone birth, with no time cost and no replacement. It is `ACCOUNTING_SHARE` by construction — the upper bound §1.2 argues against using as the effect. This **corroborates** the chapter rather than contradicting it: the model's accounting arm returns about 11% for removing a 10% loss rate outright, close enough to 9.4% to confirm the two compute the same thing. **The published literature states this hypothesis at the level the chapter says overstates it.**

**W4 fires, and the authors supply the evidence themselves.** The 9.4% decomposes into 6.0 points from early fetal mortality and 3.8 from stillbirth. Mourchid and Bakass define early fetal mortality as *abortions plus miscarriages*, and their own Bongaarts residual index attributes **0.12 births per woman to induced abortion against 0.14 for all early fetal mortality.** On their own numbers, most of the larger component is induced termination, which is A.4's estimand. **B.5's clean share of the Moroccan estimate is the stillbirth component, 3.8%, and the headline 9.4% must not be quoted as a B.5 effect.** This is the contamination the scope predicted for settings where abortion is legally restricted, arriving in the first study retrieved. A second internal tension: the paper's life-table loss quotient is 272 per 1,000 pregnancies while its reported fetal-death rates imply roughly 100 per 1,000 — the Casterline and Leridon under-reporting problem visible inside a single study.

**Valente (2015) reroutes on retrieval**, from `PRIMARY_SHOCK_TO_BIRTHS` to `PARAMETER_DETERMINANT_TO_LOSS`: the outcomes are miscarriage, stillbirth and sex at birth, not births per woman. The abstract does not say so, **so this is the routing gate working rather than a screening error.** It is nonetheless the **best-identified loss-margin estimate in the corpus**: maternal fixed effects over 11,887 Nepali pregnancies with district-by-month conflict casualties as the shock, the effect concentrated in gestational months one to five as the mechanism predicts. Moving from low- to high-intensity exposure raises miscarriage probability by 0.77 percentage points, 11.6% of the mean.

Three of its details bear on §2's identification problems, and all three were flagged there a priori:

- **Stillbirth moves the other way** (−0.22 ppt), which Valente reads as conflict-exposed fetuses being lost earlier rather than surviving to stillbirth — **compositional movement across the live-birth boundary, so W1 matters empirically and not merely definitionally.**
- **Replacement and differential reporting appear together in the author's own words**: women who lose a pregnancy may both try again sooner and under-report a further loss.
- **The result rests on the maternal-fixed-effects specification.** Within-district estimates are positive but insignificant, and the author's explanation is differential fertility timing by conflict intensity — a selection process rather than noise. Recorded as a fragility.

Risk of bias: Mourchid and Bakass rate **Critical**, binding on exposure measurement, usable as an accounting benchmark rather than causal evidence. Valente rates **Moderate**, binding on outcome measurement, with self-reported-miscarriage bias running toward zero.

**One count correction follows.** `W1977150354`, "Children of the Revolution", is confirmed to be Valente's own working paper on the same Nepal data, so it collapses into the published article and **the primary-cell count falls from 18 to 17.** That duplicate is invisible to both dedup rules the pipeline uses: the DOIs differ, and the working paper was retitled before publication, so the titles share almost no tokens.

### 6.2 The unretrieved primary evidence

**The shock studies are where identification lives.** *Famine:* the Chinese Great Leap famine against involuntary fetal loss (*Demography* 2005); the 1974–75 Bangladesh famine (*Demography* 2014); the Dutch Hunger Winter against stillbirths in 1935–47 vital statistics (*Population Studies* 2023); a 1993 account of the post-war Dresden fertility collapse with concurrent miscarriage epidemics. *Epidemics:* the 1918–20 pandemic recurs in five independent settings, and **a 2025 *Population Studies* analysis follows Swiss general fertility rates from 1871 to 2022 across the 1889–90, 1918–20, 1957 and COVID pandemics, finding births falling six to nine months after each peak and offering miscarriage as the explanation. That is the closest thing this chapter has to a replication design.** *Conflict and economic shocks:* civil conflict and gender-specific fetal loss; Danish spontaneous loss after downturns; the Gulf War and spontaneous abortion in Bahrain.

**The direct loss-to-fertility studies are few and heterogeneous**: the Moroccan life-table study; a Korean study pooling induced and spontaneous loss; two consanguinity designs — Hutterite couples and a historical Swedish population exploiting the 1844 legalisation of cousin marriage — of which **the Hutterite result is that elevated loss does *not* lower completed fertility, because compensating conceptions absorb it**; and the Danish registry of 458,475 women.

**The replacement studies convert an accounting share into a net effect, and there are five**: reproductive compensation among the Hutterites, time to pregnancy by interval after an early loss, prior losses and the chance of a live birth in the next pregnancy, fertility after recurrent miscarriage in 719 couples, and a life-course study of whether a loss changes subsequent fertility desires. **Without this stream the chapter cannot compute the quantity it needs.**

### 6.3 The transmission ledger

| Stage | Question | Sign |
|---|---|---|
| Loss rate falls → pregnancies survive | The identity arm | **Cannot be false; not the effect** |
| Survives → averted loss was viable | Over half of early losses are chromosomally abnormal | **Attenuates** |
| Time saved → a birth gained | Only where the span binds | **Regime-dependent: real, or exactly zero** |
| Measured loss → true loss | Retrospective under-reporting, correlated with the outcome | **Attenuates, and biases the association positive** |
| Measured "spontaneous" → actually spontaneous | Induced abortion reported as spontaneous where restricted | **Contaminates toward A.4** |

The third row is not an attenuation but a switch, and it is the mechanism.

---

## 7. Quantitative synthesis

### 7.1 The answer in plain terms

The sum everyone does gives an answer about two and a half times too big.

Doing it properly — counting the months a failed pregnancy costs rather than pretending it deletes a child — a woman in a society where people have children until they can no longer do so ends up with about 6% more children when pregnancy loss falls from a quarter to a tenth. That is roughly a third of one child, on top of about six. Real, but not the story of anything.

In a society where people stop at the family size they wanted, the answer is close to nothing at all. The loss delays a birth; it does not remove one.

And for the great fertility decline of 1870 to 1965 the mechanism points the wrong way. Pregnancy loss was falling across exactly that period, which pushed births **up** while fertility halved. On these numbers it pushed them up by about a tenth of the size of the fall. That does not help explain the decline; it means the decline in what people were doing was about a tenth larger than the raw numbers show.

### 7.2 The estimate

**No pooled estimate is produced, and none should be.** `PROTOCOL.md` §5.9 directs meta-analysis at three or more extractable effects, and the primary cells hold seventeen — which clears the count and **fails the precondition**. They do not share an estimand: they differ on estimand level (mechanical versus post-replacement), on loss window (pre-clinical, clinically recognised, late fetal), on outcome (births, completed parity, intentions), and on **fertility regime, which §1.2 says determines the effect's very existence.** Pooling across those produces a number with no interpretation. **A forest plot assembled from incommensurable quantities is worse than no forest plot, because it looks like a result.**

The synthesis is therefore the parameter model of §8, with the primary studies used to discipline its inputs and to test its central prediction.

---

## 8. Demographic significance

The phenomenon to be explained is measured in whole children — pre-modern variation spans roughly four to eight births per woman and the FDT is a fall of about 2.5 births from a base near 5.5; this mechanism offers, after replacement, between +0.25 and +0.37 births per woman.

Computed by `source/analysis/b5_demographic_significance.py` (20,000 Monte Carlo draws, fixed seed, 13 passing tests). Every figure is a median with a 95% interval across parameter ranges, because the inputs are genuinely uncertain.

| Phenomenon | Loss-rate change | `ACCOUNTING_SHARE` (upper bound) | `BEHAVIORAL_NET` | Overstatement |
|---|---|---|---|---|
| Pre-modern | 0.20–0.28 → 0.10–0.15 | +15.2% | **+6.2%** (+3.2% to +9.9%) | **2.5×** |
| First transition | 0.16–0.24 → 0.09–0.13 | +11.3% | **+4.5%** (+2.0% to +7.7%) | **2.5×** |

**The denominators, per `PROTOCOL.md` §4.2.1.** The pre-modern denominator is the observed *range* of completed fertility across pre-modern populations, roughly four to eight births; the FDT denominator is the observed *fall* in completed fertility across 1870–1965, roughly 2.5 births from a base near 5.5. Both are changes or ranges rather than levels, both are the phenomenon's full window rather than a study window, and both are in births per woman, matching the numerator. They are conventional magnitudes, not computed here.

**The endogeneity check** does not bite in the usual direction: falling intrauterine mortality is driven by maternal health, nutrition and infection control, which are consequences of development rather than of the fertility decline. What does bite is that **those same drivers are other chapters' treatments**, so any share credited here is at risk of being double-counted there — the §1.2 routing problem reappearing as an accounting problem.

### 8.1 Pre-modern fertility variation

For pre-modern variation, the verdict is MINOR, because moving a natural-fertility population from a high- to a low-morbidity loss regime raises completed fertility by about 6.2% (interval 3.2% to 9.9%) of a four-to-eight-birth range.

That is roughly 0.37 of a birth against a pre-modern total near six, and it moves the mean birth interval by about two months. **It is real and not trivial, and it is smaller than the other components of the birth interval** — postpartum infecundability and the waiting time to conception each move it more. Contributory rather than sufficient.

**No study identifies this effect in a pre-modern population.** The number is a model populated by parameter estimates, which is why §9 rates the cell VERY LOW while the number itself carries a computed interval.

### 8.2 First Demographic Transition

For the First Demographic Transition, the verdict is MINOR in magnitude — 10.0% of the observed change — **but the sign is inverted, and the mechanism therefore explains none of the decline.**

The decline in intrauterine mortality across the transition raises births by about 4.5% where the span binds. Applied to a starting TFR of 5.5, that is **+0.25 births per woman, against an observed decline of −2.5.**

**What the number means is not that B.5 explains 10% of the first transition.** It means the *behavioural* component of the decline was about 10% larger than the raw TFR series shows, because a rising share of conceptions was surviving while births fell. **The hypothesis deepens the puzzle other chapters are trying to solve rather than helping to solve it.**

**The verdict vocabulary has no signed value, and this chapter is where that gap bites.** `PROTOCOL.md` §4.2's bands and the template's NEGLIGIBLE/MINOR/SUBSTANTIAL/DOMINANT scale both presume the mechanism works in the direction of the phenomenon. A mechanism contributing −10% is not MINOR in the sense a reader will take. **How this should be scored is Call 1 in the search scope, is open with the PI, and generalises past this chapter**: any hypothesis whose predicted sign opposes the phenomenon it is assigned to faces it, and the ruling belongs in `PROTOCOL.md` §4.2 rather than here.

The magnitude also lands almost exactly on the old 10% threshold, which makes the verdict knife-edge and sensitive to the historical early-loss rate — the least observed parameter in the model.

### 8.3 Second Demographic Transition

For the Second Demographic Transition, the verdict is NOT ASSESSED, because the phenomenon is out of scope for this hypothesis in the registry: the age-composition channel is A.11's and A.15's (Call 2).

### 8.4 What would move these numbers

**The observation window governs everything.** These are clinically recognised losses. Total post-implantation loss is near 31%, but a conception lost before recognition costs little more than a cycle and cannot lengthen a birth interval by much; **substituting the total-loss figure is the most common way this calculation is done wrong** and would inflate every number above. The nineteenth-century early-loss rate is unobserved — historical sources record stillbirths, not miscarriages — and is the largest single source of uncertainty in the FDT row. Under-reporting biases recorded rates downward, so the historical contrast may be understated; the 53-country adjustment procedures would sharpen it. Induced abortion contaminates the measured series toward overstating spontaneous loss.

---

## 9. GRADE rating

**Deviation from protocol, stated plainly:** `PROTOCOL.md` §5.11 requires three independent raters. These ratings were produced by one analyst applying three lenses in sequence — evidence-quality, identification, transportability — which is not the same thing and does not carry the same weight. Independent re-rating is open.

| Phenomenon | GRADE | Downgrades | Demographic significance |
|---|---|---|---|
| PM | **VERY LOW** | *Imprecision and indirectness*: no study identifies the effect on completed fertility in a pre-modern population; the estimate is a model populated by parameter estimates. *Risk of bias*: the exposure in every historical source is measured with error that correlates with the outcome. | MINOR (+6.2%) |
| FDT | **LOW** | Several historical series document the fetal-mortality decline with individual-level records — Derbyshire c. 1900, Bern 1880–1922, Cumbria 1950–92, Italian regions after unification with misreporting modelled, Denmark after 1940 — and pandemic and famine shocks supply quasi-experimental variation, with the Swiss 1871–2022 series repeating it across four pandemics. *Indirectness*: **no design carries the shock through to completed fertility rather than to loss.** *Inconsistency*: the published exchange on the 1918 case disputes the channel. | MINOR in magnitude, **sign inverted** |
| SDT | **No evidence** | Out of scope in the registry. | NOT ASSESSED |

**The parameter stream would rate higher on its own and is deliberately not credited here** (Call 4). §4 explains why: crediting it would lend the causal claim the precision of the loss-rate literature.

---

## 10. Verdict

Fetal loss varies enormously across populations and has fallen substantially over the last century and a half, and both facts are well measured. **Whether that variation moved completed fertility is a different question, and the answer is that it moved it far less than the arithmetic suggests, in a way that depends on the fertility regime rather than on the loss rate.**

**The one number to carry away: 2.5×.** That is the factor by which the mechanical calculation — the one with which this hypothesis is usually asserted — overstates the effect on completed fertility. Modelled properly, moving a natural-fertility population from a high- to a low-morbidity loss regime raises completed fertility by about **6%**, not 15%.

Three qualifications belong inside this verdict.

**The effect exists only where the reproductive span binds, and vanishes where a parity target binds.** This is the mechanism, not a caveat, and it is testable — but the best-designed study located, a Danish registry of 458,475 women followed to 45, observes exactly the controlled-fertility population where the prediction says the effect should be near zero. **No study estimates the contrast the mechanism turns on.**

**For the first transition the sign is inverted.** Falling intrauterine mortality pushed births *up* by about 10% of the size of a decline that halved fertility. B.5 does not explain the first transition; it means the behavioural decline was about a tenth larger than the raw series shows.

**The first study retrieved confirms the diagnosis and fails a wall.** The only published estimate of this chapter's headline quantity computes it by adding fetal deaths to live births, with no replacement and no time cost — and its own authors' Bongaarts index implies most of its larger component is **induced** abortion, which is A.4's. B.5's clean share of it is 3.8%, not 9.4%.

**What this chapter should not be read as saying.** It does not say fetal loss is demographically trivial, and it does not say the evidence is bad. The evidence on how much loss there is, and what causes it, is extensive and often excellent. **It is evidence for a different question than the one this review asks.**

**What would change it:** the regime-contrast design in §5.1 — the effect of a loss on *completed* fertility, estimated in span-binding and target-binding populations with the same design. Historical parish reconstitution supplies one side and the Nordic registries the other, and the Danish study already located supplies half.

---

## 11. Open questions

**PI calls required.** Four scope calls are open; two bear directly on the verdict.

1. **Call 1 — how to score a wrong-signed mechanism.** §8.2 gives a magnitude of 10% with the sign opposing the phenomenon, and neither the protocol's threshold nor the template's bands has a value for it. **This generalises past this chapter and the ruling belongs in `PROTOCOL.md` §4.2.**
2. **Call 2 — the SDT scope-out** against A.11 and A.15.
3. **Call 4 — whether the parameter stream may be credited toward GRADE.** It is currently excluded, which holds the ratings down while the demographic-significance numbers rest on it.
4. **Sign the RA title/abstract gate.** `extraction/fetal-loss-intrauterine-mortality-ra-gate.csv` is generated and unsigned, which blocks the retrieval queue.
5. **Independent three-rater GRADE**, replacing the single-analyst three-lens procedure in §9.

**Evidence and retrieval priorities.**

6. **The regime-contrast study** (§5.1) is the single most informative thing that could be done.
7. **Carry the 1918 pandemic through to completed cohort fertility** rather than stopping at the birth deficit. The Swiss series across four pandemics is the natural setting, because behavioural responses to a nineteenth-century influenza epidemic and to COVID should differ while a biological channel should not.
8. **The historical early-loss rate** is the binding parameter and is currently inferred. Pregnancy-history reconstruction from populations with unusually complete registration might supply it; the Italian post-unification data with misreporting modelled is a template.
9. Retrieve the remaining 49 of 51 priority full texts; extend the screen past 392 of 11,125.

**Studies that do not exist and should.** The design in §5.2, run in two regimes. Every component exists; the two halves sit in different literatures.

---

## 12. References

Generated from `datastore/studies.json` via `make bib`; the per-hypothesis `.bib` is not yet built because no study has passed the RA inclusion gate. Works named above are identified by DOI in `literature/search-logs/fetal-loss-intrauterine-mortality-cold-start-anchors.json` and `-screen-tiers.json`.

---

## Provenance and standing caveats

This chapter is written on 2 of 51 wanted full texts (4%).

**The finding that would survive full retrieval is the accounting result** — that the mechanical calculation overstates by about 2.5× and that the effect is regime-dependent. It is derived from the birth-interval decomposition rather than from the studies, it is computed with an interval and 13 passing tests, and no additional study changes it; what additional studies would change is the **inputs**. **The findings that might not are every study-level characterisation in §6.2**, which come from abstracts, and the primary-cell count of 17, which already fell from 18 on one retrieval.

**Objection over which this chapter was written.** None recorded from the PI, but four scope calls are open and one of them — Call 1, how to score a wrong-signed mechanism — determines how §8.2 should be read.

**Numbers sourced from abstracts rather than full text.** All of §6.2. Two studies have been read; the other 49 priority records have not, and one of the two rerouted on retrieval.

**Deviation from protocol, recorded.** GRADE was produced by one analyst applying three lenses rather than by three independent raters (§9).

**Figures not derived from project data.** The pre-modern fertility range and the FDT decline used as denominators in §8 are conventional magnitudes, not computed here.

**Generated inputs.** Demographic significance: `source/analysis/b5_demographic_significance.py`, 20,000 draws under a fixed seed with 13 passing tests, output to `output/fetal-loss-intrauterine-mortality-demographic-significance.{json,md}`. Extraction, risk of bias, RA gate and retrieval log in `extraction/fetal-loss-intrauterine-mortality-*`. Search logs in `literature/search-logs/fetal-loss-intrauterine-mortality-*`; pipeline `source/build/goldset/115_b5_*` through `120_b5_*`.

**Pipeline state.** Search and screen complete but budget-bounded; RA gate open and unsigned; retrieval 2 of 51; extraction 2 rows; risk of bias 2 assessed; synthesis narrative complete with reasons for not pooling; demographic significance complete, tested and reproducible; GRADE complete with a stated deviation; lay-readability check and PI sign-off open.
