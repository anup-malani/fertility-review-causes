# Search scope — co-residence with parents and delayed household formation

**Hypothesis:** A.23 (HYPOTHESES-v5.md)
**Hypothesis slug:** `co-residence-parents-household-delay`
**Ticket:** TICK-075
**Target phenomenon:** SDT.
**Status:** DRAFT (Shravan, 2026-08-27) — walls, estimand cells and pooling rule proposed,
**not frozen.** Two PI calls below (Calls 1 and 2) have to come back before the frame is built,
because both change which records the production query is required to reach.

---

## 1. The claim

Forming an independent household is a near-universal precursor to consolidating a partnership and
having a first child. A.23 says the precursor has become harder: young adults stay in the parental
home longer, and while they are there they face practical constraints — no privacy, nowhere to host a
partner, parental oversight — and a subjective one, the sense of not yet being an adult with a
household of one's own. Fertility is delayed or foregone even where the desire for children is intact.

The mechanism is a *living arrangement*, not a price. That is the whole basis on which this
hypothesis is separate from C.2.c, and the ruling that draws the line is already made.

## 2. The inherited ruling — adopt, do not re-litigate

C.2.c's search scope (`housing-costs-search-scope.md`, ruling of 2026-07-31) resolved the three-way
overlap between C.2.c, C.3.e and A.23 by asking **what varies**, not what mechanism the author
narrates:

| Hypothesis | The variation it owns |
|---|---|
| C.2.c | Variation in housing prices and rents |
| C.3.e | Variation in liquidity / credit constraints |
| **A.23** | **Variation in co-residence with parents — whatever drives it (housing costs *or* social norms)** |

Two consequences carry directly into this chapter and are not reopened here:

- **A paper exploiting price variation is C.2.c's even when co-residence is the visible mediator.**
  C.2.c owns the treatment; A.23 owns the mediator. A paper exploiting variation in the living
  arrangement itself — norm-driven, policy-driven, or otherwise — is A.23's even when housing costs
  are the narrated cause.
- **The two chapters' demographic-significance contributions are not additive.** Most of C.2.c's
  effect on young adults travels down A.23's channel. This is the second instance of the accounting
  problem first flagged at A.10 → A.7 (TICK-054), and it was folded into that escalation rather than
  raised separately. §8 of this chapter must not add A.23's contribution to C.2.c's.

What this scope adds is the reverse-direction obligation C.2.c could not state: **A.23's own estimates
are, in large part, the mechanism by which C.2.c operates.** Where a price-identified C.2.c estimate
and a co-residence-identified A.23 estimate both exist for the same setting, they are two readings of
one channel and the chapter should say so.

## 3. What makes this chapter hard: the treatment is an event in the same sequence as the outcome

C.2.c's difficulty was that its treatment has two signs depending on tenure. A.23's is worse in kind.

Leaving the parental home, forming a union, and having a first child are three transitions in a single
life-course sequence, and people order them jointly. Someone who intends to have a child soon moves
out in order to do it. The comparison that the hypothesis appears to call for — the fertility of young
adults who live with their parents against those who do not — is therefore a comparison between people
who have started that sequence and people who have not. It will show a large fertility gap under the
null of no causal effect whatsoever.

This is not a caveat to be appended to the risk-of-bias section. It is the reason most of the topical
literature cannot be used as evidence here, and it defines what an admissible estimate is:

> **An admissible A.23 estimate uses variation in the living arrangement that is not itself chosen in
> anticipation of childbearing.**

The same structure has already bitten this review twice. It is C.2.c's endogenous-tenure problem
(people who plan children buy homes) with the anticipation running through an even shorter causal
distance, and it is A.24's venue-comparison problem: comparing couples who met online with couples who
met offline conditions on having formed a couple, so it is silent on the rate question by
construction. Here, conditioning on having left home conditions on the launch decision.

## 4. Where admissible variation could come from — enumerated before searching, deliberately

The C.3.g lesson is that a negative finding about identified evidence is only as good as the
vocabulary that looked for it: C.3.g's "no natural experiment exists" turned out to be two missing
words. So the candidate designs are enumerated here **before** the query is written, and each named
design becomes a required search string. If a cell comes back empty, it comes back empty against a
list someone can audit.

1. **Age-threshold rules in housing benefit.** The UK Local Housing Allowance shared-accommodation
   rate applies below an age cut-off that was moved from 25 to 35 in 2012 — a discontinuity in the
   subsidy for independent accommodation, at an age directly relevant to first birth.
2. **Youth housing allowances and move-out grants** conditional on establishing an independent
   residence (Southern European and Nordic schemes; the French APL literature). *These are price
   instruments aimed at the arrangement, and they sit on the Wall-1 seam — see `MIXED_PRICE_ARRANGEMENT`.*
3. **Administrative allocation of dwellings**: public-housing waiting lists and lotteries, Chinese
   work-unit and hukou-linked allocation, post-socialist restitution. Allocation moves the arrangement
   at a given price, which is exactly the variation A.23 owns.
4. **Compulsory removal from the parental home**: conscription, boarding school, residential-university
   assignment where assignment is not chosen.
5. **Dwelling destruction and reconstruction shocks** — earthquake, fire, war damage — that force or
   dissolve co-residence.
6. **Legal changes in parental support obligations and in the age of majority** for benefit purposes.
7. **Sibling composition and birth order** as instruments for the timing of home-leaving.
8. **Grandparental availability shocks** — parental death, retirement-age reform changing whether a
   grandparent is at home — for the extended-household configuration in §5.

Designs 1–2 are price-adjacent and are ruled on in Wall 1. Designs 3–6 are the clean cases.

## 5. The variable takes two configurations, and they have opposite signs

This is the chapter's organizing empirical fact, and the registered hypothesis names only one of them.

- **Pre-launch co-residence.** An unpartnered, childless young adult living in the parental home.
  This is what the v5 entry describes, and the predicted sign is **negative**: privacy and autonomy
  constraints, delayed union formation, deferred adult status.
- **Extended-household co-residence.** A couple — usually married, often already parents — living
  with or adjacent to a parent or parent-in-law. Here the parent supplies childcare and household
  labour, and the predicted sign is **positive**. This configuration is the modal one in the East
  Asian literature and a substantial part of the Southern European one.

They share a phrase and a variable name and nothing else. Pooling them would produce a number whose
sign is set by the sample's mix of life stages, in precisely the way C.2.c's aggregate elasticity is
set by its sample's tenure mix. The lesson recorded there applies unchanged: this is not a
transportable parameter.

> **PI Call 1 — does A.23 own the extended-household configuration?**
> The v5 claim, read strictly, is about the pre-launch configuration only. Two options:
> **(a)** A.23 owns the living arrangement in both configurations, reports them as two separately
> pooled cells, and its verdict is explicitly configuration-conditional. **(b)** A.23 is restricted to
> pre-launch co-residence, and the extended-household evidence routes to C.2.a (childcare) as an
> informal-childcare-supply question.
> **Recommendation: (a).** Under (b) the chapter would report only the estimates whose sign agrees with
> the registered claim, which is selection on the outcome of the review itself. Under (a) the chapter
> can state the real finding — that the sign of "co-residence with parents" depends on who is
> co-residing with whom — which is a result, not a nuisance. This is the same shape as the A.12 call
> that split at the margin rather than dropping an arm.

## 6. The homonym, and the axis the wall must be cut on

"Co-residence with parents" is also the standard term for an adult child housing an **elderly** parent.
That literature is large, sits in gerontology and long-term care, and has the dependency running the
opposite way. It is not a routing nuisance to be filtered on the word "elderly": a married couple in
Shanghai living with a healthy 62-year-old mother who minds the baby, and the same couple ten years
later caring for her, are the same household in the same dataset.

So the wall is **not** cut on the vocabulary. It is cut on **who depends on whom, and at what life
stage** — which is a full-text fact, and frequently a table-of-descriptives fact rather than an
abstract one. The A.17 lesson applies: a wall cut on the wrong axis leaves a residue that looks like
ambiguity and is actually a missing category. Three values, not two:
`PRE_LAUNCH` / `EXTENDED_COUPLE` / `ELDER_SUPPORT`, and the third is a route-out.

## 7. The boundary walls

**Wall 1 — A.23 vs C.2.c (`housing-costs`): the mediator wall. Inherited, §2.**
Price or rent variation → C.2.c, whatever the mediator. Living arrangement as the treatment, with no
price variation → A.23. **New sub-ruling required by design 2 above:** a subsidy or grant *conditional
on establishing an independent residence* is a price change **and** an arrangement instrument at once.
It is `MIXED_PRICE_ARRANGEMENT`, reported to both chapters as unallocated, on the model of C.2.c's
`MIXED_PRICE_CREDIT`. It is not silently claimed here.

**Wall 2 — A.23 vs A.7 (`age-at-marriage-timing`): the second non-additivity.**
A.23's mechanism runs substantially *through* delayed union formation, which is A.7's variable. The
discriminator is the same one: A.23 owns variation in the living arrangement; A.7 owns variation in
marriage/union timing. A study that uses co-residence to explain marriage timing, and stops there, is a
**link-1 mechanism record** for A.23 — real evidence about the first link of the chain, not a fertility
estimate — and cross-refs A.7. The non-additivity flagged at A.10 → A.7 (TICK-054) now has a third
instance; it should be settled review-wide, not here.

**Wall 3 — A.23 vs D.2.b (`marriage-family-norms`) and D.1.a: the strong-family-ties regime.**
Reher 1998, which the v5 entry lists as seminal, is a claim about cross-national *family systems*, not
about a household's living arrangement. A study whose variation is the country's family-tie regime is
D.2.b's; it is also, on its own, unidentified for A.23's purposes — cross-national comparisons of
Southern versus Northern Europe differ on everything. A.23 needs **within-setting** variation in the
arrangement.

**Wall 4 — A.23 vs C.5.a (`economic-uncertainty`) and C.3.g (`student-debt`).**
Youth labour-market insecurity and prior debt are among the main drivers of extended co-residence.
Where the treatment is the labour-market shock or the debt burden, the record belongs to those
chapters with co-residence as the mediator. Symmetric with Wall 1.

**Wall 5 — A.23 vs C.2.a (`childcare-cost-availability`).**
For the extended-household configuration, the operative mechanism is often grandparental childcare.
C.2.a owns the price and availability of childcare; A.23 owns the living arrangement that supplies it
informally. A study whose treatment is co-residence or parental proximity is A.23's with a recorded
C.2.a mechanism; one whose treatment is formal childcare cost or a childcare policy is C.2.a's.

**Wall 6 — A.23 vs C.2.g (`urbanization-residential-shift`): light.** An urban–rural contrast in
co-residence rates, without isolated variation in the arrangement, is C.2.g's.

## 8. Estimand cells

| Cell | Treatment / variation | Outcome | Routing |
|---|---|---|---|
| `PRIMARY_PRELAUNCH` | Co-residence of an unpartnered/childless young adult in the parental home | Fertility (first birth, parity progression, completed fertility) | Primary synthesis — pre-launch pool |
| `PRIMARY_EXTENDED_COUPLE` | Couple co-residing with a parent or parent-in-law | Fertility | Primary synthesis — extended-household pool, **never pooled with pre-launch** (pending PI Call 1) |
| `PRIMARY_PROXIMITY` | Residential *proximity* to parents without co-residence | Fertility | Primary synthesis, pooled separately — different treatment |
| `LINK1_ARRANGEMENT_TO_UNION` | Arrangement → union formation or marriage timing, no birth outcome | Union | Mechanism, link 1 of the chain; cross-ref A.7 |
| `LINK1_DRIVER_TO_ARRANGEMENT` | Anything → co-residence, no fertility outcome | Living arrangement | Mechanism / context; establishes the exposure trend |
| `MIXED_PRICE_ARRANGEMENT` | Subsidy or grant conditional on independent residence | Fertility | Primary, flagged unallocated; also reported to C.2.c |
| `AGGREGATE_UNSPLIT` | Co-residence with no life-stage split | Fertility | Secondary only; requires the life-stage composition recorded or it is not poolable |
| `ELDER_SUPPORT` | Adult child housing a dependent elderly parent | Any | Route out — the homonym |
| `OFF_PRICE_C2c` | Housing price or rent variation | Fertility | Route to C.2.c |
| `OFF_UNION_TIMING_A7` | Marriage/union timing as the treatment | Fertility | Route to A.7 |
| `OFF_NORMS_D2b` | Cross-national family-system regime as the variation | Fertility | Route to D.2.b |
| `OFF_UNCERTAINTY_C5a` / `OFF_DEBT_C3g` | Labour-market shock or debt burden as treatment | Fertility | Route to C.5.a / C.3.g |
| `OFF_CHILDCARE_C2a` | Formal childcare price or policy as treatment | Fertility | Route to C.2.a |
| `THEORY` | Life-course and household-formation theory, family-system typologies | No estimate | Theory stream |
| `REVERSE` | Fertility or union formation → living arrangement | Arrangement | Context — and see threat 1 |
| `INSUFFICIENT_INFO` | Not routable on the visible record | Unknown | Pairs only with `UNCERTAIN` |

## 9. Required tags on every included empirical effect

- `LIFE_STAGE_CONFIG` — `PRE_LAUNCH` / `EXTENDED_COUPLE` / `ELDER_SUPPORT` / `UNSPLIT`, and **how it
  was established** (sample restriction, an interaction, or inferred by the extractor). The A.17
  lesson: a safeguard that is never measured is a safeguard that fired zero times. This field's
  distribution is reported in the chapter, not just used for routing.
- `ARRANGEMENT_MEASURE` — co-residence indicator / duration of co-residence / age at leaving home /
  distance to parents / household composition code.
- `SOURCE_OF_VARIATION` — one of the eight designs in §4, or "cross-section only".
- `ANTICIPATION_CONTROL` — what, if anything, the design does about §3: pre-determined arrangement,
  an instrument, sibling fixed effects, event-history with time-varying covariates, or nothing.
- `OUTCOME_LEVEL` — realized births / completed fertility / stated intention. Pooled separately, per
  the standing D.3.b rule.
- `TEMPO_OR_QUANTUM` — postponement or completed fertility. A.23 is a delay mechanism by construction,
  so a period-measure effect may leave completed cohort fertility untouched. §7's verdict turns on
  this; cross-ref A.11 and the TICK-038 precedent.
- `SETTING_COHABITATION_NORM` — whether non-marital cohabitation is common in the setting. Where it is
  not, leaving home and marrying are the same event and the treatment is not separable from A.7's.

## 10. Identification threats

1. **Anticipation and joint determination (§3).** The central threat, not one of several.
2. **Reverse causation.** A pregnancy is among the most common reasons to leave the parental home. A
   panel that finds co-residence ending shortly before a first birth has found the reverse arrow.
3. **Selection into staying.** Young adults who remain at home differ in earnings, health, education,
   partnership history and parental wealth. The residual after controls is not a treatment effect.
4. **Aggregation across life-stage configurations (§5).** An unsplit estimate mixes two opposite signs.
5. **The homonym (§6).** Elder-support co-residence entering as if it were pre-launch co-residence.
6. **Instrument exclusion for the §4 designs.** Conscription changes far more than housing;
   dwelling-destruction shocks destroy local labour markets; benefit age thresholds move income as well
   as accommodation.

## 11. Evidence-base posture

The C.2.c and D.3.b posture is adopted: **a thin identified evidence base is an acceptable result, not
a search failure.** The seed harvest already suggests the shape — a large, high-quality
*transition-to-adulthood* literature whose outcome is leaving home itself, and a much smaller set that
carries the sequence through to a birth.

The standing obligation attached there attaches here. The posture governs how the shrinkage is
*interpreted*, not whether it is *reported*: that most of the co-residence literature stops at the
living arrangement or at union formation is a finding about the field and belongs in the chapter, with
the denominator visible.

## 12. Cold-start channels and the seed harvest already done

Channel 0, done before this document, is unusual to this chapter and worth naming: **C.2.c's finished
artifacts are a seed source.** `212_a23_harvest_c2c_seeds.py` recovered 159 candidates —
14 records C.2.c screened and routed here under its own ruling, 1 verified cold-start anchor, and 144
mined from C.2.c's 10,915-record snowball pool on A.23's exposure vocabulary. These are hand-sourced
seeds and are part of the evidence base, not screen residue (the D.2.d lesson, where reporting only the
screen's output undercounted the primary pool 2 against 9).

Then, as standard:

1. Prior systematic or scoping reviews of home-leaving, household formation and fertility → empirical
   anchors by external authority. *(Leakage wall: a review's search strings may feed query terms and
   its included studies may feed anchors, but never the same study to both.)*
2. Top-down theory enumeration — life-course transition models, Reher's family-tie typology, the
   semi-autonomy literature — seeds the theory set; does not count toward empirical recall.
3. Citation snowball from channels 1–2 → the orthogonal Tier-B frame.
4. Broad single-query search plus structured screen, only if gold is under the cross-validation floor.
5. The eight named designs of §4 are each their own query string, run whether or not the broad frame
   surfaces them.

Every anchor clears the mandatory existence-verification gate — a live DOI or a Crossref/publisher
record — before entering any recall denominator. **No anchor is hand-asserted from memory**, the three
works in the v5 `seminal` field included; they are candidates to verify. The anchor set must carry
deliberate off-cell decoys: price-identified housing studies (C.2.c), elder-support co-residence
(the §6 homonym), cross-national family-regime comparisons (D.2.b), and home-leaving studies whose
outcome is not a birth.

> **PI Call 2 — does the pre-modern niche connection belong here or in A.7?**
> C.2.c's scope flagged, without annexing it, that the European marriage pattern rests on economically
> identical logic: marriage waited on the availability of a *niche* — a farm, a holding, a dwelling —
> so household formation gated fertility through nuptiality. A.23 is scoped SDT, and the parallel is
> exact rather than approximate. Recommendation: leave the PM mechanism in A.7 and cite the parallel in
> A.23's §2, so the review does not later discover it as a gap. Recorded so the decision is deliberate.

## 13. When to adjudicate

The title/abstract screen decides the stream only. It does **not** ask the RA to determine the
life-stage configuration, the anticipation control, or the tempo/quantum reading from an abstract —
the first of those in particular is usually a sample-restriction or descriptives fact.

The D.3.b precedent governs: that screen's decisive routing failures were invisible to any
title/abstract screen, and the same should be expected here. Budget an RA-gate bleed-in rather than
treating the screen's routing as final.

Drafting may report only what the full-text fields support. An association between living with parents
and not having had a child, with no source of exogenous variation, documents the sequence and must not
be described as evidence that co-residence *caused* the delay: threats 1 through 3 generate that
association with no causal effect at all.
