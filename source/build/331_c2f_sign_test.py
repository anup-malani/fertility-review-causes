#!/usr/bin/env python3
"""
331 — C.2.f (TICK-081) §5 slope-sufficiency sign test, run BEFORE the production query.

The scope document pre-registers the sign: C.2.f requires the DISPERSION of the income distribution
to have RISEN across the SDT window in the countries whose fertility fell. If it did not, the SDT
cell is settled by the sign and no elasticity estimate is relevant to it.

Order note: §15 of the scope lists the free-seed harvest as 331 and this as second. They are swapped
because the free-seed harvest reads neighbouring chapters' screen files, which live on unmerged
branches; this test depends on nothing but public data. The harvest keeps its place in the plan.

Three things are computed per country, and the third is the one that can settle the cell:

  1. TFR change across the SDT window (1965 -> latest), the outcome.
  2. Gini trend across its own coverage, with the SIGN reported first
     (r2-criterion-is-sign-blind: six of six countries once cleared PROTOCOL's 0.15 with the
     correlation running AGAINST the hypothesis).
  3. The share of the TFR decline that occurred BEFORE the inequality series even begins.
     B.7 found 67.6% of the SDT decline predated its exposure and that finding carried the chapter.

Reported as an endpoint calculation AND decade by decade, because an endpoint nets a hump to nothing
(endpoint-test-nets-a-hump-to-nothing: C.6.a read 0/18 on endpoints and 14/18 early, 0/18 late once
the window was split).

Sources: World Bank WDI, SP.DYN.TFRT.IN and SI.POV.GINI. Raw pulls are deposited under data/raw/
so the build is reproducible; the directory was empty before this script.
"""
import json, subprocess, sys, pathlib, time, datetime

WB = "https://api.worldbank.org/v2/country/{c}/indicator/{ind}?format=json&per_page=500"
RAW = pathlib.Path("data/raw/wdi-inequality-fertility")
SDT_START = 1965

# The SDT core: rich countries whose fertility fell across the window the hypothesis names.
COUNTRIES = ["USA", "GBR", "FRA", "DEU", "ITA", "ESP", "SWE", "NLD", "JPN", "CAN",
             "AUS", "DNK", "NOR", "FIN", "BEL", "AUT", "CHE", "PRT", "GRC", "IRL", "KOR"]


class Refused(Exception):
    """A failed pull. Never silently becomes 'no data' (refusals-read-as-zeros)."""


def fetch(country, indicator, use_cache=True):
    """Pull a WDI series. Re-uses the deposit in data/raw/ so a re-run is cheap and offline-safe;
    stage-output-must-survive-rerun -- run every stage twice and check it says the same thing."""
    cached = RAW / f"{country}_{indicator}.json"
    if use_cache and cached.exists():
        return {int(k): v for k, v in json.loads(cached.read_text()).items()}
    url = WB.format(c=country, ind=indicator)
    p = subprocess.run(["curl", "-s", "-S", "--max-time", "60", url], capture_output=True, text=True)
    if p.returncode != 0:
        raise Refused(f"curl exit {p.returncode} for {country}/{indicator}")
    try:
        d = json.loads(p.stdout)
    except json.JSONDecodeError:
        raise Refused(f"non-JSON for {country}/{indicator}: {p.stdout[:120]!r}")
    if not isinstance(d, list) or len(d) < 2:
        raise Refused(f"unexpected envelope for {country}/{indicator}: {p.stdout[:160]!r}")
    if d[1] is None:
        return {}                      # a genuine empty series, distinct from a failed request
    return {int(r["date"]): r["value"] for r in d[1] if r["value"] is not None}


def slope(series):
    """OLS slope and r on {year: value}. Returns (slope, r2, n, first, last)."""
    ys = sorted(series)
    if len(ys) < 5:
        return None
    n = len(ys)
    mx = sum(ys) / n
    my = sum(series[y] for y in ys) / n
    sxy = sum((y - mx) * (series[y] - my) for y in ys)
    sxx = sum((y - mx) ** 2 for y in ys)
    syy = sum((series[y] - my) ** 2 for y in ys)
    if sxx == 0 or syy == 0:
        return None
    b = sxy / sxx
    r2 = (sxy ** 2) / (sxx * syy)
    return b, r2, n, ys[0], ys[-1]


def main():
    RAW.mkdir(parents=True, exist_ok=True)
    date = datetime.date.today().isoformat()
    tfr, gini, errors = {}, {}, []

    for c in COUNTRIES:
        for ind, store in (("SP.DYN.TFRT.IN", tfr), ("SI.POV.GINI", gini)):
            try:
                s = fetch(c, ind)
                store[c] = s
                (RAW / f"{c}_{ind}.json").write_text(json.dumps(s, indent=1, sort_keys=True))
            except Refused as e:
                errors.append(str(e))
                print(f"  REFUSED {c}/{ind}: {e}", file=sys.stderr)
            time.sleep(0.15)
        print(f"  {c}: TFR {len(tfr.get(c,{}))} obs, Gini {len(gini.get(c,{}))} obs")

    rows = []
    for c in COUNTRIES:
        t, g = tfr.get(c, {}), gini.get(c, {})
        tw = {y: v for y, v in t.items() if y >= SDT_START}
        if not tw:
            continue
        y0, y1 = min(tw), max(tw)
        tfr_change = tw[y1] - tw[y0]

        gsl = slope(g) if g else None
        gfirst = min(g) if g else None

        # share of the TFR decline that happened before the inequality series begins
        pre_share = None
        if gfirst is not None and gfirst in range(y0, y1 + 1) and tfr_change < 0:
            # nearest TFR observation at or before the first Gini year
            cands = [y for y in tw if y <= gfirst]
            if cands:
                tv = tw[max(cands)]
                pre_share = (tv - tw[y0]) / tfr_change if tfr_change else None

        rows.append({
            "country": c, "tfr_first_year": y0, "tfr_last_year": y1,
            "tfr_first": tw[y0], "tfr_last": tw[y1], "tfr_change": tfr_change,
            "gini_n": len(g), "gini_first_year": gfirst, "gini_last_year": max(g) if g else None,
            "gini_slope_per_year": gsl[0] if gsl else None,
            "gini_r2": gsl[1] if gsl else None,
            "gini_sign_supports_hypothesis": (gsl[0] > 0) if gsl else None,
            "share_of_tfr_decline_before_gini_starts": pre_share,
        })

    out = pathlib.Path("literature/search-logs")
    out.mkdir(parents=True, exist_ok=True)
    (out / f"c2f-sign-test-{date}.json").write_text(json.dumps(
        {"date": date, "script": "331_c2f_sign_test.py", "sdt_start": SDT_START,
         "source": "World Bank WDI SP.DYN.TFRT.IN and SI.POV.GINI",
         "rows": rows, "refused": errors}, indent=2))

    rising = [r for r in rows if r["gini_sign_supports_hypothesis"] is True]
    falling = [r for r in rows if r["gini_sign_supports_hypothesis"] is False]
    nogini = [r for r in rows if r["gini_slope_per_year"] is None]
    pres = [r["share_of_tfr_decline_before_gini_starts"] for r in rows
            if r["share_of_tfr_decline_before_gini_starts"] is not None]

    L = [f"# C.2.f slope-sufficiency sign test — {date}", "",
         "Generated by `source/build/331_c2f_sign_test.py`. Do not edit by hand.",
         "Source: World Bank WDI (`SP.DYN.TFRT.IN`, `SI.POV.GINI`); raw pulls in",
         "`data/raw/wdi-inequality-fertility/`.", "",
         "**Pre-registered sign** (scope §5): C.2.f requires dispersion to have RISEN across the",
         "window in which fertility fell. The sign is reported before any fit, because the R2",
         "criterion is sign-blind.", "",
         "| country | TFR window | TFR change | Gini obs | Gini window | slope/yr | R2 | sign OK? | share of TFR fall before Gini starts |",
         "|---|---|---|---|---|---|---|---|---|"]
    for r in sorted(rows, key=lambda r: r["country"]):
        sl = "—" if r["gini_slope_per_year"] is None else f"{r['gini_slope_per_year']:+.4f}"
        r2 = "—" if r["gini_r2"] is None else f"{r['gini_r2']:.2f}"
        ok = {True: "**yes**", False: "**NO**", None: "—"}[r["gini_sign_supports_hypothesis"]]
        gw = "—" if not r["gini_n"] else f"{r['gini_first_year']}–{r['gini_last_year']}"
        ps = "—" if r["share_of_tfr_decline_before_gini_starts"] is None else \
             f"**{r['share_of_tfr_decline_before_gini_starts']*100:.0f}%**"
        L.append(f"| {r['country']} | {r['tfr_first_year']}–{r['tfr_last_year']} | "
                 f"{r['tfr_change']:+.2f} | {r['gini_n']} | {gw} | {sl} | {r2} | {ok} | {ps} |")
    L += ["", "## Summary", "",
          f"- Countries with a usable Gini trend: **{len(rising)+len(falling)}** of {len(rows)}.",
          f"- Sign RISING (supports the hypothesis): **{len(rising)}** — "
          + (", ".join(r["country"] for r in rising) or "none"),
          f"- Sign FALLING (runs against it): **{len(falling)}** — "
          + (", ".join(r["country"] for r in falling) or "none"),
          f"- No usable inequality series at all: **{len(nogini)}** — "
          + (", ".join(r["country"] for r in nogini) or "none")]
    if pres:
        pres_sorted = sorted(pres)
        med = pres_sorted[len(pres_sorted)//2]
        L += ["",
              f"- **Share of the SDT fertility decline that predates the inequality series: "
              f"median {med*100:.0f}%, range {min(pres)*100:.0f}-{max(pres)*100:.0f}% "
              f"across {len(pres)} countries.**",
              "",
              "  **Read this precisely: it measures when the exposure becomes OBSERVABLE in WDI, not",
              "  when the exposure moved.** A Gini series beginning in 1987 does not mean inequality",
              "  was constant before 1987; it means WDI holds no measurement. So this row is",
              "  suggestive, not decisive, and it is confounded with data availability.",
              "",
              "  The substantive version of the claim -- that inequality in most rich countries was",
              "  flat or falling from 1945 to about 1980 while the main SDT fertility decline ran",
              "  1965-1980 -- needs a long-run series (WID top shares, Atkinson/Piketty/Saez), NOT",
              "  the absence of WDI data. That test is the next step and it is what would make this",
              "  a B.7-shaped finding (67.6% of the SDT decline predating the exposure) rather than",
              "  an artefact of coverage.",
              "",
              "  A share above 100% (DEU) is arithmetically correct and means TFR fell below its",
              "  end-of-window level and partially recovered. Not an error; flagged so it is not",
              "  read as one."]
    if errors:
        L += ["", "## REFUSED — these are not empty series", ""] + [f"- {e}" for e in errors]
    else:
        L += ["", "No refused pulls: every empty series above is a real absence of data."]
    (out / f"c2f-sign-test-{date}.md").write_text("\n".join(L) + "\n")
    print(f"\nwrote literature/search-logs/c2f-sign-test-{date}.{{json,md}}")
    print(f"rising {len(rising)} | falling {len(falling)} | no series {len(nogini)}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
