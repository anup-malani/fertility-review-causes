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
- [ ] 3. Literature search and AI screening, both phases (§5.1)
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

