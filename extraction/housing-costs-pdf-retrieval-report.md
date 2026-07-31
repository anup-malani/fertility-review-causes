# PDF retrieval report — housing costs (C.2.c)

**Run:** 2026-07-31, Shravan (TICK-055)  ·  **Log:** `extraction/housing-costs-pdf-retrieval-log.csv`
**Handoff worklist:** `extraction/housing-costs-retrieval-handoff.csv`

---

## 1. Result

| | retrieved | of | rate |
|---|---|---|---|
| **QUASI_EXP (priority)** | **4** | 15 | 27% |
| All gated PRIMARY | 19 | 78 | 24% |

Three passes were run, each targeting a different failure mode:

1. **Direct OA** (`retrieve_pdfs.py`) — `best_oa_location.pdf_url` and every `locations[]` PDF. 13 files.
2. **Preprint twins** (`retrieve_via_twins.py`) — the dedup step showed NBER/SSRN/RePEc carry *separate* OpenAlex records for the same study, so the published record's `locations` never lists the working paper. Searching by title and trying siblings recovered 2 more. **The twin phenomenon was a hazard at dedup; here it is a retrieval route.**
3. **OA landing pages** (`retrieve_via_landing.py`) — 19 records were `is_oa=true` with an *empty* `pdf_url`, which is a missing field rather than a paywall. Following `<meta name="citation_pdf_url">` recovered 4 more.

**This is the automated ceiling.** It matches B.1's experience (20/95, 21%) almost exactly, which is evidence the ceiling is a property of the literature and the OA infrastructure, not of the script.

## 2. Why the priority set is the hard part

The 15 identified studies are concentrated in exactly the venues that do not open: *Journal of Public Economics*, *Review of Economics and Statistics*, *Economic Inquiry*, *Review of Economic Studies*, *Journal of Health Economics*. Of the 11 still missing, 7 are `closed`, 2 `hybrid`, 2 `green`-but-unresolvable.

The associational stratum retrieves no better, and often worse — much of it is in Chinese and Korean journals with no OA route at all.

## 3. Handoff — needs a human with Zotero + the UChicago proxy

`housing-costs-retrieval-handoff.csv` lists all 59 missing records, **priority-ordered with the 11 QUASI_EXP first**, each with its DOI link, OA status, and the specific reason automation failed. Columns `retrieved_by` / `retrieved_date` / `notes` are there to be filled in.

**The 11 missing QUASI_EXP, in priority order — these are the chapter:**

| Year | Venue | Title | OA |
|---|---|---|---|
| 2010 | Economic Inquiry | THE EFFECT OF HOUSE PRICE ON FERTILITY: EVIDENCE FROM HONG KON | closed |
| 2015 | DOAJ (DOAJ: Directory of Open  | The Effect of House Prices on Fertility: Evidence from Canada | green |
| 2015 | Urban Studies | Do housing options affect child birth decisions? Evidence from | closed |
| 2019 | Journal of Policy Modeling | The long-term consequences of youth housing for childbearing a | hybrid |
| 2020 | International Regional Science | Do House Prices Affect Fertility Behavior in China? An Empiric | closed |
| 2022 | 국토계획 | The Effect of Public Rental Housing on Birth Interval of Newly | closed |
| 2024 | Population Space and Place | House prices and fertility: Can the Dutch housing crisis expla | hybrid |
| 2024 | Labour Economics | Do surging house prices discourage fertility? Global evidence, | closed |
| 2024 | SSRN Electronic Journal | The Effect of House Prices on Fertility: Evidence from House P | green |
| 2024 | Journal of Health Economics | Housing wealth, fertility and children's health in China: A re | closed |
| 2026 | Proceedings of the National Ac | Can stimulating ownership increase fertility: Evidence from ho | hybrid |

## 4. A caveat on the two twin-sourced files

Two PDFs were retrieved from a **working-paper twin**, not the published article (logged `version=preprint_twin`). Tables and specifications routinely change between versions. **Neither may supply an extracted number until it is reconciled against the published version** — flagged rather than silently treated as equivalent.

## 5. What this means for sequencing

Extraction cannot start on the identified core: 4 of 15 studies in hand. The `id_strength` labels are also unconfirmed until full text, so **both the pooled estimate and the identified-vs-associational split are currently retrieval-bound** — the same position B.1 reached at TICK-041, where the pooled estimate rested on 5 studies until a human moved it. This should be a ticket with a named owner rather than a line in a report.
