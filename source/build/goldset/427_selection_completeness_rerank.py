#!/usr/bin/env python3
"""
427 — TICK-088 stage 2, part 2: re-rank the top of the candidate table LIKE FOR LIKE, by applying
the registered-construct completeness test to A.3 and to both comparators that can still beat it.

Why this exists
---------------
`404` (TICK-087) invented a test: a candidate's retrieval frame must contain the nouns its own
registered claim uses. A frame missing them is a lower bound of unknown tightness, and a candidate
can win a ranking it does not deserve. `404` applied the test to A.6 (668 -> 1,225), then compared
that corrected number against A.3's UNCORRECTED 719 and parked A.6. `405` (this ticket) applied the
test to A.3 (719 -> 1,584 on legitimation alone, 2,419 on all twelve of its own terms) and reversed
the conclusion, which resumed A.6 and parked this ticket.

Both runs were right about the test and wrong about the comparison. Each corrected ONE candidate and
ranked the result against a comparator nobody had corrected. The probe's own warning -- never rank a
corrected frame against an uncorrected one -- was restated in `404`'s docstring and then broken in
its conclusion, and `405` broke it in the other direction. Two reversals in one day is the signal
that the fix is not another single-candidate diagnostic (`fix-the-comparison-not-the-candidate`).

So: correct every candidate that can win, by one stated rule, in one run.

The rule
--------
A candidate's frame is corrected by adding the nouns its OWN REGISTERED CLAIM names, in every
spelling that OpenAlex treats as a distinct phrase, and nothing else. Terms that name the adjacent
literature rather than the claim (a project name, a theory label, a neighbouring hypothesis's
territory) are priced in a separate block and excluded from the corrected number. This is the only
rule under which the three candidates are comparable, because it is defined by each registry entry
rather than by how much a term happens to add.

Correction is monotone: adding OR-terms can only raise a count
--------------------------------------------------------------
That gives a sound shortcut, and it is the one thing `404` and `405` both missed. If a candidate's
CORRECTED frame is below every comparator's UNCORRECTED frame, it is the smallest, and no comparator
needs correcting -- the comparison errs in the safe direction. The reverse comparison (corrected
against uncorrected, corrected larger) is the unsound one, and is exactly what both earlier runs did.
Block B tests that shortcut on A.3 first. Blocks C and D correct the comparators regardless, because
TICK-088's own scope hazard is written as "if the corrected frame exceeds C.3.a's 1,808" -- a
corrected-against-uncorrected test that has to be rewritten with a real number on both sides, and
because PI call 3 (TICK-087) needs the like-for-like table before `304` is fixed under TICK-080.

Who can still win
-----------------
From `candidate-frame-probe-2026-09-13`, the bracketed block ranks A.6 680, A.3 727, C.3.a 1,811,
D.2.c 2,024, C.2.e 2,240, C.4.a 2,417, then 2,817 and up. A.6 is no longer a candidate -- TICK-087
is drafted. A.3's corrected frame is bounded above by 2,419 (`405`, all own terms), so any candidate
whose UNCORRECTED frame already exceeds 2,419 cannot win under a monotone correction and is not
measured here: C.2.e and everything from A.19 up are out. C.4.a at 2,417 is inside that bound by two
records, which is not a margin -- it is reproduced in block A as a bound check and excluded in the
conclusion only if A.3 lands below it.

That leaves C.3.a and D.2.c as the two comparators to correct.

What the claim-noun gaps are, per candidate
-------------------------------------------
A.3   "diffusion of information about and legitimation of birth control". The frame carries neither
      legitimation nor any information/knowledge noun. It also says "linguistic, religious, and
      social networks", but those are channels, and the registry gives channels to A.20, whose note
      says it absorbs `social-network-peer-effects`, `ideational-diffusion-mass-media` and
      `linguistic-cultural-boundaries-princeton`. `405` priced the channel block; block G adds only
      the religious channel, which `405` missed and which is contested three ways (A.20's boundaries,
      D.1.a's religiosity).
C.3.a "production technology across hunter-gatherer, pastoralist, and agriculturalist economies
      ... child labor value and dependency length". The frame is seven agrarian-household phrases:
      no hunter-gatherer, no forager, no pastoralist, no agriculturalist, no child-labour-value and
      no dependency noun. This is a PM-only entry whose claim is explicitly CROSS-production-system,
      and two of its three named systems are absent from the block that selected it. Boserup,
      Kaplan, Sellen-Mace and Gibson-Mace are all anthropological.
D.2.c "preference for sons sustains higher fertility through continued childbearing until a son is
      born". The frame carries "son preference" but not "preference for sons" -- a phrase search
      does not fold word order -- and no noun for the stopping behaviour beyond "differential
      stopping".

Size is not the only input, and A.6 is the reason
-------------------------------------------------
A.6 won on size and `405` then showed it was the worst candidate on estimability: 148 records of
HIV-stigma contamination, 58 with realized-fertility vocabulary against A.3's 154. The chapter it
produced is an UNEVALUATED verdict on one contestable record. Block E measures identification
markers and outcome level on each CORRECTED frame, and block F the homonym load, so the pick is made
on screening cost AND on the chance of an estimable parameter (`smallest-is-not-cheapest`).

Lessons this design honours
---------------------------
  advance-the-baseline-when-accepting-terms — every term is priced as (baseline OR term) minus
      baseline, never by its own size.
  validate-a-null-detector-on-positives — block A runs a written chapter's frame first, and
      reproduces all four recorded figures so index drift is visible rather than silent.
  wall-cut-on-wrong-axis — the C.3.f and C.2.g walls on C.3.a's new terms are read inside the frame.
  refusals-read-as-zeros — a failed request raises and reports REFUSED. Those rows are missing,
      not zero.

Outputs literature/search-logs/selection-completeness-rerank-<date>.{json,md}. Counting only; no
records are retained, so this is cheap and re-runnable.

OpenAlex hazards honoured
-------------------------
  - a comma inside a filter VALUE is fatal and %2C does not save it -> no commas in any term
  - a phrase beginning "not" parses as boolean NOT -> none here
  - "?" is a wildcard returning 200 with a misleading body -> none here
  - hyphens fold and stopwords drop inside phrases, so "hunter-gatherer" and "hunter gatherer" are
    one term; word ORDER does not fold, so "son preference" and "preference for sons" are two
  - an AND-containing arm cannot be OR'd into a union -> every arm is pulled separately
  - this Python has no CA bundle: shell out to curl rather than urllib

Usage: python3 source/build/goldset/427_selection_completeness_rerank.py
"""
import json, subprocess, sys, urllib.parse, datetime, pathlib, time

MAILTO = "shravanh@uchicago.edu"
BASE = "https://api.openalex.org/works"
LOGDIR = pathlib.Path("literature/search-logs")
CACHE = pathlib.Path("temp/selection-completeness-rerank-cache.json")


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

OUTCOME_WIDE = ('("fertility" OR "childbearing" OR "birth rate" OR "total fertility rate" '
                'OR "family size" OR "number of children")')

IDENT = ('("instrumental variable" OR "difference-in-differences" OR "differences-in-differences" '
         'OR "natural experiment" OR "regression discontinuity" OR "randomized controlled trial" '
         'OR "randomised controlled trial" OR "event study" OR "synthetic control")')

QUAL = '("qualitative" OR "focus group" OR "in-depth interview" OR "ethnographic")'
REALIZED = ('("total fertility rate" OR "completed fertility" OR "birth rate" '
            'OR "marital fertility")')

# Pass-4 union blocks, verbatim from 304, so every reproduction is exact.
A3 = ('("diffusion of fertility control" OR "ideational change" OR "fertility diffusion" '
      'OR "innovation diffusion" OR "spread of birth control" OR "social learning" '
      'OR "cultural transmission" OR "social contagion" OR "spatial diffusion" '
      'OR "family limitation")')
C3A = ('("mode of production" OR "agricultural household" OR "peasant household" '
       'OR "farm household" OR "subsistence agriculture" OR "land tenure" OR "agrarian society")')
D2C = ('("son preference" OR "sex selection" OR "missing women" OR "sex preference" '
       'OR "gender preference" OR "sex ratio at birth" OR "sex-selective abortion" '
       'OR "daughter aversion" OR "differential stopping")')
C4A = ('("land constraints" OR "land scarcity" OR "land availability" OR "Malthusian" '
       'OR "preventive check" OR "positive check" OR "population pressure" OR "land pressure" '
       'OR "carrying capacity" OR "land inheritance" OR "subsistence crisis")')

RECORDED = {"A.3": 727, "C.3.a": 1811, "D.2.c": 2024, "C.4.a": 2417}

# The full bracketed block from `candidate-frame-probe-2026-09-13`, in its recorded order. Needed by
# the conclusion: monotone correction means any candidate whose UNCORRECTED frame already exceeds the
# winner's CORRECTED frame is excluded without being measured, which is what makes this run a
# complete ranking over the block rather than a comparison of three. A.6 is dropped -- TICK-087's
# chapter is drafted, so it is no longer a candidate.
BRACKETED = [
    ("A.3", "diffusion-of-fertility-control", 727),
    ("C.3.a", "agricultural-mode-of-production", 1811),
    ("D.2.c", "son-preference-cultural", 2024),
    ("C.2.e", "female-wage-opportunity-cost", 2240),
    ("C.4.a", "land-and-resource-constraints-malthusian", 2417),
    ("A.19", "intergenerational-transmission-fertility", 2817),
    ("A.4", "induced-abortion-access", 3432),
    ("C.2.d", "tax-and-transfer-pronatalism", 3634),
    ("C.1.a", "income-effect-normal-good", 6482),
]

# ---------------------------------------------------------------------- the claim-noun gap, per code
# Terms named by the registry claim and absent from the pass-4 block. Nominal and spelling variants
# of a claim noun count as the same noun ("legitimation"/"legitimacy"); word-order variants must be
# listed separately because a phrase search does not fold them.
CLAIM_GAPS = {
    "A.3": ["legitimation", "legitimacy", "knowledge of contraception",
            "awareness of contraception", "information diffusion", "birth control knowledge",
            "adoption of birth control"],
    "C.3.a": ["hunter-gatherer", "forager", "foraging", "pastoralist", "pastoralism",
              "agriculturalist", "production technology", "child labor value",
              "child labour value", "dependency ratio", "length of dependency"],
    "D.2.c": ["preference for sons", "desire for a son", "boy preference",
              "male child preference", "son targeting", "stopping rule"],
}

# Adjacent to the claim but NOT named by it. Priced so the excluded widening is visible as a number
# rather than as a judgement call, and excluded from every corrected frame.
ADJACENT = {
    "A.3": ["innovation adoption", "calculus of conscious choice", "European Fertility Project",
            "contraceptive diffusion", "fertility transition onset"],
    "C.3.a": ["horticultural", "shifting cultivation", "swidden", "plough agriculture",
              "hoe agriculture", "agricultural intensification"],
    "D.2.c": ["sex composition", "gender composition", "sex ratio", "fertility stopping"],
}

# The rule leaves ONE judgement open, and it is worth 4,409 records on C.3.a alone: is a term a
# morphological variant of a claim noun (in) or a SYNONYM for it (arguable), and is it a construct
# another registry entry owns (out)? STRICT drops both kinds; the sets above are the BROAD reading.
# Both are reported, because a ranking that survives the judgement is worth more than one that
# needs it settled first (`report-the-sensitivity-not-the-verdict`).
#   C.3.a  "forager"/"foraging" are synonyms for the claim's "hunter-gatherer", not variants of it,
#          and "dependency ratio" is A.9's construct (population age structure), not the claim's
#          "dependency length" -- which OpenAlex prices at +0 anyway.
#   A.3, D.2.c  every claim-gap term is a morphological or word-order variant of a noun in the
#          claim itself, so STRICT and BROAD coincide and the frames are identical by construction.
STRICT_GAPS = {
    "A.3": CLAIM_GAPS["A.3"],
    "C.3.a": ["hunter-gatherer", "pastoralist", "pastoralism", "agriculturalist",
              "production technology", "child labor value", "child labour value",
              "length of dependency"],
    "D.2.c": CLAIM_GAPS["D.2.c"],
}

# A.3's channel terms are A.20's registered territory. `405` priced nine of them; the religious
# channel is in A.3's claim and was missed, and it is contested by A.20 and D.1.a at once.
A3_RELIGIOUS = ["religious denomination", "religious affiliation", "denominational boundary"]

# Walls that C.3.a's NEW terms could breach. Read inside the corrected frame, not beside it.
C3A_WALLS = [
    ("C.3.f", "wealth flows reversal — a drafted chapter, and it owns value-of-children",
     '("wealth flows" OR "value of children" OR "intergenerational transfer" OR "old age support")'),
    ("C.3.b", "child labour and compulsory schooling — a written chapter",
     '("child labour" OR "child labor" OR "compulsory schooling" OR "school enrollment")'),
    ("C.2.g", "urbanization and residential shift — an unstarted candidate",
     '("urbanization" OR "urbanisation" OR "rural-urban migration" OR "urban residence")'),
    ("C.4.a", "land and resource constraints — an unstarted candidate sharing land vocabulary",
     '("Malthusian" OR "population pressure" OR "carrying capacity" OR "land scarcity")'),
    ("A.9", "population age structure — it owns dependency-ratio, which is why STRICT drops it",
     '("dependency ratio" OR "population age structure" OR "demographic momentum")'),
]

HOMONYMS = {
    "C.3.a": [("mode of production in Marxist political economy rather than demography",
               '("capitalism" OR "class struggle" OR "Marxist" OR "social formation")'),
              ("farm-household vocabulary in agricultural labour supply rather than fertility",
               '("labor supply" OR "labour supply" OR "crop yield" OR "technical efficiency")'),
              ("forager vocabulary in animal behaviour rather than human demography",
               '("optimal foraging" OR "foraging behaviour" OR "ant" OR "bee" OR "predator")')],
    "D.2.c": [("sex selection in animal and plant breeding",
               '("animal breeding" OR "livestock" OR "semen sexing" OR "poultry")'),
              ("sex ratio in evolutionary biology rather than human demography",
               '("Fisher" OR "sex allocation" OR "insect" OR "brood")'),
              ("missing women in labour-force participation rather than in mortality",
               '("labor force participation" OR "labour force participation" OR "gender gap in employment")')],
}


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


def widen(block: str, terms) -> str:
    """OR the terms into an existing parenthesised phrase block."""
    return block[:-1] + "".join(f' OR "{t}"' for t in terms) + ")"


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

    BLOCKS = {"A.3": A3, "C.3.a": C3A, "D.2.c": D2C}

    print("A — control, and all four recorded frames reproduced live", flush=True)
    q("control: C.2.c housing frame (a written chapter)",
      AND('("house price" OR "housing cost" OR "house prices")', OUTCOME_WIDE))
    base = {}
    for code, block in [("A.3", A3), ("C.3.a", C3A), ("D.2.c", D2C), ("C.4.a", C4A)]:
        base[code] = q(f"reproduce {code} pass-4 union frame (09-13 recorded {RECORDED[code]:,})",
                       AND(block, OUTCOME_WIDE))

    corrected = {}
    for code in ("A.3", "C.3.a", "D.2.c"):
        block, b = BLOCKS[code], base[code]
        print(f"B/C/D — {code}: pricing the nouns its own registered claim names", flush=True)
        for term in CLAIM_GAPS[code]:
            n = q(f"{code} claim-gap + {term}", AND(widen(block, [term]), OUTCOME_WIDE))
            if n is not None and b is not None:
                R[f"gain: {code} claim-gap + {term}"] = n - b
        n = q(f"{code} CORRECTED — block widened by ALL its claim nouns",
              AND(widen(block, CLAIM_GAPS[code]), OUTCOME_WIDE))
        corrected[code] = n
        if n is not None and b is not None:
            R[f"gain: {code} corrected vs reproduced"] = n - b

        print(f"      {code}: pricing the adjacent terms its claim does NOT name (excluded)",
              flush=True)
        for term in ADJACENT[code]:
            n2 = q(f"{code} adjacent + {term}", AND(widen(block, [term]), OUTCOME_WIDE))
            if n2 is not None and b is not None:
                R[f"gain: {code} adjacent + {term}"] = n2 - b
        n2 = q(f"{code} block widened by ALL adjacent terms (not the corrected frame)",
               AND(widen(block, ADJACENT[code]), OUTCOME_WIDE))
        if n2 is not None and b is not None:
            R[f"gain: {code} all adjacent vs reproduced"] = n2 - b

    print("E — estimability, measured on each CORRECTED frame", flush=True)
    for code in ("A.3", "C.3.a", "D.2.c"):
        cframe = widen(BLOCKS[code], CLAIM_GAPS[code])
        q(f"{code} corrected AND identified-design markers", AND(cframe, OUTCOME_WIDE, IDENT))
        q(f"{code} corrected AND realized-fertility vocabulary", AND(cframe, OUTCOME_WIDE, REALIZED))
        q(f"{code} corrected AND qualitative markers", AND(cframe, OUTCOME_WIDE, QUAL))

    print("F — homonym load inside each corrected comparator frame", flush=True)
    for code in ("C.3.a", "D.2.c"):
        cframe = widen(BLOCKS[code], CLAIM_GAPS[code])
        for label, block in HOMONYMS[code]:
            q(f"{code} homonym: {label}", AND(cframe, OUTCOME_WIDE, block))

    print("G — C.3.a's new terms against the walls they could breach", flush=True)
    c3a_c = widen(C3A, CLAIM_GAPS["C.3.a"])
    for code, name, block in C3A_WALLS:
        q(f"C.3.a corrected: wall {code} overlap ({name})", AND(c3a_c, OUTCOME_WIDE, block))
        q(f"C.3.a corrected: wall {code} overlap AND identified",
          AND(c3a_c, OUTCOME_WIDE, block, IDENT))

    print("H — A.3's religious channel, which 405 missed", flush=True)
    for term in A3_RELIGIOUS:
        n = q(f"A.3 channel + {term}", AND(widen(A3, [term]), OUTCOME_WIDE))
        if n is not None and base["A.3"] is not None:
            R[f"gain: A.3 channel + {term}"] = n - base["A.3"]
    n = q("A.3 block widened by ALL religious-channel terms (A.20 territory — not the corrected frame)",
          AND(widen(A3, A3_RELIGIOUS), OUTCOME_WIDE))
    if n is not None and base["A.3"] is not None:
        R["gain: A.3 all religious-channel vs reproduced"] = n - base["A.3"]

    print("I — the same correction under the STRICT reading of the rule", flush=True)
    strict = {}
    for code in ("A.3", "C.3.a", "D.2.c"):
        if STRICT_GAPS[code] == CLAIM_GAPS[code]:
            strict[code] = corrected[code]
            print(f"  {'(broad)':>8}  {code} STRICT == BROAD by construction — no query spent",
                  flush=True)
            continue
        strict[code] = q(f"{code} CORRECTED (STRICT) — synonyms and other entries' constructs dropped",
                         AND(widen(BLOCKS[code], STRICT_GAPS[code]), OUTCOME_WIDE))

    # ------------------------------------------------------------------------------- the conclusion
    stamp = datetime.date.today().isoformat()
    LOGDIR.mkdir(parents=True, exist_ok=True)
    payload = {"generated": stamp,
               "script": "source/build/goldset/427_selection_completeness_rerank.py",
               "api_key_present": bool(API_KEY),
               "recorded_2026_09_13": RECORDED,
               "reproduced": base, "corrected_broad": corrected, "corrected_strict": strict,
               "counts": R,
               "refusals": [{"label": l, "error": e} for l, e in refusals]}
    (LOGDIR / f"selection-completeness-rerank-{stamp}.json").write_text(json.dumps(payload, indent=1))

    def cell(v):
        return "REFUSED" if v is None else f"{v:,}"

    md = [f"# Selection re-rank under the completeness test — {stamp}", "",
          "Generated by `source/build/goldset/427_selection_completeness_rerank.py`. Do not edit by",
          "hand; re-run the script.", "",
          "OpenAlex `title_and_abstract.search` record counts. They size a *retrieval frame*, not an",
          "evidence base: no production query has been run, no anchor resolved and no record",
          "screened. The point of this run is the **comparison**, not any single number — `404` and",
          "`405` each corrected one candidate and ranked it against an uncorrected comparator, and",
          "reversed each other inside a day.", "",
          "**The rule.** A candidate's frame is corrected by adding the nouns its own registered",
          "claim names, in every spelling OpenAlex treats as a distinct phrase, and nothing else.",
          "Terms adjacent to the claim but not named by it are priced separately and excluded.", ""]
    if refusals:
        md += [f"**{len(refusals)} request(s) REFUSED.** Those rows are missing, not zero.", ""]

    md += ["## The ranking", "",
           "| code | slug | recorded 09-13 | reproduced | corrected (broad) | **corrected (strict)** |",
           "|---|---|---|---|---|---|"]
    SLUG = {"A.3": "`diffusion-of-fertility-control`",
            "C.3.a": "`agricultural-mode-of-production`",
            "D.2.c": "`son-preference-cultural`",
            "C.4.a": "`land-and-resource-constraints-malthusian`"}
    for code in ("A.3", "C.3.a", "D.2.c"):
        c, b = corrected.get(code), base.get(code)
        md.append(f"| {code} | {SLUG[code]} | {RECORDED[code]:,} | {cell(b)} | {cell(c)} | "
                  f"**{cell(strict.get(code))}** |")
    md.append(f"| C.4.a | {SLUG['C.4.a']} | {RECORDED['C.4.a']:,} | {cell(base.get('C.4.a'))} | "
              "not corrected | bound check only |")
    live_s = {k: v for k, v in strict.items() if v is not None}
    win = min(live_s, key=live_s.get) if live_s else None
    md += ["", "Correction is monotone — adding OR-terms can only raise a count — so a candidate",
           "whose **corrected** frame sits below every comparator's **uncorrected** frame is the",
           "smallest without the comparators being corrected at all. That is the sound direction of",
           "the comparison both earlier runs got backwards.", ""]

    if win:
        wn = live_s[win]
        md += ["", "## Conclusion", "",
               f"**{win} (`{dict((c, sl) for c, sl, _ in BRACKETED)[win]}`) is the smallest candidate "
               f"at {wn:,},** on the first comparison in which every candidate that could win was "
               "corrected by the same rule.", "",
               "Two things are worth separating. The corrected numbers move the *ranking*, not just",
               "the counts: the candidates that led the recorded table led it on frames that omitted",
               "their own claim's nouns, and the winner here is the one whose frame was closest to",
               "honest already —"]
        moves = [f"{code} {base[code]:,} → {strict[code]:,} ({(strict[code] - base[code]) / base[code]:+.0%})"
                 for code in ("A.3", "C.3.a", "D.2.c") if base.get(code) and strict.get(code)]
        md += [", ".join(moves) + " — so the test rewards a frame that already said what its",
               "hypothesis claims.", "",
               "**The rest of the block is closed out without being measured.** Correction can only",
               "raise a count, so any candidate whose *uncorrected* frame already exceeds",
               f"{wn:,} cannot win:", "",
               "| code | slug | uncorrected 09-13 | status under monotonicity |", "|---|---|---|---|"]
        for code, slug, n in BRACKETED:
            if code in strict:
                verdict = "**smallest**" if code == win else f"corrected to {strict[code]:,}"
            elif n > wn:
                verdict = f"excluded — {n:,} > {wn:,} before any correction"
            else:
                verdict = "NOT CLOSED — measure it"
            md.append(f"| {code} | `{slug}` | {n:,} | {verdict} |")
        md += ["", "### The unbracketed block", "",
               "`304`'s second table is not ranked here, and its pass-1 counts cannot be compared",
               f"with {wn:,} — seven sit below it (A.20 203, C.2.h 143, C.2.a 256, D.1.c 224,",
               "A.14 314, A.13 454, A.9 507) but each is a single-vocabulary lower bound, and the",
               "probe's standing warning is never to rank across the two blocks without widening the",
               "lower one first.", "",
               "Their *second* vocabularies do bear on it, and in the favourable direction. Each of",
               "those seven has a pass-2 count already measured at 3,050 to 14,497, and pass 2 runs a",
               f"WIDER block against the NARROWER outcome axis — so both moves from there to a pass-4",
               "union frame can only raise the count, and all seven would clear",
               f"{wn:,} several times over. The one leak is that a union block is curated rather than",
               "accumulated, so a pass-2 term can be dropped on the way. That makes this a strong",
               "presumption and not a measurement, which is the distinction `304` exists to enforce:",
               "**if any of those seven is to be retired as a candidate, it needs a pass-4 frame of",
               "its own, and that is a `304` change under TICK-080, not a conclusion of this run.**", ""]

    md += ["## Every measurement", "", "| measurement | n |", "|---|---|"]
    for label, v in R.items():
        if not label.startswith("gain: "):
            md.append(f"| {label} | {cell(v)} |")
    md += ["", "## Marginal gain of candidate terms", "",
           "Priced as (baseline OR term) minus baseline, never by the term's own size. Adjacent and",
           "channel terms are priced for the record and are **not** in any corrected frame.", "",
           "| candidate | marginal gain |", "|---|---|"]
    for label, v in R.items():
        if label.startswith("gain: "):
            md.append(f"| {label[6:]} | {v if v is not None else 'REFUSED'} |")
    (LOGDIR / f"selection-completeness-rerank-{stamp}.md").write_text("\n".join(md) + "\n")
    print(f"\nwrote {LOGDIR}/selection-completeness-rerank-{stamp}.{{json,md}}")

    live = {k: v for k, v in strict.items() if v is not None}
    if live:
        win = min(live, key=live.get)
        print(f"\nsmallest corrected frame: {win} at {live[win]:,}")
        others = [base[c] for c in ("A.3", "C.3.a", "D.2.c", "C.4.a")
                  if c != win and base.get(c) is not None]
        if others and live[win] < min(others):
            print(f"  and it is below every comparator's UNCORRECTED frame ({min(others):,}), "
                  "so the ranking holds under monotonicity alone")
    if refusals:
        print(f"{len(refusals)} refusal(s) — those rows are missing, not zero", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
