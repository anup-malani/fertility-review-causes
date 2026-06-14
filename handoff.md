# Handoff — fertility-review-causes

**Last updated:** 2026-06-14
**PI:** Anup Malani
**RAs:** Alexandra Zhou (zhitongz@uchicago.edu, Codex Pro), Shravan Haribalaraman (shravanh@uchicago.edu, Claude Max pending)
**Repo:** https://github.com/anup-malani/fertility-review-causes (private)
**Prior handoffs:** [`handoff-2026-06-06.md`](./handoff-2026-06-06.md)

---

## What this project is

Cochrane-style systematic review of every major proposed explanation for fertility decline.
65 hypotheses across four categories (Demographic / Economic / Biological / Cultural), each
evaluated against three phenomena (pre-modern, FDT, SDT). Per-hypothesis GRADE rating of
causal credibility + demographic-significance verdict. Chapter per hypothesis is the atomic
deliverable. Methodology: PROTOCOL.md. RA operating manual: RA-PLAYBOOK.md. AI context:
AGENTS.md (give this to whatever LLM you're using at session start).

---

## Work queue

All pending work is tracked in `tickets/QUEUE.md`. Start there. Do not create ad-hoc tasks
outside the ticket system.

**Summary as of 2026-06-14:**

| Priority | Ticket | Title | Who | Status |
|----------|--------|-------|-----|--------|
| 1 | TICK-007 | Gift Shravan Claude Max | Anup | open — do today |
| 2 | TICK-002 | Fix Cultural-count in Merge Notes | any | open — quick |
| 3 | TICK-003 | Promote batch-edits lesson | any | open — quick |
| 4 | TICK-004 | Revisit .gitignore for .claude/workflows/ | any | open — quick |
| 5 | TICK-008 | Design collab/ticketing system | Shravan | open — this week |
| 6 | TICK-001 | PI review of HYPOTHESES.md | Anup | open — blocks pipeline |
| 7 | TICK-005 | PROTOCOL.md + RA-PLAYBOOK.md readability pass | All | open — blocks OSF |
| — | TICK-006 | OSF pre-registration | Anup | blocked (TICK-001, TICK-005) |
| — | TICK-009 | Implement literature-search.mjs | any | blocked (TICK-001) |
| — | TICK-010 | Run pilot (quantity-quality tradeoff) | any | blocked (TICK-009) |

---

## State as of 2026-06-14

### Done

- **Project scaffolded** (2026-06-06): PROTOCOL.md, RA-PLAYBOOK.md, HYPOTHESES.md stub, full
  directory tree, 13 workflow stubs, git + GitHub remote.
- **RA onboarding** (2026-06-08 to 2026-06-10): RA-ONBOARDING v2.md authored and emailed.
- **Weekly sync set up:** Saturdays 10-11am CT, 2026-06-13 through 2026-08-15 (July 4 skip).
  Calendar event `uhni8vjlodg47msojg9cdgrd8g`.
- **enumerate-hypotheses.mjs implemented and run** (2026-06-10): 65 hypotheses, 4 categories,
  annotated with `**why:**` glosses.
- **Repo renamed** `fertility-review` → `fertility-review-causes` (2026-06-13).
- **Both RAs added as GitHub collaborators**: AlexandraZ27, shravanh7472 (2026-06-13).
- **Bibliography system re-architected**: `datastore/studies.json` → `make bib`; Zotero
  optional (2026-06-13).
- **Slack deferred**: comms via email/iMessage + `escalation-log.md` (2026-06-13).
- **RA kickoff held** (2026-06-13 10am CT): Alexandra + Shravan on Zoom. Went fine.
  Assignment: Shravan to design team coordination/ticketing system (LLM-agnostic).
- **Ticket system scaffolded** (2026-06-14): `tickets/` with QUEUE.md and TICK-001–010.
- **AGENTS.md created** (2026-06-14): LLM-agnostic AI context file at repo root.

### Pending immediate action (Anup, today)

**TICK-007 — Gift Shravan Claude Max.**
Shravan confirmed the plan (email thread 19ea817c430b8b49, message 17, 2026-06-14 03:04 UTC).
When gifting, also reply to the thread confirming:
1. Max plan gifted (instructions to activate)
2. UChicago Enterprise (~1 month out) does support Claude Code CLI — Shravan's question
3. Alexandra's Max plan standing by when she hits Codex limits

---

## RA status

| RA | GitHub | LLM | Status |
|----|--------|-----|--------|
| Alexandra Zhou | AlexandraZ27 | Codex Pro ($100/mo, self-funded) | Access confirmed; kickoff attended |
| Shravan Haribalaraman | shravanh7472 | Claude Max (to be gifted by Anup) | Access confirmed; kickoff attended; Max pending |

---

## Key artifacts

| Artifact | Path | Notes |
|----------|------|-------|
| AI context file (RA-facing) | `AGENTS.md` | Give to Claude/Codex at session start |
| Work queue | `tickets/QUEUE.md` | Start here each session |
| Hypothesis list | `HYPOTHESES.md` | DRAFT; 65 entries; needs PI review (TICK-001) |
| Methodology | `PROTOCOL.md` | Shareable; needs readability pass (TICK-005) |
| RA operating manual | `RA-PLAYBOOK.md` | Needs readability pass (TICK-005) |
| RA onboarding | `RA-ONBOARDING v2.md` | Sent to RAs 2026-06-08 |
| Bibliography generator | `scripts/make_bib.py` | Run via `make bib` |
| Bibliography source | `datastore/studies.json` | DOI-keyed; edit here, not in .bib files |
| Implemented workflows | `.claude/workflows/enumerate-hypotheses.mjs` | Gitignored; TICK-004 addresses this |
| Stub workflows | `.claude/workflows/literature-search.mjs` et al. | 11 stubs; throw on invocation |
| Session log | `session-log.md` | Cumulative |
| Decisions | `decisions/` | Durable design decisions |

---

## Next session quick-start

```
1. cd /Users/amalani/github/fertility/fertility-review-causes
2. Read this handoff.md (you're here)
3. Read tickets/QUEUE.md — pick the first open ticket assigned to you or 'any'
4. If Anup: do TICK-007 (gift Shravan Max) first — takes 5 minutes
```

---

## Patterns and lessons learned

### enumerate-hypotheses.mjs
Ran end-to-end without intervention. Merge agent's count self-report (60) disagreed with
actual file (65). Lesson: verify counts by reading the file, not the agent summary.

### Batch edits via script, not agent
Agents doing many sequential Edit calls on one file stall (the `annotate-hypotheses` workflow
stalled after ~47/65 edits). Better pattern: agent returns structured data → apply
programmatically. Recovery: extract cached StructuredOutput from agent jsonl transcripts,
apply via Python regex. See `temp/apply_explanations.py`. TICK-003 promotes this to decisions/.

### Email account discipline
RA replies came to the UChicago account. Always check both Gmail accounts for RA threads.
