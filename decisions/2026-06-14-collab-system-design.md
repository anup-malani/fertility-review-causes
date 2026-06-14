# Decision: Team collaboration / coordination system

**Date:** 2026-06-14

**Author:** Shravan Haribalaraman (RA)

**Decided by:** Shravan (TICK-008); pending PI confirmation at next sync

**Status:** Active — applies to all contributors (Anup, Alexandra, Shravan) and any AI assistant

**Review trigger (milestone, not a fixed date):** Revisit once the system has actually faced
concurrent work — concretely, at the **close of the RA pilot (Phase 1)**, when all three
contributors have worked one hypothesis together (or earlier if collisions surface during it).
Re-confirm again **once Phase 2 parallel tracks are underway**, since separate hypotheses on a
shared `main` exercise a different collision mode than everyone editing one hypothesis. The point
is to review on evidence of real concurrent load, not on the calendar.

## Context

Three humans share one private GitHub repo, each driving a different AI assistant (Anup PI;
Alexandra on Codex Pro; Shravan on Claude Max). Once parallel tracks begin (Phase 2 of the
piloting sequence — see `decisions/2026-06-14-piloting-sequence.md`), they may work different
hypotheses or pipeline stages at the same time. TICK-008 asks for a lightweight system that
solves **two separate problems** (framing from `handoff.md`):

1. **Ticketing / parallel tracks** — track who is doing what; make task dependencies explicit;
   let people pick up and log work without duplicating effort.
2. **Orchestration / coordination** — know what another contributor is doing mid-session and
   detect conflicts when two people touch related work at the same time.

**Hard constraints (from the ticket):**

- **LLM-agnostic** — must work whether a contributor uses Claude, Codex, or switches tools.
- **Git-native** — state lives in version-controlled files, not a third-party service.
- **Low overhead** — contributors should spend their time on research, not on managing the system.

**PI-set parameters for this design (2026-06-14):**

- Pure convention — no helper scripts; markdown + git discipline only.
- Keep changes to `tickets/` conservative; do not redesign the working system.
- Stale-claim threshold: 24h.
- **Current operating mode: push-to-main (Solution A).** The PI chose push-to-main for now. This
  doc specifies the branch-per-ticket alternative (Solution B) as a **co-equal, ready-to-adopt**
  solution — not a someday upgrade. The team runs one mode at a time and may switch by decision.

## Part 1 — Evaluation of problem #1 (the existing `tickets/` system)

**Verdict: adequate. It solves problem #1 and should not be redesigned.**

The `tickets/` directory already encodes everything problem #1 needs:

- Per-ticket `Blocked by` / `Blocks` fields capture serial dependencies; the canonical hard case
  (Task C waits on *both* 2A and 2B) is expressible and is in fact used (e.g. TICK-006 blocked by
  TICK-001 **and** TICK-005).
- `Parallel-safe: yes|no` flags which tickets can run concurrently.
- `QUEUE.md` separates **Open** (start now) from **Blocked** (wait) from **Done**.
- The three-file loop in `tickets/README.md` (read QUEUE → open ticket → do work → close + log)
  is simple and tool-neutral.

The only problem-#1 weakness is **drift**: dependency state is duplicated between `QUEUE.md` and
the individual ticket files, and the two can disagree (this already happened during the
TICK-010/011/012 reshuffle). This is a maintenance discipline issue, not a design flaw, and the
coordination protocol below (single claim commit, QUEUE.md as the board) reduces rather than adds
to it. No structural change to dependency tracking is warranted.

## Part 2 — Problem #2 (coordination): two co-equal solutions

The named failure mode is **two contributors picking up the same ticket at the same time**, plus
conflicts when two people touch related work simultaneously.

**The honest limitation up front:** a git-native system *cannot* provide true real-time locking.
Shared state does not exist until someone pushes and someone else pulls. There is always a window
between "A starts work" and "B can possibly see it." So the achievable goal is not to *eliminate*
the race but to **make the window small, make collisions visible, and make recovery cheap.** Both
solutions below accept this; they differ in *how small* the window is and *where* collisions surface.

We specify **two co-equal solutions**, not a default plus a fallback. Each is fully developed and
ready to run; each is best suited to a different level of concurrency. The team runs **one mode at
a time** — mixing them mid-stream breaks coordination — and switching is a team decision, not a
redesign, because both reuse the same ticket/QUEUE/`Touches` scaffolding. As of 2026-06-14 the
team operates in **Solution A** per PI choice; **Solution B** is equally specified and ready to
adopt the moment parallel load warrants it.

### Options surveyed

Three options were rejected; the two that survived are developed in full below as Solutions A and B.

- **External coordination tool** (Linear, GitHub Projects, a Slack bot). Rejected — violates
  git-native, and a tool with its own UI is not equally usable by every AI assistant. Slack was
  already deferred for this project.
- **A dedicated live board file (`tickets/ACTIVE.md`).** Rejected — a *second* source of truth
  alongside ticket `Status` and `QUEUE.md`, a third place to update per claim and a third place to
  drift. `QUEUE.md` already serves as the board; the live view belongs there.
- **A helper script to automate claiming** (`scripts/claim.sh`). Rejected — violates pure
  convention, and a script is a dependency each assistant must shell out to and parse, versus a
  protocol any assistant can simply follow.

### Shared scaffolding (used by both solutions)

- **`Touches:` field** on each ticket — the files/paths a ticket will modify. The surface for
  detecting *related-work* conflicts without reading every ticket body. Best-effort, not exhaustive.
- **`QUEUE.md` **In progress** board** — the single live view of who holds what, with an `owner`
  and a `claimed (UTC)` timestamp. The timestamp lives only here (one location, cannot drift).
- **Stale-claim rule (24h)** — a claim with no new commits for >24h is reclaimable: pull, release
  or take it over, note the reclaim in the ticket `## Log`. Prevents an abandoned session from
  blocking a ticket forever.

The two solutions differ only in the **claim mechanism**.

### Solution A — Claim-commit on push-to-main

The claim is a **tiny status change pushed to `main` before the work starts**; `git push` rejection
is the collision detector. Session loop:

1. **Pull first.** `git pull` so you are on the latest state.
2. **Check for conflicts.** In `QUEUE.md`'s **In progress** section, confirm (a) no one has claimed
   your ticket and (b) no active claim's `Touches:` overlaps the files you will edit.
3. **Claim.** Set the ticket `Status: in-progress` + your name; move its row from **Open** to
   **In progress** in `QUEUE.md` with `owner` and `claimed (UTC)`.
4. **Commit and push the claim immediately**, *before* the substantive work
   (`git commit -m "claim TICK-NNN" && git push`). This is the whole mechanism.
   - If the push is **rejected**, someone pushed first. `git pull`. If they claimed your ticket,
     they win — pick another. If it is unrelated, re-apply your claim and push again.
5. **Do the work**, committing as you go (those commits double as a liveness signal).
6. **Close.** `Status: done`, `## Log` note, move the row to **Done** in `QUEUE.md`, commit and push.

**Best when:** concurrency is low and contributors mostly touch different files. **Cost:** one
early push and one moved line over today's loop — minimal.

### Solution B — Branch-per-ticket with PR merge

The claim is a **pushed branch** named for the ticket, not a shared-file edit. A remote branch
*is* the claim — visible, timestamped, and self-documenting. Session loop:

1. **Sync `main`.** `git checkout main && git pull`.
2. **Check for conflicts.** `git branch -r` plus the **In progress** board: if `tick-NNN-*` already
   exists on `origin`, the ticket is taken. Also check `Touches:` overlap with other live branches.
3. **Claim.** `git checkout -b tick-NNN-slug`, set the ticket `Status: in-progress` + your name and
   add its **In progress** row, then **push the branch immediately**: `git push -u origin tick-NNN-slug`.
   The pushed branch is the claim; first to push wins, and a name clash is rejected by the remote.
4. **Do the work on the branch**, committing as you go. In-progress work is visible to everyone via
   `git branch -r` the *moment you push* — not only when you finish.
5. **Open a PR into `main`.** Overlapping edits with another ticket surface as PR merge conflicts,
   resolved at review time on the branch and never colliding directly on `main`. The PR also gives a
   natural review checkpoint.
6. **Close.** Merge the PR, set `Status: done`, `## Log` note, move the row to **Done**, delete the
   branch.

(The 24h stale rule applies to branches identically: a `tick-NNN-*` branch with no commits in 24h
is reclaimable — take it over or delete it, note in the `## Log`.)

**Best when:** multiple contributors work concurrently, *especially* if they may touch the same
files. **Cost:** branch + PR overhead per ticket — higher than Solution A, paid back as soon as
real parallel load makes shared-`main` collisions frequent.

## Rationale

- **Both are git-native and LLM-agnostic.** Each reuses plain `git` as the coordination primitive,
  so any assistant that can run `git` can participate, with no external service and no tool-specific
  dependency.
- **They share scaffolding, so switching is cheap.** Ticket `Status`, the `QUEUE.md` board, the
  `Touches:` field, and the 24h rule are identical across both. Moving between modes changes only
  the claim mechanism, not the rest of the system — which is *why* they can be co-equal rather than
  a one-way upgrade.
- **A is the smallest thing that works at low concurrency.** It reuses git's push/pull/reject as
  the lock, adds no new file, and costs almost nothing over today's loop.
- **B is the strongest thing at high concurrency.** The pushed branch is an isolated, timestamped
  claim that makes in-progress work visible *and* removes shared-`main` contention, with a PR review
  checkpoint as a bonus. Its cost (branch + PR per ticket) is only worth paying once collisions are
  real — which is exactly the condition under which A starts to hurt.
- **One source of truth either way.** The live view lives in `QUEUE.md` (not a new `ACTIVE.md`),
  keeping status in the file people already maintain.

## Risks and mitigations

**Solution A**

- **Residual race (sub-second simultaneous claims).** Both pull, both claim, both push at the same
  instant: the second push is rejected and that person pulls and backs off. The window is seconds,
  and the failure is caught, not silent.
  *Proposed mitigation: accept it as the irreducible cost of push-to-main; the rejected push already
  catches it. Frequent recurrence is itself the signal to switch to Solution B.*
- **`QUEUE.md` becomes a contention point.** Every claim edits one shared file.
  *Proposed mitigation: keep claims tiny and push immediately so the contended window stays small;
  treat a `QUEUE.md` conflict as the intended detector, not a failure, and resolve it in git.*

**Solution B**

- **Overhead and discipline.** Branch + PR per ticket is more steps; contributors unfamiliar with
  PR-based git may stumble.
  *Proposed mitigation: reserve Solution B for when parallel load justifies it; document the
  six-step branch loop in `README.md` so the steps are mechanical, not improvised.*
- **Stale branches accumulate.** Abandoned `tick-NNN-*` branches clutter the remote.
  *Proposed mitigation: apply the 24h stale rule to branches; delete branches on merge as step 6.*

**Both**

- **Forgotten pull/sync before work.** Skipping the first step risks duplicated effort.
  *Proposed mitigation: make pull/sync the explicit first step in `README.md` (done), and have each
  contributor's AI treat it as a standing session-start instruction; the cost is a wasted session,
  not corrupted data.*
- **`Touches:` drift / under-specification.** A ticket may touch files not listed.
  *Proposed mitigation: keep `Touches:` advisory and lean on the merge conflict as the real
  backstop; update it whenever a ticket's scope visibly grows.*
- **Convention decay.** Pure-convention systems rot if unenforced.
  *Proposed mitigation: keep both loops short and in `README.md`; revisit at the milestone review
  (see header), and if discipline slips, add a thin LLM-agnostic helper to enforce whichever mode
  is in effect.*

## What each solution does and does not solve

| Limitation | Solution A (push-to-main) | Solution B (branch-per-ticket) |
|---|---|---|
| Same-ticket collision | Caught by rejected push (seconds-wide race) | Caught by branch-name clash on push |
| Awareness of *uncommitted* in-session work | Not solved — invisible until a claim is pushed | **Solved** — pushing the branch at session start makes work visible via `git branch -r` |
| Two tickets editing one shared file | Surfaces as a conflict directly on `main` | **Solved** — resolved at PR review on the branch, never on `main` |
| Review checkpoint before merge | None | **Built in** via the PR |
| Overhead | Minimal | Branch + PR per ticket |

Neither solution closes the *uncommitted-local-work* gap completely: until something is pushed
(a claim in A, a branch in B), other contributors cannot see it. B shrinks this gap to the start of
the session rather than its end; A shrinks it to the first claim push. The pull/sync-first step is
what makes either gap small.

## Choosing and switching between the two modes

Both modes are first-class and ready. The team operates one at a time:

1. **Start in Solution A** (current PI choice) while concurrency is low — it is the lighter mode.
2. **Switch to Solution B** when parallel work makes shared-`main` collisions or same-file conflicts
   frequent, or when the team wants a PR review gate. The milestone review (see header) — close of
   the RA pilot, and again once Phase 2 parallel tracks are underway — is the natural point to make
   this call **on evidence**, not anticipation.
3. The switch is a team decision recorded here; because both modes share scaffolding, it costs no
   rework beyond agreeing on the date and everyone adopting the same loop.

The throughline: two co-equal, fully-specified modes; pick the one the observed concurrency
justifies, and switch deliberately rather than drifting between them.
