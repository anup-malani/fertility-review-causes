# TICK-016: OAS full-text data extraction
**Status:** blocked
**Assigned:** any
**Parallel-safe:** no
**Blocks:** TICK-017, TICK-018
**Blocked by:** TICK-015
**Touches:** extraction/old-age-security-pension-crowdout-studies.csv, extraction/old-age-security-pension-crowdout-effects.csv

## Description

Extract study-level and estimate-level data from included OAS full texts using `extraction/schema.md`.

## Acceptance criteria
- [ ] Study-level table exists with one row per included empirical study.
- [ ] Estimate-level table exists with one row per extractable estimate.
- [ ] Every numeric estimate has page/table/figure source information.
- [ ] RA verification sample is marked.
- [ ] Ambiguous estimates are flagged with `needs_pi = yes`.

## Log
<!-- Append completion note here when done. -->
