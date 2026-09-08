#!/usr/bin/env python3
"""
329 — C.2.f (TICK-081) stage-2: a SECOND vocabulary for the two findings 328 produced.

328 found (a) 89% of C.2.f's 716-record union frame is carried by one general-purpose term,
"income inequality", and (b) the mechanism's middle link -- inequality raising required
investment per child -- returns 3 records fertility-restricted. Both are negative findings, and
a negative finding is only as good as the vocabulary that produced it:

  empty-cell-needs-second-channel — C.3.g's "no natural experiment exists" was two missing words.
  channels-must-fail-differently — a search null counts only if the channels die for unrelated
      reasons. Test the filter on a known positive first.
  policy-literatures-indexed-in-local-vocabulary — a correctly named design can be unfindable
      under the name we use for it.

So: re-ask both questions in vocabulary that shares no term with 328. The exposure axis is
re-asked in DISTRIBUTION-STATISTIC language rather than the phrase "income inequality", and the
middle link in the language the education and consumption literatures actually use (shadow
education, private tutoring, enrichment, positional/conspicuous consumption, relative
deprivation) rather than the phrase "child investment".

Known-positive controls run FIRST. If they come back empty the channel is broken and every zero
below is uninterpretable.
"""
import json, os, subprocess, sys, urllib.parse, datetime, pathlib, time

MAILTO = "shravanh@uchicago.edu"
BASE = "https://api.openalex.org/works"
OUTCOME_WIDE = ('("fertility" OR "childbearing" OR "birth rate" OR "total fertility rate" '
                'OR "family size" OR "number of children")')


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
    """A failed request. Never let this reach a counter as a zero."""


def count(query):
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
        raise Refused(f"no meta.count: {p.stdout[:200]!r}")


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
        print(f"  {n:>8,}  {label}")
    except Refused as e:
        errors.append((label, str(e)))
        print(f"  REFUSED   {label}: {e}", file=sys.stderr)
    time.sleep(PACE)


def main():
    date = datetime.date.today().isoformat()
    rows, errors = [], []

    print("\n== known-positive controls: the channel must find things it should find ==")
    for label, q in [
        ("control: quantity-quality tradeoff exists (C.3.d's literature)",
         f'("quantity-quality" OR "child quality") AND {OUTCOME_WIDE}'),
        ("control: intensive parenting exists (D.2.d, a drafted chapter)",
         f'("intensive parenting" OR "concerted cultivation") AND {OUTCOME_WIDE}'),
        ("control: shadow education exists as a literature at all", '"shadow education"'),
    ]:
        measure(label, q, rows, errors)

    print("\n== exposure axis re-asked as DISTRIBUTION STATISTICS (no phrase shared with 328) ==")
    for label, q in [
        ("Gini", f'"Gini" AND {OUTCOME_WIDE}'),
        ("top income share", f'("top income share" OR "top 1 percent" OR "income concentration") AND {OUTCOME_WIDE}'),
        ("wage/income dispersion", f'("wage dispersion" OR "income dispersion" OR "earnings inequality") AND {OUTCOME_WIDE}'),
        ("relative deprivation", f'"relative deprivation" AND {OUTCOME_WIDE}'),
        ("status anxiety / positional externality", f'("status anxiety" OR "positional externality" OR "conspicuous consumption") AND {OUTCOME_WIDE}'),
    ]:
        measure(label, q, rows, errors)

    print("\n== the MIDDLE LINK re-asked in education/consumption vocabulary ==")
    for label, q in [
        ("shadow education / private tutoring x inequality",
         '("shadow education" OR "private tutoring" OR "cram school") AND ("inequality" OR "competition")'),
        ("enrichment / extracurricular spending x inequality",
         '("enrichment expenditure" OR "extracurricular" OR "enrichment activities") AND ("inequality" OR "income distribution")'),
        ("educational arms race, bare (328 got 16)", '("educational arms race" OR "credential inflation")'),
        ("parental spending responds to inequality",
         '("parental spending" OR "parental investment" OR "educational spending") AND ("income inequality" OR "Gini" OR "top income share")'),
    ]:
        measure(label, q, rows, errors)

    print("\n== the FULL CHAIN: does any record carry exposure AND middle link AND outcome? ==")
    for label, q in [
        ("distribution stat AND investment AND fertility",
         f'("Gini" OR "income inequality" OR "top income share") AND '
         f'("parental investment" OR "child investment" OR "educational spending" OR "private tutoring") AND {OUTCOME_WIDE}'),
        ("status/positional AND investment AND fertility",
         f'("status competition" OR "relative status" OR "social comparison" OR "positional") AND '
         f'("parental investment" OR "child investment" OR "educational spending") AND {OUTCOME_WIDE}'),
    ]:
        measure(label, q, rows, errors)

    out = pathlib.Path("literature/search-logs")
    out.mkdir(parents=True, exist_ok=True)
    blob = {"date": date, "script": "329_c2f_second_channel.py",
            "outcome_axis_wide": OUTCOME_WIDE,
            "rows": [{"label": l, "query": q, "n": n} for l, q, n in rows],
            "refused": [{"label": l, "error": e} for l, e in errors]}
    (out / f"c2f-second-channel-{date}.json").write_text(json.dumps(blob, indent=2))
    lines = [f"# C.2.f second-channel probe — {date}", "",
             "Generated by `source/build/goldset/329_c2f_second_channel.py`. Do not edit by hand.",
             "A second vocabulary for the two negative findings in `328`, sharing no phrase with them.",
             "", "| n | measurement | query |", "|---|---|---|"]
    for l, q, n in rows:
        lines.append(f"| **{n:,}** | {l} | `{q}` |")
    lines += ["", ("No refused requests: every count above is a measurement, not a failure."
                   if not errors else "## REFUSED — these are not zeros\n\n"
                   + "\n".join(f"- {l}: {e}" for l, e in errors))]
    (out / f"c2f-second-channel-{date}.md").write_text("\n".join(lines) + "\n")
    print(f"\nwrote literature/search-logs/c2f-second-channel-{date}.{{json,md}}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
