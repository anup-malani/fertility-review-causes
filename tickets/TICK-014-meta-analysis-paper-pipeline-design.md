# TICK-014: Design meta-analysis-to-paper pipeline
**Status:** done
**Assigned:** Alexandra/Codex
**Parallel-safe:** yes
**Blocks:** TICK-015, TICK-016, TICK-017, TICK-018, TICK-019
**Blocked by:** none
**Touches:** docs/meta-analysis-paper-pipeline-design.md, docs/meta-analysis-effect-size-harmonization.md, output/chapters/hybrid-chapter-template.md, extraction/

## Description

Design the post-search pipeline that turns RA-reviewed papers and retrieved PDFs into a hybrid
JEL-style / Cochrane-style chapter or paper. The design should use the local reference corpus,
the existing protocol, and the OAS pilot artifacts, while remaining general enough for later
hypotheses.

## Acceptance criteria
- [ ] Pipeline design document exists and names required inputs, outputs, and gates.
- [ ] Extraction schema and OAS extraction template exist.
- [ ] Effect-size harmonization rules exist with explicit units and escalation triggers.
- [ ] Hybrid chapter template exists.
- [ ] Downstream tickets exist for full-text screen, extraction, risk of bias, meta-analysis,
      demographic significance, and chapter drafting.

## Log
2026-07-03 — Alexandra/Codex: Added the meta-analysis-to-paper pipeline design, extraction schema
and OAS template, effect-size harmonization rules, hybrid chapter template, and downstream tickets
for full-text screening through chapter drafting.
