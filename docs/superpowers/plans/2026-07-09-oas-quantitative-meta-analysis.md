# OAS Quantitative Meta-Analysis Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build an audit-traceable quantitative synthesis for the old-age-security / pension crowd-out chapter.

**Architecture:** Add small Python analysis scripts under `source/analysis/` that validate extraction tables, generate RA-facing review sheets, harmonize estimates conservatively, and write summary tables. Human-readable numeric evidence stays in CSVs; the chapter reads those outputs and does not claim pooled effects unless the summary table supports pooling.

**Tech Stack:** Python standard library (`csv`, `dataclasses`, `decimal`, `pathlib`, `statistics`, `unittest`), local PDFs in `literature/pdfs/old-age-security-pension-crowdout/`, Markdown chapter output.

---

## File Structure

- Create `source/analysis/oas_meta_pipeline.py`: shared constants, CSV validation, RA review generation, harmonization, meta-summary, and summary-of-findings writers.
- Create `source/analysis/test_oas_meta_pipeline.py`: standard-library `unittest` checks for schema validation, RA sheet columns, harmonization, and poolability decisions.
- Create `extraction/old-age-security-pension-crowdout-effects.csv`: source-of-truth estimate extraction table.
- Create `output/old-age-security-pension-crowdout-effect-extraction-review.csv`: RA-facing exception-based verification sheet.
- Create `extraction/old-age-security-pension-crowdout-risk-of-bias.csv`: one row per included empirical study.
- Create `output/tables/old-age-security-pension-crowdout-harmonized-effects.csv`: original plus harmonized estimates and poolability decisions.
- Create `output/tables/old-age-security-pension-crowdout-meta-analysis-summary.csv`: pooled estimates if valid, otherwise explicit no-pooling rationale.
- Create `output/tables/old-age-security-pension-crowdout-summary-of-findings.csv`: GRADE-style summary rows.
- Create `output/figures/old-age-security-pension-crowdout-evidence-map.csv`: evidence-map data for downstream plotting.
- Modify `output/chapters/old-age-security-pension-crowdout.md`: replace “not yet quantitative” language with the generated quantitative synthesis.
- Modify `tickets/TICK-016-oas-data-extraction.md`, `tickets/TICK-017-oas-risk-of-bias.md`, `tickets/TICK-018-oas-effect-harmonization-meta-analysis.md`, and `tickets/TICK-019-oas-demographic-significance-and-chapter.md`: record completion notes as tasks finish.

---

### Task 1: Add Pipeline Library and Validation Tests

**Files:**
- Create: `source/analysis/oas_meta_pipeline.py`
- Create: `source/analysis/test_oas_meta_pipeline.py`

- [ ] **Step 1: Write failing tests for required CSV behavior**

Create `source/analysis/test_oas_meta_pipeline.py` with:

```python
import csv
import tempfile
import unittest
from pathlib import Path

from oas_meta_pipeline import (
    EFFECT_REQUIRED_COLUMNS,
    REVIEW_FIELDS,
    harmonize_effect_row,
    make_effect_review_columns,
    validate_required_columns,
)


class OASMetaPipelineTests(unittest.TestCase):
    def test_validate_required_columns_rejects_missing_column(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "effects.csv"
            path.write_text("effect_id,study_id\nx,y\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "Missing required columns"):
                validate_required_columns(path, EFFECT_REQUIRED_COLUMNS)

    def test_make_effect_review_columns_adds_decision_columns(self):
        columns = make_effect_review_columns()
        self.assertIn("pdf_filename", columns)
        self.assertIn("effect_original", columns)
        self.assertIn("effect_original_ra_decision", columns)
        self.assertIn("extract_page_ra_decision", columns)
        self.assertNotIn("pdf_filename_ra_decision", columns)

    def test_harmonize_percentage_points(self):
        row = {
            "effect_id": "e1",
            "outcome_family": "birth_probability",
            "outcome_unit_original": "percentage_points",
            "effect_original": "-12",
            "se_original": "3",
            "mechanism_cell": "A",
            "needs_pi": "no",
        }
        out = harmonize_effect_row(row)
        self.assertEqual(out["harmonized_outcome_unit"], "probability_of_birth")
        self.assertEqual(out["effect_harmonized"], "-0.12")
        self.assertEqual(out["se_harmonized"], "0.03")
        self.assertEqual(out["meta_analysis_group"], "cell_a_birth_probability")

    def test_harmonize_non_poolable_completed_fertility_without_se(self):
        row = {
            "effect_id": "e2",
            "outcome_family": "completed_fertility",
            "outcome_unit_original": "births_per_woman",
            "effect_original": "-1.3",
            "se_original": "",
            "mechanism_cell": "A",
            "needs_pi": "no",
        }
        out = harmonize_effect_row(row)
        self.assertEqual(out["harmonized_outcome_unit"], "births_per_woman")
        self.assertEqual(out["effect_harmonized"], "-1.3")
        self.assertEqual(out["meta_analysis_group"], "not_poolable")
        self.assertIn("missing_standard_error", out["poolability_reason"])


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run tests to verify they fail**

Run:

```bash
python3 -m unittest source/analysis/test_oas_meta_pipeline.py
```

Expected: fail with `ModuleNotFoundError: No module named 'oas_meta_pipeline'`.

- [ ] **Step 3: Implement `oas_meta_pipeline.py`**

Create `source/analysis/oas_meta_pipeline.py` with:

```python
#!/usr/bin/env python3
"""Utilities for OAS effect extraction, review, and conservative synthesis."""

from __future__ import annotations

import csv
from decimal import Decimal, InvalidOperation
from pathlib import Path


SLUG = "old-age-security-pension-crowdout"
ROOT = Path(__file__).resolve().parents[2]

EFFECT_REQUIRED_COLUMNS = [
    "effect_id",
    "study_id",
    "pdf_path",
    "pdf_filename",
    "mechanism_cell",
    "estimand_label",
    "is_primary_estimate",
    "outcome_name",
    "outcome_family",
    "outcome_unit_original",
    "effect_original",
    "se_original",
    "ci_lower_original",
    "ci_upper_original",
    "p_value",
    "n_observations",
    "n_clusters",
    "model_specification",
    "comparison_group",
    "treatment_scale_original",
    "followup_window",
    "subgroup",
    "extract_page",
    "extract_quote_or_note",
    "extracted_by",
    "ra_verified",
    "needs_pi",
]

REVIEW_FIELDS = [
    "mechanism_cell",
    "estimand_label",
    "is_primary_estimate",
    "outcome_name",
    "outcome_family",
    "outcome_unit_original",
    "effect_original",
    "se_original",
    "ci_lower_original",
    "ci_upper_original",
    "p_value",
    "model_specification",
    "treatment_scale_original",
    "followup_window",
    "subgroup",
    "extract_page",
    "extract_quote_or_note",
    "needs_pi",
]

HARMONIZED_COLUMNS = EFFECT_REQUIRED_COLUMNS + [
    "harmonized_outcome_unit",
    "effect_harmonized",
    "se_harmonized",
    "harmonization_method",
    "meta_analysis_group",
    "poolability_reason",
]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def validate_required_columns(path: Path, required: list[str]) -> None:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        fieldnames = reader.fieldnames or []
    missing = [column for column in required if column not in fieldnames]
    if missing:
        raise ValueError(f"Missing required columns in {path}: {', '.join(missing)}")


def make_effect_review_columns() -> list[str]:
    context = ["effect_id", "study_id", "pdf_filename"]
    columns: list[str] = context[:]
    for field in REVIEW_FIELDS:
        columns.extend([field, f"{field}_ra_decision"])
    return columns


def _decimal(value: str) -> Decimal | None:
    value = (value or "").strip()
    if not value:
        return None
    try:
        return Decimal(value)
    except InvalidOperation:
        return None


def _format_decimal(value: Decimal | None) -> str:
    if value is None:
        return ""
    normalized = value.normalize()
    return format(normalized, "f")


def harmonize_effect_row(row: dict[str, str]) -> dict[str, str]:
    out = dict(row)
    effect = _decimal(row.get("effect_original", ""))
    se = _decimal(row.get("se_original", ""))
    family = row.get("outcome_family", "")
    unit = row.get("outcome_unit_original", "")
    cell = row.get("mechanism_cell", "")

    out.update(
        {
            "harmonized_outcome_unit": "",
            "effect_harmonized": "",
            "se_harmonized": "",
            "harmonization_method": "",
            "meta_analysis_group": "not_poolable",
            "poolability_reason": "",
        }
    )

    if effect is None:
        out["poolability_reason"] = "missing_or_non_numeric_effect"
        return out

    if family == "birth_probability" and unit == "percentage_points":
        out["harmonized_outcome_unit"] = "probability_of_birth"
        out["effect_harmonized"] = _format_decimal(effect / Decimal("100"))
        out["se_harmonized"] = _format_decimal(se / Decimal("100")) if se is not None else ""
        out["harmonization_method"] = "percentage_points_divided_by_100"
        if cell == "A" and se is not None:
            out["meta_analysis_group"] = "cell_a_birth_probability"
            out["poolability_reason"] = "poolable_birth_probability_if_followup_windows_match"
        else:
            out["poolability_reason"] = "missing_standard_error_or_wrong_cell"
        return out

    if family == "completed_fertility" and unit == "births_per_woman":
        out["harmonized_outcome_unit"] = "births_per_woman"
        out["effect_harmonized"] = _format_decimal(effect)
        out["se_harmonized"] = _format_decimal(se)
        out["harmonization_method"] = "already_births_per_woman"
        if cell == "A" and se is not None:
            out["meta_analysis_group"] = "cell_a_completed_fertility"
            out["poolability_reason"] = "poolable_completed_fertility_if_treatment_scales_match"
        else:
            out["poolability_reason"] = "missing_standard_error_or_wrong_cell"
        return out

    if family in {"tfr", "crude_birth_rate", "child_woman_ratio"}:
        out["harmonized_outcome_unit"] = unit
        out["effect_harmonized"] = _format_decimal(effect)
        out["se_harmonized"] = _format_decimal(se)
        out["harmonization_method"] = "preserved_original_aggregate_unit"
        out["poolability_reason"] = "aggregate_or_historical_unit_not_pooled_with_micro_estimates"
        return out

    out["poolability_reason"] = "unsupported_outcome_family_or_unit"
    return out
```

- [ ] **Step 4: Run tests to verify they pass**

Run:

```bash
python3 -m unittest source/analysis/test_oas_meta_pipeline.py
```

Expected: `OK`.

- [ ] **Step 5: Commit**

Run:

```bash
git add source/analysis/oas_meta_pipeline.py source/analysis/test_oas_meta_pipeline.py
git commit -m "Add OAS meta-analysis pipeline utilities"
```

---

### Task 2: Extract Main Effect Estimates from Retrieved PDFs

**Files:**
- Create: `extraction/old-age-security-pension-crowdout-effects.csv`

- [ ] **Step 1: Create the effect table with schema-complete rows**

Use the retrieved PDFs and fill one or more main estimates per study. For each row, use `mechanism_cell`
values `A`, `B`, or `C`; use `A` for the nine primary old-age-security motive studies and `B` for Ci.
Use exact page/table/figure locators from the PDFs. If a standard error is not reported, leave
`se_original` blank and use available `ci_*` or `p_value` fields.

Create `extraction/old-age-security-pension-crowdout-effects.csv` with this header:

```csv
effect_id,study_id,pdf_path,pdf_filename,mechanism_cell,estimand_label,is_primary_estimate,outcome_name,outcome_family,outcome_unit_original,effect_original,se_original,ci_lower_original,ci_upper_original,p_value,n_observations,n_clusters,model_specification,comparison_group,treatment_scale_original,followup_window,subgroup,extract_page,extract_quote_or_note,extracted_by,ra_verified,needs_pi
```

Minimum required rows for this pass:

```text
danzer_zyska_2023_brazil_pensions_e01
rossi_godard_2022_namibia_pensions_e01
billari_galasso_2009_italy_pension_reforms_e01
han_tao_wang_zhang_2025_china_ltci_e01
guinnane_streb_2021_prussia_social_security_e01
shen_zheng_yang_2020_china_nrps_e01
ci_2024_children_insurance_e01
fenge_scheubel_2017_germany_pensions_e01
basso_bodenhorn_cuberes_2014_us_financial_development_e01
galofre_vila_2023_us_baby_boom_e01
```

- [ ] **Step 2: Validate required columns**

Run:

```bash
python3 - <<'PY'
from pathlib import Path
from source.analysis.oas_meta_pipeline import EFFECT_REQUIRED_COLUMNS, validate_required_columns
validate_required_columns(Path("extraction/old-age-security-pension-crowdout-effects.csv"), EFFECT_REQUIRED_COLUMNS)
print("effects schema ok")
PY
```

Expected: `effects schema ok`.

- [ ] **Step 3: Validate numeric locators and PI flags**

Run:

```bash
python3 - <<'PY'
import csv
from pathlib import Path

path = Path("extraction/old-age-security-pension-crowdout-effects.csv")
bad = []
with path.open(newline="", encoding="utf-8") as handle:
    for row in csv.DictReader(handle):
        if not row["effect_original"].strip():
            bad.append((row["effect_id"], "missing effect_original"))
        if not row["extract_page"].strip():
            bad.append((row["effect_id"], "missing extract_page"))
        if not row["extract_quote_or_note"].strip():
            bad.append((row["effect_id"], "missing extract_quote_or_note"))
        if row["needs_pi"] not in {"yes", "no"}:
            bad.append((row["effect_id"], "needs_pi must be yes or no"))
if bad:
    for item in bad:
        print(item)
    raise SystemExit(1)
print("effect extraction locators ok")
PY
```

Expected: `effect extraction locators ok`.

- [ ] **Step 4: Commit**

Run:

```bash
git add extraction/old-age-security-pension-crowdout-effects.csv
git commit -m "Extract OAS effect estimates"
```

---

### Task 3: Generate Effect RA Verification Sheet

**Files:**
- Modify: `source/analysis/oas_meta_pipeline.py`
- Create: `output/old-age-security-pension-crowdout-effect-extraction-review.csv`

- [ ] **Step 1: Add RA sheet generation function**

Append this function to `source/analysis/oas_meta_pipeline.py`:

```python
def make_effect_review_sheet(effects_path: Path, review_path: Path) -> None:
    validate_required_columns(effects_path, EFFECT_REQUIRED_COLUMNS)
    rows = read_csv(effects_path)
    review_columns = make_effect_review_columns()
    review_rows: list[dict[str, str]] = []
    for row in rows:
        review_row: dict[str, str] = {}
        for column in review_columns:
            if column.endswith("_ra_decision"):
                review_row[column] = ""
            else:
                review_row[column] = row.get(column, "")
        review_rows.append(review_row)
    write_csv(review_path, review_rows, review_columns)


def main() -> None:
    effects_path = ROOT / "extraction" / f"{SLUG}-effects.csv"
    review_path = ROOT / "output" / f"{SLUG}-effect-extraction-review.csv"
    harmonized_path = ROOT / "output" / "tables" / f"{SLUG}-harmonized-effects.csv"
    if effects_path.exists():
        make_effect_review_sheet(effects_path, review_path)
        rows = [harmonize_effect_row(row) for row in read_csv(effects_path)]
        write_csv(harmonized_path, rows, HARMONIZED_COLUMNS)


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Run tests**

Run:

```bash
python3 -m unittest source/analysis/test_oas_meta_pipeline.py
```

Expected: `OK`.

- [ ] **Step 3: Generate review sheet**

Run:

```bash
python3 source/analysis/oas_meta_pipeline.py
```

Expected files:

```text
output/old-age-security-pension-crowdout-effect-extraction-review.csv
output/tables/old-age-security-pension-crowdout-harmonized-effects.csv
```

- [ ] **Step 4: Validate review sheet has adjacent decision columns**

Run:

```bash
python3 - <<'PY'
import csv
from pathlib import Path
path = Path("output/old-age-security-pension-crowdout-effect-extraction-review.csv")
with path.open(newline="", encoding="utf-8") as handle:
    fieldnames = csv.DictReader(handle).fieldnames or []
for required in ["effect_original_ra_decision", "extract_page_ra_decision", "needs_pi_ra_decision"]:
    if required not in fieldnames:
        raise SystemExit(f"missing {required}")
print("effect review sheet ok")
PY
```

Expected: `effect review sheet ok`.

- [ ] **Step 5: Commit**

Run:

```bash
git add source/analysis/oas_meta_pipeline.py output/old-age-security-pension-crowdout-effect-extraction-review.csv output/tables/old-age-security-pension-crowdout-harmonized-effects.csv
git commit -m "Generate OAS effect review and harmonized tables"
```

---

### Task 4: Add Risk-of-Bias Table

**Files:**
- Create: `extraction/old-age-security-pension-crowdout-risk-of-bias.csv`

- [ ] **Step 1: Create one risk-of-bias row per empirical study**

Create `extraction/old-age-security-pension-crowdout-risk-of-bias.csv` with:

```csv
study_id,confounding,selection,exposure_classification,deviations,missing_data,outcome_measurement,reported_result_selection,identification_credibility,overall,rationale,assessed_by,ra_verified
```

Use these judgments:

```text
low
moderate
serious
critical
no_information
```

At minimum include the ten current retrieved studies. Ci remains included as mechanism evidence, but
the `rationale` should state that it is not a fertility-effect estimate. Grandparental-childcare
studies should be added only after their PDFs are retrieved; otherwise the summary table should say
Cell C quantitative risk-of-bias assessment is pending retrieval.

- [ ] **Step 2: Validate study coverage**

Run:

```bash
python3 - <<'PY'
import csv
from pathlib import Path

studies = set()
with Path("extraction/old-age-security-pension-crowdout-studies.csv").open(newline="", encoding="utf-8") as handle:
    for row in csv.DictReader(handle):
        if row["fulltext_decision"] == "INCLUDE_EMPIRICAL":
            studies.add(row["study_id"])

rob = set()
with Path("extraction/old-age-security-pension-crowdout-risk-of-bias.csv").open(newline="", encoding="utf-8") as handle:
    for row in csv.DictReader(handle):
        rob.add(row["study_id"])

missing = sorted(studies - rob)
if missing:
    raise SystemExit("missing risk-of-bias rows: " + ", ".join(missing))
print("risk-of-bias coverage ok")
PY
```

Expected: `risk-of-bias coverage ok`.

- [ ] **Step 3: Commit**

Run:

```bash
git add extraction/old-age-security-pension-crowdout-risk-of-bias.csv
git commit -m "Assess OAS risk of bias"
```

---

### Task 5: Write Meta-Analysis Summary and Evidence Map Outputs

**Files:**
- Modify: `source/analysis/oas_meta_pipeline.py`
- Create: `output/tables/old-age-security-pension-crowdout-meta-analysis-summary.csv`
- Create: `output/tables/old-age-security-pension-crowdout-summary-of-findings.csv`
- Create: `output/figures/old-age-security-pension-crowdout-evidence-map.csv`

- [ ] **Step 1: Add summary writers**

Append these functions above `main()` in `source/analysis/oas_meta_pipeline.py`:

```python
def write_meta_analysis_summary(harmonized_path: Path, summary_path: Path) -> None:
    rows = read_csv(harmonized_path)
    groups: dict[str, list[dict[str, str]]] = {}
    for row in rows:
        groups.setdefault(row.get("meta_analysis_group", "not_poolable"), []).append(row)

    summary_rows: list[dict[str, str]] = []
    for group, group_rows in sorted(groups.items()):
        if group == "not_poolable":
            summary_rows.append(
                {
                    "meta_analysis_group": group,
                    "n_effects": str(len(group_rows)),
                    "synthesis_type": "structured_narrative",
                    "pooled_effect": "",
                    "pooled_se": "",
                    "rationale": "Rows are non-poolable because outcome units, treatment scales, standard errors, or mechanism cells are incompatible.",
                }
            )
            continue
        effects = [_decimal(row.get("effect_harmonized", "")) for row in group_rows]
        ses = [_decimal(row.get("se_harmonized", "")) for row in group_rows]
        usable = [(effect, se) for effect, se in zip(effects, ses) if effect is not None and se is not None and se != 0]
        if len(usable) < 3:
            summary_rows.append(
                {
                    "meta_analysis_group": group,
                    "n_effects": str(len(group_rows)),
                    "synthesis_type": "not_pooled",
                    "pooled_effect": "",
                    "pooled_se": "",
                    "rationale": "Fewer than three compatible effects with standard errors.",
                }
            )
            continue
        weights = [Decimal("1") / (se * se) for _, se in usable]
        pooled = sum(effect * weight for (effect, _), weight in zip(usable, weights)) / sum(weights)
        pooled_se = (Decimal("1") / sum(weights)).sqrt()
        summary_rows.append(
            {
                "meta_analysis_group": group,
                "n_effects": str(len(usable)),
                "synthesis_type": "fixed_effect_inverse_variance_screening",
                "pooled_effect": _format_decimal(pooled),
                "pooled_se": _format_decimal(pooled_se),
                "rationale": "Screening estimate only; random-effects synthesis should replace this if heterogeneity warrants and enough comparable estimates exist.",
            }
        )

    write_csv(
        summary_path,
        summary_rows,
        ["meta_analysis_group", "n_effects", "synthesis_type", "pooled_effect", "pooled_se", "rationale"],
    )


def write_summary_of_findings(summary_path: Path, sof_path: Path) -> None:
    summary_rows = read_csv(summary_path)
    has_pooled = any(row["synthesis_type"] == "fixed_effect_inverse_variance_screening" for row in summary_rows)
    rows = [
        {
            "outcome_or_channel": "Classic old-age-security motive",
            "studies": "Cell A extracted studies",
            "synthesis": "pooled where compatible" if has_pooled else "structured quantitative narrative",
            "certainty": "moderate for direction; magnitude pending RA verification",
            "interpretation": "Non-child old-age security generally lowers fertility in settings where children are old-age support assets.",
        },
        {
            "outcome_or_channel": "Children as old-age-security assets",
            "studies": "Cell B mechanism studies",
            "synthesis": "not pooled with fertility effects",
            "certainty": "low-to-moderate",
            "interpretation": "Mechanism evidence supports children and purchased old-age security as substitutes, but it does not estimate fertility effects.",
        },
        {
            "outcome_or_channel": "Grandparental childcare",
            "studies": "Cell C studies pending retrieval or extraction",
            "synthesis": "separate SDT track",
            "certainty": "pending quantitative extraction",
            "interpretation": "This channel is opposite-signed and should not be pooled with the classic OAS motive.",
        },
        {
            "outcome_or_channel": "Demographic significance",
            "studies": "All extracted studies plus target-period derivation",
            "synthesis": "slope-sufficiency pending macro-data pass",
            "certainty": "low pending computation",
            "interpretation": "Current evidence supports a real mechanism but does not yet quantify its share of PM, FDT, or SDT fertility change.",
        },
    ]
    write_csv(sof_path, rows, ["outcome_or_channel", "studies", "synthesis", "certainty", "interpretation"])


def write_evidence_map(harmonized_path: Path, evidence_map_path: Path) -> None:
    rows = read_csv(harmonized_path)
    fields = [
        "effect_id",
        "study_id",
        "mechanism_cell",
        "outcome_family",
        "harmonized_outcome_unit",
        "effect_harmonized",
        "meta_analysis_group",
        "poolability_reason",
        "needs_pi",
    ]
    write_csv(evidence_map_path, rows, fields)
```

- [ ] **Step 2: Update `main()` to write all outputs**

Replace `main()` with:

```python
def main() -> None:
    effects_path = ROOT / "extraction" / f"{SLUG}-effects.csv"
    review_path = ROOT / "output" / f"{SLUG}-effect-extraction-review.csv"
    tables_dir = ROOT / "output" / "tables"
    figures_dir = ROOT / "output" / "figures"
    harmonized_path = tables_dir / f"{SLUG}-harmonized-effects.csv"
    meta_summary_path = tables_dir / f"{SLUG}-meta-analysis-summary.csv"
    sof_path = tables_dir / f"{SLUG}-summary-of-findings.csv"
    evidence_map_path = figures_dir / f"{SLUG}-evidence-map.csv"

    if effects_path.exists():
        make_effect_review_sheet(effects_path, review_path)
        rows = [harmonize_effect_row(row) for row in read_csv(effects_path)]
        write_csv(harmonized_path, rows, HARMONIZED_COLUMNS)
        write_meta_analysis_summary(harmonized_path, meta_summary_path)
        write_summary_of_findings(meta_summary_path, sof_path)
        write_evidence_map(harmonized_path, evidence_map_path)
```

- [ ] **Step 3: Run tests and regenerate outputs**

Run:

```bash
python3 -m unittest source/analysis/test_oas_meta_pipeline.py
python3 source/analysis/oas_meta_pipeline.py
```

Expected: tests pass and all four output files exist.

- [ ] **Step 4: Validate summary does not overclaim pooling**

Run:

```bash
python3 - <<'PY'
import csv
from pathlib import Path
path = Path("output/tables/old-age-security-pension-crowdout-meta-analysis-summary.csv")
with path.open(newline="", encoding="utf-8") as handle:
    rows = list(csv.DictReader(handle))
if not rows:
    raise SystemExit("empty meta-analysis summary")
for row in rows:
    if row["synthesis_type"] == "fixed_effect_inverse_variance_screening" and not row["pooled_effect"]:
        raise SystemExit("pooled row missing effect")
print("meta-analysis summary ok")
PY
```

Expected: `meta-analysis summary ok`.

- [ ] **Step 5: Commit**

Run:

```bash
git add source/analysis/oas_meta_pipeline.py output/tables/old-age-security-pension-crowdout-meta-analysis-summary.csv output/tables/old-age-security-pension-crowdout-summary-of-findings.csv output/figures/old-age-security-pension-crowdout-evidence-map.csv
git commit -m "Summarize OAS quantitative synthesis"
```

---

### Task 6: Update Chapter With Quantitative Outputs

**Files:**
- Modify: `output/chapters/old-age-security-pension-crowdout.md`

- [ ] **Step 1: Read generated output tables**

Run:

```bash
python3 - <<'PY'
from pathlib import Path
for path in [
    "output/tables/old-age-security-pension-crowdout-harmonized-effects.csv",
    "output/tables/old-age-security-pension-crowdout-meta-analysis-summary.csv",
    "output/tables/old-age-security-pension-crowdout-summary-of-findings.csv",
]:
    p = Path(path)
    print(f"{path}: {p.stat().st_size} bytes")
PY
```

Expected: all three files have positive byte counts.

- [ ] **Step 2: Replace the chapter’s quantitative-synthesis section**

Edit `output/chapters/old-age-security-pension-crowdout.md` so Section 6 states:

```markdown
## 6. Quantitative Synthesis

The quantitative synthesis is intentionally conservative. The extraction table now records the
paper-visible outcome, original effect, uncertainty when reported, treatment scale, follow-up window,
and page/table locator for each main estimate. The harmonized table preserves those original values and
adds conversions only where the unit conversion is mechanical.

Cell A and Cell C remain separate. Cell A estimates the classic old-age-security motive. Cell C estimates
grandparental-childcare effects with the opposite sign. Cell B and Cell D remain mechanism and chain-link
evidence, not fertility-effect estimates.
```

Then run this helper to generate the table-specific paragraph. Paste its output between the first
paragraph and the Cell A / Cell C paragraph:

```bash
python3 - <<'PY'
import csv
from pathlib import Path
path = Path("output/tables/old-age-security-pension-crowdout-meta-analysis-summary.csv")
with path.open(newline="", encoding="utf-8") as handle:
    rows = list(csv.DictReader(handle))
pooled = [row for row in rows if row["synthesis_type"] == "fixed_effect_inverse_variance_screening"]
if pooled:
    parts = [
        f"{row['meta_analysis_group']} pools {row['n_effects']} compatible effects with a screening fixed-effect estimate of {row['pooled_effect']} and standard error {row['pooled_se']}."
        for row in pooled
    ]
    print(" ".join(parts) + " This is reported as a screening estimate because the RA verification and heterogeneity assessment still govern whether it belongs in the final GRADE judgment.")
else:
    groups = "; ".join(f"{row['meta_analysis_group']} ({row['synthesis_type']}, n={row['n_effects']})" for row in rows)
    print("The compatibility screen does not support a pooled estimate in the current extraction. The synthesis is therefore quantitative but not pooled: " + groups + ".")
PY
```

- [ ] **Step 3: Update Summary of Findings section**

Replace the existing Section 10 table with rows from
`output/tables/old-age-security-pension-crowdout-summary-of-findings.csv`. Keep the language clear that
certainty for magnitude is pending RA verification if `ra_verified` is not `yes` for all effect rows.

- [ ] **Step 4: Update reproducibility appendix**

Add these paths if absent:

```markdown
- Effect extraction: `extraction/old-age-security-pension-crowdout-effects.csv`
- Risk of bias: `extraction/old-age-security-pension-crowdout-risk-of-bias.csv`
- Harmonized effects: `output/tables/old-age-security-pension-crowdout-harmonized-effects.csv`
- Meta-analysis summary: `output/tables/old-age-security-pension-crowdout-meta-analysis-summary.csv`
- Summary of findings: `output/tables/old-age-security-pension-crowdout-summary-of-findings.csv`
- Evidence map data: `output/figures/old-age-security-pension-crowdout-evidence-map.csv`
```

- [ ] **Step 5: Validate chapter does not contain stale “not quantitative” language**

Run:

```bash
rg -n "not yet quantitative|No pooled estimate is reported in this draft|not complete yet|not pretend" output/chapters/old-age-security-pension-crowdout.md
```

Expected: no matches. If the only match is a sentence explaining that a specific subgroup is not pooled,
rewrite it to refer to the generated meta-analysis summary table.

- [ ] **Step 6: Commit**

Run:

```bash
git add output/chapters/old-age-security-pension-crowdout.md
git commit -m "Update OAS chapter with quantitative synthesis"
```

---

### Task 7: Ticket Updates and Final Verification

**Files:**
- Modify: `tickets/TICK-016-oas-data-extraction.md`
- Modify: `tickets/TICK-017-oas-risk-of-bias.md`
- Modify: `tickets/TICK-018-oas-effect-harmonization-meta-analysis.md`
- Modify: `tickets/TICK-019-oas-demographic-significance-and-chapter.md`
- Modify: `tickets/QUEUE.md`

- [ ] **Step 1: Run final validation commands**

Run:

```bash
python3 -m unittest source/analysis/test_oas_meta_pipeline.py
python3 source/analysis/oas_meta_pipeline.py
python3 - <<'PY'
import csv
from pathlib import Path
for path in [
    "extraction/old-age-security-pension-crowdout-effects.csv",
    "extraction/old-age-security-pension-crowdout-risk-of-bias.csv",
    "output/old-age-security-pension-crowdout-effect-extraction-review.csv",
    "output/tables/old-age-security-pension-crowdout-harmonized-effects.csv",
    "output/tables/old-age-security-pension-crowdout-meta-analysis-summary.csv",
    "output/tables/old-age-security-pension-crowdout-summary-of-findings.csv",
    "output/figures/old-age-security-pension-crowdout-evidence-map.csv",
]:
    with Path(path).open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        raise SystemExit(f"{path} has no rows")
    print(f"{path}: {len(rows)} rows")
PY
```

Expected: unit tests pass, pipeline regenerates outputs, and every listed CSV has at least one row.

- [ ] **Step 2: Update ticket logs**

Add completion notes:

```markdown
- 2026-07-09: Effect-level extraction table and RA verification sheet completed for current retrieved OAS PDFs.
```

to `tickets/TICK-016-oas-data-extraction.md`.

Add:

```markdown
- 2026-07-09: Initial ROBINS-I-inspired risk-of-bias table completed for included empirical OAS studies.
```

to `tickets/TICK-017-oas-risk-of-bias.md`.

Add:

```markdown
- 2026-07-09: Harmonized-effects table, meta-analysis summary, summary-of-findings table, and evidence-map data generated. Pooling is limited to groups passing the conservative compatibility screen.
```

to `tickets/TICK-018-oas-effect-harmonization-meta-analysis.md`.

Add:

```markdown
- 2026-07-09: Chapter updated with quantitative synthesis outputs and reproducibility appendix links.
```

to `tickets/TICK-019-oas-demographic-significance-and-chapter.md`.

- [ ] **Step 3: Move tickets in `tickets/QUEUE.md` only when acceptance criteria are met**

If Tasks 2-6 pass validation, move TICK-016, TICK-017, and TICK-018 to Done. Keep TICK-019 blocked or
in progress if demographic-significance slope-sufficiency calculations are still not computed. Do not
mark TICK-019 done unless the demographic-significance table exists.

- [ ] **Step 4: Commit final ticket updates**

Run:

```bash
git add tickets/QUEUE.md tickets/TICK-016-oas-data-extraction.md tickets/TICK-017-oas-risk-of-bias.md tickets/TICK-018-oas-effect-harmonization-meta-analysis.md tickets/TICK-019-oas-demographic-significance-and-chapter.md
git commit -m "Update OAS quantitative synthesis tickets"
```

- [ ] **Step 5: Report remaining manual blockers**

In the final response, list:

```text
- Whether any effect rows have needs_pi=yes.
- Whether any Cell C grandparental-childcare PDFs are still missing.
- Whether the chapter contains a pooled estimate or a structured quantitative synthesis only.
- Whether the working tree is clean.
```

---

## Self-Review

- Spec coverage: The plan covers effect extraction, RA review sheet generation, risk of bias,
  harmonization, poolability decisions, meta-analysis summary, summary-of-findings output, evidence-map
  output, chapter update, and ticket updates.
- Placeholder scan: The plan contains no `TBD`, no `TODO`, and no generic “handle later” steps.
- Type consistency: Script functions use `Path`, `list[dict[str, str]]`, and the exact column names from
  `extraction/schema.md` and the approved spec.
- Scope check: The plan does not attempt final demographic slope-sufficiency calculations unless the
  required macro-data task is separately implemented. TICK-019 should remain open if that table is still
  absent.
