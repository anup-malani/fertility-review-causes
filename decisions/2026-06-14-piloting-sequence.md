# Decision: Piloting sequence before RA parallel tracks

**Date:** 2026-06-14  
**Decided by:** Anup Malani

---

## Decision

Run the pipeline in three phases before scaling to full parallel tracks:

| Phase | Who | Hypothesis | Purpose |
|-------|-----|-----------|---------|
| Pre-pilot | Anup + Claude | Time-cost / income-substitution | Implement and debug the full pipeline privately; learn what is PI-judgment vs RA-delegable |
| RA pilot (Phase 1) | All three | Old-age security / pensions | Teach RAs the pipeline on a clean, intuitive hypothesis; calibrate together |
| Phase 2 | RAs independently | Separate hypotheses | Parallel tracks at scale |

---

## Rationale

### Why a pre-pilot at all?

All workflow stubs throw on invocation. Someone has to implement and debug them before anyone runs the pipeline. Doing it with just Anup and Claude means failures are invisible to RAs and do not undermine their confidence in the process. The pre-pilot also answers a question PROTOCOL.md cannot answer alone: which of the 17 pipeline stages require PI judgment, and which can be delegated to an RA with a clear checklist? That answer is needed before sub-tasks can be assigned in the RA pilot.

### Why time-cost / income-substitution for the pre-pilot?

Mid-complexity. Clear theoretical grounding (Becker 1965 time-allocation model; Mincer 1963 female labor supply): children take time, women bear the primary time cost, so as women's wages rise the shadow price of children rises and fertility falls. The income effect and substitution effect work in opposite directions, and the empirical question is which dominates. Literature is manageable, not overwhelming. Close cousin to the women's opportunity cost hypothesis — check HYPOTHESES.md for overlap after TICK-001 is done; may need to differentiate the slugs.

### Why old-age security / pensions for the RA pilot?

Also mid-complexity but more intuitive and requires no prior economics. Clear theory (children as old-age insurance → state pensions crowd that out), manageable literature (~30-60 papers), mix of study designs. Also has a useful pedagogical moment: the narrow reading (state pensions specifically) is FDT/SDT; the broader reading (children as old-age support) is PM through SDT. Good for teaching RAs how to apply phenomena codes carefully.

### Why not Q-Q tradeoff?

High-complexity: enormous literature, many theoretical offshoots (endogenous growth, human capital), multiple sub-debates. Wrong vehicle for teaching the pipeline. Remains on the hypothesis list; will be evaluated in Phase 2.

---

## Sequence within the pre-pilot

1. TICK-001: Anup finishes HYPOTHESES.md review (goal: before noon 2026-06-14)
2. TICK-009: implement `literature-search.mjs`; run on time-cost/income-substitution
3. TICK-012: run full pre-pilot pipeline; produce `output/chapters/time-cost-income-substitution.md`
4. Capture pipeline lessons in `decisions/`
5. TICK-010: RA pilot Phase 1 on old-age security (blocked until TICK-012 done)
