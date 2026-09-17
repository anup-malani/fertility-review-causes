# Search scope — reduction in stigma around contraception and abortion

**Hypothesis:** A.6, slug `stigma-reduction-contraception-abortion`, HYPOTHESES-v5.md §A.6
**Ticket:** TICK-087 · branch `087-stigma-reduction-contraception-abortion`
**Status:** stage 2, drafted 2026-09-17 (Shravan). The outcome ruling, the frame correction, the six
walls, the estimand cells, the required tags, the pooling rule and the demographic-significance
route are frozen below. Six PI calls open (§13). This ticket was parked and resumed on the same day;
the resumption note in the ticket Log is load-bearing for §3.

**What is measured here and what is not.** Every count comes from
`source/build/goldset/404_a6_term_diagnostics.py` (this branch, commit `9857481`), from
`304_candidate_frame_probe.py` (branch `080-cross-chapter-statistics-comparability`, commit
`31836fb`), or from `405_a3_term_diagnostics.py` (branch `088-diffusion-of-fertility-control`,
commit `23388fd`), with logs beside this file. They are OpenAlex `title_and_abstract.search` record
counts: they size a *retrieval frame* and its overlaps. **No production query has been run, no
anchor resolved, and no record screened.** A count is not an evidence base, and a study can
estimate this chapter's parameter without carrying any of these phrases in its abstract — which,
as §3 shows, is the normal case here.

---

## 1. The claim

Registry: *cultural legitimation of contraception and abortion (independent of technological
availability) lowers fertility by enabling latent demand for fertility control to be realized.*
Phenomena: **FDT, SDT**. Cross-ref: Biological. Seminal: Cleland and Wilson 1987, Bongaarts and
Watkins 1996, Goldin and Katz 2002, Lesthaeghe 1983. Registry note: *Cleland-Wilson 'ideational'
argument vs. Easterlin demand-side; distinguishing norm from technology is hard.*

The chapter's parameter is the change in realized fertility caused by an exogenous fall in the
social cost of being known to control fertility, **holding contraceptive technology and its price
fixed (A.2), holding the legal status of abortion fixed (A.4), holding programme supply and
information fixed (A.5), and holding the content of the underlying value system fixed (D.1.a)**.

**Every clause is load-bearing.**

| clause | what it excludes | wall |
|---|---|---|
| *cultural legitimation* | a technology shock that lowers the monetary or effort price of a method | 1 (A.2) |
| *independent of technological availability* | the registry's own words; the exposure is the social cost of *using* what is already available | 1 (A.2) |
| *(abortion)* | a change in what the law permits, as distinct from what neighbours tolerate | 3 (A.4) |
| *enabling latent demand … to be realized* | a change in demand itself; A.6 requires demand to pre-exist and be suppressed | 5 (D.1.a) |
| *lowers **fertility*** | an effect that stops at contraceptive use and is never carried to a birth | §2, ruling 2 |
| — | supply-side destigmatisation delivered *as part of* a programme | 4 (A.5) |
| — | the spread of the idea, as against its acceptability | 2 (A.3) |

## 2. The rulings

Two structural ambiguities decide what this chapter is. Both are ruled here, before searching.

**Ruling 1 — the exposure is the social cost of use, not the availability of the method.** A.6 and
A.2 can be written over the same event: the arrival of the pill in a country both lowered its price
and changed what using it meant. The rule is that A.6 owns variation in the *social* price holding
the *market* price fixed, and A.2 the reverse. A study that identifies a technology shock and
reports an attitude change as a mediator is A.2 with an A.6 link; a study that identifies a
norm shock — a religious ruling, a media campaign, a cohort discontinuity in reported acceptability
— with method availability unchanged is A.6.

**Ruling 2 — the outcome is realized fertility, and contraceptive use is a link and not a
substitute for it.** This is the ruling that decides whether the chapter exists. A.6's mechanism
runs *through* use: destigmatisation lowers the social cost of using an available method, use
rises, fertility falls. The literature has therefore overwhelmingly taken **use** as its dependent
variable. Measured (`404`, block G): inside the frame, 58 records carry realized-fertility
vocabulary and 122 carry contraceptive-use vocabulary; dropping the fertility outcome axis entirely
takes the use literature from 122 to **479**. So 357 records — 74.5% of the stigma-and-use
literature — are invisible to any fertility-framed search, and the chapter's registered outcome is
carried by at most 58 records before screening.

The reason for ruling on fertility anyway is arithmetic, not taste. A review whose verdict column
is "demographic significance against PM / FDT / SDT" cannot accept an effect on use as its
parameter: use is not a birth, and the conversion from one to the other is Bongaarts' proximate-
determinants arithmetic, which is A.2's and A.13's territory and carries its own contested
parameters. Accepting use as the outcome would silently import that conversion and report it as
A.6's effect. The consequence is that **the honest expected verdict here is an empty or
near-empty primary cell**, and §5 and §12 are written so that this is reported as UNEVALUATED with
the failed route named, never as weak evidence (`empty-cell-is-the-result`).

## 3. Vocabulary diagnosis — the frame that selected this chapter is wrong, and is corrected here

A.6 was selected as the smallest bracketed candidate on a union frame of 680 (`304`, 09-13).
`404` re-measured it at **668** and found two defects.

**Defect 1 — conjunction depth.** Every other pass-4 candidate's union is a flat OR-list of exposure
terms, so applying the outcome axis (304:523) yields a two-block conjunction. A.6's union is
already `(stigma block) AND (object block)`, so the outcome axis makes it a **three-block**
conjunction. Decomposed (`404`, block B):

| frame | n | ×  vs 668 |
|---|---|---|
| stigma AND object AND outcome — as probed | 668 | — |
| stigma AND outcome, object dropped | 3,292 | 4.9 |
| stigma AND object, outcome dropped | 4,875 | 7.3 |
| object AND outcome, stigma dropped | 47,523 | 71.1 |

The outcome block is the most binding and the object block next. A vocabulary miss in a three-block
frame costs two factors rather than one, and 680 was never comparable to the 727 it was ranked
ahead of.

**Defect 2 — the registered construct's own noun is absent.** The registry defines the exposure as
cultural **legitimation**. The stigma block carries only the construct's negative pole: no form of
*legitimation*, *normalisation* or *acceptability*. Restoring them (`404`, block J):

| frame | n |
|---|---|
| as probed | 668 |
| **registered construct restored** — the frame this chapter will use | **1,225** |
| registered construct + `births` in the outcome axis | 2,338 |
| all 17 priced stigma candidates | 1,666 |

Controls reproduce, so this is a frame defect and not index drift: A.3 re-measures at 719 against a
recorded 727 and C.3.a at 1,808 against 1,811; the C.2.c housing control returns 205; `stigma`
unrestricted 202,510 against 202,130.

**The correction does not change this chapter's selection, and that had to be checked rather than
assumed.** `405` applied the same test to A.3, which had displaced A.6 on the uncorrected numbers:
A.3 fails harder — *legitimation* is in A.3's registered claim too, absent from its block, and worth
+865 records alone (719 → 1,584), with all twelve of A.3's own terms giving 2,419. Corrected, A.6 is
1,225 against A.3's 1,584–2,419, so A.6 is the smaller. C.3.a's 1,808 remains uncorrected and sits
between them; the rest of the bracketed table is uncorrected too, which is PI call 3.

### 3A. Candidate terms, priced by marginal gain

Priced as (baseline OR term) − baseline against the 668 frame, never by the term's own size
(`advance-the-baseline-when-accepting-terms`). Accepted terms are those naming the construct's
positive pole, which the registry uses and the block omitted.

| term | gain | ruling |
|---|---|---|
| legitimation | +166 | **accept** — the registry's own noun |
| normalization / normalisation | +202 / +27 | **accept** — both spellings, hyphen folding makes them one test |
| social acceptability | +41 | **accept** |
| disapproval | +130 | **accept** — bare form; the block had only *social disapproval* |
| moral acceptability | +2 | accept, costless |
| legitimacy | +53 | reject — retrieves political-legitimacy senses; *legitimation* carries the construct |
| social norms | +274 | reject — a norm about family size is D.1.a's content, not A.6's social cost |
| secrecy / embarrassment | +31 / +33 | defer — plausible bearers of the construct, but both are outcomes of stigma rather than the exposure |
| religious opposition | +26 | defer to PI call 5 — sits on the D.1.a wall |
| husband opposition | +12 | **accept at screen, not in the frame** — this is the dose unit of §5 |
| opposition to family planning | +22 | accept, costless |
| social sanction / community disapproval / normative pressure | +13 / +1 / +6 | accept, costless |

The object block is by contrast well specified: all ten priced additions together gain **+62**
(668 → 730), and no single addition exceeds +24. It is frozen as probed.

### 3B. The outcome axis, calibrated

| axis | n | gain |
|---|---|---|
| OUTCOME narrow | 601 | −67 |
| OUTCOME_WIDE — as probed | 668 | — |
| + `parity` | 702 | +34 |
| + `completed fertility` | 668 | 0 |
| + `number of children ever born` | 668 | 0 |
| + `births` | 1,164 | **+496** |

`births` is not accepted. At +496 on a 668 base it is retrieving the obstetric and clinical
literature in which "births" is a denominator rather than a demographic outcome — the same reading
the B.5 wall and the 148-record HIV block pick up. `parity` is accepted. The axis is otherwise
frozen as OUTCOME_WIDE.

**Identification, and what the frame is made of.** Inside the 668: **12** records carry an
identified-design marker (**1.8%**), **189** carry qualitative markers (**28.3%**). The frame
retrieves a measurement and advocacy tradition — stigma scales, service-delivery studies, qualitative
accounts of provider and community attitudes — not an identification literature. C.3.f's comparable
figure was 1.6%, so this is the house's normal condition rather than a surprise, but here it lands
on top of ruling 2: of 12 identified records, the number that also carry realized-fertility
vocabulary is not separately measured and is bounded above by 12. **The chapter should expect
between zero and a handful of admissible primary studies** and should be scoped so that outcome is a
finding.

## 4. The chain

The registry calls A.6 a norm hypothesis; mechanically it is three links.

```
  L1  destigmatisation  ->  contraceptive / abortion USE
  L2  use               ->  realized fertility
  L3  destigmatisation  ->  realized fertility          (= L1 x L2, this chapter's parameter)
```

**L3 is the parameter.** L1 is link evidence and is where this literature lives (479 records). L2 is
*not this chapter's to estimate*: it is Bongaarts' proximate-determinants conversion, and it is
already owned — A.2 for method effectiveness and A.13/A.14 for the biological determinants that set
the conversion rate. A.6 may cite L2 but may not re-estimate it, and a study that reports L1 and
multiplies by someone else's L2 is a calibration, not an estimate, and is tagged as such.

**Has a neighbour already answered the best-identified corner?** Recorded before reading evidence,
so the finding cannot be discovered late and written around. The best-identified corner of this
construct is the US Comstock-law and state-level pill-access literature, whose canonical citations
(Goldin and Katz 2002) are registered as seminal for **both** A.6 and A.2. That literature
identifies a *legal and availability* discontinuity. Under ruling 1 it is A.2's, and A.6 inherits it
only as context. If the admissible primary cell ends up empty, this is why: A.6's best-identified
evidence has been assigned to its neighbour by the registry's own seminal list, and that assignment
is PI call 1.

## 5. Demographic significance — the dose unit, named now

**The dose unit is the percentage-point change in the share of non-using women of reproductive age
who cite opposition (own, partner's, or others') or religious prohibition as the main reason for
non-use.** This is chosen because it exists as a repeated, cross-nationally harmonised series: it is
a standard DHS reason-for-non-use item, available across roughly ninety countries and multiple waves
from the mid-1980s. It is the only candidate dose unit for this construct that is both a measure of
*social cost* and available as a time series rather than a single cross-section.

| route | what it needs | failure condition |
|---|---|---|
| **R1 sign** | one admissible study with a signed effect of a norm shock on realized fertility | fails if none of the ≤12 identified records has fertility as its outcome under ruling 2 |
| **R2 elasticity** | a dose-response in the §5 unit, or convertible to it | fails if studies report effects per stigma-*scale* standard deviation with no mapping to the opposition share — the likely case, since scale construction is study-specific |
| **R3 counterfactual** | the DHS opposition series × an R2 elasticity | fails for **FDT** outright: no opposition series exists before the mid-1980s, so the historical phenomenon has no dose series at all. Available in principle for **SDT** in DHS countries, and unavailable for the OECD SDT, where DHS does not run |

**What would make the cell uncomputable, stated now:** for FDT, R3 is unavailable by construction
and R1 requires an identified historical norm shock with a fertility outcome; if neither exists the
FDT cell is **UNEVALUATED — no dose series and no signed estimate**, not "weak evidence". For SDT the
OECD and the DHS worlds fail differently, and the chapter must not pool them: the OECD has the
fertility decline of interest and no opposition series; the DHS countries have the series and are
mostly still in FDT. **This mismatch — the dose is measured where the phenomenon is not — is the
single largest threat to this chapter producing any demographic-significance verdict**, and it is
registered here rather than discovered in stage 10.

## 6. Registered and unregistered phenomena

Registered: **FDT, SDT**. Both are opened. **PM is not registered and is not opened**, though the
construct plainly has a pre-modern reading — the illegitimacy and premarital-sex norms of the
European Marriage Pattern are registered separately under D.2.b, and A.7 owns nuptiality. A.6's
claim is about control *within* unions, so PM is out of scope by the claim rather than by
convenience.

The live risk is the reverse of the usual one. The unregistered arm here is not a phenomenon but an
**outcome**: the 479-record contraceptive-use literature is where this hypothesis's identified
evidence most plausibly sits, and it is excluded by ruling 2. If stage 3 finds identified L1 studies
and no identified L3 studies, the chapter's honest report is that the hypothesis is well evidenced
at a link it does not own and unevidenced at the link it does
(`identified-evidence-in-the-unnamed-arm`). That is PI call 2.

## 7. Admissible variation

Enumerated before searching, so that a thin result is a statement about the literature rather than
about our imagination.

| # | variation | link | volume | identified | crossover | wall risk |
|---|---|---|---|---|---|---|
| 1 | religious ruling or authority change altering acceptability with law and supply fixed | L3 | not measured | plausible | D.1.a (religiosity) | high — wall 5 |
| 2 | mass-media or entertainment-education campaign targeting acceptability | L3 | not measured | strong elsewhere (A.20 holds the Brazil/India TV designs) | A.20, A.3 | high |
| 3 | cohort or period discontinuity in reported acceptability (WVS / DHS attitude items) | L1, L3 | 10 in-frame attitude-scale records | weak — descriptive | D.1.a | medium |
| 4 | provider- or clinic-level destigmatisation with supply held fixed | L1 | inside the 81-record A.5 overlap | plausible | A.5 | **very high** — wall 4 |
| 5 | abortion-stigma change with legal status fixed | L3 | inside the 57-record A.4 overlap | plausible | A.4 | high |
| 6 | partner/husband opposition as an intra-household constraint | L1 | +12 as a term | plausible | D.2.a (bargaining) | medium |
| 7 | legal change *as* a legitimation signal, distinct from access | L3 | inside wall 3 | strong but assigned to A.4 | A.4 | **very high** — the ruling-1 boundary |

Rows 4 and 7 are the ones most likely to decide this chapter, and both sit on walls. That is the
chapter's central difficulty, not an incidental one.

## 8. Boundary walls

Measured from both sides (`wall-cut-on-wrong-axis`); shares are of the 668 frame and of the
neighbour's own outcome-restricted frame. `id` is the count of overlapping records also carrying an
identified-design marker.

| # | wall | rule — separated by *what varies* | overlap | % ours | % theirs | id | neighbour |
|---|---|---|---|---|---|---|---|
| 1 | **A.2** contraceptive technology | A.2 owns the **market price and availability** of a method; A.6 owns the **social price of using** one already available ⇒ `MIXED_NORM_TECH` | 60 | 9.0% | 1.1% | 1 | **unstarted** |
| 2 | **A.3** diffusion of fertility control | A.3 owns **whether the idea has arrived**; A.6 owns **whether it is acceptable once it has** ⇒ `MIXED_NORM_DIFFUSION` | 2 | 0.3% | 0.4% | 0 | **unstarted** (TICK-088, parked) |
| 3 | **A.4** induced abortion access | A.4 owns **what the law permits**; A.6 owns **what the community tolerates at fixed legality** ⇒ `MIXED_NORM_LAW` | 57 | 8.5% | 2.7% | 1 | **unstarted** |
| 4 | **A.5** family planning programmes | A.5 owns **supply, information and subsidy**; A.6 owns the **social cost of use** ⇒ `MIXED_NORM_SUPPLY` | 81 | 12.1% | 1.4% | 3 | **unstarted** |
| 5 | **D.1.a** postmaterialism and secularisation | D.1.a owns **what people value**; A.6 owns **what they can be seen doing at fixed values** ⇒ `MIXED_NORM_SECULAR` | 6 | 0.9% | 0.4% | 0 | **drafted — inheritable** |
| 6 | **B.5** fetal loss (clinical homonym) | B.5 owns **spontaneous** pregnancy loss; "abortion stigma" in that literature is a different construct ⇒ `OFF_CLINICAL_LOSS` | 51 | 7.6% | 0.3% | 3 | drafted |

**Four of six neighbours are unstarted, so four of these walls must be written inheritable** — A.2,
A.3, A.4 and A.5 will be scoped *against* this document, and each rule above is phrased as a
two-sided ownership sentence for that reason. The usual move of citing the neighbour's frozen scope
is unavailable.

**The small numbers are not reassurance.** Wall 2 is the clearest case: A.6 and A.3 overlap on **2
records** while sharing **two of A.6's four registered seminals** (Cleland and Wilson 1987;
Bongaarts and Watkins 1996). The vocabularies part and the construct does not. C.3.d's inherited
finding is the precedent — a 9-record overlap, and 8 of 9 full texts could not separate the
estimands. So every `MIXED_*` cell stays open, and all six walls are adjudicated **at full text on
the mechanism**, never on the title or the instrument name
(`read-the-mechanism-not-the-instrument-name`, `design-is-not-a-property-of-the-title`).

**Homonym contamination inside our own frame.** The object block does not exclude the other stigma
literatures: HIV and sexual health **148** records (22.2% of the frame), mental illness **92**
(13.8%), obesity 19, leprosy/TB/epilepsy 14. HIV-stigma affecting contraceptive and fertility
decisions is a real and substantial literature and it is **not** this chapter's construct. At 22% it
is too large to route silently and gets its own cell (PI call 6).

## 9. Estimand cells

| cell | contents | role |
|---|---|---|
| `PRIMARY_NORM_FERTILITY` | identified effect of a norm/legitimation shock on realized fertility, technology, law and supply fixed | **primary** |
| `LINK_NORM_USE` | effect of the same shock on contraceptive or abortion use | link evidence (L1) |
| `LINK_USE_FERTILITY` | the proximate-determinants conversion | context — cited, never re-estimated here |
| `CONTEXT_STIGMA_MEASURE` | stigma scale construction, prevalence, qualitative accounts | context |
| `MIXED_NORM_TECH` | norm and technology vary together | route-out → A.2, note |
| `MIXED_NORM_DIFFUSION` | arrival and acceptability vary together | route-out → A.3, note |
| `MIXED_NORM_LAW` | legality and tolerance vary together | route-out → A.4, note |
| `MIXED_NORM_SUPPLY` | programme supply bundled with destigmatisation | route-out → A.5, note |
| `MIXED_NORM_SECULAR` | values and acceptability vary together | route-out → D.1.a, note |
| `OFF_CLINICAL_LOSS` | "abortion" as spontaneous loss | off-cell |
| `OFF_HIV_STIGMA` | HIV/STI stigma as the exposure | off-cell, own cell by volume |
| `OFF_OTHER_STIGMA` | mental illness, obesity, infectious disease | off-cell |
| `OFF_OTHER` | everything else | off-cell |

A real class that arrives mid-screen gets its own cell and the rubric is re-run over completed
strata rather than forcing it into `OFF_OTHER` (`add-a-cell-when-the-rubric-lacks-one`); and a thin
cell is treated as possibly an unscreened cell until the strata are complete
(`a-thin-cell-may-be-an-unscreened-cell`).

## 10. Required tags

| tag | values |
|---|---|
| `outcome_level` | `REALIZED` · `INTENDED` · `DESIRED` · `USE` · `STATED_ATTITUDE` |
| `dose_unit` | `REPORTED` (in §5's opposition-share unit) · `DERIVABLE` · `NONE` |
| `phenomenon_window` | `FDT` · `SDT` · `BOTH` · `NEITHER` |
| `estimator_class` | `IV` · `DID` · `RDD` · `RCT` · `EVENT_STUDY` · `SYNTH` · `OLS_ADJUSTED` · `DESCRIPTIVE` · `QUALITATIVE` · `SIMULATION` · `OTHER_LOUD` |
| `stigma_object` | `CONTRACEPTION` · `ABORTION` · `FAMILY_PLANNING` · `MIXED` |
| `stigma_bearer` | `SELF` · `PARTNER` · `COMMUNITY` · `PROVIDER` · `INSTITUTIONAL` |

`estimator_class` falls through **loudly**: an unmatched design raises rather than defaulting
(`estimator-class-list-is-a-gate`). `USE` is a value of `outcome_level` and not of the primary cell —
that is ruling 2 enforced at the tag level. Screen-stage `estimator_class` values are hypotheses,
not properties, and are re-read at full text.

## 11. Identification threats

- **Reverse causation is structural here, not incidental.** Falling fertility normalises fertility
  control: the behaviour becomes common, and commonness is what destigmatisation *is*. Stigma and
  fertility are mutually determined over exactly the period of interest, so a design without an
  exogenous norm shock is not weakly identified but unidentified. Risk-of-bias will hunt for this
  first.
- **Stigma is measured by self-report on the treated.** A respondent who has internalised
  destigmatisation reports less stigma *and* uses contraception; common-method bias runs in the
  direction of the hypothesis. The D.3.b risk-of-bias instrument added a common-method-bias domain
  (TICK-050) and this chapter should inherit it.
- **Scale non-comparability.** Stigma scales are study-specific, so a pooled standardised effect
  averages instruments measuring different constructs. This is why §5's dose unit is the DHS
  opposition item rather than a scale score.
- **Bundling.** Walls 4 and 7 are not measurement problems but treatment-definition problems:
  programmes and laws arrive as packages, and the norm component is rarely separately dosed.

## 12. Pooling rule (pre-registered)

Stratify first, then apply the ≥3 rule within stratum (`stratify-before-counting-poolable`). Strata
in priority order:

1. `PRIMARY_NORM_FERTILITY` × `FDT`
2. `PRIMARY_NORM_FERTILITY` × `SDT`
3. `LINK_NORM_USE` × `SDT`
4. `LINK_NORM_USE` × `FDT`

**Never pooled across:** `outcome_level` (a use effect and a fertility effect are different
parameters), and the OECD/DHS divide within `SDT` (§5 — the dose is measured where the phenomenon is
not).

**Predicted now, so that it is a prediction and not a rationalisation later.** Strata 1 and 2 will
each contain **fewer than 3** admissible effects; stratum 1 will most likely be **empty**. Stratum 3
will be poolable and is not this chapter's parameter. Therefore: narrative synthesis for the primary
cell, and if strata 1 and 2 are empty the verdict is **UNEVALUATED** with the failed route named —
R1 for want of an identified fertility outcome, R3 for want of a pre-1985 dose series — and
explicitly **not** "weak evidence" (`empty-cell-is-the-result`). A pooled estimate will be reported
for stratum 3 only under a heading that says it is the link and not the claim.

## 13. Open PI calls

1. **Is A.6 separable from A.2, given that the registry assigns Goldin and Katz 2002 to both?**
   Wall 1 overlap is 60 records, 9.0% of our frame, with 1 identified. §4 records that A.6's
   best-identified corner — the US pill-access and Comstock literature — is A.2's under ruling 1.
   *Recommendation: keep the wall as ruled and accept that A.6's primary cell may be empty as a
   result. The alternative — letting A.6 claim legal-access designs as legitimation signals —
   makes A.6 unfalsifiable and duplicates A.4.*

2. **Does A.6 own the contraceptive-use link, or only the fertility effect?** 479 records take use
   as the outcome against 58 carrying realized fertility. Ruling 2 says fertility; that ruling is
   what makes the primary cell nearly empty. *Recommendation: hold ruling 2, and report the use
   literature as `LINK_NORM_USE` with its own pooled estimate under a heading that disclaims it as
   the chapter's parameter. Relaxing the ruling would silently import Bongaarts' conversion and
   report it as A.6's effect.*

3. **Should the whole bracketed candidate ranking be re-run before more chapters are opened?** Two
   of two candidates tested failed the registered-construct completeness test (A.6 668 → 1,225;
   A.3 719 → 2,419), and A.6 additionally failed on conjunction depth. C.3.a, D.2.c, C.2.e, C.4.a,
   A.19, A.4, C.2.d and C.1.a are uncorrected. *Recommendation: fix `304` under TICK-080 to check
   the registry's own nouns and to record conjunction depth, then re-rank. This does not block
   TICK-087, which the PI has directed to proceed regardless of whether other candidates are
   smaller.*

4. **Is A.5 a wall or a bundle?** 81 records, 12.1% of our frame — the largest wall — and 3 of the
   5 identified records across the five substantive walls sit in it (A.2 1, A.3 0, A.4 1, A.5 3,
   D.1.a 0; B.5's 3 are excluded as a clinical homonym rather than a wall). Family-planning programmes routinely include
   destigmatisation as a designed component. *Recommendation: treat A.5 as a bundle rather than a
   wall: admit programme studies to `MIXED_NORM_SUPPLY` and require the full-text screen to ask
   whether the norm component was separately dosed. A pure wall here would discard the chapter's
   best-identified candidates unread.*

5. **Does religious opposition belong to A.6 or D.1.a?** The term gains +26. D.1.a is drafted and
   its scope is inheritable. *Recommendation: A.6 owns a religious authority's ruling as an
   exogenous shock to acceptability; D.1.a owns the secular decline in religiosity as a value
   change. Confirm against D.1.a's frozen scope before stage 3.*

6. **HIV-stigma is 22% of the frame. Route out, or open a cell?** 148 records, against 92 for
   mental-illness stigma. *Recommendation: its own cell `OFF_HIV_STIGMA` rather than `OFF_OTHER`,
   because at this volume it will otherwise dominate the off-cell counts and hide the rest, and
   because a subset of it — HIV-status stigma suppressing contraceptive use — may be admissible
   link evidence on inspection.*

## Provenance

| artifact | produced by |
|---|---|
| `literature/search-logs/a6-term-diagnostics-2026-09-17.{json,md}` | `source/build/goldset/404_a6_term_diagnostics.py`, this branch, commit `9857481` |
| `literature/search-logs/candidate-frame-probe-2026-09-13.{json,md}` | `source/build/goldset/304_candidate_frame_probe.py`, branch `080-cross-chapter-statistics-comparability`, commit `31836fb` |
| `literature/search-logs/a3-term-diagnostics-2026-09-17.{json,md}` | `source/build/goldset/405_a3_term_diagnostics.py`, branch `088-diffusion-of-fertility-control`, commit `23388fd` |
| the registry claim, phenomena, seminal list and note | `HYPOTHESES-v5.md` §A.6 |

Every number in this document is quoted from one of the artifacts above; none is retyped from memory
(`generate-result-tables-never-retype`).
