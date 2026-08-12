# Search scope — antidepressants and pharmacological subfecundity

**Hypothesis:** B.7 (HYPOTHESES-v5.md)
**Hypothesis slug:** `antidepressants-ssri-subfecundity`
**Target phenomena:** SDT only, and within the SDT only the post-1988 sub-period. The exposure did not
exist for the first two decades of the phenomenon it is assigned to — see "Phenomenon scope" and
Call 1. No PM cell, no FDT cell.
**Ticket:** TICK-066
**Status:** **DRAFT** (Shravan, 2026-08-12). Eight boundary walls specified, five scope calls raised
with recommendations. Walls freeze after the PI answers Call 1 and Call 3, or after a decision to
proceed on the recommendations. Anchor sourcing (A3) is **not** blocked by the freeze.

Built on the B.5 (`fetal-loss-intrauterine-mortality`) template, which inherits D.2.d's and D.3.b's.
Four constraints carry forward as design decisions rather than being rediscovered: the taxonomy
carries `INSUFFICIENT_INFO` and a catch-all `OFF_OTHER`; a wall whose discriminator is invisible in a
title or abstract is declared unenforceable up front instead of being trusted and audited later; the
forward-citation seed rule is uniform across seed types, with no special case for routing decoys; and
an arithmetic statement of the mechanism is treated as an upper bound to be corrected rather than as
the effect.

The scope below is written against a live reconnaissance pass over OpenAlex (2026-08-12, 54 probes,
zero failed requests, so the reported zero-hit counts are genuine absences rather than refusals). The
counts quoted in "Expected shape of the evidence" come from that pass, which is regenerable via
`source/build/goldset/123_b7_recon_probe.py` and reported in
`antidepressants-ssri-subfecundity-recon-probe.md`.

## Causal claim

Antidepressant medication, taken by roughly one in eight adults in high-income countries and by a
larger share of women than men, impairs sexual desire and orgasm in a substantial fraction of users
and may additionally perturb the reproductive endocrine axis. If those impairments reduce the rate at
which exposed people conceive, and if exposure is prevalent enough, the medication is a cause of lower
population fertility that operates without any change in what anyone wants.

The claim's position in the causal chain is what makes this chapter difficult, and the difficulty is
the reverse of B.5's. B.5 was defined by a channel whose drivers all belonged to other chapters. B.7
is defined by a **treatment** — a specific, well-measured, precisely dated pharmaceutical exposure —
whose **outcome** belongs to another chapter. The medication's proximate effect is on sexual function;
sexual function's effect on conception is A.14's (`coital-frequency-biological`); and the fertility
quantity the review cares about sits two links further down. What B.7 owns is the drug and the first
link. Everything the hypothesis asserts beyond that is a chain of inference, and the chapter's job is
to price each link rather than to assert the product.

## The chain is three links and the evidence is concentrated in the first

The hypothesis as stated in v5 compresses three distinct empirical propositions into one sentence.
They have wildly different evidence bases, and pooling them — or rating them together — is the main
way this chapter could go wrong.

| Link | Proposition | Where the evidence lives |
|---|---|---|
| **1** | Antidepressant use → sexual dysfunction (reduced desire, impaired orgasm) | Large, partly randomised, clinically measured. The best-evidenced link in the chapter. |
| **2** | Sexual dysfunction → reduced coital frequency | Thin. Desire, function, and behaviour are measured by different instruments in different literatures and are rarely estimated as a causal step. |
| **3** | Reduced coital frequency → reduced conception | Owned by A.14. Well studied, and **strongly non-linear** — the marginal return to additional acts falls off sharply, and couples who are trying to conceive time intercourse to the fertile window. |

Link 3 is where the naive version of the hypothesis fails, and it fails for a reason worth stating
plainly. For a couple actively trying to conceive, coital frequency is rarely the binding constraint:
conception probability per cycle is close to flat above two or three well-timed acts per week, so a
decrement in desire has to be very large before it moves the conception hazard at all. Where B.7 can
still bite is on people who are *not* deliberately trying — where reduced desire changes whether a
partnership forms, whether it persists, and whether unplanned conception occurs. That is a real
channel and it is a different channel from the one the mechanism paragraph in v5 describes.

**Consequence, pre-committed rather than discovered:** every included estimate is tagged with the link
it identifies, links are **never pooled across**, and the chapter's GRADE rating attaches to the
composite claim rather than to link 1. A chapter that rated link 1 and reported the rating would earn
"Moderate" or better for a proposition nobody disputes and would tell the reader nothing about whether
antidepressants affect fertility. See Call 4.

## Exposure duration is the deflator, and it is large

The second arithmetic problem is the direct analogue of B.5's, and it is the reason a large prevalence
figure does not imply a large fertility effect.

Write $p$ for the share of reproductive-age person-time spent under antidepressant exposure and $\delta$
for the proportional reduction in the conception hazard while exposed. The share of conceptions
forgone during exposure is $p\delta$ — but a conception not achieved in month $t$ is not a birth
forgone. It is a birth **postponed**, and where the reproductive span does not bind, the postponed
conception is recovered after discontinuation. Antidepressant treatment episodes are short relative to
the reproductive span: a typical episode runs months to a few years against a span of roughly
twenty-five. Even a hypothetical exposure that suppressed conception completely would, for most users,
move births in time rather than remove them.

The effect on completed fertility is therefore governed by the same regime condition B.5 identified,
arriving from the opposite direction:

- **Where the reproductive span binds** — late starters, women exposed in their late thirties, couples
  whose window is already short — exposure-driven delay converts into forgone births at close to the
  full rate.
- **Where it does not bind** — most exposed person-time — exposure changes birth timing and not birth
  count, and the effect on completed fertility approaches zero.

There is also a channel that does not run through delay at all: exposure that alters whether a union
forms or persists removes births rather than postponing them. That channel is not deflated by
recuperation, and it is the one for which the chapter has the least evidence.

Every included estimate is therefore tagged with an **estimand level**:

| Level | What it measures |
|---|---|
| `HAZARD_DECREMENT` | The effect on the per-cycle or per-period conception hazard, on time-to-pregnancy, or on a semen or sexual-function parameter. An input, not a fertility quantity. |
| `TEMPO_ADJUSTED_QUANTUM` | The effect on completed fertility, cohort parity, or TFR after whatever recuperation the population actually does. This is the quantity the review's demographic-significance verdict requires. |

The two levels are **never combined into one pooled estimate**, and any figure built on
`HAZARD_DECREMENT` carries the standing caveat that it assumes no recuperation. This is the same
discipline B.5 applies to accounting versus behavioural estimands, and D.3.b and D.2.d to stated
versus realized fertility, on a third axis.

## Phenomenon scope

**SDT: the only cell, and it is a sub-period.** Fluoxetine reached the US market in 1988. The SDT is
dated from about 1965, and in the OECD the larger part of the TFR decline — from roughly 2.7 to
roughly 1.8 — was complete before any SSRI was prescribed. B.7 cannot have caused a decline that
finished before the exposure existed. Scored against the full SDT change, the hypothesis is credited
with a denominator it had no access to; scored against the post-1988 change, it faces a much smaller
denominator and a much more demanding test. The chapter computes and reports **both**, and takes the
post-1988 figure as the verdict. See Call 1.

**FDT: no cell.** Iproniazid and imipramine date from the 1950s, within the FDT window as this review
defines it, but prescribing volumes in that period were negligible against the reproductive-age
population and the FDT closes in 1965. No search cell is opened. Records from the tricyclic era are
retained under `PARAMETER_PREVALENCE` where they document the exposure series.

**PM: no cell.** The exposure did not exist.

This is not a scoping convenience. A hypothesis whose exposure post-dates most of its assigned
phenomenon is a recurring structural feature of the review's newer entries — B.6 (microplastics and
PFAS), C.2.h (digital leisure), D.3.b (climate anxiety) and C.3.b (student debt) all share it — and
the review needs one ruling rather than five improvised ones. Call 1 asks for it.

## The eight boundary walls

Seven of the eight separate B.7 from a chapter that shares either its treatment or its outcome. The
organising question differs from B.5's. B.5 owned a channel and routed on **what was measured**; B.7
owns a treatment and routes on **what is measured and whether the medication is the variation** — the
two tests are both required here because the drug appears as a covariate in enormous literatures that
estimate something else entirely.

**Wall 1 — B.7 vs D.3.a (Mental Health Epidemic, `mental-health-anxiety-epidemic`).** The sharpest
wall in the chapter, and the one that decides whether it has any content. Nobody takes an
antidepressant at random. The exposed are depressed or anxious, and depression and anxiety plausibly
reduce fertility on their own — through partnering, through libido, and through intention.
- **D.3.a asks:** does the *disorder* reduce fertility?
- **B.7 asks:** does the *medication* reduce fertility **beyond** the disorder?
- **Discriminator:** an estimate whose exposure contrast is diagnosed-versus-undiagnosed, or symptom
  score, routes to `INDICATION_BASELINE_D3A`. An estimate whose contrast is medicated-versus-unmedicated
  **within** an indicated population — active comparator, new-user design, discordant siblings,
  within-person time-varying exposure, or an instrument for prescribing — is B.7.
- **A medicated-versus-general-population contrast is neither**, and it is what most of the literature
  reports. Those records take `MIXED_INDICATION_UNRESOLVED` and are adjudicated at full text. They are
  not excluded, because excluding them would empty the chapter; they are marked, and their
  risk-of-bias rating reflects it.
- **The sign of the confound is not obvious and must not be assumed.** Untreated depression suppresses
  fertility, so a medicated-versus-general contrast overstates the drug's decrement; but successful
  treatment restores function, so the medication's *net* effect on an indicated person can be
  positive. B.7 as stated in v5 assumes the pharmacological decrement dominates the therapeutic
  benefit. That is an assumption and the chapter reports it as one. See Call 2.

**Wall 2 — B.7 vs A.14 (Coital Frequency and Fecundability, `coital-frequency-biological`).** A.14
owns link 3 and B.7 owns links 1 and 2, and v5's A.14 entry already names B.7 as one driver of
declining libido.
- **Discriminator:** an estimate of coital frequency → conception with no medication content is A.14's
  and enters B.7 only as `LINK3_COITAL_TO_CONCEPTION`, a borrowed parameter that earns no causal
  recall credit here. An estimate of medication → sexual function or medication → coital frequency is
  B.7's.
- The parameter is nonetheless load-bearing: without it, no `HAZARD_DECREMENT` from link 1 can be
  translated into anything the review's verdict can use. The chapter records the non-linearity of the
  coital-frequency–fecundability relation explicitly, because assuming linearity is the single
  largest source of overstatement available to this hypothesis.

**Wall 3 — B.7 vs B.5 (Fetal Loss, `fetal-loss-intrauterine-mortality`), stated reciprocally.** B.5's
scope document (2026-08-11, its Wall 3) already routes this boundary, and B.7 adopts its rule verbatim
so the two chapters cannot both claim the same studies.
- **Rule:** B.7 owns **variation in the determinant**; B.5 owns **the intrauterine-survival channel and
  its fertility consequence**. A study estimating antidepressant exposure → miscarriage risk is a study
  of B.5's channel driven by B.7's treatment. With a fertility outcome, B.5 claims it and
  cross-references B.7. Without one, it is a parameter paper (`PARAMETER_DETERMINANT_TO_LOSS`), useful
  to B.5's decomposition and to this chapter's mechanism section, and counted toward neither chapter's
  causal recall.
- The consequence is quantitatively large and worth stating in advance: the antidepressant-and-
  miscarriage literature is one of the bigger cells in the corpus and **almost all of it routes out of
  B.7's recall denominator**. That is a precision gain, not a loss.

**Wall 4 — B.7 vs the pregnancy-safety literature.** The largest single body of work naming this
chapter's exposure asks whether antidepressant use *during* pregnancy harms the fetus: congenital
malformations, persistent pulmonary hypertension, preterm birth, birth weight, autism, neonatal
adaptation.
- **Discriminator:** the sample is conditioned on pregnancy and the outcome is a property of a birth
  that occurred. No fertility quantity — no count of births, no conception hazard — is estimated.
  These route to `OFF_PREGNANCY_SAFETY` and are excluded.
- The wall has no sibling hypothesis to route to; the literature simply is not about fertility. It is
  stated because it is expected to be the largest cell in the screen by a wide margin, and because
  its records match every keyword this chapter would otherwise use.

**Wall 5 — B.7 vs A.17 (ART Access, `art-access-fertility-recovery`).** Clinical fertility-treatment
populations supply the cleanest measured reproductive outcomes for medicated people, and they are
selected on subfecundity, observed under protocol, and treated with interventions that dominate any
medication effect.
- **Discriminator:** antidepressant exposure and IVF or ICSI cycle success routes to `OFF_ART_A17`
  when the estimand concerns treatment outcome, and is admissible to B.7 only as
  `PARAMETER_HAZARD_CLINICAL` with the selection flagged. No ART-derived hazard ratio is transported
  to a general population without an explicit adjustment argument recorded at extraction.

**Wall 6 — antidepressants versus the rest of the psychotropic formulary.** v5 scopes B.7 to
antidepressants, and the mechanism paragraph is specific to serotonergic action. But antipsychotics
raise prolactin, and hyperprolactinaemia suppresses ovulation and causes amenorrhoea — a
*mechanistically stronger* fecundity pathway than anything SSRIs do, and one with a well-measured
clinical literature.
- **Rule as written:** antidepressants are the primary cell. Antipsychotics, mood stabilisers and
  anticonvulsants route to `ADJACENT_PSYCHOTROPIC`, are retained and indexed, and are never pooled with
  the primary cell.
- The hypothesis's own logic argues for revisiting this, since an aggregate effect is prevalence times
  effect and B.7's case rests entirely on the prevalence factor. A drug class with a larger $\delta$
  and a smaller $p$ is the same hypothesis with the factors swapped. See Call 3.

**Wall 7 — human versus non-human.** Reconnaissance found the animal and ecotoxicology literature not
merely present but **dominant in exactly the vocabulary this chapter most needs**: on the query pairing
antidepressants with "fecundity", the highest-cited records are studies of *Daphnia*, killifish,
molluscs, zebrafish and medaka exposed to fluoxetine in water. Non-human studies route to `OFF_ANIMAL`
and are excluded. Unlike B.5's Wall 7, this one is not cheap — it is the single most likely source of
a corrupted top-of-ranking, and the screen must be told to check species on every record.

**Wall 8 — B.7 vs B.2 / B.6 (environmental exposure, `endocrine-disruptors-environmental-toxins`,
`microplastics-pfas-reproductive`).** Antidepressants reach surface water through wastewater and are
studied as environmental contaminants.
- **Discriminator:** exposure via prescription and ingestion is B.7; exposure via environmental
  contamination is B.2/B.6 and routes to `OFF_ENVIRONMENTAL_B2B6`. In practice most such records are
  also non-human and are caught by Wall 7 first; the wall is stated so that the human environmental-
  exposure records, which exist, do not fall through.

## What the title/abstract screen can and cannot enforce

Every wall above discriminates on something usually named in an abstract — the exposure, the outcome,
the setting, the species — with one large exception, and the exception is the wall that matters most.

| Wall | Enforceable at title/abstract? | Why |
|---|---|---|
| 1 (D.3.a), *is the exposure the drug or the disorder* | **Yes** | The exposure is named. |
| 1 (D.3.a), *is the indication handled* | **No** | Active comparator, new-user design and sibling structure are methods facts. Abstracts of observational pharmacoepidemiology name the design inconsistently. |
| 2 (A.14) | **Yes** | Whether the record contains medication content is visible. |
| 3 (B.5) | **Yes** | Whether a fertility outcome is estimated alongside the loss outcome is visible; that is the whole test. |
| 4 (pregnancy safety) | **Yes** | Sample conditioning on pregnancy is named, almost always in the title. |
| 5 (A.17) | **Yes** | The clinical setting is named. |
| 6 (drug class) | **Yes** | The class is named. |
| 7 (species) | **Yes**, but only if asked | Named — but the vocabulary overlap with the human literature is total, so the screen must check species explicitly on every record rather than inferring it from topic. |
| 8 (environmental) | **Yes** | Named. |
| Link assignment (1 / 2 / 3) | **Yes** | The outcome is named. |
| Estimand level (hazard vs quantum) | Partly | Time-to-pregnancy and completed-fertility outcomes are distinguishable; a "fertility" outcome unqualified is not. |
| Ascertainment of sexual dysfunction | **No** | Spontaneous report versus direct questioning changes measured prevalence several-fold and is a methods fact. |

**Consequence, pre-committed rather than discovered:** the screen assigns a routing cell and a link
with reasonable confidence, and it does **not** assign the indication-handling status or the
ascertainment method. Every included empirical paper enters full text with `INDICATION_DESIGN` unset,
and a record whose routing turns on Wall 1's design question takes `MIXED_INDICATION_UNRESOLVED` rather
than a substantive cell.

## Estimand cells

| Cell | Treatment / variation | Outcome | Routing |
|---|---|---|---|
| `PRIMARY_MEDICATION_TO_FERTILITY` | Antidepressant exposure | A fertility quantity: births, completed parity, TFR, time-to-pregnancy, fecundability | Primary synthesis — **the identification-bearing cell** |
| `PRIMARY_MALE_FECUNDITY` | Antidepressant exposure | A measured male fertility outcome, not a semen parameter | Primary synthesis, male stratum |
| `LINK1_MEDICATION_TO_SEXUAL_FUNCTION` | Antidepressant exposure | Desire, arousal, orgasm, sexual dysfunction incidence | Primary support, link 1 |
| `LINK2_FUNCTION_TO_COITAL_FREQUENCY` | Sexual dysfunction or desire | Frequency of intercourse, sexual activity | Primary support, link 2 — the chain's weakest measured joint |
| `LINK3_COITAL_TO_CONCEPTION` | Coital frequency | Conception hazard, fecundability | Borrowed from A.14; **not** in the causal recall denominator |
| `ENDOCRINE_MECHANISM` | Antidepressant exposure | Prolactin, gonadotropins, testosterone, semen parameters | Mechanism stream; supplies the endocrine pathway's plausibility, earns no causal recall |
| `PARAMETER_PREVALENCE` | — | Exposure prevalence, dispensing volume, duration of use, by age and sex | Parameter stream; feeds demographic significance; **not** in the recall denominator |
| `PARAMETER_HAZARD_CLINICAL` | Antidepressant exposure in a fertility-clinic population | Cycle-level conception or live birth | Parameter, selection-flagged (Wall 5) |
| `PARAMETER_DETERMINANT_TO_LOSS` | Antidepressant exposure | Fetal loss, no fertility outcome | Parameter; cross-filed to B.5 (Wall 3); neither chapter's recall |
| `INDICATION_BASELINE_D3A` | Depression, anxiety, or psychiatric diagnosis | Fertility | Routes to D.3.a; retained as the counterfactual B.7 must net out |
| `MEASUREMENT_ASCERTAINMENT` | — | How sexual dysfunction or exposure is ascertained; spontaneous report versus direct questioning; prescription fill versus adherence | Methods stream; load-bearing for risk of bias |
| `THEORY_SEROTONERGIC` | Formal or physiological account of serotonergic action on sexual motivation | — | Theory stream; no empirical recall credit |
| `ADJACENT_PSYCHOTROPIC` | Antipsychotics, mood stabilisers, anticonvulsants | Any reproductive outcome | Retained, indexed, never pooled — see Call 3 |
| `OFF_PREGNANCY_SAFETY` | Antidepressant exposure in pregnancy | Fetal, neonatal or child outcome | Excluded — Wall 4; expected to be the largest cell |
| `OFF_ART_A17` | Antidepressant exposure in ART | Cycle treatment success | Route to A.17 |
| `OFF_FETAL_LOSS_B5` | Antidepressant exposure | Fetal loss **with** a fertility consequence estimated | Route to B.5 |
| `OFF_ENVIRONMENTAL_B2B6` | Environmental antidepressant contamination | Any | Route to B.2 / B.6 |
| `OFF_CLINICAL_MANAGEMENT` | Treatment of antidepressant-induced sexual dysfunction — bupropion augmentation, sildenafil, drug switching | Clinical | Excluded |
| `OFF_ANIMAL` | Non-human exposure | Any | Excluded — Wall 7 |
| `OFF_OUTCOME` | Antidepressant exposure | A non-fertility, non-sexual outcome | Excluded |
| `MIXED_INDICATION_UNRESOLVED` | Medicated versus general population, indication not handled | Fertility | Held; adjudicated at full text |
| `ROUTING_DEFERRED_TO_FULLTEXT` | Routing turns on Wall 1's design question, abstract silent | Fertility | Held; adjudicated at full text |
| `REVERSE` | Low sexual desire, subfecundity, or childlessness raising the probability of diagnosis or prescription | Exposure | Context — and see the identification cautions |
| `OFF_OTHER` | Non-B.7 fertility determinant with no sibling-hypothesis home | Fertility | Route out; no sibling queue |
| `INSUFFICIENT_INFO` | Cannot be routed on the visible record | Unknown | Pairs only with `UNCERTAIN` |

`THEORY_SEROTONERGIC`, `MEASUREMENT_ASCERTAINMENT`, `ENDOCRINE_MECHANISM`, all three `PARAMETER_*`
cells, `LINK3_COITAL_TO_CONCEPTION` and `ADJACENT_PSYCHOTROPIC` carry verdict `RELEVANT` and are
separated downstream. None counts toward empirical recall.

## The identification cautions

**Confounding by indication is the estimand, not a nuisance.** This bears repeating in the operational
section because it changes what counts as a good study. A large, well-powered registry study of
medicated versus unmedicated women, adjusted for age, income and education, is *not* informative about
B.7 no matter how large it is, because the adjustment set does not contain the reason for the
prescription. A small study with an active comparator or a within-person design is worth more than a
national registry without one. Study size is close to uninformative about study value here, and the
extraction and risk-of-bias stages are built to say so.

**Reverse causation runs through the prescription.** Low sexual desire is a symptom that brings people
to clinical attention; infertility causes distress that is treated; childlessness is associated with
depression. Each produces a positive association between medication and subfecundity with no causal
path from drug to fertility at all. A cross-sectional association between current antidepressant use
and low fertility is, on its own, close to uninterpretable.

**Depression suppresses sexual function before treatment starts.** The pre-treatment baseline is not
the general population's, and studies that compare medicated patients to healthy controls attribute
the disorder's effect to the drug. Whether a study established a pre-treatment sexual-function
baseline is recorded on every link-1 record.

**Ascertainment determines the measured size of link 1.** Spontaneously reported sexual side effects
run far below the rate obtained by direct questioning with a structured instrument, and the literature
contains both. An estimate's ascertainment method is recorded and estimates are not pooled across
methods.

**Exposure is measured as prescription, and prescription is not ingestion.** Dispensing records
overstate exposure through non-adherence and understate duration through gaps. Discontinuation at
pregnancy recognition — and, in the population B.7 cares about, at pregnancy *intention* — is
systematic and is correlated with the outcome. A woman who stops her SSRI in order to conceive appears
in a registry as exposed-then-unexposed for reasons that are downstream of fertility intention.

**Designs that can survive all of this** have variation in medication exposure that is not generated by
the person's own reproductive circumstances: formulary changes, reimbursement and coverage
discontinuities, prescriber-preference instruments, guideline changes, patent expiry and price
shocks, and within-person switching between active comparators. Those are the primary targets of the
search, and `PRIMARY_MEDICATION_TO_FERTILITY` exists to hold them.

## When to adjudicate mechanisms

The title/abstract screen assigns the routing cell and the link only. For every included empirical
paper, full-text extraction records:

- `DRUG_CLASS` and `AGENT` — SSRI, SNRI, tricyclic, other; and the specific molecule where reported,
  since sexual side-effect profiles differ sharply within class;
- `EXPOSURE_MEASURE` — prescription issued, dispensed, self-reported use, or serum level; and the
  exposure window relative to the outcome;
- `INDICATION_DESIGN` — active comparator, new-user, sibling, within-person, instrument, or none. The
  field that decides whether the estimate speaks to B.7 at all (Wall 1);
- `ESTIMAND_LEVEL` — `HAZARD_DECREMENT` or `TEMPO_ADJUSTED_QUANTUM`, the field that decides poolability;
- `LINK` — 1, 2, 3, or direct-to-fertility;
- `ASCERTAINMENT` — for link-1 estimates, spontaneous report or direct structured questioning, and the
  instrument;
- `BASELINE_ESTABLISHED` — whether pre-treatment sexual function was measured;
- `EXPOSURE_DURATION` — episode length, which is the deflator of any quantum figure;
- `SEX` — the estimate's sex stratum, recorded on every row because the mechanism and the evidence base
  differ by sex and the hypothesis text and the evidence disagree about which sex carries the effect;
- `CONFOUNDERS_ADJUSTED` — depression severity and psychiatric history are mandatory; age, parity,
  partnership status and socioeconomic position are recorded when present.

Drafting may report only what these fields support. A study finding that antidepressant users have
fewer children documents an association between being the kind of person who takes an antidepressant
and having fewer children; it must not be described as evidence that the medication reduces fertility,
absent an `INDICATION_DESIGN` that identifies it.

## Eligibility rules

- Include empirical studies where the estimate bears on **antidepressant exposure → a fertility
  quantity**, or on one of the three named links, with the link recorded.
- Studies conditioned on pregnancy whose outcome is a property of the birth are `OFF_PREGNANCY_SAFETY`
  and excluded, however large that literature is.
- Antidepressant → fetal loss studies with no fertility outcome are `PARAMETER_DETERMINANT_TO_LOSS`:
  retained, indexed, cross-filed to B.5, and excluded from the causal recall denominator (Wall 3).
- Treatment of antidepressant-induced sexual dysfunction is `OFF_CLINICAL_MANAGEMENT` and excluded.
- Non-human studies are excluded (Wall 7), and species is checked on every record rather than inferred.
- Non-antidepressant psychotropics are `ADJACENT_PSYCHOTROPIC`: retained, never pooled (Wall 6).
- Phenomenon is **SDT**, and within it the post-1988 sub-period. Pre-1988 material is retained only as
  `PARAMETER_PREVALENCE` where it documents the exposure series.
- Depression → fertility studies with no medication contrast are `INDICATION_BASELINE_D3A`: retained as
  the counterfactual baseline, routed to D.3.a, and excluded from B.7's recall denominator.
- Where the abstract cannot support the routing call, defer rather than guess.

## Expected shape of the evidence (a caution, not a result)

The reconnaissance pass gives an unusually clear advance picture, and it is worth stating before the
search runs so that what comes back is read correctly.

1. **Precision binds, and by the widest margin of any chapter run so far.** Antidepressants paired with
   pregnancy or prenatal exposure return roughly 5,650 records; paired with any fertility-rate term,
   48 — and inspection of those 48 shows every one of the top-cited to be a pregnancy-safety study
   that happens to use the phrase "birth rate". The seam is not thin, it is close to absent, and the
   search must be built to find single studies inside an adjacent literature two orders of magnitude
   larger.
2. **The population-level cell may be empty.** Probes for aggregate, ecological or country-level
   antidepressant-and-births work returned 35 records with nothing on topic among the most-cited. If
   the search confirms this, **the finding is that no one has estimated the quantity the hypothesis
   asserts**, and the chapter reports that as its primary result rather than assembling a proxy.
3. **The measured evidence is male and the hypothesis text is female.** v5's claim emphasises women
   "particularly", but what resolves in the record is male: an *Andrology* study of SSRI use and
   fertility in men, semen-parameter studies in *Fertility and Sterility*, *The Journal of Urology* and
   *Urology*, and a review of antidepressants and male fertility in the *International Journal of
   Urology*. The female pathway is behavioural and is measured, where it is measured at all, as sexual
   function rather than as fertility. This mismatch is a finding about the literature and is reported
   as one.
4. **Link 1 is abundant and of high quality; links 2 and 3 are the bottleneck.** Antidepressants paired
   with sexual dysfunction return roughly 2,480 records including randomised evidence and a
   prospective multicentre incidence study of over a thousand outpatients. Nothing comparable exists
   for the step from dysfunction to coital frequency. A chapter that rated the evidence it has rather
   than the evidence the claim needs would return a confident rating for the wrong proposition.
5. **The animal literature owns the vocabulary.** On the fecundity-term probes the top-cited records are
   ecotoxicological studies of aquatic invertebrates and fish. This is not a tail risk to be audited
   later; it is the expected top of the ranking, and Wall 7 has to be enforced at screen rather than at
   extraction.
6. **The parameter stream is strong where the causal stream is weak.** Exposure prevalence is measured
   very well — national dispensing registries, NCHS data briefs, OECD defined-daily-dose series — so the
   demographic-significance computation will rest on firmer ground than the GRADE rating, the same
   inversion B.5 found. The chapter must not let the precision of the prevalence figure transfer to the
   effect figure it multiplies.
7. **Channel 1 is rich for link 1 and empty for the claim.** Systematic reviews and meta-analyses of
   antidepressant-induced sexual dysfunction exist in number. No prior review of antidepressants and
   fertility at the population level was located. A near-empty channel 1 on the estimand of interest
   is itself a finding and is reported as one.
8. **A pooled meta-analytic estimate is unlikely to be defensible.** If the primary cells yield fewer
   than three estimates sharing a link, an estimand level and a sex stratum, PROTOCOL §5.9 directs
   narrative synthesis, and the honest chapter reports a decomposition built on parameters with an
   explicit uncertainty range rather than a forest plot assembled from incommensurable quantities.

## Cold-start channels and leakage wall

1. Direct empirical papers estimating antidepressant exposure → a fertility quantity, in either sex,
   seed the empirical Tier-A candidate set.
2. Link-1 clinical and randomised evidence seeds the link-1 support set and earns no credit toward the
   primary cell.
3. Serotonergic and endocrine mechanism papers seed the mechanism stream; prevalence and dispensing
   papers seed the parameter stream; ascertainment and pharmacoepidemiological-method papers seed the
   methods stream.
4. References and citations of the independent seeds create the orthogonal Tier-B frame. Forward
   citation is applied uniformly across seed types, including routing decoys, with `seed_ids`
   provenance retained so Recall(B) can be computed with and without decoy-seeded material.
5. Production-query terms are not mined from a paper that is then used to evaluate the query; learned
   extensions are fold-local once the gold frame exists.

## Pre-query anchor audit

The verified candidate anchor set is stored in
`antidepressants-ssri-subfecundity-cold-start-anchors.json`. Four gates apply, all mandatory:

- **Existence gate** (OAS, 2026-07-08): a live DOI or a Crossref/publisher record confirming the title
  exists. No anchor is asserted from memory, and no author list is either. The reconnaissance pass ran
  this gate on twenty-two remembered titles and **ten did not resolve** — including, on the first pass,
  a spontaneous-abortion study that does exist under different wording. The lesson is recorded in the
  probe report and restated here because the two failure modes have opposite consequences: an
  unresolved title means the analyst's memory is wrong, an empty group probe means the literature is
  absent, and only the second is a finding.
- **Version-of-record gate** (D.1.b, 2026-08-07): an anchor resolving to a working paper, preprint,
  reprint, or review *of* the work fails, even at title Jaccard 1.0.
- **Book-canon gate** (D.2.d, 2026-08-08): monographs resolve to their own reviews at perfect title
  confidence. Less load-bearing here than in B.5 — B.7's canon is journal articles — but retained.
- **Shadow-record gate (new, B.7, 2026-08-12).** Two record types in this literature carry titles that
  are the target title plus a prefix, and therefore resolve at near-perfect similarity: *"Editorial
  Comment to X"* in the urology journals, and *"Faculty Opinions recommendation of X"* in the
  post-publication-review index. Both were observed live in this reconnaissance, on this chapter's two
  most important anchors. The gate rejects any candidate whose title contains the target title as a
  proper substring with a leading qualifier, and the rejection is logged rather than silent.

The set deliberately contains primary, link-1, link-2, mechanism, parameter, measurement, theory, and
off-cell decoy anchors (D.3.a depression-and-fertility, A.14 coital frequency, B.5 loss, A.17 ART, a
pregnancy-safety record for Wall 4, an antipsychotic record for Wall 6, and an ecotoxicology record for
Wall 7), so the search is tested on routing as well as on topical retrieval.

## Scope calls for the PI

**Call 1 — the exposure post-dates most of the phenomenon. Recommended: score against the post-1988
denominator, and report the full-SDT denominator alongside it.** SSRIs reached market in 1988; the SDT
opens in 1965; most of the OECD TFR decline was complete before the first prescription. Three options:
- *(a) Recommended.* Compute the decomposition share against the post-1988 change in TFR, report the
  full-SDT share alongside it, and state in the verdict table which denominator the verdict uses.
  Rationale: a hypothesis cannot explain variation that preceded its cause, and scoring against the
  full-period denominator would credit it with exactly that.
- *(b)* Score against the full SDT change as PROTOCOL §4.2 is currently written. Rejected: it is
  arithmetically flattering to every late-arriving exposure in the review and would make B.6, C.2.h and
  D.3.b look larger than they are for the same reason.
- *(c)* Introduce a fourth phenomenon, "late SDT" or "post-2008 decline", into PROTOCOL §2. Rejected
  for this ticket as too large a change to make from inside one chapter, but it is the cleaner
  long-run fix and is flagged for TICK-001.

This call generalises well beyond B.7 — every hypothesis whose exposure begins part-way through its
assigned phenomenon faces it — so a PI ruling here should probably be written into PROTOCOL §4.2
rather than into this chapter alone. It is the second such general ruling to come out of a chapter
scope in two weeks; B.5's Call 1 on inverted signs is the first, and the two are the same kind of gap
in §4.2's implicit assumptions about how a hypothesis relates to its phenomenon.

**Call 2 — the sign is ambiguous and the hypothesis assumes it away. Recommended: score the net
effect, and report the decomposition.** Antidepressants impair sexual function, and they also treat a
condition that impairs fertility through several channels. The net effect of medicating an indicated
person could go either way, and v5's claim text assumes the pharmacological decrement dominates
without argument. Recommendation: the verdict scores the **net** effect of medication versus no
medication within an indicated population, since that is the policy-relevant and
counterfactually-coherent quantity; the chapter reports the pharmacological decrement and the
therapeutic benefit separately where the evidence allows. The alternative — scoring the direct
pharmacological decrement alone — answers a question no counterfactual world corresponds to, since the
untreated comparator is not a healthy person.

**Call 3 — whether B.7 should be antidepressants or psychotropics. Recommended: antidepressants
primary, adjacent cell retained, revisit after the screen.** Antipsychotic-induced hyperprolactinaemia
suppresses ovulation through a mechanism far more direct than anything serotonergic, with a
substantial clinical literature. B.7's case rests on prevalence rather than effect size; antipsychotics
are the same hypothesis with the two factors exchanged. Recommendation: keep v5's scope for this run,
retain antipsychotics and mood stabilisers under `ADJACENT_PSYCHOTROPIC` so the material is indexed
rather than discarded, and put the widening question to the PI with the screen counts in hand. Note
that widening would also pull in the severe-mental-illness fertility literature, which is
substantially larger than B.7's own and belongs to D.3.a.

**Call 4 — what the GRADE rating attaches to. Recommended: the composite chain, with per-link ratings
shown.** The evidence is concentrated on link 1, which is not in dispute. Rating link 1 and reporting
that rating would credit the hypothesis with the quality of evidence for a proposition it does not
need to establish. Recommendation: GRADE is assigned to the composite claim — antidepressant exposure
reduces fertility — and the three links are rated separately in a subsidiary table so a reader can see
where the chain breaks. This mirrors B.5's Call 4, which kept a strong parameter stream from inflating
a weak causal rating, and the two should probably be settled together.

**Call 5 — two corrections to the v5 entry, for TICK-001.** First, the seminal list cites "Beeder and
Bhatt PMC scoping review (2025)"; what resolves is Beeder and Bhatt, *International Journal of Urology*,
2019, on antidepressants and male fertility, and the record also carries a shadow "Editorial Comment"
entry. Second, the claim text says the medication is taken "particularly by women" and locates the
mechanism there, while the measured fertility evidence that exists is male. Neither correction blocks
this run.

## Next step

A3 — source and quadruple-gate the cold-start anchors
(`source/build/goldset/124_b7_cold_start_anchors.py`). Script numbering starts at **123** (the
reconnaissance probe above). **Numbering caution:** 88 is the highest on `main`, but the unmerged
branches now collide — D.1.a holds 95–115, D.2.d holds 103–108, D.1.b holds 95–102 and B.5 holds
115–122, so 103–115 is claimed three times over. This run starts above every number in use on any
branch rather than above `main`, and the collision is flagged in TICK-066.
