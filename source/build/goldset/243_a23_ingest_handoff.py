#!/usr/bin/env python3
"""
243_a23_ingest_handoff.py — A.23, stage 5g. Install hand-retrieved PDFs under the naming convention.

The `W2_library_proxy` worklist ends in a person with institutional access, and what comes back is a
directory of files named by the publisher — `185chu.pdf`, `617kucheva.pdf`, a Wiley export with the
journal name in it. Renaming those by hand is exactly the step that later makes a chapter
unreproducible, so it is done here instead.

**EACH FILE IS MATCHED TO A RECORD BY ITS OWN CONTENT, NOT BY ITS FILENAME.** The mapping is declared
below as (file, OpenAlex id) pairs, and then CHECKED: the PDF's extracted text must contain enough of
the record's title for the match to stand. A hand-delivered file placed against the wrong record is
a silent corruption of the extraction table, and the filename a publisher chooses carries no
information that would catch it. A pair that fails the check is refused and named, not installed.

It also asserts the PDF magic bytes and a word floor, because a "PDF" that is a login page and a
scanned image with no text layer both arrive looking like a successful retrieval.

Usage:  python3 243_a23_ingest_handoff.py [source_dir]     (default ~/Downloads/a23)
Output: literature/pdfs/{slug}/{WID}__{title-slug}.pdf
        literature/search-logs/{slug}-handoff-ingest-log.md
"""
import json, os, re, shutil, sys, unicodedata

SLUG = "co-residence-parents-household-delay"
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
OA = os.path.join(ROOT, "extraction", f"{SLUG}-oa-status.json")
PDF_DIR = os.path.join(ROOT, "literature", "pdfs", SLUG)
PROV = os.path.join(ROOT, "extraction", f"{SLUG}-fetch-provenance.json")
OUT_MD = os.path.join(ROOT, "literature", "search-logs", f"{SLUG}-handoff-ingest-log.md")

MIN_WORDS = 800
TITLE_OVERLAP = 0.60      # share of the record's title tokens that must appear in the PDF text

# Declared by the person who fetched them. The filenames are the publisher's; the ids are ours.
PAIRS = [
    ("185chu.pdf", "W2099331743", "W2_library_proxy"),
    ("617kucheva.pdf", "W2791040281", "W2_library_proxy"),
    ("J of Money Credit Banking - 2017 - LAEVEN - Waking Up from the American Dream  On the "
     "Experience of Young Americans during.pdf", "W3125671386", "W2_library_proxy"),
    ("a23_W4385496510.pdf", "W4385496510", "W1_browser"),
]


def fold(s):
    s = unicodedata.normalize("NFKD", (s or "").lower())
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]+", " ", s).strip()


def slugify(t):
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", (t or "").lower()))[:60].strip("-")


def pdf_text(path):
    try:
        import fitz
        with fitz.open(path) as doc:
            return "\n".join(p.get_text() for p in doc[:6])
    except Exception:
        return ""


def main():
    src_dir = os.path.expanduser(sys.argv[1] if len(sys.argv) > 1 else "~/Downloads/a23")
    meta = {r["id"]: r for r in json.load(open(OA))}
    prov = json.load(open(PROV)) if os.path.exists(PROV) else {}
    os.makedirs(PDF_DIR, exist_ok=True)

    rows = []
    for fname, wid, worklist in PAIRS:
        p = os.path.join(src_dir, fname)
        r = dict(file=fname, id=wid, worklist=worklist, status="", note="",
                 title=(meta.get(wid, {}).get("title") or ""), words=0, overlap=0.0)
        if not os.path.exists(p):
            r.update(status="missing", note="not found in the handoff directory")
            rows.append(r); continue
        if wid not in meta:
            r.update(status="unknown_record", note="id is not in the stage-5a wantlist")
            rows.append(r); continue
        with open(p, "rb") as fh:
            if fh.read(4) != b"%PDF":
                r.update(status="not_a_pdf", note="magic bytes are not %PDF — a login page or an "
                                                  "error document saved with a .pdf name")
                rows.append(r); continue
        text = pdf_text(p)
        words = len(text.split())
        toks = [t for t in fold(r["title"]).split() if len(t) > 2]
        ft = fold(text)
        hit = sum(1 for t in set(toks) if t in ft)
        overlap = hit / len(set(toks)) if toks else 0.0
        r.update(words=words, overlap=overlap)
        if words < MIN_WORDS:
            r.update(status="no_text_layer",
                     note=f"{words} words in the first pages — a scan, and OCR is a separate job")
            rows.append(r); continue
        if overlap < TITLE_OVERLAP:
            r.update(status="title_mismatch",
                     note=f"only {overlap:.0%} of the record's title tokens appear in the file; "
                          "REFUSED rather than installed")
            rows.append(r); continue
        dest = os.path.join(PDF_DIR, f"{wid}__{slugify(r['title'])}.pdf")
        shutil.copy2(p, dest)
        prov[wid] = dict(rung=f"handoff:{worklist}", url="", outcome="pdf",
                         note=f"hand-retrieved, delivered as {fname}")
        r.update(status="installed", note=os.path.basename(dest))
        rows.append(r)

    json.dump(prov, open(PROV, "w"), indent=2, sort_keys=True)

    ok = [r for r in rows if r["status"] == "installed"]
    L = [f"# Stage 5g handoff ingest — {SLUG} (A.23)", "",
         "**Generated by:** `source/build/goldset/243_a23_ingest_handoff.py`", "",
         f"**{len(ok)} of {len(rows)} hand-retrieved files installed.** Source directory: "
         f"`{src_dir}`.", "",
         "The `W2_library_proxy` worklist ends in a person with institutional access, and what comes "
         "back is named by the publisher. Renaming by hand is the step that makes a chapter "
         "unreproducible later, so it happens here.", "",
         "**Each file is matched to its record by CONTENT.** The declared pairing is checked against "
         f"the PDF's own text: at least {TITLE_OVERLAP:.0%} of the record's title tokens must appear "
         "in the first pages. A file placed against the wrong record silently corrupts the "
         "extraction table, and a publisher's filename carries nothing that would catch it.", "",
         "| File | Record | Worklist | Words | Title overlap | Status |",
         "|---|---|---|---|---|---|"]
    for r in rows:
        L.append(f"| `{r['file'][:44]}` | `{r['id']}` | `{r['worklist']}` | {r['words']:,} | "
                 f"{r['overlap']:.0%} | **{r['status']}** |")
    L += ["", "## What each unlocks", ""]
    NOTE = {
        "W2099331743": "**The direction reported in §6.2 rests on this abstract.** Chu, Xie and Yu "
                       "treat co-residence and labour supply as jointly determined with the timing "
                       "of a first birth; correcting for that reverses the effect. The chapter has "
                       "the direction and no magnitude.",
        "W3125671386": "**The only design estimating home ownership, household formation and "
                       "fertility under one instrument** — what a decomposition of the A.23 / C.2.c "
                       "non-additivity requires.",
        "W2791040281": "**Administrative allocation of dwellings** — the scope's design 3, in the "
                       "arm with almost no identified evidence.",
        "W4385496510": "A Wall 1 record carrying both boundary variables in one model. Recovered "
                       "from the browser pass after all: the download landed, in a directory the "
                       "session had already looked in and found empty.",
    }
    for r in ok:
        L += [f"- `{r['id']}` — {NOTE.get(r['id'], '')}"]
    bad = [r for r in rows if r["status"] != "installed"]
    if bad:
        L += ["", "## Refused", ""] + [f"- `{r['file']}` → `{r['status']}`: {r['note']}" for r in bad]
    L += ["", "Provenance for each is written as `handoff:{worklist}` so the cumulative rung table "
          "shows what a human delivered against what a script did.", ""]
    open(OUT_MD, "w").write("\n".join(L) + "\n")
    for r in rows:
        print(f"  {r['status']:16s} overlap={r['overlap']:.0%} words={r['words']:>6,}  {r['file'][:50]}")
    print(f"\ninstalled {len(ok)}/{len(rows)} -> {os.path.relpath(OUT_MD, ROOT)}")


if __name__ == "__main__":
    main()
