# TICK-032: B.1 full-text screen and retrieval reconciliation
**Status:** open
**Assigned:** any
**Parallel-safe:** no
**Blocks:** TICK-033
**Blocked by:** none (frozen screen set exists)
**Touches:** literature/pdfs/evolutionary-sex-drive-contraceptive-decoupling/, extraction/evolutionary-sex-drive-contraceptive-decoupling-fulltext-screen.csv

## Description

Take the 95-paper estimand-ready pooling set and the 311 uncertain records to full text. Priority is
the status-and-reproduction (proximate-ultimate) stream, which is the only poolable cell and the
quantitative core of the chapter. Retrieve PDFs, reconcile against the OpenAlex/Crossref identity in
the frozen screen, and confirm each retrieved study still belongs to its assigned stream on full text.

## Acceptance criteria
- [ ] PDFs retrieved for the status-and-reproduction stream (Section 5.1 studies at minimum).
- [ ] Full-text screen CSV with one row per retrieved study: stream confirmed / re-routed / excluded, with reason.
- [ ] The RA gate over the 95 pooling set + 311 uncertain records is recorded (per the OAS TICK-015 pattern).
- [ ] Re-routed papers (to A.2 / A.4 / D.1.a) are logged, not silently dropped.

## Log
<!-- Append completion note here when done. -->
