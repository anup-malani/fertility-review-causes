#!/usr/bin/env python3
"""
91_c3a_make_screen_batches.py — C.3.a (mode of production and child economic value), stage A5 input.

Prepare the Tier-B frame for blinded title/abstract LLM screening. No candidate is filtered here
(keep-and-route). Records are deterministically shuffled, stripped of all discovery/gold/identity
provenance (blinding), and split into fixed-size batches. A committed manifest records paths + SHA-256;
batch payloads live in temp/ (reproducible from the committed frame). Mirrors B.1 step 66.

The rubric routes on the search-scope walls. The load-bearing one is Wall 1 / Wall 2: the forager-
agriculturalist fertility gap is overdetermined by lactational amenorrhea (A.13) and energy balance
(nutrition), so a bare subsistence-fertility comparison with no economic-value measure and no
nursing/energy control is NOT C.3.a-primary. The two routing decoys in the anchor set (Konner &
Worthman 1980 -> OFF_NURSING_A13, Ellison et al. 1993 -> OFF_NUTRITION_B) are NOT in the frame
(anchors are excluded), so decoy routing is validated by the volume of nursing/nutrition route-aways.

Inputs : literature/search-logs/{slug}-tier-b-frame.json
Outputs: temp/screen/{slug}/batch_NNN.json, RUBRIC.md
         literature/search-logs/{slug}-screen-manifest.json
         literature/search-logs/{slug}-screen-rubric.md
"""
import hashlib, json, random
from pathlib import Path

SLUG = "agricultural-mode-of-production"
SEED = 301  # C.3.a
BATCH_SIZE = 40
HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
LOGS = REPO / "literature" / "search-logs"
SCREEN = REPO / "temp" / "screen" / SLUG
SCREEN.mkdir(parents=True, exist_ok=True)

RUBRIC = """# Blinded title/abstract screening rubric — mode of production & child economic value (C.3.a)

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
"""


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    source = LOGS / f"{SLUG}-tier-b-frame.json"
    records = json.loads(source.read_text())
    ids = [r.get("paperId") for r in records]
    if any(not v for v in ids) or len(ids) != len(set(ids)):
        raise SystemExit("frame must have unique, nonblank paperId values")

    shuffled = list(records)
    random.Random(SEED).shuffle(shuffled)
    (SCREEN / "RUBRIC.md").write_text(RUBRIC)
    manifest, assigned = [], []
    for start in range(0, len(shuffled), BATCH_SIZE):
        number = start // BATCH_SIZE + 1
        batch = []
        for row in shuffled[start:start + BATCH_SIZE]:
            batch.append({
                "paperId": row["paperId"],
                "title": row.get("title") or "",
                "year": row.get("year"),
                "abstract": (row.get("abstract") or "")[:3500],
            })
            assigned.append(row["paperId"])
        ip = SCREEN / f"batch_{number:03d}.json"
        ip.write_text(json.dumps(batch, indent=2, ensure_ascii=False))
        manifest.append({"batch": number, "n": len(batch),
                         "input": str(ip.relative_to(REPO)), "input_sha256": sha256(ip),
                         "output": str((SCREEN / f"verdict_{number:03d}.json").relative_to(REPO))})
    if len(assigned) != len(records) or set(assigned) != set(ids):
        raise SystemExit("batch coverage invariant failed")

    committed = {"slug": SLUG, "stage": "blinded_title_abstract_screen_input",
                 "source": str(source.relative_to(REPO)), "source_sha256": sha256(source),
                 "seed": SEED, "batch_size": BATCH_SIZE, "records": len(records), "batches": len(manifest),
                 "records_with_abstract": sum(bool((r.get("abstract") or "").strip()) for r in records),
                 "blinded_fields": ["doi", "authors", "venue", "cited_by_count",
                                    "discovery_channels", "seed_ids", "gold_status"],
                 "coverage_verified": True, "manifest": manifest}
    (LOGS / f"{SLUG}-screen-manifest.json").write_text(json.dumps(committed, indent=2, ensure_ascii=False))
    (LOGS / f"{SLUG}-screen-rubric.md").write_text(RUBRIC)
    print(f"{len(records)} records -> {len(manifest)} blinded batches of <= {BATCH_SIZE}; "
          f"abstracts {committed['records_with_abstract']}; coverage verified")


if __name__ == "__main__":
    main()
