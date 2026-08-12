# Search scope — fetal loss and intrauterine mortality

**Hypothesis:** B.5 (HYPOTHESES-v5.md)
**Hypothesis slug:** `fetal-loss-intrauterine-mortality`
**Target phenomena:** PM and FDT. The FDT cell carries an inverted sign and is scored on magnitude
rather than on explanatory contribution — see "Phenomenon scope" and Call 1. No SDT cell (Call 2).
**Ticket:** TICK-065
**Status:** **DRAFT** (Shravan, 2026-08-11). Seven boundary walls specified, four scope calls raised
with recommendations. Walls freeze after the PI answers Call 1 and Call 3, or after a decision to
proceed on the recommendations. Anchor sourcing (A3) is **not** blocked by the freeze.

Built on the D.2.d (`child-centeredness-intensive-parenting`) template, which inherits D.3.b's. Three
constraints carry forward as design decisions rather than being rediscovered: the taxonomy carries
`INSUFFICIENT_INFO` and a catch-all `OFF_OTHER` from v1; a wall whose discriminator is invisible in a
title or abstract is declared unenforceable up front instead of being trusted and audited later; and
the forward-citation seed rule is uniform across seed types, with no special case for routing decoys.

The scope below is written against a live reconnaissance pass over OpenAlex (2026-08-11, 35 probes,
zero failed requests, so the reported zero-hit counts are genuine absences rather than refusals). The
counts quoted in "Expected shape of the evidence" come from that pass, which is regenerable via
`source/build/goldset/115_b5_recon_probe.py` and reported in
`fetal-loss-intrauterine-mortality-recon-probe.md`.

## Causal claim

Not every conception becomes a live birth, and the share that does varies across populations and over
time with maternal health, infection, and nutrition. Where a larger share of conceptions is lost
before delivery, a population records fewer live births per woman even when conception rates, marriage
patterns, and contraceptive behavior are identical. Improvement in maternal health therefore raises
live-birth fertility through a channel that requires no change in anyone's intentions.

The claim's position in the causal chain is what makes this chapter difficult, and the difficulty runs
opposite to the one D.2.d faced. B.5 is defined by a **channel**, not by a treatment. Its named
drivers — maternal health, infection, nutrition — are each owned or bordered by another chapter, and
its outcome, the count of live births, is the review's common outcome. What B.5 owns is the segment of
the reproductive process between conception and delivery. A study belongs to B.5 when the quantity
doing the causal work is **survival of an established pregnancy**, whatever moves it.

## The accounting identity is not the effect

The central analytical problem of this chapter is that B.5's mechanism has an arithmetic form that
overstates it, and the overstatement is large enough to reverse the chapter's conclusion if left
unexamined.

Write $B$ for live births, $C$ for conceptions, and $L$ for the probability that a conception is lost.
For a single conception, $B = C(1-L)$, and a fall in $L$ from 0.30 to 0.15 raises live births by 21%.
That calculation is the version of B.5 that appears in informal statements of the hypothesis, and it
is an upper bound that no population attains, because a woman does not get one conception. Over a
reproductive career, a fetal loss consumes **time**, not a birth: the gestation elapsed before the
loss, plus the recovery and waiting time to the next conception. In the Bongaarts–Potter accounting
this enters the mean birth interval as an additive component, roughly two to four months for an early
loss and up to ten for a late one. Whether that lost time costs a birth depends on which constraint
binds.

- **Where the reproductive span binds** — uncontrolled fertility, early and near-continuous exposure,
  childbearing continuing until fecundity ends — time lost to fetal loss is time that cannot be
  recovered, and the effect on completed fertility is real though far smaller than $(1-L)$ implies.
- **Where a parity target binds** — controlled fertility, stopping behavior, a desired family size
  reached well before the span runs out — a couple replaces the loss, and the effect on completed
  fertility approaches zero. The loss changes the timing of births and not their number.

Two consequences follow, and both are load-bearing. First, the hypothesis predicts its own effect to
be **largest in pre-modern and early-transition populations and to vanish as fertility comes under
control**, which is an independent theoretical justification for v5's PM/FDT assignment and a
prediction the chapter can test rather than assume. Second, an estimate of B.5's magnitude is
uninterpretable unless it states which quantity it computed. Every included estimate is therefore
tagged with an **estimand level**:

| Level | What it measures |
|---|---|
| `ACCOUNTING_SHARE` | The mechanical share, $(1-L)$-type arithmetic or a proximate-determinants decomposition holding conception behavior fixed. An **upper bound**, and reported only as one. |
| `BEHAVIORAL_NET` | The effect on completed fertility or TFR after whatever replacement the population actually does. This is the quantity the review's demographic-significance verdict requires. |

The two levels are **never combined into one pooled estimate**, and any figure built on
`ACCOUNTING_SHARE` carries the standing caveat that it assumes away replacement. This is the same
discipline D.3.b and D.2.d apply to stated intentions versus realized fertility, applied to a
different axis.

## Phenomenon scope

**PM: the primary cell.** Pre-modern populations had high and variable intrauterine mortality, little
or no parity-targeted stopping, and reproductive spans that plausibly bound. Both conditions for a
non-trivial B.5 effect hold. The evidence base is historical demography, parish and genealogical
reconstitution, and the biometric-demography tradition running from Sheps and Menken through Leridon
and Wood.

**FDT: a primary cell with an inverted sign.** Between roughly 1870 and 1965, intrauterine mortality
fell in the transitioning West alongside maternal nutrition, syphilis control, and obstetric care.
B.5 therefore predicts that live-birth fertility was pushed **upward** across precisely the period in
which TFR fell by half. The hypothesis does not explain the First Demographic Transition; if it is
demographically significant for the FDT, it **deepens the puzzle** by implying the behavioral decline
was larger than the observed TFR series shows. This is a real finding rather than a scoping
inconvenience, and the chapter reports it as one. See Call 1 for how the verdict is scored.

**SDT: no pooled cell.** Loss rates rose in the SDT era through the maternal-age composition shift,
but that shift is A.11's (tempo and postponement) and its fecundity consequence is A.15's, whose claim
text already names rising miscarriage risk. A B.5 SDT cell would restate A.15. SDT-era estimates are
retained under `SDT_AGE_COMPOSITION_CONTEXT` and are discussed where they inform the parameter
values; they are excluded from the recall denominator and from every pool. See Call 2.

## The seven boundary walls

Six of the seven walls separate B.5 from a chapter that shares either its drivers or its outcome. All
six reduce to one question: **at which reproductive margin does the estimate bite?** B.5 owns
survival conditional on conception. A paper routes on the margin its estimate identifies, not on the
disease, exposure, or population it studies.

**Wall 1 — B.5 vs A.1 (Child Mortality Decline, `child-mortality-decline-replacement`).** The two
hypotheses are adjacent mortality channels separated by the live-birth boundary, and the distinction
is mechanical-versus-behavioral as much as pre-versus-post-natal.
- **A.1 asks:** does the death of a *born* child raise subsequent fertility through replacement and
  insurance motives? The mechanism is a parental decision.
- **B.5 asks:** does the death of a *conceptus* lower the count of live births? The mechanism is
  arithmetic in the first instance, attenuated by replacement in the second.
- **Discriminator:** an estimate keyed on infant, neonatal, or child mortality routes to
  `OFF_CHILD_MORTALITY_A1`. An estimate keyed on stillbirth or spontaneous abortion is B.5.
  **Perinatal mortality straddles the boundary by construction**, since standard perinatal definitions
  pool late stillbirths with early neonatal deaths; a perinatal estimate whose components cannot be
  separated takes `MIXED_PERINATAL_UNRESOLVED` and is adjudicated at full text.
- **The replacement asymmetry, stated to prevent double-counting.** Replacement *after a fetal loss*
  is internal to B.5 — it is the attenuation described above, and B.5 cannot compute its own net
  effect without it. Replacement *after a child's death* is A.1's mechanism and its estimand. A study
  of both without separation is `MIXED_PERINATAL_UNRESOLVED`.

**Wall 2 — B.5 vs B.3 (Infectious Disease and Sterility, `infectious-disease-sterility`).** The
sharpest wall, because the two hypotheses share their causes, their populations, and their historical
literature, and because **v5's B.3 entry claims B.5's channel in its own claim text** ("reduce
fecundity through tubal damage, fetal loss, and amenorrhea"). See Call 3.
- **B.3 asks:** does infection prevent conception — through tubal occlusion, sterility, or amenorrhea?
- **B.5 asks:** does infection kill established pregnancies?
- **Discriminator:** an estimate whose outcome is failure to conceive, sterility, infertility
  prevalence, or time-to-pregnancy routes to `OFF_STERILITY_B3`. An estimate whose outcome is
  stillbirth, spontaneous abortion, or pregnancy survival is B.5. Syphilis is the paradigm B.5
  organism and gonorrhoea and chlamydia the paradigm B.3 organisms, but **the organism does not route
  the paper — the measured outcome does.** Where an infection's fertility effect is estimated without
  decomposing the conception and survival margins, the paper takes `MIXED_FECUNDITY_UNRESOLVED`.

**Wall 3 — B.5 vs the determinant chapters B.2, B.4, B.6, B.7.** Endocrine disruptors, obesity,
microplastics and PFAS, and antidepressants are all upstream causes that can operate through
intrauterine survival, and B.4's and B.6's claim texts each name pregnancy outcomes.
- **Rule:** the determinant chapters own **variation in the determinant**; B.5 owns **the survival
  channel and its fertility consequence**. A study estimating obesity → miscarriage risk is a study of
  B.5's channel driven by B.4's treatment, and it routes on whether a fertility outcome is estimated.
  With a fertility outcome, B.5 claims it and cross-references the determinant chapter. Without one,
  it is a **parameter** paper (`PARAMETER_DETERMINANT_TO_LOSS`), useful to B.5's decomposition and to
  the determinant chapter's mechanism section, and counted toward neither chapter's causal recall.
- This rule is deliberately different from D.2.d's source-of-variation rule. D.2.d is defined by a
  treatment and routes on what moves; B.5 is defined by a channel and routes on what is measured.
  Applying D.2.d's rule here would empty this chapter, because every one of B.5's drivers is another
  chapter's treatment.

**Wall 4 — B.5 vs A.4 (Induced Abortion Access, `induced-abortion-access`).** Induced and spontaneous
abortion share an outcome category, a data source, and in many settings a reporting code. The wall is
conceptually trivial and empirically the most dangerous in the chapter.
- **Discriminator:** deliberate termination is A.4 and routes to `OFF_INDUCED_ABORTION_A4`; involuntary
  loss is B.5.
- **The measurement problem is not a routing problem and cannot be fixed by a wall.** Where induced
  abortion is illegal or stigmatized, women report it as spontaneous, so a measured "fetal loss" rate
  is contaminated by exactly the variable A.4 studies — and the contamination is largest in the
  pre-modern and transitional settings that carry B.5's primary cells. Every included estimate records
  `INDUCED_SEPARATION`: how, if at all, the study distinguishes involuntary loss from induced
  termination. Studies that cannot are not excluded, because excluding them would empty the historical
  record; they are marked and their risk-of-bias rating reflects it.

**Wall 5 — B.5 vs A.15 (Maternal Age and Fecundity Decline, `maternal-age-fecundity-decline`).** The
loss rate rises steeply with maternal age, so any cross-sectional association between loss and low
fertility is confounded by the age composition of the exposed population, and A.15's claim text
already owns rising miscarriage risk as an SDT mechanism.
- **Discriminator:** an estimate whose identifying variation is maternal age or the timing of
  childbearing routes to `OFF_MATERNAL_AGE_A15`. An estimate of loss variation **within** age strata,
  or one that adjusts for maternal age and parity, is B.5. Maternal age and parity are recorded as
  mandatory candidate confounders on every included empirical paper.

**Wall 6 — B.5 vs A.17 (ART Access, `art-access-fertility-recovery`).** Clinical ART populations
supply most modern high-quality data on pregnancy loss, and they are selected on subfecundity, treated
with interventions that alter loss rates, and observed from a gestational point ordinary populations
are not.
- **Discriminator:** loss rates measured within ART or IVF cycles route to `OFF_ART_A17` when the
  estimand concerns treatment success, and are admissible to B.5 only as `PARAMETER_LOSS_LEVEL` with
  the selection flagged. No ART-derived loss rate is transported to a general population without an
  explicit adjustment argument recorded at extraction.

**Wall 7 — human versus non-human.** The reconnaissance pass surfaced a substantial veterinary and
animal-science literature on embryonic mortality and reproductive wastage in cattle, pigs, camelids,
and laboratory mammals, sharing B.5's vocabulary almost exactly. Non-human studies route to
`OFF_ANIMAL` and are excluded. The wall is stated because it is cheap to enforce and expensive to
discover late.

## What the title/abstract screen can and cannot enforce

Every wall above discriminates on the estimate's measured margin, which — unlike D.2.d's
source-of-identifying-variation — is usually named in an abstract. This chapter's screen is therefore
in a better position than D.2.d's, and the exceptions are specific and known in advance.

| Wall | Enforceable at title/abstract? | Why |
|---|---|---|
| 1 (A.1, pre- vs post-natal) | **Yes** | The outcome is named. Perinatal composites are also named, and route to the MIXED cell on sight. |
| 2 (B.3, conception vs survival) | Partly | Outcome usually named; studies reporting a compound "fecundity" effect are not separable from an abstract. |
| 3 (B.2/B.4/B.6/B.7 determinants) | **Yes** | Whether a fertility outcome is estimated is visible; that is the whole test. |
| 4 (A.4, induced vs spontaneous) | Partly for routing, **No** for measurement | Deliberate termination is named; whether the data separate the two is a data-quality fact from the methods section. |
| 5 (A.15, maternal age) | Partly | "Maternal age" is named when it is the treatment; within-stratum variation and confounder adjustment are not. |
| 6 (A.17, ART) | **Yes** | The clinical setting is named. |
| 7 (species) | **Yes** | Named, though the vocabulary overlap is total, so the screen must be told to check. |
| Estimand level (accounting vs behavioral) | **No** | Whether an estimate is a mechanical share or a post-replacement effect is a modeling fact, and abstracts of decomposition papers rarely state it. |

**Consequence, pre-committed rather than discovered:** the screen assigns a routing cell with
reasonable confidence, and it does **not** assign the estimand level. Every included empirical paper
enters full text with `ACCOUNTING_SHARE` / `BEHAVIORAL_NET` unset, and a record whose routing turns on
Wall 2 or Wall 5 and whose abstract does not name the margin takes `ROUTING_DEFERRED_TO_FULLTEXT`
rather than a substantive `OFF_*` cell.

## Estimand cells

| Cell | Treatment / variation | Outcome | Routing |
|---|---|---|---|
| `PRIMARY_LOSS_TO_FERTILITY` | Variation in the fetal-loss or stillbirth rate | Live-birth fertility: completed parity, TFR, births per woman | Primary synthesis |
| `PRIMARY_SHOCK_TO_BIRTHS` | An exogenous shock (famine, epidemic, disease-control campaign) whose estimated effect on births runs through intrauterine survival | Live births | Primary synthesis — **the identification-bearing cell** |
| `REPLACEMENT_COMPENSATION` | A fetal loss | Interval to next conception, subsequent parity, reproductive compensation | Primary support; supplies the attenuation parameter without which no `BEHAVIORAL_NET` figure can be computed |
| `MECHANICAL_ACCOUNTING` | A loss rate entered into a proximate-determinants or microsimulation model | Implied births | Primary synthesis, `ACCOUNTING_SHARE` level only; never pooled with identified estimates |
| `PARAMETER_LOSS_LEVEL` | — | The level, trend, age gradient, or gestational-age distribution of intrauterine mortality | Parameter stream; feeds demographic significance; **not** in the causal recall denominator |
| `PARAMETER_DETERMINANT_TO_LOSS` | Nutrition, infection, maternal health, exposure | Fetal loss, no fertility outcome | Parameter stream; cross-filed to the determinant chapter |
| `MEASUREMENT_METHOD` | — | Reporting quality, recall bias, definitional comparability of loss and stillbirth data | Methods stream; load-bearing for risk of bias |
| `THEORY_PROXIMATE_DETERMINANTS` | Formal treatment of intrauterine mortality within a fertility model | — | Theory stream; no empirical recall credit |
| `SDT_AGE_COMPOSITION_CONTEXT` | Postponement-driven loss variation, SDT era | Any | Context; never pooled — see Call 2 |
| `OFF_CHILD_MORTALITY_A1` | Infant, neonatal, or child mortality | Fertility | Route to A.1 |
| `OFF_STERILITY_B3` | Infection acting on conception, sterility, or infertility prevalence | Fertility | Route to B.3 |
| `OFF_INDUCED_ABORTION_A4` | Deliberate termination, abortion access or law | Fertility | Route to A.4 |
| `OFF_MATERNAL_AGE_A15` | Maternal age or childbearing timing as the identifying variation | Fertility | Route to A.15 |
| `OFF_ART_A17` | ART or IVF treatment success | Fertility | Route to A.17 |
| `OFF_DETERMINANT_CHAPTER` | Determinant → some reproductive margin other than intrauterine survival | Fertility | Route to B.2 / B.4 / B.6 / B.7 as tagged |
| `OFF_OUTCOME` | Fetal loss as a determinant of a **non-fertility** outcome — maternal mental health, later child health, obstetric risk | No fertility outcome | Context only |
| `OFF_CLINICAL_MANAGEMENT` | Diagnosis, prevention, or treatment of recurrent pregnancy loss or stillbirth | Clinical | Excluded; expected to be the largest cell |
| `OFF_ANIMAL` | Non-human embryonic or fetal mortality | Any | Excluded — Wall 7 |
| `MIXED_PERINATAL_UNRESOLVED` | Perinatal composite spanning the live-birth boundary | Fertility | Held; adjudicated at full text |
| `MIXED_FECUNDITY_UNRESOLVED` | Conception and survival margins not decomposed | Fertility | Held; adjudicated at full text |
| `ROUTING_DEFERRED_TO_FULLTEXT` | Routing turns on Wall 2 or 5, abstract silent on the margin | Fertility | Held; adjudicated at full text |
| `REVERSE` | Fertility, parity, or birth spacing affecting loss risk | Loss outcome | Context — and see the identification caution |
| `OFF_OTHER` | Non-B.5 fertility determinant with no sibling-hypothesis home | Fertility | Route out; no sibling queue |
| `INSUFFICIENT_INFO` | Cannot be routed on the visible record | Unknown | Pairs only with `UNCERTAIN` |

`THEORY_PROXIMATE_DETERMINANTS`, `MEASUREMENT_METHOD`, both `PARAMETER_*` cells, and
`SDT_AGE_COMPOSITION_CONTEXT` carry verdict `RELEVANT` and are separated downstream. None counts
toward empirical recall.

## The identification cautions

**Reverse causation runs through parity and spacing.** Higher parity and shorter birth intervals raise
loss risk, and a woman who has had many pregnancies has had more opportunities to record a loss.
Cross-sectional associations between measured loss and completed fertility are therefore contaminated
in the direction *opposite* to the hypothesis: more births produce more recorded losses. Any positive
raw association between loss and fertility is a warning sign about the design rather than evidence
against B.5.

**Selection through the loss itself.** A large share of early loss removes chromosomally abnormal
conceptions. Reducing loss does not convert one-for-one into surviving births, because part of the
averted loss would have failed later or produced a non-viable outcome. A study that treats averted
loss as equivalent to a gained birth overstates the effect, and extraction records whether the
viability of the counterfactual birth is addressed at all.

**The exposure is measured with error correlated with the outcome.** Under-reporting of pregnancy loss
in survey pregnancy histories is severe, non-random, and worse for early losses, for losses further in
the past, and for less-educated respondents — the finding of Casterline's World Fertility Survey
review, which is the chapter's methodological anchor. Because women with more births have more recent
and more salient reproductive histories, reporting quality correlates with the outcome. This is a
first-order threat and not a footnote.

**The observation window defines the quantity.** A "loss rate" means nothing without the gestational
window it is measured over: clinically recognized loss from six weeks is a different quantity from
total post-implantation loss measured by hCG assay, which is different again from stillbirth defined
at 20, 22, 24, or 28 weeks, and national stillbirth definitions differ on exactly those thresholds.
Every extracted loss quantity carries `LOSS_WINDOW_WEEKS` and the definition used, and no two
estimates are pooled across incompatible windows.

**Designs that can survive all of this** are the ones with variation in intrauterine survival external
to the woman's own reproductive behavior: famine and nutritional shocks, epidemic exposure, disease-
control and treatment campaigns, and altitude or environmental discontinuities. Those are the primary
targets of the search, and `PRIMARY_SHOCK_TO_BIRTHS` exists to hold them.

## When to adjudicate mechanisms

The title/abstract screen assigns the routing cell only. For every included empirical paper, full-text
extraction records:

- `LOSS_DEFINITION` and `LOSS_WINDOW_WEEKS` — what counts as a loss, over which gestational range;
- `ESTIMAND_LEVEL` — `ACCOUNTING_SHARE` or `BEHAVIORAL_NET`, the field that decides poolability;
- `INDUCED_SEPARATION` — how involuntary loss is distinguished from induced termination, or that it
  is not (Wall 4);
- `REPLACEMENT_TREATMENT` — whether the design allows, models, or ignores replacement after a loss;
- `FERTILITY_REGIME` — whether the study population practices parity-targeted stopping, since the
  hypothesis predicts the effect only where it does not;
- `VARIATION_SOURCE` — what generates the identifying variation, in the authors' terms;
- `CONFOUNDERS_ADJUSTED` — maternal age and parity are mandatory; nutrition, infection load, and
  socioeconomic position are recorded when present;
- `SELECTION_VIABILITY` — whether the counterfactual viability of the averted loss is addressed.

Drafting may report only what these fields support. A historical series showing stillbirth rates
falling while birth rates fell may document the covariation; it must not be described as evidence that
falling loss raised live-birth fertility, absent a design that identifies it.

## Eligibility rules

- Include empirical studies where the estimate bears on **intrauterine survival → live-birth
  fertility**, or on an upstream determinant → intrauterine survival **where a fertility consequence is
  estimated**.
- Determinant → loss studies with no fertility outcome are `PARAMETER_DETERMINANT_TO_LOSS`: retained,
  indexed, used for demographic significance, and excluded from the causal recall denominator.
- Loss → non-fertility outcome studies are `OFF_OUTCOME`, however large that literature is.
- Clinical management of recurrent pregnancy loss and stillbirth prevention is `OFF_CLINICAL_MANAGEMENT`
  and excluded.
- Non-human studies are excluded (Wall 7).
- Phenomena are **PM and FDT**. SDT-era material is retained as context under
  `SDT_AGE_COMPOSITION_CONTEXT` only.
- Maternal age and parity are recorded on every included empirical paper as mandatory confounders.
- Where the abstract cannot support the routing call, defer rather than guess.

## Expected shape of the evidence (a caution, not a result)

The reconnaissance pass gives an unusually clear advance picture, and it is worth stating before the
search runs so that what comes back is read correctly.

1. **Precision, not recall, is the binding constraint, and by a wide margin.** The record space is
   dominated by clinical and epidemiological work on miscarriage and stillbirth: probes on
   `"fetal loss" AND "fertility"` return roughly 6,000 records, of which the top-cited are thyroid
   guidelines, PCOS management, and antiphospholipid syndrome. The demographic seam is thin —
   `"fetal loss" AND "natural fertility"` returns 3 records and `"stillbirth" AND "fertility decline"`
   returns 16. The search must be built to find a small seam inside a large adjacent literature, which
   is the opposite of D.3.b's discovery problem.
2. **`OFF_CLINICAL_MANAGEMENT` and `OFF_OUTCOME` will together be most of the corpus.** That is a fact
   about the literature and not a screening defect.
3. **The `PRIMARY_SHOCK_TO_BIRTHS` cell is small but real and is where the chapter's identification
   will come from.** The reconnaissance already located famine studies in *Demography* (Chinese famine
   involuntary fetal loss, 2005; intrauterine malnutrition and fertility outcomes, 2014), the Dutch
   Hunger Winter re-examination in *Population Studies* (1993), and 1918–1920 influenza pandemic birth
   and stillbirth studies. Expect this cell to hold single digits to low tens of studies.
4. **The parameter stream will be larger and better identified than the causal stream.** Loss rates by
   maternal age, by gestational week, and by infection status are well measured. This inverts the usual
   pattern in this review, where the parameter is scarce and the topic literature is abundant, and it
   means the demographic-significance computation may rest on firmer ground than the GRADE rating.
5. **Prior meta-analyses exist for loss *prevalence* and for global stillbirth *estimates*, not for the
   fertility consequence.** Channel 1 is therefore rich for `PARAMETER_LOSS_LEVEL` and near-empty for
   the primary cell. A near-empty channel 1 on the estimand of interest is itself a finding and is
   reported as one.
6. **A pooled meta-analytic estimate may not be defensible.** If the primary cells yield fewer than
   three estimates sharing an estimand level, a loss window, and a fertility regime, PROTOCOL §5.9
   directs narrative synthesis, and the honest chapter reports a decomposition built on parameters with
   an explicit uncertainty range rather than a forest plot assembled from incommensurable quantities.

## Cold-start channels and leakage wall

1. Direct empirical papers estimating intrauterine survival → live-birth fertility, and shock studies
   running through that channel, seed the empirical Tier-A candidate set.
2. Proximate-determinants theory (Bongaarts; Bongaarts and Potter; Leridon; Wood; Sheps and Menken)
   seeds the theory set and earns no empirical recall credit.
3. Loss-rate measurement and reporting-quality papers seed the methods and parameter streams.
4. References and citations of the independent seeds create the orthogonal Tier-B frame. Forward
   citation is applied uniformly across seed types, including routing decoys, with `seed_ids`
   provenance retained so Recall(B) can be computed with and without decoy-seeded material.
5. Production-query terms are not mined from a paper that is then used to evaluate the query; learned
   extensions are fold-local once the gold frame exists.

## Pre-query anchor audit

The verified candidate anchor set is stored in
`fetal-loss-intrauterine-mortality-cold-start-anchors.json`. Three gates apply, all mandatory:

- **Existence gate** (OAS, 2026-07-08): a live DOI or a Crossref/publisher record confirming the title
  exists. No anchor is asserted from memory, and no author list is either — candidate author lists
  asserted from memory have been wrong every time they were checked.
- **Version-of-record gate** (D.1.b, 2026-08-07): an anchor resolving to a working paper, preprint,
  reprint, or review *of* the work fails, even at title Jaccard 1.0.
- **Book-canon gate** (D.2.d, 2026-08-08): monographs resolve to their own reviews at perfect title
  confidence. This gate is load-bearing here, because three of B.5's four canonical theory sources are
  books — Bongaarts and Potter 1983, Wood 1994, Leridon 1977 — and the chapter's central historical
  source, Woods 2009, already returns three review records alongside the monograph in a live probe.
  The author gate and the fallback flag are both required; neither alone suffices.

The set deliberately contains primary, shock, replacement, parameter, measurement, theory, and
off-cell decoy anchors (A.1 child mortality, B.3 sterility, A.4 induced abortion, A.15 maternal age,
and a veterinary reproductive-wastage record for Wall 7), so the search is tested on routing as well
as on topical retrieval.

## Scope calls for the PI

**Call 1 — how to score the FDT verdict given the inverted sign. Recommended: report magnitude and
sign separately, and score demographic significance on the absolute contribution.** B.5 predicts that
falling intrauterine mortality *raised* live-birth fertility during the FDT. Under PROTOCOL §4.2 as
written, a hypothesis is demographically significant if it accounts for ≥10% of observed TFR change,
which implicitly assumes the hypothesis pushes in the direction of the observed change. Three options:
- *(a) Recommended.* Score the FDT cell on the absolute size of the contribution, report the sign
  explicitly, and state in the verdict table that a significant B.5 effect implies the behavioral
  component of the FDT was **larger** than the raw TFR decline. Rationale: it preserves the
  quantitative threshold, and the offsetting-force finding is genuinely informative for the review's
  other chapters, which are collectively trying to explain a decline whose true size this would revise.
- *(b)* Score B.5 as "not significant" for the FDT on the grounds that it does not explain the decline.
  Rejected: it discards a real quantitative finding on a definitional technicality and would make the
  chapter's FDT section unwritable.
- *(c)* Drop the FDT cell. Rejected: it is where most of the measured variation in intrauterine
  mortality actually sits.

This call generalizes beyond B.5 — any hypothesis whose predicted sign opposes the phenomenon it is
assigned to faces it — so a PI ruling here should probably be written into PROTOCOL §4.2 rather than
into this chapter alone.

**Call 2 — the SDT boundary against A.15. Recommended: no SDT cell, context only.** Rising maternal
age raises loss rates, which lowers realized SDT fertility, and A.15's claim text already owns that
mechanism explicitly. Opening a B.5 SDT cell would duplicate A.15 and would double-count the same
effect in the review's synthesis. Recommendation: no pooled SDT cell; SDT-era estimates retained as
`SDT_AGE_COMPOSITION_CONTEXT` and used only to inform parameters. The residual question — whether the
*within-age* loss rate has changed in the SDT era for reasons other than composition, which would be
B.5's alone — is recorded as an open question in the chapter rather than searched for as a cell.

**Call 3 — B.3's claim text claims B.5's channel, which is a definitional problem in v5.** v5's B.3
entry states that infections reduce fecundity "through tubal damage, fetal loss, and amenorrhea",
naming B.5's channel inside B.3's claim. Wall 2 above is a workable operational line — B.3 owns the
conception margin, B.5 owns survival — but the two entries should be re-worded so the distinction
lives in HYPOTHESES rather than only in this scope document, and so that whichever chapter runs second
does not find its evidence already claimed. Flagged for TICK-001; does not block this run.

**Call 4 — whether the parameter stream earns a GRADE rating. Recommended: no.** Most of B.5's
best-measured evidence estimates loss rates and their determinants without touching fertility. That
stream is essential to the demographic-significance computation and is not evidence for the causal
claim, so rating it would inflate the chapter's GRADE. Recommendation: GRADE is assigned on the
primary cells alone, the parameter stream is reported with its own quality description in §7 of the
chapter, and the distinction is made explicit in the verdict table so a reader does not credit the
causal claim with the parameter literature's precision.

## Next step

A3 — source and triple-gate the cold-start anchors
(`source/build/goldset/116_b5_cold_start_anchors.py`). Script numbering starts at **115** (the
reconnaissance probe above): 88 is the highest on `main`, D.1.b holds 95–102 on an unmerged branch,
and the D.2.d run consumed 103–114.
