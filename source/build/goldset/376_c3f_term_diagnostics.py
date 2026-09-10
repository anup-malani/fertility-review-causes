#!/usr/bin/env python3
"""
376 — C.3.f (TICK-086) stage-2 diagnostic: score every term alone, split the frame by the
DIRECTION of the flow, and ask whether the registered claim has any identified evidence at all.

Why this exists. The 2026-09-10 candidate frame probe ranked C.3.f on a UNION frame of 1,101
records built from twelve exposure terms AND a wide fertility outcome axis. That number ranked
the candidate. It does not say which term earned it, and it does not say whether the records
inside it test the registered claim or merely share its vocabulary. Every chapter since C.2.b has
had to close that gap before scoping, so it is closed here first.

What is specific to C.3.f, and why the direction split is the whole diagnostic
-----------------------------------------------------------------------------
The registered claim (HYPOTHESES-v5 §C.3.f) is that modernization REVERSES the net direction of
intergenerational transfers -- upward (children support parents) becomes downward (parents
subsidize children) -- and that the reversal removes the economic rationale for high fertility.
The exposure is therefore a NET quantity with a SIGN, and the sign is the claim.

That makes three arms possible inside one vocabulary, and they are not the same estimand:

  UPWARD    child labour contribution, old-age support, filial support, remittances to parents.
            What children give. Its policy-identified corner is C.3.c (old-age security), a
            CLOSED chapter -- 162 records of this frame carry pension vocabulary.
  DOWNWARD  parental investment, expenditure on children, human capital investment. What parents
            give. Its price-side estimand is C.2.b (direct costs), a DRAFTED chapter.
  NET       the difference, and its sign. This alone is C.3.f's registered exposure.

If the NET arm is thin and the two one-directional arms are thick, then this chapter's evidence
base is other chapters' evidence read as halves of a difference nobody computed -- which is a
finding, and one that has to be established with a second channel before it is stated
(`empty-cell-needs-second-channel`, `empty-cell-is-the-result`).

The second worry is measurement-versus-identification. `value of children` alone is 515 of the
1,101 (probe, 09-10): the Value-of-Children survey tradition, which measures STATED valuations,
and National Transfer Accounts, which MEASURES realized flows by construction and estimates
nothing. Both describe the exposure. Neither estimates its effect on fertility. The identified-
design markers below say how much of the frame is neither.

Lessons this design honours
---------------------------
  anchored-vocabulary-has-own-homonym  — score each anchor term alone. "intergenerational
      transfer" is a public-finance and behaviour-genetics term before it is a demographic one;
      the probe put the bequest residue inside the fertility frame at 33, and that is checked
      again here against the genetics reading, which the probe did not measure.
  calibrate-the-outcome-axis-too       — the outcome axis gets the same treatment as the exposure.
  advance-the-baseline-when-accepting-terms / frame-growth-is-not-frame-gain — candidate terms are
      priced as (axis OR term) minus (axis), never by their own size.
  read-the-mechanism-not-the-instrument-name — the direction arms are defined by which way the
      resources move, not by which literature's words are used.
  validate-a-null-detector-on-positives — a control runs first, and a refused request is an error,
      never a zero (`refusals-read-as-zeros`).

Outputs literature/search-logs/c3f-term-diagnostics-<date>.{json,md}. Counting only; no records
are retained, so this is cheap and re-runnable.

Gotchas honoured (recorded from earlier chapters):
  - a comma inside a filter VALUE is fatal and %2C does not save it -> no commas in any term
  - a phrase beginning "not" parses as boolean NOT -> none here; marginal gain is computed by
    subtraction so the query language never has to express a negation
  - "?" in a search value is a wildcard and returns 200 with a misleading body -> none here
  - OpenAlex drops stopwords inside phrases, so "flow of wealth" == "flow wealth" -> the spelling
    block measures that rather than assuming it
  - this Python has no CA bundle: shell out to curl rather than urllib
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

# The twelve terms of the 2026-09-10 UNION axis for C.3.f, verbatim from 304.
TERMS = [
    "wealth flows",
    "intergenerational transfer",
    "intergenerational wealth",
    "National Transfer Accounts",
    "lifecycle deficit",
    "life cycle deficit",
    "child labour contribution",
    "child labor contribution",
    "value of children",
    "old age support",
    "old-age support",
    "filial support",
]
UNION_AXIS = "(" + " OR ".join(f'"{t}"' for t in TERMS) + ")"

# Identification markers. Deliberately design names, not topic words: a record carrying one of
# these is claiming to estimate something rather than to describe it.
IDENT = ('("instrumental variable" OR "difference-in-differences" OR "differences-in-differences" '
         'OR "natural experiment" OR "regression discontinuity" OR "randomized controlled trial" '
         'OR "randomised controlled trial" OR "event study" OR "synthetic control")')


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
        print(f"  {n:>8,}  {label}", flush=True)
        time.sleep(PACE)
        return n
    except Refused as e:
        errors.append((label, str(e)))
        print(f"  REFUSED   {label}: {e}", file=sys.stderr, flush=True)
        time.sleep(PACE)
        return None


# ------------------------------------------------------------------ the direction arms
# Defined by which way the resources move, not by which literature's words are used. A record can
# of course carry both; the overlap row below measures that rather than assuming it away.
UPWARD = ('("child labour contribution" OR "child labor contribution" OR "old age support" '
          'OR "old-age support" OR "filial support" OR "remittances to parents" '
          'OR "support of elderly parents" OR "children economic value" OR "child labor income")')
DOWNWARD = ('("parental investment" OR "expenditure on children" OR "investment in children" '
            'OR "cost of children" OR "cost of raising children" OR "human capital investment" '
            'OR "child rearing cost")')
NET = ('("wealth flows" OR "net transfer" OR "net intergenerational transfer" '
       'OR "direction of wealth flows" OR "reversal of wealth flows" OR "lifecycle deficit" '
       'OR "life cycle deficit" OR "National Transfer Accounts" OR "net cost of children")')


def main():
    date = datetime.date.today().isoformat()
    rows, errors, marginal = [], [], []

    print("\n== control: the channel must be alive before any zero below is believed ==")
    measure("CONTROL fertility decline", '"fertility decline"', rows, errors)
    baseline = measure("CONTROL C.3.f union frame (reproduces the 09-10 number: 1101)",
                       f"{UNION_AXIS} AND {OUTCOME_WIDE}", rows, errors)

    # Ordered decisive-first. The daily OpenAlex allowance is ~100 requests and this run is
    # ~63 of them, so a run that dies of budget should lose the vocabulary bookkeeping at the
    # end rather than the direction split that decides the scope.
    print("\n== THE RULING: split the frame by the DIRECTION of the flow ==")
    for label, axis in [("UPWARD children -> parents", UPWARD),
                        ("DOWNWARD parents -> children", DOWNWARD),
                        ("NET the difference and its sign", NET)]:
        measure(f"ARM {label}", f"{axis} AND {OUTCOME_WIDE}", rows, errors)
        measure(f"ARM {label} carrying an identified design",
                f"{axis} AND {OUTCOME_WIDE} AND {IDENT}", rows, errors)
    measure("ARM overlap: upward AND downward in one record",
            f"{UPWARD} AND {DOWNWARD} AND {OUTCOME_WIDE}", rows, errors)
    measure("ARM overlap: net AND (upward OR downward)",
            f"{NET} AND ({UPWARD} OR {DOWNWARD}) AND {OUTCOME_WIDE}", rows, errors)

    print("\n== how much of the union frame claims to ESTIMATE anything ==")
    measure("FRAME carrying an identified design", f"{UNION_AXIS} AND {OUTCOME_WIDE} AND {IDENT}",
            rows, errors)
    measure("FRAME carrying an accounting/measurement marker",
            f'{UNION_AXIS} AND {OUTCOME_WIDE} AND ("accounting" OR "estimates of" OR "we measure" '
            'OR "descriptive" OR "cross-country comparison")', rows, errors)

    print("\n== second channel: shocks that move the net flow without C.3.f vocabulary ==")
    # empty-cell-needs-second-channel. If the NET arm above is thin, a null is only worth
    # something when a channel that fails differently has also been tried. These are policy
    # shocks that change which way resources move, named as the policy literature names them.
    for label, q in [
        ("inheritance and land-title reform",
         '("inheritance law" OR "inheritance reform" OR "land titling" OR "land reform" '
         'OR "bequest motive")'),
        ("child labour bans and schooling supply",
         '("child labour ban" OR "child labor ban" OR "child labour law" OR "child labor law" '
         'OR "school construction" OR "schooling supply")'),
        ("pension and social-security expansion (C.3.c owns this corner)",
         '("pension expansion" OR "social pension" OR "old age pension" OR "social security '
         'expansion" OR "pension reform")'),
        ("filial-responsibility and family-support law",
         '("filial responsibility" OR "family support law" OR "elderly support law" '
         'OR "maintenance of parents")'),
    ]:
        n = measure(f"CHANNEL2 {label}", f"{q} AND {OUTCOME_WIDE}", rows, errors)
        measure(f"CHANNEL2 {label} carrying an identified design",
                f"{q} AND {OUTCOME_WIDE} AND {IDENT}", rows, errors)
        measure(f"CHANNEL2 {label} INTERSECT the C.3.f axis (crossover)",
                f"{q} AND {UNION_AXIS} AND {OUTCOME_WIDE}", rows, errors)

    print("\n== each exposure term ALONE fertility-restricted (which term earned the 1101) ==")
    for t in TERMS:
        measure(f"TERM {t}", f'"{t}" AND {OUTCOME_WIDE}', rows, errors)

    print("\n== the general-purpose terms UNRESTRICTED (how much of each is even demographic) ==")
    for t in ["intergenerational transfer", "intergenerational wealth", "value of children",
              "filial support"]:
        measure(f"BARE {t}", f'"{t}"', rows, errors)

    print("\n== the axis without each term that could be carrying it alone ==")
    for drop in ("intergenerational transfer", "value of children", "old age support"):
        minus = "(" + " OR ".join(f'"{t}"' for t in TERMS if t != drop) + ")"
        measure(f"AXIS minus '{drop}'", f"{minus} AND {OUTCOME_WIDE}", rows, errors)

    print("\n== spelling and stopword variants of the core Caldwell phrase ==")
    for v in ["wealth flow", "flow of wealth", "intergenerational flows", "net transfers",
              "direction of transfers", "intergenerational resource flows"]:
        measure(f"SPELLING {v}", f'"{v}" AND {OUTCOME_WIDE}', rows, errors)

    print("\n== homonym: the two readings the probe did not measure ==")
    for label, q in [
        ("intergenerational transfer INTERSECT behaviour genetics",
         '"intergenerational transfer" AND ("epigenetic" OR "heritability" OR "genotype" '
         'OR "transmission of traits")'),
        ("genetics residue INSIDE the fertility-restricted frame",
         f'"intergenerational transfer" AND {OUTCOME_WIDE} AND ("epigenetic" OR "heritability" '
         'OR "genotype")'),
        ("value of children INTERSECT the VOC survey tradition",
         '"value of children" AND ("attitudes" OR "survey" OR "psychological" OR "perceived value")'),
        ("VOC-survey residue INSIDE the fertility-restricted frame",
         f'"value of children" AND {OUTCOME_WIDE} AND ("attitudes" OR "survey" '
         'OR "perceived value")'),
        ("National Transfer Accounts alone (measurement by construction)",
         '("National Transfer Accounts" OR "lifecycle deficit" OR "life cycle deficit")'),
    ]:
        measure(f"HOMONYM {label}", q, rows, errors)

    print("\n== boundaries INSIDE the frame, against neighbouring registry entries ==")
    for label, q in [
        ("A.19 intergenerational transmission of FERTILITY (an unstarted candidate)",
         f'{UNION_AXIS} AND {OUTCOME_WIDE} AND ("intergenerational transmission of fertility" '
         'OR "fertility transmission" OR "intergenerational fertility correlation")'),
        ("C.3.d quantity-quality (a drafted chapter)",
         f'{UNION_AXIS} AND {OUTCOME_WIDE} AND ("quantity-quality" OR "child quality" '
         'OR "child investment")'),
        ("Alexandra's child-labour and compulsory-schooling chapter",
         f'{UNION_AXIS} AND {OUTCOME_WIDE} AND ("compulsory schooling" OR "compulsory education" '
         'OR "child labour law" OR "child labor law" OR "school leaving age")'),
    ]:
        measure(f"BOUNDARY {label}", q, rows, errors)

    print("\n== candidate terms priced by MARGINAL gain over the current axis ==")
    candidates = [
        "net cost of children",
        "intergenerational support",
        "upward transfers",
        "downward transfers",
        "economic value of children",
        "children as investment",
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
        print("  baseline refused — marginal gains not computed (a gain against a missing "
              "baseline is not a number)", file=sys.stderr)

    # ------------------------------------------------------------------ outputs
    logs = pathlib.Path("literature/search-logs")
    blob = {"date": date, "outcome_axis": OUTCOME_WIDE, "union_axis": UNION_AXIS,
            "ident_axis": IDENT, "arms": {"upward": UPWARD, "downward": DOWNWARD, "net": NET},
            "rows": [{"label": l, "query": q, "n": n} for l, q, n in rows],
            "marginal": marginal,
            "errors": [{"label": l, "error": e} for l, e in errors]}
    (logs / f"c3f-term-diagnostics-{date}.json").write_text(json.dumps(blob, indent=2) + "\n")

    md = [f"# C.3.f term diagnostics — {date}", "",
          "Generated by `source/build/goldset/376_c3f_term_diagnostics.py`. Do not edit by hand;",
          "re-run the script. Counts are OpenAlex `title_and_abstract.search` record counts.", ""]
    if errors:
        md += [f"**{len(errors)} request(s) REFUSED — those rows are missing, not zero.**", ""]
        md += [f"- `{l}` — {e}" for l, e in errors] + [""]
    else:
        md += ["No request was refused: every row below is a measurement.", ""]
    md += ["| n | row |", "|---|---|"]
    md += [f"| {n:,} | {l} |" if n is not None else f"| REFUSED | {l} |" for l, _, n in rows]
    if marginal:
        md += ["", "## Candidate terms, priced by marginal gain", "",
               f"Baseline (current axis): **{marginal[0]['baseline']:,}**", "",
               "| term | axis OR term | gain |", "|---|---|---|"]
        md += [f"| `{m['term']}` | {m['widened']:,} | {m['gain']:+,} |"
               for m in sorted(marginal, key=lambda m: -m["gain"])]
    md.append("")
    (logs / f"c3f-term-diagnostics-{date}.md").write_text("\n".join(md))
    print(f"\nwrote c3f-term-diagnostics-{date}.json and .md "
          f"({len(rows)} counts, {len(errors)} refused)")


main()
