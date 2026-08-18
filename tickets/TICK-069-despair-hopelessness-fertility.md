# TICK-069: D.3.c Despair and Hopelessness
**Status:** in-progress
**Assigned:** Shravan
**Hypothesis:** `despair-hopelessness-fertility` — HYPOTHESES-v5.md §D.3.c
**Parallel-safe:** yes
**Blocks:** none
**Blocked by:** none
**Touches:** literature/search-logs/despair-hopelessness-fertility-*, extraction/despair-hopelessness-fertility-*, output/chapters/despair-hopelessness-fertility.md, source/build/goldset/147*

## Acceptance criteria
- [x] 2. Search strategy and scope drafted — **drafted, not frozen**; 5 PI calls, 2 load-bearing
- [ ] 3. Literature search and AI screening, both phases (§5.1)
- [ ] 4. RA title/abstract review
- [ ] 5. Full-text retrieval
- [ ] 6. Full-text screen, RA spot-checks 5–10%
- [ ] 7. Extraction to `extraction/despair-hopelessness-fertility.csv`, RA verifies a random 10%
- [ ] 8. Risk-of-bias assessment per study
- [ ] 9. Meta-analysis if ≥3 extractable effects, narrative synthesis otherwise
- [ ] 10. Demographic significance against PM / FDT / SDT
- [ ] 11. GRADE rating, 3 independent raters
- [ ] 12. Chapter draft on the §6 template
- [ ] 13. RA lay-readability check
- [ ] 14. PI review and sign-off

## Log

### 2026-08-18 — stage 2, scope drafted

**Result.** Reconnaissance (`source/build/goldset/147_d3c_recon_probe.py`, 60 probes, 0 failed) and a
scope document at `literature/search-logs/despair-hopelessness-fertility-search-scope.md`: ten
boundary walls, thirteen estimand cells, five PI calls.

Three findings changed the chapter's shape:

1. **The mechanism is not measured in the literature that studies its treatment.** Place-based decline
   AND fertility = 1,539. Despair vocabulary AND fertility = 604. All three legs together = **12**, and
   the twelve are noise apart from one book review of Case and Deaton. Same test on C.5.a: 3,120 falls
   to 20. The reduced-form literature never names the mechanism D.3.c is about.
2. **The sign is not given by the theory.** A foreclosed future is the standard explanation for
   *higher* early and nonmarital childbearing (Kearney-Levine, Edin-Kefalas, the West Virginia social-
   distress line). Same antecedent, opposite sign, different margin. Estimates now carry a mandatory
   `FERTILITY_MARGIN` tag and the opposite-sign cell sits in the primary synthesis.
3. **v5's Platt and Sterling seminal is a citation defect, not a ghost.** v5 cites a EurekAlert press
   release; the paper is Platt and Sterling (2024), *Nature Mental Health*, doi
   10.1038/s44220-024-00241-1. Recovered only by author-filtered probe — title search returns zero.
   Cherlin and Edin-Kefalas both resolve to reviews of themselves (book-canon resolver failure).

**Workflow impact.** A quoted search phrase whose first word is `not` is parsed by OpenAlex as a
boolean NOT, and the enclosing AND then returns the **unrestricted** count instead of erroring — the
contested-framework probe reported 831 where the truth is 113. The failure inflates, so it reads as a
large literature. Fixed in 147 with a comment at the site; a sweep of every `source/build/**/*.py` on
every branch found no other instance.

Script numbering starts at 147, above the max of 146 across all branches, not above main's max.

