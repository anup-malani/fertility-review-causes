# TICK-076: A.18 Genetic and Heritable Variation in Fertility
**Status:** in-progress
**Assigned:** Shravan
**Hypothesis:** `heritability-fertility-genetic` — HYPOTHESES-v5.md §A.18
**Parallel-safe:** yes
**Blocks:** none
**Blocked by:** none
**Touches:** literature/search-logs/heritability-fertility-genetic-*, extraction/heritability-fertility-genetic-*, output/chapters/heritability-fertility-genetic.md

## Acceptance criteria
- [x] 2. Search strategy and scope drafted — `literature/search-logs/heritability-fertility-genetic-search-scope.md` (2026-08-31). **FROZEN:** Rulings 1–4 resolved; 5 routed to TICK-001. Stage 3 unblocked.
- [ ] 3. Literature search and AI screening, both phases (§5.1)
- [ ] 4. RA title/abstract review
- [ ] 5. Full-text retrieval
- [ ] 6. Full-text screen, RA spot-checks 5–10%
- [ ] 7. Extraction to `extraction/heritability-fertility-genetic.csv`, RA verifies a random 10%
- [ ] 8. Risk-of-bias assessment per study
- [ ] 9. Meta-analysis if ≥3 extractable effects, narrative synthesis otherwise
- [ ] 10. Demographic significance against PM / FDT / SDT
- [ ] 11. GRADE rating, 3 independent raters
- [ ] 12. Chapter draft on the §6 template
- [ ] 13. RA lay-readability check
- [ ] 14. PI review and sign-off

## Log

**2026-08-31 (Shravan) — stage 2.** Scope memo drafted; 25/25 cold-start anchors resolved against
OpenAlex, no ghost citations (`245_a18_cold_start_anchors.py`).

Three things the scope work turned up that are not local to this chapter:

1. **A.18's primary estimand is a variance component, not an effect.** Heritability cannot enter a
   PROTOCOL §4.2.1 demographic-significance calculation — there is no numerator. Ruling 1 puts the
   demsig arm on the selection *response* (a mean shift) instead. A.9, the other non-effect entry in
   the master list, will need the same treatment.
2. **The registered SDT-only phenomenon drops the identified evidence.** The best-identified
   selection-response designs are historical parish pedigrees (Milot 2011, Courtiol 2012); the
   contemporary arm is UK Biobank and HRS, the weakest designs in the set. Ruling 2 asks to admit
   PM/FDT as evidence arms with SDT still carrying the verdict. Blocks the production query.
3. **The resolver defect is still shipping.** A script written today reproduced the OpenAlex `?`
   wildcard refusal *and* recorded it as an absence. Fixed here; belongs in the shared resolver
   alongside TICK-074, which is unmerged.

Next: PI answers on Rulings 2 and 4, then stage 3.

**2026-08-31 (Shravan) — Rulings 1–4 resolved, scope frozen, stage 3 unblocked.**

1. **Demsig arm.** FDT and SDT compute on the selection response R = h² × S. **A PM cell for h² is
   opened**, which reverses the draft's flat claim that heritability has no §4.2.1 numerator anywhere:
   PM's denominator is a *range*, not a change, so a variance share is the right kind of quantity for
   it. Contingent on a protocol answer about units (below). Carries a written caution: the PM share is
   near-definitional, will clear the 10% threshold on almost any twin estimate, and means far less
   there than "significant" means in any other chapter.
2. **Phenomena.** Three-phenomenon chapter, verdicts wherever the arithmetic exists. The halfway
   version first proposed — PM/FDT as evidence, SDT-only verdicts — would have left the
   best-identified designs in the literature permanently unable to move a verdict cell.
3. **`EDUCATION_PGS`.** PGS standard units primary; conversion to children per woman a labelled
   secondary with the r_g interval propagated.
4. **Fecundity traits.** `LINK_TRAIT` unless the same study links the trait to realized births.
5. **Master-list edit confirmed necessary** and drafted in §13 for TICK-001 — `phenomena` widens to
   PM/FDT/SDT, and the `claim` becomes three clauses matching the three arms, including the moderation
   finding the registered text omits.

**Two questions escalated to Anup as protocol-level, neither blocking:** whether PM's §4.2.1
denominator admits a within-population between-individual variance numerator (binds stage 10, and A.9
has the same problem), and the fact that GRADE §4.1 has no band for a non-effect estimand, so a
competent twin design scores "Very low: correlational only" (binds stage 11; proposed
`NOT RATEABLE — non-effect estimand`).

Next: stage 3 — build the frame from anchor provenance, then the production query.
