#!/usr/bin/env python3
"""
215 — A.23 targeted anchor pulls.

TICK-075. 214's broad families were sorted by citation count and returned mostly
high-citation off-topic work: the pre-launch family's top hits are papers on
adolescent cannabis use and obesity, and the proximity family is contaminated by
plant-biology "proximity" and "pollination". Citation-sorted breadth is the wrong
instrument for finding anchors in a frame this small.

This script instead runs narrow, relevance-sorted pulls written to surface actual
ESTIMATES in each cell, and keeps the two configurations apart by construction
(Ruling 1). The output is still candidates, not anchors: selection is a read, and
every selection then clears the existence gate.

Division of labour with the C.2.c seed harvest (212): that harvest is drawn from a
housing chapter's snowball, so it covers the European home-leaving literature well
and the East Asian extended-household literature not at all. These pulls are
weighted to the second.

Usage: python3 source/build/goldset/215_a23_targeted_anchor_pulls.py
"""
import json
import subprocess
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "literature" / "search-logs" / "co-residence-parents-household-delay-targeted-pulls.json"
API = "https://api.openalex.org/works"


def api_key():
    env = ROOT / ".env"
    if env.exists():
        for line in env.read_text().splitlines():
            if line.startswith("OPENALEX_API_KEY="):
                return line.split("=", 1)[1].strip()
    return ""


KEY = api_key()
SELECT = "id,doi,title,publication_year,type,cited_by_count,primary_location,authorships"


def fetch(query, per_page=25, sort=None):
    args = ["curl", "-sS", "--max-time", "120", "--get", API,
            "--data-urlencode", f"filter=title_and_abstract.search:{query}",
            "--data-urlencode", f"per-page={per_page}",
            "--data-urlencode", f"select={SELECT}"]
    if sort:
        args += ["--data-urlencode", f"sort={sort}"]
    if KEY:
        args += ["--data-urlencode", f"api_key={KEY}"]
    last = None
    for attempt in range(3):
        r = subprocess.run(args, capture_output=True, text=True)
        if r.returncode != 0:
            last = f"curl-{r.returncode}"
            time.sleep(5 * (attempt + 1))
            continue
        try:
            d = json.loads(r.stdout)
        except Exception:
            last = "parse"
            time.sleep(5 * (attempt + 1))
            continue
        if "error" in d:
            last = str(d["error"])[:60]
            time.sleep(10 * (attempt + 1))
            continue
        recs = []
        for w in d.get("results", []):
            src = ((w.get("primary_location") or {}).get("source") or {})
            recs.append({
                "openalex": w["id"].rsplit("/", 1)[-1],
                "doi": (w.get("doi") or "").replace("https://doi.org/", "") or None,
                "title": w.get("title"), "year": w.get("publication_year"),
                "type": w.get("type"), "cited_by": w.get("cited_by_count"),
                "venue": src.get("display_name"),
                "authors": "; ".join(a["author"]["display_name"]
                                     for a in (w.get("authorships") or [])[:4]),
            })
        return recs, d["meta"]["count"], None
    return [], None, last


PULLS = [
    # --- PRIMARY_EXTENDED_COUPLE: the configuration C.2.c's pool cannot supply ---
    ("EXT", "grandparent_childcare_fertility",
     '("grandparental childcare" OR "grandparent childcare" OR "grandmother care" OR "grandparental support" OR "grandparental investment") AND (fertility OR childbearing OR "second birth" OR "birth intention")'),
    ("EXT", "coresidence_inlaws_fertility",
     '("living with parents-in-law" OR "co-residence with parents-in-law" OR "coresidence with in-laws" OR "patrilocal" OR "virilocal") AND (fertility OR childbearing OR "second birth")'),
    ("EXT", "multigen_household_fertility",
     '("multigenerational household" OR "three-generation household" OR "extended household" OR "stem family") AND (fertility OR "second birth" OR "birth intention" OR childbearing)'),
    ("EXT", "east_asia_coresidence_fertility",
     '(China OR Japan OR Korea OR Taiwan) AND (coresidence OR "co-residence" OR "living with parents" OR "multigenerational") AND (fertility OR "second child" OR "birth intention")'),

    # --- PRIMARY_PRELAUNCH: estimates, not descriptions ---
    ("PRE", "leaving_home_first_birth",
     '("leaving home" OR "leaving the parental home" OR "home leaving" OR "nest leaving") AND ("first birth" OR "transition to parenthood" OR "entry into parenthood")'),
    ("PRE", "coresidence_delay_fertility",
     '(coresidence OR "co-residence" OR "living with parents" OR "parental home") AND (postponement OR delay OR "delayed" OR timing) AND (fertility OR "first birth" OR parenthood)'),
    ("PRE", "nest_leaving_union_birth_sequence",
     '("home leaving" OR "leaving the parental home" OR "residential independence") AND ("union formation" OR cohabitation OR marriage) AND ("first birth" OR fertility)'),
    ("PRE", "southern_europe_prelaunch",
     '(Italy OR Spain OR Greece OR Portugal OR "Southern Europe") AND ("living with parents" OR "parental home" OR "leaving home" OR coresidence) AND (fertility OR "first birth" OR "lowest-low")'),

    # --- identification, both configurations ---
    ("ID", "identified_arrangement_fertility",
     '(coresidence OR "co-residence" OR "living with parents" OR "parental home" OR "leaving home" OR "multigenerational household") AND ("instrumental variable" OR "natural experiment" OR "difference-in-differences" OR "regression discontinuity" OR "fixed effects" OR "event history") AND (fertility OR "first birth" OR childbearing)'),
    ("ID", "pension_retirement_grandparent_shock",
     '("pension reform" OR "retirement age" OR "social pension") AND (grandparent OR grandmother OR "childcare by grandparents") AND (fertility OR "labour supply of mothers" OR childbearing)'),

    # --- PRIMARY_PROXIMITY, decontaminated: the 214 pull matched plant biology ---
    ("PROX", "proximity_to_parents_fertility",
     '("proximity to parents" OR "distance to parents" OR "living near parents" OR "geographical proximity to family") AND (fertility OR childbearing OR "first birth" OR "second birth")'),
]


def main():
    out, errors = {}, {}
    for cell, label, query in PULLS:
        recs, count, err = fetch(query)
        out[label] = {"cell": cell, "query": query, "frame_count": count,
                      "error": err, "top": recs}
        if err:
            errors[label] = err
        print(f"[{cell:4s}] {label:34s} {'FAILED' if err else count:>7}")
        for r in recs[:8]:
            print(f"        {r['year']} [{r['cited_by']:>4}] {r['doi']} | {r['title'][:62]}")
        print()

    OUT.write_text(json.dumps({
        "meta": {
            "ticket": "TICK-075",
            "status": "CANDIDATES — relevance-sorted targeted pulls; selection is a read, "
                      "and every selection then clears the existence gate.",
            "why": "214's citation-sorted broad families returned high-citation off-topic work; "
                   "the proximity family was contaminated by plant-biology 'proximity'.",
            "failed_pulls": len(errors),
        },
        "pulls": out, "errors": errors}, indent=1))
    print(f"failed pulls: {len(errors)}\nwrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
