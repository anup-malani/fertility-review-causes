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
- [x] 3. Literature search and AI screening, both phases (§5.1)
- [~] 4. RA title/abstract review
- [~] 5. Full-text retrieval
- [~] 6. Full-text screen, RA spot-checks 5–10%
- [~] 7. Extraction to `extraction/easterlin-relative-income.csv`, RA verifies a random 10%
- [~] 8. Risk-of-bias assessment per study
- [x] 9. Meta-analysis if ≥3 extractable effects, narrative synthesis otherwise
- [x] 10. Demographic significance against PM / FDT / SDT
- [~] 11. GRADE rating, 3 independent raters
- [x] 12. Chapter draft on the §6 template
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

### 2026-09-02 — screen COMPLETE: 709 of 709, blind sensitivity 31/31

- All seven strata finished. Validation clean: every verdict id on a sheet, no id routed twice, no
  stratum left partial. **Blind sensitivity 31/31 (100%)** — the anchors sat in the sheets unmarked
  and `312_` is the first place they are identified.
- **Yield 141/709 primary (19.9%); 293/709 (41.3%) kept in some cell.**

| cell | n | |
|---|---|---|
| `CYCLE_TEST` | **46** | the cell the scope worried had no retrievable vocabulary |
| `COHORT_SIZE_FERTILITY` | 32 | |
| `RELATIVE_INCOME_FERTILITY` | 29 | |
| `RIVAL_TEST` | 29 | Butz–Ward and the Chicago model, well populated |
| `BOOM_ALTERNATIVE` | 18 | new cell, added mid-screen |
| `MIXED_COHORT_MARRIAGE` | 15 | Wall 3, unallocated |
| `BENCHMARK_MEASURED` | **5** | |
| `LINK1_LABOUR` | 45 | context, never pooled |
| `THEORY` | 74 | |

- **`CYCLE_TEST` is the surprise, at 46.** Scope §2 separated the cycling claim from the reduced-form
  claim and expected the former to be thin; the arm calibration reinforced that by finding only one
  anchor. There is a substantial formal literature — Lee's feedback models, Samuelson's waves,
  Wachter's *Elusive Cycles*, OLG and limit-cycle models, spectral analyses, and repeated forecasting
  applications. This cell can carry the cycling claim on its own and must not be pooled with the
  reduced-form cells.
- **`BENCHMARK_MEASURED` finished at 5, not 0.** Scope §4 predicted the value-added cell might be
  empty because studies proxy the parental-household standard rather than measuring it. Five measure
  something closer to it: two Great Recession *resources-and-aspirations* papers, a test using
  **income for two generations**, subjective relative affluence, and the Depression-scarcity
  life-course study. Thin, but the cell exists and it is where the chapter's strongest identification
  claim will have to come from.
- **A new cell was added mid-screen: `BOOM_ALTERNATIVE`** — competing explanations of the baby boom
  itself (WWII female labour supply, household technology, war debt, mortgages, 1918 influenza,
  unionisation). They are not evidence about Easterlin's mechanism, but they are evidence about how
  much of the mechanism's own best case is already spoken for, which §5 demsig needs. Forcing them to
  `OFF_OTHER` would have discarded exactly those records. **The four strata screened before the cell
  existed were re-checked programmatically: zero affected records.**
- **Retrieval artefacts worth recording.** (i) 14 of 47 `arm_only_rival` records are chapters of one
  edited volume, each carrying the volume's table of contents as its abstract. (ii) The `rival` arm's
  term `"Butz"` matched a paper on obese-rat reproduction whose co-author is named Butz — an
  author-name homonym inside an exposure term. (iii) `multi_arm` contains ~20 near-duplicate
  2025–26 preprints of two titles (*Life-Value Reflow*, *Ecological Loop Demography*), which inflate
  a frame without adding a study.
- **Next: full-text retrieval.** The 141 primary records plus 15 `MIXED_COHORT_MARRIAGE` are the
  retrieval queue; `LINK1_LABOUR` and `THEORY` are context and are not retrieved in this pass.

### 2026-09-02 — full-text retrieval: automated ceiling at 19/156, and the gate is one cell

- `313_c6a_retrieval.py` (retrieval) and `314_c6a_retrieval_handoff.py` (handoff). Queue was the
  141 primary records plus 15 `MIXED_COHORT_MARRIAGE`; `LINK1_LABOUR` and `THEORY` are context by
  scope §3 and were not retrieved.
- **Rung order was chosen for this chapter, and the choice is now measured.** This is an economics
  and demography literature, so the rungs are OA locations → **RePEc/NBER** → Unpaywall → PMC BioC.
  **PMC is empty here: 45 records carry a pmid — demography journals are indexed in PubMed — and not
  one is in the PMC open-access subset.** Carrying another chapter's rung order would have spent the
  effort on the wrong index.
- **Three defects, and the first was mine.** (i) `found` was incremented for every rung *attempted*
  rather than every rung that *produced a URL*, so Unpaywall was credited with 114 "found" when 81
  of those were Unpaywall replying that no open copy exists — and those 81 were then mislabelled
  `found_not_fetched` instead of paywalled. `probed` and `found` are now separate counters. (ii) The
  same conflation applied to PMC BioC, which answers **HTTP 200 with an empty body** outside the OA
  subset; crediting the constructed URL made an absent corpus read as a broken downloader. (iii) A
  landing page is not a dead end — RePEc, EconPapers and NBER pages link the PDF one hop away, and
  26 records had died there.
- **403 is not the only shape bot defence takes.** A 202 interstitial and a 200 with a stub body are
  the same defence, quieter. Counting those as "not found" turns retrievable records into confident
  absences. Reclassified: **32 browser jobs** (open URLs defeated by defences) against **105 proxy
  jobs** (no open copy exists). A single undifferentiated "missing PDFs" list sends a person to the
  wrong tool.
- **The gate is not the rate.** 19/156 is low, but the number that decides the chapter is
  **`BENCHMARK_MEASURED` 0/5** — the only cell where a study measures the parental-household
  benchmark rather than proxying it with cohort size. **Extraction does not begin until those five
  are resolved.** This is A.17's lesson: 23/114 was survivable there and 0 of 4 identified
  direct-arm records was not.

| cell | have | browser | proxy |
|---|---|---|---|
| `BENCHMARK_MEASURED` | **0/5** | 2 | 3 |
| `RIVAL_TEST` | 3/29 | 9 | 17 |
| `CYCLE_TEST` | 6/46 | 5 | 35 |
| `COHORT_SIZE_FERTILITY` | 4/32 | 7 | 21 |
| `RELATIVE_INCOME_FERTILITY` | 3/29 | 4 | 22 |
| `MIXED_COHORT_MARRIAGE` | 3/15 | 5 | 7 |

- Handoff at `easterlin-relative-income-retrieval-handoff.md`, ordered by cell rather than by
  convenience, with the file-matching warning attached: hand-retrieved PDFs arrive publisher-named
  and a wrong pairing corrupts the extraction table silently.
- **313 is idempotent** — files already on disk are skipped with their original rung attribution
  preserved, so a second run reports the same numbers rather than losing provenance to a cache.

### 2026-09-02 — the re-run check found two hazards in 313, both now fixed

The idempotence claim in the previous entry was **asserted, not tested**. Testing it turned up two
defects, and the test itself nearly caused a third.

- **A `--limit` run REPLACED the state file.** A bounded re-run would have silently discarded the
  other 126 records' rung attribution — a shrinking input shrinking the output, which is exactly
  `stage-output-must-survive-rerun`. The state is now **merged** into what is already on disk, and
  the pass records `last_pass_n` / `last_pass_ids` so a partial run is legible as partial.
- **The cache branch invented a rung.** A file on disk with no prior state fell back to
  `via="cached"`, which was then counted in `fetched_per_rung` — a fake rung name that would make
  the second run's table disagree with the first's. It now records `unknown_provenance` and is kept
  **out** of the rung counters. This matters concretely: hand-retrieved PDFs from the handoff arrive
  with no automated provenance, and they must not be credited to a rung that never fetched them.
- **The cache path also inflated `probed`.** The rung counters ran before the cache check, so a
  cached record counted rungs nothing had contacted; a cache-only pass reported unpaywall as
  "probed 13, found 0, empty for this literature" while simultaneously showing `fetched 1`.
  Contradictory on its face. Counters now sit after the cache check.
- **Added `--ids`**, so an RA installing three hand-retrieved PDFs can re-ingest just those instead
  of re-attempting 156 records over the network. The handoff already instructs a re-run; it should
  not cost an hour.

**Verified:** re-running the 19 cached records reports `probed 0` on every rung (nothing contacted),
reproduces the fetch attribution exactly — `oa_locations` 14, `repec` 4, `unpaywall` 1 — and leaves
the state at 156 records / 19 have.

**Not claimed:** a bit-identical *full* re-run. The 137 unretrieved records re-contact the network,
and a host that answers 403 today may answer 200 tomorrow, so their classification is legitimately
live. The property that had to hold is that retrieved files survive a re-run with their provenance
intact, and that a partial pass cannot shrink the record. Both now do.

### 2026-09-02 — the browser job: 19 → 25, and what the browser was actually good for

Attempted the 32-record browser job. **The browser could not deliver files, but it diagnosed why the
script was failing, and fixing that recovered 6 records without any clicking.**

**What the browser cannot do here.** Chrome renders these PDFs fine, but no route gets bytes to disk:
downloads triggered from the page do not land in Chrome's configured download directory; a
page-context `fetch()` is refused by the extension's CSP; and a natively rendered PDF keeps its text
in the plugin, not the DOM, so there is nothing to read out either. `curl` with a browser
User-Agent still gets 403 from figshare's direct download URL, so these really are bot-defence
blocks — the classification was right, the tool was wrong.

**What it was good for: it showed me the URL my own script was refusing to try.** Reading one
EconPapers record in the browser exposed three defects in 313, all of which manufacture false
absences:

1. **I gated `oa_locations` on `loc["is_oa"]`.** *Becker vs Easterlin* has two locations, **both
   flagged `is_oa=False`**, and one of them is a 352 KB PDF on a university web server that
   downloads on the first request. **The flag is the index's opinion; the URL is the fact.** Trying
   costs one HTTP request; skipping costs a record.
2. **EconPapers/IDEAS wrap the real target in `redir.pf?u=<urlencoded>`.** The wrapper is
   bot-defended, the target usually is not. Decode the parameter and fetch the target.
3. **Landing-page link extraction looked only for `href="*.pdf"`.** DSpace and bepress serve PDFs
   from `/bitstream/` and `viewcontent.cgi` paths with no extension. Added the
   **`citation_pdf_url` meta tag**, which nearly every repository and journal platform emits and
   which is the reliable route.

**Result: 19 → 25 retrieved**, including *Becker vs Easterlin* (a `RIVAL_TEST` anchor) and — the one
that matters — **`BENCHMARK_MEASURED` is no longer 0/5.**

| cell | have | was |
|---|---|---|
| `BENCHMARK_MEASURED` | **1/5** | 0/5 |
| `RIVAL_TEST` | 6/29 | 3/29 |
| `CYCLE_TEST` | 7/46 | 6/46 |
| `RELATIVE_INCOME_FERTILITY` | 4/29 | 3/29 |
| `COHORT_SIZE_FERTILITY` | 4/32 | 4/32 |
| `MIXED_COHORT_MARRIAGE` | 3/15 | 3/15 |

**The gate still holds.** Four of five `BENCHMARK_MEASURED` records remain unread, and extraction
does not begin until they are resolved. Handoff regenerated: **26 browser jobs, 105 proxy jobs.**
The browser job now genuinely needs a human — the blocks are Cloudflare-class on `read.dukeupress.edu`,
`papers.ssrn.com`, `sciencedirect.com` and `pmc.ncbi.nlm.nih.gov`, where the clearance cookie is
HttpOnly and cannot be handed to a script.

### 2026-09-02 — 9 hand-retrieved PDFs installed by content; retrieval 25 → 34

Shravan retrieved the tier-1-to-4 priority list. Installed with
`315_c6a_install_handoff.py`, which matches each file to a record **by its own content** — never by
filename, because nothing downstream would catch a wrong pairing.

- **`117behrman.pdf` is the Tier 1 two-generations paper.** The filename says nothing; the content
  matched it at 1.00. This is the single record that gated the chapter.
- **`2060471.pdf` is Lee 1974** — believed not retrieved, but it was in the folder and matched at
  1.00. Content matching found a record nobody knew they had.
- **Butz and Ward settles its own version-twin question.** The PDF's title page reads *American
  Economic Review, Jun. 1979, Vol. 69, No. 3, pp. 318–328.* OpenAlex dates the 438-citation record
  **1977**; the version of record is **1979**. Recorded against the resolver's `MATCH_VERSION_TWIN`.
- Three identical copies of the Stockholm report were in the folder; all resolved to one record.
- One file had **no text layer** (a Wiley scan) and was matched on the **DOI printed in the
  document** instead.

**The matcher had to be built and then fixed four times, and its selftest is the only reason none of
that reached an install.** It runs against the PDFs already retrieved automatically, whose pairing
is known, and refuses to install when it scores under 80%.

1. A hand-rolled FlateDecode/Tj extractor scored **2/25**. Replaced with macOS PDFKit via JXA — no
   install needed, and it reads what a person would see.
2. Scoring counted title tokens appearing anywhere in 40,000 characters, so a generic title
   ("Did the Baby Boom Cause the US Divorce Boom") matched any fertility paper's **bibliography**
   and won seven files that were not it. Fixed to a contiguous run over the title page.
3. That broke to **2/25** because I stripped stopwords from titles but not from the text, so every
   run ended at the first `and`. Symmetric tokenisation.
4. **The DOI matcher — the strongest signal — was dead on arrival.** `pdf_text` returned *folded*
   text, and folding turns `10.1111/j.1728-4457...` into spaces, so the regex could never match
   while the title heuristics carried on and made the selftest look fine. Same shape as
   `norm-strips-punctuation-dead-patterns`, in a different stage.

Final selftest **21/25**; the four failures are scans with no text layer, reported as unmatchable
rather than guessed. Three files that tied at 1.00 against a shorter generic title were verified by
reading their title pages by hand and installed by id. All nine carry `via=unknown_provenance` and
are excluded from the rung counters, as they must be — no rung fetched them.

**`BENCHMARK_MEASURED` is 4/5.** The gate is all but cleared. The one outstanding record is
*Subjective relative affluence and expected family size* (1985, *Sociology and Social Research*),
which has **no DOI in OpenAlex** and is pre-DOI-era — it needs a catalogue or ILL request, not a
publisher lookup.

| cell | have | was |
|---|---|---|
| `BENCHMARK_MEASURED` | **4/5** | 1/5 |
| `CYCLE_TEST` | 9/46 | 7/46 |
| `RIVAL_TEST` | 7/29 | 6/29 |
| `COHORT_SIZE_FERTILITY` | 7/32 | 4/32 |
| `RELATIVE_INCOME_FERTILITY` | 4/29 | 4/29 |
| `MIXED_COHORT_MARRIAGE` | 3/15 | 3/15 |

Overall **34/156**. Handoff regenerated: 24 browser, 98 proxy.

### 2026-09-02 — extraction complete on what we have (34/34), and the chapter is drafted

- **All 34 retrieved full texts extracted**, `extraction/easterlin-relative-income.csv`, 34 rows x 20
  columns. **6 could not be read at all** — scans with no text layer — and carry `NOT EXTRACTED` in
  every field so nothing downstream can read them as absences. The most consequential is Macunovich
  (2000), the strongest global statement of the hypothesis, still unread.
- **Chapter at `output/chapters/easterlin-relative-income.md`**, 4,845 words, conformant to
  `docs/chapter-template.md`: S1–S7 present in their sections, §1–§12 in order, plain terms before
  technical in §1 and §7, S4 before any arithmetic in §8, no analogy, verdict standalone.

**The verdict changed during §8, on a number I did not have when I started writing.** I expected
NEGLIGIBLE for the SDT, because the sign test returns 0 of 18 across the full window. Computing how
the decline is *distributed* across that window reversed it: **the median country took 75% of its
entire post-1965 fertility fall during 1965–1980**, which is the sub-window where the mechanism's
exposure moves correctly in 14 of 18 countries. A mechanism that works across three-quarters of the
decline is not negligible. **SDT = MINOR**, not NEGLIGIBLE (no share was computed, and NEGLIGIBLE
asserts one under 5%) and not SUBSTANTIAL (the direction result is shared with any co-trending pair
of series, and the distinctive prediction fails).

- **The carry-away is 0 of 18.** The mechanism requires fertility to *recover* once the small
  post-bust cohorts came of age after 1980. In none of the 18 countries did it. That is the
  falsification of the cycling claim specifically, as against a general claim that young people's
  prospects matter — and it is what Wachter (1991) predicted formally when he asked whether
  dynamically possible Lee–Easterlin models exist.
- **GRADE:** PM **No evidence**; FDT **No evidence** for the FDT as a decline (the boom-era body
  answers a different question); SDT **VERY LOW**, downgraded for inconsistency (Pampel's country
  effects span significant positives and negatives; Hill's sign flips with fixed effects) and risk of
  bias (aggregate series dominate, and the exposure is mechanically a lagged function of the outcome).
- **No study in the body uses exogenous variation in cohort size.** Sixty years of testing on the
  correlation between a country's age structure and its birth rate, two series in which one is built
  from the other's past. §5.2 names the designs that would work; the immigration-wave instrument
  appears to be unused for this question.
- Stage 11 is partial: **one GRADE rater, protocol requires three.**
- Written at 22% retrieval on Shravan's instruction; no objection was recorded against doing so, and
  the Provenance block says exactly which findings would survive full retrieval and which might not.

