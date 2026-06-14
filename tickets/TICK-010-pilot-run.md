# TICK-010: Run pilot on quantity-quality tradeoff
**Status:** blocked
**Assigned:** any
**Parallel-safe:** no (sequential pipeline)
**Blocks:** —
**Blocked by:** TICK-009

## Description

Run the full 17-stage pipeline (PROTOCOL.md §5) on the pilot hypothesis `quantity-quality-
tradeoff`. This is the calibration run before scaling to all 65 hypotheses.

**Why this hypothesis:** seminal theory (Becker-Lewis 1973), credible quasi-experimental
empirics (Black-Devereux-Salvanes 2005, Angrist-Lavy-Schlosser 2010), exercises every
methodological step.

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

**Output:** `output/chapters/quantity-quality-tradeoff.md` — the first complete chapter.

## Acceptance criteria
- [ ] All pipeline workflow stubs implemented for the pilot hypothesis
- [ ] Chapter written to `output/chapters/quantity-quality-tradeoff.md`
- [ ] Chapter passes lay-readability check
- [ ] Lessons from pilot captured in `decisions/`
- [ ] Committed

## Log
<!-- Append completion note here when done. -->
