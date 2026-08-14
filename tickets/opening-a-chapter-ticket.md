# Opening a ticket for a new chapter

*Step-by-step companion to `README.md`, written 2026-08-02. The ticket numbers below (TICK-062) and
the D.1.a example are illustrative — substitute the current number from the **Next free number**
banner in `QUEUE.md` and the hypothesis you are actually opening.*

At the time of writing, TICK-061 is closed, its branch deleted, `main` clean and in sync, and the next
free number is TICK-062.

## Opening a ticket for a new chapter

Working example: D.1.a, slug `postmaterialism-individualism-secularization`.

### 1. Open Terminal and go to the repo

```bash
cd [wherever the repo lives]
```

### 2. Sync

```bash
git checkout main
git pull
git status
```

Want `nothing to commit, working tree clean`.

### 3. Get the next free number

```bash
grep "Next free number" tickets/QUEUE.md
```

Prints TICK-062.

### 4. Create the ticket file

```bash
code tickets/TICK-062-postmaterialism-individualism-secularization.md
```

Paste this in whole and save. Under the new model it's short, because `HYPOTHESES-v5.md` carries the
specification:

```markdown
# TICK-062: D.1.a Postmaterialism, Individualism, and Secularization
**Status:** open
**Assigned:** [Alexandra/Anup/Shravan -- type in your name]
**Hypothesis:** `postmaterialism-individualism-secularization` — HYPOTHESES-v5.md §D.1.a
**Parallel-safe:** yes
**Blocks:** none
**Blocked by:** none
**Touches:** literature/search-logs/postmaterialism-individualism-secularization-*, extraction/postmaterialism-individualism-secularization-*, output/chapters/postmaterialism-individualism-secularization.md

## Acceptance criteria
- [ ] 2. Search strategy and scope drafted
- [ ] 3. Literature search and AI screening, both phases (§5.1)
- [ ] 4. RA title/abstract review
- [ ] 5. Full-text retrieval
- [ ] 6. Full-text screen, RA spot-checks 5–10%
- [ ] 7. Extraction to `extraction/postmaterialism-individualism-secularization.csv`, RA verifies a random 10%
- [ ] 8. Risk-of-bias assessment per study
- [ ] 9. Meta-analysis if ≥3 extractable effects, narrative synthesis otherwise
- [ ] 10. Demographic significance against PM / FDT / SDT
- [ ] 11. GRADE rating, 3 independent raters
- [ ] 12. Chapter draft on the §6 template
- [ ] 13. RA lay-readability check
- [ ] 14. PI review and sign-off

## Log
```

Two lines are load-bearing and must be exact: `**Status:** open` (that's what `claim` rewrites) and
the `## Log` heading (that's what `close` requires). No `## Description` — that's the new rule, and
the `**Hypothesis:**` field replaces it.

### 5. Add the Open row and bump the banner

```bash
code tickets/QUEUE.md
```

**(a)** Change `Next free number is TICK-062` to `TICK-063`.

**(b)** Add this as the first row under **Open — can start now**, directly below the `|---|` divider:

```
| [TICK-062](TICK-062-postmaterialism-individualism-secularization.md) | D.1.a Postmaterialism, Individualism, and Secularization | Shravan | yes |
```

Save.

### 6. Push the creation to `main`

```bash
git add tickets/
git commit -m "Open TICK-062: D.1.a postmaterialism, individualism, secularization"
git push
```

Creation goes on `main` deliberately — pushing is what makes the number reservation visible to
Alexandra and Anup.

### 7. Claim it

```bash
scripts/ticket.sh claim 62
```

That is the whole claim. It checks that your tree is clean and `main` is in sync, that no `062-*`
branch exists on `origin`, and that nothing already **In progress** overlaps your `Touches:`; then it
creates `062-postmaterialism-individualism-secularization`, flips the status to `in-progress`, moves
the ticket's row from **Open** to **In progress** on the board with the branch name and a UTC
timestamp, commits, and pushes.

You should see:

```
  ✓ main synced, tree clean
  ✓ no 062-* branch on origin
  ✓ Touches overlap: none
  ✓ branch 062-postmaterialism-individualism-secularization created
  ✓ status → in-progress
  ✓ QUEUE.md: row moved Open → In progress
      branch  062-postmaterialism-individualism-secularization
      claimed 2026-08-13T21:04:11Z
  ✓ pushed — the branch is the claim
```

A `!` on the overlap line instead of `✓` names the ticket you collide with and the path you collide
on. It is a warning, not a refusal — overlap is often legitimate — but read it before carrying on.

If a check fails, nothing has been changed: fix what it names and run the same command again.

**Do not edit `QUEUE.md` by hand here.** Before TICK-067 this was a separate step 8, and it was the
step people skipped: TICK-062 through TICK-066 all had live branches while their rows still sat under
**Open**, which is exactly the collision Mode B exists to prevent.

### 8. Show the claim is live

```bash
git branch -r
```

`origin/062-postmaterialism-individualism-secularization` appears. That branch is the claim, and it
stays open until the chapter is drafted.
