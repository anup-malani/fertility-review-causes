#!/usr/bin/env python3
"""
423 — A.6 (TICK-087): build and stratify ARM C, the arm PI call 7(a) opened.

Why. Reading (a) put premarital-sex and out-of-wedlock norms inside A.6's exposure. `420` measured
the consequence: ARM C is 1,222 records, nearly disjoint from the two frozen arms (2 shared with
ARM A, 55 with ARM B), so the ruling added an arm rather than widening one. Up to 1,165 of those
records are new, 179 carry a fertility-outcome term and 6 carry an identified-design marker. Until
they are screened, §14's "9 of 15" is not a ceiling and `PRIMARY_NORM_FERTILITY = 0` is
conditional.

Design, following `410` rather than reinventing it
--------------------------------------------------
Same deterministic flagging, same principle: the conclusion is an absence, so effort goes where a
primary-cell study would be, the top strata are read exhaustively and the tail is sampled. Two
differences forced by what ARM C is:

  1. **Deduplication comes first.** Many ARM C records are already in the 2,815-record snowball pool
     and 164 of those are already screened. Screening them again would inflate the apparent work
     and risk contradicting an existing decision. Only genuinely new records are stratified.
  2. **The decisive stratum is defined on ARM C's own terms.** `410`'s S1 required exposure + design
     + fertility markers, where "exposure" meant the method-object stigma vocabulary. Here the
     exposure is the behaviour object, so C1 is: behaviour-object norm + design + fertility.

The flagger is the same one `410` positive-controlled against `408`'s two canons, and it is
re-controlled here on Ragan 2012 — the record that prompted call 7 and the only anchor reachable by
ARM C. A flagger that cannot route Ragan into a read stratum is the wrong flagger for this arm.

OpenAlex hazards honoured: cursor paging rather than deep `page=`; ids OR'd with `|` inside one
filter value; no commas inside a filter value; curl rather than urllib for want of a CA bundle.
"""
import json, re, subprocess, sys, urllib.parse, datetime, pathlib, time, random, csv
from collections import Counter

MAILTO = "shravanh@uchicago.edu"
BASE = "https://api.openalex.org/works"
LOGDIR = pathlib.Path("literature/search-logs")
CACHE = pathlib.Path("temp/a6-arm-c-universe-cache.json")
POOL = LOGDIR / "a6-snowball-round1-2026-09-17.json"
SCREENED = pathlib.Path("extraction/stigma-reduction-contraception-abortion-screened.csv")
SELECT = "id,display_name,publication_year,cited_by_count,authorships,abstract_inverted_index,type"
SEED = 20260917
RAGAN = "W2187750596"


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

STIGMA_WIDE = ('("stigma" OR "taboo" OR "social disapproval" OR "moral opposition" '
               'OR "disapproval" OR "shame" OR "social sanction" OR "illegitimacy")')
BEHAVIOUR = ('("premarital sex" OR "pre-marital sex" OR "nonmarital childbearing" '
             'OR "non-marital childbearing" OR "out-of-wedlock" OR "out of wedlock" '
             'OR "unwed motherhood" OR "unmarried motherhood" OR "illegitimate birth" '
             'OR "teenage pregnancy")')
ARM_C = f"{STIGMA_WIDE} AND {BEHAVIOUR}"

MARKERS = {
    "design": [r"instrumental variable", r"\b2sls\b", r"two-stage least squares",
               r"difference-in-difference", r"differences-in-difference",
               r"natural experiment", r"regression discontinuity", r"\brdd\b",
               r"randomi[sz]ed controlled trial", r"\brct\b", r"event study",
               r"synthetic control", r"fixed effects", r"panel data", r"quasi-experiment",
               r"propensity score", r"exogenous variation", r"causal effect"],
    "fertility_outcome": [r"\bfertility\b", r"total fertility", r"\btfr\b", r"birth rate",
                          r"\bbirths\b", r"childbearing", r"\bparity\b", r"children ever born",
                          r"completed fertility", r"family size", r"number of children"],
    "use_outcome": [r"contraceptive use", r"contraceptive uptake", r"contraceptive prevalence",
                    r"unmet need", r"\buptake\b", r"birth control use"],
    "norm_exposure": [r"stigma", r"taboo", r"disapprov", r"\bshame\b", r"social sanction",
                      r"illegitimac", r"moral opposition", r"acceptabilit"],
    "behaviour_object": [r"premarital sex", r"pre-marital sex", r"nonmarital childbearing",
                         r"out-of-wedlock", r"out of wedlock", r"unwed", r"unmarried mother",
                         r"illegitimate birth", r"teenage pregnancy", r"adolescent pregnancy"],
    "method_object": [r"contracept", r"abortion", r"family planning", r"birth control",
                      r"sterili[sz]ation"],
    "measure_only": [r"scale development", r"validat", r"psychometric", r"conceptual framework",
                     r"systematic review", r"scoping review", r"editorial", r"commentary",
                     r"qualitative", r"focus group", r"in-depth interview", r"ethnograph",
                     r"\bhandbook\b"],
    "off_topic": [r"\bhiv\b", r"\baids\b", r"mental illness", r"obesity", r"leprosy",
                  r"substance use", r"incarcerat"],
}
COMPILED = {k: [re.compile(p, re.I) for p in v] for k, v in MARKERS.items()}

ORDER = ["C1_DECISIVE", "C2_DESIGN", "C3_FERT_NODESIGN", "C4_NORM_ONLY", "C5_WEAK",
         "C6_NOABSTRACT"]
EXHAUSTIVE = {"C1_DECISIVE", "C2_DESIGN"}
SAMPLE_N = {"C3_FERT_NODESIGN": 80, "C4_NORM_ONLY": 60, "C5_WEAK": 40, "C6_NOABSTRACT": 40}


class Refused(Exception):
    """A failed request. Never let this reach a counter as a zero."""


def _cache():
    try:
        return json.loads(CACHE.read_text())
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def _get(qs, cache, _retried=False):
    if qs in cache:
        return cache[qs]
    url = f"{BASE}?{qs}&mailto={MAILTO}" + (f"&api_key={API_KEY}" if API_KEY else "")
    p = subprocess.run(["curl", "-s", "-S", "--max-time", "90", url],
                       capture_output=True, text=True)
    if p.returncode != 0:
        raise Refused(f"curl exit {p.returncode}")
    try:
        d = json.loads(p.stdout)
    except json.JSONDecodeError:
        raise Refused(f"non-JSON: {p.stdout[:120]!r}")
    if "error" in d:
        if not _retried and "rate" in str(d.get("error", "")).lower():
            time.sleep(5.0)
            return _get(qs, cache, _retried=True)
        raise Refused(str(d.get("error")))
    if "meta" not in d:
        raise Refused("no meta")
    cache[qs] = d
    CACHE.parent.mkdir(parents=True, exist_ok=True)
    CACHE.write_text(json.dumps(cache))
    time.sleep(PACE)
    return d


def abstract_of(w) -> str:
    inv = w.get("abstract_inverted_index")
    if not inv:
        return ""
    pos = {}
    for word, idxs in inv.items():
        for i in idxs:
            pos[i] = word
    return " ".join(pos[i] for i in sorted(pos))


def flags_for(text):
    return {k: any(p.search(text) for p in ps) for k, ps in COMPILED.items()}


def stratum_of(f, has_abs):
    if not has_abs:
        return "C6_NOABSTRACT"
    if f["norm_exposure"] and f["design"] and f["fertility_outcome"]:
        return "C1_DECISIVE"
    if f["norm_exposure"] and f["design"]:
        return "C2_DESIGN"
    if f["norm_exposure"] and f["fertility_outcome"]:
        return "C3_FERT_NODESIGN"
    if f["norm_exposure"]:
        return "C4_NORM_ONLY"
    return "C5_WEAK"


def main():
    cache = _cache()
    print(f"pulling ARM C ({ARM_C[:56]}…)", flush=True)
    q = urllib.parse.quote(ARM_C, safe="")
    recs, cursor = [], "*"
    while cursor:
        d = _get(f"filter=title_and_abstract.search:{q}&per_page=100&select={SELECT}"
                 f"&cursor={cursor}", cache)
        recs.extend(d.get("results", []))
        cursor = (d.get("meta") or {}).get("next_cursor")
        if len(recs) % 500 == 0:
            print(f"  {len(recs)}", flush=True)
    print(f"  ARM C returned {len(recs)} records", flush=True)

    pool_ids = {r["id"] for r in json.loads(POOL.read_text())["pool"]}
    screened_ids = {r["id"] for r in csv.DictReader(SCREENED.open())}
    rows = []
    for w in recs:
        wid = w["id"].rsplit("/", 1)[-1]
        title, abst = (w.get("display_name") or ""), abstract_of(w)
        f = flags_for(f"{title} {abst}")
        rows.append({"id": wid, "title": title, "year": w.get("publication_year"),
                     "cited_by": w.get("cited_by_count"), "type": w.get("type"),
                     "has_abstract": bool(abst), "flags": f,
                     "in_snowball_pool": wid in pool_ids,
                     "already_screened": wid in screened_ids,
                     "stratum": stratum_of(f, bool(abst)),
                     "snippet": re.sub(r"\s+", " ", abst)[:300]})

    dup_screened = [r for r in rows if r["already_screened"]]
    dup_pool = [r for r in rows if r["in_snowball_pool"] and not r["already_screened"]]
    fresh = [r for r in rows if not r["in_snowball_pool"] and not r["already_screened"]]
    print(f"\n  already screened : {len(dup_screened)}")
    print(f"  in snowball pool, unscreened : {len(dup_pool)}")
    print(f"  genuinely new    : {len(fresh)}", flush=True)

    # positive control: Ragan must land in a stratum that gets read
    ragan = next((r for r in rows if r["id"] == RAGAN), None)
    ctrl = bool(ragan) and (ragan["stratum"] in EXHAUSTIVE or ragan["already_screened"])
    print(f"\n  positive control — Ragan {RAGAN}: "
          + (f"stratum {ragan['stratum']}, already_screened={ragan['already_screened']} "
             f"-> {'PASS' if ctrl else 'FAIL'}" if ragan else "NOT IN ARM C -> FAIL"), flush=True)
    if not ctrl:
        print("  the flagger does not route the record that prompted call 7 into a read stratum",
              file=sys.stderr)

    tally = Counter(r["stratum"] for r in fresh)
    rng = random.Random(SEED)
    worklist = []
    for s in ORDER:
        members = [r for r in fresh if r["stratum"] == s]
        members.sort(key=lambda r: -(r["cited_by"] or 0))
        chosen = members if s in EXHAUSTIVE else (
            rng.sample(members, min(SAMPLE_N.get(s, 0), len(members)))
            if SAMPLE_N.get(s, 0) < len(members) else members)
        for r in chosen:
            worklist.append({**r, "read_mode": "exhaustive" if s in EXHAUSTIVE else "sampled"})

    stamp = datetime.date.today().isoformat()
    LOGDIR.mkdir(parents=True, exist_ok=True)
    (LOGDIR / f"a6-arm-c-universe-{stamp}.json").write_text(json.dumps(
        {"generated": stamp, "script": "source/build/goldset/423_a6_arm_c_universe.py",
         "arm_c": ARM_C, "seed": SEED, "returned": len(recs),
         "already_screened": len(dup_screened), "in_pool_unscreened": len(dup_pool),
         "fresh": len(fresh), "control_passed": ctrl, "tally_fresh": dict(tally),
         "worklist_n": len(worklist), "records": rows}, indent=1))

    md = [f"# A.6 ARM C universe — {stamp}", "",
          "Generated by `source/build/goldset/423_a6_arm_c_universe.py`. Do not edit by hand.", "",
          "ARM C is the arm PI call 7(a) opened: stigma vocabulary against a **behaviour** object",
          "(premarital sex, out-of-wedlock childbearing) rather than a method object. `420` showed",
          "it is nearly disjoint from the two frozen arms, so the ruling added an arm rather than",
          "widening one.", "",
          f"**No record here has been screened.** ARM C returned **{len(recs):,}**; of those",
          f"**{len(dup_screened)}** are already screened and **{len(dup_pool)}** are already in the",
          f"snowball pool, leaving **{len(fresh):,}** genuinely new.", "",
          f"Positive control — Ragan 2012 (`{RAGAN}`), the record that prompted call 7 and the only",
          f"anchor reachable by ARM C: **{'PASS' if ctrl else 'FAIL'}**.", "",
          "| stratum | new records | to read | mode |", "|---|---|---|---|"]
    for s in ORDER:
        n_read = sum(1 for c in worklist if c["stratum"] == s)
        md.append(f"| `{s}` | {tally.get(s, 0):,} | {n_read:,} | "
                  f"{'exhaustive' if s in EXHAUSTIVE else 'sampled'} |")
    c1 = [r for r in fresh if r["stratum"] == "C1_DECISIVE"]
    c2 = [r for r in fresh if r["stratum"] == "C2_DESIGN"]
    for label, group in (("C1_DECISIVE — norm exposure + design + fertility outcome", c1),
                         ("C2_DESIGN — norm exposure + design, no fertility outcome", c2)):
        md += ["", f"## {label} — in full", ""]
        if not group:
            md.append("*Empty.*")
        else:
            md += ["| id | year | cites | title |", "|---|---|---|---|"]
            for r in sorted(group, key=lambda r: -(r["cited_by"] or 0)):
                md.append(f"| `{r['id']}` | {r['year']} | {r['cited_by']} | "
                          f"{(r['title'] or '')[:88].replace('|', '/')} |")
    (LOGDIR / f"a6-arm-c-universe-{stamp}.md").write_text("\n".join(md) + "\n")
    print(f"\nfresh strata: {dict(tally)}")
    print(f"worklist {len(worklist)}; C1={len(c1)} C2={len(c2)}")
    print(f"wrote {LOGDIR}/a6-arm-c-universe-{stamp}.{{json,md}}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
