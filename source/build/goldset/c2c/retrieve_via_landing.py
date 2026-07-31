#!/usr/bin/env python3
"""Third retrieval pass for C.2.c: resolve PDFs from OA landing pages.

Pass 1 diagnosed 19 records that OpenAlex marks `is_oa=true` but for which `best_oa_location.pdf_url`
is empty. That is not a paywall -- it is a missing field. The record has a landing_page_url instead,
typically a repository (RePEc, an institutional repo, a journal's own OA page).

Repositories and most journals emit `<meta name="citation_pdf_url">`, the Google Scholar convention,
which points at the actual file. This pass fetches the landing page and follows that tag; it also
accepts an obvious .pdf href when the tag is absent.

Anything still missing after this is genuinely paywalled and belongs in the human/Zotero handoff.
"""
import csv
import os
import re
import subprocess
import sys

SLUG = "housing-costs"
LOG = f"extraction/{SLUG}-pdf-retrieval-log.csv"
PDFDIR = f"literature/pdfs/{SLUG}"
MAILTO = "shravanh@uchicago.edu"
UA = f"Mozilla/5.0 (compatible; fertility-review; {MAILTO})"


def title_slug(t):
    t = re.sub(r"<[^>]+>", "", t or "").lower()
    t = re.sub(r"[^a-z0-9]+", "-", t).strip("-")
    return t[:60].rstrip("-")


def landing_urls(work_id):
    import json
    r = subprocess.run(["curl", "-s", "--max-time", "45",
                        f"https://api.openalex.org/works/{work_id}?mailto={MAILTO}"],
                       capture_output=True, text=True)
    try:
        w = json.loads(r.stdout)
    except Exception:
        return []
    out = []
    for loc in ([w.get("best_oa_location")] + (w.get("locations") or [])):
        if not loc:
            continue
        if loc.get("is_oa") and loc.get("landing_page_url"):
            u = loc["landing_page_url"]
            if u not in out:
                out.append(u)
    return out


def pdf_from_landing(url):
    r = subprocess.run(["curl", "-sL", "--max-time", "60", "-A", UA, url],
                       capture_output=True, text=True, errors="ignore")
    html = r.stdout or ""
    m = re.search(r'<meta[^>]+name=["\']citation_pdf_url["\'][^>]+content=["\']([^"\']+)', html, re.I)
    if m:
        return m.group(1)
    m = re.search(r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+name=["\']citation_pdf_url["\']', html, re.I)
    if m:
        return m.group(1)
    m = re.search(r'href=["\']([^"\']+\.pdf(?:\?[^"\']*)?)["\']', html, re.I)
    if m:
        u = m.group(1)
        if u.startswith("//"):
            return "https:" + u
        if u.startswith("/"):
            base = re.match(r"(https?://[^/]+)", url)
            return (base.group(1) + u) if base else None
        if u.startswith("http"):
            return u
    return None


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
missing.sort(key=lambda r: 0 if r["id_strength"] == "QUASI_EXP" else 1)
print(f"landing-page pass over {len(missing)} records", file=sys.stderr)

rec = 0
for r in missing:
    for lp in landing_urls(r["work_id"]):
        pdf = pdf_from_landing(lp)
        if not pdf:
            continue
        fname = f"{r['work_id']}__{title_slug(r['title'])}.pdf"
        ok, detail, size = download(pdf, f"{PDFDIR}/{fname}")
        if ok:
            r.update({"download_status": "ok", "detail": f"via_landing {detail}",
                      "bytes": size, "file": fname, "pdf_url": pdf,
                      "version": r.get("version") or "published"})
            rec += 1
            print(f"  RECOVERED [{r['id_strength'][:5]}] {r['title'][:56]}", file=sys.stderr)
            break

with open(LOG, "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
    w.writeheader()
    w.writerows(rows)

got = [r for r in rows if r["download_status"] in ("ok", "already_present")]
q = [r for r in rows if r["id_strength"] == "QUASI_EXP"]
qgot = [r for r in q if r["download_status"] in ("ok", "already_present")]
print(f"\nrecovered this pass: {rec}")
print(f"total retrieved: {len(got)}/{len(rows)}")
print(f"QUASI_EXP priority set: {len(qgot)}/{len(q)}")
