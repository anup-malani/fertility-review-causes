#!/usr/bin/env python3
"""
89 (d2c) — D.2.c (TICK-092) stage-3 frame probe: confirm or refute that son preference and gender-biased
fertility norms is the smallest genuinely-unstarted candidate, and run the registered-construct
completeness test the A.6/A.3 episode made mandatory before any search spend.

Why this exists
---------------
D.2.c was picked as the smallest *unstarted* hypothesis on an extended scouting count (production frame
= 1,134, below the ~1,808 bar and below every other unstarted candidate probed: D.1.d 1,720; A.20 1,968;
A.19 2,414; B.2 4,475; A.13 5,079). TICK-087 (A.6) and TICK-088 (A.3) were both mis-ranked because their
selecting frames were priced wrong — A.6 omitted its own registered construct ("legitimation"); A.3 was
charged a neighbour's channel terms and a free-standing OR. This probe applies the corrected rule to
D.2.c *before* spending screen budget: price the frame against its OWN conjoined construct set, read
every wall from both sides, and count the homonym load inside the frame.

The son-preference-specific hazard
----------------------------------
The topic is entangled with the sex-ratio (A.10) and sex-selective-abortion (A.4) literatures, and the
word "sex ratio" appears on both sides of Wall 1. The completeness test must show that the honest D.2.c
frame is a preference-and-differential-stopping frame, and that folding a free-standing "sex ratio" OR
would annex A.10's adult-sex-ratio marriage-market literature rather than widen D.2.c. That is exactly
the free-OR inflation the A.3 park was built on.

The registered-construct completeness test
------------------------------------------
Block C prices every noun the D.2.c claim names (son preference, differential stopping / sex-composition-
conditional continuation, sex-selective abortion, skewed sex ratio at birth) as (baseline OR term) minus
baseline. A large marginal gain from a term that is genuinely D.2.c's means the baseline frame was
under-built and the term belongs in it (frame grows, but honestly). A large gain from a generic word
conjoined to nothing -- "preference", "gender", "sex ratio", "son" -- is the free-OR inflater, reported
as such, not folded into the frame.

The walls are read from both sides
-----------------------------------
Adult sex ratio / marriage market (A.10), abortion / contraception (A.4/A.2), parity stopping (A.8),
old-age security (C.3.c), gender equity (D.2.a), and child mortality (A.1) each get three numbers:
overlap with our frame, the neighbour's own frame, and the overlap among identified records -- so the
scope's routing rules can carry counts, not adjectives.

Lessons this design honours (inherited from 89_a14 / 405 / 52)
--------------------------------------------------------------
  advance-the-baseline-when-accepting-terms / frame-growth-is-not-frame-gain -- every candidate is
      priced as (baseline OR term) minus baseline, never by its own size.
  anchored-vocabulary-has-own-homonym -- "son" is a surname/given-name token, "sex"/"gender" biology and
      grammar terms, "preference" an economics term. Block I measures each inside our frame.
  wall-cut-on-wrong-axis -- every wall is read as a share of our frame AND of theirs.
  validate-a-null-detector-on-positives -- block A runs a written chapter's frame (C.2.c housing)
      first, so a broken counter shows up on a known-positive (405 recorded 205; 52 got 181).
  refusals-read-as-zeros -- a failed request raises Refused and is reported REFUSED. Those rows are
      missing, not zero.

Outputs literature/search-logs/d2c-frame-probe-<date>.{json,md}. Counting only; no records retained.

OpenAlex hazards honoured (see source/lib/openalex.py)
------------------------------------------------------
  - a comma inside a filter VALUE is fatal -> no commas in any term
  - a phrase beginning "not" parses as boolean NOT -> none here; negation is by subtraction
  - hyphens fold and stopwords drop inside phrases -> handled by the anchored vocabulary
  - >5 boolean operators throttle on the keyless path -> PACE handles it; API key present
  - shell out to curl rather than urllib, per 405 (CA-bundle portability)
"""
import json, subprocess, sys, urllib.parse, datetime, pathlib, time

MAILTO = "shravanh@uchicago.edu"
BASE = "https://api.openalex.org/works"
LOGDIR = pathlib.Path("literature/search-logs")
CACHE = pathlib.Path("temp/d2c-frame-probe-cache.json")


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

# Outcome axis: fertility only (same as the scout FERT axis, for comparability with the 1,134 scout).
# The sex-ratio-at-birth "expression" outcome is deliberately NOT free in this axis -- a free "sex ratio"
# OR would annex A.10. It enters only conjoined inside the topic union where a son-preference sense fixes
# it, and is priced separately in the completeness test.
OUTCOME = ('("fertility" OR "childbearing" OR "birth rate" OR "total fertility rate" '
           'OR "childlessness" OR "fecundity" OR "time to pregnancy" OR "subfertility" '
           'OR "infertility")')

# The son-preference topic block. NARROW is the tightest reading; D2C is the production union.
D2C_NARROW = '("son preference" OR "preference for sons" OR "desire for sons" OR "boy preference")'
D2C = ('("son preference" OR "preference for sons" OR "desire for sons" OR "boy preference" '
       'OR "sex preference" OR "gender preference" OR "sex-selective abortion" OR "sex selection" '
       'OR "prenatal sex selection" OR "differential stopping")')

IDENT = ('("instrumental variable" OR "difference-in-differences" OR "differences-in-differences" '
         'OR "natural experiment" OR "regression discontinuity" OR "randomized controlled trial" '
         'OR "randomised controlled trial" OR "event study" OR "synthetic control")')

# Block C. Every construct the D.2.c claim names (the completeness test) plus the generic words that are
# the free-OR inflation risk. Priced as (baseline OR term) minus baseline.
OWN_CANDIDATES = [
    "sex composition", "sex ratio at birth", "stopping behavior", "stopping behaviour",
    "male preference", "sex-selective", "prenatal diagnosis", "amniocentesis",
    # generic / homonym-heavy inflaters to catch free-OR behaviour:
    "sex ratio", "preference", "gender", "son",
]

# Outcome-level calibration.
LEVELS = [
    ("realized / period fertility", '("total fertility rate" OR "birth rate" OR "completed fertility")'),
    ("parity progression / stopping", '("parity progression" OR "number of children" OR "continued childbearing")'),
    ("sex ratio at birth (the substitution expression)", '("sex ratio at birth" OR "sex ratio imbalance")'),
]

# Six walls, each read from both sides and among identified records.
WALLS = [
    ("A.10", "adult sex ratio / marriage market -- the load-bearing 'sex ratio' wall (adult imbalance as exposure, not sex ratio at birth as expression)", "search-scope drafted (TICK-054, parked)",
     '("marriage market" OR "marriage squeeze" OR "adult sex ratio" OR "marriageable men" OR "sex ratio imbalance")'),
    ("A.4/A.2", "abortion / contraception -- general access removing unwanted births of any sex", "several drafted",
     '("induced abortion" OR "abortion access" OR "contraception" OR "contraceptive" OR "family planning")'),
    ("A.8", "parity-specific stopping / spacing -- sex-indifferent target-number stopping", "unstarted",
     '("parity progression" OR "family limitation" OR "birth spacing" OR "fertility control")'),
    ("C.3.c", "old-age security -- the economic root of wanting sons (pensions vs son support)", "done (OAS pilot)",
     '("old-age security" OR "pension" OR "old age support" OR "intergenerational transfers")'),
    ("D.2.a", "female empowerment / gender equity -- egalitarian norms that lower fertility broadly", "unstarted",
     '("female autonomy" OR "gender equity" OR "women empowerment" OR "female education" OR "gender equality")'),
    ("A.1", "child mortality / replacement -- continuing until a surviving son", "unstarted",
     '("child mortality" OR "infant mortality" OR "child survival" OR "replacement effect")'),
]

HOMONYMS = [
    ("son as surname / given name",
     '("Johnson" OR "Robinson" OR "Anderson" OR "prodigal son")'),
    ("sex / gender in biology and grammar",
     '("grammatical gender" OR "sex determination" OR "sexual dimorphism" OR "gender identity")'),
    ("preference in economics / consumer choice",
     '("consumer preference" OR "revealed preference" OR "time preference" OR "risk preference")'),
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
    q("control: C.2.c housing frame (a written chapter; 405 recorded 205, 52 got 181)",
      AND('("house price" OR "housing cost" OR "house prices")',
          '("fertility" OR "childbearing" OR "birth rate" OR "total fertility rate" OR "childlessness")'))
    q("D.2.c narrow frame (son-preference core AND fertility)",
      AND(D2C_NARROW, OUTCOME))
    frame = q("D.2.c production frame (topic union AND outcome)", AND(D2C, OUTCOME))
    q("D.2.c topic block with no outcome restriction", D2C)

    print("C — completeness test: pricing every registered construct", flush=True)
    for term in OWN_CANDIDATES:
        cand = D2C[:-1] + f' OR "{term}")'
        n = q(f"own + {term}", AND(cand, OUTCOME))
        if n is not None and frame is not None:
            R[f"gain: own + {term}"] = n - frame
    if frame is not None:
        allo = D2C[:-1] + "".join(f' OR "{t}"' for t in OWN_CANDIDATES) + ")"
        n = q("D.2.c block widened by ALL registered constructs", AND(allo, OUTCOME))
        if n is not None:
            R["gain: own widened by ALL"] = n - frame

    print("E — calibrating the outcome axis", flush=True)
    for label, block in LEVELS:
        q(f"level: {label}", AND(D2C, block))

    print("F — identification markers inside the frame", flush=True)
    q("frame AND identified-design markers", AND(D2C, OUTCOME, IDENT))

    print("H — the six walls, read from both sides", flush=True)
    for code, name, status, block in WALLS:
        q(f"wall {code} overlap with our frame", AND(D2C, OUTCOME, block))
        q(f"wall {code} neighbour frame", AND(block, OUTCOME))
        q(f"wall {code} overlap AND identified", AND(D2C, OUTCOME, block, IDENT))

    print("I — homonym readings inside our own frame", flush=True)
    for label, block in HOMONYMS:
        q(f"homonym: {label}", AND(D2C, OUTCOME, block))

    stamp = datetime.date.today().isoformat()
    LOGDIR.mkdir(parents=True, exist_ok=True)
    payload = {"generated": stamp, "script": "source/build/goldset/89_d2c_frame_probe.py",
               "api_key_present": bool(API_KEY), "counts": R,
               "refusals": [{"label": l, "error": e} for l, e in refusals]}
    (LOGDIR / f"d2c-frame-probe-{stamp}.json").write_text(json.dumps(payload, indent=1))

    def cell(v):
        return "REFUSED" if v is None else f"{v:,}"

    md = [f"# D.2.c son-preference frame probe — {stamp}", "",
          "Generated by `source/build/goldset/89_d2c_frame_probe.py`. Do not edit by hand;",
          "re-run the script.", "",
          "These are OpenAlex `title_and_abstract.search` record counts. They size a *retrieval",
          "frame* and its overlaps. **No production query has been run, no anchor resolved, and no",
          "record screened.** A count is not an evidence base, and a study can estimate this",
          "chapter's parameter without carrying any of these phrases in its abstract.", ""]
    if refusals:
        md += [f"**{len(refusals)} request(s) REFUSED.** Those rows are missing, not zero.", ""]
    md += ["| measurement | n |", "|---|---|"]
    for label, v in R.items():
        if not label.startswith("gain: "):
            md.append(f"| {label} | {cell(v)} |")
    md += ["", "## Marginal gain of candidate terms", "",
           "Priced as (baseline OR term) minus baseline, never by the term's own size. A large gain",
           "from a genuine D.2.c construct means the baseline was under-built; a large gain from a",
           "generic word ('sex ratio', 'preference', 'gender', 'son') is a free-OR inflater that annexes",
           "a neighbour literature (A.10 for 'sex ratio'), not a widening.", "",
           "| candidate | marginal gain |", "|---|---|"]
    for label, v in R.items():
        if label.startswith("gain: "):
            md.append(f"| {label[6:]} | {v if v is not None else 'REFUSED'} |")
    md += ["", "## Walls", "",
           "Each wall: overlap with our frame, the neighbour's own frame, and the overlap among",
           "identified records. Routing is defensible where the overlap is a small share of our",
           "frame and the identified overlap is near zero. Wall A.10 is load-bearing: the 'sex ratio'",
           "term is shared, so the overlap number here decides whether the frame is clean.", ""]
    (LOGDIR / f"d2c-frame-probe-{stamp}.md").write_text("\n".join(md) + "\n")
    print(f"\nwrote {LOGDIR}/d2c-frame-probe-{stamp}.{{json,md}}")
    if refusals:
        print(f"{len(refusals)} refusal(s) — those rows are missing, not zero", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
