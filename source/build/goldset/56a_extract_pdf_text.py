#!/usr/bin/env python3
"""
56a_extract_pdf_text.py — turn each covered PDF into a text input for extraction.

For every study in the confirmed pool that holds a full-text PDF (step 55/55b),
dump the PDF text to temp/extraction/{paperId}.txt and write a manifest the
extraction pass (56) consumes. Deterministic given the PDFs. Text is lightly
cleaned (dehyphenate line-breaks, collapse whitespace) but not truncated here;
the extraction step decides how much to feed the model.
"""
import json, os, re, glob
import fitz  # pymupdf

SLUG = "old-age-security-pension-crowdout"
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
def rp(*a): return os.path.join(ROOT, *a)
PDFDIR = rp("literature", "pdfs", SLUG)
OUT = rp("temp", "extraction")
os.makedirs(OUT, exist_ok=True)

def clean(t):
    t = re.sub(r"-\n(\w)", r"\1", t)          # de-hyphenate across line breaks
    t = re.sub(r"[ \t]+", " ", t)
    t = re.sub(r"\n{3,}", "\n\n", t)
    return t.strip()

_COMMON = set("the of and to in a is that for on as with by are be this an it from at was which "
              "pension pensions social security fertility children".split())
def looks_corrupt(t):
    """Detect font-encoding-shifted text (a custom-encoded embedded font with no
    ToUnicode CMap renders as gibberish — every glyph offset by a constant). Clean
    academic English hits ~0.30 common-word ratio; corrupt text hits <0.10.
    Caught Guinnane–Streb (Bismarck) at 0.043 vs the pool's ~0.30."""
    words = re.findall(r"[a-z]{2,}", t.lower())
    if len(words) < 200:
        return False                          # too short to judge; handled elsewhere
    return sum(1 for w in words[:4000] if w in _COMMON) / min(len(words), 4000) < 0.10

studies = json.load(open(rp("output", f"{SLUG}-fine-resolved.json")))
manifest = []
for r in studies:
    fn = r.get("pdf")
    if not fn:
        continue
    path = os.path.join(PDFDIR, fn)
    if not os.path.exists(path):
        continue
    try:
        doc = fitz.open(path)
        text = clean("\n".join(pg.get_text() for pg in doc))
        doc.close()
    except Exception as e:
        text = ""
    if len(text) < 500:                        # scanned/broken -> flag, don't fake
        manifest.append({"paperId": r["paperId"], "title": r["title"], "doi": r.get("doi"),
                         "chars": len(text), "status": "TEXT_TOO_SHORT"})
        continue
    if looks_corrupt(text):                    # font-shift gibberish -> don't feed to extractor
        manifest.append({"paperId": r["paperId"], "title": r["title"], "doi": r.get("doi"),
                         "chars": len(text), "status": "TEXT_CORRUPT"})
        continue
    txt_path = os.path.join(OUT, f"{r['paperId']}.txt")
    open(txt_path, "w").write(text)
    manifest.append({"paperId": r["paperId"], "title": r["title"], "doi": r.get("doi"),
                     "is_gold": r.get("is_gold"), "chars": len(text),
                     "txt": os.path.relpath(txt_path, ROOT), "status": "OK"})

json.dump(manifest, open(os.path.join(OUT, "manifest.json"), "w"), ensure_ascii=False, indent=1)
ok = [m for m in manifest if m["status"] == "OK"]
print(f"extracted text for {len(ok)} studies (of {len(manifest)} with PDFs)")
for m in ok:
    print(f"  {m['chars']:>7,} chars  {(m['title'] or '')[:60]}")
short = [m for m in manifest if m["status"] != "OK"]
if short:
    print(f"  {len(short)} PDF(s) had too little text (scanned?) — flagged, not extracted")
