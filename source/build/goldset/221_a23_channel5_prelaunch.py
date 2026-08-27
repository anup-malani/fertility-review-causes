#!/usr/bin/env python3
"""
221 — A.23 channel 5: the named designs, pre-launch arm.

TICK-075. The citation channel has failed twice for the pre-launch arm, for a
measured reason (snowball log §7). Channel 5 -- the designs enumerated by name in
scope §4 before any query was written -- is the only remaining route to identified
evidence for the hypothesis as registered. This script is the decisive test.

Two rules, both from chapters where the shortcut cost a real finding:

  * EVERY DESIGN GETS TWO VOCABULARIES. C.3.g's "no natural experiment exists" was
    two missing words, and this chapter has already produced its own instance --
    `"systematic review" AND "household formation" AND fertility` returns 0 while
    the bare word `review` returns 12. A single phrasing is not a search.
  * THE OUTCOME AXIS IS RELAXED, NOT REQUIRED. The pre-launch literature does not
    put fertility in its titles and abstracts reliably; requiring it is what makes
    the cell look empty. Each design is run with the fertility axis and again with
    the exposure axis alone, and both counts are recorded.

Designs 1-7 are the pre-launch designs. Design 8 (grandparental availability
shocks) is the extended arm's and was already harvested in 215; it is re-run here
only so the two arms are measured on the same instrument.

Records are printed in full for reading: the counts are small enough that the
judgment is a read, not a statistic.

Usage: python3 source/build/goldset/221_a23_channel5_prelaunch.py
"""
import json
import subprocess
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "literature" / "search-logs" / "co-residence-parents-household-delay-channel5.json"
API = "https://api.openalex.org/works"
SELECT = "id,doi,title,publication_year,type,cited_by_count,primary_location,authorships"


def api_key():
    env = ROOT / ".env"
    if env.exists():
        for line in env.read_text().splitlines():
            if line.startswith("OPENALEX_API_KEY="):
                return line.split("=", 1)[1].strip()
    return ""


KEY = api_key()


def fetch(query, per_page=25):
    args = ["curl", "-sS", "--max-time", "150", "--get", API,
            "--data-urlencode", f"filter=title_and_abstract.search:{query}",
            "--data-urlencode", f"per-page={per_page}",
            "--data-urlencode", f"select={SELECT}"]
    if KEY:
        args += ["--data-urlencode", f"api_key={KEY}"]
    last = None
    for attempt in range(3):
        r = subprocess.run(args, capture_output=True, text=True)
        if r.returncode != 0:
            last = f"curl-{r.returncode}"; time.sleep(5 * (attempt + 1)); continue
        try:
            d = json.loads(r.stdout)
        except Exception:
            last = "parse"; time.sleep(5 * (attempt + 1)); continue
        if "error" in d:
            last = str(d["error"])[:60]; time.sleep(10 * (attempt + 1)); continue
        recs = []
        for w in d.get("results", []):
            src = ((w.get("primary_location") or {}).get("source") or {})
            recs.append({
                "doi": (w.get("doi") or "").replace("https://doi.org/", "") or None,
                "title": w.get("title"), "year": w.get("publication_year"),
                "cited_by": w.get("cited_by_count"), "venue": src.get("display_name"),
                "authors": "; ".join(a["author"]["display_name"]
                                     for a in (w.get("authorships") or [])[:3]),
            })
        return recs, d["meta"]["count"], None
    return [], None, last


ARRANGEMENT = ('(coresidence OR "co-residence" OR "living with parents" OR "parental home" '
               'OR "leaving home" OR "home leaving" OR "leaving the parental home" '
               'OR "household formation" OR "residential independence" OR "young adults")')
FERT = '(fertility OR childbearing OR "first birth" OR parenthood OR "birth rate")'

# (design, vocabulary label, treatment query fragment)
DESIGNS = [
    ("1_benefit_age_threshold", "A",
     '("housing benefit" OR "housing allowance" OR "shared accommodation rate" OR "local housing allowance")'),
    ("1_benefit_age_threshold", "B",
     '("welfare eligibility" OR "benefit eligibility" OR "age cutoff" OR "age cut-off" OR "eligibility age" OR "age discontinuity")'),
    ("2_move_out_grant", "A",
     '("rent subsidy" OR "housing subsidy" OR "move-out grant" OR "youth housing policy" OR "housing grant")'),
    ("2_move_out_grant", "B",
     '("cash transfer" OR "conditional transfer" OR "leaving-home subsidy" OR "independence allowance" OR "starter home")'),
    ("3_administrative_allocation", "A",
     '("public housing" OR "social housing" OR "housing lottery" OR "housing allocation" OR "waiting list")'),
    ("3_administrative_allocation", "B",
     '(hukou OR "work unit" OR danwei OR "housing restitution" OR "housing privatization" OR "council housing")'),
    ("4_compulsory_removal", "A",
     '(conscription OR "military service" OR "compulsory service" OR draft)'),
    ("4_compulsory_removal", "B",
     '("boarding school" OR "residential college" OR "university dormitory" OR "student housing" OR "campus housing")'),
    ("5_dwelling_shock", "A",
     '(earthquake OR flood OR hurricane OR "natural disaster" OR "housing destruction")'),
    ("5_dwelling_shock", "B",
     '("war damage" OR bombing OR "forced displacement" OR "slum clearance" OR "urban renewal" OR resettlement)'),
    ("6_legal_support_age", "A",
     '("age of majority" OR "parental support obligation" OR "filial responsibility law" OR "legal drinking age")'),
    ("6_legal_support_age", "B",
     '("child support" OR "dependency age" OR "tax dependent" OR "family allowance eligibility" OR "insurance coverage age")'),
    ("7_sibling_instrument", "A",
     '("birth order" OR "sibling composition" OR "sibship size" OR "number of siblings")'),
    ("7_sibling_instrument", "B",
     '("twin birth" OR "sex composition" OR "instrumental variable" OR "exogenous variation")'),
    # the extended arm's design, run on the same instrument for comparability
    ("8_grandparent_shock", "A",
     '("pension reform" OR "retirement age" OR "social pension" OR "pension eligibility")'),
]


def main():
    results, errors = {}, {}
    for design, vocab, treatment in DESIGNS:
        key = f"{design}::{vocab}"
        with_fert, n_with, e1 = fetch(f"{treatment} AND {ARRANGEMENT} AND {FERT}")
        without_fert, n_without, e2 = fetch(f"{treatment} AND {ARRANGEMENT}")
        if e1 or e2:
            errors[key] = e1 or e2
        results[key] = {
            "design": design, "vocabulary": vocab, "treatment": treatment,
            "n_with_fertility_axis": n_with, "n_arrangement_only": n_without,
            "error": e1 or e2,
            "records_with_fertility": with_fert,
        }
        print(f"\n=== {design}  vocab {vocab} "
              f"| with fertility: {'FAIL' if e1 else n_with} "
              f"| arrangement only: {'FAIL' if e2 else n_without}")
        for r in with_fert[:10]:
            print(f"    {r['year']} [{(r['cited_by'] or 0):>4}] {r['doi']} | {(r['title'] or '')[:74]}")

    OUT.write_text(json.dumps({
        "meta": {
            "ticket": "TICK-075",
            "purpose": "Channel 5 -- the named designs of scope §4. The decisive test for the "
                       "pre-launch arm after the citation channel failed twice.",
            "method": "Two vocabularies per design; the fertility axis relaxed as well as required, "
                      "because the pre-launch literature does not reliably name its outcome.",
            "failed": len(errors),
        },
        "designs": results, "errors": errors}, indent=1))
    print(f"\nfailed: {len(errors)}\nwrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
