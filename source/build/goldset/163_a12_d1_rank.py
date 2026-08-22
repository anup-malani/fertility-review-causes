#!/usr/bin/env python3
"""
163_a12_d1_rank.py — A.12, stage D1. Deterministic ranking and the screening budget cutoff.

D1 is the free, SEMANTICALLY BLIND sieve of the cascade. It orders the Tier B frame by a two-axis
term score plus discovery channel, and applies a budget cutoff so the expensive semantic screen runs
on a bounded worklist. It decides nothing about inclusion: a D1 score is a queue position, not a
verdict. Inherits `136_b6_d1_rank.py`.

THE STRUCTURAL FACT THAT SHAPES THIS RANKER, AND IT IS SPECIFIC TO A.12. In every previous chapter
one axis was near-universal in the frame (the exposure) and the other was scarce and therefore
informative. Here **the two axes are ANTI-CORRELATED across the frame's two halves**, which the A4
diagnostics measured directly:

    seed cloud                     twin%   fert%   BOTH%
    twin-IV canon (BDS)             6.0    32.1     3.7
    twin-IV canon (Rosenzweig)     13.7    58.4    10.9
    demography (Pison-D'Addato)    84.0    47.0    43.2
    demography (Smits-Monden)      82.0    32.0    28.9
    homonym (SHELX)                 2.7     0.0     0.0

The twin-IV half carries fertility vocabulary WITHOUT twinning vocabulary, because those papers are
about family size and child outcomes and mention twins only as their instrument. The demography half
carries twinning vocabulary without a population fertility quantity, because much of it is
vital-statistics tabulation. **The primary cell needs both, so the cross-axis AND is an unusually
sharp precision engine here — and, symmetrically, neither axis alone can be trusted as a floor.**

WALL 8 IS THE REASON THIS SCRIPT NEEDS A SECOND BYPASS, AND IT IS THE MOST LOAD-BEARING ONE IN THE
PROJECT SO FAR. The scope DECLARES Wall 8 unenforceable at title/abstract: a twin-IV paper's abstract
talks about schooling and earnings and never reveals that its first-stage table estimates the
completed-fertility response to a twin birth — which is this chapter's estimand. A term-based ranker
therefore scores exactly the `PRIMARY_OFFSET_FIRSTSTAGE` population LOW on axis 1, by construction.
Those records are reachable only through the citation frame, so:

    records reached from a twin-IV canon seed AND carrying the family-size-IV DESIGN vocabulary
    (two or more of: quantity-quality, instrument, sibship size, birth order, ...) bypass the
    cutoff wherever they rank — with NO twinning term required.

That last clause is the whole design, and the first run got it wrong. Gating the bypass on a twinning
term as well recovered **4** records; gating it on the design vocabulary alone recovers **212**. The
difference is not a loosened threshold, it is a measurement: of 1,991 records reached from a twin-IV
canon seed, only **154 mention a twinning term at all**. Requiring one in order to find the Wall 8
population re-imposes exactly the visibility assumption Wall 8 denies. Seed provenance plus two
independent design terms is already a strong joint condition and does not need a third leg the wall
says cannot be there.

THE BYPASS ADMITS FAMILY-SIZE-IV PAPERS GENERALLY, NOT TWIN-IV PAPERS SPECIFICALLY, and that is
deliberate. The instrument is frequently not named in an abstract either — the admitted set includes
one-child-policy and sibling-sex-composition designs alongside twin designs. D1 is a queue, not a
verdict; separating them is the semantic screen's job and, for the first-stage table itself, full
text's. Admitting a same-shaped design that turns out not to use twins costs one screen read.
Excluding it costs a record that cannot be recovered by any later stage.

THE CLINICAL PENALTY IS DELIBERATELY MILD, FOR A MEASURED REASON — the same shape as B.6's near-zero
ART penalty. Wall 6 was re-cut on OUTCOME (population multiple-birth-rate outcomes in, per-cycle
clinical outcomes out), and a term-based sieve CANNOT make that distinction: an included
transfer-protocol study and an excluded one both say "embryo transfer". The A4 frame showed the
include-side anchor Reynolds 2003 running `clin` at 50.8%, barely below Thurin's 60.6% on the exclude
side. A heavy clinical penalty would therefore demote precisely the ART-multiples records the chapter
was ruled (Call 3) to own. It demotes; it does not decide.

THE HOMONYM PENALTY IS THE HEAVIEST DEMOTION IN ANY CHAPTER, AND IT IS THE BEST EVIDENCED. A4 did not
estimate the homonym on-topic rate from a sample, it counted it: SHELX **13 on-topic of 87,673**
citing works (0.0%), TWIP steel **0 of 1,810**. Crystallographic and metallurgical twinning share
axis 1's vocabulary completely — TWIP fired the twin diagnostic at 29.9% — and axis 2 not at all,
at 0.0%. So the cross-axis AND already handles most of it and these weights handle the residue.
Nothing is deleted: 2,073 Tier B records depend on a homonym seed alone, and a filter removing them
would also remove whatever boundary case sits among them.

PENALTIES ARE RANKING SIGNALS, NEVER FILTERS. Nothing leaves the frame. Every record keeps its score,
its rank and its hit lists, so a later stage can re-cut the cutoff without re-running retrieval.

Version duplicates are collapsed on normalized title, keeping the most-cited record and recording the
collapse — a preprint and its version of record surviving as two studies is a defect D.3.b shipped
and D.1.b caught. On this chapter it also catches the two QJE DOIs of Black, Devereux & Salvanes.

Output: literature/search-logs/{slug}-d1-ranked.json       (the whole frame, scored)
        literature/search-logs/{slug}-screen-worklist.json (what the semantic screen will read)
        literature/search-logs/{slug}-d1-log.md
"""
import json, os, re
from collections import Counter

SLUG = "twinning-multiple-births"
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
LOGS = os.path.join(ROOT, "literature", "search-logs")
TIER_A = os.path.join(LOGS, f"{SLUG}-tier-a.json")
TIER_B = os.path.join(LOGS, f"{SLUG}-tier-b-frame.json")
OUT_RANK = os.path.join(LOGS, f"{SLUG}-d1-ranked.json")
OUT_WORK = os.path.join(LOGS, f"{SLUG}-screen-worklist.json")
OUT_LOG = os.path.join(LOGS, f"{SLUG}-d1-log.md")

SCREEN_BUDGET = 800     # semantic-screen capacity for this run; see the log's budget note

# --- Axis 1: twinning / multiple births. "monozygotic" is deliberately weighted BELOW "dizygotic":
# --- MZ twinning is the twin-DESIGN vocabulary (A.18, Wall 4), while the DZ rate is what actually
# --- varies across populations and with ART and therefore what A.12 is about.
TWIN_CORE = {
    "twinning rate": 9, "twinning rates": 9, "twin birth": 8, "twin births": 8, "twinning": 7,
    "multiple birth": 8, "multiple births": 8, "multiple delivery": 8, "multiple deliveries": 8,
    "multiple pregnanc": 6, "multiple gestation": 6, "higher order multiple": 8, "dizygotic": 7,
    "twin delivery": 8, "triplet": 5, "quadruplet": 5, "twin pair": 3, "twins": 4, "twin": 3,
    "monozygotic": 3,
}

# --- Axis 2: the population fertility quantity. The scarce, informative axis on the twin-IV half of
# --- the frame, and the axis the homonym clouds cannot fire at all (measured 0.0%).
FERT_CORE = {
    "total fertility rate": 9, "total fertility": 9, "completed fertility": 9,
    "cohort fertility": 8, "parity progression": 9, "fertility decline": 7,
    "fertility transition": 6, "birth rate": 6, "childbearing": 5, "family size": 7,
    "number of children": 7, "sibship size": 7, "birth interval": 6, "stopping behavio": 9,
    "parity": 5, "fertility": 5, "births": 4, "childless": 5, "tfr": 6, "demographic": 3,
    "fecundity": 5, "quantum": 3,
}

# --- The twin-IV signature. Used BOTH as a mild bonus and as the gating condition on the Wall 8
# --- bypass. These are the words a paper uses when twins are its INSTRUMENT rather than its subject.
TWIN_IV_SIG = {
    "quantity quality": 8, "quantity-quality": 8, "natural experiment": 6, "instrument": 5,
    "instrumental variable": 7, "exogenous variation": 6, "first stage": 5, "birth order": 5,
    "family size": 5, "sibship size": 6, "child quality": 6, "human capital investment": 5,
}

# --- Demotions. Ranking signals only; nothing is removed from the frame. ---
# WALLS 1-2, and the best-evidenced demotion in the project: A4 COUNTED the on-topic rate rather than
# sampling it — SHELX 13/87,673 and TWIP 0/1,810, both 0.0%. These share axis 1 completely (TWIP fired
# the twin diagnostic at 29.9%) and axis 2 not at all.
HOMONYM = {
    "crystallograph": 12, "crystal structure": 12, "shelx": 12, "space group": 11, "diffract": 10,
    "martensit": 11, "austenit": 11, "twip steel": 12, "trip steel": 12, "digital twin": 12,
    "deformation twinning": 12, "twinning induced plasticity": 12, "stacking fault": 11,
    "dislocation": 10, "grain boundary": 10, "single crystal": 10, "microstructur": 9,
    "lattice": 9, " alloy": 8, "refinement": 6, "twin boundary": 11, "nanotwin": 12,
}
# WALL 3. A4 measured the dairy cloud at 90.0% detectable as non-human. Note this cloud DOES carry
# axis 2 vocabulary — bare "fertility" means bovine fertility there, and the seed's fert diagnostic
# read 34.8% — so the cross-axis AND does NOT handle it and the penalty has to.
NONHUMAN = {
    "ewes": 11, " ewe": 11, "lambing": 11, "ovine": 11, "caprine": 11, "holstein": 11,
    "merino": 11, "heifer": 11, " cattle": 10, "bovine": 10, "dairy": 9, " goat": 10,
    " mare": 9, " calf": 9, " calves": 9, "litter size": 10, "livestock": 10, "veterinary": 10,
    "buffalo": 9, " swine": 9, " sow ": 9, "poultry": 9, "soil fertility": 12, "agronom": 11,
    "crop yield": 11, "fertilizer": 9,
}
# WALL 4 (A.18). Moderate: this is a genuine boundary, routed and never excluded, and the heritability
# of dizygotic twinning is a real A.12 input. A4 measured the cloud thin — Tropf 2017 ran BOTH at
# 1.1% — so a heavy penalty would buy little and risk demoting the DZ-heritability records.
TWINDESIGN = {
    "heritability": 6, "twin study": 5, "twin design": 5, "genome wide": 6, "gwas": 6,
    "polygenic": 6, "genetic variance": 5, "zygosity": 4, "twin registry": 4, "co-twin": 5,
    "behavioral genetic": 5, "behaviour genetic": 5, "genetic and environmental": 5,
}
# WALLS 5-6, DELIBERATELY MILD. See the docstring: the Wall 6 re-cut is on OUTCOME, a term sieve
# cannot make that call, and A4 put the include-side anchor (Reynolds 2003, clin 50.8%) almost level
# with the exclude-side one (Thurin, 60.6%). Heavy weights here would demote the ART-multiples
# records Call 3 ruled this chapter owns.
CLINICAL = {
    "perinatal mortality": 4, "ovarian hyperstimulation": 4, "ohss": 4, "nicu": 4,
    "preterm": 3, "birth weight": 3, "neonatal": 3, "perinatal outcome": 3, "gestational age": 3,
    "caesarean": 3, "cesarean": 3, "stillbirth": 3, "low birth weight": 3, "implantation rate": 3,
    "live birth rate": 2, "pregnancy rate": 2, "cumulative live birth": 2, "morbidity": 2,
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

    STOPPING = {"PRIMARY_OFFSET_STOPPING"}
    FIRSTSTAGE = {"PRIMARY_OFFSET_FIRSTSTAGE"}
    stopping_seeds = {a["openalex_id"] for a in tier_a if a["provisional_cell"] in STOPPING}
    firststage_seeds = {a["openalex_id"] for a in tier_a if a["provisional_cell"] in FIRSTSTAGE}
    primary_seeds = stopping_seeds | firststage_seeds
    decoy_seeds = {a["openalex_id"] for a in tier_a if a["provisional_cell"].startswith("OFF_")}
    homonym_seeds = {a["openalex_id"] for a in tier_a
                     if a["provisional_cell"].startswith("OFF_HOMONYM")}

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
        s_twin, h_twin = score_terms(blob, TWIN_CORE)
        s_fert, h_fert = score_terms(blob, FERT_CORE)
        s_iv, h_iv = score_terms(blob, TWIN_IV_SIG)
        s_hom, h_hom = score_terms(blob, HOMONYM)
        s_non, h_non = score_terms(blob, NONHUMAN)
        s_des, h_des = score_terms(blob, TWINDESIGN)
        s_clin, h_clin = score_terms(blob, CLINICAL)

        t_twin, _ = score_terms(title_blob, TWIN_CORE)
        t_fert, _ = score_terms(title_blob, FERT_CORE)

        both_axes = bool(h_twin) and bool(h_fert)
        seeds = set(r["seed_ids"])
        from_stopping = bool(seeds & stopping_seeds)
        from_firststage = bool(seeds & firststage_seeds)
        from_primary = bool(seeds & primary_seeds)
        decoy_only = bool(seeds) and seeds <= decoy_seeds
        homonym_only = bool(seeds) and seeds <= homonym_seeds
        # The Wall 8 population: twins used as an INSTRUMENT for family size.
        #
        # TWO SEPARATE FLAGS, AND THE DISTINCTION IS THE WHOLE POINT. `twin_iv_shape` requires a twin
        # term as well as the design vocabulary, and is a DIAGNOSTIC only. `iv_design` requires the
        # design vocabulary alone and is what the Wall 8 bypass actually gates on.
        #
        # The first run gated the bypass on `twin_iv_shape` and recovered 4 records, which was the
        # condition being self-defeating rather than the population being small. Measured on this
        # frame: of 1,991 records reached from a twin-IV canon seed, only **154 mention a twin term
        # at all** — 92% of the twin-IV neighbourhood is invisible to axis 1. That is Wall 8 stated
        # as a number, and requiring a twinning term to find the Wall 8 population re-imposes exactly
        # the visibility assumption Wall 8 denies. Seed provenance (it cites the twin-IV canon) plus
        # two independent design terms is already a strong joint condition and does not need a third
        # leg that the wall says cannot be there.
        twin_iv_shape = bool(h_twin) and len(h_iv) >= 2
        iv_design = len(h_iv) >= 2

        # Neither axis is weighted above the other, DEPARTING from B.6/B.7 where the exposure was
        # near-universal and the outcome scarce. Here the axes are anti-correlated across the frame's
        # halves (see docstring), so up-weighting either one would systematically demote one half of
        # the chapter. The cross-axis AND carries the discrimination instead.
        score = (s_twin + s_fert + t_twin + t_fert
                 + (16 if both_axes else 0)           # the cross-axis AND is the precision engine
                 + (8 if twin_iv_shape else 0)        # the Wall 8 population, invisible to axis 1
                 + 6 * (r["n_seeds"] - 1)             # multi-seed corroboration
                 + (10 if from_primary else 0)
                 + (4 if "backward" in r["channels"] else 0)
                 - s_hom - s_non - s_des - s_clin)

        keep = ("id", "doi", "title", "year", "cited_by_count", "type", "venue", "authors",
                "abstract", "seed_ids", "n_seeds", "channels")
        r2 = {k: r.get(k) for k in keep}
        r2.update(d1_score=score, both_axes=both_axes, twin_iv_shape=twin_iv_shape,
                  iv_design=iv_design,
                  twin_hits=h_twin[:6], fert_hits=h_fert[:6], iv_hits=h_iv[:4],
                  homonym_hits=h_hom[:4], nonhuman_hits=h_non[:4], twindesign_hits=h_des[:3],
                  clinical_hits=h_clin[:4], from_stopping_seed=from_stopping,
                  from_firststage_seed=from_firststage, from_primary_seed=from_primary,
                  decoy_only=decoy_only, homonym_only=homonym_only,
                  version_duplicates=r.get("version_duplicates"))
        scored.append(r2)

    scored.sort(key=lambda x: (-x["d1_score"], -(x["cited_by_count"] or 0)))
    for i, r in enumerate(scored):
        r["d1_rank"] = i + 1
    json.dump(scored, open(OUT_RANK, "w"), indent=2)

    # ---------------- worklist: budget slice + three bypasses ----------------
    top = scored[:SCREEN_BUDGET]
    top_ids = {r["id"] for r in top}

    # BYPASS 1 — the orthogonal channel. Reached from a STOPPING-cell anchor and carrying a fertility
    # term, but ranked below the cutoff. This is the inherited bypass and the reason a tight cutoff is
    # not reckless: a dumb term-match discards exactly the quirky-titled records the frame exists to
    # find.
    bypass_orth = [r for r in scored[SCREEN_BUDGET:]
                   if r["from_stopping_seed"] and r["fert_hits"] and r["id"] not in top_ids]

    # BYPASS 2 — WALL 8, and the one this chapter cannot do without. Reached from a twin-IV canon seed
    # AND carrying the twin-IV signature. The scope declares Wall 8 unenforceable at title/abstract,
    # so these records are unreachable by ranking on topic vocabulary BY CONSTRUCTION, and a cutoff
    # that drops them would let the chapter report PRIMARY_OFFSET_FIRSTSTAGE as empty for a reason no
    # later stage could see. The signature is required, not just the seed: the six first-stage seeds
    # carry ~2,700 forward citations and waving all of them through would not be a bypass.
    seen = top_ids | {r["id"] for r in bypass_orth}
    bypass_wall8 = [r for r in scored[SCREEN_BUDGET:]
                    if r["from_firststage_seed"] and r["iv_design"] and r["id"] not in seen]

    # BYPASS 3 — both-axes completeness (inherited from B.6). EVERY record carrying both axes is
    # screened wherever it ranks. B.6's lesson: under a budget cutoff alone, an empty cell and a cell
    # nobody read produce identical evidence and mean opposite things. That matters more here than
    # anywhere, because this chapter's headline verdict is a bounded NEGATIVE — "demographically
    # trivial" — and a negative reached by not reading is not a finding.
    seen |= {r["id"] for r in bypass_wall8}
    bypass_both = [r for r in scored[SCREEN_BUDGET:] if r["both_axes"] and r["id"] not in seen]

    worklist = top + bypass_orth + bypass_wall8 + bypass_both
    for r in worklist:
        r["worklist_reason"] = ("budget_top" if r["id"] in top_ids else
                                "bypass_orthogonal" if r in bypass_orth else
                                "bypass_wall8" if r in bypass_wall8 else "bypass_both_axes")
    json.dump(worklist, open(OUT_WORK, "w"), indent=2)

    # ---------------- report ----------------
    unscreened = [r for r in scored if r["id"] not in {x["id"] for x in worklist}]
    margin = top[-1]["d1_score"] if top else None
    n_both_total = sum(1 for r in scored if r["both_axes"])
    n_both_work = sum(1 for r in worklist if r["both_axes"])
    n_iv_total = sum(1 for r in scored if r["twin_iv_shape"])
    n_iv_work = sum(1 for r in worklist if r["twin_iv_shape"])
    fs_all = [r for r in scored if r["from_firststage_seed"]]
    fs_twin = sum(1 for r in fs_all if r["twin_hits"])
    fs_design = sum(1 for r in fs_all if r["iv_design"])
    fs_work = sum(1 for r in worklist if r["from_firststage_seed"])
    unscr_hom = sum(1 for r in unscreened if r["homonym_only"])
    unscr_decoy = sum(1 for r in unscreened if r["decoy_only"])
    unscr_nonhuman = sum(1 for r in unscreened if r["nonhuman_hits"])

    pc = lambda a, b: f"{(a / b * 100):.1f}%" if b else "n/a"
    L = [f"# D1 deterministic rank and screening cutoff — {SLUG} (A.12)", "",
         f"**Frame in: {len(tier_b):,} Tier B records.** {dupes:,} version duplicates collapsed on "
         f"normalized title (most-cited kept), leaving **{len(scored):,} scored records**.", "",
         f"**Worklist out: {len(worklist):,}** — {len(top):,} from the budget slice "
         f"(SCREEN_BUDGET={SCREEN_BUDGET}), plus {len(bypass_orth):,} orthogonal-channel, "
         f"{len(bypass_wall8):,} Wall 8, and {len(bypass_both):,} both-axes bypasses. "
         f"**{len(unscreened):,} records go unread by the semantic screen** and their character is "
         "reported below, because a bounded screen that goes unstated reads as a complete one.", "",
         f"Score at the budget margin: **{margin}**. A D1 score is a queue position, not a verdict; "
         "no record is deleted and every one keeps its score, rank and hit lists, so the cutoff can "
         "be re-cut later without re-running retrieval.", "",
         "## The two axes are anti-correlated here, which is why neither is up-weighted", "",
         "Every previous chapter had one near-universal axis (the exposure) and one scarce axis (the "
         "outcome), and up-weighted the scarce one. A.12 cannot do that. The A4 diagnostics show the "
         "twin-IV half of the frame carrying fertility vocabulary WITHOUT twinning vocabulary (Black-"
         "Devereux-Salvanes: twin 6.0%, fert 32.1%) and the demography half carrying twinning without "
         "a population fertility quantity (Pison & D'Addato: twin 84.0%, fert 47.0%). Up-weighting "
         "either axis would systematically demote one half of the chapter, so the two carry equal "
         "weight and the **cross-axis AND** does the discriminating.", "",
         f"**Records carrying both axes: {n_both_total:,} of {len(scored):,} "
         f"({pc(n_both_total, len(scored))}).** {n_both_work:,} are in the worklist "
         f"(**{pc(n_both_work, n_both_total)}** — the both-axes bypass exists to make this 100%).", "",
         f"**Records with the twin-IV signature (twin term AND design vocabulary): {n_iv_total:,}.** "
         f"{n_iv_work:,} are in the worklist ({pc(n_iv_work, n_iv_total)}).", "",
         "## Wall 8, measured", "",
         f"Of **{len(fs_all):,} records reached from a twin-IV canon seed, only {fs_twin:,} mention a "
         f"twinning term at all ({pc(fs_twin, len(fs_all))}).** That is Wall 8 stated as a number "
         "rather than as a claim in the scope document: a twin-IV paper's title and abstract are "
         "about schooling, earnings or labour supply, and the twin birth appears only in the "
         "first-stage table. **92% of this chapter's identification neighbourhood is invisible to "
         "axis 1.**", "",
         f"The first version of the Wall 8 bypass required a twinning term as well as the design "
         f"vocabulary and recovered 4 records — the condition was self-defeating, not the population "
         f"small. It now gates on seed provenance plus {2} independent design terms and no twinning "
         f"term, because requiring one re-imposes precisely the visibility assumption the wall "
         f"denies. {fs_design:,} first-stage-seeded records carry the design vocabulary; "
         f"{fs_work:,} of the {len(fs_all):,} are in the worklist "
         f"({pc(fs_work, len(fs_all))}).", "",
         "The bypass admits family-size-IV papers GENERALLY, not twin-IV papers specifically — the "
         "instrument is often unnamed in an abstract too, so the admitted set includes one-child-"
         "policy and sibling-sex-composition designs beside twin designs. That is deliberate. D1 is "
         "a queue, not a verdict; separating them is the semantic screen's job and, for the "
         "first-stage table itself, full text's. Admitting a same-shaped design that turns out not "
         "to use twins costs one screen read; excluding it costs a record no later stage can "
         "recover.", "",
         "## Bypasses", "",
         "| bypass | n | why it exists |", "|---|---|---|",
         f"| orthogonal channel | {len(bypass_orth):,} | reached from a stopping-cell anchor with a "
         "fertility term but ranked below the cutoff — the quirky-titled records a term match cannot see |",
         f"| **Wall 8** | {len(bypass_wall8):,} | reached from a twin-IV canon seed AND carrying the "
         "instrument signature. The scope DECLARES Wall 8 unenforceable at title/abstract, so these "
         "are unreachable by topic ranking by construction. Without this bypass the chapter could "
         "report `PRIMARY_OFFSET_FIRSTSTAGE` empty for a reason no later stage could see. |",
         f"| both-axes completeness | {len(bypass_both):,} | every both-axes record is read wherever "
         "it ranks. This chapter's headline verdict is a bounded NEGATIVE, and a negative reached by "
         "not reading is not a finding. |", "",
         "## What the cutoff drops, and its character", "",
         f"Of {len(unscreened):,} unread records: **{unscr_hom:,} depend on a homonym seed alone** "
         f"({pc(unscr_hom, max(len(unscreened), 1))}), {unscr_decoy:,} on a routing decoy alone, and "
         f"{unscr_nonhuman:,} carry a non-human term. The homonym share is the intended effect: A4 "
         "COUNTED that cloud's on-topic rate rather than sampling it — SHELX 13 on-topic of 87,673 "
         "citing works, TWIP steel 0 of 1,810, both 0.0% — so demoting it costs the chapter nothing "
         "measurable. Nothing is deleted, and `seed_ids` provenance survives on every record.", "",
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
        ax = ("BOTH" if r["both_axes"] else "twin" if r["twin_hits"] else
              "fert" if r["fert_hits"] else "-")
        if r["twin_iv_shape"]:
            ax += "+IV"
        L.append(f"| {r['d1_rank']} | {r['d1_score']} | {ax} | {(r['title'] or '')[:66]} | "
                 f"{r.get('year')} | {r.get('cited_by_count')} |")

    if dupe_examples:
        L += ["", "## Version duplicates collapsed (sample)", "",
              "| title | kept DOI | dropped DOI | cites kept | cites dropped |",
              "|---|---|---|---|---|"]
        for t, d1, d2, c1, c2 in dupe_examples:
            L.append(f"| {t} | `{d1}` | `{d2}` | {c1} | {c2} |")

    L += ["", "## Budget note", "",
          f"SCREEN_BUDGET is set to {SCREEN_BUDGET} and the worklist came out at {len(worklist):,} "
          f"because the bypasses add {len(worklist) - len(top):,} records the cutoff would have "
          "dropped. That is the intended shape: the budget governs the ranked head, and the bypasses "
          "govern completeness on the three populations where a miss is unrecoverable — the "
          "orthogonal channel, the Wall 8 first stages, and every both-axes record. If the semantic "
          "screen's real capacity differs, change SCREEN_BUDGET and re-run; the bypasses should not "
          "be traded away for budget, because each one protects a population that cannot be "
          "recovered downstream."]
    open(OUT_LOG, "w").write("\n".join(L) + "\n")

    print(f"scored={len(scored)} (from {len(tier_b)} tier_b, {dupes} dupes collapsed)")
    print(f"worklist={len(worklist)}  top={len(top)} orth={len(bypass_orth)} "
          f"wall8={len(bypass_wall8)} both={len(bypass_both)}")
    print(f"both_axes {n_both_work}/{n_both_total} in worklist; twin_iv {n_iv_work}/{n_iv_total}")
    print(f"unscreened={len(unscreened)} (homonym_only={unscr_hom}, decoy_only={unscr_decoy})")
    print(f"-> {os.path.relpath(OUT_WORK, ROOT)}")
    print(f"-> {os.path.relpath(OUT_LOG, ROOT)}")


if __name__ == "__main__":
    main()
