# OAS Conservative Pooling Rule

**Date:** 2026-07-11  
**Status:** adopted for the current OAS/pension-crowdout pass  
**Context:** old-age security / pensions and fertility pilot

## Decision

For the OAS chapter, coefficient estimates are pooled only when all included rows share:

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

## Rationale

The OAS evidence includes credible quasi-experimental estimates, but they do not estimate one
common treatment contrast. The current candidate numeric families mix binary pension expansions,
continuous pension-value exposure, pension cuts, LTCI pilots, financial access, and broad social
spending. A single coefficient-pooled estimate across those contrasts would be hard to interpret
and would overstate comparability.

## Consequence for the Current OAS Extraction

The current extraction has two numeric families with enough rows for screening calculations:

- one-year birth probability,
- completed fertility / children ever born.

Both are retained as structured quantitative narrative rather than coefficient-pooled estimates
because both mix harmonized treatment scales. The inverse-variance calculations in the readiness
table are screening diagnostics only.

## Future Use

If a future extraction adds at least three independent studies within the same outcome family and
the same harmonized treatment scale, the pipeline may report a fixed-effect same-scale screening
estimate for that subset. Random-effects or subgroup models should only be added after there are
enough substantively comparable rows to estimate heterogeneity without pretending incompatible
treatment contrasts are exchangeable.
