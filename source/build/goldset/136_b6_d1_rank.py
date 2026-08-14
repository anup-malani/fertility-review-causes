#!/usr/bin/env python3
"""
136_b6_d1_rank.py — B.6, stage D1. Deterministic ranking and the screening budget cutoff.

D1 is the free, SEMANTICALLY BLIND sieve of the GACS cascade. It orders the 14.6k-record Tier B frame
by a two-axis term-match score together with each record's discovery channel, and applies a budget
cutoff so the expensive semantic screen runs on a bounded worklist. It decides nothing about
inclusion: a D1 score is a queue position, not a verdict.

Inherits `126_b7_d1_rank.py`. Four properties this implementation is careful about.

1. THE ORTHOGONAL-CHANNEL BYPASS. Records reached from an empirical primary anchor bypass the cutoff
   even with a weak keyword signal. Without the bypass, a dumb term-match discards exactly the
   orthogonal-recall papers the citation frame exists to catch — the quirky-titled ones the keyword
   axis cannot see. The bypass is why the cutoff can be tight without being reckless.

2. THE BOTH-AXES COMPLETENESS BYPASS (new for B.6). Every record carrying both axes is screened
   wherever it ranks, whatever its chemical family. It began as a microplastics-only rule: that half
   is heading for a finding of "no human study estimates this quantity", and under a budget cutoff
   alone an empty MP fertility cell and an MP fertility cell nobody read produce identical evidence
   and mean opposite things. The first run showed the restriction was incoherent — it left 135
   both-axes PFAS records unscreened while giving the plastic side complete coverage, protecting the
   half heading for a null and under-reading the half that will carry a synthesis. The cross-axis AND
   is this ranker's precision engine, so a record satisfying it is what the screen exists to read.
   After the change, zero both-axes records are left unscreened.

3. THE PENALTIES ARE RANKING SIGNALS, NOT FILTERS. Nothing is deleted. B.6's off-cells are enormous —
   28k microplastics records on environmental occurrence, 19k PFAS records on water treatment, a
   pregnancy-safety literature sharing every exposure term — and a filter removing them would remove
   the boundary cases sitting alongside them. They are demoted so the screen sees them late, not
   never. The fertility-clinic penalty is deliberately near-zero, for a measured reason: the A4 frame
   put the Wall 1 mixture/ART decoy at 51% on-topic, second-highest of any seed.

4. THE CUTOFF IS REPORTED, INCLUDING WHAT IT DROPS. The log states the budget, the score at the
   margin, and the number and character of records left unscreened, because a bounded screen that
   goes unstated reads as a complete one.

CHEMICAL_FAMILY is assigned here, deterministically, because the chapter splits on it and the
compound is the one routing call reliably visible in a title. `both` is a real state — Wall 1's
mixture case — and is never collapsed to one side.

Version duplicates are collapsed here on normalized title, keeping the most-cited record and
recording the collapse — a preprint and its version of record surviving as two studies is a defect
D.3.b shipped and D.1.b caught.

Output: literature/search-logs/{slug}-d1-ranked.json      (the whole frame, scored)
        literature/search-logs/{slug}-screen-worklist.json (what the semantic screen will read)
        literature/search-logs/{slug}-d1-log.md
"""
import json, os, re
from collections import Counter

SLUG = "microplastics-pfas-reproductive"
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
LOGS = os.path.join(ROOT, "literature", "search-logs")
TIER_A = os.path.join(LOGS, f"{SLUG}-tier-a.json")
TIER_B = os.path.join(LOGS, f"{SLUG}-tier-b-frame.json")
OUT_RANK = os.path.join(LOGS, f"{SLUG}-d1-ranked.json")
OUT_WORK = os.path.join(LOGS, f"{SLUG}-screen-worklist.json")
OUT_LOG = os.path.join(LOGS, f"{SLUG}-d1-log.md")

SCREEN_BUDGET = 700     # semantic-screen capacity for this run; see the log's budget note

# --- Axis 1: the exposure. Two chemical families, tagged separately, because the chapter splits
# --- on CHEMICAL_FAMILY and a record that cannot be assigned to one is a record neither chapter
# --- can use. The weights are equal across families: neither is more on-topic than the other.
PFAS_TERMS = {
    "pfas": 6, "pfoa": 6, "pfos": 6, "pfna": 5, "pfhxs": 5, "pfda": 4, "pfba": 4, "genx": 5,
    "perfluoroalkyl": 7, "polyfluoroalkyl": 7, "per and polyfluoroalkyl": 8, "perfluorinated": 6,
    "perfluorooctanoic": 7, "perfluorooctane sulfonate": 7, "fluorochemical": 5,
    "perfluoroalkyl substances": 7, "forever chemical": 5, "fluorotelomer": 4,
}
PLASTIC_TERMS = {
    "microplastic": 7, "microplastics": 7, "nanoplastic": 7, "nanoplastics": 7,
    "micro and nanoplastics": 8, "plastic particle": 6, "polystyrene": 5, "polyethylene": 4,
    "polypropylene": 4, "polyethylene terephthalate": 5, "pet particle": 4, "plastic debris": 5,
    "plastic pollution": 5, "polymer particle": 5, "plastic fragment": 5,
}
EXPOSURE_CORE = {**PFAS_TERMS, **PLASTIC_TERMS}

# --- Axis 2: the fertility outcome. GACS A2 requires AND across the axes for the keyword channel. ---
FERTILITY_CORE = {
    "fertility": 5, "total fertility": 7, "birth rate": 6, "births": 4, "childbearing": 5,
    "family size": 6, "completed fertility": 7, "parity": 4, "number of children": 5,
    "fecundability": 7, "fecundity": 6, "time to pregnancy": 7, "time-to-pregnancy": 7,
    "conception": 4, "childless": 5, "infertility": 4, "subfertility": 5, "subfecundity": 6,
    "semen quality": 6, "sperm concentration": 6, "sperm count": 6, "sperm motility": 5,
    "spermatogenesis": 4, "ovarian reserve": 6, "anti mullerian": 6, "antral follicle": 6,
    "folliculogenesis": 5, "menstrual cycle": 4, "anovulation": 5, "oocyte": 4,
    "fertility decline": 7, "tfr": 5, "demographic": 3,
}

# --- Demotions. Ranking signals only; nothing is removed from the frame. ---
# WALL 5, and it is weighted heavier than any demotion in any prior chapter. The reconnaissance found
# the non-human literature is not in the tail of this chapter's fecundity vocabulary — it IS the
# vocabulary. The A4 frame put the animal floor at 6-42% across every seed cloud, including the PFAS
# clouds. On the microplastics side the most-cited records for "reproduction" and "fecundity" are
# oysters, copepods and rotifers.
NONHUMAN = {"zebrafish": 9, "danio": 9, "daphnia": 9, "medaka": 9, "killifish": 9, "mollusc": 9,
            "mollusk": 9, "mussel": 9, "mytilus": 9, "oyster": 9, "copepod": 9, "calanus": 9,
            "tigriopus": 9, "rotifer": 9, "earthworm": 9, "nematode": 8, "caenorhabditis": 9,
            "drosophila": 8, "sea urchin": 9, "artemia": 9, "gastropod": 9, "bivalve": 9,
            "crustacean": 8, "invertebrate": 8, "aquatic organism": 8, "marine organism": 8,
            "teleost": 9, "amphibian": 8, "xenopus": 9, "murine": 7, "mice": 6, "rats": 6,
            "rodent": 7, "bovine": 6, "porcine": 6, "quail": 7, "ecotoxic": 9, "fathead minnow": 9,
            "aquaculture": 7, "wildlife": 6, "biota": 6}
# The single largest cell in the corpus overall: 28k microplastics records on occurrence and removal,
# 19k PFAS records on drinking water and remediation. It shares axis 1 completely and touches axis 2
# not at all, so the cross-axis AND already handles most of it; these weights handle the rest.
ENV_FATE = {"wastewater": 8, "sediment": 8, "soil": 7, "sludge": 8, "landfill": 8, "estuar": 7,
            "surface water": 7, "groundwater": 7, "remediation": 8, "adsorption": 8, "sorption": 8,
            "degradation": 6, "photocatal": 8, "occurrence": 5, "abundance": 5, "atmospheric": 6,
            "microbial community": 7, "biofilm": 7, "leachate": 8, "effluent": 8,
            "removal efficiency": 8, "water treatment": 7, "environmental fate": 8}
# WALL 8 — the "fertility" homonym. Cheap but load-bearing: these terms poison AXIS 2 specifically,
# which is the axis carrying the information, so a soil-science record can otherwise score as a
# strong fertility hit. Weighted at the level of the axis-2 term it is likely to have matched.
SOIL_FERTILITY = {"soil fertility": 9, "crop yield": 8, "agronomic": 8, "biochar": 9,
                  "fertilizer": 7, "soil health": 8, "arable": 7, "agricultural soil": 8}
# WALL 2. Shares every exposure term and is large (n=1,148 in reconnaissance).
PREGNANCY_SAFETY = {"birth defect": 8, "malformation": 8, "teratogen": 8, "preterm": 6,
                    "birth weight": 6, "neonatal": 6, "autism": 7, "prenatal exposure": 7,
                    "in utero": 6, "gestational age": 5, "offspring": 5, "congenital": 7,
                    "neurodevelopment": 6, "during pregnancy": 4, "cord blood": 5}
# WALL 6. Human-cell work passes the species check and would otherwise read as human evidence.
IN_VITRO = {"cell line": 6, "in vitro": 5, "cultured cells": 6, "cytotoxicity": 7, "hek293": 7,
            "hepg2": 7, "granulosa cell line": 5, "cell viability": 6, "apoptosis assay": 6}
# Non-reproductive PFAS health outcomes: large, and shares axis 1 entirely.
OFF_OUTCOME = {"thyroid": 6, "cholesterol": 6, "immune response": 5, "vaccine": 6, "kidney": 5,
               "hepatic": 5, "cancer risk": 6, "ulcerative colitis": 7, "cardiovascular": 5,
               "diabetes": 5, "obesity": 4}
# Kept mild on purpose, and for a MEASURED reason: in the A4 frame the Wall 1 mixture/ART decoy
# returned 51% on-topic, the second-highest of any seed, and the female tissue-detection literature
# is by construction an IVF literature. A heavy fertility-clinic penalty would demote exactly the
# records most likely to carry a usable exposure-outcome pair.
MILD = {"in vitro fertilization": 1, "ivf": 1, "icsi": 1, "assisted reproductive": 1}


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
        s_env, h_env = score_terms(blob, ENV_FATE)
        s_soil, h_soil = score_terms(blob, SOIL_FERTILITY)
        # "in vitro fertilization" contains "in vitro". Scored naively, every IVF record collects the
        # Wall 6 mechanism penalty, which would silently undo the deliberately near-zero ART penalty
        # three lines below and demote the ART-derived records the A4 diagnostic says are the most
        # productive in the frame. The IVF phrase is removed before the Wall 6 table is applied, and
        # only for that table.
        vitro_blob = blob.replace("in vitro fertilization", " ").replace("in vitro fertilisation", " ")
        s_vitro, h_vitro = score_terms(vitro_blob, IN_VITRO)
        s_offout, h_offout = score_terms(blob, OFF_OUTCOME)
        s_mild, _ = score_terms(blob, MILD)

        # CHEMICAL_FAMILY, assigned deterministically here rather than left to the semantic screen.
        # The chapter splits on this field, so every record needs it, and it is the one routing call
        # that is reliably visible in a title: the compound is named. `both` is a real and frequent
        # state (mixture and exposome designs, n=583 in reconnaissance) and is NOT collapsed to one
        # side — that is Wall 1's MIXTURE_UNSEPARABLE, and forcing a choice here would manufacture a
        # separability the record does not have.
        _, h_pfas = score_terms(blob, PFAS_TERMS)
        _, h_plastic = score_terms(blob, PLASTIC_TERMS)
        if h_pfas and h_plastic:
            family = "both"
        elif h_pfas:
            family = "pfas"
        elif h_plastic:
            family = "plastic"
        else:
            family = "none"
        # Title hits count double: an abstract mentions many things, a title states the subject.
        t_exp, _ = score_terms(title_blob, EXPOSURE_CORE)
        t_fert, _ = score_terms(title_blob, FERTILITY_CORE)

        both_axes = bool(h_exp) and bool(h_fert)
        seeds = set(r["seed_ids"])
        from_primary = bool(seeds & primary_seeds)
        decoy_only = bool(seeds) and seeds <= decoy_seeds

        # The fertility axis is weighted above the exposure axis, inheriting B.7's inversion for the
        # same measured reason: the frame is built entirely from MP/PFAS seeds, so axis 1 is
        # near-universal, while records carrying a fertility quantity ran from 2% to 77% by seed in
        # the A4 diagnostic. The scarce axis is the informative one.
        score = (s_exp + 2 * s_fert + t_exp + 2 * t_fert
                 + (14 if both_axes else 0)            # the cross-axis AND is the precision engine
                 + 6 * (r["n_seeds"] - 1)              # multi-seed corroboration
                 + (10 if from_primary else 0)
                 + (4 if "backward" in r["channels"] else 0)   # an anchor's own reference list
                 - s_non - s_preg - s_env - s_soil - s_vitro - s_offout - s_mild)
        r2 = {k: r[k] for k in ("id", "doi", "title", "year", "cited_by_count", "type", "venue",
                                "authors", "abstract", "seed_ids", "n_seeds", "channels")}
        r2.update(d1_score=score, both_axes=both_axes, chemical_family=family,
                  exposure_hits=h_exp[:6], fertility_hits=h_fert[:6], nonhuman_hits=h_non[:4],
                  env_fate_hits=h_env[:4], soil_hits=h_soil[:3], in_vitro_hits=h_vitro[:3],
                  off_outcome_hits=h_offout[:3], pregnancy_safety_hits=h_preg[:4],
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
    bypass_ids = {r["id"] for r in bypass}

    # SECOND BYPASS, new for B.6: EVERY record carrying both axes is screened, wherever it ranks.
    #
    # This started as a microplastics-only rule, to keep that half's expected finding — "no human
    # study estimates this quantity" — distinguishable from never having looked. Under a budget
    # cutoff alone, an empty MP fertility cell and an MP fertility cell nobody read produce identical
    # evidence and mean opposite things.
    #
    # Restricting it to one family was incoherent and the first run showed why: it left 135
    # both-axes PFAS records unscreened while giving the plastic side complete coverage — that is,
    # it protected the half heading for a null and under-read the half that will actually carry a
    # synthesis. The cross-axis AND is described three functions up as the precision engine; a record
    # satisfying it is precisely what the semantic screen exists to read, whatever its family and
    # whatever its rank. The rule is now family-blind.
    #
    # The cost is bounded by the rarity that motivates it. If this bypass is ever large relative to
    # the budget, that is itself the finding, and the budget becomes a real question rather than a
    # precaution.
    axes_bypass = [r for r in scored[SCREEN_BUDGET:]
                   if r["both_axes"] and r["id"] not in top_ids and r["id"] not in bypass_ids]
    worklist = top + bypass + axes_bypass
    axes_ids = {r["id"] for r in axes_bypass}
    for r in worklist:
        r["screen_source"] = ("d1_budget" if r["id"] in top_ids
                              else "both_axes_completeness_bypass" if r["id"] in axes_ids
                              else "orthogonal_bypass")
    json.dump(worklist, open(OUT_WORK, "w"), indent=2)

    margin = top[-1]["d1_score"] if top else None
    unscreened = [r for r in scored if r["id"] not in {x["id"] for x in worklist}]
    un_both = sum(1 for r in unscreened if r["both_axes"])
    un_primary = sum(1 for r in unscreened if r["from_primary_seed"])
    ch = Counter()
    for r in unscreened:
        ch["non-human vocabulary (Wall 5)"] += bool(r["nonhuman_hits"])
        ch["environmental-fate vocabulary"] += bool(r["env_fate_hits"])
        ch["in-vitro vocabulary (Wall 6)"] += bool(r["in_vitro_hits"])
        ch["pregnancy-safety vocabulary (Wall 2)"] += bool(r["pregnancy_safety_hits"])
        ch["non-reproductive PFAS outcome"] += bool(r["off_outcome_hits"])
        ch["soil-fertility homonym (Wall 8)"] += bool(r["soil_hits"])
        ch["no exposure-axis term at all"] += not r["exposure_hits"]
        ch["no fertility-axis term at all"] += not r["fertility_hits"]
    fam_work = Counter(r["chemical_family"] for r in worklist)
    fam_frame = Counter(r["chemical_family"] for r in scored)
    fam_both = Counter(r["chemical_family"] for r in scored if r["both_axes"])

    L = [f"# D1 deterministic rank and screening cutoff — {SLUG} (B.6)", "",
         f"Frame in: **{len(tier_b):,}** Tier B records. After collapsing **{dupes:,}** version "
         f"duplicates on normalized title: **{len(records):,}** distinct works.", "",
         f"**Screened: {len(worklist):,}** — the top **{len(top):,}** by D1 score, plus "
         f"**{len(bypass):,}** orthogonal-channel bypasses, plus **{len(axes_bypass):,}** "
         f"both-axes completeness bypasses. **Left unscreened: {len(unscreened):,}.**", "",
         f"**Score at the margin: {margin}.**", "",
         "## Chemical family — the split the chapter runs on", "",
         "Assigned deterministically from the named compound, which is the one routing call reliably "
         "visible in a title. `both` is Wall 1's mixture case and is never collapsed to one side.", "",
         "| family | whole frame | carrying both axes | in the worklist |", "|---|---|---|---|"] + [
         f"| `{k}` | {fam_frame.get(k, 0):,} | {fam_both.get(k, 0):,} | {fam_work.get(k, 0):,} |"
         for k in ("pfas", "plastic", "both", "none")] + ["",
         f"**Every record carrying both axes is screened, whatever its family and whatever its "
         f"rank** — {len(axes_bypass):,} were admitted that way, below the budget cutoff. The rule "
         "began as a microplastics-only precaution, so that half's expected finding of 'no human "
         "study estimates this quantity' could be distinguished from never having looked; it was "
         "made family-blind after the first run left 135 both-axes PFAS records unscreened while "
         "giving the plastic side complete coverage. The cross-axis AND is this ranker's precision "
         "engine, so a record satisfying it is what the screen exists to read.", "",
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
          f"worklist={len(worklist)} (top {len(top)} + orthogonal {len(bypass)} "
          f"+ both-axes {len(axes_bypass)}) unscreened={len(unscreened)} "
          f"unscreened_both_axes={un_both} margin_score={margin}")
    print(f"-> {os.path.relpath(OUT_WORK, ROOT)}")


if __name__ == "__main__":
    main()
