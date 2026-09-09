#!/usr/bin/env python3
"""
345 — C.3.d (TICK-083) stage-2, part 2: calibrate the OUTCOME axis, split the frame by the
direction of the estimand, and give the SBTC arm a second channel before calling it empty.

344 measured the exposure axis and found a clean-looking result: the dominant term is the
mechanism's own name and the vocabulary boundaries against the drafted neighbours are tiny. Three
things it did not test, each of which can invalidate that reading.

1. THE OUTCOME AXIS SHARES ITS WORD WITH TWO OTHER SCIENCES.
   `homonym-shares-outcome-vocabulary`: measuring a homonym cloud with a vocabulary that contains
   the shared word scores the wall's justification against the wall. "Fertility" means soil
   fertility in agronomy and reproductive performance in animal husbandry, and "quantity-quality"
   is a stock phrase in BOTH -- quantity and quality of yield under varying fertility, quantity
   and quality of semen. 344 found "quantity-quality" at 8,154 bare and 494 fertility-restricted
   and read the drop as the restriction working. It may instead be the restriction selecting a
   different species. `calibrate-the-outcome-axis-too` says score each outcome term alone.

2. THE FRAME MIXES TWO OPPOSITE ESTIMANDS.
   C.3.d's registered claim runs FORWARD: rising returns to child human capital lower desired
   fertility. The literature's famous micro test runs BACKWARD: does exogenously larger family
   size lower per-child investment and child outcomes? Black-Devereux-Salvanes 2005, which the
   registry itself cites as finding little tradeoff, is the backward direction and its outcome is
   children's schooling, not fertility. `anchor-on-the-estimand-not-the-famous-design`: the
   celebrated designs may not measure the registered outcome at all, which is what C.3.e found.
   344 measured the forward frame only, because OUTCOME_WIDE is a fertility axis. The backward
   literature is invisible to it, and ruling 4 cannot be written without knowing its size.

3. THE SBTC ARM RETURNED 3 AND 5, ON ONE VOCABULARY.
   `empty-cell-needs-second-channel`: C.3.g's "no natural experiment exists" was two missing
   words. A second vocabulary runs here before ruling 3 is written either way, and the channel is
   validated on a known positive first (`validate-a-null-detector-on-positives`).

Outputs literature/search-logs/c3d-outcome-axis-<date>.{json,md}. Counting only.

Same gotchas as 344: no commas in filter values, no phrase beginning "not", no "?" wildcards, no
boolean NOT anywhere (shares are computed by subtraction), and curl rather than urllib because
this Python has no CA bundle.
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

# Identical to 344 and to 304's pass 4, so the numbers compose.
OUTCOME_WIDE = ('("fertility" OR "childbearing" OR "birth rate" OR "total fertility rate" '
                'OR "family size" OR "number of children")')
OUTCOME_TERMS = ["fertility", "childbearing", "birth rate", "total fertility rate",
                 "family size", "number of children"]

TERMS = ["quantity-quality", "quantity quality tradeoff", "child quality", "child investment",
         "sibsize", "human capital of children"]
UNION_AXIS = "(" + " OR ".join(f'"{t}"' for t in TERMS) + ")"

# Words that mark a record as being about soil, crops or livestock rather than about people.
# Deliberately narrow: each is a term no human-demography abstract uses.
NONHUMAN = ('("soil fertility" OR "crop yield" OR "grain yield" OR "fertilizer" OR "fertiliser" '
            'OR "livestock" OR "dairy cattle" OR "semen quality" OR "broiler" OR "silage" '
            'OR "agronomic")')

# The backward-direction outcome: children's own human capital, not the parents' fertility.
CHILD_OUTCOME = ('("educational attainment" OR "test scores" OR "cognitive ability" '
                 'OR "years of schooling" OR "child outcomes" OR "school achievement")')


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
        print(f"  {n:>9,}  {label}")
        time.sleep(PACE)
        return n
    except Refused as e:
        errors.append((label, str(e)))
        print(f"  REFUSED    {label}: {e}", file=sys.stderr)
        time.sleep(PACE)
        return None


def pct(part, whole):
    return f"{100.0 * part / whole:.1f}%" if whole else "—"


def main():
    date = datetime.date.today().isoformat()
    rows, errors, notes = [], [], []

    print("\n== control ==")
    measure("CONTROL fertility decline", '"fertility decline"', rows, errors)
    frame = measure("CONTROL C.3.d frame (344's baseline: 762)",
                    f"{UNION_AXIS} AND {OUTCOME_WIDE}", rows, errors)

    print("\n== 1a. is the fertility restriction selecting humans or selecting agronomy? ==")
    nonhuman_in_frame = measure(
        "non-human residue INSIDE the fertility-restricted frame",
        f"{UNION_AXIS} AND {OUTCOME_WIDE} AND {NONHUMAN}", rows, errors)
    measure("quantity-quality AND fertility, non-human marked",
            f'"quantity-quality" AND {OUTCOME_WIDE} AND {NONHUMAN}', rows, errors)
    measure("quantity-quality bare AND non-human marked",
            f'"quantity-quality" AND {NONHUMAN}', rows, errors)
    measure("quantity-quality bare AND human-demographic marked",
            '"quantity-quality" AND ("household" OR "parents" OR "children" OR "demographic" '
            'OR "human capital")', rows, errors)

    print("\n== 1b. each OUTCOME term alone against the exposure axis ==")
    # calibrate-the-outcome-axis-too. A term that carries a large share of the frame while
    # contributing no human-demographic records is the C.3.e "parity" failure.
    outcome_share = {}
    for t in OUTCOME_TERMS:
        n = measure(f"OUTCOME {t}", f'{UNION_AXIS} AND "{t}"', rows, errors)
        nh = measure(f"OUTCOME {t} -- non-human marked",
                     f'{UNION_AXIS} AND "{t}" AND {NONHUMAN}', rows, errors)
        if n is not None:
            outcome_share[t] = {"n": n, "nonhuman": nh}

    print("\n== 1c. the frame WITHOUT its broadest outcome word ==")
    narrow_outcome = ('("childbearing" OR "birth rate" OR "total fertility rate" '
                      'OR "family size" OR "number of children")')
    measure("frame on the outcome axis minus bare 'fertility'",
            f"{UNION_AXIS} AND {narrow_outcome}", rows, errors)

    print("\n== 2. direction of the estimand: forward (fertility) vs backward (child outcomes) ==")
    backward = measure("BACKWARD axis AND child-outcome vocabulary",
                       f"{UNION_AXIS} AND {CHILD_OUTCOME}", rows, errors)
    both = measure("BOTH axis AND fertility AND child-outcome",
                   f"{UNION_AXIS} AND {OUTCOME_WIDE} AND {CHILD_OUTCOME}", rows, errors)
    measure("BACKWARD with an identified family-size design attached",
            f'{UNION_AXIS} AND {CHILD_OUTCOME} AND ("twin birth" OR "twinning" '
            'OR "sibling sex composition" OR "same-sex siblings" OR "instrumental variable")',
            rows, errors)
    measure("FORWARD with a returns-to-skill exposure attached",
            f'{UNION_AXIS} AND {OUTCOME_WIDE} AND ("return to education" OR "returns to schooling" '
            'OR "skill premium" OR "return to human capital")', rows, errors)
    measure("the family-size-shock literature that does NOT use C.3.d vocabulary, backward",
            f'("twin birth" OR "twinning" OR "sibling sex composition" OR "same-sex siblings") '
            f'AND {CHILD_OUTCOME}', rows, errors)

    print("\n== 3. SBTC arm, second channel -- validated on a known positive first ==")
    # validate-a-null-detector-on-positives: if these controls also return ~0 the channel is
    # broken and the null means nothing.
    measure("CHANNEL CONTROL returns to schooling AND fertility (known to exist: 344 got 212)",
            f'("return to education" OR "returns to schooling") AND {OUTCOME_WIDE}', rows, errors)
    measure("CHANNEL CONTROL skill premium bare (known large)", '"skill premium"', rows, errors)
    sbtc2 = [
        ("technology raising the return to human capital",
         '("technological change" OR "technical change" OR "industrialization" '
         'OR "industrialisation") AND ("return to human capital" OR "return to education" '
         'OR "skill premium")'),
        ("that same axis AND a fertility outcome",
         '("technological change" OR "technical change" OR "industrialization" '
         'OR "industrialisation") AND ("return to human capital" OR "return to education" '
         f'OR "skill premium") AND {OUTCOME_WIDE}'),
        ("demand for skill AND fertility",
         f'("demand for skill" OR "demand for skilled labour" OR "demand for skilled labor" '
         f'OR "skill demand") AND {OUTCOME_WIDE}'),
        ("unified growth framing of the same shock",
         f'("unified growth" OR "human capital accumulation") AND ("technological" OR "technology") '
         f'AND {OUTCOME_WIDE}'),
        ("trade shock as the skill shock AND fertility",
         f'("trade liberalization" OR "trade liberalisation" OR "import competition" '
         f'OR "China shock") AND {OUTCOME_WIDE}'),
    ]
    sbtc_counts = {}
    for label, q in sbtc2:
        sbtc_counts[label] = measure(f"SBTC2 {label}", q, rows, errors)

    # ---------------------------------------------------------------- interpretation, computed
    if frame and nonhuman_in_frame is not None:
        notes.append(f"Non-human residue inside the 762-record frame: {nonhuman_in_frame} "
                     f"({pct(nonhuman_in_frame, frame)}).")
    if frame and backward is not None:
        notes.append(f"Backward-direction frame (child outcomes): {backward} against a forward "
                     f"frame of {frame}.")
    if backward is not None and both is not None:
        notes.append(f"Records carrying BOTH outcomes: {both} "
                     f"({pct(both, backward)} of the backward frame).")

    out = pathlib.Path("literature/search-logs")
    out.mkdir(parents=True, exist_ok=True)
    blob = {"date": date, "script": "345_c3d_outcome_axis_and_direction.py",
            "outcome_axis_wide": OUTCOME_WIDE, "union_axis": UNION_AXIS,
            "nonhuman_axis": NONHUMAN, "child_outcome_axis": CHILD_OUTCOME,
            "frame": frame, "outcome_term_shares": outcome_share,
            "rows": [{"label": l, "query": q, "n": n} for l, q, n in rows],
            "notes": notes,
            "refused": [{"label": l, "error": e} for l, e in errors]}
    (out / f"c3d-outcome-axis-{date}.json").write_text(json.dumps(blob, indent=2))

    lines = [f"# C.3.d outcome-axis calibration and estimand direction — {date}", "",
             "Generated by `source/build/goldset/345_c3d_outcome_axis_and_direction.py`. Do not",
             "edit by hand; re-run the script.", "",
             f"Exposure axis: `{UNION_AXIS}`", "",
             f"Outcome axis (wide): `{OUTCOME_WIDE}`", "",
             f"Non-human marker: `{NONHUMAN}`", "",
             f"Backward-direction outcome: `{CHILD_OUTCOME}`", ""]
    if notes:
        lines += ["## What the counts say", ""] + [f"- {n}" for n in notes] + [""]
    if outcome_share:
        lines += ["## Outcome axis, each term scored alone against the exposure axis", "",
                  "| outcome term | records | of which non-human marked | share |",
                  "|---|---|---|---|"]
        for t, d in sorted(outcome_share.items(), key=lambda kv: -(kv[1]["n"] or 0)):
            nh = d["nonhuman"]
            lines.append(f"| `{t}` | {d['n']:,} | {'—' if nh is None else f'{nh:,}'} | "
                         f"{'—' if nh is None else pct(nh, d['n'])} |")
        lines.append("")
    lines += ["## Every measurement", "", "| n | measurement | query |", "|---|---|---|"]
    for l, q, n in rows:
        lines.append(f"| **{n:,}** | {l} | `{q}` |")
    if errors:
        lines += ["", "## REFUSED — these are not zeros", ""]
        lines += [f"- {l}: {e}" for l, e in errors]
    else:
        lines += ["", "No refused requests: every count above is a measurement, not a failure."]
    (out / f"c3d-outcome-axis-{date}.md").write_text("\n".join(lines) + "\n")

    print(f"\nwrote literature/search-logs/c3d-outcome-axis-{date}.{{json,md}}")
    for n in notes:
        print(f"  * {n}")
    if errors:
        print(f"WARNING: {len(errors)} refused request(s) — not counted as zeros", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
