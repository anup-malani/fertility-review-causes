#!/usr/bin/env python3
"""Open-access PDF retrieval for the C.2.c gated set.

Priority order: the 15 QUASI_EXP first, then the rest of the 78 PRIMARY. Follows the D.3.b/B.1
conventions -- PDFs to literature/pdfs/<slug>/ as W<id>__<title-slug>.pdf, a retrieval log CSV in
extraction/.

B.1 hit an automated ceiling at 20/95 and needed a human in Zotero with the UChicago proxy. The point
of this script is therefore not to get everything; it is to get what open access allows and to emit an
UNAMBIGUOUS handoff list of what it could not, so the human step is a short worklist rather than a
re-derivation.
"""
import csv
import json
import os
import re
import subprocess
import sys

SLUG = "housing-costs"
GATE = "extraction/housing-costs-ra-gate.csv"
PDFDIR = f"literature/pdfs/{SLUG}"
LOG = f"extraction/{SLUG}-pdf-retrieval-log.csv"
MAILTO = "shravanh@uchicago.edu"
UA = f"fertility-review ({MAILTO})"


def title_slug(t):
    t = re.sub(r"<[^>]+>", "", t or "").lower()
    t = re.sub(r"[^a-z0-9]+", "-", t).strip("-")
    return t[:60].rstrip("-")


def oa_lookup(work_ids):
    """Batch OpenAlex for OA locations."""
    out = {}
    for i in range(0, len(work_ids), 50):
        batch = work_ids[i:i + 50]
        r = subprocess.run(
            ["curl", "-s", "--max-time", "60", "-G", "https://api.openalex.org/works",
             "--data-urlencode", "filter=openalex_id:" + "|".join(batch),
             "--data-urlencode", "per-page=50", "--data-urlencode", "mailto=" + MAILTO,
             "--data-urlencode", "select=id,doi,title,open_access,best_oa_location,locations"],
            capture_output=True, text=True)
        try:
            data = json.loads(r.stdout)
        except Exception:
            continue
        for w in data.get("results", []):
            out[w["id"].rsplit("/", 1)[-1]] = w
    return out


def pdf_urls(w):
    """Every candidate PDF url, best first."""
    urls = []
    b = w.get("best_oa_location") or {}
    if b.get("pdf_url"):
        urls.append(b["pdf_url"])
    for loc in (w.get("locations") or []):
        u = loc.get("pdf_url")
        if u and u not in urls:
            urls.append(u)
    return urls


def download(url, dest):
    r = subprocess.run(
        ["curl", "-sL", "--max-time", "90", "-A", UA, "-o", dest, "-w", "%{http_code}", url],
        capture_output=True, text=True)
    code = (r.stdout or "").strip()[-3:]
    if not os.path.exists(dest):
        return "fail", f"http_{code}", 0
    size = os.path.getsize(dest)
    with open(dest, "rb") as fh:
        head = fh.read(5)
    if head[:4] != b"%PDF":
        os.remove(dest)
        return "fail", f"not_pdf_http_{code}", size
    if size < 20000:
        os.remove(dest)
        return "fail", f"too_small_{size}", size
    return "ok", f"http_{code}", size


def main():
    os.makedirs(PDFDIR, exist_ok=True)
    rows = [r for r in csv.DictReader(open(GATE)) if r["ra_verdict"].startswith("KEEP")]
    rows.sort(key=lambda r: (0 if r["id_strength"] == "QUASI_EXP" else 1, r["year"]))
    meta = oa_lookup([r["openalex"] for r in rows])
    existing = set(os.listdir(PDFDIR))

    out = []
    for r in rows:
        w = meta.get(r["openalex"], {})
        oa = (w.get("open_access") or {})
        fname = f"{r['openalex']}__{title_slug(r['title'])}.pdf"
        status, detail, size, used = "", "", 0, ""
        if fname in existing:
            status, detail, size = "already_present", "skip", os.path.getsize(f"{PDFDIR}/{fname}")
        else:
            urls = pdf_urls(w)
            if not urls:
                status, detail = "no_oa_url", oa.get("oa_status", "closed")
            for u in urls:
                status, detail, size = download(u, f"{PDFDIR}/{fname}")
                used = u
                if status == "ok":
                    break
        out.append({
            "work_id": r["openalex"], "doi": r["doi"], "id_strength": r["id_strength"],
            "cell": r["ra_verdict"], "year": r["year"], "venue": r["venue"],
            "oa_status": oa.get("oa_status", ""), "is_oa": oa.get("is_oa", ""),
            "pdf_url": used, "download_status": status, "detail": detail,
            "bytes": size, "file": fname if status in ("ok", "already_present") else "",
            "title": r["title"],
        })
        print(f"  [{r['id_strength'][:5]:<5}] {status:<15} {r['title'][:58]}", file=sys.stderr)

    with open(LOG, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(out[0].keys()))
        w.writeheader()
        w.writerows(out)

    got = [o for o in out if o["download_status"] in ("ok", "already_present")]
    q = [o for o in out if o["id_strength"] == "QUASI_EXP"]
    qgot = [o for o in q if o["download_status"] in ("ok", "already_present")]
    print(f"\nretrieved {len(got)}/{len(out)} overall")
    print(f"retrieved {len(qgot)}/{len(q)} of the QUASI_EXP priority set")
    print(f"log -> {LOG}")


if __name__ == "__main__":
    main()
