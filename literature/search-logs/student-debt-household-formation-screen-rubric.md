# Title/abstract screening rubric — C.3.g student debt and household formation

**Hypothesis (HYPOTHESES-v5 §C.3.g):** education debt service during prime childbearing years
reduces the household resources available for family formation — delaying or blocking marriage,
homeownership, and childbearing — in cohorts that came of age under the post-2000 student-debt
regime. Target phenomenon: **SDT only**.

You see title, venue, year, type and a truncated abstract. You do NOT see the deterministic score,
the rank, or why the record reached the worklist. That is deliberate: your reading and the term
matches must stay independent so assembly can cross-check them.

Return one JSON object per record, with these fields.

## `verdict` — RELEVANT | UNCERTAIN | NOT_RELEVANT

- **RELEVANT** — reports an empirical relationship between a young adult's OWN education debt and
  fertility, union formation, or housing/residential independence. Include studies whose estimate is
  associational; identification is recorded separately, not required.
- **UNCERTAIN** — plausibly in scope but the abstract does not settle it, OR the record is
  title-only and the title is not decisive.
- **NOT_RELEVANT** — a different exposure, a different outcome, or no empirical relationship at all.

## `exposure` — own_student_debt | parent_held_debt | general_debt | tuition_or_aid_policy | none | cannot_tell

Whose balance sheet the debt sits on is the chapter's sharpest boundary. `parent_held_debt` (Parent
PLUS, borrowing for a child's degree) sits on the older generation and cannot delay the borrower's
own childbearing. `general_debt` is credit-card, mortgage, medical or consumer debt — that is C.3.e
and C.2.c, not this chapter.

## `outcome` — fertility | union_formation | housing_residence | multiple | other | none

`fertility` = births, first birth, completed fertility, childlessness, fertility intentions.
`multiple` = more than one of the three in the estimated outcomes, which is the case that cannot be
routed at screen.

## `arm` — direct | chain | mechanism | off | cannot_tell

- **direct** = own education debt → a FERTILITY outcome. The registered estimand.
- **chain** = own education debt → marriage, homeownership or residential independence. In scope
  because v5's claim names these as the mechanism, but a DIFFERENT proposition.
- **mechanism** = debt → earnings, savings, occupational choice, liquidity. Evidence about the
  resource channel itself; not evidence for a fertility effect.
- **off** = neither.

## `design` — identified | associational | descriptive | qualitative | review | simulation | cannot_tell

`identified` requires a named strategy the abstract states: an experiment, DiD, IV, RD, event study,
policy discontinuity. **The most important record in this frame is titled "Experimental Evidence
on ... Responses to Student Debt Forgiveness"** — a design list that cannot see it is useless.

## `attain_conditioned` — yes | no | cannot_tell

Does the study hold educational ATTAINMENT fixed (compare borrowers to non-borrowers with the same
degree), or does it compare people with different amounts of schooling? Expect `cannot_tell` often;
that is information, not failure.

## `wall` — none | w1_career | w2_general_debt | w3_repayment | w4_access_to_college | w5_6_parent_balance | w7_lmic | w8_reverse

- `w1_career` — health-professions debt studied for SPECIALTY or CAREER choice. **Route by outcome,
  not by topic:** a study of medical students that reports childbearing decisions is IN, and takes
  `wall: none`. Only the ones whose estimated quantity is a career, a specialty or a practice
  location are walled.
- `w7_lmic` — school fees and child marriage in low-income settings. Different exposure, different
  outcome, different phenomenon. Tag it; it is never deleted.
- `w8_reverse` — childbearing as a CAUSE of debt (student parents borrowing more).

## `info` — sufficient | insufficient

`insufficient` whenever the record is title-only and the title is not decisive, or the abstract is
too vague to answer the fields above. **A title-only record is not a negative verdict.** Returning
NOT_RELEVANT because you could not see the abstract records "not visible" as "not relevant".

## `note` — one short clause, only when the record is a boundary case worth an RA's eye

Output format, one line per record:

```json
{"id": "W1234567890", "verdict": "RELEVANT", "exposure": "own_student_debt", "outcome": "fertility",
 "arm": "direct", "design": "associational", "attain_conditioned": "cannot_tell", "wall": "none",
 "info": "sufficient", "note": ""}
```
