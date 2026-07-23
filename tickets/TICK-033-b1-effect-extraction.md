# TICK-033: B.1 status-fertility effect extraction
**Status:** open
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
- [ ] Study-level table: one row per included empirical study, with setting, period, and sex coverage.
- [ ] Effect-level table: one row per extractable status-fertility estimate, with r/beta, SE or CI, n, and page/table source.
- [ ] Every estimate carries the contraceptive-availability moderator (present / absent / partial) for its population.
- [ ] Every estimate carries the sex of the subjects (male / female / pooled).
- [ ] Each direct-decoupling study carries a `holds_desire_fixed` flag (yes / no / unclear) — the field that separates B.1 from A.2.
- [ ] Ambiguous estimates flagged `needs_pi = yes`.

## Log
- 2026-07-22 (Claude, prototype): built the effects table `extraction/evolutionary-sex-drive-contraceptive-decoupling-effects.csv` (schema per extraction/schema.md) on the 20 retrieved PDFs. 8 effect rows: 1 fully extracted (von Rueden Zr=0.19 [0.09,0.31], contraception absent, male), 3 with direction+page locators but effect pending table extraction (Zhang China men+/women-, Hopcroft US men+, all `needs_pi=yes`), 4 routed off-pool (Skirbekk review, Bolund-Lummaa heritability, Lidborg dimorphism-MA external benchmark, Gutierrez pending). Exact table coefficients NOT guessed. Awaits Zotero retrieval of the missing 42 status-and-reproduction DOIs + RA table extraction.

