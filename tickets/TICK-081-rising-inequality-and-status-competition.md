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
