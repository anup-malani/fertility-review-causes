# Repository Organization (Proposed)

**Status:** Proposal for discussion — not yet adopted.
**Author:** Shravan (RA)
**Date:** 2026-07-15

## 1. Purpose

The repo has grown organically through the OAS pilot and now carries three kinds
of clutter that make it hard for a new RA (or a returning one) to find the live
version of anything:

1. **Function-split, not module-split.** Code lives in `source/`, inputs in
   `data/`, outputs in `output/` — three parallel trees. To understand one
   pipeline stage you have to hop across all three and mentally rejoin them.
2. **Filename versioning.** `HYPOTHESES.md` + `HYPOTHESES-v2..v5.md`,
   `RA-ONBOARDING v1/v2`, `handoff.md` + `handoff-2026-06-06.md`. This is the
   single anti-pattern Gentzkow–Shapiro name most explicitly: git already stores
   history, so parallel `-vN` files just create ambiguity about which is live.
3. **Flat output dump.** `output/` holds ~50 files, almost all prefixed
   `old-age-security-pension-crowdout-*`, with no marker of which are current
   deliverables vs. superseded intermediates (`...-recall.json` vs.
   `...-recall-deghosted.json`, a `retracted-2026-07-08/` folder, etc.).

This document proposes a structure that fixes all three, using only conventions
a reader can verify against one reference: **Gentzkow & Shapiro, *Code and Data
for the Social Sciences: A Practitioner's Guide*** (the "GS guide"). Nothing
here requires reading this file to understand the repo — that is the design goal.

## 2. The three GS rules we apply

The GS guide's *Directories* chapter gives us everything we need:

> **Rule A — Separate directories by function, into self-contained modules.**
> A *module* is one pipeline step. Everything that step needs and produces lives
> under it; you can understand or rerun it without leaving its folder.

> **Rule B — Inside every module, separate inputs from outputs.**
> We use the canonical four-way split: `code/`, `input/`, `output/`, `temp/`.
> A module's `input/` is *linked* from the previous module's `output/` — never
> hand-copied — so the data flows in one direction and there is exactly one
> authoritative copy of every file.

> **Rule C — Do not version files by name; version them with git.**
> There is one `hypotheses.md`, not five. History lives in the commit log.
> Genuinely-superseded artifacts we still want to keep go in an `_archive/`
> subfolder (§4), never in a `-v2` sibling.

The one place we extend GS is the **live/archive record** (§4): a systematic
review accumulates deliverables that are *retired but citable* (a retracted
recall set, a pre-registration draft, a superseded hypothesis list). GS's
"no `-vN` **siblings**" rule still holds — nothing lives next to the live file
under a `-v2` name — but rather than dropping retired versions into git history
where they're a click away only if you know to look, we give the archive a named
home (`_archive/`) and index it in the manifest. The archive *is* our answer to
filename versioning.

## 3. Proposed top-level structure

Three zones: **governance** (flat files at root, read by humans), **pipeline**
(numbered modules, the actual build), and **meta** (project-management trails).

```
fertility-review-causes/
│
├── README.md              ← orientation for any reader
├── CLAUDE.md              ← agent context
├── AGENTS.md              ← agent-interop rules
├── PROTOCOL.md           ← methodology spec (the "what and why")
├── RA-PLAYBOOK.md        ← RA roles + escalation
├── HYPOTHESES.md         ← master hypothesis list (ONE file; §4 retires the -vN copies)
├── MANIFEST.md           ← NEW: index of every live deliverable + its status (§4)
├── Makefile              ← one command builds the pipeline (GS Rule: automate)
│
├── pipeline/             ← the build, as ordered modules (Rules A + B)
│   ├── 1-enumerate/       hypothesis enumeration
│   ├── 2-search/          per-hypothesis literature search
│   ├── 3-screen/          PRISMA screening
│   ├── 4-extract/         study & effect extraction
│   ├── 5-analyze/         meta-analysis, GRADE, demographic significance
│   ├── 6-synthesize/      per-hypothesis chapters
│   └── 7-paper/           compiled book + JEL summary
│
├── lib/                  ← shared code used by >1 module (forest plots, GRADE helpers)
│
├── docs/                 ← methodology & style guides, design notes (this file)
│
├── project/             ← NEW home for the PM trail (§5)
│   ├── decisions/         dated decision records
│   ├── tickets/           work tickets + QUEUE
│   ├── meeting-summaries/
│   ├── handoffs/          dated handoff notes (replaces root handoff*.md)
│   └── session-log.md
│
├── datastore/           ← symlink to large-file storage (not version-controlled)
└── meta-experiments/    ← "best AI for review" side studies (kept as-is)
```

### Inside a module (the repeating unit)

Every folder under `pipeline/` has the **same** four-way shape. Once you learn
one, you know all seven:

```
pipeline/5-analyze/
├── README.md      ← what this step does, how to run it, what it emits
├── code/          ← scripts for THIS step only (e.g. oas_meta_pipeline.py)
├── input/         ← symlinks to pipeline/4-extract/output/… (never edited here)
├── output/        ← this step's deliverables, one subfolder per hypothesis
│   └── old-age-security-pension-crowdout/
│       ├── meta-analysis.json
│       ├── grade-rating.md
│       └── _archive/         ← retired-but-kept artifacts (§4)
└── temp/          ← scratch; git-ignored, safe to delete anytime
```

Key consequences, all straight from GS:

- **The hypothesis is a *key*, not a module.** The pipeline is identical for
  every hypothesis, so hypotheses become subfolders inside each module's
  `output/`, not seven parallel top-level trees. Adding a hypothesis adds one
  subfolder per module — no new structure.
- **Data flows one way.** `input/` is always symlinks into the previous
  module's `output/`. There is one authoritative copy of every file, and you can
  always see which upstream product a step consumes.
- **`temp/` is disposable** and git-ignored (as it already is). Nothing in
  `temp/` is ever a deliverable.
- **`lib/` vs `code/`:** if two modules need it, it goes in top-level `lib/`;
  if only one does, it stays in that module's `code/`.

## 4. Live vs. archive: the record (requirement c)

Two mechanisms, working together:

**(1) `_archive/` subfolders.** Any file that is superseded but worth keeping
(a retracted recall set, an earlier scoring pass, a draft we cite in the
methods) moves into an `_archive/` subfolder *next to the live version*, never
into a `-v2` sibling. The live file keeps the plain name. So:

| Instead of…                                   | We keep…                                                        |
|-----------------------------------------------|-----------------------------------------------------------------|
| `...-recall.json` + `...-recall-deghosted.json` | `recall.json` (live) + `_archive/recall-preghost.json`        |
| `output/retracted-2026-07-08/`                | `…/output/<hyp>/_archive/retracted-2026-07-08/`                |
| `HYPOTHESES.md` + `HYPOTHESES-v2..v5.md`      | `HYPOTHESES.md` (live) + `docs/_archive/hypotheses-history/v2..v5.md` |

Rule: **if a file is not in `_archive/`, it is live.** That makes "what's
current?" answerable by looking, with no tribal knowledge.

**(2) `MANIFEST.md` at root.** A single flat index — the one place that answers
"what are the current deliverables and where are they?" One line each:

```markdown
# Manifest — live deliverables

## Governance
- PROTOCOL.md — methodology spec — LIVE
- HYPOTHESES.md — master hypothesis list — LIVE (supersedes v2–v5, in git history)

## Pipeline — old-age-security-pension-crowdout (pilot)
- pipeline/5-analyze/output/old-age-security-pension-crowdout/meta-analysis.json — LIVE
- pipeline/6-synthesize/output/old-age-security-pension-crowdout/chapter.md — LIVE
- .../\_archive/retracted-2026-07-08/ — ARCHIVED 2026-07-08, see decisions/2026-07-08-…
```

The manifest is the human-readable table of contents; the `_archive/` folders
are the enforcement. Neither requires reading code to interpret.

## 5. What moves where (migration map)

No file is deleted in this proposal — everything relocates or is retired to git
history. Representative moves:

| Current location                                    | Proposed home                                                        |
|-----------------------------------------------------|----------------------------------------------------------------------|
| `source/analysis/oas_meta_pipeline.py`              | `pipeline/5-analyze/code/`                                            |
| `source/build/goldset/`                             | `pipeline/2-search/code/goldset/`                                    |
| `source/lib/`, `source/paper/`                      | `lib/`, `pipeline/7-paper/code/`                                      |
| `data/raw/`, `data/docs/`                           | `pipeline/1-enumerate/input/` (+ symlinks downstream)                |
| `literature/search-logs/`                           | `pipeline/2-search/output/<hyp>/search-logs/`                        |
| `extraction/*.csv`                                  | `pipeline/4-extract/output/<hyp>/`                                   |
| `output/old-age-…-*.{md,json,csv}` (flat ~50 files) | split across `4-extract` / `5-analyze` / `6-synthesize` output/<hyp> |
| `output/chapters/`                                  | `pipeline/6-synthesize/output/<hyp>/chapter.md`                      |
| `output/tables/`, `output/figures/`                 | `pipeline/5-analyze/output/<hyp>/`                                   |
| `output/retracted-2026-07-08/`                      | nearest `output/<hyp>/_archive/retracted-2026-07-08/`                |
| `HYPOTHESES-v2..v5.md`                              | `docs/_archive/hypotheses-history/v2..v5.md` + line in `MANIFEST.md` |
| `RA-ONBOARDING v1/v2.{md,docx}`                     | latest → `docs/ra-onboarding.md`; v1 → `docs/_archive/ra-onboarding/`|
| `handoff.md`, `handoff-2026-06-06.md`               | `project/handoffs/2026-06-06.md`, `…/2026-07-13.md`                  |
| `decisions/`, `tickets/`, `meeting-summaries/`      | under `project/`                                                     |
| `temp/*`                                            | into the owning module's `temp/` (stays git-ignored)                 |

## 6. Open questions for Anup / discussion

1. **Numbered vs. named modules.** `1-enumerate` makes pipeline order obvious
   and sorts correctly; the cost is renumbering if we insert a stage. Acceptable?
2. **`.docx` onboarding files.** Keep the Word originals in the repo, or treat
   the `.md` as canonical and store `.docx` in `datastore/`?
3. ~~How aggressively to retire `-vN` files.~~ **Decided:** superseded versions
   go into `_archive/` (e.g. `docs/_archive/hypotheses-history/`), not git
   history alone — this is exactly what the archive convention (§4) is for. They
   stay one click away and indexed in the manifest, without ambiguity about
   which file is live.
4. **Migration sequencing.** Suggest doing it per-module in the OAS pilot first,
   verifying the Makefile still builds after each move, before touching a second
   hypothesis.
```
