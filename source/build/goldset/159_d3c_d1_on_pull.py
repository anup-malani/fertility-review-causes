#!/usr/bin/env python3
r"""
159_d3c_d1_on_pull.py — D.3.c. Re-run the D1 cutoff against the REAL pull.

`154_d3c_d1_rank.py` calibrated D1's threshold on the Tier B citation frame, because C1 had not run.
It said, in its own output, that the frame is an *enriched* neighbourhood and therefore an upper bound
on the pull's survivor share, and that the calibration had to be redone against real retrieval before
budget was committed. C1 has now run (partially), so this is that redo.

Two things change when the calibration moves from the frame to the pull, and both matter:

  * **The corpus is real.** The frame is one hop from a hand-built anchor set and is dense in
    mechanism and treatment vocabulary by construction. The pull is what an outcome-only query
    actually returns from the open index, which is mostly clinical, epidemiological and demographic
    work with no relation to this hypothesis. The survivor share should fall, and by how much is the
    number that sets the screening bill.

  * **The gold is the gold that survived retrieval.** 197 of the 204 filter-eligible gold records are
    present in the partial pull. Recall is measured against those 197 — the records the screen can
    actually reach — rather than against a denominator including records the query never returned.
    Conflating "D1 dropped it" with "C1 never fetched it" would credit D1 with losses it did not cause
    and hide the ones it did.

The calibration rule is unchanged and non-negotiable: **the largest threshold that loses ZERO gold.**
A D1 false negative is unrecoverable.

Output: literature/search-logs/{slug}-d1-on-pull.md
"""
import json, os, statistics, sys

SLUG = "despair-hopelessness-fertility"
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
LOGS = os.path.join(ROOT, "literature", "search-logs")
PULL = os.path.join(ROOT, "temp", "d3c-pull", "records.jsonl")

sys.path.insert(0, HERE)
import importlib.util


def load_mod(name, fn):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, fn))
    m = importlib.util.module_from_spec(spec)
    sys.modules[name] = m
    spec.loader.exec_module(m)
    return m


d1 = load_mod("d1", "154_d3c_d1_rank.py")     # reuse the scoring function verbatim — one definition
cvb = load_mod("cvb", "152_d3c_cv_breadth.py")

# Cost model constants, identical to 155_/157_ so the three agree by construction.
CPT, RPR, BATCH, CACHE = 4.0, 20, 0.50, 0.10
PH, PS = {"in": 1.00, "out": 5.00}, {"in": 2.00, "out": 10.00}
S1_OUT, S2_OUT, S1_PASS = 12, 100, 0.15       # compressed schema


def stage(n, chars, rubric, out_per, price):
    reqs = max(1, round(n / RPR))
    eff = n * chars / CPT + reqs * rubric * CACHE
    return ((eff / 1e6) * price["in"] + (n * out_per / 1e6) * price["out"]) * (1 - BATCH)


def main():
    if not os.path.exists(PULL):
        sys.exit(f"no pull at {PULL} — run 158_ first")
    rows = []
    for line in open(PULL):
        try:
            rows.append(json.loads(line))
        except Exception:
            pass
    chars = statistics.mean(len((r.get("title") or "") + " " + (r.get("abstract") or ""))
                            for r in rows)

    gold, _n, _nc, _nn, _a = cvb.load()
    goldkeys = {cvb.norm(g["title"])[:70] for g in gold}
    # COUNT DISTINCT GOLD WORKS, NOT MATCHING RECORDS. A first version counted pull records whose
    # title matched a gold key and reported 239 "gold in pull" against a gold set of 243 — which
    # looked like the retrieval filter had cost almost nothing. It had not: the index holds several
    # records per work (preprint and published version, editions, reissues), so one gold work can
    # match two or three pull records. The distinct count is 205. The inflated figure flattered the
    # filter by ~34 records and would have understated its cost by 14 percentage points.
    scored, seen_gold = [], set()
    for r in rows:
        k = cvb.norm(r.get("title") or "")[:70]
        is_gold = k in goldkeys
        first_hit = is_gold and k not in seen_gold
        if is_gold:
            seen_gold.add(k)
        s, why = d1.score(r)
        scored.append({"score": s, "is_gold": is_gold, "gold_first_hit": first_hit})
    n_gold = len(seen_gold)

    lo, hi = min(x["score"] for x in scored), max(x["score"] for x in scored)
    curve = []
    for thr in range(lo, hi + 1):
        keep = [x for x in scored if x["score"] >= thr]
        kg = sum(1 for x in keep if x["gold_first_hit"])
        curve.append({"threshold": thr, "kept": len(keep), "share": len(keep) / len(scored),
                      "gold_kept": kg, "recall": kg / max(n_gold, 1)})
    lossless = [c for c in curve if c["recall"] >= 1.0]
    chosen = max(lossless, key=lambda c: c["threshold"]) if lossless else curve[0]

    frame = json.load(open(os.path.join(LOGS, f"{SLUG}-d1-cutoff.json")))
    n1 = chosen["kept"]
    cost = stage(n1, chars, 1500, S1_OUT, PH) + stage(n1 * S1_PASS, chars, 3000, S2_OUT, PS)
    cost_nofilter = stage(len(scored), chars, 1500, S1_OUT, PH) + \
        stage(len(scored) * S1_PASS, chars, 3000, S2_OUT, PS)

    L = [f"# D.3.c — D1 re-calibrated on the real pull", "",
         f"`154_` calibrated D1 on the Tier B citation frame because C1 had not run, and said in its "
         f"own output that the frame is enriched, that its survivor share was therefore an upper "
         f"bound, and that the calibration had to be redone against real retrieval before budget was "
         f"committed. This is that redo, over the **{len(rows):,}** records C1 actually returned.", "",
         "**Recall is measured against the gold present in the pull**, not against the full gold set — "
         f"{n_gold} distinct gold works of 243 were retrieved. Charging D1 for records C1 never "
         "returned would credit it with losses it did not cause and hide the ones it did.", "",
         "**Distinct works, not matching records.** The index holds several records per work "
         "(preprint and published version, editions, reissues), so one gold work can match two or "
         "three pull records. A first version of this script counted records and reported 239 gold "
         "in the pull against a set of 243 — which made the retrieval filter look nearly free. It is "
         "not: the distinct count is 205, and the filter's cost stands at roughly the 16% reported "
         "when it was chosen.", "",
         "| | frame (154_) | **real pull (this run)** |", "|---|---|---|",
         f"| corpus | {frame['frame_total']:,} | **{len(scored):,}** |",
         f"| gold present | {frame['gold_total']} | **{n_gold}** |",
         f"| chosen threshold | {frame['threshold']} | **{chosen['threshold']}** |",
         f"| survivors | {frame['frame_kept']:,} ({frame['kept_share']:.1%}) | "
         f"**{chosen['kept']:,} ({chosen['share']:.1%})** |",
         f"| gold recall | {frame['gold_recall']:.0%} | **{chosen['recall']:.0%}** |", "",
         "## Recall versus budget, on real retrieval", "",
         "| threshold | kept | share | gold kept | recall |", "|---|---|---|---|---|"]
    for c in curve:
        mark = " **<- chosen**" if c["threshold"] == chosen["threshold"] else ""
        L.append(f"| {c['threshold']} | {c['kept']:,} | {c['share']:.1%} | "
                 f"{c['gold_kept']}/{n_gold} | {c['recall']:.1%}{mark} |")
    L += ["", "## What it costs", "",
          f"Mean title+abstract length on the real pull is **{chars:.0f} characters** "
          f"(the frame's was 724), so the per-record cost transfers with a small adjustment.", "",
          "| | records to D2a | screen cost |", "|---|---|---|",
          f"| no D1 filter | {len(scored):,} | ${cost_nofilter:.0f} |",
          f"| **D1 at threshold {chosen['threshold']}** | **{chosen['kept']:,}** | **${cost:.0f}** |",
          f"| D1 saves | {len(scored)-chosen['kept']:,} records | **${cost_nofilter-cost:.0f}** |", "",
          "Token counts remain **estimated from measured characters** — this environment still has no "
          "Anthropic credential, so `count_tokens()` has not been run. The character counts are now "
          "real retrieval rather than a citation-frame proxy, which removes one of the two "
          "approximations but not the other.", ""]
    # Write the survivors as the screen's concrete input, so D2a has a file to read rather than a
    # threshold to re-derive. Same JSONL shape as the pull; nothing is transformed.
    out_dir = os.path.join(ROOT, "temp", "d3c-screen")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "stage1-input.jsonl")
    n_written = 0
    with open(out_path, "w") as fh:
        for r in rows:
            sc, _ = d1.score(r)
            if sc >= chosen["threshold"]:
                fh.write(json.dumps(r, ensure_ascii=False) + "\n")
                n_written += 1
    L += [f"## Screen input written", "",
          f"`{os.path.relpath(out_path, ROOT)}` — **{n_written:,} records**, the D1 survivors at "
          f"threshold {chosen['threshold']}. This is what `156_d3c_screen.py stage1` consumes.", ""]
    open(os.path.join(LOGS, f"{SLUG}-d1-on-pull.md"), "w").write("\n".join(L) + "\n")
    print(f"screen input -> {os.path.relpath(out_path, ROOT)} ({n_written:,} records)")
    print(f"pull={len(scored):,} gold_in_pull={n_gold} threshold={chosen['threshold']} "
          f"survivors={chosen['kept']:,} ({chosen['share']:.1%}) recall={chosen['recall']:.0%} "
          f"cost=${cost:.0f} (vs ${cost_nofilter:.0f} unfiltered)")


if __name__ == "__main__":
    main()
