#!/usr/bin/env python3
"""
189_a17_d1_rank.py — A.17 (assisted reproductive technology access), stage D1.

Deterministic ranking of the A4 frame and the cut into a semantic-screen worklist. Inherits
`174_a24_d1_rank.py` in structure: collapse version duplicates on normalized title, score the axes
plus demotions, take a budget slice, then add bypasses for the populations where a miss cannot be
recovered downstream. Nothing is deleted at any point — every record keeps its score, rank and hit
lists, so the cutoff can be re-cut without re-running retrieval.

THE EXPOSURE AXIS IS USELESS HERE AND IS NOT SCORED AS AN AXIS AT ALL. Every prior chapter scored an
exposure axis against an outcome axis and let the cross-axis AND do the discriminating. A.17 cannot:
the frame was pulled entirely from ART seeds, so ART vocabulary is ambient — **42% of the frame
carries it explicitly and the rest is ART-adjacent by construction**. Scoring it would rank the
clinical decoy cloud alongside the primary cell and call the result precision. ART terms are
retained on each record as `art_hits` for reporting, and contribute ZERO to the score.

WHAT DISCRIMINATES INSTEAD IS THE ARM SIGNATURE, AND THERE ARE TWO OF THEM. A.17's scope found the
hypothesis has two arms answering different questions, and they have different vocabularies:

  * ARM 2 (access) = an ACCESS exposure x a population outcome. **197 records carry access
    vocabulary (2.6% of the frame); 148 carry it with an outcome.**
  * ARM 1 (accounting) = COUNTING language x a population outcome. **236 carry counting language
    (3.1%); 156 carry it with an outcome.**

Both are scored, separately and equally, and their hits are kept apart on every record. Merging them
would produce a ranker that cannot tell a study estimating a policy response from a report tabulating
a share — which is precisely the distinction the chapter turns on and the one the scope says a
title/abstract screen cannot make unaided.

IDENTIFICATION LANGUAGE GETS A REAL BONUS, AND A4 IS WHY. A4 measured identification vocabulary at
1.4% in arm-1 neighbourhoods against 5.6% in arm-2 ones — a 4x ratio, against counting vocabulary
which was flat (3.9% vs 6.0%). So it is a genuine positive prior for the identified evidence. It is
NOT a filter and is not used as one: only 33 records in the whole frame carry it, and 94% of arm-2's
own neighbourhood carries none. A bonus that fires on 0.4% of records cannot demote anything.

DEMOTION WEIGHTS COME FROM A4's MEASUREMENTS AND ARE DELIBERATELY UNEVEN:

  * CLINICAL (Wall 1) takes the heaviest weight in the chapter. `186_` counted its on-estimand rate
    over the entire 204,210-record cloud at 0.1% under a strict vocabulary. Demoting it costs
    essentially nothing measurable — and unlike A.24's geochronology, it shares the topic axis
    completely, so nothing else will keep it out of the head.
  * SAFETY (Wall 2) takes a heavy weight too: A4's safety seed cloud ran 33% loose outcome and **0%
    strict**, i.e. it carries the words "birth" and "fertility" constantly and a population quantity
    never.
  * ONCOLOGY (Wall 5) takes a MODERATE weight, and the terms are the ONCOLOGICAL INDICATION only —
    never "fertility preservation" itself. A4 measured the preservation population at 76% oncological,
    5% elective, 17% neither; v5's claim names ELECTIVE egg freezing, so penalising the preservation
    vocabulary as such would demote the cell the registry entry asks about.
  * MULTIPLES (Wall 3) takes a MILD weight and deliberately so. It is A.12's territory by outcome,
    not by topic, and Buckles 2012 is an include for BOTH chapters. A heavy penalty would demote a
    record two chapters need in order to enforce a boundary that is a routing decision, not an
    exclusion.
  * ETIOLOGY (Wall 4) takes a moderate weight: it is a different question (why infertility rose) in
    the same vocabulary.

A THIRD OF THE FRAME HAS NO ABSTRACT AND THAT IS RECORDED PER RECORD, NOT AVERAGED AWAY. 2,524
records (33%) carry a title only. A title-only record cannot be screened on content at anything like
the power of one with an abstract, and its `NOT_RELEVANT` means "not visible" rather than "not
relevant". The flag travels with the record so the screen can bucket it as `INSUFFICIENT_INFO`
instead of silently converting missing metadata into a negative verdict — the refusals-read-as-zeros
failure wearing its third costume.

Output: literature/search-logs/{slug}-d1-ranked.json
        literature/search-logs/{slug}-screen-worklist.json
        literature/search-logs/{slug}-d1-log.md
"""
import json, os, re

SLUG = "art-access-fertility-recovery"
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
LOGS = os.path.join(ROOT, "literature", "search-logs")
TIER_A = os.path.join(LOGS, f"{SLUG}-tier-a.json")
TIER_B = os.path.join(LOGS, f"{SLUG}-tier-b-frame.json")
OUT_RANK = os.path.join(LOGS, f"{SLUG}-d1-ranked.json")
OUT_WORK = os.path.join(LOGS, f"{SLUG}-screen-worklist.json")
OUT_LOG = os.path.join(LOGS, f"{SLUG}-d1-log.md")

SCREEN_BUDGET = 800     # in-session screening throughput, NOT a cost limit — see the log's budget note

# --- ARM 2's signature: the ACCESS exposure. High weights on policy instruments that cannot mean
# --- anything else; low weights on words that have an ordinary clinical sense ("eligibility" is as
# --- likely to be trial eligibility as insurance eligibility).
ACCESS_CORE = {
    "insurance mandate": 9, "insurance mandates": 9, "mandated coverage": 9, "coverage mandate": 9,
    "state mandate": 8, "infertility insurance": 9, "insurance coverage": 7, "publicly funded": 7,
    "public funding": 7, "reimbursement": 6, "subsidy": 6, "subsidised": 6, "subsidized": 6,
    "out-of-pocket": 6, "cost sharing": 6, "co-payment": 5, "copayment": 5, "affordability": 5,
    "access to treatment": 5, "financial barrier": 6, "ability to pay": 5, "eligibility": 3,
}

# --- ARM 1's signature: COUNTING language. What a paper says when it tabulates a share rather than
# --- estimating a response. "Contribution of" scores high because it is this literature's own phrase
# --- for the quantity (Sobotka 2008, Lazzari 2021 both use it in the title).
COUNT_CORE = {
    "share of births": 9, "proportion of births": 9, "percentage of all births": 9,
    "contribution to": 7, "contribution of": 7, "accounted for": 5, "attributable to": 6,
    "registry data": 6, "register-based": 6, "population-based": 5, "nationwide": 5,
    "surveillance": 4, "annual report": 3, "national registry": 7, "cross-national": 5,
}

# --- THE OUTCOME AXIS. Loose by design — the frame is drawn loose because the strict vocabulary
# --- loses the canon (A4: strict reached 4 of 12 anchors and 2 primary-cell records out of 7,589).
# --- The WEIGHTS carry the strictness instead: population quantities score 8-9, ambiguous words that
# --- also carry a per-cycle clinical sense score 2-3. That puts precision in the ranking rather than
# --- in the frame, which is the whole architecture of this chapter's search.
POPFERT_CORE = {
    "total fertility rate": 9, "total fertility": 9, "completed fertility": 9,
    "cohort fertility": 9, "crude birth rate": 9, "parity transition": 9, "period fertility": 9,
    "fertility decline": 8, "demographic transition": 8, "population fertility": 9,
    "childlessness": 7, "number of children": 7, "childbearing": 6, "family size": 6,
    "birth rates": 4, "birth rate": 4, "fertility rate": 5, "childless": 6,
    "transition to parenthood": 6, "fertility": 2, "births": 2, "parenthood": 3, "fecundity": 3,
}

# --- IDENTIFICATION. A4-measured 4x positive prior for arm 2. A bonus, never a filter: it fires on
# --- 33 records in 7,589, so it can lift the identified evidence and cannot demote anything.
IDENT_SIG = {
    "difference-in-differences": 8, "difference in differences": 8, "natural experiment": 8,
    "quasi-experimental": 7, "instrumental variable": 7, "regression discontinuity": 8,
    "event study": 6, "exogenous variation": 7, "causal effect": 5, "policy reform": 5,
    "staggered": 5, "control group": 3, "counterfactual": 5,
}

# --- Demotions. Ranking signals only; nothing is removed from the frame. Weights from A4/186_. ---
# WALL 1, the heaviest in the chapter: 0.1% on-estimand over the whole 204,210-record cloud, and it
# shares the topic axis completely, so nothing else keeps it out of the head.
CLINICAL = {
    "live birth rate per cycle": 12, "cumulative live birth": 12, "clinical pregnancy rate": 12,
    "implantation rate": 12, "ovarian stimulation": 11, "embryo culture": 11, "blastocyst": 11,
    "luteal phase": 11, "gonadotropin": 10, "oocyte retrieval": 11, "per cycle": 10,
    "per transfer": 10, "endometrial": 10, "follicular": 9, "sperm motility": 9, "randomized": 4,
    "randomised": 4, "protocol": 3, "antagonist": 8, "agonist": 8, "vitrification": 9,
}
# WALL 2. A4: 33% loose outcome, 0% strict — it says "birth" constantly and never a population
# quantity.
SAFETY = {
    "birth defect": 11, "congenital": 11, "neonatal outcome": 11, "preterm": 10, "birth weight": 10,
    "birthweight": 10, "imprinting disorder": 11, "perinatal": 10, "ovarian hyperstimulation": 11,
    "ohss": 11, "maternal morbidity": 10, "stillbirth": 9, "gestational age": 9, "nicu": 10,
    "child development": 7, "cerebral palsy": 10,
}
# WALL 5, MODERATE, and the terms are the ONCOLOGICAL INDICATION only. "fertility preservation" is
# deliberately absent: v5's claim names ELECTIVE egg freezing, and penalising the preservation
# vocabulary as such would demote the cell the registry entry asks about.
ONCO = {
    "cancer": 8, "oncolog": 8, "chemotherap": 9, "radiotherap": 9, "gonadotoxic": 9,
    "malignan": 8, "leukemia": 8, "leukaemia": 8, "lymphoma": 8, "survivorship": 7,
    "tumour": 7, "tumor": 7, "breast cancer": 8,
}
# WALL 3, MILD AND DELIBERATELY SO. A.12's by OUTCOME, not by topic. Buckles 2012 is an include for
# both chapters; a heavy penalty would demote a record two chapters need in order to enforce a
# boundary that is a routing decision rather than an exclusion.
MULTIPLES = {
    "multiple birth": 4, "multiple births": 4, "twinning": 4, "multiple pregnancy": 4,
    "higher order multiple": 4, "single embryo transfer": 3, "multiple gestation": 4,
    "triplet": 4, "twin pregnancy": 4,
}
# WALL 4, MODERATE. A different question in the same vocabulary.
ETIOLOGY = {
    "prevalence of infertility": 8, "infertility prevalence": 8, "sperm count": 8,
    "semen quality": 8, "endocrine disrupt": 8, "etiology of infertility": 8,
    "aetiology of infertility": 8, "causes of infertility": 7, "varicocele": 8, "endometriosis": 6,
    "polycystic": 6,
}
# Reported, never scored: the topic axis. Retained so the log can show it is ambient.
ART_TERMS = ("ivf", "icsi", "assisted reproduct", "in vitro fertili", "intracytoplasmic",
             "fertility treatment", "infertility treatment", "fertility clinic", "embryo transfer",
             "ovulation induction", "assisted conception")
PRESERVE_TERMS = ("oocyte cryopreservation", "egg freezing", "fertility preservation",
                  "oocyte vitrification", "ovarian tissue cryopreservation")
ELECTIVE_TERMS = ("elective", "social freezing", "planned oocyte", "non-medical",
                  "age-related fertility decline", "employer", "workplace")


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

    ARM1_CELLS = {"P3_ART_SHARE", "P4_POSTPONEMENT_RECOVERY"}
    ARM2_CELLS = {"P1_MANDATE"}
    arm1_seeds = {a["openalex_id"] for a in tier_a if a["provisional_cell"] in ARM1_CELLS}
    arm2_seeds = {a["openalex_id"] for a in tier_a if a["provisional_cell"] in ARM2_CELLS}
    primary_seeds = arm1_seeds | arm2_seeds
    decoy_seeds = {a["openalex_id"] for a in tier_a
                   if a["provisional_cell"].startswith(("OFF_", "ROUTE_"))}

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
        s_acc, h_acc = score_terms(blob, ACCESS_CORE)
        s_cnt, h_cnt = score_terms(blob, COUNT_CORE)
        s_pop, h_pop = score_terms(blob, POPFERT_CORE)
        s_id, h_id = score_terms(blob, IDENT_SIG)
        s_clin, h_clin = score_terms(blob, CLINICAL)
        s_safe, h_safe = score_terms(blob, SAFETY)
        s_onc, h_onc = score_terms(blob, ONCO)
        s_mul, h_mul = score_terms(blob, MULTIPLES)
        s_eti, h_eti = score_terms(blob, ETIOLOGY)

        t_acc, _ = score_terms(title_blob, ACCESS_CORE)
        t_cnt, _ = score_terms(title_blob, COUNT_CORE)
        t_pop, _ = score_terms(title_blob, POPFERT_CORE)

        h_art = [t for t in ART_TERMS if t in blob]
        preserve = any(t in blob for t in PRESERVE_TERMS)
        elective = preserve and any(t in blob for t in ELECTIVE_TERMS)
        onco_named = preserve and bool(h_onc)
        # Wall 5's unenforceable residue, per record: a preservation paper naming NEITHER indication.
        w5_residue = preserve and not elective and not onco_named

        has_outcome = bool(h_pop)
        arm2_shape = bool(h_acc) and has_outcome
        arm1_shape = bool(h_cnt) and has_outcome
        seeds = set(r["seed_ids"])
        from_arm1_seed = bool(seeds & arm1_seeds)
        from_arm2_seed = bool(seeds & arm2_seeds)
        from_primary = bool(seeds & primary_seeds)
        decoy_only = bool(seeds) and seeds <= decoy_seeds
        no_abstract = not bool(r.get("abstract"))

        # The ART axis contributes ZERO. It is ambient in this frame by construction and scoring it
        # would rank the clinical cloud alongside the primary cell and call that precision.
        score = (s_acc + s_cnt + s_pop + t_acc + t_cnt + t_pop
                 + (16 if arm2_shape else 0)          # the identified cell
                 + (14 if arm1_shape else 0)          # the accounting cell
                 + s_id                               # A4's 4x prior, bonus only
                 + (8 if elective else 0)             # PI call 2's cell, ~46 records in the frame
                 + 6 * (r["n_seeds"] - 1)
                 + (10 if from_primary else 0)
                 + (4 if "backward" in r["channels"] else 0)
                 - s_clin - s_safe - s_onc - s_mul - s_eti)

        keep = ("id", "doi", "title", "year", "cited_by_count", "type", "venue", "authors",
                "abstract", "seed_ids", "n_seeds", "channels")
        r2 = {k: r.get(k) for k in keep}
        r2.update(d1_score=score, arm2_shape=arm2_shape, arm1_shape=arm1_shape,
                  has_outcome=has_outcome, preserve=preserve, elective=elective,
                  w5_residue=w5_residue, no_abstract=no_abstract,
                  access_hits=h_acc[:6], count_hits=h_cnt[:6], popfert_hits=h_pop[:6],
                  ident_hits=h_id[:4], art_hits=h_art[:4], clinical_hits=h_clin[:4],
                  safety_hits=h_safe[:4], onco_hits=h_onc[:3], multiples_hits=h_mul[:3],
                  etiology_hits=h_eti[:3],
                  from_arm1_seed=from_arm1_seed, from_arm2_seed=from_arm2_seed,
                  from_primary_seed=from_primary, decoy_only=decoy_only,
                  version_duplicates=r.get("version_duplicates"))
        scored.append(r2)

    scored.sort(key=lambda x: (-x["d1_score"], -(x["cited_by_count"] or 0)))
    for i, r in enumerate(scored):
        r["d1_rank"] = i + 1
    json.dump(scored, open(OUT_RANK, "w"), indent=2)

    # ---------------- worklist: budget slice + four bypasses ----------------
    top = scored[:SCREEN_BUDGET]
    top_ids = {r["id"] for r in top}

    # BYPASS 1 — ARM 2, the identified cell. Every record carrying an access exposure and an outcome
    # is read wherever it ranks. This is the chapter's only identified evidence and it is 148 records
    # in 7,589; a budget cutoff is exactly the wrong instrument for a population that small.
    bypass_arm2 = [r for r in scored[SCREEN_BUDGET:] if r["arm2_shape"] and r["id"] not in top_ids]

    # BYPASS 2 — ARM 1, the accounting cell. Same argument, and it is the arm that produces the
    # chapter's headline number.
    seen = top_ids | {r["id"] for r in bypass_arm2}
    bypass_arm1 = [r for r in scored[SCREEN_BUDGET:] if r["arm1_shape"] and r["id"] not in seen]

    # BYPASS 3 — THE ELECTIVE PRESERVATION CELL, which is PI call 2's. A4 counted ~46 records naming
    # an elective indication in the whole frame. If that cell is read in full and comes back empty,
    # the chapter can report it as a finding; if it is left to a budget cutoff, an empty cell and an
    # unread cell produce identical evidence and mean opposite things (B.6's rule).
    seen |= {r["id"] for r in bypass_arm1}
    bypass_elective = [r for r in scored[SCREEN_BUDGET:] if r["elective"] and r["id"] not in seen]

    # BYPASS 4 — WALL 5's RESIDUE. A4 measured 152 preservation records naming NEITHER indication.
    # They are the reason the wall needs an INSUFFICIENT_INFO bucket, and they cannot be routed
    # without being read. Restricted to those carrying an outcome, since a preservation paper with no
    # population outcome is out on Wall 5 whichever indication it turns out to have.
    seen |= {r["id"] for r in bypass_elective}
    bypass_w5 = [r for r in scored[SCREEN_BUDGET:]
                 if r["w5_residue"] and r["has_outcome"] and r["id"] not in seen]

    worklist = ([dict(r, worklist_reason="budget_slice") for r in top]
                + [dict(r, worklist_reason="bypass_arm2_identified") for r in bypass_arm2]
                + [dict(r, worklist_reason="bypass_arm1_accounting") for r in bypass_arm1]
                + [dict(r, worklist_reason="bypass_elective_preservation") for r in bypass_elective]
                + [dict(r, worklist_reason="bypass_wall5_residue") for r in bypass_w5])
    json.dump(worklist, open(OUT_WORK, "w"), indent=2)

    n = len(scored)
    pc = lambda k: f"{k / max(n, 1):.1%}"
    n_arm2 = sum(1 for r in scored if r["arm2_shape"])
    n_arm1 = sum(1 for r in scored if r["arm1_shape"])
    n_elect = sum(1 for r in scored if r["elective"])
    n_w5 = sum(1 for r in scored if r["w5_residue"])
    n_noabs = sum(1 for r in scored if r["no_abstract"])
    n_art = sum(1 for r in scored if r["art_hits"])
    n_ident = sum(1 for r in scored if r["ident_hits"])
    cut = top[-1]["d1_score"] if top else 0

    L = [f"# D1 deterministic ranking — {SLUG} (A.17)", "",
         f"**{len(tier_b):,} Tier-B records in, {dupes:,} version duplicates collapsed on normalized "
         f"title, {n:,} ranked.** Nothing is deleted: every record keeps its score, rank and hit "
         "lists, so the cutoff can be re-cut without re-running retrieval.", "",
         "## The exposure axis is ambient and is not scored", "",
         f"Every prior chapter scored an exposure axis against an outcome axis and let the cross-axis "
         f"AND do the work. A.17 cannot. The frame was pulled entirely from ART seeds, so ART "
         f"vocabulary is everywhere: **{n_art:,} records ({pc(n_art)}) name it explicitly** and the "
         "rest are ART-adjacent by construction. Scoring it would rank the 204,210-record clinical "
         "cloud alongside the primary cell and call the result precision. `art_hits` is retained on "
         "every record for reporting and contributes zero to the score.", "",
         "## What discriminates instead: two arm signatures, scored apart", "",
         "| signature | definition | records | share |", "|---|---|---|---|",
         f"| **ARM 2 (identified)** | ACCESS exposure x population outcome | {n_arm2:,} | {pc(n_arm2)} |",
         f"| **ARM 1 (accounting)** | COUNTING language x population outcome | {n_arm1:,} | {pc(n_arm1)} |",
         f"| Identification language | the A4-measured 4x prior for arm 2 | {n_ident:,} | {pc(n_ident)} |",
         f"| Elective preservation | PI call 2's cell | {n_elect:,} | {pc(n_elect)} |",
         f"| Wall 5 residue | preservation naming NEITHER indication | {n_w5:,} | {pc(n_w5)} |", "",
         "The two arm signatures are scored separately and equally and their hits are kept apart on "
         "every record. Merging them would produce a ranker that cannot distinguish a study "
         "estimating a policy response from a report tabulating a share — the distinction the whole "
         "chapter turns on.", "",
         "**Identification language is a bonus and never a filter.** It fires on "
         f"{n_ident:,} records in {n:,} ({pc(n_ident)}), so it can lift the identified evidence and "
         "is arithmetically incapable of demoting anything. A4 measured it at 1.4% in arm-1 "
         "neighbourhoods against 5.6% in arm-2 ones; that is a real prior and a thin one, and it is "
         "used accordingly.", "",
         "## A third of the frame has no abstract", "",
         f"**{n_noabs:,} records ({pc(n_noabs)}) carry a title only.** A title-only record cannot be "
         "screened on content at anything like the power of one with an abstract, and its "
         "`NOT_RELEVANT` would mean *not visible*, not *not relevant*. The `no_abstract` flag travels "
         "with every record so the screen buckets these as `INSUFFICIENT_INFO` rather than silently "
         "converting missing metadata into a negative verdict.", "",
         "## Worklist", "",
         f"**Budget slice: {len(top):,}** (score cutoff {cut}). Plus four bypasses, each carrying "
         "records read *wherever they rank*:", "",
         "| bypass | rationale | n |", "|---|---|---|",
         f"| `bypass_arm2_identified` | the chapter's only identified evidence, {n_arm2:,} records in "
         f"{n:,} — a budget cutoff is the wrong instrument for a population that small | "
         f"{len(bypass_arm2):,} |",
         f"| `bypass_arm1_accounting` | the arm that produces the headline number | {len(bypass_arm1):,} |",
         f"| `bypass_elective_preservation` | PI call 2's cell; an empty cell and an unread cell are "
         f"identical evidence and opposite conclusions | {len(bypass_elective):,} |",
         f"| `bypass_wall5_residue` | the records that cannot be routed without being read | "
         f"{len(bypass_w5):,} |",
         f"| **total worklist** | | **{len(worklist):,}** |", "",
         "**On the budget.** The 800-record slice is an in-session SCREENING-THROUGHPUT limit, not a "
         "cost limit, and the distinction matters because the two point in opposite directions. "
         f"Screening the entire {n:,}-record frame would cost single-digit dollars batched — the "
         "standing lesson is that screen cost has never been this project's binding constraint. What "
         "bounds this run is that verdicts are produced by reading batches in-session, and "
         f"{n:,} records is roughly 127 batches. **The bypasses are sized so that the budget decides "
         "only the tail: every record in either arm's candidate cell is read regardless of rank.** "
         "If a batch API key is available, the right move is to drop the slice and screen the frame "
         "entire; the ranking is retained precisely so that can be done without re-running anything "
         "upstream.", ""]

    if dupe_examples:
        L += ["## Version duplicates collapsed (examples)", "",
              "| title | kept DOI | dropped DOI | kept cites | dropped cites |", "|---|---|---|---|---|"]
        for t, d1, d2, c1, c2 in dupe_examples:
            L.append(f"| {t} | `{d1}` | `{d2}` | {c1} | {c2} |")
        L += [""]

    L += ["## Top 25 by D1 score", "",
          "| rank | score | arm | year | title | venue |", "|---|---|---|---|---|---|"]
    for r in scored[:25]:
        arm = ("**2**" if r["arm2_shape"] else "") + ("**1**" if r["arm1_shape"] else "")
        L.append(f"| {r['d1_rank']} | {r['d1_score']} | {arm or '—'} | {r.get('year')} | "
                 f"{r['title'][:74].replace('|', '/')} | {(r.get('venue') or '')[:30].replace('|', '/')} |")
    open(OUT_LOG, "w").write("\n".join(L) + "\n")

    print(f"ranked={n} (dupes collapsed={dupes})  arm2={n_arm2} arm1={n_arm1} "
          f"elective={n_elect} w5_residue={n_w5} no_abstract={n_noabs}")
    print(f"worklist={len(worklist)} = {len(top)} slice + {len(bypass_arm2)} arm2 + "
          f"{len(bypass_arm1)} arm1 + {len(bypass_elective)} elective + {len(bypass_w5)} w5")
    print(f"-> {os.path.relpath(OUT_WORK, ROOT)}")
    print(f"-> {os.path.relpath(OUT_LOG, ROOT)}")


if __name__ == "__main__":
    main()
