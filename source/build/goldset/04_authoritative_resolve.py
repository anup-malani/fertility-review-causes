#!/usr/bin/env python3
"""
Tier-A gold set, step 1b (authoritative): the on-disk prioritized.json DOI field is
corrupted (invalid DOIs + valid-but-wrong DOIs). So re-resolve EVERY distinct study's DOI
by TITLE, authoritatively, treating the on-disk DOI only as an untrusted hint to audit.

Per study:
  1. OpenAlex title.search  -> best candidate by token Jaccard (guard >= 0.60)
  2. Crossref query.bibliographic fallback if OpenAlex misses
  3. authoritative_doi = matched work's DOI (may legitimately be None: real but DOI-less)
  4. audit on-disk DOI: VALID_MATCH / VALID_WRONG_PAPER / INVALID(404) / NONE
     using OpenAlex by-DOI existence + title compare.

Cached (cache/), polite (mailto), throttled. Output: tier_a_authoritative.json + report.
"""
import json, re, sys, time, hashlib, urllib.parse, subprocess
from pathlib import Path
from collections import Counter

HERE = Path(__file__).parent
SRC = HERE / "tier_a_empirical_clusters.json"   # pre-resolution distinct studies (35)
OUT = HERE / "tier_a_authoritative.json"
CACHE = HERE / "cache"; CACHE.mkdir(exist_ok=True)
MAILTO = "shravanh@uchicago.edu"
GUARD = 0.60
STOP = {"the","a","an","of","and","in","on","for","from","to","its","by","new"}

def toks(t):
    t = re.sub(r"[^a-z0-9\s]", " ", (t or "").lower())
    return {w for w in t.split() if w not in STOP}
def jacc(a, b):
    A, B = toks(a), toks(b)
    return len(A & B)/len(A | B) if (A | B) else 0.0

def _get(url, cache_key):
    cf = CACHE / f"{cache_key}.json"
    if cf.exists():
        return json.load(open(cf))
    r = subprocess.run(["curl","-s","-w","\\n%{http_code}","--max-time","30",
                        "-A", f"fertility-review/1.0 (mailto:{MAILTO})", url],
                       capture_output=True, text=True)
    body, _, code = r.stdout.rpartition("\n")
    data = {"_http": code, "_body": None}
    if code == "200":
        try:
            data = json.loads(body); data["_http"] = "200"
        except Exception:
            # tolerate stray control chars
            try: data = json.loads(re.sub(r"[\x00-\x1f]", " ", body)); data["_http"]="200"
            except Exception: data = {"_http":"PARSE_ERR"}
    json.dump(data, open(cf, "w")); time.sleep(1.2)
    return data

def oa_title(title):
    q = urllib.parse.quote(" ".join(title.split()[:14]))
    return _get(f"https://api.openalex.org/works?filter=title.search:{q}&per-page=5&mailto={MAILTO}",
                "oatitle_"+hashlib.sha1(title.encode()).hexdigest()[:16])
def cr_title(title):
    p = urllib.parse.urlencode({"query.bibliographic": title, "rows": 5, "mailto": MAILTO})
    return _get(f"https://api.crossref.org/works?{p}",
                "crt_"+hashlib.sha1(title.encode()).hexdigest()[:16])
def oa_doi(doi):
    doi = doi.replace("https://doi.org/","").strip()
    return _get(f"https://api.openalex.org/works/doi:{urllib.parse.quote(doi)}?mailto={MAILTO}",
                "oadoi_"+hashlib.sha1(doi.encode()).hexdigest()[:16])

def best_oa(title, results):
    best=None
    for r in results or []:
        sim=jacc(title, r.get("display_name") or "")
        if best is None or sim>best[0]: best=(sim,r)
    return best
def best_cr(title, items):
    best=None
    for it in items or []:
        sim=jacc(title, (it.get("title") or [""])[0])
        if best is None or sim>best[0]: best=(sim,it)
    return best

def audit_ondisk(study):
    doi = study.get("canonical_doi")
    if not doi: return {"ondisk_doi": None, "status": "NONE"}
    d = oa_doi(doi)
    if d.get("_http")!="200" or not d.get("id"):
        return {"ondisk_doi": doi, "status": "INVALID_404"}
    sim = jacc(study["canonical_title"], d.get("display_name") or "")
    return {"ondisk_doi": doi, "status": "VALID_MATCH" if sim>=GUARD else "VALID_WRONG_PAPER",
            "resolves_to": (d.get("display_name") or "")[:70], "similarity": round(sim,3)}

def main():
    studies = json.load(open(SRC))
    for s in studies:
        title = s["canonical_title"]
        # audit the untrusted on-disk DOI
        s["ondisk_audit"] = audit_ondisk(s)
        # authoritative resolution by title: OpenAlex first
        bo = best_oa(title, oa_title(title).get("results"))
        chosen=None
        if bo and bo[0]>=GUARD:
            r=bo[1]; chosen={"src":"openalex","doi":(r.get("doi") or None),
                             "matched":r.get("display_name"),"sim":round(bo[0],3),
                             "year":r.get("publication_year"),"oa_id":r.get("id")}
        if chosen is None:
            bc = best_cr(title, cr_title(title).get("message",{}).get("items"))
            if bc and bc[0]>=GUARD:
                it=bc[1]; chosen={"src":"crossref","doi":(it.get("DOI") or None),
                                  "matched":(it.get("title") or [""])[0],"sim":round(bc[0],3),
                                  "year":(it.get("issued",{}).get("date-parts",[[None]])[0][0])}
        if chosen:
            doi = (chosen["doi"] or "").replace("https://doi.org/","") or None
            s["authoritative_doi"]=doi
            s["authoritative"]={**chosen,"doi":doi}
        else:
            s["authoritative_doi"]=None
            s["authoritative"]={"src":"UNRESOLVED"}
    json.dump(studies, open(OUT,"w"), indent=2)

    aud = Counter(s["ondisk_audit"]["status"] for s in studies)
    res = Counter(s["authoritative"]["src"] for s in studies)
    have = sum(1 for s in studies if s["authoritative_doi"])
    print("=== on-disk DOI audit (corruption) ===", file=sys.stderr)
    for k,v in aud.most_common(): print(f"  {k}: {v}", file=sys.stderr)
    print("\n=== authoritative resolution source ===", file=sys.stderr)
    for k,v in res.most_common(): print(f"  {k}: {v}", file=sys.stderr)
    print(f"\nstudies with authoritative DOI: {have}/{len(studies)}", file=sys.stderr)

    print("\n=== on-disk DOIs that were VALID but WRONG PAPER ===", file=sys.stderr)
    for s in studies:
        if s["ondisk_audit"]["status"]=="VALID_WRONG_PAPER":
            print(f"  {s['ondisk_audit']['ondisk_doi']}  ours='{s['canonical_title'][:45]}'", file=sys.stderr)
            print(f"        actually -> {s['ondisk_audit']['resolves_to']}", file=sys.stderr)
    print("\n=== still UNRESOLVED (no authoritative DOI by title) ===", file=sys.stderr)
    for s in studies:
        if not s["authoritative_doi"]:
            print(f"  [{s['year']}] {s['canonical_title'][:70]}  (src={s['authoritative']['src']})", file=sys.stderr)
    print(f"\nwritten -> {OUT}", file=sys.stderr)

if __name__=="__main__":
    main()
