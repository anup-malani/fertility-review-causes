#!/usr/bin/env python3
"""
240_a23_extract_fulltext.py — A.23, stage 6a. Turn every retrieved file into readable text.

Retrieval delivered three kinds of file — publisher PDFs, HTML bodies that cleared stage 5b's
full-text floor, and PMC structured text — and the full-text screen should not care which. This
normalises all three into `temp/a23-fulltext/{WID}.txt` with one manifest.

**IT INHERITS THE CORRUPTION DETECTOR FROM `56a`, WHICH IS NOT OPTIONAL HERE.** A PDF whose embedded
font carries no ToUnicode CMap extracts as gibberish — every glyph shifted by a constant — and the
result is a file of the right length, full of words, that means nothing. `56a` caught
Guinnane–Streb at a common-word ratio of 0.043 against a pool's 0.30. A screen fed that text does
not error; it reads a paper that does not exist.

**AND IT ADDS A SECOND FAILURE THE FIRST ONE CANNOT SEE: THE NON-ENGLISH RECORD.** This frame is
not an English-language literature — the retrieved set includes Catalan, Russian, Japanese and
Spanish records. A common-ENGLISH-word ratio flags every one of them as corrupt, which is the wrong
verdict: the text is fine and the reader is wrong. The two are separated by asking whether the text
is mostly Latin-script at all, and non-English records are routed to their own bucket to be read
rather than dropped as damaged.

**A SCANNED PDF WITH NO TEXT LAYER IS ITS OWN OUTCOME.** Older records in this frame are scans.
`pdftotext` returns near-nothing and a word-count floor is what separates that from a short paper.

Output: temp/a23-fulltext/{WID}.txt
        extraction/{slug}-fulltext-manifest.json
        literature/search-logs/{slug}-fulltext-extraction-log.md
"""
import json, os, re, unicodedata
from collections import Counter

SLUG = "co-residence-parents-household-delay"
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
PDF_DIR = os.path.join(ROOT, "literature", "pdfs", SLUG)
OUT_DIR = os.path.join(ROOT, "temp", "a23-fulltext")
OA = os.path.join(ROOT, "extraction", f"{SLUG}-oa-status.json")
OUT_JSON = os.path.join(ROOT, "extraction", f"{SLUG}-fulltext-manifest.json")
OUT_MD = os.path.join(ROOT, "literature", "search-logs", f"{SLUG}-fulltext-extraction-log.md")

MIN_WORDS = 800            # below this a "full text" is a scan, a stub or a front matter page
COMMON_EN = set("the of and to in a is that for on as with by are be this an it from at was which "
                "we our not their they have has were more than between when where household "
                "fertility children parents coresidence residence family birth women".split())


def clean(t):
    t = re.sub(r"-\n(\w)", r"\1", t)
    t = re.sub(r"[ \t]+", " ", t)
    return re.sub(r"\n{3,}", "\n\n", t).strip()


def latin_share(t):
    """Fraction of letters in the Latin script. Separates 'the extractor produced garbage' from
    'this paper is in Russian or Japanese', which a common-English-word test cannot do."""
    letters = [c for c in t[:20000] if c.isalpha()]
    if not letters:
        return 0.0
    lat = sum(1 for c in letters if "LATIN" in unicodedata.name(c, ""))
    return lat / len(letters)


def en_ratio(t):
    words = re.findall(r"[a-z]{2,}", t.lower())
    if len(words) < 200:
        return None
    n = min(len(words), 4000)
    return sum(1 for w in words[:n] if w in COMMON_EN) / n


def verdict(t):
    """(status, note). Four outcomes, and the point of having four is that three of them are
    recoverable in different ways and one is not."""
    words = len(t.split())
    if words < MIN_WORDS:
        return "too_short", f"{words} words — a scan with no text layer, or front matter only"
    ls = latin_share(t)
    if ls < 0.60:
        return "non_english_script", f"{ls:.0%} Latin script — read, do not discard"
    r = en_ratio(t)
    if r is not None and r < 0.10:
        return "corrupt_or_non_english", (f"common-English ratio {r:.3f} at {ls:.0%} Latin script "
                                          "— a font with no ToUnicode CMap, or a Latin-script "
                                          "language that is not English")
    return "ok", f"{words:,} words" + (f", English ratio {r:.2f}" if r is not None else "")


def pdf_text(path):
    try:
        import fitz
        with fitz.open(path) as doc:
            return "\n\n".join(p.get_text() for p in doc)
    except Exception as e:
        return f""


def main():
    meta = {r["id"]: r for r in json.load(open(OA))}
    os.makedirs(OUT_DIR, exist_ok=True)
    files = {}
    for f in sorted(os.listdir(PDF_DIR)):
        m = re.match(r"(W\d+)__", f)
        if m and os.path.getsize(os.path.join(PDF_DIR, f)) > 1024:
            files.setdefault(m.group(1), []).append(f)

    rows = []
    for wid, fs in sorted(files.items()):
        # Prefer structured text over a PDF: PMC BioC and the HTML floor both arrive with tables
        # intact, which is what extraction wants, and neither can be font-corrupted.
        fs = sorted(fs, key=lambda f: (0 if f.endswith(".txt") else 1, len(f)))
        src, text = None, ""
        for f in fs:
            p = os.path.join(PDF_DIR, f)
            t = clean(open(p, errors="replace").read()) if f.endswith(".txt") else clean(pdf_text(p))
            if len(t.split()) > len(text.split()):
                src, text = f, t
        st, note = verdict(text)
        if text:
            open(os.path.join(OUT_DIR, wid + ".txt"), "w").write(text)
        m = meta.get(wid, {})
        rows.append(dict(id=wid, tier=m.get("tier"), design=m.get("design"), route=m.get("route"),
                         verdict=m.get("verdict"), title=m.get("title"), source_file=src,
                         kind=("text" if (src or "").endswith(".txt") else "pdf"),
                         words=len(text.split()), status=st, note=note))

    json.dump(rows, open(OUT_JSON, "w"), indent=2)

    pc = lambda n, d: f"{n / d:.0%}" if d else "n/a"
    st = Counter(r["status"] for r in rows)
    kind = Counter(r["kind"] for r in rows)
    PRIM = ("T1_wall1_packet", "T1_primary_identified", "T2_primary_relevant",
            "T3_primary_uncertain", "T3_link1_identified")
    prim = [r for r in rows if r["tier"] in PRIM]
    prim_ok = [r for r in prim if r["status"] == "ok"]
    bad = [r for r in rows if r["status"] != "ok"]

    L = [f"# Stage 6a full-text extraction — {SLUG} (A.23)", "",
         "**Generated by:** `source/build/goldset/240_a23_extract_fulltext.py`", "",
         f"**{len(rows)} retrieved records normalised to text**; "
         f"**{st['ok']} are readable ({pc(st['ok'], len(rows))})**. Of the "
         f"{len(prim)} in a primary or critical tier, **{len(prim_ok)} are readable**.", "",
         "Three kinds of file arrive from retrieval — publisher PDFs, HTML bodies that cleared "
         "stage 5b's floor, and PMC structured text — and the screen should not care which. Where a "
         "record has both, **structured text is preferred over the PDF**: it comes with tables "
         "intact and it cannot be font-corrupted.", "",
         "## Status", "", "| Status | n | What it is |", "|---|---|---|"]
    MEAN = {"ok": "readable",
            "too_short": f"under {MIN_WORDS} words — a scan with no text layer, or front matter",
            "non_english_script": "not Latin script — **read it, do not discard it**",
            "corrupt_or_non_english": "a font with no ToUnicode CMap, or a Latin-script language "
                                      "that is not English; the two need a human to tell apart"}
    for k, n in st.most_common():
        L.append(f"| `{k}` | {n} | {MEAN.get(k, '')} |")
    L += ["", "## Why there are four statuses and not two", "",
          "`56a` detects font corruption with a common-English-word ratio, and it works: it caught "
          "a PDF at 0.043 against a pool's 0.30, where the text was the right length, full of "
          "words, and meaningless. A screen fed that does not error — it reads a paper that does "
          "not exist.", "",
          "**That test alone is wrong for this frame.** A.23's retrieved set includes Catalan, "
          "Russian, Japanese and Spanish records, and a common-English-word ratio calls every one "
          "of them corrupt. The verdict would be that the text is damaged when the text is fine and "
          "the reader is wrong. Asking first whether the text is Latin script at all separates "
          "them, and the non-Latin records go to their own bucket to be read.", "",
          "The residual `corrupt_or_non_english` bucket is honest about what it cannot separate: a "
          "Spanish paper and a corrupted English one both score low on English words at high Latin "
          "share. That is a human's call, and it is named rather than resolved by guessing.", "",
          "## Source of the text", "", "| Kind | n |", "|---|---|"]
    for k, n in kind.most_common():
        L.append(f"| {k} | {n} |")
    if bad:
        L += ["", "## Every record that is not readable, named", "",
              "| Tier | Status | Words | Record |", "|---|---|---|---|"]
        for r in sorted(bad, key=lambda x: (x["status"], x["tier"] or "")):
            L.append(f"| `{r['tier']}` | `{r['status']}` | {r['words']:,} | "
                     f"{(r['title'] or '')[:66]} |")
    L += ["", "**A retrieved file is not a readable study**, and the gap between the two is this "
          "table. Stage 6's denominator is the readable set, not the retrieved set, and the "
          "chapter reports both.", ""]
    open(OUT_MD, "w").write("\n".join(L) + "\n")
    print(f"{len(rows)} records; ok {st['ok']}; primary readable {len(prim_ok)}/{len(prim)}")
    print("status:", dict(st))
    print(f"-> {os.path.relpath(OUT_MD, ROOT)}")


if __name__ == "__main__":
    main()
