# OAS Full-Text Screen and External Validity Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Start the old-age-security pension-crowdout chapter pipeline by reconciling PDFs, coding full-text inclusion, and adding transportability fields for external-validity assessment.

**Architecture:** Treat external validity as structured study-level data that sits between internal validity/risk-of-bias and demographic significance. Keep the full-text screen narrow: it decides inclusion stream and records PDF availability; later extraction tasks populate numeric estimates and risk-of-bias tables.

**Tech Stack:** Markdown specs, CSV extraction tables, local PDF files under `literature/pdfs/old-age-security-pension-crowdout/`, and lightweight Python CSV checks.

---

### Task 1: Update Methodology Artifacts

**Files:**
- Modify: `docs/meta-analysis-paper-pipeline-design.md`
- Modify: `docs/meta-analysis-effect-size-harmonization.md`
- Modify: `extraction/schema.md`
- Modify: `output/chapters/hybrid-chapter-template.md`

- [x] **Step 1: Add external validity to the pipeline design**

Add a dedicated stage after risk of bias and before effect harmonization/demographic significance:

```markdown
### Stage 6: External Validity and Transportability

Code setting features that determine whether each internally credible estimate transports to PM,
FDT, and SDT contexts. At minimum, record welfare-state baseline, family-transfer dependence,
baseline fertility, pension coverage, treatment margin, urban/rural context, kinship/son-preference
context, target-phenomenon relevance, and a short transportability rationale.
```

- [x] **Step 2: Add study-level schema columns**

Add these columns to the study table schema and to the OAS full-text/study template once created:

```text
setting_income_level
welfare_state_baseline
pre_reform_old_age_support_norm
family_transfer_dependence
baseline_fertility_level
baseline_pension_coverage
treatment_margin
urban_rural
kinship_system_or_son_preference
period_target_relevance
transportability_to_target
external_validity_rationale
```

- [x] **Step 3: Add chapter section**

Insert an `External Validity and Transportability` section before demographic significance in the
chapter template. It must separate internal causal credibility from transportability to PM/FDT/SDT.

### Task 2: Reconcile PDFs

**Files:**
- Modify: `extraction/old-age-security-pension-crowdout-fulltext-screen.csv`
- Modify: `output/old-age-security-pension-crowdout-ra-selected-pdf-checklist.md`

- [x] **Step 1: Rename PDFs to citation-style names**

Use author-year-short-title-source filenames under:

```text
literature/pdfs/old-age-security-pension-crowdout/
```

- [x] **Step 2: Verify every `RETRIEVE` row has an existing PDF path**

Run:

```bash
python3 - <<'PY'
import csv
from pathlib import Path
rows=list(csv.DictReader(open('extraction/old-age-security-pension-crowdout-fulltext-screen.csv')))
missing=[(r['doi'], r['expected_pdf_path']) for r in rows if not Path(r['expected_pdf_path']).exists()]
print('rows', len(rows))
print('missing_paths', len(missing))
PY
```

Expected:

```text
rows 10
missing_paths 0
```

### Task 3: Full-Text Screen

**Files:**
- Modify: `extraction/old-age-security-pension-crowdout-fulltext-screen.csv`
- Create: `extraction/old-age-security-pension-crowdout-studies.csv`

- [ ] **Step 1: Screen each PDF**

For each of the 10 RA-retrieved papers, record:

```text
fulltext_decision = INCLUDE_EMPIRICAL | INCLUDE_THEORY | EXCLUDE | UNSURE_PI
included_stream = empirical_meta | empirical_narrative | theory | none
screened_by = Codex
ra_verified = not_sampled
```

- [ ] **Step 2: Create study-level skeleton**

Create `extraction/old-age-security-pension-crowdout-studies.csv` using the study-level schema,
including the external-validity columns. Populate bibliographic, PDF, setting, and initial
transportability fields from the full text where available.

- [ ] **Step 3: Verify full-text screen completeness**

Run:

```bash
python3 - <<'PY'
import csv
rows=list(csv.DictReader(open('extraction/old-age-security-pension-crowdout-fulltext-screen.csv')))
bad=[r for r in rows if not r['fulltext_decision'] or not r['included_stream'] or not r['screened_by']]
print('rows', len(rows))
print('incomplete', len(bad))
PY
```

Expected:

```text
rows 10
incomplete 0
```

### Task 3A: Exception-Based RA Verification Sheets

**Files:**
- Create: `output/old-age-security-pension-crowdout-study-extraction-review.csv`
- Create: `output/old-age-security-pension-crowdout-effect-extraction-review-template.csv`
- Modify: `extraction/schema.md`
- Modify: `docs/meta-analysis-paper-pipeline-design.md`

- [ ] **Step 1: Document the adjacent review-column convention**

For every characteristic that needs verification, reviewer-facing sheets use:

```text
characteristic
characteristic_ra_decision
characteristic_ra_notes
```

Blank `characteristic_ra_decision` means approved by default. Nonblank values are `FIX`,
`UNSURE_PI`, or `EXCLUDE`.

- [ ] **Step 2: Generate the study-level review sheet**

Create one row per study from `extraction/old-age-security-pension-crowdout-studies.csv`, with
adjacent RA review columns for bibliographic identity, design, setting, inclusion stream, and
external-validity fields.

- [ ] **Step 3: Generate the effect-level review template**

Create a header-only template for effect extraction review using the same adjacent review-column
pattern. Populate rows after effect extraction.

### Task 4: Commit Handoff

**Files:**
- Modify: `tickets/QUEUE.md`
- Modify: `tickets/TICK-015-oas-fulltext-screen.md`
- Modify/create files from Tasks 1-3

- [ ] **Step 1: Run focused validation**

Run:

```bash
python3 -m pytest source/build/goldset/test_ra_review_csv.py
```

Expected:

```text
2 passed
```

- [ ] **Step 2: Commit the completed screen**

```bash
git add docs/meta-analysis-paper-pipeline-design.md docs/meta-analysis-effect-size-harmonization.md extraction/schema.md output/chapters/hybrid-chapter-template.md extraction/old-age-security-pension-crowdout-fulltext-screen.csv extraction/old-age-security-pension-crowdout-studies.csv output/old-age-security-pension-crowdout-ra-selected-pdf-checklist.md tickets/QUEUE.md tickets/TICK-015-oas-fulltext-screen.md docs/superpowers/plans/2026-07-03-oas-fulltext-screen-external-validity.md
git commit -m "Start OAS full-text screen with transportability coding"
```

## Self-Review

- Spec coverage: covers external-validity methodology, schema, chapter placement, PDF reconciliation, and full-text screen startup.
- Placeholder scan: no `TBD` or `TODO` placeholders.
- Type consistency: `transportability_to_target`, `period_target_relevance`, and `external_validity_rationale` names match the schema changes planned for Task 1.
