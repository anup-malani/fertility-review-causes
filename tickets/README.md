# How we track work

This folder is our ticketing system. It works for any contributor — human or AI, Claude or Codex.

---

## The three-file loop

Every session, do this:

1. **Read `QUEUE.md`** — find the first open ticket assigned to you or `any`.
2. **Open that ticket** (`TICK-NNN-slug.md`), change `Status` to `in-progress`, add your name.
3. **Do the work.**
4. **Close the ticket** — change `Status` to `done`, write a one-paragraph note in the `## Log` section, strike the ticket in `QUEUE.md`.

That is the whole system. Do not start work that does not have a ticket. If something needs doing and there is no ticket for it, create one first.

---

## What a ticket looks like

```markdown
# TICK-NNN: Short title
**Status:** open | in-progress | done | blocked
**Assigned:** Anup | Alexandra | Shravan | any
**Parallel-safe:** yes | no
**Blocks:** TICK-NNN
**Blocked by:** TICK-NNN

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

## What this system does not yet solve

The current system tracks parallel tasks well. It does not yet handle real-time coordination —
knowing what another contributor's AI is doing mid-session, or detecting conflicts when two
people are working on related hypotheses at the same time. That is an open design problem
assigned to Shravan (TICK-008). If you run into a coordination gap before that is solved,
email Anup.
