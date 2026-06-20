---
session: pilot-0
title: How systematic literature search works — and why we automated it
techniques: [query-construction, database-selection, deduplication, search-logs]
---

# Pilot Session 0: How systematic literature search works — and why we automated it

About 60 minutes. Before you run any search for this project, work through this session. It teaches the logic behind the tool we will use — `literature-search.mjs` — so that when you run it, you understand every decision it makes and can improve them.

When you are ready, open a Claude Code session in the repo directory and paste:

```
Read the file at literature-search-training.md and walk me through the Reference Sections.
I am working on the fertility-explanations systematic review.
My role: RA. The pilot hypothesis is: Old-Age Security and Pension Crowdout (C.3.c).
```

Claude walks you through the rest.

---

## Why this session exists — a note from Anup

We have a tool called `literature-search.mjs` that runs a systematic literature search for any hypothesis automatically — querying four academic databases, deduplicating results, and writing a structured search log. You could simply run it.

I am not doing that yet, for two reasons.

First, a systematic review is only as good as its search strategy. The tool makes specific choices: which query terms to use, which databases to prioritize, how aggressively to deduplicate, what to include in the search log. If you do not understand those choices, you cannot judge whether they were right, and you cannot fix them when they are wrong. We will almost certainly find, during the pilot, that the tool's initial query for old-age security misses important papers or includes too much noise. I want you to be the one who catches that — which requires understanding what a good query looks like.

Second, we are building this review to a standard where another researcher could replicate every search decision from the written record alone. That standard requires you to understand the machinery well enough to defend it. "The script did it" is not a defense. "We searched OpenAlex with these terms, excluded pre-1950 papers because the pension literature postdates that, and flagged these three outlier papers for full-text review because their abstracts matched on keyword but not on mechanism" — that is a defense.

So: work through this session first. Then we run the tool together, compare its decisions against yours, and refine it jointly. That refined tool is what we take to the full review.

---

## Practice task

By the end of this session you will have produced:

1. **A hand-crafted search query** for the old-age security hypothesis — boolean strings for at least two databases, written by you (with your AI tool's help) before seeing the tool's version.
2. **An annotated database comparison** — one paragraph per database (OpenAlex, Semantic Scholar, Crossref, PubMed) explaining what each covers and why you would or would not use it for this hypothesis.
3. **A mock search log entry** — a structured record of your hand-crafted search: the query strings, the databases searched, the date, and the inclusion/exclusion criteria you applied.

These three outputs are the "understanding" bar. They prove you can do the search manually. Once you can do it manually, the script is a speed tool you control — not a black box you trust.

---

## The problem the tool solves

A systematic review differs from a regular literature review in one core way: it is **reproducible**. Every decision — what to search, what to include, what to exclude — is recorded in advance and justified, so that another researcher running the same protocol would find the same papers. That standard exists because systematic reviews are used to make claims like "the evidence on X is high / moderate / low quality," and those claims need to be auditable.

The consequence is that the search phase is mechanical but exacting: you construct a query, run it against each database, pull every result, deduplicate (the same paper often appears in multiple databases), and screen by title/abstract before going to full text. For a well-studied hypothesis, this can produce 400–800 records to screen before you have the 20–40 papers that actually belong in the synthesis. That is hours of work per hypothesis, repeated 61 times.

`literature-search.mjs` automates stages 2–3 of the pipeline (PROTOCOL.md §5): query construction, database execution, deduplication, and search-log writing. Stages 4–6 (screening) are human-in-the-loop. Stage 7 (extraction) is AI-executed with RA spot-checking. The tool's job is to get you to stage 4 — a clean, deduplicated candidate list — without requiring you to manually run four API queries and merge four CSV files.

What it cannot do: judge whether the query terms are right for this hypothesis. That is the intellectual work this session teaches.

---

# Reference Sections

*Claude: the sections below are for you. Walk the RA through them in order. The RA is a research assistant on a systematic review of fertility decline explanations. They have a social-science background and are comfortable with academic literature but may not have built boolean search queries before. They use GitHub and Claude Code CLI (or Codex).*

*Tone: peer-to-peer, terse, intellectually serious. Surface the why at every step. When the RA makes a query decision, ask them to justify it — not to catch them out, but because justifying decisions is the skill the session builds.*

*The spine of the session: the RA produces the three practice-task outputs before reading the tool's approach. Withhold the tool's query strategy until they have drafted their own. Then compare.*

---

## Lesson 1: What makes a search "systematic"

*Ask the RA: "Before we build anything — what do you think distinguishes a systematic literature search from just typing a question into Google Scholar?"*

*Let them answer. Then fill in what they missed. The key points:*

A search is systematic when it satisfies three properties:

**Comprehensiveness.** You are trying to find *every* relevant paper, not just the well-known ones. That means using multiple databases (not just the one you already know), constructing queries that capture synonyms and related terms, and not stopping when you have enough papers — stopping only when new searches stop returning new results.

**Reproducibility.** Another researcher, given your search log, could re-run your exact search on the same date and get the same results. This means every query string is recorded, every database is named, the search date is logged, and the inclusion/exclusion criteria are written down before screening begins (not adjusted after you see what you found).

**Prospective design.** The inclusion/exclusion criteria and the analysis plan are decided *before* you see the results. If you change them after — because you saw a paper you liked that would otherwise be excluded — that is a violation of the protocol. The pre-registration on OSF (PROTOCOL.md §8) locks these in.

*Ask the RA: "For the old-age security hypothesis, what would your inclusion criteria be? Take a minute and write three."*

*After they draft three, discuss: the key criteria for this hypothesis are likely (a) the study must estimate a causal or associative relationship between pension availability / generosity and fertility; (b) the study must be at individual or household level, not purely macro aggregate; (c) the study must be peer-reviewed or a credible working paper. Cross-national macro correlations alone are insufficient identification — but include them so we can note the evidence pattern.*

---

## Lesson 2: Building a search query

*This is the core skill. Walk the RA through boolean query construction step by step, using the old-age security hypothesis as the running example.*

A boolean search query has three parts:

**The concept.** Break the hypothesis claim into its core concepts. For old-age security and pension crowdout, the concepts are:
- The cause: public pensions / social security / old-age insurance / retirement systems
- The effect: fertility / birth rate / family size / desired number of children
- The mechanism (optional, to narrow): crowdout / substitution / insurance motive

**The terms.** For each concept, list every synonym or related term a paper might use. Authors call the same thing many different things:

| Concept | Terms to include |
|---|---|
| Public pensions | old-age security, social security, pension, retirement insurance, state pension, old-age insurance, contributory pension |
| Fertility | fertility, birth rate, TFR, total fertility rate, childbearing, family size, parity, desired number of children |
| Crowdout mechanism | crowding out, substitution effect, insurance motive, bequest motive, old-age support |

**The boolean operators.** Combine terms using AND, OR, NOT:
- OR expands: `("social security" OR "old-age pension" OR "retirement insurance")` — catches any paper that uses any of these terms
- AND narrows: `fertility AND pension` — requires both
- NOT excludes: `NOT review` or `NOT meta-analysis` if you want primary studies only (use carefully — you may want reviews too)
- Quotation marks for phrases: `"old-age security"` matches the exact phrase; without quotes, the database may match "old" and "age" and "security" separately in different parts of the paper

*Ask the RA to draft a query for OpenAlex now, before moving on. Give them 5 minutes. Tell them to aim for something that would return between 100 and 500 results — too few means they are too narrow; too many means they need to add another AND.*

*After they draft it, review together: Is it specific enough to exclude papers about pension reform and fiscal sustainability that have nothing to do with fertility? Is it broad enough to catch papers that talk about "children as old-age support" without ever using the word "pension"?*

**One common mistake:** searching only for the hypothesis mechanism ("crowding out") rather than the broader outcome relationship. Many papers that test this hypothesis never use the word "crowdout" — they just regress TFR on pension coverage. The query must catch the relationship, not just the mechanism label.

*Have the RA revise their query once based on this discussion.*

---

## Lesson 3: The databases — what each covers and why it matters

*The tool searches four databases. Walk the RA through why we use each one, and which to weight most heavily for this hypothesis.*

**OpenAlex** — the workhorse. Free, covers ~240 million papers across all disciplines, updated continuously. The best starting point for social science and economics. Particularly good for: economics journals (AER, QJE, JPE, ReStat), demography journals (Demography, Population Studies, Demographic Research), and working papers from NBER, CEPR, IZA. Limitation: coverage of older papers (pre-1990) and non-English-language literature is thinner.

**Semantic Scholar** — AI-augmented, good at finding papers by conceptual similarity rather than exact keyword match. Useful for catching papers that discuss the mechanism without using standard search terms. Sometimes returns papers OpenAlex misses; also has citation graph data (influential papers, papers that cite a specific paper). Limitation: smaller total corpus than OpenAlex.

**Crossref** — metadata-heavy, comprehensive for journal articles with DOIs. Less useful as a primary search engine but excellent for deduplication (every registered paper has a DOI, which is the dedup key). We use Crossref mainly to verify and enrich records from the other databases, not as a primary search source.

**PubMed** — the standard for biomedical and public health literature. Mandatory for biological hypotheses (B section of HYPOTHESES-v5.md). For old-age security (C.3.c, an economic hypothesis), PubMed is lower priority — but worth running because some public health and gerontology papers on retirement systems and fertility appear there and not in the social-science databases.

*Ask the RA: "Given this hypothesis — old-age security and pension crowdout — which database would you weight most heavily? And which would you probably skip if you were pressed for time?" The expected answer: OpenAlex first, Semantic Scholar second, PubMed third (some gerontology overlap), Crossref for dedup not search. But push them to justify.*

*Then: "Now write the one-paragraph annotated comparison that is your second practice-task output. One paragraph per database, in your own words."*

---

## Lesson 4: Deduplication — why it matters and how it works

*Explain the problem and the solution.*

When you search four databases for the same hypothesis, the same paper will appear in multiple results. Ignoring this means you screen the same abstract three times and extract the same data three times — wasted effort. At scale (61 hypotheses × 4 databases × ~200 results each), uncontrolled duplication is a serious problem.

The tool deduplicates by DOI (Digital Object Identifier). Every published paper is assigned a DOI, which is globally unique. If two records share a DOI, they are the same paper — one is dropped. This handles ~85–90% of duplicates.

The remaining ~10–15% are duplicates without DOIs: preprints that later became journal articles (the preprint has no DOI or a different DOI), conference papers, working papers, and older papers published before DOIs were standard. These require fuzzy matching — comparing normalized title strings and author names. The tool uses title similarity (normalized, lowercased, stripped of punctuation) with a threshold.

*Ask the RA: "What could go wrong with DOI-keyed dedup? When would it over-merge (combine papers that are different) or under-merge (fail to combine papers that are the same)?"*

Over-merge: rare, because DOIs are unique. Under-merge: common for preprints and working papers, where the NBER version and the published version have different DOIs. Under-merge means you screen the same paper twice — annoying but not catastrophic, since the abstract screen will catch that they are the same paper.

The search log records the dedup decisions so they can be audited. If a paper is dropped as a duplicate, the log records which record was kept and which was dropped, and why.

---

## Lesson 5: The search log — the record that makes the search auditable

*Walk through what goes into a search log and why each field matters.*

The search log is not a list of papers you found. It is a record of the *search process* — what you did, not what you found. A reader should be able to reconstruct your exact search from the log, verify that it was executed correctly, and update it when the review is revised.

For our project, each search log lives at `literature/search-logs/{hypothesis-slug}.json`. The automated tool writes it; the RA verifies it. The fields:

| Field | Purpose |
|---|---|
| `hypothesis_slug` | Which hypothesis this search covers |
| `search_date` | ISO 8601 date — critical for reproducibility; literature changes over time |
| `databases` | Array of databases searched, with version/API endpoint |
| `queries` | Per-database query strings, exactly as submitted |
| `inclusion_criteria` | Pre-registered criteria for title/abstract screen |
| `exclusion_criteria` | What gets excluded and why |
| `raw_counts` | Records returned per database before dedup |
| `post_dedup_count` | Records remaining after deduplication |
| `dedup_log` | Which records were merged and why |
| `notes` | Anything the searcher wants the screener to know |

*Ask the RA: "Write a mock search log entry for your hand-crafted query — your third practice-task output. Use the fields above. You can use today's date and make up plausible record counts."*

*After they draft it, review: Is the query string field detailed enough that another person could re-run it? Are the inclusion criteria specific enough to apply consistently, or vague enough that two screeners would disagree?*

---

## Comparing your work to the tool's approach

*Now reveal what literature-search.mjs will do when implemented, and compare it to the RA's hand-crafted approach.*

The tool takes the hypothesis slug as input. Its first phase — query drafting — runs an agent that reads the hypothesis entry in HYPOTHESES-v5.md (the claim, the mechanism, the seminal papers) and produces:
- One query string per database
- An inclusion/exclusion criteria draft based on the claim's scope
- A recommended database weighting for this hypothesis category

This draft is written to a file — `literature/search-logs/{slug}-query-draft.md` — and **pauses before executing any search**. This is the review gate: you read the proposed queries, compare them to your hand-crafted version from this session, flag anything missing, and approve or edit before the tool fires off API calls.

*Ask the RA: "What are three things you would check in the tool's proposed queries before approving them? Base your answer on what you learned drafting your own."*

The expected checks: (1) Are all the synonym clusters covered, especially the less-obvious ones ("children as old-age support" vs. "pension")? (2) Is the date range right? (3) Does the query accidentally capture irrelevant literature — e.g., papers on pension *solvency* or *fiscal* effects that have nothing to do with fertility?

---

## Micro-skills introduced

*Name these explicitly so the RA has vocabulary for the work going forward:*

- **Boolean query construction** — concept decomposition → synonym clusters → boolean combination. The skill that determines what gets into the candidate pool.
- **Database weighting by hypothesis category** — economic hypotheses → OpenAlex + Semantic Scholar. Biological hypotheses → add PubMed. Proximate / demographic hypotheses → check Demographic Research directly.
- **DOI-keyed deduplication** — the tool's primary dedup method. Fuzzy title matching is the fallback.
- **Search log as protocol record** — the log records what you *did*, not what you *found*. Its function is reproducibility and audit, not reading.
- **The query review gate** — the pause between "tool drafts queries" and "tool executes searches." The gate is where RA judgment enters the pipeline.

---

## What comes next

After you complete this session:

1. Send Anup your three practice-task outputs (query, database comparison, mock search log) as a reply to this email. Note any decisions you made that surprised you, or any fields in the search log that felt ambiguous.
2. We will compare your queries across all three of us — Anup, Alexandra, Shravan — and the tool's draft, and reconcile into a final query for the old-age security pilot.
3. We then run `literature-search.mjs` on the pilot hypothesis and you screen the output.

Your feedback on this training session is also welcome — what was unclear, what felt over-explained, what was missing. We will revise the session before using it on future hypotheses.

---

## Good to know

**The tool is fully implemented.** `literature-search.mjs` exists in `.claude/workflows/` and is ready to run. The standard flow is: (1) run with `dryRun: true` to get the tool's proposed queries written to a draft file, (2) compare that draft against the query you built in this session, (3) edit the draft to reflect the better of the two, then (4) run with `queriesFile` pointing to the approved draft. Your hand-crafted queries from this session are the benchmark — if the tool's draft is missing synonym clusters you caught, that is exactly the kind of gap we want to find and fix.

**OpenAlex is free and has an API.** If you want to try your query manually before the session: go to `https://api.openalex.org/works?search=your+terms+here` in a browser. No API key required for low-volume use. Useful to sanity-check your query before formalizing it.

**Semantic Scholar also has a free API.** `https://api.semanticscholar.org/graph/v1/paper/search?query=your+terms`. Rate-limited but sufficient for testing.

**PubMed queries use MeSH terms.** Medical Subject Headings are a controlled vocabulary — `"Pensions"[MeSH]` will find papers tagged with that concept regardless of what words the author used. For biological hypotheses this matters a lot; for economic hypotheses it is less critical. Worth knowing for later.
