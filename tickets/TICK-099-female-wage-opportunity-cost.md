# TICK-099: C.2.e Female Wage and Opportunity Cost of Time
**Status:** in-progress
**Assigned:** Shravan
**Hypothesis:** `female-wage-opportunity-cost` — HYPOTHESES-v5.md §C.2.e
**Parallel-safe:** yes
**Blocks:** none
**Blocked by:** none
**Touches:** literature/search-logs/female-wage-opportunity-cost-*, extraction/female-wage-opportunity-cost-*, output/chapters/female-wage-opportunity-cost.md, source/build/goldset/

## Acceptance criteria
- [x] 2. Search strategy and scope drafted — `literature/search-logs/female-wage-opportunity-cost-search-scope.md` (2026-10-10)
- [x] 3. Literature search and AI screening — on-branch frame probe + completeness build-up (every registered construct adds coverage; housing control 162; production frame 2,557 / ranking ~1,924) → pool 1,445 (10/15 anchors live, 712 OA) → blinded Haiku screen, 25 batches (999 abstracts; 38 in-scope, 20 OA; walls: 41→C.1.a, 87→REVERSE, 32→DEV, 28→D.2.a)
- [ ] 4. RA title/abstract review — HUMAN GATE (446 abstract-less UNCERTAIN)
- [~] 5. Full-text retrieval — 12/38 read (OA subset; 1 retrieval-failed → RA wantlist); paywalled/blocked canon on `female-wage-opportunity-cost-missing-pdf-dois.csv` (RA proxy). Per precedent, chapter written on the OA subset
- [x] 6. Full-text screen — 12 read (11 with data); RA 5–10% spot-check owed
- [x] 7. Extraction — `extraction/female-wage-opportunity-cost.csv` (12 records, 10 usable estimates); RA 10% verify owed (priority: 3 working-paper-substitute texts)
- [x] 8. Risk-of-bias — `extraction/female-wage-opportunity-cost-risk-of-bias.csv`
- [x] 9. Narrative synthesis (no homogeneous poolable set — different shocks/outcomes/margins and estimates disagree in sign)
- [x] 10. Demographic significance — PM NOT ASSESSED (out of registry scope; one income-dominated calibration); FDT potentially MAJOR but NOT ESTABLISHED (MODERATE on clean evidence); SDT potentially MAJOR but NOT ESTABLISHED (best-identified designs income-dominated)
- [x] 11. GRADE first pass — PM No evidence, FDT VERY LOW, SDT LOW; 3-rater panel = HUMAN GATE
- [x] 12. Chapter first draft — `output/chapters/female-wage-opportunity-cost.md`
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

**INTERIM CHAPTER DRAFTED 2026-10-10.** Full pipeline run end-to-end: scope → on-branch frame probe +
completeness build-up (201; housing control 162; production frame 2,557, every registered construct adds
coverage — women's employment +347, female labor supply +212, maternal employment +175 — confirming the
scout's narrow 1,259 undercount) → 15 anchors (10 resolved live, 5 carried for RA) → pool 1,445 (202) →
blinded Haiku screen, 25 batches of 40 (203; 999 abstracts, 38 in-scope/20 OA; 446 abstract-less → RA
gate) → 12 OA full texts read by parallel Sonnet extraction agents → extraction + RoB + chapter (204).
Per the standing PI instruction, written on the OA subset (12/38).

**HEADLINE:** C.2.e is the workhorse economic explanation for the FDT/SDT decline and has the *right sign*
(rising price of women's time → fewer children), with first-order macro covariation (female wages/FLFP
track falling TFR). But the clean micro evidence that the *pure* substitution effect — net of the income
effect it is entangled with and net of the selection of lower-fertility women into work — is large and
negative is thin and internally contradictory. The single cleanest design, the **Ethiopia factory-job
RCT** (Kotsadam–Pieters–Villanger 2025, 1,464 married applicants, 9-yr follow-up), finds female employment
**RAISES** completed fertility (+5% births, +15 pp motherhood): the income effect wins. The Norwegian
earnings panels agree (own earnings → +first birth, both sexes). The trade shocks that look negative run
through **men's** income (Giuntella 2022; the ADH 2019 headline) → route to C.1.a. The studies that keep
the textbook negative sign (Rondinelli Italy, first-birth hazard −0.344 on an *imputed* wage; Bullinger US
minimum wage ≈ −2%/\$1) do **not** hold income constant. The one clean price-of-time signal is ADH's
female-intensive coefficient (+2.51/1,000 — fertility rises as women's labour demand falls), but it is
weak and collinear (ρ=0.80) with the male shock. C.2.e and C.1.a are two readings of ONE confounded
wage–income gradient; when a coin flip finally separates them (Ethiopia), the **income** effect is what
moves. **VERDICT: PM NOT ASSESSED (out of registry scope; Voigtländer–Voth EMP is an income-dominated
calibration) · FDT & SDT potentially MAJOR but NOT ESTABLISHED (MODERATE at most on clean evidence — macro
covariation real, pure substitution effect weakly/mixed-identified); GRADE PM No evidence / FDT VERY LOW /
SDT LOW.**

**Routing worked hard and correctly:** 41→C.1.a (income wall from the other side), 87→REVERSE (child/
motherhood penalty), 32→DEV bundle, 28→D.2.a (empowerment). Two studies that *passed* the title/abstract
screen into C.2.e re-routed to C.1.a on full read (shock hit men's income). Three PDFs read from
working-paper substitutes (Cloudflare/captcha blocked the version of record); numbers flagged. No numbers
fabricated.

**NOW AT HUMAN GATES:** (4) RA title/abstract review of 446 abstract-less UNCERTAIN; (5) RA proxy/ILL of the
blocked canon — esp. Van den Broeck (Senegal export employment, retrieval failed), Schultz 1985 (the
historical FDT test), Butz–Ward 1979, Mincer 1963, Bullinger full text, Jensen 2012, Heath–Mobarak 2015 —
see `female-wage-opportunity-cost-missing-pdf-dois.csv`; (6) RA screen spot-check; (7) RA 10% extraction
verify (priority: the 3 working-paper-substitute texts); (11) 3-rater GRADE panel; (13) RA lay-readability;
(14) PI review + the §11 calls. The FDT/SDT verdict could move up toward MAJOR if the clean female-labour-
demand canon on the wantlist holds income fixed and finds the substitution effect dominating.
