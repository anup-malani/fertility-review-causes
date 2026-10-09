# Income Effect on Fertility — are children a normal good?

**Category:** C. Economic — C.1 Income · **Primary mechanism:** holding prices and the price of time fixed, higher household income or wealth raises fertility because children are a normal good. · **Cross-references:** C.2.e Female Wage and Opportunity Cost of Time (the load-bearing wall — a wage shock moves income *and* the price of time); C.6.a Easterlin Relative Income (relative vs absolute income); C.5.a Economic Uncertainty; C.2.d Tax and Transfer Pronatal Policies (child-contingent transfers are a price subsidy, not a pure income shock). · **Status:** TICK-098; interim draft 2026-10-09 (Shravan); NOT PI-reviewed; written on 6 of 170 in-scope full texts (4%).

---

## 1. The claim

This chapter explores the effect of household income on fertility.

**In plain terms:** if having and raising children is something people enjoy and would buy more of when they can afford it — like bigger homes, more travel, or better food — then richer families should choose to have more children, and getting richer should push a family's childbearing up, not down. That is the simplest economic guess about money and babies. The striking fact this chapter is built around is that the guess is wrong at the level of whole societies: as countries have grown vastly richer over the last century and a half, they have had *fewer* children, not more. So this chapter is not really a candidate explanation for why fertility fell — it is the baseline prediction whose failure is the puzzle that every other economic explanation in this review exists to solve.

**Technically:** in the static consumer model of Becker (1960), children enter the household utility function as a good. Holding the relative price of children and the price of parents' time fixed, an increase in full income raises the demand for children if children are a normal good (positive income elasticity). The observed secular relationship is the opposite — a negative cross-sectional and time-series association between income and fertility — which can be reconciled with a positive *pure* income effect only if offsetting forces (a rising relative price of children, a rising opportunity cost of parental time, quality-quantity substitution, changing tastes) dominate. The parameter of interest is therefore the sign and size of the pure income effect, net of those channels; the empirical difficulty is that almost nothing moves household income without also moving one of them.

## 2. Theoretical mechanism

In the Beckerian household model the demand for the number of children $n$ depends on full income $I$, the relative price of a child $p_n$, the price of parents' (mainly the mother's) time $w$, and tastes. The income effect is $\partial n/\partial I$ at fixed $p_n, w$. The hypothesis is that this derivative is positive — children are a normal good.

This is a **behavioural parameter, not an identity**: it can be wrong, and the model says exactly how. The hypothesis is falsified for the pure income effect if a clean, exogenous rise in unearned income or wealth — one that does not change wages or the relative price of a child — *lowers* fertility (children inferior), or leaves it unchanged (income irrelevant at the margin). It is *not* falsified by the raw negative income–fertility correlation, because that correlation confounds the income effect with (i) the opportunity-cost-of-time effect, since higher-earning people face a higher price of time (this is C.2.e, and it is the central wall of this chapter); (ii) quantity–quality substitution (C.3.d); and (iii) relative-income and cohort effects (C.6.a). The margin is the intensive margin (completed family size / the quantum of fertility), though several of the cleanest shocks identify only timing (the tempo margin), which is a distinct and weaker test.

The single hardest identification problem is that **the most policy-relevant income variation is earned**, and earnings move the price of time. A pure income test therefore requires a *non-labour* income or wealth shock: a lottery win, an unearned windfall, an asset-price gain to an owner, a transfer not conditioned on having children. Transfers that *are* conditioned on a birth (child allowances, baby bonuses, per-child tax exemptions) are a cut in the price of a child, not a pure income shock, and belong to C.2.d; this chapter treats them as out-of-cell evidence.

## 3. Search strategy

OpenAlex `title_and_abstract.search`, construct union AND a fertility-outcome axis, assembled from three sources (`source/build/goldset/102_c1a_build_pool.py`): 15 cold-start anchors resolved live against OpenAlex (title Jaccard ≥ 0.60, year ±1), their backward references and forward citers, and the production "identified core" (the recall union AND an identified-design marker). Pool: **1,119** unique works. Frame probe and completeness test in `literature/search-logs/c1a-frame-probe-2026-10-09.md`.

**Walls and their enforcement.** The load-bearing wall is **C.2.e (female wage / price of time)**: a wage or earnings shock moves income and the price of time together, so it cannot identify the pure income effect. The blinded screen routed 50 records to C.2.e — the wall is enforceable and was enforced. Secondary walls: **C.6.a** (relative/cohort income; 2 routed), **C.5.a / C.3.e / C.3.g** (uncertainty, credit, debt; 19 routed), and the **economic-development macro bundle** (GDP/growth/modernization, which bundles mortality decline, schooling, urbanization and women's wages) — declared an *excluded inflater in advance* (the completeness test showed "economic development" alone adds +4,364 records that annex the development literature; 24 records routed to ROUTE_DEV). The reverse cell (fertility → income) took 20.

**Boundary ruling made in advance.** Child-contingent cash (child allowances, baby bonuses, per-child exemptions) is a price-of-child subsidy and routes to C.2.d, not here, even though it raises household income; only *unconditional* income/wealth shocks are in-cell. This ruling is responsible for a large share of the RELEVANT-but-out-of-core records and is the main judgment call the RA gate should re-check.

## 4. PRISMA flow

| Stage | n |
|---|---|
| Pool assembled (anchors + citation frame + identified core) | 1,119 |
| Title/abstract screened (abstract present) | 769 |
| Abstract absent → RA title/abstract gate (UNCERTAIN) | 350 |
| In-scope after screen (RELEVANT + POOLING + HISTORICAL) | 170 |
| — of which open-access (retrievable now) | 98 |
| Routed to C.2.e (wage/price-of-time wall) | 50 |
| Routed to C.5.a / C.3.e / C.3.g, C.6.a, ROUTE_DEV, REVERSE | 115 |
| Full texts retrieved and read | 6 |
| Full texts yielding a usable income-shock fertility estimate | 3 |

Three features change how this chapter should be read. **First, 390 of 1,119 records carry no abstract** and are parked at the RA title/abstract gate; the in-scope count will move when they are screened. **Second, the in-scope set is dominated by child-contingent transfer studies** (C.2.d-adjacent), so the count of *pure* income-shock studies is far smaller than 170. **Third, three of the four highest-value clean-shock anchors are paywalled** (Lovenheim–Mumford housing wealth; Lindo displacement; the Cesarini lottery evidence) and sit on the RA wantlist — the retrieved evidence is a convenience sample of what is open-access, and it under-represents the cleanest designs.

## 5. The ideal design

**5.1 The ideal estimand.** The change in completed fertility caused by a permanent, fully-anticipated increase in household *unearned* income (or wealth), holding the wage/price of parents' time and the relative price of a child fixed, for a representative population over its reproductive span — i.e. $\partial n / \partial I$ at fixed $w, p_n$, in children per log unit of income.

**5.2 The design that would identify it.** A large, exogenous, non-labour income or wealth shock — a lottery, a universal unconditional transfer, an asset windfall uncorrelated with local labour demand — linked to administrative completed-fertility records, with the wage path shown to be unaffected, and enough follow-up to separate timing from quantum.

**5.3 Distance table.**

| Study | Shock | Clean of the wage channel? | Outcome | Distance from ideal |
|---|---|---|---|---|
| Golosov et al. 2021 (lottery/unearned income) | lottery winnings | **Yes — ideal shock** | marriage, divorce — **no fertility outcome** | Ideal design, wrong dependent variable: does not estimate the parameter |
| Dettling & Kearney 2014 (house prices) | MSA house-price change | Partly (owner side is wealth; confounded by home-equity/credit extraction) | conception-year fertility rate (timing) | Moderate: wealth shock but timing not quantum, owner/renter sign split |
| Black et al. 2013 (coal boom) | local coal income | No — raises men's wages (MIXED) | birth rates + completed fertility (CEB) | Far on cleanliness, close on outcome |
| Kearney & Wilson 2018 (fracking) | local resource boom | No — raises male earnings (MIXED) | marital/nonmarital birth rates | Far on cleanliness, close on outcome |
| Comolli 2017 (Great Recession) | macro recession | No — dominated by unemployment/uncertainty | TFR (aggregate) | Out of cell → C.5.a |

## 6. Included studies

| Study | Design | Shock type | Fertility effect | Sign | Clean income effect? |
|---|---|---|---|---|---|
| Black, Kolesnikova, Sanders & Taylor 2013 | IV + cohort DiD | MIXED (wage+income) | income elasticity of the birth rate ≈ **+0.7** (IV); completed-fertility elasticity ≈ +0.5; ≈ +0.18–0.20 child/woman (1946 cohort) | **+** | No (bundles wages) |
| Kearney & Wilson 2018 | reduced-form panel (simulated production) | MIXED (wage+income) | **+5.96** total births / 1,000 women 18–34 per \$1,000/capita new production (marital +3.57, nonmarital +2.39); no shift into marriage | **+** | No (bundles male earnings) |
| Dettling & Kearney 2014 | IV (Saiz elasticity × national trend) | wealth (owners) / price (renters) | owner side **+5%** (OLS) / **+7.2%** (IV) per \$10k; renter side **−2.4%**; net **+0.8%** at the 44% mean ownership; crossover ≈ 30% ownership | **+** (owners) | Partly (owner wealth, but home-equity/credit confound; timing only) |
| Golosov, Graber, Mogstad & Novgorodsky 2021 | lottery event-study | CLEAN unearned income | **no fertility outcome reported**; marriage +0.8pp (+5.5%), divorce −0.7pp (−5.9%) per \$100k | n/a | Yes (but does not measure fertility) |
| Comolli 2017 | macro panel (log-log FE) | CONTEXT | TFR elasticity w.r.t. unemployment ≈ −0.08; ≈ −0.047 births cumulative (~3% of TFR) — driven by unemployment/uncertainty | − | No → C.5.a |

**The naive-estimator check (§2.2).** The naive estimator in this literature is the raw cross-sectional income–fertility gradient, which is **negative**. It conditions the comparison on something that moves with the outcome: higher-income households are higher-*wage* households, and the wage is the price of the mother's time (C.2.e). The bias is therefore signed *against* the hypothesis — the naive gradient understates (indeed reverses) the pure income effect. Every identified study here that strips the wage channel out, even imperfectly, finds the sign flips to **positive**: this is the central result of the included body. The disagreement between the naive negative gradient and the identified positive effect is not heterogeneity about one parameter; it is one confounded estimator and several less-confounded ones, and the correct reading names the confound (the price of time) and reports the sign reversal.

## 7. Quantitative synthesis

**7.1 In plain terms.** When researchers find a way to make some families richer for a reason that has nothing to do with the parents getting better-paying jobs — a local mining or drilling boom, a jump in the value of a house someone already owns — those families do tend to have *more* children, not fewer. So at the level of a single family hit by a windfall, children do look like a normal good, just as the simple theory says. But two cautions swamp this. First, almost every study that finds the positive effect is looking at a boom that *also* raised wages, so we cannot cleanly separate "they had more money" from "their time became more valuable." Second, the one study using the cleanest possible money shock — lottery wins — never looked at whether winners had more children. So the honest summary is: the positive income effect probably exists and is modest, but the clean evidence for it is thin to the point of being almost absent, and it is dwarfed many times over by the forces pushing fertility down.

**7.2 The estimate.** No meta-analytic pooling is warranted: the three usable estimates are on different outcomes (birth-rate elasticity, births per 1,000 per dollar of local production, conception-year fertility rate), different shocks, and different margins (quantum vs timing), and only one even nominally isolates a non-labour shock. Narratively: the identified income elasticity of fertility is **positive and of order +0.5 to +0.7** where completed fertility is measured (Black); local positive shocks raise births by roughly 1–6% (Black, Kearney–Wilson); the one asset-wealth estimate is positive for owners (+5–7% per \$10k) but captures timing, splits by tenure, and is confounded by credit access (Dettling–Kearney). The cleanest design (Golosov) does not estimate the parameter. The body supports "children are (weakly) normal" with **low confidence**, and supports "the *pure* income effect has been cleanly identified" with essentially **none**.

## 8. Demographic significance

**The phenomenon to be explained is measured in a decline in whole children per woman (a fall in the TFR of roughly 3–5 children over the FDT and ~1 child over the SDT); this mechanism offers a *positive* income elasticity of fertility of order +0.5 to +0.7.** The units are commensurable, but **the sign is opposite**: the mechanism pushes fertility up while the phenomenon is a fall. This is decisive and is established before any share is computed — a positively-signed mechanism cannot account for a decline. What the arithmetic then shows is not how much of the decline the income effect explains, but how large a *counterforce* it was.

**Slope check (the puzzle, quantified).** Over the FDT real income per head rose several-fold; taking a conservative ln-income rise of ≈1.6 (a five-fold increase) at an elasticity of +0.7 predicts fertility should have risen by ≈ +110%. Instead it roughly halved. The pure income effect thus predicts a change of the **opposite sign and of order-of-magnitude comparable size** to what occurred — which is exactly why the cost, time-price, and value channels (C.2, C.3) must be large: they had to overcome a powerful positive income force *and* then drive fertility down on top of it.

**8.1 Pre-modern variation (PM).** For pre-modern variation, the verdict is **NOT ASSESSED**, because the in-scope historical test (Clark's Malthusian "survival of the richest" evidence, W2108780127) is paywalled and on the RA wantlist, so no PM-era share was computed; were it assessed, the sign is expected to be **positive and large** (the income effect dominated before the structural transition — richer households left more surviving children).

**8.2 First Demographic Transition (FDT).** For the FDT, the verdict is **NEGLIGIBLE**, because the pure income effect is positive while the FDT is a decline, so it explains none of the fall (its contribution is ≤ 0% of the decline; it is a counterforce the other channels had to overcome, not a cause). Denominator: the FDT TFR decline over its full window; numerator: a mechanism of the wrong sign.

**8.3 Second Demographic Transition (SDT).** For the SDT, the verdict is **NEGLIGIBLE**, because the same sign mismatch holds — the income effect, where identified, remains positive (Kearney–Wilson, Dettling–Kearney on post-1990 US data), so it cannot explain the post-1965 decline and again enters as a small positive counterforce.

## 9. GRADE rating

Rated on the question "is the pure income effect on fertility positive (children normal)?", per phenomenon.

| Phenomenon | Starting level | Downgrades | Rating |
|---|---|---|---|
| PM | — | no retrieved study in cell (Clark paywalled) | **No evidence** |
| FDT | observational/quasi-experimental | risk of bias (all identified shocks bundle wages or a credit channel) −1; indirectness (clean design measures no fertility; shocks are local/MIXED, timing not quantum) −1; imprecision (≤3 usable estimates) −1 | **Very low** |
| SDT | observational/quasi-experimental | same three downgrades; evidence is modern-US-concentrated (inconsistency/indirectness of setting) | **Very low** |

The rating concerns the *existence and sign* of the pure income effect; it is independent of the demographic verdict, which is NEGLIGIBLE for FDT/SDT on sign grounds regardless of how certain the effect is. A well-identified positive income effect and a NEGLIGIBLE contribution to the decline are fully consistent — that is the whole point of this chapter.

## 10. Verdict

Children behave as a (weakly) normal good: where a positive income or wealth shock has been credibly identified, fertility rises, which overturns the naive negative income–fertility correlation that confounds income with the price of parents' time. But the pure income effect has barely been cleanly identified — the studies that measure fertility bundle wages (coal, fracking) or a credit channel (housing), and the one near-ideal clean design (a lottery) never measured childbearing. Crucially, the effect is **positive**, and the demographic transitions are **declines**: the income effect is not a cause of fertility decline but the **counterfactual that the decline contradicts**. The one number to carry away: the income elasticity of fertility is about **+0.7** where completed fertility is measured — large enough that, applied to the income growth of the last 150 years, it predicts fertility should have *doubled*; that it instead halved is the measure of how much work the cost and value channels must do.

## 11. Open questions

- **PI call — scope of child-contingent transfers.** This draft routes child allowances / baby bonuses / per-child exemptions to C.2.d (price of a child), keeping only unconditional shocks here. A large part of the in-scope literature is transfer studies; confirm the boundary or import a defined slice.
- **PI call — the counterfactual framing.** Confirm that C.1.a should be written as the baseline/counterfactual (NEGLIGIBLE-by-sign for FDT/SDT) rather than as a candidate cause, and that PM is where its positive verdict lives.
- **Retrieval priorities (RA wantlist, `extraction/income-effect-normal-good-missing-pdf-dois.csv`):** Clark 2006 "Survival of the Richest" (the PM test — would move PM from NOT ASSESSED); Lovenheim & Mumford 2013 (the clean housing-wealth/completed-fertility study); Lindo 2010 "Are Children Really Inferior Goods?" (displacement income shock); the Cesarini Swedish-lottery evidence on fertility if it exists. The 390 abstract-less records also need the RA title/abstract gate.
- **A study that should exist but does not (cleanly):** a lottery/unconditional-transfer design with completed fertility as the primary outcome and the wage path shown flat. Golosov et al. had the ideal shock and the administrative data but did not report fertility; a fertility-outcome companion would be the single most valuable paper for this cell.

## 12. References

Becker 1960; Jones, Schoonbroodt & Tertilt 2011 (W2122913499); Black, Kolesnikova, Sanders & Taylor 2013 (10.1162/REST_a_00257); Dettling & Kearney 2014 (10.1016/j.jpubeco.2013.09.009); Kearney & Wilson 2018 (10.3386/w23408); Golosov, Graber, Mogstad & Novgorodsky 2021 (10.3386/w29000); Comolli 2017 (10.4054/DemRes.2017.36.51); Clark 2007 / 2006 (W2108780127, on wantlist); Lovenheim & Mumford 2013 (10.1162/rest_a_00266, on wantlist); Lindo 2010 (10.1353/jhr.2010.0012, on wantlist). Full extraction: `extraction/income-effect-normal-good.csv`; risk of bias: `extraction/income-effect-normal-good-risk-of-bias.csv`.

---

### Provenance and standing caveats

**This chapter is written on 6 of 170 in-scope full texts (4%).** Of the 6 retrieved, 3 yield a usable income-shock fertility estimate (Black, Kearney–Wilson, Dettling–Kearney), 1 is the ideal clean design with no fertility outcome (Golosov), 1 routes out to C.5.a (Comolli), and 1 was a procurement error (the file retrieved for the Cesarini lottery paper was a different NBER working paper and was discarded — no numbers were taken from it).

**The findings that would survive full retrieval are** the sign reversal (identified positive income effect vs naive negative gradient) and the sign-mismatch demographic verdict (NEGLIGIBLE for FDT/SDT because the mechanism is a positive counterforce), both of which are robust to adding studies and follow from the mechanism's sign. **The findings that might not are** the magnitude (the ≈ +0.7 elasticity rests largely on one MIXED coal-boom study and would shift with Lovenheim–Mumford, Lindo, and the lottery evidence) and the PM verdict (NOT ASSESSED only because Clark is unretrieved; it is expected to become positive/DOMINANT on retrieval).

**Numbers taken from abstracts rather than full text:** none in the included-study estimates (all 3 usable estimates are from full text); the in-scope counts and the transfer-literature characterization rest on title/abstract screening only.

**Human gates still open:** (4) RA title/abstract review of the 390 abstract-less UNCERTAIN records; (5) RA proxy/ILL retrieval of the paywalled canon on the wantlist; (6) RA 5–10% screen spot-check; (7) RA 10% extraction verification; (11) three-rater GRADE panel; (13) RA lay-readability; (14) PI review and the §11 calls.
