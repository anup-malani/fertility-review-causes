#!/usr/bin/env python3
"""TICK-051: D.3.b two-track synthesis.

Mirrors b1_meta_pipeline.py / oas_meta_pipeline.py, with one structural difference that
is the whole point of this script: **it evaluates the project's conservative pooling rule
and, when the rule is not met, refuses to pool and says why.** A pipeline that silently
emits a pooled number whenever it has two rows is how a chapter ends up reporting a
structural estimate it has not earned.

The two tracks are never combined (A1 scope decision 2).

Pooling rule, inherited from OAS/B.1 and applied here:
  1. same outcome family
  2. harmonised effect metric
  3. >= 3 INDEPENDENT studies  <- independence, not row count
Anything looser is labelled a structured summary, not a structural estimate.

Independence is the binding constraint for D.3.b's realized track: Golovina & Jokela and
Peters et al. are both GSOEP. Counting them as two would be double-counting one panel.

Outputs:
  output/tables/climate-anxiety-eco-doomerism-realized-summary.csv
  output/tables/climate-anxiety-eco-doomerism-pooling-decision.csv
  output/tables/climate-anxiety-eco-doomerism-synthesis-report.md
"""
from __future__ import annotations

import csv
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SLUG = "climate-anxiety-eco-doomerism"
EFFECTS_REALIZED = ROOT / "extraction" / f"{SLUG}-effects-realized.csv"
STUDIES = ROOT / "extraction" / f"{SLUG}-studies.csv"
OUT_DIR = ROOT / "output" / "tables"
MIN_INDEPENDENT_STUDIES = 3

# Studies sharing a data source are one independent unit. Keyed by study_id.
DATA_SOURCE = {
    "golovina_2024_soep_worries": "GSOEP",
    "peters_2023_soep_reciprocal": "GSOEP",
    "jylha_2025_swedish_ggs": "Swedish GGS",
    "weychert_2026_ukhls_news": "UKHLS",
}


def load_rows(path: Path) -> list[dict]:
    with open(path) as fh:
        return list(csv.DictReader(fh))


def independent_units(study_ids) -> set[str]:
    """Collapse studies onto their underlying data source."""
    return {DATA_SOURCE.get(s, s) for s in study_ids}


def primary_poolable(rows: list[dict]) -> list[dict]:
    """One estimate per study: poolable, not excluded, flagged primary where marked."""
    by_study: dict[str, dict] = {}
    for r in rows:
        if r.get("poolable") != "yes" or r.get("exclude") == "yes":
            continue
        sid = r["study_id"]
        if sid not in by_study or r.get("is_primary_estimate") == "yes":
            by_study[sid] = r
    return list(by_study.values())


def assess_pooling(rows: list[dict], track: str) -> dict:
    """Apply the conservative rule and return a decision record with reasons."""
    candidates = primary_poolable(rows)
    studies = {r["study_id"] for r in candidates}
    units = independent_units(studies)
    metrics = {r["effect_type"] for r in candidates}
    with_ci = [r for r in candidates
               if r.get("ci_lower") not in ("NR", "", None)]

    reasons: list[str] = []
    if len(units) < MIN_INDEPENDENT_STUDIES:
        shared = sorted(
            src for src in units
            if sum(1 for s in studies if DATA_SOURCE.get(s, s) == src) > 1
        )
        msg = (f"only {len(units)} independent data source(s) "
               f"({', '.join(sorted(units)) or 'none'}) across {len(studies)} study/studies; "
               f"rule requires >= {MIN_INDEPENDENT_STUDIES}")
        if shared:
            msg += f". Studies sharing a source: {', '.join(shared)}"
        reasons.append(msg)
    if len(metrics) > 1:
        reasons.append(f"effect metrics are not harmonised: {', '.join(sorted(metrics))}")
    if len(with_ci) < len(candidates):
        reasons.append(f"{len(candidates) - len(with_ci)} of {len(candidates)} poolable "
                       "estimates have no reported CI or SE")

    return {
        "track": track,
        "poolable_rows": len(candidates),
        "distinct_studies": len(studies),
        "independent_units": len(units),
        "unit_names": "; ".join(sorted(units)),
        "metrics": "; ".join(sorted(metrics)),
        "estimates_with_ci": len(with_ci),
        "pool_permitted": "no" if reasons else "yes",
        "output_type": "structured summary (NOT a pooled estimate)" if reasons else "random-effects pool",
        "reasons_withheld": " | ".join(reasons),
    }


def hr_to_log(row: dict) -> tuple[float, float] | None:
    """log-HR and its SE from a hazard ratio with a 95% CI, for display only."""
    try:
        hr = float(row["effect_value"]); lo = float(row["ci_lower"]); hi = float(row["ci_upper"])
    except (ValueError, KeyError, TypeError):
        return None
    if min(hr, lo, hi) <= 0:
        return None
    return math.log(hr), (math.log(hi) - math.log(lo)) / (2 * 1.959964)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    realized = load_rows(EFFECTS_REALIZED)
    decision = assess_pooling(realized, "realized_fertility")

    # Stated track: no effect table exists yet -- record that explicitly rather than
    # letting its absence read as "nothing to report".
    stated_decision = {
        "track": "stated_intention", "poolable_rows": 0, "distinct_studies": 0,
        "independent_units": 0, "unit_names": "", "metrics": "", "estimates_with_ci": 0,
        "pool_permitted": "no",
        "output_type": "NOT YET EXTRACTED",
        "reasons_withheld": ("61 studies in the frozen stated pool; no effect extraction has been "
                             "run. Absence of a pooled estimate here reflects work not done, not "
                             "evidence weighed."),
    }

    with open(OUT_DIR / f"{SLUG}-pooling-decision.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(decision.keys()))
        w.writeheader(); w.writerows([decision, stated_decision])

    # Structured summary of every realized estimate carrying an interval.
    summary_rows = []
    for r in realized:
        if r.get("ci_lower") in ("NR", "", None):
            continue
        lg = hr_to_log(r)
        summary_rows.append({
            "effect_id": r["effect_id"], "study_id": r["study_id"],
            "data_source": DATA_SOURCE.get(r["study_id"], "unknown"),
            "sample": r["sample"], "model": r["model"][:60],
            "effect_type": r["effect_type"], "effect": r["effect_value"],
            "ci_lower": r["ci_lower"], "ci_upper": r["ci_upper"],
            "significant": r["significant"],
            "log_effect": f"{lg[0]:.4f}" if lg else "",
            "se_log": f"{lg[1]:.4f}" if lg else "",
            "adjusts_politics": r["adjusts_politics"],
            "wall1_class": r["predictor_wall1_class"],
        })
    with open(OUT_DIR / f"{SLUG}-realized-summary.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(summary_rows[0].keys()))
        w.writeheader(); w.writerows(summary_rows)

    lines = [f"# D.3.b two-track synthesis — {SLUG}", "",
             "Generated by `source/analysis/d3b_meta_pipeline.py`. The two tracks are never",
             "combined (A1 scope decision 2).", "",
             "## Pooling decision", ""]
    for d in (decision, stated_decision):
        lines += [f"### {d['track']}", "",
                  f"- Poolable rows: {d['poolable_rows']} across {d['distinct_studies']} study/studies",
                  f"- **Independent data sources: {d['independent_units']}**"
                  + (f" ({d['unit_names']})" if d["unit_names"] else ""),
                  f"- Pool permitted: **{d['pool_permitted']}**",
                  f"- Output: **{d['output_type']}**", ""]
        if d["reasons_withheld"]:
            lines += ["Reasons the pooled estimate is withheld:", ""]
            lines += [f"- {x}" for x in d["reasons_withheld"].split(" | ")]
            lines.append("")

    lines += [
        "## What this means for the chapter", "",
        "The realized-fertility track **cannot be meta-analysed**, and the reason is",
        "independence rather than sample size. Golovina & Jokela and Peters et al. are both",
        "analyses of GSOEP; counting them as two studies would double-count one German panel.",
        "Jylhä reports OLS coefficients on number of children — a different estimand from the",
        "hazard ratios, not harmonisable with them. Weychert reports no interval at all. The",
        "AEA study was never retrieved.",
        "",
        "This is a refusal to pool, not a failed pool. Section 6 of the chapter should say so",
        "in those terms, and should not describe a forest plot that does not exist.",
        "",
        "## Structured summary — realized track", "",
        "| Study | Source | Sample | Effect (95% CI) | Sig. | Adj. politics |",
        "|---|---|---|---|---|---|",
    ]
    for s in summary_rows:
        lines.append(f"| {s['study_id'][:26]} | {s['data_source']} | {s['sample'][:22]} | "
                     f"{s['effect']} ({s['ci_lower']}, {s['ci_upper']}) | {s['significant']} | "
                     f"{s['adjusts_politics']} |")
    lines += ["",
        "## The two GSOEP analyses disagree", "",
        "Golovina & Jokela report HR 0.82 (0.75, 0.90) in the total sample; Peters et al.",
        "report HR 0.92 (0.82, 1.04), not significant, on the same panel. The specifications",
        "differ — Golovina uses the climate-change worry item over 2009–2020, very-worried",
        "versus not; Peters a lagged major-environmental-concern dummy over 1984–2020 on first",
        "birth only. The chapter should report the disagreement rather than resolve it.",
        "",
        "## The cohort result", "",
        "Peters' only significant estimate is in the cohort born **before** 1970 — HR 0.73",
        "(0.57, 0.94). Among those born 1970 or later it is a precise null, 0.98 (0.85, 1.12).",
        "D.3.b is scoped SDT-only and describes a 2020s phenomenon among young adults, so the",
        "one cohort where the association appears is the one the hypothesis does not predict.",
        "",
        "## Moderator analyses not run, and why", "",
        "The adjusted-versus-unadjusted contrast this ticket pre-specified as the chapter's",
        "central test cannot be estimated: with 3 independent sources and 1 of them adjusting",
        "for political attitudes, there is no contrast to estimate. It is recorded here as",
        "not-estimable rather than dropped, so the pre-specification is not quietly abandoned.",
    ]
    (OUT_DIR / f"{SLUG}-synthesis-report.md").write_text("\n".join(lines) + "\n")

    print(f"realized track: {decision['poolable_rows']} poolable rows, "
          f"{decision['distinct_studies']} studies, "
          f"{decision['independent_units']} independent sources")
    print(f"  pool permitted: {decision['pool_permitted']} -> {decision['output_type']}")
    for r in decision["reasons_withheld"].split(" | "):
        print(f"  - {r}")
    print(f"tables -> {OUT_DIR.relative_to(ROOT)}/{SLUG}-*.csv, -synthesis-report.md")


if __name__ == "__main__":
    main()
