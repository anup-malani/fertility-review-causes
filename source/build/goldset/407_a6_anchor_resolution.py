#!/usr/bin/env python3
"""
407 — A.6 (TICK-087) stage 3: resolve the canon to OpenAlex, then measure what share of it the
frame can actually reach.

Why this exists
---------------
Stage 2 froze a retrieval frame of 1,225 records and predicted the primary cell would be empty. A
frame size says nothing about recall. This script builds the cold-start anchor set — the works a
domain reader would name as this literature's canon — resolves each to an OpenAlex id, and then asks
of every resolved anchor: **would our frame have retrieved it?** An anchor the frame cannot reach is
a recall failure that no amount of screening effort recovers, because the record never enters the
universe.

The test that matters, and why it is run on two frames
------------------------------------------------------
`404` corrected the frame from the probe's 668 to 1,225 on the argument that the stigma block
carried only the negative pole of a construct the registry defines as *legitimation*. That argument
was made from term counts alone. Anchor reachability is an independent check on it: if the correction
was real, the corrected frame should reach anchors the probed frame misses, and the extra 557 records
should not be noise. Both frames are therefore measured against the same anchor set, and the
difference is the correction's recall payoff. If it is zero, the correction bought volume and no
recall, and §3 of the scope doc needs revisiting (`validate-a-null-detector-on-positives` run the
other way round — here the positives are known-relevant papers).

Anchor set construction
-----------------------
Three strata, kept separate because they test different things:

  REGISTERED  the four works HYPOTHESES-v5 §A.6 names as seminal. These MUST be reachable; an
              unreachable registered seminal is a scope defect, not a recall statistic.
  STIGMA_CANON the abortion- and contraceptive-stigma measurement literature (Kumar, Norris,
              Cockrill, Shellenberg, Coast, Link and Phelan). This is where the construct is
              defined and instrumented. Mostly `CONTEXT_STIGMA_MEASURE` under §9, so it tests
              whether the frame reaches the construct at all.
  OPPOSITION  the unmet-need and reason-for-non-use literature (Bongaarts and Bruce, Casterline,
              Sedgh). This is where §5's dose unit lives, so its reachability decides whether the
              demographic-significance route is populatable.

An anchor is only accepted if the resolved record's first-author surname and publication year both
match what we asked for, because OpenAlex title search will happily return a different paper with a
similar title (`resolve-then-verify`). Unverified resolutions are reported as UNRESOLVED and counted
as such; they are missing, not absent.

Lessons honoured
----------------
  refusals-read-as-zeros    — a failed request raises; an unreachable anchor and a refused request
      are different outcomes and are reported in different columns.
  validate-a-null-detector-on-positives — an anchor set is exactly a positive control for a frame.
  generate-result-tables-never-retype  — outputs json + md; the scope doc quotes those.

OpenAlex hazards honoured
-------------------------
  - a comma inside a filter VALUE is fatal; filters are SEPARATED by commas, so anchor titles are
    stripped of commas before being used as a title.search value, and the frame contains none
  - "?" is a wildcard; titles are stripped of it
  - a phrase beginning "not" parses as boolean NOT; no anchor title here begins with one
  - this Python has no CA bundle: shell out to curl rather than urllib
"""
import json, subprocess, sys, urllib.parse, datetime, pathlib, time, re

MAILTO = "shravanh@uchicago.edu"
BASE = "https://api.openalex.org/works"
LOGDIR = pathlib.Path("literature/search-logs")
CACHE = pathlib.Path("temp/a6-anchor-resolution-cache.json")


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
# As probed by 304 (668 records).
STIGMA_PROBED = ('("abortion stigma" OR "contraceptive stigma" OR "contraception stigma" '
                 'OR "family planning stigma" OR "stigma" OR "taboo" OR "social disapproval" '
                 'OR "moral opposition")')
# Corrected in scope doc section 3, with the registry's own construct restored (1,225 records).
STIGMA_CORRECTED = STIGMA_PROBED[:-1] + (' OR "legitimation" OR "normalization" OR "normalisation" '
                                         'OR "social acceptability" OR "moral acceptability" '
                                         'OR "disapproval")')

FRAME_PROBED = f"{STIGMA_PROBED} AND {OBJECT} AND {OUTCOME_WIDE}"
FRAME_CORRECTED = f"{STIGMA_CORRECTED} AND {OBJECT} AND {OUTCOME_WIDE}"

# (stratum, first-author surname, year, title)
ANCHORS = [
    ("REGISTERED", "Cleland", 1987,
     "Demand theories of the fertility transition an iconoclastic view"),
    ("REGISTERED", "Bongaarts", 1996,
     "Social interactions and contemporary fertility transitions"),
    ("REGISTERED", "Goldin", 2002,
     "The power of the pill oral contraceptives and women's career and marriage decisions"),
    ("REGISTERED", "Lesthaeghe", 1983,
     "A century of demographic and cultural change in Western Europe"),

    ("STIGMA_CANON", "Kumar", 2009, "Conceptualising abortion stigma"),
    ("STIGMA_CANON", "Norris", 2011, "Abortion stigma a reconceptualization of constituents causes and consequences"),
    ("STIGMA_CANON", "Cockrill", 2013, "The stigma of having an abortion development of a scale and characteristics of women experiencing abortion stigma"),
    ("STIGMA_CANON", "Cockrill", 2013, "I'm not that type of person managing the stigma of having an abortion"),
    ("STIGMA_CANON", "Shellenberg", 2011, "Social stigma and disclosure about induced abortion understanding stigma and disclosure"),
    ("STIGMA_CANON", "Coast", 2016, "Trajectories of women's abortion-related care a conceptual framework"),
    ("STIGMA_CANON", "Link", 2001, "Conceptualizing stigma"),
    ("STIGMA_CANON", "Hessini", 2005, "Global progress in abortion advocacy and policy an assessment of the decade since ICPD"),
    ("STIGMA_CANON", "Rossier", 2007, "Abortion an open secret rumor and social networks in Burkina Faso"),

    ("OPPOSITION", "Bongaarts", 1995, "The causes of unmet need for contraception and the social content of services"),
    ("OPPOSITION", "Casterline", 2000, "Unmet need for family planning in developing countries and implications for population policy"),
    ("OPPOSITION", "Casterline", 2001, "Obstacles to contraceptive use in Pakistan a study in Punjab"),
    ("OPPOSITION", "Casterline", 1997, "Factors underlying unmet need for family planning in the Philippines"),
    ("OPPOSITION", "Sedgh", 2014, "Reasons for contraceptive nonuse among women having unmet need for contraception in developing countries"),
    ("OPPOSITION", "Bongaarts", 1991, "The KAP-gap and the unmet need for contraception"),
    ("OPPOSITION", "Sedgh", 2016, "Insights from demographic and health surveys on reasons for nonuse of contraception"),
]


class Refused(Exception):
    """A failed request. Never let this reach a counter as a zero."""


def _cache_load():
    try:
        return json.loads(CACHE.read_text())
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def _get(url_suffix: str, cache: dict, _retried=False):
    if url_suffix in cache:
        return cache[url_suffix]
    url = f"{BASE}?{url_suffix}&mailto={MAILTO}"
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
            return _get(url_suffix, cache, _retried=True)
        raise Refused(f"api error: {msg}")
    if "meta" not in d:
        raise Refused(f"no meta in body: {p.stdout[:200]!r}")
    cache[url_suffix] = d
    CACHE.parent.mkdir(parents=True, exist_ok=True)
    CACHE.write_text(json.dumps(cache))
    time.sleep(PACE)
    return d


def clean(t: str) -> str:
    """Strip the characters that are fatal or wildcards inside an OpenAlex filter value."""
    return re.sub(r"\s+", " ", t.replace(",", " ").replace("?", " ")).strip()


def resolve(surname: str, year: int, title: str, cache: dict):
    """Title-search, then VERIFY first-author surname and year before accepting."""
    qs = (f"filter=title.search:{urllib.parse.quote(clean(title), safe='')}"
          f"&per_page=5&select=id,display_name,publication_year,authorships,cited_by_count")
    d = _get(qs, cache)
    for w in d.get("results", []):
        auths = w.get("authorships") or []
        first = (auths[0]["author"]["display_name"] if auths else "") or ""
        yr = w.get("publication_year")
        if surname.lower() in first.lower() and yr is not None and abs(yr - year) <= 1:
            return {"id": w["id"].rsplit("/", 1)[-1], "title": w["display_name"],
                    "year": yr, "cited_by": w.get("cited_by_count"), "first_author": first}
    return None


def reachable(oa_id: str, frame: str, cache: dict) -> bool:
    qs = (f"filter=openalex:{oa_id},title_and_abstract.search:"
          f"{urllib.parse.quote(frame, safe='')}&per_page=1&select=id")
    return _get(qs, cache)["meta"]["count"] == 1


def main():
    cache = _cache_load()
    rows, refusals = [], []

    for stratum, surname, year, title in ANCHORS:
        rec = {"stratum": stratum, "asked": f"{surname} {year}", "title_asked": title}
        try:
            got = resolve(surname, year, title, cache)
        except Refused as e:
            refusals.append((f"resolve {surname} {year}", str(e)))
            rec["status"] = "REFUSED"
            rows.append(rec)
            print(f"  REFUSED resolve  {surname} {year}", file=sys.stderr, flush=True)
            continue
        if not got:
            rec["status"] = "UNRESOLVED"
            rows.append(rec)
            print(f"  UNRESOLVED       {surname} {year}  {title[:54]}", flush=True)
            continue
        rec.update({"status": "resolved", **got})
        for key, frame in [("in_probed", FRAME_PROBED), ("in_corrected", FRAME_CORRECTED)]:
            try:
                rec[key] = reachable(got["id"], frame, cache)
            except Refused as e:
                refusals.append((f"{key} {got['id']}", str(e)))
                rec[key] = None
        mark = {True: "yes", False: "NO", None: "REF"}
        print(f"  {got['id']:<12} probed={mark[rec['in_probed']]:<3} "
              f"corrected={mark[rec['in_corrected']]:<3} cites={got['cited_by']:<6} "
              f"{surname} {got['year']}", flush=True)
        rows.append(rec)

    res = [r for r in rows if r["status"] == "resolved"]
    def tally(rs, key):
        return sum(1 for r in rs if r.get(key) is True)

    summary = {"anchors": len(rows), "resolved": len(res),
               "unresolved": sum(1 for r in rows if r["status"] == "UNRESOLVED"),
               "refused": sum(1 for r in rows if r["status"] == "REFUSED"),
               "reachable_probed": tally(res, "in_probed"),
               "reachable_corrected": tally(res, "in_corrected")}
    by_stratum = {}
    for s in ["REGISTERED", "STIGMA_CANON", "OPPOSITION"]:
        rs = [r for r in res if r["stratum"] == s]
        by_stratum[s] = {"resolved": len(rs), "reachable_probed": tally(rs, "in_probed"),
                         "reachable_corrected": tally(rs, "in_corrected")}

    stamp = datetime.date.today().isoformat()
    LOGDIR.mkdir(parents=True, exist_ok=True)
    (LOGDIR / f"a6-anchor-resolution-{stamp}.json").write_text(json.dumps(
        {"generated": stamp, "script": "source/build/goldset/407_a6_anchor_resolution.py",
         "frame_probed": FRAME_PROBED, "frame_corrected": FRAME_CORRECTED,
         "summary": summary, "by_stratum": by_stratum, "anchors": rows,
         "refusals": [{"label": l, "error": e} for l, e in refusals]}, indent=1))

    md = [f"# A.6 anchor resolution and frame reachability — {stamp}", "",
          "Generated by `source/build/goldset/407_a6_anchor_resolution.py`. Do not edit by hand;",
          "re-run the script.", "",
          "An anchor the frame cannot reach is a recall failure no screening effort recovers, because",
          "the record never enters the universe. **No production query has been run and no record has",
          "been screened**; this measures whether the frame *would* retrieve known-relevant work.", ""]
    if refusals:
        md += [f"**{len(refusals)} request(s) REFUSED.** Those cells are missing, not negative.", ""]
    md += [f"Anchors asked: **{summary['anchors']}** · resolved **{summary['resolved']}** · "
           f"unresolved **{summary['unresolved']}** · refused **{summary['refused']}**", "",
           f"Reachable by the **probed** frame (668): **{summary['reachable_probed']}** of "
           f"{summary['resolved']}", "",
           f"Reachable by the **corrected** frame (1,225): **{summary['reachable_corrected']}** of "
           f"{summary['resolved']}", "",
           "| stratum | resolved | reachable probed | reachable corrected |", "|---|---|---|---|"]
    for s, v in by_stratum.items():
        md.append(f"| {s} | {v['resolved']} | {v['reachable_probed']} | {v['reachable_corrected']} |")
    md += ["", "| stratum | anchor | OpenAlex | year | cites | probed | corrected |",
           "|---|---|---|---|---|---|---|"]
    mark = {True: "yes", False: "**NO**", None: "REFUSED"}
    for r in rows:
        if r["status"] != "resolved":
            md.append(f"| {r['stratum']} | {r['asked']} | — | — | — | {r['status']} | {r['status']} |")
        else:
            md.append(f"| {r['stratum']} | {r['asked']} | `{r['id']}` | {r['year']} | "
                      f"{r['cited_by']} | {mark[r['in_probed']]} | {mark[r['in_corrected']]} |")
    (LOGDIR / f"a6-anchor-resolution-{stamp}.md").write_text("\n".join(md) + "\n")

    print(f"\nresolved {summary['resolved']}/{summary['anchors']}; reachable "
          f"probed {summary['reachable_probed']} vs corrected {summary['reachable_corrected']}")
    print(f"wrote {LOGDIR}/a6-anchor-resolution-{stamp}.{{json,md}}")
    if refusals:
        print(f"{len(refusals)} refusal(s) — those cells are missing, not negative", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
