# TICK-089: D.2.c Son Preference and Gender-Biased Fertility Norms
**Status:** open
**Assigned:** Shravan
**Hypothesis:** `son-preference-cultural` — HYPOTHESES-v5.md §D.2.c
**Parallel-safe:** yes
**Blocks:** none
**Blocked by:** none
**Touches:** literature/search-logs/son-preference-cultural-*, extraction/son-preference-cultural-*, output/chapters/son-preference-cultural.md
**Selected by:** `427_selection_completeness_rerank.py` — `literature/search-logs/selection-completeness-rerank-2026-09-18.md`. Smallest candidate at a **corrected frame of 2,183**, on the first run in which every candidate that could still win was corrected by one rule: A.3 2,324, C.3.a 3,847 (strict) / 9,290 (broad), D.2.c 2,183. Everything from C.2.e (2,240) up is excluded without measurement — correction is monotone, so a frame already above 2,183 uncorrected cannot win. D.2.c won because its registered frame was nearly honest to begin with: +9% under correction, against +223% for A.3 and +113% for C.3.a.
**Why it is not only the smallest:** A.6 was chosen on size alone and produced an UNEVALUATED verdict on one contestable record. D.2.c is the best of the three on the other two axes too — **83** in-frame records carry an identified-design marker against A.3's 32 and C.3.a's 38, and homonym load is **43 of 2,183 (2%)** against A.6's 240 of 680 (35%). It is the first candidate in this block that is cheap to screen *and* likely to yield an estimable parameter.
**Scope hazard 1 — the claim is two claims, and the second one cancels the first.** §D.2.c registers a fertility-raising mechanism (continued childbearing until a son is born) *and* a substitution that partly defuses it (sex-selective abortion). A single pooled estimate over both is not this hypothesis's parameter. Stage 2 must split the estimand before any screening: the stopping-behaviour effect on realized fertility, and the availability-of-sex-selection interaction that attenuates it. `differential stopping` and `sex-selective abortion` were both already in the selecting frame, so the pool will contain both literatures mixed.
**Scope hazard 2 — three phenomena, and this is the first candidate registered for all of PM, FDT and SDT.** Every hypothesis worked since TICK-069 has been registered for one or two. The registry note says the effect is "quantitatively large in South/East Asia; eroded by sex-selective abortion in SDT settings", which is a phenomenon-varying sign, not a phenomenon-varying magnitude. Demographic significance (stage 10) has to be computed three times against PROTOCOL §4.2.1's denominator, and the PM arm has no obvious dose series.
**Scope hazard 3 — two walls with started chapters, one of them cited by the registry itself.** A.10 (`sex-ratio-marriage-market`, TICK-054, search scope drafted and PARKED pending Anup) is named in §D.2.c's own cross-ref as "one consequence", and `304` measured the pair at 17 records. C.3.c (`old-age-security-pension-crowdout`, a written chapter) is the registry's named *motivation* for son preference. A.10's scope doc is inheritable rather than absent, which is the first time a wall on a new chapter has had one — use it instead of defining the wall from scratch.

## Acceptance criteria
- [ ] 2. Search strategy and scope drafted
- [ ] 3. Literature search and AI screening, both phases (§5.1)
- [ ] 4. RA title/abstract review
- [ ] 5. Full-text retrieval  <!-- sub-ticket if it blocks on library access -->
- [ ] 6. Full-text screen, RA spot-checks 5–10%
- [ ] 7. Extraction to `extraction/son-preference-cultural.csv`, RA verifies a random 10%
- [ ] 8. Risk-of-bias assessment per study
- [ ] 9. Meta-analysis if ≥3 extractable effects, narrative synthesis otherwise
- [ ] 10. Demographic significance against PM / FDT / SDT
- [ ] 11. GRADE rating, 3 independent raters
- [ ] 12. Chapter draft on the §6 template
- [ ] 13. RA lay-readability check
- [ ] 14. PI review and sign-off

## Log
