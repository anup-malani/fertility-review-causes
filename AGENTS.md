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
All work is tracked in `tickets/`. Before starting any task, check `tickets/QUEUE.md` for the
next open item. When you pick up a ticket, mark it `in-progress` and note your name. When done,
mark it `done`, append a completion note, and update `QUEUE.md`. Never work outside a ticket
without first creating one.

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
from source. Push to `main`; no branch workflow yet.

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
