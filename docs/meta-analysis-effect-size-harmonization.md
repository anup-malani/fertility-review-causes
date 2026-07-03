# Effect-Size Harmonization Rules

**Status:** draft  
**Scope:** fertility-explanations meta-analysis chapters  
**Pilot:** old-age-security / pension crowdout of fertility

## 1. Purpose

Meta-analysis requires comparable estimands. Fertility papers report effects in many units:
birth probabilities, completed fertility, TFR, parity progression, fertility intentions,
contraceptive use, and non-fertility family investments. This document defines how to preserve
original estimates, when to harmonize them, when to pool them, and when to keep them in narrative
synthesis only.

## 2. Estimand Hierarchy

Prefer target units in this order:

1. **Births per woman / completed fertility.** Best for demographic significance and slope
   sufficiency.
2. **Probability of birth over a defined period.** Pool only with matching or convertible time
   windows.
3. **Parity progression / hazard of next birth.** Pool within parity/time groups only.
4. **TFR or aggregate fertility-rate change.** Use for macro or historical estimates; avoid pooling
   with micro completed-fertility estimates unless the mapping is explicit.
5. **Fertility intentions, contraceptive use, or family investments.** Mechanism evidence unless the
   chapter explicitly defines these as fertility-adjacent outcomes.
6. **Non-fertility outcomes.** Theory/mechanism context only unless they are necessary mediators.

## 3. Original Estimate Preservation

Every extracted estimate keeps:

- Original point estimate.
- Original unit.
- Standard error, confidence interval, or p-value if available.
- Model specification.
- Treatment/exposure scale.
- Source page/table/figure.

Never overwrite original values with harmonized values. Harmonized fields are additional columns.

## 4. Standard Conversions

### Percentage Points to Probability Units

If a paper reports a change in probability in percentage points:

```text
effect_harmonized = effect_original / 100
se_harmonized = se_original / 100
harmonized_outcome_unit = probability_of_birth
```

Use only when the outcome is a probability or binary indicator.

### Births per 1,000 Women to Births per Woman

```text
effect_harmonized = effect_original / 1000
se_harmonized = se_original / 1000
harmonized_outcome_unit = births_per_woman
```

Use when the denominator is explicitly women, not population.

### Log Fertility Outcomes

For small log changes, approximate percent change:

```text
percent_change = 100 * (exp(effect_original) - 1)
```

Do not convert log changes to births per woman without a baseline fertility level. If baseline is
available:

```text
births_per_woman_change = baseline_births_per_woman * (exp(effect_original) - 1)
```

Flag `needs_pi = yes` if the baseline must be chosen from outside the paper.

### Treatment Effects per Binary Reform Exposure

If treatment is an eligibility/reform indicator, the harmonized treatment scale is:

```text
treatment_scale_harmonized = treated_vs_control
```

Do not rescale to dollars of pension wealth unless the paper reports a first-stage or treatment
intensity conversion.

### Treatment Effects per Monetary Pension Change

If treatment is continuous pension income or pension wealth:

```text
effect_per_1000_local_currency = effect_original * 1000
```

Only use within-country synthesis unless currency, price year, and exchange/PPP conversion are
explicitly documented. For cross-country pooling, convert to PPP-adjusted 2020 USD and set
`needs_pi = yes`.

## 5. Pooling Rules

Pool estimates only if all conditions hold:

1. Same outcome family after harmonization.
2. Same treatment scale or defensible conversion.
3. Comparable time horizon.
4. Independent study units, or robust variance/cluster handling is implemented.
5. Risk-of-bias profile is not dominated by `critical` studies.

Do not pool:

- A completed-fertility estimate with a one-year birth probability without a formal conversion.
- Fertility estimates with contraceptive-use outcomes.
- Pension-as-old-age-security effects with grandparent-childcare effects unless the estimand is
  clearly labelled as a broader pension/fertility pathway.
- Multiple specifications from the same study as if they were independent.

## 6. Preferred Estimate Selection

For each study/outcome pair, choose one primary estimate for the main synthesis:

1. Authors' preferred causal specification.
2. Estimate with the clearest old-age-security mechanism.
3. Estimate with the most policy-relevant fertility outcome.
4. Estimate with the longest follow-up for completed fertility, or the pre-specified short-run
   window for birth probability.

Robustness estimates remain in the extraction table and may enter sensitivity analyses.

## 7. Sensitivity Analyses

At minimum, report:

- Main estimate only vs. all compatible estimates.
- Published version only vs. working-paper version if both contain different details.
- Excluding high/serious risk-of-bias studies.
- Excluding non-primary mechanism studies, such as grandparent-childcare channels in an
  old-age-security chapter.
- Fixed-effect vs. random-effects model when pooling is possible.

## 8. Escalation Triggers

Escalate to PI before synthesis if:

- A conversion changes the sign or practical significance of the effect.
- Baseline fertility must be imported from external macro data.
- Treatment scale requires currency/PPP conversion.
- A study reports multiple plausible primary estimates with different implications.
- A fertility-adjacent outcome is the only evidence for a target phenomenon.
- A published version and working paper disagree.

## 9. Reporting Language

Use Cochrane/GRADE certainty language for evidence strength and JEL-style prose for interpretation.

Examples:

- "Moderate-certainty quasi-experimental evidence suggests pension eligibility reduces completed
  fertility by roughly X births per woman in settings where children are an important old-age
  support asset."
- "The estimate is causally credible but demographically too small to explain more than a minor
  share of the observed SDT decline under plausible exposure changes."
- "The evidence is mechanism-relevant but not directly poolable because the outcome is
  contraceptive use rather than fertility."
