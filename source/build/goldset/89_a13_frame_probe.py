#!/usr/bin/env python3
"""
89 — A.13 (TICK-096) stage-3 frame probe: confirm or refute that breastfeeding and lactational
amenorrhea is the smallest genuinely-unstarted candidate, and run the registered-construct
completeness test the A.6/A.3 episode made mandatory before any search spend.

Why this exists
---------------
A.13 was picked a priori as the smallest *unstarted* hypothesis, on the ground that it is a Bongaarts
proximate determinant (the postpartum-infecundability index C_i) and therefore a sibling of A.14
coital frequency, whose probe measured a production frame of 373 — the smallest to date and below the
whole cross-field scout set (D.2.c 1,134, D.1.d 1,720, A.20 1,968, A.19 2,414, B.2 4,475). But A.13
was never itself measured. TICK-087 (A.6) and TICK-088 (A.3) were both mis-ranked because their
selecting frames were priced wrong — A.6 omitted its own registered construct ("legitimation"); A.3
was charged a neighbour's channel terms and a free-standing OR. This probe applies the corrected rule
to A.13 *before* spending screen budget: price the frame against its OWN conjoined construct set, read
every wall from both sides, and count the homonym load inside the frame.

The registered-construct completeness test
------------------------------------------
Block C prices every noun the A.13 claim names (exclusive/duration of breastfeeding, suckling
intensity, night feeding, the proximate-determinants framework) as (baseline OR term) minus baseline.
A large marginal gain from a term that is genuinely A.13's means the baseline frame was under-built and
the term belongs in it (frame grows, but honestly). A large gain from a generic word conjoined to
nothing — bare "lactation" (dairy science), "weaning" (child nutrition), "prolactin" (endocrinology),
"parity" (physics/statistics) — is the free-OR inflater the A.3 park was built on, and is reported as
such, not folded into the frame.

The walls are read from both sides
-----------------------------------
Contraception/abortion (A.2-A.6 — natural vs. deliberate spacing), maternal nutrition / energy balance
(A.22 deprecated), postpartum abstinence / coital frequency (A.14 — the sibling C_i-adjacent channel),
infant/child mortality (A.1 — the REVERSE/confound wall: infant death ends nursing), fecundity capacity
(A.15/B.3), and LAM-as-method (A.5 — the applied boundary case) each get three numbers: overlap with
our frame, the neighbour's own frame, and the overlap among identified records — so the scope's routing
rules can carry counts, not adjectives.

Lessons this design honours (inherited from 405 / 52 / 89_a14)
--------------------------------------------------------------
  advance-the-baseline-when-accepting-terms / frame-growth-is-not-frame-gain — every candidate is
      priced as (baseline OR term) minus baseline, never by its own size.
  anchored-vocabulary-has-own-homonym — "lactation" is a dairy/animal-science term, "parity" a
      physics/statistics one, "prolactin" an endocrine-tumour one. Block I measures each inside our
      frame.
  wall-cut-on-wrong-axis — every wall is read as a share of our frame AND of theirs.
  validate-a-null-detector-on-positives — block A runs a written chapter's frame (C.2.c housing)
      first, so a broken counter shows up on a known-positive (405 recorded 205; 52 got 181).
  refusals-read-as-zeros — a failed request raises Refused and is reported REFUSED. Those rows are
      missing, not zero.

Outputs literature/search-logs/a13-frame-probe-<date>.{json,md}. Counting only; no records retained,
so this is cheap and re-runnable. Budget note: ~41 requests, within the shared ~100/day OpenAlex
allowance.

OpenAlex hazards honoured (see source/lib/openalex.py for the full list)
------------------------------------------------------------------------
  - a comma inside a filter VALUE is fatal -> no commas in any term
  - a phrase beginning "not" parses as boolean NOT -> none here; negation is by subtraction
  - hyphens fold and stopwords drop inside phrases -> handled by the resolver downstream
  - >5 boolean operators throttle to 1 req/sec on the keyless path -> PACE handles it
  - shell out to curl rather than urllib, per 405 (CA-bundle portability)
"""
import json, subprocess, sys, urllib.parse, datetime, pathlib, time

MAILTO = "shravanh@uchicago.edu"
BASE = "https://api.openalex.org/works"
LOGDIR = pathlib.Path("literature/search-logs")
CACHE = pathlib.Path("temp/a13-frame-probe-cache.json")


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

# Outcome axis: fertility and its birth-interval / amenorrhea-duration variants. A.13's proximate
# outcome is the length of postpartum infecundability (return of menses / ovulation) and the birth
# interval, translated to natural-fertility level; the distal outcome is the usual fertility set.
OUTCOME = ('("fertility" OR "childbearing" OR "birth rate" OR "total fertility rate" '
           'OR "childlessness" OR "natural fertility" OR "birth interval" OR "birth spacing" '
           'OR "interbirth interval" OR "fecundity" OR "return of menses" OR "resumption of menses" '
           'OR "resumption of ovulation")')

# The breastfeeding / lactational-amenorrhea topic block. NARROW is the tightest mechanism-first
# reading; A13 is the production union (core exposure + the amenorrhea mechanism).
A13_NARROW = ('("lactational amenorrhea" OR "lactational amenorrhoea" OR "postpartum amenorrhea" '
              'OR "postpartum amenorrhoea" OR "postpartum infecundability")')
A13 = ('("breastfeeding" OR "breast feeding" OR "lactational amenorrhea" OR "lactational amenorrhoea" '
       'OR "postpartum amenorrhea" OR "postpartum amenorrhoea" OR "postpartum infecundability" '
       'OR "lactational infecundability")')

IDENT = ('("instrumental variable" OR "difference-in-differences" OR "differences-in-differences" '
         'OR "natural experiment" OR "regression discontinuity" OR "randomized controlled trial" '
         'OR "randomised controlled trial" OR "event study" OR "synthetic control" OR "hazard model")')

# Block C. Every construct the A.13 claim names (the completeness test) plus the generic words that are
# the free-OR inflation risk. Priced as (baseline OR term) minus baseline.
OWN_CANDIDATES = [
    "exclusive breastfeeding", "breastfeeding duration", "nursing", "suckling", "night feeding",
    "proximate determinants", "Bongaarts", "lactational amenorrhea method",
    # generic / homonym inflaters to catch free-OR behaviour:
    "lactation", "weaning", "prolactin", "parity",
]

# Outcome-level calibration.
LEVELS = [
    ("realized / period fertility", '("total fertility rate" OR "birth rate" OR "completed fertility")'),
    ("birth interval / spacing", '("birth interval" OR "birth spacing" OR "interbirth interval")'),
    ("amenorrhea duration / return of menses", '("return of menses" OR "resumption of ovulation" OR "duration of amenorrhea")'),
]

# Six walls, each read from both sides and among identified records.
WALLS = [
    ("A.2-A.6", "contraception / abortion -- natural vs. deliberate spacing (the explicit 'independent of contraception' wall)", "several drafted",
     '("contraception" OR "contraceptive" OR "family planning" OR "oral contraceptive" OR "intrauterine device")'),
    ("A.22", "maternal nutrition / energy balance -- the critical-fat pathway to amenorrhea (DEPRECATED, but physiologically entangled)", "deprecated",
     '("maternal nutrition" OR "energy balance" OR "body fat" OR "nutritional status" OR "undernutrition")'),
    ("A.14", "postpartum abstinence / coital frequency -- the sibling C_i-adjacent behavioural channel", "drafted (branch 091)",
     '("postpartum abstinence" OR "coital frequency" OR "sexual abstinence" OR "frequency of intercourse")'),
    ("A.1", "infant / child mortality -- the REVERSE/confound wall (infant death terminates nursing)", "unstarted",
     '("infant mortality" OR "child mortality" OR "neonatal mortality" OR "infant death")'),
    ("A.15/B.3", "fecundity capacity -- maternal age / sterilising infection (not behavioural spacing)", "unstarted",
     '("advanced maternal age" OR "ovarian reserve" OR "tubal infertility" OR "primary sterility")'),
    ("A.5/LAM", "lactational amenorrhea method / family-planning programs -- the applied boundary case", "unstarted",
     '("lactational amenorrhea method" OR "contraceptive efficacy" OR "Bellagio consensus" OR "method of family planning")'),
]

HOMONYMS = [
    ("lactation in dairy / animal science",
     '("dairy cattle" OR "dairy cow" OR "milk yield" OR "calving interval" OR "litter size")'),
    ("prolactin in endocrine oncology",
     '("prolactinoma" OR "pituitary adenoma" OR "macroprolactinemia")'),
    ("infant-health outcomes (should be excluded by OUTCOME)",
     '("infant growth" OR "child nutrition" OR "breast milk composition" OR "cognitive development")'),
    ("parity / weaning in other senses",
     '("parity bit" OR "parity violation" OR "ventilator weaning" OR "weaning off")'),
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
    q("A.13 narrow frame (lactational amenorrhea AND fertility+interval)",
      AND(A13_NARROW, OUTCOME))
    frame = q("A.13 production frame (topic union AND outcome)", AND(A13, OUTCOME))
    q("A.13 topic block with no outcome restriction", A13)

    print("C — completeness test: pricing every registered construct", flush=True)
    for term in OWN_CANDIDATES:
        cand = A13[:-1] + f' OR "{term}")'
        n = q(f"own + {term}", AND(cand, OUTCOME))
        if n is not None and frame is not None:
            R[f"gain: own + {term}"] = n - frame
    if frame is not None:
        allo = A13[:-1] + "".join(f' OR "{t}"' for t in OWN_CANDIDATES) + ")"
        n = q("A.13 block widened by ALL registered constructs", AND(allo, OUTCOME))
        if n is not None:
            R["gain: own widened by ALL"] = n - frame

    print("E — calibrating the outcome axis", flush=True)
    for label, block in LEVELS:
        q(f"level: {label}", AND(A13, block))

    print("F — identification markers inside the frame", flush=True)
    q("frame AND identified-design markers", AND(A13, OUTCOME, IDENT))

    print("H — the six walls, read from both sides", flush=True)
    for code, name, status, block in WALLS:
        q(f"wall {code} overlap with our frame", AND(A13, OUTCOME, block))
        q(f"wall {code} neighbour frame", AND(block, OUTCOME))
        q(f"wall {code} overlap AND identified", AND(A13, OUTCOME, block, IDENT))

    print("I — homonym readings inside our own frame", flush=True)
    for label, block in HOMONYMS:
        q(f"homonym: {label}", AND(A13, OUTCOME, block))

    stamp = datetime.date.today().isoformat()
    LOGDIR.mkdir(parents=True, exist_ok=True)
    payload = {"generated": stamp, "script": "source/build/goldset/89_a13_frame_probe.py",
               "api_key_present": bool(API_KEY), "counts": R,
               "refusals": [{"label": l, "error": e} for l, e in refusals]}
    (LOGDIR / f"a13-frame-probe-{stamp}.json").write_text(json.dumps(payload, indent=1))

    def cell(v):
        return "REFUSED" if v is None else f"{v:,}"

    md = [f"# A.13 breastfeeding / lactational-amenorrhea frame probe — {stamp}", "",
          "Generated by `source/build/goldset/89_a13_frame_probe.py`. Do not edit by hand;",
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
           "from a genuine A.13 construct means the baseline was under-built; a large gain from a",
           "generic word ('lactation', 'weaning', 'prolactin', 'parity') is a free-OR inflater, not",
           "a widening.", "", "| candidate | marginal gain |", "|---|---|"]
    for label, v in R.items():
        if label.startswith("gain: "):
            md.append(f"| {label[6:]} | {v if v is not None else 'REFUSED'} |")
    md += ["", "## Walls", "",
           "Each wall: overlap with our frame, the neighbour's own frame, and the overlap among",
           "identified records. Routing is defensible where the overlap is a small share of our",
           "frame and the identified overlap is near zero.", ""]
    (LOGDIR / f"a13-frame-probe-{stamp}.md").write_text("\n".join(md) + "\n")
    print(f"\nwrote {LOGDIR}/a13-frame-probe-{stamp}.{{json,md}}")
    if refusals:
        print(f"{len(refusals)} refusal(s) — those rows are missing, not zero", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
