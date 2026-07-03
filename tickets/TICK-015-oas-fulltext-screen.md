# TICK-015: OAS full-text screen and retrieval reconciliation
**Status:** blocked
**Assigned:** any
**Parallel-safe:** no
**Blocks:** TICK-016
**Blocked by:** RA review decisions in `output/old-age-security-pension-crowdout-ra-review.csv`
**Touches:** extraction/old-age-security-pension-crowdout-fulltext-screen.csv, literature/pdfs/old-age-security-pension-crowdout/, output/old-age-security-pension-crowdout-pdf-wantlist.md

## Description

After RA title/abstract review is complete, reconcile `RETRIEVE` decisions against the local PDF
folder and screen retrieved full texts for empirical/theory inclusion.

## Acceptance criteria
- [ ] All `RETRIEVE` rows have `available`, `needs_manual`, `not_found`, or `bad_file` PDF status.
- [ ] Missing PDFs are listed in a revised want-list.
- [ ] Full-text decisions are recorded as `INCLUDE_EMPIRICAL`, `INCLUDE_THEORY`, `EXCLUDE`, or `UNSURE_PI`.
- [ ] Exclusions have a short reason.
- [ ] Output committed.

## Log
<!-- Append completion note here when done. -->
