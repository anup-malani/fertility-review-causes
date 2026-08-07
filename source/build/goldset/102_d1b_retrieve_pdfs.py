#!/usr/bin/env python3
"""TICK-063: retrieve open-access PDFs for the D.1.b priority strata.

Mirrors 82_d3b_retrieve_pdfs.py (OpenAlex all-locations + Unpaywall + Europe PMC, %PDF
magic-byte verification, idempotent) with three D.1.b-specific differences:

  1. THREE pooling files, not two. D.1.b's outcome levels are realized fertility, stated
     intention or ideal, and family-formation behaviour, and the A1 scope forbids pooling
     them. A work appearing at more than one level is downloaded once and reported under
     every membership it holds.

  2. A FOURTH retrieval target that is not a pooling set: the Wall-5 sample. The 40
     `MECHANISM_UNRESOLVED_SCHOOLING` records drawn into the gate exist to answer a
     question that CANNOT be answered from an abstract -- whether a schooling estimate
     decomposes ideational content from wage returns. The chapter's headline ratio is
     wrong until they are read, so they are retrieved at priority 2, ahead of the two
     softer outcome levels. Retrieving a paper in order to reclassify it is unusual and
     is the reason this band exists.

  3. Retrieval rate is reported SEPARATELY per band, never as a union. A headline rate
     over the union hides a gap in the stratum that matters, which is the failure mode
     that now caps the B.1 chapter at 20/95 -- a pooled estimate resting on five studies
     selected, in effect, on open-access status.

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

SLUG = "caldwell-wealth-flows-westernization"
ROOT = Path(__file__).resolve().parents[3]
# Partial-screen aware: prefer the complete assembly, fall back to the PARTIAL one and
# carry the marker into the output filenames so a retrieval log built from half a screen
# is never mistaken for the finished one.
_complete = (ROOT / "output" / f"{SLUG}-estimand-ready-realized.json").exists()
SFX = "" if _complete else "-PARTIAL"
POOL_REALIZED = ROOT / "output" / f"{SLUG}{SFX}-estimand-ready-realized.json"
POOL_STATED = ROOT / "output" / f"{SLUG}{SFX}-estimand-ready-stated.json"
POOL_FAMILY = ROOT / "output" / f"{SLUG}{SFX}-estimand-ready-family-formation.json"
GATE_CSV = ROOT / "extraction" / f"{SLUG}{SFX}-ra-gate.csv"
PDF_DIR = ROOT / "literature" / "pdfs" / SLUG
LOG = ROOT / "extraction" / f"{SLUG}{SFX}-pdf-retrieval-log.csv"
MISSING = ROOT / "extraction" / f"{SLUG}{SFX}-missing-pdf-dois.csv"
MAILTO = "shravanh@uchicago.edu"


def _openalex_key():
    """See decisions note in 96_d1b_tier_ab_frame.py: `mailto` identifies but does not
    authenticate, and an unauthenticated caller draws on a shared anonymous daily budget
    that a batch retrieval exhausts. The funded key lives in a gitignored `.env`."""
    import os
    k = os.environ.get("OPENALEX_API_KEY")
    if k:
        return k.strip()
    envf = ROOT / ".env"
    if envf.exists():
        for line in envf.read_text().splitlines():
            if line.startswith("OPENALEX_API_KEY="):
                return line.split("=", 1)[1].strip()
    return None


_OPENALEX_KEY = _openalex_key()
UA = "Mozilla/5.0 (fertility-review-causes; mailto:shravanh@uchicago.edu)"

# Priority 0 and 1 are what the chapter's verdict rests on; 2 is what its headline number
# rests on; 3 and 4 are the softer outcome levels.
PRIORITY_DIFFUSION_INDEP = 0   # the value-added cell: designs separating ideation from structure
PRIORITY_REALIZED = 1          # the decisive outcome level
PRIORITY_WALL5 = 2             # read to reclassify, not to extract an effect
PRIORITY_STATED = 3
PRIORITY_FAMILY = 4
BAND_NAMES = {0: "diffusion_independent_of_structure", 1: "realized_fertility",
              2: "wall5_unresolved_schooling", 3: "stated_intention_or_ideal",
              4: "family_formation_behaviour"}


def slugify(title: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", (title or "").lower()).strip("-")
    return s[:60] or "untitled"


def load_pool() -> list[dict]:
    """Merge the three pooling files plus the Wall-5 gate sample into one download
    worklist, preserving membership.

    Deduplicates on paperId so a work at more than one outcome level is fetched once, and
    stamps each record with its priority band and its per-level membership flags. A record
    keeps the STRONGEST (lowest) priority it qualifies for, so a diffusion-independent
    study that also reports realized fertility is fetched first, not third.
    """
    import csv as _csv

    def _load(path):
        return json.load(open(path)) if path.exists() else []

    realized, stated, family = _load(POOL_REALIZED), _load(POOL_STATED), _load(POOL_FAMILY)

    merged: dict[str, dict] = {}

    def _add(rec, prio, **flags):
        pid = rec.get("paperId")
        if not pid:
            return
        if pid in merged:
            merged[pid]["priority"] = min(merged[pid]["priority"], prio)
            merged[pid].update({k: v or merged[pid].get(k, False) for k, v in flags.items()})
            return
        merged[pid] = dict(rec, priority=prio, in_realized=False, in_stated=False,
                           in_family=False, in_wall5=False)
        merged[pid].update(flags)

    for rec in realized:
        prio = (PRIORITY_DIFFUSION_INDEP
                if rec.get("estimand_cell") == "DIFFUSION_INDEPENDENT_OF_STRUCTURE"
                else PRIORITY_REALIZED)
        _add(rec, prio, in_realized=True)
    for rec in stated:
        prio = (PRIORITY_DIFFUSION_INDEP
                if rec.get("estimand_cell") == "DIFFUSION_INDEPENDENT_OF_STRUCTURE"
                else PRIORITY_STATED)
        _add(rec, prio, in_stated=True)
    for rec in family:
        prio = (PRIORITY_DIFFUSION_INDEP
                if rec.get("estimand_cell") == "DIFFUSION_INDEPENDENT_OF_STRUCTURE"
                else PRIORITY_FAMILY)
        _add(rec, prio, in_family=True)

    # The Wall-5 band comes from the GATE worksheet, not from a pooling file, because these
    # records are not in any pool and by construction never will be while they stay
    # unresolved. They are retrieved to be READ, so that the unresolved-vs-decomposed ratio
    # is measured from full text rather than from abstracts that structurally cannot show it.
    if GATE_CSV.exists():
        with GATE_CSV.open(encoding="utf-8") as fh:
            for r in _csv.DictReader(fh):
                if r.get("stratum") not in ("B_WALL5_SCHOOLING", "B2_PRIMARY_SCHOOLING"):
                    continue
                _add({"paperId": r["work_id"], "doi": r.get("doi") or "",
                      "title": r.get("title") or "", "year": (int(r["year"]) if
                      (r.get("year") or "").isdigit() else None),
                      "estimand_cell": r.get("screen_cell")},
                     PRIORITY_WALL5, in_wall5=True)

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
            f"&mailto={MAILTO}" + (f"&api_key={_OPENALEX_KEY}" if _OPENALEX_KEY else "")
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


def europepmc_urls(doi: str) -> list[str]:
    """Europe PMC's `?pdf=render` endpoint, promoted to a first-class source.

    Found during the TICK-049 sample sweep and it is the single most productive source in
    this project: it served PNAS, MDPI and Springer PDFs whose publisher sites return
    Cloudflare 403 to a non-browser client. Europe PMC mirrors the deposited full text and
    does not bot-block, so it routes around exactly the wall that stopped B.1.

    Caveat that must travel with it: what Europe PMC holds is often the ACCEPTED
    MANUSCRIPT, not the version of record. The ingest step records version status.
    """
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
    for u in green + other + europepmc_urls(doi) + derived_urls(w, up, doi):
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
    return BAND_NAMES.get(rec["priority"], "unknown")


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
                "cell": x.get("estimand_cell"),
                "in_realized_pool": x["in_realized"],
                "in_stated_pool": x["in_stated"],
                "in_family_pool": x["in_family"],
                "in_wall5_sample": x["in_wall5"],
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
        band_order = {n: i for i, n in BAND_NAMES.items()}
        for r in sorted(missing, key=lambda r: (band_order.get(r["band"], 99),
                                                r["oa_status"] == "closed")):
            access_class = "closed" if r["oa_status"] == "closed" else "oa_but_blocked"
            wtr.writerow({**{k: r[k] for k in fields if k != "access_class"},
                          "access_class": access_class})

    # Reporting: every band gets its own line and there is no union headline. A pooled
    # rate is what let B.1 read as "20/95 retrieved" when the real fact was that its five
    # surviving studies were selected on open-access status.
    def rate(pred):
        sel = [r for r in rows if pred(r)]
        return sum(1 for r in sel if r["file"]), len(sel)

    print(f"retrieval log -> {LOG.relative_to(ROOT)}")
    if SFX:
        print("NOTE: built from a PARTIAL screen; pools will grow when the screen completes.")
    for i in sorted(BAND_NAMES):
        n, t = rate(lambda r, b=BAND_NAMES[i]: r["band"] == b)
        if t:
            print(f"  {BAND_NAMES[i]:34} {n:3}/{t:<3} ({100*n/t:.0f}%)")
    blocked = sum(1 for r in rows if not r["file"] and r["oa_status"] != "closed")
    closed = sum(1 for r in rows if not r["file"] and r["oa_status"] == "closed")
    print(f"  handoff: {blocked} oa_but_blocked (needs a browser), {closed} closed (needs the proxy)")
    print(f"  -> {MISSING.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
