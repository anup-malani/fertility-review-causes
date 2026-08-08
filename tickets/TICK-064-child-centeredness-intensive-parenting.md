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

**2026-08-08 (Shravan) — A3 anchors sourced and dual-gated.**
`source/build/goldset/103_d2d_cold_start_anchors.py` → 23 candidates, **20 verified live DOIs, 0
flagged, 3 monographs recorded unreachable**. Cells cover 4 empirical families (incl. one
`COST_INDEPENDENCE` candidate), the theory canon, the FDT context stream, and 7 routing decoys —
one per wall plus the reverse-causation decoy.

Proceeding on the Call 1 and Call 2 recommendations as instructed; PI confirmation still outstanding.

**The version-of-record problem is the DEFAULT for this canon, not a minority case.** D.2.d's core
sources are monographs, and the indexes return their *reviews*. Hays 1996 produces six review records
at Jaccard 1.00 and no monograph; Zelizer 1985 and Ariès 1962 the same. The first run of 103 resolved
all three to wrong records with full confidence — a book review, an unrelated MIT Press book, and a
Macat study guide *about* the book.

Three defects found in machinery inherited from `95_d1b`, each fixed and each independently load-bearing:

1. **`fallback` was a diagnostic being read as an answer.** When no candidate passes the gates the
   resolver returns the best-Jaccard row "so the caller can report the near-miss", but `main()`
   treated any dict carrying a DOI as a match. Hays's review is a perfect-title, one-year-off
   near-miss and was accepted as the monograph. Now flagged `is_fallback` and refused.
2. **The `year_drift` path took no author signal at all.** That is how Zelizer acquired Newhouse's
   *Pricing the Priceless* (MIT 2002) and Ariès a 2018 study guide.
3. **The book short-title probe could clear the ordinary Jaccard bar.** "Pricing the Priceless Child"
   vs "Pricing the Priceless" scores 0.75, above `TITLE_JACCARD_MIN`, so the author gate never ran.
   Book anchors now require a positive author match at any Jaccard.

**New capability: `_author_match`, three-state.** D.1.b has no author signal. Two
same-title-different-book collisions in a four-book canon are resolvable *only* by author — Lareau
2003's true UC Press record and Penn 2005's different book of the same name both score 0.29. The
lowered book title floor (0.25) is safe only because the author gate carries the discrimination.
Lareau and Doepke-Zilibotti are reachable **only** via this path; D.1.b's resolver would record both
as absent.

Note the two defenses are genuinely independent and neither is redundant: for Hays the author check
*passes* (the review credits Hays) and only the fallback flag rejects it; for Zelizer the fallback
flag never fires and only the author check rejects it.

**Also fixed: cache keys did not cover all inputs.** Authors became an input when `_author_match`
became a gate, so corrected author lists silently returned verdicts computed from the wrong ones —
four anchors kept reporting `author_match=False` after their names were fixed. Keys now include
author surnames and carry a semantic-version suffix.

**Own-process note:** four candidate author lists were asserted from memory and *all four were
wrong* (Rotkirch was attached to "Costly children"; she is actually on the housework decoy). The
script's own no-memory rule caught them via `auth=False`. Authors are now sourced from Crossref like
every other field.

**Substantive finding, before any screening spend:** `"intensive parenting" AND fertility` returns
**17 records in all of OpenAlex**; `"concerted cultivation" AND fertility` returns 3. The scope doc's
predicted thinness is confirmed in the index. `10.1016/j.worlddev.2025.107079` (World Development
2025, "How much do norms matter for quantity and quality of children?") is the strongest
`COST_INDEPENDENCE` candidate found and may be close to the only one.