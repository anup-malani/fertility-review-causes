#!/usr/bin/env python3
"""
Step 34 - The estimand-and-mechanism gate (GACS §E1/§E3, PI-critique fix #1).

The search was built and graded to recover papers ON THE TOPIC (pensions & fertility).
The review's binding constraint is narrower: does a paper IDENTIFY THE CHAPTER'S EFFECT --
the old-age-security motive -> fertility, forward direction, fertility as the outcome? This
step folds that question into what "meta-analysis-ready" means, and into the recall yardstick.

It reads the RA's estimand adjudication (the RA-review CSV: RETRIEVE = primary cell,
EXCLUDE + a plain reason = off-cell) and produces:

  1. output/{slug}-estimand-ready-set.md      the PRIMARY-cell studies (the pooling set)
  2. output/{slug}-estimand-adjudication.csv   all reviewed studies, each tagged with an
                                               estimand cell + off-cell reason + is_gold_anchor
  3. estimand_filtered_gold.json               the primary-cell empirical anchors, keyed by
                                               gold_id/DOI -- the estimand-filtered recall
                                               denominator (input to the recall re-grade)

It is DETERMINISTIC: the RA decisions are the (immutable) human input; this step only
classifies and reshapes them. Re-running reproduces the artifacts exactly.

Two populations are gated, and the collapse is reported for each:
  - OUTPUT set  : the topical meta-analysis-ready candidates -> the estimand-ready pooling set.
  - GOLD anchors: the strong-ID empirical anchors the query is "built to recover" -> the
                  estimand-filtered anchor set (the corrected scorecard).

Inputs
  output/{slug}-ra-review.csv                     RA estimand adjudication (RETRIEVE/EXCLUDE + note)
  source/build/goldset/tier_a_draft.json          gold Tier A (provenance=="empirical" = the anchors)
  source/build/goldset/tier_a_empirical_clusters.json  member DOIs/titles for robust anchor matching
"""
import json, csv, re, sys
from pathlib import Path

SLUG = "old-age-security-pension-crowdout"
HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
RA_REVIEW = REPO / "output" / f"{SLUG}-ra-review.csv"
TIER_A = HERE / "tier_a_draft.json"
CLUSTERS = HERE / "tier_a_empirical_clusters.json"

OUT_READY = REPO / "output" / f"{SLUG}-estimand-ready-set.md"
OUT_ADJ = REPO / "output" / f"{SLUG}-estimand-adjudication.csv"
OUT_GOLD = HERE / "estimand_filtered_gold.json"

STOP = {"the", "a", "an", "of", "and", "in", "on", "for", "from", "to", "its", "by", "new", "evidence"}


def normdoi(d):
    return (d or "").lower().strip().replace("https://doi.org/", "").replace("http://dx.doi.org/", "")


def norm_tokens(t):
    t = (t or "").lower()
    t = re.sub(r"[^a-z0-9\s]", " ", t)
    return frozenset(w for w in t.split() if w not in STOP)


def jaccard(a, b):
    return len(a & b) / len(a | b) if (a | b) else 0.0


# --- estimand-cell taxonomy: map the RA's plain reason to a controlled vocabulary ----------
# PRIMARY = OAS motive -> fertility, forward direction, fertility as the outcome.
# Every off-cell bucket is a specific way the (cause -> effect) fails to be the chapter's cell.
def classify(decision, note):
    dec = (decision or "").strip().upper()
    if dec == "RETRIEVE":
        return "PRIMARY", "old-age-security motive -> fertility (forward, fertility outcome)"
    n = (note or "").strip().lower()
    if not n:
        return "OFF:unspecified", "excluded, reason not recorded (RA to annotate)"
    # order matters: check the more specific phrasings first
    if "reverse causation" in n or "effect of children on" in n:
        return "OFF:reverse-direction", note
    if "treatment not outcome" in n or "fertility is treatment" in n or "exogenous" in n or "fertility is the treatment" in n:
        return "OFF:fertility-as-cause", note
    if "not an outcome" in n or "not the outcome" in n or "fertility not" in n:
        return "OFF:outcome-not-fertility", note
    if "subsidy" in n or "different treatment" in n:
        return "OFF:different-cause", note  # check before "different mechanism": a subsidy is a different cause, not a channel
    if "different mechanism" in n:
        return "OFF:different-channel", note
    if "irrelevant" in n:
        return "OFF:off-topic", note
    return "OFF:other", note


def load_anchors():
    """The strong-ID empirical gold anchors (Tier A, provenance=='empirical'), enriched with
    member DOIs + titles so the anchor<->review match survives working-paper/published DOI drift."""
    anchors = [r for r in json.load(open(TIER_A)) if r.get("provenance") == "empirical"]
    cl_by_title = {norm_tokens(c["canonical_title"]): c.get("member_dois", [])
                   for c in json.load(open(CLUSTERS))}
    for a in anchors:
        member = cl_by_title.get(norm_tokens(a["title"]), [])
        a["_dois"] = {normdoi(a.get("doi"))} | {normdoi(d) for d in member}
        a["_dois"].discard("")
        a["_tok"] = norm_tokens(a["title"])
    return anchors


def match_anchor(row, anchors):
    """DOI-any, else exact token-set, else title Jaccard >= 0.55 with >= 5 shared tokens.
    The fuzzy fallback catches version variants that DOI/exact matching drops -- e.g. Duflo's
    NBER-WP row ('Old Age Pension ... Intra-household') vs the published WBER anchor E2
    ('Old-Age Pensions ... Intrahousehold'), which score J=0.58 across a subtitle/hyphenation
    difference. The >=5-shared-token guard blocks short-title false positives; on this corpus
    Duflo is the only fuzzy match and the next candidate is below J=0.45 (wide margin)."""
    rd, rt = normdoi(row["DOI"]), norm_tokens(row["Title"])
    for a in anchors:
        if rd and rd in a["_dois"]:
            return a
    for a in anchors:
        if rt and rt == a["_tok"]:
            return a
    best, best_j = None, 0.55
    for a in anchors:
        j = jaccard(rt, a["_tok"])
        if j >= best_j and len(rt & a["_tok"]) >= 5:
            best, best_j = a, j
    return best


def main():
    anchors = load_anchors()
    rows = list(csv.DictReader(open(RA_REVIEW)))

    adjudicated = []
    matched_ids = set()
    for r in rows:
        cell, reason = classify(r["RA Decision"], r["RA Notes"])
        a = match_anchor(r, anchors)
        if a:
            matched_ids.add(a["gold_id"])
        adjudicated.append({
            "rank": r["Rank"], "title": r["Title"], "authors": r["Authors"],
            "year": r["Year"], "doi": r["DOI"],
            "ra_decision": r["RA Decision"].strip(),
            "estimand_cell": cell, "off_cell_reason": reason if cell != "PRIMARY" else "",
            "is_gold_anchor": "yes" if a else "no",
            "gold_id": a["gold_id"] if a else "",
        })

    primary = [a for a in adjudicated if a["estimand_cell"] == "PRIMARY"]
    off = [a for a in adjudicated if a["estimand_cell"] != "PRIMARY"]

    # --- 1. estimand-adjudication.csv (full audit trail) ---
    with open(OUT_ADJ, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(adjudicated[0].keys()))
        w.writeheader()
        w.writerows(adjudicated)

    # --- 2. estimand-ready-set.md (the pooling set) ---
    L = [f"# Estimand-ready set - {SLUG}", "",
         "The papers that identify the chapter's **primary estimand cell**: the old-age-security "
         "motive -> fertility (forward direction, fertility as the outcome). This is the set that can "
         "share a pooled estimate. It is the topical meta-analysis-ready set (§E1) intersected with the "
         "estimand-and-mechanism gate; off-cell papers are retained for their own cells, not here.", "",
         f"**{len(primary)} of {len(adjudicated)}** reviewed studies are estimand-ready.", "",
         "| # | Study | Year | DOI | Gold anchor |", "|---|---|---|---|---|"]
    for i, p in enumerate(sorted(primary, key=lambda x: x["year"] or ""), 1):
        anc = p["gold_id"] if p["is_gold_anchor"] == "yes" else ""
        L.append(f"| {i} | {p['title']} | {p['year']} | {p['doi']} | {anc} |")
    L += ["", "## Off-cell studies, by why they leave the primary cell", ""]
    buckets = {}
    for o in off:
        buckets.setdefault(o["estimand_cell"], []).append(o)
    label = {
        "OFF:outcome-not-fertility": "Outcome is not fertility (schooling, survival, labor supply, savings, migration, health, birth weight, coresidence)",
        "OFF:different-channel": "Different channel (e.g. grandparental childcare - moves fertility the *other* way)",
        "OFF:fertility-as-cause": "Fertility is the cause, not the effect (fertility on the right-hand side)",
        "OFF:reverse-direction": "Reverse direction (effect of children on old-age support / pension take-up)",
        "OFF:different-cause": "Different cause/treatment (subsidy, lottery, employment, kindergarten, family cap)",
        "OFF:off-topic": "Not about old-age security",
        "OFF:unspecified": "Excluded, reason not recorded",
        "OFF:other": "Other",
    }
    for cell, items in sorted(buckets.items(), key=lambda kv: -len(kv[1])):
        L.append(f"**{label.get(cell, cell)}** - {len(items)} studies")
        for o in sorted(items, key=lambda x: x["title"]):
            anc = f" [gold anchor {o['gold_id']}]" if o["is_gold_anchor"] == "yes" else ""
            L.append(f"- {o['title']} ({o['year']}){anc}")
        L.append("")
    OUT_READY.write_text("\n".join(L) + "\n")

    # --- 3. estimand_filtered_gold.json (the corrected recall denominator) ---
    anchor_rows = [a for a in adjudicated if a["is_gold_anchor"] == "yes"]
    anchor_primary = [a for a in anchor_rows if a["estimand_cell"] == "PRIMARY"]
    anchor_off = [a for a in anchor_rows if a["estimand_cell"] != "PRIMARY"]
    filtered_gold = {
        "description": "Estimand-filtered gold: the strong-ID empirical anchors that identify the "
                       "primary estimand cell. Recall should be measured against THIS set, not the "
                       "topical anchor set. Off-cell anchors are excluded from the primary-cell recall "
                       "denominator (they belong to other chapters' cells).",
        "n_empirical_anchors_total": len(anchors),
        "n_anchors_in_review": len(matched_ids),
        "n_primary_cell": len(anchor_primary),
        "n_off_cell": len(anchor_off),
        "primary_cell_anchors": [{"gold_id": a["gold_id"], "title": a["title"], "doi": a["doi"]}
                                 for a in anchor_primary],
        "off_cell_anchors": [{"gold_id": a["gold_id"], "title": a["title"], "doi": a["doi"],
                              "estimand_cell": a["estimand_cell"], "reason": a["off_cell_reason"]}
                             for a in anchor_off],
        "anchors_not_in_review": sorted(set(a["gold_id"] for a in anchors) - matched_ids),
    }
    json.dump(filtered_gold, open(OUT_GOLD, "w"), indent=2)

    # --- console summary ---
    print("=== ESTIMAND-AND-MECHANISM GATE ===", file=sys.stderr)
    print(f"OUTPUT set : {len(adjudicated)} topical reviewed -> {len(primary)} estimand-ready "
          f"(primary cell); {len(off)} off-cell", file=sys.stderr)
    print(f"GOLD anchors: {len(anchors)} strong-ID empirical; {len(matched_ids)} in review -> "
          f"{len(anchor_primary)} primary / {len(anchor_off)} off-cell "
          f"(the corrected scorecard)", file=sys.stderr)
    print(f"  off-cell anchors: {', '.join(a['gold_id'] for a in anchor_off)}", file=sys.stderr)
    print("off-cell buckets:", file=sys.stderr)
    for cell, items in sorted(buckets.items(), key=lambda kv: -len(kv[1])):
        print(f"  {cell:<28} {len(items)}", file=sys.stderr)
    print(f"\nwritten -> {OUT_READY.name}, {OUT_ADJ.name}, {OUT_GOLD.name}", file=sys.stderr)


if __name__ == "__main__":
    main()
