# How we track work

This folder is our ticketing system. It works for any contributor — human or AI, Claude or Codex.

---

## The session loop (with claiming)

Three people may be working this repo at once, each driving a different AI. To avoid two people
grabbing the same ticket, we **claim** a ticket — announce it before doing the work — using git
itself as the signal. There are **two co-equal ways to do this**, and the team runs **one at a
time**. Both share the same `QUEUE.md` board, `Touches:` field, and 24h stale rule; they differ
only in how you claim.

**Current mode: A (push-to-main).** Switching to Mode B is a team decision (see
`decisions/2026-06-14-collab-system-design.md`). Do not mix modes — everyone uses the same one.

### Mode A — push-to-main (claim-commit)

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

### Mode B — branch-per-ticket (PR merge)

Each ticket gets its own branch; the **pushed branch is the claim** — visible to everyone via
`git branch -r` the moment you push, and merged via a PR that gives a review checkpoint.

1. **Sync `main`.** `git checkout main && git pull`.
2. **Pick + check.** Take the first **Open** ticket for you or `any`. Run `git branch -r`: if
   `tick-NNN-*` already exists on `origin`, it is taken. Also check `Touches:` overlap with other
   live branches.
3. **Claim it.** `git checkout -b tick-NNN-slug`, set the ticket `Status: in-progress` + your name,
   add its **In progress** row in `QUEUE.md`, then push the branch immediately:
   `git push -u origin tick-NNN-slug`. First to push the branch wins; a name clash is rejected.
4. **Do the work on the branch.** Commit as you go — your pushed branch shows everyone it is live.
5. **Open a PR into `main`.** Any same-file conflict with another ticket is resolved at PR review on
   the branch, never directly on `main`.
6. **Close it.** Merge the PR, set `Status: done`, write the `## Log` note, move the row to **Done**
   in `QUEUE.md`, then delete the branch.

That is the whole system. Do not start work that does not have a ticket. If something needs doing
and there is no ticket for it, create one first.

### Stale claims (24h rule) — both modes

A claim is **stale** if it has shown no new commits for more than 24h. Anyone may reclaim it: pull,
release it back to **Open** (Mode A) or take over / delete the `tick-NNN-*` branch (Mode B), and
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
<!-- When you close this ticket, write: date, who, what you did. -->
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
