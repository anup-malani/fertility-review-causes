#!/usr/bin/env python3
"""247 — A.18 pool diagnostics: how much of the snowball pool is the homonym? TICK-076.

The chapter's central retrieval problem is that "fertility" means births per woman
here, conception rate in animal science, and nutrient status in agronomy — and the
METHOD vocabulary (heritability, selection differential, breeder's equation) is
shared exactly across all three. §6 of the scope memo sized this with a fulltext
probe, which measures the contaminated space rather than our pool. This measures
our pool.

Measured on two channels that fail differently, because a contamination estimate
from a term list I wrote is an estimate of my term list:

  channel A — OpenAlex `topics`, machine-assigned, independent of anything here.
  channel B — a term list over title and venue.

The cross-tab is the output that matters. Agreement is evidence; the disagreement
cells are where the term list is wrong, and they are printed for reading rather
than summarised away. Per validate-fixes-at-scale, read what a filter REJECTS as
well as what it admits.

Usage: python3 source/build/goldset/247_a18_pool_diagnostics.py
"""
import json
import re
import subprocess
import time
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
LOGS = ROOT / "literature" / "search-logs"
POOL = LOGS / "heritability-fertility-genetic-snowball-pool.json"
OUT = LOGS / "heritability-fertility-genetic-pool-diagnostics.json"
OUT_MD = LOGS / "heritability-fertility-genetic-pool-diagnostics.md"
API = "https://api.openalex.org/works"

# Channel B. Terms chosen to name the CLOUD, never to name the positives: the
# standing lesson is that positives labelled by vocabulary get labelled by the
# vocabulary's blind spots. A cloud is a different object and may be named.
NONHUMAN = re.compile(r"\b("
    r"cattle|dairy|bull|heifer|cow|calf|calves|bovine|sow|boar|piglet|swine|porcine|"
    r"poultry|broiler|hen|chicken|layer|sheep|ewe|ram|ovine|goat|caprine|buffalo|"
    r"stallion|mare|equine|salmon|tilapia|shrimp|aquaculture|silkworm|honeybee|"
    r"mice|mouse|murine|rat|rats|drosophila|nematode|c\.? elegans|zebrafish|"
    r"maize|wheat|rice|barley|sorghum|soybean|cotton|tomato|arabidopsis|cultivar|"
    r"hybrid seed|male sterility|pollen|anther|agronom|crop|soil|fertiliser|fertilizer|"
    r"livestock|herd|breeding value"
    r")\b", re.I)

HUMAN_DEMOG = re.compile(r"\b("
    r"fertility decline|demographic transition|completed fertility|children ever born|"
    r"age at first birth|childlessness|parity|total fertility rate|tfr|"
    r"human fertility|reproductive behaviou?r|family size"
    r")\b", re.I)

# OpenAlex fields whose presence is prima facie evidence of the cloud (channel A).
CLOUD_FIELDS = {"Agricultural and Biological Sciences"}
CLOUD_SUBFIELDS = {"Animal Science and Zoology", "Agronomy and Crop Science",
                   "Soil Science", "Food Science", "Horticulture", "Plant Science",
                   "Insect Science", "Aquatic Science"}
# NOT "Ecology, Evolution, Behavior and Systematics": the first run swept it and caught
# Lande & Arnold 1983, Kingsolver 2001 and Schluter 1994 -- the estimator canon the
# SELECTION arm is built on. A filter validated only on what it admits would have kept it.
# Wall 5 / Wall 4, measured. The pool is dominated by behaviour genetics and
# sociogenomics of phenotypes that are not fertility -- educational attainment,
# cognition, psychiatric traits. That, not livestock, is what the screen must reject.
FERT_PHENO = re.compile(r"\b("
    r"fertility|fertilit|births?|childbearing|children ever born|childless|parity|"
    r"family size|offspring|reproducti\w+|fecundity|fecundability|age at first birth|"
    r"number of children|completed famil|natalit|birth rate|tfr"
    r")\b", re.I)
OTHER_PHENO = re.compile(r"\b("
    r"educational attainment|education\w* (?:attainment|achievement)|intelligence|"
    r"cognitiv\w+|iq\b|height|body mass|bmi|obesity|smoking|alcohol|depression|"
    r"schizophreni\w+|psychiatric|personality|wellbeing|well-being|longevity|lifespan|"
    r"disease risk|cancer|diabetes|blood pressure"
    r")\b", re.I)

HUMAN_SUBFIELDS = {"Demography", "Sociology and Political Science", "Genetics",
                   "Molecular Biology", "Public Health, Environmental and "
                   "Occupational Health", "Obstetrics and Gynecology",
                   "Anthropology", "Economics and Econometrics", "Epidemiology"}


def api_key():
    for line in (ROOT / ".env").read_text().splitlines():
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
    for attempt in range(tries):
        r = subprocess.run(args, capture_output=True, text=True)
        if r.returncode == 0:
            try:
                d = json.loads(r.stdout)
            except Exception:
                time.sleep(5 * (attempt + 1)); continue
            if "meta" in d:
                return d, None
        time.sleep(5 * (attempt + 1))
    return None, "failed"


def main():
    pool = json.loads(POOL.read_text())
    ids = [r["openalex"] for r in pool]
    by_id = {r["openalex"]: r for r in pool}

    cache_path = ROOT / "temp" / "a18" / "heritability-fertility-genetic-pool-topics-cache.json"
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    cached = json.loads(cache_path.read_text()) if cache_path.exists() else {}
    missing = [i for i in ids if i not in cached]
    print(f"topics: {len(ids)-len(missing)} cached, {len(missing)} to hydrate")
    topics = {i: cached[i] for i in ids if i in cached}
    ids_to_pull = missing
    for i in range(0, len(ids_to_pull), 50):
        batch = ids_to_pull[i:i + 50]
        d, err = get([("filter", "openalex_id:" + "|".join(batch)),
                      ("per-page", "50"), ("select", "id,topics")])
        if err:
            print(f"  FAILED batch {i}")
            continue
        for w in d.get("results", []):
            topics[w["id"].rsplit("/", 1)[-1]] = w.get("topics") or []
        if i % 500 == 0:
            print(f"  {min(i+50, len(ids_to_pull))}/{len(ids_to_pull)}")
    cache_path.write_text(json.dumps({**cached, **topics}))

    rows = []
    for r in pool:
        ts = topics.get(r["openalex"], [])
        top = ts[0] if ts else {}
        field = ((top.get("field") or {}).get("display_name"))
        subfield = ((top.get("subfield") or {}).get("display_name"))
        text = f"{r.get('title') or ''} {r.get('venue') or ''}"
        b_nonhuman = bool(NONHUMAN.search(text))
        b_human = bool(HUMAN_DEMOG.search(text))
        p_fert = bool(FERT_PHENO.search(r.get("title") or ""))
        p_other = bool(OTHER_PHENO.search(r.get("title") or ""))
        # The field-level rule is a fallback for a MISSING subfield only. Applying it
        # whenever the field matched swept "Ecology, Evolution, Behavior and Systematics"
        # -- which sits under Agricultural and Biological Sciences -- and with it the
        # selection-estimator canon. Removing that subfield from CLOUD_SUBFIELDS changed
        # nothing, because the field rule caught it anyway: right answer, wrong mechanism.
        a_cloud = (subfield in CLOUD_SUBFIELDS) or (subfield is None and field in CLOUD_FIELDS)
        a_human = subfield in HUMAN_SUBFIELDS
        rows.append({**{k: r[k] for k in ("openalex", "title", "year", "venue",
                                          "cited_by", "n_seeds", "seed_arms")},
                     "topic_field": field, "topic_subfield": subfield,
                     "A_cloud": a_cloud, "A_human": a_human,
                     "P_fertility_phenotype": p_fert, "P_other_phenotype": p_other,
                     "B_nonhuman": b_nonhuman, "B_humandemog": b_human,
                     "topics_missing": not ts})

    xtab = Counter((r["A_cloud"], r["B_nonhuman"]) for r in rows)
    by_arm = defaultdict(lambda: {"n": 0, "A_cloud": 0, "B_nonhuman": 0, "either": 0})
    for r in rows:
        for a in (r["seed_arms"] or ["<none>"]):
            s = by_arm[a]
            s["n"] += 1
            s["A_cloud"] += r["A_cloud"]
            s["B_nonhuman"] += r["B_nonhuman"]
            s["either"] += (r["A_cloud"] or r["B_nonhuman"])

    pheno = Counter((r["P_fertility_phenotype"], r["P_other_phenotype"]) for r in rows)
    subfields = Counter(r["topic_subfield"] for r in rows).most_common(20)
    venues = Counter(r["venue"] for r in rows if r["venue"]).most_common(20)

    disagree_A_not_B = [r for r in rows if r["A_cloud"] and not r["B_nonhuman"]]
    disagree_B_not_A = [r for r in rows if r["B_nonhuman"] and not r["A_cloud"]]

    summary = {
        "pool_size": len(rows),
        "topics_missing": sum(1 for r in rows if r["topics_missing"]),
        "A_cloud": sum(1 for r in rows if r["A_cloud"]),
        "B_nonhuman": sum(1 for r in rows if r["B_nonhuman"]),
        "either_channel": sum(1 for r in rows if r["A_cloud"] or r["B_nonhuman"]),
        "both_channels": xtab[(True, True)],
        "A_only": xtab[(True, False)],
        "B_only": xtab[(False, True)],
        "neither": xtab[(False, False)],
        "A_human_subfield": sum(1 for r in rows if r["A_human"]),
        "B_human_demography_terms": sum(1 for r in rows if r["B_humandemog"]),
        "phenotype_fertility_only": pheno[(True, False)],
        "phenotype_other_only": pheno[(False, True)],
        "phenotype_both": pheno[(True, True)],
        "phenotype_neither_visible_in_title": pheno[(False, False)],
        "by_seed_arm": {k: dict(v) for k, v in sorted(by_arm.items())},
        "top_subfields": subfields,
        "top_venues": venues,
    }

    OUT.write_text(json.dumps({"summary": summary, "rows": rows}, indent=1))

    def fmt(rs, n=15):
        return "\n".join(
            f"- {(r['title'] or '')[:96]}  \n  *{r['venue'] or '—'}*, {r['year']} — "
            f"topic: {r['topic_subfield'] or '—'}" for r in rs[:n])

    OUT_MD.write_text(f"""# A.18 pool diagnostics — the homonym, measured on the pool

Pool: {len(rows)} records from the 25-anchor snowball (246). Nothing here is screened.

## The two channels

| | channel B says non-human | B says nothing |
|---|---|---|
| **channel A says cloud** | {xtab[(True, True)]} | {xtab[(True, False)]} |
| **A says nothing** | {xtab[(False, True)]} | {xtab[(False, False)]} |

Either channel flags **{summary['either_channel']} of {len(rows)}**
({100*summary['either_channel']/len(rows):.1f}%). Both agree on {xtab[(True, True)]}.
{summary['topics_missing']} records carry no OpenAlex topic, so channel A cannot see them.

## Contamination by seed arm

| arm | reached | A: cloud | B: non-human | either | either % |
|---|---|---|---|---|---|
""" + "\n".join(
        f"| {k} | {v['n']} | {v['A_cloud']} | {v['B_nonhuman']} | {v['either']} | "
        f"{100*v['either']/v['n']:.1f}% |"
        for k, v in sorted(by_arm.items())) + f"""

## Top subfields

""" + "\n".join(f"- {s or '—'}: {n}" for s, n in subfields) + """

## Where the channels disagree — read these, do not summarise them

### A flags cloud, B does not (term list missed it)

""" + fmt(disagree_A_not_B) + """

### B flags non-human, A does not (term list may be over-reaching)

""" + fmt(disagree_B_not_A) + "\n")

    print("\n" + json.dumps({k: v for k, v in summary.items()
                             if k not in ("top_subfields", "top_venues", "by_seed_arm")}, indent=1))
    print("\nby seed arm:")
    for k, v in sorted(by_arm.items()):
        print(f"  {k:10s} n={v['n']:5d}  either={v['either']:5d}  {100*v['either']/v['n']:5.1f}%")
    print("\ntop subfields:")
    for s, n in subfields[:12]:
        print(f"  {n:5d}  {s}")
    print(f"\nwrote {OUT.relative_to(ROOT)} and {OUT_MD.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
