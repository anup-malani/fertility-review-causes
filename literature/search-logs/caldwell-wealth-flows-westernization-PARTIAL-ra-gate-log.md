# Human review gate — caldwell-wealth-flows-westernization (D.1.b) — **PARTIAL / WORK IN PROGRESS**

> **NOT THE SIGN-OFF GATE.** Built from a partial screen. The two census strata (`A_DECISIVE`, `B2_PRIMARY_SCHOOLING`) are censuses of *what has been screened so far*, not of the corpus, so re-running after the screen completes WILL add rows to them. The sampled strata are unaffected — a random sample of a random sample is still a random sample — so overturn rates from those remain valid.
>
> Review work done against this queue is not wasted: every row is a real record with a real screen verdict, and the decisions carry forward. What cannot be done from it is declaring the gate passed.

Worksheet: `extraction/caldwell-wealth-flows-westernization-PARTIAL-ra-gate.csv` — **211 rows**. Built from the completed screen over 3,253 corpus records. Sampling is deterministic; the seed and n for every sampled stratum are below, so the same draw reproduces.

## Strata

| stratum | population | drawn | rule |
|---|---:|---:|---|
| `A_DECISIVE` | 22 | 22 | census of screened-so-far |
| `B_WALL5_SCHOOLING` | 79 | 40 | seed 20260807+1 |
| `B2_PRIMARY_SCHOOLING` | 7 | 7 | census of screened-so-far |
| `C_TITLE_ONLY` | 1,578 | 60 | seed 20260807+2 |
| `D_WALL_OFF_WEALTH_FLOWS_C3f` | 28 | 12 | seed 20260807+10 |
| `D_WALL_OFF_POSTMATERIALIST_D1a` | 54 | 12 | seed 20260807+11 |
| `D_WALL_OFF_DIFFUSION_CHANNEL_A20` | 22 | 12 | seed 20260807+12 |
| `D_WALL_OFF_FERTILITY_CONTROL_A3` | 67 | 12 | seed 20260807+13 |
| `D_WALL_OFF_FEMALE_AUTONOMY_D2a` | 82 | 12 | seed 20260807+14 |
| `D_WALL_OFF_SCHOOLING_ECONOMIC` | 10 | 10 | seed 20260807+15 |
| `D_WALL_OFF_CULTURAL_EVOLUTION_D1c` | 20 | 12 | seed 20260807+16 |

## What this gate is for

**Stratum B is the point of the exercise.** The A1 scope recorded, before any screening, that a title/abstract screen cannot enforce Wall 5 — whether a schooling estimate decomposes ideational content from wage returns lives in the results tables, not the abstract. The screen therefore reports **79 unresolved against 7 decomposed (92% unresolved)**, and that figure is an upper bound *by construction*, not by caution. This stratum is read at full text because that is the only place the answer exists. Whatever share of the unresolved class turns out to decompose a mechanism after all is the correction to the chapter's headline number.

Stratum B2 censuses the other side of the same ratio. A ratio moves if either side is wrong, and reading only the larger side would let an inflated numerator through.

**Stratum C prices the abstract-availability limit.** Those records were assigned by rule and never read. The estimable question is what share would have been primary given an abstract; that share, applied to the stratum, is what the limit cost.

**Stratum D reports overturn rates by wall, not in aggregate.** The D.3.b gate overturned five of the twelve decisive records it read and the overturns clustered by wall; an aggregate rate would have hidden which wall was failing.

## Columns the human fills

`ra_verdict`, `ra_cell`, `ra_outcome_level`, `ra_route_to`, `agree_or_overturn`, `mechanism_decomposed` (stratum B and B2 only: yes / no / cannot tell), `ra_reason`, `send_to_fulltext`, `ra_initials`, `ra_date`.

`mechanism_decomposed` is the field the whole gate turns on. Record `cannot tell` freely — a paper whose mechanism genuinely cannot be determined from full text belongs in the unresolved class, and forcing a yes/no would manufacture the precision the chapter is trying to measure honestly.

