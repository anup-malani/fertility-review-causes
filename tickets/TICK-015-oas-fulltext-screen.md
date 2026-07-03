# TICK-015: OAS full-text screen and retrieval reconciliation
**Status:** done
**Assigned:** Codex
**Parallel-safe:** no
**Blocks:** TICK-016
**Blocked by:** resolved; RA review decisions exist in `output/old-age-security-pension-crowdout-ra-review.csv`
**Touches:** extraction/old-age-security-pension-crowdout-fulltext-screen.csv, literature/pdfs/old-age-security-pension-crowdout/, output/old-age-security-pension-crowdout-pdf-wantlist.md

## Description

After RA title/abstract review is complete, reconcile `RETRIEVE` decisions against the local PDF
folder and screen retrieved full texts for empirical/theory inclusion.

## Acceptance criteria
- [x] All `RETRIEVE` rows have `available`, `needs_manual`, `not_found`, or `bad_file` PDF status.
- [x] Missing PDFs are listed in a revised want-list.
- [x] Full-text decisions are recorded as `INCLUDE_EMPIRICAL`, `INCLUDE_THEORY`, `EXCLUDE`, or `UNSURE_PI`.
- [x] Exclusions have a short reason.
- [x] Output committed.

## Log
<!-- Append completion note here when done. -->
- 2026-07-03: Claimed by Codex after RA review and local PDF retrieval completed.
- 2026-07-03: Completed PDF reconciliation and full-text screen for 10 RA-retrieved papers; no missing PDFs remain. Added study-level skeleton with external-validity/transportability fields.
