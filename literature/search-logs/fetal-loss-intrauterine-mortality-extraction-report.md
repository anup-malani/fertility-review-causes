# Extraction report — fetal-loss-intrauterine-mortality (B.5)

**2 PDFs on disk, 2 studies extracted.** Both identities were verified against page 1 of the file rather than against the filename.

## The two findings that matter more than the numbers

### 1. The one published estimate of this chapter's headline quantity is an accounting share

Mourchid and Bakass estimate that intrauterine mortality reduces Moroccan potential fertility by **9.4%**, or 0.23 children per woman. That is the chapter's primary estimand, estimated directly, and it is the only study located that does so. But their potential-fertility measure is built by **adding fetal deaths to live births**: a lost conception is counted as a forgone birth, with no time cost and no replacement. It is an `ACCOUNTING_SHARE` by construction.

This corroborates the chapter's argument rather than contradicting it. The model's accounting arm gives about 11% for removing a 10% loss rate outright, against their 9.4% — close enough to confirm the two are computing the same thing. What the chapter adds is that this number is an upper bound, and that the behavioural quantity is roughly two and a half times smaller.

### 2. Wall 4 fires, and the authors supply the evidence themselves

The 9.4% decomposes into 6.0 points from early fetal mortality and 3.8 from stillbirth. The authors define early fetal mortality as *abortions plus miscarriages*, and their own Bongaarts residual index attributes **0.12 births per woman to induced abortion against 0.14 for all early fetal mortality**. On their own numbers, then, most of the larger component is induced termination — A.4's estimand, not B.5's. **B.5's clean share of the Moroccan estimate is the stillbirth component, 3.8%.** This is exactly the contamination the scope document predicted for settings where abortion is legally restricted, and it means the headline 9.4% must not be quoted as a B.5 effect.

A second internal tension is worth recording: the paper's life-table IUM quotient is 272 per 1000 pregnancies, while its reported fetal-death rates imply roughly 100 per 1000. That gap is the Casterline and Leridon under-reporting problem appearing inside a single study.

## Valente reroutes on retrieval

Screened as `PRIMARY_SHOCK_TO_BIRTHS`, it becomes `PARAMETER_DETERMINANT_TO_LOSS` at full text: the outcomes are miscarriage, stillbirth and sex at birth, not births per woman. The screen could not have known — the abstract does not say — and this is the routing gate working as designed rather than a screening error.

It is nonetheless the **best-identified loss-margin estimate in the corpus**: maternal fixed effects over 11,887 pregnancies, with district-by-month conflict casualties as the shock, and the effect concentrated in gestational months one to five as the mechanism predicts. Moving from low- to high-intensity conflict exposure raises the probability of miscarriage by 0.77 percentage points, 11.6% of the mean.

Three details bear directly on the chapter's identification section:

- **Stillbirth moves the other way** (−0.22 ppt). The author reads this as conflict-exposed fetuses being lost earlier rather than surviving to stillbirth. That is compositional movement across the live-birth boundary, and it is Wall 1 mattering empirically rather than definitionally.
- **The replacement and reporting threats appear together in the author's own words**: women who lose a pregnancy may both try again sooner and under-report a further loss. The chapter flagged both a priori; here they are documented in the setting.
- **The result rests on the maternal-FE specification.** Within-district estimates are positive but insignificant, and the author's explanation for the gap is differential fertility timing by conflict intensity — a selection process, not noise. Recorded as a fragility.

## Risk of bias

| study | overall | the binding domain |
|---|---|---|
| Mourchid & Bakass 2022 | **Critical** | Exposure measurement: contaminated by induced abortion, and the paper's own two loss measures disagree by a factor of nearly three. Usable as an accounting benchmark, not as causal evidence. |
| Valente 2015 | **Moderate** | Outcome measurement: self-reported miscarriage with documented differential under-reporting, biasing toward zero. |

## Still open

2 of 51 wantlist items retrieved. The extraction table has 2 rows and no pooling is possible or attempted: one estimate is an accounting share and the other is a determinant-to-loss effect, so they share neither an estimand nor an outcome.

## A duplicate class the pipeline cannot currently catch

W1977150354 ('Children of the Revolution: Fetal and Child Health amidst Violent Civil Conflict', RePEc 2011) is **confirmed** to be Valente's working paper on the same Nepal insurgency data — same author, same shock, same survey rounds. It collapses into W2009105027, and the primary-cell count falls from 18 to 17.

**The general point is worth carrying to every chapter.** This duplicate is invisible to both dedup rules in use. DOI dedup misses it because the two records have different DOIs. Title dedup misses it because the working paper was RETITLED before publication: 'Children of the Revolution' and 'Civil conflict, gender-specific fetal loss, and selection' share almost no tokens. The version-of-record gate handles same-title-different-version; this is the mirror case, different-title-same-work, and only author-plus-data inspection catches it. A cheap partial guard: flag same-first-author records whose abstracts name the same country and shock for human review.
