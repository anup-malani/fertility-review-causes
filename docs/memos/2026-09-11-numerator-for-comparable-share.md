# The Numerator for a Comparable Share of Fertility Decline

**From:** Shravan Hari  
**Date:** September 11, 2026  
**Re:** What number quantifies "share of the decline explained by X," given the v3 frame

## 0. Goal, Formalism & Background

We are trying to operationalize the question: "How much of the fertility decline can be explained by a given hypothesis?"  
Formally speaking, let $\mathcal{D}$ be our set of hypotheses. We are looking for a function $s_{p,\ell}:\mathcal D \to \mathbb{R}$, possibly dependent on time period $p$ and location $\ell$, that maps each hypothesis to an "explanation score".  
I began with three axioms that a reasonable function $s$ had to satisfy:
 * **Comparability**: For any two hypotheses $D_1,D_2 \in \mathcal D$, the ratio between $s_{p,\ell}(D_1)$ and $s_{p,\ell}(D_2)$ should reflect the relative contributions of $D_1$ and $D_2$ to the fertility decline. This imposes that $s_{p,\ell}$ be linear in the hypothesis' true contribution.
 * **Computability**: $s_{p,\ell}$ should be computable exclusively using quantities that we extract while writing chapters - effect sizes, CIs, and $R^2$ values.
 * **Minimal assumptions**: In calculating $s_{p,\ell}(D)$, we should impose minimal structural/functional-form assumptions, particularly if they are not economically motivated.
 * **Normalization** (enforced later): $\sum_{D \in \mathcal D} s_{p,\ell}(D)=1$ for all $(p,\ell)$ pairs.

Anup's 2026-08-30 memo builds what we might call the "denominator" of the function $s_{p,\ell}$. Without getting into the details of that memo, it requires that we determine, within each period-location pair, how much change in fertility _is_ there to explain? We'll refer to this number as $\Delta \text{TFR}_{p,\ell}$. This memo begins to answer the question of what the numerator should be.

## 1. Recommendation

Set the numerator to the change in TFR that $D$'s own effect produces over $D$'s own observed exposure
movement:

$$s_{p,\ell}(D) \;=\; \frac{\hat\beta_D \cdot \Delta X_{D,p,\ell}}{\Delta \text{TFR}_{p,\ell}}$$

Here $\hat\beta_D$ is the identified effect $d\,\text{TFR}/d\,X_D$ that $D$'s evidence base supports,
and $\Delta X_{D,p,\ell}$ is the observed movement of $D$'s exposure variable within the cell. Call it
the **attributable share**. Of the four candidate numerators in §3, it alone satisfies all three axioms.

**We already compute this and then bucket it.** PROTOCOL §4.2's second bullet, slope sufficiency, forms
$\hat\beta_D \cdot \Delta X_D$, compares it to the observed range of TFR, and reports the comparison as
*sufficient / partial / insufficient*. Both the numerator and the denominator already sit in the
pipeline.

**The attributable share differs from "share of variation explained."** Section 4 shows that the score
satisfying Axiom 1 in a variance frame is the correlation coefficient $r$, and that
$r = \beta\,\mathrm{sd}(X)/\mathrm{sd}(Y)$ is $s_{p,\ell}$ with standard deviations in place of
observed changes.

## 2. What the axioms require

Axiom 1 separates the four candidates. Write $\text{contrib}_{p,\ell}(D)$ for $D$'s true contribution
to the decline in the cell. The axiom asks that

$$\frac{s_{p,\ell}(D_1)}{s_{p,\ell}(D_2)} \;=\; \frac{\text{contrib}_{p,\ell}(D_1)}{\text{contrib}_{p,\ell}(D_2)} \qquad \text{for all } D_1, D_2 \in \mathcal{D}$$

which holds if and only if there is a constant $c_{p,\ell} > 0$ with

$$s_{p,\ell}(D) \;=\; c_{p,\ell} \cdot \text{contrib}_{p,\ell}(D), \qquad c_{p,\ell} \text{ not depending on } D.$$

Every candidate in §3 takes the form $c \cdot \text{contrib}$ for some $c$. They differ only in whether
$c$ varies with the hypothesis being scored. A $c$ that depends on $D$ rescales each hypothesis by its
own factor before the comparison, which is the comparison Axiom 1 forbids.

**Axiom 2** restricts the inputs to what a chapter produces. **Axiom 3** asks for few named assumptions
that a reader can check one at a time, not for a score that rests on none; §6 lists the six that
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

**Imposing Axiom 4.** $s_{p,\ell}$ as defined in §1 does not satisfy Axiom 4 on $\mathcal{D}$, and no
score assembled from separate literatures will. Every chapter estimates a total effect in a literature
that did not condition on the other sixty-nine. Where $D_1$ operates through $D_2$, both literatures
report an effect and both chapters correctly claim the same share of the decline. The raw scores sum
past one for reasons that have nothing to do with any chapter being wrong.

**We impose Axiom 4 by adding the residual to the set.** Let $\mathcal{D}^+ = \mathcal{D} \cup \{D_0\}$
with

$$s_{p,\ell}(D_0) \;:=\; 1 - \sum_{D \in \mathcal{D}} s_{p,\ell}(D)$$

and read the axiom as a statement about $\mathcal{D}^+$, where it holds by construction. We rescale no
individual score, so $s_{p,\ell}(D)$ keeps its absolute meaning: this share of the observed decline,
rather than this share of whatever we enumerated. $s(D_0)$ is the unexplained share of the decline.
Where the enumerated hypotheses over-claim, $s(D_0)$ goes negative, and its magnitude measures how much
they overlap and how far their literatures are inflated.

**Indexing $s$ by $(p,\ell)$ commits us to one score per cell rather than one per hypothesis.** M2 in §6
forces this, and v3 designed it that way: v3 §7 says "the resulting grid of location by period by
outcome is what a theory is tested against," and that "both a theory's external validity and its
economic significance are judged against those same cells." PROTOCOL §4.3's verdict grid therefore
becomes a region by state grid rather than three phenomenon rows.

## 3. Four candidate numerators

Write $s_{p,\ell}(D) = n_{p,\ell}(D) / \Delta\text{TFR}_{p,\ell}$. The candidates differ in the
numerator $n$, and the implied $c$ column decides among them.

| | Numerator $n_{p,\ell}(D)$ | Implied $c_{p,\ell}$ | Axiom 1 | Axiom 2 | Axiom 3 |
|---|---|---|---|---|---|
| **N1** | $\hat\beta_D \cdot \Delta X_{D,p,\ell}$ | $1/\Delta\text{TFR}_{p,\ell}$, a constant of the cell | **Satisfied** | **Satisfied**; $\hat\beta$ and CI are extracted | 6 named assumptions (§6) |
| **N2** | partial $R^2_D \times \mathrm{Var}(\text{TFR})$, v3 §9 as written | $\propto \hat\beta_D \mathrm{Var}(X_D)$, **depends on $D$** | **Violated** (§4) | Violated; no $R^2$ field, and papers rarely report partial $R^2$ | Needs a correct specification and the control set v3 §10 defers |
| **N3** | Formal decomposition (Bongaarts, Oaxaca-Blinder) | $1/\Delta\text{TFR}_{p,\ell}$ | Satisfied by construction | Violated; needs a decomposition on macro data, not a paper | Heavy: the multiplicative proximate-determinants identity, or linear additive separability |
| **N4** | Within-paper attributable $R^2$ share, v3 §12 interim | depends on the **paper's own frame**, hence on $D$ | **Violated** | Weak; needs regression output we mostly lack | Rests on an assumption v3 itself calls false |

v3 identifies N4's defect without naming it. §12 says the interim ranking is valid "only under the
assumption that a paper's own time period, location, and other frame choices are as good as randomly
assigned with respect to the theory it tests, an assumption known to be false." **That assumption is
Axiom 1 applied to N4.** Random assignment of frames is what would make $c$ independent of $D$. v3 and
this memo reject N4 by different routes.

Axiom 4 orders the four differently: N3 satisfies it by construction, N1 satisfies it on
$\mathcal{D}^+$, and N2 and N4 cannot satisfy it for the reason §2 gives.

N3 is the strongest score and the least available one. It stays the standard in the few chapters where
a published decomposition exists. N1 is the one we can compute 21 times.

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
constant of the cell rather than of the hypothesis. It is $s_{p,\ell}$ with $\mathrm{sd}()$ in place of
$\Delta$. **If the denominator is a change, the score is $s_{p,\ell}$; if it is a standard deviation,
the score is $r$. In neither case is it $R^2$.** v3's "share of variation explained" is right in spirit
and one power too far in execution.

This memo works in the change frame, which is also PROTOCOL §4.2.1's binding convention. $r$ answers
the cross-region question, why regions differ from one another rather than why fertility fell within
one. If we ever put that question, $r$ goes in its own labelled column.

**$r$ carries a sign and $R^2$ does not.** On C.6.a, six of eighteen SDT countries clear
$R^2 \ge 0.15$, and all six do so with the correlation running *against* the prediction. $r$ shows that
in the score. Finding it under $R^2$ took a separate audit, and TICK-080 item 2 exists because $R^2$
hid it.

**Scores in a column can be summed, which is what makes Axiom 4 statable.** $s_{p,\ell}$ is linear in
$\beta$ and denominated in the units of the decline, so a column totalling 3.4 tells us how much the
mechanisms overlap, how far their literatures are inflated, and how far their estimands sit from
comparable. §2 carries that excess in $s(D_0)$. N2 supports no such arithmetic.

**$\hat\beta_D$ carries its identification and a macro refit does not.** $\hat\beta_D$ arrives from a
design we already graded under PROTOCOL §4.1. An $R^2$ refit on a country-year panel is a new
regression with no identification, and its value depends on the control set v3 §10 defers. A review
organized around identification should not build its headline score out of a statistic that discards
it.

## 5. Specifying the three inputs

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
- **Units.** `docs/meta-analysis-effect-size-harmonization.md` defines the ladder, with births per woman
  as target unit 1. Conversions from birth probabilities and hazards need the survival correction.
  Stated intentions do not convert, and we should not make them.
- **$\Delta X_{D,p,\ell}$.** From macro panels, per cell. **This is the binding constraint on the
  proposal.** It is v3's Step Four, and `data/raw/` holds nothing but `.gitkeep`.
- **$\Delta\text{TFR}_{p,\ell}$.** HFD/WPP, per cell, on the milestone definition.
- **Uncertainty.** We measure $\Delta X$ and $\Delta\text{TFR}$, so the interval on $s_{p,\ell}$ is
  $\hat\beta_D$'s interval scaled by $\Delta X/\Delta\text{TFR}$. No delta method and no simulation,
  which counts toward Axiom 2.

## 6. The structural assumptions

| | Assumption | Check or bound |
|---|---|---|
| M1 | TFR is locally linear in $X_D$ over the realized $\Delta X$ | Dose-response where reported; bound $s$ with the smallest and largest identified $\hat\beta$ |
| M2 | $\hat\beta_D$ transports into the cell | What the v3 frame is for. Report $s$ per cell, and never pool $s$ across cells |
| M3 | A micro effect scales to an aggregate one | No cheap fix. Flag it, and sign the general-equilibrium offset where theory gives one |
| M4 | $\hat\beta_D$ is a total effect, not a partial one | The control-variable tension v3 §10 raises. Prefer designs whose estimand is the total effect |
| M5 | $X_D$ is measured comparably across the frame | v3 Step Four. Fails most often for cultural and policy exposures |
| M6 | $\Delta X$ summarizes the exposure's movement in the cell | Holds where that movement is monotone. Report peak year, amplitude and net/amplitude beside $\Delta X$, and take the split from outside the data |

M6 changes character once we adopt $s_{p,\ell}$, because $\Delta X_{D,p,\ell}$ is itself an endpoint
difference. A hump inside a cell nets the rise against the fall and drives the score toward zero for an
exposure that moved a great deal. C.6.a shows the size of the problem: its full-window sign test
returned 0 of 18 countries consistent, and splitting the window gave 14 of 18 early and 0 of 18 late.

Six assumptions, each attached to a specific extractable field. Axiom 3 asks for that rather than for a
score resting on nothing, so a reader can list what $s_{p,\ell}$ assumes and check the assumptions one
at a time.

## 7. Next step

Compute $s_{p,\ell}$ end-to-end on one drafted chapter and print it beside that chapter's existing
$R^2$. C.6.a is the natural pilot. It has 18 SDT countries, a computed $R^2$, and a slope test pointing
the other way, so the two scores will diverge on numbers we already hold. It needs `data/raw/` built
first, which is the cost of this memo and is worth pricing separately.
