# TICK-061: Document where ticket creation happens under Mode B
**Status:** open
**Assigned:** Shravan
**Parallel-safe:** yes
**Blocks:** none
**Blocked by:** none
**Touches:** `tickets/README.md`, `tickets/QUEUE.md`

## Description

Mode B says not to commit ticket work directly to `main`, but it never says where ticket *creation*
goes. The gap surfaced immediately after the 2026-08-02 switch, when TICK-060 had to be created and
there was no rule to follow.

The answer that makes the system work is that creation goes on `main` and creation alone. Reserving a
number is only useful if everyone can see the reservation, and a number sitting on an unmerged branch
is invisible until that branch lands. That invisibility is precisely what caused the TICK-032 double
assignment, which forced the B.1 chain renumbering from 032–037 to 041–046. Claiming and working the
ticket still go on a branch, unchanged.

`scripts/ticket.sh` also imposes four constraints on new ticket files that `tickets/README.md` does
not currently mention. Each one fails at claim or close time rather than at creation time, which is
the worst place to discover them:

1. The filename becomes the branch name, lowercased with `TICK-` dropped, so the slug must be short
   and hyphenated with no spaces.
2. Exactly one `tickets/TICK-NNN-*.md` must exist, or `claim` aborts with a count error.
3. The status line must read exactly `**Status:** open`, because `claim` rewrites it with a `sed`
   anchored on `^\*\*Status:\*\*`. A different format means the flip silently does nothing.
4. A `## Log` heading must be present from creation, because `close` refuses to run without one.

Also worth recording in the same edit: the **Next free number** banner in `QUEUE.md` is the
authoritative source for the next number, not a scan for the highest existing file. The README
currently tells contributors to look for the highest existing `TICK-NNN`, which is the method that
produced the TICK-032 collision.

## Acceptance criteria
- [ ] `tickets/README.md` "Creating a ticket" states that creation is committed to `main`, with the
      visibility reason given.
- [ ] The same section states that claiming and working the ticket still happen on a branch.
- [ ] The four `ticket.sh` constraints documented where a ticket author will read them.
- [ ] The section points at the `QUEUE.md` next-free-number banner instead of telling contributors to
      scan for the highest existing number.

## Log
<!-- On close, write date + who, then fill in the two notes below (see tickets/README.md, "Closing a ticket"). -->
