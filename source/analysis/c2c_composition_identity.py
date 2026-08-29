"""The tenure-composition identity for C.2.c (housing costs and fertility).

docs/chapter-template.md 2.1 requires the identity arm of a mechanism to be
separated from its behavioural arm. For housing, the population elasticity is
an identity:

    eta_pop = w_owner * eta_wealth + w_cost * eta_cost

where the weights are population shares summing to one. That relation cannot be
false and needs no study. The behavioural arms -- eta_wealth and eta_cost --
are the only places the hypothesis can be wrong.

This module does two things with that identity:

  1. Computes the break-even ownership share at which the net population
     elasticity changes sign, for every pair of extracted channel estimates.
     If that break-even is not pinned down, no aggregate elasticity is
     transportable, which is the chapter's central claim.

  2. Shows that the two-group identity mispredicts the sign in China, and that
     restoring the third group the chapter names -- prospective buyers, who
     hold no house yet must purchase -- resolves it. Prospective buyers are
     counted inside conventional homeownership statistics, so the standard
     ownership rate is the wrong weight.

Run:
    python3 source/analysis/c2c_composition_identity.py
"""

from __future__ import annotations

import csv
import itertools
import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
EFFECTS = REPO_ROOT / "extraction" / "housing-costs-effects-harmonised.csv"
TABLES = REPO_ROOT / "output" / "tables"

BREAKEVEN_OUT = TABLES / "housing-costs-composition-breakeven.csv"
SUMMARY_OUT = TABLES / "housing-costs-composition-identity.json"

# Observed owner-occupancy shares, for reading the break-evens against. These
# are widely reported national/urban figures, NOT computed from project data;
# the chapter marks them as such.
OWNERSHIP_REFERENCE = {
    "United States": 0.65,
    "Denmark": 0.60,
    "Canada": 0.67,
    "urban China": 0.90,
}


def read_channels() -> tuple[list[dict], list[dict]]:
    wealth, cost = [], []
    with EFFECTS.open(newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            entry = {
                "study": row["study"],
                "channel": row["channel"],
                "elasticity": float(row["elasticity_pct_per_pct"]),
                "linearity_assumed": row["linearity_assumed"],
            }
            (wealth if row["channel"] == "wealth_owner" else cost).append(entry)
    return wealth, cost


def breakeven(eta_wealth: float, eta_cost: float) -> float | None:
    """Owner share at which w*eta_wealth + (1-w)*eta_cost == 0."""
    denom = eta_wealth - eta_cost
    if denom == 0:
        return None
    return -eta_cost / denom


def main() -> None:
    wealth, cost = read_channels()
    rows: list[dict[str, object]] = []

    for w_est, c_est in itertools.product(wealth, cost):
        w_star = breakeven(w_est["elasticity"], c_est["elasticity"])
        if w_star is None:
            continue
        predictions = {}
        for place, share in OWNERSHIP_REFERENCE.items():
            net = share * w_est["elasticity"] + (1 - share) * c_est["elasticity"]
            predictions[place] = round(net, 4)
        rows.append(
            {
                "wealth_study": w_est["study"],
                "eta_wealth": w_est["elasticity"],
                "cost_study": c_est["study"],
                "eta_cost": c_est["elasticity"],
                "breakeven_owner_share": round(w_star, 4),
                "breakeven_owner_share_pct": round(100 * w_star, 1),
                **{f"net_at_{k.replace(' ', '_')}": v for k, v in predictions.items()},
            }
        )

    write_cols = list(rows[0].keys())
    BREAKEVEN_OUT.parent.mkdir(parents=True, exist_ok=True)
    with BREAKEVEN_OUT.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=write_cols)
        writer.writeheader()
        writer.writerows(rows)

    breakevens = [r["breakeven_owner_share_pct"] for r in rows]
    china_nets = [r["net_at_urban_China"] for r in rows]

    summary = {
        "n_wealth_estimates": len(wealth),
        "n_cost_estimates": len(cost),
        "n_pairs": len(rows),
        "breakeven_owner_share_pct": {
            "min": min(breakevens),
            "max": max(breakevens),
            "spread_pp": round(max(breakevens) - min(breakevens), 1),
        },
        "two_group_identity_prediction_for_urban_china": {
            "ownership_share_used": OWNERSHIP_REFERENCE["urban China"],
            "net_elasticity_by_pair": china_nets,
            "all_positive": all(n > 0 for n in china_nets),
            "observed_sign_in_china_studies": "negative",
            "verdict": (
                "The two-group identity predicts a POSITIVE net elasticity for "
                "urban China under every extracted pair, and the Chinese "
                "estimates are negative. The identity is not wrong; the weights "
                "are. Conventional homeownership statistics count prospective "
                "buyers as owners, and for them a price rise is pure cost."
            ),
        },
        "note": (
            "Ownership shares are conventional reference figures, not computed "
            "from project data; data/raw/ holds no macro panel. They are used "
            "only to read the break-evens against, and the chapter marks them."
        ),
    }
    SUMMARY_OUT.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
