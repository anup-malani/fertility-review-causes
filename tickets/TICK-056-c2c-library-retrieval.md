# TICK-056: C.2.c library retrieval of the 59 missing PDFs — needs a human with Zotero + UChicago proxy
**Status:** open
**Assigned:** Shravan or Alexandra
**Parallel-safe:** yes (no overlap with the D.3.b or B.1 chains)
**Blocks:** C.2.c extraction, risk of bias, meta-analysis, chapter
**Blocked by:** none — the automated ceiling is already hit
**Touches:** literature/pdfs/housing-costs/, extraction/housing-costs-retrieval-handoff.csv, extraction/housing-costs-pdf-retrieval-log.csv

## Description

Automated open-access retrieval for C.2.c is exhausted at **19/78 overall and 4/15 on the identified
core**. Three passes were run and each is documented in
`extraction/housing-costs-pdf-retrieval-report.md`: direct OA links, preprint-twin siblings, and OA
landing pages via `citation_pdf_url`. The ceiling matches B.1's (20/95) closely enough to suggest it
is a property of the literature and the OA infrastructure rather than of the scripts.

**The binding problem is that the identified studies are the closed ones.** The 15 quasi-experimental
papers sit in *Journal of Public Economics*, *Review of Economics and Statistics*, *Economic Inquiry*,
*Review of Economic Studies* and *Journal of Health Economics*. Eleven are still missing. Until they
are in hand:

- no pooled estimate can be produced;
- the `id_strength` labels cannot be confirmed, because QUASI_EXP vs ASSOCIATIONAL was assigned from
  titles and abstracts — so **the identified-vs-associational split itself is provisional**;
- the tenure-conditioning, parity, and tempo-vs-quantum fields the scope requires are all full-text
  facts and cannot be filled.

This is the same wall B.1 hit at TICK-041, where the pooled estimate rested on 5 studies until a human
moved it.

## Worklist

`extraction/housing-costs-retrieval-handoff.csv` — all 59 missing records, **priority-ordered with the
11 QUASI_EXP first**, each carrying its DOI link, OA status, and the specific reason automation
failed (`closed`, `publisher blocked automated fetch (403)`, `link returned HTML, not a PDF`, …).
Columns `retrieved_by` / `retrieved_date` / `notes` are there to be filled in as you go.

Retrieve the 11 QUASI_EXP first. They are the chapter; the remaining 48 are the associational stratum
and can follow.

## Acceptance criteria
- [ ] All 11 missing QUASI_EXP records retrieved, or each recorded as genuinely unobtainable with the
      route tried.
- [ ] PDFs land in `literature/pdfs/housing-costs/` as `W<id>__<title-slug>.pdf`, matching the
      convention already used by the 19 retrieved files.
- [ ] `housing-costs-pdf-retrieval-log.csv` updated so the log and the directory cannot drift.
- [ ] **The two `version=preprint_twin` files reconciled against their published versions**
      (`10.1016/j.jpubeco.2021.104366`, and the asymmetric-housing-wealth paper). Specifications
      change between working paper and article; neither may supply an extracted number until checked.
- [ ] Retrieval rate reported by stratum, since a systematically lower rate for the associational
      stratum would bias the chapter toward the identified studies — which is the *right* direction
      substantively, but must be stated rather than happen silently.

## Log
- 2026-07-31 (Shravan/Claude): opened. Automated ceiling reached at 19/78 (4/15 priority) after three
  passes. Report: `extraction/housing-costs-pdf-retrieval-report.md`.
