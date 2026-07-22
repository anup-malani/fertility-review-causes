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
- 2026-07-22 (Claude): Built `source/build/goldset/72_b1_retrieve_pdfs.py` — reproducible OA retrieval
  via OpenAlex (all locations) + Unpaywall fallback, %PDF magic-byte verification (rejects HTML paywall
  pages), idempotent. **Retrieved 19/95** open-access PDFs to the gitignored
  `literature/pdfs/evolutionary-sex-drive-contraceptive-decoupling/`. By stream:
  status_and_reproduction (Section 5.1, priority) **9/52**, desire_for_children 8/32,
  direct_decoupling 2/11. Remaining 76: 57 closed (no OA in OpenAlex or Unpaywall), 18 publisher
  bot-blocked (Atypon/Cloudflare return `<!DOCTYPE html>` even sandbox-off — confirmed genuine, not a
  sandbox artifact). This literature is Elsevier/Wiley/Springer/Duke/OUP/Royal Society/PNAS heavy with
  thin green OA, so ~20% is the automated ceiling. Retrieval log:
  `extraction/…-pdf-retrieval-log.csv`; full-text screen scaffold: `extraction/…-fulltext-screen.csv`.
  **Next lever for the paywalled remainder = authenticated browser (claude-in-chrome via Shravan's
  UChicago-proxied Chrome) or library access — the OAS-equivalent of Alexandra's retrieval step.**
  RA gate over the 95 pooling / 311 uncertain records still outstanding.
- 2026-07-22 (Claude, claude-in-chrome): drove Shravan's UChicago-authenticated Chrome to try the
  paywalled remainder. **Access confirmed** (EndNote Click "University of Chicago Library" widget; PDFs
  render with the campus IP watermark) and the fetch-blob-download primitive works (PNAS von Rueden
  W2507848855 retrieved, +1 over curl → **20/95 total, 10/52 status-and-reproduction**). **But browser
  automation does NOT scale against this publisher mix:** Elsevier/ScienceDirect (12 papers) and Royal
  Society (2) throw an interactive Cloudflare "Verify you are human" checkbox — bot-detection I am not
  permitted to complete; Wiley (7) returns HTTP 403 on the /doi/pdf(direct) endpoint even inside the
  authenticated session; the extension also gates screenshots per-domain (JS still runs). Only PNAS
  served the PDF inline/cleanly. Stopped rather than rabbit-hole. Handoff list of the 71 still-missing
  DOIs (all streams, status-and-reproduction first): `extraction/…-missing-pdf-dois.csv`. **Best next
  path = Shravan/RA via Zotero+UChicago proxy or the library's bulk get-it tools, or Shravan clicks the
  human-check where it appears; the automated ceiling here is ~20.**
