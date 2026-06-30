#!/usr/bin/env python3
"""
Residual-retry verifier (deterministic disposer for the 2026-06-29 agent fleet). Mirrors
07_verify_agent_dois.py: re-resolve every agent-proposed DOI via Crossref and accept only if
title Jaccard >= 0.50 AND |year delta| <= 3. Agent confidence is NOT trusted.

Working-paper nuance: SSRN/NBER/RePEc DOIs are often absent from Crossref. A Crossref miss on
such a DOI is NOT a rejection -- it is marked WP_UNVERIFIED (Crossref can't see it), to be
adjudicated by the RA on the agent's SSRN-page evidence, never silently folded.

Inputs : retry_input.json + resolver_agent_retry_{1..4}.json
Output : retry_verified_final.json (+ stderr summary)
Verdicts: VERIFIED | REJECTED(reason) | NOT_FOUND(agent) | WP_UNVERIFIED(working-paper, crossref-absent)
"""
import json, re, sys, time, hashlib, urllib.parse, subprocess
from pathlib import Path
from collections import Counter

HERE=Path(__file__).parent; CACHE=HERE/"cache"; CACHE.mkdir(exist_ok=True)
MAILTO="shravanh@uchicago.edu"; GUARD=0.50
STOP={"the","a","an","of","and","in","on","for","from","to","its","by","new","is","with","evidence"}
def toks(t):
    return {w for w in re.sub(r"[^a-z0-9\s]"," ",(t or "").lower()).split() if w not in STOP}
def jacc(a,b):
    A,B=toks(a),toks(b); return len(A&B)/len(A|B) if (A|B) else 0.0
def cr_doi(doi):
    doi=doi.replace("https://doi.org/","").strip().lower()
    cf=CACHE/f"verifydoi_{hashlib.sha1(doi.encode()).hexdigest()[:16]}.json"
    if cf.exists(): return json.load(open(cf))
    url=f"https://api.crossref.org/works/{urllib.parse.quote(doi)}?mailto={MAILTO}"
    r=subprocess.run(["curl","-s","-w","\\n%{http_code}","--max-time","30",
                      "-A",f"fertility-review/1.0 (mailto:{MAILTO})",url],capture_output=True,text=True)
    body,_,code=r.stdout.rpartition("\n"); data={"_http":code}
    if code=="200":
        try: data=json.loads(re.sub(r"[\x00-\x1f]"," ",body)); data["_http"]="200"
        except Exception: data={"_http":"PARSE_ERR"}
    json.dump(data,open(cf,"w")); time.sleep(1.0)
    return data
def is_wp_doi(doi):
    d=(doi or "").lower()
    return d.startswith("10.2139/ssrn") or d.startswith("10.3386/") or "/repec" in d or "iza" in d

def main():
    studies={s["id"]:s for s in json.load(open(HERE/"retry_input.json"))}
    agent={}
    for n in range(1,5):
        f=HERE/f"resolver_agent_retry_{n}.json"
        if f.exists():
            for r in json.load(open(f)): agent[r["id"]]=r
        else: print(f"  (missing {f.name})",file=sys.stderr)

    results=[]
    for sid,s in sorted(studies.items()):
        a=agent.get(sid,{})
        rec={"id":sid,"category":s["category"],"title":s["title"],"year":s.get("year"),
             "agent_found":a.get("found"),"agent_doi":a.get("doi"),"agent_conf":a.get("confidence"),
             "agent_wp":a.get("is_working_paper"),"agent_notes":a.get("notes"),"alt_dois":a.get("alt_dois",[])}
        cand=a.get("doi")
        if not a.get("found") or not cand:
            rec["verdict"]="NOT_FOUND"; rec["final_doi"]=None; results.append(rec); continue
        d=cr_doi(cand)
        if d.get("_http")!="200":
            if is_wp_doi(cand) or a.get("is_working_paper"):
                rec["verdict"]="WP_UNVERIFIED"; rec["final_doi"]=None
                rec["reason"]=f"crossref {d.get('_http')} (working-paper DOI; check agent evidence)"
            else:
                rec["verdict"]="REJECTED"; rec["final_doi"]=None; rec["reason"]=f"crossref {d.get('_http')}"
            results.append(rec); continue
        m=d.get("message",{}); crt=(m.get("title") or [""])[0]
        cry=(m.get("issued",{}).get("date-parts",[[None]])[0][0]) or \
            (m.get("published",{}).get("date-parts",[[None]])[0][0])
        sim=jacc(s["title"],crt)
        yr=s.get("year"); yr_ok=(yr is None or cry is None or abs((cry or 0)-(yr or 0))<=3)
        rec.update({"crossref_title":crt,"crossref_year":cry,"title_jaccard":round(sim,3)})
        if sim>=GUARD and yr_ok:
            rec["verdict"]="VERIFIED"; rec["final_doi"]=cand.lower()
        else:
            rec["verdict"]="REJECTED"; rec["final_doi"]=None
            rec["reason"]=f"jaccard {sim:.2f}{'' if sim>=GUARD else ' <guard'}; year {cry} vs {yr}{'' if yr_ok else ' MISMATCH'}"
        results.append(rec)

    json.dump(results,open(HERE/"retry_verified_final.json","w"),indent=2)
    c=Counter(r["verdict"] for r in results)
    print("=== retry verifier verdicts ===",file=sys.stderr)
    for k,v in c.most_common(): print(f"  {k}: {v}",file=sys.stderr)
    print(f"\nNEWLY VERIFIED (Crossref-confirmed): {c['VERIFIED']}/{len(results)}",file=sys.stderr)
    for r in results:
        if r["verdict"]=="VERIFIED":
            print(f"  id{r['id']:>2} J={r['title_jaccard']}  {r['final_doi']}  ({r['crossref_year']})",file=sys.stderr)
            print(f"        {r['crossref_title'][:72]}",file=sys.stderr)
    print(f"\nWP_UNVERIFIED (RA adjudicates on agent evidence):",file=sys.stderr)
    for r in results:
        if r["verdict"]=="WP_UNVERIFIED":
            print(f"  id{r['id']:>2} agent_doi={r['agent_doi']} conf={r['agent_conf']}  {r['title'][:50]}",file=sys.stderr)
    print(f"\nstill NOT_FOUND / REJECTED:",file=sys.stderr)
    for r in results:
        if r["verdict"] in ("NOT_FOUND","REJECTED"):
            print(f"  id{r['id']:>2} [{r['verdict']}] {r.get('reason','no agent DOI')}  | {r['title'][:46]}",file=sys.stderr)
    print(f"\nwritten -> retry_verified_final.json",file=sys.stderr)

if __name__=="__main__":
    main()
