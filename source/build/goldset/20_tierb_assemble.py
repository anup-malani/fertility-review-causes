#!/usr/bin/env python3
"""
Part 2 (Tier B) — assemble the screened tier from the 6-agent relevance audit.

Routing (precision audit over the unbiased frame):
  RELEVANT     -> Tier B core (the frozen recall-measurement set)
  UNCERTAIN    -> RA adjudication queue (NOT auto-dropped: most are title-only/ambiguous, and
                  auto-dropping would bias Tier B toward abstracted/keyword-findable papers,
                  defeating the unbiased design). RA resolves these into R / NR.
  NOT_RELEVANT -> dropped (snowball citation-noise false positives)

Keying: DOI where the OpenAlex citation-graph resolution produced one (resolve_status==
RESOLVED_DOI), else title-key (dead/drifted/no-DOI W-IDs — kept per the unbiasedness decision).

Inputs : *-tier-b-resolved.json + tierb_screen_verdict_{1..6}.json
Outputs: *-tier-b-screened.json (core), *-tier-b-uncertain-queue.json, *-tier-b-summary.md
"""
import json,sys
from pathlib import Path
from collections import Counter
HERE=Path(__file__).parent
LOGS=Path("/Users/shravanhari/~/Anup RA/projects/fertility-review-causes/literature/search-logs")

res={r["paperId"]:r for r in json.load(open(LOGS/"old-age-security-pension-crowdout-tier-b-resolved.json"))}
verd={}
for n in range(1,7):
    f=HERE/f"tierb_screen_verdict_{n}.json"
    if f.exists():
        for v in json.load(open(f)): verd[v["paperId"]]=v
    else: print(f"  WARN missing {f.name}",file=sys.stderr)

missing=[pid for pid in res if pid not in verd]
if missing: print(f"  WARN {len(missing)} frame papers have no verdict (agent gap)",file=sys.stderr)

def keyed(r):
    is_doi = r.get("resolve_status")=="RESOLVED_DOI" and r.get("doi")
    return ({"keytype":"DOI","doi":r["doi"]} if is_doi else {"keytype":"title-key","doi":None})

core=[]; queue=[]; dropped=0
for pid,r in res.items():
    v=verd.get(pid,{"verdict":"UNCERTAIN","confidence":"low","reason":"no verdict (agent gap)"})
    # For WID_DRIFT the OpenAlex year/venue/authors belong to the WRONG (drifted) paper, so they
    # are not trustworthy metadata for this gold item — only the snowball title is reliable.
    drift = r.get("resolve_status")=="WID_DRIFT"
    row={"paperId":pid,"title":r["title"],
         "year":None if drift else r.get("year"),
         "venue":None if drift else r.get("venue"),
         "authors":None if drift else r.get("authors"),
         "provenance_tier":"B","snowballPhase":r.get("snowballPhase"),
         "snow_confidence":r.get("snow_confidence"),"resolve_status":r.get("resolve_status"),
         "screen_verdict":v["verdict"],"screen_confidence":v.get("confidence"),
         "screen_reason":v.get("reason"),**keyed(r)}
    if v["verdict"]=="RELEVANT": core.append(row)
    elif v["verdict"]=="UNCERTAIN": queue.append(row)
    else: dropped+=1

json.dump(core,open(LOGS/"old-age-security-pension-crowdout-tier-b-screened.json","w"),indent=2)
json.dump(queue,open(LOGS/"old-age-security-pension-crowdout-tier-b-uncertain-queue.json","w"),indent=2)

ck=Counter(c["keytype"] for c in core)
tierA=json.load(open(LOGS/"old-age-security-pension-crowdout-tier-a-draft.json"))
L=["# Tier B — screened (Part 2)  ·  2026-06-29","",
 "Unbiased orthogonally-sourced relevant set (definition 1), DOI-resolved via the OpenAlex "
 "citation graph, then precision-audited by a 6-agent relevance screen. Dead/drifted-W-ID "
 "papers retained as title-keyed (unbiasedness decision). Agent/web DOI resolver BANNED here.","",
 "## Counts","",
 f"- frame (resolved): {len(res)}",
 f"- **Tier B core (RELEVANT): {len(core)}**  (DOI-keyed {ck['DOI']}, title-keyed {ck['title-key']})",
 f"- UNCERTAIN -> RA adjudication queue: {len(queue)}",
 f"- NOT_RELEVANT dropped (citation noise): {dropped}","",
 "## Combined gold set","",
 f"- Tier A (draft): {len(tierA)}",
 f"- Tier B core: {len(core)}",
 f"- **Total gold (A + B core): {len(tierA)+len(core)}**  (+ {len(queue)} Tier-B UNCERTAIN pending RA)","",
 "## Caveats","",
 "- ~40% of the frame is title-keyed (snowball-corpus W-ID rot); title-based recall matching is "
 "fuzzier than DOI matching. Resolution-failure was retained (not dropped) to avoid biasing "
 "Tier B toward findable papers.",
 "- The snowball was seeded off the (keyword-sourced) PI relevant set, so Tier B is *less* "
 "keyword-biased than Tier A but not perfectly independent — state this when reporting "
 "Recall(A)-Recall(B).",
 "- UNCERTAINs are NOT in the frozen core; RA must adjudicate them into R/NR before the final "
 "recall numbers, since auto-dropping would reintroduce findability bias."]
(LOGS/"old-age-security-pension-crowdout-tier-b-summary.md").write_text("\n".join(L)+"\n")

print(f"Tier B core (RELEVANT): {len(core)}  (DOI {ck['DOI']} + title-key {ck['title-key']})")
print(f"UNCERTAIN queue: {len(queue)}   NOT_RELEVANT dropped: {dropped}")
print(f"verdict dist: {dict(Counter(v['verdict'] for v in verd.values()))}")
print(f"combined gold A+B core: {len(tierA)+len(core)}")
print("written -> *-tier-b-screened.json, *-tier-b-uncertain-queue.json, *-tier-b-summary.md")
