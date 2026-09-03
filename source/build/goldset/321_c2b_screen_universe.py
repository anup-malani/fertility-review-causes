#!/usr/bin/env python3
"""321 — build C.2.b's screen universe from the calibrated query set (TICK-079).

Reads the arms script 320 calibrated, pages every screened arm to exhaustion, deduplicates, and
emits the universe the title/abstract screen will read.

Four things this does that a plain pull does not.

**Counts per arm BEFORE deduplication.** An arm whose records all arrive via another arm is
REDUNDANT, not EMPTY, and those are different findings about the search
(`dedup-before-counting-hides-redundant-rung`: Unpaywall read as found=0 across 352 records because
the filter ran before the counter).

**Injects the anchors and the free seeds.** A query-built universe systematically omits the
hand-sourced records that defined it — on C.3.e the snowball universe lacked every hand-sourced
anchor including the study another chapter had routed there (`snowball-pools-omit-their-own-seeds`).
Anchors and the 130 free seeds from script 317 are injected explicitly and labelled, and how many
were ALREADY present is reported, because that number is a recall check on the query set.

**Withholds the gold flags.** The universe the screen reads carries no `is_gold`; the key is written
to a separate file. A screen that can see which rows are gold cannot measure its own sensitivity
(`blinded-screen-audits-the-anchors`, `a-positives-only-screen-cannot-measure-sensitivity`), and on
A.23 a blinded screen corrected three anchors the exposure audit had missed.

**Reconstructs abstracts.** OpenAlex returns an inverted index, and a screen with titles only cannot
apply scope §10's tags — `design-is-not-a-property-of-the-title`. Records arriving with no abstract
are counted and flagged, because they are a different screening problem, not a missing row.

Usage: python3 source/build/goldset/321_c2b_screen_universe.py
Outputs:
  literature/search-logs/child-cost-direct-screen-universe.json   what the screen reads (no gold)
  literature/search-logs/child-cost-direct-screen-gold.json       the withheld key
  literature/search-logs/child-cost-direct-screen-universe.md     generated summary
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "source" / "lib"))
from openalex import OpenAlex, POOL                                   # noqa: E402

LOGS = ROOT / "literature" / "search-logs"
KEY = next((l.split("=", 1)[1].strip() for l in (ROOT / ".env").read_text().splitlines()
            if l.startswith("OPENALEX_API_KEY=")), "")
MAILTO = "shravanh@uchicago.edu"
SELECT = ("id,doi,display_name,publication_year,type,authorships,primary_location,"
          "cited_by_count,abstract_inverted_index")
MATCHED = {"MATCH", "MATCH_STEM", "MATCH_BY_ID", "MATCH_BY_DOI", "MATCH_VERSION_TWIN"}


def abstract_of(rec):
    inv = rec.get("abstract_inverted_index")
    if not inv:
        return None
    pos = {}
    for word, idxs in inv.items():
        for i in idxs:
            pos[i] = word
    return " ".join(pos[i] for i in sorted(pos)) or None


def short(w):
    auths = [a.get("author", {}).get("display_name", "") for a in w.get("authorships", [])]
    return {"oa_id": (w.get("id") or "").rsplit("/", 1)[-1],
            "doi": w.get("doi"), "title": w.get("display_name"),
            "year": w.get("publication_year"), "type": w.get("type"),
            "venue": ((w.get("primary_location") or {}).get("source") or {}).get("display_name"),
            "first_author": auths[0] if auths else None, "n_authors": len(auths),
            "cited_by": w.get("cited_by_count"), "abstract": abstract_of(w)}


def main():
    qpath = LOGS / "child-cost-direct-production-query.json"
    if not qpath.exists():
        sys.exit(f"{qpath.name} is missing — run 320_c2b_production_query.py first. It is the "
                 "calibrated query set this universe is built from, and 320 refuses to write it if "
                 "any of its queries were refused, so its absence means the calibration has not "
                 "completed cleanly.")
    qlog = json.loads(qpath.read_text())
    not_screened = set(qlog.get("arms_not_screened") or [])
    arms = [a for a in qlog["arms"] if a["name"] not in not_screened]
    print(f"{len(arms)} screened arms (excluded: {', '.join(sorted(not_screened)) or 'none'})\n")

    oa = OpenAlex(KEY, MAILTO, LOGS / ".cache" / "c2b-screen-pages.json")
    universe, per_arm, errors = {}, [], []
    for a in arms:
        recs, err = oa.page_all(a["query"], SELECT)
        if err:
            errors.append({"arm": a["name"], "error": err})
            print(f"  {a['name']:20} ERROR {err[:110]}")
            continue
        new = 0
        for w in recs:
            r = short(w)
            if not r["oa_id"]:
                continue
            if r["oa_id"] in universe:
                universe[r["oa_id"]]["arms"].append(a["name"])
            else:
                universe[r["oa_id"]] = {**r, "arms": [a["name"]], "provenance": ["query"]}
                new += 1
        per_arm.append({"arm": a["name"], "declared_frame": a["frame"], "pulled": len(recs),
                        "new_after_dedup": new})
        print(f"  {a['name']:20} declared {a['frame']:>5}  pulled {len(recs):>5}  "
              f"new {new:>5}  {'REDUNDANT' if recs and new == 0 else ''}")

    if errors:
        sys.exit(f"\n*** {len(errors)} arms could not be paged. NOTHING WAS WRITTEN.\n"
                 "A partly-paged universe silently under-counts every downstream number. "
                 "Pages already bought are cached, so a re-run resumes rather than re-paying.\n"
                 + "\n".join(f"  {e['arm']}: {e['error'][:160]}" for e in errors))

    # ---------------------------------------------------------------- injection
    anchors = json.loads((LOGS / "child-cost-direct-cold-start-anchors.json").read_text())
    gold_ids, already, injected = {}, 0, 0
    for a in anchors:
        if a["verdict"] not in MATCHED:
            continue
        tc = a["top_candidate"]
        oid = (tc.get("oa_id") or "").rsplit("/", 1)[-1]
        if not oid:
            continue
        is_gold = a.get("outcome_is_fertility", True) and a["arm"] not in not_screened
        gold_ids[oid] = {"arm": a["arm"], "source": a["source"], "is_gold": is_gold,
                         "outcome_is_fertility": a.get("outcome_is_fertility", True)}
        if oid in universe:
            already += 1
            gold_ids[oid]["found_by_query"] = True
            universe[oid]["provenance"].append("anchor")
        else:
            injected += 1
            gold_ids[oid]["found_by_query"] = False
            universe[oid] = {"oa_id": oid, "doi": tc.get("doi"), "title": tc.get("title"),
                             "year": tc.get("year"), "type": tc.get("type"),
                             "venue": tc.get("venue"), "first_author": tc.get("authors_first"),
                             "n_authors": None, "cited_by": tc.get("cited_by"), "abstract": None,
                             "arms": [], "provenance": ["anchor_injected"]}

    def norm_doi(d):
        if not d:
            return None
        d = d.strip().lower()
        for pre in ("https://doi.org/", "http://doi.org/", "doi:"):
            if d.startswith(pre):
                d = d[len(pre):]
        return d or None

    by_doi = {}
    for r in universe.values():
        nd = norm_doi(r.get("doi"))
        if nd:
            by_doi[nd] = r["oa_id"]

    seeds = json.loads((LOGS / "child-cost-direct-free-seeds.json").read_text())["records"]
    seed_present = seed_injected = seed_unmatchable = 0
    for sd in seeds:
        ident = (sd.get("id") or "")
        oid = ident if ident.startswith("W") else None
        nd = norm_doi(ident) if ident.startswith("10.") else None
        hit = oid if (oid and oid in universe) else (by_doi.get(nd) if nd else None)
        if hit:
            seed_present += 1
            universe[hit]["provenance"].append("free_seed")
            continue
        key = oid or (f"doi:{nd}" if nd else None)
        if not key:
            seed_unmatchable += 1     # no id and no DOI: cannot be placed, and is COUNTED not lost
            continue
        seed_injected += 1
        universe[key] = {"oa_id": oid or "", "doi": nd, "title": sd["title"],
                         "year": sd.get("year"), "type": None, "venue": None,
                         "first_author": None, "n_authors": None, "cited_by": None,
                         "abstract": None, "arms": [], "provenance": ["free_seed_injected"]}

    rows = sorted(universe.values(), key=lambda r: (-(r.get("cited_by") or 0), r["oa_id"]))
    no_abstract = sum(1 for r in rows if not r.get("abstract"))
    gold_n = sum(1 for g in gold_ids.values() if g["is_gold"])
    gold_found = sum(1 for g in gold_ids.values() if g["is_gold"] and g.get("found_by_query"))

    # What the screen reads. No gold flags, no provenance that reveals them.
    screen_rows = [{k: v for k, v in r.items() if k != "provenance"} for r in rows]
    (LOGS / "child-cost-direct-screen-universe.json").write_text(
        json.dumps({"n": len(screen_rows), "arms": [a["name"] for a in arms],
                    "records": screen_rows}, indent=1) + "\n")
    (LOGS / "child-cost-direct-screen-gold.json").write_text(
        json.dumps({"note": "WITHHELD from the screen. Merge only when scoring sensitivity.",
                    "gold": gold_ids,
                    "provenance": {r["oa_id"]: r["provenance"] for r in rows}}, indent=1) + "\n")

    L = ["# C.2.b screen universe", "",
         "Generated by `source/build/goldset/321_c2b_screen_universe.py`. Do not edit by hand.", "",
         f"**{len(rows)} records** across {len(arms)} screened arms.", "",
         "## Per arm, before deduplication", "",
         "An arm whose records all arrive via another arm is REDUNDANT, which is a different finding "
         "from EMPTY. Counting only after the dedup hides it "
         "(`dedup-before-counting-hides-redundant-rung`).", "",
         "| arm | declared frame | pulled | new after dedup |", "|---|---|---|---|"]
    L += [f"| `{p['arm']}` | {p['declared_frame']} | {p['pulled']} | {p['new_after_dedup']} |"
          for p in per_arm]
    L += ["", "## Injection", "",
          "A query-built universe omits the hand-sourced records that defined it. How many anchors "
          "were **already present** is a recall check on the query set; how many had to be injected "
          "is the size of the gap.", "",
          f"- anchors already in the pull: **{already}**; injected: **{injected}**",
          f"- free seeds already in the pull: **{seed_present}**; injected: "
          f"**{seed_injected}**",
          f"- **gold found by the query itself: {gold_found}/{gold_n}** — this is the recall "
          "check that matters. The rest are present only because they were injected, and an "
          "injected anchor tests nothing about the query.",
          f"- free seeds unmatchable (no id and no DOI): {seed_unmatchable}", "",
          "## Abstracts", "",
          f"**{no_abstract} of {len(rows)}** records carry no abstract. A title-only row cannot "
          "support scope §10's tags — `design-is-not-a-property-of-the-title` — so these are a "
          "separate screening problem and are flagged rather than treated as ordinary rows.", "",
          "## Blinding", "",
          "`child-cost-direct-screen-universe.json` carries **no** gold flags and no provenance. The "
          "key is in `child-cost-direct-screen-gold.json` and is merged only when scoring "
          "sensitivity. A screen that can see which rows are gold cannot measure its own "
          "(`a-positives-only-screen-cannot-measure-sensitivity`).", ""]
    (LOGS / "child-cost-direct-screen-universe.md").write_text("\n".join(L))
    print(f"\nuniverse {len(rows)} records; anchors {already} present / {injected} injected; "
          f"seeds {seed_present} present / {seed_injected} injected / {seed_unmatchable} "
          f"unmatchable; GOLD FOUND BY QUERY {gold_found}/{gold_n}; no abstract {no_abstract}")
    print(f"requests: {POOL['key']} keyed, {POOL['polite']} keyless, {POOL['refused']} refused; "
          f"pages {oa.stats['hit']} cached / {oa.stats['miss']} fetched")


main()
