# TICK-008: Design team collaboration / ticketing system
**Status:** done  
**Assigned:** Shravan  
**Parallel-safe:** yes  
**Blocks:** —  
**Blocked by:** —  
**Touches:** `tickets/`, `decisions/2026-06-14-collab-system-design.md`

## Description

**Background.** Three humans (Anup PI, Alexandra on Codex, Shravan on Claude Max) share one
GitHub repo and may be working on different hypotheses or pipeline stages simultaneously. We
need a lightweight system that:

- Tracks who is working on what
- Makes dependencies explicit (parallel vs. sequential)
- Lets people pick up and log work without stepping on each other
- Works for any AI assistant (Claude, Codex, or future tools)
- Lives in the repo as markdown files (not an external tool)

An initial ticket system has been scaffolded in `tickets/` (this file is part of it). Shravan's
job is to evaluate and improve it, and optionally to propose a coordination layer on top.

**The two problems Anup identified at the kickoff:**

1. **Ticketing / parallel-tracks:** a system for organizing parallel work so people don't
   duplicate effort. The `tickets/` directory is a starting point.

2. **Orchestration / conversation:** a method for the AI (or a human) to coordinate across
   multiple contributors — knowing what everyone else is doing, detecting conflicts. This is
   harder and may require a lightweight shared state file or a coordinator role.

**Shravan's assignment:**

1. Read the current `tickets/` system (README.md, QUEUE.md, TICK-*.md files).
2. Evaluate whether it solves problem #1 adequately or needs changes.
3. Propose a solution to problem #2 (orchestration/coordination). Alexandra suggested using
   Superpowers to help design this; Anup confirmed the system must be LLM-agnostic.
4. Document the proposal in `decisions/2026-06-14-collab-system-design.md`.
5. Implement any changes to `tickets/` that come out of the proposal.

**Constraints:**
- LLM-agnostic: must work whether a team member uses Claude, Codex, or switches between them
- Git-native: state lives in files, not a third-party service
- Low overhead: RAs should spend most of their time doing research, not managing the system

## Acceptance criteria
- [ ] Current `tickets/` system evaluated (is it sufficient for problem #1?)
- [ ] Proposal for coordination/orchestration (problem #2) documented
- [ ] Changes to `tickets/` implemented if needed
- [ ] `decisions/2026-06-14-collab-system-design.md` written
- [ ] Committed

## Log

**2026-06-14 — Shravan (Claude Code).** Evaluated the existing `tickets/` system: adequate for
problem #1 (dependency tracking via `Blocked by`/`Blocks`, `Parallel-safe`, QUEUE.md open/blocked/
done split) — no redesign warranted; only weakness is QUEUE↔ticket dependency drift, a discipline
issue. For problem #2 (coordination), wrote `decisions/2026-06-14-collab-system-design.md`: a
pure-convention, git-native **claim-commit** protocol — pull → check → claim → push the claim
*before* doing work, so a rejected push surfaces collisions. Added a `Touches:` field (related-work
conflict surface) and a 24h stale-claim rule. Rejected a dedicated `ACTIVE.md` (folded the live
view into QUEUE.md to avoid a third drifting source of truth), an external tool, and a helper
script. Implemented per PI parameters (no branch workflow, pure convention, conservative changes):
updated `tickets/README.md` (session loop with claiming, stale rule, template `Touches:` field,
honest "does/doesn't solve" section) and `tickets/QUEUE.md` (new **In progress** section).
Documented the branch-per-ticket upgrade (Option 2) as the strongest future option if we adopt a
branch workflow. Dogfooded the protocol by claiming this ticket under it.
