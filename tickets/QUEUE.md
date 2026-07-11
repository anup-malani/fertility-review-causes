# Work Queue

Last updated: 2026-07-11

Pick the first open ticket assigned to you or `any`. Before starting, pull/sync, then **claim** it
(move its row to **In progress** below) before doing the work — using whichever mode is active in
`README.md` (Mode A pushes the claim to `main`; Mode B pushes a `tick-NNN-*` branch). Do not start
a blocked ticket until its dependency is done. Parallel-safe tickets can be worked concurrently.

---

## Open — can start now

| Ticket | Title | Assigned | Parallel-safe |
|--------|-------|----------|---------------|
| [TICK-020](TICK-020-oas-theory-stream.md) | OAS theory stream for JEL-style mechanism section | any | yes |
| [TICK-002](TICK-002-cultural-count-fix.md) | Fix Cultural-count in Merge Notes | any | yes |
| [TICK-003](TICK-003-promote-batch-edits-lesson.md) | Promote batch-edits lesson to decisions/ | any | yes |
| [TICK-004](TICK-004-gitignore-workflows.md) | Revisit .gitignore for .claude/workflows/ | any | yes |
| [TICK-001](TICK-001-hypotheses-review.md) | PI review of HYPOTHESES.md | Anup | yes |
| [TICK-005](TICK-005-protocol-readability-pass.md) | PI + RA readability pass on PROTOCOL.md + RA-PLAYBOOK.md | Anup + RAs | yes |

## In progress — claimed, do not duplicate

| Ticket | Title | Owner | Claimed (UTC) | Touches |
|--------|-------|-------|---------------|---------|

## Blocked — waiting on dependency

| Ticket | Title | Assigned | Blocked by |
|--------|-------|----------|------------|
| [TICK-006](TICK-006-osf-preregistration.md) | OSF pre-registration | Anup | TICK-001, TICK-005 |
| [TICK-009](TICK-009-literature-search-mjs.md) | Implement literature-search.mjs | any | TICK-001 |
| [TICK-012](TICK-012-prepilot-time-cost.md) | Pre-pilot (Anup + Claude): time-cost/income-substitution | Anup + Claude | TICK-001, TICK-009 |
| [TICK-010](TICK-010-pilot-run.md) | RA pilot Phase 1: old-age security/pensions | All three | TICK-012 |
| [TICK-019](TICK-019-oas-demographic-significance-and-chapter.md) | OAS demographic significance and hybrid chapter draft | any | TICK-020; demographic-significance macro pass |

## Done

| Ticket | Title | Closed |
|--------|-------|--------|
| [TICK-007](TICK-007-gift-shravan-claude-max.md) | Gift Shravan Claude Max | 2026-06-14 |
| [TICK-011](TICK-011-hypotheses-recategorization.md) | Recategorize HYPOTHESES.md | 2026-06-14 (merged into TICK-001) |
| [TICK-008](TICK-008-collab-system-design.md) | Design team collaboration/ticketing system | 2026-06-14 |
| [TICK-013](TICK-013-agent-interop-doc.md) | Document Claude / Codex interop | 2026-06-27 |
| [TICK-014](TICK-014-meta-analysis-paper-pipeline-design.md) | Design meta-analysis-to-paper pipeline | 2026-07-03 |
| [TICK-015](TICK-015-oas-fulltext-screen.md) | OAS full-text screen and retrieval reconciliation | 2026-07-03 |
| [TICK-016](TICK-016-oas-data-extraction.md) | OAS full-text data extraction | 2026-07-09 |
| [TICK-017](TICK-017-oas-risk-of-bias.md) | OAS risk-of-bias assessment | 2026-07-09 |
| [TICK-018](TICK-018-oas-effect-harmonization-meta-analysis.md) | OAS effect harmonization and meta-analysis | 2026-07-09 |
| [TICK-021](TICK-021-oas-target-period-derivation.md) | Derive OAS target-period relevance from verified study windows | 2026-07-09 |
| [TICK-022](TICK-022-oas-multi-outcome-effect-extraction.md) | OAS multi-outcome effect extraction | 2026-07-10 |
| [TICK-023](TICK-023-oas-review-sheet-source-columns.md) | OAS effect review sheet source columns | 2026-07-10 |
| [TICK-024](TICK-024-oas-adjudicate-effect-review.md) | OAS adjudicate effect extraction review | 2026-07-10 |
| [TICK-025](TICK-025-oas-meta-analysis-readiness.md) | OAS meta-analysis readiness analysis | 2026-07-11 |
| [TICK-026](TICK-026-oas-sign-orientation-treatment-scale.md) | OAS sign orientation and treatment-scale coding | 2026-07-11 |
| [TICK-027](TICK-027-oas-pooling-rule.md) | OAS conservative pooling rule | 2026-07-11 |
| [TICK-028](TICK-028-oas-tfr-transition-classification.md) | OAS TFR-based transition classification | 2026-07-11 |
