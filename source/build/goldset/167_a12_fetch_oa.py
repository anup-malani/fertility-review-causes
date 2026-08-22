#!/usr/bin/env python3
"""
167_a12_fetch_oa.py — A.12, stage 5. Fetch the openly-available full texts and extract their text.

Reads the OA status written by 166 and fetches every record marked open into
`literature/pdfs/{slug}/{WID}__{title-slug}.pdf` (gitignored), then extracts text to a sibling `.txt`
so extraction can be hand-coded against a searchable document.

Discipline, inherited from `140_b6_fetch_oa.py` and unchanged because it keeps being right:
  * A fetch that fails is logged as FAILED and never as "closed" or "unavailable". That distinction
    is the whole reason 166 measured OA status separately from fetch success: a publisher blocking a
    scripted download has not made the paper closed, it has made THIS ROUTE closed, and the record
    belongs on the human procurement list rather than in a "not obtainable" bucket.
  * A downloaded file that is not a PDF is a failure, not a fetch. Publishers routinely return a
    200-status HTML interstitial for a blocked download; writing it to disk as `.pdf` produces a file
    that ingest reads as an empty paper. Magic bytes are checked.
  * Text-extraction failure is recorded separately from fetch failure, because a scanned PDF with no
    text layer is retrieved but not readable and the two need different remedies.

Output: literature/pdfs/{slug}/*.pdf and *.txt   (gitignored)
        extraction/{slug}-pdf-retrieval-log.csv
"""
import csv, json, os, re, subprocess, sys

SLUG = "twinning-multiple-births"
MAILTO = "shravanh@uchicago.edu"
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) fertility-review/1.0 "
      f"(mailto:{MAILTO})")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
EXTRACT = os.path.join(ROOT, "extraction")
LOGS = os.path.join(ROOT, "literature", "search-logs")
PDF_DIR = os.path.join(ROOT, "literature", "pdfs", SLUG)
OA = os.path.join(EXTRACT, f"{SLUG}-oa-status.json")
SCREENED = os.path.join(LOGS, f"{SLUG}-screened.json")
OUT_LOG = os.path.join(EXTRACT, f"{SLUG}-pdf-retrieval-log.csv")
OPEN = {"gold", "green", "hybrid", "bronze", "diamond"}


def slugify(t):
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", (t or "").lower()))[:60].strip("-")


def fetch(url, dest):
    """Returns (status, note). PDF magic bytes checked: a 200 with an HTML body is a FAILURE."""
    try:
        r = subprocess.run(["curl", "-sL", "-m", "90", "-A", UA, "-o", dest, "-w", "%{http_code}",
                            url], capture_output=True, text=True)
        code = (r.stdout or "").strip()
    except Exception as e:
        return "FAILED", f"transport: {str(e)[:80]}"
    if not os.path.exists(dest) or os.path.getsize(dest) == 0:
        return "FAILED", f"empty body (http {code})"
    with open(dest, "rb") as fh:
        head = fh.read(5)
    if head[:4] != b"%PDF":
        os.remove(dest)
        return "FAILED", f"not a PDF — publisher returned {head[:4]!r} (http {code}); route blocked, not closed"
    return "OK", f"http {code}, {os.path.getsize(dest)//1024}kb"


def extract_text(pdf, txt):
    for cmd in (["pdftotext", "-q", pdf, txt], ["/opt/homebrew/bin/pdftotext", "-q", pdf, txt]):
        try:
            subprocess.run(cmd, capture_output=True, timeout=120)
        except Exception:
            continue
        if os.path.exists(txt) and os.path.getsize(txt) > 500:
            return "OK", f"{os.path.getsize(txt)//1024}kb text"
        if os.path.exists(txt):
            return "NO_TEXT_LAYER", "extracted but under 500 bytes — likely a scan"
    return "EXTRACT_FAILED", "pdftotext unavailable or errored"


def main():
    oa = json.load(open(OA))
    meta = {r["id"]: r for r in json.load(open(SCREENED))}
    os.makedirs(PDF_DIR, exist_ok=True)
    rows, n_ok, n_fail, n_notext = [], 0, 0, 0
    targets = [(w, s) for w, s in oa.items() if s.get("status") in OPEN and s.get("url")]
    print(f"attempting {len(targets)} open records of {len(oa)} on the wantlist")
    for wid, st in targets:
        m = meta.get(wid, {})
        base = f"{wid}__{slugify(m.get('title'))}"
        pdf = os.path.join(PDF_DIR, base + ".pdf")
        txt = os.path.join(PDF_DIR, base + ".txt")
        if os.path.exists(pdf) and os.path.getsize(pdf) > 0:
            fstat, fnote = "CACHED", "already on disk"
        else:
            fstat, fnote = fetch(st["url"], pdf)
        if fstat in ("OK", "CACHED"):
            tstat, tnote = extract_text(pdf, txt)
            n_ok += 1
            if tstat != "OK":
                n_notext += 1
        else:
            tstat, tnote = "-", "-"
            n_fail += 1
        rows.append(dict(id=wid, doi=m.get("doi"), cell=m.get("cell"), year=m.get("year"),
                         title=(m.get("title") or "")[:90], oa_status=st["status"],
                         fetch=fstat, fetch_note=fnote, text=tstat, text_note=tnote,
                         url=st.get("url")))
        print(f"  {fstat:<7} {tstat:<14} {(m.get('title') or '')[:58]}")
    with open(OUT_LOG, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)
    print(f"\nfetched={n_ok} failed={n_fail} no_text_layer={n_notext}")
    print(f"-> {os.path.relpath(OUT_LOG, ROOT)}")
    print(f"-> {os.path.relpath(PDF_DIR, ROOT)}/")


if __name__ == "__main__":
    main()
