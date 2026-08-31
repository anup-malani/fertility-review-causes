# A.18 title/abstract screen — interim report, stratum A complete

**TICK-076, 2026-08-31.** Batches 1–3 of 43 screened: **165 records**, the whole of stratum A
(the 317 survivors the citation channel also reached) plus the first of stratum B.

## Yield, and why the stratification was worth building

| stratum | screened | RELEVANT | yield |
|---|---|---|---|
| A — citation intersect | 165 | 88 | **53.3%** |
| C — boolean-only tail (§17 blinded sample) | 136 | 1 | **0.7%** |

A **76× difference**. The citation channel and the boolean channel disagree about where the evidence
is, and the citation channel is right. This is the quantitative case for `label-by-provenance-not-
vocabulary` on this hypothesis, and it is why §17 declined to screen the tail exhaustively.

## The screen audits itself against hidden gold

34 of the 165 records were gold, unmarked in the batches. The screen returned **31 RELEVANT, 1
UNCERTAIN, 2 NOT_RELEVANT — sensitivity 91.2%, or 94.1% counting UNCERTAIN.**

Both "misses" were read back, and at least one indicts the gold rather than the screen:

- *Partner + Children = Happiness?* — a within-MZ twin study whose **outcome is well-being and whose
  exposure is fertility**. Rejecting it is correct for A.18; it is in the gold set only because the
  proxy gold was built on a fertility word in the title. Same failure the §15 recall audit found at
  scale.
- *Relational Aggression and Lifetime Offspring* — predictor is a behavioural disposition, not a
  genetic measure. Wall 3. Defensible, and flagged for the RA gate rather than settled here.

## What the screen found, by cell

| cell | n | |
|---|---|---|
| `H2_FERTILITY` | 26 | conjunct 1 — well populated |
| `SELECTION_DIFFERENTIAL` | 22 | conjunct 2 |
| `H2_MODERATION` | 7 | **the arm the registered claim does not contain** |
| `PREDICTED_RESPONSE` | 4 | **the only cell that can carry a demsig number** |
| `PEDIGREE_RESPONSE` | 3 | the identified historical designs (Ruling 2) |
| `WITHIN_VS_POPULATION` | 1 | the bias-magnitude record |
| | **63** | primary-synthesis total |

Plus 23 `THEORY`/`METHOD` and 7 `LINK_TRAIT` (Wall 4), 41 routed to B.1 as `OFF_STATUS_B1`, 8
`OFF_SPECIES`, and 22 `UNCERTAIN`.

**Two things follow, and both were predicted by the scope but are now measured.**

*The moderation arm is real.* Seven records — Udry 1996, Kohler et al. 2002, Nisén, a
*Genotype × Cohort Interaction* study, a Norwegian *Influence of Societal Changes on the Contribution
of Genetics to Fertility Behavior*, and two demographic-transition-and-selection papers. §4 argued
this arm exists and runs the causal arrow backwards; it does, and it is not a footnote.

*The demsig-bearing cell is the thinnest.* Ruling 1 put demographic significance on the selection
**response**, and `PREDICTED_RESPONSE` has 4 records against `H2_FERTILITY`'s 26. The well-evidenced
half of the claim is the demographically inert half — exactly the asymmetry §3 predicted, now with
counts attached.

## The exposure-distance check (the A.24 lesson)

| `exposure_distance` | n |
|---|---|
| `ANONYMOUS_VARIANCE` (twin h², no variant named) | 43 |
| `NOT_GENETIC` (theory/method records) | 23 |
| `OTHER_CORRELATED_PGS` | 13 |
| **`FERTILITY_PGS`** | **9** |

**Nine records of 88 measure a genotype associated with fertility itself.** Thirteen measure selection
on a *correlated* trait — education, psychiatric liability, cognition. That is Ruling 3's entire
reason for existing, and it is now a table rather than an expectation: the conversion from a
correlated-trait selection differential to children per woman is doing more work in this literature
than any single study does.

`decomposes` among RELEVANT: **yes 80, cannot_tell 8, no 0** — Wall 1 is rejecting at the screen, as
designed.

## Not yet done

Batches 4–43 (stratum B, the boolean relevance head) remain. Stratum C is not batched and is bounded
at ≈213 relevant records (95% CI 37–1,176) by §17.
