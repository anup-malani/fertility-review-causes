#!/usr/bin/env python3
"""353 — build C.3.d's screen universe from the calibrated query set (TICK-083).

Direct port of C.2.f's 340 (itself C.2.b's 321). Reads the arms 352 calibrated, pages every screened
arm to exhaustion, deduplicates, and emits the universe the title/abstract screen reads. The
properties that make it more than a pull are carried over unchanged:

**Counts per arm BEFORE deduplication** — an arm whose records all arrive via another arm is
REDUNDANT, not EMPTY, and those are different findings (`dedup-before-counting-hides-redundant-rung`).

**Injects the anchors and the free seeds** — a query-built universe systematically omits the
hand-sourced records that defined it (`snowball-pools-omit-their-own-seeds`). The 82 resolved
anchors from 350 and the 515 free seeds from 348 are injected and labelled, and how many were
ALREADY present is reported, because that is the recall check on the query set.

**Withholds the gold flags** — the universe carries no `is_gold`; the key goes to a separate file. A
screen that can see which rows are gold cannot measure its own sensitivity
(`blinded-screen-audits-the-anchors`, `a-positives-only-screen-cannot-measure-sensitivity`).

**Reconstructs abstracts** from OpenAlex's inverted index, because a screen with titles only cannot
apply scope §10's tags (`design-is-not-a-property-of-the-title`).

TWO PORTED DEFECTS FIXED HERE, both the same shape as the two 352 hit.

1. `is_gold` was `a.get("outcome_is_fertility", True) and ...`. Script 349 writes that field as
   `None` on all 65 controls, meaning NOT KNOWN — and `None` is falsy, so every control would have
   been marked not-gold and the recall check would have run on 17 anchors while claiming 82.
   `optional-field-gate-disengages`.
2. The C.2.f expression also tests `a["arm"] not in not_screened`, where `not_screened` holds ARM
   NAMES and `a["arm"]` holds the anchor arm VALUES those arms target. On C.2.f the two vocabularies
   coincided; here they do not, so the test would never fire. Gold is mapped through the arm
   definitions instead.

WHAT GOLD MEANS HERE, and it follows scope §2. Both FORWARD and BACKWARD anchors are legitimate
targets of the screen — backward is link 2, retrieved into `QQ_SUBSTITUTION` rather than discarded —
so an anchor is gold if its arm value is targeted by any SCREENED arm. The `c2e-boundary` arm is not
screened (it is C.2.e's chapter, scope §8 Wall 2), so nothing is gold on account of it.

THE ARM TO WATCH IS `forward-shock`. Scope §7 rows 1-6 and 346's channel-2 measurement say the
registered forward estimand lives there; 352 calibrated it at 58% of reachable, the weakest of the
four. Its pre-dedup count against its post-dedup contribution says whether it is a genuine channel
or a relabelling of the theory arm.
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
    # TWO COUNTERS PER RUNG. The ported version returned one combined (tried, filled) pair, so a
    # rung that attempted 400 and filled 0 was indistinguishable from a rung that was never
    # attempted at all -- `rung-found-is-not-rung-fetched`, where PMC and Unpaywall read as dead at
    # 0 fetches while having found 27 and 65 URLs.
    rung = {"by_id": {"tried": len(need), "filled": 0, "refused": 0},
            "by_doi": {"tried": len(by_doi), "filled": 0, "refused": 0},
            "no_route": 0}
    rung["no_route"] = sum(1 for r in universe.values()
                           if not (r.get("abstract") or "").strip()
                           and not r.get("oa_id") and not r.get("doi"))
    filled = 0
    ids = [r["oa_id"].rsplit("/", 1)[-1] for r in need]
    for i in range(0, len(ids), 50):
        chunk = ids[i:i + 50]
        page, err = oa.get({"filter": "openalex:" + "|".join(chunk),
                            "select": "id,abstract_inverted_index", "per_page": 50})
        if err:                                      # a refusal is never an empty abstract
            rung["by_id"]["refused"] += len(chunk)
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
                    rung["by_id"]["filled"] += 1

    for i in range(0, len(by_doi), 50):
        chunk = by_doi[i:i + 50]
        dois = "|".join("https://doi.org/" + c["doi"] for c in chunk)
        page, err = oa.get({"filter": "doi:" + dois,
                            "select": "id,doi,abstract_inverted_index", "per_page": 50})
        if err:
            rung["by_doi"]["refused"] += len(chunk)
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
                    rung["by_doi"]["filled"] += 1
    return len(need) + len(by_doi), filled, rung


def main():
    qpath = LOGS / "quantity-quality-tradeoff-production-query.json"
    if not qpath.exists():
        sys.exit(f"{qpath.name} is missing — run 352_c3d_production_query.py first. It is the "
                 "calibrated query set this universe is built from, and 352 refuses to write it if "
                 "any of its queries were refused, so its absence means the calibration has not "
                 "completed cleanly.")
    qlog = json.loads(qpath.read_text())
    not_screened = set(qlog.get("arms_not_screened") or [])
    arms = [a for a in qlog["arms"] if a["name"] not in not_screened]
    print(f"{len(arms)} screened arms (excluded: {', '.join(sorted(not_screened)) or 'none'})\n")

    oa = OpenAlex(KEY, MAILTO, LOGS / ".cache" / "c3d-screen-pages.json")
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
    screened_targets = {t for a in arms for t in a["targets"]}
    anchors = json.loads((LOGS / "quantity-quality-tradeoff-cold-start-anchors.json").read_text())
    gold_ids, already, injected = {}, 0, 0
    for a in anchors:
        if a["verdict"] not in MATCHED:
            continue
        tc = a["top_candidate"]
        oid = (tc.get("oa_id") or "").rsplit("/", 1)[-1]
        if not oid:
            continue
        # Gold = an anchor a SCREENED arm targets. Both directions count (scope §2): backward is
        # link 2, retrieved into its own cell, not discarded. See the header for the two ported
        # defects this replaces -- None-is-falsy on the 65 controls, and comparing arm NAMES against
        # anchor arm VALUES.
        is_gold = a["arm"] in screened_targets
        gold_ids[oid] = {"arm": a["arm"], "source": a["source"], "is_gold": is_gold,
                         "direction": a.get("direction"),
                         "outcome_is_fertility": a.get("outcome_is_fertility")}
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

    seeds = json.loads((LOGS / "quantity-quality-tradeoff-free-seeds.json").read_text())["records"]
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

    tried, filled, rung = enrich_abstracts(universe, oa)
    print(f"  abstract enrichment: {filled}/{tried} injected records filled")
    for name in ("by_id", "by_doi"):
        r_ = rung[name]
        print(f"    rung {name:7} tried {r_['tried']:>4}  filled {r_['filled']:>4}  "
              f"refused {r_['refused']:>4}"
              + ("   <- attempted and returned nothing" if r_["tried"] and not r_["filled"]
                 and not r_["refused"] else ""))
    if rung["no_route"]:
        print(f"    {rung['no_route']} records have NO ROUTE (no OpenAlex id and no DOI) — they "
              "cannot be enriched at all and are title-only by construction, not by failure")
    if tried and filled == 0:
        print("  WARNING: enrichment filled NOTHING while refusing nothing — that is an id-match "
              "bug, not an absence of abstracts. Do not screen on this universe.", file=sys.stderr)

    rows = sorted(universe.values(), key=lambda r: (-(r.get("cited_by") or 0), r["oa_id"]))
    no_abstract = sum(1 for r in rows if not r.get("abstract"))
    gold_n = sum(1 for g in gold_ids.values() if g["is_gold"])
    gold_found = sum(1 for g in gold_ids.values() if g["is_gold"] and g.get("found_by_query"))
    by_dir = {}
    for g in gold_ids.values():
        if not g["is_gold"]:
            continue
        d = by_dir.setdefault(g.get("direction") or "UNKNOWN", {"n": 0, "found": 0})
        d["n"] += 1
        d["found"] += 1 if g.get("found_by_query") else 0
    print("  gold found by the query, by direction (scope §2):")
    for d in sorted(by_dir):
        print(f"    {d:9} {by_dir[d]['found']}/{by_dir[d]['n']}")

    # What the screen reads. No gold flags, no provenance that reveals them.
    screen_rows = [{k: v for k, v in r.items() if k != "provenance"} for r in rows]
    (LOGS / "quantity-quality-tradeoff-screen-universe.json").write_text(
        json.dumps({"n": len(screen_rows), "arms": [a["name"] for a in arms],
                    "records": screen_rows}, indent=1) + "\n")
    (LOGS / "quantity-quality-tradeoff-screen-gold.json").write_text(
        json.dumps({"note": "WITHHELD from the screen. Merge only when scoring sensitivity.",
                    "gold": gold_ids,
                    "provenance": {r["oa_id"]: r["provenance"] for r in rows}}, indent=1) + "\n")

    L = ["# C.3.d screen universe", "",
         "Generated by `source/build/goldset/353_c3d_screen_universe.py`. Do not edit by hand.", "",
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
          "### Gold found by the query, by direction (scope §2)", "",
          "| direction | found by query | gold |", "|---|---|---|"]
    L += [f"| `{d}` | {by_dir[d]['found']} | {by_dir[d]['n']} |" for d in sorted(by_dir)]
    L += ["",
          "## Abstracts", "",
          f"**{no_abstract} of {len(rows)}** records carry no abstract. A title-only row cannot "
          "support scope §10's tags — `design-is-not-a-property-of-the-title` — so these are a "
          "separate screening problem and are flagged rather than treated as ordinary rows.", "",
          "## Blinding", "",
          "`quantity-quality-tradeoff-screen-universe.json` carries **no** gold flags and no provenance. The "
          "key is in `quantity-quality-tradeoff-screen-gold.json` and is merged only when scoring "
          "sensitivity. A screen that can see which rows are gold cannot measure its own "
          "(`a-positives-only-screen-cannot-measure-sensitivity`).", ""]
    (LOGS / "quantity-quality-tradeoff-screen-universe.md").write_text("\n".join(L))
    print(f"\nuniverse {len(rows)} records; anchors {already} present / {injected} injected; "
          f"seeds {seed_present} present / {seed_injected} injected / {seed_unmatchable} "
          f"unmatchable; GOLD FOUND BY QUERY {gold_found}/{gold_n}; no abstract {no_abstract}")
    print(f"requests: {POOL['key']} keyed, {POOL['polite']} keyless, {POOL['refused']} refused; "
          f"pages {oa.stats['hit']} cached / {oa.stats['miss']} fetched")


main()
