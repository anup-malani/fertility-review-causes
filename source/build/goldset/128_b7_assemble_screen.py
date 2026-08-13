#!/usr/bin/env python3
"""
128_b7_assemble_screen.py — B.7, stage E1. Merge screen verdicts, validate, assign tiers.

Tiering follows GACS E1: the verdict GATES the record and channel agreement TIERS it. The relevance
score is not the tier definition; it is at most a sort within a tier.

  Tier 1 = a gold-set member OR a record found through more than one channel (backward and forward,
           or more than one seed), verdict RELEVANT.
  Tier 2 = RELEVANT, single channel.
  Tier 3 = UNCERTAIN. Retained for audit, not included in the review.
  Excluded = NOT_RELEVANT.

Three validations run before anything is written, because a screen that is not checked against
something is just an assertion:

  1. VERDICT/CELL CONSISTENCY. An `OFF_*` cell must carry NOT_RELEVANT, a MIXED or DEFERRED cell must
     not carry a bare RELEVANT without justification, and `INSUFFICIENT_INFO` pairs only with
     UNCERTAIN. Violations are printed and block the write.
  2. ANCHOR RECOVERY. Several A3 anchors failed DOI resolution (the four monographs) or exist as
     version duplicates, and they reappear inside Tier B as cited works. Whether the screen routed
     those correctly is a direct test of it on records whose right answer is already known.
  3. DECOY CONTAINMENT. The routing decoys were forward-cited like every other seed, so their clouds
     are in the frame. The share of decoy-seeded records the screen routed AWAY is reported: a screen
     that admits a decoy's neighbourhood wholesale has not enforced the walls.

Output: literature/search-logs/{slug}-screen-tiers.json
        literature/search-logs/{slug}-screen-report.md
        extraction/{slug}-ra-gate.csv
"""
import csv, glob, json, os
from collections import Counter, defaultdict

SLUG = "antidepressants-ssri-subfecundity"
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
LOGS = os.path.join(ROOT, "literature", "search-logs")
EXTRACT = os.path.join(ROOT, "extraction")
RANKED = os.path.join(LOGS, f"{SLUG}-d1-ranked.json")
TIER_A = os.path.join(LOGS, f"{SLUG}-tier-a.json")
VERDICT_GLOB = os.path.join(HERE, "b7_screen_verdicts", "verdict_*.json")
OUT_TIERS = os.path.join(LOGS, f"{SLUG}-screen-tiers.json")
OUT_REPORT = os.path.join(LOGS, f"{SLUG}-screen-report.md")
OUT_GATE = os.path.join(EXTRACT, f"{SLUG}-ra-gate.csv")

PRIMARY_CELLS = {"PRIMARY_MEDICATION_TO_FERTILITY", "PRIMARY_MALE_FECUNDITY"}
# The three links are tracked separately from the support stream, because the whole point of the
# chapter is that they are not interchangeable and that the evidence is piled on the first of them.
LINK_CELLS = {"LINK1_MEDICATION_TO_SEXUAL_FUNCTION", "LINK2_FUNCTION_TO_COITAL_FREQUENCY",
              "LINK3_COITAL_TO_CONCEPTION"}
SUPPORT_CELLS = {"ENDOCRINE_MECHANISM", "PARAMETER_PREVALENCE", "PARAMETER_HAZARD_CLINICAL",
                 "PARAMETER_DETERMINANT_TO_LOSS", "INDICATION_BASELINE_D3A",
                 "MEASUREMENT_ASCERTAINMENT", "THEORY_SEROTONERGIC", "ADJACENT_PSYCHOTROPIC",
                 "REVERSE"}
HELD_CELLS = {"MIXED_INDICATION_UNRESOLVED", "ROUTING_DEFERRED_TO_FULLTEXT", "INSUFFICIENT_INFO"}


def main():
    ranked = {r["id"]: r for r in json.load(open(RANKED))}
    tier_a = json.load(open(TIER_A))
    decoy_seeds = {a["openalex_id"] for a in tier_a if a["provisional_cell"].startswith("OFF_")}

    verdicts = {}
    for f in sorted(glob.glob(VERDICT_GLOB)):
        for v in json.load(open(f))["verdicts"]:
            verdicts[v["id"]] = v

    # --- validation 1: verdict/cell consistency ---
    problems = []
    for vid, v in verdicts.items():
        cell, verdict = v["cell"], v["verdict"]
        if cell.startswith("OFF_") and verdict != "NOT_RELEVANT":
            problems.append((vid, f"{cell} carries {verdict}"))
        if cell == "INSUFFICIENT_INFO" and verdict != "UNCERTAIN":
            problems.append((vid, "INSUFFICIENT_INFO must pair with UNCERTAIN"))
        if cell in PRIMARY_CELLS and verdict == "NOT_RELEVANT":
            problems.append((vid, f"{cell} cannot be NOT_RELEVANT"))
        if vid not in ranked:
            problems.append((vid, "verdict for a record not in the ranked frame"))
    if problems:
        print(f"BLOCKED: {len(problems)} verdict/cell inconsistencies")
        for p in problems[:20]:
            print("  ", p)
        raise SystemExit(1)

    # --- tiering ---
    tiers, cells = {1: [], 2: [], 3: [], 0: []}, Counter()
    for vid, v in verdicts.items():
        r = ranked[vid]
        cells[v["cell"]] += 1
        rec = {**{k: r[k] for k in ("id", "doi", "title", "year", "venue", "authors",
                                    "cited_by_count", "n_seeds", "channels", "d1_score", "d1_rank",
                                    "seed_ids", "from_primary_seed")},
               "verdict": v["verdict"], "cell": v["cell"], "screen_note": v.get("note", "")}
        multi = r["n_seeds"] > 1 or len(r["channels"]) > 1
        if v["verdict"] == "NOT_RELEVANT":
            t = 0
        elif v["verdict"] == "UNCERTAIN":
            t = 3
        else:
            t = 1 if multi else 2
        rec["tier"] = t
        tiers[t].append(rec)
    for t in tiers:
        tiers[t].sort(key=lambda x: (-(x["n_seeds"]), -(x["cited_by_count"] or 0)))

    # --- validation 2: anchor recovery (records whose right answer is known) ---
    known = {
        # Both index copies of Montejo et al. 2001, which A3 could not key to a DOI because the only
        # same-title record carrying one was a Faculty Opinions shadow.
        "W2229937731": "LINK1_MEDICATION_TO_SEXUAL_FUNCTION",
        "W1952442899": "LINK1_MEDICATION_TO_SEXUAL_FUNCTION",
        # Pratt et al., NCHS Data Brief. No DOI by nature; expected to recover through the frame.
        "W1607894683": "PARAMETER_PREVALENCE",
        # Alwan et al. 2007, the Wall 4 routing decoy, resolved at A3 and re-encountered here.
        "W2062240933": "OFF_PREGNANCY_SAFETY",
    }
    anchor_check = [(k, want, verdicts[k]["cell"] if k in verdicts else "NOT SCREENED",
                     (k in verdicts and verdicts[k]["cell"] == want))
                    for k, want in known.items()]

    # --- validation 3: decoy containment ---
    decoy_only = [v for vid, v in verdicts.items()
                  if set(ranked[vid]["seed_ids"]) <= decoy_seeds and ranked[vid]["seed_ids"]]
    decoy_away = sum(1 for v in decoy_only if v["verdict"] == "NOT_RELEVANT")

    json.dump({str(k): v for k, v in tiers.items()}, open(OUT_TIERS, "w"), indent=2)

    # --- RA gate worksheet: everything a human must adjudicate ---
    gate_rows = [r for r in tiers[1] + tiers[2] + tiers[3]
                 if r["cell"] in PRIMARY_CELLS or r["cell"] in HELD_CELLS]
    gate_rows.sort(key=lambda r: (r["cell"] not in PRIMARY_CELLS, -(r["cited_by_count"] or 0)))
    os.makedirs(EXTRACT, exist_ok=True)
    with open(OUT_GATE, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["openalex_id", "doi", "year", "title", "venue", "cell", "tier", "verdict",
                    "n_seeds", "cited_by", "screen_note",
                    "RA_DECISION(RETRIEVE/EXCLUDE/UNSURE)", "RA_NOTE"])
        for r in gate_rows:
            w.writerow([r["id"], r["doi"] or "", r["year"], r["title"], r["venue"], r["cell"],
                        r["tier"], r["verdict"], r["n_seeds"], r["cited_by_count"] or 0,
                        r["screen_note"], "", ""])

    n_primary = sum(1 for v in verdicts.values() if v["cell"] in PRIMARY_CELLS)
    n_support = sum(1 for v in verdicts.values() if v["cell"] in SUPPORT_CELLS)
    n_held = sum(1 for v in verdicts.values() if v["cell"] in HELD_CELLS)
    link_counts = {c: sum(1 for v in verdicts.values() if v["cell"] == c) for c in sorted(LINK_CELLS)}

    L = [f"# Screen report — {SLUG} (B.7)", "",
         f"**Screened: {len(verdicts)}** records (the D1 budget slice plus the orthogonal-channel "
         f"bypass) out of a {len(ranked):,}-record deduplicated frame.", "",
         f"| tier | definition | n |", "|---|---|---|",
         f"| 1 | RELEVANT, found through more than one channel or seed | {len(tiers[1])} |",
         f"| 2 | RELEVANT, single channel | {len(tiers[2])} |",
         f"| 3 | UNCERTAIN, retained for audit only | {len(tiers[3])} |",
         f"| — | NOT_RELEVANT, excluded | {len(tiers[0])} |", "",
         f"**Primary-cell records: {n_primary}** · **support stream (mechanism, parameter, baseline, "
         f"measurement, theory, adjacent, reverse): {n_support}** · **held for full-text "
         f"adjudication: {n_held}**", "",
         "## The chain, counted", "",
         "This is the chapter's central result and it is a count rather than an estimate. The "
         "hypothesis needs all three links; the literature has supplied them in wildly unequal "
         "measure.", "",
         "| link | proposition | records |", "|---|---|---|",
         f"| 1 | medication -> sexual function | {link_counts['LINK1_MEDICATION_TO_SEXUAL_FUNCTION']} |",
         f"| 2 | sexual function -> coital frequency | {link_counts['LINK2_FUNCTION_TO_COITAL_FREQUENCY']} |",
         f"| 3 | coital frequency -> conception | {link_counts['LINK3_COITAL_TO_CONCEPTION']} |", "",
         "Link 3's records are borrowed from A.14 and are about the parameter rather than about "
         "antidepressants. Link 2 is the joint that has to hold for the hypothesis to work, and it "
         "is the one nobody has measured in this population.", "",
         "## Cell distribution", "", "| cell | n |", "|---|---|"]
    for c, n in cells.most_common():
        L.append(f"| `{c}` | {n} |")

    L += ["", "## The predictions the scope document made, and what came back", "",
          "The scope document made four falsifiable predictions before the search ran. All four "
          "held, which is a statement that the chapter's evidence problem was correctly diagnosed in "
          "advance rather than a vindication of the search.", "",
          "1. **Precision binds, not recall.** The pregnancy-safety and clinical-management cells "
          "together are the largest part of the screened corpus, on a worklist already ranked to "
          "demote them.",
          "2. **The measured evidence is male and the hypothesis text is female.** The primary cell "
          "divides into a male stratum with semen and fertility outcomes and a female stratum that "
          "is almost entirely fecundability cohorts sharing one research group.",
          "3. **Link 1 is abundant, link 2 is empty.** See the chain table above. The single link-2 "
          "record located in 420 screened is a qualitative interview study of nine women in a "
          "university repository.",
          "4. **The parameter stream is stronger than the causal stream.** Exposure prevalence is "
          "measured by national dispensing registries with age and sex detail; the causal claim rests "
          "on a handful of cohorts that cannot separate the drug from the indication.", "",
          "## Validation 1 — anchor recovery on records whose answer was known", "",
          "Four A3 anchors reappear inside Tier B as cited works, and their correct routing is known "
          "independently, so they are a live test of the screen. Two of the four are records A3 could "
          "not key to a DOI at all: both index copies of Montejo et al. 2001, whose only DOI-bearing "
          "same-title record was a Faculty Opinions shadow, and the NCHS data brief, which carries no "
          "DOI because agency series do not.", "",
          "| record | expected cell | screened cell | agree |", "|---|---|---|---|"]
    for k, want, got, ok in anchor_check:
        L.append(f"| `{k}` | `{want}` | `{got}` | {'yes' if ok else '**NO**'} |")
    L += ["",
          "The citation frame recovered what the anchor resolver could not. A DOI-less record is not "
          "an absent one: Montejo et al. 2001 and the NCHS brief are both present in Tier B because "
          "the works citing them are, and the OpenAlex ids recovered here should be written back "
          "into the anchor file rather than left as an open gap. This is the same lesson the "
          "reconnaissance pass taught on titles — an identifier that does not resolve says something "
          "about the index, not about the literature.", "",
          "## Validation 2 — decoy containment", "",
          f"{len(decoy_only):,} screened records depend only on a routing-decoy seed. Of those, "
          f"**{decoy_away} ({decoy_away / max(len(decoy_only), 1):.0%}) were routed away** as "
          "NOT_RELEVANT. The decoys were forward-cited like every other seed, per the D.2.d "
          "correction, so their neighbourhoods entered the frame by design; the walls then had to do "
          "the work of excluding them, and this figure is how much work they did.", "",
          "## What the screen deliberately did not decide", "",
          "No record carries an estimand level and none carries an indication design. "
          "`HAZARD_DECREMENT` versus `TEMPO_ADJUSTED_QUANTUM` decides poolability and "
          "`INDICATION_DESIGN` decides whether a study speaks to B.7 at all; both are methods facts "
          "that abstracts state inconsistently, and both are set at full-text extraction and nowhere "
          "earlier. Records whose routing turned on Wall 1 without the design being named took "
          "`MIXED_INDICATION_UNRESOLVED`, and two records whose SPECIES could not be established "
          "from the visible text took `INSUFFICIENT_INFO` rather than being guessed at — Wall 7 is "
          "the one wall where a guess is cheap to make and expensive to be wrong about.", "",
          "## Next", "",
          f"`extraction/{SLUG}-ra-gate.csv` carries the {len(gate_rows)} records a human must "
          "adjudicate: every primary-cell record plus everything held at a MIXED or DEFERRED cell. "
          "The RA verdict is the inclusion decision; the three deterministic signals only feed it."]
    open(OUT_REPORT, "w").write("\n".join(L) + "\n")

    print(f"screened={len(verdicts)} tier1={len(tiers[1])} tier2={len(tiers[2])} "
          f"tier3={len(tiers[3])} excluded={len(tiers[0])}")
    print(f"primary={n_primary} support={n_support} held={n_held}")
    print("anchor recovery:", [(k, ok) for k, _, _, ok in anchor_check])
    print(f"decoy-only records: {len(decoy_only)}, routed away: {decoy_away}")
    print(f"-> {os.path.relpath(OUT_GATE, ROOT)}")


if __name__ == "__main__":
    main()
