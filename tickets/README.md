# Ticket System

LLM-agnostic work-tracking for the fertility-review-causes project.
Works with Claude, Codex, or any AI assistant. Also readable by humans.

## Workflow

1. **Start a session:** read `QUEUE.md` to find the next open ticket assigned to you or `any`.
2. **Pick a ticket:** open `TICK-NNN-slug.md`, change `Status` to `in-progress`, add your name.
3. **Do the work.**
4. **Close a ticket:** change `Status` to `done`, append a completion note in the `## Log` section, update `QUEUE.md` (move ticket to Done section or strike it).
5. **Create a ticket:** copy the template below, assign the next unused TICK-NNN, add to `QUEUE.md` in the right position (parallel or sequential).

## Ticket template

```markdown
# TICK-NNN: Title
**Status:** open
**Assigned:** unassigned | Anup | Alexandra | Shravan | any
**Parallel-safe:** yes | no
**Blocks:** (TICK-NNN if applicable)
**Blocked by:** (TICK-NNN if applicable)

## Description
What needs to be done and why.

## Acceptance criteria
- [ ] ...

## Log
<!-- Append completion note here when done. Include date and who closed it. -->
```

## Status values

- `open` — not started
- `in-progress` — actively being worked; note who picked it up
- `done` — completed; completion note in Log section
- `blocked` — cannot start; blocked-by ticket not yet done

## Parallel-safe

- `yes` — can be worked concurrently with other open tickets
- `no` — depends on another ticket's output; check `Blocked by`

## Escalation

If you hit an ambiguity or blocker that isn't covered by PROTOCOL.md or RA-PLAYBOOK.md,
do not guess. Create a ticket with status `blocked`, note what you're waiting for, and
email Anup with `[FERT-REVIEW]` in the subject.
