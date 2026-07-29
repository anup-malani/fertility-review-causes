# Contraception-absent pool, re-run — B.1 Evolutionary Sex Drive and Contraceptive Decoupling

This file documents the re-pool of the contraception-absent cell of the status-and-reproduction
association, and the two sex-by-availability crossings the chapter reports. It exists because
`source/analysis/b1_meta_pipeline.py` reads only `extraction/…-effects.csv`, where the
contraception-absent cell holds one study, and because the pipeline computes three groupings
(overall, by availability, by sex) and never crosses sex with availability.

Everything below is computed by hand under the pipeline's own method, from values already recorded
in `extraction/evolutionary-sex-drive-contraceptive-decoupling-effects-workflow.json` and
`extraction/evolutionary-sex-drive-contraceptive-decoupling-effects.csv`. No PDF was re-read; no
value was re-extracted. Every input carries the workflow record it came from.

---

## 1. Method

Identical to `b1_meta_pipeline.py`:

- **Metric.** Fisher-z. A Pearson `r` enters as `z = atanh(r)` with variance `1/(n − 3)`. A value
  already reported as a Fisher-z (`zr`) enters directly, with variance taken from its confidence
  interval as `((hi − lo) / (2 × 1.959964))²`.
- **Pooling.** DerSimonian-Laird random effects. Between-study variance `τ²` from `(Q − df) / C`,
  floored at zero; pooled `z` is the inverse-variance-weighted mean under weights `1/(v + τ²)`;
  the 95% interval is `z ± 1.959964 × SE`, and the pooled `z` and both endpoints are back-transformed
  with `tanh`.
- **Reporting rule.** `MIN_STUDIES = 3`. A cell holding fewer than three studies is reported, not
  pooled.

Two conversions were needed, both standard and both applied to values the extraction already
recorded:

- **Cohen's d to r**, for Courtiol et al. (2012): `r = d / sqrt(d² + 4)`, the equal-group
  point-biserial identity. `d = +0.0449` gives `r = +0.0224`; `d = +0.0221` gives `r = +0.0110`.
- **Several predictors on one sample.** Lebuda et al. (2021) report two zero-order correlations on
  the same 133 people, wealth and years of schooling. Entering both would count the sample twice, so
  the two enter as the mean of their Fisher-z values, with variance `1/(n − 3)` and no gain in
  precision from the averaging. Josephson (1993) likewise reports two outcomes on one sample of 73
  women, children ever born and grandchildren ever born; only the children-ever-born estimate enters,
  because grandchildren are a different outcome from the one the pool defines.

Where a study reports disjoint samples of men and women, each sex enters as its own row, which is how
the five originally pooled studies are handled.

---

## 2. Inputs and weights — headline specification

Four studies, five effect rows, all coded `contraceptive_availability = absent`.

| Study | Sex | Predictor and outcome | Reported statistic | n | Fisher-z | Variance | Weight | Weight share | Record |
|---|---|---|---|---|---:|---:|---:|---:|---|
| von Rueden and Jaeggi (2016) | male | Men's status composite → reproductive success | Zr = 0.19 (95% CI 0.09 to 0.31), 288 associations across 46 studies in 33 nonindustrial societies | — | +0.1900 | 0.003150 | 71.15 | 20.8% | `effects.csv` b1e001 |
| Lebuda et al. (2021) | both | Observer-rated wealth → living children; years of schooling → living children | r = −0.22 and r = −0.56 | 133 | −0.4282 | 0.007692 | 53.77 | 15.7% | W3124469204 |
| Josephson (1993) | female | Husband's status (polygynous marriage) → children ever born | r = −0.328, from t = 2.93 on df 71 | 73 | −0.3406 | 0.014286 | 39.70 | 11.6% | W2163381596 |
| Courtiol et al. (2012) | male | Landowning against landless parental class → lifetime offspring | d = +0.0449 (r = +0.0224) | 3,009 | +0.0224 | 0.000333 | 88.98 | 26.0% | W2117546824 |
| Courtiol et al. (2012) | female | Same | d = +0.0221 (r = +0.0110) | 2,914 | +0.0110 | 0.000344 | 88.90 | 26.0% | W2117546824 |

`Q = 44.29` on 4 degrees of freedom; `C = 3694.15`; `τ² = 0.010905`.

**Result: pooled r = −0.0585, 95% CI −0.1630 to +0.0473, four studies, five effects, I² = 91.0.**

Pooled Fisher-z = −0.058538, SE = 0.054035.

This replaces the single-study value the chapter previously reported for this cell, von Rueden and
Jaeggi's Zr = 0.19, which is r = 0.188 on the correlation scale.

---

## 3. Sensitivity

Four alternatives to the headline specification, each varying one choice.

| Specification | k effects | k studies | Pooled r | 95% CI | I² | τ² |
|---|---:|---:|---:|---|---:|---:|
| Headline (§2) | 5 | 4 | −0.0585 | −0.163 to +0.047 | 91.0 | 0.0109 |
| Courtiol's two sexes combined into one row by fixed effect | 4 | 4 | −0.1196 | −0.323 to +0.094 | 93.2 | 0.0422 |
| Lebuda's wealth correlation only, schooling dropped | 5 | 4 | −0.0129 | −0.096 to +0.071 | 84.7 | 0.0060 |
| Lebuda's two correlations entered as separate rows | 6 | 4 | −0.1260 | −0.246 to −0.003 | 93.7 | 0.0193 |
| The three added studies only, von Rueden excluded | 4 | 3 | −0.1173 | −0.226 to −0.006 | 91.1 | 0.0095 |

Every specification returns a negative point estimate. Three of the five cross zero; two exclude it
on the negative side. None is positive, and none reproduces the positive baseline the hypothesis
predicts for populations without contraception.

---

## 4. Held out of the pool

**Sorokowski et al. (2013), Yali, Papua New Guinea.** Number of pigs owned against number of living
children: **male r = +0.42, female r = +0.27**. The values reach this project only through the
Hopcroft (2018b) review, which quotes them without a sample size, and the original paper is not in
the retrieved set. No n means no variance, and no variance means no weight. This is the largest
positive contraception-absent estimate anywhere in the corpus, so the pooled cell above is computed
without the estimate that points hardest against its result. Record: W2791607709.

**Secondary rows within the four pooled studies**, excluded to avoid double-counting a sample:
Lebuda's second wealth rating (r = −0.21, the same 133 people rated by a second judge, inter-rater
r = 0.88); Lebuda's path-model coefficients (β = −0.27 for schooling, β = +0.02 for wealth, both
adjusted rather than zero-order); Josephson's grandchildren outcome (r = −0.032) and her three
offspring-generation estimates (r = +0.143, +0.145, +0.152, all measuring a parent's status against a
child's fertility); Courtiol's married-only subsample (d = +0.0311 men, +0.0873 women), which selects
on ever marrying.

**Aggregate group ratios in the Hopcroft (2018b) review**, quoted from Bengtsson and Dribe (2014),
Vézina et al. (2014), and Maloney et al. (2014), which report group means rather than an
individual-level association and carry no computable variance.

---

## 5. The sex-by-availability crossings the chapter reports

Neither cell is produced by any project script. Both are computed here under the same method, from
`extraction/…-effects.csv` alone, and both are unchanged by the re-pool, because every estimate the
re-pool added is contraception-absent.

**Men, contraception present. Pooled r = 0.0710, 95% CI 0.0125 to 0.1291, four studies, I² = 97.45,
τ² = 0.0034.** `Q = 117.75`.

| Study | r | n | Fisher-z | Variance | Weight | Weight share |
|---|---:|---:|---:|---:|---:|---:|
| Hopcroft (2018a), US SIPP | +0.070 | 313,405 | +0.0701 | 0.00000319 | 294.86 | 26.4% |
| Hopcroft (2015), US NLSY79 | +0.08 | 2,880 | +0.0802 | 0.00034758 | 267.68 | 24.0% |
| Fieder et al. (2005), Vienna employees | +0.16 | 2,693 | +0.1614 | 0.00037175 | 265.96 | 23.8% |
| Kanazawa (2003), US GSS | −0.0195 | 12,084 | −0.0195 | 0.00008277 | 288.10 | 25.8% |

**Women, contraception present. Pooled r = −0.1275, 95% CI −0.2118 to −0.0414, three studies,
I² = 96.49, τ² = 0.0056.** `Q = 56.97`. This cell coincides with the pipeline's `sex = female`
grouping, because every female estimate in `effects.csv` comes from a contraception-present sample.

| Study | r | n | Fisher-z | Variance | Weight | Weight share |
|---|---:|---:|---:|---:|---:|---:|
| Hopcroft (2018a), US SIPP | −0.057 | 348,572 | −0.0571 | 0.00000287 | 177.98 | 34.9% |
| Hopcroft (2015), US NLSY79 | −0.15 | 2,880 | −0.1511 | 0.00034758 | 167.69 | 32.9% |
| Fieder et al. (2005), Vienna employees | −0.18 | 2,073 | −0.1820 | 0.00048309 | 163.96 | 32.2% |

---

## 6. What this file does not do

- The three added studies are **not** written into `extraction/…-effects.csv`, so
  `output/tables/…-meta-analysis-summary.csv` still reports the five-study run, and the overall pool,
  the `sex = male` pool, and the `sex = female` pool there were **not** re-run against them. Two of
  the three would move the `sex = male` and `sex = female` groupings if they were.
- `source/analysis/b1_forest_plot.py` was not re-run, so
  `output/figures/…-status-repro-forest.png` displays the five-study pool and is stale with respect
  to the contraception-absent cell.
- Risk of bias is not coded for Lebuda et al. (2021), Josephson (1993), or Courtiol et al. (2012).
- The Sorokowski et al. (2013) values remain unpooled for want of a sample size.
