#!/usr/bin/env python3
"""
Step 30 - Third-pass PDF acquisition for the NEEDS_MANUAL residual.

Fixes the step-28 miss: pass-2 leaned on OpenAlex's /works?search= endpoint, which is
anonymously rate-limited under load ("use a free API key"). But the OpenAlex /works/{doi}
OBJECT endpoint is NOT throttled, and Unpaywall + Semantic Scholar are up. So:

  DOI-bearing residuals (no key needed):
    A. OpenAlex GET /works/https://doi.org/{doi}  (unthrottled) -> harvest OA locations
    B. Unpaywall best_oa_location (keyed on DOI)
    C. Semantic Scholar openAccessPdf by DOI (with real backoff, not single-shot)
    D. landing-page <meta citation_pdf_url> extraction on any HTML candidate

  No-DOI residuals (dead-WID snowball canon):
    E. Semantic Scholar TITLE search -> openAccessPdf and/or backfill a DOI (then A-D)
    F. OpenAlex TITLE search -> ONLY if OPENALEX_API_KEY is set (else skipped, needs key)

API keys (optional, picked up from env; lift the search rate-limit):
    OPENALEX_API_KEY  -> https://openalex.org/rest-api  (free, instant, self-serve)
    S2_API_KEY        -> Semantic Scholar (application; unauth tier still used without it)

C2 discipline: title-search hits accepted only at Jaccard >= 0.80 + year gate (+/-3y).
Idempotent: only touches rows still NEEDS_MANUAL; existing PDFs are left in place.

Input : {slug}-metaanalysis-studies.json, {slug}-pdf-manifest.json
Output: more PDFs in literature/pdfs/{slug}/ ; refreshed {slug}-pdf-manifest.json ;
        {slug}-doi-backfill.json (merged) ; output/{slug}-pdf-wantlist.md (refreshed)
"""
import json, re, sys, os, time, hashlib, urllib.parse, subprocess
from pathlib import Path
from collections import Counter

ROOT = Path("/Users/shravanhari/~/Anup RA/projects/fertility-review-causes")
SL = ROOT / "literature/search-logs"
OUT = ROOT / "output"
SLUG = "old-age-security-pension-crowdout"
PDFDIR = ROOT / "literature/pdfs" / SLUG; PDFDIR.mkdir(parents=True, exist_ok=True)
CACHE = ROOT / "source/build/goldset/cache"
MAILTO = "shravanh@uchicago.edu"
OA_KEY = os.environ.get("OPENALEX_API_KEY", "").strip()
S2_KEY = os.environ.get("S2_API_KEY", "").strip()
UA = f"fertility-review/1.0 (mailto:{MAILTO})"
STOP = {"the","a","an","of","and","in","on","for","from","to","its","by","new","is","with","evidence"}

def toks(t): return {w for w in re.sub(r"[^a-z0-9\s]"," ",(t or "").lower()).split() if w not in STOP}
def jacc(a,b):
    A,B=toks(a),toks(b); return len(A&B)/len(A|B) if (A|B) else 0.0
def slug(t): return re.sub(r"[^a-z0-9]+","-",(t or "").lower()).strip("-")[:60] or "untitled"
def norm(d): return (d or "").replace("https://doi.org/","").strip().lower() or None

def curl(url, headers=None, t=30):
    cmd=["curl","-s","--max-time",str(t),"-A",UA]
    for h in (headers or []): cmd += ["-H",h]
    cmd.append(url)
    try: return subprocess.run(cmd,capture_output=True,text=True,timeout=t+10).stdout
    except Exception: return ""

def curl_pdf(url, dest):
    try:
        subprocess.run(["curl","-sL","--max-time","90","-A",UA,"-o",str(dest),url],
                       capture_output=True, timeout=100)
    except Exception: return False
    if dest.exists() and dest.stat().st_size > 2048:
        with open(dest,"rb") as f:
            if f.read(5).startswith(b"%PDF"): return True
    if dest.exists(): dest.unlink()
    return False

def cached_json(url, tag, headers=None, pause=0.5):
    cf=CACHE/f"{tag}_{hashlib.sha1(url.encode()).hexdigest()[:16]}.json"
    if cf.exists():
        try: d=json.load(open(cf))
        except Exception: d=None
        bad = (not d) or (isinstance(d,dict) and ("error" in d or ("message" in d and "data" not in d and "results" not in d and "id" not in d)))
        if not bad: return d
        cf.unlink()
    txt=curl(url, headers=headers)
    try: d=json.loads(txt)
    except Exception: d={}
    bad = (not d) or (isinstance(d,dict) and ("error" in d or ("message" in d and "data" not in d and "results" not in d and "id" not in d)))
    if not bad: json.dump(d,open(cf,"w"))
    time.sleep(pause)
    return {} if bad else d

def oa_from_work(w):
    urls=[]
    for loc in [w.get("best_oa_location"), w.get("primary_location")] + (w.get("locations") or []):
        if loc and loc.get("pdf_url"): urls.append(loc["pdf_url"])
        if loc and loc.get("landing_page_url"): urls.append(loc["landing_page_url"])
    if (w.get("open_access") or {}).get("oa_url"): urls.append(w["open_access"]["oa_url"])
    seen=[]; [seen.append(u) for u in urls if u and u not in seen]
    return seen

def oa_by_doi(doi):
    """UNTHROTTLED object endpoint."""
    url=f"https://api.openalex.org/works/https://doi.org/{urllib.parse.quote(doi)}?mailto={MAILTO}"
    if OA_KEY: url+=f"&api_key={OA_KEY}"
    w=cached_json(url,"oadoi")
    return (oa_from_work(w), norm(w.get("doi"))) if w else ([],None)

def oa_search(title, year):
    """Throttled search endpoint - only useful with a key."""
    if not OA_KEY: return [], None
    sel="id,display_name,publication_year,doi,best_oa_location,primary_location,locations,open_access"
    url=f"https://api.openalex.org/works?search={urllib.parse.quote(title)}&select={sel}&per-page=5&mailto={MAILTO}&api_key={OA_KEY}"
    d=cached_json(url,"oasearch")
    for w in d.get("results",[]):
        if jacc(title,w.get("display_name") or "")>=0.80 and (not year or not w.get("publication_year") or abs(w["publication_year"]-year)<=3):
            return oa_from_work(w), norm(w.get("doi"))
    return [], None

def s2_get(url, tag):
    hdr=[f"x-api-key: {S2_KEY}"] if S2_KEY else None
    for attempt in range(4):
        d=cached_json(url,tag,headers=hdr,pause=1.0)
        if d: return d
        time.sleep(2.0*(attempt+1))   # real backoff on 429/empty
    return {}

def s2_pdf(doi, title, year):
    f="fields=openAccessPdf,externalIds,title,year"
    d={}
    if doi:
        d=s2_get(f"https://api.semanticscholar.org/graph/v1/paper/DOI:{urllib.parse.quote(doi)}?{f}","s2doi")
    if not (d and d.get("openAccessPdf")) and title:
        s=s2_get(f"https://api.semanticscholar.org/graph/v1/paper/search?query={urllib.parse.quote(title)}&limit=5&{f}","s2search")
        for c in (s.get("data") or []):
            if jacc(title,c.get("title") or "")>=0.80 and (not year or not c.get("year") or abs((c.get("year") or 0)-year)<=3):
                d=c; break
    pdf=(d.get("openAccessPdf") or {}).get("url") if d else None
    dbf=(d.get("externalIds") or {}).get("DOI") if d else None
    return pdf, (dbf.lower() if dbf else None)

def unpaywall_pdf(doi):
    d=cached_json(f"https://api.unpaywall.org/v2/{urllib.parse.quote(doi)}?email={MAILTO}","upw")
    loc=(d.get("best_oa_location") or {})
    return loc.get("url_for_pdf") or loc.get("url")

def landing_pdf(url):
    html=curl(url, t=40)
    if not html or "<" not in html: return None
    m=re.search(r'name=["\']citation_pdf_url["\'][^>]*content=["\']([^"\']+)["\']',html,re.I) or \
      re.search(r'content=["\']([^"\']+)["\'][^>]*name=["\']citation_pdf_url["\']',html,re.I)
    return m.group(1) if m else None

def main():
    studies={s["paperId"]:s for s in json.load(open(SL/f"{SLUG}-metaanalysis-studies.json"))}
    manifest=json.load(open(SL/f"{SLUG}-pdf-manifest.json"))
    bf_path=SL/f"{SLUG}-doi-backfill.json"
    doi_backfill=json.load(open(bf_path)) if bf_path.exists() and bf_path.stat().st_size>2 else {}
    residual=[x for x in manifest if x["status"]=="NEEDS_MANUAL"]
    print(f"pass-3 over {len(residual)} residual  [OA_KEY={'set' if OA_KEY else 'none'}  S2_KEY={'set' if S2_KEY else 'none'}]",file=sys.stderr)

    recovered=0
    for i,x in enumerate(residual,1):
        pid=x["paperId"]; s=studies.get(pid,{}); title=x.get("title"); year=s.get("year")
        doi=x.get("doi") or s.get("doi_final") or doi_backfill.get(pid)
        fn=PDFDIR/f"{pid}__{slug(title)}.pdf"
        cands=list(s.get("oa_urls") or [])

        if doi:                                   # A. OpenAlex direct-by-DOI (unthrottled)
            u,_=oa_by_doi(doi); cands=u+cands
            up=unpaywall_pdf(doi)                 # B. Unpaywall
            if up: cands.insert(0,up)
        else:                                     # E/F. no-DOI: recover a DOI first
            s2pdf,s2doi=s2_pdf(None,title,year)
            if s2doi: doi=s2doi; doi_backfill[pid]=s2doi
            if s2pdf: cands.insert(0,s2pdf)
            if not doi:
                ou,od=oa_search(title,year)       # only fires if OA_KEY set
                if od: doi=od; doi_backfill[pid]=od
                cands=ou+cands
            if doi:
                u,_=oa_by_doi(doi); cands=u+cands
                up=unpaywall_pdf(doi)
                if up: cands.insert(0,up)

        if doi:                                   # C. S2 by DOI (real backoff)
            s2pdf,s2doi=s2_pdf(doi,title,year)
            if s2pdf: cands.append(s2pdf)
            if s2doi and pid not in doi_backfill and s2doi!=norm(x.get("doi")): doi_backfill.setdefault(pid,s2doi)

        expanded=[]                               # D. landing-page pdf extraction
        for u in cands:
            expanded.append(u)
            if not u.lower().endswith(".pdf"):
                lp=landing_pdf(u)
                if lp: expanded.append(lp)
        seen=[]; [seen.append(u) for u in expanded if u and u not in seen]

        got=next((u for u in seen if curl_pdf(u,fn)),None)
        if got:
            x["status"]="FETCHED"; x["file"]=fn.name; x["source_url"]=got; x["via"]="pass3"
            if pid not in doi_backfill and doi and doi!=norm(x.get("doi")): doi_backfill[pid]=doi
            recovered+=1
        print(f"  {i}/{len(residual)} {'OK ' if got else '.. '}(+{recovered}) {(title or '')[:48]}",file=sys.stderr)

    json.dump(manifest,open(SL/f"{SLUG}-pdf-manifest.json","w"),indent=2)
    json.dump(doi_backfill,open(bf_path,"w"),indent=2)

    cnt=Counter(x["status"] for x in manifest)
    still=[x for x in manifest if x["status"]=="NEEDS_MANUAL"]
    L=[f"# OAS meta-analysis — PDF want-list (RA institutional-proxy pull)\n",
       f"Auto-fetch recovered **{cnt['FETCHED']}/{len(manifest)}**; **{len(still)}** still need manual retrieval.  ",
       f"For each: open the DOI link via the UChicago proxy, else search the title in Google Scholar.\n",
       "| # | Title | Year | DOI / link | Tier | reason |","|--:|---|--:|---|:--:|---|"]
    for i,x in enumerate(still,1):
        d=x.get("doi") or doi_backfill.get(x["paperId"])
        link=f"[doi.org/{d}](https://doi.org/{d})" if d else f"[Scholar](https://scholar.google.com/scholar?q={urllib.parse.quote((x['title'] or '')[:120])})"
        L.append(f"| {i} | {(x['title'] or '')[:70].replace('|','/')} | {studies.get(x['paperId'],{}).get('year') or ''} | {link} | T{x['tier']} | {x.get('reason','')} |")
    (OUT/f"{SLUG}-pdf-wantlist.md").write_text("\n".join(L)+"\n")

    print(f"\npass-3 recovered {recovered}; totals {dict(cnt)}; DOI backfilled {len(doi_backfill)}",file=sys.stderr)

if __name__=="__main__":
    main()
