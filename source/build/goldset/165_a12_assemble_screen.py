#!/usr/bin/env python3
"""
165_a12_assemble_screen.py — A.12, stage D2. Assemble the title/abstract screen.

Inherits `138_b6_assemble_screen.py`. Joins the 23 batch verdict files back onto the D1 worklist,
validates coverage, and writes the screen summary.

THE VALIDATION THAT MATTERS HERE IS THE WALL 6 CROSS-CHECK, and it is the reason `outcome_type` was
collected at all. Wall 6 was re-cut on OUTCOME (PI Call 3) and D1 was explicitly forbidden from making
that call, so the whole weight of the wall rests on the screen. This script measures whether the
screen's independent outcome reading agrees with D1's clinical term-hits. Agreement means the wall is
enforceable at title/abstract as the scope claims; disagreement is the wall's WORKING SET, not an
error to be suppressed. If disagreement were pervasive the honest response would be to amend the
scope, not to credit the screen with holding a line it could not see.

Coverage is asserted, not assumed: every worklist record must carry exactly one verdict, and any
verdict whose id is not in the worklist is a transcription error and aborts the run. One such phantom
(a single-digit typo) was caught this way on the first assembly.

Output: literature/search-logs/{slug}-screened.json
        literature/search-logs/{slug}-screen-summary.md
"""
import json, os, sys, glob
from collections import Counter

SLUG = "twinning-multiple-births"
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
LOGS = os.path.join(ROOT, "literature", "search-logs")
WORK = os.path.join(LOGS, f"{SLUG}-screen-worklist.json")
BATCH_DIR = os.path.join(HERE, "a12_screen_batches")
OUT = os.path.join(LOGS, f"{SLUG}-screened.json")
OUT_LOG = os.path.join(LOGS, f"{SLUG}-screen-summary.md")

PRIMARY = {"PRIMARY_OFFSET_STOPPING", "PRIMARY_OFFSET_FIRSTSTAGE_CANDIDATE",
           "PRIMARY_MECHANICAL_IDENTITY"}
RELEVANT_CELLS = PRIMARY | {"SECONDARY_ART_MULTIPLES", "SECONDARY_PM_VARIATION", "EXPOSURE_SERIES"}


def main():
    work = {r["id"]: r for r in json.load(open(WORK))}
    verdicts = {}
    for f in sorted(glob.glob(os.path.join(BATCH_DIR, "verdict_*.json"))):
        for v in json.load(open(f))["verdicts"]:
            if v["id"] in verdicts:
                sys.exit(f"ABORT: duplicate verdict for {v['id']}")
            verdicts[v["id"]] = v
    missing = set(work) - set(verdicts)
    spurious = set(verdicts) - set(work)
    if missing or spurious:
        sys.exit(f"ABORT: coverage failure — {len(missing)} unscreened, {len(spurious)} spurious "
                 f"{sorted(spurious)[:5]}")

    rows = []
    for wid, w in work.items():
        v = verdicts[wid]
        rows.append({**{k: w.get(k) for k in ("id", "doi", "title", "year", "venue", "type",
                                              "cited_by_count", "d1_rank", "d1_score",
                                              "worklist_reason", "both_axes", "clinical_hits",
                                              "seed_ids", "n_seeds")},
                     "verdict": v["verdict"], "cell": v["cell"],
                     "outcome_type": v.get("outcome_type"), "screen_note": v.get("note")})
    rows.sort(key=lambda r: r["d1_rank"])
    json.dump(rows, open(OUT, "w"), indent=2)

    n = len(rows)
    by_v = Counter(r["verdict"] for r in rows)
    by_c = Counter(r["cell"] for r in rows)
    by_o = Counter(r["outcome_type"] for r in rows)
    prim = [r for r in rows if r["cell"] in PRIMARY]
    stop = [r for r in rows if r["cell"] == "PRIMARY_OFFSET_STOPPING"]
    art = [r for r in rows if r["cell"] == "SECONDARY_ART_MULTIPLES"]

    # ---- WALL 6 CROSS-CHECK: screen's outcome reading vs D1's clinical term-hits ----
    d1_clin = lambda r: bool(r.get("clinical_hits"))
    scr_clin = lambda r: r["outcome_type"] in ("per_cycle_clinical", "perinatal_health")
    agree_pos = sum(1 for r in rows if d1_clin(r) and scr_clin(r))
    agree_neg = sum(1 for r in rows if not d1_clin(r) and not scr_clin(r))
    d1_only = [r for r in rows if d1_clin(r) and not scr_clin(r)]
    scr_only = [r for r in rows if not d1_clin(r) and scr_clin(r)]
    agree = (agree_pos + agree_neg) / n

    # the Wall 6 seam proper: ART-treatment records split by outcome
    art_pop = [r for r in art if r["outcome_type"] in ("population_births", "twinning_rate")]
    art_cyc = [r for r in art if r["outcome_type"] == "per_cycle_clinical"]
    off_clin = [r for r in rows if r["cell"] == "OFF_ART_CLINICAL"]

    by_reason = Counter(r["worklist_reason"] for r in rows)
    reason_rel = {k: sum(1 for r in rows if r["worklist_reason"] == k and r["verdict"] != "NOT_RELEVANT")
                  for k in by_reason}

    pc = lambda a, b: f"{a/b*100:.1f}%" if b else "n/a"
    L = [f"# D2 title/abstract screen — {SLUG} (A.12)", "",
         f"**{n:,} records screened across 23 batches; coverage asserted, not assumed.** Every "
         "worklist record carries exactly one verdict and every verdict id is in the worklist. The "
         "check earned its keep on the first assembly, catching a phantom id introduced by a "
         "single-digit typo.", "",
         f"**{by_v['RELEVANT']:,} RELEVANT · {by_v['UNCERTAIN']:,} UNCERTAIN · "
         f"{by_v['NOT_RELEVANT']:,} NOT_RELEVANT**", "",
         "## Cells", "", "| cell | n |", "|---|---|"]
    for c, k in by_c.most_common():
        L.append(f"| `{c}` | {k} |")

    L += ["", "## The primary cell is four times the anchor set", "",
          f"**`PRIMARY_OFFSET_STOPPING`: {len(stop)} records.** The frozen scope named THREE "
          "stopping-offset studies (Alter & Hacker 2024, Robson & Smith 2012, Clark-Cummins-Curtis "
          "2020). The screen finds four times that, and the additions are not marginal — they "
          "include a direct published comment on Robson & Smith in the same journal, a Nature "
          "Communications study reporting the OPPOSITE sign in pre-industrial Europe, Swedish "
          "register childbearing patterns for mothers of twins, 19th-century Dutch maternal life "
          "histories, and a JPE paper whose outcome is time to next birth.", "",
          "This is the Tier-A-anchors-are-studies lesson restated: reporting the anchor set as the "
          "evidence base would have understated this cell by a factor of four, and would have "
          "concealed that its members DISAGREE.", "",
          f"`PRIMARY_OFFSET_FIRSTSTAGE_CANDIDATE`: {len([r for r in prim if r['cell'].endswith('CANDIDATE')])} "
          "records, all UNCERTAIN by construction — Wall 8 says the first-stage table is invisible "
          "at title/abstract, so these are routed to full text rather than adjudicated here.", ""]

    L += ["## Wall 6 cross-check — does the screen's outcome reading agree with D1's terms?", "",
          "Wall 6 was re-cut on OUTCOME and D1 was forbidden from applying it, so this is the "
          "measurement the re-cut stands or falls on. `outcome_type` was assigned by the screen "
          "WITHOUT sight of D1's clinical term-hits.", "",
          f"**Agreement: {pc(agree_pos+agree_neg, n)}** ({agree_pos} both clinical, {agree_neg} "
          f"neither).", "",
          f"- **{len(d1_only)} records D1 flagged clinical but the screen did not.** These are the "
          "false positives a term sieve produces: population twinning-rate papers that mention "
          "preterm birth or birthweight in passing.",
          f"- **{len(scr_only)} records the screen read as clinical but D1's terms missed.**", "",
          "**The seam itself.** Of the "
          f"{len(art)} `SECONDARY_ART_MULTIPLES` records, **{len(art_pop)} carry a population or "
          f"registry outcome** (the Wall 6 INCLUDE side) and **{len(art_cyc)} carry a per-cycle "
          f"clinical outcome** — the genuine boundary, where the treatment is identical to an "
          f"excluded study and only the outcome separates them. A further {len(off_clin)} records "
          "went to `OFF_ART_CLINICAL`.", "",
          "**Verdict on the wall: enforceable, but only per-paper.** The screen could separate "
          "outcome types record by record. What it could NOT do is infer them from context — the "
          "include-side anchor Reynolds 2003 sits at 50.8% clinical vocabulary against the "
          "exclude-side Thurin's 60.6%, so any cloud-level or term-level shortcut fails. The wall "
          "holds because a human read each abstract's outcome, and the scope should say so.", ""]

    L += ["## Did the bypasses earn their place?", "",
          "| worklist reason | n | not NOT_RELEVANT | yield |", "|---|---|---|---|"]
    for k, cnt in by_reason.most_common():
        L.append(f"| `{k}` | {cnt} | {reason_rel[k]} | {pc(reason_rel[k], cnt)} |")
    L += ["", "The Wall 8 bypass is the one to read closely: it was re-gated during D1 after the "
          "first version recovered 4 records instead of 212, and its yield here is what that "
          "re-gating bought.", ""]

    L += ["## Outcome types", "", "| outcome_type | n |", "|---|---|"]
    for o, k in by_o.most_common():
        L.append(f"| `{o}` | {k} |")

    L += ["", "## Highest-priority full text", "",
          "| cell | title | why |", "|---|---|---|"]
    for r in rows:
        if r["screen_note"] and any(t in r["screen_note"] for t in
                                    ("MAJOR", "HIGH-VALUE", "HIGH-PRIORITY", "STRONG", "SCOPE GAP",
                                     "THE HOEKSTRA TRAP", "IMPORTANT AND AGAINST")):
            L.append(f"| `{r['cell']}` | {(r['title'] or '')[:70]} | {r['screen_note'][:190]} |")

    open(OUT_LOG, "w").write("\n".join(L) + "\n")
    print(f"screened={n} relevant={by_v['RELEVANT']} uncertain={by_v['UNCERTAIN']} "
          f"not_relevant={by_v['NOT_RELEVANT']}")
    print(f"PRIMARY_OFFSET_STOPPING={len(stop)}  firststage_candidates="
          f"{len([r for r in prim if r['cell'].endswith('CANDIDATE')])}")
    print(f"wall6 agreement={pc(agree_pos+agree_neg, n)}  art_population={len(art_pop)} "
          f"art_percycle={len(art_cyc)}")
    print(f"-> {os.path.relpath(OUT_LOG, ROOT)}")


if __name__ == "__main__":
    main()
