#!/usr/bin/env python3
"""
121_b5_pdf_wantlist.py — B.5, stage 5 prep. Build the retrieval wantlist.

Emits the human-facing procurement list and a bare DOI file for bulk tools. Two retrieval jobs are
kept apart because they answer different questions and have different failure costs:

  JOB A — the RA gate (31 records). Needed before extraction. 18 are primary-cell records whose
          effects go in the extraction table; 13 are held records that need only enough full text to
          settle a routing question, and most are expected to route away.
  JOB B — the parameter and measurement set. These do NOT enter the extraction table and earn no
          GRADE credit, but the demographic-significance model rests on them and the FDT verdict
          turns on one of them (the historical early-loss rate). Four are monographs, which is a
          library request rather than a PDF fetch.

Target paths follow the house convention, `literature/pdfs/{slug}/{WID}__{title-slug}.pdf`, so a file
dropped there is picked up by the ingest stage without renaming. That directory is gitignored.

Output: literature/search-logs/{slug}-pdf-wantlist.md
        extraction/{slug}-retrieval-dois.txt
"""
import csv, json, os, re

SLUG = "fetal-loss-intrauterine-mortality"
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
LOGS = os.path.join(ROOT, "literature", "search-logs")
EXTRACT = os.path.join(ROOT, "extraction")
GATE = os.path.join(EXTRACT, f"{SLUG}-ra-gate.csv")
TIERS = os.path.join(LOGS, f"{SLUG}-screen-tiers.json")
ANCHORS = os.path.join(LOGS, f"{SLUG}-cold-start-anchors.json")
OUT_MD = os.path.join(LOGS, f"{SLUG}-pdf-wantlist.md")
OUT_DOI = os.path.join(EXTRACT, f"{SLUG}-retrieval-dois.txt")

# JOB B, named explicitly. Each entry says WHICH model input it supplies, because a parameter paper
# retrieved without knowing what it is for tends to be read and not used.
PARAMETER_SET = [
    ("W2037830047", "interval decomposition: the additive components, incl. time added by wastage"),
    ("W2029856993", "w (fecundability) in a natural-fertility population, by age and parity"),
    ("W1987954319", "bias in estimated fetal-death and stillbirth ratios; microsimulation"),
    ("W2326779985", "measurement: real variation vs artefacts, and induced-abortion under-reporting"),
    ("W2042808881", "loss schedule by age, gravidity and spacing across 8 WFS countries"),
    ("W2010823606", "gestational-age-resolved loss hazards, 555,038 pregnancies"),
    ("W2765259962", "US recognised-loss TREND 1990-2011"),
    ("W4376226364", "under-reporting ADJUSTMENT procedures, 157 surveys / 53 countries"),
    ("W3128085333", "four decades of DHS stillbirth measurement"),
    ("W2460102972", "full pregnancy-outcome accounting: births, induced abortion, fetal loss"),
    ("W1982023181", "FDT-era: why the Danish stillbirth rate fell after 1940"),
    ("W2083656791", "FDT-era: Derbyshire c.1900, individual-level, boundary respected"),
    ("W4385858609", "FDT-era: Bern maternity hospital 1880-1900 and 1914-1922"),
    ("W4289977916", "FDT-era: Italian regions post-unification, misreporting modelled"),
    ("W2005548471", "FDT-era: Cumbria 1950-92, 280,757 births"),
    ("W4388167902", "loss frequency by gestational stage, incl. pre-recognition"),
]

BOOKS = [
    ("W1672120424", "Wood 1994, Dynamics of Human Reproduction", "i, w, and the natural-fertility benchmark"),
    ("W1999725017", "Leridon 1977, Human Fertility: The Basic Components", "the loss schedule and interval model"),
    ("W2093319181", "Bongaarts & Potter 1983, Fertility, Biology, and Behavior", "time added per loss"),
    ("W575052866", "Biomedical and Demographic Determinants of Reproduction (1993)", "conception and fetal loss in one frame"),
]


def slugify(t):
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", (t or "").lower())).strip("-")[:60]


def main():
    gate = list(csv.DictReader(open(GATE)))
    tiers = json.load(open(TIERS))
    by_id = {r["id"]: r for t in ("0", "1", "2", "3") for r in tiers[t]}
    anchors = {a.get("doi"): a for a in json.load(open(ANCHORS)) if a.get("doi")}
    anchor_by_title = {a["title"].lower(): a for a in json.load(open(ANCHORS))}

    PRIMARY = {"PRIMARY_SHOCK_TO_BIRTHS", "PRIMARY_LOSS_TO_FERTILITY", "REPLACEMENT_COMPENSATION"}
    job_a_primary = [r for r in gate if r["cell"] in PRIMARY]
    job_a_held = [r for r in gate if r["cell"] not in PRIMARY]
    # Priority within primary: the two the chapter singles out first, then by citation weight.
    HIGHEST = {"W4283072838", "W2009105027"}
    job_a_primary.sort(key=lambda r: (r["openalex_id"] not in HIGHEST, -int(r["cited_by"] or 0)))
    job_a_held.sort(key=lambda r: (r["cell"], -int(r["cited_by"] or 0)))

    dois = []

    def row(wid, doi, title, why, year=None, venue=None):
        path = f"literature/pdfs/{SLUG}/{wid}__{slugify(title)}.pdf"
        if doi:
            dois.append(doi)
        return (f"- **{title[:96]}**  \n"
                f"  `{doi or 'NO DOI'}` · {year or '?'} · {(venue or '')[:40]}  \n"
                f"  *{why}*  \n"
                f"  → `{path}`")

    L = [f"# PDF wantlist — {SLUG} (B.5)", "",
         "Generated by `source/build/goldset/121_b5_pdf_wantlist.py`. Two jobs, kept apart because "
         "they answer different questions.", "",
         "**Where the files go.** `literature/pdfs/fetal-loss-intrauterine-mortality/` — create it if "
         "absent. Filename `{OpenAlexID}__{title-slug}.pdf`, exactly as given under each entry below. "
         "The ingest stage keys on the OpenAlex id prefix, so a file named anything else is invisible "
         "to it. The directory is gitignored: PDFs never enter the repo, only the retrieval log does.", "",
         "**If a PDF cannot be obtained**, record it as a failure in the retrieval log rather than "
         "letting it vanish. A missing study and a study that does not exist are different facts and "
         "collapsing them manufactures absences.", "",
         "---", "",
         f"## Job A — the RA gate ({len(gate)} records, all DOI-resolved)", "",
         "Needed before extraction can start. Sign `extraction/fetal-loss-intrauterine-mortality-"
         "ra-gate.csv` as you go: the RA verdict is the inclusion decision, the screen only feeds it.", "",
         f"### A1. Primary cells — extract effects ({len(job_a_primary)})", "",
         "These carry the estimates. Every one needs `ESTIMAND_LEVEL` set at full text "
         "(`ACCOUNTING_SHARE` vs `BEHAVIORAL_NET`), which is the field that decides poolability and "
         "which no abstract states.", ""]
    for r in job_a_primary:
        star = " ⭐ **highest value**" if r["openalex_id"] in HIGHEST else ""
        L.append(row(r["openalex_id"], r["doi"], r["title"] + star,
                     f"{r['cell']} — {r['screen_note'][:150]}", r["year"], r["venue"]))
    L += ["", f"### A2. Held for routing ({len(job_a_held)})", "",
          "These need only enough full text to settle one question each: whether stillbirth and "
          "neonatal components separate (Wall 1), or whether the conception and survival margins are "
          "decomposed (Wall 2). Most are expected to route away. Methods section is usually enough.", ""]
    for r in job_a_held:
        L.append(row(r["openalex_id"], r["doi"], r["title"],
                     f"{r['cell']} — {r['screen_note'][:150]}", r["year"], r["venue"]))

    L += ["", "---", "",
          f"## Job B — parameter and measurement set ({len(PARAMETER_SET)} articles + {len(BOOKS)} books)", "",
          "These do **not** enter the extraction table and earn no GRADE credit. They are the inputs "
          "to `source/analysis/b5_demographic_significance.py`, and the FDT verdict turns on one of "
          "them: the historical early-loss rate is currently inferred, and it is the single parameter "
          "that decides whether B.5 clears PROTOCOL §4.2's 10% line. The five FDT-era historical "
          "series below are the ones that could pin it down.", ""]
    for wid, why in PARAMETER_SET:
        r = by_id.get(wid)
        if not r:
            L.append(f"- `{wid}` — not found in the screened set (check the ranked frame)")
            continue
        L.append(row(wid, r.get("doi"), r["title"], why, r.get("year"), r.get("venue")))

    L += ["", f"### Books — library request, not a PDF fetch ({len(BOOKS)})", "",
          "All four failed DOI resolution at stage A3 because every same-title index record is a "
          "*review* of the book. They were recovered through the citation frame, so the OpenAlex ids "
          "below are real, but there is no article PDF to fetch. UChicago holdings or ILL.", ""]
    for wid, name, why in BOOKS:
        r = by_id.get(wid, {})
        L.append(f"- **{name}**  \n  `{wid}` · no article DOI  \n  *{why}*  \n"
                 f"  → `literature/pdfs/{SLUG}/{wid}__{slugify(r.get('title') or name)}.pdf` "
                 "(scan of the relevant chapters is fine)")

    L += ["", "---", "", "## Counts", "",
          f"| job | n | enters extraction table? |", "|---|---|---|",
          f"| A1 primary | {len(job_a_primary)} | yes |",
          f"| A2 held | {len(job_a_held)} | only those that survive routing, expect 3-5 |",
          f"| B parameters | {len(PARAMETER_SET)} | no — model inputs |",
          f"| B books | {len(BOOKS)} | no — model inputs |",
          f"| **total to procure** | **{len(gate) + len(PARAMETER_SET) + len(BOOKS)}** | |", "",
          f"Bare DOI list for Zotero or a bulk fetcher: "
          f"`extraction/{SLUG}-retrieval-dois.txt` ({len(set(dois))} DOIs).", "",
          "## Caveat on completeness", "",
          "This list is conditional on a screen bounded at 392 of 11,125 frame records. Extending the "
          "screen deeper would add primary-cell records, at a lower rate since D1 ranked the tail. The "
          "wantlist is the retrieval need *for the current screen*, not a claim that the literature "
          "holds 18 primary studies."]

    open(OUT_MD, "w").write("\n".join(L) + "\n")
    seen, ordered = set(), []
    for d in dois:
        if d and d.lower() not in seen:
            seen.add(d.lower()); ordered.append(d)
    open(OUT_DOI, "w").write("\n".join(ordered) + "\n")

    print(f"job A: {len(gate)} (primary {len(job_a_primary)}, held {len(job_a_held)})")
    print(f"job B: {len(PARAMETER_SET)} articles + {len(BOOKS)} books")
    print(f"total to procure: {len(gate) + len(PARAMETER_SET) + len(BOOKS)}  |  unique DOIs: {len(ordered)}")
    print(f"-> {os.path.relpath(OUT_MD, ROOT)}")
    print(f"-> {os.path.relpath(OUT_DOI, ROOT)}")


if __name__ == "__main__":
    main()
