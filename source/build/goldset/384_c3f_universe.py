#!/usr/bin/env python3
"""
384 — C.3.f (TICK-086) stage 3: build the screening universe from two channels.

Scope §15 ruled this chapter citation-channel-first: the term arms reach 11 of 24 anchors and cannot
reach Caldwell 1976, so a vocabulary pool alone would miss the literature it is meant to find. The
universe is therefore the union of

  TERM      each calibrated arm, pulled SEPARATELY and deduplicated by id. Never OR'd into one
            query string: 381 did that and OpenAlex collapsed the union to a single arm, returning
            46 records against a THEORY arm of 1,097, with negative marginals as the only tell
            (`and-arm-collapses-an-or-union`).
  CITATION  forward and backward from the 30 resolved anchors. Forward = works citing an anchor;
            backward = works an anchor cites.

Two decisions that are recorded here rather than made silently:

**The citation channel is gated on the OUTCOME axis, not the exposure axis.** Gating it on exposure
vocabulary would re-impose the very filter §15 found broken. The outcome axis was calibrated
separately (§3B) and `fertility` alone carries 840 of 1,099, so it is a far safer gate — but it is
still a gate, so the cost is measured: both the unrestricted and the restricted counts are reported,
and the ratio is on the page (`abstract-cap-hides-the-outcome` — a short abstract can hide the
dependent variable).

**Nothing is pulled before it is counted.** A forward-citation pull over a canon can be enormous, and
at ~100 requests a day an unbounded pull spends the allowance mid-way. The script counts every
channel first, prints the plan with its request cost, and pulls only what fits under CAP. Whatever it
declines to pull is reported as a bound, not dropped silently (`bound-what-you-did-not-screen`).

Outputs output/wealth-flows-reversal-universe.json (the screening set) and
literature/search-logs/c3f-universe-<date>.{json,md} (how it was built).
"""
import json, sys, datetime, pathlib

sys.path.insert(0, str(pathlib.Path("source/lib").resolve()))
from openalex import OpenAlex, POOL                                # noqa: E402

LOGS = pathlib.Path("literature/search-logs")
OUT = pathlib.Path("output")
DATE = datetime.date.today().isoformat()
SELECT = "id,doi,display_name,publication_year,type,cited_by_count"
CAP_PAGES = 40                      # ~8,000 records; the day's allowance is ~100 requests

OUTCOME = ('("fertility" OR "childbearing" OR "birth rate" OR "total fertility rate" '
           'OR "family size" OR "number of children")')


def main():
    cal = json.load(open(LOGS / "c3f-query-calibration-2026-09-10.json"))
    axis = json.load(open(LOGS / "c3f-theory-axis-2026-09-10.json"))
    anchors = cal["anchors"]

    # The production arms: the REBUILT theory axis (383) replaces the probe vocabulary, and row 5
    # enters at the wide spelling. The two arms 381 measured but did not adopt are excluded.
    arms = {
        "THEORY (rebuilt, 383)": axis["final_axis"],
        "MEASUREMENT": cal["arms"]["MEASUREMENT"],
        "SHOCK inheritance and land": cal["arms"]["SHOCK inheritance and land"],
        "SHOCK schooling and child-labour law": cal["arms"]["SHOCK schooling and child-labour law"],
        "SHOCK filial-responsibility law": cal["arms"]["SHOCK filial-responsibility law"],
        "SHOCK remittances to parents": cal["arms"]["SHOCK remittances to parents"],
        "ROW5 labour demand x child work":
            cal["arms"]["ROW5 labour demand x child work (wide — 'mining' not 'mining boom')"],
    }

    key = ""
    try:
        for line in open(".env"):
            if line.startswith("OPENALEX_API_KEY="):
                key = line.split("=", 1)[1].strip().strip('"')
    except FileNotFoundError:
        pass
    oa = OpenAlex(key=key, mailto="shravanh@uchicago.edu",
                  cache_path="temp/c3f-universe-cache.json")
    errors, plan = [], []

    print("== counting every channel before pulling anything ==")
    for name, ax in arms.items():
        n, err = oa.count(f"{ax} AND {OUTCOME}")
        if err:
            errors.append((name, err))
            print(f"  REFUSED  {name}: {err}", file=sys.stderr)
            continue
        plan.append({"channel": "TERM", "name": name, "query": f"{ax} AND {OUTCOME}", "n": n,
                     "pages": -(-n // 200)})
        print(f"  {n:>7,}  {-(-n // 200):>3} pages   TERM  {name}")

    # ---------------------------------------------------------------- the FLOW_MEASUREMENT channel
    # Reading the outcome gate's excluded sample exposed a contradiction in the scope's own design.
    # §9 defines a `FLOW_MEASUREMENT` cell -- "measures the flow, no fertility outcome" -- and §5
    # needs exactly that literature, because the demsig route wants a net-flow series. But every
    # channel above is gated on the outcome axis, so a record with no fertility vocabulary can
    # never enter the universe. The cell was unreachable by construction.
    #
    # Caught on a real record: "Ageing and inter-generational wealth flows in two Indonesian
    # communities" (2008) carries the chapter's central phrase and was excluded by both channels.
    #
    # So one channel runs UNGATED, on a deliberately tight axis: the flow-accounting vocabulary
    # only, never the general terms. `value of children` alone is 7,083 records unrestricted and is
    # not in here for that reason.
    FLOWMEAS = ('("wealth flows" OR "intergenerational wealth" OR "National Transfer Accounts" '
                'OR "lifecycle deficit" OR "life cycle deficit" OR "intergenerational resource flows" '
                'OR "flow of wealth" OR "net intergenerational transfer")')
    fm_n, fm_err = oa.count(FLOWMEAS)
    if fm_err:
        errors.append(("FLOW_MEASUREMENT count", fm_err))
    else:
        plan.append({"channel": "FLOWMEAS", "name": "flow accounting, UNGATED by outcome",
                     "query": FLOWMEAS, "n": fm_n, "pages": -(-fm_n // 200)})
        print(f"  {fm_n:>7,}  {-(-fm_n // 200):>3} pages   FLOWMEAS flow accounting, ungated "
              f"(the §9 cell that no gated channel could reach)")

    cites = "|".join(anchors)
    d, e1 = oa.get({"filter": f"cites:{cites}", "per-page": "1"})
    fwd_all = None if e1 else d["meta"]["count"]
    d2, e2 = oa.get({"filter": f"cites:{cites},title_and_abstract.search:{OUTCOME}",
                     "per-page": "1"})
    fwd_out = None if e2 else d2["meta"]["count"]
    if e1 or e2:
        errors.append(("forward citation counts", e1 or e2))
    else:
        plan.append({"channel": "CITATION", "name": "forward (cited-by, outcome-gated)",
                     "filter": f"cites:{cites},title_and_abstract.search:{OUTCOME}",
                     "n": fwd_out, "pages": -(-fwd_out // 200), "unrestricted": fwd_all})
        print(f"  {fwd_out:>7,}  {-(-fwd_out // 200):>3} pages   CITATION forward "
              f"(of {fwd_all:,} unrestricted — the outcome gate costs "
              f"{100 * (1 - fwd_out / fwd_all):.0f}%)")

    d3, e3 = oa.get({"filter": f"ids.openalex:{cites}", "per-page": "200",
                     "select": "id,referenced_works"})
    backward = set()
    if e3:
        errors.append(("anchor references", e3))
    else:
        for r in d3.get("results", []):
            backward |= {w.rsplit("/", 1)[-1] for w in (r.get("referenced_works") or [])}
        print(f"  {len(backward):>7,}      —   CITATION backward (references of the 30 anchors)")

    total_pages = sum(p["pages"] for p in plan)
    print(f"\nplan: {total_pages} pages ≈ {total_pages} requests, plus "
          f"{-(-len(backward) // 100)} to outcome-gate the backward set. CAP is {CAP_PAGES}.")

    # ---------------------------------------------------------------- pull
    universe, provenance = {}, {}

    def absorb(records, channel, name):
        added = 0
        for r in records:
            pid = r["id"].rsplit("/", 1)[-1]
            if pid not in universe:
                universe[pid] = {"id": pid, "doi": r.get("doi"),
                                 "title": r.get("display_name"),
                                 "year": r.get("publication_year"), "type": r.get("type"),
                                 "cited_by": r.get("cited_by_count")}
                added += 1
            provenance.setdefault(pid, []).append(f"{channel}:{name}")
        return added

    print("\n== pulling ==")
    pulled_pages, declined = 0, []
    for p in plan:
        if pulled_pages + p["pages"] > CAP_PAGES:
            declined.append(p)
            print(f"  DECLINED (would exceed cap)  {p['name']}  {p['n']:,} records")
            continue
        if p["channel"] in ("TERM", "FLOWMEAS"):
            recs, err = oa.page_all(p["query"], SELECT)
        else:
            recs, err = [], None
            cursor, got = "*", []
            while cursor:
                dd, err = oa.get({"filter": p["filter"], "per-page": "200", "cursor": cursor,
                                  "select": SELECT})
                if err:
                    break
                got += dd.get("results", [])
                cursor = (dd.get("meta") or {}).get("next_cursor")
                if not dd.get("results"):
                    break
            recs = got
        if err:
            errors.append((p["name"], err))
            print(f"  REFUSED  {p['name']}: {err}", file=sys.stderr)
            continue
        pulled_pages += p["pages"]
        n_new = absorb(recs, p["channel"], p["name"])
        print(f"  {len(recs):>7,} records, {n_new:>7,} new   {p['name']}")

    # backward set: gate on the outcome axis in chunks
    bwd_kept = 0
    if backward:
        ids = sorted(backward)
        for i in range(0, len(ids), 100):
            chunk = ids[i:i + 100]
            dd, err = oa.get({"filter": f"ids.openalex:{'|'.join(chunk)},"
                                        f"title_and_abstract.search:{OUTCOME}",
                              "per-page": "200", "select": SELECT})
            if err:
                errors.append((f"backward chunk {i}", err))
                break
            bwd_kept += absorb(dd.get("results", []), "CITATION", "backward (references)")
        print(f"  {bwd_kept:>7,} new from the backward set "
              f"({len(backward):,} references gated on the outcome axis)")

    # ---------------------------------------------------------------- seeds go IN the universe
    # `snowball-pools-omit-their-own-seeds`: a pool built FROM the anchors does not contain them.
    # A screening set that omits its own known positives cannot reach 100% recall by construction,
    # and every recall figure computed over it is wrong by the number of missing seeds.
    missing = [a for a in anchors + cal["decoys"] if a not in universe]
    if missing:
        dd, err = oa.get({"filter": "ids.openalex:" + "|".join(missing), "per-page": "200",
                          "select": SELECT})
        if err:
            errors.append(("seed backfill", err))
            print(f"  REFUSED seed backfill: {err}", file=sys.stderr)
        else:
            n_new = absorb(dd.get("results", []), "SEED", "anchor or decoy not otherwise retrieved")
            print(f"\n  {n_new} seeds added that neither channel retrieved "
                  f"({len(missing)} were missing)")

    # ------------------------------------------------- bound the cost of the outcome gate
    # The gate removed 66% of the forward-citation set. `bound-what-you-did-not-screen`: sample the
    # excluded tail rather than assuming a filter that large only removed irrelevant records.
    gate_sample = {"n": 0, "in_pool": 0, "excluded": []}
    ds, errs = oa.get({"filter": f"cites:{cites}", "sample": "100", "seed": "86",
                       "per-page": "100", "select": SELECT})
    if errs:
        errors.append(("outcome-gate sample", errs))
    else:
        for r in ds.get("results", []):
            pid = r["id"].rsplit("/", 1)[-1]
            gate_sample["n"] += 1
            if pid in universe:
                gate_sample["in_pool"] += 1
            else:
                gate_sample["excluded"].append({"id": pid, "title": r.get("display_name"),
                                                "year": r.get("publication_year")})
        print(f"\n== outcome gate, bounded on a random sample of {gate_sample['n']} "
              f"forward citations ==")
        print(f"  in the pool: {gate_sample['in_pool']}   excluded: "
              f"{len(gate_sample['excluded'])}")
        print("  a reader decides whether the excluded are fertility studies; first 15 titles:")
        for e in gate_sample["excluded"][:15]:
            print(f"    {e['year']}  {(e['title'] or '')[:90]}")

    n_anchor_in = sum(1 for a in anchors if a in universe)
    print(f"\n== universe {len(universe):,} records ==")
    print(f"  anchors present: {n_anchor_in}/{len(anchors)}")
    by_channel = {}
    for pid, srcs in provenance.items():
        for s in {x.split(":")[0] for x in srcs}:
            by_channel[s] = by_channel.get(s, 0) + 1
    print(f"  by channel: {by_channel}")
    only_cit = sum(1 for p, s in provenance.items()
                   if all(x.startswith("CITATION") for x in s))
    only_term = sum(1 for p, s in provenance.items() if all(x.startswith("TERM") for x in s))
    print(f"  reachable ONLY by the citation channel: {only_cit:,}")
    print(f"  reachable ONLY by the term channel:     {only_term:,}")

    OUT.mkdir(exist_ok=True)
    (OUT / "wealth-flows-reversal-universe.json").write_text(json.dumps(
        {"date": DATE, "n": len(universe),
         "records": [dict(v, provenance=sorted(set(provenance[k])))
                     for k, v in universe.items()]}, indent=1) + "\n")

    log = {"date": DATE, "arms": arms, "outcome_axis": OUTCOME,
           "flow_measurement_axis": FLOWMEAS, "plan": plan,
           "declined": declined, "cap_pages": CAP_PAGES,
           "forward_unrestricted": fwd_all, "forward_outcome_gated": fwd_out,
           "backward_references": len(backward), "backward_kept": bwd_kept,
           "universe_n": len(universe), "anchors_present": n_anchor_in,
           "seeds_backfilled": len(missing), "outcome_gate_sample": gate_sample,
           "anchors_total": len(anchors), "only_citation": only_cit, "only_term": only_term,
           "errors": [{"label": l, "error": e} for l, e in errors]}
    (LOGS / f"c3f-universe-{DATE}.json").write_text(json.dumps(log, indent=2) + "\n")

    md = [f"# C.3.f screening universe — {DATE}", "",
          "Built by `source/build/goldset/384_c3f_universe.py`. Arms are pulled separately and",
          "deduplicated by id; they are never OR'd into one query string.", "",
          f"**Universe: {len(universe):,} records.** Anchors present {n_anchor_in}/{len(anchors)}.",
          f"Reachable only by the citation channel: **{only_cit:,}**. Only by the term channel: "
          f"{only_term:,}.", "",
          f"Forward citations of the 30 anchors: {fwd_all:,} unrestricted, {fwd_out:,} after the",
          f"outcome gate — the gate costs {100 * (1 - fwd_out / fwd_all):.0f}%. On a random",
          f"sample of {gate_sample['n']} forward citations, {gate_sample['in_pool']} are in the",
          f"pool and {len(gate_sample['excluded'])} are not; the excluded titles are listed in the",
          "JSON for a reader to judge. The gate's cost is measured, not assumed.", "",
          "| channel | arm | records | pages |", "|---|---|---|---|"]
    md += [f"| {p['channel']} | {p['name']} | {p['n']:,} | {p['pages']} |" for p in plan]
    if declined:
        md += ["", "**Declined under the page cap, and therefore a bound on this universe rather "
                   "than an absence:**", ""]
        md += [f"- {p['name']} — {p['n']:,} records" for p in declined]
    md.append("")
    (LOGS / f"c3f-universe-{DATE}.md").write_text("\n".join(md))
    print(f"\ncache hit/miss {oa.stats['hit']}/{oa.stats['miss']}  pool {POOL}")
    print("wrote output/wealth-flows-reversal-universe.json and "
          f"literature/search-logs/c3f-universe-{DATE}.*")


main()
