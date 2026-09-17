#!/usr/bin/env python3
"""
421 — A.6 (TICK-087): retrieve the A.5-bundled records so PI call 4's inspection can happen.

Why. Call 4 ruled A.5 a **bundle, not a wall**: programme studies are admissible pending a
full-text pass that asks whether the norm component was separately dosed. 25 records sit in
`MIXED_NORM_SUPPLY`, and 3 of the 5 identified records across the substantive walls are in A.5, so
this is one of the two live routes to a non-empty primary cell.

Triage first, because it changes what to expect. Against `410`'s flags, **none** of the 25 carries
both a fertility-outcome marker and an identified-design marker: 22 have the fertility marker
alone, 3 have neither. That is not a reason to skip them — S4 was read exhaustively precisely
because a design an abstract does not name is how a primary-cell study hides — but it does mean the
prior is low and the pass is a confirmation exercise rather than a hunt.

Retrieval routes are **imported from `412`, not re-implemented.** TICK-074 exists because a shared
resolver was copied into twelve chapters and the fix had to be applied twelve times; adding a
thirteenth copy of the download-and-verify logic would earn the same ticket. `412` already carries
the routes that matter — landing-page PDFs, the DSpace 7 REST resolver, Europe PMC full-text XML,
a Wayback fallback, and verification that rejects a robot check served with HTTP 200.

19 of the 25 have a fetchable open-access URL. The remaining 6 are `oa_status: closed` and go to
the wantlist rather than being silently dropped.
"""
import csv, importlib.util, json, pathlib, subprocess, sys, urllib.parse

HERE = pathlib.Path(__file__).resolve().parent
SLUG = "stigma-reduction-contraception-abortion"
PDFDIR = pathlib.Path("literature/pdfs") / SLUG
EXTR = pathlib.Path("extraction")
LOGDIR = pathlib.Path("literature/search-logs")
SCREENED = EXTR / f"{SLUG}-screened.csv"
MAILTO = "shravanh@uchicago.edu"
OA = "https://api.openalex.org/works"


def load_412():
    """Import 412's retrieval routes. A module name starting with a digit needs importlib."""
    spec = importlib.util.spec_from_file_location(
        "r412", HERE / "412_a6_fulltext_retrieval.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def main():
    r412 = load_412()
    ids = [r["id"] for r in csv.DictReader(SCREENED.open())
           if r["cell"] == "MIXED_NORM_SUPPLY"]
    if not ids:
        print("no MIXED_NORM_SUPPLY records", file=sys.stderr)
        return 2
    PDFDIR.mkdir(parents=True, exist_ok=True)

    url = (f"{OA}?filter=openalex:{'|'.join(ids)}&per_page=50"
           f"&select=id,doi,display_name,publication_year,type,open_access,best_oa_location,"
           f"locations&mailto={MAILTO}")
    if r412.API_KEY:
        url += f"&api_key={r412.API_KEY}"
    d, err = r412.get_json(url)
    if not d or "results" not in d:
        print(f"metadata fetch failed: {err}", file=sys.stderr)
        return 2
    meta = {w["id"].rsplit("/", 1)[-1]: w for w in d["results"]}

    rows = []
    for wid in ids:
        w = meta.get(wid, {})
        title = w.get("display_name") or ""
        doi = (w.get("doi") or "").replace("https://doi.org/", "")
        oa = w.get("open_access") or {}
        bol = w.get("best_oa_location") or {}
        cands = []
        if bol.get("pdf_url"):
            cands.append(("best_oa_location", bol["pdf_url"]))
        if oa.get("oa_url") and oa["oa_url"] not in [c[1] for c in cands]:
            cands.append(("oa_url", oa["oa_url"]))
        for loc in (w.get("locations") or []):
            if loc.get("pdf_url") and loc["pdf_url"] not in [c[1] for c in cands]:
                cands.append(("location", loc["pdf_url"]))
        for loc in (w.get("locations") or []):
            lp = loc.get("landing_page_url") or ""
            if r412.looks_like_pdf(lp) and lp not in [c[1] for c in cands]:
                cands.append(("landing_page_pdf", lp))
            if "hdl.handle.net" in lp:
                for c in r412.dspace_bitstreams(lp):
                    if c not in [x[1] for x in cands]:
                        cands.append(("dspace_rest", c))
        for loc in (w.get("locations") or []):
            blob = (loc.get("landing_page_url") or "") + " " + (loc.get("pdf_url") or "")
            import re as _re
            m = _re.search(r"(PMC\d+)", blob)
            if m:
                x = (f"https://www.ebi.ac.uk/europepmc/webservices/rest/{m.group(1)}/fullTextXML")
                if x not in [c[1] for c in cands]:
                    cands.append(("europepmc_xml", x))

        base = f"{wid}__{r412.slugify(title)}"
        pdf, txt = PDFDIR / f"{base}.pdf", PDFDIR / f"{base}.txt"
        row = {"id": wid, "title": title[:150], "year": w.get("publication_year"),
               "doi": doi, "oa_status": oa.get("oa_status"),
               "n_candidate_urls": len(cands), "source": "", "status": "", "detail": "",
               "words": "", "path": ""}

        if txt.exists() and len(txt.read_text(errors="ignore").split()) >= 500:
            row.update(source="cached", status="retrieved",
                       words=str(len(txt.read_text(errors='ignore').split())), path=str(txt))
            print(f"  cached    {wid}", flush=True)
            rows.append(row)
            continue

        got = False
        for source, u in cands:
            if source == "europepmc_xml":
                ok, detail = r412.fetch_xml_text(u, txt)
                if ok:
                    row.update(source=source, status="retrieved", detail=detail,
                               words=detail.split()[0], path=str(txt))
                    print(f"  OK        {wid}  via {source}  {detail}", flush=True)
                    got = True
                    break
                continue
            ok, detail = r412.download(u, pdf)
            if not ok:
                continue
            tok, tdetail = r412.extract(pdf, txt)
            if not tok:
                pdf.unlink(missing_ok=True)
                txt.unlink(missing_ok=True)
                continue
            row.update(source=source, status="retrieved", detail=f"{detail}; {tdetail}",
                       words=tdetail.split()[0], path=str(txt))
            print(f"  OK        {wid}  via {source}  {tdetail}", flush=True)
            got = True
            break
        if not got:
            row.update(status="unavailable",
                       detail=("no candidate url" if not cands
                               else f"all {len(cands)} candidate url(s) failed"))
            print(f"  MISSING   {wid}  {row['detail']}  [{row['oa_status']}]", flush=True)
        rows.append(row)

    logp = EXTR / f"{SLUG}-a5-bundle-retrieval-log.csv"
    with logp.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    got = [r for r in rows if r["status"] == "retrieved"]
    miss = [r for r in rows if r["status"] != "retrieved"]
    md = [f"# A.6 — A.5 bundle retrieval for PI call 4 — {len(got)} of {len(rows)}", "",
          "Generated by `source/build/goldset/421_a6_a5_bundle_retrieval.py`. Routes are imported",
          "from `412`, not re-implemented: TICK-074 exists because a shared resolver was copied",
          "into twelve chapters and had to be fixed twelve times.", "",
          "Call 4 ruled A.5 a **bundle, not a wall**, so these records are admissible pending a",
          "full-text pass asking whether the norm component was separately dosed. 3 of the 5",
          "identified records across the substantive walls sit in A.5, which is why this is one of",
          "the two live routes to a non-empty primary cell.", "",
          "**Triage, before reading:** against `410`'s flags none of the 25 carries both a",
          "fertility-outcome marker and an identified-design marker — 22 have the fertility marker",
          "alone and 3 have neither. The prior is therefore low and this pass is a confirmation",
          "exercise, not a hunt. It is still done exhaustively, because a design an abstract does",
          "not name is how a primary-cell study hides.", "",
          f"**Retrieved {len(got)}** · **unavailable {len(miss)}**", "",
          "| id | year | OA | source | words | title |", "|---|---|---|---|---|---|"]
    for r in sorted(rows, key=lambda r: (r["status"] != "retrieved", r["id"])):
        md.append(f"| `{r['id']}` | {r['year']} | {r['oa_status']} | {r['source'] or '—'} | "
                  f"{r['words'] or '—'} | {r['title'][:66].replace('|', '/')} |")
    if miss:
        md += ["", "## Unavailable — for the wantlist", "",
               "| id | OA status | DOI |", "|---|---|---|"]
        for r in miss:
            md.append(f"| `{r['id']}` | {r['oa_status']} | "
                      f"{('`' + r['doi'] + '`') if r['doi'] else '— none —'} |")
    (EXTR / f"{SLUG}-a5-bundle-retrieval-report.md").write_text("\n".join(md) + "\n")
    print(f"\nretrieved {len(got)}/{len(rows)}; wrote {logp.name} and the report")
    return 0


if __name__ == "__main__":
    sys.exit(main())
