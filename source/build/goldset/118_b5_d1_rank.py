#!/usr/bin/env python3
"""
118_b5_d1_rank.py — B.5, stage D1. Deterministic ranking and the screening budget cutoff.

D1 is the free, SEMANTICALLY BLIND sieve of the GACS cascade. It orders the 11.5k-record Tier B frame
by a two-axis term-match score together with each record's discovery channel, and applies a budget
cutoff so the expensive semantic screen runs on a bounded worklist. It decides nothing about
inclusion: a D1 score is a queue position, not a verdict.

Three properties this implementation is careful about.

1. THE ORTHOGONAL-CHANNEL BYPASS. Records reached from an empirical primary anchor bypass the cutoff
   even with a weak keyword signal. Without the bypass, a dumb term-match discards exactly the
   orthogonal-recall papers the citation frame exists to catch — the quirky-titled ones the keyword
   axis cannot see. The bypass is why the cutoff can be tight without being reckless.

2. THE PENALTIES ARE RANKING SIGNALS, NOT FILTERS. Non-human and clinical-management vocabulary push a
   record down the queue; nothing is deleted. B.5's two largest expected off-cells are precisely
   veterinary reproductive wastage (Wall 7) and recurrent-pregnancy-loss management, and a filter that
   removed them would also remove the boundary cases that sit alongside them. They are demoted so the
   screen sees them late, not never. The penalty vocabulary is deliberately mild for HLA and
   Hutterite terms, because the chapter's own replacement-compensation anchor lives there.

3. THE CUTOFF IS REPORTED, INCLUDING WHAT IT DROPS. The log states the budget, the score at the
   margin, and the number and character of records left unscreened, because a bounded screen that
   goes unstated reads as a complete one.

Version duplicates are collapsed here on normalized title, keeping the most-cited record and
recording the collapse — a preprint and its version of record surviving as two studies is a defect
D.3.b shipped and D.1.b caught.

Output: literature/search-logs/{slug}-d1-ranked.json      (the whole frame, scored)
        literature/search-logs/{slug}-screen-worklist.json (what the semantic screen will read)
        literature/search-logs/{slug}-d1-log.md
"""
import json, os, re
from collections import Counter

SLUG = "fetal-loss-intrauterine-mortality"
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
LOGS = os.path.join(ROOT, "literature", "search-logs")
TIER_A = os.path.join(LOGS, f"{SLUG}-tier-a.json")
TIER_B = os.path.join(LOGS, f"{SLUG}-tier-b-frame.json")
OUT_RANK = os.path.join(LOGS, f"{SLUG}-d1-ranked.json")
OUT_WORK = os.path.join(LOGS, f"{SLUG}-screen-worklist.json")
OUT_LOG = os.path.join(LOGS, f"{SLUG}-d1-log.md")

SCREEN_BUDGET = 340     # semantic-screen capacity for this run; see the log's budget note

# --- Axis 1: the survival channel. B.5 owns survival conditional on conception. ---
SURVIVAL_CORE = {
    "fetal loss": 6, "fetal death": 6, "fetal mortality": 6, "intrauterine mortality": 7,
    "intrauterine death": 6, "pregnancy loss": 6, "spontaneous abortion": 6, "miscarriage": 5,
    "stillbirth": 5, "stillbirths": 5, "still birth": 5, "pregnancy wastage": 7,
    "fetal wastage": 7, "reproductive wastage": 6, "embryonic mortality": 5,
    "early pregnancy loss": 5, "abortus": 3, "foetal loss": 6, "foetal death": 6,
    "perinatal mortality": 3, "late fetal death": 6, "conceptus": 3, "implantation failure": 3,
}
# --- Axis 2: the fertility outcome. GACS A2 requires AND across the axes for the keyword channel. ---
FERTILITY_CORE = {
    "fertility": 5, "total fertility": 7, "birth rate": 5, "births": 4, "childbearing": 4,
    "family size": 6, "completed fertility": 7, "parity": 4, "parity progression": 7,
    "number of children": 5, "birth interval": 6, "birth spacing": 5, "natural fertility": 7,
    "fecundability": 5, "reproductive span": 5, "tfr": 5, "live birth": 3, "live births": 4,
    "demographic transition": 5, "population growth": 3, "fertility decline": 7,
}
# --- Demotions. Ranking signals only; nothing is removed from the frame. ---
NONHUMAN = {"cattle": 8, "bovine": 8, "sow": 6, "sows": 6, "swine": 8, "porcine": 8, "ewe": 6,
            "ovine": 8, "mare": 5, "equine": 8, "murine": 8, "mice": 6, "rat ": 4, "rats": 5,
            "veterinary": 8, "heifer": 8, "buffalo": 6, "goat": 6, "camelid": 8, "poultry": 8,
            "dairy": 6, "livestock": 8, "marmoset": 6, "macaque": 5, "in vitro embryo": 4}
CLINICAL = {"randomised": 3, "randomized": 3, "clinical trial": 4, "guideline": 4, "therapy": 3,
            "treatment of": 3, "heparin": 5, "aspirin": 4, "progesterone": 3, "antiphospholipid": 4,
            "thrombophilia": 4, "karyotype": 3, "management of": 4, "surgical": 4, "hysteroscop": 5,
            "ultrasound": 3, "ivf": 3, "icsi": 4, "embryo transfer": 4, "cerclage": 5}
# Kept mild on purpose: the chapter's own replacement-compensation anchor is an HLA-sharing study in
# a Hutterite population, so a heavy immunogenetics penalty would demote the value-added literature.
MILD = {"hla": 1, "hutterite": 0}


def norm(s):
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9 ]", " ", (s or "").lower())).strip()


def score_terms(blob, table):
    hits, total = [], 0
    for term, w in table.items():
        if term in blob:
            hits.append(term); total += w
    return total, hits


def main():
    tier_a = json.load(open(TIER_A))
    tier_b = json.load(open(TIER_B))
    EMPIRICAL_CELLS = {"PRIMARY_SHOCK_TO_BIRTHS", "PRIMARY_LOSS_TO_FERTILITY",
                       "REPLACEMENT_COMPENSATION"}
    primary_seeds = {a["openalex_id"] for a in tier_a if a["provisional_cell"] in EMPIRICAL_CELLS}
    decoy_seeds = {a["openalex_id"] for a in tier_a if a["provisional_cell"].startswith("OFF_")}

    # --- collapse version duplicates on normalized title, keep the most-cited ---
    by_title, dupes = {}, 0
    for r in sorted(tier_b, key=lambda x: -(x.get("cited_by_count") or 0)):
        k = norm(r["title"])
        if not k:
            by_title[r["id"]] = r
            continue
        if k in by_title:
            keep = by_title[k]
            keep["seed_ids"] = sorted(set(keep["seed_ids"]) | set(r["seed_ids"]))
            keep["n_seeds"] = len(keep["seed_ids"])
            keep.setdefault("version_duplicates", []).append({"id": r["id"], "doi": r.get("doi"),
                                                              "year": r.get("year")})
            dupes += 1
        else:
            by_title[k] = r
    records = list(by_title.values())

    scored = []
    for r in records:
        blob = norm(r["title"] + " " + (r.get("abstract") or ""))
        title_blob = norm(r["title"])
        s_surv, h_surv = score_terms(blob, SURVIVAL_CORE)
        s_fert, h_fert = score_terms(blob, FERTILITY_CORE)
        s_non, h_non = score_terms(blob, NONHUMAN)
        s_clin, h_clin = score_terms(blob, CLINICAL)
        s_mild, _ = score_terms(blob, MILD)
        # Title hits count double: an abstract mentions many things, a title states the subject.
        t_surv, _ = score_terms(title_blob, SURVIVAL_CORE)
        t_fert, _ = score_terms(title_blob, FERTILITY_CORE)

        both_axes = bool(h_surv) and bool(h_fert)
        seeds = set(r["seed_ids"])
        from_primary = bool(seeds & primary_seeds)
        decoy_only = bool(seeds) and seeds <= decoy_seeds

        score = (s_surv + s_fert + t_surv + t_fert
                 + (12 if both_axes else 0)            # the cross-axis AND is the precision engine
                 + 6 * (r["n_seeds"] - 1)              # multi-seed corroboration
                 + (10 if from_primary else 0)
                 + (4 if "backward" in r["channels"] else 0)   # an anchor's own reference list
                 - s_non - s_clin - s_mild)
        r2 = {k: r[k] for k in ("id", "doi", "title", "year", "cited_by_count", "type", "venue",
                                "authors", "abstract", "seed_ids", "n_seeds", "channels")}
        r2.update(d1_score=score, both_axes=both_axes, survival_hits=h_surv[:6],
                  fertility_hits=h_fert[:6], nonhuman_hits=h_non[:4], clinical_hits=h_clin[:4],
                  from_primary_seed=from_primary, decoy_only=decoy_only,
                  version_duplicates=r.get("version_duplicates"))
        scored.append(r2)

    scored.sort(key=lambda x: (-x["d1_score"], -(x["cited_by_count"] or 0)))
    for i, r in enumerate(scored):
        r["d1_rank"] = i + 1
    json.dump(scored, open(OUT_RANK, "w"), indent=2)

    # --- worklist: the budget slice, plus the orthogonal-channel bypass ---
    top = scored[:SCREEN_BUDGET]
    top_ids = {r["id"] for r in top}
    # Bypass: reached from an empirical primary anchor and carrying at least one survival-axis term,
    # but ranked below the cutoff. The survival-term condition keeps the bypass from importing a
    # primary anchor's entire reference list on subjects the chapter does not touch.
    bypass = [r for r in scored[SCREEN_BUDGET:]
              if r["from_primary_seed"] and r["survival_hits"] and r["id"] not in top_ids]
    worklist = top + bypass
    for r in worklist:
        r["screen_source"] = "d1_budget" if r["id"] in top_ids else "orthogonal_bypass"
    json.dump(worklist, open(OUT_WORK, "w"), indent=2)

    margin = top[-1]["d1_score"] if top else None
    unscreened = [r for r in scored if r["id"] not in {x["id"] for x in worklist}]
    un_both = sum(1 for r in unscreened if r["both_axes"])
    un_primary = sum(1 for r in unscreened if r["from_primary_seed"])
    ch = Counter()
    for r in unscreened:
        ch["non-human vocabulary"] += bool(r["nonhuman_hits"])
        ch["clinical-management vocabulary"] += bool(r["clinical_hits"])
        ch["no survival-axis term at all"] += not r["survival_hits"]
        ch["no fertility-axis term at all"] += not r["fertility_hits"]

    L = [f"# D1 deterministic rank and screening cutoff — {SLUG} (B.5)", "",
         f"Frame in: **{len(tier_b):,}** Tier B records. After collapsing **{dupes:,}** version "
         f"duplicates on normalized title: **{len(records):,}** distinct works.", "",
         f"**Screened: {len(worklist):,}** — the top **{len(top):,}** by D1 score plus "
         f"**{len(bypass):,}** orthogonal-channel bypasses. **Left unscreened: {len(unscreened):,}.**", "",
         f"**Score at the margin: {margin}.**", "",
         "## What the cutoff drops, stated rather than implied", "",
         f"Of the {len(unscreened):,} unscreened records, {un_both:,} carry terms from both axes and "
         f"{un_primary:,} were reached from an empirical primary anchor (those without a survival-axis "
         "term, which the bypass requires). The unscreened set is characterized by:", ""]
    for k, v in ch.most_common():
        L.append(f"- {v:,} — {k}")
    L += ["",
          "This is a **budget-bounded screen, not an exhaustive one**, and the number above is the "
          "honest size of the residual. Two things bound the risk. The cross-axis AND is the "
          "precision engine, so a record with no survival term and no fertility term is very unlikely "
          "to bear on B.5's estimand; and the bypass means a paper reached from a primary anchor is "
          "read even when its keyword signal is weak, which is where the quirky-titled canon lives. "
          "Extending the screen deeper is the obvious next increment if the yield at the margin is "
          "still non-trivial.", "",
          "## Ranking design", "",
          "The score is the two-axis term match (title hits counted twice, since a title states the "
          "subject and an abstract merely mentions it), plus a cross-axis bonus, plus channel "
          "features (multi-seed corroboration, reached-from-a-primary-anchor, present in an anchor's "
          "own reference list), minus demotions for non-human and clinical-management vocabulary.", "",
          "**The demotions are ranking signals and remove nothing.** B.5's two largest expected "
          "off-cells are veterinary reproductive wastage and recurrent-pregnancy-loss management, and "
          "a filter deleting them would delete the boundary cases sitting alongside them. The "
          "immunogenetics penalty is deliberately near-zero because the chapter's own "
          "replacement-compensation anchor is an HLA-sharing study in a Hutterite population.", "",
          "## Top 25 by D1 score", "",
          "| rank | score | axes | seeds | year | title |", "|---|---|---|---|---|---|"]
    for r in scored[:25]:
        L.append(f"| {r['d1_rank']} | {r['d1_score']} | {'both' if r['both_axes'] else 'one'} | "
                 f"{r['n_seeds']} | {r['year']} | {r['title'][:78].replace('|', '/')} |")
    open(OUT_LOG, "w").write("\n".join(L) + "\n")

    print(f"frame={len(tier_b)} dedup={len(records)} (collapsed {dupes}) "
          f"worklist={len(worklist)} (top {len(top)} + bypass {len(bypass)}) "
          f"unscreened={len(unscreened)} margin_score={margin}")
    print(f"-> {os.path.relpath(OUT_WORK, ROOT)}")


if __name__ == "__main__":
    main()
