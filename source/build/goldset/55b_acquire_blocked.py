#!/usr/bin/env python3
"""
55b_acquire_blocked.py — scoped PDF acquisition for the extraction-blocked studies.

Feeds the 35 blocked studies from step 55 through the FREE open-access channels
(no OpenAlex budget spend):
  A. Unpaywall best-OA-location PDF   (free, needs only an email)
  B. landing-page <meta citation_pdf_url>   (publisher HTML -> PDF)
Each candidate is downloaded and %PDF-validated before it counts. Resumable and
cached: a study already holding a valid PDF in literature/pdfs/{slug}/ is skipped,
so re-runs across network windows are cheap. Studies with no DOI (title-keyed) or
no OA copy remain on the want-list for a manual/proxy pull — never faked.

Run in the background; re-run to pick up more as networks allow.
"""
import json, os, re, subprocess, urllib.parse

SLUG = "old-age-security-pension-crowdout"
MAILTO = "shravanh@uchicago.edu"
UA = f"fertility-review/1.0 (mailto:{MAILTO})"
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
def rp(*a): return os.path.join(ROOT, *a)
PDFDIR = rp("literature", "pdfs", SLUG)
os.makedirs(PDFDIR, exist_ok=True)

def slug(t): return (re.sub(r"[^a-z0-9]+", "-", (t or "").lower()).strip("-")[:55]) or "untitled"

def curl(url, head=False):
    cmd = ["curl", "-sL", "-m", "40", "-A", UA]
    if head: cmd += ["-I"]
    cmd += [url]
    return subprocess.run(cmd, capture_output=True, text=True).stdout

def download_pdf(url, dest):
    if not url: return False
    subprocess.run(["curl", "-sL", "-m", "90", "-A", UA, "-o", dest, url], capture_output=True)
    try:
        with open(dest, "rb") as f:
            if f.read(5).startswith(b"%PDF") and os.path.getsize(dest) > 20000:
                return True
    except Exception:
        pass
    if os.path.exists(dest): os.remove(dest)
    return False

def unpaywall_pdf(doi):
    """All OA locations, not just best — a repository copy is often only in the tail."""
    out = curl(f"https://api.unpaywall.org/v2/{urllib.parse.quote(doi)}?email={MAILTO}")
    urls = []
    try:
        d = json.loads(out)
        for loc in ([d.get("best_oa_location")] + (d.get("oa_locations") or [])):
            if loc:
                urls += [loc.get("url_for_pdf"), loc.get("url")]
    except Exception:
        pass
    return [u for u in urls if u]

def landing_pdf(doi):
    """Follow the DOI to its landing page and harvest PDF candidates: the
    citation_pdf_url meta tag, plus any direct .pdf hrefs (works for EconStor,
    CaltechTHESIS, USC theses, SSRN and most repository landing pages)."""
    html = curl(f"https://doi.org/{urllib.parse.quote(doi)}")
    urls = re.findall(r'name=["\']citation_pdf_url["\'][^>]+content=["\']([^"\']+)', html, re.I)
    urls += [u for u in re.findall(r'href=["\']([^"\']+\.pdf[^"\']*)["\']', html, re.I)]
    # relative -> absolute against the resolved host is best-effort; keep absolute ones
    return [u for u in urls if u.startswith("http")]

def s2_pdf(doi):
    out = curl(f"https://api.semanticscholar.org/graph/v1/paper/DOI:{urllib.parse.quote(doi)}"
               "?fields=openAccessPdf")
    try:
        u = (json.loads(out).get("openAccessPdf") or {}).get("url")
        return [u] if u else []
    except Exception:
        return []

studies = json.load(open(rp("output", f"{SLUG}-fine-resolved.json")))
blocked = [r for r in studies if not r.get("pdf")]

log = []
got = 0
for r in blocked:
    doi = r.get("doi")
    if not doi or doi == "unknown":
        log.append((r["title"], "no-DOI", None)); continue
    dest = os.path.join(PDFDIR, f"{r['paperId']}__{slug(r['title'])}.pdf")
    if os.path.exists(dest):
        r["pdf"] = os.path.basename(dest); got += 1
        log.append((r["title"], "already", os.path.basename(dest))); continue
    ok = False
    for src, getter in [("unpaywall", unpaywall_pdf), ("s2", s2_pdf), ("landing", landing_pdf)]:
        for u in getter(doi):
            if download_pdf(u, dest):
                ok = True; break
        if ok:
            break
    if ok:
        r["pdf"] = os.path.basename(dest); got += 1
        log.append((r["title"], f"GOT/{src}", os.path.basename(dest)))
    else:
        log.append((r["title"], "paywalled/none", None))

json.dump(studies, open(rp("output", f"{SLUG}-fine-resolved.json"), "w"),
          ensure_ascii=False, indent=1)

covered = sum(1 for r in studies if r.get("pdf"))
lines = [f"# Acquisition pass (55b) — {SLUG}", "",
         f"Acquired this run: **{got}** new. Total coverage now: **{covered}/{len(studies)}**.", "",
         "| status | study |", "|---|---|"]
for t, st, fn in sorted(log, key=lambda x: x[1]):
    lines.append(f"| {st} | {(t or '')[:70]} |")
open(rp("output", f"{SLUG}-acquisition-log.md"), "w").write("\n".join(lines) + "\n")

print(f"acquisition pass done: +{got} this run; total coverage {covered}/{len(studies)}")
print(f"still blocked: {len(studies)-covered}  (see output/{SLUG}-extraction-wantlist.md)")
