# TICK-052: D.3.b demographic-significance pass (SDT only)
**Status:** open
**Assigned:** any
**Parallel-safe:** no
**Blocks:** TICK-053
**Blocked by:** TICK-050, TICK-051
**Touches:** source/analysis/d3b_demographic_significance.py, extraction/climate-anxiety-eco-doomerism-target-period-relevance.csv, output/tables/climate-anxiety-eco-doomerism-{demographic-significance,grade-verdicts}.csv

## Description

Produce the demographic-significance table and the generated GRADE verdicts, adapting
`b1_demographic_significance.py`. **There is no pre-modern or FDT cell** — the mechanism requires
knowledge of anthropogenic climate change and the hypothesis is scoped to the 2020s — so the
transition-classification step that OAS and B.1 run reduces here to confirming that every study window
falls in the SDT period. Read windows out of the PDFs rather than recalling them, as TICK-045 did.

The substantive difficulty is specific to this hypothesis and the chapter's §7 already names it. Even a
robust effect of ecological dread on stated fertility intentions has unknown demographic significance,
because getting from an intention gap to a birth gap requires two quantities this literature has barely
measured: the rate at which an intention gap translates into realized births, and the population share
holding the dread strongly enough to act on it. Reporting a large intention effect as though it were a
large demographic effect is the specific failure mode this hypothesis invites, and the pass exists
partly to prevent it.

Two defensible outputs, and the choice between them should be made on the evidence rather than on
which is more satisfying to write:

1. A bounded calculation — the pooled intention effect combined with a translation rate imported from
   outside this literature and an exposure-prevalence share — presented explicitly as a bound with its
   imported inputs labelled as imported.
2. The cell recorded as **unidentified**, as TICK-045 recorded B.1's distinctive decoupling claim,
   if no defensible translation rate exists.

The realized-fertility track is what could in principle support a direct demographic claim without the
translation step, but at k ≤ 6 it will bound very little. Say what it bounds and no more.

The desire-independence cell — the hypothesis's distinctive claim — has 4 studies, all stated
intention, none measuring births. Whether it can be assigned any share at all is doubtful and should be
resolved explicitly rather than left to the chapter's prose.

## Acceptance criteria
- [ ] Per-study window read from full text and confirmed to fall in the SDT period; no PM or FDT cell
      fabricated to fill the template.
- [ ] Demographic-significance table populated for both tracks, with the stated track's dependence on
      an intention-to-birth translation rate stated on the face of the table, not only in prose.
- [ ] The translation rate either sourced and labelled as imported, or the cell recorded as
      unidentified — with the choice and its reason logged.
- [ ] The desire-independence cell explicitly resolved: assigned a share with justification, or
      recorded as unidentified.
- [ ] GRADE verdicts **generated** by the script, not hand-typed, so ratings and underlying counts
      cannot drift apart.
- [ ] Unit tests alongside the script, per the B.1 pattern.

## Log
- 2026-07-27 (Claude): opened.
