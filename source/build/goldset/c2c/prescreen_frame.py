#!/usr/bin/env python3
"""Deterministic pre-screen of the C.2.c Tier-B frame into provisional estimand cells.

WHAT THIS IS AND IS NOT. This is a cheap title-only triage that routes the obviously-off classes and
proposes a provisional cell for the rest. It is NOT the inclusion decision. The scope doc is explicit
that the facts which actually decide routing for C.2.c -- whether a "housing" measure is a price or a
quality-weighted index, whether an estimate conditions on tenure, whether the outcome is timing or
quantum -- are full-text-only in most papers. Every label here is PROVISIONAL and gated by the RA.

Rules are ordered; first match wins. Each is recorded so the routing is auditable and so a bad rule
can be found later by its name rather than by re-deriving it.

Discipline note carried from the relevance-filter bug (snowball log §4): a substring rule is doing
classification work. After running this, READ A RANDOM SAMPLE of what each rule admits and rejects
before trusting the counts.
"""
import csv
import json
import re

FRAME = "literature/search-logs/housing-costs-tier-b-frame-deduped.json"
OUT_JSON = "literature/search-logs/housing-costs-prescreen.json"
OUT_CSV = "extraction/housing-costs-screen-worklist.csv"

RULES = [
    # (rule name, provisional cell, pattern)
    ("birth_outcome_health", "OFF_OUTCOME",
     r"birth ?weight|birthweight|preterm|prematur|birth (and infant )?outcome|birth defect|gestational|"
     r"stillbirth|infant mortality|neonat|congenital|apgar|greenness|air pollut|green space|fetal growth|"
     r"in utero|birthing people|homeless|housing insecurity during pregnancy|infant outcome"),
    ("clinical_or_nonhousing", "OFF_OTHER",
     r"physician|obstetric|gynecol|residency program|didactic|oocyte|egg freezing|"
     r"fertility (knowledge|awareness)|infertility care|reproductive endocrinolog"),
    ("living_arrangement", "OFF_LIVING_ARRANGEMENT_A23",
     r"co-?residen|coresiden|leaving home|home ?leaving|boomerang|returning to the (nest|parental)|"
     r"living with parents|parental home|nest leaving|empty nest|intergenerational co"),
    ("credit_treatment", "OFF_CREDIT_C3e",
     r"mortgage (rate|credit|market dereg|deregulation)|credit (supply|expansion|constraint|access)|"
     r"student (loan|debt)|monetary policy|interest rate|loan-to-value|financial dereg|liquidity"),
    ("reverse_direction", "REVERSE",
     r"fertility .{0,30}(housing (market|demand|price)|house price)|"
     r"(baby boom|birth|fertility) .{0,25}housing (market|demand|bubble)|"
     r"demographic .{0,20}housing market|housing demand"),
    ("marriage_only", "HOUSING_ONLY_MECHANISM",
     r"marriage (entry|delay|timing|market)|marital (entry|timing)|nuptial|union formation|"
     r"marriage (rate|probability)|delay(s|ed)? marriage"),
    ("mobility_context", "HOUSING_ONLY_MECHANISM",
     r"residential (mobility|relocation|reloc)|migration|moving|relocat|housing career|housing pathway|"
     r"housing transition|residential context"),
    ("space_quantity", "PRIMARY_SPACE_QUANTITY",
     r"crowd|housing type|dwelling (type|size)|room|apartment living|housing condition|density|"
     r"space|overcrowd"),
    ("affordability", "AFFORDABILITY_RATIO",
     r"affordab|price-to-income|housing burden|cost burden|housing stress"),
    ("rent_identified", "PRIMARY_COST_RENT_IDENTIFIED",
     r"\brent(s|al|er)?\b"),
    ("wealth_channel", "PRIMARY_WEALTH_OWNER",
     r"housing wealth|home equity|wealth (shock|effect)|homeowner"),
    ("price_channel", "PRIMARY_COST_RENTER",
     r"house ?price|housing price|home price|property price|land price|housing (boom|bust|cost)|real estate"),
]
COMPILED = [(n, c, re.compile(p, re.I)) for n, c, p in RULES]

frame = json.load(open(FRAME))
counts = {}
for r in frame:
    t = r["title"] or ""
    r["prescreen_rule"] = "unmatched"
    r["provisional_cell"] = "UNCERTAIN_NEEDS_SCREEN"
    for name, cell, pat in COMPILED:
        if pat.search(t):
            r["prescreen_rule"] = name
            r["provisional_cell"] = cell
            break
    r["ra_verdict"] = ""          # to be filled at the RA gate
    r["ra_note"] = ""
    counts[r["prescreen_rule"]] = counts.get(r["prescreen_rule"], 0) + 1

json.dump(frame, open(OUT_JSON, "w"), indent=1)

with open(OUT_CSV, "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["doi", "openalex", "year", "type", "venue", "cited_by", "title",
                "prescreen_rule", "provisional_cell", "first_found_round",
                "ra_verdict", "ra_note"])
    for r in sorted(frame, key=lambda x: (x["provisional_cell"],
                                          -(x.get("cited_by_merged") or x["cited_by"] or 0))):
        w.writerow([r["doi"], r["openalex"], r["year"], r["type"], r["venue"],
                    r.get("cited_by_merged") or r["cited_by"], r["title"],
                    r["prescreen_rule"], r["provisional_cell"], r["first_found_round"], "", ""])

print(f"frame: {len(frame)}\n")
print("rule                          n    provisional cell")
for name, cell, _ in COMPILED:
    if counts.get(name):
        print(f"  {name:<26} {counts[name]:>3}    {cell}")
print(f"  {'unmatched':<26} {counts.get('unmatched', 0):>3}    UNCERTAIN_NEEDS_SCREEN")
prim = sum(1 for r in frame if r["provisional_cell"].startswith("PRIMARY"))
print(f"\nprovisionally PRIMARY-cell: {prim}")
print(f"routed out / context      : {sum(1 for r in frame if r['provisional_cell'].startswith(('OFF_', 'HOUSING_ONLY', 'REVERSE')))}")
print(f"needs human screen        : {counts.get('unmatched', 0)}")
print(f"\nworklist -> {OUT_CSV}")
