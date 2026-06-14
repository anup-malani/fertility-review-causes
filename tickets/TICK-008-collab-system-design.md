# TICK-008: Design team collaboration / ticketing system
**Status:** in-progress  
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
- [x] Current `tickets/` system evaluated (is it sufficient for problem #1?)
- [x] Proposal for coordination/orchestration (problem #2) documented
- [x] Changes to `tickets/` implemented if needed
- [x] `decisions/2026-06-14-collab-system-design.md` written
- [x] **Implementation into the workstream documented and wired in**: the decision actually modifies
      future behavior — the decision doc specifies *how* both modes plug into our artifacts and
      routines, and the enacting edits are made (see Log).
- [x] **Mode B implemented as the active mode** (branch-per-ticket), with a helper to minimize effort.
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

**2026-06-14 (reopened) — Shravan (Claude Code).** Reopened to `in-progress` per PI feedback: a
ticket is not finished when the solution is written — it is finished when the result is stated *and*
it actually changes our future behavior. The first pass produced the design (the two co-equal modes)
but stopped short of wiring it into the repo's behavior-governing files. Added **Part 3 —
Implementing this into our workstream** to `decisions/2026-06-14-collab-system-design.md`: a concrete
map from the two-mode design onto our existing artifacts (AGENTS.md session-start, `tickets/README.md`
as the canonical loop and single mode-of-record, RA-PLAYBOOK.md cadence, the piloting phases as the
review triggers) plus a generalized **ticket-closure rule** that institutionalizes the result-and-
behavior-change test for every future ticket. Enacted the plan with edits to AGENTS.md, RA-PLAYBOOK.md,
and tickets/README.md. Left `in-progress` pending confirmation at the next sync before re-closing.

**2026-06-14 (Mode B adopted) — Shravan (Claude Code).**

**Result.** Switched the team's active coordination mode from A (push-to-main) to **B
(branch-per-ticket with PR merge)** and added a thin helper so the heavier loop costs almost no
manual git. Each ticket is now worked on its own `tick-NNN-slug` branch — the pushed branch *is* the
claim — and merged via PR, so `main` stays clean and every change gets a review gate before parallel
tracks begin.

**Workflow impact / future behavior.**
- Changes future behavior? **Yes** — this is now how everyone claims, works, and closes tickets.
- Implemented in: `tickets/README.md` (active-mode line flipped to B; Mode B promoted to the leading
  loop, Mode A demoted to documented fallback; **Using the helper** section; Mode history + switch
  note), `scripts/ticket.sh` (new `claim` / `submit` / `close` helper), `tickets/QUEUE.md` (board now
  records the branch as the claim; header points to the helper), `AGENTS.md` (Tickets + Commits
  conventions), `RA-PLAYBOOK.md` (pipeline-operator step zero),
  `decisions/2026-06-14-collab-system-design.md` (Solution B highlighted as active; Switch log; helper
  re-adopted; §3.3/§3.4 updated).
- Do differently: claim with `scripts/ticket.sh claim NNN` (creates + pushes the branch), work on
  that branch, `submit` to open the PR, write the `## Log` (Result + Workflow impact), then `close`
  to merge + delete the branch. Do not commit ticket work directly to `main` while Mode B is active.
  To switch modes later, edit only the `Current mode:` line in `tickets/README.md`, add a Mode
  history entry, and a Switch-log line in the decision doc.

Branches are created per ticket *at claim time* (the branch is the claim), so unstarted tickets were
intentionally **not** pre-branched — doing so would falsely mark them as taken. The active branch for
this ticket is `tick-008-collab-system-design`. Left `in-progress` pending confirmation at the next
sync.
