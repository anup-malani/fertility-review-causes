#!/usr/bin/env python3
"""
69_b1_cv_breadth.py — B.1 (evolutionary sex drive / contraceptive decoupling), stage A6b.

10-fold CV over the per-block breadth vector, mirroring OAS step 22. The production query is a 2-block
conjunction: (EFFECT block) AND (CAUSE block). A gold paper is RECALLED iff its title matches BOTH blocks.

Each block = a FIXED backbone UNION the top-N fold-local gold-mined discriminative terms at breadth N.

  EFFECT backbone: the definitional fertility/reproductive-outcome vocabulary. A6a showed the on-topic
                   effect language is "reproductive success / reproduction / childbearing", not just
                   "fertility/birth", so the backbone carries both.
  CAUSE backbone : the FORCED decoupling + contraception-severing cluster (design choice (b), confirmed
                   with Shravan 2026-07-21). These terms are conceptually central but empirically rare
                   (they don't reach A6a's discriminative list), so they are FORCED in — the query must
                   not structurally miss a genuine PRIMARY_DECOUPLING paper — while CV allocates the rest
                   of the cause breadth to the data-favored status/mating/motivation/evolutionary terms.

Leakage discipline: backbones are FIXED (a-priori scope vocabulary, leakage-free); the gold-mined
expansion is recomputed from the TRAINING folds' gold only each fold, so held-out recall never sees its
own labels. Matching is TITLE-only (both sides on one footing; a conservative recall lower bound —
abstract matching would only add recall). The production query is refit on the FULL gold at the chosen
(Nf,Np) in A6c after freeze.

Gold: Tier A = the 10 empirical seeds (keyword-sourced, optimistic); Tier B = the screen's
RELEVANT-empirical set (the orthogonal, unbiased sample). Headline = Recall(B); Recall(A)-Recall(B) is
the vocabulary-bias diagnostic. Also reported: recall on the rare PRIMARY_DECOUPLING/DESIRE cells (does
the forced (b) backbone actually rescue them?).

Inputs : output/{slug}-screen-tiers.json, literature/search-logs/{slug}-tier-a.json
Output : literature/search-logs/{slug}-cv-breadth.json + .md
"""
import json, re, math, random, sys
from pathlib import Path
from collections import Counter

SLUG = "evolutionary-sex-drive-contraceptive-decoupling"
HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
LOGS = REPO / "literature" / "search-logs"
OUT = REPO / "output"
K_FOLDS = 10
SEED = 811
ALPHA0 = 1000.0
MIN_GOLD_FOLD = 2
GRID = [0, 3, 6, 10, 15, 20, 30]

PRIMARY_EMPIRICAL = {"PROXIMATE_ULTIMATE", "PRIMARY_DECOUPLING", "PRIMARY_DESIRE_INDEPENDENCE",
                     "MOTIVATION_DISTINCTNESS"}
RARE_CORE = {"PRIMARY_DECOUPLING", "PRIMARY_DESIRE_INDEPENDENCE"}

EFFECT_BACKBONE = ["fertility", "fertilit*", "birth*", "reproductive success", "reproduction",
                   "reproductive", "childbearing", "childbear*", "number of children", "offspring",
                   "completed fertility", "family size", "childless*", "fecundit*", "natality", "parity"]
# Forced (b) cause backbone: decoupling + contraception-severing, conceptually central but rare.
CAUSE_BACKBONE = ["decoupl*", "dissociat*", "uncoupl*", "sever*", "sex from reproduction",
                  "sex without reproduction", "sex without conception", "sex drive", "sexual selection",
                  "contracepti*", "oral contraceptive*", "the pill", "birth control", "family planning"]

STOP = set("the a an of and in on for from to its by is with as at or be this that these those we our "
           "their his her it they i ii iii new evidence using based study studies analysis approach paper "
           "article effect effects impact role case among between within over under are was were has have "
           "had do does can could will would not no more less than into about across after before during "
           "toward towards via per vs versus also two three some how what why when where which who whom "
           "data model models results result human humans".split())

EFFECT = re.compile(r"fertil|childbear|childless|birth|fecund|natalit|offspring|reproducti|"
                    r"number of children|family size|parity|completed fertilit|procreat|babi|quantum")
CAUSE = re.compile(r"evolution|darwin|selection|sociobiolog|life history|adaptive|fitness|biosocial|"
                   r"mating|sexual|sex drive|coital|intercourse|status|wealth|mate |dominance|"
                   r"decoupl|dissociat|sever|uncoupl|contracept|\bpill\b|family planning|birth control|"
                   r"desire for children|childbearing motiv|motivation|proximate|ultimate")


def norm(s):
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9\s]", " ", (s or "").lower())).strip()


def utoks(t):
    return [w for w in norm(t).split() if len(w) > 2 and w not in STOP]


def cand_terms(title):
    u = utoks(title)
    return u + [f"{u[i]} {u[i+1]}" for i in range(len(u) - 1)]


def block_of(term):
    e, c = bool(EFFECT.search(term)), bool(CAUSE.search(term))
    return "effect" if (e and not c) else "cause" if (c and not e) else None


def compile_term(term):
    t = term.strip().lower()
    return ("prefix", norm(t[:-1])) if t.endswith("*") else ("phrase", norm(t))


def matches_block(ntitle_padded, compiled):
    for kind, val in compiled:
        if not val:
            continue
        if kind == "prefix":
            if re.search(r"\b" + re.escape(val), ntitle_padded):
                return True
        elif (" " + val + " ") in ntitle_padded:
            return True
    return False


def mine(train_titles, nc, nn):
    gc = Counter()
    for t in train_titles:
        gc.update(cand_terms(t))
    ng = sum(gc.values())
    ncomb = ng + nn
    eff, cau = [], []
    for w in set(gc):
        if gc[w] < MIN_GOLD_FOLD:
            continue
        b = block_of(w)
        if b is None:
            continue
        comb = gc[w] + nc.get(w, 0)
        aw = ALPHA0 * comb / ncomb
        delta = (math.log((gc[w] + aw) / (ng + ALPHA0 - gc[w] - aw))
                 - math.log((nc.get(w, 0) + aw) / (nn + ALPHA0 - nc.get(w, 0) - aw)))
        z = delta / math.sqrt(1.0 / (gc[w] + aw) + 1.0 / (nc.get(w, 0) + aw))
        (eff if b == "effect" else cau).append((w, z))
    eff.sort(key=lambda x: -x[1])
    cau.sort(key=lambda x: -x[1])
    return [w for w, _ in eff], [w for w, _ in cau]


def load():
    rows = json.load(open(OUT / f"{SLUG}-screen-tiers.json"))
    seeds = json.load(open(LOGS / f"{SLUG}-tier-a.json"))
    gold = [{"title": s["title"], "tier": "A", "cell": s.get("provisional_cell")}
            for s in seeds if s.get("title")]
    for r in rows:
        if r["verdict"] == "RELEVANT" and r.get("evidence_type") != "theory" and r.get("title"):
            gold.append({"title": r["title"], "tier": "B", "cell": r["cell"]})
    neg = [r["title"] for r in rows if r["verdict"] == "NOT_RELEVANT" and r.get("title")]
    nc = Counter()
    for t in neg:
        nc.update(cand_terms(t))
    return gold, nc, sum(nc.values()), neg


def cv(gold, nc, nn, Nf, Np):
    bb_e = [compile_term(t) for t in EFFECT_BACKBONE]
    bb_c = [compile_term(t) for t in CAUSE_BACKBONE]
    rnd = random.Random(SEED)
    idx = list(range(len(gold)))
    rnd.shuffle(idx)
    folds = [idx[i::K_FOLDS] for i in range(K_FOLDS)]
    hit = miss_e = miss_c = miss_both = 0
    th = {"A": 0, "B": 0}
    tt = {"A": 0, "B": 0}
    core_hit = core_tot = 0
    for k in range(K_FOLDS):
        test = set(folds[k])
        train = [gold[i]["title"] for i in idx if i not in test]
        me, mc = mine(train, nc, nn)
        eff = bb_e + [compile_term(w) for w in me[:Nf]]
        cau = bb_c + [compile_term(w) for w in mc[:Np]]
        for i in folds[k]:
            nt = " " + norm(gold[i]["title"]) + " "
            tr = gold[i]["tier"]
            tt[tr] += 1
            eok, cok = matches_block(nt, eff), matches_block(nt, cau)
            is_core = gold[i]["cell"] in RARE_CORE
            core_tot += is_core
            if eok and cok:
                hit += 1
                th[tr] += 1
                core_hit += is_core
            elif not eok and not cok:
                miss_both += 1
            elif not eok:
                miss_e += 1
            else:
                miss_c += 1
    tot = sum(tt.values())
    rA = th["A"] / tt["A"] if tt["A"] else 0
    rB = th["B"] / tt["B"] if tt["B"] else 0
    return {"Nf": Nf, "Np": Np, "recall": round(hit / tot, 4), "hit": hit, "tot": tot,
            "recall_A": round(rA, 4), "recall_B": round(rB, 4), "bias_correction": round(rA - rB, 4),
            "recall_rare_core": round(core_hit / core_tot, 4) if core_tot else None,
            "core_hit": core_hit, "core_tot": core_tot,
            "miss_effect": miss_e, "miss_cause": miss_c, "miss_both": miss_both}


def budget_proxy(gold, nc, nn, neg, Nf, Np):
    bb_e = [compile_term(t) for t in EFFECT_BACKBONE]
    bb_c = [compile_term(t) for t in CAUSE_BACKBONE]
    me, mc = mine([g["title"] for g in gold], nc, nn)
    eff = bb_e + [compile_term(w) for w in me[:Nf]]
    cau = bb_c + [compile_term(w) for w in mc[:Np]]
    n = 0
    for t in neg:
        nt = " " + norm(t) + " "
        if matches_block(nt, eff) and matches_block(nt, cau):
            n += 1
    return n


def main():
    gold, nc, nn, neg = load()
    nA = sum(1 for g in gold if g["tier"] == "A")
    nB = sum(1 for g in gold if g["tier"] == "B")
    ncore = sum(1 for g in gold if g["cell"] in RARE_CORE)
    print(f"gold {len(gold)} (A {nA}, B {nB}; rare-core {ncore}) | neg titles {len(neg)} | neg tokens {nn}",
          file=sys.stderr)
    rows = [cv(gold, nc, nn, Nf, Np) for Nf in GRID for Np in GRID]
    front = sorted(rows, key=lambda r: -r["recall"])[:8]
    for r in front:
        r["neg_matched_proxy"] = budget_proxy(gold, nc, nn, neg, r["Nf"], r["Np"])
    json.dump(rows, open(LOGS / f"{SLUG}-cv-breadth.json", "w"), indent=2)

    best = max(rows, key=lambda r: r["recall"])
    base = next(r for r in rows if r["Nf"] == 0 and r["Np"] == 0)
    by = {(r["Nf"], r["Np"]): r["recall"] for r in rows}
    L = [f"# A6b CV — breadth-vector — {SLUG}", "",
         "10-fold CV, title-only matching (conservative lower bound). Query = (EFFECT) AND (CAUSE), each "
         "= fixed backbone ∪ top-N fold-local gold-mined terms. CAUSE backbone carries the FORCED "
         "decoupling/contraception cluster (design (b)).", "",
         f"- gold = {len(gold)} (A {nA} keyword-seeds, B {nB} screen-relevant-empirical); rare decoupling/"
         f"desire core = {ncore}", f"- negatives (budget proxy) = {len(neg)}",
         f"- **backbone-only recall (Nf=Np=0): {base['recall']:.1%}** "
         f"[Rec(A) {base['recall_A']:.1%} / Rec(B) {base['recall_B']:.1%} → bias {base['bias_correction']:+.1%}] "
         f"(miss effect {base['miss_effect']}, cause {base['miss_cause']}, both {base['miss_both']}; "
         f"rare-core recall {base['recall_rare_core']})",
         f"- **best grid point: Nf={best['Nf']}, Np={best['Np']} → CV recall {best['recall']:.1%}** "
         f"[Rec(A) {best['recall_A']:.1%} / Rec(B) {best['recall_B']:.1%} → bias {best['bias_correction']:+.1%}; "
         f"rare-core recall {best['recall_rare_core']}]", "",
         "> Recall(B) is the honest primary metric (unbiased orthogonal sample); Recall(A)−Recall(B) is "
         "the vocabulary-bias diagnostic. rare-core recall checks whether the forced (b) backbone rescues "
         "the PRIMARY_DECOUPLING/DESIRE cells.", "",
         "## Recall surface (CV held-out recall by breadth vector)", "",
         "| Nf \\\\ Np | " + " | ".join(str(n) for n in GRID) + " |",
         "|" + "---|" * (len(GRID) + 1)]
    for nf in GRID:
        L.append(f"| **{nf}** | " + " | ".join(f"{by[(nf,np)]:.0%}" for np in GRID) + " |")
    L += ["", "## Recall / budget frontier (top-8 recall; neg_matched = on-disk budget proxy)", "",
          "| Nf | Np | recall | Rec(A) | Rec(B) | A−B | rare-core | miss-eff | miss-cause | miss-both | neg-matched |",
          "|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in front:
        L.append(f"| {r['Nf']} | {r['Np']} | {r['recall']:.1%} | {r['recall_A']:.0%} | {r['recall_B']:.0%} | "
                 f"{r['bias_correction']:+.0%} | {r['recall_rare_core']} | {r['miss_effect']} | "
                 f"{r['miss_cause']} | {r['miss_both']} | {r['neg_matched_proxy']} |")
    L += ["", "## Reading", "",
          "- If held-out misses concentrate on ONE block, move breadth there (the §6 allocation signal).",
          "- rare-core recall isolates whether the forced (b) decoupling backbone is doing its job; if it "
          "stays high while mined breadth grows, (b) succeeded without the mined terms crowding it out.",
          "- Production query (A6c) = refit on FULL gold at the chosen (Nf,Np); quote CV recall as the "
          "honest out-of-sample estimate. Real budget = OpenAlex universe count (A6c live search)."]
    (LOGS / f"{SLUG}-cv-breadth.md").write_text("\n".join(L) + "\n")

    print(f"backbone-only {base['recall']:.1%} (rare-core {base['recall_rare_core']}) | "
          f"best {best['recall']:.1%} @ Nf={best['Nf']},Np={best['Np']} (rare-core {best['recall_rare_core']})",
          file=sys.stderr)
    for r in front:
        print(f"  Nf={r['Nf']:>2} Np={r['Np']:>2} recall {r['recall']:.1%} "
              f"[A {r['recall_A']:.0%}/B {r['recall_B']:.0%}] core {r['recall_rare_core']} "
              f"neg {r['neg_matched_proxy']} (mE {r['miss_effect']} mC {r['miss_cause']} both {r['miss_both']})",
              file=sys.stderr)


if __name__ == "__main__":
    main()
