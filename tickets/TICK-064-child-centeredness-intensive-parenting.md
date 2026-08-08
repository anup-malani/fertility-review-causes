# TICK-064: D.2.d Child-Centered Intensive Parenting Norms
**Status:** in-progress
**Assigned:** Shravan
**Hypothesis:** `child-centeredness-intensive-parenting` — HYPOTHESES-v5.md §D.2.d
**Parallel-safe:** yes
**Blocks:** none
**Blocked by:** none
**Touches:** literature/search-logs/child-centeredness-intensive-parenting-*, extraction/child-centeredness-intensive-parenting-*, output/chapters/child-centeredness-intensive-parenting.md

## Acceptance criteria
- [x] 2. Search strategy and scope drafted
- [ ] 3. Literature search and AI screening, both phases (§5.1)
- [ ] 4. RA title/abstract review
- [ ] 5. Full-text retrieval
- [ ] 6. Full-text screen, RA spot-checks 5–10%
- [ ] 7. Extraction to `extraction/child-centeredness-intensive-parenting.csv`, RA verifies a random 10%
- [ ] 8. Risk-of-bias assessment per study
- [ ] 9. Meta-analysis if ≥3 extractable effects, narrative synthesis otherwise
- [ ] 10. Demographic significance against PM / FDT / SDT
- [ ] 11. GRADE rating, 3 independent raters
- [ ] 12. Chapter draft on the §6 template
- [ ] 13. RA lay-readability check
- [ ] 14. PI review and sign-off

## Log

**2026-08-08 (Shravan) — A1/A2 scope drafted.** `literature/search-logs/child-centeredness-intensive-parenting-search-scope.md`.
Built on the D.3.b template, per PI-adjacent instruction to mirror that run.

- Six boundary walls specified: C.3.d (quantity-quality), C.2.f (inequality/status competition),
  C.2.b (direct costs), C.2.e (female wage/time price), C.2.a (childcare), D.2.a (gender equity).
  All six discriminate on the estimate's *source of variation*, not on framing.
- D.3.b's wave-1 audit fixes inherited at v1 rather than rediscovered: `INSUFFICIENT_INFO`,
  `OFF_OTHER`, and theory split into construct vs. normative-argument cells.
- New this run: an explicit **screen-enforceability table**. Four of the six walls cannot be
  adjudicated from a title/abstract, so records turning on them take `ROUTING_DEFERRED_TO_FULLTEXT`
  instead of a substantive `OFF_*` label. This is the D.3.b Wall 1 lesson pre-committed rather than
  discovered at the RA gate.
- New this run: the anchor audit carries **both** the OAS existence gate and the D.1.b
  version-of-record gate. D.2.d's canon is monographs (Hays, Lareau, Doepke-Zilibotti), which
  resolve to reviews, editions, and chapters more readily than articles do.
- Identification caution rewritten for this hypothesis: the first-order threat is **reverse
  causation, partly mechanical** (time per child is a quantity over parity), not the confounding
  that dominated D.3.b.

**Three scope calls raised, with recommendations — walls NOT yet frozen:**
1. FDT sentimentalization literature (Zelizer, Ariès). *Recommended:* context stream only, never
   pooled — a full FDT cell would duplicate C.3.a and C.3.b.
2. Doepke-Zilibotti joint claims (inequality → parenting style → fertility). *Recommended:* D.2.d
   claims the estimate only where the parenting-style link is isolated from the inequality/returns
   shock. Consequence stated in advance: D.2.d may end with very few identified estimates.
3. C.2.f and D.2.d are near-duplicates *as written in v5* — C.2.f's notes describe D.2.d. Wall 2 is
   a workable operational line, but the v5 entries should be re-worded. Flagged for TICK-001; does
   not block this run.

Anchor sourcing (A3) is not blocked by the freeze. Script numbering starts at 103 (88 is the highest
on `main`; D.1.b holds 95-102 on an unmerged branch).