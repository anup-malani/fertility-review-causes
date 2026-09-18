#!/usr/bin/env python3
"""
94_a3_assemble_screen.py — A.3 (diffusion & social-learning of fertility control), stage A5 assembler.

Collect the 89 blinded screen verdicts, join back to the Tier-B frame (restore the metadata and
discovery provenance the screen never saw), verify full coverage, and emit the tiered corpus + the
estimand-ready pooling set + the theory stream + the screen report. Mirrors D.3.b step 76, with the
A.3-specific departures:

  * A.3's pooling integrity: the pooling set is RELEVANT ∩ a PRIMARY cell ∩ non-review, non-theory
    evidence. Reviews may hold a PRIMARY cell (rubric rule 5) and are excluded HERE on evidence_type
    (substring `review`), not by distorting the cell at screen.
  * Instead of D.3.b's stated/realized outcome-level split, A.3 splits the pooling set by
    `identification_of_diffusion`: SEPARATES_FROM_COMMON_SHOCK (the identified core) vs
    DESCRIPTIVE_RESIDUAL_ONLY (the Princeton-style residual). The A1 scope predicts a thin identified
    core; that asymmetry is the load-bearing finding to report, not to launder into one number.
  * Two theory cells (DIFFUSION_THEORY, PRINCETON_CANON) form a SEPARATE stream that does NOT count
    toward empirical recall.

Route-away cells: OFF_CHANNEL_A20 -> A.20, OFF_TECHNOLOGY_A2 -> A.2, OFF_STIGMA_LEVEL_A6 -> A.6,
OFF_VERTICAL_A19 -> A.19, OFF_PROGRAM_A5 -> A.5, OFF_VALUE_D1 -> D.1; OFF_OTHER/OFF_OUTCOME/REVERSE ->
mechanism/context.
Tiers: T1 = RELEVANT & both-channel (backward+forward corroborated); T2 = RELEVANT & single-channel;
T3 = UNCERTAIN; excluded = NOT_RELEVANT.

Outputs (output/):
  {slug}-screen-tiers.json          full joined + tiered corpus
  {slug}-estimand-ready.json        RELEVANT & primary cell & non-review/theory (the pooling set)
  {slug}-theory-stream.json         RELEVANT/UNCERTAIN & either theory cell (separate, not recall)
  {slug}-screen-report.md
"""
import json, re, sys
from pathlib import Path
from collections import Counter

SLUG = "diffusion-of-fertility-control"
HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
LOGS = REPO / "literature" / "search-logs"
OUT = REPO / "output"
OUT.mkdir(exist_ok=True)

PRIMARY_EMPIRICAL = {"PRIMARY_SOCIAL_EXPOSURE", "PRIMARY_SPATIAL_DIFFUSION",
                     "PRIMARY_CULTURAL_BOUNDARY_CONTENT", "PRIMARY_LEGITIMATION_SPREAD"}
THEORY_CELLS = {"DIFFUSION_THEORY", "PRINCETON_CANON"}
ROUTE = {"OFF_CHANNEL_A20": "A.20", "OFF_TECHNOLOGY_A2": "A.2", "OFF_STIGMA_LEVEL_A6": "A.6",
         "OFF_VERTICAL_A19": "A.19", "OFF_PROGRAM_A5": "A.5", "OFF_VALUE_D1": "D.1"}
VALID_CELLS = PRIMARY_EMPIRICAL | THEORY_CELLS | set(ROUTE) | {
    "OFF_OTHER", "OFF_OUTCOME", "REVERSE", "INSUFFICIENT_INFO", "NA"}
CANON = {c.upper(): c for c in VALID_CELLS}
SEP, DESC = "SEPARATES_FROM_COMMON_SHOCK", "DESCRIPTIVE_RESIDUAL_ONLY"


def nt(t):
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9\s]", " ", (t or "").lower())).strip()[:70]


PREPRINT_HOSTS = ("10.31235", "10.31234", "10.21203", "10.2139", "10.1101", "10.31219", "10.31730",
                  "10.3386", "osf.io", "researchsquare", "ssrn", "biorxiv", "medrxiv", "arxiv",
                  "preprints.org", "repec")


def is_preprint(r):
    doi = (r.get("doi") or "").lower()
    return (not r.get("venue")) or any(h in doi for h in PREPRINT_HOSTS)


def dedup(items):
    """Drop duplicates on EITHER identical DOI or identical normalized title, version-of-record first
    so a preprint/working-paper twin collapses onto its published version (see D.3.b step 76)."""
    ordered = sorted(enumerate(items), key=lambda p: (is_preprint(p[1]), p[0]))
    seen_doi, seen_title, out = set(), set(), []
    for _, r in ordered:
        doi = (r.get("doi") or "").lower()
        title = nt(r.get("title"))
        if (doi and doi in seen_doi) or (title and title in seen_title):
            continue
        if doi:
            seen_doi.add(doi)
        if title:
            seen_title.add(title)
        out.append(r)
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

    rows, bad_cell = [], []
    for pid, p in frame.items():
        v = verdicts.get(pid)
        if not v:
            continue
        verdict = (v.get("verdict") or "").upper()
        raw_cell = (v.get("estimand_cell") or "NA").strip()
        cell = CANON.get(raw_cell.upper())
        if cell is None:
            bad_cell.append((pid, raw_cell)); cell = "NA"
        ident = (v.get("identification_of_diffusion") or "NA").upper()
        both = len(p.get("discovery_channels") or []) > 1
        tier = 1 if (verdict == "RELEVANT" and both) else 2 if verdict == "RELEVANT" else 3 if verdict == "UNCERTAIN" else 0
        rows.append({"paperId": pid, "title": p.get("title"), "year": p.get("year"),
                     "doi": p.get("doi"), "authors": p.get("authors"), "venue": p.get("venue"),
                     "verdict": verdict, "cell": cell,
                     "diffusion_channel": v.get("diffusion_channel"),
                     "identification_of_diffusion": ident,
                     "evidence_type": (v.get("evidence_type") or "").lower(),
                     "route_to": ROUTE.get(cell),
                     "discovery_channels": p.get("discovery_channels"), "both_channel": both,
                     "tier": tier, "outcome": v.get("outcome"), "reason": v.get("reason")})
    json.dump(rows, open(OUT / f"{SLUG}-screen-tiers.json", "w"), indent=2, ensure_ascii=False)

    rel = [r for r in rows if r["verdict"] == "RELEVANT"]
    primary = [r for r in rel if r["cell"] in PRIMARY_EMPIRICAL]
    reviews = [r for r in primary if "review" in r["evidence_type"]]
    poolable = dedup([r for r in primary if "review" not in r["evidence_type"]
                      and "theor" not in r["evidence_type"]])
    identified = [r for r in poolable if r["identification_of_diffusion"] == SEP]
    descriptive = [r for r in poolable if r["identification_of_diffusion"] == DESC]
    theory = dedup([r for r in rows if r["verdict"] in ("RELEVANT", "UNCERTAIN")
                    and r["cell"] in THEORY_CELLS])
    json.dump(poolable, open(OUT / f"{SLUG}-estimand-ready.json", "w"), indent=2, ensure_ascii=False)
    json.dump(theory, open(OUT / f"{SLUG}-theory-stream.json", "w"), indent=2, ensure_ascii=False)

    vc = Counter(r["verdict"] for r in rows)
    tc = Counter(r["tier"] for r in rows)
    cellc = Counter(r["cell"] for r in rel)
    poolcells = Counter(r["cell"] for r in poolable)
    theoryc = Counter(r["cell"] for r in theory)

    # routing decoy audit: a decoy's duplicate OpenAlex record may have entered the frame
    res = json.load(open(LOGS / f"{SLUG}-anchor-resolution.json"))
    decoy_titles = {nt(it["openalex"].get("title")): it["openalex"].get("title")
                    for it in res["resolved"] if it.get("is_decoy")}
    decoy_hits = [(decoy_titles[nt(r["title"])], r["verdict"], r["cell"])
                  for r in rows if nt(r["title"]) in decoy_titles]
    title_only = sum(1 for p in frame.values() if len((p.get("abstract") or "").strip()) < 30)
    unroutable = sum(1 for r in rows if r["cell"] == "INSUFFICIENT_INFO")

    n_pool, n_id, n_desc = len(poolable), len(identified), len(descriptive)
    ratio = (f"{n_desc / n_id:.1f}x" if n_id else "undefined (no identified studies)")

    L = [f"# LLM screen — tiers + estimand-ready pooling set — {SLUG}", "",
         f"Screened the full Tier-B frame ({len(frame):,} candidates) blind on title+abstract under "
         f"the A.3 six-wall rubric (Haiku, GACS D2a), then joined verdicts back to discovery provenance. "
         f"{len(rows):,} scored"
         + (f"; ⚠️ {len(unscored)} unscored, {len(missing)} batches missing." if (unscored or missing)
            else " (full coverage; 0 missing)."), "",
         "## Verdicts", "",
         f"- RELEVANT {vc.get('RELEVANT',0)} · UNCERTAIN {vc.get('UNCERTAIN',0)} · "
         f"NOT_RELEVANT {vc.get('NOT_RELEVANT',0)}", "",
         "## Tiers", "",
         f"- **Tier 1** (relevant, both-channel corroborated): {tc.get(1,0)}",
         f"- **Tier 2** (relevant, single-channel): {tc.get(2,0)}",
         f"- **Tier 3** (uncertain): {tc.get(3,0)}",
         f"- excluded (not relevant): {tc.get(0,0)}", "",
         "Estimand cells among RELEVANT: " + ", ".join(f"{c} {n}" for c, n in cellc.most_common()), "",
         "## The pooling set and the identified/descriptive split", "",
         "The pooling set is RELEVANT ∩ a PRIMARY cell ∩ non-review, non-theory evidence, deduplicated",
         "(version-of-record over preprint/working-paper twin). A.3's binding question is not topic",
         "coverage but *identification*: whether a design separates social diffusion from a common",
         "economic/cultural shock hitting neighbours at once (the reflection problem). So the set is",
         "split on `identification_of_diffusion`, never combined into one number.", "",
         f"- **Pooling set (distinct): {n_pool}** → `{SLUG}-estimand-ready.json`",
         "  - by cell: " + (", ".join(f"{c} {n}" for c, n in poolcells.most_common()) or "—"),
         f"- **Identified core** (SEPARATES_FROM_COMMON_SHOCK): **{n_id}**",
         f"- **Descriptive residual** (DESCRIPTIVE_RESIDUAL_ONLY): **{n_desc}**",
         f"- reviews holding a primary cell (excluded from the pool on evidence_type): {len(reviews)}",
         f"- **Theory stream** (RELEVANT/UNCERTAIN ∩ {' or '.join(sorted(THEORY_CELLS))}): "
         f"**{len(theory)} distinct** → `{SLUG}-theory-stream.json` — SEPARATE; not empirical recall.",
         "  - by cell: " + (", ".join(f"{c} {n}" for c, n in theoryc.most_common()) or "—"), "",
         "### The scope's predicted thin identified core, realized", "",
         f"Descriptive residual {n_desc} vs identified core {n_id} ({ratio} the identified core). The A1 "
         "scope predicted A.3's evidence would be rich in descriptive Princeton-style residual and thin "
         "on designs that identify contagion apart from a common shock. That asymmetry is the "
         "load-bearing caveat for the whole hypothesis and is reported, not smoothed away.", "",
         "## Required audit logs", "",
         "### (1) Routing decoys"]
    if decoy_hits:
        for t, vd, c in decoy_hits:
            L.append(f"- `{t[:70]}` → **{vd} / {c}**")
    else:
        L.append("- (no decoy duplicate matched by normalized title in the scored rows)")
    L += ["", "Route-away volume overall: " + ", ".join(
        f"{c} {sum(1 for r in rows if r['cell'] == c)}" + (f" (→{ROUTE[c]})" if c in ROUTE else "")
        for c in list(ROUTE) + ["OFF_OTHER", "OFF_OUTCOME", "REVERSE"]) + ".", "",
        "### (2) Title-only ceiling",
        f"{title_only:,} of {len(frame):,} frame candidates ({title_only/len(frame):.1%}) are title-only. "
        f"The screen marked {unroutable:,} records `INSUFFICIENT_INFO`; these are the RA gate / full-text "
        "resolution queue.", "",
        "### (3) Rubric-conformance",
        f"- cell values outside the taxonomy: {len(bad_cell)}" + (f" (e.g. {bad_cell[:3]})" if bad_cell else ""),
        "", "## Caveats", "",
        "- Verdicts are AUTOMATED (Haiku D2a recall filter). The Sonnet precision pass (D2b) and RA "
        "sign-off on the boundary/UNCERTAIN papers are the remaining steps before any pooled estimate.",
        "- Tier 1 rests on both-channel (backward+forward) corroboration, not frozen gold membership.",
        "- This screen tiers the CORPUS; it does not measure search recall. Recall is graded separately "
        "against the frozen gold after the production query is fit.",
        "- Wall 1 (A.3 vs A.20 channels) is the highest-cost misroute; the RA gate should sample "
        "`diffusion_channel=MASS_MEDIA` and the OFF_CHANNEL_A20 rows first.",
        "- Distinct counts dedup by DOI-then-normalized-title, version-of-record preferred."]
    (OUT / f"{SLUG}-screen-report.md").write_text("\n".join(L) + "\n")
    print(f"scored {len(rows)} | REL {vc.get('RELEVANT',0)} UNC {vc.get('UNCERTAIN',0)} NOT {vc.get('NOT_RELEVANT',0)}")
    print(f"tiers T1 {tc.get(1,0)} T2 {tc.get(2,0)} T3 {tc.get(3,0)} excl {tc.get(0,0)}")
    print(f"pooling set {n_pool} (identified {n_id} / descriptive {n_desc}) {dict(poolcells)}")
    print(f"theory stream {len(theory)} {dict(theoryc)} | reviews excluded {len(reviews)}")
    print(f"conformance: {len(bad_cell)} bad cells | decoy hits {len(decoy_hits)}")


if __name__ == "__main__":
    main()
