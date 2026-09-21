# TICK-090: C.2.h Digital Leisure Substitution
**Status:** in-progress
**Assigned:** Shravan
**Hypothesis:** `digital-leisure-substitution` — HYPOTHESES-v5.md §C.2.h
**Parallel-safe:** yes
**Blocks:** none
**Blocked by:** none
**Touches:** literature/search-logs/digital-leisure-substitution-*, extraction/digital-leisure-substitution-*, output/chapters/digital-leisure-substitution.md

<!-- No ## Description. The slug above is the specification (HYPOTHESES-v5.md §C.2.h). -->

## Acceptance criteria
- [x] 2. Search strategy and scope drafted — `literature/search-logs/digital-leisure-substitution-search-scope.md`
- [ ] 3. Literature search and AI screening, both phases (§5.1)
- [ ] 4. RA title/abstract review
- [ ] 5. Full-text retrieval
- [ ] 6. Full-text screen, RA spot-checks 5–10%
- [ ] 7. Extraction to `extraction/digital-leisure-substitution.csv`, RA verifies a random 10%
- [ ] 8. Risk-of-bias assessment per study
- [ ] 9. Meta-analysis if ≥3 extractable effects, narrative synthesis otherwise
- [ ] 10. Demographic significance against PM / FDT / SDT
- [ ] 11. GRADE rating, 3 independent raters
- [ ] 12. Chapter draft on the §6 template
- [ ] 13. RA lay-readability check
- [ ] 14. PI review and sign-off

## Log

**2026-09-21 — opened and Stage 2 (search strategy and scope) drafted.**

*Selection context.* Picked by RA (Shravan) as the smallest *genuinely-unstarted* hypothesis after an
audit found every "Open" hypothesis row on the board (A.3/088, A.6/087, C.2.f/081, C.3.d/083,
C.3.f/086) already carries substantial unpushed branch work — A.3 in particular is drafted through
stage 12 on branch `088` (pushed to origin 2026-09-21 to un-strand it). C.2.h has no branch, no
chapter, and no prior ticket. It is a NEW-v5, SDT-only hypothesis anchored on essentially one
identified design, so it is a reasoned smallest, not a measured one. **The frame probe + registered-
construct completeness test still owe (stage 3);** the "smallest" claim is provisional until they run.

*Result.* Stage 2 deliverable at `literature/search-logs/digital-leisure-substitution-search-scope.md`.
It states C.2.h's single parameter (effect of a fall in the price / rise in the absorptiveness of
digital leisure on fertility and its partnering/coital mediators, net of C.2.e wages, A.24 matching,
A.14 coital-frequency identity, D.1.a values, D.3.a clinical distress), five boundary walls, an
estimand-cell table with routing, three conjoined query blocks for §5.1, eligibility rules, and the
reverse-causality/common-trend identification cautions. Per the A.6/A.3 lesson it carries a
**registered-construct completeness check** confirming every noun the §C.2.h claim names is in the
topic block and none is priced as a free-standing `OR`.

*Anchor verified.* Primary seed existence-checked live: Myers & Hooper, "Is the iPhone Birth
Control?", NBER w35310 (2026), nber.org/papers/w35310 + SSRN 6897299 — AT&T 2007–2011 exclusive
iPhone-carrier instrument, 33–52% of the post-2007 GFR decline, with time-use corroboration of all
three registered sub-mechanisms (social displacement, pornography, lower sexual frequency). The
registry's "3G carrier rollout" gloss is imprecise and is corrected in the scope.

*Next (stage 3, heavy infrastructure).* Cold-start anchor build + existence-verify (mirror script
89), Tier-A/B citation frame (mirror 90), and the blinded LLM title/abstract screen (91–94). These
need OpenAlex/Crossref API access and LLM screen budget. Checkpoint with RA before spending it.
