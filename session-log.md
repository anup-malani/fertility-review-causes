# Session Log

Cumulative session log. Each entry records what happened, what was produced, and what remains open. Entries are chronological.

---

## [2026-06-06 17:05] — Project scaffolding via Workflow tool

**Agent:** primary
**Machine:** MacBookPro
**Working directory:** /Users/amalani/github/fertility/fertility-explanations-review

### Summary

First session for this project. Started from a `/workflows` question that turned into a substantive project: a Cochrane-style systematic review evaluating every major proposed explanation for fertility decline, organized by four categories (demographic / economic / biological / cultural) and three target phenomena (pre-modern / FDT / SDT). Used plan mode to develop the methodological protocol, then exited to execute via the `Workflow` tool. Project is fully scaffolded at the repo root, on GitHub (private), wired for auto-sync, with PROTOCOL.md and RA-PLAYBOOK.md ready for PI review and RA onboarding. The next concrete task — implementing `enumerate-hypotheses.mjs` — is captured in `handoff.md`.

### Inputs

- User prompt describing the project goal (Cochrane-like authoritative review of fertility-decline explanations)
- User answers to three clarifying questions (scope = PM/FDT/SDT as separate phenomena; deliverable = chapters → book → JEL article; RAs are undergrads who keep pipeline running and do human-in-the-loop validation)
- `/Users/amalani/.claude/refs/scaffolding.md` and `/Users/amalani/github/research-template/DEPLOY.md` for Shapiro-Gentzkow convention
- `/Users/amalani/github/fertility/fertility-evolution/` as the structural reference

### Outputs

- `/Users/amalani/.claude/plans/cozy-growing-crab.md` — approved plan with PROTOCOL.md and RA-PLAYBOOK.md embedded verbatim
- `PROTOCOL.md` — methodological spec, 9 sections (aim, three phenomena, four categories, operational definitions of credibility + demographic significance, 17-stage pipeline, chapter template, tooling, pre-registration, update cadence); ready for PI + RA review
- `RA-PLAYBOOK.md` — five RA roles, escalation rules, tooling setup, weekly cadence, common AI failure modes to watch for
- `HYPOTHESES.md` — empty stub with four category headings; awaits population by Workflow #1
- `CLAUDE.md`, `README.md`, `.gitignore`, `.mcp.json` — parameterized from research-template
- Full Shapiro-Gentzkow directory tree (`data/`, `source/`, `output/`, `literature/`, `extraction/`, `prisma/`, `datastore/`, `temp/`, `meta-experiments/`, `decisions/`)
- `.claude/workflows/scaffold.mjs` (executed copy) + 13 pipeline workflow stubs (`enumerate-hypotheses.mjs` through `cross-chapter-check.mjs` + `pilot.mjs`) — each throws if invoked before being filled in
- Git initialized, GitHub remote `anup-malani/fertility-explanations-review` created (private), commit `733aba8`, registered in `git-auto-sync.sh` line 41 and `BACKUP-STATUS.md` line 41
- `handoff.md` — next-session context, including design sketch for `enumerate-hypotheses.mjs`
- `decisions/2026-06-06-workflow-schema-discipline.md` — when to use `schema:` on Workflow agents (promoted from this session's failure)
- `/Users/amalani/.claude/workflows/scaffold-fertility-explanations-review.mjs` (original) and `/Users/amalani/.claude/workflows/wire-git-fertility-explanations-review.mjs` (recovery) — user-global workflow scripts

### Methodology

- Plan mode: surveyed scaffolding conventions and a sibling project; asked three AskUserQuestion clarifications (scope, deliverable form, RA capabilities); drafted plan with PROTOCOL.md and RA-PLAYBOOK.md embedded verbatim in 4-backtick fenced blocks so the same file serves as plan AND content source.
- After plan approval: wrote a two-phase `scaffold.mjs` workflow (file scaffolding + git wiring). First run failed in phase 1 because the file-scaffolding agent had a `schema:` constraint and did 12 successful tool calls (most of the file work) but never issued the final `StructuredOutput` call.
- Recovery: confirmed which files made it to disk; wrote remaining static files directly via Write (PROTOCOL.md, RA-PLAYBOOK.md, HYPOTHESES.md, .gitignore, .mcp.json, 13 workflow stubs); wrote a smaller `wire-git-fertility-explanations-review.mjs` workflow for the git+backup wiring (where agent judgment was useful for editing `git-auto-sync.sh` and `BACKUP-STATUS.md` in place); that workflow completed successfully.

### Decisions & Rationale

- **Use `schema:` only where the next workflow stage actually consumes parsed structured output.** Promoted to `decisions/2026-06-06-workflow-schema-discipline.md`. Includes the recovery pattern (when a `schema:`-constrained workflow fails partway, finish deterministic file writes directly and write a smaller focused workflow for the remaining agent-judgment work).
- **Operating principle: every artifact comes from a `Workflow` invocation.** Encoded in `handoff.md` and `PROTOCOL.md` §5 indirectly. RAs invoke workflows; they do not run ad-hoc agent prompts. The 13 pipeline stubs throw on invocation so an RA cannot accidentally run an unimplemented stage.
- **Three target phenomena treated separately** (PM / FDT / SDT) rather than collapsing them into a single "fertility decline" target. User decision in plan-mode AskUserQuestion. Encoded as PROTOCOL.md §2 and the 3×2 verdict table in §4.3. No separate decisions/ file — the methodology document itself is the durable record.
- **Pilot hypothesis = quantity-quality tradeoff.** Chosen because it has both seminal theory (Becker-Lewis 1973) and credible quasi-experimental empirics (Black-Devereux-Salvanes 2005, Angrist-Lavy-Schlosser 2010), exercising every methodological step. Encoded in PROTOCOL.md §7 and handoff.md.
- **Project name = `fertility-explanations-review`.** Sits alongside existing `fertility-evolution`, `fertility-neolithic-dt`, etc. inside `/Users/amalani/github/fertility/`.

### Open Items

- [ ] PI + RAs read and edit PROTOCOL.md and RA-PLAYBOOK.md (Alexandra and Shravan need GitHub access — Anup adds them)
- [ ] OSF pre-registration: Anup uploads PROTOCOL.md, reserves DOI, links it in README.md
- [ ] **Next session: implement `.claude/workflows/enumerate-hypotheses.mjs`** — design sketch and schema rationale are in handoff.md
- [ ] Implement `literature-search.mjs` through `lay-readability-check.mjs` (workflows #2–11), refined iteratively by pilot findings
- [ ] Implement and run `pilot.mjs` on quantity-quality tradeoff
- [ ] Decide whether to edit `.claude/workflows/scaffold.mjs` (in-project copy) to apply the schema lesson before it's reused for a sister project
- [ ] Onboard Alexandra and Shravan: GitHub access, Zotero group library, Slack workspace, OSF account, Claude Code CLI install

---

## [2026-06-10 07:03] — RA onboarding, weekly sync, enumerate-hypotheses.mjs

**Agent:** primary
**Machine:** amalani-macbookpro2022
**Working directory:** /Users/amalani/github/fertility/fertility-review

### Summary

Spans 2026-06-08 through 2026-06-10. Three threads: (1) authored and sent the RA onboarding document to Alexandra Zhou and Shravan Haribalaraman; (2) set up the recurring Saturday 10am sync calendar (June 13 - Aug 15, July 4 skipped, 9 meetings); (3) implemented and ran `enumerate-hypotheses.mjs` (workflow #1), producing a populated and annotated `HYPOTHESES.md` with 65 hypotheses.

### Inputs

- Prior `handoff.md` (renamed to `handoff-2026-06-06.md` this session)
- `PROTOCOL.md` and `RA-PLAYBOOK.md` for onboarding doc structure
- Anup voice guide at `~/.claude/style.md` for voice-critic pass
- Gmail thread "Fertility causes systematic review" for RA email addresses (zhitongz@uchicago.edu, shravanh@uchicago.edu) and confirmation of Saturday 10am

### Outputs

- `RA-ONBOARDING v1.md` / `.docx` and `RA-ONBOARDING v2.md` / `.docx` — onboarding doc, two versions per the global file-versioning convention. v2 expanded "You do" from 5 to 10 jobs (added citation-checking-with-culling, chapter revisions, workflow automator/improver/documenter); toned-down overclaim; added living-guide framing. Committed `b0b2dac`.
- Email sent from amalani@uchicago.edu to Alexandra (cc Shravan) with `RA-ONBOARDING v2.md` attached. Message ID 19ea817c430b8b49.
- Calendar event `uhni8vjlodg47msojg9cdgrd8g` on anup.malani@gmail.com — recurring Saturdays 10-11am CT, 2026-06-13 through 2026-08-15, EXDATE 2026-07-04. Invites sent to both RAs.
- `.claude/workflows/enumerate-hypotheses.mjs` — implemented workflow #1: 4 parallel category-enumerator agents (schema-validated) + merge agent that dedupes cross-category overlaps, sorts, writes `HYPOTHESES.md`. (Note: `.claude/` is gitignored, so this file is not in the repo.)
- `HYPOTHESES.md` — populated with 65 hypotheses (Demographic 11, Economic 21, Biological 12, Cultural 21) with per-entry `**slug** **claim** **why** **phenomena** **seminal** **cross-ref** **notes**` fields. 9 cross-category dedup resolutions and 10 surprising-absence candidates documented in Merge Notes.
- `handoff.md` — current session state.
- `handoff-2026-06-06.md` — preserved prior handoff.
- `temp/apply_explanations.py` — recovery script that extracts cached `StructuredOutput` payloads from agent jsonl transcripts and inserts `**why:**` lines into `HYPOTHESES.md` via regex. Reusable template for future stalled-agent recoveries.
- Commits: `b0b2dac` (onboarding doc), `27b4659` (HYPOTHESES.md + handoff). Pushed to GitHub.

### Methodology

- Used `Workflow` tool four times this session: voice-critic pass on the onboarding doc (revise + voice-fix pipeline), invoked `enumerate-hypotheses.mjs`, and a one-shot inline `annotate-hypotheses` workflow to add `**why:**` glosses to each hypothesis.
- `enumerate-hypotheses.mjs` design: stage 1 fans out 4 parallel agents with a strict JSON schema (slug, name, category, one_sentence_claim, phenomena_relevance, 3-5 seminal_citations, cross_category_flag, notes); stage 2 a single merge agent with no schema that writes the file directly. Each schema-using prompt ends with an explicit "return the StructuredOutput call now" line (lesson from `scaffold.mjs`).
- `annotate-hypotheses` workflow: same per-category fan-out pattern, but the merge stage was asked to apply 65 sequential Edit calls to one file and stalled after ~47 successful edits ("agent stalled on all 6 attempts" after 180s each). Recovered by reading the 4 cached jsonl transcripts, extracting the `StructuredOutput` payloads, and applying the remaining 18 inserts via Python regex.

### Decisions & Rationale

- **Email body sent in HTML; only the `.md` attached (per user override of the global "no .md attachment for non-developers" rule).** Acknowledged user discretion; tactical, not policy-setting. Not promoted.
- **Saturday sync = one recurring event via the claude.ai Google Calendar connector** (which exposes `recurrenceData` with RRULE/EXDATE) rather than 10 separate events via gws-personal MCP (which does not expose recurrence). Tactical, not promoted.
- **`enumerate-hypotheses.mjs` v1 uses training-time knowledge only; no literature-search grounding.** Faster and sufficient for initial enumeration. Completeness critic with grounded search is a separate follow-up workflow. Captured in the workflow file header and handoff.md. Borderline — if we end up adding the completeness critic, the rationale here is the durable record. Not promoting unless we revisit.
- **`HYPOTHESES.md` annotated with `**why:**` plain-English gloss under `**claim:**`.** PI asked for it so the list is easy to scan and reorganize at a higher level. Targeted at smart undergrads with no demography background. Encoded directly in the file; no separate decisions/ file.
- **Workflow recovery pattern: agents doing many small Edits on one file stall.** `[needs promotion]` — this is a reusable lesson that will affect every future multi-edit workflow. Should become `decisions/2026-06-10-batch-edits-via-script-not-agent.md` next session. Pattern: have the agent return all edits as structured data; apply them programmatically in the script body or via one final dedicated Write call.

### Open Items

- [ ] PI review of `HYPOTHESES.md`: cull, add (especially the 10 surprising-absence candidates), decide a higher-level organizing principle on top of the four-category split
- [ ] Fix Cultural-count discrepancy in `HYPOTHESES.md` Merge Notes (says 15, actually 21) — one-line edit
- [ ] PI + RA readability pass on `PROTOCOL.md` and `RA-PLAYBOOK.md` before Saturday's kickoff
- [ ] OSF pre-registration of `PROTOCOL.md` + approved `HYPOTHESES.md`
- [ ] **Promote the batch-edits-via-script lesson** to `decisions/2026-06-10-batch-edits-via-script-not-agent.md`
- [ ] **Revisit `.gitignore`**: `.claude/` is currently gitignored, which means implemented workflow scripts (including `enumerate-hypotheses.mjs`) are not tracked. Reproducibility argues for tracking at least `.claude/workflows/`
- [ ] Implement `literature-search.mjs` (workflow #2): query strings for OpenAlex/Semantic Scholar/Crossref/PubMed, execute, dedupe, write `literature/search-logs/{slug}.json`
- [ ] First RA sync Saturday 2026-06-13 at 10am CT

## [2026-06-13 08:40] — RA setup before kickoff: repo rename, collaborators, repo-native bibliography, comms

Pre-meeting session (before the 10am first RA sync) to clear everything Anup owed Alexandra Zhou and Shravan Haribalaraman. Surfaced the real onboarding thread, which lived in the **UChicago** Gmail account (not personal) — both RAs had already replied with usernames, Zotero emails, and questions that had gone unanswered since Jun 8.

### What changed

- **Repo renamed** `anup-malani/fertility-review` → **`anup-malani/fertility-review-causes`** (GitHub + local dir + git remote). Name chosen by PI. All scaffold/history preserved; old URL auto-redirects.
- **Both RAs added as collaborators** (write): `AlexandraZ27`, `shravanh7472`. Clears Shravan's Jun 10 follow-up ("I don't think I've been added").
- **Repo-name references fixed** in `RA-ONBOARDING v2.md` and `RA-PLAYBOOK.md` (docs had pointed at the never-existent `fertility-explanations-review`); added explicit `git clone` command. Commit `fe1facd`.
- **Bibliography re-architected to repo-native** (PI decision after an options assessment): source of truth is now `datastore/studies.json` (DOI-keyed registry); `literature/bib/*.bib` are generated build artifacts via `make bib`. Added `scripts/make_bib.py`, `Makefile`, `datastore/README.md` (record schema). Zotero demoted to an optional future PDF-sharing layer — **no RA reference-manager account needed to start**. PROTOCOL §7, playbook, onboarding all updated. Commit `ae1f280`. Generator tested end-to-end (empty → graceful; sample study → correct BibTeX).
- **Slack deferred** (PI chose email/iMessage for now). All 7 Slack references across the three docs replaced with email/iMessage + `escalation-log.md`; dedicated channel revisited once pipeline cadence is clear. Commit pushed.
- **Email sent** from `amalani@uchicago.edu`, threaded into the onboarding conversation (msg `19ec33128f31e142`, CC Shravan): confirms GitHub access + answers Shravan's unanswered Jun 8 Claude-Max question.

### Decisions & Rationale

- **AI-tooling funding:** Project funds **Claude Max via monthly gift** (through research stipend); OpenAI/Codex has *no* gift-subscription equivalent (only ChatGPT Business seats, which PI won't manage). RAs may self-fund Codex (Alexandra already bought Codex Pro). Plan: gift Shravan a Max plan immediately (he has no AI sub); Alexandra keeps her Codex and pings when she hits limits — **don't start her monthly Max clock until she actually needs it** (avoid idle burn). Gifted Max bridges until UChicago's Claude contract (~1 month out) provides plans. Email asks both to affirmatively confirm before PI proceeds tomorrow.
- **Bibliography = repo-native, not Zotero:** pipeline finds papers via structured scholarly APIs (OpenAlex/S2/Crossref/PubMed) that already return DOIs+metadata, so the "library" is a machine-maintained registry, not a human-clipped reference manager. Git gives versioning, PR-diffable citation-checking, and direct agent read/write. Zotero kept only as optional PDF convenience. Encoded in `datastore/README.md` + PROTOCOL §7.
- **Email account lesson:** the onboarding thread was in the UChicago account; a personal-only search missed all RA replies. Always check both Gmail accounts for RA/work threads.

### Open Items (this session)

- [ ] Both RAs to **accept GitHub email invites** before they can clone (in their court)
- [x] Shravan confirmed funding plan (message 17, 2026-06-14 03:04 UTC) → gift Max now (TICK-007)
- [ ] Alexandra: Max plan waiting when she hits Codex limits; no action until she reports it
- [ ] Optionally point RAs at `assistants/teaching-assistant/ai-training/` guides; may skip

---

## [2026-06-14] — RA kickoff debrief; ticket system; AGENTS.md

**Agent:** primary
**Machine:** MacBookPro
**Working directory:** /Users/amalani/github/fertility/fertility-review-causes

### Summary

Post-kickoff session. Reviewed the full onboarding email thread (17 messages, UChicago account,
thread 19ea817c430b8b49). Shravan confirmed the funding plan overnight (2026-06-14 03:04 UTC) —
go ahead with Claude Max gift. Alexandra keeps Codex Pro; kickoff went fine. Key outcome from
the meeting: Shravan assigned to design the team collaboration/ticketing system, LLM-agnostic,
using Superpowers as a design aid. Anup confirmed the system must be indifferent to which LLM
the contributor uses.

This session: scaffolded the ticket system (`tickets/`), wrote `AGENTS.md` (LLM-agnostic
context file for any AI opening the repo), updated session log and handoff.

### What changed

- `AGENTS.md` created — root-level AI context file; the file RAs give to Claude or Codex at
  the start of a session to orient the assistant without re-explaining the project
- `tickets/` directory created with README, QUEUE.md, and 10 individual TICK-*.md files
  covering all open items through TICK-010 (pilot run)
- `session-log.md` updated (this entry)
- `handoff.md` updated

### RA kickoff (2026-06-13 10am CT) outcomes

- Meeting was on Shravan's Zoom link; Anup joined from ongoing 9:30 call
- Alexandra shared Superpowers (github.com/obra/superpowers) as a potential framework; Anup
  clarified it solves the planning/methodology problem, not the multi-human coordination problem
- One assignment given: Shravan to design the team coordination/ticketing system (TICK-008),
  with Superpowers as an optional design tool, but the final system must be LLM-agnostic
- Shravan confirmed he'll work Superpowers into the design process (message 15)

### Decisions & Rationale

- **AGENTS.md as the RA-facing AI context file.** Each RA, regardless of which LLM they use,
  gives `AGENTS.md` to their AI at session start. The file is intentionally LLM-agnostic: no
  Claude-specific or Codex-specific instructions. CLAUDE.md stays as the PI's Claude-specific
  configuration; AGENTS.md is the shared, RA-facing layer. Not promoting to decisions/ —
  the file itself is the durable artifact.
- **Ticket system is a proposal, not final.** `tickets/` is a first-draft system that TICK-008
  (Shravan's assignment) should evaluate and improve. The scaffolded system intentionally uses
  only markdown files and git, no external services.

### Pending (moved to tickets/)

All open items are now tracked as tickets in `tickets/QUEUE.md`. See that file for the ordered
work queue.

**Immediate action (today):** TICK-007 — gift Shravan Claude Max.
Shravan also asked whether UChicago Enterprise (~1 month) supports Claude Code CLI — answer is
yes (Enterprise API + OAuth works with Claude Code); confirm to Shravan when gifting.

---

## [2026-06-14 continued] — Ticketing email sent; pilot hypothesis decisions; pre-pilot plan

### Summary

Second block of the June 14 session. Sent the ticketing-system email to RAs, decided the
piloting sequence, switched the pilot hypothesis from Q-Q to old-age security, added the
pre-pilot concept (Anup + Claude on time-cost/income-substitution), and formalized everything
into tickets and a decisions file. Session ends with Anup about to edit HYPOTHESES.md (TICK-001).

### What changed

- **Ticketing email sent** (amalani@uchicago.edu → Alexandra + Shravan, msg 19ec6c59db41f5e6):
  explains the dependency model with an HTML table, names Shravan's TICK-008, previews
  piloting email coming separately.
- **tickets/README.md** rewritten for RA readability: three-file loop, template, escalation,
  and explicit "what this system does not yet solve" section for Shravan.
- **TICK-007 closed** — Anup gifted Shravan Claude Max directly (2026-06-14).
- **TICK-011 created** — Claude drafts root-cause vs proximate-mechanism recategorization of
  all 65 hypotheses; Anup reviews. Blocked by TICK-001.
- **Pilot hypothesis switched** from Q-Q tradeoff (high-complexity) to old-age security /
  pensions (mid-complexity). Updated TICK-009 and TICK-010.
- **TICK-012 created** — pre-pilot: Anup + Claude run full pipeline privately on time-cost /
  income-substitution before RAs see it. Blocked by TICK-001 + TICK-009. TICK-010 (RA pilot)
  now blocked by TICK-012.
- **`decisions/2026-06-14-piloting-sequence.md`** written — formal record of pre-pilot →
  RA pilot → Phase 2 sequence with rationale.
- **`handoff.md`** updated with TODAY section (two-step pickup instruction) and the full
  piloting decision table.
- **Piloting email drafted** (not sent) — awaits TICK-001 completion; Anup will start new
  session to send it and kick off the pre-pilot.

### Decisions & Rationale

- **Q-Q tradeoff dropped as pilot.** Too complex (large literature, many offshoots). Stays
  on the hypothesis list; evaluated in Phase 2.
- **Old-age security / pensions as RA pilot hypothesis.** Mid-complexity: clear theory
  (Caldwell 1976, Neher 1971, Cigno), manageable literature (~30-60 papers), mix of study
  designs, RAs can follow without economics background. Good pedagogical moment: narrow
  (state pensions) vs broad (children as insurance) readings exercises phenomena coding.
- **Time-cost / income-substitution as pre-pilot hypothesis.** Slightly more theoretical;
  Becker 1965 time-allocation + Mincer 1963 female labor supply. Note: overlaps with
  women's opportunity cost / FLFP hypothesis already in HYPOTHESES.md — check after TICK-001
  whether they need to be differentiated or are the same slug.
- **Pre-pilot rationale.** All 11 workflow stubs currently throw on invocation. Implementing
  and debugging them with just Anup + Claude means failures are invisible to RAs. Pre-pilot
  also answers: which pipeline stages require PI judgment vs can be RA-delegated?

### Open items

- [ ] **TICK-001 (in progress):** Anup finishes HYPOTHESES.md edit — goal before noon 2026-06-14
- [ ] **Next session:** implement `literature-search.mjs` (TICK-009) and run pre-pilot on
  time-cost/income-substitution (TICK-012)
- [ ] **Piloting email:** draft ready; send after TICK-001 is committed
- [ ] **TICK-008 (Shravan):** design real-time coordination layer on top of ticket system
- [ ] **TICK-011:** recategorize HYPOTHESES.md by root cause vs proximate mechanism (Claude drafts)
- [ ] **TICK-005:** PI + RA readability pass on PROTOCOL.md and RA-PLAYBOOK.md

**Addendum:** TICK-011 (recategorize HYPOTHESES.md) merged into TICK-001 — they were the
same job (decide structure + re-slot). TICK-001 now has two explicit sub-steps: A = Anup's
decision pass (in progress), B = Claude re-slots once A is committed. TICK-011 closed.

---

## 2026-06-20 22:00 — literature-search.mjs implemented; LLM screening pipeline designed

**Agent:** primary
**Machine:** MacBookPro
**Working directory:** /Users/amalani/github/fertility/fertility-review-causes

### Summary

Implemented `literature-search.mjs` (TICK-009) fully: two-pass workflow (dry-run writes query draft; pass 2 executes searches, deduplicates, writes search log JSON). Ran dry-run on pilot hypothesis `old-age-security-pension-crowdout`. Discovered the initial 3-axis query had an 83% false negative rate on seminal papers and switched to a 2-axis design. Designed and validated an LLM screening prompt (100% recall, 100% precision on 24-paper test set). Decided on a three-stage pipeline (Boolean → iterative LLM calibration → human screen) with a novel iterative Haiku/Sonnet comparison approach to derive routing rules cheaply per hypothesis category. Emailed RAs the training session assignment for tonight; they will bring hand-crafted queries to the 10am meeting on 2026-06-21.

### Inputs

- `HYPOTHESES-v5.md` — hypothesis entry for `old-age-security-pension-crowdout` (C.3.c)
- `literature-search-training.md` — training guide (already committed; context for RA pedagogy decisions)
- OpenAlex API — 200-paper sample from 2-axis query (81,648 total results)
- Gold-standard set of 12 seminal papers (Neher 1971, Nugent 1985, Cigno & Rosati 1996, Boldrin & Jones 2005, Billari & Galasso 2009, Sinn 2004, Fenge & Meier 2005, Ehrlich & Lui 1991, Cigno 1993, Rosenzweig 1988, Zhang & Zhang 2004, Entwisle & Winegarden 1984)

### Outputs

- `.claude/workflows/literature-search.mjs` — fully implemented (810 lines); gitignored; two-pass; Phases 1/2/3; JS dedup in workflow body; Python/Bash API calls per database
- `literature/search-logs/old-age-security-pension-crowdout-query-draft.md` — 2-axis approved query draft with NOT GBD clause; retrieval cap flagged as open; LLM screening layer noted as preferred resolution
- `literature/search-logs/llm-screen-prompt.md` — Sonnet/Haiku screening prompt; validated 12/12 recall, 12/12 precision; causal direction clause is the key discriminating feature
- `literature-search-training.md` — committed (16317e6); RAs emailed to complete tonight
- `handoff.md` — updated with full `calibrate-screen.mjs` implementation spec for next session
- `decisions/2026-06-20-boolean-query-two-axis.md` — promoted decision
- `decisions/2026-06-20-llm-screening-pipeline.md` — promoted decision

### Methodology

**Query calibration:** tested 3-axis query against 12 known seminal papers via OpenAlex API; measured mechanism-term hit rate in titles + reconstructed abstracts. 83% FNR → dropped mechanism axis.

**Discriminating phrase analysis:** pulled 200-paper sample from 2-axis query; classified relevant vs. false positive using heuristic signals; ran bigram/trigram frequency analysis across both groups to find distinguishing features. Found GBD cluster (27% of FPs) but no generalizable positive discriminator. Concluded: LLM layer is required, keyword AND insufficient.

**Prompt validation:** constructed 24-paper test set (12 RELEVANT, 12 NOT_RELEVANT) covering clean cases and hard cases (reversed causal direction papers). Applied screening prompt via agent. 100% performance. Key finding: causal direction clause does the work that no keyword can.

**Iterative calibration design:** derived from observation that Haiku is unreliable on ambiguous abstracts but cheap ($12/81K), while Sonnet is reliable but expensive ($147/81K). Run both on 1K-paper batches; compare divergences; revise prompt; repeat until Haiku FN rate vs. Sonnet < 3% for 2 consecutive batches. Routing rule then applied to full corpus. Estimated total cost per hypothesis: ~$37.

### Decisions & Rationale

- **Mechanism AND dropped from boolean query** — 83% FNR on known seminal papers; empirical papers in this literature avoid mechanism labels in abstracts. Promoted to `decisions/2026-06-20-boolean-query-two-axis.md`.
- **Three-stage pipeline adopted** (Boolean → LLM calibration screen → human screen) — cost asymmetry: FP costs tokens, FN is unrecoverable; LLM layer handles precision so boolean layer can maximize recall. Promoted to `decisions/2026-06-20-llm-screening-pipeline.md`.
- **Iterative 1K-batch calibration** — avoids running $147 Sonnet on full corpus before prompt is optimized; calibration converges in ~5 batches (~$10); derives category-specific routing rule that generalizes across hypotheses in same section. `[needs promotion]` — flag for next session.
- **One calibration per major category** (economic, biological, cultural, proximate; skip frameworks) — abstract structure is homogeneous within a section; routing rule derived from one hypothesis generalizes within the section. `[needs promotion]` — flag for next session.
- **Sonnet as primary model for LLM screen** (not Haiku alone) — causal direction distinction requires nuanced reading of academic prose; Haiku makes confident errors on ambiguous abstracts; $135 difference per hypothesis is justified given permanent cost of false negatives.
- **RA training before tool run** — training guide sent first so RAs draft queries independently; their queries and the tool's serve as mutual benchmarks; envelope of both is the final query. Rationale in `literature-search-training.md`.

### Open Items

- [ ] **2026-06-21 10am:** RA meeting — compare Alexandra's, Shravan's, and tool's queries for `old-age-security-pension-crowdout`; merge to envelope; approve final query
- [ ] **Next session:** build `calibrate-screen.mjs` (full spec in `handoff.md`)
- [ ] **Promote decisions:** iterative 1K-batch calibration + one-per-category reusability plan both need `decisions/` files
- [ ] **Fix `args` injection bug:** `args` global not injected when calling `Workflow({ scriptPath })` from top-level; hardcoded defaults are the current workaround; file against TICK-004 (gitignore/workflow harness)
- [ ] **Flip `dryRun` default** in `literature-search.mjs` to `false` before running pass 2
- [ ] **Run calibration:** batch 1 on `old-age-security-pension-crowdout` after `calibrate-screen.mjs` is built
- [ ] **gbrain save:** gbrain MCP tools unavailable this session; run `/mexit` at next session start to push session to brain
- [ ] **TICK-002, TICK-003, TICK-004, TICK-005:** still open; lower priority than calibration workflow

---

## [2026-06-20 14:44] — Build calibrate-screen.mjs and run batch 1

**Agent:** primary
**Machine:** MacBookPro
**Working directory:** /Users/amalani/github/fertility/fertility-review-causes

### Summary

Built `calibrate-screen.mjs` — the iterative Haiku/Sonnet calibration workflow specified in `handoff.md` — and immediately ran batch 1 on `old-age-security-pension-crowdout`. The workflow fetched 103 papers from OpenAlex (fewer than the target 1,000 — see open items), dual-screened them in parallel 100-paper chunks with Haiku and Sonnet, computed divergence statistics, and wrote a calibration report and routing rule. The stopping criterion (Haiku FN rate < 3%) was met on the first batch: Haiku FN rate = 0%, agreement rate = 81.6%, Sonnet uncertain rate = 17.5%. Four confusion papers (Haiku UNCERTAIN / Sonnet decisive) were diagnosed and three targeted prompt revision suggestions were produced.

### Inputs

- `handoff.md` — full implementation spec for `calibrate-screen.mjs`
- `literature/search-logs/old-age-security-pension-crowdout-query-draft.md` — 2-axis OpenAlex query (text body read; JSON block at bottom is stale 3-axis version)
- `literature/search-logs/llm-screen-prompt.md` — LLM screening prompt validated 2026-06-20
- `.claude/workflows/literature-search.mjs` — pattern reference for schema and Python API call conventions

### Outputs

- `.claude/workflows/calibrate-screen.mjs` — fully implemented (330 lines); inputs: `{ slug, batchNumber, promptPath, haikuModel, sonnetModel }`; Phases: load resources → cursor-paginate OpenAlex → dual-screen in parallel chunk pipelines → divergence analysis (pure JS) → calibration report + optional routing rule
- `literature/search-logs/old-age-security-pension-crowdout-calibration-batch-1.md` — calibration report: 103 papers, 0% FN, 0% FP, 81.6% agreement, 17.5% Sonnet uncertain; stopping criterion MET; 4 confusion cases diagnosed; 3 prompt revision suggestions
- `literature/search-logs/old-age-security-pension-crowdout-routing-rule.md` — routing rule: Haiku primary, ~4% escalation to Sonnet; cost estimate $58.49 for 79,727 papers vs. $191.34 pure Sonnet

### Methodology

**Workflow architecture:** `calibrate-screen.mjs` uses a parallel pipeline: two concurrent `pipeline()` calls (one Haiku, one Sonnet), each processing 100-paper chunks via sub-agents. Pure JS divergence analysis (no agent) computes FN/FP/confusion/agreement rates. A single report-writing agent receives the full annotated divergence lists and generates the markdown report. Routing rule agent fires conditionally only when stopping criterion is met.

**Args injection workaround:** top-level `Workflow({ scriptPath })` does not inject `args` into the child script. Used a thin wrapper workflow that calls `workflow(childPath, args)` to pass `{ slug, batchNumber }` cleanly to the calibration script. Documented as existing TICK-004 issue.

**promptPath default:** set to `literature/search-logs/llm-screen-prompt.md` (the actual file location) rather than the slug-specific `{slug}-llm-screen-prompt.md` from the spec, since the slug-specific file doesn't exist yet. Future hypotheses should write their prompt to `{slug}-llm-screen-prompt.md` and pass that path explicitly.

**OpenAlex query read from text body:** the `### OpenAlex (primary)` code block in the query-draft file (2-axis query, no mechanism AND). The JSON block at the bottom of the same file is stale (3-axis) and was deliberately not used.

### Decisions & Rationale

- **`promptPath` defaults to non-slug path** — `llm-screen-prompt.md` is the actual file; slug-specific naming to be enforced for future hypotheses. `[needs promotion]` — fold into a prompt management decision when multiple hypotheses have their own prompts.
- **Stopping criterion met on batch 1 with only 103 papers** — accept the result but treat it as preliminary; the fetch underdelivered (target 1,000) so the sample is small. Before the full run on 79,727 papers, verify the fetch reliably delivers the full batch size by debugging the cursor pagination. `[needs promotion]` — decision on minimum calibration sample size.

### Open Items

- [ ] **Debug fetch underdelivery:** batch 1 fetch returned 103 papers instead of 1,000. Likely a cursor pagination early-exit in the Python script (network timeout or empty results after one page). Fix before running full screen on 79,727 papers. Run batch 2 with fixed fetch to confirm FN rate holds at 0%.
- [ ] **Apply prompt revisions from calibration report** before full run: three targeted changes to handle missing-abstract papers, birth-outcome framing, and joint child-allowance/pension papers — see `calibration-batch-1.md` §Prompt Revision Suggestions.
- [ ] **Flip `dryRun` default** in `literature-search.mjs` to `false` before running pass 2 on OAS.
- [ ] **Run full LLM screen** (79,727 papers via routing rule) once fetch is debugged and prompt revised.
- [ ] **Promote decisions:** iterative calibration design + one-per-category reusability plan (flagged last session); minimum calibration sample size (flagged this session).
- [ ] **Fix `args` injection** in Workflow harness (TICK-004) — wrapper workaround works but shouldn't be permanent.
- [ ] **gbrain save:** push session notes to brain via `/mexit` at next session start.
- [ ] **TICK-002, TICK-003, TICK-005:** still open, lower priority than full screen run.
