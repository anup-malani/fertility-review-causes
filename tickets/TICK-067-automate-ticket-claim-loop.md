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
- [ ] `claim NNN` moves the ticket's row from **Open** to **In progress** in `QUEUE.md`, filling the
      Owner, Branch, Claimed (UTC), and Touches columns from the ticket file
- [ ] The board move is committed and pushed on the ticket branch, in the same run as the claim
- [ ] Preflight before any mutation: clean working tree, `main` in sync with `origin`, and a warning
      (not a hard failure) when the ticket's `Touches:` overlaps a live **In progress** row
- [ ] The Mode A rows with `—` in the Branch column are checked too, since no branch exists for them
- [ ] `claim` is idempotent enough to fail safely: if any precondition is unmet it exits before
      creating the branch, leaving the repo as it found it
- [ ] `tickets/README.md` and `tickets/opening-a-chapter-ticket.md` updated so no doc still instructs
      a human to do the step the script now does
- [ ] Verified against a real claim, not only a dry run

## Log
