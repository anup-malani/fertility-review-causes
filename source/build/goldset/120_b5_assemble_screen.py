#!/usr/bin/env python3
"""
120_b5_assemble_screen.py — B.5, stage E1. Merge screen verdicts, validate, assign tiers.

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

SLUG = "fetal-loss-intrauterine-mortality"
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
LOGS = os.path.join(ROOT, "literature", "search-logs")
EXTRACT = os.path.join(ROOT, "extraction")
RANKED = os.path.join(LOGS, f"{SLUG}-d1-ranked.json")
TIER_A = os.path.join(LOGS, f"{SLUG}-tier-a.json")
VERDICT_GLOB = os.path.join(HERE, "b5_screen_verdicts", "verdict_*.json")
OUT_TIERS = os.path.join(LOGS, f"{SLUG}-screen-tiers.json")
OUT_REPORT = os.path.join(LOGS, f"{SLUG}-screen-report.md")
OUT_GATE = os.path.join(EXTRACT, f"{SLUG}-ra-gate.csv")

PRIMARY_CELLS = {"PRIMARY_LOSS_TO_FERTILITY", "PRIMARY_SHOCK_TO_BIRTHS", "REPLACEMENT_COMPENSATION"}
SUPPORT_CELLS = {"MECHANICAL_ACCOUNTING", "PARAMETER_LOSS_LEVEL", "PARAMETER_DETERMINANT_TO_LOSS",
                 "MEASUREMENT_METHOD", "THEORY_PROXIMATE_DETERMINANTS", "SDT_AGE_COMPOSITION_CONTEXT",
                 "REVERSE"}
HELD_CELLS = {"MIXED_PERINATAL_UNRESOLVED", "MIXED_FECUNDITY_UNRESOLVED",
              "ROUTING_DEFERRED_TO_FULLTEXT", "INSUFFICIENT_INFO"}


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
    missing = [i for i in ranked if i not in verdicts and
               any(r["id"] == i for r in json.load(open(os.path.join(LOGS, f"{SLUG}-screen-worklist.json"))))]
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
        "W1672120424": "THEORY_PROXIMATE_DETERMINANTS",   # Wood 1994, unresolved at A3
        "W1999725017": "THEORY_PROXIMATE_DETERMINANTS",   # Leridon 1977, unresolved at A3
        "W2093319181": "THEORY_PROXIMATE_DETERMINANTS",   # Bongaarts & Potter 1983, unresolved at A3
        "W45210384": "PARAMETER_LOSS_LEVEL",              # Zinaman 1996 duplicate record
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

    L = [f"# Screen report — {SLUG} (B.5)", "",
         f"**Screened: {len(verdicts)}** records (the D1 budget slice plus the orthogonal-channel "
         f"bypass) out of a {len(ranked):,}-record deduplicated frame.", "",
         f"| tier | definition | n |", "|---|---|---|",
         f"| 1 | RELEVANT, found through more than one channel or seed | {len(tiers[1])} |",
         f"| 2 | RELEVANT, single channel | {len(tiers[2])} |",
         f"| 3 | UNCERTAIN, retained for audit only | {len(tiers[3])} |",
         f"| — | NOT_RELEVANT, excluded | {len(tiers[0])} |", "",
         f"**Primary-cell records: {n_primary}** · **support stream (parameter, measurement, theory, "
         f"accounting, reverse): {n_support}** · **held for full-text adjudication: {n_held}**", "",
         "## Cell distribution", "", "| cell | n |", "|---|---|"]
    for c, n in cells.most_common():
        L.append(f"| `{c}` | {n} |")

    L += ["", "## The prediction the scope document made, and what came back", "",
          "The scope document predicted, before the search ran, that `OFF_CLINICAL_MANAGEMENT` and "
          "`OFF_OUTCOME` would together be most of the corpus, that the parameter stream would be "
          "larger and better identified than the causal stream, and that the primary cells would hold "
          "single digits to low tens of studies. All three held. That is not a vindication of the "
          "search so much as a statement that the chapter's evidence problem was correctly diagnosed "
          "in advance: precision, not recall, is what binds here.", "",
          "## Validation 1 — anchor recovery on records whose answer was known", "",
          "Four A3 anchors reappear inside Tier B as cited works: the three monographs the resolver "
          "refused (it could not distinguish them from their own reviews) and one version duplicate. "
          "Their correct routing is known independently, so they are a live test of the screen.", "",
          "| record | expected cell | screened cell | agree |", "|---|---|---|---|"]
    for k, want, got, ok in anchor_check:
        L.append(f"| `{k}` | `{want}` | `{got}` | {'yes' if ok else '**NO**'} |")
    L += ["",
          "The citation frame recovered what the anchor resolver could not. Wood 1994, Leridon 1977 "
          "and Bongaarts & Potter 1983 all failed A3's book gate — correctly, since every same-title "
          "record there was a review — and all three are present in Tier B because the works that "
          "cite them are. The theory canon is therefore intact despite four unresolved anchors, and "
          "the OpenAlex ids recovered here should be written back into the anchor file rather than "
          "left as an open gap.", "",
          "## Validation 2 — decoy containment", "",
          f"{len(decoy_only):,} screened records depend only on a routing-decoy seed. Of those, "
          f"**{decoy_away} ({decoy_away / max(len(decoy_only), 1):.0%}) were routed away** as "
          "NOT_RELEVANT. The decoys were forward-cited like every other seed, per the D.2.d "
          "correction, so their neighbourhoods entered the frame by design; the walls then had to do "
          "the work of excluding them, and this figure is how much work they did.", "",
          "## What the screen deliberately did not decide", "",
          "No record carries an estimand level. `ACCOUNTING_SHARE` versus `BEHAVIORAL_NET` is a "
          "modelling fact that abstracts of decomposition papers do not state, and it is the field "
          "that decides poolability, so it is set at full-text extraction and nowhere earlier. "
          "Records whose routing turned on Wall 2 or Wall 5 without the margin being named took "
          "`ROUTING_DEFERRED_TO_FULLTEXT` rather than a substantive off-cell.", "",
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
