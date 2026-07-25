#!/usr/bin/env python3
"""
b1_forest_plot.py — forest plot of the B.1 status -> reproductive-success pool, by sex.

Reads the poolable status-reproduction correlations from the effects CSV and the pooled estimates from
the meta-analysis summary CSV, and renders a forest plot grouped by sex. Per-study 95% CIs are computed
on the Fisher-z scale (se = 1/sqrt(n-3)) and back-transformed to r; a study's own reported CI is used
when present (von Rueden's meta-analytic Zr). Marker area is proportional to inverse-variance weight,
the standard forest-plot encoding.

Design follows the project dataviz method: validated categorical pair (blue = men #2a78d6, orange =
women #eb6834, CVD dE 24.7), thin marks, recessive axes, a zero reference line, direct value labels,
and group headers so identity is never color-alone.

Outputs: output/figures/{slug}-status-repro-forest.png and .pdf
"""
import csv, math
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

SLUG = "evolutionary-sex-drive-contraceptive-decoupling"
REPO = Path(__file__).resolve().parents[2]
EFF = REPO / "extraction" / f"{SLUG}-effects.csv"
SUMM = REPO / "output" / "tables" / f"{SLUG}-meta-analysis-summary.csv"
OUT = REPO / "output" / "figures" / f"{SLUG}-status-repro-forest"

BLUE, ORANGE = "#2a78d6", "#eb6834"      # validated categorical slots 1,2 (men, women)
INK, MUTED, GRID, SURFACE = "#0b0b0b", "#52514e", "#d8d7d2", "#fcfcfb"

LABEL = {  # short reader labels + contraception context
    "W2507848855": ("von Rueden & Jaeggi 2016", "no contraception"),
    "W2859705526": ("Hopcroft 2018 (US SIPP)", ""),
    "W1966706839": ("Hopcroft 2015 (NLSY79)", ""),
    "W2164643379": ("Fieder et al. 2005", ""),
    "W2033659528": ("Kanazawa 2003 (GSS)", ""),
}


def ci_from_r(r, n):
    z = math.atanh(max(min(r, 0.999), -0.999))
    se = 1.0 / math.sqrt(n - 3)
    return math.tanh(z - 1.96 * se), math.tanh(z + 1.96 * se), 1.0 / (se * se)


def load():
    studies = {"male": [], "female": []}
    for row in csv.DictReader(open(EFF)):
        if row["estimand"] != "STATUS_REPRODUCTION" or row["effect_type"] not in ("r", "zr"):
            continue
        if row["exclude"] == "yes" or not row["effect_value"]:
            continue
        sex = row["sex"]
        if sex not in studies:
            continue
        r = float(row["effect_value"])
        if row["ci_lower"] and row["ci_upper"]:                     # study-reported CI (von Rueden)
            lo, hi = float(row["ci_lower"]), float(row["ci_upper"])
            wt = 1.0 / (((math.atanh(hi) - math.atanh(lo)) / (2 * 1.96)) ** 2)
        else:
            lo, hi, wt = ci_from_r(r, float(row["n"]))
        lbl, ctx = LABEL.get(row["study_id"], (row["study_id"], ""))
        studies[sex].append({"label": lbl, "ctx": ctx, "r": r, "lo": lo, "hi": hi, "wt": wt})
    for s in studies.values():
        s.sort(key=lambda d: d["r"], reverse=True)
    return studies


def pooled():
    out = {}
    for row in csv.DictReader(open(SUMM)):
        if row["group"] in ("sex=male", "sex=female") and row["status"] == "pooled":
            out[row["group"].split("=")[1]] = (float(row["pooled_r"]), float(row["r_ci_lower"]),
                                               float(row["r_ci_upper"]), float(row["I2_pct"]))
    return out


def diamond(ax, y, r, lo, hi, color, h=0.28):
    ax.add_patch(Polygon([(lo, y), (r, y + h), (hi, y), (r, y - h)], closed=True,
                         facecolor=color, edgecolor="white", linewidth=1.2, zorder=5))


def main():
    studies, pool = load(), pooled()
    wts = [d["wt"] for s in studies.values() for d in s]
    wmin, wmax = min(wts), max(wts)

    def msize(w):                                                   # inverse-variance -> marker area
        return 45 + 320 * (math.sqrt(w) - math.sqrt(wmin)) / (math.sqrt(wmax) - math.sqrt(wmin) + 1e-9)

    rows, y = [], 0.0
    for sex, color in (("male", BLUE), ("female", ORANGE)):
        rows.append(("header", sex, color, y)); y -= 1.0
        for d in studies[sex]:
            rows.append(("study", d, color, y)); y -= 1.0
        pr, plo, phi, i2 = pool[sex]
        rows.append(("pooled", (pr, plo, phi, i2), color, y)); y -= 1.0
        y -= 0.6

    fig, ax = plt.subplots(figsize=(9.2, 6.6), dpi=200)
    fig.patch.set_facecolor(SURFACE); ax.set_facecolor(SURFACE)
    ax.axvline(0, color=GRID, lw=1.4, zorder=1)                     # null reference

    for kind, payload, color, y in rows:
        if kind == "header":
            ax.text(-0.375, y, "MEN" if payload == "male" else "WOMEN", ha="left", va="center",
                    fontsize=11, fontweight="bold", color=color)
        elif kind == "study":
            d = payload
            ax.plot([d["lo"], d["hi"]], [y, y], color=color, lw=1.6, solid_capstyle="round", zorder=3)
            ax.scatter([d["r"]], [y], s=msize(d["wt"]), color=color, edgecolor="white",
                       linewidth=1.0, zorder=4)
            tag = f"  {d['label']}" + (f"  ·  {d['ctx']}" if d["ctx"] else "")
            ax.text(-0.375, y, tag, ha="left", va="center", fontsize=9.5, color=INK)
            ax.text(0.52, y, f"{d['r']:+.2f}  [{d['lo']:+.2f}, {d['hi']:+.2f}]", ha="right",
                    va="center", fontsize=8.8, color=MUTED, family="DejaVu Sans Mono")
        else:
            pr, plo, phi, i2 = payload
            diamond(ax, y, pr, plo, phi, color)
            ax.text(-0.375, y, "  Pooled", ha="left", va="center", fontsize=9.5,
                    fontweight="bold", color=INK)
            ax.text(0.52, y, f"{pr:+.2f}  [{plo:+.2f}, {phi:+.2f}]", ha="right", va="center",
                    fontsize=8.8, fontweight="bold", color=INK, family="DejaVu Sans Mono")

    ax.set_xlim(-0.40, 0.54); ax.set_ylim(y - 0.4, 1.05)
    ax.set_xlabel("Correlation of status with number of children  (Pearson r, Fisher-z pooled)",
                  fontsize=9.5, color=INK)
    ax.set_xticks([-0.3, -0.2, -0.1, 0, 0.1, 0.2, 0.3])
    ax.tick_params(axis="x", colors=MUTED, labelsize=8.5, length=3)
    ax.text(-0.30, 1.0, "fewer children", ha="center", va="bottom", fontsize=7.5, color=MUTED, style="italic")
    ax.text(0.30, 1.0, "more children", ha="center", va="bottom", fontsize=7.5, color=MUTED, style="italic")
    for sp in ("top", "right", "left"):
        ax.spines[sp].set_visible(False)
    ax.spines["bottom"].set_color(GRID)
    ax.set_yticks([])
    ax.set_title("Status and reproductive success: a sex reversal that cancels in aggregate",
                 fontsize=12.5, fontweight="bold", color=INK, loc="left", pad=14)

    fig.tight_layout()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(str(OUT) + ".png", facecolor=SURFACE, bbox_inches="tight")
    fig.savefig(str(OUT) + ".pdf", facecolor=SURFACE, bbox_inches="tight")
    print("wrote", OUT.name + ".png / .pdf")


if __name__ == "__main__":
    main()
