# TICK-011: Recategorize HYPOTHESES.md by root cause vs proximate mechanism
**Status:** blocked
**Assigned:** Claude drafts → Anup reviews
**Parallel-safe:** no
**Blocks:** TICK-006, TICK-009
**Blocked by:** TICK-001

## Description

The current four-category split (Demographic / Economic / Biological / Cultural) conflates
root causes with proximate mechanisms. The Demographic category in particular captures *how*
fertility changes (marriage age, birth spacing, contraception, child mortality) more than *why*
people want fewer children. Economic, Biological, and Cultural hypotheses are closer to root
causes.

**Proposed reorganization:**

- **Root causes** — *why* people want fewer or more children:
  - Economic (income, cost of children, Q-Q tradeoff, women's opportunity cost, etc.)
  - Biological (fecundity, pathogen stress, endocrine disruption, etc.)
  - Cultural / evolutionary (ideational change, social learning, religion, status competition, etc.)

- **Proximate mechanisms** — *how* fertility responds once preferences change:
  - Demographic mechanisms (child mortality → replacement/insurance, marriage patterns,
    contraception access, birth spacing, migration, etc.)

**Task:**

1. Claude reads the current 65 hypotheses in `HYPOTHESES.md`
2. Claude proposes a revised two-tier structure: root causes (Economic / Biological / Cultural)
   with proximate mechanisms either as a separate section or as a sub-layer within each root cause
3. Claude re-slots each of the 65 hypotheses into the proposed structure, flagging any that
   are genuinely ambiguous
4. Anup reviews the proposed re-slotting and approves, modifies, or rejects the structure
5. Implement the approved structure in `HYPOTHESES.md`

**Note:** this ticket is for the *structure* decision. Adding/culling individual hypotheses
is covered by TICK-001 (which should be complete first so the list is stable before we
reorganize it).

## Acceptance criteria
- [ ] Proposed two-tier structure written up (in this ticket's Log or a temp file)
- [ ] All 65 hypotheses re-slotted with ambiguous cases flagged
- [ ] Anup has reviewed and approved the structure
- [ ] `HYPOTHESES.md` updated with the approved structure
- [ ] Header updated to reflect the new organization
- [ ] Committed

## Log
<!-- Claude: append proposed structure here when ready to draft. Anup: add review decision. -->
