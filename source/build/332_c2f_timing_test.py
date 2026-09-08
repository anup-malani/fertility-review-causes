#!/usr/bin/env python3
"""
332 — C.2.f (TICK-081) timing test on a LONG-RUN inequality series.

Script 331 found that median 79% of the SDT fertility decline predates the WDI Gini series, and
said in its own log that this measures when the exposure becomes OBSERVABLE, not when it moved.
This script runs the substantive version of that claim, which needs a series covering the period.

Source: WID top-10% pre-tax national income share, via Our World in Data's grapher CSV (the WID
bulk file is 882 MB; this is the same variable at 95 KB). Deposited in data/raw/.

The test. Inequality in the rich countries is U-shaped over the 20th century: falling from the war
to a trough around 1975-1985, rising after. The SDT fertility collapse ran roughly 1965-1980. So:

    what share of the SDT fertility decline happened BEFORE inequality turned up?

If most of it did, the exposure was moving the WRONG WAY (or flat) through the period in which the
outcome moved, and the SDT cell is settled on timing rather than on any elasticity. That is B.7's
finding -- 67.6% of the SDT decline predating the exposure -- in a second chapter.

The trough is found from the data, not assumed, and the pre- and post-trough slopes are reported so
a country with no U-shape is visible as such rather than silently forced into one.

Reported decade by decade as well as endpoint-to-endpoint: endpoint-test-nets-a-hump-to-nothing.
"""
import csv, json, subprocess, sys, pathlib, datetime

RAW = pathlib.Path("data/raw/wid-top10-share")
WDI_RAW = pathlib.Path("data/raw/wdi-inequality-fertility")
OWID = "https://ourworldindata.org/grapher/income-share-top-10-before-tax-wid.csv"
SDT_START = 1965
TROUGH_WINDOW = (1950, 1995)      # where a post-war U-turn could plausibly sit

COUNTRIES = ["USA", "GBR", "FRA", "DEU", "ITA", "ESP", "SWE", "NLD", "JPN", "CAN",
             "AUS", "DNK", "NOR", "FIN", "BEL", "AUT", "CHE", "PRT", "GRC", "IRL", "KOR"]


class Refused(Exception):
    pass


def load_top10():
    RAW.mkdir(parents=True, exist_ok=True)
    dep = RAW / "owid-wid-top10-before-tax.csv"
    if not dep.exists():
        p = subprocess.run(["curl", "-sL", "--max-time", "60", OWID, "-o", str(dep)],
                           capture_output=True, text=True)
        if p.returncode != 0 or not dep.exists() or dep.stat().st_size < 1000:
            raise Refused(f"OWID pull failed (curl {p.returncode}, "
                          f"{dep.stat().st_size if dep.exists() else 0} bytes)")
    out = {}
    with dep.open() as fh:
        for r in csv.DictReader(fh):
            code = r.get("Code") or ""
            val = r.get("Share (richest decile, before tax)")
            if not code or not val:
                continue
            out.setdefault(code, {})[int(r["Year"])] = float(val)
    if "USA" not in out:
        raise Refused("USA missing from the OWID file — schema changed, do not treat as no data")
    return out


def load_tfr(c):
    f = WDI_RAW / f"{c}_SP.DYN.TFRT.IN.json"
    if not f.exists():
        raise Refused(f"{f} missing — run 331 first; this is not an empty series")
    return {int(k): v for k, v in json.loads(f.read_text()).items()}


def slope(series, lo, hi):
    ys = [y for y in sorted(series) if lo <= y <= hi]
    if len(ys) < 4:
        return None
    n = len(ys); mx = sum(ys)/n; my = sum(series[y] for y in ys)/n
    sxx = sum((y-mx)**2 for y in ys)
    if sxx == 0:
        return None
    return sum((y-mx)*(series[y]-my) for y in ys)/sxx


def main():
    date = datetime.date.today().isoformat()
    try:
        top10 = load_top10()
    except Refused as e:
        print(f"REFUSED: {e}", file=sys.stderr)
        return 1

    rows, skipped = [], []
    for c in COUNTRIES:
        ineq = top10.get(c, {})
        pre = [y for y in ineq if SDT_START <= y <= 1980]
        if len(pre) < 5:
            skipped.append((c, f"{len(pre)} obs in {SDT_START}-1980"))
            continue
        try:
            tfr = load_tfr(c)
        except Refused as e:
            skipped.append((c, str(e))); continue

        cand = {y: v for y, v in ineq.items() if TROUGH_WINDOW[0] <= y <= TROUGH_WINDOW[1]}
        trough = min(cand, key=lambda y: cand[y])
        b_pre = slope(ineq, TROUGH_WINDOW[0], trough)
        b_post = slope(ineq, trough, 2024)

        tw = {y: v for y, v in tfr.items() if y >= SDT_START}
        y0, y1 = min(tw), max(tw)
        total = tw[y1] - tw[y0]
        at_trough = tw[max(y for y in tw if y <= trough)] if any(y <= trough for y in tw) else None
        share_before = ((at_trough - tw[y0]) / total) if (at_trough is not None and total) else None

        decades = []
        for d0 in range(1960, 2020, 10):
            ds = [y for y in tw if d0 <= y < d0+10]
            if len(ds) >= 2:
                decades.append((d0, tw[max(ds)] - tw[min(ds)]))

        rows.append({"country": c, "trough_year": trough,
                     "top10_at_trough": round(cand[trough], 2),
                     "slope_pre_trough": b_pre, "slope_post_trough": b_post,
                     "u_shaped": (b_pre is not None and b_post is not None
                                  and b_pre < 0 < b_post),
                     "tfr_window": [y0, y1], "tfr_total_change": round(total, 3),
                     "tfr_at_trough": at_trough,
                     "share_of_decline_before_trough": share_before,
                     "tfr_by_decade": decades})

    out = pathlib.Path("literature/search-logs"); out.mkdir(parents=True, exist_ok=True)
    (out / f"c2f-timing-test-{date}.json").write_text(json.dumps(
        {"date": date, "script": "332_c2f_timing_test.py", "source": OWID,
         "rows": rows, "skipped": [{"country": c, "reason": r} for c, r in skipped]}, indent=2))

    shares = [r["share_of_decline_before_trough"] for r in rows
              if r["share_of_decline_before_trough"] is not None]
    L = [f"# C.2.f timing test — long-run inequality — {date}", "",
         "Generated by `source/build/332_c2f_timing_test.py`. Do not edit by hand.",
         "Exposure: WID top-10% pre-tax national income share via Our World in Data",
         f"(`{OWID}`), deposited in `data/raw/wid-top10-share/`. Outcome: WDI TFR from script 331.", "",
         "**The question.** Rich-country inequality is U-shaped: falling to a trough around 1975-85,",
         "rising after. The SDT fertility collapse ran roughly 1965-1980. What share of the decline",
         "happened BEFORE inequality turned up? The trough is found from the data, not assumed.", "",
         "| country | trough | top10 at trough | slope pre | slope post | U-shaped? | TFR change | share of decline BEFORE the trough |",
         "|---|---|---|---|---|---|---|---|"]
    for r in sorted(rows, key=lambda r: -(r["share_of_decline_before_trough"] or -9)):
        sp = "—" if r["slope_pre_trough"] is None else f"{r['slope_pre_trough']:+.3f}"
        sq = "—" if r["slope_post_trough"] is None else f"{r['slope_post_trough']:+.3f}"
        sh = "—" if r["share_of_decline_before_trough"] is None else \
             f"**{r['share_of_decline_before_trough']*100:.0f}%**"
        L.append(f"| {r['country']} | {r['trough_year']} | {r['top10_at_trough']} | {sp} | {sq} | "
                 f"{'yes' if r['u_shaped'] else 'NO'} | {r['tfr_total_change']:+.2f} | {sh} |")
    L += ["", "## TFR change by decade (the hump check)", "",
          "| country | " + " | ".join(f"{d}s" for d in range(1960, 2020, 10)) + " |",
          "|---" * 7 + "|"]
    for r in sorted(rows, key=lambda r: r["country"]):
        d = dict(r["tfr_by_decade"])
        L.append(f"| {r['country']} | " + " | ".join(
            (f"{d[y]:+.2f}" if y in d else "—") for y in range(1960, 2020, 10)) + " |")
    if shares:
        s = sorted(shares); med = s[len(s)//2]
        L += ["", "## Summary", "",
              f"- Countries with ≥5 inequality observations in {SDT_START}-1980: **{len(rows)}** "
              f"of {len(COUNTRIES)}.",
              f"- U-shaped (fell then rose): **{sum(1 for r in rows if r['u_shaped'])}** of {len(rows)}.",
              f"- **Share of the SDT fertility decline completed BEFORE inequality turned up: "
              f"median {med*100:.0f}%, range {min(shares)*100:.0f}-{max(shares)*100:.0f}%.**",
              "",
              "  Unlike script 331's 79%, this is NOT confounded with data availability: the",
              "  inequality series covers the whole period here, and the trough is measured in it.",
              "",
              f"- Countries excluded for thin pre-1980 coverage: **{len(skipped)}** — "
              + ", ".join(c for c, _ in skipped) + ".",
              "  Their exclusion is a coverage limit, not a finding, and it is not evidence either way."]
    (out / f"c2f-timing-test-{date}.md").write_text("\n".join(L) + "\n")
    print(f"wrote literature/search-logs/c2f-timing-test-{date}.{{json,md}}")
    print(f"countries tested {len(rows)}, skipped {len(skipped)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
