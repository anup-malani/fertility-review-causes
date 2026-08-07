# TICK-063: D.1.b Cultural Westernization and Developmental Idealism
**Status:** in-progress
**Assigned:** Shravan
**Hypothesis:** `caldwell-wealth-flows-westernization` — HYPOTHESES-v5.md §D.1.b
**Parallel-safe:** yes
**Blocks:** none
**Blocked by:** none
**Touches:** literature/search-logs/caldwell-wealth-flows-westernization-*, extraction/caldwell-wealth-flows-westernization-*, output/chapters/caldwell-wealth-flows-westernization.md

## Acceptance criteria
- [x] 2. Search strategy and scope drafted — `literature/search-logs/caldwell-wealth-flows-westernization-search-scope.md` (walls DRAFT, two calls open, see Log)
- [ ] 3. Literature search and AI screening, both phases (§5.1)
- [ ] 4. RA title/abstract review
- [ ] 5. Full-text retrieval
- [ ] 6. Full-text screen, RA spot-checks 5–10%
- [ ] 7. Extraction to `extraction/caldwell-wealth-flows-westernization.csv`, RA verifies a random 10%
- [ ] 8. Risk-of-bias assessment per study
- [ ] 9. Meta-analysis if ≥3 extractable effects, narrative synthesis otherwise
- [ ] 10. Demographic significance against PM / FDT / SDT
- [ ] 11. GRADE rating, 3 independent raters
- [ ] 12. Chapter draft on the §6 template
- [ ] 13. RA lay-readability check
- [ ] 14. PI review and sign-off

## Log

### 2026-08-07 — Phase A (instrument) built; two scope calls open

**Done.**
- Search scope and the six boundary walls drafted: `literature/search-logs/{slug}-search-scope.md`.
  D.1.b sits between C.3.f (wealth flows), D.1.a (postmaterialism), A.3 and A.20 (diffusion), D.2.a
  (female empowerment), C.3.b (compulsory schooling), and D.1.c (cultural evolution), and routing is
  the central screening task, as it was for B.1 and D.3.b.
- Blinded title/abstract screening rubric: `literature/search-logs/{slug}-screen-rubric.md`.
- Cold-start anchors sourced live and existence-verified: `source/build/goldset/95_d1b_cold_start_anchors.py`
  → `{slug}-cold-start-anchors.{json,md}`. 28 anchors: 12 empirical, 6 theory canon, 8 routing decoys
  (one per wall plus the FDT restriction), 1 contrary-evidence design, and 1 dual-home media case.

**Script numbering.** 89–94 are claimed by the D.1.a chain on `062-postmaterialism-individualism-secularization`,
which has not merged. D.1.b starts at 95. Checked with `git ls-tree` across all remote branches
before writing — the collision the QUEUE.md renumber note exists to prevent, caught in advance.

**Method finding, written up at `decisions/2026-08-07-version-of-record-gate.md`.** The inherited
existence gate passed 8 of 28 anchors at the WRONG VERSION of the right paper — NBER and IDB working
papers for Jensen & Oster and La Ferrara, a Research Square preprint for Okoye & Pongou, a 2024
reprint for Caldwell 1980, and a *Choice* review in place of Thornton's 2005 monograph. All passed at
title Jaccard 1.0, because a preprint's title is identical to the article's. The existence gate
catches titles that resolve to nothing; it cannot catch titles that resolve to the wrong real thing.
Resolver rewritten to rank candidates for version-of-record status. Proposed follow-up ticket: re-grade
the frozen OAS, B.1, and D.3.b anchor sets against the version gate, since none was built with one.

**Two scope calls — both APPROVED (Shravan, 2026-08-07). Boundary walls now FROZEN, all six hard.**
1. **The FDT cell is restricted to the diffused transition** — post-1945 societies entering transition
   under exposure to an external modern model. The historical Western FDT (1870–1930) is the *source*
   of the package, not a case of it. Declined alternative: carry it and treat westernization as
   within-Europe diffusion, which would make this chapter a near-duplicate of A.3 and hand it the
   Princeton corpus.
2. **Reduced-form schooling → fertility estimates stay out of the pool.** Most decompose no mechanism,
   so they are neither D.1.b nor C.3.b on their own evidence. They take
   `MECHANISM_UNRESOLVED_SCHOOLING` / `UNCERTAIN` and are reported as a count. Declined alternative:
   admit them and downgrade for indirectness at GRADE — that would let the best-identified literature
   in the review answer a question it was not designed to answer. The size of this class relative to
   the class that does decompose is expected to be the chapter's central honest number.

**A4 forward-citation policy, retuned from D.3.b's.** D.3.b was a five-year-old literature whose
forward clouds were small and whose cap was "retained for safety". D.1.b's canon is fifty years old
and among the most-cited in demography, and its two media quasi-experiments sit inside development
economics, so their forward clouds are broad rather than topical. At D.3.b's settings this step would
request on the order of 50,000 records. `MAX_FORWARD_PAGES` 20→10 and `FWD_THEORY_CAP` 1500→600;
backward references still taken from every resolved anchor, including the excluded theory ones.
Budget parameter, not a recall claim — if a primary cell comes back thin, raise the cap for that
cell's seeds and re-run.

**Next:** A4 Tier A/B citation frame (script 96), then the blinded screen.