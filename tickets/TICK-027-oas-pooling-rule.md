# TICK-027: OAS conservative pooling rule
**Status:** done
**Assigned:** Codex
**Parallel-safe:** no
**Blocks:** TICK-019
**Blocked by:** none
**Touches:** source/analysis/oas_meta_pipeline.py, source/analysis/test_oas_meta_pipeline.py, output/tables/old-age-security-pension-crowdout-*.csv, output/chapters/old-age-security-pension-crowdout.md

## Description

Implement the recommended conservative pooling rule for the OAS quantitative synthesis. A group
is eligible for coefficient pooling only when rows share the same mechanism cell, outcome family,
harmonized outcome unit, harmonized treatment scale, and usable oriented effect/SE, with at
least three independent studies. Otherwise the group remains
screening-only or narrative-only.

## Acceptance criteria
- [x] The pooling rule is encoded in the analysis pipeline rather than only described in prose.
- [x] Readiness output reports recommended synthesis status and rationale.
- [x] No grand pooled estimate is produced across incompatible treatment scales or outcomes.
- [x] Chapter text explains the recommended rule and its consequence for the current OAS rows.
- [x] Tests cover a poolable same-scale group and an incompatible mixed-scale group.

## Log
<!-- Append completion note here when done. -->
- 2026-07-11 Codex: Adopted conservative same-scale pooling rule, added readiness columns for recommended synthesis and recommended pooled estimates, documented the rule in `decisions/`, and updated the chapter to treat current coefficient evidence as structured quantitative narrative because candidate families mix treatment scales.
