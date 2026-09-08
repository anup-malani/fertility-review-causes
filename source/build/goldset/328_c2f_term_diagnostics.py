#!/usr/bin/env python3
"""
328 — C.2.f (TICK-081) stage-2 diagnostic: score every exposure term ALONE.

Why this exists. The 2026-09-03 candidate frame probe ranked C.2.f on a UNION frame of 714
records, built as (7-term exposure axis) AND (fertility outcome axis). That number ranks the
candidate; it does not tell you which term earned it. Two lessons say measure before trusting:

  anchored-vocabulary-has-own-homonym — score each anchor term alone; on A.17 one term carried
      94% of the contamination while the block looked fine.
  calibrate-the-outcome-axis-too — the outcome axis needs the same treatment; on C.3.e "parity"
      was half the frame for zero gold.

The specific worry here is NOT C.2.b's kind of homonym (a shared phrase owned by another field,
which the fertility restriction removes). It is a within-field scope problem: "income inequality"
AND "fertility" is a large and genuinely demographic literature that is mostly NOT about status
competition in child investment — inequality as a CONSEQUENCE of differential fertility, income
gradients in fertility, inequality and teen childbearing (which is D.3.c's and C.6.a's estimand).
The fertility axis cannot separate those, because they are about fertility.

Outputs literature/search-logs/c2f-term-diagnostics-<date>.{json,md}. Counting only — no records
are retained, so this is cheap and re-runnable.

Gotchas honoured (all recorded from earlier chapters):
  - a comma inside a filter VALUE is fatal and %2C does not save it -> no commas in any term
  - a phrase beginning "not" parses as boolean NOT -> none here
  - "?" in a search value is a wildcard and 200s with a misleading body -> none here
  - OpenAlex drops stopwords inside phrases -> noted per term where it could bite
  - this Python has no CA bundle: shell out to curl rather than urllib (refusals-read-as-zeros)
"""
import json, os, subprocess, sys, urllib.parse, datetime, pathlib, time

MAILTO = "shravanh@uchicago.edu"
BASE = "https://api.openalex.org/works"

# OpenAlex throttles queries with >5 boolean operators to 1 req/s unauthenticated, 5 req/s with a
# key. Every query here is over that threshold. A first run at 0.2s spacing had 6 of 24 requests
# refused -- which the Refused path correctly kept OUT of the counts rather than recording as 0.
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

# The seven terms of the 2026-09-03 UNION axis for C.2.f, verbatim.
TERMS = [
    "income inequality",
    "status competition",
    "positional competition",
    "positional good",
    "relative status",
    "social comparison",
    "educational arms race",
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
    except Refused as e:
        errors.append((label, str(e)))
        print(f"  REFUSED   {label}: {e}", file=sys.stderr)
    time.sleep(PACE)


def main():
    date = datetime.date.today().isoformat()
    rows, errors = [], []

    print("\n== control: the channel must be alive before any zero is believed ==")
    measure("CONTROL fertility decline", '"fertility decline"', rows, errors)
    measure("CONTROL C.2.f union frame (reproduces the 09-03 number)",
            f"{UNION_AXIS} AND {OUTCOME_WIDE}", rows, errors)

    print("\n== each exposure term ALONE, fertility-restricted ==")
    for t in TERMS:
        measure(f"TERM {t}", f'"{t}" AND {OUTCOME_WIDE}', rows, errors)

    print("\n== each term alone, UNRESTRICTED (how much of it is even demographic) ==")
    for t in TERMS:
        measure(f"BARE {t}", f'"{t}"', rows, errors)

    print("\n== the axis WITHOUT its largest term ==")
    minus = "(" + " OR ".join(f'"{t}"' for t in TERMS if t != "income inequality") + ")"
    measure("AXIS minus 'income inequality'", f"{minus} AND {OUTCOME_WIDE}", rows, errors)

    print("\n== within-field scope probes: fertility literatures that are NOT this mechanism ==")
    scope = [
        ("inequality as CONSEQUENCE of differential fertility",
         '"income inequality" AND ("differential fertility" OR "fertility differentials")'),
        ("income gradient in fertility",
         '"income inequality" AND ("income gradient" OR "socioeconomic gradient" OR "education gradient")'),
        ("teen childbearing arm (D.3.c / C.6.a estimand)",
         '"income inequality" AND ("teen birth" OR "teenage childbearing" OR "teen childbearing")'),
        ("boundary INSIDE the frame: C.3.d quantity-quality vocabulary",
         f'{UNION_AXIS} AND {OUTCOME_WIDE} AND ("quantity-quality" OR "child quality" OR "child investment")'),
        ("boundary INSIDE the frame: D.2.d intensive-parenting vocabulary",
         f'{UNION_AXIS} AND {OUTCOME_WIDE} AND ("intensive parenting" OR "concerted cultivation")'),
        ("boundary INSIDE the frame: C.6.a Easterlin vocabulary",
         f'{UNION_AXIS} AND {OUTCOME_WIDE} AND ("Easterlin" OR "relative income" OR "cohort size")'),
        ("the MIDDLE LINK: inequality -> investment per child",
         '"income inequality" AND ("investment per child" OR "child investment" OR "parental investment")'),
        ("the MIDDLE LINK, fertility-restricted",
         f'"income inequality" AND {OUTCOME_WIDE} AND ("investment per child" OR "child investment" OR "parental investment")'),
    ]
    for label, q in scope:
        measure(f"SCOPE {label}", q, rows, errors)

    out = pathlib.Path("literature/search-logs")
    out.mkdir(parents=True, exist_ok=True)
    blob = {"date": date, "script": "328_c2f_term_diagnostics.py",
            "outcome_axis_wide": OUTCOME_WIDE, "union_axis": UNION_AXIS,
            "rows": [{"label": l, "query": q, "n": n} for l, q, n in rows],
            "refused": [{"label": l, "error": e} for l, e in errors]}
    (out / f"c2f-term-diagnostics-{date}.json").write_text(json.dumps(blob, indent=2))

    lines = [f"# C.2.f term diagnostics — {date}", "",
             "Generated by `source/build/goldset/328_c2f_term_diagnostics.py`. Do not edit by hand.",
             "Counts are OpenAlex `title_and_abstract.search` record counts.", "",
             f"Outcome axis (wide): `{OUTCOME_WIDE}`", "",
             "| n | measurement | query |", "|---|---|---|"]
    for l, q, n in rows:
        lines.append(f"| **{n:,}** | {l} | `{q}` |")
    if errors:
        lines += ["", "## REFUSED — these are not zeros", ""]
        lines += [f"- {l}: {e}" for l, e in errors]
    else:
        lines += ["", "No refused requests: every count above is a measurement, not a failure."]
    (out / f"c2f-term-diagnostics-{date}.md").write_text("\n".join(lines) + "\n")

    print(f"\nwrote literature/search-logs/c2f-term-diagnostics-{date}.{{json,md}}")
    if errors:
        print(f"WARNING: {len(errors)} refused request(s) — not counted as zeros", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
