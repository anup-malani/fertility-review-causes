#!/usr/bin/env python3
"""
55_pdf_coverage.py — fine filter, extraction prerequisite: PDF full-text coverage.

Extraction (step 56) needs results TABLES, not abstracts, so it can only run on
studies whose full text we hold. This step reconciles the 40-study confirmed pool
against the PDFs already on disk (literature/pdfs/{slug}/, named by W-ID prefix)
and splits the pool into:
  - EXTRACTABLE   : full text present (this study's W-ID or a merged variant's)
  - BLOCKED       : no PDF -> goes on the acquisition want-list, NOT silently
                    dropped (silent drops bias the pool toward easy-to-get papers)

Match is by W-ID (paperId + dup_wids), with a normalized-title fallback against the
filename slug. Deterministic, offline. Emits the coverage split + a want-list.
"""
import json, os, re, glob
import unicodedata

SLUG = "old-age-security-pension-crowdout"
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
def rp(*a): return os.path.join(ROOT, *a)

# --- canonical fold, TICK-074. Keep in sync with source/lib/textnorm.py; the sync is ENFORCED by
# scripts/verify_norm.py, which imports every copy and compares it against the canonical one on a
# shared test vector. Two defects live here, both silent and both producing confident wrong answers:
# an unfolded accent SHATTERS a surname (Spéder -> "der"), and an ASCII apostrophe becomes a SPACE
# while a curly one is DELETED, so the same title normalises two different ways and a correct anchor
# is refused as NO-MATCH. Fold every class BEFORE the ASCII strip, and fold both spellings alike.
_TRANSLIT = {ord("ø"): "o", ord("Ø"): "O", ord("đ"): "d", ord("Đ"): "D", ord("ð"): "d",
             ord("Ð"): "D", ord("þ"): "th", ord("Þ"): "Th", ord("ı"): "i", ord("İ"): "I",
             ord("ł"): "l", ord("Ł"): "L", ord("æ"): "ae", ord("Æ"): "Ae", ord("œ"): "oe",
             ord("Œ"): "Oe", ord("ß"): "ss", ord("ħ"): "h", ord("Ħ"): "H", ord("ŋ"): "n",
             ord("Ŋ"): "N"}
_APOSTROPHE_CLASS = re.compile("['‘’ʼ´`]")
_DASH_CLASS = re.compile("[-‐‑‒–—―−­]")


def norm(s):
    s = (s or "").translate(_TRANSLIT)
    s = _APOSTROPHE_CLASS.sub("", s)
    s = _DASH_CLASS.sub(" ", s)
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode("ascii")
    s = re.sub(r"[^a-z0-9 ]", " ", s.lower())
    return re.sub(r"\s+", " ", s).strip()


def norm_slug(s):
    """55_'s original semantics: a squashed filename key with no separators at all. Built on the
    canonical fold so an accented title slugs the same way from either spelling."""
    return norm(s).replace(" ", "")

studies = json.load(open(rp("output", f"{SLUG}-fine-resolved.json")))
pdf_dir = rp("literature", "pdfs", SLUG)
pdfs = [os.path.basename(p) for p in glob.glob(os.path.join(pdf_dir, "*.pdf"))]

# index PDFs by W-ID prefix and by title-slug
pdf_by_wid, pdf_slugs = {}, []
for fn in pdfs:
    wid = fn.split("__", 1)[0]
    pdf_by_wid[wid] = fn
    slug = fn.split("__", 1)[1].rsplit(".pdf", 1)[0] if "__" in fn else fn
    pdf_slugs.append((norm_slug(slug), fn))

def find_pdf(r):
    for w in [r["paperId"]] + r.get("dup_wids", []):
        if w in pdf_by_wid:
            return pdf_by_wid[w]
    tn = norm_slug(r["title"])[:40]                 # title-slug fallback (filenames truncate)
    for sslug, fn in pdf_slugs:
        if tn and (tn in sslug or sslug[:40] == tn):
            return fn
    return None

covered, blocked = [], []
for r in studies:
    fn = find_pdf(r)
    r["pdf"] = fn
    (covered if fn else blocked).append(r)

json.dump(studies, open(rp("output", f"{SLUG}-fine-resolved.json"), "w"),
          ensure_ascii=False, indent=1)

# want-list for the blocked papers (DOI link + scholar link)
wl = [f"# Extraction want-list — {SLUG}", "",
      f"{len(blocked)} of {len(studies)} confirmed studies lack full text and are "
      f"**extraction-blocked** until acquired. Not dropped — flagged.", ""]
for r in blocked:
    doi = r.get("doi")
    link = f"https://doi.org/{doi}" if doi and doi != "unknown" else \
           "https://scholar.google.com/scholar?q=" + re.sub(r"\s+", "+", (r["title"] or ""))
    wl.append(f"- {(r['title'] or '')[:75]}"
              + (f"  ·gold" if r.get("is_gold") else "")
              + f"\n    {link}"
              + (f"  ·existence={r.get('existence')}" if r.get("existence", "").startswith(("ABSENT", "UNCONF")) else ""))
open(rp("output", f"{SLUG}-extraction-wantlist.md"), "w").write("\n".join(wl) + "\n")

print(f"PDF coverage over {len(studies)} distinct studies:")
print(f"  EXTRACTABLE (full text present): {len(covered)}")
print(f"  BLOCKED (need acquisition):      {len(blocked)}")
gold_blocked = [r for r in blocked if r.get("is_gold")]
print(f"  of blocked, gold anchors: {len(gold_blocked)}")
print(f"wrote output/{SLUG}-extraction-wantlist.md")
print(f"\nready for extraction (step 56): {len(covered)} studies with full text")
