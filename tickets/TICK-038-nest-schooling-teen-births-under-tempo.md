# TICK-038: Nest compulsory-schooling teenage births under tempo postponement
**Status:** in-progress
**Assigned:** Alexandra
**Parallel-safe:** no
**Blocks:** --
**Blocked by:** --
**Touches:** HYPOTHESES.md, output/chapters/child-labor-laws-and-schooling.md, extraction/compulsory-education-*, source/build/goldset/76_*, handoff.md, session-log.md, tickets/TICK-031-*, tickets/TICK-032-*, tickets/QUEUE.md

## Description

Remove compulsory education and teenage births as a standalone master hypothesis. Treat it as a
policy-driver evidence stream under `tempo-effects-birth-postponement`, while retaining
`compulsory-education-child-economic-value` as a separate quantum hypothesis. Preserve the existing
tempo retrieval and extraction artifacts with names and documentation that reflect their nested
status.

## Acceptance criteria

- [ ] The master list contains no standalone `compulsory-education-teenage-births` hypothesis.
- [ ] `tempo-effects-birth-postponement` explicitly includes compulsory schooling as a driver-specific evidence stream.
- [ ] Routing, extraction, chapter, handoff, and ticket documentation use nested-stream terminology.
- [ ] Generated tempo artifacts remain reproducible and do not lose study-level provenance.

## Log
<!-- Add completion note when closing. -->
