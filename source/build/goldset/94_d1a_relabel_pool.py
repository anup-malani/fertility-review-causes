#!/usr/bin/env python3
"""
94_d1a_relabel_pool.py — recompute relevance on a stored snowball pool. No network.

Direct analogue of the C.2.c `relabel_pool.py`, and written for the same reason: the relevance filter
that feeds the saturation statistic was found to be wrong, and the pool has to be re-scored without
re-pulling. Keeping this as a separate step means the yield number can be corrected and DIFFED against
the number that was wrong, rather than quietly replaced.

Imports the corrected TREATMENT / OUTCOME patterns from 93 so there is exactly one definition of
relevance in the tree. Two definitions is how they drift.

Output: temp/d1a/snowball-r1-pool-relabelled.json
        temp/d1a/relabel-diff.md   (what changed, and a fresh audit sample to hand-read)
"""
import importlib.util, json, os, random, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
TMP = os.path.join(ROOT, "temp", "d1a")
POOL = os.path.join(TMP, "snowball-r1-pool.json")
OUT = os.path.join(TMP, "snowball-r1-pool-relabelled.json")
DIFF = os.path.join(TMP, "relabel-diff.md")

spec = importlib.util.spec_from_file_location("sb", os.path.join(HERE, "93_d1a_snowball_r1.py"))
sb = importlib.util.module_from_spec(spec)
sys.modules["sb"] = sb
spec.loader.exec_module(sb)


def main():
    d = json.load(open(POOL))
    pool = d["pool"]
    was_rel = {i: r["relevant"] for i, r in enumerate(pool)}
    gained, lost = [], []
    for i, r in enumerate(pool):
        ok, why = sb.relevant(r)
        if ok and not was_rel[i]:
            gained.append(r)
        if was_rel[i] and not ok:
            lost.append(r)
        r["relevant"], r["relevance_reason"] = ok, why

    rel = [r for r in pool if r["relevant"]]
    pulled = d["counts"]["records_pulled"]
    y_new = len(rel) / pulled * 50 if pulled else 0
    y_old = d["counts"]["yield_per_50_pulled"]
    d["counts"].update({"relevant": len(rel), "yield_per_50_pulled": round(y_new, 2),
                        "relabel": {"previous_relevant": len(was_rel) and sum(was_rel.values()),
                                    "previous_yield_per_50": y_old,
                                    "gained_by_fix": len(gained), "lost_by_fix": len(lost)}})
    json.dump(d, open(OUT, "w"), indent=1)

    random.seed(23)
    L = ["# D.1.a snowball round 1 — relevance relabel diff", "",
         f"- previous relevant: **{sum(was_rel.values())}**, yield **{y_old}** per 50",
         f"- corrected relevant: **{len(rel)}**, yield **{y_new:.2f}** per 50",
         f"- newly admitted by the quoted-phrase fix (bug B): **{len(gained)}**",
         f"- removed by the `reproduc\\w+` narrowing (bug A): **{len(lost)}**",
         f"- stop floor is 1.0 per 50 — round 2 "
         f"{'IS REQUIRED' if y_new >= 1.0 else 'is not required on this statistic alone'}", "",
         "## Newly admitted (all)" if len(gained) <= 40 else "## Newly admitted (sample of 40)", ""]
    for r in (gained if len(gained) <= 40 else random.sample(gained, 40)):
        L.append(f"- [{r.get('year')}] {(r.get('title') or '')[:100]}  — `{r['relevance_reason']}`")
    L += ["", "## Removed (all)" if len(lost) <= 40 else "## Removed (sample of 40)", ""]
    for r in (lost if len(lost) <= 40 else random.sample(lost, 40)):
        L.append(f"- [{r.get('year')}] {(r.get('title') or '')[:100]}  — `{r['relevance_reason']}`")
    L += ["", "## Fresh audit sample of the corrected ADMITTED set (25)",
          "", "*Hand-read this before quoting the yield. A filter that has been wrong once gets read "
          "again, not trusted.*", ""]
    for r in random.sample(rel, min(25, len(rel))):
        L.append(f"- [{r.get('year')}] {(r.get('title') or '')[:100]}  — `{r['relevance_reason']}`")
    open(DIFF, "w").write("\n".join(L))
    print(f"previous {sum(was_rel.values())} rel (yield {y_old}) -> corrected {len(rel)} rel "
          f"(yield {y_new:.2f})", file=sys.stderr)
    print(f"gained {len(gained)}, lost {len(lost)}", file=sys.stderr)
    print(f"wrote {OUT}\nwrote {DIFF}", file=sys.stderr)


if __name__ == "__main__":
    main()
