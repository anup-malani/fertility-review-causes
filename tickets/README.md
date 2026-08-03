# How we track work

This folder is our ticketing system. It works for any contributor — human or AI, Claude or Codex.

---

## The session loop (with claiming)

Three people may be working this repo at once, each driving a different AI. To avoid two people
grabbing the same ticket, we **claim** a ticket — announce it before doing the work — using git
itself as the signal. There are **two co-equal ways to do this**, and the team runs **one at a
time**. Both share the same `QUEUE.md` board, `Touches:` field, and stale rule (24h, or 72h for
hypothesis tickets); they differ
only in how you claim.

**Current mode: B (branch-per-ticket).** This line is the single source of truth for the active mode
— nothing else restates it. Switching modes is a team decision: edit this line, add a dated entry to
**Mode history** below, and append a one-liner to `decisions/2026-06-14-collab-system-design.md`.
Do not mix modes — everyone uses the same one.

**The easy way: use the helper.** `scripts/ticket.sh` runs the whole Mode B loop in three commands —
`claim`, `submit`, `close` (see **Using the helper** below). It is the recommended path and keeps the
branch workflow to almost no manual git. The step-by-step loop is written out underneath only as the
fallback for any tool that cannot run the helper.

**Mode history**
- 2026-06-14 — Mode A (push-to-main) adopted at setup.
- 2026-06-14 — Switched to **Mode B** (branch-per-ticket): a pushed branch surfaces in-progress work
  immediately, keeps `main` clean, and adds a PR review gate before parallel tracks begin. Helper
  `scripts/ticket.sh` added so the heavier loop stays low-effort.

### Using the helper (recommended) — `scripts/ticket.sh`

The helper runs the active Mode B loop for you. Three commands per ticket:

```
scripts/ticket.sh claim  NNN   # sync main, create + push NNN-slug, mark the ticket in-progress
scripts/ticket.sh submit NNN   # push your branch and open the PR into main (uses gh if available)
scripts/ticket.sh close  NNN   # mark the ticket done, then merge + delete the branch
```

`claim` derives the slug from the ticket filename, refuses if a `NNN-*` branch already exists on
`origin` (someone else has it), and flips the ticket's `Status:` line for you. You still: move the
ticket's row on the `QUEUE.md` board, do the work, and — before `close` — write the `## Log`
(**Result** + **Workflow impact**, see "Closing a ticket"). Everything git-shaped is automated; only
the judgment parts are left to you. If you cannot run the helper, follow the manual loop below.

### Mode B — branch-per-ticket (PR merge) — ACTIVE

Each ticket gets its own branch; the **pushed branch is the claim** — visible to everyone via
`git branch -r` the moment you push, and merged via a PR that gives a review checkpoint.

1. **Sync `main`.** `git checkout main && git pull`.
2. **Pick + check.** Take the first **Open** ticket for you or `any`. Run `git branch -r`: if
   `NNN-*` already exists on `origin`, it is taken. Also check `Touches:` overlap with other
   live branches.
3. **Claim it.** `git checkout -b NNN-slug`, set the ticket `Status: in-progress` + your name,
   add its **In progress** row in `QUEUE.md`, then push the branch immediately:
   `git push -u origin NNN-slug`. First to push the branch wins; a name clash is rejected.
   *(`scripts/ticket.sh claim NNN` does steps 1–3.)*
4. **Do the work on the branch.** Commit as you go — your pushed branch shows everyone it is live.
5. **Open a PR into `main`.** Any same-file conflict with another ticket is resolved at PR review on
   the branch, never directly on `main`. *(`scripts/ticket.sh submit NNN`.)*
6. **Close it.** Merge the PR, set `Status: done`, write the `## Log` note, move the row to **Done**
   in `QUEUE.md`, then delete the branch. *(`scripts/ticket.sh close NNN` does the merge + delete.)*

### Mode A — push-to-main (claim-commit) — fallback, not currently active

Everyone pushes to `main`; the claim is a tiny status change pushed *before* you start, so a
rejected push tells you someone got there first.

1. **Pull first.** `git pull` so you are on the latest state.
2. **Pick + check.** From `QUEUE.md`, take the first **Open** ticket assigned to you or `any`. In
   the **In progress** section, confirm no one has claimed it and no active claim's `Touches:`
   overlaps the files you expect to edit. (If it does, pick another or coordinate first.)
3. **Claim it.** Set the ticket `Status: in-progress` + your name; move its row from **Open** to
   **In progress** in `QUEUE.md` with your name and a UTC timestamp.
4. **Commit and push the claim immediately — before doing the work:**
   `git commit -m "claim TICK-NNN" && git push`.
   - If the push is **rejected**, someone pushed first. `git pull`. If they claimed your ticket,
     they win — pick another. Otherwise re-apply your claim and push again.
5. **Do the work.** Commit as you go; those commits also signal the claim is still live.
6. **Close it.** Set `Status: done`, write a one-paragraph `## Log` note, move the row to **Done**
   in `QUEUE.md`, then commit and push.

That is the whole system. Do not start work that does not have a ticket. If something needs doing
and there is no ticket for it, create one first.

### Closing a ticket — the result must change behavior (both modes)

A ticket is **not** done when the solution is written; it is done when the result is stated *and*,
where applicable, it has actually changed how we work. Every closed ticket's `## Log` must contain
two notes:

1. **Result** (always) — one or two sentences: what you decided or produced.

2. **Workflow impact / future behavior** (when applicable) — present whenever the ticket changes how
   anyone works going forward. It must answer three things:
   - **Changes future behavior?** yes / no.
   - **Implemented in** — the repo file(s) that *enact* the change (e.g. `AGENTS.md`,
     `RA-PLAYBOOK.md`, `tickets/README.md`, a workflow script). A decision that no operating file
     points to is **not done** — it is inert until a file contributors actually read tells them to
     behave differently.
   - **Do differently** — what future humans or AI assistants should now do (or stop doing).

   Omit this note only if the ticket genuinely changes nothing about future workflow (e.g. a one-off
   data fix). If you omit it, say so in one line so the omission is deliberate, not forgotten.

(Rationale and full statement: `decisions/2026-06-14-collab-system-design.md` §3.5.)

### Stale claims (24h rule, 72h for hypothesis tickets) — both modes

A claim is **stale** if it has shown no new commits for more than 24h. Anyone may reclaim it: pull,
release it back to **Open** (Mode A) or take over / delete the `NNN-*` branch (Mode B), and
note the reclaim in the ticket's `## Log`. This keeps an abandoned session from blocking a ticket
forever.

**Hypothesis tickets get 72h instead of 24h.** A hypothesis usually runs one or two days, so a single
gap day in the middle is normal working rhythm rather than abandonment, and 24h would flag it as
stale while the owner is still on it.

---

## Hypothesis tickets: one ticket, one branch, one hypothesis

**A hypothesis is one ticket and one branch, start to finish.** The ticket opens when you take the
hypothesis and closes when its chapter is drafted and reviewed. Do not split a hypothesis into a chain
of stage tickets. The stages live in the acceptance criteria, and the branch is `NNN-<hypothesis-slug>`
exactly as for any other ticket.

This replaces the chain pattern used for B.1 (TICK-041 to 046) and D.3.b (TICK-047 to 053). Chains
reserve numbers for stages nobody has scoped yet, so when the shape of the work changes the numbers
churn, which is what forced the B.1 renumbering. The single-ticket shape has already been run: TICK-055
took C.2.c from search scope to a drafted chapter with risk of bias and demographic significance
complete, inside one working day. **In-flight chains are not converted** — B.1 and D.3.b finish as
they are.

**A hypothesis ticket has no `## Description`.** The hypothesis is fully specified in
`HYPOTHESES-v5.md` under its slug, which carries the claim, the mechanism, the phenomena, the seminal
citations, the cross-references, and the known objections. Restating any of it in the ticket creates a
second copy that drifts. Name the slug in a `**Hypothesis:**` field and stop.

### When a hypothesis needs a second ticket

Only one stage earns its own ticket: **full-text retrieval that blocks on library access.** It is the
one stage that needs different hands (Zotero plus the UChicago proxy) and can stall for weeks. B.1 has
sat at 20 of 95 PDFs since 2026-07-25 for exactly this reason. When it happens, open one retrieval
sub-ticket, hand it to whoever has library access, and let the hypothesis ticket carry on against the
records you do have. TICK-056 is the precedent: it recovered 15 of 15 and unblocked C.2.c extraction.

Every other stage stays inside the hypothesis ticket.

### What a hypothesis ticket looks like

```markdown
# TICK-NNN: <Code and name, e.g. D.1.a Postmaterialism, Individualism, and Secularization>
**Status:** open
**Assigned:** Anup | Alexandra | Shravan
**Hypothesis:** `hypothesis-slug` — HYPOTHESES-v5.md §<code>
**Parallel-safe:** yes | no
**Blocks:** TICK-NNN
**Blocked by:** TICK-NNN
**Touches:** literature/search-logs/<slug>-*, extraction/<slug>-*, output/chapters/<slug>.md

<!-- No ## Description. The slug above is the specification. -->

## Acceptance criteria
<!-- The PROTOCOL §5 pipeline, in order. Delete any stage the hypothesis genuinely does not reach,
     and say in the Log why. -->
- [ ] 2. Search strategy and scope drafted
- [ ] 3. Literature search and AI screening, both phases (§5.1)
- [ ] 4. RA title/abstract review
- [ ] 5. Full-text retrieval  <!-- sub-ticket if it blocks on library access -->
- [ ] 6. Full-text screen, RA spot-checks 5–10%
- [ ] 7. Extraction to `extraction/<slug>.csv`, RA verifies a random 10%
- [ ] 8. Risk-of-bias assessment per study
- [ ] 9. Meta-analysis if ≥3 extractable effects, narrative synthesis otherwise
- [ ] 10. Demographic significance against PM / FDT / SDT
- [ ] 11. GRADE rating, 3 independent raters
- [ ] 12. Chapter draft on the §6 template
- [ ] 13. RA lay-readability check
- [ ] 14. PI review and sign-off

## Log
<!-- A dated entry per stage as you go, then the two closing notes. -->
```

The `**Status:** open` line and the `## Log` heading are load-bearing for `scripts/ticket.sh`; see the
four constraints under "Creating a ticket" above.

---

## What a non-hypothesis ticket looks like

```markdown
# TICK-NNN: Short title
**Status:** open | in-progress | done | blocked
**Assigned:** Anup | Alexandra | Shravan | any
**Parallel-safe:** yes | no
**Blocks:** TICK-NNN
**Blocked by:** TICK-NNN
**Touches:** paths/this/ticket/will/edit — best-effort, for conflict checking

## Description
What needs to be done and why, in plain English.

## Acceptance criteria
- [ ] Specific, checkable outcome

## Log
<!-- On close, write date + who, then fill in the two notes below (see "Closing a ticket" above). -->

**Result.** <One or two sentences: what you decided or produced.>

**Workflow impact / future behavior.** <When the ticket changes how we work:>
- Changes future behavior? <yes / no>
- Implemented in: <repo file(s) that enact the change, e.g. `AGENTS.md`, `tickets/README.md`>
- Do differently: <what future humans or AI assistants should now do.>
<!-- Omit the impact note only if nothing about future workflow changes; if so, say so in one line. -->
```

---

## Parallel-safe means you can start it now

- `yes` — safe to pick up alongside other open tickets
- `no` — depends on another ticket finishing first; see `Blocked by`

Check `QUEUE.md` before picking a ticket to make sure you are not about to duplicate someone else's in-progress work.

---

## Creating a ticket

Creating a ticket is not claiming one. Copy the template above, take the next number, add the row to
`QUEUE.md` in the right place (open tickets at the top, blocked tickets below), note any dependencies,
and push. A branch appears later, when someone claims it.

**Take the number from the "Next free number" banner at the top of `QUEUE.md`, and bump the banner in
the same commit.** Do not scan for the highest existing `TICK-NNN`. Scanning is what produced the
TICK-032 double assignment on 2026-07-25, because the two colliding workstreams each scanned a `main`
that did not yet show the other's number.

**Commit ticket creation to `main`, even under Mode B.** Mode B's rule against committing to `main`
governs ticket *work*, not ticket *creation*. Reserving a number is only useful if everyone can see
the reservation, and a number sitting on an unmerged branch stays invisible until that branch lands.
Claiming and working the ticket still happen on a branch, unchanged.

### Four things `scripts/ticket.sh` requires of a new ticket file

Each of these fails later, at claim or close time, rather than when you create the file:

1. **The filename becomes the branch name**, lowercased with the `TICK-` prefix dropped, so
   `TICK-060-document-ticket-creation-rule.md` yields branch `060-document-ticket-creation-rule`. Keep
   the slug short and hyphenated, with no spaces.
2. **Exactly one `tickets/TICK-NNN-*.md` may exist.** Two files sharing a number and `claim` aborts
   with a count error.
3. **The status line must read exactly `**Status:** open`.** `claim` rewrites it with a `sed` anchored
   on `^\*\*Status:\*\*`, so any other format means the flip silently does nothing and the ticket looks
   unclaimed while a branch exists for it.
4. **Include the `## Log` heading from the start**, even empty. `close` refuses to run on a ticket
   that has none.

---

## Escalating to Anup

Email amalani@uchicago.edu with `[FERT-REVIEW]` in the subject. iMessage for anything urgent.
Mirror the escalation in `escalation-log.md` in the repo root.

Escalate when: a citation cannot be verified, the protocol is ambiguous, a hypothesis does
not fit cleanly into one category, or any deviation from the pre-registered plan is needed.

---

## What this system does and does not solve

Both modes (TICK-008, see `decisions/2026-06-14-collab-system-design.md`) handle the common case:
two people reaching for the same ticket. The claim — a pushed status change (Mode A) or a pushed
branch (Mode B) — makes the collision visible instead of both people quietly duplicating work. The
`Touches:` field plus the **In progress** board flag related-work conflicts before they happen.

Where the modes differ:

- **Uncommitted in-session work.** Under **Mode A** it is invisible until you push a claim; under
  **Mode B** pushing your branch at session start makes the work visible to everyone immediately.
  Either way, always pull/sync *before* claiming — that is what keeps the gap small.
- **Two tickets editing the same file at once.** Under **Mode A** this surfaces as a normal merge
  conflict on `main`, resolved in git. Under **Mode B** it is resolved at PR review on the branch,
  never directly on `main`.

If concurrency makes these collisions frequent under Mode A, that is the signal to switch to Mode B
(a team decision — see the decision doc). If you hit a coordination gap neither mode covers,
email Anup.
