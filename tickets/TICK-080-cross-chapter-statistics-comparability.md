# TICK-080: Cross-chapter statistics — comparability, the demsig routes, and the sign-blind R²
**Status:** open
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
run so far have surfaced eight specific ways it fails. They are itemized below with the evidence that
produced them; each is a question for the PI, not a defect with an obvious fix.

### 1. The three demsig routes are OR'd, and they can contradict each other

§4.2 makes a hypothesis demographically significant if **any one** of decomposition share ≥ 10%,
slope sufficiency = "sufficient", or conditional R² ≥ 0.15 clears. The routes are not
interchangeable, they are not equally strong, and on at least one chapter they disagree in opposite
directions. On C.6.a (Easterlin), the R² route certifies the hypothesis while the slope route refutes
it — the exposure moved the *wrong way* across the SDT window. Read literally, the OR gives C.6.a a
`significant` cell.

The protocol needs either a precedence order, a conjunction, or an explicit "routes disagree" verdict
that is not silently resolved by whichever route happens to be computable in that chapter.

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

Worse, the within-country time-series version is close to automatic: TFR trends down over the SDT
window, and any exposure that also trends will clear 0.15 on shared trend alone. A threshold that a
mechanism passes by being non-constant is not discriminating between hypotheses, which is the only
job it has here.

### 4. GRADE has no band for an empty cell

A.23's registered cell held 38 screened records, **two extracted effects and zero identified
designs**, and neither effect estimated the registered exposure on fertility. `VERY LOW` is the only
available rating and it is actively misleading: a reader takes it for a badly identified body of
evidence rather than an absent one, and those imply different next steps — read more carefully versus
run a study that does not exist. Proposed value: **UNEVALUATED**, with a mandatory sentence beside it.

### 5. GRADE has no band for a non-effect estimand

§4.1's bands are identification strategies. A competent twin design estimating a variance component
falls to "Very low: correlational only", which reads as *badly identified* when the truth is
*different question, answered well*. A.18 hit this on every arm. Proposed value: **NOT RATEABLE —
non-effect estimand**.

### 6. Variance components, denominators, and what PM's "range" admits

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

### 7. Endpoint tests on non-monotone exposures

A start-to-end difference summarizes a *monotone* series. Over a window containing a hump it nets the
rise against the fall and reports "no movement" about an exposure that moved a great deal. C.6.a's
first sign test returned **0 of 18 countries consistent** for 1965–2024; splitting the window gave
**14 of 18 for 1965–80** and **0 of 18 for 1980–**. Same data — the second reading locates the failure
instead of asserting it. Any cyclical exposure needs peak year, amplitude and net/amplitude reported
beside the endpoint difference, with the split derived from a source outside the data.

### 8. Pooling rules are currently chapter-local, and the outcome level is not fixed

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

### 9. The comparison object does not exist yet

There is no cross-chapter table. Verdicts live in per-chapter CSVs in `output/tables/` with
per-chapter column sets, so the review's headline claim — this explanation carries more of the decline
than that one — cannot currently be read off anything. When it is built it must be **generated from
the computed per-chapter outputs, never hand-entered**: A.17's hand-typed demsig table had the right
offsets against the wrong baselines, and nothing caught it but a re-derivation.

### What this costs

Items 2, 4 and 5 are retroactive. A sign condition on the R² route changes at least C.6.a's SDT cell;
new GRADE bands change at least A.23 and A.18, and probably A.9 and A.12 when they are re-read. The
ticket is not done when the protocol is amended — it is done when the affected drafted chapters have
been re-graded, or the re-grade is scheduled with a named list.

## Acceptance criteria
- [ ] A `decisions/` entry recording each ruling, the evidence that forced it, and what it costs
- [ ] §4.2 amended: a **sign condition** on the R² route, and a stated rule for what happens when the
      three routes disagree (precedence, conjunction, or an explicit disagreement verdict)
- [ ] §4.2 amended: **which** R² the 0.15 threshold applies to, and the control set that makes it
      "conditional" — plus whatever guard is decided for shared-trend inflation
- [ ] §4.1 gains bands for the empty cell (**UNEVALUATED**) and the non-effect estimand
      (**NOT RATEABLE**), each with the sentence the chapter must print beside it
- [ ] §4.2.1's PM cell states what a variance share is allowed to be divided by, and requires the
      near-definitional caveat where the number is printed
- [ ] The non-monotone-exposure reporting requirement written into `docs/chapter-template.md`
- [ ] The three pooling rulings either promoted to PROTOCOL §5 or explicitly recorded as chapter-local
- [ ] A generator emitting `output/tables/cross-chapter-verdicts.csv` from per-chapter computed
      outputs, with no hand-entered cell, and a check that fails if a chapter's inputs are missing
- [ ] The re-grade list: which drafted chapters change under the rulings above, and by how much
- [ ] C.6.a's PI Call 3 closed here rather than in that chapter

## Log
