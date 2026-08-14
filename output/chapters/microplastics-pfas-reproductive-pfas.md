# Chapter: PFAS and Fecundity

**Category:** Biological
**Primary mechanism:** Persistent fluorinated compounds accumulate in blood and follicular fluid, disrupt hormone signalling, and lower the chance of conceiving in each menstrual cycle.
**Cross-references:** Companion chapter on microplastics and nanoplastics, which shares this hypothesis entry (HYPOTHESES-v5.md §B.6) and must be read with it; B.2 (legacy endocrine disruptors); B.5 (fetal loss); A.17 (assisted reproduction); A.16 (paternal age and sperm quality).

## 1. The claim

Per- and polyfluoroalkyl substances, known as PFAS, reduce the per-cycle probability of conception in exposed women and impair semen quality in exposed men. Almost everyone in industrialised countries carries these compounds in their blood. If the effect is real and the exposure is general, PFAS lower realised fertility without changing what anyone wants, and the fertility decline after 1965 has a biological component that no account of preferences can capture.

## 2. Theoretical mechanism

PFAS resist metabolic breakdown and persist in the body for years. Olsen and colleagues (2007) measured serum half-lives of several years in retired fluorochemical workers, which means a single exposure keeps acting long after it ends. The compounds bind to albumin and to hormone transport proteins, and Ding and colleagues (2020) review evidence that they alter ovarian steroid production and follicle development. Two studies in this review exposed human cells directly: one found altered steroid synthesis in primary granulosa cells, another found impaired spermatogenesis in a stem-cell-derived model. The mechanism is the strongest part of the case, and it is not what the rating below turns on.

The mechanism also creates the problem that decides this chapter. The body clears PFAS through three routes that are all reproductive: transfer across the placenta, lactation, and menstrual blood loss. Brantsæter and colleagues (2013) measured this directly, showing that a woman's parity predicts her serum concentration. Having children therefore lowers PFAS levels, so any comparison of high-PFAS and low-PFAS women partly compares women who have already given birth against women who have not. Rickard and colleagues (2021) put elimination in the title of their review of PFAS and female reproductive outcomes, so the field recognises the difficulty.

This makes parity handling the field that decides whether a study speaks to the hypothesis at all. A study that restricts to women who have never given birth removes the backwards pathway. A study that adjusts for parity as a control variable does not, because parity lies on the path from earlier childbearing to current exposure, and controlling for it can introduce a second bias rather than remove the first. We committed to this distinction before reading any study, and we report the restricted and unrestricted analyses as separate tracks.

## 3. Search strategy

We built the search from 32 anchor papers, each verified against a live record so that no citation rests on memory. Three of the four works that HYPOTHESES-v5.md lists as seminal for this hypothesis did not resolve as written, and one of them is a paper about a phthalate, which belongs to B.2 rather than here. Section 10 records the corrections.

From those anchors we pulled everything they cite and everything that cites them, using OpenAlex, which produced 14,561 records with no failed requests. We then scored every record on two axes, the chemical named and the fertility outcome named, and screened the top 700 plus every record carrying terms from both axes at any rank. Nine boundary rules kept the search separate from neighbouring hypotheses. The two that removed most records were species, because studies of fish and rodents dominate this vocabulary, and pregnancy safety, because a study of PFAS and birth weight measures a property of a birth that happened rather than a count of births.

Full search terms, boundary rules and screening decisions are in `literature/search-logs/microplastics-pfas-reproductive-search-scope.md` and the accompanying screen rubric. Every script runs from raw input to output without manual steps.

## 4. PRISMA flow

| Stage | Records |
|---|---|
| Anchor papers, verified | 32 |
| Citation frame, one hop forward and backward | 14,561 |
| After collapsing duplicate versions | 14,296 |
| Screened on title and abstract | 920 |
| Excluded at screen | 462 |
| Held as unclear, retained for audit | 25 |
| Passed the screen | 433 |
| Full text sought | 239 |
| Full text obtained | 119 |
| PFAS studies contributing an effect estimate | 4 |

The gap between 239 and 119 matters for how you read what follows. Two automated passes reached half the records we wanted. Publishers blocked 38 downloads of papers that are free to read, and a further 40 sat in PubMed Central as author manuscripts that one route could not fetch and another could. Retrieval reached PFAS papers less often than microplastics papers, 51 percent against 59 percent, so the comparison between the two halves of this hypothesis rests on slightly thinner coverage of the PFAS side.

## 5. Included studies

| Study | Country | Design | Sample | Outcome | Estimate | Parity handling | Risk of bias |
|---|---|---|---|---|---|---|---|
| Jørgensen 2014 | Greenland, Poland, Ukraine | Pregnancy cohort | 938 | Time to pregnancy, PFNA | FR 0.80 (0.69, 0.94) | None | Serious |
| Jørgensen 2014 | Greenland | Pregnancy cohort | subset | Infertility over 13 months | OR 1.53 (1.08, 2.15) | None | Serious |
| Jørgensen 2014 | Same cohort, restricted | Pregnancy cohort | first-birth women | Both outcomes | Not replicated | Restricted to first births | Low for this bias |
| Whitworth 2016 | Norway | Birth cohort | 226 | Time to pregnancy, PFOSA | FOR 0.91 (0.71, 1.17) | Restricted to first births | Low for this bias, imprecise |
| Cohen 2023 | Singapore | Preconception cohort | 382 | Fecundability, PFDA | FR 0.90 (0.82, 0.98) | Adjusted only | Moderate |
| Cohen 2023 | Singapore | Preconception cohort | 382 | Fecundability, PFOS | FR 0.88 (0.79, 0.99) | Adjusted only | Moderate |
| Cohen 2023 | Singapore | Preconception cohort | 382 | Clinical pregnancy, PFDA | OR 0.74 (0.56, 0.98) | Adjusted only | Moderate |
| Lum 2016 | United States | Preconception cohort | 501 | Menstrual cycle length | AF 1.03 (1.00, 1.05) | Adjusted only | Serious, wrong outcome |

The full table with every compound, all 12 rows, sits in `extraction/microplastics-pfas-reproductive-effects.csv`. Sample sizes come from the published reports.

## 6. Quantitative synthesis

We did not pool these estimates. PROTOCOL §5.9 requires at least three estimates that share a chemical family, an outcome type, a sex, and a parity-handling status before pooling. The restricted track holds two studies, and one of them reports no number at all. A forest plot built across the restricted and unrestricted tracks would average a result against its own correction.

The finding is the disagreement between the tracks, and both cohorts that tested it reported it themselves.

| Cohort | Unrestricted | Restricted to first births |
|---|---|---|
| Jørgensen 2014, PFNA, fecundability | FR 0.80 (0.69, 0.94) | Not replicated |
| Jørgensen 2014, PFNA, infertility | OR 1.53 (1.08, 2.15) | Not replicated |
| Whitworth 2016, PFOSA, fecundability | FOR 0.85 (0.83, 1.09) | FOR 0.91 (0.71, 1.17) |

Jørgensen and colleagues state that among women having their first birth, the associations they found in the whole sample could not be replicated. Whitworth and colleagues restricted their analysis to 226 women having a first birth and found nothing, for PFOSA or for any other compound they measured. Two teams, working in different countries on different cohorts, each found that removing women who had already given birth removed the association. That is the pattern the elimination mechanism predicts, and it is the reason this chapter rates the causal claim as it does.

Cohen and colleagues (2023) provide the strongest counterweight and the clearest illustration of why the distinction matters. They measured exposure before conception, which fixes the timing problem that troubles the two pregnancy cohorts, and they found reduced fecundability for several compounds. They adjusted for parity rather than restricting on it. Their result belongs in the unrestricted track, and it stands as the best available argument that the association survives better designs.

Publication bias could not be assessed. Four studies do not support a funnel plot, and the Egger test needs ten.

## 7. Demographic significance

### 7.1 Pre-modern
No cell. Industrial production of these compounds began in the late 1940s.

### 7.2 First Demographic Transition
No cell. Production volumes before 1965 were negligible against the reproductive-age population.

### 7.3 Second Demographic Transition

The verdict turns on the direction of the exposure trend, and no effect size is needed to reach it.

Botelho and colleagues (2025) report two decades of United States national biomonitoring data. Between 1999 and March 2020, serum PFOS fell by 87 percent, PFOA by 74 percent, and PFHxS by 52 percent, following the industrial phase-out that began in 2002. Over the same years the United States total fertility rate fell from 2.007 to 1.641, a drop of 18.2 percent (World Bank, cached in `data/raw/`).

Exposure and fertility fell together. The hypothesis requires them to move apart. If PFAS suppress fertility, then removing most of the exposure should have raised fertility across exactly the window in which fertility dropped. Taking the largest unrestricted estimate in this review at face value, Cohen's fecundability ratio of 0.88 per quartile, and reading an 87 percent fall in concentration as roughly three quartile steps downward, the implied change is a fecundability gain near 47 percent. The hypothesis, granted its own contested number, predicts that the post-2000 American fertility decline should not have happened.

Three considerations make that calculation generous, and we state them rather than adjust for them. The estimate does not survive parity restriction. A fecundability ratio moves the time a couple waits, and converts into a birth forgone only where a woman runs out of reproductive years, which most exposed women do not. Mapping a percentage change in concentration onto quartile steps is rough, and we use it to show that the sign problem is large rather than to calibrate anything.

**Slope sufficiency: insufficient, and wrong-signed.** We computed no decomposition share. Building one on an estimate this chapter's own evidence identifies as partly reverse-causal would dress arithmetic as a finding.

One route to a different answer remains open. The falling series covers the legacy compounds. Manufacturers replaced them with short-chain substitutes as they withdrew, and national biomonitoring did not track most substitutes across this window. The replacement exposure series is unknown rather than flat, and no study estimates a fertility outcome for any replacement compound. A PFAS contribution to recent fertility decline survives only there.

## 8. GRADE rating

**Very low.** PROTOCOL §4.1 assigns this level where the evidence pattern is inconsistent. The inconsistency here appears within cohorts rather than between them, between the unrestricted and restricted analyses of the same data, which is the sharpest form the problem can take. On design alone the evidence would sit at Low, since it consists of cohorts with covariate control and no identifying variation. It does not reach Low because the disagreement is not noise across settings but the signature of the confounding the mechanism predicts.

The full domain-by-domain reasoning is in `literature/search-logs/microplastics-pfas-reproductive-grade.md`. PROTOCOL §5.11 requires three independent raters, and that panel has not run. One analyst writing three opinions in one sitting is one rater, and recording it otherwise would misstate how the rating was produced.

## 9. Verdict

| Phenomenon | Causal credibility | Demographic significance |
|---|---|---|
| Pre-modern | No cell | Insufficient data |
| First Demographic Transition | No cell | Insufficient data |
| Second Demographic Transition | **Very low** | **Not significant** |

## 10. Open questions and recommended studies

**The contaminated communities have never been studied for fertility.** Ronneby in Sweden, the Veneto region in Italy, the Mid-Ohio Valley in the United States, and several firefighter cohorts carry serum concentrations one to two orders of magnitude above background, from causes unrelated to the residents' own reproductive histories. Across 920 screened records, not one estimated a fertility outcome in these populations. Researchers have studied them for cancer, thyroid disease, cholesterol, ulcerative colitis, immune response, and birth weight. A time-to-pregnancy or completed-parity analysis in any of them would produce the first estimate in this literature with exposure variation that parity cannot explain.

**A first-birth cohort with exposure measured before conception would settle the central question.** Cohen and colleagues have the timing right and the parity handling wrong; Whitworth has the parity handling right and 226 women. One study with both would move this rating.

**The replacement compounds need an exposure series before they need an effect estimate.** Nobody can compute a demographic contribution for GenX or the short-chain substitutes without knowing how population exposure has moved.

**Three citation corrections for TICK-001.** HYPOTHESES-v5.md cites a Lancet Commission on Reproductive Health (2025) that does not exist; the intended work is almost certainly Landrigan and colleagues, *The Minderoo-Monaco Commission on Plastics and Human Health*, Annals of Global Health, 2023. It cites Yang et al., Scientific Reports (2025), which resolves to nothing on four wordings. It cites Shoaito et al., Environment International (2023), which is Shoaito and colleagues 2019 in Environmental Health Perspectives, and concerns a phthalate metabolite, placing it on B.2's side of the boundary that defines this hypothesis.

## 11. References

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
Rickard, B.P., Rizvi, I., Fenton, S.E. (2021). Per- and poly-fluoroalkyl substances (PFAS) and female reproductive outcomes: PFAS elimination, endocrine-mediated effects, and disease. *Toxicology*.
Waterfield, G., et al. (2020). Reducing exposure to high levels of perfluorinated compounds in drinking water improves reproductive outcomes: evidence from an intervention in Minnesota. *Environmental Health*.
Whitworth, K.W., et al. (2016). Brief report: perfluorooctane sulfonamide and fecundability. *Epidemiology*.
World Bank. Total fertility rate, United States. World Development Indicators, SP.DYN.TFRT.IN.
