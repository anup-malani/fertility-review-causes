# TICK-075: A.23 Co-Residence with Parents and Delayed Household Formation
**Status:** in-progress
**Assigned:** Shravan
**Hypothesis:** `co-residence-parents-household-delay` — HYPOTHESES-v5.md §A.23
**Parallel-safe:** yes
**Blocks:** none
**Blocked by:** none
**Touches:** literature/search-logs/co-residence-parents-household-delay-*, extraction/co-residence-parents-household-delay-*, output/chapters/co-residence-parents-household-delay.md

## Acceptance criteria
- [x] 2. Search strategy and scope drafted (DRAFT, not frozen — Wall 1 second read open)
- [x] 3. Literature search and AI screening, both phases (§5.1) — 1,572/1,572 screened
- [x] 4. RA title/abstract review — abstract recovery + re-read done; NOT independent (same reader)
- [~] 5. Full-text retrieval — scripted passes + browser pass COMPLETE (101/436). 335 handed off; 3 subscription-walled studies are the priority
- [~] 6. Full-text screen — done on the 89 readable texts; **RA spot-check NOT done**
- [~] 7. Extraction — 16 effects, 13 studies; **RA has NOT verified a random 10%**
- [x] 8. Risk-of-bias — seven domains, derived from the extraction fields rather than assigned
- [x] 9. Narrative synthesis — the ≥3 test was APPLIED after stratification and nothing pools
- [x] 10. Demographic significance — PM not assessed, FDT not identified, SDT 3% AND WRONG-SIGNED
- [~] 11. GRADE rated per phenomenon; **one rater, not three**
- [x] 12. Chapter drafted on the docs/chapter-template.md three-layer structure
- [ ] 13. RA lay-readability check
- [ ] 14. PI review and sign-off

## Inherited boundary

C.2.c (TICK-055/056) already drew this wall and it should be adopted, not re-litigated.
`literature/search-logs/housing-costs-search-scope.md` **Wall 2 — the mediator wall**:

- **A.23 owns** variation in the living arrangement itself → fertility, at given prices.
- **C.2.c owns** housing cost → fertility *including* the part travelling through co-residence,
  because C.2.c owns the treatment and A.23 owns the mediator.

Two consequences carry into this chapter:

1. The two contributions are **not additive** — most of C.2.c's young-adult effect runs down A.23's
   channel. Same accounting problem flagged at A.10 → A.7 (TICK-054); the demographic-significance
   section must not double-count.
2. `housing-costs-snowball-log.md` records A.23 boundary cases (boomerang moves, returning to the
   nest, leaving home) that routed **out** of C.2.c. Harvest them as seeds before running a fresh
   frame; C.2.c's `HOUSING_ONLY_MECHANISM` bucket is a second seed source.

## Why this one now

Smallest remaining frame by an order of magnitude on a one-shot OpenAlex probe (~361 records against
~1,000–39,000 for the other unstarted narrow candidates), single phenomenon (SDT), single mechanism,
and the scope wall arrives pre-drawn from a finished chapter.

**Superseded, 2026-08-27:** the ~361 came from a narrow selection-time probe. The measured frame on
the full exposure vocabulary is **1,012**; see `co-residence-parents-household-delay-search-scope.md`
§11. The like-for-like ordering that picked A.23 is undisturbed, but this number is the right one.

## Log

### 2026-08-28 (afternoon) — rulings taken, chapter drafted

Scripts 237-242. **`output/chapters/co-residence-parents-household-delay.md` is drafted** on the
three-layer template. Not PI-reviewed.

**Browser pass (5f).** Recovered no files — Chrome renders a PDF in a viewer no tool can read, and a
localhost sink is refused by Chrome's private-network rule. It recovered 5 abstracts and 8 route
verdicts, and the verdicts are the finding: **a curl 200 carrying HTML is not proof the route is
open.** Duke University Press paywalls both its records, which `235` had filed as browser work.

**Three rulings taken** (`…-wall1-ruling.md`, `…-rulings-and-amendments.md`), all PI-pending.
Wall 1 sorted on OUTCOME rather than exposure shrinks the dispute from 26 records to 7 studies, so
position 3 — shared and non-additive — became the cheap option instead of the expensive one.

**THE CHAPTER'S RESULT.** The cell the registered claim names — an unpartnered childless young adult
in the parental home — holds **zero identified designs and zero effect estimates.** The literature
that looks like it is about the claim is describing the joint timing of leaving home and childbearing,
or estimating what makes young people stay. The best-identified evidence in the chapter (MODERATE)
is about link 1, and the one study there that looks for a fertility effect reports a null.

**Demographic significance is NEGLIGIBLE AND WRONG-SIGNED:** 3% of the SDT fall, in the direction of
raising fertility. Both configurations of the exposure rose and they push opposite ways, so a
calculation counting only the named configuration would have credited that share to the decline.

**Still open:** 5 PI rulings; RA spot-check of the screen; RA verification of 10% of the extraction;
two more GRADE raters; and three subscription-walled studies (Chu; Laeven & Popov; Kucheva) that are
the top of the library worklist — Chu could change the direction reported in §6.2.

### 2026-08-28 — stage 5 run end to end; the scripted part is finished

Scripts 232-236. **101 of 436 on disk (23%)** — 79 PDFs, 3 HTML full texts, 13 PMC texts,
6 twins.

**The rate is not the result.** The two rows that decide whether stage 5 is finished are the
Wall 1 packet at **5 of 26** and the identified designs at **9 of 22**. The chapter's
retrieval problem is its shape, not its rate: the tiers holding the open ruling and the
GRADE evidence are the ones publishers defend hardest.

**Three counters were lying, and each would have produced a confident false negative.**

1. **Unpaywall reported `found 0 / reached 352`** — the shape of a dead rung. It was not:
   it returned a url for most records with a DOI, and the de-duplication filter ran before
   the counter. The rung is *redundant* against OpenAlex's own `locations` here. `found`
   and `novel` are now separate counters.
2. **PMC's fourth zero was the PDF route, not PMC.** 5b found 14 urls and fetched 0,
   matching A.12, A.24 and C.3.g. `234` asked the structured-text routes and got **13 of
   the 14**, including both identified social-pension studies on link 1. *The honest
   re-reading of all four chapters is that they measured the same defended route rather
   than PMC's coverage — the rung should not be retired.*
3. **The on-disk cache erased rung attribution.** A re-run over a populated `pdfs/`
   directory collapsed every counter into `cached`. Provenance is now written per file.

**Two rungs added, both paid.** The deterministic rung went **22 for 22**. The 14 records
under DOI prefix `10.4054` are two publishers' objects — 8 Demographic Research articles and
6 MPIDR working papers — with different path constructions; a rung written at the prefix
would have taken the 8 and silently dropped the 6.

**A version pair is one study** (`236`). The Wall 1 packet documents two pairs inside the
frame and 5b failed on both members of each; both are now open through the preprint.

**Open, and it is a human's turn:** `W1_browser` 55 records (13 critical) — a 200 that was
not the article, mostly SSRN `doi.org` 403s, with the blocked twin named for each;
`W2_library_proxy` 185 (13 critical); `W3_librarian` 95 (4 critical), no DOI at all.

**Still open from 8/27:** the Wall 1 second read, the pooling rule, and six scope amendments.

### 2026-08-27 — stages 2, 3 and 4 run end to end

Scripts 212–231. Scope drafted with Rulings 1 and 2 taken; anchors gated (33 FOUND);
snowball rounds 1–2 (3,793-record pool); channel 5; production query V2 adopted
(frame 1,711, gold recall 100%); frame pulled and hand-supplemented (1,572); rubric
and 29 batches; **screen complete, 1,572/1,572**; RA gate (Crossref abstract recovery,
re-read, retrieval queue, Wall 1 packet).

**Result:** 78 RELEVANT / 397 UNCERTAIN / 1,097 NOT_RELEVANT. 117 primary-cell records
(49 extended-household, 38 pre-launch, 26 MIXED_PRICE_ARRANGEMENT, 4 proximity).
436 records queued for retrieval in 8 tiers.

**Open before freeze:** the Wall 1 second read (packet assembled — it decides whether
the chapter has an identified core), sign-off on the pooling rule, and six scope
amendments the screen generated.

### 2026-08-27 — stage 2 opened

- `212_a23_harvest_c2c_seeds.py` — 159 seed candidates recovered from C.2.c's finished artifacts
  (14 routed records, 1 verified anchor, 144 mined from the 10,915-record snowball pool).
- `213_a23_frame_probe.py` — frame sized before any production query: 1,012 records in the screenable
  exposure ∩ fertility frame, 1,948 in the union-outcome frame, 87 carrying identification vocabulary.
- `co-residence-parents-household-delay-search-scope.md` — DRAFT. Two PI calls open (§5 configuration
  ownership, §12 the pre-modern niche).
- Scripts numbered from 212: the highest across all live branches was 211 (C.3.g), not 88 as `main`
  alone shows.
