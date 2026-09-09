#!/usr/bin/env python3
"""
344 — C.3.d (TICK-083) stage-2 diagnostic: score every exposure term ALONE, then price the
candidate terms by MARGINAL gain rather than by their own size.

Why this exists. The 2026-09-09 candidate frame probe ranked C.3.d on a UNION frame of 762
records, built as a 6-term exposure axis AND a wide fertility outcome axis. That number ranked
the candidate; it does not say which term earned it, and TICK-081 opened with the same gap and
had to close it before scoping. Three lessons drive the design:

  anchored-vocabulary-has-own-homonym — score each anchor term alone. On A.17 one term carried
      94% of the contamination while the block looked clean.
  calibrate-the-outcome-axis-too — the outcome axis gets the same treatment. On C.3.e "parity"
      was half the frame for zero gold.
  advance-the-baseline-when-accepting-terms / frame-growth-is-not-frame-gain — a candidate term
      measured against a FROZEN baseline is credited with records earlier terms already had. On
      A.23 "emancipation" grew the frame 40% for zero gold. So candidate terms here are priced as
      (axis OR term) minus (axis): what the term adds that the axis did not already have.

The specific worry for C.3.d is not C.2.b's kind of homonym. It is that two of the six terms are
general-purpose:

  "child quality"    — Becker's term, but also childcare quality, quality of care, child health
                       service quality. The fertility restriction does NOT remove those, because
                       childcare-quality papers talk about children.
  "child investment" — shared outright with C.2.f (status competition), D.2.d (intensive
                       parenting) and C.2.b (direct costs), all three of which are DRAFTED. A
                       record inside this frame is as likely to be theirs as ours.

Two scope questions decided by numbers here rather than by argument at stage 2:

  Ruling 3 — the registry absorbs skill-biased technical change into C.3.d. If SBTC-exposure
      studies that estimate fertility effects exist at all, they are a separate search axis, not
      a routing rule, because they share no vocabulary with the Becker literature.
  Ruling 4 — the exposure is four estimands wearing one name (returns to schooling, family-size
      shocks, schooling reforms, unified-growth calibrations). Each gets its own count so the
      required-tags list at stage 2 is derived rather than guessed.

Outputs literature/search-logs/c3d-term-diagnostics-<date>.{json,md}. Counting only — no records
are retained, so this is cheap and re-runnable.

Gotchas honoured (all recorded from earlier chapters):
  - a comma inside a filter VALUE is fatal and %2C does not save it -> no commas in any term
  - a phrase beginning "not" parses as boolean NOT -> none here, and no NOT is used at all;
    marginal gain is computed by subtraction so the query language never has to express it
  - "?" in a search value is a wildcard and 200s with a misleading body -> none here
  - OpenAlex drops stopwords inside phrases, so "quantity and quality of children" == "quantity
    quality children" -> the spelling block below measures that rather than assuming it
  - this Python has no CA bundle: shell out to curl rather than urllib (refusals-read-as-zeros)
"""
import json, subprocess, sys, urllib.parse, datetime, pathlib, time

MAILTO = "shravanh@uchicago.edu"
BASE = "https://api.openalex.org/works"


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

# The six terms of the 2026-09-09 UNION axis for C.3.d, verbatim from 304.
TERMS = [
    "quantity-quality",
    "quantity quality tradeoff",
    "child quality",
    "child investment",
    "sibsize",
    "human capital of children",
]

UNION_AXIS = "(" + " OR ".join(f'"{t}"' for t in TERMS) + ")"


class Refused(Exception):
    """A failed request. Never let this reach a counter as a zero."""


def count(query: str) -> int:
    """Record count for a title_and_abstract.search filter. Raises rather than returning 0."""
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
        raise Refused(f"api error: {d.get('error')} {d.get('message','')}")
    try:
        return d["meta"]["count"]
    except (KeyError, TypeError):
        raise Refused(f"no meta.count in body: {p.stdout[:200]!r}")


def measure(label, query, rows, errors):
    """Count one query. Returns the count, or None if the request was refused."""
    try:
        try:
            n = count(query)
        except Refused as first:
            if "Rate limit" not in str(first):
                raise
            time.sleep(2.0)          # one retry, spaced past the >5-operator throttle
            n = count(query)
        rows.append((label, query, n))
        print(f"  {n:>8,}  {label}")
        time.sleep(PACE)
        return n
    except Refused as e:
        errors.append((label, str(e)))
        print(f"  REFUSED   {label}: {e}", file=sys.stderr)
        time.sleep(PACE)
        return None


def main():
    date = datetime.date.today().isoformat()
    rows, errors = [], []
    marginal = []

    print("\n== control: the channel must be alive before any zero is believed ==")
    measure("CONTROL fertility decline", '"fertility decline"', rows, errors)
    baseline = measure("CONTROL C.3.d union frame (reproduces the 09-09 number: 762)",
                       f"{UNION_AXIS} AND {OUTCOME_WIDE}", rows, errors)

    print("\n== each exposure term ALONE, fertility-restricted ==")
    for t in TERMS:
        measure(f"TERM {t}", f'"{t}" AND {OUTCOME_WIDE}', rows, errors)

    print("\n== each term alone, UNRESTRICTED (how much of it is even demographic) ==")
    for t in TERMS:
        measure(f"BARE {t}", f'"{t}"', rows, errors)

    print("\n== the axis without each of its two general-purpose terms ==")
    for drop in ("child quality", "child investment"):
        minus = "(" + " OR ".join(f'"{t}"' for t in TERMS if t != drop) + ")"
        measure(f"AXIS minus '{drop}'", f"{minus} AND {OUTCOME_WIDE}", rows, errors)

    print("\n== spelling and stopword variants of the core Becker phrase ==")
    # OpenAlex drops stopwords inside phrases, so several of these should collapse onto each
    # other. Where they do NOT, the axis is missing records for a hyphen.
    for v in ["quantity-quality tradeoff", "quantity-quality trade-off",
              "quantity quality trade off", "quantity and quality of children",
              "trade-off between quantity and quality", "child quantity",
              "quantity-quality model"]:
        measure(f"SPELLING {v}", f'"{v}" AND {OUTCOME_WIDE}', rows, errors)

    print("\n== homonym: is 'child quality' Becker's term or childcare quality? ==")
    homonym = [
        ("child quality, unrestricted", '"child quality"'),
        ("child quality INTERSECT childcare/service quality",
         '"child quality" AND ("child care" OR "childcare" OR "quality of care" OR "day care")'),
        ("child quality INTERSECT clinical/health-services",
         '"child quality" AND ("patients" OR "hospital" OR "clinical" OR "health care quality")'),
        ("child quality INTERSECT Becker vocabulary",
         '"child quality" AND ("quantity" OR "human capital" OR "fertility")'),
        ("childcare residue INSIDE the fertility-restricted frame",
         f'"child quality" AND {OUTCOME_WIDE} AND ("child care" OR "childcare" OR "quality of care")'),
        ("child investment, unrestricted", '"child investment"'),
        ("child investment INTERSECT development-aid framing",
         '"child investment" AND ("developing countries" OR "poverty" OR "cash transfer" OR "nutrition")'),
    ]
    for label, q in homonym:
        measure(f"HOMONYM {label}", q, rows, errors)

    print("\n== boundaries INSIDE the frame, against chapters that are already drafted ==")
    boundary = [
        ("C.2.f status competition / reference standard (the wall under challenge)",
         f'{UNION_AXIS} AND {OUTCOME_WIDE} AND ("income inequality" OR "status competition" '
         'OR "positional good" OR "social comparison" OR "educational arms race")'),
        ("C.2.b direct cost of children",
         f'{UNION_AXIS} AND {OUTCOME_WIDE} AND ("cost of children" OR "child cost" '
         'OR "expenditure on children" OR "cost of raising children")'),
        ("D.2.d intensive parenting norms",
         f'{UNION_AXIS} AND {OUTCOME_WIDE} AND ("intensive parenting" OR "concerted cultivation" '
         'OR "parenting norms")'),
        ("C.3.f wealth flows / value of children",
         f'{UNION_AXIS} AND {OUTCOME_WIDE} AND ("wealth flows" OR "value of children" '
         'OR "intergenerational transfer")'),
        ("A.12 twin instrument (drafted -- check its pool before building one)",
         f'{UNION_AXIS} AND {OUTCOME_WIDE} AND ("twin birth" OR "twinning" OR "twins as an instrument" '
         'OR "same-sex siblings" OR "sibling sex composition")'),
        ("Alexandra's compulsory-schooling chapter",
         f'{UNION_AXIS} AND {OUTCOME_WIDE} AND ("compulsory schooling" OR "compulsory education" '
         'OR "school leaving age" OR "child labour law" OR "child labor law")'),
    ]
    for label, q in boundary:
        measure(f"BOUNDARY {label}", q, rows, errors)

    print("\n== ruling 3: does the SBTC arm exist as a fertility literature at all? ==")
    sbtc_axis = ('("skill-biased technical change" OR "skill biased technological change" '
                 'OR "routine task" OR "routinization" OR "computerization" OR "automation")')
    measure("SBTC axis, unrestricted", sbtc_axis, rows, errors)
    measure("SBTC axis AND fertility outcome", f"{sbtc_axis} AND {OUTCOME_WIDE}", rows, errors)
    measure("SBTC axis AND fertility AND returns-to-skill framing",
            f'{sbtc_axis} AND {OUTCOME_WIDE} AND ("return to education" OR "returns to schooling" '
            'OR "skill premium" OR "college premium")', rows, errors)
    measure("SBTC axis INTERSECT the current C.3.d axis (shared vocabulary, if any)",
            f"{sbtc_axis} AND {UNION_AXIS} AND {OUTCOME_WIDE}", rows, errors)

    print("\n== ruling 4: the four estimands wearing one name ==")
    for label, q in [
        ("returns to schooling / skill premium",
         '("return to education" OR "returns to schooling" OR "returns to education" '
         'OR "skill premium" OR "college premium")'),
        ("family-size shocks (twins / sex composition)",
         '("twin birth" OR "twinning" OR "sibling sex composition" OR "same-sex siblings")'),
        ("schooling reforms as the policy variation",
         '("compulsory schooling" OR "compulsory education" OR "school leaving age" '
         'OR "education reform")'),
        ("unified growth / calibrated macro",
         '("unified growth" OR "unified growth theory" OR "growth and demographic transition" '
         'OR "calibrated overlapping generations")'),
    ]:
        measure(f"ESTIMAND {label}", f'{q} AND {OUTCOME_WIDE}', rows, errors)
        measure(f"ESTIMAND {label} INTERSECT the C.3.d axis",
                f'{q} AND {UNION_AXIS} AND {OUTCOME_WIDE}', rows, errors)

    print("\n== candidate terms, priced by MARGINAL gain over the current axis ==")
    # frame-growth-is-not-frame-gain: a candidate term's own size says nothing. What matters is
    # (axis OR term) minus (axis). No boolean NOT is used -- the subtraction does that work.
    candidates = [
        "quality-quantity",                  # the reversed hyphenation, a real journal usage
        "child human capital",
        "investment in children",
        "parental investment",
        "human capital investment",
        "sibship size",
        "family size and educational attainment",
        "dilution of resources",
        "resource dilution",
        "education-fertility tradeoff",
    ]
    if baseline is not None:
        for t in candidates:
            widened = "(" + " OR ".join(f'"{x}"' for x in TERMS + [t]) + ")"
            n = measure(f"CANDIDATE +{t} (axis OR term)", f"{widened} AND {OUTCOME_WIDE}",
                        rows, errors)
            if n is not None:
                marginal.append({"term": t, "widened": n, "baseline": baseline,
                                 "gain": n - baseline})
                print(f"           -> marginal gain {n - baseline:+,}")
    else:
        print("  SKIPPED — the baseline count was refused, so no gain can be computed. "
              "A gain measured against a missing baseline is the defect this guards against.",
              file=sys.stderr)

    out = pathlib.Path("literature/search-logs")
    out.mkdir(parents=True, exist_ok=True)
    blob = {"date": date, "script": "344_c3d_term_diagnostics.py",
            "outcome_axis_wide": OUTCOME_WIDE, "union_axis": UNION_AXIS,
            "baseline_union_frame": baseline,
            "rows": [{"label": l, "query": q, "n": n} for l, q, n in rows],
            "marginal": marginal,
            "refused": [{"label": l, "error": e} for l, e in errors]}
    (out / f"c3d-term-diagnostics-{date}.json").write_text(json.dumps(blob, indent=2))

    lines = [f"# C.3.d term diagnostics — {date}", "",
             "Generated by `source/build/goldset/344_c3d_term_diagnostics.py`. Do not edit by hand;",
             "re-run the script. Counts are OpenAlex `title_and_abstract.search` record counts, not",
             "screened pools.", "",
             f"Outcome axis (wide): `{OUTCOME_WIDE}`", "",
             f"Current C.3.d union axis: `{UNION_AXIS}`", ""]
    if marginal:
        lines += ["## Candidate terms, by marginal gain over the current axis", "",
                  f"Baseline (axis AND outcome): **{baseline:,}**. Gain is `(axis OR term) - axis`, "
                  "so a term",
                  "that only re-finds records the axis already had scores 0 however large it is "
                  "on its own.", "",
                  "| candidate term | frame with it | marginal gain |", "|---|---|---|"]
        for m in sorted(marginal, key=lambda m: -m["gain"]):
            lines.append(f"| `{m['term']}` | {m['widened']:,} | **{m['gain']:+,}** |")
        lines.append("")
    lines += ["## Every measurement", "", "| n | measurement | query |", "|---|---|---|"]
    for l, q, n in rows:
        lines.append(f"| **{n:,}** | {l} | `{q}` |")
    if errors:
        lines += ["", "## REFUSED — these are not zeros", "",
                  "A refused request is a failed request. It is recorded here rather than counted "
                  "as absence.", ""]
        lines += [f"- {l}: {e}" for l, e in errors]
    else:
        lines += ["", "No refused requests: every count above is a measurement, not a failure."]
    (out / f"c3d-term-diagnostics-{date}.md").write_text("\n".join(lines) + "\n")

    print(f"\nwrote literature/search-logs/c3d-term-diagnostics-{date}.{{json,md}}")
    if errors:
        print(f"WARNING: {len(errors)} refused request(s) — not counted as zeros", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
