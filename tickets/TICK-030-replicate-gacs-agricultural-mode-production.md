# TICK-030: Replicate GACS for agricultural mode of production
**Status:** in-progress
**Assigned:** any
**Parallel-safe:** no
**Blocks:** --
**Blocked by:** --
**Touches:** source/build/goldset/, literature/search-logs/agricultural-mode-of-production-*, tickets/QUEUE.md, tickets/TICK-030-replicate-gacs-agricultural-mode-production.md, handoff.md, session-log.md

## Description
Replicate the latest Gold-Anchored Clustered Search (GACS) procedure on the approved
`agricultural-mode-of-production` hypothesis. Treat this as the documented second-hypothesis
generalization test: build an independent cold-start gold instrument, define and calibrate the
cause/effect vocabulary clusters without leakage, run the production search and screening funnel,
and preserve reproducible search and recall artifacts.

## Acceptance criteria
- [ ] The hypothesis and estimand cells are specified for PM mode-of-production / child-economic-value mechanisms.
- [ ] A DOI/title-keyed, provenance-recorded cold-start gold set is built from orthogonal sources and frozen after review.
- [ ] Query terms and breadth are calibrated without training/test leakage, with recall and candidate-budget results recorded.
- [ ] The live search is run reproducibly with caching, deduplication, and a search log.
- [ ] The deterministic and LLM screening funnel produces tiered topical and estimand-ready outputs.
- [ ] Cross-hypothesis lessons and any deviations from the documented GACS prototype are recorded.

## Log
- 2026-07-16, Alexandra: Released before search implementation at the user's request so the linked
  child-labor-laws/compulsory-schooling hypothesis can be searched first. No hypothesis-specific
  production artifacts had been created.
- 2026-10-04, Shravan: Reclaimed as the next-smallest unstarted hypothesis (frame-probe union frame
  1811, the smallest candidate with no branch/search-log/extraction). Stage 2 search scope drafted:
  `literature/search-logs/agricultural-mode-of-production-search-scope.md` (DRAFT, not frozen). The
  scope establishes the chapter's central identification problem — the forager–agriculturalist
  fertility gap is overdetermined by the A.13 lactational-amenorrhea and nutrition-energy channels, so
  a bare cross-subsistence correlation is off-cell — plus the Boserup reverse-causal (density →
  intensification) threat, eight boundary walls, estimand cells, required tags, and the cold-start
  plan. Next: build and existence-verify the cold-start gold anchor set.
- 2026-10-04, Shravan: Stage A3 cold-start gold anchor set built and existence-verified via
  `source/build/goldset/89_c3a_cold_start_anchors.py` (adapts the B.1 builder; no DOI hand-asserted —
  live Crossref match + doi.org re-affirm, three-state gate). 21 candidates → **16 verified live DOIs,
  0 flagged, 5 expected pre-DOI book misses** (Boserup 1965, Netting 1993, Lee 1979, Howell 2010,
  Caldwell 1982). Value-channel empirical core 6/6 verified; both load-bearing routing decoys (A.13
  Konner & Worthman 1980, nutrition Ellison et al. 1993) verified. Artifacts:
  `agricultural-mode-of-production-cold-start-anchors.{json,md}`. Branch pushed to origin. Next GACS
  stage: Tier-B orthogonal frame (citation snowball) → discriminative terms → CV breadth → production
  query → live search + screen.
- 2026-10-04, Shravan: Stage A4 Tier-A/B frame built (`90_c3a_tier_ab_frame.py`, adapts 65): all 21
  anchors resolved in OpenAlex, **Tier A = 12 empirical seeds**, **Tier B = 4,756** deduped candidates
  (3,066 w/ abstracts, 0 deferred). Stage A5 screen apparatus built: `91_c3a_make_screen_batches.py`
  (119 blinded batches of 40, seed 301), `92_c3a_validate_screen.py` (fail-closed validator+assembler),
  `93_c3a_run_screen.py` (resumable runner; adds neutral-cwd + per-batch-retry hardening). Rubric
  validated on **pilot batch 1 (40/40 valid; walls fire — OFF_NUTRITION_B/OFF_WEALTH_FLOWS/REVERSE
  present)**.
  **BLOCKER (open): the full screen cannot run unattended here.** Nested `claude -p` hangs indefinitely
  on some batches (observed one call alive 17+ min, past the 900s subprocess timeout, which did not
  kill it). Full screen stopped after 1/119 batches. The instrument is complete and committed; the
  screen needs either (a) a hardened runner (process-group kill + shorter timeout) in a reliable
  environment, or (b) an API-key-based scorer instead of the nested CLI. Everything downstream
  (assemble → discriminative terms → production query → live search) waits on the screened frame.
