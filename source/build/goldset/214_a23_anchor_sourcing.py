#!/usr/bin/env python3
"""
214 — A.23 cold-start anchor sourcing, channels 1, 2 and 5.

TICK-075. Runs the named query families of the search scope and dumps candidates
for hand-selection into the anchor set. It does NOT decide anchors; selection is a
judgment made by reading the output, and every selected anchor still has to clear
the existence gate before it enters a recall denominator.

Channel 1 — prior systematic/scoping reviews and meta-analyses (anchors by
            external authority).
Channel 2 — theory canon (seeds the theory set; does not count toward empirical
            recall).
Channel 5 — the eight named designs of scope §4, each its own query string, run
            whether or not a broad frame would have surfaced them. This is the
            C.3.g lesson: a negative finding about identified evidence is only as
            good as the vocabulary that looked for it.

Ruling 1 (2026-08-27) requires BOTH configurations to be reachable, so the
extended-household vocabulary is a first-class query family here, not an
afterthought. The pre-launch vocabulary alone would build the one-sided pool the
ruling exists to prevent.

Also collects the deliberate off-cell DECOYS the scope requires, so the eventual
production query is tested on routing and not only on topical retrieval.

Shells out to curl: this interpreter has no CA bundle and urllib raises
CERTIFICATE_VERIFY_FAILED on every request, which would look like an empty
literature. A failed request is recorded as an error, never as zero results.

Usage: python3 source/build/goldset/214_a23_anchor_sourcing.py
"""
import json
import subprocess
import sys
import time
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "literature" / "search-logs" / "co-residence-parents-household-delay-anchor-candidates.json"
API = "https://api.openalex.org/works"
PER_PAGE = 25


def api_key():
    env = ROOT / ".env"
    if env.exists():
        for line in env.read_text().splitlines():
            if line.startswith("OPENALEX_API_KEY="):
                return line.split("=", 1)[1].strip()
    return ""


KEY = api_key()
SELECT = "id,doi,title,publication_year,type,cited_by_count,primary_location,authorships"


def fetch(query, tries=3, per_page=PER_PAGE):
    """Return (records, count, error). Errors are errors, never empty results."""
    args = [
        "curl", "-sS", "--max-time", "120", "--get", API,
        "--data-urlencode", f"filter=title_and_abstract.search:{query}",
        "--data-urlencode", f"per-page={per_page}",
        "--data-urlencode", "sort=cited_by_count:desc",
        "--data-urlencode", f"select={SELECT}",
    ]
    if KEY:
        args += ["--data-urlencode", f"api_key={KEY}"]
    last = None
    for attempt in range(tries):
        r = subprocess.run(args, capture_output=True, text=True)
        if r.returncode != 0:
            last = f"curl-{r.returncode}: {r.stderr.strip()[:70]}"
            time.sleep(5 * (attempt + 1))
            continue
        try:
            d = json.loads(r.stdout)
        except Exception as e:
            last = f"parse: {type(e).__name__}"
            time.sleep(5 * (attempt + 1))
            continue
        if "error" in d:
            last = f"{d['error']}: {str(d.get('message'))[:60]}"
            time.sleep(10 * (attempt + 1))
            continue
        recs = []
        for w in d.get("results", []):
            src = ((w.get("primary_location") or {}).get("source") or {})
            recs.append({
                "openalex": w["id"].rsplit("/", 1)[-1],
                "doi": (w.get("doi") or "").replace("https://doi.org/", "") or None,
                "title": w.get("title"),
                "year": w.get("publication_year"),
                "type": w.get("type"),
                "cited_by": w.get("cited_by_count"),
                "venue": src.get("display_name"),
                "authors": "; ".join(a["author"]["display_name"]
                                     for a in (w.get("authorships") or [])[:4]),
            })
        return recs, d["meta"]["count"], None
    return [], None, last


# --- vocabulary blocks ------------------------------------------------------
PRELAUNCH = ('(coresidence OR "co-residence" OR "living with parents" OR "living at home" '
             'OR "parental home" OR "leaving home" OR "leaving the parental home" '
             'OR "home leaving" OR "nest leaving" OR "residential independence" OR boomerang)')
EXTENDED = ('("multigenerational household" OR "three-generation household" OR "extended household" '
            'OR "stem family" OR "parents-in-law" OR "grandparental childcare" '
            'OR "grandparent childcare" OR "intergenerational coresidence" '
            'OR "intergenerational co-residence" OR "living with in-laws")')
FERT = '(fertility OR childbearing OR "first birth" OR parenthood OR "birth rate")'
REVIEW = ('("systematic review" OR "meta-analysis" OR "scoping review" OR "literature review" '
          'OR "review of the literature" OR "research synthesis")')

FAMILIES = [
    # (channel, label, query, note)
    ("1", "reviews_prelaunch", f"{REVIEW} AND {PRELAUNCH} AND {FERT}",
     "prior reviews covering the pre-launch configuration"),
    ("1", "reviews_extended", f"{REVIEW} AND {EXTENDED} AND {FERT}",
     "prior reviews covering the extended-household configuration (Ruling 1)"),
    ("1", "reviews_household_formation", f'{REVIEW} AND "household formation" AND {FERT}',
     "prior reviews on household formation and fertility"),

    ("2", "theory_lifecourse", f'("life course" OR "transition to adulthood" OR "life-course transitions") AND {PRELAUNCH} AND {FERT}',
     "life-course transition theory"),
    ("2", "theory_family_system", '("family system" OR "family ties" OR "strong family" OR "familism" OR "stem family") AND (fertility OR "household formation" OR "leaving home")',
     "family-system typologies (Reher, Hajnal) — theory and Wall 3 decoys"),
    ("2", "theory_semi_autonomy", '("semi-autonomy" OR "semi-dependent" OR "emerging adulthood" OR "delayed adulthood") AND (fertility OR "parental home" OR coresidence)',
     "semi-autonomy / emerging adulthood"),

    # channel 5 — the eight named designs of scope §4
    ("5", "design1_benefit_age_threshold", f'("housing benefit" OR "housing allowance" OR "shared accommodation rate" OR "local housing allowance" OR "welfare benefit") AND ("age threshold" OR "age limit" OR "regression discontinuity" OR "eligibility age") AND ({PRELAUNCH} OR {FERT})',
     "design 1: age-threshold rules in housing benefit"),
    ("5", "design2_move_out_grant", f'("housing allowance" OR "rent subsidy" OR "housing subsidy" OR "move-out grant" OR "youth housing") AND {PRELAUNCH}',
     "design 2: youth housing allowances and move-out grants (Wall 1 seam)"),
    ("5", "design3_allocation", f'("public housing" OR "housing lottery" OR "waiting list" OR "housing allocation" OR "work unit housing" OR hukou OR restitution) AND ({PRELAUNCH} OR {EXTENDED}) AND {FERT}',
     "design 3: administrative allocation of dwellings"),
    ("5", "design4_compulsory_removal", f'(conscription OR "military service" OR "boarding school" OR "dormitory" OR "university dormitory") AND ({PRELAUNCH} OR {FERT})',
     "design 4: compulsory removal from the parental home"),
    ("5", "design5_dwelling_shock", f'(earthquake OR "housing destruction" OR "war damage" OR "natural disaster" OR reconstruction) AND ({PRELAUNCH} OR {EXTENDED}) AND {FERT}',
     "design 5: dwelling destruction and reconstruction shocks"),
    ("5", "design6_legal_support_age", f'("age of majority" OR "parental support obligation" OR "filial responsibility law" OR "child support" OR "legal reform") AND {PRELAUNCH}',
     "design 6: legal change in support obligations and majority age"),
    ("5", "design7_sibling_instrument", f'("birth order" OR "sibling composition" OR "number of siblings" OR "sibship size") AND {PRELAUNCH}',
     "design 7: sibling composition as an instrument for home-leaving"),
    ("5", "design8_grandparent_shock", f'("retirement age" OR "pension reform" OR "grandmother" OR "grandparent" OR "parental death") AND {EXTENDED} AND {FERT}',
     "design 8: grandparental availability shocks"),

    # the two primary cells, broad, for hand-picking empirical anchors
    ("A", "primary_prelaunch_broad", f"{PRELAUNCH} AND {FERT}",
     "pre-launch cell, broad — hand-pick empirical anchors"),
    ("A", "primary_extended_broad", f"{EXTENDED} AND {FERT}",
     "extended-household cell, broad — hand-pick empirical anchors (Ruling 1)"),
    ("A", "primary_proximity", '("proximity to parents" OR "distance to parents" OR "geographical proximity" OR "living near parents") AND ' + FERT,
     "proximity cell — a different treatment, pooled separately"),

    # deliberate off-cell decoys, for the routing test
    ("D", "decoy_price_c2c", f'("house price" OR "housing price" OR rent OR "housing cost" OR "home equity") AND {PRELAUNCH} AND {FERT}',
     "decoy: price-identified, routes to C.2.c"),
    ("D", "decoy_eldercare", f'{PRELAUNCH} AND ("elderly parents" OR "older parents" OR caregiving OR "long-term care" OR filial) AND {FERT}',
     "decoy: the elder-support homonym"),
    ("D", "decoy_premodern_niche", '("European marriage pattern" OR Hajnal OR "preventive check" OR "niche" OR "peasant household") AND ("household formation" OR marriage) AND fertility',
     "decoy: the pre-modern niche — A.7's under Ruling 2"),
    ("D", "decoy_link1_only", f"{PRELAUNCH} AND (\"union formation\" OR \"partnership formation\" OR \"marriage timing\") AND NOT {FERT}",
     "decoy: link-1 only, no fertility outcome"),
]


def main():
    if not KEY:
        print("WARNING: no OPENALEX_API_KEY; anonymous search is rate-limited under load.",
              file=sys.stderr)
    out, errors = {}, {}
    for channel, label, query, note in FAMILIES:
        recs, count, err = fetch(query)
        out[label] = {"channel": channel, "note": note, "query": query,
                      "frame_count": count, "error": err, "top": recs}
        if err:
            errors[label] = err
        print(f"[ch{channel}] {label:32s} {'FAILED' if err else count:>8}  {note}")

    payload = {
        "meta": {
            "ticket": "TICK-075",
            "hypothesis": "A.23 co-residence-parents-household-delay",
            "status": "CANDIDATES — not anchors. Selection is a judgment made by reading this file; "
                      "every selected anchor must then clear the existence gate.",
            "ruling_1": "A.23 owns both configurations, so the extended-household vocabulary is a "
                        "first-class query family here (2026-08-27).",
            "failed_families": len(errors),
            "per_page": PER_PAGE,
        },
        "families": out,
        "errors": errors,
    }
    OUT.write_text(json.dumps(payload, indent=1))
    print(f"\nfailed families: {len(errors)}")
    print(f"wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
