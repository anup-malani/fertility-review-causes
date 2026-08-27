#!/usr/bin/env python3
"""
228 — A.23 screen assembly and gold audit.

TICK-075. Merges the 29 verdict files back onto the frame, and does the thing the
blinding was for: checks how the screen treated the GATED ANCHORS it could not see.

The frame marked which records were gold and which were decoys; the batches withheld
both. So the screen's verdicts on those records are an out-of-sample test of the
rubric, not a restatement of the anchor set. Three numbers matter:

  * gold recall -- what share of gold candidates the screen kept (RELEVANT or
    UNCERTAIN). A gold record marked NOT_RELEVANT is a screen failure and is named.
  * decoy rejection -- what share of the deliberate off-cell decoys the screen routed
    out. A decoy marked RELEVANT is the other failure mode.
  * `exposure_is_arrangement` on the eight anchors reclassified in 222/223 -- these
    are the records whose exposure is the grandmother's time rather than the
    arrangement. If the screen independently says `no` on them, the rubric's central
    test works at scale; if it says `yes`, the reclassification rests on the audit
    alone.

Also reports the routing distribution, the `cannot_tell` share on the Ruling-1
configuration split (the measurement §6 promised), and the no-abstract bucket's
verdicts.

Usage: python3 source/build/goldset/228_a23_assemble_screen.py
"""
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
LOGS = ROOT / "literature" / "search-logs"
HERE = Path(__file__).resolve().parent
FRAME = LOGS / "co-residence-parents-household-delay-frame.json"
VDIR = HERE / "a23_screen_verdicts"
OUT = LOGS / "co-residence-parents-household-delay-screened.json"
REPORT = LOGS / "co-residence-parents-household-delay-screen-report.md"

RECLASSIFIED = {
    "10.1016/j.jpubeco.2023.104928", "10.1093/cesifo/ifu030",
    "10.1016/j.econlet.2025.112239", "10.1007/s10797-023-09822-9",
    "10.1093/esr/jcad040", "10.4054/demres.2014.31.1",
    "10.1371/journal.pone.0286496", "10.1098/rspb.2011.1424",
    "10.1007/s10680-012-9273-2",
}


def main():
    doc = json.loads(FRAME.read_text())
    frame = {r["openalex"]: r for r in doc["records"]}

    verdicts = {}
    for f in sorted(VDIR.glob("verdict_*.json")):
        for v in json.loads(f.read_text())["verdicts"]:
            verdicts[v["openalex"]] = v

    missing = [k for k in frame if k not in verdicts]
    extra = [k for k in verdicts if k not in frame]

    merged = []
    for oid, rec in frame.items():
        v = verdicts.get(oid, {})
        merged.append({**{k: rec[k] for k in
                          ("openalex", "doi", "title", "year", "venue", "type",
                           "is_anchor", "anchor_cell", "anchor_gold", "hand_added")},
                       "abstract_present": bool(rec.get("abstract")),
                       **{k: v.get(k) for k in
                          ("verdict", "exposure_is_arrangement", "config", "outcome",
                           "design", "anticipation_flag", "route", "info", "note")}})

    kept = {"RELEVANT", "UNCERTAIN"}
    gold = [m for m in merged if m["anchor_gold"]]
    gold_kept = [m for m in gold if m["verdict"] in kept]
    gold_lost = [m for m in gold if m["verdict"] == "NOT_RELEVANT"]

    anchors = [m for m in merged if m["is_anchor"]]
    decoys = [m for m in anchors if m["anchor_cell"] in
              ("OFF_PRICE_C2c", "ELDER_SUPPORT", "OFF_OUTCOME", "THEORY")]
    decoys_kept_relevant = [m for m in decoys if m["verdict"] == "RELEVANT"]

    recl = [m for m in merged if m["doi"] in RECLASSIFIED]
    recl_agree = [m for m in recl if m["exposure_is_arrangement"] == "no"]

    arr = [m for m in merged if m["exposure_is_arrangement"] == "yes"]
    ct = sum(1 for m in arr if m["config"] == "cannot_tell")
    noabs = [m for m in merged if not m["abstract_present"]]

    meta = {
        "ticket": "TICK-075",
        "frame": len(frame), "screened": len(verdicts),
        "unscreened": missing, "verdicts_without_a_frame_record": extra,
        "verdict": dict(Counter(m["verdict"] for m in merged).most_common()),
        "gold_in_frame": len(gold),
        "gold_kept": len(gold_kept),
        "gold_lost": [{"doi": m["doi"], "title": m["title"]} for m in gold_lost],
        "decoys_in_frame": len(decoys),
        "decoys_marked_relevant": [{"doi": m["doi"], "title": m["title"]}
                                   for m in decoys_kept_relevant],
        "reclassified_anchors_in_frame": len(recl),
        "reclassified_anchors_screen_says_not_arrangement": len(recl_agree),
        "exposure_is_arrangement": dict(Counter(m["exposure_is_arrangement"] for m in merged).most_common()),
        "config_cannot_tell_share_among_arrangement_records":
            round(100 * ct / max(1, len(arr)), 1),
        "no_abstract": len(noabs),
        "no_abstract_verdicts": dict(Counter(m["verdict"] for m in noabs).most_common()),
        "no_abstract_marked_not_relevant": sum(1 for m in noabs if m["verdict"] == "NOT_RELEVANT"),
        "routes": dict(Counter(m["route"] for m in merged).most_common()),
        "design_among_arrangement_records": dict(Counter(m["design"] for m in arr).most_common()),
        "hand_added_verdicts": {m["doi"]: m["verdict"] for m in merged if m["hand_added"]},
    }
    OUT.write_text(json.dumps({"meta": meta, "records": merged}, indent=1))

    print(json.dumps(meta, indent=1)[:4000])
    print(f"\nwrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
