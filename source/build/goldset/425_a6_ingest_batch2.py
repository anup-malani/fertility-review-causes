#!/usr/bin/env python3
"""
425 — A.6 (TICK-087): ingest the second batch of library PDFs — the two gate records and one
call-8 candidate.

These three close, or fail to close, the two conditions on which `PRIMARY_NORM_FERTILITY = 0`
currently rests:

  W2086018683  Phillips et al. 1996, *The Long-term Demographic Role of Community-based Family
               Planning in Rural Bangladesh* — **Matlab**. The A.5 gate: the canonical A.5
               quasi-experiment with a demographic outcome, and the one design that could plausibly
               dose a norm component separately.
  W1968910820  Kelly and Cutright 1983, *A Time Series Analysis of Swedish Illegitimacy Rates,
               1911-1974*, Sociological Focus 16(2). The call-8 gate, and its abstract already
               settles half the question: the outcome is **age-specific illegitimacy rates**, which
               is a fertility rate for the unmarried subpopulation and therefore convertible, and
               the design is a multivariate regression on annual change. What remains is whether
               any regressor is a normative construct.
  W7124168863  Xu 2026, *Religion Affects Whether US Women Marry Early…*, JSSR — the hybrid-OA
               call-8 candidate.

Verification is by content, not filename, for the reason `414` recorded: one of these arrived as
`EBSCO-FullText-09_17_2026.pdf` and says nothing in its name, and Wiley's own exports misdated two
of the previous batch. A mis-assigned full text is worse than a missing one because it attaches a
screen decision to the wrong study. Each file is identified from its extracted text — by DOI where
the publisher stamps one, by a distinctive title fragment otherwise — and the script refuses to
write unless the mapping is one-to-one.

The scanned-PDF check from `414` is retained: words per page against a calibrated floor, so a
page-image scan cannot be banked as text on the strength of a watermark.
"""
import csv, re, shutil, subprocess, sys, pathlib, unicodedata

SLUG = "stigma-reduction-contraception-abortion"
SRC = pathlib.Path.home() / "Downloads" / "a6"
PDFDIR = pathlib.Path("literature/pdfs") / SLUG
EXTR = pathlib.Path("extraction")
LOG = EXTR / f"{SLUG}-pdf-retrieval-log.csv"

EXPECT = {
    "W2086018683": (None, "long-term demographic role of community-based family planning", 1996,
                    "The Long-term Demographic Role of Community-based Family Planning in Rural "
                    "Bangladesh"),
    "W1968910820": (None, "time series analysis of swedish illegitimacy", 1983,
                    "A Time Series Analysis of Swedish Illegitimacy Rates 1911-1974"),
    "W7124168863": ("10.1111/jssr.70016", "religion affects whether us women marry early", 2026,
                    "Religion Affects Whether US Women Marry Early Without Cohabiting or Having a "
                    "Nonmarital Birth"),
}
_FOLD = {0x2018: "'", 0x2019: "'", 0x201c: '"', 0x201d: '"', 0x2013: "-", 0x2014: "-",
         0x2026: "..."}


def fold(s):
    s = unicodedata.normalize("NFKC", s or "").translate(_FOLD)
    return re.sub(r"\s+", " ", s).strip().lower()


def slugify(s):
    s = unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode()
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", s.lower())).strip("-")[:62] or "untitled"


def text_of(pdf, pages=None):
    cmd = ["pdftotext", "-q"] + (["-f", "1", "-l", str(pages)] if pages else [])
    p = subprocess.run(cmd + [str(pdf), "-"], capture_output=True, text=True)
    return p.stdout if p.returncode == 0 else ""


def page_count(pdf):
    out = subprocess.run(["pdfinfo", str(pdf)], capture_output=True, text=True).stdout
    m = re.search(r"^Pages:\s+(\d+)", out or "", re.M)
    return int(m.group(1)) if m else 0


def is_scanned(pdf, words):
    n = page_count(pdf)
    if n == 0:
        return False
    fonts = subprocess.run(["pdffonts", str(pdf)], capture_output=True, text=True).stdout
    n_fonts = len([l for l in fonts.splitlines()[2:] if l.strip()])
    return (words / n) < 120 and n_fonts <= 3


def main():
    pdfs = sorted(SRC.glob("*.pdf"))
    found, unmatched = {}, []
    for f in pdfs:
        head = fold(text_of(f, pages=3))
        hit = None
        for wid, (doi, frag, _y, _t) in EXPECT.items():
            if doi and doi.lower() in head:
                hit = wid
                break
        if not hit:
            for wid, (_d, frag, _y, _t) in EXPECT.items():
                if frag in head:
                    hit = wid
                    break
        if hit and hit not in found:
            found[hit] = f
        elif hit:
            unmatched.append((f.name, f"second file matching {hit}"))

    missing = [w for w in EXPECT if w not in found]
    if missing or unmatched:
        print("REFUSING TO INGEST — mapping is not one-to-one:", file=sys.stderr)
        for w in missing:
            print(f"  unmatched record: {w} ({EXPECT[w][3][:56]})", file=sys.stderr)
        for n, why in unmatched:
            print(f"  unmatched file:   {n[:64]} — {why}", file=sys.stderr)
        return 2

    PDFDIR.mkdir(parents=True, exist_ok=True)
    rows = []
    for wid, src in found.items():
        doi, _frag, yr, title = EXPECT[wid]
        base = f"{wid}__{slugify(title)}"
        pdf, txt = PDFDIR / f"{base}.pdf", PDFDIR / f"{base}.txt"
        shutil.copy2(src, pdf)
        body = text_of(pdf)
        words = len(body.split())
        scanned = is_scanned(pdf, words)
        ok = words >= 500 and not scanned
        if ok:
            txt.write_text(body)
        else:
            txt.unlink(missing_ok=True)
        rows.append({"id": wid, "title": title[:150], "year": yr, "type": "article",
                     "doi": doi or "", "is_oa": "False", "oa_status": "closed",
                     "n_candidate_urls": "0", "source": "library_proxy_batch2",
                     "status": "retrieved" if ok else ("needs_ocr" if scanned else "corrupt"),
                     "detail": (f"UChicago proxy via Downloads/a6, batch 2; matched from content; "
                                f"{words:,} words"
                                + (f" of watermark only across {page_count(pdf)} pages - OCR "
                                   f"REQUIRED" if scanned else "")),
                     "words": str(words), "path": str(txt) if ok else "", "is_decider": "no"})
        tag = "OK       " if ok else ("NEEDS OCR" if scanned else "CORRUPT  ")
        print(f"  {tag} {wid}  {words:,} words  <- {src.name[:46]}", flush=True)

    old = list(csv.DictReader(LOG.open())) if LOG.exists() else []
    fields = list(old[0].keys()) if old else list(rows[0].keys())
    byid = {r["id"]: r for r in old}
    for r in rows:
        byid[r["id"]] = {k: r.get(k, "") for k in fields}
    with LOG.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        w.writerows(byid.values())
    print(f"\ningested {len(rows)}; full-text corpus now "
          f"{sum(1 for r in byid.values() if r['status'] == 'retrieved')} records")
    return 0


if __name__ == "__main__":
    sys.exit(main())
