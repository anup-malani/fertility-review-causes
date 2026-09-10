#!/usr/bin/env python3
"""
386 — C.3.f: how much of the ungated FLOW_MEASUREMENT channel is the finance homonym.

384 added a channel that runs UNGATED by the outcome axis, because §9's `FLOW_MEASUREMENT` cell is
defined by the ABSENCE of a fertility outcome and no gated channel could reach it. That was the
right fix. The probe's tail then showed what it cost: stratum 8 screened 19 of 25 OFF_TOPIC, and the
19 are one literature — family offices, estate planning, bequest taxation, wealth mobility, private
banking. `intergenerational wealth` is a finance term before it is a demographic one, and without
the outcome axis nothing was holding it down.

This measures the damage locally, on the already-hydrated text, at no API cost: which flow-accounting
term each ungated record actually matches, and how many carry finance vocabulary. Then it prices the
obvious fix — dropping `intergenerational wealth` from that channel only — against what it would
cost in records this chapter wants.

`term-acceptance-needs-a-price-ceiling` in reverse: a term is dropped on what it costs, and kept on
what it uniquely reaches, and both numbers go on the page.

Output literature/search-logs/c3f-flowmeas-contamination-<date>.{json,md}. No network access.
"""
import json, re, sys, datetime, pathlib, collections

ROOT = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "source" / "lib"))
import textnorm                                                    # noqa: E402

LOGS = ROOT / "literature" / "search-logs"
DATE = datetime.date.today().isoformat()
HYDRATED = ROOT / "temp" / "c3f-universe-hydrated.json"

FLOW_TERMS = ["wealth flows", "intergenerational wealth", "National Transfer Accounts",
              "lifecycle deficit", "life cycle deficit", "intergenerational resource flows",
              "flow of wealth", "net intergenerational transfer"]

# Vocabulary of the literature the tail turned out to be. Chosen from the 19 OFF_TOPIC records in
# stratum 8, not invented: family offices, estate planning, bequest taxation, wealth mobility.
FINANCE = ["estate", "bequest", "inheritance tax", "portfolio", "private banking", "family office",
           "wealth mobility", "wealth inequality", "capital flight", "tax", "asset", "philanthrop",
           "wealth transmission", "wealth concentration", "savings behavior", "savings behaviour"]
# The demographic signal that should be present if a record belongs in FLOW_MEASUREMENT at all.
DEMOG = ["fertility", "childbearing", "birth", "children", "child", "family size", "age profile",
         "generational economy", "life cycle", "lifecycle", "demographic", "population"]


def main():
    if not HYDRATED.exists():
        sys.exit("run 385 --hydrate first")
    recs = json.loads(HYDRATED.read_text())["records"]
    only_fm, both = [], []
    for r in recs:
        prov = {p.split(":")[0] for p in r.get("provenance") or []}
        if prov == {"FLOWMEAS"}:
            only_fm.append(r)
        elif "FLOWMEAS" in prov:
            both.append(r)

    print(f"universe {len(recs):,}")
    print(f"  reachable ONLY by the ungated channel: {len(only_fm):,}")
    print(f"  also reachable by a gated channel:     {len(both):,}")

    def terms_in(r):
        blob = textnorm.norm(f"{r.get('title','')} {r.get('abstract','')}")
        return [t for t in FLOW_TERMS if textnorm.norm(t) in blob]

    by_term = collections.Counter()
    finance_hits, demog_hits, iw_only = 0, 0, []
    for r in only_fm:
        ts = terms_in(r)
        for t in ts:
            by_term[t] += 1
        blob = textnorm.norm(f"{r.get('title','')} {r.get('abstract','')}")
        fin = any(textnorm.norm(f) in blob for f in FINANCE)
        dem = any(textnorm.norm(d) in blob for d in DEMOG)
        finance_hits += fin
        demog_hits += dem
        if ts == ["intergenerational wealth"]:
            iw_only.append({"id": r["id"], "title": r.get("title"), "year": r.get("year"),
                            "finance": fin, "demographic": dem})

    print("\n== which flow-accounting term the ungated-only records match ==")
    for t, n in by_term.most_common():
        print(f"  {n:>5}  {t}")
    print(f"\n  carrying finance vocabulary:     {finance_hits:,} of {len(only_fm):,} "
          f"({100 * finance_hits / max(len(only_fm), 1):.0f}%)")
    print(f"  carrying demographic vocabulary: {demog_hits:,} of {len(only_fm):,} "
          f"({100 * demog_hits / max(len(only_fm), 1):.0f}%)")

    n_iw = len(iw_only)
    iw_fin = sum(1 for r in iw_only if r["finance"])
    iw_dem_only = sum(1 for r in iw_only if r["demographic"] and not r["finance"])
    print(f"\n== the fix: drop 'intergenerational wealth' from the UNGATED channel only ==")
    print(f"  records reached by that term ALONE: {n_iw:,}")
    print(f"    of which carry finance vocabulary:            {iw_fin:,} "
          f"({100 * iw_fin / max(n_iw, 1):.0f}%)")
    print(f"    of which are demographic and NOT finance:     {iw_dem_only:,}  <- the cost of the fix")
    print("\n  a sample of what dropping it would lose (demographic, not finance):")
    shown = 0
    for r in iw_only:
        if r["demographic"] and not r["finance"] and shown < 12:
            print(f"    {r['year']}  {(r['title'] or '')[:88]}")
            shown += 1

    blob = {"date": DATE, "universe": len(recs), "only_flowmeas": len(only_fm),
            "also_gated": len(both), "by_term": dict(by_term),
            "finance_vocab": finance_hits, "demographic_vocab": demog_hits,
            "intergenerational_wealth_only": n_iw, "iw_finance": iw_fin,
            "iw_demographic_not_finance": iw_dem_only,
            "would_lose": [r for r in iw_only if r["demographic"] and not r["finance"]]}
    (LOGS / f"c3f-flowmeas-contamination-{DATE}.json").write_text(json.dumps(blob, indent=2) + "\n")

    md = [f"# C.3.f — the ungated channel's homonym cost — {DATE}", "",
          "Generated by `source/build/goldset/386_c3f_flowmeas_contamination.py`. Local only.", "",
          f"- universe: **{len(recs):,}**",
          f"- reachable only by the ungated FLOW_MEASUREMENT channel: **{len(only_fm):,}**",
          f"- of those, carrying finance vocabulary: **{finance_hits:,} "
          f"({100 * finance_hits / max(len(only_fm), 1):.0f}%)**", "",
          "| flow-accounting term | ungated-only records matching |", "|---|---|"]
    md += [f"| `{t}` | {n:,} |" for t, n in by_term.most_common()]
    md += ["", "## Dropping `intergenerational wealth` from the ungated channel", "",
           f"- reached by that term alone: **{n_iw:,}**",
           f"- of those, finance vocabulary: **{iw_fin:,}**",
           f"- demographic and not finance — the cost of the fix: **{iw_dem_only:,}**", ""]
    (LOGS / f"c3f-flowmeas-contamination-{DATE}.md").write_text("\n".join(md))
    print(f"\nwrote c3f-flowmeas-contamination-{DATE}.json and .md")


main()
