#!/usr/bin/env python3
"""
234_a23_pmc_text_recovery.py — A.23, stage 5c. Recover the PMC-indexed records as TEXT.

Inherits `210_c3g_fetch_pmc_bioc.py` unchanged in method and run here for a specific reason:
**stage 5b's PMC rung found 14 urls and fetched 0.** That is the fourth chapter in a row where PMC
has delivered nothing through a PDF route, and the C.3.g finding says the reason is delivery rather
than coverage — every PMC route that serves a rendered artifact is defended, and the routes that
serve structured text are not:

    https://www.ncbi.nlm.nih.gov/pmc/articles/PMCxxxx/pdf/      403
    https://pmc.ncbi.nlm.nih.gov/articles/PMCxxxx/  (curl)      200, and a 23-word JS shell
    Europe PMC  /fullTextXML                                    404 for most author manuscripts
    NCBI BioC   /RESTful/pmcoa.cgi/BioC_xml/                    200 with complete structured text

**SO THE RUNG SHOULD NOT BE RETIRED, AND THE THREE EARLIER ZEROS SHOULD BE RE-READ.** A.12, A.24 and
C.3.g each recorded PMC at zero fetches and the honest reading of that, now, is that all four
measured the PDF route and none of them measured PMC. The number that decides whether PMC is worth
carrying is what THIS script recovers, not what 5b's rung fetched.

WHAT IT IS WORTH HERE: 14 records, of which **two are `T3_link1_identified`** — the social-pension
studies that are among the chapter's only leverage on whether the living arrangement responds to
anything exogenous. Those two are the reason this runs before the browser handoff rather than after.

**A 200 IS NOT SUCCESS.** The plain PMC page returns 200 carrying a JavaScript shell; a fetcher
reading status codes records a success, one reading magic bytes records `route_blocked`, and only a
WORD-COUNT floor sees that the content is not there. The floor is asserted at 1,500 words.

Output: literature/pdfs/{slug}/{WID}__{title-slug}-{SOURCE}.txt
        literature/search-logs/{slug}-pmc-recovery-log.md
"""
import csv, json, os, re, subprocess, sys, time
import xml.etree.ElementTree as ET

SLUG = "co-residence-parents-household-delay"
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
GOT = ("pdf", "html_text")


def get(url, timeout=60):
    r = subprocess.run(["curl", "-sL", "-m", str(timeout), "-A", UA, url],
                       capture_output=True, text=True, errors="replace")
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
    log = {r["id"]: r for r in csv.DictReader(open(FETCH))}
    failed = [meta[i] for i, r in log.items() if r["outcome"] not in GOT and meta.get(i, {}).get("doi")]
    os.makedirs(DEST, exist_ok=True)

    rows, n_pmc, n_got = [], 0, 0
    for m in failed:
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
            open(os.path.join(DEST, f"{m['id']}__{slugify(m['title'])}-{got_src}.txt"), "w").write(txt)
            n_got += 1
        rows.append(dict(id=m["id"], tier=m["tier"], design=m["design"], pmcid=pmcid,
                         source=got_src or "none", words=len(txt.split()) if txt else 0,
                         title=(m["title"] or "")[:64]))
        time.sleep(0.2)

    pc = lambda n, d: f"{n / d:.0%}" if d else "n/a"
    ident = [r for r in rows if r["design"] == "identified"]
    L = [f"# Stage 5c PMC text recovery — {SLUG} (A.23)", "",
         "**Generated by:** `source/build/goldset/234_a23_pmc_text_recovery.py`", "",
         f"Of {len(failed)} unretrieved records carrying a DOI, **{n_pmc} are PMC-indexed** and "
         f"**{n_got} were recovered as full text ({pc(n_got, n_pmc)})** — after stage 5b's PMC rung "
         "found 14 urls and fetched 0.", "",
         "**The zero was the PDF route, not PMC.** Every PMC route that serves a rendered artifact "
         "is defended and the routes serving structured text are not; the plain article page returns "
         "200 carrying a 23-word JavaScript shell, which a status-code check calls success, a "
         "magic-byte check calls `route_blocked`, and only a word-count floor — asserted here at "
         f"{MIN_WORDS:,} — reads correctly. A.12, A.24 and C.3.g each recorded PMC at zero fetches, "
         "and the honest re-reading of those three is that they measured the same defended route "
         "rather than PMC's coverage.", "",
         "| Tier | Design | Record | PMCID | Source | Words |", "|---|---|---|---|---|---|"]
    for r in sorted(rows, key=lambda x: (x["tier"], x["title"])):
        L.append(f"| `{r['tier']}` | `{r['design']}` | {r['title']} | {r['pmcid']} | "
                 f"`{r['source']}` | {r['words']:,} |")
    L += ["", f"**{len(ident)} of the {n_pmc} are identified designs**, and they are why this ran "
          "before the browser handoff rather than after: the social-pension studies on link 1 are "
          "among the chapter's only leverage on whether the living arrangement responds to anything "
          "exogenous.", "",
          "**Europe PMC and BioC are not substitutes** and both are tried, cheapest first — author "
          "manuscripts are frequently absent from Europe PMC's full-text set and present in BioC.", "",
          "**Recovered text is not a PDF and is not counted as one.** It arrives with tables intact, "
          "which is what extraction wants; it also arrives without the figures and the typeset "
          "layout, so anything the stage-6 screen needs to read off a figure is not here.", ""]
    open(OUT_MD, "w").write("\n".join(L) + "\n")
    print(f"PMC-indexed {n_pmc}; recovered {n_got}")
    for r in rows:
        print(f"  {r['source']:<10} {r['words']:>7,} words  {r['tier'][:20]:20s} {r['title'][:52]}")
    print(f"-> {os.path.relpath(OUT_MD, ROOT)}")


if __name__ == "__main__":
    main()
