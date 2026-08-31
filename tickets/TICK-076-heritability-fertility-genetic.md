# TICK-076: A.18 Genetic and Heritable Variation in Fertility
**Status:** in-progress
**Assigned:** Shravan
**Hypothesis:** `heritability-fertility-genetic` — HYPOTHESES-v5.md §A.18
**Parallel-safe:** yes
**Blocks:** none
**Blocked by:** none
**Touches:** literature/search-logs/heritability-fertility-genetic-*, extraction/heritability-fertility-genetic-*, output/chapters/heritability-fertility-genetic.md

## Acceptance criteria
- [x] 2. Search strategy and scope drafted — `literature/search-logs/heritability-fertility-genetic-search-scope.md` (2026-08-31). **Not frozen:** 5 rulings pending PI, of which 2 and 4 block stage 3.
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
