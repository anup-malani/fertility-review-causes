# TICK-048: D.3.b full-text retrieval and reconciliation
**Status:** partial — automated ceiling reached at 27/67; 22 of the 40 missing are free to read and merely bot-blocked
**Assigned:** any
**Parallel-safe:** yes (with the full-62 half of TICK-047)
**Blocks:** TICK-049
**Blocked by:** TICK-047 (decisive-12 half only)
**Touches:** source/build/goldset/82_d3b_retrieve_pdfs.py, source/build/goldset/83_d3b_ingest_pdfs.py, literature/pdfs/climate-anxiety-eco-doomerism/, extraction/climate-anxiety-eco-doomerism-pdf-retrieval-log.csv, extraction/climate-anxiety-eco-doomerism-fulltext-screen.csv

## Description

Retrieve full text for the two frozen pooling sets and confirm on full text that each study still
belongs to the stream the title-and-abstract screen assigned it. Mirror the B.1 pair
`72_b1_retrieve_pdfs.py` (OpenAlex all-locations + Unpaywall fallback, `%PDF` magic-byte verification
to reject HTML paywall pages, idempotent) and `74_b1_ingest_pdfs.py`.

**Priority order is not arbitrary and should not be reordered for convenience:** the 8
realized-fertility studies, then the 4 DESIRE_INDEPENDENCE studies, then the 62 stated-intention pool.
The first twelve are what the chapter's conclusion turns on.

**This ticket is expected to behave very differently from its B.1 analogue and the difference should be
measured, not assumed.** TICK-041 hit an automated ceiling at 20 of 95 because the B.1 corpus is
Elsevier/Wiley/Springer/Royal-Society heavy with thin green OA, and that ceiling now bounds the whole
B.1 chapter — its pooled estimate rests on 5 of 52 intended studies, selected by open-access
availability rather than at random. D.3.b's corpus looks structurally different: all 62 stated records
carry DOIs, and the decisive strata sit in PLoS ONE, BMC, Frontiers, Population and Environment,
Demographic Research, an MPIDR working paper, and Research Square. If the OA rate here is high, D.3.b
avoids the selection problem that caps B.1. If it is not, say so early and loudly — a low rate changes
what this chapter is allowed to claim, and it is better known on day one than at synthesis.

## Acceptance criteria
- [ ] `82_d3b_retrieve_pdfs.py` and `83_d3b_ingest_pdfs.py`, reproducible and idempotent, mirroring the
      B.1 scripts' structure.
- [ ] PDFs retrieved to the gitignored `literature/pdfs/climate-anxiety-eco-doomerism/`, with the
      realized-fertility 8 and desire-independence 4 attempted first.
- [ ] Retrieval log CSV: one row per DOI with outcome (retrieved / closed / bot-blocked), source
      location, and verification result.
- [ ] Retrieval rate reported **separately for the decisive 12 and the 62**, since a headline rate over
      the union would hide a gap in the stratum that matters.
- [ ] Full-text screen CSV: one row per retrieved study — stream confirmed / re-routed / excluded, with
      reason. Re-routed papers logged, not silently dropped.
- [ ] A missing-DOI handoff list produced for anything the automated path cannot reach, following the
      B.1 pattern, so a human with Zotero + the UChicago proxy can close the gap.

## Log
- 2026-07-27 (Claude): **automated ceiling reached at 27/67 distinct works. The decisive
  12 sits at 5/12, and that is the number that matters, not the headline.** Split as the
  ticket requires:

  | Band | Retrieved |
  |---|---|
  | realized_fertility | 4/8 |
  | desire_independence | **1/4** |
  | stated_intention | 22/55 |
  | full pool (distinct) | 27/67 |

  **The split reporting immediately earned its keep and my day-one expectation was
  wrong.** I predicted this corpus would avoid B.1's retrieval problem because it is
  recent and OA-heavy. The overall rate is indeed roughly double B.1's (40% vs 21%), but
  the decisive strata are *worse* than the headline, and desire-independence — the cell
  carrying the hypothesis's distinctive claim — came back 0/4 on the first run. A union
  rate would have reported "27/67, better than B.1" and hidden it.

  **A retriever defect was found and fixed mid-ticket, and it was not a paywall.** Three
  of the four desire-independence studies failed as `not_pdf_html_paywall` while OpenAlex
  reported them gold or diamond OA. Cause: OpenAlex returns `pdf_url: None` for those
  records and offers only landing pages (PMC, DOAJ, the bare DOI), so `candidate_urls()`
  was handed an HTML page and correctly rejected it. Free articles were being logged as
  unreachable. Fix = `derived_urls()`, which constructs PDF URLs deterministically from
  landing-page metadata: PMC article id → `/pdf/`, and DOI prefix `10.1371` → the PLoS
  `type=printable` file endpoint. The candidate cap was raised 6 → 10 so the derived URLs
  are not truncated away. This recovered the PLoS ONE study (desire-independence 0 → 1)
  and one stated study. **This is a bug pattern worth checking in the B.1 and OAS
  retrievers too: a `pdf_url`-only candidate list silently misreports gold OA as closed.**

  **What remains is a genuine block, not a missing construction.** PMC returns a 1.8 KB
  HTML interstitial to non-browser agents on `/pdf/`; Duke UP and Wiley refuse likewise.
  That is B.1's Cloudflare wall in a different costume and I stopped rather than fight it.

  **The handoff is materially better than B.1's and the ticket should not be read as a
  repeat.** Of the 40 missing, **22 are `oa_but_blocked` — free to read, refusing only a
  non-browser client — and 18 are genuinely `closed`.** The handoff CSV now carries an
  `access_class` column on that split, because the two need different work: the 22 need
  a human with an ordinary browser and no entitlement at all, while only the 18 need the
  UChicago proxy or ILL. B.1's 71-DOI handoff was mostly genuinely closed. Reporting
  these as one pile would overstate how much library access this chapter needs.

  Decisive-12 remainder, all seven:
  - `10.1111/jomf.70095` (Wiley, hybrid) — oa_but_blocked
  - `10.1111/padr.12646` (Wiley PDR, hybrid) — oa_but_blocked
  - `10.1111/sjpe.12125` (Wiley SJPE, green) — oa_but_blocked *(the growth model; may be
    set aside at the TICK-047 gate, in which case it is not needed)*
  - `10.1257/pandp.20251127` (AEA P&P) — closed *(the air-pollution study; same caveat)*
  - `10.1215/22011919-11713414` (Duke UP, diamond) — oa_but_blocked
  - `10.1016/j.joclim.2024.100346` (Elsevier/PMC, gold) — oa_but_blocked
  - `10.1080/23251042.2024.2408779` (T&F) — closed

  **Two of the four missing realized-fertility studies are exactly the two flagged for
  possible exclusion at the TICK-047 gate.** If the gate sets both aside, the empirical
  realized base is 6 and we hold 4 of 6 — so the gate should be run before any more
  retrieval effort is spent on those two DOIs.

  Next lever is a human with a browser against the 22 `oa_but_blocked` rows, desire-
  independence and realized first. Wiley (8 DOIs) is the single biggest cluster.
- 2026-07-27 (Claude): opened.
