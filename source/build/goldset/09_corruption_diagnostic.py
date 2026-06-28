#!/usr/bin/env python3
"""
Locate the corruption: classify every on-disk DOI in the strong-ID core by SOURCE
(phase1 keyword vs phase2 snowball) and test the shuffle-vs-hallucination hypothesis.
"""
import json, re, time, hashlib, urllib.parse, subprocess
from pathlib import Path
from collections import Counter, defaultdict
HERE=Path(__file__).parent
CACHE=HERE/"cache"; CACHE.mkdir(exist_ok=True)
PRIOR=Path("/Users/shravanhari/~/Anup RA/projects/fertility-review-causes/literature/search-logs/old-age-security-pension-crowdout-prioritized.json")
MAILTO="shravanh@uchicago.edu"
STOP={"the","a","an","of","and","in","on","for","from","to","its","by","new","is","with","evidence"}
def toks(t): return {w for w in re.sub(r"[^a-z0-9\s]"," ",(t or "").lower()).split() if w not in STOP}
def jacc(a,b):
    A,B=toks(a),toks(b); return len(A&B)/len(A|B) if (A|B) else 0.0
def cr_doi(doi):
    doi=doi.replace("https://doi.org/","").strip().lower()
    cf=CACHE/f"verifydoi_{hashlib.sha1(doi.encode()).hexdigest()[:16]}.json"
    if cf.exists(): return json.load(open(cf))
    url=f"https://api.crossref.org/works/{urllib.parse.quote(doi)}?mailto={MAILTO}"
    r=subprocess.run(["curl","-s","-w","\\n%{http_code}","--max-time","30","-A",f"fr/1.0 (mailto:{MAILTO})",url],capture_output=True,text=True)
    body,_,code=r.stdout.rpartition("\n"); data={"_http":code}
    if code=="200":
        try: data=json.loads(re.sub(r"[\x00-\x1f]"," ",body)); data["_http"]="200"
        except Exception: data={"_http":"PARSE_ERR"}
    json.dump(data,open(cf,"w")); time.sleep(1.0)
    return data

d=json.load(open(PRIOR)); papers=d["papers"]
core=[p for p in papers if p.get("evidenceType")==4 and p.get("identification")==3]
# full corpus DOI index for the shuffle test
all_dois={ (p.get("doi") or "").replace("https://doi.org/","").lower():p["title"] for p in papers if p.get("doi") }

by_src=defaultdict(Counter)
records=[]
for p in core:
    doi=(p.get("doi") or "").strip()
    src=p.get("source")
    if not doi:
        by_src[src]["NO_DOI"]+=1; continue
    m=cr_doi(doi)
    if m.get("_http")!="200":
        verdict="INVALID_404"
    else:
        crt=(m.get("message",{}).get("title") or [""])[0]
        verdict="CORRECT" if jacc(p["title"],crt)>=0.5 else "WRONG_PAPER"
    by_src[src][verdict]+=1
    records.append((src,verdict,doi,p["title"]))

print("=== DOI validity by source (record-level, strong-ID core) ===")
for src in sorted(by_src):
    c=by_src[src]; tot=sum(c.values()); haddoi=tot-c.get("NO_DOI",0)
    correct=c.get("CORRECT",0)
    print(f"  {src}: {dict(c)}  | of those with a DOI: {correct}/{haddoi} correct"+(f" ({100*correct//haddoi}%)" if haddoi else ""))

print("\n=== shuffle test: do WRONG_PAPER DOIs belong to OTHER corpus papers? ===")
for src,verdict,doi,title in records:
    if verdict=="WRONG_PAPER":
        m=cr_doi(doi); realt=(m.get("message",{}).get("title") or [""])[0]
        in_corpus = doi.lower() in all_dois
        print(f"  {doi}  attached to: '{title[:38]}'")
        print(f"        really is : '{realt[:50]}'  | this DOI elsewhere in corpus: {in_corpus}")
