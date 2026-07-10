# TICK-016: OAS full-text data extraction
**Status:** done
**Assigned:** Codex
**Parallel-safe:** no
**Blocks:** TICK-017, TICK-018
**Blocked by:** resolved; TICK-015 completed on 2026-07-03
**Touches:** extraction/old-age-security-pension-crowdout-studies.csv, extraction/old-age-security-pension-crowdout-effects.csv

## Description

Extract study-level and estimate-level data from included OAS full texts using `extraction/schema.md`.

## Acceptance criteria
- [ ] Study-level table exists with one row per included empirical study.
- [ ] Estimate-level table exists with one row per extractable estimate.
- [ ] Every numeric estimate has page/table/figure source information.
- [ ] RA verification tables use adjacent value / RA decision / RA notes columns; blank RA decisions mean approved.
- [ ] Ambiguous estimates are flagged with `needs_pi = yes`.

## Log
<!-- Append completion note here when done. -->
- 2026-07-03: Claimed by Codex. First subtask is to add exception-based RA verification tables for study-level and effect-level extraction fields.
- 2026-07-09: Alexandra completed the study-level RA review sheet. No nonblank RA decision flags
  were present, so reviewed fields were treated as approved by default and synced back to
  `extraction/old-age-security-pension-crowdout-studies.csv`.
- 2026-07-09: Effect-level extraction table and RA verification sheet completed for current
  retrieved OAS PDFs. Extracted 10 main effects with PDF page/table locators; two rows are marked
  `needs_pi = yes` for missing uncertainty or estimand interpretation.
