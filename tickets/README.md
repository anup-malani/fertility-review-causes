# How we track work

This folder is our ticketing system. It works for any contributor — human or AI, Claude or Codex.

---

## The session loop (with claiming)

Three people may be working this repo at once, each driving a different AI. Because everyone
pushes to `main`, we coordinate with a **claim commit**: you announce a ticket by pushing a tiny
status change *before* you start the work, so a rejected push tells you someone got there first.
Every session, do this:

1. **Pull first.** `git pull` so you are looking at the latest state.
2. **Read `QUEUE.md`** — pick the first **Open** ticket assigned to you or `any`. Before you take
   it, check the **In progress** section: make sure no one has claimed it, and that no active
   claim's `Touches:` paths overlap the files you expect to edit. (If they do, pick another ticket
   or coordinate first.)
3. **Claim it.** In the ticket file set `Status: in-progress` and add your name. In `QUEUE.md`,
   move the ticket's row from **Open** to **In progress** with your name and a UTC timestamp.
4. **Commit and push the claim immediately — before doing the work:**
   `git commit -m "claim TICK-NNN" && git push`.
   - If the push is **rejected**, someone pushed first. `git pull`. If they claimed your ticket,
     they win — pick another. Otherwise re-apply your claim and push again.
5. **Do the work.** Commit as you go; those commits also signal the claim is still live.
6. **Close it.** Set `Status: done`, write a one-paragraph note in the ticket's `## Log` section,
   move the row to **Done** in `QUEUE.md`, then commit and push.

That is the whole system. Do not start work that does not have a ticket. If something needs doing
and there is no ticket for it, create one first.

### Stale claims (24h rule)

A claim is **stale** if it has been `in-progress` for more than 24h with no new commits referencing
it. Anyone may reclaim a stale ticket: pull, set it back to `Open` (or re-claim it under your own
name), and note the reclaim in the ticket's `## Log`. This keeps an abandoned session from blocking
a ticket forever.

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

The claim-commit loop above (TICK-008, see `decisions/2026-06-14-collab-system-design.md`) handles
the common case: two people reaching for the same ticket. The early claim push makes the collision
visible — the second push is rejected — instead of both people quietly duplicating work. The
`Touches:` field plus the **In progress** board flag related-work conflicts before they happen.

What it does **not** solve, because we are git-native with no branch workflow:

- **Uncommitted in-session work is invisible.** If someone is editing files locally and has not
  pushed a claim, you cannot see it. Claiming before you work shrinks this gap; it does not close
  it. Always `git pull` before claiming.
- **Two tickets editing the same file at once** still produce a normal merge conflict. Resolve it
  in git. (Branch-per-ticket would fix this and is the recommended upgrade if it starts to hurt —
  see the decision doc.)

If you hit a coordination gap these rules don't cover, email Anup.
