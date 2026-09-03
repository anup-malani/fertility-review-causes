# Provenance — US CPI child-cost components

Pulled 2026-09-03T17:15:56+00:00 by `source/build/318_c2b_child_price_index.py`.

CPI series come from **DBnomics** (`api.db.nomics.world/v22/series/BLS/cu/<id>`), which
mirrors the BLS CPI-U. DBnomics is used rather than BLS directly because the BLS flat
files at `download.bls.gov` return HTTP 403 from Akamai bot defence, and the unregistered
BLS public API v1 silently ignores `startyear`/`endyear` and returns only the most recent
three years — a defect that would have produced a confident wrong answer.

US TFR comes from the World Bank WDI, indicator `SP.DYN.TFRT.IN`.

Responses are stored unmodified. Derived series live in `output/tables/`.

| component | series | role | note |
|---|---|---|---|
| `all_items` | `CUUR0000SA0` | deflator | CPI-U all items; the deflator |
| `books_supplies` | `CUUR0000SEEA` | education | educational books and supplies, from 1967 |
| `school_tuition` | `CUUR0000SEEB02` | education | elementary and high school tuition, from 1978 |
| `college_tuition` | `CUUR0000SEEB01` | education | college tuition and fees, from 1978 |
| `medical` | `CUUR0000SAM` | health | medical care, all ages, from 1935 |
| `apparel` | `CUUR0000SAA` | clothing | ALL apparel — a SUBSTITUTE for the children's series §5 named, which BLS does not publish here |
| `daycare` | `CUUR0000SEEB03` | EXCLUDED | day care and preschool — C.2.a's, excluded from every arm, reported for reference |
