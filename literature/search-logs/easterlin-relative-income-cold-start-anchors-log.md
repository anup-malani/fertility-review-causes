# C.6.a cold-start anchors — resolved 2026-09-02, all 31 confirmed

**TICK-078.** Candidates in `easterlin-relative-income-anchor-candidates.json`, resolution in
`easterlin-relative-income-cold-start-anchors.json`, resolver
`source/build/goldset/307_c6a_cold_start_anchors.py`.

## The candidate list is built as its own control

Thirty-one candidates, split into two kinds, and the split is the point:

- **18 `control`** — titles copied verbatim from records that script 305 found sitting in other
  chapters' pools. These works demonstrably exist. A resolver failure on one of them is a **broken
  resolver**.
- **13 `hand`** — author–year–title triples written from knowledge of the literature. A failure on
  one of these may be a **ghost citation**.

Without the split a run of NO_RESULTS is uninterpretable — it could be the tool or it could be the
literature. This is `validate-a-null-detector-on-positives` built into the candidate list rather than
bolted on afterwards, and it earned its place immediately: the first run returned 18/18 controls and
10/13 hand, which localised every failure to the candidate side before any of them was read.

## Result

| | resolved | verdicts |
|---|---|---|
| control | **18 / 18** | 14 `MATCH_BY_DOI`, 4 `MATCH` |
| hand | **13 / 13** | 10 `MATCH`, 1 `MATCH_STEM`, 2 `MATCH_VERSION_TWIN` |

**Zero ghost citations.** Every hand-typed title corresponds to a real indexed work. That is worth
stating plainly because the opposite result is common enough that this check exists.

## Three resolver defects, each of which cost a real anchor

All three were found on Easterlin's *Birth and Fortune*, and all three are inherited — they are in
the C.3.e reference implementation this script was ported from, and therefore in every copy on
`main`. Reported to TICK-074.

**1. `is_stem` had only ever been fixed in one direction.** It tolerates the index carrying a
*longer* title than the candidate (a subtitle the candidate omitted). The observed failure is the
mirror: *Birth and Fortune: The Impact of Numbers on Personal Welfare* is indexed as the bare **Birth
and fortune**. The index has the SHORTER title. Jaccard 0.33, while four *reviews* of the book —
which carry its full title verbatim — score 1.00. Fixed with `is_stem_reversed`, gated behind the
first-author test because that direction is the riskier one.

**2. The first-author gate was a scoring weight, not a discriminator.** Those reviews list Easterlin
as a co-author, so they pass an "author appears anywhere" test and fail only the first-author one. On
score they beat the book **1.20 to 0.83**, and the gate could then only *refuse the winner* — it had
no way to promote the correct record sitting in the same result set. Ranking now puts the gate first:
passing an applicable first-author gate outranks everything, failing one outranks nothing.

**3. The early exit was conditioned on a different test than the verdict.** The loop stopped as soon
as any candidate scored ≥ 1.0 — including one the gate was certain to refuse — so the later rungs,
the ones that can actually reach a truncated book title, never ran. **An early exit must be
conditioned on the same gate the verdict uses.** This is the defect that actually did the damage;
fixing 1 and 2 alone left the anchor unresolved, because the rung that finds it was never reached.

A fourth, smaller: the pre-colon head rung required a 4-token head. *Birth and Fortune* is three.
Lowered to 3 where a first author is available to gate on.

## Version twins — five of thirty-one, and the citations are on the wrong record

| anchor | primary | twin |
|---|---|---|
| Welch, cohort size and earnings | 1979 article, **659** cites | 1979 preprint, **0** |
| Pampel and Peters, *The Easterlin Effect* | 1995 article, 96 | 1995 article, 3 |
| Samuelson, self-generated fertility waves | 1976 article, 68 | 1976 article, 17 |
| Ermisch, Easterlin hypothesis in Britain | 1979 article, 56 | 1979 article, 13 |
| Korenman and Neumark, cohort crowding | 1997 NBER report, 100 | 1997 preprint, 7 |

Both ids are kept for every pair. A snowball seeded on one twin misses the other's citing set, and
the split is severe — Welch's twin carries **zero** of 659 citations.

Butz and Ward is the sharpest case and gets its own verdict class. Two records share the title: the
one OpenAlex dates **1977** carries **438** citations, and a **1979** record of the same title carries
**0**. The commonly cited version of record is the 1979 *AER* article, so a candidate naming either
year fails a ±1 year gate against the other. `MATCH_VERSION_TWIN` — same title, same first author,
different year — records this as one study rather than sending it to a human read.

## Coverage of the estimand cells

The resolved set spans every primary cell: `RELATIVE_INCOME_FERTILITY` (6), `COHORT_SIZE_FERTILITY`
(4), `CYCLE_TEST` and cycle theory (3), `RIVAL_TEST` (4, including Butz and Ward themselves),
`MIXED_COHORT_MARRIAGE` (2, the Wall 3 boundary), `LINK1_LABOUR` (6), reviews and theory (6).

**`BENCHMARK_MEASURED` has exactly one anchor** — Easterlin's own 1976 statement of the
aspirations-versus-resources mechanism — and that anchor is theory, not an estimate. The cell scope
§4 called the value-added cell currently has no empirical anchor at all. That is a prediction the
search will test, not yet a finding.

## What this set is for, and what it is not

These are **calibration targets for the production query**, not the evidence base. Recall is scored
against them per link, because a query tuned on the large link-1 cohort-crowding literature will look
excellent and find nothing about fertility. Two of them are deliberately negative controls for the
outcome axis: the *Birth and Fortune* book review cluster, and the Easterlin-hypothesis-and-asset-
prices work that shares every exposure word and has no fertility outcome.
