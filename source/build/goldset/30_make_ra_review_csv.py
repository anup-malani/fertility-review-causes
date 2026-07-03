#!/usr/bin/env python3
"""
Step 30 - Build the RA review CSV from the finalized GACS meta-analysis-ready set.

Input : {slug}-metaanalysis-ready-final.json plus scoring/screening metadata
Output: temp/{slug}-ra-review.csv
        temp/{slug}-unresolved-audit.csv

The RA review sheet excludes records whose DOI identity is not trusted. Unresolved/title-keyed
records are routed to the audit sheet first, because RA review should not treat unverified
paper identities as normal review candidates.
"""
from pathlib import Path

from ra_review_csv import build_ra_review_csvs


SLUG = "old-age-security-pension-crowdout"


def repo_root():
    return Path(__file__).resolve().parents[3]


def main():
    root = repo_root()
    result = build_ra_review_csvs(
        logs_dir=root / "literature" / "search-logs",
        output_dir=root / "temp",
        slug=SLUG,
    )
    print(
        f"{result['total']} finalized records -> {result['review']} RA-review rows, "
        f"{result['audit']} unresolved audit rows"
    )
    print(f"RA review -> {result['review_path']}")
    print(f"Unresolved audit -> {result['audit_path']}")


if __name__ == "__main__":
    main()
