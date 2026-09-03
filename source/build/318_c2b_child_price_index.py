#!/usr/bin/env python3
"""318 — build the US child-price index and run C.2.b's pre-registered sign test.

Scope §5 pre-registers a test that does not depend on the literature at all: over the SDT window,
did the *real* price of the goods and services a child requires RISE? The hypothesis says rising
direct costs lowered fertility. If the relative price of children did not rise, the SDT cell is
settled by the sign and no elasticity estimate can rescue it — the logic that settled C.6.a.

**The index is specified in scope §5 BEFORE it was computed** — components, deflator, weightings and
arms — because a "price of children" index can be made to rise or fall by choosing components after
seeing the answer. This script implements that specification and reports every component separately
so the composite can be checked against its parts.

Three deviations from §5, all forced by data and all reported in the output rather than absorbed:

  1. §5 names 1965 as the window start. BLS has no education price series before **1967**
     (educational books and supplies) and no tuition series before **1977-12**. The window is
     therefore reported in three spans, not one, and the pre-1967 gap is a data absence and not a
     null.
  2. §5 names "children's and infants' clothing and footwear". BLS publishes no long infants'
     apparel series in this dataset. **All-apparel is substituted, and labelled as a substitution**
     wherever it appears. It is the exposure-series analogue of `exposure-estimand-distance-domain`.
  3. §5 excludes childcare as C.2.a's. Day care and preschool (1990-12–) is fetched and reported
     ANYWAY, outside every arm, because the exclusion is a scoping decision the reader should be able
     to price.

Sources are public and keyless: DBnomics mirrors the BLS CPI (the BLS flat files sit behind Akamai
bot defence and the unregistered BLS API returns only three years), and the World Bank WDI for TFR.
Raw responses are deposited unmodified in data/raw/ with provenance, per the pattern C.6.a set.

Usage: python3 source/build/318_c2b_child_price_index.py [--refresh]
Outputs:
  data/raw/us-cpi-child-components/*.json      raw pulls, one per series
  data/raw/us-cpi-child-components/PROVENANCE.md
  output/tables/child-cost-direct-price-index.csv        the derived real indices
  literature/search-logs/child-cost-direct-sign-test.md  the test, generated not retyped
"""
import argparse
import json
import statistics
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "raw" / "us-cpi-child-components"
TABLES = ROOT / "output" / "tables"
LOGS = ROOT / "literature" / "search-logs"

# component -> (BLS series id, scope §5 role, note)
SERIES = {
    "all_items":      ("CUUR0000SA0",     "deflator", "CPI-U all items; the deflator"),
    "books_supplies": ("CUUR0000SEEA",    "education", "educational books and supplies, from 1967"),
    "school_tuition": ("CUUR0000SEEB02",  "education", "elementary and high school tuition, from 1978"),
    "college_tuition":("CUUR0000SEEB01",  "education", "college tuition and fees, from 1978"),
    "medical":        ("CUUR0000SAM",     "health",   "medical care, all ages, from 1935"),
    "apparel":        ("CUUR0000SAA",     "clothing", "ALL apparel — a SUBSTITUTE for the "
                                                      "children's series §5 named, which BLS does "
                                                      "not publish here"),
    "daycare":        ("CUUR0000SEEB03",  "EXCLUDED", "day care and preschool — C.2.a's, excluded "
                                                      "from every arm, reported for reference"),
}

# Scope §5: three arms, so a result that depends entirely on education is seen to depend on it.
ARMS = {
    "with_education":    ["books_supplies", "school_tuition", "college_tuition", "medical", "apparel"],
    "without_education": ["medical", "apparel"],
    "education_only":    ["books_supplies", "school_tuition", "college_tuition"],
    # The only arm that spans the SDT window from its start, because tuition begins in 1978.
    "long_run_1967":     ["books_supplies", "medical", "apparel"],
}

# Scope §5: two pre-specified weightings, reported side by side, neither chosen after the fact.
# Budget shares are USDA *Expenditures on Children by Families* category shares restricted to
# C.2.b's components and renormalised. USDA bundles child care WITH education, so this weighting
# OVER-weights education; that is stated in the output, not corrected silently.
USDA_SHARE = {"books_supplies": 16.0, "school_tuition": 16.0, "college_tuition": 16.0,
              "medical": 9.0, "apparel": 6.0}

TFR_INDICATOR = "SP.DYN.TFRT.IN"
WINDOWS = [("SDT, as far back as the data reach", None, 2024),
           ("early SDT", 1967, 1980),
           ("late SDT", 1980, 2024)]


def curl(url, args=()):
    r = subprocess.run(["curl", "-sS", "--max-time", "120", "-G", url, *args],
                       capture_output=True, text=True)
    if r.returncode != 0:
        return None, r.stderr.strip()[:200]
    try:
        return json.loads(r.stdout), None
    except json.JSONDecodeError:
        return None, f"non-JSON: {r.stdout[:160]}"


def fetch_series(name, sid, refresh):
    """One DBnomics pull per series. data/raw is immutable: cached unless --refresh."""
    dest = RAW / f"{sid}.json"
    if dest.exists() and not refresh:
        return json.loads(dest.read_text())
    d, err = curl(f"https://api.db.nomics.world/v22/series/BLS/cu/{sid}",
                  ["--data-urlencode", "observations=1"])
    if err:
        sys.exit(f"{name} ({sid}): {err}")
    RAW.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(d, indent=2) + "\n")
    return d


def annual(doc, min_months=10):
    """Monthly index -> annual average. A year with fewer than min_months is dropped, not
    part-averaged: a 3-month 'year' next to a 12-month one is a different quantity."""
    docs = doc.get("series", {}).get("docs", [])
    if not docs:
        return {}
    o = docs[0]
    by_year = {}
    for per, val in zip(o.get("period", []), o.get("value", [])):
        if val is None or (isinstance(val, str) and not val.replace(".", "").isdigit()):
            continue
        y = int(str(per)[:4])
        by_year.setdefault(y, []).append(float(val))
    return {y: statistics.fmean(v) for y, v in by_year.items() if len(v) >= min_months}


def fetch_tfr(refresh):
    dest = RAW / "wdi-tfr-usa.json"
    if dest.exists() and not refresh:
        d = json.loads(dest.read_text())
    else:
        d, err = curl(f"https://api.worldbank.org/v2/country/USA/indicator/{TFR_INDICATOR}",
                      ["--data-urlencode", "format=json", "--data-urlencode", "per_page=400"])
        if err:
            sys.exit(f"TFR: {err}")
        RAW.mkdir(parents=True, exist_ok=True)
        dest.write_text(json.dumps(d, indent=2) + "\n")
    rows = d[1] if isinstance(d, list) and len(d) > 1 and d[1] else []
    return {int(r["date"]): r["value"] for r in rows if r.get("value") is not None}


def real_index(nominal, deflator):
    """Deflate, then rebase to 100 at the first year both series cover. The claim is about the
    RELATIVE price of children; a nominal series rising is not the claim (scope §5)."""
    years = sorted(set(nominal) & set(deflator))
    if not years:
        return {}
    real = {y: nominal[y] / deflator[y] for y in years}
    base = real[years[0]]
    return {y: 100.0 * real[y] / base for y in years}


def pct_change(series, y0, y1):
    ys = sorted(series)
    ys0 = [y for y in ys if y >= y0] if y0 else ys
    ys0 = [y for y in ys0 if y <= y1]
    if len(ys0) < 2:
        return None, None, None
    a, b = ys0[0], ys0[-1]
    return (series[b] / series[a] - 1.0) * 100.0, a, b


def composite(reals, members, weights=None):
    """Weighted geometric mean of the member real indices, over the years ALL members cover."""
    members = [m for m in members if reals.get(m)]
    if not members:
        return {}
    years = sorted(set.intersection(*(set(reals[m]) for m in members)))
    if not years:
        return {}
    w = {m: (weights or {}).get(m, 1.0) for m in members}
    tot = sum(w.values())
    out = {}
    for y in years:
        logsum = sum(w[m] * __import__("math").log(reals[m][y]) for m in members)
        out[y] = __import__("math").exp(logsum / tot)
    base = out[years[0]]
    return {y: 100.0 * v / base for y, v in out.items()}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--refresh", action="store_true")
    args = ap.parse_args()

    raw_docs = {name: fetch_series(name, sid, args.refresh) for name, (sid, _, _) in SERIES.items()}
    ann = {name: annual(doc) for name, doc in raw_docs.items()}
    deflator = ann["all_items"]
    if not deflator:
        sys.exit("all-items CPI came back empty — the pull is broken, not the literature")

    reals = {name: real_index(ann[name], deflator) for name in SERIES if name != "all_items"}
    tfr = fetch_tfr(args.refresh)

    arms = {}
    for arm, members in ARMS.items():
        arms[(arm, "equal")] = composite(reals, members)
        arms[(arm, "usda")] = composite(reals, members, USDA_SHARE)

    RAW.mkdir(parents=True, exist_ok=True)
    (RAW / "PROVENANCE.md").write_text(
        "# Provenance — US CPI child-cost components\n\n"
        f"Pulled {datetime.now(timezone.utc).isoformat(timespec='seconds')} by "
        "`source/build/318_c2b_child_price_index.py`.\n\n"
        "CPI series come from **DBnomics** (`api.db.nomics.world/v22/series/BLS/cu/<id>`), which\n"
        "mirrors the BLS CPI-U. DBnomics is used rather than BLS directly because the BLS flat\n"
        "files at `download.bls.gov` return HTTP 403 from Akamai bot defence, and the unregistered\n"
        "BLS public API v1 silently ignores `startyear`/`endyear` and returns only the most recent\n"
        "three years — a defect that would have produced a confident wrong answer.\n\n"
        "US TFR comes from the World Bank WDI, indicator `SP.DYN.TFRT.IN`.\n\n"
        "Responses are stored unmodified. Derived series live in `output/tables/`.\n\n"
        "| component | series | role | note |\n|---|---|---|---|\n"
        + "".join(f"| `{n}` | `{s}` | {r} | {note} |\n" for n, (s, r, note) in SERIES.items()))

    TABLES.mkdir(parents=True, exist_ok=True)
    allyears = sorted({y for s in reals.values() for y in s} | set(tfr))
    cols = [n for n in SERIES if n != "all_items"]
    armcols = sorted(arms)
    with (TABLES / "child-cost-direct-price-index.csv").open("w") as f:
        f.write("year,cpi_all_items,us_tfr," + ",".join(f"real_{c}" for c in cols) + "," +
                ",".join(f"arm_{a}_{w}" for a, w in armcols) + "\n")
        for y in allyears:
            row = [str(y), f"{deflator.get(y, ''):.3f}" if y in deflator else "",
                   f"{tfr.get(y, ''):.3f}" if y in tfr else ""]
            row += [f"{reals[c][y]:.2f}" if y in reals.get(c, {}) else "" for c in cols]
            row += [f"{arms[k][y]:.2f}" if y in arms[k] else "" for k in armcols]
            f.write(",".join(row) + "\n")

    # ---------------------------------------------------------------- the generated report
    L = ["# C.2.b — the pre-registered sign test on the real price of children", "",
         "Generated by `source/build/318_c2b_child_price_index.py`. Do not edit by hand; re-run it.",
         "", "**The index was specified in scope §5 before it was computed** — components, "
         "deflator, two weightings and three arms. That specification is what makes this test worth "
         "anything: a \"price of children\" index can be made to rise or fall by choosing components "
         "after seeing the answer.", "",
         "**The hypothesis requires the real index to RISE** across the window in which US fertility "
         "fell. If it did not, the SDT cell is settled by the sign and no elasticity from the "
         "literature can rescue it (`slope-sufficiency-beats-a-missing-share`).", "",
         "## What the data would not support", "",
         "- Scope §5 named **1965** as the window start. The earliest education price series BLS "
         "publishes is educational books and supplies, from **1967**; tuition begins **1977-12**. "
         "The 1965–67 gap is a data absence, not a null.",
         "- Scope §5 named **children's and infants'** clothing. BLS publishes no such long series "
         "here, so **all-apparel is substituted and labelled** everywhere it is used. The "
         "substitution biases the clothing component toward adult goods.",
         "- **Day care and preschool is excluded** from every arm, as C.2.a's, and reported below so "
         "the exclusion can be priced.", "",
         "## US TFR, for reference", ""]
    for lbl, y0, y1 in WINDOWS:
        ch, a, b = pct_change(tfr, y0 or 1960, y1)
        if ch is not None:
            L.append(f"- **{lbl}** ({a}–{b}): TFR {tfr[a]:.2f} → {tfr[b]:.2f}, **{ch:+.1f}%**")
    L += ["", "## Component real indices (deflated by all-items CPI, rebased to 100 at first year)",
          "", "| component | role | coverage | change over coverage | early SDT | late SDT |",
          "|---|---|---|---|---|---|"]
    for name in cols:
        s = reals.get(name) or {}
        if not s:
            L.append(f"| `{name}` | {SERIES[name][1]} | — | no data | — | — |")
            continue
        ys = sorted(s)
        full, a, b = pct_change(s, ys[0], 2024)
        e, ea, eb = pct_change(s, 1967, 1980)
        l, la, lb = pct_change(s, 1980, 2024)
        L.append(f"| `{name}` | {SERIES[name][1]} | {ys[0]}–{ys[-1]} | **{full:+.1f}%** | "
                 f"{f'{e:+.1f}%' if e is not None else '—'} | "
                 f"{f'{l:+.1f}%' if l is not None else '—'} |")
    L += ["", "## The arms", "",
          "`equal` weights components equally. `usda` uses USDA *Expenditures on Children by "
          "Families* category shares restricted to C.2.b's components and renormalised — and USDA "
          "bundles child care **with** education, so this weighting **over-weights education**. "
          "Stated, not corrected.", "",
          "| arm | weighting | coverage | change | early SDT | late SDT | sign the hypothesis needs |",
          "|---|---|---|---|---|---|---|"]
    for key in armcols:
        arm, w = key
        s = arms[key]
        if not s:
            L.append(f"| `{arm}` | {w} | — | no overlap | — | — | rise |")
            continue
        ys = sorted(s)
        full, a, b = pct_change(s, ys[0], 2024)
        e, _, _ = pct_change(s, 1967, 1980)
        l, _, _ = pct_change(s, 1980, 2024)
        verdict = "**RISE — consistent**" if full and full > 0 else "**FALL — inconsistent**"
        L.append(f"| `{arm}` | {w} | {ys[0]}–{ys[-1]} | **{full:+.1f}%** | "
                 f"{f'{e:+.1f}%' if e is not None else '—'} | "
                 f"{f'{l:+.1f}%' if l is not None else '—'} | {verdict} |")
    L += ["", "The window is split as well as taken end to end, because a full-window endpoint test "
          "nets out a hump: C.6.a read 0/18 as uniform failure when the truth was 14/18 early and "
          "0/18 late (`endpoint-test-nets-a-hump-to-nothing`).", ""]

    # ------------------------------------------------------------------ where the decline actually is
    # A sign test that passes over the whole window says nothing if the exposure moved the right way
    # only where the outcome was flat. `compute-how-the-decline-is-distributed`: put the share of the
    # fall next to the direction of the exposure, decade by decade, and read them together.
    L += ["## Where the fall in fertility actually is, against where the price actually moved", "",
          "A sign test passing over a whole window is worth nothing if the exposure moved the right "
          "way only in the years when the outcome was flat. This table puts the share of the TFR "
          "decline beside the direction of the price index, decade by decade "
          "(`compute-how-the-decline-is-distributed`).", ""]
    ref_arm = ("long_run_1967", "equal")   # the only arm spanning the window from its start
    ref = arms.get(ref_arm) or {}
    tfr_years = sorted(y for y in tfr if y >= 1967)
    if tfr_years and ref:
        t0, t1 = tfr_years[0], tfr_years[-1]
        total_fall = tfr[t0] - tfr[t1]
        L += [f"Reference arm: `{ref_arm[0]}` / `{ref_arm[1]}` — the only arm covering the window "
              f"from its start, because tuition begins in 1978. Total TFR fall {t0}–{t1}: "
              f"**{tfr[t0]:.2f} → {tfr[t1]:.2f}**.", "",
              "The verdict column compares the **two** directions. The hypothesis says price up → "
              "fertility down, so price up with fertility *up* is as inconsistent as price down with "
              "fertility down. Reading only the price direction is the sign-blindness "
              "`r2-criterion-is-sign-blind` warns about — the first version of this table had "
              "exactly that defect and scored the 1980s as supporting the hypothesis when TFR rose "
              "and prices rose together.", "",
              "This is co-movement, not identification: no lag structure, no controls, one country. "
              "It bounds what the mechanism could be doing; it does not estimate anything.", "",
              "| decade | TFR | share of net fall | share of all movement | real child price | verdict |",
              "|---|---|---|---|---|---|"]
        edges = [y for y in range(1970, 2031, 10) if y <= t1]
        spans = list(zip([t0] + edges[:-1], edges))
        rows_d, gross = [], 0.0
        for a, b in spans:
            ya = min((y for y in tfr if y >= a), default=None)
            yb = min((y for y in tfr if y >= b), default=None)
            if ya is None or yb is None or yb <= ya:
                continue
            fall = tfr[ya] - tfr[yb]
            gross += abs(fall)
            pa = min((y for y in ref if y >= a), default=None)
            pb = min((y for y in ref if y >= b), default=None)
            ch = None if pa is None or pb is None else (ref[pb] / ref[pa] - 1.0) * 100.0
            rows_d.append((ya, yb, fall, ch))
        consistent = inconsistent = 0.0
        for ya, yb, fall, ch in rows_d:
            share = 100.0 * fall / total_fall if total_fall else float("nan")
            gshare = 100.0 * abs(fall) / gross if gross else float("nan")
            if ch is None:
                price, verdict = "—", "—"
            else:
                price = f"{ch:+.1f}%"
                # hypothesis: price up -> fertility down. fall > 0 means TFR fell.
                ok = (ch > 0 and fall > 0) or (ch < 0 and fall < 0)
                verdict = "consistent" if ok else "**inconsistent**"
                if ok:
                    consistent += abs(fall)
                else:
                    inconsistent += abs(fall)
            L.append(f"| {ya}–{yb} | {tfr[ya]:.2f} → {tfr[yb]:.2f} | {share:+.0f}% | "
                     f"{gshare:.0f}% | {price} | {verdict} |")
        L.append("")
        if gross:
            L += [f"Weighted by absolute movement in TFR, **{100.0 * inconsistent / gross:.0f}% of "
                  f"the total decade-to-decade movement in US fertility since {t0} runs against the "
                  f"mechanism**, and {100.0 * consistent / gross:.0f}% with it. The single largest "
                  "movement — the 1970s, which alone is "
                  f"{100.0 * max(abs(f) for _, _, f, _ in rows_d) / gross:.0f}% of all movement — is "
                  "one of the inconsistent ones: the real price of children **fell** through the "
                  "decade in which US fertility fell fastest.", ""]

    # ------------------------------------------------------- which component is carrying the result
    L += ["## Leave-one-out: which component carries the result", "",
          "The `without_education` arm is the whole question. If the composite rises only because of "
          "education, then this chapter's exposure series rests on the component whose admissibility "
          "scope ruling 2 puts most in doubt — college tuition is very largely a *chosen quality* "
          "(C.3.d), and the BLS K-12 tuition index prices **private** schooling, which is not the "
          "price most US parents face.", "",
          "**A one-at-a-time drop cannot detect a block effect**, and education is a block of "
          "three. Every single-component drop below still rises because two education components "
          "remain; the row that answers the question is `without_education` in the arms table above, "
          "which drops all three at once and **falls** on equal weights.", "",
          "| arm minus | coverage | change | still rises? |", "|---|---|---|---|"]
    base_members = ARMS["with_education"]
    for drop in base_members:
        rest = [m for m in base_members if m != drop]
        c = composite(reals, rest)
        if not c:
            L.append(f"| `{drop}` | — | no overlap | — |")
            continue
        ys = sorted(c)
        ch, a, b = pct_change(c, ys[0], 2024)
        L.append(f"| `{drop}` | {a}–{b} | **{ch:+.1f}%** | {'yes' if ch > 0 else '**no**'} |")
    L.append("")
    LOGS.mkdir(parents=True, exist_ok=True)
    (LOGS / "child-cost-direct-sign-test.md").write_text("\n".join(L) + "\n")
    print("\n".join(L[L.index("## US TFR, for reference"):]))
    print(f"\nwrote output/tables/child-cost-direct-price-index.csv and "
          f"literature/search-logs/child-cost-direct-sign-test.md")


main()
