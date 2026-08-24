#!/usr/bin/env python3
"""
178_a24_fetch_oa.py — A.24, stage 5. Fetch the open records and measure every recovery rung.

Inherits `167_a12_fetch_oa.py` and `168_a12_fetch_recovery.py`, merged into one pass because the
standing finding from A.12 is that RUNG ORDER IS CHAPTER-SPECIFIC AND MUST BE MEASURED: B.6 built its
recovery around PMC, and on A.12's literature PMC returned zero while the cheap `locations` sweep did
all the work. Keeping the rungs in separate scripts made that comparison awkward, so they run here in
one pass with a yield counted per rung.

Rung order, cheapest first:
  0  the `best_oa_location` URL OpenAlex nominates.
  1  every OTHER open location on the record — free, already in hand from 177_, and A.12's best rung.
  2  the `citation_pdf_url` meta tag on the landing page. One extra request per record.
  3  PMC via id-conversion. Expected to return ~nothing on A.24, whose literature is economics,
     sociology and communication rather than biomedicine — and that expectation is RECORDED so the
     zero, if it comes, is a measurement rather than a surprise.

**A 200 CARRYING HTML IS A BLOCKED ROUTE, NOT A CLOSED PAPER.** The PDF magic bytes are checked on
every fetch and an HTML body is recorded as `route blocked`. A.12's first pass had 84 of 88 failures
in that class, and calling them "not obtainable" would have written a false ceiling into the chapter.

Output: literature/search-logs/{slug}-fetch-log.csv
        literature/pdfs/{slug}/{WID}__{title-slug}.pdf|.txt   (gitignored)
"""
import csv, json, os, re, subprocess, time

SLUG = "dating-apps-union-formation-friction"
MAILTO = "shravanh@uchicago.edu"
UA = f"fertility-review/1.0 (mailto:{MAILTO})"
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
LOGS = os.path.join(ROOT, "literature", "search-logs")
EXTRACT = os.path.join(ROOT, "extraction")
SCREENED = os.path.join(LOGS, f"{SLUG}-screened.json")
OA = os.path.join(EXTRACT, f"{SLUG}-oa-status.json")
PDF_DIR = os.path.join(ROOT, "literature", "pdfs", SLUG)
OUT_LOG = os.path.join(LOGS, f"{SLUG}-fetch-log.csv")
OPEN = {"gold", "green", "hybrid", "bronze", "diamond"}


def slugify(t):
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", (t or "").lower()))[:60].strip("-")


def fetch(url, dest):
    """(status, note). PDF magic bytes checked: a 200 with an HTML body is a FAILURE, and it is a
    blocked route rather than a closed paper."""
    if not url:
        return "FAILED", "no url"
    try:
        r = subprocess.run(["curl", "-sL", "-m", "90", "-A", UA, "-o", dest, "-w", "%{http_code}",
                            url], capture_output=True, text=True)
        code = (r.stdout or "").strip()
    except Exception as e:
        return "FAILED", f"transport: {str(e)[:70]}"
    if not os.path.exists(dest) or os.path.getsize(dest) == 0:
        return "FAILED", f"empty body (http {code})"
    with open(dest, "rb") as fh:
        head = fh.read(5)
    if head[:4] != b"%PDF":
        os.remove(dest)
        return "FAILED", f"not a PDF — got {head[:4]!r} (http {code}); route blocked, not closed"
    return "OK", f"http {code}, {os.path.getsize(dest)//1024}kb"


def citation_pdf_url(landing):
    if not landing:
        return None
    try:
        html = subprocess.run(["curl", "-sL", "-m", "45", "-A", UA, landing],
                              capture_output=True, text=True).stdout[:400000]
    except Exception:
        return None
    m = re.search(r'<meta[^>]+name=["\']citation_pdf_url["\'][^>]+content=["\']([^"\']+)', html, re.I)
    if not m:
        m = re.search(r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+name=["\']citation_pdf_url["\']', html, re.I)
    return m.group(1) if m else None


def pmc_pdf(doi):
    """PMC via id-conversion. Expected to return nothing on this literature; measured anyway."""
    if not doi:
        return None
    try:
        out = subprocess.run(["curl", "-s", "-m", "40", "-A", UA,
                              "https://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/?format=json&ids="
                              + doi], capture_output=True, text=True).stdout
        d = json.loads(out)
    except Exception:
        return None
    for rec in d.get("records", []):
        if rec.get("pmcid"):
            return f"https://www.ncbi.nlm.nih.gov/pmc/articles/{rec['pmcid']}/pdf/"
    return None


def extract_text(pdf, txt):
    for cmd in (["pdftotext", "-q", pdf, txt], ["/opt/homebrew/bin/pdftotext", "-q", pdf, txt]):
        try:
            subprocess.run(cmd, capture_output=True, timeout=120)
        except Exception:
            continue
        if os.path.exists(txt) and os.path.getsize(txt) > 500:
            return "OK", f"{os.path.getsize(txt)//1024}kb text"
        if os.path.exists(txt):
            return "NO_TEXT_LAYER", "under 500 bytes — likely a scan"
    return "EXTRACT_FAILED", "pdftotext unavailable or errored"


def main():
    oa = json.load(open(OA))
    meta = {r["id"]: r for r in json.load(open(SCREENED))}
    os.makedirs(PDF_DIR, exist_ok=True)
    rows = []
    rung_yield = {0: 0, 1: 0, 2: 0, 3: 0}
    n_ok = n_fail = n_notext = 0
    blocked = 0

    targets = [w for w, s in oa.items() if s.get("status") in OPEN and s.get("url")]
    print(f"attempting {len(targets)} nominally-open records of {len(oa)} on the wantlist")
    for wid in targets:
        s, m = oa[wid], meta.get(wid, {})
        base = f"{wid}__{slugify(m.get('title'))}"
        pdf = os.path.join(PDF_DIR, base + ".pdf")
        txt = os.path.join(PDF_DIR, base + ".txt")
        if os.path.exists(pdf) and os.path.getsize(pdf) > 0:
            fstat, fnote, rung = "CACHED", "already on disk", -1
        else:
            fstat, fnote = fetch(s.get("pdf_url") or s.get("url"), pdf)
            rung = 0
            if fstat != "OK":
                if "route blocked" in fnote:
                    blocked += 1
                for alt in (s.get("alt_pdfs") or []):
                    if alt and alt != (s.get("pdf_url") or s.get("url")):
                        fstat, fnote = fetch(alt, pdf)
                        if fstat == "OK":
                            rung, fnote = 1, "rung 1 (alternate OA location): " + fnote
                            break
            if fstat != "OK":
                for land in ([s.get("url")] + (s.get("alt_landing") or [])):
                    cand = citation_pdf_url(land)
                    if cand:
                        fstat, fnote = fetch(cand, pdf)
                        if fstat == "OK":
                            rung, fnote = 2, "rung 2 (citation_pdf_url): " + fnote
                            break
            if fstat != "OK":
                cand = pmc_pdf(s.get("doi") or m.get("doi"))
                if cand:
                    fstat, fnote = fetch(cand, pdf)
                    if fstat == "OK":
                        rung, fnote = 3, "rung 3 (PMC): " + fnote
        if fstat in ("OK", "CACHED"):
            tstat, tnote = extract_text(pdf, txt)
            n_ok += 1
            if rung >= 0:
                rung_yield[rung] += 1
            if tstat != "OK":
                n_notext += 1
        else:
            tstat, tnote = "-", "-"
            n_fail += 1
        rows.append(dict(id=wid, doi=s.get("doi") or m.get("doi"), cell=m.get("cell"),
                         year=m.get("year"), title=(m.get("title") or "")[:90],
                         oa_status=s.get("status"), rung=rung, fetch=fstat, fetch_note=fnote,
                         text=tstat, text_note=tnote, url=s.get("url")))
        print(f"  {fstat:<7} r{rung:<2} {tstat:<14} {(m.get('title') or '')[:52]}")
        time.sleep(0.1)

    with open(OUT_LOG, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)
    print(f"\nfetched={n_ok} failed={n_fail} no_text_layer={n_notext} html_blocked={blocked}")
    print(f"rung yields: 0(best_oa)={rung_yield[0]} 1(alt_locations)={rung_yield[1]} "
          f"2(citation_pdf_url)={rung_yield[2]} 3(PMC)={rung_yield[3]}")
    print(f"-> {os.path.relpath(OUT_LOG, ROOT)}")


if __name__ == "__main__":
    main()
