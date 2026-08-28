#!/usr/bin/env python3
"""
233_a23_fetch_fulltext.py — A.23, stage 5b. Fetch the queue and measure every recovery rung.

Inherits `208_c3g_fetch_oa.py`. Three things change, and each is a response to something the last
two chapters' fetch logs actually showed rather than a refinement for its own sake.

**1. A BLOCKED PDF ROUTE IS NOT A BLOCKED PAPER — ASK WHAT THE 200 CONTAINED.**
C.3.g recorded 33 `route_blocked` failures: a 200 whose body was HTML rather than a PDF. That check
was right to reject the body as a PDF and wrong to stop there, because for part of this literature
the HTML body IS the article — Demographic Research, PLOS, Frontiers, MDPI and Springer's open
titles all serve complete full text as a page. Those 33 went onto a human's worklist while the text
the extractor needed was already in the response.

So every non-PDF 200 is now examined instead of discarded, and admitted as `html_text` only if it
passes a floor that an abstract page cannot: **2,500 words of stripped body text AND at least three
distinct article section headings.** The floor exists because of the PMC finding — a plain PMC page
returns 200 carrying a 23-word JavaScript shell, and a fetcher that reads status codes calls that a
success. Word counts are written to the log for every admission so the rule can be audited rather
than trusted, and `html_text` is reported as its OWN outcome, never folded into the PDF count.

**2. RUNGS ARE EVALUATED LAZILY, AND A THIRD COUNTER MAKES THAT READABLE.**
C.3.g built every candidate url before trying any of them, spending a landing-page fetch, a PMC
lookup and an Unpaywall lookup on records the first rung had already served. Rungs are now generated
in order and stop at the first success. That changes what `found` means — a late rung is only ever
asked about records the earlier rungs failed on — so a third counter, `reached`, records how many
records got as far as asking. `found 0 / reached 12` and `found 27 / fetched 0` are different
failures and the A.17 finding was that they must not look alike.

**3. THE DETERMINISTIC RUNGS COME FIRST AND COST NOTHING.**
`232` counted their populations before any request was spent: 8 Demographic Research articles, 6
MPIDR working papers and technical reports, 5 OSF/SocArXiv preprints, 3 NBER papers. All four paths
are fixed by the shape of the DOI. The MPIDR pair is the point worth carrying forward — those 14
`10.4054` records are two publishers' objects under one prefix, and a rung written at the prefix
would have taken the 8 and silently dropped the 6.

**THE RUNG THAT DELIVERED EACH FILE IS WRITTEN DOWN, BECAUSE THE CACHE ERASES IT OTHERWISE.**
A second run over a populated `literature/pdfs/` directory does no rung work, so every counter
collapses into `cached` and the summary reports that nothing delivered anything. That is a
reproducibility defect, not a cosmetic one: the artefact of record would depend on whether the
directory happened to be empty. Each success now writes its rung and url to
`{slug}-fetch-provenance.json`, and the summary reports cumulative attribution from that file.

**A RUNG CAN BE REDUNDANT RATHER THAN EMPTY, AND ONE COUNTER CANNOT TELL THEM APART.**
The first run of this script reported Unpaywall as `found 0 / reached 352` — the shape of a rung
with nothing to offer this literature, and grounds to retire it. It was wrong. Hand-testing returned
a url for most records carrying a DOI; the urls were filtered out because an earlier rung had
already tried them, and the filter ran BEFORE the counter. So `found` now counts every url a rung
returns and `novel` counts the ones not already tried. The right conclusion — Unpaywall is redundant
against OpenAlex's own `locations` for this chapter — is a different claim from the one the old
counter made, and only the four-counter version can state it.

**RECORDS ARE FETCHED IN A POOL OF 8, WHICH IS A WALL-CLOCK DECISION AND NOT A CHANGE OF METHOD.**
Every record still walks the same rungs in the same order and stops at the same point. Serially this
queue ran at about two records a minute, because the tiers that matter most are the ones publishers
defend hardest and every defended route costs a full timeout; 436 records would have taken most of a
day. Counters are merged under a lock and the destination path is keyed by OpenAlex id, so no two
workers can write the same file.

**PMC IS BEING MEASURED FOR THE FOURTH TIME.** A.12, A.24 and C.3.g each returned ~zero fetches.
22 records here carry a `PubMed` venue, which is the best case this chapter offers it. If it returns
zero again the rung should be retired from the shared scaffold instead of carried by habit; `234`
picks up whatever it FINDS but cannot fetch, since the PMC failure is delivery, not coverage.

Output: literature/search-logs/{slug}-fetch-log.csv
        literature/search-logs/{slug}-fetch-summary.md
        literature/pdfs/{slug}/{WID}__{title-slug}.pdf   (gitignored)
        literature/pdfs/{slug}/{WID}__{title-slug}.html.txt
"""
import csv, json, os, re, subprocess, sys, threading, time
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor

SLUG = "co-residence-parents-household-delay"
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
PROV = os.path.join(EXTRACT, f"{SLUG}-fetch-provenance.json")

HTML_MIN_WORDS = 2500
SECTION_WORDS = ["introduction", "background", "data", "method", "results", "discussion",
                 "conclusion", "references", "literature review", "estimation"]
MIN_SECTIONS = 3
WORKERS = 8

TIER_ORDER = ["T1_wall1_packet", "T1_primary_identified", "T2_primary_relevant",
              "T3_primary_uncertain", "T3_link1_identified",
              "T4_insufficient_resolve_at_retrieval", "T5_link1", "T6_theory_stream"]


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


def get(url, timeout=30):
    try:
        r = subprocess.run(["curl", "-sL", "-m", str(timeout), "-A", UA, url],
                           capture_output=True, text=True, errors="replace")
        return r.stdout if r.returncode == 0 else None
    except Exception:
        return None


def html_to_text(html):
    """Strip a page to its readable body text. Deliberately crude: the decision this feeds is a
    word-count floor, and a crude stripper biases that floor DOWNWARD, which is the safe direction."""
    h = re.sub(r"(?is)<(script|style|nav|header|footer|noscript)[^>]*>.*?</\1>", " ", html)
    h = re.sub(r"(?s)<[^>]+>", " ", h)
    h = re.sub(r"&#\d+;|&#x[0-9a-fA-F]+;|&[a-z]+;", " ", h)
    return re.sub(r"\s+", " ", h).strip()


def html_is_fulltext(text):
    """(ok, words, n_sections). An abstract page and a JavaScript shell both return 200."""
    words = len(text.split())
    low = text.lower()
    n_sec = sum(1 for s in SECTION_WORDS if s in low)
    return (words >= HTML_MIN_WORDS and n_sec >= MIN_SECTIONS), words, n_sec


def fetch_one(url, pdf_dest, txt_dest):
    """(outcome, note). Outcomes: pdf | html_text | route_blocked | empty_or_tiny | exception.

    A 200 with an HTML body is not thrown away. It is read, measured, and admitted only if it
    clears a floor an abstract page cannot."""
    if not url:
        return "no_url", "no_url"
    tmp = pdf_dest + ".part"
    try:
        r = subprocess.run(["curl", "-sL", "-m", "45", "-A", UA,
                            "-H", "Accept: application/pdf,text/html;q=0.8,*/*;q=0.5",
                            "-o", tmp, "-w", "%{http_code}", url],
                           capture_output=True, text=True)
        code = (r.stdout or "").strip()
    except Exception as e:
        return "exception", f"exception:{str(e)[:40]}"
    if not os.path.exists(tmp) or os.path.getsize(tmp) < 1024:
        if os.path.exists(tmp):
            os.remove(tmp)
        return "empty_or_tiny", f"empty_or_tiny:{code}"
    with open(tmp, "rb") as fh:
        head = fh.read(5)
    if head[:4] == b"%PDF":
        os.replace(tmp, pdf_dest)
        return "pdf", f"pdf:{code}"
    try:
        raw = open(tmp, "rb").read().decode("utf-8", "replace")
    except Exception:
        raw = ""
    os.remove(tmp)
    text = html_to_text(raw)
    ok, words, n_sec = html_is_fulltext(text)
    if ok:
        open(txt_dest, "w").write(text)
        return "html_text", f"html_text:{code}:words={words}:sections={n_sec}"
    return "route_blocked", f"route_blocked:{code}:words={words}:sections={n_sec}"


# ---------- rungs, generated lazily and in order ----------

def rung_deterministic(r):
    """Construction, not search. The DOI's own shape fixes the path; no request is spent finding it."""
    d = (r.get("doi") or "").lower()
    out = []
    m = re.match(r"10\.4054/demres\.(\d{4})\.(\d+)\.(\d+)$", d)
    if m:
        vol, art = m.group(2), m.group(3)
        out.append(f"https://www.demographic-research.org/volumes/vol{vol}/{art}/{vol}-{art}.pdf")
    m = re.match(r"10\.4054/mpidr-wp-(\d{4})-(\d+)$", d)
    if m:
        out.append(f"https://www.demogr.mpg.de/papers/working/wp-{m.group(1)}-{m.group(2)}.pdf")
    m = re.match(r"10\.4054/mpidr-tr-(\d{4})-(\d+)$", d)
    if m:
        out.append(f"https://www.demogr.mpg.de/papers/technicalreports/"
                   f"tr-{m.group(1)}-{m.group(2)}.pdf")
    m = re.match(r"10\.3386/(w\d+)$", d)
    if m:
        out.append(f"https://www.nber.org/system/files/working_papers/{m.group(1)}/{m.group(1)}.pdf")
    if d.startswith("10.31235/"):
        out.append(f"https://osf.io/download/{d.split('/')[-1].replace('osf.io/', '')}/")
    return out


def rung_best_oa(r):
    return [r.get("best_url")] if r.get("best_url") else []


def rung_other_locations(r):
    d = get(f"https://api.openalex.org/works/{r['id']}?select=locations&api_key={KEY}")
    try:
        j = json.loads(d) if d else {}
    except Exception:
        return []
    out = []
    for l in (j.get("locations") or []):
        if l.get("is_oa"):
            u = l.get("pdf_url") or l.get("landing_page_url")
            if u and u != r.get("best_url"):
                out.append(u)
    return out


def rung_citation_meta(r):
    landing = r.get("best_url")
    if not landing:
        return []
    html = get(landing, timeout=25)
    if not html:
        return []
    m = re.search(r'<meta[^>]+name=["\']citation_pdf_url["\'][^>]+content=["\']([^"\']+)', html, re.I)
    return [m.group(1)] if m else []


def rung_pmc(r):
    doi = r.get("doi")
    if not doi:
        return []
    j = get("https://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/?ids=" + doi +
            f"&format=json&tool=fertility-review&email={MAILTO}", timeout=30)
    try:
        recs = json.loads(j).get("records") or [] if j else []
    except Exception:
        return []
    return [f"https://www.ncbi.nlm.nih.gov/pmc/articles/{x['pmcid']}/pdf/"
            for x in recs if x.get("pmcid")]


def rung_unpaywall(r):
    doi = r.get("doi")
    if not doi:
        return []
    j = get(f"https://api.unpaywall.org/v2/{doi}?email={MAILTO}", timeout=30)
    try:
        d = json.loads(j) if j else {}
    except Exception:
        return []
    loc = d.get("best_oa_location") or {}
    u = loc.get("url_for_pdf") or loc.get("url")
    return [u] if u else []


RUNGS = [("0_deterministic", rung_deterministic), ("1_best_oa", rung_best_oa),
         ("2_other_locations", rung_other_locations), ("3_citation_meta", rung_citation_meta),
         ("4_pmc", rung_pmc), ("5_unpaywall", rung_unpaywall)]


def main():
    if not KEY:
        sys.stderr.write("ABORT: no OPENALEX_API_KEY.\n")
        sys.exit(3)
    rows = json.load(open(OA))
    os.makedirs(PDF_DIR, exist_ok=True)
    prov = json.load(open(PROV)) if os.path.exists(PROV) else {}
    reached, found, novel, fetched = Counter(), Counter(), Counter(), Counter()
    lock = threading.Lock()
    done = [0]

    def work(r):
        """One record, all rungs in order, stopping at the first recovery.

        Records are independent, so the pool below is a wall-clock decision and not a change of
        method: every record still walks the same rungs in the same order and its counters are
        merged under a lock. The serial version ran at ~2 records a minute because the tiers that
        matter most are the ones publishers defend hardest, and each defended route costs a full
        timeout."""
        base = f"{r['id']}__{slugify(r['title'] or 'untitled')}"
        pdf_dest = os.path.join(PDF_DIR, base + ".pdf")
        txt_dest = os.path.join(PDF_DIR, base + ".html.txt")
        row = dict(id=r["id"], tier=r["tier"], design=r["design"], route=r["route"],
                   doi=r.get("doi") or "", title=(r["title"] or "")[:70])
        for dest, kind in ((pdf_dest, "pdf"), (txt_dest, "html_text")):
            if os.path.exists(dest) and os.path.getsize(dest) > 1024:
                with lock:
                    fetched["cached"] += 1
                    done[0] += 1
                    prior = prov.get(r["id"]) or {}
                row.update(rung=prior.get("rung", "unknown_prior_run"), outcome=kind,
                           note="cached: " + prior.get("note", "no provenance recorded"),
                           url=prior.get("url", ""))
                return row

        outcome, used_rung, used_url, note = "no_url", "", "", "no_candidate_url"
        seen = set()
        for rung_name, rung_fn in RUNGS:
            with lock:
                reached[rung_name] += 1
            try:
                urls = rung_fn(r)
            except Exception:
                urls = []
            urls = [u for u in urls if u]
            fresh = [u for u in urls if u not in seen]
            with lock:
                found[rung_name] += len(urls)
                novel[rung_name] += len(fresh)
            if not fresh:
                continue
            urls = fresh
            for u in urls:
                seen.add(u)
                oc, n = fetch_one(u, pdf_dest, txt_dest)
                if oc in ("pdf", "html_text"):
                    outcome, used_rung, used_url, note = oc, rung_name, u, n
                    with lock:
                        fetched[rung_name] += 1
                        prov[r["id"]] = dict(rung=rung_name, url=u, outcome=oc, note=n)
                    break
                outcome, note = oc, n
            if used_rung:
                break
        row.update(rung=used_rung or "none", outcome=outcome, note=note, url=used_url)
        with lock:
            done[0] += 1
            if done[0] % 20 == 0:
                print(f"  {done[0]}/{len(rows)}", flush=True)
        return row

    with ThreadPoolExecutor(max_workers=WORKERS) as ex:
        log = list(ex.map(work, rows))
    json.dump(prov, open(PROV, "w"), indent=2, sort_keys=True)

    with open(OUT_LOG, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["id", "tier", "design", "route", "title", "doi",
                                           "rung", "outcome", "note", "url"])
        w.writeheader()
        for row in log:
            w.writerow(row)

    pc = lambda n, d: f"{n / d:.0%}" if d else "n/a"
    got = lambda xs: sum(1 for x in xs if x["outcome"] in ("pdf", "html_text"))
    n_pdf = sum(1 for x in log if x["outcome"] == "pdf")
    n_html = sum(1 for x in log if x["outcome"] == "html_text")
    by_tier = defaultdict(list)
    by_design = defaultdict(list)
    for x in log:
        by_tier[x["tier"]].append(x)
        by_design[x["design"]].append(x)
    fails = [x for x in log if x["outcome"] not in ("pdf", "html_text")]
    fail_kind = Counter(x["outcome"] for x in fails)
    oa_flag = {r["id"]: r["is_oa"] for r in rows}
    no_doi = {r["id"] for r in rows if not r.get("doi")}
    oa_but_failed = [x for x in fails if oa_flag.get(x["id"])]
    blocked = [x for x in fails if x["outcome"] == "route_blocked"]

    L = [f"# Stage 5b full-text fetch — {SLUG} (A.23)", "",
         "**Generated by:** `source/build/goldset/233_a23_fetch_fulltext.py`", "",
         f"**{n_pdf + n_html} of {len(rows)} recovered ({pc(n_pdf + n_html, len(rows))})** — "
         f"**{n_pdf} as PDF and {n_html} as HTML full text.** The two are reported apart and never "
         "added into a single retrieval claim without saying so: an `html_text` file cleared a word "
         "and section floor, which is evidence that the body was the article and not proof of it. "
         "Every one carries its word count in the log and they are the first thing the stage-6 "
         "spot-check should look at.", "",
         "## Recovery by tier — the queue's own priority order", "",
         "| Tier | Wanted | PDF | HTML text | Recovered |", "|---|---|---|---|---|"]
    for t in TIER_ORDER:
        g = by_tier.get(t, [])
        if not g:
            continue
        p_ = sum(1 for x in g if x["outcome"] == "pdf")
        h_ = sum(1 for x in g if x["outcome"] == "html_text")
        L.append(f"| `{t}` | {len(g)} | {p_} | {h_} | {pc(p_ + h_, len(g))} |")
    L += ["", "## Recovery by design — the cross-tab that decides whether this was enough", "",
          "A.17's finding, restated: a retrieval RATE hides WHICH records were missed. 23 of 114 was "
          "survivable there; 0 of 4 identified direct-arm records was not.", "",
          "| Design | Wanted | Recovered | |", "|---|---|---|---|"]
    for d in ["identified", "observational", "descriptive", "cannot_tell", "theory"]:
        g = by_design.get(d, [])
        if not g:
            continue
        L.append(f"| `{d}` | {len(g)} | {got(g)} | {pc(got(g), len(g))} |")
    L += ["", "## Rung yield — reached, found, novel, fetched", "",
          "Four counters, and the fourth was added because the first run of this script produced a "
          "false negative with it missing. Rungs are tried in order and stop at the first success, "
          "so `reached` says how many records got as far as asking. `found` counts every url the "
          "rung returned; `novel` counts the ones no earlier rung had already tried. **A rung can be "
          "REDUNDANT rather than EMPTY, and counting after de-duplication makes the two identical.** "
          "Unpaywall recorded `found 0 / reached 352` here — read as a rung with nothing to offer "
          "this literature. It was not: hand-testing it returned a url for most records with a DOI, "
          "and almost every one was the url `1_best_oa` had already failed on. The rung is "
          "redundant against OpenAlex's own locations for this chapter, which is a finding; it is "
          "not the finding the old counter reported.", "",
          "| Rung | Records reached | URLs found | Novel urls | Recovered | Hit rate on novel |",
          "|---|---|---|---|---|---|"]
    for rung, _ in RUNGS:
        L.append(f"| `{rung}` | {reached.get(rung, 0)} | {found.get(rung, 0)} | "
                 f"{novel.get(rung, 0)} | {fetched.get(rung, 0)} | "
                 f"{pc(fetched.get(rung, 0), novel.get(rung, 0))} |")
    if fetched.get("cached"):
        L.append(f"| `cached` | — | — | — | {fetched['cached']} | n/a |")
    cum = Counter(v.get("rung", "unknown_prior_run") for v in prov.values())
    L += ["", "### Cumulative rung attribution", "",
          "The counters above describe THIS RUN, and a run that finds its files already on disk "
          "does no rung work at all — the whole table collapses into `cached` and the attribution "
          "is lost. So the rung that actually delivered each file is written to "
          f"`extraction/{SLUG}-fetch-provenance.json` when it is fetched, and the cumulative "
          "picture is read back from there. This is the table to quote.", "",
          "| Rung | Files delivered |", "|---|---|"]
    for k, n in cum.most_common():
        L.append(f"| `{k}` | {n} |")
    L += ["", "## Failures, by kind", "", "| Kind | n | Reading |", "|---|---|---|"]
    READ = {"route_blocked": "a 200 whose body was neither a PDF nor long enough to be the "
                             "article — **open content behind bot defence, or an abstract page**; "
                             "a browser-job, not a proxy-job",
            "no_url": "no open location on any rung — a genuinely closed paper, or a record with "
                      "no DOI and no repository copy",
            "empty_or_tiny": "a truncated or empty response; usually a redirect to a splash page",
            "exception": "transport failure — UNCONFIRMED, not closed"}
    for k, n in fail_kind.most_common():
        L.append(f"| `{k}` | {n} | {READ.get(k, '')} |")
    L += ["", f"**{len(oa_but_failed)} records OpenAlex calls OPEN ACCESS were not recovered**, and "
          f"{len(blocked)} of all failures were blocked routes rather than absent ones. That is the "
          "population the browser handoff exists for, and it is a different worklist from the "
          f"**{sum(1 for x in fails if x['id'] in no_doi)} failures with no DOI**, which no proxy "
          "and no rung can resolve and which need a librarian.", "",
          "## What this stage does not claim", "",
          "- **A recovered file is not a read study.** Stage 6 is the full-text screen; this is "
          "delivery only.",
          "- **The `html_text` floor is a rule that can be wrong in both directions.** It can admit "
          "a long review page and it can refuse a short article. Word counts are logged for every "
          "record precisely so the rule is auditable rather than trusted — the standing finding that "
          "a safeguard must be measured, not assumed to have fired.", ""]
    open(OUT_MD, "w").write("\n".join(L) + "\n")
    print(f"\nrecovered {n_pdf + n_html}/{len(rows)} ({pc(n_pdf + n_html, len(rows))}) — "
          f"{n_pdf} pdf, {n_html} html")
    print("reached:", dict(reached))
    print("found  :", dict(found))
    print("novel  :", dict(novel))
    print("fetched:", dict(fetched))
    print("fails  :", dict(fail_kind))
    print(f"-> {os.path.relpath(OUT_MD, ROOT)}")


if __name__ == "__main__":
    main()
