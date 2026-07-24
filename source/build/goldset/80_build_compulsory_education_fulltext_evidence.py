#!/usr/bin/env python3
"""Build verified partial full-text evidence and preliminary risk-of-bias tables.

Rows are limited to PDFs retrieved and text-extracted by steps 78-79. Values below were checked
against the named PDF sections/tables; missing values remain missing rather than inferred.
"""

import csv
from pathlib import Path


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
EVIDENCE_OUT = REPO / "extraction/compulsory-education-accessible-fulltext-evidence.csv"
ROB_OUT = REPO / "extraction/compulsory-education-accessible-risk-of-bias-preliminary.csv"

EVIDENCE_FIELDS = [
    "paperId", "title", "workstream", "fulltext_decision", "design", "setting", "reform",
    "schooling_first_stage", "fertility_outcome", "effect_summary", "persistence_or_rebound",
    "completed_fertility", "mechanism", "child_value_mechanism_status", "synthesis_status",
    "source_locator", "pdf_path",
]

ROWS = [
    {
        "paperId": "W2169373049", "title": "Fast Times at Ridgemont High? The Effect of Compulsory Schooling Laws on Teenage Births",
        "workstream": "TEMPO_COMPULSORY_SCHOOLING", "fulltext_decision": "INCLUDE",
        "design": "US state/cohort compulsory-law design; Norwegian reform design", "setting": "United States; Norway",
        "reform": "Minimum dropout ages in US; Norway minimum dropout age 14 to 16",
        "schooling_first_stage": "Law-based mandatory attainment; exact first-stage coefficient not extracted in current pass",
        "fertility_outcome": "Probability first birth before ages 17-21",
        "effect_summary": "US dropout age 16: -0.008 probability of teen birth (4.7% of mean); dropout age 17: -0.015 (8.8%); Norway reform: -0.006 (3.5%)",
        "persistence_or_rebound": "Age-threshold pattern reported; completed-fertility follow-up unavailable",
        "completed_fertility": "NOT_REPORTED", "mechanism": "School attendance/incapacitation candidate",
        "child_value_mechanism_status": "NOT_TESTED", "synthesis_status": "NARRATIVE_NUMERIC_SE_NOT_YET_EXTRACTED",
        "source_locator": "PDF abstract; Table 2 discussion, PDF pp. 17-18", "pdf_path": "literature/pdfs/compulsory-education/W2169373049__fast-times-at-ridgemont-high-the-effect-of-compulsory-schooling-laws-on-.pdf",
    },
    {
        "paperId": "W2185731654", "title": "The Impact of Education on Family Formation: Quasi-Experimental Evidence from the UK",
        "workstream": "BOTH", "fulltext_decision": "INCLUDE_BOTH_OUTCOMES",
        "design": "Regression discontinuity at 1972 UK ROSLA cohort cutoff", "setting": "United Kingdom",
        "reform": "Minimum school-leaving age 15 to 16", "schooling_first_stage": "+0.31 years education (women)",
        "fertility_outcome": "Age-specific births at 16-19; completed fertility by 45",
        "effect_summary": "Age 17 reduced-form -0.0031 to -0.0034 (3.1-3.4 births per 1,000; about 8%); IV scaling about 26% decline",
        "persistence_or_rebound": "No detectable effects at ages 18-19; effects essentially zero beyond teen years",
        "completed_fertility": "Precisely zero; 95% CI excludes effects larger than one tenth of OLS association",
        "mechanism": "Conception reduction during compulsory schooling; negligible abortion effect; incapacitation",
        "child_value_mechanism_status": "WRONG_MECHANISM_OWN_SCHOOLING", "synthesis_status": "TEMPO_NUMERIC; QUANTUM_NARRATIVE_PENDING_TABLE_EXTRACTION",
        "source_locator": "PDF introduction p. 3; Table 1 pp. 16-17; Table 3 pp. 20-21",
        "pdf_path": "literature/pdfs/compulsory-education/W2185731654__the-impact-of-education-on-family-formation-quasi-experimental-evidence-.pdf",
    },
    {
        "paperId": "W3006219298", "title": "Books or babies? The incapacitation effect of schooling on minority women",
        "workstream": "TEMPO_COMPULSORY_SCHOOLING", "fulltext_decision": "INCLUDE",
        "design": "Regression discontinuity around school-entry cutoff and leaving-age reform", "setting": "Hungary; Roma women",
        "reform": "Increase in compulsory school-leaving age", "schooling_first_stage": "Enrollment-rule compliance about 78-80%; reform exposure extends schooling",
        "fertility_outcome": "Teenage motherhood; age at motherhood; conception timing",
        "effect_summary": "Teenage motherhood decreased 13.4-26.0%; motherhood delayed by 2 years",
        "persistence_or_rebound": "Pregnancy falls during school terms but not summer/Christmas breaks",
        "completed_fertility": "NOT_REPORTED", "mechanism": "Direct incapacitation evidence using conception dates",
        "child_value_mechanism_status": "NOT_TESTED", "synthesis_status": "NARRATIVE_PERCENT_RANGE_SE_NOT_YET_EXTRACTED",
        "source_locator": "PDF abstract; mechanism discussion; enrollment compliance Table 2",
        "pdf_path": "literature/pdfs/compulsory-education/W3006219298__books-or-babies-the-incapacitation-effect-of-schooling-on-minority-women.pdf",
    },
    {
        "paperId": "W4385628385", "title": "Women's education, marriage, and fertility outcomes: Evidence from Thailand's compulsory schooling law",
        "workstream": "TEMPO_COMPULSORY_SCHOOLING", "fulltext_decision": "INCLUDE",
        "design": "Donut-hole regression discontinuity", "setting": "Thailand",
        "reform": "Compulsory education extended from 6 to 9 years",
        "schooling_first_stage": "Lower-secondary completion +7.6 to +8.9 pp overall; heterogeneous increases",
        "fertility_outcome": "Ever birth and births by age; cumulative births",
        "effect_summary": "Ever birth falls about 4-5 pp at ages 14-15; births decrease through age 17",
        "persistence_or_rebound": "Fertility rises after school years and is significantly higher at age 20; catch-up around ages 20-21",
        "completed_fertility": "NOT_OBSERVED", "mechanism": "Predominantly in-school incapacitation; short-lived human-capital spillover; delayed marriage",
        "child_value_mechanism_status": "NOT_TESTED", "synthesis_status": "NARRATIVE_AGE_SPECIFIC_FIGURE_EXTRACTION_PENDING",
        "source_locator": "PDF abstract; Figure 4 discussion pp. 16-17; Table 1 first stage",
        "pdf_path": "literature/pdfs/compulsory-education/W4385628385__women-s-education-marriage-and-fertility-outcomes-evidence-from-thailand.pdf",
    },
    {
        "paperId": "W4412362654", "title": "Do Compulsory Schooling Laws Affect Fertility Behaviors and Marriages? Evidence From India",
        "workstream": "TEMPO_COMPULSORY_SCHOOLING", "fulltext_decision": "INCLUDE_ADJACENT_MECHANISM",
        "design": "Instrumental-variable staggered difference-in-differences", "setting": "India",
        "reform": "2010 Right to Education Act; compulsory primary education ages 6-14",
        "schooling_first_stage": "+0.645 years education; first-stage F-statistic >10",
        "fertility_outcome": "Sexual activity, marriage, first birth, and fertility by ages 15-25",
        "effect_summary": "Sexual activity by 18 -7.2 pp; married by 21 -3.9 pp; first birth by 21 -2.6 pp",
        "persistence_or_rebound": "Fertility effect becomes more negative in early twenties rather than disappearing after school",
        "completed_fertility": "NOT_OBSERVED", "mechanism": "Human capital/knowledge, contraception, partner matching; paper rejects incapacitation as main channel",
        "child_value_mechanism_status": "WRONG_MECHANISM_OWN_SCHOOLING", "synthesis_status": "ADJACENT_TEMPO_DRIVER_NOT_INCAPACITATION",
        "source_locator": "PDF abstract; Table 3 p. 14; Table 4 pp. 15-16; conclusion p. 23",
        "pdf_path": "literature/pdfs/compulsory-education/W4412362654__do-compulsory-schooling-laws-affect-fertility-behaviors-and-marriages.pdf",
    },
    {
        "paperId": "W2186769068", "title": "Compulsory Education and Teenage Motherhood",
        "workstream": "TEMPO_COMPULSORY_SCHOOLING", "fulltext_decision": "INCLUDE",
        "design": "Sharp regression discontinuity at UK ROSLA cohort cutoff", "setting": "United Kingdom",
        "reform": "Minimum school-leaving age increased by one year", "schooling_first_stage": "School participation falls about 30 pp at cutoff; reform increases mandatory schooling",
        "fertility_outcome": "Motherhood at each teenage age and cumulative teenage motherhood",
        "effect_summary": "Motherhood at age 16 -0.40 pp; cumulative effect by age 18 -0.81 pp",
        "persistence_or_rebound": "Non-monotonic teen pattern; positive effect at 19; reform influence dissipates after age 20",
        "completed_fertility": "NOT_OBSERVED_SAMPLE_TO_AGE_30", "mechanism": "Incarceration plus short beyond-incarceration postponement",
        "child_value_mechanism_status": "NOT_TESTED", "synthesis_status": "TEMPO_NUMERIC_TABLES_2_3",
        "source_locator": "PDF abstract; Tables 2-3 and discussion pp. 20-23",
        "pdf_path": "literature/pdfs/compulsory-education/W2186769068__compulsory-education-and-teenage-motherhood.pdf",
    },
    {
        "paperId": "W2108204833", "title": "The Effects of Compulsory-Schooling Laws on Teenage Marriage and Births in Turkey",
        "workstream": "TEMPO_COMPULSORY_SCHOOLING", "fulltext_decision": "INCLUDE",
        "design": "Cohort discontinuity / policy exposure design", "setting": "Turkey",
        "reform": "Compulsory schooling extended from 5 to 8 years in 1997", "schooling_first_stage": "Large enrollment increase in targeted ages; exact coefficient pending table extraction",
        "fertility_outcome": "Marriage by 16 and first birth by 17-18",
        "effect_summary": "Marriage by 16 reduced 44%; first birth by 17 reduced 36%",
        "persistence_or_rebound": "Effects disappear after age 17 for marriage and age 18 for first birth in published version; delay operates through marriage",
        "completed_fertility": "NOT_REPORTED", "mechanism": "Compulsory attendance plus temporary marriage-market human-capital effect",
        "child_value_mechanism_status": "NOT_TESTED", "synthesis_status": "NARRATIVE_PERCENT_EFFECTS_TABLE_EXTRACTION_PENDING",
        "source_locator": "IZA PDF abstract; Tables 5-8; conclusion pp. 27-28",
        "pdf_path": "literature/pdfs/compulsory-education/W2108204833__effects-of-compulsory-schooling-laws-on-teenage-marriage-and-births-turkey.pdf",
    },
    {
        "paperId": "W2154210580", "title": "Does education reduce teen fertility? Evidence from compulsory schooling laws",
        "workstream": "TEMPO_COMPULSORY_SCHOOLING", "fulltext_decision": "INCLUDE",
        "design": "Canadian compulsory-schooling-law IV", "setting": "Canada",
        "reform": "Changes in provincial minimum school-leaving ages", "schooling_first_stage": "Strong law-induced schooling first stage; dropout-age increase raises attainment about 6-7 pp on attendance margin",
        "fertility_outcome": "First birth and number of children by ages 17 onward",
        "effect_summary": "Teen birth probability reduced about 2-3 pp; effects concentrated at ages 17-18",
        "persistence_or_rebound": "Negative effect disappears after ages 17-18; temporary delay",
        "completed_fertility": "NOT_REPORTED", "mechanism": "Strong incarceration/incapacitation pattern",
        "child_value_mechanism_status": "NOT_TESTED", "synthesis_status": "TEMPO_NUMERIC_SE_EXTRACTION_PENDING",
        "source_locator": "NBER PDF abstract; Tables 2-4; conclusion",
        "pdf_path": "literature/pdfs/compulsory-education/W2154210580__does-education-reduce-teen-fertility.pdf",
    },
    {
        "paperId": "W4409029977", "title": "The Causal Effects of Education on Age at Marriage and Marital Fertility",
        "workstream": "CHILD_ECONOMIC_VALUE_QUANTUM", "fulltext_decision": "INCLUDE_REDUCED_FORM_ONLY",
        "design": "Regression discontinuity at 1947 and 1972 English school-leaving reforms", "setting": "England and Wales",
        "reform": "Minimum school-leaving age raised by one year in 1947 and 1972",
        "schooling_first_stage": "Reform-scaled additional year; exact preferred first-stage coefficient not extracted here",
        "fertility_outcome": "First-marriage fertility; age at first marriage",
        "effect_summary": "1947 scaled fertility effect range -0.046 to +0.132 child; 1972 range -0.030 to +0.061; preferred estimates effectively zero",
        "persistence_or_rebound": "Completed marital fertility observed", "completed_fertility": "Precisely zero/non-trivial negative effects ruled out",
        "mechanism": "Prospective woman's own education; no child-work-value test",
        "child_value_mechanism_status": "WRONG_MECHANISM_OWN_SCHOOLING", "synthesis_status": "REDUCED_FORM_CONTEXT_NOT_DIRECT_MECHANISM",
        "source_locator": "PDF Tables A12-A13 and Figure 6 discussion pp. 18-20; conclusion p. 23",
        "pdf_path": "literature/pdfs/compulsory-education/W4409029977__the-causal-effects-of-education-on-age-at-marriage-and-marital-fertility.pdf",
    },
    {
        "paperId": "W2411634914", "title": "Is Education Always Reducing Fertility? Evidence from Compulsory Schooling Reforms",
        "workstream": "CHILD_ECONOMIC_VALUE_QUANTUM", "fulltext_decision": "INCLUDE_REDUCED_FORM_ONLY",
        "design": "Cross-country compulsory-reform IV", "setting": "England and seven Continental European countries",
        "reform": "Compulsory-schooling extensions implemented 1936-1975", "schooling_first_stage": "Mandatory schooling instruments; single-country first stages generally 0.22-0.40 years",
        "fertility_outcome": "Completed number of biological children and childlessness",
        "effect_summary": "Negative education-fertility effect in England; no fertility reduction or childlessness increase in Continental Europe",
        "persistence_or_rebound": "Completed cohort fertility observed", "completed_fertility": "England negative; Continental Europe null/nonnegative",
        "mechanism": "Prospective adult's own schooling; marriage-market and labor-supply channels",
        "child_value_mechanism_status": "WRONG_MECHANISM_OWN_SCHOOLING", "synthesis_status": "REDUCED_FORM_CONTEXT_TABLE_EXTRACTION_PENDING",
        "source_locator": "Author manuscript abstract and Sections 2-4; completed-fertility definition pp. 11-12",
        "pdf_path": "literature/pdfs/compulsory-education/W2411634914__is-education-always-reducing-fertility.pdf",
    },
    {
        "paperId": "W3212471012", "title": "Maternal education and child health: Causal evidence from Denmark",
        "workstream": "TEMPO_COMPULSORY_SCHOOLING", "fulltext_decision": "INCLUDE_ADJACENT_OUTCOME",
        "design": "Fuzzy regression discontinuity", "setting": "Denmark",
        "reform": "Compulsory schooling raised from 7 to 9 years in 1972", "schooling_first_stage": "Strong compulsory-margin first stage; preferred first-stage F about 118",
        "fertility_outcome": "Number of children, any child, and age at first birth",
        "effect_summary": "No effect on having children or number of children; age at first birth postponed about 0.5 year, marginally significant",
        "persistence_or_rebound": "Completed number of children measured at age 39", "completed_fertility": "No causal effect on number of children",
        "mechanism": "Prospective mother's own schooling; timing effect not specifically teenage incapacitation",
        "child_value_mechanism_status": "WRONG_MECHANISM_OWN_SCHOOLING", "synthesis_status": "ADJACENT_TEMPO_NOT_TEEN_SPECIFIC",
        "source_locator": "PDF Table 1; Tables 2-3 first stage; Table 6 and discussion",
        "pdf_path": "literature/pdfs/compulsory-education/W3212471012__maternal-education-and-child-health-denmark.pdf",
    },
    {
        "paperId": "W3125141375", "title": "Technological Progress and Economic Transformation",
        "workstream": "CHILD_ECONOMIC_VALUE_THEORY", "fulltext_decision": "INCLUDE_THEORY_COUNTEREVIDENCE",
        "design": "Calibrated macroeconomic theory", "setting": "United States historical transition",
        "reform": "Child-labor and compulsory-schooling laws discussed as alternative explanation",
        "schooling_first_stage": "Not an empirical policy first stage", "fertility_outcome": "Model fertility transition",
        "effect_summary": "Model links technological change, skill demand, child labor decline, and fertility decline",
        "persistence_or_rebound": "Not applicable", "completed_fertility": "MODEL_OUTCOME",
        "mechanism": "Child productivity/value mechanism, but argues child labor largely declined before binding federal law",
        "child_value_mechanism_status": "THEORY_RELEVANT_POLICY_CAUSATION_CHALLENGED", "synthesis_status": "THEORY_NARRATIVE",
        "source_locator": "PDF Section 4, especially pp. 27-28", "pdf_path": "literature/pdfs/compulsory-education/W3125141375__technological-progress-and-economic-transformation.pdf",
    },
]

ROB_FIELDS = [
    "paperId", "design", "confounding", "selection_or_sorting", "treatment_classification",
    "outcome_measurement", "missing_data", "selective_reporting", "overall_preliminary",
    "rationale", "status",
]

ROB = [
    ["W2169373049", "Law/cohort quasi-experiment", "SERIOUS", "MODERATE", "MODERATE", "LOW", "MODERATE", "MODERATE", "SERIOUS",
     "US law adoption may correlate with state trends; Norway is stronger but estimates need specification-level review.", "PRELIMINARY_FULLTEXT"],
    ["W2185731654", "RD", "LOW", "LOW", "LOW", "LOW", "LOW", "LOW", "LOW",
     "Sharp cohort cutoff, strong first stage, administrative births, extensive falsification; preferred-table verification still pending.", "PRELIMINARY_FULLTEXT"],
    ["W3006219298", "RD", "MODERATE", "MODERATE", "MODERATE", "LOW", "MODERATE", "LOW", "MODERATE",
     "Paper cannot fully exclude enrollment manipulation for Roma subgroup; conception-timing evidence strongly supports mechanism.", "PRELIMINARY_FULLTEXT"],
    ["W4385628385", "Donut-hole RD", "MODERATE", "MODERATE", "LOW", "LOW", "MODERATE", "MODERATE", "MODERATE",
     "Birth-date heaping motivates donut-hole design; age-specific and subgroup multiplicity require care.", "PRELIMINARY_FULLTEXT"],
    ["W4412362654", "IV staggered DiD", "SERIOUS", "MODERATE", "MODERATE", "LOW", "MODERATE", "MODERATE", "SERIOUS",
     "Exclusion restriction and staggered-policy comparisons are material; estimates identify own-human-capital channels, not pure incapacitation.", "PRELIMINARY_FULLTEXT"],
    ["W2186769068", "Sharp RD", "MODERATE", "LOW", "LOW", "MODERATE", "MODERATE", "MODERATE", "MODERATE",
     "RD is transparent, but household survey fertility measurement and non-monotonic age estimates limit precision.", "PRELIMINARY_FULLTEXT"],
    ["W2108204833", "Cohort policy discontinuity", "MODERATE", "MODERATE", "MODERATE", "LOW", "MODERATE", "MODERATE", "MODERATE",
     "Strong policy discontinuity and mechanism pattern; school-start assumptions and cohort trends require specification review.", "PRELIMINARY_FULLTEXT"],
    ["W2154210580", "Compulsory-law IV", "MODERATE", "MODERATE", "LOW", "LOW", "LOW", "LOW", "MODERATE",
     "Strong first stage and age-specific falsification pattern; provincial law endogeneity remains a possible concern.", "PRELIMINARY_FULLTEXT"],
    ["W4409029977", "RD", "LOW", "LOW", "LOW", "MODERATE", "MODERATE", "LOW", "MODERATE",
     "Large linked sample and robust RD intervals; linkage and marital-fertility measurement remain limitations.", "PRELIMINARY_FULLTEXT"],
    ["W2411634914", "Cross-country IV", "MODERATE", "MODERATE", "MODERATE", "LOW", "MODERATE", "MODERATE", "SERIOUS",
     "Multiple reforms and completed-fertility data are strengths; pooled exclusion restriction and heterogeneous reform contexts limit causal comparability.", "PRELIMINARY_FULLTEXT"],
    ["W3212471012", "Fuzzy RD", "LOW", "MODERATE", "LOW", "LOW", "LOW", "LOW", "MODERATE",
     "Strong first stage and administrative registers; donut-hole/cohort exclusions and marginal timing estimate warrant caution.", "PRELIMINARY_FULLTEXT"],
]


def write(path, fields, rows):
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main():
    write(EVIDENCE_OUT, EVIDENCE_FIELDS, ROWS)
    rob_rows = [dict(zip(ROB_FIELDS, row)) for row in ROB]
    write(ROB_OUT, ROB_FIELDS, rob_rows)
    print(f"wrote {len(ROWS)} accessible full-text evidence rows")
    print(f"wrote {len(rob_rows)} preliminary empirical risk-of-bias rows")


if __name__ == "__main__":
    main()
