#!/usr/bin/env python3
"""Build the post-RA full-text retrieval list for TICK-031.

Blank RA decisions approve the strict screen. RA corrections govern classification;
theory rows are retained for the chapter elsewhere but are not sent to the RA doing
quantitative extraction/meta-analysis. Known working-paper/published-paper variants
are collapsed to one preferred retrieval record.
"""

import csv
from pathlib import Path


SLUG = "child-labor-laws-and-schooling"
HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
SOURCE = REPO / "output" / f"{SLUG}-strict-focused-ra-review.csv"
OUTPUT = REPO / "output" / f"{SLUG}-metaanalysis-doi-retrieval.csv"

# The value is (canonical paperId, note). These are bibliographic versions of the
# same study, not independent estimates. Prefer the published article.
VERSION_ALIASES = {
    "W2122096529": (
        "W2411634914",
        "Two working-paper records collapsed into published article 10.1111/ecoj.12394.",
    ),
    "W2188242424": (
        "W2411634914",
        "Two working-paper records collapsed into published article 10.1111/ecoj.12394.",
    ),
    "W3024321219": (
        "W2154210580",
        "NBER working-paper version collapsed into published article 10.1016/j.jhealeco.2019.102268.",
    ),
}

FIELDS = [
    "retrieval_id",
    "identifier_status",
    "doi",
    "doi_url",
    "title",
    "year",
    "authors",
    "venue",
    "outcome_family",
    "estimand_cell",
    "evidence_type",
    "treatment",
    "outcome",
    "paperId",
    "alternate_paperIds",
    "version_note",
    "ra_status",
]


def clean(value):
    return (value or "").strip()


def main():
    with SOURCE.open(newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.DictReader(handle))

    unresolved = [
        row["paperId"]
        for row in rows
        if clean(row.get("ra_decision")).upper() in {"UNSURE_PI"}
    ]
    if unresolved:
        raise SystemExit(f"RA review still has unresolved rows: {unresolved}")

    canonical = {}
    alternates = {}
    notes = {}
    for row in rows:
        decision = clean(row.get("ra_decision")).upper()
        if decision == "EXCLUDE" or clean(row.get("retrieval_candidate")).upper() != "YES":
            continue

        effective_cell = clean(row.get("ra_corrected_estimand_cell")) or clean(row.get("estimand_cell"))
        if effective_cell == "THEORY" or clean(row.get("evidence_type")).lower() == "theory":
            continue
        if effective_cell not in {"PRIMARY_CS_QUANTUM", "PRIMARY_CL_QUANTUM", "PRIMARY_JOINT_QUANTUM", "TEMPO"}:
            raise SystemExit(f"unexpected quantitative estimand cell for {row['paperId']}: {effective_cell}")

        canonical_id, note = VERSION_ALIASES.get(row["paperId"], (row["paperId"], ""))
        if canonical_id != row["paperId"]:
            alternates.setdefault(canonical_id, []).append(row["paperId"])
            notes[canonical_id] = note
            continue
        canonical[canonical_id] = (row, effective_cell)

    missing_canonical = sorted(set(alternates) - set(canonical))
    if missing_canonical:
        raise SystemExit(f"version alias points to missing canonical rows: {missing_canonical}")

    out = []
    for canonical_id, (row, effective_cell) in canonical.items():
        doi = clean(row.get("doi")).lower()
        outcome_family = "FERTILITY_QUANTUM" if effective_cell.endswith("QUANTUM") else "FERTILITY_TEMPO"
        out.append(
            {
                "identifier_status": "DOI_RESOLVED" if doi else "TITLE_ONLY_NO_DOI",
                "doi": doi,
                "doi_url": f"https://doi.org/{doi}" if doi else "",
                "title": clean(row.get("title")),
                "year": clean(row.get("year")),
                "authors": clean(row.get("authors")),
                "venue": clean(row.get("venue")),
                "outcome_family": outcome_family,
                "estimand_cell": effective_cell,
                "evidence_type": clean(row.get("evidence_type")),
                "treatment": clean(row.get("treatment")),
                "outcome": clean(row.get("outcome")),
                "paperId": canonical_id,
                "alternate_paperIds": ";".join(alternates.get(canonical_id, [])),
                "version_note": notes.get(canonical_id, ""),
                "ra_status": "APPROVED_BLANK" if not clean(row.get("ra_decision")) else clean(row.get("ra_decision")).upper(),
            }
        )

    out.sort(key=lambda row: (row["outcome_family"], int(row["year"] or 0), row["title"].casefold()))
    for index, row in enumerate(out, 1):
        row["retrieval_id"] = f"CLS-{index:03d}"

    duplicate_dois = sorted({row["doi"] for row in out if sum(x["doi"] == row["doi"] for x in out) > 1})
    if duplicate_dois:
        raise SystemExit(f"duplicate DOI after study deduplication: {duplicate_dois}")

    with OUTPUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(out)

    counts = {family: sum(row["outcome_family"] == family for row in out) for family in {row["outcome_family"] for row in out}}
    print(f"wrote {len(out)} distinct studies -> {OUTPUT.relative_to(REPO)}")
    print(f"DOIs resolved: {sum(bool(row['doi']) for row in out)}/{len(out)}")
    print("outcome families:", ", ".join(f"{key}={counts[key]}" for key in sorted(counts)))
    print(f"collapsed version records: {sum(len(value) for value in alternates.values())}")


if __name__ == "__main__":
    main()
