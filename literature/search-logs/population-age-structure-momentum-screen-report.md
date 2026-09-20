# Full screen + PRISMA — A.9 population age structure and demographic momentum

**Run:** 2026-09-20, Shravan (TICK-089). **Full universe:** `…-screen-full.json` (1,299 deduped records).
**Included set:** `…-included-studies.json` (16). Supersedes the core-screen report's preliminary
"empty cell" read (retracted — see `…-recall-check-report.md`).

## Universe

Effective production frame = tight momentum axis (738) ∪ refined gated axis (age-structure × decomposition
× births, 434) ∪ Tier-B snowball (199), deduped, channel-2 seeds removed → **1,299 records screened**.
The gated axis is included in refined form (the recall check proved dropping it lost real decompositions);
its epidemiological rate-standardization bulk is excluded at the screen, not at the query.

## PRISMA flow

| Stage | n |
|---|---:|
| Records screened (deduped universe) | 1,299 |
| — Excluded: off-topic / topical-overlap (`OFF` + `FERT_OTHER`) | 1,001 |
| — Excluded: population-size/growth outcome (`OFF_OUTCOME_POP`, Wall 3) | 123 |
| — Excluded: homonym (ecology/parasite/soil/education `age structure`/`decomposition`) | 81 |
| — Routed to A.11 (tempo, Wall 1) | 26 |
| — Routed to JEL theory stream (formal momentum/stable-population canon) | 38 (+12 canon anchors) |
| **Included — empirical primary (age-structure→birth-rate/count decomposition)** | **16** |

The decision-critical adjudication bucket (decomposition or age-structure records carrying a fertility
term) was 30 records, each read on title+abstract; 16 are genuine A.9 primaries and the rest route off
(preterm-birth health outcomes, fertility→age-structure reverse direction, projections, homonyms). The
full pass added exactly **one** primary beyond the recall check (Hong Kong 1968), which is the
reassurance that the included set is stable and near-complete.

## Included studies (16) — the extraction target

The A.9 estimand is the **age-structure/age-composition contribution share** of an observed CBR or
birth-count change; in the multi-component decompositions the other components (marriage, marital
fertility) route to A.7/A.2 at the component level (scope Wall 2).

| Year | Setting | Cell | DOI |
|---|---|---|---|
| 2024 | Malawi | PRIMARY_COMPOSITION | 10.22146/jp.102685 |
| 2023 | South Korea | PRIMARY_COMPOSITION_BIRTHS | 10.31693/kjps.2023.09.46.3.4 |
| 2022 | South Korea | PRIMARY_COMPOSITION_CBR | 10.1007/s12546-022-09287-3 |
| 2021 | China | PRIMARY_COMPOSITION_BIRTHS | 10.1007/s42379-021-00094-6 |
| 2019 | South Korea | PRIMARY_COMPOSITION_BIRTHS | 10.22823/jkea.25.1.201904.37 |
| 2019 | South Africa | PRIMARY_COMPOSITION | (no DOI — RA procurement) |
| 2017 | China / India | PRIMARY_MOMENTUM | 10.12765/cpos-2017-12 |
| 2014 | China | PRIMARY_COMPOSITION_CBR | (no DOI — RA procurement) |
| 2011 | South Africa | PRIMARY_COMPOSITION_CBR | (no DOI — RA procurement) |
| 2005 | USA | PRIMARY_COMPOSITION | 10.1080/19485565.2002.9989096 |
| 1996 | USA | PRIMARY_COMPOSITION | 10.2307/2061868 |
| 1991 | China | PRIMARY_COMPOSITION_CBR | 10.2307/1971949 |
| 1991 | Mexico | PRIMARY_COMPOSITION_CBR | (no DOI — RA procurement) |
| 1983 | India | PRIMARY_COMPOSITION | 10.25336/p6kw20 |
| 1932 | USA | PRIMARY_COMPOSITION_CBR | 10.1086/215925 |
| 1968 | Hong Kong | PRIMARY_COMPOSITION_CBR | 10.1080/00324728.1968.10405534 |

Coverage: China ×3, South Korea ×3, USA ×3, South Africa ×2, plus China/India, Malawi, Mexico, India,
Hong Kong; 1932–2024. Enough spread to synthesize the composition share across settings and eras.

## Consequences

- **Stage 9 = quantitative synthesis** of the age-structure contribution share (magnitude distribution
  across settings/eras), not narrative-only. GRADE stays **NOT RATEABLE** (decomposition shares, not
  effect sizes); demsig **per outcome** (CBR/births empirically anchored; period TFR / CCF = 0 by
  construction).
- **RA procurement needed** (PROTOCOL stage 5 human gate): several items are non-English (Korean,
  Chinese) and/or have no DOI (South Africa 2019/2011, China 2014, Mexico 1991) — flag for the
  UChicago-library/RA retrieval queue.

## Next

Stage 5–7: full-text retrieval (AI-accessible first, remainder to RA) → extract the age-structure share
(magnitude, sign, period, setting, decomposition method, outcome level CBR vs births) into
`extraction/population-age-structure-momentum.csv`, RA verifies 10%.
