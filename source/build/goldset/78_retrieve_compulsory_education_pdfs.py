#!/usr/bin/env python3
"""Retrieve open-access PDFs for the compulsory-education evidence workstreams.

Sources are Alexandra's two RA-approved mechanism sets. Candidate URLs come from OpenAlex,
Unpaywall, stable NBER working-paper paths, and any DOI URL that directly resolves to a PDF.
Downloads are accepted only when they begin with PDF magic bytes. Failures remain explicit in the
manifest for institutional/manual retrieval; no paper is silently dropped.
"""

import csv
import hashlib
import json
import re
import subprocess
import time
import urllib.parse
from pathlib import Path


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
PDF_DIR = REPO / "literature/pdfs/compulsory-education"
CACHE_DIR = REPO / "source/build/goldset/cache/compulsory-education-pdfs"
MANIFEST = REPO / "output/compulsory-education-pdf-retrieval-manifest.csv"
ACQUISITION_QUEUE = REPO / "output/compulsory-education-pdf-acquisition-queue.csv"
INPUTS = [
    REPO / "output/compulsory-education-child-economic-value-ra-approved-papers.csv",
    REPO / "output/tempo-effects-birth-postponement-compulsory-schooling-ra-approved-papers.csv",
]
MAILTO = "zhitongz@uchicago.edu"

FIELDS = [
    "paperId", "doi", "title", "year", "authors", "sets", "evidence_roles", "status",
    "pdf_path", "source_url", "attempted_urls", "reason",
]


def slug(text):
    return re.sub(r"[^a-z0-9]+", "-", (text or "").lower()).strip("-")[:72] or "untitled"


def curl_json(url, cache_key):
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    path = CACHE_DIR / f"{cache_key}.json"
    if path.exists():
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            pass
    result = subprocess.run(
        ["curl", "-sL", "--max-time", "20", "-A", f"fertility-review/1.0 (mailto:{MAILTO})", url],
        capture_output=True, text=True, timeout=25,
    )
    try:
        data = json.loads(result.stdout)
    except Exception:
        data = {}
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    time.sleep(0.25)
    return data


def openalex_urls(paper_id):
    data = curl_json(
        f"https://api.openalex.org/works/{paper_id}?mailto={urllib.parse.quote(MAILTO)}",
        f"openalex_{paper_id}",
    )
    urls = []
    for location in [data.get("best_oa_location"), data.get("primary_location")] + list(data.get("locations") or []):
        if not location:
            continue
        for key in ("pdf_url",):
            value = location.get(key)
            if value and value not in urls:
                urls.append(value)
    return urls


def unpaywall_urls(doi):
    if not doi:
        return []
    key = hashlib.sha1(doi.encode()).hexdigest()[:16]
    data = curl_json(
        f"https://api.unpaywall.org/v2/{urllib.parse.quote(doi)}?email={urllib.parse.quote(MAILTO)}",
        f"unpaywall_{key}",
    )
    urls = []
    for location in [data.get("best_oa_location")] + list(data.get("oa_locations") or []):
        if not location:
            continue
        for name in ("url_for_pdf",):
            value = location.get(name)
            if value and value not in urls:
                urls.append(value)
    return urls


def special_urls(doi):
    if not doi:
        return []
    match = re.fullmatch(r"10\.3386/w(\d+)", doi)
    if match:
        number = match.group(1)
        return [f"https://www.nber.org/system/files/working_papers/w{number}/w{number}.pdf"]
    return []


def semantic_scholar_urls(doi, paper_id):
    identifier = f"DOI:{doi}" if doi else paper_id
    data = curl_json(
        "https://api.semanticscholar.org/graph/v1/paper/"
        f"{urllib.parse.quote(identifier, safe=':')}?fields=title,openAccessPdf",
        f"s2_{hashlib.sha1(identifier.encode()).hexdigest()[:16]}",
    )
    location = data.get("openAccessPdf") or {}
    return [location["url"]] if location.get("url") else []


def crossref_urls(doi):
    if not doi:
        return []
    data = curl_json(
        f"https://api.crossref.org/works/{urllib.parse.quote(doi)}",
        f"crossref_{hashlib.sha1(doi.encode()).hexdigest()[:16]}",
    )
    urls = []
    for link in (data.get("message") or {}).get("link") or []:
        if "pdf" in (link.get("content-type") or "").lower() and link.get("URL"):
            urls.append(link["URL"])
    return urls


def valid_pdf(path):
    return path.exists() and path.stat().st_size > 2048 and path.read_bytes()[:5] == b"%PDF-"


def download(url, destination):
    partial = destination.with_suffix(".partial")
    result = subprocess.run(
        ["curl", "-sL", "--max-time", "35", "-A", f"fertility-review/1.0 (mailto:{MAILTO})",
         "-o", str(partial), url],
        capture_output=True, timeout=42,
    )
    if result.returncode == 0 and valid_pdf(partial):
        partial.replace(destination)
        return True
    if partial.exists():
        partial.unlink()
    return False


def read_sources():
    merged = {}
    for path in INPUTS:
        with path.open(newline="", encoding="utf-8-sig") as handle:
            for row in csv.DictReader(handle):
                record = merged.setdefault(row["paperId"], dict(row, sets=[], evidence_roles=[]))
                if row["mechanism_set"] not in record["sets"]:
                    record["sets"].append(row["mechanism_set"])
                if row["evidence_role"] not in record["evidence_roles"]:
                    record["evidence_roles"].append(row["evidence_role"])
    return sorted(merged.values(), key=lambda row: (int(row["year"] or 0), row["title"].casefold()))


def main():
    PDF_DIR.mkdir(parents=True, exist_ok=True)
    manifest = []
    if MANIFEST.exists():
        with MANIFEST.open(newline="", encoding="utf-8-sig") as handle:
            manifest = list(csv.DictReader(handle))
    prior = {row["paperId"]: row for row in manifest}
    for index, row in enumerate(read_sources(), 1):
        existing_candidates = sorted(PDF_DIR.glob(f"{row['paperId']}__*.pdf"))
        existing = next((path for path in existing_candidates if valid_pdf(path)), None)
        if row["paperId"] in prior and existing:
            prior[row["paperId"]]["status"] = "RETRIEVED"
            prior[row["paperId"]]["pdf_path"] = str(existing.relative_to(REPO))
            prior[row["paperId"]]["reason"] = "existing validated PDF"
            continue
        if row["paperId"] in prior:
            continue
        doi = (row.get("doi") or "").strip().lower()
        destination = PDF_DIR / f"{row['paperId']}__{slug(row['title'])}.pdf"
        urls = []
        for url in (special_urls(doi) + openalex_urls(row["paperId"]) + unpaywall_urls(doi)
                    + semantic_scholar_urls(doi, row["paperId"]) + crossref_urls(doi)):
            if url and url not in urls:
                urls.append(url)
        urls = urls[:6]
        source_url = ""
        if valid_pdf(destination):
            status, reason = "RETRIEVED", "existing validated PDF"
        else:
            for url in urls:
                if download(url, destination):
                    source_url = url
                    break
            if source_url:
                status, reason = "RETRIEVED", "validated open-access PDF"
            else:
                status = "NEEDS_INSTITUTIONAL_OR_MANUAL"
                reason = "no candidate URL returned a validated PDF" if urls else "no open-access candidate URL"
        manifest.append({
            "paperId": row["paperId"], "doi": doi, "title": row["title"], "year": row["year"],
            "authors": row["authors"], "sets": ";".join(row["sets"]),
            "evidence_roles": ";".join(row["evidence_roles"]), "status": status,
            "pdf_path": str(destination.relative_to(REPO)) if status == "RETRIEVED" else "",
            "source_url": source_url, "attempted_urls": ";".join(urls), "reason": reason,
        })
        prior[row["paperId"]] = manifest[-1]
        print(f"[{index:02d}/25] {status:31s} {row['title'][:65]}", flush=True)

        # Preserve progress if a later host stalls or the process is interrupted.
        with MANIFEST.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=FIELDS, lineterminator="\n")
            writer.writeheader()
            writer.writerows(manifest)

    manifest = list(prior.values()) if prior else manifest
    with MANIFEST.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(manifest)
    missing = [row for row in manifest if row["status"] != "RETRIEVED"]
    with ACQUISITION_QUEUE.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(missing)
    retrieved = sum(row["status"] == "RETRIEVED" for row in manifest)
    print(f"retrieved {retrieved}/{len(manifest)} distinct approved sources")
    print(f"manual/institutional queue: {len(manifest) - retrieved}")


if __name__ == "__main__":
    main()
