# TICK-041: B.1 full-text screen and retrieval reconciliation
**Status:** partial — blocked on human library retrieval (automated ceiling reached at 20/95)
**Assigned:** any
**Parallel-safe:** no
**Blocks:** TICK-042
**Blocked by:** none (frozen screen set exists)
**Touches:** literature/pdfs/evolutionary-sex-drive-contraceptive-decoupling/, extraction/evolutionary-sex-drive-contraceptive-decoupling-fulltext-screen.csv

## Description

Take the 95-paper estimand-ready pooling set and the 311 uncertain records to full text. Priority is
the status-and-reproduction (proximate-ultimate) stream, which is the only poolable cell and the
quantitative core of the chapter. Retrieve PDFs, reconcile against the OpenAlex/Crossref identity in
the frozen screen, and confirm each retrieved study still belongs to its assigned stream on full text.

## Acceptance criteria
- [~] PDFs retrieved for the status-and-reproduction stream (Section 5.1 studies at minimum). **20 of 95 overall; 10 of 52 in this stream. Automated ceiling — see log.**
- [x] Full-text screen CSV with one row per retrieved study: stream confirmed / re-routed / excluded, with reason.
- [ ] The RA gate over the 95 pooling set + 311 uncertain records is recorded (per the OAS TICK-015 pattern). **Outstanding.**
- [x] Re-routed papers (to A.2 / A.4 / D.1.a) are logged, not silently dropped.

## Log
- 2026-07-25 (Claude): **This ticket is the binding constraint on the whole B.1 chapter and should not
  be closed.** Downstream work (TICK-042/034/035/036) was completed on the 20 PDFs that could be got
  automatically, which yielded 5 extractable studies. So the chapter's pooled estimate rests on 5 of
  the 52 status-and-reproduction studies the frozen screen identified — a 10% sample of the intended
  pool, chosen by what happens to be open-access rather than at random. Open-access availability
  plausibly correlates with study age, publisher, and field, so this is a potential selection problem
  on top of a precision problem, and the chapter should not be sent outside the team without either
  widening retrieval or stating the limit explicitly.
  **What unblocks it:** the 71 DOIs in `extraction/…-missing-pdf-dois.csv`, retrieved by a human via
  Zotero + the UChicago proxy or the library's bulk tools. Status-and-reproduction DOIs first — those
  are the only ones that change the pooled numbers.
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
