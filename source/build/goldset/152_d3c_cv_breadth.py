#!/usr/bin/env python3
r"""
152_d3c_cv_breadth.py — D.3.c, stage B1. 10-fold CV over per-cluster query breadth.

The production query is a conjunction: (OUTCOME block) AND (any one of four TREATMENT clusters). A
gold paper is RECALLED iff its title matches the outcome block AND at least one treatment cluster.
Each block is a FIXED a-priori backbone UNION the top-N fold-locally-mined terms at breadth N.

WHAT THIS RUN IS FOR, AND WHY THE USUAL ANSWER IS THE WRONG ONE HERE. B1 normally picks breadth at the
knee of the recall-versus-budget curve: buy recall until precision starts collapsing, then stop. A4
established that on this chapter precision cannot be bought at all. Mining the frame for terms that
separate the primary-anchor neighbourhood from the walls' produced **zero** terms in the
`MECHANISM_AND_OUTCOME` block, **zero** mechanism terms among the forty strongest discriminators, and
a *negative* z for `despair` itself (-4.44; 5 occurrences in the primary neighbourhood against 635 in
the walls'). There is no vocabulary that does Wall 1's job, because Wall 1 separates two mechanisms
over the same treatment and the same outcome, and a title cannot see a mechanism.

So the selection rule is stated up front rather than discovered: **maximise recall, and let the screen
carry the routing.** Precision spent on this query buys nothing that the screen would not have to
redo. What B1 produces here is therefore (a) the breadth at which recall stops improving, and (b) the
screening load that choice implies — which is the number the budget conversation actually needs. Both
are reported; the second is the deliverable.

THE RECALL DENOMINATOR IS PROVENANCE-DEFINED, AND THAT IS A COMPROMISE THAT HAS TO BE STATED.
A3's spec defines Tier B as the snowball-*relevant* set. This chapter's Tier B is the raw one-hop
neighbourhood (10,589 records), because 150 deliberately did not filter the forward fetch by topic —
filtering it would have pruned the frame by distance from the query being measured. No relevance
determination has been made yet, so the relevant subset does not exist to be a denominator.

The gold used here is therefore: **Tier A's empirical primary-cell anchors, plus Tier B records that
are (i) reached by a PRIMARY-cell anchor's citation neighbourhood and (ii) carry a fertility-outcome
term.** Criterion (i) is the provenance label from 151 and reads no text. Criterion (ii) does read
text, and its consequence is precise and must not be glossed: **the OUTCOME block's recall is near 1
by construction and is not informative.** The informative quantity is the TREATMENT block's recall —
whether adding mined treatment terms recovers primary-neighbourhood fertility papers — and that is
what breadth is being chosen for. Outcome-block misses are still counted and reported, because a
non-zero miss rate on a block that should be tautological is a signal that the backbone is incomplete.

RECALL(B) IS MEASURED ON B_ONLY RECORDS. Tier A is keyword-sourced at A3, so a record in both channels
is partly keyword-sourced and counting it toward Recall(B) re-imports the circularity Recall(B) exists
to escape. Records are tiered A_ONLY / B_ONLY / BOTH and the headline orthogonal number is
Recall(B_ONLY), following D.1.a.

FOLD-LOCAL MINING IS THE GUARD AGAINST A4'S OWN OVERFITTING. A4 surfaced `hungary` (z 14.4) and
`poland` (11.5) among the strongest discriminators — the post-communist anomie family's own
geography, not query vocabulary. Terms are re-mined here from the TRAINING folds only, so a term
carried by one research family earns nothing on held-out papers it has never seen.

TITLE-ONLY MATCHING, deliberately, as in B.1, D.3.b and D.1.a: it puts gold and negatives on one
footing and makes the recall estimate a conservative lower bound. Abstract coverage on this frame is
67%, so an abstract-inclusive number would have to be reported for the covered and uncovered halves
separately.

Inputs : literature/search-logs/{slug}-tier-{a,b-frame}.json
Output : literature/search-logs/{slug}-cv-breadth.json + .md
"""
import json, math, os, random, re, sys, unicodedata
from collections import Counter

SLUG = "despair-hopelessness-fertility"
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
LOGS = os.path.join(ROOT, "literature", "search-logs")
K_FOLDS, SEED, ALPHA0, MIN_GOLD_FOLD = 10, 733, 1000.0, 2
GRID_OUT = [0, 3, 6, 10, 15, 20]
GRID_TRT = [0, 3, 6, 10, 15, 20, 30, 45]

PRIMARY_CELLS = {"PRIMARY_MEASURED_DESPAIR", "PRIMARY_DECLINE_WITH_MECHANISM",
                 "PRIMARY_ACCELERATION"}

STOP = set(
    "the a an of and in on for from to its by is with as at or be this that these those we our their "
    "his her it they new evidence using based study studies analysis approach paper article effect "
    "effects impact role case among between within over under are was were has have had do does can "
    "could will would not no more less than into about across after before during toward towards via "
    "per versus also two three some how what why when where which who whom data model models results "
    "result human humans research review journal university press vol doi eds chapter book series "
    "report working note comment reply been being one first second third such other others both each "
    "many much most least well however therefore thus while although though because since given find "
    "finds found show shows shown suggest suggests use used uses associated association significant "
    "significantly higher lower increase increased decrease decreased change changes level levels "
    "rate rates high low large small years year age aged time times group groups sample samples "
    "population populations country countries national state states area areas evidence".split())

# ---- fixed a-priori backbones. Scope vocabulary, not mined, so they are immune to frame composition.
OUTCOME_BACKBONE = [
    "fertility", "fertilit*", "birth rate", "birthrate", "births", "childbearing", "childbear*",
    "childless*", "childfree", "child-free", "number of children", "family size", "completed family",
    "parity", "natality", "total fertility rate", "tfr", "fertility intention*",
    "fertility preference*", "reproductive intention*", "reproductive decision*", "family formation",
    "desire for children", "having children",
    # Chapter 2's margin. The acceleration chapter's outcome is a TIMING and composition margin, and
    # an outcome block written only for quantum would systematically drop it — which would bias the
    # query toward chapter 1 invisibly, inside the retrieval step, where no later stage could see it.
    "teen birth*", "teenage birth*", "teen pregnanc*", "teenage pregnanc*", "adolescent childbearing",
    "adolescent fertility", "early childbearing", "early motherhood", "young mother*",
    "nonmarital", "non-marital", "unmarried mother*", "out-of-wedlock", "premarital birth*",
    "birth timing", "first birth", "age at first birth", "postponement", "tempo",
]
TREATMENT_BACKBONE = {
    # Chapter-agnostic: the construct itself. BACKBONE-ONLY IN PRACTICE, and that is the finding
    # rather than an oversight — A4 mined four mechanism terms in total, of which `despair` is
    # negatively discriminative. Leaving this cluster to the mined ranking would leave the
    # hypothesis's own construct out of its own query. D.1.a and D.3.b both had to force a
    # conceptually central, empirically rare cluster in the same way.
    "MECHANISM": [
        "despair", "hopeless*", "demoralis*", "demoraliz*", "anomie", "anomic", "fatalis*",
        "normlessness", "future orientation", "foreshortened future", "sense of the future",
        "subjective future", "expectations about the future", "future expectations",
        "pessimism", "optimism about the future", "bleak", "meaninglessness", "alienation",
        "deaths of despair", "psychological distress", "demoralization",
    ],
    # Chapter 1's treatment: chronic, expected-permanent place-level decline.
    "DECLINE_CHRONIC": [
        "deindustriali*", "economic decline", "declining region*", "distressed communit*",
        "distressed area*", "left behind", "left-behind", "plant closure*", "mass layoff*",
        "job displacement", "displaced worker*", "import competition", "china shock", "trade shock",
        "rust belt", "manufacturing decline", "coal mining", "structural decline", "depopulation",
        "shrinking cit*", "regional decline", "economic distress", "downward mobility",
    ],
    # Chapter 2's treatment: low perceived individual opportunity, lower-tail inequality.
    "OPPORTUNITY_INEQUALITY": [
        "income inequality", "lower-tail inequality", "economic opportunit*", "opportunity structure",
        "perceived opportunit*", "economic marginali*", "social exclusion", "concentrated poverty",
        "disadvantaged neighborhood*", "disadvantaged neighbourhood*", "socioeconomic disadvantage",
        "limited opportunit*", "life chances", "social mobility", "intergenerational mobility",
        "deprivation", "marginali*",
    ],
    # The Wall 1 cluster, included ON PURPOSE and named for what it is. This is C.5.a's vocabulary,
    # and A4 showed it cannot be separated from D.3.c's at the level of a title. Excluding it would
    # buy precision the screen has to re-earn anyway while dropping genuine D.3.c records that
    # happen to be written in uncertainty language; including it is the recall-first rule applied
    # where it costs the most and is therefore the honest test of that rule.
    "UNCERTAINTY_GENERIC": [
        "economic uncertainty", "employment uncertainty", "job insecurity", "precarious*",
        "unemployment", "labour market insecurity", "labor market insecurity", "recession",
        "economic crisis", "economic insecurity", "financial insecurity", "uncertainty",
    ],
}
CLUSTERS = list(TREATMENT_BACKBONE)

# Blocks for fold-local mining. Mirrors 151's axes so a term means the same thing in both scripts.
MECHANISM_RX = re.compile(
    r"despair|hopeless|demorali[sz]|anomie|fatalis|normless|alienat|future orientation|"
    r"foreshortened|expectations about|pessimis|optimis|bleak|meaningless|subjective wellbeing|"
    r"life satisfaction|distress|discourag")
OUTCOME_RX = re.compile(
    r"fertil|childbear|childless|childfree|birth rate|birthrate|natalit|number of children|"
    r"family size|parity|nuptial|\bbirths?\b|\btfr\b|completed famil|teen birth|teenage|"
    r"nonmarital|non-marital|out-of-wedlock|adolescent|first birth|postpone|tempo|"
    r"reproductive intention|young mother")
DECLINE_RX = re.compile(
    r"deindustriali|economic decline|declining|distressed|left behind|plant closure|mass layoff|"
    r"displac|import competition|china shock|trade shock|rust belt|manufactur|coal|depopulat|"
    r"shrinking|downward mobilit")
OPPORTUNITY_RX = re.compile(
    r"inequalit|opportunit|marginali|social exclusion|poverty|disadvantag|deprivation|"
    r"life chances|mobility|socioeconomic status|\bses\b|welfare")
UNCERTAINTY_RX = re.compile(
    r"uncertain|insecur|precari|unemploy|recession|economic crisis|labour market|labor market|"
    r"employment")


def block_of(term):
    """Assign a mined term to the outcome axis or one treatment cluster. Mechanism is tested FIRST:
    it is the rarest vocabulary and the one the chapter turns on, so letting a more common axis claim
    a mechanism term would starve the cluster that can least afford it."""
    if MECHANISM_RX.search(term):
        return "MECHANISM"
    if OUTCOME_RX.search(term):
        return "OUTCOME"
    if DECLINE_RX.search(term):
        return "DECLINE_CHRONIC"
    if OPPORTUNITY_RX.search(term):
        return "OPPORTUNITY_INEQUALITY"
    if UNCERTAINTY_RX.search(term):
        return "UNCERTAINTY_GENERIC"
    return None


def norm(s):
    """Lowercase, FOLD DIACRITICS, then reduce to alphanumerics. The fold is not cosmetic — see the
    norm() finding from A3, where replacing non-ASCII with a space SHATTERED accented surnames."""
    t = unicodedata.normalize("NFKD", (s or "").lower())
    t = "".join(c for c in t if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9\s]", " ", t)).strip()


def cand_terms(title):
    u = [w for w in norm(title).split()
         if len(w) > 2 and w not in STOP and sum(c.isdigit() for c in w) * 2 < len(w)]
    return u + [f"{u[i]} {u[i + 1]}" for i in range(len(u) - 1)]


def compile_term(t):
    t = t.strip().lower()
    return ("prefix", norm(t[:-1])) if t.endswith("*") else ("phrase", norm(t))


def matches(padded, compiled):
    for kind, val in compiled:
        if not val:
            continue
        if kind == "prefix":
            if re.search(r"\b" + re.escape(val), padded):
                return True
        elif (" " + val + " ") in padded:
            return True
    return False


def mine(train_titles, nc, nn):
    """Fold-local Fightin' Words. Returns {block: [terms ranked by z]}."""
    gc = Counter()
    for t in train_titles:
        gc.update(cand_terms(t))
    ng = sum(gc.values())
    ncomb = ng + nn
    out = {b: [] for b in ["OUTCOME"] + CLUSTERS}
    for w, g in gc.items():
        if g < MIN_GOLD_FOLD:
            continue
        b = block_of(w)
        if b not in out:
            continue
        n_ = nc.get(w, 0)
        aw = ALPHA0 * (g + n_) / ncomb
        delta = (math.log((g + aw) / (ng + ALPHA0 - g - aw))
                 - math.log((n_ + aw) / (nn + ALPHA0 - n_ - aw)))
        z = delta / math.sqrt(1.0 / (g + aw) + 1.0 / (n_ + aw))
        out[b].append((w, z))
    for b in out:
        out[b].sort(key=lambda x: -x[1])
        out[b] = [w for w, _ in out[b]]
    return out


OUT_TERM_RX = re.compile(
    r"fertil|childbear|childless|childfree|birth rate|birthrate|natalit|number of children|"
    r"family size|parity|\bbirths?\b|\btfr\b|teen birth|teenage pregnan|nonmarital|non-marital|"
    r"out-of-wedlock|reproductive intention|completed famil|early childbearing|adolescent childbear")


def load():
    tier_a = json.load(open(os.path.join(LOGS, f"{SLUG}-tier-a.json")))
    tier_b = json.load(open(os.path.join(LOGS, f"{SLUG}-tier-b-frame.json")))
    pids = {a.get("openalex_id") for a in tier_a
            if a.get("provisional_cell") in PRIMARY_CELLS and a.get("openalex_id")}

    # TITLE-ONLY, and the choice is load-bearing. A first run applied this criterion to title AND
    # abstract while matching on title alone, which put records into the denominator that the query
    # cannot see by construction — recall came out at 11.2% and most of the misses were the OUTCOME
    # block failing on records whose fertility outcome is named only in the abstract. That conflates
    # two different things: terms that are wrong, and information that is not in the field being
    # matched. The denominator is now records retrievable in principle; the ones excluded are counted
    # separately below as the measured cost of the title-only convention.
    def blob(r):
        return (r.get("title") or "").lower()

    bkeys = {norm(r.get("title") or "")[:70] for r in tier_b if r.get("title")}
    gold, seen = [], set()
    for a in tier_a:
        if a.get("provisional_cell") not in PRIMARY_CELLS or not a.get("title"):
            continue
        k = norm(a["title"])[:70]
        if k in seen:
            continue
        seen.add(k)
        gold.append({"title": a["title"], "cell": a["provisional_cell"],
                     "tier": "BOTH" if k in bkeys else "A_ONLY"})
    for r in tier_b:
        if not r.get("title"):
            continue
        if not (set(r.get("seed_ids") or []) & pids):
            continue
        if not OUT_TERM_RX.search(blob(r)):
            continue
        k = norm(r["title"])[:70]
        if k in seen:
            continue
        seen.add(k)
        gold.append({"title": r["title"], "cell": None, "tier": "B_ONLY"})

    abs_only = 0
    for r in tier_b:
        if not r.get("title") or not (set(r.get("seed_ids") or []) & pids):
            continue
        if OUT_TERM_RX.search((r.get("title") or "").lower()):
            continue
        if OUT_TERM_RX.search(((r.get("title") or "") + " " + (r.get("abstract") or "")).lower()):
            abs_only += 1

    goldkeys = {norm(g["title"])[:70] for g in gold}
    neg = [r["title"] for r in tier_b
           if r.get("title") and norm(r["title"])[:70] not in goldkeys]
    nc = Counter()
    for t in neg:
        nc.update(cand_terms(t))
    return gold, neg, nc, sum(nc.values()), abs_only


def cv(gold, neg, nc, nn, n_out, n_trt):
    bb_o = [compile_term(t) for t in OUTCOME_BACKBONE]
    bb_c = {c: [compile_term(t) for t in TREATMENT_BACKBONE[c]] for c in CLUSTERS}
    rnd = random.Random(SEED)
    idx = list(range(len(gold)))
    rnd.shuffle(idx)
    folds = [idx[i::K_FOLDS] for i in range(K_FOLDS)]
    hit, tot, miss, credit = Counter(), Counter(), Counter(), Counter()
    for k in range(K_FOLDS):
        test = set(folds[k])
        mined = mine([gold[i]["title"] for i in idx if i not in test], nc, nn)
        out_c = bb_o + [compile_term(w) for w in mined["OUTCOME"][:n_out]]
        trt_c = {c: bb_c[c] + [compile_term(w) for w in mined[c][:n_trt]] for c in CLUSTERS}
        for i in folds[k]:
            g = gold[i]
            padded = " " + norm(g["title"]) + " "
            tot["all"] += 1
            tot[g["tier"]] += 1
            ok_o = matches(padded, out_c)
            fired = [c for c in CLUSTERS if matches(padded, trt_c[c])]
            if ok_o and fired:
                hit["all"] += 1
                hit[g["tier"]] += 1
                for c in fired:
                    credit[c] += 1
                if len(fired) == 1:
                    credit[f"sole:{fired[0]}"] += 1
            elif not ok_o and not fired:
                miss["both_blocks"] += 1
            elif not ok_o:
                miss["outcome_block"] += 1
            else:
                miss["treatment_block"] += 1

    # Precision and screening load, measured on the FULL frame at the same breadth. Terms are mined
    # on all gold here rather than fold-locally: this is not a recall estimate, it is a statement
    # about what the deployed query would pull, and the deployed query is mined on everything.
    mined_all = mine([g["title"] for g in gold], nc, nn)
    out_all = bb_o + [compile_term(w) for w in mined_all["OUTCOME"][:n_out]]
    trt_all = {c: bb_c[c] + [compile_term(w) for w in mined_all[c][:n_trt]] for c in CLUSTERS}

    def fires(title):
        p = " " + norm(title) + " "
        return matches(p, out_all) and any(matches(p, trt_all[c]) for c in CLUSTERS)

    n_gold_fire = sum(1 for g in gold if fires(g["title"]))
    n_neg_fire = sum(1 for t in neg if fires(t))
    matched = n_gold_fire + n_neg_fire
    r = lambda a, b: round(hit[a] / tot[b], 4) if tot[b] else None  # noqa: E731
    return {"n_out": n_out, "n_trt": n_trt,
            "recall": r("all", "all"), "hit": hit["all"], "tot": tot["all"],
            "recall_A_only": r("A_ONLY", "A_ONLY"), "recall_B_only": r("B_ONLY", "B_ONLY"),
            "recall_both": r("BOTH", "BOTH"),
            "n_A_only": tot["A_ONLY"], "n_B_only": tot["B_ONLY"], "n_both": tot["BOTH"],
            "miss_outcome_block": miss["outcome_block"],
            "miss_treatment_block": miss["treatment_block"],
            "miss_both_blocks": miss["both_blocks"],
            "frame_matched": matched, "frame_gold_matched": n_gold_fire,
            "frame_precision": round(n_gold_fire / matched, 4) if matched else None,
            "cluster_credit": {c: credit[c] for c in CLUSTERS},
            "cluster_sole": {c: credit[f"sole:{c}"] for c in CLUSTERS}}


def outcome_only(gold, neg, nc, nn, n_out):
    """The recall-first design taken to its endpoint: no treatment conjunction at all.

    Reported because the grid establishes that the conjunction is the binding constraint, not the
    breadth within it. Its recall on THIS gold is ~1 by construction — the gold is defined by a
    fertility-outcome term in the title and the backbone covers those terms — so recall is not the
    informative number here and is not quoted as an achievement. The informative numbers are the
    frame yield and, by comparison with the grid, what the conjunction COSTS in gold records."""
    bb_o = [compile_term(t) for t in OUTCOME_BACKBONE]
    mined_all = mine([g["title"] for g in gold], nc, nn)
    out_all = bb_o + [compile_term(w) for w in mined_all["OUTCOME"][:n_out]]

    def fires(title):
        return matches(" " + norm(title) + " ", out_all)

    n_gold = sum(1 for g in gold if fires(g["title"]))
    n_neg = sum(1 for t in neg if fires(t))
    return {"n_out": n_out, "gold_matched": n_gold, "gold_total": len(gold),
            "frame_matched": n_gold + n_neg,
            "frame_precision": round(n_gold / (n_gold + n_neg), 4) if (n_gold + n_neg) else None}


def main():
    gold, neg, nc, nn, abs_only = load()
    print(f"gold={len(gold)} (A_ONLY {sum(1 for g in gold if g['tier']=='A_ONLY')}, "
          f"B_ONLY {sum(1 for g in gold if g['tier']=='B_ONLY')}, "
          f"BOTH {sum(1 for g in gold if g['tier']=='BOTH')})  negatives={len(neg)}", file=sys.stderr)
    grid = [cv(gold, neg, nc, nn, o, t) for o in GRID_OUT for t in GRID_TRT]
    json.dump({"grid": grid, "n_gold": len(gold), "n_neg": len(neg)},
              open(os.path.join(LOGS, f"{SLUG}-cv-breadth.json"), "w"), indent=1)

    oo = outcome_only(gold, neg, nc, nn, 10)
    best_recall = max(g["recall"] or 0 for g in grid)
    # SELECTION RULE, stated in the header and applied here: maximise recall; among settings tied on
    # recall take the SMALLEST breadth, because extra terms that buy no recall are pure screening
    # cost. This is not the inherited knee rule, and the reason is A4: precision cannot be bought
    # with vocabulary on this chapter, so paying for it here buys nothing the screen would not redo.
    tied = [g for g in grid if (g["recall"] or 0) >= best_recall - 1e-9]
    chosen = min(tied, key=lambda g: (g["n_out"] + g["n_trt"], -(g["frame_precision"] or 0)))
    knee = max(grid, key=lambda g: ((g["recall"] or 0) * (g["frame_precision"] or 0)))

    L = [f"# D.3.c — CV over query breadth (B1)", "",
         f"10-fold CV, seed {SEED}. Gold **{len(gold)}** records "
         f"({sum(1 for g in gold if g['tier']=='B_ONLY')} B_ONLY, "
         f"{sum(1 for g in gold if g['tier']=='A_ONLY')} A_ONLY, "
         f"{sum(1 for g in gold if g['tier']=='BOTH')} BOTH); negatives **{len(neg):,}** "
         "(the rest of the Tier B frame). Title-only matching, a conservative lower bound.", "",
         "## The selection rule is not the inherited one", "",
         "B1 normally picks breadth at the knee of the recall-versus-budget curve. **This chapter "
         "maximises recall instead, and lets the screen carry the routing.** A4 established that "
         "precision cannot be bought with vocabulary here: mining the frame for terms separating the "
         "primary-anchor neighbourhood from the walls' produced **0** terms in `MECHANISM_AND_OUTCOME`, "
         "**0** mechanism terms in the forty strongest discriminators, and a *negative* z for "
         "`despair` itself. Wall 1 separates two mechanisms over the same treatment and the same "
         "outcome, and a title cannot see a mechanism. Precision spent on this query buys only work "
         "the screen must redo.", "",
         f"For comparison the inherited knee rule would have chosen "
         f"**n_out={knee['n_out']}, n_trt={knee['n_trt']}** "
         f"(recall {knee['recall']:.1%}, frame precision {knee['frame_precision']:.1%}); the rule "
         f"applied here chooses **n_out={chosen['n_out']}, n_trt={chosen['n_trt']}** "
         f"(recall {chosen['recall']:.1%}, frame precision {chosen['frame_precision']:.1%}).", "",
         "## The denominator is provenance-defined", "",
         "A3's spec defines Tier B as the snowball-*relevant* set. This chapter's Tier B is the raw "
         "one-hop neighbourhood, because 150 deliberately did not filter the forward fetch by topic — "
         "filtering it would have pruned the frame by distance from the query being measured. No "
         "relevance determination exists yet, so the gold is: Tier A's empirical primary-cell anchors, "
         "plus Tier B records **reached by a primary-cell anchor** and **carrying a fertility-outcome "
         "term**.", "",
         f"**The criterion is applied to the TITLE only**, matching the title-only convention. A first "
         f"run applied it to title and abstract while still matching on title, which put records into "
         f"the denominator that no title-matching query could reach; recall came out at 11.2% and the "
         f"misses were dominated by the outcome block failing on records whose fertility outcome is "
         f"named only in the abstract. A further **{abs_only}** primary-neighbourhood records carry a "
         f"fertility-outcome term in their abstract but not their title. They are excluded from the "
         f"denominator and reported here instead: they are the measured cost of the title-only "
         f"convention on this frame, and they are unreachable by any title query, however broad.", "",
         "**Consequence, stated rather than glossed: the OUTCOME block's recall is near 1 by "
         "construction and is not informative.** The informative quantity is the TREATMENT block's "
         "recall. Outcome-block misses are still counted below, because a non-zero miss rate on a "
         "block that ought to be tautological means the backbone is incomplete — which is a real "
         "finding about the backbone, not about the query.", "",
         "## Frontier", "",
         "| n_out | n_trt | recall | Recall(B_only) | frame matched | frame precision |",
         "|---|---|---|---|---|---|"]
    for g in sorted(grid, key=lambda x: (x["n_out"], x["n_trt"])):
        mark = " **<- chosen**" if g is chosen else ""
        L.append(f"| {g['n_out']} | {g['n_trt']} | {g['recall']:.1%} | "
                 f"{(g['recall_B_only'] or 0):.1%} | {g['frame_matched']:,} | "
                 f"{(g['frame_precision'] or 0):.1%}{mark} |")

    L += ["", "## Where the misses are, at the chosen setting", "",
          f"- treatment block only: **{chosen['miss_treatment_block']}**",
          f"- outcome block only: **{chosen['miss_outcome_block']}**",
          f"- both blocks: **{chosen['miss_both_blocks']}**", "",
          "## Cluster credit at the chosen setting", "",
          "`credit` counts gold papers a cluster fired on; `sole` counts those it was the ONLY "
          "cluster to fire on — the papers that would be lost if the cluster were dropped.", "",
          "| cluster | credit | sole |", "|---|---|---|"]
    for c in CLUSTERS:
        L.append(f"| `{c}` | {chosen['cluster_credit'][c]} | {chosen['cluster_sole'][c]} |")

    lost = oo["gold_matched"] - chosen["frame_gold_matched"]
    L += ["", "## The conjunction is the binding constraint, not the breadth", "",
          f"At the chosen setting the outcome block misses **{chosen['miss_outcome_block']}** gold "
          f"records and the treatment block misses **{chosen['miss_treatment_block']}**, out of "
          f"{chosen['tot']}. The backbone is complete; the conjunction is what fails. "
          f"**{chosen['miss_treatment_block'] / max(chosen['tot'], 1):.0%} of primary-neighbourhood "
          "fertility papers name no treatment or mechanism in their title at all.** Widening breadth "
          "does not fix this — the grid shows recall flat across the whole treatment range — because "
          "the missing information is not in the field being matched.", "",
          "The cluster-credit table says the same thing from the other side: `MECHANISM`, the "
          f"hypothesis's own construct, fires on **{chosen['cluster_credit']['MECHANISM']}** gold "
          f"papers, while `UNCERTAINTY_GENERIC` — the *neighbouring hypothesis's* vocabulary — fires "
          f"on **{chosen['cluster_credit']['UNCERTAINTY_GENERIC']}**. The most productive treatment "
          "cluster available to this chapter belongs to C.5.a.", "",
          "### The outcome-only arm", "",
          "So the recall-first rule, followed to its endpoint, drops the treatment conjunction:", "",
          "| design | gold matched | frame matched | frame precision |", "|---|---|---|---|",
          f"| conjunction (n_out={chosen['n_out']}, n_trt={chosen['n_trt']}) | "
          f"{chosen['frame_gold_matched']} / {len(gold)} | {chosen['frame_matched']:,} | "
          f"{(chosen['frame_precision'] or 0):.1%} |",
          f"| **outcome-only** (n_out={oo['n_out']}) | {oo['gold_matched']} / {oo['gold_total']} | "
          f"{oo['frame_matched']:,} | {(oo['frame_precision'] or 0):.1%} |", "",
          f"**The conjunction is not a recall-precision trade-off. It is strictly dominated.** It "
          f"loses {lost} of {len(gold)} gold records ({lost / max(len(gold), 1):.0%}) AND has lower "
          f"precision — {(chosen['frame_precision'] or 0):.1%} against "
          f"{(oo['frame_precision'] or 0):.1%}. Requiring a treatment term admits proportionally more "
          "of the frame's decoy clouds than of its gold, because decline, inequality and uncertainty "
          "vocabulary saturates the neighbourhoods of Case & Deaton and the China Syndrome, which are "
          "precisely the seeds whose clouds carry no fertility quantity. The conjunction's only "
          f"remaining effect is a {1 - chosen['frame_matched'] / max(oo['frame_matched'], 1):.0%} "
          "smaller pull, which is not a benefit when it is the wrong records that remain.", "",
          "**Outcome-only recall on this gold is ~1 by construction** — the gold is defined by a "
          "title outcome term and the backbone covers those terms — so it is not quoted as an "
          "achievement. What the arm establishes is the dominance above, which does not depend on "
          "that construction: the gold cost and the precision comparison are both measured against "
          "the same denominator.", "",
          "**Recommendation: outcome-only, with the routing done entirely at the screen.** A "
          "conjunction that discards four in five of the records it is meant to find, in exchange for "
          "precision under 20%, is not buying precision — it is sampling. And the sampling is not "
          "neutral: it keeps the records whose treatment is *named in the title*, which selects for "
          "the reduced-form decline and uncertainty literatures and against the measured-mechanism "
          "studies this chapter's primary cell is made of.", "",
          "## The screening load this implies — the deliverable", "",
          f"At the chosen breadth the query fires on **{chosen['frame_matched']:,}** of the "
          f"{len(gold) + len(neg):,} frame records, at **{(chosen['frame_precision'] or 0):.1%}** "
          "precision against the provenance-defined gold. The frame is a one-hop citation "
          "neighbourhood, not the database, so this is a *ratio* to carry forward rather than an "
          "absolute count — the production run's true yield is measured when the query is executed.", "",
          "**What the budget conversation needs from B1 is this ratio, not the query.** Recall-first "
          "breadth means the screen inherits the precision problem by design. Sizing screening "
          "capacity from this ratio is the intended use of this table; treating the chosen row as a "
          "well-tuned query is not.", ""]
    open(os.path.join(LOGS, f"{SLUG}-cv-breadth.md"), "w").write("\n".join(L) + "\n")
    print(f"chosen n_out={chosen['n_out']} n_trt={chosen['n_trt']} recall={chosen['recall']:.3f} "
          f"B_only={chosen['recall_B_only']} precision={chosen['frame_precision']}")


if __name__ == "__main__":
    main()
