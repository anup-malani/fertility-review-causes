# TICK-013: Document Claude / Codex interop
**Status:** done
**Assigned:** Alexandra/Codex
**Parallel-safe:** yes
**Blocks:** —
**Blocked by:** —
**Touches:** AGENTS.md, docs/agent-interop.md

## Description

Document the practical mapping between Claude Code workflow invocations and Codex execution
for this repo. The goal is not to translate private agent transcripts, but to make clear that
tracked artifacts are the shared interface and that Codex should write the same outputs as
Claude workflow stages.

## Acceptance criteria
- [x] `docs/agent-interop.md` created
- [x] `AGENTS.md` links to the interop doc
- [x] The doc explains that durable handoff happens through tracked repo artifacts, not agent memory

## Log

2026-06-27, Alexandra/Codex: Added `docs/agent-interop.md` with Claude invocation patterns,
Codex equivalents, handoff rules, and the current `TICK-004` limitation. Linked it from
`AGENTS.md`.
