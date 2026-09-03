# Search scope — rising direct costs of children

**Hypothesis:** C.2.b, slug `child-cost-direct`, HYPOTHESES-v5.md §C.2.b
**Ticket:** TICK-079 · branch `079-child-cost-direct`
**Status:** stage 2, drafted 2026-09-03 (Shravan). Walls, estimand cells, required tags, the pooling
rule and the demographic-significance route are frozen below. Three PI calls open.

**Nothing here is a measured result about the literature.** No production query has been run and no
anchor resolved. The only measured numbers are the OpenAlex record counts in §1 and §9, which come
from `source/build/goldset/304_candidate_frame_probe.py` and count a *retrieval frame*, not an
evidence base.

---

## 1. The claim

The registry entry: *rising direct expenditures required per child — schooling, health, consumption
norms — reduce fertility by raising the price of children.* Phenomena: **FDT and SDT**. Cross-ref:
D.2.d. Seminal: Caldwell 1976, Lino 2017, Folbre 2008, Doepke and Kindermann 2019. The registry's own
note: *separating direct cost from quality-investment cost (C.3.d) is an identification challenge.*

The chapter's parameter is the change in completed fertility caused by an exogenous rise in the
**price** of the goods and services a child requires, holding household income, the price of the
mother's time, and the chosen level of investment per child fixed.

Every clause in that sentence is doing work. "Price" rather than expenditure is §2 and it is the
ruling this chapter turns on. "Holding the chosen level of investment fixed" is the C.3.d wall (§8
Wall 1). "Holding the price of the mother's time fixed" is C.2.e. What remains after the four
neighbouring cost chapters take their components is §3.

Frame size from script 304: **587 records** in the deduplicated union frame across three
vocabularies, the smallest of the 37 unstarted candidates. It is a frame. It says nothing about how
much admissible evidence exists, and §7 exists because the honest prior is that very little does.

---

## 2. The estimand is a price faced, not an expenditure observed

This is the ruling that decides the chapter, and it has to be frozen before a single query runs,
because the vocabulary of the hypothesis and the vocabulary of the accounting literature are the
same words.

Observed spending per child is **quantity chosen times price faced**, and fertility and
quantity-per-child are chosen together. Three consequences:

**The raw correlation is an identity, not an effect.** A household with two children spends more per
child than an otherwise identical household with five, because the same budget is divided fewer ways
and because the parents who chose two were choosing intensity. Under any quantity-quality model the
correlation between expenditure per child and fertility is negative **with no price change
anywhere**. A design that regresses fertility on a cost-per-child figure recovers the household
budget constraint.

**The canonical series are outputs of that identity.** USDA *Expenditures on Children by Families*
(the Lino series) is computed from Consumer Expenditure Survey budgets *conditional on family size
and income*: it estimates what families of a given size do spend, by construction. The same is true
of every equivalence-scale estimate (§9, `COST_SERIES_MEASUREMENT`). These are legitimate measurement
work and they are the natural source for the exposure series in §5 — but as an *exposure* in an
effect regression they are the dependent variable of the model they are being used to test.

**So admissibility is defined on the variation, not on the vocabulary.** An included effect needs a
price of a child-specific input that moved for a reason other than the household's own fertility and
investment choices. §7 enumerates where such variation could come from, before any query, so that a
thin primary cell is a finding about the literature rather than an artefact of not having thought of
the design.

Precedents, and this chapter is the third instance of the same failure shape:
`exposure-estimand-distance-domain` (A.24 had zero studies measuring its registered exposure and
found out at extraction), `read-the-mechanism-not-the-instrument-name` (C.3.e routed four of four
full texts out once the mechanism was read rather than the label), and
`exposure-outcome-same-sequence` (A.23, where the obvious comparison shows an effect under the null).

---

## 3. The cost bundle splits four ways and three of the pieces belong to other chapters

"The direct cost of a child" is not one price. Under the what-varies boundary rule frozen by C.2.c on
2026-07-31, the bundle is already allocated:

| component | chapter | status |
|---|---|---|
| childcare price | C.2.a | unstarted |
| housing price and space | C.2.c | **written**; sign is tenure-conditional |
| the mother's forgone time | C.2.e | unstarted |
| the norm defining what a proper child requires | D.2.d | **drafted** |
| the chosen level of investment per child | C.3.d | unstarted |
| net-of-transfer price | C.2.d | unstarted |
| **the out-of-pocket price of child-specific goods and services** | **C.2.b** | this chapter |

**Ruling: C.2.b is the residual, not the total.** It owns schooling fees and school-related outlays,
child health costs, and child-specific goods — and it does not own the four components above. The
alternative reading, in which C.2.b is the total direct cost with the neighbours as named components,
is rejected for a specific reason: it would make this chapter's estimate a function of five other
chapters' estimates, none of which is finished, and the review has no device for that. B.6 split a
bundle two ways at stage 2 for the same reason.

The cost of the ruling is that the residual may be small. That is the risk §7 is enumerated against,
and it is stated here so that it cannot later be presented as a discovery.

The measured contamination is low, so this is a definitional problem and not a retrieval one: the
boundary probes returned **28** records for the C.2.a childcare vocabulary and **11** for C.2.c's
housing vocabulary inside the fertility-restricted frame.

---

## 4. The hypothesis is about a rise; the identified variation is mostly a fall

Almost every clean policy shock to the price of a child-specific input **lowers** it: school-fee
abolition, free primary education, subsidised uniforms and meals, child health-insurance expansion.
The hypothesis is stated as a rise.

Using a fall to test a claim about a rise assumes symmetry. That assumption may be reasonable and it
is certainly common, but it is an assumption, it is not in the registry, and the review has to see it
rather than absorb it. Every included effect is therefore tagged `exposure_direction` ∈ {`RISE`,
`FALL`}, effects are **stratified on it before the ≥3 poolability test** (§12), and a synthesis that
rests on `FALL` evidence says so in the verdict sentence.

There is a second, compounding problem with the same records. The cleanest fee-abolition designs are
in low- and middle-income countries in the 1990s and 2000s — a PM/FDT-like setting — while the
registry's SDT claim is about rising child costs in rich countries after 1965. Transporting a
schooling-price elasticity from Malawi 1994 to the American SDT is a stronger assumption than the
GRADE indirectness domain usually carries. Each effect gets `phenomenon_window` and a transport note,
and the SDT cell is never populated by an LMIC fee study without the transport being argued in the
chapter text.

---

## 5. Demographic significance — the route is named before searching

Per `three-demsig-routes-before-not-assessed`, the route is chosen now and NOT ASSESSED requires
naming which route failed and why.

PROTOCOL §4.2.1's decomposition route needs a share-of-a-change denominator and an elasticity, and it
will be available only if §7 yields pooled estimates. **The route this chapter commits to is slope
sufficiency**, which needs no decomposition denominator: did the exposure move in the direction and
by enough that the mechanism could account for the observed fertility change? C.6.a settled its SDT
cell that way, on a sign test run before its search.

### The index is specified before it is computed

The failure mode here is obvious and worth naming: a "price of children" index can be made to rise or
fall by choosing components after seeing the answer. The specification is therefore frozen now.

- **Source.** National CPI sub-indices (US BLS; OECD/Eurostat COICOP for the comparison countries),
  deposited raw in `data/raw/` beside `wdi-age-structure/` with a PROVENANCE note, as C.6.a did.
- **Components, named in advance.** (a) education, tuition and school fees; (b) children's and
  infants' clothing and footwear; (c) medical care. Childcare is **excluded** — it is C.2.a's, and
  where a national series bundles it with education that bundling is reported, not silently used.
- **Deflator.** All-items CPI. The claim is about the *relative* price of children; a nominal series
  rising is not the claim and will not be reported as if it were.
- **Weights.** Two pre-specified variants reported side by side and neither chosen after the fact:
  equal weight across components, and household-budget child-expenditure shares.
- **Arms.** Reported with education, without education, and education alone. Education carries the
  ruling-1 ambiguity in its sharpest form — university tuition is very largely a *chosen quality*
  (C.3.d) rather than a required direct cost — so a result that depends entirely on the education
  component is reported as depending on it.
- **Window.** 1965–present for SDT. For FDT (roughly 1870–1965) comparable price series exist for few
  countries; if they do not exist, that is stated as a data absence and not as a null.
- **The sign the hypothesis requires:** the real index **rises** across the window in which fertility
  fell. If it did not, the SDT cell is settled by the sign and the elasticity estimates are
  irrelevant to it — the same logic that settled C.6.a.

Two guards carried in from other chapters. `r2-criterion-is-sign-blind`: any R² reported here
carries a sign condition, because six of eighteen countries cleared PROTOCOL §4.2's 0.15 threshold on
C.6.a with the correlation running *against* the hypothesis. And
`endpoint-test-nets-a-hump-to-nothing`: the window is split as well as taken end to end, because a
full-window endpoint test nets out any hump and C.6.a read 0/18 as uniform failure when the truth was
14/18 early and 0/18 late.

---

## 6. Two phenomena, and the FDT arm collides with a written chapter

v5 registers FDT **and** SDT, and the FDT seminal citation is Caldwell 1976 — whose mechanism is that
mass schooling makes children expensive. That mechanism has two halves and they are different
chapters:

- the **out-of-pocket price** of schooling a child (fees, uniforms, books) — C.2.b, this chapter;
- the **forgone productive value** of a child who is at school rather than working, and the legal
  compulsion that puts them there — C.3.a (mode of production) and C.3.b (child labour restrictions
  and compulsory schooling, **a written chapter**).

**Ruling: the FDT arm stays in scope, restricted to the out-of-pocket half.** It is not dropped,
because `identified-evidence-in-the-unnamed-arm` says to count identified designs per arm before
scoping one out, and the fee-abolition designs of §7 are the best-identified variation this chapter
is likely to see. Where a study cannot separate fees from forgone child labour it is tagged
`MIXED_PRICE_VALUE` and held jointly claimed and unallocated, on C.2.c's `MIXED_PRICE_CREDIT`
precedent rather than a new device.

Caldwell 1976 is now cited by four chapters — C.2.b, C.3.a, C.3.b and D.1.b. That is a registry
observation worth a PI call (§14, Call 2), not a defect.

---

## 7. Where admissible variation could come from — enumerated before searching

Written before any query so that a thin result is a statement about the literature. Each row is a
prediction to be tested, not a finding.

| # | variation | direction | expected volume | wall risk |
|---|---|---|---|---|
| 1 | School-fee abolition / free primary education (Uganda 1997, Malawi 1994, Kenya 2003, Ghana, Tanzania, Ethiopia) | FALL | the largest single source | C.3.b if compulsion moves with it |
| 2 | Fee *introduction* or cost-sharing under structural adjustment, 1980s–90s | RISE | thin, and the only direct test of the claim as stated | endogenous to fiscal crisis |
| 3 | Child health-insurance expansion (US Medicaid/SCHIP, Mexico Seguro Popular, Thailand 30-baht) | FALL | moderate | C.2.d if delivered as a transfer |
| 4 | In-kind school costs — uniforms, textbooks, meals — varied by programme | FALL | thin but clean | — |
| 5 | Compulsory-schooling extensions that raise direct outlay | RISE | moderate | **C.3.b owns this**; admissible only if the fee channel is separated |
| 6 | Private-school tuition or school-choice cost shocks | either | thin | C.3.d (quality chosen) |
| 7 | Child-specific commodity price shocks (infant formula, infant food tariffs) | RISE | very thin | — |
| 8 | Anticipated future cost of a child (university tuition faced by prospective parents) | RISE | thin | C.3.d; distinct from C.3.g, which is the *parent's own* prior debt |
| 9 | Fee or cost discontinuities at a parity threshold (a third child costs a step more) | RISE | thin | C.2.d if implemented through the tax system |
| 10 | Cross-sectional or time-series variation in a constructed child-price index | either | common | almost never exogenous; expected to land in `EXPENDITURE_ASSOCIATION` |

**If rows 1–4 are where the identified evidence turns out to live, this chapter's SDT cell is
populated mainly by LMIC cost *reductions* and its honest verdict will say so.** That is written here,
before the search, so that it is a pre-registered expectation rather than a rationalisation.

`channels-must-fail-differently`: if the primary cell comes back empty, the null is only worth
something if the channels died for unrelated reasons. The second channel is the **policy-evaluation
vocabulary** — "fee abolition", "free primary education", "user fees", "cost sharing" — which is a
different literature's local vocabulary from the economics of fertility, exactly the
`policy-literatures-indexed-in-local-vocabulary` failure that was worth +40% of A.23's frame.

---

## 8. The boundary walls

| # | wall | rule — separated by *what varies* | neighbour status |
|---|---|---|---|
| 1 | **C.3.d quantity-quality** | C.2.b owns an exogenous move in the **price of a required input**; C.3.d owns the household's **chosen investment level** per child. Registry flags this itself. | unstarted — ruling must be written so C.3.d can inherit it |
| 2 | C.2.a childcare | childcare price is C.2.a's, entire. Measured contamination **28**. | unstarted |
| 3 | C.2.c housing | housing price is C.2.c's; its sign is tenure-conditional and not transportable. Measured contamination **11**. | written |
| 4 | C.2.e female time price | opportunity cost of the mother's time is not a direct cost | unstarted |
| 5 | C.2.d tax and transfer | C.2.d owns the **net-of-transfer** price. A study varying a child benefit is C.2.d's. Where a policy moves the gross price *and* a transfer, tag `MIXED_PRICE_TRANSFER` and leave unallocated. | unstarted |
| 6 | C.3.b compulsory schooling | see §6: fees here, compulsion and forgone child labour there | written |
| 7 | D.2.d intensive-parenting norms | D.2.d owns the **norm** that defines what a proper child requires; C.2.b owns the **price** of meeting it | drafted |
| 8 | C.3.g student debt | C.3.g is the prospective parent's *own* prior education debt; C.2.b is the price of the *child* | written |
| 9 | **paediatric cost-of-illness homonym** | "cost of children" is shared with the cost-of-treating-sick-children literature. **Measured, not assumed:** 740 records unrestricted, 206 intersect the illness vocabulary, and **10** survive inside the fertility-restricted frame. The outcome axis separates the two literatures on its own, as it did for C.6.a's happiness literature. **No screen rule is spent on it.** | — |

---

## 9. Estimand cells

| cell | contents | role |
|---|---|---|
| `PRICE_SHOCK_FERTILITY` | exogenous move in the price of a child-specific good or service → realized fertility | **primary** |
| `SCHOOL_COST_FERTILITY` | school fees and school-related outlays → realized fertility | **primary** |
| `CHILD_HEALTH_COST_FERTILITY` | price of children's health care → realized fertility | **primary** |
| `MIXED_PRICE_VALUE` | fees inseparable from forgone child labour (§6) | jointly claimed, unallocated |
| `MIXED_PRICE_TRANSFER` | gross price and transfer move together (Wall 5) | jointly claimed, unallocated |
| `PERCEIVED_COST` | stated cost as a barrier → intentions or desires | **separate outcome level; never pooled with realized** |
| `EXPENDITURE_ASSOCIATION` | expenditure per child vs fertility, no price variation | context; the §2 identity; **never primary, never pooled** |
| `COST_SERIES_MEASUREMENT` | equivalence scales, cost-of-a-child accounting (92 records on the probe) | **exposure measurement**, a source for §5; not an effect |
| `QQ_BOUNDARY` | price of child *quality* varied | Wall 1 packet |
| `THEORY` | models of child price and fertility | context |

`add-a-cell-when-the-rubric-lacks-one`: if a real class of record does not fit, add the cell mid-screen
and re-check completed strata as code, rather than forcing it to `OFF_OTHER`.

---

## 10. Required tags on every included empirical effect

| tag | values |
|---|---|
| `exposure_type` | `PRICE_EXOGENOUS` · `PRICE_POLICY` · `EXPENDITURE_OBSERVED` · `PERCEIVED` |
| `exposure_distance` | `PRICE_MEASURED` · `PRICE_PROXIED` · `EXPENDITURE_ONLY` · `NOT_A_COST` |
| `exposure_direction` | `RISE` · `FALL` |
| `cost_component` | `SCHOOLING` · `HEALTH` · `GOODS` · `TOTAL_BUNDLE` · `OTHER_CHAPTER` |
| `outcome_level` | `REALIZED` · `INTENDED` · `DESIRED` |
| `estimator_class` | with a **loud** fall-through — an unlisted correction must raise, not silently land in `uncorrected` (`estimator-class-list-is-a-gate`) |
| `phenomenon_window` | `PM` · `FDT` · `SDT`, plus a transport note where the setting and the claimed phenomenon differ (§4) |

`design` values from the title/abstract screen are **hypotheses, not properties** — A.23 carried a
paper as an administrative allocation through search, screen and priority retrieval and it was IPTW
(`design-is-not-a-property-of-the-title`). Every `design` is re-read at full text.

---

## 11. Identification threats the risk-of-bias pass is looking for

1. **The budget identity (§2)** — expenditure per child regressed on fertility. The dominant threat;
   `EXPENDITURE_ASSOCIATION` exists to quarantine it.
2. **Reverse causation through anticipation** — parents who intend fewer children plan more expensive
   ones. Bites even some price designs if the price is a menu the household selects from.
3. **Fee changes bundled with quality changes** — abolishing fees typically also raises class sizes;
   the price fell and the quality fell with it, so the elasticity is not a pure price elasticity.
4. **Fiscal endogeneity** — cost-sharing was introduced under structural adjustment, alongside income
   shocks that move fertility directly (row 2 of §7).
5. **Composition** — a child-price index whose movement is driven by one component (§5 arms).
6. **Transport** (§4) — an LMIC schooling elasticity carried to the rich-country SDT.

---

## 12. Pooling rule (pre-registered)

Stratify **first**, then apply the ≥3 test to each stratum, with strata derived from the required-tag
list (`stratify-before-counting-poolable`). Never pooled across:

- `outcome_level` — realized, intended and desired are different quantities and C.3.e found a null
  and a +0.4 inside a single RCT across that boundary (`outcome-level-separates-channels`);
- `exposure_direction` — pooling a rise with a fall assumes symmetry (§4). A stratum that pools them
  states the assumption in the chapter text;
- `cost_component` — a schooling-fee elasticity and a child-health-price elasticity are not the same
  parameter;
- `EXPENDITURE_ASSOCIATION` with any price cell, ever.

Where studies disagree, ask first whether they share an **estimator** before averaging
(`resolve-disagreements-dont-average`); A.12 had four biased estimates against one corrected.

---

## 13. Cold-start plan (a plan, not a result)

1. **Free seeds first.** Port `305_c6a_free_seeds.py`. C.2.c, D.2.d, C.3.b, C.3.e and C.3.c all
   plausibly routed cost-of-children records into their own screen files before this chapter existed
   — `snowball-pools-omit-their-own-seeds` in reverse, at zero retrieval cost.
2. **The exposure series and the §5 sign test, before the search.** C.6.a ran its sign test first and
   it settled the SDT cell.
3. **Anchors.** Port the resolver from `307_c6a_cold_start_anchors.py` — the only copy carrying all
   four TICK-074 fixes plus the three defects found on C.6.a's *Birth and Fortune* anchor. **Not**
   from `275_`. Candidate list carries `control` titles copied verbatim from records the free-seed
   harvest proves exist, so a failure localises to the resolver before anything is read.
4. **Production query calibrated per arm**, scored separately against each arm's own anchors. C.6.a's
   single-axis design plateaued at 15/21 with the misses clustered by arm; §7's policy-evaluation
   vocabulary is a structurally different arm and will not be reached by tightening a fertility axis.
5. **Screen**, with hidden gold controls and a blinded batch (`blinded-screen-audits-the-anchors`).

**Script numbering starts at 317.** Max across every branch on origin is 316
(`script-number-collision`: start above every branch, not above main).

---

## 14. PI calls

**Call 1 — is C.2.b the residual or the total?** §3 rules it the residual, on the grounds that the
alternative makes this chapter's estimate a function of five unfinished chapters. The reading matters
beyond C.2.b: it sets how the review handles any hypothesis whose named quantity is an aggregate of
its neighbours' quantities, and C.2.f and C.3.f have the same shape.

**Call 2 — Caldwell 1976 is now the seminal citation of four chapters** (C.2.b, C.3.a, C.3.b, D.1.b).
That is not a defect, but a shared seminal citation was the evidence that a wall was broken on C.2.c,
and it is worth Anup deciding whether the registry should carry a note. Flagged, not made:
HYPOTHESES-v5.md is under PI review at TICK-001.

**Call 3 — the symmetry assumption in §4.** If the identified evidence is overwhelmingly cost
*reductions* and the registered claim is about a rise, does the review (a) report the elasticity with
the symmetry assumption stated, (b) restrict to `RISE` evidence and report a much thinner cell, or
(c) rate the SDT cell down for indirectness? This chapter proposes (a) with the assumption stated in
the verdict sentence, but it is a protocol-level choice and C.2.d will hit it next.

---

## 15. Next steps, in order

1. Free-seed harvest (script 317).
2. Child-price index and the pre-registered §5 sign test (script 318) — before the search.
3. Cold-start anchors (319).
4. Production query, calibrated per arm (320).
5. Screen universe (321).

---

## 16. Amendments — 2026-09-03, after the free-seed harvest (script 317)

The harvest recovered **130** records from neighbouring chapters' pools at zero retrieval cost. Two
of them change decisions taken above. Both are amendments to this document, not discoveries to be
reported later as if they had been anticipated.

### 16.1 Wall 4 is a vocabulary problem, not only a routing problem

§8 Wall 4 separated C.2.e (the price of the mother's time) from C.2.b on *what varies* and assumed
the screen would enforce it. It will not, because **the two literatures share this chapter's own
name.** In the harvest, **17 of 130** kept records are the time-cost / child-penalty literature: 11
of the 33 returned by `cost of children`, and **5 of the 6** returned by `cost of childbearing`.

"The Career Costs of Children", "Time and the Cost of Children", "The Time Cost of Children as
Parents' Forgone Leisure" and "Estimating the Indirect Cost of Children in terms of Loss of Career
Advancement" are all titled in C.2.b's vocabulary and all measure C.2.e's estimand.

**Amendment:** the exposure axis in script 320 separates the two — it does not defer the separation
to the screen. `cost of childbearing` is not usable as a stand-alone exposure term at 5/6
contamination. Records that match anyway are kept and tagged, because they are Wall 4's own packet
and `decoy-clouds-are-boundary-cases` says a boundary record is the useful kind.

This is `anchored-vocabulary-has-own-homonym`: the term that names the hypothesis is the term that
imports the neighbour. It was measurable in advance and §8 did not measure it — only the
cost-of-illness homonym was scored, and that one turned out to be the harmless one (2 records
dropped, against 17).

### 16.2 The best-identified vein may be identifying the wrong estimand

§7 row 1 named school-fee abolition as the largest expected source of identified variation, and the
harvest agrees on volume: **24** school-fee records, the second-largest term. But of the **8** that
carry a fertility or family-planning outcome, **6 name women's or girls' schooling in the title** —
*Abolishing user fees, fertility choice, and educational attainment*; *Women's schooling, fertility,
and child health outcomes: Uganda's free primary education*; *Free Primary Education, Schooling, and
Fertility: Ethiopia*; and three more.

If those papers identify through the mother's own schooling, they are not measuring the price of a
child. They are measuring an education effect that **lowers** fertility, while the C.2.b mechanism
says a price cut should **raise** it. Pooling them into `SCHOOL_COST_FERTILITY` would put a
wrong-signed education elasticity into this chapter's primary cell and call it a price elasticity.

**This is a title-level signal and nothing more.** `design-is-not-a-property-of-the-title`: A.23
carried a paper as an administrative allocation through search, screen and priority retrieval and it
was IPTW. Every one of these is re-read at full text before routing.

**Amendment — a required check, not a new wall.** Every record entering `SCHOOL_COST_FERTILITY` must
have its identifying channel read and recorded as `channel` ∈ {`PRICE_OF_CHILD`, `MATERNAL_SCHOOLING`,
`BOTH_UNSEPARATED`}. `MATERNAL_SCHOOLING` routes out. `BOTH_UNSEPARATED` is held jointly claimed and
unallocated. A cell populated mostly by `MATERNAL_SCHOOLING` is reported as an **empty primary cell**
in those words (`empty-cell-is-the-result`), not as weak evidence.

### 16.3 Two smaller items

**User-fee removal for facility-based delivery is the price of a birth, not the price of a child.**
Three such records are in the harvest. It is a real out-of-pocket price and it is plausibly in scope,
but it is a different component from anything in §3 and it belongs to the *event* rather than the
*child*. **Ruling: admissible, as its own `cost_component` value `BIRTH_EVENT`**, reported separately
and never pooled with `SCHOOLING` or `HEALTH`. Flagged for Anup alongside PI Call 1.

**`tuition` is the largest single term (40 records) and roughly 13% on topic.** The rest is C.3.g's
higher-education-finance literature — student debt, college affordability, state appropriations. It
is kept, because it holds the only record matching §7 row 8: *The Influence of College Tuition and
Fees on Fertility Rate in Taiwan* (2006), the anticipated future cost of a child. `tuition` does not
become a production-query axis on its own; it is a seed-harvest term only, and the distinction is
recorded because `frame-growth-is-not-frame-gain` — a term that grows the frame without adding gold
is a cost, and this one is on the line.
