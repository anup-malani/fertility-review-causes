# TICK-060: Document where ticket creation happens under Mode B
<!-- Numbered TICK-061 while it was worked; renumbered to 060 on 2026-08-02. Commits bd7e3be,
     ae14c64, 9449f01, 1cfaebe and PR #2 all name TICK-061 and refer to this ticket. -->
**Status:** done
**Assigned:** Shravan
**Parallel-safe:** yes
**Blocks:** none
**Blocked by:** none
**Touches:** `tickets/README.md`, `tickets/QUEUE.md`

## Description

Mode B says not to commit ticket work directly to `main`, but it never says where ticket *creation*
goes. The gap surfaced immediately after the 2026-08-02 switch, on the first ticket that had to be
created under Mode B, when there was no rule to follow.

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
- 2026-08-02 (Shravan/Claude): **all four acceptance criteria met** in `tickets/README.md`, "Creating
  a ticket". Two things the drafting settled beyond the ticket:
  **(1) The banner instruction was actively wrong, not merely absent.** The section told contributors
  to "look at the highest existing TICK-NNN," which is the exact method that produced the TICK-032
  collision: both colliding workstreams scanned a `main` that did not yet show the other's number. The
  `QUEUE.md` next-free banner exists because scanning failed, so the README was pointing at the
  discredited method while the banner sat three files away. Replaced, with the bump-in-the-same-commit
  requirement made explicit.
  **(2) Constraint 3 is the dangerous one and deserves its stated failure mode.** A malformed
  `**Status:**` line does not error. `claim` still creates and pushes the branch, so the ticket reads
  `open` on the board while a branch exists for it, which is the one state the whole claim mechanism is
  built to prevent. Documented with that consequence attached rather than as a formatting nit.

**Result.** Documented that ticket creation is committed to `main` while claiming and working stay on
a branch, replaced the highest-number scan with the `QUEUE.md` next-free banner, and wrote down the
four constraints `scripts/ticket.sh` places on a new ticket file.

**Workflow impact / future behavior.**
- Changes future behavior? **Yes.**
- Implemented in: `tickets/README.md` ("Creating a ticket", plus its new subsection on the
  `ticket.sh` constraints).
- Do differently: take the next ticket number from the `QUEUE.md` banner rather than scanning for the
  highest file, and bump the banner in the same commit. Commit the new ticket to `main`; do not open a
  branch for creation alone. Name the file so its slug works as a branch name, keep exactly one file
  per number, write the status line as `**Status:** open` verbatim, and include the `## Log` heading
  from the start.
