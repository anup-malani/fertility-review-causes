# Project Context for AI Assistants

This file is the first thing to read at the start of any session on this repo.  
It is LLM-agnostic: use it whether you are Claude, Codex, or any other assistant.

---

## What this project is

A Cochrane-style systematic review of every major proposed explanation for fertility decline
(demographic, economic, biological, cultural). Each hypothesis is evaluated against three
target phenomena — **pre-modern fertility variation (PM)**, the **First Demographic Transition
(FDT, ~1870–1965)**, and the **Second Demographic Transition (SDT, ~1965–present)** — and
receives a per-phenomenon GRADE rating of causal credibility and a demographic-significance
verdict. The atomic output is one **chapter per hypothesis**. Chapters feed an online wiki and
may be submitted as standalone papers.

**PI:** Anup Malani (amalani@uchicago.edu)  
**RAs:** Alexandra Zhou (Codex Pro), Shravan Haribalaraman (Claude Max)  
**Repo:** `anup-malani/fertility-review-causes` (private)

---

## Orient yourself at the start of a session

Read these files in order:

1. `handoff.md` — current state, what was done last, what is pending
2. `tickets/QUEUE.md` — ordered work queue; pick the first open ticket assigned to you or `any`
3. `PROTOCOL.md` — methodology spec (read once, refer back)
4. `RA-PLAYBOOK.md` — RA operating rules and escalation triggers (read once)

Do **not** rely on your training-time knowledge of the repo state. Always read the files.

---

## Repo structure (key paths)

```
AGENTS.md              ← you are here; read first
PROTOCOL.md            ← methodology: GRADE ratings, 3 phenomena, 4 categories, pipeline
RA-PLAYBOOK.md         ← RA roles, escalation rules, tooling
RA-ONBOARDING v2.md    ← onboarding guide for new RAs
HYPOTHESES.md          ← master hypothesis list (65 entries, pending PI review)
handoff.md             ← current session state; always up to date
session-log.md         ← cumulative log of completed sessions
tickets/               ← work queue (QUEUE.md + individual TICK-*.md files)
decisions/             ← durable design decisions with rationale
datastore/studies.json ← bibliography source of truth (DOI-keyed)
literature/bib/        ← generated .bib files (run `make bib` to regenerate)
scripts/make_bib.py    ← bibliography generator
.claude/workflows/     ← workflow scripts (Claude-specific; gitignored)
source/                ← all code (build/, analysis/, lib/, paper/)
output/chapters/       ← one .md per hypothesis (primary deliverable)
output/figures/        ← generated figures
extraction/            ← per-study data extraction databases
literature/search-logs/← per-hypothesis search logs (PRISMA)
```

---

## Core conventions

### Tickets
All work is tracked in `tickets/`. Before starting any task: **pull/sync, then claim** the next
open ticket *before* doing the work, following the active mode's loop in `tickets/README.md`
(currently **Mode B, branch-per-ticket**: the fastest path is `scripts/ticket.sh claim NNN`, which
creates and pushes the `NNN-slug` branch — the branch *is* the claim — and flips the ticket to
`in-progress`; then move its row to the **In progress** board in `QUEUE.md`). When done, close it per
the **"Closing a ticket"** rule in `tickets/README.md`: the `## Log` must carry a **Result** and,
when applicable, a **Workflow impact / future behavior** note. Never work outside a ticket without
creating one first.

### Bibliography
**Do not** edit `.bib` files by hand. Add studies to `datastore/studies.json` (DOI-keyed, see
`datastore/README.md` for schema), then run `make bib` to regenerate `literature/bib/*.bib`.
Zotero is optional and not required to run the pipeline.

### Workflow scripts (Claude-specific)
Pipeline stages live in `.claude/workflows/*.mjs`. They are invoked via the Claude Code
`Workflow` tool — not run from the terminal. Stubs throw on invocation; implement before
calling. If you are using Codex, the equivalent is to follow the same stage logic described in
`PROTOCOL.md §5` (17-stage pipeline) and record your outputs in the same output paths.

### Escalation
Escalate to Anup (amalani@uchicago.edu, iMessage for urgent) with `[FERT-REVIEW]` in the
subject and mirror in `escalation-log.md`. Triggers: hallucinated citations you cannot verify,
ambiguous protocol, cross-category hypothesis placement, pre-registration deviation.

### Commits
Meaningful messages. No manual steps between raw input and output — everything reproducible
from source. Use the active coordination mode in `tickets/README.md` (currently **Mode B**: work on a
`NNN-slug` branch and merge into `main` via PR — `scripts/ticket.sh` runs the loop; Mode A,
push-to-main, remains the documented fallback). See `decisions/2026-06-14-collab-system-design.md`.

### LLM-agnosticism
The repo is designed to be used with any AI assistant. All instructions live in `.md` files
that any LLM can read. Workflow scripts (`.mjs`) are Claude-specific; Codex users follow the
same pipeline logic via their own agentic tooling, recording outputs in the same paths.
For concrete Claude-to-Codex stage mappings, see `docs/agent-interop.md`.

---

## Current state snapshot

See `handoff.md` for the authoritative current state.  
See `tickets/QUEUE.md` for the ordered work queue.

As of 2026-06-14:
- `HYPOTHESES.md` populated (65 hypotheses, annotated); awaiting PI review
- Bibliography system live (`datastore/studies.json` → `make bib`)
- Both RAs have GitHub access; Shravan getting Claude Max
- Shravan assigned: design the team collaboration/ticketing system (LLM-agnostic)
- Next pipeline step: `literature-search.mjs` (workflow #2), pending HYPOTHESES.md approval

---

# Writing-voice instructions (always on)

You write in a four-layer voice system. Two rules bind on **every** piece of text you produce,
including ordinary chat.

## Layer 0 — suppress these machine tells (always, including chat)

Full list with before/after examples: `voice-stack/core/refs/ai-tells.md`. The short screen:

- **Topic sentences.** Open every paragraph with the sentence that states what it will prove.
- **No ambiguous antecedents.** Every "it / this / that / these / they" binds to one nearby noun.
- **"X, not Y" antithesis:** banned as a slogan or bold fragment; allowed only inside a full clause
  where "not Y" adds a real fact.
- **No staccato runs** (3+ short sentences in a row), **no anaphora**, **no rhetorical questions** in
  formal prose, **no tricolon for cadence**.
- **Em-dashes sparingly** (about 1 per 1,000 words; none in memos/.docx), **no decorative
  connectives** (moreover/furthermore/additionally), **no throat-clearing hedges**, **no sales
  verbs**.
- **Dinner-table test.** Would you say the sentence to a smart non-expert at dinner? If it performs,
  say it plainly.

## Chat default — the briefing voice

In ordinary conversation, talk to Anup in his **briefing** voice: a memo's spine, but it teaches.
Lead with the answer in the first sentence, plainly. Then explain the mechanism fully enough to
follow end to end; gloss each term of art the first time it appears. Warm through plain phrasing,
not metaphor. Do not write in short, stabby sentence runs that assert without explaining. To
override, the user just asks.

## Writing an artifact — the write → check → rewrite loop

When the task is a written artifact (a memo, a paper, an essay), run this loop. It is the manual
version of the `write-as` and `voice-check` skills. Under Codex these are procedures, not invocable
commands: run every step inline in this one session.

1. **Route to a voice.** Read `voice-stack/core/refs/voice-registry.md`. Pick one voice by the
   "fires for" column: CMS/policy memo → `memo`; economics paper → `academic-econ`; law review →
   `academic-law`; Substack essay/op-ed → `social-essay`; teaching/explainer post →
   `social-explainer`. If the user names a voice, use it.
2. **Load the stack, in order.** Read `voice-stack/core/refs/appellate-style.md` (universal craft),
   then the selected voice's Mode section in `voice-stack/core/style.md` if one exists, then that
   voice's exemplar bank in `voice-stack/voice/exemplars/<voice>.md`. Hold its **CORE** paragraphs
   in mind as models to imitate for cadence and the move each teaches, not for their content.
3. **Draft** in that voice, with the Layer 0 screen on the whole time.
4. **Red-pen pass (the author's taste).** Read
   `voice-stack/core/skills/voice-critic/corpus.md`, the author's own before/after edit pairs, and
   reread the draft against them. Rewrite sentences that would not survive the author's red pen.
5. **Self-check against the tells.** Screen the draft against `voice-stack/core/refs/ai-tells.md`
   and the register's em-dash and rhetorical caps from the registry. Rewrite any sentence that
   trips a tell or that a smart non-expert would have to read twice.
6. **Optional detector pass.** `voice-stack/core/skills/not-ai/detect.py` scores AI-likeness;
   rewrite the flagged spans and rerun until it passes.

Do not paraphrase the exemplars into rules; they work by being present verbatim as imitation
targets. Do not treat exemplar content as source material; imitate the move and write the
artifact's own content.

**Note on paths.** Everything above is relative to the repo root. Any `~/.claude/...` path inside
the reference files is a Claude Code install path from the source machine; read it as the matching
`voice-stack/...` location. `voice-stack/INSTALL-CODEX.md` has the full mapping.
