# Search scope — microplastics and PFAS in reproductive tissues

**Hypothesis:** B.6 (HYPOTHESES-v5.md)
**Hypothesis slug:** `microplastics-pfas-reproductive`
**Target phenomena:** SDT only. No PM cell, no FDT cell. Unlike B.7, **no sub-period restriction is
needed**: the exposure is older than the phenomenon, not younger than it — see "Phenomenon scope".
**Ticket:** TICK-068
**Status:** **DRAFT** (Shravan, 2026-08-14). Nine boundary walls specified, five scope calls raised
with recommendations. Walls freeze after the PI answers Call 1, or after a decision to proceed on the
recommendations. Anchor sourcing (A3) is **not** blocked by the freeze.

Built on the B.7 (`antidepressants-ssri-subfecundity`) template, which inherits B.5's, D.2.d's and
D.3.b's. Five constraints carry forward as design decisions rather than being rediscovered: the
taxonomy carries `INSUFFICIENT_INFO` and a catch-all `OFF_OTHER`; a wall whose discriminator is
invisible in a title or abstract is declared unenforceable up front rather than trusted and audited
later; the forward-citation seed rule is uniform across seed types with no special case for routing
decoys; an arithmetic statement of the mechanism is treated as an upper bound to be corrected rather
than as the effect; and a chapter whose evidence sits on a different proposition from its claim rates
the claim, not the evidence.

The scope below is written against two live reconnaissance passes over OpenAlex (2026-08-14; 72 + 20
probes, **zero failed requests in both**, so every zero-hit count reported here is a genuine absence
rather than a refusal). Counts are regenerable via `source/build/goldset/132_b6_recon_probe.py` and
`133_b6_anchor_retry.py`, reported in `microplastics-pfas-reproductive-recon-probe.md` and
`microplastics-pfas-reproductive-anchor-retry.md`.

## Causal claim

Microplastic particles and PFAS are present in the human reproductive tract — measured directly in
placenta, testis, semen and follicular fluid rather than inferred from serum — and that presence
impairs sperm production, ovarian function and implantation. Exposure is close to universal and, for
plastics, rising. If the impairment is real and the exposure is general, the result is a fertility
decrement that operates on biological capacity rather than on intention.

The claim's difficulty is neither B.5's (a channel whose drivers belong elsewhere) nor B.7's (a
treatment whose outcome belongs elsewhere). B.6's difficulty is that **it is two hypotheses wearing
one number**, and the two halves fail in opposite directions. PFAS has a genuine human fertility
epidemiology and an exposure series that is falling. Microplastics has a genuine and rapidly growing
tissue-detection literature, a rising exposure series, and — in humans — almost no fertility
epidemiology at all. A bundled rating would average a measured-but-shrinking exposure against an
unmeasured-but-growing one and describe neither.

## The bundle is the chapter's central problem

v5 split B.6 out of B.2 on the ground that microplastics and PFAS differ from phthalates and BPA in
chemical properties, exposure pathway and literature base. That is true. It is also true of
microplastics relative to PFAS, and the reconnaissance measures how true.

| | **PFAS** | **Microplastics** |
|---|---|---|
| Human fertility epidemiology | Real and datable. Time-to-pregnancy and fecundability, n = 127; infertility/subfecundity, n = 237. Canonical works at 87–411 citations, from 2009 onward. | Effectively absent. The MP fecundability/infertility probe returns n = 257 whose **entire** most-cited head is marine ecotoxicology — oysters, copepods, rotifers. No human fertility-outcome cohort surfaced. |
| Tissue detection | Long-standing. Serum biomonitoring since the early 2000s; follicular fluid and seminal plasma, n = 141, with records back to 2005. | The genuinely new thing. Placenta 2020 (3,321 cites), blood 2022 (3,753), testis and semen 2023 (473), follicular fluid 2025 (116). |
| Individual exposure measure | Serum concentration, well validated, half-lives characterised. | No biomonitoring series. Intake is *modelled* from diet and air (n = 2,097), not measured in people over time. |
| Exposure trend | **Falling** for the legacy compounds the fertility literature actually measures. | **Rising**, tracking plastic production. |
| Prior systematic reviews on fertility | Yes — n = 33, including a 2016 review in *Critical Reviews in Toxicology* and a 2022 meta-analysis in *Environmental Research*. | None located on human fertility. The MP review literature (n = 371) is environmental and toxicological. |

The trend row is the one that changes the verdict, and it is not a matter of interpretation. NHANES
1999–2008 (Kato et al., *Environmental Science & Technology*) reports that **PFOS concentrations
showed a significant downward trend "because of discontinuing industrial production of PFOS"**, PFHxS
likewise downward, PFOA elevated in 1999–2000 and flat thereafter, and only PFNA trending upward.
v5's entry says the exposure "is structurally rising". That is right for microplastics and wrong for
the legacy PFAS that carries the human fertility evidence.

**Consequence, pre-committed rather than discovered:** every estimate is tagged with a
`CHEMICAL_FAMILY` of `PFAS_LEGACY`, `PFAS_REPLACEMENT`, or `PLASTIC_PARTICLE`; families are **never
pooled**; and the demographic-significance computation runs **once per family**, each against its own
exposure series. A single bundled B.6 effect size is not a quantity this chapter will produce. See
Call 1.

## Presence is exposure, not effect

The strongest single fact the reconnaissance produced concerns the study v5 leads with. B.6's
justification for existing is tissue-level detection, and the flagship detection study in the female
tract is Montano et al. (2025), *Ecotoxicology and Environmental Safety* — "First evidence of
microplastics in human ovarian follicular fluid". Its abstract reports microplastics in 14 of 18
women, a significant correlation with FSH, and then, in the authors' own words, that **no correlation
with anti-Müllerian hormone, fertilization outcomes, miscarriages, or live birth was observed.**

So the work cited to establish that microplastics threaten female fertility measured four fertility
endpoints and found nothing on any of them, in eighteen women recruited at an IVF centre. This is not
a criticism of the study, which is an exposure-assessment advance and says so. It is a statement about
what the hypothesis currently rests on: detecting a substance in a tissue establishes that the tissue
is exposed. It does not establish an effect, and the review's GRADE rating attaches to effects.

The chapter therefore separates a `DETECTION_TISSUE` stream from the causal stream at the point of
screening, and detection records — however novel, however well cited — earn **no** causal recall
credit. See Call 5.

## Phenomenon scope

**SDT: the only cell, and the whole of it.** Large-scale production of both families predates the
phenomenon. PFOA and PFOS manufacture dates from the late 1940s and 1950s; mass consumer plastics
from the same period. The exposure was therefore present, and rising, across the entire SDT window
including the 1965–1980 stretch in which the larger part of the OECD TFR decline occurred.

This is worth stating explicitly because **B.7's scope document (2026-08-12, its Call 1) names B.6 as
one of four hypotheses whose exposure post-dates most of its assigned phenomenon. For B.6 that is
incorrect, and the forward reference should be struck.** What post-dates the phenomenon is the
*measurement*, not the exposure: analytical chemistry capable of finding particles in follicular fluid
is five years old, and PFAS serum biomonitoring is twenty-five. The recency of the literature is a
fact about instruments. Reading it as recency of exposure would invert the chapter's timing argument,
and it is an easy mistake to make because every citation is new.

The corollary cuts against the hypothesis rather than for it. Because the exposure is old, B.6 does
not get B.7's excuse of a short denominator; it is exposed to the full-period test, and it has to
explain why fertility kept falling through the 2000s and 2010s in populations whose legacy-PFAS burden
was falling at the same time.

**FDT: no cell.** Production begins at the very end of the FDT window and at negligible per-capita
volume. Pre-1965 material is retained only as `PARAMETER_EXPOSURE` where it documents the production
or concentration series.

**PM: no cell.** The exposure did not exist.

## The nine boundary walls

**Wall 1 — B.6 vs B.2 (Endocrine Disruptors, `endocrine-disruptors-environmental-toxins`).** The
constitutive wall: B.6 exists only because this line was drawn in v5, so if it cannot be enforced the
split cannot be either.
- **Discriminator:** chemical family. Microplastics, nanoplastics and PFAS are B.6; phthalates,
  bisphenols, organochlorines, dioxins and industrial solvents are B.2.
- **The hard case is mixtures, and it is not rare: n = 583** records measure at least one family from
  each side together, under mixture, co-exposure or exposome designs. A mixture index spanning both
  sides is attributable to neither.
- **Rule:** a study reporting compound-specific estimates contributes its B.6-family estimates to this
  chapter and its B.2-family estimates to that one. A study reporting **only** a joint index takes
  `MIXTURE_UNSEPARABLE`, is retained, is cross-filed to both chapters, and is pooled in neither.
- A second hard case is physical rather than statistical: plastic particles carry and leach
  plasticisers, so "phthalate-contaminated microplastic" exposures are genuinely both families at
  once. These take `MIXTURE_UNSEPARABLE` on the same rule.
- **v5's own seminal list violates this wall.** Its fourth citation, traced in the retry pass, resolves
  to Shoaito et al. (2019) in *Environmental Health Perspectives* on **MEHP — a phthalate metabolite**
  — and cytotrophoblast differentiation. That is a B.2 paper offered as evidence for B.6. See Call 4.
- The sibling is much the larger literature: legacy EDCs paired with fertility returns n = 2,666
  against B.6's own human seam. B.6 is the smaller, newer half of the split.

**Wall 2 — B.6 vs the pregnancy-safety literature.** n = 1,148, the largest single adjacent body.
- **Discriminator:** the sample is conditioned on pregnancy and the outcome is a property of a birth
  that occurred — birth weight, gestational age, preterm birth, congenital anomaly, neurodevelopment.
  No fertility quantity is estimated. Route to `OFF_PREGNANCY_SAFETY` and exclude.
- **This wall is expensive here in a way it was not in B.7, and the cost should be recorded before it
  is paid.** The single best-identified study anywhere in B.6's space is Waterfield, Rogers, Grandjean,
  Auffhammer and Sunding (2020), *Environmental Health* — a difference-in-differences design exploiting
  the 2006 installation of a water filtration plant in Oakdale, Minnesota, which sharply cut PFAS
  exposure in one community relative to its neighbours. It is the only credible natural experiment the
  reconnaissance found. Its outcomes are birth weight and preterm birth. Under this wall it routes out.
  See Call 3.

**Wall 3 — B.6 vs B.5 (Fetal Loss, `fetal-loss-intrauterine-mortality`), stated reciprocally.** n = 148.
B.5's scope document (2026-08-11, its Wall 3) routes this boundary and B.6 adopts the rule verbatim, as
B.7 did, so no two chapters can claim the same studies.
- **Rule:** B.6 owns **variation in the determinant**; B.5 owns **the intrauterine-survival channel and
  its fertility consequence**. An exposure→miscarriage study with a fertility outcome is B.5's and
  cross-references B.6. Without one it is `PARAMETER_DETERMINANT_TO_LOSS`: retained, indexed, counted
  toward neither chapter's causal recall.

**Wall 4 — B.6 vs A.17 (ART Access, `art-access-fertility-recovery`).** n = 105 on the cycle-outcome
probe, n = 84 on the ART-derived exposure-outcome probe.
- Sharper here than in B.7, and structurally so: **follicular fluid is obtained at oocyte retrieval,
  so the female tissue-detection literature is by construction an IVF literature.** The Montano
  sample is 18 women at a Salerno IVF centre. The sampling frame is selected on subfecundity.
- **Discriminator:** an estimand concerning ART treatment success routes to `OFF_ART_A17`. Exposure
  measured in an ART population with a general-fertility estimand is admissible as
  `PARAMETER_HAZARD_CLINICAL` or `DETECTION_TISSUE` with the selection flagged. No ART-derived estimate
  is transported to a general population without an explicit adjustment argument recorded at extraction.

**Wall 5 — human versus non-human.** The single largest threat to a clean ranking.
- The MP corpus is 67,902 records of which roughly 28,000 are marine and aquatic. On **exactly the
  vocabulary this chapter needs** — fecundity, reproduction, sperm — the most-cited records are
  *Calanus*, *Tigriopus*, *Mytilus*, *Daphnia*, oysters and zebrafish. The MP fecundability probe's top
  eight are all non-human. The MP sperm probe's top eight are mice, earthworms and in-vitro systems,
  with a single human record.
- Non-human studies route to `OFF_ANIMAL` and are excluded. As in B.7, **the screen is told to check
  species on every record** rather than infer it from topic, because the topical vocabulary does not
  discriminate at all.

**Wall 6 — in vivo human versus in vitro.** n = 5,337.
- Granulosa-cell, trophoblast-cell and oocyte-maturation exposure experiments dominate the mechanism
  literature. Route to `MECHANISM_INVITRO`: retained in the mechanism stream, no causal recall credit.
- Stated separately from Wall 5 because an in-vitro study of *human* cells passes the species check and
  would otherwise be admitted as human evidence.

**Wall 7 — B.6 vs A.16 (Paternal Age and Sperm Quality) and the unattributed outcome trend.** n = 2,169
on the temporal-sperm-count-trend probe, a literature older and larger than B.6's own.
- A measured decline in semen quality over time, with **no exposure measured**, is not evidence for
  B.6, for B.2, or for A.16. It is a description of the phenomenon those hypotheses compete to explain.
  Route to `OUTCOME_TREND_UNATTRIBUTED`: retained as context for the demographic-significance section,
  no causal recall credit.
- Where aging is the exposure contrast, the record is A.16's.

**Wall 8 — the "fertility" homonym.** Cheap, and stated because it corrupts precisely the probes that
matter most.
- The aggregate-fertility probe (n = 173) returned, among its most-cited, reviews of microplastics in
  **soil** and of biochar improving **soil fertility**. The word "fertility" in an environmental corpus
  more often means soil than people.
- Route to `OFF_SOIL_FERTILITY`. Enforceable trivially at title, but the production query must not
  treat a "fertility" keyword hit as topical evidence.

**Wall 9 — general-population versus high-exposure populations.** n = 1,475 occupational and
contaminated-community records; Ronneby n = 79, Veneto n = 225, C8/Mid-Ohio Valley n = 34.
- These are **not** excluded: they carry the only substantial exogenous variation in exposure that
  exists, and Wall 9 is therefore a transport wall rather than a routing wall.
- **Rule:** admissible as `PRIMARY_HIGH_EXPOSURE` with serum levels recorded. Never pooled with
  general-population estimates without an explicit dose-response argument, since contaminated-community
  serum concentrations run one to two orders of magnitude above background and the hypothesis is about
  background exposure.
- Reconnaissance caution: the C8 reproductive cell (n = 34) is, on inspection, almost entirely
  pregnancy-outcome work that Wall 2 excludes. The high-exposure cohorts have been studied for cancer,
  thyroid, lipids, ulcerative colitis and birth outcomes far more than for fertility.

## What the title/abstract screen can and cannot enforce

| Wall / field | Enforceable at title/abstract? | Why |
|---|---|---|
| 1 (B.2), *which chemical family* | **Yes** | The compound is named, nearly always in the title. |
| 1 (B.2), *whether a mixture index is separable* | **No** | Whether compound-specific estimates are reported is a results fact. Abstracts report the index. |
| 2 (pregnancy safety) | **Yes** | Conditioning on pregnancy is named, almost always in the title. |
| 3 (B.5) | **Yes** | Whether a fertility outcome accompanies the loss outcome is visible; that is the whole test. |
| 4 (A.17) | **Yes** for the estimand; **partly** for the sampling frame | "IVF" in the setting is named; that a follicular-fluid sample *implies* an ART frame must be inferred, so the screen is told the implication explicitly. |
| 5 (species) | **Yes**, but only if asked | Named — but vocabulary overlap with the human literature is total, so species is checked on every record rather than inferred from topic. |
| 6 (in vitro) | **Yes** | Named. |
| 7 (outcome trend) | **Yes** | Whether an exposure is measured is visible. |
| 8 (soil) | **Yes** | Named. |
| 9 (high exposure) | **Yes** | The cohort or community is named. |
| `CHEMICAL_FAMILY` | **Yes** | The compound is named. |
| Estimand level (hazard vs quantum) | Partly | Time-to-pregnancy and completed-parity outcomes are distinguishable; an unqualified "fertility" outcome is not. |
| **`PARITY_HANDLING`** (the reverse-causation design) | **No** | Nulliparous restriction, parity stratification and first-pregnancy-only sampling are methods facts, reported inconsistently in abstracts. |
| `BLANK_CONTROL` (MP contamination control) | **No** | Procedural blanks are a methods fact and are almost never in an abstract. |

**Consequence, pre-committed rather than discovered:** the screen assigns a routing cell and a chemical
family with reasonable confidence, and does **not** assign parity handling, blank control, or mixture
separability. Every included empirical paper enters full text with `PARITY_HANDLING` unset. This is the
same admission D.3.b made about its Wall 1 and B.7 about its indication designs, and it is made here in
advance rather than after an audit discovers it.

## Estimand cells

| Cell | Exposure / variation | Outcome | Routing |
|---|---|---|---|
| `PRIMARY_EXPOSURE_TO_FERTILITY` | Measured MP or PFAS exposure | A fertility quantity: births, completed parity, TFR, time-to-pregnancy, fecundability | Primary synthesis — **the identification-bearing cell** |
| `PRIMARY_MALE_FECUNDITY` | Measured exposure | A measured male fertility outcome, not a semen parameter alone | Primary synthesis, male stratum |
| `PRIMARY_HIGH_EXPOSURE` | Contaminated-community or occupational exposure | A fertility quantity | Primary synthesis, transport-flagged (Wall 9) |
| `SEMEN_PARAMETER` | Measured exposure | Sperm count, concentration, motility, morphology | Support; an input to fertility, not a fertility quantity |
| `OVARIAN_PARAMETER` | Measured exposure | AMH, antral follicle count, ovarian reserve, cycle characteristics | Support, as above |
| `DETECTION_TISSUE` | — | Concentration of MP or PFAS measured in a reproductive tissue or fluid | Exposure-assessment stream; **no causal recall credit** — see "Presence is exposure, not effect" |
| `MECHANISM_INVITRO` | Exposure of human or animal cells | Cellular or molecular endpoint | Mechanism stream; no causal recall |
| `PARAMETER_EXPOSURE` | — | Population exposure levels, serum trends, intake estimates, production series | Parameter stream; feeds demographic significance; **not** in the recall denominator |
| `PARAMETER_PHARMACOKINETIC` | — | Half-life, elimination, transplacental and lactational transfer, determinants of serum level | Parameter stream; **load-bearing for the reverse-causation correction** |
| `PARAMETER_DETERMINANT_TO_LOSS` | Measured exposure | Fetal loss, no fertility outcome | Parameter; cross-filed to B.5 (Wall 3); neither chapter's recall |
| `MEASUREMENT_METHOD` | — | Detection methodology, blank control, spectroscopic identification, exposure misclassification | Methods stream; load-bearing for risk of bias |
| `MIXTURE_UNSEPARABLE` | Joint index spanning B.6 and B.2 families | Any | Retained, cross-filed to both, pooled in neither (Wall 1) |
| `OUTCOME_TREND_UNATTRIBUTED` | None measured | Temporal trend in semen quality or fertility | Context for demographic significance; no causal recall (Wall 7) |
| `OFF_PREGNANCY_SAFETY` | Measured exposure in pregnancy | Fetal, neonatal or child outcome | Excluded — Wall 2; the largest adjacent cell |
| `OFF_ART_A17` | Measured exposure in ART | Cycle treatment success | Route to A.17 |
| `OFF_FETAL_LOSS_B5` | Measured exposure | Fetal loss **with** a fertility consequence estimated | Route to B.5 |
| `OFF_LEGACY_EDC_B2` | Phthalate, bisphenol, organochlorine, solvent | Any | Route to B.2 |
| `OFF_ANIMAL` | Non-human exposure | Any | Excluded — Wall 5 |
| `OFF_SOIL_FERTILITY` | — | Soil or agronomic fertility | Excluded — Wall 8 |
| `OFF_ENVIRONMENTAL_FATE` | — | Occurrence, transport, degradation, remediation | Excluded; the largest cell in the corpus overall |
| `OFF_OUTCOME` | Measured exposure | A non-fertility, non-reproductive outcome (thyroid, lipids, cancer) | Excluded |
| `ROUTING_DEFERRED_TO_FULLTEXT` | Routing turns on mixture separability or parity handling | Fertility | Held; adjudicated at full text |
| `REVERSE` | Parity, pregnancy or lactation as a determinant of measured exposure | Exposure | **Context, and the chapter's central identification threat** |
| `OFF_OTHER` | Non-B.6 fertility determinant with no sibling home | Fertility | Route out; no sibling queue |
| `INSUFFICIENT_INFO` | Cannot be routed on the visible record | Unknown | Pairs only with `UNCERTAIN` |

`DETECTION_TISSUE`, `MECHANISM_INVITRO`, both `PARAMETER_*` cells, `MEASUREMENT_METHOD`,
`SEMEN_PARAMETER`, `OVARIAN_PARAMETER` and `OUTCOME_TREND_UNATTRIBUTED` carry verdict `RELEVANT` and are
separated downstream. None counts toward empirical recall.

## The identification cautions

**Reverse causation is mechanical, not merely plausible, and it is the estimand problem of this
chapter.** PFAS leave the body by three routes that are all reproductive: transplacental transfer,
lactation, and menstrual blood loss. Parity therefore *causes* lower serum PFAS. Any cross-sectional
or retrospective association between high serum PFAS and low parity, or between high serum PFAS and
long time-to-pregnancy among women who have been pregnant before, is generated in part or in whole by
elimination running backwards along the arrow the hypothesis wants to draw.

This is not a subtle confound and the literature knows it: the pharmacokinetic stream is large
(n = 3,115 on elimination and half-life; n = 194 on parity as a determinant of serum concentration;
n = 155 naming reverse causation or restricting to nulliparous women). The canonical sequence is
itself the story — Fei et al. (2009, *Human Reproduction*, 387 cites) reported subfecundity;
Whitworth et al. (2011, *Epidemiology*) stratified by parity; and Bach et al. (2015, *Environmental
Health*) is titled "Perfluoroalkyl acids and time to pregnancy **revisited**: an update from the Danish
National Birth Cohort". A chapter that pools across this sequence without recording the design
difference would average a finding with its own correction.

**Consequence:** every PFAS estimate records `PARITY_HANDLING` — nulliparous-restricted,
parity-stratified, first-pregnancy-only, or none — and estimates without it are **not pooled** with
estimates that have it. This is the axis D.3.b uses for adjusted-versus-unadjusted and B.7 for
indication design. See Call 2.

**Exposure timing is frequently posterior to the outcome.** Serum measured during or after pregnancy,
which is how most cohort samples are drawn, is measured after the conception whose hazard is being
explained, and after the elimination that pregnancy itself causes. Preconception measurement is the
design that identifies; it is rare.

**Selection into the tissue-detection literature is severe and structural.** Follicular fluid comes
from oocyte retrieval, testicular tissue from surgery or autopsy, placenta from delivery. The
populations are ART patients, surgical patients, decedents and delivered women — never a random sample
of the reproductive-age population. Detection prevalence from these sources cannot be read as
population exposure prevalence, and the demographic-significance computation must not do so.

**Microplastic measurement is contamination-prone in a direction that inflates.** Plastic labware,
airborne synthetic fibres and sample handling all deposit particles. A detection study without
procedural blanks reports an unknown mixture of biology and laboratory. `BLANK_CONTROL` is recorded on
every `DETECTION_TISSUE` record and drives its risk-of-bias rating.

**The two families' exposure series move in opposite directions, so the aggregate calculation must be
disaggregated.** Legacy PFOS and PFHxS fell after production was discontinued; PFOA has been flat since
2003; PFNA rose; plastic particle exposure rose throughout. A single "B.6 exposure is rising" premise
is false for the half of the hypothesis that carries the fertility evidence.

**Designs that can survive all of this** have exposure variation not generated by the person's own
reproductive history: contaminated water supplies and their remediation, industrial point sources,
occupational cohorts, regulatory phase-outs, and preconception-measured prospective cohorts restricted
to nulliparous women. These are the primary targets of the search. The reconnaissance located
**exactly one** natural experiment on a reproductive endpoint, and Wall 2 routes it out.

## When to adjudicate mechanisms

The title/abstract screen assigns the routing cell and the chemical family only. For every included
empirical paper, full-text extraction records:

- `CHEMICAL_FAMILY` and `COMPOUND` — `PFAS_LEGACY` / `PFAS_REPLACEMENT` / `PLASTIC_PARTICLE`, and the
  specific analyte, since half-lives and trends differ sharply within family;
- `EXPOSURE_MEASURE` — serum, plasma, urine, tissue concentration, modelled intake, or residence
  proxy; and the timing relative to the outcome, with preconception flagged;
- `PARITY_HANDLING` — nulliparous-restricted, parity-stratified, first-pregnancy-only, or none. The
  field that decides whether a PFAS estimate speaks to B.6 at all;
- `BLANK_CONTROL` — for particle detection, whether procedural blanks and contamination controls were
  run and reported;
- `ESTIMAND_LEVEL` — `HAZARD_DECREMENT` or `TEMPO_ADJUSTED_QUANTUM`, the field that decides poolability;
- `SAMPLING_FRAME` — general population, ART clinic, occupational, contaminated community, surgical,
  autopsy;
- `SEX` — recorded on every row; the mechanisms and the evidence bases differ by sex;
- `MIXTURE_SEPARABLE` — whether compound-specific estimates are recoverable (Wall 1);
- `CONFOUNDERS_ADJUSTED` — parity and breastfeeding history are mandatory for PFAS; age, BMI,
  socioeconomic position and smoking recorded when present.

Drafting may report only what these fields support. A study finding that women with higher serum PFAS
took longer to conceive documents an association that elimination kinetics alone can produce; it must
not be described as evidence that PFAS reduces fecundity, absent a `PARITY_HANDLING` that identifies it.

## Eligibility rules

- Include empirical studies where the estimate bears on **measured MP or PFAS exposure → a fertility
  quantity or a directly reproductive parameter**, in humans, with the chemical family recorded.
- Studies conditioned on pregnancy whose outcome is a property of the birth are `OFF_PREGNANCY_SAFETY`
  and excluded, however well identified (Wall 2, and see Call 3).
- Tissue-detection studies with no outcome are `DETECTION_TISSUE`: retained, indexed, excluded from the
  causal recall denominator.
- Non-human studies are excluded (Wall 5), and species is checked on every record rather than inferred.
- Human-cell in-vitro studies are `MECHANISM_INVITRO`: retained, no causal recall (Wall 6).
- Legacy EDC studies are `OFF_LEGACY_EDC_B2`; joint-family mixture indices are `MIXTURE_UNSEPARABLE`,
  cross-filed and never pooled (Wall 1).
- High-exposure cohort studies are admissible as `PRIMARY_HIGH_EXPOSURE`, transport-flagged (Wall 9).
- Outcome trends with no exposure measured are `OUTCOME_TREND_UNATTRIBUTED` (Wall 7).
- Phenomenon is **SDT**, whole period. Pre-1965 material is retained only as `PARAMETER_EXPOSURE`.
- Where the abstract cannot support the routing call, defer rather than guess.

## Expected shape of the evidence (a caution, not a result)

1. **The demographic seam is close to empty, and thinner than B.7's.** Both families paired with any
   aggregate fertility term return n = 48, and inspection of the head shows reviews of reproductive
   toxicology, mouse experiments, and a cohort profile — not one population-level estimate. B.7's
   equivalent probe returned 48 as well, but B.7 at least had a measured national exposure series to
   multiply. **If the search confirms this, the finding is that nobody has estimated the quantity the
   hypothesis asserts**, and the chapter reports that as its primary result rather than assembling a
   proxy.
2. **There is no quasi-experimental estimate of either exposure on a fertility quantity.** The
   difference-in-differences and instrumental-variable probe (n = 70) returns one relevant record — the
   Minnesota water-filtration study — whose outcomes are birth weight and preterm birth. Every other
   human fertility estimate in the corpus is serum-concentration association. **The GRADE ceiling is
   therefore set before the search runs, and it is Low at best**, on grounds of design rather than
   volume.
3. **The two halves must be rated separately or the rating is meaningless.** See the bundle table.
4. **The microplastics fertility cell may be empty in humans.** If it is, the honest report is that the
   tissue-detection literature has established exposure and not yet tested effect — which is what its
   own flagship paper says.
5. **The animal and environmental literatures own the vocabulary, more completely than in any chapter
   run so far.** 67,902 MP records and 81,123 PFAS records, against a human fertility seam in the low
   hundreds. This is a three-orders-of-magnitude precision problem and Wall 5 must be enforced at
   screen, not at extraction.
6. **The parameter stream is strong where the causal stream is weak** — NHANES biomonitoring, half-life
   studies, production series — the same inversion B.5 and B.7 found. The chapter must not let the
   precision of the exposure series transfer to the effect it multiplies.
7. **Channel 1 exists for PFAS and not for microplastics.** Prior systematic reviews of PFAS and human
   fertility number 33, including a meta-analysis of female fertility; no equivalent for microplastics
   was located. Recall(A) will be computable for one half of the chapter and not the other.
8. **A pooled meta-analytic estimate is unlikely to be defensible across families, and may not be within
   them.** If the primary cells yield fewer than three estimates sharing a chemical family, an estimand
   level, a sex stratum and a parity-handling status, PROTOCOL §5.9 directs narrative synthesis, and the
   chapter reports a decomposition with an explicit uncertainty range rather than a forest plot built
   from incommensurable quantities.

## Cold-start channels and leakage wall

1. Direct empirical papers estimating MP or PFAS exposure → a fertility quantity, in either sex, seed
   the empirical Tier-A candidate set.
2. Tissue-detection papers seed the exposure-assessment stream and earn no credit toward the primary
   cell.
3. Pharmacokinetic and elimination papers seed the parameter stream — weighted more heavily here than
   in prior chapters, because they carry the reverse-causation correction; biomonitoring and production
   papers seed the exposure-series stream; detection-methodology papers seed the methods stream.
4. References and citations of the independent seeds create the orthogonal Tier-B frame. Forward
   citation is applied uniformly across seed types, including routing decoys, with `seed_ids`
   provenance retained so Recall(B) can be computed with and without decoy-seeded material.
5. Production-query terms are not mined from a paper that is then used to evaluate the query; learned
   extensions are fold-local once the gold frame exists.

## Pre-query anchor audit

The verified candidate anchor set is stored in `microplastics-pfas-reproductive-cold-start-anchors.json`.
Five gates apply, all mandatory.

- **Existence gate** (OAS, 2026-07-08): a live DOI or a Crossref/publisher record confirming the title
  exists. No anchor is asserted from memory, and no author list is either. This pass ran the gate on
  28 titles and **9 did not resolve**, including three of v5's four seminal citations.
- **Version-of-record gate** (D.1.b, 2026-08-07): an anchor resolving to a working paper, preprint,
  reprint, or review *of* the work fails, even at title Jaccard 1.0. **Live example in this corpus:**
  the follicular-fluid study exists both as a 2024 medRxiv preprint and a 2025 journal article under a
  title differing only in capitalisation.
- **Book-canon gate** (D.2.d, 2026-08-08): monographs resolve to their own reviews at perfect title
  confidence. Live here — Swan's *Count Down* is a trade monograph adjacent to this literature.
- **Shadow-record gate** (B.7, 2026-08-12): named qualifiers only, never bare suffix-containment.
  Confirmed live in this corpus on three separate anchors — "Faculty Opinions recommendation of X"
  twice, "Letter to the editor, X", and "Re: X" in *The Journal of Urology*.
- **Duplicate-record gate (new, B.6, 2026-08-14).** The Minderoo-Monaco Commission resolves to **two
  distinct OpenAlex records with different DOIs** (`10.5334/aogh.4056`, 447 citations, and
  `10.5334/aogh.4083`, 41 citations) plus a separate erratum record. DOI-level deduplication passes
  both and would double-count the anchor and split its citation weight. The gate clusters on normalised
  title + year + venue, keeps the higher-cited record as canonical, and **logs** the demotion rather
  than dropping it silently. Commission reports, consensus statements and multi-part reviews are the
  record types where this occurs.

The set deliberately contains primary, detection, mechanism, parameter, pharmacokinetic, measurement
and off-cell decoy anchors (a B.2 phthalate record for Wall 1, a pregnancy-safety record for Wall 2, an
ART record for Wall 4, a marine ecotoxicology record for Wall 5, a soil-fertility record for Wall 8, and
a C8 cohort record for Wall 9), so the search is tested on routing as well as on topical retrieval.

## Scope calls for the PI

**Call 1 — B.6 bundles two hypotheses with opposite evidence profiles and opposite exposure trends.
Recommended: one chapter, two verdicts.** PFAS has human fertility epidemiology and a falling legacy
exposure series; microplastics has tissue detection, a rising exposure series, and almost no human
fertility epidemiology. Three options:
- *(a) Recommended.* Keep one chapter and one ticket, but issue **per-family GRADE ratings and
  per-family demographic-significance verdicts**, with no bundled B.6 effect size at any point.
  Rationale: it costs nothing procedurally, and it is the only way either verdict means anything.
- *(b)* Split into B.6.a (PFAS) and B.6.b (microplastics and nanoplastics) in v6. Cleaner in the long
  run and probably where this ends up, but too large a change to make from inside one chapter; flagged
  for TICK-001.
- *(c)* Rate the bundle. Rejected: it would average a measured, shrinking exposure against an
  unmeasured, growing one.

**Call 2 — the reverse-causation problem is mechanical, and the estimate base is largely contaminated
by it. Recommended: a two-track synthesis on parity handling.** PFAS elimination through pregnancy,
lactation and menstruation makes parity a cause of exposure. Recommendation: the primary synthesis is
restricted to `PARITY_HANDLING` ∈ {nulliparous-restricted, parity-stratified, first-pregnancy-only},
with the unrestricted set reported alongside as a sensitivity and the gap between them reported as a
quantity of interest. This is D.3.b's adjusted-versus-unadjusted design on a different axis, and the
comparison is arguably the most informative thing this chapter can produce.

**Call 3 — Wall 2 excludes the only credible natural experiment in the corpus. Recommended: uphold the
exclusion and report the loss.** Waterfield et al. (2020) is a difference-in-differences design on a
water-filtration intervention in Minnesota; its outcomes are birth weight and preterm birth, so it
estimates B.6's exposure on B.2-style birth outcomes and not on any fertility quantity. Recommendation:
route it `OFF_PREGNANCY_SAFETY` as the wall requires, and state in the chapter that the best-identified
study in the space does not estimate the review's outcome. Admitting it would import an estimand the
demographic-significance calculation cannot use.

**Call 4 — three of v5's four seminal citations for B.6 do not resolve as written. For TICK-001.**
All four were probed on multiple wordings with zero failed requests:
- *"Zhao et al. Fertility & Sterility (2025)"*, cited for follicular fluid, is a conflation of two
  different works. **Zhao et al. (2023) is real** — "Detection and characterization of microplastics in
  the human testis and semen", *Science of the Total Environment*, 473 citations — but it is 2023, in a
  different journal, and concerns **testis and semen, not follicular fluid**. The follicular-fluid study
  is **Montano et al. (2025)**, *Ecotoxicology and Environmental Safety*.
- *"Lancet Commission on Reproductive Health (2025)"* **does not exist.** What is almost certainly meant
  is **The Minderoo-Monaco Commission on Plastics and Human Health**, Landrigan et al., *Annals of Global
  Health*, **2023**, 447 citations — a different commission, a different publisher, and two years earlier.
- *"Yang et al. Scientific Reports (2025)"* **did not resolve on any of four wordings** and cannot be
  cited until someone produces the DOI.
- *"Shoaito et al. Environment International (2023)"* resolves to **Shoaito et al. (2019),
  *Environmental Health Perspectives***, on **MEHP, a phthalate metabolite**, and cytotrophoblast
  differentiation. Wrong year, wrong journal, and on the **B.2 side of the wall that defines B.6**.

  None of these blocks this run; the anchors below are sourced from what resolves. But a hypothesis
  entry whose seminal list is three-quarters wrong is a warning about the other v5 entries added in the
  same pass, and TICK-001 should re-verify B.7's and C.2.h's lists on the same gates.

**Call 5 — what a detection literature can and cannot support. Recommended: state the premise as an
exposure-assessment advance, and rate effects.** v5 justifies splitting B.6 from B.2 on the ground that
the 2020s tissue-detection studies are a step change. They are — as exposure assessment. But the
flagship female-tract study reports no association with AMH, fertilization outcomes, miscarriage or live
birth, in 18 IVF patients. Recommendation: the chapter states plainly that presence in tissue
establishes exposure and not effect, keeps `DETECTION_TISSUE` out of the causal recall denominator, and
attaches GRADE to effect estimates only. The alternative — treating detection as partial evidence of
effect — would give B.6 a credibility rating built on measurements that contain no outcome.

## Next step

A3 — source and quintuple-gate the cold-start anchors
(`source/build/goldset/134_b6_cold_start_anchors.py`). Script numbering starts at **132** (the
reconnaissance probe) and 133 (the anchor retry); 134 is next. **Numbering caution:** 88 is the highest
on `main`, but the unmerged branches collide badly — D.1.b holds 95–102, D.1.a 95–115, D.2.d 103–108,
B.5 115–122 and B.7 123–131. This run starts above every number in use on **any** branch, local or
remote, rather than above `main`; note that D.1.a's 115 exists only on an unpushed local branch and is
invisible to a scan of `origin`. The collision is flagged in TICK-068.
