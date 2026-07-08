#!/usr/bin/env python3
"""
47_merge_refreeze_gate.py — merge rebuilt anchors, re-freeze, re-grade, evaluate the health gate.

Runs after the CLEAN re-run (44 de-ghost, 45 re-grade, 46 rebuild). Produces the rebuilt gold
the end-to-end number is measured on, and decides whether to proceed to the screen:

  1. de-ghosted Tier B survivors (44, clean)  UNION  46's verified net-new canon anchors
     (existence-gated; keyed on their real DOI) -> re-frozen Tier B v2.
  2. build estimand tags for the new anchors from their enumeration cell.
  3. re-grade estimand-filtered Recall(B) on the rebuilt gold (reuse 22's matching, as 45 does).
  4. HEALTH GATE (Shravan 2026-07-08): estimand-filtered Recall(B) >= 0.80 -> PROCEED to screen;
     else PAUSE. (Recall-only gate; anchor count may sit a bit under the §7.2 floor of 30.)

Writes a machine-readable decision file the orchestrator reads to branch.

Inputs : {slug}-tier-a-frozen.json, {slug}-tier-b-deghosted.json (clean),
         {slug}-gold-rebuild-verified.json, estimand_tierb_tags_deghosted.json,
         {slug}-external-backbone.json, {slug}-screened.json
Outputs: {slug}-tier-b-rebuilt.json, estimand_tierb_tags_rebuilt.json,
         {slug}-rebuilt-recall.md, {slug}-gate-decision.json
"""
import json, importlib.util, random, sys
from pathlib import Path
from collections import Counter

SLUG = "old-age-security-pension-crowdout"
HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
LOGS = REPO / "literature" / "search-logs"
OUT = REPO / "output"
GATE = 0.80

def load_cv():
    spec = importlib.util.spec_from_file_location("cv22", HERE / "22_cv_breadth.py")
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

def main():
    m = load_cv()
    A = json.load(open(LOGS / f"{SLUG}-tier-a-frozen.json"))
    Bd = json.load(open(LOGS / f"{SLUG}-tier-b-deghosted.json"))
    verified = json.load(open(LOGS / f"{SLUG}-gold-rebuild-verified.json"))
    tags = {t["id"]: t for t in json.load(open(HERE / "estimand_tierb_tags_deghosted.json"))}

    have = {(g.get("doi") or "").lower().replace("https://doi.org/","") for g in Bd if g.get("doi")}
    B = list(Bd)
    added = 0
    for v in verified:
        doi = (v.get("doi") or "").lower().replace("https://doi.org/","")
        if not doi or doi in have:
            continue
        have.add(doi)
        pid = doi                                     # key new anchors on their DOI
        B.append({"paperId": pid, "doi": doi, "title": v.get("matched_title") or v["enum_title"],
                  "year": v.get("resolved_year") or v.get("enum_year"),
                  "authors": v.get("enum_author"), "provenance_tier": "B",
                  "screen_verdict": "RELEVANT", "screen_confidence": "canon-verified",
                  "screen_reason": f"rebuilt existence-gated canon anchor ({v['source']})"})
        tags[pid] = {"id": pid, "cell": v["cell"], "confidence": "canon-verified",
                     "outcome": "fertility" if v["cell"] == "PRIMARY" else "n/a",
                     "direction": "forward", "mechanism": "canon enumeration",
                     "reason": f"existence-gated canon anchor: {v['enum_author']} {v['enum_year']}"}
        added += 1

    json.dump(B, open(LOGS / f"{SLUG}-tier-b-rebuilt.json", "w"), indent=2, ensure_ascii=False)
    surv_tags = [t for t in tags.values() if t["id"] in {g["paperId"] for g in B}]
    json.dump(surv_tags, open(HERE / "estimand_tierb_tags_rebuilt.json", "w"), indent=2, ensure_ascii=False)

    # re-grade recall (same title-match CV as 45)
    gold = [{"title": g["title"], "tier": "A", "pid": None} for g in A] + \
           [{"title": g["title"], "tier": "B", "pid": g.get("paperId")} for g in B]
    bb_f, bb_p = m.load_backbone(); nc, nn = m.neg_counts()
    rows = [m.cv(gold, bb_f, bb_p, nc, nn, Nf, Np) for Nf in m.GRID for Np in m.GRID]
    front = sorted(rows, key=lambda r: -r["recall"])[:8]
    for r in front: r["neg_matched"] = m.budget_proxy(gold, bb_f, bb_p, nc, nn, r["Nf"], r["Np"])
    top = max(r["recall"] for r in rows)
    near = [r for r in front if r["recall"] >= top - 0.005]
    sel = min(near, key=lambda r: r["neg_matched"]) if near else max(rows, key=lambda r: r["recall"])
    Nf, Np = sel["Nf"], sel["Np"]
    rnd = random.Random(m.SEED); idx = list(range(len(gold))); rnd.shuffle(idx)
    folds = [idx[i::m.K_FOLDS] for i in range(m.K_FOLDS)]
    rec = {}
    for k in range(m.K_FOLDS):
        test = set(folds[k]); train = [gold[i]["title"] for i in idx if i not in test]
        mf, mp = m.mine(train, nc, nn)
        ft = bb_f + [m.compile_term(w) for w in mf[:Nf]]; pt = bb_p + [m.compile_term(w) for w in mp[:Np]]
        for i in folds[k]:
            nt = " " + m.norm(gold[i]["title"]) + " "
            rec[i] = m.title_matches_block(nt, ft) and m.title_matches_block(nt, pt)
    B_idx = [i for i in range(len(gold)) if gold[i]["tier"] == "B"]
    cell_of = lambda i: tags.get(gold[i]["pid"], {}).get("cell", "?")
    prim_idx = [i for i in B_idx if cell_of(i) == "PRIMARY"]
    prim_hit = sum(1 for i in prim_idx if rec[i])
    prim_n = len(prim_idx)
    recall = prim_hit / prim_n if prim_n else float("nan")
    top_hit = sum(1 for i in B_idx if rec[i])
    cells = Counter(cell_of(i) for i in B_idx)

    passed = prim_n > 0 and recall >= GATE
    decision = {"rebuilt_tier_b": len(B), "added_anchors": added,
                "primary_denominator": prim_n, "primary_hits": prim_hit,
                "estimand_recall_B": round(recall, 4) if prim_n else None,
                "topical_recall_B": round(top_hit / len(B_idx), 4),
                "selected_breadth": {"Nf": Nf, "Np": Np}, "gate": GATE,
                "gate_passed": passed,
                "action": "PROCEED_TO_SCREEN" if passed else "PAUSE",
                "tier_b_cells": dict(cells)}
    json.dump(decision, open(OUT / f"{SLUG}-gate-decision.json", "w"), indent=2)

    L = [f"# Rebuilt-gold recall + health gate — {SLUG}", "",
         f"Rebuilt Tier B = {len(B)} (de-ghosted survivors + {added} existence-gated canon anchors). "
         f"Estimand-filtered Recall(B) re-graded on the rebuilt denominator.", "",
         f"- **estimand-filtered Recall(B) = {recall:.1%} ({prim_hit}/{prim_n})**  vs gate ≥ {GATE:.0%}  → "
         f"**{'PASS → proceed to screen' if passed else 'BELOW → PAUSE'}**",
         f"- topical Recall(B) = {top_hit}/{len(B_idx)} ({top_hit/len(B_idx):.1%})",
         f"- selected breadth Nf={Nf}, Np={Np}",
         f"- PRIMARY denominator = {prim_n} (§7.2 floor 30: {'met' if prim_n>=30 else 'under, accepted per recall-only gate'})", "",
         "Cells: " + ", ".join(f"{c} {n}" for c, n in sorted(cells.items(), key=lambda kv: -kv[1]))]
    (OUT / f"{SLUG}-rebuilt-recall.md").write_text("\n".join(L) + "\n")

    print(f"rebuilt Tier B {len(B)} (+{added}); PRIMARY {prim_n}", file=sys.stderr)
    print(f"estimand Recall(B) {recall:.1%} ({prim_hit}/{prim_n}) vs {GATE:.0%} -> {decision['action']}", file=sys.stderr)

if __name__ == "__main__":
    main()
