#!/usr/bin/env python3
"""
89 — A.14 (TICK-091) stage-3 frame probe: confirm or refute that coital frequency and fecundability is
the smallest genuinely-unstarted candidate, and run the registered-construct completeness test the
A.6/A.3 episode made mandatory before any search spend.

Why this exists
---------------
A.14 was picked as the smallest *unstarted* hypothesis on a cheap scouting count (production frame
= 373, an order of magnitude below the ~1,808 bar and below every other unstarted candidate). TICK-087
(A.6) and TICK-088 (A.3) were both mis-ranked because their selecting frames were priced wrong — A.6
omitted its own registered construct ("legitimation"); A.3 was charged a neighbour's channel terms and
a free-standing OR. This probe applies the corrected rule to A.14 *before* spending screen budget:
price the frame against its OWN conjoined construct set, read every wall from both sides, and count the
homonym load inside the frame.

The registered-construct completeness test
------------------------------------------
Block C prices every noun the A.14 claim names (coital frequency, intercourse, abstinence, spousal
separation, libido/desire, the "sex recession") as (baseline OR term) minus baseline. A large marginal
gain from a term that is genuinely A.14's means the baseline frame was under-built and the term belongs
in it (frame grows, but honestly). A large gain from a generic word conjoined to nothing -- "separation",
"activity", "desire" -- is the free-OR inflater the A.3 park was built on, and is reported as such, not
folded into the frame.

The walls are read from both sides
-----------------------------------
Contraception/abortion (A.2-A.6), marriage/union (A.7/C.7), lactation (A.13), fecundity capacity
(A.15/A.16/B.3), the upstream causes (C.2.h/B.7), and fetal loss (B.5) each get three numbers: overlap
with our frame, the neighbour's own frame, and the overlap among identified records -- so the scope's
routing rules can carry counts, not adjectives.

Lessons this design honours (inherited from 405 / 52)
-----------------------------------------------------
  advance-the-baseline-when-accepting-terms / frame-growth-is-not-frame-gain -- every candidate is
      priced as (baseline OR term) minus baseline, never by its own size.
  anchored-vocabulary-has-own-homonym -- "separation" is a statistics/chemistry/law term, "activity" a
      physics/biochemistry one, "migration" a cell-biology/ornithology one, "frequency" a physics one.
      Block I measures each inside our frame.
  wall-cut-on-wrong-axis -- every wall is read as a share of our frame AND of theirs.
  validate-a-null-detector-on-positives -- block A runs a written chapter's frame (C.2.c housing)
      first, so a broken counter shows up on a known-positive (405 recorded 205; 52 got 181).
  refusals-read-as-zeros -- a failed request raises Refused and is reported REFUSED. Those rows are
      missing, not zero.

Outputs literature/search-logs/a14-frame-probe-<date>.{json,md}. Counting only; no records retained,
so this is cheap and re-runnable. Budget note: ~55 requests, within the shared ~100/day OpenAlex
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
CACHE = pathlib.Path("temp/a14-frame-probe-cache.json")


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

# Outcome axis: fertility and its fecundability/conception variants. A.14's proximate outcome is the
# per-cycle conception probability and time-to-pregnancy as well as births.
OUTCOME = ('("fertility" OR "childbearing" OR "birth rate" OR "total fertility rate" '
           'OR "childlessness" OR "fecundity" OR "fecundability" OR "time to pregnancy" '
           'OR "conception probability" OR "pregnancy rate")')

# The coital-frequency topic block. NARROW is the tightest reading; A14 is the production union.
A14_NARROW = '("coital frequency" OR "frequency of intercourse" OR "sexual frequency" OR "coital rate")'
A14 = ('("coital frequency" OR "frequency of intercourse" OR "sexual frequency" OR "coital rate" '
       'OR "sexual abstinence" OR "postpartum abstinence" OR "spousal separation" '
       'OR "marital separation" OR "spousal absence")')

IDENT = ('("instrumental variable" OR "difference-in-differences" OR "differences-in-differences" '
         'OR "natural experiment" OR "regression discontinuity" OR "randomized controlled trial" '
         'OR "randomised controlled trial" OR "event study" OR "synthetic control")')

# Block C. Every construct the A.14 claim names (the completeness test) plus the generic design/driver
# words that are the free-OR inflation risk. Priced as (baseline OR term) minus baseline.
OWN_CANDIDATES = [
    "coitus", "sexual intercourse", "sexual activity", "sexual desire", "libido",
    "sexless", "sex recession", "labor migration", "spousal migration", "postpartum taboo",
    # generic inflaters to catch free-OR behaviour:
    "separation", "activity", "desire", "migration",
]

# Outcome-level calibration.
LEVELS = [
    ("realized / period fertility", '("total fertility rate" OR "birth rate" OR "completed fertility")'),
    ("fecundability / time-to-pregnancy", '("fecundability" OR "time to pregnancy" OR "conception probability")'),
    ("birth timing / seasonality", '("birth seasonality" OR "seasonality of births" OR "birth timing")'),
]

# Six walls, each read from both sides and among identified records.
WALLS = [
    ("A.2-A.6", "contraception / abortion -- the Cc/Ca indices (the explicit 'independent of contraception' wall)", "several drafted",
     '("contraception" OR "contraceptive" OR "family planning" OR "induced abortion" OR "oral contraceptive")'),
    ("A.7/C.7", "marriage timing / marriage market / union formation -- the Cm index", "drafted (marriage-market)",
     '("age at marriage" OR "marriage rate" OR "union formation" OR "proportion married" OR "nuptiality")'),
    ("A.13", "breastfeeding / lactational amenorrhoea -- the Ci index", "unstarted",
     '("breastfeeding" OR "lactational amenorrhea" OR "lactational amenorrhoea" OR "postpartum infecundability")'),
    ("A.15/A.16/B.3", "fecundity capacity -- maternal age / sperm quality / sterilising infection", "unstarted",
     '("advanced maternal age" OR "ovarian reserve" OR "sperm count" OR "semen quality" OR "tubal infertility")'),
    ("C.2.h/B.7", "upstream causes of a frequency change -- digital leisure / antidepressants", "drafted (branches 090/066)",
     '("smartphone" OR "social media" OR "screen time" OR "antidepressant" OR "SSRI")'),
    ("B.5", "fetal loss / intrauterine mortality -- conception survival, not occurrence", "drafted (branch 065)",
     '("miscarriage" OR "spontaneous abortion" OR "stillbirth" OR "fetal loss" OR "intrauterine mortality")'),
]

HOMONYMS = [
    ("separation in statistics / chemistry / law",
     '("separation of variables" OR "chromatographic separation" OR "legal separation" OR "phase separation")'),
    ("activity in physics / biochemistry",
     '("enzyme activity" OR "physical activity" OR "radioactivity" OR "optical activity")'),
    ("migration in cell biology / ornithology",
     '("cell migration" OR "bird migration" OR "electrophoretic migration")'),
    ("frequency in physics / signal processing",
     '("radio frequency" OR "resonant frequency" OR "frequency domain" OR "high frequency")'),
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
    q("A.14 narrow frame (coital/sexual frequency AND fertility+fecundability)",
      AND(A14_NARROW, OUTCOME))
    frame = q("A.14 production frame (topic union AND outcome)", AND(A14, OUTCOME))
    q("A.14 topic block with no outcome restriction", A14)

    print("C — completeness test: pricing every registered construct", flush=True)
    for term in OWN_CANDIDATES:
        cand = A14[:-1] + f' OR "{term}")'
        n = q(f"own + {term}", AND(cand, OUTCOME))
        if n is not None and frame is not None:
            R[f"gain: own + {term}"] = n - frame
    if frame is not None:
        allo = A14[:-1] + "".join(f' OR "{t}"' for t in OWN_CANDIDATES) + ")"
        n = q("A.14 block widened by ALL registered constructs", AND(allo, OUTCOME))
        if n is not None:
            R["gain: own widened by ALL"] = n - frame

    print("E — calibrating the outcome axis", flush=True)
    for label, block in LEVELS:
        q(f"level: {label}", AND(A14, block))

    print("F — identification markers inside the frame", flush=True)
    q("frame AND identified-design markers", AND(A14, OUTCOME, IDENT))

    print("H — the six walls, read from both sides", flush=True)
    for code, name, status, block in WALLS:
        q(f"wall {code} overlap with our frame", AND(A14, OUTCOME, block))
        q(f"wall {code} neighbour frame", AND(block, OUTCOME))
        q(f"wall {code} overlap AND identified", AND(A14, OUTCOME, block, IDENT))

    print("I — homonym readings inside our own frame", flush=True)
    for label, block in HOMONYMS:
        q(f"homonym: {label}", AND(A14, OUTCOME, block))

    stamp = datetime.date.today().isoformat()
    LOGDIR.mkdir(parents=True, exist_ok=True)
    payload = {"generated": stamp, "script": "source/build/goldset/89_a14_frame_probe.py",
               "api_key_present": bool(API_KEY), "counts": R,
               "refusals": [{"label": l, "error": e} for l, e in refusals]}
    (LOGDIR / f"a14-frame-probe-{stamp}.json").write_text(json.dumps(payload, indent=1))

    def cell(v):
        return "REFUSED" if v is None else f"{v:,}"

    md = [f"# A.14 coital-frequency frame probe — {stamp}", "",
          "Generated by `source/build/goldset/89_a14_frame_probe.py`. Do not edit by hand;",
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
           "from a genuine A.14 construct means the baseline was under-built; a large gain from a",
           "generic word ('separation', 'activity', 'desire', 'migration') is a free-OR inflater, not",
           "a widening.", "", "| candidate | marginal gain |", "|---|---|"]
    for label, v in R.items():
        if label.startswith("gain: "):
            md.append(f"| {label[6:]} | {v if v is not None else 'REFUSED'} |")
    md += ["", "## Walls", "",
           "Each wall: overlap with our frame, the neighbour's own frame, and the overlap among",
           "identified records. Routing is defensible where the overlap is a small share of our",
           "frame and the identified overlap is near zero.", ""]
    (LOGDIR / f"a14-frame-probe-{stamp}.md").write_text("\n".join(md) + "\n")
    print(f"\nwrote {LOGDIR}/a14-frame-probe-{stamp}.{{json,md}}")
    if refusals:
        print(f"{len(refusals)} refusal(s) — those rows are missing, not zero", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
