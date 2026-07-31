# TICK-054: A.10 search scope — boundary walls, estimand cells, sign convention
**Status:** in-progress
**Assigned:** Shravan
**Parallel-safe:** yes (no file overlap with the live D.3.b or B.1 chains)
**Blocks:** A.10 cold-start anchors, A.10 query build (tickets not yet opened)
**Blocked by:** none
**Touches:** literature/search-logs/sex-ratio-marriage-market-search-scope.md, tickets/QUEUE.md

## Description

Open A.10 (Sex Ratio Imbalance and Marriage Market Effects, slug `sex-ratio-marriage-market`) at GACS
Phase A1/A2: state the causal claim as `cause → effect`, fix the boundary walls, enumerate the
estimand cells, and freeze the eligibility rules — the same artifact that opened D.3.b
(`climate-anxiety-eco-doomerism-search-scope.md`) and gated everything downstream of it.

A.10 arrives with three problems that must be settled in the scope doc, before any search:

1. **The hypothesis list overlaps itself.** C.7.a's claim text in HYPOTHESES-v5.md names "sex ratios"
   as one of *its* mechanisms, and cross-refs A.10. As written, a sex-ratio paper satisfies both
   entries. Without a rule, the same studies land in two chapters and the review double-counts.
   A.7 (marriage timing) is the *mediator* of most A.10 estimates, which is a second double-count
   channel; D.2.c (son preference) is the *upstream cause* of the Asian sex-ratio skew, which is a
   third.

2. **The sign is not fixed by the hypothesis.** Whether a skewed ratio raises or lowers fertility
   depends on which sex is scarce, whose fertility is measured (per-woman, per-man, aggregate
   births), and whether the channel is match probability or intra-marriage bargaining power — the
   Guttentag–Secord prediction runs opposite to the pure exposure prediction for the scarce sex.
   A pooled estimate is meaningless until a sign convention is pre-registered, as at TICK-026 for
   OAS.

3. **There is a standing PI prior to test, not assume.** Anup's marginal note in HYPOTHESES-v2.md
   (carried into the v5 `notes` field): A.10 is proximate, and "nobody thinks it has had a
   first-order effect on total fertility, because globally sex ratios tend to be close to the
   so-called natural rate — tell me if I'm wrong." That is a demographic-significance prediction
   stated in advance. The scope doc records it as a pre-registered prior and states the one
   substantive objection to its premise (the marriage-market-relevant ratio is not the sex ratio at
   birth), so §7 of the chapter tests it rather than inheriting it.

A fourth item is an escalation, not a scope decision: HYPOTHESES.md's own merge notes flag that
**war/conscription as a direct fertility shock is not enumerated anywhere in the review**. The
cleanest A.10 identification strategies (WWI/WWII cross-region military mortality) sit exactly on
that gap, so war-shock papers currently have no home chapter to route to.

## Acceptance criteria
- [ ] `sex-ratio-marriage-market-search-scope.md` written to `literature/search-logs/`, following the
      D.3.b scope structure: causal claim, boundary walls, estimand cells, eligibility rules,
      adjudication timing, expected shape of the evidence, cold-start channels + leakage wall.
- [ ] A wall vs C.7.a stated as an operational discriminator (headcount vs match-quality), not a
      description, and testable from a title/abstract where possible.
- [ ] A wall vs A.7 that states the double-counting hazard explicitly and names which chapter owns
      the estimate when marriage timing is the mediator.
- [ ] A wall vs D.2.c keyed on generational timing (parents' own fertility vs the skewed cohort's
      fertility ~20 years later).
- [ ] A pre-registered sign convention naming the reference direction, the denominator (whose
      fertility), and the rule for the mechanical composition effect that overlaps A.9.
- [ ] The PI's no-first-order-effect prior recorded verbatim as a testable prediction, with the
      operational-vs-birth sex-ratio objection stated.
- [ ] The war-shock enumeration gap escalated: a cell to catch those papers plus a note that the
      routing target does not exist yet.
- [ ] Scope frozen with a date and author line, matching the D.3.b convention.

## Log
- 2026-07-31 (Shravan/Claude): opened and claimed. No prior A.10 artifacts exist in
  `literature/search-logs/`, `extraction/`, or `output/chapters/`.
