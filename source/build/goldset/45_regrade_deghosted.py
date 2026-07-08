#!/usr/bin/env python3
"""
45_regrade_deghosted.py — the HONEST recall re-grade, on the de-ghosted gold.

Same chain as 42_cv_refit_frozen.py, but the Tier-B denominator is the de-ghosted set
(44_deghost_gold.py) — real papers only, ghosts quarantined. Re-selects breadth on the
recall/budget frontier over the de-ghosted gold (the fold-local mined terms shift once the
ghost titles are gone), refits the production query, and grades estimand-filtered Recall(B)
against the pre-registered 0.80 bar. This number supersedes the retracted 82.5%.

Tier A is used unchanged (it is clean — 11% no-DOI, DOI-resolver-sourced) for the mining
folds; only Tier B (the Recall(B) denominator) is de-ghosted.

Inputs : {slug}-tier-a-frozen.json, {slug}-tier-b-deghosted.json,
         {slug}-external-backbone.json, {slug}-screened.json, estimand_tierb_tags_deghosted.json
Outputs: {slug}-production-query-deghosted.json, {slug}-clean-run-recall-deghosted.json/.md
"""
import json, importlib.util, random, sys
from pathlib import Path
from collections import Counter

SLUG = "old-age-security-pension-crowdout"
HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
LOGS = REPO / "literature" / "search-logs"
OUT = REPO / "output"
PREREG_BAR = 0.80
TOPICAL_BAR = 0.72

def load_cv():
    spec = importlib.util.spec_from_file_location("cv22", HERE / "22_cv_breadth.py")
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

def main():
    m = load_cv()
    A = json.load(open(LOGS / f"{SLUG}-tier-a-frozen.json"))
    B = json.load(open(LOGS / f"{SLUG}-tier-b-deghosted.json"))
    gold = [{"title": g["title"], "tier": "A", "pid": None} for g in A] + \
           [{"title": g["title"], "tier": "B", "pid": g.get("paperId")} for g in B]
    bb_f, bb_p = m.load_backbone(); nc, nn = m.neg_counts()
    tags = {t["id"]: t for t in json.load(open(HERE / "estimand_tierb_tags_deghosted.json"))}
    print(f"de-ghosted gold {len(gold)} (A {len(A)}, B {len(B)})", file=sys.stderr)

    rows = [m.cv(gold, bb_f, bb_p, nc, nn, Nf, Np) for Nf in m.GRID for Np in m.GRID]
    front = sorted(rows, key=lambda r: -r["recall"])[:8]
    for r in front:
        r["neg_matched"] = m.budget_proxy(gold, bb_f, bb_p, nc, nn, r["Nf"], r["Np"])
    top = max(r["recall"] for r in rows)
    near = [r for r in front if r["recall"] >= top - 0.005]
    sel = min(near, key=lambda r: r["neg_matched"]) if near else max(rows, key=lambda r: r["recall"])
    Nf, Np = sel["Nf"], sel["Np"]

    rnd = random.Random(m.SEED); idx = list(range(len(gold))); rnd.shuffle(idx)
    folds = [idx[i::m.K_FOLDS] for i in range(m.K_FOLDS)]
    recovered = {}
    for k in range(m.K_FOLDS):
        test = set(folds[k]); train = [gold[i]["title"] for i in idx if i not in test]
        mf, mp = m.mine(train, nc, nn)
        fterms = bb_f + [m.compile_term(w) for w in mf[:Nf]]
        pterms = bb_p + [m.compile_term(w) for w in mp[:Np]]
        for i in folds[k]:
            nt = " " + m.norm(gold[i]["title"]) + " "
            recovered[i] = m.title_matches_block(nt, fterms) and m.title_matches_block(nt, pterms)

    B_idx = [i for i in range(len(gold)) if gold[i]["tier"] == "B"]
    A_idx = [i for i in range(len(gold)) if gold[i]["tier"] == "A"]
    cell_of = lambda i: tags.get(gold[i]["pid"], {}).get("cell", "?")
    conf_of = lambda i: tags.get(gold[i]["pid"], {}).get("confidence", "?")
    def recall(ii):
        ii = list(ii)
        if not ii: return (float("nan"), 0, 0)
        h = sum(1 for i in ii if recovered[i]); return (h/len(ii), h, len(ii))

    topical = recall(B_idx)
    empirical = recall([i for i in B_idx if cell_of(i) not in ("THEORY","?")])
    primary = recall([i for i in B_idx if cell_of(i) == "PRIMARY"])
    theory = recall([i for i in B_idx if cell_of(i) == "THEORY"])
    prim_high = recall([i for i in B_idx if cell_of(i) == "PRIMARY" and conf_of(i) == "HIGH"])
    recall_A = recall(A_idx)
    cells = Counter(cell_of(i) for i in B_idx)

    mf_full, mp_full = m.mine([g["title"] for g in gold], nc, nn)
    bbraw = json.load(open(LOGS / f"{SLUG}-external-backbone.json"))
    prod = {"hypothesis": SLUG, "deghosted": True, "breadth": {"Nf": Nf, "Np": Np},
            "fertility_block": {"backbone": bbraw["fertility_block"], "mined_expansion": mf_full[:Nf]},
            "pension_oas_block": {"backbone": bbraw["pension_oas_block"], "mined_expansion": mp_full[:Np]}}
    json.dump(prod, open(LOGS / f"{SLUG}-production-query-deghosted.json", "w"), indent=2, ensure_ascii=False)

    passed = primary[0] >= PREREG_BAR if primary[2] else False
    result = {"deghosted": True, "selected_breadth": {"Nf": Nf, "Np": Np},
              "cv_recall_selected": sel["recall"], "neg_matched_selected": sel.get("neg_matched"),
              "recall": {"topical": topical, "empirical": empirical, "estimand_primary": primary,
                         "theory": theory, "primary_high_conf": prim_high, "tier_a": recall_A},
              "tier_b_cells": dict(cells), "tier_b_n": len(B_idx),
              "prereg_bar_estimand": PREREG_BAR, "estimand_pass": passed}
    json.dump(result, open(OUT / f"{SLUG}-clean-run-recall-deghosted.json", "w"), indent=2)

    def pct(r): return f"{r[0]:.1%} ({r[1]}/{r[2]})" if r[2] else "n/a (0)"
    verdict = "PASS" if passed else "BELOW BAR"
    L = [f"# HONEST recall re-grade on the de-ghosted gold — {SLUG}", "",
         "Supersedes the retracted 82.5% (which counted ghost anchors as recall hits). Same chain as "
         "`42`, but the Tier-B denominator is the de-ghosted set (real papers only; ghosts quarantined "
         f"by `44`). Estimand-filtered Recall(B) vs the pre-registered {PREREG_BAR:.0%} bar.", "",
         f"## De-ghosted Tier B: {len(B_idx)} papers (was 257)", "",
         "| Cell | Count | Share |", "|---|---|---|"]
    for c, n in sorted(cells.items(), key=lambda kv: -kv[1]):
        L.append(f"| {c} | {n} | {n/max(len(B_idx),1):.0%} |")
    L += ["", f"Selected breadth (re-fit on de-ghosted gold): **Nf={Nf}, Np={Np}** · CV recall "
          f"{sel['recall']:.1%} · budget {sel.get('neg_matched')} negs", "",
          "## Recall (honest denominator)", "",
          "| Recall(B) against ... | value | bar | verdict |", "|---|---|---|---|",
          f"| **estimand-filtered (PRIMARY, real)** | {pct(primary)} | ≥ {PREREG_BAR:.0%} | **{verdict}** |",
          f"| topical (all de-ghosted Tier B) | {pct(topical)} | ≥ {TOPICAL_BAR:.0%} | {'PASS' if topical[0]>=TOPICAL_BAR else 'BELOW'} |",
          f"| empirical (drop theory) | {pct(empirical)} | — | — |",
          f"| memo: theory | {pct(theory)} | — | — |",
          f"| memo: PRIMARY high-confidence | {pct(prim_high)} | — | — |",
          f"| memo: Recall(A) over Tier A | {pct(recall_A)} | — | — |", "",
          "## Reading", "",
          f"On the ghost-purged denominator, estimand-filtered Recall(B) = **{pct(primary)}** vs the "
          f"pre-registered {PREREG_BAR:.0%} → **{verdict}**. "
          + ("This is the honest recall of the *real* primary-cell literature; it holds the bar even "
             "after removing the fictional anchors that flattered the earlier number."
             if passed else
             "Removing the ghosts drops the estimand recall below the pre-registered bar — the real "
             "recall of retrievable primary-cell papers is lower than the ghost-inflated 82.5% implied. "
             "This is the true state of the search and must be reported as such; the query needs "
             "recall work (breadth/snowball) before this chapter's search is at benchmark."), "",
          "*Title-only matching (conservative lower bound). Tier A used unchanged (clean) for mining.*"]
    (OUT / f"{SLUG}-clean-run-recall-deghosted.md").write_text("\n".join(L) + "\n")

    print(f"de-ghosted Tier B {len(B_idx)}  cells {dict(cells)}", file=sys.stderr)
    print(f"estimand Recall(B) {pct(primary)}  vs {PREREG_BAR:.0%} -> {verdict}", file=sys.stderr)
    print(f"topical {pct(topical)}  theory {pct(theory)}", file=sys.stderr)

if __name__ == "__main__":
    main()
