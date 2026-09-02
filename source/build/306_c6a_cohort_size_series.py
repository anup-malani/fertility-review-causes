#!/usr/bin/env python3
"""306 — build the relative-cohort-size series and run C.6.a's pre-registered sign test.

Scope §5 pre-registers a test that does not depend on the literature at all: over the SDT window,
did the exposure move in the direction the hypothesis needs? Easterlin's mechanism is that a LARGE
entering cohort is crowded, earns little relative to the standard it grew up with, and has FEWER
children. So the hypothesis requires d(TFR)/d(RCS) < 0, and it requires relative cohort size to have
RISEN over any window across which it wants to explain a fertility fall.

This script fetches the inputs, deposits them in data/raw/ with provenance (that directory was empty
before this chapter — see the scope), derives the series, and reports the test. It is deliberately
literature-independent: nothing here is an estimate from a study, and the R² it reports IS one of
PROTOCOL §4.2's three demographic-significance routes (route C), computed as pre-specified.

Relative cohort size, following the standard construction: population aged 20-29 divided by
population aged 30-64, both sexes, at time t. The numerator is the cohort entering the labour market
and beginning childbearing; the denominator is the established cohort it is crowding against.

Usage: python3 source/build/306_c6a_cohort_size_series.py [--refresh]
Outputs:
  data/raw/wdi-age-structure/*.json          raw World Bank pulls, one file per indicator
  data/raw/wdi-age-structure/PROVENANCE.md   what was pulled, when, and from where
  output/tables/easterlin-relative-cohort-size.csv     the derived series
  literature/search-logs/easterlin-relative-income-sign-test.md   the test, generated
"""
import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "raw" / "wdi-age-structure"
TABLES = ROOT / "output" / "tables"
LOGS = ROOT / "literature" / "search-logs"

# OECD-ish set carrying the SDT literature, with continuous WDI coverage from 1960.
COUNTRIES = ["USA", "GBR", "FRA", "DEU", "ITA", "ESP", "JPN", "SWE", "NLD",
             "CAN", "AUS", "DNK", "NOR", "FIN", "BEL", "AUT", "CHE", "KOR"]

YOUNG = ["2024", "2529"]                                    # ages 20-29: the entering cohort
PRIME = ["3034", "3539", "4044", "4549", "5054", "5559", "6064"]   # ages 30-64: the established one
AGE_BANDS = YOUNG + PRIME
SEXES = ["MA", "FE"]

TOTALS = {"MA": "SP.POP.TOTL.MA.IN", "FE": "SP.POP.TOTL.FE.IN"}
TFR = "SP.DYN.TFRT.IN"
START, END = 1960, 2024

# The SDT window per PROTOCOL §2, and the split the registry's own note implies.
SDT = (1965, END)
EARLY = (1965, 1980)      # the window the hypothesis is famous for getting right
LATE = (1980, END)        # "weaker post-1980 empirical support" -- HYPOTHESES-v5 §C.6.a


def indicators():
    for band in AGE_BANDS:
        for sex in SEXES:
            yield f"SP.POP.{band}.{sex}.5Y"
    for code in TOTALS.values():
        yield code
    yield TFR


def fetch(indicator, refresh):
    """One World Bank pull per indicator, all countries. Cached on disk; data/raw is immutable."""
    dest = RAW / f"{indicator}.json"
    if dest.exists() and not refresh:
        return json.loads(dest.read_text())
    url = (f"https://api.worldbank.org/v2/country/{';'.join(COUNTRIES)}/indicator/{indicator}"
           f"?format=json&per_page=20000&date={START}:{END}")
    r = subprocess.run(["curl", "-sS", "--max-time", "120", url], capture_output=True, text=True)
    try:
        payload = json.loads(r.stdout)
    except json.JSONDecodeError:
        sys.exit(f"{indicator}: non-JSON response — {r.stdout[:200]}")
    if not isinstance(payload, list) or len(payload) < 2 or payload[1] is None:
        sys.exit(f"{indicator}: no data in response — {str(payload)[:200]}")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(payload, indent=1) + "\n")
    return payload


def series(payload):
    out = {}
    for row in payload[1]:
        v = row.get("value")
        if v is None:
            continue
        out[(row["countryiso3code"], int(row["date"]))] = float(v)
    return out


def pearson(xs, ys):
    n = len(xs)
    if n < 3:
        return None, None
    mx, my = sum(xs) / n, sum(ys) / n
    sxy = sum((a - mx) * (b - my) for a, b in zip(xs, ys))
    sxx = sum((a - mx) ** 2 for a in xs)
    syy = sum((b - my) ** 2 for b in ys)
    if sxx <= 0 or syy <= 0:
        return None, None
    r = sxy / (sxx * syy) ** 0.5
    return r, r * r


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--refresh", action="store_true", help="re-pull even if cached in data/raw")
    args = ap.parse_args()

    RAW.mkdir(parents=True, exist_ok=True)
    data = {}
    for ind in indicators():
        data[ind] = series(fetch(ind, args.refresh))
        print(f"  {ind:24} {len(data[ind])} observations", flush=True)

    # Age-band shares are percentages OF THAT SEX's population, so they must be weighted back to
    # counts before the two sexes can be added. A share of a share is not a population.
    rows = []
    for c in COUNTRIES:
        for y in range(START, END + 1):
            young = prime = 0.0
            ok = True
            for band in AGE_BANDS:
                for sex in SEXES:
                    share = data[f"SP.POP.{band}.{sex}.5Y"].get((c, y))
                    total = data[TOTALS[sex]].get((c, y))
                    if share is None or total is None:
                        ok = False
                        break
                    count = share / 100.0 * total
                    if band in YOUNG:
                        young += count
                    else:
                        prime += count
                if not ok:
                    break
            tfr = data[TFR].get((c, y))
            if ok and prime > 0:
                rows.append({"country": c, "year": y, "rcs": young / prime,
                             "tfr": tfr if tfr is not None else ""})

    TABLES.mkdir(parents=True, exist_ok=True)
    csv = TABLES / "easterlin-relative-cohort-size.csv"
    csv.write_text("country,year,relative_cohort_size,tfr\n" + "".join(
        f"{r['country']},{r['year']},{r['rcs']:.6f},{r['tfr']}\n" for r in rows))

    by_country = {}
    for r in rows:
        by_country.setdefault(r["country"], []).append(r)

    def window(c, lo, hi):
        return [r for r in by_country.get(c, []) if lo <= r["year"] <= hi and r["tfr"] != ""]

    def endpoint(w):
        """Sign test on a window's endpoints. The hypothesis needs d(TFR)/d(RCS) < 0, so a FALL in
        TFR requires a RISE in RCS."""
        if len(w) < 5:
            return None
        d_rcs = w[-1]["rcs"] - w[0]["rcs"]
        d_tfr = w[-1]["tfr"] - w[0]["tfr"]
        return {"y0": w[0]["year"], "y1": w[-1]["year"],
                "rcs0": w[0]["rcs"], "rcs1": w[-1]["rcs"], "d_rcs": d_rcs,
                "tfr0": w[0]["tfr"], "tfr1": w[-1]["tfr"], "d_tfr": d_tfr,
                "needs": "rise" if d_tfr < 0 else "fall",
                "moved": "rose" if d_rcs > 0 else "fell",
                "consistent": (d_tfr < 0 and d_rcs > 0) or (d_tfr > 0 and d_rcs < 0)}

    results = []
    for c in COUNTRIES:
        w = window(c, *SDT)
        if len(w) < 10:
            results.append({"country": c, "note": "insufficient coverage"})
            continue
        r_all, r2_all = pearson([x["rcs"] for x in w], [x["tfr"] for x in w])
        e, l = window(c, *EARLY), window(c, *LATE)
        r_e = pearson([x["rcs"] for x in e], [x["tfr"] for x in e])[0] if len(e) >= 5 else None
        r_l = pearson([x["rcs"] for x in l], [x["tfr"] for x in l])[0] if len(l) >= 5 else None
        # RCS is NOT monotone over the SDT window -- it is a hump, which is the whole point of a
        # cyclical mechanism. An endpoint test on the full window therefore nets the hump to nearly
        # nothing and reports a non-result. Report the peak, and test each sub-window separately.
        peak = max(w, key=lambda x: x["rcs"])
        amp = peak["rcs"] - min(w, key=lambda x: x["rcs"])["rcs"]
        full = endpoint(w)
        results.append({"country": c, "full": full, "early": endpoint(e), "late": endpoint(l),
                        "peak_year": peak["year"], "peak_rcs": peak["rcs"], "amplitude": amp,
                        "net_over_amp": abs(full["d_rcs"]) / amp if amp > 0 else None,
                        "r_all": r_all, "r2_all": r2_all, "r_early": r_e, "r_late": r_l})

    scored = [r for r in results if "full" in r]
    n_full = sum(1 for r in scored if r["full"]["consistent"])
    n_early = sum(1 for r in scored if r["early"] and r["early"]["consistent"])
    n_late = sum(1 for r in scored if r["late"] and r["late"]["consistent"])

    def fmt(v, n=3):
        return "—" if v is None else f"{v:.{n}f}"

    L = [f"# C.6.a sign test — did the exposure move the way the hypothesis needs?", "",
         "Generated by `source/build/306_c6a_cohort_size_series.py`. Do not edit by hand.", "",
         f"Run {datetime.now(timezone.utc).date().isoformat()}. **This test uses no study estimate.** "
         "It asks the prior question that scope §5 pre-registered before any search: over the SDT "
         "window, did relative cohort size move in the direction Easterlin's mechanism requires?", "",
         "## The prediction, stated as a sign", "",
         "A large entering cohort is crowded, earns little against the standard it grew up with, and "
         "has fewer children: **d(TFR)/d(RCS) < 0**. To explain a *fall* in fertility, relative "
         "cohort size must therefore have **risen** across the window. Relative cohort size here is "
         "population aged 20–29 over population aged 30–64, both sexes.", "",
         "## Why the window has to be split, and it is not a choice made after seeing the data", "",
         "Relative cohort size is **not monotone** across the SDT window — it is a hump, which is "
         "exactly what a cyclical mechanism should produce. An endpoint test on the full window "
         "therefore nets the rise against the fall and reports a non-result about a series that "
         "moved a great deal. The split at 1980 is the one HYPOTHESES-v5 §C.6.a's own note implies "
         "when it says support weakens after that date, so the sub-windows test the registry's "
         "claim rather than a window chosen to suit an answer.", "",
         "**And the full-window column is not merely uninformative — it is the finding.** Where the "
         "exposure ends within a small fraction of its own amplitude of where it started, while TFR "
         "falls by roughly a birth and stays down, a mechanism driven by that exposure has nothing "
         "left over to account for the level shift. `net / amplitude` below is that ratio.", "",
         "## Full SDT window", "",
         "| country | window | RCS start → end | Δ RCS | peak | amplitude | net/amp | TFR start → end | Δ TFR | consistent? |",
         "|---|---|---|---|---|---|---|---|---|---|"]
    for r in results:
        if "full" not in r:
            L.append(f"| {r['country']} | — | — | — | — | — | — | — | — | {r['note']} |")
            continue
        f = r["full"]
        L.append(f"| {r['country']} | {f['y0']}–{f['y1']} | {f['rcs0']:.3f} → {f['rcs1']:.3f} | "
                 f"{f['d_rcs']:+.3f} | {r['peak_rcs']:.3f} ({r['peak_year']}) | "
                 f"{r['amplitude']:.3f} | {fmt(r['net_over_amp'], 2)} | "
                 f"{f['tfr0']:.2f} → {f['tfr1']:.2f} | {f['d_tfr']:+.2f} | "
                 f"{'yes' if f['consistent'] else '**NO**'} |")
    L += ["", f"**{n_full} of {len(scored)}** consistent across the full window.", "",
          "## The two sub-windows", "",
          "| country | 1965–80: Δ RCS | Δ TFR | consistent? | 1980–: Δ RCS | Δ TFR | consistent? |",
          "|---|---|---|---|---|---|---|"]
    for r in results:
        if "full" not in r:
            continue
        e, l = r["early"], r["late"]
        ec = "—" if not e else ("yes" if e["consistent"] else "**NO**")
        lc = "—" if not l else ("yes" if l["consistent"] else "**NO**")
        L.append(f"| {r['country']} | {fmt(e and e['d_rcs'])} | {fmt(e and e['d_tfr'], 2)} | {ec} | "
                 f"{fmt(l and l['d_rcs'])} | {fmt(l and l['d_tfr'], 2)} | {lc} |")
    L += ["", f"**Early window (1965–80): {n_early} of {len(scored)} consistent. "
              f"Late window (1980–): {n_late} of {len(scored)}.**", "",
          "## Route C — within-country time-series R² of TFR on relative cohort size", "",
          "PROTOCOL §4.2 lists three demographic-significance routes and this is the third, computed "
          "as pre-specified. A *negative* r is the direction the hypothesis predicts.", "",
          "| country | r (1965–) | R² (1965–) | r (1965–80) | r (1980–) |", "|---|---|---|---|---|"]
    for r in results:
        if "full" not in r:
            continue
        L.append(f"| {r['country']} | {fmt(r['r_all'])} | {fmt(r['r2_all'])} | "
                 f"{fmt(r['r_early'])} | {fmt(r['r_late'])} |")
    # PROTOCOL §4.2's third demsig criterion is "conditional R2 >= 0.15". R2 is SIGN-BLIND: a series
    # that fits well in the direction OPPOSITE to the hypothesis clears the threshold exactly as a
    # confirming one does. Count that rather than describe it.
    clear = [r for r in results if "full" in r and r["r2_all"] is not None and r["r2_all"] >= 0.15]
    wrong = [r for r in clear if r["r_all"] > 0]   # hypothesis predicts r < 0
    L += ["", f"**{len(clear)} of {len(scored)} countries clear PROTOCOL §4.2's R² ≥ 0.15 threshold "
              f"on the full window, and {len(wrong)} of those {len(clear)} do so with the "
              f"correlation running the WRONG WAY** "
              f"({', '.join(r['country'] for r in wrong) or 'none'}).", "",
          "R² is sign-blind. A series fitting tightly in the direction *opposite* to the hypothesis "
          "clears the threshold exactly as a confirming one does, so the R² criterion as written "
          "could certify a hypothesis on evidence that runs against it. **The R² route needs a sign "
          "condition attached**; this chapter applies one, and it is raised as a protocol-level "
          "question rather than settled here.", "",
          "## What this does and does not establish", "",
          "**Does:** whether the exposure moved in the required direction, in each window, and the "
          "route-C R². Both are properties of the data, not of any study.", "",
          "**Does not:** a causal effect. A time-series correlation between two trending demographic "
          "series is not an estimate of anything, and scope §2 explains why it cannot be — relative "
          "cohort size at *t* is this outcome's own history twenty years earlier. The elasticity for "
          "route B still has to come from identified studies.", "",
          "**Caveats on the inputs.** World Bank age-band shares derive from UN WPP interpolations, "
          "not from register counts; period TFR is tempo-distorted, so a postponement-driven trough "
          "overstates the fall in completed fertility. Both cut the same way here — neither "
          "manufactures a sign reversal.", ""]
    (LOGS / "easterlin-relative-income-sign-test.md").write_text("\n".join(L))

    prov = RAW / "PROVENANCE.md"
    prov.write_text(
        "# WDI age structure and fertility — provenance\n\n"
        f"Pulled {datetime.now(timezone.utc).isoformat(timespec='seconds')} by "
        "`source/build/306_c6a_cohort_size_series.py` for TICK-078 (C.6.a).\n\n"
        f"Source: World Bank World Development Indicators API, `api.worldbank.org/v2`, "
        f"{START}–{END}, {len(COUNTRIES)} countries: {', '.join(COUNTRIES)}.\n\n"
        "One file per indicator, unmodified API responses. Age-band indicators "
        "(`SP.POP.<band>.<sex>.5Y`) are percentages **of that sex's population**, so they must be "
        "weighted by `SP.POP.TOTL.<sex>.IN` before the sexes are summed.\n\n"
        "WDI age structure derives from UN WPP; it is an interpolation, not a register count.\n\n"
        "This directory was empty before this pull, despite `CLAUDE.md` describing it as holding the "
        "macro panels. Later chapters needing age structure or TFR should read from here rather than "
        "re-pulling. Re-pull with `--refresh`.\n")

    print(f"\nconsistent with the required sign — full window {n_full}/{len(scored)}, "
          f"1965-80 {n_early}/{len(scored)}, 1980- {n_late}/{len(scored)}")
    print(f"wrote {csv.relative_to(ROOT)} and easterlin-relative-income-sign-test.md")


main()
