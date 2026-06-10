# Handoff — fertility-explanations-review

**Last session:** 2026-06-10 (started 2026-06-08)
**PI:** Anup Malani
**RAs:** Alexandra Zhou (zhitongz@uchicago.edu), Shravan Haribalaraman (shravanh@uchicago.edu)
**Repo:** https://github.com/anup-malani/fertility-explanations-review (private)
**Prior handoff:** [`handoff-2026-06-06.md`](./handoff-2026-06-06.md)

## What this project is

Cochrane-style systematic review of every major proposed explanation for fertility decline. Each hypothesis sorted into one of four categories (Demographic, Economic, Biological, Cultural) and evaluated against three phenomena (Pre-modern, FDT, SDT). Per hypothesis we produce a per-phenomenon GRADE rating of **causal credibility** and a **demographic-significance** verdict. Chapter per hypothesis is the atomic unit; chapters feed an online wiki and may be submitted as standalone papers.

Methodology spec: [`PROTOCOL.md`](./PROTOCOL.md). RA operating manual: [`RA-PLAYBOOK.md`](./RA-PLAYBOOK.md). RA onboarding: [`RA-ONBOARDING v2.md`](./RA-ONBOARDING%20v2.md).

## Operating principle

Every artifact comes from a `Workflow` invocation. Workflows live in `.claude/workflows/`. `scaffold.mjs` and `enumerate-hypotheses.mjs` are implemented; the other 12 are stubs that throw on invocation.

## State at handoff

### Done this session

- **RA onboarding doc** authored (`RA-ONBOARDING v1.md`, then `RA-ONBOARDING v2.md` with PI revisions: expanded "You do" from 5 to 10 jobs, including citation-checking with culling, chapter revisions, workflow automation/improvement/documentation; toned-down overclaim; living-guide framing). Committed (b0b2dac). Sent to both RAs from amalani@uchicago.edu with the .md attached.
- **Saturday weekly sync** set up. One recurring event on anup.malani@gmail.com, Saturdays 10-11am CT, 2026-06-13 through 2026-08-15, July 4 excluded. 9 total meetings. Invites sent to both RAs. Event ID `uhni8vjlodg47msojg9cdgrd8g`.
- **`enumerate-hypotheses.mjs` implemented** (workflow #1). 4 parallel category-enumerator agents (schema-validated structured output) → merge agent that dedupes cross-category overlaps, sorts, writes `HYPOTHESES.md`. Per-stage lessons from scaffold.mjs baked in (explicit "return StructuredOutput now" instruction; merge stage has no schema, verifies by reading filesystem).
- **`enumerate-hypotheses.mjs` invoked.** 75 hypotheses proposed across 4 categories → 65 in the final file after the merge agent's dedup pass (the merge agent's self-reported count of 60 was a misreport; actual count is 65: Demographic 11, Economic 21, Biological 12, Cultural 21). 9 cross-category resolutions documented in the file's Merge Notes section. 10 surprising absences flagged for PI consideration (war/conscription, famine, climate shocks, state capacity, epidemics as shocks distinct from chronic STI burden, air pollution distinct from endocrine disruptors, religious-pronatalist subgroups, LGBTQ family formation, migration, polygyny).
- **Annotated `HYPOTHESES.md`** with a plain-English `**why:**` mechanism gloss (2-3 sentences) under each entry's `**claim:**`. Targeted at smart undergrads with no demography background, to make the list easy to scan and reorganize. Recovery story below.

### Done in prior session (2026-06-06)

- Project scaffolded at `/Users/amalani/github/fertility/fertility-review/` (note: repo name on disk is `fertility-review`, not `fertility-explanations-review`)
- Shapiro-Gentzkow directory tree
- `PROTOCOL.md`, `RA-PLAYBOOK.md`, `HYPOTHESES.md` stub, `CLAUDE.md`, `README.md`, `.gitignore`, `.mcp.json`
- `.claude/workflows/scaffold.mjs` (executed) + 13 stubbed pipeline workflows
- `git init`, initial commit (733aba8), private GitHub remote, auto-sync registration

### Pending (in order)

1. **PI review of `HYPOTHESES.md`.** Cull, add (especially the 10 surprising-absence candidates), reorganize. PI mentioned wanting a higher-level organizing principle on top of the four-category split (e.g., proximate-determinants vs. preference-shifters vs. constraint-relaxers, or supply-vs-demand, or PM-only vs. FDT vs. SDT). When the principle is chosen, the file can be resorted/tagged.
2. **Fix the Cultural-count discrepancy** in `HYPOTHESES.md` Merge Notes (says 15, actually 21). One-line edit.
3. **PI + RA readability pass on PROTOCOL.md and RA-PLAYBOOK.md.** Edit, commit, share with Alexandra and Shravan ahead of Saturday's kickoff.
4. **OSF pre-registration of `PROTOCOL.md` + approved `HYPOTHESES.md`.** Anup does this manually; reserve DOI; link back into `README.md`.
5. **Implement `literature-search.mjs`** (workflow #2). Take an approved hypothesis (likely quantity-quality tradeoff as the pilot), generate search query strings for OpenAlex, Semantic Scholar, Crossref, PubMed; execute searches; dedupe; write `literature/search-logs/{slug}.json`. Anup runs first; once stable RAs run.
6. **Implement workflows #3-13** iteratively, refined by pilot findings.
7. **Run `pilot.mjs`** end-to-end on quantity-quality tradeoff. Calibration before scaling.

## Saturday kickoff (2026-06-13)

First sync. Agenda probably: review onboarding doc questions, walk RAs through the repo, demonstrate one workflow invocation, set per-RA first-week assignments (likely: Alexandra reads PROTOCOL.md and Cultural hypotheses, Shravan reads PROTOCOL.md and Economic hypotheses; both flag confusion and missing hypotheses).

Both RAs replied to confirm Sat 10am. Calendar invite sent.

## Recovery patterns observed

### `enumerate-hypotheses.mjs`

Ran end-to-end without intervention. The merge agent's count self-report disagreed with the actual file contents (60 vs. 65, Cultural 15 vs. 21). Lesson: when an agent both writes a file and reports counts, the counts can drift from what was written. Always verify by reading the file, not by trusting the agent's summary.

### `annotate-hypotheses` (one-shot inline workflow, not saved as a script)

4 parallel category agents drafted plain-English `why:` glosses for their categories' hypotheses (StructuredOutput schema). Merge agent was supposed to apply 65 Edit calls to `HYPOTHESES.md`. The merge agent **stalled** after ~47 successful Edits — workflow harness reported "agent stalled on all 6 attempts (no progress for 180000ms each)".

Recovery: extracted the cached StructuredOutput payloads from the 4 per-category agents' jsonl transcripts in `~/.claude/projects/.../subagents/workflows/wf_98a3d40d-3d4/`, applied the remaining 18 inserts via a Python regex pass (`temp/apply_explanations.py`). Total inserted: 47 (by the agent before stall) + 18 (by Python) = 65.

**Lesson for future workflows:** agents doing many small Edit calls on the same file are fragile. Better pattern: have the agent return all edits as structured data, then apply them programmatically in the workflow script body (or via a final dedicated "write" agent that does ONE Write call with the fully reconstructed file). Don't ask one agent to do 60+ sequential Edits.

## Pointers to known artifacts

- Prior handoff (initial scaffold session): `handoff-2026-06-06.md`
- Plan that generated the project: `/Users/amalani/.claude/plans/cozy-growing-crab.md`
- Implemented workflows:
  - `.claude/workflows/scaffold.mjs`
  - `.claude/workflows/enumerate-hypotheses.mjs`
- Stub workflows (throw on invocation; implement before running):
  - `literature-search.mjs`, `screen-titles-abstracts.mjs`, `acquire-pdfs.mjs`, `extract-data.mjs`, `risk-of-bias.mjs`, `meta-analyze.mjs`, `demographic-significance.mjs`, `grade-rating.mjs`, `synthesize-chapter.mjs`, `lay-readability-check.mjs`, `cross-chapter-check.mjs`, `pilot.mjs`
- Recovered scaffold workflow (user-global): `/Users/amalani/.claude/workflows/scaffold-fertility-explanations-review.mjs`
- Recovered git-wiring workflow: `/Users/amalani/.claude/workflows/wire-git-fertility-explanations-review.mjs`
- Research-template canonical files: `/Users/amalani/github/research-template/`
- Sibling project (structural reference): `/Users/amalani/github/fertility/fertility-evolution/`
- Annotation-apply script (one-off, may be useful as a template for future recovery): `temp/apply_explanations.py`

## Quick start for next session

```
1. cd /Users/amalani/github/fertility/fertility-review
2. Open this handoff.md
3. Skim HYPOTHESES.md in Obsidian; decide cull/add/reorganize
4. (If Saturday) run the RA kickoff
5. Next workflow to implement: literature-search.mjs
   - Take one approved hypothesis as input
   - Generate query strings for OpenAlex, Semantic Scholar, Crossref, PubMed
   - Execute searches via their APIs
   - Dedupe by DOI/title
   - Write literature/search-logs/{slug}.json
```
