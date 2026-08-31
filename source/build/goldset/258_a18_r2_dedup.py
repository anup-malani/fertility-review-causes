#!/usr/bin/env python3
"""258 — A.18 round-2 dedup: title clusters and version pairs. TICK-076.

256 deduped only on openalex id, so it reported a NEW count inflated two ways,
both visible on the first screening batch:

  1. **Title clusters.** Williams 1957 (*Pleiotropy, natural selection, and the
     evolution of senescence*) appeared twice, as did Charlesworth's *Evolution in
     Age-Structured Populations*. 254 already built exactly this fix for the frame
     and 256 did not reuse it — a defect fixed once and then not carried forward.
  2. **Version pairs.** A preprint carries a different openalex id from its
     published version, so the bioRxiv twins of Beauchamp 2016 and of the
     schizophrenia MR were counted as new material when they are the SAME STUDY
     already screened. A version pair is one study.

Both merges require **first-author agreement**, and an unreadable author gets a
unique sentinel so it prevents a merge rather than licensing one.

Usage: python3 source/build/goldset/258_a18_r2_dedup.py
"""
import json
import re
import unicodedata
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
LOGS = ROOT / "literature" / "search-logs"
TEMP = ROOT / "temp" / "a18"
IN = TEMP / "heritability-fertility-genetic-snowball-pool-r2.json"
OUT = TEMP / "heritability-fertility-genetic-snowball-pool-r2-deduped.json"
OUT_LOG = LOGS / "heritability-fertility-genetic-r2-dedup-log.json"

TRANSLIT = {"ø": "o", "æ": "ae", "å": "a", "ß": "ss", "đ": "d", "ł": "l", "ð": "d", "þ": "th"}


def fold(s):
    s = (s or "").lower()
    for k, v in TRANSLIT.items():
        s = s.replace(k, v)
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]+", " ", s).strip()


def first_author(r):
    a = (r.get("authors") or "").split(";")
    if not a or not a[0].strip():
        return f"__noauthor__{r['openalex']}"
    t = fold(a[0]).split()
    return t[-1] if t else f"__unreadable__{r['openalex']}"


def main():
    new = json.loads(IN.read_text())
    n0 = len(new)

    # --- known titles, for the version-pair check --------------------------
    known_titles = {}
    for src in (LOGS / "heritability-fertility-genetic-snowball-pool.json",):
        for r in json.loads(src.read_text()):
            known_titles.setdefault(fold(r.get("title")), first_author(r))
    for r in json.loads((TEMP / "heritability-fertility-genetic-frame-deduped.json").read_text())["records"]:
        known_titles.setdefault(fold(r.get("title")), first_author(r))

    version_pairs = []
    remaining = []
    for r in new:
        t = fold(r.get("title"))
        if t and t in known_titles and known_titles[t] == first_author(r):
            version_pairs.append({"openalex": r["openalex"], "title": r.get("title"),
                                  "type": r.get("type"), "year": r.get("year")})
        else:
            remaining.append(r)

    # --- title clusters within what is left --------------------------------
    groups = defaultdict(list)
    for r in remaining:
        t = fold(r.get("title"))
        (groups[t] if t else groups[f"__untitled__{r['openalex']}"]).append(r)
    kept, merged, apart = [], [], 0
    for t, g in groups.items():
        if len(g) == 1:
            kept.append(g[0]); continue
        by_auth = defaultdict(list)
        for r in g:
            by_auth[first_author(r)].append(r)
        if len(by_auth) > 1:
            apart += 1
        for auth, sub in by_auth.items():
            if len(sub) == 1:
                kept.append(sub[0]); continue
            sub.sort(key=lambda r: (r.get("doi") is None,
                                    "preprint" in (r.get("type") or ""),
                                    -(r.get("cited_by") or 0)))
            keeper = sub[0]
            for loser in sub[1:]:
                keeper["seeds_backward"] = sorted(set(keeper["seeds_backward"]) | set(loser["seeds_backward"]))
                keeper["seeds_forward"] = sorted(set(keeper["seeds_forward"]) | set(loser["seeds_forward"]))
            keeper["n_seeds"] = len(keeper["seeds_backward"]) + len(keeper["seeds_forward"])
            merged.append({"kept": keeper["openalex"], "title": keeper.get("title"),
                           "collapsed": len(sub) - 1})
            kept.append(keeper)

    kept.sort(key=lambda r: (-r.get("n_seeds", 0), -(r.get("cited_by") or 0)))
    log = {"ticket": "TICK-076", "round": 2,
           "in": n0,
           "version_pairs_of_already_known_studies": len(version_pairs),
           "title_clusters_merged": len(merged),
           "records_collapsed_by_title": sum(m["collapsed"] for m in merged),
           "clusters_kept_apart_author_disagreement": apart,
           "final": len(kept),
           "inflation_of_the_reported_NEW": n0 - len(kept),
           "examples_version_pairs": version_pairs[:10],
           "biggest_title_merges": sorted(merged, key=lambda m: -m["collapsed"])[:8],
           "note": "A version pair is one study. Both merges require first-author agreement."}
    OUT.write_text(json.dumps(kept, indent=1))
    OUT_LOG.write_text(json.dumps(log, indent=1))
    print(json.dumps({k: v for k, v in log.items()
                      if not k.startswith(("examples", "biggest"))}, indent=1))
    print("\nversion pairs of already-screened studies (examples):")
    for v in version_pairs[:8]:
        print(f"   {(v['title'] or '')[:74]}  [{v['type']}, {v['year']}]")
    print("\nbiggest title merges:")
    for m in log["biggest_title_merges"][:5]:
        print(f"   -{m['collapsed']}  {(m['title'] or '')[:74]}")


if __name__ == "__main__":
    main()
