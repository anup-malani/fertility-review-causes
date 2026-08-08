#!/usr/bin/env python3
"""
108_d2d_assemble_screen.py — D.2.d, stage A5 output.

Assemble the completed screen batches into a corpus with cells, re-attaching the metadata that was
blinded at step 105, and write a screen report whose FIRST claim is what was not screened.

THIS IS A PARTIAL SCREEN AND THE REPORT SAYS SO IN ITS HEADLINE. The run was stopped deliberately
(Shravan, 2026-08-08) after the per-batch runtime degraded by an order of magnitude; the remaining
batches are outstanding, not absent. Three numbers must travel together everywhere this screen is
quoted, and the report is built so they cannot be separated:

    frame                 2,677
    model-screened          n_screened   (batches completed)
    title-only, unscreened    796        (rubric policy, no model call)
    abstract-bearing, NOT YET screened   (the gap this run left)

A reader given only the screened count would take it for the denominator. On a chapter whose central
finding so far is an ABSENCE — no primary-cell record in the first 75 verdicts — that confusion is not
cosmetic: an absence measured over 21% of a frame is a different claim from an absence measured over
all of it, and only one of them is currently supportable.

Outputs: output/{slug}-screen-tiers.json
         output/{slug}-screen-report.md
"""
import json, pathlib
from collections import Counter, defaultdict

SLUG = "child-centeredness-intensive-parenting"
HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[2]
LOGS = REPO / "literature" / "search-logs"
OUT = REPO / "output"
SCREEN = REPO / "temp" / "screen" / SLUG

PRIMARY = {"PRIMARY_NORM_EXPOSURE", "PRIMARY_TIME_INTENSITY",
           "PRIMARY_PERCEIVED_STANDARD", "COST_INDEPENDENCE"}
THEORY = {"PARENTING_NORM_THEORY", "PARENTING_NORM_CONSTRUCT", "FDT_SENTIMENTALIZATION_CONTEXT"}
DEFERRED = {"ROUTING_DEFERRED_TO_FULLTEXT", "MIXED_NORM_UNRESOLVED", "INSUFFICIENT_INFO"}


def main():
    frame = {r["paperId"]: r for r in json.loads((LOGS / f"{SLUG}-tier-b-frame.json").read_text())}
    manifest = json.loads((LOGS / f"{SLUG}-screen-manifest.json").read_text())
    title_only = json.loads((LOGS / f"{SLUG}-title-only-stratum.json").read_text())
    res = json.loads((LOGS / f"{SLUG}-anchor-resolution.json").read_text())
    decoy_seeds = {it["openalex"]["paperId"] for it in res["resolved"] if it["is_decoy"]}

    done_batches, rows = [], []
    for entry in manifest["manifest"]:
        vp = REPO / entry["output"]
        if not vp.exists():
            continue
        done_batches.append(entry["batch"])
        for v in json.loads(vp.read_text()):
            rec = frame.get(v["paperId"], {})
            sids = set(rec.get("seed_ids") or [])
            rows.append({**v,
                         "title": rec.get("title"), "year": rec.get("year"),
                         "doi": rec.get("doi"), "venue": rec.get("venue"),
                         "cited_by_count": rec.get("cited_by_count"),
                         "discovery_channels": rec.get("discovery_channels"),
                         "seed_ids": sorted(sids),
                         "decoy_seeded": bool(sids) and sids <= decoy_seeds,
                         "screen_batch": entry["batch"]})

    n_frame = manifest["frame_records"]
    n_screenable = manifest["model_screened_records"]
    n_title_only = manifest["title_only_records_not_model_screened"]
    n_screened = len(rows)
    n_gap = n_screenable - n_screened
    outstanding = [e["batch"] for e in manifest["manifest"] if e["batch"] not in done_batches]

    cells = Counter(r["estimand_cell"] for r in rows)
    verdicts = Counter(r["verdict"] for r in rows)
    levels = Counter(r["outcome_level"] for r in rows)
    by_origin = defaultdict(Counter)
    for r in rows:
        by_origin["decoy-seeded" if r["decoy_seeded"] else "other"][r["estimand_cell"]] += 1

    primary_rows = [r for r in rows if r["estimand_cell"] in PRIMARY]
    theory_rows = [r for r in rows if r["estimand_cell"] in THEORY]
    deferred_rows = [r for r in rows if r["estimand_cell"] in DEFERRED]

    tiers = {"slug": SLUG, "stage": "partial_screen_not_frozen",
             "coverage": {"frame": n_frame, "abstract_bearing": n_screenable,
                          "model_screened": n_screened,
                          "abstract_bearing_not_screened": n_gap,
                          "title_only_unscreened": n_title_only,
                          "batches_done": sorted(done_batches),
                          "batches_outstanding": outstanding,
                          "share_of_frame_screened": round(n_screened / n_frame, 3)},
             "records": rows}
    OUT.mkdir(exist_ok=True)
    (OUT / f"{SLUG}-screen-tiers.json").write_text(json.dumps(tiers, indent=2, ensure_ascii=False))

    pct = 100 * n_screened / n_frame
    L = [f"# Screen report (PARTIAL) — {SLUG} (D.2.d)", "",
         "> **This screen is incomplete and every number below is conditional on that.**", "",
         f"> | | n | share of frame |",
         f"> |---|---|---|",
         f"> | Tier-B frame | {n_frame:,} | 100% |",
         f"> | **Model-screened (this report)** | **{n_screened:,}** | **{pct:.0f}%** |",
         f"> | Abstract-bearing, NOT yet screened | {n_gap:,} | {100*n_gap/n_frame:.0f}% |",
         f"> | Title-only, unscreened by rubric policy | {n_title_only:,} | {100*n_title_only/n_frame:.0f}% |",
         "",
         f"> {len(done_batches)} of {len(manifest['manifest'])} batches completed. Outstanding: "
         f"{outstanding if len(outstanding) <= 25 else str(outstanding[:25]) + ' …'}.",
         "> The run was stopped deliberately after per-batch runtime degraded roughly twelve-fold; "
         "these batches are **outstanding, not absent**, and the frame, batches and rubric are frozen "
         "so completing them changes nothing already screened.", "",
         "## Verdicts", "",
         "| verdict | n |", "|---|---|"]
    for v, n in verdicts.most_common():
        L.append(f"| {v} | {n} |")
    L += ["", "## Estimand cells", "", "| cell | n |", "|---|---|"]
    for c, n in cells.most_common():
        L.append(f"| `{c}` | {n} |")
    L += ["", "## The primary stratum", "",
          f"**Records in a primary empirical cell: {len(primary_rows)}.**"]
    if not primary_rows:
        L += ["", "Not one record in the screened set reached `PRIMARY_NORM_EXPOSURE`, "
              "`PRIMARY_TIME_INTENSITY`, `PRIMARY_PERCEIVED_STANDARD`, or `COST_INDEPENDENCE`.",
              "",
              "This is consistent with two earlier independent measurements, and it is the chapter's "
              "central finding so far — but it is measured over "
              f"{pct:.0f}% of the frame and cannot yet be stated as a property of the literature:", "",
              "1. `\"intensive parenting\" AND fertility` returns 17 records in all of OpenAlex (A3).",
              "2. The theory canon's forward-citation clouds are 1.1–13.9% on-topic (A4).",
              "3. No primary-cell record in this screen.", "",
              "The A3 anchors remain the empirical base: 7 Tier-A seeds, of which exactly one "
              "(`10.1016/j.worlddev.2025.107079`) is a `COST_INDEPENDENCE` candidate."]
    else:
        L += ["", "| cell | outcome level | year | title |", "|---|---|---|---|"]
        for r in primary_rows:
            L.append(f"| `{r['estimand_cell']}` | {r['outcome_level']} | {r.get('year')} | "
                     f"{(r.get('title') or '')[:70]} |")
    L += ["", "## Theory and context stream", "",
          f"{len(theory_rows)} records. These carry `RELEVANT` and are separated downstream; they do "
          "**not** count toward empirical recall.", "",
          "## Deferred routing", "",
          f"{len(deferred_rows)} records could not be routed from the abstract "
          f"({100*len(deferred_rows)/max(1,n_screened):.0f}% of screened). Four of the six boundary "
          "walls are not enforceable at title/abstract, so these are held for full text rather than "
          "assigned an `OFF_*` label the abstract could not support.", "",
          "## Decoy-seeding sensitivity", "",
          "41% of the frame was reachable only via a routing-decoy seed. Cell distribution by origin:",
          "", "| origin | n | top cells |", "|---|---|---|"]
    for origin in ("decoy-seeded", "other"):
        c = by_origin[origin]
        top = ", ".join(f"`{k}` {v}" for k, v in c.most_common(4))
        L.append(f"| {origin} | {sum(c.values())} | {top} |")
    L += ["", "Recall(B) must be computed both with and without the decoy-seeded stratum; `seed_ids` "
          "provenance is carried on every record so this is a filter, not a re-run.", "",
          "## Outcome levels", "", "| level | n |", "|---|---|"]
    for k, n in levels.most_common():
        L.append(f"| {k} | {n} |")
    (OUT / f"{SLUG}-screen-report.md").write_text("\n".join(L) + "\n")
    print(f"screened {n_screened} of {n_screenable} abstract-bearing ({pct:.0f}% of frame {n_frame})")
    print(f"primary-cell records: {len(primary_rows)} | theory: {len(theory_rows)} | "
          f"deferred: {len(deferred_rows)}")
    print("cells:", dict(cells.most_common()))


if __name__ == "__main__":
    main()
