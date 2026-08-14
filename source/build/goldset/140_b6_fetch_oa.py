#!/usr/bin/env python3
"""
140_b6_fetch_oa.py — B.6, stage 5. Fetch the openly-available full texts and extract their text.

Reads the OA status file written by 139 and fetches every record marked open, into the house path
`literature/pdfs/{slug}/{WID}__{title-slug}.pdf` (gitignored), then extracts text to a sibling `.txt`
so extraction can be hand-coded against a searchable document.

Discipline:
  * A fetch that fails is logged as FAILED and never as "closed" or "unavailable". The distinction is
    the whole reason 129 measured OA status separately from fetch success: a publisher that blocks a
    scripted download has not made the paper closed, it has made THIS ROUTE closed, and the record
    belongs on the human procurement list rather than in a "not obtainable" bucket.
  * A downloaded file that is not a PDF is a failure, not a fetch. Publishers commonly return a
    200-status HTML interstitial for a blocked download; writing it to disk as a .pdf produces a file
    that ingest reads as an empty paper. The magic bytes are checked.
  * Text extraction failure is recorded separately from fetch failure, because a scanned PDF with no
    text layer is retrieved but not readable, and the two need different remedies.

Output: literature/pdfs/{slug}/*.pdf and *.txt   (gitignored)
        extraction/{slug}-pdf-retrieval-log.csv
"""
import csv, json, os, re, subprocess, time

SLUG = "microplastics-pfas-reproductive"
MAILTO = "shravanh@uchicago.edu"
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) fertility-review/1.0 "
      f"(mailto:{MAILTO})")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
EXTRACT = os.path.join(ROOT, "extraction")
LOGS = os.path.join(ROOT, "literature", "search-logs")
PDF_DIR = os.path.join(ROOT, "literature", "pdfs", SLUG)
OA = os.path.join(EXTRACT, f"{SLUG}-oa-status.json")
GATE = os.path.join(EXTRACT, f"{SLUG}-ra-gate.csv")
TIERS = os.path.join(LOGS, f"{SLUG}-screen-tiers.json")
OUT_LOG = os.path.join(EXTRACT, f"{SLUG}-pdf-retrieval-log.csv")

OPEN = {"gold", "green", "hybrid", "bronze", "diamond"}
PRIMARY_CELLS = {"PRIMARY_EXPOSURE_TO_FERTILITY", "PRIMARY_MALE_FECUNDITY", "PRIMARY_HIGH_EXPOSURE"}
INPUT_CELLS = {"SEMEN_PARAMETER", "OVARIAN_PARAMETER"}


def slugify(t):
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", (t or "").lower()))[:60].strip("-")


def fetch(url, dest):
    """Returns (status, note). PDF magic bytes are checked: a 200 with an HTML body is a FAILURE."""
    try:
        r = subprocess.run(["curl", "-sL", "-m", "90", "-A", UA, "-o", dest, "-w", "%{http_code}",
                            url], capture_output=True, text=True)
        code = (r.stdout or "").strip()
    except Exception as e:
        return "FAILED", f"transport: {str(e)[:80]}"
    if not os.path.exists(dest) or os.path.getsize(dest) < 2000:
        if os.path.exists(dest):
            os.remove(dest)
        return "FAILED", f"http {code}, body too small"
    with open(dest, "rb") as fh:
        head = fh.read(5)
    if head[:4] != b"%PDF":
        os.remove(dest)
        return "FAILED", f"http {code}, not a PDF (publisher interstitial or paywall page)"
    return "OK", f"http {code}, {os.path.getsize(dest) // 1024} KB"


def oa_locations(wid):
    """Every OA pdf_url OpenAlex knows for a work, not just the best one.

    `best_oa_location` is a single publisher-side link, and publishers are exactly who returns 403 to
    a script. The repository copies further down the location list usually do not."""
    url = (f"https://api.openalex.org/works/{wid}?select=locations&mailto={MAILTO}")
    try:
        d = json.loads(subprocess.run(["curl", "-s", "-m", "30", "-A", UA, url],
                                      capture_output=True, text=True).stdout)
    except Exception:
        return []
    out = []
    for loc in (d.get("locations") or []):
        if loc.get("pdf_url"):
            src = (loc.get("source") or {}) or {}
            out.append((loc["pdf_url"], src.get("display_name") or "repository"))
    return out


def europepmc_text(doi, txt_path):
    """Europe PMC full text by DOI. This literature is biomedical and largely PubMed-indexed, so the
    PMC open-access subset reaches records the publisher route refuses. Returns (status, note)."""
    if not doi:
        return "FAILED", "no doi"
    q = ('https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=DOI:%22'
         + doi + '%22&resultType=core&format=json&pageSize=1')
    try:
        d = json.loads(subprocess.run(["curl", "-s", "-m", "40", "-A", UA, q],
                                      capture_output=True, text=True).stdout)
        hits = ((d.get("resultList") or {}).get("result") or [])
    except Exception as e:
        return "FAILED", f"epmc search: {str(e)[:60]}"
    if not hits:
        return "FAILED", "not in Europe PMC"
    h = hits[0]
    pmcid = h.get("pmcid")
    if not pmcid or h.get("isOpenAccess") != "Y":
        return "FAILED", f"epmc hit but not OA (pmcid={pmcid or 'none'})"
    url = f"https://www.ebi.ac.uk/europepmc/webservices/rest/{pmcid}/fullTextXML"
    try:
        xml = subprocess.run(["curl", "-s", "-m", "60", "-A", UA, url],
                             capture_output=True, text=True).stdout
    except Exception as e:
        return "FAILED", f"epmc fulltext: {str(e)[:60]}"
    if len(xml) < 3000 or "<article" not in xml:
        return "FAILED", f"epmc fulltext empty for {pmcid}"
    text = re.sub(r"<[^>]+>", " ", xml)
    text = re.sub(r"\s+", " ", text)
    open(txt_path, "w").write(text)
    return "OK", f"Europe PMC {pmcid}, {len(text) // 1024} KB text"


def to_text(pdf, txt):
    try:
        subprocess.run(["pdftotext", "-q", "-enc", "UTF-8", pdf, txt], timeout=120)
    except Exception as e:
        return "TEXT_FAILED", str(e)[:60]
    if not os.path.exists(txt) or os.path.getsize(txt) < 500:
        return "TEXT_EMPTY", "no text layer; likely a scan, needs OCR"
    return "OK", f"{os.path.getsize(txt) // 1024} KB text"


def main():
    oa = json.load(open(OA))
    gate = {r["openalex_id"]: r for r in csv.DictReader(open(GATE))}
    tiers = json.load(open(TIERS))
    by_id = {r["id"]: r for t in tiers.values() for r in t}
    os.makedirs(PDF_DIR, exist_ok=True)

    rows = []
    for wid, st in oa.items():
        rec = by_id.get(wid, {})
        title = rec.get("title") or (gate.get(wid, {}) or {}).get("title") or wid
        doi = rec.get("doi") or (gate.get(wid, {}) or {}).get("doi") or ""
        cell = (gate.get(wid) or {}).get("cell", "")
        if cell in PRIMARY_CELLS:
            job = "A_primary"
        elif cell in INPUT_CELLS:
            job = "A2_input"
        elif wid in gate:
            job = "B_held"
        else:
            job = "C_parameter"
        family = (gate.get(wid) or {}).get("screen_family") or (rec.get("screen_family") or "")
        base = os.path.join(PDF_DIR, f"{wid}__{slugify(title)}")
        pdf, txt = base + ".pdf", base + ".txt"
        # ROUTE LADDER. Each rung fails for a different reason, so a rung that fails says nothing
        # about the next one. The publisher link is tried first because it is the version of record;
        # repository copies next; Europe PMC last because it yields text rather than a PDF.
        if os.path.exists(txt) and os.path.getsize(txt) > 500:
            rows.append([wid, doi, job, family, st["oa_status"], st.get("host", ""), "OK/OK",
                         "already present", title[:90]])
            continue
        attempts, fstat, fnote, tstat = [], "FAILED", "", ""
        urls = []
        if st.get("pdf_url"):
            urls.append((st["pdf_url"], st.get("host") or "publisher"))
        urls += [u for u in oa_locations(wid) if u[0] not in {x[0] for x in urls}]
        for u, host in urls[:5]:
            s, n = fetch(u, pdf)
            attempts.append(f"{host[:22]}:{n}")
            time.sleep(0.5)
            if s == "OK":
                fstat, fnote = "OK", "; ".join(attempts)
                break
        if fstat == "OK":
            tstat, tnote = to_text(pdf, txt)
            fnote = f"{fnote}; text: {tnote}"
        if fstat != "OK" or tstat in ("TEXT_EMPTY", "TEXT_FAILED"):
            s, n = europepmc_text(doi, txt)
            attempts.append(f"europepmc:{n}")
            if s == "OK":
                fstat, tstat = "OK", "OK"
            fnote = "; ".join(attempts)
        if fstat != "OK":
            fnote = "; ".join(attempts) or "no OA location known"
        rows.append([wid, doi, job, family, st["oa_status"], st.get("host", ""),
                     f"{fstat}/{tstat}" if tstat else fstat, fnote, title[:90]])

    with open(OUT_LOG, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["openalex_id", "doi", "job", "chemical_family", "oa_status", "host", "result",
                    "note", "title"])
        w.writerows(rows)

    def readable(r):
        return r[6].startswith("OK/OK") or r[6] == "OK/OK"

    got = sum(1 for r in rows if readable(r))
    failed = sum(1 for r in rows if "FAILED" in r[6])
    print(f"records={len(rows)} readable={got} failed_fetch={failed}")
    for j in ("A_primary", "A2_input", "B_held", "C_parameter"):
        jr = [r for r in rows if r[2] == j]
        if jr:
            print(f"  {j:<12} {sum(1 for r in jr if readable(r))}/{len(jr)} readable")
    # THE SELECTION TEST, restated after the fetch rather than only before it. A ceiling measured in
    # 139 is a forecast; this is what actually landed on disk, and it is the number the chapter's
    # limitations paragraph has to quote.
    print("  by family (A + A2):")
    for f in ("pfas", "plastic", "both", "unclear", "none", ""):
        fr = [r for r in rows if r[2] in ("A_primary", "A2_input") and r[3] == f]
        if fr:
            print(f"    {f or '(unstated)':<10} {sum(1 for r in fr if readable(r))}/{len(fr)}")
    print(f"-> {os.path.relpath(OUT_LOG, ROOT)}")


if __name__ == "__main__":
    main()
