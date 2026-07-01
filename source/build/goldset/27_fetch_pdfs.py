#!/usr/bin/env python3
"""
Step 27 - OUTPUT 2: fetch a final folder of PDFs for the meta-analysis-ready set.

Open-access only, two sources per paper (C3-clean, no paywalled scraping):
  1. OpenAlex OA urls (best_oa_location / primary_location / open_access.oa_url) from step-23 enrichment
  2. Unpaywall best_oa_location.url_for_pdf, keyed on the finalized DOI
Each candidate URL is downloaded and validated by %PDF magic bytes; the first valid one wins.
Anything with no OA source, or whose OA links all fail/return non-PDF, is recorded as
NEEDS_MANUAL (title + DOI) for RA institutional-access retrieval - never silently dropped.

Files land in literature/pdfs/{slug}/ named <paperId>__<title-slug>.pdf (stable, dedup-safe).

Input : {slug}-metaanalysis-ready-final.json
Output: literature/pdfs/{slug}/*.pdf + {slug}-pdf-manifest.json + (stderr) coverage
"""
import json, re, sys, time, hashlib, urllib.parse, subprocess
from pathlib import Path
from collections import Counter

ROOT = Path("/Users/shravanhari/~/Anup RA/projects/fertility-review-causes")
SL = ROOT / "literature/search-logs"
SLUG = "old-age-security-pension-crowdout"
PDFDIR = ROOT / "literature/pdfs" / SLUG; PDFDIR.mkdir(parents=True, exist_ok=True)
CACHE = ROOT / "source/build/goldset/cache"
MAILTO = "shravanh@uchicago.edu"

def slug(t):
    return re.sub(r"[^a-z0-9]+", "-", (t or "").lower()).strip("-")[:60] or "untitled"

def unpaywall_pdf(doi):
    cf = CACHE / f"upw_{hashlib.sha1(doi.encode()).hexdigest()[:16]}.json"
    if cf.exists(): d = json.load(open(cf))
    else:
        r = subprocess.run(["curl","-s","--max-time","30",
            f"https://api.unpaywall.org/v2/{urllib.parse.quote(doi)}?email={MAILTO}"],
            capture_output=True, text=True)
        try: d = json.loads(r.stdout)
        except Exception: d = {}
        json.dump(d, open(cf, "w")); time.sleep(0.5)
    loc = d.get("best_oa_location") or {}
    return loc.get("url_for_pdf") or loc.get("url")

def download_pdf(url, dest):
    """Return True iff a valid PDF was written to dest."""
    try:
        subprocess.run(["curl","-sL","--max-time","90","-A",f"fertility-review/1.0 (mailto:{MAILTO})",
                        "-o", str(dest), url], capture_output=True, timeout=100)
    except Exception:
        return False
    if dest.exists() and dest.stat().st_size > 2048:
        with open(dest, "rb") as f:
            if f.read(5).startswith(b"%PDF"): return True
    if dest.exists(): dest.unlink()
    return False

def main():
    rows = json.load(open(SL / f"{SLUG}-metaanalysis-studies.json"))
    manifest = []; cnt = Counter()
    for i, r in enumerate(rows, 1):
        pid = r["paperId"]; doi = r.get("doi_final")
        fn = PDFDIR / f"{pid}__{slug(r.get('title'))}.pdf"
        urls = list(r.get("oa_urls") or [])
        if doi:
            u = unpaywall_pdf(doi)
            if u and u not in urls: urls.append(u)
        rec = {"paperId": pid, "title": r.get("title"), "doi": doi,
               "tier": r["tier"], "evidenceType": r["evidenceType"]}
        if fn.exists() and fn.stat().st_size > 2048:
            rec["status"], rec["file"] = "FETCHED", fn.name; cnt["FETCHED"] += 1
        elif not urls:
            rec["status"] = "NEEDS_MANUAL"; rec["reason"] = "no OA source"; cnt["NEEDS_MANUAL"] += 1
        else:
            ok = next((u for u in urls if download_pdf(u, fn)), None)
            if ok:
                rec["status"], rec["file"], rec["source_url"] = "FETCHED", fn.name, ok; cnt["FETCHED"] += 1
            else:
                rec["status"] = "NEEDS_MANUAL"; rec["reason"] = "OA links failed/non-PDF"; cnt["NEEDS_MANUAL"] += 1
        manifest.append(rec)
        if i % 40 == 0: print(f"  {i}/{len(rows)}: {dict(cnt)}", file=sys.stderr)

    json.dump(manifest, open(SL / f"{SLUG}-pdf-manifest.json", "w"), indent=2)
    print(f"\nPDF fetch: {dict(cnt)} into {PDFDIR}", file=sys.stderr)
    print(f"manifest -> {SLUG}-pdf-manifest.json", file=sys.stderr)

if __name__ == "__main__":
    main()
