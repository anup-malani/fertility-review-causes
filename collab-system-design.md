# How we claim work: the two coordination modes

**Mode B, branch-per-ticket, is the implemented and active mode.** It was designed under TICK-008 on
2026-06-14 and took effect on `main` when the `008-collab-system-design` branch merged on 2026-08-02.
Mode A, push-to-main, remains fully documented as the fallback. The active mode is recorded in exactly
one place, the `Current mode:` line at `tickets/README.md:15`; every other file points at that line
rather than restating it, so the mode cannot drift out of sync across documents.

## The problem it solves

Three people (Anup, Alexandra on Codex, Shravan on Claude) share one repository and one `main`. The
named failure mode is two contributors reaching for the same ticket at the same time, plus two tickets
editing the same file at once. The design states its limit honestly at the top: git cannot give you a
real lock, because shared state does not exist until someone pushes and someone else pulls. The goal
is therefore to make the race window small, make collisions loud, and make recovery cheap.

Both modes share the same scaffolding. Each ticket carries a `Touches:` field listing the paths it
expects to edit, the **In progress** table in `QUEUE.md` records owner and UTC claim time, and a claim
goes stale after 24 hours without new commits. The modes differ only in the claim mechanism, which is
why the decision doc calls them co-equal rather than treating B as a one-way upgrade. Switching back
costs nothing but agreement.

## Mode B (active): the claim is a pushed branch

Each ticket gets a branch named `NNN-slug`, taken from the ticket's filename with the `TICK-` prefix
dropped. TICK-008 becomes `008-collab-system-design`. Pushing that branch is the claim: it is visible
to everyone through `git branch -r` from the moment it lands, and the remote rejects a duplicate name,
so the first push wins.

The loop runs in six steps:

1. `git checkout main && git pull`.
2. Check `git branch -r`. If `NNN-*` already exists on `origin`, that ticket is taken. Also compare
   `Touches:` against the other live branches.
3. `git checkout -b NNN-slug`, set the ticket to `Status: in-progress`, add its **In progress** row in
   `QUEUE.md`, then push immediately with `git push -u origin NNN-slug`.
4. Do the work on the branch, committing as you go.
5. Open a pull request into `main`. A same-file conflict with another ticket surfaces at PR review on
   the branch and never lands directly on `main`. The PR doubles as a review checkpoint.
6. Merge, set `Status: done`, write the `## Log` note, move the row to **Done**, and delete the branch.

`scripts/ticket.sh` runs the git-shaped parts of that loop in three commands. `claim NNN` does steps 1
through 3, `submit NNN` does step 5, and `close NNN` does step 6. The helper deliberately leaves the
judgment work to you: moving the row on the `QUEUE.md` board, and writing the `## Log` with its
**Result** and **Workflow impact** notes. `close` refuses to run on a ticket that has no `## Log`
section at all.

The 24-hour stale rule applies unchanged. An `NNN-*` branch with no commits in 24 hours can be
reclaimed by anyone: take it over or delete it, and note the reclaim in the ticket's `## Log`.

## Mode A (documented fallback): the claim is a pushed status change

Under Mode A everyone pushes to `main`, and the claim is a small status change pushed before the work
starts. You pull, check the **In progress** board for your ticket and for `Touches:` overlap, flip the
ticket to `Status: in-progress`, move its row from **Open** to **In progress** with your name and a UTC
timestamp, then run `git commit -m "claim TICK-NNN" && git push` before doing anything else. You work,
committing as you go, and close by flipping the status to `done`, writing the `## Log` note, and moving
the row to **Done**.

The whole mechanism sits in that push. A rejected push is the collision detector: someone got there
first, so you pull, and if they took your ticket they win and you pick another. Otherwise you reapply
the claim and push again.

## What B buys and what it costs

Mode B addresses two gaps that Mode A leaves open. The first is awareness of in-session work: under
Mode A your work stays invisible until you push a claim, and stays completely invisible while
uncommitted, whereas under Mode B the branch you push at session start announces the work from minute
one. The second is two tickets touching one file, which lands as a merge conflict on `main` under Mode
A and as a PR review conflict on a branch under Mode B. Mode B also adds a review gate that Mode A
does not have.

The cost is one branch and one pull request per ticket, which is why `scripts/ticket.sh` exists.

## Why we switched

The evidence for switching accumulated in the repository before the decision was taken. The TICK-032
double-assignment on 2026-07-25 forced a renumbering of the whole B.1 chain from 032–037 to 041–046,
and it happened because two workstreams sat unmerged on a shared `main`. The lesson the `QUEUE.md`
banner drew from that collision ("claim a number by pushing its QUEUE.md row before starting work, not
after") restates Mode A's own claim step, which had not held under real load. The team was also
already running `008-collab-system-design` and `worktree-b1-extraction-workstream` as branches without
the protocol around them. The original rule was to switch on evidence rather than in anticipation, and
that evidence arrived.

## Two things to watch during the changeover

**Claims made before the switch are invisible to the helper.** Seven tickets were claimed under Mode A
and carry `—` in the **Branch** column of the `QUEUE.md` board: TICK-055, 054, 049, 047, 046, 019, and
031. They are valid claims, but `ticket.sh claim` checks only whether an `NNN-*` branch exists on
`origin`; it never reads the board. Running `claim` on one of those numbers would hand a second person
a branch for work someone already owns. Read the **In progress** board before claiming until those
rows have drained, either by closing the tickets or by backfilling branches for them.

**`submit` and `close` need the `gh` CLI.** `claim` works with plain git alone. Without `gh` installed,
the other two commands print manual instructions instead of opening or merging the pull request, so the
PR step happens in the browser. Install it with `brew install gh && gh auth login` to get the full
three-command loop.

## Switching modes later

Changing the active mode is a team decision and a three-touch edit. Change the `Current mode:` line in
`tickets/README.md`, append a dated entry to the **Mode history** list in the same file, and append a
line to the **Switch log** in `decisions/2026-06-14-collab-system-design.md`. Nothing else records the
mode, so nothing else needs changing.

Sources: `decisions/2026-06-14-collab-system-design.md`, `tickets/README.md:15` (mode of record),
`tickets/README.md:47-64` (the Mode B loop), and `scripts/ticket.sh`.
