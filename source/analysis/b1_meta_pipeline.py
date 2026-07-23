#!/usr/bin/env python3
"""TICK-035 (prototype): B.1 status-fertility meta-analysis pipeline.

Pools the association between an evolutionary status/wealth predictor and reproductive
success (number of children), moderated by contraceptive availability and sex. This is the
chapter's accepted quantitative core: the prediction is a positive association where
contraception is absent, attenuated or reversed where it is present.

Design mirrors source/analysis/oas_meta_pipeline.py: stdlib only (csv + math), a conservative
pooling rule (>= MIN_STUDIES independent studies per pool), and a Fisher-z metric so
correlation-type effects from heterogeneous designs can be combined and back-transformed to r.

Effects are read from extraction/{SLUG}-effects.csv. Only rows that are primary, on the
STATUS_REPRODUCTION estimand, not excluded, and carrying a usable effect + variance are pooled;
everything else (pending table extraction, reviews, other estimands) is reported but not pooled.
Pooled numbers are written only when the conservative rule is met.
"""
from __future__ import annotations

import csv
import math
from pathlib import Path

SLUG = "evolutionary-sex-drive-contraceptive-decoupling"
ROOT = Path(__file__).resolve().parents[2]
EFFECTS = ROOT / "extraction" / f"{SLUG}-effects.csv"
OUT = ROOT / "output" / "tables" / f"{SLUG}-meta-analysis-summary.csv"

MIN_STUDIES = 3  # conservative pooling rule: fewer than this is reported, not pooled
Z95 = 1.959963985


# ---- effect-size harmonization to the Fisher-z metric -------------------------------------

def fisher_z(r: float) -> float:
    """Fisher variance-stabilizing transform of a correlation."""
    r = max(min(r, 0.999999), -0.999999)
    return math.atanh(r)


def inv_fisher_z(z: float) -> float:
    return math.tanh(z)


def z_and_var(row: dict) -> tuple[float, float] | None:
    """Return (fisher_z effect, variance of z) for a poolable row, or None if not usable.

    Supports two input forms:
      effect_type='zr'  -> effect_value is already a Fisher-z; variance from its CI or SE.
      effect_type='r'   -> Pearson r; converted to Fisher-z; variance = 1/(n-3).
    """
    et = (row.get("effect_type") or "").strip().lower()
    val = _num(row.get("effect_value"))
    if val is None:
        return None
    se = _num(row.get("se"))
    lo, hi = _num(row.get("ci_lower")), _num(row.get("ci_upper"))
    n = _num(row.get("n"))

    if et == "zr":
        z = val
        if se is not None:
            var = se ** 2
        elif lo is not None and hi is not None:
            var = ((hi - lo) / (2 * Z95)) ** 2
        else:
            return None
        return z, var
    if et == "r":
        z = fisher_z(val)
        if n is not None and n > 3:
            return z, 1.0 / (n - 3)
        if lo is not None and hi is not None:
            zl, zh = fisher_z(lo), fisher_z(hi)
            return z, ((zh - zl) / (2 * Z95)) ** 2
        return None
    return None  # beta / OR need separate harmonization; out of scope for the prototype


def _num(x) -> float | None:
    try:
        s = str(x).strip().replace("−", "-")
        return float(s) if s not in ("", "NA", "None") else None
    except (TypeError, ValueError):
        return None


# ---- random-effects pooling (DerSimonian-Laird) -------------------------------------------

def dersimonian_laird(effects: list[float], variances: list[float]) -> dict:
    """Random-effects pool on the Fisher-z scale. Returns pooled z, SE, tau^2, Q, I^2, and the
    back-transformed r with its 95% CI."""
    k = len(effects)
    wf = [1.0 / v for v in variances]
    mean_fixed = sum(w * e for w, e in zip(wf, effects)) / sum(wf)
    Q = sum(w * (e - mean_fixed) ** 2 for w, e in zip(wf, effects))
    df = k - 1
    C = sum(wf) - sum(w ** 2 for w in wf) / sum(wf)
    tau2 = max(0.0, (Q - df) / C) if C > 0 else 0.0
    wr = [1.0 / (v + tau2) for v in variances]
    z = sum(w * e for w, e in zip(wr, effects)) / sum(wr)
    se = math.sqrt(1.0 / sum(wr))
    i2 = max(0.0, (Q - df) / Q) * 100 if Q > 0 else 0.0
    zlo, zhi = z - Z95 * se, z + Z95 * se
    return {
        "k": k, "pooled_z": z, "se_z": se, "tau2": tau2, "Q": Q, "I2_pct": i2,
        "pooled_r": inv_fisher_z(z), "r_ci_lower": inv_fisher_z(zlo), "r_ci_upper": inv_fisher_z(zhi),
    }


# ---- driver -------------------------------------------------------------------------------

def load_poolable(rows: list[dict]) -> list[dict]:
    keep = []
    for r in rows:
        if (r.get("estimand") or "").strip() != "STATUS_REPRODUCTION":
            continue
        if (r.get("is_primary_estimate") or "").strip().lower() not in ("yes", "y", "true", "1"):
            continue
        if (r.get("exclude") or "").strip().lower() in ("yes", "y", "true", "1"):
            continue
        zv = z_and_var(r)
        if zv is None:
            continue
        r["_z"], r["_var"] = zv
        keep.append(r)
    return keep


def pool_group(rows: list[dict], label: str) -> dict:
    studies = {r["study_id"] for r in rows}
    if len(studies) < MIN_STUDIES:
        return {"group": label, "k_effects": len(rows), "k_studies": len(studies),
                "status": f"insufficient (<{MIN_STUDIES} studies); reported not pooled",
                "pooled_r": "", "r_ci_lower": "", "r_ci_upper": "", "I2_pct": "", "tau2": ""}
    res = dersimonian_laird([r["_z"] for r in rows], [r["_var"] for r in rows])
    return {"group": label, "k_effects": res["k"], "k_studies": len(studies), "status": "pooled",
            "pooled_r": round(res["pooled_r"], 4), "r_ci_lower": round(res["r_ci_lower"], 4),
            "r_ci_upper": round(res["r_ci_upper"], 4), "I2_pct": round(res["I2_pct"], 1),
            "tau2": round(res["tau2"], 4)}


def run() -> list[dict]:
    rows = list(csv.DictReader(open(EFFECTS)))
    poolable = load_poolable(rows)
    summaries = [pool_group(poolable, "overall")]
    for mod, field in (("contraceptive_availability", "contraceptive_availability"), ("sex", "sex")):
        vals = sorted({(r.get(field) or "").strip() for r in poolable if (r.get(field) or "").strip()})
        for v in vals:
            summaries.append(pool_group([r for r in poolable if (r.get(field) or "").strip() == v],
                                        f"{mod}={v}"))
    return summaries


def main() -> None:
    rows = list(csv.DictReader(open(EFFECTS)))
    poolable = load_poolable(rows)
    summaries = run()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(summaries[0].keys()))
        w.writeheader()
        w.writerows(summaries)
    n_effects = len(rows)
    n_status = sum(1 for r in rows if (r.get("estimand") or "") == "STATUS_REPRODUCTION")
    n_pending = sum(1 for r in rows if (r.get("needs_pi") or "").strip().lower() in ("yes", "y"))
    print(f"effect rows: {n_effects} | STATUS_REPRODUCTION: {n_status} | "
          f"poolable now: {len(poolable)} | pending extraction: {n_pending}")
    for s in summaries:
        print(f"  {s['group']:34} k_studies={s['k_studies']} {s['status']}"
              + (f" r={s['pooled_r']} [{s['r_ci_lower']},{s['r_ci_upper']}] I2={s['I2_pct']}%"
                 if s["status"] == "pooled" else ""))
    print(f"summary -> {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
