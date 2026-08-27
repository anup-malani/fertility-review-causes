#!/usr/bin/env python3
"""
222 — A.23 production query: construction and gold-recall calibration.

TICK-075. Builds the two-axis boolean query (CAUSE × FERTILITY) per the
2026-06-20 decision -- the boolean layer optimises RECALL and the LLM screen
optimises precision, because a false negative at the search stage is
unrecoverable and a false positive is not.

Calibration is a per-anchor membership test, not a spot check: for each gated
anchor, ask OpenAlex whether that exact work is inside the query's result set
(`filter=title_and_abstract.search:<Q>,openalex_id:<W...>`). A record either
matches or it does not, so recall is measured rather than estimated.

Four variants are scored so the choices are visible rather than asserted:
  V1  the full exposure axis × fertility            -- the candidate
  V2  V1 with the emancipation family removed       -- what the omission cost
  V3  V1 with a union/partnership outcome added     -- catches the link-1 stream
  V4  the fertility axis ALONE, no exposure axis    -- the outcome-only arm

V4 exists because a conjunction can be dominated by one of its arms, and the only
way to know is to measure the arm. On D.3.c the conjunction lost 85% of gold AND
precision against the outcome-only query.

Usage: python3 source/build/goldset/222_a23_production_query.py
"""
import json
import subprocess
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
LOGS = ROOT / "literature" / "search-logs"
ANCHORS = LOGS / "co-residence-parents-household-delay-cold-start-anchors.json"
OUT = LOGS / "co-residence-parents-household-delay-production-query.json"
API = "https://api.openalex.org/works"


def api_key():
    env = ROOT / ".env"
    if env.exists():
        for line in env.read_text().splitlines():
            if line.startswith("OPENALEX_API_KEY="):
                return line.split("=", 1)[1].strip()
    return ""


KEY = api_key()


def get(params, tries=3):
    args = ["curl", "-sS", "--max-time", "150", "--get", API]
    for k, v in params:
        args += ["--data-urlencode", f"{k}={v}"]
    if KEY:
        args += ["--data-urlencode", f"api_key={KEY}"]
    last = None
    for attempt in range(tries):
        r = subprocess.run(args, capture_output=True, text=True)
        if r.returncode != 0:
            last = f"curl-{r.returncode}"; time.sleep(5 * (attempt + 1)); continue
        try:
            d = json.loads(r.stdout)
        except Exception:
            last = "parse"; time.sleep(5 * (attempt + 1)); continue
        if "error" in d:
            last = str(d["error"])[:70]; time.sleep(10 * (attempt + 1)); continue
        return d, None
    return None, last


# ---------------------------------------------------------------- the axes ---
# CAUSE axis. Three families, kept separate so each can be scored alone.
PRELAUNCH = (
    'coresidence OR "co-residence" OR coresiding OR coresident '
    'OR "living with parents" OR "living at home" OR "parental home" '
    'OR "leaving home" OR "leaving the parental home" OR "home leaving" '
    'OR "nest leaving" OR "residential independence" OR boomerang '
    'OR "household formation" OR "independent household"')
EMANCIPATION = (
    'emancipation OR "living apart from parents" OR "living independently" '
    'OR "residential autonomy" OR "leaving the nest"')
EXTENDED = (
    '"multigenerational household" OR "three-generation household" '
    'OR "extended household" OR "stem family" OR "parents-in-law" '
    'OR "grandparental childcare" OR "grandparent childcare" '
    'OR "intergenerational coresidence" OR "intergenerational co-residence" '
    'OR "living with in-laws" OR patrilocal')

FERT = ('fertility OR childbearing OR "first birth" OR "second birth" '
        'OR parenthood OR "birth rate" OR childlessness OR "family size" '
        'OR "number of children" OR "birth intention" OR "fertility intention"')
UNION = ('"union formation" OR "partnership formation" OR "marriage timing" '
         'OR "age at marriage" OR cohabitation')

CAUSE_FULL = f"({PRELAUNCH} OR {EMANCIPATION} OR {EXTENDED})"
CAUSE_NO_EMAN = f"({PRELAUNCH} OR {EXTENDED})"

QUALIFIED_EMAN = ('"youth emancipation" OR "residential emancipation" '
                  'OR "emancipation of young people" OR "living apart from parents"')

VARIANTS = {
    "V1_full": f"{CAUSE_FULL} AND ({FERT})",
    "V2_no_emancipation": f"{CAUSE_NO_EMAN} AND ({FERT})",
    "V3_plus_union_outcome": f"{CAUSE_FULL} AND ({FERT} OR {UNION})",
    "V4_outcome_only": f"({FERT})",
    "V5_qualified_emancipation": f"({CAUSE_NO_EMAN[1:-1]} OR {QUALIFIED_EMAN}) AND ({FERT})",
}

# What each optional family adds that the rest of the axis does not already reach.
# A frame that grows is not the same as a frame that improves: the bare word
# `emancipation` grew this frame 40% and every one of those records had to be
# looked at before the growth could be called a gain.
ADDS_ALONE = {
    "bare_emancipation": f"({EMANCIPATION}) AND ({FERT}) NOT {CAUSE_NO_EMAN}",
    "qualified_emancipation": f"({QUALIFIED_EMAN}) AND ({FERT}) NOT {CAUSE_NO_EMAN}",
}


def main():
    anchors = json.loads(ANCHORS.read_text())["anchors"]

    # --- resolve anchors to OpenAlex ids ------------------------------------
    print(f"resolving {len(anchors)} anchors to OpenAlex ids")
    resolved, unresolvable = [], []
    for a in anchors:
        d, err = get([("filter", f"doi:{a['doi']}"), ("per-page", "1"), ("select", "id,title")])
        if err or not d.get("results"):
            unresolvable.append({"doi": a["doi"], "reason": err or "no_openalex_record"})
            continue
        resolved.append({**a, "openalex": d["results"][0]["id"].rsplit("/", 1)[-1]})
    print(f"  {len(resolved)} resolved, {len(unresolvable)} not in OpenAlex\n")

    gold = [a for a in resolved if a["gold_status"] == "gold_candidate"]
    decoys = [a for a in resolved if a["provenance_channel"] == "decoy"]
    print(f"gold candidates: {len(gold)}   decoys: {len(decoys)}\n")

    results = {}
    for name, q in VARIANTS.items():
        d, err = get([("filter", f"title_and_abstract.search:{q}"), ("per-page", "1")])
        frame = None if err else d["meta"]["count"]
        hits, misses, errors = [], [], []
        for a in resolved:
            dd, e = get([("filter", f"title_and_abstract.search:{q},openalex_id:{a['openalex']}"),
                         ("per-page", "1")])
            if e:
                errors.append(a["doi"]); continue
            (hits if dd["meta"]["count"] else misses).append(a)
        gold_hits = [a for a in hits if a["gold_status"] == "gold_candidate"]
        gold_misses = [a for a in misses if a["gold_status"] == "gold_candidate"]
        decoy_hits = [a for a in hits if a["provenance_channel"] == "decoy"]
        results[name] = {
            "query": q, "frame_size": frame,
            "anchors_tested": len(resolved) - len(errors),
            "recall_all": round(100 * len(hits) / max(1, len(resolved) - len(errors)), 1),
            "recall_gold": round(100 * len(gold_hits) / max(1, len(gold)), 1),
            "gold_missed": [{"doi": a["doi"], "cell": a["provisional_cell"],
                             "title": a["recorded_title"]} for a in gold_misses],
            "decoys_admitted": len(decoy_hits),
            "decoys_total": len(decoys),
            "test_errors": errors,
        }
        r = results[name]
        print(f"{name:24s} frame={str(frame):>7}  recall_all={r['recall_all']:>5}%  "
              f"recall_gold={r['recall_gold']:>5}%  decoys_admitted={r['decoys_admitted']}/{r['decoys_total']}")
        for m in r["gold_missed"]:
            print(f"      MISSED GOLD  {m['doi']:34s} {m['cell']:26s} {m['title'][:44]}")

    # --- each CAUSE family alone, against the fertility axis -----------------
    print("\ncause families scored alone (never trust a block):")
    families = {"prelaunch": PRELAUNCH, "emancipation": EMANCIPATION, "extended": EXTENDED}
    fam = {}
    for label, block in families.items():
        d, err = get([("filter", f"title_and_abstract.search:({block}) AND ({FERT})"),
                      ("per-page", "1")])
        n = None if err else d["meta"]["count"]
        gold_in = 0
        for a in gold:
            dd, e = get([("filter", f"title_and_abstract.search:({block}) AND ({FERT}),"
                                    f"openalex_id:{a['openalex']}"), ("per-page", "1")])
            if not e and dd["meta"]["count"]:
                gold_in += 1
        fam[label] = {"frame": n, "gold_reached": gold_in, "gold_total": len(gold)}
        print(f"  {label:14s} frame={str(n):>7}  gold reached {gold_in}/{len(gold)}")

    # --- what the optional families add that the rest does not reach -------
    print("\nwhat each optional family adds ALONE (frame growth is not frame gain):")
    adds = {}
    for label, q in ADDS_ALONE.items():
        d, err = get([("filter", f"title_and_abstract.search:{q}"), ("per-page", "10"),
                      ("sort", "cited_by_count:desc"), ("select", "title,publication_year")])
        adds[label] = {"query": q, "n": None if err else d["meta"]["count"], "error": err,
                       "sample": [w.get("title") for w in (d or {}).get("results", [])]}
        print(f"  {label:26s} {adds[label]['n']}")
        for t in adds[label]["sample"][:6]:
            print(f"      {(t or '')[:74]}")

    OUT.write_text(json.dumps({
        "meta": {
            "ticket": "TICK-075",
            "construction": "Two-axis CAUSE x FERTILITY per decisions/2026-06-20. Boolean layer "
                            "optimises recall; the LLM screen optimises precision.",
            "calibration": "Per-anchor membership test against OpenAlex, not a spot check.",
            "anchors_resolved": len(resolved),
            "anchors_not_in_openalex": unresolvable,
        },
        "axes": {"prelaunch": PRELAUNCH, "emancipation": EMANCIPATION,
                 "extended": EXTENDED, "fertility": FERT, "union": UNION},
        "variants": results,
        "cause_families_alone": fam,
        "optional_families_add_alone": adds,
        "adopted": {
            "variant": "V2_no_emancipation",
            "why": "100% gold recall (12/12) at the smallest frame of the variants that achieve it. "
                   "The emancipation family was added on 2026-08-27 after the channel-5 pass and is "
                   "now REMOVED: the bare word is a homonym -- the 489 records it reached alone are "
                   "slave emancipation, female emancipation and care-leaver emancipation -- and the "
                   "study it was added for is reachable through \"household formation\" anyway. "
                   "Qualifying it recovers only 48 records, mostly disability and gerontology uses "
                   "of \"living independently\".",
        },
    }, indent=1))
    print(f"\nwrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
