#!/usr/bin/env python3
"""
Instantiate the gold-anchored method's 3 OUTPUT tiers on the EXISTING screened corpus
(demonstration; the production keyword query has not run yet).

Signals per paper:
  G = in the gold-anchor set (the 14 verified strong-ID studies; matched by on-disk paperId)
  K = keyword channel  = paperId in screened.json (PI keyword pull) OR sequential-screened.json
  S = snowball channel = paperId in snowball.json
  V = final two-stage screen verdict + confidence (prefer master screened.json)

Tiers:
  Tier 1 (Core)            : G  OR  (V=RELEVANT & conf=HIGH & multi-channel[K&S])
  Tier 2 (Confirmed single): V=RELEVANT & not Tier1                 (single-channel, or RELEVANT-MED)
  Tier 3 (Recall net)      : V=UNCERTAIN  OR  (V=NOT_RELEVANT & conf=LOW)
  (excluded)               : V=NOT_RELEVANT & conf in {HIGH,MEDIUM}
Secondary sort within tiers: Anup compositeScore (where available) then channel-count.
"""
import json, sys
from pathlib import Path
from collections import Counter
LOG=Path("/Users/shravanhari/~/Anup RA/projects/fertility-review-causes/literature/search-logs")
HERE=Path(__file__).parent
def arr(p):
    d=json.load(open(p)); return d["papers"] if isinstance(d,dict) and "papers" in d else d

screened=arr(LOG/"old-age-security-pension-crowdout-screened.json")
seq=arr(LOG/"old-age-security-pension-crowdout-sequential-screened.json")
snow=arr(LOG/"old-age-security-pension-crowdout-snowball.json")
prioritized=arr(LOG/"old-age-security-pension-crowdout-prioritized.json")

Kids=set(p["paperId"] for p in screened)|set(p["paperId"] for p in seq)   # keyword channel
Sids=set(p["paperId"] for p in snow)                                       # snowball channel
comp={p["paperId"]:p.get("compositeScore") for p in prioritized}           # Anup score (RELEVANT set)

# gold-anchor paperIds: member_wids of the 14 verified studies
final=json.load(open(HERE/"tier_a_resolved_final.json"))
verified=json.load(open(HERE/"tier_a_verified_final.json"))
import json as _j
vids={r["id"] for r in verified if r["verdict"]=="VERIFIED"}|{17}
inp={s["id"]:s["title"] for s in _j.load(open(HERE/"resolver_input.json"))}
vtitles={inp[i] for i in vids if i in inp}
G=set()
for s in final:
    if s["canonical_title"] in vtitles:
        G|=set(s.get("member_wids",[]))

# master verdict map (prefer screened.json, then seq, then snow)
V={}
for src in (snow, seq, screened):   # later overrides earlier -> screened wins
    for p in src:
        V[p["paperId"]]={"title":p.get("title"),"verdict":p.get("llm_verdict"),
                         "conf":p.get("llm_confidence")}

universe=Kids|Sids
def tier(pid):
    info=V.get(pid,{}); v=info.get("verdict"); c=info.get("conf")
    k=pid in Kids; s=pid in Sids; multi=k and s
    if pid in G: return 1,"gold-anchor",k,s
    if v=="RELEVANT" and c=="HIGH" and multi: return 1,"multi-channel RELEVANT-HIGH",k,s
    if v=="RELEVANT": return 2,("multi-channel RELEVANT-MED" if multi else "single-channel RELEVANT"),k,s
    if v=="UNCERTAIN": return 3,"uncertain",k,s
    if v=="NOT_RELEVANT" and c=="LOW": return 3,"low-conf NOT_RELEVANT",k,s
    return 0,"excluded (NOT_RELEVANT hi/med)",k,s

rows=[]
for pid in universe:
    t,reason,k,s=tier(pid)
    info=V.get(pid,{})
    rows.append({"paperId":pid,"tier":t,"reason":reason,"verdict":info.get("verdict"),
                 "confidence":info.get("conf"),"channel":("K&S" if (k and s) else ("K" if k else "S")),
                 "compositeScore":comp.get(pid),"in_gold":pid in G,"title":info.get("title")})
# sort: tier asc, then compositeScore desc, then channel-count
rows.sort(key=lambda r:(r["tier"] if r["tier"]>0 else 9, -(r["compositeScore"] or -1),
                        0 if r["channel"]=="K&S" else 1))
json.dump(rows, open(HERE/"tiers_instantiated.json","w"), indent=2)

tc=Counter(r["tier"] for r in rows)
print(f"UNIVERSE (all screened, deduped by paperId): {len(rows)}")
print(f"  keyword K: {len(Kids&universe)}  snowball S: {len(Sids)}  multi-channel K&S: {len(Kids&Sids)}  gold G: {len(G&universe)}/{len(G)}")
print(f"\n=== 3 OUTPUT TIERS ===")
for t,label in [(1,'Tier 1 Core'),(2,'Tier 2 Confirmed single-channel'),(3,'Tier 3 Recall net'),(0,'excluded')]:
    grp=[r for r in rows if r["tier"]==t]
    print(f"  {label}: {len(grp)}")
    if t in (1,2,3):
        sub=Counter(r["reason"] for r in grp)
        for k,v in sub.most_common(): print(f"        - {k}: {v}")
# channel composition of Tier 1 & 2 (the union story)
print("\nTier 1 channel mix:", dict(Counter(r["channel"] for r in rows if r["tier"]==1)))
print("Tier 2 channel mix:", dict(Counter(r["channel"] for r in rows if r["tier"]==2)))
print("\nTop of Tier 1 (by compositeScore):")
for r in [r for r in rows if r["tier"]==1][:8]:
    print(f"  cs={r['compositeScore']} [{r['channel']}] {r['reason'][:22]:22} {(r['title'] or '')[:48]}")
