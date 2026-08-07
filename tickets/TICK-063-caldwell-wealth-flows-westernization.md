# TICK-063: D.1.b Cultural Westernization and Developmental Idealism
**Status:** in-progress
**Assigned:** Shravan
**Hypothesis:** `caldwell-wealth-flows-westernization` — HYPOTHESES-v5.md §D.1.b
**Parallel-safe:** yes
**Blocks:** none
**Blocked by:** none
**Touches:** literature/search-logs/caldwell-wealth-flows-westernization-*, extraction/caldwell-wealth-flows-westernization-*, output/chapters/caldwell-wealth-flows-westernization.md

## Acceptance criteria
- [x] 2. Search strategy and scope drafted — `{slug}-search-scope.md`; six boundary walls **FROZEN** 2026-08-07, both scope calls approved
- [ ] 3. Literature search and AI screening, both phases (§5.1) — A3 anchors and A4 frame done (Tier A 14, Tier B 4,701); D1 ranking and the blinded screen outstanding
- [ ] 4. RA title/abstract review
- [x] 5. Full-text retrieval — 17/88 (19%); **retrieval-bound**, 43 closed + 28 blocked handed off
- [x] 6. Full-text screen — all 17 read and adjudicated; 6 overturned, primary cells 9→3
- [x] 7. Extraction — `extraction/{slug}-fulltext-adjudication.csv`; second-reader pass outstanding
- [x] 8. Risk of bias — 3 surviving studies: 2 serious, 1 critical
- [x] 9. Synthesis — narrative; no pool possible (one study at each of three outcome levels)
- [x] 10. Demographic significance — **not identified** for both live phenomena; no share computed, and why
- [~] 11. GRADE — very low for both live phenomena, **single-rater**; 3-rater panel outstanding
- [x] 12. Chapter draft — `output/chapters/{slug}.md`, INTERIM status
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

### 2026-08-07 (cont.) — A4 frame built

`source/build/goldset/96_d1b_tier_ab_frame.py` → Tier A **14 empirical seeds** across all five cells
(DI belief 5, media 3, Western contact 3, schooling-ideational 2, diffusion-independent-of-structure 1);
Tier B **4,701 deduplicated candidates**, 3,123 with usable abstracts, 44 found by both channels, 0
deferred. For comparison, D.3.b's frame was 1,170. The records found by both channels are almost
entirely the developmental-idealism literature, which is the signal that the anchors and walls are
aimed correctly.

**Blocker found and cleared: OpenAlex authentication.** The build first died on
`Insufficient budget ... Resets at midnight UTC`, and before that presented merely as everything being
slow, because the retry loops sat through full curl timeouts. Cause: the goldset scripts send
`mailto=` only, which identifies the caller but does not authenticate, so they draw on a shared
anonymous daily budget. **A funded `OPENALEX_API_KEY` has been sitting in `.env` unused the whole
time.** Wired into script 96 via `_openalex_key()` (env first, then `.env`; never inlined, never in a
cache filename or an exception message). *The older goldset scripts still have this bug, and this is
very likely the real cause of the D.1.a blocker recorded as "OpenAlex canon resolution now unusable"
— worth re-testing TICK-062 before treating it as blocked.*

Also: **`.env` was not gitignored.** Fixed. A live API key was sitting one `git add .` away from a
public commit.

**The version-of-record problem recurred at A4**, which is the more useful half of the finding.
Stage A4 resolves anchors again, in OpenAlex, and its title path was still an argmax — so Caldwell
1982 resolved to the 1983 PDR review of the book at similarity 1.0. OpenAlex has no record for the
monograph at all: only a review stub, typed `article`, with **zero** referenced_works and the book's
**1,338 citations attributed to it**. The frame log therefore reported a resolved anchor with a
citation count in the thousands that contributed nothing to Tier B, and no count would have exposed
it — an anchor with an empty reference list looks the same as one whose references were already in
the frame. Fixed by carrying `is_book` from A3 into A4. A resolution rule has to hold at every stage
that resolves; fixing it where it was found leaves it live everywhere else.

**Next:** D1 ranking and the blinded title/abstract screen over the 4,701-record frame.
### 2026-08-07 (cont.) — interim chapter on the retrieved 17

Retrieval reached 17 of 88 (19%). All 17 read at full text and adjudicated
(`extraction/{slug}-fulltext-adjudication.csv`). Three findings:

1. **Primary cells 9 → 3 on reading; 67% overturn.** Five of the six overturns are one
   mistake repeated: the screen treated an exposure that COULD carry Western family
   content -- a television, a migration, a development programme -- as though it did.
   Electrification delivers TV access but does not establish what was watched. This is
   what the walls were written to prevent and what an abstract cannot enforce.
2. **The value-added cell is empty.** Its one retrieved record is a calibrated structural
   model, not an empirical design separating ideation from structure.
3. **0 of 8 schooling papers decompose their mechanism.** The screen's 92% upper bound
   did not come down on full-text reading. Cummins 2025 cites Caldwell 1980 by name and
   still does not separate his mechanism from opportunity cost.

Surviving evidence: three studies at three different outcome levels, so no pooling is
arithmetically possible. The one direct contextual test on births (Kravdal 2000,
Zimbabwe) is a null -- and its residual confounding runs in the hypothesis's favour, so
the null is worth more than its risk-of-bias rating suggests.

Verdict: very low / not identified for both live phenomena. "Not identified" rather than
"not significant" -- the mechanism has barely been tested in a way that could reveal its
size.

**Still open:** 58 unscreened batches; 43 closed + 28 blocked retrievals (a bounded
library task, same trip as TICK-041); second-reader pass on the adjudications; 3-rater
GRADE.
