#!/usr/bin/env python3
"""
180_a24_extraction_scaffold.py — A.24, stages 6 and 7. Full-text screen and extraction scaffold.

Builds the study-level extraction sheet from the RETRIEVED records, carrying the two fields the PI
rulings of 2026-08-24 added and pre-filling everything the pipeline already knows so the reader
codes judgements rather than re-typing metadata.

THE TWO FIELDS THE RULINGS ADDED, AND WHY EACH IS KEYED THE WAY IT IS:

  `era`  (Call 3 — pre-app online dating is in scope). Keyed on the study's EXPOSURE period, NOT its
         publication year, because a 2020 paper analysing 2009-2016 panel waves is measuring a
         pre-app and early-app world while a 2019 paper on Tinder is not. Values: `pre_app` (exposure
         ends ≤2012), `app_era` (exposure begins ≥2013), `spans` (crosses the discontinuity),
         `unclear`. The synthesis reports the app-era subset SEPARATELY rather than pooling across a
         technological break, so a mis-keyed era silently pools two different technologies.

  `shared_with`  (Call 2 — technology-diffusion records are shared with C.2.h). Set on every
         `SECONDARY_TECH_*` record. The working rule recorded at freeze is SHARED EVIDENCE BASE,
         SINGLE CLAIMANT ON MAGNITUDE: both chapters extract and grade the record, and synthesis
         names which chapter carries its contribution to the aggregate. The tag exists so synthesis
         can find them without re-searching, and so the double-count is visible if it ever happens.

WHAT THE FULL-TEXT SCREEN IS FOR HERE. The title/abstract screen routed on what an abstract shows.
Stage 6 asks a different question of each retrieved record: does it actually ESTIMATE the
relationship its abstract implies, and on what design? A qualitative interview study of twenty app
users and a nationally-representative panel both landed in `PRIMARY_APP_UNION` at D2 and they are not
the same evidence. `evidence_type` and `design` carry that separation; `fulltext_decision` records
whether the record survives into the graded set at all.

Output: extraction/{slug}-studies.csv     (scaffold; rows populated by reading)
        extraction/{slug}-effects.csv     (effect-level, one row per estimate)
"""
import csv, json, os, glob

SLUG = "dating-apps-union-formation-friction"
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
LOGS = os.path.join(ROOT, "literature", "search-logs")
EXTRACT = os.path.join(ROOT, "extraction")
SCREENED = os.path.join(LOGS, f"{SLUG}-screened.json")
FETCH = os.path.join(LOGS, f"{SLUG}-fetch-log.csv")
PDF_DIR = os.path.join(ROOT, "literature", "pdfs", SLUG)
OUT_STUDIES = os.path.join(EXTRACT, f"{SLUG}-studies.csv")
OUT_EFFECTS = os.path.join(EXTRACT, f"{SLUG}-effects.csv")

STUDY_COLS = ["study_id", "paper_id", "doi", "title", "authors", "year", "venue", "cell",
              "era", "shared_with", "country", "exposure_period_start", "exposure_period_end",
              "data_source", "population", "n_analytic", "exposure_measure", "outcome_family",
              "outcome_measure", "design", "evidence_type", "identification_source",
              "link_graded", "fulltext_decision", "fulltext_reason", "reverse_causality_tested",
              "pdf_filename", "extraction_status", "needs_pi", "notes"]

EFFECT_COLS = ["effect_id", "study_id", "paper_id", "outcome_family", "outcome_measure",
               "exposure_contrast", "subgroup", "coefficient", "se", "ci_low", "ci_high", "p_value",
               "units", "sign_vs_v5", "model", "adjusted_for", "era", "notes"]

CAUSAL = {"PRIMARY_APP_FERTILITY", "PRIMARY_APP_UNION",
          "SECONDARY_TECH_FERTILITY", "SECONDARY_TECH_UNION", "REVERSE_DIRECTION"}


def main():
    scr = {r["id"]: r for r in json.load(open(SCREENED))}
    got = [r["id"] for r in csv.DictReader(open(FETCH)) if r["fetch"] in ("OK", "CACHED")]
    order = {"PRIMARY_APP_FERTILITY": 0, "SECONDARY_TECH_FERTILITY": 1, "SECONDARY_TECH_UNION": 1,
             "PRIMARY_APP_UNION": 2, "REVERSE_DIRECTION": 3, "MECHANISM_CHOICE_FRICTION": 4,
             "EXPOSURE_SERIES": 5}
    got.sort(key=lambda w: (order.get(scr[w]["cell"], 9), scr[w]["d1_rank"]))

    if os.path.exists(OUT_STUDIES):
        print(f"{os.path.relpath(OUT_STUDIES, ROOT)} exists; not overwriting a populated sheet")
        return
    rows = []
    for w in got:
        m = scr[w]
        txt = glob.glob(os.path.join(PDF_DIR, w + "__*.txt"))
        rows.append({c: "" for c in STUDY_COLS} | {
            "paper_id": w, "doi": m.get("doi") or "", "title": m.get("title") or "",
            "year": m.get("year") or "", "venue": m.get("venue") or "", "cell": m["cell"],
            "shared_with": "C.2.h" if m["cell"].startswith("SECONDARY_TECH") else "",
            "link_graded": ("link2_tech_to_union" if m["cell"].endswith("UNION")
                            else "link3_imported_from_A7" if m["cell"].endswith("FERTILITY") else ""),
            "pdf_filename": os.path.basename(txt[0]).replace(".txt", ".pdf") if txt else "",
            "extraction_status": "not_started",
        })
    with open(OUT_STUDIES, "w", newline="") as fh:
        w_ = csv.DictWriter(fh, fieldnames=STUDY_COLS)
        w_.writeheader(); w_.writerows(rows)
    if not os.path.exists(OUT_EFFECTS):
        with open(OUT_EFFECTS, "w", newline="") as fh:
            csv.DictWriter(fh, fieldnames=EFFECT_COLS).writeheader()
    n_causal = sum(1 for r in rows if r["cell"] in CAUSAL)
    print(f"scaffolded {len(rows)} retrieved records ({n_causal} in causal cells)")
    print(f"-> {os.path.relpath(OUT_STUDIES, ROOT)}")
    print(f"-> {os.path.relpath(OUT_EFFECTS, ROOT)}")


if __name__ == "__main__":
    main()
