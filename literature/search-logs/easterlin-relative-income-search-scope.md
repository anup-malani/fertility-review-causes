# Search scope — Easterlin relative income and cohort size

**Hypothesis:** C.6.a, slug `easterlin-relative-income`, HYPOTHESES-v5.md §C.6.a
**Ticket:** TICK-078 · branch `078-easterlin-relative-income`
**Status:** stage 2, drafted 2026-09-02 (Shravan). Walls and the demographic-significance route frozen
below; two PI calls open.

**Nothing in this document is a measured result about the literature.** No production query has been
run and no anchor has been resolved. The only measured numbers here are the OpenAlex record counts in
§1 and §8 Wall 6, which come from `source/build/goldset/304_candidate_frame_probe.py` and are counts
of a *frame*, not of an evidence base.

---

## 1. The claim

The registry entry: *fertility rises when a cohort's earnings prospects are favorable relative to the
consumption aspirations formed in their parents' household, generating endogenous fertility cycles
driven by cohort size.* Phenomena: **SDT**. Cross-ref: none listed. Sign: positive — relative income
up, fertility up.

The chapter's parameter is the change in fertility caused by an exogenous change in a cohort's
earnings prospects **measured against the consumption standard of the household that raised it**,
holding absolute income and prices fixed. Two features of that sentence do all the work below: the
benchmark is cohort-specific (§4), and the exposure that is supposed to move it — relative cohort
size — is the outcome of the same process twenty-odd years earlier (§2).

Frame size, from script 304: **487 records** in the deduplicated union frame, the smallest of the
unstarted hypotheses. That is a retrieval frame. It is not a claim about how much evidence exists.

---

## 2. This hypothesis is a difference equation, and that changes what counts as evidence

Relative cohort size at *t* is, definitionally, the number of births at *t−20* to *t−30* scaled by
neighbouring cohorts. **The exposure is the outcome's own history.** Three consequences, and they are
not caveats — they determine what the search must find.

**A raw correlation between cohort size and fertility is partly an identity.** Large cohorts entering
the labour market are, by construction, the children of a high-fertility past. Any design that
regresses fertility on contemporaneous cohort size without breaking that link is measuring the
feedback and the behavioural response together. This is the A.12 problem (an SDT arm that is partly a
feedback of postponement) and the A.23 problem (exposure and outcome in the same sequence, where the
obvious comparison shows an effect under the null) arriving together. The discipline both chapters
converged on applies here: **define admissibility and enumerate the designs before querying** (§7).

**The cycling claim and the reduced-form claim are different claims with different tests.** "Relative
income raises fertility" is a reduced-form link. "Cohort size generates endogenous fertility cycles"
is a statement about a dynamic system — it requires the feedback to be strong enough, and lagged
enough, to produce oscillation rather than convergence. A literature can support the first and refute
the second. They are separate estimand cells (§9: `RELATIVE_INCOME_FERTILITY` vs `CYCLE_TEST`) and
they are **never pooled**.

**Admissible variation must break the feedback.** Cohort size has to have been moved by something
other than the previous generation's fertility choices. §7 enumerates the candidates before any query
is run, so that a thin result there is a finding about the literature rather than an artefact of not
having thought of a design.

---

## 3. Three links, and the large literature sits on the first one

| link | statement | where the literature lives |
|---|---|---|
| **1** | Relative cohort size → the cohort's own labour-market position (relative wages, unemployment, entry earnings) | Large, and largely in labour economics — cohort-crowding studies. **Usually no fertility outcome at all.** |
| **2** | Labour-market position, relative to the parental-household standard → fertility | The hypothesis proper |
| **3** | Fertility → cohort size, 20–30 years later | The feedback that closes the cycle; mechanical, but its lag and amplitude are estimable |

**The rule, inherited from B.7:** count records per link before rating anything. B.7's three-link
chain had exactly one record on its middle link, and that fact — not the chapter's overall record
count — was the finding. A chapter whose evidence sits on link 1 has evidence about labour markets,
not about fertility. Link-1 records are tagged `LINK1_LABOUR`, held as context, and are **never
primary and never pooled** (§9, §12).

---

## 4. The benchmark is the hypothesis, and it is probably unmeasured

Easterlin's mechanism is not "young people with better jobs have more children." It is that a cohort
judges its prospects against **the living standard of the household it grew up in**. Strip the
benchmark out and what remains is C.1.a (the income effect), which is a different chapter.

Almost every empirical test is expected to replace the benchmark with a proxy — usually relative
cohort size itself, or a young/old wage ratio. That may be perfectly reasonable, but it is a
substitution and the review has to see it. Every included effect is therefore tagged with an
`exposure_distance`, the A.24 device:

| value | what the study actually measured |
|---|---|
| `RELATIVE_MEASURED` | The parental-household living standard, or another explicit cohort-specific benchmark, measured and used |
| `RELATIVE_PROXIED` | A young/old or own-generation/parental-generation wage or income ratio |
| `COHORT_SIZE_ONLY` | Relative cohort size, or birth-cohort size, as the sole exposure |
| `ABSOLUTE_INCOME` | Own income or employment with no benchmark — routes out to C.1.a or C.5.a |

Two precedents make this worth pre-registering rather than discovering. D.3.c's mechanism was
unmeasured throughout its own treatment literature. A.24 had **zero** studies measuring its
registered exposure, and finding that out late cost the chapter its primary cell. If
`RELATIVE_MEASURED` comes back empty here, that is a reportable finding about the literature and it
is stated in those words — not smuggled in as a downgrade for indirectness.

---

## 5. Demographic significance, pre-specified — and why this chapter does not get NOT ASSESSED for free

This is the ruling the ticket opened on, and it resolves more cleanly than expected.

The worry was that PROTOCOL §4.2.1 fixes the demsig denominator as a **change** — the fall in
completed fertility over the phenomenon's window — and that a mechanism predicting an *oscillation*
has no numerator to put over it. That is true of **one** of the three routes. §4.2 offers three, and
they are independent:

- **Route A — decomposition share. Not the route here.** A share of a monotone decline attributable
  to a mechanism whose own prediction is a cycle is not a well-posed quantity. Compute it only if an
  included study supplies one, and label it as that study's.
- **Route B — slope sufficiency. This is the primary route.** §4.2 asks: given the literature's best
  d(fertility)/d(X) and the **observed range of X over the target period**, can the effect plausibly
  produce the observed range of TFR? Both inputs are obtainable. Relative cohort size over
  1965–present is computable from published cohort-size series (HFD, WPP) — see the note below on
  where those series will have to come from.
- **Route C — R² benchmarks. Available.** Within-country time-series R² of TFR on relative cohort
  size, alone and conditional on standard controls; cross-country within-period R².

**The sign test, written down before the search so it cannot be a post-hoc reading.** Slope
sufficiency has a prior question attached to it, which C.3.e's chapter turned on: *did the exposure
move in the direction the hypothesis needs?* For the SDT window, the arithmetic is stated here in
advance:

> The baby-boom cohorts were followed by smaller ones. Cohorts entering the labour market from the
> mid-1970s onward are, on the Easterlin measure, *small* relative to their predecessors. The
> hypothesis therefore predicts their relative income to be **favourable** and their fertility to be
> **high**. Observed SDT fertility fell, and kept falling.

If that holds when computed on the actual cohort-size series for the countries carrying the SDT, then
**the SDT cell is settled by the sign, and the missing decomposition share is irrelevant to it** —
`slope-sufficiency-beats-a-missing-share`, the C.3.e finding, applied to a chapter where the same
structure is visible before the search rather than after it.

**Computed 2026-09-02, before any search — `easterlin-relative-income-sign-test.md`.** The test was
run on 18 SDT countries from World Bank age structure. It splits, and the split is the registry's own
claim rather than a window chosen after the fact: **1965–80, 14 of 18 countries consistent** with the
required sign — this is the mechanism's famous success case, and the within-window correlations are
very strong (US r = −0.98, Belgium −0.99, Canada −0.98). **1980–present, 0 of 18.** Across the full
window, 0 of 18, and relative cohort size *returns to within a fraction of its own amplitude of where
it started* while TFR falls by roughly a birth and stays down. A driver that ends where it began has
nothing left over to explain a permanent level shift. That is the cycles-cannot-explain-a-trend point,
measured rather than asserted, and it is the chapter's spine.

What would overturn it, specified now: (i) relative cohort size does not in fact fall over the window
in the countries carrying the SDT — this is an arithmetic question and is computed at stage 10 from
HFD/WPP regardless of what the literature says; (ii) the effect is institutionally moderated (the
`INSTITUTIONAL_MODERATION` cell) in a way that flips its sign in the relevant period; (iii) the
relevant exposure is not cohort size but a cohort-relative *wage*, which need not have moved with
cohort size after 1975.

### The exposure series does not exist in this repository yet

`CLAUDE.md` describes `data/raw/` as holding the macro panels — HFD, WPP, Maddison, Gapminder, WDI.
**It does not.** On `main` and on every branch, `data/raw/` contains `.gitkeep` and nothing else; the
only macro data anywhere in the repository is two small ad-hoc World Bank TFR pulls that B.7 and B.6
each fetched for their own demsig cell and left on their own unmerged branches
(`wdi_tfr_usa_oecd_dnk_nor.json`, `worldbank-usa-tfr.json`). There is no shared panel, and every
chapter's demographic-significance denominator so far has been taken from what individual studies
reported.

That is survivable for a chapter whose numerator comes out of the literature. It is **not** survivable
for this one, because §5's decisive computation — which way relative cohort size moved over the SDT
window — is an exposure series, not an estimate, and no study has to supply it.

So this chapter builds it: a numbered script under `source/build/` that pulls births by year for the
SDT countries, derives relative cohort size at labour-market entry, and **deposits the series in
`data/raw/` with its provenance**, so that A.9, C.2.d and any later cohort-structure chapter inherit
it instead of re-fetching. That is the single-command-reproducibility standard the project is built
on, applied to the first chapter whose verdict actually depends on a macro series.

**The chapter does not record NOT ASSESSED merely because the mechanism is cyclical.** `empty-cell-is-
the-result` is for genuinely empty cells. Two of the three routes are computable here, and a cell
recorded as NOT ASSESSED when a computation was available would be a failure of the chapter, not a
property of the hypothesis. Compare A.18, where NOT ASSESSED was correct because no *S* existed at
all: the lesson there was stated as `variance-component-has-no-demsig-numerator`, and its own
correction note says to check the phenomenon before saying "nowhere." Checked. It is not nowhere.

---

## 6. Ruling 2 — the phenomenon assignment, and a rule that breaks on this hypothesis

v5 registers C.6.a as **SDT only**. But its founding evidence is the US baby boom and bust, roughly
1946–1975, and PROTOCOL §2 dates the SDT from ~1965. The hypothesis's best case sits mostly *before*
its registered phenomenon.

**Ruling (RA authority, flagged for PI confirmation):** the chapter evaluates the **SDT cell as
registered**, and carries the boom/bust as the mechanism's own best case, classified by PROTOCOL §2's
replacement-status rule rather than by calendar period — first and last in-window TFR both above 2.1
is FDT-like, a crossing is FDT|SDT. Applied to US boom-era study windows, which sit above 2.1
throughout, that rule returns **FDT-like**.

That result is uncomfortable and the discomfort is the point: **PROTOCOL's replacement rule assigns a
fertility *rise* to a phenomenon defined as a *decline*.** The rule was written for monotone
transitions and this is the first hypothesis in the review whose central evidence is an increase.
This is PI Call 1 (§14) and it is protocol-level, not chapter-level — the answer changes how any
future pronatalist or boom-related hypothesis (C.2.d, D.1.d) is classified, not just this one.

**PM is out of scope by mechanism**, provisionally: the hypothesis requires a labour market with
cohort-varying entry wages and a measurable parental consumption standard. If the search returns
historical cohort-size work that meets §4's bar, the cell reopens; the search is not restricted to
prevent it.

---

## 7. Where admissible variation could come from — enumerated before searching

Per §2, an admissible design needs cohort size (or cohort-relative earnings) moved by something other
than the prior generation's fertility choices.

| # | Source of variation | Breaks the feedback? | Note |
|---|---|---|---|
| 1 | **Policy-created cohort discontinuities** — Romania's Decree 770 (1966) produced a step change in cohort size in a single year; China's one-child-policy cohorts reach the labour market as an engineered deficit | **Yes, cleanly** | The first thing to hunt. A single-year step is the sharpest available instrument for cohort size. Boundary: the Decree 770 cohort is already used in the review for A.4 (abortion access) — the *exposure* there is abortion legality, here it is the size of the cohort that resulted. Different treatments, same event; tag and route carefully |
| 2 | **War-driven birth deficits and military mortality** — WWI and WWII cohorts | Partly | Confounded with the marriage market (Wall 3) and with the war itself |
| 3 | **Famine cohorts** — Dutch Hunger Winter, Great Leap Forward, the Ukrainian famine | Yes for size | Confounded with in-utero health, which is a biological exposure (B-section); admissible only where the design separates cohort *size* from cohort *health* |
| 4 | **Epidemic mortality** — 1918 influenza and similar cohort-thinning shocks | Yes for size | Same health confound as 3 |
| 5 | **Immigration waves** that change the size of a labour-market entry cohort without changing anyone's birth cohort | **Yes, cleanly** | Underused, and the mechanism is exactly Easterlin's — crowding at entry. Worth a dedicated query axis |
| 6 | **Within-country cross-region variation** in cohort size at a point in time | Partly | Regional cohort size still reflects regional fertility history; needs a migration-driven or policy-driven component |
| 7 | **The aggregate time series** — Easterlin's own test | **No** | Context and theory stream only; never primary, whatever its provenance |

Rows 1 and 5 are where a boundary-spanning design would live — one study that moves cohort size
exogenously *and* measures fertility. `one-study-can-carry-the-structure`: a single such design beats
any cross-literature count, and the search goes looking for it deliberately rather than hoping it
turns up.

---

## 8. The boundary walls

v5 lists no cross-references for C.6.a. That is a gap in the registry, not an absence of neighbours —
five of the six walls below are real, and PI Call 2 (§14) proposes the registry edit.

**Wall 1 — C.6.a vs C.1.a (`income-effect-normal-good`).** Discriminator: is the exposure benchmarked
to a cohort-specific standard? Absolute income or employment, however well identified, is C.1.a's.
`ABSOLUTE_INCOME` on the §4 scale routes out.

**Wall 2 — C.6.a vs C.5.a (`economic-uncertainty-and-unemployment`).** Both are about young people's
labour-market prospects. Discriminator — **what varies**, the rule frozen by C.2.c on 2026-07-31: a
shock common to all cohorts alive at the time (a recession, an aggregate unemployment rate) is
C.5.a's; variation that is *cohort-specific by construction* — cohort size, cohort entry conditions,
cohort-relative wages — is C.6.a's.

**Wall 3 — C.6.a vs C.7.a (`marriage-market-economics`) and A.10 (`sex-ratio-marriage-market`).**
Cohort growth moves the marriage market, and the marriage squeeze is part of Easterlin's own account.
Under the what-varies rule: **C.6.a owns variation in relative cohort size and cohort-relative
earnings; C.7.a owns variation in marriage-market composition; A.10 owns variation in the sex ratio.**
A design whose channel is a marriage squeeze *created by cohort growth* is jointly claimed by C.6.a
and C.7.a and cannot be allocated — tag `MIXED_COHORT_MARRIAGE`, report it unallocated, and flag it to
C.7.a, exactly as C.2.c created `MIXED_PRICE_CREDIT` and reported it into C.3.e. C.7.a is a finished
chapter and A.10 has a drafted scope; both are read before the wall packet is adjudicated.

**Wall 4 — C.6.a vs A.9 (`population-age-structure-momentum`).** A.9 owns the **mechanical**
composition effect of age structure on the crude birth rate. C.6.a owns the **behavioural** response
to cohort size. Discriminator: an age-standardised outcome (period or cohort TFR, completed fertility,
parity progression) can carry a behavioural claim; a crude birth rate cannot separate the two and is
`UNDECOMPOSED` → route to A.9. This is A.18's Wall 1 in a different domain, and it will move records.

**Wall 5 — C.6.a vs C.2.e (`female-wage-opportunity-cost`): the named rival, which is kept, not
walled out.** Butz and Ward's female-wage model explains the same postwar US series that Easterlin's
does. A study that runs the two against each other is admissible to both chapters and is **the most
informative kind of record this search can find** — a horse race between two mechanisms on one series
identifies more than either tested alone. Tag `RIVAL_TEST`, keep, and cross-file to C.2.e.

**Wall 6 — the happiness homonym, measured and dismissed.** "Easterlin" and "relative income" both
anchor a large subjective-well-being literature: 437 records for `"Easterlin paradox"` unrestricted
and 566 for relative income ∩ well-being. Intersected with the fertility outcome axis, `"Easterlin
paradox"` returns **2**. The outcome axis separates the literatures by itself. **No screen rule is
spent on this wall.** Recording it because the usual finding runs the other way —
`homonym-shares-outcome-vocabulary` exists because a homonym cloud shared A.17's outcome word — and a
measured non-threat is as much a result as a measured threat.

---

## 9. Estimand cells

| cell | definition | outcome | role |
|---|---|---|---|
| `RELATIVE_INCOME_FERTILITY` | Cohort-relative earnings or prospects → fertility | Fertility | **Primary** |
| `COHORT_SIZE_FERTILITY` | Relative cohort size → fertility, behavioural (age-standardised outcome) | Fertility | **Primary** |
| `BENCHMARK_MEASURED` | Either of the above where the parental-household standard is actually measured (§4 `RELATIVE_MEASURED`) | Fertility | **The value-added cell** |
| `CYCLE_TEST` | Tests of endogenous oscillation itself — difference-equation, VAR, spectral, or simulation tests of self-generating cycles | Fertility | Primary for the cycling claim; never pooled with the reduced-form cells |
| `RIVAL_TEST` | Easterlin against a named alternative (Butz–Ward and others) on the same data | Fertility | Primary; cross-file to the rival's chapter |
| `INSTITUTIONAL_MODERATION` | The effect conditioned on labour-market institutions or welfare-state structure | Fertility | Moderation arm — the cell that could flip the §5 sign test |
| `LINK1_LABOUR` | Cohort size → wages, unemployment, entry earnings | **No fertility outcome** | Context only; never primary, never pooled |
| `MIXED_COHORT_MARRIAGE` | Channel is a marriage squeeze created by cohort growth | Fertility or nuptiality | Unallocated (Wall 3); reported, not pooled |
| `OFF_ABSOLUTE_C1a` | Absolute income or employment, no benchmark | Fertility | Route to C.1.a |
| `OFF_UNCERTAINTY_C5a` | Aggregate labour-market shock common across cohorts | Fertility | Route to C.5.a |
| `OFF_COMPOSITION_A9` | Crude-rate result with no age standardisation | Crude birth rate | Route to A.9 (Wall 4) |
| `OFF_SEXRATIO_A10` / `OFF_MARRIAGE_C7a` | Sex ratio, or marriage-market composition not driven by cohort size | Fertility or nuptiality | Route out |
| `THEORY` | Formal models of self-generating fertility cycles; Easterlin's own expositions | No estimate | Theory stream |
| `INSUFFICIENT_INFO` | Not routable on the visible record | — | Pairs only with `UNCERTAIN` |

---

## 10. Required tags on every included empirical effect

`country`, `period`, `phenomenon` (assigned by PROTOCOL §2's replacement rule, never by calendar
period alone), `exposure_measure`, `exposure_distance` (§4), `benchmark_measured` (bool),
`outcome_level` (**realized / stated** — C.3.e found a realized-fertility null sitting beside a
stated-desire positive inside a single RCT; these are never pooled), `outcome_measure` (period TFR /
cohort TFR / completed fertility / crude birth rate / parity progression / timing),
`design`, `estimator_class`, `identified` (bool), `sign`, `cycle_tested` (bool), `rival_model_tested`.

Two of these carry warnings from earlier chapters. `design` is a **hypothesis about the study, not a
property of its title** — A.23 carried a paper through search, screen and priority retrieval as an
administrative allocation when it was IPTW. And `estimator_class` is a **gate**: an unlisted
correction that falls through to `uncorrected` pools with what it should be separated from, so the
fall-through is loud and logged rather than silent.

---

## 11. Identification threats the risk-of-bias pass is looking for

1. **The feedback (§2).** Exposure is lagged outcome. The pass asks of every study: what breaks it?
2. **Age–period–cohort collinearity.** Structural, not incidental, for a hypothesis whose exposure
   *is* a cohort index. Any study identifying all three effects has imposed a restriction; the
   restriction is recorded and is a risk-of-bias domain of its own.
3. **Common trend.** Cohort size and fertility both trend over the long run; a level relationship in
   levels is nearly uninformative.
4. **Effective sample size in the time series.** Forty annual observations fitting a cyclical model
   provide far fewer independent observations than n suggests. Expect overfitting and record whether
   inference accounts for serial correlation.
5. **Vintage effects, and how to tell them from publication selection.** The registry notes "weaker
   post-1980 empirical support." Two explanations — a genuinely time-varying effect, or selection in
   what got published — and they are distinguishable. **Pre-registered:** plot every extracted
   estimate against its publication year *and* against its data window. A fading effect across data
   windows is the first; a fading effect across publication years at fixed data window is the second.

---

## 12. Pooling rule (pre-registered)

Stratify **first**, on (link × `exposure_distance` × `outcome_level` × phenomenon), then apply the ≥3
test within stratum. Never before — `stratify-before-counting-poolable`. Binding consequences:

- `LINK1_LABOUR` never pools with anything; it has no fertility outcome.
- `COHORT_SIZE_ONLY` never pools with `RELATIVE_MEASURED`: they are different exposures.
- `CYCLE_TEST` never pools with the reduced-form cells: different estimands (§2).
- Realized and stated outcomes never pool.
- Where studies disagree, ask first whether they share an **estimator**, before averaging anything —
  A.12 had four biased estimates against one corrected, and the average of those five is not an
  estimate of anything.

---

## 13. Cold-start anchors — the plan, not a result

**Free seeds first.** Neighbouring chapters routed Easterlin records into their own screen files
before this chapter existed: 15 mentions in `credit-constraints-screen-universe.json`, 14 in B.1's
tier-B frame, 6 in C.2.c's snowball pool, 6 in C.3.c's OA enrichment, more on unmerged branches. These
are provenance-labelled hits from adjacent literatures and are mined **before** the cold-start round —
`snowball-pools-omit-their-own-seeds` in reverse.

**Registry seminal:** Easterlin 1961, Easterlin 1976, Macunovich 1998.

**Named candidates to resolve.** These are *candidates for the anchor resolver*, recorded so the
resolution round has targets. **None is resolved, and none may be cited anywhere in the chapter until
it has been:** Easterlin's *Birth and Fortune*; formal self-generating-cycle models (Lee; Samuelson)
for the theory stream; cohort-crowding wage studies (Welch; Korenman and Neumark) as link-1 context;
review articles (Pampel and Peters; Macunovich); Butz and Ward as the `RIVAL_TEST` anchor; the
published critiques of the Easterlin effect; cross-national tests. Author-year pairs written from
memory are **hypotheses about the literature**, and `never-hand-type-a-record-id` applies with equal
force to a hand-typed citation.

**Resolver hazards that apply to this chapter's anchor set**, all previously diagnosed and each to be
verified as fixed in the copy used here rather than assumed: `title.search` is not a root parameter
(the title channel was dead in every resolver until C.3.e); apostrophes break both halves of
resolution; a book canon needs **first**-author agreement, because a review can list the reviewed
author as a co-author; the QJE DOI migration splits citations across two DOIs; and NBER/journal twins
carry the citations while the version of record carries none — seed the snowball with **both**.

**`no-review-exists-is-a-finding` cuts the other way here.** Two review articles are *believed* to
exist. If channel 1 comes back dry on them, that is a signal to try a second vocabulary before
concluding anything — a dry channel removes the external-authority anchor source, and believing a
zero is how a chapter loses its calibration set.

---

## 14. Rulings

**Ruling 1 — what demographic significance means for a cyclical mechanism. RESOLVED (RA authority),
§5.** Slope sufficiency and R², not a decomposition share; the sign test is pre-registered above, and
computed from HFD/WPP at stage 10 independently of what the literature reports.

**Ruling 2 — phenomenon assignment for the baby boom. RESOLVED provisionally (RA authority), §6.**
SDT cell as registered; boom/bust classified by the replacement rule, which returns FDT-like.

**Ruling 3 — the cohort-size marriage squeeze. RESOLVED, Wall 3.** Jointly claimed, unallocated,
tagged `MIXED_COHORT_MARRIAGE`, reported and flagged to C.7.a. Follows C.2.c's `MIXED_PRICE_CREDIT`
precedent rather than inventing a new device.

### PI Call 1 — protocol-level, and it outlives this chapter

PROTOCOL §2's replacement-status rule classifies a study window by whether in-window TFR sits above or
below 2.1. Applied to the US baby boom it returns **FDT-like** — assigning a fertility *rise* to a
phenomenon defined as a *decline*. The rule was written for monotone transitions. C.6.a is the first
hypothesis whose central evidence is an increase, and it will not be the last (C.2.d pronatal
transfers, D.1.d pronatalist ideology). **Question for Anup:** should the review carry a fourth
classification for fertility *recoveries* and *booms*, or should such windows be reported inside the
adjacent phenomenon with an explicit direction flag? The chapter proceeds on the second reading and
will re-cut cheaply if the answer differs.

### PI Call 2 — a proposed registry edit, flagged and not made

v5 gives C.6.a `cross-ref: --`. On the walls in §8 the correct entry is **C.1.a, C.5.a, C.7.a, A.9,
and C.2.e**, with C.2.e marked as the named rival model rather than a boundary. Flagged rather than
made, because `HYPOTHESES-v5.md` is under PI review at TICK-001 — the same course C.2.c took with the
Lovenheim–Mumford double-listing, and which C.3.e then had to resolve. Recording it here so it is not
flagged a third time and acted on a fourth.

### PI Call 3 — the R² criterion is sign-blind, and this chapter demonstrates it

PROTOCOL §4.2's third route to demographic significance is "conditional R² ≥ 0.15". **R² does not
know the sign.** On the sign-test run, **6 of 18 countries clear the 0.15 threshold on TFR against
relative cohort size, and all 6 do so with the correlation running opposite to what the hypothesis
predicts** (Japan R² = 0.71 at r = +0.84; Switzerland 0.46 at +0.68; Korea 0.44 at +0.66; also
Sweden, Canada, Australia). Read literally, the criterion would certify C.6.a as demographically
significant on the strength of evidence against it.

This chapter attaches a sign condition and proceeds — an R² only counts toward demographic
significance where the relationship runs in the direction the hypothesis predicts. **Question for
Anup:** should §4.2 carry that condition generally? It affects every hypothesis with a
directional prediction, which is all of them, and it is invisible in chapters whose fitted sign
happens to be right.

---

## 15. Next steps, in order

1. Mine the free seeds in the neighbouring chapters' screen files (§13) — before the cold-start round,
   not after.
2. Cold-start anchor resolution, with the §13 hazard list verified as fixed in this chapter's copy of
   the resolver, not assumed.
3. Calibrate the production query against the resolved anchors, **per link and per arm** — recall is
   scored separately for link 1 and link 2, because a query tuned on the large link-1 literature will
   look excellent and find nothing about fertility (`sub-literature-renames-the-outcome`).
4. Run the §7 enumeration as its own query axis. Rows 1 and 5 (policy cohort discontinuities,
   immigration waves) get dedicated queries; a null there is only worth reporting if the channels
   failed for unrelated reasons (`channels-must-fail-differently`).
5. Build the cohort-size series and compute the §5 sign test **early** — it does not depend on the
   literature at all, and if it comes out as §5 anticipates, it reorders everything downstream. This
   is also the step that repairs the empty `data/raw/` for every chapter after this one.
