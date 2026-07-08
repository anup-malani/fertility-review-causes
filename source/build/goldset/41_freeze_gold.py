#!/usr/bin/env python3
"""
41_freeze_gold.py — gold-freeze step 2 of 2 (canonical workflow §7, move 2 prerequisite).

Apply the RA sign-off on the 52 Tier-B UNCERTAINs and emit the FROZEN, DOI-keyed
gold instrument the clean end-to-end run measures against.

Inputs (all committed/reproducible):
  output/{slug}-tierb-uncertain-adjudication.csv   RA sign-off ("approve as recommended"
                                                   -> ra_decision := rec_decision)
  blind_reads.json                                 estimand cell for each promoted paper
  literature/search-logs/{slug}-tier-a-draft.json  Tier A (56 anchors)
  literature/search-logs/{slug}-tier-b-screened.json  Tier B (247 RELEVANT)
  estimand_tierb_tags.json                         247 Tier-B estimand tags
  tierb_screen_batch_*.json                        metadata for promoted papers

Outputs (the frozen instrument):
  literature/search-logs/{slug}-tier-a-frozen.json     56, RA-signed
  literature/search-logs/{slug}-tier-b-frozen.json     247 + promotions
  estimand_tierb_tags_frozen.json                      tags extended to match
  literature/search-logs/{slug}-gold-freeze-manifest.json   counts, sign-off, stamp

Freeze date is a fixed constant so re-runs are bit-identical (the repo freezes gold
as committed artifacts even though upstream resolution is not bit-deterministic).
"""
import json, glob, csv, os

SLUG = "old-age-security-pension-crowdout"
FREEZE_DATE = "2026-07-08"
FREEZE_BY = "Shravan (RA) — approved as recommended; blind second read by Claude (Opus)"

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
LOGS = os.path.join(ROOT, "literature", "search-logs")
OUT = os.path.join(ROOT, "output")

# ---- 1. apply the sign-off: ra_decision := rec_decision --------------------
adj_path = os.path.join(OUT, f"{SLUG}-tierb-uncertain-adjudication.csv")
rows = list(csv.DictReader(open(adj_path)))
for r in rows:
    if not r["ra_decision"]:                      # unsigned -> take recommendation
        r["ra_decision"] = r["rec_decision"]
        r["ra_cell"] = r["rec_cell"]
        r["ra_note"] = "approved as recommended"
with open(adj_path, "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=rows[0].keys())
    w.writeheader(); w.writerows(rows)

promoted = [r for r in rows if r["ra_decision"] == "INCLUDE"]
promoted_ids = {r["paperId"] for r in promoted}
print(f"sign-off applied: {len(promoted)} INCLUDE / {len(rows)-len(promoted)} EXCLUDE of {len(rows)}")

# ---- 2. gather metadata for promoted papers --------------------------------
meta = {}
for f in sorted(glob.glob(os.path.join(HERE, "tierb_screen_batch_*.json"))):
    d = json.load(open(f))
    items = d if isinstance(d, list) else list(d.values())[0]
    for it in items:
        if isinstance(it, dict) and it.get("paperId"):
            meta[it["paperId"]] = it
blind = json.load(open(os.path.join(HERE, "blind_reads.json")))

# ---- 3. extend Tier B (247 -> +promotions) ---------------------------------
tierb = json.load(open(os.path.join(LOGS, f"{SLUG}-tier-b-screened.json")))
existing_ids = {b["paperId"] for b in tierb}
assert not (promoted_ids & existing_ids), "a promoted paper is already in Tier B"

for pid in promoted_ids:
    m = meta.get(pid, {})
    tierb.append({
        "paperId": pid,
        "title": m.get("title"),
        "year": m.get("year"),
        "venue": m.get("venue"),
        "authors": m.get("authors"),
        "provenance_tier": "B",
        "snowballPhase": m.get("snowballPhase"),
        "snow_confidence": m.get("snow_confidence"),
        "resolve_status": m.get("resolve_status"),
        "screen_verdict": "RELEVANT",
        "screen_confidence": "RA-adjudicated",
        "screen_reason": f"Promoted from UNCERTAIN on RA sign-off {FREEZE_DATE}: {blind[pid]['reason']}",
        "keytype": m.get("keytype"),
        "doi": m.get("doi"),
    })

# ---- 4. extend the estimand tags to match ----------------------------------
tags = json.load(open(os.path.join(HERE, "estimand_tierb_tags.json")))
tag_ids = {t["id"] for t in tags}
cell_map = {"THEORY": ("fertility (model equilibrium)", "forward"),
            "OFF": ("off-outcome (see reason)", "forward"),
            "PRIMARY": ("fertility", "forward")}
for pid in promoted_ids:
    if pid in tag_ids:
        continue
    b = blind[pid]
    outcome, direction = cell_map.get(b["cell"], ("unknown", "forward"))
    tags.append({
        "id": pid, "outcome": outcome, "direction": direction,
        "mechanism": b["reason"], "cell": b["cell"],
        "confidence": "RA-adjudicated",
        "reason": f"RA-adjudicated promotion {FREEZE_DATE}: {b['reason']}",
    })

# ---- 5. freeze Tier A (sign-off only; content unchanged) -------------------
tiera = json.load(open(os.path.join(LOGS, f"{SLUG}-tier-a-draft.json")))

# ---- 6. write frozen artifacts + manifest ----------------------------------
def dump(path, obj):
    json.dump(obj, open(path, "w"), indent=2, ensure_ascii=False)

dump(os.path.join(LOGS, f"{SLUG}-tier-a-frozen.json"), tiera)
dump(os.path.join(LOGS, f"{SLUG}-tier-b-frozen.json"), tierb)
dump(os.path.join(HERE, "estimand_tierb_tags_frozen.json"), tags)

from collections import Counter
cell_counts = Counter(t["cell"] for t in tags)
n_primary = cell_counts.get("PRIMARY", 0)

manifest = {
    "hypothesis": SLUG,
    "freeze_date": FREEZE_DATE,
    "frozen_by": FREEZE_BY,
    "tier_a_anchors": len(tiera),
    "tier_b_before": len(existing_ids),
    "tier_b_promoted": len(promoted_ids),
    "tier_b_after": len(tierb),
    "uncertains_adjudicated": len(rows),
    "uncertains_included": len(promoted_ids),
    "uncertains_excluded": len(rows) - len(promoted_ids),
    "promotions_by_cell": dict(Counter(blind[p]["cell"] for p in promoted_ids)),
    "tier_b_estimand_cells": dict(cell_counts),
    "primary_cell_denominator": n_primary,
    "note": ("All promotions are THEORY/OFF (0 PRIMARY), so the frozen gold is "
             "denominator-neutral for estimand-filtered Recall(B); it enlarges only "
             "the topical/theory tail. 3 corrupted + 34 title-only UNCERTAINs excluded "
             "(conservative denominator, abstract-or-live-DOI hygiene gate)."),
    "provenance": ["40_freeze_adjudicate_uncertains.py", "41_freeze_gold.py"],
}
dump(os.path.join(LOGS, f"{SLUG}-gold-freeze-manifest.json"), manifest)

print(f"\nFROZEN GOLD  ({FREEZE_DATE})")
print(f"  Tier A: {len(tiera)} anchors (signed)")
print(f"  Tier B: {len(existing_ids)} + {len(promoted_ids)} = {len(tierb)}")
print(f"  promotions by cell: {manifest['promotions_by_cell']}")
print(f"  PRIMARY-cell denominator (unchanged): {n_primary}")
print(f"  wrote frozen Tier A/B, extended tags, and the freeze manifest to literature/search-logs/")
