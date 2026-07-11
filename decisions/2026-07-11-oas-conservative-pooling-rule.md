# OAS Conservative Pooling Rule

**Date:** 2026-07-11  
**Status:** amended for the current OAS/pension-crowdout pass
**Context:** old-age security / pensions and fertility pilot

## Decision

For the OAS chapter, a strict same-treatment pooled estimate is reported only when all included rows
share:

- the same mechanism cell,
- the same outcome family,
- the same harmonized outcome unit,
- the same harmonized treatment scale,
- usable oriented effect estimates and standard errors,
- at least three independent studies.

Eligible effects must already be oriented so the coefficient means the fertility effect of more
non-child old-age security. Original treatment direction is not a separate pooling key after this
orientation step; treatment-scale labels capture whether the contrast is a pension expansion,
pension cut, financial-access expansion, LTCI pilot, or broader social-spending exposure.

The chapter also reports a second, looser quantitative object: **outcome-specific fixed-effect
inverse-variance summaries**. These are allowed when rows share the same mechanism cell, outcome
family, harmonized outcome unit, usable oriented effect, and usable oriented standard error, even if
the harmonized treatment scale differs. They must be labeled as outcome-family summaries rather than
as one structural treatment effect.

## Rationale

The OAS evidence includes credible quasi-experimental estimates, but they do not estimate one
common treatment contrast. The current candidate numeric families mix binary pension expansions,
continuous pension-value exposure, pension cuts, LTCI pilots, financial access, and broad social
spending. A single coefficient-pooled estimate across those contrasts would be hard to interpret
and would overstate comparability.

## Consequence for the Current OAS Extraction

The current extraction has two classic old-age-security numeric families with enough usable rows for
outcome-specific fixed-effect summaries:

- one-year birth probability: pooled oriented effect = -0.006954 on the probability-of-birth scale
  (SE 0.002037; 95% CI -0.010946 to -0.002963; five independent studies),
- completed fertility / children ever born: pooled oriented effect = -0.067672 births per woman
  (SE 0.026971; 95% CI -0.120536 to -0.014808; three independent studies).

Both remain too heterogeneous for a single same-treatment pooled coefficient because both mix
harmonized treatment scales. The reported pooled values are therefore outcome-specific quantitative
summaries. They should be used to summarize direction and approximate magnitude within outcome
family, not as a universal estimate of "the effect of pensions."

## Future Use

For future hypotheses, report both layers when data permit:

1. A same-treatment pooled estimate when mechanism, outcome, unit, treatment scale, and standard
   errors match.
2. An outcome-specific pooled summary when mechanism, outcome, and unit match but treatment scales
   differ.

Random-effects or subgroup models should only be added after there are enough substantively
comparable rows to estimate heterogeneity without pretending incompatible treatment contrasts are
exchangeable.
