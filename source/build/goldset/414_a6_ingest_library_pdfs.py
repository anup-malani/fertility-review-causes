#!/usr/bin/env python3
"""
414 — A.6 (TICK-087) stage 5b: ingest the six library-retrieved PDFs and verify each is the record
it is supposed to be.

Where these came from. `412` could not reach six records by open access: five `oa_status: closed`
behind Wiley, and one 2012 working paper with no DOI whose only recorded URL had 404'd with no
Wayback snapshot. Shravan pulled all six by hand through the UChicago proxy into `~/Downloads/a6`.
That closes the gap TICK-041 never closed on B.1, where 71 of 95 are still outstanding — the
difference is that this queue was six records, not seventy-one.

Why the mapping is verified from content and not from filenames
--------------------------------------------------------------
The publisher filenames are not trustworthy and two of them are wrong. Wiley's export names the
Caldwell paper "2004" when its own watermark and DOI say 1999, and names the Wolff paper "2003"
when the watermark says 2000; the Prettner paper's filename says 2016 while the journal header
says 2017, 21(3). One file is called `paper_846.pdf` and says nothing at all. Matching on filename
would have mis-assigned at least one record, and a mis-assigned full text is worse than a missing
one: it would attach a screen decision to the wrong study.

So each PDF is identified from its extracted text, by DOI first — Wiley stamps the DOI into the
download watermark, which is the most reliable identifier available — and by a distinctive title
fragment otherwise, for the one record that has no DOI. The script refuses to write anything unless
all six map one-to-one.

Outputs the same artifacts `412` does, so the two retrieval routes are recorded in one place:
  literature/pdfs/stigma-reduction-contraception-abortion/<id>__<slug>.{pdf,txt}
  extraction/stigma-reduction-contraception-abortion-pdf-ingest-report.md
and it rewrites the rows it owns in the retrieval log.
"""
import csv, re, shutil, subprocess, sys, pathlib, unicodedata

SLUG = "stigma-reduction-contraception-abortion"
SRC = pathlib.Path.home() / "Downloads" / "a6"
PDFDIR = pathlib.Path("literature/pdfs") / SLUG
EXTR = pathlib.Path("extraction")
LOG = EXTR / f"{SLUG}-pdf-retrieval-log.csv"

# id -> (expected DOI or None, distinctive title fragment, expected year)
EXPECT = {
    "W2112312272": ("10.1111/j.1728-4457.1999.00479.x", "delayed western fertility decline", 1999),
    "W1986910339": ("10.1002/psp.480", "regional fertility differences in turkey", 2008),
    "W3121483375": ("10.1111/rode.12280", "it's a sin", 2016),
    "W4403200839": ("10.1111/padr.12669", "fertility desires and contraceptive transition", 2024),
    "W1976018943": ("10.1111/j.1728-4465.2000.00124.x", "role of couple negotiation", 2000),
    "W2187750596": (None, "sex and the single girl", 2012),
}
TITLES = {
    "W2112312272": "The Delayed Western Fertility Decline: An Examination of English-Speaking Countries",
    "W1986910339": "Regional fertility differences in Turkey: persistent high fertility in the southeast",
    "W3121483375": "It's a Sin - Contraceptive Use, Religious Beliefs, and Long-run Economic Development",
    "W4403200839": "Fertility Desires and Contraceptive Transition",
    "W1976018943": "The Role of Couple Negotiation in Unmet Need for Contraception and the Decision to Stop Childbearing in Uganda",
    "W2187750596": "Sex and the Single Girl: Cultural Persistence and the Pill",
}


def slugify(s: str) -> str:
    s = unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode()
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", s.lower())).strip("-")[:62] or "untitled"


def fold(s: str) -> str:
    s = unicodedata.normalize("NFKC", s or "")
    for a, b in [("‘", "'"), ("’", "'"), ("“", '"'), ("”", '"'),
                 ("–", "-"), ("—", "-")]:
        s = s.replace(a, b)
    return re.sub(r"\s+", " ", s).lower()


def page_count(pdf: pathlib.Path) -> int:
    p = subprocess.run(["pdfinfo", str(pdf)], capture_output=True, text=True)
    m = re.search(r"^Pages:\s+(\d+)", p.stdout or "", re.M)
    return int(m.group(1)) if m else 0


def is_scanned(pdf: pathlib.Path, words: int) -> bool:
    """True when the PDF is page images with no text layer.

    A raw word count cannot detect this. Wiley stamps a ~40-word download watermark onto every
    page, so a 35-page scan of a journal article extracts ~1,400 words of pure watermark and sails
    past any plausible minimum-length check. Both Wiley scans here did exactly that on the first
    run and were recorded as retrieved. The discriminating statistic is words PER PAGE: 37-38 for
    these two against 531 for the born-digital paper in the same batch, and 1 embedded font against
    30 (`validate-a-null-detector-on-positives` - the detector has to be calibrated on a known
    good file, not on a threshold picked from intuition).
    """
    n = page_count(pdf)
    if n == 0:
        return False
    wpp = words / n
    fonts = subprocess.run(["pdffonts", str(pdf)], capture_output=True, text=True).stdout
    n_fonts = max(0, len([l for l in fonts.splitlines()[2:] if l.strip()]))
    return wpp < 120 and n_fonts <= 3


def text_of(pdf: pathlib.Path, pages=None) -> str:
    cmd = ["pdftotext", "-q"]
    if pages:
        cmd += ["-f", "1", "-l", str(pages)]
    p = subprocess.run(cmd + [str(pdf), "-"], capture_output=True, text=True)
    return p.stdout if p.returncode == 0 else ""


def main():
    if not SRC.is_dir():
        print(f"{SRC} does not exist", file=sys.stderr)
        return 2
    pdfs = sorted(SRC.glob("*.pdf"))
    if not pdfs:
        print(f"no PDFs in {SRC}", file=sys.stderr)
        return 2

    # identify every file from its own first pages
    found, unmatched = {}, []
    for f in pdfs:
        head = fold(text_of(f, pages=3))
        hit = None
        for wid, (doi, frag, _yr) in EXPECT.items():
            if doi and doi.lower() in head:
                hit = wid
                break
        if not hit:
            for wid, (_doi, frag, _yr) in EXPECT.items():
                if frag in head:
                    hit = wid
                    break
        if hit and hit not in found:
            found[hit] = f
        else:
            unmatched.append((f.name, "duplicate match: " + hit if hit else "no match"))

    missing = [w for w in EXPECT if w not in found]
    if missing or unmatched:
        print("REFUSING TO INGEST — the mapping is not one-to-one:", file=sys.stderr)
        for w in missing:
            print(f"  unmatched record: {w} ({TITLES[w][:60]})", file=sys.stderr)
        for name, why in unmatched:
            print(f"  unmatched file:   {name[:70]} — {why}", file=sys.stderr)
        return 2

    PDFDIR.mkdir(parents=True, exist_ok=True)
    rows = []
    for wid, src in found.items():
        base = f"{wid}__{slugify(TITLES[wid])}"
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
        doi, frag, yr = EXPECT[wid]
        rows.append({"id": wid, "title": TITLES[wid][:150], "year": yr, "type": "article",
                     "doi": doi or "", "is_oa": "False", "oa_status": "closed",
                     "n_candidate_urls": "0", "source": "library_proxy",
                     "status": "retrieved" if ok else ("needs_ocr" if scanned else "corrupt"),
                     "detail": (f"UChicago proxy via Downloads/a6; matched on "
                                f"{'DOI watermark' if doi and doi.lower() in fold(text_of(pdf, 3)) else 'title fragment'}; "
                                f"{words:,} words"
                                + (f" of watermark only across {page_count(pdf)} pages - PAGE "
                                   f"IMAGES, NO TEXT LAYER, OCR REQUIRED" if scanned else "")),
                     "words": str(words), "path": str(txt) if ok else "", "is_decider": "no"})
        tag = "OK       " if ok else ("NEEDS OCR" if scanned else "CORRUPT  ")
        print(f"  {tag} {wid}  {words:,} words"
              + (f" ({words // max(1, page_count(pdf))}/page — scan)" if scanned else "")
              + f"  <- {src.name[:44]}", flush=True)

    # rewrite the rows 414 owns, leaving 412's rows intact
    old = list(csv.DictReader(LOG.open())) if LOG.exists() else []
    fields = list(old[0].keys()) if old else list(rows[0].keys())
    byid = {r["id"]: r for r in old}
    for r in rows:
        byid[r["id"]] = {k: r.get(k, "") for k in fields}
    with LOG.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        w.writerows(byid.values())

    got = sum(1 for r in byid.values() if r["status"] == "retrieved")
    rep = [f"# A.6 library PDF ingest — {len(rows)} of {len(EXPECT)}", "",
           "Generated by `source/build/goldset/414_a6_ingest_library_pdfs.py`. Do not edit by hand.",
           "",
           "These six were the residue `412` could not reach by open access: five `oa_status:",
           "closed` behind Wiley, and one 2012 working paper with no DOI whose only recorded URL",
           "had 404'd with no Wayback snapshot. Retrieved by hand through the UChicago proxy.", "",
           "**Every mapping is verified from the PDF's own text, not its filename.** The publisher",
           "filenames are wrong for two records — Wiley names the Caldwell paper 2004 when its",
           "watermark and DOI say 1999, and the Wolff paper 2003 when the watermark says 2000 —",
           "and one file is named `paper_846.pdf` and says nothing at all. A mis-assigned full text",
           "is worse than a missing one, because it attaches a screen decision to the wrong study.",
           "", f"Full-text corpus for this chapter now stands at **{got}** records.", "",
           "| id | year | DOI | words | status | matched on |", "|---|---|---|---|---|---|"]
    for r in rows:
        rep.append(f"| `{r['id']}` | {r['year']} | "
                   f"{('`' + r['doi'] + '`') if r['doi'] else '— none —'} | "
                   f"{int(r['words']):,} | "
                   f"{'**' + r['status'] + '**' if r['status'] != 'retrieved' else r['status']} | "
                   f"{'DOI watermark' if r['doi'] else 'title fragment'} |")
    ocr = [r for r in rows if r["status"] == "needs_ocr"]
    if ocr:
        rep += ["", "## Two records are page images, not text", "",
                "Wiley's scans of the older articles carry no text layer. They are **not** ingested",
                "as full text: `pdftotext` returns only the ~40-word-per-page download watermark,",
                "which is why a minimum-length check passed them on the first run. Words per page",
                "is the statistic that separates them — 37-38 against 531 for the born-digital",
                "paper in the same batch — and both also carry a single embedded font against 30.",
                "They need OCR before they can be screened.", "",
                "| id | pages | words extracted | what it is |", "|---|---|---|---|"]
        for r in ocr:
            rep.append(f"| `{r['id']}` | {r['detail'].split('across ')[-1].split(' pages')[0]} | "
                       f"{int(r['words']):,} | watermark only |")
    (EXTR / f"{SLUG}-pdf-ingest-report.md").write_text("\n".join(rep) + "\n")
    print(f"\ningested {len(rows)}; corpus now {got} records; rewrote {LOG.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
