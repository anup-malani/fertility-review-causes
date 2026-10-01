# TICK-096: A.13 Breastfeeding and Lactational Amenorrhea
**Status:** in-progress
**Assigned:** Shravan
**Hypothesis:** `breastfeeding-lactational-amenorrhea` — HYPOTHESES-v5.md §A.13
**Parallel-safe:** yes
**Blocks:** none
**Blocked by:** none
**Touches:** literature/search-logs/breastfeeding-lactational-amenorrhea-*, extraction/breastfeeding-lactational-amenorrhea-*, output/chapters/breastfeeding-lactational-amenorrhea.md

## Acceptance criteria
- [ ] 2. Search strategy and scope drafted
- [ ] 3. Literature search and AI screening, both phases (§5.1)
- [ ] 4. RA title/abstract review
- [ ] 5. Full-text retrieval
- [ ] 6. Full-text screen, RA spot-checks 5–10%
- [ ] 7. Extraction to `extraction/breastfeeding-lactational-amenorrhea.csv`, RA verifies a random 10%
- [ ] 8. Risk-of-bias assessment per study
- [ ] 9. Meta-analysis if ≥3 extractable effects, narrative synthesis otherwise
- [ ] 10. Demographic significance against PM / FDT / SDT
- [ ] 11. GRADE rating, 3 independent raters
- [ ] 12. Chapter draft on the §6 template
- [ ] 13. RA lay-readability check
- [ ] 14. PI review and sign-off

## Log

**Selection rationale (2026-10-01).** Picked as the next-smallest genuinely-unstarted hypothesis.
A.13 is a **Bongaarts proximate determinant** — the postpartum-infecundability index (C_i) — and
therefore a direct sibling of A.14 Coital Frequency (TICK-091), whose frame probe measured **373**,
"an order of magnitude below the ~1,808 bar and below every other unstarted candidate." The bounded
biological proximate-determinant cluster (A.12 twinning, A.14 coital frequency, A.13 breastfeeding,
A.15 maternal age) is the smallest-frame family in the review; A.14's measured 373 anchors the
expectation that A.13's honest selecting frame is small and well-contained. A.13 is **not** in the
TICK-092/093/094 cross-field scout (that ranked the cultural/demographic candidates: D.2.c 1,134,
D.1.d 1,720, A.20 1,968, A.19 2,414, B.2 4,475); like A.14 it sits below that set.

The board's "Open" list is stale — verified against `git branch -r`, not the board. A.13 is genuinely
unstarted: no `NNN-*` branch, no `output/chapters/breastfeeding-lactational-amenorrhea.md`, no prior
ticket, no search logs.

**Estimand.** The effect of *breastfeeding intensity/duration* on fertility through the length of
postpartum lactational amenorrhea and anovulation — i.e. the contribution of nursing to birth
spacing and natural-fertility levels, isolated from deliberate contraception and from maternal
nutrition. The parameter is a *spacing/quantum* effect on the birth interval (the Bongaarts C_i
index), not a desired-family-size effect.

**Caveat carried into stages 2–3 (the A.6/A.3 lesson).** Stage 3 must run the full frame probe +
registered-construct completeness test before the "smallest" claim is trusted — confirm the
*selecting* frame includes the registry's own constructs (lactational amenorrhea, postpartum
infecundability/anovulation, birth spacing/interval, suckling intensity, the Bongaarts proximate-
determinants framework) and that no load-bearing construct is omitted in a way that would move the
count.

**LOAD-BEARING walls (set these in the stage-2 scope, read from both sides before trusting the frame):**
- **A.2 Modern Contraceptive Technology (drafted) / A.5 Family Planning.** Breastfeeding is
  *natural* child-spacing; the frame must not annex the enormous literature in which lactation is a
  covariate inside contraceptive-method or family-planning-program studies. Route studies on which
  mechanism carries the spacing effect (suckling-driven amenorrhea vs. method adoption, incl. LAM as a
  *contraceptive method* — a boundary case).
- **A.22 Nutrition and Energy Availability [DEPRECATED].** The maternal-nutrition→amenorrhea pathway
  (the critical-fat/energy-balance debate) overlaps lactational amenorrhea physiologically; A.13 owns
  the *suckling* channel, not the energy-availability channel. A.22 is deprecated, so guard against
  the frame silently absorbing the nutrition-fecundity literature.
- **Demographic-significance boundary.** A.13 is demographically load-bearing mainly in natural-
  fertility / pre-modern and LMIC settings; in contracepting FDT/SDT populations the C_i contribution
  is small and dominated by deliberate control. Stage 10 should expect PM-significant, FDT/SDT-minor.
- **REVERSE / mechanical cell.** Shorter intervals driven by early weaning that is itself a response
  to a new pregnancy or to desired closer spacing (reverse pathway); and the mechanical identity by
  which any birth-interval component moves period rates. Both belong outside the identified core.

**Standing checkpoint.** Stage 3 is the OpenAlex-heavy frame probe; per the standing "pause before the
OpenAlex spend" rule (405/52/A.20/A.19 precedent), stage 2 drafts the scope and then PAUSES for the
RA/PI go-ahead before the probe runs.
