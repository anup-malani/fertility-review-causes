# Work Queue

Last updated: 2026-06-14

Pick the first open ticket assigned to you or `any`. Before starting, pull/sync, then **claim** it
before doing the work. The active mode is **Mode B (branch-per-ticket)** — the simplest path is
`scripts/ticket.sh claim NNN`, which creates and pushes the `NNN-slug` branch and flips the
ticket status; then move its row to **In progress** below. (See `README.md` for the full loop and
the Mode A fallback.) Do not start a blocked ticket until its dependency is done. Parallel-safe
tickets can be worked concurrently.

---

## Open — can start now

| Ticket | Title | Assigned | Parallel-safe |
|--------|-------|----------|---------------|
| [TICK-002](TICK-002-cultural-count-fix.md) | Fix Cultural-count in Merge Notes | any | yes |
| [TICK-003](TICK-003-promote-batch-edits-lesson.md) | Promote batch-edits lesson to decisions/ | any | yes |
| [TICK-004](TICK-004-gitignore-workflows.md) | Revisit .gitignore for .claude/workflows/ | any | yes |
| [TICK-001](TICK-001-hypotheses-review.md) | PI review of HYPOTHESES.md | Anup | yes |
| [TICK-005](TICK-005-protocol-readability-pass.md) | PI + RA readability pass on PROTOCOL.md + RA-PLAYBOOK.md | Anup + RAs | yes |

## In progress — claimed, do not duplicate

| Ticket | Title | Owner | Branch (the claim) | Claimed (UTC) | Touches |
|--------|-------|-------|--------------------|---------------|---------|
| [TICK-008](TICK-008-collab-system-design.md) | Design collab/ticketing system (Mode B implementation) | Shravan | `008-collab-system-design` | 2026-06-14 20:43 | `tickets/`, `decisions/2026-06-14-collab-system-design.md`, `AGENTS.md`, `RA-PLAYBOOK.md`, `scripts/ticket.sh` |

## Blocked — waiting on dependency

| Ticket | Title | Assigned | Blocked by |
|--------|-------|----------|------------|
| [TICK-006](TICK-006-osf-preregistration.md) | OSF pre-registration | Anup | TICK-001, TICK-005 |
| [TICK-009](TICK-009-literature-search-mjs.md) | Implement literature-search.mjs | any | TICK-001 |
| [TICK-012](TICK-012-prepilot-time-cost.md) | Pre-pilot (Anup + Claude): time-cost/income-substitution | Anup + Claude | TICK-001, TICK-009 |
| [TICK-010](TICK-010-pilot-run.md) | RA pilot Phase 1: old-age security/pensions | All three | TICK-012 |

## Done

| Ticket | Title | Closed |
|--------|-------|--------|
| [TICK-007](TICK-007-gift-shravan-claude-max.md) | Gift Shravan Claude Max | 2026-06-14 |
| [TICK-011](TICK-011-hypotheses-recategorization.md) | Recategorize HYPOTHESES.md | 2026-06-14 (merged into TICK-001) |
| ~~[TICK-008]~~ | _reopened 2026-06-14 — now In progress (workstream implementation + Mode B)_ | — |
