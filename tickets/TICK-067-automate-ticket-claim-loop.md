# TICK-067: Automate the QUEUE.md board move in `scripts/ticket.sh claim`
**Status:** in-progress
**Assigned:** Shravan
**Parallel-safe:** yes
**Blocks:** none
**Blocked by:** none
**Touches:** `scripts/ticket.sh`, `tickets/README.md`, `tickets/opening-a-chapter-ticket.md`

## Description
`scripts/ticket.sh claim NNN` automates the git half of a claim — sync `main`, refuse if the branch
already exists on `origin`, flip `**Status:**`, commit, push — and then tells the contributor to move
the ticket's row on the `QUEUE.md` board by hand. That hand step is being skipped. TICK-062 through
TICK-066 all have live `origin/06*-*` branches, but as of 2026-08-13 all five still sit under
**Open** in `QUEUE.md` with no **In progress** row.

The board is not decoration. Under Mode B it is the only place `Touches:` overlap is visible, and it
is the only record of the pre-Mode-B claims whose **Branch** column reads `—` — the ones the README
warns `claim` cannot see. A board that lags five tickets behind cannot do either job, so the
collision check that Mode B is supposed to provide is currently not running for Alexandra or Anup.

The move is pure mechanics: the row text, the branch name, and `Touches:` are all already derivable
from the ticket file the script has just parsed, and the timestamp is `date -u`. Nothing about it
needs judgment, which is why it should not be left to a human at the end of a checklist.

Scope is the claim step only. Ticket *creation* (writing the file, bumping the **Next free number**
banner, adding the **Open** row) stays manual under this ticket.

## Acceptance criteria
- [x] `claim NNN` moves the ticket's row from **Open** to **In progress** in `QUEUE.md`, filling the
      Owner, Branch, Claimed (UTC), and Touches columns from the ticket file
- [x] The board move is committed and pushed on the ticket branch, in the same run as the claim
- [x] Preflight before any mutation: clean working tree, `main` in sync with `origin`, and a warning
      (not a hard failure) when the ticket's `Touches:` overlaps a live **In progress** row
- [x] The Mode A rows with `—` in the Branch column are checked too, since no branch exists for them
- [x] `claim` is idempotent enough to fail safely: if any precondition is unmet it exits before
      creating the branch, leaving the repo as it found it
- [x] `tickets/README.md` and `tickets/opening-a-chapter-ticket.md` updated so no doc still instructs
      a human to do the step the script now does
- [x] Verified against a real claim, not only a dry run

## Log

**2026-08-13 — Shravan.** Built and verified.

`scripts/ticket.sh claim` now does the board move itself. It reads the title from the ticket's `#`
heading rather than from the existing board row, because a row wrapped across two physical lines —
TICK-063's is — cannot be re-read reliably; the old row is removed by swallowing physical lines until
the five pipes of a complete four-column row have been seen. Cells are escaped before they are
written: an unquoted `Touches:` list carrying two `*` globs renders as italics on GitHub rather than
as paths, which is why the list is backticked.

Three preflight checks run before anything is mutated — clean tree and synced `main`, no `NNN-*` on
`origin`, and the ticket fields the row is built from. A fourth, `Touches:` overlap against live
**In progress** rows, warns without refusing. Overlap is compared on a path key of directory plus the
first three hyphen-groups of the basename: exact-path matching was the first implementation and it
was useless, silently reporting "no overlap" for TICK-048 against the in-progress TICK-047 and
TICK-049 when all three touch `extraction/climate-anxiety-eco-doomerism-*`. Because the check reads
the board rather than `git branch -r`, it also sees the Mode A rows whose Branch column is `—`, and
taking one of those over now rewrites its Branch and Claimed cells in place instead of adding a
second row for the same ticket.

Verified by running the real script against a scratch clone carrying the real `tickets/` tree: the
wrapped-row case, the Mode A takeover, refusal on a dirty tree, refusal on an already-claimed ticket,
and the overlap warning firing on all three genuine collisions. Not a dry run — real branches, real
commits, real pushes — but to a throwaway remote rather than `origin`.

**Result.** The one step of the claim loop that was pure bookkeeping is now automated, and the docs no
longer ask a human to do it. What prompted the ticket is that the step was being skipped: TICK-062
through TICK-066 all had live `origin/06*` branches while their rows still sat under **Open**, so the
board — the only place `Touches:` conflicts are visible to Alexandra and Anup under Mode B — was five
tickets stale.

**Workflow impact / future behavior.**
- Changes future behavior? yes.
- Implemented in: `scripts/ticket.sh` (the `claim` path), `tickets/README.md` ("Using the helper",
  Mode B step 3), `tickets/opening-a-chapter-ticket.md` (steps 7–8, now 7), `tickets/QUEUE.md` (the
  In-progress note about Mode A rows).
- Do differently: **stop editing `QUEUE.md` by hand when claiming.** `scripts/ticket.sh claim NNN` is
  now the whole claim — branch, status, and board row in one commit and one push. Read the overlap
  warning when it fires rather than skipping past it; it is advisory because only a human can tell a
  real conflict from a shared directory.

**Known follow-up, not done here.** The five stale board rows (TICK-062 to TICK-066) are not
backfilled by this ticket. `claim` refuses a ticket whose branch already exists, so it cannot fix
them, and their current states differ — D.1.a is blocked on a PI call, A.10 is parked. They need a
person who knows the state of each to move the rows by hand.

**Scope note.** Ticket *creation* — writing the file, bumping the **Next free number** banner, adding
the **Open** row — was deliberately left manual, per the scope set when this ticket was opened.
