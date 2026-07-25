#!/usr/bin/env python3
"""
81_d3b_cluster_overlap.py - D.3.b (climate anxiety / eco-doomerism), stage A6d.

Mirror of B.1's `71_b1_cluster_overlap.py`. The section 7.2 cluster-count overlap test, run for real
now that the gold exists. A2 could only give a design-time conceptual read; the binding test is
retrieval-overlap on the frozen gold.

A2 fixed FIVE provisional cause-axis families and recorded two design-time predictions worth
testing here:
  - watch-TRIPLE 1 <-> 2 <-> 4 (anxiety construct, habitability fear, eco-doom) are all affective
    dread and were expected to MERGE;
  - family 3 (carbon ethics) was expected to stay DISTINCT, having its own theory tail;
  - honest post-A3 expectation was therefore 3 operational clusters, not 5.

Section 7.2's merge rule: two families that recover essentially the same gold anchors (Jaccard >= 0.60
on retrieved gold sets) are one operational cluster, not two.

Method (deterministic, no LLM):
  1. Each family = a family-SPECIFIC cause-side term regex. The shared fertility/reproductive/intention
     EFFECT axis is held OUT of every family; including it would wash every Jaccard toward 1.
  2. Each family retrieves the gold papers (RELEVANT screen verdicts + Tier-A seeds) whose
     title+abstract matches its terms. Theory is INCLUDED here, unlike the recall work in 79 and 80:
     this test is about cause-axis vocabulary structure, not empirical recall, and the theory stream
     is a genuine part of the cause axis.
  3. Pairwise Jaccard, plus overlap coefficient as a robustness lens for unequal set sizes.
  4. Merge any pair with Jaccard >= 0.60 (single-linkage, transitive); report the surviving partition.

Inputs : output/{slug}-screen-tiers.json, literature/search-logs/{slug}-tier-a.json,
         literature/search-logs/{slug}-tier-b-frame.json (abstracts)
Output : output/{slug}-cluster-overlap.md
"""
import json, re
from pathlib import Path
from itertools import combinations

SLUG = "climate-anxiety-eco-doomerism"
HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
LOGS = REPO / "literature" / "search-logs"
OUT = REPO / "output" / f"{SLUG}-cluster-overlap.md"
MERGE = 0.60

# EFFECT axis held OUT of every family: fertility / childbearing / reproductive outcome / intention.
# The five family regexes below are CAUSE-side only.
CLUSTERS = {
    "climate-anxiety-construct": [
        r"climate anxiet", r"eco-?anxiet", r"climate distress", r"eco-?distress", r"climate worr",
        r"climate concern", r"climate emotion", r"climate grief", r"ecological grief", r"solastalgia",
        r"environmental worr", r"environmental concern", r"climate change anxiet", r"climate fear",
        r"eco-?gu?ilt", r"climate psycholog",
    ],
    "habitability-future-fear": [
        r"habitab", r"bring a child into", r"world to bring", r"future for (their |our )?children",
        r"climate future", r"uncertain future", r"liveab", r"livab", r"planetary boundar",
        r"future generation", r"world (they|we) will inherit", r"quality of life.*future",
        r"what kind of world",
    ],
    "carbon-ethics-antinatalism": [
        r"carbon footprint", r"carbon legacy", r"carbon emission", r"anti-?natalis", r"antinatal",
        r"procreat\w* ethic", r"population ethic", r"environmental ethic", r"moral (duty|obligation)",
        r"overpopulat", r"population growth", r"sustainab\w* population", r"ethics of having",
        r"climate ethic",
    ],
    "eco-doom-pessimism": [
        r"eco-?doom", r"doomis", r"\bdoom\b", r"apocalyp", r"civilizational collapse",
        r"societal collapse", r"eco-?pessimis", r"climate pessimis", r"climate despair",
        r"climate dread", r"hopeless", r"existential (threat|risk|dread)", r"catastroph",
        r"extinction", r"end of the world",
    ],
    "reproductive-decision-motivation": [
        r"reproductive decision", r"childbearing decision", r"family planning decision",
        r"decision-?making", r"reproductive motiv", r"childbearing motiv", r"parenthood motiv",
        r"attitude", r"willingness", r"value orientation", r"ambivalen", r"life course",
        r"reproductive autonom",
    ],
}
COMPILED = {c: re.compile("|".join(p), re.I) for c, p in CLUSTERS.items()}

# A2's design-time predictions, tested explicitly below.
A2_MERGE_TRIPLE = {"climate-anxiety-construct", "habitability-future-fear", "eco-doom-pessimism"}
A2_DISTINCT = "carbon-ethics-antinatalism"
A2_EXPECTED_COUNT = 3


def norm(s):
    return re.sub(r"\s+", " ", (s or "")).strip()


def load_gold():
    rows = json.load(open(REPO / "output" / f"{SLUG}-screen-tiers.json"))
    seeds = json.load(open(LOGS / f"{SLUG}-tier-a.json"))
    fa = {r["paperId"]: (r.get("abstract") or "")
          for r in json.load(open(LOGS / f"{SLUG}-tier-b-frame.json"))}
    gold = []
    for s in seeds:
        if s.get("title"):
            gold.append({"id": s["paperId"], "text": norm(s["title"] + " " + (s.get("abstract") or "")),
                         "has_abs": bool(s.get("abstract"))})
    for r in rows:
        if r["verdict"] == "RELEVANT" and r.get("title"):
            ab = fa.get(r["paperId"], "")
            gold.append({"id": r["paperId"], "text": norm(r["title"] + " " + ab), "has_abs": bool(ab)})
    return gold


def jaccard(a, b):
    u = len(a | b)
    return len(a & b) / u if u else float("nan")


def overlap_coef(a, b):
    m = min(len(a), len(b))
    return len(a & b) / m if m else float("nan")


def _union_find(names, jac, thr):
    parent = {n: n for n in names}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    merges = []
    for a, b in combinations(names, 2):
        if jac[(a, b)] >= thr:
            merges.append((a, b, jac[(a, b)]))
            parent[find(a)] = find(b)
    groups = {}
    for n in names:
        groups.setdefault(find(n), []).append(n)
    return list(groups.values()), merges


def main():
    gold = load_gold()
    names = list(CLUSTERS)
    retrieved = {c: {g["id"] for g in gold if COMPILED[c].search(g["text"])} for c in names}
    jac, ov = {}, {}
    for a, b in combinations(names, 2):
        jac[(a, b)] = jac[(b, a)] = jaccard(retrieved[a], retrieved[b])
        ov[(a, b)] = ov[(b, a)] = overlap_coef(retrieved[a], retrieved[b])
    groups, merges = _union_find(names, jac, MERGE)
    sens = [(thr, len(_union_find(names, jac, thr)[0])) for thr in (0.60, 0.50, 0.40, 0.30, 0.25, 0.20)]
    n_gold = len(gold)
    n_abs = sum(1 for g in gold if g["has_abs"])

    triple_js = {f"{a} x {b}": jac[(a, b)] for a, b in combinations(sorted(A2_MERGE_TRIPLE), 2)}
    triple_merged = all(v >= MERGE for v in triple_js.values())
    carbon_max = max(jac[(A2_DISTINCT, b)] for b in names if b != A2_DISTINCT)

    L = [f"# Cluster-count overlap test (section 7.2) - {SLUG}", "",
         "The binding retrieval-overlap test, now run on the frozen gold. A2 fixed **five** provisional "
         "cause-axis families; the section 7.2 merge rule is *Jaccard >= 0.60 on retrieved gold sets*. "
         "This settles whether five is the operational count or collapses.", "",
         f"**Gold:** {n_gold} papers (RELEVANT screen verdicts + Tier-A seeds), {n_abs} with abstracts. "
         "Each family is a CAUSE-side term regex; the shared fertility/reproductive/intention EFFECT "
         "axis is held out so it cannot wash overlaps toward 1. A family *retrieves* every gold paper "
         "whose title+abstract matches its terms.", "",
         "Theory records are included here, unlike the recall work in steps 79 and 80. This test is "
         "about cause-axis vocabulary structure rather than empirical recall, and the theory stream is "
         "a genuine part of that axis.", "",
         "## Retrieval per family", "", "| Family | Gold retrieved |", "|---|---|"]
    for c in names:
        L.append(f"| {c} | {len(retrieved[c])} |")
    L += ["", "## Pairwise Jaccard of retrieved gold sets", "",
          "| | " + " | ".join(names) + " |", "|" + "---|" * (len(names) + 1)]
    for a in names:
        row = [f"**{a}**"]
        for b in names:
            row.append("-" if a == b else f"{jac[(a,b)]:.2f}" + (" (merge)" if jac[(a, b)] >= MERGE else ""))
        L.append("| " + " | ".join(row) + " |")
    L += ["", f"(merge = Jaccard >= {MERGE:.2f}, the section 7.2 threshold.)", "",
          "## Overlap coefficient (intersection over min set size) - robustness lens", "",
          "| | " + " | ".join(names) + " |", "|" + "---|" * (len(names) + 1)]
    for a in names:
        row = [f"**{a}**"]
        for b in names:
            row.append("-" if a == b else f"{ov[(a,b)]:.2f}")
        L.append("| " + " | ".join(row) + " |")
    L += ["", "## Merge-threshold sensitivity", "",
          "| Jaccard threshold | cluster count |", "|---|---|"]
    for thr, cnt in sens:
        L.append(f"| {thr:.2f} | {cnt}{'  <- section 7.2 default' if abs(thr-MERGE) < 1e-9 else ''} |")
    L += ["", "## Merges and resulting count", ""]
    if merges:
        for a, b, v in sorted(merges, key=lambda t: -t[2]):
            L.append(f"- **{a} approximately equals {b}** (Jaccard {v:.2f}) -> merge")
    else:
        L.append("- No pair reaches the merge threshold; the five families stay distinct.")
    L += ["", f"**Empirical cluster count: {len(groups)}** (from five hand-estimated). "
              "Surviving clusters:", ""]
    for grp in sorted(groups, key=lambda g: -len(g)):
        L.append(f"- {' + '.join(grp) if len(grp) > 1 else grp[0]}")

    L += ["", "## A2's design-time predictions, scored", "",
          f"A2 predicted the affective-dread TRIPLE would merge and that `{A2_DISTINCT}` would stay "
          f"distinct, giving an honest expectation of **{A2_EXPECTED_COUNT}** operational clusters.", "",
          "| A2 prediction | test | outcome |", "|---|---|---|"]
    trip = "; ".join(f"{k} = {v:.2f}" for k, v in triple_js.items())
    L.append(f"| triple (anxiety, habitability, eco-doom) merges | all three pairwise Jaccards >= "
             f"{MERGE:.2f} | {'CONFIRMED' if triple_merged else 'FALSIFIED'} ({trip}) |")
    L.append(f"| `{A2_DISTINCT}` stays distinct | max Jaccard against any other family | "
             f"{'CONFIRMED' if carbon_max < MERGE else 'FALSIFIED'} (max {carbon_max:.2f}) |")
    L.append(f"| operational count = {A2_EXPECTED_COUNT} | empirical count | "
             f"{'CONFIRMED' if len(groups) == A2_EXPECTED_COUNT else 'FALSIFIED'} "
             f"(got {len(groups)}) |")

    top = max(combinations(names, 2), key=lambda p: jac[p])
    L += ["", "## Reading", "",
          f"The A2 five resolve to **{len(groups)}** operational clusters under the section 7.2 rule "
          f"(Jaccard >= {MERGE:.2f}). The closest pair is `{top[0]}` x `{top[1]}` "
          f"(Jaccard {jac[top]:.2f}, overlap {ov[top]:.2f}).", "",
          "This is a retrieval-overlap count, not a semantic one. Two families can mean different "
          "things and still be one operational cluster if they pull the same papers; where they pull "
          "different papers, the split earns its keep for search-budget allocation.", "",
          "**Caveats.** (1) Retrieval is on title+abstract, and the "
          f"{n_gold - n_abs} title-only gold papers under-retrieve, so a borderline pair may read as "
          "'unmerged on current text'. (2) Term lists are discriminative cores; broadening them shifts "
          "cell membership but not the block structure. (3) This is the *operational* count for budget "
          "allocation; the semantic families remain worth naming for vocabulary coverage."]
    OUT.write_text("\n".join(L) + "\n")

    print(f"gold {n_gold} ({n_abs} w/abstract)")
    print("retrieved:", {c: len(retrieved[c]) for c in names})
    for a, b in combinations(names, 2):
        flag = "  <- MERGE" if jac[(a, b)] >= MERGE else ""
        print(f"  {a:34s} x {b:34s} J={jac[(a,b)]:.3f} ov={ov[(a,b)]:.2f}{flag}")
    print(f"empirical cluster count: {len(groups)} (from 5; A2 expected {A2_EXPECTED_COUNT})")
    for grp in groups:
        print("  cluster:", " + ".join(grp))
    print(f"A2 triple-merge prediction: {'CONFIRMED' if triple_merged else 'FALSIFIED'} ({trip})")
    print(f"A2 carbon-distinct prediction: {'CONFIRMED' if carbon_max < MERGE else 'FALSIFIED'} "
          f"(max J {carbon_max:.2f})")


if __name__ == "__main__":
    main()
