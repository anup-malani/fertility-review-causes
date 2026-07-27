# TICK-048: D.3.b full-text retrieval and reconciliation
**Status:** open
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
- 2026-07-27 (Claude): opened.
