#!/usr/bin/env python3
"""
141_b6_fetch_pmc_efetch.py — B.6, stage 5 recovery. Add the NCBI efetch rung to the route ladder.

`140` fetched 92 of 239 records readable against an OA ceiling of ~77%. Ninety-six records that
OpenAlex calls OPEN failed to fetch, and the failure notes split into two dominant shapes:

    40  "epmc hit but not OA"                     -> Europe PMC has the record, refuses the text
    38  "not a PDF (publisher interstitial)"      -> publisher blocks the scripted download

This script targets the first. The diagnosis is that those records are AUTHOR-MANUSCRIPT DEPOSITS in
PubMed Central: `isOpenAccess: N` but `inEPMC: Y` and `hasPDF: Y`. They are not open-access by
licence, so Europe PMC's `fullTextXML` endpoint returns 404 — but the manuscript is in PMC and NCBI's
`efetch` serves the full JATS XML for it. Verified live on two failures before this script was
written: `PMC5131715` and `PMC10234267` both 404 at Europe PMC and both return >110 KB of XML with a
populated `<body>` (33k characters of text) from efetch.

The distinction the inherited ladder missed is between OPEN ACCESS (a licence fact) and RETRIEVABLE
(an access fact). `140` treated Europe PMC's `isOpenAccess` flag as the gate on whether to try for
text at all, which conflates them. A record can be all-rights-reserved at the publisher and still
have a readable author manuscript in PMC, and for NIH-funded work that is the common case — which is
why this recovers disproportionately from the US-funded PFAS cohorts, the half of the chapter the
`139` selection test flagged as under-reached.

Discipline carried from 140: a failure is logged as FAILED with its reason, never as "closed"; text
extracted from XML is marked as such so a reader knows it is not a page-faithful PDF; and a record
already readable is skipped rather than refetched.

Output: literature/pdfs/{slug}/*.txt   (gitignored)
        extraction/{slug}-pdf-retrieval-log-2.csv   (the recovery pass, kept separate from 140's)
"""
import csv, json, os, re, subprocess, time

SLUG = "microplastics-pfas-reproductive"
MAILTO = "shravanh@uchicago.edu"
UA = f"fertility-review/1.0 (mailto:{MAILTO})"
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
EXTRACT = os.path.join(ROOT, "extraction")
PDF_DIR = os.path.join(ROOT, "literature", "pdfs", SLUG)
IN_LOG = os.path.join(EXTRACT, f"{SLUG}-pdf-retrieval-log.csv")
OUT_LOG = os.path.join(EXTRACT, f"{SLUG}-pdf-retrieval-log-2.csv")

MIN_BODY = 3000     # a <body> shorter than this is a stub, not a paper


def slugify(t):
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", (t or "").lower()))[:60].strip("-")


def epmc_ids(doi):
    """Return (pmcid, pmid, in_epmc). Deliberately does NOT filter on isOpenAccess — that flag is a
    licence statement and this script's whole point is that it does not decide retrievability."""
    q = ('https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=DOI:%22'
         + doi + '%22&resultType=core&format=json&pageSize=1')
    try:
        d = json.loads(subprocess.run(["curl", "-s", "-m", "40", "-A", UA, q],
                                      capture_output=True, text=True).stdout)
        hits = ((d.get("resultList") or {}).get("result") or [])
    except Exception:
        return None, None, None
    if not hits:
        return None, None, None
    h = hits[0]
    return h.get("pmcid"), h.get("pmid"), h.get("inEPMC")


def efetch_body(pmcid):
    """NCBI efetch for a PMC id. Returns (text, note)."""
    num = pmcid.replace("PMC", "")
    url = ("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pmc&id=" + num
           + "&rettype=xml&email=" + MAILTO)
    try:
        xml = subprocess.run(["curl", "-s", "-m", "60", "-A", UA, url],
                             capture_output=True, text=True).stdout
    except Exception as e:
        return None, f"efetch transport: {str(e)[:60]}"
    if len(xml) < 2000 or "<body" not in xml:
        return None, f"efetch returned no body ({len(xml)} B)"
    m = re.search(r"<body.*?</body>", xml, re.S)
    if not m:
        return None, "no <body> element"
    text = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", m.group(0))).strip()
    if len(text) < MIN_BODY:
        return None, f"body too short ({len(text)} chars) — abstract-only deposit"
    return text, f"efetch {pmcid}, {len(text) // 1024} KB text"


def main():
    rows = list(csv.DictReader(open(IN_LOG)))
    os.makedirs(PDF_DIR, exist_ok=True)

    todo = [r for r in rows if "FAILED" in r["result"]]
    out, recovered = [], 0
    for r in todo:
        wid, doi = r["openalex_id"], r["doi"]
        txt = os.path.join(PDF_DIR, f"{wid}__{slugify(r['title'])}.txt")
        if os.path.exists(txt) and os.path.getsize(txt) > 500:
            continue
        if not doi:
            out.append([wid, doi, r["job"], r["chemical_family"], r["oa_status"], "FAILED",
                        "no doi", r["title"]])
            continue
        pmcid, pmid, in_epmc = epmc_ids(doi)
        time.sleep(0.35)
        if not pmcid:
            out.append([wid, doi, r["job"], r["chemical_family"], r["oa_status"], "FAILED",
                        f"no PMC id (inEPMC={in_epmc}, pmid={pmid or 'none'})", r["title"]])
            continue
        text, note = efetch_body(pmcid)
        time.sleep(0.35)
        if text:
            open(txt, "w").write(text)
            recovered += 1
            out.append([wid, doi, r["job"], r["chemical_family"], r["oa_status"], "OK_XML", note,
                        r["title"]])
        else:
            out.append([wid, doi, r["job"], r["chemical_family"], r["oa_status"], "FAILED", note,
                        r["title"]])

    with open(OUT_LOG, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["openalex_id", "doi", "job", "chemical_family", "oa_status", "result", "note",
                    "title"])
        w.writerows(out)

    # Combined position after both passes.
    readable = set()
    for f in os.listdir(PDF_DIR):
        if f.endswith(".txt") and os.path.getsize(os.path.join(PDF_DIR, f)) > 500:
            readable.add(f.split("__")[0])
    by_job, by_fam = {}, {}
    for r in rows:
        j = by_job.setdefault(r["job"], [0, 0])
        j[1] += 1
        if r["openalex_id"] in readable:
            j[0] += 1
        if r["job"] in ("A_primary", "A2_input"):
            f = by_fam.setdefault(r["chemical_family"] or "(unstated)", [0, 0])
            f[1] += 1
            if r["openalex_id"] in readable:
                f[0] += 1

    print(f"attempted={len(todo)} recovered_via_efetch={recovered} still_failed={len(out) - recovered}")
    print(f"TOTAL readable now: {len(readable)}/{len(rows)}")
    for j in ("A_primary", "A2_input", "B_held", "C_parameter"):
        if j in by_job:
            g, n = by_job[j]
            print(f"  {j:<12} {g}/{n} ({g / n:.0%})")
    print("  by family (A + A2):")
    for f, (g, n) in sorted(by_fam.items()):
        print(f"    {f:<10} {g}/{n} ({g / n:.0%})")
    print(f"-> {os.path.relpath(OUT_LOG, ROOT)}")


if __name__ == "__main__":
    main()
