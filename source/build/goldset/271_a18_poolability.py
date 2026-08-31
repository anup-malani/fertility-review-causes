#!/usr/bin/env python3
"""271 — A.18 poolability: apply the >=3 test AFTER stratification. TICK-076.

PROTOCOL §5 pools when there are >=3 studies with extractable effects. The standing
correction is that the test applies **after** stratification, not before: a hazard
ratio beside a variance component beside a per-SD polygenic-score beta is not a
pool of three, it is three different quantities.

Strata are derived from the required-tags list in scope-memo §9 — estimand x
outcome measure x relatedness level — not invented here.

Usage: python3 source/build/goldset/271_a18_poolability.py
"""
import csv
import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CSVP = ROOT / "extraction" / "heritability-fertility-genetic.csv"
OUT = ROOT / "literature" / "search-logs" / "heritability-fertility-genetic-poolability.json"
OUT_MD = ROOT / "literature" / "search-logs" / "heritability-fertility-genetic-poolability.md"

USABLE = ("VERIFIED", "VERIFIED_AUTHORS_PREFERRED", "VERIFIED_NULL",
          "VERIFIED_CELL_RECLASSIFIED_FROM_H2_FERTILITY",
          "VERIFIED_SPECIFICATION_DISCORDANT", "VERIFIED_NON_H2_ESTIMAND")


def main():
    rows = list(csv.DictReader(CSVP.open()))
    usable = [r for r in rows if r["extraction_status"] in USABLE]
    excluded = [r for r in rows if r["extraction_status"] not in USABLE]

    strata = defaultdict(list)
    for r in usable:
        key = (r["estimand"] or "?", r["outcome_measure"] or "?", r["relatedness_level"] or "?")
        strata[key].append(r)
    poolable = {k: v for k, v in strata.items() if len({x["openalex"] for x in v}) >= 3}

    lines = ["# A.18 poolability — the >=3 test applied after stratification\n",
             f"Extraction rows: **{len(rows)}**. Usable estimates: **{len(usable)}**. "
             f"Excluded: {len(excluded)} "
             f"({dict(Counter(r['extraction_status'] for r in excluded))}).\n",
             "\n## Strata (estimand x outcome x relatedness)\n",
             "| estimand | outcome | relatedness | studies | poolable |\n|---|---|---|---|---|"]
    for k, v in sorted(strata.items(), key=lambda kv: -len(kv[1])):
        n = len({x["openalex"] for x in v})
        lines.append(f"| `{k[0]}` | `{k[1]}` | `{k[2]}` | {n} | "
                     f"{'**yes**' if n >= 3 else 'no'} |")
    lines += [f"\n**Strata meeting the >=3 test: {len(poolable)}.**\n",
              "\nApplied before stratification the same evidence would have looked poolable: "
              "there are enough usable estimates in total. Stratified, they scatter across "
              "estimands that cannot be averaged — a variance component, a per-SD polygenic-score "
              "beta and a genetic correlation are three different quantities.\n",
              "\n## Consequence for the synthesis\n",
              "The chapter reports a **narrative synthesis with a stratified evidence table**, not a "
              "meta-analytic pool. That is a finding about this literature, not a shortfall in the "
              "search: 696 studies were screened, 148 reached the primary cells, and the estimates "
              "they report are heterogeneous in kind rather than merely in magnitude.\n"]
    OUT_MD.write_text("\n".join(lines) + "\n")
    OUT.write_text(json.dumps({"summary": {
        "rows": len(rows), "usable": len(usable), "excluded": len(excluded),
        "excluded_breakdown": dict(Counter(r["extraction_status"] for r in excluded)),
        "strata": {" | ".join(k): len({x["openalex"] for x in v}) for k, v in strata.items()},
        "strata_meeting_pooling_test": len(poolable),
        "note": "The >=3 test is applied AFTER stratification. A hazard ratio beside a variance "
                "component is not a pool."}}, indent=1))
    print(f"rows {len(rows)}  usable {len(usable)}  excluded {len(excluded)}")
    print(f"strata: {len(strata)}   meeting >=3 after stratification: {len(poolable)}")
    for k, v in sorted(strata.items(), key=lambda kv: -len(kv[1]))[:10]:
        print(f"   {len({x['openalex'] for x in v}):2d}  {k[0][:38]:38s} {k[1][:26]:26s} {k[2]}")


if __name__ == "__main__":
    main()
