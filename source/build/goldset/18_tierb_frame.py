#!/usr/bin/env python3
"""
Part 2 (Tier B) — build the frame. Tier B = an UNBIASED sample of relevant papers w.r.t.
keyword-findability. Decision (Shravan, 2026-06-29): definition (1) — the orthogonally-SOURCED
relevant set, taken WHOLE; we do NOT filter for keyword-absence/vocabulary-disconnection
(filtering on findability would re-introduce the selection bias we're correcting for). The
snowball's citation-graph sourcing is what delivers the unbiasedness; orthogonality is a
property of the source, not a filter we apply.

Frame = snowball llm_verdict==RELEVANT, minus papers already claimed by Tier A (gold draft +
the 15 hard residuals / dev pool), deduped by normalized title. Keyword-universe membership is
IGNORED (that was the rejected definition 2).

NOTE: snowball records carry no DOI/year/abstract — only (paperId W-ID, title, phase, verdict).
DOI resolution + abstracts come later via the OpenAlex citation graph (the orthogonal channel;
the agent/web resolver is BANNED for Tier B, spec §3/§8).

Inputs : *-snowball.json, *-tier-a-draft.json, retry_verified_final.json (residual titles)
Output : old-age-security-pension-crowdout-tier-b-frame.json + stderr stats
"""
import json,re,sys
from pathlib import Path
from collections import Counter
HERE=Path(__file__).parent
LOGS=Path("/Users/shravanhari/~/Anup RA/projects/fertility-review-causes/literature/search-logs")
def norm(t): return re.sub(r"[^a-z0-9]+"," ",(t or "").lower()).strip()
def ndoi(d): return (d or "").replace("https://doi.org/","").strip().lower() or None

snow=json.load(open(LOGS/"old-age-security-pension-crowdout-snowball.json"))["papers"]
tierA=json.load(open(LOGS/"old-age-security-pension-crowdout-tier-a-draft.json"))
residual=[r for r in json.load(open(HERE/"retry_verified_final.json")) if r["verdict"]=="NOT_FOUND"]

# exclusion set: Tier A gold (56) + the 15 hard residuals (Tier A empirical, dev pool)
excl_title={norm(g["title"]) for g in tierA}
excl_doi={ndoi(g.get("doi")) for g in tierA if g.get("doi")}
excl_title|={norm(r["title"]) for r in residual}

rel=[p for p in snow if p.get("llm_verdict")=="RELEVANT"]
seen=set(); frame=[]; drop_excl=0; drop_dup=0
for p in rel:
    nt=norm(p["title"])
    if nt in excl_title or ndoi(p.get("doi")) in excl_doi: drop_excl+=1; continue
    if nt in seen: drop_dup+=1; continue
    seen.add(nt)
    frame.append({"paperId":p["paperId"],"title":p["title"],"snowballPhase":p.get("snowballPhase"),
                  "snow_confidence":p.get("llm_confidence"),"snow_reason":p.get("llm_reason")})

json.dump(frame,open(LOGS/"old-age-security-pension-crowdout-tier-b-frame.json","w"),indent=2)
print("=== Tier B frame (definition 1: unbiased orthogonally-sourced relevant set) ===",file=sys.stderr)
print(f"snowball RELEVANT          : {len(rel)}",file=sys.stderr)
print(f"  - Tier A / residual overlap: {drop_excl}",file=sys.stderr)
print(f"  - duplicate titles         : {drop_dup}",file=sys.stderr)
print(f"FRAME (distinct)           : {len(frame)}",file=sys.stderr)
print(f"  confidence: {dict(Counter(p['snow_confidence'] for p in frame))}",file=sys.stderr)
print(f"  phase     : {dict(Counter(p['snowballPhase'] for p in frame))}",file=sys.stderr)
wid=sum(1 for p in frame if (p['paperId'] or '').startswith('W'))
print(f"  resolvable by W-ID (OpenAlex citation graph): {wid}/{len(frame)}",file=sys.stderr)
print(f"\nwritten -> old-age-security-pension-crowdout-tier-b-frame.json",file=sys.stderr)
