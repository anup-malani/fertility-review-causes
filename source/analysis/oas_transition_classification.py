#!/usr/bin/env python3
"""Build TFR-based transition classifications for the OAS chapter."""

from __future__ import annotations

import csv
from pathlib import Path


SLUG = "old-age-security-pension-crowdout"
ROOT = Path(__file__).resolve().parents[2]
PROXIMATE_ROOT = ROOT.parent / "proximate-causes"
UN_TFR_PATH = PROXIMATE_ROOT / "code" / "raw" / "UN" / "UN_TFR.csv"
ASFR_BO_PATH = PROXIMATE_ROOT / "created" / "ASFR" / "ASFR_BO_merged.csv"
REPLACEMENT_TFR = 2.1

COUNTRY_ALIASES = {
    "United States": "United States of America",
    "Imperial Germany": "Germany",
}

POLICY_CONSTRAINED_COUNTRIES = {"China"}

OUTPUT_COLUMNS = [
    "study_id",
    "country_or_region",
    "tfr_country",
    "period_start",
    "period_end",
    "primary_outcome_family",
    "tfr_start_year",
    "tfr_start",
    "replacement_status_start",
    "tfr_end_year",
    "tfr_end",
    "replacement_status_end",
    "derived_period_target_relevance_tfr",
    "policy_constrained_low_fertility",
    "needs_human_review",
    "tfr_source",
    "classification_basis",
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


def _format_float(value: float | None) -> str:
    if value is None:
        return ""
    return f"{value:.4f}".rstrip("0").rstrip(".")


def canonical_country(country_or_region: str) -> str:
    return COUNTRY_ALIASES.get(country_or_region, country_or_region)


def load_un_tfr(path: Path = UN_TFR_PATH) -> dict[tuple[str, int], float]:
    tfr: dict[tuple[str, int], float] = {}
    for row in read_csv(path):
        value = (row.get("Value") or "").strip()
        if not value:
            continue
        tfr[(row["Country or Area"], int(row["Year(s)"]))] = float(value)
    return tfr


def load_asfr_tfr(path: Path = ASFR_BO_PATH) -> dict[tuple[str, int], float]:
    """Compute TFR from parity-specific ASFR rows.

    Values are five-year age-bin ASFRs by birth order, so TFR is 5 times the
    country-year sum across age groups and birth orders.
    """
    tfr: dict[tuple[str, int], float] = {}
    for row in read_csv(path):
        value = (row.get("Value") or "").strip()
        if not value:
            continue
        key = (row["Country or Area"], int(row["Year"]))
        tfr[key] = tfr.get(key, 0.0) + (float(value) * 5)
    return tfr


def nearest_tfr_in_window(
    tfr: dict[tuple[str, int], float],
    country: str,
    start: int,
    end: int,
    *,
    prefer: str,
) -> tuple[int, float] | tuple[None, None]:
    years = sorted(year for c, year in tfr if c == country and start <= year <= end)
    if not years:
        return None, None
    year = years[0] if prefer == "start" else years[-1]
    return year, tfr[(country, year)]


def replacement_status(tfr: float | None) -> str:
    if tfr is None:
        return "missing_tfr"
    if tfr < REPLACEMENT_TFR:
        return "below_replacement"
    return "above_replacement"


def classify_replacement_window(
    tfr_start: float | None,
    tfr_end: float | None,
    *,
    primary_outcome_family: str,
) -> dict[str, str]:
    start_status = replacement_status(tfr_start)
    end_status = replacement_status(tfr_end)
    if start_status == "missing_tfr" or end_status == "missing_tfr":
        classification = "unclassified_no_tfr"
    elif start_status == "above_replacement" and end_status == "above_replacement":
        classification = "FDT"
    elif start_status == "below_replacement" and end_status == "below_replacement":
        classification = "SDT"
    elif start_status == "above_replacement" and end_status == "below_replacement":
        classification = "FDT|SDT"
    else:
        classification = "SDT|FDT_reverse_crossing"

    if primary_outcome_family == "non_fertility" and classification != "unclassified_no_tfr":
        classification = f"{classification}_contextual"

    return {
        "replacement_status_start": start_status,
        "replacement_status_end": end_status,
        "derived_period_target_relevance_tfr": classification,
    }


def _lookup_window_tfr(
    tfr: dict[tuple[str, int], float], country: str, start: int, end: int
) -> tuple[tuple[int, float] | tuple[None, None], tuple[int, float] | tuple[None, None]]:
    start_value = nearest_tfr_in_window(tfr, country, start, end, prefer="start")
    end_value = nearest_tfr_in_window(tfr, country, start, end, prefer="end")
    return start_value, end_value


def classify_study_row(
    row: dict[str, str],
    tfr: dict[tuple[str, int], float],
    *,
    source_label: str = "UN_TFR.csv",
) -> dict[str, str]:
    country = canonical_country(row["country_or_region"])
    start = int(row["period_start"])
    end = int(row["period_end"])
    (start_year, tfr_start), (end_year, tfr_end) = _lookup_window_tfr(
        tfr, country, start, end
    )
    classification = classify_replacement_window(
        tfr_start,
        tfr_end,
        primary_outcome_family=row.get("primary_outcome_family", ""),
    )
    missing = tfr_start is None or tfr_end is None
    policy_constrained = country in POLICY_CONSTRAINED_COUNTRIES and not missing
    basis = (
        "No TFR observation in the study window; do not infer above/below replacement from this source."
        if missing
        else (
            f"{country} TFR is {classification['replacement_status_start']} at the first "
            f"available in-window year and {classification['replacement_status_end']} at "
            "the last available in-window year."
        )
    )
    if policy_constrained:
        basis += " China is marked policy-constrained for SDT interpretation."

    return {
        "study_id": row["study_id"],
        "country_or_region": row["country_or_region"],
        "tfr_country": country,
        "period_start": row["period_start"],
        "period_end": row["period_end"],
        "primary_outcome_family": row.get("primary_outcome_family", ""),
        "tfr_start_year": "" if start_year is None else str(start_year),
        "tfr_start": _format_float(tfr_start),
        "tfr_end_year": "" if end_year is None else str(end_year),
        "tfr_end": _format_float(tfr_end),
        "policy_constrained_low_fertility": "yes" if policy_constrained else "no",
        "needs_human_review": "yes" if missing or policy_constrained else "no",
        "tfr_source": source_label,
        "classification_basis": basis,
        **classification,
    }


def write_transition_classification(
    input_path: Path,
    output_path: Path,
    tfr: dict[tuple[str, int], float],
    *,
    source_label: str = "UN_TFR.csv",
) -> None:
    rows = [
        classify_study_row(row, tfr, source_label=source_label)
        for row in read_csv(input_path)
    ]
    write_csv(output_path, rows, OUTPUT_COLUMNS)


def main() -> None:
    input_path = ROOT / "extraction" / f"{SLUG}-target-period-relevance.csv"
    output_path = ROOT / "output" / "tables" / f"{SLUG}-tfr-transition-classification.csv"
    write_transition_classification(input_path, output_path, load_un_tfr())


if __name__ == "__main__":
    main()
