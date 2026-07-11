# TFR Replacement-Based Transition Classification

**Date:** 2026-07-11  
**Status:** adopted for OAS and recommended for future hypothesis chapters  
**Context:** demographic-significance and target-period relevance

## Decision

When classifying a study window as FDT-like or SDT-like, use the country's fertility level during
the study window rather than calendar period or income level alone.

The operational rule is:

- If the first and last available in-window TFR observations are both above 2.1, classify the
  study window as `FDT`.
- If both are below 2.1, classify it as `SDT`.
- If the window crosses from above to below replacement, classify it as `FDT|SDT`.
- If no TFR observation exists in the study window, do not guess; classify it as
  `unclassified_no_tfr` and require human interpretation.
- If the outcome is not fertility, append `_contextual` to the classification because the row
  informs mechanism relevance rather than a direct fertility effect.
- Flag low-fertility settings with binding fertility policy, such as China in the one-child /
  two-child-policy era, for human review even when the mechanical TFR classification is `SDT`.

## Data Handling

Alexandra's `proximate-causes` directory is a read-only data source for this project. Do not write
derived files, caches, or edits there from `fertility-review-causes`. Store all derived transition
classification tables and scripts in the current repository.

For the OAS pass, the primary source is:

`/Users/alexandra/Library/CloudStorage/Box-Box/proximate-causes/code/raw/UN/UN_TFR.csv`

The derived output is:

`output/tables/old-age-security-pension-crowdout-tfr-transition-classification.csv`

## Rationale

Anup's replacement-status rule solves a recurring classification problem: a modern developing
country can be in an FDT-like fertility regime if TFR remains above replacement, while a lower-
fertility setting can be SDT-like even outside the classic OECD calendar sequence. The rule makes
the classification reproducible and prevents the chapter from sorting studies only by country
income or date.

## OAS Consequence

The OAS classification pass yields:

- Brazil: `FDT|SDT`, because the study window crosses from above to below replacement.
- Namibia and postwar United States: `FDT`, because available in-window TFR remains above
  replacement.
- Italy and the China pension/LTCI rows: `SDT`, because available in-window TFR is below
  replacement.
- China rows: human-review flag because fertility was policy-constrained.
- Prussia, Imperial Germany, and U.S. 1850: `unclassified_no_tfr` from the local TFR source;
  historical interpretation should be recorded separately rather than inferred from missing data.
