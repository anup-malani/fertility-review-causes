#!/usr/bin/env python3
"""
193_a17_fetch_oa.py — A.17, stage 5. Fetch the open records and measure every recovery rung.

Inherits `178_a24_fetch_oa.py`, which merged A.12's fetch and recovery passes because the standing
finding is that RUNG ORDER IS CHAPTER-SPECIFIC AND MUST BE MEASURED: B.6 built its recovery around
PMC, and on A.12's literature PMC returned zero while the cheap `locations` sweep did all the work.

**A.17 IS THE FIRST CHAPTER IN THE SERIES WHERE PMC SHOULD ACTUALLY PAY, AND THE PREDICTION IS
RECORDED BEFORE THE RUN.** A.12 was demography, A.24 was economics and communication, and PMC
returned nothing on either. A.17's jobs A4 and A5 are clinical — Human Reproduction, Fertility and
Sterility, BJOG, JAMA — which is precisely PMC's coverage. If the rung still returns zero here, that
is evidence the rung should be retired from the shared scaffold rather than carried by habit; if it
pays, it pays on the two jobs with the WORST OA rates (A4 at 55%), which is where recovery matters
most. Either outcome is a measurement.

Rung order, cheapest first:
  0  the `best_oa_location` URL OpenAlex nominates.
  1  every OTHER open location on the record — free, already in hand from 192_, and A.12's best rung.
  2  the `citation_pdf_url` meta tag on the landing page. One extra request per record.
  3  PMC via id-conversion. See the prediction above.
  4  Unpaywall by DOI. New rung, added because A.17's closed set is 32 records and Unpaywall
     sometimes carries a green copy OpenAlex has not indexed. Its yield is measured separately so it
     can be retired if it returns nothing.

**A 200 CARRYING HTML IS A BLOCKED ROUTE, NOT A CLOSED PAPER.** The PDF magic bytes are checked on
every fetch and an HTML body is recorded as `route_blocked`. A.12's first pass had 84 of 88 failures
in that class, and calling them "not obtainable" would have written a false ceiling into the chapter.
The distinction is load-bearing here because the closed set becomes the library wantlist, and a
blocked route belongs on a retry list rather than in front of a human with a proxy.

Output: literature/search-logs/{slug}-fetch-log.csv
        literature/pdfs/{slug}/{WID}__{title-slug}.pdf   (gitignored)
"""
import csv, json, os, re, subprocess, sys, time
from collections import Counter

SLUG = "art-access-fertility-recovery"
MAILTO = "shravanh@uchicago.edu"
UA = f"fertility-review/1.0 (mailto:{MAILTO})"
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
LOGS = os.path.join(ROOT, "literature", "search-logs")
EXTRACT = os.path.join(ROOT, "extraction")
OA = os.path.join(EXTRACT, f"{SLUG}-oa-status.json")
PDF_DIR = os.path.join(ROOT, "literature", "pdfs", SLUG)
OUT_LOG = os.path.join(LOGS, f"{SLUG}-fetch-log.csv")
OUT_MD = os.path.join(LOGS, f"{SLUG}-fetch-summary.md")


def openalex_key():
    k = os.environ.get("OPENALEX_API_KEY")
    if k:
        return k.strip()
    envp = os.path.join(ROOT, ".env")
    if os.path.exists(envp):
        for line in open(envp):
            if line.startswith("OPENALEX_API_KEY="):
                return line.split("=", 1)[1].strip()
    return ""


KEY = openalex_key()


def slugify(t):
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", (t or "").lower()))[:60].strip("-")


def get(url, timeout=60):
    try:
        r = subprocess.run(["curl", "-sL", "-m", str(timeout), "-A", UA, url],
                           capture_output=True, text=True)
        return r.stdout if r.returncode == 0 else None
    except Exception:
        return None


def fetch_pdf(url, dest):
    """(ok, note). PDF magic bytes checked: a 200 with an HTML body is a BLOCKED ROUTE, not a closed
    paper, and the two go to different places downstream."""
    if not url:
        return False, "no_url"
    try:
        r = subprocess.run(["curl", "-sL", "-m", "90", "-A", UA, "-o", dest, "-w", "%{http_code}",
                            url], capture_output=True, text=True)
        code = (r.stdout or "").strip()
    except Exception as e:
        return False, f"exception:{str(e)[:40]}"
    if not os.path.exists(dest) or os.path.getsize(dest) < 1024:
        if os.path.exists(dest):
            os.remove(dest)
        return False, f"empty_or_tiny:{code}"
    with open(dest, "rb") as fh:
        head = fh.read(5)
    if head[:4] != b"%PDF":
        os.remove(dest)
        return False, f"route_blocked:{code}"
    return True, f"ok:{code}"


def locations_of(wid):
    d = get(f"https://api.openalex.org/works/{wid}?select=locations,best_oa_location"
            f"&api_key={KEY}")
    if not d:
        return []
    try:
        j = json.loads(d)
    except Exception:
        return []
    out = []
    for l in (j.get("locations") or []):
        if l.get("is_oa"):
            out.append(l.get("pdf_url") or l.get("landing_page_url"))
    return [u for u in out if u]


def citation_pdf_url(landing):
    if not landing:
        return None
    html = get(landing, timeout=45)
    if not html:
        return None
    m = re.search(r'<meta[^>]+name=["\']citation_pdf_url["\'][^>]+content=["\']([^"\']+)', html, re.I)
    return m.group(1) if m else None


def pmc_pdf(doi):
    if not doi:
        return None
    # NCBI 301-redirects this to pmc.ncbi.nlm.nih.gov/tools/idconv/api/v1/articles/; curl -L
    # follows it, but the API WARNS when tool and email are absent, so both are sent.
    j = get("https://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/?ids=" + doi +
            f"&format=json&tool=fertility-review&email={MAILTO}")
    if not j:
        return None
    try:
        recs = json.loads(j).get("records") or []
    except Exception:
        return None
    for r in recs:
        if r.get("pmcid"):
            return f"https://www.ncbi.nlm.nih.gov/pmc/articles/{r['pmcid']}/pdf/"
    return None


def unpaywall_pdf(doi):
    if not doi:
        return None
    j = get(f"https://api.unpaywall.org/v2/{doi}?email={MAILTO}")
    if not j:
        return None
    try:
        d = json.loads(j)
    except Exception:
        return None
    loc = d.get("best_oa_location") or {}
    return loc.get("url_for_pdf") or loc.get("url")


def main():
    if not KEY:
        sys.stderr.write("ABORT: no OPENALEX_API_KEY.\n")
        sys.exit(3)
    rows = json.load(open(OA))
    os.makedirs(PDF_DIR, exist_ok=True)

    log, rung_hits, rung_found = [], Counter(), Counter()
    for i, r in enumerate(rows, 1):
        wid, doi = r["id"], r.get("doi")
        dest = os.path.join(PDF_DIR, f"{wid}__{slugify(r['title'])}.pdf")
        if os.path.exists(dest) and os.path.getsize(dest) > 1024:
            log.append(dict(id=wid, job=r["job"], doi=doi, rung="cached", ok=True,
                            note="already on disk", url=""))
            rung_hits["cached"] += 1
            continue

        attempts, got, used_rung, used_url, note = [], False, "", "", ""
        # rung 0 — the nominated best OA location
        cand = [("0_best_oa", r.get("best_url"))]
        # rung 1 — every other open location
        if not got:
            for u in locations_of(wid):
                if u != r.get("best_url"):
                    cand.append(("1_other_locations", u))
        for rung, url in cand:
            if url:
                rung_found[rung] += 1
            ok, n = fetch_pdf(url, dest)
            attempts.append((rung, n))
            if ok:
                got, used_rung, used_url, note = True, rung, url, n
                break
        # rung 2 — citation_pdf_url on the landing page
        if not got:
            u = citation_pdf_url(r.get("best_url"))
            if u:
                rung_found["2_citation_meta"] += 1
            ok, n = fetch_pdf(u, dest)
            attempts.append(("2_citation_meta", n))
            if ok:
                got, used_rung, used_url, note = True, "2_citation_meta", u, n
        # rung 3 — PMC. Predicted to pay on this chapter for the first time in the series.
        # NOTE the two counters: a rung that FINDS a url whose fetch is then blocked is a LIVE rung,
        # not a dead one. Counting only successes would retire a working rung for a publisher's
        # bot-block, which is refusals-read-as-zeros wearing a retrieval costume.
        if not got:
            u = pmc_pdf(doi)
            if u:
                rung_found["3_pmc"] += 1
            ok, n = fetch_pdf(u, dest)
            attempts.append(("3_pmc", n))
            if ok:
                got, used_rung, used_url, note = True, "3_pmc", u, n
        # rung 4 — Unpaywall
        if not got:
            u = unpaywall_pdf(doi)
            if u:
                rung_found["4_unpaywall"] += 1
            ok, n = fetch_pdf(u, dest)
            attempts.append(("4_unpaywall", n))
            if ok:
                got, used_rung, used_url, note = True, "4_unpaywall", u, n

        if got:
            rung_hits[used_rung] += 1
        else:
            blocked = any(a[1].startswith("route_blocked") for a in attempts)
            note = "route_blocked" if blocked else "no_route"
            rung_hits["FAILED_" + note] += 1
        log.append(dict(id=wid, job=r["job"], doi=doi, rung=used_rung or "none", ok=got,
                        note=note or ";".join(f"{a}:{b}" for a, b in attempts)[:180],
                        url=used_url))
        if i % 20 == 0:
            print(f"  ...{i}/{len(rows)}  got={sum(1 for x in log if x['ok'])}")
        time.sleep(0.1)

    with open(OUT_LOG, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["id", "job", "doi", "rung", "ok", "note", "url"])
        w.writeheader()
        w.writerows(log)

    got_n = sum(1 for x in log if x["ok"])
    by_job = {}
    for x in log:
        j = by_job.setdefault(x["job"], [0, 0])
        j[1] += 1
        if x["ok"]:
            j[0] += 1
    pc = lambda a, b: f"{a / max(b, 1):.0%}"
    L = [f"# Stage 5 fetch — {SLUG} (A.17)", "",
         f"**{got_n} of {len(log)} retrieved ({pc(got_n, len(log))}).** Files land in "
         f"`literature/pdfs/{SLUG}/` under the house naming convention and are gitignored.", "",
         "## Yield per rung — measured, not assumed", "",
         "The standing finding is that rung order is chapter-specific. B.6 built its recovery around "
         "PMC; on A.12's demography literature PMC returned zero while the free `locations` sweep did "
         "all the work. **A.17 was predicted, before this run, to be the first chapter where PMC "
         "pays** — jobs A4 and A5 are clinical, which is PMC's coverage, and they have the worst OA "
         "rates. The table below settles it either way.", "",
         "**Two columns, and the difference between them is the finding.** `found a URL` is whether "
         "the rung located a candidate; `fetched` is whether that candidate returned PDF bytes. A "
         "rung that finds URLs which are then blocked by a publisher's bot defence is a LIVE rung "
         "being defeated downstream — retiring it on a zero in the second column would be "
         "refusals-read-as-zeros in retrieval costume.", "",
         "| rung | found a URL | fetched | cost |", "|---|---|---|---|"]
    COST = {"cached": "free (already on disk)", "0_best_oa": "free — already in hand from 192_",
            "1_other_locations": "free — one API call already made",
            "2_citation_meta": "one landing-page request per record",
            "3_pmc": "one id-conversion request per record",
            "4_unpaywall": "one API request per record"}
    for k, v in rung_hits.most_common():
        if not k.startswith("FAILED"):
            L.append(f"| `{k}` | {rung_found.get(k, '—')} | {v} | {COST.get(k, '')} |")
    L += ["", "| failure class | records | meaning |", "|---|---|---|"]
    for k in sorted(set(rung_found) - set(rung_hits)):
        L.append(f"| `{k}` | {rung_found[k]} | **0** | {COST.get(k, '')} |")
    L += [""]
    for k, v in rung_hits.most_common():
        if k.startswith("FAILED"):
            mean = ("a 200 carrying HTML — the route is blocked, the paper is not necessarily closed; "
                    "these go on a RETRY list, not to a human with a proxy"
                    if "route_blocked" in k else
                    "no open route found at any rung; these are the library wantlist")
            L.append(f"| `{k}` | {v} | {mean} |")
    L += ["", "## Retrieved, by job", "",
          "Read this by row. The jobs are not interchangeable: A1 is the counterfactual set the "
          "chapter's headline number depends on, and A2 is the identified evidence that no other "
          "route can recover.", "",
          "| job | retrieved | wanted | rate |", "|---|---|---|---|"]
    for j in sorted(by_job):
        g, t = by_job[j]
        L.append(f"| `{j}` | {g} | {t} | **{pc(g, t)}** |")
    L += ["", f"| **total** | **{got_n}** | **{len(log)}** | {pc(got_n, len(log))} |", ""]
    open(OUT_MD, "w").write("\n".join(L) + "\n")

    print(f"\nretrieved={got_n}/{len(log)} ({pc(got_n, len(log))})")
    for k, v in rung_hits.most_common():
        print(f"  fetched {k:24} {v}")
    for k, v in rung_found.most_common():
        print(f"  found   {k:24} {v}")
    print(f"-> {os.path.relpath(OUT_MD, ROOT)}")


if __name__ == "__main__":
    main()
