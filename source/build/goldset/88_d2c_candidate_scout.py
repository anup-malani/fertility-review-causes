#!/usr/bin/env python3
"""
Extended candidate scout for the NEXT hypothesis (post-TICK-091).

TICK-091's scout (source/build/goldset/88_a14_candidate_scout.py) only ranked the biological/
proximate un-started set. A.14 is now done, so the smallest MEASURED remaining is B.2 endocrine
(4,475). But the un-ticketed cultural/demographic candidates were never scouted. This script
measures those on the SAME production-frame axis (topic AND fertility/fecundity) so the "smallest"
claim is honest across categories. B.2 and A.13 are re-included as comparison anchors.

Same count() as 88 (curl, title_and_abstract.search, keyed).
"""
import json, subprocess, urllib.parse, time, pathlib

MAILTO = "shravanh@uchicago.edu"
BASE = "https://api.openalex.org/works"
CACHE = pathlib.Path("temp/next-candidate-scout-cache.json")


def _api_key():
    try:
        for line in open(".env"):
            if line.startswith("OPENALEX_API_KEY="):
                return line.split("=", 1)[1].strip().strip('"') or None
    except FileNotFoundError:
        pass
    return None


KEY = _api_key()
PACE = 0.25 if KEY else 1.25
cache = json.loads(CACHE.read_text()) if CACHE.exists() else {}


def count(q):
    if q in cache:
        return cache[q]
    url = (f"{BASE}?filter=title_and_abstract.search:{urllib.parse.quote(q, safe='')}"
           f"&per_page=1&mailto={MAILTO}")
    if KEY:
        url += f"&api_key={KEY}"
    p = subprocess.run(["curl", "-s", "-S", "--max-time", "60", url], capture_output=True, text=True)
    if p.returncode != 0:
        return None
    try:
        d = json.loads(p.stdout)
    except json.JSONDecodeError:
        return None
    if "error" in d:
        return None
    n = d.get("meta", {}).get("count")
    if n is not None:
        cache[q] = n
        CACHE.parent.mkdir(parents=True, exist_ok=True)
        CACHE.write_text(json.dumps(cache, indent=1, sort_keys=True))
        time.sleep(PACE)
    return n


FERT = ('("fertility" OR "childbearing" OR "birth rate" OR "total fertility rate" OR "childlessness" '
        'OR "fecundity" OR "time to pregnancy" OR "subfertility" OR "infertility")')

CANDS = {
    # --- comparison anchors from script 88 (biological) ---
    "B.2 endocrine-disruptors [anchor]":
        '("endocrine disruptor" OR "endocrine disrupting" OR "phthalate" OR "bisphenol")',
    "A.13 breastfeeding-lactational-amenorrhea [anchor]":
        '("breastfeeding" OR "lactational amenorrhea" OR "lactational amenorrhoea" OR "breast feeding")',
    # --- un-measured un-ticketed candidates (cultural/demographic) ---
    "A.19 intergenerational-transmission-fertility":
        '("intergenerational transmission" OR "fertility preferences" OR "family size norms" OR '
        '"transmission of fertility" OR "vertical transmission")',
    "A.20 cultural-diffusion-mechanisms":
        '("cultural diffusion" OR "social network" OR "peer effect" OR "social learning" OR '
        '"ideational diffusion" OR "mass media")',
    "D.1.d nationalism-pronatalist-ideology":
        '("pronatalist" OR "pronatalism" OR "pro-natalist" OR "natalist policy" OR '
        '"nationalist ideology" OR "patriotic duty")',
    "D.2.c son-preference-cultural":
        '("son preference" OR "sex-selective" OR "sex selective" OR "gender preference" OR '
        '"desire for sons" OR "boy preference")',
}


def main():
    print(f"api_key={bool(KEY)}  outcome axis = FERT (same as script 88)\n")
    rows = []
    for name, topic in CANDS.items():
        n = count(f"{topic} AND {FERT}")
        rows.append((name, n))
        print(f"  {('REFUSED' if n is None else format(n, ',')):>10}  {name}")
    print("\n--- ranked smallest-first (this run) ---")
    for name, n in sorted(rows, key=lambda r: (r[1] is None, r[1] if r[1] is not None else 0)):
        print(f"  {('REFUSED' if n is None else format(n, ',')):>10}  {name}")
    print("\nReference (script 88): A.14=373 | B.2=4,475 | A.13=5,078 | B.3=9,442 | "
          "A.15=15,325 | B.4=21,710 | A.16=25,214.  'smallest' bar ~1,808.")


if __name__ == "__main__":
    main()
