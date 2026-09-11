# The Numerator for a Comparable Share of Fertility Decline

**From:** Shravan Hari  
**Date:** September 11, 2026  
**Re:** What number quantifies "share of the decline explained by X," given the v3 frame

## 0. Goal, Formalism & Background

We are trying to operationalize the question: "How much of the fertility decline can be explained by a given hypothesis?"  
Formally speaking, let $\mathcal{D}$ be our set of hypotheses. We are looking for a function $s_{p,\ell}:\mathcal D \to \mathbb{R}$, possibly dependent on time period $p$ and location $\ell$, that maps each hypothesis to an "explanation score".  
I began with five axioms that a reasonable function $s$ had to satisfy:
 * **Comparability**: For any two hypotheses $D_1,D_2 \in \mathcal D$, the ratio between $s_{p,\ell}(D_1)$ and $s_{p,\ell}(D_2)$ should reflect the relative contributions of $D_1$ and $D_2$ to the fertility decline. This imposes that $s_{p,\ell}$ be linear in the hypothesis' true contribution.
 * **Computability**: $s_{p,\ell}$ should be computable exclusively using quantities that we extract while writing chapters - effect sizes, CIs, and $R^2$ values.
 * **Minimal assumptions**: In calculating $s_{p,\ell}(D)$, we should impose minimal structural/functional-form assumptions, particularly if they are not economically motivated.
 * **Normalization**: $\sum_{D \in \mathcal D} s_{p,\ell}(D)=1$ for all $(p,\ell)$ pairs.
 * **Non-redundancy**: if $D_1$'s effect on fertility runs through $D_2$, then $s_{p,\ell}(D_1)$ and $s_{p,\ell}(D_2)$ must not both count that channel.

Anup's 2026-08-30 memo builds what we might call the "denominator" of the function $s_{p,\ell}$. Without getting into the details of that memo, it requires that we determine, within each period-location pair, how much change in fertility _is_ there to explain? We'll refer to this number as $\Delta \text{TFR}_{p,\ell}$. This memo begins to answer the question of what the numerator should be.

## 1. Recommendation

Set the numerator to the change in TFR that $D$'s own effect produces over the part of $D$'s exposure
movement that no other hypothesis caused:

$$s_{p,\ell}(D) \;=\; \frac{\hat\beta_D \cdot \Delta\varepsilon_{D,p,\ell}}{\Delta \text{TFR}_{p,\ell}}$$

Here $\hat\beta_D$ is the identified total effect $d\,\text{TFR}/d\,X_D$ that $D$'s evidence base
supports, and $\Delta\varepsilon_{D,p,\ell}$ is the **autonomous movement** of $D$'s exposure variable
within the cell: the observed movement $\Delta X_{D,p,\ell}$ _minus_ the part that $D$'s causal parents
among the other hypotheses drove. Call $s_{p,\ell}$ the **attributable share**.

**The score residualizes the exposure and leaves the effect alone.** $\hat\beta_D$ is the total effect
our designs identify and PROTOCOL §4.1 already graded, so the graph enters through
$\Delta\varepsilon_{D,p,\ell}$ and we refit no estimate. §5 derives the two corrections a graph
makes available and shows why our evidence base supports this one.

**The correction is targeted rather than global.** A hypothesis with no causal parents in $\mathcal{D}$
has $\Delta\varepsilon_D = \Delta X_D$, so its attributable share equals its uncorrected share. Only
hypotheses whose exposure other hypotheses move get corrected, and §5 gives the correction a row per
causal edge.

**The attributable share differs from "share of variation explained."** Section 4 shows that the score
satisfying Axiom 1 in a variance frame is the correlation coefficient $r$, and that
$r = \beta\,\mathrm{sd}(X)/\mathrm{sd}(Y)$ is the uncorrected share with standard deviations in place
of observed changes.

## 2. What the axioms require

Axiom 1 separates the four candidates. Write $\text{contrib}_{p,\ell}(D)$ for $D$'s true contribution
to the decline in the cell. The axiom asks that

$$\frac{s_{p,\ell}(D_1)}{s_{p,\ell}(D_2)} \;=\; \frac{\text{contrib}_{p,\ell}(D_1)}{\text{contrib}_{p,\ell}(D_2)} \qquad \text{for all } D_1, D_2 \in \mathcal{D}$$

which holds if and only if there is a constant $c_{p,\ell} > 0$ with

$$s_{p,\ell}(D) \;=\; c_{p,\ell} \cdot \text{contrib}_{p,\ell}(D), \qquad c_{p,\ell} \text{ not depending on } D.$$

Every candidate in §3 takes the form $c \cdot \text{contrib}$ for some $c$. They differ only in whether
$c$ varies with the hypothesis being scored. A $c$ that depends on $D$ rescales each hypothesis by its
own factor before the comparison, which is the comparison Axiom 1 forbids. The recommended score has
$c_{p,\ell} = 1/\Delta\text{TFR}_{p,\ell}$, a constant of the cell, so residualizing the exposure term
leaves Axiom 1 intact.

**Axiom 2** restricts the inputs to what a chapter produces. **Axiom 3** asks for few named assumptions
that a reader can check one at a time, not for a score that rests on none; §8 lists the eight that
$s_{p,\ell}$ carries.

**Axiom 4** pins a constant the other three leave free. Axiom 1 determines $s$ only up to a positive
$c_{p,\ell}$, and Axiom 4 chooses it:

$$s_{p,\ell}(D) \;=\; \frac{\text{contrib}_{p,\ell}(D)}{\sum_{D' \in \mathcal{D}} \text{contrib}_{p,\ell}(D')}$$

a share in the literal sense. Axiom 4 also cuts against the $R^2$ family. When two exposures move
together, their separate $R^2$ values do not add up to the $R^2$ of a model holding both, and no
rescaling repairs that. Repair needs a method for splitting shared explanatory power among correlated
exposures (Shapley values, or LMG), which in turn needs a joint distribution over seventy separate
literatures that we cannot supply. Axiom 4 is also the axiom N3 was built to satisfy, since a
decomposition sums to one by construction. It therefore pulls toward N3, and Axiom 2 is the only reason
we cannot go there.

**Axiom 4 needs Axiom 5 to have any content.** Scores assembled from separate literatures sum past one,
because every chapter estimates a total effect in a literature that did not condition on the other
sixty-nine. The cheap repair adds a residual hypothesis $D_0$ to the set, defines
$s(D_0) = 1 - \sum_{D} s(D)$, and reads Axiom 4 on $\mathcal{D}^+ = \mathcal{D}\cup\{D_0\}$, where it
then holds. **It holds whatever the individual scores are**, which makes it a definition of $s(D_0)$ and
no restriction at all on $s$. Keep $D_0$, since the unexplained share of the decline is worth reporting
and a negative value flags over-claiming. Axiom 5 supplies the restriction the sum was supposed to
impose: the scores must form an additive decomposition of $\Delta\text{TFR}$, with each causal channel
counted once.

**Indexing $s$ by $(p,\ell)$ commits us to one score per cell rather than one per hypothesis.** M2 in §8
forces this, and v3 designed it that way: v3 §7 says "the resulting grid of location by period by
outcome is what a theory is tested against," and that "both a theory's external validity and its
economic significance are judged against those same cells." PROTOCOL §4.3's verdict grid therefore
becomes a region by state grid rather than three phenomenon rows.

## 3. Four candidate numerators

Write $s_{p,\ell}(D) = n_{p,\ell}(D) / \Delta\text{TFR}_{p,\ell}$. The candidates differ in the
numerator $n$, and the implied $c$ column decides among them.

| | Numerator $n_{p,\ell}(D)$ | Implied $c_{p,\ell}$ | Ax. 1 | Ax. 2 | Ax. 3 | Ax. 5 |
|---|---|---|---|---|---|---|
| **N1** | $\hat\beta_D \cdot \Delta\varepsilon_{D,p,\ell}$ | $1/\Delta\text{TFR}_{p,\ell}$, a constant of the cell | **Yes** | **Yes** for $\hat\beta$; the graph is an added input (§6) | 8 named assumptions (§8) | **Yes**, given the graph |
| **N2** | partial $R^2_D \times \mathrm{Var}(\text{TFR})$, v3 §9 as written | $\propto \hat\beta_D \mathrm{Var}(X_D)$, **depends on $D$** | **No** (§4) | No; papers rarely report partial $R^2$ | Needs a correct specification and the control set v3 §10 defers | No |
| **N3** | Formal decomposition (Bongaarts, Oaxaca-Blinder) | $1/\Delta\text{TFR}_{p,\ell}$ | Yes | No; needs a decomposition on macro data, not a paper | Heavy: the multiplicative proximate-determinants identity, or linear additive separability | Yes by construction |
| **N4** | Within-paper attributable $R^2$ share, v3 §12 interim | depends on the **paper's own frame**, hence on $D$ | **No** | Weak; needs regression output we mostly lack | Rests on an assumption v3 itself calls false | No |

v3 identifies N4's defect without naming it. §12 says the interim ranking is valid "only under the
assumption that a paper's own time period, location, and other frame choices are as good as randomly
assigned with respect to the theory it tests, an assumption known to be false." **That assumption is
Axiom 1 applied to N4.** Random assignment of frames is what would make $c$ independent of $D$. v3 and
this memo reject N4 by different routes.

N3 stays the strongest score and the least available one. Where a published decomposition exists for a
chapter, it remains the standard, and §5 shows that N1 with the graph correction is the same arithmetic
built from meta-analytic parts. N1 is the one we can compute 21 times.

## 4. Why $R^2$ violates Axiom 1, and what the variance frame's correct score is

In the bivariate case $R^2 = \beta^2 \mathrm{Var}(X)/\mathrm{Var}(Y)$, so for two hypotheses measured
on exposures of equal variance,

$$\frac{R^2_{D_1}}{R^2_{D_2}} \;=\; \left(\frac{\beta_1}{\beta_2}\right)^{\!2}.$$

A hypothesis contributing twice as much scores **four times** as high. The ratio of scores is the
square of the ratio of contributions, which violates Axiom 1 in the damaging direction: it widens the
apparent gap between the leading hypothesis and the rest, and that gap is what a reader will quote.

Take the square root and the violation disappears:

$$r \;=\; \beta \cdot \frac{\mathrm{sd}(X)}{\mathrm{sd}(Y)}$$

$r$ is linear in $\beta$, signed, unit-free, and satisfies Axiom 1 with $c = 1/\mathrm{sd}(Y)$, a
constant of the cell rather than of the hypothesis. It is the attributable share with $\mathrm{sd}()$
in place of $\Delta$. **If the denominator is a change, the score is $s_{p,\ell}$; if it is a standard
deviation, the score is $r$. In neither case is it $R^2$.** v3's "share of variation explained" is right
in spirit and one power too far in execution.

This memo works in the change frame, which is also PROTOCOL §4.2.1's binding convention. $r$ answers
the cross-region question, why regions differ from one another rather than why fertility fell within
one. If we ever put that question, $r$ goes in its own labelled column.

**$r$ carries a sign and $R^2$ does not.** On C.6.a, six of eighteen SDT countries clear
$R^2 \ge 0.15$, and all six do so with the correlation running *against* the prediction. $r$ shows that
in the score. Finding it under $R^2$ took a separate audit, and TICK-080 item 2 exists because $R^2$
hid it.

**The change frame also buys a decomposition that the variance frame cannot give us.** §5 sums the
attributable shares into an accounting identity that holds whatever the correlations among the exposures
are, because a linear structural equation for TFR is additive in its arguments. A variance decomposition
has no such property: correlated inputs are the reason Shapley values and LMG exist, and both need the
joint distribution across our seventy literatures that §2 says we cannot supply. Working in changes
means we never have to buy that distribution.

**$\hat\beta_D$ carries its identification and a macro refit does not.** $\hat\beta_D$ arrives from a
design we already graded under PROTOCOL §4.1. An $R^2$ refit on a country-year panel is a new
regression with no identification, and its value depends on the control set v3 §10 defers. A review
organized around identification should not build its headline score out of a statistic that discards
it.

## 5. DAG

Suppose the hypothesis exposures $X_1,\dots,X_n$ and TFR obey a linear structural system on an acyclic
graph $G$:

$$X_j \;=\; \sum_{k \in \mathrm{pa}(j)} \alpha_{jk} X_k + \varepsilon_j, \qquad \text{TFR} \;=\; \sum_j \beta_j^{\mathrm{dir}} X_j + \varepsilon_{\text{TFR}}$$

where $\mathrm{pa}(j)$ collects the parents of cause $X_j$, $\alpha_{jk}$ is the effect of $X_k$ on
$X_j$, and $\beta_j^{\mathrm{dir}}$ is the **direct** effect of $X_j$ on TFR holding the other exposures
fixed. The total effect $\hat\beta_j$ that a chapter identifies sums the direct effect and every
indirect path: in matrix form $\hat\beta = (I-A)^{-\top}\beta^{\mathrm{dir}}$, where $A$ collects the
$\alpha_{jk}$.

Differencing each equation across a cell gives two exact identities.

$$\textbf{(I)}\quad \Delta\text{TFR} \;=\; \sum_j \beta_j^{\mathrm{dir}}\,\Delta X_j \;+\; \Delta\varepsilon_{\text{TFR}}$$

$$\textbf{(II)}\quad \Delta\text{TFR} \;=\; \sum_j \hat\beta_j\,\Delta\varepsilon_j \;+\; \Delta\varepsilon_{\text{TFR}}, \qquad \Delta\varepsilon_j = \Delta X_j - \sum_{k \in \mathrm{pa}(j)} \alpha_{jk}\,\Delta X_k$$

Identity (I) restates TFR's own structural equation. Identity (II) follows from the reduced form
$\text{TFR} = \beta^{\mathrm{dir}\top}(I-A)^{-1}\varepsilon + \varepsilon_{\text{TFR}}$, whose
coefficient vector is the total-effect vector $\hat\beta$. **Both hold as arithmetic, not as
approximations, and neither requires the $\varepsilon_j$ to be uncorrelated.** Unobserved causes shared
between two exposures threaten our estimates of $\hat\beta$ and $\alpha$; they leave the accounting
alone.

A three-node example shows what separates them. Let $X_1 \to X_2 \to \text{TFR}$ and $X_1 \to
\text{TFR}$, so $X_2 = \alpha X_1 + \varepsilon_2$ and $\text{TFR} = \beta_1 X_1 + \beta_2 X_2 +
\varepsilon_{\text{TFR}}$. Identity (I) attributes $\beta_1 \Delta X_1 + \beta_2 \Delta X_2$. Identity
(II) attributes $(\beta_1 + \beta_2\alpha)\Delta X_1 + \beta_2(\Delta X_2 - \alpha \Delta X_1)$, which
multiplies out to the same total. **The two identities split the same decline differently.** (I) hands
each mediated path to the proximate variable that transmits it; (II) hands it to the root variable that
set it moving. That choice is `decisions/2026-06-14-proximate-vs-root-cause-categories.md` written as
arithmetic, and the graph makes it explicit rather than leaving it to whichever estimand a chapter
happened to extract.

**The uncorrected share is neither identity.** It pairs the total effect with the raw exposure change,
$\hat\beta_j \Delta X_j$, which gives $X_1$ credit for the path it drives through $X_2$ and gives $X_2$
credit for its full movement including the part $X_1$ drove. Summing uncorrected shares overshoots
identity (II) by

$$\text{excess}_{p,\ell} \;=\; \sum_j \hat\beta_j \left(\Delta X_j - \Delta\varepsilon_j\right) \;=\; \sum_j \hat\beta_j \sum_{k \in \mathrm{pa}(j)} \alpha_{jk}\,\Delta X_k$$

**Each term of that sum names one edge of the graph.** TICK-080 item 10 asks for the shares that sum
past one to be reportable; this is the report, one row per causal edge, in units of TFR. It also
separates overlap between two hypotheses from inflation inside one literature. The edge terms measure
the overlap, and whatever excess survives the correction, which shows up as a negative $s(D_0)$,
measures the inflation.

**Build on identity (II).** Three reasons, in order of weight. First, $\hat\beta_j$ is the estimand our
designs deliver and §4.1 graded, while identity (I) needs a direct effect from every chapter. Our
evidence base rarely reports one, and where a paper does condition on a mediator, that estimate is a
direct effect only if nothing unobserved causes both the mediator and fertility, which we cannot check
for most pairs. Second, a direct effect is defined against the variable set, so adding a seventy-first
hypothesis changes $\beta_j^{\mathrm{dir}}$ for every other hypothesis. Under (II) the graph-dependence
lands on $\Delta\varepsilon_j$ instead, which at least describes the world rather than our table of
contents. Third, (II) puts the root cause at the top of the column, matching how the review organizes
hypotheses in the first place.

## 6. What the graph must supply, and what it costs

Identity (II) needs one input that no chapter produces: the $\alpha_{jk}$ for each edge, which is the
effect of one hypothesis' exposure on another's. **These are not identified anywhere in our evidence base, and
most of them are not identified anywhere.** Axiom 5 costs us this, and it trades against
Axioms 2 and 3. Four things keep the price payable.

**Draw the graph over blocks, not hypotheses.** Eight to twelve families, following the tiering proposal
in TICK-080 item 10, with edges between blocks and no edges drawn inside one. A 70-node graph asks for
2,415 pairwise judgments we cannot defend; a 10-node graph asks for 45.

**Most of the content sits in the edges we omit.** An absent edge sets its correction term to zero and
needs no estimate. The $\alpha$ values matter only for the edges we assert, and the arithmetic falls
back to the uncorrected share wherever we assert nothing.

**Sign restrictions give bounds where point estimates fail.** Knowing that $\alpha_{jk} > 0$ and
$\Delta X_k < 0$ signs the correction term, so we can report $s_{p,\ell}$ as an interval running from
the uncorrected share to a bound built from the largest defensible $\alpha$. An interval that excludes
zero settles the question a point estimate would have settled.

**Merge cycles into a single block.** Female labor supply and fertility plausibly cause each other, as
do income and fertility, and an acyclic graph forbids that. v3's periods offer one way out, since
unrolling the feedback across periods restores acyclicity, at the cost of many more edges. Merging the
cycle into one block costs less: we report the block's share and decline to split it among its members,
which is what TICK-080 item 11 already recommends for the ranked output.

**We hold a first draft of the edge list.** `HYPOTHESES.md` carries 74 `cross-ref` fields, each naming
the root-cause category or the specific hypothesis that supplies a proximate mechanism's deeper
explanation. Most point at a category and a handful name a hypothesis, so the field needs promotion to
a machine-readable edge list before it can feed a score. The file also still heads that section
`## Demographic` rather than `## Proximate Causes`, so the 2026-06-14 decision never reached it.

## 7. Specifying the inputs

v3 keeps two levels apart. The **cell** $(p,\ell)$ is a region crossed with a milestone state, because
v3 §5 makes milestones regional: "the unit for defining a period is typically the region." The **unit
of analysis inside a cell** is the country, per v3 §12 Step Two. The region fixes when the window is,
and countries supply the observations that construct $\Delta X$ and $\Delta\text{TFR}$ within it. One
denominator per cell, many countries beneath it.

**Fix the cell at region by state for every hypothesis.** v3 §7 lets the unit float, allowing
"individual countries available as a finer unit inside a region where a theory's treatment variable is
measured at that level." Score $D_1$ on a region cell and $D_2$ on country cells inside it, and their
denominators differ, so $c$ depends on $D$ and Axiom 1 fails by construction. That is the defect
disqualifying N2 and N4, reached through the frame rather than through the statistic. Use country data
to construct $\Delta X$ inside a fixed cell. Measurement quality may vary by hypothesis; the
denominator may not. v3 §8's per-theory filtering is harmless by comparison, because Axiom 1 compares
$D_1$ and $D_2$ at a fixed $(p,\ell)$, so a hypothesis making no claim about a cell has no score there
instead of a score of zero.

- **$\hat\beta_D$.** The pooled estimate where the arm is poolable (≥3 studies *after* stratification),
  and the best-identified single estimate otherwise. The GRADE rating travels with the number unchanged.
  Each estimate needs a new extraction field recording what the design conditioned on, so that we can
  tell a total effect from a mediator-adjusted one. We do not record this today, for any chapter.
- **Units.** `docs/meta-analysis-effect-size-harmonization.md` defines the ladder, with births per woman
  as target unit 1. Conversions from birth probabilities and hazards need the survival correction.
  Stated intentions do not convert, and we should not make them.
- **$\Delta X_{D,p,\ell}$.** From macro panels, per cell. **This is the binding constraint on the
  proposal.** It is v3's Step Four, and `data/raw/` holds nothing but `.gitkeep`.
- **$\alpha_{jk}$.** Per asserted edge of the block graph, with a signed bound where no identified
  estimate exists. §6 gives the procedure; §9 prices the first pass.
- **$\Delta\text{TFR}_{p,\ell}$.** HFD/WPP, per cell, on the milestone definition.
- **Uncertainty.** We measure $\Delta X$ and $\Delta\text{TFR}$, so the interval on $s_{p,\ell}$ is
  $\hat\beta_D$'s interval scaled by $\Delta\varepsilon/\Delta\text{TFR}$, widened by the range of
  defensible $\alpha$ on the asserted edges. No delta method and no simulation, which counts toward
  Axiom 2.

## 8. The structural assumptions

| | Assumption | Check or bound |
|---|---|---|
| M1 | TFR is locally linear in $X_D$ over the realized $\Delta X$ | Dose-response where reported; bound $s$ with the smallest and largest identified $\hat\beta$ |
| M2 | $\hat\beta_D$ transports into the cell | What the v3 frame is for. Report $s$ per cell, and never pool $s$ across cells |
| M3 | A micro effect scales to an aggregate one | No cheap fix. Flag it, and sign the general-equilibrium offset where theory gives one |
| M4 | $\hat\beta_D$ is a total effect | The new extraction field in §7. Prefer designs whose estimand is the total effect, and drop mediator-adjusted estimates from the score rather than reading them as direct effects |
| M5 | $X_D$ is measured comparably across the frame | v3 Step Four. Fails most often for cultural and policy exposures |
| M6 | $\Delta X$ summarizes the exposure's movement in the cell | Holds where that movement is monotone. Report peak year, amplitude and net/amplitude beside $\Delta X$, and take the split from outside the data |
| M7 | The block graph omits no edge that carries weight, and contains no cycle | Publish the graph, its omissions and its merged blocks as a versioned artifact. A wrongly omitted edge leaves that channel double-counted, which is where we already are |
| M8 | $\alpha_{jk}$ is constant across the cell and signed as asserted | Report the bound, not a point, wherever no identified estimate exists |

M6 changes character under $s_{p,\ell}$, because $\Delta\varepsilon_{D,p,\ell}$ is a difference between
endpoints. A hump inside a cell nets the rise against the fall and drives the score toward zero for an
exposure that moved a great deal. C.6.a shows the size of the problem: its full-window sign test
returned 0 of 18 countries consistent, and splitting the window gave 14 of 18 early and 0 of 18 late.

Eight assumptions, each attached to a specific extractable field or to a published edge. Axiom 3 asks
for that rather than for a score resting on nothing, so a reader can list what $s_{p,\ell}$ assumes and
check the assumptions one at a time. M7 and M8 are the two that Axiom 5 added, and they are the two we
would be making in silence today if we published the uncorrected share and let the columns sum to 3.

## 9. Next steps

1. **Promote `cross-ref` to an edge list and collapse it to blocks.** Eight to twelve nodes, acyclic
   after merging, published in `decisions/` with the omitted edges named. This costs no data and settles
   M7.
2. **Add the conditioning field to extraction**, so that M4 becomes checkable on the chapters already
   drafted rather than assumed.
3. **Pilot on C.6.a.** Print three numbers beside each other: the chapter's existing $R^2$, the
   uncorrected share, and the attributable share $s_{p,\ell}$. C.6.a has 18
   SDT countries, a computed $R^2$, and a slope test pointing the other way, so the scores will diverge
   on numbers we already hold. Relative cohort size sits downstream of at least one other hypothesis, so
   the gap between the second and third numbers is the first double-count we measure.

Steps 1 and 2 run now. Step 3 needs `data/raw/` built, which is v3's Step Four, and which this memo has
now made a prerequisite for two numbers rather than one. That cost is worth pricing separately.
