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
cd "/Users/shravanhari/~/Anup RA/projects/fertility-review-causes"
```

Quotes required — your repo sits under a directory literally named `~`.

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
**Assigned:** Shravan
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
git branch -r
scripts/ticket.sh claim 62
```

`git branch -r` confirms no `062-*` exists yet. Then `claim` creates
`062-postmaterialism-individualism-secularization`, flips the status to `in-progress`, commits, and
pushes.

### 8. Finish the claim, on the branch

```bash
date -u +%Y-%m-%dT%H:%M:%SZ
code tickets/QUEUE.md
```

Delete the TICK-062 row from **Open**, add it to **In progress** (six columns, note the extra `Branch`
one), pasting your timestamp:

```
| [TICK-062](TICK-062-postmaterialism-individualism-secularization.md) | D.1.a Postmaterialism, Individualism, and Secularization | Shravan | `062-postmaterialism-individualism-secularization` | PASTE_TIMESTAMP | `literature/search-logs/postmaterialism-individualism-secularization-*`, `extraction/postmaterialism-individualism-secularization-*` |
```

Then:

```bash
git add tickets/
git commit -m "TICK-062: claim on the board"
git push
```

### 9. Show the claim is live

```bash
git branch -r
```

`origin/062-postmaterialism-individualism-secularization` appears. That branch is the claim, and it
stays open until the chapter is drafted.
