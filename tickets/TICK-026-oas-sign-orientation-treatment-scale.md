# TICK-026: OAS sign orientation and treatment-scale coding
**Status:** done
**Assigned:** Codex
**Parallel-safe:** no
**Blocks:** TICK-019
**Blocked by:** none
**Touches:** source/analysis/oas_meta_pipeline.py, source/analysis/test_oas_meta_pipeline.py, output/tables/old-age-security-pension-crowdout-*.csv, output/chapters/old-age-security-pension-crowdout.md

## Description

Assume PI approval for the previously flagged OAS effect rows and code sign orientation plus
harmonized treatment-scale labels. Oriented effects should mean the fertility effect of more
non-child old-age security.

## Acceptance criteria
- [x] Harmonized effects include PI-assumption, OAS direction, oriented effect/SE, orientation method, and treatment-scale columns.
- [x] Pension-cut estimates are sign-flipped when oriented to "more OAS".
- [x] Readiness output uses oriented effects and treats `needs_pi` rows as resolved under the PI-approval assumption.
- [x] Chapter describes what sign orientation changes and what still blocks pooling.
- [x] Tests cover sign orientation and readiness PI-resolution behavior.

## Log
<!-- Append completion note here when done. -->
- 2026-07-11 Codex: Added PI-assumed approval, OAS treatment direction, sign-oriented effects, harmonized treatment-scale labels, oriented readiness screening fields, and chapter text clarifying that pooling remains blocked by treatment-scale/follow-up/target-setting comparability.
