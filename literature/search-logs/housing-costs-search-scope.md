# Search scope — housing costs and space constraints

**Hypothesis:** C.2.c (HYPOTHESES-v5.md)
**Hypothesis slug:** `housing-costs`
**Target phenomenon:** SDT primary. **FDT-period evidence is not excluded on period grounds** —
ruling below. See "A note on the pre-modern niche" below for the PM boundary, which this scope does
not annex.

> **Period ruling (Shravan, 2026-07-31).** The v5 entry scopes C.2.c to SDT only. Li 2024 (*Labour
> Economics*, `10.1016/j.labeco.2024.102572`) runs a global house-price panel **1870–2012** framed
> against the fertility transition, and is **admitted to this chapter**. The practical consequence is
> that a study is not excluded merely because its window predates the SDT. The **`phenomena` field in
> HYPOTHESES-v5 still reads "SDT"** and updating it is a PI call, not an RA one — so this ruling
> governs *inclusion* while the formal per-phenomenon verdict structure stays SDT-primary. If further
> FDT-era evidence accumulates in the snowball, the field needs a formal update rather than a second
> case-by-case exception; flag it at that point. Every effect carries its period regardless (see the
> required tags), so the FDT-era estimates stay separable in synthesis.
**Status:** DRAFT (Shravan, 2026-07-31) — walls, estimand structure, and pooling rule proposed,
**not yet frozen.** Identifying variation RULED (Shravan, 2026-07-31; see below). Freeze requires a
second read on the tenure-conditioning decision and sign-off on the pooling rule. Channel-1 anchor
sourcing in progress.

## Ruling on the identifying variation (Shravan, 2026-07-31)

The three-way overlap between C.2.c, C.3.e, and A.23 is resolved by asking **what varies**, not what
mechanism the author narrates. Each of the three hypotheses is defined by a different underlying
source of variation:

| Hypothesis | The variation it owns |
|---|---|
| **C.2.c** | **Variation in housing prices** |
| C.3.e | Variation in liquidity / credit constraints |
| A.23 | Variation in co-residence with parents — whatever drives it (housing costs *or* social norms) |

Two consequences the rule settles immediately:

- **A.23 is not a housing hypothesis.** Co-residence has multiple upstream drivers, and A.23 owns the
  co-residence variation itself. So a paper exploiting price variation is C.2.c's even when
  co-residence is the visible mediator, and a paper exploiting variation in co-residence — norm-driven
  or otherwise — is A.23's even when housing costs are the narrated cause. This is the mediator rule
  of Wall 2, now grounded in the source of variation rather than in a mechanism judgment.
- **The home-equity/collateral studies are C.2.c's**, because their identifying variation is a
  housing price shock, not a change in credit terms. That resolves the Lovenheim and Mumford
  double-listing (Wall 1).

**Reading applied in this scope, flagged for correction:** "housing prices" is read as *the price of
housing*, covering both purchase prices and **rents** — rent is the price of housing services, and the
contrast the ruling draws is against liquidity and co-residence, not against rents. Under this reading
the rent stratum stays in, and stays the cleanest identification of the cost channel. Two secondary
cells sit further from the ruling's centre and are marked as such below: affordability ratios (a
ratio, not a price) and physical space or dwelling size (a quantity constraint at given price — the
"space constraints" half of the hypothesis title). Neither is dropped; both are demoted out of the
primary pools.

## Causal claim

Housing is an input to child-rearing that is bought in large, lumpy units: an additional child
requires additional space, and space is priced. Where house prices and rents are high relative to the
resources of people in their childbearing years, the implicit price of an additional child rises, and
fertility falls — through forgone or postponed births, and through blocked transitions to the parities
that require another bedroom.

That is the claim. The chapter's difficulty is that the claim, as stated, is about a **net** effect
that the literature has already decomposed into two opposing channels.

## The sign is tenure-conditional, and this is the whole chapter

C.2.c's own `notes` field in HYPOTHESES-v5.md concedes it: "Ambiguous sign because home-equity wealth
effect partially offsets cost effect." Unpacked, a rise in house prices does two different things to
two different groups:

- **The cost channel.** For renters, and for prospective buyers not yet on the ladder, a price or rent
  increase is a pure increase in the price of the space input. Predicted effect on fertility:
  **negative.**
- **The wealth channel.** For existing owners, the same price increase is a capital gain. If children
  are a normal good (the C.1.a baseline), it raises desired fertility; it also relaxes collateral
  constraints by raising home equity that can be borrowed against. Predicted effect: **positive.**

The organizing empirical result of this literature is that both channels are present and **opposite in
sign**, split by housing tenure. Three consequences follow, and they structure everything downstream.

**Consequence 1 — the aggregate elasticity is not a transportable parameter.** Any population-level
estimate of "the effect of house prices on fertility" is a tenure-composition-weighted average of two
opposing effects. The weight is the homeownership rate among people of childbearing age in that
setting. The same price shock therefore has a different aggregate effect in a country with 45%
ownership than in one with 75%, **with identical behavioral parameters.** A meta-analysis that pools
aggregate estimates across settings is estimating the sample's tenure mix, not a behavioral quantity.

**Consequence 2 — the interpretable estimates condition on an endogenous variable.** Splitting by
tenure is what makes the estimates interpretable, and tenure is chosen. People who intend to have
children buy homes, buy earlier, and buy larger; homeownership at the time of a price shock is
therefore partly an expression of the fertility intentions the study is trying to explain. The
tenure-split estimates the chapter needs are conditioned on a variable selected on the outcome. This
is structurally the same problem as A.10's conditioning on marital status, and it is where the
risk-of-bias pass will concentrate rather than being a caveat appended at the end.

**Consequence 3 — rent variation is the cleanest test of the hypothesis as written.** A rent increase
carries no offsetting wealth gain for the person paying it. Estimates identified off rents isolate the
cost channel without requiring a tenure split. Estimates identified off prices confound cost and
wealth unless split. This is a quality ordering on the evidence, and it should be recorded as one.

## Pooling rule (pre-registered — in the spirit of TICK-027 and the A.10 sign convention)

1. **Orient every effect** as the change in the outcome per unit increase in the housing price or rent
   measure. Record the measure, its units, and whether it is a level, a log, or a ratio.
2. **The primary pooled targets are the two tenure-specific channels, pooled separately:** a
   cost-channel pool (renters and prospective buyers, or rent-identified estimates) and a
   wealth-channel pool (existing owners). **These two are never combined into one pooled estimate.**
3. **Aggregate, tenure-unsplit estimates are a derived quantity, not a primary pooling target.** They
   may be pooled only as a secondary analysis, and only with the **homeownership rate among the
   childbearing-age sample recorded as a required moderator**. An aggregate estimate whose setting's
   ownership rate cannot be established is not poolable.
4. **Do not pool across treatment types** — price, rent, affordability ratio, and physical space are
   different treatments (below), not different measures of one treatment.
5. **Do not pool across outcome levels.** Realized births, completed fertility, and stated intentions
   pool separately, per the standing D.3.b synthesis rule.

## The treatment is four different variables

The hypothesis title names two things — costs *and* space constraints — and the literature uses at
least four distinct regressors. They are not interchangeable.

- **House price** (asset price). Carries both the cost and the wealth component. Requires a tenure
  split to interpret.
- **Rent.** Pure cost for the payer. The cleanest identification of the cost channel.
- **Affordability ratio** (price-to-income, rent-to-income, or a housing-cost burden share).
  **Treat with suspicion and record separately.** Income sits in the denominator and has its own
  independent effect on fertility (C.1.a), so a coefficient on an affordability ratio mixes a price
  effect with an income effect running the other way. A negative coefficient on price-to-income is
  consistent with a pure positive income effect and no price effect at all.
- **Physical space or quantity** — dwelling size, rooms per person, crowding, minimum-unit
  regulation. This is the "space constraints" half of the hypothesis, and it operates **at a given
  price**: a household that cannot fit a third child into a two-bedroom flat faces a quantity
  constraint, not a price. Distinct estimand, its own cell.

## The boundary walls

**Wall 1 — C.2.c vs C.3.e (`credit-constraints`): source of exogenous variation. The demonstrated
failure.**

This wall is not hypothetical: **Lovenheim and Mumford 2013 is listed as `seminal` for both C.2.c and
C.3.e** in HYPOTHESES-v5.md. The same paper is currently claimed by two hypotheses, because the
home-equity channel — price up, collateral value up, borrowing capacity up, fertility up — is
describable either as a housing-price effect or as a relaxed credit constraint.

- **Discriminator: what is the source of exogenous variation the estimate uses?**
  - Variation in **housing prices or rents** → **C.2.c**, whatever channel the authors invoke. This
    follows the v5 entry, which explicitly assigns the wealth-offset ambiguity to C.2.c; the chapter
    cannot adjudicate its own sign if it does not own both channels.
  - Variation in **credit terms holding housing prices fixed** — mortgage credit supply shocks,
    loan-to-value or debt-to-income caps, interest-rate shocks, deposit requirements, insurance
    access → **C.3.e**.
- Under this rule the housing-price-shock studies are **C.2.c's**, and C.3.e should carry them as a
  cross-reference rather than as seminal works. *(Recommended master-list edit for TICK-001: strike
  Lovenheim and Mumford 2013 from C.3.e's seminal list and cross-ref C.2.c instead. Flagged, not
  made — HYPOTHESES-v5.md is under PI review.)*
- A design that jointly exploits a price shock **and** a credit-access shock, and cannot separate
  them, is `MIXED_PRICE_CREDIT` and is reported to both chapters as unallocated.

**Wall 2 — C.2.c vs A.23 (`co-residence-parents-household-delay`): the mediator wall.**

The master list already draws this one, and correctly: A.23's mechanism is that co-residence blocks
household formation and sexual autonomy "even at given housing prices — the constraint operates
through living arrangements, not just affordability."

- **A.23 owns** living arrangement → fertility, at given prices.
- **C.2.c owns** housing cost → fertility **including the part that runs through co-residence**,
  because C.2.c owns the treatment and A.23 owns the mediator.
- **Discriminator:** does the estimate exploit variation in housing prices or rents? If yes it is
  C.2.c's reduced form, whatever the mediator. If the treatment is the living arrangement itself, with
  no price variation, it is A.23's.
- **Non-additivity hazard — the second instance in the review.** C.2.c's demographic-significance
  contribution and A.23's are **not additive**; most of C.2.c's effect on young adults travels down
  A.23's channel. This is the identical accounting problem flagged at A.10 → A.7 (TICK-054), which
  makes two chapters hitting it and argues for a **review-wide rule** rather than a per-chapter note.
  Folded into the TICK-054 escalation rather than raised separately.

**Wall 3 — C.2.c vs C.2.b (`child-cost-direct`): which price moved.**

Housing is a line item in any full accounting of what a child costs, so a cost-of-children study
generally contains a housing component.

- **Discriminator:** C.2.c is identified off variation in the **price of housing specifically**;
  C.2.b off the general cost bundle and the consumption norms that set it.
- A cost-of-raising-a-child calculation that includes a housing allocation is **C.2.b**, even though
  housing is inside it. A study of house price variation is C.2.c, even though housing is a child
  cost.

**Wall 4 — C.2.c vs C.2.g (`urbanization-residential-shift`): within-market variation.**

Cities have higher housing costs and lower fertility, which makes the urban fertility deficit
attributable to housing on a cross-section — and to five other things as well.

- **Discriminator:** C.2.c requires variation in housing costs **within** a defined market or over
  time, with the price as the identified treatment. A rural-versus-urban fertility comparison, or a
  density gradient, attributed to housing costs without isolating price variation, is **C.2.g** — its
  entry already names housing as one of its own channels and owns the composition-versus-behavior
  decomposition.

**Wall 5 — C.2.c vs C.1.a (`income-effect-normal-good`): cross-feed, not a route.**

The wealth channel is an income/wealth effect that happens to arrive through a housing asset. C.2.c
owns it, per Wall 1. But the relationship runs the other way too, and the chapter should say so: the
housing-wealth literature is one of the **better natural experiments available for testing C.1.a's
income effect**, since a price shock delivers a wealth change plausibly unrelated to the household's
own productivity or preferences. So wealth-channel estimates live in C.2.c and are **fed to C.1.a as
evidence.** That is a cross-reference obligation, not a routing decision.

**Wall 6 — C.3.g (`student-debt-household-formation`): light.** Student debt compounds a housing
affordability constraint but is a distinct prior liability. A paper whose treatment is debt burden is
C.3.g; one whose treatment is house prices, with debt as a moderator, is C.2.c with a recorded
moderator.

## Estimand cells

| Cell | Treatment / variation | Fertility outcome | Routing |
|---|---|---|---|
| `PRIMARY_COST_RENTER` | Housing price or rent variation, on renters / prospective buyers | Fertility (births, parity progression, completed fertility) | Primary synthesis — cost-channel pool |
| `PRIMARY_COST_RENT_IDENTIFIED` | Rent variation, no tenure split needed | Fertility | Primary synthesis — cost-channel pool, highest-quality stratum |
| `PRIMARY_WEALTH_OWNER` | Housing price variation, on existing owners | Fertility | Primary synthesis — wealth-channel pool (separate); also fed to C.1.a |
| `PRIMARY_SPACE_QUANTITY` | Dwelling size, rooms, crowding, or unit-size regulation at given price | Fertility | Primary synthesis, pooled separately (different treatment) |
| `AGGREGATE_UNSPLIT` | Price variation, population-level, no tenure split | Fertility | Secondary only; requires the ownership-rate moderator or it is not poolable |
| `AFFORDABILITY_RATIO` | Price-to-income or housing-burden share | Fertility | Recorded separately; not pooled with price or rent estimates (income confound) |
| `MIXED_PRICE_CREDIT` | Price and credit-access variation, inseparable | Fertility | Primary, flagged unallocated; also reported to C.3.e |
| `HOUSING_ONLY_MECHANISM` | Housing costs → co-residence, household formation, homeownership, migration — **no fertility outcome** | None | Mechanism / context; cross-ref A.23 |
| `HOUSING_MARKET_THEORY` | Housing-regime typologies, formal models of lumpy durable goods and family formation | No empirical fertility estimate | Theory stream |
| `OFF_CREDIT_C3e` | Credit terms / mortgage supply at fixed prices | Fertility | Route to C.3.e |
| `OFF_LIVING_ARRANGEMENT_A23` | Living arrangement as treatment, no price variation | Fertility | Route to A.23 |
| `OFF_CHILD_COST_C2b` | General cost-of-children bundle | Fertility | Route to C.2.b |
| `OFF_URBANIZATION_C2g` | Urban–rural or density comparison without isolated price variation | Fertility | Route to C.2.g |
| `OFF_DEBT_C3g` | Student or consumer debt burden as treatment | Fertility | Route to C.3.g |
| `OFF_OUTCOME` | Housing costs → some other non-fertility outcome (migration, marriage, labor supply, health, wellbeing) | None | Mechanism / context only |
| `OFF_OTHER` | Non-C.2.c fertility determinant with no sibling home | Fertility | Route out; no sibling queue |
| `REVERSE` | Fertility or family formation → housing demand, tenure, or prices | Housing outcome | Context — and see the identification threat below |
| `INSUFFICIENT_INFO` | Cannot be routed on the visible record | Unknown | Pairs only with `UNCERTAIN` |

## Required tags on every included empirical effect

Beyond the routing cell, each effect carries:

- `TENURE_GROUP` — renter / owner / prospective buyer / unsplit, and how tenure was measured and
  when relative to the shock (pre-determined tenure is materially better than contemporaneous).
- `OWNERSHIP_RATE` — the homeownership rate of the childbearing-age population in the setting.
  Required on every `AGGREGATE_UNSPLIT` effect; without it the effect is not poolable.
- `TREATMENT_TYPE` — price / rent / affordability ratio / physical space.
- `PARITY` — **housing plausibly binds hardest at the transition requiring an additional bedroom**,
  so parity-specific effects are expected and a pooled all-parity number would mask them. Record the
  parity the estimate refers to; cross-ref A.8.
- `TEMPO_OR_QUANTUM` — does the estimate speak to **timing** of births or to **completed** fertility?
  Housing effects are widely suspected to be substantially postponement. If they are, C.2.c's
  demographic significance for completed cohort fertility is far smaller than its effect on period
  measures, and the chapter's §7 verdict turns on this. Cross-ref A.11 (tempo), and note the
  precedent set at TICK-038 for nesting a tempo interpretation under A.11.
- `OUTCOME_LEVEL` — realized births / completed fertility / stated intention.
- `SOURCE_OF_VARIATION` — supply-elasticity or land-use instrument, national price cycle interacted
  with local exposure, policy shock, panel/time-series variation, or cross-section only.

## Identification threats (what the risk-of-bias pass is actually looking for)

1. **Reverse causality and anticipatory sorting.** People who plan children buy larger homes, buy
   earlier, and move to family-oriented areas. Fertility intentions drive housing demand, which drives
   prices. A cross-sectional association between local prices and local fertility is contaminated in
   both directions at once.
2. **Endogenous location.** High-price areas differ systematically in amenities, industry mix,
   education, female wages (C.2.e), and culture. Regional price variation is not exogenous to
   fertility determinants; it is nearly a summary statistic for them.
3. **Endogenous tenure** (Consequence 2 above). The tenure split that makes the estimates
   interpretable conditions on a choice made in anticipation of the outcome. Designs using
   pre-determined tenure, or instrumenting it, are materially stronger and should be graded as such.
4. **The affordability-ratio income confound** — income in the denominator carries its own fertility
   effect in the opposite direction.
5. **Instrument exclusion.** The standard instruments — housing supply elasticity from land
   unavailability or topography, land-use regulation, national price cycles interacted with local
   exposure — each have known exclusion problems. Supply-inelastic places differ from elastic ones on
   more than supply; national cycles move local labor markets and incomes simultaneously.
   **Record which of these the design addresses**, not merely which instrument it uses.

## When to adjudicate

The title/abstract screen decides only which stream a paper belongs to. It does **not** require the
RA to determine the tenure split, the parity, or the tempo/quantum reading from an abstract.

**The D.3.b and A.10 caution applies here with equal force.** Whether an estimate is tenure-split,
what the treatment variable actually is (price vs affordability ratio vs rent), and whether the
outcome is timing or quantum are **full-text-only facts in most papers**. The D.3.b stratum-A gate
found its decisive routing failures were invisible to any title/abstract screen; expect the same and
budget an RA-gate bleed-in rather than treating the screen's routing as final.

Drafting may report only what these full-text fields support. A regional correlation between house
prices and fertility, with no source of exogenous variation, may document an association but must not
be described as evidence that housing costs *caused* the fertility difference — threats 1 and 2 above
are sufficient on their own to generate that correlation with no causal effect at all.

## A note on the pre-modern niche (scope observation, not an expansion)

The v5 entry scopes C.2.c to the SDT, and this scope keeps that. It is worth recording, for A.7's
chapter rather than this one, that the pre-modern European marriage pattern rests on economically
identical logic: household formation required a **niche** — a farm, a holding, a dwelling — and
marriage waited until one was available, which is a space-and-housing constraint operating on
fertility through nuptiality. That mechanism currently lives inside A.7 (Hajnal, the preventive
check). No action here; flagged so the connection is not lost, and so the review does not later
discover it as a gap.

## Expected shape of the evidence (a caution, not a result)

1. **This is a well-studied hypothesis with a genuine quantitative literature**, credible
   quasi-experimental designs, and plausibly some prior systematic or scoping reviews — which makes it,
   like A.10, a reasonable candidate for exercising the cold-start bootstrap's channel 1 and GACS §7
   move 5.
2. **The literature spans two disciplines with two vocabularies.** Economics says *house prices,
   housing wealth, real estate, home equity, housing supply elasticity*; demography and housing studies
   say *housing tenure, dwelling, residential, homeownership, housing regime, housing career*. These
   are largely non-overlapping vocabulary families and should be expected to form **separate cause-axis
   clusters** under the GACS granularity rule, not one merged cluster.
3. **The estimand collapse should be less severe than A.10's** — fertility is commonly the outcome in
   this literature rather than incidental to it — but `HOUSING_ONLY_MECHANISM` will still be large,
   because a great deal of this work stops at homeownership, household formation, or co-residence and
   never reaches a birth.
4. **Expect the tenure split to be missing more often than present.** Many estimates will be
   `AGGREGATE_UNSPLIT`, which under the pooling rule above are secondary and require an ownership-rate
   moderator. If that stratum dominates, the honest chapter result is that the literature mostly
   reports a composition-weighted average and cannot identify the behavioral parameters separately —
   which is a finding about the field, and should be reported as one rather than engineered around.
5. **Geographic skew** toward the US, UK, and high-price East Asian and Southern European settings.
   Since the aggregate effect depends on the ownership rate, and ownership rates vary enormously
   across exactly these settings, the geographic skew is not merely an external-validity caveat here —
   it directly moves the pooled number.

## Cold-start channels and leakage wall

1. Prior meta-analyses and systematic or scoping reviews of housing and fertility → empirical anchors
   by external authority. *(Leakage wall: a review's search strings may feed query terms and its
   included studies may feed anchors, but never the same study to both.)*
2. Top-down theory/canon enumeration — housing-regime typologies, models of lumpy durable goods and
   household formation — seeds the theory set. Does not count toward empirical recall.
3. Citation snowball from the channel-1 and channel-2 seeds → the orthogonal Tier-B frame.
4. Broad single-query search plus a structured screen, **only if** the gold is still under the
   cross-validation floor (≥ 30 empirical anchors). Tier B is never drawn from this channel.
5. Production-query terms are not mined from a paper and then evaluated on it; learned extensions are
   fold-local once the gold frame exists.

## Pre-query anchor audit (not yet built)

The verified anchor set will be stored in `housing-costs-cold-start-anchors.json`. Every anchor must
clear the **mandatory existence-verification gate** — a live DOI, or a Crossref/publisher record
confirming the title exists — before it enters any recall denominator. **No anchor is hand-asserted
from memory**, including the four works named in the v5 `seminal` field, which are **candidates to
verify, not anchors**. This is the standing rule from the 2026-07-08 run that found ~40% of the frozen
OAS Tier B was fabricated snowball citations.

The anchor set must deliberately carry **off-cell decoys** so the eventual query is tested on routing
as well as topical retrieval: credit-supply-shock studies (C.3.e), living-arrangement studies (A.23),
urban–rural fertility comparisons (C.2.g), cost-of-children accounting (C.2.b), and housing-cost
studies whose outcome is migration or marriage rather than fertility. Given Wall 1's demonstrated
failure in the master list itself, the C.3.e decoys are the ones that matter most.
