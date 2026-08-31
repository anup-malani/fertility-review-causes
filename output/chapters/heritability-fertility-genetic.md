# Chapter A.18: Genetic and Heritable Variation in Fertility

**Category** · Proximate Causes
**Primary mechanism** · Some of the difference between individuals in how many children they have tracks inherited genetic variation, and natural selection acting on that variation could in principle raise average fertility over generations.
**Cross-references** · D.1.c (cultural evolution — the competing transmission channel) · A.19 (intergenerational transmission — the undecomposed correlation) · B.1 (status and fertility) · A.15/A.16/B.3/B.4 (heritable fecundity traits)
**Status** · TICK-076 · drafted 2026-08-31 · **not PI-reviewed** · written on **56 of 148 wanted full texts (37.8%)**

---

## 1. The claim

**This chapter explores the effect of heritable genetic variation on realized fertility.**

### 1.1 In plain terms

**In plain terms: people differ in how many children they end up having, and part of that difference is inherited from their parents — not learned from them, but passed on biologically — so that if having more children runs in a family for genetic reasons, and people who have more children pass those genes on more often, the average number of children a population has could drift upward over time.**

Three separate things are being claimed there, and it is worth separating them at the start because the evidence for them is completely different.

The first is that the differences between people are partly inherited. Some people have four children and some have none, and the claim is that a portion of that spread — not the level, the spread — tracks something biological passed from parent to child.

The second is that this inheritance could change the average. If people who have more children are passing on whatever makes them have more children, then each generation should contain a slightly larger share of that inherited tendency, and the population average should creep up. This is the half of the claim that would matter for the fertility decline, because the decline is a fall in the average.

The third is not in the original claim at all, and this chapter found that it is the best-supported of the three: how much of the difference between people is inherited **depends on the society they live in**. When everybody has as many children as custom and circumstance dictate, inheritance has little room to show itself. When people choose, whatever they inherited has room to express itself. On that reading the inherited share is a *consequence* of a society changing, not a cause of the change.

### 1.2 Technically

**The parameter this chapter estimates is the narrow-sense heritability of realized fertility, h², measured as a share of between-individual phenotypic variance; and, separately, the per-generation response to selection R = h² × S, measured in children per woman per generation.**

Two estimands, because the registered claim is a conjunction. h² is a variance decomposition within a population at a point in time. R is a shift in a mean across generations. They are different moments of the same distribution, they are estimated by different literatures, and — this is the chapter's organising fact — only R is a claim about fertility decline at all.

The margin is **intensive**: h² decomposes variance in a count (children ever born) or a timing (age at first birth), not a binary transition, except where the outcome is childlessness, which is extensive and is reported separately.

---

## 2. Theoretical mechanism

In the reader's vocabulary: this is a claim about the **variance decomposition** of an outcome, plus a claim about **selection on a correlated latent trait**.

The variance claim is that Var(fertility) = Var_A + Var_C + Var_E — additive genetic, shared environment, and everything else — and that Var_A / Var(total) is meaningfully above zero. Note what this does *not* say. It says nothing about the mean. A population can have h² = 0.4 with a total fertility rate (TFR: the number of children a woman would bear if she experienced current age-specific birth rates throughout her reproductive life) of 6, or with a TFR of 1.3. The decomposition is silent about which.

The selection claim is the breeder's equation, R = h² × S, where S is the selection differential — the covariance between the trait and relative fitness. If genotypes associated with higher fertility are, by construction, over-represented in the next generation, mean genetic propensity rises and measured fertility follows.

**The identity/behaviour split matters here and is unusual.** Neither claim is behavioural in the sense the rest of this review uses. h² is an accounting statement about variance; R is an accounting statement about how a trait mean moves under differential reproduction. Neither describes a decision. What makes A.18 a *hypothesis* rather than an identity is the empirical content of the inputs: whether Var_A is non-zero, and whether S is large enough to move a mean on a timescale that matters.

**What would make the hypothesis wrong.** If the apparent heritability of fertility is shared family environment misattributed to genes, the first conjunct fails. If S on fertility-associated genotypes is near zero — because fertility is under strong environmental control, or because the genetic architecture is too diffuse — the second fails regardless of h². And if h² is large only *because* a society has moved to individual control, then the arrow runs from the demographic transition to the heritability, and A.18 is an outcome of the phenomena rather than an explanation of them.

---

## 3. Search strategy

Reproducible from `literature/search-logs/heritability-fertility-genetic-search-scope.md`. Two axes, GENETIC × FERTILITY, no mechanism axis, per `decisions/2026-06-20-boolean-query-two-axis.md`. Frame 45,491 records, deduplicated to 42,050 distinct works.

**Six walls.** Wall 1 (vs A.19): a parent–child fertility correlation with no decomposition is not evidence for A.18, because it is equally consistent with pure social transmission — only designs that attribute variance to genotype count. Wall 3 (vs B.1): the predictor must be a genetic measure, not achieved status. Wall 4: heritability of a fecundity trait with no fertility outcome is context, not a primary record. Wall 5: a genetic study of a non-fertility phenotype is out unless fertility is an outcome. Wall 6: non-human study organisms are out.

**One wall was declared unenforceable in advance, and the declaration was measured.** The phenotype wall — is the outcome a fertility outcome? — is invisible to a title-only screen: 66% of frame records name no phenotype in their title, and a title-only prescreen would have removed 62% of the frame while destroying eight known-relevant records. The screen therefore ran on abstracts, and abstract-level silence routed to `INSUFFICIENT_INFO` rather than to rejection.

**Two search findings bear on how the chapter should be read.** First, the outcome axis was initially wrong: in the evolutionary-selection literature the fertility outcome is called **fitness**, and the first query lost seven of nine selection anchors before that word was added, taking anchor recall from 64% to 84%. Second, PROTOCOL §5.1's saturation stopping rule fails on this hypothesis — at its 1,000-record threshold the chapter would have captured **31.7%** of its known gold, with the recall curve still climbing at 26% of the frame. The frame was therefore pulled whole rather than truncated.

---

## 4. PRISMA flow

| Stage | n |
|---|---|
| Boolean frame (deduplicated distinct works) | 42,050 |
| Citation-snowball pool, round 1 (25 anchors) | 3,140 |
| Deterministic prescreen survivors | 29,394 |
| Screened at title/abstract | 696 |
| RELEVANT | 262 |
| UNCERTAIN | 57 |
| **Primary-cell studies** | **148** |
| Full text retrieved and usable | 56 (37.8%) |
| **Usable extracted estimates** | **22** |
| Poolable strata (≥3 after stratification) | **0 of 21** |

**Three features of this funnel change how the chapter reads.**

**The citation channel out-performed the boolean channel by 76×.** Screening yield was 53.0% among records both channels reached, against 0.7% in the boolean-only tail. On this hypothesis, provenance beats vocabulary — which is unsurprising once you see that "fertility" means births per woman here, conception rate in animal science, and nutrient status in agronomy, and that the *method* vocabulary is shared with all three.

**Most of the frame was not screened, and the unscreened part is bounded rather than ignored.** A blinded sample of 150 tail records with 12 hidden positive controls returned screener sensitivity of 12/12 and a prevalence of 1/136, implying **≈213 relevant records (95% CI 37–1,176)** left unread. That is stated rather than claimed away.

**The retrieval figure fell on inspection.** An initial 73% was wrong: 46 of those "retrievals" were Cloudflare bot-challenge pages served with HTTP 200 that stripped to between 11 and 303 characters of text. True usable full text is 37.8%.

---

## 5. The ideal design

### 5.1 The ideal estimand

The change in mean completed fertility, in children per woman per generation, produced by selection on a polygenic score constructed specifically for number of children ever born, in a population with complete reproductive histories to age 45, observed across at least two consecutive generations with genotypes measured in both, with the score's association to fertility estimated **within sibships** so that population stratification and genetic nurture are removed.

### 5.2 The design that would identify it

**Source of variation:** Mendelian segregation within families — which allele a sibling receives is random conditional on parental genotype, and independent of everything about the family. **Comparison group:** siblings discordant on the fertility polygenic score. **Identifying assumption, falsifiable:** conditional on parental genotype, the score is independent of the rearing environment; testable by checking whether the non-transmitted parental alleles predict offspring fertility. **Estimating equation:** completed fertility regressed on the within-sibship deviation in the score, with family fixed effects. **Data:** a genotyped multi-generational register with completed fertility for both generations — the Icelandic, Norwegian or Danish registers are the only plausible sources. **Panel length:** two generations, roughly 60 years. **Sample size:** at an R² of the order of 0.015, tens of thousands of sibling pairs.

### 5.3 The distance table

| Study | Exposure | Outcome | Horizon | Assignment | Distance |
|---|---|---|---|---|---|
| Within-family UK Biobank (h² = 0.27) | anonymous variance, not a fertility PGS | children ever born ✓ | one generation | **within-family ✓** | close on assignment, far on exposure |
| Tropf et al. mega-analysis | anonymous variance | CEB ✓ | one generation | population | far |
| Ísleifsson et al., Iceland | anonymous variance | lifetime reproductive success ✓ | **multi-generational ✓** | within-family ✓ | closest available |
| Briley et al., genotype × cohort | anonymous variance | completed fertility ✓ | cross-cohort | twin | far on exposure |
| Sociogenomics PGS (R² ≈ 0.015) | **fertility PGS ✓** | CEB/AFB ✓ | one generation | population | far on assignment |
| Bangladeshi parity GWAS | anonymous variance | parity ✓ | one generation | population | far |

**No study implements the ideal design, and the gap is the chapter's central finding.** The nearest is Ísleifsson et al., which has the multi-generational horizon and the within-family assignment, and whose exposure is an anonymous variance component rather than a fertility-specific score. Nothing in the evidence base estimates the registered estimand — a selection response on fertility-associated genotypes — at all.

---

## 6. Included studies

22 usable estimates from the 56 retrieved full texts. The complete table is `extraction/heritability-fertility-genetic.csv`; every numeric cell carries the verbatim sentence it was read from.

| Study | Design | Estimand | Estimate |
|---|---|---|---|
| Within-family UK Biobank | sibling IBD regression | h², number of children | **0.27 (SE 0.11)** |
| Ísleifsson et al., Iceland | pedigree IBD REML | h², lifetime reproductive success | **0.137 (0.02)**, superseded → **0.00 (0.05)** |
| Tropf et al., mega-analysis | GREML | h²_SNP, CEB | **0.038 (0.0097)** → **0.22 (0.026)** with cohort |
| Tropf et al. 2015 | GREML | h²_SNP, CEB | 0.10 (0.05) |
| Childlessness, sexual dimorphism | GREML, twin sample | h², childlessness | 0.455 (CI 0.341–0.569) |
| Day et al. | GREML | h²_SNP, age at first birth | 0.290 (0.015) |
| Framingham | pedigree | h², CEB | 0.09 (P = 0.03) |
| Brigos-Barrios et al. | GREML | h²_SNP, reproductive success | 0.03 (0.0014) |
| Bangladeshi parity GWAS | GREML | h²_SNP, number of children | **0.149 (SE 0.24), n.s.** |
| Historical sibling cohorts | DeFries–Fulker | h² by cohort, completed fertility | female **0.39 → 0.46**; male **0.37 → 0.07** |
| Briley et al. | twin | cohort-interaction term | **−.032 (.014) spline / +.016 (.009) quartic** |
| Sociogenomics of PGS | population PGS | variance explained | **R² ≈ 0.015** |
| Cognitive genetic factors | population PGS | PGS → fertility β | **−0.045 (p = .11)** |

### The naive estimator, and why disagreements are resolved rather than averaged

**The naive estimator in this literature is the parent–child fertility correlation.** An author who did not think hard would observe that people whose parents had many children tend to have many children, and call the difference heritable. It conditions on nothing that separates transmission channels: the identical correlation is produced by shared genes, by shared upbringing, by inherited wealth, and by a transmitted norm. Its bias is **upward** and its magnitude is not small.

Thirteen of the 37 gold-set records that the production query correctly refused were exactly this design. Wall 1 exists to route them to A.19, and among included studies `decomposes` is yes 141 / cannot_tell 7 / **no 0**.

**The disagreement that matters is not between studies but within one.** Ísleifsson et al. report h² = 0.137 (SE 0.02) for lifetime reproductive success from IBD-based REML on 8,456 Icelandic full-sibling pairs. They then add a family effect, let it compete with relatedness, and report f² = 0.129 (0.03) with **a genetic effect of 0.00 (0.05)** — concluding, in their own words, that the 0.137 "was based solely on shared family effects among full siblings and was not due to shared genes."

That is the naive estimator's bias, measured inside a single paper, on the best pedigree data available. Averaging 0.137 into a pool with the other estimates would manufacture exactly the false middle §2.2 of the template warns against. **The corrected estimate is 0.00**, and it is reported as the authors' preferred value.

The same pattern separates the population and within-family estimates across studies: population SNP-heritabilities cluster at 0.03–0.10, the within-family estimate is 0.27, and classical twin estimates on childlessness reach 0.455. These are not heterogeneous measurements of one parameter. They are estimators with different and known biases, and the chapter reports them stratified.

---

## 7. Quantitative synthesis

### 7.1 The answer in plain terms

**No pooled number is reported, because the studies do not measure the same thing.** Twenty-two usable estimates fall into twenty-one different combinations of quantity, outcome and design; the largest group contains two. Averaging a share-of-variance with a per-standard-deviation score effect and a genetic correlation would produce a number that means nothing.

What the evidence does support, stated plainly: **some of the difference between people in how many children they have is inherited, the amount is modest, and the best-designed study finds none of it once shared family upbringing is allowed to compete.** The strongest single result in the chapter is that the inherited share *changes with the society* — which is a finding about the transition acting on genetics, not genetics acting on the transition.

### 7.2 The estimate

Thirteen heritability estimates, range **0.00 to 0.455**, and the range is structured rather than noisy:

- **Population molecular estimates** (GREML on unrelated individuals): 0.03–0.10 for children ever born.
- **Within-family estimates** (sibling IBD, immune to stratification and genetic nurture): 0.27 (SE 0.11).
- **Classical twin estimates**: up to 0.455 for childlessness, resting on the equal-environments assumption.
- **The best pedigree estimate**: 0.00 (0.05) once shared family effects compete.
- **The only non-European-ancestry estimate**: 0.149 (SE 0.24), **not significant**.

**Poolability: 0 of 21 strata meet the ≥3 test after stratification.** Applied before stratification the 22 estimates would have looked comfortably poolable. This is a narrative synthesis by necessity, and the necessity is a property of the literature.

**The registered exposure is barely measured.** Only **9 of 148** primary studies measure a genotype associated with fertility itself; 36 measure selection on a correlated trait such as education or psychiatric liability, and 102 decompose an anonymous variance component naming no variant. Where a fertility polygenic score is used, it explains **R² ≈ 0.015 — about 1.5% of variance** — and its association with fertility in one study is **β = −0.045 (p = .11)**, against educational attainment's β = −0.32 (p < .001) in the same model.

**Risk of bias: 18 of 22 estimates SERIOUS, 4 MODERATE, none LOW.** The binding domain is gene–environment correlation: for the two-thirds of the evidence that is an anonymous variance component, "heritability of number of children" absorbs the heritability of education, health and partnering upstream of fertility. That is a property of the quantity, not a defect in the studies, and no design removes it.

---

## 8. Demographic significance

**The phenomenon to be explained is measured in children per woman; this mechanism offers, for its first conjunct, a share of between-individual variance — a quantity with no numerator for a change in a mean.**

That units check settles most of the section before any arithmetic. A heritability cannot be divided by a fall in the total fertility rate, because it is not a fall in anything. The only quantity in this hypothesis denominated in children per woman is the **response to selection**, R = h² × S, and the whole of the demographic-significance case rests on it.

R needs two inputs. The chapter has h², in quantity. **It does not have S** — the selection differential on a fertility-associated genetic measure. That cell held six screened studies; one was retrieved; that one turned out to be a coalescent simulation whose outcomes are genealogy-tree shape and effective population size, and it was reclassified out. The three selection quantities that were extracted are a gradient on height, a gradient on body mass index, and an opportunity-for-selection index by wealth class — selection on **phenotypes**, not on a fertility genotype. Substituting one would answer a different question.

**What is computable is the inversion.** At the largest observed heritability, S would have to exceed **0.11 times the observed decline, per generation**, for the genetic response to reach the 10% significance threshold over the SDT's two generations. At the Iceland authors' preferred h² = 0.00, **no value of S produces any response at all.** The §4.2.1 denominator — the fall in completed fertility over each phenomenon's full definitional window, from the Human Fertility Database — is not sourced on this branch, so the inversion is reported per unit of denominator rather than as a share; naming a denominator I did not source is the error §4.2.1 rule 4 exists to prevent.

### 8.1 Pre-modern

**For pre-modern variation, the verdict is NOT ASSESSED, because the cell that could carry a number is contingent on an unresolved protocol question about units.** PM is the one phenomenon whose §4.2.1 denominator is a *range* rather than a change, so a variance share is at least the right kind of quantity for it. But h² is a within-population, between-individual variance, while §4.2.1's PM denominator is a range *across* populations and §2's other clause is within-population *over time*. It matches none of the three as written. The question is with the PI.

One caution attaches to that cell if it opens: the share would be close to definitional. h² *is* the share of within-population variance attributable to genotype, so dividing it by a within-population variance denominator returns h², and the 10% threshold reduces to "is h² ≥ 0.10" — which most twin estimates clear. It would read as *significant* while meaning far less than that word means anywhere else in this review.

### 8.2 First Demographic Transition

**For the FDT, the verdict is NOT ASSESSED, because the selection differential on fertility-associated genotypes is absent from the evidence base.** Three generations at the observed heritability range would require S above 0.073 times the observed decline per generation to reach significance; whether any plausible S approaches that is precisely what the unretrieved studies would settle.

### 8.3 Second Demographic Transition

**For the SDT, the verdict is NOT ASSESSED, for the same reason: no study in the evidence base estimates S on a fertility-associated genetic measure.** This is the phenomenon the hypothesis was registered against, and it is the one the evidence is least able to speak to.

**NOT ASSESSED is not a polite way of saying small.** No number is withheld here because it turned out to be near zero; no number exists because the inputs were never estimated. A reader who takes "not assessed" to mean "negligible" has learned something the evidence does not say — and would be surprised to find that the arithmetic, if S were ever measured, could in principle clear the threshold at the upper end of the heritability range.

---

## 9. GRADE rating

> **The three independent raters required by PROTOCOL §5 step 11 have not been run.** What follows is one rater. One model arguing several positions surfaces contingencies but is not independence, and calling it a panel would misrepresent the process.

> **GRADE §4.1 has no band for two of these arms.** Its levels are identification strategies — RCT, natural experiment, IV/DiD/RD, "correlational only". A classical twin design or a GREML decomposition is none of them, so the letter of the table puts a competent variance decomposition at *Very low: correlational only*, which tells a reader the literature is badly identified when the truth is that it answers a different question well. `NOT RATEABLE — non-effect estimand` is used instead, and the amendment is with the PI.

| Arm | Rating | Downgrades named |
|---|---|---|
| Conjunct 1 — heritability | **NOT RATEABLE — non-effect estimand** | not applicable: the bands do not fit the quantity |
| Conjunct 2 — selection response | **NO EVIDENCE — cell empty** | not *Very low*: that describes weak evidence, this is absent evidence |
| Conjunct 3 — moderation | **LOW** | risk of bias (18/22 serious); inconsistency (sign flips between specifications within one study, and between sexes within one dataset); indirectness (exposure is anonymous variance, not a fertility genotype); no quasi-experimental design available |

| Phenomenon | Causal credibility | Demographic significance |
|---|---|---|
| PM | NOT RATEABLE (h²) | NOT ASSESSED — contingent |
| FDT | NOT RATEABLE (h²) · NO EVIDENCE (response) | NOT ASSESSED |
| SDT | NOT RATEABLE (h²) · NO EVIDENCE (response) | NOT ASSESSED |

---

## 10. Verdict

**A.18's registered claim is a conjunction, and this review can evaluate only half of it. The half it can evaluate is real but demographically inert; the half that would matter is unevaluated, not small.**

Fertility is somewhat heritable. Across thirteen estimates the range runs from 0.00 to 0.455, structured by design rather than scattered: population molecular estimates cluster at **0.03–0.10**, the one estimate immune to population stratification and genetic nurture is **0.27 (SE 0.11)**, and the best pedigree study in the literature — Icelandic national genealogy joined to genotypes — reports **0.00 (0.05)** once shared family environment is allowed to compete with relatedness, having first reported 0.137 before that competition.

**The single number to carry away is 1.5%.** That is the share of variance in fertility outcomes explained by the polygenic scores built for them — the only measure in this literature that corresponds to the exposure A.18 actually registers. Nine of 148 primary studies measure that exposure at all.

None of this bears on the fertility decline. A heritability is a share of the differences between people at a moment; the phenomena this review explains are changes in averages over decades. The quantity that would connect them — the per-generation response to selection — **has no estimate in this evidence base at all**, because the cell that would hold it contained six screened studies, one retrieved, and that one a simulation.

**What would change this verdict:** an estimate of the selection differential on a fertility-specific polygenic score, in a population with completed reproductive histories, measured within sibships. Five such studies were screened into this chapter and none was retrievable. Four of the five are behind bot defences rather than paywalls, and a person with a browser could clear them in an afternoon.

**The finding most likely to survive is one the registered claim does not make.** Heritability of fertility is not a constant: it rises fivefold in molecular estimates once population and birth cohort are modelled, and it moves across historical cohorts — upward for women, downward for men, in the same data. If that holds, then the inherited share of fertility differences is something the demographic transition *produced*, not something that produced it, and A.18 belongs in this review as an outcome of the phenomena rather than an explanation of them.

---

## 11. Open questions

**PI calls outstanding.** (1) Does PM's §4.2.1 denominator admit a within-population between-individual variance numerator? A.9 has the same problem and the answer should serve both. (2) Should GRADE §4.1 gain a `NOT RATEABLE — non-effect estimand` value? (3) §5.1's saturation stopping rule captured 31.7% of known gold here; every chapter that used it has an unmeasured recall problem, checkable with one relevance-ordered pull each. (4) The v5 master-list entry needs its `phenomena` widened to PM/FDT/SDT and its `claim` rewritten as three clauses. (5) The three-rater GRADE panel has not been run.

**Retrieval priorities, in order.** The five unretrieved `PREDICTED_RESPONSE` studies, which are the difference between NOT ASSESSED and a verdict. Then the eight outstanding `H2_MODERATION` records, the arm with the chapter's most defensible finding and its worst retrieval rate (53.8%). The browser-job and proxy-job lists are split in `heritability-fertility-genetic-retrieval-handoff.md`.

**Studies that do not exist and should.** A within-sibship estimate of the association between a fertility-specific polygenic score and completed fertility, in a Nordic register with genotypes in two generations. Nothing in the 696 screened studies does this, and it is the study §5.2 specifies. Second: any estimate of h² for realized fertility outside European-ancestry populations with adequate precision — the one attempt returns 0.149 with a standard error of 0.24.

---

## 12. References

Full bibliography with resolved DOIs in `literature/search-logs/heritability-fertility-genetic-cold-start-anchors.json` (25 anchors, all verified) and the extraction table. Principal works cited above: Ísleifsson et al. (Iceland pedigree); Tropf et al. 2015 (*PLoS ONE*) and 2016 (mega-analysis); Briley, Harden and Tucker-Drob (genotype × cohort); Day et al. 2016 (*Nature Genetics*); Barban et al. 2016 (*Nature Genetics*); Kohler, Rodgers and Christensen 1999 (*Population and Development Review*); Udry 1996 (*PDR*); Howe et al. 2022 (*Nature Genetics*, within-sibship); Rausher 1992 (*Evolution*, environmental-covariance bias in selection differentials).

---

## Provenance and standing caveats

**This chapter is written on 56 of 148 wanted full texts (37.8%).**

**The findings that would survive full retrieval are** the units mismatch between a variance component and a change in a mean, which no study could alter; the structured spread of heritability estimates by design class; the Ísleifsson within-paper correction from 0.137 to 0.00; and the observation that only nine of 148 studies measure the registered exposure. **The findings that might not are** the moderation arm's direction, which already flips between specifications within one study and between sexes within one dataset and is drawn from five of thirteen screened records; and the claim that no selection-response estimate exists, which rests on five unretrieved studies and would be overturned by any one of them.

**An additional 213 relevant records (95% CI 37–1,176) were never screened**, in the boolean-only tail, measured by a blinded sample against a screen of demonstrated 100% sensitivity on hidden controls.

**No numbers in this chapter are sourced from abstracts.** Every estimate in §6 and §7 was read from full text, and each carries its source sentence in `extraction/heritability-fertility-genetic.csv`. Two studies in the primary set were found to be duplicate version pairs retitled between preprint and publication, and are excluded from all counts.

**Objections recorded.** None raised by a person: this chapter has not been PI-reviewed and the RA's 10% extraction verification has not been run. The author's own standing objection is that a chapter reporting NOT ASSESSED on all three phenomena is publishable only if the reader is told, prominently and more than once, that this reflects absent inputs rather than measured smallness — §8 and §10 both carry that sentence deliberately.
