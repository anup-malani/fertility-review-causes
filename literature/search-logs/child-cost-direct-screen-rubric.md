# C.2.b title/abstract screen — rubric

**Hypothesis:** C.2.b `child-cost-direct` · **Ticket:** TICK-079 · **Frozen:** 2026-09-03, before any
record was screened.

Applies to `child-cost-direct-screen-universe.json` (built by script 321). The gold key is withheld
in `child-cost-direct-screen-gold.json` and merged only when scoring sensitivity.

---

## 0. The one question that decides admissibility

> **Did something move the PRICE a household faces for a child-specific good or service, for a reason
> other than that household's own fertility and investment choices?**

Scope §2: spending per child is quantity-chosen × price-faced, and fertility and quantity-per-child
are chosen together. A household with two children spends more per child than an identical household
with five, **with no price change anywhere**. So a record reporting that families who spend more per
child have fewer children has reported the budget constraint, not an effect.

Admissibility is therefore a property of the **variation**, never of the vocabulary. A paper titled
*The Cost of Children and Fertility* that regresses TFR on a cost-of-a-child series is
`EXPENDITURE_ASSOCIATION`. A paper about school uniform subsidies that never says "cost of children"
may be `SCHOOL_COST_FERTILITY`.

---

## 1. Route in this order — first match wins

1. **Is the outcome fertility?** Realized births, completed fertility, TFR, parity progression,
   timing of first birth, or stated intentions/desires. If the outcome is enrolment, learning,
   child health, maternal labour supply, or expenditure itself → not this chapter's outcome. Tag
   `outcome_level = NONE` and route out (but see cell `COST_SERIES_MEASUREMENT`).
2. **Is the exposure a price, or an expenditure?** Expenditure observed → `EXPENDITURE_ASSOCIATION`.
   Stop there; it is never primary and never pooled.
3. **Whose price is it?** Childcare → C.2.a. Housing → C.2.c. The mother's time → C.2.e.
   Net-of-transfer child benefit → C.2.d. Chosen investment level per child → C.3.d.
   Only what is left — schooling outlays, child health costs, child-specific goods — is C.2.b's.
4. **Which cell** (§2 below).
5. **Tag** (§3 below).

---

## 2. Cells

| cell | admit when | role |
|---|---|---|
| `PRICE_SHOCK_FERTILITY` | an exogenous move in the price of a child-specific good or service, outcome realized fertility | **primary** |
| `SCHOOL_COST_FERTILITY` | school fees or school-related outlays move, outcome realized fertility — **subject to the channel gate, §4** | **primary** |
| `CHILD_HEALTH_COST_FERTILITY` | the price of children's health care moves, outcome realized fertility | **primary** |
| `BIRTH_EVENT_COST` | maternity or delivery user fees — the price of a **birth**, not of a child (scope §16.3) | primary, reported separately, never pooled with `SCHOOLING` or `HEALTH` |
| `MIXED_PRICE_VALUE` | fees inseparable from forgone child labour (scope §6) | jointly claimed, unallocated |
| `MIXED_PRICE_TRANSFER` | gross price and a transfer move together (Wall 5) | jointly claimed, unallocated |
| `PERCEIVED_COST` | stated cost as a barrier → intentions or desires | **separate outcome level; never pooled with realized** |
| `PRICE_ASSOCIATION` | a **price** of children (constructed index, net price, cross-national cost level) regressed on fertility with **no exogenous variation** | context; not primary |
| `EXPENDITURE_ASSOCIATION` | expenditure per child vs fertility, no price variation | context; the §2 identity |
| `COST_SERIES_MEASUREMENT` | equivalence scales, cost-of-a-child accounting, price-index construction | exposure measurement, not an effect |
| `QQ_BOUNDARY` | the price of child *quality* or investment is what moves | Wall 1 packet |
| `TIMECOST_BOUNDARY` | career cost, child penalty, forgone earnings, time use | **Wall 4 packet — see §5** |
| `THEORY` | models of child price and fertility, no estimate | context |
| `OFF_OTHER` | none of the above | excluded |

If a real class of record fits none of these, **add a cell and re-check the completed batches as
code** rather than forcing it into `OFF_OTHER` (`add-a-cell-when-the-rubric-lacks-one`; C.6.a's
`BOOM_ALTERNATIVE` was added mid-screen this way).

---

## 3. Required tags on every admitted record

| tag | values |
|---|---|
| `exposure_type` | `PRICE_EXOGENOUS` · `PRICE_POLICY` · `EXPENDITURE_OBSERVED` · `PERCEIVED` |
| `exposure_distance` | `PRICE_MEASURED` · `PRICE_PROXIED` · `EXPENDITURE_ONLY` · `NOT_A_COST` |
| `exposure_direction` | `RISE` · `FALL` — scope §4: the hypothesis is about a rise and nearly every clean shock is a fall |
| `cost_component` | `SCHOOLING` · `HEALTH` · `GOODS` · `BIRTH_EVENT` · `TOTAL_BUNDLE` · `OTHER_CHAPTER` |
| `outcome_level` | `REALIZED` · `INTENDED` · `DESIRED` · `NONE` |
| `design` | a **hypothesis**, re-read at full text — `design-is-not-a-property-of-the-title` |
| `phenomenon_window` | `PM` · `FDT` · `SDT`, plus a transport note where setting and claimed phenomenon differ |
| `channel` | **school-fee records only** — see §4 |

---

## 4. The channel gate on school-fee records

Scope §16.2. Of the 24 school-fee records in the free-seed harvest, 8 carry a fertility outcome and
**6 name women's or girls' schooling in the title**. If a fee-abolition paper identifies through the
mother's own schooling, it is measuring an education effect that **lowers** fertility — the opposite
sign to the price effect C.2.b claims. Pooling it into `SCHOOL_COST_FERTILITY` would put a
wrong-signed education elasticity in the primary cell and call it a price elasticity.

Every record entering `SCHOOL_COST_FERTILITY` is tagged:

- `PRICE_OF_CHILD` — the paper's own stated channel is the household's cost of a child. **Admit.**
- `MATERNAL_SCHOOLING` — the channel is the mother's own education or years of schooling.
  **Route out** to the schooling literature.
- `BOTH_UNSEPARATED` — both are present and the paper does not separate them. **Jointly claimed,
  unallocated.**

At title/abstract this tag is a *hypothesis*; it is confirmed at full text. **A cell populated mostly
by `MATERNAL_SCHOOLING` is reported as an EMPTY primary cell in those words**
(`empty-cell-is-the-result`) — not as weak evidence.

---

## 5. The Wall 4 vocabulary trap

Scope §16.1. "Cost of children" is the shared phrase of this chapter and of C.2.e's time-cost /
child-penalty literature: 17 of 130 harvested records were the latter, including **5 of the 6**
returned by "cost of childbearing". A screener reading only the exposure phrase will admit them.

**Test:** ask what the household gives up. Money spent on the child → C.2.b. Earnings, hours or
career the parent forgoes → `TIMECOST_BOUNDARY`, C.2.e's. *The Career Costs of Children* is titled in
C.2.b's vocabulary and belongs to C.2.e.

---

## 6. Screening discipline

- **Every row gets a verdict.** No row may be skipped, including obvious excludes: hidden controls
  need a verdict on every row or sensitivity cannot be computed
  (`a-positives-only-screen-cannot-measure-sensitivity`).
- **Blinded.** The universe carries no gold flags. Do not consult the gold file while screening.
- **`INSUFFICIENT_INFO` is a verdict**, used when the abstract is missing or silent on the
  discriminating fact. It is not an exclusion, and the count is reported. Records flagged as having
  no abstract are expected to concentrate here.
- **Screen notes are load-bearing.** Band and priority rules key on the note first, not on the cell
  (`band-rules-must-read-screen-notes`: cell-keyed P0 buried the only identified estimate in P3).
- **Probe depth, don't screen sequentially.** Spaced part-batches map the yield curve for the cost of
  two (`probe-depth-dont-screen-sequentially`).
- **Spot-check 5–10% by a second reader**, stratified on the flags that matter — `channel`,
  `exposure_direction`, and the no-abstract flag — not on a uniform random draw
  (`safeguards-must-be-measured-not-trusted`).

---

## 7. Amendment — 2026-09-03, `PRICE_ASSOCIATION` added mid-screen

Batch `rest-00` produced a class the rubric had no cell for: a study using a **price** of children —
Ermisch's net price of a child, cross-national child-cost levels, Japan's aggregate cost-of-children
index — regressed on fertility with **no exogenous variation** in it.

§1 step 2 routes on price-vs-expenditure, so these clear it. But `PRICE_SHOCK_FERTILITY` requires an
exogenous move, which they do not have, and `EXPENDITURE_ASSOCIATION` is specifically the §2 budget
identity, which they are not: a constructed price index is not the same object as observed spending
per child, and collapsing them would hide the distinction the chapter turns on.

They are added as `PRICE_ASSOCIATION` rather than forced into `OFF_OTHER`
(`add-a-cell-when-the-rubric-lacks-one`; C.6.a's `BOOM_ALTERNATIVE` was added the same way). It is
**context, never primary**: the exposure is right and the identification is absent, so these records
speak to whether the mechanism's vocabulary is used, not to whether the mechanism works.

**Completed batches were re-checked as code against the new cell**, not left as they were.
