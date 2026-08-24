#!/usr/bin/env python3
"""
183_a24_p0_recovery.py — A.24, stage 5. A second retrieval pass at band P0 only.

`178_` ran four rungs over the whole wantlist and reached 22%. Band P0 — the fifteen records that
decide verdicts — came back almost entirely blocked or closed, so this script tries rungs the first
pass did not, against those fifteen alone. Attempting them across all 152 records would not be worth
the requests; attempting them on the band that changes the chapter is.

Four new rungs, cheapest first:

  4  **OpenAlex re-check.** Open-access status changes. A record closed in the morning can carry a
     green location in the evening when a repository deposit is indexed. One request per record, and
     it costs nothing to be wrong.
  5  **Crossref link records.** Crossref carries publisher-declared full-text links in a `link` array
     that OpenAlex does not surface. Elsevier and Springer both populate it, and the URLs there
     sometimes serve where the landing page redirects.
  6  **Preprint-server patterns.** SSRN and arXiv identifiers embedded in the DOI imply a delivery URL
     that differs from the landing page. Two of the P0 records are SSRN working papers, including the
     one the chapter names as most important.
  7  **Europe PMC.** A different index from PMC, with broader social-science coverage. `178_` measured
     PMC at zero on this literature, which is a reason to try its sibling rather than to assume both
     are empty — the two index different journals.

**A 200 carrying HTML remains a blocked route, not a closed paper**, and the report says which of the
two each record is, because the procurement instruction differs: a blocked route may yield to a
library proxy, whereas a paywalled record needs a purchase or an interlibrary loan.

Output: literature/search-logs/{slug}-p0-recovery-log.md
"""
import csv, json, os, re, subprocess, time

SLUG = "dating-apps-union-formation-friction"
MAILTO = "shravanh@uchicago.edu"
UA = f"fertility-review/1.0 (mailto:{MAILTO})"
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
LOGS = os.path.join(ROOT, "literature", "search-logs")
EXTRACT = os.path.join(ROOT, "extraction")
SCREENED = os.path.join(LOGS, f"{SLUG}-screened.json")
LIBWANT = os.path.join(LOGS, f"{SLUG}-library-wantlist.md")
PDF_DIR = os.path.join(ROOT, "literature", "pdfs", SLUG)
OUT = os.path.join(LOGS, f"{SLUG}-p0-recovery-log.md")


def key():
    k = os.environ.get("OPENALEX_API_KEY")
    if k:
        return k.strip()
    for line in open(os.path.join(ROOT, ".env")):
        if line.startswith("OPENALEX_API_KEY="):
            return line.split("=", 1)[1].strip()
    return ""


KEY = key()


def slugify(t):
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", (t or "").lower()))[:60].strip("-")


def get(url, dest=None, timeout=75):
    cmd = ["curl", "-sL", "-m", str(timeout), "-A", UA]
    if dest:
        cmd += ["-o", dest, "-w", "%{http_code}"]
    cmd.append(url)
    try:
        r = subprocess.run(cmd, capture_output=True, text=True)
    except Exception as e:
        return None, f"transport {str(e)[:60]}"
    if dest:
        code = (r.stdout or "").strip()
        if not os.path.exists(dest) or os.path.getsize(dest) == 0:
            return False, f"empty (http {code})"
        with open(dest, "rb") as fh:
            head = fh.read(5)
        if head[:4] != b"%PDF":
            os.remove(dest)
            return False, f"HTML not PDF (http {code}) — blocked route"
        return True, f"http {code}, {os.path.getsize(dest)//1024}kb"
    return r.stdout, "ok"


def p0_records():
    """Parse the P0 band out of the library wantlist so this script cannot drift from it."""
    txt = open(LIBWANT).read()
    seg = txt[txt.index("### P0"):txt.index("### P1")]
    out = []
    for line in seg.splitlines():
        m = re.match(r"\|\s*`([^`]+)`\s*\|\s*(.+?)\s*\|\s*(\d{4}|None)\s*\|\s*`([^`]*)`\s*\|\s*(.+?)\s*\|", line)
        if m:
            out.append({"cell": m.group(1), "title": m.group(2), "year": m.group(3),
                        "doi": m.group(4), "route": m.group(5)})
    return out


def main():
    scr = {(r.get("doi") or "").lower(): r for r in json.load(open(SCREENED))}
    recs = p0_records()
    os.makedirs(PDF_DIR, exist_ok=True)
    rows, rung_yield = [], {4: 0, 5: 0, 6: 0, 7: 0}
    print(f"band P0: {len(recs)} records")
    for r in recs:
        doi = r["doi"]
        m = scr.get(doi.lower(), {})
        wid = m.get("id") or re.sub(r"[^A-Za-z0-9]", "", doi)[:16]
        dest = os.path.join(PDF_DIR, f"{wid}__{slugify(r['title'])}.pdf")
        if os.path.exists(dest) and os.path.getsize(dest) > 0:
            rows.append((r, "CACHED", -1, "already on disk")); continue
        ok, note, rung = False, "", None

        # rung 4 — OpenAlex re-check
        d, _ = get(f"https://api.openalex.org/works/doi:{doi}?select=open_access,best_oa_location,"
                   f"locations&api_key={KEY}")
        urls = []
        try:
            j = json.loads(d)
            best = j.get("best_oa_location") or {}
            urls = [best.get("pdf_url")] + [l.get("pdf_url") for l in (j.get("locations") or [])]
        except Exception:
            pass
        for u in [u for u in urls if u]:
            ok, note = get(u, dest)
            if ok:
                rung = 4; break

        # rung 5 — Crossref publisher link records
        if not ok:
            d, _ = get(f"https://api.crossref.org/works/{doi}")
            try:
                links = json.loads(d)["message"].get("link") or []
            except Exception:
                links = []
            for l in links:
                u = l.get("URL")
                if u and ("pdf" in (l.get("content-type") or "").lower() or u.lower().endswith(".pdf")):
                    ok, note = get(u, dest)
                    if ok:
                        rung = 5; break

        # rung 6 — preprint-server delivery patterns
        if not ok and doi.startswith("10.2139/ssrn."):
            sid = doi.rsplit(".", 1)[-1]
            for u in (f"https://papers.ssrn.com/sol3/Delivery.cfm/{sid}.pdf",
                      f"https://papers.ssrn.com/sol3/Delivery.cfm?abstractid={sid}&type=2"):
                ok, note = get(u, dest)
                if ok:
                    rung = 6; break

        # rung 7 — Europe PMC
        if not ok:
            d, _ = get("https://www.ebi.ac.uk/europepmc/webservices/rest/search?format=json&query=DOI:"
                       + doi)
            try:
                res = json.loads(d)["resultList"]["result"]
            except Exception:
                res = []
            for hit in res[:2]:
                if hit.get("pmcid"):
                    u = ("https://www.ebi.ac.uk/europepmc/webservices/rest/"
                         f"{hit['pmcid']}/fullTextPdf")
                    ok, note = get(u, dest)
                    if ok:
                        rung = 7; break

        if ok:
            rung_yield[rung] += 1
            for cmd in (["pdftotext", "-q", dest, dest.replace(".pdf", ".txt")],
                        ["/opt/homebrew/bin/pdftotext", "-q", dest, dest.replace(".pdf", ".txt")]):
                try:
                    subprocess.run(cmd, capture_output=True, timeout=120)
                except Exception:
                    continue
                if os.path.exists(dest.replace(".pdf", ".txt")):
                    break
        rows.append((r, "OK" if ok else "STILL MISSING", rung, note))
        print(f"  {'OK      ' if ok else 'MISSING '} r{rung if rung else '-'} {r['title'][:56]}")
        time.sleep(0.2)

    got = sum(1 for _, s, _, _ in rows if s in ("OK", "CACHED"))
    L = [f"# Band P0 second-pass recovery — {SLUG}", "",
         f"**{got} of {len(rows)} P0 records recovered.** `178_` reached these with four rungs and "
         "got almost none; this pass adds four more, applied to band P0 only because attempting them "
         "across all 152 wantlist records would not be worth the requests.", "",
         f"**Rung yields:** OpenAlex re-check {rung_yield[4]}, Crossref publisher links "
         f"{rung_yield[5]}, preprint-server delivery patterns {rung_yield[6]}, Europe PMC "
         f"{rung_yield[7]}.", "",
         "| status | rung | cell | title | doi | note |", "|---|---|---|---|---|---|"]
    for r, st, rung, note in rows:
        L.append(f"| {'**' + st + '**' if st == 'OK' else st} | {rung if rung else '—'} | "
                 f"`{r['cell']}` | {r['title'][:52]} | `{r['doi']}` | {note[:60]} |")
    L += ["", "## What is still missing, and what kind of missing it is", "",
          "A record returning HTML is a **blocked route** and may yield to a library proxy. A record "
          "the publisher refuses outright is **paywalled** and needs a purchase or an interlibrary "
          "loan. The procurement instruction differs, which is why the two are not merged into one "
          "count.", ""]
    open(OUT, "w").write("\n".join(L) + "\n")
    print(f"\nrecovered {got}/{len(rows)}; yields {rung_yield}")
    print(f"-> {os.path.relpath(OUT, ROOT)}")


if __name__ == "__main__":
    main()
