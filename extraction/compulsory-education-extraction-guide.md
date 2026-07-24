# Compulsory-education extraction guide

## Purpose

The original combined search supplies one standalone hypothesis and one nested evidence stream. Run
`source/build/goldset/76_split_compulsory_education_workstreams.py` to regenerate their retrieval
manifests and blank study-level extraction sheets from the RA-approved focused handoff.

The generated sheets are:

- `compulsory-education-child-economic-value-study-extraction.csv`
- `tempo-effects-birth-postponement-compulsory-schooling-study-extraction.csv`

Do not infer blank fields from titles or abstracts. Complete them from the retrieved full text and
record a page, table, figure, or appendix locator in the adjacent `_source` field. Under the
exception-based RA convention, a blank `_ra_decision` approves the extracted value; use `FIX`,
`UNSURE_PI`, or `EXCLUDE` only when action is needed.

## Hypothesis A: child economic value and completed fertility

The causal chain is:

`compulsory education -> less child work -> lower economic value of children -> fewer completed births`

Use these controlled values for `whose_schooling_changed`:

- `PROSPECTIVE_PARENT`
- `FUTURE_CHILD`
- `BOTH`
- `UNCLEAR`

Use these controlled values for `mechanism_classification`:

- `CHILD_ECONOMIC_RETURN`
- `CHILD_QUALITY_COST`
- `WOMENS_OPPORTUNITY_COST`
- `MARRIAGE_BIRTH_TIMING`
- `KNOWLEDGE_PREFERENCES_CONTRACEPTION`
- `MIXED_OR_UNCLEAR`

Use these controlled values for `mechanism_directness`:

- `DIRECT`: the study identifies a child-work first stage and connects it to fertility.
- `PARTIAL`: the study identifies some, but not all, links in the causal chain.
- `REDUCED_FORM`: the law affects fertility but the child-economic-value channel is not isolated.
- `WRONG_MECHANISM`: the estimate concerns another pathway and does not test this hypothesis.

The primary outcomes are completed fertility, children ever born, parity, and childlessness.
Desired fertility is not interchangeable with realized fertility and must be labeled separately.

## Tempo-postponement evidence stream: compulsory schooling and teenage births

This is not a standalone master hypothesis. It is a policy-driver stream under
`tempo-effects-birth-postponement`. Its causal chain is:

`compulsory education -> continued enrollment -> reduced teenage exposure -> fewer or later teenage births`

Use these controlled values for `tempo_outcome_type`:

- `TEEN_PREGNANCY`
- `TEEN_LIVE_BIRTH`
- `TEEN_MOTHERHOOD`
- `AGE_AT_FIRST_BIRTH`
- `AGE_SPECIFIC_FERTILITY`
- `TEEN_MARRIAGE_MEDIATOR`
- `OTHER_TEMPO`

Use `pregnancy_or_live_birth` to prevent conflating conceptions with births:

- `PREGNANCY`
- `LIVE_BIRTH`
- `MOTHERHOOD_STATUS`
- `TIMING_ONLY`
- `UNCLEAR`

Record the exact age cutoff in `age_threshold`. Extract later-age estimates where available so
`effect_duration`, `later_birth_rebound`, and `completed_fertility_followup` can distinguish
postponement from a permanent decline in fertility quantum.

## Routing and synthesis rules

- A study can appear in both workstreams, but its outcomes and risk-of-bias judgments remain
  estimate-specific.
- Do not pool pregnancy and live birth.
- Do not pool desired and realized fertility.
- Do not interpret a teenage-birth reduction as a completed-fertility reduction.
- Do not describe own-schooling estimates as proof of the child-economic-value mechanism.
- Separate PRISMA counts will be generated after the full 1,255-record RA exception review and
  production keyword search are complete.
