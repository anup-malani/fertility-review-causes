# TICK-099: C.2.e Female Wage and Opportunity Cost of Time
**Status:** in-progress
**Assigned:** Shravan
**Hypothesis:** `female-wage-opportunity-cost` — HYPOTHESES-v5.md §C.2.e
**Parallel-safe:** yes
**Blocks:** none
**Blocked by:** none
**Touches:** literature/search-logs/female-wage-opportunity-cost-*, extraction/female-wage-opportunity-cost-*, output/chapters/female-wage-opportunity-cost.md, source/build/goldset/

## Acceptance criteria
- [ ] 2. Search strategy and scope drafted — `literature/search-logs/female-wage-opportunity-cost-search-scope.md`
- [ ] 3. Literature search and AI screening — on-branch frame probe + completeness test (give C.2.e its OWN analogous treatment terms this time) + housing control; anchors resolved live → pool → blinded Haiku screen
- [ ] 4. RA title/abstract review — HUMAN GATE (abstract-less UNCERTAIN)
- [ ] 5. Full-text retrieval — OA subset read now; paywalled canon → RA proxy wantlist
- [ ] 6. Full-text screen — OA subset read in full; RA spot-check owed
- [ ] 7. Extraction — `extraction/female-wage-opportunity-cost.csv`; RA 10% verify owed
- [ ] 8. Risk-of-bias — `extraction/female-wage-opportunity-cost-risk-of-bias.csv`
- [ ] 9. Narrative synthesis
- [ ] 10. Demographic significance — PM/FDT/SDT per registry
- [ ] 11. GRADE first pass — 3-rater panel = HUMAN GATE
- [ ] 12. Chapter first draft — `output/chapters/female-wage-opportunity-cost.md`
- [ ] 13. RA lay-readability check — HUMAN GATE
- [ ] 14. PI review and sign-off — HUMAN GATE

## Log

**Selection rationale (2026-10-10).** C.2.e is the next-smallest genuinely-unstarted hypothesis once
C.1.a (TICK-098, income effect ~1,620) is consumed. The honest, completeness-tested ranking established
in TICK-098's pre-claim selection probe is:

| code | slug | narrow scout | honest (completeness-tested) |
|---|---|---|---|
| ~~C.1.a~~ | ~~income-effect-normal-good~~ | ~~1,620~~ | **consumed (TICK-098)** |
| **C.2.e** | female-wage-opportunity-cost | 1,259 (scout UNDERCOUNT) | **~2,035** |
| C.4.a | land-and-resource-constraints-malthusian | 893 | ~2,400 (jumps once "real wages" added) |
| B.2 | endocrine-disruptors | 4,465 | (the stale prior) |

The TICK-098 probe already ran the registered-construct completeness test on C.2.e and found the scout's
narrow 1,259 UNDERCOUNTED it: the scout union used only 4 terms and omitted plain synonyms of C.2.e's own
registered constructs ("women's employment", "female labor supply", "female wages"). Adding only those
synonyms takes the frame to ~1,863; "+maternal employment" (+172) and "+substitution effect" (+92) take
the honest frame to ~2,035. So C.2.e is next-smallest after C.1.a. Genuinely unstarted: no `NNN-*` branch,
no `output/chapters/female-wage-opportunity-cost.md`, no prior ticket (verified against `git branch -a`
and `git log --all`, not the board). Note: `main` HEAD is "Open TICK-098" — TICK-098's work lives on its
unmerged branch (the standing merge debt); the true next free number is 099.

**Estimand.** The effect of *exogenous variation in the female (maternal) wage or the opportunity cost of
women's time*, holding non-labor income constant, on *fertility* — i.e. the **substitution effect** of a
rising price of the mother's time. The parameter is the fertility response to a wage/earnings/labor-demand
shock that raises the price of child-rearing time (minimum-wage changes, trade/labor-demand shocks,
occupation- or sector-specific wage shifts, returns to schooling, gender-wage-gap closure). Phenomena FDT,
SDT (per registry — C.2.e does not claim PM).

**This hypothesis is a candidate CAUSE of decline (unlike C.1.a).** The standard Becker/Mincer/Willis
account: as women's wages rise, every hour of childcare forgoes more earnings; the substitution effect
raises the effective price of children and, if it dominates the (positive) income effect, net fertility
falls. This is THE workhorse economic explanation for the FDT/SDT decline. The chapter's job is to
establish whether the pure price-of-time (substitution) effect is (a) correctly signed (negative), (b)
causally identified off a wage shock that is not merely an income shock, and (c) large enough to carry a
demographically significant share of the decline.

**LOAD-BEARING walls (read from both sides at Stage 3):**
- **C.1.a Income Effect / Normal Good (drafted, TICK-098) — THE wall, read from the other side.** A wage
  change moves income AND the price of time together. C.2.e owns ONLY the price-of-time (substitution)
  channel with non-labor income held constant; C.1.a owns the pure income (wealth) channel. A study whose
  shock is a *non-labor* income/wealth shock (lottery, transfer, housing wealth) routes to C.1.a. C.2.e
  needs a shock to the *wage rate / price of time*. This is the wall the hypothesis is defined against.
- **D.2.a Female Empowerment / Autonomy (branch 062-ish ideational channel).** C.2.e is the *economic*
  (labor-market price) channel of rising female status; D.2.a is the *ideational/autonomy/norm* channel.
  A study identifying off norms/attitudes/empowerment rather than the wage → D.2.a.
- **C.2.h Digital Leisure Substitution (drafted/queued).** Also a substitution effect, but toward leisure
  consumption (lower price of non-child leisure goods), not toward labor income. Route device/leisure
  shocks → C.2.h.
- **FLFP as OUTCOME vs TREATMENT.** Female labor-force participation is frequently the *outcome* of
  fertility (reverse) or jointly determined; C.2.e needs the wage/price-of-time as the *exogenous driver*
  of fertility. Simple FLFP–fertility correlations without a wage shock are the mechanical/reverse cell.
- **The "economic development / GDP → fertility" macro bundle — EXCLUDED inflater** (same as C.1.a):
  bundles mortality decline, schooling, urbanization. Screen-routing signal only, never base recall.

**Caveat carried into Stage 3 (the A.6/A.3 lesson, and the specific C.1.a-vs-C.2.e apples-to-apples note).**
The on-branch frame probe must (a) re-run the registered-construct completeness test giving C.2.e its OWN
analogous treatment/identification terms (minimum wage, trade shock, returns to schooling, gender wage
gap) — the terms the C.1.a probe deliberately withheld from C.2.e to keep the *ranking* comparison honest
— and (b) confirm the selecting frame includes every registered construct (female wage, opportunity cost
of time, female labor force participation, substitution effect, price of time, women's employment) while
the development/income/empowerment OR-inflaters stay out of base recall; (c) reproduce the housing control
at ~162 on the identical reduced outcome axis.
