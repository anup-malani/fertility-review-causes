#!/usr/bin/env python3
"""250 — A.18 recall audit: does the query miss gold, or does the gold miss the walls? TICK-076.

249's repaired query scored 59.8% against a proxy gold set built from the pool
(>=3 seeds, fertility word in title). That number is only as good as the gold, and
the standing lesson is to read a missed record's exposure BEFORE widening the query
— on A.23 that moved 8 of 19 gold out of the chapter entirely.

Reading all 37 misses here shows the same thing, larger. The proxy gold was built
on an OUTCOME word, so it admits every record about fertility regardless of whether
the exposure is genetic — which is precisely what walls 1 and 3 route out:

  Wall 1 (-> A.19)  parent-child fertility correlations with no decomposition.
                    Explicitly NOT evidence for A.18: equally consistent with pure
                    social transmission. Scope memo §7.
  Wall 3 (-> B.1)   phenotypic status -> reproductive success. The predictor is not
                    a genetic measure.
  No exposure       general fertility demography with no genetic content at all.

So the query refusing them is the walls working, not recall failing. This script
makes that claim auditable rather than asserted: it classifies every miss by an
explicit rule, prints each class in full, and reports recall both raw and net of
route-outs.

**These classifications are hypotheses, not findings.** They are keyed on titles,
and design is not a property of a title — A.23 carried a paper through search,
screen and priority retrieval as an administrative allocation when it was IPTW.
Every row here goes to the RA gate for confirmation against the abstract.

Usage: python3 source/build/goldset/250_a18_recall_audit.py
"""
import json
import os
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
LOGS = ROOT / "literature" / "search-logs"
OUT = LOGS / "heritability-fertility-genetic-recall-audit.json"
OUT_MD = LOGS / "heritability-fertility-genetic-recall-audit.md"

RULES = [
    ("WALL1_A19_TRANSMISSION", re.compile(
        r"intergenerational|across generations|generational|"
        r"fertility of parents and children|family size of parents|"
        r"parents and children|family influences on fertility|family systems and fertility", re.I)),
    ("WALL3_B1_STATUS", re.compile(
        r"\bstatus\b|high-status|social class|resource availability|"
        r"income and marriage|socioeconomic position", re.I)),
    ("A18_CANDIDATE", re.compile(
        r"genetic|heritab|cognitive ability|personality|maladaptive|"
        r"evolutionary perspective|fittest|long-term fitness|selection", re.I)),
    ("NO_GENETIC_EXPOSURE", re.compile(r".", re.I)),   # fall-through, and it is LOUD
]


def classify(title):
    for name, pat in RULES:
        if pat.search(title or ""):
            return name
    return "UNCLASSIFIED"


def main():
    rep = json.loads((LOGS / "heritability-fertility-genetic-production-query-repaired.json").read_text())
    pool = json.loads((LOGS / "heritability-fertility-genetic-snowball-pool.json").read_text())
    FERT = re.compile(r"\b(fertility|births?|children|childless|parity|family size|"
                      r"offspring|reproductive success|fecundity|childbearing)\b", re.I)
    indep = [r for r in pool if r["n_seeds"] >= 3 and FERT.search(r["title"] or "")]
    ids = [r["openalex"] for r in indep]

    key = ""
    for line in (ROOT / ".env").read_text().splitlines():
        if line.startswith("OPENALEX_API_KEY="):
            key = line.split("=", 1)[1].strip()
    hits = set()
    for i in range(0, len(ids), 50):
        args = ["curl", "-sS", "-G", "https://api.openalex.org/works",
                "--data-urlencode", f"filter=title_and_abstract.search:{rep['query']},"
                                    f"openalex_id:{'|'.join(ids[i:i+50])}",
                "--data-urlencode", "per-page=50", "--data-urlencode", "select=id",
                "--data-urlencode", f"api_key={key}"]
        d = json.loads(subprocess.run(args, capture_output=True, text=True).stdout)
        hits |= {w["id"].rsplit("/", 1)[-1] for w in d.get("results", [])}

    missed = [r for r in indep if r["openalex"] not in hits]
    for r in missed:
        r["miss_class"] = classify(r["title"])

    from collections import Counter, defaultdict
    counts = Counter(r["miss_class"] for r in missed)
    routed_out = sum(v for k, v in counts.items()
                     if k in ("WALL1_A19_TRANSMISSION", "WALL3_B1_STATUS", "NO_GENETIC_EXPOSURE"))
    real_misses = counts.get("A18_CANDIDATE", 0)

    raw = 100 * len(hits) / len(indep)
    net_denom = len(indep) - routed_out
    net = 100 * len(hits) / net_denom if net_denom else None

    by_class = defaultdict(list)
    for r in missed:
        by_class[r["miss_class"]].append(r)

    summary = {
        "proxy_gold": len(indep), "retrieved": len(hits), "missed": len(missed),
        "raw_pool_recall_pct": round(raw, 1),
        "missed_by_class": dict(counts),
        "route_outs_among_misses": routed_out,
        "genuine_a18_candidates_missed": real_misses,
        "net_pool_recall_pct": round(net, 1) if net else None,
        "net_denominator": net_denom,
        "caveat": "Classifications are title-keyed hypotheses for the RA gate, not findings. "
                  "Design is not a property of a title.",
    }
    OUT.write_text(json.dumps({"summary": summary, "missed": missed}, indent=1))

    md = [f"""# A.18 recall audit — the misses indict the gold, not the query

Proxy gold: {len(indep)} pool records (>=3 seeds, fertility word in title). Retrieved by the
repaired query: {len(hits)}. Missed: {len(missed)}.

- **Raw pool recall: {raw:.1f}%**
- **Net of wall route-outs: {net:.1f}%** ({len(hits)}/{net_denom})
- Genuine A.18 candidates missed: **{real_misses}**

The proxy gold was built on an OUTCOME word, so it admits any record about fertility whether or
not the exposure is genetic. Walls 1 and 3 exist to route exactly those out. The query refusing
them is the walls working.

**Every classification below is a title-keyed hypothesis for the RA gate.** Design is not a
property of a title.
"""]
    for cls in ("A18_CANDIDATE", "WALL1_A19_TRANSMISSION", "WALL3_B1_STATUS",
                "NO_GENETIC_EXPOSURE", "UNCLASSIFIED"):
        rs = by_class.get(cls, [])
        if not rs:
            continue
        md.append(f"\n## {cls} — {len(rs)}\n")
        for r in sorted(rs, key=lambda x: -(x["cited_by"] or 0)):
            md.append(f"- {(r['title'] or '')[:100]}  \n  *{r['venue'] or '—'}*, "
                      f"{r['year']}, cited {r['cited_by']}")
    OUT_MD.write_text("\n".join(md) + "\n")

    print(json.dumps(summary, indent=1))
    print(f"\nwrote {OUT.relative_to(ROOT)} and {OUT_MD.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
