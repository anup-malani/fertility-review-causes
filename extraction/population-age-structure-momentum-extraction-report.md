# Extraction report — A.9 population age structure and demographic momentum

**Run:** 2026-09-20, Shravan (TICK-089). PDFs from `~/Downloads/A9/` (Shravan-procured) + 2 OA PDFs
retrieved earlier. Extracted with `pdftotext`. Data in `population-age-structure-momentum.csv`.

## Files received (11) and disposition

**Matched A.9 primaries (8):** `2061868`→A9-11 (US 1996), `215925`→A9-15 (US 1932),
`Freedman-…1968`→A9-16 (Hong Kong), `KCI_FI002458711`→A9-05 (Korea 2019, Lee Cheol-hee),
`palamuleni-2011`→A9-09 (South Africa), `s12546-022-09287-3`→A9-03 (Korea 2022),
`s42379-021-00094-6`→A9-02 (China 2021), `Stable aggregate fertility…`→A9-10 (US 2005).

**Not A.9 — do not include (3):**
- `sustainability-14-03711` — Liu et al., age structure → **economic growth** in China (wrong outcome).
- `N0700320202` — Lee, old-housing → regional birth rate, spatial Durbin model (2026): a **C.2.c housing**
  paper, not an age-structure decomposition.
- `YI-MARRIAGEFERTILITYCHINA-1993` — Zeng Yi/Vaupel/Wang, *Genus* 1993, decomposes fertility **by parity**,
  not by age structure. A *different* paper than the still-missing A9-12 (Yi et al. 1991 PDR), which it
  cites — so A9-12 exists and is still to be procured.

## Extraction status (16 included)

| Status | n | Study IDs |
|---|---:|---|
| EXTRACTED (numeric) | 6 | A9-02, A9-03, A9-07, A9-08, A9-09, A9-16 |
| EXTRACTED (qualitative — pin table number) | 2 | A9-05 (Korean), A9-10 |
| PARTIAL (component present, pin number) | 2 | A9-11, A9-15 |
| Needs OCR (scanned, no text layer) | 1 | A9-14 (India 1983) |
| Still to procure | 5 | A9-01 (China 2014), A9-04 (Korea 2023), A9-06 (South Africa 2019), A9-12 (China 1991), A9-13 (Mexico 1991) |

## The age-structure contribution, by study (preliminary)

| Study | Setting / period | Outcome | Age-structure contribution |
|---|---|---|---|
| A9-16 Freedman 1968 | Hong Kong 1961–65 / 1961–66 | CBR | **~80%** of the decline (1961–65); ~50% (1961–66) |
| A9-09 Palamuleni 2011 | South Africa 1996–2001 | CBR | **+60%** (age structure *raised* the CBR) |
| A9-07 Chaurasia 2017 | China/India 1950–2015 | natural growth / CBR | age-composition ~**80%** of India growth 2010–15, >100% China; CBR multiplier 1.01–1.21 |
| A9-03 Korea 2022 | South Korea, to ~2015 | CBR | **−0.37** (vs marriage −2.26); ~2.9% |
| A9-02 China 2021 | China 2012–19 | births (count) | size-of-women dragged births −150 to −340k; **secondary** to marriage |
| A9-05 Korea 2019 | South Korea to 2017 | births (count) | **secondary** contributor; marriage primary |
| A9-08 Malawi 2024 | Malawi 1992–2015 | TFR/CBR | **small residual (~0–20%)**; marital fertility + nuptiality dominate |
| A9-10 US 2005 | USA 1970–99 | GFR | age distribution **compensated (+)** for marriage decline |
| A9-11 US 1996 | USA 1960–92 | nonmarital fertility ratio | age-distribution component present; shift to older ages post-1980 |
| A9-15 US 1932 | USA 1920–30 | CBR/specific rates | age-composition shift documented (descriptive) |

## Preliminary synthesis signal (for stage 9)

The age-structure/composition contribution to CBR/birth-count change is **large but highly setting- and
period-dependent, and signed both ways**:
- **Dominant** in momentum-heavy transitions and short windows: Hong Kong ~80%, South Africa +60%,
  China/India ~80–100% of growth. Here composition *is* most of the measured headline movement.
- **Secondary** where marriage and marital fertility carry the decline: Malawi ~0–20%, Korea, China 2021.
- **Compensating/positive** in the low-fertility US, offsetting marriage decline in the GFR.
- **Zero by construction** for period TFR and completed cohort fertility everywhere (A9-07 confirms via
  its own `f = w × TFR/35`).

This is exactly the **per-outcome, per-setting** verdict the scope and TICK-080 anticipated: A.9 can be
the mechanical majority of a CBR/birth-count movement in one setting and a minor residual in another,
and the honest chapter reports the *distribution* of the composition share, not a single number — while
noting the number is zero for the quantum measures by construction.

## Next

1. **OCR A9-14** (India 1983) or procure a text version.
2. **Procure the 5 missing** (A9-01, A9-04, A9-06, A9-12, A9-13) — A9-12 is Yi/Vaupel/Wang 1991 PDR
   `10.2307/1971949` (the Genus 1993 substitute does not replace it).
3. **Pin exact numbers** for A9-05, A9-10 (tables), A9-11.
4. Then stage 9 quantitative synthesis of the composition-share distribution + stage 10 per-outcome demsig.
