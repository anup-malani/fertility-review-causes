#!/usr/bin/env python3
"""Split Alexandra's approved focused review into two mechanism-oriented paper sets.

Set 1 corresponds to the original child-economic-value hypothesis. It includes its approved theory
papers plus quantum policy papers, but labels the latter as reduced-form pending full-text mechanism
verification. Set 2 contains the compulsory-schooling/teenage-birth stream nested under tempo
postponement. Bibliographic versions are collapsed and an explicitly dual-outcome study may appear
in both sets.
"""

import csv
from pathlib import Path


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
SOURCE = REPO / "output/child-labor-laws-and-schooling-strict-focused-ra-review.csv"

VALUE_OUTPUT = REPO / "output/compulsory-education-child-economic-value-ra-approved-papers.csv"
TEMPO_OUTPUT = REPO / "output/tempo-effects-birth-postponement-compulsory-schooling-ra-approved-papers.csv"

VERSION_ALIASES = {
    "W2122096529": "W2411634914",
    "W2188242424": "W2411634914",
    "W3024321219": "W2154210580",
}

DUAL_ROUTE = {
    "W2185731654": "Existing abstract explicitly reports both teen fertility and completed fertility.",
}

FIELDS = [
    "set_id", "mechanism_set", "parent_hypothesis_slug", "evidence_stream", "paperId", "doi",
    "title", "year", "authors", "venue", "effective_estimand_cell", "evidence_type",
    "evidence_role", "mechanism_status", "route_reason", "ra_decision", "ra_note",
    "alternate_paperIds", "shared_across_sets",
]


def clean(value):
    return (value or "").strip()


def read_approved():
    with SOURCE.open(newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.DictReader(handle))
    approved = []
    for row in rows:
        if clean(row.get("retrieval_candidate")).upper() != "YES":
            continue
        if clean(row.get("ra_decision")).upper() in {"EXCLUDE", "UNSURE_PI"}:
            continue
        row["effective_estimand_cell"] = (
            clean(row.get("ra_corrected_estimand_cell")) or clean(row.get("estimand_cell"))
        )
        approved.append(row)
    return approved


def collapse_versions(rows):
    by_id = {row["paperId"]: row for row in rows}
    alternates = {}
    for alternate, canonical in VERSION_ALIASES.items():
        if alternate in by_id and canonical in by_id:
            alternates.setdefault(canonical, []).append(alternate)
            del by_id[alternate]
    return list(by_id.values()), alternates


def base(row, alternates, shared):
    return {
        "paperId": row["paperId"],
        "doi": clean(row.get("doi")).lower(),
        "title": clean(row.get("title")),
        "year": clean(row.get("year")),
        "authors": clean(row.get("authors")),
        "venue": clean(row.get("venue")),
        "effective_estimand_cell": row["effective_estimand_cell"],
        "evidence_type": clean(row.get("evidence_type")),
        "ra_decision": clean(row.get("ra_decision")) or "APPROVED_BLANK",
        "ra_note": clean(row.get("ra_note")),
        "alternate_paperIds": ";".join(alternates.get(row["paperId"], [])),
        "shared_across_sets": "YES" if shared else "NO",
    }


def write(path, rows):
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main():
    rows, alternates = collapse_versions(read_approved())
    by_id = {row["paperId"]: row for row in rows}
    missing_dual = sorted(set(DUAL_ROUTE) - set(by_id))
    if missing_dual:
        raise SystemExit(f"Dual-route papers missing after RA filter: {missing_dual}")

    value_rows = []
    tempo_rows = []
    for row in rows:
        cell = row["effective_estimand_cell"]
        shared = row["paperId"] in DUAL_ROUTE
        if cell == "THEORY":
            out = base(row, alternates, shared)
            out.update({
                "mechanism_set": "DECREASED_CHILD_ECONOMIC_VALUE",
                "parent_hypothesis_slug": "compulsory-education-child-economic-value",
                "evidence_stream": "THEORY_AND_MECHANISM",
                "evidence_role": "THEORY_MECHANISM",
                "mechanism_status": "DIRECT_OR_FORMAL_THEORY_PENDING_FULLTEXT",
                "route_reason": "RA-approved theory record directly linking child labor/schooling policy and fertility.",
            })
            value_rows.append(out)
        elif cell in {"PRIMARY_CS_QUANTUM", "PRIMARY_CL_QUANTUM", "PRIMARY_JOINT_QUANTUM"}:
            out = base(row, alternates, shared)
            out.update({
                "mechanism_set": "DECREASED_CHILD_ECONOMIC_VALUE",
                "parent_hypothesis_slug": "compulsory-education-child-economic-value",
                "evidence_stream": "EMPIRICAL_QUANTUM",
                "evidence_role": "REDUCED_FORM_QUANTUM",
                "mechanism_status": "NOT_YET_SHOWN_FULLTEXT_REQUIRED",
                "route_reason": "RA-approved compulsory-policy record with a quantum outcome; child-value mechanism not established by title/abstract.",
            })
            value_rows.append(out)
        if cell == "TEMPO" or shared:
            out = base(row, alternates, shared)
            out.update({
                "mechanism_set": "DECREASED_TEEN_PREGNANCY_OR_BIRTH",
                "parent_hypothesis_slug": "tempo-effects-birth-postponement",
                "evidence_stream": "COMPULSORY_SCHOOLING_TEENAGE_BIRTHS",
                "evidence_role": "EMPIRICAL_TEMPO",
                "mechanism_status": "DIRECT_TEMPO_CANDIDATE_PENDING_FULLTEXT",
                "route_reason": DUAL_ROUTE.get(
                    row["paperId"],
                    "RA-approved tempo record on teenage pregnancy, birth, motherhood, or age at first birth.",
                ),
            })
            tempo_rows.append(out)

    value_rows.sort(key=lambda row: (row["evidence_role"], int(row["year"] or 0), row["title"].casefold()))
    tempo_rows.sort(key=lambda row: (int(row["year"] or 0), row["title"].casefold()))
    for index, row in enumerate(value_rows, 1):
        row["set_id"] = f"VALUE-{index:03d}"
    for index, row in enumerate(tempo_rows, 1):
        row["set_id"] = f"TEEN-{index:03d}"

    if len(value_rows) != 16 or len(tempo_rows) != 10:
        raise SystemExit(f"Unexpected set sizes after deduplication: value={len(value_rows)}, tempo={len(tempo_rows)}")
    write(VALUE_OUTPUT, value_rows)
    write(TEMPO_OUTPUT, tempo_rows)
    print(f"decreased child economic value: {len(value_rows)} papers")
    print(f"  theory/mechanism: {sum(r['evidence_role'] == 'THEORY_MECHANISM' for r in value_rows)}")
    print(f"  reduced-form quantum: {sum(r['evidence_role'] == 'REDUCED_FORM_QUANTUM' for r in value_rows)}")
    print(f"decreased teen pregnancy/birth: {len(tempo_rows)} papers")
    print(f"shared across sets: {sum(r['shared_across_sets'] == 'YES' for r in tempo_rows)}")


if __name__ == "__main__":
    main()
