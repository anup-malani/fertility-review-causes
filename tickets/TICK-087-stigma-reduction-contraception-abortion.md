# TICK-087: A.6 Reduction in Stigma Around Contraception and Abortion
**Status:** in-progress — resumed 2026-09-17 after `405` reversed the finding that parked this ticket. A.6 is the strict-smallest candidate on a like-for-like corrected comparison (1,225 v. A.3's 1,584–2,419). PI directed: proceed on A.6 and do not re-rank the rest of the block first.
**Assigned:** Shravan
**Hypothesis:** `stigma-reduction-contraception-abortion` — HYPOTHESES-v5.md §A.6
**Parallel-safe:** yes
**Blocks:** none
**Blocked by:** none
**Touches:** literature/search-logs/stigma-reduction-contraception-abortion-*, extraction/stigma-reduction-contraception-abortion-*, output/chapters/stigma-reduction-contraception-abortion.md
**Selected by:** `candidate-frame-probe-2026-09-13` — smallest union frame in the bracketed block at 680 (next: A.3 at 727). The narrow pass puts A.6 at 12, which is a lower bound and not comparable to the other block.
**Scope hazard:** three of A.6's boundaries are with *unstarted* candidates — A.4 (29 shared records), A.5 (81), A.2 (59). The usual move of citing the neighbouring chapter's scope doc is unavailable, so stage 2 has to define those three walls from scratch. `stigma` unrestricted is 202,130 records, so the 680 holds only as long as the bracketing does.

## Acceptance criteria
- [x] 2. Search strategy and scope drafted — `literature/search-logs/stigma-reduction-contraception-abortion-search-scope.md`, frozen 2026-09-17, six PI calls open, numbers asserted by `406`
- [ ] 3. Literature search and AI screening, both phases (§5.1)
- [ ] 4. RA title/abstract review
- [ ] 5. Full-text retrieval
- [ ] 6. Full-text screen, RA spot-checks 5–10%
- [ ] 7. Extraction to `extraction/stigma-reduction-contraception-abortion.csv`, RA verifies a random 10%
- [ ] 8. Risk-of-bias assessment per study
- [ ] 9. Meta-analysis if ≥3 extractable effects, narrative synthesis otherwise
- [ ] 10. Demographic significance against PM / FDT / SDT
- [ ] 11. GRADE rating, 3 independent raters
- [ ] 12. Chapter draft on the §6 template
- [ ] 13. RA lay-readability check
- [ ] 14. PI review and sign-off

## Log

**2026-09-17 — parked before stage 2, then RESUMED the same day. Read the resumption note at the end of this entry before acting on anything above it.**

*Result.* `404_a6_term_diagnostics.py` audited the frame that selected A.6 and it does not hold.
Two defects, the second decisive:

1. A.6's union frame is a **three-block conjunction** — stigma AND object AND outcome — where every
   other pass-4 candidate is a flat OR-list and therefore two-block once `304` applies the outcome
   axis (304:523). The 668 was never comparable to the 727 it beat.
2. The stigma block carries no form of **legitimation**, **normalisation** or **acceptability** —
   only the negative pole of a construct HYPOTHESES-v5 §A.6 defines as "cultural *legitimation* of
   contraception and abortion". Restoring the registry's own vocabulary: 668 → **1,225**. Adding
   `births` to the outcome axis: → **2,338**. Controls reproduce (A.3 719 v. 727 recorded, C.3.a
   1,808 v. 1,811), so this is a frame defect and not index drift.

On the corrected frame A.6 is not the smallest unstarted candidate. A.3 is, at 719, and TICK-088
was opened for it. This ticket is parked rather than closed: the hypothesis is still live and
unstarted, and everything measured here is inheritable when it reopens.

Two findings that survive the switch and should be read before A.6 is reopened:

- **The registered outcome is barely estimated.** 12 of 668 in-frame records carry an
  identified-design marker (1.8%); 189 carry qualitative markers (28%); only 58 carry
  realized-fertility vocabulary. Meanwhile 479 stigma-and-object records take *contraceptive use*
  as the dependent variable and are invisible to any fertility outcome axis. A.6's mechanism runs
  through use, so a fertility-framed search retrieves the minority of its own literature. The
  likely honest verdict is UNEVALUATED with the failed route named, not weak evidence
  (`empty-cell-is-the-result`).
- **Walls, measured from both sides** (frame 668): A.5 81 records — 12.1% of ours, 1.4% of theirs;
  A.2 60 / 9.0% / 1.1%; A.4 57 / 8.5% / 2.7%; B.5 51 / 7.6% / 0.3%; D.1.a 6 / 0.9% / 0.4%; A.3
  **2 / 0.3% / 0.4%** despite A.3 sharing two of A.6's four registered seminals (Cleland and
  Wilson 1987; Bongaarts and Watkins 1996). That is the C.3.d shape — vocabularies part while the
  construct does not — so the A.6/A.3 wall is adjudicable only at full text, and whichever chapter
  is written second inherits the obligation. HIV-stigma contamination inside A.6's own frame is
  148 records, 22%.

*Workflow impact.* The defect is generic, not specific to A.6: a candidate whose registered
construct has an **asymmetric vocabulary** — a well-named negative pole and an unnamed positive one,
or the reverse — will be under-framed by `304` and can win a ranking it does not deserve. `304`
prices candidate terms by marginal gain but never asks whether the registered *claim's own nouns*
are present in the block at all. Until that check is added to `304`, every frame it reports is a
lower bound of unknown tightness, and the two-block/three-block distinction should be recorded per
candidate so conjunction depth is visible in the ranking table. Raised as a PI call on TICK-088
rather than fixed here, since it is a `304` change and `304` belongs to TICK-080.

**2026-09-17 — resumed. The park was based on a comparison that was not like-for-like.**

`405` (TICK-088, branch `088-diffusion-of-fertility-control`, commit `23388fd`) applied this
ticket's own completeness test to A.3, the candidate that displaced A.6. A.3 fails it harder:
"legitimation" is in A.3's registered claim, absent from its pass-4 block, and worth **+865 records
alone** (719 → 1,584); all twelve terms A.3 owns give **2,419**.

Corrected, like for like:

| candidate | as probed | corrected |
|---|---|---|
| **A.6** | 668 | **1,225** |
| A.3 | 719 | 1,584 (legitimation only) – 2,419 (all own terms) |
| C.3.a | 1,808 | uncorrected |

So A.6 is the smallest of the two, the probe's original ordering was directionally right, and the
park rested on `404` correcting A.6 and then comparing the result against A.3's *uncorrected*
number. The error was in the application, not the test.

Two measured facts from `405` cut against A.6 on grounds other than size, and the chapter should
carry them rather than bury them: A.3's frame is nearly free of homonyms (7 / 1 / 7 / 8 records)
where A.6 carries **148** records of HIV-stigma and 92 of mental-illness stigma, 22% and 14% of its
frame; and A.3 has **154** in-frame records with realized-fertility vocabulary against A.6's **58**.
A.6 is cheaper to screen and less likely to yield an estimable parameter. That tension is a PI call
in the scope doc, not a reason to switch again — the PI has directed that work continue on A.6
regardless of whether other candidates are smaller.
