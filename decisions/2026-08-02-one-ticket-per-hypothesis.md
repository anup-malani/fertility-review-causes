# One ticket and one branch per hypothesis

**Date:** 2026-08-02
**Decided by:** Shravan (RA), under TICK-061. **Pending PI confirmation at the Monday sync.**
**Supersedes:** the stage-chain pattern used for B.1 and D.3.b. Operates within Mode B
(`decisions/2026-06-14-collab-system-design.md`).

## Decision

A hypothesis is one ticket and one branch, from search scope through PI sign-off. The PROTOCOL §5
pipeline stages become the ticket's acceptance criteria rather than separate tickets. A hypothesis
ticket carries no `## Description`; it names its `HYPOTHESES-v5.md` slug instead.

One exception: full-text retrieval that blocks on library access gets its own sub-ticket.

## Why

**Chains are where the numbering damage came from.** B.1 ran as TICK-041 through 046 and had to be
renumbered from 032–037 after a double assignment, which required a translation table in `QUEUE.md`
because the pushed commits named the old numbers. D.3.b runs as seven tickets carrying 40 commits.
Chains reserve numbers for stages nobody has scoped yet, so when the shape of the work changes, the
numbers churn. Three renumbering events have now been paid for.

**The single-ticket shape was already run, and it worked.** TICK-055 took C.2.c from search scope to a
drafted chapter with risk of bias and demographic significance complete, in 25 commits between 10:17
and 15:08 on 2026-07-31. One ticket, one owner, fifteen dated log entries forming a continuous
narrative of the decisions taken.

**Two operating facts make it safe**, both confirmed by the RA who runs the pipeline: one person takes
a full hypothesis, and most hypotheses finish in one or two days. A branch that lives two days does not
drift from `main`, and a pull request covering two days of work stays reviewable, so the Mode B review
gate survives without splitting the merge across stage boundaries.

**The description was a second copy of the master list.** `HYPOTHESES-v5.md` already specifies each
hypothesis under its slug with the claim, mechanism, phenomena, seminal citations, cross-references,
and known objections. A ticket restating any of that drifts from the entry it copies.

## What it costs

**Parallelism inside a hypothesis is gone.** TICK-048 was marked parallel-safe against half of
TICK-047, and that kind of split is no longer available. This is acceptable only because one person
owns a full hypothesis; if that assumption changes, this decision needs revisiting.

**Dependency scheduling moves from the board into the checklist.** The **Blocked** table currently
tracks four real D.3.b dependencies. Under one ticket the sequencing lives in the ordered acceptance
criteria, which is weaker: nothing mechanically stops a stage being started early.

**Retrieval remains the known stall.** B.1 has sat at 20 of 95 PDFs since 2026-07-25 waiting for
someone with Zotero and the UChicago proxy, which is what turned a two-day hypothesis into a two-week
one. The sub-ticket exception exists to keep that stall from blocking everything downstream of it;
TICK-056 is the precedent, recovering 15 of 15 and unblocking C.2.c extraction.

**The stale rule needed amending.** Hypothesis tickets move to 72h because a two-day ticket with one
gap day would otherwise be flagged stale while its owner is still working it. Everything else stays at
24h.

## Scope

**In-flight chains are not converted.** D.3.b (TICK-047 through 053) and B.1 (TICK-041 through 046)
finish under the old shape. Converting them mid-flight would mean renumbering, which is the cost this
decision exists to eliminate.

## Implemented in

- `tickets/README.md` — "Hypothesis tickets: one ticket, one branch, one hypothesis", the
  hypothesis-ticket template, the retrieval sub-ticket exception, and the amended stale rule in both
  places it is stated.
- `tickets/TICK-061-one-ticket-per-hypothesis.md` — the ticket and its log.
