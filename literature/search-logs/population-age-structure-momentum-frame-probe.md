# Frame probe — A.9 population age structure and demographic momentum

**Run:** 2026-09-20 (Shravan), targeted A.9 sizing. Reuses the exact `count()` mechanics of
`source/build/goldset/304_candidate_frame_probe.py` (OpenAlex `title_and_abstract.search` on
`cause_axis [AND outcome_axis]`, `meta.count`). Raw counts in
`population-age-structure-momentum-frame-probe.json`.

**Purpose:** size the A.9 literature (per TICK-089 stage-2 item 1). *Not* a "which is smallest"
ranking — A.9 was already nominated; this measures how big its literature is and, more importantly,
**how much of the apparent frame is real vs. homonym.**

**Outcome axis** (held identical to 304): `("fertility" OR "childbearing" OR "birth rate" OR "total
fertility rate")`. Wide outcome adds `"family size" OR "number of children"`.

**Control:** C.3.e `("credit constraint" OR "liquidity constraint")` ∩ fertility = **85**, identical to
the 304 09-13 run's control — the probe is working; a run of zeros would have read as broken.

## Counts (∩ fertility outcome unless noted)

| Layer | Axis | n |
|---|---|---:|
| **Momentum core** | `"population momentum" OR "demographic momentum"` | **192** |
| NARROW frame | core + `"population age structure"` | 502 |
| WIDE frame | + `"age structure" OR "age composition" OR "tempo effect" OR "compositional change"` | 3,636 |
| UNION frame | all distinct terms, deduped | 3,636 |
| UNION (wide outcome) | UNION ∩ wide outcome | 3,805 |
| sublit | `"population age structure"` alone | 314 |
| sublit | `"age structure" OR "age composition"` alone | 3,213 |
| sublit | `"compositional change"` alone | 235 |
| sublit | `"tempo effect"` alone (A.11 term) | 49 |
| homonym | `"demographic momentum"` **unrestricted** | 85 |
| homonym | `"population momentum"` **unrestricted** | 230 |
| homonym | `"age structure"` **unrestricted, all fields** | 32,363 |
| homonym | age-structure **ecology** residue *inside* the fertility frame | 106 |
| boundary | A.11 tempo overlap inside frame (`… AND (tempo OR postponement OR quantum OR Bongaarts-Feeney)`) | 136 |

*(304's carried-forward 09-09 numbers were NARROW 507 / WIDE 3673; this run's 502 / 3636 are the same
frames re-measured 11 days later — the ~1% drift is index growth, not a definitional change.)*

## Reading

1. **A.9 is a small literature.** The anchored, mechanism-specific core is **~200 records**
   (`population momentum`/`demographic momentum`), and a defensible working frame is **~500** (adding
   `population age structure`). Both are small by the standards of the 304 ranking, whose union
   finalists ran 680–6,482.
2. **The WIDE/UNION frame of ~3,600 is homonym-inflated and must be discarded as the frame.** It is
   almost entirely the generic pair `age structure`/`age composition` (3,213 alone ≈ the whole WIDE
   frame). That pair returns **32,363 unrestricted** — it is a core term of population *ecology* and
   *population genetics*, not of demographic momentum — and **106 ecology records leak in even with the
   fertility outcome gate applied.** Using WIDE as the screen input would bury the ~200 real records
   under thousands of age-structured-fish-population and age-structured-epidemic-model papers.
3. **The momentum vocabulary itself is clean.** `demographic momentum` returns only 85 records even
   *unrestricted* — it is an intrinsically demographic phrase with almost no cross-field contamination;
   `population momentum` adds a modest finance/physics tail (230 unrestricted, 192 once gated on
   fertility). So the core anchors are safe; the risk is entirely in the breadth extension.
4. **The A.11 (tempo) boundary is real but bounded:** ~136 records in the frame also carry tempo/
   postponement/quantum vocabulary. Consistent with the scope's Wall 1 — these straddle A.9/A.11 and are
   split at the component level (composition → A.9, tempo → A.11), not routed whole.

## Implication for the production query (stage 3)

- **Anchor the cause axis on momentum-specific vocabulary:** `population momentum`, `demographic
  momentum`, `population age structure`, `age composition change`/`compositional change`,
  `standardization`/`decomposition of the crude birth rate`, `momentum factor`.
- **Do not admit bare `age structure`/`age composition` as a frame term.** Admit them only as a breadth
  extension gated by a *decomposition* or *crude-birth-rate/births* co-term, or they contribute 3,000+
  mostly-ecology records for a few true hits.
- Expect the estimand-ready cell (birth-rate/birth-count decompositions, momentum computations with a
  births interpretation) to be a **small fraction even of the ~200 core**, because much of the momentum
  literature's outcome is population *size/growth*, not a birth rate (scope Wall 3 / `OFF_OUTCOME_POP`).
  `empty-cell-is-the-result` is a live possibility for the identified-design cell.
