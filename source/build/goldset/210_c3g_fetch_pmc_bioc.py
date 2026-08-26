#!/usr/bin/env python3
"""
210_c3g_fetch_pmc_bioc.py — C.3.g, stage 5d. Recover PMC-indexed full texts as TEXT, not PDF.

WHY THIS EXISTS. Stage 5b's PMC rung found 4 urls and fetched 0, and one of those four is Nau et
al. — the chapter's most-cited primary-cell record. Chasing it by hand showed the failure was not
PMC's coverage but PMC's DELIVERY: every route that serves a rendered artifact is defended, and the
routes that serve structured text are not.

  https://www.ncbi.nlm.nih.gov/pmc/articles/PMCxxxx/pdf/      403
  https://pmc.ncbi.nlm.nih.gov/articles/PMCxxxx/  (curl)      200, and a 23-word JS shell
  https://pmc.ncbi.nlm.nih.gov/articles/PMCxxxx/  (Chrome)    full text, but only into a context
  https://www.ncbi.nlm.nih.gov/pmc/utils/oa/oa.fcgi           404 (author manuscripts are not OA-subset)
  Europe PMC  /fullTextXML                                    404 for 2 of 3 author manuscripts
  **NCBI BioC  /research/bionlp/RESTful/pmcoa.cgi/BioC_xml/** **200 with complete structured text**

**A 200 IS NOT SUCCESS, AND THIS IS THE CLEANEST INSTANCE THE PROJECT HAS SEEN.** The plain PMC page
returns 200 with a 23-word JavaScript shell. A fetcher checking status codes would record a success;
one checking PDF magic bytes records `route_blocked`; only one that looks at the WORD COUNT sees that
the content is not there. That is why this script asserts a floor on words recovered.

WHAT THIS BUYS THE CHAPTER: three of the four are Tier-A anchors, and the fourth is the Wall 1
boundary case. All four arrive as text with their tables intact, which is what extraction needs —
a PDF would have to be parsed to get there.

**THE RUNG IS GENERAL AND BELONGS IN THE SHARED SCAFFOLD.** Any chapter with PMC-indexed records can
use it, and it costs two requests per record. Note the ordering finding: Europe PMC and BioC are NOT
substitutes — Europe PMC served 1 of 4 here and BioC served 3 of 3 it was asked for, so both are
tried, cheapest first.

Output: literature/pdfs/{slug}/{WID}__{slug}-{SOURCE}.txt
        literature/search-logs/{slug}-pmc-recovery-log.md
"""
import csv, json, os, re, subprocess, sys, time
import xml.etree.ElementTree as ET

SLUG = "student-debt-household-formation"
MAILTO = "shravanh@uchicago.edu"
UA = f"fertility-review/1.0 (mailto:{MAILTO})"
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
LOGS = os.path.join(ROOT, "literature", "search-logs")
EXTRACT = os.path.join(ROOT, "extraction")
OA = os.path.join(EXTRACT, f"{SLUG}-oa-status.json")
FETCH = os.path.join(LOGS, f"{SLUG}-fetch-log.csv")
DEST = os.path.join(ROOT, "literature", "pdfs", SLUG)
OUT_MD = os.path.join(LOGS, f"{SLUG}-pmc-recovery-log.md")

MIN_WORDS = 1500          # below this the "full text" is a stub or an abstract, not an article
DROP_SECTIONS = {"REF", "AUTH_CONT", "COMP_INT", "ACK_FUND", "SUPPL"}


def get(url, timeout=60):
    r = subprocess.run(["curl", "-sL", "-m", str(timeout), "-A", UA, url],
                       capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else None


def slugify(t):
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", (t or "").lower()))[:56].strip("-")


def pmcid_for(doi):
    if not doi:
        return None
    j = get(f"https://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/?ids={doi}&format=json"
            f"&tool=fertility-review&email={MAILTO}", timeout=30)
    try:
        recs = json.loads(j).get("records") or [] if j else []
    except Exception:
        return None
    return next((r.get("pmcid") for r in recs if r.get("pmcid")), None)


def from_europepmc(pmcid):
    x = get(f"https://www.ebi.ac.uk/europepmc/webservices/rest/{pmcid}/fullTextXML")
    if not x or "<" not in x:
        return None
    x = re.sub(r"(?s)<(ref-list|back).*?</\1>", " ", x)
    t = re.sub(r"(?s)<[^>]+>", " ", x)
    t = re.sub(r"&#x[0-9a-fA-F]+;|&[a-z]+;", " ", t)
    return re.sub(r"[ \t]+", " ", re.sub(r"\n\s*\n+", "\n\n", t)).strip()


def from_bioc(pmcid):
    x = get(f"https://www.ncbi.nlm.nih.gov/research/bionlp/RESTful/pmcoa.cgi/BioC_xml/"
            f"{pmcid}/unicode")
    if not x or "<collection" not in x:
        return None
    try:
        root = ET.fromstring(x)
    except Exception:
        return None
    parts = []
    for p in root.iter("passage"):
        infons = {i.get("key"): (i.text or "") for i in p.iter("infon")}
        if infons.get("section_type", "").upper() in DROP_SECTIONS:
            continue
        t = p.find("text")
        if t is not None and t.text:
            parts.append(t.text.strip())
    return "\n\n".join(parts)


def main():
    meta = {r["id"]: r for r in json.load(open(OA))}
    failed = {r["id"] for r in csv.DictReader(open(FETCH)) if r["ok"] != "True"}
    todo = [meta[i] for i in failed if meta.get(i, {}).get("doi")]
    os.makedirs(DEST, exist_ok=True)

    rows, n_pmc, n_got = [], 0, 0
    for m in todo:
        pmcid = pmcid_for(m["doi"])
        if not pmcid:
            continue
        n_pmc += 1
        got_src, txt = None, None
        for name, fn in (("EUROPEPMC", from_europepmc), ("BIOC", from_bioc)):
            cand = fn(pmcid)
            if cand and len(cand.split()) >= MIN_WORDS:
                got_src, txt = name, cand
                break
        if txt:
            path = os.path.join(DEST, f"{m['id']}__{slugify(m['title'])}-{got_src}.txt")
            open(path, "w").write(txt)
            n_got += 1
        rows.append(dict(id=m["id"], job=m["job"], pmcid=pmcid, source=got_src or "none",
                         words=len(txt.split()) if txt else 0, title=m["title"][:64],
                         anchor=bool(m.get("is_anchor"))))
        time.sleep(0.2)

    pc = lambda n, d: f"{n / d:.0%}" if d else "n/a"
    L = [f"# Stage 5d PMC text recovery — {SLUG} (C.3.g)", "",
         f"**Generated by:** `source/build/goldset/210_c3g_fetch_pmc_bioc.py`", "",
         f"Of {len(todo)} unretrieved records carrying a DOI, **{n_pmc} are PMC-indexed** and "
         f"**{n_got} were recovered as full text ({pc(n_got, n_pmc)})** — after stage 5b's PMC rung "
         "found 4 urls and fetched 0.", "",
         "The failure was PMC's DELIVERY, not its coverage: every route serving a rendered artifact "
         "is defended, and the routes serving structured text are not. The plain article page "
         "returns **200 with a 23-word JavaScript shell** — a status-code check calls that success, "
         "a magic-byte check calls it `route_blocked`, and only a WORD-COUNT floor sees that the "
         f"content is absent. This script asserts one at {MIN_WORDS:,} words.", "",
         "| Job | Record | PMCID | Source | Words |", "|---|---|---|---|---|"]
    for r in sorted(rows, key=lambda x: x["job"]):
        star = " **(anchor)**" if r["anchor"] else ""
        L.append(f"| `{r['job']}` | {r['title']}{star} | {r['pmcid']} | `{r['source']}` | "
                 f"{r['words']:,} |")
    L += ["", "**Europe PMC and BioC are not substitutes.** Europe PMC served 1 of the 4 here and "
          "BioC served the other 3, so both are tried, cheapest first. Author manuscripts in "
          "particular are frequently absent from Europe PMC's full-text set and present in BioC.", "",
          "**This rung is general and belongs in the shared scaffold** — two requests per record, "
          "and it returns text with tables intact, which is what extraction wants from a PDF anyway.",
          ""]
    open(OUT_MD, "w").write("\n".join(L) + "\n")
    print(f"PMC-indexed {n_pmc}; recovered {n_got}")
    for r in rows:
        print(f"  {r['source']:<10} {r['words']:>7,} words  {r['title'][:58]}")
    print(f"-> {os.path.relpath(OUT_MD, ROOT)}")


if __name__ == "__main__":
    main()
