# Search scope — postmaterialism, individualism, and secularization

**Hypothesis:** D.1.a (HYPOTHESES-v5.md)
**Hypothesis slug:** `postmaterialism-individualism-secularization`
**Target phenomenon:** SDT primary. FDT-era evidence is admitted on the ruling below. PM is not
annexed; see "A note on the pre-modern baseline."
**Status:** DRAFT (Shravan, 2026-08-03). Five strata, an admissible-design ladder with pre-committed
GRADE ceilings, a measure-content rule, a pooling rule, and eleven walls are proposed and **not
frozen.** Freeze requires PI sign-off on Ruling 2 (the measure-content bar) and Ruling 3 (the design
ladder), because both can lower the chapter's rating before a single study is read. Cold-start
anchor sourcing has not begun.

This scope is the artifact that opened D.3.b, A.10, and C.2.c, applied to the hardest causal case in
the master list. The ticket brief that specifies it is recoverable at
`git show eecf024:tickets/TICK-060-d1a-search-scope.md`; the work is now carried by TICK-062 under
the one-ticket-per-hypothesis model.

---

## Causal claim, stated as cause → effect

**Cause:** the distribution of held values in a population shifts away from materialist, conformist,
and religiously grounded orientations, and toward postmaterialist self-expression, personal
autonomy, and secular authority.

**Effect:** desired and realized fertility fall, through three sub-mechanisms the v5 entry names:
the good life is redefined away from family formation, normative pressure to reproduce weakens, and
religious prescriptions against small families and contraception lose force.

The claim is about a shift in *values*, held by people, that changes fertility behavior at given
prices, incomes, and technology. Every routing rule below follows from that sentence. The
identifying variation has to be in values. Variation in the price of children, in the technology of
control, or in who transmits a norm to whom belongs to another chapter, however cultural the author's
narration.

---

## The problem the chapter exists to solve

D.1.a's own `notes` field concedes the difficulty: "Criticized as descriptive rather than causal and
hard to separate from income/security mechanisms." The concession is accurate and it is not a small
one. Lesthaeghe and van de Kaa documented a bundle of changes that moved together across postwar
Europe: later marriage, cohabitation, divorce, contraception, secularization, and low fertility. A
bundle that moves together is a characterization of the transition, and the Second Demographic
Transition literature has been criticized on exactly this ground for three decades, most sharply in
Zaidi and Morgan's review. A GRADE rating needs an estimand and a source of variation in the cause,
and co-movement supplies neither.

Two consequences follow, and they organize the rest of this document.

**First, the chapter must state in advance what would count as evidence.** If admissible design
classes are not fixed before the search, the screen will return several hundred papers reporting
that value indices and fertility correlate, and the chapter will have to decide after the fact
whether that constitutes causal evidence. Deciding after the fact is how a rating drifts upward.
Ruling 3 fixes the ladder now.

**Second, a very low or no-evidence verdict has to be reachable by design.** The honest possible
outcome for parts of this hypothesis is a theory-heavy section resting on almost no identified
estimates. That result is a finding about the field, and the scope is built so it can be reported
rather than engineered around. This is the same posture recorded for D.3.b's Wall 2 and for C.2.c's
evidence base, and it carries the same standing obligation: the posture governs how a thin evidence
base is *interpreted*, never whether it is *reported*.

---

## Ruling 1 — five strata, estimated separately (Shravan, 2026-08-03)

The v5 entry absorbs five sub-claims: `secular-ideational-shift`, `individualism-rise`,
`secularization-religiosity-decline`, `childlessness-as-acceptable-choice`, and
`consumerism-aspirational-lifestyles`. They are measured five different ways by five literatures with
different validity records. An effect size on one is not exchangeable with an effect size on another,
so a pooled number across them would mean whatever the measure mix in the sample happened to be. That
is the same structural defect the C.2.c tenure ruling identified, arriving through measurement rather
than through composition.

**The five strata are estimated separately and never combined into one pooled effect.** The chapter's
headline result is a stratum table, not a single elasticity.

| Stratum | Construct | Measure family | Validity note |
|---|---|---|---|
| `S1_POSTMATERIALISM` | Priority on self-expression and belonging over physical and economic security | Inglehart four-item and twelve-item batteries; WVS/EVS survival-versus-self-expression dimension | The battery is a *ranked-priority* instrument. Its scores respond to short-run inflation and unemployment, so period effects contaminate the cohort interpretation the theory needs |
| `S2_INDIVIDUALISM` | Autonomy of the individual against obligation to kin and collective | Hofstede individualism; Schwartz autonomy and self-direction; kinship-intensity indices; historical individualism instruments | The country-level indices are near-constant within a country over the study window, so they identify cross-sectionally and inherit every cross-country confound |
| `S3_SECULARIZATION` | Decline of religious affiliation, practice, and authority | Affiliation, service attendance, prayer frequency, salience, denomination | The one stratum with a large individual-level literature and with genuine natural experiments available. Expected to carry the chapter |
| `S4_CHILDLESSNESS_NORM` | Normative acceptability of voluntary childlessness | Attitude items on approval of remaining childfree; childfree self-identification | Largely barred from the causal pool by Ruling 2. Its item content is the outcome |
| `S5_CONSUMERISM` | Orientation toward acquisition and lifestyle consumption | Richins–Dawson material-values scale; consumption-aspiration measures | Thin fertility literature. Carries the vocabulary trap noted below |

**Vocabulary trap, load-bearing for the search.** The word *materialism* has opposite meanings in the
two literatures that feed this chapter. Inglehart's *materialist* prioritizes physical and economic
security, and is the pole D.1.a says fertility declines *away from*. The consumer-psychology
*materialist* is acquisitive and lifestyle-oriented, which is the S5 pole D.1.a says fertility
declines *toward*. A query built on the term without disambiguation retrieves both and scores them in
opposite directions. Handle this in the cause-axis clusters, not at screening, or it is paid for in
screening cost and in sign errors at extraction.

---

## Ruling 2 — the measure-content rule (Shravan, 2026-08-03)

**A value measure whose item content refers to children, family size, parenthood, or reproduction is
endogenous by construction when the outcome is the same respondent's own fertility.** Such estimates
are barred from the primary causal pool.

The reasoning is short. Regressing a respondent's childlessness on that respondent's approval of
childlessness estimates the consistency between a stated preference and a realized outcome. It does
not test whether a shift in values caused a shift in fertility, because the regressor is a report of
the preference whose realization is the dependent variable. A strong coefficient there is compatible
with no value change and no causal effect at all.

The rule cuts a real and populated class of studies, so it needs a precise boundary:

- **Barred from the causal pool:** own attitude toward childbearing, ideal family size, approval of
  voluntary childlessness, or childfree identification, related to the same person's fertility.
  These route to `NORM_ACCEPTABILITY_DESCRIPTIVE`, where they are reported as evidence on the
  prevalence and correlates of the norm rather than as effect estimates.
- **Admissible:** a value measure with no reproductive item content (postmaterialism battery,
  attendance, autonomy index) related to the respondent's fertility.
- **Admissible:** an *environment-level* norm measure — the community, cohort, or leave-one-out mean
  acceptability of childlessness — related to *individual* fertility. Aggregating away the
  respondent's own report breaks the definitional link and makes the estimate a social-norm effect.
  Note that such estimates then face the A.20 wall, since a norm-diffusion design may belong there.

**This is D.1.a's version of the D.3.b stratum-A finding, and it fails the same way.** Whether a
value scale contains reproductive items is a property of the instrument, reported in a methods
section, and it is invisible in a title and usually in an abstract. The D.3.b RA gate found its
decisive routing failures were precisely of this kind, and the realized pool fell from eight to five
when the gate ran. Budget an RA-gate bleed-in for D.1.a now rather than discovering it at extraction.
S4 is where it will concentrate.

---

## Ruling 3 — the admissible-design ladder, with pre-committed GRADE ceilings (Shravan, 2026-08-03)

Each design class carries the highest GRADE rating it can support, fixed before the evidence is seen.
Pre-committing the ceiling is what prevents the failure mode RA-PLAYBOOK names explicitly: a rating
that reads Moderate over studies that are all cross-sectional with no identification.

**Tier 1 — exogenous shock to the value or religiosity distribution. Ceiling: Moderate; High only
with replication across settings and designs.** The design exploits variation in values or religious
practice that is plausibly unrelated to the fertility preferences of the affected population, with
fertility measured afterward. Candidate sources: state secularization and anti-religious campaigns;
reform of church membership, church tax, or the cost of affiliation; repeal of blue laws and
Sunday-trading restrictions; clergy-scandal shocks to attendance; compulsory secular schooling
extensions; religious-market deregulation; resettlement and forced-migration episodes that mixed
value distributions.

**Tier 2 — value measured before the outcome, with the environment held fixed. Ceiling: Low.** Three
families qualify: panel designs measuring values on childless respondents and following them to
realized births; epidemiological or immigrant designs that hold host-country institutions and prices
fixed while ancestral *value* measures vary (see Wall 8 for what the proxy must contain); and
within-family or sibling designs that difference out household background. Temporal precedence and a
fixed environment are real improvements over contemporaneous correlation and are not identification.

**Tier 3 — individual-level cross-section or contemporaneous panel with controls. Ceiling: Very
low.** Values and fertility measured at the same time on the same people, with covariate adjustment.
This will be the modal included study. It documents an association.

**Tier 4 — aggregate co-movement. No causal weight; descriptive stream only.** Country-level or
region-level correlation between a value index and TFR, including the cross-national scatterplots
that constitute the canonical SDT evidence base. These enter the chapter as description of the
phenomenon to be explained, and they are not effect estimates. Three defects justify the exclusion
jointly: the unit count is around fifty with a dozen collinear covariates, GDP per capita is among
them, and countries are not independent draws because values diffuse across borders, which is
Galton's problem in its original demographic form.

**A study is rated on the design that produces the estimate, not on the sophistication of the paper
around it.** A widely cited theoretical statement supported by a scatterplot is Tier 4.

---

## Ruling 4 — period (Shravan, 2026-08-03)

**FDT-era evidence is admitted; the `phenomena` field goes to the PI.** The v5 entry scopes D.1.a to
SDT alone. Secularization is nonetheless central to FDT scholarship: the Princeton European Fertility
Project's own residual explanation was ideational, and the secularization and lay-culture markers in
that literature are measurements of exactly the S3 construct applied to the first transition. A
chapter that excluded them on period grounds would omit the largest body of evidence bearing on its
own strongest stratum.

Following the C.2.c precedent, this ruling governs *inclusion* while the per-phenomenon verdict
structure stays SDT-primary, and the field update is a PI call rather than an RA one. Every effect
carries its period regardless, so FDT-era estimates stay separable in synthesis.

**This is the third chapter in a row to hit the same restriction** — A.10, then C.2.c and its Li 2024
exception, now D.1.a. Three instances make it a master-list question rather than a third
case-by-case ruling, and it is escalated as such below.

---

## Ruling 5 — sign convention (Shravan, 2026-08-03)

**Orient every effect as the change in fertility per unit movement toward the postmaterialist,
individualist, or secular pole.** A negative sign therefore supports the hypothesis in every stratum.

The convention is not cosmetic. S3 is almost always coded in the opposite direction, since the
literature regresses fertility on *religiosity*, so most included estimates must be sign-flipped on
entry and the flip recorded. Mixing flipped and unflipped estimates in one pool is a mechanical way to
produce a near-zero pooled effect, and it is the error the A.10 sign convention was written to
prevent.

---

## Pooling rule (pre-registered)

1. **Never pool across strata.** S1 through S5 are separate estimands (Ruling 1).
2. **Within a stratum, pool only within a measure family.** Service attendance and stated religious
   salience are not two measurements of one regressor; they pool separately unless the extraction
   establishes a defensible common scale.
3. **Never pool across outcome levels.** Realized births, completed fertility, and stated intention
   or ideal family size pool separately. This is the standing D.3.b synthesis rule and it applies
   with more force here, because a large share of this literature has intentions as its only outcome.
4. **Never pool across design tiers.** A Tier 1 estimate and a Tier 3 estimate are not two draws from
   one distribution. Report tiers separately and let the reader see whether the identified estimates
   agree with the correlational ones. Where they disagree, that disagreement is a headline result.
5. **Tier 4 estimates never enter any pool.**
6. **Record the survey source on every effect and treat shared sources as non-independent.** Much of
   this literature runs on a handful of instruments: WVS/EVS, ESS, GSS, NSFG, DHS, and the national
   generations-and-gender panels. Twenty papers on overlapping WVS waves and countries are not twenty
   independent estimates. `DATA_SOURCE` is a required tag and a clustering variable in any pooled
   analysis; a random-effects model that ignores it will understate the variance badly.

---

## The boundary walls

D.1.a sits at the center of the cultural category, and four proximate entries name it as the root
cause behind them. Routing volume will be the largest of any chapter so far, and most candidate papers
will belong to a neighbor.

**Wall 1 — D.1.a vs D.3.b (`climate-anxiety-eco-doomerism`). Adopted by reference; not restated.**
The D.3.b scope's Wall 1 already specifies this boundary from the other side, and the discriminator
there is authoritative for both chapters. In brief: D.1.a covers a genuine fall in the desire for
children, D.3.b covers a live desire suppressed by ecological dread. Read the rule in
`climate-anxiety-eco-doomerism-search-scope.md`.

*General point worth recording, per the TICK-060 brief:* a wall between paired hypotheses should be
written once and referenced from the other side. Two independently drafted statements of one boundary
drift apart, and papers then satisfy both chapters or neither. Recommended as a standing convention.

**Wall 2 — D.1.a vs D.1.b (`caldwell-wealth-flows-westernization`): internal change versus external
transmission.** D.1.b covers a modernity package transmitted to societies mid-transition from
outside, through schooling, media, and development institutions. D.1.a covers value change arising
within already-modernized societies.

- **Discriminator: where is the identifying variation?** Variation in *exposure to an external
  cultural source* — media reach, missionary contact, migrant return flows, schooling that carries a
  foreign family model — routes to D.1.b. Variation in *values held within an affluent population*
  routes to D.1.a.
- Setting is a strong prior but never decides on its own. A study of secularization in contemporary
  South Korea is D.1.a; a study of Western family ideals reaching rural Nepal is D.1.b.

**Wall 3 — D.1.a vs D.1.c (`cultural-evolution-demographic-transition`): content versus transmission
dynamics.** D.1.c is a claim about *how* low-fertility behavior spreads, through prestige-biased
imitation of high-status people, and it is deliberately agnostic about which values are being copied.
D.1.a is a claim about *which* values changed.

- **Discriminator:** does the estimate turn on status or prestige asymmetry in the transmission
  process? That is D.1.c. Does it turn on the measured content of a value orientation? That is D.1.a.

**Wall 4 — D.1.a vs D.1.d (`nationalism-pronatalist-ideology`): direction and agent.** D.1.d is
state-sponsored ideology pushing fertility up. D.1.a is a diffuse secular value shift pushing it
down. A study of a pronatalist campaign is D.1.d even where it invokes traditional or religious
values, because the treatment is the campaign.

**Wall 5 — D.1.a vs D.2.a (`female-empowerment-gender-equity`): whose autonomy, and about what.**
This wall is thin and matters a great deal, because women's autonomy is a component of the
individualism construct and gender-role attitudes correlate with every S1 and S2 measure.

- **D.2.a owns** gender-specific norms: egalitarian gender-role attitudes, women's decision-making
  authority, the division of household labor, and the gender-revolution U-curve.
- **D.1.a owns** general value orientations that are not gender-specific: postmaterialism,
  individual autonomy as such, and religiosity.
- **Discriminator:** is the measured construct about *relations between men and women*, or about the
  *individual against collective obligation and religious authority*? Female education used as a proxy
  for autonomy is D.2.a's, and additionally faces Wall 9.

**Wall 6 — D.1.a vs D.2.b (`marriage-family-norms`): the value versus the institution.** D.2.b owns
norms governing marriage, union formation, and kinship structure. D.1.a owns the underlying value
shift where it is measured directly. Because the SDT literature narrates cohabitation, divorce, and
secular values as one bundle, this wall will be tested constantly.

- **Discriminator:** is the treatment a measured *value orientation*, or a *partnership behavior or
  institutional norm*? Cohabitation, divorce liberalization, and union deinstitutionalization are
  D.2.b's treatments even when the paper calls them SDT indicators.
- **Non-additivity applies here too.** Where D.1.a operates by weakening the marriage norm, D.2.b is
  the mediator and the two contributions are not additive.

**Wall 7 — D.1.a vs D.2.d (`child-centeredness-intensive-parenting`): which norm, and which
direction of cost.** D.2.d raises the cost per child through a parenting standard. D.1.a reduces the
value of children relative to competing adult goals. A study of parenting-intensity norms is D.2.d
even though both are cultural.

**Wall 8 — D.1.a vs A.19 (`intergenerational-transmission-fertility`): the demonstrated wall failure.**
A.19's seminal list contains **Fernández and Fogli 2009**, and its `notes` field claims the
epidemiological approach outright: "Epidemiological approach (Fernandez-Fogli) uses immigrants to
isolate cultural from environmental effects." That design is simultaneously the best available tool
for D.1.a's claim, since it holds prices, institutions, and markets fixed while culture varies. The
same identification strategy is therefore claimed by two chapters, which is structurally the
Lovenheim and Mumford problem C.2.c had to resolve.

- **Discriminator: what does the culture proxy contain?**
  - Ancestral-country **fertility rate** as the proxy → **A.19**. The estimate tests persistence of
    a fertility norm, and it is direction-agnostic about which values changed.
  - Ancestral-country **value measure** — religiosity, individualism index, postmaterialism score,
    kinship intensity → **D.1.a**. The estimate tests the content claim this chapter makes.
- A study using both proxies is `MIXED_CULTURE_PROXY`, reported to both chapters as unallocated.
- *Recommended master-list note for TICK-001: A.19's `notes` should record that the epidemiological
  design is a shared instrument whose routing depends on proxy content, not a possession of A.19.
  Flagged, not made.*

**Wall 9 — D.1.a vs A.3, A.6, and A.20: the root-cause-versus-proximate wall, and the chapter's
largest routing problem.** Three proximate entries name D.1.a as the root cause sitting behind them:
A.3 (diffusion and social learning of fertility control), A.6 (reduction in stigma around
contraception and abortion), and A.20 (cultural diffusion mechanisms). A.6's `notes` field says it
plainly: "the root cultural cause lives in D."

- **A.3 owns** the spread of information about and legitimation of birth control.
- **A.6 owns** the fall in stigma attached to contraception and abortion specifically.
- **A.20 owns** the *channels* of spread — networks, media reach, linguistic and community
  boundaries — independent of content, and it carries the media quasi-experiments (La Ferrara et al.,
  Jensen and Oster).
- **D.1.a owns** the change in general value content, and owns the reduced form from that change to
  fertility even where a proximate determinant mediates it.
- **Discriminator:** is the treatment a *measured value orientation* (D.1.a), a *contraceptive-specific
  attitude or legitimation* (A.6), *information about fertility control* (A.3), or *exposure to a
  transmission channel* (A.20)? Media-exposure designs are A.20's by treatment, however cultural the
  outcome, unless the paper measures the value shift itself and uses it as the regressor.

**Wall 10 — D.1.a vs C.1.a and C.5.a: the Inglehart mediation problem.** Postmaterialist value change
is theorized by Inglehart as a *consequence* of affluence and existential security. If values are
simply the channel through which rising income and security operate, then D.1.a has no independent
variation and its apparent effect is C.1.a's or C.5.a's. The v5 `notes` field flags this as "hard to
separate from income/security mechanisms," and it is the single most likely reason the chapter's final
verdict is weak.

- **Discriminator:** does the design produce variation in values that is *not* variation in income or
  economic security? An estimate that holds income and security fixed while values vary, or that
  instruments values with something other than contemporaneous affluence, is D.1.a's. An estimate
  identified off income or unemployment variation, with values narrated but not measured, belongs to
  C.1.a or C.5.a whatever the paper's framing.
- **Record on every included effect whether income and economic security were held fixed.** This is
  not a covariate note. It is the fact that decides whether the estimate speaks to D.1.a at all.

**Wall 11 — D.1.a vs C.2.h (`digital-leisure-substitution`): value versus technology.** C.2.h owns
variation in the availability and use of digital leisure. D.1.a owns the measured preference for
self-oriented consumption. Broadband rollout and smartphone diffusion are C.2.h's treatments.

*Light cross-references, no wall needed:* C.2.f (status competition in child investment), B.1
(evolutionary sex drive and contraceptive decoupling, which D.1.a's normalization of contraceptive use
feeds), and A.11 (tempo).

---

## Non-additivity: the sharpest instance in the review so far

D.1.a's effect on fertility runs almost entirely through proximate determinants that have their own
chapters: contraceptive legitimation and use (A.6, A.2, B.1), the spread of control practices (A.3),
marriage and union norms (D.2.b), and marriage timing (A.7). The chapter's reduced-form estimate and
the proximate chapters' estimates are measuring overlapping portions of the same decline, and their
demographic-significance shares cannot be added.

**This is the third recorded instance and it is worse than the first two.** A.10 → A.7 and
C.2.c → A.23 are each one hypothesis with one mediator. D.1.a is a root cause whose entire pathway is
mediated by four or five hypotheses that the review is separately crediting. If every proximate
chapter claims its share and D.1.a claims the reduced form, the shares sum past one hundred percent,
and the review's central deliverable — a per-hypothesis demographic-significance verdict — becomes
internally inconsistent at the point where a reader adds it up.

Folded into the standing TICK-054 escalation rather than raised separately, with the note that D.1.a
raises the stakes from an accounting nuisance to a structural defect in the verdict format. The review
needs a general rule that distinguishes reduced-form shares from mediated shares and states which one
each chapter reports.

---

## Estimand cells

| Cell | Treatment / variation | Fertility outcome | Routing |
|---|---|---|---|
| `PRIMARY_POSTMATERIAL_S1` | Postmaterialist or self-expression value measure | Fertility, intention, or completed parity | Primary synthesis — S1 pool |
| `PRIMARY_INDIVIDUALISM_S2` | Individualism, autonomy, or kinship-intensity measure | Fertility | Primary synthesis — S2 pool |
| `PRIMARY_SECULAR_S3` | Religiosity, affiliation, attendance, salience, denomination | Fertility | Primary synthesis — S3 pool; expected core |
| `PRIMARY_SECULAR_SHOCK_S3` | Exogenous shock to religiosity or religious institutions (Tier 1) | Fertility | Primary synthesis — S3 pool, highest-quality stratum |
| `PRIMARY_CONSUMERISM_S5` | Consumption orientation or material-values scale | Fertility | Primary synthesis — S5 pool |
| `PRIMARY_VALUE_EX_ANTE` | Any admissible value measure recorded *before* the fertility outcome, on childless respondents (Tier 2) | Realized births | Primary; the value-added cell, and the only individual-level design that breaks the reverse-causality tie |
| `NORM_ACCEPTABILITY_DESCRIPTIVE` | Own attitude toward childbearing, childlessness, or ideal family size | Own fertility | Barred from causal pool by Ruling 2; reported descriptively |
| `NORM_ENVIRONMENT_LEVEL` | Community, cohort, or leave-one-out norm acceptability | Individual fertility | Primary if it clears Wall 9 against A.20 |
| `AGGREGATE_COMOVEMENT` | Country or region value index versus TFR (Tier 4) | Aggregate fertility | Descriptive stream; never pooled |
| `MIXED_CULTURE_PROXY` | Epidemiological design using both ancestral fertility and ancestral values | Fertility | Primary, flagged unallocated; reported to A.19 |
| `SDT_FRAMEWORK_THEORY` | Statements, elaborations, and critiques of the SDT framework; value-change theory | No empirical fertility estimate | Theory stream |
| `VALUE_CONSTRUCT` | Value measures as the *object* of study — scale validation, measurement invariance, prevalence, determinants of secularization | No fertility outcome | Theory stream |
| `OFF_WESTERNIZATION_D1b` | Exposure to an external modernity package | Fertility | Route to D.1.b |
| `OFF_TRANSMISSION_D1c` | Prestige-biased or status-graded transmission | Fertility | Route to D.1.c |
| `OFF_GENDER_D2a` | Gender-role attitudes, women's autonomy, gender-equity indices | Fertility | Route to D.2.a |
| `OFF_MARRIAGE_NORM_D2b` | Partnership behavior or marriage-institution norms as treatment | Fertility | Route to D.2.b |
| `OFF_PARENTING_D2d` | Parenting-intensity norms | Fertility | Route to D.2.d |
| `OFF_PERSISTENCE_A19` | Ancestral-fertility proxy for culture | Fertility | Route to A.19 |
| `OFF_PROXIMATE_A3_A6` | Contraceptive legitimation, stigma, or information about control | Fertility | Route to A.6 or A.3 |
| `OFF_CHANNEL_A20` | Media, network, or boundary exposure as treatment | Fertility | Route to A.20 |
| `OFF_INCOME_SECURITY` | Income, affluence, or economic-security variation with values narrated but not measured | Fertility | Route to C.1.a or C.5.a |
| `OFF_OUTCOME` | Value change → a non-fertility outcome (voting, consumption, wellbeing, labor supply) | None | Mechanism / context only |
| `OFF_OTHER` | Non-D.1.a fertility determinant with no sibling home | Fertility | Route out; no sibling queue |
| `REVERSE` | Parenthood or fertility status → values, religiosity, or attendance | Value outcome | Context, and see threat 1 below |
| `INSUFFICIENT_INFO` | Cannot be routed on the visible record | Unknown | Pairs only with `UNCERTAIN` |

---

## Required tags on every included empirical effect

- `STRATUM` — S1 through S5, per Ruling 1.
- `MEASURE` — the named instrument, its item count, and whether any item carries reproductive content
  (the Ruling 2 test).
- `DESIGN_TIER` — 1 through 4, per Ruling 3, with the source of variation named.
- `SIGN_FLIPPED` — whether the reported coefficient was reoriented to the convention in Ruling 5.
- `OUTCOME_LEVEL` — realized births / completed fertility / stated intention or ideal family size.
- `TEMPO_OR_QUANTUM` — timing versus completed fertility. Secularization and value change plausibly
  act on both, and a postponement-only effect carries far less demographic significance. Cross-ref
  A.11; precedent for nesting a tempo reading under A.11 was set at TICK-038.
- `INCOME_SECURITY_HELD_FIXED` — whether income and economic security are controlled, instrumented,
  or fixed by design. Required by Wall 10; an effect without it cannot be attributed to values.
- `DATA_SOURCE` — the survey instrument and waves, for the non-independence clustering in pooling
  rule 6.
- `MEASUREMENT_TIMING` — whether values were recorded before, at the same time as, or after the
  fertility outcome. This decides Tier 2 eligibility and is the reverse-causality test.
- `PERIOD` — study window and its FDT/SDT classification under the replacement-status rule in
  PROTOCOL §2.

---

## Identification threats (what the risk-of-bias pass is looking for)

1. **Reverse causality, and it runs in the direction that flatters the hypothesis.** Having children
   raises religious participation: parents return to congregations for childrearing, community, and
   schooling. Values also adjust to realized life courses, so people who have not had children may
   report more self-oriented values partly *because* they have not had children. A contemporaneous
   religiosity-fertility correlation therefore overstates the causal effect, and the childfree
   literature is the most exposed, since value orientations there are frequently collected after the
   fertility outcome is settled. `MEASUREMENT_TIMING` exists to grade this, and it is the binding
   domain for this chapter in the way endogenous tenure was for C.2.c.
2. **Endogeneity by construction** (Ruling 2). Handled by routing rather than by grading, but any
   estimate that slips past the screen must be caught here.
3. **Common causes of values and fertility.** Education, income, urban residence, cohort, and
   migration status predict both. Education is the worst of them, because it is the most common
   covariate *and* the most common proxy for secular-individualist orientation, so controlling for it
   may absorb the mechanism while failing to control for it leaves the estimate confounded.
4. **The Inglehart mediation problem** (Wall 10) as a grading domain, not only a routing rule. An
   estimate that does not hold income and security fixed cannot separate D.1.a from C.1.a or C.5.a,
   whatever its design tier.
5. **Ecological inference and Galton's problem** on all Tier 4 material, which is why Tier 4 carries
   no causal weight.
6. **Non-independence across studies sharing a survey** (pooling rule 6).
7. **Justification bias in stated reasons.** Respondents asked why they have no children supply
   socially acceptable accounts, and self-expression is a more acceptable account than infertility or
   partnership failure. Stated-reason studies measure the acceptability of reasons alongside the
   reasons.

---

## When to adjudicate

The title/abstract screen decides only which stream a paper belongs to. It does not require the RA to
determine the design tier, the item content of the value scale, or the measurement timing.

**Three of this chapter's load-bearing facts are full-text-only.** Whether the value instrument
contains reproductive items (Ruling 2), whether values were measured before or after the fertility
outcome (Tier 2 eligibility), and whether income and security were held fixed (Wall 10) are all
methods-section facts. Expect the screen's routing to be provisional, and budget the RA gate
accordingly. The D.3.b precedent is exact and its gate cut the realized pool by nearly half.

Drafting may report only what these full-text fields support. A cross-sectional association between
secularism and low fertility, with no source of exogenous variation and no timing information,
documents an association and must not be described as evidence that the value shift *caused* the
fertility difference. Threats 1 and 3 alone are sufficient to generate that association with no causal
effect at all.

---

## Expected shape of the evidence (a caution, not a result)

1. **The strata will be radically unequal, and the search should not be budgeted evenly.** S3
   (secularization) has a large individual-level empirical literature, a long history in demography,
   and access to genuine natural experiments. S1 and S2 have a large *theoretical* and *measurement*
   literature with very few fertility estimates that are not Tier 4. S4 is largely barred by Ruling 2.
   S5 is thin. Expect S3 to supply most of what the chapter can rate, exactly as rent-identified
   estimates were expected to carry C.2.c.
2. **Channel 1 will be stratum-asymmetric.** Reviews and meta-analyses of religion and fertility
   plausibly exist and would be the privileged seed for S3. A prior systematic review of
   postmaterialism and fertility very likely does not exist. A near-empty channel 1 for S1, S2, and S5
   is a finding rather than a search failure, and it would be the third chapter in a row to find
   channel 1 empty or thin, which is worth reporting on GACS §7 move 5 as tested rather than open.
3. **Four vocabulary families, barely overlapping.** Demography and the SDT tradition (Lesthaeghe,
   van de Kaa, Sobotka, Zaidi and Morgan; *Population and Development Review*, *Demographic
   Research*, *European Journal of Population*); sociology of religion (*Journal for the Scientific
   Study of Religion*, *Review of Religious Research*, *Demography*); cross-cultural values psychology
   (Inglehart, Schwartz; *Social Indicators Research*, *Journal of Cross-Cultural Psychology*); and
   the economics of culture (Fernández, Alesina and Giuliano, Enke; *QJE*, *AEJ*, *Journal of
   Economic Growth*), which says *culture*, *kinship intensity*, and *epidemiological approach* and
   almost never says *postmaterialism*. This is the widest vocabulary sprawl of any chapter attempted
   so far and predicts a higher cluster count under the GACS granularity rule than C.2.c's two
   families.
4. **Estimand collapse will be severe.** Most WVS and EVS papers have no fertility outcome at all,
   most SDT papers are descriptive, and most religiosity papers in the sociology-of-religion corpus
   study attendance rather than births. `VALUE_CONSTRUCT` and `OFF_OUTCOME` will be large cells.
5. **Routing volume will exceed every previous chapter.** Eleven walls, four proximate entries that
   name D.1.a as their root cause, and a sibling queue that includes most of section D. Screening
   cost should be budgeted against routing, not against topical retrieval.
6. **Geographic skew** toward Western Europe and the United States, with the WVS and EVS supplying
   most of the cross-national coverage. Since S3's natural experiments are concentrated in a few
   national settings, external validity will be a live limitation on the one stratum that can be rated.

---

## A note on the pre-modern baseline (scope observation, not an expansion)

D.1.a is not annexing PM. The secularization mechanism nonetheless presupposes a pre-modern baseline
of binding religious prescription, and the fertility differentials between religious communities in
pre-transition populations are the evidence that the baseline existed. That material is context for
this chapter's mechanism section and belongs substantively to D.2.b, which owns the PM normative
structure and carries Hajnal. Recorded so the connection is not lost and so the review does not later
discover it as a gap.

---

## Cold-start channels and leakage wall

1. Prior meta-analyses and systematic or scoping reviews, sought **separately per stratum** and
   expected to exist mainly for S3 → empirical anchors by external authority. *(Leakage wall: a
   review's search strings may feed query terms and its included studies may feed anchors, but never
   the same study to both.)*
2. Top-down theory and canon enumeration — Lesthaeghe, van de Kaa, Inglehart, Norris and Inglehart,
   Schwartz, and the SDT critiques — seeds the theory set. Does not count toward empirical recall.
3. Citation snowball from the channel-1 and channel-2 seeds → the orthogonal Tier-B frame. Run it
   per stratum rather than pooled, since the four vocabulary families will not reach each other.
4. Broad single-query search plus a structured screen, **only if** the gold is still under the
   cross-validation floor of thirty empirical anchors. Tier B is never drawn from this channel.
5. Production-query terms are not mined from a paper and then evaluated on it; learned extensions are
   fold-local once the gold frame exists.

**The inbound queue from D.3.b, and why it cannot be trusted as a sample.** The D.3.b RA gate routed
seventeen distinct records to `OFF_POSTMATERIALIST_D1a`, fifteen carrying DOIs, listed in
`extraction/climate-anxiety-eco-doomerism-ra-gate.csv`. They include Lesthaeghe's 2014 SDT overview,
a 2025 *Journal of Family Studies* paper titled "Postmaterialism and voluntary childlessness," two
environmentalism-and-fertility papers, and a run of voluntary-childlessness and childfree studies from
2021 to 2026. They are useful cold-start material and they are **Tier-A eligible only**. They must not
enter Tier B, under the integrity constraint recorded for C.2.c: they are what a climate-anxiety query
happened to surface, so they over-represent S4 childfree work and under-represent S3 secularization
and the S1 measurement literature entirely. Admitting them to Tier B would make Recall(B) a measure of
D.3.b's query shape.

Note also that most of the childfree records in that queue will land in
`NORM_ACCEPTABILITY_DESCRIPTIVE` once Ruling 2 is applied, so the inbound queue is a weaker
contribution to the empirical core than its record count suggests.

---

## Pre-query anchor audit (not yet built)

The verified anchor set will be stored in
`postmaterialism-individualism-secularization-cold-start-anchors.json`. Every anchor must clear the
**mandatory existence-verification gate** — a live DOI, or a Crossref or publisher record confirming
the title exists — before it enters any recall denominator. **No anchor is hand-asserted from
memory**, including the eight works named in the v5 `seminal` field, which are candidates to verify
rather than anchors. This is the standing rule from the 2026-07-08 run that found roughly forty
percent of the frozen OAS Tier B was fabricated.

Two chapter-specific cautions for the anchor build:

- **The seminal field is theory-heavy.** Lesthaeghe 1983, van de Kaa 1987, Lesthaeghe and van de Kaa
  1986, Lesthaeghe and Surkyn 1988, Inglehart 1977, and Norris and Inglehart 2004 are framework
  statements, and under the GACS Tier-A rule they seed the theory canon without counting toward
  empirical recall. Reaching the thirty-anchor cross-validation floor will require empirical anchors
  the v5 entry does not name, concentrated in S3.
- **Older canonical works predate DOIs.** Several will resolve by title through Crossref or a
  publisher record rather than by live DOI. Under the resolution rule they are kept and keyed on
  title; dropping them would bias the denominator toward recent, easily found work, which in this
  literature means biasing it toward the SDT framework papers and away from the FDT-era empirical
  material Ruling 4 just admitted.

The anchor set must carry **off-cell decoys** so the query is tested on routing as well as topical
retrieval. Given that routing is this chapter's dominant screening cost, the decoy set matters more
here than anywhere previous: include gender-attitude studies (D.2.a), marriage-norm and cohabitation
studies (D.2.b), media-exposure quasi-experiments (A.20), contraceptive-stigma studies (A.6),
epidemiological-approach papers using ancestral fertility (A.19), and income or unemployment studies
that narrate value change without measuring it (C.1.a, C.5.a).

---

## Escalations opened by this scope

1. **The SDT-only `phenomena` restriction, third instance.** A.10, C.2.c, and now D.1.a have each
   found evidence outside their assigned phenomenon. This is a master-list question for TICK-001
   rather than a fourth case-by-case exception, and the specific request for D.1.a is whether the
   field should read FDT, SDT.
2. **Non-additivity of mediated demographic-significance shares, third and sharpest instance.**
   Folded into the standing TICK-054 escalation, with the added observation that D.1.a makes it a
   defect in the verdict format rather than a per-chapter accounting note.
3. **A.19's claim on the epidemiological approach** (Wall 8). Recommended master-list note for
   TICK-001; flagged, not made.
4. **Rulings 2 and 3 need PI sign-off before the scope freezes.** Both bar or cap classes of evidence
   before any study is read, which is exactly the kind of pre-registered decision that must not be
   made unilaterally by an RA. Ruling 2 removes most of one of the five sub-claims the master list
   assigned to this chapter. Ruling 3 pre-commits the canonical SDT evidence base to carrying no
   causal weight.
