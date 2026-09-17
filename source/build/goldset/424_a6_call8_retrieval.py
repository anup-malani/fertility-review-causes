#!/usr/bin/env python3
"""
424 — A.6 (TICK-087): retrieve the seven call-8 candidates and classify their outcome measure.

The question call 8 asks. ARM C produced seven studies pairing a normative exposure with a birth
outcome — the first such records in the chapter. The PI's test is whether their outcome can be
**converted into realized-fertility terms**; if not, the answer to call 8 is no.

That test has a precise answer and it turns on which measure a paper uses:

  illegitimacy RATIO   nonmarital births / all births. A **composition**. Not convertible to a
                       fertility level without the total-birth denominator and the female
                       population; it can move with no change in fertility at all.
  illegitimacy RATE    nonmarital births per 1,000 unmarried women. A genuine **fertility rate for
                       a subpopulation**, and convertible: it enters the general fertility rate
                       additively, weighted by the unmarried share. This is Coale's distinction
                       between I_h and the composition indices.
  a fertility LEVEL    TFR, GFR, completed fertility, children ever born, births per woman.
                       Admissible directly under ruling 2, no conversion needed.

So the same seven records could answer call 8 either way, and only the full texts say which. This
script retrieves them and scores the measure vocabulary; the classification itself is then made by
reading, not by the score.

Version copies as an asset, for once. These seven studies appear as **13** OpenAlex records —
*From Shame to Game* alone has six, under four title variants and three years. ARM C's screen
recorded that as a counting defect that inflates frame sizes, and it does. Here it is also extra
retrieval surface: if the canonical version is closed, a working paper or repository copy of the
same study may not be, so every version is tried before a study is declared unavailable. Retrieval
routes are imported from `412` rather than copied, for the reason TICK-074 exists.
"""
import csv, importlib.util, json, pathlib, re, subprocess, sys

HERE = pathlib.Path(__file__).resolve().parent
SLUG = "stigma-reduction-contraception-abortion"
PDFDIR = pathlib.Path("literature/pdfs") / SLUG
EXTR = pathlib.Path("extraction")
LOGDIR = pathlib.Path("literature/search-logs")
MAILTO = "shravanh@uchicago.edu"
OA = "https://api.openalex.org/works"

# study -> versions, best first. Every version is tried; the first that yields text wins.
STUDIES = {
    "female-sexual-attitudes-illegitimacy-1981": ["W2314052622"],
    "adolescent-background-fertility-norms-1990": ["W222766436"],
    "social-approval-values-afdc-2001": ["W2160737213", "W2892194071"],
    "from-shame-to-game": ["W3124400004", "W2102216183", "W3125493078", "W1534552387",
                           "W4414567048", "W4321338848"],
    "religion-marry-early-nonmarital-birth-2026": ["W7124168863"],
    "swedish-illegitimacy-rates-1983": ["W1968910820"],
    "illegitimate-births-bridal-pregnancy-2008": ["W4251999233"],
}

MEASURE = {
    "ratio_composition": [r"illegitimacy ratio", r"ratio of illegitimate", r"share of births",
                          r"proportion of (?:all )?births", r"percent(?:age)? of births",
                          r"nonmarital birth ratio", r"non-marital birth ratio",
                          r"fraction of births"],
    "rate_subpopulation": [r"illegitimacy rate", r"illegitimate birth rate",
                           r"nonmarital (?:birth|fertility) rate", r"per 1[,.]?000 unmarried",
                           r"per thousand unmarried", r"births per unmarried",
                           r"unmarried women aged"],
    "fertility_level": [r"total fertility rate", r"\btfr\b", r"general fertility rate",
                        r"completed fertility", r"children ever born", r"births per woman",
                        r"crude birth rate", r"age-specific fertility"],
}
COMPILED = {k: [re.compile(p, re.I) for p in v] for k, v in MEASURE.items()}


def load_412():
    spec = importlib.util.spec_from_file_location("r412", HERE / "412_a6_fulltext_retrieval.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def candidates_for(w, r412):
    oa = w.get("open_access") or {}
    bol = w.get("best_oa_location") or {}
    out = []
    if bol.get("pdf_url"):
        out.append(("best_oa_location", bol["pdf_url"]))
    if oa.get("oa_url") and oa["oa_url"] not in [c[1] for c in out]:
        out.append(("oa_url", oa["oa_url"]))
    for loc in (w.get("locations") or []):
        if loc.get("pdf_url") and loc["pdf_url"] not in [c[1] for c in out]:
            out.append(("location", loc["pdf_url"]))
    for loc in (w.get("locations") or []):
        lp = loc.get("landing_page_url") or ""
        if r412.looks_like_pdf(lp) and lp not in [c[1] for c in out]:
            out.append(("landing_page_pdf", lp))
        if "hdl.handle.net" in lp:
            for c in r412.dspace_bitstreams(lp):
                if c not in [x[1] for x in out]:
                    out.append(("dspace_rest", c))
    for loc in (w.get("locations") or []):
        m = re.search(r"(PMC\d+)", (loc.get("landing_page_url") or "")
                      + " " + (loc.get("pdf_url") or ""))
        if m:
            u = f"https://www.ebi.ac.uk/europepmc/webservices/rest/{m.group(1)}/fullTextXML"
            if u not in [c[1] for c in out]:
                out.append(("europepmc_xml", u))
    return out


def main():
    r412 = load_412()
    all_ids = [i for v in STUDIES.values() for i in v]
    url = (f"{OA}?filter=openalex:{'|'.join(all_ids)}&per_page=50"
           f"&select=id,doi,display_name,publication_year,type,open_access,best_oa_location,"
           f"locations&mailto={MAILTO}")
    if r412.API_KEY:
        url += f"&api_key={r412.API_KEY}"
    d, err = r412.get_json(url)
    if not d or "results" not in d:
        print(f"metadata fetch failed: {err}", file=sys.stderr)
        return 2
    meta = {w["id"].rsplit("/", 1)[-1]: w for w in d["results"]}
    PDFDIR.mkdir(parents=True, exist_ok=True)

    rows = []
    for study, versions in STUDIES.items():
        got = None
        tried = []
        for wid in versions:
            w = meta.get(wid)
            if not w:
                tried.append((wid, "not in OpenAlex response"))
                continue
            base = f"{wid}__{r412.slugify(w.get('display_name') or study)}"
            pdf, txt = PDFDIR / f"{base}.pdf", PDFDIR / f"{base}.txt"
            if txt.exists() and len(txt.read_text(errors="ignore").split()) >= 500:
                got = (wid, "cached", txt)
                break
            for src, u in candidates_for(w, r412):
                if src == "europepmc_xml":
                    ok, detail = r412.fetch_xml_text(u, txt)
                    if ok:
                        got = (wid, src, txt)
                        break
                    continue
                ok, _ = r412.download(u, pdf)
                if not ok:
                    continue
                tok, _ = r412.extract(pdf, txt)
                if tok:
                    got = (wid, src, txt)
                    break
                pdf.unlink(missing_ok=True)
                txt.unlink(missing_ok=True)
            if got:
                break
            tried.append((wid, f"{len((w.get('locations') or []))} location(s), none yielded text"))

        row = {"study": study, "versions": len(versions), "status": "", "id": "", "source": "",
               "words": "", "ratio_composition": "", "rate_subpopulation": "",
               "fertility_level": "", "tried": "; ".join(f"{a}: {b}" for a, b in tried)[:200]}
        if got:
            wid, src, txt = got
            body = txt.read_text(errors="ignore")
            counts = {k: sum(len(p.findall(body)) for p in ps) for k, ps in COMPILED.items()}
            row.update(status="retrieved", id=wid, source=src, words=str(len(body.split())),
                       **{k: str(v) for k, v in counts.items()})
            print(f"  OK       {study[:42]:<42} {wid}  via {src}  "
                  f"ratio={counts['ratio_composition']} rate={counts['rate_subpopulation']} "
                  f"level={counts['fertility_level']}", flush=True)
        else:
            row["status"] = "unavailable"
            print(f"  MISSING  {study[:42]:<42} all {len(versions)} version(s) failed", flush=True)
        rows.append(row)

    logp = EXTR / f"{SLUG}-call8-retrieval-log.csv"
    with logp.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    got_n = sum(1 for r in rows if r["status"] == "retrieved")
    print(f"\nretrieved {got_n}/{len(rows)} studies; wrote {logp.name}")
    print("measure-vocabulary counts are a ROUTING aid; the ratio-vs-rate call is made by reading.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
