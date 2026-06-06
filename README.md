# Fertility-Explanations Systematic Review

A Cochrane-style systematic review evaluating every major proposed explanation for fertility decline (demographic, economic, biological, cultural) against three target phenomena: pre-modern fertility variation, the First Demographic Transition (~1870–1965), and the Second Demographic Transition (~1965–present). Each hypothesis receives a per-phenomenon GRADE rating of causal credibility and a demographic-significance verdict, synthesized into a per-hypothesis chapter following PROTOCOL.md §6.

**Coauthors:** Solo-PI (Anup Malani); Alexandra ___ (RA, U. Chicago); Shravan ___ (RA, U. Chicago)

## Project documents

Start here before doing anything else in this repo:

- **PROTOCOL.md** — methodology spec. Defines the aim, the three target phenomena, the four hypothesis categories, the GRADE-style causal-credibility rating, the demographic-significance computation, the 14-stage pipeline, and the chapter template. Shareable with external readers and RAs.
- **RA-PLAYBOOK.md** — RA-specific roles, escalation rules, tooling setup, weekly cadence. Read once front-to-back; refer back when in doubt.
- **HYPOTHESES.md** — the master hypothesis list. Populated by `.claude/workflows/enumerate-hypotheses.mjs` and PI-approved before any subsequent workflow runs.
- **.claude/workflows/** — the 13 pipeline workflows (enumeration → literature search → screening → acquisition → extraction → risk-of-bias → meta-analysis → demographic significance → GRADE rating → chapter synthesis → readability check → cross-chapter check, plus the end-to-end `pilot.mjs`).

## Repository Structure

```
├── data/                 Raw data and documentation (immutable)
│   ├── raw/              Original, unmodified data files
│   └── docs/             Codebooks, data dictionaries
│
├── source/               All authored code and manuscript files
│   ├── build/            Data cleaning and construction scripts
│   ├── analysis/         Analysis scripts
│   ├── lib/              Shared functions, packages, requirements
│   └── paper/            LaTeX/LyX manuscript source
│
├── output/               All generated files (reproducible from source/)
│   ├── chapters/         One .md per hypothesis
│   ├── tables/           Generated tables
│   ├── figures/          Generated figures
│   └── paper/            Compiled manuscript
│
├── literature/           Papers, historical sources, reference materials
│   ├── bib/              BibTeX, Zotero export
│   ├── pdfs/             Downloaded PDFs
│   └── search-logs/      Per-hypothesis search query logs
│
├── extraction/           Per-study extraction databases
├── prisma/               PRISMA flow diagrams and screening logs
├── datastore/            Large files, symlinked (not version controlled)
├── temp/                 Intermediate files (not version controlled)
├── meta-experiments/     RA methodology comparison findings
└── .claude/
    ├── skills/           Project skills
    └── workflows/        Saved workflow scripts
```

## Setup

1. Clone the repository.
2. Create a symlink for large data files:
   ```
   ln -s /path/to/shared/storage datastore
   ```
3. Install dependencies listed in `source/lib/`.
4. Run the build system from the project root to reproduce all outputs from raw data.

## Conventions

Raw data in `data/raw/` is immutable. Never modify original data files; all transformations belong in `source/build/` with outputs written to `output/data/`.

All results in `output/` should be reproducible from `source/` and `data/` via a single build command. No manual steps between raw data and final output.
