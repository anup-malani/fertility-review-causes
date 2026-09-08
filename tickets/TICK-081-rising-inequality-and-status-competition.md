# TICK-081: C.2.f Inequality and Status Competition in Child Investment
**Status:** in-progress
**Assigned:** Shravan
**Hypothesis:** `rising-inequality-and-status-competition` — HYPOTHESES-v5.md §C.2.f
**Parallel-safe:** yes
**Blocks:** none
**Blocked by:** none
**Touches:** literature/search-logs/rising-inequality-and-status-competition-*, extraction/rising-inequality-and-status-competition-*, output/chapters/rising-inequality-and-status-competition.md, source/build/goldset/32[89]*, source/build/goldset/33*

## Acceptance criteria
- [ ] 2. Search strategy and scope drafted
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

