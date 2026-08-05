#!/usr/bin/env python3
"""
97_d1a_rescore_pools.py — re-score BOTH snowball pools under the current relevance filter. No network.

Generalises `94_`, which could only re-score round 1. Once there are two rounds, scoring them under
different filter versions makes the yields incomparable and the stop rule meaningless -- round 1 at
v2 and round 2 at v3 would produce a change in yield that is partly a change in the literature and
partly a change in the ruler, with no way to tell which. Every reported number comes from one filter
version, and the version is stamped into the output.

Also writes the audit sample the standing requirement calls for. That requirement has now paid for
itself three times on this chapter: the v1 read found two bugs, the v2 read found bug C, and the v3
read found v2's own over-correction. The sample is drawn from ADMITTED and REJECTED records both,
because v1's false negatives were invisible in the admitted set by construction.

Output: temp/d1a/snowball-r{1,2}-pool-scored.json
        temp/d1a/rescore-audit.md
"""
import json, os, random, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from d1a_relevance import VERSION, relevant  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
TMP = os.path.join(ROOT, "temp", "d1a")
POOLS = [("round 1", os.path.join(TMP, "snowball-r1-pool-relabelled.json"),
          os.path.join(TMP, "snowball-r1-pool-scored.json")),
         ("round 2", os.path.join(TMP, "snowball-r2-pool.json"),
          os.path.join(TMP, "snowball-r2-pool-scored.json"))]
AUDIT = os.path.join(TMP, "rescore-audit.md")
SAMPLE_N = 30


def main():
    random.seed(97)
    L = [f"# D.1.a — snowball pools re-scored under relevance filter **v{VERSION}**", "",
         "*Both rounds scored by one filter version. A yield computed under a different ruler than "
         "the round it is compared to is not a saturation statistic.*", ""]
    summary = {}

    for name, src, dst in POOLS:
        d = json.load(open(src))
        pool = d["pool"]
        before = sum(1 for r in pool if r.get("relevant"))
        gained, lost = [], []
        for r in pool:
            was = r.get("relevant")
            ok, why = relevant(r)
            if ok and not was:
                gained.append(r)
            elif was and not ok:
                lost.append(r)
            r["relevant"], r["relevance_reason"] = ok, why

        rel = [r for r in pool if r["relevant"]]
        # Round 2's denominator is NEW relevant records only; round 1's is all of them.
        scope = [r for r in rel if r.get("new_in_r2", True)]
        pulled = (d["counts"]["records_pulled"] if name == "round 1"
                  else d["counts"]["round2_total"]["records_pulled"])
        y = len(scope) / pulled * 50 if pulled else 0
        d["relevance_filter_version"] = VERSION
        d["rescored"] = {"before": before, "after": len(rel), "gained": len(gained),
                         "lost": len(lost), "counted_for_yield": len(scope),
                         "records_pulled": pulled, "yield_per_50": round(y, 2)}
        json.dump(d, open(dst, "w"), indent=1)
        summary[name] = d["rescored"]

        L += [f"## {name}", "",
              f"- relevant before re-score: **{before}** → after: **{len(rel)}** "
              f"(gained {len(gained)}, lost {len(lost)})",
              f"- counted toward yield: **{len(scope)}** of **{pulled}** pulled → "
              f"**{y:.2f}** per 50 (floor 1.0)", ""]
        for tag, recs in (("newly admitted by this version", gained),
                          ("newly rejected by this version", lost)):
            if not recs:
                continue
            shown = recs if len(recs) <= 20 else random.sample(recs, 20)
            L += [f"### {name}: {tag} ({len(recs)}"
                  f"{', sample of 20' if len(recs) > 20 else ''})", ""]
            L += [f"- [{r.get('year')}] {(r.get('title') or '')[:96]}  — `{r['relevance_reason']}`"
                  for r in shown] + [""]

        rej = [r for r in pool if not r["relevant"] and r.get("new_in_r2", True)]
        L += [f"### {name}: audit sample — ADMITTED ({min(SAMPLE_N, len(scope))})", ""]
        L += [f"- [{r.get('year')}] {(r.get('title') or '')[:96]}  — `{r['relevance_reason']}`"
              for r in random.sample(scope, min(SAMPLE_N, len(scope)))] + [""]
        L += [f"### {name}: audit sample — REJECTED ({min(SAMPLE_N, len(rej))})", ""]
        L += [f"- [{r.get('year')}] {(r.get('title') or '')[:96]}  — `{r['relevance_reason'][:60]}`"
              for r in random.sample(rej, min(SAMPLE_N, len(rej)))] + [""]

    open(AUDIT, "w").write("\n".join(L))
    print(json.dumps(summary, indent=1), file=sys.stderr)
    print(f"wrote {AUDIT}", file=sys.stderr)


if __name__ == "__main__":
    main()
