# TICK-088: A.3 Diffusion and Social-Learning of Fertility Control
**Status:** parked 2026-09-17 — not pursued now. `405` showed A.3's corrected frame (1,584–2,419) is larger than A.6's (1,225), so A.6 resumed as the strict-smallest candidate under TICK-087. A.3 remains live and unstarted; `405` is complete and inheritable.
**Assigned:** Shravan
**Hypothesis:** `diffusion-of-fertility-control` — HYPOTHESES-v5.md §A.3
**Parallel-safe:** yes
**Blocks:** none
**Blocked by:** none
**Touches:** literature/search-logs/diffusion-of-fertility-control-*, extraction/diffusion-of-fertility-control-*, output/chapters/diffusion-of-fertility-control.md
**Selected by:** `candidate-frame-probe-2026-09-13` put A.3 second at a union frame of 727, behind A.6 at 680. `404` (TICK-087, branch `087-stigma-reduction-contraception-abortion`, commit `9857481`) then showed A.6's frame omits its own registered construct and corrects to 1,225, which makes A.3 the smallest bracketed candidate. A.3 re-measured at **719** against the recorded 727 on 2026-09-17, so the index is stable.
**Scope hazard — do this before anything else:** A.3 has not been tested for the defect that unseated A.6, and it has the same shape. A.3's registered claim says fertility control spreads via "linguistic, religious, and social networks" and by "information about and **legitimation** of birth control", yet the pass-4 block carries no form of *legitimation*, no *social network*, no *peer effect* and nothing linguistic or religious. Stage 2 therefore opens with a registered-construct completeness test (`405`), mirroring `404` blocks C and J. **If the corrected frame exceeds C.3.a's 1,808, A.3 is not the smallest either and the selection goes back to the board rather than forward into a search.**
**Second hazard:** A.3 shares two of four registered seminals with A.6 (Cleland and Wilson 1987; Bongaarts and Watkins 1996) while overlapping it on only 2 records of vocabulary — the C.3.d shape, where the vocabularies part and the construct does not. That wall is adjudicable only at full text, and A.3 is now the chapter written first, so it owns defining it. A.3 is also registered as *proximate*: per §A.3's own note it "describes the spread mechanism, not what is being spread or why people adopt it", so the §4 chain must say which link is this chapter's parameter and which belongs to D.1.a / D.1.b.

## Acceptance criteria
- [ ] 2. Search strategy and scope drafted
- [ ] 3. Literature search and AI screening, both phases (§5.1)
- [ ] 4. RA title/abstract review
- [ ] 5. Full-text retrieval
- [ ] 6. Full-text screen, RA spot-checks 5–10%
- [ ] 7. Extraction to `extraction/diffusion-of-fertility-control.csv`, RA verifies a random 10%
- [ ] 8. Risk-of-bias assessment per study
- [ ] 9. Meta-analysis if ≥3 extractable effects, narrative synthesis otherwise
- [ ] 10. Demographic significance against PM / FDT / SDT
- [ ] 11. GRADE rating, 3 independent raters
- [ ] 12. Chapter draft on the §6 template
- [ ] 13. RA lay-readability check
- [ ] 14. PI review and sign-off

## Log

**2026-09-17 — parked the same day it was opened, by its own opening measurement.**

*Result.* TICK-088 existed because `404` reported A.6 was not the smallest candidate. `405` ran the
completeness test this ticket was opened to run, and it reversed that: A.3 fails the test harder
than A.6 does. "legitimation" is in A.3's registered claim, absent from its pass-4 block, and worth
**+865 records alone** (719 → 1,584); all twelve of the terms A.3 genuinely owns give **2,419**, a
3.4× widening. Against A.6's corrected 1,225 the ordering is the reverse of what `404` concluded.

`404`'s defect was not the test but its application: it corrected one candidate and compared the
result against its comparator's *uncorrected* number. The probe's own warning — never rank a
corrected frame against an uncorrected one — was restated in `404`'s docstring and then broken in
its conclusion.

A.3 measurements worth inheriting when this reopens:

- **The A.20 wall is A.3's existence question.** A.20 (`cultural-diffusion-mechanisms`) absorbs
  `social-network-peer-effects`, `ideational-diffusion-mass-media` and
  `linguistic-cultural-boundaries-princeton`; both entries are registered *proximate*, both say
  "independent of" the underlying driver, and they share two seminals (Coale and Watkins 1986;
  Bongaarts and Watkins 1996). Overlap is 59 records — 8.2% of A.3's frame, 2.3% of A.20's 2,543 —
  with exactly **1** identified record in it. Annexing A.20's channel terms takes A.3 to 3,354, so
  the registry's thin A.3/A.20 distinction is load-bearing and needs a PI call before either is
  scoped.
- **The vocabulary is clean.** Homonym contamination inside the frame is 7 (machine learning /
  animal behaviour), 1 (physical sciences), 7 (biology), 8 (epidemic spread). A.3 does not have
  A.6's problem.
- **More of the registered outcome is present than in A.6.** 154 in-frame records carry
  realized-fertility vocabulary and 16 of 719 an identified-design marker (2.2%); the
  adoption-timing level is **0**.
- Other walls, ours/theirs: A.6 12 / 1.7% / 0.4%; D.1.a 33 / 4.6% / 2.4%; A.2 20 / 2.8% / 0.4%;
  A.19 11 / 1.5% / 1.8%; D.1.b 1 / 0.1% / 0.5%.

*Workflow impact.* `304` is unreliable as a ranking instrument until it (a) checks that each
candidate's registered claim's own nouns appear in its block, and (b) records conjunction depth, so
a three-block frame is never ranked against a two-block one. Two of two candidates tested failed
(a); A.6 was the only one that failed (b). C.3.a, D.2.c, C.2.e, C.4.a, A.19, A.4, C.2.d and C.1.a
are all still uncorrected, so the bracketed table's ordering should not be trusted. This is a `304`
change and `304` belongs to TICK-080.
