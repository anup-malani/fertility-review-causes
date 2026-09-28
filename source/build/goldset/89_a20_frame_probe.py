#!/usr/bin/env python3
"""
89 (a20) — A.20 (TICK-094) stage-3 frame probe: confirm or refute that cultural diffusion mechanisms is
the next-smallest genuinely-unstarted candidate, and run the registered-construct completeness test the
A.6/A.3 episode made mandatory before any search spend.

Why this exists
---------------
A.20 was picked as the next-smallest *unstarted* hypothesis on TICK-092/093's extended scouting count
(production frame = ~1,968, next after D.1.d's 1,720 and above the ~1,808 bar by a hair: A.19 2,414;
B.2 4,475). But that scout was *partitioned* and never priced A.20's frame against its OWN conjoined
construct set. TICK-087 (A.6) and TICK-088 (A.3) were both mis-ranked because their selecting frames were
priced wrong — A.6 omitted its own registered construct ("legitimation"); A.3 was charged a neighbour's
channel terms and a free-standing OR. This probe applies the corrected rule to A.20 *before* spending
screen budget: price the frame against its OWN conjoined construct set, read every wall from both sides,
and count the homonym load inside the frame.

The cultural-diffusion-specific hazard
--------------------------------------
A.20 is a mechanism/channel hypothesis, so by construction it overlaps every *content* hypothesis that
diffuses. The load-bearing wall is A.3 (Diffusion and Social-Learning of Fertility Control, drafted as
TICK-088): A.20 and A.3 share the word "diffusion" and their seminal set. The redundancy worry is real
and this probe is its test. The prior that resolves most of it: A.3's own Wall 1 (resolved 2026-09-18)
routed the cleanest identified estimates in the neighbourhood — the Brazil soap-opera (La Ferrara, Chong &
Duryea 2012) and India cable-TV (Jensen & Oster 2009) quasi-experiments — TO A.20, because their treatment
is content-agnostic signal coverage of entertainment, not a family-planning message. Those are A.20's
registered seminals. So the completeness test must show that (a) the honest A.20 frame is a *channels*
frame (mass media, social networks, peer/network effects, community boundaries), and that (b) folding a
free-standing "diffusion", "network", "media", or "television" OR would annex a neighbour or a homonym
literature (physics diffusion, social-network *methodology*, generic media/TV research) rather than widen
A.20. That is exactly the free-OR inflation the A.3 park was built on.

The registered-construct completeness test
------------------------------------------
Block C prices every noun the A.20 claim names (social networks, mass media / radio / TV / soap operas,
linguistic/cultural community boundaries, diffusion of innovations / social contagion) as
(baseline OR term) minus baseline. A large marginal gain from a term that is genuinely A.20's means the
baseline frame was under-built and the term belongs in it (frame grows, but honestly). A large gain from a
generic word conjoined to nothing -- "diffusion", "network", "media", "television", "radio" -- is the
free-OR inflater, reported as such, not folded into the frame.

The walls are read from both sides
-----------------------------------
A.3 (fertility-control CONTENT, LOAD-BEARING), A.19 (vertical transmission), A.2 (contraceptive
TECHNOLOGY), A.5 (family-planning program MESSAGE), D.1.a (secular value-shift content), and D.1.d
(nationalist content) each get three numbers: overlap with our frame, the neighbour's own frame, and the
overlap among identified records -- so the scope's routing rules can carry counts, not adjectives. The
A.3 wall is the one that decides whether A.20 is a distinct chapter or a re-run: the test is whether the
*identified* overlap is thin (A.20's identified core = the media-reach/network designs A.3 excluded).

Lessons this design honours (inherited from 89_d1d / 89_d2c / 89_a14 / 405 / 52)
-------------------------------------------------------------------------------
  advance-the-baseline-when-accepting-terms / frame-growth-is-not-frame-gain -- every candidate is
      priced as (baseline OR term) minus baseline, never by its own size.
  anchored-vocabulary-has-own-homonym -- "diffusion" is a physics/technology/marketing token, "network" a
      social-network-analysis-methodology one, "media" a generic-communications one. Block I measures each
      inside our frame.
  wall-cut-on-wrong-axis -- every wall is read as a share of our frame AND of theirs.
  validate-a-null-detector-on-positives -- block A runs a written chapter's frame (C.2.c housing) first,
      so a broken counter shows up on a known-positive (405 recorded 205; 52 got 181; 89_d2c 170;
      89_d1d 166).
  refusals-read-as-zeros -- a failed request raises Refused and is reported REFUSED. Those rows are
      missing, not zero.

Outputs literature/search-logs/a20-frame-probe-<date>.{json,md}. Counting only; no records retained.

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
CACHE = pathlib.Path("temp/a20-frame-probe-cache.json")


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

# Outcome axis: fertility only, IDENTICAL to 89_d1d / 89_d2c, so the control-housing frame reproduces
# (~166-205) and the A.20 production frame is comparable across probes.
OUTCOME = ('("fertility" OR "childbearing" OR "birth rate" OR "total fertility rate" '
           'OR "childlessness" OR "fecundity" OR "time to pregnancy" OR "subfertility" '
           'OR "infertility")')

# The cultural-diffusion-channel topic block. NARROW is the tightest reading; A20 is the production union
# of the genuinely channel-specific phrases only. The homonym-heavy words (diffusion, network, media,
# television, radio) are priced in the completeness test (block C) and enter the frame only if they earn
# it there. "social network" and "social learning" are borderline (SNA methodology; shared with A.3) and
# are priced rather than assumed.
A20_NARROW = '("diffusion of innovations" OR "social contagion")'
A20 = ('("diffusion of innovations" OR "social contagion" OR "social interaction" '
       'OR "social influence" OR "peer effects" OR "peer influence" OR "network effects" '
       'OR "mass media" OR "media exposure" OR "telenovela" OR "soap opera" OR "cable television")')

IDENT = ('("instrumental variable" OR "difference-in-differences" OR "differences-in-differences" '
         'OR "natural experiment" OR "regression discontinuity" OR "randomized controlled trial" '
         'OR "randomised controlled trial" OR "event study" OR "synthetic control")')

# Block C. Every construct the A.20 claim names (the completeness test) plus the generic words that are
# the free-OR inflation risk. Priced as (baseline OR term) minus baseline.
OWN_CANDIDATES = [
    # genuine A.20 constructs to test for inclusion:
    "social network", "social learning", "linguistic boundary", "language group",
    "cultural boundary", "spatial diffusion",
    # generic / homonym-heavy inflaters to catch free-OR behaviour:
    "diffusion", "network", "media", "television", "radio", "communication", "social media",
]

# Outcome-level calibration.
LEVELS = [
    ("realized / period fertility", '("total fertility rate" OR "birth rate" OR "completed fertility")'),
    ("contraceptive adoption / uptake", '("contraceptive use" OR "contraceptive adoption" OR "family planning use")'),
    ("pace / geography of change", '("fertility transition" OR "fertility decline" OR "timing of decline")'),
]

# Six walls, each read from both sides and among identified records.
WALLS = [
    ("A.3", "diffusion of fertility-CONTROL knowledge -- the CONTENT that rides our channel (LOAD-BEARING)", "done (TICK-088, unmerged)",
     '("fertility control" OR "family limitation" OR "birth control" OR "contraceptive knowledge")'),
    ("A.19", "intergenerational transmission -- vertical (parent-child), not horizontal channels", "unstarted",
     '("intergenerational transmission" OR "vertical transmission" OR "transmission of fertility" OR "parental fertility")'),
    ("A.2", "contraceptive TECHNOLOGY -- spread of the physical method, not the norm", "done/adjacent",
     '("oral contraceptive" OR "contraceptive technology" OR "intrauterine device" OR "sterilization")'),
    ("A.5", "family-planning PROGRAM message -- deliberate IEC content, not content-agnostic reach", "adjacent",
     '("family planning program" OR "family planning campaign" OR "outreach worker" OR "information education communication")'),
    ("D.1.a", "postmaterialism / secularization -- the value-shift CONTENT our channel may carry", "branch 062 (unmerged)",
     '("secularization" OR "secularisation" OR "individualism" OR "postmaterialism" OR "value change")'),
    ("D.1.d", "nationalist / pronatalist ideology -- the state-framing CONTENT our channel may carry", "done (TICK-093, unmerged)",
     '("pronatalism" OR "pronatalist" OR "demographic nationalism" OR "population campaign")'),
]

HOMONYMS = [
    ("diffusion in the physical sciences (not social diffusion)",
     '("diffusion coefficient" OR "diffusion tensor" OR "molecular diffusion" OR "gas diffusion")'),
    ("social network ANALYSIS as a method (not a substantive channel claim)",
     '("social network analysis" OR "network centrality" OR "graph theory")'),
    ("media / communication in marketing or non-fertility research",
     '("advertising" OR "marketing" OR "brand awareness" OR "consumer behaviour")'),
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
    q("control: C.2.c housing frame (a written chapter; 405 recorded 205, 52 got 181, 89_d2c 170, 89_d1d 166)",
      AND('("house price" OR "housing cost" OR "house prices")',
          '("fertility" OR "childbearing" OR "birth rate" OR "total fertility rate" OR "childlessness")'))
    q("A.20 narrow frame (diffusion-of-innovations core AND fertility)",
      AND(A20_NARROW, OUTCOME))
    frame = q("A.20 production frame (topic union AND outcome)", AND(A20, OUTCOME))
    q("A.20 topic block with no outcome restriction", A20)

    print("C — completeness test: pricing every registered construct", flush=True)
    for term in OWN_CANDIDATES:
        cand = A20[:-1] + f' OR "{term}")'
        n = q(f"own + {term}", AND(cand, OUTCOME))
        if n is not None and frame is not None:
            R[f"gain: own + {term}"] = n - frame
    if frame is not None:
        allo = A20[:-1] + "".join(f' OR "{t}"' for t in OWN_CANDIDATES) + ")"
        n = q("A.20 block widened by ALL registered constructs", AND(allo, OUTCOME))
        if n is not None:
            R["gain: own widened by ALL"] = n - frame

    print("E — calibrating the outcome axis", flush=True)
    for label, block in LEVELS:
        q(f"level: {label}", AND(A20, block))

    print("F — identification markers inside the frame", flush=True)
    q("frame AND identified-design markers", AND(A20, OUTCOME, IDENT))

    print("H — the six walls, read from both sides", flush=True)
    for code, name, status, block in WALLS:
        q(f"wall {code} overlap with our frame", AND(A20, OUTCOME, block))
        q(f"wall {code} neighbour frame", AND(block, OUTCOME))
        q(f"wall {code} overlap AND identified", AND(A20, OUTCOME, block, IDENT))

    print("I — homonym readings inside our own frame", flush=True)
    for label, block in HOMONYMS:
        q(f"homonym: {label}", AND(A20, OUTCOME, block))

    stamp = datetime.date.today().isoformat()
    LOGDIR.mkdir(parents=True, exist_ok=True)
    payload = {"generated": stamp, "script": "source/build/goldset/89_a20_frame_probe.py",
               "api_key_present": bool(API_KEY), "counts": R,
               "refusals": [{"label": l, "error": e} for l, e in refusals]}
    (LOGDIR / f"a20-frame-probe-{stamp}.json").write_text(json.dumps(payload, indent=1))

    def cell(v):
        return "REFUSED" if v is None else f"{v:,}"

    md = [f"# A.20 cultural-diffusion-mechanisms frame probe — {stamp}", "",
          "Generated by `source/build/goldset/89_a20_frame_probe.py`. Do not edit by hand;",
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
           "from a genuine A.20 construct means the baseline was under-built; a large gain from a",
           "generic word ('diffusion', 'network', 'media', 'television', 'radio') is a free-OR",
           "inflater that annexes a neighbour or homonym literature, not a widening.", "",
           "| candidate | marginal gain |", "|---|---|"]
    for label, v in R.items():
        if label.startswith("gain: "):
            md.append(f"| {label[6:]} | {v if v is not None else 'REFUSED'} |")
    md += ["", "## Walls", "",
           "Each wall: overlap with our frame, the neighbour's own frame, and the overlap among",
           "identified records. Routing is defensible where the overlap is a small share of our",
           "frame and the identified overlap is near zero. A.3 (fertility-control CONTENT) is the",
           "load-bearing wall: A.20 owns the channel, A.3 owns the message it carries. The test is",
           "that the *identified* overlap is thin -- A.20's identified core is the media-reach and",
           "network-position designs A.3 deliberately excluded as content-agnostic (Brazil novela,",
           "India cable TV), not a re-run of A.3's fertility-control-knowledge cell.", ""]
    (LOGDIR / f"a20-frame-probe-{stamp}.md").write_text("\n".join(md) + "\n")
    print(f"\nwrote {LOGDIR}/a20-frame-probe-{stamp}.{{json,md}}")
    if refusals:
        print(f"{len(refusals)} refusal(s) — those rows are missing, not zero", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
