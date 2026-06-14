# TICK-012: Pre-pilot — full pipeline on time-cost / income-substitution
**Status:** blocked
**Assigned:** Anup + Claude
**Parallel-safe:** no
**Blocks:** TICK-010
**Blocked by:** TICK-001, TICK-009

## Description

Run the full 17-stage pipeline privately (Anup + Claude, no RAs) on the time-cost /
income-substitution hypothesis. Purpose: implement and debug the pipeline before RAs
see it; learn which stages require PI judgment vs can be delegated.

**Hypothesis:** Children take time, and the primary time cost falls on women. As women's
wages rise, the opportunity cost (shadow price) of having children rises. The substitution
effect (children become more expensive) tends to dominate the income effect (higher income
makes children more affordable), resulting in falling fertility as incomes and wages rise.
Grounded in Becker (1965) time-allocation model and Mincer (1963) female labor supply.

**Note on overlap:** this hypothesis is closely related to "women's opportunity cost / female
labor force participation" in HYPOTHESES.md. After TICK-001 is done, verify they are
differentiated cleanly. The time-cost framing emphasizes the theoretical mechanism (time
budget + income vs substitution effects); the FLFP framing emphasizes the empirical
phenomenon. May be the same slug or may need to be two distinct entries.

**Slug to use:** `time-cost-income-substitution` (confirm or adjust after TICK-001)

**Output:** `output/chapters/time-cost-income-substitution.md`

**After completing this ticket:** document pipeline lessons in `decisions/` before
starting the RA pilot (TICK-010). Key questions to answer:
- Which stages are PI-judgment vs RA-delegable?
- What does "done" look like at each stage? (concretize for RA instructions)
- What failed or was unclear in the workflow scripts?
- What did PROTOCOL.md underspecify?

## Acceptance criteria
- [ ] `literature-search.mjs` run on this hypothesis
- [ ] All pipeline stages completed (or explicitly deferred with reason)
- [ ] Chapter written to `output/chapters/time-cost-income-substitution.md`
- [ ] Pipeline lessons documented in `decisions/2026-06-14-prepilot-lessons.md`
- [ ] TICK-010 (RA pilot) unblocked — Anup has a clear sub-task list for RAs

## Log
<!-- Append completion note here when done. -->
