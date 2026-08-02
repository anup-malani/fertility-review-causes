# voice-stack — for Codex

**This package is the Codex build.** If you use Claude Code instead, ask for the Claude Code build
(`voice-stack-for-Claude-Code.zip`) — this one won't set you up for Claude Code.

This package makes Codex draft in a specific person's voice, screen its own drafts for the tics that
make text read as machine-written, and rewrite until they're gone. It ships loaded with Anup
Malani's voice as a worked example; `BUILD-YOUR-VOICE.md` shows how to swap in your own.

## Get started

Follow `INSTALL-CODEX.md`. Codex has no skill system, so "install" is two moves: drop this
`voice-stack/` folder into the repo where you draft, and copy `AGENTS.md` to that repo's root.
Codex reads the nearest `AGENTS.md` up the directory tree the way Claude Code reads `CLAUDE.md`, so
once it's in place the Layer 0 screen binds on every turn and `AGENTS.md` walks Codex through the
write → check → rewrite loop as a written procedure. Same four layers, same result — driven by
prompts instead of slash commands. `INSTALL-CODEX.md` has ready-to-paste prompts.

## The four layers

The system separates two things that are usually confused: removing the machine signature (the same
for everyone) and adding a person's fingerprint (different for every writer and every genre).

- **Layer 0 — the negative screen** (`core/refs/ai-tells.md`). Machine tells plus a plain-English
  dinner-table test. Removes machine-ness. Universal; on for everything, including chat.
- **Layer 1 — universal craft** (`core/refs/appellate-style.md`). Structure and sentence-craft
  universals — topic sentences, brutal clarity, sentence rhythm. The same for every voice.
- **Layer 2 — the per-voice model** (`core/style.md` Modes + `voice/exemplars/*.md` banks). The
  personal fingerprint, one profile per register. This is the swap point if you want your own voice.
- **Layer 3 — output formatting** (`core/style.md`, the .docx / .pptx specs). Applied at export.

A small **router** (`core/refs/voice-registry.md`) selects the Layer 2 voice by artifact type.

## Make it your own

`BUILD-YOUR-VOICE.md`. The short version: replace the paragraphs in `voice/exemplars/*.md` with your
own writing, one bank per register, and leave Layer 0 and Layer 1 untouched. Edit the name/pronouns
in `AGENTS.md`, then re-copy it to your repo root.

## What's in the box

```
voice-stack/
├── README.md                 (this file)
├── INSTALL-CODEX.md          the install
├── AGENTS.md                 Codex always-on instructions (place at your repo root)
├── BUILD-YOUR-VOICE.md       how to swap in a different voice
├── core/                     GENERIC — rules, craft, router, Modes, skills
│   ├── refs/                 ai-tells, appellate-style, voice-registry, architecture
│   ├── style.md              Layer 2 Modes + Layer 3 formatting
│   └── skills/                write-as, voice-check, voice-critic, not-ai
│                             (read as procedures; Codex can't invoke them as commands)
└── voice/                    SWAP POINT — the personal layer
    └── exemplars/            the six voice banks (Anup's, as the worked example)
```

## What this build deliberately leaves out

This is a review/RA subset of Anup's full private voice-stack, trimmed for external sharing:

- **`corpus.md`** (in `core/skills/voice-critic/`) ships as a blank template, not Anup's real
  edit-pair corpus — that file is private. Build your own per `BUILD-YOUR-VOICE.md` if you want the
  red-pen pass to learn your taste specifically.
- **`grill-me`**, **`file-voice-ticket`**, and **`process-voice-tickets`** — maintainer-only tools
  that write into Anup's personal rule-curation pipeline. Not needed to draft or screen a document;
  left out on purpose.
- Git history, sync scripts, and other maintainer/update-workflow files — not relevant to using the
  stack.

Everything you need to draft in-voice and self-screen a draft — all six exemplar banks, the full
tell screen, the router, and `AGENTS.md` — is here.

## A note on the skill files under `core/skills/`

Those `SKILL.md` files were written for Claude Code, where they run as slash commands. Under Codex
you read them as procedures — the loop in `AGENTS.md` already spells out how. Two Claude-only
mechanisms to ignore if you open a `SKILL.md` directly: (1) `voice-critic`'s "spawn a subagent"
step — run that pass inline instead; (2) the `/pptx` pointer in `core/style.md` for PowerPoint
formatting is not part of this package. Neither affects the writing-voice loop. `INSTALL-CODEX.md`
has the full path-mapping table.
