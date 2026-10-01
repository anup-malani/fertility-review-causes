# Search scope — breastfeeding and lactational amenorrhea

**Hypothesis:** A.13 (HYPOTHESES-v5.md §A.13), slug `breastfeeding-lactational-amenorrhea`.
**Ticket:** TICK-096. **Stage:** 2 (scope drafted). **Stage 3 (frame probe) is PAUSED** at the
standing "pause before the OpenAlex spend" checkpoint — do not run the probe until the RA/PI
go-ahead (405/52/A.20/A.19 precedent).

---

## Causal claim

Breastfeeding — specifically the intensity and duration of suckling — suppresses ovulation through
suckling-induced hyperprolactinemia, extending postpartum lactational amenorrhea and anovulation.
In the absence of deliberate contraception this lengthens birth intervals and lowers natural
fertility; declines in breastfeeding (shorter durations, earlier supplementation, formula
substitution) shorten intervals and raise fertility. This is Bongaarts proximate-determinant #3 —
the postpartum-infecundability index **C_i** (Bongaarts 1978; Bongaarts & Potter 1983).

## This chapter's parameter (the §4 chain)

The parameter is the effect of **breastfeeding intensity/duration** on the **length of postpartum
infecundability** (months of lactational amenorrhea → the birth interval → the C_i component of
total natural fertility), isolated from:
1. deliberate contraception and postpartum abstinence (A.2, A.5, and the abstinence component of
   C_i, which A.13 does **not** own), and
2. maternal nutrition / energy balance (A.22, deprecated).

It is a **spacing / quantum** parameter on the birth interval, **not** a desired-family-size
parameter. The headline quantity is "months of amenorrhea per unit of breastfeeding
intensity/duration," and at the aggregate level the implied change in C_i and in the mean birth
interval. The identification workhorses, in decreasing order of how cleanly they break the confounds:

1. **Prospective cohort / hazard studies of the return of menses** conditioned on measured nursing
   intensity (full vs. partial, night feeds, supplementation timing) — e.g. the WHO multicentre
   study, Kennedy & Visness.
2. **Physiological / experimental suckling-prolactin studies** (Howie & McNeilly; McNeilly) that
   establish the dose-response mechanism and rule out reverse pathways.
3. **Historical-demographic and natural-fertility reconstitutions** that recover birth-interval
   effects of breastfeeding regimes (Knodel; Wood; Konner & Worthman) — larger external validity,
   weaker individual-level identification.

## Registered-construct completeness check (the A.6/A.3 lesson)

Every construct the §A.13 claim names must be present in the Phase-1 query blocks, so the
*selecting* frame cannot be unseated by an omitted registered construct (the defect that corrected
A.6 668→1,225 and hardened A.20/A.19):

- **lactational amenorrhea** / postpartum amenorrhea — the core outcome; must be present.
- **postpartum infecundability / anovulation / return of menses / resumption of ovulation** — the
  physiological mechanism.
- **breastfeeding / lactation / nursing / suckling intensity / exclusive vs. partial / night
  feeding / supplementation** — the exposure and its dose.
- **birth interval / birth spacing / interbirth interval / natural fertility** — the fertility
  outcome and the demographic translation.
- **Bongaarts proximate determinants / C_i index** — the framework that ties it to TFR.
- **LAM (Lactational Amenorrhea Method) / Bellagio consensus** — the applied boundary case (see
  Wall 1).

**Candidate homonym / leak terms to price in the probe and likely fold-at-screen, not admit raw:**
bare `breastfeeding` (overwhelmingly an infant-health / nutrition / morbidity literature with no
fertility outcome — the dominant homonym, an order of magnitude larger than the fertility cell),
`lactation` (dairy / animal-science), `prolactin` (endocrinology unrelated to fertility spacing),
`weaning` (child-nutrition). Admit these only conjoined with a fertility / amenorrhea / birth-
interval sense, mirroring the A.19 `second generation` and A.20 `social network` keep-and-route
treatment.

## Boundary walls (the load-bearing routing rules)

- **Wall 1 — A.2 Modern Contraception (drafted) / A.5 Family Planning Programs.** A.13 owns
  *natural* child-spacing via suckling physiology. The frame must not annex studies where lactation
  is merely a covariate inside contraceptive-method or program evaluations. **LAM is the explicit
  boundary case:** when breastfeeding is adopted and promoted *as a contraceptive method*, the
  spacing effect is partly behavioural (A.2/A.5) and partly physiological (A.13). Route on which
  mechanism carries the measured effect; LAM-efficacy trials that isolate the amenorrhea mechanism
  are IN, program-adoption studies are a shared-boundary / OFF cell.
- **Wall 2 — A.22 Nutrition and Energy Availability [DEPRECATED].** The maternal-nutrition →
  amenorrhea pathway (critical-fat / energy-balance; Frisch) is physiologically entangled with
  lactational amenorrhea because undernourished nursing mothers stay amenorrheic longer. A.13 owns
  the **suckling-intensity** channel; studies that attribute the amenorrhea to maternal energy
  balance rather than to nursing behaviour route OFF. Because A.22 is deprecated, guard actively
  against the frame silently absorbing the nutrition-fecundity literature.
- **Wall 3 — infant mortality feedback (REVERSE / confound).** Early infant death terminates nursing,
  shortening amenorrhea and the interval and raising the next-birth hazard; conversely a new
  pregnancy prompts weaning. Studies whose interval variation is driven by infant death or by
  weaning-on-conception, not by the exogenous nursing regime, are a REVERSE cell (cross-ref the
  child-mortality literature, A.1) and belong outside the identified core.
- **Wall 4 — demographic-significance boundary (for stage 10, flagged now).** A.13 is load-bearing
  mainly in **natural-fertility / pre-modern (PM)** and some **LMIC** settings. In contracepting
  **FDT/SDT** populations the C_i contribution is small and dominated by deliberate control — except
  as a *historical counter-force* during the FDT, where declining breastfeeding (urbanization,
  wet-nursing, early formula) **raised** fertility and partly offset the transition. Keep that
  sign-flipped FDT channel in scope; expect PM-major, FDT-mixed/minor, SDT-minor.

## Estimand cells

| Cell | Design / content | Disposition |
|---|---|---|
| `AMENORRHEA_DURATION` | Nursing intensity/duration → months of lactational amenorrhea (cohort, hazard, WHO-type) | IDENTIFIED CORE |
| `SUCKLING_MECHANISM` | Suckling → prolactin → anovulation (physiological / experimental) | IDENTIFIED CORE (mechanism) |
| `BIRTH_INTERVAL` | Breastfeeding regime → interbirth interval / natural fertility (historical demography, reconstitution) | IDENTIFIED CORE (aggregate) |
| `LAM_EFFICACY` | LAM as method — amenorrhea-conditioned pregnancy risk (Bellagio) | IN if the amenorrhea mechanism is isolated; else Wall 1 shared-boundary |
| `MIXED_NUTRITION` | Amenorrhea attributed to maternal energy balance | Wall 2 — OFF/bounded |
| `REVERSE_MORTALITY` | Interval driven by infant death / weaning-on-conception | Wall 3 — OFF |
| `OFF_INFANT_HEALTH` | Breastfeeding → child morbidity/IQ/nutrition, no fertility outcome | OFF (dominant homonym) |

## Query blocks (for §5.1 Phase 1)

Draft — to be priced by the stage-3 frame probe. Conjunctive: (exposure) AND (mechanism/outcome),
with the infant-health homonym excluded unless a fertility sense co-occurs.

- **B1 Exposure:** breastfeeding OR lactation OR nursing OR suckling OR "breastfeeding intensity" OR
  "exclusive breastfeeding" OR "full breastfeeding" OR supplementation OR "night feeding" OR weaning
- **B2 Mechanism/outcome:** "lactational amenorrhea" OR "postpartum amenorrhea" OR "postpartum
  infecundability" OR "return of menses" OR "resumption of menses" OR "resumption of ovulation" OR
  anovulation OR "birth interval" OR "birth spacing" OR "interbirth interval" OR "natural fertility"
- **B3 Framework:** "proximate determinants" OR "Bongaarts" OR "postpartum infecundability index" OR
  C_i OR "lactational amenorrhea method" OR LAM OR "Bellagio consensus"
- **Selecting frame ≈ B1 AND (B2 OR B3).** Bare B1 (breastfeeding alone) is the recall pool, folded
  at screen with a fertility/amenorrhea homonym filter.

## Eligibility rules

- **Include:** human studies reporting a quantitative link between breastfeeding exposure and
  lactational amenorrhea duration, postpartum anovulation, birth interval, natural-fertility level,
  or the C_i index; physiological suckling-prolactin studies establishing the mechanism; LAM-efficacy
  studies that isolate the amenorrhea mechanism; historical-demographic reconstitutions of
  breastfeeding and spacing.
- **Exclude:** infant-health / nutrition / morbidity / cognition outcomes with no fertility or
  amenorrhea endpoint (dominant homonym); animal-science lactation; studies where the spacing effect
  is carried by deliberate contraception/abstinence (Wall 1) or by maternal energy balance (Wall 2),
  unless they separately identify the suckling channel; interval variation driven by infant death or
  weaning-on-conception (Wall 3).
- **Languages/period:** no date limit (PM reconstitutions are in scope); English-language screen with
  translation flagged for seminal non-English natural-fertility work.

## Identification cautions

- Breastfeeding is **not randomly assigned**: nursing intensity correlates with parity, maternal
  education, infant health, and culture — any of which independently move fertility. Prefer designs
  with measured intensity and within-population dose-response over cross-population correlations.
- **Recall and definitional heterogeneity:** "exclusive/full/partial" breastfeeding is coded
  inconsistently; amenorrhea is self-reported with recall error. Extraction (stage 7) must record the
  breastfeeding definition and the amenorrhea ascertainment.
- **Aggregation:** the C_i index translates individual amenorrhea into a population fertility effect
  only under natural-fertility assumptions; in contracepting populations the mapping breaks (Wall 4).
- **Mechanism vs. magnitude:** the suckling-prolactin mechanism is well established and near-settled
  physiology (expect high GRADE on existence); the contested quantity is the *demographic magnitude*
  and its setting-dependence, which is where the credibility rating will bind.

## Seed anchors (for the stage-3 cold-start, once un-paused)

Core (identified): Bongaarts 1978 (proximate determinants); Bongaarts & Potter 1983; Howie &
McNeilly (suckling → prolactin → ovarian suppression); Kennedy & Visness 1992 (Lancet, return of
ovulation); the WHO multicentre study of breastfeeding and lactational amenorrhea; Konner &
Worthman 1980 (!Kung nursing & birth spacing); Wood 1994 (*Dynamics of Human Reproduction*).
Decoys (one per wall): a modern contraceptive-method evaluation with lactation as covariate (Wall 1);
a Frisch critical-fat / energy-balance amenorrhea paper (Wall 2); a Preston/Knodel infant-mortality →
birth-interval study (Wall 3); a breastfeeding → infant-health outcome paper (dominant homonym).
