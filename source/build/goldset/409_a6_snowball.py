#!/usr/bin/env python3
"""
409 — A.6 (TICK-087) stage 3, Phase 2: citation snowball round 1 from the 15 resolved anchors, and
the bridge test that follows from 408's diagnosis.

Why this carries recall rather than supplementing it
-----------------------------------------------------
`408` established that A.6's term channel cannot be primary: the stage-2 frame reached 0 of 15
resolved anchors, the two-arm replacement reaches 9, and the six it misses fail for reasons no
choice of terms can fix — three of them (Cleland and Wilson 1987, Bongaarts and Watkins 1996,
Lesthaeghe 1983) are unreachable by any operational vocabulary including A.3's own. PROTOCOL §5.1
Phase 2 is therefore the primary channel here, not the supplement, and this script builds it.

The bridge test, which is the point
-----------------------------------
`408`'s diagnosis was that A.6's construct spans two literatures that do not share vocabulary: a
STIGMA canon that never mentions fertility, and a DEMOGRAPHIC canon that never says stigma. Their
vocabulary intersection is 20 records. But a study that actually estimates A.6's parameter would
have to engage both halves — it would measure a normative barrier AND report a fertility or use
outcome — and such a study would plausibly **cite both canons** even though no single query reaches
it.

So every snowball candidate is scored not just by how many seeds link to it but by **which strata
those seeds belong to**. A candidate linked by seeds from both `STIGMA_CANON` and `OPPOSITION` is a
*bridge*, and bridges are this chapter's highest-prior candidates for the primary estimand cell.
This is a citation-structure test for a construct whose vocabulary test failed, and it is the reason
the snowball is worth running before PI call 1 is answered: bridges are candidates under either the
registered definition or the redefinition that call proposes.

Direction and bounding
----------------------
  BACKWARD  every seed's `referenced_works`, taken whole. Cheap (664 ids across 15 seeds) and
            unfiltered, because a seed's own reference list is by construction on-topic. Note that
            Cleland and Wilson 1987 and Lesthaeghe 1983 have **no** reference list in the index, so
            the backward channel is empty for exactly the anchors the term channel also missed.
  FORWARD   `cites:<seed>` intersected with the OBJECT block. The filter is principled rather than
            merely economical: A.6's claim is about contraception and abortion, so a citing paper
            with no contraceptive object cannot be in scope. It is also what makes the round
            tractable — it removes 77% of raw forward citations overall and 99% of Link and Phelan
            2001's 8,624, which would otherwise flood the pool with the general stigma-theory
            literature that `404` already measured as 148 records of HIV-stigma contamination.

Round 1 only. PROTOCOL §5.1 caps snowball depth at 2 rounds (Wohlin 2014); round 2 is a separate
run seeded on round 1's screened-relevant set, which does not exist yet because **nothing here has
been screened**.

Lessons honoured
----------------
  refusals-read-as-zeros   — a failed page raises and is reported; a seed whose expansion refused is
      recorded as incomplete rather than as having no citations.
  read-the-mechanism-not-the-instrument-name — the bridge score is a prior for screening order, not
      an inclusion criterion. No record is admitted or excluded by it.
  generate-result-tables-never-retype — emits the pool as json plus an md summary.

OpenAlex hazards honoured
-------------------------
  - filters are comma-separated, so no comma may appear inside a filter VALUE; none does
  - ids are OR'd with "|" inside one filter value, which is the documented form and needs no commas
  - cursor paging is used rather than deep `page=`, which caps out
  - this Python has no CA bundle: shell out to curl rather than urllib
"""
import json, subprocess, sys, urllib.parse, datetime, pathlib, time
from collections import defaultdict

MAILTO = "shravanh@uchicago.edu"
BASE = "https://api.openalex.org/works"
LOGDIR = pathlib.Path("literature/search-logs")
CACHE = pathlib.Path("temp/a6-snowball-cache.json")
ANCHOR_JSON = LOGDIR / "a6-anchor-resolution-2026-09-17.json"
SELECT = "id,display_name,publication_year,cited_by_count,authorships,abstract_inverted_index"
OBJECT = ('("contraception" OR "contraceptive" OR "abortion" OR "family planning" '
          'OR "birth control")')


def _api_key():
    try:
        for line in open(".env"):
            if line.startswith("OPENALEX_API_KEY="):
                return line.split("=", 1)[1].strip().strip('"') or None
    except FileNotFoundError:
        pass
    return None


API_KEY = _api_key()
PACE = 0.25 if API_KEY else 1.25


class Refused(Exception):
    """A failed request. Never let this reach a counter as a zero."""


def _cache_load():
    try:
        return json.loads(CACHE.read_text())
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def _get(qs: str, cache: dict, _retried=False):
    if qs in cache:
        return cache[qs]
    url = f"{BASE}?{qs}&mailto={MAILTO}"
    if API_KEY:
        url += f"&api_key={API_KEY}"
    p = subprocess.run(["curl", "-s", "-S", "--max-time", "90", url],
                       capture_output=True, text=True)
    if p.returncode != 0:
        raise Refused(f"curl exit {p.returncode}: {p.stderr.strip()[:200]}")
    try:
        d = json.loads(p.stdout)
    except json.JSONDecodeError:
        raise Refused(f"non-JSON body: {p.stdout[:200]!r}")
    if "error" in d:
        msg = f"{d.get('error')} {d.get('message','')}"
        if not _retried and "rate" in msg.lower():
            time.sleep(5.0)
            return _get(qs, cache, _retried=True)
        raise Refused(f"api error: {msg}")
    if "meta" not in d:
        raise Refused(f"no meta in body: {p.stdout[:200]!r}")
    cache[qs] = d
    CACHE.parent.mkdir(parents=True, exist_ok=True)
    CACHE.write_text(json.dumps(cache))
    time.sleep(PACE)
    return d


def paged(filter_expr: str, cache: dict, cap=4000):
    """Cursor-paged fetch of one filter expression."""
    out, cursor = [], "*"
    while cursor and len(out) < cap:
        d = _get(f"filter={filter_expr}&per_page=100&select={SELECT}&cursor={cursor}", cache)
        out.extend(d.get("results", []))
        cursor = (d.get("meta") or {}).get("next_cursor")
    return out


def rec(w):
    auths = w.get("authorships") or []
    return {"id": w["id"].rsplit("/", 1)[-1], "title": w.get("display_name"),
            "year": w.get("publication_year"), "cited_by": w.get("cited_by_count"),
            "first_author": (auths[0]["author"]["display_name"] if auths else None),
            "has_abstract": bool(w.get("abstract_inverted_index"))}


def main():
    cache = _cache_load()
    seeds = [a for a in json.loads(ANCHOR_JSON.read_text())["anchors"] if a["status"] == "resolved"]
    seed_ids = {s["id"] for s in seeds}
    stratum_of = {s["id"]: s["stratum"] for s in seeds}
    label_of = {s["id"]: s["asked"] for s in seeds}

    links = defaultdict(list)          # candidate id -> [(seed_id, direction)]
    meta, refusals, per_seed = {}, [], {}

    print("BACKWARD — each seed's reference list", flush=True)
    backward_ids = defaultdict(set)
    for s in seeds:
        try:
            d = _get(f"filter=openalex:{s['id']}&per_page=1&select=id,referenced_works", cache)
            refs = [r.rsplit("/", 1)[-1] for r in
                    ((d.get("results") or [{}])[0].get("referenced_works") or [])]
        except Refused as e:
            refusals.append((f"backward {s['asked']}", str(e)))
            print(f"  REFUSED  {s['asked']}", file=sys.stderr, flush=True)
            continue
        for r in refs:
            backward_ids[r].add(s["id"])
        per_seed[s["asked"]] = {"backward": len(refs)}
        print(f"  {len(refs):>4}  {s['asked']}", flush=True)

    # batch-fetch metadata for backward ids, 50 at a time, OR'd with "|"
    bids = [b for b in backward_ids if b not in seed_ids]
    print(f"  fetching metadata for {len(bids)} distinct backward ids", flush=True)
    for i in range(0, len(bids), 50):
        chunk = bids[i:i + 50]
        try:
            d = _get(f"filter=openalex:{'|'.join(chunk)}&per_page=50&select={SELECT}", cache)
        except Refused as e:
            refusals.append((f"backward meta chunk {i}", str(e)))
            continue
        for w in d.get("results", []):
            r = rec(w)
            meta[r["id"]] = r
    for b in bids:
        if b in meta:
            for sid in backward_ids[b]:
                links[b].append((sid, "backward"))

    print("FORWARD — citing works, intersected with the object block", flush=True)
    obj = urllib.parse.quote(OBJECT, safe="")
    for s in seeds:
        try:
            ws = paged(f"cites:{s['id']},title_and_abstract.search:{obj}", cache)
        except Refused as e:
            refusals.append((f"forward {s['asked']}", str(e)))
            print(f"  REFUSED  {s['asked']}", file=sys.stderr, flush=True)
            continue
        per_seed.setdefault(s["asked"], {})["forward"] = len(ws)
        for w in ws:
            r = rec(w)
            if r["id"] in seed_ids:
                continue
            meta[r["id"]] = r
            links[r["id"]].append((s["id"], "forward"))
        print(f"  {len(ws):>4}  {s['asked']}", flush=True)

    pool = []
    for cid, ls in links.items():
        sids = {sid for sid, _ in ls}
        strata = {stratum_of[sid] for sid in sids}
        pool.append({**meta[cid],
                     "degree": len(sids),
                     "seeds": sorted(label_of[sid] for sid in sids),
                     "directions": sorted({d for _, d in ls}),
                     "strata": sorted(strata),
                     "bridge": len({"STIGMA_CANON", "OPPOSITION"} & strata) == 2,
                     "registered_linked": "REGISTERED" in strata})
    pool.sort(key=lambda r: (-r["degree"], -(r["cited_by"] or 0)))

    bridges = [r for r in pool if r["bridge"]]
    deg = defaultdict(int)
    for r in pool:
        deg[r["degree"]] += 1
    summary = {"seeds": len(seeds), "pool": len(pool),
               "backward_distinct": len(bids), "bridges": len(bridges),
               "degree_ge2": sum(1 for r in pool if r["degree"] >= 2),
               "degree_ge3": sum(1 for r in pool if r["degree"] >= 3),
               "no_abstract": sum(1 for r in pool if not r["has_abstract"]),
               "degree_distribution": dict(sorted(deg.items()))}

    stamp = datetime.date.today().isoformat()
    LOGDIR.mkdir(parents=True, exist_ok=True)
    (LOGDIR / f"a6-snowball-round1-{stamp}.json").write_text(json.dumps(
        {"generated": stamp, "script": "source/build/goldset/409_a6_snowball.py",
         "object_filter": OBJECT, "summary": summary, "per_seed": per_seed,
         "refusals": [{"label": l, "error": e} for l, e in refusals], "pool": pool}, indent=1))

    md = [f"# A.6 snowball round 1 — {stamp}", "",
          "Generated by `source/build/goldset/409_a6_snowball.py`. Do not edit by hand;",
          "re-run the script.", "",
          "Phase 2 of PROTOCOL §5.1, run as the **primary** channel rather than the supplement,",
          "because `408` showed A.6's term channel reaches 0 of 15 anchors on the stage-2 frame and",
          "9 of 15 on its replacement, with the remaining six unreachable by any vocabulary.", "",
          "**Nothing here has been screened.** This is a candidate pool, not an evidence base. The",
          "bridge flag is a prior for screening ORDER and admits nothing.", ""]
    if refusals:
        md += [f"**{len(refusals)} request(s) REFUSED.** Those expansions are incomplete, not empty.",
               ""]
    md += [f"Seeds **{summary['seeds']}** · pool **{summary['pool']:,}** · distinct backward ids "
           f"**{summary['backward_distinct']}** · no abstract **{summary['no_abstract']:,}**", "",
           f"Linked by ≥2 seeds: **{summary['degree_ge2']:,}** · by ≥3: **{summary['degree_ge3']:,}**",
           "",
           f"**Bridges — linked by both the stigma canon and the opposition canon: "
           f"{summary['bridges']}.** These are the highest-prior candidates for "
           f"`PRIMARY_NORM_FERTILITY`, because a study estimating A.6's parameter must engage both "
           f"halves of a construct whose two literatures share only 20 records of vocabulary.", "",
           "| degree | candidates |", "|---|---|"]
    for k, v in summary["degree_distribution"].items():
        md.append(f"| {k} | {v:,} |")
    md += ["", "## Per-seed expansion", "",
           "| seed | backward refs | forward (object-filtered) |", "|---|---|---|"]
    for s in seeds:
        v = per_seed.get(s["asked"], {})
        md.append(f"| {s['asked']} ({s['stratum']}) | {v.get('backward', 'REFUSED')} | "
                  f"{v.get('forward', 'REFUSED')} |")
    if bridges:
        md += ["", "## Bridges, ranked", "",
               "| id | year | cites | first author | title | seeds |", "|---|---|---|---|---|---|"]
        for r in bridges[:60]:
            t = (r["title"] or "")[:88].replace("|", "/")
            md.append(f"| `{r['id']}` | {r['year']} | {r['cited_by']} | {r['first_author']} | "
                      f"{t} | {'; '.join(r['seeds'])} |")
    md += ["", "## Highest-degree candidates", "",
           "| id | deg | year | cites | first author | title |", "|---|---|---|---|---|---|"]
    for r in pool[:40]:
        t = (r["title"] or "")[:88].replace("|", "/")
        md.append(f"| `{r['id']}` | {r['degree']} | {r['year']} | {r['cited_by']} | "
                  f"{r['first_author']} | {t} |")
    (LOGDIR / f"a6-snowball-round1-{stamp}.md").write_text("\n".join(md) + "\n")

    print(f"\npool {summary['pool']:,} · bridges {summary['bridges']} · "
          f"deg>=2 {summary['degree_ge2']:,} · deg>=3 {summary['degree_ge3']:,}")
    print(f"wrote {LOGDIR}/a6-snowball-round1-{stamp}.{{json,md}}")
    if refusals:
        print(f"{len(refusals)} refusal(s) — those expansions are incomplete, not empty",
              file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
