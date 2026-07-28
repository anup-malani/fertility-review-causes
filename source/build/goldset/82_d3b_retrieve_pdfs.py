#!/usr/bin/env python3
"""TICK-048: retrieve open-access PDFs for the D.3.b estimand-ready pooling sets.

Mirrors 72_b1_retrieve_pdfs.py (OpenAlex all-locations + Unpaywall fallback, %PDF
magic-byte verification, idempotent) with three D.3.b-specific differences:

  1. TWO pooling files, not one. A1 scope decision 2 forbids a combined set, so the
     stated and realized pools are read separately and a work's membership in each is
     recorded. Three works appear in both (outcome_level BOTH); they are downloaded
     once and reported under both memberships.
  2. Priority is the DECISIVE 12 -- the 8 realized-fertility studies and the 4
     DESIRE_INDEPENDENCE studies -- ahead of the remaining stated-intention pool. Those
     twelve are what the chapter's conclusion turns on.
  3. Retrieval rate is reported SEPARATELY for the decisive 12 and for the full pool.
     A headline rate over the union would hide a gap in the stratum that matters, which
     is the failure mode that now caps the B.1 chapter (20/95, selected on open access).

Outputs:
  literature/pdfs/climate-anxiety-eco-doomerism/{WID}__{slug}.pdf   (gitignored)
  extraction/climate-anxiety-eco-doomerism-pdf-retrieval-log.csv
  extraction/climate-anxiety-eco-doomerism-missing-pdf-dois.csv     (human handoff)
"""
from __future__ import annotations

import csv
import json
import re
import subprocess
import time
from pathlib import Path

SLUG = "climate-anxiety-eco-doomerism"
ROOT = Path(__file__).resolve().parents[3]
POOL_STATED = ROOT / "output" / f"{SLUG}-estimand-ready-stated.json"
POOL_REALIZED = ROOT / "output" / f"{SLUG}-estimand-ready-realized.json"
PDF_DIR = ROOT / "literature" / "pdfs" / SLUG
LOG = ROOT / "extraction" / f"{SLUG}-pdf-retrieval-log.csv"
MISSING = ROOT / "extraction" / f"{SLUG}-missing-pdf-dois.csv"
MAILTO = "shravanh@uchicago.edu"
UA = "Mozilla/5.0 (fertility-review-causes; mailto:shravanh@uchicago.edu)"

# Priority 0 and 1 together are the "decisive 12" the chapter's conclusion turns on.
PRIORITY_REALIZED = 0
PRIORITY_DESIRE_INDEPENDENCE = 1
PRIORITY_STATED_REST = 2


def slugify(title: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", (title or "").lower()).strip("-")
    return s[:60] or "untitled"


def load_pool() -> list[dict]:
    """Merge the two pooling files into one download worklist, preserving membership.

    Deduplicates on paperId so a BOTH-level study is fetched once, and stamps each
    record with its priority band and its stated/realized membership flags.
    """
    stated = json.load(open(POOL_STATED))
    realized = json.load(open(POOL_REALIZED))
    realized_ids = {x["paperId"] for x in realized}

    merged: dict[str, dict] = {}
    for rec in realized:
        merged[rec["paperId"]] = dict(rec, in_realized=True, in_stated=False,
                                      priority=PRIORITY_REALIZED)
    for rec in stated:
        pid = rec["paperId"]
        if pid in merged:
            merged[pid]["in_stated"] = True
            continue
        prio = (PRIORITY_DESIRE_INDEPENDENCE
                if rec.get("cell") == "DESIRE_INDEPENDENCE" else PRIORITY_STATED_REST)
        merged[pid] = dict(rec, in_realized=pid in realized_ids, in_stated=True,
                           priority=prio)

    pool = list(merged.values())
    pool.sort(key=lambda x: (x["priority"], -(x.get("year") or 0)))
    return pool


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


def derived_urls(w: dict, up: dict, doi: str) -> list[str]:
    """PDF URLs constructed from landing pages, for records where the metadata has no
    pdf_url at all.

    This is not a nicety. On the first D.3.b run, three of the four DESIRE_INDEPENDENCE
    studies -- the cell carrying the hypothesis's distinctive claim -- failed as
    `not_pdf_html_paywall` while OpenAlex reported them gold or diamond OA. The cause was
    not a paywall: OpenAlex returned `pdf_url: None` for them and offered only landing
    pages (PMC, DOAJ, the DOI), so the downloader was handed an HTML page and correctly
    rejected it. A free article read as a closed one.

    Two constructions cover it. PMC exposes a PDF under `/pdf/` on the article id, and
    PLoS serves a `type=printable` file endpoint keyed on the DOI. Both are deterministic
    from metadata already in hand -- no search, no guessing at titles.
    """
    out: list[str] = []
    d = (doi or "").replace("https://doi.org/", "")

    landings = [
        loc.get("landing_page_url")
        for loc in (w.get("locations") or [])
        if loc.get("landing_page_url")
    ]
    for key in ("best_oa_location", "primary_location"):
        loc = w.get(key) or {}
        if loc.get("landing_page_url"):
            landings.append(loc["landing_page_url"])
    for loc in (up.get("oa_locations") or []):
        if loc.get("url"):
            landings.append(loc["url"])

    for url in landings:
        m = re.search(r"/pmc/articles/(?:PMC)?(\d+)", url) or re.search(
            r"pmc\.ncbi\.nlm\.nih\.gov/articles/(?:PMC)?(\d+)", url
        )
        if m:
            pmcid = f"PMC{m.group(1)}"
            out.append(f"https://pmc.ncbi.nlm.nih.gov/articles/{pmcid}/pdf/")
            out.append(f"https://www.ncbi.nlm.nih.gov/pmc/articles/{pmcid}/pdf/")

    if d.startswith("10.1371/"):
        out.append(
            f"https://journals.plos.org/plosone/article/file?id={d}&type=printable"
        )

    # Research Square preprints: 10.21203/rs.3.rs-<id>/v<n> -> /article/rs-<id>/v<n>.pdf
    m = re.match(r"10\.21203/rs\.3\.(rs-\d+)/v(\d+)", d)
    if m:
        out.append(f"https://www.researchsquare.com/article/{m.group(1)}/v{m.group(2)}.pdf")

    # Tried and rejected, recorded so nobody re-derives them: MDPI (/pdf) and PNAS
    # (/doi/pdf/) both return Cloudflare 403 to a non-browser client, and Springer's
    # /content/pdf/ path returns 200 with HTML. Those need a human with a browser.

    return out


def candidate_urls(w: dict, up: dict, doi: str = "") -> list[str]:
    """Ordered, de-duplicated PDF-URL candidates. Repository (green) copies first,
    since publisher bronze links often serve HTML to a non-browser client. Derived
    landing-page constructions come last, as a fallback for metadata with no pdf_url."""
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
    for u in green + other + derived_urls(w, up, doi):
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


def band(rec: dict) -> str:
    if rec["priority"] == PRIORITY_REALIZED:
        return "realized_fertility"
    if rec["priority"] == PRIORITY_DESIRE_INDEPENDENCE:
        return "desire_independence"
    return "stated_intention"


def main() -> None:
    PDF_DIR.mkdir(parents=True, exist_ok=True)
    LOG.parent.mkdir(parents=True, exist_ok=True)
    pool = load_pool()

    work_ids = [x["paperId"] for x in pool if str(x.get("paperId", "")).startswith("W")]
    meta = openalex_batch(work_ids)

    rows = []
    for x in pool:
        wid = x.get("paperId", "")
        w = meta.get(wid, {})
        oa = w.get("open_access") or {}
        doi = x.get("doi") or ""
        dest = PDF_DIR / f"{wid}__{slugify(x.get('title',''))}.pdf"
        status, detail, size, used_url = "no_oa_url", "", 0, ""
        if dest.exists():
            status, detail, size = "already_present", "skip", dest.stat().st_size
        else:
            up = unpaywall(doi)
            urls = candidate_urls(w, up, doi)
            tried = []
            # Cap raised from the B.1 script's 6: the derived constructions are appended
            # after the metadata URLs, so a low cap would truncate exactly the fallback
            # that rescues the no-pdf_url records.
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
        rows.append(
            {
                "work_id": wid,
                "doi": doi,
                "band": band(x),
                "cell": x.get("cell"),
                "in_stated_pool": x["in_stated"],
                "in_realized_pool": x["in_realized"],
                "outcome_level": x.get("outcome_level"),
                "year": x.get("year"),
                "venue": x.get("venue") or "",
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

    # The handoff splits on access_class, because the two classes need different humans.
    # `oa_but_blocked` is free to read and merely refuses a non-browser client (Wiley 403,
    # PMC's interstitial, Duke UP): anyone with a browser can fetch it, no entitlement
    # needed. `closed` genuinely requires the UChicago proxy or ILL. Reporting these as
    # one undifferentiated "missing" pile would overstate how much library access the
    # chapter actually needs.
    missing = [r for r in rows if not r["file"]]
    fields = ["band", "access_class", "doi", "work_id", "year", "venue", "detail", "title"]
    with open(MISSING, "w", newline="") as fh:
        wtr = csv.DictWriter(fh, fieldnames=fields)
        wtr.writeheader()
        for r in sorted(missing, key=lambda r: (r["band"] != "realized_fertility",
                                                r["band"] != "desire_independence",
                                                r["oa_status"] == "closed")):
            access_class = "closed" if r["oa_status"] == "closed" else "oa_but_blocked"
            wtr.writerow({**{k: r[k] for k in fields if k != "access_class"},
                          "access_class": access_class})

    # Reporting: the decisive 12 gets its own line. A union-only rate would hide
    # exactly the gap that matters -- see the module docstring.
    def rate(pred) -> tuple[int, int]:
        sel = [r for r in rows if pred(r)]
        return sum(1 for r in sel if r["file"]), len(sel)

    dec_n, dec_t = rate(lambda r: r["band"] in ("realized_fertility", "desire_independence"))
    all_n, all_t = rate(lambda _: True)
    print(f"DECISIVE 12: {dec_n}/{dec_t}")
    for b in ("realized_fertility", "desire_independence", "stated_intention"):
        n, t = rate(lambda r, b=b: r["band"] == b)
        if t:
            print(f"  {b}: {n}/{t}")
    print(f"FULL POOL (distinct works): {all_n}/{all_t}")
    print(f"log     -> {LOG.relative_to(ROOT)}")
    print(f"handoff -> {MISSING.relative_to(ROOT)} ({len(missing)} rows)")


if __name__ == "__main__":
    main()
