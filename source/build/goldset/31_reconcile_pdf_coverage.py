#!/usr/bin/env python3
"""
Step 31 - Reconcile PDF coverage to the canonical DISTINCT-STUDY set (post step-26c re-dedup).

Steps 27/28/30 built the manifest per paper-RECORD, before the author+containment merge collapsed
version-variants (e.g. the SSRN preprint and NBER working paper whose OA PDFs cover a study whose
published version is paywalled). This step re-keys coverage to the 60 canonical studies: a study
counts as COVERED if ANY of its versions (canonical paperId OR any alt_version paperId) has a PDF
on disk. Produces the study-level manifest, the reconciled want-list, and a coverage summary.

Input : {slug}-metaanalysis-studies.json, {slug}-pdf-manifest.json, literature/pdfs/{slug}/*.pdf
Output: {slug}-pdf-coverage.json (study-level), output/{slug}-pdf-wantlist.md (reconciled)
"""
import json, urllib.parse
from pathlib import Path

ROOT = Path("/Users/shravanhari/~/Anup RA/projects/fertility-review-causes")
SL = ROOT / "literature/search-logs"
OUT = ROOT / "output"
SLUG = "old-age-security-pension-crowdout"
PDFDIR = ROOT / "literature/pdfs" / SLUG

def main():
    studies = json.load(open(SL / f"{SLUG}-metaanalysis-studies.json"))
    manifest = {x["paperId"]: x for x in json.load(open(SL / f"{SLUG}-pdf-manifest.json"))}
    disp_p = SL / f"{SLUG}-nodoi-web-hunt-disposition.json"
    disp = {d["paperId"]: d for d in json.load(open(disp_p))} if disp_p.exists() else {}
    on_disk = {}
    for p in PDFDIR.glob("*.pdf"):
        on_disk.setdefault(p.name.split("__")[0], p.name)

    cov = []; covered = 0; want = []
    for s in studies:
        vids = [s["paperId"]] + [a["paperId"] for a in s.get("alt_versions", [])]
        pdf = next((on_disk[v] for v in vids if v in on_disk), None)
        rec = {"paperId": s["paperId"], "title": s["title"], "doi": s.get("doi_final"),
               "tier": s["tier"], "evidenceType": s["evidenceType"],
               "n_versions": len(vids), "covered": bool(pdf), "file": pdf}
        cov.append(rec)
        if pdf: covered += 1
        else:
            d = disp.get(s["paperId"])
            # Route confirmed dup/phantom no-DOI entries to the disposition file, not the want-list.
            if d and d["category"] in ("DUP_OF_INCLUDED", "PHANTOM"):
                rec["disposition"] = d["category"]; cov[-1] = rec
                continue
            reason = (d["evidence"][:80] if d else
                      next((manifest[v].get("reason") for v in vids if v in manifest and manifest[v].get("reason")), "no OA source"))
            want.append({**rec, "reason": reason, "year": s.get("year")})

    json.dump({"n_studies": len(studies), "covered": covered, "missing": len(want), "studies": cov},
              open(SL / f"{SLUG}-pdf-coverage.json", "w"), indent=2)

    n_dup = sum(1 for c in cov if c.get("disposition") == "DUP_OF_INCLUDED")
    n_ph = sum(1 for c in cov if c.get("disposition") == "PHANTOM")
    L = [f"# OAS meta-analysis — PDF want-list (RA institutional-proxy pull)\n",
         f"**Study-level coverage: {covered}/{len(studies)} distinct studies have a PDF** "
         f"in `literature/pdfs/{SLUG}/` ({len(list(PDFDIR.glob('*.pdf')))} files; some studies covered by a working-paper version).  ",
         f"**{len(want)} studies still need retrieval** (below) — genuine papers only.\n",
         "> These are the real, retrievable residual. Most are **paywalled-published (have a DOI):** "
         "pull via the UChicago proxy. One or two are **no-DOI working papers** with a known source to "
         "retry (e.g. the Ghana paper's IZA link).\n",
         f"> **Separately, {n_dup + n_ph} of the no-DOI dead-WID entries were NOT genuine retrieval "
         f"targets** — a web hunt found {n_dup} are corrupted-title **duplicates of studies already in "
         f"the set** and {n_ph} are **phantom/unverifiable**. They are routed out of this list to "
         f"`output/{SLUG}-nodoi-web-hunt-disposition.md` for RA adjudication (confirming the duplicates "
         f"drops the distinct count 60 → ~{len(studies) - n_dup}).\n",
         "| # | Title | Year | DOI / link | Tier | reason |", "|--:|---|--:|---|:--:|---|"]
    for i, x in enumerate(sorted(want, key=lambda r: (0 if r["doi"] else 1, r["tier"])), 1):
        if x["doi"]:
            link = f"[doi.org/{x['doi']}](https://doi.org/{x['doi']})"
        else:
            link = f"[Scholar](https://scholar.google.com/scholar?q={urllib.parse.quote((x['title'] or '')[:120])})"
        L.append(f"| {i} | {(x['title'] or '')[:70].replace('|','/')} | {x.get('year') or ''} | {link} | T{x['tier']} | {x['reason']} |")
    (OUT / f"{SLUG}-pdf-wantlist.md").write_text("\n".join(L) + "\n")

    print(f"study-level coverage {covered}/{len(studies)}; want-list {len(want)} studies "
          f"({sum(1 for w in want if w['doi'])} with DOI / {sum(1 for w in want if not w['doi'])} no-DOI)")
    print(f"-> output/{SLUG}-pdf-wantlist.md ; {SLUG}-pdf-coverage.json")

if __name__ == "__main__":
    main()
