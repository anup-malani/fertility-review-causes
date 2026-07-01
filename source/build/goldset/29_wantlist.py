#!/usr/bin/env python3
"""
Step 29 - Build the click-ready RA want-list for the residual PDFs (manual institutional-proxy
pull). Each row: DOI link (from manifest DOI, step-26 finalized DOI, or step-28 backfill) +
a pre-built Google Scholar search link, grouped by why auto-fetch missed it.

Input : {slug}-pdf-manifest.json, {slug}-metaanalysis-studies.json, {slug}-doi-backfill.json
Output: output/{slug}-pdf-wantlist.md
"""
import json, urllib.parse
from pathlib import Path

ROOT = Path("/Users/shravanhari/~/Anup RA/projects/fertility-review-causes")
SL = ROOT / "literature/search-logs"; OUT = ROOT / "output"
SLUG = "old-age-security-pension-crowdout"

REASON_HDR = {"no OA source": "No open-access copy indexed (mostly working papers / paywalled)",
              "OA links failed/non-PDF": "OA link existed but resolved to a landing page / failed"}

def gs(title): return "https://scholar.google.com/scholar?q=" + urllib.parse.quote(f'"{title}"')

def main():
    manifest = json.load(open(SL / f"{SLUG}-pdf-manifest.json"))
    studies = {s["paperId"]: s for s in json.load(open(SL / f"{SLUG}-metaanalysis-studies.json"))}
    backfill = json.load(open(SL / f"{SLUG}-doi-backfill.json")) if (SL / f"{SLUG}-doi-backfill.json").exists() else {}
    fetched = [x for x in manifest if x["status"] == "FETCHED"]
    still = [x for x in manifest if x["status"] == "NEEDS_MANUAL"]

    def doi_of(x):
        s = studies.get(x["paperId"], {})
        return x.get("doi") or s.get("doi_final") or s.get("doi") or backfill.get(x["paperId"])

    L = ["# OAS Meta-Analysis — PDF Want-List (manual retrieval)\n",
         f"**Auto-fetched:** {len(fetched)}/{len(manifest)} → `literature/pdfs/{SLUG}/`  ",
         f"**Need manual pull:** {len(still)} (below)  ",
         "**Method:** click the DOI link through the UChicago library proxy; if none/paywalled, use the Scholar link and grab the top free PDF (author copy / working paper). Save into the same `literature/pdfs/` folder named `<paperId>__<slug>.pdf`.\n",
         "> Note: auto-fetch only covered open-access copies; both discovery APIs (OpenAlex/Semantic Scholar) were anonymously rate-limited during this run, so some of these likely *do* have free copies findable via Scholar — this list is a starting point, not a paywall verdict.\n"]

    by_reason = {}
    for x in still: by_reason.setdefault(x.get("reason", "other"), []).append(x)
    n = 0
    for reason, items in sorted(by_reason.items(), key=lambda kv: -len(kv[1])):
        L.append(f"\n## {REASON_HDR.get(reason, reason)} — {len(items)} papers\n")
        for x in items:
            n += 1
            d = doi_of(x); s = studies.get(x["paperId"], {})
            doicell = f"[doi.org/{d}](https://doi.org/{d})" if d else "*(no DOI)*"
            L.append(f"{n}. **{x['title']}** ({s.get('year') or 'n.d.'}, T{x['tier']}) — "
                     f"{doicell} · [Scholar]({gs(x['title'])})")
    (OUT / f"{SLUG}-pdf-wantlist.md").write_text("\n".join(L) + "\n")
    print(f"want-list: {len(still)} papers, {sum(1 for x in still if doi_of(x))} with a DOI link "
          f"-> output/{SLUG}-pdf-wantlist.md")

if __name__ == "__main__":
    main()
