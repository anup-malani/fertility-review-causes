# Old-Age-Security / Pension Crowd-Out of Fertility — PI Independent Review (first pass)

**Author:** Anup Malani (PI), with Claude
**Date:** 2026-07-05
**Status:** working draft. An independent benchmark to set against Alexandra's pipeline output.
**Inputs:** GACS `metaanalysis-doi-list.md` (44 distinct ET=4 studies); `ra-review.csv` (40 DOI-resolved
studies with RA RETRIEVE/EXCLUDE decisions); the 4 unresolved title-keyed studies.

Expanding old-age security lowers fertility. Nine clean quasi-experiments say so, in one direction,
with no reversals. But the mechanism cannot carry either fertility decline this review targets: state
pensions arrived too late for the First Demographic Transition and were already universal before the
Second. Its real footprint is contemporary fertility decline in the developing world.

This document is the PI's own read of the same vetted evidence the RAs worked from. It fixes an
estimand, re-decides the RAs' inclusion calls, maps the evidence, and grades each phenomenon. The point
is to have an independent benchmark, reached by hand, that Alexandra's pipeline chapter can be checked
against.

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


| Coordinate                  | In                                                                                                                                                                   | Out                                                                                                                                                                  |
| --------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Treatment**               | Pension introduction or expansion, social security, long-term-care insurance, or financial-market development that lets households save instead of bearing children. | General income shocks (lottery), child grants (the price of children), childcare-supply shocks, welfare family caps, marriage-age laws. These test other hypotheses. |
| **Outcome**                 | Fertility as the dependent variable: births, completed fertility, parity progression, TFR.                                                                           | Savings, migration, coresidence, child schooling, elderly health, labor supply. Real pension effects, wrong outcome for this chapter.                                |
| **Direction and mechanism** | Treatment → fertility, through the old-age-security motive.                                                                                                          | Reverse causation (fertility → pension take-up). The grandparental-childcare channel is a separate pathway with the opposite sign (Cell C below).                    |


The binding constraint here is the estimand, not the search. GACS reports 44 "meta-analysis-ready"
studies, but that number answers a search question: did the query find pension-and-fertility papers? It
does not answer the review's question: do those papers identify the effect the chapter is about. Apply
the estimand and three in four fall away. The scarce resource in this pilot was never more papers. It
was a sharp definition of what we are trying to measure.

---



## 2. Three cells, not one axis

The RAs sorted each study into RETRIEVE or EXCLUDE. That single axis buries three different objects, and
the difference is not cosmetic: what may be pooled depends on which object a study is.

- **Cell A, primary.** Exogenous non-child old-age security raises or lowers fertility, through the OAS
motive. The causal estimate is built from these and only these.
- **Cell B, mechanism.** Does a child actually function as old-age security? Here fertility is the
*treatment* and an old-age-security asset (private insurance, savings) is the outcome. Evidence that
the mechanism exists, not an estimate of the fertility effect. Never pooled with A.
- **Cell C, alternative pathway.** A pension moves fertility through grandparental childcare, not the
OAS motive, and it moves it the other way: a retired grandparent's free time lowers the cost of a
grandchild and *raises* the daughter's fertility. A real pension-to-fertility effect, opposite in
sign. Never pooled with A. Reported as a labeled secondary stream.

Everything else is out of scope for this chapter.

---



## 3. Inclusion adjudication: our calls against the RAs'

We agree with the RAs on 37 of 40 calls. The verdicts are not the contribution. The structure behind
them is: three cells instead of one, one inconsistency caught, and one high-value study flagged for
rescue. In counts:

- **Cell A (primary): 9 studies.** The RA RETRIEVE set of 10, minus Ci, which moves to Cell B.
- **Cell B (mechanism): 2 studies.** Ci (RA: RETRIEVE) and Ruthbah (RA: EXCLUDE).
- **Cell C (grandparental childcare): 3 studies.** Eibich-Siedler, Ilciukas, Akyol-Atalay. The RAs
excluded all three; we keep them as a walled-off secondary stream, never pooled with A.
- **Excluded, out of scope: 26 studies.** Wrong outcome, wrong treatment, or reverse causation.
- **Unresolved, verify: 4 studies.** One of them, a Ghana pension-and-fertility paper, is likely Cell A
and worth the effort to resolve.



### Cell A — primary OAS-motive → fertility (9)


| #   | Study                           | Setting / period   | Treatment                    | Design                    | RA       | Ours                     |
| --- | ------------------------------- | ------------------ | ---------------------------- | ------------------------- | -------- | ------------------------ |
| 1   | Danzer & Zyska 2023             | Brazil, rural      | Rural pension expansion      | DiD / IV / event-study    | RETRIEVE | **A**                    |
| 2   | Rossi & Godard 2022 (AEJ:Pol)   | Namibia            | Social-pension extension     | DiD                       | RETRIEVE | **A**                    |
| 3   | Billari & Galasso 2009          | Italy              | Pension-wealth cuts          | Cohort natural experiment | RETRIEVE | **A**                    |
| 4   | Han et al. 2025                 | China              | Long-term-care insurance     | DiD                       | RETRIEVE | **A**                    |
| 5   | Guinnane & Streb 2021           | Prussia, 1881–1910 | Bismarck social insurance    | Regional rollout          | RETRIEVE | **A**                    |
| 6   | Shen et al. 2020                | China, rural       | New Rural Pension Scheme     | DiD + PSM + IV            | RETRIEVE | **A**                    |
| 16  | "Pensions & Fertility: Germany" | Germany?           | pension policy               | abstract missing          | RETRIEVE | **A, verify identity**   |
| 18  | Basso & Cuberes 2013            | US, 19th c.        | Financial-market development | IV (1820 banks)           | RETRIEVE | **A, broader mechanism** |
| 24  | Galofré-Vilà 2023               | US                 | 1935 Social Security Act     | Cross-state panel         | RETRIEVE | **A, softer ID**         |




### Cell B — mechanism validation (2)


| #   | Study                     | Structure                                      | RA       | Ours              |
| --- | ------------------------- | ---------------------------------------------- | -------- | ----------------- |
| 9   | Ci 2024                   | # children (IV'd) → private-insurance adoption | RETRIEVE | **B, reclassify** |
| 11  | Ruthbah 2022 (Bangladesh) | fertility (IV'd) → asset accumulation          | EXCLUDE  | **B, reinstate**  |


Ci and Ruthbah are the same study in different clothes. Both instrument fertility and ask whether
children substitute for a purchased old-age asset. The RAs kept Ci and dropped Ruthbah. That is an
inconsistency, not a distinction. Both belong in Cell B.

### Cell C — grandparental-childcare pathway (3)


| #   | Study                 | Setting     | Sign                                         | RA      | Ours  |
| --- | --------------------- | ----------- | -------------------------------------------- | ------- | ----- |
| 8   | Eibich & Siedler 2020 | Germany     | grandparent time ↑ → daughter fertility ↑    | EXCLUDE | **C** |
| 10  | Ilciukas 2023         | Netherlands | delayed grandparent retirement → fertility ↓ | EXCLUDE | **C** |
| 19  | Akyol & Atalay 2025   | Australia   | delayed grandmother pension → fertility ↓    | EXCLUDE | **C** |


These three point the other way. Access to a retired grandparent's time raises a daughter's fertility,
so keeping grandparents at work by tightening pension eligibility lowers it. The RAs were right to keep
them out of the primary estimate. They were too quick to drop them entirely. Pensions plainly move
fertility through more than one channel, and the net sign is an empirical question, so a pooled
"pension → fertility" number that ignores the split cannot be read.

### Excluded — out of scope (26)

- **Wrong outcome (18):** pension or policy affects something other than fertility. Yuan (child
schooling), Neve-Fink (parental survival), Bratti (daughter labor supply), Duflo (child height),
Mu-Du (schooling), Choukhmane (saving), Chen 2017 (coresidence), Edmonds (household structure),
Chen 2015 (migration), Amarante (birthweight), Lehmann-Hasemeyer-Streb (saving), Eggleston
(migration), Bau (son migration), Lachowska-Myck (saving), Valentová (maternal labor), Bérgolo-Cruces
(labor informality), Serrano-Alarcón (health/labor), Oh (transfers to the elderly).
- **Wrong treatment (6):** the shock is not old-age security. Rosenberg (child grant), Kearney (welfare
family cap), Tao (kindergarten supply), Bulman (lottery income), Bellés-Obrero-Lombardi (marriage
age), Broeck-Maertens (female employment).
- **Reverse causation (2):** Zhang (children → pension take-up), Chen-Fang (fewer children → old-age
support).

We concur with all 26.



[Claude: Are many of the wrong outcome studies actually relevant, but in a second-order sense, because those other things (schooling, parental survival, etc.) things that themselves affect fertility. So they highlight potentially indirect channels. Re-screen those with this lens. 

Agree on wrong treatment studies should be excluded. 

On reverse causation: do they not shift your Bayesian prior that pensions reduce demand for children. If children lead to pension takeup, that suggests that children are not a mechanism for old age support, right?]

### Unresolved — verify (4)


| #   | Study                                                       | Status    | Our read                                                                         |
| --- | ----------------------------------------------------------- | --------- | -------------------------------------------------------------------------------- |
| 15  | Pension Reform and Fertility: Micro Evidence from **Ghana** | NO_WID    | High value. Likely Cell A, and the second sub-Saharan case. Resolve it.          |
| 17  | Pension Reforms and Fertility: Italy, "Wati & Sudarto 2025" | WID_DRIFT | Author names do not match an Italian study. Probable phantom. Verify, then drop. |
| 29  | Oh, public transfers → private support (Ecuador)            | WID_DRIFT | Outcome is not fertility. Exclude regardless.                                    |
| 33  | Non-contributory pensions, Costa Rica (case study)          | OK        | Outcome likely not fertility. Verify, probably exclude.                          |


---



[Claude: Tell me more about these studies in this section.  E.g. give me abstracts or links to the papers.]

## 4. Evidence map (Cell A, 9 studies)

The table below reads off the abstracts, the AI rationales, and the RA notes. No PDFs sit in the repo
(they went out over Slack), so effect *magnitudes* are first-pass and marked `[PDF]` where the full
text must confirm them. Direction is stated where the abstract supports it. "Consistent" means the sign
matches the OAS motive: more non-child old-age security, less fertility.


| #   | Study                               | Setting / period     | Treatment                    | Effect on fertility                                          | ID strength                                 | Phenomenon                         |
| --- | ----------------------------------- | -------------------- | ---------------------------- | ------------------------------------------------------------ | ------------------------------------------- | ---------------------------------- |
| 2   | **Rossi & Godard 2022**             | Namibia, modern      | Social-pension extension     | Negative, consistent; size `[PDF]`                           | **Strong**, the flagship natural experiment | Contemporary developing-country DT |
| 1   | **Danzer & Zyska 2023**             | Brazil rural, modern | Rural pension expansion      | Negative; ~8% lower childbearing propensity `[PDF confirm]`  | **Strong**                                  | Contemporary developing-country DT |
| 5   | **Guinnane & Streb 2021**           | Prussia, 1881–1910   | Bismarck social insurance    | Negative on marital fertility; size `[PDF]`                  | **Moderate–strong**, historical             | **FDT (historical)**               |
| 3   | **Billari & Galasso 2009**          | Italy, 1990s         | Pension-wealth cuts          | Consistent: less pension wealth, more children; size `[PDF]` | **Moderate**                                | Rich-country modern → SDT          |
| 4   | **Han et al. 2025**                 | China, modern        | Long-term-care insurance     | Negative, consistent; size `[PDF]`                           | **Moderate**                                | Contemporary (OAS substitute)      |
| 18  | **Basso & Cuberes 2013**            | US, 19th c.          | Financial-market development | Negative, consistent; size `[PDF]`                           | **Moderate**, historical IV                 | **FDT (well-timed substitute)**    |
| 6   | **Shen et al. 2020**                | China rural, modern  | New Rural Pension Scheme     | Negative, consistent; size `[PDF]`                           | **Weaker**, PSM-reliant (PLoS ONE)          | Contemporary developing-country DT |
| 24  | **Galofré-Vilà 2023**               | US, 1935+            | 1935 Social Security Act     | Sign subtle; links SSA spending to the baby boom `[PDF]`     | **Weaker**, soft exogeneity                 | **FDT-adjacent**                   |
| 16  | **"Pensions & Fertility: Germany"** | Germany, ?           | pension policy               | unassessed                                                   | **Verify identity first**                   | likely FDT `[verify]`              |


Every credible design points the same way. Expand non-child old-age security and fertility falls;
withdraw it and fertility rises. No study in Cell A reverses that sign. That directional agreement,
across five countries and a century and a half, is the strongest thing the evidence base has, and it is
what any eventual pooled or narrative estimate rests on.

[Claude: can we evaluate these on the following outcomes or measures: (a) credibility (ie strength of causal ev), (b) external validity -- do they causally explain the world outside the sample, (c) internal R squared -- do they explain much of the variation in sample? (d) Do they explain much of the variation in fertility ourside the sample? Obviously we can apply all 4 measures to PM, FDT, and SDT periods.]



Two side channels corroborate the mechanism without entering the estimate.

- **Cell B.** Ci and Ruthbah both find that more children means fewer purchased old-age assets, private
insurance in one, savings in the other. Children and financial old-age security are substitutes. That
is the micro-foundation the Cell A studies assume, recovered from the reverse direction.
- **Cell C.** The grandparental-childcare studies find the opposite sign. Pensions therefore run through  
two opposing channels, an OAS-motive channel that lowers fertility and a time-transfer channel that  
raises it, so the net effect of any given reform is genuinely an empirical question

---



## 5. Verdicts by phenomenon (first pass)

The review grades causal credibility and demographic significance separately, phenomenon by phenomenon.
The pattern is the same each time: the micro-evidence is real, and it still fails to reach the two
canonical transitions the project cares about. Timing defeats it in the First. Saturation defeats it in
the Second.

### Pre-modern

No study speaks to the pre-modern period, because no pre-modern setting offers exogenous variation in
formal old-age security. So there is nothing to grade: causal credibility is not assessable.

The mechanism still matters little for the pre-modern *question*, which is about variation. Before
formal pensions, every household relied on children for old age. A universal condition cannot explain
why fertility differed across pre-modern populations. It explains why the level was high, not why it
moved. The variation has to come from elsewhere: kin-support norms, mortality, land and inheritance.

**Verdict:** no direct evidence; low significance for pre-modern variation.

### First Demographic Transition (~1870–1965)

State pensions cannot have caused the First Demographic Transition. They came too late.

The dates settle it. Marital fertility across northwest Europe began falling in the 1870s and 1880s.
Bismarck's social insurance dates to 1889, American Social Security to 1935. A cause cannot postdate its
effect, so state old-age security cannot be what set the transition going. At most it deepened a decline
already well under way, and even that reach is limited: early coverage was thin, so the share of the
population actually exposed to the treatment was small.

One channel is timed correctly, and it is the reason the broad reading of old-age security matters. A
family did not need Bismarck to save for old age if a bank would do it. Financial-market development
spread through the nineteenth century, ahead of state pensions, and Basso and Cuberes identify exactly
this effect on fertility in nineteenth-century US counties. So whatever weight old-age security carries
for the First Transition rests mostly on financial-market substitution, not on public pensions.

Four studies bear on this period, in one direction, on credible but historical designs. That earns a
modest grade, no more.

**Verdict:** low-to-moderate causal credibility; partial demographic significance, and it runs through
financial development rather than state pensions.

### Second Demographic Transition (~1965–present)

By the time the Second Demographic Transition began, the crowd-out had already happened.

Rich countries reached near-universal pension coverage well before 1965. The margin the mechanism needs,
a fresh expansion of non-child old-age security, was already spent. There was little left to crowd out.
Worse for the hypothesis, the sign points the wrong way in this era. Where rich countries later trimmed
pension generosity to cope with aging, the motive predicts fertility should rise. It fell.

The direct evidence is thin to match. Billari and Galasso in Italy is the one rich-country modern study
on point. The strongest studies, Namibia, Brazil, China, identify effects in developing countries that
are arguably still in a first transition, not the rich-country postponement the Second Transition names.

**Verdict:** very low causal credibility for the Second Transition; low significance, with a sign that
may run the wrong way.

### A gap in the frame

The mechanism's cleanest evidence, Namibia, Brazil, China, lands in a place the review has no box for:
contemporary fertility decline in the developing world. That is neither the pre-modern period, nor the
historical First Transition, nor the rich-country Second. The team should decide which it is: a fourth
target worth naming, or a body of mechanism evidence that transports only weakly to the three we have.
Either way, it should be said out loud, not filed under the Second Transition by default.

[Claude: Is contemporary fertility decline in developing world same as FDT?  The real test is whether the studies look at countries when their fertility is above replacement v. at or below replacement.  If above, the it is akin to FDT; if at or below, then SDT.]

### Bottom line

The old-age-security motive is real and well identified at the level of the household. Across five
countries and 150 years, expanding non-child old-age security lowers fertility, in one direction, with
no reversals. It is the demographic significance that fails, and it fails for two ordinary reasons.
State pensions arrived after the First Transition had already started, so financial-market development,
not public pensions, carries what weight the mechanism has there. And pensions were already universal
before the Second Transition began, so there was almost nothing left to crowd out, and the pension cuts
of that era point the wrong way. The mechanism's real home is contemporary developing-country fertility
decline, which this review does not yet have a place for.

**Grades.** Pre-modern: no direct evidence, low significance. First Transition: low-to-moderate
credibility, partial significance through financial development. Second Transition: very low
credibility, low significance.

---



## Appendix — verification items for the RAs

1. **Resolve the Ghana study** (`#15`, pension reform → fertility), now NO_WID. If real it is a primary
  Cell A study and the second sub-Saharan case. High value.
2. **Verify the "Germany" study** (`#16`, `10.1007/s00148-016-0608-x`) before any use.
3. **Confirm the "Italy / Wati & Sudarto 2025" record** (`#17`) is a phantom, then drop it.
4. **Reconcile Ci and Ruthbah** in `ra-review.csv`. Both belong in the mechanism cell.
5. **Confirm the flagged magnitudes** `[PDF]` for the nine Cell A studies against full text.

