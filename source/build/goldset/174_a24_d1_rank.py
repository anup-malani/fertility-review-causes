#!/usr/bin/env python3
"""
174_a24_d1_rank.py — A.24 (dating apps and union-formation friction), stage D1.

Deterministic ranking of the A4 frame and the cut into a semantic-screen worklist. Inherits
`163_a12_d1_rank.py` in structure: collapse version duplicates on normalized title, score two axes
plus demotions, take a budget slice, then add bypasses for the populations where a miss cannot be
recovered downstream. Nothing is deleted at any point — every record keeps its score, rank and hit
lists, so the cutoff can be re-cut without re-running retrieval.

THE AXES ARE ANTI-CORRELATED, AS IN A.12, BUT FOR THE MIRROR REASON — AND THAT MIRROR IS WHY THE
EXPOSURE AXIS MUST NOT BE UP-WEIGHTED. Most chapters have a near-universal exposure axis and a scarce
outcome axis, and up-weight the scarce one. A.24 cannot. A4 measured the two halves of this frame
pulling in opposite directions:

  * the APP half (mechanism, sexual-health and platform clouds) is dense in exposure vocabulary and
    thin on outcomes — Tinder-use 75% app / 11% outcome, `OFF_SEXHEALTH` 43% app / 6% outcome;
  * the IDENTIFIED half (the technology-diffusion seeds, which carry every quasi-experiment this
    chapter can reach) runs the other way — Billari et al. **0% app** / 55% outcome, Bellou 8% app /
    45% outcome.

Up-weighting the exposure axis would therefore demote precisely the evidence the chapter needs, and
up-weighting the outcome axis would demote the mechanism literature. Both carry equal weight and the
**cross-axis AND** does the discriminating.

THE OUTCOME AXIS IS SCORED AS ONE AND REPORTED AS TWO. `UNION_CORE` and `FERT_CORE` contribute
equally, because the chapter's spine is the union link and demoting it would be self-defeating. But
their hits are kept separate on every record, because A4 measured the gap between them — 25.6% union
against 9.5% fertility inside the empirical clouds — and that gap is the chapter's central finding.
A merged axis would make it unrecoverable at D2.

THE EMPTY CELL GETS ITS OWN BYPASS, WHICH IS NEW HERE. `PRIMARY_APP_FERTILITY` has no anchor because
the recon probe found no study that estimates it. A cell that the hypothesis is *about* and that the
evidence base leaves empty is exactly the cell where a budget cutoff is most dangerous: an empty cell
and a cell nobody read produce identical evidence and mean opposite things (B.6's rule). So every
record carrying app vocabulary AND a fertility term is screened wherever it ranks, and the count of
those records is reported as the empty cell's candidate pool. If the pool is read in full and stays
empty, the chapter can say so as a finding rather than as an absence of effort.

WALL 9's BYPASS GATES ON PROVENANCE AND OUTCOME, NEVER ON APP VOCABULARY. A4 measured the wall: of
277 records reachable from a technology-diffusion seed, 21 (7.6%) carry an outcome and no app
vocabulary while only 7 (2.5%) carry app vocabulary at all. Requiring the app axis to find the
population the wall calls invisible is the self-defeating gate A.12 measured at 4 records against
212. Note what A4 also established and what this script must not paper over: the whole identification
neighbourhood is 277 records against A.12's 1,991. The bypass is correct and it is not large.

DEMOTION WEIGHTS ARE SET FROM A4's MEASUREMENTS, NOT FROM INTUITION, AND THEY ARE DELIBERATELY
UNEVEN:

  * GEOCHRONOLOGY and AGRONOMY take the heaviest weights in the chapter. A4 COUNTED their on-outcome
    rates over the entire cloud rather than sampling — 0.0% and 0.1% on a human-anchored vocabulary —
    so demoting them costs nothing measurable. (The plain-vocabulary rate for agronomy read 16.8%,
    which is the word "fertility" meaning SOIL fertility; a homonym family that shares a word with
    the outcome axis cannot be measured with a vocabulary containing that word.)
  * DATING VIOLENCE takes only a MILD weight despite being the largest single cloud in the frame,
    because A4 measured it at **0.0% app vocabulary**: the cross-axis AND already excludes it, and a
    heavy penalty would buy nothing while risking the genuine app-and-abuse seam.
  * SEXUAL HEALTH and PLATFORM ENGINEERING take mild weights for the opposite reason — they run 43%
    and 21% app vocabulary, so they share the exposure axis heavily and a heavy penalty would demote
    real records. Walls 4 and 5 are cut on OUTCOME, a term sieve cannot make that call, and A.12's
    Wall 6 established what happens when one tries.

Output: literature/search-logs/{slug}-d1-ranked.json
        literature/search-logs/{slug}-screen-worklist.json
        literature/search-logs/{slug}-d1-log.md
"""
import json, os, re

SLUG = "dating-apps-union-formation-friction"
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
LOGS = os.path.join(ROOT, "literature", "search-logs")
TIER_A = os.path.join(LOGS, f"{SLUG}-tier-a.json")
TIER_B = os.path.join(LOGS, f"{SLUG}-tier-b-frame.json")
OUT_RANK = os.path.join(LOGS, f"{SLUG}-d1-ranked.json")
OUT_WORK = os.path.join(LOGS, f"{SLUG}-screen-worklist.json")
OUT_LOG = os.path.join(LOGS, f"{SLUG}-d1-log.md")

SCREEN_BUDGET = 800     # semantic-screen capacity for this run; see the log's budget note

# --- Axis 1: the EXPOSURE. Platform names score high because they are unambiguous; the generic
# --- "matchmaking" and "swipe" score low because they carry other senses. NOT up-weighted relative
# --- to axis 2 — see the docstring.
APP_CORE = {
    "dating app": 9, "dating apps": 9, "online dating": 9, "internet dating": 8, "mobile dating": 8,
    "dating website": 8, "dating websites": 8, "dating platform": 8, "dating site": 6,
    "dating sites": 6, "tinder": 9, "grindr": 7, "bumble": 7, "okcupid": 7, "online dater": 8,
    "met online": 7, "dating service": 6, "swiping": 5, "swipe": 4, "matchmaking": 4,
    "digital dating": 8, "app-based": 4,
}

# --- Axis 2a: UNION FORMATION. The outcome this chapter's reachable link actually has.
UNION_CORE = {
    "union formation": 9, "partner formation": 9, "couple formation": 9,
    "relationship formation": 9, "marriage formation": 9, "partnership formation": 9,
    "entry into marriage": 9, "family formation": 8, "marriage rate": 8, "marriage rates": 8,
    "cohabitation": 7, "repartnering": 7, "singlehood": 7, "unpartnered": 7,
    "relationship dissolution": 6, "marital stability": 6, "marital satisfaction": 5,
    "romantic relationship": 5, "pair bond": 6, "marriage": 5, "marital": 4, "divorce": 4,
    "breakup": 4, "commitment": 3, "partnership": 3,
}

# --- Axis 2b: FERTILITY. Scored equally with 2a — the two are one axis for ranking and two for
# --- reporting. The high weights sit on quantities that cannot mean anything but a demographic
# --- outcome, which also keeps agronomic "fertility" out of the top of the queue.
FERT_CORE = {
    "total fertility rate": 9, "total fertility": 9, "completed fertility": 9,
    "cohort fertility": 8, "fertility decline": 8, "fertility rate": 7, "birth rate": 7,
    "childbearing": 7, "transition to parenthood": 8, "number of children": 7,
    "childlessness": 7, "childless": 6, "fertility intention": 7, "birth intention": 7,
    "family size": 6, "tfr": 7, "fertility": 4, "births": 3, "fecundity": 4, "parenthood": 4,
}

# --- The Wall 9 signature: technology diffusion as an exposure. Used as a mild bonus AND as the
# --- gating condition on the Wall 9 bypass. These are the words the identified estimates use INSTEAD
# --- of naming a dating app.
TECH_SIG = {
    "broadband": 8, "high-speed internet": 8, "high speed internet": 8, "internet diffusion": 8,
    "internet access": 6, "smartphone": 7, "mobile phone": 5, "cellular": 5, "3g": 6, "4g": 5,
    "mobile broadband": 7, "internet use": 4, "digital technology": 4, "technology adoption": 5,
    "instrumental variable": 5, "difference-in-differences": 5, "natural experiment": 5,
    "quasi-experimental": 5, "exogenous variation": 5,
}

# --- Demotions. Ranking signals only; nothing is removed from the frame. Weights from A4. ---
# WALL 1, and the best-evidenced demotion in this chapter: A4 counted 6 on-outcome records among
# 4,992 citing works, and 0.0% on a human-anchored vocabulary. Shares NEITHER axis once the app terms
# are word-boundary matched (a bare-substring "dating app" was matching "dating applications").
GEOCHRON = {
    "radiocarbon": 12, "radiometric dating": 12, "luminescence": 12, "geochronolog": 12,
    "dendrochronolog": 12, "osl dating": 12, "cosmogenic": 11, "zircon": 11, "u-pb": 11,
    "stratigraph": 10, "holocene": 10, "pleistocene": 10, "quaternary": 10, "sediment": 9,
    "archaeolog": 9, "palaeo": 9, "paleo": 9, "isotopic": 8, "chronolog": 6,
}
# WALL 2. A4: 0.1% on-outcome on a human-anchored vocabulary. This cloud DOES fire axis 2b through
# the bare word "fertility", exactly as A.12's dairy cloud did, so the cross-axis AND does not handle
# it and the penalty has to.
NONHUMAN = {
    "soil fertility": 12, "agronom": 12, "biofertil": 12, "fertilizer": 10, "fertiliser": 10,
    "crop yield": 11, "rhizobact": 11, "livestock": 10, "bovine": 10, "ovine": 10, " ewe": 10,
    " cattle": 10, "dairy": 9, "maize": 10, "nitrogen": 9, "veterinary": 10, "litter size": 10,
    "poultry": 9, "soil microbial": 11,
}
# WALL 3, DELIBERATELY MILD DESPITE BEING THE LARGEST CLOUD IN THE FRAME. A4 measured it at 0.0% app
# vocabulary, so the cross-axis AND already keeps it out of the head; a heavy penalty would buy
# nothing and would risk the genuine app-and-abuse seam, which is a boundary case for the screen
# rather than for the ranker.
VIOLENCE = {
    "intimate partner violence": 5, "dating violence": 4, "sexual assault": 5, "sexual coercion": 4,
    "victimization": 4, "victimisation": 4, "perpetration": 4, "gender-based violence": 5,
    "domestic violence": 5, "stalking": 4, "child maltreatment": 5, "abusive": 3,
}
# WALL 5, MILD. 43% app vocabulary in A4 — this cloud shares the exposure axis heavily and the wall
# is cut on OUTCOME. A term sieve cannot make that call.
SEXHEALTH = {
    "hiv": 5, "sexually transmitted": 5, "syphilis": 5, "gonorrh": 5, "chlamyd": 5,
    "pre-exposure prophylaxis": 5, "condom": 4, "sexual risk": 4, "men who have sex with men": 4,
    "unprotected sex": 4, "sexual health": 3, "hookup": 2, "casual sex": 2,
}
# WALL 4, MILD, for the same reason and with a sharper precedent: A.12's Wall 6 put its include-side
# anchor almost level with its exclude-side one on cloud vocabulary. Here the include-side anchor
# (Jung et al. 2021, a randomized field experiment with matching outcomes) sits inside exactly this
# vocabulary.
PLATFORM = {
    "recommender": 5, "recommendation algorithm": 5, "collaborative filtering": 5,
    "deep learning": 5, "neural network": 5, "click-through": 4, "user engagement": 3,
    "machine learning": 3, "platform design": 2,
}


def norm(s):
    return " " + re.sub(r"\s+", " ", re.sub(r"[^a-z0-9 ]", " ", (s or "").lower())).strip() + " "


def score_terms(blob, table):
    hits, total = [], 0
    for term, w in table.items():
        if term in blob:
            hits.append(term); total += w
    return total, hits


def main():
    tier_a = json.load(open(TIER_A))
    tier_b = json.load(open(TIER_B))

    APP_CELLS = {"PRIMARY_APP_UNION", "PRIMARY_APP_FERTILITY"}
    TECH_CELLS = {"SECONDARY_TECH_UNION", "SECONDARY_TECH_FERTILITY"}
    app_seeds = {a["openalex_id"] for a in tier_a if a["provisional_cell"] in APP_CELLS}
    tech_seeds = {a["openalex_id"] for a in tier_a if a["provisional_cell"] in TECH_CELLS}
    primary_seeds = app_seeds | tech_seeds
    decoy_seeds = {a["openalex_id"] for a in tier_a if a["provisional_cell"].startswith("OFF_")}
    homonym_seeds = {a["openalex_id"] for a in tier_a
                     if a["provisional_cell"] in ("OFF_HOMONYM_GEOCHRON", "OFF_NONHUMAN")}

    # --- collapse version duplicates on normalized title, keep the most-cited ---
    by_title, dupes, dupe_examples = {}, 0, []
    for r in sorted(tier_b, key=lambda x: -(x.get("cited_by_count") or 0)):
        k = norm(r["title"]).strip()
        if not k:
            by_title[r["id"]] = r
            continue
        if k in by_title:
            keep = by_title[k]
            keep["seed_ids"] = sorted(set(keep["seed_ids"]) | set(r["seed_ids"]))
            keep["n_seeds"] = len(keep["seed_ids"])
            keep.setdefault("version_duplicates", []).append(
                {"id": r["id"], "doi": r.get("doi"), "year": r.get("year")})
            dupes += 1
            if len(dupe_examples) < 8:
                dupe_examples.append((keep["title"][:58], keep.get("doi"), r.get("doi"),
                                      keep.get("cited_by_count"), r.get("cited_by_count")))
        else:
            by_title[k] = r
    records = list(by_title.values())

    scored = []
    for r in records:
        blob = norm(r["title"] + " " + (r.get("abstract") or ""))
        title_blob = norm(r["title"])
        s_app, h_app = score_terms(blob, APP_CORE)
        s_un, h_un = score_terms(blob, UNION_CORE)
        s_fe, h_fe = score_terms(blob, FERT_CORE)
        s_tech, h_tech = score_terms(blob, TECH_SIG)
        s_geo, h_geo = score_terms(blob, GEOCHRON)
        s_non, h_non = score_terms(blob, NONHUMAN)
        s_vio, h_vio = score_terms(blob, VIOLENCE)
        s_sex, h_sex = score_terms(blob, SEXHEALTH)
        s_plat, h_plat = score_terms(blob, PLATFORM)

        t_app, _ = score_terms(title_blob, APP_CORE)
        t_un, _ = score_terms(title_blob, UNION_CORE)
        t_fe, _ = score_terms(title_blob, FERT_CORE)

        has_outcome = bool(h_un) or bool(h_fe)
        both_axes = bool(h_app) and has_outcome
        # The candidate pool for the EMPTY cell. Every one of these is read wherever it ranks.
        empty_cell_candidate = bool(h_app) and bool(h_fe)
        seeds = set(r["seed_ids"])
        from_app_seed = bool(seeds & app_seeds)
        from_tech_seed = bool(seeds & tech_seeds)
        from_primary = bool(seeds & primary_seeds)
        decoy_only = bool(seeds) and seeds <= decoy_seeds
        homonym_only = bool(seeds) and seeds <= homonym_seeds
        # THE WALL 9 SHAPE. Technology exposure plus an outcome and NO app vocabulary — what the
        # identified estimates themselves look like, and what an app-axis screen cannot see. Gated on
        # the tech signature alone; requiring an app term here would re-impose the visibility
        # assumption Wall 9 denies.
        wall9_shape = (len(h_tech) >= 2) and has_outcome and not h_app

        # Neither axis is up-weighted; see the docstring. The cross-axis AND is the precision engine.
        score = (s_app + s_un + s_fe + t_app + t_un + t_fe
                 + (16 if both_axes else 0)
                 + (6 if empty_cell_candidate else 0)   # the cell the hypothesis is about
                 + (8 if wall9_shape else 0)            # invisible to the exposure axis by construction
                 + 6 * (r["n_seeds"] - 1)
                 + (10 if from_primary else 0)
                 + (4 if "backward" in r["channels"] else 0)
                 - s_geo - s_non - s_vio - s_sex - s_plat)

        keep = ("id", "doi", "title", "year", "cited_by_count", "type", "venue", "authors",
                "abstract", "seed_ids", "n_seeds", "channels")
        r2 = {k: r.get(k) for k in keep}
        r2.update(d1_score=score, both_axes=both_axes, wall9_shape=wall9_shape,
                  empty_cell_candidate=empty_cell_candidate, has_outcome=has_outcome,
                  app_hits=h_app[:6], union_hits=h_un[:6], fert_hits=h_fe[:6], tech_hits=h_tech[:4],
                  geochron_hits=h_geo[:4], nonhuman_hits=h_non[:4], violence_hits=h_vio[:3],
                  sexhealth_hits=h_sex[:3], platform_hits=h_plat[:3],
                  from_app_seed=from_app_seed, from_tech_seed=from_tech_seed,
                  from_primary_seed=from_primary, decoy_only=decoy_only, homonym_only=homonym_only,
                  version_duplicates=r.get("version_duplicates"))
        scored.append(r2)

    scored.sort(key=lambda x: (-x["d1_score"], -(x["cited_by_count"] or 0)))
    for i, r in enumerate(scored):
        r["d1_rank"] = i + 1
    json.dump(scored, open(OUT_RANK, "w"), indent=2)

    # ---------------- worklist: budget slice + four bypasses ----------------
    top = scored[:SCREEN_BUDGET]
    top_ids = {r["id"] for r in top}

    # BYPASS 1 — THE EMPTY CELL. App vocabulary AND a fertility term, wherever it ranks. This is the
    # cell the registry entry is about and the cell A3 could not anchor. Ordered FIRST so these
    # records are labelled by the reason that matters rather than absorbed into both-axes.
    bypass_empty = [r for r in scored[SCREEN_BUDGET:]
                    if r["empty_cell_candidate"] and r["id"] not in top_ids]

    # BYPASS 2 — WALL 9. Gated on the technology signature plus an outcome, never on app vocabulary.
    seen = top_ids | {r["id"] for r in bypass_empty}
    bypass_wall9 = [r for r in scored[SCREEN_BUDGET:]
                    if r["wall9_shape"] and r["from_tech_seed"] and r["id"] not in seen]

    # BYPASS 3 — both-axes completeness (B.6's rule). Every record carrying the exposure and an
    # outcome is read wherever it ranks: this chapter's likely headline is a bounded refutation, and
    # a refutation reached by not reading is not a finding.
    seen |= {r["id"] for r in bypass_wall9}
    bypass_both = [r for r in scored[SCREEN_BUDGET:] if r["both_axes"] and r["id"] not in seen]

    # BYPASS 4 — the inherited orthogonal channel: reached from a PRIMARY_APP_* anchor and carrying
    # an outcome term, but ranked below the cutoff. Carried, and its yield MEASURED SEPARATELY at D2:
    # on A.12 this inherited bypass returned 5% against the chapter-specific one's 44%, and an
    # inherited bypass that has stopped paying should be retired rather than carried forever.
    seen |= {r["id"] for r in bypass_both}
    bypass_orth = [r for r in scored[SCREEN_BUDGET:]
                   if r["from_app_seed"] and r["has_outcome"] and r["id"] not in seen]

    worklist = top + bypass_empty + bypass_wall9 + bypass_both + bypass_orth
    empty_ids = {r["id"] for r in bypass_empty}
    w9_ids = {r["id"] for r in bypass_wall9}
    both_ids = {r["id"] for r in bypass_both}
    for r in worklist:
        r["worklist_reason"] = ("budget_top" if r["id"] in top_ids else
                                "bypass_empty_cell" if r["id"] in empty_ids else
                                "bypass_wall9" if r["id"] in w9_ids else
                                "bypass_both_axes" if r["id"] in both_ids else
                                "bypass_orthogonal")
    json.dump(worklist, open(OUT_WORK, "w"), indent=2)

    # ---------------- report ----------------
    work_ids = {x["id"] for x in worklist}
    unscreened = [r for r in scored if r["id"] not in work_ids]
    margin = top[-1]["d1_score"] if top else None
    n_both_total = sum(1 for r in scored if r["both_axes"])
    n_both_work = sum(1 for r in worklist if r["both_axes"])
    n_empty_total = sum(1 for r in scored if r["empty_cell_candidate"])
    n_empty_work = sum(1 for r in worklist if r["empty_cell_candidate"])
    tech_all = [r for r in scored if r["from_tech_seed"]]
    tech_app = sum(1 for r in tech_all if r["app_hits"])
    tech_w9 = sum(1 for r in tech_all if r["wall9_shape"])
    tech_work = sum(1 for r in worklist if r["from_tech_seed"])
    n_union_work = sum(1 for r in worklist if r["union_hits"])
    n_fert_work = sum(1 for r in worklist if r["fert_hits"])
    unscr_hom = sum(1 for r in unscreened if r["homonym_only"])
    unscr_decoy = sum(1 for r in unscreened if r["decoy_only"])
    unscr_both = sum(1 for r in unscreened if r["both_axes"])

    pc = lambda a, b: f"{(a / b * 100):.1f}%" if b else "n/a"
    L = [f"# D1 deterministic rank and screening cutoff — {SLUG} (A.24)", "",
         f"**Frame in: {len(tier_b):,} Tier B records.** {dupes:,} version duplicates collapsed on "
         f"normalized title (most-cited kept), leaving **{len(scored):,} scored records**.", "",
         f"**Worklist out: {len(worklist):,}** — {len(top):,} from the budget slice "
         f"(SCREEN_BUDGET={SCREEN_BUDGET}), plus {len(bypass_empty):,} empty-cell, "
         f"{len(bypass_wall9):,} Wall 9, {len(bypass_both):,} both-axes and {len(bypass_orth):,} "
         f"orthogonal bypasses. **{len(unscreened):,} records go unread by the semantic screen** and "
         "their character is reported below, because a bounded screen that goes unstated reads as a "
         "complete one.", "",
         f"Score at the budget margin: **{margin}**. A D1 score is a queue position, not a verdict; "
         "no record is deleted and every one keeps its score, rank and hit lists, so the cutoff can "
         "be re-cut later without re-running retrieval.", "",
         "## The axes are anti-correlated, so neither is up-weighted", "",
         "A.12 reached the same conclusion from the opposite arrangement. Here the APP half of the "
         "frame is dense in exposure vocabulary and thin on outcomes (Tinder-use 75% app / 11% "
         "outcome; `OFF_SEXHEALTH` 43% / 6%), while the IDENTIFIED half — the technology-diffusion "
         "seeds carrying every quasi-experiment this chapter can reach — runs the other way "
         "(**Billari et al. 0% app / 55% outcome**; Bellou 8% / 45%). Up-weighting the exposure axis "
         "would demote exactly the evidence the chapter needs; up-weighting the outcome axis would "
         "demote the mechanism literature. Equal weight, and the **cross-axis AND** discriminates.", "",
         f"**Records carrying both axes: {n_both_total:,} of {len(scored):,} "
         f"({pc(n_both_total, len(scored))}).** {n_both_work:,} are in the worklist "
         f"(**{pc(n_both_work, n_both_total)}** — the both-axes bypass exists to make this 100%).", "",
         "## The empty cell has its own bypass", "",
         f"`PRIMARY_APP_FERTILITY` has no anchor: the recon probe found eleven records at app "
         "exposure against a population fertility quantity and none was an estimate. A cell the "
         "hypothesis is ABOUT and the evidence base leaves empty is where a budget cutoff is most "
         "dangerous, because an empty cell and a cell nobody read produce identical evidence and "
         "mean opposite things.", "",
         f"**Candidate pool for the empty cell — records carrying app vocabulary AND a fertility "
         f"term: {n_empty_total:,}.** {n_empty_work:,} are in the worklist "
         f"({pc(n_empty_work, n_empty_total)}). If that pool is read in full and still yields no "
         "estimate, the chapter reports an absence it has actually looked for.", "",
         "## Wall 9, measured on the ranked frame", "",
         f"Of **{len(tech_all):,} records reached from a technology-diffusion seed, {tech_app:,} "
         f"carry app vocabulary at all ({pc(tech_app, len(tech_all))})** and {tech_w9:,} carry the "
         f"Wall 9 shape — a technology exposure plus an outcome with no app term "
         f"({pc(tech_w9, len(tech_all))}). {tech_work:,} of the {len(tech_all):,} are in the "
         f"worklist ({pc(tech_work, len(tech_all))}).", "",
         "The bypass gates on the technology signature plus an outcome and NEVER on app vocabulary: "
         "requiring the exposure axis to find the population the wall calls invisible is the "
         "self-defeating gate A.12 measured at 4 records against 212. **What this bypass cannot do "
         "is make the neighbourhood bigger.** A4 established that the entire identification "
         "neighbourhood for this chapter is 277 records against A.12's 1,991. The bypass recovers "
         "what is there; the chapter still has to say plainly that what is there is thin.", "",
         "The breadth is deliberate and its cost is stated: the bypass admits "
         "technology-and-outcome papers generally, so internet-and-labour-supply and "
         "internet-and-wellbeing records arrive beside internet-and-marriage ones. Separating them "
         "is the semantic screen's job. Admitting a same-shaped paper that turns out not to be about "
         "partnering costs one screen read; excluding it costs a record no later stage can recover.", "",
         "## Where the outcome axis stops, on the worklist", "",
         f"**{n_union_work:,} worklist records carry a union construct and {n_fert_work:,} carry a "
         f"fertility quantity** ({pc(n_union_work, len(worklist))} against "
         f"{pc(n_fert_work, len(worklist))}). The two limbs score equally and are reported "
         "separately for exactly this reason: A4 measured the same split inside the empirical clouds "
         "(25.6% union / 9.5% fertility), and it is the chapter's central empirical claim stated as "
         "a property of the literature rather than as an argument.", "",
         "## Bypasses", "",
         "| bypass | n | why it exists |", "|---|---|---|",
         f"| **empty cell** | {len(bypass_empty):,} | app vocabulary AND a fertility term. The cell "
         "the registry entry is about, which A3 could not anchor. Read in full or the chapter cannot "
         "distinguish an empty cell from an unread one. |",
         f"| **Wall 9** | {len(bypass_wall9):,} | technology exposure plus an outcome, no app term, "
         "reached from a technology-diffusion seed. Unreachable by exposure-axis ranking by "
         "construction. |",
         f"| both-axes completeness | {len(bypass_both):,} | every remaining both-axes record, "
         "wherever it ranks. The likely headline is a bounded refutation and a refutation reached by "
         "not reading is not a finding. |",
         f"| orthogonal (inherited) | {len(bypass_orth):,} | reached from a `PRIMARY_APP_*` anchor "
         "with an outcome term but below the cutoff. **Yield to be measured separately at D2**: on "
         "A.12 this inherited bypass returned 5% against the chapter-specific one's 44%, and an "
         "inherited bypass that has stopped paying should be retired rather than carried forever. |", "",
         "## What the cutoff drops, and its character", "",
         f"Of {len(unscreened):,} unread records: **{unscr_hom:,} depend on a homonym seed alone** "
         f"({pc(unscr_hom, max(len(unscreened), 1))}) and {unscr_decoy:,} on a routing decoy alone "
         f"({pc(unscr_decoy, max(len(unscreened), 1))}). **Both-axes records left unread: "
         f"{unscr_both:,}** — this number must be zero, and if it is not the both-axes bypass has a "
         "defect.", "",
         "The homonym share is the intended effect and it is the best-evidenced demotion in the "
         "chapter: A4 counted those clouds' on-outcome rates over their entire citation sets rather "
         "than sampling them — 0.0% for geochronology and 0.1% for agronomy on a human-anchored "
         "vocabulary — so demoting them costs nothing measurable. Nothing is deleted, and `seed_ids` "
         "provenance survives on every record.", "",
         "## Score distribution", "", "| band | n |", "|---|---|"]
    bands = [(60, 10 ** 9), (40, 60), (25, 40), (15, 25), (5, 15), (0, 5), (-10 ** 9, 0)]
    for lo, hi in bands:
        n = sum(1 for r in scored if lo <= r["d1_score"] < hi)
        label = f"{lo} to {hi - 1}" if hi < 10 ** 8 else f"{lo}+"
        if lo == -10 ** 9:
            label = "negative"
        L.append(f"| {label} | {n:,} |")

    L += ["", "## Top 25 by D1 score", "",
          "| # | score | axes | title | year | cites |", "|---|---|---|---|---|---|"]
    for r in scored[:25]:
        ax = ("BOTH" if r["both_axes"] else "app" if r["app_hits"] else
              "out" if r["has_outcome"] else "-")
        if r["wall9_shape"]:
            ax += "+W9"
        if r["empty_cell_candidate"]:
            ax += "+FERT"
        L.append(f"| {r['d1_rank']} | {r['d1_score']} | {ax} | {(r['title'] or '')[:66]} | "
                 f"{r.get('year')} | {r.get('cited_by_count')} |")

    if dupe_examples:
        L += ["", "## Version duplicates collapsed (sample)", "",
              "| title | kept DOI | dropped DOI | cites kept | cites dropped |",
              "|---|---|---|---|---|"]
        for t, d1, d2, c1, c2 in dupe_examples:
            L.append(f"| {t} | `{d1}` | `{d2}` | {c1} | {c2} |")

    L += ["", "## Budget note", "",
          f"SCREEN_BUDGET is {SCREEN_BUDGET} and the worklist came out at {len(worklist):,} because "
          f"the bypasses add {len(worklist) - len(top):,} records the cutoff would have dropped. The "
          "budget governs the ranked head; the bypasses govern completeness on the four populations "
          "where a miss is unrecoverable — the empty cell, the Wall 9 identification set, every "
          "both-axes record, and the orthogonal channel. If the screen's real capacity differs, "
          "change SCREEN_BUDGET and re-run; the bypasses should not be traded away for budget, "
          "because each protects a population no later stage can recover."]
    open(OUT_LOG, "w").write("\n".join(L) + "\n")

    print(f"scored={len(scored)} (from {len(tier_b)} tier_b, {dupes} dupes collapsed)")
    print(f"worklist={len(worklist)}  top={len(top)} empty={len(bypass_empty)} "
          f"wall9={len(bypass_wall9)} both={len(bypass_both)} orth={len(bypass_orth)}")
    print(f"both_axes {n_both_work}/{n_both_total} in worklist; empty-cell pool "
          f"{n_empty_work}/{n_empty_total}; unread both-axes={unscr_both} (must be 0)")
    print(f"unscreened={len(unscreened)} (homonym_only={unscr_hom}, decoy_only={unscr_decoy})")
    print(f"-> {os.path.relpath(OUT_WORK, ROOT)}")
    print(f"-> {os.path.relpath(OUT_LOG, ROOT)}")


if __name__ == "__main__":
    main()
