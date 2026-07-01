#!/usr/bin/env python3
"""
Step 24a - Build Sonnet evidence-scoring batches for the 735 unscored T1uT2 candidates.

Emits N batch files (title + abstract + paperId) into a scoring dir, plus a shared rubric
file, so scoring agents can run in parallel and write one output file each. The rubric is
reconstructed EXACTLY from Anup's 542 scored papers (compositeScore == ET + id + centrality,
verified 542/542) so the new scores are commensurable with the existing 474.

Input : {slug}-metaanalysis-candidates.json, {slug}-oa-enrichment.json
Output: temp/scoring/{slug}-batch-XX.json  (input), RUBRIC.md (shared), manifest.json
"""
import json, math
from pathlib import Path

SL = Path("/Users/shravanhari/~/Anup RA/projects/fertility-review-causes/literature/search-logs")
OUT = Path("/Users/shravanhari/~/Anup RA/projects/fertility-review-causes/temp/scoring")
OUT.mkdir(parents=True, exist_ok=True)
SLUG = "old-age-security-pension-crowdout"
BATCH = 50

RUBRIC = """# OAS evidence-scoring rubric (reconstructed from Anup's 542 scored papers)

Score each paper on THREE integer dimensions. `compositeScore = evidenceType + identification + centrality` (0-10) is computed downstream; do NOT output it.

## evidenceType (0-4) - what KIND of evidence the study provides on the OAS->fertility link
- 0 = qualitative / descriptive fieldwork or survey with no quantitative estimation, OR pure data description
- 1 = theoretical / formal model, possibly with a qualitative review of empirical findings; no own estimation
- 2 = econometric estimation on observational data (OLS, structural, panel) WITHOUT an exogenous identification strategy
- 3 = empirical with a proxy / instrument / cross-sectional design that is causal-leaning but not a clean experiment
- 4 = natural or quasi-experiment: exploits exogenous variation (pension reform, policy discontinuity) for causal identification

## identification (0-3) - strength of the causal identification strategy
- 0 = none (pure theory / description)
- 1 = weak (raw correlation / OLS with no confound handling)
- 2 = moderate (controls, proxies, structural estimation, historical quasi-variation argued not clean)
- 3 = strong (clean natural experiment, IV, or credible discontinuity)

## centrality (0-3) - how central the OAS -> fertility question is to the paper
- 0 = tangential mention
- 1 = one of several themes
- 2 = major theme but not the sole focus
- 3 = the primary research question

## Output
Return a JSON array; one object per input paperId, PRESERVING every paperId given:
[{"paperId":"W...","evidenceType":0-4,"identification":0-3,"centrality":0-3,"mechanism":"<short tag>","scoreRationale":"<=200 chars"}]
- Score on the ABSTRACT when present; on the TITLE ALONE when abstract is null (do NOT drop it - be conservative, lean to the lower evidenceType if design is unclear from title).
- The corpus is already screened RELEVANT to old-age-security/pension crowdout of fertility; you are grading evidence quality, not relevance.
"""

def main():
    cands = json.load(open(SL / f"{SLUG}-metaanalysis-candidates.json"))
    enrich = json.load(open(SL / f"{SLUG}-oa-enrichment.json"))
    todo = [c for c in cands if not c["scored"]]

    items = []
    for c in todo:
        e = enrich.get(c["paperId"], {})
        items.append({
            "paperId": c["paperId"],
            "title": c.get("title") or e.get("oa_title"),
            "abstract": e.get("abstract"),
        })

    (OUT / "RUBRIC.md").write_text(RUBRIC)
    nb = math.ceil(len(items) / BATCH)
    manifest = []
    for i in range(nb):
        chunk = items[i*BATCH:(i+1)*BATCH]
        fn = OUT / f"{SLUG}-batch-{i+1:02d}.json"
        json.dump(chunk, open(fn, "w"), indent=2)
        manifest.append({"batch": i+1, "input": str(fn),
                         "output": str(OUT / f"{SLUG}-scores-{i+1:02d}.json"),
                         "n": len(chunk)})
    json.dump(manifest, open(OUT / "manifest.json", "w"), indent=2)
    tl = sum(1 for it in items if not it["abstract"])
    print(f"{len(items)} papers -> {nb} batches of <= {BATCH} ({tl} title-only)")
    print(f"scoring dir: {OUT}")

if __name__ == "__main__":
    main()
