#!/usr/bin/env python3
"""
56b_assemble_sets.py — assemble the two nested extractable sets (fine filter §4.1).

Reads the frozen per-study extraction records (temp/extraction/rec_*.json, produced
by the step-56 Sonnet pass) and the confirmed pool, and emits:

  CAUSAL SET (inner) -> causal-credibility.  Studies that credibly identify the
    effect, with an extractable causal record. Grouped by treatment_type subgroup
    (reform / pension-wealth / eligibility / ...). A partial correlation r is
    DERIVED here (never extracted): r = t / sqrt(t^2 + df), with t = estimate/se
    when a t-stat is not printed and df ~ n-2 when df is unknown. This is the
    downstream harmonization the design defers out of the extraction step.

  R2 SET (outer) -> demographic-significance.  All studies with an extractable
    association record (a fertility~OAS regression), reported DESCRIPTIVELY (a
    table of partial correlations / R²), NOT pooled into one number.

  NARRATIVE-ONLY.  In-cell studies where neither record is extractable.

Deterministic given the frozen records. Numbers are carried with their verbatim
provenance quote; the RA verifies them (step 58) before anything is pooled.
"""
import json, os, glob, math

SLUG = "old-age-security-pension-crowdout"
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
def rp(*a): return os.path.join(ROOT, *a)

pool = {r["paperId"]: r for r in json.load(open(rp("output", f"{SLUG}-fine-resolved.json")))}
recs = {}
for f in glob.glob(rp("temp", "extraction", "rec_*.json")):
    try:
        r = json.load(open(f))
        recs[r["paperId"]] = r
    except Exception:
        pass

def num(x):
    try: return float(x)
    except (TypeError, ValueError): return None

def partial_r(cr):
    """Derive partial correlation from whatever the causal/assoc record printed."""
    t = num(cr.get("t_stat"))
    if t is None:
        est, se = num(cr.get("estimate") if "estimate" in cr else cr.get("coef")), num(cr.get("se"))
        if est is not None and se not in (None, 0):
            t = est / se
    if t is None:
        return None, None
    df = num(cr.get("df_or_n")) or num(cr.get("n"))
    df = (df - 2) if df and df > 3 else (df or 100)      # crude fallback df
    r = t / math.sqrt(t * t + df)
    return round(r, 4), round(r * r, 4)

causal, r2set, narrative = [], [], []
for pid, meta in pool.items():
    rec = recs.get(pid)
    if not rec:
        continue                                          # not yet extracted (no PDF / agent pending)
    title = meta["title"]
    cr = rec.get("causal_record") or {}
    rr = rec.get("r2_record") or {}
    did_causal = rec.get("identifies_causal") and cr.get("extractable")
    if did_causal:
        pr, pr2 = partial_r(cr)
        causal.append({
            "paperId": pid, "title": title, "doi": meta.get("doi"), "is_gold": meta.get("is_gold"),
            "treatment_type": cr.get("treatment_type") or "other",
            "identification": rec.get("identification_strategy"),
            "estimate": num(cr.get("estimate")), "se": num(cr.get("se")),
            "ci": [num(cr.get("ci_low")), num(cr.get("ci_high"))],
            "t_stat": num(cr.get("t_stat")), "n": num(cr.get("n")), "sign": cr.get("sign"),
            "outcome_units": cr.get("outcome_units"), "interpretation": cr.get("estimate_interpretation"),
            "partial_r": pr, "spec": cr.get("preferred_spec"),
            # author's own demographic-magnitude statement (feeds the per-setting derived share, step 59)
            "reported_magnitude": rec.get("reported_magnitude") or cr.get("reported_magnitude"),
            "quote": cr.get("quote"), "confidence": rec.get("confidence"),
        })
    if rr.get("extractable"):
        pr, pr2 = partial_r(rr)
        r2set.append({
            "paperId": pid, "title": title, "doi": meta.get("doi"), "is_gold": meta.get("is_gold"),
            "coef": num(rr.get("coef")), "se": num(rr.get("se")), "t_stat": num(rr.get("t_stat")),
            "df_or_n": num(rr.get("df_or_n")), "partial_r": rr.get("partial_r") or pr,
            "partial_r2": pr2, "r2_model": num(rr.get("r2_model")),
            "also_causal": bool(did_causal), "quote": rr.get("quote"),
        })
    if not did_causal and not rr.get("extractable"):
        narrative.append({"paperId": pid, "title": title, "doi": meta.get("doi"),
                          "reason": rec.get("notes")})

# ---- outputs ----
json.dump(causal, open(rp("output", f"{SLUG}-causal-set.json"), "w"), ensure_ascii=False, indent=1)
json.dump(r2set, open(rp("output", f"{SLUG}-r2-set.json"), "w"), ensure_ascii=False, indent=1)

from collections import defaultdict
byt = defaultdict(list)
for c in causal: byt[c["treatment_type"]].append(c)

L = [f"# Causal set (inner) — identified effect on fertility · {SLUG}", "",
     f"{len(causal)} extractable causal record(s), grouped by treatment type. "
     "Pooled within subgroup (random-effects) at step 59; partial *r* is derived, all numbers RA-verified "
     "at step 58 before pooling.", ""]
for tt, cs in sorted(byt.items(), key=lambda x: -len(x[1])):
    L.append(f"## treatment type: {tt}  ({len(cs)})")
    L.append("| study | est | se | t | n | outcome | partial r | quote |")
    L.append("|---|---|---|---|---|---|---|---|")
    for c in cs:
        L.append(f"| {(c['title'] or '')[:38]}{' ·gold' if c['is_gold'] else ''} "
                 f"| {c['estimate']} | {c['se']} | {c['t_stat']} | {c['n']} "
                 f"| {(c['outcome_units'] or '')[:22]} | {c['partial_r']} | {(c['quote'] or '')[:60]}… |")
    L.append("")
open(rp("output", f"{SLUG}-causal-set.md"), "w").write("\n".join(L) + "\n")

R = [f"# R² set (outer) — explanatory power · {SLUG}", "",
     f"{len(r2set)} extractable association record(s). **Descriptive** — a distribution of partial "
     "correlations, NOT a single pooled number. Feeds the demographic-significance verdict.", "",
     "| study | coef | se | t | df/N | partial r | partial R² | model R² | also causal? |",
     "|---|---|---|---|---|---|---|---|---|"]
for x in r2set:
    R.append(f"| {(x['title'] or '')[:40]}{' ·gold' if x['is_gold'] else ''} | {x['coef']} | {x['se']} "
             f"| {x['t_stat']} | {x['df_or_n']} | {x['partial_r']} | {x['partial_r2']} | {x['r2_model']} "
             f"| {'yes' if x['also_causal'] else ''} |")
open(rp("output", f"{SLUG}-r2-set.md"), "w").write("\n".join(R) + "\n")

if narrative:
    N = [f"# Narrative-only — in-cell but not extractable · {SLUG}", ""]
    for x in narrative:
        N.append(f"- {(x['title'] or '')[:70]} — {(x['reason'] or '')[:100]}")
    open(rp("output", f"{SLUG}-narrative-only.md"), "w").write("\n".join(N) + "\n")

print(f"extraction records assembled: {len(recs)} of {len(pool)} studies extracted")
print(f"  CAUSAL set:    {len(causal)}  (by treatment: {dict((k,len(v)) for k,v in byt.items())})")
print(f"  R² set:        {len(r2set)}")
print(f"  narrative-only:{len(narrative)}")
print(f"  awaiting extraction (no PDF/agent): {len(pool)-len(recs)}")
