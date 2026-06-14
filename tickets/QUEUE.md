# Work Queue

Last updated: 2026-06-14 (updated)

Pick the first open ticket assigned to you or `any`. Do not start a blocked ticket until its
dependency is done. Parallel-safe tickets can be worked concurrently.

---

## Open — can start now

| Ticket | Title | Assigned | Parallel-safe |
|--------|-------|----------|---------------|
| [TICK-002](TICK-002-cultural-count-fix.md) | Fix Cultural-count in Merge Notes | any | yes |
| [TICK-003](TICK-003-promote-batch-edits-lesson.md) | Promote batch-edits lesson to decisions/ | any | yes |
| [TICK-004](TICK-004-gitignore-workflows.md) | Revisit .gitignore for .claude/workflows/ | any | yes |
| [TICK-008](TICK-008-collab-system-design.md) | Design team collaboration/ticketing system | Shravan | yes |
| [TICK-001](TICK-001-hypotheses-review.md) | PI review of HYPOTHESES.md | Anup | yes |
| [TICK-005](TICK-005-protocol-readability-pass.md) | PI + RA readability pass on PROTOCOL.md + RA-PLAYBOOK.md | Anup + RAs | yes |

## Blocked — waiting on dependency

| Ticket | Title | Assigned | Blocked by |
|--------|-------|----------|------------|
| [TICK-006](TICK-006-osf-preregistration.md) | OSF pre-registration | Anup | TICK-001, TICK-005 |
| [TICK-009](TICK-009-literature-search-mjs.md) | Implement literature-search.mjs | any | TICK-001 |
| [TICK-010](TICK-010-pilot-run.md) | Run pilot on quantity-quality tradeoff | any | TICK-009 |
| [TICK-011](TICK-011-hypotheses-recategorization.md) | Recategorize HYPOTHESES.md (root vs proximate) | Claude → Anup | TICK-001 |

## Done

| Ticket | Title | Closed |
|--------|-------|--------|
| [TICK-007](TICK-007-gift-shravan-claude-max.md) | Gift Shravan Claude Max | 2026-06-14 |
