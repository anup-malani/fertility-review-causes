# TICK-032: Split compulsory education into value-of-children and teenage-birth hypotheses
**Status:** done
**Assigned:** Alexandra
**Parallel-safe:** no
**Blocks:** --
**Blocked by:** --
**Touches:** HYPOTHESES.md, output/chapters/child-labor-laws-and-schooling.md, tickets/TICK-031-replicate-gacs-child-labor-schooling.md, tickets/QUEUE.md, handoff.md, session-log.md

## Description
Split the combined child-labor-laws/compulsory-schooling hypothesis into two causally distinct
hypotheses: (1) compulsory education reduces completed fertility by preventing children from
working and lowering their economic value to parents; and (2) compulsory education directly
reduces teenage births by keeping adolescents in school. Preserve the distinction between
fertility quantum and tempo, and route the existing search and draft evidence accordingly.

## Acceptance criteria
- [x] `HYPOTHESES.md` contains two separately named and slugged hypotheses with distinct mechanisms and outcomes.
- [x] The existing chapter is reframed as a shared evidence-base draft rather than one combined hypothesis verdict.
- [x] TICK-031 and the handoff explain how existing quantum and tempo records route to the two hypotheses.
- [x] No evidence is represented as measuring the child-economic-value channel unless it identifies that mechanism.
- [x] The session log records the split and the next analytical steps for each hypothesis.

## Log
- 2026-07-24: Superseded in part by TICK-038. The child-economic-value hypothesis remains
  standalone; the teenage-birth material is now nested under `tempo-effects-birth-postponement`.
- 2026-07-24, Alexandra/Codex: Split the master-list entry into
  `compulsory-education-child-economic-value` (quantum) and
  `compulsory-education-teenage-births` (tempo). Reframed the existing chapter as a shared
  evidence-base draft, routed the focused retrieval records, and updated TICK-031, the handoff,
  and session log. Existing combined-slug search artifacts are retained for provenance.
