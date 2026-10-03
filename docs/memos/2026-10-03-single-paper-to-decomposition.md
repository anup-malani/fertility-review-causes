# From the Single Paper Up: A Per-Cell Decomposition of the Decline

**From:** Shravan Hari  
**Date:** October 3, 2026  
**Re:** Building up the necessary quantities & assumptions to decompose fertility decline

## 0. Setup and what this memo is for

This memo starts at the
paper-level and rebuilds the logic developed in the two older memos from there, because the inputs those memos assume present challenges: they are the output
of an extraction we have not fully specified, and the whole construction depends on what
we can and cannot pull out of a single study.

**The setup.** We have a set of papers, indexed $i$. Each paper studies a treatment $D$, an outcome
$Y$, and a vector of study-level covariates $X$, and reports an estimate of the effect of $D$ on $Y$
conditional on $X$. Each paper is attached to a location $\ell$ and a period $p$ drawn from finite
sets $L$ and $P$. For now, hold $D$, $X$, and $Y$ fixed across papers, and we'll start to relax these assumptions. Write a cell as
$(p,\ell)\in P\times L$.

For each cell $(p,\ell)$ we want two numbers per hypothesis $D$:

1. the **causal effect** of $D$ on $Y$ in that cell — a per-unit rate, $\beta_D(p,\ell)$; and
2. the **significance** of $D$ in that cell — how much of the actual change in $Y$ that cell saw is
   attributable to $D$,

and we want both to **decompose** the realized change: the significances of the different hypotheses
should sum to the total change in $Y$ in the cell, so that the review can say "this much of the
decline here was $D_1$, this much was $D_2$," and have the pieces add up.

This first part treats the atom of the construction: **a single paper.** What must come out of it
before its estimate can serve either target?

## 1. What one paper gives us versus what we need

Let $\Delta Y(p,\ell)$ be the realized change in the outcome in the cell — the quantity we wish to decompose. Read the outcome through a locally-linear structural model in the exposures, so that the
change decomposes as a sum of per-hypothesis contributions:

$$\Delta Y(p,\ell) \;=\; \sum_D \underbrace{\beta_D(p,\ell)\,\Delta D(p,\ell)}_{\text{contribution } c_D(p,\ell)} \;+\; \text{residual}(p,\ell).$$

Each contribution is a product of two factors of entirely different character:

- $\beta_D(p,\ell)$, the **causal rate** — what a one-unit movement in the exposure does to $Y$,
  holding the cell fixed. This is target 1. It is intensive: it says nothing about how far the
  exposure actually moved.
- $\Delta D(p,\ell)$, the **movement of the exposure** in the cell — how far $D$ actually travelled
  over the period in that location. It is a fact about the world's history, not about any study.

Their product $c_D(p,\ell)=\beta_D(p,\ell)\,\Delta D(p,\ell)$ is target 2, the "significance". It is
extensive, carried in the units of $\Delta Y$, and it is the thing that sums. The causal effect and
the significance are therefore not two readings of one number: the first is a more theoretical rate, the second scales that rate
against the size of treatment change. A large causal effect with a treatment that barely varied is
demographically trivial, and a small effect on an exposure that varied a lot may explain most of the decline.

**One single paper measures the rate, not the movement.** A study estimates $\beta_D$ on a sample it
selected, under an identification strategy, in whatever units it chose, with sampling error. It does
**not** measure $\Delta D(p,\ell)$ or $\Delta Y(p,\ell)$: those are properties of the cell, not of the
study's design, and a study that happens to report its own sample's change in $D$ reports the change
in *its sample*, which is not the cell's historical movement. This is the organizing split of the
whole extraction:

> From the **paper** we take $\beta_D(p,\ell)$ — and everything needed to make that number a clean,
> total-effect, common-unit causal rate with a known uncertainty. From the **macro panel**
> (`data/raw/`, still unbuilt) we take $\Delta D(p,\ell)$ and $\Delta Y(p,\ell)$. Significance is never obtainable from the literature alone — one of those two factors lives outside
> every paper we will ever read.

So "what to extract from one paper" is exactly the list of things that pin down $\beta_D(p,\ell)$ as a
quantity admissible into the decomposition, plus the sample moments needed to recover it when the paper
reports it in a transformed form and to bound its use at the cell's realized movement. The next two
subsections give that list.

### 1.1 What pins down the causal rate

| | Extract | Why it is needed | Recorded today? |
|---|---|---|---|
| **E1** | **The cell** $(p,\ell)$ the estimate pertains to | Every downstream quantity is indexed by the cell; an estimate with no cell cannot enter the grid. (A sample spanning several cells is the subject of the 2026-09-19 memo; here one paper, one cell.) | Partly — period/location are screened but not stored as a clean $(p,\ell)$ key |
| **E2** | **The point estimate** $\hat\beta_i$ — the reported effect of $D$ on $Y$ | It is the measurement of the rate. | Yes |
| **E3** | **The functional form** of the specification — level–level, log–level, log–log, semi-elasticity, hazard or odds ratio, probit/logit index, standardized ("beta") coefficient | Determines the map from $\hat\beta_i$ to a common $dY/dD$, and whether that map needs auxiliary moments (an elasticity needs sample means; a standardized coefficient needs E8's standard deviations). Two papers reporting "$\,0.3\,$" under different forms are not reporting the same rate. | No — captured informally in notes, not as a field |
| **E4** | **The native units of $D$ and of $Y$** | To place $\hat\beta_i$ on the common outcome scale (births per woman) and a common exposure scaling via `docs/meta-analysis-effect-size-harmonization.md`. Additivity in §0 requires every term in one unit. | Partly — harmonization ladder exists; per-estimate source units not always stored |
| **E5** | **The covariate set $X$, each covariate classified by its causal role relative to $D\to Y$**: confounder (back-door, needed for identification), mediator (on a path $D\to X\to Y$), collider, or neutral/precision-only | This decides **which estimand** $\hat\beta_i$ is, and therefore whether it is the *total* effect the decomposition requires. Condition on a mediator and $\hat\beta_i$ is a direct effect, strictly smaller than the total, and the contributions will under-sum; condition on a collider and $\hat\beta_i$ is biased and the estimand is not causal at all. This is the single most consequential item and the one we do not record. | **No** — flagged in the 2026-09-11 memo (M4) as "not recorded today, for any chapter" |
| **E6** | **The identification strategy / design** — RCT, IV, DiD, RD, panel FE, matched, cross-sectional OLS — and the estimand it targets (ATE, ATT, LATE) | Decides whether $\hat\beta_i$ is a causal rate at all versus a conditional correlation (this is what §4.1 GRADE already grades), and whether the estimand is the cell-average total effect the decomposition wants or a sub-population effect (a compliers' LATE) that needs a transport argument before it can stand in for $\beta_D(p,\ell)$. | Partly — design captured for GRADE; estimand type not stored as a field |
| **E7** | **The uncertainty** — $\widehat{\operatorname{se}}(\hat\beta_i)$, or a CI, or a $t$/$p$ with enough to back out the standard error | Becomes the $v_i$ that weights papers when several share a cell (2026-09-19 memo) and propagates into the interval on the significance (2026-09-11 memo §7). A rate with no uncertainty cannot be pooled or bounded. | Yes |

### 1.2 What significance additionally needs, and why most of it is not in the paper

Target 2 is $c_D(p,\ell)=\beta_D(p,\ell)\,\Delta D(p,\ell)$. Given the rate from §1.1, the significance
needs the exposure's movement and the total decline — and those are macro, not from the paper:

- **$\Delta D(p,\ell)$** — the cell's realized movement of the exposure. From the macro panel.
- **$\Delta Y(p,\ell)$** — the cell's realized change in the outcome, the denominator of the share and
  the target of the decomposition. From HFD/WPP on the milestone definition.

What the *paper* can still add here is a set of sample moments, worth extracting for three distinct
jobs even though none of them is the significance itself:

| | Extract | Why it is needed | Recorded today? |
|---|---|---|---|
| **E8** | **Sample standard deviations** $\operatorname{sd}(D\mid S_i)$ and $\operatorname{sd}(Y\mid S_i)$ (or variances) | (a) Recover $\hat\beta_i$ when the paper reports only a standardized coefficient or an $R^2$ (via $r=\hat\beta\,\operatorname{sd}(D)/\operatorname{sd}(Y)$), completing E3's conversion. (b) Strip the variance ratio that makes $R^2$ and $r$ non-portable: the 2026-09-11 memo §4 and 2026-09-19 memo §4 showed a paper's in-sample explanatory power folds in $\operatorname{Var}(D\mid S_i)/\operatorname{Var}(Y\mid S_i)$, which is a feature of the sample, not of the mechanism. Extracting the two variances is what lets us *remove* them rather than mistake them for significance. | No |
| **E9** | **The sample's realized range or change of $D$** — $\Delta D_i$ or $[\min,\max]$ of $D$ in-sample | Checks local linearity (the 2026-09-11 memo's M1): a linear rate estimated over a narrow in-sample range is an extrapolation when applied to a large historical $\Delta D(p,\ell)$. Where a dose–response is reported, it bounds the rate at the cell's movement rather than assuming the slope is constant out to it. | No |

E8 and E9 are the bridge between the paper's own frame and the cell's. They are also the inputs that
let us *report* the $R^2$ route as a diagnostic beside the significance without letting it certify
anything — which is the disposition the 2026-09-11 memo argued route 3 should have.

## 2. Two papers in one cell

Now take two papers, $i=1,2$, both attached to the same cell $(p,\ell)$, each having yielded a clean
rate from §1: a pair $(\hat\beta_1, v_1)$ and $(\hat\beta_2, v_2)$, where $v_i=\operatorname{se}(\hat\beta_i)^2$,
already on the common scale and already screened for estimand (E5, E6). We want one number for the cell,
$\hat\beta(p,\ell)$. The word "pool" makes this sound like averaging; the first-principles content is
in deciding *what two estimates are estimates of*, because the arithmetic of combination is only
licensed once that is settled.

**A caveat that governs the whole section.** What each paper identifies — under its design — is a
marginal feature of the response: a contrast between the $D=1$ and $D=0$ outcome distributions, or, for
continuous $D$, a slope of $Y$ in $D$ over the dose range its sample spans. We never observe the joint
distribution of outcomes across treatment values, and for a continuous treatment we never observe the
dose–response surface — only slices of it, one per study, at each study's own location on that surface.
Pooling presumes those slices are measuring one object. Whether they are is the question; the formula is
downstream of the answer.

### 2.1 The case where pooling means what it sounds like

Suppose the two papers estimate the **same** cell rate and differ only by sampling noise:

$$\hat\beta_i = \beta(p,\ell) + e_i, \qquad E[e_i]=0, \quad \operatorname{Var}(e_i)=v_i, \quad e_1\perp e_2.$$

This is the common-effect (fixed-effect) model. Combining two unbiased measurements of one quantity
with known variances has a single best linear unbiased answer — the **inverse-variance weighted mean**:

$$\hat\beta(p,\ell) \;=\; \frac{w_1\hat\beta_1 + w_2\hat\beta_2}{w_1 + w_2}, \qquad w_i = \frac{1}{v_i}, \qquad \operatorname{Var}\!\big(\hat\beta(p,\ell)\big) = \frac{1}{w_1+w_2}.$$

Everything that follows is about when this model is false, which — with two studies drawn from two
samples — is the default, not the exception.

### 2.2 Two samples in one cell need not share an estimand

A cell is a region-period, not a homogeneous population. Two papers inside it can be estimating
genuinely different numbers for reasons that have nothing to do with sampling error:

- **Within-cell effect heterogeneity.** If the per-unit effect varies across individuals,
  sub-regions, or sub-periods within the cell, each paper recovers a *composition-weighted average* of
  those unit-level effects over its own sample, $\hat\beta_i \approx \int \beta(u)\,d\omega_i(u)$. This
  is the 2026-09-19 memo's structure operating *inside* a cell rather than across cells: two samples,
  two compositions $\omega_i$, two different weighted averages of the same underlying effects.
- **Continuous treatments.** When $D$ is continuous and the response is curved, each
  paper's slope is an average derivative over the dose interval its sample spans (E9). Two papers
  positioned on different parts of the curve report different slopes with *no* inconsistency and *no*
  bias — they are correct answers to different questions. This is the joint-distribution caveat made
  concrete: the "pooled slope" is a chord across the union of two ranges, and its value depends on the
  distribution over dose, which is exactly the object we do not observe.
- **Estimand type.** An ATT, a compliers' LATE, an RD-style local effect, and an ATE are different weightings of the same
  unit-level effects. Two papers reporting different estimand types are not two noisy reads of one
  number even before heterogeneity enters.

In every one of these, $E[\hat\beta_1]\ne E[\hat\beta_2]$, the common-effect model of §2.1 is false,
and inverse-variance weighting answers a question we did not ask. It returns the average effect over a
composition that is *neither* sample's and *not* the cell's target composition — it is the blend that
the two samples' precisions happen to induce. **Precision weights are not representativeness weights.**
A large, tightly-estimated study of an unrepresentative subpopulation dominates the pool and drags
$\hat\beta(p,\ell)$ toward its own composition, which is the opposite of what the decomposition wants:
the decomposition needs $\beta$ at the cell's *demographic* composition, so that $\beta\,\Delta D$ is
the cell's actual contribution. The principled repair is the 2026-09-19 memo's — post-stratify each
estimate to the cell's target composition before combining — and it needs the composition weights
$\omega_i$, which §1 flagged (E1 extended) we do not store.

### 2.3 Heterogeneity is not identified from two numbers

The model when §2.2 holds needs a between-study component,

$$\hat\beta_i = \beta(p,\ell) + u_i + e_i, \qquad u_i \sim (0,\tau^2),$$

and reweights by $w_i = 1/(v_i+\tau^2)$. The difficulty is that **$\tau^2$ cannot be estimated from
two studies.** All the information about disagreement is in the single contrast $\hat\beta_1-\hat\beta_2$,
whose expected square is

$$E\big[(\hat\beta_1-\hat\beta_2)^2\big] = (\beta_1-\beta_2)^2 + v_1 + v_2.$$

From this, we cannot separate the systematic gap $(\beta_1-\beta_2)^2$ from the sampling issues
$v_1+v_2$. So with $n=2$ we can *detect gross disagreement* —
if $|\hat\beta_1-\hat\beta_2|$ dwarfs $\sqrt{v_1+v_2}$, something real differs — but we cannot measure that, and therefore cannot set the weights the random-effects model needs or widen the
interval by the right amount. Reporting the §2.1 inverse-variance CI when heterogeneity is in fact
present would require us to make a strong assumption about homogeneity of treatment effects.

### 2.4 Before averaging, screen for bias — do not average across identification quality

Note: we won't worry about this issue for now. We'll deal with correcting it later, but it's worth saying.  
Inverse-variance weighting assumes **both** estimates are unbiased for the target. If one is not —
$E[\hat\beta_i]=\beta+b_i$ — the pool inherits $\sum w_i b_i / \sum w_i$, and the damage is worse than a
simple average would do, because the biased estimate is often the *more precise* one: an observational
study with a large $N$ carries a small $v_i$, hence a large $w_i$, and so dominates a small, clean
quasi-experiment. Precision-weighting a confounded OLS against an RCT moves the pool toward the
confounded number and reports a tight interval around it. This is the A.12 situation and the standing
ruling it produced — *resolve disagreements, do not average* (TICK-080 item 9;
`decisions/2026-07-11-oas-conservative-pooling-rule.md`).

### 2.5 What to do with exactly two papers

The arithmetic is cheap; the licensing is the work. Concretely:

1. **Gate (§2.4).** If the two estimate different estimands or differ in identification quality, do not
   pool — select the better-identified and report the other alongside. This is also why the project's
   working rule requires $\ge 3$ studies *after stratification* before a pool is formed: two studies are
   below the line at which a pool is the default object.
2. **If they pass the gate, inverse-variance combine (§2.1)** — but report the result as *conditional on
   a common effect*, an assumption two studies cannot test (§2.3).
3. **Carry the disagreement as a number**, $\hat\beta_1-\hat\beta_2$ against $\sqrt{v_1+v_2}$. A gap far
   outside the sampling floor is a finding about within-cell heterogeneity, not a blemish to be smoothed
   into a mean.
4. **Prefer borrowed heterogeneity to assumed homogeneity.** Because $\tau^2$ is unidentified at
   $n=2$ but the decomposition still needs an honest interval, the right home for the heterogeneity is
   the cross-cell hierarchy: estimate $\tau^2$ (and the composition structure) from *all* cells at once
   and lend it to this one, so the two-study cell is shrunk and its interval widened by a $\tau^2$ the
   data elsewhere can support. That is partial pooling, and it is the subject of the next part — which is
   where two-in-a-cell stops being a special case and becomes one draw in the 2026-09-19 memo's crossed
   random-effects model.

## 3. N papers across the grid

Now take $N$ papers with the same $D$, $X$, $Y$, each tagged to a cell $(p_i,\ell_i)$ but spread across
$P\times L$, and ask for an estimate $\hat\beta(p,\ell)$ at **every** cell of the grid — including the
many that hold one paper or none. Three simplifications are granted for this part and it is worth saying
what each buys: **no biased estimates** turns off the §2.4 selection gate; **no publication bias** means
the observed estimates are a fair sample of the ones run; and **a common estimand up to scaling** means
every paper, once rescaled, is unbiased for the true effect of *its own cell*, $\hat\beta_i=\beta(p_i,\ell_i)+e_i$.
Together they collapse §2.2's within-cell heterogeneity: two papers in one cell now disagree only by
sampling error, so §2.1's inverse-variance pooling is exactly right *within* any occupied cell. What is
left — and it is the whole problem now — is that the cells are not occupied. With an average of around ten
papers per hypothesis and a grid of dozens of cells, most cells have zero or one paper, and §2.1 says
nothing about a cell it has no paper in.

### 3.1 Two "bad" answers

Two extremes are available without any new idea, and both fail the per-cell requirement:

- **Pool within each occupied cell, leave the rest blank.** This is §2.1 run cell by cell. It discards
  every cross-cell relationship — a paper in France tells us nothing about Italy, a 1960s study nothing
  about the 1970s — and returns no number precisely where coverage is thin, which is most of the grid.
- **Pool everything into one global mean.** This uses all $N$ papers but throws away all $(p,\ell)$
  variation, reporting one effect for every cell and so answering a different question than the review
  asks.

The right estimator lives between them: use every paper to inform every cell, but let the cells differ.
That is only possible if the cells are *linked by a structure*, so that a paper in one cell carries
information about its neighbours. Supplying that structure is the content of the generalization.

### 3.2 The structure that links cells

Impose the 2026-09-19 memo's decomposition on the cell effect:

$$\beta(p,\ell) \;=\; \bar\beta \;+\; \phi_p \;+\; \gamma_\ell \;+\; \delta_{p\ell}, \qquad \textstyle\sum_p\phi_p=\sum_\ell\gamma_\ell=0,\ \sum_p\delta_{p\ell}=\sum_\ell\delta_{p\ell}=0,$$

with each paper an observation on its own cell, $\hat\beta_i=\beta(p_i,\ell_i)+e_i$, $\operatorname{Var}(e_i)=v_i$.
The decomposition is what makes a paper in $(p,\ell')$ informative about $(p,\ell)$: they **share
$\phi_p$**. The period main effect is estimated from every paper in that period, wherever located; the
location main effect from every paper in that location, whenever run; and a cell's own idiosyncrasy
$\delta_{p\ell}$ is all that remains cell-specific. The identity is saturated — any array on the grid
can be written this way — so it asserts nothing until we restrict $\delta$. The restriction is where
borrowing happens, and it is the whole ballgame.

### 3.3 Why the fixed-effects reading is not enough

Treat $\phi,\gamma,\delta$ as free parameters and the model is a precision-weighted (GLS) regression of
the $\hat\beta_i$ on period and location dummies with their interactions. It separates the two margins
only where the design is **connected** — papers that vary period while sharing a location, and vice
versa, so that $\phi$ can be told apart from $\gamma$ (the 2026-09-19 memo's overlap condition S5). And
a free $\delta_{p\ell}$ needs at least one paper in cell $(p,\ell)$: with the interaction saturated, an
empty cell's $\delta$ is unidentified and the fitted value does not exist. So the fixed-effects reading
returns the within-cell pool where there is data, the margins where the grid is connected, and
**nothing at all for an empty cell** — it is §2.5's "below the line" problem written across the whole
grid rather than one cell. It does not produce an estimate everywhere, which is what we asked for.

### 3.4 The random-effects reading produces an estimate everywhere

Let the components be exchangeable draws,

$$\phi_p\sim(0,\sigma_P^2),\quad \gamma_\ell\sim(0,\sigma_L^2),\quad \delta_{p\ell}\sim(0,\sigma_{PL}^2),$$

fit the mixed model by REML, and read the cell effect off as the prediction

$$\hat\beta(p,\ell) \;=\; \hat{\bar\beta} + \hat\phi_p + \hat\gamma_\ell + \hat\delta_{p\ell},$$

the posterior mean (BLUP), evaluated at every cell. The mechanism is shrinkage. Writing the margin
prediction as $m_{p\ell}=\hat{\bar\beta}+\hat\phi_p+\hat\gamma_\ell$ and the cell's own precision-weighted
mean as $\bar y_{p\ell}$ with variance $V_{p\ell}=1/\sum_{i\in(p,\ell)}w_i$, the interaction behaves as

$$\hat\beta(p,\ell) \;\approx\; \lambda_{p\ell}\,\bar y_{p\ell} + (1-\lambda_{p\ell})\,m_{p\ell}, \qquad \lambda_{p\ell}=\frac{\sigma_{PL}^2}{\sigma_{PL}^2+V_{p\ell}}.$$

A data-rich cell ($V_{p\ell}$ small, $\lambda\to1$) sits near its own §2.1 pool; a thin cell is pulled
toward its margin; an **empty** cell ($V_{p\ell}=\infty$, $\lambda=0$) falls back exactly to the margin
prediction $m_{p\ell}$, and a cell with no papers in its row or column falls all the way to $\hat{\bar\beta}$.
Every cell of $P\times L$ now has a number. That is the generalization.

### 3.5 Does this fix §2.3 and §2.5?

Directly, and with the accounting kept honest:

**§2.5 — yes, mechanically, and the hard threshold dissolves.** Every cell gets an estimate, including
the two-paper and zero-paper cells that §2 could not serve. The project's $\ge 3$-after-stratification
rule was a frequentist guard against pooling too little; partial pooling replaces that hard cutoff with
**continuous shrinkage** — a cell contributes in proportion to its information rather than being in or
out. The cost is visible in the formula: a thin cell's estimate is mostly $m_{p\ell}$, i.e. *prediction
from the margins*, model and not measurement. The right disclosure is the 2026-09-19 memo's — report
$\lambda_{p\ell}$ per cell, so a reader sees how much of $\hat\beta(p,\ell)$ is that cell's own data.

**§2.3 — maybe, but the heterogeneity that becomes identified is a different object than the one that was
not.** §2.3's obstruction was that the between-study variance could not be estimated from the single
disagreement two papers provide. Across the grid, the disagreements from *all* cells are pooled, so the
variance components $\sigma_P^2,\sigma_L^2,\sigma_{PL}^2$ (and the residual) are estimated with the full
$N$ papers' worth of degrees of freedom, not one. The weights $1/(v_i+\text{component variance})$ and
the widened intervals that §2.3 could not set are now available. Two qualifications keep this from being
something for nothing:

1. **It is the cross-cell variance, under exchangeability.** What the grid identifies is how cell
   effects vary *across* the grid ($\sigma_{PL}^2$ and the margins), estimable only because we assumed
   the $\delta_{p\ell}$ are exchangeable draws from one law (S6). The within-cell disagreement of §2.3
   was set to pure noise by this part's common-estimand assumption; relax that and a study-level
   residual reappears, again estimable only by pooling it across cells under the same exchangeability.
2. **It needs overlap.** The margins separate, and so inform empty cells, only if the design is
   connected (S5). Where period and location are confounded in the sample — all early studies in one set
   of countries, all late ones in another — the model still returns a number, but it leans on
   exchangeability rather than on a real separation of the two margins, and should be read as such.

So the generalization does not *eliminate* the identification gap of §2.3; it **relocates** it. The gap
that two papers in one cell could not close is moved to a level — the whole grid — where there are
enough papers to estimate a variance, and the move is paid for with two assumptions (exchangeability and
overlap) that the single-cell problem never had to make. That is the honest statement of what borrowing
strength buys: not information from nowhere, but information from the other cells, licensed by the claim
that the cells are alike enough to lend to one another.

### 3.6 What is still owed

Three things are deferred, none of them undone by this part:

- **Papers that span several cells.** Here each paper sat in one cell; a paper whose sample mixes
  periods or countries contributes a composition-weighted average across cells, which is the
  2026-09-19 memo's full setup (its weights $\omega_i$ and the weight-construction rule S7). The mixed
  model above is the single-cell special case of it.
- **Empty-cell extrapolation.** A cell outside the studies' support is pure margin prediction; flag it
  and widen its interval rather than report a point (2026-09-19 memo §7).
- **The significance step is untouched.** This part delivers the *rate* $\hat\beta(p,\ell)$ at every
  cell. The significance $c_D(p,\ell)=\hat\beta(p,\ell)\,\Delta D(p,\ell)$ still needs the cell's
  exposure movement and the total decline from the macro panel, per §1.2 — the literature cannot supply
  them however many papers it holds.

## 4. Relaxing "same $X$": covariate sets that differ across studies

Now let each paper condition on its own covariate set $X_i$. **Conditioning on a different set generally changes the estimand**, so two papers with different
$X_i$ can be unbiased estimates of genuinely different causal quantities, and no multiplicative scaling
maps one to the other. This is the first assumption we relax that breaks "commensurable up to scaling".

### 4.1 The estimand is indexed by the conditioning set

Read the world through a linear structural model, as in the 2026-09-11 memo. What the coefficient on $D$
converges to depends on what $X_i$ contains, and each kind of covariate acts differently:

- **Confounder** (common cause of $D$ and $Y$). Including it closes a back-door path and is required for
  identification; omitting it leaves omitted-variable bias.
- **Mediator** (on a path $D\to M\to Y$). Including it *removes* the indirect path it carries, moving the
  estimand from the **total** effect to a **direct** effect:
  $$\operatorname{plim}\hat\beta_i \;=\; \beta^{\text{total}} \;-\; \sum_{m\in X_i\cap\mathcal M}\theta_m\pi_m,$$
  with $\pi_m$ the effect of $D$ on $M$ and $\theta_m$ the effect of $M$ on $Y$. Both the total and the
  direct effect are well-defined and well-identified — they are simply different questions.
- **Collider** (common effect). Including it opens a spurious path and induces bias.
- **Neutral / pure outcome predictor** (predicts $Y$, unrelated to $D$'s assignment). Including it leaves
  the estimand unchanged and only sharpens precision. This is the *only* covariate whose presence or
  absence is innocuous for what $\hat\beta_i$ means.
- **Pure treatment predictor** (predicts $D$ only). Including it leaves the estimand unchanged in the
  ideal case but costs variation in $D$, raising $v_i$.

### 4.2 Under "no bias," varying $X$ reduces to the total-vs-direct split

We are still carrying part 3's "no biased estimates." That assumption does real work here: it rules out
omitted confounders and included colliders, because both produce bias. The only ways $X$ can vary while
every estimate stays unbiased *for some estimand* are therefore two:

1. **Different valid adjustment sets.** If every $X_i$ is a sufficient back-door set for the total effect
   (confounders, with any mix of neutral covariates), then every paper identifies the **same** total
   effect, even though the sets differ — different sufficient adjustment sets give the same causal
   quantity. Here varying $X$ touches only $v_i$, part 3 goes through unchanged, and this is the case
   "commensurable up to scaling" was quietly assuming. Relaxing "same $X$" is *benign* precisely in this
   region, and now we can say why rather than assume it.
2. **Some sets include mediators.** Then those papers identify a direct effect, a different but unbiased
   estimand, offset from the total by the additive path term in §4.1.

So, holding "no bias," relaxing "same $X$" isolates exactly one real problem: **total versus direct
effect**, which is the 2026-09-11 memo's identity (I) versus (II) appearing at the extraction level.

### 4.3 Scaling cannot bridge total and direct

The total and direct effects differ by $\sum_m\theta_m\pi_m$, an *additive* quantity in the units of the
effect, not a ratio. No per-study scalar converts one into the other, because the gap depends on the
path coefficients, which vary by mediator and by cell and can even flip sign. Recovering the total effect
from a mediator-adjusted estimate requires **adding the indirect paths back**, and those path
coefficients are exactly the cross-edge quantities $\alpha_{jk}$ the 2026-09-11 memo §6 flagged as "not
identified anywhere in our evidence base." This is why §4 is categorically unlike parts 2–3: the earlier
incommensurabilities were differences in units, population, or precision, all reachable by scaling or
reweighting; this one is a difference in the causal quantity itself.

### 4.4 What to do

1. **Fix the target estimand: the total effect.** The decomposition (§1) attributes shares of the
   realized decline, and a mediated path is part of the decline $D$ produces; the direct effect would
   under-count it. So the grid we want is the total-effect grid.
2. **Partition by estimand, then run part 3 within each class.** Keep the papers whose $X_i$ is a valid
   total-effect adjustment set (no mediators) as the total-effect sample, and pool them by §3 — their
   $X$-differences are now known to be benign (§4.2, case 1). Papers that condition on mediators form a
   separate direct-effect sample. This is part 2's "resolve, do not average" generalized: the gate is now
   the *estimand set by $X$*, not identification quality, and it requires E5 on every paper to run.
3. **Model the shift and recover the total effect by meta-regression.** Rather than discard the
   mediator-adjusted papers, carry the control-set composition as a moderator:
   $$\hat\beta_i \;=\; \beta^{\text{total}}(p_i,\ell_i) \;-\; \sum_m \mathbb 1[m\in X_i]\,\psi_m \;+\; e_i,$$
   where $\psi_m=\theta_m\pi_m$ is the indirect path through mediator $m$. Fit this alongside the
   $(p,\ell)$ structure of §3; the prediction at "no mediators controlled" is the total effect, and the
   fitted $\hat\psi_m$ is an estimate of the indirect path. The bonus is real: **the cross-study
   variation in what people control for partially identifies the mediation paths** — the 2026-09-11
   memo's DAG edges — from the meta-sample itself, without a study that contains both legs. The price is
   also real: each moderator spends degrees of freedom against a thin sample, $\psi_m$ must be assumed
   roughly constant across cells (or modeled, at more df), the control-set indicators must not be
   collinear with the $(p,\ell)$ design (the overlap problem of §3.3 in a new dimension), and the whole
   thing rests on a correct E5 classification.

### 4.5 The catch in the classification, and what survives

Operation 3 — and the partition in operation 2 — presume we can label each covariate confounder,
mediator, or collider. For this literature that label is **not intrinsic to the variable**: female labour
supply, income, and education are each plausibly a cause, a consequence, and a correlate of fertility,
and which role a given covariate plays depends on the assumed graph and sometimes on the cell. A variable
that is a confounder in one cell is a mediator in another. This is the same simultaneity the 2026-09-11
memo §6 handled by merging cycles into one block, and it bounds how fine the classification can honestly
be: where $D$ and a covariate are mutually causal, "total effect of $D$ controlling for that covariate"
is not well-posed, and the pair should be treated as one block rather than split by conditioning.

What survives relaxing "same $X$": within a single estimand class — papers that all adjust for a valid
total-effect set — part 3 holds verbatim, and the $X$-variation is pure precision. Across classes,
scaling fails and we either partition (operation 2) or model the shift (operation 3), both of which
require E5 and neither of which is free. The clean summary is that **"same $X$" was never really about
the covariates; it was about holding the estimand fixed.** Varying $X$ is harmless exactly to the extent
that it leaves the estimand alone, and harmful — in a way no rescaling repairs — exactly when it does
not.

## 5. Next steps

Parts 1–4 show how to combine **valid, representative** estimates of **commensurable** quantities into a
per-cell rate. Three assumptions still stand between that and the real evidence base, and they come off in
a definite order: relaxing **different $Y$** finishes the commensurability question ($D$ was held fixed,
$X$ is done, $Y$ remains); relaxing **bias** breaks the validity each estimate was granted; relaxing
**publication bias** breaks the representativeness of the set we observe. Each is a part in its own right.

### 5.1 Different $Y$

Let papers measure different outcomes. Two sub-cases, mirroring §4's split into benign and
not-scalable:

- **Commensurable up to scaling.** TFR, age-specific rates, birth probabilities, and hazards are
  different encodings of the same quantum and convert onto births-per-woman through
  `docs/meta-analysis-effect-size-harmonization.md`, some needing a survival correction. This is part 3's
  world: the conversion is a known scalar and the machinery is untouched.
- **Different outcome level — not scalable.** Realized fertility, stated desires, period TFR, and
  completed cohort fertility are **different estimands**, not different units of one. Stated intentions do
  not convert to realized births (the earlier memos already keep them out); period and cohort measures
  embed tempo and composition differently. This is the §4 situation moved to the outcome: no scalar
  bridges the levels, so the operation is again *partition, do not pool* — one grid per outcome level —
  and TICK-080 item 9's "never pool across outcome levels" is this rule.

The choice of $Y$ is not only a harmonization question; it sets what the decomposition is *of*. The
accounting layer (A.9 / A.11) enters or vanishes with the outcome — zero by construction on cohort
fertility, large on the CBR — so "which $Y$ the column is in" and the item-10 netting are one decision,
to be made before the grids are built rather than after.

### 5.2 Bias

Drop "no biased estimates," and everything §4.2 quarantined returns: omitted confounders, colliders, bad
controls, and selection on unobservables in observational designs. An estimate becomes
$\hat\beta_i=\beta+b_i$, and the danger is structural, not statistical. Meta-analysis averages away
*sampling* error, not *bias*: if a shared confounder runs through a literature, the per-study biases are
correlated and the pool converges to $\beta+\bar b$, not $\beta$ — more studies tighten a wrong number.
Worse, the part-3 machinery actively spreads it: inverse-variance weighting hands the most weight to the
large, precise observational studies that are often the most biased (§2.4), and partial pooling shrinks a
clean quasi-experiment *toward* the biased majority, so borrowing strength can import bias across the
grid. This is where identification quality (E6) and the §4.1 GRADE ratings stop being a side column and
become weights or a gate: select the better-identified arm, bound the pool by the sign of the bias where
theory gives one, or fit a bias-aware model — and treat a cell's estimate as credible only to the GRADE
of the designs beneath it.

### 5.3 Publication bias

Drop "the observed estimates are a fair sample of those run." Selection on significance, size, or sign
truncates the meta-sample, so even unbiased-per-study estimates give an inflated pool. The review's
exposure is sharper than any single chapter's, because selection distorts a **ranking** more than a level
(TICK-080 item 11): the hypothesis that tops the table is disproportionately the one whose literature is
most inflated, and inflation is worst in small literatures on novel treatments — precisely the ones that
look most surprising when they rank high. The tools are the funnel-based correctors (PET-PEESE, with its
known over-correction under heterogeneity), selection models, and RoBMA; the reporting consequence is
that a point-estimate ordering is mostly noise past the top few, so the defensible output is a **tier
list with the pairwise comparisons that survive**, not a ranked list. Publication bias compounds §5.2
rather than replacing it — selection on significance sits on top of whatever confounding is already
there — so it is relaxed last, once the per-study bias model it rides on is in place.
