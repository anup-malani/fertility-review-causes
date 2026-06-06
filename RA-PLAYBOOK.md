# RA Playbook — Fertility-Explanations Systematic Review

This is your operating manual. Read it once front-to-back; refer back when in doubt. The companion document is `PROTOCOL.md`, which describes the methodology. This document describes **your job**.

## Roles

You have five jobs. They are listed by frequency:

### A. Pipeline operator (daily-to-weekly)
You run the workflows. For each hypothesis we work on, you execute the pipeline stages from `PROTOCOL.md` §5 in order. The workflows are saved under `.claude/workflows/` — invoke them via Claude Code. You don't need to understand the statistics; you need to make sure each stage runs to completion, the output looks reasonable, and the next stage can begin.

### B. Sanity validator (every chapter draft)
After the AI produces a chapter, you read it as a smart undergraduate would. Flag anything that:
- Doesn't make sense to you (you can't follow the argument)
- Sounds overconfident given the cited evidence
- Uses jargon without explaining it
- Contradicts something in an adjacent chapter
- Cites a paper whose title doesn't match the claim it's being used to support
- Includes a number (effect size, p-value, sample size) that wasn't extracted from the included studies

Use the escalation log (Section "Escalation rules" below) for anything you flag.

### C. Source procurer (as needed)
The AI can't always get the PDF it needs. When the pipeline flags a missing source, you procure it:
1. Try the UChicago library proxy first (your UChicago login + the library website).
2. If not there, request via Interlibrary Loan (UChicago library website → ILL).
3. If still not there, email the author directly (template in `meta-experiments/source-procurement/`).
4. Last resort: archive.org, Internet Archive Scholar.

Drop retrieved PDFs in `literature/pdfs/{hypothesis-slug}/` with filename `{first-author}-{year}-{short-title}.pdf`.

### D. Methodology meta-experimenter (~monthly)
We need to know which AI tools work best for which stages. You run small comparison experiments:
- Pick a single hypothesis we've already screened.
- Run the title/abstract screen using Elicit, Consensus, Scite, or another candidate.
- Compare against our AI agent's output and the human gold standard.
- Write up findings as a short note in `meta-experiments/`.

Anup will tell you which tools and which stages to test, but you drive the comparisons.

### E. Quality auditor (continuous)
You maintain the `escalation-log.md` — a running list of issues flagged, who handled them, and the resolution.

## Escalation rules

These conditions trigger an escalation to Anup. Don't try to resolve these yourself:

| Condition | Why it matters |
|---|---|
| Suspected hallucinated citation | The AI sometimes invents papers. If a citation can't be verified in OpenAlex / Google Scholar, flag it. |
| Two extraction agents disagree on a numeric value by > 20% | One of them is wrong. We need to know which. |
| Effect direction conflicts with theory or with most prior studies | May be a real anomaly or an extraction error. Either way, PI looks. |
| Chapter has fewer than 5 included studies after full-text screen | Hypothesis may be underpowered for meta-analysis; need PI call on whether to proceed narratively or drop. |
| GRADE rating panel disagrees by more than 1 level | The rating is unstable; PI breaks tie. |
| Lay-readability check: you can't follow the argument | Either the writing is bad or the reasoning is muddled. PI decides. |
| Pre-registration deviation needed | Any change to the locked search strategy, inclusion criteria, or analysis plan goes to PI before execution. |

Escalation channel: Slack to Anup with `[FERT-REVIEW]` prefix; mirror in `escalation-log.md` in the repo.

## Tooling setup

You need accounts/access to:

- GitHub access to `anup-malani/fertility-explanations-review` (Anup will add you)
- Zotero account, joined to group library `fertility-explanations-review`
- UChicago library proxy (your UChicago login)
- Claude Code CLI installed locally (Anup will help)
- OSF account for pre-registration entries
- Slack workspace `fertility-review` (Anup will set up)

Optional (try as part of meta-experiments):
- Elicit, Consensus, Scite (free tiers)
- Connected Papers
- ResearchRabbit

## Weekly cadence

- **Monday:** 30-min sync with Anup. Status of in-progress hypotheses, escalations from the past week, plan for the week.
- **Wed/Thu:** mid-week check-in (async, Slack). Anything blocked?
- **Friday:** end-of-week summary — what shipped, what's escalated, what's blocked. Posted to Slack and appended to `session-log.md`.

## A non-exhaustive list of things that go wrong (so you know what to look for)

- The AI makes up a paper title that sounds plausible but doesn't exist.
- The AI extracts a "TFR" value that's actually a CBR (or vice versa).
- The AI confuses pre-modern (PM) and FDT in a chapter that should clearly distinguish them.
- The AI applies a search query string that misses the foundational paper everyone in the field knows.
- The AI's GRADE rating reads "Moderate" but the cited studies are all cross-sectional with no identification.
- A chapter cites a paper for a finding that the paper, when you actually read it, doesn't make.
- A forest plot is generated but the included-studies table doesn't match the studies in the plot.

If you see any of these — escalate. The whole point of the review is to be reliable, and reliability requires catching these.
