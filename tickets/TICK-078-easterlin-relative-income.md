# TICK-078: C.6.a Easterlin Relative Income / Cohort Size
**Status:** in-progress
**Assigned:** Shravan
**Hypothesis:** `easterlin-relative-income` — HYPOTHESES-v5.md §C.6.a
**Parallel-safe:** yes
**Blocks:** none
**Blocked by:** none
**Touches:** literature/search-logs/easterlin-relative-income-*, extraction/easterlin-relative-income-*, output/chapters/easterlin-relative-income.md

## Acceptance criteria
- [x] 2. Search strategy and scope drafted
- [ ] 3. Literature search and AI screening, both phases (§5.1)
- [ ] 4. RA title/abstract review
- [ ] 5. Full-text retrieval
- [ ] 6. Full-text screen, RA spot-checks 5–10%
- [ ] 7. Extraction to `extraction/easterlin-relative-income.csv`, RA verifies a random 10%
- [ ] 8. Risk-of-bias assessment per study
- [ ] 9. Meta-analysis if ≥3 extractable effects, narrative synthesis otherwise
- [ ] 10. Demographic significance against PM / FDT / SDT
- [ ] 11. GRADE rating, 3 independent raters
- [ ] 12. Chapter draft on the §6 template
- [ ] 13. RA lay-readability check
- [ ] 14. PI review and sign-off

## Why this one now

Smallest remaining frame of the unstarted hypotheses on a three-vocabulary OpenAlex probe
(`source/build/goldset/304_candidate_frame_probe.py`, log at
`literature/search-logs/candidate-frame-probe-2026-09-02.md`): **487 records** in the deduplicated
union frame, against 675 for the next candidate (A.6) and 1,103 for the one after (C.3.f). Single
phenomenon (v5 registers it **SDT only**), single mechanism, and v5's `cross-ref` field is empty, so
it opens with no inherited boundary debt.

The probe was run three times on purpose. A single narrow axis put C.6.a at 236 and A.6 at 12; the
second vocabulary moved A.6 to 686 and C.2.h from 141 to 4,484. Ranking on the first probe alone
would have picked the wrong chapter — `empty-cell-needs-second-channel`, applied to sizing rather
than to a finding.

**The homonym was measured, not assumed.** "Easterlin" and "relative income" both anchor a large
happiness literature: 437 records for "Easterlin paradox" and 566 for relative income ∩ well-being.
Intersected with the fertility outcome axis, "Easterlin paradox" returns **2**. The outcome axis
separates the two literatures by itself, which is not true of most candidates this size.

## Open rulings to freeze at stage 2

1. **A cycling mechanism against a level-shift phenomenon.** v5's own note says the hypothesis
   "predicts oscillation, not a secular decline." PROTOCOL §6 demographic significance asks what
   share of a decline the mechanism accounts for; a mechanism whose prediction is a cycle has no
   natural numerator there. Decide **before searching** what demsig means for C.6.a — the share of
   the post-war boom-and-bust amplitude, the share of the secular SDT decline, or NOT ASSESSED with
   a stated reason. A.18 hit the same wall from the other direction and the lesson is recorded in
   `variance-component-has-no-demsig-numerator`: check the phenomenon before saying "nowhere."
2. **Registered as SDT-only, but the founding evidence is the US baby boom and bust**, which
   straddles the FDT/SDT hinge (~1946–1975). Freeze whether the boom is in scope, and if so under
   which phenomenon, rather than discovering the ambiguity at synthesis.
3. **The marriage-market channel.** Relative cohort size acts partly through a marriage squeeze,
   which is C.7.a's and A.10's variation. v5 lists no cross-ref, but the wall is real. C.7.a is a
   finished chapter and A.10 has a drafted scope; cut the wall against both. Under the boundary rule
   frozen by C.2.c on 2026-07-31, neighbours are separated by *what varies*: **C.6.a owns variation
   in relative cohort size and cohort-relative earnings; C.7.a owns variation in marriage-market
   composition; A.10 owns variation in the sex ratio.**
4. **C.6.a vs C.1.a (income) and C.5.a (economic uncertainty).** The discriminator is whether the
   estimate is of an *absolute* income or employment level, or of income *relative to a
   cohort-specific benchmark* (parental household consumption, or own-cohort size). Absolute-level
   designs route out.

## Cold-start seeds already in hand

Finished and in-progress chapters have routed Easterlin records into their own screen files without
this chapter existing: 15 mentions in `credit-constraints-screen-universe.json`, 14 in B.1's
tier-B frame, 6 in C.2.c's snowball pool, 6 in C.3.c's OA enrichment, plus more on unmerged
branches. Mine these before the cold-start anchor round — they are provenance-labelled hits from
neighbouring literatures, which is the `snowball-pools-omit-their-own-seeds` failure in reverse.

## Log

### 2026-09-02 — opened, and scope drafted with three rulings resolved

- Selected by `source/build/goldset/304_candidate_frame_probe.py`, which sizes every unstarted
  hypothesis and generates its own ranking table. Union frames: **C.6.a 487**, A.6 675, C.3.f 1,103,
  A.19 2,774. Four passes, because one vocabulary ranks the wrong chapter — a narrow axis put A.6
  first at 12 records against a union frame of 675.
- Scope at `literature/search-logs/easterlin-relative-income-search-scope.md`. Six walls, twelve
  estimand cells, required tags, pooling rule and the demsig route all frozen before any query.
- **Ruling 1 (the ticket's central question — what does demographic significance mean for a mechanism
  that predicts a cycle?): RESOLVED, and it does not go to NOT ASSESSED.** PROTOCOL §4.2 offers three
  independent routes and only the first needs a decomposition denominator. Slope sufficiency and R²
  are both computable here. The **sign test is pre-registered before the search**: post-boom cohorts
  entering the labour market are small, so the hypothesis predicts favourable relative income and
  *rising* fertility across the SDT window, against an observed fall. If that holds when computed,
  the SDT cell is settled by the sign and the missing share is irrelevant to it.
- **Ruling 2 (phenomenon assignment): RESOLVED provisionally.** SDT cell as registered; the baby boom
  classified by PROTOCOL §2's replacement rule, which returns FDT-like — assigning a fertility *rise*
  to a phenomenon defined as a decline. That is PI Call 1 and it is protocol-level: C.6.a is the first
  hypothesis in the review whose central evidence is an increase, and C.2.d and D.1.d will follow.
- **Ruling 3 (the cohort-size marriage squeeze): RESOLVED** as jointly claimed and unallocated, on
  C.2.c's `MIXED_PRICE_CREDIT` precedent rather than a new device.
- **Wall 6 is a measured non-threat.** "Easterlin paradox" returns 437 records unrestricted and **2**
  against the fertility outcome axis, so the happiness literature separates itself and no screen rule
  is spent on it. Recorded because the usual finding runs the other way.
- **Found while checking a claim in the draft: `data/raw/` is empty.** `CLAUDE.md` describes it as
  holding HFD, WPP, Maddison, Gapminder and WDI; on `main` and every branch it holds `.gitkeep` alone.
  The only macro data in the repository is two ad-hoc World Bank TFR pulls sitting on B.6's and B.7's
  unmerged branches. Every demsig denominator to date has come from what individual studies reported.
  This chapter cannot borrow that workaround — its decisive computation is an exposure series, not an
  estimate — so it builds the series and deposits it in `data/raw/` for A.9, C.2.d and anything else
  that needs cohort structure.
- Open for Anup: **PI Call 1** (the replacement rule has no category for a fertility rise) and
  **PI Call 2** (v5 gives C.6.a `cross-ref: --`; on the walls it should read C.1.a, C.5.a, C.7.a, A.9,
  C.2.e). Call 2 is flagged, not made, because HYPOTHESES-v5.md is under PI review at TICK-001.

### 2026-09-02 — free seeds harvested, and the pre-registered sign test run before any search

- **143 free seed candidates** recovered by `source/build/goldset/305_c6a_free_seeds.py` from other
  chapters' pools — 842 branch:file pairs, 60 unique blobs, zero retrieval cost. Includes Macunovich's
  relative-cohort-size paper, two Butz–Ward evaluations for `RIVAL_TEST`, a Lee–Easterlin dynamic-
  cycles paper for `CYCLE_TEST`, a cohort-size marriage-market study for Wall 3, and a Chinese-famine
  cohort-shrinkage index — scope §7 row 3 arriving unbidden.
- The harvest reports yield **per term and per term alone**, which is what caught the first run's
  defect: a bare `baby boom` returned 402 of 480 records, nearly all *Baby Boomers* the living
  generation. Excluding the `-er` suffix cuts the pool to 143 and makes the axis usable.
- **`data/raw/` is no longer empty.** `source/build/306_c6a_cohort_size_series.py` pulls World Bank
  age structure and TFR for 18 SDT countries, 1960–2024, deposits the unmodified responses in
  `data/raw/wdi-age-structure/` with a PROVENANCE note, and derives
  `output/tables/easterlin-relative-cohort-size.csv`. Later chapters read from there instead of
  re-pulling.
- **The sign test, run before any search, at `easterlin-relative-income-sign-test.md`.** Result:
  **1965–80, 14 of 18 countries consistent** with the sign the mechanism requires, with very strong
  within-window correlations (US r = −0.98, Belgium −0.99, Canada −0.98). **1980–present, 0 of 18.**
  Full window, 0 of 18.
- **The full-window column is the finding, not a null.** Relative cohort size is a *hump*: it returns
  to within a fraction of its own amplitude of where it began (US 0.333 → 0.466 in 1980 → 0.291)
  while TFR falls by roughly a birth and stays down. A driver that ends where it started cannot
  account for a permanent level shift. The first version of this test reported only full-window
  endpoints and read "0 of 18" as uniform failure; splitting the window recovered the mechanism's
  genuine success case and located the failure precisely where the registry says it is.
- **PI Call 3 raised — PROTOCOL §4.2's R² criterion is sign-blind.** 6 of 18 countries clear the
  0.15 threshold and **all 6 do so with the correlation running against the hypothesis** (Japan
  R² = 0.71 at r = +0.84). Read literally the criterion certifies a hypothesis on evidence that
  refutes it. This chapter attaches a sign condition; whether §4.2 should carry one generally is for
  Anup, and it affects every hypothesis with a directional prediction.
