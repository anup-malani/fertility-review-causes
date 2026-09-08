#!/usr/bin/env python3
"""340 — build C.2.f's screen universe from the calibrated query set (TICK-081).

Direct port of C.2.b's 321. Reads the arms script 337 calibrated at 92% union primary recall, pages
every screened arm to exhaustion, deduplicates, and emits the universe the title/abstract screen
reads. The four properties that make it more than a pull are carried over unchanged:

**Counts per arm BEFORE deduplication** — an arm whose records all arrive via another arm is
REDUNDANT, not EMPTY, and those are different findings (`dedup-before-counting-hides-redundant-rung`).

**Injects the anchors and the free seeds** — a query-built universe systematically omits the
hand-sourced records that defined it (`snowball-pools-omit-their-own-seeds`). The 35 candidates from
339 and the 393 free seeds from 335 are injected and labelled, and how many were ALREADY present is
reported, because that is a recall check on the query set.

**Withholds the gold flags** — the universe carries no `is_gold`; the key goes to a separate file. A
screen that can see which rows are gold cannot measure its own sensitivity
(`blinded-screen-audits-the-anchors`, `a-positives-only-screen-cannot-measure-sensitivity`).

**Reconstructs abstracts** from OpenAlex's inverted index, because a screen with titles only cannot
apply scope §10's tags (`design-is-not-a-property-of-the-title`).

Two things specific to C.2.f.

**`education-competition` is the arm to watch.** Scope §4A: it is the recovered second channel and
the only arm carrying a named policy shock (China 2021, Korea 1980). Its pre-dedup count against its
post-dedup contribution says whether it is a genuine channel or a relabelling of the dispersion arm.

**`positional-canon` and `link1-investment` contribute rows they cannot recall.** Their anchors are
not retrievable by vocabulary (scope §4A), so those arms are in the universe for their FRAME, while
their anchors arrive only through injection. That asymmetry is reported rather than smoothed over.
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



def enrich_abstracts(universe, oa):
    """Fetch abstracts for INJECTED records, which arrive with title and DOI only.

    Without this the anchors and free seeds enter the screen title-only, and a title-only screen
    cannot apply scope §10's tags -- `design-is-not-a-property-of-the-title`, where A.23 carried a
    paper as an administrative allocation through search, screen and priority retrieval and it was
    IPTW. These are also the records that matter most: `tier-a-anchors-are-studies` (on D.2.d,
    reporting screen output as the evidence base dropped the hand-sourced seeds, 2 against 9).

    The first version of this script did not do this, and 350 of the universe's 550 missing
    abstracts were the injected records at a 100% miss rate against 19-26% for the query pull.
    """
    need = [r for r in universe.values()
            if not (r.get("abstract") or "").strip() and r.get("oa_id")]
    # Rung 2: injected records carrying a DOI but no OpenAlex id were never tried by the id rung.
    # `rung-found-is-not-rung-fetched` -- count what each rung attempts, not only what it returns.
    by_doi = [r for r in universe.values()
              if not (r.get("abstract") or "").strip() and not r.get("oa_id") and r.get("doi")]
    filled = 0
    ids = [r["oa_id"].rsplit("/", 1)[-1] for r in need]
    for i in range(0, len(ids), 50):
        chunk = ids[i:i + 50]
        page, err = oa.get({"filter": "openalex:" + "|".join(chunk),
                            "select": "id,abstract_inverted_index", "per_page": 50})
        if err:                                      # a refusal is never an empty abstract
            print(f"  enrich: REFUSED on chunk {i // 50} ({err}) — "
                  f"{len(chunk)} records keep their missing abstract", file=sys.stderr)
            continue
        # Match on the BARE id. Injected records store "W2048002868" while the query pull and the
        # API both return "https://openalex.org/W2048002868", so a raw lookup matched nothing and
        # reported 0/232 filled with zero refusals -- a silent zero from an id-format mismatch.
        got = {w["id"].rsplit("/", 1)[-1]: w for w in page.get("results", [])}
        for r in need:
            w = got.get(r["oa_id"].rsplit("/", 1)[-1])
            if w:
                a = abstract_of(w)
                if a:
                    r["abstract"] = a
                    filled += 1

    for i in range(0, len(by_doi), 50):
        chunk = by_doi[i:i + 50]
        dois = "|".join("https://doi.org/" + c["doi"] for c in chunk)
        page, err = oa.get({"filter": "doi:" + dois,
                            "select": "id,doi,abstract_inverted_index", "per_page": 50})
        if err:
            print(f"  enrich(doi): REFUSED on chunk {i // 50} ({err})", file=sys.stderr)
            continue
        got = {(w.get("doi") or "").replace("https://doi.org/", "").lower(): w
               for w in page.get("results", [])}
        for r in chunk:
            w = got.get(r["doi"].lower())
            if w:
                if not r.get("oa_id"):
                    r["oa_id"] = w["id"].rsplit("/", 1)[-1]
                a = abstract_of(w)
                if a:
                    r["abstract"] = a
                    filled += 1
    return len(need) + len(by_doi), filled


def main():
    qpath = LOGS / "rising-inequality-and-status-competition-production-query.json"
    if not qpath.exists():
        sys.exit(f"{qpath.name} is missing — run 337_c2f_production_query.py first. It is the "
                 "calibrated query set this universe is built from, and 320 refuses to write it if "
                 "any of its queries were refused, so its absence means the calibration has not "
                 "completed cleanly.")
    qlog = json.loads(qpath.read_text())
    not_screened = set(qlog.get("arms_not_screened") or [])
    arms = [a for a in qlog["arms"] if a["name"] not in not_screened]
    print(f"{len(arms)} screened arms (excluded: {', '.join(sorted(not_screened)) or 'none'})\n")

    oa = OpenAlex(KEY, MAILTO, LOGS / ".cache" / "c2f-screen-pages.json")
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
    anchors = json.loads((LOGS / "rising-inequality-and-status-competition-cold-start-anchors.json").read_text())
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

    seeds = json.loads((LOGS / "rising-inequality-and-status-competition-free-seeds.json").read_text())["records"]
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

    tried, filled = enrich_abstracts(universe, oa)
    print(f"  abstract enrichment: {filled}/{tried} injected records filled")
    if tried and filled == 0:
        print("  WARNING: enrichment filled NOTHING while refusing nothing — that is an id-match "
              "bug, not an absence of abstracts. Do not screen on this universe.", file=sys.stderr)

    rows = sorted(universe.values(), key=lambda r: (-(r.get("cited_by") or 0), r["oa_id"]))
    no_abstract = sum(1 for r in rows if not r.get("abstract"))
    gold_n = sum(1 for g in gold_ids.values() if g["is_gold"])
    gold_found = sum(1 for g in gold_ids.values() if g["is_gold"] and g.get("found_by_query"))

    # What the screen reads. No gold flags, no provenance that reveals them.
    screen_rows = [{k: v for k, v in r.items() if k != "provenance"} for r in rows]
    (LOGS / "rising-inequality-and-status-competition-screen-universe.json").write_text(
        json.dumps({"n": len(screen_rows), "arms": [a["name"] for a in arms],
                    "records": screen_rows}, indent=1) + "\n")
    (LOGS / "rising-inequality-and-status-competition-screen-gold.json").write_text(
        json.dumps({"note": "WITHHELD from the screen. Merge only when scoring sensitivity.",
                    "gold": gold_ids,
                    "provenance": {r["oa_id"]: r["provenance"] for r in rows}}, indent=1) + "\n")

    L = ["# C.2.f screen universe", "",
         "Generated by `source/build/goldset/340_c2f_screen_universe.py`. Do not edit by hand.", "",
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
          "`rising-inequality-and-status-competition-screen-universe.json` carries **no** gold flags and no provenance. The "
          "key is in `rising-inequality-and-status-competition-screen-gold.json` and is merged only when scoring "
          "sensitivity. A screen that can see which rows are gold cannot measure its own "
          "(`a-positives-only-screen-cannot-measure-sensitivity`).", ""]
    (LOGS / "rising-inequality-and-status-competition-screen-universe.md").write_text("\n".join(L))
    print(f"\nuniverse {len(rows)} records; anchors {already} present / {injected} injected; "
          f"seeds {seed_present} present / {seed_injected} injected / {seed_unmatchable} "
          f"unmatchable; GOLD FOUND BY QUERY {gold_found}/{gold_n}; no abstract {no_abstract}")
    print(f"requests: {POOL['key']} keyed, {POOL['polite']} keyless, {POOL['refused']} refused; "
          f"pages {oa.stats['hit']} cached / {oa.stats['miss']} fetched")


main()
