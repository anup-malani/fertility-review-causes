# Old-Age-Security / Pension Crowd-Out of Fertility — PI Independent Review (first pass)

**Author:** Anup Malani (PI), with Claude
**Date:** 2026-07-05
**Status:** working draft, v3. Incorporates PI margin comments on v2.
**Inputs:** GACS `metaanalysis-doi-list.md` (44 distinct ET=4 studies); `ra-review.csv` (40 DOI-resolved
studies with RA RETRIEVE/EXCLUDE decisions); the 4 unresolved title-keyed studies, now resolved (§3.5).

Expanding old-age security lowers fertility. Nine clean quasi-experiments say so, in one direction,
with no reversals. The mechanism is real at the household level. What it cannot yet do is explain much
of the fertility decline this review targets: state pensions arrived too late for the First Demographic
Transition, and rich-country pensions were already universal before the Second. The one modern setting
where a fresh pension expansion meets below-replacement fertility is China, and even there the effect is
a small slice of a decline driven mostly by other forces.

This document is the PI's own read of the same vetted evidence the RAs worked from. It fixes an
estimand, re-decides the RAs' inclusion calls, maps the evidence, grades it on four measures, and
applies those measures across the three phenomena. The point is an independent benchmark, reached by
hand, that Alexandra's pipeline chapter can be checked against.

**What changed from v2 (PI comments).** Four moves. First, the "wrong outcome" exclusions were
re-screened: many trace the causal chain (pension → saving; pension → children's schooling; children →
old-age support), so they now sit in a new Cell D rather than the trash. Second, the reverse-causation
studies are read as prior-updating mechanism evidence, not noise. Third, the evaluation is rebuilt
around the PI's four measures. Fourth, studies are sorted into FDT and SDT by whether the country sat
above or below replacement fertility at the time of treatment, which is what makes a setting FDT-like or
SDT-like. That last move reclassifies China and Italy into the SDT and changes the SDT verdict.

---

## 1. What counts as evidence (the estimand)

One question decides which studies belong in this chapter: does the study estimate the effect of
*non-child old-age security* on *fertility*, through the *old-age-security motive*? Most papers that
mention pensions and fertility do not.

The hypothesis is old and specific. Children were once a household's retirement plan, its insurance and
its investment for old age (Neher 1971; Caldwell 1976; Cigno 1993). Give parents another way to secure
old age, whether a state pension, social insurance, long-term-care insurance, or a bank that lets them
save, and the retirement demand for children falls. Fertility follows.

The estimand is therefore the causal effect of an exogenous rise in non-child old-age security on
completed fertility, working through that motive. Three coordinates pin it down, and the whole
adjudication turns on getting them right.

| Coordinate | In | Out |
|---|---|---|
| **Treatment** | Pension introduction or expansion, social security, long-term-care insurance, or financial-market development that lets households save instead of bearing children. | General income shocks (lottery), child grants (the price of children), childcare-supply shocks, welfare family caps, marriage-age laws. These test other hypotheses. |
| **Outcome** | Fertility as the dependent variable: births, completed fertility, parity progression, TFR. | Savings, migration, coresidence, child schooling, elderly health, labor supply. Real pension effects, but a different outcome. See Cell D: some of these trace the causal chain even though fertility is not the outcome. |
| **Direction and mechanism** | Treatment → fertility, through the old-age-security motive. | Reverse causation (fertility → pension take-up) is not the estimand, but it updates the prior on whether children are old-age security. The grandparental-childcare channel is a separate pathway with the opposite sign (Cell C). |

The binding constraint here is the estimand, not the search. GACS reports 44 "meta-analysis-ready"
studies, but that number answers a search question: did the query find pension-and-fertility papers? It
does not answer the review's question: do those papers identify the effect the chapter is about. Apply
the estimand and three in four fall away from the primary cell. The scarce resource in this pilot was
never more papers. It was a sharp definition of what we are trying to measure.

---

## 2. Four cells, not one axis

The RAs sorted each study into RETRIEVE or EXCLUDE. That single axis buries four different objects, and
the difference is not cosmetic: what may be pooled, and what merely informs the prior, depends on which
object a study is.

- **Cell A, primary.** Exogenous non-child old-age security moves fertility, through the OAS motive. The
  causal estimate is built from these and only these.
- **Cell B, mechanism.** Does a child actually function as old-age security? Fertility is the *treatment*
  and an old-age-security asset (private insurance, savings) is the outcome. Evidence that the mechanism
  exists, not an estimate of the fertility effect. Never pooled with A.
- **Cell C, alternative pathway.** A pension moves fertility through grandparental childcare, not the OAS
  motive, and it moves it the other way: a retired grandparent's free time lowers the cost of a
  grandchild and *raises* the daughter's fertility. A real pension-to-fertility effect, opposite in sign.
  Never pooled with A. Reported as a labeled secondary stream.
- **Cell D, indirect channels and chain links.** The treatment is old-age security and the outcome is one
  step short of fertility: private saving, children's schooling or health, coresidence, or old-age
  support itself. These do not estimate the fertility effect, but they light up the links in the causal
  chain the OAS story runs through, and several update the prior on whether the mechanism operates at
  all. This cell answers the PI's point that "wrong outcome" is not the same as "no information."

Everything outside these four cells is out of scope.

---

## 3. Inclusion adjudication: our calls against the RAs'

We agree with the RAs on most binary calls, and the verdicts are not the contribution. The structure is:
four cells instead of one, one inconsistency caught, one high-value study rescued, and a re-reading of
the "wrong outcome" pile that recovers a dozen studies as chain evidence. In counts:

- **Cell A (primary): 9 studies.**
- **Cell B (mechanism): 2 studies** (Ci, Ruthbah).
- **Cell C (grandparental childcare): 3 studies** (Eibich-Siedler, Ilciukas, Akyol-Atalay).
- **Cell D (indirect / chain): ~12 studies** re-screened out of the old "wrong outcome" pile.
- **Excluded, genuinely out of scope: ~11 studies** (wrong treatment, or no fertility link even at one
  remove).

### Cell A — primary OAS-motive → fertility (9)

| # | Study | Setting / period | Treatment | Design | Replacement at treatment | Phenomenon |
|--:|---|---|---|---|---|---|
| 1 | Danzer & Zyska 2023 | Brazil, rural, ~1991 | Rural pension expansion | DiD / IV / event-study | above (~2.8) | FDT-like |
| 2 | Rossi & Godard 2022 (AEJ:Pol) | Namibia, ~1990s–2000s | Social-pension extension | DiD | above (~4.5) | FDT-like |
| 3 | Billari & Galasso 2009 | Italy, 1990s | Pension-wealth cuts | Cohort natural experiment | **below (~1.3)** | **SDT** |
| 4 | Han et al. 2025 | China, ~2016 | Long-term-care insurance | DiD | **below (~1.6)** | **SDT** |
| 5 | Guinnane & Streb 2021 | Prussia, 1881–1910 | Bismarck social insurance | Regional rollout | above | **FDT (historical)** |
| 6 | Shen et al. 2020 | China, rural, ~2009 | New Rural Pension Scheme | DiD + PSM + IV | **below (~1.5)** | **SDT** |
| 16 | **Fenge & Scheubel 2017** ("Germany") | Imperial Germany, 1895–1907 | Bismarck pension insurance | Regional variation, 23 provinces | above | **FDT (historical)** |
| 18 | Basso & Cuberes 2013 | US counties, 19th c. | Financial-market development | IV (1820 banks) | above | **FDT (well-timed substitute)** |
| 24 | Galofré-Vilà 2023 | US, 1935+ | 1935 Social Security Act | Cross-state panel | above | **FDT-adjacent** |

Study #16 is resolved (§3.5): it is Fenge and Scheubel (2017), a *historical* Bismarck-Germany study,
not a modern one. It joins the FDT-historical cluster and corroborates Guinnane-Streb on the same reform.

### Cell B — mechanism validation (2)

| # | Study | Structure | RA | Ours |
|--:|---|---|---|---|
| 9 | Ci 2024 | # children (IV'd) → private-insurance adoption | RETRIEVE | **B, reclassify** |
| 11 | Ruthbah 2022 (Bangladesh) | fertility (IV'd) → asset accumulation | EXCLUDE | **B, reinstate** |

Ci and Ruthbah are the same study in different clothes. Both instrument fertility and ask whether
children substitute for a purchased old-age asset. The RAs kept Ci and dropped Ruthbah. That is an
inconsistency, not a distinction. Both belong in Cell B.

### Cell C — grandparental-childcare pathway (3)

| # | Study | Setting | Sign | Ours |
|--:|---|---|---|---|
| 8 | Eibich & Siedler 2020 | Germany | grandparent time ↑ → daughter fertility ↑ | **C** |
| 10 | Ilciukas 2023 | Netherlands | delayed grandparent retirement → fertility ↓ | **C** |
| 19 | Akyol & Atalay 2025 | Australia | delayed grandmother pension → fertility ↓ | **C** |

These three point the other way. Access to a retired grandparent's time raises a daughter's fertility,
so keeping grandparents at work by tightening pension eligibility lowers it. The RAs were right to keep
them out of the primary estimate. They were too quick to drop them entirely. Pensions plainly move
fertility through more than one channel, and the net sign is an empirical question, so a pooled
"pension → fertility" number that ignores the split cannot be read.

### Cell D — indirect channels and chain links (~12, re-screened from "wrong outcome")

The PI's point is right: a pension study whose outcome is not fertility can still trace a link in the
OAS chain, and a link that itself bears on fertility. Three groups fall out.

**D1. Does the OAS substitute exist? Pension crowds out private saving.** Choukhmane et al. (one-child
policy → household saving), Lehmann-Hasemeyer & Streb (Bismarck insurance → private saving), Lachowska &
Myck (Polish reform → saving). If a pension crowds out the *saving* motive for children, it is crowding
out the same asset demand that the OAS story says it crowds out for *children*. This is the cleanest
indirect corroboration in the set, and the saving elasticity is a rough ceiling on what to expect for
the fertility elasticity.

**D2. Do children actually deliver old-age support? The return on the "investment."** Chen & Fang (fewer
children → less old-age support), Zhang (children → pension take-up), Neve & Fink (children's schooling →
parent's survival), and the coresidence and migration studies (Chen 2015, Eggleston et al., Edmonds et
al., Chen et al. 2017, Bau et al.). These test whether children pay the old-age dividend the motive
assumes. If they do, the prior on the mechanism rises; if pensions dissolve coresidence and transfers,
the substitution is visible on the support margin even when fertility is not measured.

**D3. Quantity-quality channel.** Yuan et al., Mu & Du (pension → children's schooling), Duflo (pension →
child health). If a pension reform raises investment *per* child, that is the quality margin, which
co-moves with lower quantity. An indirect channel, not proof, and it can cut either way.

Cell D never enters the fertility estimate. It sets priors, bounds magnitudes, and tells the reader which
links in the chain are independently supported.

### Reverse causation, reconsidered

The PI asked whether the reverse-causation studies shift the prior. They do. Chen & Fang (fewer children
→ less old-age support in old age) is direct evidence that children *are* old-age security, which is the
premise of the whole chapter; it raises the prior. Zhang (children → pension take-up) cuts the other way,
and its sign is the test: if more children *raise* pension take-up, children and pensions are complements,
not substitutes, and the OAS story weakens; if more children *lower* take-up, they are substitutes, and it
strengthens. So the reverse studies are not noise to discard. They are Bayesian updates whose direction we
should read off the sign, which means pulling the two estimates (flagged for retrieval). Both now sit in
Cell D.

### Excluded — genuinely out of scope (~11)

- **Wrong treatment (not old-age security):** Rosenberg (child grant), Kearney (welfare family cap), Tao
  (kindergarten supply), Bulman (lottery income), Bellés-Obrero-Lombardi (marriage age), Broeck-Maertens
  (female employment), Amarante (cash transfer to pregnant women), Valentová (parental leave).
- **No fertility link even at one remove:** Bérgolo-Cruces (labor informality), Serrano-Alarcón (retiree
  health and labor). Bratti sits at the border: pension → daughter's labor supply is a step toward the
  grandparental-childcare channel, so it is better read alongside Cell C than dropped.

### 3.5 The four unresolved studies, resolved

| # | Study | Verdict | Detail |
|--:|---|---|---|
| 15 | **Ghana** | **Real. Cell A candidate, FDT-like.** | Zelu, Iranzo & Pérez-Laborda (2023), "Pension Policy Reform and Fertility: Micro Evidence from Ghana," IZA/BREAD G²LM\|LIC conference. [Conference PDF](https://conference.iza.org/conference_files/GLMLIC_BREAD_Conference_2023/zelu_b34232.pdf) (host down 2026-07-05; abstract pending retrieval). Ghana TFR ~4 in the study window, above replacement, so FDT-like. The second sub-Saharan case after Namibia. Retrieve. |
| 16 | **Germany** | **Real. Now placed in Cell A, FDT (historical).** | Fenge & Scheubel (2017), "Pensions and fertility: back to the roots," *J. Population Economics* 30(1):93–139, [doi:10.1007/s00148-016-0608-x](https://link.springer.com/article/10.1007/s00148-016-0608-x). Regional variation across 23 provinces of Imperial Germany in Bismarck's pension system; finds a negative effect of pension-insurance introduction on fertility. Historical, not modern. |
| 17 | **Italy, "Wati & Sudarto 2025"** | **Phantom. Drop.** | No such paper exists. The real Italian pension-fertility work is Billari-Galasso (#3, already in the set) and the Battistin–De Nadai–Padula grandparental-childcare study. Author names do not match the topic; this is the ghost-citation signature Shravan's evaluation §5 describes. |
| 29 | **Ecuador, "Oh"** | **Exclude (off-outcome).** | Outcome is public-versus-private transfers to the elderly, not fertility. Belongs in Cell D at most; the closest real literature is Mexico (PROGRESA; Juárez), not an Ecuadorian RCT. |
| 33 | **Costa Rica** | **Exclude (off-outcome).** | Elizondo, Flores & Quinto (2018), "The Impact of Non-contributory Pensions. A Case Study for Costa Rica," [BSE WP](https://thevoice.bse.eu/wp-content/uploads/2018/11/Elizondo_Flores_Quinto_2018.pdf). Outcomes are employment, schooling, household composition, and well-being. Fertility is not among them. |

---

## 4. Evidence map (Cell A, 9 studies)

The table reads off the abstracts, the AI rationales, and the RA notes. No PDFs sit in the repo (they
went out over Slack), so effect *magnitudes* are first-pass and marked `[PDF]` where the full text must
confirm them. "Consistent" means the sign matches the OAS motive: more non-child old-age security, less
fertility. Replacement status at the time of treatment is what sorts each study into FDT or SDT (§5, §6).

| # | Study | Setting / period | Treatment | Effect on fertility | Credibility (a) | Phenomenon |
|--:|---|---|---|---|---|---|
| 2 | **Rossi & Godard 2022** | Namibia, modern | Social-pension extension | Negative, consistent; size `[PDF]` | **Strong**, flagship natural experiment | FDT-like (above repl.) |
| 1 | **Danzer & Zyska 2023** | Brazil rural, ~1991 | Rural pension expansion | Negative; ~10% lower short-run childbearing, ~1.3 fewer completed births over 20 yr `[PDF confirm]` | **Strong** | FDT-like (above repl.) |
| 5 | **Guinnane & Streb 2021** | Prussia, 1881–1910 | Bismarck social insurance | Negative on marital fertility; size `[PDF]` | **Moderate–strong**, historical | **FDT (historical)** |
| 16 | **Fenge & Scheubel 2017** | Imperial Germany, 1895–1907 | Bismarck pension insurance | Negative, consistent (23-province variation) | **Moderate**, historical | **FDT (historical)** |
| 18 | **Basso & Cuberes 2013** | US, 19th c. | Financial-market development | Negative, consistent; size `[PDF]` | **Moderate**, historical IV | **FDT (well-timed substitute)** |
| 24 | **Galofré-Vilà 2023** | US, 1935+ | 1935 Social Security Act | Sign subtle; links SSA spending to the baby boom `[PDF]` | **Weaker**, soft exogeneity | **FDT-adjacent** |
| 3 | **Billari & Galasso 2009** | Italy, 1990s | Pension-wealth cuts | Consistent: less pension wealth, more children; size `[PDF]` | **Moderate** | **SDT (below repl.)** |
| 6 | **Shen et al. 2020** | China rural, ~2009 | New Rural Pension Scheme | Negative, consistent; size `[PDF]` | **Weaker**, PSM-reliant (PLoS ONE) | **SDT (below repl.)** |
| 4 | **Han et al. 2025** | China, ~2016 | Long-term-care insurance | Negative, consistent; size `[PDF]` | **Moderate** | **SDT (below repl.)** |

Every credible design points the same way. Expand non-child old-age security and fertility falls;
withdraw it and fertility rises. No study in Cell A reverses that sign. That directional agreement,
across five countries and 150 years, is the strongest thing the evidence base has, and it is what any
eventual pooled or narrative estimate rests on.

Two side channels corroborate the mechanism without entering the estimate. Cell B: Ci and Ruthbah find
that more children means fewer purchased old-age assets, private insurance in one, savings in the other,
so children and financial old-age security are substitutes, the micro-foundation the Cell A studies
assume, recovered from the reverse direction. Cell C: the grandparental-childcare studies find the
opposite sign, so pensions run through two opposing channels and the net effect of any given reform is
an empirical question.

---

## 5. How to grade a study: four measures

The PI's frame separates two questions that a single "how good is this study" rating runs together. Does
the study *identify a causal effect*, and does that cause *explain much of the variation in fertility*?
Each question can be asked inside the study's own sample or outside it. That gives a two-by-two.

| | Does it identify a causal effect? | Does it explain much variation? |
|---|---|---|
| **In-sample** | **(a) Credibility.** Strength of the identification. | **(c) Internal R².** Share of in-sample fertility variation the cause moves. |
| **Out-of-sample** | **(b) External validity.** Does the causal estimate transport to other settings? | **(d) Demographic significance.** Does the cause explain the actual fertility decline in the target period? |

The distinction earns its keep because the four measures come apart. A pension natural experiment can
score high on (a) and low on (c): the effect is cleanly identified and still small next to everything
else moving fertility in that sample. And a study high on (a) and (c) can be low on (b) and (d): a real,
large effect in rural Namibia need not transport to Italy, and need not explain much of any historical
transition. The OAS literature lives in exactly that corner. Its best studies are credible (a). They are
modest on in-sample explanatory power (c), because a pension reform shifts births by a few percent or a
fraction of a child while income, education, and mortality move the rest. They are limited on transport
(b), because the settings are specific. And they are low on demographic significance (d), for the timing
and saturation reasons in §6. High credibility, low significance, is the whole finding in one line.

Measures (c) and (d) need numbers the abstracts do not carry: an in-sample R² or variance share, and a
decomposition of the target-period decline. Both are flagged for the full-text and macro-data pass. The
first pass fills (a) at the study level (§4) and (b) and (d) at the period level (§6).

---

## 6. Verdicts by phenomenon (first pass)

Studies are sorted by the demography, not the calendar or the income level. A country above replacement
fertility at the time of treatment is living an FDT-like decline; a country at or below replacement is
living an SDT-like one. That test, which the PI proposed, is what assigns each modern study, and it
moves China and Italy into the SDT.

### Pre-modern

No study speaks to the pre-modern period, because no pre-modern setting offers exogenous variation in
formal old-age security. Credibility (a) is not assessable, and (b), (c), (d) have nothing to sit on.

The mechanism still matters little for the pre-modern *question*, which is about variation. Before formal
pensions, every household relied on children for old age. A universal condition cannot explain why
fertility differed across pre-modern populations. It explains why the level was high, not why it moved.
The variation has to come from elsewhere: kin-support norms, mortality, land and inheritance.

**Verdict:** no direct evidence; demographic significance low for pre-modern variation.

### First Demographic Transition (~1870–1965)

State pensions cannot have caused the First Demographic Transition. They came too late.

The dates settle it. Marital fertility across northwest Europe began falling in the 1870s and 1880s.
Bismarck's pension insurance dates to 1889, American Social Security to 1935. A cause cannot postdate its
effect, so state old-age security cannot be what set the transition going. At most it deepened a decline
already under way, and even that reach is limited: early coverage was thin, so the population share
actually exposed was small. That is measure (d) coming up short even where (a) is respectable. Six studies
sit here now, counting Ghana and the two Bismarck papers, all pointing one way, on credible but historical
designs. That earns modest credibility (a) and modest transport within the historical West (b).

One channel is timed correctly, and it is the reason the broad reading of old-age security matters. A
family did not need Bismarck to save for old age if a bank would do it. Financial-market development
spread through the nineteenth century, ahead of state pensions, and Basso and Cuberes identify exactly
this effect on fertility in nineteenth-century US counties. So whatever demographic weight (d) the
mechanism carries for the First Transition rests mostly on financial-market substitution, not on public
pensions.

**Verdict:** (a) low-to-moderate; (b) moderate within the historical West; (c) small; (d) partial, and it
runs through financial development rather than state pensions.

### Second Demographic Transition (~1965–present)

The SDT verdict changes once the replacement test does the sorting. Three studies now sit here, not one:
Billari-Galasso in Italy, and Shen and Han in China, all below replacement at treatment. So the evidence
is no longer a single Italian study. That raises SDT credibility (a) from very low to low-moderate.

Demographic significance (d) still splits, and the split is the interesting part. In *rich* countries the
saturation argument holds. By the time the SDT began, near-universal pension coverage was already in
place, so the fresh expansion the mechanism needs had already happened, and there was little left to crowd
out. Worse, where rich countries later trimmed pensions to cope with aging, the motive predicts fertility
should rise. It fell. Italy is the rich-country case, and its demographic significance is low for exactly
this reason.

China is the exception that sharpens the rule. China is below replacement, so it is SDT-like on the
demography, but its pension systems were *new and expanding* in the 2000s and 2010s, so it escapes the
saturation that mutes the mechanism in the rich-country SDT. Shen and Han are therefore the most
informative SDT-context evidence we have: they show OAS crowd-out can still bite below replacement, when
the pension margin is live. But their demographic significance (d) is bounded from above by everything
else driving Chinese fertility, above all the one-child policy and rapid development, next to which a
rural-pension or long-term-care rollout is a small slice. And their external validity (b) to the rich
low-fertility world is weak, because the rich world's pensions are not expanding.

**Verdict:** (a) low-to-moderate; (b) low, China does not transport to the saturated rich world; (c)
small; (d) low, saturation and wrong sign in rich countries, a minor share in China.

### The frame holds, if we sort by replacement

v2 worried that "contemporary developing-country" fertility decline had no box in the PM/FDT/SDT frame.
The PI's replacement test dissolves the worry. There is no orphan category. A study belongs to the FDT or
the SDT by whether its country sat above or below replacement at treatment, which is the demographic
content of the two transitions in the first place. Namibia, Brazil, and Ghana are above replacement and
FDT-like. China and Italy are below and SDT. What looked like a gap was just a mislabeling by calendar and
income; sort by demography and every study lands.

### Bottom line

The old-age-security motive is real and well identified at the level of the household. Across five
countries and 150 years, expanding non-child old-age security lowers fertility, in one direction, with no
reversals. High marks on credibility (a). The trouble is that credibility is not significance. On the
measures that ask how much fertility the mechanism actually explains, in-sample (c) and out (d), it is
modest to low everywhere. State pensions arrived after the First Transition had started, so
financial-market development, not public pensions, carries what weight the mechanism has there. Rich
countries were already saturated before the Second Transition began, and their later pension cuts point
the wrong way. The one live modern test, China below replacement with expanding pensions, confirms the
effect and bounds it small against everything else moving Chinese fertility. A credible mechanism that
explains little of the variation is the honest summary.

**Grades.** Pre-modern: no direct evidence, low significance. First Transition: low-to-moderate
credibility, partial significance through financial development. Second Transition: low-to-moderate
credibility, low significance, with the rich-country sign running the wrong way and China a small share.

---

## Appendix — verification items for the RAs

1. **Retrieve the Ghana paper** (Zelu, Iranzo & Pérez-Laborda 2023). Confirmed real; abstract still
   needed (IZA host was down 2026-07-05). Likely a primary Cell A study and the second sub-Saharan case.
2. **Study #16 is Fenge & Scheubel 2017**, a historical Bismarck-Germany study. Update the record and
   place it in the FDT-historical cluster.
3. **Drop the "Italy / Wati & Sudarto 2025" record** (#17). Confirmed phantom.
4. **Reconcile Ci and Ruthbah** in `ra-review.csv`. Both belong in Cell B.
5. **Pull the two reverse-causation estimates** (Chen-Fang; Zhang) and read their signs; they update the
   mechanism prior (§3, "Reverse causation, reconsidered").
6. **Confirm the flagged magnitudes** `[PDF]` for the nine Cell A studies, and extract an in-sample R² or
   variance share (measure c) where the paper reports one.
7. **Get replacement-level TFR at treatment** for each modern study to confirm the FDT/SDT sort in §6
   (first-pass values are approximate).
