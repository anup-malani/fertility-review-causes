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

**2026-08-08 (Shravan) — A4 frame builder written, BLOCKED, not run.**
`source/build/goldset/104_d2d_tier_ab_frame.py`. Mirrors `96_d1b_tier_ab_frame.py`. **No Tier A or
Tier B output exists yet** — the run aborts for want of an OpenAlex key and writes nothing.

**Blocker: `.env` was deleted during the key rotation and the new key is nowhere the scripts look**
(not in `.env`, not in the shell environment). The shared anonymous budget is exhausted
(`$0 remaining, resets at midnight UTC`). Drop the rotated key into `.env` — now gitignored — and
re-run; cached responses are reused so the run resumes rather than restarting.

**New guard: hard stop on budget exhaustion.** OpenAlex answers an out-of-budget request with HTTP
200 and a JSON error body. The inherited `get_json` refuses to cache it and `main()` records the
anchor as deferred — correct for a transient fault, wrong for this one, because a budget error
persists for hours (retryAfter ~26,000s observed). Every anchor would defer in turn and the run
would finish "successfully" with a near-empty Tier B. `BudgetExhausted` now aborts on first
occurrence and writes nothing.

This was not hypothetical. While preparing A4, a keyless probe of the three monograph titles returned
budget errors that the calling script rendered as "(no results)", and **Hays, Lareau and Zelizer were
nearly recorded as absent from OpenAlex when the query had never run** — the UNCONFIRMED-vs-ABSENT
confusion, reappearing one layer up in the caller rather than in the resolver. Caught by re-verifying.

**Known loss to carry into the log:** Hays 1996, Zelizer 1985 and Ariès 1962 have no DOI (A3) and the
book-shape rule refuses to resolve them by title, because a monograph's top title match is its own
review and a review's reference list and citation cloud are not the book's. Three of the four central
theory anchors therefore seed no part of Tier B. Lareau and Doepke-Zilibotti do resolve, via the DOIs
the A3 author gate recovered.

**Forward-seed policy loosened relative to D.1.b** (12 pages, cap 1,000 vs 10/600). Different reason,
not carelessness: Caldwell's forward cloud is all of demography, whereas Lareau and Doepke-Zilibotti
are cited *by* the intensive-parenting literature, so forward citation is doing most of the discovery
work here — the estimand-level query reaches only 17 records in the whole index. Against that, the
predicted `OFF_OUTCOME` flood lives in exactly those clouds, so the cap is loosened rather than
removed, and every excluded seed is logged with its count.

**2026-08-08 (Shravan) — A4 frame built.** Key restored to `.env`; run completed, 0 deferred.

- Anchors resolved **20/23**; the 3 unresolved are Hays, Zelizer, Ariès, refused by the book-shape
  rule as predicted. They seed nothing.
- **Tier A = 7** empirical seeds: NORM_EXPOSURE 2, TIME_INTENSITY 2, PERCEIVED_STANDARD 2,
  COST_INDEPENDENCE 1.
- **Tier B = 1,772** deduplicated candidates (forward 967, backward 791, both 14; 1,265 with usable
  abstracts, 507 without). 14 forward pages, no seed hit the 12-page cap.
- Forward-seeded 12 anchors; excluded 8 — 7 routing decoys plus Lareau (cb=2,172 > cap).

**The forward-cap rationale I wrote was wrong, and the run measured it.** I loosened D.1.b's 10/600
to 12/1,000 arguing that Lareau's and Doepke-Zilibotti's forward clouds are on-topic. Measured share
of citing works mentioning fertility / family size / childbearing:

| seed | citing | on-topic | % |
|---|---|---|---|
| Lareau, *Unequal Childhoods* | 2,169 | 23 | 1.1% |
| Doepke-Zilibotti, *Parenting With Style* | 345 | 12 | 3.5% |
| Ishizuka, *Parenting Standards* | 288 | 18 | 6.2% |
| Ramey & Ramey, *The Rug Rat Race* | 187 | 26 | 13.9% |

The theory canon's clouds are overwhelmingly `OFF_OUTCOME`, as the scope doc predicted. The cap made
the right call on Lareau for the wrong stated reason. Docstring corrected; threshold retained at
1,000 now that it is measured rather than guessed.

**Open design question — the decoy-exclusion rule is removing the highest-yield channel.** The two
most on-topic forward clouds in the whole anchor set belong to *routing decoys*, which the inherited
rule never forward-seeds:

| decoy | citing | on-topic | % |
|---|---|---|---|
| Becker & Lewis 1973 (Wall 1, C.3.d) | 505 | 256 | **50.7%** |
| Lawson & Mace 2009 (REVERSE) | 197 | 58 | **29.4%** |

The rule exists so a decoy does not import its neighbour's literature. But Tier B is a frame *to be
screened*, route-away material is expected in it, and these two clouds are concentrated exactly where
Wall 1 and the reverse-causation threat need adjudication — the chapter's hardest routing calls.
Seeding them would add ~700 records, ~314 on-topic. `seed_ids` provenance is already recorded, so
Recall(B) can be computed with and without them as a sensitivity check.

Not actioned — this changes the frame materially and is a methods call, not an implementation detail.
Note what is *not* an option: filtering the forward fetch by fertility vocabulary would prune Tier B
by distance from the production query and bias Recall(B). On-topic fraction is a seed-selection
diagnostic only, never a filter on the frame.

**2026-08-08 (Shravan) — A4 re-run with routing decoys forward-seeded.** Blanket decoy exclusion
dropped; rule is now uniform (empirical seeds always forward-cite; every other seed forward-cites
unless its cloud exceeds `FWD_CLOUD_CAP`). No decoy special case in either direction.

Measured on-topic share of each decoy's citing works before changing anything — six of seven are far
denser in on-topic material than the theory canon (1.1–13.9%):

| decoy (wall) | citing | on-topic | % |
|---|---|---|---|
| Hazan & Zoabi (Wall 2, C.2.f) | 178 | 157 | **88.2%** |
| Miettinen et al. (Wall 6, D.2.a) | 36 | 31 | **86.1%** |
| Ishchanova (Wall 5, C.2.a) | 3 | 2 | 66.7% |
| Becker & Lewis (Wall 1, C.3.d) | 505 | 256 | 50.7% |
| Butz & Ward (Wall 4, C.2.e) | 13 | 6 | 46.2% |
| Lawson & Mace (REVERSE) | 197 | 58 | 29.4% |
| OECD (Wall 3, C.2.b) | 2 | 0 | 0.0% |

Not an accident of this anchor set: a decoy is *chosen* to sit just across a boundary wall, so its
citation neighbourhood is where the boundary cases live — and boundary cases are what the six walls
exist to adjudicate. The inherited rule left Tier B systematically thin in the papers hardest to route.

**Result:** Tier B **1,772 → 2,677**; forward-seeded anchors 12 → 19; both-channel 14 → 20; usable
abstracts 1,265 → 1,881; forward pages 14 → 23. Lareau is now the only forward-excluded anchor.
**1,090 records (41% of the frame) depend on a decoy seed** by one channel or the other — that is
the set to toggle for the Recall(B) sensitivity check, and `seed_ids` provenance makes it a filter
rather than a re-run.

**Process note, second in a row:** I proposed seeding two decoys based on the two I had happened to
measure. Measuring all seven showed the highest-yield one (Hazan & Zoabi, 88.2%) was not among them.
Both forward-seed parameters on this chapter were first set by intuition and then corrected by a
measurement that cost about a cent. Measure the seeds before setting the policy, not after.
