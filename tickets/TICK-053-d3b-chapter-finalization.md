# TICK-053: D.3.b chapter finalization and PI review
**Status:** open
**Assigned:** any
**Parallel-safe:** no
**Blocks:** none
**Blocked by:** TICK-052
**Touches:** output/chapters/climate-anxiety-eco-doomerism.md, output/chapters/climate-anxiety-eco-doomerism-pi-review-packet.md

## Description

Convert the structural skeleton into a full chapter by replacing every PENDING slot with an extracted
result, then run the PI-review cycle as OAS and B.1 did (v1..vN benchmark files).

The skeleton was written so this step is mechanical rather than interpretive: Sections 3, 4, 5, 13 and
the evidence-base counts are already real, and Sections 1, 6, 7, 9, 10 plus every rating are
placeholders that each state what will be decided and on what evidence. The work is filling them, and
removing the reading note at the top once nothing PENDING remains.

Specific slots, in the order the skeleton lists them:

- **§1 Verdict** — the four-row phenomenon table. The two "Not applicable" rows stay as they are; the
  SDT stated-intention and SDT desire-independence rows take generated ratings from TICK-052.
- **§5.1, §5.2, §5.3** — the PENDING extraction notes replaced with what extraction found; the 5.2
  table gains extracted effects; the 5.3 question ("does any of the four in fact hold desire fixed")
  answered from the TICK-049 field.
- **§6 Quantitative synthesis** — currently PENDING in full; takes both tracks from TICK-051 with the
  no-combined-estimate rule visible in the prose, not just honored in the tables.
- **§7 Demographic significance** — from TICK-052.
- **§9 Risk of bias** — the three named risks converted from anticipated to assessed, from TICK-050.
- **§10 and §10.1** — the summary table and the GRADE rating, reconciled against the generated verdict
  table rather than typed.
- **§11 and §12** — the interpretation and limitations sections currently forecast their own results
  ("is PENDING", "limitations are known before its results are"); rewrite in the past tense now that
  the results exist.
- **§13** — the "Pending before this chapter is anything more than a skeleton" paragraph replaced with
  what was actually done, including the TICK-047 gate overturn rate and the TICK-048 retrieval rate.
- **Draft-status line and the reading note** — flipped to review-ready and removed respectively.

The Wall 2 scope decision (Shravan, 2026-07-25) stands: the general-anxiety probe is **not** planned,
§12 keeps its interpretive limit, and §13 keeps it under "Not planned". Do not reopen it during
finalization.

Run `chapter-writing-style-guide.md` and the stop-slop pass **after** the numbers land, per TICK-046.

## Acceptance criteria
- [ ] Every PENDING marker in the chapter resolved or explicitly converted to a stated limitation.
- [ ] Ratings taken from the TICK-052 generated verdict table, not hand-entered.
- [ ] Reading note removed and draft-status line flipped to review-ready.
- [ ] Appendix paths verified to resolve (three were wrong in B.1 and only caught at finalization).
- [ ] Style guide + stop-slop pass re-run after the numbers land.
- [ ] PI-review packet created with numbered decisions for Anup, preserving the honest verdict —
      including, if it holds, that the distinctive desire-independence claim is unidentified.
- [ ] Anup's review returned and v1 responses applied. *(Not RA work; the ticket stays open until it
      comes back.)*

## Log
- 2026-07-27 (Claude): opened.
