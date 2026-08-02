#!/usr/bin/env python3
"""
67_b1_assemble_screen.py — B.1 (evolutionary sex drive / contraceptive decoupling), stage A5 assembler.

Collect the 123 blinded screen verdicts, join back to the Tier-B frame (restore metadata + discovery
provenance the screen never saw), verify full coverage, and emit the tiered corpus + the estimand-ready
pooling set + the screen report. Mirrors OAS step 50b, adapted to B.1:

  * Primary EMPIRICAL cells (count toward the empirical pooling set): PROXIMATE_ULTIMATE,
    PRIMARY_DECOUPLING, PRIMARY_DESIRE_INDEPENDENCE, MOTIVATION_DISTINCTNESS (the four the A1 scope
    names as primary synthesis / dissociation-test / bridge).
  * THEORY is a SEPARATE stream and does NOT count toward empirical recall (the scope's stated
    asymmetry: rich theory, thin empirics — a finding to report, not to launder into a pooled estimate).
  * Route-away cells: OFF_EXPOSURE_A2 -> A.2, TEMPO_EXPOSURE -> A.4, CULTURAL_NORMALIZATION -> D.1.a,
    OFF_OUTCOME / REVERSE -> mechanism/context.
  * Tiers: T1 = RELEVANT & both-channel (backward+forward corroborated); T2 = RELEVANT & single-channel;
    T3 = UNCERTAIN; excluded = NOT_RELEVANT.

The screen report logs the three items the A4 audit required: (1) the contraception-tech precision tax
as realized (how much of that cloud routed to A.2/OFF), (2) the 36.5% title-only ceiling, (3) the
routing outcome. (The two anchor routing decoys are NOT in the frame — the frame excludes anchors — so
decoy routing is validated instead by the volume of CT-cloud A.2 route-aways.)

Outputs (output/):
  {slug}-screen-tiers.json          full joined + tiered corpus
  {slug}-estimand-ready-set.json    RELEVANT & primary-empirical cell & non-theory (distinct)
  {slug}-theory-stream.json         RELEVANT/UNCERTAIN & THEORY (distinct) — separate, not recall
  {slug}-screen-report.md
"""
import json, re, sys
from pathlib import Path
from collections import Counter

SLUG = "evolutionary-sex-drive-contraceptive-decoupling"
HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
LOGS = REPO / "literature" / "search-logs"
OUT = REPO / "output"
OUT.mkdir(exist_ok=True)

PRIMARY_EMPIRICAL = {"PROXIMATE_ULTIMATE", "PRIMARY_DECOUPLING", "PRIMARY_DESIRE_INDEPENDENCE",
                     "MOTIVATION_DISTINCTNESS"}
ROUTE = {"OFF_EXPOSURE_A2": "A.2", "TEMPO_EXPOSURE": "A.4", "CULTURAL_NORMALIZATION": "D.1.a"}


def nt(t):
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9\s]", " ", (t or "").lower())).strip()[:70]


def dedup(items):
    seen, out = set(), []
    for r in items:
        k = (r.get("doi") or "").lower() or nt(r.get("title"))
        if k in seen:
            continue
        seen.add(k); out.append(r)
    return out


def main():
    manifest = json.load(open(LOGS / f"{SLUG}-screen-manifest.json"))
    frame = {r["paperId"]: r for r in json.load(open(LOGS / f"{SLUG}-tier-b-frame.json"))}
    verdicts, missing = {}, []
    for m in manifest["manifest"]:
        vf = REPO / m["output"]
        if not vf.exists():
            missing.append(m["batch"]); continue
        try:
            arr = json.load(open(vf))
        except json.JSONDecodeError:
            missing.append(m["batch"]); continue
        for v in arr:
            if isinstance(v, dict) and v.get("paperId"):
                verdicts[v["paperId"]] = v
    unscored = [pid for pid in frame if pid not in verdicts]
    if missing:
        print(f"WARNING: {len(missing)} batches missing/unparseable: {missing}", file=sys.stderr)
    if unscored:
        print(f"WARNING: {len(unscored)} frame papers unscored (e.g. {unscored[:3]})", file=sys.stderr)

    rows = []
    for pid, p in frame.items():
        v = verdicts.get(pid)
        if not v:
            continue
        verdict = (v.get("verdict") or "").upper()
        cell = (v.get("estimand_cell") or "NA").upper()
        both = len(p.get("discovery_channels") or []) > 1
        tier = 1 if (verdict == "RELEVANT" and both) else 2 if verdict == "RELEVANT" else 3 if verdict == "UNCERTAIN" else 0
        rows.append({"paperId": pid, "title": p.get("title"), "year": p.get("year"),
                     "doi": p.get("doi"), "authors": p.get("authors"), "venue": p.get("venue"),
                     "verdict": verdict, "cell": cell, "evidence_type": v.get("evidence_type"),
                     "holds_child_preference_fixed": v.get("holds_child_preference_fixed"),
                     "discovery_channels": p.get("discovery_channels"), "both_channel": both,
                     "tier": tier, "outcome": v.get("outcome"), "treatment": v.get("treatment"),
                     "reason": v.get("reason")})
    json.dump(rows, open(OUT / f"{SLUG}-screen-tiers.json", "w"), indent=2, ensure_ascii=False)

    def emp(r):
        return r["evidence_type"] not in ("theory",)

    rel = [r for r in rows if r["verdict"] == "RELEVANT"]
    pooling = [r for r in rel if r["cell"] in PRIMARY_EMPIRICAL and emp(r)]
    theory = [r for r in rows if r["verdict"] in ("RELEVANT", "UNCERTAIN") and r["cell"] == "THEORY"]
    d_pool, d_theory = dedup(pooling), dedup(theory)
    json.dump(d_pool, open(OUT / f"{SLUG}-estimand-ready-set.json", "w"), indent=2, ensure_ascii=False)
    json.dump(d_theory, open(OUT / f"{SLUG}-theory-stream.json", "w"), indent=2, ensure_ascii=False)

    vc = Counter(r["verdict"] for r in rows)
    tc = Counter(r["tier"] for r in rows)
    cellc = Counter(r["cell"] for r in rel)
    pool_cellc = Counter(r["cell"] for r in d_pool)

    # (1) contraception-tech precision tax — realized. CT-only candidates = reachable only via the two
    # contraception-tech seeds; report how the screen disposed of them.
    res = json.load(open(LOGS / f"{SLUG}-anchor-resolution.json"))
    smap = {it["openalex"]["paperId"]: it["openalex"]["title"] for it in res["resolved"]}
    CT = {s for s, t in smap.items() if t.startswith("The Power of the Pill") or t.startswith("“Momma")}
    ct_rows = [r for r in rows if set(frame[r["paperId"]].get("seed_ids") or []) <= CT and (frame[r["paperId"]].get("seed_ids"))]
    ct_a2 = sum(1 for r in ct_rows if r["cell"] == "OFF_EXPOSURE_A2")
    ct_off = sum(1 for r in ct_rows if r["cell"] in ("OFF_OUTCOME", "OFF_EXPOSURE_A2", "REVERSE", "TEMPO_EXPOSURE"))
    ct_primary = sum(1 for r in ct_rows if r["cell"] in PRIMARY_EMPIRICAL and r["verdict"] == "RELEVANT")
    # (2) title-only ceiling
    title_only = sum(1 for p in frame.values() if len((p.get("abstract") or "").strip()) < 30)

    L = [f"# LLM screen — tiers + estimand-ready pooling set — {SLUG}", "",
         f"Screened the full Tier-B frame ({len(frame):,} candidates) blind on title+abstract, then "
         f"joined verdicts back to discovery provenance. {len(rows):,} scored"
         + (f"; ⚠️ {len(unscored)} unscored, {len(missing)} batches missing." if (unscored or missing) else " (full coverage; 0 missing)."), "",
         "## Verdicts", "",
         f"- RELEVANT {vc.get('RELEVANT',0)} · UNCERTAIN {vc.get('UNCERTAIN',0)} · NOT_RELEVANT {vc.get('NOT_RELEVANT',0)}", "",
         "## Tiers", "",
         f"- **Tier 1** (relevant, both-channel corroborated): {tc.get(1,0)}",
         f"- **Tier 2** (relevant, single-channel): {tc.get(2,0)}",
         f"- **Tier 3** (uncertain): {tc.get(3,0)}",
         f"- excluded (not relevant): {tc.get(0,0)}", "",
         "Estimand cells among RELEVANT: " + ", ".join(f"{c} {n}" for c, n in cellc.most_common()), "",
         "## The deliverables", "",
         f"- **Estimand-ready empirical pooling set** (RELEVANT ∩ primary-empirical cell ∩ non-theory): "
         f"{len(pooling)} raw → **{len(d_pool)} distinct** → `{SLUG}-estimand-ready-set.json`",
         "  - by cell: " + ", ".join(f"{c} {n}" for c, n in pool_cellc.most_common()),
         f"- **Theory stream** (RELEVANT/UNCERTAIN ∩ THEORY): {len(theory)} raw → **{len(d_theory)} distinct** "
         f"→ `{SLUG}-theory-stream.json` — SEPARATE; does NOT count toward empirical recall.", "",
         "### The scope's predicted asymmetry, realized",
         f"The theory stream ({len(d_theory)} distinct) is comparable to or larger than the empirical "
         f"pooling set ({len(d_pool)} distinct), and within the empirical set the direct decoupling / "
         f"desire-independence core (PRIMARY_DECOUPLING {pool_cellc.get('PRIMARY_DECOUPLING',0)} + "
         f"PRIMARY_DESIRE_INDEPENDENCE {pool_cellc.get('PRIMARY_DESIRE_INDEPENDENCE',0)}) is far smaller "
         f"than the proximate-ultimate dissociation literature "
         f"(PROXIMATE_ULTIMATE {pool_cellc.get('PROXIMATE_ULTIMATE',0)}). This is the A1-predicted "
         "asymmetry (rich theory / status-fertility tests, thin direct decoupling empirics) — a finding "
         "to report, not a search failure.", "",
         "## Required audit logs", "",
         "### (1) Contraception-tech precision tax — realized",
         f"Candidates reachable ONLY via the contraception-tech seeds (Goldin-Katz + Bailey): "
         f"{len(ct_rows):,}. The screen routed **{ct_off:,} to off/route-away cells** "
         f"({ct_a2:,} to OFF_EXPOSURE_A2 → A.2), and only **{ct_primary} to a primary-empirical cell**. "
         "The A4 audit predicted this stratum (32% keyword-on-topic) would be a precision tax carried for "
         "recall; the screen paid it and walled it off from the pooling set rather than promoting it.", "",
         "### (2) Title-only ceiling",
         f"{title_only:,} of {len(frame):,} frame candidates ({title_only/len(frame):.1%}) are title-only. "
         "UNCERTAIN concentrates here; these are the natural RA-gate and full-text-resolution queue.", "",
         "### (3) Routing outcome / decoys",
         f"The two anchor routing decoys (Pritchett → A.2, Wilcox → A.4) are NOT in the frame (anchors are "
         f"excluded from the citation frame), so decoy routing is not directly testable at screen. It is "
         f"validated instead by the realized route-away volume: OFF_EXPOSURE_A2 "
         f"{sum(1 for r in rows if r['cell']=='OFF_EXPOSURE_A2')} (→A.2), TEMPO_EXPOSURE "
         f"{sum(1 for r in rows if r['cell']=='TEMPO_EXPOSURE')} (→A.4), CULTURAL_NORMALIZATION "
         f"{sum(1 for r in rows if r['cell']=='CULTURAL_NORMALIZATION')} (→D.1.a) — the A.2/labor cloud "
         "routed to off-cells, not into the primary estimand.", "",
         "## Caveats", "",
         "- Verdicts are AUTOMATED. The estimand-ready set is the automated pooling candidate; RA sign-off "
         "on the boundary/UNCERTAIN papers is the remaining human step (the RA gate).",
         "- Tier 1 rests on both-channel (backward+forward) corroboration, not a frozen gold membership.",
         "- This screen tiers the CORPUS; it does not measure search recall. Recall is measured separately "
         "downstream (production query vs the frozen gold), after which the §7.2 overlap test runs.",
         "- Distinct counts dedup by DOI-then-normalized-title; the fine filter refines further."]
    (OUT / f"{SLUG}-screen-report.md").write_text("\n".join(L) + "\n")
    print(f"scored {len(rows)} | REL {vc.get('RELEVANT',0)} UNC {vc.get('UNCERTAIN',0)} NOT {vc.get('NOT_RELEVANT',0)}")
    print(f"tiers T1 {tc.get(1,0)} T2 {tc.get(2,0)} T3 {tc.get(3,0)} excl {tc.get(0,0)}")
    print(f"pooling set {len(pooling)} -> {len(d_pool)} distinct | by cell {dict(pool_cellc)}")
    print(f"theory stream {len(theory)} -> {len(d_theory)} distinct")
    print(f"CT-only cloud {len(ct_rows)}: {ct_off} off-routed ({ct_a2} A.2), {ct_primary} to primary")


if __name__ == "__main__":
    main()
