#!/usr/bin/env python3
"""
56c_extractability_ledger.py — classify the RA-confirmed pool by the LOOSE bar.

Working definition (Shravan, 2026-07-10): a study is EXTRACTABLE if we can pull
BOTH (a) a numeric effect size of a social-security/pension variable on a
fertility outcome and (b) a sample/population size N. That is all that is needed
to call it extractable right now; the causal/R^2 split, treatment-type pooling,
partial-R^2, derived shares, and the GRADE rating are all deferred (see 56b for
the richer machinery, run later).

Reads the confirmed pool (fine-resolved.json), the frozen per-study extraction
records (temp/extraction/rec_*.json), and the PDF folder, and emits a single
ledger over all 40 studies with one of three statuses:

  EXTRACTABLE     - an extraction record yields effect size + N.
  PDF_NO_EFFECT   - a PDF/record exists but no (effect size + N) was found.
  NO_PDF          - no full text yet -> acquisition is the only blocker.

Deterministic given the frozen records. Likely within-pool duplicates are
flagged (normalized-title near-match) but NOT merged - that is an RA call.
"""
import json, os, glob, re
from collections import defaultdict

SLUG = "old-age-security-pension-crowdout"
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
def rp(*a): return os.path.join(ROOT, *a)

pool = json.load(open(rp("output", f"{SLUG}-fine-resolved.json")))
recs = {}
for f in glob.glob(rp("temp", "extraction", "rec_*.json")):
    try:
        r = json.load(open(f)); recs[r["paperId"]] = r
    except Exception:
        pass

# PDF availability by paperId prefix and by title-prefix match
pdfdir = rp("literature", "pdfs", SLUG)
pdfs = os.listdir(pdfdir) if os.path.isdir(pdfdir) else []
pid_pdf = {}
for f in pdfs:
    m = re.match(r"(W\d+)__", f)
    if m: pid_pdf.setdefault(m.group(1), f)
def norm(t): return re.sub(r"[^a-z0-9]+", " ", (t or "").lower()).strip()
pdf_titles = {f: norm(f.split("__", 1)[1][:-4]) for f in pdfs if "__" in f}

def has_pdf(pid, title):
    # exact paperId match only. Title-prefix matching cross-contaminates near-duplicate
    # titles (e.g. the typo-dup "What explains fertilit?" onto the real Italian paper's
    # PDF), which would falsely populate PDF_NO_EFFECT. A study with a genuine record but
    # a drifted paperId still lands EXTRACTABLE via effect_and_n(), independent of this.
    return pid_pdf.get(pid)

def num(x):
    try: return float(x)
    except (TypeError, ValueError): return None

def effect_and_n(rec):
    """Loose bar: does either record carry an effect size AND an N?"""
    if not rec: return (None, None, None)
    for key in ("causal_record", "r2_record"):
        r = rec.get(key) or {}
        est = num(r.get("estimate")) if r.get("estimate") is not None else num(r.get("coef"))
        n = num(r.get("n")) or num(r.get("df_or_n"))
        if est is not None and n is not None:
            return (est, n, key)
    # effect present but N missing, or vice versa -> report what we have, not extractable
    for key in ("causal_record", "r2_record"):
        r = rec.get(key) or {}
        est = num(r.get("estimate")) if r.get("estimate") is not None else num(r.get("coef"))
        n = num(r.get("n")) or num(r.get("df_or_n"))
        if est is not None or n is not None:
            return (est, n, None)
    return (None, None, None)

# likely within-pool duplicates (token-set Jaccard on normalized titles).
# A shared prefix is NOT enough ("The Impact of Social Security on {Saving...Germany}"
# vs "{...Fertility Willingness}" share 6 words but are different papers); require
# high whole-title token overlap.
titles = {r["paperId"]: norm(r["title"]) for r in pool}
toks = {p: set(t.split()) for p, t in titles.items()}
dups = {}
ids = list(titles)
for i, a in enumerate(ids):
    for b in ids[i+1:]:
        ta, tb = toks[a], toks[b]
        if len(ta) < 4 or len(tb) < 4: continue
        j = len(ta & tb) / len(ta | tb)
        if j >= 0.80:
            dups.setdefault(a, b); dups.setdefault(b, a)

ledger = []
for r in pool:
    pid, title = r["paperId"], r["title"]
    rec = recs.get(pid)
    est, n, src = effect_and_n(rec)
    pdf = has_pdf(pid, title)
    if est is not None and n is not None:
        status = "EXTRACTABLE"
    elif pdf or rec:
        status = "PDF_NO_EFFECT"
    else:
        status = "NO_PDF"
    ledger.append({
        "paperId": pid, "title": title, "doi": r.get("doi"), "is_gold": bool(r.get("is_gold")),
        "status": status, "effect_size": est, "n": n, "from_record": src,
        "has_pdf": bool(pdf), "has_record": bool(rec),
        "dup_of": dups.get(pid),
    })

order = {"EXTRACTABLE": 0, "PDF_NO_EFFECT": 1, "NO_PDF": 2}
ledger.sort(key=lambda x: (order[x["status"]], not x["is_gold"], x["title"] or ""))

json.dump(ledger, open(rp("output", f"{SLUG}-extractability-ledger.json"), "w"),
          ensure_ascii=False, indent=1)

counts = defaultdict(int)
for x in ledger: counts[x["status"]] += 1
gold_extractable = sum(1 for x in ledger if x["status"] == "EXTRACTABLE" and x["is_gold"])

L = [f"# Extractability ledger — {SLUG}", "",
     "**Loose bar (2026-07-10):** a study is *extractable* if we can pull an effect size "
     "of an OAS/pension variable on fertility **and** a sample size N. Causal/R² split, "
     "pooling, and GRADE are deferred.", "",
     f"- **EXTRACTABLE: {counts['EXTRACTABLE']} / {len(ledger)}**  ({gold_extractable} gold)",
     f"- PDF_NO_EFFECT (full text, no effect+N found): {counts['PDF_NO_EFFECT']}",
     f"- NO_PDF (acquisition is the only blocker): {counts['NO_PDF']}", "",
     "| status | gold | study | effect | N | doi | note |",
     "|---|---|---|---|---|---|---|"]
for x in ledger:
    note = f"dup of {x['dup_of']}" if x["dup_of"] else ""
    L.append(f"| {x['status']} | {'G' if x['is_gold'] else ''} | {(x['title'] or '')[:46]} "
             f"| {x['effect_size'] if x['effect_size'] is not None else ''} "
             f"| {int(x['n']) if x['n'] else ''} | {x['doi'] or ''} | {note} |")
open(rp("output", f"{SLUG}-extractability-ledger.md"), "w").write("\n".join(L) + "\n")

print(f"pool={len(ledger)}  EXTRACTABLE={counts['EXTRACTABLE']} ({gold_extractable} gold)  "
      f"PDF_NO_EFFECT={counts['PDF_NO_EFFECT']}  NO_PDF={counts['NO_PDF']}")
if dups:
    print("likely within-pool dups (flagged, not merged):",
          {k: v for k, v in dups.items()})
