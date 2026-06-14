# TICK-001: PI review of HYPOTHESES.md
**Status:** open
**Assigned:** Anup
**Parallel-safe:** yes
**Blocks:** TICK-006, TICK-009
**Blocked by:** —

## Description

`HYPOTHESES.md` was populated by `enumerate-hypotheses.mjs` with 65 hypotheses (Demographic 11,
Economic 21, Biological 12, Cultural 21) and annotated with `**why:**` plain-English glosses.
It is a draft. Anup needs to review it before it becomes the authoritative input to
`literature-search.mjs`.

Specific sub-tasks:

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

3. **Organize at a higher level.** Current four-category split (Demographic / Economic /
   Biological / Cultural) may be supplemented or replaced by a cross-cutting organizing
   principle. Options discussed: proximate-determinants vs. preference-shifters vs.
   constraint-relaxers; supply-vs-demand; PM-only vs. FDT vs. SDT. PI to decide.

4. **Resolve the boundary-setting note.** Line 9–13 of `HYPOTHESES.md` contains a Claude-
   generated note asking whether Demographic hypotheses are really mechanisms rather than root
   causes, and whether the file should organize by root cause (economics/biology/culture) and
   treat demography as the mechanism layer. PI to decide and remove the note.

5. **Commit and mark DRAFT → approved** in the file header.

## Acceptance criteria
- [ ] All 10 surprising-absence candidates reviewed (add, defer, or explicitly exclude)
- [ ] Boundary-setting note (lines 9–13) resolved and removed
- [ ] Higher-level organizing principle documented (even if "keep current four-category split")
- [ ] Header changed from `Status: DRAFT` to `Status: APPROVED — [date]`
- [ ] Committed

## Log
<!-- Append completion note here when done. -->
