# Search scope — intergenerational wealth flows reversal

**Hypothesis:** C.3.f, slug `wealth-flows-reversal`, HYPOTHESES-v5.md §C.3.f
**Ticket:** TICK-086 · branch `086-wealth-flows-reversal`
**Status:** stage 2, drafted 2026-09-10 (Shravan). The direction ruling, the walls, the estimand
cells, the required tags, the pooling rule and the demographic-significance route are frozen below.
Five PI calls open (§13). **Amended 2026-09-10 (`379`)**: the three gaps this document flagged — Wall 5, §7 rows 5 and 6, and the §7 row 4 null — are now measured, and the outcome axis is calibrated. Amendments are marked **[379]**.

**What is measured here and what is not.** Every count comes from
`source/build/goldset/304_candidate_frame_probe.py`, `376_c3f_term_diagnostics.py` and
`377_c3f_inherited_seeds.py`, with logs beside this file. They are OpenAlex title/abstract record
counts and one hand-read set of 28 records: they size a *retrieval frame* and its overlaps. **No
production query has been run, no anchor resolved, and no record screened.** A count is not an
evidence base, and a study can estimate this chapter's parameter without carrying any of these
phrases in its abstract — which, as §3 shows, is the normal case here.

---

## 1. The claim

Registry: *modernization reverses the net direction of intergenerational transfers from
child-to-parent to parent-to-child, eliminating the economic rationale for high fertility by turning
children from net assets into net liabilities.* Phenomenon: **FDT**. Cross-ref: D.1.b (the cultural
channel through which the shift occurs). Seminal: Caldwell 1976, Caldwell 1982, Kaplan 1994, Lee
2000. Registry note: *this entry captures the economic mechanism of Caldwell's theory; the cultural
channel lives in D.1.b. Both entries are needed; they are complementary not redundant.*

The chapter's parameter is the change in completed fertility caused by an exogenous change in the
**net direction and magnitude of private transfers between parents and their children**, holding
household income, child mortality and the price of any required input fixed.

Every clause is load-bearing. **"Net"** rather than upward or downward is §2, and it is the ruling
that decides what this chapter is. **"Private"** rather than public is Wall 1: a state pension that
substitutes for support from children is C.3.c's estimand, and C.3.c is a *closed* chapter.
**"Between parents and their children"** excludes transfers to and from other kin, which is most of
what the elder-care literature measures. **"Holding income fixed"** is Wall 5 (C.1.a), and it is
violated by almost every shock in §7. And **completed fertility** — rather than the flow itself, or
attitudes about children — is what separates this chapter's evidence from its background, which on
the numbers below is most of the literature.

---

## 2. The direction ruling — and it is the ruling that decides the chapter

**The registered exposure is a net quantity with a sign. The literature that exists is
one-directional, and its thick side belongs to another chapter.**

Measured inside the fertility-restricted frame (`376`):

| arm | what it measures | records | carrying an identified design |
|---|---|---|---|
| **UPWARD** | what children give: child labour contribution, old-age support, filial support, remittances to parents | 227 | 12 |
| **DOWNWARD** | what parents give: parental investment, expenditure on children, human-capital investment | 1,168 | 68 |
| **NET — the registered exposure** | the difference and its sign: net transfers, the NTA lifecycle deficit, the direction of the flow | **166** | **6** |

Arms overlap little: 15 records carry both directions, 20 carry the net alongside one of the
components. These are three literatures, not three views of one.

**Ruling.** The **NET** arm is C.3.f's primary cell. **UPWARD** and **DOWNWARD** measured alone are
admitted as mechanism evidence on the two components of the difference, tagged `flow_direction`, and
**never pooled — with each other or with the net arm.**

The reason is arithmetic, not taste. The net flow is downward minus upward. A rise in the downward
component and a rise in the upward component move the net in *opposite* directions. A synthesis that
averaged "wealth flow" effects without a direction tag would be averaging quantities whose signs are
opposed by construction, and would return a number near zero whatever the world was doing. This is a
harder version of `outcome-level-separates-channels`: there, two levels of one outcome; here, two
components whose sum is the thing we care about.

**The thick arm is not ours anyway.** The downward component — what a child costs — is C.2.b's
registered estimand (rising direct costs of children), and C.2.b is drafted. Its 68 identified
designs are read here as evidence on one half of a difference, not as evidence for this hypothesis.

**Corroboration from a second and independent route.** D.1.b's screen routed 28 records to C.3.f
under a wall written on the exposure alone. Hand-read (`377`, routing in
`c3f-inherited-seeds-routing.md`), **four of the twenty-eight carry both a flow-moving exposure and a
fertility outcome.** Six measure a transfer with no fertility outcome at all; four are C.3.c's; one
runs in reverse. Twenty-eight hand-adjudicated records and a 1,099-record frame agree on the shape.

---

## 3. This is a measurement vocabulary, not an estimation one

C.3.d found that a theory's own words retrieve the theory and miss the studies that test it. C.3.f
has the same disease in a different form: the vocabulary retrieves the theory **and its measurement
tradition**, and misses identification entirely.

**Eighteen records in the whole 1,099-record frame carry an identified-design marker — 1.6%.**
Against 256 carrying an accounting or measurement marker. The literature named after Caldwell
describes the exposure carefully and estimates its effect on fertility almost never.

Which terms earn the frame (`376`, each scored alone against the wide outcome axis):

| term | alone | unrestricted |
|---|---|---|
| `value of children` | **515** | 7,083 |
| `intergenerational transfer` | **284** | 3,176 |
| `old age support` / `old-age support` | 205 / 205 | — |
| `wealth flows` | 74 | 237 |
| `National Transfer Accounts` | 60 | 425 |
| `intergenerational wealth` | 33 | 528 |
| `filial support` | 7 | 109 |
| `life cycle deficit` · `lifecycle deficit` · `child labour contribution` · `child labor contribution` | 3 · 1 · 1 · **0** | — |

Three findings, each with a consequence.

**One term is nearly half the frame, and it is the measurement tradition.** `value of children` is
515 of 1,099; dropping it takes the frame to 607. Inside the fertility restriction, 191 of those
carry Value-of-Children *survey* vocabulary — an instrument eliciting what parents say children are
worth to them. A stated valuation is not a realized flow and its usual outcome is an intention. This
is PI call 1; the recommendation is background and link-1 mechanism evidence, never pooled, never a
demsig numerator.

**Four of the twelve axis terms are dead.** `child labor contribution` returns zero, and the other
three return one to three records. They were carried into the probe's union axis from the registry's
own phrasing and they retrieve nothing. Drop all four from the production query.

**One drop test is uninformative and would have read as a clean result.** Removing `old age support`
changes the frame by exactly zero, because its hyphenated twin `old-age support` is also in the axis
and OpenAlex folds the hyphen — both return 205. The term is not redundant; the *test* was. Any
future drop test must remove a term and every spelling of it together.

Homonyms are clean, which is worth stating because two of these terms are large general-purpose words
elsewhere. `intergenerational transfer` is a public-finance and behaviour-genetics phrase — 3,176
records unrestricted, 364 of them bequest-and-estate — but the bequest residue *inside* the
fertility-restricted frame is 33 (3.0%) and the genetics residue is **1**. `wealth flows` intersects
capital markets 21 times unrestricted. Neither needs a homonym gate.

### 3B. The outcome axis, calibrated **[379]**

`calibrate-the-outcome-axis-too`. Each outcome term scored against the C.3.f exposure axis:

| term | n |
|---|---|
| `fertility` | 840 |
| `number of children` | 211 |
| `childbearing` · `family size` | 160 each |
| `birth rate` | 77 |
| `total fertility rate` | 45 |

**The specific worry was `family size`.** In a transfer literature that phrase often means *household*
size — who lives with whom — not completed fertility, and admitting it would let co-residence records
in as fertility ones. Measured: `family size` inside this frame intersects household-size vocabulary
**5 times**, and `number of children` **4 times**. The worry is discharged; both terms stay.

### 3A. Candidate terms, priced by marginal gain

Priced as (axis OR term) minus (axis), never by their own size, against a baseline of 1,099
(`frame-growth-is-not-frame-gain`, `advance-the-baseline-when-accepting-terms`):

| term | gain |
|---|---|
| `intergenerational support` | **+114** |
| `children as investment` | +19 |
| `net cost of children` · `upward transfers` · `downward transfers` | +2 each |
| `economic value of children` | 0 |

`term-acceptance-needs-a-price-ceiling`: a positive gain is not a reason to accept. Five of these six
buy nothing and are rejected. **`intergenerational support` is accepted provisionally and into the
UPWARD arm only**, and its +114 is checked for the elder-care/no-fertility-outcome failure before
production — the six `OFF_OUTCOME` records among the inherited seeds are all of exactly that shape,
and "intergenerational support" is the phrase they use.

---

## 4. A two-link conjunction whose better-identified link is already written, and negligible

The registered claim is a chain:

> modernization → the net flow reverses → the economic rationale for high fertility disappears →
> fertility falls

Link 1 (does the flow reverse?) is a measurement question, and the measurement tradition above
answers it. Link 2 (does the reversal reduce fertility?) is this chapter's parameter.

**Link 2's best-identified corner has already been done, by C.3.c, and it came back negligible.** A
state pension is a public substitute for old-age support from children: where it expands, the upward
flow's value falls, which is a clean and policy-timed move in one component of the net flow. That is
the pension-crowdout literature — 433 records with a fertility outcome, 26 identified designs
(`376`), the densest identification anywhere near this hypothesis. The old-age-security chapter is
closed. Its FDT verdict is **NEGLIGIBLE**: 0.0677 births per woman, 2.3% of a three-birth decline,
GRADE **VERY LOW**, with MINOR reachable only under universal pension coverage that no FDT-era
society had.

Two things follow, and they pull in opposite directions.

**It bounds a component, not the mechanism.** Pension expansion moves the *public* substitute for one
side of the flow. Caldwell's claim is about the whole private net flow reversing under mass schooling
and the transformation of the household — a much larger object, and one no pension reform
approximates. C.3.c's number is a floor on what its own corner can contribute, not a ceiling on
C.3.f.

**And it is the most informative prior available.** The one place where this mechanism has been
identified with policy variation, measured with a dose, and carried through to a demographic share
produced 2.3% of the FDT. A chapter that expects a large answer needs to say why its uncontaminated
variation should behave so differently from its cleanest corner. This is the same shape as C.3.d's
§4, where the middle link's best identification ran against the claim, and it is recorded here before
any evidence is read so that the finding cannot be discovered late and written around.

PI call 4 asks whether C.3.f inherits C.3.c's verdict as a bound on the public-substitute component
or re-opens it. The recommendation is to inherit and cite: re-running a closed chapter's evidence
base under a new name is how one hypothesis becomes two chapters that disagree.

---

## 5. Demographic significance — one phenomenon, and the dose unit named now

FDT is the only registered phenomenon, so this chapter has exactly one demsig cell and no second
chance. `check-all-three-demsig-routes` requires each route to be named and its failure stated before
NOT ASSESSED is written.

**The dose unit is named here, in stage 2, because C.3.c shows what it costs not to.** That chapter's
§5.1 records that no included study reported a fertility response to a *quantified* change in old-age
security — a coverage rate, a replacement rate, a pension-wealth amount — and that "this single
missing unit is what makes the chapter's demographic significance uncomputable." It was foreseeable
without reading a paper. So: **C.3.f's dose unit is the net transfer over childhood expressed as a
share of the recipient's lifetime consumption — the sign and magnitude of the NTA lifecycle deficit,
or a village-study equivalent in adult-consumption units.** `dose_unit` is a required tag (§10), so a
study that reports no dose is visible at extraction rather than at stage 10.

**Route R1, sign.** Did the net flow reverse, in the countries whose fertility fell, across
1870–1965? Pre-registered sign: the hypothesis requires reversal to precede or accompany the decline.

**Route R2, elasticity.** A slope from an identified study times the observed change in the dose.

**Route R3, counterfactual.** Off a single identified historical study, if one exists.

**Say now what would make the cell computable, because on present knowledge it may not be.** National
Transfer Accounts is the only systematic net-flow series and it begins in the 1990s. There is no
net-transfer series for any country covering the First Demographic Transition. The historical
evidence is village measurement — Cain's Bangladesh village, Nag, White and Peet's Java and Nepal
sites, Kaplan's forager and horticulturalist samples — each a single setting at a single period. A
comparison between a 1977 village measurement and a 2000s NTA profile is a **cross-sectional contrast
between two societies presented as a change within one**, and it is not a demsig numerator.

Pre-registered: the FDT cell requires (a) a net-flow measure covering the transition window in at
least two countries on a consistent definition, and (b) a fertility series over the same window. If
(a) fails, R1 falls to R3 off a single identified study; if that also fails, the cell is **NOT
ASSESSED with the failed route named** — never "weak", never a VERY LOW rating attached to a number
that was not computed (`empty-cell-is-the-result`). PI call 5 asks whether a chapter whose only
registered phenomenon ends NOT ASSESSED is an acceptable output. It is: that is a finding about the
state of the evidence, and saying so plainly is worth more than a number built on a two-point
contrast.

Rules inherited, each of which changed an answer on an earlier chapter:

- **The R² criterion is sign-blind** (`r2-criterion-is-sign-blind`). Report the sign first.
- **Do not net a hump to nothing** (`endpoint-test-nets-a-hump-to-nothing`): report peak, amplitude
  and net over a split window.
- **Numerator and denominator share one window** (`demsig-numerator-denominator-window`). Print the
  window beside every share.
- Series go in `data/raw/` with a build script. **`data/raw` is empty** (`data-raw-is-empty`), so this
  is a build, not a fetch.

---

## 6. FDT is registered; PM and SDT are not opened, and here is why that is a live risk

**PM will look well populated and is not this chapter's.** The flow-measurement canon — Cain, Nag,
White and Peet, Kaplan — measures pre-transition and mid-transition societies, and it is the most
substantive material C.3.f has. It is link-1 measurement of the exposure, not a PM cell. Cross-
population variation in what children produce is **C.3.a** (mode of production), unstarted; the
Malthusian resource constraint is **C.4.a**, unstarted. Neither is opened here.

**SDT is not registered but is not scoped out silently.** `identified-evidence-in-the-unnamed-arm`:
on A.23 the named arm had almost no identified designs and the unnamed one did. Remittances,
long-term-care insurance and filial-responsibility law are all SDT-era, and two of them appear in the
inherited seeds. Count identified designs per phenomenon before dropping either, and amend this
document in writing if the unregistered arm turns out to hold the evidence.

---

## 7. Where admissible variation could come from — enumerated before searching

Written before any production query, so that a thin result is a statement about the literature rather
than about our imagination. Volumes from `376`; "crossover" is the intersection with the C.3.f
vocabulary axis.

| # | variation | link | volume | identified | crossover | wall risk |
|---|---|---|---|---|---|---|
| 1 | Pension and social-security expansion substituting for support from children | 2 | 433 | **26** | 19 | **C.3.c owns this and has closed it** (§4) |
| 2 | Inheritance law and land-title reform moving the downward bequest flow | 2 | 291 | 9 | 6 | C.4.a (land), C.1.a (it moves wealth) |
| 3 | Child-labour bans and schooling supply removing the child's contribution | 1→2 | 46 | 11 | 2 | Alexandra's chapter; C.3.a — `same-policy-two-estimands` |
| 4 | Filial-responsibility and family-support law mandating upward support | 2 | 250 **[379]** | **0** | 0 | the null survives widening — see below |
| 5 | Labour-demand shocks raising a child's earning power (mining, cash cropping, colonial labour migration) | 1→2 | 19 **[379]** | 1 | 1 | C.3.a; C.1.a. Two of the four primary seeds are here, and the axis may not reach them |
| 6 | Migrant remittances reversing the flow upward in adulthood | 2 | 429 **[379]** | 18 | 5 | **C.1.a — PI call 2, now largely settled by measurement** |
| 7 | NTA cross-country lifecycle-deficit profiles against fertility | 1 | 425 | — | — | association only; never primary |

**Row 3 is small and is the best-shaped variation on the list.** Forty-six records, eleven of them
identified — a higher identified share than anything else here — and a crossover of 2, meaning the
Caldwell vocabulary is blind to almost all of it. It is also the row most likely to collide with
Alexandra's compulsory-schooling chapter, which owns the same policy through the same mechanism.
Coordinate before building, do not re-derive.

**Row 4 — the null was probed, and it holds. [379]** A law that *mandates* upward support is the
cleanest conceivable move in the upward component. The original 24 records were a spelling artefact:
a law is indexed in its local name (`policy-literatures-indexed-in-the-local-vocabulary`), and across
eight national spellings the legal literature is **250 records**, ten times larger — `maintenance of
parents` alone is 147, the Indian Maintenance and Welfare of Parents Act vocabulary. Of those 250,
**5 carry a fertility outcome and 0 carry an identified design.** The identified-design detector was
validated on three vocabularies where such designs certainly exist and returned 26, 76 and 78, so the
zero is about this literature and not about the detector (`validate-a-null-detector-on-positives`).
**This is now a real finding rather than a thin query**: the cleanest available policy variation in
the upward flow has never been used to estimate a fertility effect.

**Row 6 — PI call 2 is largely settled by measurement. [379]** The remittance literature with a
fertility outcome is 429 records carrying 18 identified designs, which would be the largest
identified block available to this chapter. But only **6** are signed on the transfer with parents
named as recipients, while **40** carry C.1.a income vocabulary. So the literature is overwhelmingly
about what remittances do to household income, which is C.1.a's estimand, and the part that is about
a child-to-parent transfer is about six records.

**Row 5 is a lower bound and its axis is under suspicion. [379]** Nineteen records, one identified.
But one of the four primary seeds is *Lithium-ion batteries and fertility in Africa* — child labour
in mines — and the shock axis here says `mining boom`, not `mining`. Before this row is called thin,
test whether the axis retrieves the seeds already known to sit in it. A count from an axis that
cannot reach its own known positives is not a measurement of the literature.

**The channels fail differently, which is what makes any null here worth something.** Crossovers of
6, 2, 19 and 0 against a 1,099-record frame mean the policy literatures and the theory vocabulary are
near-disjoint (`channels-must-fail-differently`, `empty-cell-needs-second-channel`). A production
query built only from Caldwell's words would find almost none of rows 2, 3 or 4.

---

## 8. The boundary walls

Overlaps measured inside the fertility-restricted frame (`304`, `376`).

| # | wall | rule — separated by *what varies* | overlap | % of frame | neighbour |
|---|---|---|---|---|---|
| 1 | **C.3.c old-age security** | C.3.c owns the **public substitute** for the upward flow — pensions, social security, long-term-care insurance. C.3.f owns the **private net flow**. ⇒ `MIXED_PUBLIC_PRIVATE`, routed out with a note. | **162** | **15%** | **closed** — inherit, do not re-open |
| 2 | **C.3.a mode of production** | C.3.a owns cross-**population** variation in baseline child productive value; C.3.f owns **change over time** in the net flow within a population. ⇒ `MIXED_FLOW_PRODUCTION`. | 5 | 0.5% | unstarted — **PI call 3**; write it inheritable |
| 3 | C.2.b direct costs | C.2.b owns the **price** of a required input; C.3.f owns the **net** of what a child costs against what a child gives. | 19 | 1.7% | drafted |
| 4 | C.3.d quantity-quality | C.3.d owns the **return** to making a child more productive later; C.3.f owns children ceasing to be net producers at all. Inherited verbatim from C.3.d's Wall 8. | 21 | 1.9% | drafted |
| 5 | C.1.a income effect | C.1.a owns **own income**; C.3.f owns the **flow**, holding income fixed. ⇒ `MIXED_FLOW_INCOME`. | 51 **[379]** | 4.6% (0.8% of C.1.a) | unstarted |
| 6 | **D.1.b cultural westernization** | D.1.b owns exposure to a normative model of the modern family; C.3.f owns the transfer. **Written by D.1.b and inherited verbatim**: a study measuring transfers, their direction or their magnitude is C.3.f's even when it cites Caldwell's cultural argument in its framing. | 1 | 0.1% | drafted |
| 7 | A.19 intergenerational transmission of fertility | A.19 owns fertility inherited from parents; C.3.f owns resources moving between them. Shares one word. | 1 | 0.1% | unstarted |
| 8 | Alexandra's compulsory schooling | Her chapter owns the reform through the **child's lost labour value**; C.3.f owns it through the **net flow**. These are close to the same thing — coordinate rather than wall. | 5 | 0.5% | in progress |
| 9 | **direction** (§2) | Not a neighbour but a wall: single-component records are link evidence, never primary and never a demsig numerator. | 227 up / 1,168 down | — | — |
| 10 | **outcome level** | A stated valuation of children is not a realized flow. Never pooled with realized outcomes. | 191 | 17% | — |

**Wall 5 was measured after this document was first frozen, and the answer relocates the risk. [379]**
Read from both sides (`wall-cut-on-wrong-axis`), C.3.f and C.1.a share 51 records: 4.6% of this frame
and 0.8% of C.1.a's 6,397. More to the point, **0 of C.3.f's 18 identified records carry C.1.a
vocabulary** — the population that matters is not contaminated at the vocabulary level at all.

But 0 of 18 is a small denominator, and the risk did not vanish; it moved. The §7 rows that carry the
identification *do* intersect income vocabulary: remittances 40, inheritance and land reform 7,
labour-demand shocks 5. **Wall 5 is a channel-2 wall, not a channel-1 wall** — it will be adjudicated
on the policy-shock records the theory vocabulary cannot see, not on the Caldwell literature. Wall 5
therefore stays a full-text wall and its `MIXED_FLOW_INCOME` cell stays open.

**The small numbers are not reassurance.** C.3.d recorded the same pattern and drew the right
conclusion from it: C.2.f's *vocabulary* overlap with C.3.d was nine records, and at full text eight
of C.2.f's nine included studies could not separate the two estimands. Here, Wall 2 has a
vocabulary overlap of five records and **three of the four primary seeds move the flow through child
labour demand**, which is C.3.a's mechanism. The estimand collision is an order of magnitude larger
than the word collision. Walls 2, 3 and 5 are adjudicated at **full text**, on the mechanism, never
on the title (`design-is-not-a-property-of-the-title`, `read-the-mechanism-not-the-instrument-name`).

---

## 9. Estimand cells

| cell | contents | role |
|---|---|---|
| `NET_FLOW_FERTILITY` | exogenous move in the net direction or magnitude of private transfers → realized fertility | **primary** |
| `SHOCK_NET_FERTILITY` | a policy or labour-demand shock from §7 → realized fertility, with the flow measured or argued | **primary** |
| `UPWARD_COMPONENT` | upward flow alone → fertility | link evidence; never pooled with the net arm |
| `DOWNWARD_COMPONENT` | downward flow or child cost alone → fertility | link evidence; mostly C.2.b's |
| `FLOW_MEASUREMENT` | measures the flow, no fertility outcome — Cain, Nag-White-Peet, NTA profiles | **link 1.** Never primary, never a demsig numerator |
| `VOC_STATED` | elicited valuation of children → intentions or desires | separate outcome level; never pooled with realized |
| `MIXED_PUBLIC_PRIVATE` | a public transfer substituting for the private flow (Wall 1) | C.3.c's; route out with a note |
| `MIXED_FLOW_PRODUCTION` | the flow moves because the production system changed (Wall 2) | jointly claimed with C.3.a, unallocated |
| `MIXED_FLOW_INCOME` | the flow and household income move together (Wall 5) | jointly claimed with C.1.a, unallocated |
| `FLOW_ASSOCIATION` | a flow series against a fertility series, no identified variation | context; never primary, never pooled |
| `REVERSE` | fertility → the flow, or → expectations of support | context. Structurally common here (§11) |
| `THEORY` | Caldwell's statements and their extensions and critiques | context |

`add-a-cell-when-the-rubric-lacks-one`: a real class that does not fit gets a cell mid-screen, added
as code and re-run over completed strata, not forced into `OFF_OTHER`. And a thin cell may be an
unscreened cell (`a-thin-cell-may-be-an-unscreened-cell`).

---

## 10. Required tags on every included empirical effect

| tag | values |
|---|---|
| `flow_direction` | `UPWARD` · `DOWNWARD` · `NET` · `BOTH_MEASURED` — §2. The single most important field |
| `flow_object` | `PRIVATE_FAMILY` · `PUBLIC_TRANSFER` · `MIXED` — Wall 1, made a data field so it is auditable |
| `dose_unit` | `REPORTED` · `DERIVABLE` · `NONE`, plus the unit — §5. C.3.c's missing unit, promoted to a field |
| `sign_convention` | the orientation of the reported coefficient, recorded explicitly, because the arms carry opposite signs by construction |
| `exposure_source` | `CHILD_LABOUR_DEMAND` · `SCHOOLING_LAW` · `INHERITANCE_LAW` · `PENSION` · `FILIAL_LAW` · `REMITTANCE` · `NTA_SERIES` · `VILLAGE_MEASUREMENT` · `SURVEY_INSTRUMENT` |
| `outcome_object` | `FERTILITY` · `FLOW_MAGNITUDE` · `NONE` |
| `outcome_level` | `REALIZED` · `INTENDED` · `DESIRED` · `STATED_VALUATION` |
| `link_measured` | `LINK1_FLOW_REVERSAL` · `LINK2_FERTILITY` · `FULL_CHAIN` |
| `estimator_class` | with a **loud** fall-through — an unlisted correction must raise, never land silently in `uncorrected` (`estimator-class-list-is-a-gate`) |
| `phenomenon_window` | `PM` · `FDT` · `SDT` · `OTHER`, plus a transport note where setting and claimed phenomenon differ |

`flow_direction` and `outcome_object` are separate fields deliberately: a study can measure the net
flow and report no fertility outcome, and that is the modal record here. Screen-stage `design` values
are **hypotheses, not properties**, and every one is re-read at full text.

---

## 11. Identification threats the risk-of-bias pass is looking for

**Reverse causation is structural, not incidental.** How many children support you in old age depends
on how many children you had. The flow is mechanically a function of fertility, so any association
between the two is contaminated in both directions at once, and the contamination has the same sign
as the hypothesis. The inherited seed set already contains one record whose estimate runs
fertility → old-age-support expectations. Every `FLOW_ASSOCIATION` record is presumed contaminated
unless the design says otherwise.

**The exposure is usually inferred rather than measured.** "Children became net liabilities" is
routinely asserted from rising schooling rates or falling child employment, which are proxies for one
component. A study that argues the flow reversed without measuring it has an unmeasured exposure, and
`exposure-estimand-distance-domain` applies: rate how far the measured exposure sits from the
registered one.

**Simultaneity with the neighbours.** Mass schooling moves the flow, the return to child human
capital (C.3.d) and the mother's opportunity cost (C.2.e) together. Land reform moves the flow and
household wealth (C.1.a) together. Wall 5 is where this is adjudicated, and it is unmeasured.

**Selection in the measurement canon.** Village flow studies were sited where the flow was
interesting, and the classic sites are few and repeatedly reanalysed. Treat the canon as a
convenience sample of settings, and count settings rather than papers.

**Common-source bias in the VOC instruments**, where the valuation and the intention are elicited
from the same respondent in the same sitting.

---

## 12. Pooling rule (pre-registered)

Stratify **first**, then apply the ≥3 test to each stratum (`stratify-before-counting-poolable`):

1. `flow_direction` — **never pool across it.** Opposite signs by construction (§2).
2. `outcome_level` — `STATED_VALUATION` never pools with `REALIZED`.
3. `phenomenon_window`.
4. `flow_object` — `PUBLIC_TRANSFER` is C.3.c's and does not enter this chapter's pool at all.

**Predicted now, so that it is a prediction and not a rationalisation later: the
NET × REALIZED × FDT stratum will not reach three studies.** Six records in the entire frame carry
both the net arm and an identified-design marker, before any screening removes the ones that turn out
to measure something else. Narrative synthesis is the expected route, and a meta-analysis would be
the surprise. `an-empty-cell-is-the-result`: if the stratum is empty, the chapter says UNEVALUATED
with the search that failed described, not "weak evidence".

---

## 13. Open PI calls

1. **Is the Value-of-Children survey tradition evidence or background?** 515 records carry the term,
   47% of the frame; 191 sit inside the fertility restriction. It elicits a stated valuation, not a
   realized flow, and reports an intention, not a birth. *Recommendation: background and link-1
   mechanism evidence; never pooled, never a demsig numerator.*
2. **Are migrant remittances to parents an upward flow for our purposes?** Two inherited seeds
   estimate remittances → fertility. They are literally child-to-parent transfers, but D.1.b read the
   Moroccan mechanism as income and human capital, which is C.1.a's. **[379] The measurement mostly
   answers this:** 429 records with a fertility outcome and 18 identified designs, but only 6 signed
   on the transfer with parents named as recipients, against 40 carrying income vocabulary.
   *Recommendation: in scope only where the estimate is signed on the transfer rather than on
   household income, tagged `shared_with: C.1.a`. On the measurement that is roughly six records, so
   the call decides a small cell rather than the chapter — but it decides whether the chapter's
   largest identified block is admissible, so it is still worth a ruling.*
3. **Where does the C.3.a wall sit?** Three of four primary seeds move the flow through child labour
   demand, which is C.3.a's mechanism, and C.3.a is unstarted with a union frame of 1,811.
   *Recommendation: C.3.a owns cross-population variation in baseline child productive value; C.3.f
   owns change over time in the net flow within a population. Written to be inheritable, since C.3.a
   will be scoped against it.*
4. **Does C.3.f inherit C.3.c's closed verdict on the pension corner, or re-open it?** That corner
   holds 433 records and 26 identified designs — the densest identification near this hypothesis —
   and C.3.c rated it NEGLIGIBLE for FDT at GRADE VERY LOW. *Recommendation: inherit and cite, and
   route `MIXED_PUBLIC_PRIVATE` out. Re-running a closed chapter's evidence under a new name produces
   two chapters that disagree.*
5. **Is NOT ASSESSED an acceptable output for a chapter whose only registered phenomenon is FDT?**
   §5 sets out why the FDT demsig cell may be uncomputable: NTA begins in the 1990s and no net-flow
   series covers 1870–1965. *Recommendation: yes, with the failed route named. A two-point contrast
   between a 1977 village and a 2000s NTA profile is a comparison between two societies, not a change
   within one, and presenting it as a demsig share would be worse than declining to compute one.*

---

## Provenance

| artifact | produced by |
|---|---|
| `candidate-frame-probe-2026-09-10.{json,md}` | `source/build/goldset/304_candidate_frame_probe.py` |
| `c3f-term-diagnostics-2026-09-10.{json,md}` | `source/build/goldset/376_c3f_term_diagnostics.py` |
| `c3f-inherited-seeds-2026-09-10.{json,md}` | `source/build/goldset/377_c3f_inherited_seeds.py` |
| `c3f-wall5-null-probe-2026-09-10.{json,md}` | `source/build/goldset/379_c3f_wall5_and_null_probe.py` |
| `c3f-inherited-seeds-routing.md` | hand-read, 2026-09-10 |

Inherited seeds come from branch `063-caldwell-wealth-flows-westernization` at `5859297e`. C.3.c
figures are from `output/chapters/old-age-security-pension-crowdout.md` on `main`. Every number in
this document is quoted from one of the four artifacts above; none is retyped from memory
(`generate-result-tables-never-retype`).
