# A5 wave-1 screen audit — climate-anxiety-eco-doomerism (D.3.b)

Batches 001–005 of 30 (200 of 1,170 records), five independent blinded screeners, run 2026-07-24.
Wave 1 was gated deliberately so rubric defects surface before the remaining 25 batches are spent.
**Verdict: do not run waves 2–6 on rubric v1.** Five of five screeners flagged the same load-bearing
ambiguity, and it governs 21 of the 35 RELEVANT verdicts.

## Mechanical validation (passes)

| check | result |
|---|---|
| verdict files present | 5/5 |
| verdicts per batch | 40/40 on every batch |
| paperId set + input order | exact match to batch input, all 5 |
| required fields present | 200/200 |
| out-of-taxonomy cell values | 0 |
| `NA` cell paired with non-`NOT_RELEVANT` verdict | 0 |

The blinded-batch machinery works. Every problem below is in the rubric, not the pipeline.

## Wave-1 substantive signal

| | n (of 200) |
|---|---|
| NOT_RELEVANT | 145 |
| RELEVANT | 35 |
| UNCERTAIN | 20 |

Cells: `NA` 103 · **`THEORY` 35** · `OFF_OUTCOME` 28 · `PRIMARY_ECO_PESSIMISM` 9 · `OFF_ECON_C5a` 8 ·
`OFF_POSTMATERIALIST_D1a` 6 · `PRIMARY_HABITABILITY_FEAR` 4 · `REVERSE` 2 · `DESIRE_INDEPENDENCE` 2 ·
`OFF_CLINICAL_D3a` 2 · `PRIMARY_CARBON_ETHICS` 1.

Outcome levels: `NA` 180 · `STATED_INTENTION_OR_ATTITUDE` 18 · `BOTH` 1 · **`REALIZED_FERTILITY` 1**.

**The A1 scope's predicted evidence asymmetry is confirmed in-sample, and it is more extreme than
predicted.** Only 16 of 200 records reached an empirical primary cell, against 35 in the theory stream —
theory outnumbers empirics better than 2:1. Naively scaled to the full 1,170-record frame that is roughly
95 empirical-primary and 205 theory. More striking: exactly **one** record in 200 carried a realized-
fertility outcome (one further record carried both levels). The stated-intention/realized split is not
merely skewed, it is close to degenerate. This is a finding to report, not a defect to fix — but it does
mean the realized-fertility pool may not be poolable at all, which is worth knowing now rather than at A7.

## Defects, ordered by how much corpus they distort

**1. `THEORY`'s verdict polarity is undefined. (All 5 screeners; governs 21 of 35 RELEVANT.)**
The preamble says to *preserve* the anti-natalist and climate-anxiety-psychometric streams; the verdict
rules define `RELEVANT` only for papers with a fertility estimand, which `THEORY` papers by definition
lack. All five screeners independently resolved this as `RELEVANT` + `THEORY`, and all five flagged that
a screener reading the verdict rules literally would have said `NOT_RELEVANT`. That the five agreed is
luck, not rubric design; across 25 more batches it would not hold.

**2. There is no cell for "insufficient information." (4 screeners.)**
`estimand_cell: NA` is restricted to `NOT_RELEVANT`, so every abstract-less record a screener cannot
exclude must be assigned a substantive cell it has not earned. Batch 1 parked six such records in
`THEORY`; batch 5 used `OFF_OUTCOME` "purely as a placeholder." This mechanically inflates cell counts
with records nobody has information about — and `THEORY` is absorbing most of the inflation, which
contaminates defect 1.

**3. Rule 5 orphans genuine reviews of the core estimand. (2 screeners, both severe.)**
Rule 5 forbids a PRIMARY cell for reviews, but a systematic review of climate concern → reproductive
decision-making is squarely the D.3.b question and has nowhere honest to go. Batch 1 forced one into
`THEORY` ("semantically wrong"); batch 2 forced another into `DESIRE_INDEPENDENCE` and called it, in its
own words, "a lie of convenience." The second failure is the worse one: it corrupts the value-added cell,
which is the whole point of the hypothesis.

**4. `THEORY` as written admits non-ecological anti-natalism. (1 screener, but flood risk.)**
The cell reads "anti-natalist / eco-ethics philosophy" disjunctively, so Benatar/Kantian harm-of-existence
philosophy qualifies with no ecological content whatsoever — contradicting Wall 2's own logic that the
feared object must be specifically ecological. That is a large literature and it will pour in.

**5. Rule 7's `THEORY`/`OFF_OUTCOME` split is undecidable for the literature's largest class. (3 screeners.)**
Papers where climate anxiety is itself the *dependent variable*. Rule 7 defines `OFF_OUTCOME` as a
construct "applied to a non-fertility outcome," which does not cover climate-anxiety-as-outcome studies,
leaving them homeless. Batch 1 sent two structurally near-identical papers to opposite cells.

**6. Rule 2 (`outcome_level`) contradicts `UNCERTAIN`. (3 screeners.)**
`outcome_level` is mandatory on every UNCERTAIN empirical paper, but `NA` is reserved for theory and
NOT_RELEVANT. A record that is UNCERTAIN *precisely because* the outcome is unknown cannot be expressed
without overstating. Screeners split between violating the letter of the rule and guessing.

**7. The `OFF_*` cells are being used as a wastebasket. (2 screeners.)**
They are routing labels that put papers in a sibling hypothesis's queue. Batch 5 routed "childfree in
Islamic law" to `OFF_POSTMATERIALIST_D1a`; batch 3 routed partisanship→fertility desires there too, while
noting "partisanship is not postmaterialism," and forced a mixed-factor postponement scale into
`OFF_CLINICAL_D3a`. Left alone, this ships junk to D.1.a and D.3.a.

**8. Generic future-pessimism has no tiebreak. (2 screeners.)**
Youth surveys citing "the turbulent state of the world" — a feared object named as neither climate nor
economics — sit exactly on the Wall 1 / Wall 3 seam. Relatedly, batch 3 found the mirror-image trap: a
paper motivated on "environmental cataclysm" whose *reported* reasons are financial and freedom-related.
Wall 1 should say explicitly that climate framing with non-climate reported reasons routes off.

**9. Rule 3's seam is unresolved. (1 screener.)** Physical exposure in the treatment, attitudinal in the
outcome — climate disasters → intentions to remain childless. Rule 3 excludes exposure studies "with no
affective/attitudinal mechanism"; here the outcome is attitudinal but the mechanism is not affective. The
rule must say which side wins. (Otherwise rule 3 performed well: it cleanly excluded EDC, traffic-
pollution, and heat-to-birth-outcome epidemiology across several batches.)

**10. `REVERSE` is nearly unusable and its verdict is unstated. (2 screeners.)** It covers parenthood
*status* → climate concern, but real papers run through lived experience and generativity. Both screeners
routed such papers to `OFF_OUTCOME` instead.

**11. No home for conflict/war-driven insecurity. (1 screener.)** Childbearing under invasion is a
"future looks bad" paper whose feared object is bombardment — routed to `OFF_ECON_C5a` because Wall 3's
option-value language fits, which sends it to the wrong sibling hypothesis.

**12. Title-only policy is unstated. (2 screeners.)** Batch 4 overrode "use UNCERTAIN" twice where the
title states the estimand verbatim, then had to guess `outcome_level`. Batch 3 noted the perverse
consequence: with no policy, the verdict becomes a function of abstract availability rather than content.

## Proposed rubric v2 amendments

Grouped by whether they touch the A1 frozen taxonomy. Items A–F are clarifications that do not change
the cell list; items G–J do change it and need sign-off.

**Clarifications (no taxonomy change):**
- **A.** State that `THEORY` takes verdict `RELEVANT`, and that the theory stream is separated downstream
  and excluded from empirical recall. This matches B.1 step 67's existing assembler design and what all
  five screeners already did. *(Fixes 1.)*
- **B.** Permit `outcome_level: NA` on `UNCERTAIN`. *(Fixes 6.)*
- **C.** Relax rule 5: reviews may take a PRIMARY cell with `evidence_type: review`; the assembler
  excludes reviews from the pooled estimate. Preferable to adding a review cell. *(Fixes 3.)*
- **D.** Narrow `THEORY` to *ecological* anti-natalism and eco-ethics; non-ecological anti-natalism
  routes off. *(Fixes 4.)*
- **E.** Rule 7 rewrite: climate-anxiety-as-dependent-variable → `OFF_OUTCOME`, reserving `THEORY` for
  construct development and philosophy. *(Fixes 5.)*
- **F.** Add three tiebreaks — generic future-pessimism with an unnamed feared object → `UNCERTAIN`;
  climate framing with non-climate reported reasons → route off per Wall 1; physical exposure →
  attitudinal outcome is IN scope (the outcome side wins, since the estimand is about reproductive
  intention). *(Fixes 8, 9.)* Plus a stated title-only policy. *(Fixes 12.)*

**Taxonomy changes (need sign-off):**
- **G.** Add `INSUFFICIENT_INFO`, usable only with `UNCERTAIN`. *(Fixes 2.)*
- **H.** Add `OFF_OTHER` for non-D.3.b papers with no sibling-hypothesis home, so the `OFF_*` routing
  labels stop shipping junk to D.1.a/D.3.a/C.5.a. *(Fixes 7, 11.)*
- **I.** Widen `REVERSE` to parenthood status *or experience* → eco-concern, and state its verdict.
  *(Fixes 10.)*
- **J.** Optional: split `THEORY` into `ECO_ETHICS_THEORY` and `ANXIETY_CONSTRUCT`. Two screeners
  recommended it. Defensible to defer — the split can be made at synthesis from `evidence_type`.

## Re-run implication

Rubric v2 changes verdicts, so batches 001–005 must be re-screened under v2 alongside the other 25;
wave-1 verdicts are diagnostic, not corpus. Cost is 5 agents of the 30 — the audit paid for itself.
