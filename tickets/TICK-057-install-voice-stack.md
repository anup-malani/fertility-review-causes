# TICK-057: Install voice-stack for Codex
**Status:** done
**Assigned:** Alexandra
**Parallel-safe:** yes
**Touches:** `AGENTS.md`; `tickets/QUEUE.md`; `tickets/TICK-041-install-voice-stack.md`

## Description
Install the repository-local voice-stack instructions by appending the supplied Codex instruction
block to the root `AGENTS.md` without replacing the existing project instructions.

## Acceptance criteria
- [x] Root `AGENTS.md` retains the existing project instructions.
- [x] Root `AGENTS.md` contains the voice-stack always-on and artifact-writing instructions.
- [x] The installed paths resolve to the repository's `voice-stack/` directory.

## Log
2026-08-01, Alexandra/Codex: Preserved the project instructions, appended the repository-local
voice-stack always-on and artifact-writing block to root `AGENTS.md`, and verified that every
installed path resolves within the included `voice-stack/` package.
