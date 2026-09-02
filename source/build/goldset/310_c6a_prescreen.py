#!/usr/bin/env python3
"""310 — C.6.a deterministic prescreen, with every rule recall-checked before it may fire. TICK-078.

A prescreen rule is a claim that a class of records cannot be relevant. The claim is testable: run it
against the resolved anchors and see what it deletes. A.18's prescreen proposed several rules and
only two survived this check; a species filter on that chapter flagged the selection estimators its
own primary arm runs on (`filter-can-delete-your-own-method-canon`).

So: no rule fires unless it drops ZERO anchors. Rules that touch an anchor are reported with the
anchor they would have deleted and are DISABLED, not weakened -- a rule that needs an exception to
survive is a rule that has not been understood yet.

Rules are also reported with their yield, because a rule that drops nothing is dead weight carried
into every future chapter that copies this file.

Usage: python3 source/build/goldset/310_c6a_prescreen.py
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
LOGS = ROOT / "literature" / "search-logs"
U = json.loads((LOGS / "easterlin-relative-income-screen-universe.json").read_text())
A = json.loads((LOGS / "easterlin-relative-income-cold-start-anchors.json").read_text())
OUT = LOGS / "easterlin-relative-income-prescreen.json"

GOLD = {a["top_candidate"]["oa_id"].rsplit("/", 1)[-1]: a["key"]
        for a in A if (a.get("top_candidate") or {}).get("oa_id")}

NON_STUDY = {"dataset", "peer-review", "paratext", "editorial", "erratum", "letter",
             "retraction", "grant"}


def text(r):
    return ((r.get("title") or "") + " . " + (r.get("abstract") or "")).lower()


# Each rule: (name, predicate -> True means DROP, one-line justification)
RULES = [
    ("non_study_type",
     lambda r: (r.get("type") or "").lower() in NON_STUDY,
     "A dataset, editorial, erratum or peer-review record is not a study."),

    ("plant_gene_baby_boom",
     lambda r: bool(re.search(r"arabidopsis|transcription factor|somatic embryo|"
                              r"\bBBM\b|plant regeneration", text(r), re.I)),
     "BABY BOOM is an Arabidopsis transcription factor; those records use the word 'fertile'."),

    ("generational_label_only",
     lambda r: bool(re.search(r"baby boomer", text(r), re.I))
     and not re.search(r"relative income|cohort size|easterlin|relative cohort|"
                       r"countercyclical|fertility rate|birth rate|childbearing", text(r), re.I),
     "'Baby Boomers' the living generation -- retirement, gerontology, marketing -- with no "
     "C.6.a exposure or fertility-outcome term anywhere in title or abstract."),

    ("happiness_homonym",
     lambda r: bool(re.search(r"easterlin paradox|life satisfaction|subjective well[- ]being|"
                              r"happiness", text(r), re.I))
     and not re.search(r"fertility|childbearing|birth rate|family size|cohort size",
                       text(r), re.I),
     "The Easterlin-paradox well-being literature, with no fertility term present."),

    ("clinical_fertility",
     lambda r: bool(re.search(r"\bivf\b|in vitro fertilization|sperm|oocyte|embryo transfer|"
                              r"infertility treatment|assisted reproduct", text(r), re.I))
     and not re.search(r"relative income|cohort size|easterlin|baby boom", text(r), re.I),
     "Clinical reproductive medicine -- A.17's literature, not C.6.a's."),

    ("soil_fertility",
     lambda r: bool(re.search(r"soil fertilit|fertiliz|fertilis|crop yield|agronom|nitrogen|"
                              r"livestock|maize|wheat yield", text(r), re.I)),
     "Agronomic 'fertility'. Inherited from C.3.e's prescreen."),
]


def main():
    records = U["records"]
    report, accepted, dropped_ids = [], [], set()
    for name, pred, why in RULES:
        hits = [r for r in records if pred(r)]
        touched = [(r["openalex"], GOLD[r["openalex"]]) for r in hits if r["openalex"] in GOLD]
        ok = not touched
        report.append({"rule": name, "why": why, "n_dropped": len(hits),
                       "gold_touched": [t[1] for t in touched], "enabled": ok})
        flag = "ENABLED " if ok else "DISABLED"
        print(f"{flag} {name:26} would drop {len(hits):4}"
              + (f"   *** TOUCHES GOLD: {', '.join(t[1] for t in touched)}" if touched else ""))
        if ok:
            accepted.append(name)
            dropped_ids |= {r["openalex"] for r in hits}

    survivors = [r for r in records if r["openalex"] not in dropped_ids]
    gold_kept = sum(1 for g in GOLD if g in {r["openalex"] for r in survivors})
    print(f"\n{len(records)} -> {len(survivors)} survivors "
          f"({len(dropped_ids)} dropped by {len(accepted)} enabled rules)")
    print(f"gold retained {gold_kept}/{len(GOLD)}")
    dead = [r["rule"] for r in report if r["enabled"] and r["n_dropped"] == 0]
    if dead:
        print(f"DEAD RULES (enabled, dropped nothing -- do not copy forward): {', '.join(dead)}")

    OUT.write_text(json.dumps({
        "n_in": len(records), "n_out": len(survivors), "n_dropped": len(dropped_ids),
        "gold_total": len(GOLD), "gold_retained": gold_kept,
        "accepted_rules": accepted, "rules": report,
        "survivor_ids": sorted(r["openalex"] for r in survivors)}, indent=1) + "\n")
    print(f"written: {OUT.name}")


main()
