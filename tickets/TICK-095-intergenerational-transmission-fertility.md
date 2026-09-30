# TICK-095: A.19 Intergenerational Transmission of Fertility Preferences
**Status:** open
**Assigned:** Shravan
**Hypothesis:** `intergenerational-transmission-fertility` — HYPOTHESES-v5.md §A.19
**Parallel-safe:** yes
**Blocks:** none
**Blocked by:** none
**Touches:** literature/search-logs/intergenerational-transmission-fertility-*, extraction/intergenerational-transmission-fertility-*, output/chapters/intergenerational-transmission-fertility.md

## Acceptance criteria
- [ ] 2. Search strategy and scope drafted — `literature/search-logs/intergenerational-transmission-fertility-search-scope.md`
- [ ] 3. Literature search and AI screening, both phases (§5.1)
- [ ] 4. RA title/abstract review
- [ ] 5. Full-text retrieval
- [ ] 6. Full-text screen
- [ ] 7. Extraction
- [ ] 8. Risk-of-bias
- [ ] 9. Meta-analysis if ≥3 extractable effects, narrative synthesis otherwise
- [ ] 10. Demographic significance against PM / FDT / SDT
- [ ] 11. GRADE rating, 3 independent raters
- [ ] 12. Chapter first draft
- [ ] 13. RA lay-readability check
- [ ] 14. PI review and sign-off

## Log

**Selection rationale (2026-09-30).** Picked as the next-smallest genuinely-unstarted hypothesis by
measured frame, taken directly per the standing rule that the fresh cross-field scout is skipped once
the current scout's ranking still holds. The board's "Open" list is stale — candidates 086–094 all have
live branches with commits and unique chapters (verified against `git branch`, not the board). A.19 is
genuinely unstarted: no `NNN-*` branch, no `output/chapters/intergenerational-transmission-fertility.md`,
no prior ticket. TICK-092/093/094's extended cultural/demographic scout ranked the remaining unstarted
candidates D.2.c 1,134 (→092), D.1.d 1,720 (→093), A.20 ~1,968 (→094), then **A.19 2,414**, B.2 4,475.
With A.20 claimed, **A.19 is the next-smallest** and B.2 (endocrine disruptors) follows.

**Estimand.** The effect of *parental fertility preferences / family-size norms* on *offspring realized
and desired fertility*, net of shared genes and shared environment. The parameter is the vertical
(parent→child) transmission coefficient — the persistence channel — not the parent-offspring fertility
*correlation* as such, which is confounded. Fernandez–Fogli's epidemiological (immigrant) design is the
identification workhorse: it isolates the cultural component by holding the institutional/market
environment fixed across ancestry groups. Seminal: Murphy 1999, Murphy & Knudsen 2002, Kolk 2014,
Fernandez & Fogli 2009. Phenomena PM/FDT/SDT.

**Caveat carried into stages 2–3 (the A.6/A.3 lesson).** Stage 3 must run the full frame probe +
registered-construct completeness test before the "smallest" claim (2,414) is trusted — confirm the
*selecting* frame includes the registry's own constructs (intergenerational transmission, persistence /
slow convergence, the epidemiological/immigrant approach, culture vs environment) and that no
load-bearing construct is omitted in a way that would move the count, as omitting "legitimation"
unseated A.6 (`404`) and the completeness test hardened A.20.

**LOAD-BEARING walls (read from both sides before trusting the frame):**
- **A.18 Genetic and Heritable Variation in Fertility (TICK-076, drafted).** THE central wall. A raw
  parent-offspring fertility correlation (e.g. much of the Kolk 2014 realized-fertility literature) is
  equally consistent with genetic heritability. A.19 owns the *cultural transmission of preferences*
  net of genes; A.18 owns the genetic component. The identification split is exactly what the
  epidemiological design buys — studies that cannot separate the two route to a shared boundary, not
  into A.19's identified core.
- **A.20 Cultural Diffusion Mechanisms (TICK-094) / A.3 Diffusion of Fertility Control (TICK-088).**
  *Vertical* (parent→child, across generations) vs *horizontal* (peer/network/media, within a cohort)
  transmission. A.19 owns the vertical channel; A.20/A.3 own horizontal spread. Social-network and
  intergenerational-mobility papers straddle the line and must be routed on which channel carries the
  effect.
- **D (all cultural root-cause entries).** Transmission preserves whatever norm is current — A.19
  explains *persistence and slow adjustment*, not the *direction* of change. It must not absorb the
  root-cause content (secularization, individualism, gender norms). The wall is: does the study
  identify transmission of a preference, or the emergence/change of the preference itself?
- **REVERSE / mechanical cell.** Parent-offspring parity correlation driven by shared environment
  (region, income, religion co-residence) rather than preference transmission; and reverse pathways
  where offspring outcomes reshape reported parental norms. Both belong outside the identified core.
