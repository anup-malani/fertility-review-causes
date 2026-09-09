# TICK-083: C.3.d Quantity-Quality Tradeoff
**Status:** in-progress
**Assigned:** Shravan
**Hypothesis:** `quantity-quality-tradeoff` — HYPOTHESES-v5.md §C.3.d
**Parallel-safe:** yes
**Blocks:** none
**Blocked by:** none
**Touches:** literature/search-logs/quantity-quality-tradeoff-*, extraction/quantity-quality-tradeoff-*, output/chapters/quantity-quality-tradeoff.md, source/build/goldset/34[4-9]*, source/build/goldset/35*

## Acceptance criteria
- [ ] 2. Search strategy and scope drafted
- [ ] 3. Literature search and AI screening, both phases (§5.1)
- [ ] 4. RA title/abstract review
- [ ] 5. Full-text retrieval
- [ ] 6. Full-text screen, RA spot-checks 5–10%
- [ ] 7. Extraction to `extraction/quantity-quality-tradeoff.csv`, RA verifies a random 10%
- [ ] 8. Risk-of-bias assessment per study
- [ ] 9. Meta-analysis if ≥3 extractable effects, narrative synthesis otherwise
- [ ] 10. Demographic significance against PM / FDT / SDT
- [ ] 11. GRADE rating, 3 independent raters
- [ ] 12. Chapter draft on the §6 template
- [ ] 13. RA lay-readability check
- [ ] 14. PI review and sign-off

## Why this one now

**Not the smallest frame — the largest of the three finalists, and chosen anyway.** On the 2026-09-03
probe (`literature/search-logs/candidate-frame-probe-2026-09-03.md`, still only on the 078 branch)
the union frames of the finalists were C.2.b **587**, A.6 **675**, C.2.f **714**, A.3 **726**, C.3.d
**762**. C.2.b (TICK-079) and C.2.f (TICK-081) are both drafted. Of what is left the spread is A.6
675 → C.3.d 762, **13%**, and TICK-079 set the precedent that 15% is inside vocabulary noise. Size
does not decide this. The tiebreak does, and it runs three ways at once.

**A.6 and A.3 lose on inherited boundary debt, which is TICK-081's argument unchanged.** A.6's
stigma-specific axis returns **12** records against a 675 union and A.3's core is **26** of 726 — both
frames are almost entirely loose general-purpose vocabulary rather than an anchored literature. A.6 is
by construction the residual left after A.2, A.4 and A.5. Checked 2026-09-09: none of those three has
a branch on `origin`, so all remain unstarted and the diagnosis stands a second time.

**C.3.d's core is 567 of 762** — an anchored literature, the same signature that made C.2.f preferable
to A.6 a week ago.

**Both of C.3.d's walls are already written, by chapters that are already drafted.** C.2.b's scope
ruling 2 was deliberately drafted in a form C.3.d could inherit. C.2.f's ruling 1 states the split
directly: C.3.d owns variation in the *return* to child quality, C.2.f owns variation in the
*reference standard*. This chapter inherits both rather than re-litigating either.

**The decisive reason is that C.2.f's PI call 3 is a question about C.3.d that gets more expensive
every week it waits.** The C.2.f chapter (drafted 2026-09-08) found that **eight of its nine studies
cannot separate the return from the reference standard**, and asked whether the C.2.f/C.3.d boundary
is tenable at all — flagging explicitly that it is decidable *because C.3.d is unstarted*. Once
chapters exist on both sides of that wall, reopening it means rewriting both.

**No frame number goes in this ticket until the homonym check runs.** The 09-03 probe ran a homonym
check for C.2.b only, and TICK-081 opened with the same gap. "Quality" is a far larger and more
general word than "inequality" was, and C.2.f's own shape — a 690-record core against a 24-record
social-comparison sub-literature — is the signature of a frame carried by one general-purpose axis.
Per `anchored-vocabulary-has-own-homonym`, score each anchor term alone before trusting the block;
per `calibrate-the-outcome-axis-too`, the outcome axis needs the same treatment. Re-run `304_` first
so the numbers this chapter is scoped against are current rather than six days old and on a branch.

## Open rulings to freeze at stage 2

1. **C.3.d vs C.2.f, inherited but now under active challenge.** The registered split is return
   (C.3.d) vs reference standard (C.2.f). C.2.f measured that split and found only one of nine studies
   could honour it. Do not simply re-assert the wall: measure it on C.3.d's own pool the way C.2.f
   did, and if it fails from this side too, that is a finding about the registry, not about the
   search. C.2.f's PI call 3 is the place it lands.
2. **C.3.d vs C.2.b.** C.2.b owns the *price faced* for a child at fixed quality; C.3.d owns the
   *shadow price of quantity* induced by the return to quality. C.2.b's ruling 2 is the inheritable
   form. Name what happens to studies that measure total expenditure per child without decomposing
   it — that is C.2.b's estimand or neither's, and `read-the-mechanism-not-the-instrument-name`
   applies.
3. **The registry absorbs SBTC into this entry, and that decision needs operationalizing.** The notes
   say skill-biased technical change is "the technology shock that raises the return to human
   capital" — the same mechanism in another framing. Decide at stage 2 whether SBTC-exposure studies
   (routine-task displacement, computerization, trade shocks) that estimate fertility effects belong
   in the primary cell or are a separate arm. They will not share a vocabulary with the Becker
   literature, so this decides a whole search axis, not just a routing rule.
4. **The exposure is not one variable, and the QQ literature knows it.** Returns to schooling, family
   size shocks (twins, sibling sex composition), compulsory-schooling reforms and unified-growth
   calibrations are four different estimands wearing one name. `stratify-before-counting-poolable`
   applies at extraction, but the strata must be derivable from a required-tags list decided here.
   Note that the twin-instrument literature is A.12's exposure used as C.3.d's instrument — `A.12`
   is drafted, so check its pool before building one.
5. **The famous micro result runs against the hypothesis, and the macro literature is calibrated
   rather than estimated.** Black-Devereux-Salvanes 2005 finds little tradeoff; the registry says so
   itself. Galor-Weil and Galor-Moav are unified-growth calibrations, not identified estimates.
   Decide before searching how calibrated macro models are treated — `anchor-on-the-estimand-not-the-famous-design`
   says the celebrated designs may not measure the outcome at all, and on C.3.e that was exactly
   right.
6. **FDT *and* SDT, which is unusual here and doubles the demsig work.** Most recent chapters have
   been SDT-only. Per `three-demsig-routes-before-not-assessed`, name the live route for each
   phenomenon separately at stage 2. Returns-to-schooling series for the FDT window are thin and
   country-specific; say now what would make the FDT cell computable rather than discovering at
   stage 10 that it is not.

## Assets in hand before the cold start

- **Free seeds.** C.2.b, C.2.f, C.3.e, C.3.f, C.3.g, D.2.d and A.12 all plausibly routed
  QQ records into their own screen files. Port the free-seed harvester (`335_c2f_free_seeds.py`,
  the newest copy); `snowball-pools-omit-their-own-seeds` in reverse, and it costs nothing.
- **Shared libraries are canonical on `main` now.** `source/lib/textnorm.py` (TICK-074, merged
  2026-09-08) and `source/lib/openalex.py` (merged 2026-09-08). **Import them; do not copy a
  `norm()` or an OpenAlex client.** Note TICK-082 is open against `textnorm.norm()` — it does not
  strip HTML markup — so expect that defect rather than rediscovering it.
- **Anchor resolver.** Port from `336_c2f_cold_start_anchors.py`, the newest copy.
- **Script numbering.** Max across **every branch on origin** is 343, so C.3.d starts at **344**
  (`script-number-collision`: start above every branch, not above main).
- **Merge debt is a live hazard.** The frame probe (`304_`) and every script this ticket ports sit
  on unmerged branches. Note what gets ported and from where, or the next chapter re-derives it.

## Log
