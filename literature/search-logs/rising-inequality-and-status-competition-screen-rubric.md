# C.2.f title/abstract screen — rubric

**Hypothesis:** C.2.f `rising-inequality-and-status-competition` · **Ticket:** TICK-081 ·
**Frozen:** 2026-09-08, before any record was screened.

Applies to `rising-inequality-and-status-competition-screen-universe.json` (script 340, 1,366
records). The gold key is withheld in `...-screen-gold.json` and merged only when scoring
sensitivity. **313 records (23%) carry no abstract**; those are screened on title alone and tagged
`title_only = true`, because a title-only judgement is a weaker judgement and must be visible as one
(`design-is-not-a-property-of-the-title`).

---

## 0. The one question that decides admissibility

> **Did something move the DISPERSION of the income distribution the household faces, or the
> investment required to hold a given relative position — for a reason other than the household's own
> income, and separably from the RETURN to child human capital?**

Scope §2 is the whole chapter. C.2.f and C.3.d predict the same reduced form from different
primitives, and in the canonical models they move together: skill-biased technical change raises the
return to child human capital (C.3.d's variation) **and** raises dispersion (C.2.f's) because they
are the same shock.

- **C.3.d owns the RETURN.** Investment rises because each unit of it is worth more.
- **C.2.f owns the REFERENCE STANDARD.** Investment rises because holding a given relative position
  now costs more, with the return unchanged.

The discriminating prediction is that investment responds to **dispersion holding the return fixed**,
and more strongly where allocation is explicitly rank-based. A study that varies SBTC exposure and
reads off fertility is **not this chapter's** unless it separates the two.

Admissibility is a property of the **variation**, never of the vocabulary. A paper titled *Income
Inequality and Fertility* that regresses TFR on a Gini series is `INEQ_ASSOCIATION`. A paper about a
private-tutoring ban that never says "inequality" may be `TUTORING_POLICY_FERTILITY`.

---

## 1. Route in this order — first match wins

1. **Is the outcome fertility?** Realized births, completed fertility, TFR, parity progression,
   timing of first birth, or stated intentions/desires. If the outcome is test scores, enrolment,
   consumption, wages, or investment itself → not this chapter's outcome. Tag `outcome_level = NONE`
   and route to `INEQ_INVESTMENT` if it is link 1, else out.
2. **Which direction does the arrow run?** If fertility (or assortative mating) is the CAUSE and
   inequality the outcome → `WRONG_DIRECTION`. Stop. Scope §8 Wall 9.
3. **Is the exposure a distribution statistic, or own income?** Own income, household income, an
   income shock or a windfall → **C.1.a**, not this chapter. If both move and cannot be separated →
   `MIXED_INEQ_INCOME`. Scope §8 Wall 4, the largest wall at 90 records.
4. **Is the return separable from the reference standard?** If the design varies the return to human
   capital → **C.3.d**. If both and inseparable → `MIXED_RETURN_POSITION`. Scope §8 Wall 1.
5. **Whose comparison group?** Against the **parental cohort's** standard → **C.6.a** (Easterlin,
   written; do not reopen). Against the **contemporaneous** distribution → C.2.f. Scope §8 Wall 2.
6. **Is it the norm or the price?** The norm defining what a proper child requires → **D.2.d**. The
   price of a required input → **C.2.b**. The required QUANTITY of investment rising with dispersion
   → C.2.f. Walls 3 and 6.
7. **Which cell** (§2), then **tag** (§3).

---

## 2. Cells

| cell | admit when | role |
|---|---|---|
| `DISPERSION_FERTILITY` | exogenous move in income dispersion → realized fertility, return held or measured | **primary** |
| `POSITIONAL_ALLOCATION_FERTILITY` | rank-based allocation intensity (exam-allocated places, class-rank admissions) → realized fertility | **primary** |
| `REQUIRED_INVESTMENT_FERTILITY` | required investment per child moves → realized fertility | **primary** |
| `TUTORING_POLICY_FERTILITY` | **a policy shock to required investment** — China 2021 "double reduction", Korea's 1980 ban and its lifting, tutoring regulation | **primary, and the cell most likely to hold an identified design** (scope §4A, §7 row 7) |
| `INEQ_INVESTMENT` | inequality → investment per child, **no fertility outcome** | link 1; supports the mechanism, **never a primary effect** |
| `MIXED_RETURN_POSITION` | return and dispersion move together, not separated | jointly claimed with C.3.d, unallocated |
| `MIXED_INEQ_INCOME` | dispersion and own income move together | jointly claimed with C.1.a, unallocated |
| `PERCEIVED_STATUS` | stated status or education pressure → intentions or desires | **separate outcome level; never pooled with realized** |
| `INEQ_ASSOCIATION` | area or period inequality vs fertility, no identified variation | context; **never primary, never pooled** |
| `WRONG_DIRECTION` | differential fertility or assortative mating → inequality | context only |
| `EDUCOMP_BOUNDARY` | shadow education / tutoring with a non-fertility outcome | scope §4A packet |
| `QQ_BOUNDARY` | the price or return of child *quality* is what moves | Wall 1 packet |
| `THEORY` | models of positional competition and fertility, no estimate | context |
| `OFF_OTHER` | none of the above | out |

`add-a-cell-when-the-rubric-lacks-one`: if a real class of record does not fit, **add the cell
mid-screen and re-run completed strata as code** rather than forcing it to `OFF_OTHER`. A thin cell
may be an unscreened cell — C.3.e's Arm S went 3 → 16 in one wave.

---

## 3. Tags — every admitted record

| tag | values |
|---|---|
| `exposure_statistic` | `GINI` · `TOP_SHARE` · `RATIO_90_10` · `DISPERSION_OTHER` · `POSITIONAL_INTENSITY` · `REQUIRED_INVESTMENT` · `PERCEIVED` |
| `exposure_level` | `NATIONAL` · `SUBNATIONAL` · `LOCAL_LABOR_MARKET` · `SCHOOL_DISTRICT` · `INDIVIDUAL_REFERENCE_GROUP` |
| **`return_separated`** | `YES` · `NO` · `UNCLEAR` · `NOT_APPLICABLE` — **Wall 1 made a data field** |
| **`own_income_held`** | `YES` · `NO` · `UNCLEAR` — **Wall 4 made a data field** |
| `link_measured` | `LINK1_INVESTMENT` · `LINK2_QUANTITY` · `FULL_CHAIN` |
| `outcome_level` | `REALIZED` · `INTENDED` · `DESIRED` · `NONE` |
| `design` | a **hypothesis, not a property** — re-read at full text (`design-is-not-a-property-of-the-title`) |
| `title_only` | `true` where the record carried no abstract |

**`return_separated` and `own_income_held` are screen-visible on purpose.** D.3.b's lesson is that a
wall the screen cannot see is a wall the screen cannot enforce, and Walls 1 and 4 are this chapter's
two largest. At title/abstract they will very often be `UNCLEAR`; **that is a legitimate value and
must not be coerced to `NO`.** The count of `UNCLEAR` is itself a finding about the literature, and
it sizes the full-text work.

---

## 4. What the screen must NOT do

- **Do not use the arm a record arrived on.** Batches are blinded of arm membership: the arm predicts
  the cell, so showing it makes the screen agree with the query rather than judge the record.
- **Do not treat `"income inequality"` in a title as evidence of this chapter's exposure.** Scope §3:
  that term carries 89% of the frame and most of it is not this mechanism.
- **Do not route a record out for lacking the word "positional".** Scope §4A: the full chain is
  written in the East Asian education-competition vocabulary, and probing it in
  economics-of-inequality vocabulary returned 2 records against 56.
- **Do not resolve `UNCLEAR` by guessing.** See §3.
- **Every emitted row comes back with a verdict**, including obvious excludes — hidden controls need a
  verdict on every row or sensitivity cannot be computed
  (`a-positives-only-screen-cannot-measure-sensitivity`).

---

## 5. Known clouds, measured, and what to do with each

| cloud | measured | action |
|---|---|---|
| behavioural-ecology "parental investment" (Trivers sense) | 31 of 143 free-seed hits | `OFF_OTHER` **unless** it carries a C.2.f exposure term — 9 records do (conspicuous-consumption signalling, sexual selection and growth) and those are boundary cases, not noise (`decoy-clouds-are-boundary-cases`) |
| C.3.d quantity-quality | 8 inside the frame | `QQ_BOUNDARY` |
| C.6.a Easterlin / relative income | 15 | route to C.6.a, written |
| C.1.a own income | 90 — the largest | `MIXED_INEQ_INCOME` or route to C.1.a |
| C.5.a uncertainty / unemployment | 70 | route to C.5.a |
| D.3.c despair / teen births (Kearney–Levine's headline) | 21 | route to D.3.c, drafted |
| gender-inequality homonym | 30, against a 2,281-record literature | `OFF_OTHER`, **no screen rule spent** — the exposure axis separates it |
| health / educational inequality as outcome | 8 | `OFF_OTHER` |
| wrong direction | 25 | `WRONG_DIRECTION` |
| `"involution"` / *neijuan* | 398, all veterinary/obstetric | never searched; if one arrives, `OFF_OTHER` |
