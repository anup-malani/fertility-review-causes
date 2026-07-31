#!/usr/bin/env python3
"""Second retrieval pass for C.2.c: reach closed papers through their preprint twins.

The dedup step documented that NBER, SSRN, RePEc and OSF carry separate OpenAlex records for the same
study -- a hazard there, because DOI dedup misses them and citation counts split. Here it is an asset:
the published version of an economics paper is usually paywalled while its working-paper twin is a
free PDF. OpenAlex's `locations` for the published record does NOT include the twin, because OpenAlex
treats them as different works, so the first pass could not see them.

This pass searches OpenAlex by title for every priority record still missing a PDF, collects ALL
sibling records, and tries their OA URLs.

The retrieved file is the WORKING PAPER, not the published article. That matters for extraction:
tables and specifications routinely change between versions. Every file retrieved this way is logged
with `version=preprint_twin` and must be reconciled against the published version before any number
is extracted from it.
"""
import csv
import json
import os
import re
import subprocess
import sys

SLUG = "housing-costs"
LOG = f"extraction/{SLUG}-pdf-retrieval-log.csv"
PDFDIR = f"literature/pdfs/{SLUG}"
MAILTO = "shravanh@uchicago.edu"
UA = f"fertility-review ({MAILTO})"


def title_slug(t):
    t = re.sub(r"<[^>]+>", "", t or "").lower()
    t = re.sub(r"[^a-z0-9]+", "-", t).strip("-")
    return t[:60].rstrip("-")


def siblings(title):
    r = subprocess.run(
        ["curl", "-s", "--max-time", "60", "-G", "https://api.openalex.org/works",
         "--data-urlencode", f"search={title[:150]}",
         "--data-urlencode", "per-page=8", "--data-urlencode", "mailto=" + MAILTO,
         "--data-urlencode", "select=id,doi,title,publication_year,type,best_oa_location,locations"],
        capture_output=True, text=True)
    try:
        return json.loads(r.stdout).get("results", [])
    except Exception:
        return []


def norm(t):
    return re.sub(r"[^a-z0-9]+", " ", (t or "").lower()).strip()


def urls_of(w):
    out = []
    b = w.get("best_oa_location") or {}
    if b.get("pdf_url"):
        out.append(b["pdf_url"])
    for loc in (w.get("locations") or []):
        u = loc.get("pdf_url")
        if u and u not in out:
            out.append(u)
    return out


def download(url, dest):
    r = subprocess.run(["curl", "-sL", "--max-time", "90", "-A", UA, "-o", dest,
                        "-w", "%{http_code}", url], capture_output=True, text=True)
    code = (r.stdout or "").strip()[-3:]
    if not os.path.exists(dest):
        return False, f"http_{code}", 0
    size = os.path.getsize(dest)
    with open(dest, "rb") as fh:
        if fh.read(4) != b"%PDF":
            os.remove(dest)
            return False, f"not_pdf_http_{code}", size
    if size < 20000:
        os.remove(dest)
        return False, f"too_small_{size}", size
    return True, f"http_{code}", size


rows = list(csv.DictReader(open(LOG)))
missing = [r for r in rows if r["download_status"] not in ("ok", "already_present")]
# priority: QUASI_EXP first
missing.sort(key=lambda r: 0 if r["id_strength"] == "QUASI_EXP" else 1)
print(f"retrying {len(missing)} records via sibling versions "
      f"({sum(1 for r in missing if r['id_strength'] == 'QUASI_EXP')} QUASI_EXP)", file=sys.stderr)

recovered = 0
for r in missing:
    sibs = siblings(r["title"])
    target = norm(r["title"])[:70]
    got = False
    for w in sibs:
        if norm(w.get("title"))[:70] != target:
            continue
        if w["id"].rsplit("/", 1)[-1] == r["work_id"]:
            continue                      # the closed record we already tried
        for u in urls_of(w):
            fname = f"{r['work_id']}__{title_slug(r['title'])}.pdf"
            ok, detail, size = download(u, f"{PDFDIR}/{fname}")
            if ok:
                r.update({"download_status": "ok", "detail": f"via_sibling {w.get('doi', '')} {detail}",
                          "bytes": size, "file": fname, "pdf_url": u,
                          "version": "preprint_twin"})
                recovered += 1
                got = True
                print(f"  RECOVERED [{r['id_strength'][:5]}] {r['title'][:56]}", file=sys.stderr)
                break
        if got:
            break

for r in rows:
    r.setdefault("version", "published" if r["download_status"] in ("ok", "already_present") else "")
with open(LOG, "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
    w.writeheader()
    w.writerows(rows)

got_all = [r for r in rows if r["download_status"] in ("ok", "already_present")]
q = [r for r in rows if r["id_strength"] == "QUASI_EXP"]
qgot = [r for r in q if r["download_status"] in ("ok", "already_present")]
print(f"\nrecovered this pass: {recovered}")
print(f"total retrieved: {len(got_all)}/{len(rows)}")
print(f"QUASI_EXP priority set: {len(qgot)}/{len(q)}")
