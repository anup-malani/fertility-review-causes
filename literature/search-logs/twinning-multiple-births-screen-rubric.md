# Screening rubric — twinning-multiple-births (A.12)

Title/abstract screen over the D1 worklist. The screener sees title, venue, year, type and a truncated abstract, and does NOT see the D1 score or rank, the discovery channel, the `worklist_reason`, or D1's clinical term-hits.

## What the screen decides

For each record emit `{id, verdict, cell, outcome_type, note?}` where `verdict` is `RELEVANT` / `UNCERTAIN` / `NOT_RELEVANT`, `cell` is one of the cells below, and `outcome_type` is one of the outcome types below.

## `outcome_type` is the whole point of this screen, not a convenience field

**Wall 6 was re-cut on OUTCOME rather than on treatment (PI Call 3, 2026-08-22).** A transfer-protocol study whose outcome is a POPULATION multiple-birth rate is IN (`SECONDARY_ART_MULTIPLES`); one whose outcome is a per-cycle clinical quantity is OUT (`OFF_ART_CLINICAL`). The treatment can be word-for-word identical.

**D1 was explicitly forbidden from making that call and deliberately penalised clinical vocabulary only mildly**, because a term sieve cannot see an outcome: A4 measured the include-side anchor (Reynolds 2003) at 50.8% clinical vocabulary against the exclude-side anchor (Thurin 2004) at 60.6%. The entire weight of Wall 6 therefore rests here.

`outcome_type` is assigned INDEPENDENTLY and cross-checked at assembly against D1's clinical term-hits. Disagreement is not an error to be suppressed — it is Wall 6's working set. If disagreement is rare the wall is enforceable at title/abstract as the scope claims; if it is common the wall is NOT enforceable and the scope must be amended rather than this screen credited with holding a line it could not see.

## Standing instructions, each tied to something measured

**The primary cell is populated by VITAL-STATISTICS REPORTS, not estimation studies, and that is correct rather than disappointing.** A.12 is an accounting identity with a behavioural offset: identities get tabulated, not identified. The reconnaissance found the primary-cell probes headed by *Births: Final Data* and *Annual Summary of Vital Statistics*. A screener expecting effect estimates will read the cell as empty and be wrong. Route a twinning-rate tabulation to `EXPOSURE_SERIES` as RELEVANT — it carries the stage-10 computation — and never to `NOT_RELEVANT` for lacking an estimate.

**Do NOT try to enforce Wall 8; it is declared unenforceable.** A family-size IV paper's abstract is about schooling, earnings or labour supply, and its first-stage table — which is where this chapter's estimand actually lives — is invisible. Measured on this frame: of 1,991 records reached from a twin-IV canon seed, **only 154 mention a twinning term at all**. Route a family-size IV design to `PRIMARY_OFFSET_FIRSTSTAGE_CANDIDATE` as `UNCERTAIN` with `outcome_type: child_outcome`, and let full text decide. Marking it NOT_RELEVANT because the abstract is about education is the single most damaging error available in this screen.

**Tabulation is not estimation, and neither is detection.** A record reporting that the twinning rate rose is describing the exposure series. It is RELEVANT and it earns NO causal recall credit. Only `PRIMARY_*` cells do.

**Check the species on every record; do not infer it from topic.** The veterinary cloud is not a homonym — those papers really are about twinning and really are about fertility, and bare 'fertility' there means bovine fertility. A4 measured the dairy seed's cloud at 90.0% detectably non-human while its fertility-vocabulary rate read 34.8%, so the cross-axis AND does NOT screen it out and only the species check will.

**Homonyms should be near-absent here, and their presence is a signal.** A4 counted rather than sampled: SHELX 13 on-topic of 87,673 citing works, TWIP steel 0 of 1,810. D1 demoted them heavily and no homonym-hit record appears in its top 200. If a batch contains several, something upstream has gone wrong and it is worth saying so in a `note`.

**A.18 is routed, never excluded.** Twins-as-design is Wall 4 and belongs to A.18 — but the heritability of DIZYGOTIC twinning is a genuine A.12 input and belongs in `EXPOSURE_SERIES`. Zygosity is the discriminator: MZ twinning is roughly constant across populations, DZ twinning is what varies with age, genetics and ART and is what this chapter is about.

**Defer rather than guess.** An exclusion the abstract could not support is a silent false negative, and nothing downstream can recover it.

## Cells

| cell | definition |
|---|---|
| `PRIMARY_OFFSET_STOPPING` | A twin/multiple birth as the exposure -> SUBSEQUENT or COMPLETED fertility. Does a twin birth displace later births? The chapter's only estimable parameter and its causal recall spine. |
| `PRIMARY_OFFSET_FIRSTSTAGE_CANDIDATE` | A family-size IV design (twins, sibling sex composition, one-child policy) whose FIRST STAGE may estimate the completed-fertility response to a twin birth. Wall 8: the abstract will be about schooling, earnings or labour supply and will NOT say. Route here as UNCERTAIN and let full text decide. NEVER NOT_RELEVANT merely because the abstract is about child outcomes. |
| `PRIMARY_MECHANICAL_IDENTITY` | Explicitly computes or decomposes the arithmetic contribution of multiple births to a birth count or TFR. Rare by nature: an identity gets tabulated, not identified. |
| `SECONDARY_ART_MULTIPLES` | ART's contribution to the MULTIPLE-BIRTH RATE, or a transfer-protocol/eSET study whose outcome is a POPULATION or REGISTRY multiple-birth rate. The Wall 6 INCLUDE side. Per Call 3, A.12 owns the multiplier only; ART's contribution to DELIVERIES is A.17's. |
| `SECONDARY_PM_VARIATION` | Cross-population or historical variation in the twinning rate (West African DZ excess, pre-transition series). Pulled and tagged per Call 5, not excluded, so an overturn costs a re-screen and not a re-search. |
| `EXPOSURE_SERIES` | Twinning-rate levels, trends, compilations, or DETERMINANTS (maternal age, parity, ART, nutrition, genetics). Includes vital-statistics reports. RELEVANT and load-bearing for the stage-10 computation, but it estimates no effect and earns NO causal recall credit. |
| `OFF_ART_CLINICAL` | ART practice whose outcome is PER-CYCLE or clinical: live-birth rate per cycle, cumulative pregnancy rate, implantation, OHSS, embryo quality, cost-effectiveness of a protocol. The Wall 6 EXCLUDE side. The treatment may be identical to a SECONDARY_ART_MULTIPLES record; the OUTCOME is what separates them. |
| `OFF_ART_UPTAKE_A17` | ART access, uptake, funding, insurance mandates, or ART's contribution to total births or TFR through DELIVERIES. A.17's under Call 3's split at the margin. |
| `OFF_PERINATAL` | Outcomes OF being a multiple, or of a twin pregnancy: preterm birth, birth weight, neonatal and maternal morbidity, TTTS, mode of delivery, perinatal mortality. Wall 5, and large. |
| `OFF_TWINDESIGN` | Twins as a research DESIGN rather than a rate: heritability, twin registries, GWAS, zygosity-based variance decomposition. Wall 4, A.18's. ROUTED, never excluded — the heritability of DIZYGOTIC twinning is a genuine A.12 input and belongs in EXPOSURE_SERIES. |
| `OFF_NONHUMAN` | Twinning or fertility in a non-human species, or soil/agronomic fertility. Wall 3. The veterinary literature is NOT a homonym — it really is about twinning and really is about fertility — so only the species separates it. |
| `OFF_HOMONYM_CRYSTAL` | 'Twinning' as a crystal lattice defect. Wall 1. Measured at 0.0% on-topic (13 of 87,673). |
| `OFF_HOMONYM_ENGINEERING` | TWIP/TRIP steel ('TWinning-Induced Plasticity'), digital twins, deformation twinning. Wall 2. Measured at 0.0% on-topic (0 of 1,810). |
| `OFF_OTHER` | A fertility determinant with no A.12 content and no sibling-hypothesis home here. |
| `INSUFFICIENT_INFO` | Cannot be routed on the visible record. Pairs only with UNCERTAIN. |

## Outcome types

| outcome_type | definition |
|---|---|
| `population_births` | A population or cohort birth count, TFR, completed fertility, parity progression, or a registry-level multiple-birth RATE. |
| `twinning_rate` | The twinning or multiple-birth rate itself is the outcome being described or explained. |
| `per_cycle_clinical` | A per-cycle or per-treatment clinical quantity: live-birth rate per cycle, pregnancy/implantation rate, OHSS, embryo quality. |
| `perinatal_health` | A health outcome of a pregnancy or newborn: preterm, birth weight, neonatal or maternal morbidity or mortality. |
| `child_outcome` | A child or adult outcome of family size: schooling, earnings, IQ, health. The Wall 8 shape. |
| `other` | None of the above. |
| `unclear` | The abstract does not state an outcome. |

## Verdict convention

- `RELEVANT` — a primary, secondary, or exposure-series cell. Exposure-series records are RELEVANT and carry the demographic-significance computation; they earn no causal recall credit and must never be routed to a `PRIMARY_*` cell.
- `UNCERTAIN` — routing genuinely unclear on the visible record, or a Wall 8 first-stage candidate. Pairs with `PRIMARY_OFFSET_FIRSTSTAGE_CANDIDATE` or `INSUFFICIENT_INFO`.
- `NOT_RELEVANT` — an `OFF_*` cell.

## Batches

23 batches of up to 60 records; **1,376 records total**, 1,251 carrying an abstract (91%). Abstracts truncated to 80 words — raised from B.6's 60 because this chapter's decisive fact is usually the OUTCOME, and structured ART and perinatal abstracts state it late.

**125 records carry no abstract at all** and are screened on title, venue, year and type alone. Where that is not enough the answer is `UNCERTAIN` + `INSUFFICIENT_INFO`, not a guess.
