#!/usr/bin/env python3
"""
213 — A.23 pre-query frame probe.

TICK-075. Sizes the candidate cells of the A.23 frame before any production query
is written, so the scope doc's cell structure rests on measured counts rather than
on an impression of the literature.

Two standing rules are enforced here:

  * A FAILED request is recorded as `error`, never as a count of 0. The
    refusals-read-as-zeros defect turns a rate-limited probe into a confident
    "this literature does not exist". OpenAlex is currently rate-limiting
    anonymous search under load, so this is live, not hypothetical.
  * Every term block is ALSO scored alone. A block's count tells you nothing
    about which of its terms carried it; the anchored-vocabulary lesson from
    A.17 was a single term carrying 94% of the contamination.

Reads OPENALEX_API_KEY from .env (gitignored).

Usage: python3 source/build/goldset/213_a23_frame_probe.py
"""
import json
import os
import subprocess
import sys
import time
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "literature" / "search-logs" / "co-residence-parents-household-delay-frame-probe.json"
API = "https://api.openalex.org/works"


def api_key():
    env = ROOT / ".env"
    if env.exists():
        for line in env.read_text().splitlines():
            if line.startswith("OPENALEX_API_KEY="):
                return line.split("=", 1)[1].strip()
    return os.environ.get("OPENALEX_API_KEY", "")


KEY = api_key()


def count(query, tries=4):
    """Return (count, error). Exactly one of the two is None. Never conflates them.

    Shells out to curl deliberately. This interpreter has no CA bundle -- urllib
    raises CERTIFICATE_VERIFY_FAILED on every https call -- so a urllib-based probe
    returns 28 transport errors that look exactly like an empty literature. Known
    defect, logged once already; curl carries the system trust store.
    """
    enc = urllib.parse.quote(query)
    url = f"{API}?filter=title_and_abstract.search:{enc}&per-page=1"
    url += f"&api_key={KEY}" if KEY else "&mailto=shravanh@uchicago.edu"
    last = None
    for attempt in range(tries):
        try:
            r = subprocess.run(["curl", "-sS", "--max-time", "90", url],
                               capture_output=True, text=True)
            if r.returncode != 0:
                last = f"curl-{r.returncode}: {r.stderr.strip()[:80]}"
                time.sleep(5 * (attempt + 1))
                continue
            d = json.loads(r.stdout)
            if "error" in d:
                last = f"{d['error']}: {str(d.get('message'))[:80]}"
                time.sleep(10 * (attempt + 1))
                continue
            return d["meta"]["count"], None
        except Exception as e:
            last = f"{type(e).__name__}: {str(e)[:80]}"
            time.sleep(5 * (attempt + 1))
    return None, last


# --- axis vocabularies ------------------------------------------------------
CORESIDE = '(coresidence OR "co-residence" OR coresiding OR coresident OR "living with parents" OR "living at home" OR "parental home")'
LEAVING = '("leaving home" OR "leaving the parental home" OR "home leaving" OR "nest leaving" OR "residential independence" OR boomerang)'
HHFORM = '("household formation" OR "independent household" OR "multigenerational household")'
EXPOSURE = f"({CORESIDE} OR {LEAVING} OR {HHFORM})"
FERT = '(fertility OR childbearing OR "first birth" OR parenthood OR "birth rate")'
UNION = '("union formation" OR "partnership formation" OR marriage OR cohabitation)'
IDENT = '(instrument OR "natural experiment" OR "difference-in-differences" OR experimental OR "regression discontinuity" OR causal OR exogenous)'
ELDER = '(elderly OR caregiving OR "older parents" OR "long-term care" OR dementia OR filial)'

PROBES = [
    # label, query, what the number is for
    ("exposure_all", EXPOSURE, "the whole exposure cloud, any outcome"),
    ("coreside_only", CORESIDE, "co-residence sub-cloud alone"),
    ("leaving_only", LEAVING, "leaving-home sub-cloud alone"),
    ("hhform_only", HHFORM, "household-formation sub-cloud alone"),
    ("exposure_x_fertility", f"{EXPOSURE} AND {FERT}", "PRIMARY cell frame: exposure with a fertility outcome"),
    ("exposure_x_union", f"{EXPOSURE} AND {UNION}", "link-1 cell: exposure with a union outcome only"),
    ("exposure_x_fert_x_ident", f"{EXPOSURE} AND {FERT} AND {IDENT}", "identified sub-frame"),
    ("exposure_x_fert_x_elder", f"{EXPOSURE} AND {FERT} AND {ELDER}", "the eldercare homonym inside the primary frame"),
    ("coreside_x_fert", f"{CORESIDE} AND {FERT}", "co-residence sub-cloud with fertility"),
    ("coreside_x_fert_x_elder", f"{CORESIDE} AND {FERT} AND {ELDER}", "eldercare share of the co-residence sub-cloud"),
    ("leaving_x_fert", f"{LEAVING} AND {FERT}", "leaving-home sub-cloud with fertility"),
    ("hhform_x_fert", f"{HHFORM} AND {FERT}", "household-formation sub-cloud with fertility"),
]

# Each exposure term scored ALONE against the fertility axis, so no term's
# contribution is hidden inside a block.
SOLO_TERMS = [
    "coresidence", '"co-residence"', "coresiding", "coresident",
    '"living with parents"', '"living at home"', '"parental home"',
    '"leaving home"', '"leaving the parental home"', '"home leaving"',
    '"nest leaving"', '"residential independence"', "boomerang",
    '"household formation"', '"independent household"', '"multigenerational household"',
]


def main():
    if not KEY:
        print("WARNING: no OPENALEX_API_KEY found; anonymous search is being "
              "rate-limited under load and probes will mostly fail.", file=sys.stderr)

    results, errors = {}, {}
    for label, q, why in PROBES:
        n, err = count(q)
        results[label] = {"count": n, "error": err, "purpose": why, "query": q}
        if err:
            errors[label] = err
        print(f"{label:28s} {'FAILED' if err else n:>10}  {why}")

    print("\n--- each exposure term alone, against the fertility axis ---")
    solo = {}
    for t in SOLO_TERMS:
        n, err = count(f"{t} AND {FERT}")
        solo[t] = {"count": n, "error": err}
        if err:
            errors[f"solo:{t}"] = err
        print(f"  {t:34s} {'FAILED' if err else n:>8}")

    payload = {
        "meta": {
            "ticket": "TICK-075",
            "hypothesis": "A.23 co-residence-parents-household-delay",
            "source": "OpenAlex title_and_abstract.search",
            "authenticated": bool(KEY),
            "failed_probes": len(errors),
            "note": ("Counts are frame sizes, not evidence counts. A failed probe is "
                     "recorded as an error and is NOT a zero."),
        },
        "probes": results,
        "solo_terms": solo,
        "errors": errors,
    }
    OUT.write_text(json.dumps(payload, indent=1))
    print(f"\nfailed probes: {len(errors)}")
    print(f"wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
