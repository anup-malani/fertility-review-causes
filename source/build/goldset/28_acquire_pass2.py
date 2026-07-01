#!/usr/bin/env python3
"""
Step 28 - Second-pass PDF acquisition for the NEEDS_MANUAL residual from step 27.

The step-23 enrichment failed for these papers largely because their W-IDs were DEAD/DRIFTED
(this corpus has ~40% W-ID rot) - so they had no OA url and often no DOI. But the papers still
exist under CURRENT W-IDs. So the primary recovery channel here is:

  A. OpenAlex TITLE SEARCH -> re-resolve to a live work (bypasses the dead W-ID) -> harvest its
     OA locations (best_oa_location / locations[].pdf_url / open_access.oa_url) AND backfill the
     DOI. OpenAlex is not hard-throttled (subject only to the daily budget), unlike S2.
  B. Landing-page PDF extraction: fetch each candidate OA url; if it is HTML, pull the
     <meta name="citation_pdf_url"> the publisher/repository exposes.
  C. Unpaywall on any newly backfilled DOI.
  D. Semantic Scholar openAccessPdf - SINGLE best-effort attempt only (S2 hard-throttles the
     unauthenticated shared IP; no long backoff, skip on 429).

C2 discipline: title-search hits (OpenAlex or S2) accepted only at Jaccard >= 0.80 + year gate.
Residual (truly no free copy) -> click-ready RA want-list for institutional-proxy pull.

Input : {slug}-metaanalysis-studies.json, {slug}-pdf-manifest.json
Output: more PDFs in literature/pdfs/{slug}/ ; refreshed {slug}-pdf-manifest.json ;
        {slug}-doi-backfill.json ; output/{slug}-pdf-wantlist.md
"""
import json, re, sys, time, hashlib, urllib.parse, subprocess
from pathlib import Path
from collections import Counter

ROOT = Path("/Users/shravanhari/~/Anup RA/projects/fertility-review-causes")
SL = ROOT / "literature/search-logs"
OUT = ROOT / "output"
SLUG = "old-age-security-pension-crowdout"
PDFDIR = ROOT / "literature/pdfs" / SLUG
CACHE = ROOT / "source/build/goldset/cache"
MAILTO = "shravanh@uchicago.edu"
STOP = {"the","a","an","of","and","in","on","for","from","to","its","by","new","is","with","evidence"}

def toks(t): return {w for w in re.sub(r"[^a-z0-9\s]"," ",(t or "").lower()).split() if w not in STOP}
def jacc(a,b):
    A,B=toks(a),toks(b); return len(A&B)/len(A|B) if (A|B) else 0.0
def slug(t): return re.sub(r"[^a-z0-9]+","-",(t or "").lower()).strip("-")[:60] or "untitled"
def norm(d): return (d or "").replace("https://doi.org/","").strip().lower() or None

def curl_pdf(url, dest):
    try:
        subprocess.run(["curl","-sL","--max-time","90","-A",f"fertility-review/1.0 (mailto:{MAILTO})",
                        "-o",str(dest),url], capture_output=True, timeout=100)
    except Exception: return False
    if dest.exists() and dest.stat().st_size > 2048:
        with open(dest,"rb") as f:
            if f.read(5).startswith(b"%PDF"): return True
    if dest.exists(): dest.unlink()
    return False

def curl_text(url, t=40):
    try:
        return subprocess.run(["curl","-sL","--max-time",str(t),"-A",f"fertility-review/1.0 (mailto:{MAILTO})",url],
                              capture_output=True,text=True,timeout=t+10).stdout
    except Exception: return ""

def cached_json(url, tag, single=False):
    cf=CACHE/f"{tag}_{hashlib.sha1(url.encode()).hexdigest()[:16]}.json"
    if cf.exists():
        d=json.load(open(cf))
        if d and not (isinstance(d,dict) and ("error" in d or ("message" in d and "data" not in d and "results" not in d))):
            return d
        cf.unlink()
    r=subprocess.run(["curl","-s","--max-time","30","-A",f"fertility-review/1.0 (mailto:{MAILTO})",url],
                     capture_output=True,text=True)
    try: d=json.loads(r.stdout)
    except Exception: d={}
    ok = d and not (isinstance(d,dict) and ("error" in d or ("message" in d and "data" not in d and "results" not in d)))
    if ok: json.dump(d,open(cf,"w"))
    time.sleep(0.4 if single else 1.0)
    return d if ok else {}

def oa_from_work(w):
    urls=[]
    for loc in [w.get("best_oa_location"), w.get("primary_location")] + (w.get("locations") or []):
        if loc and loc.get("pdf_url"): urls.append(loc["pdf_url"])
        if loc and (loc.get("landing_page_url")): urls.append(loc["landing_page_url"])
    if (w.get("open_access") or {}).get("oa_url"): urls.append(w["open_access"]["oa_url"])
    seen=[]; [seen.append(u) for u in urls if u and u not in seen]
    return seen

def openalex_search(title, year):
    sel="id,display_name,publication_year,doi,best_oa_location,primary_location,locations,open_access"
    url=f"https://api.openalex.org/works?search={urllib.parse.quote(title)}&select={sel}&per-page=5&mailto={MAILTO}"
    d=cached_json(url,"oasearch")
    for w in d.get("results",[]):
        if jacc(title, w.get("display_name") or "")>=0.80 and (not year or not w.get("publication_year") or abs(w["publication_year"]-year)<=3):
            return oa_from_work(w), norm(w.get("doi"))
    return [], None

def s2_besteffort(doi, title, year):
    f="fields=openAccessPdf,externalIds,title,year"
    d={}
    if doi: d=cached_json(f"https://api.semanticscholar.org/graph/v1/paper/DOI:{urllib.parse.quote(doi)}?{f}","s2doi",single=True)
    if not (d and d.get("openAccessPdf")) and title:
        s=cached_json(f"https://api.semanticscholar.org/graph/v1/paper/search?query={urllib.parse.quote(title)}&limit=5&{f}","s2search",single=True)
        for c in (s.get("data") or []):
            if jacc(title,c.get("title") or "")>=0.80: d=c; break
    pdf=(d.get("openAccessPdf") or {}).get("url") if d else None
    dbf=(d.get("externalIds") or {}).get("DOI") if d else None
    return pdf, (dbf.lower() if dbf else None)

def unpaywall_pdf(doi):
    d=cached_json(f"https://api.unpaywall.org/v2/{urllib.parse.quote(doi)}?email={MAILTO}","upw")
    loc=(d.get("best_oa_location") or {})
    return loc.get("url_for_pdf") or loc.get("url")

def landing_pdf(url):
    html=curl_text(url)
    if not html or "<" not in html: return None
    m=re.search(r'name=["\']citation_pdf_url["\'][^>]*content=["\']([^"\']+)["\']',html,re.I) or \
      re.search(r'content=["\']([^"\']+)["\'][^>]*name=["\']citation_pdf_url["\']',html,re.I)
    return m.group(1) if m else None

def main():
    studies={s["paperId"]:s for s in json.load(open(SL/f"{SLUG}-metaanalysis-studies.json"))}
    manifest=json.load(open(SL/f"{SLUG}-pdf-manifest.json"))
    residual=[x for x in manifest if x["status"]=="NEEDS_MANUAL"]
    print(f"pass-2 over {len(residual)} residual...",file=sys.stderr)

    doi_backfill={}; recovered=0
    for i,x in enumerate(residual,1):
        pid=x["paperId"]; s=studies.get(pid,{}); title=x.get("title"); year=s.get("year")
        doi=x.get("doi")
        fn=PDFDIR/f"{pid}__{slug(title)}.pdf"
        cands=list(s.get("oa_urls") or [])

        # A. OpenAlex re-resolution (fresh W-ID -> OA urls + DOI)
        oa_urls, oa_doi = openalex_search(title, year) if title else ([], None)
        cands = oa_urls + cands
        if oa_doi and not doi: doi=oa_doi; doi_backfill[pid]=oa_doi

        # C. Unpaywall on any DOI we now have
        if doi:
            u=unpaywall_pdf(doi)
            if u: cands.insert(0,u)

        # D. S2 best-effort (single attempt)
        s2pdf,s2doi=s2_besteffort(doi,title,year)
        if s2doi and not doi: doi_backfill.setdefault(pid,s2doi)
        if s2pdf: cands.append(s2pdf)

        # B. landing-page extraction on everything HTML, plus raw candidates
        expanded=[]
        for u in cands:
            expanded.append(u)
            if not u.lower().endswith(".pdf"):
                lp=landing_pdf(u)
                if lp: expanded.append(lp)
        seen=[]; [seen.append(u) for u in expanded if u and u not in seen]

        got=next((u for u in seen if curl_pdf(u,fn)),None)
        if got:
            x["status"]="FETCHED"; x["file"]=fn.name; x["source_url"]=got; x["via"]="pass2"
            recovered+=1
        print(f"  {i}/{len(residual)} {'OK' if got else '..'} (+{recovered}) {(title or '')[:45]}",file=sys.stderr)

    json.dump(manifest,open(SL/f"{SLUG}-pdf-manifest.json","w"),indent=2)
    json.dump(doi_backfill,open(SL/f"{SLUG}-doi-backfill.json","w"),indent=2)

    cnt=Counter(x["status"] for x in manifest)
    still=[x for x in manifest if x["status"]=="NEEDS_MANUAL"]
    L=[f"# OAS meta-analysis — PDF want-list (RA institutional-proxy pull)\n",
       f"Auto-fetch recovered **{cnt['FETCHED']}/{len(manifest)}**; **{len(still)}** still need manual retrieval.  ",
       f"For each: open the DOI link via the UChicago proxy, else search the title in Google Scholar.\n",
       "| # | Title | Year | DOI / link | Tier | reason |","|--:|---|--:|---|:--:|---|"]
    for i,x in enumerate(still,1):
        d=x.get("doi") or doi_backfill.get(x["paperId"])
        link=f"https://doi.org/{d}" if d else "(no DOI — search by title)"
        L.append(f"| {i} | {(x['title'] or '')[:70].replace('|','/')} | {studies.get(x['paperId'],{}).get('year') or ''} | {link} | T{x['tier']} | {x.get('reason','')} |")
    (OUT/f"{SLUG}-pdf-wantlist.md").write_text("\n".join(L)+"\n")

    print(f"\npass-2 recovered {recovered}; total {dict(cnt)}; DOI backfilled {len(doi_backfill)}",file=sys.stderr)
    print(f"want-list -> output/{SLUG}-pdf-wantlist.md",file=sys.stderr)

if __name__=="__main__":
    main()
