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
- [~] 3. Literature search and AI screening, both phases (§5.1) — free seeds + anchors done
- [ ] 4. RA title/abstract review
- [ ] 5. Full-text retrieval
- [ ] 6. Full-text screen, RA spot-checks 5–10%
- [ ] 7. Extraction to `extraction/rising-inequality-and-status-competition.csv`, RA verifies a random 10%
- [ ] 8. Risk-of-bias assessment per study
- [ ] 9. Meta-analysis if ≥3 extractable effects, narrative synthesis otherwise
- [ ] 10. Demographic significance against PM / FDT / SDT
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

