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

- No branch workflow for now — everyone continues to push to `main`.
- Pure convention — no helper scripts; markdown + git discipline only.
- Keep changes to `tickets/` conservative; do not redesign the working system.
- Stale-claim threshold: 24h.

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

## Part 2 — Problem #2 (coordination) and the fundamental limitation

The named failure mode is **two contributors picking up the same ticket at the same time**, plus
conflicts when two people touch related work simultaneously.

**The honest limitation up front:** a git-native system *cannot* provide true real-time locking.
Shared state does not exist until someone pushes and someone else pulls. There is always a window
between "A starts work" and "B can possibly see it." So the achievable goal is not to *eliminate*
the race but to **make the window small, make collisions visible, and make recovery cheap.** Any
design claiming more than that would be dishonest given the constraints. We accept the residual
race and handle it explicitly rather than pretend it is gone.

### Options considered

1. **External coordination tool** (Linear, GitHub Projects, a Slack bot, a shared doc).
   Rejected — violates git-native; and a tool with its own UI/affordances is not equally usable
   by every AI assistant (LLM-agnostic). Slack was already deferred for this project.

2. **Branch-per-ticket, coordinate via remote branches** (`git branch -r` shows in-progress work).
   This is the strongest *technical* answer — work is isolated, and a pushed branch is a visible,
   timestamped claim. Rejected for now by PI decision (no branch workflow). Recorded here as the
   natural upgrade path if push-to-main collisions become frequent.

3. **A dedicated live board file (`tickets/ACTIVE.md`).** A single file listing who is active on
   what. Considered and **rejected** — it would be a *second* source of truth alongside ticket
   `Status` and `QUEUE.md`, adding a third place to update per claim and a third place to drift.
   `QUEUE.md` is already the file every contributor reads at session start; the live view belongs
   there, not in a new file.

4. **Claim-commit discipline, with `QUEUE.md` as the live board.** Chosen — see below.

5. **A helper script to automate claiming** (`scripts/claim.sh`). Rejected by PI decision (pure
   convention). A script also subtly works against LLM-agnosticism: it becomes a dependency each
   assistant must shell out to and parse, versus a protocol any assistant can simply follow.

### Decision — Option 4: claim-commit discipline on `QUEUE.md`

Coordination is achieved by a **claim commit**: a contributor announces work by committing and
pushing a tiny status change *before doing the work*, using `git push` rejection as the collision
detector. Concretely, the session loop becomes:

1. **Pull first.** `git pull` so you are looking at the latest state.
2. **Check for conflicts.** In `QUEUE.md`'s new **In progress** section, confirm (a) no one has
   claimed your ticket, and (b) no active claim's `Touches:` paths overlap the files you will edit.
3. **Claim.** Set the ticket's `Status: in-progress` and add your name; move its row from **Open**
   to **In progress** in `QUEUE.md` with an `owner` and a `claimed (UTC)` timestamp.
4. **Commit and push the claim immediately** — *before* doing the substantive work
   (`git commit -m "claim TICK-NNN" && git push`). This is the whole coordination mechanism.
   - If the push is **rejected**, someone pushed first. `git pull`. If they claimed your ticket,
     they win — pick another. If it is an unrelated change, re-apply your claim and push again.
5. **Do the work**, committing as you go (those commits double as a liveness signal).
6. **Close.** `Status: done`, write the `## Log` note, move the row to **Done** in `QUEUE.md`,
   commit and push.

Supporting rules:

- **`Touches:` field** is added to the ticket template — the files/paths a ticket will modify. It
  is the surface for detecting *related-work* conflicts (problem #2's second half) without reading
  every ticket body. Best-effort, not exhaustive.
- **Stale-claim rule (24h).** A claim is stale if it has been `in-progress` for more than 24h with
  no new commits referencing it. Anyone may reclaim a stale ticket: pull, set it back to `open` (or
  re-claim it), and note the reclaim in the ticket `## Log`. This prevents an abandoned session
  from blocking a ticket forever.
- **`claimed (UTC)` timestamp** lives only in the `QUEUE.md` **In progress** row (single location),
  so it cannot drift against a copy in the ticket file.

## Rationale

- **It is the smallest thing that works.** The claim commit reuses git's existing
  push/pull/reject machinery as the lock. No new tooling, no new file, nothing tool-specific —
  any assistant that can run `git` can participate, satisfying LLM-agnostic + git-native at once.
- **Collisions become visible exactly where they must be resolved.** A rejected push *is* the
  conflict signal; a markdown merge conflict on the `QUEUE.md` In-progress row is trivial to read
  and resolve, and it surfaces the race instead of hiding it.
- **Low overhead.** The added cost over today's loop is one early `git push` and one line moved
  in `QUEUE.md`. Contributors already read `QUEUE.md` first thing, so the live board costs nothing
  to consult.
- **One source of truth.** Folding the live view into `QUEUE.md` (rather than a new `ACTIVE.md`)
  keeps status in the file people already maintain and avoids a third drifting copy.

## Risks and mitigations

- **Residual race (sub-second simultaneous claims).** Two people who both pull, both claim, and
  both push within the same instant: the second push is rejected and that person pulls and backs
  off. The window is the time between pull and push of a one-line change — seconds — and the
  failure is caught, not silent.
  *Proposed mitigation: accept it as the irreducible cost of a git-native design; the rejected
  push already catches it. If sub-second collisions ever recur, that is the signal to move to
  branch-per-ticket (Option 2), where the claim is a pushed branch rather than a shared-file edit.*
- **Forgotten pull-before-work.** If someone skips step 1, they may duplicate effort.
  *Proposed mitigation: make `git pull` the explicit first step of the loop in `README.md` (done),
  and have each contributor's AI assistant treat "pull before claiming" as a standing
  session-start instruction; the cost of a missed pull is a wasted session, not corrupted data.*
- **`Touches:` drift / under-specification.** A ticket may touch files not listed.
  *Proposed mitigation: keep `Touches:` advisory rather than authoritative, and lean on the merge
  conflict as the real backstop; update `Touches:` whenever a ticket's scope visibly grows.*
- **`QUEUE.md` itself becomes a contention point.** Every claim edits one shared file.
  *Proposed mitigation: keep claims tiny and push them immediately so the contended window stays
  small; treat a conflict on `QUEUE.md` as the intended detector, not a failure, and resolve it in
  git.*
- **Convention decay.** Pure-convention systems rot if unenforced.
  *Proposed mitigation: keep the loop short and in `README.md`, and re-evaluate at the milestone
  review (see header) — if collisions prove common, adopt branch-per-ticket (Option 2) or a thin helper script
  to enforce the protocol mechanically.*

## What this does NOT solve

Each limit below is paired with a **proposed change** that is *recorded but deliberately not
implemented now* — the team should adopt it only if the limit actually bites in practice.

- **True real-time awareness of another contributor's *uncommitted* in-session work.** If A is
  editing files locally and has not pushed a claim, B cannot see it. The claim-before-work step
  shrinks this gap; it does not close it.
  - *Proposed change (not implemented): move to branch-per-ticket (Option 2) and push the branch at
    session start, so in-progress work becomes a visible remote artifact (`git branch -r`) the
    moment a contributor begins, not only when they finish.*
- **Conflicts inside a single shared file edited by two tickets at once.** These still surface as
  ordinary git merge conflicts.
  - *Proposed change (not implemented): adopt branch-per-ticket (Option 2) with PR-based merges into
    `main`, so overlapping edits are resolved at review time on a branch instead of colliding
    directly on `main`.*

These are documented limits, not oversights. The milestone review (see header) should check whether
the residual races actually bite in practice before adding heavier machinery.

## Future / next steps

This design is intentionally the minimum that works under today's constraints (push-to-main, pure
convention). The likely evolution, in rough order:

1. **Run it through the RA pilot (Phase 1) and Phase 2** and watch for real collisions. The
   milestone review (see header) is the decision point — triggered by real concurrent work, not a
   fixed date.
2. **If push-to-main collisions become common, switch to a branch workflow — and adopt Option 2
   (branch-per-ticket) as the upgrade.** It is the strongest of the options considered: a pushed
   branch is an isolated, timestamped, self-documenting claim that makes in-progress work visible
   *and* removes shared-file contention on `main` — directly fixing both limits listed above. It
   was set aside here only because the PI chose no branch workflow for now, not on its merits.
3. **Only if convention decay persists even with branches**, add a thin, LLM-agnostic helper (a
   plain shell/python claim script) to enforce the protocol mechanically. Kept last because it adds
   a dependency every assistant must invoke, working against the LLM-agnostic goal.

The throughline: prefer the lightest mechanism that the observed failure rate justifies, and let
evidence from the pilot — not anticipation — trigger each upgrade.
