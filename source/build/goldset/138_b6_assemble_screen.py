#!/usr/bin/env python3
"""
138_b6_assemble_screen.py — B.6, stage E1. Merge screen verdicts, validate, assign tiers.

Inherits `128_b7_assemble_screen.py`. Tiering follows GACS E1: the verdict GATES the record and
channel agreement TIERS it.

  Tier 1 = RELEVANT and found through more than one channel or seed.
  Tier 2 = RELEVANT, single channel.
  Tier 3 = UNCERTAIN. Retained for audit, not included in the review.
  Excluded = NOT_RELEVANT.

Five validations run before anything is written, because a screen that is not checked against
something is just an assertion. Three are inherited; two are new for B.6.

  1. VERDICT/CELL CONSISTENCY. An `OFF_*` cell must carry NOT_RELEVANT, `INSUFFICIENT_INFO` pairs
     only with UNCERTAIN, a PRIMARY cell cannot be NOT_RELEVANT.
  2. ANCHOR RECOVERY. Several A3 anchors reappear inside Tier B as cited works, sometimes as
     duplicate or correspondence records. Whether the screen routed them correctly is a direct test
     on records whose right answer is already known.
  3. DECOY CONTAINMENT. The routing decoys were forward-cited like every other seed, so their clouds
     are in the frame. The share of decoy-seeded records the screen routed AWAY is reported.
  4. CHEMICAL-FAMILY AGREEMENT (new). D1 assigned `chemical_family` deterministically from the named
     compound; the screener assigned it independently, without seeing D1's tag. Disagreement is not
     an error to suppress — it flags records where the title names one family and the study measures
     another, which is the shape of a Wall 1 mixture case a term-match cannot see. The rate is the
     honest measure of how well the split the chapter runs on can actually be operationalised.
  5. SHADOW-CLUSTER DETECTION (new). The A3 shadow gate protects the ANCHOR set. Nothing protected
     Tier B, and the screen found that open-peer-review journals mint a separately-DOI'd record per
     referee report: one eLife paper occupies six rows in this frame (article, duplicate, Author
     Response, three Reviewer Public Reviews) and one PeerJ review occupies four. This validation
     re-runs the qualifier test over every screened title and reports what the D1 title-collapse
     missed, so the extraction stage inherits a count rather than a surprise.

Output: literature/search-logs/{slug}-screen-tiers.json
        literature/search-logs/{slug}-screen-report.md
        extraction/{slug}-ra-gate.csv
"""
import csv, glob, json, os, re
from collections import Counter

SLUG = "microplastics-pfas-reproductive"
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
LOGS = os.path.join(ROOT, "literature", "search-logs")
EXTRACT = os.path.join(ROOT, "extraction")
RANKED = os.path.join(LOGS, f"{SLUG}-d1-ranked.json")
TIER_A = os.path.join(LOGS, f"{SLUG}-tier-a.json")
VERDICT_GLOB = os.path.join(HERE, "b6_screen_verdicts", "verdict_*.json")
OUT_TIERS = os.path.join(LOGS, f"{SLUG}-screen-tiers.json")
OUT_REPORT = os.path.join(LOGS, f"{SLUG}-screen-report.md")
OUT_GATE = os.path.join(EXTRACT, f"{SLUG}-ra-gate.csv")

PRIMARY_CELLS = {"PRIMARY_EXPOSURE_TO_FERTILITY", "PRIMARY_MALE_FECUNDITY", "PRIMARY_HIGH_EXPOSURE"}
# Inputs to fertility rather than fertility quantities. Kept separate from PRIMARY because conflating
# them is how a semen-parameter literature gets read as a fertility literature.
INPUT_CELLS = {"SEMEN_PARAMETER", "OVARIAN_PARAMETER"}
SUPPORT_CELLS = {"DETECTION_TISSUE", "MECHANISM_INVITRO", "PARAMETER_EXPOSURE",
                 "PARAMETER_PHARMACOKINETIC", "PARAMETER_DETERMINANT_TO_LOSS", "MEASUREMENT_METHOD",
                 "OUTCOME_TREND_UNATTRIBUTED", "REVERSE"}
HELD_CELLS = {"MIXTURE_UNSEPARABLE", "ROUTING_DEFERRED_TO_FULLTEXT", "INSUFFICIENT_INFO"}

# Same discipline as the A3 gate: NAMED qualifiers only, matched against punctuation-stripped titles,
# never bare suffix-containment. The last four are the shapes this screen found live and that the A3
# list does not carry.
#
# !! WRITE THESE AGAINST norm()-ED TEXT — NO PUNCTUATION. !! The first run of this file made exactly
# the mistake documented for the A3 gate three hours earlier: `^reviewer\s+#?\d+\s*\(` requires a
# literal "(" that norm() has already deleted, so it matched nothing, and `^retractions?` misses the
# commonest form, "RETRACTED:". Shadow detections went 6 -> 12 on the same 920 records once fixed.
# The lesson is that knowing about a class of bug does not prevent writing it again; only running the
# gate against a case it should catch does.
SHADOW_PATTERNS = [
    (r"^faculty\s+opinions?\s+recommendation\s+of\b", "faculty-opinions"),
    (r"^editorial\s+comment\s+(to|on)\b", "editorial-comment"),
    (r"^corrections?\b", "correction"),
    (r"^retract(ed|ion|ions)\b", "retraction"),
    (r"^erratum\b", "erratum"),
    (r"^expressions?\s+of\s+concern\b", "expression-of-concern"),
    (r"^re\b", "re-letter"),
    (r"^letter\s+to\s+the\s+editors?\b", "letter-to-editor"),
    (r"^comment\s+on\b", "comment-on"),
    (r"^author\s+response\b", "author-response"),
    (r"^reviewer\s+\d+\s+public\s+review\b", "reviewer-public-review"),
    (r"^peer\s+review\s+#?\d+\s+of\b", "peer-review-n"),
]


def norm(s):
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9 ]", " ", (s or "").lower())).strip()


def shadow_kind(title):
    t = norm(title)
    for pat, kind in SHADOW_PATTERNS:
        if re.search(pat, t):
            return kind
    return None


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
                                    "seed_ids", "from_primary_seed", "chemical_family")},
               "verdict": v["verdict"], "cell": v["cell"],
               "screen_family": v.get("family", ""), "screen_note": v.get("note", "")}
        multi = r["n_seeds"] > 1 or len(r["channels"]) > 1
        t = 0 if v["verdict"] == "NOT_RELEVANT" else (3 if v["verdict"] == "UNCERTAIN" else (1 if multi else 2))
        rec["tier"] = t
        tiers[t].append(rec)
    for t in tiers:
        tiers[t].sort(key=lambda x: (-(x["n_seeds"]), -(x["cited_by_count"] or 0)))

    allrecs = tiers[0] + tiers[1] + tiers[2] + tiers[3]

    # --- validation 2: anchor recovery ---
    known = {
        # Duplicate index record of Fei et al. 2009, the founding primary anchor. Carries no DOI.
        "W2908713169": "PRIMARY_EXPOSURE_TO_FERTILITY",
        # Correspondence attached to the nulliparous-women TTP anchor.
        "W2315733616": "PRIMARY_EXPOSURE_TO_FERTILITY",
        # The Wall 5 routing decoy (Sussarellu oyster) re-encountered inside its own cloud.
        "W2329639071": "OFF_ANIMAL",
        # The Wall 7 decoy's 2022 successor.
        "W4309099580": "OUTCOME_TREND_UNATTRIBUTED",
    }
    anchor_check = [(k, want, verdicts[k]["cell"] if k in verdicts else "NOT SCREENED",
                     (k in verdicts and verdicts[k]["cell"] == want))
                    for k, want in known.items()]

    # --- validation 3: decoy containment ---
    decoy_only = [v for vid, v in verdicts.items()
                  if ranked[vid]["seed_ids"] and set(ranked[vid]["seed_ids"]) <= decoy_seeds]
    decoy_away = sum(1 for v in decoy_only if v["verdict"] == "NOT_RELEVANT")

    # --- validation 4: chemical-family agreement (D1 deterministic vs screener, blind) ---
    fam_pairs = Counter()
    fam_disagree = []
    for r in allrecs:
        d1f, scf = r["chemical_family"], r["screen_family"]
        if not scf:
            continue
        fam_pairs[(d1f, scf)] += 1
        if d1f != scf:
            fam_disagree.append(r)
    n_fam = sum(fam_pairs.values())
    n_agree = sum(c for (a, b), c in fam_pairs.items() if a == b)

    # --- validation 5: shadow clusters inside Tier B ---
    shadows = []
    for r in allrecs:
        k = shadow_kind(r["title"])
        if k:
            shadows.append((k, r))
    shadow_counts = Counter(k for k, _ in shadows)

    json.dump({str(k): v for k, v in tiers.items()}, open(OUT_TIERS, "w"), indent=2)

    # --- RA gate worksheet ---
    gate_rows = [r for r in tiers[1] + tiers[2] + tiers[3]
                 if r["cell"] in PRIMARY_CELLS or r["cell"] in HELD_CELLS or r["cell"] in INPUT_CELLS]
    gate_rows.sort(key=lambda r: (r["cell"] not in PRIMARY_CELLS, r["cell"] not in INPUT_CELLS,
                                  -(r["cited_by_count"] or 0)))
    os.makedirs(EXTRACT, exist_ok=True)
    with open(OUT_GATE, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["openalex_id", "doi", "year", "title", "venue", "cell", "chemical_family",
                    "screen_family", "tier", "verdict", "n_seeds", "cited_by", "screen_note",
                    "RA_DECISION(RETRIEVE/EXCLUDE/UNSURE)", "RA_NOTE"])
        for r in gate_rows:
            w.writerow([r["id"], r["doi"] or "", r["year"], r["title"], r["venue"], r["cell"],
                        r["chemical_family"], r["screen_family"], r["tier"], r["verdict"],
                        r["n_seeds"], r["cited_by_count"] or 0, r["screen_note"], "", ""])

    def cell_by_family(cellset):
        out = Counter()
        for r in allrecs:
            if r["cell"] in cellset:
                out[r["screen_family"] or "unstated"] += 1
        return out

    n_primary = sum(1 for v in verdicts.values() if v["cell"] in PRIMARY_CELLS)
    n_input = sum(1 for v in verdicts.values() if v["cell"] in INPUT_CELLS)
    n_support = sum(1 for v in verdicts.values() if v["cell"] in SUPPORT_CELLS)
    n_held = sum(1 for v in verdicts.values() if v["cell"] in HELD_CELLS)
    prim_fam, input_fam = cell_by_family(PRIMARY_CELLS), cell_by_family(INPUT_CELLS)

    L = [f"# Screen report — {SLUG} (B.6)", "",
         f"**Screened: {len(verdicts)}** records — the D1 budget slice plus the both-axes "
         f"completeness bypass — out of a {len(ranked):,}-record deduplicated frame.", "",
         "| tier | definition | n |", "|---|---|---|",
         f"| 1 | RELEVANT, found through more than one channel or seed | {len(tiers[1])} |",
         f"| 2 | RELEVANT, single channel | {len(tiers[2])} |",
         f"| 3 | UNCERTAIN, retained for audit only | {len(tiers[3])} |",
         f"| — | NOT_RELEVANT, excluded | {len(tiers[0])} |", "",
         f"**Primary-cell records: {n_primary}** · **fertility-INPUT records (semen, ovarian): "
         f"{n_input}** · **support stream: {n_support}** · **held for full-text adjudication: "
         f"{n_held}**", "",
         "## The two families, counted", "",
         "This is the chapter's central result and it is a count rather than an estimate. Call 1 "
         "split B.6 into two chapters on the argument that its halves have incompatible evidence "
         "bases. The screen measures that argument.", "",
         "| cell group | pfas | plastic | both | none/unclear |", "|---|---|---|---|---|",
         f"| PRIMARY (a fertility quantity) | {prim_fam['pfas']} | {prim_fam['plastic']} | "
         f"{prim_fam['both']} | {prim_fam['none'] + prim_fam['unclear'] + prim_fam['unstated']} |",
         f"| INPUT (semen / ovarian parameter) | {input_fam['pfas']} | {input_fam['plastic']} | "
         f"{input_fam['both']} | {input_fam['none'] + input_fam['unclear'] + input_fam['unstated']} |",
         "", "## Cell distribution", "", "| cell | n |", "|---|---|"]
    for c, n in cells.most_common():
        L.append(f"| `{c}` | {n} |")

    L += ["", "## Validation 1 — anchor recovery on records whose answer was known", "", "",
          "| record | expected cell | screened cell | agree |", "|---|---|---|---|"]
    for k, want, got, ok in anchor_check:
        L.append(f"| `{k}` | `{want}` | `{got}` | {'yes' if ok else '**NO**'} |")

    L += ["", "## Validation 2 — decoy containment", "",
          f"{len(decoy_only)} screened records depend on a routing-decoy seed alone. The screen "
          f"routed **{decoy_away} of them away** ({decoy_away / max(len(decoy_only), 1):.0%}). A "
          "screen that admitted a decoy's neighbourhood wholesale would not be enforcing the walls; "
          "one that rejected all of it would mean the decoys were badly chosen, since a decoy sits "
          "beside the boundary cases the walls exist to adjudicate.", "",
          "## Validation 3 — chemical-family agreement, D1 versus the blind screener", "",
          f"D1 assigned the family deterministically from the named compound. The screener assigned "
          f"it independently, without seeing D1's tag. They agree on **{n_agree} of {n_fam} "
          f"records ({n_agree / max(n_fam, 1):.0%})**.", "",
          "| D1 tag | screener | n |", "|---|---|---|"]
    for (a, b), c in fam_pairs.most_common(12):
        L.append(f"| `{a}` | `{b}` | {c}{' ' if a == b else '  ← disagree'} |")

    L += ["", "## Validation 4 — shadow records inside Tier B", "",
          f"**{len(shadows)} screened records carry a shadow qualifier in their title.** The A3 gate "
          "protects the ANCHOR set; nothing protected Tier B, and the D1 title-collapse groups on "
          "the full normalised title, so a record titled *'Reviewer #2 (Public Review): X'* does not "
          "collapse onto *X*. Each of these is a separately-DOI'd row that an extraction stage would "
          "otherwise count as a study.", "",
          "| qualifier shape | n |", "|---|---|"]
    for k, n in shadow_counts.most_common():
        L.append(f"| `{k}` | {n} |")
    L += ["",
          "The two open-peer-review shapes — `reviewer-public-review` and `peer-review-n` — are new "
          "here and are the highest-multiplicity ones seen in any chapter: one eLife paper occupies "
          "six rows in this frame and one PeerJ review occupies four. They belong in "
          "`SHADOW_QUALIFIERS` in the A3 resolver, and the title-collapse in D1 should strip a "
          "leading qualifier before grouping.", ""]
    if shadows:
        L += ["Records:", ""]
        for k, r in sorted(shadows, key=lambda x: x[0]):
            L.append(f"- `{k}` — {r['title'][:96]}  ({r['id']}, tier {r['tier']})")

    open(OUT_REPORT, "w").write("\n".join(L) + "\n")

    print(f"screened={len(verdicts)} tier1={len(tiers[1])} tier2={len(tiers[2])} "
          f"tier3={len(tiers[3])} excluded={len(tiers[0])}")
    print(f"primary={n_primary} input={n_input} support={n_support} held={n_held}")
    print(f"family_agreement={n_agree}/{n_fam} ({n_agree / max(n_fam, 1):.0%}) "
          f"decoy_away={decoy_away}/{len(decoy_only)} shadows={len(shadows)}")
    print(f"anchor_recovery={sum(1 for *_, ok in anchor_check if ok)}/{len(anchor_check)}")
    print(f"-> {os.path.relpath(OUT_REPORT, ROOT)}")
    print(f"-> {os.path.relpath(OUT_GATE, ROOT)} ({len(gate_rows)} rows for the RA)")


if __name__ == "__main__":
    main()
