# TICK-037: B.1 chapter finalization and PI review
**Status:** awaiting PI review (RA work complete)
**Assigned:** any
**Parallel-safe:** no
**Blocks:** none
**Blocked by:** TICK-036
**Touches:** output/chapters/evolutionary-sex-drive-contraceptive-decoupling.md, output/chapters/evolutionary-sex-drive-contraceptive-decoupling-pi-review v1.md

## Description

Fold the pooled status-fertility estimate, risk-of-bias ratings, and demographic-significance table into
the reader-facing chapter, then run the PI-review cycle as with OAS (v1..vN benchmark files). The
reader-facing draft already exists (2026-07-22) in the OAS final template; this ticket replaces its two
pending placeholders (the Section 6 pooled paragraph and the risk-of-bias summary) with extracted
results and takes the chapter through Anup's review.

## Acceptance criteria
- [x] Section 6 pending paragraph replaced with the project-native pooled estimate from TICK-035.
- [x] Risk-of-bias summary (Section 9) reflects the TICK-034 ratings.
- [x] Demographic-significance verdicts (Section 7, 10.1) reconciled with the TICK-036 table.
- [x] chapter-writing-style-guide.md and stop-slop pass re-run after the numbers land.
- [x] PI-review packet created; the honest verdict (distinctive decoupling claim unidentified) is preserved.
- [ ] Anup's review returned and v1 responses applied. **This is the remaining step and it is not RA work.**

## Log
**2026-07-25 RA work complete; chapter is review-ready.**

Chapter changes: draft-status line flipped to review-ready; Section 1 verdict table SDT row sharpened;
Section 6 third caution added on unequal sample sizes and the verification pass rewritten now that it is
done; Section 7.1 qualified by the k=1 and regime-versus-date caveats; Section 7.2 timing argument
rewritten to lead with the derived in-window fact; Section 7.3 given the new magnitude paragraph;
Sections 10 and 10.1 reconciled with the generated verdict table; Section 12 third extension rewritten
now that the meta-analysis exists; appendix updated.

Three appendix paths were wrong and are fixed: the cold-start anchors, screen rubric, and tier files
live under `literature/search-logs/`, not `output/`. Every path in the appendix now resolves on disk.
Stop-slop clean: 0 prose em-dashes in both chapter and packet.

**PI review packet:** `output/chapters/{slug}-pi-review-packet.md`, with six numbered decisions and a
recommendation on each. Two robustness checks were run specifically for it:

1. *Weighting.* The open worry that Hopcroft 2018's 313,405 observations would dominate is resolved by
   the specification already in use. Under fixed effects it would carry 94.6% of the male-cell weight;
   under random effects with tau-squared 0.0034 it carries 23.2%, and all five weights fall between 12%
   and 23%.
2. *Leave-one-out.* Point estimates are stable (male +0.065 to +0.113, female -0.102 to -0.163, no sign
   flips), but statistical significance in each cell rests on one study: dropping Hopcroft 2018 puts the
   male CI at -0.004 to 0.196, and dropping Hopcroft 2015 puts the female CI at -0.236 to 0.005. The
   chapter's "consistent direction, not a precise magnitude" wording is the right one.

Also surfaced for the packet: the contraception absent-versus-present contrast is +0.19 (k=1) against
+0.071 (k=4), directionally exactly as predicted. The chapter currently withholds it as underpowered.
DECISION 3 asks whether to report it descriptively instead; my recommendation is to report it with the
k=1 caveat, since withholding the one contrast favorable to the hypothesis reads worse than reporting a
weak one honestly.
