# TICK-031: Replicate GACS for child-labor laws and compulsory schooling
**Status:** in-progress
**Assigned:** Alexandra
**Parallel-safe:** no
**Blocks:** --
**Blocked by:** --
**Touches:** source/build/goldset/, literature/search-logs/child-labor-laws-and-schooling-*, output/child-labor-laws-and-schooling-*, tickets/QUEUE.md, tickets/TICK-031-replicate-gacs-child-labor-schooling.md, handoff.md, session-log.md

## Description
Replicate the latest Gold-Anchored Clustered Search (GACS) procedure on the approved
`child-labor-laws-and-schooling` hypothesis before undertaking the linked mode-of-production
hypothesis. Build an independent cold-start gold instrument; distinguish child-labor restrictions,
compulsory schooling, and related human-capital mechanisms; calibrate the query without leakage; and
run a reproducible production search and screening funnel for the FDT estimand.

## Acceptance criteria
- [ ] The FDT hypothesis and primary/off-cell estimands are specified before screening.
- [ ] A DOI/title-keyed, provenance-recorded cold-start gold set is built from orthogonal sources and frozen after review.
- [ ] Query terms and breadth are calibrated without training/test leakage, with recall and candidate-budget results recorded.
- [ ] The live search is run reproducibly with caching, deduplication, and a search log.
- [ ] The deterministic and LLM screening funnel produces tiered topical and estimand-ready outputs.
- [ ] Studies belonging primarily to mode of production are routed to TICK-030 rather than combined with this estimand.
- [ ] Full-text extraction distinguishes child economic return, child quality cost, women's own opportunity cost, timing, knowledge/preferences, and mixed/unclear mechanisms before drafting.
- [ ] Full-text extraction records whether the law changes the prospective parent's schooling, the expected schooling of future children, or both.
- [ ] Cross-hypothesis lessons and any deviations from the documented GACS prototype are recorded.

## Log
- 2026-07-24, Alexandra/Codex: Added reproducible step 81 with 14 specification-level tempo-effect
  rows and a four-family pooling-readiness audit. No family meets the minimum of three independent
  studies with comparable estimates and standard errors; no pooled estimate was generated. The
  tempo draft now reports structured quantitative synthesis as the defensible endpoint pending
  Silles and further table extraction. The next human gate is acquisition of the 11 queued PDFs or
  authorization to proceed with a partial 6/16-source child-value chapter.
- 2026-07-24, Alexandra/Codex: Targeted repository search retrieved Hazan-Berdugo and
  Mookherjee-Prina-Ray, raising coverage to 14/25 overall and 6/16 in the child-value set. Both are
  direct formal-theory support for a child-labor-regulation/fertility mechanism. No retrieved
  empirical paper yet identifies that mechanism. Eleven sources remain queued (10 child-value;
  one tempo).
- 2026-07-24, Alexandra/Codex: Automated open-access retrieval and partial full-text synthesis.
  Steps 78-80 now retrieve/validate PDFs, extract cached text, and build verified evidence plus
  preliminary risk-of-bias tables. Coverage is 12/25 distinct approved sources overall, 9/10 for
  the compulsory-schooling tempo stream, and 4/16 for the child-economic-value set. Produced two
  chapter drafts. Thirteen sources remain on the explicit acquisition queue; 12 belong to the
  child-value set. Final mechanism adjudication, effect-level pooling, demographic scaling, and
  GRADE are blocked on those sources and/or later independent review.
- 2026-07-24, Alexandra/Codex: Reprocessed Alexandra's strict RA relevance decisions into two
  explicit paper sets via step 77. The child-economic-value set contains 16 distinct papers: 10
  theory/mechanism papers and 6 empirical quantum papers flagged as reduced-form pending full-text
  mechanism verification. The compulsory-schooling teenage-pregnancy/birth set contains 10
  empirical tempo papers. Three redundant versions were collapsed; Geruso-Royer is intentionally
  shared because it reports both teen and completed fertility.
- 2026-07-24, Alexandra/Codex: TICK-038 supersedes the earlier two-hypothesis routing. Compulsory
  schooling and teenage births is now the `COMPULSORY_SCHOOLING_TEENAGE_BIRTHS` evidence stream
  nested under `tempo-effects-birth-postponement`, not a standalone hypothesis. The child-economic-
  value quantum hypothesis remains separate.
- 2026-07-24, Alexandra/Codex: Started the post-split chapter pipeline. Added reproducible step 76,
  which generates separate retrieval manifests and pre-populated full-text extraction sheets for
  the child-economic-value and teenage-birth hypotheses. The current focused handoff routes 6
  candidate studies to the quantum workstream and 10 to the tempo workstream because Geruso-Royer
  explicitly reports both teen and completed fertility. Added a field guide with controlled
  mechanism/outcome vocabularies and fail-safe synthesis rules. All extraction fields remain blank
  pending PDFs; no full-text findings were inferred from abstracts.
- 2026-07-24, Alexandra/Codex: The combined hypothesis was split by TICK-032. Quantum records now
  route to `compulsory-education-child-economic-value`, where they count as reduced-form evidence
  unless the child-work-value mechanism is identified. Tempo records route to
  what was initially named `compulsory-education-teenage-births`. Existing combined-slug search artifacts remain the shared
  provenance record and must not be interpreted as a single estimand.
- 2026-07-16, Alexandra/Codex: Completed the entire pre-RA cold-start citation screen. Seven
  independently sourced anchors generated a 1,255-record DOI/title-deduplicated citation frame.
  All 32 blinded title/abstract batches were semantically screened and passed fail-closed schema,
  ordering, checksum, and coverage validation (1,255/1,255; zero errors): 233 RELEVANT, 128
  UNCERTAIN, and 894 NOT_RELEVANT. Generated the complete screened frame, estimand report, and
  exception-based RA review CSV. Work intentionally stops before RA adjudication and gold freeze.
- 2026-07-16, Alexandra/Codex: After RA spot review exposed false fertility-outcome classifications,
  applied a stricter evidence-grounded second pass to the 42-row focused set. The audit requires an
  explicit covered policy plus fertility outcome for empirical rows and a direct child-policy/fertility
  link for theory. It preserves RA annotations, routes adjacent evidence out, quarantines one metadata
  mismatch, and produces 28 strict retrieval candidates without overwriting the edited RA sheet.
- 2026-07-16, Alexandra/Codex: Converted Alexandra's completed strict RA review into the quantitative
  full-text retrieval handoff. The reproducible list contains 15 distinct empirical studies: 14 with
  resolved DOIs and one title-only working paper, split into 6 fertility-quantum and 9 fertility-tempo
  studies. Three redundant working-paper/version records were collapsed into their preferred published
  study. RA-corrected theory rows remain outside the meta-analysis retrieval list.
