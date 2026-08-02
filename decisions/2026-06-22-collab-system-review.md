# Review: how the ticket-branch collaboration system works

**Date:** 2026-06-22
**Author:** Shravan Hari
**Status:** Companion review to `decisions/2026-06-14-collab-system-design.md` (the system of record). This document does not change the system; it explains it, compares it to standard software practice, and specifies the cross-team communication protocol that rides on top of it.
**Scope:** TICK-008. Read alongside `tickets/README.md` (the canonical loop) and `decisions/2026-06-14-collab-system-design.md` (rationale + the two co-equal modes).

---

## Part 1 — How we organize work and navigate it collectively

### The shape of the system

Three people (Anup as PI; Alexandra on Codex; Shravan on Claude) share one private repo and may
work different hypotheses or pipeline stages at once. The system that coordinates them is
deliberately small and lives entirely in version-controlled markdown plus one shell helper:

- **`tickets/TICK-NNN-*.md`** — one file per unit of work. Each carries `Status`, `Assigned`,
  `Parallel-safe`, `Blocks` / `Blocked by` (dependencies), and `Touches` (the files it will edit).
- **`tickets/QUEUE.md`** — the board: **Open** / **In progress** / **Blocked** / **Done**. The
  single live view of who holds what.
- **`tickets/README.md`** — the loop everyone runs, and the **single source of truth for the active
  mode** (`Current mode:` line). Nothing else restates the mode.
- **`scripts/ticket.sh`** — a thin wrapper (`claim` / `submit` / `close`) over plain `git`/`gh` so
  the active branch-per-ticket loop costs almost no manual git.

### Which TICK-008 problems this solves, and how

TICK-008 named two problems. The system addresses them as follows:

**Problem #1 — parallel tracks (who is doing what; dependencies; no duplicated effort).**
Solved by the ticket fields and the board. `Blocked by` / `Blocks` make serial dependencies
explicit (the hard case — a ticket waiting on *two* others — is expressible and used, e.g. TICK-006
blocked by TICK-001 **and** TICK-005). `Parallel-safe` flags what can run concurrently. `QUEUE.md`'s
Open/Blocked split tells you what is safe to start *now*. The one residual weakness is **drift**:
dependency state is duplicated between `QUEUE.md` and the ticket files and can disagree. That is a
discipline issue, not a design flaw — mitigated by keeping the timestamp/owner in exactly one place
(the board) and reviewing at the weekly sync.

**Problem #2 — coordination (knowing what others are doing mid-session; catching collisions).**
The honest limit first: a git-native system **cannot** give real-time locking — shared state does
not exist until someone pushes and someone else pulls. So the goal is not to eliminate the race but
to **make the window small, collisions visible, and recovery cheap.** We do this with a
**claim-before-work** rule: you announce a ticket *before* doing it, using git itself as the signal.
We run **Mode B (branch-per-ticket)**: the claim is a **pushed branch** named `NNN-slug`. A name
clash on push is rejected by the remote (same-ticket collision caught), the branch is visible via
`git branch -r` the moment you push (in-progress work surfaces at session start, not at the end),
same-file conflicts between two tickets resolve at **PR review on the branch and never on `main`**,
and every ticket gets a review gate before it lands. The `Touches` field plus the In-progress board
flag related-work conflicts *before* they happen. Mode A (push-to-main, claim = a tiny pushed status
change, collision = rejected push) remains fully specified as the documented fallback for low load.
Both share the same scaffolding, so switching modes is a team decision, not a redesign.

### The ticket lifecycle, start to finish

The full loop, with **manual human steps in bold**. "Manual" means a human (RA or PI) must do it;
everything else is a one-command helper call or AI-executed work.

| # | Step | Who / how |
|---|------|-----------|
| 0 | **Sync + pick a ticket** — pull `main`, take the first Open ticket for you or `any` from `QUEUE.md`; confirm no `NNN-*` branch exists and no live `Touches` overlap | **RA/PI (judgment)** |
| 1 | Claim — create + push `NNN-slug`, flip ticket to `in-progress` | `scripts/ticket.sh claim NNN` (automated) |
| 2 | **Add the In-progress row** to `QUEUE.md` (owner, branch, UTC, Touches) | **RA/PI (manual edit)** |
| 3 | Do the work on the branch, committing as you go | AI-executed; **RA/PI directs & spot-checks** |
| 4 | Submit — push branch, open PR into `main` | `scripts/ticket.sh submit NNN` (automated) |
| 5 | **Review the PR** | **The other RA or PI (manual review gate)** |
| 6 | **Write the `## Log`** — *Result* + *Workflow impact / future behavior* | **RA/PI (manual; the closure rule)** |
| 7 | Close — merge PR, mark `done`, delete branch | `scripts/ticket.sh close NNN` (automated) |
| 8 | **Move the row to Done** in `QUEUE.md` | **RA/PI (manual edit)** |

Two human responsibilities are load-bearing and cannot be automated away:

- **The closure rule (step 6).** A ticket is done only when its result is *stated* and, where
  applicable, has *changed how we work* — naming the repo file(s) that enact the change and what
  others should now do differently. A decision no operating file points to is inert. (Full statement:
  `decisions/2026-06-14-collab-system-design.md` §3.5.)
- **Protocol gates.** Independently of TICK-008, `PROTOCOL.md §5` marks human-in-the-loop gates
  (PI approves hypotheses; RA spot-checks 5–10% of screens, verifies 10% of extractions, runs the
  lay-readability check; PI signs off chapters; GRADE disagreements > 1 level escalate to PI). The
  ticket system schedules *who picks up what*; these gates govern *what must be human-checked inside
  a ticket*. The two compose: a chapter ticket is not closeable until its protocol gates are cleared.

---

## Part 2 — Comparison to standard software-engineering practice

The system is intentionally a **lightweight subset of normal GitHub flow**, adapted so it stays
LLM-agnostic and so a research team — not a full-time eng team — can run it with near-zero overhead.

| Dimension | Standard SWE practice | Ours | Why we differ |
|---|---|---|---|
| Issue tracking | GitHub Issues / Jira / Linear (hosted UI) | Markdown ticket files + `QUEUE.md` in the repo | A hosted UI is not equally usable by every AI assistant; git-native files are. |
| Branching | Feature branch → PR → review → merge (e.g. GitHub Flow) | **Identical** — `NNN-slug` branch → PR → review → merge | We adopt this directly; it is the part SWE got right for parallel work. |
| Claiming work | Assignee field / project board column | **The pushed branch is the claim**; board mirrors it | One mechanism (push) does both claim and collision detection — fewer moving parts. |
| Review gate | Required PR review, often + CI | PR review by the other RA / PI | Same gate; CI is light here (mainly `make bib` reproducibility, not test suites). |
| Automation | CI/CD, bots, templates | `scripts/ticket.sh` + `make` targets | Same instinct (script the repetitive parts), scaled to a 3-person team. |

**Where we deliberately stay lighter:** no required CI on every push, no protected-branch
enforcement, no external project-management tool, no real-time locking. These are convention, not
machinery — appropriate for three contributors, and revisited on evidence at the weekly sync.

### Integrating the Gentzkow–Shapiro production process

The point of borrowing SWE branching is not the branching itself — it is that it lets us enforce the
*Code and Data for the Social Sciences* discipline on a multi-author research pipeline. The ticket-
branch system is the carrier for four G–S commitments:

- **Clean / replicable.** `main` is always a clean, reviewed state because every change lands through
  a PR — never a half-finished direct push. Anyone can `clone` + `make` from any commit on `main` and
  reproduce outputs. The branch model is what keeps `main` reproducible while work is in flight.
- **Automated.** "No manual steps between raw input and output" (CLAUDE.md / AGENTS.md) is enforced
  in code review: the bibliography is **generated** (`datastore/studies.json` → `make bib`, never
  hand-edited `.bib`), and the PR diff makes a hand-edit visible and rejectable. `scripts/ticket.sh`
  applies the same "script it, don't do it by hand" rule to the coordination loop itself.
- **Tractable.** Modular structure (separation of `build/` / `analysis/` / `lib/`; one chapter per
  hypothesis as the atomic deliverable) means tickets are small and independent, so parallel tracks
  rarely touch the same files — and when they do, `Touches` + the PR surface it early. Work is
  decomposed the way G–S decompose code: small, named, reusable units.
- **Documented / no oral tradition.** Every durable choice is a `decisions/*.md` file; every loop is
  in `tickets/README.md`; the closure rule forces each ticket to record what changed and where. A new
  RA can run the system from the files alone — which is exactly the G–S standard ("documented so a new
  RA can run them without oral tradition"). The PR + `## Log` together form the audit trail that makes
  the *research* process, not just the code, replicable.

In short: SWE branching gives us the *mechanism*; Gentzkow–Shapiro gives us the *standard the
mechanism is there to enforce*. The review gate is where the two meet — it is simultaneously a code
review (SWE) and a reproducibility/citation check (G–S).

---

## Part 3 — Cross-team communication protocol

Communication rides on the ticket-branch system so that **state lives in the repo** and chat is
reserved for things git cannot carry (judgment, escalation, scheduling). The ordering principle:
**say it in the repo if the repo can hold it; use a human channel only for what it cannot.**

### 3.1 Channels and what each is for

| Channel | Carries | Does **not** carry |
|---|---|---|
| **Ticket file (`## Description`, `## Log`)** | Scope, decisions, the Result + Workflow-impact record | Time-sensitive pings |
| **`QUEUE.md` board** | Who holds what, right now (owner, branch, UTC, Touches) | Discussion |
| **Branch + PR** | In-progress work (visible on push), review comments, merge conflicts | Anything before a branch is pushed |
| **`decisions/*.md`** | Durable, repo-wide choices and rationale | Per-ticket detail |
| **Weekly sync (Mon, 30 min)** | Status, plan, the standing coordination check | A substitute for writing it down afterward |
| **Email / iMessage `[FERT-REVIEW]`** | Escalations, urgent unblocking | Decisions (those get mirrored to the repo) |
| **`escalation-log.md`** | The durable mirror of every escalation + resolution | — |

### 3.2 Standing rules

1. **Sync before you touch anything.** `git checkout main && git pull` is step zero of every
   session, for humans and AIs alike (AGENTS.md "Orient yourself"; RA-PLAYBOOK Role A step zero).
   This is what keeps the awareness gap small.
2. **The branch *is* the announcement.** Push your `NNN-slug` branch at the start of work, not the
   end — that is what makes in-progress work visible to the others without a message.
3. **Check `Touches` before you start.** If your ticket overlaps a live branch's `Touches`,
   coordinate (a PR comment or a sync line) before editing — don't race to the merge.
4. **Conflicts are resolved on the branch, never on `main`.** A same-file collision is a PR merge
   conflict, handled at review by the two ticket owners; `main` never sees it.
5. **Every closed ticket leaves a written trace.** The `## Log` Result + Workflow-impact note *is*
   the async status update — no separate report needed.
6. **Escalate by the rules, mirror to the repo.** The escalation triggers (RA-PLAYBOOK + PROTOCOL
   §5/§11: unverifiable citation, extraction disagreement > 20%, GRADE panel split > 1 level,
   pre-registration deviation, etc.) go to Anup by email/iMessage **and** into `escalation-log.md`,
   so a chat decision never lives only in chat.

### 3.3 Routine cadence

- **Per session:** sync → claim (branch = announcement) → work → PR (review = conversation) →
  `## Log` (the written status) → close.
- **Mid-week (Wed/Thu, async):** quick "anything blocked?" by email/iMessage; blockers become or
  update tickets.
- **Weekly (Mon sync):** status of in-progress hypotheses, escalations, the week's plan, **and the
  standing coordination check** — any claim collisions, stale (>24h) branches, or PR-review backlog?
  Is the active mode still right for the load we actually saw? (RA-PLAYBOOK Weekly cadence;
  decision doc §3.4.) This is the recurring prompt that keeps the convention from decaying.
- **Friday:** end-of-week summary appended to `session-log.md`.

### 3.4 Where this protocol stops

It coordinates *who does what* and *how we talk about it*; it does **not** override the
human-in-the-loop research gates in `PROTOCOL.md §5`. A PR being mergeable (no git conflict, review
approved) is necessary but not sufficient to close a chapter ticket — the protocol gates (spot-checks,
lay-readability, PI sign-off, GRADE escalation) still bind. When in doubt about *content*, escalate to
Anup; when in doubt about *coordination*, the answer is in `tickets/README.md`.
