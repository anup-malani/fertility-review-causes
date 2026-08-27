#!/usr/bin/env python3
"""
220 — A.23 cloud scoring after round 2.

TICK-075. Re-scores the merged pool by SEED PROVENANCE, so the round-1 finding --
that the pre-launch citation cloud never pairs an exposure term with a fertility
term -- can be tested against round 2's deliberately axis-spanning seeds rather
than asserted again.

Exists as its own script because 219's inline version of this scoring was wrong:
`set(back) | set(fwd) & seeds` parses as `set(back) | (set(fwd) & seeds)`, which is
truthy for any record with a backward seed, and it reported a 2,010-record
"pre-launch cloud". The corrected expression parenthesises the union. Recomputing
from the saved pool costs nothing and keeps the arithmetic out of the pull script.

Scoring is TITLE-ONLY -- the pool carries no abstracts -- so every percentage is a
floor on the true rate.

Usage: python3 source/build/goldset/220_a23_cloud_scoring.py
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
LOGS = ROOT / "literature" / "search-logs"
POOL = LOGS / "co-residence-parents-household-delay-snowball-pool.json"
ANCHORS = LOGS / "co-residence-parents-household-delay-cold-start-anchors.json"
R2 = LOGS / "co-residence-parents-household-delay-snowball-round2.json"
OUT = LOGS / "co-residence-parents-household-delay-cloud-scoring.json"

PRELAUNCH = re.compile(
    r"co-?resid|living with (?:their )?parents?|liv\w* at home|parental (?:home|nest)|"
    r"leav\w* (?:the )?(?:parental |family )?(?:home|nest)|home-?leaving|nest-?leav|"
    r"boomerang|residential (?:independence|autonomy)|household formation|"
    r"transition to adulthood|young adults?", re.I)
EXTENDED = re.compile(
    r"multigenerational|three-?generation|extended (?:family )?household|stem family|"
    r"parents?-in-law|in-laws|grandparent|grandmother|grandfather|grandchild|"
    r"patrilocal|virilocal|intergenerational co-?resid", re.I)
FERT = re.compile(
    r"fertilit|childbear|child-?bearing|first birth|second birth|birth rate|"
    r"parenthood|childless|family size|number of children|tfr\b", re.I)
LABOUR = re.compile(
    r"labou?r (?:force|supply|market)|employment|female employment|maternal employment|"
    r"work(?:ing)? mothers?|wages?|hours worked|labor participation|labour participation", re.I)
ELDER = re.compile(
    r"elder|older (?:adults?|people|parents?)|ag(?:e)?ing|long-?term care|caregiv|"
    r"dementia|widow|filial|nursing home|frail", re.I)


def score(recs):
    n = len(recs) or 1
    def pct(rx, second=None):
        if second is None:
            k = sum(1 for r in recs if rx.search(r["title"] or ""))
        else:
            k = sum(1 for r in recs
                    if rx.search(r["title"] or "") and second.search(r["title"] or ""))
        return round(100 * k / n, 1)
    return {
        "n": len(recs),
        "exposure_prelaunch_pct": pct(PRELAUNCH),
        "exposure_extended_pct": pct(EXTENDED),
        "fertility_pct": pct(FERT),
        "prelaunch_x_fertility_pct": pct(PRELAUNCH, FERT),
        "extended_x_fertility_pct": pct(EXTENDED, FERT),
        "labour_supply_pct": pct(LABOUR),
        "eldercare_pct": pct(ELDER),
    }


def main():
    pool = json.loads(POOL.read_text())
    anchors = json.loads(ANCHORS.read_text())["anchors"]
    r2 = json.loads(R2.read_text())

    r1_prelaunch = {a["doi"] for a in anchors if a["provisional_cell"] == "PRIMARY_PRELAUNCH"}
    r1_extended = {a["doi"] for a in anchors if a["provisional_cell"] == "PRIMARY_EXTENDED_COUPLE"}
    r1_decoy = {a["doi"] for a in anchors if a["provenance_channel"] == "decoy"}
    r2_seeds = {g["doi"] for g in r2["existence_gate"] if g["existence"] == "FOUND"}

    def cloud(seed_dois):
        return [r for r in pool
                if (set(r["seeds_backward"]) | set(r["seeds_forward"])) & seed_dois]

    groups = {
        "whole_pool": pool,
        "round1_only": [r for r in pool if r.get("first_found_round") == 1],
        "round2_new": [r for r in pool if r.get("first_found_round") == 2],
        "cloud_r1_prelaunch_seeds": cloud(r1_prelaunch),
        "cloud_r2_prelaunch_seeds": cloud(r2_seeds),
        "cloud_all_prelaunch_seeds": cloud(r1_prelaunch | r2_seeds),
        "cloud_extended_seeds": cloud(r1_extended),
        "cloud_decoy_seeds_only": [r for r in pool
                                   if (set(r["seeds_backward"]) | set(r["seeds_forward"]))
                                   and (set(r["seeds_backward"]) | set(r["seeds_forward"])) <= r1_decoy],
        "multi_seed_3plus": [r for r in pool if r["n_seeds"] >= 3],
    }

    out = {k: score(v) for k, v in groups.items()}
    hdr = ("group", "n", "pre%", "ext%", "fert%", "pre×f", "ext×f", "lab%", "eld%")
    print(f"{hdr[0]:28s}{hdr[1]:>6}{hdr[2]:>7}{hdr[3]:>7}{hdr[4]:>7}{hdr[5]:>7}{hdr[6]:>7}{hdr[7]:>7}{hdr[8]:>7}")
    for k, v in out.items():
        print(f"{k:28s}{v['n']:>6}{v['exposure_prelaunch_pct']:>7}{v['exposure_extended_pct']:>7}"
              f"{v['fertility_pct']:>7}{v['prelaunch_x_fertility_pct']:>7}"
              f"{v['extended_x_fertility_pct']:>7}{v['labour_supply_pct']:>7}{v['eldercare_pct']:>7}")

    OUT.write_text(json.dumps({
        "meta": {
            "ticket": "TICK-075", "after_round": 2, "pool_size": len(pool),
            "scoring": "TITLE ONLY; every percentage is a floor, not an estimate.",
            "supersedes": "219's inline round-2 pre-launch figure (n=2010), which was an "
                          "operator-precedence bug: `set(a) | set(b) & seeds` parses as "
                          "`set(a) | (set(b) & seeds)`.",
        },
        "groups": out,
    }, indent=1))
    print(f"\nwrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
