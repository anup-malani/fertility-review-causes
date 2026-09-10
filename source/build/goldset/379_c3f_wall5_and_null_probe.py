#!/usr/bin/env python3
"""
379 — C.3.f (TICK-086) stage-3 preflight: discharge the three gaps the frozen scope names.

The scope (2026-09-10) froze with three things measured nowhere, and each was written down as a gap
rather than left to read as a zero. This closes all three before the production query is built.

  1. WALL 5 (C.1.a income) is unmeasured, and it is the wall most likely to be violated by the §7
     rows that carry the identification. Measured here from BOTH sides: an overlap read from one
     side says only which frame is bigger (`wall-cut-on-wrong-axis`). Also measured inside the
     identified subset, because 18 identified designs is the population that matters and a share of
     1,099 says nothing about them.

  2. §7 rows 5 and 6 (labour-demand shocks to a child's earning power; migrant remittances) had no
     volume at all. Row 6 is PI call 2, and the call turns on whether these studies are signed on
     the transfer or on household income — so the income intersection is measured, not argued.

  3. §7 row 4 — filial-responsibility law, 24 records and ZERO identified designs — is the one place
     a null would be informative, and a null on one spelling is not a null
     (`validate-a-null-detector-on-positives`). Two defences here. The vocabulary is widened to
     eight national spellings of the same legal instrument, because a law is indexed in the local
     name (`policy-literatures-indexed-in-the-local-vocabulary`); and the identified-design detector
     is run against three vocabularies where identified designs are KNOWN to exist, so that a zero
     is a statement about the literature rather than about the detector.

And one thing the scope owed §3: the outcome axis was never calibrated on its own
(`calibrate-the-outcome-axis-too`). Each outcome term is scored against the C.3.f exposure axis. The
specific worry is `family size`: in a transfer literature that phrase often means HOUSEHOLD size,
not completed fertility, and it would then be admitting co-residence records as fertility ones.

Outputs literature/search-logs/c3f-wall5-null-probe-<date>.{json,md}. Counting only.

Gotchas honoured: no commas in filter values; no phrase beginning "not"; no "?" wildcards; curl
rather than urllib (no CA bundle); a refusal raises and is recorded as an error, never as a zero.
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
OUTCOME_TERMS = ["fertility", "childbearing", "birth rate", "total fertility rate",
                 "family size", "number of children"]

# Verbatim from the scope, which took it from 304's UNION row.
C3F = ('("wealth flows" OR "intergenerational transfer" OR "intergenerational wealth" '
       'OR "National Transfer Accounts" OR "lifecycle deficit" OR "life cycle deficit" '
       'OR "child labour contribution" OR "child labor contribution" OR "value of children" '
       'OR "old age support" OR "old-age support" OR "filial support")')

# C.1.a's union axis, verbatim from 304, so the two sides of Wall 5 are the same objects the
# ranking used.
C1A = ('("income effect" OR "income elasticity" OR "normal good" OR "permanent income" '
       'OR "income shock" OR "household income" OR "family income" OR "windfall" '
       'OR "lottery winnings")')

IDENT = ('("instrumental variable" OR "difference-in-differences" OR "differences-in-differences" '
         'OR "natural experiment" OR "regression discontinuity" OR "randomized controlled trial" '
         'OR "randomised controlled trial" OR "event study" OR "synthetic control")')

# §7 row 2, verbatim from 376, so the intersections below are against the same object.
INHERITANCE = ('("inheritance law" OR "inheritance reform" OR "land titling" OR "land reform" '
               'OR "bequest motive")')

# §7 row 5: a labour-demand shock AND child work. Two axes, because a commodity boom alone is an
# economics literature and child work alone is a labour literature; the estimand needs both.
CHILD_WORK = ('("child labour" OR "child labor" OR "child work" OR "child employment" '
              'OR "working children")')
LABOUR_DEMAND = ('("commodity price" OR "mining boom" OR "cash crop" OR "export crop" '
                 'OR "trade shock" OR "labour demand" OR "labor demand" OR "mechanization" '
                 'OR "mechanisation" OR "agricultural productivity shock")')
ROW5 = f"{CHILD_WORK} AND {LABOUR_DEMAND}"

REMITTANCE = '("remittance" OR "remittances")'

# §7 row 4: eight national names for one legal instrument. A law is indexed in the local vocabulary.
FILIAL_SPELLINGS = [
    "filial responsibility law",
    "filial piety law",
    "family support obligation",
    "parental maintenance",
    "maintenance of parents",
    "elderly rights law",
    "old age maintenance",
    "elder support law",
]
FILIAL_UNION = "(" + " OR ".join(f'"{t}"' for t in FILIAL_SPELLINGS) + ")"

# Known-positive vocabularies for the detector. Each is a literature where identified designs
# certainly exist; if IDENT returns 0 on these, the detector is broken and row 4's zero means
# nothing.
DETECTOR_CONTROLS = [
    ("pension and social-security expansion (376 measured 26)",
     '("pension expansion" OR "social pension" OR "old age pension" OR "pension reform")'),
    ("compulsory schooling reform", '("compulsory schooling" OR "school leaving age" '
     'OR "compulsory education")'),
    ("cash transfer programmes", '("cash transfer" OR "conditional cash transfer")'),
]


class Refused(Exception):
    """A failed request. Never let this reach a counter as a zero."""


def count(query: str) -> int:
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
    try:
        try:
            n = count(query)
        except Refused as first:
            if "Rate limit" not in str(first):
                raise
            time.sleep(2.0)
            n = count(query)
        rows.append((label, query, n))
        print(f"  {n:>8,}  {label}", flush=True)
        time.sleep(PACE)
        return n
    except Refused as e:
        errors.append((label, str(e)))
        print(f"  REFUSED   {label}: {e}", file=sys.stderr, flush=True)
        time.sleep(PACE)
        return None


def main():
    date = datetime.date.today().isoformat()
    rows, errors = [], []

    print("\n== control ==")
    frame = measure("CONTROL C.3.f frame (the scope's 1099)", f"{C3F} AND {OUTCOME_WIDE}",
                    rows, errors)
    if not frame:
        sys.exit("control failed — nothing below is a measurement")

    print("\n== WALL 5: C.1.a income, measured from both sides ==")
    c1a = measure("C.1.a neighbour frame", f"{C1A} AND {OUTCOME_WIDE}", rows, errors)
    ov = measure("overlap: C.3.f AND C.1.a", f"{C3F} AND {C1A} AND {OUTCOME_WIDE}", rows, errors)
    ident_frame = measure("C.3.f frame carrying an identified design (376 got 18)",
                          f"{C3F} AND {OUTCOME_WIDE} AND {IDENT}", rows, errors)
    ident_ov = measure("overlap INSIDE the identified subset",
                       f"{C3F} AND {C1A} AND {OUTCOME_WIDE} AND {IDENT}", rows, errors)
    if None not in (c1a, ov):
        print(f"           -> {100*ov/frame:.1f}% of C.3.f · {100*ov/c1a:.1f}% of C.1.a")
    if None not in (ident_frame, ident_ov) and ident_frame:
        print(f"           -> {100*ident_ov/ident_frame:.0f}% of C.3.f's identified records")

    print("\n== §7 rows that move income as well as the flow ==")
    measure("row 2 inheritance/land AND C.1.a", f"{INHERITANCE} AND {C1A} AND {OUTCOME_WIDE}",
            rows, errors)
    measure("row 5 labour-demand x child work AND C.1.a", f"{ROW5} AND {C1A} AND {OUTCOME_WIDE}",
            rows, errors)
    measure("row 6 remittances AND C.1.a", f"{REMITTANCE} AND {C1A} AND {OUTCOME_WIDE}",
            rows, errors)

    print("\n== §7 row 5: labour-demand shocks to a child's earning power ==")
    measure("row 5 volume", f"{ROW5} AND {OUTCOME_WIDE}", rows, errors)
    measure("row 5 carrying an identified design", f"{ROW5} AND {OUTCOME_WIDE} AND {IDENT}",
            rows, errors)
    measure("row 5 crossover with the C.3.f axis", f"{ROW5} AND {C3F} AND {OUTCOME_WIDE}",
            rows, errors)

    print("\n== §7 row 6: remittances, and PI call 2 ==")
    measure("row 6 volume", f"{REMITTANCE} AND {OUTCOME_WIDE}", rows, errors)
    measure("row 6 carrying an identified design", f"{REMITTANCE} AND {OUTCOME_WIDE} AND {IDENT}",
            rows, errors)
    measure("row 6 crossover with the C.3.f axis", f"{REMITTANCE} AND {C3F} AND {OUTCOME_WIDE}",
            rows, errors)
    measure("row 6 signed on the TRANSFER (parents named as recipients)",
            f'{REMITTANCE} AND {OUTCOME_WIDE} AND ("remittances to parents" OR "support to parents" '
            'OR "old age support" OR "filial")', rows, errors)

    print("\n== §7 row 4: is the filial-law null a literature or a spelling? ==")
    for t in FILIAL_SPELLINGS:
        measure(f"spelling '{t}'", f'"{t}"', rows, errors)
    measure("filial-law union, unrestricted", FILIAL_UNION, rows, errors)
    measure("filial-law union AND a fertility outcome", f"{FILIAL_UNION} AND {OUTCOME_WIDE}",
            rows, errors)
    measure("filial-law union AND fertility AND an identified design",
            f"{FILIAL_UNION} AND {OUTCOME_WIDE} AND {IDENT}", rows, errors)

    print("\n== the identified-design detector, validated on known positives ==")
    for label, axis in DETECTOR_CONTROLS:
        measure(f"DETECTOR {label}", f"{axis} AND {OUTCOME_WIDE} AND {IDENT}", rows, errors)

    print("\n== outcome axis, calibrated term by term against the C.3.f exposure axis ==")
    for t in OUTCOME_TERMS:
        measure(f"OUTCOME '{t}'", f'{C3F} AND "{t}"', rows, errors)
    measure("'family size' INTERSECT household-size vocabulary (the worry)",
            f'{C3F} AND "family size" AND ("household size" OR "co-residence" OR "coresidence" '
            'OR "household composition" OR "living arrangements")', rows, errors)
    measure("'number of children' INTERSECT the same",
            f'{C3F} AND "number of children" AND ("household size" OR "co-residence" '
            'OR "coresidence" OR "household composition" OR "living arrangements")', rows, errors)

    # ------------------------------------------------------------------ outputs
    logs = pathlib.Path("literature/search-logs")
    blob = {"date": date, "outcome_axis": OUTCOME_WIDE, "c3f_axis": C3F, "c1a_axis": C1A,
            "ident_axis": IDENT, "row5_axis": ROW5, "filial_union": FILIAL_UNION,
            "rows": [{"label": l, "query": q, "n": n} for l, q, n in rows],
            "errors": [{"label": l, "error": e} for l, e in errors]}
    (logs / f"c3f-wall5-null-probe-{date}.json").write_text(json.dumps(blob, indent=2) + "\n")

    md = [f"# C.3.f — Wall 5, the §7 gaps, and the filial-law null — {date}", "",
          "Generated by `source/build/goldset/379_c3f_wall5_and_null_probe.py`. Do not edit by",
          "hand; re-run the script.", ""]
    md += ([f"**{len(errors)} request(s) REFUSED — those rows are missing, not zero.**", ""] +
           [f"- `{l}` — {e}" for l, e in errors] + [""]) if errors else \
          ["No request was refused: every row below is a measurement.", ""]
    md += ["| n | row |", "|---|---|"]
    md += [f"| {n:,} | {l} |" if n is not None else f"| REFUSED | {l} |" for l, _, n in rows]
    md.append("")
    (logs / f"c3f-wall5-null-probe-{date}.md").write_text("\n".join(md))
    print(f"\nwrote c3f-wall5-null-probe-{date}.json and .md "
          f"({len(rows)} counts, {len(errors)} refused)")


main()
