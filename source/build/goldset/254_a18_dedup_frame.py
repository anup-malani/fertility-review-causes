#!/usr/bin/env python3
"""254 — A.18 frame dedup, both kinds, before any count is reported. TICK-076.

Two distinct duplications were found in the 45,568-record pull, and they need
different treatment:

  1. 236 rows carry an openalex id that already appeared. Pure cursor-paging
     artefact; collapse silently.
  2. 2,996 normalised titles are shared by DISTINCT ids -- 3,800 extra records,
     8.3% of the frame. The largest cluster is one Figshare item deposited 159
     times.

Kind 2 is where the standing correction applies: same title + year + venue with
two DOIs is USUALLY two works, so a title match alone must not collapse records.
The gate requires **first-author agreement** as well, and a cluster that fails it
is kept intact and flagged rather than merged. Books and reports resolve to their
own reviews at Jaccard 1.00, which is what that rule exists to stop.

Order matters: dedup runs BEFORE any denominator is reported. The prescreen was
first reported against 45,568 and its survivors against 32,126 — both inflated by
duplicates, and one 159-copy cluster had already put two rows into the tail-audit
sample, contaminating a prevalence estimate.

Usage: python3 source/build/goldset/254_a18_dedup_frame.py
"""
import json
import re
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
LOGS = ROOT / "literature" / "search-logs"
TEMP = ROOT / "temp" / "a18"
IN = TEMP / "heritability-fertility-genetic-frame.json"
OUT = TEMP / "heritability-fertility-genetic-frame-deduped.json"
OUT_LOG = LOGS / "heritability-fertility-genetic-dedup-log.json"

TRANSLIT = {"ø": "o", "æ": "ae", "å": "a", "ß": "ss", "đ": "d", "ł": "l", "þ": "th"}


def fold(s):
    s = (s or "").lower()
    for k, v in TRANSLIT.items():
        s = s.replace(k, v)
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]+", " ", s).strip()


def first_author(rec):
    """Folded last name of the first author, or a UNIQUE sentinel when unreadable.

    A name can fold to nothing -- a fully non-Latin name loses every character to
    the ASCII strip. Returning "" for those would put every unreadable-author record
    in one bucket and MERGE them, which is the wrong direction: an author we cannot
    read must PREVENT a merge, not license one. So each unreadable record gets its
    own sentinel and stays apart.
    """
    a = (rec.get("authors") or "").split(";")
    if not a or not a[0].strip():
        return f"__noauthor__{rec['openalex']}"
    tok = fold(a[0]).split()
    return tok[-1] if tok else f"__unreadable__{rec['openalex']}"


def main():
    frame = json.loads(IN.read_text())
    records = frame["records"]
    n0 = len(records)

    # --- kind 1: repeated openalex id ---------------------------------------
    byid = {}
    for r in records:
        byid.setdefault(r["openalex"], r)
    n1 = len(byid)

    # --- kind 2: same folded title across distinct ids ----------------------
    groups = defaultdict(list)
    for r in byid.values():
        t = fold(r.get("title"))
        if t:
            groups[t].append(r)

    kept, merged, kept_apart = [], [], []
    for t, g in groups.items():
        if len(g) == 1:
            kept.append(g[0]); continue
        # cluster only records whose FIRST AUTHOR agrees; others stay separate
        by_auth = defaultdict(list)
        for r in g:
            by_auth[first_author(r)].append(r)
        for auth, sub in by_auth.items():
            if len(sub) == 1:
                kept.append(sub[0]); continue
            sub.sort(key=lambda r: (r.get("doi") is None,
                                    "preprint" in (r.get("type") or ""),
                                    -(r.get("cited_by") or 0)))
            kept.append(sub[0])
            merged.append({"kept": sub[0]["openalex"], "title": sub[0].get("title"),
                           "collapsed": len(sub) - 1, "first_author": auth})
        if len(by_auth) > 1:
            kept_apart.append({"title": g[0].get("title"), "distinct_first_authors": len(by_auth),
                               "records": len(g)})
    # records with no title survive untouched
    kept += [r for r in byid.values() if not fold(r.get("title"))]

    log = {
        "ticket": "TICK-076",
        "rows_in": n0,
        "duplicate_openalex_ids_collapsed": n0 - n1,
        "after_id_dedup": n1,
        "title_clusters_merged": len(merged),
        "records_collapsed_by_title": sum(m["collapsed"] for m in merged),
        "title_clusters_kept_apart_author_disagreement": len(kept_apart),
        "final": len(kept),
        "biggest_merges": sorted(merged, key=lambda m: -m["collapsed"])[:8],
        "kept_apart_examples": kept_apart[:8],
        "note": "First-author agreement is required to merge a title cluster; a shared "
                "title with different first authors is two works, not one.",
    }
    frame["records"] = kept
    frame["meta"]["deduped"] = log
    frame["meta"]["pulled"] = len(kept)
    OUT.write_text(json.dumps(frame, indent=1))
    OUT_LOG.write_text(json.dumps(log, indent=1))
    print(json.dumps({k: v for k, v in log.items()
                      if k not in ("biggest_merges", "kept_apart_examples")}, indent=1))
    print("\nbiggest merges:")
    for m in log["biggest_merges"]:
        print(f"   -{m['collapsed']:4d}  {(m['title'] or '')[:78]}")
    print("\nkept apart on author disagreement:")
    for k in log["kept_apart_examples"][:5]:
        print(f"   {k['records']} records / {k['distinct_first_authors']} first authors — "
              f"{(k['title'] or '')[:66]}")
    print(f"\nwrote {OUT} and {OUT_LOG.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
