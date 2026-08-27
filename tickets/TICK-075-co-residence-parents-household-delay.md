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
- [ ] 5. Full-text retrieval
- [ ] 6. Full-text screen, RA spot-checks 5–10%
- [ ] 7. Extraction to `extraction/co-residence-parents-household-delay.csv`, RA verifies a random 10%
- [ ] 8. Risk-of-bias assessment per study
- [ ] 9. Meta-analysis if ≥3 extractable effects, narrative synthesis otherwise
- [ ] 10. Demographic significance against PM / FDT / SDT
- [ ] 11. GRADE rating, 3 independent raters
- [ ] 12. Chapter draft on the §6 template
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
