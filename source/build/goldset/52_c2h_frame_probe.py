#!/usr/bin/env python3
"""
52 — C.2.h (TICK-090) stage-3 frame probe: confirm or refute that digital-leisure substitution is
the smallest genuinely-unstarted candidate, and run the registered-construct completeness test the
A.6/A.3 episode made mandatory before any search spend.

Why this exists
---------------
C.2.h was picked as the smallest *unstarted* hypothesis on a reasoned prior (a NEW-v5, SDT-only
entry anchored on one identified design, Myers-Hooper w35310), not a measurement. TICK-087 (A.6) and
TICK-088 (A.3) were both mis-ranked because their selecting frames were priced wrong — A.6 omitted
its own registered construct ("legitimation"); A.3 was charged a neighbour's channel terms and a
free-standing OR. This probe applies the corrected rule to C.2.h *before* spending screen budget:
price the frame against its OWN conjoined construct set, read every wall from both sides, and count
the homonym load inside the frame.

The registered-construct completeness test
------------------------------------------
Block C prices every noun the C.2.h claim names (smartphone, social media, streaming, gaming,
pornography, screen time, the time/attention budget) as (baseline OR term) minus baseline. A large
marginal gain from a term that is genuinely C.2.h's means the baseline frame was under-built and the
term belongs in it (frame grows, but honestly). A large gain from a generic word conjoined to
nothing -- "substitution", "attention" -- is the free-OR inflater the A.3 park was built on, and is
reported as such, not folded into the frame.

The walls are read from both sides
-----------------------------------
C.2.e (wages), A.24 (dating apps), A.14 (coital frequency), D.1.a (values), D.3.a (mental health)
each get three numbers: overlap with our frame, the neighbour's own frame, and the overlap among
identified records -- so the scope's routing rules can carry counts, not adjectives.

Lessons this design honours (inherited from 405)
-------------------------------------------------
  advance-the-baseline-when-accepting-terms / frame-growth-is-not-frame-gain -- every candidate is
      priced as (baseline OR term) minus baseline, never by its own size.
  anchored-vocabulary-has-own-homonym -- "substitution" is a chemistry/econometrics term,
      "attention" a machine-learning one, "screen(ing)" a medical one, "gaming" a game-theory /
      gambling one. Block I measures each inside our frame.
  wall-cut-on-wrong-axis -- every wall is read as a share of our frame AND of theirs.
  validate-a-null-detector-on-positives -- block A runs a written chapter's frame (C.2.c housing)
      first, so a broken counter shows up on a known-positive rather than silently on C.2.h.
  refusals-read-as-zeros -- a failed request raises Refused and is reported REFUSED. Those rows are
      missing, not zero.

Outputs literature/search-logs/c2h-frame-probe-<date>.{json,md}. Counting only; no records retained,
so this is cheap and re-runnable. Budget note: ~43 requests, within the shared ~100/day OpenAlex
allowance.

OpenAlex hazards honoured (see source/lib/openalex.py for the full list)
------------------------------------------------------------------------
  - a comma inside a filter VALUE is fatal -> no commas in any term
  - a phrase beginning "not" parses as boolean NOT -> none here; negation is by subtraction
  - hyphens fold and stopwords drop inside phrases -> a drop test removes every spelling together
  - >5 boolean operators throttle to 1 req/sec on the keyless path -> PACE handles it
  - shell out to curl rather than urllib, per 405 (CA-bundle portability)
"""
import json, subprocess, sys, urllib.parse, datetime, pathlib, time

MAILTO = "shravanh@uchicago.edu"
BASE = "https://api.openalex.org/works"
LOGDIR = pathlib.Path("literature/search-logs")
CACHE = pathlib.Path("temp/c2h-frame-probe-cache.json")


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

# Outcome axis: fertility first, with a partnering-inclusive wide variant (C.2.h's proximate
# outcomes are union formation and coital frequency as well as births).
OUTCOME = '("fertility" OR "childbearing" OR "birth rate" OR "total fertility rate" OR "childlessness")'
OUTCOME_WIDE = ('("fertility" OR "childbearing" OR "birth rate" OR "total fertility rate" '
                'OR "childlessness" OR "union formation" OR "marriage rate" OR "cohabitation")')

# The digital-leisure topic block. NARROW is the tightest reading; C2H is the production union.
C2H_NARROW = '("smartphone" OR "social media" OR "screen time" OR "online pornography")'
C2H = ('("smartphone" OR "social media" OR "screen time" OR "online pornography" '
       'OR "mobile internet" OR "video game" OR "digital media" OR "broadband internet")')

IDENT = ('("instrumental variable" OR "difference-in-differences" OR "differences-in-differences" '
         'OR "natural experiment" OR "regression discontinuity" OR "randomized controlled trial" '
         'OR "randomised controlled trial" OR "event study" OR "synthetic control")')

# Block C. Every construct the C.2.h claim names (the completeness test) plus the two generic design
# words that are the free-OR inflation risk. Priced as (baseline OR term) minus baseline.
OWN_CANDIDATES = [
    "smartphone", "social media", "screen time", "pornography", "video game", "gaming",
    "streaming", "internet access", "digital leisure", "time displacement",
    "substitution", "attention",
]

# Outcome-level calibration.
LEVELS = [
    ("realized fertility", '("total fertility rate" OR "birth rate" OR "completed fertility")'),
    ("partnering / union formation", '("union formation" OR "cohabitation" OR "marriage rate")'),
    ("coital frequency", '("coital frequency" OR "sexual frequency" OR "frequency of intercourse")'),
]

# Five walls, each read from both sides and among identified records.
WALLS = [
    ("C.2.e", "female wage / opportunity cost of time -- drafted on branch 081 neighbourhood", "drafted-adjacent",
     '("female wage" OR "opportunity cost of time" OR "female labor force participation" '
     'OR "female labour force participation")'),
    ("A.24", "dating apps and union-formation friction -- same device", "drafted (branch 071)",
     '("dating app" OR "online dating" OR "dating application")'),
    ("A.14", "coital frequency and fecundability -- the proximate-determinant identity", "unstarted",
     '("coital frequency" OR "sexual frequency" OR "frequency of intercourse" OR "fecundability")'),
    ("D.1.a", "postmaterialism / individualism / secularisation -- the value shift", "drafted (branch 062)",
     '("secularization" OR "secularisation" OR "individualism" OR "postmaterialism" OR "value change")'),
    ("D.3.a", "mental health and anxiety epidemic -- the clinical pathway", "unstarted",
     '("anxiety" OR "depression" OR "mental health" OR "mood disorder")'),
]

HOMONYMS = [
    ("substitution in chemistry / econometrics",
     '("substitution reaction" OR "import substitution" OR "elasticity of substitution" OR "nucleophilic")'),
    ("attention in machine learning / neuroscience",
     '("attention mechanism" OR "neural network" OR "transformer model" OR "visual attention")'),
    ("screen or screening in medicine",
     '("cancer screening" OR "prenatal screening" OR "screening test" OR "sunscreen")'),
    ("gaming in game theory / gambling",
     '("game theory" OR "gambling" OR "casino" OR "problem gambling")'),
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
    q("control: C.2.c housing frame (a written chapter; 405 recorded 205)",
      AND('("house price" OR "housing cost" OR "house prices")', OUTCOME_WIDE))
    q("C.2.h narrow frame (smartphone/social media/screen time/porn AND fertility)",
      AND(C2H_NARROW, OUTCOME))
    frame = q("C.2.h production frame (topic union AND outcome-wide)", AND(C2H, OUTCOME_WIDE))
    q("C.2.h topic block with no outcome restriction", C2H)

    print("C — completeness test: pricing every registered construct", flush=True)
    for term in OWN_CANDIDATES:
        cand = C2H[:-1] + f' OR "{term}")'
        n = q(f"own + {term}", AND(cand, OUTCOME_WIDE))
        if n is not None and frame is not None:
            R[f"gain: own + {term}"] = n - frame
    if frame is not None:
        allo = C2H[:-1] + "".join(f' OR "{t}"' for t in OWN_CANDIDATES) + ")"
        n = q("C.2.h block widened by ALL registered constructs", AND(allo, OUTCOME_WIDE))
        if n is not None:
            R["gain: own widened by ALL"] = n - frame

    print("E — calibrating the outcome axis", flush=True)
    q("outcome narrow instead of wide", AND(C2H, OUTCOME))
    for extra in ["coital frequency", "sexual frequency", "births"]:
        cand = OUTCOME_WIDE[:-1] + f' OR "{extra}")'
        n = q(f"outcome + {extra}", AND(C2H, cand))
        if n is not None and frame is not None:
            R[f"gain: outcome + {extra}"] = n - frame

    print("F — identification markers inside the frame", flush=True)
    q("frame AND identified-design markers", AND(C2H, OUTCOME_WIDE, IDENT))

    print("G — outcome level", flush=True)
    for label, block in LEVELS:
        q(f"level: {label}", AND(C2H, OUTCOME_WIDE, block))

    print("H — the five walls, read from both sides", flush=True)
    for code, name, status, block in WALLS:
        q(f"wall {code} overlap with our frame", AND(C2H, OUTCOME_WIDE, block))
        q(f"wall {code} neighbour frame", AND(block, OUTCOME_WIDE))
        q(f"wall {code} overlap AND identified", AND(C2H, OUTCOME_WIDE, block, IDENT))

    print("I — homonym readings inside our own frame", flush=True)
    for label, block in HOMONYMS:
        q(f"homonym: {label}", AND(C2H, OUTCOME_WIDE, block))

    stamp = datetime.date.today().isoformat()
    LOGDIR.mkdir(parents=True, exist_ok=True)
    payload = {"generated": stamp, "script": "source/build/goldset/52_c2h_frame_probe.py",
               "api_key_present": bool(API_KEY), "counts": R,
               "refusals": [{"label": l, "error": e} for l, e in refusals]}
    (LOGDIR / f"c2h-frame-probe-{stamp}.json").write_text(json.dumps(payload, indent=1))

    def cell(v):
        return "REFUSED" if v is None else f"{v:,}"

    md = [f"# C.2.h digital-leisure frame probe — {stamp}", "",
          "Generated by `source/build/goldset/52_c2h_frame_probe.py`. Do not edit by hand;",
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
           "from a genuine C.2.h construct means the baseline was under-built; a large gain from a",
           "generic word ('substitution', 'attention') is a free-OR inflater, not a widening.",
           "", "| candidate | marginal gain |", "|---|---|"]
    for label, v in R.items():
        if label.startswith("gain: "):
            md.append(f"| {label[6:]} | {v if v is not None else 'REFUSED'} |")
    md += ["", "## Walls", "",
           "Each wall: overlap with our frame, the neighbour's own frame, and the overlap among",
           "identified records. Routing is defensible where the overlap is a small share of our",
           "frame and the identified overlap is near zero.", ""]
    (LOGDIR / f"c2h-frame-probe-{stamp}.md").write_text("\n".join(md) + "\n")
    print(f"\nwrote {LOGDIR}/c2h-frame-probe-{stamp}.{{json,md}}")
    if refusals:
        print(f"{len(refusals)} refusal(s) — those rows are missing, not zero", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
