# C.6.a title/abstract screen rubric

**TICK-078.** Applies to `easterlin-relative-income-screen-universe.json` after the 310 prescreen.
Every record gets exactly one cell. Cells are scope §9's; the walls are scope §8's.

## The one question that routes most records

**What does the estimate actually vary?** Not what the author says the paper is about. A study whose
identifying variation is an aggregate recession is C.5.a's however often it says "cohort"; a study
whose variation is relative cohort size is C.6.a's however it frames the mechanism. This is the rule
C.2.c froze on 2026-07-31 and every chapter since has used.

## Cells

| cell | admit when | note |
|---|---|---|
| `RELATIVE_INCOME_FERTILITY` | Cohort-relative earnings or prospects → fertility | Primary |
| `COHORT_SIZE_FERTILITY` | Relative cohort size → fertility, with an **age-standardised** outcome | Primary. A crude birth rate cannot separate behaviour from composition → `OFF_COMPOSITION_A9` |
| `BENCHMARK_MEASURED` | Either of the above where the **parental-household standard** is measured, not proxied | The value-added cell. Expected to be near-empty; say so if it is |
| `CYCLE_TEST` | Tests endogenous oscillation itself — difference-equation, VAR, spectral, simulation | Never pooled with the reduced-form cells |
| `RIVAL_TEST` | Easterlin against a named alternative on the same data (Butz–Ward and others) | Primary; cross-file to the rival's chapter |
| `INSTITUTIONAL_MODERATION` | The effect conditioned on labour-market institutions or welfare structure | The cell that could flip the §5 sign test |
| `LINK1_LABOUR` | Cohort size → wages, unemployment, entry earnings, **no fertility outcome** | Context only. Never primary, never pooled |
| `MIXED_COHORT_MARRIAGE` | Channel is a marriage squeeze created by cohort growth | Unallocated (Wall 3); report, do not pool |
| `THEORY` | Formal models, expositions, reviews with no new estimate | Theory stream |

## Route out

| tag | when |
|---|---|
| `OFF_ABSOLUTE_C1a` | Absolute income or employment, no cohort-relative benchmark |
| `OFF_UNCERTAINTY_C5a` | Aggregate labour-market shock common across cohorts |
| `OFF_COMPOSITION_A9` | Crude-rate result with no age standardisation; pure momentum/age-structure accounting |
| `OFF_MARRIAGE_C7a` | Marriage-market composition not driven by cohort size |
| `OFF_SEXRATIO_A10` | Sex ratio at birth, missing women, dowry, China/India marriage squeeze |
| `OFF_CLINICAL` | Reproductive medicine, menstrual cycle, fecundity biology |
| `OFF_OTHER` | Anything else with no C.6.a exposure |
| `INSUFFICIENT_INFO` | Not routable on title and abstract alone. Pairs only with `UNCERTAIN` |

## Three standing traps on this hypothesis

1. **"Baby boom/boomer".** The generational label (retirement, marketing, gerontology) is not the
   demographic event. The prescreen removes the clearest cases; the rest are read.
2. **"Fertility cycles" means the menstrual cycle** in most of the indexed literature. → `OFF_CLINICAL`.
3. **"Relative income" belongs to two literatures.** The subjective-well-being one (Easterlin
   paradox) is not this hypothesis. → `OFF_OTHER`.

## What the screen may not do

It may not decide `identified` or `design` — those are full-text properties, and A.23 carried a paper
through search, screen and priority retrieval as an administrative allocation when it was IPTW. The
screen assigns a **cell**; design is a hypothesis recorded at extraction.

## Blinding

The 31 resolved anchors are in the sheets **unmarked**. Sensitivity is computed after ingest by
checking which of them the screen returned to a primary cell. A screen that knows which records are
gold measures nothing.
