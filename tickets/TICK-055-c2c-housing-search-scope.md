# TICK-055: C.2.c search scope — tenure-conditional sign, pooling rule, walls
**Status:** in-progress
**Assigned:** Shravan
**Parallel-safe:** yes (no file overlap with the live D.3.b, B.1, or A.10 work)
**Blocks:** C.2.c cold-start anchors, C.2.c query build (tickets not yet opened)
**Blocked by:** none
**Touches:** literature/search-logs/housing-costs-search-scope.md, tickets/QUEUE.md

## Description

Open C.2.c (Housing Costs and Space Constraints, slug `housing-costs`, SDT only) at GACS Phase
A1/A2 — the same scope artifact that opened D.3.b and A.10.

C.2.c looks like a simple cost hypothesis and is not. Its own `notes` field concedes the problem:
"Ambiguous sign because home-equity wealth effect partially offsets cost effect." A house price
increase is a **cost** to renters and prospective buyers and a **wealth gain** to existing owners,
and the two push fertility in opposite directions. Three consequences the scope has to settle before
any search runs:

1. **The aggregate elasticity is not a transportable parameter.** Any population-level estimate is a
   tenure-composition-weighted average of two opposing channels, with the weight set by the local
   homeownership rate among people of childbearing age. Pooling aggregate estimates across settings
   with different ownership rates produces a number that is an artifact of the sample's tenure mix,
   not a behavioral parameter. This needs a pooling rule before extraction, in the spirit of the OAS
   conservative pooling rule (TICK-027) and the A.10 sign convention (TICK-054).

2. **Conditioning on tenure — the thing the chapter must do — conditions on an endogenous
   variable.** Homeownership at the time of a price shock is chosen partly in anticipation of
   children. So the tenure-split estimates that make the chapter interpretable are themselves
   selected. This is the same structural problem as A.10's "conditions on marital status" cell, and
   it is where the risk-of-bias pass will concentrate.

3. **A demonstrated wall failure, not a hypothetical one.** Lovenheim and Mumford 2013 is listed as
   **seminal for both C.2.c and C.3.e** in HYPOTHESES-v5.md. The same paper is claimed by two
   hypotheses, which means the home-equity/collateral channel currently has two homes. A
   source-of-variation rule has to decide it.

Also needed: walls against A.23 (co-residence), C.2.b (direct child costs), C.2.g (urbanization),
and C.1.a (income effect), plus a tempo-vs-quantum tag, since a housing effect that only postpones
births has a much smaller demographic significance than one that reduces completed fertility.

**Second instance of the non-additivity problem.** Housing cost → co-residence (A.23) → fertility is
C.2.c's reduced form, exactly as sex ratio → marriage timing (A.7) → fertility is A.10's. That is now
two chapters hitting the same accounting hazard, which strengthens the case that the review needs a
general rule rather than a per-chapter note. Feeds the escalation already open from TICK-054.

## Acceptance criteria
- [ ] `housing-costs-search-scope.md` written to `literature/search-logs/`, following the D.3.b and
      A.10 scope structure.
- [ ] A tenure-conditional estimand structure: cost channel, wealth channel, and net/aggregate as a
      derived quantity rather than a primary pooled target.
- [ ] A pooling rule stating what may and may not be combined, with homeownership rate recorded as a
      required moderator on every aggregate estimate.
- [ ] Wall vs C.3.e keyed on source of exogenous variation (housing price vs credit terms), with the
      Lovenheim and Mumford double-listing resolved and the master-list correction recommended.
- [ ] Walls vs A.23, C.2.b, C.2.g, C.1.a, each with an operational discriminator.
- [ ] The endogenous-tenure threat stated as a risk-of-bias domain, not just a caveat.
- [ ] Treatment taxonomy separating price, rent, affordability ratio, and physical space/dwelling
      size — the "space constraints" half of the hypothesis title is a distinct estimand.
- [ ] Tempo-vs-quantum tag required on every included effect, with the A.11 cross-ref.

## Log
- 2026-07-31 (Shravan, RA decision): **a thin price-variation evidence base is an acceptable
  outcome.** The meta-analysis is constrained by the studies that exist; if few identify off housing
  prices, C.2.c becomes a theory-heavy chapter and that is the correct result, not a reason to loosen
  the walls or the price-variation ruling. Same posture as the D.3.b Wall 2 decision of 2026-07-25,
  and it carries the same standing obligation: the posture governs how the shrinkage is *interpreted*,
  not whether it is *reported*. That most of this literature studies tenure and mobility rather than
  prices is a finding about the field and belongs in the chapter, as does the surviving-study count.
- 2026-07-31 (Shravan/Claude): **snowball round 3. Merged pool 1,735; Tier-B frame 203.**
  **(1) Round 3 was the most valuable round and vindicated two scope calls.** It produced **the rent
  stratum** — `10.1016/j.regsciurbeco.2008.08.007`, "Do higher rents discourage fertility? Evidence
  from U.S. cities, 1940–2000" — which is close to the ideal C.2.c study: rent-identified, so it
  isolates the cost channel with no wealth offset and **no endogenous tenure split required**, over a
  60-year panel. And it produced a **historical cluster** reaching back to "Housing and the Birth Rate
  in Sweden" (*American Sociological Review*, **1937**), plus apartment-living and crowding studies
  from 1978–1995.
  **(2) The period question has outgrown the Li 2024 exception.** That ruling said if further FDT-era
  evidence accumulated, the `phenomena` field needs a formal update rather than a second case-by-case
  admission. Round 3 shows a housing-and-fertility literature running back to the 1930s, so **the
  threshold the ruling set is met and the field should go to Anup.**
  **(3) Main methodological result: the §7.2 stop rule is defective.** Yield decay stalled — 7.65,
  3.74, 2.93 per 50 — because each round added seeds targeting a new under-reached area. That is
  coverage expansion, not exhaustion of a fixed frontier, and the rule cannot tell the difference. It
  is ambiguous between a **same-seed** reading (this snowball stopped at round 2) and an
  **expanding-seed** reading (it may never terminate, since termination depends on RA imagination).
  Recommended amendment, for every hypothesis: report the **overlap rate** alongside yield — it climbs
  0% → 20% → 37% here and is the convergence signal that survives seed expansion; require the stop
  test to run **same-seed**; and make "no under-reached sub-area can be named" an explicit recorded
  stopping condition.
  **(4) Seed rule tightened.** Round 1 excluded keyword-scouted papers as seeds outright. Round 3
  replaced that with the test that actually matters — membership in the citation-reachable pool, not
  method of first discovery — since only a paper reachable *only* by keyword imports the query's blind
  spots. Li 2024 qualifies under the tightened rule and was seeded.
- 2026-07-31 (Shravan, RA decision): **Li 2024 admitted to the chapter**, so FDT-period evidence is
  not excluded on period grounds. The v5 `phenomena` field still reads SDT and updating it is a PI
  call, so the ruling governs *inclusion* while the verdict structure stays SDT-primary. If the
  snowball turns up more FDT-era evidence, the field needs a formal update rather than a second
  case-by-case exception.
- 2026-07-31 (Shravan/Claude): **channel-3 snowball, round 1 of ≥2.** 693-record pool,
  106-record Tier-B candidate frame. `housing-costs-snowball-{pool.json,log.md}`,
  `housing-costs-tier-b-frame.json`; scripts in `source/build/goldset/c2c/`.
  **(1) 82% of the housing→fertility core was snowball-only** — 87 of 106, 63 of them peer-reviewed
  articles. **But read it honestly: this is a breadth miss, not vocabulary-invisibility.** I checked
  the 532 off-keyword records for housing papers hiding from the vocabulary and there are
  essentially none — those buckets are other chapters' canon (C.1.a, C.5.a, C.2.d, Section E). The
  87 all carry both terms in their titles; the keyword sweep missed them by running few query forms
  and taking top-25 by citation. **Consequence: a C.2.c Recall(B) will be a weak test** — Tier B here
  is genuinely keyword-reachable, so a high number is near-guaranteed and largely uninformative. Do
  not quote it as evidence the method generalises without that caveat attached.
  **(2) Saturation NOT reached — round 2 is required.** 87 new relevant per 693 pulled ≈ 6.3 per 50,
  about six times the §7.2 stop floor. Also the seed set is unbalanced (3 econ-price, 1
  macro-comparative, **zero demog-tenure**); round 2 needs channel-2 canon seeds on the demography
  side. Keyword-scouted papers were declined as seeds on purpose, Li 2024 included, to keep Tier B
  non-circular.
  **(3) The preprint-twin hazard did measurable damage, not hypothetical damage.** The Dettling &
  Kearney JPubE record carries `cited_by_count = 0` — all 67 forward citations sit on the NBER twin.
  A snowball off published DOIs alone would have pulled **zero** forward citations from one of four
  canon seeds, silently. Repaired by merging twin citation sets (`twins.sh`). **This belongs in the
  pipeline as a standing step**, since every economics hypothesis will hit it. 46 duplicate-title
  groups / 105 records in the pool; *Partisan Fertility* appears five times.
  **(4) Two clean Wall 1 tests surfaced**, both routing to C.3.e under the ruling despite
  housing framing: `10.1093/restud/rdad034` (mortgage rate pass-through → fertility) and
  `10.1093/rfs/hhaa073` (mortgage market deregulation). Added to the decoy set. Also found
  `10.1007/s11150-016-9355-8`, "The asymmetric housing wealth effect on childbirth" — directly on the
  tenure asymmetry the pooling rule is built around, and a priority read.
  **(5) The ≥30 anchor floor is clearable but not yet cleared** — 63 new candidates are unscreened,
  and the count that matters is post-screen.
- 2026-07-31 (Shravan/Claude): **channel-1 anchor sourcing run. 25 anchors, all 25
  existence-verified, zero ghosts.** `housing-costs-cold-start-anchors.{json,md}`.
  **(1) Channel 1 is empty — no systematic review or meta-analysis of housing → fertility exists.**
  Four probe forms run before concluding it (OpenAlex `type:review`, two title/abstract review
  phrasings, WebSearch). The one near miss — Grewal et al. 2024, housing prices → *health* — was run
  down and excluded: its only overlap with this literature is Daysal et al. 2021, included for birth
  weight and prematurity, not fertility. **Two hypotheses in a row have now found channel 1 empty
  from opposite causes** (D.3.b too new, C.2.c never synthesised), which suggests GACS §7 move 5
  should be reported as tested-and-failed on that leg rather than left open.
  **(2) Tier-B integrity constraint, flagged before it becomes circular.** 20 of the 25 came from my
  own OpenAlex keyword sweep, which is GACS **channel 4**, not channel 2. They are Tier-A eligible
  but **must not enter Tier B** — that is exactly how the OAS recall number got inflated. Tier B has
  to come from a channel-3 snowball off the four canon seeds, which is the next step. Anchor count
  ~20, still **below the ≥30 CV floor**; the snowball has to close both gaps.
  **(3) All four v5 seminal names verify**, but the author list for Daysal et al. is incomplete in v5
  — it omits **Siersbæk**. Correction for TICK-001. Process note: my first Crossref probe for that
  paper returned nothing and it looked like a ghost; the query string was simply wrong. A single
  failed lookup is not evidence of non-existence.
  **(4) `housing` AND `fertility` is a booby-trapped phrase** — both are core vocabulary in animal
  science (livestock housing, breeding fertility) and agronomy (soil fertility). Dairy-cattle,
  biochar, and ruminant papers frequently out-ranked the on-topic economics by citation count.
  Epidemiological "Cohort Profile" papers are a second polluting class. Needs handling in the
  production query, not at screening, or it is paid for in LLM cost.
  **(5) The two vocabulary families are real and barely overlap** — `econ-price` (JPubE, REStat,
  Economic Inquiry, J. Housing Econ) vs `demog-tenure` (Housing Studies as the hub, Demography,
  Demographic Research, EJP). They surface different papers, not the same papers renamed. Separate
  cause-axis clusters, separately budgeted.
  **(6) Preprint twins are pervasive and DOI dedup will not catch them.** Four of the five strongest
  anchors have NBER/SSRN twins on separate DOIs, and citation counts split across versions — the
  Dettling & Kearney JPubE record shows c=0 while its NBER twin shows c=67, so a citation-ranked
  cutoff would keep the working paper and discard the published one. Normalized-title dedup is
  load-bearing; the published version wins.
  **(7) New scope question for the PI, separate from A.10's.** Li 2024 (Labour Economics) runs a
  global house-price panel **1870–2012** framed against the fertility transition, i.e. FDT — but v5
  scopes C.2.c to **SDT only**, which would exclude the most historically comprehensive study in the
  pool. Unlike the A.10 war-shock gap the routing target exists; the only question is the period
  restriction. Does not block the snowball.
- 2026-07-31 (Shravan/Claude): **scope drafted, not frozen.**
  `literature/search-logs/housing-costs-search-scope.md`. Six walls, 18 estimand cells, a
  pre-registered pooling rule, and seven required per-effect tags. What the drafting settled or
  surfaced beyond the ticket:
  **(1) The pooling decision, which is the consequential one.** The primary pooled targets are the
  two tenure-specific channels, pooled *separately*; the aggregate net effect is demoted to a
  secondary, derived quantity requiring the setting's homeownership rate as a moderator. This means
  the review does **not** primarily estimate the thing the hypothesis as written claims — the net
  effect — because that quantity is a composition-weighted average, not a behavioral parameter, and
  is not transportable across settings. Needs sign-off; it is the analogue of TICK-027 for this
  chapter and should probably become a `decisions/` entry if it holds.
  **(2) Rent-identified estimates are a quality stratum, not just another measure.** A rent increase
  has no offsetting wealth gain for the payer, so rent variation isolates the cost channel without
  needing the endogenous tenure split at all. Given that the tenure split is C.2.c's main
  identification weakness, the rent stratum may end up carrying the chapter.
  **(3) Affordability ratios are close to uninterpretable** and are barred from the price and rent
  pools. Income sits in the denominator with its own opposite-signed fertility effect (C.1.a), so a
  negative price-to-income coefficient is consistent with a pure income effect and no price effect.
  **(4) Two heterogeneity dimensions are load-bearing, not optional:** parity (housing should bind
  hardest at the birth that requires another bedroom — cross-ref A.8) and tempo-vs-quantum (if
  housing mostly postpones, the §7 demographic-significance verdict shrinks sharply — cross-ref A.11,
  precedent at TICK-038).
  **(5) The Lovenheim and Mumford double-listing is resolved by a source-of-variation rule**: housing
  price variation → C.2.c regardless of the channel invoked; credit terms at fixed prices → C.3.e.
  Master-list correction recommended for TICK-001, not made here.
  **(6) Non-additivity, second instance.** C.2.c → A.23 → fertility has the identical structure to
  A.10 → A.7 → fertility. Folded into the TICK-054 escalation rather than raised separately, since
  two instances make it a review-wide rule question rather than a chapter quirk.
- 2026-07-31 (Shravan/Claude): opened and claimed. No prior C.2.c artifacts in
  `literature/search-logs/`, `extraction/`, or `output/chapters/`.
