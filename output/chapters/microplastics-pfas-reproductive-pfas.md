# PFAS and Reproductive Function

**Category:** Biological
**Primary mechanism:** Per- and polyfluoroalkyl substances reduce the per-cycle probability of conception in exposed women and impair semen quality in exposed men, so near-universal exposure lowers realised fertility without changing what anyone wants.
**Cross-references:** Companion chapter on **microplastics**, which shares this hypothesis entry (`HYPOTHESES-v5.md` §B.6) and must be read with it — the two fail for opposite reasons and their verdicts are not commensurable. Also B.2 legacy endocrine disruptors (which owns phthalates, and to which one of this hypothesis's listed seminal works actually belongs) · A.17 assisted reproduction · A.16 paternal age and sperm quality.
**Status:** TICK-068. Rewritten against `docs/chapter-template.md` on 2026-08-29. The three-rater GRADE panel required by `PROTOCOL.md` §5.11 has not run; five PI calls are open on the shared scope, and three citation corrections are owed to TICK-001. Written on 119 of 239 wanted full texts (50%), with PFAS papers reached less often than microplastics papers (51% against 59%).

---

## 1. The claim

This chapter explores the effect of PFAS exposure on fertility.

### 1.1 In plain terms

In plain terms: certain industrial chemicals used to make things waterproof and non-stick do not break down. They build up in the blood and stay there for years, and nearly everyone in an industrialised country has some. The claim is that they interfere with the machinery that makes eggs and sperm, so people conceive less easily — no one having chosen anything.

There is a trap in this that decides the whole chapter, and it is worth following slowly.

**The body gets rid of these chemicals mainly through pregnancy, breastfeeding and menstruation.** So a woman who has already had a child has *less* of the chemical in her blood, precisely because she had the child. Now compare women with high levels against women with low levels and ask who has had fewer children. The high-level group will look worse — but partly because having children is what lowered the other group's levels in the first place.

The comparison runs backwards, and it runs backwards by an amount nobody can easily calculate. The one clean way round it is to look only at women who have never given birth, so nothing has been flushed out yet. **Two research teams did that, in different countries. Both found their result disappeared.**

There is also a simpler problem. These chemicals were largely phased out after 2002 and blood levels have fallen by more than three quarters. Birth rates fell too, over the same years. If the chemicals were holding fertility down, removing them should have pushed it up.

### 1.2 The claim precisely

The parameter this chapter estimates is the change in the per-cycle probability of conception, and thereby in completed fertility in births per woman, caused by an increase in serum PFAS concentration, signed so that a negative value means fewer births.

The chapter is scoped to the **SDT** (the Second Demographic Transition, roughly 1965 onward). There is no **PM** (pre-modern) cell — industrial production began in the late 1940s — and no **FDT** (First Demographic Transition) cell, since production volumes before 1965 were negligible against the reproductive-age population.

**The mechanism creates the identification problem, and this is the chapter's organising fact.** PFAS resist metabolic breakdown and persist for years — Olsen and colleagues (2007) measured serum half-lives of several years in retired fluorochemical workers, so a single exposure keeps acting long after it ends. **The body clears them through three routes that are all reproductive: transfer across the placenta, lactation, and menstrual blood loss.** Brantsæter and colleagues (2013) measured this directly, showing that **a woman's parity predicts her serum concentration.**

**Having children therefore lowers PFAS levels**, so any comparison of high-PFAS and low-PFAS women partly compares women who have already given birth against women who have not. Rickard and colleagues (2021) put elimination in the title of their review, so the field recognises the difficulty.

**This makes parity handling the field that decides whether a study speaks to the hypothesis at all**, and the distinction is not between good and better adjustment but between two different quantities:

- **Restricting to women who have never given birth removes the backwards pathway.**
- **Adjusting for parity as a control variable does not**, because parity lies on the path from earlier childbearing to current exposure, and controlling for a mediator of the reverse pathway can introduce a second bias rather than remove the first.

**This was committed before any study was read**, and the restricted and unrestricted analyses are reported as separate tracks throughout.

**Margin.** Extensive, at the level of conception per cycle.

**What would make the hypothesis wrong.** It is wrong if the association vanishes once the reverse pathway is closed by restriction — which §7.2 reports happened in both cohorts that tested it — or if exposure and fertility move together rather than apart, which §8.3 reports for the United States since 1999.

---

## 2. Theoretical mechanism

In the reader's own vocabulary: a persistent, near-universal exposure acting directly on the biological capacity to conceive, with no price, no preference and no choice in it.

**The mechanism is the strongest part of the case, and it is not what the rating turns on.** The compounds bind to albumin and to hormone transport proteins, and Ding and colleagues (2020) review evidence that they alter ovarian steroid production and follicle development. Two studies in this review exposed human cells directly: one found altered steroid synthesis in primary granulosa cells, another impaired spermatogenesis in a stem-cell-derived model.

**A plausible mechanism and a real exposure are compatible with an effect of zero on the population**, and this chapter is a case where the mechanistic evidence is far stronger than the epidemiological evidence and points in a direction the epidemiology does not support.

**What would make the hypothesis wrong** is in §1.2. Both tests have been run — restriction, and the exposure trend — and the hypothesis fails both.

---

## 3. Search strategy

Built from **32 anchor papers, each verified against a live record so that no citation rests on memory.** One hop forward and backward through OpenAlex produced 14,561 records with no failed requests. Every record was scored on two axes — the chemical named and the fertility outcome named — and the top 700 screened **plus every record carrying terms from both axes at any rank**.

| Wall | Rule | Enforceable at title/abstract? |
|---|---|---|
| **W1 Species** | Human subjects only. | Partially — studies of fish and rodents dominate this vocabulary, and this removed most records |
| **W2 Pregnancy safety** | A study of PFAS and birth weight measures a property of **a birth that happened**, not a count of births. | Yes — and this removed the second-largest block |
| **W3 Compound family** | PFAS, not phthalates (B.2) or plasticisers. | Yes |
| **W4 Parity handling** | Restriction to first births and adjustment for parity are **different tracks**, never pooled. | **No — a design fact, and the one that decides the chapter** |

Nine boundary rules in total; the two above removed the most records.

**Three of the four works `HYPOTHESES-v5.md` lists as seminal for this hypothesis did not resolve as written, and one of them is a paper about a phthalate**, which belongs to B.2 rather than here. The corrections are owed to TICK-001 and are recorded in §11.

---

## 4. PRISMA flow

| Stage | Records |
|---|---:|
| Anchor papers, verified | 32 |
| Citation frame, one hop forward and backward | 14,561 |
| After collapsing duplicate versions | 14,296 |
| Screened on title and abstract | 920 |
| Excluded at screen | 462 |
| Held as unclear, retained for audit | 25 |
| Passed the screen | 433 |
| Full text sought | 239 |
| **Full text obtained** | **119** |
| **PFAS studies contributing an effect estimate** | **4** |

Two features change how this funnel should be read.

**The gap between 239 and 119 is a retrieval failure with a specific shape.** Two automated passes reached half the records wanted. **Publishers blocked 38 downloads of papers that are free to read**, and a further 40 sat in PubMed Central as author manuscripts that one route could not fetch and another could. **Retrieval reached PFAS papers less often than microplastics papers, 51% against 59%**, so the comparison between the two halves of this hypothesis rests on slightly thinner coverage of the PFAS side.

**Four studies is the whole evidence base**, and §7 explains why four is not enough to pool even before the parity-track split.

---

## 5. The ideal design

Written before the literature was read, so §6 can be measured against a fixed yardstick.

### 5.1 The ideal estimand

The change in the per-cycle probability of conception caused by an increase in serum PFAS concentration, **among women who have never given birth**, with exposure measured **before conception**, and with exposure variation arising from a source **unrelated to the woman's own reproductive history**.

All three clauses address the same problem from different directions, and no existing study has more than two. The first closes the elimination pathway by restriction. The second fixes the timing, so exposure is not measured after the outcome has begun. **The third is the strongest and the one no study has at all**: if exposure varies because of where a person lives rather than because of what their body has already done, the reverse pathway is broken by design rather than by sample restriction.

### 5.2 The design that would identify it

**Source of variation.** **Point-source contamination.** Communities with serum concentrations one to two orders of magnitude above background from a contaminated water supply or occupational exposure — **Ronneby in Sweden, the Veneto region in Italy, the Mid-Ohio Valley in the United States, and several firefighter cohorts.** The exposure there is caused by a water main or a workplace, not by a reproductive history.

**Comparison group.** Neighbouring communities on uncontaminated supply, or the same community before contamination, matched on the ordinary determinants of fertility.

**Identifying assumption.** Contamination is unrelated to fertility except through PFAS. Falsifiable: pre-contamination fertility trends; a placebo on outcomes the compounds should not affect; and a **dose-response gradient across distance from the source or across water-district boundaries.**

**Estimating equation.** Time-to-pregnancy or completed parity on serum concentration or on residence in a contaminated district, **restricted to first births**, with exposure measured before the attempt.

**Data required.** Serum measurement or a validated residence-based exposure proxy, linked to a fertility outcome, in a contaminated population. **The serum measurements largely already exist** — these communities have been extensively biomonitored.

**Sample size.** With order-of-magnitude exposure contrast, this needs far fewer participants than the background-variation designs, which is what makes it the tractable route.

**What the ideal design excludes.** Adjustment for parity in place of restriction (§1.2). Pregnancy cohorts, where exposure is measured after conception. And any study whose outcome is a property of a birth that occurred — birth weight, gestational age — rather than whether a birth occurred.

### 5.3 Distance from the ideal

| Study | First births only? | Exposure before conception? | Exposure independent of reproductive history? | Distance |
|---|---|---|---|---|
| **Cohen 2023** (Singapore) | **No — adjusted only** | **Yes — preconception** | No | **Right timing, wrong parity handling** |
| **Whitworth 2016** (Norway) | **Yes — restricted** | No — birth cohort | No | **Right parity handling, 226 women** |
| Jørgensen 2014 (Greenland/Poland/Ukraine) | Both tracks reported | No — pregnancy cohort | No | Reports the contrast that decides the chapter |
| Lum 2016 (US) | No — adjusted only | Yes | No | **Wrong outcome** — menstrual cycle length |
| **Contaminated-community cohorts** | — | — | **Yes** | **Not one estimates a fertility outcome** |

**No study implements the ideal design, and the shortfall is precise: Cohen has the timing right and the parity handling wrong; Whitworth has the parity handling right and 226 women. One study with both would move this rating.**

**And the third clause — exposure independent of reproductive history — is satisfied by no study at all, despite the populations existing and being heavily studied.** Across 920 screened records, **not one estimated a fertility outcome in a contaminated community.** Researchers have studied them for cancer, thyroid disease, cholesterol, ulcerative colitis, immune response and birth weight. **A time-to-pregnancy or completed-parity analysis in any of them would produce the first estimate in this literature with exposure variation that parity cannot explain.**

---

## 6. Included studies

| Study | Country | Design | Sample | Outcome | Estimate | Parity handling | Risk of bias |
|---|---|---|---|---|---|---|---|
| Jørgensen 2014 | Greenland, Poland, Ukraine | Pregnancy cohort | 938 | Time to pregnancy, PFNA | **FR 0.80 (0.69, 0.94)** | **None** | Serious |
| Jørgensen 2014 | Greenland | Pregnancy cohort | subset | Infertility over 13 months | **OR 1.53 (1.08, 2.15)** | **None** | Serious |
| **Jørgensen 2014, restricted** | Same cohort | Pregnancy cohort | first-birth women | Both outcomes | **Not replicated** | **Restricted** | Low for this bias |
| Whitworth 2016 | Norway | Birth cohort | 226 | Time to pregnancy, PFOSA | **FOR 0.91 (0.71, 1.17)** | **Restricted** | Low for this bias, imprecise |
| Cohen 2023 | Singapore | Preconception cohort | 382 | Fecundability, PFDA | FR 0.90 (0.82, 0.98) | Adjusted only | Moderate |
| Cohen 2023 | Singapore | Preconception cohort | 382 | Fecundability, PFOS | FR 0.88 (0.79, 0.99) | Adjusted only | Moderate |
| Cohen 2023 | Singapore | Preconception cohort | 382 | Clinical pregnancy, PFDA | OR 0.74 (0.56, 0.98) | Adjusted only | Moderate |
| Lum 2016 | United States | Preconception cohort | 501 | Menstrual cycle length | AF 1.03 (1.00, 1.05) | Adjusted only | Serious, wrong outcome |

Full table with every compound, all 12 rows, in `extraction/microplastics-pfas-reproductive-effects.csv`.

### 6.1 The naive estimator, and why it is reverse-causal by construction

**What is the naive estimator?** Compare fertility between women with high and low serum PFAS.

**It is contaminated by a reverse pathway that is not merely plausible but measured.** Pregnancy, lactation and menstrual loss are the body's main elimination routes, so parity *causes* low PFAS. Brantsæter and colleagues demonstrated the dependence directly.

**The bias runs toward the hypothesis**, and its size is unknown because it depends on how much of the between-woman variance in serum concentration is elimination rather than intake.

**How many included studies escape it? Two, and both lost their result when they did.** This is the chapter's central finding and §7.2 sets it out.

**Adjusting for parity is not an escape**, for the reason in §1.2: parity is a mediator of the reverse pathway, and conditioning on it can open a second bias rather than close the first. Three of the four studies adjust rather than restrict.

### 6.2 The transmission ledger

| Stage | Question | Sign |
|---|---|---|
| Production → human exposure | Established; near-universal | Holds |
| Exposure → measured serum concentration | **Partly determined by the outcome** via elimination | **Reverses** |
| Concentration → impaired conception | The claim; two designs that close the reverse path find nothing | **Absent when tested cleanly** |
| Impaired conception → births forgone | A fecundability ratio moves waiting time; converts to a birth only where the span binds | **Attenuates severely** |
| Aggregate → the phenomenon | Exposure **fell** 87% while fertility fell 18% | **Wrong direction** |

The second row is a reversal rather than an attenuation, and the last is the sign problem in §8.3.

---

## 7. Quantitative synthesis

### 7.1 The answer in plain terms

Four studies, and the important thing about them is not their average but a comparison two of them made against themselves.

When researchers looked at all women, they found that those with more of the chemical in their blood took longer to conceive. When the same researchers looked only at women who had never given birth — the group whose blood levels cannot have been lowered by a previous pregnancy — the finding went away. A second team, in a different country with a different cohort, did the same thing and got the same result: nothing.

That is exactly what you would expect if the original finding was the backwards effect described in §1.1 rather than a real one.

The strongest study pointing the other way measured the chemicals before women started trying, which fixes a different problem — but it did not restrict to first births, so it does not address this one.

### 7.2 The estimate

**No pooling.** `PROTOCOL.md` §5.9 requires at least three estimates sharing a chemical family, an outcome type, a sex **and a parity-handling status**. The restricted track holds two studies and one reports no number at all. **A forest plot built across the restricted and unrestricted tracks would average a result against its own correction.**

**The finding is the disagreement between the tracks, and both cohorts that tested it reported it themselves.**

| Cohort | Unrestricted | Restricted to first births |
|---|---|---|
| Jørgensen 2014, PFNA, fecundability | FR 0.80 (0.69, 0.94) | **Not replicated** |
| Jørgensen 2014, PFNA, infertility | OR 1.53 (1.08, 2.15) | **Not replicated** |
| Whitworth 2016, PFOSA, fecundability | FOR 0.85 (0.83, 1.09) | FOR 0.91 (0.71, 1.17) |

Jørgensen and colleagues state that among women having their first birth, the associations found in the whole sample could not be replicated. Whitworth and colleagues restricted to 226 first-birth women and found nothing, for PFOSA or any other compound measured. **Two teams, in different countries on different cohorts, each found that removing women who had already given birth removed the association. That is the pattern the elimination mechanism predicts.**

**Cohen and colleagues provide the strongest counterweight and the clearest illustration of why the distinction matters.** They measured exposure before conception, which fixes the timing problem troubling the two pregnancy cohorts, and found reduced fecundability for several compounds. **They adjusted for parity rather than restricting on it.** Their result belongs in the unrestricted track, and it stands as the best available argument that the association survives better designs.

**Publication bias could not be assessed.** Four studies do not support a funnel plot, and the Egger test needs ten.

---

## 8. Demographic significance

The phenomenon to be explained is measured in whole children — the SDT is a fall of roughly one and a half births per woman; this mechanism offers a fecundability ratio whose only clean tests return nothing, **and whose exposure moved in the wrong direction across the period being explained.**

**The verdict turns on the direction of the exposure trend, and no effect size is needed to reach it.**

Botelho and colleagues (2025) report two decades of US national biomonitoring. Between 1999 and March 2020, **serum PFOS fell 87%, PFOA 74%, and PFHxS 52%**, following the industrial phase-out begun in 2002. Over the same years the **US total fertility rate fell from 2.007 to 1.641, a drop of 18.2%** (World Bank, cached in `data/raw/`).

**Exposure and fertility fell together. The hypothesis requires them to move apart.** If PFAS suppress fertility, removing most of the exposure should have raised fertility across exactly the window in which fertility dropped.

Taking the largest unrestricted estimate at face value — Cohen's fecundability ratio of 0.88 per quartile, and reading an 87% fall in concentration as roughly three quartile steps downward — **the implied change is a fecundability gain near 47%.** Granted its own contested number, **the hypothesis predicts that the post-2000 American fertility decline should not have happened.**

Three considerations make that calculation generous, and they are stated rather than adjusted for. The estimate does not survive parity restriction. A fecundability ratio moves the time a couple waits and converts into a birth forgone only where a woman runs out of reproductive years, which most exposed women do not. And mapping a percentage change in concentration onto quartile steps is rough — it is used to show the sign problem is large, not to calibrate anything.

**The endogeneity check** is clean in the aggregate — PFAS production is not caused by the fertility decline — but the *individual-level* reverse pathway in §1.2 is the sharpest in the review, and it is the reason the individual estimates cannot be used.

**No decomposition share is computed**, and under `PROTOCOL.md` §4.2.1 none should be: **building a share on an estimate this chapter's own evidence identifies as partly reverse-causal would dress arithmetic as a finding.**

**One route to a different answer remains open.** The falling series covers the **legacy** compounds. Manufacturers replaced them with short-chain substitutes as they withdrew, and **national biomonitoring did not track most substitutes across this window.** The replacement exposure series is **unknown rather than flat**, and no study estimates a fertility outcome for any replacement compound. A PFAS contribution to recent fertility decline survives only there.

### 8.1 Pre-modern fertility variation

For pre-modern variation, the verdict is NOT ASSESSED, because the phenomenon is out of scope for this hypothesis in the registry: industrial production began in the late 1940s.

### 8.2 First Demographic Transition

For the First Demographic Transition, the verdict is NOT ASSESSED, on the same ground.

### 8.3 Second Demographic Transition

For the Second Demographic Transition, the verdict is NEGLIGIBLE, because exposure to the legacy compounds fell by 74–87% across the period while fertility fell 18.2%, so the mechanism's own movement was in the wrong direction and cannot have contributed to the decline.

**Slope sufficiency: insufficient, and wrong-signed.** This is the second chapter in the review to return a wrong-signed result, after B.5, and **the vocabulary handles it no better here.** NEGLIGIBLE is used because the mechanism's contribution to the *decline* is not merely small but of the wrong sign — but a reader will take NEGLIGIBLE to mean "a small positive contribution", which is not what the evidence says. **B.5's Call 1 — how to score a mechanism whose predicted sign opposes the phenomenon — applies here identically, and the ruling belongs in `PROTOCOL.md` §4.2.**

The one live route is the replacement compounds, for which no exposure series and no effect estimate exists.

---

## 9. GRADE rating

| Phenomenon | GRADE | Downgrades | Demographic significance |
|---|---|---|---|
| PM | **No evidence** | Out of scope in the registry. | NOT ASSESSED |
| FDT | **No evidence** | Same. | NOT ASSESSED |
| **SDT** | **VERY LOW** | *Inconsistency*, and in its sharpest possible form: **the disagreement is within cohorts rather than between them**, between the unrestricted and restricted analyses of the same data. *Risk of bias*: the reverse pathway from parity to exposure is measured, and three of four studies adjust rather than restrict. *Imprecision*: four studies; the restricted track holds two, one reporting no number. | NEGLIGIBLE |

**On design alone the evidence would sit at LOW**, since it consists of cohorts with covariate control and no identifying variation. **It does not reach LOW because the disagreement is not noise across settings but the signature of the confounding the mechanism predicts.**

`PROTOCOL.md` §5.11 requires three independent raters, and **that panel has not run. One analyst writing three opinions in one sitting is one rater**, and recording it otherwise would misstate how the rating was produced.

---

## 10. Verdict

PFAS are near-universal, persist for years, and have a well-supported biological mechanism. **The epidemiological evidence that they lower fertility does not survive the one correction the mechanism itself demands.**

**The one number to carry away: 87%.** That is how far US serum PFOS fell between 1999 and 2020 — while fertility fell 18.2% over the same years. **Exposure and fertility moved together; the hypothesis requires them to move apart.**

Three qualifications belong inside this verdict.

**Two cohorts tested the association against its own confound and both lost it.** Because the body clears PFAS through pregnancy, lactation and menstruation, having children lowers exposure. Restricting to women who have never given birth closes that pathway, and when Jørgensen and Whitworth did so, in different countries on different cohorts, the associations did not replicate.

**The strongest counterweight fixes a different problem.** Cohen measured exposure before conception, which is right, and adjusted for parity rather than restricting, which does not address the reverse pathway and can open a second bias.

**One route remains open and it is a real one.** The falling series covers the legacy compounds; the short-chain replacements were not tracked by national biomonitoring across this window, so their exposure series is unknown rather than flat, and no study estimates a fertility outcome for any of them.

**What would change it:** the design in §5.2 — a fertility outcome in a contaminated community. Across 920 screened records **not one exists**, though these populations have been studied for cancer, thyroid disease, cholesterol, ulcerative colitis, immune response and birth weight, and their serum measurements largely already exist.

---

## 11. Open questions

**PI calls required.**

1. **Five calls are open on the shared B.6 scope**, including whether the PFAS and microplastics halves should be separate registry entries. **They fail for opposite reasons — one because the evidence points the wrong way, one because it does not exist — and their verdicts are not commensurable.**
2. **How to score a wrong-signed mechanism.** Identical to B.5's Call 1. NEGLIGIBLE reads as "small and positive" and the evidence says "wrong direction". The ruling belongs in `PROTOCOL.md` §4.2.
3. **Three-rater GRADE** has not run.

**Evidence priorities.**

4. **A fertility outcome in a contaminated community** — Ronneby, the Veneto, the Mid-Ohio Valley, or a firefighter cohort. This is the single most valuable study that could be run, the exposure variation is unrelated to reproductive history, and the biomonitoring already exists.
5. **A first-birth cohort with exposure measured before conception.** Cohen has the timing right and the parity handling wrong; Whitworth has the parity handling right and 226 women.
6. **The replacement compounds need an exposure series before they need an effect estimate.** Nobody can compute a demographic contribution for GenX or the short-chain substitutes without knowing how population exposure has moved.
7. Recover the 38 publisher-blocked and 40 PMC author-manuscript retrievals; PFAS coverage is thinner than microplastics coverage.

**Three citation corrections owed to TICK-001.** `HYPOTHESES-v5.md` cites a Lancet Commission on Reproductive Health (2025) **that does not exist**; the intended work is almost certainly Landrigan et al., *The Minderoo-Monaco Commission on Plastics and Human Health*, *Annals of Global Health*, 2023. It cites Yang et al., *Scientific Reports* (2025), which **resolves to nothing on four wordings**. And it cites Shoaito et al., *Environment International* (2023), which is **Shoaito et al. 2019 in *Environmental Health Perspectives*, and concerns a phthalate metabolite** — placing it on B.2's side of the boundary that defines this hypothesis.

**Studies that do not exist and should.** The contaminated-community design in §5.2.

---

## 12. References

Bach, C.C., et al. (2016). Perfluoroalkyl and polyfluoroalkyl substances and measures of human fertility: a systematic review. *Critical Reviews in Toxicology*.
Botelho, J.C., et al. (2025). Per- and polyfluoroalkyl substances exposure in the U.S. population: NHANES 1999–March 2020. *Environmental Research*.
Brantsæter, A.L., et al. (2013). Determinants of plasma concentrations of perfluoroalkyl substances in pregnant Norwegian women. *Environment International*.
Cohen, N.J., et al. (2023). Exposure to perfluoroalkyl substances and women's fertility outcomes in a Singaporean population-based preconception cohort. *Science of the Total Environment*.
Ding, N., et al. (2020). Perfluoroalkyl and polyfluoroalkyl substances (PFAS) and their effects on the ovary. *Human Reproduction Update*.
Fei, C., et al. (2009). Maternal levels of perfluorinated chemicals and subfecundity. *Human Reproduction*.
Joensen, U.N., et al. (2009). Do perfluoroalkyl compounds impair human semen quality? *Environmental Health Perspectives*.
Jørgensen, K.T., et al. (2014). Perfluoroalkyl substances and time to pregnancy in couples from Greenland, Poland and Ukraine. *Environmental Health*.
Landrigan, P.J., et al. (2023). The Minderoo-Monaco Commission on Plastics and Human Health. *Annals of Global Health*.
Lum, K.J., et al. (2016). Perfluoroalkyl chemicals, menstrual cycle length, and fecundity. *Epidemiology*.
Olsen, G.W., et al. (2007). Half-life of serum elimination of perfluorooctanesulfonate, perfluorohexanesulfonate, and perfluorooctanoate in retired fluorochemical production workers. *Environmental Health Perspectives*.
Rickard, B.P., Rizvi, I., Fenton, S.E. (2021). Per- and poly-fluoroalkyl substances (PFAS) and female reproductive outcomes. *Toxicology*.
Waterfield, G., et al. (2020). Reducing exposure to high levels of perfluorinated compounds in drinking water improves reproductive outcomes: evidence from an intervention in Minnesota. *Environmental Health*.
Whitworth, K.W., et al. (2016). Brief report: perfluorooctane sulfonamide and fecundability. *Epidemiology*.
World Bank. Total fertility rate, United States. World Development Indicators, SP.DYN.TFRT.IN.

---

## Provenance and standing caveats

This chapter is written on 119 of 239 wanted full texts (50%), with PFAS papers reached less often than microplastics papers (51% against 59%).

**The findings that would survive full retrieval are the two that do not depend on the effect estimates at all**: the within-cohort disagreement between restricted and unrestricted tracks, which both teams reported themselves; and the exposure trend, which is national biomonitoring rather than a study result. **The finding that might not is the magnitude of any surviving association**, which rests on four studies of which two are in the restricted track and one of those reports no number.

**Objection over which this chapter was written.** None recorded from the PI, but five calls are open on the shared scope, the three-rater GRADE has not run, and the wrong-signed-verdict question is unresolved across two chapters.

**Numbers sourced from abstracts rather than full text.** None in §6; all four contributing studies were retrieved. The 120 unretrieved records are characterised by abstract or not at all.

**Figures not derived from project data.** The SDT decline magnitude in §8 is conventional. The US TFR series is World Bank data cached in `data/raw/`; the serum trends are Botelho et al. (2025) as published.

**Citation integrity.** Three of four works listed as seminal for this hypothesis in `HYPOTHESES-v5.md` did not resolve as written, and one belongs to a different chapter. Corrections in §11, owed to TICK-001.

**Generated inputs.** Shared search with the microplastics chapter; records split at extraction on the compound measured. Screen, retrieval logs, RA gate, effects and risk of bias in `extraction/microplastics-pfas-reproductive-*`; scope, walls and screen rubric in `literature/search-logs/microplastics-pfas-reproductive-search-scope.md`; GRADE reasoning in `-grade.md`. Every script runs from raw input to output without manual steps.
