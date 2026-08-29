"""Diagnostics required by docs/chapter-template.md for the OAS chapter.

The chapter template (Layer 2) requires three checks that the original OAS
synthesis did not run:

  * 2.2  the naive-estimator / weight-concentration check -- who actually
         carries the pooled estimate, and is the disagreement between studies
         about the *estimator* or about the world?
  * 2.3  the attrition ledger between the counted event and the
         demographically relevant quantity;
  * 2.4  the units check (S4) before any arithmetic, and the endogeneity of
         the mechanism to the phenomenon.

This module computes the parts of those checks that are derivable from files
already in the repository, and writes them to output/tables/ so the chapter
quotes generated numbers rather than retyped ones.

It deliberately does NOT invent a TFR denominator. The UN TFR panel used by
oas_transition_classification.py lives outside this repository, so the
corrected slope-sufficiency shares cannot be computed here; what this script
does instead is show that the denominator actually used is a within-window
movement rather than the phenomenon, and report the arithmetic consequences.

Run:
    python3 source/analysis/oas_synthesis_diagnostics.py
"""

from __future__ import annotations

import csv
import json
from decimal import Decimal
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
TABLES = REPO_ROOT / "output" / "tables"

HARMONIZED_PATH = TABLES / "old-age-security-pension-crowdout-harmonized-effects.csv"
POOLED_PATH = TABLES / "old-age-security-pension-crowdout-outcome-specific-pooled-estimates.csv"
SLOPE_PATH = TABLES / "old-age-security-pension-crowdout-cell-c-slope-sufficiency.csv"
STUDIES_PATH = (
    REPO_ROOT / "extraction" / "old-age-security-pension-crowdout-studies.csv"
)

WEIGHTS_OUT = TABLES / "old-age-security-pension-crowdout-pool-weight-concentration.csv"
DENOM_OUT = TABLES / "old-age-security-pension-crowdout-slope-denominator-check.csv"
SENSITIVITY_OUT = TABLES / "old-age-security-pension-crowdout-pool-exclusion-sensitivity.csv"
UNITS_OUT = TABLES / "old-age-security-pension-crowdout-units-check.csv"
SUMMARY_OUT = TABLES / "old-age-security-pension-crowdout-synthesis-diagnostics.json"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def _num(value: str) -> float | None:
    value = (value or "").strip()
    if not value:
        return None
    try:
        return float(value)
    except ValueError:
        return None


# ---------------------------------------------------------------------------
# 2.2  Weight concentration in the outcome-specific pools
# ---------------------------------------------------------------------------


def pool_weight_concentration() -> tuple[list[dict[str, object]], dict[str, object]]:
    """Recover the inverse-variance weight each study carries in each pool.

    The pooled estimates are fixed-effect inverse-variance summaries, so a
    study's influence is 1/se^2 relative to the sum. Because the studies do
    not share a treatment scale, that weight is set by the units in which each
    paper happened to measure its treatment, not by study quality or by how
    directly the study speaks to the estimand. This function makes the
    resulting concentration visible.
    """
    harmonized = {r["effect_id"]: r for r in read_csv(HARMONIZED_PATH)}
    studies = {r["study_id"]: r for r in read_csv(STUDIES_PATH)}

    rows: list[dict[str, object]] = []
    summary: dict[str, object] = {}

    for pool in read_csv(POOLED_PATH):
        effect_ids = [e for e in pool["included_effect_ids"].split(";") if e]
        pooled_effect = _num(pool["pooled_effect"])

        contributions: list[dict[str, object]] = []
        total_weight = 0.0
        for effect_id in effect_ids:
            row = harmonized.get(effect_id, {})
            effect = _num(row.get("effect_oriented_more_oas", ""))
            se = _num(row.get("se_oriented_more_oas", ""))
            if effect is None or se is None or se == 0:
                continue
            weight = 1.0 / (se**2)
            total_weight += weight
            contributions.append(
                {
                    "effect_id": effect_id,
                    "study_id": row.get("study_id", ""),
                    "effect_oriented_more_oas": effect,
                    "se_oriented_more_oas": se,
                    "treatment_scale_harmonized": row.get(
                        "treatment_scale_harmonized", ""
                    ),
                    "raw_weight": weight,
                }
            )

        # Reproduce the pooled estimate as an arithmetic check on this script.
        recomputed = (
            sum(c["raw_weight"] * c["effect_oriented_more_oas"] for c in contributions)
            / total_weight
            if total_weight
            else None
        )

        for contribution in contributions:
            share = contribution["raw_weight"] / total_weight
            study = studies.get(contribution["study_id"], {})
            rows.append(
                {
                    "pooled_group": pool["pooled_group"],
                    "outcome_family": pool["outcome_family"],
                    "study_id": contribution["study_id"],
                    "effect_id": contribution["effect_id"],
                    "country_or_region": study.get("country_or_region", ""),
                    "treatment_scale_original": study.get("treatment_or_exposure", ""),
                    "treatment_scale_harmonized": contribution[
                        "treatment_scale_harmonized"
                    ],
                    "effect_oriented_more_oas": round(
                        contribution["effect_oriented_more_oas"], 8
                    ),
                    "se_oriented_more_oas": round(contribution["se_oriented_more_oas"], 8),
                    "inverse_variance_weight": round(contribution["raw_weight"], 4),
                    "weight_share": round(share, 6),
                    "weight_share_pct": round(100 * share, 2),
                }
            )

        ranked = sorted(rows_for(rows, pool["pooled_group"]), key=lambda r: -r["weight_share"])
        top_two = sum(r["weight_share"] for r in ranked[:2])
        summary[pool["pooled_group"]] = {
            "n_studies_reported": int(pool["n_studies"]),
            "n_studies_with_usable_weight": len(contributions),
            "pooled_effect_reported": pooled_effect,
            "pooled_effect_recomputed": None if recomputed is None else round(recomputed, 8),
            "reproduces_reported_pool": (
                recomputed is not None
                and pooled_effect is not None
                and abs(recomputed - pooled_effect) < 1e-6
            ),
            "top_two_weight_share_pct": round(100 * top_two, 2),
            "top_two_studies": [r["study_id"] for r in ranked[:2]],
            "least_weighted_study": ranked[-1]["study_id"] if ranked else None,
            "least_weighted_share_pct": ranked[-1]["weight_share_pct"] if ranked else None,
            "distinct_treatment_scales": pool["n_treatment_scales"],
        }

    return rows, summary


def rows_for(rows: list[dict[str, object]], pooled_group: str) -> list[dict[str, object]]:
    return [r for r in rows if r["pooled_group"] == pooled_group]


# ---------------------------------------------------------------------------
# 2.4  What denominator does the Cell C slope-sufficiency screen actually use?
# ---------------------------------------------------------------------------


def slope_denominator_check() -> tuple[list[dict[str, object]], dict[str, object]]:
    """Audit the denominator in the Cell C slope-sufficiency screen.

    The screen divides each availability-oriented effect by the TFR change
    *inside the study window*. The chapter's target phenomenon is the SDT
    decline, which is a much larger quantity. Dividing by the in-window change
    therefore does not answer "what share of the phenomenon does this
    mechanism explain"; it answers "how big is this effect relative to a few
    years of local drift". A share above 100% is the diagnostic: no mechanism
    accounts for more than all of the thing it explains, so a share above 1
    identifies a denominator that is not the phenomenon.
    """
    rows: list[dict[str, object]] = []
    impossible = 0
    computed = 0

    for row in read_csv(SLOPE_PATH):
        share = _num(row["effect_share_of_observed_decline"])
        decline = _num(row["observed_tfr_decline"])
        effect = _num(row["availability_oriented_effect"])
        tfr_start = _num(row["tfr_start"])
        tfr_end = _num(row["tfr_end"])

        if share is None:
            verdict = "no_denominator_tfr_did_not_decline_in_window"
        elif share > 1:
            verdict = "impossible_as_a_share_denominator_is_not_the_phenomenon"
            impossible += 1
            computed += 1
        else:
            verdict = "share_of_in_window_movement_not_of_the_phenomenon"
            computed += 1

        rows.append(
            {
                "effect_id": row["effect_id"],
                "country_or_region": row["country_or_region"],
                "window": f"{row['period_start']}-{row['period_end']}",
                "harmonized_outcome_unit": row["harmonized_outcome_unit"],
                "availability_oriented_effect": effect,
                "denominator_used": decline,
                "denominator_definition": "in_window_tfr_change",
                "tfr_start": tfr_start,
                "tfr_end": tfr_end,
                "reported_share": share,
                "reported_share_pct": None if share is None else round(100 * share, 1),
                "reported_label": row["slope_sufficiency_label"],
                "unit_mismatch": (
                    "yes_probability_effect_over_tfr_denominator"
                    if row["harmonized_outcome_unit"] == "probability_of_birth"
                    else "no_both_births_per_woman"
                ),
                "denominator_verdict": verdict,
            }
        )

    summary = {
        "n_rows": len(rows),
        "n_with_computed_share": computed,
        "n_shares_above_100pct": impossible,
        "n_unit_mismatched": sum(
            1 for r in rows if r["unit_mismatch"].startswith("yes")
        ),
        "largest_denominator_used": max(
            (r["denominator_used"] for r in rows if r["denominator_used"] is not None),
            default=None,
        ),
        "denominator_is_the_phenomenon": False,
        "note": (
            "Every denominator is an in-window TFR change of about 0.1 births. "
            "The SDT decline the chapter must explain is roughly an order of "
            "magnitude larger, so every reported share is inflated by roughly "
            "that factor. Recomputing requires the UN TFR panel referenced by "
            "oas_transition_classification.py, which is not reachable from "
            "this repository."
        ),
    }
    return rows, summary


# ---------------------------------------------------------------------------
# 2.2  Does the pooled sign survive the orientation rulings?
# ---------------------------------------------------------------------------


def exclusion_sensitivity() -> list[dict[str, object]]:
    """Re-pool including estimates that share a pool's unit but were excluded.

    Some effects were dropped from the pools by an orientation ruling rather
    than by a units problem -- most importantly the estimates coded
    `not_oriented_broader_social_spending_mechanism`. Those rulings may well be
    right, but a ruling that removes a precise estimate of the opposite sign is
    doing the work the pooled number appears to be doing, and the template's
    "resolve disagreements, do not average them" rule requires it to be shown
    rather than buried in a poolability flag.
    """
    harmonized = read_csv(HARMONIZED_PATH)
    by_id = {r["effect_id"]: r for r in harmonized}
    rows: list[dict[str, object]] = []

    for pool in read_csv(POOLED_PATH):
        unit = pool["harmonized_outcome_unit"]
        included = [e for e in pool["included_effect_ids"].split(";") if e]

        # Candidates: same mechanism cell AND same harmonised unit, with a
        # usable effect and SE, that the pool nonetheless leaves out. Cell C is
        # excluded here on purpose: the grandparental-childcare channel is a
        # different estimand with the opposite predicted sign, so the chapter
        # is right to keep it in its own track and re-pooling it would be a
        # category error rather than a sensitivity.
        candidates = []
        for row in harmonized:
            if row["effect_id"] in included:
                continue
            if row.get("mechanism_cell") != pool["mechanism_cell"]:
                continue
            if row.get("harmonized_outcome_unit") != unit:
                continue
            effect = _num(row.get("effect_harmonized", ""))
            se = _num(row.get("se_harmonized", ""))
            if effect is None or se is None or se == 0:
                continue
            candidates.append((row, effect, se))

        base = []
        for effect_id in included:
            row = by_id.get(effect_id, {})
            effect = _num(row.get("effect_oriented_more_oas", ""))
            se = _num(row.get("se_oriented_more_oas", ""))
            if effect is not None and se:
                base.append((effect, se))

        for row, effect, se in candidates:
            combined = base + [(effect, se)]
            total = sum(1 / s**2 for _, s in combined)
            repooled = sum((1 / s**2) * e for e, s in combined) / total
            added_share = (1 / se**2) / total
            reported = _num(pool["pooled_effect"])
            rows.append(
                {
                    "pooled_group": pool["pooled_group"],
                    "harmonized_outcome_unit": unit,
                    "excluded_effect_id": row["effect_id"],
                    "excluded_study_id": row.get("study_id", ""),
                    "exclusion_reason": row.get("orientation_method", "")
                    or row.get("poolability_reason", ""),
                    "excluded_effect_as_reported": round(effect, 6),
                    "excluded_se": round(se, 6),
                    "weight_share_if_included_pct": round(100 * added_share, 2),
                    "pooled_effect_as_published": reported,
                    "pooled_effect_if_included": round(repooled, 8),
                    "sign_flips": (
                        reported is not None and (reported < 0) != (repooled < 0)
                    ),
                }
            )

    return rows


# ---------------------------------------------------------------------------
# 2.4 / S4  Units check and break-even denominators
# ---------------------------------------------------------------------------

# Verdict bands from docs/chapter-template.md 2.4, as shares of the phenomenon.
BANDS = [
    ("NEGLIGIBLE", 0.00, 0.05),
    ("MINOR", 0.05, 0.20),
    ("SUBSTANTIAL", 0.20, 0.50),
    ("DOMINANT", 0.50, None),
]

# Mechanism magnitudes the chapter could offer, in births per woman, each with
# the most favourable dose assumption available in the extracted evidence.
MECHANISM_MAGNITUDES = [
    {
        "label": "Cell A pooled completed-fertility summary",
        "births_per_woman": 0.067672,
        "dose_assumption": (
            "the pooled contrast itself, which mixes a pension expansion, a "
            "pension cut and a participation IV and therefore has no single dose"
        ),
        "source": "outcome-specific-pooled-estimates.csv",
    },
    {
        "label": "Largest per-person Cell A estimate (Shen, rural China NRPS)",
        "births_per_woman": 0.169,
        "dose_assumption": (
            "every woman in the population moved from no pension to NRPS "
            "participation -- the most generous dose the evidence permits"
        ),
        "source": "effects.csv shen_zheng_yang_2020_china_nrps_e01",
    },
    {
        "label": "Cell C Netherlands reduced-form (Ilciukas)",
        "births_per_woman": 0.056,
        "dose_assumption": "the 2006 Dutch pension reform as assigned",
        "source": "cell-c-slope-sufficiency.csv ilciukas_e01",
    },
    {
        "label": "Cell C Australia grandmother eligibility (Akyol and Atalay)",
        "births_per_woman": 0.067,
        "dose_assumption": "maternal grandmother age-pension eligibility",
        "source": "cell-c-slope-sufficiency.csv akyol_atalay_e02",
    },
]


def units_check() -> list[dict[str, object]]:
    """S4: what denominator would each mechanism magnitude need to matter?

    The chapter cannot compute decomposition shares without the UN TFR panel,
    which is not reachable from this repository. It can, however, invert the
    question: for a mechanism that offers X births per woman, how large can the
    phenomenon be before X stops clearing a given verdict band? That is
    computable from X alone, and it is the form of the units check that does
    not require importing an outside number.
    """
    rows: list[dict[str, object]] = []
    for item in MECHANISM_MAGNITUDES:
        magnitude = item["births_per_woman"]
        row: dict[str, object] = {
            "mechanism_magnitude_label": item["label"],
            "mechanism_births_per_woman": magnitude,
            "dose_assumption": item["dose_assumption"],
            "source": item["source"],
        }
        for name, low, high in BANDS:
            # Largest phenomenon (in births) for which this magnitude still
            # reaches at least the band's lower edge.
            row[f"max_phenomenon_births_to_reach_{name}"] = (
                None if low == 0 else round(magnitude / low, 3)
            )
        rows.append(row)
    return rows


def main() -> None:
    weight_rows, weight_summary = pool_weight_concentration()
    write_csv(
        WEIGHTS_OUT,
        weight_rows,
        [
            "pooled_group",
            "outcome_family",
            "study_id",
            "effect_id",
            "country_or_region",
            "treatment_scale_original",
            "treatment_scale_harmonized",
            "effect_oriented_more_oas",
            "se_oriented_more_oas",
            "inverse_variance_weight",
            "weight_share",
            "weight_share_pct",
        ],
    )

    denom_rows, denom_summary = slope_denominator_check()
    write_csv(
        DENOM_OUT,
        denom_rows,
        [
            "effect_id",
            "country_or_region",
            "window",
            "harmonized_outcome_unit",
            "availability_oriented_effect",
            "denominator_used",
            "denominator_definition",
            "tfr_start",
            "tfr_end",
            "reported_share",
            "reported_share_pct",
            "reported_label",
            "unit_mismatch",
            "denominator_verdict",
        ],
    )

    sensitivity_rows = exclusion_sensitivity()
    write_csv(
        SENSITIVITY_OUT,
        sensitivity_rows,
        [
            "pooled_group",
            "harmonized_outcome_unit",
            "excluded_effect_id",
            "excluded_study_id",
            "exclusion_reason",
            "excluded_effect_as_reported",
            "excluded_se",
            "weight_share_if_included_pct",
            "pooled_effect_as_published",
            "pooled_effect_if_included",
            "sign_flips",
        ],
    )

    units_rows = units_check()
    write_csv(
        UNITS_OUT,
        units_rows,
        list(units_rows[0].keys()),
    )

    summary = {
        "pool_weight_concentration": weight_summary,
        "units_check": units_rows,
        "slope_denominator_check": denom_summary,
        "exclusion_sensitivity": {
            "n_candidates": len(sensitivity_rows),
            "n_that_flip_the_pooled_sign": sum(
                1 for r in sensitivity_rows if r["sign_flips"]
            ),
            "rows": sensitivity_rows,
        },
    }
    SUMMARY_OUT.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
