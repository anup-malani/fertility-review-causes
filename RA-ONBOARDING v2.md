# RA Onboarding -- Fertility-Explanations Systematic Review

**To:** Alexandra and Shravan
**From:** Anup Malani
**Date:** 2026-06-08

This document explains what we are doing, what I will do, what Claude (the AI) will do, and what you will do. Read it once front-to-back. Then read `PROTOCOL.md` (the methodology spec) and `RA-PLAYBOOK.md` (your operating manual) in the same repo.

You don't need to know demography to start. You will pick it up by working on it. What I need from you is what undergraduates in econ and math at Chicago are already trained to do: read carefully, notice when something doesn't add up, and tell me when it doesn't.

**This is a living guide.** The project is new, the workflows are not yet stable, and our division of labor will change as we learn what works. Expect revisions. When you notice the doc has drifted from how we actually operate, tell me, or edit it and send a PR.

## 1. What this project is

Why has fertility fallen? Economists, demographers, biologists, and sociologists have proposed dozens of explanations. Female wages rose, child mortality fell, contraception spread, religion declined, secular individualism rose, endocrine disruptors accumulated, and so on. Most of these explanations are taught as if settled. Few have been evaluated against each other on the same evidentiary footing.

We are doing that evaluation. For each major proposed explanation, we ask two questions:

1. **Is it causally credible?** Is there well-identified evidence that the proposed cause actually moves fertility?
2. **Is it demographically significant?** Even if real, does it account for a meaningful fraction of the fertility change we actually observe?

These questions are distinct. A cause can be real but tiny. A cause can be a large correlate without being established as causal. We rate every hypothesis on both, against three target phenomena:

- **Pre-modern** fertility variation (pre-1870, including hunter-gatherer baselines)
- **First Demographic Transition** (~1870-1965: TFR falls from ~6 to ~2.5 in modernizing societies)
- **Second Demographic Transition** (~1965-present: TFR falls from ~2.5 to ~1.5)

The atomic unit is a chapter per hypothesis. Chapters become parts of an online wiki we maintain as a living reference, and individual chapters or clusters of them may also be submitted as standalone papers.

The model is a **Cochrane systematic review**, the standard in medicine. We are applying that standard to a question that economics and demography have argued about more than measured.

## 2. Why this project matters

Two reasons:

1. **Policy.** Most rich countries are below replacement fertility. Governments are spending billions on pronatalist policy without knowing which proposed causes are real. If the dominant cause is housing costs, you build housing. If it is shifting cultural norms, housing won't help. Comparative evaluation of the candidate causes is missing, and we want to supply some of it.
2. **Method.** A transparent, AI-assisted systematic review of a contested social-science question is itself an experiment in how to do this kind of work. We will learn whether the approach scales. If it does, that is useful to know. If it doesn't, that is also useful to know.

On the career side: you will graduate having co-authored a substantive piece of work with a senior PI and having become genuinely skilled with Claude Code. How that skill pays off is uncertain. The skill itself is real.

## 3. What you will learn

You will leave this project competent in three things:

- **Demography.** Total fertility rates, parity progression, Bongaarts proximate determinants, Lee-Carter decomposition. You'll learn it as we go; you don't need it on day one.
- **Systematic-review methodology.** PRISMA flow, GRADE ratings, risk-of-bias assessment, random-effects meta-analysis. You'll do these.
- **Claude Code as a research tool.** You'll write and run multi-agent workflows that fan out tasks, verify each other, and produce auditable output. This is well beyond using ChatGPT for homework.

## 4. Who does what

The methodology pipeline has 14 stages (see `PROTOCOL.md` §5). Here is who owns each.

### I do

- Approve the master hypothesis list before any work begins.
- Set inclusion / exclusion criteria for each hypothesis and lock them on OSF (pre-registration).
- Resolve every escalation you flag.
- Review and sign off on every chapter.
- Hold the final responsibility for the work and its public claims.

### Claude does

- Propose candidate hypotheses for me to approve.
- Draft and execute literature searches across OpenAlex, Semantic Scholar, Crossref, and PubMed.
- Title/abstract screen every paper against the pre-registered criteria.
- Extract data from included PDFs into structured templates.
- Run risk-of-bias assessments and meta-analyses (via R `metafor`).
- Compute demographic-significance numbers against the macro datasets.
- Generate GRADE ratings (via a 3-rater agent panel; they have to agree within one level or it escalates to me).
- Draft the chapter following our template.

### You do

You have several jobs. Listed roughly by how often you do them:

1. **Pipeline operator (daily-to-weekly).** You invoke the workflows. The workflows live in `.claude/workflows/`. Your job is to make sure each stage runs to completion, the output looks reasonable, and the next stage can begin. You don't need to understand the statistics to do this. You need to notice when something looks wrong.

2. **Sanity validator (every chapter draft).** After Claude produces a chapter, you read it as a smart Chicago undergrad would. Flag anything that doesn't make sense, sounds overconfident given the cited evidence, uses jargon without explaining it, cites a paper whose title doesn't match the claim, or includes a number that wasn't extracted from the included studies. This is the most important thing you do. AI is a fluent and confident liar; you are the check.

3. **Citation checker (every chapter draft).** Independently verify every non-trivial citation and **cull the hallucinated ones before they reach me**. Spin up a separate Claude agent, or use a different LLM, and confirm three things for each cite: the paper exists, the paper actually says what we claim, and the claim is consistent with the paper's title and abstract. Cross-model verification catches errors that a single model will repeat back to you. Don't pass me a chapter with a fake citation in it. If you can't verify a cite, remove the claim or replace the cite. If a chapter would lose a load-bearing claim by culling, flag it and I'll decide.

4. **Source procurer (as needed).** When Claude flags a PDF it can't get, you get it. UChicago library proxy first, then ILL, then emailing authors. Drop the PDF in `literature/pdfs/{hypothesis-slug}/`.

5. **Chapter reviser (after PI review).** After I review a chapter, you apply the requested revisions. Not just spot-checking. Actual editing: rewriting paragraphs, recomputing tables, re-running a meta-analysis with a corrected inclusion list, updating figures. Push the revised chapter back for a second pass.

6. **Workflow automator (ongoing).** Where a workflow runs on a predictable cadence or in response to a predictable trigger, automate it. Cron jobs, `/loop`, scheduled remote agents, file-watchers. Don't ask me to manually kick off something that a trigger could handle. Every automated job must notify on each run, success or failure.

7. **Workflow improver (ongoing).** When a workflow fails, runs slowly, or produces bad output, propose a fix and send a PR. Treat the workflow scripts as research artifacts that themselves need iteration. A broken workflow that no one fixes is a tax on the rest of the pipeline.

8. **Workflow documenter (ongoing).** Maintain a living `WORKFLOWS.md` (or equivalent) that documents, for each workflow: what it does, how it's invoked, what the inputs and outputs look like, the common failure modes, and the recovery pattern when it breaks. A new RA should be able to read this and run the pipeline without asking either of us.

9. **Methodology meta-experimenter (~monthly).** We need to know which AI tools work best for which stages. About once a month I'll ask you to compare our pipeline against Elicit, Consensus, Scite, or another candidate on a single hypothesis. Write up findings as a short note in `meta-experiments/`. These may become a paper of their own.

10. **Quality auditor (continuous).** Maintain `escalation-log.md`. Every flagged issue, who handled it, what the resolution was. Audit trail for the project.

The full description of these roles, escalation rules, and the list of things that commonly go wrong is in `RA-PLAYBOOK.md`. Read it.

## 5. What gets escalated to me

Don't try to resolve these. Flag them and I take it:

- Suspected hallucinated citation (paper that may not exist).
- Two extraction agents disagree on a number by more than 20%.
- Effect direction conflicts with theory or with most prior studies.
- A hypothesis ends up with fewer than 5 included studies after full-text screen.
- GRADE rating panel disagrees by more than one level.
- You read a chapter and can't follow the argument.
- Any deviation from the pre-registered protocol.

Channel: email me with `[FERT-REVIEW]` in the subject (iMessage for anything urgent); mirror the flag in `escalation-log.md`. We'll stand up a dedicated channel once the pipeline is running and we see what cadence we actually need.

## 6. Where we are right now

The repository is scaffolded. `PROTOCOL.md`, `RA-PLAYBOOK.md`, and 13 stub workflow files exist. The hypothesis list (`HYPOTHESES.md`) is empty. That is the next thing to populate.

**Next workflow to implement:** `enumerate-hypotheses.mjs`. Four parallel agents (one per category: demographic, economic, biological, cultural) propose candidate hypotheses. I review the draft list and approve. Then we lock the protocol on OSF, and we begin.

You don't run this one. I do, because the design questions are still open. Once `HYPOTHESES.md` is approved, you will pilot the full pipeline on **one** hypothesis (likely the quantity-quality tradeoff in the economic category) before we scale.

## 7. Setup checklist

Before our first sync:

- [ ] Send me the GitHub username you want added to `anup-malani/fertility-review-causes` (private repo). Once I've added you and you've accepted the email invite, clone it:
  ```
  git clone https://github.com/anup-malani/fertility-review-causes.git
  ```
- [ ] (No reference-manager account needed to start.) The bibliography is repo-native — source of truth is `datastore/studies.json`, and `.bib` files are generated with `make bib`. If we later add a shared Zotero group for PDF sharing, I'll ask for your account email then.
- [ ] Confirm you have UChicago library proxy access (sign into the library website remotely; if it works, you're set).
- [ ] Create an OSF account (osf.io) with your UChicago email.
- [ ] Install **both** the Claude Code CLI and the Claude desktop app on your laptop. I'll send my own user guides separately. Read those before our first sync rather than waiting for me to walk you through it.
- [ ] Read `PROTOCOL.md` and `RA-PLAYBOOK.md` in this repo.

## 8. Cadence

- **Monday:** 30-min sync. Status, escalations, plan for the week.
- **Wed/Thu:** async check-in by email/iMessage. Blocked on anything?
- **Friday:** end-of-week summary by email, mirrored to `session-log.md`.

## 9. Things to keep in mind

- This is novel work. Some workflows will fail the first time. That is expected. We learn what works by trying things and writing down what broke.
- I would rather you flag five things that turn out to be fine than miss one real problem. Over-escalating is free; under-escalating costs us credibility.
- When you are not sure whether something is in your job or mine, ask. The rule of thumb: any judgment that affects what the published chapter claims is mine. Anything operational is yours.
- You are not expected to know demography on day one. You are expected to learn it on the job and ask when you don't follow something.

## 10. Status of this document

This onboarding doc is version-controlled and will be revised as the project evolves. The role list in §4, the escalation rules in §5, and the cadence in §8 are the most likely to change. If something here contradicts how we actually operate, the operation wins and the doc is wrong. Tell me, or fix it and send a PR.
