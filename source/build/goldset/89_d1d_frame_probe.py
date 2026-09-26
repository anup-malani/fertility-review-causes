#!/usr/bin/env python3
"""
89 (d1d) — D.1.d (TICK-093) stage-3 frame probe: confirm or refute that nationalist and pronatalist
ideology is the next-smallest genuinely-unstarted candidate, and run the registered-construct
completeness test the A.6/A.3 episode made mandatory before any search spend.

Why this exists
---------------
D.1.d was picked as the next-smallest *unstarted* hypothesis on TICK-092's extended scouting count
(production frame = 1,720, next after D.2.c's 1,134 and below the ~1,808 bar: A.20 1,968; A.19 2,414;
B.2 4,475). But that scout was *partitioned* — biological-only on TICK-091, cultural/demographic-only on
TICK-092 — and never compared the economic C-section candidates (C.2.d, C.2.a, C.6.b) against D.1.d.
TICK-087 (A.6) and TICK-088 (A.3) were both mis-ranked because their selecting frames were priced wrong —
A.6 omitted its own registered construct ("legitimation"); A.3 was charged a neighbour's channel terms and
a free-standing OR. This probe applies the corrected rule to D.1.d *before* spending screen budget: price
the frame against its OWN conjoined construct set, read every wall from both sides, and count the homonym
load inside the frame.

The nationalist-pronatalism-specific hazard
-------------------------------------------
The topic sits behind two heavy homonyms. "national fertility (rate)" means a country's TFR, not
nationalist ideology; "population policy" is a catch-all that sweeps in C.2.d transfers, A.4 abortion
bans, and family planning. And the topic is bundled in every famous episode with money (C.2.d) and often
with coercion (A.4 — Romania's Decree 770 was an abortion ban, not persuasion). The completeness test
must show that the honest D.1.d frame is a *pronatalist-ideology* frame, and that folding a free-standing
"nationalism", "national", or "population policy" OR would annex a neighbour literature rather than widen
D.1.d. That is exactly the free-OR inflation the A.3 park was built on.

The registered-construct completeness test
------------------------------------------
Block C prices every noun the D.1.d claim names (pronatalist ideology, patriotic/national duty framing,
propaganda/campaigns, honorific awards for large families) as (baseline OR term) minus baseline. A large
marginal gain from a term that is genuinely D.1.d's means the baseline frame was under-built and the term
belongs in it (frame grows, but honestly). A large gain from a generic word conjoined to nothing --
"nationalism", "national", "population policy", "patriotism", "propaganda" -- is the free-OR inflater,
reported as such, not folded into the frame.

The walls are read from both sides
-----------------------------------
Tax/transfer pronatalism (C.2.d, LOAD-BEARING), abortion/contraception (A.4/A.2, LOAD-BEARING coercion),
secularization/individualism (D.1.a), religiosity (D.1.a arm), cultural-diffusion channels (A.20), and
old-age security as an economic root/motive (C.3.c) each get three numbers: overlap with our frame, the
neighbour's own frame, and the overlap among identified records -- so the scope's routing rules can carry
counts, not adjectives.

Lessons this design honours (inherited from 89_d2c / 89_a14 / 405 / 52)
----------------------------------------------------------------------
  advance-the-baseline-when-accepting-terms / frame-growth-is-not-frame-gain -- every candidate is
      priced as (baseline OR term) minus baseline, never by its own size.
  anchored-vocabulary-has-own-homonym -- "national" is a national-income/nationality/nationalization
      token, "natal" a medical (pre-/post-/neo-natal) one, "population policy" a family-planning
      catch-all. Block I measures each inside our frame.
  wall-cut-on-wrong-axis -- every wall is read as a share of our frame AND of theirs.
  validate-a-null-detector-on-positives -- block A runs a written chapter's frame (C.2.c housing)
      first, so a broken counter shows up on a known-positive (405 recorded 205; 52 got 181; 89_d2c 170).
  refusals-read-as-zeros -- a failed request raises Refused and is reported REFUSED. Those rows are
      missing, not zero.

Outputs literature/search-logs/d1d-frame-probe-<date>.{json,md}. Counting only; no records retained.

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
CACHE = pathlib.Path("temp/d1d-frame-probe-cache.json")


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

# Outcome axis: fertility only, IDENTICAL to 89_d2c, so the control-housing frame reproduces (~170-205)
# and the D.1.d production frame is comparable across probes.
OUTCOME = ('("fertility" OR "childbearing" OR "birth rate" OR "total fertility rate" '
           'OR "childlessness" OR "fecundity" OR "time to pregnancy" OR "subfertility" '
           'OR "infertility")')

# The nationalist-pronatalist-ideology topic block. NARROW is the tightest reading; D1D is the production
# union. Only the genuinely D.1.d-specific phrases enter the base frame; the homonym-heavy words
# (nationalism, national, population policy, patriotism, propaganda) are priced in the completeness test
# and enter the frame only if they earn it there.
# Two terms were tested and EXCLUDED from the honest frame by the first probe run (2026-09-26):
#   - "natalism": 2,677 AND-fertility, but 602 (22%) overlap the perinatal medical literature
#     (neonatal/prenatal/postnatal) via `natal` stemming -- a homonym leak, not a widening. Dropped;
#     it is priced in OWN_CANDIDATES below to keep the exclusion visible.
#   - "pronatal": 370 AND-fertility, identical to "pronatalism" (the hyphen in "pro-natal" folds), so it
#     is redundant and adds nothing. Dropped.
# The clean frame (pronatalist core + "natalist", which is clean at only 2 medical overlaps, + the
# specific-episode phrases) is 1,751 -- at/just below the ~1,808 bar and matching TICK-092's 1,720 scout.
D1D_NARROW = '("pronatalism" OR "pronatalist")'
D1D = ('("pronatalism" OR "pronatalist" OR "natalist" '
       'OR "pronatalist policy" OR "pronatalist propaganda" OR "demographic nationalism" '
       'OR "cult of motherhood" OR "battle for births")')

IDENT = ('("instrumental variable" OR "difference-in-differences" OR "differences-in-differences" '
         'OR "natural experiment" OR "regression discontinuity" OR "randomized controlled trial" '
         'OR "randomised controlled trial" OR "event study" OR "synthetic control")')

# Block C. Every construct the D.1.d claim names (the completeness test) plus the generic words that are
# the free-OR inflation risk. Priced as (baseline OR term) minus baseline.
OWN_CANDIDATES = [
    # genuine D.1.d constructs to test for inclusion:
    "patriotic duty", "national duty", "duty to the nation", "population campaign",
    "motherhood medal", "mother heroine", "population politics",
    # generic / homonym-heavy inflaters to catch free-OR behaviour (and "natalism", the medical-natal
    # stemming leak found on the first run and excluded from the frame above):
    "natalism", "nationalism", "nationalist", "patriotism", "national", "population policy", "propaganda",
]

# Outcome-level calibration.
LEVELS = [
    ("realized / period fertility", '("total fertility rate" OR "birth rate" OR "completed fertility")'),
    ("fertility intentions / desired family size", '("fertility intentions" OR "desired family size" OR "number of children")'),
    ("period vs quantum framing", '("period fertility" OR "tempo effect" OR "quantum")'),
]

# Six walls, each read from both sides and among identified records.
WALLS = [
    ("C.2.d", "tax and transfer pronatalism -- the money the ideology is bundled with (LOAD-BEARING)", "unstarted",
     '("child allowance" OR "baby bonus" OR "parental leave" OR "child benefit" OR "family allowance" OR "childcare subsidy" OR "tax credit")'),
    ("A.4/A.2", "abortion / contraception -- coercive restriction of fertility control (Romania 1966), not persuasion (LOAD-BEARING)", "several drafted",
     '("induced abortion" OR "abortion access" OR "abortion ban" OR "contraception" OR "contraceptive" OR "family planning")'),
    ("D.1.a", "postmaterialism / individualism / secularization -- the diffuse opposite-signed value shift", "branch 062 (unmerged)",
     '("secularization" OR "secularisation" OR "individualism" OR "postmaterialism" OR "post-materialism" OR "value change")'),
    ("D.1.a-relig", "religiosity as a diffuse value (the secularization arm)", "branch 062 (unmerged)",
     '("religiosity" OR "religious" OR "religion" OR "church attendance")'),
    ("A.20", "cultural diffusion channels -- media/networks regardless of message content", "unstarted",
     '("mass media" OR "social network" OR "television" OR "radio" OR "diffusion of innovations")'),
    ("C.3.c", "old-age security -- an economic root of / state motive for wanting births", "done (OAS pilot)",
     '("old-age security" OR "pension" OR "old age support" OR "intergenerational transfers")'),
]

HOMONYMS = [
    ("national income / nationality / nationalization (not nationalism)",
     '("national income" OR "nationality" OR "nationalization" OR "nationalized")'),
    ("natal in medicine (pre-/post-/neo-/ante-natal)",
     '("prenatal care" OR "postnatal" OR "neonatal" OR "antenatal")'),
    ("population policy as a family-planning catch-all",
     '("population control" OR "family planning program" OR "birth control program")'),
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
    q("control: C.2.c housing frame (a written chapter; 405 recorded 205, 52 got 181, 89_d2c 170)",
      AND('("house price" OR "housing cost" OR "house prices")',
          '("fertility" OR "childbearing" OR "birth rate" OR "total fertility rate" OR "childlessness")'))
    q("D.1.d narrow frame (pronatalism core AND fertility)",
      AND(D1D_NARROW, OUTCOME))
    frame = q("D.1.d production frame (topic union AND outcome)", AND(D1D, OUTCOME))
    q("D.1.d topic block with no outcome restriction", D1D)

    print("C — completeness test: pricing every registered construct", flush=True)
    for term in OWN_CANDIDATES:
        cand = D1D[:-1] + f' OR "{term}")'
        n = q(f"own + {term}", AND(cand, OUTCOME))
        if n is not None and frame is not None:
            R[f"gain: own + {term}"] = n - frame
    if frame is not None:
        allo = D1D[:-1] + "".join(f' OR "{t}"' for t in OWN_CANDIDATES) + ")"
        n = q("D.1.d block widened by ALL registered constructs", AND(allo, OUTCOME))
        if n is not None:
            R["gain: own widened by ALL"] = n - frame

    print("E — calibrating the outcome axis", flush=True)
    for label, block in LEVELS:
        q(f"level: {label}", AND(D1D, block))

    print("F — identification markers inside the frame", flush=True)
    q("frame AND identified-design markers", AND(D1D, OUTCOME, IDENT))

    print("H — the six walls, read from both sides", flush=True)
    for code, name, status, block in WALLS:
        q(f"wall {code} overlap with our frame", AND(D1D, OUTCOME, block))
        q(f"wall {code} neighbour frame", AND(block, OUTCOME))
        q(f"wall {code} overlap AND identified", AND(D1D, OUTCOME, block, IDENT))

    print("I — homonym readings inside our own frame", flush=True)
    for label, block in HOMONYMS:
        q(f"homonym: {label}", AND(D1D, OUTCOME, block))

    stamp = datetime.date.today().isoformat()
    LOGDIR.mkdir(parents=True, exist_ok=True)
    payload = {"generated": stamp, "script": "source/build/goldset/89_d1d_frame_probe.py",
               "api_key_present": bool(API_KEY), "counts": R,
               "refusals": [{"label": l, "error": e} for l, e in refusals]}
    (LOGDIR / f"d1d-frame-probe-{stamp}.json").write_text(json.dumps(payload, indent=1))

    def cell(v):
        return "REFUSED" if v is None else f"{v:,}"

    md = [f"# D.1.d nationalist/pronatalist-ideology frame probe — {stamp}", "",
          "Generated by `source/build/goldset/89_d1d_frame_probe.py`. Do not edit by hand;",
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
           "from a genuine D.1.d construct means the baseline was under-built; a large gain from a",
           "generic word ('nationalism', 'national', 'population policy', 'patriotism', 'propaganda')",
           "is a free-OR inflater that annexes a neighbour literature, not a widening.", "",
           "| candidate | marginal gain |", "|---|---|"]
    for label, v in R.items():
        if label.startswith("gain: "):
            md.append(f"| {label[6:]} | {v if v is not None else 'REFUSED'} |")
    md += ["", "## Walls", "",
           "Each wall: overlap with our frame, the neighbour's own frame, and the overlap among",
           "identified records. Routing is defensible where the overlap is a small share of our",
           "frame and the identified overlap is near zero. C.2.d (transfers) and A.4/A.2 (abortion",
           "bans) are load-bearing: the ideology is bundled with the money in every famous episode,",
           "and Romania 1966 is a coercion effect, not a persuasion effect.", ""]
    (LOGDIR / f"d1d-frame-probe-{stamp}.md").write_text("\n".join(md) + "\n")
    print(f"\nwrote {LOGDIR}/d1d-frame-probe-{stamp}.{{json,md}}")
    if refusals:
        print(f"{len(refusals)} refusal(s) — those rows are missing, not zero", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
