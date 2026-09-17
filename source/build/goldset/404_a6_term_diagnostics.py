#!/usr/bin/env python3
"""
404 — A.6 (TICK-087) stage-2 diagnostic: audit the conjunction that won A.6 the rank, price every
term in both exposure blocks, split the frame by OUTCOME LEVEL, and measure six walls from both
sides.

Why this exists
---------------
The 2026-09-13 candidate frame probe (`304`, committed on branch 080 as 31836fb) ranked A.6 first
among bracketed candidates on a union frame of 680, ahead of A.3 at 727. That number selected the
chapter. This script asks whether it means what the ranking assumed it means.

The conjunction problem, which is specific to A.6
-------------------------------------------------
Pass 4 of `304` applies OUTCOME_WIDE to every union frame (304:523). For a candidate whose union is
a flat OR-list of exposure terms -- C.3.f's twelve, A.19's eleven -- the result is a TWO-block
conjunction: exposure AND outcome. A.6's union is not a flat OR-list. It is

    (stigma OR taboo OR social disapproval OR moral opposition OR ...4 compounds)
      AND (contraception OR contraceptive OR abortion OR family planning OR birth control)

so with the outcome axis applied A.6's 680 is a THREE-block conjunction: stigma AND object AND
outcome. That is defensible -- A.6's exposure genuinely is a two-part concept, stigma *about a
specific object* -- but it has two consequences the ranking did not account for.

  1. The 680 is depressed relative to the two-block frames it was ranked against. Comparing it to
     C.3.f's 1,101 or A.3's 727 is not comparing like with like.
  2. Vocabulary misses compound MULTIPLICATIVELY across three blocks. A paper estimating this
     chapter's parameter while writing "religious opposition to family limitation" rather than
     "stigma" is lost at block 1; one writing "moral acceptability of birth spacing" is lost at
     block 2. In a two-block frame a single miss costs one factor; here it can cost two.

So the first job is not to scope A.6 but to establish whether 680 is a frame or an artefact. Blocks
B and C below answer that: B decomposes the conjunction to show which block binds, and C prices
plausible additions to the stigma block on top of the registered eight. If C balloons the frame,
A.6 is not the smallest candidate and the selection in TICK-087 has to be revisited before any
production query is run (`frame-growth-is-not-frame-gain` cuts the other way too: growth that comes
from terms a domain reader would have registered is gain, not noise).

The outcome-level problem, which decides the estimand
----------------------------------------------------
A.6's mechanism runs THROUGH contraceptive use: destigmatisation lowers the social cost of using an
available method, use rises, fertility falls. So most of this literature's natural dependent
variable is contraceptive use or unmet need, not a birth. A frame built on a fertility outcome axis
will therefore retrieve the minority of the literature that carried a fertility word, and the
chapter's parameter -- an effect on FERTILITY -- may be estimated almost nowhere. Block G measures
the split before the estimand is declared, because declaring it after would be fitting the estimand
to what happened to be retrievable (`calibrate-the-outcome-axis-too`).

The wall problem, which is unusual here
---------------------------------------
Three of A.6's six neighbours are UNSTARTED candidates (A.2, A.4, A.5); one more, A.3, is unstarted
AND shares two of A.6's four registered seminal citations (Cleland and Wilson 1987; Bongaarts and
Watkins 1996). A shared seminal citation is the signature TICK-055 recorded for a wall that is
broken rather than tight. So the A.6/A.3 wall is measured here even though `304` never measured it:
the probe measured A.3's boundaries against A.20, D.1.a and A.2, and never against A.6.

Every wall is read from BOTH sides (`wall-cut-on-wrong-axis`): an overlap of 29 records is small as
a share of a 680 frame and large as a share of a 200 one, and only the pair of shares says whether
the wall holds. Overlap among IDENTIFIED records is measured separately, because C.3.d's inherited
finding is that small vocabulary overlaps do not reassure -- 8 of its 9 overlapping full texts could
not separate the two estimands (`design-is-not-a-property-of-the-title`).

Lessons this design honours
---------------------------
  anchored-vocabulary-has-own-homonym   — "stigma" unrestricted is 202,130 records (probe, 09-13).
      Block I measures the HIV / mental-illness / obesity / leprosy readings inside our own frame
      rather than trusting the object block to exclude them.
  advance-the-baseline-when-accepting-terms / frame-growth-is-not-frame-gain — candidate terms are
      priced as (baseline OR term) minus baseline, never by their own size.
  calibrate-the-outcome-axis-too        — block E does to the outcome axis what C does to exposure.
  validate-a-null-detector-on-positives — block A runs a written chapter's frame first, and the
      three probe figures are re-measured so that index drift is visible rather than silent.
  refusals-read-as-zeros                — a failed request raises and is reported as REFUSED. Those
      rows are missing, not zero.

Outputs literature/search-logs/a6-term-diagnostics-<date>.{json,md}. Counting only; no records are
retained, so this is cheap and re-runnable.

OpenAlex hazards honoured
-------------------------
  - a comma inside a filter VALUE is fatal and %2C does not save it -> no commas in any term
  - a phrase beginning "not" parses as boolean NOT -> none here; every negation is computed by
    subtraction so the query language never has to express one
  - "?" in a search value is a wildcard and returns 200 with a misleading body -> none here
  - OpenAlex folds hyphens and drops stopwords inside phrases, so "social disapproval" and
    "social-disapproval" are one term, and a drop test must remove every spelling together
  - an AND-containing arm cannot be OR'd into a union -> every arm here is pulled separately and
    no arm is concatenated into another with OR
  - this Python has no CA bundle: shell out to curl rather than urllib
"""
import json, subprocess, sys, urllib.parse, datetime, pathlib, time

MAILTO = "shravanh@uchicago.edu"
BASE = "https://api.openalex.org/works"
LOGDIR = pathlib.Path("literature/search-logs")
CACHE = pathlib.Path("temp/a6-term-diagnostics-cache.json")


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

# ----------------------------------------------------------------- the axes, verbatim from 304
OUTCOME = '("fertility" OR "childbearing" OR "birth rate" OR "total fertility rate")'
OUTCOME_WIDE = ('("fertility" OR "childbearing" OR "birth rate" OR "total fertility rate" '
                'OR "family size" OR "number of children")')

# A.6 pass 1, pass 2 and pass 4, copied from 304 so the reproduction is exact.
A6_NARROW = ('("abortion stigma" OR "contraceptive stigma" OR "contraception stigma" '
             'OR "family planning stigma")')
A6_WIDE_STIGMA = '("stigma" OR "taboo" OR "social disapproval" OR "shame")'
A6_WIDE_OBJECT = '("contraception" OR "contraceptive" OR "abortion" OR "family planning")'
STIGMA = ('("abortion stigma" OR "contraceptive stigma" OR "contraception stigma" '
          'OR "family planning stigma" OR "stigma" OR "taboo" OR "social disapproval" '
          'OR "moral opposition")')
OBJECT = ('("contraception" OR "contraceptive" OR "abortion" OR "family planning" '
          'OR "birth control")')

IDENT = ('("instrumental variable" OR "difference-in-differences" OR "differences-in-differences" '
         'OR "natural experiment" OR "regression discontinuity" OR "randomized controlled trial" '
         'OR "randomised controlled trial" OR "event study" OR "synthetic control")')

# Candidate additions to the stigma block. Every one is a phrase a domain author could plausibly
# use for the SAME construct -- the social cost of being seen to control fertility -- and none is
# a synonym for the object. Priced on top of the registered eight, in this order.
STIGMA_CANDIDATES = [
    "social acceptability", "moral acceptability", "religious opposition", "moral objection",
    "disapproval", "social norms", "normative pressure", "legitimation", "legitimacy",
    "normalization", "normalisation", "secrecy", "embarrassment", "social sanction",
    "community disapproval", "husband opposition", "opposition to family planning",
]

# Candidate additions to the object block, same treatment.
OBJECT_CANDIDATES = [
    "fertility control", "family limitation", "birth spacing", "sterilization", "sterilisation",
    "intrauterine device", "oral contraceptive", "condom", "emergency contraception",
    "termination of pregnancy",
]

# Outcome-level vocabularies. A.6's mechanism runs through USE, so the use row is the one that
# decides whether this chapter's registered outcome is estimated at all.
LEVELS = [
    ("realized fertility", '("total fertility rate" OR "completed fertility" OR "birth rate" '
                           'OR "number of children ever born")'),
    ("intention or desire", '("fertility intention" OR "desired family size" OR "ideal family size" '
                            'OR "fertility preferences" OR "wanted fertility")'),
    ("contraceptive use as the outcome", '("contraceptive use" OR "contraceptive uptake" '
                                         'OR "contraceptive prevalence" OR "unmet need")'),
    ("attitude or scale measurement", '("attitude scale" OR "stigma scale" OR "vignette" '
                                      'OR "survey experiment" OR "psychometric")'),
]

# The six walls. Each neighbour gets its own block, ANDed with OUTCOME_WIDE for the neighbour's own
# frame, so an overlap can be expressed as a share of THEIR frame as well as ours.
WALLS = [
    ("A.2", "contraceptive technology and diffusion", "unstarted",
     '("oral contraceptive" OR "contraceptive technology" OR "intrauterine device" '
     'OR "modern contraception" OR "contraceptive method mix")'),
    ("A.3", "diffusion and social learning of fertility control", "unstarted — shares 2 of 4 seminals",
     '("diffusion of fertility control" OR "fertility diffusion" OR "spread of birth control" '
     'OR "family limitation" OR "ideational change" OR "social learning")'),
    ("A.4", "induced abortion access and legalisation", "unstarted",
     '("induced abortion" OR "abortion legalization" OR "abortion legalisation" OR "abortion law" '
     'OR "abortion access" OR "abortion restriction" OR "abortion policy")'),
    ("A.5", "organised family planning programmes", "unstarted",
     '("family planning program" OR "family planning programme" OR "family planning services" '
     'OR "unmet need for contraception")'),
    ("D.1.a", "postmaterialism individualism and secularisation", "drafted — inheritable",
     '("secularization" OR "secularisation" OR "individualism" OR "postmaterialism" '
     'OR "value change" OR "religiosity")'),
    ("B.5", "fetal loss and intrauterine mortality (clinical homonym)", "drafted",
     '("spontaneous abortion" OR "miscarriage" OR "pregnancy loss" OR "stillbirth")'),
]

# Block J. The registered claim (HYPOTHESES-v5 §A.6) is about "cultural LEGITIMATION of
# contraception and abortion". The probe's stigma block contains no form of "legitimation",
# "normalisation" or "acceptability" -- that is, not the registered construct's own central noun,
# only its negative pole. These six restore it. They are not speculative synonyms: they are the
# words the registry itself uses, so growth here is frame GAIN and not frame noise.
STIGMA_REGISTERED = ["legitimation", "normalization", "normalisation", "social acceptability",
                     "moral acceptability", "disapproval"]

# The two candidates A.6 was ranked ahead of, reproduced verbatim from 304's pass-4 list so the
# re-check compares like with like. Both are flat OR-lists: TWO-block conjunctions once the outcome
# axis is applied, against A.6's three.
A3_UNION = ('("diffusion of fertility control" OR "ideational change" OR "fertility diffusion" '
            'OR "innovation diffusion" OR "spread of birth control" OR "social learning" '
            'OR "cultural transmission" OR "social contagion" OR "spatial diffusion" '
            'OR "family limitation")')
C3A_UNION = ('("mode of production" OR "agricultural household" OR "peasant household" '
             'OR "farm household" OR "subsistence agriculture" OR "land tenure" '
             'OR "agrarian society")')

# Homonym readings of "stigma" that the object block is supposed to exclude.
HOMONYMS = [
    ("HIV and sexual health", '("HIV" OR "AIDS" OR "sexually transmitted")'),
    ("mental illness", '("mental illness" OR "mental health" OR "depression" OR "schizophrenia")'),
    ("obesity and body weight", '("obesity" OR "overweight" OR "body weight")'),
    ("leprosy tuberculosis and infectious disease", '("leprosy" OR "tuberculosis" OR "epilepsy")'),
]


class Refused(Exception):
    """A failed request. Never let this reach a counter as a zero."""


def _cache_load():
    try:
        return json.loads(CACHE.read_text())
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def count(query: str, cache: dict, _retried=False) -> int:
    """Record count for one title_and_abstract.search query. Cached by exact query string."""
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
        """Measure one labelled query, recording a refusal rather than a zero."""
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

    print("A — control and reproduction of the 09-13 figures", flush=True)
    q("control: C.2.c housing frame (a written chapter)",
      AND('("house price" OR "housing cost" OR "house prices")', OUTCOME_WIDE))
    q("reproduce A.6 pass 1 narrow (09-13 recorded 12)", AND(A6_NARROW, OUTCOME))
    q("reproduce A.6 pass 2 wide (09-13 recorded 691)",
      AND(A6_WIDE_STIGMA, A6_WIDE_OBJECT, OUTCOME_WIDE))
    frame = q("reproduce A.6 pass 4 union frame (09-13 recorded 680)",
              AND(STIGMA, OBJECT, OUTCOME_WIDE))
    q("reproduce stigma unrestricted (09-13 recorded 202130)", '"stigma"')

    print("B — decomposing the three-block conjunction", flush=True)
    q("stigma block AND outcome, object block dropped", AND(STIGMA, OUTCOME_WIDE))
    q("object block AND outcome, stigma block dropped", AND(OBJECT, OUTCOME_WIDE))
    q("stigma AND object, outcome block dropped", AND(STIGMA, OBJECT))

    print("C — pricing candidate additions to the STIGMA block", flush=True)
    base_stigma, base_n = STIGMA, frame
    for term in STIGMA_CANDIDATES:
        cand = base_stigma[:-1] + f' OR "{term}")'
        n = q(f"stigma + {term}", AND(cand, OBJECT, OUTCOME_WIDE))
        if n is not None and base_n is not None:
            R[f"gain: stigma + {term}"] = n - base_n
    if base_n is not None:
        allc = base_stigma[:-1] + "".join(f' OR "{t}"' for t in STIGMA_CANDIDATES) + ")"
        n = q("stigma block widened by ALL candidates", AND(allc, OBJECT, OUTCOME_WIDE))
        if n is not None:
            R["gain: stigma widened by ALL"] = n - base_n

    print("D — pricing candidate additions to the OBJECT block", flush=True)
    for term in OBJECT_CANDIDATES:
        cand = OBJECT[:-1] + f' OR "{term}")'
        n = q(f"object + {term}", AND(STIGMA, cand, OUTCOME_WIDE))
        if n is not None and frame is not None:
            R[f"gain: object + {term}"] = n - frame
    if frame is not None:
        allo = OBJECT[:-1] + "".join(f' OR "{t}"' for t in OBJECT_CANDIDATES) + ")"
        n = q("object block widened by ALL candidates", AND(STIGMA, allo, OUTCOME_WIDE))
        if n is not None:
            R["gain: object widened by ALL"] = n - frame

    print("E — calibrating the outcome axis", flush=True)
    q("outcome narrow instead of wide", AND(STIGMA, OBJECT, OUTCOME))
    for extra in ["completed fertility", "parity", "births", "number of children ever born"]:
        cand = OUTCOME_WIDE[:-1] + f' OR "{extra}")'
        n = q(f"outcome + {extra}", AND(STIGMA, OBJECT, cand))
        if n is not None and frame is not None:
            R[f"gain: outcome + {extra}"] = n - frame

    print("F — identification markers inside the frame", flush=True)
    q("frame AND identified-design markers", AND(STIGMA, OBJECT, OUTCOME_WIDE, IDENT))
    q("frame AND qualitative markers",
      AND(STIGMA, OBJECT, OUTCOME_WIDE,
          '("qualitative" OR "focus group" OR "in-depth interview" OR "ethnographic")'))

    print("G — outcome level inside the frame", flush=True)
    for label, block in LEVELS:
        q(f"level: {label}", AND(STIGMA, OBJECT, OUTCOME_WIDE, block))
    for label, block in LEVELS:
        q(f"level without our outcome axis: {label}", AND(STIGMA, OBJECT, block))

    print("H — the six walls, read from both sides", flush=True)
    for code, name, status, block in WALLS:
        q(f"wall {code} overlap with our frame", AND(STIGMA, OBJECT, OUTCOME_WIDE, block))
        q(f"wall {code} neighbour frame", AND(block, OUTCOME_WIDE))
        q(f"wall {code} overlap AND identified", AND(STIGMA, OBJECT, OUTCOME_WIDE, block, IDENT))

    print("I — homonym readings inside our own frame", flush=True)
    for label, block in HOMONYMS:
        q(f"homonym: {label}", AND(STIGMA, OBJECT, OUTCOME_WIDE, block))

    print("J — does the selection survive restoring the registered construct?", flush=True)
    reg = STIGMA[:-1] + "".join(f' OR "{t}"' for t in STIGMA_REGISTERED) + ")"
    n_reg = q("frame with the registered construct restored", AND(reg, OBJECT, OUTCOME_WIDE))
    if n_reg is not None and frame is not None:
        R["gain: registered construct restored"] = n_reg - frame
    out_births = OUTCOME_WIDE[:-1] + ' OR "births")'
    q("frame with registered construct AND births in the outcome axis",
      AND(reg, OBJECT, out_births))
    q("re-check A.3 union frame (09-13 recorded 727)", AND(A3_UNION, OUTCOME_WIDE))
    q("re-check C.3.a union frame (09-13 recorded 1811)", AND(C3A_UNION, OUTCOME_WIDE))

    stamp = datetime.date.today().isoformat()
    LOGDIR.mkdir(parents=True, exist_ok=True)
    payload = {"generated": stamp, "script": "source/build/goldset/404_a6_term_diagnostics.py",
               "api_key_present": bool(API_KEY), "counts": R,
               "refusals": [{"label": l, "error": e} for l, e in refusals]}
    (LOGDIR / f"a6-term-diagnostics-{stamp}.json").write_text(json.dumps(payload, indent=1))

    def row(label):
        v = R.get(label)
        return "REFUSED" if v is None else f"{v:,}"

    md = [f"# A.6 term diagnostics — {stamp}", "",
          "Generated by `source/build/goldset/404_a6_term_diagnostics.py`. Do not edit by hand;",
          "re-run the script.", "",
          "These are OpenAlex `title_and_abstract.search` record counts. They size a *retrieval",
          "frame* and its overlaps. **No production query has been run, no anchor resolved, and no",
          "record screened.** A count is not an evidence base, and a study can estimate this",
          "chapter's parameter without carrying any of these phrases in its abstract.", ""]
    if refusals:
        md += [f"**{len(refusals)} request(s) REFUSED.** Those rows are missing, not zero.", ""]
    md += ["| block | measurement | n |", "|---|---|---|"]
    for label in R:
        if label.startswith("gain: "):
            continue
        md.append(f"| | {label} | {row(label)} |")
    md += ["", "## Marginal gain of candidate terms", "",
           "Priced as (baseline OR term) minus baseline, never by the term's own size.", "",
           "| candidate | marginal gain |", "|---|---|"]
    for label, v in R.items():
        if label.startswith("gain: "):
            md.append(f"| {label[6:]} | {v if v is not None else 'REFUSED'} |")
    (LOGDIR / f"a6-term-diagnostics-{stamp}.md").write_text("\n".join(md) + "\n")
    print(f"\nwrote {LOGDIR}/a6-term-diagnostics-{stamp}.{{json,md}}")
    if refusals:
        print(f"{len(refusals)} refusal(s) — those rows are missing, not zero", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
