# TICK-047: D.3.b RA gate over boundary calls and unscreenable records
**Status:** open
**Assigned:** Shravan
**Parallel-safe:** no (gates the decisive 12; the full-62 pass is parallel-safe with TICK-048)
**Blocks:** TICK-048, TICK-049
**Blocked by:** none (frozen screen exists)
**Touches:** extraction/climate-anxiety-eco-doomerism-ra-gate.csv, literature/search-logs/climate-anxiety-eco-doomerism-ra-gate-log.md

## Description

The D.3.b screen verdicts are AUTOMATED. Before anything is retrieved or extracted, a human signs off
on the boundary calls and resolves the records that could not be screened from title alone. This is the
step the screen report names as "the remaining human step (the RA gate)" and the run-state note names
as the next executable step.

Two populations need the gate, and they are not equally urgent:

1. **The decisive 12** — the 8 realized-fertility studies and the 4 DESIRE_INDEPENDENCE studies. The
   chapter's conclusion turns on these. They must be gated before TICK-049 extraction begins.
2. **The remainder** — 125 UNCERTAIN records, 122 marked `INSUFFICIENT_INFO`, and the 62-study
   stated-intention pool. This pass can run alongside TICK-048 retrieval.

**Sample Wall 1 (D.1.a postmaterialism) misroutes first.** 50 records routed `OFF_POSTMATERIALIST_D1a`.
The left-politics/education/secularism confound is simultaneously the Wall 1 routing rule and the
chapter's central identification threat, which means a misrouted study and a confounded estimate are
the same error. This is where a screening mistake costs the most downstream.

Two classification calls inside the realized-fertility 8 are already known and should be decided here
rather than discovered at extraction:

- `10.1111/sjpe.12125` (Scottish J. Political Economy 2017) is a formal endogenous-growth model with no
  empirical realized fertility in it. Almost certainly belongs in the theory stream.
- `10.1257/pandp.20251127` (AEA P&P 2025) identifies from air-pollution exposure, not expressed
  ecological dread — the exact case precision-rule 3 was written to exclude.

If both are set aside the empirical realized base is 6, two of them not peer-reviewed. That number
propagates into Sections 1, 5.2, 10, and 12 of the chapter, so record the decision explicitly.

## Acceptance criteria
- [ ] Gate CSV with one row per gated record: screen verdict, RA verdict, agree/overturn, reason.
- [ ] All 12 decisive studies (8 realized + 4 desire-independence) gated, with the two flagged
      classification calls resolved and their effect on the counts recorded.
- [ ] A Wall 1 misroute sample drawn from the 50 `OFF_POSTMATERIALIST_D1a` records, with the sample
      size and selection rule stated, not chosen ad hoc.
- [ ] The 122 `INSUFFICIENT_INFO` records dispositioned: resolved to a cell, sent to full text, or
      excluded with reason.
- [ ] Overturn rate reported by wall (D.1.a / D.3.a / C.5.a), since that rate is the honest measure of
      how much the automated screen can be trusted in the chapter's §13 appendix.
- [ ] Any pool-count change written back to `output/climate-anxiety-eco-doomerism-screen-report.md`
      rather than only into the chapter, so the generated report and the prose cannot drift.

## Log
- 2026-07-27 (Claude): opened. Precondition verified — all 62 stated-intention records carry DOIs, and
  the frozen pooling sets are `output/climate-anxiety-eco-doomerism-estimand-ready-{stated,realized}.json`.
