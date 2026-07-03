# Extraction Schema

**Purpose:** Define the structured data needed to move from full-text PDFs to risk-of-bias
assessment, effect harmonization, meta-analysis, demographic significance, and chapter drafting.

Use one study-level table and one estimate-level table. A single paper can contribute multiple
estimate rows.

## RA Verification Convention

Reviewer-facing verification sheets use an exception-based format. For each characteristic that
needs human verification, place the extracted value next to two review columns:

```text
{characteristic}
{characteristic}_ra_decision
{characteristic}_ra_notes
```

Blank `{characteristic}_ra_decision` means the reviewer approves the extracted value. Reviewers
only need to mark fields that are wrong, ambiguous, or should be excluded. Valid nonblank decisions:

- `FIX` — value is wrong; corrected value or instruction goes in `{characteristic}_ra_notes`.
- `UNSURE_PI` — reviewer cannot adjudicate; PI decision required.
- `EXCLUDE` — value or estimate should not be used for synthesis.

This convention applies to both study-level characteristics and estimate-level characteristics.
The source-of-truth extraction tables remain compact; reviewer-facing sheets may duplicate columns
to make human checking faster.

## Study-Level Table: `{slug}-studies.csv`

One row per included empirical study.

| Column | Required | Description |
|---|---:|---|
| `study_id` | yes | Stable local ID, preferably `{first_author}_{year}_{short_slug}`. |
| `paper_id` | yes | OpenAlex W-ID or local hash from GACS. |
| `doi` | yes if available | Canonical DOI from the clean DOI list. |
| `title` | yes | Full study title. |
| `authors` | yes | Semicolon-separated author names. |
| `year` | yes | Publication or working-paper year. |
| `journal_or_series` | no | Journal, working-paper series, or institution. |
| `country_or_region` | yes | Country, region, or multi-country scope. |
| `period_start` | no | First year of sample period. |
| `period_end` | no | Last year of sample period. |
| `population` | yes | Target population, e.g. rural married women, households, adult children. |
| `treatment_or_exposure` | yes | Policy, institution, or variable changing old-age security. |
| `mechanism_stream` | yes | `old_age_security`, `grandparent_childcare`, `intergenerational_transfer`, `other`. |
| `primary_outcome_family` | yes | `fertility`, `fertility_adjacent`, `non_fertility`. |
| `design` | yes | RCT, DiD, event study, IV, RD, panel FE, OLS, structural, qualitative, theory. |
| `identification_source` | yes | Source of identifying variation, e.g. reform rollout, age cutoff, eligibility rule. |
| `data_source` | no | Survey/admin dataset or macro source. |
| `setting_income_level` | no | `low_income`, `lower_middle_income`, `upper_middle_income`, `high_income`, `historical`, or `mixed`. |
| `welfare_state_baseline` | yes | Pre-treatment welfare/pension baseline: `none_or_minimal`, `emerging`, `mature`, `mixed`, or `unclear`. |
| `pre_reform_old_age_support_norm` | yes | Dominant old-age support arrangement before treatment: `family_children`, `state_pension`, `private_savings`, `mixed`, or `unclear`. |
| `family_transfer_dependence` | yes | Importance of family/children for old-age support: `high`, `moderate`, `low`, or `unclear`. |
| `baseline_fertility_level` | no | Baseline fertility level or qualitative category if numeric baseline is unavailable. |
| `baseline_pension_coverage` | no | Baseline pension or old-age insurance coverage before the treatment. |
| `treatment_margin` | yes | `new_coverage`, `benefit_generosity`, `eligibility_age`, `long_term_care_insurance`, `financial_market_access`, `other`, or `unclear`. |
| `urban_rural` | no | `urban`, `rural`, `mixed`, `national`, or `unclear`. |
| `kinship_system_or_son_preference` | no | Relevant kinship, lineage, co-residence, or son-preference context. |
| `period_target_relevance` | yes | Pipe-separated target relevance: `PM`, `FDT`, `SDT`, `none`, or combinations such as `FDT|SDT`. |
| `transportability_to_target` | yes | Overall transportability judgment for this project: `high`, `moderate`, `low`, or `unclear`. |
| `external_validity_rationale` | yes | Short explanation of why the setting does or does not transport to PM/FDT/SDT. |
| `included_stream` | yes | `empirical_meta`, `empirical_narrative`, `theory`, `exclude_after_fulltext`. |
| `fulltext_decision` | yes | `INCLUDE_EMPIRICAL`, `INCLUDE_THEORY`, `EXCLUDE`, `UNSURE_PI`. |
| `fulltext_reason` | yes | Short rationale for inclusion/exclusion. |
| `pdf_path` | yes if included | Local path to the PDF used for extraction. |
| `extraction_status` | yes | `not_started`, `extracted`, `ra_verified`, `needs_pi`. |
| `notes` | no | Free text. |

## Theory-Source Table: `{slug}-theory-sources.csv`

One row per theory, conceptual, or canonical mechanism source used for the JEL-style theory section.
These rows are not empirical studies and do not enter effect-size synthesis.

| Column | Required | Description |
|---|---:|---|
| `theory_id` | yes | Stable local ID, preferably `{slug}_theory_{nn}`. |
| `title` | yes | Full source title. |
| `authors` | yes | Semicolon-separated author names. |
| `year` | yes if available | Publication year. |
| `venue` | no | Journal, book, working-paper series, or publisher. |
| `doi` | no | DOI when available; blank for books/chapters without DOI. |
| `stratum` | yes | `theory_foundational`, `theory_formal`, `mechanism_background`, or `empirical_classic_background`. |
| `mechanism_role` | yes | Short description of how the source informs the chapter mechanism. |
| `use_in_chapter` | yes | `theory_section`, `mechanism_background`, `historical_context`, or `do_not_use`. |
| `source_status` | yes | `VERIFIED`, `TITLE_KEY`, `UNRESOLVED`, or other source-resolution status. |
| `retrieval_status` | yes | `retrieved`, `not_retrieved`, `not_needed`, or `needs_manual`. |
| `notes` | no | Version, retrieval, or interpretation notes. |

## Estimate-Level Table: `{slug}-effects.csv`

One row per estimate, contrast, or model specification that may enter synthesis.

| Column | Required | Description |
|---|---:|---|
| `effect_id` | yes | Stable ID, e.g. `{study_id}_e01`. |
| `study_id` | yes | Links to study-level table. |
| `estimand_label` | yes | Short label: main DiD, IV parity 2+, event-study 10-year effect, etc. |
| `is_primary_estimate` | yes | `yes` if authors' preferred/main estimate for this outcome. |
| `outcome_name` | yes | Exact outcome name from paper. |
| `outcome_family` | yes | `birth_probability`, `completed_fertility`, `tfr`, `parity_progression`, `intentions`, `contraception`, `other`. |
| `outcome_unit_original` | yes | Original units, e.g. percentage points, births per woman, log births. |
| `effect_original` | yes | Reported point estimate. |
| `se_original` | no | Reported or computed standard error. |
| `ci_lower_original` | no | Lower confidence interval. |
| `ci_upper_original` | no | Upper confidence interval. |
| `p_value` | no | Reported p-value. |
| `n_observations` | no | Observations in model. |
| `n_clusters` | no | Cluster count if relevant. |
| `model_specification` | yes | Controls/fixed effects/model notes. |
| `comparison_group` | no | Control or reference group. |
| `treatment_scale_original` | yes | Original treatment scale, e.g. eligible vs not, pension wealth, reform exposure. |
| `followup_window` | no | Time horizon after exposure. |
| `subgroup` | no | Sex, parity, age, income, region, etc. |
| `harmonized_outcome_unit` | no until harmonized | Target unit after conversion. |
| `effect_harmonized` | no until harmonized | Converted effect. |
| `se_harmonized` | no until harmonized | Converted standard error. |
| `harmonization_method` | no until harmonized | Formula or rule used. |
| `meta_analysis_group` | no until harmonized | Pooling group ID or `not_poolable`. |
| `risk_of_bias_overall` | no until RoB | Overall risk-of-bias judgment. |
| `extract_page` | yes | Page/table/figure location in PDF. |
| `extract_quote_or_note` | yes | Short paraphrase or compliant excerpt locating the number. |
| `extracted_by` | yes | Agent or RA name. |
| `ra_verified` | yes | `yes`, `no`, or `not_sampled`. |
| `needs_pi` | yes | `yes` if interpretation/harmonization is ambiguous. |

## Risk-of-Bias Table: `{slug}-risk-of-bias.csv`

One row per included empirical study.

| Column | Required | Description |
|---|---:|---|
| `study_id` | yes | Links to study table. |
| `confounding` | yes | `low`, `moderate`, `serious`, `critical`, `no_information`. |
| `selection` | yes | Selection into study/sample. |
| `exposure_classification` | yes | Correct classification of treatment/exposure. |
| `deviations` | yes | Deviations from intended intervention/exposure. |
| `missing_data` | yes | Missing data/attrition risk. |
| `outcome_measurement` | yes | Outcome validity and measurement timing. |
| `reported_result_selection` | yes | Selective reporting/model mining risk. |
| `identification_credibility` | yes | Economics-specific judgment on research design. |
| `overall` | yes | Worst-domain rule, with PI override allowed only if explained. |
| `rationale` | yes | Short explanation with page/table references where possible. |
| `assessed_by` | yes | Agent/RA name. |
| `ra_verified` | yes | `yes`, `no`, or `not_sampled`. |

## Full-Text Screen Table: `{slug}-fulltext-screen.csv`

One row per paper marked `RETRIEVE` or `UNSURE` at title/abstract review.

| Column | Required | Description |
|---|---:|---|
| `paper_id` | yes | GACS paper ID. |
| `doi` | yes if available | Canonical DOI. |
| `title` | yes | Paper title. |
| `pdf_status` | yes | `available`, `needs_manual`, `not_found`, `bad_file`. |
| `manifest_status` | no | Retrieval manifest status or `MANUAL` for user-provided PDFs. |
| `expected_pdf_path` | yes if available | Local path to the PDF used for screening. |
| `fulltext_decision` | yes | `INCLUDE_EMPIRICAL`, `INCLUDE_THEORY`, `EXCLUDE`, `UNSURE_PI`. |
| `exclusion_reason` | no | Required when excluded. |
| `included_stream` | yes | `empirical_meta`, `empirical_narrative`, `theory`, `none`. |
| `screened_by` | yes | Agent/RA name. |
| `ra_verified` | yes | `yes`, `no`, or `not_sampled`. |
| `notes` | no | Free text. |
