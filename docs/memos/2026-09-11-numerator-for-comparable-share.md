# The Numerator for a Comparable Share of Fertility Decline

**To:** Anup Malani
**From:** Shravan
**Date:** September 11, 2026
**Re:** What number quantifies "share of the decline explained by X," given the v3 frame

## 1. Recommendation

Use the **attributable share**

> **S = β̂ · ΔX / ΔTFR**

the identified effect of the mechanism on fertility, times the observed movement of the exposure over
a cell of the standardized frame, over that cell's observed change in TFR. It is unit-free, linear in
the effect size, signed, and computable today from fields our extraction tables already carry. It is
the only candidate of the four below that satisfies all three criteria.

Two things about this recommendation are worth stating at the top. First, **S already exists in the
protocol.** PROTOCOL §4.2's second bullet — "slope sufficiency" — computes exactly β̂ · ΔX against the
observed range of TFR, and then discards the ratio into a three-level bucket (sufficient / partial /
insufficient). We do not need a new statistic so much as we need to stop throwing this one away.

Second, **S is not a rejection of the v3 framework's "share of variation explained."** It is that
quantity's linear form. Section 5 below shows that the variance-frame statistic satisfying criterion 1
is the correlation coefficient *r*, not R² — and that r = β · sd(X)/sd(Y) is S with standard deviations
in place of observed changes. The two framings are the same object measured against two different
benchmarks of movement. R² is their square, and squaring is what breaks the comparison.

## 2. The criteria, stated precisely

**C1 — Comparable, with interpretable differences.** Stronger than a common scale. It requires that
the difference between two hypotheses' values mean "this one accounts for that much more of the
decline." That demands the statistic be **linear in the mechanism's contribution**. A convex transform
of a contribution is still comparable in the weak sense of being on one axis, and still useless for
saying how much more.

**C2 — Computable from what we extract.** Effect size, CI, and R². In practice the first two: no
extraction table in any of the 21 chapters has an R² column, and partial or incremental R² is rarely
reported in the papers themselves even when a model R² is.

**C3 — Minimal structural and functional-form assumptions.** Not zero assumptions. Few, named, and
each separately checkable against something we hold.

## 3. The denominator is nearly settled, but v3 leaves one fork open

The v3 memo fixes the outcome (TFR), keys periods to demographic milestones rather than calendar
years, and sets locations at the region level. That is the denominator, and it is the right move —
it is what makes two chapters' numbers refer to the same movement.

One ambiguity has to be closed before the numerator can be chosen. v3 §3 and §9 speak of "how much
variation in the outcome there is to explain" and "the share of variation the treatment variable
explains." v3 §5 and §12 Step One define periods as *states* a region occupies — above replacement,
below replacement. The first is a **variance across cells**; the second supports a **change within a
cell**. These are different denominators and they take different numerators.

**Recommendation: the denominator is a change within a cell.** The review's question is what share of
the *decline* a mechanism carries, PROTOCOL §4.2.1 already fixes the change convention as binding, and
a share of a decline is what a reader of the verdict grid will take the number to mean. The
variance-across-cells statistic answers a real and different question — why regions differ from each
other — and if we want it, it should be reported as a second, separately labelled column, not folded
into the same cell.

## 4. Four candidate numerators

| | Numerator | C1 comparable | C2 computable | C3 assumptions |
|---|---|---|---|---|
| **N1** | β̂ · ΔX | **Yes** — linear in β, unit-free ratio, signed | **Yes** — β̂ and CI are extracted; ΔX and ΔTFR from macro panels | 5 named assumptions (§7), each checkable |
| **N2** | partial R² × Var(TFR) — v3 §9 as written | **No** — quadratic in β, sign-blind, non-additive | **No** — no R² field exists; partial R² rarely reported | Requires a correctly specified model and a control set v3 §10 defers |
| **N3** | Formal decomposition (Bongaarts, Oaxaca-Blinder) | Yes — it is a share of the change by construction | **No** — not extractable from a paper; needs a full decomposition on macro data | Heavy: the multiplicative proximate-determinants identity, or linear additive separability |
| **N4** | Within-paper attributable R² share — v3 §12 interim | **No** — inherits N2's defects, plus each paper's own frame | Weak — needs regression output we mostly do not have | Rests on an assumption v3 itself calls false |

N3 is the strongest statistic and the least available one; it stays as the gold standard for the few
chapters where a published decomposition exists. N1 is the one that can actually be computed 21 times.

## 5. Why R² fails criterion 1, and what the variance frame's correct statistic is

This is the load-bearing argument, so it is worth being exact. In the bivariate case,

> R² = β² · Var(X) / Var(Y)

R² is **quadratic in the effect size**. Doubling a mechanism's effect quadruples its R² share while
only doubling its share of the decline. Differences in R² therefore do not measure differences in
contribution; they measure differences in a convex transform of contribution, which systematically
exaggerates the gap between a large mechanism and a moderate one. That is a direct failure of C1.

Take the square root and the problem disappears:

> r = β · sd(X) / sd(Y)

The correlation coefficient is **linear in β**, signed, and unit-free — and it is structurally
identical to S = β · ΔX / ΔTFR, with sd() in place of Δ. **If the frame's benchmark of movement is a
standard deviation, the statistic that satisfies C1 is r. If it is an observed change, the statistic is
S.** v3's "share of variation explained" is correct in spirit and goes one power too far in execution.
Reporting r instead of R² also disposes of the sign-blindness in TICK-080 item 2 for free, since r
carries the sign that R² discards. On C.6.a, six of eighteen SDT countries clear R² ≥ 0.15 and all six
do so with the correlation running against the prediction; r would have shown that in the statistic
rather than requiring a separate audit to discover it.

Two further reasons to prefer S over any R²-family statistic:

**Additivity.** Because S is linear in β, shares are additive when mechanisms are orthogonal. A column
summing past 1 is then a *measurement* of overlap, literature inflation, and non-comparability — the
quantity TICK-080 item 10 proposes to report as a result. Under R² a sum past 1 has no such reading; it
is simply uninterpretable.

**Identification inheritance.** β̂ arrives from a study whose design we have already graded under
PROTOCOL §4.1. A macro R² refit on a country-year panel does not inherit that identification — it is a
new, unidentified regression, and its value depends on a control set that v3 §10 explicitly defers.
Building the headline statistic out of R² discards the identification the review spent 21 chapters
establishing, which is a strange thing for a review organized around identification to do.

## 6. Specifying S

- **Which β̂.** The pooled estimate where the arm is poolable (≥3 studies *after* stratification), the
  best-identified single estimate otherwise. The GRADE rating travels with the number, unchanged.
- **Units.** `docs/meta-analysis-effect-size-harmonization.md` already defines the ladder, with births
  per woman as target unit 1. Conversions from birth probabilities and hazards need the survival
  correction; conversions from intentions are not conversions and should not be made.
- **ΔX.** From macro panels, per cell. **This is the binding constraint on the whole proposal** — it is
  v3's Step Four, and `data/raw/` currently holds nothing but `.gitkeep`.
- **ΔTFR.** HFD/WPP, per cell, by the milestone definition.
- **Uncertainty.** ΔX and ΔTFR are measured, so S's interval is β̂'s interval scaled by ΔX/ΔTFR — no
  delta method, no simulation. Cheap, and a further point for C2.

## 7. Assumptions, and what checks each one

| | Assumption | Check or bound |
|---|---|---|
| A1 | TFR is locally linear in X over the realized ΔX | Dose-response where reported; bound S with the smallest and largest identified β |
| A2 | β̂ transports to the cell | This is what the v3 frame is for. Report S per cell; do not pool S across cells |
| A3 | A micro effect scales to an aggregate one | No cheap fix. Flag, and sign the likely GE offset where theory gives one |
| A4 | β̂ is the total effect, not a partial one | v3 §10's control-variable tension, arriving from the other side. Prefer designs whose estimand is the total effect |
| A5 | X is measured comparably across the frame | v3 Step Four; fails loudest for the cultural and policy exposures |

Five assumptions, each attached to a specific extractable field. That is what C3 should mean — not that
the number is assumption-free, but that a reader can see every assumption it rests on and check them
one at a time.

## 8. Calls for you

1. **Change or variance denominator** (§3). Everything downstream depends on it.
2. **Does the numerator come from β̂, or from a macro refit?** Identification inheritance says β̂.
3. **Cell-level S, or one pooled S per hypothesis?** A2 says cell-level, which makes the verdict grid
   wider than §4.3 currently is.
4. **Does S replace the three-route disjunction entirely**, or become a fourth route?

## 9. Next step

Compute S end-to-end on one drafted chapter and put it beside that chapter's existing R². C.6.a is the
natural pilot: it already has 18 SDT countries, a computed R², and a slope test that points the other
way, so it will show the divergence between the two statistics concretely rather than in the abstract.
It requires `data/raw/` to be built first, which is the real cost of this memo and is worth pricing
separately.
