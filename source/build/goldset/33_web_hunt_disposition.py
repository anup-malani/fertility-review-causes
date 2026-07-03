#!/usr/bin/env python3
"""
Step 33 - Record the web-hunt disposition of the 19 no-DOI Tier-B studies.

Four parallel web-research agents searched each corrupted-title no-DOI entry for the real paper,
with a right-paper verification guard (topic = old-age-security -> fertility; setting/authors must
match; no wrong-paper guessing). Result: only 3 map to genuinely new retrievable papers; 8 are
corrupted-title DUPLICATES of studies already in the set; 8 are PHANTOM/unverifiable (no findable
real paper, or a real paper on the wrong topic). This is an RA-adjudication artifact - it does NOT
auto-merge or drop anything, because the agent inferences are medium/low confidence and the merges
touch Tier B (the recall denominator). If the RA confirms the 8 duplicates, the distinct-study
count drops 60 -> ~52.

Output: output/{slug}-nodoi-web-hunt-disposition.md , {slug}-nodoi-web-hunt-disposition.json
"""
import json
from pathlib import Path

ROOT = Path("/Users/shravanhari/~/Anup RA/projects/fertility-review-causes")
SL = ROOT / "literature/search-logs"
OUT = ROOT / "output"
SLUG = "old-age-security-pension-crowdout"
SCRATCH = Path("/private/tmp/claude-501/-Users-shravanhari---Anup-RA-projects-fertility-review-causes/5a0555ce-ca49-4068-a29d-d4225df68d7a/scratchpad/nodoi19.json")

# category: NEW_FETCHED | NEW_PDF_UNAVAIL | DUP_OF_INCLUDED | PHANTOM
VERDICTS = {
 1:  ("DUP_OF_INCLUDED","10.1371/journal.pone.0234657","medium","No exact-title paper found; reads as a garbled variant of the Shen/Zheng/Yang NRPS->fertility study."),
 2:  ("PHANTOM",None,"high","Extensive search found NO empirical Chile-1981 pension-privatization->fertility study; all Chile-1981 hits concern pension finance, not fertility."),
 3:  ("PHANTOM",None,"high","No Chile paper by this title; 'children as retirement saving' appears only as a theory framing, not a Chile empirical study."),
 4:  ("PHANTOM",None,"medium","No NCMS->savings+fertility paper; nearest real study (Bai & Wu, NCMS & consumption) is off-topic (consumption, not fertility)."),
 5:  ("DUP_OF_INCLUDED","10.1371/journal.pone.0234657","high","Clean topical match to Shen/Zheng/Yang (NRPS, DiD on CFPS). No distinct paper of this title exists."),
 6:  ("DUP_OF_INCLUDED","10.1371/journal.pone.0234657","high","Garbled variant of the Shen NRPS->fertility study; no separate paper located."),
 7:  ("DUP_OF_INCLUDED","10.1371/journal.pone.0234657","medium","No distinct paper found across RePEc/SSRN/Scholar; best match is the Shen NRPS study (likely duplicate)."),
 8:  ("NEW_PDF_UNAVAIL",None,"high","REAL distinct paper: Zelu, Iranzo & Perez-Laborda, 'Pension Policy Reform and Fertility: Micro Evidence from Ghana' (URV WP, IZA/BREAD GLMLIC 2023). Exact-title match. OA PDF at conference.iza.org/.../zelu_b34232.pdf currently returns 503 - retry."),
 9:  ("PHANTOM",None,"high","No 'social security as a commitment mechanism / rural China' paper locatable; title appears fabricated."),
 10: ("PHANTOM",None,"medium","No quasi-experimental Hungarian pension->fertility study exists; the country in the title matches no real paper."),
 11: ("DUP_OF_INCLUDED","10.1257/pol.20200440","medium","'Pensions and Fertility' uniquely identifies Danzer & Zyska (AEJ:EP 2023, IZA DP 13048); setting is garbled (real setting Brazil, not Austria)."),
 12: ("PHANTOM",None,"medium","Zero exact-title hits; setting confirmed not Turkey. Its stored abstract is an organic-chemistry paper (W2131777609 is a documented WID-drift corrupt record) - so nothing real to resolve to. Ghost."),
 13: ("DUP_OF_INCLUDED","10.1257/pol.20200466","medium","Title stem 'The Old-Age Security Motive for Fertility: Evidence from the Extension of...' is verbatim Rossi & Godard (AEJ:EP 2022); setting garbled (real setting Namibia, not Rural China)."),
 14: ("PHANTOM",None,"low","Loose paraphrase; best thematic match is the Rossi & Godard Namibia paper (i.e. likely a duplicate of #13), but no verbatim anchor - unverifiable."),
 15: ("DUP_OF_INCLUDED","10.1371/journal.pone.0234657","medium","NRPS setting anchor matches Shen/Zheng/Yang; '...and Saving Behaviors' + 2023 date do not match the real 2020 paper."),
 16: ("DUP_OF_INCLUDED","10.1371/journal.pone.0234657","medium","Generalized/garbled form of the Shen NRPS->fertility study; no more authoritative match exists."),
 17: ("PHANTOM",None,"high","The real 2011 paper with this title (Staubli & Zweimueller) is a LABOR-MARKET study of older-worker employment - NOT fertility. Wrong-topic trap; correctly rejected."),
 18: ("NEW_FETCHED","10.4284/0038-4038-2013.055","medium","Real on-topic paper: Amuedo-Dorantes & Juarez, old-age transfers crowding out private gifts - setting MEXICO ('70 y Mas'), NOT Ecuador, and method is triple-difference, NOT the RCT the corrupted title claims. PDF fetched. RA: confirm this is the intended study."),
 19: ("NEW_FETCHED",None,"high","Real exact-title match: Elizondo, Flores & Quinto (2018), 'The Impact of Non-contributory Pensions: A Case Study for Costa Rica', Barcelona School of Economics. PDF fetched. NOTE: a master's-project working paper - RA confirm it meets the evidence bar."),
}
CAT_LABEL = {"NEW_FETCHED":"✅ new — PDF fetched","NEW_PDF_UNAVAIL":"🟡 new — real, PDF unavailable (retry)",
             "DUP_OF_INCLUDED":"♻️ duplicate of an included study","PHANTOM":"⛔ phantom / unverifiable"}

def main():
    src = {x["n"]: x for x in json.load(open(SCRATCH))}
    recs = []
    for n, (cat, maps_to, conf, ev) in sorted(VERDICTS.items()):
        s = src[n]
        recs.append({"n": n, "paperId": s["paperId"], "query_title": s["title"],
                     "category": cat, "maps_to_doi": maps_to, "confidence": conf, "evidence": ev})
    json.dump(recs, open(SL / f"{SLUG}-nodoi-web-hunt-disposition.json", "w"), indent=2)

    from collections import Counter
    c = Counter(r["category"] for r in recs)
    L = ["# No-DOI Tier-B studies — web-hunt disposition\n",
         "**What this is.** The 19 no-DOI, dead-WID studies in the meta-analysis set carried "
         "title-keyed metadata from the citation snowball, where ~40% of W-IDs have rotted/drifted. "
         "Four web-research agents searched each for the real paper, with a right-paper guard (topic "
         "must be old-age-security→fertility; setting/authors must match; no wrong-paper guessing).\n",
         "**Bottom line.** Only **3 of 19** map to genuinely new retrievable papers. **8 of 19** are "
         "corrupted-title **duplicates of studies already in the set** (Shen ×6, Danzer & Zyska ×1, "
         "Rossi & Godard ×1). **8 of 19** are **phantom/unverifiable** — no findable real paper, or a "
         "real paper on the wrong topic (the snowball's WID-drift corruption mangled titles *and* "
         "settings: 'Austria' was Brazil, 'Rural China' was Namibia, 'Ecuador' was Mexico).\n",
         f"| category | n |\n|---|--:|",
         f"| ✅ new, PDF fetched | {c['NEW_FETCHED']} |",
         f"| 🟡 new, real but PDF unavailable | {c['NEW_PDF_UNAVAIL']} |",
         f"| ♻️ duplicate of an included study | {c['DUP_OF_INCLUDED']} |",
         f"| ⛔ phantom / unverifiable | {c['PHANTOM']} |\n",
         "> **RA DECISION NEEDED.** The 8 duplicates are medium/low-confidence agent inferences that "
         "were NOT auto-merged. If you confirm them, the distinct-study count drops **60 → ~52**, and "
         "the same 16 dup+phantom entries should be pruned from Tier B (they inflate the recall "
         "denominator). Confidence is flagged per row; the settings are corrupted, so verify before merging.\n",
         "| # | query title (corrupted) | disposition | conf | maps to / note |",
         "|--:|---|---|:--:|---|"]
    for r in recs:
        mt = f"`{r['maps_to_doi']}`" if r["maps_to_doi"] else "—"
        L.append(f"| {r['n']} | {(r['query_title'] or '')[:58].replace('|','/')} | {CAT_LABEL[r['category']]} | {r['confidence']} | {mt} · {r['evidence'][:90]} |")
    (OUT / f"{SLUG}-nodoi-web-hunt-disposition.md").write_text("\n".join(L) + "\n")
    print(f"disposition: {dict(c)}  -> output/{SLUG}-nodoi-web-hunt-disposition.md")

if __name__ == "__main__":
    main()
