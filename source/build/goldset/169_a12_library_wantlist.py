#!/usr/bin/env python3
"""
169_a12_library_wantlist.py — A.12, stage 5. The residual procurement list for a human.

Inherits `142_b6_library_wantlist.py`. Everything the automated rungs could not reach, ordered so
that a person with a library proxy spends their time on the records that change the chapter rather
than on the longest list.

**THE ORDERING IS THE PRODUCT.** A flat list of a hundred DOIs gets worked from the top and abandoned
in the middle, which silently selects the evidence base by alphabetical accident. This list is ordered
by what a missing record costs:

  P0  `PRIMARY_OFFSET_STOPPING` — the causal spine. A missing record here is a missing study in the
      only cell that earns GRADE credit, and the cell's members DISAGREE with each other, so a
      partial read is worse than a small one: it could resolve a live disagreement by accident of
      retrieval.
  P1  the four JOB B1 methods entry points. All four are closed, and they are the only efficient
      route into 223 first-stage candidates that Wall 8 makes invisible to screening. Four PDFs here
      are worth more than forty anywhere else on this list.
  P2  records carrying the identity's CORRECTIONS — vanishing twin, differential twin mortality,
      measurement and zygosity method. The chapter's headline arithmetic is wrong without these, and
      wrong in a stated direction.
  P3  the Wall 6 INCLUDE side and the high-grade ART designs. These carry the ART arm's magnitude.
  P4  everything else on the wantlist.

Each line names WHY, so a partial procurement run still produces a defensible evidence base and the
chapter can state exactly which priority band it got through.

Output: literature/search-logs/{slug}-library-wantlist.md
        extraction/{slug}-library-dois.txt
"""
import csv, json, os
from collections import Counter

SLUG = "twinning-multiple-births"
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
EXTRACT = os.path.join(ROOT, "extraction")
LOGS = os.path.join(ROOT, "literature", "search-logs")
PDF_DIR = os.path.join(ROOT, "literature", "pdfs", SLUG)
OA = os.path.join(EXTRACT, f"{SLUG}-oa-status.json")
FETCH = os.path.join(EXTRACT, f"{SLUG}-pdf-retrieval-log.csv")
RECOV = os.path.join(EXTRACT, f"{SLUG}-pdf-recovery-log.csv")
SCREENED = os.path.join(LOGS, f"{SLUG}-screened.json")
OUT_MD = os.path.join(LOGS, f"{SLUG}-library-wantlist.md")
OUT_DOI = os.path.join(EXTRACT, f"{SLUG}-library-dois.txt")

B1_IDS = {"W2224629890", "W2150439610", "W2604712881", "W2013583398"}
CORRECTION_PATS = ("vanishing", "VANISHING", "conceived multiple", "foetal reduction",
                   "twin mortality", "neonatal deaths", "infanticide", "Weinberg",
                   "MEASUREMENT", "ascertain", "under-registration", "INTERGENERATIONAL")
HIGH_GRADE = ("RANDOMISED", "randomised", "meta-analysis", "META-ANALYSIS", "COCHRANE", "Cochrane",
              "systematic review", "POLICY", "LEGISLATION", "policy comparison", "CALL 3 CASE",
              "QUANTIFIES", "BOUNDS", "bounds")


def main():
    meta = {r["id"]: r for r in json.load(open(SCREENED))}
    want = json.load(open(OA))
    got = set()
    for f in os.listdir(PDF_DIR):
        if f.endswith(".pdf") and os.path.getsize(os.path.join(PDF_DIR, f)) > 1000:
            got.add(f.split("__")[0])
    recov = {r["id"]: r for r in csv.DictReader(open(RECOV))} if os.path.exists(RECOV) else {}
    fetched = {r["id"]: r for r in csv.DictReader(open(FETCH))}

    residual = []
    for wid in want:
        if wid in got:
            continue
        m = meta.get(wid, {})
        note = m.get("screen_note") or ""
        cell = m.get("cell")
        if cell == "PRIMARY_OFFSET_STOPPING":
            p, why = 0, "CAUSAL SPINE — the only cell earning GRADE credit, and its members disagree"
        elif wid in B1_IDS:
            p, why = 1, "METHODS ENTRY POINT — one of four routes into 223 first-stage candidates Wall 8 hides"
        elif any(t in note for t in CORRECTION_PATS):
            p, why = 2, "IDENTITY CORRECTION — the headline arithmetic is wrong without it"
        elif cell == "SECONDARY_ART_MULTIPLES" and (
                m.get("outcome_type") in ("population_births", "twinning_rate")
                or any(t in note for t in HIGH_GRADE)):
            p, why = 3, "ART arm magnitude — Wall 6 include side or a high-grade design"
        else:
            p, why = 4, f"wantlist residual ({cell})"
        r = recov.get(wid, {})
        route = ("blocked at every rung; %s alternate locations tried" % r.get("n_alt_locations", "?")
                 if r else "not open per OpenAlex — never attempted automatically")
        residual.append(dict(p=p, id=wid, doi=(m.get("doi") or "").replace("https://doi.org/", ""),
                             year=m.get("year"), venue=(m.get("venue") or "")[:34],
                             title=(m.get("title") or "")[:78], cell=cell, why=why,
                             route=route, note=note[:150],
                             oa=want[wid].get("status"), url=want[wid].get("url") or ""))
    residual.sort(key=lambda r: (r["p"], -(meta.get(r["id"], {}).get("cited_by_count") or 0)))

    with open(OUT_DOI, "w") as fh:
        for r in residual:
            if r["doi"]:
                fh.write(r["doi"] + "\n")

    n_want, n_got = len(want), len(got & set(want))
    bands = Counter(r["p"] for r in residual)
    BAND = {0: "P0 — causal spine", 1: "P1 — methods entry points",
            2: "P2 — identity corrections", 3: "P3 — ART arm magnitude", 4: "P4 — residual"}
    L = [f"# Stage 5 residual — library procurement list — {SLUG} (A.12)", "",
         f"**{n_got} of {n_want} wantlist records are readable ({n_got/n_want*100:.0f}%). "
         f"{len(residual)} need a human with a library proxy.**", "",
         "Nothing here is known to be unobtainable. Every record either was never open per OpenAlex, "
         "or was open but returned an HTML interstitial to every automated rung — a blocked route, "
         "not a closed paper.", "",
         "## Priority bands", "", "| band | n | why this order |", "|---|---|---|",
         f"| **P0** | {bands[0]} | The causal spine. A gap here is a missing study in the only cell "
         "earning GRADE credit — and because the cell's members DISAGREE, a partial read is worse "
         "than a small one: it could settle a live disagreement by accident of retrieval. |",
         f"| **P1** | {bands[1]} | All four methods entry points into the Wall 8 cell. Four PDFs here "
         "are worth more than forty anywhere else on this list. |",
         f"| **P2** | {bands[2]} | The identity's corrections. The chapter's headline arithmetic is "
         "wrong without these, and wrong in a known direction. |",
         f"| **P3** | {bands[3]} | The ART arm's magnitude — Wall 6 include side and high-grade designs. |",
         f"| **P4** | {bands[4]} | Everything else on the wantlist. |", "",
         "**A partial run is fine and expected. State the band you reached** — the chapter can then "
         "say exactly what it read and what it did not, which is the difference between a bounded "
         "evidence base and an unstated one.", ""]
    for p in sorted(bands):
        items = [r for r in residual if r["p"] == p]
        L += [f"## {BAND[p]} ({len(items)})", "",
              "| year | title | venue | DOI | why |", "|---|---|---|---|---|"]
        for r in items:
            L.append(f"| {r['year']} | {r['title']} | {r['venue']} | "
                     f"{('`'+r['doi']+'`') if r['doi'] else '—'} | {r['why']} |")
        L.append("")
    L += ["## Target path", "",
          f"Drop files at `literature/pdfs/{SLUG}/{{WID}}__{{any-slug}}.pdf` — the leading OpenAlex "
          "id before the double underscore is what ingest keys on; the rest of the filename is free. "
          "That directory is gitignored.", "",
          f"DOIs for a batch request: `extraction/{SLUG}-library-dois.txt`"]
    open(OUT_MD, "w").write("\n".join(L) + "\n")
    print(f"readable={n_got}/{n_want} ({n_got/n_want*100:.0f}%)  residual={len(residual)}")
    for p in sorted(bands):
        print(f"  {BAND[p]:<32} {bands[p]}")
    print(f"-> {os.path.relpath(OUT_MD, ROOT)}")


if __name__ == "__main__":
    main()
