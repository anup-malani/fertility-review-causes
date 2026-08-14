# Extraction report — microplastics-pfas-reproductive (B.6)

Hand-coded from the 9 full texts held that carry an estimate. Located first by `143_b6_fulltext_probe.py`, so every coded value has a quoted passage behind it in `extraction/microplastics-pfas-reproductive-fulltext-probe.csv`.

**17 effect rows** — 12 PFAS, 5 microplastics. **2 rows are in the restricted (parity-handled) track.** 5 rows carry `NUMERIC_UNRECOVERED`.

## 1. The two tracks disagree, and both cohorts that tested it say so

This is the chapter's central empirical result. Call 2 pre-committed to a two-track synthesis on parity handling because PFAS leave the body through pregnancy, lactation and menstruation, so parity causes exposure. The prediction was that the restricted track would be weaker. It is — and the evidence comes from inside the literature:

| cohort | unrestricted | parity-restricted |
|---|---|---|
| INUENDO (PFNA, fecundability) | FR 0.80 [0.69–0.94] | **not replicated** (authors' own words) |
| INUENDO (PFNA, infertility) | OR 1.53 [1.08–2.15] | **not replicated** |
| MoBa (PFOSA, fecundability) | FOR 0.85 [0.83–1.09] | FOR 0.91 [0.71–1.17], null |

Two independent cohorts, two independent restricted analyses, no surviving association. The chapter should state this as its primary finding on the PFAS side and should not report the unrestricted estimates as though they were the result.

## 2. Adjusting for parity is not restricting on it

S-PRESTO — the one preconception-measured cohort held, and on exposure timing the best-designed — finds decreased fecundability (PFDA FR 0.90 [0.82, 0.98], PFOS 0.88 [0.79, 0.99], mixture 0.89 [0.73, 1.02]). It **adjusts** for parity rather than restricting on it. Parity sits on the path from prior reproduction to current exposure, so adjustment leaves the reverse-causal channel partly open and can induce collider bias on top.

`PARITY_HANDLING` therefore needs **four** levels rather than the two Call 2 implied: `nulliparous_restricted`, `parity_stratified`, `parity_adjusted`, `none`. Only the first two enter the restricted track. This is a refinement to the frozen scope and should be recorded as one.

## 3. The microplastics primary cell contains no effect estimate

Every held plastic-family record in a PRIMARY cell is a review or opinion piece. The five empirical microplastics records held all estimate fertility **inputs** — sperm parameters, retrieved oocytes, AMH — not fertility quantities. They are small, largely ART-derived, and their p-values cluster at the margin (0.041, 0.056, 0.080, 0.083, 0.091), with the single strong result (p = 0.0003) attaching to IVF fertilization rate, which Wall 4 routes to A.17.

So the microplastics chapter's GRADE rating attaches to a cell that presently holds no estimate of the exposure against a fertility quantity. That is a defensible verdict of **Very Low / no rateable evidence**, and it is a finding rather than a gap in this review's search — the screen read 920 records and the completeness bypass guaranteed every both-axes plastic record was read.

## 4. Numerics lost to text extraction

5 rows are marked `NUMERIC_UNRECOVERED`. Decimals split across the PDF-to-text and XML-to-text boundaries, so the direction and p-value are legible but the point estimate and interval are not. **These are recorded as missing rather than reconstructed**: a number transcribed wrongly is worse than a number recorded as absent, and every one of them is on the microplastics side, where the evidence is thinnest and an invented figure would do the most damage. They need PDF-quality re-extraction before any pooling.

## Poolability

Not yet. PROTOCOL §5.9 requires three estimates sharing a chemical family, an estimand level, a sex stratum and a parity-handling status. The restricted track holds 2 rows across two cohorts, one of which reports no point estimate at all. The honest output is a narrative synthesis with the two-track disagreement as its centre, not a forest plot.

