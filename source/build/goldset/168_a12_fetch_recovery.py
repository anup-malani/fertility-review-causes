#!/usr/bin/env python3
"""
168_a12_fetch_recovery.py — A.12, stage 5. Recovery rung for records the first fetch could not reach.

Inherits the intent of `141_b6_fetch_pmc_efetch.py`: after the primary fetch, try the routes the
primary fetch did not.

**WHY A RECOVERY RUNG IS NEEDED HERE, STATED AS A NUMBER.** 167 attempted 142 records that OpenAlex
marks open and retrieved 54. Of the 88 failures, **84 were HTML interstitials** — the publisher
returned a landing page with a 200 status instead of a PDF. Under the standing discipline that is a
BLOCKED ROUTE, not a closed paper, and the correct response is to try other routes before handing the
record to a human.

Three routes, in order of cost:

  1. **Every OA location, not just the best one.** 166 recorded `best_oa_location` only, and
     OpenAlex's "best" is chosen by version precedence, not by whether a scripted GET can reach it. A
     record whose publisher landing page blocks automation frequently has a green repository copy —
     PMC, a university repository, RePEc, arXiv — sitting in `locations` unread. This is the cheapest
     rung and it costs one API call per record.
  2. **PubMed Central by PMCID.** PMC serves PDFs to scripted clients where publishers do not, and
     much of this chapter's ART and epidemiology literature is deposited there.
  3. **Landing-page scrape for a `citation_pdf_url` meta tag.** Publishers that block a direct PDF
     GET often still advertise the PDF path in the landing page's Highwire metadata. This is the
     last automated rung; anything failing it goes to the human list.

Every rung records WHICH route succeeded, so the next chapter can order them by observed yield rather
than by guess.

TIMEOUTS AND CAPS ARE STATED BECAUSE THEY BOUND THE RESULT. Each HTTP attempt is capped at 25s and
each record tries at most FOUR alternate locations. The first run of this script used 90s timeouts and
no cap and did not finish in ten minutes — a blocked publisher does not fail fast, it hangs. A record
reported here as still-blocked is therefore 'not reachable within this budget', not 'not reachable'.
The count of alternate locations tried is recorded per record so the budget's cost is visible.

Output: extraction/{slug}-pdf-recovery-log.csv
        literature/pdfs/{slug}/*.pdf and *.txt   (gitignored)
"""
import csv, json, os, re, subprocess, time

SLUG = "twinning-multiple-births"
MAILTO = "shravanh@uchicago.edu"
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) fertility-review/1.0 "
      f"(mailto:{MAILTO})")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
EXTRACT = os.path.join(ROOT, "extraction")
LOGS = os.path.join(ROOT, "literature", "search-logs")
PDF_DIR = os.path.join(ROOT, "literature", "pdfs", SLUG)
PRIOR = os.path.join(EXTRACT, f"{SLUG}-pdf-retrieval-log.csv")
SCREENED = os.path.join(LOGS, f"{SLUG}-screened.json")
OUT = os.path.join(EXTRACT, f"{SLUG}-pdf-recovery-log.csv")


def slugify(t):
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", (t or "").lower()))[:60].strip("-")


def get(url, dest=None, timeout=25):
    args = ["curl", "-sL", "-m", str(timeout), "-A", UA]
    if dest:
        args += ["-o", dest, "-w", "%{http_code}"]
    args.append(url)
    try:
        r = subprocess.run(args, capture_output=True, text=True, timeout=timeout + 30)
    except Exception:
        return None
    return r.stdout


def try_pdf(url, dest, timeout=25):
    """True only if the bytes are actually a PDF."""
    if not url:
        return False
    get(url, dest, timeout=timeout)
    if not os.path.exists(dest) or os.path.getsize(dest) < 1000:
        if os.path.exists(dest):
            os.remove(dest)
        return False
    with open(dest, "rb") as fh:
        if fh.read(4) != b"%PDF":
            os.remove(dest)
            return False
    return True


def all_locations(wid):
    d = get(f"https://api.openalex.org/works/{wid}?select=locations,ids,best_oa_location"
            f"&mailto={MAILTO}")
    try:
        w = json.loads(d)
    except Exception:
        return [], None
    urls, pmcid = [], None
    ids = w.get("ids") or {}
    if ids.get("pmcid"):
        pmcid = str(ids["pmcid"]).rsplit("/", 1)[-1]
    for loc in (w.get("locations") or []):
        if loc.get("pdf_url"):
            urls.append(loc["pdf_url"])
        elif loc.get("landing_page_url"):
            urls.append(loc["landing_page_url"])
    seen, out = set(), []
    for u in urls:
        if u not in seen:
            seen.add(u); out.append(u)
    return out, pmcid


def citation_pdf_url(landing):
    html = get(landing, timeout=20)
    if not html:
        return None
    m = re.search(r'<meta[^>]+name=["\']citation_pdf_url["\'][^>]+content=["\']([^"\']+)', html, re.I)
    if not m:
        m = re.search(r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+name=["\']citation_pdf_url', html, re.I)
    return m.group(1) if m else None


def extract_text(pdf, txt):
    for cmd in (["pdftotext", "-q", pdf, txt], ["/opt/homebrew/bin/pdftotext", "-q", pdf, txt]):
        try:
            subprocess.run(cmd, capture_output=True, timeout=120)
        except Exception:
            continue
        if os.path.exists(txt) and os.path.getsize(txt) > 500:
            return "OK"
        if os.path.exists(txt):
            return "NO_TEXT_LAYER"
    return "EXTRACT_FAILED"


def main():
    prior = list(csv.DictReader(open(PRIOR)))
    meta = {r["id"]: r for r in json.load(open(SCREENED))}
    failed = [r for r in prior if r["fetch"] == "FAILED"]
    print(f"recovery targets: {len(failed)} records the primary fetch could not reach\n")
    rows, won = [], 0
    for r in failed:
        wid = r["id"]
        m = meta.get(wid, {})
        base = f"{wid}__{slugify(m.get('title'))}"
        pdf = os.path.join(PDF_DIR, base + ".pdf")
        txt = os.path.join(PDF_DIR, base + ".txt")
        route, ok = None, False
        locs, pmcid = all_locations(wid)
        for u in locs[:4]:                 # cap: 4 alternate routes per record, reported below
            if u == r.get("url"):
                continue                      # already tried in 167
            if try_pdf(u, pdf):
                route, ok = f"alt_location:{u[:60]}", True
                break
        if not ok and pmcid:
            u = f"https://www.ncbi.nlm.nih.gov/pmc/articles/{pmcid}/pdf/"
            if try_pdf(u, pdf):
                route, ok = f"pmc:{pmcid}", True
        if not ok:
            land = r.get("url")
            if land:
                cu = citation_pdf_url(land)
                if cu and try_pdf(cu, pdf):
                    route, ok = f"citation_pdf_url:{cu[:50]}", True
        tstat = extract_text(pdf, txt) if ok else "-"
        if ok:
            won += 1
        rows.append(dict(id=wid, cell=m.get("cell"), year=m.get("year"),
                         title=(m.get("title") or "")[:90],
                         recovered=("YES" if ok else "no"), route=route or "-",
                         n_alt_locations=len(locs), pmcid=pmcid or "-", text=tstat))
        print(f"  {'RECOVERED' if ok else 'still-blocked':<14} "
              f"{(route or '')[:44]:<44} {(m.get('title') or '')[:44]}")
        time.sleep(0.2)
    with open(OUT, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)
    from collections import Counter
    print(f"\nrecovered={won} of {len(failed)}")
    print("by route:", dict(Counter(r["route"].split(":")[0] for r in rows if r["recovered"] == "YES")))
    print(f"-> {os.path.relpath(OUT, ROOT)}")


if __name__ == "__main__":
    main()
