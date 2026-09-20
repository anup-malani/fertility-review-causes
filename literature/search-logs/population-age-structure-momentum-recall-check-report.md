# Targeted recall check — A.9 (CORRECTS the core-screen "empty cell" finding)

**Run:** 2026-09-20, Shravan (TICK-089). **Results:** `…-recall-check-results.json`.
**Headline: the core-first screen's `empty-cell-is-the-result` conclusion is RETRACTED.** A.9's empirical
primary cell is **~15 studies**, not ~2.

## What the recall check did

Two focused OpenAlex queries at the empirical cell — (Q1) `age structure/composition × decomposition ×
births/fertility`, (Q2) `crude birth rate/number of births × decomposition/Kitagawa/Das Gupta` — deduped
against the 62 already-screened core records and the anchors, then title+abstract screened. 31 new
candidate decomposition records; **13 are genuine A.9 primaries**, 17 OFF (homonyms, projections,
proximate-determinant/marriage decompositions, non-birth-rate outcomes), 1 theory.

## Why the core screen undercounted (two causes, both mine)

1. **The core-first set was the highest-prior title-heuristic subset.** Most real decompositions have
   generic titles ("Decomposition of fertility/CBR in [country]") and land in the tail, not the top.
2. **I dropped the gated generic axis wholesale as "epidemiological standardization noise."** That was
   wrong for recall: the gated axis (`age structure/composition` + a decomposition co-term) held the
   real A.9 birth-rate decompositions *mixed with* the epidemiological rate-standardization noise. The
   fix is not to drop it but to **refine it** — require the age-structure term to co-occur with a
   birth/fertility term AND a decomposition term (exactly recall Q1), which isolates the ~15 from the
   disease-rate standardization. `population-age-structure-momentum-production-query.json` is updated
   accordingly.

The "screen the core first" decision was right precisely because it was cheap and the follow-up recall
check caught the error before any verdict was written.

## The A.9 empirical primary cell (~15 studies)

Multi-component birth-rate/CBR/birth-count decompositions from which the **age-structure/age-composition
contribution share** is one extractable component (the other components — marriage, marital fertility —
route to A.7/A.2 at the component level, per scope Wall 2):

| Year | Setting | DOI | Cell |
|---|---|---|---|
| 2024 | Malawi | 10.22146/jp.102685 | PRIMARY_COMPOSITION (age structure + nuptiality + marital fertility → TFR) |
| 2023 | South Korea | 10.31693/kjps.2023.09.46.3.4 | PRIMARY_COMPOSITION_BIRTHS (female population + marriage + marital fertility) |
| 2022 | South Korea | 10.1007/s12546-022-09287-3 | PRIMARY_COMPOSITION_CBR |
| 2021 | China | 10.1007/s42379-021-00094-6 | PRIMARY_COMPOSITION_BIRTHS (core) |
| 2019 | South Korea | 10.22823/jkea.25.1.201904.37 | PRIMARY_COMPOSITION_BIRTHS |
| 2019 | South Africa | (no DOI) | PRIMARY_COMPOSITION (age-sex structure) |
| 2017 | China / India | 10.12765/cpos-2017-12 | PRIMARY_MOMENTUM (age-composition momentum; growth outcome) |
| 2014 | China | (no DOI) | PRIMARY_COMPOSITION_CBR (core; age-structure share of CBR) |
| 2011 | South Africa | (no DOI) | PRIMARY_COMPOSITION_CBR |
| 2005 | USA | 10.1080/19485565.2002.9989096 | PRIMARY_COMPOSITION (GFR: age distribution component) |
| 1996 | USA | 10.2307/2061868 | PRIMARY_COMPOSITION (Das Gupta; age distribution component) |
| 1991 | China | 10.2307/1971949 | PRIMARY_COMPOSITION_CBR (triple standardization) |
| 1991 | Mexico | (no DOI) | PRIMARY_COMPOSITION_CBR (age-sex distribution) |
| 1983 | India | 10.25336/p6kw20 | PRIMARY_COMPOSITION (borderline; age pattern) |
| 1932 | USA | 10.1086/215925 | PRIMARY_COMPOSITION_CBR (historical; age composition vs specific rates) |

## What this changes

- **Stage 9 is now a quantitative synthesis, not narrative-only.** With ~15 studies reporting an
  age-structure contribution share, the chapter can synthesize the *distribution of the composition
  share* across settings/eras (e.g., "age structure accounted for X–Y% of observed CBR/birth-count
  change"). These are decomposition shares, not effect sizes, so the GRADE stays **NOT RATEABLE** and
  the demsig is reported per outcome — but the CBR/births cell now has a real, quantified magnitude
  behind it, not just accounting theory.
- **The demographic-significance verdict is now empirically anchored**, not purely definitional: the
  studies show *how large* the composition component actually is across real transitions (and that it is
  meaningful for the CBR/birth count while zero by construction for period TFR / CCF).
- **`empty-cell-is-the-result` no longer applies to A.9.** Retract it wherever written (scope, ticket,
  earlier commit messages).

## Next

Full-text retrieval of the ~15 primaries (several are non-English or no-DOI — RA/library procurement
likely for the South Africa 2019/2011, Mexico 1991, Korea Korean-language, and the 1932/1983 items),
then extraction of the **age-structure contribution share** (magnitude, sign, period, setting,
decomposition method, outcome level CBR vs births) into `extraction/population-age-structure-momentum.csv`.
A full PRISMA pass over the remaining worklist is now more clearly worthwhile, since the cell is real.
