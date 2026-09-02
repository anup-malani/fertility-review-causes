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

### 2026-09-02 — cold-start anchors: 31 of 31, zero ghosts, three inherited resolver defects

- `source/build/goldset/307_c6a_cold_start_anchors.py`, a direct port of C.3.e's `275_` — the only
  copy carrying all four TICK-074 fixes. Log at `easterlin-relative-income-cold-start-anchors-log.md`.
- **The candidate list is its own control.** 18 `control` candidates are titles copied verbatim from
  records script 305 found in other chapters' pools, so they demonstrably exist; 13 `hand` candidates
  are author–year–title triples written from knowledge of the literature. A failure on a control is a
  broken resolver; a failure on a hand candidate may be a ghost citation. **Controls 18/18 on the
  first run**, which localised every failure to the candidate side before any of it was read.
- **Final: 31/31. Zero ghost citations** — every hand-typed title corresponds to a real indexed work.
- **Three inherited resolver defects, all found on one anchor** (Easterlin's *Birth and Fortune*),
  all present in `275_` and therefore in every copy on `main`. Reported to TICK-074 as defects 5–8.
  (i) `is_stem` was fixed in one direction only — it tolerates the index having the *longer* title,
  not the shorter one, and this book is indexed as the bare *Birth and fortune* at Jaccard 0.33 while
  four **reviews** of it score 1.00. (ii) The first-author gate was a scoring weight, so it could
  refuse the winner but not promote the correct record sitting in the same result set — the reviews
  beat the book 1.20 to 0.83. (iii) **The early exit was conditioned on a different test than the
  verdict**, so the loop stopped on a record the gate was certain to refuse and the rungs that can
  reach a truncated book title never ran. Fixing (i) and (ii) alone did not resolve the anchor; (iii)
  is what did.
- **New verdict class, `MATCH_VERSION_TWIN`**, proposed shared. Butz and Ward's *Emergence of
  Countercyclical U.S. Fertility* exists twice: the record OpenAlex dates 1977 carries **438**
  citations and the 1979 record carries **0**, so a candidate naming either year fails a ±1 gate
  against the other. Five of 31 anchors have twins and the split is severe — Welch's twin holds
  **0** of 659 citations. Both ids kept for every pair; a snowball seeded on one misses the other's
  citing set.
- **`BENCHMARK_MEASURED` — scope §4's value-added cell — has one anchor, and it is theory**
  (Easterlin's own 1976 aspirations-versus-resources statement). No empirical anchor measures the
  parental-household benchmark. A prediction for the search to test, not yet a finding.

### 2026-09-02 — production query: a SET of five, 90% recall, 909-record frame

- `source/build/goldset/308_c6a_production_query.py`, log at
  `easterlin-relative-income-production-query.{json,md}`. Recall is measured by asking OpenAlex which
  anchors each query returns (`ids.openalex:` alongside the search filter), never by re-implementing
  its tokenizer locally.
- **The first design was the wrong shape, and the anchors said so.** One exposure axis calibrated
  against all primary anchors plateaued at **15/21**, and the six misses clustered by arm rather than
  scattering: all three `RIVAL_TEST` anchors are Butz–Ward papers arguing the competing female-wage
  model and never use Easterlin's vocabulary; the `MIXED_COHORT_MARRIAGE` anchor pairs a cohort-size
  exposure with a *marriage* outcome. **No tuning of a single axis reaches them.** Scope §8 Wall 5
  says the rival-model tests are the most informative records this search can find, so a query that
  structurally cannot retrieve them is not one to tighten.
- **Rebuilt as five arms**, each calibrated against its own target cells: `easterlin` (6/8, frame
  339), `cohort-size` (3/4, 203), `cycle` (1/1, 444), `rival` (4/5, 66), `marriage-boundary` (2/2,
  550). **Union primary recall 18/20 = 90%**, deduplicated frame **909** — three arms carry
  `"Easterlin"`, so the 1,602 sum of arms is an upper bound, not the screening cost. The union query
  was checked to recall the same 18 the arms recall separately; a lower number would have meant the
  nested boolean parses differently than intended and its count is unusable.
- **The acceptance rule had to be made cost-aware.** Accepting any term with recall gain > 0 admitted
  `"aspirations"` for **one** anchor at **2,082 records**, and leave-one-out then showed it carried
  nothing else. Now gain > 0 **and** under 400 records per anchor, with every rejection logged at its
  price so the ceiling is auditable. `"Becker"` was rejected the same way on the rival arm (581/anchor)
  and `"aspirations"` again on the easterlin arm (3,087/anchor).
- **The outcome axis is calibrated per arm too**, and it held two of the three remaining misses —
  an anchor whose outcome is *family formation* is invisible to a fertility-only outcome axis however
  well the exposure axis is tuned. Adding it took the union from 17/20 to 18/20 for +5 records.
- **The two remaining misses are Easterlin's own 1961 and 1976 papers, and they are not a reason to
  add terms.** The only term reaching the 1976 paper prices at 3,087 records per anchor. Both route
  to the Phase 2 citation channel, which is where the most-cited works in a field are cheapest to
  find. `LINK1_LABOUR` anchors are also unreachable and that is by design — no arm targets link 1,
  and a query retrieving that literature well would be retrieving the wrong literature.
- **A caveat recorded rather than papered over:** the `cycle` arm has one target anchor, so its
  leave-one-out cannot discriminate. `"fertility cycles"` and `"fertility waves"` carry nothing
  uniquely against a single anchor, which is not evidence that they carry nothing. Kept, and flagged
  for re-calibration once the screen produces more cycle-cell records.

### 2026-09-02 — screen: universe built, prescreen recall-checked, 164 of 709 screened

- Pipeline: `309_` universe → `310_` prescreen → `311_` sheets → screen → `312_` validating ingest.
  Rubric at `easterlin-relative-income-screen-rubric.md`.
- **Two homonym clouds found by stratifying the universe, and both were free to remove.** The
  `cycle` arm's 177-record private stratum turned out to be **menstrual** cycles — menstruation,
  menopause, cycle-tracking — because `"fertility cycles"` means that in most of the indexed
  literature. The `marriage-boundary` arm's 151-record stratum was the sex-ratio and dowry literature
  of China and India, which Wall 3 assigns to A.10. Re-specifying both arms took the frame **909 →
  683 with recall unchanged at 18/20**.
- **The recall-side diagnostic had already flagged both and I had dismissed it.** Leave-one-out said
  `"fertility cycles"` and `"marriage squeeze"` carried no anchor uniquely, and I kept them because
  the cycle arm has one target anchor and LOO cannot discriminate on one. **The precision side
  settled what the recall side could not** — a term adding 177 records and no gold is the shape of a
  homonym cloud. 308 now computes `unique_records` and flags `suspect_homonym` so this is visible
  without a hand read.
- **A third homonym, in the `easterlin` arm: Duesenberry's relative-income hypothesis in CONSUMPTION
  theory**, plus "relative income poverty" as a poverty-measurement term. Together ~21 of that
  stratum's 87 records. Not removable by prescreen without risking the real ones; routed at the screen.
- Prescreen: 6 rules, all recall-checked, **31/31 gold retained**, 798 → 709.
- **Screened 164 (23%): `anchor_only` 5, `arm_only_rival` 47, `arm_only_marriage-boundary` 25,
  `arm_only_easterlin` 87 — each complete.** Ingest validates that every verdict id is on a sheet,
  no id is routed twice, and no stratum is left half-screened and reported as done.
- **Blind sensitivity 12/12 (100%).** The anchors sit in the sheets unmarked; 312 is the first place
  they are identified.
- Yield so far: **33/164 primary (20%)**, 59/164 kept in some cell. `RIVAL_TEST` 16 and
  `RELATIVE_INCOME_FERTILITY` 16 are both well populated.
- **`BENCHMARK_MEASURED` has its first empirical record.** Scope §4 predicted the value-added cell
  might be empty — that no study measures the parental-household standard rather than proxying it.
  *Scarcity and Prosperity in Postwar Childbearing* (1981) follows two 1920s birth cohorts through
  Depression scarcity into postwar prosperity, which is the benchmark measured rather than assumed.
  One record is not a cell, but it is not zero.
- **One retrieval artefact worth recording:** 14 of the 47 `arm_only_rival` records are chapters of a
  single edited volume, each carrying the volume's table of contents as its abstract. A shared-abstract
  volume can supply a third of a stratum on one term match.
- **Outstanding: 545 records in three strata** — `multi_arm` 374, `free_seed_only` 98,
  `arm_only_cycle` 73.

