#!/usr/bin/env python3
"""
412 — A.6 (TICK-087) stage 5: retrieve full text for the 8 records the screen left unresolved.

Why only 8. The screen (`411`) read 164 records exhaustively and assigned
`PRIMARY_NORM_FERTILITY` to none of them. Eight are `INSUFFICIENT_INFO`: the abstract could not
decide them, so each could in principle carry the estimate the chapter has so far failed to find.
They are the whole of the full-text queue, and retrieving them is what converts "empty so far" into
the closed UNEVALUATED verdict the scope doc pre-registered at §12.

One of the eight decides the chapter
------------------------------------
`W108787496` is the only record in S1_DECISIVE and the highest-degree record in the entire 2,815
pool, cited by 5 of the 15 anchors. It is a 2014 dissertation on why fertility preferences diverge
from realized fertility across three NFHS waves — a normative-adjacent exposure AND a fertility
outcome, with the design hidden behind the word "essays". If the primary cell is non-empty, it is
this record. It is retrieved first and its outcome is reported separately, because an inconclusive
result here is not the same kind of fact as an inconclusive result on the other seven.

Retrieval order, and the ceiling to expect
------------------------------------------
  1. OpenAlex `best_oa_location.pdf_url`, then `open_access.oa_url`, then any location's pdf_url.
  2. Unpaywall by DOI, which indexes repository copies OpenAlex sometimes misses.
  3. Whatever remains goes to a wantlist for library retrieval.

TICK-041 is the standing warning: on B.1 the automated ceiling was 20 of 95, and the pooled estimate
still rests on 5 studies because the other 71 need a human with Zotero and the UChicago proxy. A low
yield here is the expected outcome, not a malfunction — and for this chapter the honest reading is
that **8 records is small enough that a human can finish the job**, which is the opposite of B.1's
position.

Every download is verified rather than assumed
----------------------------------------------
A 200 response is not a PDF. Each file is checked for the `%PDF` magic bytes, then text-extracted
with pdftotext, then the extracted text is checked for a plausible length and for the absence of the
publisher-interstitial phrases that indicate a paywall or a robot check served with status 200
(`validate-a-null-detector-on-positives` applied to retrieval: a file that is not the paper must
read as a failure, not as a success with short text).

Outputs
-------
  literature/pdfs/stigma-reduction-contraception-abortion/<id>__<slug>.{pdf,txt}
  extraction/stigma-reduction-contraception-abortion-pdf-retrieval-log.csv
  extraction/stigma-reduction-contraception-abortion-pdf-retrieval-report.md
  literature/search-logs/stigma-reduction-contraception-abortion-library-wantlist.md
"""
import csv, html, json, re, subprocess, sys, pathlib, time, unicodedata, urllib.parse

MAILTO = "shravanh@uchicago.edu"
OA_BASE = "https://api.openalex.org/works"
UNPAY = "https://api.unpaywall.org/v2"
SLUG = "stigma-reduction-contraception-abortion"
PDFDIR = pathlib.Path("literature/pdfs") / SLUG
LOGDIR = pathlib.Path("literature/search-logs")
EXTR = pathlib.Path("extraction")
SCREENED = EXTR / f"{SLUG}-screened.csv"
DECIDER = "W108787496"

PAYWALL_MARKERS = [
    "just a moment", "enable javascript", "verify you are a human", "cloudflare",
    "access denied", "institutional login", "purchase pdf", "subscribe to",
    "you do not have access", "captcha", "request permission",
]


def _api_key():
    try:
        for line in open(".env"):
            if line.startswith("OPENALEX_API_KEY="):
                return line.split("=", 1)[1].strip().strip('"') or None
    except FileNotFoundError:
        pass
    return None


API_KEY = _api_key()


def slugify(s: str) -> str:
    s = unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode()
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", s.lower())).strip("-")[:62] or "untitled"


def get_json(url: str):
    p = subprocess.run(["curl", "-s", "-S", "-L", "--max-time", "60", url],
                       capture_output=True, text=True)
    if p.returncode != 0:
        return None, f"curl exit {p.returncode}: {p.stderr.strip()[:120]}"
    try:
        return json.loads(p.stdout), None
    except json.JSONDecodeError:
        return None, f"non-JSON: {p.stdout[:120]!r}"


def looks_like_pdf(u: str) -> bool:
    u = (u or "").lower().split("?")[0]
    return u.endswith(".pdf") or "/pdf/" in u or "/bitstream/" in u


def fetch_xml_text(url: str, txt: pathlib.Path):
    """Europe PMC full-text XML -> plain text. Not a PDF path; writes .txt directly."""
    p = subprocess.run(["curl", "-s", "-S", "-L", "--max-time", "120",
                        "-A", f"fertility-review/1.0 (mailto:{MAILTO})", url],
                       capture_output=True, text=True)
    if p.returncode != 0 or not p.stdout.strip():
        return False, f"curl exit {p.returncode}"
    body = p.stdout
    if "<" not in body[:200]:
        return False, "not XML"
    body = re.sub(r"(?s)<(ref-list|back|front)\b.*?</\1>", " ", body)
    body = re.sub(r"(?s)<[^>]+>", " ", body)
    body = html.unescape(re.sub(r"\s+", " ", body)).strip()
    words = len(body.split())
    if words < 500:
        return False, f"only {words} words of XML text"
    txt.write_text(body)
    return True, f"{words:,} words"


def dspace_bitstreams(handle_url: str):
    """Resolve a Handle to a DSpace 7 item and return its ORIGINAL bitstream content URLs.

    DSpace 7 serves a JavaScript app at the handle URL, so the landing page contains no link to
    the file and a naive fetch returns 200 with HTML. The decider (W108787496) is exactly this
    case. The REST API is the only reliable route: /server/api/pid/find resolves the handle to an
    item uuid, then bundles -> ORIGINAL -> bitstreams -> content.
    """
    m = re.search(r"hdl\.handle\.net/(\d+(?:\.\d+)*)/(\S+)", handle_url or "")
    if not m:
        return []
    handle = f"{m.group(1)}/{m.group(2)}"
    p = subprocess.run(["curl", "-s", "-L", "-o", "/dev/null", "-w", "%{url_effective}",
                        "-A", "Mozilla/5.0", handle_url], capture_output=True, text=True)
    eff = (p.stdout or "").strip()
    hm = re.match(r"(https?://[^/]+)", eff)
    if not hm:
        return []
    host = hm.group(1)
    d, _ = get_json(f"{host}/server/api/pid/find?id=hdl:{handle}")
    if not d or not d.get("uuid"):
        return []
    b, _ = get_json(f"{host}/server/api/core/items/{d['uuid']}/bundles")
    out = []
    for bundle in ((b or {}).get("_embedded") or {}).get("bundles", []):
        if bundle.get("name") != "ORIGINAL":
            continue
        href = ((bundle.get("_links") or {}).get("bitstreams") or {}).get("href")
        if not href:
            continue
        bs, _ = get_json(href)
        for x in ((bs or {}).get("_embedded") or {}).get("bitstreams", []):
            c = ((x.get("_links") or {}).get("content") or {}).get("href")
            if c and (x.get("name") or "").lower().endswith(".pdf"):
                out.append(c)
    return out


def wayback(url: str):
    """Last resort: an archived copy of a URL that has since 404'd."""
    d, _ = get_json("http://archive.org/wayback/available?url="
                    + urllib.parse.quote(url or "", safe=""))
    snap = (((d or {}).get("archived_snapshots") or {}).get("closest") or {})
    return snap.get("url") if snap.get("available") else None


def download(url: str, dest: pathlib.Path):
    """Fetch a URL and accept it only if it is really a PDF."""
    p = subprocess.run(
        ["curl", "-s", "-S", "-L", "--max-time", "120", "--compressed",
         "-A", f"Mozilla/5.0 (compatible; fertility-review/1.0; mailto:{MAILTO})",
         "-o", str(dest), "-w", "%{http_code}", url],
        capture_output=True, text=True)
    if p.returncode != 0:
        dest.unlink(missing_ok=True)
        return False, f"curl exit {p.returncode}"
    code = (p.stdout or "").strip()[-3:]
    if not dest.exists() or dest.stat().st_size < 2048:
        dest.unlink(missing_ok=True)
        return False, f"http {code}, too small"
    head = dest.open("rb").read(5)
    if head[:4] != b"%PDF":
        snippet = dest.open("rb").read(400).decode("utf-8", "ignore").lower()
        dest.unlink(missing_ok=True)
        hit = next((m for m in PAYWALL_MARKERS if m in snippet), None)
        return False, f"http {code}, not a PDF" + (f" ({hit})" if hit else "")
    return True, f"http {code}, {dest.stat().st_size // 1024} KB"


def extract(pdf: pathlib.Path, txt: pathlib.Path):
    p = subprocess.run(["pdftotext", "-q", str(pdf), str(txt)], capture_output=True, text=True)
    if p.returncode != 0 or not txt.exists():
        return False, f"pdftotext failed: {p.stderr.strip()[:100]}"
    body = txt.read_text(errors="ignore")
    words = len(body.split())
    if words < 500:
        low = body.lower()
        hit = next((m for m in PAYWALL_MARKERS if m in low), None)
        return False, f"only {words} words" + (f", looks like an interstitial ({hit})" if hit else "")
    return True, f"{words:,} words"


def main():
    ids = [r["id"] for r in csv.DictReader(SCREENED.open())
           if r["cell"] == "INSUFFICIENT_INFO"]
    ids.sort(key=lambda i: (i != DECIDER))          # the decider first
    if not ids:
        print("no INSUFFICIENT_INFO records to retrieve", file=sys.stderr)
        return 2
    PDFDIR.mkdir(parents=True, exist_ok=True)

    url = (f"{OA_BASE}?filter=openalex:{'|'.join(ids)}&per_page=50"
           f"&select=id,doi,display_name,publication_year,type,open_access,"
           f"best_oa_location,locations&mailto={MAILTO}")
    if API_KEY:
        url += f"&api_key={API_KEY}"
    d, err = get_json(url)
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
        # A repository often records a direct PDF in landing_page_url and leaves pdf_url null.
        # Missing this cost 3 of 8 records on the first run, including the decider, whose PDF sits
        # in DukeSpace as a plain bitstream URL.
        for loc in (w.get("locations") or []):
            lp = loc.get("landing_page_url") or ""
            if looks_like_pdf(lp) and lp not in [c[1] for c in cands]:
                cands.append(("landing_page_pdf", lp))
        # DSpace repositories: resolve the handle through the REST API.
        for loc in (w.get("locations") or []):
            lp = loc.get("landing_page_url") or ""
            if "hdl.handle.net" in lp:
                for c in dspace_bitstreams(lp):
                    if c not in [x[1] for x in cands]:
                        cands.append(("dspace_rest", c))
        # Europe PMC serves full-text XML for PMC records without the robot check that blocks the
        # PMC and publisher PDF endpoints.
        for loc in (w.get("locations") or []):
            m = re.search(r"(PMC\d+)", (loc.get("landing_page_url") or "")
                          + " " + (loc.get("pdf_url") or ""))
            if m:
                x = (f"https://www.ebi.ac.uk/europepmc/webservices/rest/{m.group(1)}"
                     f"/fullTextXML")
                if x not in [c[1] for c in cands]:
                    cands.append(("europepmc_xml", x))
        if doi:
            u, uerr = get_json(f"{UNPAY}/{urllib.parse.quote(doi)}?email={MAILTO}")
            time.sleep(0.3)
            if u:
                for loc in ([u.get("best_oa_location")] + (u.get("oa_locations") or [])):
                    if loc and loc.get("url_for_pdf") and \
                            loc["url_for_pdf"] not in [c[1] for c in cands]:
                        cands.append(("unpaywall", loc["url_for_pdf"]))

        base = f"{wid}__{slugify(title)}"
        pdf, txt = PDFDIR / f"{base}.pdf", PDFDIR / f"{base}.txt"
        row = {"id": wid, "title": title[:150], "year": w.get("publication_year"),
               "type": w.get("type"), "doi": doi, "is_oa": oa.get("is_oa"),
               "oa_status": oa.get("oa_status"), "n_candidate_urls": len(cands),
               "source": "", "status": "", "detail": "", "words": "",
               "path": "", "is_decider": "yes" if wid == DECIDER else "no"}

        if pdf.exists() and txt.exists():
            ok, detail = extract(pdf, txt)
            row.update(source="cached", status="retrieved" if ok else "corrupt",
                       detail=detail, path=str(txt) if ok else "")
            rows.append(row)
            print(f"  cached    {wid}  {detail}", flush=True)
            continue

        got = False
        for source, u in cands:
            if source == "europepmc_xml":
                xok, xdetail = fetch_xml_text(u, txt)
                if not xok:
                    print(f"    x {source}: {xdetail}", flush=True)
                    continue
                row.update(source=source, status="retrieved",
                           detail=f"full-text XML; {xdetail}",
                           words=xdetail.split()[0], path=str(txt))
                print(f"  OK        {wid}  via {source}  {xdetail}", flush=True)
                got = True
                break
            ok, detail = download(u, pdf)
            if not ok:
                print(f"    x {source}: {detail}", flush=True)
                continue
            tok, tdetail = extract(pdf, txt)
            if not tok:
                print(f"    x {source}: pdf ok but {tdetail}", flush=True)
                pdf.unlink(missing_ok=True)
                txt.unlink(missing_ok=True)
                continue
            row.update(source=source, status="retrieved", detail=f"{detail}; {tdetail}",
                       words=tdetail.split()[0], path=str(txt))
            print(f"  OK        {wid}  via {source}  {tdetail}", flush=True)
            got = True
            break
        if not got and cands:
            for _src, u in list(cands):
                if not looks_like_pdf(u):
                    continue
                arch = wayback(u)
                if not arch:
                    continue
                ok, detail = download(arch, pdf)
                if not ok:
                    print(f"    x wayback: {detail}", flush=True)
                    continue
                tok, tdetail = extract(pdf, txt)
                if not tok:
                    pdf.unlink(missing_ok=True)
                    txt.unlink(missing_ok=True)
                    print(f"    x wayback: pdf ok but {tdetail}", flush=True)
                    continue
                row.update(source="wayback", status="retrieved",
                           detail=f"archived copy; {detail}; {tdetail}",
                           words=tdetail.split()[0], path=str(txt))
                print(f"  OK        {wid}  via wayback  {tdetail}", flush=True)
                got = True
                break
        if not got:
            row.update(status="unavailable",
                       detail=("no candidate url" if not cands
                               else f"all {len(cands)} candidate url(s) failed"))
            print(f"  MISSING   {wid}  {row['detail']}"
                  + ("   <-- THIS IS THE DECIDER" if wid == DECIDER else ""), flush=True)
        rows.append(row)

    logp = EXTR / f"{SLUG}-pdf-retrieval-log.csv"
    with logp.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    got = [r for r in rows if r["status"] == "retrieved"]
    missing = [r for r in rows if r["status"] != "retrieved"]
    rep = [f"# A.6 full-text retrieval — {len(got)} of {len(rows)}", "",
           "Generated by `source/build/goldset/412_a6_fulltext_retrieval.py`. Do not edit by hand;",
           "re-run the script. Cached files are re-verified rather than trusted.", "",
           "These 8 records are the entire full-text queue: the screen (`411`) read 164 records",
           "exhaustively, assigned `PRIMARY_NORM_FERTILITY` to none, and left these unresolved.",
           "Retrieving them is what converts an empty-so-far primary cell into the closed",
           "UNEVALUATED verdict the scope doc pre-registered at §12.", "",
           "Every download is verified for `%PDF` magic bytes and then for extracted-text length,",
           "because a paywall or robot check is commonly served with HTTP 200.", "",
           f"**Retrieved {len(got)}** · **unavailable {len(missing)}**", ""]
    dec = next((r for r in rows if r["is_decider"] == "yes"), None)
    if dec:
        rep += [f"## The decider: `{dec['id']}`", "",
                f"*{dec['title']}* ({dec['year']}, {dec['type']}) — **{dec['status']}**: "
                f"{dec['detail']}", "",
                "This is the only S1_DECISIVE record and the highest-degree record in the 2,815",
                "pool. If `PRIMARY_NORM_FERTILITY` is non-empty it is this record, so its",
                "retrieval status is reported separately from the other seven.", ""]
    rep += ["## All records", "",
            "| id | year | type | OA | source | status | detail |", "|---|---|---|---|---|---|---|"]
    for r in rows:
        rep.append(f"| `{r['id']}`{' **(decider)**' if r['is_decider'] == 'yes' else ''} | "
                   f"{r['year']} | {r['type']} | {r['oa_status']} | {r['source'] or '—'} | "
                   f"{r['status']} | {r['detail']} |")
    (EXTR / f"{SLUG}-pdf-retrieval-report.md").write_text("\n".join(rep) + "\n")

    want = [f"# A.6 library wantlist — {len(missing)} record(s)", "",
            "Generated by `source/build/goldset/412_a6_fulltext_retrieval.py`.", "",
            "Automated open-access retrieval could not reach these. TICK-041's warning applies:",
            "on B.1 the automated ceiling was 20 of 95 and the rest needed a human with Zotero and",
            "the UChicago proxy. The difference here is scale — this list is short enough to",
            "finish by hand, and one of these records decides whether this chapter's primary cell",
            "can be closed.", ""]
    if missing:
        want += ["| id | year | type | DOI | why it matters |", "|---|---|---|---|---|"]
        for r in missing:
            why = ("**THE DECIDER** — only S1 record, cited by 5 of 15 anchors; decides the "
                   "primary cell" if r["is_decider"] == "yes" else "screen could not resolve on abstract")
            want.append(f"| `{r['id']}` | {r['year']} | {r['type']} | "
                        f"{('`' + r['doi'] + '`') if r['doi'] else '— none in OpenAlex —'} | {why} |")
        want += ["", "Titles, for searching a catalogue by hand:", ""]
        for r in missing:
            want.append(f"- `{r['id']}` — *{r['title']}* ({r['year']})")
    else:
        want += ["Nothing outstanding: all 8 were retrieved automatically."]
    (LOGDIR / f"{SLUG}-library-wantlist.md").write_text("\n".join(want) + "\n")

    print(f"\nretrieved {len(got)}/{len(rows)}; wrote {logp.name}, the report and the wantlist")
    if dec and dec["status"] != "retrieved":
        print("the decider was NOT retrieved — the primary cell cannot be closed yet",
              file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
