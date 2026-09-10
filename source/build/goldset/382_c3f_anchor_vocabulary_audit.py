#!/usr/bin/env python3
"""
382 — C.3.f (TICK-086): why the calibrated arms miss the anchors they miss.

381 measured recall per arm and found THEORY 7/24, MEASUREMENT 3/24 and every SHOCK arm 0/24. Two
explanations were available and they have opposite fixes: the anchors are unreachable (a ceiling, so
change the channel) or the vocabulary is wrong (a query defect, so change the terms).
`recall-miss-can-indict-the-anchors` says read the missed record before tightening the query, and
`misses-that-cluster-mean-wrong-shape` says cross-tab the misses before concluding anything.

So this fetches the anchors' own titles and abstracts ONCE — one batched request for all thirty
records — and then does the whole diagnosis locally. Every term of every arm is tested against every
anchor's real text in memory, at no further cost. That turns a question that would otherwise be
priced in API calls (one per term per anchor) into a text problem, which matters at ~100 requests a
day.

What it reports:
  - per anchor: which arm terms actually occur in its title or abstract
  - per term: how many anchors it reaches, so a term earning nothing is visible
  - the anchors NO term reaches, with their text, because those decide whether the query can work
    at all or whether this chapter is citation-channel-first

An abstract check ran first and ruled out the obvious story: 23 of 24 anchors have an abstract
indexed, so this is not the title-only stratum problem.

Output literature/search-logs/c3f-anchor-vocabulary-<date>.{json,md}.
"""
import json, sys, datetime, pathlib, re

sys.path.insert(0, str(pathlib.Path("source/lib").resolve()))
import textnorm                                                    # noqa: E402
from openalex import OpenAlex                                      # noqa: E402

LOGS = pathlib.Path("literature/search-logs")
DATE = datetime.date.today().isoformat()


def abstract_of(rec):
    """OpenAlex stores abstracts as an inverted index. Rebuild the text."""
    inv = rec.get("abstract_inverted_index")
    if not inv:
        return ""
    positions = [(p, w) for w, ps in inv.items() for p in ps]
    return " ".join(w for _, w in sorted(positions))


def terms_of(axis):
    """The quoted phrases inside an arm's boolean string."""
    return re.findall(r'"([^"]+)"', axis)


def main():
    cal = json.load(open(LOGS / "c3f-query-calibration-2026-09-10.json"))
    ids = cal["anchors"] + cal["decoys"]
    labels = cal["labels"]
    arms = cal["arms"]

    key = ""
    try:
        for line in open(".env"):
            if line.startswith("OPENALEX_API_KEY="):
                key = line.split("=", 1)[1].strip().strip('"')
    except FileNotFoundError:
        pass
    oa = OpenAlex(key=key, mailto="shravanh@uchicago.edu",
                  cache_path="temp/c3f-anchor-cache.json")

    cache_key = json.dumps(["texts", sorted(ids)])
    if cache_key in oa.cache:
        texts = oa.cache[cache_key]
        print(f"texts for {len(texts)} records (cached)")
    else:
        d, err = oa.get({"filter": "ids.openalex:" + "|".join(ids), "per-page": "200",
                         "select": "id,display_name,publication_year,abstract_inverted_index"})
        if err:
            sys.exit(f"batched text fetch refused (NOT an empty result): {err}")
        texts = {r["id"].rsplit("/", 1)[-1]:
                 {"title": r.get("display_name") or "", "abstract": abstract_of(r),
                  "year": r.get("publication_year")}
                 for r in d.get("results", [])}
        oa._remember(cache_key, texts)
        print(f"fetched texts for {len(texts)} of {len(ids)} records in ONE request")

    # ---- every term of every arm, tested locally against every anchor's real text
    term_arm = {}
    for arm, axis in arms.items():
        for t in terms_of(axis):
            term_arm.setdefault(t, []).append(arm)

    hits = {}          # anchor -> [terms it contains]
    for pid in ids:
        blob = textnorm.norm(f"{texts.get(pid, {}).get('title','')} "
                             f"{texts.get(pid, {}).get('abstract','')}")
        hits[pid] = sorted(t for t in term_arm if textnorm.norm(t) in blob)

    term_reach = {t: sum(1 for pid in cal["anchors"] if t in hits[pid]) for t in term_arm}
    unreached = [pid for pid in cal["anchors"] if not hits[pid]]

    print(f"\n== anchors reached by at least one term of any arm: "
          f"{len(cal['anchors']) - len(unreached)}/{len(cal['anchors'])} ==")
    print("\n== terms that reach nothing (dead weight in the production query) ==")
    for t, n in sorted(term_reach.items(), key=lambda kv: kv[1]):
        if n == 0:
            print(f"  0   {t:44} [{', '.join(sorted(set(term_arm[t])))[:52]}]")
    print("\n== terms that earn their place ==")
    for t, n in sorted(term_reach.items(), key=lambda kv: -kv[1]):
        if n:
            print(f"  {n:>2}  {t:44} [{', '.join(sorted(set(term_arm[t])))[:52]}]")

    print(f"\n== the {len(unreached)} anchors NO term reaches — read them, do not tighten ==")
    for pid in unreached:
        t = texts.get(pid, {})
        print(f"\n  {pid}  {labels.get(pid,'')[:70]}")
        print(f"    title: {t.get('title','')[:110]}")
        ab = t.get("abstract", "")
        print(f"    abstract: {(ab[:300] + '...') if len(ab) > 300 else (ab or '(none indexed)')}")

    blob = {"date": DATE, "n_anchors": len(cal["anchors"]), "n_decoys": len(cal["decoys"]),
            "term_reach": term_reach, "term_arm": term_arm,
            "per_anchor_terms": hits, "unreached": unreached,
            "texts": {k: {"title": v["title"], "year": v["year"],
                          "abstract_chars": len(v["abstract"])} for k, v in texts.items()}}
    (LOGS / f"c3f-anchor-vocabulary-{DATE}.json").write_text(json.dumps(blob, indent=2) + "\n")

    md = [f"# C.3.f — which arm terms actually occur in the anchors — {DATE}", "",
          "Generated by `source/build/goldset/382_c3f_anchor_vocabulary_audit.py`. One batched",
          "request for all thirty texts; every term tested locally against the real text.", "",
          f"Anchors reached by at least one term: **{len(cal['anchors']) - len(unreached)} of "
          f"{len(cal['anchors'])}**.", "",
          "| term | anchors reached | arm |", "|---|---|---|"]
    md += [f"| `{t}` | {n} | {', '.join(sorted(set(term_arm[t])))} |"
           for t, n in sorted(term_reach.items(), key=lambda kv: -kv[1])]
    md += ["", f"## The {len(unreached)} anchors no term reaches", ""]
    for pid in unreached:
        t = texts.get(pid, {})
        md += [f"**`{pid}` — {labels.get(pid,'')}**", "",
               f"- title: {t.get('title','')}",
               f"- abstract: {(t.get('abstract','') or '(none indexed)')[:400]}", ""]
    (LOGS / f"c3f-anchor-vocabulary-{DATE}.md").write_text("\n".join(md))
    print(f"\nwrote c3f-anchor-vocabulary-{DATE}.json and .md")


main()
