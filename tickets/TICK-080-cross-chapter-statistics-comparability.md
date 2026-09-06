# TICK-080: Cross-chapter statistics — comparability, the demsig routes, and the sign-blind R²
**Status:** in-progress
**Assigned:** Shravan
**Parallel-safe:** yes — but any resolution is **retroactive** (see *What this costs*)
**Blocks:** none
**Blocked by:** none
**Touches:** `PROTOCOL.md` §4.1–§4.3, `decisions/`, `docs/chapter-template.md`,
`source/analysis/` (a new cross-chapter table generator), `output/tables/`

## Description

This is a standing methods ticket, not a hypothesis. Its subject is the statistics themselves: what
each chapter is licensed to compute, and whether two chapters' numbers can be put in the same table.

Twenty-one chapters now exist in some state of draft. Each one ends in the §4.3 verdict grid — a
GRADE rating and a demographic-significance band per phenomenon — and that grid is the review's
headline output. It is also the one artifact that must be **comparable across hypotheses**, because
the whole point of the review is that a reader can look down the column and see which explanations
carry the decline. Nothing in the pipeline currently guarantees that comparability, and the chapters
run so far have surfaced twelve specific ways it fails. They are itemized below with the evidence that
produced them; each is a question for the PI, not a defect with an obvious fix.

### 1. The three demsig routes are OR'd, they can contradict, and they do not decompose the same moment

§4.2 makes a hypothesis demographically significant if **any one** of decomposition share ≥ 10%,
slope sufficiency = "sufficient", or conditional R² ≥ 0.15 clears. The routes are not
interchangeable, they are not equally strong, and on at least one chapter they disagree in opposite
directions. On C.6.a (Easterlin), the R² route certifies the hypothesis while the slope route refutes
it — the exposure moved the *wrong way* across the SDT window. Read literally, the OR gives C.6.a a
`significant` cell.

Underneath the disagreement is a **category difference that the OR hides**. Routes 1 and 2 decompose a
*change in a mean*: what fraction of the observed fall in TFR the mechanism accounts for. Route 3
decomposes a *variance*. These are different moments of different quantities, and no threshold
convention makes them interchangeable. §4.2.1 already implies this — it fixes the FDT and SDT
denominators as changes and the PM denominator as a *range* — which means **route 3 is well-posed at
PM, where the phenomenon is variation, and category-mismatched at FDT and SDT, where it is not.**
That asymmetry is nowhere in the protocol as written.

The live options are therefore wider than a precedence rule: precedence, conjunction, an explicit
"routes disagree" verdict, or **demoting route 3 from a certification route to a diagnostic** at the
two decline phenomena while keeping it at PM. See item 4 — the demotion case is stronger than the
sign problem alone makes it look.

### 2. R² is sign-blind

The third route has no sign condition. **R² does not know the direction of the relationship**, so a
tight fit running *against* the hypothesis clears 0.15 exactly as a confirming one does.

Measured on C.6.a: of 18 SDT countries, 6 clear R² ≥ 0.15 for TFR on relative cohort size, and **all
6 do so with the correlation running against the prediction** — Japan R² = 0.71 at r = +0.84,
Switzerland 0.46 at +0.68, Korea 0.44 at +0.66. This is invisible in any chapter whose fitted sign
happens to be right, so it will not surface on its own. Already raised as C.6.a's PI Call 3; it
belongs here rather than in one chapter, because the answer changes every chapter's third route.

### 3. "Conditional R² ≥ 0.15" does not name one statistic

§4.2 lists **two** R² benchmarks — within-country time-series, and cross-country within-period —
"alone and conditional on standard controls". The threshold sentence then refers to "its conditional
R²", singular, and no control set is specified anywhere. Two chapters can each report a defensible
number, compare it to the same 0.15, and be measuring different things.

### 4. 0.15 is below the spurious-regression floor

This is item 3's problem in its severe form, and it is independent of the sign condition. Two
**independent random walks** routinely produce R² around 0.3 in finite samples — the Granger–Newbold
spurious-regression result. TFR trends monotonically across both the FDT and the SDT window, so any
exposure that also trends will clear 0.15 on shared trend alone.

A threshold that two unrelated random walks clear roughly twice over is not discriminating between
hypotheses, which is the only job it has here. Either the route is restricted to differenced or
detrended series with the autocorrelation modelled explicitly, or the threshold moves by an order of
magnitude, or route 3 stops certifying anything at FDT and SDT. Note that the sign condition in item 2
does **not** rescue this: a wrongly-signed spurious fit and a rightly-signed spurious fit are equally
uninformative, and the sign condition only removes the first.

### 5. GRADE has no band for an empty cell

A.23's registered cell held 38 screened records, **two extracted effects and zero identified
designs**, and neither effect estimated the registered exposure on fertility. `VERY LOW` is the only
available rating and it is actively misleading: a reader takes it for a badly identified body of
evidence rather than an absent one, and those imply different next steps — read more carefully versus
run a study that does not exist. Proposed value: **UNEVALUATED**, with a mandatory sentence beside it.

### 6. GRADE has no band for a non-effect estimand

§4.1's bands are identification strategies. A competent twin design estimating a variance component
falls to "Very low: correlational only", which reads as *badly identified* when the truth is
*different question, answered well*. A.18 hit this on every arm. Proposed value: **NOT RATEABLE —
non-effect estimand**.

### 7. Variance components, denominators, and what PM's "range" admits

§4.2.1 fixes the denominator as a *change* for FDT and SDT and a *range* for PM. A variance component
therefore has no numerator at FDT or SDT — there is no counterfactual in which the component is
withdrawn — but PM is explicitly a variation phenomenon, so a variance share is the right *kind* of
numerator there. Two problems in that PM cell, both live:

- **Units.** h² is *within*-population *between-individual*; §4.2.1's PM denominator is a range
  *across* populations; §2's other clause is within-population *over time*. h² matches none of the
  three as written.
- **The share is near-definitional.** Divide h² by a within-population variance and h² comes back
  out. The 10% threshold degrades to "is h² ≥ 0.10", and the cell prints `significant` while meaning
  far less than the same word means in a decomposition chapter.

A.9 `population-age-structure-momentum` has both problems and no chapter yet.

### 8. Endpoint tests on non-monotone exposures

A start-to-end difference summarizes a *monotone* series. Over a window containing a hump it nets the
rise against the fall and reports "no movement" about an exposure that moved a great deal. C.6.a's
first sign test returned **0 of 18 countries consistent** for 1965–2024; splitting the window gave
**14 of 18 for 1965–80** and **0 of 18 for 1980–**. Same data — the second reading locates the failure
instead of asserting it. Any cyclical exposure needs peak year, amplitude and net/amplitude reported
beside the endpoint difference, with the split derived from a source outside the data.

### 9. Pooling rules are currently chapter-local, and the outcome level is not fixed

Three rulings have been made inside chapters that should either be promoted to the protocol or
explicitly scoped as local:

- **Stratify before applying the ≥3 test.** A hazard ratio beside a mean is not a pool (A.23).
- **Resolve disagreements, do not average.** A.12 had four studies on a biased estimator and one
  corrected; the pooled mean is not a compromise between them.
- **Never pool across outcome levels.** Inside a single C.3.e RCT, realized fertility is null and
  stated desires are +0.4. A chapter that pools them reports a number no other chapter's number is
  comparable to.

`decisions/2026-07-11-oas-conservative-pooling-rule.md` is the existing precedent and is written for
one chapter.

### 10. The shares will sum past 1, and the double-counting is structural

Every chapter estimates a **total effect**, in a literature that did not condition on the other
sixty-nine hypotheses. Where A operates through B, both literatures report a real effect and **both
chapters correctly claim the same share of the decline**. No single study contains both, so nothing
inside a chapter can detect it. This is not a defect in any chapter and it will not be fixed by
grading them more carefully.

It is squarely our situation: C.2.b (direct costs), C.2.c (housing) and C.3.e (credit constraints)
are not independent mechanisms, and D.1.a (postmaterialism) is plausibly upstream of much of category
C. When the cross-chapter table in item 12 is built, the shares in a column will sum well past 1 for
reasons having nothing to do with any chapter being wrong.

Two things follow.

**A partial order over blocks is a precondition for any ranked output.** Not a DAG over hypotheses —
a seventy-node diagram is not credible to a reader or to us. Tiers over the eight-to-twelve
conceptual families, with within-tier ordering left undirected where we cannot defend it, and credit
propagating forward across tiers only. The A/B/C/D categories plus
`decisions/2026-06-14-proximate-vs-root-cause-categories.md` are already a first draft of exactly this
partial order; formalizing it is cheap.

**The excess over 1 is itself reportable.** A column summing to 3.4 says the mechanisms share most of
their explanatory content, *or* the literatures are inflated, *or* the estimands are not comparable.
For a generic analyst those are indistinguishable. We can partly separate them — the GRADE column
speaks to inflation, the extraction tables to comparability, a block tiering to overlap — and
attributing the excess across the three is reachable **without solving the decomposition problem at
all**. Treat it as a candidate headline result rather than an embarrassment to be normalized away.

### 11. A ranked output invites winner's curse, and nothing currently guards against it

Publication bias distorts a **ranking** far more than it distorts any single estimate. Whichever
hypothesis tops the table is disproportionately the one whose literature is most inflated, and
inflation is worst in small literatures on novel treatments — precisely the ones that will look most
surprising and most quotable when they rank high.

Two guards, and the second matters more:

- A bias correction per chapter where the pool supports one (selection models or RoBMA in preference
  to PET-PEESE, which over-corrects under high heterogeneity).
- **Partial pooling across chapters** — treat the per-chapter estimates as draws from a common
  distribution and shrink. Shrinkage buys much more for ranking than for estimation; the hospital-
  and school-ranking literature found this repeatedly.

And the reporting consequence: with per-chapter standard errors and τ², a point-estimate ordering is
mostly noise past the top few. The defensible output is **a tier list with the pairwise comparisons
that survive**, not an ordered list. Note that the network-meta-analysis vocabulary for this (SUCRA,
rankograms) assumes every arm has an estimate — several of ours have **none** (A.23, A.24), so one
tier of our list is `UNEVALUATED` and is a different object from a noisy rank.

### 12. The comparison object does not exist yet

There is no cross-chapter table. Verdicts live in per-chapter CSVs in `output/tables/` with
per-chapter column sets, so the review's headline claim — this explanation carries more of the decline
than that one — cannot currently be read off anything. When it is built it must be **generated from
the computed per-chapter outputs, never hand-entered**: A.17's hand-typed demsig table had the right
offsets against the wrong baselines, and nothing caught it but a re-derivation.

### What this costs

Items 2, 4, 5 and 6 are retroactive. A sign condition on the R² route changes at least C.6.a's SDT
cell; a spurious-regression restriction changes every chapter that used route 3 on an undifferenced
series; new GRADE bands change at least A.23 and A.18, and probably A.9 and A.12 when they are
re-read. The ticket is not done when the protocol is amended — it is done when the affected drafted
chapters have been re-graded, or the re-grade is scheduled with a named list.

Items 10 and 11 are **not** retroactive to any chapter. They are conditions on an artifact that does
not exist yet, and both must be settled before it is built rather than after.

### Reading

Four references worth having before starting, none of which needs to be re-derived:

- **Heskes, Sijben, Bucur & Claassen (2020), "Causal Shapley values."** Replaces the conditional
  expectations in a Shapley decomposition with interventional ones, so credit propagates to
  descendants of an intervention but not to its ancestors. The transportable idea for item 10 is not
  the numerical machinery — which needs a joint distribution over treatments that seventy separate
  literatures cannot supply — but the **causal chain graph**: tiers with an ordering only *between*
  components, and symmetric treatment within them. That is the item-10 proposal.
- **Frye, Rowat & Feige (2020), "Asymmetric Shapley values."** The neighbouring approach: keep
  conditional expectations, restrict the permutation average to orderings consistent with the causal
  structure. Pushes more credit to root causes. Worth knowing which of the two a tiering implements.
- **Cheung & Chan, two-stage meta-analytic SEM (MASEM).** The established answer to "I have effects
  from disconnected literatures and need the overlap structure": pool a *correlation matrix* across
  studies, then decompose that. The obstacle at our scale is coverage — a 71×71 matrix needs 2,485
  pairwise correlations — and worse for us, our chapters extract heterogeneous causal estimands from
  IV, DiD and RD designs that share no common covariance matrix. **Check whether even one block has
  the pairwise coverage before committing to this route.** The realistic alternative is to borrow the
  covariance structure from a country-year macro panel (HFD/WPP/Maddison) while keeping the
  meta-analytic estimates for magnitudes — which first requires that `data/raw/` actually be built.
- **The hospital- and school-ranking shrinkage literature**, for item 11: raw rankings are dominated
  by noise and shrunk rankings are dramatically more stable.

## Acceptance criteria
- [ ] A `decisions/` entry recording each ruling, the evidence that forced it, and what it costs
- [ ] §4.2 amended: a **sign condition** on the R² route, and a stated rule for what happens when the
      three routes disagree (precedence, conjunction, an explicit disagreement verdict, or demotion)
- [ ] §4.2 states that routes 1 and 2 decompose a mean change and route 3 a variance, and rules on
      whether route 3 certifies at FDT and SDT at all or only at PM
- [ ] §4.2 amended: **which** R² the 0.15 threshold applies to, and the control set that makes it
      "conditional"
- [ ] The spurious-regression guard decided and written in: differencing/detrending requirement, a
      revised threshold, or demotion — with the reasoning recorded, since 0.15 is below the level two
      independent random walks reach
- [ ] §4.1 gains bands for the empty cell (**UNEVALUATED**) and the non-effect estimand
      (**NOT RATEABLE**), each with the sentence the chapter must print beside it
- [ ] §4.2.1's PM cell states what a variance share is allowed to be divided by, and requires the
      near-definitional caveat where the number is printed
- [ ] The non-monotone-exposure reporting requirement written into `docs/chapter-template.md`
- [ ] The three pooling rulings either promoted to PROTOCOL §5 or explicitly recorded as chapter-local
- [ ] A **partial order over hypothesis blocks** committed to the repo — eight to twelve families,
      tiers only, within-tier ordering left undirected where undefended — with the rule that a share
      may not be claimed by two chapters in different tiers without a note saying which is upstream
- [ ] The protocol says what to do when a column's shares sum past 1, including the option of
      reporting the excess and its attribution as a result
- [ ] A shrinkage/partial-pooling step specified for any ranked output, and the ranked output
      specified as a tier list with surviving pairwise comparisons rather than an ordered list
- [ ] A generator emitting `output/tables/cross-chapter-verdicts.csv` from per-chapter computed
      outputs, with no hand-entered cell, and a check that fails if a chapter's inputs are missing
- [ ] The re-grade list: which drafted chapters change under the rulings above, and by how much
- [ ] C.6.a's PI Call 3 closed here rather than in that chapter

## Log
