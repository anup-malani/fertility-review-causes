#!/usr/bin/env python3
"""
Apply the 2026-06-29 residual-retry outcomes to the Tier-A gold set.

Disposition (after deterministic Crossref pass #13, agent fleet, verifier #14):
  ACCEPT  id1  -> verifier false-negative; Crossref-confirmed Fenge & Scheubel 2016
                  (corpus title is a corrupted paraphrase, J=0.40 < guard). Manual accept.
  DROP    id15,16,20 -> category A: agents confirmed no real paper exists (corrupted/chimeric).
  DROP    id19 -> duplicate of id18 (both -> Rossi & Godard 10.1257/pol.20200466).
  TITLEKEY id28 -> real working paper (Zelu/Iranzo/Perez-Laborda, Ghana, IZA-BREAD 2023) but
                   no DOI exists anywhere -> keep as a title-keyed gold item.
  RESIDUAL (15) -> genuinely unresolvable now; candidate DOIs confirmed wrong/fabricated/
                   unregistered. A true recall ceiling, not an API/rate-limit artifact.

Outputs (committed deliverables in literature/search-logs/):
  - old-age-security-pension-crowdout-tier-a-verified.json   (14 -> 15, id1 added)
  - old-age-security-pension-crowdout-tier-a-retry-disposition.md  (full audit of the 21)
"""
import json
from pathlib import Path
HERE=Path(__file__).parent
LOGS=Path("/Users/shravanhari/~/Anup RA/projects/fertility-review-causes/literature/search-logs")
VERIFIED=LOGS/"old-age-security-pension-crowdout-tier-a-verified.json"

retry={r["id"]:r for r in json.load(open(HERE/"retry_verified_final.json"))}
agents={}
for n in range(1,5):
    f=HERE/f"resolver_agent_retry_{n}.json"
    if f.exists():
        for r in json.load(open(f)): agents[r["id"]]=r

DROP={15:"category A: no real paper (corrupted record); candidates 404/unrelated",
      16:"category A: chimeric variant of id18 (Rossi & Godard Namibia); candidate 404",
      19:"duplicate of id18 -> Rossi & Godard 10.1257/pol.20200466",
      20:"category A: no real paper (corrupted record); candidate 404"}
TITLEKEY={28:"real WP, no DOI exists (Zelu/Iranzo/Perez-Laborda, Ghana, IZA-BREAD 2023)"}
ACCEPT_ID1={
  "id":1,"canonical_doi":"10.1007/s00148-016-0608-x","alt_dois":[],
  "is_working_paper":False,
  "registered_title":"Pensions and fertility: back to the roots",
  "title":"Pensions and Fertility: Evidence from Germany","year":2016,
  "provenance_tier":"A","stratum":None,"source":"on-disk-44 (strong-ID empirical)",
  "resolution":"agent-proposed + RA manual-accept (Crossref-confirmed Fenge & Scheubel, "
               "J Pop Econ 2016). Verifier title-guard FN: J=0.40 vs corrupted corpus title.",
  "note":"verifier FN; real title 'Pensions and fertility: back to the roots' (Fenge & Scheubel)"}

# 1) fold id1 into verified core (idempotent)
core=json.load(open(VERIFIED))
if not any(r["id"]==1 for r in core):
    core.append(ACCEPT_ID1)
    core.sort(key=lambda r:r["id"])
    json.dump(core,open(VERIFIED,"w"),indent=2)
print(f"verified core now: {len(core)} studies (id1 {'added' if any(r['id']==1 for r in core) else 'MISSING'})")

# 2) disposition table
ALL=[r["id"] for r in json.load(open(HERE/"retry_input.json"))]
def disp(i):
    if i==1: return "ACCEPT (verified)","manual-accept; "+ACCEPT_ID1["note"]
    if i in DROP: return "DROP",DROP[i]
    if i in TITLEKEY: return "TITLE-KEY",TITLEKEY[i]
    a=agents.get(i,{}); return "RESIDUAL",(a.get("notes") or "unresolvable; candidate bad")[:140]

lines=["# Tier-A residual retry — disposition (2026-06-29)","",
 "Retry of the 21 unverified Tier-A residuals after the OpenAlex budget + Semantic Scholar "
 "rate-limit reset. Pipeline: deterministic Crossref pass (`13_crossref_retry.py`) -> 4-agent "
 "fleet (Crossref/OpenAlex/web/SSRN, no fabrication) -> deterministic verifier "
 "(`14_verify_retry.py`, Crossref title J>=0.50 & |yearD|<=3).","",
 "**Outcome: +1 verified (id1), +1 title-keyed (id28), 4 dropped as not-real/dup, 15 hard "
 "residual.** The retry did NOT meaningfully shrink the residual even with APIs uncapped — "
 "confirming a genuine recall/identifiability ceiling, not an API artifact. Candidate DOIs "
 "for the residual are confirmed wrong-paper, fabricated (404), or unregistered SSRN handles.","",
 "| id | disposition | basis |","|---|---|---|"]
from collections import Counter
cnt=Counter()
for i in ALL:
    d,why=disp(i); cnt[d.split()[0]]+=1
    t=next(r["title"] for r in json.load(open(HERE/"retry_input.json")) if r["id"]==i)
    lines.append(f"| {i} | {d} | {why.replace('|','/')} |")
lines+=["","## Summary",""]
for k,v in cnt.most_common(): lines.append(f"- **{k}**: {v}")
lines+=["",
 "## Gold-set impact","",
 "- Verified-with-DOI core: **14 -> 15** (id1 Fenge & Scheubel added).",
 "- Title-keyed gold items (real, no DOI): **+1** (id28 Ghana WP).",
 "- Dropped from the 35 distinct studies as not-real/duplicate: **4** (id15/16/19/20) -> "
 "**31 real distinct studies**.",
 "- Hard residual (real-but-unresolvable DOI): **15** — recommend RA hand-resolution via "
 "library/EconLit/direct author contact, or title-keying where a stable DOI never existed.",
 "",
 "## Method note (carry to promotion)","",
 "The J>=0.50 title guard is sound for *verifying a proposed DOI* but false-matches when used "
 "to *select* from blind Crossref search (observed: id5 Ecuador->Korea, id6 rural-China->wrong "
 "Zhang at J~0.5). `13_crossref_retry.py` therefore requires J>=0.80 for search-derived "
 "auto-accept; candidate-DOI verification keeps J>=0.50. Conversely, id1 shows the guard can "
 "*false-reject* a true match when the corpus title is corrupted — hence agent-evidence + RA "
 "adjudication remains the backstop."]
out=LOGS/"old-age-security-pension-crowdout-tier-a-retry-disposition.md"
out.write_text("\n".join(lines)+"\n")
print(f"written -> {out.name}")
print("disposition counts:",dict(cnt))
if __name__!="__main__": pass
