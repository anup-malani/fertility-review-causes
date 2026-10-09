# Blinded title/abstract screening rubric — Income Effect on Fertility (C.1.a, TICK-098)

## Review question

Does the paper bear on **C.1.a** — the claim that, **holding prices and the price of time (wages)
constant**, higher household income or wealth raises fertility because *children are a normal good*? The
primary estimand is the effect of an **income or wealth shock that is NOT also a wage / price-of-time
shock** on a fertility outcome. C.1.a is the baseline normal-good counterfactual; its *secular failure*
is the puzzle other chapters address, so a correctly-signed-but-small or near-zero clean estimate is
exactly what this chapter expects to find.

Judge ONLY the supplied title and abstract. Discovery channel and anchor status are intentionally
hidden. If the abstract is missing or cannot distinguish the shock type, use `UNCERTAIN` — do not infer
from author, journal, or title fragments.

## THE LOAD-BEARING BOUNDARY (C.1.a vs C.2.e)

A **wage / earnings** change moves income **and** the price of a mother's time **together**. That is the
female-wage / opportunity-cost channel (C.2.e), **not** C.1.a. C.1.a owns only the pure income (wealth)
channel. So the single most important routing judgment is the **shock type**:

- Non-labor income / wealth shock (lottery, cash transfer, UBI/NIT, EITC income component, housing or
  asset-price wealth, resource/commodity windfall, inheritance, pension/benefit lump sum) → **C.1.a** (RELEVANT).
- Wage rate, earnings, labor-demand, minimum wage, trade shock, job displacement where the operative
  margin is *earnings/employment of the mother* → **ROUTE_C2E**.
- Relative / cohort income, "doing better than your parents" → **ROUTE_C6A** (Easterlin).
- Uncertainty / job insecurity / credit or liquidity constraint / student debt / unemployment-as-risk →
  **ROUTE_UNCERTAINTY**.
- Macro "economic development / GDP / growth / modernization → fertility" with no clean household-income
  identification → **ROUTE_DEV**.
- Fertility → income/labor supply (reverse) → **REVERSE**.

## Verdicts (choose exactly one)

- `RELEVANT` — estimates a non-labor income/wealth shock → fertility (the C.1.a core).
- `RELEVANT_HISTORICAL` — pre-industrial / historical income–fertility gradient (PM-era sign test).
- `POOLING` — RELEVANT **and** reports an extractable quantitative effect (coefficient/elasticity/CI or
  enough to compute one). A POOLING paper is also RELEVANT; use POOLING when an effect size is present.
- `THEORY` — theoretical model / review of the income–fertility relationship. Keep, do not pool.
- `ROUTE_C2E` / `ROUTE_C6A` / `ROUTE_UNCERTAINTY` / `ROUTE_DEV` — on fertility but the operative channel
  belongs to a neighbour cell (see boundary).
- `REVERSE` — fertility causing income.
- `OFF` — not about income/wealth → fertility at all.
- `UNCERTAIN` — abstract missing or insufficient to route.

## Output

JSON array, one object per record, each: `{"idx", "paperId", "verdict", "confidence"
("high"|"medium"|"low"), "reason" (<=20 words)}`. Return every supplied record exactly once.
