# Comparing Effects from Incomparable Samples

**From:** Shravan Hari  
**Date:** September 19, 2026  
**Re:** Recovering one effect per cell from many selected-sample estimates, given the v3 frame

## 0. What this memo is for

The previous memo (2026-09-11, "The Numerator for a Comparable Share") took a single identified effect
$\hat\beta_D$ per hypothesis as given and asked how to combine hypotheses into comparable shares:

$$s_{p,\ell}(D) \;=\; \frac{\hat\beta_D \cdot \Delta\varepsilon_{D,p,\ell}}{\Delta\text{TFR}_{p,\ell}}.$$

That memo needs an input we do not have. We hold a **pile** of estimates $\{\hat\beta_D^{(i)}\}$, one
per paper, and the papers disagree: they run on different samples, estimate effects on different outcome
parameters, and report different $R^2$. Somebody selected each paper's sample, so on its own the pile
estimates no common quantity, and memo 1's score has no input until we say what the pile estimates.

This memo answers that. It gets from many selected-sample estimates to one effect per cell,
$\hat\beta_D(p,\ell)$, the input memo 1's procedure needs. It keeps memo 1's frame: the five axioms and
the cell $(p,\ell)$ = region-period × country of memo 1's §7. It treats only *sample* selection, meaning
which units a given study observed.

## 1. Recommendation

Model the per-cell effect as a grand mean plus period, country, and interaction components, one step
beyond a two-way fixed-effects decomposition:

$$\beta_D(p,\ell) \;=\; \bar\beta_D \;+\; \phi_p \;+\; \gamma_\ell \;+\; \delta_{p\ell},$$

with the usual margin normalizations. Each paper recovers the **composition-weighted average** of these
cell effects over the cells its sample covers, plus a mean-zero estimation error. A **random-effects**
meta-regression of the study estimates on their observed sample composition recovers the components, and
prediction at the target cell gives $\hat\beta_D(p,\ell)$, the number memo 1's score needs.

One assumption does much of the work. Call it **A-SEL**: sample selection is uncorrelated with the
causal effect once we condition on composition. A study's sample may draw heavily from particular
periods and countries, but, given that composition, which units it contains is uncorrelated with the
size of the effect. This is weaker than assuming selection ignorable outright. It is weaker along the
dimension we most fear, data availability that favours recent periods and rich countries, because that
selection runs through period and country, which the model absorbs.

**The reframing turns sample-selection bias into composition bias, and composition is observed.** We can
now measure how far two papers on one hypothesis disagree and say why. Their disagreement becomes a
measured object, the periods and countries each one sampled, which we can adjust for.

## 2. The decomposition

Index the effect by the cell $(p,\ell)$, period crossed with country, and split it two-way plus
interaction:

$$\beta_D(p,\ell) \;=\; \underbrace{\bar\beta_D}_{\text{grand mean}} \;+\; \underbrace{\phi_p}_{\text{period}} \;+\; \underbrace{\gamma_\ell}_{\text{country}} \;+\; \underbrace{\delta_{p\ell}}_{\text{interaction}}, \qquad \sum_p \phi_p = \sum_\ell \gamma_\ell = 0, \quad \sum_p \delta_{p\ell} = \sum_\ell \delta_{p\ell} = 0.$$

A two-way fixed-effects reading stops at $\bar\beta_D+\phi_p+\gamma_\ell$ and imposes separability. The
interaction $\delta_{p\ell}$ is the step beyond, and it is the term memo 1 most needs, because memo 1's
score is defined *per cell* and only $\delta_{p\ell}$ lets the effect differ across cells in a way the
two margins cannot.

The decomposition is an identity, not a restriction. Any function on a finite $p\times\ell$ grid takes
this form once $\delta_{p\ell}$ is saturated, so the form asserts nothing on its own. The restriction
enters in §5: **parsimony on $\delta$**, meaning sparsity, smoothness, or a sign bound, so that finitely
many studies can estimate the cell effect. Both the modeling content and the cost sit there. Keep the
identity and the restriction separate.

## 3. What a paper recovers, and where A-SEL lives

A paper does not sample a cell; it samples a *mix* of cells. Let $\omega_i(p,\ell) \ge 0$ be study $i$'s
share of sample in cell $(p,\ell)$, with $\sum_{p,\ell}\omega_i(p,\ell)=1$ and observable marginals
$\omega_i^P(p) = \sum_\ell \omega_i(p,\ell)$ and $\omega_i^L(\ell) = \sum_p \omega_i(p,\ell)$. Harmonized
onto the common outcome $Y$ (§6), study $i$ estimates the composition-weighted effect

$$\hat\beta_D^{(i)} \;=\; \bar\beta_D \;+\; \sum_p \omega_i^P(p)\,\phi_p \;+\; \sum_\ell \omega_i^L(\ell)\,\gamma_\ell \;+\; \sum_{p,\ell}\omega_i(p,\ell)\,\delta_{p\ell} \;+\; e_i, \qquad E[e_i]=0,\ \operatorname{Var}(e_i)=v_i.$$

The weights are sample shares, so a study's estimate is a **convex** combination of the cell effects it
covers: no weight is negative, and the study's own aggregation introduces no perverse weighting. The
$\hat\beta_D$ we get is a weakly causal parameter.

**Old A-SEL was monolithic; the decomposition splits it.** In the earlier framing, "selection
uncorrelated with the effect" had to hold against the entire effect draw, which meant assuming away the
selection we most fear, data availability that pulls samples toward recent periods and rich countries.
That is selection on period and country, on $\phi_p$ and $\gamma_\ell$. The decomposition lets us stop
assuming it and absorb it instead. Two readings:

- **Fixed-effects reading.** Treat $\phi,\gamma,\delta$ as parameters and regress the estimates
  $\hat\beta_D^{(i)}$ on their composition weights, a precision-weighted meta-regression. A-SEL then
  narrows to $e_i \perp \text{composition}$: whatever selection remains once we condition on which
  periods and countries a study sampled is uncorrelated with the effect.
- **Random-effects reading.** Let $\phi_p \sim (0,\sigma_P^2)$, $\gamma_\ell \sim (0,\sigma_L^2)$,
  $\delta_{p\ell} \sim (0,\sigma_{PL}^2)$, a crossed random-effects (mixed) meta-analysis. A-SEL becomes
  study composition uncorrelated with the random components, and we gain partial pooling and the
  variance decomposition of §4.

So selection may be correlated with period and country to any degree; A-SEL is needed only for the
residual, the cell-level interaction and idiosyncratic error the grid does not span. That is weaker than
the monolithic assumption, and weaker along the dimension that matters.

**The data point to a random-effects model.** With an average of ten studies per hypothesis spread over
a wide country grid, the fixed-effects reading leaves most country and interaction cells identified by
one study or none, so it returns nothing where we need a number. Random effects restore identification
by borrowing strength across cells through shared variance components, the price of having an estimate at
all. That price is three assumptions the fixed-effects reading does not need. We name each and where it
enters: the exchangeability and distributional assumption on the components (S6, §5); the stronger form
of A-SEL, composition uncorrelated with the *random* components rather than the residual alone (S4, §6);
and the shrinkage of each cell effect toward the grand mean (§7). None is innocuous; each buys an
estimate the fixed-effects model would not deliver.

## 4. What the framing buys

**It explains the $R^2$ symptom and confirms memo 1 §4.** Anup's complaint was that papers carry
different explanatory power because they run on different samples. In each sample
$R^2_i = \beta_D(S_i)^2\,\operatorname{Var}(X_D\mid S_i)/\operatorname{Var}(Y\mid S_i)$. The
decomposition recovers the $\beta$ factor, now a modeled function of composition. It does nothing for the
variance ratio, which reflects sample composition rather than bias. So $\beta$ is portable and $R^2$ is
not, which is why memo 1 built the score on $\beta$ and rejected $R^2$. This memo supplies the
statistical reason: the effect is a structural object with a period and country decomposition, and $R^2$
folds in two nuisance sample variances that no orthogonality assumption can remove.

**It breaks down where the effect lives.** In the random-effects reading, $\sigma_P^2$, $\sigma_L^2$ and
$\sigma_{PL}^2$ report how much of the effect's variation is period-driven, country-driven, or
cell-idiosyncratic. That maps onto the review's three target phenomena: a hypothesis whose variation is
mostly $\sigma_P^2$ is a common historical shift of the kind the First and Second Demographic
Transitions describe, while one dominated by $\sigma_L^2$ is a cross-country institutional story. The
decomposition turns "is this effect general?" into three estimable numbers.

## 5. Estimation and prediction at the target cell

Fit the model in one pass. With the study estimates $\hat\beta_D^{(i)}$, their squared standard errors
$v_i$, and their composition weights $\{\omega_i(p,\ell)\}$ as data, a mixed model returns
$\hat{\bar\beta}_D$, the components, and the variance components, with inverse-variance weighting on the
$v_i$ and shrinkage on sparse cells. The **target-cell effect is a prediction**:

$$\hat\beta_D(p,\ell) \;=\; \hat{\bar\beta}_D + \hat\phi_p + \hat\gamma_\ell + \hat\delta_{p\ell},$$

evaluated at the $(p,\ell)$ the review cares about rather than at the study population's average
composition.

**Prediction at the target cell defuses the representativeness worry.** The pooled mean answers a
question about the grid the studies populate, which may sit far from the target cells. Because we observe
composition and model the margins, we do not report the study-population average and hope. We
**reweight**: post-stratify to the target cell's composition and predict there. Where a target cell lies
outside the studies' composition support, the prediction is extrapolation, and §7 says what to do about
it.

Fit it as a **crossed random-effects mixed model**: $\phi_p$, $\gamma_\ell$ and $\delta_{p\ell}$ as
three independent zero-mean random effects with variances $\sigma_P^2$, $\sigma_L^2$, $\sigma_{PL}^2$,
inverse-variance weighting on the $v_i$, and REML for the variance components. The target-cell effect
above is then the **posterior mean** of the sum, a shrunken prediction. Cells with many studies sit near
their raw estimate; cells with few are pulled toward the relevant margin, and toward $\bar\beta_D$ when
studies are fewest. That shrinkage restores identification where §7's overlap fails, and it is the first
strong assumption we make. Fit the additive model first and test whether $\delta$ earns its degrees of
freedom before spending them.

**Where the strong assumptions enter, and why we need them.** Sparsity pushes us past what the data
alone identify. We mark the three places where assumption, not data, buys identification, so a reader can
locate each:

1. **A distribution on the components, and exchangeability** (S6). Treating countries as draws from a
   common $(0,\sigma_L^2)$ law lets a data-rich country inform a data-poor one. It holds when countries
   are exchangeable within the grid and fails when a cell is one of a kind. We flag any cell whose
   prediction is mostly shrinkage.
2. **A-SEL against the random components, not just the residual** (S4). Borrowing strength across
   countries assumes the country composition of studies is uncorrelated with $\gamma_\ell$ itself, a
   stronger statement than the fixed-effects residual condition. Where composition tracks the effect, as
   when data availability correlates with effect size, this assumption is at risk, and the residual
   meta-regression of S4 checks it.
3. **Shrinkage biases the individual cell effect** (§7), the quantity memo 1's score consumes. We take a
   biased but estimable cell effect over an unbiased one we cannot identify, and report the shrinkage
   weight per cell so a reader sees how much of $\hat\beta_D(p,\ell)$ is data and how much is model.

## 6. Assumptions on the data-generating process

| | Assumption | Check or bound |
|---|---|---|
| S1 | **Common outcome.** Every study's estimate maps onto the common $Y$ (births per woman) via the harmonization ladder, so the $\hat\beta_D^{(i)}$ are on one scale | `docs/meta-analysis-effect-size-harmonization.md`. Stated intentions do not convert and stay out |
| S2 | **Effect decomposition.** $\beta_D(p,\ell)=\bar\beta_D+\phi_p+\gamma_\ell+\delta_{p\ell}$. An identity when $\delta$ is saturated; the working restriction is **parsimony on $\delta$** | Test additive vs. interacted fit; where $\delta$ is unidentified, sign-bound it rather than drop it (§7) |
| S3 | **Convex aggregation.** $\hat\beta_D^{(i)}=\sum_{p,\ell}\omega_i(p,\ell)\beta_D(p,\ell)+e_i$ with non-negative shares $\omega_i$ summing to one and mean-zero $e_i$ | The weights $\omega_i$ are **not extracted today** and are rarely reported by papers. Exact only for single-cell studies; otherwise we construct them under S7 |
| S4 | **A-SEL (random-effects form).** Study composition uncorrelated with the random components $\{\phi_p,\gamma_\ell,\delta_{p\ell}\}$, not merely the residual, the stronger condition shrinkage requires (§5) | Meta-regress residuals on sample covariates outside $(p,\ell)$; a systematic relationship is evidence against S4 |
| S5 | **Overlap.** Studies vary in period-mix and country-mix with enough overlap to separate $\phi$ from $\gamma$ (and $\delta$ where claimed) | Inspect the composition design matrix for collinearity; under S6 a collinear region returns a number, but one that is mostly shrinkage (§7) |
| S6 | **Exchangeable components with a variance structure.** $\phi_p\sim(0,\sigma_P^2)$, $\gamma_\ell\sim(0,\sigma_L^2)$, $\delta_{p\ell}\sim(0,\sigma_{PL}^2)$, mutually independent, the random-effects assumption that restores identification under sparsity | Flag cells whose prediction is mostly shrinkage; $\sigma_P^2$ rests on few periods and is the weakest component (§7) |
| S7 | **Weight-construction rule.** Where $\omega_i$ is not a point mass, split a study's weight across the cells of its support: mass 1 on a single tagged state; **span-proportional** across period states (sample-window years in each state, using the region's milestone dates) where years are recorded; **uniform** across states where years are `NR`; degenerate on country for single-country studies, and uniform (later person-year or population) across countries otherwise | Run **uniform-vs-span as a sensitivity check**: if the fitted components barely move, report the simpler rule and note the check; if they move, that is a finding. Span reduces a straddler bias, so it is the default where years exist |

The memo inherits S1 and memo 1's local-linearity and comparable-measurement assumptions (M1, M5)
unchanged; the sample-selection layer adds the seven above. S4 is the assumption Anup's framing is built
around. S2's parsimony on $\delta$ trades identifiability against how cell-specific the answer
can be. The random-effects choice adds S4 and S6, and our data force S7: we do not observe the weights S3
wants, so we construct them. Each is the price of an estimate where the data are too thin to identify
one.

## 7. Costs of the proposal

**Overlap and collinearity bind first.** Separating $\phi$ from $\gamma$ needs studies that differ in
period composition while overlapping in country composition, and the reverse. If pre-transition studies
cluster on one set of countries and Second-Transition studies on another, the two margins are collinear.
This is S5. Under the random-effects fit it no longer leaves the margins unidentified: the variance
components and shrinkage return a number. But that number leans on S6's exchangeability where the data
cannot separate the margins, so read a collinear region as model output rather than measurement.

**Shrinkage biases the cell effect, and the period variance rests on few levels.** The posterior cell
effect is pulled toward the grand mean by an amount that grows as a cell's studies thin out, so
$\hat\beta_D(p,\ell)$, memo 1's input, is biased toward the hypothesis-wide average in the cells we know
least about. We accept this to have any estimate, and report the per-cell shrinkage weight so the bias
stays visible. Separately, v3 defines only a few period states, so $\sigma_P^2$ rests on a handful of
levels and is the least trustworthy variance component. Where it matters, fix it to a defensible value or
place an informative prior rather than read a variance off three numbers.

**The interaction is the data-hungriest term and the one we most want.** With a handful of studies per
hypothesis, $\delta_{p\ell}$ is close to unidentified, so the estimable part is often the additive
$\bar\beta_D+\phi_p+\gamma_\ell$, which is separable across the grid and cannot express a cell-specific
effect. The fallback is the one memo 1 §6 took for the edge coefficients: report a sign-bounded interval
for $\delta$ rather than a point, and let the score be an interval. A tension remains: the estimable part
is not fully cell-specific, and the cell-specific part is hard to estimate. State it plainly.

**Extrapolation past the support.** Predicting $\hat\beta_D(p,\ell)$ at a target cell outside the
studies' composition support (§5) leans on the functional form S2 rather than on data. Flag such cells
and widen their intervals; do not report a point where the support is empty.
