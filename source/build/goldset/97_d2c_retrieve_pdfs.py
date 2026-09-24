#!/usr/bin/env python3
"""TICK-092 stage 5: retrieve open-access PDFs for the D.2.c estimand-ready pooling set.

Mirrors 82_d3b_retrieve_pdfs.py (OpenAlex all-locations + Unpaywall + Europe PMC + derived landing-page
constructions, %PDF magic-byte verification, idempotent). D.2.c pool from the assembler
(estimand-ready.json). Priority is the identified-design core (identification in
{EXOGENOUS_FREQUENCY_SHOCK, PROSPECTIVE_MEASUREMENT}) — the studies the chapter's causal claim turns on — ahead of the
associational remainder, and the retrieval rate is reported SEPARATELY for the core and the full pool so
a headline rate cannot hide a gap in the stratum that matters.

Stage-4 note: the human RA title/abstract gate is NOT yet returned; this retrieves against the AI
screen's pool as-is ("with what we have"). Nothing is dropped silently — every unreachable record lands
on the handoff list split by access class (closed vs oa-but-blocked), which is the PROTOCOL step-5 "RA
procures PDFs the AI can't access" deliverable.

Outputs:
  literature/pdfs/son-preference-cultural/W<id>__<slug>.pdf   (gitignored if large)
  extraction/son-preference-cultural-pdf-retrieval-log.csv
  extraction/son-preference-cultural-missing-pdf-dois.csv     (human handoff)
"""
from __future__ import annotations

import csv
import json
import re
import subprocess
import time
from pathlib import Path

SLUG = "son-preference-cultural"
ROOT = Path(__file__).resolve().parents[3]
POOL = ROOT / "literature" / "search-logs" / f"{SLUG}-estimand-ready.json"
PDF_DIR = ROOT / "literature" / "pdfs" / SLUG
LOG = ROOT / "extraction" / f"{SLUG}-pdf-retrieval-log.csv"
MISSING = ROOT / "extraction" / f"{SLUG}-missing-pdf-dois.csv"
MAILTO = "shravanh@uchicago.edu"
UA = "Mozilla/5.0 (fertility-review-causes; mailto:shravanh@uchicago.edu)"

PRIORITY_IDENTIFIED = 0
PRIORITY_ASSOCIATIONAL = 1


def slugify(title: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", (title or "").lower()).strip("-")
    return s[:60] or "untitled"


def wid_of(rec: dict) -> str:
    return str(rec.get("id", "")).rsplit("/", 1)[-1]


def load_pool() -> list[dict]:
    pool = json.load(open(POOL))
    for rec in pool:
        ident = str(rec.get("identification", "")).upper()
        rec["priority"] = (PRIORITY_IDENTIFIED if ident in ("NATURAL_EXPERIMENT", "REVEALED_STOPPING")
                           else PRIORITY_ASSOCIATIONAL)
    pool.sort(key=lambda x: (x["priority"], -(x.get("cited_by_count") or 0), -(x.get("year") or 0)))
    return pool


def openalex_batch(work_ids: list[str]) -> dict[str, dict]:
    out: dict[str, dict] = {}
    for i in range(0, len(work_ids), 50):
        chunk = work_ids[i:i + 50]
        filt = "openalex_id:" + "|".join(chunk)
        url = ("https://api.openalex.org/works"
               f"?filter={filt}&per-page=50"
               "&select=id,doi,title,open_access,best_oa_location,primary_location,locations"
               f"&mailto={MAILTO}")
        proc = subprocess.run(["curl", "-sL", "--max-time", "40", "-A", UA, url],
                              check=True, capture_output=True)
        data = json.loads(proc.stdout)
        for w in data.get("results", []):
            out[w["id"].rsplit("/", 1)[-1]] = w
        time.sleep(0.3)
    return out


def unpaywall(doi: str) -> dict:
    if not doi:
        return {}
    d = doi.replace("https://doi.org/", "")
    url = f"https://api.unpaywall.org/v2/{d}?email={MAILTO}"
    try:
        proc = subprocess.run(["curl", "-sL", "--max-time", "30", "-A", UA, url],
                              check=True, capture_output=True)
        return json.loads(proc.stdout)
    except (subprocess.CalledProcessError, json.JSONDecodeError):
        return {}


def derived_urls(w: dict, up: dict, doi: str) -> list[str]:
    """PDF URLs constructed from landing pages, for records whose metadata has no pdf_url.
    PMC /pdf/, PLoS printable, Research Square article PDFs — all deterministic from metadata in hand.
    MDPI, PNAS, Springer are known to 403/HTML a non-browser client and are left to the human."""
    out: list[str] = []
    d = (doi or "").replace("https://doi.org/", "")
    landings = [loc.get("landing_page_url") for loc in (w.get("locations") or [])
                if loc.get("landing_page_url")]
    for key in ("best_oa_location", "primary_location"):
        loc = w.get(key) or {}
        if loc.get("landing_page_url"):
            landings.append(loc["landing_page_url"])
    for loc in (up.get("oa_locations") or []):
        if loc.get("url"):
            landings.append(loc["url"])
    for url in landings:
        m = re.search(r"/pmc/articles/(?:PMC)?(\d+)", url) or re.search(
            r"pmc\.ncbi\.nlm\.nih\.gov/articles/(?:PMC)?(\d+)", url)
        if m:
            pmcid = f"PMC{m.group(1)}"
            out.append(f"https://pmc.ncbi.nlm.nih.gov/articles/{pmcid}/pdf/")
            out.append(f"https://www.ncbi.nlm.nih.gov/pmc/articles/{pmcid}/pdf/")
    if d.startswith("10.1371/"):
        out.append(f"https://journals.plos.org/plosone/article/file?id={d}&type=printable")
    m = re.match(r"10\.21203/rs\.3\.(rs-\d+)/v(\d+)", d)
    if m:
        out.append(f"https://www.researchsquare.com/article/{m.group(1)}/v{m.group(2)}.pdf")
    return out


def europepmc_urls(doi: str) -> list[str]:
    """Europe PMC ?pdf=render — the most productive source in this project; mirrors deposited full
    text and does not bot-block. Often the accepted manuscript, not the VoR (ingest records that)."""
    d = (doi or "").replace("https://doi.org/", "")
    if not d:
        return []
    url = ("https://www.ebi.ac.uk/europepmc/webservices/rest/search"
           f"?query=DOI:%22{d}%22&resultType=core&format=json")
    try:
        p = subprocess.run(["curl", "-sL", "--max-time", "35", "-A", UA, url],
                           check=True, capture_output=True)
        data = json.loads(p.stdout)
    except (subprocess.CalledProcessError, json.JSONDecodeError):
        return []
    out = []
    for r in ((data.get("resultList") or {}).get("result") or []):
        if r.get("pmcid"):
            out.append(f"https://europepmc.org/articles/{r['pmcid']}?pdf=render")
            out.append("https://www.ebi.ac.uk/europepmc/webservices/rest/"
                       f"{r['pmcid']}/fullTextPDF")
    return out


def candidate_urls(w: dict, up: dict, doi: str = "") -> list[str]:
    """Ordered, de-duplicated PDF-URL candidates. Repository (green) copies first, since publisher
    bronze links often serve HTML to a non-browser client; derived constructions last."""
    green, other = [], []
    for loc in (w.get("locations") or []):
        u = loc.get("pdf_url")
        if not u:
            continue
        (green if (loc.get("version") == "publishedVersion" and loc.get("host_type") == "repository")
         or loc.get("host_type") == "repository" else other).append(u)
    for key in ("best_oa_location", "primary_location"):
        loc = w.get(key) or {}
        if loc.get("pdf_url"):
            other.append(loc["pdf_url"])
    if (w.get("open_access") or {}).get("oa_url"):
        other.append(w["open_access"]["oa_url"])
    for loc in (up.get("oa_locations") or []):
        u = loc.get("url_for_pdf") or loc.get("url")
        if not u:
            continue
        (green if loc.get("host_type") == "repository" else other).append(u)
    best = (up.get("best_oa_location") or {})
    if best.get("url_for_pdf"):
        other.append(best["url_for_pdf"])
    seen, ordered = set(), []
    for u in green + other + europepmc_urls(doi) + derived_urls(w, up, doi):
        if u and u not in seen:
            seen.add(u)
            ordered.append(u)
    return ordered


def download(url: str, dest: Path) -> tuple[bool, str]:
    tmp = dest.with_suffix(".part")
    try:
        subprocess.run(["curl", "-sL", "--max-time", "90", "-A", UA, "-o", str(tmp), url],
                       check=True, capture_output=True)
    except subprocess.CalledProcessError as e:
        return False, f"curl_error:{e.returncode}"
    if not tmp.exists() or tmp.stat().st_size < 1024:
        tmp.unlink(missing_ok=True)
        return False, "empty_or_tiny"
    with open(tmp, "rb") as fh:
        head = fh.read(5)
    if head[:4] != b"%PDF":
        tmp.unlink(missing_ok=True)
        return False, "not_pdf_html_paywall"
    tmp.rename(dest)
    return True, "ok"


def band(rec: dict) -> str:
    return "identified_core" if rec["priority"] == PRIORITY_IDENTIFIED else "associational"


def main() -> None:
    PDF_DIR.mkdir(parents=True, exist_ok=True)
    LOG.parent.mkdir(parents=True, exist_ok=True)
    pool = load_pool()
    work_ids = [wid_of(x) for x in pool if wid_of(x).startswith("W")]
    meta = openalex_batch(work_ids)

    rows = []
    for x in pool:
        wid = wid_of(x)
        w = meta.get(wid, {})
        oa = w.get("open_access") or {}
        doi = x.get("doi") or ""
        dest = PDF_DIR / f"{wid}__{slugify(x.get('title', ''))}.pdf"
        status, detail, size, used_url = "no_oa_url", "", 0, ""
        # This pass retrieves the identified-design core only (380 records); the associational
        # remainder (667) is deferred to the RA extraction backlog without download attempts, so the
        # pass finishes in minutes rather than hours. Deferred rows still land on the handoff.
        if band(x) == "associational":
            status, detail = "deferred_ra_backlog", "associational_not_attempted"
        elif dest.exists():
            status, detail, size = "already_present", "skip", dest.stat().st_size
        else:
            up = unpaywall(doi)
            urls = candidate_urls(w, up, doi)
            tried = []
            for url in urls[:10]:
                ok, why = download(url, dest)
                tried.append(why)
                if ok:
                    status, detail, size, used_url = "downloaded", "ok", dest.stat().st_size, url
                    break
                time.sleep(0.2)
            if status != "downloaded":
                status = "failed" if urls else "no_oa_url"
                detail = ",".join(dict.fromkeys(tried)) if tried else "closed"
            time.sleep(0.2)
        rows.append({
            "work_id": wid,
            "doi": doi,
            "band": band(x),
            "estimand_cell": str(x.get("estimand_cell", "")).upper(),
            "identification": str(x.get("identification", "")).upper(),
            "sub_mechanism": str(x.get("sub_mechanism", "")).upper(),
            "year": x.get("year"),
            "cited_by_count": x.get("cited_by_count") or 0,
            "oa_status": oa.get("oa_status") or "closed",
            "pdf_url": used_url,
            "download_status": status,
            "detail": detail,
            "bytes": size,
            "file": dest.name if status in ("downloaded", "already_present") else "",
            "title": (x.get("title") or "")[:120],
        })

    with open(LOG, "w", newline="") as fh:
        wtr = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        wtr.writeheader()
        wtr.writerows(rows)

    # Handoff split by access class: `oa_but_blocked` is free to read and merely refuses a non-browser
    # client (anyone with a browser fetches it); `closed` needs the UChicago proxy or ILL.
    missing = [r for r in rows if not r["file"]]
    fields = ["band", "access_class", "doi", "work_id", "year", "oa_status", "detail", "title"]
    with open(MISSING, "w", newline="") as fh:
        wtr = csv.DictWriter(fh, fieldnames=fields)
        wtr.writeheader()
        for r in sorted(missing, key=lambda r: (r["band"] != "identified_core",
                                                r["oa_status"] == "closed")):
            access_class = "closed" if r["oa_status"] == "closed" else "oa_but_blocked"
            wtr.writerow({"band": r["band"], "access_class": access_class, "doi": r["doi"],
                          "work_id": r["work_id"], "year": r["year"], "oa_status": r["oa_status"],
                          "detail": r["detail"], "title": r["title"]})

    def rate(pred) -> tuple[int, int]:
        sel = [r for r in rows if pred(r)]
        return sum(1 for r in sel if r["file"]), len(sel)

    core_n, core_t = rate(lambda r: r["band"] == "identified_core")
    all_n, all_t = rate(lambda _: True)
    print(f"IDENTIFIED CORE: {core_n}/{core_t}")
    assoc_n, assoc_t = rate(lambda r: r["band"] == "associational")
    print(f"  associational: {assoc_n}/{assoc_t}")
    print(f"FULL POOL: {all_n}/{all_t}")
    print(f"log     -> {LOG.relative_to(ROOT)}")
    print(f"handoff -> {MISSING.relative_to(ROOT)} ({len(missing)} rows)")


if __name__ == "__main__":
    main()
