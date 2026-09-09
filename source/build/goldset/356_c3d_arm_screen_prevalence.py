#!/usr/bin/env python3
"""356 — bound the C.3.d forward arms from a partial screen, rather than claiming completeness.

The exhaustive forward-arm screen is 1,776 rows (1,184 target records + 592 decoys) across 30
batches. Two of those batches are screened. `bound-what-you-did-not-screen` is explicit about what
to do here: sample blind with hidden controls, report PREVALENCE with an interval and the
sensitivity that backs it, and never report a partial pass as if it were the population.

Three things this script does that a raw count of the verdict file would not.

**It splits target rows from decoys.** The batches are ~2/3 arm records and ~1/3 size-matched decoys
drawn from the rest of the universe, shuffled, with arm membership withheld from the screener. A
prevalence computed over all screened rows would be a blend of two populations. The decoy rate is
reported too, because it is a free estimate of the NON-forward remainder.

**It reports a Wilson interval.** A point estimate off 80-odd rows invites being quoted as if it
were the count. The interval is the honest object, and it is wide.

**It counts Wall 2 as a share of the FORWARD records, not of all rows.** Scope §8 wall 2 --
C.3.d owns the return to the CHILD's human capital, C.2.e the PARENT's -- is the wall this scope
added, and PI call 3 asks whether scope §7 row 3 should move to C.2.e wholesale. The denominator
that answers that question is "records whose exposure moves a return and whose outcome is
fertility", not "records screened".

Output: literature/search-logs/quantity-quality-tradeoff-arm-screen-prevalence.{json,md}
"""
import csv
import json
import math
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
LOGS = ROOT / "literature" / "search-logs"
BATCH = ROOT / "extraction" / "quantity-quality-tradeoff-screen-batches"
VERD = ROOT / "extraction" / "quantity-quality-tradeoff-screen-verdicts.csv"

TARGET_ARMS = {"forward-shock", "forward-design"}
PRIMARY = {"RETURN_FERTILITY", "SHOCK_FERTILITY"}
# The denominator for the Wall 2 question: a return-moving exposure with a fertility outcome.
FORWARD_FAMILY = PRIMARY | {"MIXED_CHILD_PARENT_RETURN", "MIXED_RETURN_POSITION",
                            "MIXED_RETURN_INCOME"}


def wilson(k, n, z=1.96):
    """Wilson score interval. Reported instead of a bare rate because n is small."""
    if not n:
        return (0.0, 0.0, 0.0)
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (p, max(0.0, c - h), min(1.0, c + h))


def main():
    verdicts = {r["screen_id"]: r for r in csv.DictReader(VERD.open())}
    universe = json.loads((LOGS / "quantity-quality-tradeoff-screen-universe.json").read_text())
    # screen_id is a position in the citation-ranked universe; arm membership lives there, not in
    # the blinded batches.
    arms_of = {f"C3D{i:04d}": set(r.get("arms") or [])
               for i, r in enumerate(universe["records"])}

    done, batches = set(), []
    for p in sorted(BATCH.glob("arms-forward-design-forward-shock-*.json")):
        ids = [r["screen_id"] for r in json.loads(p.read_text())["records"]]
        if all(i in verdicts for i in ids):
            batches.append(p.name)
            done |= set(ids)

    n_target_total = sum(1 for sid, a in arms_of.items() if a & TARGET_ARMS)
    rows = [(sid, verdicts[sid], bool(arms_of.get(sid, set()) & TARGET_ARMS)) for sid in sorted(done)]
    tgt = [(s, v) for s, v, t in rows if t]
    dec = [(s, v) for s, v, t in rows if not t]

    def block(pairs, label):
        n = len(pairs)
        prim = sum(1 for _, v in pairs if v["cell"] in PRIMARY)
        fam = [v for _, v in pairs if v["cell"] in FORWARD_FAMILY]
        w2 = sum(1 for v in fam if "W2_PARENT_RETURN" in (v["wall_risk"] or ""))
        off = sum(1 for _, v in pairs if v["cell"] == "OFF_TOPIC")
        p, lo, hi = wilson(prim, n)
        return {"label": label, "n": n, "primary": prim, "primary_rate": p,
                "primary_lo": lo, "primary_hi": hi, "off_topic": off,
                "forward_family": len(fam), "wall2": w2,
                "wall2_share": (w2 / len(fam)) if fam else None,
                "cells": dict(Counter(v["cell"] for _, v in pairs))}

    t, d = block(tgt, "forward arms (target)"), block(dec, "decoys (rest of universe)")
    proj_lo, proj_hi = t["primary_lo"] * n_target_total, t["primary_hi"] * n_target_total

    blob = {"batches_screened": batches, "n_screened": len(rows),
            "target_records_in_arms": n_target_total,
            "target": t, "decoy": d,
            "projected_primary_in_forward_arms": {"point": t["primary_rate"] * n_target_total,
                                                  "lo": proj_lo, "hi": proj_hi},
            "coverage": len(tgt) / n_target_total if n_target_total else None}
    (LOGS / "quantity-quality-tradeoff-arm-screen-prevalence.json").write_text(
        json.dumps(blob, indent=2) + "\n")

    print(f"{len(batches)} of 30 forward-arm batches screened ({len(rows)} rows)")
    print(f"coverage of the {n_target_total} forward-arm records: {len(tgt)} "
          f"({100*len(tgt)/n_target_total:.1f}%)\n")
    for b in (t, d):
        print(f"{b['label']:28} n={b['n']:>3}  primary {b['primary']:>2} "
              f"({100*b['primary_rate']:.1f}%, 95% CI {100*b['primary_lo']:.1f}–"
              f"{100*b['primary_hi']:.1f}%)   off-topic {b['off_topic']}")
    print(f"\nPROJECTED primary records in the forward arms: "
          f"{proj_lo:.0f}–{proj_hi:.0f} (point {t['primary_rate']*n_target_total:.0f}) "
          f"of {n_target_total}")
    print(f"\nWall 2 (scope §8, C.2.e) among records with a return-moving exposure AND a fertility "
          f"outcome:")
    for b in (t, d):
        if b["forward_family"]:
            print(f"  {b['label']:28} {b['wall2']}/{b['forward_family']} "
                  f"({100*b['wall2_share']:.0f}%)")

    L = ["# C.3.d forward-arm screen — partial, bounded", "",
         "Generated by `source/build/goldset/356_c3d_arm_screen_prevalence.py`. Do not edit by hand.",
         "",
         f"**{len(batches)} of 30 batches screened**, {len(rows)} rows. This is a PARTIAL pass and "
         "is reported as a bound, not a count (`bound-what-you-did-not-screen`). The exhaustive "
         f"screen of {n_target_total} forward-arm records remains outstanding.", "",
         "Batches mix ~2/3 arm records with ~1/3 size-matched decoys from the rest of the universe, "
         "shuffled, with arm membership withheld from the screener. The two populations are "
         "reported separately: a blended rate would describe neither.", "",
         "| population | n | primary | rate | 95% CI (Wilson) | off-topic |",
         "|---|---|---|---|---|---|"]
    for b in (t, d):
        L.append(f"| {b['label']} | {b['n']} | {b['primary']} | {100*b['primary_rate']:.1f}% | "
                 f"{100*b['primary_lo']:.1f}–{100*b['primary_hi']:.1f}% | {b['off_topic']} |")
    L += ["", f"**Projected primary records in the forward arms: {proj_lo:.0f}–{proj_hi:.0f}** "
          f"of {n_target_total}, from the interval above. The point estimate is "
          f"{t['primary_rate']*n_target_total:.0f} and should not be quoted without the range.", "",
          "## Wall 2 — the share that is C.2.e's estimand, not this chapter's", "",
          "Denominator is records whose exposure moves a **return** and whose outcome is "
          "**fertility** — not all screened rows. Scope §8 wall 2 gives C.3.d the return to the "
          "**child's** human capital and C.2.e the **parent's**; PI call 3 asks whether scope §7 "
          "row 3 moves to C.2.e wholesale.", "",
          "| population | wall-2 flagged | forward-family records | share |", "|---|---|---|---|"]
    for b in (t, d):
        if b["forward_family"]:
            L.append(f"| {b['label']} | {b['wall2']} | {b['forward_family']} | "
                     f"{100*b['wall2_share']:.0f}% |")
    L.append("")
    (LOGS / "quantity-quality-tradeoff-arm-screen-prevalence.md").write_text("\n".join(L))
    print(f"\nwrote quantity-quality-tradeoff-arm-screen-prevalence.{{json,md}}")


main()
