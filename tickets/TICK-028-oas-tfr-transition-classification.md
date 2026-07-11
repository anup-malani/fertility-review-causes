# TICK-028: OAS TFR-based transition classification
**Status:** done
**Assigned:** Codex
**Parallel-safe:** no
**Blocks:** TICK-019
**Blocked by:** none
**Touches:** source/analysis/oas_transition_classification.py, source/analysis/test_oas_transition_classification.py, output/tables/old-age-security-pension-crowdout-tfr-transition-classification.csv, output/chapters/old-age-security-pension-crowdout.md

## Description

Use TFR data from Alexandra's local `proximate-causes` directory as read-only input to classify
OAS study windows by above/below replacement fertility. Store all derived data and scripts in the
current `fertility-review-causes` repository.

## Acceptance criteria
- [x] No files are written in `proximate-causes`.
- [x] The classifier reads UN TFR from `proximate-causes` and keeps derived outputs in this repo.
- [x] Output table records start/end TFR, replacement status, classification, source, and caveats.
- [x] Historical cases with no TFR coverage are flagged instead of silently guessed.
- [x] Tests cover above-replacement, below-replacement, crossing, and missing-TFR cases.

## Log
<!-- Append completion note here when done. -->
- 2026-07-11 Codex: Added read-only UN TFR classifier, generated `output/tables/old-age-security-pension-crowdout-tfr-transition-classification.csv`, and updated the chapter with the above/below-replacement transition classifications.
- 2026-07-11 Codex: Promoted the rule to
  `decisions/2026-07-11-tfr-replacement-transition-classification.md` and cross-referenced it from
  the protocol, pipeline design, RA playbook, chapter template, and OAS demographic-significance
  ticket.
