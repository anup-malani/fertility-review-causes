# TICK-081: C.2.f Inequality and Status Competition in Child Investment
**Status:** in-progress
**Assigned:** Shravan
**Hypothesis:** `rising-inequality-and-status-competition` — HYPOTHESES-v5.md §C.2.f
**Parallel-safe:** yes
**Blocks:** none
**Blocked by:** none
**Touches:** literature/search-logs/rising-inequality-and-status-competition-*, extraction/rising-inequality-and-status-competition-*, output/chapters/rising-inequality-and-status-competition.md, source/build/goldset/32[89]*, source/build/goldset/33*

## Acceptance criteria
- [x] 2. Search strategy and scope drafted
- [~] 3. Literature search and AI screening, both phases (§5.1) — targeted arms screened exhaustively; `dispersion` remainder outstanding
- [ ] 4. RA title/abstract review
- [~] 5. Full-text retrieval — **15/19 primary**; both gating cells COMPLETE; 4 outstanding
- [ ] 6. Full-text screen, RA spot-checks 5–10%
- [x] 7. Extraction — all 15 retrieved records extracted (14 rows; one version pair); RA verification outstanding
- [x] 8. Risk-of-bias assessment per study — 9 assessed
- [x] 9. Narrative synthesis — the ≥3 test fails on every stratum
- [x] 10. Demographic significance — three routes computed
- [ ] 11. GRADE rating, 3 independent raters
- [ ] 12. Chapter draft on the §6 template
- [ ] 13. RA lay-readability check
- [ ] 14. PI review and sign-off

## Why this one now

**Not the smallest frame — the second smallest, chosen on the tiebreak.** On the 2026-09-03 probe
(`literature/search-logs/candidate-frame-probe-2026-09-03.md`, still only on the 078 branch) the
union frames of the four remaining finalists are A.6 **675**, C.2.f **714**, A.3 **726**, C.3.d
**762**. C.2.b, which took 587, is drafted. The spread across those four is 13%, and TICK-079 set the
precedent that 15% is inside vocabulary noise, so **size does not decide this** and the tiebreak
governs.

**A.6 loses the tiebreak on inherited boundary debt, and the argument is TICK-079's, not a new one.**
A.6's stigma-specific axis returns **12** records against a 675 union, so its frame is almost
entirely the loose "stigma OR taboo" vocabulary; and A.6 is by construction the residual left after
A.2, A.4 and A.5, all three unstarted. A.3 has the same shape — core 26 of 726 — and shares A.6's
seminal citations, so those two are entangled with each other *and* with three unscoped literatures.
Nothing has started A.2, A.4 or A.5 since 09-03, so the diagnosis stands.

**C.2.f inverts that on both counts.** Its core is **539 of 714**, an anchored literature rather than
a vocabulary artefact, and every wall it needs cuts against something already written: D.2.d (drafted
2026-08-15, the norm driving the competition, and the registry's own cross-ref), C.6.a (drafted
2026-09-02, and the registry explicitly files Easterlin relative-income cycling away from C.2.f into
C.6), and C.2.b (drafted 2026-09-03). Its one unstarted neighbour is C.3.d, and C.2.b's scope ruling
2 was deliberately written in a form C.3.d can inherit, which C.2.f can lean on rather than
re-litigate.

**The homonym is NOT measured, and that is the first stage-2 task.** The 09-03 probe ran a homonym
check for C.2.b only. "Inequality" is a large literature that is mostly not about fertility, and
C.2.f's own social-comparison sub-literature is just **24** records against a 690 core — which is the
signature of a frame carried by a general-purpose axis. Per `anchored-vocabulary-has-own-homonym`,
score each anchor term alone before trusting the block; per `calibrate-the-outcome-axis-too`, the
outcome axis needs the same treatment. Do not write a frame number into this ticket until that runs.

## Open rulings to freeze at stage 2

1. **C.2.f vs C.3.d, and this is the wall that defines the chapter.** Both are about investment per
   child. Under the what-varies rule frozen by C.2.c on 2026-07-31 and extended by C.2.b's ruling 2:
   C.3.d owns variation in the *return* to child quality (rising returns to human capital raise the
   shadow price of quantity); C.2.f owns variation in the *reference standard* — how much investment
   is required to hold a given relative position, which moves with the income distribution rather
   than with the return. Two chapters can share a seminal citation (de la Croix–Doepke sits in both
   literatures) without sharing an estimand.
2. **C.2.f vs C.6.a, which the registry already rules on but does not operationalize.** The note says
   Easterlin relative-income cycling is filed under C.6. Easterlin is relative income against the
   *parental* cohort's standard; C.2.f is relative position against the *contemporaneous*
   distribution. Freeze the discriminating question — which comparison group the exposure varies —
   and write it so C.6.a's written chapter does not need reopening.
3. **The exposure is a distribution statistic, and the units question is not cosmetic.** Gini, top
   shares, 90/10 ratios and local-area dispersion are not interchangeable, and neither are their
   levels of measurement (national panel vs. commuting zone vs. school district). Name the admissible
   exposure set before querying. `stratify-before-counting-poolable` applies at extraction, but the
   strata have to be derivable from a required-tags list decided here.
4. **SDT-only per the registry, so name the demsig route before searching.** Per
   `three-demsig-routes-before-not-assessed`, decide now which of the three routes is live. Inequality
   series exist for the SDT window (WID, LIS, Census), so slope sufficiency is computable the way
   C.6.a's sign test and C.2.b's price index were — **pre-register the sign**: the hypothesis requires
   inequality to have risen across the window in the countries whose fertility fell. Where it did not,
   the cell is settled by the sign regardless of the elasticity estimates.
5. **Kearney–Levine is a seminal cite whose most famous result is about the wrong outcome.** Its
   headline is teen childbearing and "economic despair", which is D.3.c's estimand (drafted) and not a
   status-competition-in-investment mechanism. Decide at stage 2 whether the teen-birth arm is in
   scope, and expect `design-is-not-a-property-of-the-title` to bite: routing here will have to be
   read off mechanisms, not titles.
6. **The mechanism is a conjunction and the middle link is the one to count.** Inequality → required
   investment per child → fertility. The first and last links have literatures; the middle one may
   not be measured in either. Per `b7-antidepressants` and D.3.c, count identified estimates per link
   before writing a verdict, and do not let a well-populated first link stand in for the chain.

## Assets in hand before the cold start

- **Free seeds.** D.2.d, C.6.a, C.2.b, C.3.e and C.3.g all plausibly routed inequality-and-investment
  records into their own screen files. Port the free-seed harvester (`317_c2b_free_seeds.py`); it is
  `snowball-pools-omit-their-own-seeds` in reverse and costs nothing.
- **Resolver.** `source/lib/textnorm.py` is now canonical on `main` (TICK-074, merged 2026-09-08) —
  import it, do not copy a `norm()`. Port the anchor resolver from `319_c2b_cold_start_anchors.py`,
  the newest copy.
- **Script numbering.** Max across **every branch on origin** is 327, so C.2.f starts at **328**
  (`script-number-collision`: start above every branch, not above main).
- **Merge debt is a live hazard for this chapter.** The frame probe (`304_`), the shared OpenAlex
  client (`source/lib/openalex.py`) and every script this ticket ports sit on unmerged branches. Note
  what gets ported and from where, or the next chapter re-derives it.

## Log

### 2026-09-08 — stage-2 term diagnostics, and the frame is NOT what ranked it

Scripts `328_c2f_term_diagnostics.py` and `329_c2f_second_channel.py`; logs
`literature/search-logs/c2f-term-diagnostics-2026-09-08.md` and `c2f-second-channel-2026-09-08.md`.
Counting only, no records retained, both re-runnable. 24 and 14 measurements, **zero refused** — the
first run of `328` had 6 requests throttled by OpenAlex's >5-boolean-operator limit and the `Refused`
path kept them out of the counts rather than recording them as zeros, which is the whole reason that
path exists.

**The union frame reproduces: 716 today against 714 on 09-03.** Everything below is inside it.

**Finding 1 — 89% of the frame is one general-purpose term.**

| measurement | n |
|---|---|
| C.2.f union frame | **716** |
| `"income inequality"` alone, fertility-restricted | **635** |
| the whole axis MINUS `"income inequality"` | **83** |
| `"income inequality"` unrestricted | 49,350 |

The six mechanism-specific terms sum to 83 and the axis-minus-largest is also 83, so they barely
overlap: status competition 13, relative status 44, social comparison 24, positional competition 2,
positional good 0, educational arms race 0.

**This falsifies the reason I picked C.2.f over A.6.** The "Why this one now" section above argues
that C.2.f's 539-of-714 core is "an anchored literature rather than a vocabulary artefact", against
A.6's 12-of-675. That was read off the probe's pass-1 label without checking what the pass-1 query
contained — it is `("income inequality" OR "status competition" OR "positional competition" OR
"relative status")`, so the 539 is the same general term, not a core. On the metric I actually meant,
C.2.f is **83/716 = 11.6%** mechanism-specific against A.6's **12/675 = 1.8%** — still ~6x better,
and C.2.f additionally has a real Tier-A theory canon and a large middle-link literature to snowball,
which A.6 does not. **The pick stands; the stated reason for it does not.**

**Finding 2 — the middle link has a large literature and it does not touch fertility.**

The mechanism is a conjunction: inequality → required investment per child → fertility. Second
channel, sharing no phrase with the first:

| measurement | n |
|---|---|
| shadow education / private tutoring × inequality | 580 |
| enrichment / extracurricular spending × inequality | 343 |
| `"educational arms race" OR "credential inflation"` | 221 |
| parental spending responds to inequality | 40 |
| **full chain: exposure AND investment AND fertility** | **2** |
| **full chain: status/positional AND investment AND fertility** | **2** |

Known-positive controls alive on the same channel (Q-Q 683, intensive parenting 29, shadow education
1,285), so the 2s are measurements and not a dead query.

**Read this as a lower bound, not as the evidence base.** These are title/abstract phrase counts; a
study can estimate the chain without carrying all three vocabularies in its abstract, and
`tier-a-anchors-are-studies` says the hand-sourced canon (de la Croix–Doepke 2003, Kearney–Levine
2014, Doepke–Hannusch–Kindermann–Tertilt 2022) will not come from counts at all. But the shape is
B.7's and A.24's: **expect an empty or near-empty primary cell and an UNEVALUATED verdict**, per
`empty-cell-is-the-result`, and plan the chapter as the rigorous establishment of that rather than as
a pooling exercise.

**Two corrections to the scope above, both now measured.** Ruling 3's exposure set must include the
distribution statistics, which the 09-03 axis missed entirely — `"Gini"` alone is 288 inside the
frame, top income share 8, wage dispersion 36, relative deprivation 35, status anxiety / positional
externality 34. And `"credential inflation"` is worth ~205 records on its own against
`"educational arms race"`'s 16; it belongs in the axis.

**Boundaries are small inside the frame and none is alarming:** C.3.d 8, D.2.d 3, C.6.a 15. The
C.6.a number matters because ruling 2 predicted that wall would be the expensive one — it is not.

Next: freeze rulings 1–6 with the revised exposure axis, then A3 cold-start anchors on the Tier-A
canon (import `source/lib/textnorm.py`, now canonical on `main`; do not copy a `norm()`).

### 2026-09-08 — walls measured (script 330) and the scope FROZEN

`literature/search-logs/rising-inequality-and-status-competition-search-scope.md`, 353 lines, on the
C.2.b section order. Walls, estimand cells, required tags, pooling rule and the demsig route are
frozen. Four PI calls open. `330_c2f_wall_probes.py` + log; 12 measurements, zero refused.

**The four walls that had no number now have one**, all inside the fertility-restricted frame of 635:

| wall | n | note |
|---|---|---|
| C.1.a own income | **90** | the largest, and the one most likely to be violated silently |
| C.5.a uncertainty | **70** | §7 row 3 moves dispersion and insecurity together |
| D.3.c despair / teen births | **21** | Kearney–Levine's headline is this, not status competition |
| C.2.h digital reference group | **1** | no screen rule spent |
| gender-inequality homonym | **30** | the gender-and-fertility literature is 2,281 and barely intersects |
| health / educational inequality | **8** | no screen rule spent |
| wrong direction (fertility → inequality) | **25** | context cell |
| cross-sectional gradient | **26** | context cell |

**A diagnostic of mine was refuted by its own output, exactly as `diagnostic-refuted-by-own-output`
predicts.** `330`'s identification probe used a narrow IDENT list — natural experiment,
diff-in-diff, IV, RDD, randomized — and returned **32** of 635. The list lacks bare `"experiment"`,
`"event study"`, `"synthetic control"`, `"quasi-experimental"`, and the panel vocabulary. Re-measured:
adding the first group gives 13 more, adding the panel group 59 more, and the **union of all three is
89**, 2.8x the narrow count. The scope document uses the range, not the 32, and notes that panel
fixed effects is weak identification *for this estimand* — a panel regression of fertility on a Gini
is still associational for a positional mechanism.

**The scope's substantive core is §2 and §4.** §2 freezes the C.3.d wall on return-vs-reference-
standard, written so C.3.d can inherit it. §4 records that both outer links of the conjunction have
substantial literatures, that the join has ~2 records, and that link 2 *is C.3.d's chapter* — so
C.2.f risks being composed entirely of its neighbours' links. §7 rows 6 and 7 (rank-based school
allocation; shadow-education bans, Korea 1980 and China 2021) are named as the only two places where
the positional mechanism separates from the return, and row 7 sits directly on the missing link.

**PI call 1 is the real one**: whether C.2.f survives as its own chapter, merges into C.3.d as its
positional arm, or waits for C.3.d. Recommendation recorded as run-it-and-report-UNEVALUATED.

Next: free-seed harvest (331), then build the inequality series and run the §5 sign test **before**
the production query — on C.6.a the sign test settled the cell, and on C.2.b the index inverted its
own answer once the deflator was fixed.

### 2026-09-08 — §5 sign test run BEFORE the production query, and the sign fails in 8 of 21

`source/build/331_c2f_sign_test.py`, log `literature/search-logs/c2f-sign-test-2026-09-08.md`, raw
pulls deposited in `data/raw/wdi-inequality-fertility/` — **the first real contents `data/raw` has
had** (`data-raw-is-empty`). World Bank WDI, `SP.DYN.TFRT.IN` and `SI.POV.GINI`, 21 SDT-core
countries, 42 pulls, zero refused. Re-running re-uses the deposit rather than re-fetching.

Order changed from scope §15: the free-seed harvest was to be 331 and this 332. Swapped because the
harvest reads neighbouring chapters' screen files, which sit on unmerged branches; this test depends
on nothing but public data. The harvest keeps its place in the plan.

**Result 1 — the pre-registered sign fails in 8 of 21 countries.**

| | countries |
|---|---|
| Gini RISING, sign supports the hypothesis (13) | USA, GBR, DEU, ITA, ESP, SWE, AUS, DNK, NOR, FIN, BEL, AUT, KOR |
| Gini FALLING, sign runs against it (8) | **FRA, NLD, JPN, CAN, CHE, PRT, GRC, IRL** |

Fertility fell in all 21. So in **38% of the SDT core the exposure moved the wrong way**, and the
hypothesis has to explain those countries' declines with something else. Reported sign-first: the R²
column shows why (`r2-criterion-is-sign-blind`) — IRL fits at R²=0.76 and PRT at 0.67, both with the
correlation running *against* the hypothesis. A fit criterion alone would have counted them as
support.

**Result 2 — median 79% of the SDT decline predates the inequality series, and the caveat is the
finding's limit.** Range 20–103% across 20 countries. **This measures when the exposure becomes
OBSERVABLE in WDI, not when it moved**, so it is suggestive and confounded with data availability —
a Gini series starting in 1987 does not mean inequality was flat before 1987. The log now says so in
its own generated text rather than only here, because the first version of that summary asserted
"the elasticity cannot be doing the work", which the data cannot support.

**The substantive version is the next test and it is worth running.** The claim that inequality was
flat or falling from 1945 to ~1980 while the main SDT fertility collapse ran 1965–1980 needs a
long-run series — WID top shares, Atkinson/Piketty/Saez — not the absence of WDI data. If it holds,
this is B.7's finding in a second chapter (67.6% of the SDT decline predating the exposure) and it
would settle the SDT cell on timing rather than on elasticity. WID's bulk file is 882 MB, so this
needs a per-country route rather than the whole download.

**Where this leaves the chapter.** Two independent lines now point the same way: §4's conjunction has
~2 records at the join, and the exposure has the wrong sign in 38% of the countries and is
unobservable across most of the period in which the outcome moved. Neither is yet a verdict — both
are pre-search measurements — but the working expectation of **SDT UNEVALUATED or a demonstrated
wrong sign** is now supported by two channels rather than one.

DEU's 103% is arithmetically correct: TFR fell below its end-of-window level and partially recovered.
Flagged in the log so it is not read as the >100% banding error the chapter template forbids.

Next: long-run WID series for the timing test, then the free-seed harvest, then anchors.

### 2026-09-08 — timing test on a long-run series: the exposure moves the wrong way through most of the decline

`source/build/332_c2f_timing_test.py`, log `literature/search-logs/c2f-timing-test-2026-09-08.md`.
Exposure: **WID top-10% pre-tax income share** via Our World in Data's grapher CSV — the same
variable as WID's 882 MB bulk file at 95 KB — deposited in `data/raw/wid-top10-share/`. Outcome: the
WDI TFR pull from 331, read from its deposit rather than re-fetched.

This is the substantive version of 331's suggestive result, and it survives the caveat that killed
it: **the inequality series covers the whole period here, so nothing is confounded with data
availability.**

**The test.** Rich-country inequality is U-shaped — falling to a post-war trough, rising after. The
SDT fertility collapse ran roughly 1965–1980. What share of the decline was complete **before
inequality turned up**? The trough is found in the data, not assumed, and the pre/post slopes are
reported so a country with no U-shape shows as one.

**Result: median 69% of the SDT decline was complete before inequality turned up. Range 31–84%,
across 9 countries with a computable share, 8 of 10 U-shaped.** In every one of the ten the
pre-trough inequality slope is **negative** — so through the period carrying most of the fertility
decline, the exposure was moving in the direction *opposite* to the one the hypothesis requires.

| | |
|---|---|
| GRC 84 · CHE 83 · FRA 80 · SWE 76 · AUS 69 | most of the decline predates the turn |
| FIN 51 · PRT 48 | roughly half |
| USA 34 · IRL 31 | most of the decline follows the turn — these run WITH the hypothesis |

**The carry-away number is an upper bound, and it is the useful output.** In the median country only
about **31%** of the SDT decline is even *available* for this mechanism to explain, because the rest
happened while the exposure moved the other way. That bound is derived from exposure and outcome
alone and holds whatever the elasticity turns out to be — `slope-sufficiency-beats-a-missing-share`:
no denominator needed, ask whether the exposure moved the right way.

**Three limits are in the log rather than buried, and the first is material.** TFR is a period
measure and the 1965–1980 collapse is **partly tempo, not quantum** — A.11's chapter. Postponement
depresses period TFR without an equal fall in completed cohort fertility, so a cohort series would
put less of the decline in the pre-trough window. **The bias runs against the finding**, so 69% is an
overstatement of unknown size and the test must be re-run on HFD completed cohort fertility before
the number enters a verdict. Also: the trough of measured inequality is not necessarily when the
mechanism switches on (the registered claim is about *rising* inequality, so the test is fair to the
claim as written); and 11 of 21 countries are excluded for thin pre-1980 coverage, including GBR,
DEU, ITA, ESP and JPN.

**Three independent lines now agree**, all pre-search: the conjunction has ~2 records at its join
(§4), the exposure has the wrong sign over the whole window in 8 of 21 countries (331), and it moves
the wrong way through ~69% of the decline in the countries with long series (332). None is a verdict
— the literature has not been searched — but the SDT cell now has a **pre-registered upper bound of
roughly 31%** before a single study is read.

Next: re-run 332 on HFD completed cohort fertility to remove the tempo bias, then the free-seed
harvest and cold-start anchors.

### 2026-09-08 — tempo adjustment: 332's carry-away number does NOT survive

`source/build/333_c2f_tempo_adjusted_timing.py`, log
`literature/search-logs/c2f-tempo-adjusted-2026-09-08.md`. Eurostat `demo_find` (`TOTFERRT`,
`AGEMOTH`) deposited in `data/raw/eurostat-fertility/`.

HFD cohort fertility needs an account, so the tempo correction is computed instead from data that is
open: Eurostat carries mean age at childbirth from 1960 beside the TFR, which gives the
Bongaarts–Feeney adjustment `TFR/(1-r)` directly.

**The first run of this check produced three false numbers and I nearly reported them.** It returned
SWE **-156%** — an impossible share — FRA compared against 332 using a window that silently started
in **1999** rather than 1965, and a headline "median falls 76% → 32%" computed over two different
country sets. Three guards now stand, each named after the failure that motivated it: a **common
window** (refuse a country whose adjusted series does not start at 1965), a **denominator floor**
(a share whose denominator is under 0.25 children is undefined, not small — that was Sweden at
-0.14), and a **plausibility band** against the unadjusted series. FRA and SWE are now reported
`UNCOMPUTABLE` **with the reason printed in the table** rather than as numbers.

**Result, like for like on the five countries where both measures compute** (FIN, PRT, GRC, IRL, CHE):

| measure | median share of the SDT decline before the inequality trough |
|---|---|
| period TFR | **51%** |
| tempo-adjusted | **32%** |

Per country: CHE 83→73, FIN 51→30, GRC 84→32, IRL 31→23, PRT 48→49.

**This retracts the carry-away number I recorded three hours ago.** 332's "median 69%, so only ~31%
of the SDT decline is available for this mechanism" is **not robust**. The correction runs in the
predicted direction and is large: on these five countries roughly **two thirds** of the decline
remains available to the mechanism, not one third. **332's 69% is an upper bound and nothing more.**

**What survives is directional, and it is weaker than what 332 claimed.** A substantial part of the
SDT decline does predate the inequality turn — every computable country still shows 23–73% — and in
all ten countries of 332 the pre-trough inequality slope is negative. But the *fraction* is not
pinned down, and no share number should enter a verdict until the definitive version is run on HFD
completed cohort fertility. ~~**HFD requires an account: that is a human step, like the B.1 Zotero retrieval, and it is the
blocker to name in the PI packet.**~~ **RETRACTED 2026-09-08 — see the correction entry below.
Eurostat `demo_frate` gives single-year ASFR from 1960; cohort fertility is the diagonal sum and
needs no account. There is no blocker.**

The aggregate BF adjustment is also not the parity-specific form its authors recommend, and `r` is
smoothed over 5 years. Both are stated in the log.

**Status of the three pre-search lines**, revised:
1. §4's conjunction has ~2 records at the join — **unchanged**.
2. The exposure has the wrong sign over the whole window in 8 of 21 countries (331) — **unchanged**.
3. Timing (332) — **weakened**: directionally intact, magnitude retracted pending HFD.

Next: free-seed harvest and cold-start anchors. The demsig side is as far as it goes without HFD.

### 2026-09-08 — CORRECTION: the HFD blocker recorded above is false

**Retracting the sentence "HFD requires an account: that is a human step, like the B.1 Zotero
retrieval, and it is the blocker to name in the PI packet."** It is wrong and it must not go to the
PI. There is no blocker.

**Eurostat `demo_frate` carries single-year age-specific fertility rates for 1960–2024.** Completed
cohort fertility is the diagonal sum of that table (cohort = year − age), so every cohort whose full
15–49 span falls inside the window is directly computable — **cohorts born 1945 through 1975**,
which is exactly the SDT range. That is the same construction HFD performs. HFD is a convenience
here, not a requirement.

**How the false blocker was produced, because the mechanism matters more than the fact.** I guessed
four OWID grapher slugs and one HFD download URL, got 404s from all five, and recorded a
human-in-the-loop blocker. I did not query the Eurostat catalogue, which answers it in one request.
That is `refusals-read-as-zeros` — a failed search reported as an absence — committed while writing
explicit `Refused` handling into scripts 328–333 so that the *API* could not do the same thing to me.
The guard was pointed outward and not at my own search.

**A second error, larger and quieter: cohort fertility does not fit the test I said it would
settle.** CFR is indexed by birth cohort; `332` asks what share of the *calendar-time* decline
preceded a *calendar-time* inequality trough. The two do not align without an explicit mapping —
attributing each cohort to its mean year of childbearing, or re-expressing the exposure in cohort
terms. Obtaining HFD would not have closed the question; it would have changed it. **Naming a data
source as "the definitive version" without checking that its index matches the test is the real
mistake here**, and it is the one worth carrying forward.

**Revised next step**, replacing "get HFD credentials": build completed cohort fertility from
Eurostat `demo_frate` (script 334) and re-run the timing test with the cohort→calendar mapping stated
as an assumption rather than buried. This also removes Bongaarts–Feeney from the chain entirely —
no `r`, no division by `(1-r)`, and none of the blow-ups that made `333` need three guards.

`333`'s substantive result is unaffected: the tempo correction still runs against `332`, and `332`'s
69% is still an upper bound. Only the claim about what is needed to settle it changes.

### 2026-09-08 — free seeds (335) and cold-start anchors (336)

**Free seeds: 393 records recovered at zero retrieval cost**, from 1,830 branch:file pairs across
142 unique blobs. Yield per term repeats §3's diagnostic exactly: `income inequality` returns 189
(186 catchable by no other term) while the entire mechanism-specific vocabulary — status competition
4, positional 2, relative status 11, social comparison 13, arms race 7, relative deprivation 4,
distribution statistics 5 — returns **46 between them**. `shadow education` returns 19 free records
on link 1, the link §4 measured as missing from the fertility literature.

I misread the head of the `investment per child` term (143 records) as mostly Trivers-style
evolutionary parental investment. **Measured, that cloud is 31 of 143 (23%)**; the bulk is the
economics sense, which is C.3.d's quantity-quality literature — Wall 1's packet, not contamination.
Both clouds now have their own counted column rather than an eyeball
(`citation-sorted-head-is-not-the-population`). Neither is dropped: 9 records are evolutionary AND
carry a C.2.f exposure term (conspicuous-consumption signalling, sexual selection and growth), which
is where boundary cases live.

**Anchors: 65/65 controls and 13/14 hand, zero ghost citations.**

| | |
|---|---|
| control (taken programmatically from 335, never retyped) | **65/65** — `MATCH_BY_DOI` |
| hand (the Tier-A canon) | **13/14** clean |
| the exception | Frank 2007 *Falling Behind* → `MATCH_TITLE_AUTHOR_DISAGREES`, top candidate a **Choice Reviews Online book review** of it |

That exception is the `anchor-resolver-book-canon` failure caught working: a monograph resolving to
its own review at Jaccard 1.00, refused by the first-author gate. All four positional monographs —
Hirsch, Frank, Schor, Veblen — went through that gate and only the review was rejected.

**A false alarm I raised and then measured away, worth recording because the shape recurs.** The
resolved records appeared to carry no author list at all, which would have meant the first-author
gate silently no-opped on all 79 (`optional-field-gate-disengages`). It does not: `top_candidate`
stores the field as `authors_first`, and I queried `authors`, which is never written.
`first_author_ok` is **True on 13 hand anchors and False on exactly the book review**. The gate is
live. `candidate-attribution-is-the-error` — check which side is wrong before keying an exception —
and the wrong side was mine.

Two OpenAlex metadata oddities, both benign once the author gate is read: Schor's *The Overspent
American* carries venue "Medical Entomology and Zoology" (first author still checks out, so the venue
field is noise), and Hirsch's *Social Limits to Growth* resolves to a 1976 `article` rather than the
Harvard UP book, with Hirsch as first author.

**§4's conjunction now has a second, independent confirmation on the canon rather than on counts.**
Of the 14 hand anchors, **9 are flagged `outcome_is_fertility: false`** — Ramey & Ramey, Kornrich &
Furstenberg, Schneider et al., Frank's *Expenditure Cascades*, and the four positional monographs.
The positional and link-1 canon is real, resolvable and substantial, and it **does not measure
fertility**. That is the chapter's central problem stated in its own seminal literature.

Next: production query on the revised axis (337).

### 2026-09-08 — production query (337), and §4's central finding is RETRACTED

**The headline first: the full chain is not empty. Scope §4 is withdrawn and amended as §4A.**

`338` + log. §4 probed the conjunction in economics-of-inequality vocabulary and got **2** records.
The same chain in the East Asian education-competition vocabulary returns **56** (shadow education /
private tutoring / cram school × fertility), **14** (education competition × fertility) and **20**
(tutoring ban / "double reduction" × fertility). Titles include *The impact of shadow education
expenditures on fertility rates in South Korea*, *Education Competition and Fertility Intention:
Evidence from China's Private Tutoring Ban*, and *Expansion of shadow education, status
externalities, and fertility intentions*.

**This lands scope §7 row 7**, which was pre-registered as one of only two places where the
positional mechanism separates from the return. China's 2021 tutoring ban is a policy shock to
required investment per child with fertility outcomes attached.

`"involution"` (*neijuan*) is REFUSED and the refusal recorded: 398 records against the fertility
axis, all the veterinary/obstetric homonym — uterine involution in dairy cattle, thymic involution in
pregnancy, 7,379 records in that vocabulary.

**How it surfaced, via two of my own errors.**

1. **The first control list was not a control list.** It required only "carries an exposure term and
   has a DOI", which admitted *The Nuclear Arms Race: An Evolutionary Perspective* and *Conspicuous
   Consumption: Vehicle Purchases by Non-Profits*. The mechanism arm read **2/57** — a number that
   measured my list, not the query. Controls now require an exposure term AND a fertility outcome;
   the interpretable figure is **2/13**.
2. **Then 2/13 was itself the finding.** I tested the recall mechanism against those 13 controls
   before blaming the query: the outcome axis alone returns each of them, so recall measurement was
   sound and the controls genuinely lacked the arm's vocabulary. Reading them showed they were never
   status-competition records — they are the shadow-education cloud. A calibration failure was the
   route to the substantive result.

**Calibration state, and it is NOT ready for a screen universe.**

| arm | recall | frame |
|---|---|---|
| `dispersion` | 13/16 | 851 |
| `mechanism` | 2/13 | 92 |
| `link1-investment` | 0/5 | 47 |
| `positional-canon` | 0/3 | 5 |
| `c3d-boundary` (not screened) | 0/1 | 683 |
| **union primary** | **5/15 (33%)** | **982** |

33% is far below the ~90% floors C.2.b and C.6.a calibrated to. Two structural reasons, both real:
the `mechanism` arm's controls belong in a sixth arm that does not yet exist (§4A), and the
`positional-canon` monographs are **not retrievable by vocabulary at all** — *The Theory of the
Leisure Class* contains neither "positional good" nor an investment term, so those anchors have to
come through the citation channel rather than a query.

**Also fixed:** the generated report carried C.6.a's script name, a hardcoded 2026-09-03 date and
C.2.b's arm prose describing fee-abolition and time-cost arms this chapter does not have. The port
copied the code and not the report text.

Next, in order: (1) sixth arm in the education-competition vocabulary and re-assign the 13 mechanism
controls to it; (2) homonym-check `"educational burden"` (117, unchecked); (3) re-calibrate to a
stated recall floor; (4) only then build the screen universe.

### 2026-09-08 — production query CALIBRATED at 92%, frame 1,016

Scripts `339` (candidate builder) and `337` (calibration). The §4A channel was added as a sixth arm
and the calibration converged.

| arm | recall | frame |
|---|---|---|
| `dispersion` | **12/13** | 851 |
| `mechanism` | **2/2** | 92 |
| `education-competition` (§4A, new) | **7/8** | 43 |
| `link1-investment` | 0/5 | 47 |
| `positional-canon` | 0/3 | 5 |
| `c3d-boundary` (not screened) | 0/1 | 683 |
| **union primary** | **11/12 — 92%** | **1,016** |

92% meets the floor C.2.b (93%) and C.6.a calibrated to. The union query was checked to recall the
same anchors the arms recall separately (11 vs 11), so the nested boolean is being parsed as
intended and its count is usable.

**The two zero arms are not failures and must not be re-tuned into the union.** `link1-investment`
and `positional-canon` target anchors whose own outcome is not fertility, so they are excluded from
`PRIMARY_ARMS` by construction. *The Theory of the Leisure Class* contains neither "positional good"
nor an investment term: those anchors are **not retrievable by vocabulary at all** and route to the
citation channel. Spending frame on them would buy nothing.

**The candidate builder is now a script (`339`) because it was wrong twice as inline code.** v1
required only an exposure term plus a DOI and admitted *The Nuclear Arms Race: An Evolutionary
Perspective*. v2 added a fertility word and the `birth` word-boundary admitted *…and the birth of
Haute Couture* and *…the Birth of the Consumer in Japan* — "birth of X" is an idiom, not an outcome.
v3 excludes the idiom by name, excludes the behavioural-ecology cloud, and **derives the arm from the
title's own term family** rather than from the free-seed bucket. That last change is what fixed the
mechanism arm: every shadow-education record had been landing in `mechanism`, which is why it scored
2/13 against vocabulary it does not contain.

**One anchor was corrected on my side, not OpenAlex's.** *The impact of shadow education expenditures
on fertility rates in South Korea* came back `NEEDS_HUMAN_READ` at Jaccard 1.0 with an exact title
match in *Journal of Population Economics*: the year was mine, hand-typed as 2024 against a true
2026. `candidate-attribution-is-the-error`.

**`"education expenditure"` is excluded from the new arm by decision, not oversight.** It returns 102
against the fertility axis and splits roughly 50/50 into household and **government** spending; the
public-finance half is C.2.d's estimand. `"educational burden"` (16) carries the household sense.

**Stage 3 is now unblocked.** 1,016 records is a screenable frame — an order of magnitude below the
pools D.1.a and A.18 had to bound by sampling.

Next: screen universe and rubric (340). The rubric must carry `return_separated` and `own_income_held`
as screen-visible fields, or Walls 1 and 4 cannot be enforced at title/abstract.

### 2026-09-08 — screen universe built: 1,366 records, ready to screen

`340_c2f_screen_universe.py`, ported from C.2.b's `321`. Also landed the shared OpenAlex client on
`main` (`source/lib/openalex.py`, written for C.2.b and stranded on its branch since 09-03) rather
than making a second copy of it — it is purely additive, nothing on `main` imports it, so unlike the
textnorm fix it cannot change existing behaviour. Both `main` checks stayed green.

**Every arm contributes genuinely new records — none is redundant** (`dedup-before-counting-hides-
redundant-rung`):

| arm | declared | pulled | new after dedup |
|---|---|---|---|
| dispersion | 851 | 851 | 851 |
| mechanism | 92 | 92 | 79 |
| education-competition | 43 | 43 | 42 |
| link1-investment | 47 | 47 | 39 |
| positional-canon | 5 | 5 | 5 |

Universe **1,366**; anchors 22 present / 12 injected; free seeds 40 present / 338 injected / 15
unmatchable; **gold found by query 19/22**. Gold flags are withheld from the file the screen reads.

**The abstract enrichment is new work and it was needed.** The port injected anchors and free seeds
with title and DOI only, so 350 of the universe's 550 missing abstracts were the injected records —
a **100%** miss rate against 19–26% for the query pull. Those are the highest-value rows in the
universe (`tier-a-anchors-are-studies`: on D.2.d that distinction was 2 studies against 9), and a
title-only row cannot carry scope §10's tags (`design-is-not-a-property-of-the-title`).

Two rungs now run, and the first one was broken in a way worth recording. It filled **0 of 232 while
refusing nothing** — injected records store the bare id `W2048002868` while the query pull and the
API both return `https://openalex.org/W2048002868`, so the lookup matched nothing. A silent zero from
an id-format mismatch, in a session where I have flagged three others. There is now a **loud warning
when enrichment fills nothing while refusing nothing**, because that combination is always a bug and
never an absence. Rung 2 (DOI) then covered the 118 injected records that had no OpenAlex id at all
and were never tried by rung 1 (`rung-found-is-not-rung-fetched`).

Result: **237/550 filled, no-abstract down from 550 to 313 (23%)** — in line with the query pull's
natural rate, so what remains is genuine absence rather than a fetch we skipped.

One loose end: `dispersion` declared 851 and pulled 852 on one run, a one-record drift between
calibration and pull. Not blocking, but it should not be silent — noted for the screen log.

Next: the screen rubric. It must carry `return_separated` and `own_income_held` as screen-visible
fields or Walls 1 and 4 cannot be enforced at title/abstract, and the rubric needs an
`education-competition` cell that scope §4A only created today.

### 2026-09-08 — rubric frozen, depth probe screened (150 of 1,366)

**Rubric frozen before any record was screened**,
`literature/search-logs/rising-inequality-and-status-competition-screen-rubric.md`, 136 lines.
`return_separated` and `own_income_held` are screen-visible fields, because Walls 1 and 4 are this
chapter's two largest (8 and 90 records) and a wall the screen cannot see is a wall it cannot
enforce. `UNCLEAR` is an explicit legitimate value on both and **must not be coerced to `NO`** — the
count of `UNCLEAR` is itself a finding and it sizes the full-text work.

Batcher `341` ported from C.2.b's `322`. Its screen-id prefix was literally `C2B`, which would have
collided with C.2.b's ids in any shared table; now `C2F`.

**Depth probe: 5 strata x 30 = 150 records (11%), evenly spaced by citation rank.**

| cell | n |
|---|---|
| `OFF_OTHER` | 120 |
| `THEORY` | 10 |
| `INEQ_INVESTMENT` | 6 |
| `WRONG_DIRECTION` | 5 |
| `EDUCOMP_BOUNDARY` | 4 |
| `INEQ_ASSOCIATION` | 2 |
| `QQ_BOUNDARY` | 1 |
| **`REQUIRED_INVESTMENT_FERTILITY`** | **1** |
| **`DISPERSION_FERTILITY`** | **1** |

**Primary yield 2/150 (1.3%), and the curve is inverted.** By stratum: 0, 0, 0, 1, 1. The citation
HEAD holds no primary cell at all — it is the canon (Veblen, Hirsch, Schor, Becker, de la Croix,
Doepke, Ramey & Ramey, Kornrich, Schneider, Frank), which is 10 `THEORY` plus 6 `INEQ_INVESTMENT`.
Both primary candidates sit in the deep strata. This is the opposite of A.18's declining curve, and
it is a warning against ever screening this universe front-to-back
(`citation-sorted-head-is-not-the-population`).

Best candidate found: **C2F1108, *Development Strategy, Relative Deprivation and Fertility Behavior
in Taiwan* (1979)** — relative deprivation against fertility behaviour, which is the registered
exposure against the registered outcome. It is a PhD thesis whose abstract is the single word "PhD",
so it is title-only and needs full text.

**The probe design under-samples the arm that matters, and that is the actionable finding.** Strata
are evenly spaced across all 1,366 records, which are dominated by `dispersion` (851). The
`education-competition` arm — scope §4A's recovered channel, the one carrying the China 2021 and
Korea 1980 policy shocks — is **42 records, 3% of the universe**, so an 11% sample reaches about
five of them. The 1.3% primary yield is therefore a statement about the dispersion literature, not
about this chapter's best cell.

**So the next pass is not a bigger sample.** `education-competition` (42) and `mechanism` (79) are
121 records between them and should be screened **exhaustively** — cheaper than another probe and
aimed where the primary cells are. `dispersion`'s 851 can then be screened knowing its measured
yield is near zero, which is exactly the cost information the probe existed to buy.

30 of the 150 were title-only and are flagged as such.

### 2026-09-08 — targeted arms screened exhaustively: the primary cell is 18 records, not empty

`341 --arms education-competition,mechanism`: **134 targeted records screened exhaustively, mixed
with 67 shuffled decoys** drawn from the rest of the universe. Decoys exist because a pure
single-arm batch tells the screen every row's arm, and the arm predicts the cell; with them, no row's
arm is inferable from its position.

**The arm-targeted pass is 10x the citation-ranked probe, and the decoys prove it is the targeting
and not the screener.**

| | primary yield |
|---|---|
| targeted arms (`education-competition` + `mechanism`) | **18/134 — 13.4%** |
| decoys (rest of universe, mostly `dispersion`) | **0/67 — 0.0%** |
| the earlier citation-ranked probe | 2/150 — 1.3% |

**The primary cell now holds 18 records**, against the ~2 that scope §4 measured this morning and the
"expect an empty cell" it concluded:

| cell | n |
|---|---|
| `DISPERSION_FERTILITY` | **8** |
| `REQUIRED_INVESTMENT_FERTILITY` | **6** |
| `POSITIONAL_ALLOCATION_FERTILITY` | **2** |
| `TUTORING_POLICY_FERTILITY` | **2** |
| `PERCEIVED_STATUS` (separate outcome level) | 1 |

Plus 15 `EDUCOMP_BOUNDARY`, 10 `QQ_BOUNDARY` (Wall 1's packet), 6 `WRONG_DIRECTION` (Wall 9), 7
`THEORY`, 4 `INEQ_ASSOCIATION`.

**The single most valuable record in the chapter is C2F1279:** *The impact of China's "Double
Reduction" policy on the fertility and education investment behaviour* (2026). One policy shock,
**both** outcomes — the required investment per child AND fertility. That is
`one-study-can-carry-the-structure`: a design estimating both links beats any cross-literature count,
and scope §7 row 7 pre-registered exactly this as the place to hunt. C2F0428 (*Education Competition
and Fertility Intention: Evidence from China's Private Tutoring Ban*) is the same shock on the
intention outcome.

The `DISPERSION_FERTILITY` eight are mostly China/Korea/Taiwan micro studies using relative
deprivation or realized-vs-desired fertility gaps, plus the 1979 Taiwan thesis the probe found and a
1987 status-anxiety paper. **Whether any of them separates the return from the reference standard
(Wall 1) or holds own income fixed (Wall 4) cannot be judged at title/abstract** — that is what
`return_separated` and `own_income_held` exist to record, and it is the full-text question.

**6 of the 18 are title-only** and need full text before anything is claimed about their designs.

**What this means for the remaining screen.** `dispersion`'s 851 records now have two independent
measurements of near-zero yield (0/67 decoys, and the probe's dispersion-dominated 1.3%). They are
**not** skippable — the probe's curve was flat and its cleanest record was in the last stratum — but
they can be screened last and at lower priority, which is exactly the cost information the probe was
bought for.

**PI call 1 should now be answered differently from this morning.** The recommendation recorded at
scope §14 was run-it-and-report-UNEVALUATED. On 18 primary records including a policy shock with both
outcomes, C.2.f is a chapter with an evidence base, and the question is no longer whether it survives
but whether Wall 1 can be enforced at full text.

### 2026-09-08 — tier-1 full-text retrieval: 7/19, and the cell that matters is EMPTY

`342_c2f_fulltext_retrieval.py`, ported from C.2.b's `324` with the rung order re-argued for this
literature rather than inherited.

**Three rung predictions were recorded in the script docstring BEFORE the run, and all three held:**

| rung | predicted | measured |
|---|---|---|
| `oa_location` | carries most of it | probed 19, **found 19, fetched 7** |
| `wp_host` | little — not an NBER/IZA literature | probed 19, found **0** |
| `pmc_bioc` | empty — no biomedical indexing | probed 12, found **0** |

`unpaywall` probed 12, **found 4, fetched 0** — not dead, its URLs are blocked. That is
`rung-found-is-not-rung-fetched` reproducing: one counter would have reported it as an empty rung.

**Coverage by cell is the number, not the 37% rate** (`retrieval-rate-hides-which-records`):

| cell | retrieved |
|---|---|
| `DISPERSION_FERTILITY` | 4/8 |
| `REQUIRED_INVESTMENT_FERTILITY` | 2/7 |
| `POSITIONAL_ALLOCATION_FERTILITY` | 1/2 |
| **`TUTORING_POLICY_FERTILITY`** | **0/2 — EMPTY** |

**The empty cell is the one carrying the boundary-spanning design.** C2F1279 (*The impact of China's
"Double Reduction" policy on the fertility and education investment behaviour*, **Applied
Economics**, Taylor & Francis) and C2F0428 (*Education Competition and Fertility Intention: Evidence
from China's Private Tutoring Ban*, SSRN). Both are recoverable — T&F is squarely inside the
UChicago proxy and SSRN is free but bot-defended — but **neither can be read until a human runs the
handoff, and the chapter's best evidence is behind that step.** 37% would have read as survivable;
0/2 on this cell is not.

**A third handoff kind, pre-registered and then measured.** The docstring predicted that regional
Chinese and Korean venues sit outside both open access and the UChicago proxy, making them a third
job rather than a `proxy` job. `reclassify_regional()` now looks up the **Crossref publisher** for
every `proxy` failure and moves it when the publisher is outside the set the library can be expected
to license. It moved one: *China Soft Science* (China Science Publishing & Media). Telling a human
to "try the proxy" for that would have burned the one expensive resource in this pipeline.
Handoff is now **5 proxy, 6 browser, 1 regional**.

**Two of my own reporting bugs, both caught before the numbers were written down.** The summary
counter was computed in the fetch loop and printed the PRE-reclassification handoff counts, so it
disagreed with the files on disk. And the new per-cell coverage line checked `status == "fetched"`
literally, reporting **0/19 primary against a true 7/19**, because a re-run reports
`already_on_disk` and a twin-covered record reports `covered_by_twin` — the script has a `GOT` set
for exactly this. Same shape as the id-format mismatch in `340`'s enrichment: a plausible-looking
zero from checking one literal.

Next: the handoff is a human step (5 proxy + 6 browser + 1 regional). Tier 2 (the 30-record boundary
packet) has not been run. **Extraction is gated on `TUTORING_POLICY_FERTILITY`**, so the two records
in it are the priority — not the 12-record total.

### 2026-09-08 — handoff installed (8) and browser job run: primary cell now 15/19

**Install (script `343`).** 10 PDFs supplied; **8 installed, 2 refused**, matched by CONTENT not
filename — the files arrive named `EBSCO-FullText-09_08_2026.pdf` and
`05E53C072D3948BDA9AEF3723DC3CF35.pdf`, so the filename carries nothing.

**The content match earned its keep immediately.** One file was *Mobile Health App Use Among Older
Adults* — not in this chapter at all. The other was *Gendered fertility intentions and child
schooling: insights on the quantity–quality trade-off from Ethiopia* (J. Demographic Economics 2025),
which my **first** matcher paired with C2F0844 *Marital Fertility and Investment in Children's
Education* at 0.80 token overlap. They share only the generic words fertility, investment, children,
education. The rule is now **contiguous title containment**, not token overlap, and both files were
correctly refused. `handoff-file-match-by-content`: a wrong pairing is worse than a missing file,
because it enters the extraction table looking correct.

The Ethiopia paper is **not in our universe and is plausibly on-topic** (quantity-quality, fertility
intentions). Logged as a candidate for the screen rather than discarded.

**Both gating cells are now COMPLETE:**

| cell | before | after |
|---|---|---|
| `TUTORING_POLICY_FERTILITY` | 0/2 | **2/2** |
| `POSITIONAL_ALLOCATION_FERTILITY` | 1/2 | **2/2** |
| `DISPERSION_FERTILITY` | 4/8 | 6/8 |
| `REQUIRED_INVESTMENT_FERTILITY` | 2/7 | 5/7 |
| **primary overall** | 7/19 | **15/19** |

C2F1279 (China's Double Reduction, both outcomes) and C2F0428 (tutoring ban → fertility intention)
are both on disk. **Extraction is no longer gated.**

**Browser job on the three browser-classified records — and it reclassified all three.**

- **C2F1108** — Deep Blue *loads*, but the file reads **"Access Restricted to UM users only."** So
  `browser` was the wrong call: no browser session gets this, it is an entitlement problem. The page
  names **ProQuest Dissertation No. 8007866**, which UChicago licenses. Reclassified `proquest` with
  that instruction.
- **C2F0721** — `ir.lib.ncu.edu.tw` returns a browser error page over both http and https. The URL is
  **dead**, not bot-defended. Title searches on both the Chinese and English forms returned zero web
  results. Reclassified `dead`; do not retry the URL.
- **C2F0515** — `en.cnki.com.cn` errors. CNKI is a subscription database, so this was never a browser
  job. Reclassified `regional`.

**All three were misfiled by the automated classifier, and the reason is general:** it infers the
handoff from an HTTP-level symptom (a 200 that is not a PDF, or no status line at all), and three
different underlying causes — an entitlement wall behind a public landing page, a dead host, and a
subscription database — all present the same way to curl. The classifier cannot see the difference;
opening the page can. That is worth carrying to other chapters.

Outstanding: **4** — C2F1108 (proquest), C2F0844 (proxy), C2F0515 (regional/ILL), C2F0721 (dead).
None is in a gating cell.

### 2026-09-08 — extraction begun, and it reverses which record carries the chapter

`extraction/rising-inequality-and-status-competition-extraction.csv`, 22 columns on the C.2.b
schema plus this chapter's `return_separated` / `own_income_held` / `link_measured` fields.

**I had the two `TUTORING_POLICY` records the wrong way round, and full text is what showed it.**

**C2F1279 (Zhou, Shao & Zhang, *Applied Economics* 2026) is mostly a SIMULATION.** I called it "the
single most valuable record in the chapter" and "one policy shock, both outcomes". At full text it
is two things: §III is an IV estimate on CFPS 2018 (n=3,481) of shadow-education **expenditure** on
fertility **intentions**, and §§IV–VI are a calibrated heterogeneous-agent model solved with a new
DeepHAM+DIRECT algorithm. **The Double Reduction result is model-generated — there is no DiD, no
event study, no estimate of the policy's effect on anyone's fertility.** Its own abstract says
"quantitative simulations show". That is `design-is-not-a-property-of-the-title` paying out exactly
as the rubric warned: I carried this through search, screen, priority retrieval and a handoff
request as the identified design.

Its empirical arm also has a specific problem worth recording: the instrument is **county-level peer
shadow-education expenditure**, and county-level peer spending *is the reference standard this
chapter names as the mechanism* — so it plausibly affects fertility intentions directly and the
exclusion restriction is doing heavy work. Flagged for risk of bias.

**C2F0428 (Meng, Wang, Yang & Zhang 2025) is the identified design, and it is a good one.**

- A survey experiment eliciting fertility intentions with and without the policy, within-subject with
  individual fixed effects plus a between-subject arm — **and** a city-level **DID on ACTUAL BIRTH
  RATES**, policy intensity measured as per-capita tutoring institutions in 2016, five years before
  the policy, against 2023 (319 cities) and 2024 (204 cities).
- Ban raises expected total fertility **7–8%**, larger where intensity is higher; the DID finds
  higher-intensity cities had significantly greater increases in actual birth rates.
- **The channel decomposition is what makes it C.2.f's rather than C.2.b's.** The primary driver is
  the *perceived reduction in educational competition* (45% of parents expected others to cut
  tutoring), ahead of parental health, then time (−0.69 h/day) and money (−275 RMB/month, −34.5%).

**This is the first record in the chapter where Wall 1 is actually satisfied.** A tutoring ban does
not change the **return** to human capital; it changes the investment required to hold a given rank
— and the authors' own footnote defines perceived competition as how hard it is for a child to
maintain the academic ranking that determines elite admission. `return_separated = YES`. Every other
primary record so far is `NO` or `UNCLEAR`.

**Consequence for pooling:** the two must never be pooled, though they nominally study the same
policy. One is an estimate and one is a simulation (`resolve-disagreements-dont-average`: ask whether
they share an estimator before averaging — here they do not even share an epistemic class).

Remaining: 13 of 15 retrieved records to extract.

### 2026-09-08 — extraction COMPLETE on the 15 retrieved records, and the cell collapses

14 rows (15 records; C2F1346 and C2F1212 are one study). **Nine of the fifteen changed cell or
status at full text.** The screen's own rubric said `design` values are hypotheses; this is the size
of the correction.

**The identified evidence is two studies, not nineteen.**

| record | design | outcome | effect |
|---|---|---|---|
| **C2F0428** Meng et al. | within-subject experiment + **city DID on ACTUAL births** | intended **and realized** | ban raises expected fertility **7-8%**; higher-intensity cities show greater actual birth increases; **perceived competition is the primary channel**, ahead of money and time |
| **C2F0592** Kim, *J Pop Econ* | **FE-IV**, instrument = provincial composition of parents with school-age children | **realized TFR** | 1% higher shadow-education spend → **TFR −0.18 to −0.26%**, stronger at higher parities |

Both are `return_separated = YES` or near it, both are on the education-competition arm, and both
support the hypothesis.

**The dispersion arm's identified estimates run AGAINST it — and that is the finding of the day.**

- **C2F0357** (2SLS, individual relative deprivation): income inequality **BOOSTS** fertility
  intentions. Channels: "build hopes on children", "allocate more time to families", and **"put less
  value on children's education"**.
- **C2F1346/1212** (Meng & Xie, IV, CFPS): inequality **AMPLIFIES** fertility; mediator is that
  higher inequality **lowers** educational aspirations, cutting the anticipated cost of children.

Both are the reverse of C.2.f's mechanism: inequality reduces required investment rather than
raising it. The two supporting dispersion records (C2F1217, C2F1264) are FE-only and their own
authors call them associations.

**So the sign splits cleanly by exposure**, exactly as §3's diagnostic predicted: measured as
**required educational investment** the mechanism works; measured as **income inequality** it
reverses. That is a chapter-defining result and it is not a wash — it says the general term §3
measured at 89% of the frame is not measuring this mechanism.

**C2F1348 (Kim, *The Race for Elite Destinations*) is the most decision-relevant record for the
verdict even though it is a model.** It formalises the assignment externality exactly as C.2.f
describes it — families spend 9% of lifetime income on education with near-zero measured returns,
and a capacity-preserving lottery would raise completed fertility by **0.24 children per couple**.
And its own cohort decomposition concludes: **"Preference shifts, not a fiercer race, explain the
decline across cohorts."** The strongest formal statement of the mechanism says the mechanism did
not drive the historical decline.

**Re-cellings worth naming.**

- **C2F0259 was the gender homonym.** "Relative status of women" means status relative to MEN, which
  is D.2.a's estimand, not position in the income distribution. Scope §8 Wall 10 measured that cloud
  at 30 records and predicted it would arrive; it arrived in the primary cell.
- **C2F1327 and C2F0593** are unidentified associations, so a **new cell `EDUCOMP_ASSOCIATION`** was
  added at extraction — the rubric had `INEQ_ASSOCIATION` only for inequality exposures
  (`add-a-cell-when-the-rubric-lacks-one`). C2F0593 is notable anyway: it names the mechanism in its
  own title (地位外部性, status externality).
- **C2F1343** (CSU dissertation) identifies peer effects in shadow-education *spending* with PSM/AIPW
  — but the fertility chapter is a model. Link 1 only.
- **C2F0066** (Johansson 1987, PDR) and **C2F0850** (Korean policy essay) carry no estimation.

**Pooling implication:** the ≥3 test now fails on every stratum. Two identified estimates with
different outcome levels, different exposures and different countries do not pool
(`stratify-before-counting-poolable`). This chapter is a narrative synthesis, not a meta-analysis.

Next: risk of bias (stage 8), then the demsig section — where C2F0592's elasticity and C2F1348's
0.24-children counterfactual are the two numbers that can carry it.

### 2026-09-08 — risk of bias (9) and demographic significance (3 routes)

**Risk of bias: 2 MODERATE, 7 HIGH.** The domains are this chapter's walls made into rateable
fields, and one result dominates:

> **D2 — is the RETURN separated from the REFERENCE STANDARD — is LOW in exactly ONE of nine
> studies.** C2F0428, the tutoring ban. Every other study is HIGH.

That is Wall 1 measured rather than asserted: **only one study in the chapter can distinguish C.2.f
from C.3.d.** Scope §2 said this wall decides the chapter, and it does.

The other binding domain is D5 (reference-group composition), HIGH in five. C2F1279 fails it on its
own terms: it instruments own shadow-education spending with **county peer spending**, which assumes
county-level competition affects fertility *only* through own spending — but that competition is
precisely the reference standard this chapter says is the mechanism.

**Demographic significance — `source/analysis/c2f_demographic_significance.py`, table generated not
retyped** (`generate-result-tables-never-retype`; A.17's hand-typed demsig had right offsets and
wrong baselines).

| route | result |
|---|---|
| **R2 elasticity** — C2F0592's identified −0.18/−0.26% per 1%, applied to Korea's +31% real private-education spend 2007–23 against an observed TFR fall of 1.26 → 0.72 | **11–16%** of the decline |
| **R3 counterfactual** — C2F1348's lottery raising completed fertility 0.24 children, against Korea's 2.82 → 0.75 post-1980 fall | **12%** |
| **R1 sign** — scripts 331–333 | wrong sign in **8 of 21** SDT-core countries; the exposure moved the wrong way through most of the decline |

**Two independent routes converge on roughly an eighth of Korea's fertility decline.** They share no
data and no method — one is an FE-IV elasticity on provincial spending, the other a calibrated
assignment-externality model. Convergence at 11–16% and 12% is worth more than either alone, though
some of the closeness is luck given R2's inputs.

**The weakest link is named rather than buried:** Korea's private-education spending growth is
hand-entered from KOSIS and is the only unautomated number in the computation. It must be replaced
by a machine-read pull before sign-off. R2 also transports a *provincial* elasticity to a *national*
time series — same country, different variation.

**The shape of the verdict is now clear, and it is not the registered hypothesis.** What survives is
the education-competition arm in East Asia, worth ~12% of Korea's decline, resting on **one**
study that clears Wall 1. What fails is the exposure the registry actually names: measured as income
inequality the sign reverses in two identified studies and is wrong in 38% of the SDT core.

Next: GRADE (stage 11) and the chapter draft (12). The GRADE rating has to carry that split — this
is not one body of evidence with a single certainty level.

