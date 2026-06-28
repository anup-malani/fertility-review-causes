#!/usr/bin/env python3
"""
Reusable resolver, part 2 (deterministic disposer): independently verify every DOI the
agent fleet returned. We do NOT trust the agents' self-reported confidence; we re-resolve
each DOI via Crossref and accept only if title (Jaccard >= 0.50, allowing subtitle drift)
AND year (|delta| <= 3, working-paper vs published) corroborate. doi.org existence is a
secondary signal (publisher HEAD blocks 403 on some valid DOIs, so Crossref-200 is primary).

Inputs : resolver_input.json (the 35 studies) + resolver_agent_{1..5}.json (agent candidates)
Output : tier_a_verified_final.json + manual handoff list to stderr.
Verdict per study: VERIFIED | REJECTED(reason) | NOT_FOUND(agent) | NO_DOI(working-paper)
"""
import json, re, sys, time, hashlib, urllib.parse, subprocess
from pathlib import Path
from collections import Counter

HERE = Path(__file__).parent
CACHE = HERE / "cache"; CACHE.mkdir(exist_ok=True)
MAILTO = "shravanh@uchicago.edu"
GUARD = 0.50
STOP = {"the","a","an","of","and","in","on","for","from","to","its","by","new","is","with","evidence"}

def toks(t):
    t=re.sub(r"[^a-z0-9\s]"," ",(t or "").lower())
    return {w for w in t.split() if w not in STOP}
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

def main():
    studies={s["id"]:s for s in json.load(open(HERE/"resolver_input.json"))}
    agent={}
    for n in range(1,6):
        f=HERE/f"resolver_agent_{n}.json"
        if f.exists():
            for r in json.load(open(f)): agent[r["id"]]=r

    results=[]
    for sid,s in sorted(studies.items()):
        a=agent.get(sid,{})
        rec={"id":sid,"title":s["title"],"year_hint":s["year_hint"],
             "agent_found":a.get("found"),"agent_doi":a.get("doi"),
             "agent_conf":a.get("confidence"),"agent_notes":a.get("notes"),
             "is_working_paper":a.get("is_working_paper"),"alt_dois":a.get("alt_dois",[])}
        if not a.get("found") or not a.get("doi"):
            rec["verdict"]="NOT_FOUND"; rec["final_doi"]=None
            results.append(rec); continue
        d=cr_doi(a["doi"])
        if d.get("_http")!="200":
            rec["verdict"]="REJECTED"; rec["reason"]=f"crossref {d.get('_http')}"; rec["final_doi"]=None
            results.append(rec); continue
        m=d.get("message",{})
        crt=(m.get("title") or [""])[0]
        cry=(m.get("issued",{}).get("date-parts",[[None]])[0][0]) or m.get("published",{}).get("date-parts",[[None]])[0][0]
        sim=jacc(s["title"],crt)
        yr_ok = (s["year_hint"] is None or cry is None or abs((cry or 0)-(s["year_hint"] or 0))<=3)
        rec.update({"crossref_title":crt,"crossref_year":cry,"title_jaccard":round(sim,3)})
        if sim>=GUARD and yr_ok:
            rec["verdict"]="VERIFIED"; rec["final_doi"]=a["doi"].lower()
        else:
            rec["verdict"]="REJECTED"
            rec["reason"]=f"jaccard {sim:.2f}{'' if sim>=GUARD else ' <guard'}; year {cry} vs {s['year_hint']}{'' if yr_ok else ' MISMATCH'}"
            rec["final_doi"]=None
        results.append(rec)

    json.dump(results, open(HERE/"tier_a_verified_final.json","w"), indent=2)
    c=Counter(r["verdict"] for r in results)
    print("=== deterministic verifier verdicts ===", file=sys.stderr)
    for k,v in c.most_common(): print(f"  {k}: {v}", file=sys.stderr)
    print(f"\nVERIFIED (into frozen Tier A): {c['VERIFIED']}/{len(results)}", file=sys.stderr)

    print("\n=== MANUAL HANDOFF (NOT_FOUND / REJECTED) ===", file=sys.stderr)
    for r in results:
        if r["verdict"] in ("NOT_FOUND","REJECTED"):
            extra = r.get('reason','') or (r.get('agent_notes','') or '')[:70]
            print(f"  id{r['id']:2} [{r['year_hint']}] {r['title'][:54]}", file=sys.stderr)
            print(f"        {r['verdict']}: {extra}", file=sys.stderr)
    print(f"\nwritten -> tier_a_verified_final.json", file=sys.stderr)

if __name__=="__main__":
    main()
