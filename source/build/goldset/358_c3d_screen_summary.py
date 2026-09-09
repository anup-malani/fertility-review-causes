#!/usr/bin/env python3
"""358 — the completed C.3.d title/abstract screen: cells, the direction split, and the walls.

The screen is COMPLETE: 3,254 of 3,254 records carry a verdict, none unscreened. That matters for
what can be said afterwards -- a share computed over a partial screen is a bound
(`bound-what-you-did-not-screen`), and these are counts.

WHAT THIS SCRIPT IS FOR. The verdict file answers "which cell" one record at a time. The three
questions the chapter turns on are aggregates, and each has a denominator that is easy to get wrong:

1. **The direction split** (scope §2). Forward is the registered estimand; backward is link 2. The
   denominator is records in an estimand cell, NOT all screened rows -- half the universe is
   OFF_TOPIC and including it would make both arms look tiny.
2. **Wall 2** (scope §8, C.2.e). "How much of the forward arm is actually the PARENT's return" has
   as its denominator the FORWARD FAMILY -- records whose exposure moves a return and whose outcome
   is fertility -- not all screened rows and not all forward-direction rows.
3. **Sensitivity**, which needs the withheld gold key merged here and only here.

Output: literature/search-logs/quantity-quality-tradeoff-screen-summary.{json,md}
"""
import csv
import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
LOGS = ROOT / "literature" / "search-logs"
VERD = ROOT / "extraction" / "quantity-quality-tradeoff-screen-verdicts.csv"

PRIMARY = {"RETURN_FERTILITY", "SHOCK_FERTILITY"}
MIXED = {"MIXED_CHILD_PARENT_RETURN", "MIXED_RETURN_POSITION", "MIXED_RETURN_INCOME"}
# The denominator for the Wall 2 question: a return-moving exposure with a fertility outcome.
FORWARD_FAMILY = PRIMARY | MIXED
IN_SCOPE = FORWARD_FAMILY | {"QQ_SUBSTITUTION", "RETURN_ASSOCIATION", "PERCEIVED_RETURN", "THEORY"}
EXCLUDED = {"OFF_TOPIC", "OFF_OTHER", "UNCLEAR"}


def main():
    rows = list(csv.DictReader(VERD.open()))
    universe = json.loads((LOGS / "quantity-quality-tradeoff-screen-universe.json").read_text())
    gold = json.loads((LOGS / "quantity-quality-tradeoff-screen-gold.json").read_text())["gold"]
    by_sid = {f"C3D{i:04d}": r for i, r in enumerate(universe["records"])}

    n = len(rows)
    assert n == universe["n"], f"screen is INCOMPLETE: {n} verdicts for {universe['n']} records"
    cells = Counter(r["cell"] for r in rows)
    dirs = Counter(r["direction"] for r in rows)
    in_scope = sum(v for k, v in cells.items() if k in IN_SCOPE)
    primary = sum(cells.get(c, 0) for c in PRIMARY)
    fwd_family = sum(cells.get(c, 0) for c in FORWARD_FAMILY)
    backward = cells.get("QQ_SUBSTITUTION", 0)

    # Walls, counted over the forward family -- the denominator that answers PI call 3.
    walls = Counter()
    for r in rows:
        for w in (r["wall_risk"] or "").split(";"):
            if w:
                walls[w] += 1
    w2_in_family = sum(1 for r in rows
                       if r["cell"] in FORWARD_FAMILY and "W2_PARENT_RETURN" in (r["wall_risk"] or ""))

    # Identified designs in the primary cells -- what can actually carry an effect estimate.
    IDENT = {"RCT", "IV", "DID", "RDD", "EVENT_STUDY", "NATURAL_EXPERIMENT"}
    prim_ident = sum(1 for r in rows if r["cell"] in PRIMARY and r["design"] in IDENT)
    back_ident = sum(1 for r in rows if r["cell"] == "QQ_SUBSTITUTION" and r["design"] in IDENT)

    # Sensitivity: merge the withheld key HERE and only here.
    sens = defaultdict(lambda: {"n": 0, "kept": 0, "missed": []})
    for sid, v in ((r["screen_id"], r) for r in rows):
        rec = by_sid.get(sid) or {}
        g = gold.get(rec.get("oa_id") or "")
        if not g or not g.get("is_gold"):
            continue
        d = g.get("direction") or "UNKNOWN"
        sens[d]["n"] += 1
        if v["cell"] in IN_SCOPE:
            sens[d]["kept"] += 1
        else:
            sens[d]["missed"].append({"screen_id": sid, "cell": v["cell"],
                                      "title": (rec.get("title") or "")[:70]})

    blob = {"n_screened": n, "complete": True, "cells": dict(cells), "directions": dict(dirs),
            "in_scope": in_scope, "primary": primary, "forward_family": fwd_family,
            "backward": backward, "walls": dict(walls),
            "wall2_in_forward_family": w2_in_family,
            "primary_identified": prim_ident, "backward_identified": back_ident,
            "sensitivity": {k: {"n": v["n"], "kept": v["kept"], "missed": v["missed"]}
                            for k, v in sens.items()}}
    (LOGS / "quantity-quality-tradeoff-screen-summary.json").write_text(json.dumps(blob, indent=2) + "\n")

    pc = lambda x, d: f"{100*x/d:.1f}%" if d else "—"
    print(f"SCREEN COMPLETE: {n}/{universe['n']} records, 0 unscreened\n")
    print("cells:")
    for k, v in cells.most_common():
        print(f"  {k:28} {v:>5}  {pc(v, n)}")
    print(f"\nin scope {in_scope} ({pc(in_scope, n)}); excluded {n - in_scope}")
    print(f"\nTHE DIRECTION SPLIT (scope §2), over records in an estimand cell:")
    print(f"  backward  QQ_SUBSTITUTION           {backward:>5}  {pc(backward, in_scope)}")
    print(f"  forward   primary cells             {primary:>5}  {pc(primary, in_scope)}")
    print(f"  forward   family incl. MIXED        {fwd_family:>5}  {pc(fwd_family, in_scope)}")
    print(f"  ratio backward : forward-primary    {backward/primary:.1f} : 1")
    print(f"\n  identified designs: primary {prim_ident}/{primary}, backward {back_ident}/{backward}")
    print(f"\nWALL 2 (scope §8, C.2.e) over the FORWARD FAMILY -- the denominator for PI call 3:")
    print(f"  {w2_in_family}/{fwd_family} = {pc(w2_in_family, fwd_family)} of the forward arm is "
          f"the PARENT's return")
    print("\nwall risk flags across all screened rows:")
    for k, v in walls.most_common():
        print(f"  {k:22} {v:>5}")
    print("\nSENSITIVITY on the withheld gold:")
    for d in sorted(sens):
        v = sens[d]
        print(f"  {d:9} {v['kept']}/{v['n']}")
        for m in v["missed"]:
            print(f"      routed out -> {m['cell']:14} {m['title']}")

    L = ["# C.3.d title/abstract screen — complete", "",
         "Generated by `source/build/goldset/358_c3d_screen_summary.py`. Do not edit by hand.", "",
         f"**{n} of {universe['n']} records screened, none unscreened.** Every figure below is a "
         "count, not a bound.", "",
         "## Cells", "", "| cell | n | share |", "|---|---|---|"]
    L += [f"| `{k}` | {v} | {pc(v, n)} |" for k, v in cells.most_common()]
    L += ["", "## The direction split (scope §2)", "",
          "Denominator is records in an estimand cell — half the universe is OFF_TOPIC and "
          "including it would make both arms look tiny.", "",
          "| arm | n | share of in-scope | identified designs |", "|---|---|---|---|",
          f"| backward (`QQ_SUBSTITUTION`, link 2) | {backward} | {pc(backward, in_scope)} | {back_ident} |",
          f"| forward, primary cells | {primary} | {pc(primary, in_scope)} | {prim_ident} |",
          f"| forward family incl. `MIXED_*` | {fwd_family} | {pc(fwd_family, in_scope)} | — |", "",
          f"**The backward arm outnumbers the registered forward estimand {backward/primary:.1f} to 1.**",
          "", "## Wall 2 — how much of the forward arm is C.2.e's", "",
          f"**{w2_in_family} of {fwd_family} forward-family records ({pc(w2_in_family, fwd_family)}) "
          "carry `W2_PARENT_RETURN`** — the exposure moves the *parent's* return, not the child's. "
          "That is the denominator scope PI call 3 asks about.", "",
          "| wall | flagged rows |", "|---|---|"]
    L += [f"| `{k}` | {v} |" for k, v in walls.most_common()]
    L += ["", "## Sensitivity against the withheld gold", "",
          "| direction | kept in scope | gold |", "|---|---|---|"]
    L += [f"| `{d}` | {sens[d]['kept']} | {sens[d]['n']} |" for d in sorted(sens)]
    L.append("")
    (LOGS / "quantity-quality-tradeoff-screen-summary.md").write_text("\n".join(L))
    print(f"\nwrote quantity-quality-tradeoff-screen-summary.{{json,md}}")


main()
