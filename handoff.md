# Handoff — fertility-review-causes

**Last updated:** 2026-06-20
**PI:** Anup Malani
**RAs:** Alexandra Zhou (zhitongz@uchicago.edu, Codex Pro), Shravan Haribalaraman (shravanh@uchicago.edu, Claude Max pending)
**Repo:** https://github.com/anup-malani/fertility-review-causes (private)
**Prior handoffs:** [`handoff-2026-06-06.md`](./handoff-2026-06-06.md)

---

## TODAY — 2026-06-21 (pick up here)

**Meeting with RAs at 10am today.** Alexandra and Shravan were emailed last night to complete `literature-search-training.md` (now committed, they can `git pull`) and bring hand-crafted queries for `old-age-security-pension-crowdout` (C.3.c). At the meeting: compare their queries + the tool's draft → merge to envelope → approve final query → decide on calibration run.

**Step 1 (next session):** Build `calibrate-screen.mjs` — the iterative Haiku/Sonnet calibration workflow described in detail below. Then run it on the old-age-security hypothesis.

---

## SESSION LOG — 2026-06-20

### What was accomplished

**TICK-009 complete: `literature-search.mjs` fully implemented.**
- Two-pass architecture: `dryRun: true` writes query draft and exits; pass 2 (with `queriesFile`) executes searches
- Phase 1: agent reads HYPOTHESES-v5.md by slug, drafts per-database boolean queries + inclusion/exclusion criteria + rationale using QUERY_SCHEMA structured output
- Phase 2: parallel agents query OpenAlex, Semantic Scholar, Crossref, PubMed (bio only) via Python/Bash
- Phase 3: deduplication in JS (DOI primary, normalized title fallback); writes `literature/search-logs/{slug}.json`
- Known issue: `args` global not injected when calling via top-level `Workflow()` tool with `scriptPath`. Workaround: defaults hardcoded in script (`slug = args?.slug || 'old-age-security-pension-crowdout'`, `dryRun` defaults to `true`). Fix needed before production: pass inputs via a JSON sidecar file or wrap in a named workflow.

**Dry run completed on `old-age-security-pension-crowdout`.**
- Query draft: `literature/search-logs/old-age-security-pension-crowdout-query-draft.md`
- Tool initially proposed 3-axis query (CAUSE × FERTILITY × MECHANISM)
- Calibration test against 12 seminal papers: mechanism AND produced **83% false negative rate** (10/12 seminal papers missed) — papers that study pension→fertility rarely use mechanism labels in their abstracts
- Decision: **drop mechanism AND**, go to 2-axis (CAUSE × FERTILITY)
- Added `NOT "global burden of disease"` to exclude GBD epidemiology papers (main FP cluster identified via discriminating phrase analysis on 200-paper sample)
- 2-axis query returns ~81,648 results in OpenAlex — not directly screenable

**LLM screening layer designed and validated.**
- Prompt: `literature/search-logs/llm-screen-prompt.md`
- Key clause: causal direction ("pension → fertility, NOT fertility → pension sustainability") — this is the discriminating feature no keyword could capture
- Test: 24 papers (12 RELEVANT, 12 NOT_RELEVANT), 100% recall, 100% precision, all HIGH confidence
- Gray zones identified: OLG macro models (fertility as 3rd-order equilibrium), QQ-tradeoff papers with OAS mentions

**Pipeline architecture decided.**
Three-stage pipeline for all 61 hypotheses:
1. **Boolean search** (maximize recall, accept high FP) — existing `literature-search.mjs`
2. **LLM calibration screen** (iterative prompt optimization; Haiku as primary, Sonnet as teacher/gold standard) — `calibrate-screen.mjs` to build
3. **Human title/abstract screen** — existing `screen-titles-abstracts.mjs` (stub; to implement)

**RAs emailed.** Training session email sent (message ID: 19ee5cbe426877fb) to zhitongz@uchicago.edu (CC: shravanh@uchicago.edu). Subject: "Tonight's assignment — literature search training (before tomorrow's 10am meeting)." `literature-search-training.md` committed (commit 16317e6) so they can `git pull`.

### Commits this session
- `16317e6` — Add literature-search-training.md for RA pilot session
- `eccff64` — Add OAS query draft and LLM screening prompt for pilot hypothesis

---

## NEXT SESSION — BUILD `calibrate-screen.mjs`

### What it does

Iterative Haiku/Sonnet calibration workflow. Runs both models on 1,000 papers at a time from the Boolean search results. Compares divergences. Writes a calibration report. Human reviews, revises the prompt, increments batch. Repeat until false negative rate (Haiku says NOT_RELEVANT, Sonnet says RELEVANT) drops below 3% for two consecutive batches. Then apply the final routing rule to the remaining papers.

**Why this design:**
- FP at the Boolean stage costs only LLM tokens. FN at the Boolean stage is unrecoverable.
- FP at the LLM stage adds human screening burden. FN at the LLM stage is also unrecoverable.
- Haiku is fast and cheap ($12 for 81K abstracts) but makes confident errors on ambiguous abstracts.
- Sonnet is the ground truth ($147 for 81K) but we don't need to run it on everything if we have a routing rule.
- Iterative calibration derives the routing rule empirically: run both on batches of 1K, find where they diverge, revise the prompt until divergence stabilizes.
- Total cost per hypothesis: ~$10 calibration (5 batches × 1K) + ~$27 full run (Haiku + ~10% Sonnet escalation) = ~$37 vs. $147 pure Sonnet.

**Reusability plan — run once per major category:**
- Economic (C section): this hypothesis (old-age-security-pension-crowdout) is the pilot
- Biological (B section): pick one (e.g., `endocrine-disruptors-fecundity`)
- Cultural (D section): pick one (e.g., `secularization-religiosity`)
- Proximate (A section): pick one (e.g., `marriage-timing-union-formation`)
- Frameworks (E section): skip — small section, use economic routing rule
Each calibration produces a category-specific routing rule and a document of abstract patterns that required prompt revision. Those documents inform subsequent hypotheses in the same category.

### Implementation spec for `calibrate-screen.mjs`

**Input:** `args = { slug, batchNumber, promptPath, haikuModel, sonnetModel }`
- `slug`: hypothesis slug (default: `'old-age-security-pension-crowdout'`)
- `batchNumber`: which 1K batch to process (default: 1; batch N = papers (N-1)*1000 to N*1000)
- `promptPath`: path to the screening prompt markdown file (default: `literature/search-logs/{slug}-llm-screen-prompt.md`)
- `haikuModel`: override (default: `'claude-haiku-4-5-20251001'`)
- `sonnetModel`: override (default: `'claude-sonnet-4-6'`)

**Data source:** The 81K papers are NOT pre-fetched. The workflow re-queries OpenAlex using the approved query from `{slug}-query-draft.md` (machine-readable JSON block at the bottom), paginated using OpenAlex cursor, skipping to the right batch offset.

**Phase 1 — Fetch batch:** agent queries OpenAlex for papers (batch_number-1)*1000 to batch_number*1000, returns 1K paper records (title, abstract, doi, year).

**Phase 2 — Dual screen:** `parallel()` of two agents:
- Agent A: Haiku — screens all 1K abstracts using the prompt, returns `{ paperId, verdict, confidence, reason }[]`
- Agent B: Sonnet — same prompt, same papers, returns same schema

**Phase 3 — Compare divergences:** Script (JS, no agent) computes:
- Agreement rate (both RELEVANT, both NOT_RELEVANT, both UNCERTAIN)
- Haiku FN rate: papers where Haiku=NOT_RELEVANT, Sonnet=RELEVANT (dangerous)
- Haiku FP rate: papers where Haiku=RELEVANT, Sonnet=NOT_RELEVANT (annoying but safe)
- Haiku confusion rate: papers where Haiku=UNCERTAIN, Sonnet=RELEVANT or NOT_RELEVANT
- Sonnet UNCERTAIN rate: papers where Sonnet itself is UNCERTAIN (gray zone)

**Phase 4 — Write calibration report:** agent writes `literature/search-logs/{slug}-calibration-batch-{n}.md` containing:
- Summary stats (agreement rate, FN rate, FP rate, Sonnet UNCERTAIN rate)
- Whether stopping criterion met: FN rate < 3%
- Annotated list of all divergent papers (title, both verdicts, both reasons)
- **Prompt revision suggestions**: agent analyzes divergence patterns and proposes specific additions to the screening prompt to fix systematic errors
- Stopping recommendation: continue to next batch, or converged

**Phase 5 — Write routing rule (only when stopping criterion met):** writes `literature/search-logs/{slug}-routing-rule.md`:
- Recommended Haiku confidence threshold for routing to Sonnet
- Estimated cost per 1K papers under this routing rule
- Observed FN rate at this threshold

**Output:** returns `{ batchNumber, agreementRate, haikuFnRate, haikuFpRate, stoppingCriterionMet, reportPath }`

### Prompt schema (for calibration agent screening output)

Each screened paper should return:
```json
{
  "paperId": "string (doi or title hash)",
  "title": "string",
  "verdict": "RELEVANT | NOT_RELEVANT | UNCERTAIN",
  "confidence": "HIGH | MEDIUM | LOW",
  "reason": "string (one sentence)"
}
```

### After calibration converges

Once the routing rule is derived for the economic category:
1. Update `literature/search-logs/llm-screen-prompt.md` with the final prompt version
2. Run full screen on 81K papers using routing rule (Haiku primary, Sonnet for MEDIUM/LOW/UNCERTAIN)
3. Output: `literature/search-logs/old-age-security-pension-crowdout.json` updated with `llm_verdict`, `llm_confidence`, `llm_reason` fields on each paper
4. Hand survivors to `screen-titles-abstracts.mjs` for human review

### Known issues / open questions
- `args` global not injected in top-level `Workflow({ scriptPath })` calls — fix the workflow harness or pass inputs via a JSON sidecar; document in TICK-004
- Retrieval cap still open: do we re-query OpenAlex per batch (cursor-paginated), or do we store all 81K to a local file first? Cursor approach is simpler but requires re-auth each batch. Local file approach requires ~50MB disk but is faster and more reliable for iteration.
- The `literature-search.mjs` `dryRun` default is currently `true` — flip to `false` before running pass 2 on this hypothesis.

---

---

## HYPOTHESES.md status (2026-06-18)

| Version | Description | Status |
|---------|-------------|--------|
| v1 = `HYPOTHESES.md` | Original 65 entries, 4 flat categories | Preserved as authoritative v1 |
| v2 | Two-tier structure + PI inline comments | Archived |
| v3 | 47 entries, 5 sections, Economic sub-structured | Archived |
| v4 | v3 + hierarchical outline codes (A/B/C/D/E) | Archived |
| **v5** | **61 active entries + 2 deprecated; 14 new entries from bookmark + literature sweep** | **Current working version** |

New in v5: A.23 (co-residence), A.24 (dating apps), B.6 (microplastics/PFAS), B.7 (antidepressants), C.2.h (digital leisure substitution), C.3.g (student debt), D.3.a–c (psychological distress sub-section: mental health, climate anxiety, despair).

Sweep log: `literature/search-logs/hypothesis-sweep-2026-06-14.md`

---

## What this project is

Cochrane-style systematic review of every major proposed explanation for fertility decline.
65 hypotheses in two tiers — Proximate Causes (mechanisms) + three root-cause categories (Economic / Biological / Cultural) — each
evaluated against three phenomena (pre-modern, FDT, SDT). Per-hypothesis GRADE rating of
causal credibility + demographic-significance verdict. Chapter per hypothesis is the atomic
deliverable. Methodology: PROTOCOL.md. RA operating manual: RA-PLAYBOOK.md. AI context:
AGENTS.md (give this to whatever LLM you're using at session start).

---

## How the work is organized — two separate questions

### Question 1: Task dependencies (the ticket system)

Some tasks can be done at the same time (parallel); others must wait for something else to finish first (serial). | Task | Can start when… |
|------|----------------|
| 1A | immediately |
| 1B | immediately — run alongside 1A, they don't touch each other |
| 2A | 1A is done |
| 2B | 1B is done |
| **C** | **both 2A AND 2B are done — not just one of them** |

1A and 1B can be worked simultaneously. 2A cannot start until 1A is done. 2B cannot start until 1B is done. Task C cannot start until *both* 2A and 2B are finished — the last row is the key case.

The `tickets/` system encodes this with the `Blocked by` field. Our QUEUE.md separates open (start now) from blocked (wait). This is a solved problem for this project.

The one thing the ticket system does not yet handle: two people picking up the same ticket at the same time. That is Shravan's TICK-008 — a lightweight real-time coordination layer on top.

### Question 2: How we run the research (the piloting approach)

Separate from task ordering is the question of *what* the tasks are and how we assign the 65 hypotheses across three contributors. **Decision (2026-06-14):**

- **Phase 1 (weeks 1–2):** All three work through one hypothesis together — the pilot (quantity-quality tradeoff). Anup sets pace, RAs do sub-tasks. Goal: everyone knows what "done" looks like at each pipeline stage. Output: first chapter.
- **Phase 2 (weeks 3+):** RAs each take separate hypotheses and run them independently. Parallel tracks. Anup reviews chapters.
- **Optional Phase 2b (week 3–4):** Both RAs take the *same* hypothesis independently with their own AI tool, compare processes. Captures AI-tool differences. Lives in `meta-experiments/`.

This decision will be sent to RAs in a follow-up email after Phase 1 is underway.

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
