#!/usr/bin/env python3
"""
Apply the corpus-wide W-ID DOI recovery to the 35 gold studies: for each study, take the
title-verified recovered DOI from its member W-ID(s); merge with the 14 already agent+verified.
Report final gold-set DOI coverage and which of the 21 manual residuals are now recovered.
Plus: corruption-changed-by-source over the full corpus (confirm it's phase2).
"""
import json
from pathlib import Path
from collections import Counter, defaultdict
HERE=Path(__file__).parent
corr={r["paperId"]:r for r in json.load(open(HERE/"prioritized_doi_corrected.json"))}
final=json.load(open(HERE/"tier_a_resolved_final.json"))         # has member_wids
verified={r["id"]:r for r in json.load(open(HERE/"tier_a_verified_final.json"))}  # agent+verifier
inp={s["id"]:s for s in json.load(open(HERE/"resolver_input.json"))}

# id17 override (Billari-Galasso) already accepted earlier
agent_verified_ids={i for i,r in verified.items() if r["verdict"]=="VERIFIED"} | {17}

# DOIs already claimed by an agent-verified study (reject W-ID-collision false recoveries)
claimed={verified[i].get("final_doi") for i in agent_verified_ids if verified.get(i,{}).get("final_doi")}
rows=[]
for s in final:
    sid=[k for k,v in inp.items() if v["title"]==s["canonical_title"]]
    sid=sid[0] if sid else None
    wid_doi=None; wid_used=None
    for w in s.get("member_wids",[]):
        c=corr.get(w)
        if c and c.get("status")=="RECOVERED_DOI" and c.get("corrected_doi"):
            cand=c["corrected_doi"]
            if cand in claimed:        # shared/collided W-ID -> would duplicate another study
                wid_used=f"{w}:COLLISION({cand})"; continue
            wid_doi=cand; wid_used=w; claimed.add(cand); break
    rows.append({"id":sid,"title":s["canonical_title"],"year":s.get("year"),
                 "wid_recovered_doi":wid_doi,"wid_used":wid_used,
                 "agent_verified": sid in agent_verified_ids})

have_now=[r for r in rows if r["wid_recovered_doi"] or r["agent_verified"]]
newly=[r for r in rows if r["wid_recovered_doi"] and not r["agent_verified"]]
still=[r for r in rows if not r["wid_recovered_doi"] and not r["agent_verified"]]

print(f"GOLD-SET DOI coverage now: {len(have_now)}/35")
print(f"  agent+verifier: {len(agent_verified_ids & {r['id'] for r in rows})}")
print(f"  NEWLY recovered by W-ID re-fetch (were in the 21 residual): {len(newly)}")
for r in sorted(newly,key=lambda x:x['id'] or 0):
    print(f"     id{r['id']:2} {r['wid_recovered_doi']:32} {r['title'][:46]}")
print(f"  STILL unresolved: {len(still)}")
for r in sorted(still,key=lambda x:x['id'] or 0):
    st=corr.get(r['wid_used'] or '',{}).get('status')
    # show member-wid statuses
    s=[x for x in final if x['canonical_title']==r['title']][0]
    sts=[corr.get(w,{}).get('status','?') for w in s.get('member_wids',[])] or ['NO_WID']
    print(f"     id{r['id']:2} {r['title'][:50]}  wid-status={sts}")

# corruption-changed by source (full corpus)
bysrc=defaultdict(Counter)
for r in corr.values():
    if r.get("ondisk_doi") and r.get("status")=="RECOVERED_DOI":
        bysrc[r["source"]]["changed" if r["ondisk_doi"]!=r["corrected_doi"] else "same"]+=1
print("\n=== on-disk DOI corrected vs matched, by source (full corpus, checkable subset) ===")
for src in sorted(bysrc):
    c=bysrc[src]; tot=c["changed"]+c["same"]
    print(f"  {src}: {c['changed']} corrected / {tot} checkable ({100*c['changed']//tot if tot else 0}% wrong)")
json.dump(rows, open(HERE/"goldset_doi_coverage.json","w"), indent=2)
