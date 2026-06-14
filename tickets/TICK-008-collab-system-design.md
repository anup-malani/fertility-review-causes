# TICK-008: Design team collaboration / ticketing system
**Status:** open
**Assigned:** Shravan
**Parallel-safe:** yes
**Blocks:** —
**Blocked by:** —

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
<!-- Append completion note here when done. -->
