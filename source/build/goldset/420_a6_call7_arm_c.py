#!/usr/bin/env python3
"""
420 — A.6 (TICK-087): size the recall gap created by PI call 7, reading (a).

The ruling and what it changes. Call 7 was ruled **no** — no `MIXED_NORM_MARRIAGE` cell and no
D.2.b wall — under reading **(a)**: norms about premarital sex and out-of-wedlock childbearing fall
*inside* A.6's exposure rather than outside it. For the screened records that is a no-op; Ragan
2012 stays `LINK_NORM_USE` and nothing is reclassified.

But it is not a no-op for **retrieval**. §A.6's registered object is "contraception and abortion",
and both retrieval arms frozen in §14 were built on that object:

    ARM A   compound-stigma phrases  AND  (contraception OR contraceptive OR abortion OR
                                           family planning OR birth control)
    ARM B   opposition / unmet-need  AND  the same object block

Under reading (a) the exposure also covers stigma whose object is the *behaviour* — premarital sex,
nonmarital childbearing, illegitimacy — with contraception as the response to it rather than the
thing disapproved of. Ragan is exactly that shape: her regressor is historical out-of-wedlock
childbearing, and she is in the pool only because the snowball reached her from a seed, not because
either arm's vocabulary would have found her. So the ruling widens the estimand without widening
the search, which is a recall gap and has to be measured before the chapter claims a ceiling
(`frame-growth-is-not-frame-gain`, read in the direction the ruling forces).

What this measures
------------------
  ARM C     a behaviour-object block AND the same stigma vocabulary, no outcome block, matching
            §14's design decision to screen for the outcome rather than retrieve on it.
  overlap   ARM C against ARM A and ARM B separately, so the union can be computed exactly by
            inclusion-exclusion rather than guessed.
  anchors   whether ARM C reaches Ragan 2012 (`W2187750596`) and the two premarital-sex records
            already screened, as a positive control on the block: a behaviour-object block that
            cannot reach the very record that prompted the call is the wrong block.

If ARM C's marginal contribution is small, §14's ceiling stands and the ruling costs nothing. If it
is large, the chapter has an unscreened arm and §14's "9 of 15" recall figure is no longer the
ceiling it claims to be.
"""
import json, subprocess, sys, urllib.parse, datetime, pathlib, time

MAILTO = "shravanh@uchicago.edu"
BASE = "https://api.openalex.org/works"
LOGDIR = pathlib.Path("literature/search-logs")
CACHE = pathlib.Path("temp/a6-arm-c-cache.json")


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

OBJECT = ('("contraception" OR "contraceptive" OR "abortion" OR "family planning" '
          'OR "birth control")')
STIGMA_COMPOUND = ('("abortion stigma" OR "contraceptive stigma" OR "contraception stigma" '
                   'OR "family planning stigma")')
OPPOSITION = ('("unmet need" OR "reasons for nonuse" OR "reasons for non-use" '
              'OR "opposition to use" OR "husband opposition" OR "partner opposition" '
              'OR "religious objection" OR "moral objection" OR "disapproval" '
              'OR "social acceptability" OR "legitimation" OR "normative approval")')
# The stigma vocabulary, for pairing with a behaviour object rather than a method object.
STIGMA_WIDE = ('("stigma" OR "taboo" OR "social disapproval" OR "moral opposition" '
               'OR "disapproval" OR "shame" OR "social sanction" OR "illegitimacy")')
# The behaviour object that reading (a) brings inside A.6.
BEHAVIOUR = ('("premarital sex" OR "pre-marital sex" OR "nonmarital childbearing" '
             'OR "non-marital childbearing" OR "out-of-wedlock" OR "out of wedlock" '
             'OR "unwed motherhood" OR "unmarried motherhood" OR "illegitimate birth" '
             'OR "teenage pregnancy")')

ARM_A = f"{STIGMA_COMPOUND} AND {OBJECT}"
ARM_B = f"{OPPOSITION} AND {OBJECT}"
ARM_C = f"{STIGMA_WIDE} AND {BEHAVIOUR}"
QUERIES = {
    "ARM A (frozen)": ARM_A,
    "ARM B (frozen)": ARM_B,
    "ARM A intersect ARM B": f"{STIGMA_COMPOUND} AND {OPPOSITION} AND {OBJECT}",
    "ARM C (call 7 reading a)": ARM_C,
    "ARM C intersect ARM A": f"{STIGMA_WIDE} AND {BEHAVIOUR} AND {STIGMA_COMPOUND} AND {OBJECT}",
    "ARM C intersect ARM B": f"{STIGMA_WIDE} AND {BEHAVIOUR} AND {OPPOSITION} AND {OBJECT}",
    "ARM C AND a method object": f"{STIGMA_WIDE} AND {BEHAVIOUR} AND {OBJECT}",
    "ARM C AND a fertility outcome":
        f"{STIGMA_WIDE} AND {BEHAVIOUR} AND "
        '("fertility" OR "childbearing" OR "birth rate" OR "total fertility rate" '
        'OR "family size" OR "number of children")',
    "ARM C AND identified-design markers":
        f"{STIGMA_WIDE} AND {BEHAVIOUR} AND "
        '("instrumental variable" OR "difference-in-differences" OR "natural experiment" '
        'OR "regression discontinuity" OR "randomized controlled trial" OR "event study")',
}
# Positive control: ARM C must reach the record that prompted the call.
ANCHORS = {"W2187750596": "Ragan 2012, out-of-wedlock norms and Pill demand — prompted call 7",
           "W4224236986": "McLoughlin Brooks and Weitzman 2022 — measures disapproval of premarital sex",
           "W2562118812": "S4 record on abortion stigma, as a negative-ish control"}


class Refused(Exception):
    """A failed request. Never let this reach a counter as a zero."""


def _cache():
    try:
        return json.loads(CACHE.read_text())
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def _get(qs, cache, _retried=False):
    if qs in cache:
        return cache[qs]
    url = f"{BASE}?{qs}&mailto={MAILTO}" + (f"&api_key={API_KEY}" if API_KEY else "")
    p = subprocess.run(["curl", "-s", "-S", "--max-time", "60", url],
                       capture_output=True, text=True)
    if p.returncode != 0:
        raise Refused(f"curl exit {p.returncode}")
    try:
        d = json.loads(p.stdout)
    except json.JSONDecodeError:
        raise Refused(f"non-JSON: {p.stdout[:120]!r}")
    if "error" in d:
        if not _retried and "rate" in str(d.get("error", "")).lower():
            time.sleep(5.0)
            return _get(qs, cache, _retried=True)
        raise Refused(str(d.get("error")))
    if "meta" not in d:
        raise Refused("no meta")
    cache[qs] = d
    CACHE.parent.mkdir(parents=True, exist_ok=True)
    CACHE.write_text(json.dumps(cache))
    time.sleep(PACE)
    return d


def size(q, cache):
    return _get(f"filter=title_and_abstract.search:{urllib.parse.quote(q, safe='')}&per_page=1",
                cache)["meta"]["count"]


def reach(wid, q, cache):
    return _get(f"filter=openalex:{wid},title_and_abstract.search:"
                f"{urllib.parse.quote(q, safe='')}&per_page=1&select=id", cache)["meta"]["count"] == 1


def main():
    cache, R, refusals = _cache(), {}, []
    for label, q in QUERIES.items():
        try:
            R[label] = size(q, cache)
            print(f"  {R[label]:>8}  {label}", flush=True)
        except Refused as e:
            refusals.append((label, str(e)))
            R[label] = None
            print(f"  REFUSED  {label} ({e})", file=sys.stderr, flush=True)

    a, b, ab = R["ARM A (frozen)"], R["ARM B (frozen)"], R["ARM A intersect ARM B"]
    c, ca, cb = R["ARM C (call 7 reading a)"], R["ARM C intersect ARM A"], R["ARM C intersect ARM B"]
    if None not in (a, b, ab, c, ca, cb):
        R["union A+B (frozen, §14)"] = a + b - ab
        # Inclusion-exclusion over three sets needs the triple intersection; bound it instead.
        R["union A+B+C, upper bound"] = a + b - ab + c - ca - cb
        R["ARM C marginal, upper bound"] = c - ca - cb
        print(f"\n  frozen union A+B = {R['union A+B (frozen, §14)']:,}")
        print(f"  ARM C marginal contribution <= {R['ARM C marginal, upper bound']:,} "
              f"({100 * R['ARM C marginal, upper bound'] / R['union A+B (frozen, §14)']:.0f}% of "
              f"the frozen union)")

    print("\npositive control — does ARM C reach the records that prompted the ruling?", flush=True)
    for wid, why in ANCHORS.items():
        try:
            for label, q in (("ARM C", ARM_C), ("ARM A", ARM_A), ("ARM B", ARM_B)):
                R[f"{label} reaches {wid}"] = reach(wid, q, cache)
            print(f"  {wid}  C={'y' if R[f'ARM C reaches {wid}'] else 'n'} "
                  f"A={'y' if R[f'ARM A reaches {wid}'] else 'n'} "
                  f"B={'y' if R[f'ARM B reaches {wid}'] else 'n'}   {why[:62]}", flush=True)
        except Refused as e:
            refusals.append((wid, str(e)))

    stamp = datetime.date.today().isoformat()
    LOGDIR.mkdir(parents=True, exist_ok=True)
    (LOGDIR / f"a6-arm-c-{stamp}.json").write_text(json.dumps(
        {"generated": stamp, "script": "source/build/goldset/420_a6_call7_arm_c.py",
         "ruling": "PI call 7 = no cell, no wall, reading (a): premarital-sex and out-of-wedlock "
                   "norms fall INSIDE A.6's exposure",
         "queries": QUERIES, "counts": R,
         "refusals": [{"label": l, "error": e} for l, e in refusals]}, indent=1))

    md = [f"# A.6 ARM C — the recall gap opened by PI call 7 — {stamp}", "",
          "Generated by `source/build/goldset/420_a6_call7_arm_c.py`. Do not edit by hand;",
          "re-run the script.", "",
          "Call 7 was ruled **no cell and no wall**, under reading **(a)**: norms about premarital",
          "sex and out-of-wedlock childbearing fall *inside* A.6's exposure. For already-screened",
          "records that is a no-op. For **retrieval** it is not: both arms frozen in §14 were built",
          "on the registry's literal object, \"contraception and abortion\", and reading (a) admits",
          "stigma whose object is the *behaviour*, with contraception as the response. Ragan 2012 is",
          "that shape and is in the pool only because the snowball reached her from a seed.", "",
          "**No production query has been run and no record screened.** These are frame sizes.", ""]
    if refusals:
        md += [f"**{len(refusals)} REFUSED.** Missing, not zero.", ""]
    md += ["| frame | records |", "|---|---|"]
    for k, v in R.items():
        if isinstance(v, int):
            md.append(f"| {k} | {v:,} |")
    md += ["", "## Positive control", "",
           "A behaviour-object block that cannot reach the record which prompted the ruling is the",
           "wrong block.", "", "| record | ARM C | ARM A | ARM B | why it is here |",
           "|---|---|---|---|---|"]
    for wid, why in ANCHORS.items():
        y = lambda k: ("yes" if R.get(k) else "**no**") if R.get(k) is not None else "REFUSED"
        md.append(f"| `{wid}` | {y(f'ARM C reaches {wid}')} | {y(f'ARM A reaches {wid}')} | "
                  f"{y(f'ARM B reaches {wid}')} | {why} |")
    (LOGDIR / f"a6-arm-c-{stamp}.md").write_text("\n".join(md) + "\n")
    print(f"\nwrote {LOGDIR}/a6-arm-c-{stamp}.{{json,md}}")
    return 1 if refusals else 0


if __name__ == "__main__":
    sys.exit(main())
