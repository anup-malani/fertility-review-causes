#!/usr/bin/env python3
"""
71_b1_cluster_overlap.py — B.1 (evolutionary sex drive / contraceptive decoupling), stage A6d.

The §7.2 cluster-count overlap test, run for real now that the gold exists (A2 could only give a
design-time conceptual read; the binding test is retrieval-overlap on the frozen gold). Mirrors OAS
step 38.

The A2 query-clustering fixed FIVE provisional cause-axis families. §7.2's merge rule: two families
that recover essentially the same gold anchors (Jaccard >= 0.60 on retrieved gold sets) are one
operational cluster, not two. This runs that rule empirically — does the hand-drawn five hold, or
collapse to three or four?

Method (deterministic, no LLM):
  1. Each family = a family-SPECIFIC term regex (the shared fertility/reproductive EFFECT axis is held
     out — including it would wash every Jaccard toward 1).
  2. Each family retrieves the gold papers (RELEVANT screen verdicts + Tier-A seeds) whose title+abstract
     matches its terms.
  3. Pairwise Jaccard (and overlap coefficient, robust to unequal set sizes) over retrieved sets.
  4. Merge any pair with Jaccard >= 0.60 (single-linkage, transitive); report the surviving partition.

Inputs : output/{slug}-screen-tiers.json, literature/search-logs/{slug}-tier-a.json,
         literature/search-logs/{slug}-tier-b-frame.json (abstracts)
Output : output/{slug}-cluster-overlap.md
"""
import json, re
from pathlib import Path
from itertools import combinations

SLUG = "evolutionary-sex-drive-contraceptive-decoupling"
HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
LOGS = REPO / "literature" / "search-logs"
OUT = REPO / "output" / f"{SLUG}-cluster-overlap.md"
MERGE = 0.60

# EFFECT axis — held OUT of every family (shared outcome vocabulary):
#   fertility/birth/reproductive success/reproduction/childbearing/offspring/family size ...
# The five family regexes are CAUSE-side only.
CLUSTERS = {
    "evolutionary-biosocial-theory": [
        r"evolution", r"darwin", r"natural selection", r"sociobiolog", r"life history",
        r"inclusive fitness", r"\bfitness\b", r"biosocial", r"adaptive", r"mismatch", r"maladaptive",
        r"parental investment", r"selfish gene", r"behavioral ecolog", r"evolutionary demograph",
    ],
    "proximate-ultimate": [
        r"proximate", r"ultimate", r"\bstatus\b", r"social status", r"mating success", r"mate competition",
        r"sociosexual", r"dominance", r"\bwealth\b", r"income", r"social success", r"resource",
    ],
    "decoupling-severing": [
        r"decoupl", r"dissociat", r"sever", r"uncoupl", r"delink", r"sex from reproduction",
        r"sex without (reproduction|conception)", r"disconnect", r"break the link", r"severing",
    ],
    "childbearing-motivation": [
        r"childbearing motiv", r"desire for children", r"\bmotivation", r"\bintention", r"procreat",
        r"nurturanc", r"wanting children", r"desire[sd]? for", r"psychological", r"attitude",
    ],
    "contraception-as-technology": [
        r"contracept", r"\bpill\b", r"oral contraceptive", r"birth control", r"family planning",
        r"fertility control", r"fertility regulation", r"contraceptive technolog", r"the pill",
    ],
}
COMPILED = {c: re.compile("|".join(p), re.I) for c, p in CLUSTERS.items()}


def norm(s):
    return re.sub(r"\s+", " ", (s or "")).strip()


def load_gold():
    rows = json.load(open(REPO / "output" / f"{SLUG}-screen-tiers.json"))
    seeds = json.load(open(LOGS / f"{SLUG}-tier-a.json"))
    fa = {r["paperId"]: (r.get("abstract") or "") for r in json.load(open(LOGS / f"{SLUG}-tier-b-frame.json"))}
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


def merge_clusters(names, jac):
    parent = {n: n for n in names}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    merges = []
    for a, b in combinations(names, 2):
        if jac[(a, b)] >= MERGE:
            merges.append((a, b, jac[(a, b)]))
            parent[find(a)] = find(b)
    groups = {}
    for n in names:
        groups.setdefault(find(n), []).append(n)
    return list(groups.values()), merges


def count_at(names, jac, thr):
    parent = {n: n for n in names}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for a, b in combinations(names, 2):
        if jac[(a, b)] >= thr:
            parent[find(a)] = find(b)
    return len({find(n) for n in names})


def main():
    gold = load_gold()
    names = list(CLUSTERS)
    retrieved = {c: {g["id"] for g in gold if COMPILED[c].search(g["text"])} for c in names}
    jac, ov = {}, {}
    for a, b in combinations(names, 2):
        jac[(a, b)] = jac[(b, a)] = jaccard(retrieved[a], retrieved[b])
        ov[(a, b)] = ov[(b, a)] = overlap_coef(retrieved[a], retrieved[b])
    groups, merges = merge_clusters(names, jac)
    sens = [(thr, count_at(names, jac, thr)) for thr in (0.60, 0.50, 0.40, 0.30, 0.25, 0.20)]
    n_gold = len(gold)
    n_abs = sum(1 for g in gold if g["has_abs"])

    L = [f"# Cluster-count overlap test (§7.2) — {SLUG}", "",
         "The binding retrieval-overlap test, now run on the frozen gold (A2 gave only the design-time "
         "conceptual read). A2 fixed **five** provisional cause-axis families; §7.2's merge rule is "
         "*Jaccard >= 0.60 on retrieved gold sets*. This settles whether five is the operational count "
         "or collapses to three/four.", "",
         f"**Gold:** {n_gold} papers (RELEVANT screen verdicts + Tier-A seeds), {n_abs} with abstracts. "
         "Each family = a CAUSE-side term regex (the shared fertility/reproductive EFFECT axis is held "
         "out so it cannot wash overlaps toward 1); a family *retrieves* every gold paper whose "
         "title+abstract matches its terms.", "",
         "## Retrieval per family", "", "| Family | Gold retrieved |", "|---|---|"]
    for c in names:
        L.append(f"| {c} | {len(retrieved[c])} |")
    L += ["", "## Pairwise Jaccard of retrieved gold sets", "",
          "| | " + " | ".join(names) + " |", "|" + "---|" * (len(names) + 1)]
    for a in names:
        row = [f"**{a}**"]
        for b in names:
            row.append("—" if a == b else f"{jac[(a,b)]:.2f}" + (" ✓" if jac[(a, b)] >= MERGE else ""))
        L.append("| " + " | ".join(row) + " |")
    L += ["", f"(✓ = Jaccard >= {MERGE:.2f}, the §7.2 merge threshold.)", "",
          "## Overlap coefficient (|A∩B| / min|A|,|B|) — robustness lens", "",
          "| | " + " | ".join(names) + " |", "|" + "---|" * (len(names) + 1)]
    for a in names:
        row = [f"**{a}**"]
        for b in names:
            row.append("—" if a == b else f"{ov[(a,b)]:.2f}")
        L.append("| " + " | ".join(row) + " |")
    L += ["", "## Merge-threshold sensitivity", "",
          "| Jaccard threshold | cluster count |", "|---|---|"]
    for thr, cnt in sens:
        L.append(f"| {thr:.2f} | {cnt}{'  ← §7.2 default' if abs(thr-MERGE)<1e-9 else ''} |")
    L += ["", "## Merges and resulting count", ""]
    if merges:
        for a, b, v in sorted(merges, key=lambda t: -t[2]):
            L.append(f"- **{a} ≈ {b}** (Jaccard {v:.2f}) → merge")
    else:
        L.append("- No pair reaches the merge threshold; the five families stay distinct.")
    L += ["", f"**Empirical cluster count: {len(groups)}** (from five hand-estimated). Surviving clusters:", ""]
    for grp in sorted(groups, key=lambda g: -len(g)):
        L.append(f"- {' + '.join(grp) if len(grp) > 1 else grp[0]}")

    top = max(combinations(names, 2), key=lambda p: jac[p])
    L += ["", "## Reading", "",
          f"The A2 five resolve to **{len(groups)}** operational clusters under the §7.2 rule "
          f"(Jaccard ≥ {MERGE:.2f}). "
          + ("A2's watch-pair prediction (decoupling ≈ contraception-technology) is tested here directly. "
             if any({"decoupling-severing", "contraception-as-technology"} <= {a, b} for a, b, _ in merges)
             else f"The closest pair is `{top[0]}` × `{top[1]}` (Jaccard {jac[top]:.2f}, overlap "
                  f"{ov[top]:.2f}). ")
          + "This is a retrieval-overlap count, not a semantic one: two families can mean different "
          "things yet be one operational cluster if they pull the same papers. Where they pull different "
          "papers, the split earns its keep for search-budget allocation.", "",
          "**Caveats.** (1) Retrieval is on title+abstract; the "
          f"{n_gold - n_abs} title-only gold papers under-retrieve, so a borderline pair may be "
          "'unmerged on current text'. (2) Term lists are discriminative cores; broadening shifts cells "
          "but not the block structure. (3) This is the *operational* count for budget; the semantic "
          "families remain worth naming for vocabulary coverage."]
    OUT.write_text("\n".join(L) + "\n")
    print(f"gold {n_gold} ({n_abs} w/abstract)")
    print("retrieved:", {c: len(retrieved[c]) for c in names})
    for a, b in combinations(names, 2):
        flag = "  <- MERGE" if jac[(a, b)] >= MERGE else ""
        print(f"  {a:30s} x {b:30s} J={jac[(a,b)]:.3f} ov={ov[(a,b)]:.2f}{flag}")
    print(f"empirical cluster count: {len(groups)} (from 5)")
    for grp in groups:
        print("  cluster:", " + ".join(grp))


if __name__ == "__main__":
    main()
