# Screen rubric — A.6 reduction in stigma around contraception and abortion

**Hypothesis:** A.6, slug `stigma-reduction-contraception-abortion`, HYPOTHESES-v5.md §A.6
**Ticket:** TICK-087 · branch `087-stigma-reduction-contraception-abortion`
**Authority:** this rubric implements the scope doc
(`stigma-reduction-contraception-abortion-search-scope.md`) §§2, 9, 10 and 12. Where the two
disagree the scope doc wins and this file is wrong and must be fixed.
**Status:** v1, 2026-09-17.

## What this screen is trying to settle

Four independent channels predict that `PRIMARY_NORM_FERTILITY` is empty (scope §15). **The screen's
job is therefore to establish that emptiness properly, not to find a result.** A screen aimed at
confirming an absence has a different failure mode from one aimed at finding studies: the danger is
not missing a paper, it is *concluding absence without having looked where the paper would be*. The
stratification in `410` is built for exactly that — it routes agent reading to the records that
would contain a primary-cell study if one existed, and it must be exhaustive there rather than
sampled.

A record is never excluded because it is unlikely to be a primary-cell study. It is excluded only on
what it *is*.

## The two rulings this rubric enforces

**Ruling 1 (exposure).** A.6 owns variation in the **social price** of using a method, holding
market price, legality and programme supply fixed. A record whose treatment is a technology arrival,
a law change, or a programme rollout is A.2, A.4 or A.5 — route, do not exclude.

**Ruling 2 (outcome).** A.6's parameter is **realized fertility**. Contraceptive use is a *link*, not
a substitute. This is the ruling that the frame could not enforce (scope §14), so the screen enforces
it through `outcome_level`. A record with a use outcome and no fertility outcome is
`LINK_NORM_USE` — real, retained, and not the chapter's parameter.

## Decision procedure

Apply in order. Stop at the first rule that fires.

1. **Object gate.** Is the record about contraception, abortion, family planning, birth control or
   sterilisation as the behaviour at issue? If no → `OFF_OTHER`.
2. **Homonym gate.** Is the stigma at issue attached to something other than fertility control —
   HIV status, mental illness, obesity, infertility, leprosy? If yes → `OFF_HIV_STIGMA` (for HIV and
   STI) or `OFF_OTHER_STIGMA`. Scope §8 measured these at 148 and 92 records inside the frame, so
   this gate fires often and must not be skipped.
3. **Clinical-sense gate.** Does "abortion" mean *spontaneous* loss, miscarriage or stillbirth? If
   yes → `OFF_CLINICAL_LOSS` (the B.5 boundary).
4. **Exposure gate.** Is the exposure a normative or social-cost construct — stigma, taboo,
   disapproval, opposition, acceptability, legitimation, shame, secrecy, religious objection,
   partner or community disapproval? If no → `OFF_OTHER`.
5. **Bundling check (ruling 1).** Does the exposure vary *together with* technology, law or
   programme supply, with no separate dose on the norm component? If yes → `MIXED_NORM_TECH`,
   `MIXED_NORM_LAW` or `MIXED_NORM_SUPPLY` as appropriate. Also `MIXED_NORM_DIFFUSION` (A.3, where
   the exposure is the *arrival* of the idea) and `MIXED_NORM_SECULAR` (D.1.a, where it is a change
   in values rather than in what can be seen being done).
6. **Estimation check.** Does the record *estimate an effect*, as against measuring, describing,
   theorising or advocating? Scale-construction and validation papers, conceptual frameworks,
   prevalence studies, qualitative accounts and policy documents → `CONTEXT_STIGMA_MEASURE`.
7. **Outcome check (ruling 2).** Outcome is realized fertility → `PRIMARY_NORM_FERTILITY`. Outcome
   is contraceptive or abortion use, uptake, continuation or unmet need → `LINK_NORM_USE`. Outcome
   is the use-to-fertility conversion itself → `LINK_USE_FERTILITY`.
8. **Fall-through.** Anything reaching here without a cell is `INSUFFICIENT_INFO`, **not**
   `OFF_OTHER`. An unreadable title with no abstract is missing information, not an exclusion. These
   are re-screened at full text.

`INSUFFICIENT_INFO` is expected to be large in the degree-1 strata, where many records have no
abstract in the index (`410` counts them). A thin cell may be an unscreened cell
(`a-thin-cell-may-be-an-unscreened-cell`).

If a real class of record has no cell here, **add a cell and re-run this rubric over every completed
batch** rather than forcing it into `OFF_OTHER` (`add-a-cell-when-the-rubric-lacks-one`). Record the
addition in the batch log with the batch number at which it was added.

## Cells

Verbatim from scope §9. `primary` is one cell only.

| cell | role |
|---|---|
| `PRIMARY_NORM_FERTILITY` | **primary** |
| `LINK_NORM_USE` | link evidence (L1) |
| `LINK_USE_FERTILITY` | context — cited, never re-estimated here |
| `CONTEXT_STIGMA_MEASURE` | context |
| `MIXED_NORM_TECH` · `MIXED_NORM_DIFFUSION` · `MIXED_NORM_LAW` · `MIXED_NORM_SUPPLY` · `MIXED_NORM_SECULAR` | route-out, with a note |
| `OFF_CLINICAL_LOSS` · `OFF_HIV_STIGMA` · `OFF_OTHER_STIGMA` · `OFF_OTHER` | off-cell |
| `INSUFFICIENT_INFO` | unresolved, re-screen at full text |

## Tags recorded at screen

From scope §10. Screen-stage values are **hypotheses, not properties**, and are re-read at full text
(`design-is-not-a-property-of-the-title`).

| tag | values |
|---|---|
| `outcome_level` | `REALIZED` · `INTENDED` · `DESIRED` · `USE` · `STATED_ATTITUDE` · `NONE` |
| `dose_unit` | `REPORTED` (in §5's opposition-share unit) · `DERIVABLE` · `NONE` |
| `phenomenon_window` | `FDT` · `SDT` · `BOTH` · `NEITHER` |
| `estimator_class` | `IV` · `DID` · `RDD` · `RCT` · `EVENT_STUDY` · `SYNTH` · `OLS_ADJUSTED` · `DESCRIPTIVE` · `QUALITATIVE` · `SIMULATION` · `OTHER_LOUD` |
| `stigma_object` | `CONTRACEPTION` · `ABORTION` · `FAMILY_PLANNING` · `MIXED` |
| `stigma_bearer` | `SELF` · `PARTNER` · `COMMUNITY` · `PROVIDER` · `INSTITUTIONAL` |

`estimator_class` falls through **loudly**: a design that matches none of these is `OTHER_LOUD` with
a free-text note, never silently `DESCRIPTIVE` (`estimator-class-list-is-a-gate`).

## What counts as "estimates an effect" (rule 6)

This is the rule that will decide most of this pool, so it is spelled out. A record estimates an
effect if it reports a quantitative relationship between a norm/social-cost exposure and an outcome,
with some attempt at identification or adjustment. It does **not** estimate an effect if it:

- constructs or validates a stigma scale (however quantitative);
- reports the prevalence of stigma, or of opposition as a reason for non-use, without relating it to
  an outcome across units;
- describes women's experiences, however systematically;
- proposes a framework, typology or research agenda;
- is a policy document, declaration, editorial or commentary;
- is a textbook, handbook or review that reports no new estimate.

A cross-sectional regression of use on a stigma score **does** estimate an effect and is
`LINK_NORM_USE` with `estimator_class: OLS_ADJUSTED` — admissible as link evidence, and its
identification weakness is risk-of-bias's problem, not the screen's.

## Second-reader rule

PROTOCOL §5.1 step 6 requires RA spot-checks of 5–10%. For this chapter the spot-check is **not** a
random 5–10%: it is **100% of every record assigned `PRIMARY_NORM_FERTILITY`, plus 100% of
`INSUFFICIENT_INFO` in the identified-design strata, plus a random 10% of everything else.** The
asymmetry is deliberate. The chapter's conclusion is an absence, so the costly error is a
false-negative on the primary cell, and the primary cell is expected to be small enough that
exhaustive second reading is cheap.

## Batch logging

Each batch appends to `stigma-reduction-contraception-abortion-screen-log.md`: batch id, stratum,
n, cell tally, any cell added mid-screen, and every `PRIMARY_NORM_FERTILITY` or borderline call with
a one-line reason. Decisions go to
`extraction/stigma-reduction-contraception-abortion-screened.csv`, one row per record.
