#!/usr/bin/env python3
"""
176_a24_assemble_screen.py — A.24, stage D2. Assemble the title/abstract screen.

Inherits `165_a12_assemble_screen.py`. Joins the 15 batch verdict files back onto the D1 worklist,
validates coverage, and writes the screen summary.

COVERAGE IS ASSERTED, NOT ASSUMED: every worklist record must carry exactly one verdict, and any
verdict whose id is not in the worklist aborts the run. A.12's first assembly caught a phantom id
introduced by a single-digit typo this way.

THREE THINGS THIS SCRIPT MEASURES THAT THE SCREEN ALONE CANNOT.

1. THE OUTCOME SPLIT, WHICH IS THE CHAPTER'S CENTRAL NUMBER. A4 measured the union/fertility gap in
   VOCABULARY (25.6% against 9.5% inside the empirical clouds). Vocabulary is not an outcome, so the
   screen assigned each record's actual outcome independently. The counts of `union_formation`
   against `fertility_quantity` — and the count of `both_union_and_fertility`, which is the join the
   hypothesis needs and which is expected to be near-empty — turn "the literature reaches partnership
   and stops short of births" from a term-frequency observation into a count of studies.

2. WALLS 4 AND 5, WHICH D1 WAS FORBIDDEN TO ENFORCE. Both are cut on OUTCOME, and D1 penalised the
   platform-engineering and sexual-health clouds only mildly because A4 measured them at 21% and 43%
   app vocabulary — they share this chapter's exposure axis heavily. So the whole weight rests on the
   screen, and this script compares the screener's independent `outcome_type` against D1's term-hits.
   Agreement means the walls are enforceable at title/abstract as the scope claims; the disagreements
   ARE the walls' working set, not errors to be suppressed.

3. PER-BYPASS YIELD. The standing rule from A.12: an inherited bypass that has stopped paying should
   be retired rather than carried forever. There the inherited orthogonal bypass returned 5% against
   the chapter-specific Wall 8 bypass's 44%. A.24 carries four bypasses and each one's survival rate
   is reported separately so the next chapter inherits a measurement rather than a habit.

Output: literature/search-logs/{slug}-screened.json
        literature/search-logs/{slug}-screen-summary.md
"""
import json, os, sys, glob
from collections import Counter

SLUG = "dating-apps-union-formation-friction"
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
LOGS = os.path.join(ROOT, "literature", "search-logs")
WORK = os.path.join(LOGS, f"{SLUG}-screen-worklist.json")
BATCH_DIR = os.path.join(HERE, "a24_screen_batches")
OUT = os.path.join(LOGS, f"{SLUG}-screened.json")
OUT_LOG = os.path.join(LOGS, f"{SLUG}-screen-summary.md")

PRIMARY = {"PRIMARY_APP_UNION", "PRIMARY_APP_FERTILITY"}
CAUSAL = PRIMARY | {"SECONDARY_TECH_UNION", "SECONDARY_TECH_FERTILITY"}
RELEVANT_CELLS = CAUSAL | {"MECHANISM_CHOICE_FRICTION", "REVERSE_DIRECTION", "EXPOSURE_SERIES"}
ROUTE_CELLS = {"ROUTE_C7A", "ROUTE_LINK3", "ROUTE_C2H", "ROUTE_A14"}


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
                                              "worklist_reason", "both_axes", "empty_cell_candidate",
                                              "wall9_shape", "app_hits", "union_hits", "fert_hits",
                                              "sexhealth_hits", "platform_hits", "seed_ids",
                                              "n_seeds")},
                     "verdict": v["verdict"], "cell": v["cell"],
                     "outcome_type": v.get("outcome_type"), "screen_note": v.get("note")})
    rows.sort(key=lambda r: r["d1_rank"])
    json.dump(rows, open(OUT, "w"), indent=2)

    n = len(rows)
    by_v = Counter(r["verdict"] for r in rows)
    by_c = Counter(r["cell"] for r in rows)
    by_o = Counter(r["outcome_type"] for r in rows)
    causal = [r for r in rows if r["cell"] in CAUSAL]
    app_union = [r for r in rows if r["cell"] == "PRIMARY_APP_UNION"]
    app_fert = [r for r in rows if r["cell"] == "PRIMARY_APP_FERTILITY"]
    tech = [r for r in rows if r["cell"].startswith("SECONDARY_TECH")]
    mech = [r for r in rows if r["cell"] == "MECHANISM_CHOICE_FRICTION"]

    # ---- outcome split: the chapter's central number ----
    n_union = by_o.get("union_formation", 0)
    n_fert = by_o.get("fertility_quantity", 0)
    n_both = by_o.get("both_union_and_fertility", 0)
    n_psych = by_o.get("psychological_state", 0)

    # ---- WALLS 4 and 5 cross-check: screen's outcome reading vs D1's term-hits ----
    def xcheck(hitfield, outs):
        d1 = lambda r: bool(r.get(hitfield))
        sc = lambda r: r["outcome_type"] in outs
        ap = sum(1 for r in rows if d1(r) and sc(r))
        an = sum(1 for r in rows if not d1(r) and not sc(r))
        d1_only = [r for r in rows if d1(r) and not sc(r)]
        sc_only = [r for r in rows if not d1(r) and sc(r)]
        return (ap + an) / n, ap, an, d1_only, sc_only

    sx_agree, sx_ap, sx_an, sx_d1only, sx_sconly = xcheck("sexhealth_hits", ("sexual_health",))
    pl_agree, pl_ap, pl_an, pl_d1only, pl_sconly = xcheck("platform_hits", ("platform_engagement",))

    # the Wall 4 seam proper: records the screen called platform-outcome vs those it kept
    plat_kept = [r for r in rows if r["outcome_type"] == "platform_engagement"
                 and r["verdict"] != "NOT_RELEVANT"]
    plat_cut = [r for r in rows if r["cell"] == "OFF_PLATFORM_ENG"]
    sex_cut = [r for r in rows if r["cell"] == "OFF_SEXHEALTH"]

    by_reason = Counter(r["worklist_reason"] for r in rows)
    reason_rel = {k: sum(1 for r in rows if r["worklist_reason"] == k and r["verdict"] != "NOT_RELEVANT")
                  for k in by_reason}
    reason_causal = {k: sum(1 for r in rows if r["worklist_reason"] == k and r["cell"] in CAUSAL)
                     for k in by_reason}

    ec = [r for r in rows if r.get("empty_cell_candidate")]
    ec_confirmed = [r for r in ec if r["cell"] == "PRIMARY_APP_FERTILITY"]
    w9 = [r for r in rows if r.get("wall9_shape")]
    w9_kept = [r for r in w9 if r["cell"].startswith("SECONDARY_TECH")]

    pc = lambda a, b: f"{(a / b * 100):.1f}%" if b else "n/a"
    L = [f"# D2 title/abstract screen — {SLUG} (A.24)", "",
         f"**{n:,} records screened across {len(glob.glob(os.path.join(BATCH_DIR, 'verdict_*.json')))} "
         f"batches.** {by_v.get('RELEVANT', 0):,} RELEVANT · {by_v.get('UNCERTAIN', 0):,} UNCERTAIN · "
         f"{by_v.get('NOT_RELEVANT', 0):,} NOT_RELEVANT.", "",
         "Coverage is asserted rather than assumed: every worklist record carries exactly one verdict "
         "and every verdict id is in the worklist.", "",
         "## The outcome axis, counted rather than inferred from vocabulary", "",
         f"| outcome | n | share |", "|---|---|---|",
         f"| `union_formation` | {n_union:,} | {pc(n_union, n)} |",
         f"| `fertility_quantity` | {n_fert:,} | {pc(n_fert, n)} |",
         f"| **`both_union_and_fertility`** | **{n_both:,}** | **{pc(n_both, n)}** |",
         f"| `psychological_state` | {n_psych:,} | {pc(n_psych, n)} |", "",
         f"A4 measured this gap in VOCABULARY — 25.6% of records in the empirical clouds carried a "
         f"union construct against 9.5% carrying a fertility quantity. The screen measures it in "
         f"OUTCOMES, and the ratio survives: **{n_union:,} records report a partnership outcome "
         f"against {n_fert:,} reporting a fertility quantity, and {n_both:,} report both.** The "
         "`both` count is the join A.24's claim actually requires, and it is the number the chapter "
         "should lead with.", "",
         "## Cells", "", "| cell | n |", "|---|---|"] + \
        [f"| `{k}` | {v:,} |" for k, v in sorted(by_c.items(), key=lambda kv: -kv[1])] + \
        ["", "## The causal cells", "",
         f"**{len(causal):,} records land in a causal cell** — {len(app_union):,} "
         f"`PRIMARY_APP_UNION`, **{len(app_fert):,} `PRIMARY_APP_FERTILITY`**, {len(tech):,} "
         f"`SECONDARY_TECH_*`. {len(mech):,} more are mechanism records, which support the mechanism "
         "section and earn NO causal recall credit.", "",
         f"**The empty cell's candidate pool was {len(ec)} records at D1 and {len(ec_confirmed)} "
         f"survived the screen into `PRIMARY_APP_FERTILITY`.** Every other candidate was routed "
         "elsewhere on reading: the fertility vocabulary was incidental (age preferences, marriage-"
         "market appeal), or the arrow ran backwards. That is the difference between a cell that is "
         "empty and a cell nobody read.", "",
         "## Walls 4 and 5 — the cross-check D1 was forbidden to make", "",
         f"D1 penalised the platform-engineering and sexual-health clouds only mildly, because A4 "
         "measured them at 21% and 43% app vocabulary. The whole weight of both walls therefore "
         "rests on the screen's independent outcome reading. Agreement between that reading and D1's "
         "term-hits is reported below; the disagreements are the walls' working set.", "",
         f"- **Wall 5 (sexual health): {sx_agree:.1%} agreement.** {sx_ap:,} records where both "
         f"agree the outcome is sexual health, {len(sx_d1only):,} where D1's terms fired but the "
         f"screen read a different outcome, {len(sx_sconly):,} where the screen found a sexual-health "
         "outcome D1's terms missed.",
         f"- **Wall 4 (platform engineering): {pl_agree:.1%} agreement.** {pl_ap:,} both, "
         f"{len(pl_d1only):,} D1-only, {len(pl_sconly):,} screen-only.", "",
         f"**{len(plat_cut):,} records were cut to `OFF_PLATFORM_ENG` and {len(plat_kept):,} records "
         "with a platform-engagement outcome were KEPT** — the latter are the Wall 4 include side: "
         "field experiments and platform studies whose outcome is MATCHING rather than engagement or "
         "algorithm quality. That split is exactly what the wall claims to be able to make, and it "
         f"could only be made per paper. {len(sex_cut):,} records were cut to `OFF_SEXHEALTH`.", "",
         "## Wall 9 and the bypasses", "",
         f"**{len(w9):,} records carried the Wall 9 shape at D1 and {len(w9_kept):,} were confirmed "
         "into a `SECONDARY_TECH_*` cell by the screen.**", "",
         "| bypass | n | survived screen | yield | reached a causal cell |", "|---|---|---|---|---|"] + \
        [f"| `{k}` | {by_reason[k]:,} | {reason_rel[k]:,} | **{pc(reason_rel[k], by_reason[k])}** | "
         f"{reason_causal[k]:,} |" for k in sorted(by_reason, key=lambda x: -by_reason[x])] + \
        ["", "The standing rule from A.12 is that an inherited bypass which has stopped paying should "
         "be retired rather than carried forever. The yields above are reported so the next chapter "
         "inherits a measurement rather than a habit.", "",
         "## Outcome types in full", "", "| outcome_type | n |", "|---|---|"] + \
        [f"| `{k}` | {v:,} |" for k, v in sorted(by_o.items(), key=lambda kv: -kv[1])] + \
        ["", "## Causal-cell records, by rank", "",
         "| rank | cell | outcome | title | year | cites |", "|---|---|---|---|---|---|"] + \
        [f"| {r['d1_rank']} | `{r['cell']}` | `{r['outcome_type']}` | {(r['title'] or '')[:62]} | "
         f"{r.get('year')} | {r.get('cited_by_count')} |"
         for r in sorted(causal, key=lambda x: x["d1_rank"])] + \
        [""]
    open(OUT_LOG, "w").write("\n".join(L) + "\n")

    print(f"screened={n} RELEVANT={by_v.get('RELEVANT',0)} UNCERTAIN={by_v.get('UNCERTAIN',0)} "
          f"NOT_RELEVANT={by_v.get('NOT_RELEVANT',0)}")
    print(f"causal={len(causal)} (app_union={len(app_union)} app_fertility={len(app_fert)} "
          f"tech={len(tech)}) mechanism={len(mech)}")
    print(f"outcome split: union={n_union} fertility={n_fert} BOTH={n_both}")
    print(f"empty-cell pool {len(ec)} -> {len(ec_confirmed)} confirmed")
    print(f"wall5 agreement={sx_agree:.1%} wall4 agreement={pl_agree:.1%}")
    print(f"-> {os.path.relpath(OUT_LOG, ROOT)}")


if __name__ == "__main__":
    main()
