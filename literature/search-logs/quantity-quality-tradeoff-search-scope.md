# Search scope — the quantity-quality tradeoff

**Hypothesis:** C.3.d, slug `quantity-quality-tradeoff`, HYPOTHESES-v5.md §C.3.d
**Ticket:** TICK-083 · branch `083-quantity-quality-tradeoff`
**Status:** stage 2, drafted 2026-09-09 (Shravan). Walls, estimand cells, required tags, the pooling
rule and both demographic-significance routes are frozen below. Five PI calls open (§13).

**What is measured here and what is not.** Every count below comes from
`source/build/goldset/344_c3d_term_diagnostics.py`, `345_c3d_outcome_axis_and_direction.py` and
`346_c3d_forward_channel_and_walls.py`, with logs beside this file. They are OpenAlex title/abstract
record counts: they size a *retrieval frame* and its overlaps. **No production query has been run, no
anchor resolved, and no record screened.** A count is not an evidence base, and a record can estimate
this chapter's parameter without carrying any of these phrases in its abstract.

---

## 1. The claim

Registry: *rising returns to child human capital raise the shadow price of an additional child
relative to investing more in each existing child, lowering desired fertility as parents substitute
quality for quantity; skill-biased technical change is the labor-market force driving this
reallocation.* Phenomena: **FDT and SDT**. Cross-ref: none recorded. Seminal: Becker 1960, Becker and
Lewis 1973, Becker and Tomes 1976, Galor and Weil 2000, Galor and Moav 2002, Doepke 2004, Greenwood
Seshadri and Vandenbroucke 2005. Registry notes: *absorbs `skill-biased-technical-change`; micro
evidence mixed (Black-Devereux-Salvanes 2005 finds little tradeoff); macro role central in unified
growth theory.*

The chapter's parameter is the change in completed fertility caused by an exogenous rise in the
**return to the human capital of one's own children**, operating through the substitution of
investment per child for number of children, holding own income and the return to the *parents'* own
human capital fixed.

Every clause is load-bearing. "Return" rather than reference standard is Wall 1 (C.2.f). "Of one's
own children" rather than of the parents is **Wall 2 (C.2.e), the wall this scope adds and the one
most likely to be violated silently**. "Holding own income fixed" is Wall 4 (C.1.a). And "completed
fertility" — rather than investment per child, or children's attainment — is §2, the ruling that
decides what this chapter is.

---

## 2. The direction ruling — and it is the ruling that decides the chapter

**The registered claim runs forward. The famous literature runs backward. They are different
estimands and only one of them answers the registry.**

| direction | question | outcome | canonical work |
|---|---|---|---|
| **FORWARD** | does an exogenous rise in the return to child human capital lower fertility? | **fertility** | Galor–Weil, Becker–Murphy–Tamura |
| **BACKWARD** | does an exogenous rise in family size lower investment or attainment per child? | **children's outcomes** | Black–Devereux–Salvanes 2005, Angrist–Lavy–Schlosser 2010, Rosenzweig–Wolpin 1980 |

Both are called "the quantity-quality tradeoff" in ordinary speech. Only the forward direction has
fertility as its dependent variable, and the registry's outcome is fertility.

This matters because **the registry cites the backward literature as evidence about C.3.d.** Its own
note says "micro evidence mixed (Black-Devereux-Salvanes 2005 finds little tradeoff)". BDS instruments
family size with twin births and reads off children's education. It is a superb study and it does not
estimate the registered parameter. `anchor-on-the-estimand-not-the-famous-design`: on C.3.e the
celebrated designs did not measure the outcome at all, 112 term-only against 2 provenance-only hits.

**Ruling.** The **forward** arm is C.3.d's primary cell. The **backward** arm is admitted as
**mechanism evidence on link 2** (§4) and is tagged `direction=BACKWARD`. It is never pooled with the
forward arm, and it **cannot carry a demographic-significance number**, because a demsig share needs a
fertility numerator and the backward arm has none. `outcome-level-separates-channels` applies with
extra force here: this is not two levels of one outcome, it is two different outcomes.

Measured, inside the 762-record frame (`345`):

| | n |
|---|---|
| forward: returns-to-skill exposure **and** a fertility outcome | 8 → **16** (`346`, two more spellings) |
| backward: child-outcome vocabulary | 200 |
| backward **with an identified family-size design** | 35 |
| carrying both outcomes | 98 |

**The doubling from 8 to 16 on two added spellings is itself a warning** and is why §3 exists.

---

## 3. The theory's own vocabulary does not index the studies that test the theory

This is the central retrieval finding and it changes how the chapter must be searched.

The exposure axis looks healthy. Unlike C.2.f — whose frame turned out to be 89% one general-purpose
term — C.3.d's dominant term is the mechanism's proper name (`344`):

| term | fertility-restricted | bare |
|---|---|---|
| `quantity-quality` | **494** (65% of the frame) | 8,154 |
| `child quality` | 243 | 793 |
| `quantity quality tradeoff` | 95 | 162 |
| `child investment` | 40 | 125 |
| `human capital of children` | 31 | 182 |
| `sibsize` | 27 | 69 |

Dropping `child quality` costs 176 records; dropping `child investment` costs 30. **The homonym worry
was tested and cleared**: "fertility" is a soil-science and animal-husbandry word and
`quantity-quality` is a stock phrase in both, but the non-human residue inside the frame is **43 of
762 (5.6%)**, and 42 of the 43 sit under the single outcome word `fertility` — the other five outcome
terms carry 0, 0, 0, 2, 0 (`345`). On A.24 the same pattern was 16.8%, so it was worth the queries.

**And none of that helps, because the empirical literature is named after its designs.** Measured
across `344`, `345`, `346`:

| | n |
|---|---|
| forward arm on channel 1, **inside** the C.3.d frame | 16 |
| forward arm on channel 1, **not** restricted to the frame | **231** |
| family-size-shock records (twins, sex composition) overall | 4,690 |
| …of which use any C.3.d term | **61** |
| twins × child-outcome vocabulary, outside the axis | 1,562 |
| channel-2 shock axis × fertility | **770** |
| …of which are in the C.3.d frame | **15** |

93% of the channel-1 forward arm and 98% of the channel-2 shock literature sit outside C.3.d's own
vocabulary. **A production query built on the theory axis retrieves the theoretical literature and
misses the empirical one.** This is `sub-literature-renames-the-outcome` (A.18 lost 7 of 9 SELECTION
anchors because that literature calls fertility "fitness") and
`policy-literatures-indexed-in-the-local-vocabulary` (worth +40% of A.23's frame) arriving together.

**Consequence, pre-registered: the production query has THREE axes, not one.**

1. **Theory axis** — the 762-record frame above, plus the candidate terms in §3A.
2. **Design axis** — twin births, sibling sex composition, compulsory-schooling reforms, school
   construction, family-size instruments.
3. **Shock axis** — import competition and the China shock, robot and computer adoption, schooling
   supply expansion, historical industrialization, occupational structure, local labour-demand shocks.

Each axis is intersected with the outcome axis separately and the results unioned. **Recall is
checked per axis**, not in aggregate — `diagnostic-and-retrieval-vocabularies-differ` and
`sub-literature-renames-the-outcome` both say a pooled recall number hides an arm that is failing.

### 3A. Candidate terms, priced by marginal gain

`advance-the-baseline-when-accepting-terms`: a candidate scored against a frozen baseline is credited
with records earlier terms already had — on A.23 that kept 17 terms where 4 were warranted.
Every candidate below was priced as `(axis OR term) − axis` (`344`).

| candidate | marginal gain |
|---|---|
| `parental investment` | +332 |
| `human capital investment` | +306 |
| `investment in children` | +182 |
| `sibship size` | +182 |
| `quality-quantity` (the reversed hyphenation) | +138 |
| `resource dilution` | +62 |
| `family size and educational attainment` | +42 |
| `child human capital` | +14 |
| `dilution of resources` | +2 |
| `education-fertility tradeoff` | +0 |

**None of these is accepted yet.** `frame-growth-is-not-frame-gain`: "emancipation" grew A.23's frame
40% for zero gold. Each is run alone against the anchor set at stage 3 and kept only if it carries
gold. `quality-quantity` is the most likely to survive (a real journal usage, not a new concept);
`parental investment` and `human capital investment` are the most likely to be pure growth, since
both are general developmental-psychology and macro vocabulary.

---

## 4. The mechanism is a three-link conjunction and the middle link's best evidence is negative

Return to child human capital rises → parents substitute quality for quantity → fertility falls.

| link | claim | where the evidence is | measured |
|---|---|---|---|
| 1 | the return to child human capital rose | economic history, labour economics | 231 (ch1), 770 (ch2 shocks) |
| 2 | quantity and quality genuinely trade off | the **backward** twins / sex-composition literature | 1,562 outside the axis, 35 identified inside |
| 3 | the composite lowers completed fertility | the **forward** arm | 16 in frame, 231 out |

`b7-antidepressants` and D.3.c both say: count identified estimates per link before writing a verdict,
and do not let a well-populated outer link stand in for the chain. Here the shape is unusual and worth
stating now, because it will drive the GRADE rating:

**Link 2's best-identified evidence runs against the mechanism.** The registry says so itself. BDS
2005 (Norwegian twins) finds little tradeoff; Angrist–Lavy–Schlosser (Israel) find essentially none;
Qian finds a positive effect in China. The twin-instrument design is the cleanest identification in
the whole hypothesis and it largely fails to find the substitution the theory requires.

**So the chapter is likely to conclude that the theoretically central mechanism has strong
identification and weak support at its middle link, while its registered forward link is measured
almost entirely outside its own vocabulary.** That is a prediction recorded before searching, so a
result matching it is a finding and a result contradicting it is a correction — not a story fitted
afterwards.

---

## 5. Demographic significance — two phenomena, two routes, both named before searching

Per `three-demsig-routes-before-not-assessed`, name the live route for each phenomenon separately and
say which failed before ever writing NOT ASSESSED. `check-all-three-demsig-routes`.

**SDT (1965–present). Route: R2 elasticity, with R1 sign as a gate.** The exposure series exists —
the US college wage premium (Goldin–Katz, Autor), OECD returns-to-schooling series, Psacharopoulos–
Patrinos. Pre-registered sign: the hypothesis requires the return to child human capital to have
**risen** across the SDT window in the countries whose fertility fell.

**This test is weaker than C.2.f's and is expected to pass in the Anglosphere and fail in
continental Europe.** The US and UK college premium rose sharply after ~1980; the French and German
premia were roughly flat, and Nordic premia compressed — while fertility fell in all of them. So
unlike C.2.f, where the sign settled the cell, here the sign is likely to **split by country**, and
the honest output is a country-stratified sign table rather than a single verdict. Pre-registered:
if the premium did not rise where fertility fell, those countries are settled by sign regardless of
any elasticity.

**FDT (~1870–1965). Route: R1 sign first; R2 elasticity only if a defensible series exists.**
Historical returns-to-schooling series are thin, country-specific and reconstructed. Candidates:
Goldin–Katz for the US 1915–2005, Long and Crafts for Britain, Prussian and Swedish school data.
**Say now what would make this cell computable**, so stage 10 does not discover it is not: the FDT
cell needs (a) a returns series covering the transition window in at least three countries, and (b)
a fertility series over the same window. If (a) fails, the FDT route falls back to **R3 counterfactual**
off a single identified historical study, and if that also fails the cell is **NOT ASSESSED with the
failed route named** — never "weak", never VERY LOW. `empty-cell-is-the-result`.

Rules inherited, both of which changed an answer on an earlier chapter:

- **The R² criterion is sign-blind** (`r2-criterion-is-sign-blind`): six of six countries cleared
  PROTOCOL's 0.15 with the correlation running against the hypothesis. Report the sign first.
- **Do not net a hump to nothing** (`endpoint-test-nets-a-hump-to-nothing`): report peak, amplitude
  and net/amplitude across a split window. An endpoint test read C.6.a as 0/18 where a split window
  read 14/18 early and 0/18 late.
- **Numerator and denominator share one window** (`demsig-numerator-denominator-window`): a 1978+
  exposure over a 1967+ decline inflated C.2.b's shares from 44% to 196%. Print the window beside
  every share.
- Series go in `data/raw/` with a build script. **`data/raw` is currently empty** apart from two
  ad-hoc pulls on unmerged branches, so this is a build, not a fetch (`data-raw-is-empty`).

---

## 6. Both phenomena are registered, and neither arm is quietly dropped

C.3.d is one of the few entries registered for **FDT and SDT** both. Most recent chapters have been
SDT-only and the habit is a hazard. `identified-evidence-in-the-unnamed-arm`: on A.23 the *named* arm
had almost no identified designs and the unnamed one did. Count identified designs per phenomenon
before scoping either out, and amend this document in writing if one is dropped.

PM is **not** registered and is not opened. The pre-modern quantity-quality argument belongs to C.3.a
(mode of production) and C.4.a (Malthusian constraints), both unstarted.

---

## 7. Where admissible variation could come from — enumerated before searching

Written before any query so a thin result is a statement about the literature rather than about our
imagination. Each row is a prediction to test. Volumes are from `344`–`346`.

| # | variation | link | direction | measured volume | wall risk |
|---|---|---|---|---|---|
| 1 | Trade / import-competition exposure shifting the local skill premium | 1→3 | FORWARD | 88 | C.5.a (the same shock raises uncertainty); C.1.a (it moves income) |
| 2 | Robot and computer adoption shifting skill demand | 1→3 | FORWARD | 27 | C.2.e if it displaces *women's* work |
| 3 | Schooling supply expansion — school construction, universal primary education | 1→3 | FORWARD | 188 | **C.2.e** and Alexandra's compulsory-schooling chapter; `same-policy-two-estimands` |
| 4 | Historical industrialization and the rise of literacy | 1→3 | FORWARD | 275 | C.3.f (children stop producing); C.3.a |
| 5 | Occupational-structure / white-collar shift | 1→3 | FORWARD | 329 | C.2.g urbanization moves with it |
| 6 | Local labour-demand shocks to skill | 1→3 | FORWARD | 23 | C.1.a directly |
| 7 | Twin births as an instrument for family size | 2 | BACKWARD | 4,690 (61 in axis) | **A.12** owns twinning as an exposure; here it is an instrument |
| 8 | Sibling sex composition as an instrument for family size | 2 | BACKWARD | inside row 7 | D.2.c son preference where sex composition is chosen |
| 9 | Compulsory-schooling / school-leaving-age reforms | 1 or 2 | either | 364 neighbour frame | **Alexandra's chapter**; the reform moves child labour value *and* the return |
| 10 | Returns-to-schooling time series vs fertility, no identified variation | 1→3 | FORWARD | large | `RETURN_ASSOCIATION`, context only |
| 11 | Elicited beliefs about returns vs desired family size | 1→3 | FORWARD | very thin | `PERCEIVED` outcome level, never pooled with realized |

**Rows 1–6 are the rows to hunt**, and row 3 is the largest. 35 of the 770 channel-2 records carry an
identified-design marker (`346`), so identified forward variation exists and the search must reach it.
`one-study-can-carry-the-structure`: a single design estimating both investment per child and
fertility off one shock beats any cross-literature count, and rows 1–6 are where such a design lives.

**Channels, per `channels-must-fail-differently`.** Channel 1 is the economics-of-education
vocabulary (returns to schooling, skill premium). Channel 2 is the six shock literatures in their own
local words. Their measured intersection is 0, 0, 2, 11, 1 and 3 records — they do not merely fail
differently, they barely meet. A null on both would therefore be worth something. Channel 3, if both
thin out, is provenance: forward citations of Becker–Lewis and Galor–Weil, and the reference lists of
the twin-instrument papers.

---

## 8. The boundary walls

Contamination measured 2026-09-09 inside the fertility-restricted frame, **from both sides** (`346`),
because an overlap read from one side says only which frame is bigger (`wall-cut-on-wrong-axis`).

| # | wall | rule — separated by *what varies* | neighbour frame | overlap | % of C.3.d | neighbour |
|---|---|---|---|---|---|---|
| 1 | **C.2.f status competition** | C.3.d owns the **return** to child quality; C.2.f owns the **reference standard**. Inherited verbatim from C.2.f §2. Inseparable ⇒ `MIXED_RETURN_POSITION`. | 718 | **9** | 1.2% | drafted — **PI call 3 is open on whether this wall holds at all** |
| 2 | **C.2.e female wage / opportunity cost** | **The wall this scope adds.** C.3.d owns the return to the **child's** human capital; C.2.e owns the return to the **parent's**. A schooling-supply shock moves both. ⇒ `MIXED_CHILD_PARENT_RETURN`. | 1,738 | 13 | 1.7% | unstarted — write it inheritable |
| 3 | C.2.b direct costs | C.2.b owns the **price** of a required input; C.3.d owns the **quantity** of investment chosen because its return rose. | 326 | 12 | 1.6% | drafted |
| 4 | C.1.a income effect | C.1.a owns **own income**; C.3.d owns the **return**, holding income fixed. Almost every shock in §7 moves both. | 421 | 20 | 2.6% | unstarted |
| 5 | **A.12 twinning** | A.12 owns twinning **as an exposure** (an accounting identity on the birth rate); C.3.d uses twin births **as an instrument** for family size. Same variable, different roles — `snowball-the-estimand-not-the-estimator`. **Check A.12's pool before building one.** | 5,550 | **60** | 7.9% | drafted |
| 6 | A.1 child mortality | A.1 owns **survival**; investment is riskier when children die, which is Becker's own quantity-quality-with-mortality. Largest raw overlap after A.12. | 7,416 | **38** | 5.0% | unstarted |
| 7 | Alexandra's compulsory schooling | Her chapter owns the reform's effect through **child labour value**; C.3.d owns it through the **return to schooling**. `same-policy-two-estimands`. Coordinate rather than re-derive. | 364 | 6 | 0.8% | in progress (TICK-031/032) |
| 8 | C.3.f wealth flows | C.3.f owns children ceasing to be **net producers**; C.3.d owns the return to making them more productive later. | 859 | 11 | 1.4% | unstarted |
| 9 | D.2.d intensive parenting | D.2.d owns the **norm** defining what a proper child requires; C.3.d owns the **return** that makes investment pay. | 40 | **0** | 0% | drafted |
| 10 | **direction** (§2) | Not a neighbour but a wall: BACKWARD records are mechanism evidence on link 2, never a primary effect and never a demsig numerator. | — | 200 in frame | 26% | — |

**The wall numbers are small and must not be read as reassurance.** Every vocabulary overlap here is
under 8%. C.2.f's overlap with this chapter is **nine records, 1.2%** — and C.2.f found that **eight
of its nine included studies could not separate the return from the reference standard**, at full
text. The estimand collision is an order of magnitude larger than the word collision. A count of
shared phrases bounds shared vocabulary and says nothing about shared parameters, which is exactly
why ruling 1 cannot be discharged by this table. Walls 1, 2 and 4 are adjudicated at **full text**,
on the mechanism, not on the title (`design-is-not-a-property-of-the-title`,
`read-the-mechanism-not-the-instrument-name`).

---

## 9. Estimand cells

| cell | contents | role |
|---|---|---|
| `RETURN_FERTILITY` | exogenous move in the return to child human capital → realized fertility | **primary, forward** |
| `SHOCK_FERTILITY` | trade / technology / schooling-supply / industrialization shock → realized fertility, with the return measured or argued | **primary, forward** |
| `QQ_SUBSTITUTION` | exogenous family size → investment or attainment per child | **link 2, backward.** Mechanism evidence. Never primary, never a demsig numerator |
| `MIXED_RETURN_POSITION` | return and reference standard move together (Wall 1) | jointly claimed with C.2.f, unallocated |
| `MIXED_CHILD_PARENT_RETURN` | the child's and the parent's returns move together (Wall 2) | jointly claimed with C.2.e, unallocated |
| `MIXED_RETURN_INCOME` | return and own income move together (Wall 4) | jointly claimed with C.1.a, unallocated |
| `RETURN_ASSOCIATION` | returns series vs fertility series, no identified variation | context; never primary, never pooled |
| `PERCEIVED_RETURN` | elicited beliefs about returns → intentions or desires | **separate outcome level; never pooled with realized** |
| `THEORY` | unified-growth and calibrated OLG models | context. **A calibration is not an identified estimate** (§13 call 4) |

`add-a-cell-when-the-rubric-lacks-one`: if a real class of record does not fit, add the cell mid-screen
and re-run completed strata as code rather than forcing it into `OFF_OTHER`. And a thin cell may be an
unscreened cell (`a-thin-cell-may-be-an-unscreened-cell`) — C.3.e's Arm S went 3 → 16 in one wave.

---

## 10. Required tags on every included empirical effect

| tag | values |
|---|---|
| `direction` | `FORWARD` · `BACKWARD` — §2. The single most important field in the table |
| `exposure_object` | `CHILD_RETURN` · `PARENT_RETURN` · `BOTH` — Wall 2, made a data field so it is auditable |
| `exposure_source` | `SCHOOLING_SUPPLY` · `TRADE` · `TECHNOLOGY` · `OCCUPATIONAL` · `HISTORICAL_INDUSTRIALIZATION` · `LOCAL_DEMAND` · `RETURNS_SERIES` · `TWIN` · `SEX_COMPOSITION` · `SCHOOLING_REFORM` |
| `return_separated_from_position` | `YES` · `NO` · `NOT_APPLICABLE` — Wall 1, likewise |
| `own_income_held` | `YES` · `NO` — Wall 4, likewise |
| `outcome_object` | `FERTILITY` · `INVESTMENT_PER_CHILD` · `CHILD_ATTAINMENT` |
| `outcome_level` | `REALIZED` · `INTENDED` · `DESIRED` |
| `link_measured` | `LINK1_RETURN` · `LINK2_SUBSTITUTION` · `LINK3_FERTILITY` · `FULL_CHAIN` |
| `estimator_class` | with a **loud** fall-through — an unlisted correction must raise, never land silently in `uncorrected` (`estimator-class-list-is-a-gate`) |
| `phenomenon_window` | `FDT` · `SDT` · `OTHER`, plus a transport note where the setting and the claimed phenomenon differ |

`direction` and `outcome_object` are separate fields deliberately: a backward study can have
`INVESTMENT_PER_CHILD` or `CHILD_ATTAINMENT` as its outcome and they are not the same quantity.
`stratify-before-counting-poolable` requires the strata to be derivable from this list, and they are.
Screen-stage `design` values are **hypotheses, not properties**, and every one is re-read at full text
— A.23 carried a paper as an administrative allocation through search, screen and priority retrieval
and it was IPTW.

---

## 11. Identification threats the risk-of-bias pass is looking for

1. **The parent's return moves with the child's** (Wall 2) — the dominant threat, and the reason
   schooling-supply designs (§7 row 3, the largest) are the most contaminated. An education-expansion
   shock raises the mother's wage and the child's expected return at once, and the first is C.2.e's
   parameter with the same predicted sign.
2. **Income moves with the return** (Wall 4) — a rising skill premium raises the earnings of the
   skilled. Any design without a separate income control is estimating a composite.
3. **The reference standard moves with the return** (Wall 1) — SBTC raises both, which is C.2.f's §2
   from the other side, and C.2.f's own studies failed this eight times in nine.
4. **The twin instrument is not exclusion-valid for the forward arm** — twin births are an instrument
   for *family size*, which identifies link 2. Using them to speak about link 3 imports the assumption
   that twinning affects fertility only through family size, which A.12 shows is false.
5. **Reverse causation on link 2** — parents who intend fewer children invest more in each, so
   cross-sectional sibsize–attainment gradients have the arrow ambiguous by construction.
6. **Calibration presented as estimation** (§13 call 4) — a unified-growth model matched to moments
   is not an identified effect, and its "elasticity" is an assumption.
7. **Sign-blind fit** (§5) — a high R² against a returns series with the wrong sign.

---

## 12. Pooling rule (pre-registered)

Stratify **first**, then apply the ≥3 test within each stratum, strata derived from §10
(`stratify-before-counting-poolable`). Never pooled across:

- `direction` — forward and backward are different outcomes, not two levels of one (§2);
- `outcome_object` — a fertility elasticity, a spending response and a test-score effect are three
  parameters;
- `outcome_level` — realized, intended and desired are different quantities; C.3.e found a null and a
  +0.4 inside a single RCT across that boundary (`outcome-level-separates-channels`);
- `exposure_source` — a trade shock and a schooling-supply shock are not the same exposure;
- `estimator_class` — `resolve-disagreements-dont-average`: ask whether disagreeing studies share an
  estimator before pooling. A.12 had four biased against one corrected, and averaging them would have
  reported the bias.

Where a stratum has fewer than three effects the synthesis is narrative and says so.
`identities-need-a-survival-correction` does not apply here — this chapter has no accounting identity.

---

## 13. Open PI calls

1. **Does C.3.d's registered forward claim survive its own literature?** The forward arm is 231
   records on channel 1 and 770 on channel 2, but 16 inside the theory's own frame; and the middle
   link's best identification (twins) largely fails to find the substitution. This is a question about
   the registry entry, not about the search. C.2.f raised the mirror-image call one week ago.
2. **Is the C.2.f/C.3.d wall tenable?** C.2.f's PI call 3 asks this and flagged that it is decidable
   only while C.3.d is unstarted. It is now started, so the call has a deadline. Recommendation:
   answer it with a count of `MIXED_RETURN_POSITION` from **both** chapters' full-text passes rather
   than from either scope's vocabulary table, since the word overlap (9 records) understates the
   estimand overlap by an order of magnitude.
3. **Wall 2 (C.2.e) is new and C.2.e is unstarted.** Confirm that C.3.d owns the return to the
   *child's* human capital and C.2.e the *parent's*, so C.2.e can inherit it. If instead the PI wants
   schooling-supply shocks routed wholesale to C.2.e, §7 row 3 — the largest forward row — leaves this
   chapter and the scope changes materially.
4. **Are unified-growth calibrations evidence?** They are the registry's stated reason the macro role
   is "central", they are 85–123 records, and they are not identified estimates. This scope puts them
   in `THEORY`, context only. That is a defensible call and it is not obviously the PI's.
5. **Coordination with Alexandra on compulsory-schooling reforms** (§7 rows 3 and 9, Wall 7). The same
   reforms identify her chapter's estimand and this one's. `same-policy-two-estimands` says the
   estimand is in the identifying contrast, not the policy — but two RAs should not extract the same
   papers to different tables in parallel.

---

## Provenance

Scripts `344`, `345`, `346` on branch `083-quantity-quality-tradeoff`; the frame probe `304` was
ported to this branch from `078-easterlin-relative-income` on 2026-09-09 and re-run. Logs:
`candidate-frame-probe-2026-09-09.*`, `c3d-term-diagnostics-2026-09-09.*`,
`c3d-outcome-axis-2026-09-09.*`, `c3d-forward-channel-walls-2026-09-09.*`.

Inherited without re-litigation: C.2.c's what-varies rule (2026-07-31), C.2.b's scope ruling 2, and
C.2.f's §2 return-vs-reference-standard split. Nothing in this document reopens a written chapter.
