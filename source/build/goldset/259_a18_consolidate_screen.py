#!/usr/bin/env python3
"""259 — A.18 consolidated screen result: the evidence base, by cell and arm. TICK-076.

Merges every verdict file (round 1 stratum A+B, the stratum B depth probes, and
round 2) into one evidence table and reports what the chapter actually has.

Reports PRIMARY cells separately from METHOD/THEORY, because the two are not the
same kind of record: a methods paper informs how the chapter computes, an
included study is what it computes on. Conflating them would inflate the evidence
base — the failure the Tier-A lesson records, where screen output was reported as
the evidence base and dropped the hand-sourced seeds.

Also reports the two distributions the scope memo committed to putting in a table
rather than in prose: `exposure_distance` (Ruling 3) and `decomposes` (Wall 1).

Usage: python3 source/build/goldset/259_a18_consolidate_screen.py
"""
import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
LOGS = ROOT / "literature" / "search-logs"
TEMP = ROOT / "temp" / "a18"
OUT = LOGS / "heritability-fertility-genetic-evidence-base.json"
OUT_MD = LOGS / "heritability-fertility-genetic-evidence-base.md"

PRIMARY = ["H2_FERTILITY", "H2_MODERATION", "SELECTION_DIFFERENTIAL",
           "PEDIGREE_RESPONSE", "PREDICTED_RESPONSE", "ALLELE_FREQ_TREND",
           "WITHIN_VS_POPULATION"]


def main():
    recs = {}
    for vf in sorted((TEMP / "a18_screen_verdicts").glob("*.json")):
        v = json.loads(vf.read_text())
        src = "round2" if vf.name.startswith("r2_") else ("probe" if "probe" in vf.name else "round1")
        bdir = TEMP / ("a18_r2_batches" if src == "round2" else "a18_screen_batches")
        bnum = v["batch"]
        bfile = bdir / f"batch_{int(str(bnum).split('-')[-1]):02d}.json"
        if not bfile.exists():
            continue
        byref = {r["ref"]: r for r in json.loads(bfile.read_text())["records"]}
        for ref, d in v["verdicts"].items():
            r = byref.get(ref)
            if not r:
                continue
            oid = r["openalex"]
            if oid in recs and recs[oid]["verdict"] == "RELEVANT":
                continue          # a study seen twice is one study
            recs[oid] = {**d, "ref": ref, "source": src, "title": r.get("title"),
                         "year": r.get("year"), "venue": r.get("venue")}

    rel = {k: v for k, v in recs.items() if v["verdict"] == "RELEVANT"}
    unc = {k: v for k, v in recs.items() if v["verdict"] == "UNCERTAIN"}
    prim = {k: v for k, v in rel.items() if v["cell"] in PRIMARY}
    meth = {k: v for k, v in rel.items() if v["cell"] not in PRIMARY}

    cells = Counter(v["cell"] for v in prim.values())
    dist = Counter(v["exposure_distance"] for v in prim.values())
    dec = Counter(v["decomposes"] for v in prim.values())
    bysrc = Counter(v["source"] for v in prim.values())

    print(f"screened (distinct studies): {len(recs):,}")
    print(f"  RELEVANT {len(rel)}   UNCERTAIN {len(unc)}   NOT_RELEVANT {len(recs)-len(rel)-len(unc)}")
    print(f"\nPRIMARY-CELL studies: {len(prim)}     METHOD/THEORY/LINK: {len(meth)}\n")
    print("primary cells:")
    for c in PRIMARY:
        if cells.get(c):
            print(f"   {c:26s} {cells[c]:4d}")
    print(f"\nexposure_distance (Ruling 3):")
    for k, n in dist.most_common():
        print(f"   {k:24s} {n:4d}   {100*n/len(prim):5.1f}%")
    print(f"\ndecomposes (Wall 1):")
    for k, n in dec.most_common():
        print(f"   {k:14s} {n:4d}")
    print(f"\nprimary studies by search round: {dict(bysrc)}")

    payload = {"meta": {"ticket": "TICK-076",
                        "screened_distinct": len(recs),
                        "relevant": len(rel), "uncertain": len(unc),
                        "primary_cell_studies": len(prim),
                        "method_theory_link": len(meth),
                        "cells": dict(cells),
                        "exposure_distance": dict(dist),
                        "decomposes": dict(dec),
                        "primary_by_round": dict(bysrc)},
               "primary": [{"openalex": k, **v} for k, v in prim.items()]}
    OUT.write_text(json.dumps(payload, indent=1))

    md = ["# A.18 evidence base after screening\n",
          f"Distinct studies screened: **{len(recs):,}** — RELEVANT {len(rel)}, "
          f"UNCERTAIN {len(unc)}.\n",
          f"\n**Primary-cell studies: {len(prim)}.** Method/theory/link records: {len(meth)} "
          "(these inform how the chapter computes; they are not included studies).\n",
          "\n## Primary synthesis cells\n\n| cell | studies |\n|---|---|"]
    for c in PRIMARY:
        if cells.get(c):
            md.append(f"| `{c}` | {cells[c]} |")
    md += ["\n## Exposure distance from the registered exposure (Ruling 3)\n",
           "| measured exposure | studies | share |\n|---|---|---|"]
    for k, n in dist.most_common():
        md.append(f"| `{k}` | {n} | {100*n/len(prim):.1f}% |")
    md += ["\n## Wall 1: does the design decompose?\n",
           "| `decomposes` | studies |\n|---|---|"]
    for k, n in dec.most_common():
        md.append(f"| `{k}` | {n} |")
    OUT_MD.write_text("\n".join(md) + "\n")
    print(f"\nwrote {OUT.relative_to(ROOT)} and {OUT_MD.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
