# TICK-098: C.1.a Income Effect on Fertility
**Status:** open
**Assigned:** Shravan
**Hypothesis:** `income-effect-normal-good` — HYPOTHESES-v5.md §C.1.a
**Parallel-safe:** yes
**Blocks:** none
**Blocked by:** none
**Touches:** literature/search-logs/income-effect-normal-good-*, extraction/income-effect-normal-good-*, output/chapters/income-effect-normal-good.md, source/build/goldset/

## Acceptance criteria
- [ ] 2. Search strategy and scope drafted
- [ ] 3. Literature search and AI screening, both phases (§5.1)
- [ ] 4. RA title/abstract review
- [ ] 5. Full-text retrieval
- [ ] 6. Full-text screen, RA spot-checks 5–10%
- [ ] 7. Extraction to `extraction/income-effect-normal-good.csv`, RA verifies a random 10%
- [ ] 8. Risk-of-bias assessment per study
- [ ] 9. Meta-analysis if ≥3 extractable effects, narrative synthesis otherwise
- [ ] 10. Demographic significance against PM / FDT / SDT
- [ ] 11. GRADE rating, 3 independent raters
- [ ] 12. Chapter draft on the §6 template
- [ ] 13. RA lay-readability check
- [ ] 14. PI review and sign-off

## Log

**Selection rationale (2026-10-09) — the ranking FLIPPED under the completeness test; this is the
A.6/A.3 lesson caught *before* a claim, not after.** C.1.a was NOT the apparent next pick. The fresh
2026-10-08 cross-field scout (run for TICK-097, cache `temp/next-candidate-scout-cache-2026-10-08.json`)
left this narrow ranking of genuinely-unstarted candidates after D.1.c was consumed:

| code | slug | narrow frame | honest frame (completeness-tested) |
|---|---|---|---|
| C.4.a | land-and-resource-constraints-malthusian | 893 | ~2,400 (jumps once "real wages" added — logged in TICK-097) |
| **C.2.e** | female-wage-opportunity-cost | **1,259** | **~1,863–2,035** (scout UNDERCOUNTED) |
| **C.1.a** | income-effect-normal-good | **1,620** | **~1,620–1,680** (near-complete; robust) |
| B.2 | endocrine-disruptors | 4,465 | (the stale prior) |

By narrow frame C.2.e (1,259) looked smaller than C.1.a (1,620), so the naive pick was C.2.e. A
selection-hardening probe (`temp/.../c2e_select_probe.py`, cache in scratchpad; identical outcome axis to
`100_d1c_frame_probe.py`, housing control reproduced at 162) ran the registered-construct completeness
test on BOTH and flipped the order:

- **C.2.e is undercounted by the scout.** The scout union used only 4 terms; it omitted plain synonyms of
  C.2.e's *own* registered constructs — "women's employment", "female labor supply", "female wages".
  Adding only those synonyms (no neighbour inflater) takes the frame to **1,863**; "+maternal employment"
  (+172) and "+substitution effect" (+92) take the honest frame to **~2,035**. This is the exact A.6/A.3
  failure mode (a registered noun missing from the selecting frame).
- **C.1.a is near-complete and robust at ~1,620.** Every genuine construct adds ≤24 (permanent income
  +24, wealth effect +24, normal good +15, income elasticity of fertility +0). The large gains are all
  free-OR inflaters that annex the development literature and are correctly EXCLUDED: "economic
  development" +4,364, "living standards" +913, "GDP per capita" +613 (these bundle mortality decline,
  schooling, structural change — not the pure income/normal-good channel).

Honest ranking is therefore **C.1.a ~1,620 < C.2.e ~2,035 < C.4.a ~2,400 < B.2 4,465**, so C.1.a is the
next-smallest genuinely-unstarted hypothesis. Genuinely unstarted: no `NNN-*` branch, no
`output/chapters/income-effect-normal-good.md`, no prior ticket (verified against `git branch -a` and
`git log --all`, not the board). Note: the main-branch QUEUE banner read "TICK-097" (stale — 097's board
move lives on its unmerged branch); the true next free number was 098.

**Estimand.** The effect of *exogenous variation in household income or wealth, holding prices and the
price of time (wages) constant,* on *fertility* — i.e. the sign and magnitude of the **pure income
effect**, testing whether children are a *normal good*. The parameter is the income elasticity of
fertility identified off an income/wealth shock that is NOT also a wage/price-of-time shock (cash
transfers, UBI/negative income tax, lottery wins, resource/commodity windfalls, inheritances, EITC
income component). Phenomena PM, FDT, SDT (per registry).

**This hypothesis is the counterfactual, not a candidate cause of decline.** C.1.a is the baseline
Beckerian prediction (income ↑ → fertility ↑ if children are normal) whose *secular failure* is the
puzzle every other economic chapter addresses. Clark 2007 documents the income effect *dominating* in
pre-industrial England (positive gradient, PM). In the FDT/SDT era the cross-sectional gradient turns
negative, which the registry attributes to the cost/value channels (C.2, C.3) overwhelming a
positive-but-small pure income effect. So the chapter's job is unusual: establish the SIGN and size of
the *pure* income effect once the substitution/relative/uncertainty channels are netted out, and read
the demographic-significance verdict as "does the normal-good mechanism survive as a positive force,
and is it large enough to matter against the cost channels." Expect the headline to be that the raw
income–fertility gradient is confounded and the clean (transfer/windfall) estimates are small and often
near zero or mildly positive.

**LOAD-BEARING walls (read from both sides at Stage 3):**
- **C.2.e Female Wage / Opportunity Cost of Time — THE wall.** A wage change moves income AND the price
  of time together; C.1.a owns ONLY the income (wealth) channel with the price of time held constant.
  Any study whose shock is a wage/earnings change routes to C.2.e. C.1.a needs a non-labor income/wealth
  shock. This is the wall the whole hypothesis is defined against (its registry claim says so).
- **C.6.a Easterlin Relative Income (drafted, TICK-078).** C.1.a is *absolute* income (normal good);
  Easterlin is *relative*/cohort income and predicts oscillation, not a level. A study identifying off
  relative income → C.6.a.
- **C.5.a Economic Uncertainty / C.3.e Credit Constraints (drafted) / C.3.g Student Debt (drafted).**
  These move resources through risk, liquidity, or debt, not a permanent-income normal-good effect.
- **The "economic development → fertility" macro bundle — the inflater, EXCLUDED.** The probe shows
  "economic development" adds +4,364; that literature bundles mortality decline, schooling, urbanization,
  and women's wages. It is NOT the pure income effect and must stay out of the recall frame (screen-
  routing signal only).
- **REVERSE / mechanical cell.** Fertility affecting household income (children → lower maternal labor
  supply → lower income) is the reverse-causality cell, outside the core.

**Caveat carried into Stage 3 (the A.6/A.3 lesson).** Even though the selection probe already ran the
completeness test and C.1.a was robust at ~1,620, Stage 3 must still re-run the full frame probe +
completeness test + housing control on the branch, formalized as a `source/build/goldset/NNN_c1a_frame_probe.py`
artifact, and confirm the selecting frame includes every registered construct (income effect, household
income, income elasticity, permanent income, wealth effect, normal good) while the development/wage/
relative-income OR-inflaters stay out of base recall. Selection-probe artifacts to port onto the branch:
`c2e_select_probe.py` + `c2e-select-cache.json` (session scratchpad).
