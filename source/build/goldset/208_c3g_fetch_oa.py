#!/usr/bin/env python3
"""
208_c3g_fetch_oa.py — C.3.g, stage 5b. Fetch the open records and measure every recovery rung.

Inherits `193_a17_fetch_oa.py`. Two things change and both are chapter-specific by design, because
the standing finding is that RUNG ORDER MUST BE MEASURED RATHER THAN INHERITED: B.6 built its
recovery around PMC and A.12 found PMC returning zero while the free `locations` sweep did the work;
A.17 predicted PMC would finally pay on a clinical literature.

**NEW RUNG: WORKING-PAPER REPOSITORIES, and the prediction is recorded before the run.** An unusual
share of this chapter's records are paywalled articles with a free NBER, FEDS, SSRN or
institutional-repository twin — the version-pair structure that has recurred at every stage here.
NBER and FEDS both mint DOIs whose shape determines the PDF URL exactly, so the rung is deterministic
rather than a search. It is counted separately so it can be justified or dropped on evidence.

**PMC IS PREDICTED TO RETURN ZERO.** Economics, sociology and household finance; PMC indexes
biomedicine. A third zero after A.12 and A.24 is grounds to retire the rung from the shared scaffold
rather than carry it by habit. Retained for this run precisely so the third measurement exists.

**TWO COUNTERS PER RUNG, NOT ONE.** A rung that FOUND 65 urls and FETCHED 0 looks identical to a
dead rung if only fetches are counted, and on A.17 that is exactly what PMC and Unpaywall looked
like. `found` and `fetched` are reported separately for every rung.

**A 200 CARRYING HTML IS A BLOCKED ROUTE, NOT A CLOSED PAPER.** PDF magic bytes are checked on every
fetch and an HTML body is recorded as `route_blocked`. The distinction is load-bearing because the
failures become the library wantlist, and a blocked route belongs in a browser rather than in front
of a human with a proxy. This chapter has already met it: WUSTL Open Scholarship and SAGE both
returned 403 to curl on open-access content.

Output: literature/search-logs/{slug}-fetch-log.csv
        literature/search-logs/{slug}-fetch-summary.md
        literature/pdfs/{slug}/{WID}__{title-slug}.pdf   (gitignored)
"""
import csv, json, os, re, subprocess, sys, time
from collections import Counter

SLUG = "student-debt-household-formation"
MAILTO = "shravanh@uchicago.edu"
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
      "Chrome/120.0.0.0 Safari/537.36")
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


def get(url, timeout=45):
    try:
        r = subprocess.run(["curl", "-sL", "-m", str(timeout), "-A", UA, url],
                           capture_output=True, text=True)
        return r.stdout if r.returncode == 0 else None
    except Exception:
        return None


def fetch_pdf(url, dest):
    """(ok, note). A 200 with an HTML body is a BLOCKED ROUTE, not a closed paper."""
    if not url:
        return False, "no_url"
    try:
        r = subprocess.run(["curl", "-sL", "-m", "90", "-A", UA,
                            "-H", "Accept: application/pdf,text/html;q=0.8,*/*;q=0.5",
                            "-o", dest, "-w", "%{http_code}", url],
                           capture_output=True, text=True)
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
    d = get(f"https://api.openalex.org/works/{wid}?select=locations,best_oa_location&api_key={KEY}")
    try:
        j = json.loads(d) if d else {}
    except Exception:
        return []
    out = []
    for l in (j.get("locations") or []):
        if l.get("is_oa"):
            u = l.get("pdf_url") or l.get("landing_page_url")
            if u:
                out.append(u)
    return out


def citation_pdf_url(landing):
    if not landing:
        return None
    html = get(landing, timeout=45)
    if not html:
        return None
    m = re.search(r'<meta[^>]+name=["\']citation_pdf_url["\'][^>]+content=["\']([^"\']+)', html, re.I)
    return m.group(1) if m else None


def working_paper_urls(doi, landing):
    """DETERMINISTIC free-copy URLs for the working-paper series this literature lives in.

    NBER and FEDS both mint DOIs whose shape fixes the PDF path exactly, so this is a construction
    rather than a search — no request is spent discovering it. The rung exists because C.3.g's
    records are disproportionately paywalled articles with a free working-paper twin."""
    out = []
    d = (doi or "").lower()
    m = re.match(r"10\.3386/(w\d+)$", d)                      # NBER
    if m:
        w = m.group(1)
        out.append(f"https://www.nber.org/system/files/working_papers/{w}/{w}.pdf")
    m = re.match(r"10\.17016/feds\.(\d{4})\.(\d+)$", d)       # Fed FEDS series
    if m:
        yr, num = m.group(1), m.group(2).zfill(3)
        out.append(f"https://www.federalreserve.gov/econres/feds/files/{yr}{num}pap.pdf")
    m = re.match(r"10\.17016/2380-7172\.(\d+)$", d)           # FEDS Notes
    if m:
        out.append(f"https://www.federalreserve.gov/econres/notes/feds-notes/files/{m.group(1)}.pdf")
    if landing and "repec" in landing.lower():
        out.append(landing)
    return out


def pmc_pdf(doi):
    if not doi:
        return None
    j = get("https://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/?ids=" + doi +
            f"&format=json&tool=fertility-review&email={MAILTO}")
    try:
        recs = json.loads(j).get("records") or [] if j else []
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
    try:
        d = json.loads(j) if j else {}
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
    log, rung_found, rung_fetched = [], Counter(), Counter()

    for i, r in enumerate(rows, 1):
        wid, doi = r["id"], r.get("doi")
        dest = os.path.join(PDF_DIR, f"{wid}__{slugify(r['title'])}.pdf")
        if os.path.exists(dest) and os.path.getsize(dest) > 1024:
            log.append(dict(id=wid, job=r["job"], doi=doi or "", rung="cached", ok=True,
                            note="already on disk", url="", title=r["title"][:70]))
            rung_fetched["cached"] += 1
            continue

        cand = [("0_best_oa", r.get("best_url"))]
        for u in locations_of(wid):
            if u != r.get("best_url"):
                cand.append(("1_other_locations", u))
        for u in working_paper_urls(doi, r.get("best_url")):
            cand.append(("2_working_paper", u))
        cpu = citation_pdf_url(r.get("best_url"))
        if cpu:
            cand.append(("3_citation_meta", cpu))
        pm = pmc_pdf(doi)
        if pm:
            cand.append(("4_pmc", pm))
        up = unpaywall_pdf(doi)
        if up:
            cand.append(("5_unpaywall", up))

        got, used_rung, used_url, note = False, "", "", ""
        seen = set()
        for rung, url in cand:
            if not url or url in seen:
                continue
            seen.add(url)
            rung_found[rung] += 1
            ok, n = fetch_pdf(url, dest)
            if ok:
                got, used_rung, used_url, note = True, rung, url, n
                rung_fetched[rung] += 1
                break
            note = n
        log.append(dict(id=wid, job=r["job"], doi=doi or "", rung=used_rung or "none",
                        ok=got, note=note or "no_candidate_url", url=used_url,
                        title=r["title"][:70]))
        if i % 15 == 0:
            print(f"  {i}/{len(rows)} — {sum(1 for x in log if x['ok'])} retrieved")
        time.sleep(0.1)

    with open(OUT_LOG, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["id", "job", "title", "doi", "rung", "ok", "note", "url"])
        w.writeheader()
        for row in log:
            w.writerow(row)

    n_ok = sum(1 for x in log if x["ok"])
    by_job = {}
    for r in rows:
        j = r["job"]
        by_job.setdefault(j, [0, 0])
        by_job[j][0] += 1
    for x in log:
        if x["ok"]:
            by_job[x["job"]][1] += 1
    fails = [x for x in log if not x["ok"]]
    fail_kind = Counter(x["note"].split(":")[0] for x in fails)
    oa_flag = {r["id"]: r["is_oa"] for r in rows}
    oa_but_failed = [x for x in fails if oa_flag.get(x["id"])]
    pc = lambda n, d: f"{n / d:.0%}" if d else "n/a"

    L = [f"# Stage 5b fetch — {SLUG} (C.3.g)", "",
         f"**Generated by:** `source/build/goldset/208_c3g_fetch_oa.py`", "",
         f"**{n_ok} of {len(rows)} retrieved ({pc(n_ok, len(rows))}).** OpenAlex flagged "
         f"{sum(1 for r in rows if r['is_oa'])} as open access, so the OA rate was a ceiling of "
         f"{pc(sum(1 for r in rows if r['is_oa']), len(rows))} and this run reached "
         f"{pc(n_ok, len(rows))} of the whole set.", "",
         "## Retrieval by job — the number that matters is J1", "",
         "| Job | Wanted | Retrieved | |", "|---|---|---|---|"]
    for j in sorted(by_job):
        w_, g_ = by_job[j]
        L.append(f"| `{j}` | {w_} | {g_} | {pc(g_, w_)} |")
    L += ["", "## Rung yield — found against fetched", "",
          "Two counters, because a rung that FOUND urls and FETCHED nothing looks identical to a "
          "dead rung when only fetches are counted. On A.17, PMC and Unpaywall looked dead at 0 "
          "fetches while having found 27 and 65 urls between them.", "",
          "| Rung | URLs found | PDFs fetched | Hit rate |", "|---|---|---|---|"]
    for rung in sorted(set(rung_found) | set(rung_fetched)):
        f_, g_ = rung_found.get(rung, 0), rung_fetched.get(rung, 0)
        L.append(f"| `{rung}` | {f_} | {g_} | {pc(g_, f_)} |")
    L += ["", "## Failures, by kind", "",
          "| Kind | n | Reading |", "|---|---|---|"]
    READ = {"route_blocked": "a 200 with an HTML body — **open content behind bot defence**; a "
                             "browser-job, not a proxy-job",
            "no_candidate_url": "no open location anywhere — a genuine closed paper, or a record "
                                "with no DOI and no repository copy",
            "empty_or_tiny": "a truncated or empty response; usually a redirect to a splash page",
            "exception": "transport failure — UNCONFIRMED, not closed"}
    for k, n in fail_kind.most_common():
        L.append(f"| `{k}` | {n} | {READ.get(k, '')} |")
    L += ["", f"**{len(oa_but_failed)} records OpenAlex calls OPEN ACCESS could not be fetched.** "
          "That gap is the honest measure of how much of the open literature is unreachable by "
          "script, and it is the population the browser handoff exists for.", ""]
    open(OUT_MD, "w").write("\n".join(L) + "\n")
    print(f"\nretrieved {n_ok}/{len(rows)} ({pc(n_ok, len(rows))})")
    print("rung found  :", dict(rung_found))
    print("rung fetched:", dict(rung_fetched))
    print("fail kinds  :", dict(fail_kind))
    print(f"-> {os.path.relpath(OUT_MD, ROOT)}")


if __name__ == "__main__":
    main()
