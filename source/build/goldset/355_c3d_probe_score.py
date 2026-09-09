#!/usr/bin/env python3
"""355 — score C.3.d's depth probe: the yield curve by stratum, and sensitivity against the
withheld gold key.

Two questions, and they are different.

**Does the yield fall with citation rank?** If it does, the remainder can be truncated and the tail
sampled. If it does not, it cannot: on C.2.b the curve was flat and the single best record sat in
the LAST stratum (`a-flat-yield-curve-forbids-truncation`). The probe took 25 records from each of
6 evenly spaced strata of the citation-ranked universe rather than screening front-to-back, because
a front-to-back pass measures the head and reports it as the population
(`citation-sorted-head-is-not-the-population`, `probe-depth-dont-screen-sequentially`).

**Did the screen find the records it was not told about?** The batches carried no gold flag, no
provenance and no arm. The key in `...-screen-gold.json` is merged HERE and only here. A screen that
can see which rows are gold cannot measure its own sensitivity
(`a-positives-only-screen-cannot-measure-sensitivity`), and every emitted row was required to come
back with a verdict precisely so that this table has a denominator.

Sensitivity is reported BY DIRECTION, because scope §2 says the two arms are different questions and
a pooled number would hide an arm failing.

Output: literature/search-logs/quantity-quality-tradeoff-probe-score.{json,md}
"""
import csv
import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
LOGS = ROOT / "literature" / "search-logs"
BATCH = ROOT / "extraction" / "quantity-quality-tradeoff-screen-batches"
VERD = ROOT / "extraction" / "quantity-quality-tradeoff-screen-verdicts.csv"

PRIMARY = {"RETURN_FERTILITY", "SHOCK_FERTILITY"}

# GOLD ERRATA. A record here is in the gold key and should NOT be: the blinded screen routed it out
# and the screen was right. Recorded rather than quietly deleted, because "the screen missed a gold
# record" and "the gold key contains a record that is not gold" are different findings and only the
# second one is true here (`a-recall-miss-can-indict-the-anchors`,
# `blinded-screen-audits-the-anchors`).
#
# W4409548817 — "Genetics of twin birth rate in German Holstein and options for breeding", a DAIRY
# CATTLE paper. It reached the seed table on "twin birth" and cleared the outcome tier on "birth
# rate"; 348's soil/livestock filter carried `dairy (cow|cattle)` but no BREED NAME. 348's DROP is
# now widened with breed and husbandry terms, verified behaviourally against 7 cases and against the
# whole 515-record seed table, where it removes this one record and nothing else. Not re-run on this
# chapter: `screen_id` is a position in the citation-ranked universe, so re-running would renumber
# every id and invalidate 150 hand-screened verdicts to remove one bad control out of 82.
GOLD_ERRATA = {
    "W4409548817": "dairy-cattle twinning genetics; livestock homonym that 348's breed-name gap "
                   "let into the seed table. The screen was right to route it out.",
}
IN_SCOPE = PRIMARY | {"QQ_SUBSTITUTION", "MIXED_CHILD_PARENT_RETURN", "MIXED_RETURN_POSITION",
                      "MIXED_RETURN_INCOME", "RETURN_ASSOCIATION", "PERCEIVED_RETURN", "THEORY"}


def main():
    verdicts = {r["screen_id"]: r for r in csv.DictReader(VERD.open())}
    universe = json.loads((LOGS / "quantity-quality-tradeoff-screen-universe.json").read_text())
    goldkey = json.loads((LOGS / "quantity-quality-tradeoff-screen-gold.json").read_text())
    gold = goldkey["gold"]

    # screen_id is position-based in the citation-ranked universe, so it maps back to the record.
    by_sid = {}
    for i, r in enumerate(universe["records"]):
        by_sid[f"C3D{i:04d}"] = r

    strata = []
    for s in range(1, 7):
        p = BATCH / f"probe-s{s}-of-6.json"
        ids = [r["screen_id"] for r in json.loads(p.read_text())["records"]]
        rows = [verdicts[i] for i in ids if i in verdicts]
        missing = [i for i in ids if i not in verdicts]
        cells = Counter(r["cell"] for r in rows)
        strata.append({
            "stratum": s, "n": len(ids), "verdicts": len(rows), "missing_verdict": missing,
            "primary": sum(1 for r in rows if r["cell"] in PRIMARY),
            "in_scope": sum(1 for r in rows if r["cell"] in IN_SCOPE),
            "off_topic": cells.get("OFF_TOPIC", 0),
            "backward": sum(1 for r in rows if r["direction"] == "BACKWARD"),
            "forward": sum(1 for r in rows if r["direction"] == "FORWARD"),
            "cells": dict(cells)})

    # ---- sensitivity: gold rows that were IN the probe, and what the screen did with them
    sens = defaultdict(lambda: {"n": 0, "in_scope": 0, "off": 0, "rows": []})
    errata_seen = []
    for sid, rec in by_sid.items():
        if sid not in verdicts:
            continue
        oid = rec.get("oa_id")
        g = gold.get(oid)
        if not g or not g.get("is_gold"):
            continue
        if oid in GOLD_ERRATA:
            errata_seen.append({"oa_id": oid, "screen_id": sid,
                                "title": (rec.get("title") or "")[:70],
                                "cell": verdicts[sid]["cell"], "why": GOLD_ERRATA[oid]})
            continue                      # not gold; excluded from the denominator, not counted

        v = verdicts[sid]
        d = g.get("direction") or "UNKNOWN"
        sens[d]["n"] += 1
        keep = v["cell"] in IN_SCOPE
        sens[d]["in_scope"] += 1 if keep else 0
        sens[d]["off"] += 0 if keep else 1
        sens[d]["rows"].append({"screen_id": sid, "kept": keep, "cell": v["cell"],
                                "title": (rec.get("title") or "")[:70]})

    total_n = sum(s["n"] for s in strata)
    total_prim = sum(s["primary"] for s in strata)
    total_scope = sum(s["in_scope"] for s in strata)
    unscreened = [i for s in strata for i in s["missing_verdict"]]

    blob = {"n_screened": total_n, "primary": total_prim, "in_scope": total_scope,
            "strata": strata,
            "sensitivity": {k: {kk: vv for kk, vv in v.items()} for k, v in sens.items()},
            "gold_errata_excluded": errata_seen,
            "rows_without_verdict": unscreened}
    (LOGS / "quantity-quality-tradeoff-probe-score.json").write_text(json.dumps(blob, indent=2) + "\n")

    print(f"screened {total_n} records across 6 strata; "
          f"primary {total_prim} ({100*total_prim/total_n:.1f}%), "
          f"in scope {total_scope} ({100*total_scope/total_n:.1f}%)")
    if unscreened:
        print(f"  !! {len(unscreened)} emitted rows have NO verdict — sensitivity has no "
              f"denominator until they do")
    print("\nyield curve by citation-rank stratum (1 = most cited):")
    print(f"  {'stratum':>8} {'n':>4} {'primary':>8} {'in scope':>9} {'off-topic':>10} "
          f"{'fwd':>5} {'back':>5}")
    for s in strata:
        print(f"  {s['stratum']:>8} {s['n']:>4} {s['primary']:>8} {s['in_scope']:>9} "
              f"{s['off_topic']:>10} {s['forward']:>5} {s['backward']:>5}")

    if errata_seen:
        print(f"\ngold errata excluded from the denominator ({len(errata_seen)}): records in the "
              "gold key that are NOT gold, which the blinded screen caught:")
        for e in errata_seen:
            print(f"    {e['screen_id']} -> {e['cell']:10} {e['title']}")
    print("\nsensitivity on the WITHHELD gold that landed in the probe, by direction:")
    for d in sorted(sens):
        v = sens[d]
        print(f"  {d:9} {v['in_scope']}/{v['n']} kept in scope")
        for r in v["rows"]:
            if not r["kept"]:
                print(f"      MISSED -> {r['cell']:14} {r['title']}")

    L = ["# C.3.d depth-probe score", "",
         "Generated by `source/build/goldset/355_c3d_probe_score.py`. Do not edit by hand.", "",
         f"**{total_n} records screened** across 6 evenly spaced strata of the citation-ranked "
         f"universe (3,254 records). Primary cells **{total_prim}** "
         f"({100*total_prim/total_n:.1f}%); in scope **{total_scope}** "
         f"({100*total_scope/total_n:.1f}%).", "",
         "## Yield curve", "",
         "The probe is spaced rather than front-to-back because a front-to-back pass measures the "
         "head and then reports it as the population "
         "(`citation-sorted-head-is-not-the-population`). Whether the remainder can be truncated is "
         "a question for this table, not an assumption.", "",
         "| stratum | n | primary | in scope | off-topic | forward | backward |",
         "|---|---|---|---|---|---|---|"]
    L += [f"| {s['stratum']} | {s['n']} | {s['primary']} | {s['in_scope']} | {s['off_topic']} | "
          f"{s['forward']} | {s['backward']} |" for s in strata]
    L += ["", "## Sensitivity against the withheld gold", "",
          "The batches carried no gold flag, no provenance and no arm; the key is merged only here. "
          "Reported by direction, because scope §2 makes the two arms different questions and a "
          "pooled number would hide one failing.", "",
          "| direction | kept in scope | gold in probe |", "|---|---|---|"]
    L += [f"| `{d}` | {sens[d]['in_scope']} | {sens[d]['n']} |" for d in sorted(sens)]
    missed = [(d, r) for d in sens for r in sens[d]["rows"] if not r["kept"]]
    if missed:
        L += ["", "### Gold the screen routed out", "",
              "| direction | cell given | title |", "|---|---|---|"]
        L += [f"| `{d}` | `{r['cell']}` | {r['title']} |" for d, r in missed]
    else:
        L += ["", "**No gold was routed out of scope.**"]
    if errata_seen:
        L += ["", "### Gold errata — records in the key that are NOT gold", "",
              "The blinded screen routed these out and was right to. They are excluded from the "
              "denominator above rather than counted as misses: *the screen missed a gold record* "
              "and *the key contains a record that is not gold* are different findings.", "",
              "| screen id | cell given | title | why |", "|---|---|---|---|"]
        L += [f"| `{e['screen_id']}` | `{e['cell']}` | {e['title']} | {e['why']} |"
              for e in errata_seen]
    L.append("")
    (LOGS / "quantity-quality-tradeoff-probe-score.md").write_text("\n".join(L))
    print(f"\nwrote quantity-quality-tradeoff-probe-score.{{json,md}}")


main()
