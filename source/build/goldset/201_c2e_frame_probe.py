#!/usr/bin/env python3
"""
201 (c2e) — C.2.e (TICK-099) stage-3 frame probe: confirm C.2.e (female wage / opportunity cost of time
— the substitution effect of a rising price of the mother's time on fertility) is the next-smallest
genuinely-unstarted candidate, and run the registered-construct completeness test the A.6/A.3 episode
made mandatory before any search spend.

Why this exists
---------------
C.2.e is next-smallest after C.1.a (TICK-098). The 2026-10-08 scout priced C.2.e narrow at 1,259 using a
4-term union that omitted plain synonyms of C.2.e's OWN registered constructs; the TICK-098 selection
probe showed those synonyms ("female labor supply", "women's employment", "female wages") take the honest
frame to ~1,863, and "+maternal employment"/"+substitution effect" to ~2,035. This script re-runs that
test on-branch, and — unlike the C.1.a probe, which deliberately WITHHELD C.2.e's treatment/ID terms to
keep the *ranking* comparison apples-to-apples — now gives C.2.e its OWN analogous treatment terms
(minimum wage, trade shock, returns to schooling, gender wage gap) so the production *recall* frame is the
one that will actually retrieve the empirical studies. Rule applied BEFORE screen budget is spent: price
the frame against its OWN conjoined construct set, keep the generic OR-inflaters OUT of base recall, and
count the homonym load inside the frame.

The C.2.e-specific hazard
-------------------------
"Female labor" and "women's employment" sit inside the whole economics-of-gender-and-work literature. The
pure price-of-time (substitution) effect — non-labor income held constant — is a NARROW thing. The
inflaters that must stay OUT of base recall: "economic development"/"GDP" (the development bundle, which
bundles mortality decline + schooling + urbanization); "female empowerment"/"gender equality"/"female
autonomy" (D.2.a, the IDEATIONAL channel of the same phenomenon); "income effect"/"household income"
(C.1.a, the pure income/wealth channel — THE wall, read from the other side). The completeness test must
show the honest C.2.e frame is a wage/price-of-time/labor-supply frame, and that folding a free-standing
"female empowerment" or "economic development" OR annexes a neighbour literature rather than widening C.2.e.

The registered-construct completeness test
------------------------------------------
Block C prices every noun the C.2.e claim names (female wage, opportunity cost of time, female labor force
participation, female labor supply, women's employment, substitution effect, price of time, maternal
employment) PLUS C.2.e's analogous treatment/ID terms (minimum wage, trade shock, returns to schooling,
gender wage gap) as (baseline OR term) minus baseline, plus the generic / neighbour words that are the
free-OR risk (economic development, GDP per capita, female empowerment, gender equality, income effect,
household income). A large gain from a genuine C.2.e term means the baseline was under-built; a large gain
from a generic/neighbour word conjoined to nothing is the inflater, reported as such, not folded in.

The walls are read from both sides
-----------------------------------
C.1.a income/wealth (LOAD-BEARING; THE wall from the other side), D.2.a female empowerment (ideational),
C.2.h digital leisure substitution, the economic-development macro bundle, and the FLFP-as-OUTCOME /
REVERSE cell (fertility -> female labor supply) each get three numbers: overlap with our frame, the
neighbour's own frame, and the overlap among identified records.

Lessons honoured: advance-the-baseline-when-accepting-terms; validate-a-null-detector-on-positives (the
C.2.c housing control runs first on the identical reduced outcome axis; prior runs recorded 205/181/170/
162); refusals-read-as-zeros.

Outputs literature/search-logs/c2e-frame-probe-<date>.{json,md}. Counting only; no records retained.
"""
import json, subprocess, sys, urllib.parse, datetime, pathlib, time

MAILTO = "shravanh@uchicago.edu"
BASE = "https://api.openalex.org/works"
LOGDIR = pathlib.Path("literature/search-logs")
CACHE = pathlib.Path("temp/c2e-frame-probe-cache.json")


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

# Narrow = the distinctive opportunity-cost / price-of-time / substitution core.
C2E_NARROW = ('("opportunity cost of time" OR "opportunity cost of children" OR "price of time" '
              'OR "price of a woman\'s time" OR "substitution effect" AND "fertility")')
# Production = the registered construct union, with C.2.e's OWN treatment/ID terms added for recall.
C2E = ('("female wage" OR "female wages" OR "women\'s wages" OR "opportunity cost of time" '
       'OR "female labor force participation" OR "female labour force participation" '
       'OR "female labor supply" OR "female labour supply" OR "women\'s employment" '
       'OR "maternal employment" OR "substitution effect" OR "price of time" '
       'OR "returns to schooling" OR "gender wage gap" OR "minimum wage" OR "trade shock")')

IDENT = ('("instrumental variable" OR "difference-in-differences" OR "differences-in-differences" '
         'OR "natural experiment" OR "regression discontinuity" OR "randomized controlled trial" '
         'OR "randomised controlled trial" OR "event study" OR "synthetic control")')

OWN_CANDIDATES = [
    # genuine C.2.e registered constructs to test for inclusion:
    "female wage", "opportunity cost of time", "female labor force participation",
    "female labor supply", "women's employment", "maternal employment", "substitution effect",
    "price of time",
    # C.2.e's OWN analogous treatment / identification terms (withheld in the C.1.a ranking probe):
    "minimum wage", "trade shock", "returns to schooling", "gender wage gap",
    # generic / neighbour-channel / homonym inflaters to catch free-OR behaviour:
    "economic development", "GDP per capita", "female empowerment", "gender equality",
    "income effect", "household income",
]

LEVELS = [
    ("realized / period fertility", '("total fertility rate" OR "birth rate" OR "completed fertility")'),
    ("fertility intentions / desired family size", '("fertility intentions" OR "desired family size" OR "number of children")'),
    ("timing / tempo", '("fertility timing" OR "age at first birth" OR "postponement" OR "birth spacing")'),
]

WALLS = [
    ("C.1.a", "income / wealth -- a wage shock moves income AND the price of time; C.1.a owns the pure non-labor income channel (LOAD-BEARING; THE wall from the other side)", "drafted (branch 098, unmerged)",
     '("income effect" OR "household income" OR "wealth effect" OR "lottery" OR "cash transfer" OR "unearned income")'),
    ("D.2.a", "female empowerment / autonomy -- the IDEATIONAL channel of rising female status, not the wage", "drafted/ideational channel",
     '("female empowerment" OR "gender equality" OR "female autonomy" OR "gender equity" OR "women\'s autonomy")'),
    ("C.2.h", "digital leisure substitution -- substitution toward leisure goods, not labor income", "queued/drafted",
     '("smartphone" OR "social media" OR "digital leisure" OR "screen time" OR "internet")'),
    ("DEV", "economic-development macro bundle -- development annexes mortality/schooling/urbanization, NOT the pure price-of-time effect", "excluded inflater",
     '("economic development" OR "GDP per capita" OR "economic growth" OR "modernization")'),
    ("REVERSE", "fertility -> female labor supply (children reduce maternal employment); FLFP as OUTCOME not treatment", "n/a (mechanical/reverse cell)",
     '("effect of children on" OR "motherhood penalty" OR "child penalty")'),
]

HOMONYMS = [
    ("substitution effect in the pure consumer-theory / Slutsky sense, not price-of-time fertility",
     '("Slutsky" OR "compensated demand" OR "Hicksian")'),
    ("female employment as an OUTCOME of fertility, no wage shock (the reverse reading inside our frame)",
     '("child penalty" OR "motherhood penalty" OR "effect of childbearing")'),
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
    q("control: C.2.c housing frame (a written chapter; prior runs 205/181/170/162)",
      AND('("house price" OR "housing cost" OR "house prices")',
          '("fertility" OR "childbearing" OR "birth rate" OR "total fertility rate" OR "childlessness")'))
    q("C.2.e narrow frame (opportunity-cost / price-of-time core AND fertility)",
      AND(C2E_NARROW, OUTCOME))
    frame = q("C.2.e production frame (construct union + treatment terms AND outcome)", AND(C2E, OUTCOME))
    q("C.2.e topic block with no outcome restriction", C2E)

    print("C — completeness test: pricing every registered construct + own treatment terms", flush=True)
    for term in OWN_CANDIDATES:
        cand = C2E[:-1] + f' OR "{term}")'
        n = q(f"own + {term}", AND(cand, OUTCOME))
        if n is not None and frame is not None:
            R[f"gain: own + {term}"] = n - frame
    if frame is not None:
        allo = C2E[:-1] + "".join(f' OR "{t}"' for t in OWN_CANDIDATES) + ")"
        n = q("C.2.e block widened by ALL candidate terms", AND(allo, OUTCOME))
        if n is not None:
            R["gain: own widened by ALL"] = n - frame

    print("D — incremental build-up (completeness: does each registered construct add coverage?)",
          flush=True)
    # Start from the scout's narrow seed and add each registered construct in order, logging the
    # cumulative count and the marginal gain. This is the TICK-098 selection-probe method, re-run
    # on-branch: a construct that adds 0 is redundant; the point is that none of the registered
    # constructs is MISSING from the frame (the A.6/A.3 completeness requirement).
    BUILDUP = [
        "female labor force participation",   # scout seed term
        "female wage",
        "opportunity cost of time",
        "female labor supply",
        "women's employment",
        "maternal employment",
        "substitution effect",
        "price of time",
        "returns to schooling",
        "gender wage gap",
        "minimum wage",
        "trade shock",
    ]
    acc, prev = [], None
    for term in BUILDUP:
        acc.append(term)
        blk = "(" + " OR ".join(f'"{t}"' for t in acc) + ")"
        n = q(f"buildup[{len(acc)}]: + {term}", AND(blk, OUTCOME))
        if n is not None and prev is not None:
            R[f"gain: buildup + {term}"] = n - prev
        if n is not None:
            prev = n

    print("E — calibrating the outcome axis", flush=True)
    for label, block in LEVELS:
        q(f"level: {label}", AND(C2E, block))

    print("F — identification markers inside the frame", flush=True)
    q("frame AND identified-design markers", AND(C2E, OUTCOME, IDENT))

    print("H — the walls, read from both sides", flush=True)
    for code, name, status, block in WALLS:
        q(f"wall {code} overlap with our frame", AND(C2E, OUTCOME, block))
        q(f"wall {code} neighbour frame", AND(block, OUTCOME))
        q(f"wall {code} overlap AND identified", AND(C2E, OUTCOME, block, IDENT))

    print("I — homonym readings inside our own frame", flush=True)
    for label, block in HOMONYMS:
        q(f"homonym: {label}", AND(C2E, OUTCOME, block))

    stamp = datetime.date.today().isoformat()
    LOGDIR.mkdir(parents=True, exist_ok=True)
    payload = {"generated": stamp, "script": "source/build/goldset/201_c2e_frame_probe.py",
               "api_key_present": bool(API_KEY), "counts": R,
               "walls": [{"code": c, "name": n, "status": s} for c, n, s, _ in WALLS],
               "refusals": [{"label": l, "error": e} for l, e in refusals]}
    (LOGDIR / f"c2e-frame-probe-{stamp}.json").write_text(json.dumps(payload, indent=1))

    def cell(v):
        return "REFUSED" if v is None else f"{v:,}"

    md = [f"# C.2.e female-wage / opportunity-cost frame probe — {stamp}", "",
          "Generated by `source/build/goldset/201_c2e_frame_probe.py`. Do not edit by hand; re-run.", "",
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
           "Priced as (baseline OR term) minus baseline. A large gain from a genuine C.2.e construct or",
           "its own treatment term means the baseline was under-built; a large gain from a generic word",
           "('economic development', 'GDP', 'female empowerment', 'income effect') is a free-OR inflater",
           "that annexes a neighbour literature (the development bundle, D.2.a, C.1.a), not a widening.", "",
           "| candidate | marginal gain |", "|---|---|"]
    for label, v in R.items():
        if label.startswith("gain: "):
            md.append(f"| {label[6:]} | {v if v is not None else 'REFUSED'} |")
    md += ["", "## Walls", "",
           "Each wall: overlap with our frame, the neighbour's own frame, and the overlap among",
           "identified records. C.1.a (income / wealth) is the load-bearing wall read from the other",
           "side: a wage shock moves income AND the price of time, so C.2.e must identify off a shock to",
           "the wage rate / price of time with non-labor income held constant. D.2.a (female empowerment)",
           "is the ideational sibling; the economic-development bundle is the excluded inflater; and FLFP",
           "as an OUTCOME of fertility (child penalty) is the reverse cell.", ""]
    (LOGDIR / f"c2e-frame-probe-{stamp}.md").write_text("\n".join(md) + "\n")
    print(f"\nwrote {LOGDIR}/c2e-frame-probe-{stamp}.{{json,md}}")
    if refusals:
        print(f"{len(refusals)} refusal(s) — those rows are missing, not zero", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
