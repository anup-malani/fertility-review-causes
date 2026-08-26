# TICK-073: C.3.g Student Debt and Household Formation Constraint
**Status:** in-progress
**Assigned:** Shravan
**Hypothesis:** `student-debt-household-formation` — HYPOTHESES-v5.md §C.3.g
**Parallel-safe:** yes
**Blocks:** none
**Blocked by:** none
**Touches:** literature/search-logs/student-debt-household-formation-*, extraction/student-debt-household-formation-*, output/chapters/student-debt-household-formation.md, source/build/goldset/199*

## Acceptance criteria
- [x] 2. Search strategy and scope drafted — DRAFT 2026-08-26, not frozen (Calls 1 and 5 open)
- [ ] 3. Literature search and AI screening, both phases (§5.1)
- [ ] 4. RA title/abstract review
- [ ] 5. Full-text retrieval
- [ ] 6. Full-text screen, RA spot-checks 5–10%
- [ ] 7. Extraction to `extraction/student-debt-household-formation.csv`, RA verifies a random 10%
- [ ] 8. Risk-of-bias assessment per study
- [ ] 9. Meta-analysis if ≥3 extractable effects, narrative synthesis otherwise
- [ ] 10. Demographic significance against PM / FDT / SDT
- [ ] 11. GRADE rating, 3 independent raters
- [ ] 12. Chapter draft on the §6 template
- [ ] 13. RA lay-readability check
- [ ] 14. PI review and sign-off

## Log

### 2026-08-26 — Stage 2 (scope), drafted

Two probes, 71 requests, 0 failures. The frame is 394 records and can be screened whole.
Structural finding: the identified variation (210 records) and the registered outcome do not
intersect — student debt x fertility x identification is 2 records, neither an estimate, and the
policy-variation cell (forgiveness, repayment reform, tuition regime) is measured EMPTY. The
identified body sits on marriage, homeownership and co-residence, which v5's own claim names as the
mechanism, so the chapter is a two-arm chain chapter: arm 1 direct and associational (rated), arm 2
identified on link 1 with link 2 borrowed from A.7/A.23/C.2.c (a bound, not pooled).

Also found: a shared-resolver defect (an apostrophe-bearing word in a `title.search` query returns a
confident WRONG match at n=1, not a zero), and v5's C.3.g seminal list does not resolve at all.
