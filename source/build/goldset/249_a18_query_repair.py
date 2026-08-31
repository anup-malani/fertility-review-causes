#!/usr/bin/env python3
"""249 — A.18 production query, repaired and scored leave-one-out. TICK-076.

248 measured the candidate conjunction at 64% anchor recall and 54% pool recall
— a 46% false-negative rate, past the 20% threshold the 2026-06-20 decision set
for revisiting a query. The misses were not random: seven of the nine SELECTION
anchors, including Kong, Beauchamp, Byars, Sanjak and Milot.

Reading the missed records rather than widening blindly found the cause. **In the
evolutionary-selection sub-literature the fertility outcome is called `fitness`.**
Byars 2009, Beauchamp 2016, Milot 2011 and Sanjak 2017 report selection on
lifetime reproductive success and none of them needs the word "fertility" to do
it. Two smaller gaps: bare `twins` (the axis had only "twin study", so Kohler
2002's "Danish twin cohorts" failed) and `genotype`.

Every term is then scored LEAVE-ONE-OUT: drop it from the full query and measure
what the frame and the gold lose. That is the only way to separate a term that
adds records from a term that adds relevant records, and on this hypothesis the
difference is large — "parity" carries a 240,805-record frame for zero anchors.

A term that names an ENUMERATED DESIGN (scope memo §5) is kept even at zero yield,
provided its frame cost is small: those terms exist so that an empty cell is empty
against an auditable list. Cheap-and-zero is not the same as dead weight.

Usage: python3 source/build/goldset/249_a18_query_repair.py
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
OUT = LOGS / "heritability-fertility-genetic-production-query-repaired.json"
API = "https://api.openalex.org/works"

# Stemming note, measured in 248: OpenAlex stems, so "heritable"=="heritability",
# "twin studies"=="twin study" and "childless"=="childlessness" returned identical
# frames and identical gold. The duplicates are dropped; they were doing no work.
GENETIC = [
    '"heritability"', '"twin study"', '"twins"', '"monozygotic"', '"dizygotic"',
    '"behavior genetic"', '"behaviour genetic"', '"adoption study"',
    '"polygenic score"', '"polygenic index"', '"genome-wide association"',
    '"SNP heritability"', '"genetic variance"', '"additive genetic"',
    '"within-sibship"', '"genotype"',
    '"natural selection"', '"selection differential"', '"selection gradient"',
    '"response to selection"', '"quantitative genetics"',
]
FERTILITY = [
    '"fertility"', '"children ever born"', '"completed fertility"',
    '"number of children"', '"family size"', '"age at first birth"',
    '"childlessness"', '"reproductive success"', '"reproductive output"',
    '"offspring number"', '"fecundity"', '"fitness"',
]
# Terms that name an enumerated design in scope-memo §5 and are kept at zero yield
# so long as they are cheap. Recorded so the decision is auditable, not tacit.
DESIGN_TERMS = {'"adoption study"', '"polygenic index"', '"selection differential"',
                '"selection gradient"', '"within-sibship"', '"SNP heritability"'}
# Dropped by 248 for high frame cost at zero gold: measured, not assumed.
DROPPED = {'"parity"': "240,805 frame / 0 anchors / 3 pool",
           '"pedigree"': "63,967 frame / 0 anchors / 0 pool",
           '"GWAS"': "75,753 frame; subsumed by genome-wide association",
           '"heritable"': "stemming duplicate of heritability",
           '"twin studies"': "stemming duplicate of twin study",
           '"childless"': "stemming duplicate of childlessness"}

BAD = re.compile(r"[,?!]")


def OR(ts):
    return "(" + " OR ".join(ts) + ")"


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
    for attempt in range(tries):
        r = subprocess.run(args, capture_output=True, text=True)
        if r.returncode == 0:
            try:
                d = json.loads(r.stdout)
            except Exception:
                time.sleep(5 * (attempt + 1)); continue
            if "meta" in d and "error" not in d:
                return d, None
        time.sleep(5 * (attempt + 1))
    return None, "failed"


def members(query, ids):
    hits = set()
    for i in range(0, len(ids), 50):
        d, e = get([("filter", f"title_and_abstract.search:{query},"
                               f"openalex_id:{'|'.join(ids[i:i+50])}"),
                    ("per-page", "50"), ("select", "id")])
        if e:
            continue
        for w in d.get("results", []):
            hits.add(w["id"].rsplit("/", 1)[-1])
    return hits


def count(query):
    d, e = get([("filter", f"title_and_abstract.search:{query}"),
                ("per-page", "1"), ("select", "id")])
    return (d["meta"]["count"] if d else None)


def main():
    anchors = json.loads(ANCHORS.read_text())
    aids = [a["top_candidate"]["oa_id"].rsplit("/", 1)[-1] for a in anchors]
    meta = {i: a for i, a in zip(aids, anchors)}

    pool = json.loads(POOL.read_text())
    FERT_T = re.compile(r"\b(fertility|births?|children|childless|parity|family size|"
                        r"offspring|reproductive success|fecundity|childbearing)\b", re.I)
    indep = [r["openalex"] for r in pool
             if r["n_seeds"] >= 3 and FERT_T.search(r["title"] or "")]

    Q = f"{OR(GENETIC)} AND {OR(FERTILITY)}"
    assert not BAD.search(Q)

    n = count(Q)
    ah, ih = members(Q, aids), members(Q, indep)
    print(f"REPAIRED  frame={n:,}  anchors={len(ah)}/{len(aids)} "
          f"({100*len(ah)/len(aids):.1f}%)  pool={len(ih)}/{len(indep)} "
          f"({100*len(ih)/len(indep):.1f}%)")
    misses = [meta[i] for i in aids if i not in ah]
    for m in misses:
        print(f"  still missing: {m['arm']:10s} {m['first_author']} "
              f"{m['top_candidate']['year']} — {(m['top_candidate']['title'] or '')[:60]}")

    # --- leave-one-out --------------------------------------------------------
    print("\nleave-one-out: what does each term actually buy?")
    loo = {}
    for axis, terms in (("GENETIC", GENETIC), ("FERTILITY", FERTILITY)):
        for t in terms:
            rest = [x for x in terms if x != t]
            if not rest:
                continue
            q = (f"{OR(rest)} AND {OR(FERTILITY)}" if axis == "GENETIC"
                 else f"{OR(GENETIC)} AND {OR(rest)}")
            n2 = count(q)
            a2, i2 = members(q, aids), members(q, indep)
            loo[t] = {"axis": axis,
                      "frame_without": n2, "frame_cost": (n - n2) if n2 is not None else None,
                      "anchors_without": len(a2), "anchors_gain": len(ah) - len(a2),
                      "pool_without": len(i2), "pool_gain": len(ih) - len(i2),
                      "names_enumerated_design": t in DESIGN_TERMS}
            g = loo[t]
            tag = ""
            if g["anchors_gain"] == 0 and g["pool_gain"] == 0:
                tag = "  KEEP (names a §5 design)" if g["names_enumerated_design"] else "  <-- buys nothing"
            print(f"  {axis:9s} {t:28s} frame+{str(g['frame_cost']):>8s}  "
                  f"anchors+{g['anchors_gain']}  pool+{g['pool_gain']}{tag}")

    payload = {
        "meta": {"ticket": "TICK-076",
                 "supersedes": "248 V1 (64% anchor / 54% pool recall)",
                 "repair": "added 'fitness', 'twins', 'genotype'; dropped 6 terms",
                 "dropped_with_reason": DROPPED,
                 "note": "Anchor recall is a floor test; pool recall is the independent estimate."},
        "query": Q, "frame_size": n,
        "anchor_recall": f"{len(ah)}/{len(aids)}",
        "anchor_recall_pct": round(100 * len(ah) / len(aids), 1),
        "pool_recall": f"{len(ih)}/{len(indep)}",
        "pool_recall_pct": round(100 * len(ih) / len(indep), 1),
        "remaining_misses": [{"arm": m["arm"], "first_author": m["first_author"],
                              "year": m["top_candidate"]["year"],
                              "title": m["top_candidate"]["title"]} for m in misses],
        "leave_one_out": loo,
    }
    OUT.write_text(json.dumps(payload, indent=1))
    print(f"\nwrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
