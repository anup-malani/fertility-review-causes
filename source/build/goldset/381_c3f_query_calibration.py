#!/usr/bin/env python3
"""
381 — C.3.f (TICK-086) stage 3: build the production query and calibrate it PER AXIS.

The scope says the evidence sits in three near-disjoint places, so the query is three axes and not
one block:

  THEORY       Caldwell's vocabulary. Retrieves the theory and the measurement tradition, and
               (376) almost none of the identification -- 18 identified designs in 1,099 records.
  MEASUREMENT  the flow-accounting tradition: National Transfer Accounts, the lifecycle deficit,
               the village flow studies. This is link-1 evidence and it is most of the canon.
  SHOCK        the policy and labour-demand literatures that move the flow, each named as its own
               field names it. Crossovers with THEORY measured at 6, 2, 19 and 0 (376), so a query
               built from Caldwell's words alone would find almost none of it.

Why recall is measured per axis and not once at the end. `reachability-ceiling-before-recall`: an
axis that reaches nothing is invisible inside a union, because the union's recall is carried by
whichever axis works. C.3.d checked recall per axis for the same reason and found its theory axis
reached 3 of 8.

How recall is measured, cheaply. One request per arm: `title_and_abstract.search:<axis>` AND
`ids.openalex:<the anchors>` returns exactly the anchors that arm retrieves. Thirty anchors, one
request -- not thirty. Commas separate filters here and no comma appears inside a value
(`openalex-comma-breaks-filters`).

**Row 5's axis is on trial, not in production.** The scope flagged that its shock vocabulary said
`mining boom` where the seed it must reach is child labour in mines. Both spellings are measured
here against that seed by id, because an axis that cannot retrieve its own known positive is not a
measurement of a literature (`validate-a-null-detector-on-positives`).

Decoys are scored separately and never averaged with anchors. A decoy the query retrieves is a
boundary case to route, not a failure (`decoy-clouds-are-boundary-cases`).

Outputs literature/search-logs/c3f-query-calibration-<date>.{json,md}.
"""
import json, sys, datetime, pathlib

sys.path.insert(0, str(pathlib.Path("source/lib").resolve()))
from openalex import OpenAlex, POOL                                # noqa: E402

LOGS = pathlib.Path("literature/search-logs")
DATE = datetime.date.today().isoformat()

OUTCOME = ('("fertility" OR "childbearing" OR "birth rate" OR "total fertility rate" '
           'OR "family size" OR "number of children")')

# --- THEORY. The 12-term probe axis minus the four dead terms (376: 1, 0, 1, 3 records), plus the
# one candidate that cleared the price ceiling. `intergenerational support` is carried in its own
# sub-arm so its elder-care contamination is visible rather than folded into the block.
THEORY = ('("wealth flows" OR "intergenerational transfer" OR "intergenerational wealth" '
          'OR "value of children" OR "old age support" OR "old-age support" OR "filial support" '
          'OR "net transfers" OR "children as investment")')
THEORY_PLUS = THEORY[:-1] + ' OR "intergenerational support")'

# --- MEASUREMENT. The flow-accounting tradition, which the theory axis reaches only partly.
MEASUREMENT = ('("National Transfer Accounts" OR "lifecycle deficit" OR "life cycle deficit" '
               'OR "economic life cycle" OR "intergenerational resource flows" '
               'OR "flow of wealth" OR "direction of transfers" OR "economic value of children")')

# --- SHOCK, one arm per §7 row, each in its own field's vocabulary.
SHOCK_INHERITANCE = ('("inheritance law" OR "inheritance reform" OR "land titling" '
                     'OR "land reform" OR "bequest motive" OR "inheritance rights")')
SHOCK_SCHOOLING = ('("child labour ban" OR "child labor ban" OR "child labour law" '
                   'OR "child labor law" OR "school construction" OR "schooling supply" '
                   'OR "compulsory schooling" OR "compulsory education")')
SHOCK_FILIAL = ('("filial responsibility law" OR "filial piety law" OR "family support obligation" '
                'OR "parental maintenance" OR "maintenance of parents" OR "elderly rights law" '
                'OR "old age maintenance")')
SHOCK_REMITTANCE = ('("remittances to parents" OR "support to parents" OR "transfers to parents" '
                    'OR "remittances and fertility")')

# --- Row 5, the arm on trial. Two spellings of one axis.
CHILD_WORK = ('("child labour" OR "child labor" OR "child work" OR "child employment" '
              'OR "working children")')
NARROW_DEMAND = ('("commodity price" OR "mining boom" OR "cash crop" OR "export crop" '
                 'OR "trade shock" OR "labour demand" OR "labor demand" OR "mechanization" '
                 'OR "mechanisation" OR "agricultural productivity shock")')
WIDE_DEMAND = ('("commodity price" OR "mining" OR "mines" OR "cash crop" OR "export crop" '
               'OR "trade shock" OR "labour demand" OR "labor demand" OR "mechanization" '
               'OR "mechanisation" OR "plantation" OR "agricultural productivity")')
ROW5_NARROW = f"{CHILD_WORK} AND {NARROW_DEMAND}"
ROW5_WIDE = f"{CHILD_WORK} AND {WIDE_DEMAND}"

ARMS = [
    ("THEORY", THEORY),
    ("THEORY + intergenerational support", THEORY_PLUS),
    ("MEASUREMENT", MEASUREMENT),
    ("SHOCK inheritance and land", SHOCK_INHERITANCE),
    ("SHOCK schooling and child-labour law", SHOCK_SCHOOLING),
    ("SHOCK filial-responsibility law", SHOCK_FILIAL),
    ("SHOCK remittances to parents", SHOCK_REMITTANCE),
    ("ROW5 labour demand x child work (narrow — the scope's)", ROW5_NARROW),
    ("ROW5 labour demand x child work (wide — 'mining' not 'mining boom')", ROW5_WIDE),
]

# The union that would go to production. Row 5 enters at whichever spelling passes its own test.
def union_of(names, arms):
    return " OR ".join(dict(arms)[n] for n in names)


def anchors_from_380():
    """(anchor ids, decoy ids, label map). Derived from 380's JSON — never hand-typed."""
    d = json.load(open(LOGS / "c3f-anchors-2026-09-10.json"))
    anchors, decoys, label = [], [], {}
    for c in d["inherited"]:
        if c["confirmed"]:
            anchors.append(c["id"])
            label[c["id"]] = f"inherited · {(c['title'] or '')[:58]}"
    recovered = {r["expect_title"]: r["best"] for r in d["retried"]
                 if r["verdict"] == "RECOVERED" and r["best"]}
    for r in d["resolved"]:
        best = r.get("best")
        if r["verdict"] in ("OK", "VERSION_DIFFERS") and best:
            pid = best["id"]
        elif r["expect_title"] in recovered:
            pid = recovered[r["expect_title"]]["id"]
        else:
            continue                      # unreachable: the index holds only a review, or nothing
        (decoys if r["kind"] == "DECOY" else anchors).append(pid)
        label[pid] = f"{r['kind'].lower()} · {r['expect_author']} {r['expect_year']} · {r['arm']}"
    return anchors, decoys, label


def retrieved(oa, axis, ids, errors, tag):
    """Which of `ids` this axis retrieves. One request, not len(ids)."""
    params = {"filter": f"title_and_abstract.search:{axis},ids.openalex:{'|'.join(ids)}",
              "per-page": "200", "select": "id"}
    key = json.dumps(["hits", axis, sorted(ids)])
    if key in oa.cache:
        oa.stats["hit"] += 1
        return set(oa.cache[key]), None
    oa.stats["miss"] += 1
    d, err = oa.get(params)
    if err:
        errors.append((tag, err))
        return None, err
    hits = [r["id"].rsplit("/", 1)[-1] for r in d.get("results", [])]
    oa._remember(key, hits)
    return set(hits), None


def main():
    key = ""
    try:
        for line in open(".env"):
            if line.startswith("OPENALEX_API_KEY="):
                key = line.split("=", 1)[1].strip().strip('"')
    except FileNotFoundError:
        pass
    oa = OpenAlex(key=key, mailto="shravanh@uchicago.edu",
                  cache_path="temp/c3f-anchor-cache.json")
    errors, rows = [], []

    anchors, decoys, label = anchors_from_380()
    print(f"anchors {len(anchors)} · decoys {len(decoys)} (derived from 380, none hand-typed)")

    print("\n== per-arm volume, anchor recall and decoy leakage ==")
    per_arm = {}
    for name, axis in ARMS:
        q = f"{axis} AND {OUTCOME}"
        n, err = oa.count(q)
        if err:
            errors.append((name, err))
            print(f"  REFUSED  {name}: {err}", file=sys.stderr)
            continue
        hits, e1 = retrieved(oa, q, anchors, errors, f"{name}/anchors")
        leak, e2 = retrieved(oa, q, decoys, errors, f"{name}/decoys")
        per_arm[name] = {"axis": axis, "n": n, "hits": sorted(hits or []),
                         "leak": sorted(leak or [])}
        rows.append((name, n, len(hits or []), len(leak or [])))
        print(f"  {n:>7,}  recall {len(hits or []):>2}/{len(anchors)}  "
              f"decoys {len(leak or [])}/{len(decoys)}   {name}")

    print("\n== ROW 5 on trial: does either spelling retrieve the seed it must reach? ==")
    LITHIUM = "W4392107509"       # 'Lithium-ion batteries and fertility in Africa', from 377
    for name in [n for n, _ in ARMS if n.startswith("ROW5")]:
        got = LITHIUM in per_arm.get(name, {}).get("hits", [])
        print(f"  {'REACHES' if got else 'MISSES '} the mining seed — {name}")

    print("\n== the union, and each arm's marginal contribution to it ==")
    keep = [n for n, _ in ARMS if n != "ROW5 labour demand x child work (narrow — the scope's)"
            and n != "THEORY"]
    union_axis = f"({union_of(keep, ARMS)}) AND {OUTCOME}"
    un, err = oa.count(union_axis)
    uh, _ = retrieved(oa, union_axis, anchors, errors, "union/anchors")
    ul, _ = retrieved(oa, union_axis, decoys, errors, "union/decoys")
    print(f"  union {un:,}  recall {len(uh or [])}/{len(anchors)}  decoys {len(ul or [])}/{len(decoys)}")
    marginal = {}
    for name in keep:
        rest = [k for k in keep if k != name]
        q = f"({union_of(rest, ARMS)}) AND {OUTCOME}"
        n2, e = oa.count(q)
        h2, _ = retrieved(oa, q, anchors, errors, f"union-minus/{name}")
        if e:
            continue
        marginal[name] = {"union_without": n2, "records_added": (un or 0) - n2,
                          "anchors_added": len(uh or []) - len(h2 or [])}
        print(f"  dropping {name:56} -{(un or 0)-n2:>6,} records, "
              f"-{len(uh or [])-len(h2 or []):>2} anchors")

    unreached = [a for a in anchors if a not in (uh or set())]
    print(f"\n== {len(unreached)} anchors the union does not reach ==")
    for a in unreached:
        print(f"  {a}  {label.get(a, '')}")

    blob = {"date": DATE, "outcome_axis": OUTCOME, "arms": {n: a for n, a in ARMS},
            "union_arms": keep, "union_axis": union_axis,
            "anchors": anchors, "decoys": decoys, "labels": label,
            "per_arm": per_arm, "union": {"n": un, "recall": sorted(uh or []),
                                          "leak": sorted(ul or [])},
            "marginal": marginal, "unreached": unreached,
            "errors": [{"label": l, "error": e} for l, e in errors]}
    (LOGS / f"c3f-query-calibration-{DATE}.json").write_text(json.dumps(blob, indent=2) + "\n")

    md = [f"# C.3.f production query — calibration {DATE}", "",
          "Generated by `source/build/goldset/381_c3f_query_calibration.py`. Do not edit by hand.",
          "", f"Anchors **{len(anchors)}** · decoys **{len(decoys)}**, both derived from `380`.",
          "Recall and leakage are never averaged: a decoy the query retrieves is a boundary case to",
          "route, not a failure.", "",
          "| arm | records | anchor recall | decoy leakage |", "|---|---|---|---|"]
    md += [f"| {n} | {v:,} | {h}/{len(anchors)} | {l}/{len(decoys)} |" for n, v, h, l in rows]
    md += ["", f"**Union of the production arms: {un:,} records, recall "
               f"{len(uh or [])}/{len(anchors)}, decoy leakage {len(ul or [])}/{len(decoys)}.**", "",
           "| dropping this arm | records lost | anchors lost |", "|---|---|---|"]
    md += [f"| {k} | {v['records_added']:,} | {v['anchors_added']} |"
           for k, v in sorted(marginal.items(), key=lambda kv: -kv[1]["anchors_added"])]
    md += ["", f"## The {len(unreached)} anchors the union does not reach", ""]
    md += [f"- `{a}` — {label.get(a, '')}" for a in unreached] or ["None."]
    md.append("")
    (LOGS / f"c3f-query-calibration-{DATE}.md").write_text("\n".join(md))
    print(f"\ncache hit/miss {oa.stats['hit']}/{oa.stats['miss']}  pool {POOL}")
    print(f"wrote c3f-query-calibration-{DATE}.json and .md")


main()
