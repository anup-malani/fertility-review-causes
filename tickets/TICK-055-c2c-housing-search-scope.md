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
- 2026-07-31 (Shravan/Claude): opened and claimed. No prior C.2.c artifacts in
  `literature/search-logs/`, `extraction/`, or `output/chapters/`.
