#!/usr/bin/env python3
"""
Part 1c (assembly) — merge the empirical core + the canon/theory + anchor seed into one
stratified Tier-A draft, and tally against the 60-floor / 80-100 target. NOT frozen as the
validation core until RA sign-off (method spec §7: never let a co-evolving set inflate recall).

Strata (spec §3, for representativeness not per-stratum estimates):
  theory-foundational | theory-formal | empirical-classic | empirical-modern
Empirical-modern items also carry a (setting, era) tag for coverage auditing.

Inputs : tier-a-verified.json (15) + canon_resolved.json (40) + id28 title-key (Ghana)
Outputs: tier_a_draft.json + ../literature/search-logs/old-age-security-pension-crowdout-tier-a-stratified-draft.md
"""
import json
from pathlib import Path
from collections import Counter, defaultdict
HERE=Path(__file__).parent
LOGS=Path("/Users/shravanhari/~/Anup RA/projects/fertility-review-causes/literature/search-logs")

# empirical-core (setting, era) map by id (modern natural-experiment / micro studies)
EMP={1:("Germany","SDT"),2:("South Africa","SDT"),7:("Europe","SDT"),8:("China","SDT"),
     9:("China","SDT"),12:("China","SDT"),13:("Europe","SDT"),14:("Germany","FDT"),
     17:("Italy","SDT"),18:("Namibia","SDT"),23:("Bangladesh","SDT"),24:("cross-country","SDT"),
     25:("Europe","SDT"),29:("cross-country","SDT"),34:("China","SDT")}

gold=[]
# 1) empirical verified core
for r in json.load(open(LOGS/"old-age-security-pension-crowdout-tier-a-verified.json")):
    setting,era=EMP.get(r["id"],("?","SDT"))
    gold.append({"gold_id":f"E{r['id']}","title":r["registered_title"],"doi":r["canonical_doi"],
                 "keytype":"DOI","provenance":"empirical","stratum":"empirical-modern",
                 "setting":setting,"era":era,"year":r.get("year"),
                 "is_working_paper":r.get("is_working_paper",False)})
# 2) empirical title-key residual we keep (id28 Ghana, real WP no DOI)
gold.append({"gold_id":"E28","title":"Pension Policy Reform and Fertility: Micro Evidence from Ghana",
             "doi":None,"keytype":"title-key","provenance":"empirical","stratum":"empirical-modern",
             "setting":"Ghana","era":"SDT","year":2024,"is_working_paper":True})
# 3) canon / theory / anchor
for i,r in enumerate(json.load(open(LOGS/"old-age-security-pension-crowdout-canon-resolved.json"))):
    gold.append({"gold_id":f"C{i}","title":r["title"],"doi":r.get("final_doi"),
                 "keytype":"DOI" if r["verdict"]=="VERIFIED" else "title-key",
                 "provenance":"canon","stratum":r["stratum"],
                 "setting":None,"era":None,"year":r["year"],
                 "authors":r.get("authors"),"is_working_paper":False})

json.dump(gold,open(LOGS/"old-age-security-pension-crowdout-tier-a-draft.json","w"),indent=2)

# ---- tally ----
by_strat=Counter(g["stratum"] for g in gold)
by_key=Counter(g["keytype"] for g in gold)
doi_n=by_key["DOI"]; tk_n=by_key["title-key"]; usable=len(gold)
settings=Counter(g["setting"] for g in gold if g["provenance"]=="empirical")
eras=Counter(g["era"] for g in gold if g["provenance"]=="empirical")

L=["# Tier A — stratified draft (Part 1c assembled)  ·  2026-06-29","",
 "**Status: DRAFT, not frozen.** Validation core is frozen only on RA sign-off (spec §7). The "
 "15 hard residuals (real empirical, DOI unresolved) are NOT in this count — they enter a "
 "*development pool* and graduate into Tier A as human resolution lands.","",
 f"## Headline","",
 f"- **Usable now (DOI + title-key): {usable}**  (DOI-resolved powered set: {doi_n}; title-keyed: {tk_n})",
 f"- Floor = 60, target = 80-100.  +{max(0,60-usable)} to floor; the 15 residuals + a little more canon clear it.",
 f"- Total real distinct studies in scope (incl. pending residuals): **{usable+15}**.","",
 "## By stratum",""]
for s in ["theory-foundational","theory-formal","empirical-classic","empirical-modern"]:
    rows=[g for g in gold if g["stratum"]==s]
    d=sum(1 for g in rows if g["keytype"]=="DOI"); t=len(rows)-d
    L.append(f"- **{s}**: {len(rows)}  (DOI {d}, title-key {t})")
L+=["", "## Empirical-modern coverage (representativeness audit)","",
 f"- settings: "+", ".join(f"{k} {v}" for k,v in settings.most_common()),
 f"- eras: "+", ".join(f"{k} {v}" for k,v in eras.most_common())+"  (FDT anchor = id14 Bismarck; classics add LDC/US era tests)","",
 "## Provenance split","",
 f"- empirical (on-disk core + Ghana TK): {sum(1 for g in gold if g['provenance']=='empirical')}",
 f"- canon / theory / anchor (Part 1c): {sum(1 for g in gold if g['provenance']=='canon')}","",
 "Artifacts (all in `literature/search-logs/`): `*-tier-a-draft.json`, `*-canon-resolved.json`, "
 "`*-tier-a-verified.json`."]
(LOGS/"old-age-security-pension-crowdout-tier-a-stratified-draft.md").write_text("\n".join(L)+"\n")

print(f"Tier A draft assembled: {usable} usable ({doi_n} DOI + {tk_n} title-key)")
print("by stratum:",dict(by_strat))
print("empirical settings:",dict(settings))
print("empirical eras:",dict(eras))
print(f"floor gap: {max(0,60-usable)}; total incl. residuals: {usable+15}")
print("written -> *-tier-a-draft.json, *-tier-a-stratified-draft.md")
