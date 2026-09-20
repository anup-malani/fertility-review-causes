# Production keyword search — A.9 population age structure and demographic momentum

**Run:** 2026-09-20, Shravan (TICK-089). **Query:** `population-age-structure-momentum-production-query.json`.
**Worklist:** `population-age-structure-momentum-screen-worklist.json` (565 records, tight axis).
**Orthogonal channel:** `population-age-structure-momentum-snowball-tierb.json` (199 records).

## What was run

Two-axis OpenAlex `title_and_abstract.search`, `EFFECT AND CAUSE`, cursor-paged:

- **EFFECT** = crude/period birth measures + counts + core fertility (`crude birth rate`, `birth rate`,
  `number of births`, `general fertility rate`, `total fertility rate`, `fertility`, `childbearing`,
  `reproduction rate`). Deliberately CBR/births-weighted because that is A.9's outcome (period TFR/CCF
  are composition-free by construction).
- **CAUSE (tight)** = momentum + explicit birth-rate-decomposition vocabulary (`population momentum`,
  `demographic momentum`, `momentum of population growth`, `momentum factor`, `population age
  structure`, `decomposition of the birth rate`, `decomposition of fertility`, `components of change in
  the birth rate`). **570 records.**
- **CAUSE (gated generic)** = (`age structure`/`age composition`/`age distribution`) AND a
  decomposition/rate co-term AND the effect axis. **324 records — tested and DROPPED.**

## The gated generic extension is net-negative and was dropped

The scope and frame probe predicted bare `age structure`/`age composition` is homonym-inflated. The
production run confirms it in a second, more specific way: even gated by a decomposition/rate co-term,
the 324 records are dominated by **epidemiological rate-standardization** (age-standardized *disease*
rates, Kitagawa/Das Gupta applied to mortality and morbidity), not birth-rate composition — only ~19
were birth-rate `PRIMARY_COMPOSITION`. Including it would add ~300 off-topic records to the screen for
~19 hits, most of which the tight axis's explicit `decomposition of the birth rate` phrases and the
Tier-B snowball already reach. **Effective production frame = tight axis (565, after seed removal) ∪
Tier-B (199).**

## Worklist composition (565 tight-axis records, provisional title-only tags)

| Provisional cell | n |
|---|---:|
| OFF_OTHER (general demographic-transition/age-structure papers, no decomposition) | 323 |
| FERT_OTHER | 85 |
| OFF_OUTCOME_POP (population growth/size/aging — the expected-largest off-cell) | 81 |
| MOMENTUM | 35 |
| OFF_OTHER_ECOLOGY_HOMONYM | 25 |
| PRIMARY_COMPOSITION (birth-rate/count decompositions) | 9 |
| OFF_TEMPO_A11 (→ A.11) | 6 |
| AGE_STRUCT_AMBIG | 1 |

**21 records are multi-channel** (in both the keyword pull and the Tier-B snowball) → Tier-1 core
candidates (GACS E1: gold membership or ≥2-channel agreement).

The plausibly-primary core is small — **~45 records** (35 MOMENTUM + 9 PRIMARY_COMPOSITION + 1 ambig) —
and the birth-rate-decomposition cell specifically is **9 records** on a title heuristic, likely fewer
after screening. This is the fourth independent confirmation (frame probe, channel-1 empty, channel-2/3
anchors, now the production pull) that A.9's identified/empirical cell is near-empty and the chapter is
a theory-plus-decomposition synthesis. `empty-cell-is-the-result` remains the live expectation.

## Next — stage 3 screen (NOT yet run; the session's biggest step)

Screen the ~700-record union (565 keyword ∪ 199 Tier-B) through the D1→Haiku→Sonnet→RA cascade:
route MOMENTUM/PRIMARY_COMPOSITION to the empirical/decomposition stream, momentum-theory and
formal-demography canon to the JEL theory stream, OFF_OUTCOME_POP / OFF_TEMPO_A11 / ecology-homonym
out (with A.11 cross-ref at the component level), and report Recall(B) against the Tier-B frame. No
`sequential-screen.mjs`/`snowball-citations.mjs` is present on this branch, so the screen is either an
inline LLM effort or needs that tooling — flagged for a go-ahead before the spend.
