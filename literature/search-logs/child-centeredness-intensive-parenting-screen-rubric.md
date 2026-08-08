# Blinded title/abstract screening rubric — child-centered intensive parenting (D.2.d) — v2

## Review question

Does the paper bear on **D.2.d** — the claim that a shift in the *normative standard of what a parent
owes a child* raises the time and emotional cost per child and reduces fertility? The distinctive
D.2.d claim is about the **norm**, not the price: that the standard moved, and would have raised the
cost per child even holding money prices, wages, and returns to child human capital fixed. Preserve
the parenting-ideology theory stream and the FDT-era sentimentalization stream, but route them outside
the empirical primary estimands.

Judge ONLY the supplied title and abstract. Discovery channel and anchor status are intentionally
hidden. Do not infer findings from author, journal, or title fragments, and do not look anything up.

**Title-only policy.** Many records have no abstract. A title alone is sufficient ONLY when it states
the estimand verbatim (e.g. "Intensive Parenting Ideals and Fertility"); route such a record normally
but set `outcome_level` to `NA` unless the title also names the outcome level. In every other
abstract-less case use `UNCERTAIN` with `estimand_cell: INSUFFICIENT_INFO`. Never invent a substantive
cell for a record you know nothing about — that corrupts the cell counts.

**Phenomenon scope is SDT for everything pooled.** FDT-era material on the historical revaluation of
the child (sentimentalization, the "priceless child", the invention of childhood) is retained as
context under `FDT_SENTIMENTALIZATION_CONTEXT` and is never pooled. There is no pre-modern cell.

## The routing question, asked once

Every wall below reduces to the same question: **what does the estimate actually vary?** Route on the
source of identifying variation, never on the paper's framing and never on whose theory it cites. A
paper whose narrative is entirely about intensive parenting, but whose variation is in inequality,
wages, or returns to schooling, belongs to a neighbour.

## THE SIX BOUNDARY WALLS

**Wall 1 — vs C.3.d (quantity-quality tradeoff).** C.3.d varies a *return or price* — skill premia,
returns to schooling, the price of child quality. D.2.d varies a *norm or standard*. A study
identifying off returns to human capital routes to `OFF_QQ_C3d` **even when framed as being about
parenting intensity**. Nearly every D.2.d paper cites Becker; citing him is not routing.

**Wall 2 — vs C.2.f (inequality and status competition).** C.2.f varies inequality, relative position,
or status pressure. D.2.d varies the parenting standard, holding that fixed. Doepke–Zilibotti-type
work is a *joint* claim (inequality → parenting style → fertility) and stays here **only** when the
estimate isolates the parenting-style link from the inequality or returns shock driving it; otherwise
`OFF_INEQUALITY_C2f`.

**Wall 3 — vs C.2.b (rising direct costs).** C.2.b measures *money* — expenditure per child, cost-of-
raising estimates, price indices. D.2.d measures the standard, and centrally the *time, attention, and
emotional labour* it demands. A paper reporting only a money aggregate routes to `OFF_DIRECT_COST_C2b`
whatever its narrative.

**Wall 4 — vs C.2.e (female wage / opportunity cost of time).** C.2.e varies the *price* of the
mother's time (wages, labour-demand shocks). D.2.d varies the *quantity of time the norm demands*, at
a fixed wage. Wage or labour-demand variation → `OFF_TIMECOST_C2e`.

**Wall 5 — vs C.2.a (childcare cost and availability).** Childcare price, subsidy, or supply variation
→ `OFF_CHILDCARE_C2a`. D.2.d's neighbouring claim is that the norm designates *parental* care as
non-substitutable — a belief about adequacy, not a supply curve.

**Wall 6 — vs D.2.a (female empowerment / gender equity).** D.2.a varies gender-role attitudes, the
division of domestic labour, or partner care-sharing. D.2.d varies the *total* standard of care a
child is owed, irrespective of who supplies it. Papers on intensive *mothering* routinely straddle;
where neither term is isolated use `MIXED_NORM_UNRESOLVED`.

## WHAT THIS SCREEN CANNOT DECIDE — read before routing anything OFF

Four of the six walls discriminate on the estimate's source of variation, which is a **design fact that
usually appears only in a methods section.** You will frequently not be able to tell.

| Wall | Decidable here? |
|---|---|
| 1 (C.3.d) | **No** — returns-variation vs norm-variation is a design fact |
| 2 (C.2.f) | **No** — whether the parenting link is isolated is invisible in an abstract |
| 3 (C.2.b) | Usually — money vs time is normally named |
| 4 (C.2.e) | Partly — "wage" is named; "hours at fixed wages" is not |
| 5 (C.2.a) | **Yes** — childcare price/supply is a named intervention |
| 6 (D.2.a) | **No** — gender-role vs care-level variation is a design fact |

**When routing turns on Wall 1, 2, or 6 and the abstract does not name the source of variation, use
`ROUTING_DEFERRED_TO_FULLTEXT` with verdict `UNCERTAIN`.** Do not guess an `OFF_*` label. An `OFF_*`
assigned on an abstract that could not support it is a silent false negative, and on this hypothesis
the `OFF_*` cells are where most of the corpus lands. Deferring is the correct answer, not a failure.

## Reverse causation — the first-order threat here

Parental time and attention *per child* is a quantity divided by the number of children, so a parent of
one supplies more per child almost by construction. Papers where **parity drives parenting intensity**
take `REVERSE`, not a primary cell. If the abstract does not establish direction, that is `UNCERTAIN`,
not a primary cell.

## Required output

Return one JSON array, in input order, exactly one object per paper:

```json
{
  "paperId": "copy exactly",
  "verdict": "RELEVANT | UNCERTAIN | NOT_RELEVANT",
  "estimand_cell": "PRIMARY_NORM_EXPOSURE | PRIMARY_TIME_INTENSITY | PRIMARY_PERCEIVED_STANDARD | COST_INDEPENDENCE | PARENTING_NORM_CONSTRUCT | PARENTING_NORM_THEORY | FDT_SENTIMENTALIZATION_CONTEXT | OFF_QQ_C3d | OFF_INEQUALITY_C2f | OFF_DIRECT_COST_C2b | OFF_TIMECOST_C2e | OFF_CHILDCARE_C2a | OFF_GENDER_D2a | MIXED_NORM_UNRESOLVED | ROUTING_DEFERRED_TO_FULLTEXT | OFF_OTHER | OFF_OUTCOME | REVERSE | INSUFFICIENT_INFO | NA",
  "outcome_level": "STATED_INTENTION_OR_ATTITUDE | REALIZED_FERTILITY | BOTH | NA",
  "norm_measure": "attitude scale | time use | perceived standard | policy/media exposure | inferred, not measured | n/a",
  "variation_source": "short phrase in the authors' own terms, or 'not stated'",
  "treatment": "short phrase or n/a",
  "outcome": "short phrase or n/a",
  "direction_established": "yes | no | unclear",
  "evidence_type": "quasi-experimental | observational | structural | theory | review | qualitative | mechanism | other",
  "reason": "one concise clause grounded in title/abstract"
}
```

`variation_source` is the field that later settles Walls 1, 2, 4 and 6. Record what the abstract says,
including "not stated" — a truthful "not stated" is more useful than a confident guess, and it is what
justifies `ROUTING_DEFERRED_TO_FULLTEXT`.

## Verdict rules

- `RELEVANT`: studies a parenting norm, standard, or measured parenting intensity as a determinant of
  fertility intention or behaviour. **`RELEVANT` ALSO covers the two theory cells and the FDT context
  cell** — see the note below.
- `UNCERTAIN`: plausibly belongs, but missing or ambiguous information prevents confident routing.
  This includes every `ROUTING_DEFERRED_TO_FULLTEXT`, every `INSUFFICIENT_INFO`, and any case where
  direction is unestablished.
- `NOT_RELEVANT`: does not bear on the norm → fertility estimand. General parenting research, general
  fertility-decline research, and child-outcome research are NOT automatically relevant.

**The theory and context streams take `RELEVANT`, or `UNCERTAIN` if you cannot tell whether the
paper belongs here at all.** They never take `NOT_RELEVANT` — a theory paper that belongs to a
neighbour takes that neighbour's `OFF_*` cell. *(v2: v1 forced `RELEVANT`, which made a screener who
genuinely could not separate norm content from investment content assert relevance anyway.)*

**`PARENTING_NORM_CONSTRUCT` is empirical and takes empirical evidence types.** Measuring prevalence,
trends, or class gradients in parenting norms is observational research; it belongs in this cell with
`evidence_type: observational`. Only `PARENTING_NORM_THEORY` and `FDT_SENTIMENTALIZATION_CONTEXT` are
argument rather than estimate. *(v2: v1's validator rejected correct construct-cell calls.)*

**The theory and context streams take `RELEVANT`.** `PARENTING_NORM_THEORY`,
`PARENTING_NORM_CONSTRUCT`, and `FDT_SENTIMENTALIZATION_CONTEXT` papers have no fertility estimand by
definition, and the verdict rules above define `RELEVANT` in terms of one. Resolve that tension this
way and not by reading the rules literally: these three cells are `RELEVANT`, and are separated
downstream. They do **not** count toward empirical recall. *(This ambiguity is fixed here at v1 because
it governed 21 of 35 RELEVANT verdicts in D.3.b's wave-1 audit before being caught.)*

**Reviews and meta-analyses.** A systematic review or meta-analysis *of the core estimand* takes the
matching PRIMARY cell with `evidence_type: review` — it is not exiled to a theory cell. A review of an
adjacent literature routes by its subject like any other paper. *(Also a D.3.b wave-1 defect, fixed
here at v1.)*

**`OFF_OUTCOME` is expected to be the largest cell by a wide margin.** The intensive-parenting
literature is overwhelmingly about child development, attainment, and parental — especially maternal —
wellbeing. Parenting intensity with a non-fertility outcome is `OFF_OUTCOME`, verdict `NOT_RELEVANT`.
That is a fact about the literature, not a screening failure, and you should not strain to rescue such
papers into a primary cell.

**`OFF_OTHER`** takes non-D.2.d fertility determinants with no sibling-hypothesis home, so the `OFF_*`
routing labels do not ship junk into the C.3.d / C.2.f / C.2.b / C.2.e / C.2.a / D.2.a queues.

## Cell definitions, briefly

| cell | what earns it |
|---|---|
| `PRIMARY_NORM_EXPOSURE` | exposure to or internalization of an intensive/child-centered parenting norm → fertility |
| `PRIMARY_TIME_INTENSITY` | measured parental time, supervision, or enrichment per child → fertility |
| `PRIMARY_PERCEIVED_STANDARD` | perceived standard of adequate parenting → fertility |
| `COST_INDEPENDENCE` | the above, with money price, wages, **and** returns to child human capital held fixed — the value-added cell; expect it to be rare or empty |
| `PARENTING_NORM_CONSTRUCT` | the norm as object of study: scale validation, prevalence, trends, class gradients; no fertility outcome |
| `PARENTING_NORM_THEORY` | normative, historical, or theoretical argument about child-centeredness and family size |
| `FDT_SENTIMENTALIZATION_CONTEXT` | historical revaluation of the child in the FDT era; context, never pooled |
| `REVERSE` | parity or family size drives parenting intensity |
| `OFF_OUTCOME` | parenting intensity → any non-fertility outcome |
| `INSUFFICIENT_INFO` | cannot be routed on the visible record; pairs only with `UNCERTAIN` |
