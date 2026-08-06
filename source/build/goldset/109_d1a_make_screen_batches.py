#!/usr/bin/env python3
r"""
109_d1a_make_screen_batches.py — D.1.a. Blind the screening corpus and cut it into batches.

Mirrors B.1 step 66 and D.3.b step 75. What differs is the source and the calibration.

SOURCE IS THE PRE-FILTERED v2 CORPUS. `104_` already removed the clinical/veterinary collision and
the book reviews mechanically, so the paid screen is not spent reading obstetrics abstracts. The
queue is an id list; titles and abstracts are joined from the v2 corpus, which stays the single
record of what the pull returned.

THE RUBRIC IS READ, NOT EMBEDDED. D.3.b carried its rubric as a string literal inside its batching
script, which makes the script and the committed rubric two sources of truth that can drift. D.1.a's
rubric is already a committed artifact, so it is read from disk and its SHA-256 goes in the manifest.
The screen is then pinned to a specific rubric version rather than to whatever was pasted into a
script.

CALIBRATION RUNS FIRST AND IT IS PRE-LABELLED. 15,586 records is roughly 390 model invocations, and
authorising that before knowing whether the screen works is how a chapter buys 390 batches of
confident nonsense. Tier A carries 48 hand-built anchors with known `role`, `pair` and `design_tier`
-- including **10 DECOYS** chosen to sit exactly on the boundaries the rubric says will be tested:
gender-role attitudes (D.2.a), mass-media exposure (D.1.b / A.20), and religion against
*contraceptive use* rather than fertility (OFF_OUTCOME). A screen that admits those is
mis-calibrated in the direction that matters, and it costs two batches to find out.

The answer key is written to a SEPARATE committed file. The batches contain no labels, no roles, no
DOIs, no authors, no venues, no citation counts and no cluster provenance -- the screen must not be
able to infer anchor status, because Recall measured against a gold set the screen can recognise is
not a measurement.

CALIBRATION RECORDS CARRY THE SAME INFORMATION PRODUCTION WILL. Only 14 of the 48 Tier-A rows store
an abstract, but the production corpus holds abstracts for ~69% of records. Calibrating on
title-only records would test the screen on a harder input than it will actually face and would push
almost everything to UNCERTAIN by construction. Tier-A rows are therefore joined to the v2 corpus by
DOI and normalised title to pick up the abstract the screen would really see.

Usage:  python3 109_d1a_make_screen_batches.py
Output: temp/screen/{slug}/calib_NNN.json, batch_NNN.json, RUBRIC.md   (gitignored)
        literature/search-logs/{slug}-screen-manifest.json
        literature/search-logs/{slug}-screen-calibration-key.json
"""
import hashlib, json, random, sys
from pathlib import Path
import importlib.util

SLUG = "postmaterialism-individualism-secularization"
SEED = 621                    # D.1.a / TICK-062
BATCH_SIZE = 40
HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
LOGS = REPO / "literature" / "search-logs"
SCREEN = REPO / "temp" / "screen" / SLUG
SCREEN.mkdir(parents=True, exist_ok=True)

_spec = importlib.util.spec_from_file_location("cv", str(HERE / "101_d1a_cv_breadth.py"))
cv = importlib.util.module_from_spec(_spec)
sys.modules["cv"] = cv
_spec.loader.exec_module(cv)

# Everything the screen must not see. Anchor status must be uninferable or Recall(gold) is theatre.
BLINDED = ["doi", "authors", "venue", "cited_by_count", "clusters", "openalex_id",
           "role", "pair", "design_tier", "provisional_cell", "resolution", "title_key",
           "snowball_round", "seen_from", "relevance_reason"]


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_batches(rows, prefix, start_no=1):
    manifest = []
    for i in range(0, len(rows), BATCH_SIZE):
        n = i // BATCH_SIZE + start_no
        batch = [{"paperId": r["screen_id"], "title": r["title"] or "",
                  "year": r.get("year"), "abstract": (r.get("abstract") or "")[:3500]}
                 for r in rows[i:i + BATCH_SIZE]]
        p = SCREEN / f"{prefix}_{n:03d}.json"
        p.write_text(json.dumps(batch, indent=2, ensure_ascii=False))
        manifest.append({"batch": n, "kind": prefix, "n": len(batch),
                         "input": str(p.relative_to(REPO)), "input_sha256": sha256(p),
                         "output": str((SCREEN / f"verdict_{prefix}_{n:03d}.json")
                                       .relative_to(REPO))})
    return manifest


def main():
    corpus_p = LOGS / f"{SLUG}-live-corpus-v2.json"
    pref_p = LOGS / f"{SLUG}-prefilter-v2.json"
    rubric_p = LOGS / f"{SLUG}-screen-rubric.md"
    corpus = json.loads(corpus_p.read_text())
    if corpus.get("incomplete_clusters"):
        raise SystemExit("v2 corpus is incomplete; screening it would screen the wrong question")
    pref = json.loads(pref_p.read_text())
    if not pref.get("source_corpus_complete"):
        raise SystemExit("pre-filter ran on an incomplete corpus")

    by_id = {r["openalex_id"]: r for r in corpus["records"]}
    queue_ids = pref["screening_queue_ids"]
    missing = [i for i in queue_ids if i not in by_id]
    if missing:
        raise SystemExit(f"{len(missing)} queued ids absent from the corpus")

    prod = []
    for i in queue_ids:
        r = by_id[i]
        prod.append({"screen_id": i, "title": r.get("title"), "year": r.get("year"),
                     "abstract": r.get("abstract")})

    # ---- calibration -------------------------------------------------------------------------
    tier_a = json.loads((LOGS / f"{SLUG}-tier-a.json").read_text())
    by_doi = {r["doi"]: r for r in corpus["records"] if r.get("doi")}
    by_title = {}
    for r in corpus["records"]:
        if r.get("title"):
            by_title.setdefault(cv.norm(r["title"])[:70], r)
    calib, key, joined = [], [], 0
    for r in tier_a:
        if not r.get("title"):
            continue
        hit = by_doi.get(r.get("doi")) or by_title.get(cv.norm(r["title"])[:70])
        abstract = (r.get("abstract") or "") or ((hit or {}).get("abstract") or "")
        if not (r.get("abstract") or "").strip() and (hit or {}).get("abstract"):
            joined += 1
        sid = f"CAL-{r['paperId']}"
        calib.append({"screen_id": sid, "title": r["title"], "year": r.get("year"),
                      "abstract": abstract})
        key.append({"paperId": sid, "title": r["title"], "role": r.get("role"),
                    "pair": r.get("pair"), "design_tier": r.get("design_tier"),
                    "provisional_cell": r.get("provisional_cell"),
                    "expect_route_away": r.get("role") == "DECOY",
                    "has_abstract": bool(abstract.strip())})

    rng = random.Random(SEED)
    rng.shuffle(prod)
    rng.shuffle(calib)

    (SCREEN / "RUBRIC.md").write_text(rubric_p.read_text())
    man = write_batches(calib, "calib") + write_batches(prod, "batch")

    n_dec = sum(1 for k in key if k["expect_route_away"])
    committed = {
        "slug": SLUG, "stage": "blinded_title_abstract_screen_input",
        "corpus": corpus_p.name, "corpus_sha256": sha256(corpus_p),
        "prefilter": pref_p.name, "prefilter_sha256": sha256(pref_p),
        "rubric": rubric_p.name, "rubric_sha256": sha256(rubric_p),
        "seed": SEED, "batch_size": BATCH_SIZE,
        "production_records": len(prod), "calibration_records": len(calib),
        "production_batches": sum(1 for m in man if m["kind"] == "batch"),
        "calibration_batches": sum(1 for m in man if m["kind"] == "calib"),
        "calibration_decoys": n_dec,
        "records_with_abstract": sum(bool((r.get("abstract") or "").strip()) for r in prod),
        "calibration_abstracts_joined_from_corpus": joined,
        "blinded_fields": BLINDED,
        "run_order": "calibration batches FIRST; production is not authorised until calibration is read",
        "coverage_verified": True, "manifest": man,
    }
    (LOGS / f"{SLUG}-screen-manifest.json").write_text(
        json.dumps(committed, indent=2, ensure_ascii=False))
    (LOGS / f"{SLUG}-screen-calibration-key.json").write_text(
        json.dumps(key, indent=2, ensure_ascii=False))

    pct = 100 * committed["records_with_abstract"] / len(prod)
    print(f"production {len(prod):,} records -> {committed['production_batches']} batches of "
          f"<= {BATCH_SIZE} ({pct:.0f}% carry an abstract)", file=sys.stderr)
    print(f"calibration {len(calib)} records -> {committed['calibration_batches']} batches, "
          f"{n_dec} decoys, {joined} abstracts joined from the corpus", file=sys.stderr)
    print(f"wrote manifest and calibration key to literature/search-logs/", file=sys.stderr)


if __name__ == "__main__":
    main()
