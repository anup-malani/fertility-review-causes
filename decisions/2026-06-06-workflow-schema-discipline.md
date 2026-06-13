# Decision: When to use `schema:` on `Workflow` agents

**Date:** 2026-06-06
**Author:** Anup Malani (PI) + Claude Code session
**Status:** Active — applies to every workflow script written for this project
**Review date:** 2026-12-06 (revisit after the first 5–10 production workflows have run)

## Context

The project is built on `Workflow`-tool fan-out. Workflow's `agent()` call accepts an optional `schema:` parameter that forces the spawned subagent to call `StructuredOutput` at the end of its turn, returning a validated JSON object instead of free text. The temptation is to use `schema:` everywhere — it feels like safer engineering and gives downstream code structured data without parsing.

In practice (see `scaffold.mjs`, first run, wf_ce133085-352), this caused a hard workflow failure. The scaffold-files agent did 12 successful tool calls (real work — directories created, CLAUDE.md and README.md written) but never issued the final `StructuredOutput` call, and the workflow runtime tore down with `Error: agent({schema}): subagent completed without calling StructuredOutput (after 2 in-conversation nudges)`. All work produced before the timeout was kept on disk, but the workflow's resume cache holds only successful agent calls — so `resumeFromRunId` would have re-run the failed call from scratch.

## Options

1. **`schema:` everywhere.** Maximally defensive — every workflow stage produces structured data, no parsing in the script body.
2. **`schema:` only where the next stage needs parsed data.** Use schemas at workflow boundaries where output feeds a merge step, a filter, a fan-out, or a structured write. Skip the schema when verification can be done by reading the filesystem (or by reading the agent's free-text return directly).
3. **No `schema:` ever.** Always parse free-text returns in the script body. Maximally flexible — but loses validation, retries on malformed output, and any guardrail against the agent forgetting to return data at all.

## Decision

**Option 2** — use `schema:` only when the next stage actually consumes parsed structured output.

Concretely:
- **Use `schema:`** on the per-category enumeration agents in `enumerate-hypotheses.mjs` (the merge step needs typed records), on the two-rater screening agents (the reconciliation step compares records by field), on the data-extraction agents (the agreement check is numeric), on the GRADE rater panel (majority vote).
- **Skip `schema:`** on the chapter-synthesis agent (output is a markdown file written to disk — verification is "did the file get written"), on the lay-readability check (output is a list of flagged passages, readable as plain text), on the scaffold/wire agents (verification is filesystem state via `ls`/`grep`).
- **When a schema is used, end the agent prompt with an explicit final-call instruction:** "After completing the work, immediately call the StructuredOutput tool with your result. Do not summarize, do not narrate — just call the tool." Models sometimes finish the work and forget the structured-output call without this nudge.

## Rationale

The failure mode is specifically that the agent finishes the substantive work (sometimes a long sequence of tool calls) and then exits the turn without producing the structured output. The runtime gives two in-conversation nudges and then hard-fails. The harder the substantive work, the more likely the agent loses track of the schema obligation.

When the schema is consumed downstream, this risk is worth accepting because the alternative (parsing free text) is worse — the agent might omit fields, use inconsistent units, or wrap the data in unparseable prose. But when the schema is *not* consumed (e.g., verification can be done by reading the resulting file), the schema buys nothing and risks total workflow failure.

## Risks

- **Drift:** RAs writing new workflows will be tempted to copy the `schema:` pattern blindly. Mitigate by including a one-line comment in every workflow stub: `// schema: <yes — needed for merge step> // schema: <no — verification by filesystem>`.
- **Free-text parsing fragility:** Schema-less agents can still produce inconsistent output. Mitigate by checking the filesystem state directly rather than parsing the return — if the agent claims success but the file isn't on disk, the workflow should fail explicitly with its own error, not silently accept the claim.

## Pattern: how to recover when a `schema:` workflow fails

If a workflow with `schema:` fails after partial work:

1. **Check the filesystem.** Most deterministic file-writing work is already done — don't re-run it.
2. **Finish the deterministic part directly** with Write/Edit. Don't relaunch the workflow just for purity.
3. **For the remaining agent-judgment parts**, write a smaller focused workflow that does only the missing work. This is how `scaffold.mjs` was recovered: split into static-file writes (done directly via Write) + `wire-git-fertility-explanations-review.mjs` (small workflow for git wiring where agent judgment was useful).
4. **Update the original workflow script** to remove the schema constraint that caused the failure, so a re-run by the next person doesn't repeat the mistake. (Or convert it to a checklist agent without schema — verification by filesystem.)

The recovered scaffold workflow remains in the project (`.claude/workflows/scaffold.mjs`) as a reproducibility record, but it should be edited to apply the lesson before any sister project is scaffolded from it.
