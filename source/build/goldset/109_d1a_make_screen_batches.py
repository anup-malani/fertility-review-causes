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


def write_batches(rows, prefix, idmap, start_no=1):
    """Write blinded batches using SHORT POSITIONAL IDS, and record the mapping separately.

    THE IDS THE SCREENER SEES ARE `CAL001-07`, NOT A 44-CHARACTER HEX STRING. The first live run
    proved why: the screener has to echo every id back exactly, and one batch of two failed on a
    single mangled character out of forty ids. Validation caught it and the whole batch was
    discarded -- correct, and unaffordable at 390 batches, where that rate loses half the run to
    transcription rather than to judgement.

    It also closes a blinding leak that was there from the start. Production ids were real OpenAlex
    work ids, which are lookupable; a screen that can identify the record is not blind. The real id
    never leaves `idmap.json`, which is not sent to any model.
    """
    manifest = []
    for i in range(0, len(rows), BATCH_SIZE):
        n = i // BATCH_SIZE + start_no
        chunk = rows[i:i + BATCH_SIZE]
        batch = []
        for j, r in enumerate(chunk, start=1):
            short = f"{prefix.upper()}{n:03d}-{j:02d}"
            idmap[short] = r["screen_id"]
            batch.append({"paperId": short, "title": r["title"] or "",
                          "year": r.get("year"), "abstract": (r.get("abstract") or "")[:3500]})
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
    # Prefer the relabelled anchors when they exist. `112_` corrected labels the calibration
    # exposed as wrong; screening against the uncorrected set would keep scoring the screen against
    # known-bad answers. The original file is never modified, so the correction is reversible by
    # deleting one artifact.
    relab = LOGS / f"{SLUG}-tier-a-relabelled.json"
    tier_a_path = relab if relab.exists() else LOGS / f"{SLUG}-tier-a.json"
    tier_a = json.loads(tier_a_path.read_text())
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
        # SIX TIER-A ROWS CARRY `paperId: null`, AND NAMING THEM ALL "CAL-None" CORRUPTED THE FIRST
        # CALIBRATION. They collapsed to one id, so the answer key kept only the last of the six and
        # the verdict lookup kept only the last verdict -- silently dropping 3 empirical anchors and
        # one decoy from the scoring, which is why the report said "28 empirical anchors" when there
        # are 31. Validation passed throughout, because the verdict list still matched the batch's
        # id list position for position; duplicate ids are consistent with themselves.
        # D.3.b's step 75 asserted unique, nonblank paperIds and this script did not. Fall back to a
        # title hash so every record has a stable, distinct id.
        raw = r.get("paperId") or "T" + hashlib.sha256(
            cv.norm(r["title"]).encode()).hexdigest()[:10]
        sid = f"CAL-{raw}"
        calib.append({"screen_id": sid, "title": r["title"], "year": r.get("year"),
                      "abstract": abstract})
        key.append({"screen_id": sid, "title": r["title"], "role": r.get("role"),
                    "pair": r.get("pair"), "design_tier": r.get("design_tier"),
                    "provisional_cell": r.get("provisional_cell"),
                    "expect_route_away": r.get("role") == "DECOY",
                    "has_abstract": bool(abstract.strip())})

    # Enforced over BOTH sets, because a duplicate id is invisible downstream: the verdict list
    # still lines up with the batch position for position, so validation passes and only the
    # key-join quietly loses records.
    for label, rows in (("production", prod), ("calibration", calib)):
        ids = [r["screen_id"] for r in rows]
        if any(not i for i in ids) or len(ids) != len(set(ids)):
            dupes = {i for i in ids if ids.count(i) > 1}
            raise SystemExit(f"{label} ids must be unique and nonblank; "
                             f"{len(ids) - len(set(ids))} duplicates e.g. {sorted(dupes)[:5]}")

    rng = random.Random(SEED)
    rng.shuffle(prod)
    rng.shuffle(calib)

    (SCREEN / "RUBRIC.md").write_text(rubric_p.read_text())
    idmap = {}
    man = write_batches(calib, "calib", idmap) + write_batches(prod, "batch", idmap)
    (SCREEN / "idmap.json").write_text(json.dumps(idmap, indent=1))

    n_dec = sum(1 for k in key if k["expect_route_away"])
    committed = {
        "slug": SLUG, "stage": "blinded_title_abstract_screen_input",
        "corpus": corpus_p.name, "corpus_sha256": sha256(corpus_p),
        "prefilter": pref_p.name, "prefilter_sha256": sha256(pref_p),
        "rubric": rubric_p.name, "rubric_sha256": sha256(rubric_p),
        "tier_a_source": tier_a_path.name, "tier_a_sha256": sha256(tier_a_path),
        "seed": SEED, "batch_size": BATCH_SIZE,
        "production_records": len(prod), "calibration_records": len(calib),
        "production_batches": sum(1 for m in man if m["kind"] == "batch"),
        "calibration_batches": sum(1 for m in man if m["kind"] == "calib"),
        "calibration_decoys": n_dec,
        "records_with_abstract": sum(bool((r.get("abstract") or "").strip()) for r in prod),
        "calibration_abstracts_joined_from_corpus": joined,
        "blinded_fields": BLINDED,
        "id_scheme": "short positional (CAL001-07 / BATCH001-07); real ids only in idmap.json",
        "idmap": str((SCREEN / "idmap.json").relative_to(REPO)),
        "run_order": "calibration batches FIRST; production is not authorised until calibration is read",
        "coverage_verified": True, "manifest": man,
    }
    (LOGS / f"{SLUG}-screen-manifest.json").write_text(
        json.dumps(committed, indent=2, ensure_ascii=False))
    rev = {v: k for k, v in idmap.items()}
    for row in key:
        row["paperId"] = rev[row.pop("screen_id")]     # key on the short id the screener echoes
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
