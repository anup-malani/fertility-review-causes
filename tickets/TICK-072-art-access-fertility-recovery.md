# TICK-072: A.17 Assisted Reproductive Technology Access
**Status:** in-progress
**Assigned:** Shravan
**Hypothesis:** `art-access-fertility-recovery` — HYPOTHESES-v5.md §A.17
**Parallel-safe:** yes
**Blocks:** none
**Blocked by:** none
**Touches:** literature/search-logs/art-access-fertility-recovery-*, extraction/art-access-fertility-recovery-*, output/chapters/art-access-fertility-recovery.md, source/build/goldset/185*

## Acceptance criteria
- [x] 2. Search strategy and scope drafted — `literature/search-logs/art-access-fertility-recovery-search-scope.md` (DRAFT, 8 walls / 6 cells / 5 PI calls; not frozen, Calls 2-3 change the frame)
- [x] 3. Literature search and AI screening, both phases (§5.1) — A3 anchors 21/23 (`187_`); A4 frame 7,589 records (`188_`); D1 ranked 7,313, worklist 1,020 (`189_`); D2 screen complete, 192 RELEVANT / 212 UNCERTAIN / 616 NOT_RELEVANT (`190_`, `191_`)
- [ ] 4. RA title/abstract review — **stratify the spot-check on `no_abstract`**: the screen's title-only safeguard was measured inert (0 of 234 routed to INSUFFICIENT_INFO)
- [ ] 5. Full-text retrieval — **PARTIAL: 33/131 automated (`192_`-`194_`). 67 are BLOCKED-BUT-OPEN (a browser, no proxy needed; URL list in `extraction/art-access-fertility-recovery-blocked-but-open.txt`) and 31 NO ROUTE (needs UChicago proxy). Job A1, the counterfactual set the headline number rests on, is 2 of 14 in hand**
- [ ] 6. Full-text screen, RA spot-checks 5–10% — **PROVISIONAL pass done on the 33 retrieved (`195_`, `196_`). Arm 1: 9 of 14 report a contribution without confronting the counterfactual, 4 confront it. RE-RUN when the 67 blocked-but-open arrive; everything is keyed on the OpenAlex id and skips completed work.**
- [x] 7. Extraction — `extraction/art-access-fertility-recovery-fulltext-screened.json` (33 records, arm/counterfactual/quantity). **RA 10% verification outstanding; stratify on `no_abstract`**
- [x] 8. Risk of bias — `extraction/art-access-fertility-recovery-risk-of-bias.csv` (`198_`). Separate instruments per arm; A1.4 postponement-feedback SERIOUS on all 14 arm-1 records
- [x] 9. Narrative synthesis — **no pooling, by ruling**: the two arms do not estimate the same parameter
- [x] 10. Demographic significance (`197_`) — SDT offset 2.7%–11.8% across five countries, verdict MINOR; PM and FDT NOT ASSESSED (technology did not exist)
- [ ] 11. GRADE — SDT **LOW** (3 downgrades named) in `198_`. **Rated by ONE rater; the 3-independent-rater requirement is OPEN**
- [x] 12. Chapter draft — `output/chapters/art-access-fertility-recovery.md`, INTERIM on 33/131 full texts. All seven mandatory sentences present
- [ ] 13. RA lay-readability check
- [ ] 14. PI review and sign-off

## Log
