#!/usr/bin/env python3
"""
50b_assemble_tiers.py — collect screen verdicts, apply the estimand gate, emit tiers + pooling set.

Reads temp/screen/verdict_XX.json (one per batch, written by the screening agents), validates every
pooled paperId got a verdict, then:
  - tiers: T1 = RELEVANT & gold-member (gold-corroborated); T2 = RELEVANT & single-channel;
           T3 = UNCERTAIN; excluded = NOT_RELEVANT.
           (No fresh snowball channel was run on this corpus, so multi-channel agreement isn't
            available here; T1 rests on gold membership. Documented, not hidden.)
  - topical meta-analysis-ready = (T1 ∪ T2) ∩ empirical (evidence_type != theory).
  - estimand-ready pooling set   = topical ∩ estimand_cell==PRIMARY.
  - screen recall of the gold: of the rebuilt-gold PRIMARY anchors present in the pool, how many the
    screen marked RELEVANT & PRIMARY (a sanity check on the automated gate vs the curated gold).

Output: {slug}-screen-tiers.json, {slug}-screen-report.md
"""
import json, sys
from pathlib import Path
from collections import Counter

SLUG = "old-age-security-pension-crowdout"
HERE = Path(__file__).resolve().parent
LOGS = HERE.parents[2] / "literature" / "search-logs"
SCREEN = HERE.parents[2] / "temp" / "screen"
OUT = HERE.parents[2] / "output"

def main():
    manifest = json.load(open(SCREEN / "manifest.json"))
    pool = {p["paperId"]: p for p in json.load(open(LOGS / f"{SLUG}-d1-pool.json"))}
    verdicts = {}
    missing_batches = []
    for m in manifest:
        vf = Path(m["output"])
        if not vf.exists():
            missing_batches.append(m["batch"]); continue
        try:
            arr = json.load(open(vf))
        except json.JSONDecodeError:
            missing_batches.append(m["batch"]); continue
        for v in arr:
            if isinstance(v, dict) and v.get("paperId"):
                verdicts[v["paperId"]] = v
    if missing_batches:
        print(f"WARNING: {len(missing_batches)} batches missing/unparseable: {missing_batches}", file=sys.stderr)
    unscored = [pid for pid in pool if pid not in verdicts]
    if unscored:
        print(f"WARNING: {len(unscored)} pooled papers unscored (e.g. {unscored[:3]})", file=sys.stderr)

    def emp(v): return v.get("evidence_type") not in ("theory",)
    rows = []
    for pid, p in pool.items():
        v = verdicts.get(pid)
        if not v:
            continue
        verdict = (v.get("verdict") or "").upper()
        cell = (v.get("estimand_cell") or "NA").upper()
        is_gold = bool(p.get("is_gold"))
        if verdict == "RELEVANT":
            tier = 1 if is_gold else 2
        elif verdict == "UNCERTAIN":
            tier = 3
        else:
            tier = 0
        rows.append({"paperId": pid, "title": p.get("title"), "verdict": verdict, "cell": cell,
                     "evidence_type": v.get("evidence_type"), "is_gold": is_gold, "tier": tier,
                     "outcome": v.get("outcome"), "mechanism": v.get("mechanism"),
                     "direction": v.get("direction"), "reason": v.get("reason")})
    json.dump(rows, open(OUT / f"{SLUG}-screen-tiers.json", "w"), indent=2, ensure_ascii=False)

    import re as _re
    def _nt(t): return _re.sub(r"\s+", " ", _re.sub(r"[^a-z0-9\s]", " ", (t or "").lower())).strip()[:60]
    def dedup(items):
        seen, out = set(), []
        for r in items:
            k = (r.get("paperId2") or "").lower() or _nt(r.get("title"))
            if k in seen: continue
            seen.add(k); out.append(r)
        return out

    vc = Counter(r["verdict"] for r in rows)
    tc = Counter(r["tier"] for r in rows)
    t12 = [r for r in rows if r["tier"] in (1, 2)]
    topical = [r for r in t12 if r["evidence_type"] != "theory"]
    estimand_ready = [r for r in topical if r["cell"] == "PRIMARY"]
    cellc = Counter(r["cell"] for r in t12)
    # distinct (deduped by normalized title) — the corpus carries preprint/published near-dupes
    d_t1 = len(dedup([r for r in rows if r["tier"] == 1]))
    d_t2 = len(dedup([r for r in rows if r["tier"] == 2]))
    d_topical = len(dedup(topical))
    d_estimand = dedup(estimand_ready)
    json.dump(d_estimand, open(OUT / f"{SLUG}-estimand-ready-set.json", "w"), indent=2, ensure_ascii=False)

    # screen recall of the gold's PRIMARY anchors present in the pool
    tags = {t["id"]: t for t in json.load(open(HERE / "estimand_tierb_tags_rebuilt.json"))}
    gold_prim_in_pool = [pid for pid in pool if tags.get(pid, {}).get("cell") == "PRIMARY"]
    gp_screen_prim = sum(1 for pid in gold_prim_in_pool
                         if verdicts.get(pid, {}).get("estimand_cell", "").upper() == "PRIMARY"
                         and verdicts.get(pid, {}).get("verdict", "").upper() in ("RELEVANT", "UNCERTAIN"))

    L = [f"# LLM screen — tiers + estimand-ready pooling set — {SLUG}", "",
         f"Screened the D1 pool ({len(pool)} papers) with per-paper relevance + estimand extraction, "
         f"then applied the estimand gate. {len(rows)} scored"
         + (f"; ⚠️ {len(unscored)} unscored, {len(missing_batches)} batches missing." if (unscored or missing_batches) else "."), "",
         "## Verdicts", "",
         f"- RELEVANT {vc.get('RELEVANT',0)} · UNCERTAIN {vc.get('UNCERTAIN',0)} · NOT_RELEVANT {vc.get('NOT_RELEVANT',0)}", "",
         "## Tiers  (raw records → distinct after title-dedup)", "",
         f"- **Tier 1** (relevant, gold-corroborated): {tc.get(1,0)} → **{d_t1} distinct**",
         f"- **Tier 2** (relevant, single-channel): {tc.get(2,0)} → **{d_t2} distinct**",
         f"- **Tier 3** (uncertain net): {tc.get(3,0)}",
         f"- excluded (not relevant): {tc.get(0,0)}", "",
         "## Meta-analysis sets (the deliverable)", "",
         f"- **Topical meta-analysis-ready** (T1∪T2 ∩ empirical): {len(topical)} → **{d_topical} distinct**",
         f"- **Estimand-ready pooling set** (topical ∩ PRIMARY cell): {len(estimand_ready)} → **{len(d_estimand)} distinct** "
         f"→ `{SLUG}-estimand-ready-set.json`", "",
         "The corpus carries preprint/published near-duplicates (multiple OpenAlex IDs per paper); the "
         "distinct counts dedup by normalized title. Full dedup (DOI→title clustering, the Thursday "
         "'fine filter') will refine these slightly.", "",
         "Estimand cells within T1∪T2: " + ", ".join(f"{c} {n}" for c, n in cellc.most_common()), "",
         "## Screen vs gold (sanity check)", "",
         f"- gold PRIMARY anchors present in the pool: {len(gold_prim_in_pool)}",
         f"- of those, screen also called PRIMARY (RELEVANT/UNCERTAIN): {gp_screen_prim} "
         f"({gp_screen_prim/max(len(gold_prim_in_pool),1):.0%}) — automated gate vs curated gold agreement", "",
         "## Caveats", "",
         "- Tier 1 rests on gold membership (no fresh snowball channel was run on this corpus), so "
         "multi-channel corroboration is not yet a T1 basis here.",
         "- Automated verdicts (RA gate still pending): the estimand-ready set is the *automated* pooling "
         "candidate; RA sign-off on the boundary/UNCERTAIN papers is the remaining human step.",
         "- Recall of the effect-identifying literature is the separately-measured 80.6% (rebuilt gold); "
         "this screen assigns the *corpus* to tiers and does not re-measure recall."]
    (OUT / f"{SLUG}-screen-report.md").write_text("\n".join(L) + "\n")
    print(f"scored {len(rows)} | RELEVANT {vc.get('RELEVANT',0)} UNCERTAIN {vc.get('UNCERTAIN',0)} NOT {vc.get('NOT_RELEVANT',0)}")
    print(f"tiers: T1 {tc.get(1,0)} T2 {tc.get(2,0)} T3 {tc.get(3,0)} excl {tc.get(0,0)}")
    print(f"topical-ready {len(topical)} | estimand-ready pooling set {len(estimand_ready)}")
    print(f"screen-vs-gold PRIMARY recall {gp_screen_prim}/{len(gold_prim_in_pool)}")

if __name__ == "__main__":
    main()
