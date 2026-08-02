#!/usr/bin/env python3
"""Second-pass screen of the C.2.c UNCERTAIN records using title + abstract.

The first pass ran on titles alone and left 92 records unrouted -- correctly, because a title like
"Housing and Fertility" does not say whether the treatment is a price, a tenure status, or a housing
expenditure, and price-vs-tenure is exactly what the 2026-07-31 ruling turns on.

This pass looks for the TREATMENT in the abstract. Rules are ordered by how decisive the signal is for
the ruling: an explicit price/rent/wealth treatment routes to a PRIMARY cell; a tenure-only or
condition-only treatment routes to the tenure/space cells, which the ruling demotes; an outcome that
is not fertility routes out.

Still provisional. Whether an estimate conditions on tenure, and whether it speaks to tempo or
quantum, remain full-text facts. Abstract-less records are carried on title and flagged, never dropped.
"""
import csv
import json
import re

SRC = "literature/search-logs/housing-costs-frame-abstracts.json"
OUT_JSON = "literature/search-logs/housing-costs-screen-pass2.json"
OUT_CSV = "extraction/housing-costs-screen-worklist.csv"

RULES = [
    ("abs_outcome_not_fertility", "OFF_OUTCOME",
     r"birth ?weight|preterm|prematur|perinatal|infant (health|mortality)|birth outcome|"
     r"child (health|development) outcome"),
    ("abs_credit_treatment", "OFF_CREDIT_C3e",
     r"mortgage (rate|interest|credit|finance|loan)|housing finance|credit constraint|"
     r"loan-to-value|down ?payment|monetary policy"),
    ("abs_reverse", "REVERSE",
     r"(fertility|birth|baby boom|demographic)[^.]{0,60}(on|for|affect\w*|impact\w*|drive\w*)[^.]{0,25}"
     r"(housing (market|demand|price)|house price|housing economy)"),
    ("abs_rent", "PRIMARY_COST_RENT_IDENTIFIED", r"\brent(s|al|ers)?\b"),
    ("abs_wealth", "PRIMARY_WEALTH_OWNER",
     r"housing wealth|home equity|house(hold)? wealth shock|wealth effect|property value"),
    ("abs_price", "PRIMARY_COST_RENTER",
     r"hous(e|ing) price|home price|property price|land price|housing cost|price of housing|"
     r"housing expenditure|purchase restriction|housing market volatil"),
    ("abs_affordability", "AFFORDABILITY_RATIO",
     r"affordab|price-to-income|housing burden|cost burden"),
    ("abs_tenure", "AGGREGATE_UNSPLIT",
     r"homeown|home-own|housing tenure|owner-occup|tenure status|housing status|public housing|"
     r"social housing|housing regime"),
    ("abs_space_condition", "PRIMARY_SPACE_QUANTITY",
     r"crowd|dwelling size|housing condition|number of rooms|floor area|housing quality|"
     r"built environment|residential environment|housing space"),
]
COMPILED = [(n, c, re.compile(p, re.I)) for n, c, p in RULES]

frame = json.load(open(SRC))
resolved, still = 0, 0
for r in frame:
    if r["prescreen_rule"] != "unmatched":
        r["screen_pass"] = "pass1_title"
        continue
    text = f"{r['title']} {r.get('abstract', '')}"
    r["screen_pass"] = "pass2_abstract" if r["has_abstract"] else "pass2_title_only"
    for name, cell, pat in COMPILED:
        if pat.search(text):
            r["prescreen_rule"] = name
            r["provisional_cell"] = cell
            resolved += 1
            break
    else:
        r["provisional_cell"] = ("UNCERTAIN_NEEDS_FULLTEXT" if r["has_abstract"]
                                 else "INSUFFICIENT_INFO")
        still += 1

json.dump(frame, open(OUT_JSON, "w"), indent=1)

with open(OUT_CSV, "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["doi", "openalex", "year", "type", "venue", "cited_by", "title",
                "prescreen_rule", "provisional_cell", "screen_pass", "has_abstract",
                "first_found_round", "ra_verdict", "ra_note"])
    for r in sorted(frame, key=lambda x: (x["provisional_cell"],
                                          -(x.get("cited_by_merged") or x["cited_by"] or 0))):
        w.writerow([r["doi"], r["openalex"], r["year"], r["type"], r["venue"],
                    r.get("cited_by_merged") or r["cited_by"], r["title"],
                    r["prescreen_rule"], r["provisional_cell"], r["screen_pass"],
                    r["has_abstract"], r["first_found_round"], "", ""])

from collections import Counter
c = Counter(r["provisional_cell"] for r in frame)
print(f"pass-2 resolved {resolved} of the 92 uncertain; {still} remain unresolved\n")
print("final provisional cell distribution:")
for cell, n in c.most_common():
    print(f"  {n:>4}  {cell}")
prim = sum(v for k, v in c.items() if k.startswith("PRIMARY"))
print(f"\nPRIMARY-cell total: {prim}")
print(f"worklist -> {OUT_CSV}")
