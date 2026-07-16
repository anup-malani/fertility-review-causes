# Blinded title/abstract screening rubric — child-labor laws and compulsory schooling

## Review question

Do binding child-labor restrictions, minimum-working-age rules, compulsory-attendance laws, or
school-leaving-age mandates causally affect fertility during or around the First Demographic
Transition? Preserve theory and policy first-stage evidence, but route it outside the primary
fertility estimands.

Judge only the supplied title and abstract. Discovery channel and anchor status are intentionally
hidden. When the abstract is missing or cannot distinguish a plausible relevant paper, use
`UNCERTAIN`; do not infer findings from author, journal, or title fragments.

## Required output

Return one JSON array, in input order, with exactly one object per paper:

```json
{
  "paperId": "copy exactly",
  "verdict": "RELEVANT | UNCERTAIN | NOT_RELEVANT",
  "estimand_cell": "PRIMARY_CL_QUANTUM | PRIMARY_CS_QUANTUM | PRIMARY_JOINT_QUANTUM | TEMPO | THEORY | OFF_OUTCOME | OFF_EXPOSURE | MODE_PRODUCTION | REVERSE | NA",
  "treatment": "short phrase or n/a",
  "outcome": "short phrase or n/a",
  "direction": "forward | reverse | n/a",
  "evidence_type": "quasi-experimental | observational | structural | theory | review | mechanism | other",
  "reason": "one concise clause grounded in title/abstract"
}
```

## Verdict rules

- `RELEVANT`: directly studies or models the child-labor/schooling-law–fertility relationship, or
  directly estimates whether the relevant laws changed work/attendance (a required mechanism first
  stage).
- `UNCERTAIN`: plausibly belongs, but missing/ambiguous information prevents confident routing.
- `NOT_RELEVANT`: does not study the covered legal-policy mechanism. General education–fertility,
  child-labor prevalence, or schooling studies are not automatically relevant.

## Estimand cells

- `PRIMARY_CL_QUANTUM`: binding child-labor restriction/minimum working age → completed fertility,
  children ever born, parity, or cohort fertility.
- `PRIMARY_CS_QUANTUM`: compulsory attendance/school-leaving mandate → the same quantum outcomes.
- `PRIMARY_JOINT_QUANTUM`: inseparable joint child-labor and schooling reform → quantum fertility.
- `TEMPO`: covered reform → teenage birth, age at first birth, or timing only. Use this even if the
  paper casually calls timing “fertility.”
- `THEORY`: formal/conceptual model of regulation, child labor/schooling, and fertility, without an
  empirical policy effect on fertility.
- `OFF_OUTCOME`: covered law → schooling, child labor, wages, health, or growth without fertility.
- `OFF_EXPOSURE`: education/school expansion → fertility without legal-policy variation.
- `MODE_PRODUCTION`: productive value of children/subsistence technology without the covered law;
  route to the agricultural-mode-of-production hypothesis.
- `REVERSE`: fertility/family size → demand for, adoption of, or response to regulation.
- `NA`: only with `NOT_RELEVANT`.

## Precision rules

1. A policy variable and a fertility outcome must both be present for a PRIMARY or TEMPO cell.
2. Education instrumented by a schooling law is `OFF_EXPOSURE` if the paper interprets only the
   effect of education and does not identify/report the policy effect relevant to this hypothesis.
3. Do not turn an `OFF_OUTCOME` first-stage paper into PRIMARY merely because fertility is mentioned
   as motivation.
4. Do not combine tempo and quantum. If both are reported, use the relevant PRIMARY quantum cell and
   mention tempo in `reason`.
5. Reviews may be `RELEVANT` but cannot be PRIMARY; use the best non-primary cell and
   `evidence_type=review`.
