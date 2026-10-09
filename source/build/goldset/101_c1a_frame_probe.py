#!/usr/bin/env python3
"""
101 (c1a) — C.1.a (TICK-098) stage-3 frame probe: confirm C.1.a (income effect / children as a normal
good) is the next-smallest genuinely-unstarted candidate, and run the registered-construct completeness
test the A.6/A.3 episode made mandatory before any search spend.

Why this exists
---------------
C.1.a was selected by a FLIP. The fresh 2026-10-08 cross-field scout ranked, after D.1.c, C.4.a 893,
C.2.e 1,259, C.1.a 1,620 narrow — so C.2.e *looked* smaller. A pre-claim selection probe
(temp/c2e_select_probe.py) priced both against their own registered constructs and flipped the order:
C.2.e's scout union omitted plain synonyms of its own constructs (women's employment / female labor
supply), so 1,259 undercounted it to an honest ~2,035; C.1.a is near-complete and robust at ~1,620.
This script re-runs the test on-branch and reads the walls from both sides, applying the corrected rule
BEFORE screen budget is spent: price the frame against its OWN conjoined construct set, keep the generic
OR-inflaters OUT of base recall, and count the homonym load inside the frame.

The C.1.a-specific hazard
-------------------------
"Income" and "household income" sit inside the whole economics-of-the-household literature. The pure
income effect (children as a normal good, prices and the price of time held constant) is a NARROW thing;
"economic development", "GDP", "living standards" annex the development-and-fertility bundle (mortality
decline + schooling + urbanization + female wages), which is NOT the pure income effect; "female wage" /
"earnings" is the price-of-time channel (C.2.e, THE wall); "relative income" is Easterlin (C.6.a). The
completeness test must show the honest C.1.a frame is an income/wealth/normal-good frame and that folding
a free-standing "economic development" or "wage" OR annexes a neighbour literature rather than widening
C.1.a — the free-OR inflation the A.3 park was built on.

The registered-construct completeness test
------------------------------------------
Block C prices every noun the C.1.a claim names (income effect, household income, income elasticity,
permanent income, wealth effect, normal good) as (baseline OR term) minus baseline, plus the generic /
neighbour words that are the free-OR risk (economic development, GDP per capita, living standards, female
wage, relative income). A large gain from a genuine C.1.a term means the baseline was under-built; a
large gain from a generic word conjoined to nothing is the inflater, reported as such, not folded in.

The walls are read from both sides
-----------------------------------
C.2.e female-wage / price-of-time (LOAD-BEARING), C.6.a relative/cohort income, C.5.a/C.3.e/C.3.g
uncertainty-liquidity-debt, the economic-development macro bundle, and the REVERSE cell (fertility ->
income) each get three numbers: overlap with our frame, the neighbour's own frame, and the overlap among
identified records.

Lessons honoured: advance-the-baseline-when-accepting-terms; validate-a-null-detector-on-positives (the
C.2.c housing control runs first on the identical reduced outcome axis; 405 recorded 205, 52 got 181,
89_d2c 170, 100_d1c 162); refusals-read-as-zeros.

Outputs literature/search-logs/c1a-frame-probe-<date>.{json,md}. Counting only; no records retained.
"""
import json, subprocess, sys, urllib.parse, datetime, pathlib, time

MAILTO = "shravanh@uchicago.edu"
BASE = "https://api.openalex.org/works"
LOGDIR = pathlib.Path("literature/search-logs")
CACHE = pathlib.Path("temp/c1a-frame-probe-cache.json")


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

OUTCOME = ('("fertility" OR "childbearing" OR "birth rate" OR "total fertility rate" '
           'OR "childlessness" OR "fecundity" OR "time to pregnancy" OR "subfertility" '
           'OR "infertility")')

# Narrow = the distinctive normal-good / income-elasticity core. Production = the registered union.
C1A_NARROW = '("income elasticity of fertility" OR "children as a normal good" OR "normal good")'
C1A = ('("income effect" OR "household income" OR "income elasticity" OR "permanent income" '
       'OR "wealth effect" OR "income shock" OR "cash transfer" OR "lottery")')

IDENT = ('("instrumental variable" OR "difference-in-differences" OR "differences-in-differences" '
         'OR "natural experiment" OR "regression discontinuity" OR "randomized controlled trial" '
         'OR "randomised controlled trial" OR "event study" OR "synthetic control")')

OWN_CANDIDATES = [
    # genuine C.1.a constructs to test for inclusion:
    "income elasticity of fertility", "permanent income", "wealth effect", "normal good",
    "household income", "unearned income", "windfall", "income transfer", "basic income",
    # generic / neighbour-channel / homonym inflaters to catch free-OR behaviour:
    "economic development", "GDP per capita", "living standards", "economic growth",
    "female wage", "relative income", "poverty",
]

LEVELS = [
    ("realized / period fertility", '("total fertility rate" OR "birth rate" OR "completed fertility")'),
    ("fertility intentions / desired family size", '("fertility intentions" OR "desired family size" OR "number of children")'),
    ("pre-industrial / historical gradient", '("pre-industrial" OR "historical demography" OR "surviving children" OR "Malthusian")'),
]

WALLS = [
    ("C.2.e", "female wage / price of time -- a wage shock moves income AND the price of time (LOAD-BEARING; the central wall)", "unstarted",
     '("female wage" OR "opportunity cost of time" OR "female labor force participation" OR "female labour force participation" OR "earnings")'),
    ("C.6.a", "Easterlin relative / cohort income -- relative not absolute income", "drafted (branch 078, unmerged)",
     '("relative income" OR "relative cohort size" OR "Easterlin")'),
    ("C.5.a/C.3.e/C.3.g", "uncertainty / liquidity / debt -- resources via risk, not permanent-income normal good", "drafted",
     '("economic uncertainty" OR "job insecurity" OR "credit constraint" OR "liquidity constraint" OR "student debt" OR "unemployment")'),
    ("DEV", "economic-development macro bundle -- development annexes mortality/schooling/urbanization/wages, NOT the pure income effect", "excluded inflater",
     '("economic development" OR "GDP per capita" OR "economic growth" OR "modernization")'),
    ("REVERSE", "fertility -> household income (children lower maternal labor supply)", "n/a (mechanical cell)",
     '("maternal labor supply" OR "cost of children" OR "labor force participation")'),
]

HOMONYMS = [
    ("income effect in the pure consumer-theory / Slutsky sense, not household fertility",
     '("Slutsky" OR "compensated demand" OR "Hicksian")'),
    ("development-economics income with no normal-good test (the inflater reading inside our frame)",
     '("economic development" OR "developing countries" OR "GDP")'),
]


class Refused(Exception):
    """A failed request. Never let this reach a counter as a zero."""


def _cache_load():
    try:
        return json.loads(CACHE.read_text())
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def count(query: str, cache: dict, _retried=False) -> int:
    if query in cache:
        return cache[query]
    url = (f"{BASE}?filter=title_and_abstract.search:{urllib.parse.quote(query, safe='')}"
           f"&per_page=1&mailto={MAILTO}")
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
            return count(query, cache, _retried=True)
        raise Refused(f"api error: {msg}")
    try:
        n = d["meta"]["count"]
    except (KeyError, TypeError):
        raise Refused(f"no meta.count in body: {p.stdout[:200]!r}")
    cache[query] = n
    CACHE.parent.mkdir(parents=True, exist_ok=True)
    CACHE.write_text(json.dumps(cache, indent=1, sort_keys=True))
    time.sleep(PACE)
    return n


def AND(*blocks) -> str:
    return " AND ".join(b for b in blocks if b)


def main():
    cache = _cache_load()
    refusals, R = [], {}

    def q(label, query):
        try:
            n = count(query, cache)
            R[label] = n
            print(f"  {n:>8}  {label}", flush=True)
            return n
        except Refused as e:
            refusals.append((label, str(e)))
            R[label] = None
            print(f"  REFUSED  {label}  ({e})", file=sys.stderr, flush=True)
            return None

    print("A — control and frame", flush=True)
    q("control: C.2.c housing frame (a written chapter; 405 recorded 205, 52 got 181, 89_d2c 170, 100_d1c 162)",
      AND('("house price" OR "housing cost" OR "house prices")',
          '("fertility" OR "childbearing" OR "birth rate" OR "total fertility rate" OR "childlessness")'))
    q("C.1.a narrow frame (normal-good / income-elasticity core AND fertility)",
      AND(C1A_NARROW, OUTCOME))
    frame = q("C.1.a production frame (topic union AND outcome)", AND(C1A, OUTCOME))
    q("C.1.a topic block with no outcome restriction", C1A)

    print("C — completeness test: pricing every registered construct", flush=True)
    for term in OWN_CANDIDATES:
        cand = C1A[:-1] + f' OR "{term}")'
        n = q(f"own + {term}", AND(cand, OUTCOME))
        if n is not None and frame is not None:
            R[f"gain: own + {term}"] = n - frame
    if frame is not None:
        allo = C1A[:-1] + "".join(f' OR "{t}"' for t in OWN_CANDIDATES) + ")"
        n = q("C.1.a block widened by ALL registered constructs", AND(allo, OUTCOME))
        if n is not None:
            R["gain: own widened by ALL"] = n - frame

    print("E — calibrating the outcome axis", flush=True)
    for label, block in LEVELS:
        q(f"level: {label}", AND(C1A, block))

    print("F — identification markers inside the frame", flush=True)
    q("frame AND identified-design markers", AND(C1A, OUTCOME, IDENT))

    print("H — the walls, read from both sides", flush=True)
    for code, name, status, block in WALLS:
        q(f"wall {code} overlap with our frame", AND(C1A, OUTCOME, block))
        q(f"wall {code} neighbour frame", AND(block, OUTCOME))
        q(f"wall {code} overlap AND identified", AND(C1A, OUTCOME, block, IDENT))

    print("I — homonym readings inside our own frame", flush=True)
    for label, block in HOMONYMS:
        q(f"homonym: {label}", AND(C1A, OUTCOME, block))

    stamp = datetime.date.today().isoformat()
    LOGDIR.mkdir(parents=True, exist_ok=True)
    payload = {"generated": stamp, "script": "source/build/goldset/101_c1a_frame_probe.py",
               "api_key_present": bool(API_KEY), "counts": R,
               "walls": [{"code": c, "name": n, "status": s} for c, n, s, _ in WALLS],
               "refusals": [{"label": l, "error": e} for l, e in refusals]}
    (LOGDIR / f"c1a-frame-probe-{stamp}.json").write_text(json.dumps(payload, indent=1))

    def cell(v):
        return "REFUSED" if v is None else f"{v:,}"

    md = [f"# C.1.a income-effect / normal-good frame probe — {stamp}", "",
          "Generated by `source/build/goldset/101_c1a_frame_probe.py`. Do not edit by hand; re-run.", "",
          "OpenAlex `title_and_abstract.search` record counts. They size a *retrieval frame* and its",
          "overlaps. **No production query has been run, no anchor resolved, no record screened.** A",
          "study can estimate this chapter's parameter without carrying any of these phrases.", ""]
    if refusals:
        md += [f"**{len(refusals)} request(s) REFUSED.** Those rows are missing, not zero.", ""]
    md += ["| measurement | n |", "|---|---|"]
    for label, v in R.items():
        if not label.startswith("gain: "):
            md.append(f"| {label} | {cell(v)} |")
    md += ["", "## Marginal gain of candidate terms", "",
           "Priced as (baseline OR term) minus baseline. A large gain from a genuine C.1.a construct",
           "means the baseline was under-built; a large gain from a generic word ('economic development',",
           "'GDP', 'female wage', 'relative income') is a free-OR inflater that annexes a neighbour",
           "literature (the development bundle, C.2.e, C.6.a), not a widening.", "",
           "| candidate | marginal gain |", "|---|---|"]
    for label, v in R.items():
        if label.startswith("gain: "):
            md.append(f"| {label[6:]} | {v if v is not None else 'REFUSED'} |")
    md += ["", "## Walls", "",
           "Each wall: overlap with our frame, the neighbour's own frame, and the overlap among",
           "identified records. C.2.e (female wage / price of time) is the load-bearing wall: a wage",
           "shock moves income AND the price of time, so C.1.a must identify off a non-labor income/",
           "wealth shock. The economic-development bundle is the excluded inflater.", ""]
    (LOGDIR / f"c1a-frame-probe-{stamp}.md").write_text("\n".join(md) + "\n")
    print(f"\nwrote {LOGDIR}/c1a-frame-probe-{stamp}.{{json,md}}")
    if refusals:
        print(f"{len(refusals)} refusal(s) — those rows are missing, not zero", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
