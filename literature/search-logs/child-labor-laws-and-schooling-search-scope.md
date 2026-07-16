# Search scope — child-labor laws and compulsory schooling

**Ticket:** TICK-031  
**Hypothesis slug:** `child-labor-laws-and-schooling`  
**Target phenomenon:** First Demographic Transition (FDT)  
**Status:** cold-start scope frozen before query construction; gold anchors not yet RA-frozen

## Causal claim

Legal restrictions on child labor and compulsory-schooling mandates reduce the expected economic
return from children and/or increase required human-capital investment, causing parents to choose
fewer births. The policy may also delay births without reducing completed fertility; tempo and
quantum effects must therefore remain distinct.

## Estimand cells

| Cell | Treatment | Fertility outcome | Routing |
|---|---|---|---|
| `PRIMARY_CL_QUANTUM` | Binding child-labor restriction or higher minimum working age | Completed fertility, children ever born, parity, cohort fertility | Primary synthesis |
| `PRIMARY_CS_QUANTUM` | Binding compulsory-attendance or school-leaving-age law | Completed fertility, children ever born, parity, cohort fertility | Primary synthesis |
| `PRIMARY_JOINT_QUANTUM` | Reform jointly changing child-labor and schooling constraints | Same quantum outcomes | Primary, reported separately unless components are identified |
| `TEMPO` | Any covered reform | Age at first birth, teenage birth, birth timing only | Structured secondary synthesis; do not pool as completed fertility |
| `THEORY` | Model of child labor/schooling regulation and fertility choice | No empirical fertility estimate | Theory stream |
| `OFF_OUTCOME` | Covered reform | Schooling, child labor, wages, health, or growth without a fertility outcome | Mechanism/context only |
| `OFF_EXPOSURE` | Education attainment or schooling expansion without legal-policy variation | Any fertility outcome | Route to education/quality-quantity literature |
| `MODE_PRODUCTION` | Subsistence technology or children's productive value without a legal reform | Any fertility outcome | Route to TICK-030 |
| `REVERSE` | Fertility affects demand for or adoption of regulation | Law/policy outcome | Theory/context, not causal effect sought here |

## Eligibility rules

- Include empirical studies only when the treatment is a child-labor rule, compulsory-schooling
  rule, minimum working age, school-entry/exit mandate, or a clearly identified joint reform.
- Preserve historical FDT evidence even when modern microdata are used to recover affected cohorts.
- Record enforcement and first-stage effects wherever available; a law on the books that did not
  change work or attendance is not equivalent to a binding treatment.
- Keep theory papers and mechanism-only first-stage papers discoverable but outside the empirical
  primary-cell recall denominator.
- Treat teenage births and postponement as tempo evidence unless completed fertility is also shown.
- Do not combine the mode-of-production hypothesis with this legal-policy estimand.

## Cold-start channels and leakage wall

1. Direct empirical papers identified independently from the hypothesis list and bibliographic
   searches seed the empirical Tier-A candidate set.
2. Canonical theory papers seed the theory set but do not count toward empirical recall.
3. References and citations of the independent seeds create the orthogonal Tier-B candidate frame.
4. Production-query terms will not be mined from a paper and then evaluated on that same paper;
   learned extensions must be fold-local after the gold frame exists.

## Pre-query anchor audit (not yet the frozen gold)

The initial verified set is stored in
`child-labor-laws-and-schooling-cold-start-anchors.json`. It deliberately contains primary,
tempo, theory, and off-outcome anchors so the eventual search is tested on routing as well as topical
retrieval. Bibliographic identity is verified against publisher/NBER/RePEc pages; substantive
eligibility remains subject to abstract/full-text screening and RA freeze.

