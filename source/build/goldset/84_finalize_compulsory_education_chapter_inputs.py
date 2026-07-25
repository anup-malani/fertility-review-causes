#!/usr/bin/env python3
"""Build final chapter-support artifacts and the required RA readability gate.

This stage does not alter Alexandra's relevance or mechanism decisions. It summarizes the
documented citation-frame flow, joins study evidence to preliminary risk of bias, computes
an analytic sensitivity interval for Shanan's published 8% decomposition, and creates blank
human readability checklists for the two chapter drafts.
"""

from __future__ import annotations

import csv
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
OUTPUT = ROOT / "output"
EXTRACTION = ROOT / "extraction"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, fields: list[str], rows: list[dict[str, object]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def build_prisma() -> None:
    rows = [
        {"stage": "citation_frame_identified_and_deduplicated", "count": 1255, "stream": "shared", "interpretation": "Cold-start forward/backward citation frame; not a keyword-search PRISMA count."},
        {"stage": "ai_title_abstract_relevant", "count": 233, "stream": "shared", "interpretation": "Blinded AI screen."},
        {"stage": "ai_title_abstract_uncertain", "count": 128, "stream": "shared", "interpretation": "Blinded AI screen."},
        {"stage": "ai_title_abstract_not_relevant", "count": 894, "stream": "shared", "interpretation": "Blinded AI screen."},
        {"stage": "focused_ra_review_set", "count": 42, "stream": "shared", "interpretation": "Exception-focused RA sheet derived from the citation frame."},
        {"stage": "strict_retrieval_candidates", "count": 28, "stream": "shared", "interpretation": "Strict outcome/policy gate before publication-version collapse."},
        {"stage": "ra_approved_distinct", "count": 16, "stream": "child_economic_value", "interpretation": "Ten theory/mechanism and six empirical quantum papers."},
        {"stage": "ra_approved_distinct", "count": 10, "stream": "teenage_birth_postponement", "interpretation": "Empirical tempo papers."},
        {"stage": "ra_approved_union_distinct", "count": 25, "stream": "shared", "interpretation": "Geruso-Royer is shared across the two sets."},
        {"stage": "approved_full_texts_retrieved", "count": 25, "stream": "shared", "interpretation": "Complete approved-set retrieval."},
        {"stage": "post_review_primary_supplement", "count": 1, "stream": "child_economic_value", "interpretation": "Shanan (2023); not retroactively counted as RA-approved."},
    ]
    write_csv(
        OUTPUT / "compulsory-education-stream-prisma-accounting.csv",
        ["stage", "count", "stream", "interpretation"],
        rows,
    )


def build_included_studies() -> None:
    evidence = read_csv(EXTRACTION / "compulsory-education-accessible-fulltext-evidence.csv")
    rob = {row["paperId"]: row for row in read_csv(EXTRACTION / "compulsory-education-accessible-risk-of-bias-preliminary.csv")}
    fields = [
        "paperId", "title", "workstream", "design", "setting", "reform", "fertility_outcome",
        "effect_summary", "completed_fertility", "mechanism", "overall_preliminary_risk_of_bias",
        "source_locator", "pdf_path",
    ]
    rows: list[dict[str, object]] = []
    for row in evidence:
        rows.append({
            "paperId": row["paperId"],
            "title": row["title"],
            "workstream": row["workstream"],
            "design": row["design"],
            "setting": row["setting"],
            "reform": row["reform"],
            "fertility_outcome": row["fertility_outcome"],
            "effect_summary": row["effect_summary"],
            "completed_fertility": row["completed_fertility"],
            "mechanism": row["mechanism"],
            "overall_preliminary_risk_of_bias": rob.get(row["paperId"], {}).get("overall_preliminary", "NOT_APPLICABLE_THEORY"),
            "source_locator": row["source_locator"],
            "pdf_path": row["pdf_path"],
        })
    rows.append({
        "paperId": "W3174215957",
        "title": "The effect of compulsory schooling laws and child labor restrictions on fertility: evidence from the early twentieth century",
        "workstream": "CHILD_ECONOMIC_VALUE_POST_REVIEW_SUPPLEMENT",
        "design": "Historical state/cohort and neighboring-border quasi-experiment",
        "setting": "United States, 1880-1940 cohorts/censuses",
        "reform": "State compulsory-schooling and child-labor restrictions",
        "fertility_outcome": "Completed fertility and annual birth probability",
        "effect_summary": "Any-law exposure ages 20-30: -0.301 child (SE 0.044); annual birth probability: -0.0085 (SE 0.0011)",
        "completed_fertility": "NEGATIVE",
        "mechanism": "Value of children; lost child earnings and increased expected quality cannot be separated",
        "overall_preliminary_risk_of_bias": "SERIOUS",
        "source_locator": "Published PDF Tables 2, 4-5, 7-8, 11; Sections 5-9",
        "pdf_path": "literature/pdfs/compulsory-education/W3174215957__shanan-compulsory-schooling-child-labor-fertility.pdf",
    })
    write_csv(OUTPUT / "compulsory-education-included-studies.csv", fields, rows)


def build_shanan_scaling() -> None:
    exposure_change = 1.00 - 0.52
    effect_pp = 0.85
    effect_se_pp = 0.11
    observed_decline_pp = 18.0 - 13.0
    share = exposure_change * effect_pp / observed_decline_pp
    share_se = exposure_change * effect_se_pp / observed_decline_pp
    lower = share - 1.96 * share_se
    upper = share + 1.96 * share_se
    row = {
        "study": "Shanan (2023)",
        "target": "1900-1930 annual birth-probability decline among 30-year-old native-born US women",
        "exposure_change": f"{exposure_change:.2f}",
        "effect_percentage_points": f"{effect_pp:.2f}",
        "effect_se_percentage_points": f"{effect_se_pp:.2f}",
        "observed_decline_percentage_points": f"{observed_decline_pp:.2f}",
        "attributable_share": f"{share:.4f}",
        "analytic_se": f"{share_se:.4f}",
        "analytic_95ci_lower": f"{lower:.4f}",
        "analytic_95ci_upper": f"{upper:.4f}",
        "protocol_threshold": "0.10",
        "point_estimate_threshold_result": "BELOW_THRESHOLD",
        "interval_relation_to_threshold": "UPPER_BOUND_ABOVE_THRESHOLD" if upper >= 0.10 else "ENTIRE_INTERVAL_BELOW_THRESHOLD",
        "interval_method": "Delta-method propagation of reported coefficient SE; exposure and denominator treated as fixed",
        "protocol_caveat": "Sensitivity interval only; not the protocol-preferred bootstrap CI and not a TFR decomposition",
    }
    write_csv(
        OUTPUT / "compulsory-education-shanan-demographic-significance.csv",
        list(row),
        [row],
    )


def chapter_sections(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    return re.findall(r"^## (.+)$", text, flags=re.MULTILINE)


def build_readability_gate() -> None:
    chapters = [
        OUTPUT / "chapters" / "compulsory-education-child-economic-value.md",
        OUTPUT / "chapters" / "tempo-effects-birth-postponement.md",
    ]
    rows: list[dict[str, object]] = []
    for chapter in chapters:
        for section in chapter_sections(chapter):
            rows.append({
                "chapter": chapter.name,
                "section": section,
                "ai_precheck": "READY_FOR_HUMAN_REVIEW",
                "ra_readability_decision": "",
                "ra_issue_type": "",
                "ra_note": "",
                "needs_pi_decision": "",
            })
    write_csv(
        OUTPUT / "compulsory-education-chapters-lay-readability-review.csv",
        ["chapter", "section", "ai_precheck", "ra_readability_decision", "ra_issue_type", "ra_note", "needs_pi_decision"],
        rows,
    )


def main() -> None:
    build_prisma()
    build_included_studies()
    build_shanan_scaling()
    build_readability_gate()
    print("wrote PRISMA accounting, included studies, Shanan scaling, and readability gate")


if __name__ == "__main__":
    main()
