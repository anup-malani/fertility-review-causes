# Search scope — mode of production and child economic value

**Hypothesis:** C.3.a (HYPOTHESES-v5.md §C.3.a)
**Hypothesis slug:** `agricultural-mode-of-production`
**Ticket:** TICK-030 (the documented second-hypothesis GACS generalization test)
**Target phenomenon:** **PM only.** This is binding on the denominator (see "PM is a variation
phenomenon" below) and it is binding on scope: a study is in-cell only if its identifying variation is
variation in the *subsistence/production system* or in the *economic value of children* that the system
sets. Within-industrial-economy declines in child labor value belong to C.3.b and C.3.d, not here.
**Status:** DRAFT (Shravan, 2026-10-04) — causal claim, the overdetermination problem, walls,
estimand cells, and cold-start plan proposed, **not yet frozen.** Freeze requires (i) a second read on
the A.13/nutrition overdetermination ruling, which is the whole chapter, and (ii) sign-off on the
cross-society-vs-within-society pooling rule. Anchor sourcing not yet started.

---

## Causal claim

A society's mode of subsistence — foraging, horticulture, pastoralism, intensive (plough/irrigated)
agriculture — fixes two parameters of the economics of children: **how productive children are** (the
age at which a child becomes a net producer, and the value of the labor they supply before that) and
**how costly they are to raise** (the compatibility of childcare with the subsistence work the mother
must do, and the length of dependency). Where children start contributing early, contribute much, and
reach self-sufficiency young, the net cost of a child is low and the privately optimal number is high.
Where children are economically idle for years and impose a mobility or opportunity cost on the mother,
the optimal number is low. The claim is that this mechanism accounts for a substantial share of the
**observed range of completed fertility across pre-modern populations**: foragers low, intensive
agriculturalists high, with pastoralists and horticulturalists in between.

That is the claim. Its difficulty is not that the correlation is missing — the cross-cultural
correlation between subsistence intensity and fertility is one of the better-documented facts in
anthropological demography. Its difficulty is that **the correlation is overdetermined**: at least
three mechanisms predict it, only one of them is C.3.a's, and the raw forager–agriculturalist gap is
consistent with any of them. Separating them is the whole chapter.

## PM is a variation phenomenon — the denominator is a range, not a change

Per PROTOCOL §4.2.1, the PM denominator is the **observed range of completed fertility across
pre-modern populations**, a range rather than a change. The demographic-significance question for C.3.a
is therefore: *of the spread in completed fertility across pre-modern societies — roughly ~4 to ~8
children ever born across the ethnographic record — what fraction is attributable to differences in
mode of production, net of the biological and ecological channels that co-vary with it?* A share of a
*decline* (the FDT/SDT framing) is a category error here, and so is any number computed against a
single society's time series unless that series spans a genuine mode-of-production transition.

## The forager–agriculturalist gap is overdetermined — and this is the whole chapter

The organizing empirical fact is that mobile foragers have **longer birth intervals and lower completed
fertility** than settled agriculturalists. C.3.a reads this as the child-economic-value mechanism. But
the same gap is predicted, from the same societies, by two non-economic mechanisms that the review
houses elsewhere:

- **The lactational-amenorrhea channel (A.13 / `breastfeeding-lactational-amenorrhea`).** Mobile
  foragers nurse intensively and on-demand for 3–4 years because they have no weaning foods and must
  carry the child; intensive nursing suppresses ovulation and lengthens birth intervals *mechanically,
  with no reference to the value of child labor at all.* Settled agriculturalists wean earlier onto
  cereal gruels and conceive sooner. This is a **biological proximate determinant**, and it predicts
  exactly the forager-low / farmer-high pattern C.3.a claims.
- **The energy-balance / nutrition channel (B, `nutrition-energy-availability`).** Foragers'
  higher energy expenditure and more variable food supply depress fecundity and raise fetal loss
  relative to grain-storing agriculturalists. Again: same predicted gap, no economics.

**Consequence 1 — a bare cross-subsistence fertility correlation identifies nothing.** A study showing
that farmers out-reproduce foragers, with no design that strips out the nursing and energetics
channels, is **topical but off-cell**: it documents the explanandum, not the C.3.a mechanism. This is
the direct analog of the housing chapter's rule that an aggregate price–fertility correlation is not
evidence on the cost channel; here the confounds are biological rather than a wealth offset, but the
logic is identical.

**Consequence 2 — the identifying evidence for C.3.a is evidence on the *value* channel specifically.**
The studies that can carry the chapter are the ones that measure the economic mechanism directly and
show it moves fertility *holding the proximate determinants fixed or controlled*: time-allocation and
energetics studies measuring children's **net production by age** across production systems (Kaplan,
Kramer, Lee); studies of **within-society mode-of-production transitions** (sedentarization,
agricultural intensification, adoption of plough or cash crops, land settlement) where the nursing and
nutrition regime can be tracked alongside the production change; and cross-cultural studies that enter a
**direct measure of child labor value or dependency length** rather than subsistence category as a bare
dummy.

**Consequence 3 — A.13 and C.3.a are not additive, and their boundary is a routing wall, not a
caveat.** If part of the forager–farmer gap is nursing and part is child-labor-value, the two shares
sum to the gap and cannot both be counted in full. This is the same non-additivity hazard flagged at
A.10→A.7 (TICK-054) and C.2.c→A.23 (housing Wall 2); it is folded into that standing escalation rather
than raised fresh. The practical rule: a forager–farmer fertility difference whose mechanism is not
pinned is reported to **both** C.3.a and A.13 as unallocated (`MIXED_VALUE_NURSING`), never booked in
full to either.

## The Boserup simultaneity — the reverse-causal threat that mirrors the hypothesis

C.3.a says mode of production → fertility. Boserup's own thesis (1965), the chapter's seminal citation,
runs the arrow the **other way**: population density drives agricultural intensification. Higher
fertility and density raise the labor available and the pressure on land, which *induces* the shift from
long-fallow to intensive cultivation. So subsistence intensity and fertility are **jointly
determined**, and the cross-sectional correlation is contaminated by simultaneity in exactly the
direction that would manufacture C.3.a's result with the causation reversed. A design that cannot break
this loop — most cross-sectional ethnographic comparisons cannot — can document the association but may
not call it evidence that the production system *caused* the fertility level. Studies exploiting an
**exogenous shock to the production system** (an imposed settlement scheme, an irrigation project, a
cash-crop introduction, a technology adoption driven by something other than local population pressure)
are the ones that address the threat, and must be graded up accordingly.

## The boundary walls

Each wall is drawn on **what varies**, per the housing-chapter rule, not on the mechanism the author
narrates. The frame-probe boundary counts (2026-09-13) are shown where measured.

**Wall 1 — C.3.a vs A.13 (`breastfeeding-lactational-amenorrhea`): the overdetermination wall. The one
that matters most.** Covered in full above. Discriminator: does the estimate identify the **child
economic-value / dependency** channel (directly measured, or with the nursing/energy regime held
fixed), or does it ride on a bare subsistence–fertility gap that the nursing channel predicts equally
well? The latter is `MIXED_VALUE_NURSING`, reported to both.

**Wall 2 — C.3.a vs B (`nutrition-energy-availability`): the energetics confound.** Same gap, maternal
energy-balance channel. Discriminator: variation in the **production/subsistence system and the child
labor value it sets** (C.3.a) vs variation in **caloric intake / energy expenditure / nutritional
status** as the treatment (nutrition-energy). A study whose regressor is food energy or maternal
condition is not C.3.a's even if subsistence mode is the ultimate cause of the nutrition difference.

**Wall 3 — C.3.a vs C.3.b (`child-labor-laws-and-schooling`): level-across-systems vs policy-shock.**
Both are child-economic-value hypotheses. C.3.a owns the **pre-modern cross-production-system level**
set by the subsistence technology; C.3.b owns the **within-industrializing-economy decline** driven by
compulsory-schooling and child-labor law. Discriminator: variation in subsistence/production system
(C.3.a) vs variation in child-labor law or school-leaving age (C.3.b). Frame-probe boundary: 6 records
— the vocabularies barely overlap, as expected.

**Wall 4 — C.3.a vs C.3.d (`quantity-quality-tradeoff`): levels vs decline, already drawn in v5.** The
v5 `notes` field states it: "Mode of Production explains baseline fertility *levels* across production
systems; QQ explains the *decline* within industrializing economies as returns to human capital rise."
Discriminator: cross-production-system variation in child labor value (C.3.a) vs variation in the
**return to human-capital investment per child** (C.3.d). A study of rising returns to schooling is
C.3.d even in an agrarian setting.

**Wall 5 — C.3.a vs C.3.f (`wealth-flows-reversal`): the level vs the reversal.** Caldwell's wealth
flows and C.3.a are close kin — both are about the net economic contribution of children. C.3.a owns
the **cross-sectional PM variation** in child productivity by subsistence mode; C.3.f owns the
**direction of net intergenerational transfers and its reversal** with modernization (an FDT story).
Discriminator: does the estimate exploit variation **across pre-modern production systems** (C.3.a) or
variation in the **net flow direction / modernization** of a transitioning society (C.3.f)? Kaplan's
embodied-capital and net-transfer measurements are the shared toolkit and will be cited by both; the
*estimate* routes on which variation it uses. Frame-probe boundary: 7 records.

**Wall 6 — C.3.a vs C.4.a (`land-and-resource-constraints-malthusian`): production technology vs the
real-wage check.** Both are PM-economic and both touch Boserup. C.4.a owns variation in **land
availability and real wages** working through the preventive/positive check (nuptiality, mortality);
C.3.a owns variation in the **production technology and the child labor value it sets**. A study
exploiting real-wage or land-per-capita variation → nuptiality is C.4.a; one exploiting the
subsistence-system → child-productivity difference is C.3.a. The Boserup simultaneity lives on this
wall, because density → intensification is the mechanism that joins them.

**Wall 7 — C.3.a vs C.2.g (`urbanization-residential-shift`): cross-system vs the rural–urban shift.**
Urban children are economically idle and rural children are not, so urban–rural fertility gaps are
partly a child-labor-value story. Discriminator: C.3.a requires variation in the **production system
itself** (forager/pastoral/agricultural); a **rural-versus-urban** comparison within a modernizing
economy, or a residential-composition shift, is C.2.g — which already names the economic value of
children in urban vs rural production as one of its own channels. Frame-probe boundary: 23 records.

**Wall 8 — C.3.a vs C.1.a (`income-effect-normal-good`): cross-feed, not a route.** Intensive
agriculture is both a different production technology *and* a higher-income regime, so a farmer–forager
fertility gap confounds the value channel with a pure income effect. C.3.a owns the value channel; where
a study can isolate an income movement at fixed production technology it is fed to C.1.a as evidence.
Note this cuts against the hypothesis: the income effect on children-as-normal-good predicts the *same*
sign as the value channel across the subsistence gradient, so it is a fourth overdetermining route, not
an offset.

## Estimand cells

| Cell | Treatment / variation | Fertility outcome | Routing |
|---|---|---|---|
| `PRIMARY_VALUE_DIRECT` | Direct measure of children's net production / age-specific labor value / dependency length, varying by production system, linked to fertility | Completed fertility, CEB, birth interval | Primary synthesis — the value-channel core |
| `PRIMARY_TRANSITION` | Within-society mode-of-production change (sedentarization, intensification, plough/irrigation/cash-crop adoption, settlement scheme) with nursing/nutrition trackable | Fertility change across the transition | Primary synthesis, highest-identification stratum |
| `PRIMARY_CROSS_SYSTEM_CONDITIONED` | Cross-cultural subsistence–fertility estimate that **controls for or holds fixed** the nursing and energy channels, or enters a direct child-value measure | Completed fertility / CEB | Primary synthesis |
| `BARE_CROSS_SYSTEM` | Cross-cultural subsistence category → fertility, no nursing/energy control, no direct value measure | Fertility | Documents the explanandum; **not pooled as C.3.a evidence** (overdetermined) |
| `MIXED_VALUE_NURSING` | Forager–farmer gap, mechanism unpinned between value and lactational amenorrhea | Fertility | Primary, flagged unallocated; also reported to A.13 (non-additive) |
| `CHILD_LABOR_NO_FERTILITY` | Children's production / time allocation measured, **no fertility outcome** | None | Mechanism / context stream |
| `MODE_OF_PRODUCTION_THEORY` | Boserup/embodied-capital/behavioral-ecology models of subsistence and family size | No empirical fertility estimate | Theory stream |
| `OFF_NUTRITION_B` | Caloric intake / energy balance / nutritional status as treatment | Fertility | Route to `nutrition-energy-availability` |
| `OFF_NURSING_A13` | Breastfeeding duration/intensity as treatment, no production-system variation | Fertility | Route to A.13 |
| `OFF_CHILD_LABOR_LAW_C3b` | Child-labor law / compulsory schooling as treatment | Fertility | Route to C.3.b |
| `OFF_QQ_C3d` | Returns to human capital / quality investment as treatment | Fertility | Route to C.3.d |
| `OFF_WEALTH_FLOWS_C3f` | Net transfer direction / modernization reversal as treatment | Fertility | Route to C.3.f |
| `OFF_LAND_WAGE_C4a` | Land availability / real wage as treatment → nuptiality or check | Fertility | Route to C.4.a |
| `OFF_URBAN_C2g` | Rural–urban or residential-shift comparison | Fertility | Route to C.2.g |
| `OFF_OUTCOME` | Mode of production → some non-fertility outcome (growth, nutrition, labor supply, migration) | None | Context only |
| `OFF_OTHER` | Non-C.3.a fertility determinant, no sibling home | Fertility | Route out |
| `REVERSE` | Fertility / population density → agricultural intensification (the Boserup direction) | Intensification outcome | Context — the identification threat itself; retain and count |
| `INSUFFICIENT_INFO` | Cannot be routed on the visible record | Unknown | Pairs only with `UNCERTAIN` |

## Required tags on every included empirical effect

- `SUBSISTENCE_MODE` — forager / horticulturalist / pastoralist / extensive-agriculturalist /
  intensive-(plough or irrigated)-agriculturalist / transitional, and how coded.
- `DESIGN_UNIT` — cross-society (ethnographic sample) / within-society transition / single-society
  age-production study. Within-society transitions are materially stronger; grade accordingly.
- `CHILD_VALUE_MEASURE` — direct energetics / time-allocation / net-transfer accounting / proxy
  (e.g., bare subsistence dummy). A `BARE_CROSS_SYSTEM` effect has no direct measure by definition.
- `PROXIMATE_CONTROLS` — does the design hold fixed or control the nursing channel (A.13) and the
  energy channel (nutrition)? List which. This tag is what separates `PRIMARY_CROSS_SYSTEM_CONDITIONED`
  from `BARE_CROSS_SYSTEM`.
- `OUTCOME_MEASURE` — completed fertility / CEB / TFR / birth interval / age-specific fertility.
- `IDENTIFICATION` — exogenous shock to production system / within-society panel / cross-section only;
  and whether the Boserup simultaneity is addressed (`REVERSE`-direction threat).
- `NON_INDEPENDENCE` — is Galton's problem (cross-cultural non-independence from shared descent or
  diffusion) addressed by a phylogenetic, regional, or spatial control? Required on every cross-society
  estimate.
- `DATA_SOURCE` — SCCS / Ethnographic Atlas / D-PLACE / single-society fieldwork / historical
  parish or census demography.
- `PERIOD_AND_PLACE` — recorded even though the phenomenon is PM, so ethnographic-present and
  historical estimates stay separable.

## Identification threats (what the risk-of-bias pass is looking for)

1. **Overdetermination by proximate determinants (Walls 1–2).** The headline gap is predicted by
   lactational amenorrhea and by energy balance independent of any economic value. A design that does
   not strip these out is not evidence on C.3.a's mechanism. This is the primary threat and the reason
   `BARE_CROSS_SYSTEM` is not poolable.
2. **Boserup simultaneity / reverse causation.** Density and fertility drive intensification; the
   cross-section is contaminated in the direction that fakes the result. Only exogenous production-system
   shocks, or within-society designs that establish timing, address it.
3. **Galton's problem.** Societies in a cross-cultural sample are not independent draws — they share
   ancestry and borrow from neighbors, so a raw cross-cultural correlation overstates its own
   significance and can be an artifact of a few cultural lineages. Proper tests require phylogenetic or
   spatial autocorrelation controls (Mace & Pagel; the D-PLACE toolkit). Record whether the design has
   them.
4. **Ecological bundling.** Mode of production travels with climate, disease burden (B.3), soil,
   market access, and kinship (D). Regional subsistence variation is close to a summary statistic for
   the whole ecological package, not an isolated treatment.
5. **Income confound running the same way (Wall 8).** The normal-good income effect predicts the same
   cross-gradient sign, so it adds to the overdetermination rather than offsetting it.
6. **Optimal vs realized fertility.** The economic mechanism acts on *desired/optimal* fertility;
   realized fertility is filtered through the proximate determinants. A study measuring desired family
   size by subsistence mode speaks to the mechanism but not directly to the completed-fertility
   denominator, and vice versa. Record which the outcome is (`OUTCOME_LEVEL`-style: desired vs realized).

## Evidence-base posture

**A theory-heavy chapter resting on a thin directly-identified core is the expected and acceptable
outcome**, by the same posture taken on C.2.c and D.3.b. The topical literature is large
(frame-probe union frame 1811; "mode of production INTERSECT fertility" = 112), but most of it is
`BARE_CROSS_SYSTEM` or `CHILD_LABOR_NO_FERTILITY`, and the directly-identified value-channel evidence —
energetics/time-allocation studies that reach a fertility outcome, and clean within-society transition
studies — will be a small set. The shrinkage of the pools under the overdetermination wall is the
correct result, not a search failure, and the **count of studies that survive it is itself a finding
about the field** and belongs in the chapter beside the denominator. Do not loosen Wall 1 to rescue the
pool.

## Cold-start channels and leakage wall

1. Prior reviews / meta-analyses / syntheses of subsistence and fertility and of cross-cultural
   fertility variation (behavioral-ecology and anthropological-demography reviews) → empirical anchors
   by external authority. *(Leakage wall: a review's search strings may feed query terms and its
   included studies may feed anchors, but never the same study to both.)*
2. Top-down theory/canon enumeration — Boserup intensification, Kaplan embodied-capital and
   intergenerational transfers, Lee & Kramer net-production models, Sellen & Mace / Gibson & Mace
   cross-cultural tests, Kramer on children's help — seeds the theory set. Does not count toward
   empirical recall.
3. Citation snowball from the channel-1 and channel-2 seeds → the orthogonal Tier-B frame.
4. Broad single-query search plus a structured screen, **only if** the gold is still under the
   cross-validation floor (≥ 30 empirical anchors). Given the thin directly-identified core, this
   channel is likely to be needed; Tier B is never drawn from it.
5. Production-query terms are fold-local once the gold frame exists — never mined from a paper and then
   evaluated on it.

## Pre-query anchor audit (not yet built)

The verified anchor set will be stored in `agricultural-mode-of-production-cold-start-anchors.json`.
Every anchor clears the **mandatory existence-verification gate** — a live DOI or a Crossref/publisher
record confirming the title exists — before it enters any recall denominator. **No anchor is
hand-asserted from memory**, the four v5 `seminal` works included: they are candidates to verify, not
anchors. This is the standing rule from the 2026-07-08 OAS run that found ~40% of a frozen Tier B was
fabricated snowball citations.

The anchor set must deliberately carry **off-cell decoys** so the eventual query is tested on routing,
not only topical retrieval. The decoys that matter most, in order:

1. **A.13 breastfeeding / lactational-amenorrhea studies** on the same forager–farmer populations —
   Wall 1 is the chapter's central failure mode, so these are the load-bearing decoys.
2. **Nutrition / energy-balance fecundity studies** (Wall 2).
3. **C.3.b child-labor-law / compulsory-schooling studies** (the FDT policy channel).
4. **C.2.g rural–urban fertility comparisons** attributing the gap to child labor value.
5. **Boserup-direction studies** (density/fertility → intensification), which are the `REVERSE` cell and
   the identification threat in one.
