# TICK-010: Run pilot on old-age security / pensions
**Status:** blocked
**Assigned:** any
**Parallel-safe:** no (sequential pipeline)
**Blocks:** —
**Blocked by:** TICK-012

## Description

Run the full 17-stage pipeline (PROTOCOL.md §5) on the pilot hypothesis `old-age-security-pensions`.
This is the calibration run before scaling to all 65 hypotheses.

**Why this hypothesis:** mid-complexity — clear, bounded theory; manageable literature
(~30-60 core papers); mix of study designs that exercises the risk-of-bias rubric; RAs can
follow it without prior economics background. The phenomena question is also pedagogically
useful: the narrow reading (state pensions crowd out child-as-insurance motive) is FDT/SDT
only; the broader reading (children as old-age support) is relevant PM through SDT.

Q-Q tradeoff was the original choice but is high-complexity (enormous literature, many
theoretical offshoots). It stays on the hypothesis list and will be evaluated in Phase 2.

**Seminal references to seed the search:** Caldwell 1976, Neher 1971, Cigno & Rosati 1992,
Boldrin & Jones 2002, Boldrin et al. 2005, Pay-as-you-go pension expansion studies.

**Stages to run (implement each workflow stub before invoking):**
1. `literature-search.mjs` ← TICK-009 (done)
2. `screen-titles-abstracts.mjs`
3. `acquire-pdfs.mjs`
4. `extract-data.mjs`
5. `risk-of-bias.mjs`
6. `meta-analyze.mjs`
7. `demographic-significance.mjs`
8. `grade-rating.mjs`
9. `synthesize-chapter.mjs`
10. `lay-readability-check.mjs`
11. `cross-chapter-check.mjs`

**Output:** `output/chapters/old-age-security-pensions.md` — the first complete chapter.

## Acceptance criteria
- [ ] All pipeline workflow stubs implemented for the pilot hypothesis
- [ ] Chapter written to `output/chapters/old-age-security-pensions.md`
- [ ] Phenomena handled correctly (narrow vs broad reading documented)
- [ ] Chapter passes lay-readability check
- [ ] Lessons from pilot captured in `decisions/`
- [ ] Committed

## Log
<!-- Append completion note here when done. -->
