# TICK-061: One ticket and one branch per hypothesis
**Status:** in-progress
**Assigned:** Shravan
**Parallel-safe:** yes
**Blocks:** none
**Blocked by:** none
**Touches:** `tickets/README.md`, `decisions/2026-08-02-one-ticket-per-hypothesis.md`, `tickets/QUEUE.md`

## Description

Hypotheses are currently worked as ticket chains, and the chains are where the numbering damage comes
from. B.1 ran as TICK-041 through 046 and had to be renumbered from 032–037 after a double
assignment. D.3.b runs as TICK-047 through 053, seven tickets carrying 40 commits. Chains reserve
numbers for stages nobody has scoped yet, so when the shape of the work changes, the numbers churn.

The single-ticket alternative has already been run and it worked. TICK-055 took C.2.c from search
scope to a drafted chapter with risk of bias and demographic significance complete, in 25 commits
between 10:17 and 15:08 on 2026-07-31. One ticket, one owner, one continuous log. Adopt that shape
deliberately rather than by accident.

The operating assumptions that make it work, both confirmed by the PI-facing RA: **one person takes
a full hypothesis**, and **most hypotheses finish in one or two days**. Those two facts retire the
objections a hypothesis-scale ticket would otherwise face. A branch that lives two days does not
drift from `main`, and a pull request covering two days of work is reviewable, so the Mode B review
gate survives without splitting the merge across stage boundaries.

Two exceptions have to be written in rather than discovered later:

1. **Retrieval is the one stage that can stall for weeks and needs different hands.** B.1 has sat at
   20 of 95 PDFs since 2026-07-25 waiting for someone with Zotero and the UChicago proxy, which is
   what turned a two-day hypothesis into a two-week one. When retrieval blocks on library access,
   spawn one sub-ticket for it and let the hypothesis ticket continue on the retrievable set. TICK-056
   did exactly this for C.2.c and recovered 15 of 15, unblocking extraction.
2. **The 24h stale rule misfires on a two-day ticket with a gap day.** Hypothesis tickets need 72h;
   everything else stays at 24h.

A hypothesis ticket also needs no `## Description`. The hypothesis is fully specified in
`HYPOTHESES-v5.md` under its slug, which carries the claim, the mechanism, the phenomena, the seminal
citations, the cross-references, and the known objections. Restating any of that in the ticket
creates a second copy that drifts from the master list. The ticket names the slug and stops.

In-flight chains are not converted. D.3.b (047–053) and B.1 (041–046) finish under the old shape,
because converting them mid-flight would mean the renumbering this ticket exists to eliminate.

## Acceptance criteria
- [ ] `tickets/README.md` documents one ticket and one branch per hypothesis, with the ordered
      PROTOCOL §5 stages as the acceptance-criteria template.
- [ ] A hypothesis-ticket template added, with no `## Description` and a `**Hypothesis:**` slug
      reference in its place.
- [ ] The template preserves the two `ticket.sh` load-bearing elements: the verbatim
      `**Status:** open` line and the `## Log` heading.
- [ ] The retrieval sub-ticket exception documented, citing the B.1 stall and the TICK-056 precedent.
- [ ] The stale rule amended to 72h for hypothesis tickets, 24h for everything else, in both places
      `tickets/README.md` states it.
- [ ] A `decisions/` entry recording the change, its evidence, and what it costs.
- [ ] The decision entry records that in-flight chains are not converted.

## Log
<!-- On close, write date + who, then fill in the two notes below (see tickets/README.md, "Closing a ticket"). -->
