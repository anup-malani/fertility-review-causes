# Demographic significance — microplastics-pfas-reproductive (B.6)

Computed once per chemical family, as Call 1 requires. Inputs are fetched, not asserted: the exposure change comes from a full text held in this chapter (`W4406683543`, NHANES 1999–March 2020) and the fertility series from World Bank WDI `SP.DYN.TFRT.IN`, cached to `data/raw/worldbank-usa-tfr.json`.

## PFAS — the verdict is a sign, not a magnitude

Over **1999–2020**, US serum concentrations of the legacy compounds fell steeply:

| compound | decline in serum geometric mean |
|---|---|
| PFOS | **−87%** |
| PFOA | **−74%** |
| PFHxS | **−52%** |

Over the same window US TFR moved **2.007 → 1.641**, a change of **-18.2%**.

**The exposure and the outcome moved in the same direction, and the hypothesis requires them to move in opposite directions.** If PFAS suppress fertility, then an 87% fall in PFOS should have *raised* fertility across precisely this window. Fertility fell by 18%.

Taking the largest unrestricted association in the extraction table at face value — S-PRESTO's fecundability ratio of 0.88 per quartile increase — and reading an 87% concentration decline as roughly 3 quartile steps downward, the implied change is a fecundability *gain* of about **+47%**. The hypothesis, granted its own contested estimate, predicts the post-2000 US fertility decline should not have happened.

### Three reasons that upper bound is still too generous

1. **The estimate does not survive parity handling.** The extraction found that in both cohorts that ran a parity-restricted analysis, the association was not replicated (INUENDO) or was null (MoBa). The figure above uses a number the chapter's own evidence says is substantially reverse-causal.
2. **A fecundability ratio is not a fertility quantity.** It moves time-to-pregnancy. It converts into completed family size only where the reproductive span binds, which for most exposed person-time it does not. The scope document pre-committed to keeping `HAZARD_DECREMENT` and `TEMPO_ADJUSTED_QUANTUM` apart for exactly this reason, and no record in the extraction table carries the latter.
3. **The quartile arithmetic is an illustration, not a calibration.** Mapping a percentage concentration change onto quartile steps of a right-skewed distribution is rough, and it is done here only to show that the sign problem is not marginal.

### PFAS_REPLACEMENT — a separate arm, and unresolved

The falling series is the LEGACY compounds. Short-chain and replacement substances (GenX/HFPO-DA, PFO4DA, other precursors) entered use as the legacy ones were phased out, and NHANES did not measure most of them across this window. **The replacement arm's exposure series is therefore unknown, not flat**, and the chapter must say so rather than let the legacy decline stand for the whole family. The screen found mechanism work on replacements (`W7134253977` on GenX, `W4407964415` on PFO4DA, `W4205205091` on legacy vs replacement endocrine disruption) but no exposure series and no fertility estimate.

### Verdict — PFAS

**Demographically insignificant for the post-2000 period, on a sign argument that does not depend on the effect size.** The legacy exposure fell by most of its 1999 level across the window in which US fertility fell by 18%. Even the contested unrestricted association, applied generously, predicts the opposite of the observed change. The replacement arm is unresolved and is the only route by which a PFAS contribution to recent decline could survive; establishing it requires an exposure series nobody has built.

## Microplastics — not computable, and that is the finding

The demographic-significance calculation is exposure change × effect size. The exposure series is rising: plastic production has grown throughout the SDT and human internal exposure with it. **The effect size does not exist.** The extraction found five reviews and no effect estimate in the primary cell, and five empirical records that estimate fertility *inputs* — sperm parameters, retrieved oocytes, AMH — with p-values clustered at the margin and samples drawn from ART clinics.

Multiplying a well-measured rising exposure by an effect size that has not been estimated produces a number with no content. The chapter reports **not computable** and states why, which is a stronger and more useful claim than a decomposition built on a placeholder.

### Verdict — microplastics

**Not computable. No effect estimate on a fertility quantity exists in a 920-record screen** whose completeness bypass guaranteed every both-axes plastic record was read. The exposure is real, rising, and now measurable inside the reproductive tract; what has not been done is the study that estimates its effect on a fertility outcome in humans. That absence is this half of the chapter's result.

## Why the two verdicts differ in kind

PFAS fails on **evidence that exists and points the wrong way**. Microplastics fails on **evidence that does not exist**. Both are negative verdicts and they are not interchangeable: the first is close to settled for the legacy compounds and could only be reopened by the replacement arm, while the second could be overturned by a single well-designed cohort. A bundled B.6 verdict would have concealed that difference, which is the strongest retrospective argument for the Call 1 split.
