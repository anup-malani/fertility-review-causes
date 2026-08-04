# Search scope — postmaterialism, individualism, and secularization

**Hypothesis:** D.1.a (HYPOTHESES-v5.md)
**Hypothesis slug:** `postmaterialism-individualism-secularization`
**Target phenomenon:** SDT primary. FDT-era evidence is admitted on the ruling below. PM is not
annexed; see "A note on the pre-modern baseline."
**Status:** DRAFT (Shravan, 2026-08-03; rewritten same day onto the treatment × outcome definition).
Five treatment × outcome pairs, a design ladder with pre-committed GRADE ceilings, a degenerate-pair
rule, a pooling rule, and seven walls are proposed and **not frozen.** Freeze requires PI sign-off on
Rulings 2 and 3, because both cap the chapter's rating before a single study is read. Cold-start
anchor sourcing has not begun.

> **Scoping convention adopted (Shravan, 2026-08-03).** A hypothesis is defined as a **treatment ×
> outcome pair**. Routing asks two questions of a study — what is the treatment variable, and what is
> the outcome variable — and nothing else. Mediators, channels, and the mechanism the author narrates
> do not enter the definition and do not route a paper. This scope was first drafted on a
> cause → effect-plus-mechanism spine and rewritten onto this one; the earlier version is at commit
> `8811c17`. Whether the convention should be recorded in `PROTOCOL.md` for every chapter is raised
> under "Escalations" below.

The scoping brief that specifies this ticket's stage 2 is recoverable at
`git show eecf024:tickets/TICK-060-d1a-search-scope.md`; the work is now carried by TICK-062 under the
one-ticket-per-hypothesis model.

---

## The pair

**Treatment.** A measured value orientation on one of three axes: materialist → postmaterialist,
collectivist-obligated → individualist-autonomous, religious → secular.

**Outcome.** Fertility: realized births, parity progression, completed fertility, or stated fertility
intention.

**Direction claimed.** Movement toward the postmaterialist, individualist, or secular pole reduces the
outcome.

That is the whole definition. A study is in scope when its treatment variable is a value measure of
this content and its outcome variable is fertility. A study is out of scope when either half fails,
and it routes on **its own** treatment variable rather than on the mechanism its authors invoke.

**The routing test, in full:**

1. Is the regressor a measured value orientation of the specified content? If it is something else —
   a price, an income, a technology, a policy, a behavior, an exposure — the study belongs to whichever
   hypothesis owns that treatment.
2. Is the dependent variable a fertility measure? If it is contraceptive use, marriage, migration,
   wellbeing, or voting, the study is mechanism or context and carries no effect estimate here.
3. Are the treatment and the outcome the same construct? If so there is no pair; see Ruling 2.

---

## Ruling 1 — the chapter carries five pairs, estimated separately (Shravan, 2026-08-03)

The v5 entry absorbs five sub-claims: `secular-ideational-shift`, `individualism-rise`,
`secularization-religiosity-decline`, `childlessness-as-acceptable-choice`, and
`consumerism-aspirational-lifestyles`. Under the treatment × outcome definition these are **five
different treatments against one outcome**, which makes them five pairs sharing a chapter rather than
one hypothesis with five facets. An effect size on one is not exchangeable with an effect size on
another, so a pooled number across them would report whatever the measure mix in the sample happened
to be.

**The five pairs are estimated separately and never combined into one pooled effect.** The chapter's
headline result is a five-row table, not a single elasticity.

| Pair | Treatment variable | Measure family | Measurement note |
|---|---|---|---|
| `S1_POSTMATERIALISM` | Priority on self-expression and belonging over physical and economic security | Inglehart four-item and twelve-item batteries; WVS/EVS survival-versus-self-expression dimension | A ranked-priority instrument whose scores move with contemporaneous inflation and unemployment, so period effects contaminate the cohort reading the theory needs |
| `S2_INDIVIDUALISM` | Autonomy of the individual against obligation to kin and collective | Hofstede individualism; Schwartz autonomy and self-direction; kinship-intensity indices | The country-level indices are near-constant within a country over most study windows, so they identify cross-sectionally and inherit every cross-country confound |
| `S3_SECULARIZATION` | Religious affiliation, practice, and authority | Affiliation, service attendance, prayer frequency, salience, denomination | The one pair with a large individual-level literature and access to genuine natural experiments. Expected to carry the chapter |
| `S4_CHILDLESSNESS_NORM` | Normative acceptability of voluntary childlessness | Attitude items on approval of remaining childfree; childfree self-identification | Largely a degenerate pair under Ruling 2 |
| `S5_CONSUMERISM` | Orientation toward acquisition and lifestyle consumption | Richins–Dawson material-values scale; consumption-aspiration measures | Thin fertility literature. Carries the vocabulary trap below |

**Recommendation for TICK-001, flagged not made.** If a hypothesis is a treatment × outcome pair, then
five pairs is five hypotheses and the master list should carry them as such, with `S3_SECULARIZATION`
split out first since it is the only one with a rateable evidence base. The precedent is TICK-032,
which split the compulsory-education entry for the same reason. This scope keeps them in one chapter
because the master list does, and reports them separately so a later split costs nothing.

**Vocabulary trap, load-bearing for the query build.** The word *materialism* names opposite treatments
in the two literatures that feed this chapter. Inglehart's *materialist* prioritizes physical and
economic security, which is the pole D.1.a says fertility declines away from. The consumer-psychology
*materialist* is acquisitive and lifestyle-oriented, which is the S5 pole D.1.a says fertility
declines toward. A query using the term without disambiguation retrieves both and scores them in
opposite directions. Handle it in the cause-axis clusters, not at screening.

---

## Ruling 2 — the degenerate-pair rule (Shravan, 2026-08-03)

**When the treatment measure and the outcome measure are the same construct, there is no pair, and the
estimate is barred from the causal pool.**

A respondent's approval of voluntary childlessness, regressed on that respondent's childlessness, is a
correlation between a stated preference and its realization. Treatment and outcome are one variable
measured twice. The coefficient reports preference-outcome consistency and is compatible with no value
change and no causal effect at all.

The rule cuts a real and populated class of studies, so its boundary is stated precisely:

- **Barred from the causal pool:** own attitude toward childbearing, own ideal family size, own
  approval of voluntary childlessness, or childfree self-identification, against the same person's
  fertility. These route to `NORM_ACCEPTABILITY_DESCRIPTIVE` and are reported as evidence on the
  prevalence and correlates of the norm.
- **Admissible:** a value measure carrying no reproductive item content — postmaterialism battery,
  service attendance, autonomy index — against the respondent's fertility. Treatment and outcome are
  distinct constructs.
- **Admissible:** an *environment-level* norm measure, such as the community, cohort, or
  leave-one-out mean acceptability of childlessness, against *individual* fertility. Aggregating away
  the respondent's own report makes the treatment a distinct variable. Such estimates then face Wall 6,
  because a norm-exposure design may have exposure rather than the norm as its treatment.

**The test is invisible to a title/abstract screen.** Whether a value scale contains reproductive items
is a property of the instrument, reported in a methods section. The D.3.b RA gate found its decisive
routing failures were of exactly this kind and cut the realized pool from eight to five. Budget an
RA-gate bleed-in now; S4 is where it will concentrate.

---

## Ruling 3 — the admissible-design ladder, with pre-committed GRADE ceilings (Shravan, 2026-08-03)

The v5 `notes` field concedes that D.1.a is "criticized as descriptive rather than causal." The
concession is accurate. If admissible design classes are not fixed before the search, the screen will
return several hundred papers reporting that value indices and fertility correlate, and the chapter
will decide after the fact whether that is causal evidence. Deciding after the fact is how a rating
drifts upward, and RA-PLAYBOOK names the resulting failure explicitly: a rating that reads Moderate
over studies that are all cross-sectional with no identification.

Each design class therefore carries in advance the highest GRADE rating it can support.

**Tier 1 — exogenous variation in the treatment. Ceiling: Moderate; High only with replication across
settings and designs.** The design moves the value or religiosity distribution for reasons plausibly
unrelated to the affected population's fertility preferences, and measures fertility afterward.
Candidate sources: state secularization and anti-religious campaigns; reform of church membership,
church tax, or the cost of affiliation; repeal of blue laws and Sunday-trading restrictions;
clergy-scandal shocks to attendance; compulsory secular schooling extensions; religious-market
deregulation; resettlement episodes that mixed value distributions.

**Tier 2 — treatment measured before the outcome, environment held fixed. Ceiling: Low.** Three
families qualify: panels measuring values on childless respondents and following them to realized
births; epidemiological or immigrant designs holding host institutions and prices fixed while an
ancestral *value* measure varies (Wall 5 governs what the proxy must contain); and within-family or
sibling designs differencing out household background. Temporal precedence and a fixed environment
improve on contemporaneous correlation and are not identification.

**Tier 3 — individual-level cross-section or contemporaneous panel with controls. Ceiling: Very low.**
Treatment and outcome measured at the same time on the same people, with covariate adjustment. This
will be the modal included study.

**Tier 4 — aggregate co-movement. No causal weight; descriptive stream only.** Country-level or
region-level correlation between a value index and TFR, which is the canonical SDT evidence base.
These enter as description of the phenomenon to be explained. Three defects justify the exclusion
jointly: the unit count is around fifty against a dozen collinear covariates, GDP per capita is among
them, and countries are not independent draws because values diffuse across borders, which is Galton's
problem in its original demographic form.

**A study is rated on the design that produces the estimate, not on the sophistication of the paper
around it.** A widely cited framework statement supported by a scatterplot is Tier 4.

---

## Ruling 4 — period (Shravan, 2026-08-03)

**FDT-era evidence is admitted; the `phenomena` field goes to the PI.** The v5 entry scopes D.1.a to
SDT alone, but the Princeton European Fertility Project's secularization and lay-culture measures are
the S3 treatment applied to the first transition. Excluding them on period grounds would drop the
largest body of evidence bearing on the chapter's strongest pair.

Following the C.2.c precedent, the ruling governs *inclusion* while the per-phenomenon verdict
structure stays SDT-primary, and the field update is a PI call. Every effect carries its period, so
FDT-era estimates stay separable in synthesis.

**Third chapter in a row to hit this restriction** — A.10, then C.2.c and its Li 2024 exception, now
D.1.a. Three instances make it a master-list question rather than a third case-by-case ruling.

---

## Ruling 5 — sign convention (Shravan, 2026-08-03)

**Orient every effect as the change in fertility per unit movement toward the postmaterialist,
individualist, or secular pole.** A negative sign supports the hypothesis in every pair.

The convention is not cosmetic. S3 is almost always coded in the opposite direction, since the
literature regresses fertility on *religiosity*, so most included estimates must be sign-flipped on
entry and the flip recorded. Mixing flipped and unflipped estimates in one pool is a mechanical route
to a near-zero pooled effect, and it is the error the A.10 sign convention was written to prevent.

---

## Pooling rule (pre-registered)

1. **Never pool across pairs.** S1 through S5 are five treatments (Ruling 1).
2. **Within a pair, pool only within a measure family.** Service attendance and stated religious
   salience are different treatments, not two measurements of one, and pool separately unless
   extraction establishes a defensible common scale.
3. **Never pool across outcome levels.** Realized births, completed fertility, and stated intention or
   ideal family size pool separately. This is the standing D.3.b synthesis rule and it binds harder
   here, because a large share of this literature has intentions as its only outcome.
4. **Never pool across design tiers.** A Tier 1 estimate and a Tier 3 estimate are not two draws from
   one distribution. Report tiers separately; where the identified estimates disagree with the
   correlational ones, the disagreement is a headline result.
5. **Tier 4 estimates never enter any pool.**
6. **Record the survey source on every effect and treat shared sources as non-independent.** Much of
   this literature runs on a handful of instruments — WVS/EVS, ESS, GSS, NSFG, DHS, and the national
   generations-and-gender panels — so twenty papers on overlapping waves and countries are not twenty
   independent estimates. `DATA_SOURCE` is a required tag and a clustering variable in any pooled
   analysis; a random-effects model ignoring it will understate the variance badly.

---

## The boundary walls

Each wall names the neighbor's **treatment**. Nothing below turns on a mechanism or a mediator: a
study whose treatment is a value measure and whose outcome is fertility is this chapter's even when
the effect plainly travels through contraception, marriage, or migration, and a study whose treatment
is something else is not this chapter's however cultural its framing.

**Wall 1 — D.3.b (`climate-anxiety-eco-doomerism`). Adopted by reference; not restated.** The D.3.b
scope's Wall 1 already specifies this boundary from the other side and is authoritative for both
chapters. In treatment terms: D.3.b's treatment is measured ecological fear or eco-ethical concern;
D.1.a's is a general value orientation with no fear content. Read the rule in
`climate-anxiety-eco-doomerism-search-scope.md`.

*General point worth recording:* a wall between paired hypotheses should be written once and
referenced from the other side. Two independently drafted statements of one boundary drift apart, and
papers then satisfy both chapters or neither.

**Wall 2 — D.1.b (`caldwell-wealth-flows-westernization`): exposure versus value.** D.1.b's treatment
is *exposure to an external cultural source* — media reach, missionary contact, migrant return flows,
schooling carrying a foreign family model. D.1.a's treatment is a value *held*, measured on the
respondent or the population. Setting is a strong prior and never decides on its own: measured
secularity in contemporary South Korea is D.1.a; exposure of rural Nepal to Western family ideals is
D.1.b.

**Wall 3 — D.1.c (`cultural-evolution-demographic-transition`): status asymmetry versus value
content.** D.1.c's treatment is a prestige or status gradient in the transmission process. D.1.a's is
the measured content of a value orientation. A design turning on who imitates whom is D.1.c's.

**Wall 4 — D.2.a (`female-empowerment-gender-equity`) and D.2.b (`marriage-family-norms`): which
attitude, and attitude versus behavior.** Both neighbors sit close and will be tested constantly,
because the SDT literature reports value change, gender attitudes, and partnership behavior as one
bundle.

- **D.2.a's treatment** is a gender-specific attitude or index: egalitarian gender-role attitudes,
  women's decision-making authority, gender-equity indices. **D.1.a's treatment** is a general value
  orientation that is not gender-specific. Female education used as a proxy for autonomy is D.2.a's,
  and also fails Wall 7.
- **D.2.b's treatment** is a partnership behavior or marriage-institution measure: cohabitation,
  divorce liberalization, union deinstitutionalization, kinship structure. These are D.2.b's even
  when a paper labels them SDT indicators, because they are behaviors rather than held values.
- **D.2.d (`child-centeredness-intensive-parenting`)** takes a parenting-standard measure as its
  treatment, so it is D.2.d's, light wall.

**Wall 5 — A.19 (`intergenerational-transmission-fertility`): what the culture proxy contains. The
demonstrated failure.** A.19's seminal list contains **Fernández and Fogli 2009** and its `notes`
field claims the epidemiological approach outright: "Epidemiological approach (Fernandez-Fogli) uses
immigrants to isolate cultural from environmental effects." That design is simultaneously the best
available tool for D.1.a, since it holds prices, institutions, and markets fixed while the treatment
varies. One identification strategy, two chapters, which is structurally the Lovenheim and Mumford
problem C.2.c had to resolve.

- **Discriminator: the content of the proxy, which is the treatment variable.**
  - Ancestral-country **fertility rate** as the proxy → **A.19**. The treatment is a fertility norm,
    so the pair is fertility × fertility and the claim is persistence.
  - Ancestral-country **value measure** — religiosity, individualism index, postmaterialism score,
    kinship intensity → **D.1.a**. The treatment is a value.
- A study using both proxies is `MIXED_CULTURE_PROXY`, reported to both chapters as unallocated.
- *Recommended master-list note for TICK-001: A.19's `notes` should record that the epidemiological
  design is a shared instrument routed by proxy content, not a possession of A.19. Flagged, not made.*

**Wall 6 — A.3, A.6, and A.20: the proximate entries whose treatments are not values.** Three
proximate entries name D.1.a as the root cause behind them, and A.6's `notes` says it plainly: "the
root cultural cause lives in D." Under the treatment × outcome definition the boundary is mechanical
and none of it turns on which is root and which is proximate.

- **A.3's treatment** is information about and legitimation of birth control.
- **A.6's treatment** is a contraception- or abortion-specific attitude or stigma measure.
- **A.20's treatment** is exposure to a transmission channel: media reach, network position,
  linguistic or community boundary. The media quasi-experiments (La Ferrara et al., Jensen and Oster)
  are A.20's by treatment.
- **D.1.a's treatment** is a general value orientation. It owns the estimate whenever that is the
  regressor, including when the fitted effect runs through contraceptive use.

**Wall 7 — C.1.a (`income-effect-normal-good`) and C.5.a (`economic-uncertainty-and-unemployment`):
values must be measured, not narrated.** Inglehart theorizes postmaterialist values as a consequence
of affluence and existential security, and the v5 `notes` field flags the hypothesis as "hard to
separate from income/security mechanisms."

- **Discriminator:** is the regressor a measured value, or an income or employment variable? A study
  identified off income, growth, or unemployment variation, with value change narrated but not
  measured, has income as its treatment and belongs to C.1.a or C.5.a whatever its framing.
- **Separately, record on every included effect whether income and economic security were held
  fixed.** That is a grading fact rather than a routing fact: an estimate whose treatment is a value
  measure is in scope regardless, but one that leaves income free cannot distinguish the value effect
  from the affluence effect, and Ruling 3's tiers grade it accordingly.

*Light cross-references, no wall needed:* C.2.h (digital leisure, whose treatment is technology
availability or use), C.2.f, B.1, and A.11.

---

## Estimand cells

Every cell is a treatment × outcome pair. The treatment column decides the routing.

| Cell | Treatment variable | Outcome variable | Routing |
|---|---|---|---|
| `PRIMARY_POSTMATERIAL_S1` | Postmaterialist or self-expression value measure | Fertility | Primary — S1 pool |
| `PRIMARY_INDIVIDUALISM_S2` | Individualism, autonomy, or kinship-intensity measure | Fertility | Primary — S2 pool |
| `PRIMARY_SECULAR_S3` | Religiosity, affiliation, attendance, salience, denomination | Fertility | Primary — S3 pool; expected core |
| `PRIMARY_SECULAR_SHOCK_S3` | Same, moved by an exogenous shock (Tier 1) | Fertility | Primary — S3 pool, highest-quality stratum |
| `PRIMARY_CONSUMERISM_S5` | Consumption orientation or material-values scale | Fertility | Primary — S5 pool |
| `PRIMARY_VALUE_EX_ANTE` | Any admissible value measure recorded *before* the outcome, on childless respondents (Tier 2) | Realized births | Primary; the value-added cell, and the only individual-level design that breaks the reverse-causality tie |
| `NORM_ACCEPTABILITY_DESCRIPTIVE` | Own attitude toward childbearing, childlessness, or ideal family size | Own fertility | Degenerate pair under Ruling 2; reported descriptively, barred from the causal pool |
| `NORM_ENVIRONMENT_LEVEL` | Community, cohort, or leave-one-out norm acceptability | Individual fertility | Primary if the treatment is the norm rather than exposure to it (Wall 6) |
| `AGGREGATE_COMOVEMENT` | Country or region value index (Tier 4) | Aggregate TFR | Descriptive stream; never pooled |
| `MIXED_CULTURE_PROXY` | Ancestral fertility and ancestral values jointly | Fertility | Primary, flagged unallocated; reported to A.19 |
| `SDT_FRAMEWORK_THEORY` | None — framework statement, elaboration, or critique | None | Theory stream |
| `VALUE_CONSTRUCT` | Value measure as the *dependent* variable — scale validation, prevalence, determinants of secularization | Not fertility | Theory stream |
| `OFF_EXPOSURE_D1b` | Exposure to an external modernity package | Fertility | Route to D.1.b |
| `OFF_STATUS_D1c` | Prestige or status gradient in transmission | Fertility | Route to D.1.c |
| `OFF_GENDER_D2a` | Gender-role attitudes, women's autonomy, gender-equity index | Fertility | Route to D.2.a |
| `OFF_PARTNERSHIP_D2b` | Cohabitation, divorce, union deinstitutionalization, kinship structure | Fertility | Route to D.2.b |
| `OFF_PARENTING_D2d` | Parenting-standard measure | Fertility | Route to D.2.d |
| `OFF_ANCESTRAL_FERTILITY_A19` | Ancestral-country fertility rate | Fertility | Route to A.19 |
| `OFF_CONTRACEPTIVE_ATTITUDE_A3_A6` | Birth-control information, legitimation, or contraception-specific stigma | Fertility | Route to A.6 or A.3 |
| `OFF_CHANNEL_A20` | Media, network, or boundary exposure | Fertility | Route to A.20 |
| `OFF_INCOME_SECURITY` | Income, growth, affluence, unemployment, or job insecurity | Fertility | Route to C.1.a or C.5.a |
| `OFF_OUTCOME` | Admissible value measure | Not fertility — contraceptive use, marriage, migration, wellbeing, voting | Mechanism / context only; no effect estimate |
| `OFF_OTHER` | Some other fertility determinant with no sibling home | Fertility | Route out; no sibling queue |
| `REVERSE` | Parenthood or fertility status | Values, religiosity, attendance | Context, and see threat 1 |
| `INSUFFICIENT_INFO` | Not determinable on the visible record | Unknown | Pairs only with `UNCERTAIN` |

---

## Required tags on every included empirical effect

- `PAIR` — S1 through S5, per Ruling 1.
- `TREATMENT_MEASURE` — the named instrument, its item count, and whether any item carries
  reproductive content (the Ruling 2 test).
- `OUTCOME_LEVEL` — realized births / completed fertility / stated intention or ideal family size.
- `DESIGN_TIER` — 1 through 4 per Ruling 3, with the source of variation in the treatment named.
- `SIGN_FLIPPED` — whether the coefficient was reoriented to Ruling 5.
- `MEASUREMENT_TIMING` — treatment recorded before, at the same time as, or after the outcome. Decides
  Tier 2 eligibility and is the reverse-causality test.
- `INCOME_SECURITY_HELD_FIXED` — whether income and economic security are controlled, instrumented, or
  fixed by design (Wall 7, grading half).
- `TEMPO_OR_QUANTUM` — timing versus completed fertility. A postponement-only effect carries far less
  demographic significance. Cross-ref A.11; precedent for nesting a tempo reading under A.11 was set at
  TICK-038.
- `DATA_SOURCE` — survey instrument and waves, for the non-independence clustering in pooling rule 6.
- `PERIOD` — study window and its FDT/SDT classification under the replacement-status rule in
  PROTOCOL §2.

---

## Identification threats (what the risk-of-bias pass is looking for)

1. **Reverse causality, running in the direction that flatters the hypothesis.** Having children
   raises religious participation, since parents return to congregations for childrearing, community,
   and schooling. Values also adjust to realized life courses, so people who have not had children may
   report more self-oriented values partly because they have not had them. A contemporaneous
   religiosity-fertility correlation therefore overstates the effect. The childfree literature is most
   exposed, since value orientations there are frequently collected after the outcome is settled.
   `MEASUREMENT_TIMING` grades this, and it is this chapter's binding domain the way endogenous tenure
   was C.2.c's.
2. **Degenerate pairs that slip the screen** (Ruling 2). Caught here if routing missed them.
3. **Common causes of treatment and outcome.** Education, income, urban residence, cohort, and
   migration status predict both. Education is the worst, because it is the most common covariate
   *and* the most common proxy for secular-individualist orientation: controlling for it may absorb
   the treatment, and failing to control for it leaves the estimate confounded.
4. **Affluence and security moving the treatment** (Wall 7, grading half). An estimate that leaves
   income free cannot separate the value effect from the income effect at any design tier.
5. **Ecological inference and Galton's problem** on all Tier 4 material.
6. **Non-independence across studies sharing a survey** (pooling rule 6).
7. **Justification bias in stated reasons.** Respondents asked why they have no children supply
   socially acceptable accounts, and self-expression is more acceptable than infertility or
   partnership failure. Stated-reason studies measure the acceptability of reasons alongside the
   reasons.

---

## When to adjudicate

The title/abstract screen decides only which stream a paper belongs to, and it can usually identify
the treatment variable from an abstract. It cannot determine three facts that this chapter's grading
turns on, all of which are methods-section facts: whether the value instrument contains reproductive
items (Ruling 2), whether the treatment was measured before or after the outcome (Tier 2 eligibility),
and whether income and security were held fixed (Wall 7). Expect the screen's routing to be
provisional and budget the RA gate accordingly; the D.3.b precedent is exact and its gate cut the
realized pool by nearly half.

Drafting may report only what these full-text fields support. A cross-sectional association between
secularity and low fertility, with no exogenous variation in the treatment and no timing information,
documents an association and must not be described as evidence that the value shift *caused* the
fertility difference. Threats 1 and 3 alone are sufficient to generate that association with no causal
effect at all.

---

## Expected shape of the evidence (a caution, not a result)

1. **The five pairs will be radically unequal, and the search should not be budgeted evenly.** S3 has
   a large individual-level empirical literature, a long history in demography, and access to genuine
   natural experiments. S1 and S2 have a large theoretical and measurement literature with very few
   fertility estimates above Tier 4. S4 is largely degenerate under Ruling 2. S5 is thin. Expect S3 to
   supply most of what the chapter can rate, exactly as rent-identified estimates were expected to
   carry C.2.c.
2. **Channel 1 will be pair-asymmetric.** Reviews and meta-analyses of religion and fertility
   plausibly exist and would be the privileged seed for S3. A prior systematic review of
   postmaterialism and fertility very likely does not. A near-empty channel 1 for S1, S2, and S5 is a
   finding rather than a search failure, and it would be the third chapter running to find channel 1
   thin or empty, which is worth reporting on GACS §7 move 5 as tested rather than open.
3. **Four vocabulary families, barely overlapping.** Demography and the SDT tradition (Lesthaeghe, van
   de Kaa, Sobotka, Zaidi and Morgan; *Population and Development Review*, *Demographic Research*,
   *European Journal of Population*); sociology of religion (*Journal for the Scientific Study of
   Religion*, *Review of Religious Research*, *Demography*); cross-cultural values psychology
   (Inglehart, Schwartz; *Social Indicators Research*, *Journal of Cross-Cultural Psychology*); and
   the economics of culture (Fernández, Alesina and Giuliano, Enke; *QJE*, *AEJ*, *Journal of Economic
   Growth*), which says *culture*, *kinship intensity*, and *epidemiological approach* and almost never
   says *postmaterialism*. The widest vocabulary sprawl of any chapter attempted so far, predicting a
   higher cluster count under the GACS granularity rule than C.2.c's two families.
4. **Estimand collapse will be severe.** Most WVS and EVS papers have no fertility outcome, most SDT
   papers are descriptive, and most religiosity papers in the sociology-of-religion corpus have
   attendance rather than births as the outcome. `VALUE_CONSTRUCT` and `OFF_OUTCOME` will be large.
5. **Routing volume will exceed every previous chapter.** Seven walls covering most of section D plus
   four entries in section A. Screening cost should be budgeted against routing rather than against
   topical retrieval.
6. **Geographic skew** toward Western Europe and the United States, with WVS and EVS supplying most
   cross-national coverage. S3's natural experiments are concentrated in a few national settings, so
   external validity will be a live limitation on the one pair that can be rated.

---

## A note on the pre-modern baseline (scope observation, not an expansion)

D.1.a is not annexing PM. Fertility differentials between religious communities in pre-transition
populations are nonetheless the evidence that religious prescription once bound, which is the baseline
the S3 pair measures movement away from. That material is context for the chapter's mechanism section
and belongs substantively to D.2.b, which owns the PM normative structure and carries Hajnal. Recorded
so the connection is not lost and the review does not later discover it as a gap.

---

## Cold-start channels and leakage wall

1. Prior meta-analyses and systematic or scoping reviews, sought **separately per pair** and expected
   to exist mainly for S3 → empirical anchors by external authority. *(Leakage wall: a review's search
   strings may feed query terms and its included studies may feed anchors, but never the same study to
   both.)*
2. Top-down theory and canon enumeration — Lesthaeghe, van de Kaa, Inglehart, Norris and Inglehart,
   Schwartz, and the SDT critiques — seeds the theory set. Does not count toward empirical recall.
3. Citation snowball from the channel-1 and channel-2 seeds → the orthogonal Tier-B frame. Run it per
   pair rather than pooled, since the four vocabulary families will not reach each other.
4. Broad single-query search plus a structured screen, **only if** the gold is still under the
   cross-validation floor of thirty empirical anchors. Tier B is never drawn from this channel.
5. Production-query terms are not mined from a paper and then evaluated on it; learned extensions are
   fold-local once the gold frame exists.

**The inbound queue from D.3.b, and why it is not a sample.** The D.3.b RA gate routed seventeen
distinct records to `OFF_POSTMATERIALIST_D1a`, fifteen carrying DOIs, listed in
`extraction/climate-anxiety-eco-doomerism-ra-gate.csv`. They include Lesthaeghe's 2014 SDT overview, a
2025 *Journal of Family Studies* paper titled "Postmaterialism and voluntary childlessness," two
environmentalism-and-fertility papers, and a run of voluntary-childlessness and childfree studies from
2021 to 2026. They are useful cold-start material and they are **Tier-A eligible only**. They must not
enter Tier B, under the integrity constraint recorded for C.2.c: they are what a climate-anxiety query
happened to surface, so they over-represent S4 and under-represent S3 and the S1 measurement literature
entirely. Admitting them to Tier B would make Recall(B) a measure of D.3.b's query shape.

Most of the childfree records in that queue will land in `NORM_ACCEPTABILITY_DESCRIPTIVE` once Ruling 2
is applied, so the queue contributes less to the empirical core than its record count suggests.

---

## Pre-query anchor audit (not yet built)

The verified anchor set will be stored in
`postmaterialism-individualism-secularization-cold-start-anchors.json`. Every anchor must clear the
**mandatory existence-verification gate** — a live DOI, or a Crossref or publisher record confirming
the title exists — before it enters any recall denominator. **No anchor is hand-asserted from memory**,
including the eight works named in the v5 `seminal` field, which are candidates to verify rather than
anchors. This is the standing rule from the 2026-07-08 run that found roughly forty percent of the
frozen OAS Tier B was fabricated.

Two chapter-specific cautions:

- **The seminal field is theory-heavy.** Lesthaeghe 1983, van de Kaa 1987, Lesthaeghe and van de Kaa
  1986, Lesthaeghe and Surkyn 1988, Inglehart 1977, and Norris and Inglehart 2004 are framework
  statements. Under the GACS Tier-A rule they seed the theory canon without counting toward empirical
  recall, so reaching the thirty-anchor cross-validation floor will require empirical anchors the v5
  entry does not name, concentrated in S3.
- **Older canonical works predate DOIs** and will resolve by title through Crossref or a publisher
  record. Under the resolution rule they are kept and keyed on title; dropping them would bias the
  denominator toward recent, easily found work, which here means biasing it toward SDT framework papers
  and away from the FDT-era empirical material Ruling 4 admits.

The anchor set must carry **off-cell decoys** so the query is tested on routing as well as topical
retrieval. Routing is this chapter's dominant screening cost, so the decoy set matters more here than
anywhere previous: gender-attitude studies (D.2.a), cohabitation and marriage-norm studies (D.2.b),
media-exposure quasi-experiments (A.20), contraceptive-stigma studies (A.6), epidemiological-approach
papers using ancestral fertility (A.19), and income or unemployment studies that narrate value change
without measuring it (C.1.a, C.5.a).

---

## Escalations opened by this scope

1. **Rulings 2 and 3 need PI sign-off before the scope freezes.** Both bar or cap classes of evidence
   before any study is read, which is the kind of pre-registered decision an RA should not make alone.
   Ruling 2 removes most of one of the five sub-claims the master list assigned to this chapter.
   Ruling 3 pre-commits the canonical SDT evidence base to carrying no causal weight.
2. **The treatment × outcome definition should probably be recorded in `PROTOCOL.md`.** It arrived as
   PI guidance during this scope and it changes routing across every chapter, not only this one: it
   makes mediator overlap a synthesis question rather than a scoping question, and it retires the
   root-cause-versus-proximate reasoning that Walls 5 and 6 previously carried. A convention that no
   operating file states is inert, per the ticket-closing rule.
3. **The SDT-only `phenomena` restriction, third instance.** A.10, C.2.c, and now D.1.a. A master-list
   question for TICK-001 rather than a fourth exception; the specific request is whether D.1.a's field
   should read FDT, SDT.
4. **A.19's claim on the epidemiological approach** (Wall 5). Recommended master-list note for
   TICK-001; flagged, not made.
5. **Five pairs is arguably five hypotheses** (Ruling 1). Under the definition adopted here the master
   list should probably split D.1.a, starting with S3. Precedent at TICK-032.

*One item the earlier draft raised is deliberately demoted.* The non-additivity of demographic-
significance shares across D.1.a and the proximate entries it feeds is real, and under the treatment ×
outcome definition it is **not a scoping problem** — the treatments differ, so the routing is clean and
no study is double-counted. It reappears only at §7, when shares that overlap in the same decline are
added. It stays folded into the standing TICK-054 escalation and out of this chapter's walls.
