# Search scope — population age structure and demographic momentum

**Hypothesis:** A.9 (HYPOTHESES-v5.md)
**Hypothesis slug:** `population-age-structure-momentum`
**Target phenomena:** FDT, SDT (registry §A.9; PM is **not** listed — see "Phenomena" below).
**Status:** DRAFT (Shravan, 2026-09-20) — walls, outcome convention, and estimand cells proposed,
**not yet frozen.** Freeze requires (a) the frame-probe run and registered-construct completeness test
the ticket demands, (b) a second read on Wall 1 (A.9 vs A.11 tempo), and (c) a PI ruling on how A.9's
non-effect estimand is rated and reported (escalated below; it is the same review-wide accounting item
TICK-080 §5–6 and TICK-054 Wall 2 already raised). Gold anchors not yet sourced.

## What A.9 is — the accounting bucket, not a behavioural cause

A.9 is unlike every treatment-effect hypothesis piloted so far. It does not claim that anyone *chose*
to have fewer or more children. It claims that a headline fertility number can move — up or down —
**with no change whatsoever in the childbearing behaviour of any woman at any age**, purely because the
age composition of the population changed. The mechanism is arithmetic: a birth rate is a ratio of
births to people (or person-years), and both the numerator's generating population (women in the
childbearing ages) and the denominator's composition shift over time independently of age-specific
rates.

Two distinct constructs travel under the A.9 name, and the search must hold them apart because they
attach to different outcomes and different literatures:

- **Age-composition (structure) effects** on *period* measures. Holding every age-specific fertility
  rate fixed, a population with a larger share of women in the peak childbearing ages (roughly 20–34)
  produces a higher crude birth rate and more births. This is the object of the standardization /
  decomposition tradition (Kitagawa 1955; Das Gupta 1993; Cho–Retherford; Preston–Heuveline–Guillot
  ch. 2–3).
- **Demographic momentum** (Keyfitz 1971; Espenshade et al. 2011; Bongaarts & Bulatao 1999; Schoen &
  Kim). Even after age-specific rates fall to exact replacement (NRR → 1), a population with a young
  age structure keeps *growing* — and its annual births stay elevated — for roughly 50–70 years,
  because the large young cohorts have yet to move through the reproductive ages. The "momentum factor"
  quantifies the eventual population size relative to its size at the moment rates hit replacement. In
  the SDT the sign flips: an *old* age structure carries **negative** momentum, suppressing births and
  population even if rates recover.

Both are the *same* underlying fact — age structure moves headline aggregates on its own — measured on
different outcomes and over different horizons.

## The outcome variable is not the period TFR

This is the load-bearing conceptual correction for A.9, and it is the analogue of the sex-ratio scope's
"the treatment is not the SRB." Three quantities travel under "fertility," and A.9 acts on them
completely differently — one by construction, one not at all, one not at all:

- **Crude birth rate (CBR) and the absolute number of births.** *Composition-laden by construction.*
  CBR = births / total population; it rises and falls with the share of the population that is women of
  childbearing age. This is where the A.9 effect **is real and can be large.** The number of births —
  the input to population growth — is likewise composition-laden.
- **Period total fertility rate (period TFR).** *Composition-free by construction.* Period TFR is the
  sum of single-year age-specific fertility rates for a synthetic cohort; it already conditions on age
  and is therefore, by its own definition, **purged of age composition.** Age structure cannot move a
  correctly computed period TFR. **The v5 claim text — "drive crude birth rates and period TFR
  independent of any change in age-specific fertility" — is imprecise on the "period TFR" clause and
  should be corrected**: the mechanical composition effect lands on the CBR and on counts, not on the
  TFR. (What *does* distort period TFR without a quantum change is **tempo** — a timing shift in
  age-specific rates — which is A.11's, not A.9's. This is exactly Wall 1.) *Recommended master-list
  edit flagged for TICK-001; not made here because HYPOTHESES-v5.md is under PI review.*
- **Completed cohort fertility (CCF, children ever born).** *Composition-irrelevant by construction.*
  A real cohort's completed fertility is a property of that cohort's own rates; age structure is not an
  input. A.9's effect on CCF is **zero by construction.**

Everything downstream — the estimand, the sign convention, the demographic-significance verdict, and
the GRADE flag — follows from which of these three outcomes a paper puts on the left-hand side. **A
paper whose fertility outcome is a period TFR or a cohort CCF, attributing movement in it to "age
structure," has almost certainly mislabeled a tempo effect, a quantum effect, or a measurement error,
and must be read at full text before it is admitted.**

## The standing prediction to test (from the registry note and TICK-080)

The v5 `notes` field states the demographic-significance conclusion in advance: *"Largely
accounting/measurement; matters for interpreting CBR and short-run TFR but not for completed cohort
fertility."* Recorded here as a prediction to test in §7 of the chapter, not an assumption to inherit.
TICK-080 §5–6 sharpens why this hypothesis is different in kind and pre-registers two problems the
chapter cannot dodge:

1. **A.9 is a non-effect estimand.** Its evidence is decomposition and projection arithmetic, not
   identified causal designs. GRADE's bands (§4.1) are a ladder of identification strategies; a clean
   Das Gupta decomposition is not "very low: correlational only," it is *a different question answered
   exactly.* A.9 should be rated **NOT RATEABLE — non-effect estimand** (TICK-080 §5), with a mandatory
   sentence beside the cell, rather than forced onto the effect-estimate ladder.
2. **The demographic-significance share is near-definitional and outcome-dependent.** §4.2's
   decomposition-share route asks whether the exposure explains ≥ 10% of the observed change. For A.9
   on the CBR/births outcome the composition share **is** the accounting share by construction — of
   course it clears 10%, that is what a decomposition *is* — so `significant` prints while meaning far
   less than the same word means in a behavioural chapter. On the period-TFR and CCF outcomes the share
   is **zero** by construction. The verdict must therefore be reported **per outcome**, with the
   construction stated, or it is tautological in one cell and vacuous in the other two.

The honest expected verdict, then, is not one label but three: **large-to-dominant for CBR / births /
short-run population growth** (this is a genuine and quantitatively major fact — momentum drives a
large share of 21st-century global population growth); **zero by construction for period TFR**; **zero
by construction for completed cohort fertility.** The chapter's value is making that split legible and
supplying the decomposition magnitudes for the first cell, not adjudicating a contested effect.

## Boundary walls (the load-bearing routing rules)

**Wall 1 — A.9 vs A.11 (`tempo-effects-birth-postponement`): composition vs timing. The sharpest
wall.** Both are "the headline number moved without a real change in family size," which is why they
are constantly conflated, but they are mechanically disjoint:

- **A.11 (tempo)** distorts the **period TFR** through a shift in the *timing* of age-specific rates
  (postponement thins the period cross-section). It operates *inside* the age-specific rate schedule.
- **A.9 (composition/momentum)** distorts the **CBR and counts** through the *weights* on an unchanged
  rate schedule. It operates on the age *distribution of the population*, leaving rates untouched.
- **Discriminator (operational):** does the paper's mechanism run through a change in the *timing/level
  of age-specific rates* (A.11) or through a change in the *population age distribution holding rates
  fixed* (A.9)? A Bongaarts–Feeney tempo adjustment is A.11's; a Das Gupta / Kitagawa rate-vs-composition
  decomposition of the CBR is A.9's.
- **A.11 is drafted, so this wall is inherited, not litigated** — but a decomposition paper that
  partitions CBR change into (rate, composition) *and* further splits the rate part into (tempo,
  quantum) straddles both chapters at the level of the *component*, never the study. The composition
  component is A.9's; the tempo component is A.11's.

**Wall 2 — A.9 as the shared accounting residual (the non-additivity problem).** A.9 is the bucket
that every other proximate cause's *aggregate-count* claim must be netted against. The sex-ratio scope
already writes this rule from the other side: A.10's Wall 4 routes any aggregate-birth or CBR outcome
"with no composition adjustment" to `MECHANICAL_COMPOSITION → A.9`. The same is true of A.1, A.7, A.8,
A.10 and any chapter that reports a births/CBR/growth outcome. **Consequence for A.9's own verdict:**
A.9's demographic significance on the CBR/births outcome is **not additive** with the other chapters'
contributions — it is the mechanical component *already embedded in* their aggregate numbers, not a
separate independent push. A review that sums per-hypothesis CBR contributions and then adds A.9 double-
counts. This needs a review-wide accounting rule; it is the same escalation A.10 (Wall 2/Wall 5) and
TICK-080 raise, and A.9 is the natural place to *land* that rule because A.9 *is* the accounting
component. **Escalate to Anup, folded into the existing non-additive-proximate-causes question:** does
A.9 own and define the mechanical-composition component that the other chapters then report *net of*,
and is A.9's CBR verdict stated as "the mechanical share of observed CBR change" rather than as an
independent contribution? Blocks the freeze of this scope; does not block anchor sourcing.

**Wall 3 — A.9 vs population growth/size as the outcome (the "not-fertility" wall).** The demographic-
momentum literature's dominant outcome is **future population size or the growth rate**, not fertility.
Keyfitz's momentum factor is a ratio of ultimate to current population; the Bongaarts–Bulatao and Lutz
projections are about population trajectories. **A paper whose left-hand side is population size or
growth, with no fertility rate or birth-count estimand, is `OFF_OUTCOME`** — context and theory for the
mechanism, but not an effect on fertility, which is what this review measures. This will be a large
cell, exactly as `OFF_OUTCOME` (sex-ratio → savings/crime) was for A.10. Predict it now so it is not
misread as a search failure. The admissible A.9 core is the subset that decomposes a **birth rate or a
birth count** into rate and composition components.

**Wall 4 — A.9 vs A.1 (`child-mortality-decline-replacement`): the determinant of momentum.** Falling
mortality is *what builds* the young, momentum-laden age structure (and it widens the gross-vs-net
reproduction gap). But *why the age structure is young* is A.1's / mortality's question; A.9 takes the
age structure as given and asks what it mechanically does to the CBR/births. A paper estimating
mortality decline → age structure, or mortality decline → the gross/net reproduction gap, with no
composition-to-birth-rate decomposition, is a **determinant** of A.9's exposure: `EXPOSURE_DETERMINANT`,
context only. (The gross-vs-net reproduction-rate gap itself sits on the A.1/A.9 seam and is extracted
as a component, flagged for both.)

## Outcome and magnitude convention (pre-registered)

A.9 has no "sign fixed by the hypothesis" the way a treatment does; its "effect" is a **decomposition
share or a momentum factor**, and it is meaningless without the outcome and the method attached. The
conventions:

1. **Outcome, always recorded and never pooled across.** Every extracted quantity carries its outcome:
   `CBR`, `BIRTHS_COUNT`, `POP_GROWTH`/`POP_SIZE` (→ Wall 3, off-cell), `PERIOD_TFR` (→ should be ~0;
   if non-zero, a red flag to read at full text), or `CCF` (→ 0 by construction). **CBR/BIRTHS effects
   are never pooled with growth/size quantities**, which are off-cell anyway.
2. **The quantity is a share or a factor, oriented consistently.** For decomposition studies, extract
   the **share of the observed change in the outcome attributable to the age-composition (structure)
   component**, with the sign oriented so that a positive share means composition pushed the outcome in
   the *same* direction as the observed net change. Record the counterpart rate-component share; the two
   should sum to the total (report the interaction/residual term where the method produces one). For
   momentum studies, extract the **momentum factor** (ultimate ÷ current population, or the equivalent
   births ratio) and its sign (young structure > 1, aged structure < 1).
3. **Method and horizon are load-bearing metadata.** Record the decomposition method (Kitagawa, Das
   Gupta, Cho–Retherford, Bongaarts–Feeney-hybrid, Lee–Carter-adjacent, direct standardization), the
   base and comparison periods, the geographic unit, and — for momentum — the horizon (stable-population
   asymptotic vs finite-horizon projection) and whether mortality is held fixed.
4. **No causal language for a decomposition.** A composition share is an accounting attribution, not a
   causal effect; the chapter reports it as such. This is the whole point of the non-effect-estimand
   flag (§ GRADE, below).

## Estimand cells

| Cell | Variation / object | Outcome | Routing |
|---|---|---|---|
| `PRIMARY_COMPOSITION_CBR` | Rate-vs-composition decomposition of a crude birth rate (or general fertility rate) | Share of CBR/GFR change from age composition, rates held fixed | Primary synthesis |
| `PRIMARY_COMPOSITION_BIRTHS` | Same decomposition applied to the birth count | Share of birth-count change from composition | Primary synthesis |
| `PRIMARY_MOMENTUM` | Demographic-momentum computation (Keyfitz factor, Espenshade decomposition, stable-population momentum) with a **births/rate** interpretation | Momentum factor / momentum share of births | Primary — the value-added cell for the trajectory question |
| `BRIDGE_TEMPO_QUANTUM_SPLIT` | Decomposition that isolates composition **and** a tempo/quantum split of the rate part | Composition component (A.9) + tempo component (A.11) | Component-level: composition to A.9, tempo to A.11 |
| `EXPOSURE_DETERMINANT` | Mortality decline / migration / past fertility → the age structure or the gross–net gap, **no composition-to-birth-rate step** | No fertility-rate decomposition | Context; the mortality part cross-refs A.1 |
| `OFF_OUTCOME_POP` | Momentum/age structure → **population size or growth rate** | No fertility rate/count decomposition | Off-cell (Wall 3); theory/context |
| `OFF_TEMPO_A11` | Timing shift in age-specific rates distorting period TFR | Period TFR | Route to A.11 |
| `OFF_PERIOD_TFR_MISLABELLED` | Claims age structure moves a **period TFR** | Period TFR | Read at full text; almost always tempo/quantum/measurement, route accordingly |
| `MOMENTUM_THEORY` | Stable-population theory, formal momentum derivations, projection methodology | No empirical decomposition estimate | Theory stream |
| `OFF_OTHER` | Non-A.9 fertility determinant with no sibling home | Fertility | Route out |
| `REVERSE` | Fertility change → age structure (the obvious accounting direction) | Age-structure outcome | Context, not the object sought |
| `INSUFFICIENT_INFO` | Cannot be routed on the visible record | Unknown | Pairs only with `UNCERTAIN` |

`OFF_OUTCOME_POP` is expected to be the **largest** cell by a wide margin: the momentum literature is
overwhelmingly about population size and growth, not about a birth rate. That is a fact about the field
and belongs in the chapter, not a search failure.

## Eligibility rules

- Include an empirical/measurement study only when it **decomposes a birth rate or a birth count into a
  composition (age-structure) component and a rate component**, or computes a **demographic-momentum
  quantity with a births/rate interpretation.** Population-size and growth-rate studies seed context and
  theory; they do not enter the empirical decomposition recall denominator (Wall 3).
- The outcome must be a **CBR, GFR, or birth count** for the composition cells. A period-TFR or CCF
  outcome attributed to age structure is a full-text-only red flag (§ "outcome is not the period TFR").
- **Every extracted quantity carries:** the outcome type, the decomposition method, the base/comparison
  periods, the geographic unit, whether mortality is held fixed, and (for momentum) the horizon and
  whether the factor is asymptotic or finite-horizon. Without these it cannot be oriented or pooled.
- Formal stable-population theory and projection methodology seed the **theory** stream and do **not**
  count toward empirical recall.
- Both registered phenomena (FDT, SDT) are in scope; **record the period and setting on every quantity**,
  because the demographic-significance verdict is made per phenomenon and the two eras carry opposite-
  signed momentum (young/positive in the FDT, aged/negative in the SDT).

## Phenomena

Registry §A.9 lists **FDT and SDT**, not PM, so stage 10 assesses two phenomena. The exclusion of PM is
defensible: the pre-modern era's near-stationary, high-mortality age structures produce little of the
transitional composition swing that makes A.9 bite, and the pre-modern gross-vs-net reproduction gap is
better filed under mortality (A.1) than under composition. **Do not re-add PM without a PI ruling**; if
a decomposition of a pre-modern CBR series surfaces, hold it and flag it rather than silently widening
scope. The FDT cell is where positive momentum and a youthful structure inflated CBRs even as rates
began to fall (part of why the CBR lagged the rate decline); the SDT cell is where negative momentum
from population aging now suppresses births and growth at constant or recovering rates.

## GRADE and demographic-significance flags (tie-in to TICK-080)

A.9 is the concrete case that motivated two of TICK-080's proposed protocol amendments, so this scope
adopts them provisionally and the chapter must not be finalized until TICK-080 rules:

- **GRADE:** rate A.9 **NOT RATEABLE — non-effect estimand** (TICK-080 §5), not on the identification
  ladder. A decomposition's credibility is about data quality and method validity, not about an
  identification strategy for a counterfactual that does not exist.
- **Demographic significance:** report **per outcome**, each with its construction stated — CBR/births
  (near-definitional large share; report the *magnitude* of the composition component, which is the
  informative number, not the pass/fail), period TFR (**0 by construction**), CCF (**0 by
  construction**). Do not print a single `significant`/`not significant` label for the hypothesis as a
  whole; it is a category error here (TICK-080 §6).

## Cold-start channels and leakage wall

1. Prior demographic-decomposition reviews, formal-demography textbook treatments
   (Preston–Heuveline–Guillot; Keyfitz–Caswell), and any systematic compilations of CBR-decomposition
   estimates → measurement anchors by external authority. *(Leakage wall: a source's method text may
   feed query terms and its worked decompositions may feed anchors, but never the same study to both.)*
2. Top-down canon enumeration — stable-population theory, momentum derivations, standardization/
   decomposition methodology — seeds the theory set and classic worked examples; does not count toward
   empirical recall.
3. Citation snowball from the channel-1 and channel-2 seeds → the orthogonal Tier-B frame.
4. Broad single-query search plus a structured screen, **only if** the gold is still under the
   cross-validation floor (≥ 30 empirical anchors — likely binding here, since the empirical
   *decomposition* literature on birth rates may be thin once population-size papers are excluded).
   Tier B is never drawn from this channel.
5. Production-query terms are mined fold-locally once the gold frame exists; never mined from a paper and
   then evaluated on it.

## Pre-query anchor audit (not yet built)

Verified anchors will be stored in `population-age-structure-momentum-cold-start-anchors.json`. Every
anchor clears the **mandatory existence-verification gate** (a live DOI or a Crossref/publisher record)
before it enters any recall denominator — the standing rule from the 2026-07-08 OAS run that found ~40%
of the frozen Tier B was fabricated. The seminal names in the v5 entry (Keyfitz 1971; Bongaarts &
Bulatao 1999; Lutz et al. 2003) are **candidates to verify, not anchors** — and Keyfitz 1971 in
particular is the kind of famous, single-author, half-century-old citation an LLM reproduces fluently
from memory in the exact register of a real reference, which is precisely the failure the gate exists to
catch. Because `OFF_OUTCOME_POP` dominates the field, the anchor set must deliberately carry **off-cell
decoys** — momentum→population-size, a Bongaarts–Feeney tempo paper (A.11), and a mortality→age-
structure paper (A.1) — so the query is tested on routing, not just retrieval. **Routing, not retrieval,
is this chapter's binding constraint**, exactly as it was for A.10.

## Open items before freeze (from TICK-089)

1. **Run the frame probe.** *(Done 2026-09-20 — `population-age-structure-momentum-frame-probe.md`.)*
   A.9 anchored **momentum core ≈ 200** (`population momentum`/`demographic momentum`), working frame
   **≈ 500** (adding `population age structure`). The WIDE frame (~3,600) is **homonym-inflated** —
   almost entirely the generic pair `age structure`/`age composition` (3,213 alone; 32,363 unrestricted,
   an ecology/population-genetics term), which leaks 106 ecology records into the frame even with the
   fertility gate. **Do not use WIDE as the frame.** Anchor the production cause axis on momentum-specific
   vocabulary and admit generic age-structure terms only under a decomposition/CBR gate (see the probe
   doc's "Implication for the production query"). Control (C.3.e) = 85, matching 304's run.
2. **Registered-construct completeness test.** A.6 and A.3 each led on raw count and were passed over
   because the selecting frame omitted the registry's own construct and undercounted the literature
   (`404`, TICK-087/088). Confirm the A.9 frame carries the registry's construct vocabulary —
   *demographic momentum*, *population momentum*, *age structure / age composition*, *tempo–quantum /
   rate–composition decomposition*, *standardization* — before its count is trusted.
3. **Homonym residue check.** "Momentum" is a physics and finance word; "age structure" and "population
   structure" are population-genetics and ecology words. Run the homonym-residue check *inside* the
   fertility-restricted frame, as C.3.f did, and record the residue fraction wherever a count is quoted.
4. **Wall 1 second read** (A.9 vs A.11 tempo) and the **Wall 2 escalation** (the non-additive
   accounting rule / whether A.9 defines the mechanical-composition component the other chapters report
   net of). Both block the freeze; neither blocks anchor sourcing.
