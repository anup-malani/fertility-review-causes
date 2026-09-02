#!/usr/bin/env python3
"""309 — C.6.a screen universe: pull the five arms, fold in the other channels, dedup. TICK-078.

Three discovery channels, kept distinguishable in `provenance` so yield can be measured per channel
rather than assumed equal across them:

  `arm:<name>`  the calibrated production queries (308), cursor-paged in full
  `free_seed`   the 143 records script 305 harvested from other chapters' pools -- a genuinely
                different channel, since those records were retrieved by other hypotheses' queries
  `anchor`      the 31 resolved cold-start anchors (307), injected unconditionally

Anchors are injected whether or not the queries return them. A pool that omits its own anchors
cannot measure its own recall, and two of these anchors are known unreachable by any arm
(`snowball-pools-omit-their-own-seeds`). They are NOT flagged in the emitted screen sheets -- the
screen has to meet them blind, or its sensitivity is measured on records it knows the answer to
(`blinded-screens-audit-the-anchors`, `a-positives-only-screen-cannot-measure-sensitivity`).

Abstracts are reconstructed from OpenAlex's inverted index; a record with no abstract is kept and
marked, because absence of an abstract is a retrieval fact, not a relevance judgement.

Usage: python3 source/build/goldset/309_c6a_build_screen_universe.py
"""
import json
import subprocess
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
LOGS = ROOT / "literature" / "search-logs"
KEY = next((l.split("=", 1)[1].strip() for l in (ROOT / ".env").read_text().splitlines()
            if l.startswith("OPENALEX_API_KEY=")), "")
MAILTO = "shravanh@uchicago.edu"
OUT = LOGS / "easterlin-relative-income-screen-universe.json"

SELECT = ("id,doi,display_name,publication_year,type,authorships,primary_location,"
          "cited_by_count,abstract_inverted_index,referenced_works_count")


def call(params):
    args = ["curl", "-sS", "--max-time", "180", "-G", "https://api.openalex.org/works"]
    for k, v in params.items():
        args += ["--data-urlencode", f"{k}={v}"]
    args += ["--data-urlencode", f"api_key={KEY}", "--data-urlencode", f"mailto={MAILTO}"]
    r = subprocess.run(args, capture_output=True, text=True)
    try:
        d = json.loads(r.stdout)
    except json.JSONDecodeError:
        return None, f"non-JSON: {r.stdout[:200]}"
    if "meta" not in d or d["meta"].get("count") is None:
        return None, f"query refused (NOT an empty literature): {json.dumps(d)[:200]}"
    return d, None


def abstract(inv):
    if not inv:
        return ""
    pos = {}
    for word, idxs in inv.items():
        for i in idxs:
            pos[i] = word
    return " ".join(pos[i] for i in sorted(pos))


def flatten(w):
    auths = [a.get("author", {}).get("display_name", "") for a in w.get("authorships", [])]
    return {"openalex": w["id"].rsplit("/", 1)[-1],
            "doi": w.get("doi"), "title": w.get("display_name") or "",
            "year": w.get("publication_year"), "type": w.get("type"),
            "venue": ((w.get("primary_location") or {}).get("source") or {}).get("display_name"),
            "authors": auths[:6], "cited_by": w.get("cited_by_count"),
            "abstract": abstract(w.get("abstract_inverted_index")),
            "n_refs": w.get("referenced_works_count")}


def page_all(query, label):
    """Cursor-page a query to exhaustion. A cursor that stops early is a defect, not a small
    literature -- the reported count is checked against what was actually collected."""
    out, cursor, expected = [], "*", None
    while cursor:
        d, err = call({"filter": f"title_and_abstract.search:{query}", "per-page": "200",
                       "cursor": cursor, "select": SELECT})
        if err:
            print(f"  {label}: ERROR {err}")
            return out, expected
        if expected is None:
            expected = d["meta"]["count"]
        out += [flatten(w) for w in d.get("results", [])]
        cursor = d["meta"].get("next_cursor")
        if not d.get("results"):
            break
        time.sleep(0.2)
    status = "ok" if expected is not None and len(out) >= expected else "SHORT"
    print(f"  {label}: collected {len(out)} of {expected} reported  [{status}]")
    return out, expected


def main():
    arms = json.loads((LOGS / "easterlin-relative-income-production-query.json").read_text())
    universe, provenance = {}, {}

    print("ARMS")
    for a in arms["arms"]:
        rows, expected = page_all(a["query"], a["name"])
        for r in rows:
            universe.setdefault(r["openalex"], r)
            provenance.setdefault(r["openalex"], set()).add(f"arm:{a['name']}")

    print("\nFREE SEEDS (script 305)")
    seeds = json.loads((LOGS / "easterlin-relative-income-free-seeds.json").read_text())["records"]
    seed_ids = [s["id"].rsplit("/", 1)[-1] for s in seeds
                if s["id"].startswith("W") or "openalex" in s["id"]]
    seed_dois = [s["id"] for s in seeds if s["id"].startswith("10.")]
    fetched = 0
    for i in range(0, len(seed_ids), 50):
        chunk = seed_ids[i:i + 50]
        d, err = call({"filter": f"ids.openalex:{'|'.join(chunk)}", "per-page": "200",
                       "select": SELECT})
        if err:
            continue
        for w in d.get("results", []):
            r = flatten(w)
            universe.setdefault(r["openalex"], r)
            provenance.setdefault(r["openalex"], set()).add("free_seed")
            fetched += 1
    for i in range(0, len(seed_dois), 40):
        chunk = seed_dois[i:i + 40]
        d, err = call({"filter": f"doi:{'|'.join(chunk)}", "per-page": "200", "select": SELECT})
        if err:
            continue
        for w in d.get("results", []):
            r = flatten(w)
            universe.setdefault(r["openalex"], r)
            provenance.setdefault(r["openalex"], set()).add("free_seed")
            fetched += 1
    print(f"  resolved {fetched} of {len(seeds)} seed records "
          f"({len(seed_ids)} by id, {len(seed_dois)} by doi)")

    print("\nANCHORS (injected unconditionally)")
    anchors = json.loads((LOGS / "easterlin-relative-income-cold-start-anchors.json").read_text())
    aids = [a["top_candidate"]["oa_id"].rsplit("/", 1)[-1] for a in anchors
            if (a.get("top_candidate") or {}).get("oa_id")]
    already = sum(1 for i in aids if i in universe)
    for i in range(0, len(aids), 50):
        d, err = call({"filter": f"ids.openalex:{'|'.join(aids[i:i+50])}", "per-page": "200",
                       "select": SELECT})
        if err:
            continue
        for w in d.get("results", []):
            r = flatten(w)
            universe.setdefault(r["openalex"], r)
            provenance.setdefault(r["openalex"], set()).add("anchor")
    print(f"  {len(aids)} anchors; {already} were already in the pool, "
          f"{len(aids) - already} injected")

    for k, v in universe.items():
        v["provenance"] = sorted(provenance[k])
    rows = sorted(universe.values(), key=lambda r: -(r["cited_by"] or 0))
    no_abs = sum(1 for r in rows if not r["abstract"])
    OUT.write_text(json.dumps({"n": len(rows), "no_abstract": no_abs, "records": rows},
                              indent=1) + "\n")

    from collections import Counter
    c = Counter(p for r in rows for p in r["provenance"])
    print(f"\nUNIVERSE {len(rows)} records, {no_abs} without an abstract "
          f"({100*no_abs/len(rows):.0f}%)")
    for k, v in c.most_common():
        print(f"  {k:24} {v}")
    print(f"written: {OUT.name}")


main()
