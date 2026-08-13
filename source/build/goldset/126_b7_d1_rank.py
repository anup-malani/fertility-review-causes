#!/usr/bin/env python3
"""
126_b7_d1_rank.py — B.7, stage D1. Deterministic ranking and the screening budget cutoff.

D1 is the free, SEMANTICALLY BLIND sieve of the GACS cascade. It orders the 7.2k-record Tier B frame
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

SLUG = "antidepressants-ssri-subfecundity"
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
LOGS = os.path.join(ROOT, "literature", "search-logs")
TIER_A = os.path.join(LOGS, f"{SLUG}-tier-a.json")
TIER_B = os.path.join(LOGS, f"{SLUG}-tier-b-frame.json")
OUT_RANK = os.path.join(LOGS, f"{SLUG}-d1-ranked.json")
OUT_WORK = os.path.join(LOGS, f"{SLUG}-screen-worklist.json")
OUT_LOG = os.path.join(LOGS, f"{SLUG}-d1-log.md")

SCREEN_BUDGET = 400     # semantic-screen capacity for this run; see the log's budget note

# --- Axis 1: the exposure. B.7 owns a drug, so axis 1 is pharmacological rather than anatomical. ---
EXPOSURE_CORE = {
    "antidepressant": 6, "antidepressants": 6, "ssri": 6, "ssris": 6,
    "selective serotonin reuptake": 7, "serotonin reuptake inhibitor": 7, "snri": 5,
    "fluoxetine": 5, "sertraline": 5, "paroxetine": 5, "citalopram": 5, "escitalopram": 5,
    "venlafaxine": 5, "fluvoxamine": 5, "bupropion": 3, "duloxetine": 4, "mirtazapine": 4,
    "tricyclic": 4, "imipramine": 3, "clomipramine": 3, "psychotropic": 3,
    "antidepressant use": 7, "antidepressant treatment": 5, "serotonergic": 4,
}
# --- Axis 2: the fertility outcome. GACS A2 requires AND across the axes for the keyword channel. ---
FERTILITY_CORE = {
    "fertility": 5, "total fertility": 7, "birth rate": 6, "births": 4, "childbearing": 5,
    "family size": 6, "completed fertility": 7, "parity": 4, "number of children": 5,
    "fecundability": 7, "fecundity": 6, "time to pregnancy": 7, "time-to-pregnancy": 7,
    "conception": 4, "childless": 5, "infertility": 4, "subfertility": 5, "subfecundity": 6,
    "semen quality": 6, "sperm concentration": 6, "sperm motility": 5, "spermatogenesis": 4,
    "coital frequency": 7, "sexual frequency": 6, "frequency of intercourse": 7,
    "fertility decline": 7, "tfr": 5, "demographic": 3,
}
# --- Demotions. Ranking signals only; nothing is removed from the frame. ---
# Wall 7. The reconnaissance found this literature at the TOP of the fecundity-term ranking, not in
# its tail, so the weights are heavier than B.5's veterinary demotion: there the animal work was a
# nuisance, here it is the default occupant of the chapter's own vocabulary.
NONHUMAN = {"zebrafish": 9, "daphnia": 9, "medaka": 9, "killifish": 9, "mollusc": 9, "mollusk": 9,
            "crustacean": 8, "invertebrate": 8, "aquatic": 8, "effluent": 8, "ecotoxic": 9,
            "fathead minnow": 9, "snail": 7, "goldfish": 9, "murine": 7, "mice": 5, "rats": 5,
            "rodent": 6, "in vitro cell": 4, "veterinary": 7, "wastewater": 8, "surface water": 7,
            "environmental concentration": 7}
# Wall 4. Expected to be the single largest cell in the corpus, and it shares every exposure term.
PREGNANCY_SAFETY = {"birth defect": 8, "malformation": 8, "teratogen": 8, "preterm": 6,
                    "birth weight": 6, "neonatal": 6, "autism": 7, "pulmonary hypertension": 8,
                    "prenatal exposure": 7, "in utero": 6, "gestational age": 5, "offspring": 5,
                    "breastfeeding": 5, "lactation": 5, "congenital": 7, "neurodevelopment": 6,
                    "during pregnancy": 4}
# Management of the side effect rather than measurement of its consequence.
CLINICAL = {"antidote": 6, "augmentation": 4, "switching": 3, "sildenafil": 5, "tadalafil": 5,
            "randomized controlled trial of": 3, "efficacy and tolerability": 4, "dose": 2,
            "management of": 4, "guideline": 4}
# Kept mild on purpose: the chapter's own ART decoy returned the HIGHEST on-topic fraction of any seed
# cloud in the A4 frame (66.7%), so a heavy fertility-clinic penalty would demote the material most
# likely to carry a usable conception hazard.
MILD = {"in vitro fertilization": 1, "ivf": 1, "icsi": 1}


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
    EMPIRICAL_CELLS = {"PRIMARY_MEDICATION_TO_FERTILITY", "PRIMARY_MALE_FECUNDITY"}
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
        s_exp, h_exp = score_terms(blob, EXPOSURE_CORE)
        s_fert, h_fert = score_terms(blob, FERTILITY_CORE)
        s_non, h_non = score_terms(blob, NONHUMAN)
        s_preg, h_preg = score_terms(blob, PREGNANCY_SAFETY)
        s_clin, h_clin = score_terms(blob, CLINICAL)
        s_mild, _ = score_terms(blob, MILD)
        # Title hits count double: an abstract mentions many things, a title states the subject.
        t_exp, _ = score_terms(title_blob, EXPOSURE_CORE)
        t_fert, _ = score_terms(title_blob, FERTILITY_CORE)

        both_axes = bool(h_exp) and bool(h_fert)
        seeds = set(r["seed_ids"])
        from_primary = bool(seeds & primary_seeds)
        decoy_only = bool(seeds) and seeds <= decoy_seeds

        # The fertility axis is weighted above the exposure axis, which inverts B.5's symmetric
        # treatment. The reason is measured rather than assumed: in the A4 frame the exposure axis is
        # near-universal (every seed cloud is an antidepressant literature) while records carrying a
        # fertility quantity run from 0.7% to 68% by seed. The scarce axis is the informative one.
        score = (s_exp + 2 * s_fert + t_exp + 2 * t_fert
                 + (14 if both_axes else 0)            # the cross-axis AND is the precision engine
                 + 6 * (r["n_seeds"] - 1)              # multi-seed corroboration
                 + (10 if from_primary else 0)
                 + (4 if "backward" in r["channels"] else 0)   # an anchor's own reference list
                 - s_non - s_preg - s_clin - s_mild)
        r2 = {k: r[k] for k in ("id", "doi", "title", "year", "cited_by_count", "type", "venue",
                                "authors", "abstract", "seed_ids", "n_seeds", "channels")}
        r2.update(d1_score=score, both_axes=both_axes, exposure_hits=h_exp[:6],
                  fertility_hits=h_fert[:6], nonhuman_hits=h_non[:4], clinical_hits=h_clin[:4],
                  pregnancy_safety_hits=h_preg[:4],
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
    # Bypass: reached from an empirical primary anchor and carrying at least one FERTILITY-axis
    # term, but ranked below the cutoff.
    #
    # DELIBERATE DEVIATION from B.5, which required a term from its own axis 1. Axis 1 there was the
    # survival channel, which is scarce; axis 1 here is the exposure, which is ubiquitous in a frame
    # built entirely from antidepressant seeds, so the inherited condition would wave through most of
    # the residual and stop being a bypass. The scarce axis is the one that carries information, and
    # for this chapter that is the fertility outcome.
    bypass = [r for r in scored[SCREEN_BUDGET:]
              if r["from_primary_seed"] and r["fertility_hits"] and r["id"] not in top_ids]
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
        ch["no exposure-axis term at all"] += not r["exposure_hits"]
        ch["pregnancy-safety vocabulary (Wall 4)"] += bool(r["pregnancy_safety_hits"])
        ch["no fertility-axis term at all"] += not r["fertility_hits"]

    L = [f"# D1 deterministic rank and screening cutoff — {SLUG} (B.7)", "",
         f"Frame in: **{len(tier_b):,}** Tier B records. After collapsing **{dupes:,}** version "
         f"duplicates on normalized title: **{len(records):,}** distinct works.", "",
         f"**Screened: {len(worklist):,}** — the top **{len(top):,}** by D1 score plus "
         f"**{len(bypass):,}** orthogonal-channel bypasses. **Left unscreened: {len(unscreened):,}.**", "",
         f"**Score at the margin: {margin}.**", "",
         "## What the cutoff drops, stated rather than implied", "",
         f"Of the {len(unscreened):,} unscreened records, {un_both:,} carry terms from both axes and "
         f"{un_primary:,} were reached from an empirical primary anchor (those without a fertility-axis "
         "term, which the bypass requires). The unscreened set is characterized by:", ""]
    for k, v in ch.most_common():
        L.append(f"- {v:,} — {k}")
    L += ["",
          "This is a **budget-bounded screen, not an exhaustive one**, and the number above is the "
          "honest size of the residual. Two things bound the risk. The cross-axis AND is the "
          "precision engine, so a record with no exposure term and no fertility term is very unlikely "
          "to bear on B.7's estimand; and the bypass means a paper reached from a primary anchor is "
          "read even when its keyword signal is weak, which is where the quirky-titled canon lives. "
          "Extending the screen deeper is the obvious next increment if the yield at the margin is "
          "still non-trivial.", "",
          "## Ranking design", "",
          "The score is the two-axis term match (title hits counted twice, since a title states the "
          "subject and an abstract merely mentions it), plus a cross-axis bonus, plus channel "
          "features (multi-seed corroboration, reached-from-a-primary-anchor, present in an anchor's "
          "own reference list), minus demotions for non-human and clinical-management vocabulary.", "",
          "**The demotions are ranking signals and remove nothing.** B.7's two largest expected "
          "off-cells are the pregnancy-safety literature (Wall 4) and the aquatic-ecotoxicology "
          "literature (Wall 7), and a filter deleting them would delete the boundary cases sitting "
          "alongside them — an antidepressant-and-miscarriage study is one word away from a "
          "pregnancy-safety study and belongs to B.5. The fertility-clinic penalty is deliberately "
          "near-zero because the chapter's ART decoy returned the highest on-topic fraction of any "
          "seed cloud in the A4 frame.", "",
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
