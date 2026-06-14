# How we track work

This folder is our ticketing system. It works for any contributor — human or AI, Claude or Codex.

---

## The session loop (with claiming)

Three people may be working this repo at once, each driving a different AI. To avoid two people
grabbing the same ticket, we **claim** a ticket — announce it before doing the work — using git
itself as the signal. There are **two co-equal ways to do this**, and the team runs **one at a
time**. Both share the same `QUEUE.md` board, `Touches:` field, and 24h stale rule; they differ
only in how you claim.

**Current mode: B (branch-per-ticket).** This line is the single source of truth for the active mode
— nothing else restates it. Switching modes is a team decision: edit this line, add a dated entry to
**Mode history** below, and append a one-liner to `decisions/2026-06-14-collab-system-design.md`.
Do not mix modes — everyone uses the same one.

**The easy way: use the helper.** `scripts/ticket.sh` runs the whole Mode B loop in three commands —
`claim`, `submit`, `close` (see **Using the helper** below). It is the recommended path and keeps the
branch workflow to almost no manual git. The step-by-step loop is written out underneath only as the
fallback for any tool that cannot run the helper.

**Mode history**
- 2026-06-14 — Mode A (push-to-main) adopted at setup.
- 2026-06-14 — Switched to **Mode B** (branch-per-ticket): a pushed branch surfaces in-progress work
  immediately, keeps `main` clean, and adds a PR review gate before parallel tracks begin. Helper
  `scripts/ticket.sh` added so the heavier loop stays low-effort.

### Using the helper (recommended) — `scripts/ticket.sh`

The helper runs the active Mode B loop for you. Three commands per ticket:

```
scripts/ticket.sh claim  NNN   # sync main, create + push NNN-slug, mark the ticket in-progress
scripts/ticket.sh submit NNN   # push your branch and open the PR into main (uses gh if available)
scripts/ticket.sh close  NNN   # mark the ticket done, then merge + delete the branch
```

`claim` derives the slug from the ticket filename, refuses if a `NNN-*` branch already exists on
`origin` (someone else has it), and flips the ticket's `Status:` line for you. You still: move the
ticket's row on the `QUEUE.md` board, do the work, and — before `close` — write the `## Log`
(**Result** + **Workflow impact**, see "Closing a ticket"). Everything git-shaped is automated; only
the judgment parts are left to you. If you cannot run the helper, follow the manual loop below.

### Mode B — branch-per-ticket (PR merge) — ACTIVE

Each ticket gets its own branch; the **pushed branch is the claim** — visible to everyone via
`git branch -r` the moment you push, and merged via a PR that gives a review checkpoint.

1. **Sync `main`.** `git checkout main && git pull`.
2. **Pick + check.** Take the first **Open** ticket for you or `any`. Run `git branch -r`: if
   `NNN-*` already exists on `origin`, it is taken. Also check `Touches:` overlap with other
   live branches.
3. **Claim it.** `git checkout -b NNN-slug`, set the ticket `Status: in-progress` + your name,
   add its **In progress** row in `QUEUE.md`, then push the branch immediately:
   `git push -u origin NNN-slug`. First to push the branch wins; a name clash is rejected.
   *(`scripts/ticket.sh claim NNN` does steps 1–3.)*
4. **Do the work on the branch.** Commit as you go — your pushed branch shows everyone it is live.
5. **Open a PR into `main`.** Any same-file conflict with another ticket is resolved at PR review on
   the branch, never directly on `main`. *(`scripts/ticket.sh submit NNN`.)*
6. **Close it.** Merge the PR, set `Status: done`, write the `## Log` note, move the row to **Done**
   in `QUEUE.md`, then delete the branch. *(`scripts/ticket.sh close NNN` does the merge + delete.)*

### Mode A — push-to-main (claim-commit) — fallback, not currently active

Everyone pushes to `main`; the claim is a tiny status change pushed *before* you start, so a
rejected push tells you someone got there first.

1. **Pull first.** `git pull` so you are on the latest state.
2. **Pick + check.** From `QUEUE.md`, take the first **Open** ticket assigned to you or `any`. In
   the **In progress** section, confirm no one has claimed it and no active claim's `Touches:`
   overlaps the files you expect to edit. (If it does, pick another or coordinate first.)
3. **Claim it.** Set the ticket `Status: in-progress` + your name; move its row from **Open** to
   **In progress** in `QUEUE.md` with your name and a UTC timestamp.
4. **Commit and push the claim immediately — before doing the work:**
   `git commit -m "claim TICK-NNN" && git push`.
   - If the push is **rejected**, someone pushed first. `git pull`. If they claimed your ticket,
     they win — pick another. Otherwise re-apply your claim and push again.
5. **Do the work.** Commit as you go; those commits also signal the claim is still live.
6. **Close it.** Set `Status: done`, write a one-paragraph `## Log` note, move the row to **Done**
   in `QUEUE.md`, then commit and push.

That is the whole system. Do not start work that does not have a ticket. If something needs doing
and there is no ticket for it, create one first.

### Closing a ticket — the result must change behavior (both modes)

A ticket is **not** done when the solution is written; it is done when the result is stated *and*,
where applicable, it has actually changed how we work. Every closed ticket's `## Log` must contain
two notes:

1. **Result** (always) — one or two sentences: what you decided or produced.

2. **Workflow impact / future behavior** (when applicable) — present whenever the ticket changes how
   anyone works going forward. It must answer three things:
   - **Changes future behavior?** yes / no.
   - **Implemented in** — the repo file(s) that *enact* the change (e.g. `AGENTS.md`,
     `RA-PLAYBOOK.md`, `tickets/README.md`, a workflow script). A decision that no operating file
     points to is **not done** — it is inert until a file contributors actually read tells them to
     behave differently.
   - **Do differently** — what future humans or AI assistants should now do (or stop doing).

   Omit this note only if the ticket genuinely changes nothing about future workflow (e.g. a one-off
   data fix). If you omit it, say so in one line so the omission is deliberate, not forgotten.

(Rationale and full statement: `decisions/2026-06-14-collab-system-design.md` §3.5.)

### Stale claims (24h rule) — both modes

A claim is **stale** if it has shown no new commits for more than 24h. Anyone may reclaim it: pull,
release it back to **Open** (Mode A) or take over / delete the `NNN-*` branch (Mode B), and
note the reclaim in the ticket's `## Log`. This keeps an abandoned session from blocking a ticket
forever.

---

## What a ticket looks like

```markdown
# TICK-NNN: Short title
**Status:** open | in-progress | done | blocked
**Assigned:** Anup | Alexandra | Shravan | any
**Parallel-safe:** yes | no
**Blocks:** TICK-NNN
**Blocked by:** TICK-NNN
**Touches:** paths/this/ticket/will/edit — best-effort, for conflict checking

## Description
What needs to be done and why, in plain English.

## Acceptance criteria
- [ ] Specific, checkable outcome

## Log
<!-- On close, write date + who, then fill in the two notes below (see "Closing a ticket" above). -->

**Result.** <One or two sentences: what you decided or produced.>

**Workflow impact / future behavior.** <When the ticket changes how we work:>
- Changes future behavior? <yes / no>
- Implemented in: <repo file(s) that enact the change, e.g. `AGENTS.md`, `tickets/README.md`>
- Do differently: <what future humans or AI assistants should now do.>
<!-- Omit the impact note only if nothing about future workflow changes; if so, say so in one line. -->
```

---

## Parallel-safe means you can start it now

- `yes` — safe to pick up alongside other open tickets
- `no` — depends on another ticket finishing first; see `Blocked by`

Check `QUEUE.md` before picking a ticket to make sure you are not about to duplicate someone else's in-progress work.

---

## Creating a ticket

Copy the template above. Assign the next unused number (look at the highest existing TICK-NNN). Add it to `QUEUE.md` in the right place — open tickets at the top, blocked tickets below. Note any dependencies.

---

## Escalating to Anup

Email amalani@uchicago.edu with `[FERT-REVIEW]` in the subject. iMessage for anything urgent.
Mirror the escalation in `escalation-log.md` in the repo root.

Escalate when: a citation cannot be verified, the protocol is ambiguous, a hypothesis does
not fit cleanly into one category, or any deviation from the pre-registered plan is needed.

---

## What this system does and does not solve

Both modes (TICK-008, see `decisions/2026-06-14-collab-system-design.md`) handle the common case:
two people reaching for the same ticket. The claim — a pushed status change (Mode A) or a pushed
branch (Mode B) — makes the collision visible instead of both people quietly duplicating work. The
`Touches:` field plus the **In progress** board flag related-work conflicts before they happen.

Where the modes differ:

- **Uncommitted in-session work.** Under **Mode A** it is invisible until you push a claim; under
  **Mode B** pushing your branch at session start makes the work visible to everyone immediately.
  Either way, always pull/sync *before* claiming — that is what keeps the gap small.
- **Two tickets editing the same file at once.** Under **Mode A** this surfaces as a normal merge
  conflict on `main`, resolved in git. Under **Mode B** it is resolved at PR review on the branch,
  never directly on `main`.

If concurrency makes these collisions frequent under Mode A, that is the signal to switch to Mode B
(a team decision — see the decision doc). If you hit a coordination gap neither mode covers,
email Anup.
