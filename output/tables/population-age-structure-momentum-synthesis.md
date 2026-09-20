# Stage 9 — Quantitative synthesis: age structure / demographic momentum (A.9)

**Prepared:** 2026-09-20, Shravan (TICK-089). **Inputs:** `extraction/population-age-structure-momentum.csv`
(10 of 16 included studies retrieved and extracted; 6 not procurable — see the extraction report).
**Form:** structured quantitative synthesis, **not a pooled meta-analytic estimate** (justified below).

## Why not a pooled estimate

PROTOCOL §5 stage 9 pools with `metafor` when there are ≥3 studies with **comparable effect sizes**.
A.9 fails the comparability precondition on three independent counts, so pooling a single number would be
a category error (the TICK-080 item-8 "never pool across outcome levels" rule, plus the non-effect-estimand
nature of the estimand):

1. **The estimand is a decomposition share, not an effect size.** There is no treatment and no
   counterfactual contrast; each study reports what fraction of an observed change it *attributes* to the
   age-structure component. Shares are not variance-weightable like effect sizes.
2. **The outcome level differs across studies** — share of a CBR change, contribution to a birth *count*,
   an age-composition *multiplier* on the birth rate, and the momentum share of the *growth* rate are
   different quantities on different scales.
3. **The sign is not fixed** — the age-structure component *raised* the CBR in some settings and *lowered*
   it in others (see below), so an unsigned pool is meaningless and a signed pool averages opposites.

The defensible synthesis is therefore the **distribution of the age-structure share and its moderators**,
reported per outcome, with the sign preserved.

## Harmonized evidence table (10 studies)

Age-structure/composition contribution to the observed change in the stated outcome. "Share" = fraction
of the observed movement attributed to the age-structure component; sign = direction the component pushed
the outcome.

| Study | Setting | Period | Outcome | Age-structure contribution | Sign | Method | Regime |
|---|---|---|---|---|---|---|---|
| Freedman 1968 (A9-16) | Hong Kong | 1961–65 / 1961–66 | CBR | **~80%** (1961–65); ~50% (1961–66) | − (reduced CBR) | standardization | momentum-dominant |
| Palamuleni 2011 (A9-09) | South Africa | 1996–2001 | CBR | **+60%** | + (raised CBR) | std./decomposition | composition-dominant |
| Chaurasia 2017 (A9-07) | China / India | 1950–2015 | natural growth / CBR | momentum ≈ **80%** of India growth 2010–15, >100% China; CBR multiplier 1.01–1.21 | + (inflated) | Kitagawa | momentum-dominant |
| A9-03 | South Korea | ~1990–2015 | CBR | −0.37 of the change (vs −2.26 marriage); **~2.9%** | − | additive decomposition | marriage-dominant |
| A9-02 | China | 2012–19 | births (count) | size-of-women −150 to −340k; **secondary** | − | multiplicative (4-factor) | marriage-dominant |
| A9-05 | South Korea | –2017 | births (count) | **secondary** contributor | − | decomposition | marriage-dominant |
| A9-08 | Malawi | 1992–2015 | TFR / CBR | **small residual (~0–20%)** | ± small | std./decomposition | marital-fertility/nuptiality-dominant |
| A9-10 | USA | 1970–99 | GFR | age distribution **compensated** (offset marriage decline) | + | 4-component decomposition | compensating |
| A9-11 | USA | 1960–92 | nonmarital fertility ratio | component present; older-age shift post-1980 | period-dependent | Das Gupta | mixed |
| A9-15 | USA | 1920–30 | CBR / specific rates | age-composition shift documented | descriptive | comparative | descriptive |

## Quantitative synthesis

**Magnitude.** The age-structure share of an observed CBR/birth-count movement spans essentially the
whole possible range across settings: from **~0–3%** (Malawi in some intervals; South Korea ~2.9%) to
**~60–100%** (South Africa +60%; Hong Kong ~80% of the 1961–65 decline; China/India momentum ~80–100% of
growth). There is no central tendency worth reporting as "the" A.9 effect; the dispersion *is* the result.

**Sign.** The component is signed both ways and the sign is informative:
- **Negative** (age structure reduced the CBR/births) where a shrinking or aging reproductive-age
  population coincided with fertility decline — Hong Kong 1961–65, South Korea, China 2012–19.
- **Positive** (age structure raised or propped up the CBR) where a youthful, momentum-laden structure
  inflated the crude rate — South Africa 1996–2001, China/India momentum, and the US, where the age
  distribution *compensated* for declining marriage and helped keep the GFR flat 1970–99.

**Moderators of the magnitude** (read off the regime column):
1. **Distance of the age structure from stationarity (momentum).** The share is largest where the
   population carries strong positive or negative momentum — post-transition youthful bulges (Hong Kong,
   South Africa, China/India) — and smallest in slower or marriage-driven transitions.
2. **Length of the observation window.** Composition dominates *short-run* CBR movements (Hong Kong's
   five-year window: ~80%) and recedes over longer or behaviourally-driven intervals.
3. **What else is moving.** Where marriage and marital fertility carry the change (Malawi, Korea, China
   2021), age structure is a minor residual; where behaviour is comparatively stable, composition is the
   majority of the measured movement.

**Outcome dependence (the load-bearing result).** Every non-trivial age-structure contribution above is
on a **crude or count measure** — the CBR, the number of births, or the growth rate. For the **period
TFR and completed cohort fertility the contribution is zero by construction**, and Chaurasia 2017
confirms this analytically (its `f = w × TFR/35` isolates the composition multiplier from the TFR). So
A.9's demographic significance lives entirely in the crude/count outcomes and vanishes in the quantum
measures — which is precisely the per-outcome split the scope and TICK-080 (items 6–7) require the verdict
to report.

## Limitations

- **10 of 16 included studies retrieved.** Six were not procurable (China 2014; Korea 2023; South Africa
  2019 thesis; the China 1991 PDR paper — a Genus 1993 substitute was found but is a parity decomposition,
  not age-structure; Mexico 1991; India 1983 is a scanned no-OCR image). The retrieved set still spans
  China, Korea, USA, South Africa, Hong Kong, Malawi, India across 1932–2024, so the qualitative pattern is
  unlikely to reverse, but the missing East-Asian and Latin American items could sharpen the marriage-vs-
  composition split.
- **Heterogeneous decomposition methods** (Kitagawa, Das Gupta, standardization, bespoke multiplicative)
  and outcome definitions; harmonization is at the level of the reported share, not re-computed.
- **Two studies are qualitative/partial** (A9-05 Korean-language, A9-10, A9-11, A9-15): direction is firm,
  exact component values still to be pinned from tables.

## Feeds into

- **Stage 10 (demographic significance):** report per outcome — CBR/births: significant and often
  dominant *but setting- and period-specific* (range ~0 to ~100%, both signs); period TFR / CCF: **zero by
  construction**. Do not print a single significance label (TICK-080 item 6).
- **Stage 11 (GRADE): NOT RATEABLE — non-effect estimand** (TICK-080 item 5); the evidence is sound
  decomposition arithmetic, not an identification strategy.
- A **figure** for the chapter: an ordered, signed dot/range plot of the age-structure share by
  setting/period, faceted by outcome (CBR/births vs growth), rather than a forest plot (which would imply
  a poolable common effect).
