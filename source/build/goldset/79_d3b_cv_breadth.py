#!/usr/bin/env python3
"""
79_d3b_cv_breadth.py - D.3.b (climate anxiety / eco-doomerism), stage A6b.

Mirror of B.1's `69_b1_cv_breadth.py`. 10-fold CV over the per-block breadth vector. The production
query is a 2-block conjunction: (EFFECT block) AND (CAUSE block). A gold paper is RECALLED iff its
title matches BOTH blocks.

Each block = a FIXED backbone UNION the top-N fold-local gold-mined discriminative terms at breadth N.

  EFFECT backbone: the definitional fertility-and-intention vocabulary. A6a found that "fertility" is
                   actually a NEGATIVE discriminator inside this frame (z = -1.8; it appears far more
                   in the near-miss negatives, which are dominated by physical-climate-exposure to
                   fertility papers), while the on-topic effect language is "reproductive",
                   "procreation", and "intentions". The backbone keeps "fertility" anyway, because it
                   is definitional scope vocabulary and a production query that could not retrieve a
                   paper saying "fertility" would be indefensible. The mined expansion is what
                   supplies the precision.
  CAUSE backbone : the FORCED climate-affect cluster, this chapter's analogue of B.1's design (b).
                   The carbon-ethics and desire-independence vocabulary is conceptually central and
                   empirically rare (PRIMARY_CARBON_ETHICS = 7 papers, DESIRE_INDEPENDENCE = 4), so it
                   is forced in rather than left to the mined ranking, which would never surface it.

Leakage discipline, two separate walls:
  1. CV leakage: backbones are FIXED a-priori scope vocabulary; the gold-mined expansion is recomputed
     from the TRAINING folds only, so held-out recall never sees its own labels.
  2. SOURCE leakage (D.3.b-specific, binding from A3): no term here comes from the PLOS Climate
     review's published search string. Every mined term comes from our own screen verdicts.

Matching is TITLE-only (both sides on one footing; a conservative lower bound, since abstract matching
would only add recall). The production query is refit on the FULL gold at the chosen (Nf,Np) in A6c.

Gold: Tier A = the 10 empirical seeds (keyword-sourced, optimistic); Tier B = the screen's
RELEVANT set restricted to the four EMPIRICAL primary cells (the orthogonal, unbiased sample).
Carried over from B.1's design point: the THEORY stream (ECO_ETHICS_THEORY, ANXIETY_CONSTRUCT) is a
separate stream and does NOT count toward empirical recall. For D.3.b that exclusion is large, since
theory outnumbers the empirical core more than two to one, and counting it would flatter recall.

Two diagnostics beyond B.1's:
  - recall on RARE_CORE (DESIRE_INDEPENDENCE + PRIMARY_CARBON_ETHICS), the value-added cells;
  - recall on REALIZED_FERTILITY outcomes, which number 8 in the entire frame after dedup. If the production
    query cannot retrieve those, the one stratum that could ever support a realized-fertility pool is
    structurally invisible to it, and that is worth knowing at A6 rather than at A7.

Inputs : output/{slug}-screen-tiers.json, literature/search-logs/{slug}-tier-a.json
Output : literature/search-logs/{slug}-cv-breadth.json + .md
"""
import json, re, math, random, sys
import unicodedata
from pathlib import Path
from collections import Counter

SLUG = "climate-anxiety-eco-doomerism"
HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
LOGS = REPO / "literature" / "search-logs"
OUT = REPO / "output"
K_FOLDS = 10
SEED = 733
ALPHA0 = 1000.0
MIN_GOLD_FOLD = 2
# Grid extended past B.1's [0..30]: a first run peaked at the Np=30 edge with the cause block still
# binding, so the plateau had not been reached and 30 would have been an artefact of the grid.
GRID = [0, 3, 6, 10, 15, 20, 30, 45, 60, 80]

PRIMARY_EMPIRICAL = {"PRIMARY_HABITABILITY_FEAR", "PRIMARY_CARBON_ETHICS", "PRIMARY_ECO_PESSIMISM",
                     "DESIRE_INDEPENDENCE"}
RARE_CORE = {"DESIRE_INDEPENDENCE", "PRIMARY_CARBON_ETHICS"}
NON_EMPIRICAL_EVIDENCE = {"theory", "review"}

EFFECT_BACKBONE = ["fertility", "fertilit*", "birth*", "childbearing", "childbear*", "childless*",
                   "childfree", "child-free", "number of children", "offspring", "family size",
                   "reproductive", "reproduction", "reproducti*", "procreat*", "natality", "parity",
                   "have children", "having children", "fertility intention*",
                   "reproductive intention*", "childbearing intention*", "pregnancy intention*",
                   "remain childless", "voluntary childless*"]
# Forced climate-affect + ethics cause backbone: conceptually central, empirically rare.
CAUSE_BACKBONE = ["climate anxiety", "eco-anxiety", "eco anxiety", "climate distress", "climate worry",
                  "climate worries", "climate concern*", "climate grief", "climate emotion*",
                  "solastalgia", "eco-distress", "ecological grief",
                  "eco-doom*", "doomism", "eco-pessimis*", "climate pessimis*", "climate despair",
                  "climate dread", "climate doom", "apocalyp*", "collapse",
                  "carbon footprint", "carbon legacy", "antinatalis*", "anti-natalis*",
                  "environmental antinatalis*", "procreative ethic*", "population ethic*",
                  "overpopulation",
                  "habitabilit*", "bring a child into", "world to bring", "future for children",
                  "climate future", "planetary",
                  "climate change", "global warming", "climate crisis", "ecological crisis",
                  "environmental crisis"]

STOP = set("the a an of and in on for from to its by is with as at or be this that these those we our "
           "their his her it they i ii iii new evidence using based study studies analysis approach paper "
           "article effect effects impact role case among between within over under are was were has have "
           "had do does can could will would not no more less than into about across after before during "
           "toward towards via per vs versus also two three some how what why when where which who whom "
           "data model models results result human humans".split())

EFFECT = re.compile(r"fertil|childbear|childless|childfree|child-free|birth rate|birthrate|natalit|"
                    r"offspring|reproducti|number of children|family size|parity|procreat|babi|"
                    r"have children|having children|child rearing|childrearing|"
                    r"intention|intent to|desire for a child|remain childless|voluntary childless")
CAUSE = re.compile(
    r"\bclimate\b|\beco\b|anxiet|anxious|worri|\bworry\b|concern|emotion|feeling|"
    r"\bfear|afraid|distress|grief|guilt|hope\b|hopeless|"
    r"climate anxiet|eco-anxiet|eco anxiet|climate worr|climate concern|climate distress|"
    r"climate emotion|climate grief|solastalgia|environmental concern|environmental worr|"
    r"habitab|planetary|future for children|bring a child|uncertain future|climate future|"
    r"world to bring|liveab|livab|"
    r"carbon|footprint|emission|antinatal|anti-natal|overpopulat|population ethic|"
    r"procreat\w* ethic|environmental ethic|moral|ethic|"
    r"doom|apocalyp|collapse|catastroph|existential|pessimis|dread|despair|extinction|"
    r"end of the world|crisis|"
    r"reproductive decision|childbearing decision|decision-making|decision making|motivation|"
    r"attitude|willingness|"
    r"climate change|global warming|environment|ecolog|sustainab|green ")


# --- canonical fold, TICK-074. Keep in sync with source/lib/textnorm.py; the sync is ENFORCED by
# scripts/verify_norm.py, which imports every copy and compares it against the canonical one on a
# shared test vector. Two defects live here, both silent and both producing confident wrong answers:
# an unfolded accent SHATTERS a surname (Spéder -> "der"), and an ASCII apostrophe becomes a SPACE
# while a curly one is DELETED, so the same title normalises two different ways and a correct anchor
# is refused as NO-MATCH. Fold every class BEFORE the ASCII strip, and fold both spellings alike.
_TRANSLIT = {ord("ø"): "o", ord("Ø"): "O", ord("đ"): "d", ord("Đ"): "D", ord("ð"): "d",
             ord("Ð"): "D", ord("þ"): "th", ord("Þ"): "Th", ord("ı"): "i", ord("İ"): "I",
             ord("ł"): "l", ord("Ł"): "L", ord("æ"): "ae", ord("Æ"): "Ae", ord("œ"): "oe",
             ord("Œ"): "Oe", ord("ß"): "ss", ord("ħ"): "h", ord("Ħ"): "H", ord("ŋ"): "n",
             ord("Ŋ"): "N"}
_APOSTROPHE_CLASS = re.compile("['‘’ʼ´`]")
_DASH_CLASS = re.compile("[-‐‑‒–—―−­]")


def norm(s):
    s = (s or "").translate(_TRANSLIT)
    s = _APOSTROPHE_CLASS.sub("", s)
    s = _DASH_CLASS.sub(" ", s)
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode("ascii")
    s = re.sub(r"[^a-z0-9 ]", " ", s.lower())
    return re.sub(r"\s+", " ", s).strip()


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
    gold = [{"title": s["title"], "tier": "A", "cell": s.get("provisional_cell"), "outcome_level": None}
            for s in seeds if s.get("title")]
    for r in rows:
        if (r["verdict"] == "RELEVANT"
                and r.get("cell") in PRIMARY_EMPIRICAL
                and r.get("evidence_type") not in NON_EMPIRICAL_EVIDENCE
                and r.get("title")):
            gold.append({"title": r["title"], "tier": "B", "cell": r["cell"],
                         "outcome_level": r.get("outcome_level")})
    neg = [r["title"] for r in rows if r["verdict"] == "NOT_RELEVANT" and r.get("title")]
    nc = Counter()
    for t in neg:
        nc.update(cand_terms(t))
    return dedup_gold(gold), nc, sum(nc.values()), neg


# Gold is deduplicated on normalized title. The frame carries preprint/version-of-record pairs under
# distinct OpenAlex ids (e.g. the SocArXiv and Population and Development Review versions of the same
# worries-and-childbearing paper). Counting both would weight one study twice in the recall denominator.
def dedup_gold(gold):
    seen, out = set(), []
    for g in gold:
        k = norm(g["title"])[:70]
        if k in seen:
            continue
        seen.add(k)
        out.append(g)
    return out


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
    real_hit = real_tot = 0
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
            is_real = gold[i].get("outcome_level") in ("REALIZED_FERTILITY", "BOTH")
            core_tot += is_core
            real_tot += is_real
            if eok and cok:
                hit += 1
                th[tr] += 1
                core_hit += is_core
                real_hit += is_real
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
            "recall_realized": round(real_hit / real_tot, 4) if real_tot else None,
            "real_hit": real_hit, "real_tot": real_tot,
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
    nreal = sum(1 for g in gold if g.get("outcome_level") in ("REALIZED_FERTILITY", "BOTH"))
    print(f"gold {len(gold)} (A {nA}, B {nB}; rare-core {ncore}; realized-fertility {nreal}) | "
          f"neg titles {len(neg)} | neg tokens {nn}", file=sys.stderr)
    rows = [cv(gold, nc, nn, Nf, Np) for Nf in GRID for Np in GRID]
    front = sorted(rows, key=lambda r: -r["recall"])[:8]
    for r in front:
        r["neg_matched_proxy"] = budget_proxy(gold, nc, nn, neg, r["Nf"], r["Np"])
    json.dump(rows, open(LOGS / f"{SLUG}-cv-breadth.json", "w"), indent=2)

    best = max(rows, key=lambda r: r["recall"])
    base = next(r for r in rows if r["Nf"] == 0 and r["Np"] == 0)
    by = {(r["Nf"], r["Np"]): r["recall"] for r in rows}
    L = [f"# A6b CV - breadth-vector - {SLUG}", "",
         "10-fold CV, title-only matching (conservative lower bound). Query = (EFFECT) AND (CAUSE), each "
         "= fixed backbone union top-N fold-local gold-mined terms. CAUSE backbone carries the FORCED "
         "climate-affect and carbon-ethics cluster, this chapter's analogue of B.1's design (b).", "",
         "**Theory is excluded from gold.** ECO_ETHICS_THEORY and ANXIETY_CONSTRUCT form a separate "
         "stream and do not count toward empirical recall. That exclusion is large here, since theory "
         "outnumbers the empirical core more than two to one; counting it would flatter recall.", "",
         f"- gold = {len(gold)} (A {nA} keyword-seeds, B {nB} screen-relevant-empirical); "
         f"rare value-added core = {ncore}; realized-fertility outcomes = {nreal}",
         f"- negatives (budget proxy) = {len(neg)}",
         f"- **backbone-only recall (Nf=Np=0): {base['recall']:.1%}** "
         f"[Rec(A) {base['recall_A']:.1%} / Rec(B) {base['recall_B']:.1%} -> bias {base['bias_correction']:+.1%}] "
         f"(miss effect {base['miss_effect']}, cause {base['miss_cause']}, both {base['miss_both']}; "
         f"rare-core {base['recall_rare_core']}, realized-fertility {base['recall_realized']})",
         f"- **best grid point: Nf={best['Nf']}, Np={best['Np']} -> CV recall {best['recall']:.1%}** "
         f"[Rec(A) {best['recall_A']:.1%} / Rec(B) {best['recall_B']:.1%} -> bias {best['bias_correction']:+.1%}; "
         f"rare-core {best['recall_rare_core']}, realized-fertility {best['recall_realized']}]", "",
         "> Recall(B) is the honest primary metric (unbiased orthogonal sample); Recall(A) minus "
         "Recall(B) is the vocabulary-bias diagnostic. rare-core recall checks whether the forced cause "
         "backbone rescues DESIRE_INDEPENDENCE and PRIMARY_CARBON_ETHICS. realized-fertility recall "
         "checks whether the query can see the only stratum that could ever support a realized-fertility "
         "pool.", "",
         "## Recall surface (CV held-out recall by breadth vector)", "",
         "| Nf \\\\ Np | " + " | ".join(str(n) for n in GRID) + " |",
         "|" + "---|" * (len(GRID) + 1)]
    for nf in GRID:
        L.append(f"| **{nf}** | " + " | ".join(f"{by[(nf,np)]:.0%}" for np in GRID) + " |")
    L += ["", "## Recall / budget frontier (top-8 recall; neg_matched = on-disk budget proxy)", "",
          "| Nf | Np | recall | Rec(A) | Rec(B) | A-B | rare-core | realized | miss-eff | miss-cause | "
          "miss-both | neg-matched |",
          "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in front:
        L.append(f"| {r['Nf']} | {r['Np']} | {r['recall']:.1%} | {r['recall_A']:.0%} | {r['recall_B']:.0%} | "
                 f"{r['bias_correction']:+.0%} | {r['recall_rare_core']} | {r['recall_realized']} | "
                 f"{r['miss_effect']} | {r['miss_cause']} | {r['miss_both']} | {r['neg_matched_proxy']} |")
    L += ["", "## Reading", "",
          "- If held-out misses concentrate on ONE block, move breadth there (the section 6 allocation "
          "signal).",
          "- rare-core recall isolates whether the forced cause backbone is doing its job. If it stays "
          "high while mined breadth grows, the forced cluster succeeded without the mined terms crowding "
          "it out.",
          "- realized-fertility recall is the D.3.b-specific check. The whole frame holds 9 such records, "
          "so this number is noisy by construction; read it as a structural signal, not an estimate.",
          "- Production query (A6c) = refit on FULL gold at the chosen (Nf,Np); quote CV recall as the "
          "honest out-of-sample estimate. Real budget = OpenAlex universe count (A6c live search)."]
    (LOGS / f"{SLUG}-cv-breadth.md").write_text("\n".join(L) + "\n")

    print(f"backbone-only {base['recall']:.1%} (rare-core {base['recall_rare_core']}, "
          f"realized {base['recall_realized']}) | best {best['recall']:.1%} @ "
          f"Nf={best['Nf']},Np={best['Np']} (rare-core {best['recall_rare_core']}, "
          f"realized {best['recall_realized']})", file=sys.stderr)
    for r in front:
        print(f"  Nf={r['Nf']:>2} Np={r['Np']:>2} recall {r['recall']:.1%} "
              f"[A {r['recall_A']:.0%}/B {r['recall_B']:.0%}] core {r['recall_rare_core']} "
              f"real {r['recall_realized']} neg {r['neg_matched_proxy']} "
              f"(mE {r['miss_effect']} mC {r['miss_cause']} both {r['miss_both']})", file=sys.stderr)


if __name__ == "__main__":
    main()
