# Decision: Two-axis boolean query (CAUSE × FERTILITY); mechanism AND dropped

**Date:** 2026-06-20
**Status:** Adopted

## Context

The initial `literature-search.mjs` dry-run on `old-age-security-pension-crowdout` produced a three-axis boolean query: CAUSE × FERTILITY × MECHANISM, where the mechanism axis included terms like "crowding out," "substitut*," "insurance motive," "old-age support," "intergenerational transfer," "value of children." The tool added this axis to reduce false positives (fiscal pension papers, demographic projections).

## Calibration test

Gold-standard set of 12 known seminal papers (Neher 1971, Nugent 1985, Cigno & Rosati 1996, Boldrin & Jones 2005, Billari & Galasso 2009, Sinn 2004, Fenge & Meier 2005, Ehrlich & Lui 1991, Cigno 1993, Rosenzweig 1988, Zhang & Zhang 2004, Entwisle & Winegarden 1984) tested against the mechanism AND. Result: **10/12 papers missed — 83% false negative rate.**

Reason: empirical papers in this literature typically regress TFR or family size on pension coverage without labeling the mechanism in their abstract. Mechanism vocabulary ("crowding out," "insurance motive") appears primarily in theoretical and survey papers, not in the identification-strategy empirical work.

## Options considered

1. **3-axis (CAUSE × FERTILITY × MECHANISM):** high precision, 83% FNR — unacceptable for systematic review.
2. **2-of-3 match:** complex boolean construction, unclear precision gain, untested.
3. **Expand mechanism axis:** add more terms — but the empirical literature avoids mechanism labels by design; any expansion recreates the same problem.
4. **2-axis (CAUSE × FERTILITY):** 83,648 results in OpenAlex, ~48% precision at k=200, seminal papers rank in top 20 by relevance — but full corpus not screenable.

## Decision

**Drop the mechanism AND entirely. Use 2-axis (CAUSE × FERTILITY).**

Also add `NOT "global burden of disease"` to exclude the GBD epidemiology cluster (7/26 false positives in the sample were IHME/Gates papers matching incidentally).

The false positive problem (81K results) is addressed by the LLM screening layer (see `2026-06-20-llm-screening-pipeline.md`), not by tightening the boolean query. Boolean layer optimizes for recall; LLM layer optimizes for precision.

## Rationale

In a Cochrane-style systematic review, false negatives at the search stage are unrecoverable. False positives are filtered downstream. The mechanism AND was inverting this cost structure — sacrificing recall for precision at the wrong stage of the pipeline.

## Generalization

This principle applies to all 61 hypotheses: **do not add a mechanism axis to the boolean query without empirical validation that the mechanism vocabulary appears in abstract text.** For most economic and cultural hypotheses, empirical papers use outcome variables and identification strategies without labeling mechanisms. The mechanism axis is appropriate only for biological hypotheses (B section) where MeSH vocabulary is controlled and mechanism terms are standardized.

## Review date

Revisit if any subsequent hypothesis shows >20% false negative rate on the 2-axis query in the gold-standard calibration test.
