#!/usr/bin/env python3
"""248 — A.18 production query: construction, variant scoring, gold-recall floor test. TICK-076.

Two axes (GENETIC × FERTILITY) per the 2026-06-20 decision: the boolean layer
optimises RECALL and the LLM screen optimises precision, because a false negative
at the search stage is unrecoverable and a false positive is not. No mechanism
axis.

Recall is MEASURED, not estimated: for each anchor, ask OpenAlex whether that
exact work sits inside the query's result set, via
`filter=title_and_abstract.search:<Q>,openalex_id:<W...>`. A work either matches
or it does not.

**What this test is and is not.** The 25 anchors are the snowball's own seeds, so
anchor recall is a FLOOR test — a query that cannot retrieve its own anchors is
broken — not an unbiased recall estimate. The independent estimate comes from the
pool: §b scores each variant against high-multi-seed pool records the anchors did
not supply, which is a channel that failed differently.

Variants, so the choices are visible rather than asserted:
  V1  full genetic axis × fertility axis            -- the candidate
  V2  V1 minus the evolutionary-fitness vocabulary  -- what that family is worth
  V3  V1 plus moderation vocabulary                 -- H2_MOD is the thinnest arm
  V4  fertility axis ALONE                          -- the outcome-only arm
  V5  genetic axis ALONE                            -- the exposure-only arm

V4 and V5 exist because a conjunction can be dominated by one of its arms and the
only way to know is to measure each arm. Every term is ALSO scored alone (§c):
an axis is a block of assumptions until each member has been run by itself, and
on this hypothesis "fertility" and "heritability" each carry a large homonym.

Query-syntax hazards this file is written around: a comma in a FILTER VALUE is
fatal and %2C does not save it; `?` is a wildcard and `!` is negation; a phrase
beginning with a stopword loses it; a phrase beginning with "not" parses as
boolean NOT and silently returns an unrestricted count. No term below contains
any of these.

Usage: python3 source/build/goldset/248_a18_production_query.py
"""
import json
import re
import subprocess
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
LOGS = ROOT / "literature" / "search-logs"
ANCHORS = LOGS / "heritability-fertility-genetic-cold-start-anchors.json"
POOL = LOGS / "heritability-fertility-genetic-snowball-pool.json"
OUT = LOGS / "heritability-fertility-genetic-production-query.json"
OUT_MD = LOGS / "heritability-fertility-genetic-production-query.md"
API = "https://api.openalex.org/works"

# --- the axes -------------------------------------------------------------
# GENETIC: how the exposure is measured. Deliberately spans three vocabularies
# that do not co-occur -- behaviour genetics (twin/heritability), molecular
# (GWAS/polygenic), and evolutionary quantitative genetics (selection/fitness) --
# because the chapter's three arms are indexed in three different literatures.
GENETIC_BEHAV = ['"heritability"', '"heritable"', '"twin study"', '"twin studies"',
                 '"monozygotic"', '"dizygotic"', '"behaviour genetic"',
                 '"behavior genetic"', '"adoption study"']
GENETIC_MOLEC = ['"polygenic score"', '"polygenic index"', '"genome-wide association"',
                 '"GWAS"', '"SNP heritability"', '"genetic variance"',
                 '"additive genetic"', '"within-sibship"']
GENETIC_EVOL = ['"natural selection"', '"selection differential"', '"selection gradient"',
                '"response to selection"', '"quantitative genetics"', '"pedigree"']

FERTILITY = ['"fertility"', '"children ever born"', '"completed fertility"',
             '"number of children"', '"family size"', '"age at first birth"',
             '"childlessness"', '"childless"', '"parity"',
             '"reproductive success"', '"offspring number"', '"fecundity"']

MODERATION = ['"gene-environment interaction"', '"nature and nurture"',
              '"across cohorts"', '"cohort differences"']


def OR(terms):
    return "(" + " OR ".join(terms) + ")"


GENETIC_ALL = GENETIC_BEHAV + GENETIC_MOLEC + GENETIC_EVOL
VARIANTS = {
    "V1_genetic_x_fertility": f"{OR(GENETIC_ALL)} AND {OR(FERTILITY)}",
    "V2_no_evolutionary_family": f"{OR(GENETIC_BEHAV + GENETIC_MOLEC)} AND {OR(FERTILITY)}",
    "V3_plus_moderation": f"{OR(GENETIC_ALL + MODERATION)} AND {OR(FERTILITY)}",
    "V4_fertility_only": OR(FERTILITY),
    "V5_genetic_only": OR(GENETIC_ALL),
}

BAD = re.compile(r"[,?!]")


def api_key():
    for line in (ROOT / ".env").read_text().splitlines():
        if line.startswith("OPENALEX_API_KEY="):
            return line.split("=", 1)[1].strip()
    return ""


KEY = api_key()


def get(params, tries=3):
    args = ["curl", "-sS", "--max-time", "180", "--get", API]
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
            last = str(d["error"])[:90]; time.sleep(10 * (attempt + 1)); continue
        if "meta" not in d:
            last = "no meta - refused, NOT empty"; time.sleep(10 * (attempt + 1)); continue
        return d, None
    return None, last


def members(query, ids):
    """Which of `ids` sit inside `query`? Measured, not sampled."""
    hits, err = set(), None
    for i in range(0, len(ids), 50):
        batch = ids[i:i + 50]
        d, e = get([("filter", f"title_and_abstract.search:{query},"
                               f"openalex_id:{'|'.join(batch)}"),
                    ("per-page", "50"), ("select", "id")])
        if e:
            err = e
            continue
        for w in d.get("results", []):
            hits.add(w["id"].rsplit("/", 1)[-1])
    return hits, err


def count(query):
    d, e = get([("filter", f"title_and_abstract.search:{query}"),
                ("per-page", "1"), ("select", "id")])
    return (d["meta"]["count"] if d else None), e


def main():
    for name, q in VARIANTS.items():
        assert not BAD.search(q), f"{name} carries a comma/?/! -- would break the filter"

    anchors = json.loads(ANCHORS.read_text())
    anchor_ids = [a["top_candidate"]["oa_id"].rsplit("/", 1)[-1] for a in anchors]
    meta = {i: a for i, a in zip(anchor_ids, anchors)}

    pool = json.loads(POOL.read_text())
    # Independent gold: pool records reached by >=3 seeds that name a fertility
    # outcome in the title. Not anchors, so not circular; unscreened, so a
    # proxy for relevance and labelled as one.
    FERT_T = re.compile(r"\b(fertility|births?|children|childless|parity|family size|"
                        r"offspring|reproductive success|fecundity|childbearing)\b", re.I)
    indep = [r for r in pool if r["n_seeds"] >= 3 and FERT_T.search(r["title"] or "")]
    indep_ids = [r["openalex"] for r in indep]
    print(f"anchors: {len(anchor_ids)}   independent pool gold: {len(indep_ids)}\n")

    results = {}
    for name, q in VARIANTS.items():
        n, cerr = count(q)
        hits, herr = members(q, anchor_ids)
        ihits, ierr = members(q, indep_ids)
        missed = [meta[i] for i in anchor_ids if i not in hits]
        results[name] = {
            "query": q,
            "frame_size": n, "count_error": cerr,
            "anchor_recall": f"{len(hits)}/{len(anchor_ids)}",
            "anchor_recall_pct": round(100 * len(hits) / len(anchor_ids), 1),
            "anchor_misses": [{"arm": m["arm"], "first_author": m["first_author"],
                               "year": m["top_candidate"]["year"],
                               "title": m["top_candidate"]["title"]} for m in missed],
            "pool_recall": f"{len(ihits)}/{len(indep_ids)}",
            "pool_recall_pct": round(100 * len(ihits) / max(len(indep_ids), 1), 1),
            "errors": [e for e in (herr, ierr) if e],
        }
        print(f"{name:28s} frame={str(n):>9s}  anchors={results[name]['anchor_recall']:>6s} "
              f"({results[name]['anchor_recall_pct']:5.1f}%)  pool={results[name]['pool_recall']:>8s} "
              f"({results[name]['pool_recall_pct']:5.1f}%)")

    # --- per-term solo scoring -------------------------------------------
    print("\nper-term solo scores (an axis is a block of assumptions until each member is run alone)")
    solo = {}
    for axis, terms in (("GENETIC", GENETIC_ALL), ("FERTILITY", FERTILITY),
                        ("MODERATION", MODERATION)):
        for t in terms:
            n, _ = count(t)
            hits, _ = members(t, anchor_ids)
            ihits, _ = members(t, indep_ids)
            solo[t] = {"axis": axis, "frame_size": n,
                       "anchors": len(hits), "pool_gold": len(ihits)}
            print(f"  {axis:11s} {t:32s} frame={str(n):>10s}  anchors={len(hits):2d}/25  "
                  f"pool={len(ihits):3d}/{len(indep_ids)}")

    payload = {"meta": {"ticket": "TICK-076",
                        "anchors": len(anchor_ids),
                        "independent_pool_gold": len(indep_ids),
                        "note": "Anchor recall is a FLOOR test - the anchors seeded the pool. "
                                "Pool recall is the independent-channel estimate."},
               "variants": results, "per_term": solo,
               "independent_gold": [{"openalex": r["openalex"], "title": r["title"],
                                     "year": r["year"], "n_seeds": r["n_seeds"]}
                                    for r in indep]}
    OUT.write_text(json.dumps(payload, indent=1))
    print(f"\nwrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
