# Search scope — Income Effect on Fertility (children as a normal good)

**Ticket:** TICK-098
**Hypothesis slug:** `income-effect-normal-good`
**Registry:** HYPOTHESES-v5.md §C.1.a
**Target phenomena:** PM, FDT, SDT (per registry)
**Status:** Stage 2 scope DRAFTED and Stage 3 selection-hardening probe RUN (Shravan, 2026-10-09). The
"smallest" claim holds after a completeness test that FLIPPED the scout's narrow ranking (see Selection
note). Honest production frame ≈ **1,620**, robust: every genuine registered construct adds ≤24; the
large OR-gains are development/wage/relative-income inflaters that annex neighbour literatures and are
excluded. Housing control reproduced at 162. Next: formalize the on-branch frame probe
(`source/build/goldset/101_c1a_frame_probe.py`), resolve cold-start anchors, build citation + production
frames, blinded screen, OA retrieval, interim synthesis.

## Causal claim

Holding prices and the price of time (wages) constant, an exogenous increase in household income or
wealth raises fertility, because children are a normal good. C.1.a is the **baseline Beckerian
counterfactual** — the prediction whose *secular failure* (fertility falls as incomes rise) is the
central puzzle every other economic hypothesis (C.2 cost, C.3 value, C.6 relative income) exists to
resolve. The chapter's job is therefore not to explain the decline but to establish the **sign and
magnitude of the pure income effect once the confounds are stripped out**, and to read demographic
significance as: does the normal-good mechanism survive as a positive force, and is it large enough to
matter against the cost/value channels?

## Estimand

The income elasticity of fertility (or the per-dollar / per-shock marginal effect) identified off an
**income or wealth shock that is NOT also a shock to the price of time or relative prices**. Treatment
variants, in descending order of cleanliness for the *pure* effect:

| cell | shock | why it isolates the income effect |
|---|---|---|
| CLEAN | lottery / lump-sum windfall (Cesarini et al. 2017) | pure wealth, prices & wages unchanged |
| CLEAN | cash transfer / UBI / negative income tax / EITC income component | income moved, (ideally) price of time held |
| CLEAN | housing-wealth / asset-price windfall (Lovenheim–Mumford 2013, Dettling–Kearney 2014) | wealth shock to owners |
| CLEAN | commodity/resource windfall to households (Kearney–Wilson 2018 fracking; Black et al. coal booms) | local income shock |
| MIXED → route out | wage/earnings change, job loss/displacement (Lindo 2010), trade shock | moves income AND price of time → **C.2.e** |
| CONTEXT | pre-industrial income–fertility gradient (Clark 2007) | historical PM-era test of the normal-good sign |

**Outcome axis** (identical to the d1c/d1d probes so the housing control reproduces): fertility /
childbearing / birth rate / TFR / childlessness / completed fertility / fertility intentions.

## Eligibility rules

- **Include** studies that estimate the effect of a plausibly-exogenous income or wealth shock on a
  fertility outcome, with the price of time / wages not the driving channel.
- **Include** the historical/pre-industrial gradient studies (PM-era sign test; Clark 2007 and the
  historical-demography literature on wealth and surviving offspring).
- **Exclude** pure wage/opportunity-cost studies (→ C.2.e), relative/cohort-income studies (→ C.6.a),
  pure uncertainty/liquidity/debt studies (→ C.5.a / C.3.e / C.3.g), and the macro
  "economic-development → fertility" bundle (confounds income with mortality decline, schooling,
  urbanization, women's wages).
- **Reverse cell** (route out): fertility → household income (children lower maternal labor supply).

## Walls (load-bearing; read from both sides at Stage 3)

1. **C.2.e Female Wage / Opportunity Cost of Time — THE wall.** A wage shock moves income *and* the
   price of time together. C.1.a owns only the income (wealth) channel with the price of time held
   constant; identification must use a non-labor income/wealth shock. A study whose treatment is a
   wage/earnings change routes to C.2.e. (The registry claim defines C.1.a against exactly this.)
2. **C.6.a Easterlin Relative Income (drafted, TICK-078).** Absolute (normal-good) vs relative/cohort
   income. Oscillation-predicting relative-income designs → C.6.a.
3. **C.5.a Economic Uncertainty · C.3.e Credit Constraints · C.3.g Student Debt (drafted).** Resources
   moved through risk / liquidity / debt, not a permanent-income normal-good effect.
4. **"Economic development → fertility" macro bundle — EXCLUDED inflater.** Probe: +4,364 records. Bundles
   mortality decline, schooling, structural change, female wages. Screen-routing signal only, never base
   recall.
5. **REVERSE / mechanical.** Fertility → income.

## Selection note — the completeness test flipped the scout's narrow ranking (the A.6/A.3 lesson)

The fresh 2026-10-08 cross-field scout left, after D.1.c, a narrow ranking of unstarted candidates in
which C.2.e (female-wage) looked *smaller* than C.1.a: C.4.a 893, **C.2.e 1,259**, **C.1.a 1,620**,
B.2 4,465. A pre-claim selection-hardening probe (`temp/c2e_select_probe.py`, cache
`temp/c2e-select-cache.json`; identical outcome axis; housing control 162) priced each candidate against
its own registered constructs and flipped the order:

- **C.2.e was undercounted.** Its scout union omitted plain synonyms of its *own* constructs; adding only
  "female wages / female labor supply / women's employment" (no inflater) takes the frame to **1,863**,
  and "+maternal employment" (+172) / "+substitution effect" (+92) to **~2,035**.
- **C.1.a is near-complete and robust at ~1,620.** Genuine additions ≤24 each (permanent income +24,
  wealth effect +24, normal good +15, income elasticity of fertility +0). Inflaters correctly excluded:
  economic development +4,364, living standards +913, GDP per capita +613.

Honest ranking: **C.1.a ~1,620 < C.2.e ~2,035 < C.4.a ~2,400 < B.2 4,465.** C.1.a is the next-smallest.
Full numbers in the ticket Log and `literature/search-logs/c1a-frame-probe-2026-10-09.md`.

**On-branch Stage-3 probe (2026-10-09), apples-to-apples note.** The on-branch frame probe
(`101_c1a_frame_probe.py`) reports a C.1.a *production recall* frame of **2,191**, not 1,620 — because
it adds the CLEAN-cell identification-strategy terms (income shock, cash transfer, lottery) that are the
right recall terms for actually retrieving the pure-income-effect studies. This is NOT a re-flip against
C.2.e: on an apples-to-apples **claim-noun** basis (the comparison the ranking is made on) C.1.a is
~1,680 (every registered claim noun adds ≤24: income elasticity +0, permanent income +0, wealth effect
+0, normal good +15), below C.2.e's claim-noun ~1,863–2,035; the C.2.e frame was NOT given its analogous
treatment terms (minimum wage, trade shock), so adding ID strategies to C.1.a only is not comparable.
2,191 is C.1.a's fuller recall frame; ~1,680 is its ranking frame. Housing control reproduced at 162.
Walls clean at the identified level: C.2.e (THE wall) overlap-AND-identified 22/166 (resolves at full
text on labor vs non-labor income shock), C.6.a 1, uncertainty/debt 7, DEV bundle 13 (neighbour 10,215
correctly excluded from base recall), REVERSE 10. Identified empirical core ≈ **166** records.

## Cold-start anchors (pre-query; to be RA-frozen)

Seminal (registry): Becker 1960 "An Economic Analysis of Fertility"; Malthus 1798 (positive check,
income→fertility, not OpenAlex-indexed); Jones, Schoonbroodt & Tertilt 2011 "Fertility Theories: Can
They Explain the Negative Fertility–Income Relationship?"; Clark 2007 *A Farewell to Alms* (pre-industrial
positive gradient). Key CLEAN-cell empirical anchors: Cesarini, Lindqvist, Notowidigdo & Östling 2017
(Swedish lottery wealth → fertility/labor); Lovenheim & Mumford 2013 (housing wealth → fertility);
Dettling & Kearney 2014 (house prices → births, owners vs renters); Kearney & Wilson 2018 (fracking income
→ fertility, marital vs non-marital); Lindo 2010 (husband job displacement → fertility — MIXED, routes to
C.2.e but anchors the wall); Black, Kolesnikova, Sanders & Taylor 2013 (Appalachian coal booms → fertility);
Löken 2010 / Löken, Mogstad & Wiswall 2012 (Norwegian oil-income → child outcomes, income nonlinearity).
