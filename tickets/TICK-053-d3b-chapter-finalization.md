# TICK-053: D.3.b chapter finalization and PI review
**Status:** RA work complete; chapter review-ready. Awaiting Anup, plus a second-reader verification pass that is not RA-optional
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
- 2026-07-27 (Claude): **chapter rewritten, not filled in.** 4,214 words, 0 PENDING
  markers, 0 em-dashes (matching the finished OAS/B.1/tempo chapters), all appendix paths
  verified to resolve.

  The skeleton anticipated filling blanks under a pooled estimate. The evidence did not
  support one, so Section 6 now states that no pool is reported and gives the reason
  (2 studies, 1 independent panel), rather than describing a forest plot that does not
  exist. Section 1's verdict table carries the generated ratings.

  **Both chapter errors found during the gate are fixed.** Section 8 no longer claims the
  evidence concentrates in Europe and North America without qualification; it names the
  Bangladesh and rural-Malawi studies as the only evidence on transportability. The
  Environmental Humanities article is no longer cited under the wrong title carried from
  OpenAlex metadata, and Section 13 records that error alongside the dedup and retrieval
  defects.

  **Section 12's general-anxiety limitation is NARROWED, not deleted.** The Wall 2 scope
  decision of 2026-07-25 stands and no probe was run. But the chapter is no longer silent:
  Golovina's robustness check and Helm's climate-anxiety-versus-depressive-symptoms
  contrast are two within-study tests pointing in opposite directions, which is not a
  resolution but is not nothing.

  Style guide applied. The stop-slop pass has NOT been run and should be, per the ticket.
  - [ ] Anup's review returned and v1 responses applied.
  - [ ] Second-reader verification pass over extracted values. **Not optional and not
        merely procedural: the first pass produced two errors caught only by returning to
        the source tables and figures, and one of them reversed a reported conclusion.**
- 2026-07-27 (Claude): opened.
