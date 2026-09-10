#!/usr/bin/env python3
"""
387 — C.3.f: freeze the screen ids, then prune the ungated channel's finance homonym.

386 measured what the ungated FLOW_MEASUREMENT channel cost: `intergenerational wealth` alone
reaches 396 records that no gated channel reaches, 61% of them carrying finance vocabulary — family
offices, estate planning, bequest taxation, wealth mobility — and only 44 are demographic without
also being finance. Reading those 44 they are mostly housing-finance transfers and politicians'
estates, not the flow this chapter measures. The term is dropped from that channel.

**The ids are frozen before anything is removed, and that is the point of this script.**
`screen_id` was position-based over the citation-sorted universe, so removing 396 records would
renumber everything below the first removal and silently invalidate every verdict already written
(50 of them, strata 1 and 8). `stage-output-must-survive-rerun`: a stage's output has to survive the
next stage editing its input. The ids are written into the hydrated file once, and 385 reads them
from there instead of recomputing.

Two refusals, because a prune that quietly drops the wrong thing is worse than no prune:
  * no anchor and no decoy may be removed — checked against 381's list, and the run aborts if one is
  * no record with a verdict already written may be removed — checked against the verdicts CSV

Output: rewrites temp/c3f-universe-hydrated.json and output/wealth-flows-reversal-universe.json,
and writes literature/search-logs/c3f-universe-prune-<date>.{json,md}.
"""
import csv, json, sys, datetime, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "source" / "lib"))
import textnorm                                                    # noqa: E402

LOGS = ROOT / "literature" / "search-logs"
DATE = datetime.date.today().isoformat()
HYDRATED = ROOT / "temp" / "c3f-universe-hydrated.json"
UNIVERSE = ROOT / "output" / "wealth-flows-reversal-universe.json"
VERDICTS = ROOT / "extraction" / "wealth-flows-reversal-screen-verdicts.csv"

DROP_TERM = "intergenerational wealth"
KEEP_TERMS = ["wealth flows", "National Transfer Accounts", "lifecycle deficit",
              "life cycle deficit", "intergenerational resource flows", "flow of wealth",
              "net intergenerational transfer"]


def main():
    recs = json.loads(HYDRATED.read_text())["records"]
    cal = json.load(open(LOGS / "c3f-query-calibration-2026-09-10.json"))
    protected = set(cal["anchors"]) | set(cal["decoys"])

    # ---------------------------------------------------------------- freeze the ids
    already = sum(1 for r in recs if "screen_id" in r)
    if already and already != len(recs):
        sys.exit(f"{already} of {len(recs)} records carry a frozen id — refusing to renumber a "
                 "partially frozen file")
    if not already:
        ordered = sorted(recs, key=lambda r: -(r.get("cited_by") or 0))
        for i, r in enumerate(ordered):
            r["screen_id"] = f"C3F{i:04d}"
        recs = ordered
        print(f"froze {len(recs)} screen ids from the citation-sorted order")
    else:
        print(f"{already} ids already frozen; keeping them")

    # ---------------------------------------------------------------- decide the prune
    def flow_terms(r):
        blob = textnorm.norm(f"{r.get('title','')} {r.get('abstract','')}")
        hits = [t for t in KEEP_TERMS if textnorm.norm(t) in blob]
        if textnorm.norm(DROP_TERM) in blob:
            hits.append(DROP_TERM)
        return hits

    drop = []
    for r in recs:
        prov = {p.split(":")[0] for p in r.get("provenance") or []}
        if prov != {"FLOWMEAS"}:
            continue                                  # another channel also reaches it: keep
        if flow_terms(r) == [DROP_TERM]:
            drop.append(r)
    drop_ids = {r["id"] for r in drop}

    # ---------------------------------------------------------------- refuse to lose these
    lost_anchors = drop_ids & protected
    if lost_anchors:
        sys.exit(f"prune would remove {len(lost_anchors)} anchor/decoy records: "
                 f"{sorted(lost_anchors)}. Refusing.")
    screened = set()
    if VERDICTS.exists():
        with VERDICTS.open() as f:
            screened = {r["screen_id"] for r in csv.DictReader(f)}
    # An already-screened record is KEPT whatever the rule says: its verdict is the record of a
    # decision, and removing it would erase that. The prune exists to save screening effort, and a
    # record already screened costs nothing more. So they come out of the drop set rather than
    # aborting the run.
    #
    # They are also the rule's validation. Twelve of stratum 8's verdicts fall inside the drop set,
    # and the check below reports how they were routed by hand: if the rule were wrong, some would
    # be something other than OFF_TOPIC (`safeguards-must-be-measured-not-trusted`).
    verdict_cell = {}
    if VERDICTS.exists():
        with VERDICTS.open() as f:
            verdict_cell = {r["screen_id"]: r["cell"] for r in csv.DictReader(f)}
    overlap = [r for r in drop if r["screen_id"] in verdict_cell]
    if overlap:
        cells = {}
        for r in overlap:
            cells[verdict_cell[r["screen_id"]]] = cells.get(verdict_cell[r["screen_id"]], 0) + 1
        print(f"\n  {len(overlap)} of the drop set already carry a hand verdict. Kept, and they "
              f"validate the rule:")
        for c, n in sorted(cells.items(), key=lambda kv: -kv[1]):
            print(f"    {n:>3}  {c}")
        if any(c not in ("OFF_TOPIC", "INSUFFICIENT_INFO") for c in cells):
            sys.exit("a record inside the drop set was hand-routed to something other than "
                     "OFF_TOPIC or INSUFFICIENT_INFO. The rule is wrong. Refusing to prune.")
        drop = [r for r in drop if r["screen_id"] not in verdict_cell]
        drop_ids = {r["id"] for r in drop}

    kept = [r for r in recs if r["id"] not in drop_ids]
    print(f"\npruning {len(drop)} records reached ONLY by the ungated channel and ONLY by "
          f"'{DROP_TERM}'")
    print(f"  no anchor or decoy removed (checked {len(protected)})")
    print(f"  no already-screened record removed (checked {len(screened)} verdicts)")
    print(f"  universe {len(recs):,} -> {len(kept):,}")

    HYDRATED.write_text(json.dumps({"n": len(kept), "records": kept}, indent=1) + "\n")
    univ = json.loads(UNIVERSE.read_text())
    univ["records"] = [r for r in univ["records"] if r["id"] not in drop_ids]
    univ["n"] = len(univ["records"])
    univ["pruned"] = {"date": DATE, "n": len(drop), "rule":
                      f"provenance == FLOWMEAS only AND the only flow term matched is "
                      f"'{DROP_TERM}'"}
    UNIVERSE.write_text(json.dumps(univ, indent=1) + "\n")

    log = {"date": DATE, "drop_term": DROP_TERM, "keep_terms": KEEP_TERMS,
           "before": len(recs), "after": len(kept), "pruned": len(drop),
           "anchors_protected": len(protected), "verdicts_protected": len(screened),
           "rule_validated_on": {"n": len(overlap),
                                 "cells": sorted({verdict_cell[r["screen_id"]] for r in overlap})},
           "examples": [{"id": r["id"], "screen_id": r["screen_id"], "title": r.get("title"),
                         "year": r.get("year")} for r in drop[:40]]}
    (LOGS / f"c3f-universe-prune-{DATE}.json").write_text(json.dumps(log, indent=2) + "\n")
    md = [f"# C.3.f universe prune — {DATE}", "",
          "By `source/build/goldset/387_c3f_universe_prune.py`.", "",
          f"**{len(recs):,} → {len(kept):,}** ({len(drop):,} removed).", "",
          f"Rule: a record is removed only if the ungated FLOW_MEASUREMENT channel is its *only*",
          f"provenance **and** `{DROP_TERM}` is the *only* flow-accounting term it matches. A record",
          "any other channel or term reaches is kept.", "",
          f"Screen ids were frozen before the prune, so the {len(screened)} verdicts already written",
          "still address the same records. No anchor or decoy was removed.", ""]
    (LOGS / f"c3f-universe-prune-{DATE}.md").write_text("\n".join(md))
    print(f"wrote c3f-universe-prune-{DATE}.json and .md")


main()
