# C.3.d title/abstract screening rubric

**Hypothesis:** C.3.d `quantity-quality-tradeoff` · **Ticket:** TICK-083 · **Frozen:** 2026-09-09
**Scope:** `quantity-quality-tradeoff-search-scope.md` — cells are §9, tags are §10, walls are §8.

Every emitted row gets a verdict, **including the obvious excludes**. Hidden controls are mixed into
these batches and sensitivity cannot be computed from a positives-only pass
(`a-positives-only-screen-cannot-measure-sensitivity`).

---

## 0. What this screen can and cannot decide

It decides **routing**: which estimand cell a record provisionally belongs to. It does **not**
adjudicate the walls. Scope §8's walls 1, 2 and 4 turn on which *primitive* the design varies —
the return vs the reference standard, the child's return vs the parent's, the return vs own income —
and none of that is reliably visible in a title and abstract. D.3.b established the general point:
a title/abstract screen cannot enforce a wall whose content is invisible to it. So:

- **Flag wall risk, do not resolve it.** `wall_risk` is a list, and a record can carry several.
- **`design` values are hypotheses, not properties.** A.23 carried a paper as an administrative
  allocation through search, screen *and* priority retrieval, and it was IPTW
  (`design-is-not-a-property-of-the-title`). Every value is re-read at full text.
- **21% of rows have no abstract.** A title-only judgement is a weaker judgement and must be visible
  as one: set `title_only: true` and prefer `UNCLEAR` over a confident cell.

---

## 1. The first question is DIRECTION, and it decides everything after it

This is scope §2, the ruling the chapter turns on. Ask **what is on the left-hand side**:

| | exposure | outcome | direction |
|---|---|---|---|
| **FORWARD** | something that moves the **return to child human capital** | **fertility** / births / family size | `FORWARD` |
| **BACKWARD** | **family size** (or a shock to it: twins, sex composition) | **children's** schooling, attainment, test scores, health, investment received | `BACKWARD` |

Both are called "the quantity-quality tradeoff" in ordinary speech. Only FORWARD answers the
registered claim. **A record can be BACKWARD and still be in scope** — it is link 2, mechanism
evidence, in cell `QQ_SUBSTITUTION`. It is never pooled with a forward effect and never carries a
demographic-significance number.

If the abstract estimates **both** directions, set `direction: BOTH` and say so in the note — a
single design spanning the boundary is worth more than any cross-literature count
(`one-study-can-carry-the-structure`).

---

## 2. Cells

| cell | route here when | role |
|---|---|---|
| `RETURN_FERTILITY` | an exogenous move in the **return** to child human capital (skill premium, returns to schooling) → **fertility** | **PRIMARY** |
| `SHOCK_FERTILITY` | a trade / technology / schooling-supply / industrialization shock → **fertility**, with the return measured or argued as the channel | **PRIMARY** |
| `QQ_SUBSTITUTION` | exogenous **family size** → investment or attainment **per child** | link 2, mechanism evidence |
| `MIXED_RETURN_POSITION` | the return and the **reference standard** move together and are not separated (Wall 1, C.2.f) | unallocated, jointly claimed |
| `MIXED_CHILD_PARENT_RETURN` | the **child's** and the **parent's** returns move together (Wall 2, C.2.e) | unallocated, jointly claimed |
| `MIXED_RETURN_INCOME` | the return and **own income** move together (Wall 4, C.1.a) | unallocated, jointly claimed |
| `RETURN_ASSOCIATION` | a returns series against a fertility series, **no identified variation** | context; never primary, never pooled |
| `PERCEIVED_RETURN` | **elicited beliefs** about returns → intentions or desires | separate outcome level; never pooled with realized |
| `THEORY` | a model — unified growth, calibrated OLG, pure theory with no estimate | context only (§13 call 4) |
| `OFF_TOPIC` | not about fertility, child investment or child outcomes at all | excluded |
| `OFF_OTHER` | on topic but another chapter's estimand outright (name it in `note`) | excluded, routed |
| `UNCLEAR` | cannot tell from what is shown | **needs full text**, not a rejection |

`add-a-cell-when-the-rubric-lacks-one`: if a real class of record fits none of these, **add the
cell** and re-run completed strata as code rather than forcing it into `OFF_OTHER`.

---

## 3. Wall risk flags — record, do not adjudicate

| flag | when the abstract suggests it |
|---|---|
| `W1_POSITION` | status competition, relative standing, positional concerns, educational arms race |
| `W2_PARENT_RETURN` | **the exposure is the mother's / women's / parents' own schooling or wage** |
| `W4_INCOME` | the shock plainly moves household income as well as the return |
| `W5_A12_TWINNING` | twinning as the *exposure* on aggregate births, rather than as an instrument |
| `W6_MORTALITY` | child mortality / survival is the moving part |
| `W7_SCHOOLING_LAW` | a compulsory-schooling or child-labour law (Alexandra's chapter shares these) |

**`W2_PARENT_RETURN` is the one to be liberal with.** 350 already found it on 5 of 26 resolved
fertility-outcome controls, and that count needed the parent *named in the title*, so it is a floor.
Scope §7 row 3 — schooling supply, the largest forward row — moves both returns almost by
construction.

---

## 4. Fields to return, one row per record

```
screen_id, direction, cell, design, wall_risk, outcome_object, title_only, confidence, note
```

- `direction`: `FORWARD` · `BACKWARD` · `BOTH` · `NA`
- `design`: `RCT` · `IV` · `DID` · `RDD` · `EVENT_STUDY` · `NATURAL_EXPERIMENT` · `PANEL_FE` ·
  `CROSS_SECTION` · `CALIBRATION` · `DESCRIPTIVE` · `REVIEW` · `UNCLEAR` — **a hypothesis, re-read
  at full text**
- `outcome_object`: `FERTILITY` · `INVESTMENT_PER_CHILD` · `CHILD_ATTAINMENT` · `OTHER` · `NA`
- `confidence`: `HIGH` · `MED` · `LOW`
- `note`: one line. **Say what varies and what is measured**, not what the title is about. Where a
  record is routed out, name the chapter it goes to.

---

## 5. Decision order

1. Is it about human fertility, child investment or child outcomes at all? If not → `OFF_TOPIC`.
2. Is it a model with no estimate? → `THEORY`.
3. What is the **outcome**? Fertility → forward family. Child outcomes → `QQ_SUBSTITUTION`.
4. What **varies**, and is it separable from the reference standard (W1), the parent's return (W2),
   and own income (W4)? Not separable and central → the matching `MIXED_*` cell. Separable → the
   primary cell, with the wall flagged if the abstract raises it.
5. Is the variation **identified**? If not, and the outcome is fertility → `RETURN_ASSOCIATION`.
6. Is the outcome **stated** rather than realized? → `PERCEIVED_RETURN`.
7. Still unsure → `UNCLEAR`. Never guess a cell to avoid an `UNCLEAR`; a thin cell may be an
   unscreened cell (`a-thin-cell-may-be-an-unscreened-cell`), but a wrongly-filled one is worse.
