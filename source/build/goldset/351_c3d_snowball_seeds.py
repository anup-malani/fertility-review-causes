#!/usr/bin/env python3
"""351 — turn the resolved C.3.d anchors into a snowball SEED SET, applying the version-pair rule.

Why this is a separate step rather than "seed on the anchors". Reading 350's output showed that for
two of the seventeen hand anchors the version of record is a near-dead seed:

    Galor & Moav 2002, "Natural Selection and the Origin of Economic Growth"
        QJE article  (10.1162/003355302320935007)      1 citation
        SSRN preprint                                 93 citations
    Doepke 2004, "Accounting for Fertility Decline during the Transition to Growth"
        Journal of Economic Growth article            11 citations
        SSRN preprint                                145 citations

Both are works with citation counts in the thousands elsewhere. This is NOT the QJE DOI-migration
split -- that shape is also present here, on Black-Devereux-Salvanes (10.1162 at 1,051 alongside
10.1093/qje at 446), and the twin gate catches it because both records exist and both carry
citations. The Galor-Moav shape is different: the OUP twin does not exist at all
(`filter=doi:10.1093/qje/117.4.1133` returns no record), so there is nothing to merge. OpenAlex's
citation graph simply never attached to the published version.

The practical consequence is the same either way and it is the point of this script: **a snowball
seeded on the version of record would harvest 1 citing work where the pair has 93.**
`citations-dont-follow-version-of-record` recorded the risk; these two are the case where the
version of record is not merely incomplete but is the WRONG seed.

So the seed set is the UNION of every member of each version pair, and the rule is stated rather
than left implicit: seed on all of them, deduplicate the citing sets afterwards. `version-pair-is-one-study`
says a preprint twin is one study for extraction; it is two seeds for retrieval, and those are
different questions.

Reads 350's JSON. No API calls.

Output: literature/search-logs/quantity-quality-tradeoff-snowball-seeds.{json,md}
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
LOGS = ROOT / "literature" / "search-logs"
ANCH = LOGS / "quantity-quality-tradeoff-cold-start-anchors.json"

MATCHED = {"MATCH", "MATCH_STEM", "MATCH_BY_ID", "MATCH_BY_DOI", "MATCH_VERSION_TWIN"}

# Below this share of the version pair's best citation count, the version of record is a dead seed
# and seeding on it alone would report an empty citing set as an absence.
DEAD_SEED_SHARE = 0.10


def main():
    anchors = json.loads(ANCH.read_text())
    seeds, rows, dead = [], [], []

    for a in anchors:
        if a["verdict"] not in MATCHED:
            continue
        tc = a.get("top_candidate") or {}
        pair = [{"oa_id": tc.get("oa_id"), "doi": tc.get("doi"), "year": tc.get("year"),
                 "cited_by": tc.get("cited_by") or 0, "role": "version_of_record",
                 "venue": tc.get("venue")}]
        for t in (a.get("twins") or []):
            pair.append({"oa_id": t.get("oa_id"), "doi": t.get("doi"), "year": t.get("year"),
                         "cited_by": t.get("cited_by") or 0, "role": "twin",
                         "venue": t.get("venue")})
        best = max(p["cited_by"] for p in pair)
        vor = pair[0]["cited_by"]
        row = {"title": a["title"], "source": a["source"], "direction": a.get("direction"),
               "arm": a["arm"], "n_versions": len(pair), "vor_cited_by": vor,
               "pair_best_cited_by": best, "pair_total_cited_by": sum(p["cited_by"] for p in pair),
               "vor_share": round(vor / best, 3) if best else None,
               "versions": pair}
        # A single-version anchor cannot have a dead-seed problem; only flag real pairs.
        row["dead_version_of_record"] = bool(len(pair) > 1 and best > 0
                                             and vor / best < DEAD_SEED_SHARE)
        if row["dead_version_of_record"]:
            dead.append(row)
        rows.append(row)
        for p in pair:
            if p["oa_id"]:
                seeds.append({"oa_id": p["oa_id"], "doi": p["doi"], "role": p["role"],
                              "cited_by": p["cited_by"], "anchor": a["title"],
                              "direction": a.get("direction"), "source": a["source"]})

    uniq = {s["oa_id"]: s for s in seeds}
    blob = {"n_anchors": len(rows), "n_seed_records": len(uniq),
            "n_multi_version": sum(1 for r in rows if r["n_versions"] > 1),
            "n_dead_version_of_record": len(dead),
            "citations_reachable_via_vor_only": sum(r["vor_cited_by"] for r in rows),
            "citations_reachable_via_full_pair": sum(r["pair_total_cited_by"] for r in rows),
            "anchors": rows, "seeds": sorted(uniq.values(), key=lambda s: -s["cited_by"])}
    (LOGS / "quantity-quality-tradeoff-snowball-seeds.json").write_text(
        json.dumps(blob, indent=2) + "\n")

    vor_only = blob["citations_reachable_via_vor_only"]
    full = blob["citations_reachable_via_full_pair"]
    L = ["# C.3.d snowball seed set", "",
         "Generated by `source/build/goldset/351_c3d_snowball_seeds.py`. Do not edit by hand.", "",
         f"**{len(uniq)} seed records from {len(rows)} resolved anchors.** "
         f"{blob['n_multi_version']} anchors have more than one version in the index.", "",
         "**The seed set is the union of every member of each version pair, not the version of "
         "record.** Seeding on versions of record alone would reach "
         f"**{vor_only:,}** citing works; seeding on the full pairs reaches **{full:,}** — "
         f"{full - vor_only:,} more, or {100 * (full - vor_only) / vor_only:.1f}%. "
         "`version-pair-is-one-study` makes a preprint twin ONE study at extraction; for retrieval "
         "it is TWO seeds, and those are different questions.", ""]
    if dead:
        L += [f"## {len(dead)} anchors whose version of record is a DEAD SEED", "",
              f"The published version carries under {int(DEAD_SEED_SHARE * 100)}% of the pair's "
              "citations. For these, seeding on the version of record would return a near-empty "
              "citing set, and an empty citing set reads as an absence "
              "(`refusals-read-as-zeros` in its retrieval form).", "",
              "| anchor | version of record | preprint / twin | VOR share |",
              "|---|---|---|---|"]
        for r in dead:
            vor, best = r["versions"][0], max(r["versions"][1:], key=lambda p: p["cited_by"])
            L.append(f"| {r['title'][:52]} | {vor['cited_by']:,} ({vor['year']}, "
                     f"{(vor['venue'] or '')[:24]}) | {best['cited_by']:,} ({best['year']}, "
                     f"{(best['venue'] or '')[:24]}) | {100 * r['vor_share']:.0f}% |")
        L.append("")
    L += ["## Seeds by direction (scope §2)", "",
          "| direction | anchors | seed records | citations reachable |", "|---|---|---|---|"]
    for d in ("THEORY", "BACKWARD", "FORWARD", "UNKNOWN"):
        rs = [r for r in rows if r["direction"] == d]
        if not rs:
            continue
        ss = [s for s in uniq.values() if s["direction"] == d]
        L.append(f"| `{d}` | {len(rs)} | {len(ss)} | {sum(r['pair_total_cited_by'] for r in rs):,} |")
    L += ["", "## Multi-version anchors", "",
          "| anchor | versions | VOR cites | pair total |", "|---|---|---|---|"]
    for r in sorted((r for r in rows if r["n_versions"] > 1),
                    key=lambda r: -r["pair_total_cited_by"]):
        L.append(f"| {r['title'][:56]} | {r['n_versions']} | {r['vor_cited_by']:,} | "
                 f"{r['pair_total_cited_by']:,} |")
    L.append("")
    (LOGS / "quantity-quality-tradeoff-snowball-seeds.md").write_text("\n".join(L))

    print(f"{len(rows)} resolved anchors -> {len(uniq)} seed records "
          f"({blob['n_multi_version']} multi-version)")
    print(f"citations reachable: version-of-record only {vor_only:,}  |  full pairs {full:,}  "
          f"(+{100 * (full - vor_only) / vor_only:.1f}%)")
    if dead:
        print(f"\n{len(dead)} anchors have a DEAD version of record "
              f"(<{int(DEAD_SEED_SHARE * 100)}% of the pair's citations):")
        for r in dead:
            print(f"  {r['vor_cited_by']:>5,} vs {r['pair_best_cited_by']:>5,}  {r['title'][:58]}")


main()
