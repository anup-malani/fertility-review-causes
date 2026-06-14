# TICK-003: Promote batch-edits lesson to decisions/
**Status:** open
**Assigned:** any
**Parallel-safe:** yes
**Blocks:** —
**Blocked by:** —

## Description

A reusable design lesson was identified in the 2026-06-10 session: workflow agents that make
many sequential Edit calls to a single file are fragile and stall. The better pattern is to
have the agent return all edits as structured data and apply them programmatically (via a
script or a single Write call). This should be documented as a durable decision so every
future workflow is designed correctly from the start.

Create `decisions/2026-06-10-batch-edits-via-script-not-agent.md` with the lesson,
rationale, and the recovery pattern used in the `annotate-hypotheses` workflow.

## Acceptance criteria
- [ ] `decisions/2026-06-10-batch-edits-via-script-not-agent.md` created
- [ ] Covers: the failure mode, the correct pattern, the recovery pattern, when exceptions are acceptable
- [ ] Committed

## Log
<!-- Append completion note here when done. -->
