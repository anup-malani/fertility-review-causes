#!/usr/bin/env python3
"""
408 — A.6 (TICK-087) stage 3: the reachability ceiling of the frozen frame, and the two-arm
retrieval design that replaces it.

Why this exists
---------------
`407` resolved 15 of 20 cold-start anchors and found that the frame frozen in stage 2 reaches
**0** of them on the probed spelling and **1** on the corrected spelling. A frame that retrieves 668
records and none of its own canon is not a narrow frame, it is the wrong instrument. This script
establishes why, and measures the design that fixes it, so the scope doc can be amended with
numbers rather than with an intention.

The diagnosis: two literatures, disjoint vocabularies
-----------------------------------------------------
Testing each block of the frozen conjunction separately against each anchor (block B below) shows a
clean bifurcation, and it is not a missing-abstract artefact -- 9 of 10 anchors tested have
abstracts in the index:

  the DEMOGRAPHIC canon   (Cleland and Wilson 1987, Bongaarts and Watkins 1996, Bongaarts and
                          Bruce 1995, Casterline 2000, Sedgh 2014, Bongaarts 1991, Lesthaeghe 1983)
                          satisfies the OBJECT block and often the OUTCOME block, and fails the
                          STIGMA block. This literature does not use the word stigma. It says
                          *unmet need*, *reasons for non-use*, *opposition*, *disapproval*.

  the STIGMA canon        (Kumar 2009, Norris 2011, Cockrill 2013 x2, Link and Phelan 2001)
                          satisfies the STIGMA block and fails the OUTCOME block. This literature
                          does not mention fertility. It measures and theorises the construct.

A.6's registered exposure sits at the intersection of these two, and the intersection is nearly
empty of canonical work. The 668 records that satisfy all three blocks are therefore not the
literature's core but a thin and partly accidental slice of it -- a hand sample of three pulled at
random included one paper on rheumatic heart disease in Uganda.

The design that replaces it
---------------------------
Two arms, pulled SEPARATELY and deduplicated by id, because an AND-containing arm cannot be OR'd
into a union:

  ARM A  compound-stigma phrases AND object, and **no outcome block**
  ARM B  opposition / unmet-need vocabulary AND object, and **no outcome block**

Dropping the outcome block is the substantive change, and it is forced. Requiring a fertility word
at retrieval time costs ARM B two of nine canonical anchors (3/9 with it, 5/9 without) and costs
ARM A four of six. That is ruling 2's price made concrete: almost nothing in either literature
states a fertility outcome in its title or abstract. **So the outcome restriction moves from the
retrieval step to the screening step**, where a human or a rubric can read for it, rather than
silently deleting the literature before anyone sees it. The union frame is computed exactly by
inclusion-exclusion, since the arms' intersection is itself expressible as a single conjunction.

What this does NOT fix, and the finding that follows
-----------------------------------------------------
Four anchors are unreachable by either arm: Cleland and Wilson 1987, Bongaarts and Watkins 1996,
Lesthaeghe 1983 and Casterline 2001. Block D tests the first three against **A.3's own** pass-4
block and they are unreachable there too. They are old, broad, theoretical papers whose abstracts
carry no operational vocabulary at all, so no term channel of any spelling will find them. This is
the `086` finding in a new place: **the term channel cannot be primary**, and citation snowball from
resolved anchors (PROTOCOL §5.1 Phase 2) has to carry the recall.

It also bears on PI call 1. Three of A.6's four registered seminal works are the ideational-change
canon rather than a stigma canon, and the fourth (Goldin and Katz 2002) is A.2's technology canon
and did not resolve in `407`. On the registry's own citation list, **A.6 has no canonical literature
of its own** -- which is an argument about whether the hypothesis is separable, not merely about how
to search for it.

Lessons honoured
----------------
  validate-a-null-detector-on-positives — the reachability test is itself positive-controlled in
      block A on records known to be inside the frame, because a 0/15 result from a broken test
      looks exactly like a 0/15 result from a broken frame.
  refusals-read-as-zeros    — a refusal is reported as REFUSED, never as unreachable.
  frame-growth-is-not-frame-gain — read in reverse here: the arms are larger than the frozen frame
      and the justification is measured recall, not size.
  generate-result-tables-never-retype — emits json + md; the scope doc amendment quotes those.

OpenAlex hazards honoured
-------------------------
  - filters are separated by commas, so no comma may appear inside a filter VALUE; none does
  - "?" is a wildcard; none present
  - no phrase begins with "not"; the union is computed by inclusion-exclusion, never by negation
  - an AND-containing arm cannot be OR'd into a union; the arms are pulled separately
  - this Python has no CA bundle: shell out to curl rather than urllib
"""
import json, subprocess, sys, urllib.parse, datetime, pathlib, time

MAILTO = "shravanh@uchicago.edu"
BASE = "https://api.openalex.org/works"
LOGDIR = pathlib.Path("literature/search-logs")
CACHE = pathlib.Path("temp/a6-retrieval-design-cache.json")
ANCHOR_JSON = LOGDIR / "a6-anchor-resolution-2026-09-17.json"


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

OUTCOME_WIDE = ('("fertility" OR "childbearing" OR "birth rate" OR "total fertility rate" '
                'OR "family size" OR "number of children")')
OBJECT = ('("contraception" OR "contraceptive" OR "abortion" OR "family planning" '
          'OR "birth control")')
STIGMA_PROBED = ('("abortion stigma" OR "contraceptive stigma" OR "contraception stigma" '
                 'OR "family planning stigma" OR "stigma" OR "taboo" OR "social disapproval" '
                 'OR "moral opposition")')
STIGMA_CORRECTED = STIGMA_PROBED[:-1] + (' OR "legitimation" OR "normalization" OR "normalisation" '
                                         'OR "social acceptability" OR "moral acceptability" '
                                         'OR "disapproval")')
# ARM A: the compound phrases only. The bare word "stigma" is not used, because paired with the
# object block it is what dragged in the 148 HIV-stigma records measured by 404.
STIGMA_COMPOUND = ('("abortion stigma" OR "contraceptive stigma" OR "contraception stigma" '
                   'OR "family planning stigma")')
# ARM B: the demographic half's own words for the same construct. "unmet need" is included because
# it is the container in which this literature reports opposition as a reason for non-use, and it is
# where section 5's dose unit lives.
OPPOSITION = ('("unmet need" OR "reasons for nonuse" OR "reasons for non-use" '
              'OR "opposition to use" OR "husband opposition" OR "partner opposition" '
              'OR "religious objection" OR "moral objection" OR "disapproval" '
              'OR "social acceptability" OR "legitimation" OR "normative approval")')
A3_BLOCK = ('("diffusion of fertility control" OR "ideational change" OR "fertility diffusion" '
            'OR "innovation diffusion" OR "spread of birth control" OR "social learning" '
            'OR "cultural transmission" OR "social contagion" OR "spatial diffusion" '
            'OR "family limitation")')

FRAMES = {
    "frozen 3-block (probed)": f"{STIGMA_PROBED} AND {OBJECT} AND {OUTCOME_WIDE}",
    "frozen 3-block (corrected)": f"{STIGMA_CORRECTED} AND {OBJECT} AND {OUTCOME_WIDE}",
    "ARM A compound-stigma x object": f"{STIGMA_COMPOUND} AND {OBJECT}",
    "ARM B opposition x object": f"{OPPOSITION} AND {OBJECT}",
    "ARM B with outcome block (rejected)": f"{OPPOSITION} AND {OBJECT} AND {OUTCOME_WIDE}",
    "ARM A intersect ARM B": f"{STIGMA_COMPOUND} AND {OPPOSITION} AND {OBJECT}",
}
BLOCKS = {"stigma block": STIGMA_PROBED, "object block": OBJECT, "outcome block": OUTCOME_WIDE}


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
    p = subprocess.run(["curl", "-s", "-S", "--max-time", "60", url],
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


def size(query: str, cache: dict) -> int:
    return _get(f"filter=title_and_abstract.search:{urllib.parse.quote(query, safe='')}"
                f"&per_page=1", cache)["meta"]["count"]


def reach(oa_id: str, query: str, cache: dict) -> bool:
    return _get(f"filter=openalex:{oa_id},title_and_abstract.search:"
                f"{urllib.parse.quote(query, safe='')}&per_page=1&select=id",
                cache)["meta"]["count"] == 1


def has_abstract(oa_id: str, cache: dict) -> bool:
    d = _get(f"filter=openalex:{oa_id}&per_page=1&select=id,abstract_inverted_index", cache)
    return bool((d.get("results") or [{}])[0].get("abstract_inverted_index"))


def main():
    cache = _cache_load()
    refusals, R = [], {}
    anchors = [a for a in json.loads(ANCHOR_JSON.read_text())["anchors"]
               if a["status"] == "resolved"]

    print("A — positive control: records known to be inside the frozen frame must read as reachable",
          flush=True)
    frozen = FRAMES["frozen 3-block (probed)"]
    d = _get(f"filter=title_and_abstract.search:{urllib.parse.quote(frozen, safe='')}"
             f"&per_page=3&select=id", cache)
    control_ids = [w["id"].rsplit("/", 1)[-1] for w in d["results"]]
    control_ok = all(reach(i, frozen, cache) for i in control_ids)
    R["positive control passed"] = control_ok
    print(f"  {control_ids} -> {'PASS' if control_ok else 'FAIL'}", flush=True)
    if not control_ok:
        print("  reachability test is broken; refusing to report a recall statistic", file=sys.stderr)
        return 2

    print("B — frame sizes", flush=True)
    for name, q in FRAMES.items():
        try:
            R[f"size: {name}"] = size(q, cache)
            print(f"  {R[f'size: {name}']:>8}  {name}", flush=True)
        except Refused as e:
            refusals.append((f"size {name}", str(e)))
            R[f"size: {name}"] = None
    a, b, ab = (R["size: ARM A compound-stigma x object"], R["size: ARM B opposition x object"],
                R["size: ARM A intersect ARM B"])
    if None not in (a, b, ab):
        R["size: union of arms (inclusion-exclusion)"] = a + b - ab
        print(f"  {a + b - ab:>8}  union of arms = {a} + {b} - {ab}", flush=True)

    print("C — anchor reachability, per frame", flush=True)
    per_frame = {k: 0 for k in FRAMES}
    rows = []
    for an in anchors:
        row = {"stratum": an["stratum"], "anchor": an["asked"], "id": an["id"]}
        try:
            row["has_abstract"] = has_abstract(an["id"], cache)
        except Refused as e:
            refusals.append((f"abstract {an['id']}", str(e)))
            row["has_abstract"] = None
        for name, q in FRAMES.items():
            if name == "ARM A intersect ARM B":
                continue
            try:
                ok = reach(an["id"], q, cache)
            except Refused as e:
                refusals.append((f"{name} {an['id']}", str(e)))
                ok = None
            row[name] = ok
            per_frame[name] += 1 if ok else 0
        for bname, bq in BLOCKS.items():
            try:
                row[bname] = reach(an["id"], bq, cache)
            except Refused as e:
                refusals.append((f"{bname} {an['id']}", str(e)))
                row[bname] = None
        row["either arm"] = bool(row.get("ARM A compound-stigma x object")) or \
                            bool(row.get("ARM B opposition x object"))
        rows.append(row)
        print(f"  {an['asked']:<26} abs={str(row['has_abstract'])[:5]:<5} "
              f"frozen={'y' if row['frozen 3-block (probed)'] else 'n'} "
              f"armA={'y' if row['ARM A compound-stigma x object'] else 'n'} "
              f"armB={'y' if row['ARM B opposition x object'] else 'n'} "
              f"either={'y' if row['either arm'] else 'n'}", flush=True)
    R["reachable: either arm"] = sum(1 for r in rows if r["either arm"])
    for name in FRAMES:
        if name != "ARM A intersect ARM B":
            R[f"reachable: {name}"] = per_frame[name]

    print("D — the three ideational seminals against A.3's own block", flush=True)
    for an in anchors:
        if an["asked"] in ("Cleland 1987", "Bongaarts 1996", "Lesthaeghe 1983"):
            try:
                ok = reach(an["id"], A3_BLOCK, cache)
            except Refused as e:
                refusals.append((f"A.3 block {an['id']}", str(e)))
                ok = None
            R[f"A.3 block reaches {an['asked']}"] = ok
            print(f"  {'yes' if ok else 'NO '}  {an['asked']}", flush=True)

    stamp = datetime.date.today().isoformat()
    LOGDIR.mkdir(parents=True, exist_ok=True)
    (LOGDIR / f"a6-retrieval-design-{stamp}.json").write_text(json.dumps(
        {"generated": stamp, "script": "source/build/goldset/408_a6_retrieval_design.py",
         "frames": FRAMES, "counts": R, "anchors": rows,
         "refusals": [{"label": l, "error": e} for l, e in refusals]}, indent=1))

    n = len(rows)
    y = {True: "yes", False: "**NO**", None: "REFUSED"}
    md = [f"# A.6 retrieval design and reachability ceiling — {stamp}", "",
          "Generated by `source/build/goldset/408_a6_retrieval_design.py`. Do not edit by hand;",
          "re-run the script.", "",
          "**No production query has been run and no record has been screened.** This measures",
          "whether a frame *would* retrieve known-relevant work. A count is not an evidence base.", ""]
    if refusals:
        md += [f"**{len(refusals)} request(s) REFUSED.** Those cells are missing, not negative.", ""]
    md += [f"Positive control: {'PASS' if control_ok else 'FAIL'} — records inside the frozen frame "
           f"read as reachable, so a low recall figure is a property of the frame and not of the test.",
           "", "## Frames", "", "| frame | records | anchors reached (of "
           f"{n}) |", "|---|---|---|"]
    for name in FRAMES:
        if name == "ARM A intersect ARM B":
            md.append(f"| {name} | {R.get(f'size: {name}'):,} | — (intersection term) |")
        else:
            md.append(f"| {name} | {R.get(f'size: {name}'):,} | **{per_frame[name]}** |")
    md.append(f"| **union of the two arms** | **{R.get('size: union of arms (inclusion-exclusion)'):,}** "
              f"| **{R['reachable: either arm']}** |")
    md += ["", "## Per-anchor, and which block rejects it", "",
           "| stratum | anchor | abstract | stigma blk | object blk | outcome blk | frozen | ARM A | ARM B | either |",
           "|---|---|---|---|---|---|---|---|---|---|"]
    for r in rows:
        md.append(f"| {r['stratum']} | {r['anchor']} | {y[r['has_abstract']]} | "
                  f"{y[r['stigma block']]} | {y[r['object block']]} | {y[r['outcome block']]} | "
                  f"{y[r['frozen 3-block (probed)']]} | {y[r['ARM A compound-stigma x object']]} | "
                  f"{y[r['ARM B opposition x object']]} | {y[r['either arm']]} |")
    md += ["", "## A.6's ideational seminals against A.3's own block", "",
           "| anchor | reachable by A.3's pass-4 block |", "|---|---|"]
    for k, v in R.items():
        if k.startswith("A.3 block reaches "):
            md.append(f"| {k[len('A.3 block reaches '):]} | {y[v]} |")
    (LOGDIR / f"a6-retrieval-design-{stamp}.md").write_text("\n".join(md) + "\n")
    print(f"\nwrote {LOGDIR}/a6-retrieval-design-{stamp}.{{json,md}}")
    if refusals:
        print(f"{len(refusals)} refusal(s) — those cells are missing, not negative", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
