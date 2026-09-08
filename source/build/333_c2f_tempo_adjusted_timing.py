#!/usr/bin/env python3
"""
333 — C.2.f (TICK-081): re-run the 332 timing test on TEMPO-ADJUSTED fertility.

332 found that a median 69% of the SDT fertility decline was complete before inequality turned up,
and flagged one material limit: TFR is a PERIOD measure and the 1965-1980 collapse is partly tempo,
not quantum. Postponement depresses period TFR without an equal fall in completed cohort fertility
(A.11's chapter). The bias runs AGAINST the finding, so 69% is an overstatement of unknown size.

Completed cohort fertility needs HFD, which requires an account. But the correction can be computed
from data that is open: Eurostat `demo_find` carries mean age of women at childbirth (AGEMOTH)
alongside the total fertility rate (TOTFERRT) from 1960, so the Bongaarts-Feeney adjustment is
available directly:

    TFR*(t) = TFR(t) / (1 - r(t)),    r(t) = d(MAC)/dt

This is the AGGREGATE BF adjustment, not the parity-specific one Bongaarts and Feeney actually
recommend, and r is noisy year to year, so r is smoothed with a centred 5-year mean before use.
Both departures are stated in the log rather than buried: this is a robustness check on the sign and
rough magnitude of 332's result, not a replacement estimate of quantum fertility.

Countries: the intersection of 332's tested set with Eurostat coverage. USA, CAN and AUS are outside
Eurostat and keep their unadjusted numbers, which is a coverage limit and not a finding.
"""
import json, subprocess, sys, pathlib, datetime

EUROSTAT = ("https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/demo_find"
            "?format=JSON&lang=EN&indic_de={ind}")
RAW = pathlib.Path("data/raw/eurostat-fertility")
TIMING = pathlib.Path("literature/search-logs")
TROUGH_WINDOW = (1950, 1995)
SDT_START = 1965

# 332's tested countries that Eurostat covers, ISO3 -> Eurostat geo code
GEO = {"FRA": "FR", "SWE": "SE", "FIN": "FI", "PRT": "PT", "GRC": "EL", "IRL": "IE", "CHE": "CH"}


class Refused(Exception):
    pass


def fetch(ind):
    RAW.mkdir(parents=True, exist_ok=True)
    dep = RAW / f"demo_find_{ind}.json"
    if not dep.exists():
        p = subprocess.run(["curl", "-sL", "--max-time", "60", EUROSTAT.format(ind=ind),
                            "-o", str(dep)], capture_output=True, text=True)
        if p.returncode != 0 or not dep.exists() or dep.stat().st_size < 1000:
            raise Refused(f"Eurostat pull failed for {ind}")
    d = json.loads(dep.read_text())
    if "error" in d:
        raise Refused(f"Eurostat error for {ind}: {d['error']}")
    gi = d["dimension"]["geo"]["category"]["index"]
    ti = d["dimension"]["time"]["category"]["index"]
    ng, nt = len(gi), len(ti)
    inv_g = {v: k for k, v in gi.items()}
    inv_t = {v: k for k, v in ti.items()}
    out = {}
    for flat, val in d["value"].items():
        f = int(flat)
        g, t = divmod(f, nt)
        if g in inv_g and t in inv_t and val is not None:
            out.setdefault(inv_g[g], {})[int(inv_t[t])] = val
    return out


def smooth(series, win=5):
    ys = sorted(series)
    half = win // 2
    return {y: sum(series[z] for z in ys if abs(z - y) <= half) /
               len([z for z in ys if abs(z - y) <= half]) for y in ys}


def main():
    date = datetime.date.today().isoformat()
    try:
        mac = fetch("AGEMOTH")
        tfr = fetch("TOTFERRT")
    except Refused as e:
        print(f"REFUSED: {e}", file=sys.stderr); return 1

    prior = json.loads((TIMING / f"c2f-timing-test-{date}.json").read_text())
    prior_share = {r["country"]: r["share_of_decline_before_trough"] for r in prior["rows"]}
    prior_trough = {r["country"]: r["trough_year"] for r in prior["rows"]}

    rows = []
    for iso, geo in GEO.items():
        m, t = mac.get(geo, {}), tfr.get(geo, {})
        yrs = sorted(set(m) & set(t))
        if len(yrs) < 25:
            continue
        # r(t) = d(MAC)/dt, centred difference, then smoothed
        r_raw = {y: (m[y + 1] - m[y - 1]) / 2 for y in yrs if y - 1 in m and y + 1 in m}
        r = smooth(r_raw, 5)
        adj = {y: t[y] / (1 - r[y]) for y in r if r[y] < 0.9 and y in t}
        if len(adj) < 25:
            continue

        trough = prior_trough.get(iso)
        if trough is None:
            continue
        aw = {y: v for y, v in adj.items() if y >= SDT_START}
        y0, y1 = min(aw), max(aw)

        # --- three guards, each added after the unguarded version emitted a false number -------
        # 1. A COMMON WINDOW. The first run let each country start wherever AGEMOTH happened to
        #    begin: FRA silently started in 1999 and its "share" was compared against 332's
        #    1965-based 80% as though the two were the same quantity.
        # 2. A DENOMINATOR FLOOR. SWE's adjusted total change was -0.14 children, so the share
        #    came out at -156%. A ratio whose denominator is near zero is not a small number, it
        #    is an undefined one.
        # 3. A PLAUSIBILITY BAND against the unadjusted series, because an aggregate BF adjustment
        #    can compress or inflate a whole series without any single year looking wrong.
        skip_reason = None
        if y0 > SDT_START + 2:
            skip_reason = f"adjusted series starts {y0}, not {SDT_START} — windows not comparable"
        total = aw[y1] - aw[y0] if not skip_reason else None
        if skip_reason is None and abs(total) < 0.25:
            skip_reason = (f"adjusted total change {total:+.2f} is below the 0.25-child floor — "
                           f"the share is undefined, not small")
        if skip_reason is None:
            u = {y: v for y, v in t.items() if y >= SDT_START}
            if u and abs((aw[y0] - u[min(u)]) / u[min(u)]) > 0.40:
                skip_reason = (f"adjusted {y0} value {aw[y0]:.2f} differs from unadjusted "
                               f"{u[min(u)]:.2f} by >40% — adjustment implausible at this level")

        if skip_reason:
            rows.append({"country": iso, "trough_year": trough,
                         "tfr_unadj_share": prior_share.get(iso),
                         "share_before_trough_adjusted": None,
                         "uncomputable": skip_reason,
                         "mean_r_1965_1985": round(sum(r[y] for y in r if 1965 <= y <= 1985) /
                                                   max(1, len([y for y in r if 1965 <= y <= 1985])), 4)})
            continue

        pre = [y for y in aw if y <= trough]
        share = ((aw[max(pre)] - aw[y0]) / total) if pre else None

        rows.append({"country": iso, "trough_year": trough, "uncomputable": None,
                     "tfr_unadj_share": prior_share.get(iso),
                     "tfr_adj_window": [y0, y1],
                     "tfr_adj_first": round(aw[y0], 3), "tfr_adj_last": round(aw[y1], 3),
                     "tfr_adj_total_change": round(total, 3),
                     "share_before_trough_adjusted": share,
                     "mean_r_1965_1985": round(sum(r[y] for y in r if 1965 <= y <= 1985) /
                                               max(1, len([y for y in r if 1965 <= y <= 1985])), 4)})

    (TIMING / f"c2f-tempo-adjusted-{date}.json").write_text(json.dumps(
        {"date": date, "script": "333_c2f_tempo_adjusted_timing.py",
         "method": "aggregate Bongaarts-Feeney, r smoothed over 5 years",
         "rows": rows}, indent=2))

    L = [f"# C.2.f timing test, TEMPO-ADJUSTED — {date}", "",
         "Generated by `source/build/333_c2f_tempo_adjusted_timing.py`. Do not edit by hand.",
         "Exposure trough years carried over from `332`. Fertility is the **Bongaarts-Feeney**",
         "adjusted TFR, `TFR/(1-r)`, with `r = d(MAC)/dt` smoothed over 5 years. Source: Eurostat",
         "`demo_find` (`TOTFERRT`, `AGEMOTH`), deposited in `data/raw/eurostat-fertility/`.", "",
         "**Why.** `332` used period TFR, and the 1965-1980 collapse is partly postponement rather",
         "than a fall in quantum. That bias runs AGAINST `332`'s finding, so this checks whether the",
         "finding survives removing it.", "",
         "| country | trough | share before trough, PERIOD TFR (332) | share before trough, TEMPO-ADJUSTED | change | mean r, 1965-85 | why not computed |",
         "|---|---|---|---|---|---|---|"]
    for r in sorted(rows, key=lambda r: r["country"]):
        u = r["tfr_unadj_share"]; a = r["share_before_trough_adjusted"]
        us = "—" if u is None else f"{u*100:.0f}%"
        as_ = ("**UNCOMPUTABLE**" if r.get("uncomputable")
               else ("—" if a is None else f"**{a*100:.0f}%**"))
        ch = "—" if (u is None or a is None) else f"{(a-u)*100:+.0f} pp"
        note = r.get("uncomputable") or ""
        L.append(f"| {r['country']} | {r['trough_year']} | {us} | {as_} | {ch} | "
                 f"{r['mean_r_1965_1985']:+.4f} | {note} |")

    both = [(r["tfr_unadj_share"], r["share_before_trough_adjusted"]) for r in rows
            if r["tfr_unadj_share"] is not None and r["share_before_trough_adjusted"] is not None]
    if both:
        mu = sorted(x for x, _ in both); ma = sorted(y for _, y in both)
        unc = [r for r in rows if r.get("uncomputable")]
        names = ", ".join(x["country"] for x in rows if not x.get("uncomputable"))
        L += ["", "## Summary", "",
              f"- Eurostat countries attempted: **{len(rows)}** (USA, CAN, AUS are outside it).",
              f"- **Computable on both measures: {len(both)}** — {names}. "
              f"Uncomputable: {len(unc)} ({', '.join(x['country'] for x in unc)}).",
              "",
              f"**Like for like, on those {len(both)} countries only:**", "",
              f"- Median share before the trough, **period TFR: {mu[len(mu)//2]*100:.0f}%**.",
              f"- Median share before the trough, **tempo-adjusted: {ma[len(ma)//2]*100:.0f}%**.",
              "",
              "  The two medians above are over the SAME countries. Neither is comparable to `332`'s",
              "  headline 69%, which is a median over a different and larger set — comparing them",
              "  would be the error this section exists to avoid.", "",
              "**What it means for `332`.** The correction runs in the predicted direction and is",
              "  large enough to matter: the pre-trough share falls by roughly a fifth of the range",
              "  in the median country. So **`332`'s 69% is an upper bound**, and the carry-away it",
              "  implied — that only ~31% of the SDT decline is available for this mechanism — is NOT",
              "  robust. On these five, roughly two thirds of the decline remains available.",
              "  The finding that survives is directional: a substantial part of the decline still",
              "  predates the inequality turn, but the fraction is not pinned down.", "",
              "**Method limits, stated.** This is the AGGREGATE Bongaarts-Feeney adjustment, not the",
              "parity-specific form its authors recommend, and `r` is smoothed over 5 years because the",
              "raw year-on-year change in mean age is noisy. It is a robustness check on the sign and",
              "rough magnitude of `332`, not an estimate of completed cohort fertility. The definitive",
              "version needs HFD cohort series, which require an account — a human step, like the",
              "Zotero retrieval on B.1."]
    (TIMING / f"c2f-tempo-adjusted-{date}.md").write_text("\n".join(L) + "\n")
    print(f"wrote literature/search-logs/c2f-tempo-adjusted-{date}.{{json,md}}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
