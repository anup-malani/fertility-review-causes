# TICK-065: B.5. Fetal Loss and Intrauterine Mortality
**Status:** in-progress
**Assigned:** Shravan
**Hypothesis:** `fetal-loss-intrauterine-mortality` — HYPOTHESES-v5.md §B.5
**Parallel-safe:** yes
**Blocks:** none
**Blocked by:** none
**Touches:** literature/search-logs/fetal-loss-intrauterine-mortality-*, extraction/fetal-loss-intrauterine-mortality-*, output/chapters/fetal-loss-intrauterine-mortality.md

## Acceptance criteria
- [x] 2. Search strategy and scope drafted
- [x] 3. Literature search and AI screening, both phases (§5.1)
- [ ] 4. RA title/abstract review
- [ ] 5. Full-text retrieval
- [ ] 6. Full-text screen, RA spot-checks 5–10%
- [ ] 7. Extraction to `extraction/fetal-loss-intrauterine-mortality.csv`, RA verifies a random 10%
- [ ] 8. Risk-of-bias assessment per study
- [x] 9. Meta-analysis if ≥3 extractable effects, narrative synthesis otherwise — narrative; no pooling, reasons in chapter §6
- [x] 10. Demographic significance against PM / FDT / SDT
- [~] 11. GRADE rating, 3 independent raters — rated, but by one analyst applying three lenses; independent re-rating open
- [x] 12. Chapter draft on the §6 template
- [ ] 13. RA lay-readability check
- [ ] 14. PI review and sign-off

## Log

### 2026-08-11 — Shravan

Ran the chapter end to end as far as the human gates allow. Stages 2, 3, 9, 10 and 12
are done; stage 11 is done with a stated deviation; stages 4-8, 13 and 14 are open and
four of them are blocked on PDF procurement, which is an RA gate under PROTOCOL §5.

**Result.** The chapter has a defensible finding and it is a quantitative one. B.5's
mechanism has an arithmetic form, births proportional to (1-p), that overstates its
effect on completed fertility by about 2.5x, because a fetal loss consumes a fraction
of a birth interval rather than a birth. Modelled on the Sheps-Menken/Bongaarts
interval decomposition, the pre-modern effect is +6.2% (95% interval +3.2% to +9.9%)
and the FDT effect is +4.5%, or +0.25 births per woman. The FDT sign is INVERTED:
falling intrauterine mortality pushed births up across a period when TFR halved, so
B.5 does not explain the first transition and instead implies its behavioural
component was about 10% larger than the raw series shows. That magnitude lands almost
exactly on PROTOCOL §4.2's 10% threshold, so the verdict is knife-edge and turns on
the historical early-loss rate, which is the model's least observed parameter.

The effect exists only where the reproductive span binds and vanishes under a binding
parity target, which is a testable prediction rather than a modelling convenience, and
the best-designed study located (Danish registry, 458,475 women, completed family size)
observes exactly the regime where the prediction says it should find nothing.

**Pipeline.** Scripts 115-120 plus `source/analysis/b5_demographic_significance.py`
(13 tests, all passing). 31 anchors sourced live, 25 verified through three gates;
citation frame 11,504 records; D1 rank bounding the screen to 392 of 11,125, with the
10,733 unscreened residual characterised rather than left implicit; screen gives 18
primary-cell records, 267 support-stream, 13 held.

**Workflow impact / future behaviour.**

1. The A3 resolver had three defects found only by reading its REFUSALS, not its
   acceptances. The worst: Crossref and OpenAlex use different `type` vocabularies
   (`journal-article` vs `article`) and the unmapped OpenAlex value fell to the "other"
   default, penalising every OpenAlex record by 90 points. Two anchors resolved to
   same-title impostors as a result. Any chapter mirroring 116 must port
   `canon_type()`. The other two: a missing author list ranked neutral (now a penalty,
   still not a rejection), and `-\d{1,3}$` matched an ISBN check digit.
2. The book-canon gate is confirmed necessary on a second, unrelated canon. For
   Leridon 1977, Sheps-Menken 1973 and Preston 1978 the review records credit the
   BOOKS' OWN AUTHORS, so the author gate passes and only the review-shape and
   fallback flags reject. Both defences needed; neither redundant.
3. **The citation frame recovers books the anchor resolver cannot.** Wood 1994,
   Leridon 1977, Bongaarts-Potter 1983 and the 1993 Biomedical and Demographic
   Determinants volume all failed A3 and all reappear in Tier B as cited works, correctly
   routed by the screen. Unresolved monograph anchors are therefore recoverable at A4
   and should be written back rather than treated as a permanent gap.
4. The D.2.d uniform forward-seed rule replicates here: 16% of the frame depends only
   on a decoy seed, and decoy clouds ran 68-75% on-topic against 70.5% for the theory
   canon.
5. **A scope call that outgrew the chapter.** B.5's predicted sign opposes the FDT it
   is assigned to, and PROTOCOL §4.2's significance test implicitly assumes a
   hypothesis pushes with the phenomenon. That is a protocol gap, not a B.5 quirk, and
   the ruling belongs in §4.2. Raised as Call 1.

**Open, in priority order:** RA gate signature on
`extraction/fetal-loss-intrauterine-mortality-ra-gate.csv` (31 rows); PDF procurement,
with the Moroccan intrauterine-mortality/fertility study and the *Journal of Health
Economics* conflict paper as the two highest-value retrievals; extraction and risk of
bias; independent GRADE re-rating; PI answers on Calls 1-4.

