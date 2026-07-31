#!/usr/bin/env python3
"""Harmonise the C.2.c poolable effects to a common elasticity (TICK-055, pass 3).

The five poolable estimates arrive in four incompatible units: percent-per-$10,000, percent-per-
100,000-DKK, percent-per-percent, and births-per-1,000-per-10-percent. Nothing can be compared, let
alone pooled, until they are on one scale.

Target scale: **% change in fertility per 1% change in the housing price/wealth measure**, evaluated
at each study's own sample mean. Every baseline below was read from the study's own descriptive
statistics table -- read VISUALLY from the PDF where pdftotext could not render the table, which was
the case for both dollar-denominated studies.

Linearity caveat: converting a per-$10,000 effect into an elasticity at the mean assumes the effect
is locally linear in price. Dettling & Kearney state that assumption explicitly ("under the assumption
of linear effects"); it is imposed, not tested, and it is the main thing that could move these numbers.
"""

STUDIES = [
    # (short_cite, channel, effect_pct, unit_change_pct, baseline_note)
    ("Dettling & Kearney (US, IV)", "wealth_owner", +5.0, 10_000 / 162_356 * 100,
     "mean MSA home price $162,356 (Table 1, Aggregate Variables)"),
    ("Dettling & Kearney (US, IV)", "cost_nonowner", -2.4, 10_000 / 162_356 * 100,
     "same baseline"),
    ("Daysal et al. (Denmark)", "wealth_owner", +2.32, 100_000 / 978_070 * 100,
     "mean estimated home value at purchase 9.7807 x 100,000 DKK (Table 1, Summary Statistics)"),
    ("Ang et al. (China, RD)", "wealth_owner", +0.18, 1.0,
     "already reported as an elasticity"),
    ("Liu & Zhang (China, HPR)", "cost_prospective_buyer", -0.88 / 10.72 * 100, 10.0,
     "mean birth rate 10.72 per 1,000 in sample; effect -0.88 per 1,000"),
]

rows = []
for cite, ch, eff, unit, note in STUDIES:
    rows.append((cite, ch, eff / unit, eff, unit, note))

print("HARMONISED ELASTICITIES  (% change in fertility per 1% change in price/wealth)\n")
print(f"{'study':<32}{'channel':<24}{'elasticity':>11}   basis")
print("-" * 108)
for cite, ch, el, eff, unit, note in sorted(rows, key=lambda r: (r[1], -r[2])):
    print(f"{cite:<32}{ch:<24}{el:>+11.2f}   {eff:+.2f}% per {unit:.2f}% price change")

print("\nby channel:")
for ch in ("wealth_owner", "cost_nonowner", "cost_prospective_buyer"):
    els = [r[2] for r in rows if r[1] == ch]
    if els:
        print(f"  {ch:<24} n={len(els)}  range {min(els):+.2f} to {max(els):+.2f}")

print("\nbaselines used (all read from the study's own table):")
for cite, ch, el, eff, unit, note in rows:
    print(f"  {cite:<32} {note}")

import csv
with open("extraction/housing-costs-effects-harmonised.csv", "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["study", "channel", "elasticity_pct_per_pct", "reported_effect_pct",
                "implied_price_change_pct", "baseline_source", "linearity_assumed"])
    for cite, ch, el, eff, unit, note in rows:
        w.writerow([cite, ch, round(el, 3), eff, round(unit, 2), note,
                    "yes" if unit != 1.0 else "no"])
print("\n-> extraction/housing-costs-effects-harmonised.csv")
