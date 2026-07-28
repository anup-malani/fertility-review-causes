#!/usr/bin/env python3
"""TICK-049/053: compute the Wall 1 bleed-in rate over the stated sample.

The bleed-in rate is the share of the retrieved D.3.b literature whose exposure variable
measures environmental VALUES or BEHAVIOUR rather than ecological FEAR. It is the reason
the stated pool was sampled at random rather than extracted by convenience, and it is the
chapter's one genuinely new empirical claim about the field.

It is reported with a Wilson interval and with the realised sample coverage attached,
because a rate computed on a sample with heavy non-response is not an estimate of
anything. The stated-sample log set the non-response floor at two thirds.

Two rates are reported, not one, because the classification has a defensible strict
reading and a defensible broad reading and the choice moves the number a lot:
  strict — only `environmental_values_or_behaviour` counts as a bleed-in
  broad  — `mixed` counts too (composites that average fear with behaviour or knowledge,
           and physical-exposure designs whose narrated mechanism is economic)

Outputs:
  output/tables/climate-anxiety-eco-doomerism-bleed-in-rate.csv
"""
from __future__ import annotations

import csv
import math
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SLUG = "climate-anxiety-eco-doomerism"
STATED = ROOT / "extraction" / f"{SLUG}-effects-stated.csv"
REALIZED_STUDIES = ROOT / "extraction" / f"{SLUG}-studies.csv"
SAMPLE = ROOT / "extraction" / f"{SLUG}-stated-sample.csv"
OUT = ROOT / "output" / "tables" / f"{SLUG}-bleed-in-rate.csv"

STRICT = {"environmental_values_or_behaviour"}
BROAD = STRICT | {"mixed"}


def wilson(k: int, n: int, z: float = 1.959964) -> tuple[float, float]:
    """Wilson score interval — correct at small n, unlike the normal approximation."""
    if n == 0:
        return (0.0, 0.0)
    p = k / n
    d = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / d
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (max(0.0, centre - half), min(1.0, centre + half))


def main() -> None:
    # One classification per STUDY, not per effect row.
    by_study: dict[str, str] = {}
    for r in csv.DictReader(open(STATED)):
        by_study.setdefault(r["study_id"], r["wall1_class"])

    counts = Counter(by_study.values())
    n = len(by_study)
    k_strict = sum(v for c, v in counts.items() if c in STRICT)
    k_broad = sum(v for c, v in counts.items() if c in BROAD)

    sample_rows = list(csv.DictReader(open(SAMPLE)))
    selected = len(sample_rows)
    in_hand = sum(1 for r in sample_rows if r["pdf_in_hand"] == "yes")
    coverage = in_hand / selected if selected else 0.0

    rows = []
    for label, k, defn in (("strict", k_strict, "environmental_values_or_behaviour only"),
                           ("broad", k_broad, "environmental_values_or_behaviour + mixed")):
        lo, hi = wilson(k, n)
        rows.append({
            "track": "stated_intention", "reading": label, "definition": defn,
            "bleed_in": k, "studies_classified": n,
            "rate": f"{k / n:.3f}" if n else "",
            "ci95_lower": f"{lo:.3f}", "ci95_upper": f"{hi:.3f}",
            "sample_selected": selected, "sample_in_hand": in_hand,
            "sample_coverage": f"{coverage:.3f}",
            "coverage_above_two_thirds": "yes" if coverage >= 2 / 3 else "NO",
        })

    # Realized track, for comparison. Classified at the gate, not here.
    for label, k, defn in (("strict", 2, "Traylor & Chae, Ivanova & Ruttenauer"),
                           ("broad", 3, "+ Weychert (media exposure, not dread)")):
        lo, hi = wilson(k, 8)
        rows.append({
            "track": "realized_fertility", "reading": label, "definition": defn,
            "bleed_in": k, "studies_classified": 8, "rate": f"{k / 8:.3f}",
            "ci95_lower": f"{lo:.3f}", "ci95_upper": f"{hi:.3f}",
            "sample_selected": 8, "sample_in_hand": 8, "sample_coverage": "1.000",
            "coverage_above_two_thirds": "yes (census, not a sample)",
        })

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)

    print(f"stated sample: {n} studies classified, coverage {in_hand}/{selected} "
          f"({coverage:.0%}, floor 67%)")
    print("  class distribution:", dict(counts))
    for r in rows:
        print(f"  {r['track']:18} {r['reading']:6} {r['bleed_in']}/{r['studies_classified']} "
              f"= {r['rate']}  95% CI [{r['ci95_lower']}, {r['ci95_upper']}]")
    print(f"-> {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
