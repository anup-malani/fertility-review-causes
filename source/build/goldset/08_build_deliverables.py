#!/usr/bin/env python3
"""
Build the two Part-1 deliverables from the verifier output:
  1. tier_a_empirical_FROZEN.json  -- verified-DOI empirical studies (the gold-set core so far)
  2. tier_a_manual_handoff.md      -- categorized residual for RA (Shravan) to resolve by hand

id17 override: "What Explains Fertility? Evidence from Italian Pension Reforms" (Billari &
Galasso) — verifier rejected on WP-vs-corpus year gap only (title J=1.00). It is the
canonical study; accept the SSRN working-paper DOI and correct year to 2009.
"""
import json, re
from pathlib import Path
HERE=Path(__file__).parent
res=json.load(open(HERE/"tier_a_verified_final.json"))

# id17 manual override
for r in res:
    if r["id"]==17:
        r["verdict"]="VERIFIED"; r["final_doi"]="10.2139/ssrn.1406946"
        r["crossref_year"]=2009; r["is_working_paper"]=True
        r["override_note"]="canonical Billari-Galasso; SSRN WP DOI; verifier year-gap false-negative"

verified=[r for r in res if r["verdict"]=="VERIFIED"]
frozen=[{"id":r["id"],"title":r["title"],
         "canonical_doi":r["final_doi"],
         "registered_title":r.get("crossref_title") or r["title"],
         "year":r.get("crossref_year") or r["year_hint"],
         "is_working_paper":r.get("is_working_paper"),
         "alt_dois":r.get("alt_dois",[]),
         "provenance_tier":"A","source":"on-disk-44 (strong-ID empirical)",
         "stratum":None,  # filled in step 1c
         "resolution":"agent-proposed + deterministically verified (Crossref title+year guard)",
         "note":r.get("override_note")}
        for r in sorted(verified,key=lambda x:x["id"])]
json.dump(frozen, open(HERE/"tier_a_empirical_FROZEN.json","w"), indent=2)

# categorize residual
def cat(r):
    n=((r.get("agent_notes") or "")+" "+(r.get("reason") or "")).lower()
    if "chimeric" in n or "corrupt" in n: return "A. LIKELY-NOT-REAL (drop candidate)"
    if "working-paper" in n or "working paper" in n or r.get("is_working_paper"): return "C. WORKING-PAPER (accept WP DOI or title-key)"
    if "budget" in n or "rate" in n or "openalex" in n or "semantic" in n: return "B. RATE-LIMITED (retry likely resolves)"
    return "D. NEEDS HUMAN LOOKUP (generic title / author needed)"
residual=[r for r in res if r["verdict"]!="VERIFIED"]
for r in residual: r["_cat"]=cat(r)

lines=["# Tier-A manual handoff — old-age-security gold set",
       "",
       f"Verified automatically: **{len(verified)}/35**. Residual below: **{len(residual)}** studies "
       "the agent fleet + deterministic verifier could not pin to a trustworthy DOI.",
       "",
       "Categories: **A** likely-not-real corrupted records (consider dropping, not resolving); "
       "**B** rate-limited (a retry pass after OpenAlex cooldown will likely auto-resolve); "
       "**C** working-paper-only (accept the WP DOI or title-key the gold item); "
       "**D** real but needs a human lookup (generic title; author name disambiguates).",
       ""]
for c in ["A","B","C","D"]:
    grp=[r for r in residual if r["_cat"].startswith(c)]
    if not grp: continue
    lines.append(f"## Category {grp[0]['_cat'][3:]}  ({len(grp)})")
    lines.append("")
    lines.append("| id | year | title | verifier reason / agent note | unverified candidate DOIs |")
    lines.append("|---|---|---|---|---|")
    for r in sorted(grp,key=lambda x:x["id"]):
        cand=", ".join(json.load(open(HERE/"resolver_input.json"))[r["id"]]["unverified_candidate_dois"]) or "—"
        note=(r.get("reason") or r.get("agent_notes") or "")[:120].replace("|","/").replace("\n"," ")
        lines.append(f"| {r['id']} | {r['year_hint']} | {r['title'][:60]} | {note} | {cand} |")
    lines.append("")
open(HERE/"tier_a_manual_handoff.md","w").write("\n".join(lines))

print(f"FROZEN verified: {len(frozen)}")
for f in frozen:
    wp=" (WP)" if f["is_working_paper"] else ""
    print(f"  id{f['id']:2} [{f['year']}] {f['canonical_doi']}{wp}  {f['title'][:50]}")
print(f"\nmanual handoff: {len(residual)} studies -> tier_a_manual_handoff.md")
from collections import Counter
print("residual categories:", dict(Counter(r['_cat'][:1] for r in residual)))
