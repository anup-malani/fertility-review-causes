# Compulsory-Education Second Review Instructions

Reviewer: Alexandra  
Review unit: one empirical paper per row  
Review sheet: `output/compulsory-education-second-review-sheet.csv`

## Before reviewing

Do not consult `extraction/compulsory-education-accessible-risk-of-bias-preliminary.csv` or the
provisional GRADE sections in the chapter drafts until the sheet is complete. The review sheet
contains study facts and source locators but omits the first reviewer's judgments.

## Complete every row

Use `INCLUDE`, `EXCLUDE`, or `UNCLEAR` for `include_decision`. Classify the mechanism in plain
language, paying particular attention to whether the treatment changes the prospective parent's
own schooling or the expected work value of future children.

For each risk-of-bias domain, use `LOW`, `MODERATE`, `SERIOUS`, `CRITICAL`, or `NO_INFORMATION`:

- confounding
- selection or sorting
- treatment classification
- outcome measurement
- missing data
- selective reporting
- overall risk of bias

Give a short evidence-based explanation in `rob_rationale`, citing a table, page, or section when
possible.

Then assess directness, precision, consistency, and publication-bias concern. Enter a suggested
GRADE level (`HIGH`, `MODERATE`, `LOW`, or `VERY_LOW`) and explain it. The row-level GRADE entry is
your view of how that study contributes to its assigned evidence stream, not a mechanical average
of bias domains.

For demographic significance use `LARGE`, `MODERATE`, `SMALL`, `NEGLIGIBLE`, or
`INSUFFICIENT_DATA`, with a short rationale. Mark `needs_pi_decision=YES` only for a genuine
protocol, routing, or interpretation dispute.

## Stream-level judgments

After completing all rows, add two final lines to `reviewer_notes` in any row from the relevant
stream:

1. `STREAM_GRADE_CHILD_VALUE: [rating] — [reason]`
2. `STREAM_GRADE_TEMPO_SCHOOLING: [rating] — [reason]`

Save the completed CSV in place and tell Codex it is ready. Codex will compare it against the first
review, produce a disagreement table, and route only unresolved material judgments to the PI.
