# TICK-089: A.9 Population Age Structure and Demographic Momentum
**Status:** in-progress
**Assigned:** Shravan
**Hypothesis:** `population-age-structure-momentum` — HYPOTHESES-v5.md §A.9
**Parallel-safe:** yes
**Blocks:** none
**Blocked by:** none
**Touches:** literature/search-logs/population-age-structure-momentum-*, extraction/population-age-structure-momentum-*, output/chapters/population-age-structure-momentum.md

## Acceptance criteria
- [x] 2. Search strategy and scope drafted — `literature/search-logs/population-age-structure-momentum-search-scope.md` (DRAFT, not frozen)
- [ ] 3. Literature search and AI screening, both phases (§5.1)
- [ ] 4. RA title/abstract review
- [ ] 5. Full-text retrieval
- [ ] 6. Full-text screen, RA spot-checks 5–10%
- [ ] 7. Extraction to `extraction/population-age-structure-momentum.csv`, RA verifies a random 10%
- [ ] 8. Risk-of-bias assessment per study
- [ ] 9. Meta-analysis if ≥3 extractable effects, narrative synthesis otherwise
- [ ] 10. Demographic significance against PM / FDT / SDT
- [ ] 11. GRADE rating, 3 independent raters
- [ ] 12. Chapter draft on the §6 template
- [ ] 13. RA lay-readability check
- [ ] 14. PI review and sign-off

## Why this one now

Nominated as the smallest open **A. Proximate Causes** candidate. The three obviously-small
proximate determinants that would otherwise lead the ranking — A.12 twinning (TICK-070), A.17 ART
(TICK-072), A.18 heritability (TICK-076) — are already claimed, as are A.3 (TICK-088), A.6 (TICK-087,
parked), A.23 (TICK-075) and A.24 (TICK-071). A.11 tempo is drafted. Of what remains open (A.1, A.2,
A.4, A.5, A.7, A.8, A.9, A.13, A.14, A.15, A.16, A.19, A.20), A.9 is the only one whose mechanism is
an **accounting identity** (age composition → CBR / period TFR, holding age-specific rates fixed)
rather than a contested behavioural or biological literature; its registry note calls it "largely
accounting/measurement," and its seminal set (Keyfitz 1971; Bongaarts & Bulatao 1999; Lutz et al.
2003) is small and uncontested. It parallels the already-drafted **A.11 tempo-effects** chapter — the
same "measurement/mechanical determinant" shape — so we reuse that template for the hard part, which
is framing a mechanical determinant against PM / FDT / SDT.

**Caveats to resolve in stage 2, before trusting the "smallest" claim:**

1. **The frame probe has not measured A.9.** `source/build/goldset/304_candidate_frame_probe.py` and
   its 09-10 / 09-13 runs live on the unmerged TICK-080 branch and do not yet include A.9. Smallness
   here is qualitative (registry note + seminal set), not a measured union-frame/anchored-core count.
   Run A.9 through the probe as the first scope step and record its union frame, anchored core, and the
   core-of-union ratio (the C.2.f / C.3.d "anchored literature" signature).
2. **Registered-construct completeness test.** A.6 and A.3 each placed first on raw count and were
   passed over because their selecting frame omitted the registry's own construct and undercounted the
   literature (`404`, TICK-087/TICK-088). A.9 must be cleared of the same defect: confirm the frame
   carries the registry's construct vocabulary (demographic momentum, age-structure / population-age
   composition, tempo-vs-quantum-adjacent decomposition terms) before its count is trusted.
3. **Homonym load.** "Momentum" and "age structure" are heavily overloaded outside demography
   (physics, finance, population-genetics age structure). Run the homonym residue check inside the
   fertility-restricted frame, as C.3.f did.
4. **Boundary with A.11 tempo.** Momentum (a stock/composition effect on completed and period
   fertility) and tempo (a timing distortion of period TFR) are distinct but adjacent and both live in
   the period-vs-cohort measurement debate. Measure the A.9↔A.11 wall and state the scope split
   explicitly; A.11 is drafted so that wall is inherited, not litigated.

**Phenomena:** registry §A.9 lists **FDT, SDT** (not PM), so stage 10 assesses two phenomena. The
likely verdict is near-determinate — momentum/composition moves CBR and short-run period TFR but not
completed cohort fertility — which is the reason this is a low-risk pass through the full pipeline
rather than a novel-evidence chapter. `empty-cell-is-the-result` / `empty-cell-needs-second-channel`
apply if the identified-design cell is thin.

## Log

**2026-09-20 (Shravan) — stage 2 search scope drafted.**

*Result.* Drafted `literature/search-logs/population-age-structure-momentum-search-scope.md` (DRAFT,
not frozen). Key rulings:
- A.9 is a **non-effect estimand** (decomposition/accounting + demographic momentum), not a treatment.
  Two constructs held apart: age-composition effects on period *counts/CBR*, and Keyfitz-style
  demographic momentum.
- **Load-bearing correction:** the composition effect lands on the **CBR and birth counts**, is **zero
  by construction on the period TFR** (which is already age-standardized) and **zero on completed cohort
  fertility.** The v5 claim text ("...crude birth rates and period TFR...") is imprecise on the TFR
  clause — flagged for TICK-001; tempo (A.11), not composition, is what moves period TFR.
- Four boundary walls: **W1 A.9 vs A.11 tempo** (composition/weights vs timing/rates — the sharpest),
  **W2 A.9 as the shared accounting residual** (A.10's Wall 4 already routes `MECHANICAL_COMPOSITION →
  A.9`; A.9's CBR verdict is *not additive* with other chapters), **W3 A.9 vs population-size/growth
  outcomes** (`OFF_OUTCOME_POP`, expected largest cell), **W4 A.9 vs A.1 mortality** (determinant of the
  age structure).
- Adopts TICK-080 §5–6 provisionally: GRADE **NOT RATEABLE — non-effect estimand**; demographic
  significance reported **per outcome** (CBR/births large-by-construction → report magnitude not
  pass/fail; period TFR = 0; CCF = 0), not a single label.

*Escalations to Anup (recorded here; no repo-wide escalation-log.md exists — same practice as A.10 /
TICK-054):*
1. **Non-additive proximate causes / mechanical-composition ownership.** Does A.9 own and *define* the
   mechanical-composition component that A.1/A.7/A.8/A.10 then report *net of*? Same item TICK-054
   (A.10 Wall 2) and TICK-080 raise; A.9 is the natural place to land the rule. **Blocks freeze.**
2. **Rating a non-effect estimand.** Confirm GRADE "NOT RATEABLE" and the per-outcome demsig reporting
   for A.9 (this is the concrete case behind TICK-080 §5–6). **Blocks freeze.**

*Workflow impact.* First chapter whose primary estimand is an accounting identity; it is the test case
for TICK-080's non-effect-estimand GRADE band and per-outcome demsig reporting, and the landing site
for the review-wide non-additivity rule. Reusable: the "the outcome is not the period TFR" three-way
outcome split parallels A.11 tempo and should be cross-linked when both are finalized.

*Next.* Stage 2 open items before freeze: run the frame probe (`304_candidate_frame_probe.py`, on the
TICK-080 branch) on A.9; registered-construct completeness test; homonym-residue check ("momentum",
"age structure"); second read on Wall 1; then anchor sourcing (channels 1–3, existence-gated).
