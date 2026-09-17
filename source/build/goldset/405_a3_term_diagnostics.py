#!/usr/bin/env python3
"""
405 — A.3 (TICK-088) stage-2 diagnostic: clear or convict A.3's frame of the defect that unseated
A.6, then measure the A.20 wall, which is the question of whether this chapter exists separately at
all.

Why this exists
---------------
`404` unseated A.6 by showing its selecting frame carried only the negative pole of a construct the
registry defines by its positive one: no form of "legitimation" in a block scoping "cultural
LEGITIMATION of contraception and abortion". A.6 corrected from 668 to 1,225 and A.3 became the
smallest bracketed candidate at 719. TICK-088 therefore opens by asking the same question of A.3
before spending anything on a search (`advance-the-baseline-when-accepting-terms`).

The question is not the one it first appears to be
--------------------------------------------------
A.3's registered claim is that fertility control spreads "through linguistic, religious, and social
networks via diffusion of information about and legitimation of birth control". Read alone, A.3's
pass-4 block looks badly under-framed: it carries no *social network*, no *peer effect*, nothing
linguistic, nothing religious.

But those terms are not A.3's to carry. A.20 (`cultural-diffusion-mechanisms`) is a separate
registered hypothesis whose claim is the channels "social networks, mass media, and
linguistic/cultural community boundaries", and whose registry note says it **absorbs**
`social-network-peer-effects`, `ideational-diffusion-mass-media` and
`linguistic-cultural-boundaries-princeton`. So A.3's omissions are A.20's territory, and what looked
like a completeness defect is mostly a wall. Block C prices only the terms A.3 genuinely owns —
those naming the *thing being spread*, not the *channel it spreads through*.

One term sits in neither camp cleanly, and it is the same word that unseated A.6: **legitimation**.
It appears in A.3's registered claim, it is absent from A.3's block, and it is A.6's central noun.
A.20 cannot own it because A.20 is explicitly "independent of the content of those norms", and
legitimation is content. So legitimation is a genuine A.3 gap AND a live A.3/A.6 boundary term, and
block C prices it first.

The A.20 wall is the chapter's existence question
-------------------------------------------------
A.3 and A.20 are both registered as *proximate/mechanism* entries; both say "independent of" the
underlying driver; both describe spread through networks and linguistic communities; and they share
two seminal citations (Coale and Watkins 1986; Bongaarts and Watkins 1996). The registry's own
distinction is thin: A.3 is the diffusion *of fertility-control information and legitimation
specifically*, A.20 is the *channel architecture whatever the content*. `304` measured the pair at
7 records, which by the C.3.d inherited finding is not reassurance — a 7-record vocabulary overlap
told C.3.d nothing, and 8 of its 9 overlapping full texts could not separate the estimands
(`design-is-not-a-property-of-the-title`). Block H measures the pair from both sides and among
identified records, so the scope doc can put a number on a PI call that may end in a merge.

Lessons this design honours
---------------------------
  anchored-vocabulary-has-own-homonym   — "social learning" is a machine-learning and animal-
      behaviour term before it is a demographic one (`304` put that reading at 1,775) and
      "diffusion" is a physical-sciences term at 221,765. Block I measures both inside our frame.
  advance-the-baseline-when-accepting-terms / frame-growth-is-not-frame-gain — every candidate is
      priced as (baseline OR term) minus baseline, never by its own size.
  calibrate-the-outcome-axis-too        — block E.
  wall-cut-on-wrong-axis                — every wall is read as a share of our frame AND of theirs.
  validate-a-null-detector-on-positives — block A runs a written chapter's frame first and
      re-measures the recorded figures so drift is visible rather than silent.
  refusals-read-as-zeros                — a failed request raises and reports REFUSED. Those rows
      are missing, not zero.

Outputs literature/search-logs/a3-term-diagnostics-<date>.{json,md}. Counting only; no records are
retained, so this is cheap and re-runnable.

OpenAlex hazards honoured
-------------------------
  - a comma inside a filter VALUE is fatal and %2C does not save it -> no commas in any term
  - a phrase beginning "not" parses as boolean NOT -> none here; negation is by subtraction
  - "?" is a wildcard returning 200 with a misleading body -> none here
  - hyphens fold and stopwords drop inside phrases, so a drop test must remove every spelling
    together ("social learning" and "social-learning" are one term)
  - an AND-containing arm cannot be OR'd into a union -> every arm is pulled separately
  - this Python has no CA bundle: shell out to curl rather than urllib
"""
import json, subprocess, sys, urllib.parse, datetime, pathlib, time

MAILTO = "shravanh@uchicago.edu"
BASE = "https://api.openalex.org/works"
LOGDIR = pathlib.Path("literature/search-logs")
CACHE = pathlib.Path("temp/a3-term-diagnostics-cache.json")


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

OUTCOME = '("fertility" OR "childbearing" OR "birth rate" OR "total fertility rate")'
OUTCOME_WIDE = ('("fertility" OR "childbearing" OR "birth rate" OR "total fertility rate" '
                'OR "family size" OR "number of children")')

# A.3 pass 1 and pass 4, verbatim from 304, so the reproduction is exact.
A3_NARROW = ('("diffusion of fertility control" OR "fertility diffusion" '
             'OR "spread of birth control" OR "family limitation")')
A3 = ('("diffusion of fertility control" OR "ideational change" OR "fertility diffusion" '
      'OR "innovation diffusion" OR "spread of birth control" OR "social learning" '
      'OR "cultural transmission" OR "social contagion" OR "spatial diffusion" '
      'OR "family limitation")')

IDENT = ('("instrumental variable" OR "difference-in-differences" OR "differences-in-differences" '
         'OR "natural experiment" OR "regression discontinuity" OR "randomized controlled trial" '
         'OR "randomised controlled trial" OR "event study" OR "synthetic control")')

# Block C. Terms naming WHAT IS SPREAD -- A.3's own territory. Channel terms are deliberately
# excluded here and measured as the A.20 wall in block H instead. "legitimation" is priced first
# because it is in A.3's registered claim, absent from its block, and A.6's central noun.
OWN_CANDIDATES = [
    "legitimation", "legitimacy", "contraceptive diffusion", "knowledge of contraception",
    "awareness of contraception", "information diffusion", "adoption of birth control",
    "innovation adoption", "calculus of conscious choice", "fertility transition onset",
    "European Fertility Project", "birth control knowledge",
]

# Channel terms, priced separately so the scope doc can state what A.3 would gain by annexing
# A.20's territory -- a number the PI call needs, not a widening this script recommends.
CHANNEL_CANDIDATES = [
    "social network", "peer effect", "peer influence", "social influence", "mass media",
    "linguistic boundary", "language boundary", "cultural boundary", "neighbourhood effect",
]

LEVELS = [
    ("realized fertility", '("total fertility rate" OR "completed fertility" OR "birth rate" '
                           'OR "marital fertility")'),
    ("intention or desire", '("fertility intention" OR "desired family size" OR "ideal family size" '
                            'OR "fertility preferences")'),
    ("contraceptive use as the outcome", '("contraceptive use" OR "contraceptive uptake" '
                                         'OR "contraceptive prevalence" OR "unmet need")'),
    ("adoption or innovation timing", '("time to adoption" OR "adoption timing" OR "hazard of adoption")'),
]

# Phenomenon windows. A.3 is registered FDT and SDT, and the two arms are different literatures:
# historical European demography versus contemporary LMIC diffusion studies.
WINDOWS = [
    ("FDT / historical European", '("historical demography" OR "nineteenth century" '
                                  'OR "19th century" OR "parish register" OR "pre-transitional")'),
    ("SDT / contemporary LMIC", '("sub-Saharan" OR "developing countries" OR "Demographic and Health Survey" '
                                'OR "low-income countries")'),
]

WALLS = [
    ("A.20", "cultural diffusion mechanisms — the existence question", "unstarted — shares 2 of 4 seminals",
     '("social network" OR "peer effect" OR "peer influence" OR "mass media" OR "soap opera" '
     'OR "linguistic boundary" OR "language boundary" OR "cultural boundary")'),
    ("A.6", "stigma reduction — parked TICK-087, shares 2 of 4 seminals", "parked",
     '("stigma" OR "taboo" OR "social disapproval" OR "moral opposition")'),
    ("A.19", "intergenerational transmission — vertical rather than horizontal spread", "unstarted",
     '("intergenerational transmission" OR "fertility transmission" OR "parental family size" '
     'OR "sibship size")'),
    ("A.2", "contraceptive technology and diffusion", "unstarted",
     '("oral contraceptive" OR "contraceptive technology" OR "intrauterine device" '
     'OR "modern contraception")'),
    ("D.1.a", "postmaterialism individualism and secularisation", "drafted — inheritable",
     '("secularization" OR "secularisation" OR "individualism" OR "postmaterialism" '
     'OR "value change" OR "religiosity")'),
    ("D.1.b", "cultural westernisation and developmental idealism", "drafted — inheritable",
     '("westernization" OR "westernisation" OR "mass schooling" OR "developmental idealism")'),
]

HOMONYMS = [
    ("social learning in machine learning and animal behaviour",
     '("machine learning" OR "reinforcement learning" OR "neural network" OR "animal behaviour" '
     'OR "primate" OR "chimpanzee")'),
    ("diffusion in the physical sciences",
     '("molecular diffusion" OR "thermal diffusion" OR "solute" OR "membrane")'),
    ("cultural transmission in biology",
     '("birdsong" OR "vertical transmission" OR "gene culture coevolution")'),
    ("epidemic and disease spread", '("epidemic" OR "infectious disease" OR "contact tracing")'),
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

    print("A — control and reproduction", flush=True)
    q("control: C.2.c housing frame (a written chapter)",
      AND('("house price" OR "housing cost" OR "house prices")', OUTCOME_WIDE))
    q("reproduce A.3 pass 1 narrow (09-13 recorded 112 on a wider narrow block)",
      AND(A3_NARROW, OUTCOME))
    frame = q("reproduce A.3 pass 4 union frame (09-13 recorded 727)", AND(A3, OUTCOME_WIDE))
    q("A.3 block with no outcome restriction", A3)

    print("C — pricing the terms A.3 OWNS (what is spread)", flush=True)
    for term in OWN_CANDIDATES:
        cand = A3[:-1] + f' OR "{term}")'
        n = q(f"own + {term}", AND(cand, OUTCOME_WIDE))
        if n is not None and frame is not None:
            R[f"gain: own + {term}"] = n - frame
    if frame is not None:
        allo = A3[:-1] + "".join(f' OR "{t}"' for t in OWN_CANDIDATES) + ")"
        n = q("A.3 block widened by ALL of its own terms", AND(allo, OUTCOME_WIDE))
        if n is not None:
            R["gain: own widened by ALL"] = n - frame

    print("D — pricing CHANNEL terms (A.20's territory, for the PI call only)", flush=True)
    for term in CHANNEL_CANDIDATES:
        cand = A3[:-1] + f' OR "{term}")'
        n = q(f"channel + {term}", AND(cand, OUTCOME_WIDE))
        if n is not None and frame is not None:
            R[f"gain: channel + {term}"] = n - frame
    if frame is not None:
        allc = A3[:-1] + "".join(f' OR "{t}"' for t in CHANNEL_CANDIDATES) + ")"
        n = q("A.3 block widened by ALL channel terms", AND(allc, OUTCOME_WIDE))
        if n is not None:
            R["gain: channel widened by ALL"] = n - frame

    print("E — calibrating the outcome axis", flush=True)
    q("outcome narrow instead of wide", AND(A3, OUTCOME))
    for extra in ["marital fertility", "parity", "births", "contraceptive use"]:
        cand = OUTCOME_WIDE[:-1] + f' OR "{extra}")'
        n = q(f"outcome + {extra}", AND(A3, cand))
        if n is not None and frame is not None:
            R[f"gain: outcome + {extra}"] = n - frame

    print("F — identification markers inside the frame", flush=True)
    q("frame AND identified-design markers", AND(A3, OUTCOME_WIDE, IDENT))
    q("frame AND qualitative markers",
      AND(A3, OUTCOME_WIDE, '("qualitative" OR "focus group" OR "in-depth interview" OR "ethnographic")'))
    q("frame AND simulation or model-only markers",
      AND(A3, OUTCOME_WIDE, '("agent-based" OR "simulation" OR "microsimulation" OR "calibrated model")'))

    print("G — outcome level and phenomenon window", flush=True)
    for label, block in LEVELS:
        q(f"level: {label}", AND(A3, OUTCOME_WIDE, block))
    for label, block in WINDOWS:
        q(f"window: {label}", AND(A3, OUTCOME_WIDE, block))

    print("H — the six walls, read from both sides", flush=True)
    for code, name, status, block in WALLS:
        q(f"wall {code} overlap with our frame", AND(A3, OUTCOME_WIDE, block))
        q(f"wall {code} neighbour frame", AND(block, OUTCOME_WIDE))
        q(f"wall {code} overlap AND identified", AND(A3, OUTCOME_WIDE, block, IDENT))

    print("I — homonym readings inside our own frame", flush=True)
    for label, block in HOMONYMS:
        q(f"homonym: {label}", AND(A3, OUTCOME_WIDE, block))

    stamp = datetime.date.today().isoformat()
    LOGDIR.mkdir(parents=True, exist_ok=True)
    payload = {"generated": stamp, "script": "source/build/goldset/405_a3_term_diagnostics.py",
               "api_key_present": bool(API_KEY), "counts": R,
               "refusals": [{"label": l, "error": e} for l, e in refusals]}
    (LOGDIR / f"a3-term-diagnostics-{stamp}.json").write_text(json.dumps(payload, indent=1))

    def cell(v):
        return "REFUSED" if v is None else f"{v:,}"

    md = [f"# A.3 term diagnostics — {stamp}", "",
          "Generated by `source/build/goldset/405_a3_term_diagnostics.py`. Do not edit by hand;",
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
           "Priced as (baseline OR term) minus baseline, never by the term's own size. Channel terms",
           "are A.20's registered territory and are priced for the PI call, not proposed as a widening.",
           "", "| candidate | marginal gain |", "|---|---|"]
    for label, v in R.items():
        if label.startswith("gain: "):
            md.append(f"| {label[6:]} | {v if v is not None else 'REFUSED'} |")
    (LOGDIR / f"a3-term-diagnostics-{stamp}.md").write_text("\n".join(md) + "\n")
    print(f"\nwrote {LOGDIR}/a3-term-diagnostics-{stamp}.{{json,md}}")
    if refusals:
        print(f"{len(refusals)} refusal(s) — those rows are missing, not zero", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
