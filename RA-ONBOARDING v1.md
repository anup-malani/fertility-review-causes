# RA Onboarding — Fertility-Explanations Systematic Review

**To:** Alexandra and Shravan
**From:** Anup Malani
**Date:** 2026-06-08

Welcome. This document explains what we are doing, why it matters, what I will do, what Claude (the AI) will do, and what you will do. Read it once front-to-back. Then read `PROTOCOL.md` (the methodology spec) and `RA-PLAYBOOK.md` (your operating manual) in the same repo.

You don't need to know demography to start. You will pick it up by working on it. What I need from you is what undergraduates in econ and math at Chicago are already trained to do well: read carefully, notice when something doesn't add up, and tell me when it doesn't.

## 1. What this project is

Why has fertility fallen? Economists, demographers, biologists, and sociologists have proposed dozens of explanations — female wages rose, child mortality fell, contraception spread, religion declined, secular individualism rose, endocrine disruptors accumulated, and so on. Most of these explanations are taught as if they were settled. Few have been evaluated against each other on the same evidentiary footing.

We are doing that evaluation. For each major proposed explanation, we ask two questions:

1. **Is it causally credible?** Is there well-identified evidence that the proposed cause actually moves fertility?
2. **Is it demographically significant?** Even if real, does it account for a meaningful fraction of the fertility change we actually observe?

These questions are distinct. A cause can be real but tiny. A cause can be a large correlate but unproven as causal. We will rate every hypothesis on both, against three target phenomena:

- **Pre-modern** fertility variation (pre-1870, including hunter-gatherer baselines)
- **First Demographic Transition** (~1870–1965: TFR falls from ~6 to ~2.5 in modernizing societies)
- **Second Demographic Transition** (~1965–present: TFR falls from ~2.5 to ~1.5)

The atomic unit is a chapter per hypothesis. Chapters become parts of an online wiki we maintain as a living reference work, and individual chapters or clusters of them may also be submitted as standalone papers.

The model is a **Cochrane systematic review** — the gold standard in medicine. We are bringing that standard to a question that economics and demography have so far argued about more than measured.

## 2. Why this project matters

Three reasons:

1. **Policy.** Most rich countries are below replacement fertility. Governments are spending billions on pronatalist policy without knowing which proposed causes are real. If the dominant cause is housing costs, you build housing. If it is shifting cultural norms, housing won't help. The honest answer to "which is it" requires the kind of comparative evaluation no one has done.
2. **Method.** A rigorous, transparent, AI-assisted systematic review of a contested social-science question is a research artifact in itself. Done well, this is a template other fields will copy.
3. **Career.** You will graduate having co-authored a major work with a senior PI and having become genuinely skilled with Claude Code. That skill will compound over time — how much, and in what direction, no one knows yet, but the floor is high and the ceiling is open.

## 3. What you will learn

You will leave this project fluent in three things:

- **Demography.** Total fertility rates, parity progression, Bongaarts proximate determinants, Lee-Carter decomposition. You'll learn it as we go; you don't need it on day one.
- **Systematic-review methodology.** PRISMA flow, GRADE ratings, risk-of-bias assessment, random-effects meta-analysis. You'll do these.
- **Claude Code as a research tool.** Not "ChatGPT for homework" — you'll learn to write and run multi-agent workflows that fan out tasks, verify each other, and produce auditable output. This is the part of your training that will compound the most.

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
- Generate GRADE ratings (via a 3-rater agent panel — they have to agree within one level or it escalates to me).
- Draft the chapter following our template.

### You do

You have five jobs. Listed by how often you do them:

1. **Pipeline operator (daily-to-weekly).** You invoke the workflows. The workflows live in `.claude/workflows/`. Your job is to make sure each stage runs to completion, the output looks reasonable, and the next stage can begin. You don't need to understand the statistics to do this — you need to notice when something looks wrong.

2. **Sanity validator (every chapter draft).** After Claude produces a chapter, you read it as a smart Chicago undergrad would. You flag anything that doesn't make sense, sounds overconfident given the cited evidence, uses jargon without explaining it, cites a paper whose title doesn't match the claim, or includes a number that wasn't extracted from the included studies. This is the most important thing you do. AI is a fluent and confident liar; you are the check.

3. **Source procurer (as needed).** When Claude flags a PDF it can't get, you get it — UChicago library proxy first, then ILL, then emailing authors. Drop the PDF in `literature/pdfs/{hypothesis-slug}/`.

4. **Methodology meta-experimenter (~monthly).** We need to know which AI tools work best for which stages. About once a month I'll ask you to compare our pipeline against Elicit, Consensus, Scite, or another candidate on a single hypothesis. You write up findings as a short note in `meta-experiments/`. These notes may become a paper of their own.

5. **Quality auditor (continuous).** You maintain `escalation-log.md` — every flagged issue, who handled it, what the resolution was. Audit trail for the project.

The full description of these roles, escalation rules, and the list of things that commonly go wrong is in `RA-PLAYBOOK.md`. Read it.

## 5. What gets escalated to me

Don't try to resolve these — flag them and I take it:

- Suspected hallucinated citation (paper that may not exist).
- Two extraction agents disagree on a number by more than 20%.
- Effect direction conflicts with theory or with most prior studies.
- A hypothesis ends up with fewer than 5 included studies after full-text screen.
- GRADE rating panel disagrees by more than one level.
- You read a chapter and can't follow the argument.
- Any deviation from the pre-registered protocol.

Channel: Slack to me with `[FERT-REVIEW]` prefix; mirror the flag in `escalation-log.md`.

## 6. Where we are right now

The repository is scaffolded. `PROTOCOL.md`, `RA-PLAYBOOK.md`, and 13 stub workflow files exist. The hypothesis list (`HYPOTHESES.md`) is empty — that is the next thing to populate.

**Next workflow to implement:** `enumerate-hypotheses.mjs`. Four parallel agents (one per category — demographic, economic, biological, cultural) propose candidate hypotheses. I review the draft list and approve. Then we lock the protocol on OSF, and we begin.

You don't run this one — I do, because the design questions are still open. Once `HYPOTHESES.md` is approved, you will pilot the full pipeline on **one** hypothesis (likely the quantity-quality tradeoff in the economic category) before we scale.

## 7. Setup checklist

Before our first sync:

- [ ] Send me the GitHub username you want added to `anup-malani/fertility-explanations-review` (private repo).
- [ ] Create a Zotero account and send me the email — I'll add you to the group library.
- [ ] Confirm you have UChicago library proxy access (sign into the library website remotely; if it works, you're set).
- [ ] Create an OSF account (osf.io) with your UChicago email.
- [ ] Install **both** the Claude Code CLI and the Claude desktop app on your laptop. I'll send my own user guides separately — read those before our first sync rather than waiting for me to walk you through it.
- [ ] Read `PROTOCOL.md` and `RA-PLAYBOOK.md` in this repo.

## 8. Cadence

- **Monday:** 30-min sync. Status, escalations, plan for the week.
- **Wed/Thu:** async check-in on Slack. Blocked on anything?
- **Friday:** end-of-week summary in Slack, mirrored to `session-log.md`.

## 9. Things to keep in mind

- This is novel work. Some of the workflows will fail the first time. That is expected. The way we learn what works is by trying things and writing down what broke.
- I would rather you flag five things that turn out to be fine than miss one real problem. Over-escalating is free; under-escalating costs us credibility.
- When you are not sure whether something is in your job or mine: ask. The rule of thumb is that any judgment that affects what the published chapter claims is mine. Anything operational is yours.
- You are not expected to know demography on day one. You are expected to learn it on the job and ask when you don't follow something.

Welcome aboard.
