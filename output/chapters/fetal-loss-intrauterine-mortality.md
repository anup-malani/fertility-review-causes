# Chapter: Fetal Loss and Intrauterine Mortality

**Category:** Biological
**Primary mechanism:** Not every conception becomes a live birth, so populations that lose a larger share of pregnancies record fewer births per woman at the same conception rate, and improvements in maternal health raise live-birth fertility without any change in intentions.
**Target phenomena:** Pre-modern and the first demographic transition. No second-transition cell: the modern rise in loss rates runs through the maternal-age composition shift, which belongs to postponement (A.11) and to age-related fecundity decline (A.15).
**Cross-references:** child mortality decline (A.1, the same mortality logic on the other side of the live-birth boundary, and behavioural where this is mechanical); infectious disease and sterility (B.3, the same organisms acting on conception rather than on survival); induced abortion access (A.4, the other way a conception fails to become a birth, and the principal contaminant of the measured series); obesity and metabolic subfecundity (B.4) and endocrine disruptors (B.2, B.6), whose treatments act partly through this channel.
**Draft status:** DRAFT. The search, screen, and demographic-significance computation are complete and reproducible. Full-text retrieval and effect extraction are **not** done, and under PROTOCOL §5 those are human gates: the RA gate worksheet is generated and unsigned, and no PDF has been procured. Every quantitative claim below therefore comes from the parameter model or from screened abstracts, never from an extracted effect size. The GRADE ratings were produced by one analyst applying three lenses rather than by three independent raters, which is a stated deviation.
**Last updated:** 2026-08-11

---

## 1. Verdict

Fetal loss varies enormously across populations and has fallen substantially over the last century and a half, and both facts are well measured. Whether that variation moved completed fertility is a different question, and the answer is that it moved it far less than the arithmetic suggests, in a way that depends on the fertility regime rather than on the loss rate.

| Phenomenon | Causal credibility | Demographic significance | Verdict |
|---|---|---|---|
| Pre-modern | Very low | Partial: +6.2% of completed fertility (95% interval +3.2% to +9.9%) moving from a high- to a low-morbidity loss regime | The mechanism is sound and the parameters are decent, but no study identifies the effect on completed fertility in a pre-modern population. |
| First transition | Low | 10.0% of the observed TFR change **in magnitude, with the opposite sign** | Falling intrauterine mortality pushed births UP across a period when fertility halved. B.5 does not explain the first transition; if it is significant, it deepens the puzzle. |
| Second transition | Not applicable | Not applicable | Scoped out. The age-composition channel is A.11's and A.15's. |

Four findings drive these ratings.

**The mechanical calculation overstates the effect by a factor of about two and a half, and the mechanical calculation is what the hypothesis is usually asserted with.** If a quarter of conceptions are lost and that falls to a tenth, live births per conception rise 20%. But a woman does not get one conception. Over a reproductive career a fetal loss consumes *time* — the gestation elapsed before it, a recovery period, and a fresh wait to conceive — and so lengthens the birth interval rather than deleting a birth. Modelled properly, the same improvement raises completed fertility by about 6%.

**The effect exists only where the reproductive span binds, and vanishes where a parity target binds.** In an uncontrolled-fertility population, time lost cannot be recovered and the effect is real. Where couples stop at a target family size reached well before fecundity ends, they replace the loss and completed fertility is unchanged. This is not a modelling convenience; it is the mechanism, and it predicts that B.5's effect should be largest in pre-modern populations and decay to nothing under controlled fertility. It is also testable, and the single best-designed study located — a Danish registry of 458,475 women followed from age 20 to 45, with completed family size as the outcome — observes exactly the controlled-fertility population where the prediction says the effect should be near zero.

**The exposure is measured with error that correlates with the outcome, in the settings that matter most.** Retrospective pregnancy histories omit losses non-randomly, and worse for early losses, for losses further in the past, and for less-educated respondents. Where induced abortion is illegal or stigmatised, it is reported as spontaneous. Both problems are largest in exactly the pre-modern and transitional settings that carry this chapter's two live cells. The demographic literature has known this since Leridon's 1976 reconsideration and Casterline's 1989 World Fertility Survey review, and a 2023 analysis of 157 surveys across 53 countries now supplies quantified adjustment procedures.

**The literature that would identify the effect barely exists, and this was predicted before the search ran.** A probe of `"fetal loss" AND "natural fertility"` returns three records; `"stillbirth" AND "fertility decline"` returns sixteen. Against that, the clinical literature on miscarriage and stillbirth runs to thousands. Of 392 records screened from the citation frame, 18 fall in a primary cell and 267 in the parameter, measurement, and theory streams. The evidence is abundant on how much loss there is and what causes it, and nearly silent on what it does to the number of children a woman ends up with.

## 2. The Claim and the Mechanism

The claim is that intrauterine mortality is a real determinant of live-birth fertility, and a biological one: it requires no change in what anyone wants. Populations with worse maternal health, more infection, and worse nutrition lose more pregnancies and record fewer births per woman at the same conception rate.

What makes the chapter difficult is that B.5 is defined by a **channel**, not by a treatment. Its named drivers — maternal health, infection, nutrition — are each owned or bordered by another chapter, and its outcome, live births, is the review's common outcome. What B.5 owns is the segment of the reproductive process between conception and delivery. A study belongs here when the quantity doing the causal work is survival of an established pregnancy, whatever moves it. That is why this chapter routes on the margin an estimate bites at rather than on the source of identifying variation: applying the source-of-variation rule used elsewhere in this review would empty B.5, since every one of its drivers is another chapter's treatment.

### The accounting identity is not the effect

Write $B$ for live births, $C$ for conceptions, and $p$ for the probability a conception is lost. For a single conception, $B = C(1-p)$, and this is the form in which the hypothesis is usually stated. It is an upper bound that no population attains.

Over a reproductive career the mean closed birth interval decomposes additively, in the tradition running from Sheps and Menken's 1973 birth-interval models through Bongaarts's 1978 framework and Bongaarts and Potter's 1983 treatment:

$$BI = i + w + g + TA(p), \qquad TA(p) = \frac{p}{1-p}\,(g_L + r + w)$$

where $i$ is postpartum infecundability, $w$ the waiting time to conception, $g$ gestation, $g_L$ the gestation elapsed at a loss, and $r$ the recovery period after one. The expected number of losses per live birth is $p/(1-p)$, not $p$: at a 25% loss rate a woman expects one loss for every three live births, and each costs her roughly eight to eleven months rather than a child.

Whether that lost time costs a birth depends on which constraint binds:

- **Where the reproductive span binds** — uncontrolled fertility, early and near-continuous exposure, childbearing continuing until fecundity ends — lost time cannot be recovered, and the effect on completed fertility is real though much smaller than $(1-p)$ implies.
- **Where a parity target binds** — a desired family size reached well before the span runs out — the couple replaces the loss, and the effect on completed fertility approaches zero. The loss changes the timing of births, not their number.

Every estimate in this chapter is therefore tagged with an estimand level: `ACCOUNTING_SHARE` for the mechanical calculation, `BEHAVIORAL_NET` for the effect on completed fertility after whatever replacement the population actually does. **The two are never combined into one pooled estimate**, and the second is the quantity PROTOCOL §4.2 asks for.

### Three identification problems, in order of severity

**Reverse causation runs through parity and spacing, and it runs the wrong way.** Higher parity and shorter birth intervals raise loss risk, and a woman with more pregnancies has had more opportunities to record a loss. A raw cross-sectional association between measured loss and completed fertility is therefore contaminated *toward a positive sign* — more births produce more recorded losses. A positive raw correlation is a warning about the design, not evidence for the hypothesis. Two studies in the screened set attack this directly: an Egyptian analysis titled, flatly, "High fertility does not cause spontaneous intrauterine fetal loss", and a 1989 study of whether gravidity and age drive the loss gradient in Australian pregnancy histories.

**Loss is partly a selection mechanism.** Over half of early miscarriages carry chromosomal abnormalities. Averted loss does not convert one-for-one into a surviving birth, because part of what is averted would have failed later or produced a non-viable outcome. A 1996 study of stressful life events conditioned on *chromosomally normal* spontaneous abortion, which is the design that separates selection-driven from environmentally driven loss; it is rare.

**The measurement problem is first-order, not a footnote.** Because women with more births have more recent and more salient reproductive histories, reporting quality correlates with the outcome. And a "loss rate" means nothing without the gestational window it is measured over: clinically recognised loss from six weeks is a different quantity from total post-implantation loss, which Wilcox and colleagues put near 31% by hCG assay in 1988, which is different again from stillbirth defined at 20, 22, 24, or 28 weeks. National definitions differ on exactly those thresholds. Quebec's change to its fetal-mortality definition, and its effect on the reported rate, is the cleanest natural experiment on the point.

## 3. How the Evidence Is Organised

The screen sorted records by the margin their estimate bites at. The resulting distribution is itself the chapter's main empirical finding about the field.

| Stream | n screened | What it contains | Role |
|---|---|---|---|
| Primary cells | 18 | Loss → live-birth fertility; exogenous shocks running through intrauterine survival to births; replacement and compensation after a loss | The causal evidence, and the recall denominator |
| Parameter | ~200 | Loss levels, trends, age gradients, gestational distributions; determinants of loss with no fertility outcome | Feeds demographic significance. **Not** evidence for the causal claim |
| Measurement | ~40 | Reporting quality, misclassification, definitional comparability | The risk-of-bias spine |
| Theory and accounting | ~12 | Proximate-determinants models; microsimulation | The framework of §2 |
| Held for full text | 13 | Perinatal composites, undecomposed fecundity, routing deferred | Adjudicated on retrieval |
| Excluded | 94 | Clinical management of recurrent loss, non-fertility outcomes, non-human studies | — |

The parameter stream is larger and better identified than the causal stream. That inverts the usual pattern in this review, where a topic literature is abundant and the parameter scarce, and it has a consequence for how the chapter should be read: **the demographic-significance computation rests on firmer ground than the GRADE rating does.** The parameter stream is not credited toward the GRADE rating, and the two are reported separately so that a reader does not lend the causal claim the precision of the loss-rate literature.

## 4. Search and Screen

Full detail is in `literature/search-logs/fetal-loss-intrauterine-mortality-*`; the pipeline is `source/build/goldset/115_b5_*` through `120_b5_*`.

A reconnaissance probe ran before the scope was fixed (35 OpenAlex queries, zero failed requests, so its zero-hit counts are genuine absences). It established that the demographic seam is thin inside a very large clinical literature, and the scope document was written against that measurement rather than against an expectation.

Thirty-one cold-start anchors were sourced live and passed through three gates: existence, version-of-record, and a book-canon gate. Twenty-five verified. The book gate earned its place — five of this canon's works are monographs and every one returns its own reviews, and for Leridon 1977, Sheps and Menken 1973, and Preston 1978 the review records credit the *books' own authors*, so the author check passes and only the review-shape test rejects. Three defects in the resolver were found by auditing its refusals rather than its acceptances: a Crossref/OpenAlex type-vocabulary mismatch that had silently penalised every OpenAlex record by 90 points, a missing-author state that ranked neutral, and an ISBN check digit misread as a chapter ordinal.

The citation frame took one hop backward and forward from the verified anchors: 11,504 records, deduplicated to 11,125. Routing decoys were forward-cited like every other seed, following the finding on D.2.d that a decoy's neighbourhood is where boundary cases live; 1,888 frame records (16%) exist only because of that, and the decoy clouds ran 68–75% on-topic, at or above the theory canon.

A deterministic two-axis rank then bounded the semantic screen to 392 records: the top 340 by score plus 52 orthogonal-channel bypasses. **This is a budget-bounded screen and 10,733 records went unread.** The residual is characterised in the D1 log; most of it carries no term from one or both axes. Extending the screen deeper is the obvious next increment.

Two validations were run rather than asserted. Four records whose correct routing was known independently — the three monographs the anchor resolver had refused, plus one version duplicate — reappeared inside the frame as cited works, and the screen routed all four correctly. The citation frame thereby recovered Wood 1994, Leridon 1977, and Bongaarts and Potter 1983, so the theory canon is intact despite four unresolved anchors. Separately, of the twelve screened records depending only on a decoy seed, six were routed away.

## 5. What the Primary Evidence Actually Is

No effect sizes have been extracted, because no full text has been retrieved. What follows describes the designs located and what they can bear, and it is deliberately not a results section.

**The shock studies are where identification lives.** The chapter's strongest designs use exogenous variation in intrauterine survival and observe births.

- *Famine.* The Chinese Great Leap famine against involuntary fetal loss in national survey data (*Demography*, 2005); the 1974–75 Bangladesh famine against birth and fertility outcomes (*Demography*, 2014); the Dutch Hunger Winter against stillbirths as a distinct age group in 1935–47 vital statistics (*Population Studies*, 2023); and a 1993 account attributing the post-war Dresden fertility collapse to food-supply failure with concurrent miscarriage epidemics.
- *Epidemics.* The 1918–20 pandemic recurs in five independent settings: US monthly birth series, Taiwan 1906–43, Japan, Arizona birth records, and Lausanne maternity records. Most importantly, a 2025 *Population Studies* analysis follows Swiss general fertility rates from 1871 to 2022 across the 1889–90, 1918–20, 1957, and COVID pandemics and finds births falling six to nine months after each peak, offering miscarriage as the explanation. That is the closest thing this chapter has to a replication design.
- *Conflict and economic shocks.* Civil conflict and gender-specific fetal loss in the *Journal of Health Economics*; Danish spontaneous loss following national economic downturns; the Gulf War and spontaneous abortion in Bahrain.

The recurring weakness is that these designs are strong on the exposure and weak on the estimand. Several identify the shock's effect on *loss* and infer the birth consequence rather than estimating it, and the 1918 literature contains an explicit dispute — a published exchange over whether the 1919–20 natality decline reflects influenza-induced miscarriage or wartime behaviour — which is precisely the confound the chapter cannot dismiss.

**The direct loss-to-fertility studies are few and heterogeneous.** A Moroccan study builds an intrauterine-mortality life table and estimates its effect on women's fertility, which is exactly the chapter's estimand, in an obscure venue that makes retrieval and quality assessment a priority. A Korean study relates pregnancy wastage to fertility in a setting where induced and spontaneous loss are pooled. Two consanguinity designs — Hutterite couples and a historical Swedish population exploiting the 1844 legalisation of cousin marriage — ask whether elevated loss lowers completed fertility, and the Hutterite result is that it does not, because compensating conceptions absorb it. And the Danish registry study of 458,475 women relates early pregnancy complications to completed family size in a controlled-fertility population.

**The replacement studies are the ones that convert an accounting share into a net effect**, and there are five: reproductive compensation among the Hutterites, time to pregnancy and live birth by the interval after an early loss (from a randomised trial's secondary analysis), prior losses and the chance of a live birth in the next pregnancy in a national registry, fertility after recurrent miscarriage in 719 couples, and a life-course study of whether a loss changes subsequent fertility desires and intentions. Without this stream the chapter cannot compute the quantity it needs.

## 6. Quantitative Synthesis

**No pooled estimate is produced, and none should be.** PROTOCOL §5.9 directs meta-analysis when three or more studies carry extractable effect sizes. The primary cells hold eighteen records, which clears that count, but they do not share an estimand: they differ on the estimand level (mechanical versus post-replacement), on the loss window (pre-clinical, clinically recognised, or late fetal), on the outcome (births, completed parity, intentions), and on the fertility regime, which the model in §2 says determines the effect's very existence. Pooling across those would produce a number with no interpretation. A forest plot assembled from incommensurable quantities is worse than no forest plot, because it looks like a result.

The synthesis is therefore the parameter model of §7, with the primary studies used to discipline its inputs and to test its central prediction.

## 7. Demographic Significance

Computed by `source/analysis/b5_demographic_significance.py` (20,000 Monte Carlo draws, fixed seed, 13 passing tests). Every figure is a median with a 95% interval across the parameter ranges, because the inputs are genuinely uncertain.

| Phenomenon | Loss-rate change | `ACCOUNTING_SHARE` (upper bound) | `BEHAVIORAL_NET` | Overstatement |
|---|---|---|---|---|
| Pre-modern | 0.20–0.28 → 0.10–0.15 | +15.2% | **+6.2%** (+3.2% to +9.9%) | 2.5× |
| First transition | 0.16–0.24 → 0.09–0.13 | +11.3% | **+4.5%** (+2.0% to +7.7%) | 2.5× |

### 7.1 Pre-modern

Moving a natural-fertility population from a high-morbidity to a low-morbidity loss regime raises completed fertility by about 6%, or roughly 0.37 of a birth against a pre-modern total fertility near six. The mean birth interval moves by about two months.

**Verdict: partial.** The effect is real and not trivial, and it is smaller than the other components of the birth interval — postpartum infecundability and the waiting time to conception each move it more. It clears no threshold in PROTOCOL §4.2 decisively on its own, and it is contributory rather than sufficient against pre-modern cross-population fertility variation of roughly four to eight births.

### 7.2 First transition

The decline in intrauterine mortality across the transition raises births by about 4.5% where the span binds. Applied to a starting TFR of 5.5, that is **+0.25 births per woman**, against an observed decline of −2.5.

**The sign is inverted, and the magnitude lands almost exactly on the threshold.** At 10.0% of the observed change, B.5 sits on PROTOCOL §4.2's 10% significance line — which makes the verdict knife-edge and sensitive to the historical early-loss rate, the least observed parameter in the model. What the number means is not that B.5 explains 10% of the first transition, but that the *behavioural* component of the decline was about 10% larger than the raw TFR series shows, because a rising share of conceptions was surviving while births fell. The hypothesis deepens the puzzle other chapters are trying to solve rather than helping to solve it.

How this should be scored is Call 1 in the search scope and is open with the PI. It generalises past this chapter: any hypothesis whose predicted sign opposes the phenomenon it is assigned to faces it, and the ruling probably belongs in PROTOCOL §4.2 rather than here.

### 7.3 Second transition

No cell. Scoped out against A.11 and A.15 (Call 2).

### 7.4 What would move these numbers

The observation window governs everything. These are clinically recognised losses. Total post-implantation loss is near 31%, but a conception lost before recognition costs little more than a cycle and cannot lengthen a birth interval by much; substituting the total-loss figure is the most common way this calculation is done wrong and would inflate every number above. The nineteenth-century early-loss rate is unobserved — historical sources record stillbirths, not miscarriages — and is the largest single source of uncertainty in the FDT row. Under-reporting biases recorded rates downward, so the historical contrast may be understated; the 53-country adjustment procedures would sharpen it. Induced abortion contaminates the measured series in the direction of overstating spontaneous loss.

## 8. GRADE

**Deviation from protocol, stated plainly:** PROTOCOL §5.11 requires a panel of three independent raters. These ratings were produced by one analyst applying three lenses in sequence — evidence-quality, identification, and transportability — which is not the same thing and does not carry the same weight. Independent re-rating is an open item.

| Phenomenon | Rating | Justification |
|---|---|---|
| Pre-modern | **Very low** | No study identifies the effect of intrauterine mortality on completed fertility in a pre-modern population. The mechanism is well specified and the parameters are decent, but the evidence is a model populated by parameter estimates, and the exposure in every historical source is measured with error that correlates with the outcome. |
| First transition | **Low** | Several historical series document the decline in fetal mortality with individual-level records — Derbyshire around 1900, Bern 1880–1922, Cumbria 1950–92, Italian regions after unification with misreporting modelled, Denmark after 1940. The pandemic and famine shocks supply quasi-experimental variation, and the Swiss 1871–2022 series repeats it across four pandemics. What is missing is any design that carries the shock through to completed fertility rather than to loss, and the one published exchange on the 1918 case disputes the channel. |
| Second transition | Not applicable | — |

The parameter stream would rate higher on its own and is deliberately not credited here (Call 4 in the search scope).

## 9. Verdict

| | Causal credibility | Demographic significance |
|---|---|---|
| Pre-modern | Very low | Partial (+6.2%, interval +3.2% to +9.9%) |
| First transition | Low | 10.0% of the observed change in magnitude, **opposite sign**; scoring pending Call 1 |
| Second transition | Not applicable | Not applicable |

## 10. Open Questions and Recommended Studies

**What would change the verdict, in order of value.**

The single most informative study would test the regime-dependence prediction directly: estimate the effect of a loss on *completed* fertility separately in span-binding and target-binding populations, using the same design. The prediction is a substantial effect in the first and approximately zero in the second. Historical parish reconstitution on one side and the Nordic registries on the other could do it, and the Danish registry study already located supplies half.

Second, the 1918 pandemic deserves a design that carries the shock through to completed cohort fertility rather than stopping at the birth deficit. The published dispute over whether the 1919–20 natality decline was miscarriage or behaviour is unresolved, and the Swiss series across four pandemics is the natural setting for resolving it, because behavioural responses to a nineteenth-century influenza epidemic and to COVID should differ while a biological channel should not.

Third, the historical early-loss rate is the binding parameter and is currently inferred. Serological or skeletal evidence will not supply it, but pregnancy-history reconstruction from populations with unusually complete registration might, and the Italian post-unification data with misreporting explicitly modelled is a template.

**What this chapter should not be read as saying.** It does not say that fetal loss is demographically trivial. It says that the mechanical calculation with which the hypothesis is usually asserted overstates it by roughly two and a half times, that the residual effect is real but modest and regime-dependent, and that for the first demographic transition it points the wrong way. Nor does it say the evidence is bad: the evidence on how much loss there is, and on what causes it, is extensive and often excellent. It is simply evidence for a different question than the one this review asks.

## 11. References

Generated from `datastore/studies.json` via `make bib`; the per-hypothesis `.bib` is not yet built because no study has passed the RA inclusion gate. Works named in the text above are identified by DOI in `literature/search-logs/fetal-loss-intrauterine-mortality-cold-start-anchors.json` and `-screen-tiers.json`.

---

## Appendix: pipeline state and open gates

| PROTOCOL stage | State |
|---|---|
| 2. Search strategy and scope | Complete; four scope calls open with the PI |
| 3. Search and AI screening | Complete, budget-bounded at 392 of 11,125 |
| 4. RA title/abstract review | **Open.** `extraction/fetal-loss-intrauterine-mortality-ra-gate.csv` generated, unsigned |
| 5. Full-text retrieval | **Open.** No PDF procured |
| 6. Full-text screen | Blocked on 5 |
| 7. Extraction | Blocked on 5 |
| 8. Risk of bias | Blocked on 5 |
| 9. Synthesis | Narrative complete; no pooling, with reasons |
| 10. Demographic significance | Complete, tested, reproducible |
| 11. GRADE | Complete with a stated deviation on rater independence |
| 12. Chapter draft | This document |
| 13. RA lay-readability check | Open |
| 14. PI sign-off | Open |
