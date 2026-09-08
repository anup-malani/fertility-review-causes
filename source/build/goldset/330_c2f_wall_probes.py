#!/usr/bin/env python3
"""
330 — C.2.f (TICK-081) stage-2: numbers for the boundary walls 328/329 left unmeasured.

328 measured the C.3.d, D.2.d and C.6.a walls inside the fertility-restricted frame (8, 3, 15).
Four more walls carry no number yet, and a wall written without one is an assumption:

  C.1.a  own income vs position in the distribution
  C.5.a  dispersion vs individual-level income risk
  D.3.c  Kearney-Levine's "economic despair" teen-birth arm (328 got 18 on one vocabulary)
  homonym  "inequality" in this frame that is GENDER / health / educational inequality, which is
           D.2.a's estimand and not a distribution statistic at all

Also splits the frame by DIRECTION OF CAUSATION. C.2.f needs inequality as the cause; a large part
of the demographic inequality-and-fertility literature runs the other way (differential fertility as
a cause of inequality) or is a cross-sectional gradient. Those are context, not the primary cell,
and they should be sized before the screen rubric is written rather than discovered during it.

Same Refused discipline as 328/329: a throttled or failed request never reaches a counter as a zero.
"""
import json, subprocess, sys, urllib.parse, datetime, pathlib, time

MAILTO = "shravanh@uchicago.edu"
BASE = "https://api.openalex.org/works"
OUTCOME_WIDE = ('("fertility" OR "childbearing" OR "birth rate" OR "total fertility rate" '
                'OR "family size" OR "number of children")')
INEQ = '"income inequality"'


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


class Refused(Exception):
    pass


def count(query):
    url = (f"{BASE}?filter=title_and_abstract.search:{urllib.parse.quote(query, safe='')}"
           f"&per_page=1&mailto={MAILTO}")
    if API_KEY:
        url += f"&api_key={API_KEY}"
    p = subprocess.run(["curl", "-s", "-S", "--max-time", "60", url], capture_output=True, text=True)
    if p.returncode != 0:
        raise Refused(f"curl exit {p.returncode}")
    try:
        d = json.loads(p.stdout)
    except json.JSONDecodeError:
        raise Refused(f"non-JSON: {p.stdout[:160]!r}")
    if "error" in d:
        raise Refused(f"api error: {d.get('error')} {d.get('message','')}")
    try:
        return d["meta"]["count"]
    except (KeyError, TypeError):
        raise Refused("no meta.count")


def measure(label, query, rows, errors):
    try:
        try:
            n = count(query)
        except Refused as first:
            if "Rate limit" not in str(first):
                raise
            time.sleep(2.0)
            n = count(query)
        rows.append((label, query, n)); print(f"  {n:>7,}  {label}")
    except Refused as e:
        errors.append((label, str(e))); print(f"  REFUSED  {label}: {e}", file=sys.stderr)
    time.sleep(PACE)


def main():
    date = datetime.date.today().isoformat()
    rows, errors = [], []
    F = f"{INEQ} AND {OUTCOME_WIDE}"

    print("\n== baseline ==")
    measure("the 'income inequality' arm of the frame (328 got 635)", F, rows, errors)

    print("\n== walls, inside the fertility-restricted frame ==")
    for label, extra in [
        ("C.1.a own-income / income-effect vocabulary",
         '("income effect" OR "household income" OR "family income" OR "income elasticity")'),
        ("C.5.a uncertainty / unemployment vocabulary",
         '("economic uncertainty" OR "unemployment" OR "job insecurity" OR "precarity")'),
        ("D.3.c despair / teen-birth vocabulary (2nd wording)",
         '("despair" OR "hopelessness" OR "economic despair" OR "teen birth" OR "adolescent childbearing")'),
        ("C.2.h digital / social-media reference group",
         '("social media" OR "internet use" OR "smartphone")'),
    ]:
        measure(f"WALL {label}", f"{F} AND {extra}", rows, errors)

    print("\n== homonym: 'inequality' that is not a distribution statistic ==")
    for label, q in [
        ("gender inequality arm (D.2.a's estimand)",
         f'("gender inequality" OR "gender equity" OR "gender gap") AND {OUTCOME_WIDE}'),
        ("gender arm INSIDE the income-inequality frame",
         f'{F} AND ("gender inequality" OR "gender equity" OR "gender gap")'),
        ("health / educational inequality inside the frame",
         f'{F} AND ("health inequality" OR "health disparities" OR "educational inequality")'),
    ]:
        measure(f"HOMONYM {label}", q, rows, errors)

    print("\n== direction of causation: C.2.f needs inequality as the CAUSE ==")
    for label, q in [
        ("fertility as a cause of inequality (wrong direction)",
         f'{F} AND ("differential fertility" OR "fertility differentials" OR "assortative mating")'),
        ("cross-sectional gradient (context, not an effect)",
         f'{F} AND ("income gradient" OR "socioeconomic gradient" OR "socioeconomic status")'),
        ("policy/quasi-experimental language inside the frame",
         f'{F} AND ("natural experiment" OR "difference-in-differences" OR "instrumental variable" '
         f'OR "regression discontinuity" OR "randomized")'),
    ]:
        measure(f"DIRECTION {label}", q, rows, errors)

    out = pathlib.Path("literature/search-logs"); out.mkdir(parents=True, exist_ok=True)
    (out / f"c2f-wall-probes-{date}.json").write_text(json.dumps(
        {"date": date, "script": "330_c2f_wall_probes.py", "frame": F,
         "rows": [{"label": l, "query": q, "n": n} for l, q, n in rows],
         "refused": [{"label": l, "error": e} for l, e in errors]}, indent=2))
    lines = [f"# C.2.f wall probes — {date}", "",
             "Generated by `source/build/goldset/330_c2f_wall_probes.py`. Do not edit by hand.",
             f"All rows except the homonym gender arm sit inside `{F}`.", "",
             "| n | measurement | query |", "|---|---|---|"]
    for l, q, n in rows:
        lines.append(f"| **{n:,}** | {l} | `{q}` |")
    lines += ["", ("No refused requests: every count is a measurement, not a failure."
                   if not errors else "## REFUSED — not zeros\n\n"
                   + "\n".join(f"- {l}: {e}" for l, e in errors))]
    (out / f"c2f-wall-probes-{date}.md").write_text("\n".join(lines) + "\n")
    print(f"\nwrote literature/search-logs/c2f-wall-probes-{date}.{{json,md}}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
