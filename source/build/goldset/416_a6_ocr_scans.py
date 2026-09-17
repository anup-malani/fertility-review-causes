#!/usr/bin/env python3
"""
416 — A.6 (TICK-087) stage 5c: OCR the two Wiley page-image scans so they can be screened.

Why this exists. `414` held two records at `needs_ocr`: Wiley's scans of Caldwell (PDR 1999) and
Wolff (Studies in Family Planning 2000) are page images with no text layer. `pdftotext` returns
only the ~40-word-per-page download watermark, which is why a naive minimum-length check passed
them as retrieved on the first attempt. Wolff is the record whose outcome may be parity rather than
contraceptive use, so leaving it unread would leave the chapter's central absence claim resting on
an unopened file.

`--force-ocr`, deliberately. The PDFs *do* carry a text layer — the watermark — so `--skip-text`
would skip every page and `--redo-ocr` expects real prior OCR. `--force-ocr` rasterises and
re-recognises everything, discarding the watermark layer. The watermark itself gets OCR'd along with
the page, which is harmless: it adds a constant ~40 words per page that the verification below
accounts for by requiring a large multiple of it.

Verification, calibrated rather than guessed. OCR can fail quietly — a skewed or low-DPI scan
yields a page of plausible-looking garbage. So the same words-per-page statistic that *detected* the
problem is used to confirm the fix, against the born-digital paper in the same batch as the known
good case: `W3121483375` runs 531 words/page. A scan that comes out below 200 words/page after OCR
is reported as a failure, not banked as text (`validate-a-null-detector-on-positives`).

The original downloads are never overwritten. OCR output goes to `<base>.ocr.pdf` and the extracted
text to `<base>.txt`, so the proxy-retrieved file stays exactly as Wiley served it.
"""
import csv, re, subprocess, sys, pathlib

SLUG = "stigma-reduction-contraception-abortion"
PDFDIR = pathlib.Path("literature/pdfs") / SLUG
EXTR = pathlib.Path("extraction")
LOG = EXTR / f"{SLUG}-pdf-retrieval-log.csv"
MIN_WPP = 200          # the born-digital paper in this batch runs 531; the scans ran 37-38
CALIBRATION = ("W3121483375", 531)


def page_count(pdf: pathlib.Path) -> int:
    out = subprocess.run(["pdfinfo", str(pdf)], capture_output=True, text=True).stdout
    m = re.search(r"^Pages:\s+(\d+)", out or "", re.M)
    return int(m.group(1)) if m else 0


def words_of(pdf: pathlib.Path) -> tuple[str, int]:
    p = subprocess.run(["pdftotext", "-q", str(pdf), "-"], capture_output=True, text=True)
    body = p.stdout if p.returncode == 0 else ""
    return body, len(body.split())


def main():
    if not LOG.exists():
        print(f"{LOG} missing", file=sys.stderr)
        return 2
    rows = list(csv.DictReader(LOG.open()))
    fields = list(rows[0].keys())
    targets = [r for r in rows if r["status"] == "needs_ocr"]
    if not targets:
        print("nothing at needs_ocr — already OCR'd or nothing to do")
        return 0

    # calibration: confirm the known-good file still reads as good, so MIN_WPP means something
    cal_id, cal_expect = CALIBRATION
    cal = next((p for p in PDFDIR.glob(f"{cal_id}*.pdf") if ".ocr." not in p.name), None)
    if cal:
        _, w = words_of(cal)
        wpp = w // max(1, page_count(cal))
        print(f"calibration: {cal_id} reads {wpp} words/page (expected ~{cal_expect}); "
              f"threshold is {MIN_WPP}", flush=True)
        if wpp < MIN_WPP:
            print("  calibration file is below the threshold — the threshold is wrong, "
                  "refusing to run", file=sys.stderr)
            return 2

    results = []
    for r in targets:
        wid = r["id"]
        src = next((p for p in PDFDIR.glob(f"{wid}*.pdf") if ".ocr." not in p.name), None)
        if not src:
            print(f"  MISSING PDF for {wid}", file=sys.stderr)
            results.append((wid, False, "source pdf not found", 0, 0))
            continue
        ocr = src.with_suffix(".ocr.pdf")
        txt = src.with_suffix(".txt")
        n = page_count(src)
        print(f"  OCR {wid} ({n} pages) …", flush=True)
        p = subprocess.run(["ocrmypdf", "--force-ocr", "-l", "eng", "--quiet",
                            str(src), str(ocr)], capture_output=True, text=True)
        if p.returncode != 0 or not ocr.exists():
            print(f"    FAILED: {(p.stderr or '').strip()[:160]}", file=sys.stderr)
            results.append((wid, False, f"ocrmypdf exit {p.returncode}", n, 0))
            continue
        body, words = words_of(ocr)
        wpp = words // max(1, n)
        if wpp < MIN_WPP:
            ocr.unlink(missing_ok=True)
            print(f"    FAILED verification: {words:,} words, {wpp}/page < {MIN_WPP}",
                  file=sys.stderr)
            results.append((wid, False, f"{words} words, {wpp}/page below threshold", n, words))
            continue
        txt.write_text(body)
        print(f"    OK {words:,} words, {wpp}/page", flush=True)
        results.append((wid, True, f"OCR'd, {words:,} words, {wpp}/page", n, words))

    byid = {r["id"]: r for r in rows}
    for wid, ok, detail, n, words in results:
        row = byid[wid]
        row["status"] = "retrieved" if ok else "ocr_failed"
        row["words"] = str(words)
        row["source"] = "library_proxy+ocr"
        row["detail"] = (f"page-image scan, {n} pages; " + detail)
        row["path"] = (str(next(PDFDIR.glob(f"{wid}*.txt"))) if ok else "")
    with LOG.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        w.writerows(byid.values())

    ok_n = sum(1 for _w, ok, *_ in results if ok)
    corpus = sum(1 for r in byid.values() if r["status"] == "retrieved")
    rep = [f"# A.6 OCR of the page-image scans — {ok_n} of {len(results)}", "",
           "Generated by `source/build/goldset/416_a6_ocr_scans.py`. Do not edit by hand.", "",
           "Wiley's scans of the two oldest records carry no text layer. `pdftotext` returned only",
           "the ~40-word-per-page download watermark, which is why a minimum-length check banked",
           "them as retrieved on the first attempt. `--force-ocr` is required rather than",
           "`--skip-text`, because the watermark *is* a text layer and would cause every page to be",
           "skipped.", "",
           f"Verification is calibrated, not guessed: the born-digital paper in the same batch",
           f"(`{cal_id}`) runs ~{cal_expect} words/page, so anything below **{MIN_WPP}** words/page",
           "after OCR is reported as a failure rather than written to disk.", "",
           f"**Full-text corpus for this chapter now stands at {corpus} of 8.**", "",
           "| id | pages | words after OCR | words/page | result |", "|---|---|---|---|---|"]
    for wid, ok, detail, n, words in results:
        rep.append(f"| `{wid}` | {n} | {words:,} | {words // max(1, n)} | "
                   f"{'OCR succeeded' if ok else '**' + detail + '**'} |")
    rep += ["", "Originals are untouched: OCR output is written to `<base>.ocr.pdf` and the text to",
            "`<base>.txt`, so the proxy-retrieved PDF remains exactly as the publisher served it."]
    (EXTR / f"{SLUG}-ocr-report.md").write_text("\n".join(rep) + "\n")
    print(f"\nOCR'd {ok_n}/{len(results)}; corpus now {corpus}/8; rewrote {LOG.name}")
    return 0 if ok_n == len(results) else 1


if __name__ == "__main__":
    sys.exit(main())
