TICK-008 is closed and its *Mode A* half is what the repo runs today — the **In progress** board in `tickets/QUEUE.md` is full of live Mode A claims. The piece that was designed, written up, and never turned on is **Solution B, branch-per-ticket**. Sources: `decisions/2026-06-14-collab-system-design.md` and `tickets/README.md:37-53`.

## The problem it solves

Three people (Anup, Alexandra on Codex, you on Claude) share one repo and one `main`. The named failure mode is two contributors reaching for the same ticket at the same time, plus two tickets editing the same file at once. The design's honest premise up front: git cannot give you a real lock, because shared state doesn't exist until someone pushes and someone else pulls. So the goal is not to eliminate the race but to make the window small, make collisions loud, and make recovery cheap.

Both solutions share the same scaffolding — the `Touches:` field on each ticket (best-effort list of paths it will edit), the **In progress** table in `QUEUE.md` with owner and UTC claim time, and the 24h stale-claim rule. They differ **only** in the claim mechanism, which is exactly why the decision doc calls them co-equal rather than a one-way upgrade: switching costs nothing but agreement.

## Mode A (what we run now): the claim is a pushed status change

Pull → check the **In progress** board for your ticket and for `Touches:` overlap → flip the ticket to `Status: in-progress`, move its row from **Open** to **In progress** with your name and timestamp → `git commit -m "claim TICK-NNN" && git push` **before doing any real work** → then work, committing as you go → close by flipping to `done`, writing the `## Log` note, and moving the row to **Done**.

The whole mechanism is step 4. `git push` rejection *is* the collision detector: if your push bounces, someone got there first. Pull; if they took your ticket they win and you pick another, otherwise reapply the claim and push again.

## Mode B (unimplemented): the claim is a pushed branch

1. `git checkout main && git pull`.
2. Check `git branch -r` — if `tick-NNN-*` already exists on `origin`, that ticket is taken. Also eyeball `Touches:` overlap against other live branches.
3. `git checkout -b tick-NNN-slug`, set `Status: in-progress`, add the **In progress** row, then **immediately** `git push -u origin tick-NNN-slug`. The pushed branch *is* the claim. First push wins; a duplicate name is rejected by the remote.
4. Do the work on the branch, committing as you go.
5. Open a PR into `main`. Same-file conflicts with another ticket surface as PR merge conflicts and get resolved on the branch — never directly on `main`. The PR doubles as a review checkpoint.
6. Merge, set `Status: done`, write the `## Log` note, move the row to **Done**, delete the branch.

The 24h stale rule applies identically: a `tick-NNN-*` branch with no commits in 24h is reclaimable — take it over or delete it, and note the reclaim in the ticket's `## Log`.

## What B buys and what it costs

Two things A genuinely does not solve. First, **awareness of in-session work**: under A your work is invisible to everyone until you push a claim, and truly invisible while uncommitted; under B, pushing the branch at session start makes the work visible via `git branch -r` from minute one. Second, **two tickets touching one file**: under A that lands as a merge conflict on `main`; under B it lands at PR review on a branch. Plus you get a review gate you don't currently have.

The cost is a branch and a PR per ticket. The doc's rule for switching is to do it **on evidence** — when shared-`main` collisions or same-file conflicts actually become frequent — not in anticipation, with the milestone review (close of the RA pilot, and again once Phase 2 parallel tracks run) as the natural decision point.

## One thing worth flagging

The evidence for switching may already be in the repo. The TICK-032 double-assignment on 2026-07-25 — which forced renumbering the whole B.1 chain 032–037 → 041–046 — happened because two workstreams sat unmerged on a shared `main`, and the QUEUE.md banner's own lesson ("claim a number by pushing its QUEUE.md row *before* starting work, not after") is a restatement of Mode A's step 4 that didn't hold under real load. There's also already an `origin/008-collab-system-design` branch and a `worktree-b1-extraction-workstream` branch, so the team is partly working branch-style without the protocol around it. That's an argument to put the Mode B switch on the agenda at the next sync — but it's a team decision recorded in the decision doc, not something to flip unilaterally.
