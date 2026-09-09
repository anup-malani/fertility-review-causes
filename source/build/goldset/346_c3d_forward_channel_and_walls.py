#!/usr/bin/env python3
"""
346 — C.3.d (TICK-083) stage-2, part 3: a SECOND CHANNEL for the forward arm, and the wall probes
the scope document's boundary table needs.

Why this runs BEFORE the scope is drafted. 345 measured the forward arm -- a returns-to-skill
exposure with a fertility outcome, inside C.3.d's own frame -- at EIGHT records. That number is
about to become the most consequential sentence in the chapter, and it currently rests on one
vocabulary. C.2.f drafted exactly that sentence on one vocabulary in its scope §4 ("expect an empty
or near-empty primary cell") and had to RETRACT it the same week: the chain was not missing from
the literature, it was missing from the words the probe used, and it was written in the East Asian
education-competition vocabulary instead. `empty-cell-needs-second-channel`.

`channels-must-fail-differently` sets the bar: a null is worth something only if the channels die
for unrelated reasons. So channel 2 here shares no phrase with channel 1. Channel 1 asked for the
return to skill in the economics-of-education vocabulary. Channel 2 asks for the SHOCKS that move
it, in each shock literature's own local words -- trade exposure, technology adoption, schooling
supply, historical industrialization -- which is `policy-literatures-indexed-in-the-local-
vocabulary`, worth +40% of A.23's frame.

`validate-a-null-detector-on-positives`: every channel is fired at a known positive first. A
channel that returns 0 on its control is broken and its zeros are not evidence.

The wall block measures each boundary in BOTH directions -- how much of C.3.d's frame the
neighbour's vocabulary claims, and how much of the neighbour's frame C.3.d's vocabulary claims --
because a small overlap read from one side only says which frame is bigger, not where the estimands
collide. `wall-cut-on-wrong-axis`.

Outputs literature/search-logs/c3d-forward-channel-walls-<date>.{json,md}. Counting only.

Same gotchas as 344 and 345: no commas in filter values, no phrase beginning "not", no "?"
wildcards, no boolean NOT, curl rather than urllib.
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
TERMS = ["quantity-quality", "quantity quality tradeoff", "child quality", "child investment",
         "sibsize", "human capital of children"]
UNION_AXIS = "(" + " OR ".join(f'"{t}"' for t in TERMS) + ")"

# Channel 1's vocabulary, quarantined here so channel 2 can be checked for overlap against it.
CHANNEL1 = ('("return to education" OR "returns to schooling" OR "returns to education" '
            'OR "skill premium" OR "college premium" OR "return to human capital")')


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


def main():
    date = datetime.date.today().isoformat()
    rows, errors = [], []
    channel2, walls = [], []

    print("\n== controls ==")
    measure("CONTROL fertility decline", '"fertility decline"', rows, errors)
    frame = measure("CONTROL C.3.d frame (762)", f"{UNION_AXIS} AND {OUTCOME_WIDE}", rows, errors)
    ch1 = measure("CHANNEL 1 forward arm, inside the C.3.d frame (345 got 8)",
                  f"{UNION_AXIS} AND {OUTCOME_WIDE} AND {CHANNEL1}", rows, errors)
    measure("CHANNEL 1 forward arm, NOT restricted to the C.3.d frame",
            f"{CHANNEL1} AND {OUTCOME_WIDE}", rows, errors)

    print("\n== channel 2: the SHOCKS that move the return, each in its own local vocabulary ==")
    # Each row is (label, control query -- must be non-zero, arm query -- the measurement).
    ch2 = [
        ("trade / import competition",
         '("import competition" OR "trade liberalization" OR "trade liberalisation" OR "China shock")',
         f'("import competition" OR "trade liberalization" OR "trade liberalisation" '
         f'OR "China shock") AND {OUTCOME_WIDE}'),
        ("technology adoption / automation exposure",
         '("robot adoption" OR "industrial robots" OR "computer adoption" OR "routine-biased")',
         f'("robot adoption" OR "industrial robots" OR "computer adoption" OR "routine-biased") '
         f'AND {OUTCOME_WIDE}'),
        ("schooling supply expansion",
         '("school construction" OR "school expansion" OR "education expansion" '
         'OR "universal primary education")',
         f'("school construction" OR "school expansion" OR "education expansion" '
         f'OR "universal primary education") AND {OUTCOME_WIDE}'),
        ("historical industrialization and human capital",
         '("industrial revolution" OR "industrialization" OR "industrialisation") '
         'AND ("human capital" OR "literacy" OR "schooling")',
         f'("industrial revolution" OR "industrialization" OR "industrialisation") '
         f'AND ("human capital" OR "literacy" OR "schooling") AND {OUTCOME_WIDE}'),
        ("local labour-demand shocks to skill",
         '("labour demand shock" OR "labor demand shock" OR "local labour market" '
         'OR "local labor market") AND ("skill" OR "education")',
         f'("labour demand shock" OR "labor demand shock" OR "local labour market" '
         f'OR "local labor market") AND ("skill" OR "education") AND {OUTCOME_WIDE}'),
        ("occupational structure / white-collar shift",
         '("occupational structure" OR "white-collar" OR "skilled occupations" OR "deskilling")',
         f'("occupational structure" OR "white-collar" OR "skilled occupations" OR "deskilling") '
         f'AND {OUTCOME_WIDE}'),
    ]
    for label, ctrl_q, arm_q in ch2:
        c = measure(f"CH2 CONTROL {label}", ctrl_q, rows, errors)
        a = measure(f"CH2 ARM     {label} AND fertility", arm_q, rows, errors)
        x = measure(f"CH2 XOVER   {label} INTERSECT channel-1 vocabulary",
                    f"({arm_q}) AND {CHANNEL1}", rows, errors)
        channel2.append({"label": label, "control": c, "arm": a, "overlap_ch1": x})

    print("\n== does channel 2 reach records channel 1 and the C.3.d axis both miss? ==")
    ch2_axis = ('("import competition" OR "trade liberalization" OR "China shock" '
                'OR "industrial robots" OR "school construction" OR "education expansion" '
                'OR "industrial revolution" OR "occupational structure")')
    measure("channel-2 axis AND fertility", f"{ch2_axis} AND {OUTCOME_WIDE}", rows, errors)
    measure("channel-2 axis AND fertility AND the C.3.d frame",
            f"{ch2_axis} AND {OUTCOME_WIDE} AND {UNION_AXIS}", rows, errors)
    measure("channel-2 axis AND fertility AND channel-1 vocabulary",
            f"{ch2_axis} AND {OUTCOME_WIDE} AND {CHANNEL1}", rows, errors)
    measure("channel-2 axis AND fertility AND an identified-design marker",
            f'{ch2_axis} AND {OUTCOME_WIDE} AND ("difference-in-differences" OR "instrumental '
            'variable" OR "natural experiment" OR "regression discontinuity" OR "event study")',
            rows, errors)

    print("\n== walls, measured from BOTH sides ==")
    # (label, neighbour vocabulary, neighbour's own outcome-restricted frame)
    wall_defs = [
        ("C.2.f reference standard -- the wall C.2.f's PI call 3 challenges",
         '("income inequality" OR "status competition" OR "positional good" OR "relative status" '
         'OR "social comparison" OR "educational arms race")'),
        ("C.2.e female wage / opportunity cost of mother's time",
         '("opportunity cost of time" OR "female wage" OR "female labor force participation" '
         'OR "female labour force participation" OR "mother\'s education")'),
        ("C.2.b direct cost of children",
         '("cost of children" OR "child cost" OR "expenditure on children" '
         'OR "cost of raising children")'),
        ("C.1.a income effect",
         '("income effect" OR "income elasticity" OR "permanent income" OR "income shock")'),
        ("A.1 child mortality and replacement",
         '("child mortality" OR "infant mortality" OR "child survival" OR "replacement effect")'),
        ("A.12 twinning as an accounting identity (drafted) vs as an instrument",
         '("twin birth" OR "twinning" OR "multiple births")'),
        ("Alexandra's compulsory schooling / child labour laws",
         '("compulsory schooling" OR "compulsory education" OR "school leaving age" '
         'OR "child labour law" OR "child labor law")'),
        ("C.3.f wealth flows / value of children",
         '("wealth flows" OR "value of children" OR "intergenerational transfer")'),
        ("D.2.d intensive parenting norms",
         '("intensive parenting" OR "concerted cultivation" OR "parenting norms")'),
    ]
    for label, vocab in wall_defs:
        nb = measure(f"WALL {label} -- neighbour frame", f"{vocab} AND {OUTCOME_WIDE}", rows, errors)
        ov = measure(f"WALL {label} -- overlap with the C.3.d frame",
                     f"{vocab} AND {OUTCOME_WIDE} AND {UNION_AXIS}", rows, errors)
        walls.append({"label": label, "neighbour_frame": nb, "overlap": ov})

    out = pathlib.Path("literature/search-logs")
    out.mkdir(parents=True, exist_ok=True)
    blob = {"date": date, "script": "346_c3d_forward_channel_and_walls.py",
            "outcome_axis_wide": OUTCOME_WIDE, "union_axis": UNION_AXIS, "channel1": CHANNEL1,
            "frame": frame, "channel1_forward_arm_in_frame": ch1,
            "channel2": channel2, "walls": walls,
            "rows": [{"label": l, "query": q, "n": n} for l, q, n in rows],
            "refused": [{"label": l, "error": e} for l, e in errors]}
    (out / f"c3d-forward-channel-walls-{date}.json").write_text(json.dumps(blob, indent=2))

    lines = [f"# C.3.d forward-arm second channel and wall probes — {date}", "",
             "Generated by `source/build/goldset/346_c3d_forward_channel_and_walls.py`. Do not edit",
             "by hand; re-run the script.", "",
             f"C.3.d exposure axis: `{UNION_AXIS}`", "",
             f"Channel 1 (economics-of-education vocabulary): `{CHANNEL1}`", "",
             f"Forward arm on channel 1, inside the C.3.d frame: **{ch1}**", "",
             "## Channel 2 — the shocks that move the return, in each literature's own words", "",
             "A channel whose CONTROL is 0 is broken and its arm count is not evidence.", "",
             "| shock literature | control (alive?) | AND fertility | of which also channel-1 vocab |",
             "|---|---|---|---|"]
    for c in channel2:
        f = lambda v: "—" if v is None else f"{v:,}"
        lines.append(f"| {c['label']} | {f(c['control'])} | **{f(c['arm'])}** | {f(c['overlap_ch1'])} |")
    lines += ["", "## Walls, measured from both sides", "",
              "Overlap read from one side only says which frame is bigger, not where the estimands",
              "collide.", "",
              "| wall | neighbour frame | overlap with C.3.d's 762 | share of C.3.d | share of neighbour |",
              "|---|---|---|---|---|"]
    for w in walls:
        nb, ov = w["neighbour_frame"], w["overlap"]
        s_c = f"{100.0*ov/frame:.1f}%" if (ov is not None and frame) else "—"
        s_n = f"{100.0*ov/nb:.1f}%" if (ov is not None and nb) else "—"
        lines.append(f"| {w['label']} | {'—' if nb is None else f'{nb:,}'} | "
                     f"{'—' if ov is None else f'{ov:,}'} | {s_c} | {s_n} |")
    lines += ["", "## Every measurement", "", "| n | measurement | query |", "|---|---|---|"]
    for l, q, n in rows:
        lines.append(f"| **{n:,}** | {l} | `{q}` |")
    if errors:
        lines += ["", "## REFUSED — these are not zeros", ""]
        lines += [f"- {l}: {e}" for l, e in errors]
    else:
        lines += ["", "No refused requests: every count above is a measurement, not a failure."]
    (out / f"c3d-forward-channel-walls-{date}.md").write_text("\n".join(lines) + "\n")
    print(f"\nwrote literature/search-logs/c3d-forward-channel-walls-{date}.{{json,md}}")
    dead = [c["label"] for c in channel2 if not c["control"]]
    if dead:
        print(f"  ! BROKEN CHANNELS (control returned 0 or refused): {dead}", file=sys.stderr)
    if errors:
        print(f"WARNING: {len(errors)} refused request(s) — not counted as zeros", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
