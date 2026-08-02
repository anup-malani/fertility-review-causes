# TICK-052: D.3.b demographic-significance pass (SDT only)
**Status:** done — SDT-only pass complete; realized share reported as a bounded range with a zero floor, stated and distinctive cells recorded unidentified
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
- 2026-07-27 (Claude): `source/analysis/d3b_demographic_significance.py` + 12 unit tests (all
  passing). Outputs `output/tables/climate-anxiety-eco-doomerism-{demographic-significance,
  grade-verdicts}.csv`. Verdicts are COMPUTED from the evidence tables, not typed, which
  matters more here than in B.1 because the ratings are unfavourable and a hand-typed
  unfavourable rating invites quiet softening later.

  **Both tracks rate VERY LOW.** Realized: 4 downgrades (risk of bias, inconsistency
  between two analyses of one panel, indirectness because the ecological content of the
  fear is not shown to matter, imprecision because no pool is possible). Stated: 4
  downgrades (design, indirectness on both outcome and exposure, inconsistency, sampled
  coverage).

  **The transition pass is trivial and the hard part is magnitude.** SDT-only by scope, so
  every window falls in the SDT period by construction and there is no pre-modern or FDT
  cell to classify.

  **The realized share is a RANGE WITH A ZERO FLOOR, not a point.** 0 to about 4.5% of the
  birth hazard, built by multiplying the prevalence of dread bearing on childbearing
  (25.2%, Vercammen PNAS, US youth) by the proportional hazard reduction among the very
  worried (18%, Golovina, GSOEP). Every step is weak: the prevalence is American and the
  hazard German, questioning whether one will have children is not intending to forgo them
  and neither is a birth, and the hazard estimate does not survive adjustment for general
  worry. **The floor is zero for a substantive reason** — Peters' cohort-stratified
  estimate for those born 1970 or later, the cohort this hypothesis is about, is 0.98
  (0.85, 1.12). Flagged `needs_human_review=yes`.

  Stated intentions: NOT IDENTIFIED, and the tests assert the pipeline cannot emit a point
  estimate for it. Bastianelli's extensive-margin-only result means the intention effect is
  not a uniform family-size reduction even on its own terms. Distinctive claim:
  UNIDENTIFIED, mirroring B.1.
- 2026-07-27 (Claude): opened.
