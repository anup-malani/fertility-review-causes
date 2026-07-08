#!/usr/bin/env python3
"""
40_freeze_adjudicate_uncertains.py — gold-freeze step 1 of 2.

Adjudicate the 52 Tier-B UNCERTAINs ahead of the clean end-to-end run (canonical
workflow §7, move 2). Two-stage:

  (a) abstract-or-live-DOI HYGIENE GATE — classify each UNCERTAIN's abstract as
      CLEAN / CORRUPTED / TITLE_ONLY. Corrupted = ghost-citation contamination
      (an off-topic abstract mis-joined onto a pension paper; the evaluation §5
      and the Tier-B audit both caught these). A corrupted abstract is demoted to
      TITLE_ONLY — we will not adjudicate against injected text.

  (b) build the batched RA sign-off SHEET (one CSV, estimand-adjudication.csv
      schema) with a recommended decision per paper:
        - TITLE_ONLY  -> rec EXCLUDE   (policy: title-only UNCERTAINs are not
                          promoted into the frozen Tier B — conservative
                          denominator; they stay in the Tier-3 recall net)
        - CLEAN       -> rec from the blind second read in blind_reads.json
                          (independent of the original screen verdict)

The RA (Shravan) reviews the sheet — the CLEAN rows are the real decisions; the
TITLE_ONLY/CORRUPTED rows are shown for awareness with a default EXCLUDE.

Outputs:
  output/{slug}-tierb-uncertain-adjudication.csv   the sign-off sheet
  uncertain_hygiene.json                           per-paper hygiene classification
"""
import json, glob, csv, re, os

SLUG = "old-age-security-pension-crowdout"
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "..", "output")

# ---- load UNCERTAIN verdicts + screen metadata -----------------------------
verd = {}
for f in sorted(glob.glob(os.path.join(HERE, "tierb_screen_verdict_*.json"))):
    for it in json.load(open(f)):
        verd[it["paperId"]] = it
meta = {}
for f in sorted(glob.glob(os.path.join(HERE, "tierb_screen_batch_*.json"))):
    d = json.load(open(f))
    items = d if isinstance(d, list) else list(d.values())[0]
    for it in items:
        if isinstance(it, dict) and it.get("paperId"):
            meta[it["paperId"]] = it

unc = [v for v in verd.values() if v["verdict"].upper() == "UNCERTAIN"]

# ---- hygiene gate ----------------------------------------------------------
# On-topic lexicon: a clean abstract for this hypothesis should hit at least one.
ONTOPIC = re.compile(
    r"fertilit|birth|child|pension|social security|old[- ]age|payg|pay-as-you-go|"
    r"overlapping generation|olg|intergenerational|transfer|family support|"
    r"demographic|offspring|parenthood|dependenc|savings|retire",
    re.I,
)
# Known contamination markers seen in the pilot (openworm/C.elegans, IUCN Red List,
# speech/chemistry/Shakespeare injections). Generic enough to catch the class.
CONTAM = re.compile(
    r"c\.?\s*elegans|openworm|iucn|red list|threatened species|conservation status|"
    r"phoneme|speech recognition|organic chemistry|shakespeare|behavioural database",
    re.I,
)

def classify(paper_id, m):
    ab = (m.get("abstract") or m.get("abstractText") or "").strip()
    title = m.get("title") or ""
    if len(ab) < 40:
        return "TITLE_ONLY", "no usable abstract"
    if CONTAM.search(ab):
        return "CORRUPTED", "off-topic injected text (ghost-citation contamination)"
    # substantive abstract with zero on-topic vocabulary -> almost certainly injected
    if not ONTOPIC.search(ab):
        return "CORRUPTED", "abstract shares no on-topic vocabulary with the hypothesis"
    return "CLEAN", "abstract usable"

hygiene = {}
for u in unc:
    pid = u["paperId"]
    m = meta.get(pid, {})
    cls, why = classify(pid, m)
    hygiene[pid] = {"class": cls, "why": why, "title": m.get("title"),
                    "year": m.get("year"), "authors": m.get("authors"),
                    "orig_confidence": u.get("confidence"), "orig_reason": u.get("reason")}

json.dump(hygiene, open(os.path.join(HERE, "uncertain_hygiene.json"), "w"), indent=2)

n_clean = sum(1 for h in hygiene.values() if h["class"] == "CLEAN")
n_corr = sum(1 for h in hygiene.values() if h["class"] == "CORRUPTED")
n_title = sum(1 for h in hygiene.values() if h["class"] == "TITLE_ONLY")
print(f"UNCERTAINs: {len(unc)}  |  CLEAN {n_clean}  CORRUPTED {n_corr}  TITLE_ONLY {n_title}")
print("CLEAN (the real adjudication set):")
for pid, h in hygiene.items():
    if h["class"] == "CLEAN":
        print(f"  {pid}  {(h['title'] or '')[:70]}")
print("CORRUPTED (demote -> title-only -> EXCLUDE):")
for pid, h in hygiene.items():
    if h["class"] == "CORRUPTED":
        print(f"  {pid}  {(h['title'] or '')[:60]}  [{h['why']}]")

# ---- merge the blind second read (CLEAN rows only) -------------------------
blind_path = os.path.join(HERE, "blind_reads.json")
blind = json.load(open(blind_path)) if os.path.exists(blind_path) else {}

def rec_for(pid, cls):
    if cls in ("TITLE_ONLY", "CORRUPTED"):
        return "EXCLUDE", "", "title-only/corrupted — not promoted to Tier B (policy)"
    b = blind.get(pid)
    if not b:
        return "", "", "PENDING blind read"
    return b["decision"], b.get("cell", ""), b.get("reason", "")

# ---- write the sign-off sheet ---------------------------------------------
os.makedirs(OUT, exist_ok=True)
sheet = os.path.join(OUT, f"{SLUG}-tierb-uncertain-adjudication.csv")
# CLEAN first (real decisions), then corrupted, then title-only
order = {"CLEAN": 0, "CORRUPTED": 1, "TITLE_ONLY": 2}
rows = sorted(unc, key=lambda u: order[hygiene[u["paperId"]]["class"]])
with open(sheet, "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["paperId", "hygiene", "title", "authors", "year",
                "rec_decision", "rec_cell", "rec_reason",
                "ra_decision", "ra_cell", "ra_note"])
    for u in rows:
        pid = u["paperId"]
        h = hygiene[pid]
        dec, cell, reason = rec_for(pid, h["class"])
        w.writerow([pid, h["class"], h["title"], h.get("authors"), h.get("year"),
                    dec, cell, reason, "", "", ""])
print(f"\nwrote {sheet}")
print("  CLEAN rows carry the blind-read recommendation; RA fills ra_decision/ra_cell/ra_note.")
