#!/usr/bin/env python3
"""
383 — C.3.f (TICK-086): rebuild the THEORY axis from the anchors' own language, and test it.

382 found that 13 of 24 anchors contain not one term of any calibrated arm, and the misses cluster:
they are the THEORY and measurement anchors, not the shock ones. That distinction decides the fix.

  THEORY is defective. `wealth flows` reaches 4 of 24 and does not reach Caldwell 1976, the paper
  that founded the theory. `old age support` reaches 0 — Bau 2021 says "supports parents in their
  old age". `wealth-flow theory` in the Iowa study is singular and hyphenated, and the plural term
  does not match it.

  The SHOCK arms are UNTESTABLE for recall, not broken. They score 0/24 because no anchor lives in
  their cells — §7 rows 2, 3 and 4 have no canonical work, which is the finding those rows already
  recorded. Adding terms until their recall rises would be fitting the query to the absence of
  anchors (`misses-that-cluster-mean-wrong-shape`). They are left alone.

Candidate terms are mined from the unreached anchors' own titles and abstracts, locally and free,
then priced the way every other term in this chapter has been: by MARGINAL anchor recall over the
current axis, not by their own size, and against a frame cost so a term that doubles the frame for
one anchor is visible (`term-acceptance-needs-a-price-ceiling`, `frame-growth-is-not-frame-gain`).

Mining vocabulary is not retrieval vocabulary (`mining-vocabulary-is-not-retrieval-vocabulary`): a
phrase lifted from an anchor may be common English. Every accepted term is therefore reported with
BOTH what it adds in anchors and what it adds in records.

Output literature/search-logs/c3f-theory-axis-<date>.{json,md}.
"""
import json, sys, datetime, pathlib, re, collections

sys.path.insert(0, str(pathlib.Path("source/lib").resolve()))
import textnorm                                                    # noqa: E402
from openalex import OpenAlex                                      # noqa: E402

LOGS = pathlib.Path("literature/search-logs")
DATE = datetime.date.today().isoformat()
OUTCOME = ('("fertility" OR "childbearing" OR "birth rate" OR "total fertility rate" '
           'OR "family size" OR "number of children")')

STOP = set("the a an of in on and or to for with by from as at is are was were be been this that "
           "these those it its their his her our we i they them he she which who whom whose what "
           "when where how why not no nor but if then than so such can could may might will would "
           "shall should must have has had do does did done being more most less least much many "
           "some any all both each few other another same own very s t".split())

# Hand-chosen from the mined list below. Mining proposes; a person disposes
# (`dont-automate-a-hand-read-seed-choice`). Each is a phrase an anchor actually uses.
CANDIDATES = [
    "wealth flow",                     # singular; the Iowa study says "wealth-flow theory"
    "economic value of children",
    "economic contribution of children",
    "productive contribution",
    "children's usefulness",
    "usefulness of children",
    "support in old age",              # the form Bau 2021 uses; "old age support" reaches 0
    "supporting parents",
    "support of parents",
    "economic rationality of high fertility",
    "wealth inheritance",
    "parental investment",
    "net cost of children",
    "children as economic assets",
    "economic benefits of children",
    "intergenerational flows of wealth",
]

BASE = ('("wealth flows" OR "intergenerational transfer" OR "intergenerational wealth" '
        'OR "value of children" OR "National Transfer Accounts" OR "flow of wealth")')


def main():
    cal = json.load(open(LOGS / "c3f-query-calibration-2026-09-10.json"))
    voc = json.load(open(LOGS / "c3f-anchor-vocabulary-2026-09-10.json"))
    anchors, labels = cal["anchors"], cal["labels"]

    key = ""
    try:
        for line in open(".env"):
            if line.startswith("OPENALEX_API_KEY="):
                key = line.split("=", 1)[1].strip().strip('"')
    except FileNotFoundError:
        pass
    oa = OpenAlex(key=key, mailto="shravanh@uchicago.edu",
                  cache_path="temp/c3f-anchor-cache.json")
    texts = oa.cache[json.dumps(["texts", sorted(cal["anchors"] + cal["decoys"])])]

    # ---------------------------------------------------------------- local mining, no requests
    print("== phrases the unreached anchors actually use (mined locally) ==")
    grams = collections.Counter()
    for pid in voc["unreached"]:
        blob = textnorm.norm(f"{texts[pid]['title']} {texts[pid]['abstract']}")
        w = [x for x in blob.split() if x not in STOP]
        for n in (2, 3):
            for i in range(len(w) - n + 1):
                grams[" ".join(w[i:i + n])] += 1
    mined = [(g, c) for g, c in grams.most_common(40) if c > 1]
    for g, c in mined[:24]:
        print(f"  {c:>2}  {g}")

    # ---------------------------------------------------------------- price each candidate
    def recall(axis, tag):
        q = f"{axis} AND {OUTCOME}"
        n, e1 = oa.count(q)
        k = json.dumps(["hits", q, sorted(anchors)])
        if k in oa.cache:
            oa.stats["hit"] += 1
            hits = set(oa.cache[k])
        else:
            oa.stats["miss"] += 1
            d, e2 = oa.get({"filter": f"title_and_abstract.search:{q},"
                                      f"ids.openalex:{'|'.join(anchors)}",
                            "per-page": "200", "select": "id"})
            if e2:
                print(f"  REFUSED {tag}: {e2}", file=sys.stderr)
                return None, None
            hits = {r["id"].rsplit("/", 1)[-1] for r in d.get("results", [])}
            oa._remember(k, sorted(hits))
        return n, hits

    print("\n== baseline: the surviving THEORY + MEASUREMENT terms ==")
    base_n, base_hits = recall(BASE, "base")
    print(f"  {base_n:,} records · recall {len(base_hits)}/{len(anchors)}")

    print("\n== each candidate, priced against a baseline that ADVANCES as terms are accepted ==")
    # `advance-the-baseline-when-accepting-terms`. Priced against a frozen baseline, `wealth
    # inheritance` (+5 records) and `parental investment` (+367) each claimed the SAME anchor, and
    # accepting both would have bought nothing for 367 records. The baseline advances, so a term is
    # priced against what the axis already has.
    priced, accepted = [], []
    cur_axis, cur_n, cur_hits = BASE, base_n, base_hits
    order = sorted(CANDIDATES)          # a stable order, so the run is reproducible
    remaining = list(order)
    while remaining:
        best = None
        for t in remaining:
            axis = cur_axis[:-1] + f' OR "{t}")'
            n, hits = recall(axis, t)
            if n is None:
                continue
            gained = sorted(hits - cur_hits)
            row = {"term": t, "records_added": n - cur_n, "anchors_added": len(gained),
                   "anchors": [labels.get(g, g)[:56] for g in gained],
                   "priced_against": cur_n}
            if gained and (best is None or
                           (len(gained), -(n - cur_n)) > (best["anchors_added"],
                                                          -best["records_added"])):
                best = dict(row, axis=axis, n=n, hits=hits)
            if not any(p["term"] == t for p in priced):
                priced.append(row)
        if best is None:
            break
        accepted.append(best["term"])
        remaining.remove(best["term"])
        print(f"  ACCEPT  +{best['records_added']:>5,} records  +{best['anchors_added']} anchors  "
              f"{best['term']}")
        for a in best["anchors"]:
            print(f"            {a}")
        cur_axis, cur_n, cur_hits = best["axis"], best["n"], best["hits"]
    print("\n  rejected (buy no anchor the axis does not already have):")
    for t in remaining:
        row = next((r for r in priced if r["term"] == t), None)
        print(f"    {t:42} would have cost +{(row or {}).get('records_added', 0):,} records")

    final = cur_axis
    print("\n== the rebuilt THEORY axis ==")
    fn, fh = recall(final, "final")
    print(f"  {fn:,} records · recall {len(fh)}/{len(anchors)}  "
          f"(was {len(base_hits)}/{len(anchors)} at {base_n:,})")
    still = [a for a in anchors if a not in fh]
    print(f"\n== {len(still)} anchors the rebuilt axis still does not reach ==")
    for a in still:
        print(f"  {labels.get(a, a)[:78]}")

    blob = {"date": DATE, "base_axis": BASE, "base_records": base_n,
            "base_recall": sorted(base_hits), "mined": mined, "priced": priced,
            "accepted": accepted, "final_axis": final, "final_records": fn,
            "final_recall": sorted(fh), "still_unreached": still,
            "n_anchors": len(anchors)}
    (LOGS / f"c3f-theory-axis-{DATE}.json").write_text(json.dumps(blob, indent=2) + "\n")

    md = [f"# C.3.f — rebuilding the THEORY axis from the anchors' own language — {DATE}", "",
          "Generated by `source/build/goldset/383_c3f_theory_axis_rebuild.py`.", "",
          f"Baseline (surviving probe terms): **{base_n:,} records, recall "
          f"{len(base_hits)}/{len(anchors)}**.", "",
          "| candidate term | + records | + anchors | which anchors |", "|---|---|---|---|"]
    md += [f"| `{p['term']}` | {p['records_added']:+,} | {p['anchors_added']} | "
           f"{'; '.join(p['anchors']) or '—'} |"
           for p in sorted(priced, key=lambda p: (-p["anchors_added"], p["records_added"]))]
    md += ["", f"**Rebuilt axis: {fn:,} records, recall {len(fh)}/{len(anchors)}.**", "",
           f"## The {len(still)} anchors it still does not reach", ""]
    md += [f"- {labels.get(a, a)}" for a in still]
    md.append("")
    (LOGS / f"c3f-theory-axis-{DATE}.md").write_text("\n".join(md))
    print(f"\ncache hit/miss {oa.stats['hit']}/{oa.stats['miss']}")
    print(f"wrote c3f-theory-axis-{DATE}.json and .md")


main()
