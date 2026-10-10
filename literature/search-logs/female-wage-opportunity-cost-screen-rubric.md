# Blinded title/abstract screening rubric — Female Wage and Opportunity Cost of Time (C.2.e, TICK-099)

## Review question

Does the paper bear on **C.2.e** — the claim that, **holding non-labor income constant**, a rise in the
**female (maternal) wage / the opportunity cost of women's time** lowers fertility because the
**substitution effect** raises the effective price of child-rearing time? The primary estimand is the
fertility response to a **shock to the wage rate / price of a woman's time** (not merely an income shock).
C.2.e is a candidate *cause* of the FDT/SDT decline — a correctly-signed (negative) and large substitution
effect is exactly what this chapter is looking for.

Judge ONLY the supplied title and abstract. Discovery channel and anchor status are intentionally hidden.
If the abstract is missing or cannot distinguish the shock type, use `UNCERTAIN` — do not infer from
author, journal, or title fragments.

## THE LOAD-BEARING BOUNDARY (C.2.e vs C.1.a)

A **wage / earnings** change moves income **and** the price of a mother's time **together**. C.2.e owns
only the **price-of-time (substitution)** channel; C.1.a owns the **pure non-labor income / wealth**
channel. So the single most important routing judgment is the **shock type**:

- Wage rate, earnings, labor-demand, minimum wage, trade/export shock, returns to schooling, gender-wage-
  gap / equal-pay reform, occupation/sector wage shift — where the operative margin is the **price of the
  mother's time / her wage** → **C.2.e** (RELEVANT).
- Non-labor income / wealth shock (lottery, cash transfer, UBI/NIT, EITC income component, housing/asset
  wealth, resource windfall, inheritance) where the price of time is held → **ROUTE_C1A**.
- Norms / attitudes / female autonomy / empowerment / gender ideology with no wage channel →
  **ROUTE_D2A** (female empowerment, ideational).
- Smartphone / social media / digital leisure substitution → **ROUTE_C2H**.
- Macro "economic development / GDP / growth / modernization → fertility" with no clean wage/price-of-time
  identification → **ROUTE_DEV**.
- Fertility → female labor supply / employment (reverse; child or motherhood penalty; FLFP as the OUTCOME
  of childbearing) → **REVERSE**.

## Verdicts (choose exactly one)

- `RELEVANT` — estimates a female-wage / price-of-time (substitution) shock → fertility (the C.2.e core).
- `POOLING` — RELEVANT **and** reports an extractable quantitative effect (coefficient/elasticity/CI or
  enough to compute one). A POOLING paper is also RELEVANT; use POOLING when an effect size is present.
- `THEORY` — theoretical model / review of the wage–opportunity-cost–fertility relationship. Keep, do not
  pool.
- `ROUTE_C1A` / `ROUTE_D2A` / `ROUTE_C2H` / `ROUTE_DEV` — on fertility but the operative channel belongs to
  a neighbour cell (see boundary).
- `REVERSE` — fertility causing female labor supply / employment (child/motherhood penalty).
- `OFF` — not about the female wage / price of time → fertility at all.
- `UNCERTAIN` — abstract missing or insufficient to route.

## Output

JSON array, one object per record, each: `{"idx", "paperId", "verdict", "confidence"
("high"|"medium"|"low"), "reason" (<=20 words)}`. Return every supplied record exactly once.
