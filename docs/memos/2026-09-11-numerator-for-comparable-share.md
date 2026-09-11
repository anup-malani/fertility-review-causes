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

Anup's 2026-08-30 memo builds what we might call the "denominator" of the function $s_{p,\ell}$. Without getting into the details of that memo, it requires that we determine, within each period-location pair, how much variation in fertility _is_ there to explain? We'll refer to this number as $\Delta \text{TFR}_{p,\ell}$. This memo begins to answer the question of what the numerator should be.

## 1. Recommendation

Set the numerator to the **attributable movement** — the change in TFR that $D$'s own effect, applied
to $D$'s own observed exposure movement, accounts for. That is

$$s_{p,\ell}(D) \;=\; \frac{\hat\beta_D \cdot \Delta X_{D,p,\ell}}{\Delta \text{TFR}_{p,\ell}}$$

where $\hat\beta_D$ is the identified effect $d\,\text{TFR}/d\,X_D$ that $D$'s evidence base supports,
and $\Delta X_{D,p,\ell}$ is the observed movement of $D$'s exposure variable within the cell. Call it
the **attributable share**. Of the four candidate numerators in §4 it is the only one that satisfies
all three axioms.

Two remarks before the argument.

**We already compute this and then discard it.** PROTOCOL §4.2's second bullet — slope sufficiency —
forms $\hat\beta_D \cdot \Delta X_D$, compares it to the observed range of TFR, and reports the
comparison as *sufficient / partial / insufficient*. The numerator and denominator are both already in
the pipeline; what is thrown away is the ratio itself. Recovering $s_{p,\ell}$ is less a new statistic
than an instruction to stop bucketing an existing one.

**This does not reject v3's "share of variation explained."** Section 5 shows that the variance-frame
score satisfying Axiom 1 is the correlation coefficient $r$, not $R^2$, and that
$r = \beta\,\mathrm{sd}(X)/\mathrm{sd}(Y)$ is exactly $s_{p,\ell}$ with standard deviations in place of
observed changes. The change frame and the variance frame give the same score against two different
benchmarks of movement. $R^2$ is that score squared, and the squaring is what breaks Axiom 1.

## 2. What the axioms require

Axiom 1 has sharp formal content worth extracting, because it is what separates the candidates. Write
$\text{contrib}_{p,\ell}(D)$ for $D$'s true contribution to the decline in the cell. The axiom asks
that

$$\frac{s_{p,\ell}(D_1)}{s_{p,\ell}(D_2)} \;=\; \frac{\text{contrib}_{p,\ell}(D_1)}{\text{contrib}_{p,\ell}(D_2)} \qquad \text{for all } D_1, D_2 \in \mathcal{D}$$

which holds if and only if there is a constant $c_{p,\ell} > 0$ with

$$s_{p,\ell}(D) \;=\; c_{p,\ell} \cdot \text{contrib}_{p,\ell}(D), \qquad c_{p,\ell} \text{ not depending on } D.$$

**The whole memo turns on that last clause.** Every candidate below is of the form
$c \cdot \text{contrib}$ for *some* $c$; what separates them is whether $c$ is allowed to vary with the
hypothesis being scored. A $c$ that depends on $D$ rescales each hypothesis by a different factor
before comparing them, which is precisely the comparison Axiom 1 forbids.

**Axiom 2** restricts the admissible inputs to what a chapter actually produces. In practice this is
narrower than the axiom states: effect sizes and CIs, not $R^2$. No extraction table in any of the 21
chapters carries an $R^2$ column, and partial or incremental $R^2$ — the quantity an $R^2$-based score
would need — is rarely reported in the papers even where a model $R^2$ is.

**Axiom 3** should be read as *few, named, and separately checkable*, not as *none*. §7 lists the five
that $s_{p,\ell}$ carries and what checks each.

One further observation about the formalism itself. **Indexing $s$ by $(p,\ell)$ is a substantive
commitment, not bookkeeping.** It says a hypothesis has no single score — it has one per cell — which
is the right consequence of M2 below, and which makes the verdict grid wider than PROTOCOL §4.3's
three rows.

## 3. The denominator: the notation says change, the gloss says variation

§0 writes the denominator $\Delta \text{TFR}_{p,\ell}$ and glosses it as "how much variation in
fertility *is* there to explain." The symbol is a change; the gloss is a variance. v3 has the identical
split — §3 and §9 speak of the share of *variation* explained, while §5 and §12 Step One define periods
as *states* a region occupies, which supports a change within a cell.

**Recommendation: close it as a change.** The review's question is what share of the *decline* a
mechanism carries; PROTOCOL §4.2.1 already fixes the change convention as binding; and a share of a
decline is what a reader of the verdict grid will take the number to mean. The variance reading
answers a real but different question — why regions differ from one another — and if we want it, §5
says exactly what it costs: the score must be $r$, not $R^2$, or Axiom 1 fails.

## 4. Four candidate numerators

Writing $s_{p,\ell}(D) = n_{p,\ell}(D) / \Delta\text{TFR}_{p,\ell}$, the candidates differ in the
numerator $n$, and the column that decides the question is the third.

| | Numerator $n_{p,\ell}(D)$ | Implied $c_{p,\ell}$ | Axiom 1 | Axiom 2 | Axiom 3 |
|---|---|---|---|---|---|
| **N1** | $\hat\beta_D \cdot \Delta X_{D,p,\ell}$ | $1/\Delta\text{TFR}_{p,\ell}$ — cell only | **Satisfied** | **Satisfied** — $\hat\beta$ and CI are extracted | 5 named assumptions (§7) |
| **N2** | partial $R^2_D \times \mathrm{Var}(\text{TFR})$ — v3 §9 as written | $\propto \hat\beta_D \mathrm{Var}(X_D)$ — **depends on $D$** | **Violated** (§5) | Violated — no $R^2$ field; partial $R^2$ rarely reported | Needs a correct specification and the control set v3 §10 defers |
| **N3** | Formal decomposition (Bongaarts, Oaxaca-Blinder) | $1/\Delta\text{TFR}_{p,\ell}$ | Satisfied by construction | Violated — needs a decomposition on macro data, not a paper | Heavy: the multiplicative proximate-determinants identity, or linear additive separability |
| **N4** | Within-paper attributable $R^2$ share — v3 §12 interim | depends on the **paper's own frame**, hence on $D$ | **Violated** | Weak — needs regression output we mostly lack | Rests on an assumption v3 itself calls false |

N4 is worth dwelling on, because v3 already identifies its defect without naming it as such. §12 says
the interim ranking is valid "only under the assumption that a paper's own time period, location, and
other frame choices are as good as randomly assigned with respect to the theory it tests — an
assumption known to be false." **That assumption is exactly Axiom 1 applied to N4**: random assignment
of frames is what would make $c$ independent of $D$. v3 and this memo reach the same verdict on N4 by
different routes, which is some evidence the axiom is the right one.

N3 is the strongest score and the least available one. It stays the gold standard in the few chapters
where a published decomposition exists. N1 is the one that can be computed 21 times.

## 5. Why $R^2$ violates Axiom 1, and what the variance frame's correct score is

In the bivariate case $R^2 = \beta^2 \mathrm{Var}(X)/\mathrm{Var}(Y)$, so for two hypotheses measured
on exposures of equal variance,

$$\frac{R^2_{D_1}}{R^2_{D_2}} \;=\; \left(\frac{\beta_1}{\beta_2}\right)^{\!2}.$$

A hypothesis contributing twice as much scores **four times** as high. The ratio of scores is the
square of the ratio of contributions, which is a direct violation of Axiom 1 — and it is a violation
in the damaging direction, since it inflates the apparent gap between the leading hypothesis and the
rest exactly where we most need the comparison to be honest.

Take the square root and the violation disappears:

$$r \;=\; \beta \cdot \frac{\mathrm{sd}(X)}{\mathrm{sd}(Y)}$$

$r$ is linear in $\beta$, signed, unit-free, and satisfies Axiom 1 with $c = 1/\mathrm{sd}(Y)$ — a
constant of the cell, not of the hypothesis. Structurally it is $s_{p,\ell}$ with $\mathrm{sd}()$ in
place of $\Delta$. **If the denominator is a change, the score is $s_{p,\ell}$; if it is a standard
deviation, the score is $r$. In neither case is it $R^2$.** v3's "share of variation explained" is
right in spirit and one power too far in execution.

Three consequences follow.

**The sign returns for free.** $r$ carries the sign that $R^2$ discards. On C.6.a, six of eighteen SDT
countries clear $R^2 \ge 0.15$ and all six do so with the correlation running *against* the
prediction. Under $r$ that is visible in the score; under $R^2$ it took a separate audit to find, and
TICK-080 item 2 exists only because $R^2$ hides it.

**Shares become additive, and the sum is interpretable.** If contributions are orthogonal and exhaust
the decline then $\sum_D \text{contrib}_{p,\ell}(D) = \Delta\text{TFR}_{p,\ell}$, so Axiom 1 gives
$\sum_D s_{p,\ell}(D) = 1$. An observed column summing to 3.4 is then a *measurement* of the failure
of orthogonality, plus literature inflation, plus non-comparability — the three-way attribution
TICK-080 item 10 proposes to report as a result. Under N2 no such identity exists and a sum past 1
means nothing at all.

**Identification is inherited rather than discarded.** $\hat\beta_D$ arrives from a design already
graded under PROTOCOL §4.1. An $R^2$ refit on a country-year macro panel is a new and unidentified
regression whose value depends on a control set v3 §10 explicitly defers. Building the headline score
out of $R^2$ throws away the identification the review spent 21 chapters establishing, which is a
strange thing for a review organized around identification to do.

## 6. Specifying the three inputs

- **$\hat\beta_D$.** The pooled estimate where the arm is poolable (≥3 studies *after* stratification),
  the best-identified single estimate otherwise. The GRADE rating travels with the number unchanged.
- **Units.** `docs/meta-analysis-effect-size-harmonization.md` already defines the ladder, with births
  per woman as target unit 1. Conversions from birth probabilities and hazards need the survival
  correction; conversions from stated intentions are not conversions and should not be made.
- **$\Delta X_{D,p,\ell}$.** From macro panels, per cell. **This is the binding constraint on the
  entire proposal** — it is v3's Step Four, and `data/raw/` currently holds nothing but `.gitkeep`.
- **$\Delta\text{TFR}_{p,\ell}$.** HFD/WPP, per cell, on the milestone definition.
- **Uncertainty.** $\Delta X$ and $\Delta\text{TFR}$ are measured, so the interval on $s_{p,\ell}$ is
  $\hat\beta_D$'s interval scaled by $\Delta X/\Delta\text{TFR}$ — no delta method, no simulation. That
  is a further point for Axiom 2.

## 7. The structural assumptions

| | Assumption | Check or bound |
|---|---|---|
| M1 | TFR is locally linear in $X_D$ over the realized $\Delta X$ | Dose-response where reported; bound $s$ with the smallest and largest identified $\hat\beta$ |
| M2 | $\hat\beta_D$ transports into the cell | What the v3 frame is for. Report $s$ per cell; never pool $s$ across cells |
| M3 | A micro effect scales to an aggregate one | No cheap fix. Flag, and sign the likely GE offset where theory gives one |
| M4 | $\hat\beta_D$ is a total effect, not a partial one | v3 §10's control-variable tension, arriving from the other side. Prefer designs whose estimand is the total effect |
| M5 | $X_D$ is measured comparably across the frame | v3 Step Four; fails loudest for the cultural and policy exposures |

Five assumptions, each attached to a specific extractable field. That is what Axiom 3 should mean in
practice — not that the score is assumption-free, but that a reader can enumerate what it rests on and
check the assumptions one at a time.

## 8. Calls for you

1. **Is $\Delta\text{TFR}_{p,\ell}$ a change or a variance?** (§3.) Everything downstream turns on it,
   and §5 prices the variance branch: the score becomes $r$.
2. **Does the numerator come from $\hat\beta_D$ or from a macro refit?** Identification inheritance
   says $\hat\beta_D$.
3. **§0 indexes $s$ by $(p,\ell)$, which settles cell-level versus pooled scoring in favour of
   cell-level.** Confirm that is intended: it widens PROTOCOL §4.3's grid from three phenomenon rows
   to a full region × state grid.
4. **Does $s_{p,\ell}$ replace the three-route disjunction in §4.2 entirely, or join it as a fourth
   route?** The disjunction is what TICK-080 item 1 is about, and a single score dissolves it.

## 9. Next step

Compute $s_{p,\ell}$ end-to-end on one drafted chapter and print it beside that chapter's existing
$R^2$. C.6.a is the natural pilot: it already has 18 SDT countries, a computed $R^2$, and a slope test
pointing the other way, so it shows the divergence between the two scores on real numbers rather than
in the abstract. It needs `data/raw/` built first, which is the real cost here and is worth pricing
separately.
