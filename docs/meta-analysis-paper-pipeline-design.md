# Meta-Analysis-to-Paper Pipeline Design

**Status:** draft for PI/RA review  
**Created:** 2026-07-03  
**Pilot hypothesis:** old-age-security / pension crowdout of fertility  
**Reference corpus:** `literature/reference-corpus/README.md`

## 1. Goal

Build a reproducible pipeline that turns a GACS search output, RA-reviewed papers, and retrieved
PDFs into a chapter/paper that combines:

- **JEL-style economics synthesis:** mechanism-first theory, economic interpretation, heterogeneity,
  external validity, and policy relevance.
- **Cochrane-style review procedure:** explicit eligibility criteria, PRISMA accounting,
  full-text screen, risk-of-bias assessment, structured extraction, GRADE-style certainty language,
  and transparent summary-of-findings tables.

The output should be usable as one hypothesis chapter and, when strong enough, as the core of a
standalone review paper.

## 2. Design Principles

1. **Audit trail before prose.** Every claim in the paper must trace to a structured row in an
   extraction table, a risk-of-bias judgment, a meta-analysis output, or a named theory source.
2. **Theory and empirical evidence are routed separately.** Theory papers support the mechanism and
   intellectual genealogy. Empirical papers support effect estimates, GRADE judgments, and
   demographic significance.
3. **Do not force pooling.** If estimates are not commensurable, the pipeline produces a structured
   narrative synthesis and a harvest plot/evidence map rather than a misleading pooled estimate.
4. **Economics-facing interpretation is explicit.** Meta-analysis outputs are translated into
   economically interpretable units, heterogeneous-margin explanations, and slope-sufficiency
   calculations against observed fertility changes.
5. **External validity is coded, not buried.** Each study records the setting features that govern
   whether an internally credible estimate transports to PM, FDT, or SDT contexts.
6. **Human gates are narrow and logged.** RA and PI judgments should occur at full-text inclusion,
   extraction verification, risk-of-bias disputes, effect harmonization choices, and GRADE disputes.

## 3. Inputs

| Input | Path | Producer | Notes |
|---|---|---|---|
| Clean DOI list | `output/{slug}-metaanalysis-doi-list.md` | GACS Phase E | Deduped distinct-study list; authoritative paper identity set. |
| RA review sheet | `output/{slug}-ra-review.csv` | `source/build/goldset/30_make_ra_review_csv.py` | RA marks `RETRIEVE`, `EXCLUDE`, or `UNSURE`. |
| Unresolved audit | `output/{slug}-unresolved-audit.csv` | `source/build/goldset/30_make_ra_review_csv.py` | Identity verification queue; not normal review input. |
| PDF want-list | `output/{slug}-pdf-wantlist.md` | GACS PDF acquisition steps | Lists residual PDFs requiring manual retrieval. |
| Retrieved PDFs | `literature/pdfs/{slug}/` | RA/source procurer | Named by `paperId` and short title where possible. |
| Search method | `literature/search-logs/canonical-search-workflow.md` | Team synthesis | Describes GACS methodology and recall accounting. |
| Extraction schema | `extraction/schema.md` | This design | Defines one row per estimate. |
| Theory-source table | `extraction/{slug}-theory-sources.csv` | Canon/gold-set stage + RA review | Canonical theory and mechanism papers for the JEL-style section; kept separate from empirical synthesis. |
| Reference corpus | `literature/reference-corpus/` | RA/Codex | JEL and Cochrane exemplars for structure and style. |

## 4. Outputs

| Output | Path | Purpose |
|---|---|---|
| Full-text screen | `extraction/{slug}-fulltext-screen.csv` | Record inclusion/exclusion after PDFs. |
| Extraction table | `extraction/{slug}-effects.csv` | One row per usable estimate or contrast. |
| Study table | `extraction/{slug}-studies.csv` | One row per included study. |
| Theory-source table | `extraction/{slug}-theory-sources.csv` | Canonical theory, intellectual genealogy, and mechanism sources. |
| Risk-of-bias table | `extraction/{slug}-risk-of-bias.csv` | ROBINS-I style domain judgments. |
| Harmonized effects | `output/tables/{slug}-harmonized-effects.csv` | Estimates converted to target units with assumptions. |
| Meta-analysis outputs | `output/tables/{slug}-meta-analysis-summary.csv`, `output/figures/{slug}-forest-*.pdf` | Pooled or grouped evidence. |
| PRISMA flow | `prisma/{slug}-flow.md`, `output/figures/{slug}-prisma.pdf` | Search/screen/retrieval/full-text accounting. |
| Summary of findings | `output/tables/{slug}-summary-of-findings.csv` | Cochrane/GRADE-style certainty table. |
| Demographic significance | `output/tables/{slug}-demographic-significance.csv` | PM/FDT/SDT slope-sufficiency and share calculations. |
| Chapter draft | `output/chapters/{slug}.md` | Hybrid JEL/Cochrane chapter. |

## 5. Pipeline Stages

### Stage 1: RA Title/Abstract Decision Intake

Read `output/{slug}-ra-review.csv` and keep only rows marked `RETRIEVE`. Rows marked `UNSURE`
are held in a PI/second-RA queue. Rows marked `EXCLUDE` remain in the audit trail and never enter
full-text retrieval unless PI overrides.

Acceptance checks:
- All `RETRIEVE` rows have DOI, title, authors, and score rationale.
- No `UNRESOLVED` DOI-trust records are mixed into the normal retrieval queue.
- Every decision has either a valid label or is flagged as incomplete.

### Stage 2: PDF Retrieval Reconciliation

Compare `RETRIEVE` rows against files in `literature/pdfs/{slug}/`. Create a retrieval status table:

- `PDF_AVAILABLE`: file exists and opens.
- `NEEDS_MANUAL`: no PDF yet; use DOI/UChicago proxy/Scholar/ILL.
- `IDENTITY_PROBLEM`: DOI/title mismatch, bad file, or unresolved audit item.

This stage should never silently drop a missing PDF. It writes a revised want-list if new manual
downloads are required after RA review.

### Stage 3: Full-Text Screen

Screen each retrieved full text against pre-specified criteria:

- Population/context relevant to the target hypothesis.
- Cause/intervention/exposure matches the mechanism.
- Fertility or fertility-adjacent outcome is measured, or the paper belongs only in the theory stream.
- Design has extractable causal or descriptive evidence.
- Duplicate/version status is resolved.

Output one row per full-text paper with decision `INCLUDE_EMPIRICAL`, `INCLUDE_THEORY`,
`EXCLUDE`, or `UNSURE_PI`.

### Stage 4: Theory Stream Construction

Build a separate theory-source table before or alongside empirical extraction. The theory stream
should include canonical fertility economics, old-age-security, wealth-flows, intergenerational
transfer, PAYG/social-security, and child-as-asset models. These sources are not counted as
empirical studies and do not enter effect-size synthesis.

The theory-source table should record:

- Bibliographic identity and DOI/title-key status.
- Whether the source is foundational theory, formal model, conceptual mechanism, or
  empirical-classic background.
- The mechanism role it plays in the chapter.
- Whether a full text has been retrieved and whether the source has been RA-verified.

The chapter uses this table for the JEL-style mechanism and intellectual-genealogy section.

### Stage 5: Structured Empirical Extraction

Create two linked tables:

- Study-level table: bibliographic identity, country, period, population, intervention/exposure,
  design, data source, and notes.
- Estimate-level table: one row per effect estimate, with original units, standard error or
  confidence interval, outcome definition, model specification, and extraction location.

Every numeric extraction must include source page/table/figure and a confidence flag.

For human verification, generate reviewer-facing copies with adjacent columns for each
characteristic:

```text
{characteristic}, {characteristic}_ra_decision, {characteristic}_ra_notes
```

Blank RA decision cells mean approved. Reviewers only mark fields that are wrong, ambiguous, or
should be excluded. This keeps human review fast while preserving field-level accountability.

### Stage 6: Risk of Bias

Use a ROBINS-I-inspired table for observational/quasi-experimental work:

- Confounding
- Selection into study
- Classification of intervention/exposure
- Deviations from intended intervention
- Missing data
- Outcome measurement
- Selection of reported result
- Identification credibility

Domain judgments are `low`, `moderate`, `serious`, `critical`, or `no information`, plus a short
rationale. Identification credibility is an economics-specific extension used to bridge ROBINS-I
with quasi-experimental designs.

### Stage 7: External Validity and Transportability

Code setting features that determine whether each internally credible estimate transports to PM,
FDT, and SDT contexts:

- Income level and welfare-state baseline.
- Pre-reform old-age support norms and family-transfer dependence.
- Baseline fertility and baseline pension coverage.
- Treatment margin, including whether the shock is new coverage, benefit generosity, eligibility,
  long-term care insurance, or financial-market substitution.
- Urban/rural context and kinship or son-preference institutions.
- Target-phenomenon relevance: `PM`, `FDT`, `SDT`, combinations, or `none`.

The synthesis should separate two judgments: internal causal credibility in the study setting and
transportability to each target phenomenon. An internally credible pension expansion study in rural
or historical settings may have high mechanism relevance but limited SDT transportability if family
old-age support is weak in the target setting.

### Stage 8: Effect Harmonization

Convert estimates into a hierarchy of comparable fertility units:

1. Births per woman / completed fertility change.
2. Probability of birth in a period.
3. Parity-specific birth hazard or probability.
4. Fertility intention or contraceptive-use outcomes, if the hypothesis chapter allows
   fertility-adjacent evidence.

The pipeline should retain original estimates even when harmonization is impossible. Harmonization
assumptions must be explicit and reversible.

### Stage 9: Quantitative Synthesis

Pool only estimates with compatible estimands, outcomes, exposure scales, and follow-up windows.
Default model:

- Random-effects meta-analysis when at least three comparable estimates exist.
- Cluster or robust variance handling when several estimates come from the same study.
- Meta-regression only when the number of independent studies is large enough to support it.

If pooling is inappropriate, produce grouped tables and a narrative synthesis organized by design,
country/period, treatment margin, and outcome margin.

### Stage 10: Demographic Significance

Translate causal estimates into demographic relevance:

- Slope sufficiency: can observed changes in the cause plausibly generate observed PM/FDT/SDT
  fertility movement?
- Decomposition share where macro data allow it.
- Conditional association benchmarks only as supporting evidence, never as causal proof.

This is the key bridge from Cochrane-style causal evidence to the project’s core question:
does the mechanism matter enough to explain fertility decline?

### Stage 11: GRADE and Summary of Findings

Create a per-phenomenon GRADE judgment for PM, FDT, and SDT:

- Starting level based on study design and identification.
- Downgrade for risk of bias, inconsistency, indirectness, imprecision, and publication bias.
- Upgrade only with strong, replicated quasi-experimental evidence and large coherent effects.

Output a summary-of-findings table with effect size, number of studies, settings, certainty, and
plain-language interpretation.

### Stage 12: Hybrid Chapter/Paper Draft

Generate a chapter whose main text reads like a JEL review and whose methods/results audit trail
meets Cochrane expectations. The chapter should not hide uncertainty in prose; it should use
Cochrane/GRADE certainty language while preserving economics interpretation.

## 6. Recommended Chapter Structure

1. Claim and bottom-line verdict.
2. Mechanism and intellectual genealogy.
3. Search and inclusion methods.
4. PRISMA flow.
5. Evidence map and included studies.
6. Risk of bias and identification quality.
7. Quantitative synthesis or structured narrative synthesis.
8. Theory-source table and mechanism map.
9. External validity and transportability to PM/FDT/SDT.
10. Demographic significance for PM/FDT/SDT.
11. GRADE certainty and summary of findings.
12. Interpretation for economics readers.
13. Open questions and high-value research designs.
14. References and reproducibility appendix.

## 7. Human Review Gates

| Gate | Reviewer | Trigger |
|---|---|---|
| RA title/abstract review | RA | Before PDF retrieval/final full-text set. |
| Identity verification | RA or PI | No DOI, DOI drift, title mismatch, duplicate uncertainty. |
| Full-text inclusion | RA; PI for `UNSURE_PI` | Before extraction. |
| Extraction verification | RA | Random 10% plus all high-influence estimates. |
| Risk-of-bias disputes | PI | Domain disagreement or identification ambiguity. |
| Harmonization disputes | PI | Unit conversion changes substantive interpretation. |
| GRADE disagreements | PI | Raters differ by more than one certainty level. |

## 8. Implementation Order

1. Freeze RA review decisions and PDF status.
2. Build the full-text screen and retrieval reconciliation scripts.
3. Populate the OAS theory-source table and empirical extraction templates.
4. Implement risk-of-bias and transportability table generation.
5. Implement effect harmonization and meta-analysis scripts.
6. Generate PRISMA, summary-of-findings, and demographic-significance outputs.
7. Draft the OAS chapter from structured outputs.

## 9. Open Design Questions

1. Whether fertility-adjacent outcomes, such as contraception or education investments, enter
   quantitative synthesis or only mechanism narrative.
2. Whether the OAS chapter should include all 40 DOI-trusted RA candidates or only those marked
   `RETRIEVE` after RA review.
3. Whether published and working-paper versions should both be inspected when the published version
   has less detail than the working paper.
4. Whether demographic significance should be computed before or after PI signs off on effect-size
   harmonization.
