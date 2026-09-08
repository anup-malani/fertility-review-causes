# Search scope — inequality and status competition in child investment

**Hypothesis:** C.2.f, slug `rising-inequality-and-status-competition`, HYPOTHESES-v5.md §C.2.f
**Ticket:** TICK-081 · branch `081-rising-inequality-and-status-competition`
**Status:** stage 2, drafted 2026-09-08 (Shravan). Walls, estimand cells, required tags, the pooling
rule and the demographic-significance route are frozen below. Four PI calls open.

**What is measured here and what is not.** Every count below comes from
`source/build/goldset/328_c2f_term_diagnostics.py`, `329_c2f_second_channel.py` and
`330_c2f_wall_probes.py`, with logs beside this file. They are OpenAlex title/abstract record counts:
they size a *retrieval frame* and its overlaps. **No production query has been run, no anchor
resolved, and no record screened.** A count is not an evidence base, and a record can estimate this
chapter's parameter without carrying any of these phrases in its abstract.

---

## 1. The claim

Registry: *rising income inequality raises the required quality investment per child to maintain
relative status, increasing the effective cost per child and lowering fertility.* Phenomenon:
**SDT only**. Cross-ref: D.2.d. Seminal: de la Croix and Doepke 2003, Kearney and Levine 2014,
Doepke Hannusch Kindermann and Tertilt 2022. Registry note: *the status competition norm is Cultural;
the mechanism through which it reduces fertility is cost. Easterlin relative-income cycling is filed
separately under C.6.*

The chapter's parameter is the change in completed fertility caused by an exogenous rise in the
**dispersion of the income distribution faced by prospective parents**, operating through the
investment per child required to hold a given **relative position**, holding own income and the
return to child human capital fixed.

Every clause is load-bearing. "Dispersion" rather than own income is Wall 4 (C.1.a). "Relative
position" rather than the return to skill is **Wall 1 (C.3.d), the wall this chapter turns on**, and
§2. "Contemporaneous distribution" rather than the parental cohort's standard is Wall 2 (C.6.a).

---

## 2. The estimand is a reference standard, not a return — and this is the ruling that decides the chapter

C.2.f and C.3.d predict the same reduced form from different primitives, and in the canonical models
they move together. Skill-biased technical change raises the **return** to child human capital
(C.3.d's variation) and raises **dispersion** (C.2.f's variation) simultaneously, because they are
the same shock. de la Croix–Doepke sits in both literatures for exactly this reason.

Under the what-varies rule frozen by C.2.c on 2026-07-31 and extended by C.2.b's ruling 2:

> **C.3.d owns variation in the RETURN to child quality.** Investment rises because each unit of it
> is worth more.
> **C.2.f owns variation in the REFERENCE STANDARD.** Investment rises because holding a given
> relative position now costs more, with the return to it unchanged.

The distinction is not cosmetic, because the two have **opposite welfare content and a different
testable prediction**. Under a pure return mechanism, everyone investing more makes everyone better
off. Under a pure positional mechanism, everyone investing more leaves everyone in the same place —
a positional externality, the "arms race" reading. The discriminating prediction is that **investment
per child responds to dispersion holding the return fixed**, and that the response is larger where
the allocation is more explicitly rank-based (exam-allocated school places, class-rank admissions).

**A study that varies SBTC exposure and reads off fertility is not this chapter's** unless it
separates the two. Where it cannot, tag `MIXED_RETURN_POSITION` and leave it unallocated rather than
claiming it. C.3.d is **unstarted**, so this ruling has to be written in a form C.3.d can inherit
rather than re-litigate — the same obligation C.2.b's ruling 2 accepted toward the same neighbour.

Precedents for the failure this is guarding against: `read-the-mechanism-not-the-instrument-name`
(C.3.e routed four of four full texts out once the mechanism was read rather than the label) and
`exposure-estimand-distance-domain` (A.24 had zero studies measuring its registered exposure and
discovered it at extraction).

---

## 3. The frame that ranked this chapter is 89% one general-purpose term

Measured 2026-09-08, script `328`. The union frame reproduces the 09-03 probe (716 today, 714 then).

| measurement | n |
|---|---|
| C.2.f union frame, fertility-restricted | **716** |
| `"income inequality"` alone, fertility-restricted | **635 (89%)** |
| the whole exposure axis MINUS `"income inequality"` | **83** |
| `"income inequality"` unrestricted | 49,350 |

The six mechanism-specific terms sum to 83 and the axis-minus-largest is also 83, so they scarcely
overlap: relative status 44, social comparison 24, status competition 13, positional competition 2,
positional good 0, educational arms race 0.

**This retires the reason C.2.f was picked over A.6.** TICK-081's *Why this one now* argued that
C.2.f's "539-of-714 core" was an anchored literature against A.6's 12-of-675 — but the pass-1 query
generating that 539 is `("income inequality" OR "status competition" OR "positional competition" OR
"relative status")`, i.e. the same general term. On the metric intended, C.2.f is **83/716 = 11.6%**
mechanism-specific against A.6's **1.8%**. The pick survives — six times better, plus a real Tier-A
theory canon and a large middle-link literature to snowball, neither of which A.6 has — but it
survives on a different and weaker margin than the one recorded, and the ticket says so.

**Two corrections to the exposure axis follow, both measured.** The 09-03 axis omitted the
distribution statistics entirely: inside the frame, `"Gini"` alone is **288**, wage/income dispersion
36, relative deprivation 35, status anxiety / positional externality / conspicuous consumption 34,
top income share 8. And `"credential inflation"` is worth roughly **205** records against
`"educational arms race"`'s 16. Both go into the production axis. Per
`advance-the-baseline-when-accepting-terms`, each candidate term is scored against the *running*
frame, not a frozen one, or later terms inherit credit for earlier ones' gold.

---

## 4. The mechanism is a conjunction, and the join is where it fails

Inequality → required investment per child → fertility. Each link, measured (`328`, `329`):

| link | measurement | n |
|---|---|---|
| 1 | shadow education / private tutoring × inequality | 580 |
| 1 | enrichment / extracurricular spending × inequality | 343 |
| 1 | `"educational arms race" OR "credential inflation"` | 221 |
| 2 | quantity-quality / child quality, fertility-restricted | 683 |
| **1+2+3** | **exposure AND investment AND fertility** | **2** |
| **1+2+3** | **status/positional AND investment AND fertility** | **2** |

Known-positive controls alive on the same channel (Q-Q 683, intensive parenting 29, shadow education
1,285), so the 2s are measurements rather than a dead query, and the two channels share no phrase
(`channels-must-fail-differently`).

**Both outer links have substantial literatures and the join has essentially nothing.** Worse for the
chapter's independence: link 2 — investment per child crowding out quantity — *is C.3.d's chapter*.
So C.2.f is at risk of being composed entirely of its neighbours' links, with its own contribution
reduced to link 1, which is an education-and-consumption literature that does not measure fertility.

**What would make a study C.2.f's own** is therefore narrow and should be stated before searching: it
varies dispersion (or an explicitly positional feature of the allocation), holds the return fixed or
measures it separately, and estimates a **fertility** response. §7 enumerates where such variation
could come from.

**Expect an empty or near-empty primary cell.** That is a legitimate result and the chapter is
planned as the rigorous establishment of it, not as a pooling exercise: `empty-cell-is-the-result`
says say **UNEVALUATED**, not "weak", because GRADE has no band for an empty cell and VERY LOW reads
as a poorly identified literature rather than an absent one. The same shape as B.7 (link 2 of three
had one record) and A.24 (primary cell measured empty).

---

## 5. Demographic significance — route named before searching, sign pre-registered

Per `three-demsig-routes-before-not-assessed`, name the route now and say which failed before ever
writing NOT ASSESSED. Route: **slope sufficiency**, computable without a decomposition denominator,
as C.6.a's sign test and C.2.b's price index were.

**Pre-registered sign.** The hypothesis requires the dispersion of the income distribution to have
**risen** across the SDT window in the countries whose fertility fell. This is a strong test because
it is very likely to fail cross-nationally: inequality rose sharply in the US and UK after ~1980, was
roughly flat or fell in France, and moved late and modestly in much of continental Europe and Japan —
while fertility fell in all of them. **If dispersion did not rise where fertility fell, the SDT cell
is settled by the sign and no elasticity estimate is relevant to it.**

Rules inherited from the last two chapters, both of which changed an answer:

- **The R² criterion is sign-blind** (`r2-criterion-is-sign-blind`): six of six countries cleared
  PROTOCOL's 0.15 with the correlation running *against* the hypothesis. Report the sign first.
- **Do not net a hump to nothing** (`endpoint-test-nets-a-hump-to-nothing`): report peak, amplitude,
  and net/amplitude across a split window, not endpoints. On C.6.a an endpoint test read 0/18 and a
  split window read 14/18 early and 0/18 late.
- Series to build and deposit in `data/raw/`: WID top shares, LIS Gini, OECD IDD, plus a US Census
  Gini for the long series. **`data/raw` is currently empty** apart from two ad-hoc pulls on unmerged
  branches, so this is a build, not a fetch.

---

## 6. SDT only, and the FDT arm is not quietly in scope

The registry registers **SDT** alone. Do not open an FDT arm: the FDT-era inequality-and-fertility
argument is the differential-fertility literature, which runs the causal arrow the other way (§8 Wall
9) and is C.3.a's and A.19's territory. `identified-evidence-in-the-unnamed-arm` says count identified
designs per arm before scoping one out — that count is a stage-3 deliverable, and if the FDT arm
turns out to hold identified designs the scope is amended in writing rather than silently.

---

## 7. Where admissible variation could come from — enumerated before searching

Written before any query so a thin result is a statement about the literature rather than about our
imagination. Each row is a prediction to test.

| # | variation | direction | expected volume | wall risk |
|---|---|---|---|---|
| 1 | Local-area (commuting zone, county, school district) dispersion vs fertility | either | the largest source | almost never exogenous; lands in `INEQ_ASSOCIATION` |
| 2 | Top-share shocks from tax reform (TRA86, top marginal rate changes) | RISE | thin | C.1.a if own income moves |
| 3 | Trade / China-shock exposure raising local dispersion | RISE | moderate | **C.5.a** — the same shock raises uncertainty and unemployment |
| 4 | Finance deregulation raising top incomes | RISE | thin | C.1.a |
| 5 | Minimum-wage changes compressing the bottom | FALL | thin | C.1.a directly |
| 6 | Rank-based school allocation — exam-allocated places, class-rank admissions (Texas Top Ten Percent) | positional intensity | thin, and the **cleanest test of the positional mechanism** | C.3.d if it also moves the return |
| 7 | Shadow-education / private-tutoring bans and deregulation (Korea 1980 ban and its lifting, China 2021 "double reduction") | required investment | thin and **directly on link 1** | C.2.b if the price rather than the required quantity moves |
| 8 | Survey or lab elicitation of positional preferences against desired family size | either | thin | `PERCEIVED` outcome level, never pooled with realized |
| 9 | Reference-group shifts through media or migration | either | very thin | C.2.h, D.1.b |

**Row 6 and row 7 are the rows to hunt.** They are the only two where the positional mechanism is
separable from the return, and row 7 sits directly on the link the measurements say is missing.
`one-study-can-carry-the-structure`: a single design estimating both investment and fertility off one
policy beats any cross-literature count, and rows 6–7 are where such a design would live.

**Second channel, per `channels-must-fail-differently`.** If the primary cell is empty, the null is
worth something only if the channels died for unrelated reasons. Channel 2 is the **education-policy
local vocabulary** — "shadow education", "private tutoring", "cram school", "double reduction",
"credential inflation" — a different literature's own words, the
`policy-literatures-indexed-in-local-vocabulary` failure that was worth +40% of A.23's frame. Channel
2 is already measured live at 580 and 343 records, so it is a real channel and not a formality.

---

## 8. The boundary walls

All contamination figures measured 2026-09-08 inside the fertility-restricted frame (`328`, `330`).

| # | wall | rule — separated by *what varies* | measured | neighbour |
|---|---|---|---|---|
| 1 | **C.3.d quantity-quality** | **The wall this chapter turns on** (§2): C.3.d owns the **return** to child quality, C.2.f owns the **reference standard**. Inseparable ⇒ `MIXED_RETURN_POSITION`, unallocated. | **8** | unstarted — write it inheritable |
| 2 | C.6.a Easterlin | C.6.a is relative income against the **parental cohort's** standard; C.2.f is position in the **contemporaneous** distribution. Registry already rules; this operationalises it. | **15** | written — do not reopen |
| 3 | D.2.d intensive parenting | D.2.d owns the **norm** defining what a proper child requires; C.2.f owns the **dispersion** that moves the required level. | **3** | drafted |
| 4 | **C.1.a income effect** | C.1.a owns **own income**; C.2.f owns **position** holding own income fixed. The largest wall by volume, and the one most likely to be violated silently, since most inequality shocks move own income too. | **90** | unstarted |
| 5 | C.5.a economic uncertainty | C.5.a owns **individual-level risk**; C.2.f owns **cross-sectional dispersion**. Row 3 of §7 moves both. | **70** | unstarted |
| 6 | C.2.b direct costs | C.2.b owns the **price** of a required input; C.2.f owns the **required quantity** rising with dispersion. | — | drafted |
| 7 | D.3.c despair | Kearney–Levine's headline result is teen childbearing via "economic despair", which is **D.3.c's estimand**, not status competition in investment. Expect `design-is-not-a-property-of-the-title` to bite here. | **21** | drafted |
| 8 | C.2.h digital leisure | reference-group shift through media | **1** — no screen rule spent | unstarted |
| 9 | **direction of causation** | C.2.f needs inequality as the **cause**. Differential fertility *causing* inequality, and cross-sectional income gradients in fertility, are context. | **25** and **26** | — |
| 10 | **gender/health "inequality" homonym** | "inequality" that is gender inequality (D.2.a's estimand) or health inequality is not a distribution statistic. The gender-and-fertility literature is large (2,281) but barely intersects this frame: **30**. Health/educational: **8**. **No screen rule spent** — the exposure axis separates them on its own. | **30 / 8** | — |

---

## 9. Estimand cells

| cell | contents | role |
|---|---|---|
| `DISPERSION_FERTILITY` | exogenous move in income dispersion → realized fertility, return held or measured | **primary** |
| `POSITIONAL_ALLOCATION_FERTILITY` | rank-based allocation intensity (§7 row 6) → realized fertility | **primary** |
| `REQUIRED_INVESTMENT_FERTILITY` | policy moving required investment per child (§7 row 7) → realized fertility | **primary** |
| `INEQ_INVESTMENT` | inequality → investment per child, **no fertility outcome** | link 1; supports the mechanism, never a primary effect |
| `MIXED_RETURN_POSITION` | return and dispersion move together and are not separated (§2) | jointly claimed with C.3.d, unallocated |
| `MIXED_INEQ_INCOME` | dispersion and own income move together (Wall 4) | jointly claimed with C.1.a, unallocated |
| `PERCEIVED_STATUS` | stated status pressure → intentions or desires | **separate outcome level; never pooled with realized** |
| `INEQ_ASSOCIATION` | area or period inequality vs fertility, no identified variation | context; **never primary, never pooled** |
| `WRONG_DIRECTION` | differential fertility → inequality | context only |
| `THEORY` | models of positional competition and fertility | context |

`add-a-cell-when-the-rubric-lacks-one`: if a real class of record does not fit, add the cell
mid-screen and re-run completed strata as code rather than forcing it to `OFF_OTHER`. A thin cell may
be an unscreened cell (`a-thin-cell-may-be-an-unscreened-cell`) — C.3.e's Arm S went 3 → 16 in one
wave.

---

## 10. Required tags on every included empirical effect

| tag | values |
|---|---|
| `exposure_statistic` | `GINI` · `TOP_SHARE` · `RATIO_90_10` · `DISPERSION_OTHER` · `POSITIONAL_INTENSITY` · `PERCEIVED` |
| `exposure_level` | `NATIONAL` · `SUBNATIONAL` · `LOCAL_LABOR_MARKET` · `SCHOOL_DISTRICT` · `INDIVIDUAL_REFERENCE_GROUP` |
| `return_separated` | `YES` · `NO` · `NOT_APPLICABLE` — the §2 ruling, made a data field so Wall 1 is auditable |
| `own_income_held` | `YES` · `NO` — Wall 4, likewise |
| `link_measured` | `LINK1_INVESTMENT` · `LINK2_QUANTITY` · `FULL_CHAIN` |
| `outcome_level` | `REALIZED` · `INTENDED` · `DESIRED` |
| `estimator_class` | with a **loud** fall-through — an unlisted correction must raise, never land silently in `uncorrected` (`estimator-class-list-is-a-gate`) |
| `phenomenon_window` | `SDT`, plus a transport note where the setting and the claimed phenomenon differ |

`exposure_statistic` and `exposure_level` are separate fields deliberately: a national Gini and a
commuting-zone Gini are not the same exposure, and `stratify-before-counting-poolable` requires the
strata to be derivable from this list. `design` values from the title/abstract screen are
**hypotheses, not properties**, and every one is re-read at full text
(`design-is-not-a-property-of-the-title`).

---

## 11. Identification threats the risk-of-bias pass is looking for

1. **Own income moves with dispersion** (Wall 4, 90 records) — the dominant threat. A local-area
   inequality measure is correlated with local income levels, and the income effect is C.1.a's
   parameter with a different sign story.
2. **The return moves with dispersion** (§2, Wall 1) — SBTC raises both. A design that cannot
   separate them is estimating a composite.
3. **Uncertainty moves with dispersion** (Wall 5, 70 records) — trade and technology shocks raise
   local dispersion *and* job insecurity; C.5.a owns the second.
4. **Reverse causation** (Wall 9, 25 records) — differential fertility by income changes measured
   inequality directly, so contemporaneous area-level regressions have the arrow ambiguous by
   construction.
5. **Compositional change in the reference group** — migration and sorting change who a household
   compares itself to without any change in the national statistic.
6. **Sign-blind fit** (§5) — a high R² against an inequality series with the wrong sign.

---

## 12. Pooling rule (pre-registered)

Stratify **first**, then apply the ≥3 test within each stratum, strata derived from §10
(`stratify-before-counting-poolable`). Never pooled across:

- `outcome_level` — realized, intended and desired are different quantities; C.3.e found a null and a
  +0.4 inside a single RCT across that boundary (`outcome-level-separates-channels`);
- `exposure_statistic` — a Gini elasticity and a top-share elasticity are not the same parameter, and
  neither is a positional-intensity design;
- `exposure_level` — a national time-series coefficient and a school-district one answer different
  questions;
- `link_measured` — a link-1 investment response is **never** pooled with a fertility effect;
- `INEQ_ASSOCIATION` with any identified cell, ever.

Where studies disagree, ask whether they share an **estimator** before averaging
(`resolve-disagreements-dont-average`).

---

## 13. Cold-start plan (a plan, not a result)

1. **Free seeds first.** Port `317_c2b_free_seeds.py`. D.2.d, C.6.a, C.2.b, C.3.e, C.3.g and D.3.c
   all plausibly routed inequality-and-investment records into their own screen files before this
   chapter existed — `snowball-pools-omit-their-own-seeds` in reverse, at zero retrieval cost.
2. **The exposure series and the §5 sign test, before the search.** C.6.a ran its sign test first and
   it settled the SDT cell; C.2.b's index inverted its own answer when the deflator was corrected.
3. **Anchors.** Port the resolver from `319_c2b_cold_start_anchors.py`, the newest copy. **Import
   `source/lib/textnorm.py`** — canonical on `main` since TICK-074 merged 2026-09-08 — rather than
   copying a `norm()`. Anchor on the **estimand, not the famous design**
   (`anchor-on-the-estimand-not-the-famous-design`): the celebrated inequality papers may not measure
   fertility at all, and Kearney–Levine's most-cited result is Wall 7's.
4. **Book canon.** de la Croix–Doepke and Doepke et al. are articles, but the positional-competition
   canon (Frank, Hirsch, Schor) is monographs: apply the **first-author** gate
   (`book-canon-first-author`) and the fallback flag, or a monograph resolves to its own review at
   Jaccard 1.00.
5. **Script numbering.** 328–330 are used by the three diagnostics above. Continue at **331**.

---

## 14. PI calls

1. **Does C.2.f survive as its own chapter?** §4 measures both outer links as substantial and the
   join as ~2 records, and link 2 *is* C.3.d. The alternatives are (a) run it and report UNEVALUATED,
   (b) merge it into C.3.d as the positional arm of one chapter, or (c) defer it until C.3.d is
   written so the wall is cut against a live neighbour. **Recommendation: (a)**, because an
   UNEVALUATED verdict on a hypothesis this prominent in public discussion is itself the deliverable,
   and because `one-hypothesis-two-chapters` says split or merge at synthesis, not in the registry.
2. **Is the §2 return/reference-standard rule the right cut**, given that the canonical model
   generates both from one shock? If the PI prefers a different cut, it must be made before stage 3,
   because it determines the screen rubric.
3. **Is the FDT arm genuinely out (§6)?** The registry says SDT only, but the differential-fertility
   literature is large and adjacent.
4. **Is `INEQ_INVESTMENT` (link 1, no fertility outcome) in scope as mechanism evidence?** It is a
   500+ record literature that cannot bear on the demographic-significance verdict. Including it
   risks a chapter that looks well-evidenced and answers a different question.

---

## 15. Next steps, in order

1. Free-seed harvest (script 331).
2. Build the inequality series and run the §5 sign test **before** the production query.
3. Cold-start anchors on the Tier-A canon (332), first-author gate for the monographs.
4. Production query on the revised axis — distribution statistics and `credential inflation` added,
   each new term scored against the running baseline.
5. Screen universe and rubric; the rubric must carry `return_separated` and `own_income_held` as
   screen-visible fields or Walls 1 and 4 cannot be enforced at title/abstract
   (`band-rules-must-read-screen-notes`, and D.3.b's lesson that a wall invisible to the screen
   cannot be enforced there).
