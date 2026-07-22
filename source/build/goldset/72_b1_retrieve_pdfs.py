#!/usr/bin/env python3
"""TICK-032: retrieve open-access PDFs for the B.1 estimand-ready pooling set.

Prioritizes the status-and-reproduction (PROXIMATE_ULTIMATE) stream, which is the
chapter's poolable cell. Resolves each study's open-access PDF via OpenAlex, downloads
it, verifies the %PDF magic bytes (rejecting HTML paywall pages), and writes a retrieval
log. Idempotent: skips files already on disk.

Outputs:
  literature/pdfs/evolutionary-sex-drive-contraceptive-decoupling/{WID}__{slug}.pdf
  extraction/evolutionary-sex-drive-contraceptive-decoupling-pdf-retrieval-log.csv
"""
from __future__ import annotations

import csv
import json
import re
import subprocess
import time
from pathlib import Path

SLUG = "evolutionary-sex-drive-contraceptive-decoupling"
ROOT = Path(__file__).resolve().parents[3]
POOL = ROOT / "output" / f"{SLUG}-estimand-ready-set.json"
PDF_DIR = ROOT / "literature" / "pdfs" / SLUG
LOG = ROOT / "extraction" / f"{SLUG}-pdf-retrieval-log.csv"
MAILTO = "shravanh@uchicago.edu"
UA = "Mozilla/5.0 (fertility-review-causes; mailto:shravanh@uchicago.edu)"

# Priority order: Section 5.1 first, then the bridge and distinctive-claim cells.
CELL_PRIORITY = {
    "PROXIMATE_ULTIMATE": 0,
    "PRIMARY_DECOUPLING": 1,
    "PRIMARY_DESIRE_INDEPENDENCE": 1,
    "MOTIVATION_DISTINCTNESS": 2,
}


def slugify(title: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", (title or "").lower()).strip("-")
    return s[:60] or "untitled"


def openalex_batch(work_ids: list[str]) -> dict[str, dict]:
    """Fetch OA metadata for up to 50 works per request."""
    out: dict[str, dict] = {}
    for i in range(0, len(work_ids), 50):
        chunk = work_ids[i : i + 50]
        filt = "openalex_id:" + "|".join(chunk)
        url = (
            "https://api.openalex.org/works"
            f"?filter={filt}&per-page=50"
            "&select=id,doi,title,open_access,best_oa_location,primary_location,locations"
            f"&mailto={MAILTO}"
        )
        proc = subprocess.run(
            ["curl", "-sL", "--max-time", "40", "-A", UA, url],
            check=True,
            capture_output=True,
        )
        data = json.loads(proc.stdout)
        for w in data.get("results", []):
            wid = w["id"].rsplit("/", 1)[-1]
            out[wid] = w
        time.sleep(0.3)
    return out


def unpaywall(doi: str) -> dict:
    if not doi:
        return {}
    d = doi.replace("https://doi.org/", "")
    url = f"https://api.unpaywall.org/v2/{d}?email={MAILTO}"
    try:
        proc = subprocess.run(
            ["curl", "-sL", "--max-time", "30", "-A", UA, url],
            check=True,
            capture_output=True,
        )
        return json.loads(proc.stdout)
    except (subprocess.CalledProcessError, json.JSONDecodeError):
        return {}


def candidate_urls(w: dict, up: dict) -> list[str]:
    """Ordered, de-duplicated PDF-URL candidates. Repository (green) copies first,
    since publisher bronze links often serve HTML to a non-browser client."""
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
    # Unpaywall locations
    for loc in (up.get("oa_locations") or []):
        u = loc.get("url_for_pdf") or loc.get("url")
        if not u:
            continue
        (green if loc.get("host_type") == "repository" else other).append(u)
    best = (up.get("best_oa_location") or {})
    if best.get("url_for_pdf"):
        other.append(best["url_for_pdf"])
    seen, ordered = set(), []
    for u in green + other:
        if u and u not in seen:
            seen.add(u)
            ordered.append(u)
    return ordered


def download(url: str, dest: Path) -> tuple[bool, str]:
    """curl the URL; keep only if the payload starts with %PDF."""
    tmp = dest.with_suffix(".part")
    try:
        subprocess.run(
            ["curl", "-sL", "--max-time", "90", "-A", UA, "-o", str(tmp), url],
            check=True,
            capture_output=True,
        )
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


def main() -> None:
    PDF_DIR.mkdir(parents=True, exist_ok=True)
    LOG.parent.mkdir(parents=True, exist_ok=True)
    pool = json.load(open(POOL))
    pool.sort(key=lambda x: (CELL_PRIORITY.get(x.get("cell"), 9), x.get("year") or 0))

    work_ids = [x["paperId"] for x in pool if str(x.get("paperId", "")).startswith("W")]
    meta = openalex_batch(work_ids)

    rows = []
    got = 0
    for x in pool:
        wid = x.get("paperId", "")
        w = meta.get(wid, {})
        oa = w.get("open_access") or {}
        doi = x.get("doi") or ""
        dest = PDF_DIR / f"{wid}__{slugify(x.get('title',''))}.pdf"
        status, detail, size, used_url = "no_oa_url", "", 0, ""
        if dest.exists():
            status, detail, size = "already_present", "skip", dest.stat().st_size
            got += 1
        else:
            up = unpaywall(doi)
            urls = candidate_urls(w, up)
            tried = []
            for url in urls[:6]:
                ok, why = download(url, dest)
                tried.append(why)
                if ok:
                    status, detail, size, used_url = "downloaded", "ok", dest.stat().st_size, url
                    got += 1
                    break
                time.sleep(0.2)
            if status != "downloaded":
                status = "failed" if urls else "no_oa_url"
                detail = ",".join(dict.fromkeys(tried)) if tried else "closed"
            time.sleep(0.2)
        rows.append(
            {
                "work_id": wid,
                "doi": doi,
                "cell": x.get("cell"),
                "year": x.get("year"),
                "oa_status": oa.get("oa_status") or "closed",
                "pdf_url": used_url,
                "download_status": status,
                "detail": detail,
                "bytes": size,
                "file": dest.name if status in ("downloaded", "already_present") else "",
                "title": (x.get("title") or "")[:120],
            }
        )

    with open(LOG, "w", newline="") as fh:
        wtr = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        wtr.writeheader()
        wtr.writerows(rows)

    by_cell: dict[str, list[int]] = {}
    for r in rows:
        c = by_cell.setdefault(r["cell"], [0, 0])
        c[1] += 1
        if r["file"]:
            c[0] += 1
    print(f"PDFs on disk: {got}/{len(pool)}")
    for c, (n, tot) in sorted(by_cell.items()):
        print(f"  {c}: {n}/{tot}")
    print(f"log -> {LOG.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
