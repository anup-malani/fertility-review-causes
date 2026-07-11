# PROTOCOL — Fertility-Explanations Systematic Review

**Principal Investigator:** Anup Malani
**Research Assistants:** Alexandra ___, Shravan ___
**Status:** Draft v0.1 — pending PI approval, then pre-registration on OSF before any screening begins.

## 1. Aim

To produce the authoritative reference work evaluating, for every major proposed explanation of fertility variation and decline, two questions:

1. **Is the explanation causally credible?** (i.e., is there well-identified evidence that the proposed cause actually affects fertility, and at what effect size)
2. **Is the explanation demographically significant?** (i.e., does the proposed cause account for a meaningful fraction of the observed fertility variation in the period(s) it claims to explain)

These two questions are distinct. An explanation can be causally credible but demographically trivial (real but small), or demographically significant in cross-section but causally unidentified (correlated but unproven).

## 2. Three phenomena to explain

Each hypothesis is evaluated against **three** target phenomena. The same explanation may be significant for one and not another:

- **Pre-modern (PM):** pre-1870 fertility variation across populations and within populations over time, including hunter-gatherer / agriculturalist / pastoralist baselines.
- **First Demographic Transition (FDT):** TFR decline from ~5–7 to ~2.5–3.5 in modernizing societies, roughly 1870–1965 in the West (later elsewhere).
- **Second Demographic Transition (SDT):** TFR decline from ~2.5–3.5 to ~1.3–2.0, roughly 1965–present, OECD then global.

A "verdict" on a hypothesis is therefore a 3-tuple: { significance for PM, significance for FDT, significance for SDT }.

For study-window classification, use replacement status when TFR data are available. A study window
whose first and last available in-window TFR observations are both above 2.1 is FDT-like; both
below 2.1 is SDT-like; an above-to-below crossing is FDT|SDT. If no in-window TFR observation
exists, do not guess from calendar period alone; flag the row for human interpretation. Low-fertility
settings with binding fertility policy, such as China in the one-child / two-child-policy era,
must be flagged for human review. See
`decisions/2026-07-11-tfr-replacement-transition-classification.md`.

## 3. Four categories of explanation

Hypotheses are sorted into one of four categories. Cross-category hypotheses are assigned to the **primary mechanism** with a flagged cross-reference.

- **Demographic** — proximate determinants and population-structure mechanisms (mortality decline, marriage timing, breastfeeding/lactational amenorrhea, contraceptive technology and access, sex ratios, tempo effects).
- **Economic** — relative prices, opportunity costs, and household optimization (quantity-quality tradeoff, female wage growth, child-rearing costs, housing costs, urbanization, pension crowding-out of old-age insurance motive for children, dynastic-capital and Becker-Barro motives, credit constraints).
- **Biological** — physiological capacity and exposure (fecundity changes with age, age at menarche, infectious disease, environmental toxins / endocrine disruptors, nutrition / energy availability, paternal age, ART access).
- **Cultural** — preferences, values, norms, and ideational diffusion (postmaterialism, religiosity decline, individualism, female autonomy / education-as-empowerment, social-network and peer effects, secular ideational change à la Lesthaeghe).

**Cross-category resolution rule:** Assign to the category of the most proximate causal mechanism. Female labor-force participation → Economic (wage channel) with cross-ref to Cultural (norm channel). Child mortality decline → Demographic (replacement) with cross-ref to Economic (q-q tradeoff via reduced expected cost per surviving child).

## 4. Operational definitions

### 4.1 Causal credibility (GRADE-style rating)

We adapt GRADE (used in Cochrane Reviews) for observational and quasi-experimental research:

| Rating | Evidence pattern |
|---|---|
| **High** | Multiple well-identified RCTs or natural experiments converging on a consistent effect size, across multiple settings. |
| **Moderate** | Quasi-experimental designs (IV, DiD, RD, event-study) with credible identification, replicated across ≥2 settings, broadly consistent in direction and magnitude. |
| **Low** | Cross-sectional or panel with controls, no clear identification; or one credible quasi-experiment without replication. |
| **Very low** | Correlational only, mechanism speculative, or evidence pattern inconsistent. |

The rating applies to the **causal claim**, not the existence of the correlation.

### 4.2 Demographic significance

For each hypothesis × phenomenon pair, compute:

- **Decomposition share** — what fraction of the observed TFR change is attributable to the hypothesized cause, using the best available decomposition (Bongaarts proximate determinants for demographic hypotheses; Oaxaca-Blinder for cross-country economic comparisons; Lee-Carter or component-projection for time-series). Reported as a point estimate with bootstrap CI.
- **Slope sufficiency** — given the literature's best estimate of the causal effect size (d fertility / d X), and the observed range of X over the target period, can the effect plausibly produce the observed range of TFR? Sufficient / partial / insufficient.
- **R² benchmarks** — within-country time-series R² and cross-country within-period R² of TFR on X (alone and conditional on standard controls).

A hypothesis is **demographically significant** for a phenomenon if its decomposition share ≥ 10% **or** its slope-sufficiency is "sufficient" **or** its conditional R² ≥ 0.15. The 10% / 0.15 thresholds are conventional; thresholds will be pre-registered on OSF and reported alongside results so readers can apply their own.

### 4.3 Verdict structure (per hypothesis)

| | Causal credibility | Demographic significance |
|---|---|---|
| Pre-modern | (GRADE rating) | (significant / partial / not significant / insufficient data) |
| FDT | (GRADE rating) | (significant / partial / not significant / insufficient data) |
| SDT | (GRADE rating) | (significant / partial / not significant / insufficient data) |

## 5. Methodology pipeline

For each hypothesis, the following stages are executed. **Bold** indicates a human-in-the-loop gate; everything else is AI-executed and AI-verified with RA sample-checking.

1. **Hypothesis approved into the master list (HYPOTHESES.md).** AI proposes candidates per category; PI approves.
2. Search strategy drafted (query strings for OpenAlex, Semantic Scholar, Crossref, plus demography-specific sources: Demographic Research, Pop & Dev Review, Population Studies, Vienna Yearbook, PAA).
3. Literature search and AI screening — two phases (see §5.1 below).
4. **RA title/abstract review** of the union of Phase 1 and Phase 2 RELEVANT papers; target 60–100 papers for full-text retrieval. RA flags each paper for retrieval or exclusion.
5. Full-text retrieval. **RA procures PDFs the AI can't access** (UChicago library proxy, ILL, emailing authors).
6. Full-text screen. **RA spot-checks 5–10%.**
7. Data extraction into structured template (`extraction/{hypothesis-slug}.csv`). **RA verifies a random 10% sample against PDFs.**
8. Risk-of-bias assessment per study (ROBINS-I for observational; RoB 2 for any RCTs).
9. Meta-analysis (R `metafor`) if ≥3 studies with extractable effect sizes; narrative synthesis otherwise.
10. Demographic-significance computation against PM / FDT / SDT using extracted estimates + macro datasets (HFD, WPP, Maddison, Gapminder). For target-period classification, read macro data from source repositories as read-only inputs and store derived outputs in this repo.
11. GRADE rating — judge panel of 3 independent agent raters; **disagreements > 1 level escalate to PI.**
12. Chapter draft using fixed template (Section 6).
13. **RA lay-readability check** — RA reads the chapter and flags any passage that doesn't make sense to a smart undergrad, or any claim that smells overconfident given the cited evidence.
14. PI review and sign-off.

### 5.1 Literature search and AI screening

The search pipeline has two phases with orthogonal recall mechanisms: keyword relevance ranking (Phase 1) and citation network proximity (Phase 2). The two phases together screen approximately 200–600 papers per hypothesis rather than the ~12,000 that a full OpenAlex cursor pull would require.

**Phase 1 — Sequential Saturation Search (`sequential-screen.mjs`)**

Papers are pulled from OpenAlex in batches of 100, ordered by OpenAlex's default relevance ranking (no explicit `sort` parameter). Each batch is screened immediately by Claude Haiku against the hypothesis inclusion criteria. The yield rate — the fraction of each batch that passes as RELEVANT — is tracked across batches.

Stopping rules (first met):
- Yield < 5% for 2 consecutive batches, OR
- 1,000 total papers screened, OR
- OpenAlex cursor exhausted.

Expected output: 20–50 RELEVANT seed papers from approximately 200–400 screened.

Rationale: OpenAlex relevance scores are monotonically decreasing across pages for a given query. Saturation sampling exploits this property to concentrate screening effort on the most relevant portion of the retrieval set rather than screening exhaustively to a hard cursor cap (~6,400 results for `search=` queries).

**Phase 2 — Citation Snowball (`snowball-citations.mjs`)**

Phase 2 expands coverage via the citation network, using the Phase 1 RELEVANT papers as seeds.

- **Phase 2a (backward citations):** All `referenced_works` for every Phase 1 RELEVANT seed are fetched from OpenAlex. Metadata is batch-retrieved and each new paper is Haiku-screened.
- **Phase 2b (forward citations):** For the top 15 Phase 1 seeds ranked by Haiku confidence score, citing papers are fetched in parallel from three sources:
  - OpenAlex: `filter=cites:{openalex_id}`
  - Semantic Scholar: `/graph/v1/paper/{id}/citations`
  - Web of Science (optional, requires `WOS_API_KEY`): `/citing?uniqueId={wos_uid}` — uses the UChicago institutional key.

All papers retrieved in Phase 2 are deduplicated against the Phase 1 corpus before screening. Maximum snowball depth is 2 rounds, consistent with standard practice (Wohlin 2014); round 3 returns less than 5% new material and is not performed. Expected output: 20–50 additional RELEVANT papers.

**PRISMA documentation**

Phase 1 and Phase 2 are tracked separately in the PRISMA flow diagram. Each phase has its own "identified," "screened," "excluded," and "included" counts. The union of Phase 1 RELEVANT and Phase 2 RELEVANT papers forms the input to the RA title/abstract review in step 4 above.

After all chapters are signed off:

15. Cross-chapter contradiction check (workflow scans every chapter for claims that conflict with claims in other chapters).
16. Book compilation (LaTeX).
17. JEL-style summary article (~20k words).

## 6. Chapter template

Every chapter has the same structure:

```
# Chapter [N]: [Hypothesis name]

**Category:** [Demographic / Economic / Biological / Cultural]
**Primary mechanism:** [one-sentence mechanism statement]
**Cross-references:** [other chapters with related mechanisms]

## 1. The claim
[2–4 sentences: precise statement of the causal claim, including direction and units]

## 2. Theoretical mechanism
[½–1 page: how the cause produces fertility change, with citations to the formative theoretical statements]

## 3. Search strategy
[Query strings, databases searched, date range, inclusion/exclusion criteria. Reproducible.]

## 4. PRISMA flow
[Diagram + table: records identified → after deduplication → after title/abstract screen → after full-text screen → included in synthesis]

## 5. Included studies
[Table: author-year, country, period, design, sample, effect-size estimate, RoB rating]

## 6. Quantitative synthesis
[Forest plot if applicable. Pooled effect, heterogeneity (I², τ²), moderator analyses, sensitivity, publication-bias check (funnel + Egger)]

## 7. Demographic significance
### 7.1 Pre-modern
[Decomposition share, slope-sufficiency, R²; verdict]
### 7.2 FDT
[Same]
### 7.3 SDT
[Same]

## 8. GRADE rating
[Per-phenomenon rating with justification]

## 9. Verdict
[The 3×2 verdict table from §4.3]

## 10. Open questions and recommended studies
[What evidence would change the verdict? What study designs would be most informative?]

## 11. References
```

## 7. Tooling

- **Citation management (source of truth):** A repo-native, DOI-keyed registry of screened/included studies at `datastore/studies.json`. The screening and dedup stages write to it; per-hypothesis `.bib` files in `literature/bib/` are **generated** from it via `make bib` (never hand-edited). Because the registry lives in git, the bibliography is versioned, diffable in PRs, and the citation-check happens in code review. Agents (Claude or Codex) read and write the registry directly.
- **Citation management (optional convenience layer):** A Zotero group library may be added later *only* as a shared PDF store with one-click browser capture for the source-procurer role. If used, it exports **into** `literature/bib/`; it is never the system of record.
- **Search APIs:** OpenAlex (free, broad coverage), Semantic Scholar (free, AI-augmented), Crossref. PubMed for biological hypotheses.
- **Meta-analysis:** R with `metafor`. Python `statsmodels` as fallback. AI generates the analysis script; RA verifies sample by re-running.
- **Macro datasets:** Human Fertility Database, UN WPP, Gapminder, Maddison, World Bank WDI. Cached locally in `data/raw/`.
- **Pre-registration:** OSF. Each hypothesis gets a pre-registered protocol entry before screening begins.

## 8. Pre-registration

Before any screening for a given hypothesis begins, the following are locked on OSF:

- Inclusion / exclusion criteria
- Search query strings
- Data extraction template
- Statistical analysis plan (random-effects model, heterogeneity tests, sensitivity analyses, publication-bias diagnostics)
- Demographic-significance thresholds

Deviations from pre-registration are reported in the chapter as "deviations from protocol" with justification.

## 9. Update cadence

Chapters are versioned. The review is a **living document** — when major new evidence is published, the relevant chapter is updated and the version log records the change. Annual full-corpus search rerun.
