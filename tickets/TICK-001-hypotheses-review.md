# TICK-001: Review and recategorize HYPOTHESES.md
**Status:** in-progress
**Assigned:** Anup (decisions) + Claude (mechanical re-slotting)
**Parallel-safe:** yes
**Blocks:** TICK-006, TICK-009, TICK-012
**Blocked by:** —

## Description

`HYPOTHESES.md` was populated by `enumerate-hypotheses.mjs` with 65 hypotheses and annotated
with `**why:**` glosses. It is a draft. This ticket covers the full review-and-restructure job
in two sequential sub-steps:

### Sub-step A — Anup's decision pass (in progress)

1. **Cull.** Remove duplicates or hypotheses too weak to merit a full chapter.

2. **Add.** The enumeration workflow flagged 10 surprising absences:
   - War/conscription (demographic disruption, male mortality)
   - Famine shocks
   - Climate shocks
   - State capacity and institutional change
   - Epidemic shocks (distinct from chronic STI burden)
   - Air pollution / industrial toxins (distinct from endocrine disruptors)
   - Religious-pronatalist subgroups (counter-trend fertility)
   - LGBTQ family formation (SDT-specific)
   - Migration selection effects
   - Polygyny / marriage-market structure

3. **Decide the organizing structure.** The current four-category split (Demographic /
   Economic / Biological / Cultural) conflates root causes with proximate mechanisms.
   Proposed two-tier structure:
   - **Root causes** — *why* people want fewer children: Economic, Biological, Cultural/evolutionary
   - **Proximate mechanisms** — *how* fertility responds: Demographic mechanisms (child
     mortality, contraception, marriage patterns, birth spacing, etc.)
   Resolve the boundary-setting note at lines 9–13 and remove it.

4. **Commit the culled/added/restructured list** (even if re-slotting is not yet done).

### Sub-step B — Claude re-slots (after Sub-step A is committed)

Once Anup has decided the structure, Claude reads the updated hypothesis list and re-slots
all entries into the approved two-tier structure, flagging genuinely ambiguous cases.
Anup reviews the re-slotting and approves or adjusts. Claude commits the final version
and updates the header to `Status: APPROVED — [date]`.

## Acceptance criteria
- [ ] All 10 surprising-absence candidates reviewed (add, defer, or explicitly exclude)
- [ ] Boundary-setting note (lines 9–13) resolved and removed
- [ ] Organizing structure decided and documented
- [ ] Sub-step A committed
- [ ] All 65 hypotheses re-slotted into approved structure (Sub-step B)
- [ ] Header changed from `Status: DRAFT` to `Status: APPROVED — [date]`
- [ ] Final version committed

## Log
<!-- Append completion note here when done. -->
