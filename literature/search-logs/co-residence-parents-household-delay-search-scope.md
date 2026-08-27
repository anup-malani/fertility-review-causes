# Search scope — co-residence with parents and delayed household formation

**Hypothesis:** A.23 (HYPOTHESES-v5.md)
**Hypothesis slug:** `co-residence-parents-household-delay`
**Ticket:** TICK-075
**Target phenomenon:** SDT.
**Status:** DRAFT (Shravan, 2026-08-27) — walls, estimand cells and pooling rule proposed,
**not frozen.** Rulings 1 and 2 (§5, §12) were taken on 2026-08-27 and are marked *PI confirmation
pending*; Ruling 1 widens what the production query is required to reach and is load-bearing for the
anchor set. Freeze requires a second read on the `MIXED_PRICE_ARRANGEMENT` sub-ruling in Wall 1 and
sign-off on the pooling rule.

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

> **Ruling 1 — A.23 owns both configurations. (Shravan, 2026-08-27; PI confirmation pending.)**
> The alternative — restricting the chapter to pre-launch co-residence and routing the
> extended-household evidence to C.2.a as an informal-childcare question — would have the chapter
> report only the estimates whose sign agrees with the registered claim. That is selection on the
> outcome of the review itself. Owning both lets the chapter state the actual finding: **the sign of
> "co-residence with parents" is set by who is co-residing with whom.** Same shape as the A.12 call
> that split at the margin rather than dropping an arm.
>
> Three things follow and bind the rest of this document. **The two cells are never pooled**, and an
> estimate that cannot be assigned to a configuration is `AGGREGATE_UNSPLIT` and secondary. **The
> production query must reach both**, which means the extended-household vocabulary — multigenerational
> household, grandparental childcare, living with parents-in-law, stem family — is required, not
> optional; the pre-launch vocabulary alone would have produced the one-sided pool this ruling exists
> to prevent. And **the §7 verdict is configuration-conditional**, in the way C.2.c's is
> tenure-conditional: there is no single A.23 sign to report.
>
> The v5 `claim` field, which describes only the pre-launch mechanism, should be widened to match.
> Flagged to TICK-001 as a master-list edit; not made here.

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
| `PRIMARY_EXTENDED_COUPLE` | Couple co-residing with a parent or parent-in-law | Fertility | Primary synthesis — extended-household pool, **never pooled with pre-launch** (Ruling 1) |
| `PRIMARY_PROXIMITY` | Residential *proximity* to parents without co-residence | Fertility | Primary synthesis, pooled separately — different treatment |
| `LINK1_ARRANGEMENT_TO_UNION` | Arrangement → union formation or marriage timing, no birth outcome | Union | Mechanism, link 1 of the chain; cross-ref A.7 |
| `LINK1_DRIVER_TO_ARRANGEMENT` | Anything → co-residence, no fertility outcome | Living arrangement | Mechanism / context; establishes the exposure trend |
| `MIXED_PRICE_ARRANGEMENT` | Subsidy or grant conditional on independent residence | Fertility | Primary, flagged unallocated; also reported to C.2.c |
| `AGGREGATE_UNSPLIT` | Co-residence with no life-stage split | Fertility | Secondary only; requires the life-stage composition recorded or it is not poolable |
| `OFF_OUTCOME_LABOUR_SUPPLY` | Co-residence or grandparental childcare → maternal employment, hours, wages | Labour supply | Route out, **named**; the largest single route-out on the round-1 pool. Cross-ref C.2.e |
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

## 11. Measured frame, and the evidence-base posture

`213_a23_frame_probe.py` sizes the cells on OpenAlex `title_and_abstract.search` before any production
query is written. These are **frame sizes, not evidence counts** — what a screen would have to read,
not what would survive it. No probe failed; a failed probe is recorded as an error and never as a zero.

| | records |
|---|---|
| Exposure cloud, any outcome | 32,795 |
| — co-residence sub-cloud | 17,869 |
| — leaving-home sub-cloud | 13,820 |
| — household-formation sub-cloud | 2,192 |
| **Exposure ∩ fertility outcome — the screenable frame (as first measured)** | **1,012** |
| Same, with the emancipation family briefly added and then removed (§16, §17) | 1,419 |
| Exposure ∩ *union* outcome (link 1 only) | 1,948 |
| Exposure ∩ fertility ∩ identification vocabulary | 87 |
| Exposure ∩ fertility ∩ elder-support vocabulary | 124 |

Three readings, all of which the scope above anticipated and one of which it can now size.

**The literature stops before the birth.** The union-outcome frame is nearly twice the fertility frame
— 1,948 against 1,012. §3 predicted this and §8 gives it a cell (`LINK1_ARRANGEMENT_TO_UNION`); the
ratio says the link-1 cell is where the mass of this field actually sits.

**The identified sub-frame is 87 records, 8.6% of the screenable frame** — and that is a generous
upper bound, since matching an identification word in an abstract is not the same as identifying off
admissible variation in the sense of §3. The §4 enumeration of eight designs exists because this
number is small enough that finding the real ones cannot be left to a broad query.

**The homonym is 12.3% of the frame on vocabulary, and that understates it.** 124 of the 1,012 records
carry elder-support vocabulary, and 104 of the co-residence sub-cloud's 632. But §6's point is exactly
that the vocabulary does not separate the constructs — a record about a young couple living with a
healthy parent-in-law who minds the baby carries none of these words. The 12.3% is the share the
*screen* can see, not the share that is there.

**Amended 2026-08-27:** the block below is the vocabulary as first frozen, and it was missing the
emancipation family — see §16. The numbers here are the pre-amendment measurements, kept so the
correction is auditable.

Each exposure term was also scored alone against the fertility axis rather than trusted inside a block
(the A.17 lesson, where one anchor term carried 94% of a block's contamination). `"parental home"`
(213), `"household formation"` (168) and `"co-residence"` (155) carry the frame; `"nest leaving"` (8)
and `boomerang` (24) are nearly free to include and are kept for recall rather than yield. Full
term-by-term counts in `co-residence-parents-household-delay-frame-probe.json`.

*Correction to the ticket's opening estimate.* TICK-075 records ~361 records for this frame, from a
one-shot probe run on a narrower vocabulary at the time the hypothesis was chosen. The measured frame
is **1,012**. The ordering that selected A.23 as the smallest remaining hypothesis was made on
like-for-like narrow probes across candidates and is not disturbed, but the number in the ticket is
superseded by this one.

### Posture

The C.2.c and D.3.b posture is adopted: **a thin identified evidence base is an acceptable result, not
a search failure.** The seed harvest and the frame probe agree on the shape — a large, high-quality
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

**The v5 seminal field has already been put through the gate, with a result worth recording.**
Reher 1998 resolves (`10.2307/2807972`) but is a cross-national family-system typology — theory and a
Wall-3 decoy, not an empirical anchor. Fokkema and Liefbroer 2008 resolves
(`10.4054/demres.2008.19.36`) but is descriptive trends in living arrangements with no fertility
estimate — a `LINK1_DRIVER_TO_ARRANGEMENT` record. **"Baizan 2006" does not resolve**: no 2006 work by
that author about co-residence or home-leaving was found, and the 2006 records under the name are about
temporary contracts and Spanish fertility, which is C.5.a's subject. It is recorded as `UNRESOLVED`,
not as absent — it may be a chapter or working paper outside the index, or a mis-citation — and flagged
to TICK-001. So **none of the three works the master list offers as seminal is an empirical anchor for
this chapter's primary cells**, which is itself a signal about how thin the identified core will be.

*(Method note, since it nearly produced a false negative: the unaccented query `Baizan` returns 2
records and the accented `Baizán` returns 362. The accent-folding defect logged on D.1.a is live in
this chapter's author space, and every author query here must be run accented.)*

Every anchor clears the mandatory existence-verification gate — a live DOI or a Crossref/publisher
record — before entering any recall denominator. **No anchor is hand-asserted from memory**, the three
works in the v5 `seminal` field included; they are candidates to verify. The anchor set must carry
deliberate off-cell decoys: price-identified housing studies (C.2.c), elder-support co-residence
(the §6 homonym), cross-national family-regime comparisons (D.2.b), and home-leaving studies whose
outcome is not a birth.

> **Ruling 2 — the pre-modern niche stays in A.7. (Shravan, 2026-08-27; PI confirmation pending.)**
> C.2.c's scope flagged, without annexing it, that the European marriage pattern rests on identical
> logic: marriage waited on the availability of a *niche* — a farm, a holding, a dwelling — so
> household formation gated fertility through nuptiality. The parallel is exact rather than
> approximate, and A.23 stays scoped to the SDT: the PM mechanism remains A.7's, and A.23 cites it.
> Recorded so the review does not later rediscover it as a gap, and so the decision is deliberate
> rather than an omission. The practical consequence for this chapter is small but real — **a
> pre-modern niche study is not an A.23 anchor, and belongs in the decoy set** for the routing test.

## 13. What the anchor sourcing found (2026-08-27)

Channels 1, 2 and 5 have been run (`214_a23_anchor_sourcing.py`, `215_a23_targeted_anchor_pulls.py`)
and 30 anchors have cleared the Crossref existence gate (`216_a23_verify_anchors.py`): 30 FOUND, 0
UNRESOLVED, 0 ERROR. Verification is against Crossref rather than OpenAlex, which is where the
candidates came from. Two results change how this chapter should be read.

### Channel 1 is dry, and that is a finding

**No prior systematic review, scoping review or meta-analysis of the living arrangement and fertility
exists.** The review-vocabulary families return 25, 5 and 0 records, and reading them shows the hits
are off-topic — a handbook of adolescence, a scoping review of loneliness in parenthood, a systematic
review of in-work poverty. A second vocabulary was tried before concluding this, per the C.3.g lesson:
the bare word `review` returns 83 and `"research agenda"` 4, and neither surfaces a synthesis of this
question. The nearest thing the field has is Furstenberg's *On a New Schedule* (`10.1353/foc.0.0038`),
a narrative review of the transition to adulthood.

So this chapter has **no external-authority anchor source**, and the cross-validation floor cannot be
met from channel 1. Recall has to be established from channels 2, 3 and 5 and from the C.2.c seed
harvest. Note also a vocabulary artifact worth carrying forward: `"systematic review" AND "household
formation" AND fertility` returns **0**, while the same query with the bare word `review` returns 12.
The zero is a property of the phrase, not of the literature.

### The identified evidence is almost entirely in the arm the registered claim does not name

Of the 20 gold candidates, **16 are `PRIMARY_EXTENDED_COUPLE` and 3 are `PRIMARY_PRELAUNCH`**. More
sharply: every identified design that survived sourcing is in the extended-household arm. Design 8 —
grandparental availability shocks from pension and retirement-age reform — yields six anchors with
credible exogenous variation (`10.1016/j.jpubeco.2023.104928`, `10.1093/cesifo/ifu030`,
`10.1086/719161`, `10.1016/j.econlet.2025.112239`, `10.1007/s10797-023-09822-9`,
`10.2139/ssrn.2420716`). The pre-launch designs return almost nothing: the housing-benefit age
threshold family returns 3 records, administrative dwelling allocation 2, and dwelling-destruction
shocks 5.

The asymmetry has three consequences.

**It vindicates Ruling 1 immediately, and for a reason the ruling did not anticipate.** The ruling was
taken to avoid selecting on the sign. What the sourcing shows is stronger: had the chapter been
restricted to the pre-launch configuration, it would have had **essentially no identified evidence at
all**. The identified evidence that exists is in the arm the v5 claim does not name — and it runs the
other way, since grandparental availability *raises* fertility.

**It relocates the chapter's centre of gravity.** A.23 as registered is a story about young adults
failing to launch in Southern Europe. The evidence base is mostly about grandmothers in China, Italy
and Germany deciding whether to retire. Both are "co-residence with parents"; §5 and §6 are the reason
they are not the same variable.

**It sets up the §7 verdict now rather than at synthesis.** The pre-launch arm — the registered
hypothesis — is heading for a low GRADE on sparse and mostly associational evidence, while the
extended-household arm may support a moderate rating on an effect of the opposite sign. A chapter that
reported a single A.23 verdict would have to average those, which is exactly the error the review has
already ruled against: ask whether disagreeing estimates share an estimator before pooling them, and
here they do not even share a population.

### Reading the gate's output

Two anchors were flagged for low title overlap and both are subtitle truncations in what we recorded,
not mismatches — the standing caution that a title-stem index makes a correct anchor look wrong. One
of them earned its flag for a different reason: reading the resolved title of `10.1016/j.socscimed.
2003.10.003` showed the outcome is "stress and health behaviors", not fertility, so it was
reclassified out of the gold set and into the decoy set. **The gate's value here was not the DOI
check — every DOI resolved — it was reading what came back.**

## 14. Status of the two arms after sourcing and snowball (2026-08-27)

Three independent measurements now agree, and they change what this chapter is going to be able to
say. Recorded here so the synthesis stage inherits it rather than rediscovering it.

| | Pre-launch arm (the registered claim) | Extended-household arm |
|---|---|---|
| Gold candidates from anchor sourcing | 3 | 16 |
| Identified designs surviving sourcing | ~0 | 6 (pension / retirement-age variation) |
| Citation cloud reached | 1,260 records | 809 records |
| Records pairing exposure with a fertility outcome | **6 (0.5%)** | 3.8% |
| Predicted sign | negative | positive |

The pre-launch arm is the hypothesis as registered, and it is the arm with almost no evidence. The
extended-household arm has the evidence, the identification, and the opposite sign. §7's verdict will
be configuration-conditional not as a refinement but because there is no single quantity to report.

**The chapter is not split.** The profile — different signs, different literatures, different evidence
volumes — is the one that usually argues for two chapters, and the review's standing rule is that a
split belongs at synthesis unless the splitting field is visible at title/abstract. Here it is not:
§6 established that the life-stage configuration is a full-text fact. So the split stays where Ruling
1 put it, as two pooled cells in one chapter.

**The remaining route to pre-launch evidence is channel 5**, the eight named designs of §4. The
citation channel has now failed for that arm twice, for a measured reason, and a third round would be
spending against a known result.

## 16. Channel 5, and the word the frame was missing

The named-design pass (`221_a23_channel5_prelaunch.py`) ran all eight designs of §4 with **two
vocabularies each** and with the fertility axis both required and relaxed. Almost all of it is noise:
designs 3, 4, 5 and 6 return nothing usable, and design 7's sibling-instrument literature is about
educational attainment, not home-leaving. Designs 1 and 2 returned **one study**, and it is the single
most important record this chapter has found.

### Aparicio-Fenoll and Oppedisano (2014), *B.E. Journal of Economic Analysis & Policy*

`10.1515/bejeap-2014-0003`, "Fostering Household Formation: Evidence from a Spanish Rental Subsidy".
Spain introduced a monthly cash subsidy in 2008, worth about 20% of a young adult's average wage,
**conditional on renting accommodation**. The paper exploits the **eligibility age threshold** in a
difference-in-differences design and estimates effects on the probability of living apart from
parents, of living with a romantic partner, **and on childbearing**, comparing 22-year-olds with
21-year-olds. Effects are positive on all three and larger for lower earners and in high-rent areas.

That is the entire causal chain — treatment → living arrangement → union → birth — identified in one
design, on the configuration the registered hypothesis names. Against a pre-launch citation cloud of
1,260 records that yielded six title-level candidates and no identification, one paper of this shape
is worth more than any count: the boundary-spanning design beats the cross-literature tally.

It routes to `MIXED_PRICE_ARRANGEMENT` under Wall 1's sub-ruling — a subsidy conditional on
establishing an independent residence is a price change *and* an arrangement instrument — so it is
reported to C.2.c as unallocated rather than silently claimed here. The sub-ruling was written before
this study was found; the case is now real rather than hypothetical, and that is what the second read
on Wall 1 has to settle.

### The frame was missing a word, and it was the word the setting uses

Design 1's first vocabulary — "housing benefit", "shared accommodation rate", "local housing
allowance" — returned **one** record, and it was irrelevant. The second vocabulary — "eligibility
age", "age cutoff", "age discontinuity" — returned the Spanish study. Neither the study's title nor
its abstract contains any of this scope's frozen exposure terms. What it says is **emancipation**.

That is the standard term in the Spanish and Italian literature, which is exactly the setting A.23 is
about — and it was not in the exposure block. The cost is measurable:

| Exposure vocabulary ∩ fertility axis | records |
|---|---|
| As frozen in §11 | 1,012 |
| Plus `emancipation`, `"living apart from parents"`, `"living independently"` | **1,419** |
| `emancipation` and `"living apart from parents"` alone | 385 |

A 40% frame expansion from three phrases — which looked like a fix, and was not. **See §17: the
calibration showed the bare word `emancipation` is a homonym and the family has been removed again.**
The two things worth keeping from this episode are below; the vocabulary change itself is reversed.

Two things to carry, beyond the fix. **A design can be named correctly and still be unfindable**: §4
named "youth housing allowances conditional on independent residence" and the query built from that
description found nothing, because policy literatures are indexed in the vocabulary of the country
that ran the policy. And **the second vocabulary is not a formality** — this chapter has now produced
two instances where it changed the answer, the review-phrase zero in §13 and this one.

### Status of the pre-launch arm, revised

The arm is not empty. It has one identified study that spans the whole chain, plus three or four
observational records, against sixteen in the extended arm. That is a thin, honest evidence base, and
under §11's posture it is the right result rather than a reason to loosen a wall. The GRADE rating for
the pre-launch arm will rest substantially on this one paper, and the risk-of-bias pass should treat
it accordingly: an eligibility-age discontinuity compares 22-year-olds with 21-year-olds, which is a
narrow window on a hypothesis about a decade-long delay.

## 17. The production query, and what calibrating it found

`222_a23_production_query.py` builds the two-axis CAUSE × FERTILITY query required by the 2026-06-20
decision — the boolean layer optimises recall, the LLM screen optimises precision — and calibrates it
with a **per-anchor membership test**: for each gated anchor, ask OpenAlex whether that exact work is
inside the query's result set. A record either matches or it does not, so recall is measured, not
sampled.

### The first calibration failed, and the failure was the finding

V1 reached **78.9%** of gold. Four gold anchors were missed, all extended-household, all grandparent
studies. Reading their abstracts settled it in the other direction from the one expected: **none of
the four contains any co-residence language at all.** "Fertility and parental retirement" exploits a
Dutch pension reform; the exposure is the grandmother's *time*, and the living arrangement never
appears. The same for the Italian and Australian retirement-age papers and the grandparental-investment
studies.

Under the what-varies rule inherited from C.2.c, that is not A.23's variation — it is C.2.a's, the
availability of (informal) childcare at a given living arrangement. **The query was right and the
classification was wrong.** `223_a23_exposure_audit.py` re-ran the test over every anchor
mechanically: 8 of 19 gold candidates carried no arrangement exposure, and all eight are now routed to
`OFF_CHILDCARE_C2a` and kept as cross-references and decoys.

This is worth stating plainly because it changes the chapter, not just the anchor file. **The
extended-household arm's apparent six identified designs are mostly not about A.23's exposure.** The
snowball log already warned that the identified-design count might overstate the fertility evidence;
the mechanism turns out to be worse than that — those designs are not measuring this hypothesis's
treatment at all.

A second defect surfaced in the same pass: `gold_status` was assigned by testing for a `PRIMARY`
prefix on the cell name, which silently excluded `MIXED_PRICE_ARRANGEMENT` — that is, it excluded
Aparicio-Fenoll and Oppedisano, the one identified pre-launch study, from every recall denominator.
Fixed.

### The adopted query

On the corrected gold set (12 at the time of writing, 11 after the ninth reclassification below), the variants reach **100%**:

| Variant | frame | gold recall | decoys admitted |
|---|---|---|---|
| V1 full (with emancipation) | 2,200 | 100% | 3/5 |
| **V2 no emancipation — adopted** | **1,711** | **100%** | 3/5 |
| V3 plus a union outcome | 2,823 | 100% | 3/5 |
| V4 outcome axis only | 622,829 | 100% | 5/5 |
| V5 qualified emancipation | 1,715 | 100% | 3/5 |

**V2 is adopted**: full recall at the smallest frame that achieves it. V3's extra 1,112 records buy no
recall, and the union-outcome stream is better served as a separate link-1 pull than by widening the
primary query. V4 is the outcome-only arm, run because a conjunction can be dominated by one of its
arms — here it is not: the conjunction keeps all the gold and cuts the frame by a factor of 364.

### The emancipation family is removed, and the last turn's conclusion with it

§16 recorded a 40% frame expansion from adding `emancipation` and reported it as a fix. Measuring what
those records *are* reverses that. The 489 records the bare word reaches alone are slave emancipation,
female emancipation, care-leaver emancipation and oocyte-vitrification-as-women's-emancipation. It
adds **zero** gold. And the study it was added for is reachable anyway — through `"household
formation"`, which its abstract does contain. Qualifying the word to `"youth emancipation"`,
`"residential emancipation"` and `"emancipation of young people"` recovers 4 records.

**Frame growth is not frame gain.** The right test for a candidate term is not how much it adds but
what it adds and whether any of it is gold, and that test was available before the term went in.

What survives from §16 is the real finding: the Spanish study was found by the *design* vocabulary
("eligibility age", "age cutoff"), not by any exposure term, and a design can be named correctly in a
scope and still be unfindable through the mechanism's vocabulary.

### A ninth reclassification, caught by the screen (2026-08-27)

Screening batch 14 turned up a duplicate of the anchor *Grandparenting and Childbearing in the
Extended Family* that carries an abstract the anchor record lacks. It shows the exposure is
**grandparents' childcare provision measured in SHARE**, not co-residence — the same error as the
other eight, and it survived the 223 audit only because that audit had nothing to read. The anchor is
reclassified to `OFF_CHILDCARE_C2a` and gold falls from 12 to **11**. Recall is unchanged at 100% on
every variant.

The generalisable point: **a title-only record cannot clear an exposure test.** 223 scored nine
anchors `NO_ABSTRACT` and left them on their titles; at least one of those was wrong in the direction
the test exists to catch. The remaining eight should be re-checked against full text at extraction
rather than trusted, and the screen — which sees duplicates the anchor set does not — is a second
channel for catching them.

### The recall figure's limitation, stated

Gold is **11 records**, against the cold-start protocol's cross-validation floor of ≥30 empirical
anchors. Channel 1 is dry (§13) so no external-authority anchors exist, and after the §17
reclassification the gold set is small. It is also not fully independent of the query: several anchors
were sourced with vocabulary that overlaps the cause axis. **100% recall on 11 partly non-independent
anchors is a weak guarantee, and should be read as "no known miss" rather than as a recall estimate.**
The screen's own outputs, and the RA gate, remain the real test.

## 18. The frame, and a second recall test the gold set could not run

`224_a23_pull_frame.py` pulled the adopted query in full. **1,715 records, 1,570 after
normalized-title dedup**, 145 duplicates collapsed. All 12 gold anchors are present, along with 23 of
the 33 gated anchors — the missing ten are the reclassified off-cell anchors and decoys, which is what
should happen.

**240 records (15.3%) have no indexed abstract.** That bucket is sized here rather than discovered
during screening, because a screener who returns NOT_RELEVANT on a title-only record has recorded
"not visible" as "not relevant" — the refusals-read-as-zeros failure in another costume. Those records
take `INSUFFICIENT_INFO` unless the title alone is decisive.

### An independent-channel recall test

Gold recall is measured on 12 partly non-independent anchors, which §17 already flagged as weak. The
frame and the 3,793-record snowball pool were built by genuinely independent channels and overlap by
only **8.1%**, so the pool can be used as a second, harder test: how many pool records that look
on-topic on their titles does the query fail to reach?

Twelve pool records pair an exposure and a fertility term in the title. **The query reaches ten and
misses two.** Both are missed for the same reason — they word the exposure as *household structure* or
*living arrangement*, neither of which is in the cause axis.

### The obvious fix was measured and rejected

| | records |
|---|---|
| V2, adopted | 1,711 |
| V2 + the living-arrangement family | 3,151 |
| That family alone, not reachable by V2 | 1,440 |
| The same, qualified with parents / young adults / grandparents | 504 |
| Gold gained | **0** |

Reading the additions says why. *Living arrangement* and *household structure* are generic demographic
terms: the 1,440 records are ageing cohort profiles, single-parent families, marital dissolution, and
children's living arrangements with one parent versus two. Even the qualified 504 is dominated by them.
An 84% frame expansion — or a 29% one — to recover two records is a precision cost the screen pays for
nothing.

**So the two records are added to the frame by hand**, from the independent channel, each through the
Crossref existence gate, each carrying `hand_added` and its reason (`226_a23_frame_supplement.py`).
Frame: **1,572**. This is auditable in a way a quietly widened axis is not — the frame's own metadata
names the records the boolean query did not produce, and the rejected expansion is recorded with its
measured cost rather than left as a judgement call.

This is the second time in this chapter that a candidate term's frame growth turned out to be the
wrong construct, after `emancipation` in §17. The rule that came out of the first case held on the
second: run the term alone, subtract what the axis already reaches, read what remains, and check
whether it moves gold.

## 15. When to adjudicate

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
