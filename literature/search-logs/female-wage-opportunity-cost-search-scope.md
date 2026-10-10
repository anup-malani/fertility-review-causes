# Search scope — Female Wage and Opportunity Cost of Time (C.2.e)

**Ticket:** TICK-099
**Hypothesis slug:** `female-wage-opportunity-cost`
**Registry:** HYPOTHESES-v5.md §C.2.e
**Target phenomena:** FDT, SDT (per registry — C.2.e does **not** claim PM)
**Status:** Stage 2 scope DRAFTED and Stage 3 on-branch frame probe RUN (Shravan, 2026-10-10). C.2.e is the
next-smallest genuinely-unstarted hypothesis after C.1.a (TICK-098). The on-branch probe
(`source/build/goldset/201_c2e_frame_probe.py`) reproduces the housing control at **162**, confirms the
honest production frame at **~2,557** (claim-noun/ranking frame ~1,924), and — via an incremental build-up
— confirms every registered construct adds coverage and the scout's narrow 1,259 UNDERCOUNTED C.2.e by
omitting its own synonyms (women's employment +347, female labor supply +212, maternal employment +175).

## Causal claim

Holding non-labor income constant, an exogenous rise in the **female (maternal) wage / the opportunity
cost of women's time** lowers fertility, because the **substitution effect** raises the effective price of
child-rearing time. This is the workhorse Becker/Mincer/Willis economic account of the FDT/SDT decline:
raising children takes time, predominantly the mother's; as her wage rises, each hour of childcare forgoes
more earnings, and if the substitution effect dominates the (positive) income effect, net fertility falls.
Unlike C.1.a (the normal-good counterfactual, whose secular *failure* is the puzzle), C.2.e is a candidate
**cause** of decline. The chapter's job: establish whether the pure price-of-time effect is (a) correctly
signed (negative), (b) causally identified off a wage/price-of-time shock that is not merely an income
shock, and (c) large enough to carry a demographically significant share of the FDT/SDT decline.

## Estimand

The fertility response to an **exogenous shock to the female wage / the price of a woman's time**, with
non-labor income held constant — i.e. the sign and magnitude of the **substitution effect**. Treatment
variants, in descending order of cleanliness for isolating the price-of-time channel:

| cell | shock | why it isolates the price-of-time (substitution) effect |
|---|---|---|
| CLEAN | labor-demand / trade shock raising female wages (e.g. export manufacturing, Bangladesh garment) | moves the wage with non-labor income roughly held |
| CLEAN | minimum-wage change bearing on female-dominated low-wage work | exogenous wage-floor shift to the price of time |
| CLEAN | sector/occupation wage shifts, returns to schooling for women | changes the price of the mother's time |
| CLEAN | gender-wage-gap closure / equal-pay reforms | raises female relative wage → price of time |
| MIXED → route out | a household income/wealth windfall (lottery, transfer, housing wealth) | moves income with the price of time held → **C.1.a** |
| MIXED → route out | norm/attitude/empowerment shift with no wage channel | ideational, not price → **D.2.a** |

**Outcome axis** (identical to the c1a/d1c/d1d probes so the housing control reproduces at 162):
fertility / childbearing / birth rate / TFR / childlessness / completed fertility / fertility intentions /
timing (age at first birth, postponement).

## Eligibility rules

- **Include** studies estimating the effect of a plausibly-exogenous shock to the female wage / price of
  the mother's time on a fertility outcome (substitution channel), with non-labor income not the driver.
- **Include** studies identifying off labor-demand/trade shocks, minimum wage, returns to schooling, or
  gender-wage-gap reforms where the operative margin is the price of the mother's time.
- **Exclude** pure non-labor income/wealth shocks (→ **C.1.a**), ideational empowerment/autonomy/norm
  studies with no wage channel (→ **D.2.a**), digital-leisure substitution (→ **C.2.h**), and the macro
  "economic-development/GDP → fertility" bundle (confounds the wage with mortality decline, schooling,
  urbanization).
- **Reverse / mechanical cell** (route out): fertility → female labor supply (the child/motherhood
  penalty — FLFP as the *outcome* of childbearing, not the wage as the exogenous driver of fertility).

## Walls (load-bearing; read from both sides at Stage 3)

1. **C.1.a Income Effect / Normal Good (drafted, TICK-098) — THE wall, read from the other side.** A wage
   change moves income *and* the price of time together. C.2.e owns only the price-of-time (substitution)
   channel with non-labor income held constant; C.1.a owns the pure income/wealth channel. A study whose
   shock is a *non-labor* income/wealth shock routes to C.1.a. On-branch probe: overlap 159, neighbour
   frame 2,068, overlap-AND-identified **19** (these resolve at full text on labor vs non-labor shock).
2. **D.2.a Female Empowerment / Autonomy.** C.2.e is the *economic* (labor-market price) channel of rising
   female status; D.2.a is the *ideational/autonomy/norm* channel. Norm/attitude/empowerment identification
   → D.2.a. Probe: overlap 165, neighbour 2,458, overlap-identified 12.
3. **C.2.h Digital Leisure Substitution.** Also a substitution effect, but toward leisure consumption, not
   labor income. Probe: overlap 28, identified 3.
4. **"Economic development / GDP → fertility" macro bundle — EXCLUDED inflater.** Probe: adding "economic
   development" alone adds +4,263 to the frame; neighbour frame 10,225. Bundles mortality decline,
   schooling, urbanization. Screen-routing signal only, never base recall.
5. **REVERSE / mechanical.** Fertility → female labor supply (child/motherhood penalty). Probe: overlap 51,
   identified 7; homonym "female employment as OUTCOME" reads 46 inside our frame.

## Selection note — next-smallest after C.1.a; the scout UNDERCOUNTED C.2.e

The 2026-10-08 cross-field scout priced C.2.e narrow at **1,259** using a 4-term union that omitted plain
synonyms of C.2.e's own registered constructs. The TICK-098 pre-claim selection probe showed those
synonyms take the honest frame to ~1,863 (+female labor supply/women's employment), and
"+maternal employment"/"+substitution effect" to **~2,035**. The honest, completeness-tested ranking:
**C.1.a ~1,620 < C.2.e ~2,035 < C.4.a ~2,400 < B.2 4,465.** With C.1.a consumed (TICK-098), C.2.e is
next-smallest.

**On-branch Stage-3 probe (2026-10-10), apples-to-apples note.** The on-branch probe reports a C.2.e
*production recall* frame of **2,557**, higher than the ~2,035 ranking estimate, because — per the ticket
caveat — it gives C.2.e its OWN analogous treatment/identification terms (minimum wage +153, trade shock
+11, returns to schooling +14, gender wage gap +171) that the C.1.a ranking probe deliberately withheld to
keep the *ranking* comparison honest. On the claim-noun basis (the comparison the ranking is made on) C.2.e
is ~1,924, still above C.1.a's ~1,680. The incremental build-up confirms completeness: from the scout seed
(FLFP, 798) every registered construct adds coverage — nothing redundant, nothing missing (the A.6/A.3
requirement). Housing control reproduced at 162. Identified empirical core (frame AND identified-design
markers) ≈ **211** records. Full numbers in `literature/search-logs/c2e-frame-probe-2026-10-10.md`.

## Cold-start anchors (pre-query; to be RA-frozen)

Seminal (registry): Mincer 1963 "Market Prices, Opportunity Costs, and Income Effects"; Becker 1965 "A
Theory of the Allocation of Time"; Willis 1973 "A New Approach to the Economic Theory of Fertility
Behavior"; Butz & Ward 1979 "The Emergence of Countercyclical U.S. Fertility"; Schultz 1985 "Changing
World Prices, Women's Wages, and the Fertility Transition: Sweden, 1860–1910"; Autor, Dorn, Hanson,
Pettersson & Song 2019 (trade-induced labor-demand shifts). Key CLEAN-cell empirical anchors: Heckman &
Walker 1990 (Swedish wages → birth timing); Schultz 1985 (Swedish grain/wage prices → fertility
transition); Jensen 2012 (India BPO recruiting → young women's work and fertility/marriage); Heath & Mobarak
2015 (Bangladesh garment export → girls' schooling, marriage, fertility); Bloom, Canning, Fink & Finlay
2009 (female labor supply and fertility); Agüero & Marks 2011 (infertility shocks as instrument — the
reverse-cell check); Angrist & Evans 1998 (children → labor supply — the REVERSE anchor that marks the
wall). Treatment-anchor for the price-of-time identification: Adda, Dustmann & Stevens 2017 (career costs
of children, dynamic life-cycle).
