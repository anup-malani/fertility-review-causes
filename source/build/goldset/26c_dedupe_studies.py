#!/usr/bin/env python3
"""
Step 26c - Collapse the meta-analysis-ready records to DISTINCT STUDIES and drop non-papers,
then regenerate OUTPUT 1 (the markdown DOI list) from the clean set.

Two problems the paperId-level tiering can't see:
  1. Version-variants: one study appears under several works (published + SSRN/WP preprints,
     each with its own W-ID and DOI). A meta-analysis wants ONE row per study.
  2. Non-papers: OpenAlex indexes replication/data-and-code DEPOSITS (ICPSR/openICPSR,
     DOI prefix 10.3886, or titles beginning "Data and Code for"/"Replication ...") as works;
     they can score ET==4 off the deposit description but are not evidence records.

Dedup key = normalized title (author-agnostic; version-variants share a title). Within a study
group the CANONICAL record is chosen by: DOI trust rank -> published-over-workingpaper ->
higher tier (T1>T2) -> has-DOI -> lower composite tie-break. Dropped variants are recorded.

Input : {slug}-metaanalysis-ready-final.json
Output: {slug}-metaanalysis-studies.json (canonical, one per study),
        output/{slug}-metaanalysis-doi-list.md (regenerated), {slug}-dedupe-log.json
"""
import json, re
from pathlib import Path
from collections import defaultdict

ROOT = Path("/Users/shravanhari/~/Anup RA/projects/fertility-review-causes")
SL = ROOT / "literature/search-logs"
OUT = ROOT / "output"
SLUG = "old-age-security-pension-crowdout"

STOP = {"the","a","an","of","and","in","on","for","from","to","its","by","new","is","with","evidence"}
def ttokens(t):
    # delete intra-word hyphens/apostrophes (micro-economic -> microeconomic, children's -> childrens)
    # BEFORE splitting on remaining punctuation, so punctuation variants collapse to one token set.
    s = re.sub(r"[-'’]", "", (t or "").lower())
    return {w for w in re.sub(r"[^a-z0-9\s]", " ", s).split() if w not in STOP}
def tkey(t):
    return " ".join(sorted(ttokens(t)))[:70]

def first_author(r):
    a = r.get("authors") or []
    if not a: return None
    s = re.sub(r"[^a-z]", "", (a[0] or "").split()[-1].lower()) if a[0] else ""
    return s if len(s) >= 3 else None

TRUST_RANK = {"gold-RA-verified": 0, "gold-RA-verified(title)": 0, "corrected-map(title-verified)": 1,
              "crossref-search(J>=0.80)": 2, "openalex-fresh(guarded)": 3, "UNRESOLVED": 9}

def is_nonpaper(r):
    t = (r.get("title") or "").lower()
    d = (r.get("doi_final") or "")
    return (t.startswith("data and code") or t.startswith("replication")
            or "replication package" in t or d.startswith("10.3886"))

def is_wp(r):
    d = (r.get("doi_final") or "")
    return d.startswith("10.2139/ssrn") or "working paper" in (r.get("title") or "").lower()

def canon_sort(r):
    return (TRUST_RANK.get(r.get("doi_trust"), 5), 1 if is_wp(r) else 0,
            r.get("tier", 9), 0 if r.get("doi_final") else 1, -(r.get("compositeScore") or 0))

ET_LABEL = {4: "natural/quasi-experiment", 3: "proxy/IV", 2: "observational"}
def authstr(a):
    if not a: return "n.a."
    return (a[0] if len(a) == 1 else f"{a[0]} et al.") if len(a) > 2 else " & ".join(a)

def main():
    rows = json.load(open(SL / f"{SLUG}-metaanalysis-ready-final.json"))
    nonpapers = [r for r in rows if is_nonpaper(r)]
    papers = [r for r in rows if not is_nonpaper(r)]

    groups = defaultdict(list)
    for r in papers:
        groups[tkey(r["title"])].append(r)

    studies = []; merged_log = []
    for k, v in groups.items():
        v.sort(key=canon_sort)
        canon = dict(v[0])
        if len(v) > 1:
            canon["alt_versions"] = [{"paperId": x["paperId"], "doi": x["doi_final"],
                                      "year": x.get("year"), "trust": x["doi_trust"]} for x in v[1:]]
            merged_log.append({"title": canon["title"], "kept": canon["paperId"],
                               "kept_doi": canon["doi_final"], "n_versions": len(v)})
        studies.append(canon)

    # Second pass: catch working-paper/published version-variants whose titles differ in LENGTH
    # (one is a subtitle-extended version of the other), which the title-key pass cannot see.
    # Conservative guard: same first-author surname + year within 3 + one title's content-token
    # set is a subset of the other's (smaller side >= 2 tokens). Guards against WID-drift garbage
    # metadata by requiring the author key to be a real (>=3 char) surname.
    merged = True
    while merged:
        merged = False
        for i in range(len(studies)):
            for j in range(i + 1, len(studies)):
                a, b = studies[i], studies[j]
                fa, fb = first_author(a), first_author(b)
                if not fa or fa != fb: continue
                ya, yb = a.get("year"), b.get("year")
                if ya and yb and abs(ya - yb) > 3: continue
                ta, tb = ttokens(a["title"]), ttokens(b["title"])
                small = ta if len(ta) <= len(tb) else tb
                if len(small) >= 2 and (ta <= tb or tb <= ta):
                    pair = sorted([a, b], key=canon_sort)
                    keep, drop = dict(pair[0]), pair[1]
                    keep["alt_versions"] = keep.get("alt_versions", []) + [
                        {"paperId": drop["paperId"], "doi": drop["doi_final"],
                         "year": drop.get("year"), "trust": drop["doi_trust"]}] + drop.get("alt_versions", [])
                    merged_log.append({"title": keep["title"], "kept": keep["paperId"],
                                       "kept_doi": keep["doi_final"],
                                       "n_versions": 1 + len(keep["alt_versions"]),
                                       "merge": "author+containment"})
                    studies = [s for k2, s in enumerate(studies) if k2 not in (i, j)] + [keep]
                    merged = True
                    break
            if merged: break

    # Third/fourth pass: apply the web-hunt disposition (step 33). Gated on the disposition file so
    # the base pipeline is unaffected. (a) DUP_OF_INCLUDED: corrupted-title dead-WID entries a web
    # hunt mapped to a paper ALREADY in the set -> merge into that canonical study by DOI. (b)
    # PHANTOM: entries with no real paper on the web (ghost/hallucinated forward-citation records,
    # dead W-IDs, mis-joined metadata) -> drop entirely. Both were RA-confirmed.
    dropped_phantoms = []
    disp_p = SL / f"{SLUG}-nodoi-web-hunt-disposition.json"
    if disp_p.exists():
        disp = json.load(open(disp_p))
        forced = {d["paperId"]: d["maps_to_doi"] for d in disp
                  if d["category"] == "DUP_OF_INCLUDED" and d["maps_to_doi"]}
        phantoms = {d["paperId"] for d in disp if d["category"] == "PHANTOM"}
        by_doi = {s["doi_final"]: s for s in studies if s.get("doi_final")}
        keep = []
        for s in studies:
            if s["paperId"] in phantoms:
                dropped_phantoms.append({"paperId": s["paperId"], "title": s["title"]})
                continue
            tgt = forced.get(s["paperId"])
            if tgt and tgt in by_doi and by_doi[tgt] is not s:
                canon = by_doi[tgt]
                canon.setdefault("alt_versions", []).append(
                    {"paperId": s["paperId"], "doi": s.get("doi_final"), "year": s.get("year"),
                     "trust": s.get("doi_trust"), "merge": "web-hunt-duplicate"})
                merged_log.append({"title": s["title"], "kept": canon["paperId"],
                                   "kept_doi": canon["doi_final"], "merge": "web-hunt-duplicate"})
            else:
                keep.append(s)
        studies = keep

    studies.sort(key=lambda r: (r["tier"], -(r.get("compositeScore") or 0)))

    json.dump(studies, open(SL / f"{SLUG}-metaanalysis-studies.json", "w"), indent=2)
    json.dump({"dropped_nonpapers": [{"paperId": r["paperId"], "title": r["title"],
                                      "doi": r["doi_final"]} for r in nonpapers],
               "merged_version_groups": merged_log,
               "dropped_phantoms": dropped_phantoms},
              open(SL / f"{SLUG}-dedupe-log.json", "w"), indent=2)

    res = sum(1 for r in studies if r["doi_final"])
    trust_ct = defaultdict(int)
    for r in studies: trust_ct[r["doi_trust"]] += 1

    L = ["# Old-Age-Security / Pension-Crowdout — Meta-Analysis-Ready DOI List\n",
         "**Hypothesis:** old-age-security / pension crowdout of fertility  ",
         "**Set:** meta-analysis-ready = (Tier 1 ∪ Tier 2) ∩ evidenceType == 4 (natural/quasi-experiments), deduped to distinct studies  ",
         f"**Distinct studies = {len(studies)}**  (from {len(papers)} paper-records; {len(rows)-len(papers)} non-paper deposits dropped, {len(papers)-len(studies)-len(dropped_phantoms)} version-variants merged, {len(dropped_phantoms)} ghost/phantom entries dropped)  ",
         "pipeline: GACS Phase E on the OAS pilot (legacy-migration path)  ",
         "**Generated by:** `source/build/goldset/26c_dedupe_studies.py`\n",
         f"DOIs resolved: **{res}/{len(studies)}**  ·  trust: " +
         " · ".join(f"{k} {n}" for k, n in sorted(trust_ct.items())) + "\n",
         "| # | DOI | Title | Authors | Year | Tier | ET | comp | channel | gold | DOI trust | alt versions |",
         "|--:|---|---|---|--:|:--:|:--:|:--:|:--:|:--:|---|--:|"]
    for i, r in enumerate(studies, 1):
        d = r["doi_final"]
        dcell = f"`{d}`" if d else f"⚠ UNRESOLVED ({r.get('doi_flag')})"
        t = (r["title"] or "")[:80].replace("|", "\\|")
        L.append(f"| {i} | {dcell} | {t} | {authstr(r.get('authors'))} | {r.get('year') or ''} "
                 f"| T{r['tier']} | {r['evidenceType']} | {r['compositeScore']} | {r.get('channel') or ''} "
                 f"| {'★' if r['in_gold'] else ''} | {r['doi_trust']} | {len(r.get('alt_versions', []))} |")
    L.append("\n## Plain DOI list (resolved distinct studies)\n")
    for r in studies:
        if r["doi_final"]: L.append(f"- {r['doi_final']}")
    unres = [r for r in studies if not r["doi_final"]]
    if unres:
        L.append(f"\n## Unresolved ({len(unres)}) — title-keyed, need manual/Crossref resolution\n")
        for r in unres:
            L.append(f"- [{r.get('doi_flag')}] {r['title']} ({r.get('year') or 'n.d.'}) — {r['paperId']}")
    if nonpapers:
        L.append(f"\n## Dropped — non-paper deposits ({len(nonpapers)})\n")
        for r in nonpapers:
            L.append(f"- {r['title']} — `{r['doi_final']}`")
    (OUT / f"{SLUG}-metaanalysis-doi-list.md").write_text("\n".join(L) + "\n")

    print(f"{len(rows)} records -> {len(studies)} distinct studies "
          f"({len(nonpapers)} non-papers dropped, {len(papers)-len(studies)-len(dropped_phantoms)} versions merged, "
          f"{len(dropped_phantoms)} phantoms dropped) | DOIs {res}/{len(studies)} resolved")
    print(f"OUTPUT 1 (deduped) -> output/{SLUG}-metaanalysis-doi-list.md")

if __name__ == "__main__":
    main()
