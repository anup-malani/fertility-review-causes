# OAS Quantitative Meta-Analysis Design

**Date:** 2026-07-09  
**Status:** Approved by Alexandra for implementation  
**Scope:** Old-age-security / pension crowd-out of fertility chapter

## Goal

Turn `output/chapters/old-age-security-pension-crowdout.md` from a narrative first draft into a
quantitative, audit-traceable meta-analysis chapter where the data support pooling only when the
estimands are coherent.

## Approved Approach

Use an audit-first quantitative synthesis.

1. Extract effect estimates from the retrieved PDFs into
   `extraction/old-age-security-pension-crowdout-effects.csv`.
2. Generate an exception-based RA verification sheet at
   `output/old-age-security-pension-crowdout-effect-extraction-review.csv`.
3. Assess risk of bias in
   `extraction/old-age-security-pension-crowdout-risk-of-bias.csv`.
4. Harmonize effects conservatively into
   `output/tables/old-age-security-pension-crowdout-harmonized-effects.csv`.
5. Define poolable groups explicitly and run quantitative synthesis only where estimates share a
   coherent outcome, treatment scale, follow-up window, and mechanism cell.
6. Update the chapter with extracted estimates, poolability decisions, risk-of-bias summary,
   summary-of-findings language, and demographic-significance status.

## Core Design Decisions

- Preserve original estimates. Harmonized columns are additional fields, never replacements.
- Do not pool Cell A old-age-security-motive estimates with Cell C grandparental-childcare estimates.
- Do not pool mechanism-only Cell B or indirect Cell D evidence with fertility estimates.
- If estimates are heterogeneous in outcome or treatment scale, produce a quantitative evidence table
  and structured narrative synthesis rather than a misleading pooled estimate.
- Every numeric claim in the chapter must trace to an effect row with a PDF page, table, or figure
  locator.
- RA verification uses the existing exception-based convention: blank RA decision cells mean approved.

## Outputs

| Output | Purpose |
|---|---|
| `extraction/old-age-security-pension-crowdout-effects.csv` | Source-of-truth estimate-level extraction table. |
| `output/old-age-security-pension-crowdout-effect-extraction-review.csv` | RA-facing effect verification sheet. |
| `extraction/old-age-security-pension-crowdout-risk-of-bias.csv` | ROBINS-I-inspired study risk-of-bias table. |
| `output/tables/old-age-security-pension-crowdout-harmonized-effects.csv` | Original and harmonized effects plus poolability decisions. |
| `output/tables/old-age-security-pension-crowdout-meta-analysis-summary.csv` | Pooled estimates where valid, or explicit no-pooling rationale. |
| `output/tables/old-age-security-pension-crowdout-summary-of-findings.csv` | GRADE-style chapter summary rows. |
| `output/figures/old-age-security-pension-crowdout-evidence-map.csv` | Lightweight evidence-map data if forest plots are not justified. |
| `output/chapters/old-age-security-pension-crowdout.md` | Updated quantitative chapter. |

## Implementation Constraints

- Follow `extraction/schema.md` and `docs/meta-analysis-effect-size-harmonization.md`.
- Use the retrieved PDFs in `literature/pdfs/old-age-security-pension-crowdout/` as the evidence
  source for numeric extraction.
- Keep grandparental-childcare studies as a separate Cell C track. If their PDFs are missing, the
  chapter should state that SDT quantitative synthesis is pending retrieval/extraction.
- Keep China-specific SDT relevance flagged as policy-constrained.
- Commit in coherent increments after tests or validation checks.

## Validation

- CSVs must parse with Python `csv.DictReader`.
- Required schema columns must be present.
- Every extracted numeric effect must have `extract_page`, `extract_quote_or_note`, and `needs_pi`.
- Harmonized outputs must retain non-poolable rows with a reason.
- The chapter must not claim a pooled effect unless the meta-analysis summary table contains one.
