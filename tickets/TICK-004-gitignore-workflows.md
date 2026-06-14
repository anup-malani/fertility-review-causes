# TICK-004: Revisit .gitignore for .claude/workflows/
**Status:** open
**Assigned:** any
**Parallel-safe:** yes
**Blocks:** —
**Blocked by:** —

## Description

`.claude/` is currently gitignored, which means implemented workflow scripts (including
`enumerate-hypotheses.mjs`) are not tracked in version control. This undermines
reproducibility: if the repo is cloned fresh, the workflows are gone.

Reproducibility argues for tracking at least `.claude/workflows/`. The rest of `.claude/`
(session transcripts, settings, etc.) can remain gitignored.

Consider: update `.gitignore` to un-ignore `.claude/workflows/` only and add the implemented
workflow scripts to the repo. Alternatively, move the workflow scripts to a tracked directory
(e.g., `scripts/workflows/`) and symlink or reference from `.claude/`.

Note: Claude Code–specific files (`.claude/settings.json`, `.claude/projects/`) should stay
gitignored. Only the `.mjs` workflow scripts need to be tracked.

## Acceptance criteria
- [ ] Decision made and documented (track in `.claude/workflows/` or move to `scripts/workflows/`)
- [ ] Implemented workflow scripts (`enumerate-hypotheses.mjs`, `scaffold.mjs`) are tracked
- [ ] `.gitignore` updated accordingly
- [ ] Committed

## Log
<!-- Append completion note here when done. -->
