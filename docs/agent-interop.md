# Claude / Codex Interop

This project does not translate Claude conversations into Codex conversations, or the reverse.
Agents interoperate through tracked repo artifacts: tickets, protocol documents, search logs,
JSON outputs, extraction files, chapter drafts, handoff notes, and commits.

## Shared contract

Every pipeline stage should have:

- A named stage in `PROTOCOL.md`.
- A ticket or decision record when implementation details are not obvious.
- Tracked input files and tracked output paths.
- A reproducible log in `literature/search-logs/`, `prisma/`, `extraction/`, `output/`, or
  `session-log.md`, depending on the stage.

The artifact path is the interface. Agent transcripts, private memory, and tool-specific
session state are not part of the interface.

## Invocation mapping

Claude Code can invoke Claude workflow scripts directly with `Workflow(...)`. Codex cannot use
that tool. Until `TICK-004` moves executable workflow logic into a tracked, agent-neutral
location, Codex should treat the Claude command as a stage label and execute the same stage
contract from `PROTOCOL.md`, the relevant ticket, and the latest handoff.

| Stage | Claude invocation pattern | Codex equivalent |
|---|---|---|
| Hypothesis enumeration | `Workflow({ name: "enumerate-hypotheses", args: {...} })` | Read `PROTOCOL.md`, `HYPOTHESES.md`, and the ticket; edit the tracked hypothesis file directly; record changes in `session-log.md` or the ticket log. |
| Literature query draft | `Workflow({ name: "literature-search", args: { slug, dryRun: true } })` | Draft the query file at `literature/search-logs/{slug}-query-draft.md`, including the human-readable rationale and machine-readable JSON block. |
| Literature search execution | `Workflow({ name: "literature-search", args: { slug, queriesFile } })` | Execute the approved database/API search logic with local scripts or Codex tooling; write `literature/search-logs/{slug}.json` and any PRISMA search log. |
| Sequential screen | `Workflow({ name: "sequential-screen", args: { slug } })` | Pull ranked OpenAlex batches, apply the documented screening prompt/routing rule, and write the same `literature/search-logs/{slug}-sequential-screened.json` output schema. |
| Citation snowball | `Workflow({ name: "snowball-citations", args: { slug } })` | Use the relevant seed set, fetch backward/forward citations, deduplicate by DOI/title, screen, and write `literature/search-logs/{slug}-snowball.json`. |
| Prioritization | `Workflow({ name: "prioritize-papers", args: { slug } })` | Score the relevant union on evidence type, identification, and centrality; write `literature/search-logs/{slug}-prioritized.json`. |
| Title/abstract screen | `Workflow({ name: "screen-titles-abstracts", args: { slug } })` | Add screen verdict fields to the search-log JSON or create the agreed RA review sheet; preserve the routing rule and audit counts. |
| PDF acquisition | `Workflow({ name: "acquire-pdfs", args: { slug } })` | Record which PDFs were found, missing, or escalated; put retrieved PDFs under `literature/pdfs/{slug}/` if available. |
| Data extraction | `Workflow({ name: "extract-data", args: { slug } })` | Fill `extraction/{slug}.csv` or the agreed extraction database from included studies; flag fields that require RA verification. |
| Risk of bias | `Workflow({ name: "risk-of-bias", args: { slug } })` | Apply the protocol rubric and write structured risk-of-bias fields in the extraction output or companion log. |
| Meta-analysis | `Workflow({ name: "meta-analyze", args: { slug } })` | Run the documented R/Python analysis from tracked inputs; write generated tables/figures under `output/`. |
| Demographic significance | `Workflow({ name: "demographic-significance", args: { slug } })` | Compute PM/FDT/SDT significance metrics from extracted effects and macro data; write reproducible outputs under `output/`. |
| GRADE rating | `Workflow({ name: "grade-rating", args: { slug } })` | Produce the per-phenomenon GRADE ratings and escalation notes if raters disagree by more than one level. |
| Chapter synthesis | `Workflow({ name: "synthesize-chapter", args: { slug } })` | Draft `output/chapters/{slug}.md` using the fixed chapter template and only tracked evidence. |
| Lay readability check | `Workflow({ name: "lay-readability-check", args: { slug } })` | Review the chapter against `RA-PLAYBOOK.md`; write flags in the chapter, ticket log, or escalation log as appropriate. |
| Cross-chapter check | `Workflow({ name: "cross-chapter-check", args: {...} })` | Compare chapter claims against existing chapters and record contradictions or required revisions. |

## Handoff rules

- Put durable project memory in `handoff.md`, `session-log.md`, tickets, decisions, and output files.
- Put task status in `tickets/QUEUE.md` and the individual ticket log.
- Put methodological choices in `decisions/` when they should bind future work.
- Put per-hypothesis search decisions in `literature/search-logs/`.
- Do not depend on Claude transcript history, Codex conversation history, local caches, or untracked
  `.claude/`, `.codex/`, `.agents/`, or `temp/` files for another contributor to continue work.

## Current limitation

`TICK-004` remains the main infrastructure gap. The repo should track the executable workflow
logic or move it to an agent-neutral script location. Until then, Claude workflow commands are
not reproducible instructions for Codex; they are pointers to the stage contract and expected
artifact paths.
