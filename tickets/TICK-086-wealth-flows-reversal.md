# TICK-086: C.3.f Intergenerational Wealth Flows Reversal
**Status:** in-progress
**Assigned:** Shravan
**Hypothesis:** `wealth-flows-reversal` — HYPOTHESES-v5.md §C.3.f
**Parallel-safe:** yes
**Blocks:** none
**Blocked by:** none
**Touches:** literature/search-logs/wealth-flows-reversal-*, extraction/wealth-flows-reversal-*, output/chapters/wealth-flows-reversal.md, source/build/goldset/37[6-9]*, source/build/goldset/38*, source/build/goldset/304_candidate_frame_probe.py

## Acceptance criteria
- [x] 2. Search strategy and scope drafted — `literature/search-logs/wealth-flows-reversal-search-scope.md`, 2026-09-10. Direction ruling, 10 walls, estimand cells, required tags, pooling rule and the single demsig route frozen; 5 PI calls open. All 83 quoted figures asserted against their logs by `378`, verified to fire on three classes of mutation
- [ ] 3. Literature search and AI screening, both phases (§5.1)
- [ ] 4. RA title/abstract review
- [ ] 5. Full-text retrieval
- [ ] 6. Full-text screen, RA spot-checks 5–10%
- [ ] 7. Extraction to `extraction/wealth-flows-reversal.csv`, RA verifies a random 10%
- [ ] 8. Risk-of-bias assessment per study
- [ ] 9. Meta-analysis if ≥3 extractable effects, narrative synthesis otherwise
- [ ] 10. Demographic significance against PM / FDT / SDT
- [ ] 11. GRADE rating, 3 independent raters
- [ ] 12. Chapter draft on the §6 template
- [ ] 13. RA lay-readability check
- [ ] 14. PI review and sign-off

## Why this one now

Ranked by `source/build/goldset/304_candidate_frame_probe.py`, re-run 2026-09-10
(`literature/search-logs/candidate-frame-probe-2026-09-10.md`). Coverage arithmetic on the page: **61
live registry entries = 26 started + 1 excluded + 34 candidates measured.** Control (C.3.e, chapter
written) returned 85, so a zero anywhere below is literature and not a broken probe.

**Two candidates were still unranked, and measuring them is what made this ranking a whole set rather
than a subset.** C.4.a (narrow 1016) and D.2.c (narrow 1055) sat in the pass-1-only block with counts
*below* the incumbent union frame, so the corollary that retires a candidate on its narrow count
alone never reached them. Widened on a second vocabulary they come in at **C.4.a 2417** and **D.2.c
2024** — both above C.3.f and out of contention for now, but measured rather than assumed
(`candidate-list-is-itself-a-filter`).

**The three smallest union frames are A.6 680, A.3 727, C.3.f 1101, and the smallest again does not
win.** A.6's stigma-specific axis returns **12** records against its 680 union and A.3's core is
**26** of 727: both frames are loose general-purpose vocabulary rather than an anchored literature.
A.6 is by construction the residual left after A.2, A.4 and A.5, and A.3 is the Princeton project's
residual explanation; none of A.2, A.4, A.5 has a branch on `origin` (checked 2026-09-10), so both
would draw their walls unilaterally against three unstarted and much larger literatures. **This is
the third consecutive ranking in which A.6 and A.3 place first and are passed over** — TICK-081 and
TICK-083 made the same argument. They should be scheduled deliberately after A.2/A.4/A.5 rather than
deferred a fourth time; that is a PI call, recorded here as call 1.

**C.3.f's core is 367 of 1101 — an anchored literature**, the signature that made C.2.f preferable to
A.6 and C.3.d preferable to A.3.

**Its walls are already written, and the homonym pass says they barely touch it.** Measured inside
the fertility-restricted frame: the boundary against D.1.b (Cultural Westernization, drafted) is **1
record**, against C.2.b (price of children, drafted) **19**, against C.3.a (mode of production,
unstarted) **5**. The registry's claim that C.3.f and D.1.b are "complementary not redundant" holds at
the vocabulary level. The one real wall is **C.3.c old-age security at 162 records (15% of the
frame)** — and C.3.c is a *closed* chapter, so that wall is inherited rather than litigated.

**The homonym check ran this time, and it clears.** "Intergenerational transfer" is a public-finance
and behaviour-genetics word — 3,176 records unrestricted, 364 of them bequest-and-estate — but the
residue *inside* the fertility-restricted frame is **33 of 1101 (3.0%)**. "Wealth flows" is not a
finance term in practice: 237 unrestricted, 21 intersecting capital markets. The 09-09 run printed
this heading over an empty table because every row in it belonged to a started chapter; rows for the
live candidates were added before this ticket was opened.

**C.3.f is FDT-only** (registry §C.3.f), so stage 10 has one phenomenon to assess rather than three.

Open before stage 2: `value of children` alone is **515** of the 1101 frame — the Value-of-Children
survey tradition, a measurement literature rather than an identified-design one. Whether it is the
chapter's evidence or its background is the first scope ruling, and it is the reason the primary cell
could be thin. `empty-cell-is-the-result` applies if it is; `empty-cell-needs-second-channel` applies
before saying so.

## Log
