#!/usr/bin/env python3
"""278 — C.3.e production query, built and calibrated per arm. TICK-077.

Ruling 1 made this one chapter with two arms that DO NOT SHARE A VOCABULARY: Arm S is
development economics, Arm B is household finance. A single pooled recall number would
hide a dead arm, so every measurement below is per arm.

Method, in order:
  1. Frame count for each arm's query.
  2. Gold recall per arm, against the 26 anchors resolved in 275, computed by intersecting
     the query with the anchor ids in ONE call per query rather than 26.
  3. Decoy admission, reported separately. A decoy is a boundary case, not an error: a
     query that admits decoys is not thereby wrong, but the rate has to be visible because
     it is the screen's workload.
  4. LEAVE-ONE-OUT on every exposure term, in both directions -- what recall is lost if the
     term goes, and how much frame it adds. An axis accepted as a block is a block of
     assumptions; 276 already showed single terms carrying 70-90% of a block here.

OpenAlex hazards enforced by assertion below, all previously paid for:
  - a phrase starting "not" parses as boolean NOT and silently returns an unrestricted count
  - `?` is a wildcard and `!` negation; a 200 whose body is an error reads as an empty
    literature unless meta.count is checked
  - stopwords are dropped inside quoted phrases
  - commas separate FILTERS; a comma inside a filter VALUE is fatal and %2C does not save it

Usage: python3 278_c3e_production_query.py
"""
import json, re, subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
LOGS = ROOT / "literature" / "search-logs"
ANCHORS = LOGS / "credit-constraints-cold-start-anchors.json"
OUT = LOGS / "credit-constraints-production-query.json"
KEY = next((l.split("=", 1)[1].strip() for l in (ROOT / ".env").read_text().splitlines()
            if l.startswith("OPENALEX_API_KEY=")), "")
MAILTO = "shravanh@uchicago.edu"


def q(params):
    args = ["curl", "-sS", "--max-time", "120", "-G", "https://api.openalex.org/works"]
    for k, v in params:
        args += ["--data-urlencode", f"{k}={v}"]
    args += ["--data-urlencode", f"api_key={KEY}", "--data-urlencode", f"mailto={MAILTO}"]
    r = subprocess.run(args, capture_output=True, text=True)
    try:
        d = json.loads(r.stdout)
    except json.JSONDecodeError:
        return None, "non-JSON body"
    if "meta" not in d or d["meta"].get("count") is None:
        return None, (d.get("message") or "refused")[:100]
    return d, None


def phrase(p):
    assert not p.lower().startswith("not "), f"leading 'not' is boolean NOT: {p}"
    assert "?" not in p and "!" not in p and "," not in p, f"unsafe char in {p}"
    return f'"{p}"'


def blk(terms):
    return "(" + " OR ".join(phrase(t) for t in terms) + ")"


OUTCOME = ["fertility", "birth rate", "birth rates", "childbearing", "births",
           "number of children", "family size", "parity", "birth spacing",
           "completed fertility", "fertility intentions"]

EXPOSURE = {
    "S": ["children as insurance", "insurance motive", "old age security",
          "old-age security", "precautionary saving", "consumption smoothing",
          "informal insurance", "risk sharing", "crop insurance", "income risk",
          "savings account", "commitment savings"],
    "B": ["credit constraint", "credit constraints", "liquidity constraint",
          "borrowing constraint", "down payment", "loan-to-value", "mortgage credit",
          "credit supply", "credit expansion", "interest rate", "mortgage rate",
          "loan ceiling", "collateral constraint"],
    "composite": ["financial inclusion", "bank branch", "microfinance", "microcredit",
                  "access to credit", "credit access", "financial development",
                  "access to finance", "banking access", "financial access"],
}


def frame(expo_terms):
    return f"title_and_abstract.search:{blk(expo_terms)} AND {blk(OUTCOME)}"


def main():
    anchors = json.loads(ANCHORS.read_text())
    ids = {a["key"]: a["top_candidate"]["oa_id"].rsplit("/", 1)[-1] for a in anchors}
    arm_of = {a["key"]: a["arm"] for a in anchors}
    role_of = {a["key"]: a.get("role", "anchor") for a in anchors}
    gold = {k: v for k, v in ids.items() if role_of[k] != "decoy"}
    decoy = {k: v for k, v in ids.items() if role_of[k] == "decoy"}

    def matched(filter_str, want):
        """Which of `want` the query returns. One call, not len(want) calls."""
        if not want:
            return set()
        hit = set()
        keys = list(want)
        for i in range(0, len(keys), 40):
            batch = keys[i:i + 40]
            d, err = q([("filter", "openalex_id:" + "|".join(want[k] for k in batch)
                         + "," + filter_str),
                        ("per-page", "40"), ("select", "id")])
            if err:
                raise SystemExit(f"recall query refused: {err}")
            got = {w["id"].rsplit("/", 1)[-1] for w in d["results"]}
            hit |= {k for k in batch if want[k] in got}
        return hit

    res = {"outcome_axis": OUTCOME, "exposure_axes": EXPOSURE, "arms": {}, "leave_one_out": {}}

    for arm, terms in EXPOSURE.items():
        f = frame(terms)
        d, err = q([("filter", f), ("per-page", "1"), ("select", "id")])
        n = None if err else d["meta"]["count"]
        arm_gold = {k: v for k, v in gold.items() if arm_of[k] == arm}
        hit_own = matched(f, arm_gold)
        hit_all = matched(f, gold)
        hit_decoy = matched(f, decoy)
        res["arms"][arm] = {
            "frame_count": n, "error": err,
            "gold_in_arm": len(arm_gold), "gold_in_arm_recalled": len(hit_own),
            "gold_in_arm_missed": sorted(set(arm_gold) - hit_own),
            "gold_all_recalled": len(hit_all), "gold_all": len(gold),
            "decoys_admitted": sorted(hit_decoy),
        }
        print(f"\n=== ARM {arm}: frame {n}")
        print(f"    own-arm gold {len(hit_own)}/{len(arm_gold)}"
              f"   all-gold {len(hit_all)}/{len(gold)}"
              f"   decoys admitted {len(hit_decoy)}/{len(decoy)}")
        if set(arm_gold) - hit_own:
            print("    MISSED:", ", ".join(sorted(set(arm_gold) - hit_own)))

        # leave-one-out
        loo = []
        for t in terms:
            rest = [x for x in terms if x != t]
            fr = frame(rest)
            d2, e2 = q([("filter", fr), ("per-page", "1"), ("select", "id")])
            n2 = None if e2 else d2["meta"]["count"]
            h2 = matched(fr, arm_gold)
            alone, ea = q([("filter", f"title_and_abstract.search:{phrase(t)} AND {blk(OUTCOME)}"),
                           ("per-page", "1"), ("select", "id")])
            loo.append({"term": t,
                        "frame_without": n2,
                        "frame_added_by_term": (n - n2) if (n is not None and n2 is not None) else None,
                        "term_alone": None if ea else alone["meta"]["count"],
                        "gold_lost_without": sorted(hit_own - h2)})
        loo.sort(key=lambda x: -(x["frame_added_by_term"] or 0))
        res["leave_one_out"][arm] = loo
        print(f"    {'term':26s} {'adds':>7s} {'alone':>7s}  gold lost if dropped")
        for x in loo:
            print(f"    {x['term']:26s} {str(x['frame_added_by_term']):>7s} "
                  f"{str(x['term_alone']):>7s}  {','.join(x['gold_lost_without']) or '-'}")

    OUT.write_text(json.dumps(res, indent=2))
    print(f"\nwritten: {OUT}")


if __name__ == "__main__":
    main()
