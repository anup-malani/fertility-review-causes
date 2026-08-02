# Install the voice stack for Codex

This is the install path for **Codex**. This zip is the Codex build; if you use Claude Code
instead, ask for the Claude Code zip. Codex does not have Claude Code's skill system, so "install"
here means two things: put the voice files where Codex can read them, and drop an `AGENTS.md` at the
root of the repo you work in so the rules bind on every turn. Codex reads the nearest `AGENTS.md` up
the directory tree the same way Claude Code reads `CLAUDE.md`.

If you want *your own* voice rather than Anup's, do `BUILD-YOUR-VOICE.md` first — it is a
ten-minute swap of the exemplar files.

When you unzip this package, the folder is named `voice-stack/` — this guide uses that name
throughout.

## Step 1 — Put the folder in your project

Copy the whole `voice-stack/` folder into the repository where you draft (for the fertility review,
that is the review repo). Commit it, so a fresh clone has it too. A good home is a top-level
`voice-stack/` directory.

Note: the fertility-review repo's `.gitignore` ignores `.claude/` wholesale, which is why project
skills there die on a fresh clone. Putting the stack in a plain `voice-stack/` directory (not under
`.claude/`) sidesteps that — it gets committed normally.

## Step 2 — Place AGENTS.md at the repo root

Copy `voice-stack/AGENTS.md` to the **root** of the repo (one level above `voice-stack/`). If an
`AGENTS.md` already exists there, append the voice-stack content to it rather than overwriting.

```
cp voice-stack/AGENTS.md ./AGENTS.md          # or append if one exists
```

Open the copied `AGENTS.md` and confirm the `voice-stack/...` paths in it match where you put the
folder. If you nested it differently, fix the paths.

## Step 3 — Draft with the loop

With `AGENTS.md` in place, Codex applies the Layer 0 screen automatically. To write an artifact,
give Codex a prompt like:

> Write the [Methods section / this chapter] as a `academic-econ` artifact. Follow the write → check
> → rewrite loop in `AGENTS.md`: route to the voice, read `voice-stack/core/refs/appellate-style.md`
> and the `voice-stack/voice/exemplars/academic-econ.md` CORE paragraphs and the Academic (Economics)
> Mode in `voice-stack/core/style.md`, draft in that voice, then self-check against
> `voice-stack/core/refs/ai-tells.md` and rewrite anything that trips a tell.

Then, to screen a finished draft:

> Screen this draft against `voice-stack/core/refs/ai-tells.md` and the register caps in
> `voice-stack/core/refs/voice-registry.md`. List every tell with a fix, then apply the fixes.

## Step 4 — Optional: the AI-detector pass

`voice-stack/core/skills/not-ai/detect.py` is a standalone Python script that scores how AI-like a
passage reads. Run it, rewrite the flagged spans in the author's voice, and re-run until it passes.
It needs Python 3; see the header of the script for usage.

## Reading the files: the one path rule

The reference and skill files were written for the Claude Code install, where they live under
`~/.claude/`. In this Codex setup they live in the repo under `voice-stack/`. So whenever you (or
Codex) hit a `~/.claude/...` path *inside* one of these files, read it as the matching `voice-stack/`
location:

| A `~/.claude/...` path inside a file | Read it as |
|---|---|
| `~/.claude/refs/<file>.md` | `voice-stack/core/refs/<file>.md` |
| `~/.claude/style.md` | `voice-stack/core/style.md` |
| `~/.claude/refs/exemplars/<voice>.md` | `voice-stack/voice/exemplars/<voice>.md` (note: the folder name changes too) |
| `~/.claude/skills/<name>/...` | `voice-stack/core/skills/<name>/...` |

`AGENTS.md` already uses the `voice-stack/` paths, so if you drive from it you rarely need this table.
It matters when you open a `SKILL.md` or a reference file directly and follow a path it names.

## What Codex gets vs. what it doesn't

- **Gets:** the same four layers, the same exemplars, the same tell screen and register caps, the
  corpus-based red-pen pass, and a written procedure that reproduces the write → check → rewrite
  workflow.
- **Doesn't get:** the one-word skill invocations (`/write-as`, `/voice-check`). Those are Claude
  Code features. Under Codex the loop is prompt-driven, which is exactly the "replicate the
  multi-layer approach" this package is for.
- **Two Claude-only mechanisms to ignore if you read a `SKILL.md` directly:** (1) `voice-critic`'s
  step to "spawn a subagent (sonnet)" — run that pass inline in your Codex session instead; (2) the
  `/pptx` skill referenced by `core/style.md` for PowerPoint formatting is not part of this package,
  so skip that pointer unless you separately have it. Neither affects the writing-voice loop.
