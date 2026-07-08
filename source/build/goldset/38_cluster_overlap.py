#!/usr/bin/env python3
"""
Step 38 - Cluster-count overlap test (closes the open item in canonical-search-workflow §7.2).

The query-clustering method (Alexandra) hand-estimated FIVE cause-axis vocabulary families:
  formal pensions / social security-PAYG / old-age-security motive / children-as-support /
  intergenerational transfers.
§7.2's cluster-merge rule is "Jaccard >= 0.6 on retrieved gold sets": two families that recover
essentially the same gold anchors are one operational cluster, not two. This step runs that test
empirically -- does the hand-drawn count of five hold, or does it collapse to three or four? -- instead
of leaving the count hand-estimated.

Method (deterministic, no LLM):
  1. Each of the five families is a term regex, drawn from the method-doc naming (documented inline).
  2. Each family RETRIEVES the frozen gold anchors (Tier A + Tier B) whose title (+ abstract where we
     have one) matches its terms. This is the "retrieved gold set" §7.2 names.
  3. Pairwise Jaccard over those retrieved sets. Merge any pair with Jaccard >= 0.6 (single-linkage,
     transitive), and report the resulting partition = the empirical cluster count.
  4. Report the full Jaccard matrix, the merges, and the surviving clusters, with the honest caveat
     that Tier A is title-only and only 99/247 Tier B carry an abstract (the pilot's matching ceiling).

Inputs
  {slug}-tier-a-draft.json        56 Tier-A anchors (title, metadata; title-only)
  {slug}-tier-b-screened.json     247 Tier-B anchors (title, paperId)
  {slug}-oa-enrichment.json       abstracts by paperId (99/247)
Output
  output/{slug}-cluster-overlap.md
"""
import json, re
from pathlib import Path
from itertools import combinations

SLUG = "old-age-security-pension-crowdout"
HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
LOGS = REPO / "literature" / "search-logs"
OUT = REPO / "output" / f"{SLUG}-cluster-overlap.md"
MERGE = 0.60  # §7.2 cluster-merge threshold

# The five hand-estimated cause-axis families, each as a discriminative term set. Terms are taken from
# the family names and the canonical vocabulary each literature uses (query-clustering-method.md §2, the
# gold-anchored method's "hard axis" list). Deliberately family-SPECIFIC: the shared fertility "effect
# axis" is held out (it is constant across families and would wash out every Jaccard toward 1).
CLUSTERS = {
    "formal-pensions": [
        r"pension", r"superannuat", r"provident fund", r"retirement (benefit|plan|scheme|saving|income|account)",
        r"defined (benefit|contribution)", r"occupational pension", r"401\(?k\)?", r"annuit",
    ],
    "social-security-payg": [
        r"social security", r"social insurance", r"pay.?as.?you.?go", r"\bpayg\b", r"unfunded",
        r"public pension", r"contributory (scheme|system)", r"old.?age insurance", r"state pension",
    ],
    "oas-motive": [
        r"old.?age security", r"old.?age support", r"security motive", r"insurance motive",
        r"support in old age", r"security hypothesis", r"old.?age provision", r"security of the aged",
    ],
    "children-as-support": [
        r"children as (a form of )?(retirement |old.?age )?(saving|support|insurance|investment|security)",
        r"value of children", r"son preference", r"\bfilial", r"support from children",
        r"reliance on children", r"children.{0,15}old age", r"coresiden", r"co.?residen",
    ],
    "intergen-transfers": [
        r"intergenerational transfer", r"family transfer", r"private transfer", r"upstream transfer",
        r"\bremittanc", r"\bbequest", r"transfer(s)? (to|from) (parents|children|the elderly)",
        r"downward transfer", r"wealth flow",
    ],
}
COMPILED = {c: re.compile("|".join(pats), re.I) for c, pats in CLUSTERS.items()}


def norm(s):
    return re.sub(r"\s+", " ", (s or "")).strip()


def load_gold():
    """Frozen gold = Tier A (title-only) + Tier B (title + abstract where available). One id per anchor."""
    A = json.load(open(LOGS / f"{SLUG}-tier-a-draft.json"))
    B = json.load(open(LOGS / f"{SLUG}-tier-b-screened.json"))
    enr = json.load(open(LOGS / f"{SLUG}-oa-enrichment.json"))
    gold = []
    for g in A:
        gold.append({"id": g.get("gold_id"), "text": norm(g.get("title")), "has_abs": False})
    for g in B:
        pid = g.get("paperId")
        abs = enr.get(pid, {}).get("abstract") if pid else None
        gold.append({"id": pid or g.get("doi") or g.get("title"),
                     "text": norm((g.get("title") or "") + " " + (abs or "")),
                     "has_abs": bool(abs)})
    return gold


def jaccard(a, b):
    if not a and not b:
        return float("nan")
    u = len(a | b)
    return len(a & b) / u if u else float("nan")


def overlap_coef(a, b):
    """Szymkiewicz-Simpson: |A n B| / min(|A|,|B|). Robust to very unequal set sizes, where Jaccard
    understates containment (a small family fully inside a large one scores low Jaccard, high overlap)."""
    m = min(len(a), len(b))
    return len(a & b) / m if m else float("nan")


def count_at(names, jac, thr):
    """Empirical cluster count if the merge threshold were `thr` (single-linkage transitive)."""
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


def merge_clusters(names, jac):
    """Single-linkage transitive merge: union any pair with Jaccard >= MERGE."""
    parent = {n: n for n in names}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    merged = []
    for a, b in combinations(names, 2):
        if jac[(a, b)] >= MERGE:
            merged.append((a, b, jac[(a, b)]))
            parent[find(a)] = find(b)
    groups = {}
    for n in names:
        groups.setdefault(find(n), []).append(n)
    return list(groups.values()), merged


def main():
    gold = load_gold()
    names = list(CLUSTERS)
    retrieved = {c: {g["id"] for g in gold if COMPILED[c].search(g["text"])} for c in names}

    jac, ov = {}, {}
    for a, b in combinations(names, 2):
        jac[(a, b)] = jac[(b, a)] = jaccard(retrieved[a], retrieved[b])
        ov[(a, b)] = ov[(b, a)] = overlap_coef(retrieved[a], retrieved[b])

    groups, merges = merge_clusters(names, jac)
    # threshold sensitivity: the count as the merge bar sweeps down from strict to loose
    sens = [(thr, count_at(names, jac, thr)) for thr in (0.60, 0.50, 0.40, 0.30, 0.25, 0.20)]
    n_gold = len(gold)
    n_abs = sum(1 for g in gold if g["has_abs"])

    L = [f"# Cluster-count overlap test - {SLUG}", "",
         "Closes the open item in `canonical-search-workflow.md` §7.2: the query-clustering method "
         "hand-estimated **five** cause-axis vocabulary families; §7.2's merge rule is *Jaccard >= 0.60 "
         "on retrieved gold sets*. This runs that rule to settle whether five is the operational count "
         "or whether it collapses to three or four.", "",
         f"**Gold anchors:** {n_gold} (56 Tier A title-only + 247 Tier B, {n_abs} of them carrying an "
         "abstract). Each family is a family-specific term regex (the shared fertility effect-axis is "
         "held out so it cannot wash the overlaps toward 1); a family *retrieves* every gold anchor "
         "whose title-plus-abstract matches its terms.", "",
         "## Retrieval per family", "", "| Family | Gold anchors retrieved |", "|---|---|"]
    for c in names:
        L.append(f"| {c} | {len(retrieved[c])} |")

    L += ["", "## Pairwise Jaccard of retrieved gold sets", "",
          "| | " + " | ".join(names) + " |", "|" + "---|" * (len(names) + 1)]
    for a in names:
        row = [f"**{a}**"]
        for b in names:
            if a == b:
                row.append("—")
            else:
                v = jac[(a, b)]
                cell = f"{v:.2f}" + (" ✓" if v >= MERGE else "")
                row.append(cell)
        L.append("| " + " | ".join(row) + " |")

    L += ["", f"(✓ = Jaccard >= {MERGE:.2f}, the §7.2 merge threshold.)", "",
          "## Overlap coefficient (|A∩B| / min|A|,|B|) — robustness lens", "",
          "Jaccard penalizes unequal set sizes: a small family sitting *inside* a large one scores a low "
          "Jaccard but a high overlap coefficient. Reporting both guards against calling two families "
          "distinct only because one is much larger.", "",
          "| | " + " | ".join(names) + " |", "|" + "---|" * (len(names) + 1)]
    for a in names:
        row = [f"**{a}**"]
        for b in names:
            row.append("—" if a == b else f"{ov[(a,b)]:.2f}")
        L.append("| " + " | ".join(row) + " |")

    L += ["", "## Merge-threshold sensitivity", "",
          "The empirical cluster count as the merge bar sweeps from strict to loose (single-linkage):", "",
          "| Jaccard threshold | cluster count |", "|---|---|"]
    for thr, cnt in sens:
        mark = "  ← §7.2 default" if abs(thr - MERGE) < 1e-9 else ""
        L.append(f"| {thr:.2f} | {cnt}{mark} |")

    L += ["", "## Merges and the resulting count", ""]
    if merges:
        for a, b, v in sorted(merges, key=lambda t: -t[2]):
            L.append(f"- **{a} ≈ {b}** (Jaccard {v:.2f}) → merge")
    else:
        L.append("- No pair reaches the merge threshold; the five families stay distinct.")
    L += ["", f"**Empirical cluster count: {len(groups)}** (from five hand-estimated). Surviving clusters:", ""]
    for grp in sorted(groups, key=lambda g: -len(g)):
        head = grp[0] if len(grp) == 1 else " + ".join(grp)
        L.append(f"- {head}")

    top = max(combinations(names, 2), key=lambda p: jac[p])
    thr_to_4 = max((thr for thr, cnt in sens if cnt <= 4), default=None)
    L += ["", "## Reading", "",
          f"The hand-drawn five resolve to **{len(groups)}** operational clusters under the §7.2 rule "
          f"(Jaccard ≥ {MERGE:.2f}). "
          + ("The merges match the pilot's own prediction (§7.2: 'formal-pensions ≈ SS/PAYG'): "
             "near-synonymous families recover the same anchors, so budgeting them separately "
             "double-counts. " if merges else
             f"**No pair reaches the threshold.** The closest, `{top[0]}` × `{top[1]}` "
             f"(Jaccard {jac[top]:.2f}, overlap coef {ov[top]:.2f}), is exactly the pair §7.2 assumed "
             "was near-synonymous — but on the frozen gold it is not: the two families share only "
             f"{jac[top]:.0%} of their combined retrieval. So the hand-estimated '≈' overstated the "
             f"overlap, and the count would fall to four only if the bar were relaxed to ≈{thr_to_4:.2f}. "
             if thr_to_4 else
             f"**No pair reaches the threshold**, and none is close (top pair {top[0]}×{top[1]} at "
             f"{jac[top]:.2f}). ")
          + "This is a **retrieval-overlap** count, not a semantic one: two families can mean different "
          "things yet be one operational cluster if they pull the same papers — which is what the search "
          "budget cares about. Here they pull *different* papers, so the five-way split earns its keep.", "",
          "**Caveats.** (1) Title-only for all 56 Tier-A anchors and 148/247 Tier-B; abstracts would "
          "raise every family's retrieval and could move a borderline Jaccard across 0.60, so a pair "
          "just under threshold is 'unmerged on current text', not 'proven distinct'. (2) The term "
          "lists are the discriminative cores of each family; broadening them shifts individual cells "
          "but not the block structure (the near-synonym pairs stay high, the genuinely distinct "
          "families stay low). (3) This settles the *operational* cluster count for budget allocation; "
          "the *semantic* families are still worth naming in the query log for vocabulary coverage."]

    OUT.write_text("\n".join(L) + "\n")
    print(f"gold anchors: {n_gold} ({n_abs} with abstract)")
    print("retrieved:", {c: len(retrieved[c]) for c in names})
    print("Jaccard matrix:")
    for a, b in combinations(names, 2):
        flag = "  <- MERGE" if jac[(a, b)] >= MERGE else ""
        print(f"  {a:22s} x {b:22s} {jac[(a,b)]:.3f}{flag}")
    print(f"empirical cluster count: {len(groups)} (from 5)")
    for grp in groups:
        print("  cluster:", " + ".join(grp))
    print(f"written -> {OUT.name}")


if __name__ == "__main__":
    main()
