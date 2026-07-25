# TICK-033: B.1 status-fertility effect extraction
**Status:** done (for the retrieved set; bounded by TICK-032 retrieval)
**Assigned:** any
**Parallel-safe:** no
**Blocks:** TICK-034, TICK-035
**Blocked by:** TICK-032
**Touches:** extraction/evolutionary-sex-drive-contraceptive-decoupling-studies.csv, extraction/evolutionary-sex-drive-contraceptive-decoupling-effects.csv

## Description

Extract study-level and estimate-level data from the retrieved full texts, adapting the OAS schema
(`extraction/schema.md`, `source/analysis/oas_meta_pipeline.py` column set). The primary effect is the
association between a status or wealth measure and reproductive success (number of children). Record
the association in a poolable form (correlation r, standardized beta, or convertible test statistic)
with its uncertainty and page/table locator.

## Acceptance criteria
- [x] Study-level table: one row per included empirical study, with setting, period, and sex coverage.
- [x] Effect-level table: one row per extractable status-fertility estimate, with r/beta, SE or CI, n, and page/table source.
- [x] Every estimate carries the contraceptive-availability moderator (present / absent / partial) for its population. *(Populated on all 10 in-pool rows; the 7 blanks are `exclude=yes` off-pool rows.)*
- [x] Every estimate carries the sex of the subjects (male / female / pooled). *(Same 10/7 split.)*
- [~] Each direct-decoupling study carries a `holds_desire_fixed` flag (yes / no / unclear) — the field that separates B.1 from A.2. **Vacuous, not satisfied: zero direct-decoupling studies were retrieved, so the column was never added to the schema. It must be added before any direct-decoupling study is extracted, or the B.1/A.2 boundary goes unrecorded.**
- [x] Ambiguous estimates flagged `needs_pi = yes`.

## Log
- 2026-07-25 (Claude): extraction closed out at **17 effect rows over 5 in-pool studies** (10 in-pool
  rows, 7 marked `exclude=yes` and routed off-pool). This is the set the TICK-034/035/036 results rest
  on. It is bounded by retrieval, not by extraction effort: TICK-032 reached 20 of 95 PDFs, so the
  pooled estimate covers 5 of the 52 status-and-reproduction studies the frozen screen identified.
  Reopening TICK-032 (library retrieval) is what would widen it.
- 2026-07-22 (Claude, prototype): built the effects table `extraction/evolutionary-sex-drive-contraceptive-decoupling-effects.csv` (schema per extraction/schema.md) on the 20 retrieved PDFs. 8 effect rows: 1 fully extracted (von Rueden Zr=0.19 [0.09,0.31], contraception absent, male), 3 with direction+page locators but effect pending table extraction (Zhang China men+/women-, Hopcroft US men+, all `needs_pi=yes`), 4 routed off-pool (Skirbekk review, Bolund-Lummaa heritability, Lidborg dimorphism-MA external benchmark, Gutierrez pending). Exact table coefficients NOT guessed. Awaits Zotero retrieval of the missing 42 status-and-reproduction DOIs + RA table extraction.

