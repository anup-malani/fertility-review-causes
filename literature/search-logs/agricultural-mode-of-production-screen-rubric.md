# Blinded title/abstract screening rubric — mode of production & child economic value (C.3.a)

## Review question

Does the paper bear on **C.3.a** — the claim that a society's **mode of subsistence** (foraging,
horticulture, pastoralism, extensive vs intensive agriculture) sets the **economic value of children**
(their labor productivity, the age they become net producers, the length of dependency, the
compatibility of childcare with the mother's subsistence work) and thereby sets the **baseline level of
fertility** across pre-modern populations? This is a PRE-MODERN cross-population *level* phenomenon.

Judge ONLY the supplied title and abstract. Discovery channel and anchor status are intentionally
hidden. When the abstract is missing or cannot distinguish a plausible relevant paper, use `UNCERTAIN`;
do not infer findings from author, journal, or title fragments.

## THE LOAD-BEARING BOUNDARY — the forager/agriculturalist gap is overdetermined (Walls 1 & 2)

The headline fact — mobile foragers have longer birth intervals and lower fertility than settled
agriculturalists — is predicted by THREE mechanisms, only one of which is C.3.a's:

- **C.3.a (this chapter):** children's **economic value / labor** differs by production system.
- **A.13 (route away):** intensive on-demand **breastfeeding / lactational amenorrhea** suppresses
  ovulation and lengthens birth intervals — a biological proximate determinant, no economics.
- **Nutrition (route away):** maternal **energy balance / caloric availability** changes fecundity —
  no economics.

Therefore a paper that reports a subsistence-fertility difference is C.3.a-**primary ONLY IF** it
either (a) **measures the child economic-value / labor / dependency channel directly**, or (b) **holds
fixed or controls** the nursing and energy channels. A bare cross-subsistence fertility comparison with
neither is `BARE_CROSS_SYSTEM` (topical, documents the explanandum, NOT pooled as causal evidence). A
paper whose mechanism is nursing is `OFF_NURSING_A13`; whose mechanism is energy/nutrition is
`OFF_NUTRITION_B`. Do NOT promote these to a PRIMARY cell because subsistence or fertility is mentioned.

## Required output

Return one JSON array, in input order, exactly one object per paper:

```json
{
  "paperId": "copy exactly",
  "verdict": "RELEVANT | UNCERTAIN | NOT_RELEVANT",
  "estimand_cell": "PRIMARY_VALUE_DIRECT | PRIMARY_CROSS_SYSTEM_CONDITIONED | PRIMARY_TRANSITION | BARE_CROSS_SYSTEM | MIXED_VALUE_NURSING | CHILD_LABOR_NO_FERTILITY | MODE_OF_PRODUCTION_THEORY | OFF_NURSING_A13 | OFF_NUTRITION_B | OFF_CHILD_LABOR_LAW_C3b | OFF_QQ_C3d | OFF_WEALTH_FLOWS_C3f | OFF_LAND_WAGE_C4a | OFF_URBAN_C2g | OFF_OUTCOME | OFF_OTHER | REVERSE | NA",
  "subsistence_mode": "forager | horticulturalist | pastoralist | agriculturalist | mixed | cross-cultural | n/a",
  "treatment": "short phrase or n/a",
  "outcome": "short phrase or n/a",
  "proximate_controls": "value-measured | nursing/energy-controlled | neither | n/a",
  "evidence_type": "cross-cultural | within-society-transition | single-society-energetics | observational | structural | theory | review | mechanism | other",
  "reason": "one concise clause grounded in title/abstract"
}
```

## Verdict rules

- `RELEVANT`: studies or models how the production/subsistence system or the economic value of children
  shapes fertility across pre-modern populations — including the bare cross-subsistence comparison and
  the child-labor-value mechanism (even without a fertility outcome), and the theory canon.
- `UNCERTAIN`: plausibly belongs, but missing/ambiguous information prevents confident routing.
- `NOT_RELEVANT`: does not bear on production system → child value → fertility. A generic fertility,
  demography, agriculture, or development paper is NOT automatically relevant.

## Estimand cells

- `PRIMARY_VALUE_DIRECT`: direct measurement of children's net production / age-specific labor value /
  dependency length by production system, linked to fertility. The value-channel core.
- `PRIMARY_CROSS_SYSTEM_CONDITIONED`: cross-cultural subsistence → fertility that **controls/holds fixed
  the nursing and energy channels** OR enters a direct child-value measure (incl. phylogenetically
  controlled comparisons).
- `PRIMARY_TRANSITION`: a within-society mode-of-production change (sedentarization, intensification,
  plough/irrigation/cash-crop adoption, labor-saving technology, settlement scheme) → fertility change.
- `BARE_CROSS_SYSTEM`: subsistence category → fertility with NO value measure and NO nursing/energy
  control. Topical; documents the explanandum; not pooled as C.3.a causal evidence.
- `MIXED_VALUE_NURSING`: forager-farmer gap where value and lactational-amenorrhea channels are not
  separable. Flag; reported to both C.3.a and A.13 (non-additive).
- `CHILD_LABOR_NO_FERTILITY`: children's production / time allocation measured by production system,
  **no fertility outcome**. Mechanism/context.
- `MODE_OF_PRODUCTION_THEORY`: Boserup intensification, embodied-capital / net-transfer models,
  behavioral-ecology models of subsistence and family size, with no empirical fertility estimate.
- `OFF_NURSING_A13`: mechanism is breastfeeding / lactational amenorrhea → birth spacing. Route to A.13.
- `OFF_NUTRITION_B`: mechanism is caloric intake / energy balance / maternal condition → fecundity.
  Route to nutrition-energy-availability.
- `OFF_CHILD_LABOR_LAW_C3b`: treatment is child-labor law / compulsory schooling (industrial-economy
  policy). Route to C.3.b.
- `OFF_QQ_C3d`: treatment is returns to human capital / quality investment per child. Route to C.3.d.
- `OFF_WEALTH_FLOWS_C3f`: treatment is net intergenerational-transfer direction / modernization reversal
  (an FDT story). Route to C.3.f.
- `OFF_LAND_WAGE_C4a`: treatment is land availability / real wages → nuptiality or the Malthusian check.
  Route to C.4.a.
- `OFF_URBAN_C2g`: rural-urban or residential-shift comparison. Route to C.2.g.
- `OFF_OUTCOME`: production system → some non-fertility outcome (growth, nutrition, labor supply,
  migration, health) with no fertility. Mechanism/context.
- `OFF_OTHER`: a fertility determinant outside C.3.a with no sibling home here.
- `REVERSE`: fertility / population density → agricultural intensification (the Boserup direction).
- `NA`: a genuinely off-topic paper with no sensible route. Use only with `NOT_RELEVANT`.

**Verdict × cell convention.** A `NOT_RELEVANT` paper may carry `NA` *or* an `OFF_*`/`REVERSE` route
cell (routing an off-topic paper to where it belongs is useful). The in-scope cells — the three
`PRIMARY_*`, `BARE_CROSS_SYSTEM`, `MIXED_VALUE_NURSING`, `CHILD_LABOR_NO_FERTILITY`,
`MODE_OF_PRODUCTION_THEORY` — mean the paper IS relevant to C.3.a, so they require `RELEVANT` or
`UNCERTAIN`, never `NOT_RELEVANT`.

## Precision rules

1. A PRIMARY cell requires BOTH a production-system / child-value treatment AND a fertility outcome,
   AND (for the cross-system cell) that the nursing/energy confound is addressed. Otherwise use
   `BARE_CROSS_SYSTEM`, `CHILD_LABOR_NO_FERTILITY`, or an OFF cell.
2. A subsistence-fertility difference whose stated mechanism is breastfeeding is `OFF_NURSING_A13`, and
   whose stated mechanism is nutrition/energy is `OFF_NUTRITION_B`, even if it mentions child labor in
   passing. This is the overdetermination wall; enforce it.
3. A within-industrial-economy fertility decline driven by schooling, child-labor law, or rising
   returns to human capital is C.3.b / C.3.d (`OFF_CHILD_LABOR_LAW_C3b` / `OFF_QQ_C3d`), NOT the
   pre-modern cross-system level — even in an agrarian setting.
4. Reviews may be `RELEVANT` but cannot be PRIMARY; use the best non-primary cell and
   `evidence_type=review`.
5. Set `proximate_controls=value-measured` only when the design actually measures the child
   economic-value / labor channel; `nursing/energy-controlled` only when it controls or holds those
   fixed. This is the clause that separates a PRIMARY cell from `BARE_CROSS_SYSTEM`.
