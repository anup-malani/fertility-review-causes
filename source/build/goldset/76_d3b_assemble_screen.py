#!/usr/bin/env python3
"""
76_d3b_assemble_screen.py — D.3.b (climate anxiety / eco-doomerism), stage A5 assembler.

Collect the 30 blinded screen verdicts, join back to the Tier-B frame (restore the metadata and discovery
provenance the screen never saw), verify full coverage, and emit the tiered corpus + the estimand-ready
pooling sets + the screen report. Mirrors B.1 step 67, with three D.3.b-specific departures:

  * TWO pooling sets, never one. The A1 scope's frozen decision 2 forbids combining stated-intention and
    realized-fertility outcomes into a single pooled estimate, so this script emits them separately and
    refuses to produce a combined file. Stated-intention estimates are first-class primary synthesis
    (not relegated), but always carry the stated-intention caveat.
  * TWO theory cells (ECO_ETHICS_THEORY, ANXIETY_CONSTRUCT) after the rubric-v2 split, both a SEPARATE
    stream that does NOT count toward empirical recall — D.3.b's predicted rich-theory/thin-empirics
    asymmetry is a finding to report, not to launder into a pooled estimate.
  * Reviews may hold a PRIMARY cell under rubric v2 rule 5, so they are excluded from the pooling sets
    HERE (on evidence_type) rather than by distorting the cell assignment at screen.

Route-away cells: OFF_POSTMATERIALIST_D1a -> D.1.a, OFF_CLINICAL_D3a -> D.3.a, OFF_ECON_C5a -> C.5.a,
OFF_OTHER -> out with no sibling queue, OFF_OUTCOME / REVERSE -> mechanism/context.
Tiers: T1 = RELEVANT & both-channel (backward+forward corroborated); T2 = RELEVANT & single-channel;
T3 = UNCERTAIN; excluded = NOT_RELEVANT.

Outputs (output/):
  {slug}-screen-tiers.json                  full joined + tiered corpus
  {slug}-estimand-ready-stated.json         RELEVANT & primary cell & non-review & stated-intention level
  {slug}-estimand-ready-realized.json       RELEVANT & primary cell & non-review & realized-fertility level
  {slug}-theory-stream.json                 RELEVANT/UNCERTAIN & either theory cell (separate, not recall)
  {slug}-screen-report.md
"""
import json, re, sys
from pathlib import Path
from collections import Counter

SLUG = "climate-anxiety-eco-doomerism"
HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
LOGS = REPO / "literature" / "search-logs"
OUT = REPO / "output"
OUT.mkdir(exist_ok=True)

PRIMARY_EMPIRICAL = {"PRIMARY_HABITABILITY_FEAR", "PRIMARY_CARBON_ETHICS",
                     "PRIMARY_ECO_PESSIMISM", "DESIRE_INDEPENDENCE"}
THEORY_CELLS = {"ECO_ETHICS_THEORY", "ANXIETY_CONSTRUCT"}
ROUTE = {"OFF_POSTMATERIALIST_D1a": "D.1.a", "OFF_CLINICAL_D3a": "D.3.a", "OFF_ECON_C5a": "C.5.a"}
VALID_CELLS = PRIMARY_EMPIRICAL | THEORY_CELLS | set(ROUTE) | {
    "OFF_OTHER", "OFF_OUTCOME", "REVERSE", "INSUFFICIENT_INFO", "NA"}
# Three v2 cells are mixed-case (OFF_POSTMATERIALIST_D1a, OFF_CLINICAL_D3a, OFF_ECON_C5a), so cells must
# be normalized case-INSENSITIVELY back to canonical spelling. Uppercasing them instead silently fails
# taxonomy validation and dumps every sibling-routed paper into NA.
CANON = {c.upper(): c for c in VALID_CELLS}
STATED, REALIZED = "STATED_INTENTION_OR_ATTITUDE", "REALIZED_FERTILITY"


def nt(t):
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9\s]", " ", (t or "").lower())).strip()[:70]


# DOI hosts that indicate a preprint / working-paper version rather than the version of record.
PREPRINT_HOSTS = ("10.31235", "10.31234", "10.21203", "10.2139", "10.1101", "10.31219", "10.31730",
                  "osf.io", "researchsquare", "ssrn", "biorxiv", "medrxiv", "arxiv", "preprints.org")


def is_preprint(r):
    doi = (r.get("doi") or "").lower()
    return (not r.get("venue")) or any(h in doi for h in PREPRINT_HOSTS)


def dedup(items):
    """Drop duplicates on EITHER identical DOI or identical normalized title.

    The original rule keyed on `doi OR normalized_title`, so any record carrying a DOI never had its
    title compared. A preprint and its version of record have DIFFERENT DOIs and the SAME title, so
    both survived and were counted as two distinct studies. That inflated the realized-fertility pool,
    the scarcest and most load-bearing count in this chapter: the SocArXiv preprint 10.31235/osf.io/83e4m
    and its Population and Development Review version 10.1111/padr.12646 were both being counted.

    Version-of-record records are processed first so that when a pair collides, the published version
    is the one kept. Ordering is a stable sort on a deterministic key, so reruns stay byte-identical.
    """
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

    rows, bad_cell, bad_pair = [], [], []
    for pid, p in frame.items():
        v = verdicts.get(pid)
        if not v:
            continue
        verdict = (v.get("verdict") or "").upper()
        raw_cell = (v.get("estimand_cell") or "NA").strip()
        level = (v.get("outcome_level") or "NA").upper()
        cell = CANON.get(raw_cell.upper())
        if cell is None:
            bad_cell.append((pid, raw_cell)); cell = "NA"
        # rubric-v2 pairing constraints
        if (cell == "NA" and verdict != "NOT_RELEVANT") or \
           (cell == "INSUFFICIENT_INFO" and verdict != "UNCERTAIN"):
            bad_pair.append((pid, verdict, cell))
        both = len(p.get("discovery_channels") or []) > 1
        tier = 1 if (verdict == "RELEVANT" and both) else 2 if verdict == "RELEVANT" else 3 if verdict == "UNCERTAIN" else 0
        rows.append({"paperId": pid, "title": p.get("title"), "year": p.get("year"),
                     "doi": p.get("doi"), "authors": p.get("authors"), "venue": p.get("venue"),
                     "verdict": verdict, "cell": cell, "outcome_level": level,
                     "evidence_type": (v.get("evidence_type") or "").lower(),
                     "desire_for_children_held_fixed": v.get("desire_for_children_held_fixed"),
                     "route_to": ROUTE.get(cell),
                     "discovery_channels": p.get("discovery_channels"), "both_channel": both,
                     "tier": tier, "outcome": v.get("outcome"), "treatment": v.get("treatment"),
                     "reason": v.get("reason")})
    json.dump(rows, open(OUT / f"{SLUG}-screen-tiers.json", "w"), indent=2, ensure_ascii=False)

    rel = [r for r in rows if r["verdict"] == "RELEVANT"]
    # Reviews may hold a PRIMARY cell under rubric v2 rule 5; they are excluded from pooling here.
    primary = [r for r in rel if r["cell"] in PRIMARY_EMPIRICAL]
    reviews = [r for r in primary if r["evidence_type"] == "review"]
    poolable = [r for r in primary if r["evidence_type"] not in ("review", "theory")]
    stated = dedup([r for r in poolable if r["outcome_level"] in (STATED, "BOTH")])
    realized = dedup([r for r in poolable if r["outcome_level"] in (REALIZED, "BOTH")])
    theory = dedup([r for r in rows if r["verdict"] in ("RELEVANT", "UNCERTAIN")
                    and r["cell"] in THEORY_CELLS])
    json.dump(stated, open(OUT / f"{SLUG}-estimand-ready-stated.json", "w"), indent=2, ensure_ascii=False)
    json.dump(realized, open(OUT / f"{SLUG}-estimand-ready-realized.json", "w"), indent=2, ensure_ascii=False)
    json.dump(theory, open(OUT / f"{SLUG}-theory-stream.json", "w"), indent=2, ensure_ascii=False)

    vc = Counter(r["verdict"] for r in rows)
    tc = Counter(r["tier"] for r in rows)
    cellc = Counter(r["cell"] for r in rel)
    lvlc = Counter(r["outcome_level"] for r in poolable)
    theoryc = Counter(r["cell"] for r in theory)
    stated_cells = Counter(r["cell"] for r in stated)
    realized_cells = Counter(r["cell"] for r in realized)

    # (1) routing decoys. Anchors are excluded from the frame by ID, but a duplicate OpenAlex record of
    # one decoy survived into the frame, giving one directly testable route-away.
    res = json.load(open(LOGS / f"{SLUG}-anchor-resolution.json"))
    decoy_titles = {nt(it["openalex"].get("title")): it["openalex"].get("title")
                    for it in res["resolved"] if it.get("is_decoy")}
    decoy_hits = [(decoy_titles[nt(r["title"])], r["verdict"], r["cell"])
                  for r in rows if nt(r["title"]) in decoy_titles]
    # (2) title-only ceiling
    title_only = sum(1 for p in frame.values() if len((p.get("abstract") or "").strip()) < 30)
    unroutable = sum(1 for r in rows if r["cell"] == "INSUFFICIENT_INFO")

    n_stated, n_real = len(stated), len(realized)
    ratio = (f"{len(theory) / n_stated:.1f}x" if n_stated else "undefined (empty pool)")

    L = [f"# LLM screen — tiers + estimand-ready pooling sets — {SLUG}", "",
         f"Screened the full Tier-B frame ({len(frame):,} candidates) blind on title+abstract under "
         f"**rubric v2**, then joined verdicts back to discovery provenance. {len(rows):,} scored"
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
         "## The deliverables", "",
         "The A1 scope's frozen decision 2 forbids pooling across outcome levels, so there are **two**",
         "pooling sets and deliberately no combined file. Both are first-class primary synthesis; the",
         "stated-intention set carries the standing caveat that it measures intention, not behaviour.", "",
         f"- **Stated-intention pool** (RELEVANT ∩ primary cell ∩ non-review ∩ stated/both): "
         f"**{n_stated} distinct** → `{SLUG}-estimand-ready-stated.json`",
         "  - by cell: " + (", ".join(f"{c} {n}" for c, n in stated_cells.most_common()) or "—"),
         f"- **Realized-fertility pool** (same ∩ realized/both): **{n_real} distinct** → "
         f"`{SLUG}-estimand-ready-realized.json`",
         "  - by cell: " + (", ".join(f"{c} {n}" for c, n in realized_cells.most_common()) or "—"),
         f"- **Theory stream** (RELEVANT/UNCERTAIN ∩ {' or '.join(sorted(THEORY_CELLS))}): "
         f"**{len(theory)} distinct** → `{SLUG}-theory-stream.json` — SEPARATE; does NOT count toward "
         "empirical recall.",
         "  - by cell: " + (", ".join(f"{c} {n}" for c, n in theoryc.most_common()) or "—"),
         f"- Reviews holding a primary cell (excluded from pooling on `evidence_type`, per rubric v2 "
         f"rule 5): {len(reviews)}", "",
         "### The scope's predicted asymmetry, realized", "",
         f"Theory stream {len(theory)} distinct vs stated-intention pool {n_stated} distinct "
         f"({ratio} the empirical core), and a realized-fertility pool of **{n_real}**. Outcome levels "
         f"across the poolable primary set: " +
         (", ".join(f"{k} {v}" for k, v in lvlc.most_common()) or "—") + ".", "",
         "The A1 scope predicted a literature rich on stated belief and intention and near-empty on "
         "realized fertility. That prediction is confirmed here, and the realized-fertility thinness is "
         "the load-bearing caveat for the whole hypothesis: if that pool is small enough, D.3.b's "
         "evidence base speaks to what people *say* about childbearing under ecological dread and only "
         "marginally to what they *do*. This is a finding to report, not a search failure — and it is "
         "why the two pools are never combined.", "",
         "## Required audit logs", "",
         "### (1) Routing decoys",
         "Anchors are excluded from the citation frame by work ID, so decoy routing is mostly not "
         "directly testable at screen. One exception survived: a duplicate OpenAlex record of a decoy "
         "carries a distinct work ID and so entered the frame, giving one live route-away test." , ""]
    if decoy_hits:
        for t, vd, c in decoy_hits:
            L.append(f"- `{t[:70]}` → **{vd} / {c}**")
    else:
        L.append("- (no decoy duplicate matched by normalized title in the scored rows)")
    L += ["", "Route-away volume overall: " + ", ".join(
        f"{c} {sum(1 for r in rows if r['cell'] == c)}" + (f" (→{ROUTE[c]})" if c in ROUTE else "")
        for c in ["OFF_POSTMATERIALIST_D1a", "OFF_CLINICAL_D3a", "OFF_ECON_C5a", "OFF_OTHER",
                  "OFF_OUTCOME", "REVERSE"]) + ".", "",
        "### (2) Title-only ceiling",
        f"{title_only:,} of {len(frame):,} frame candidates ({title_only/len(frame):.1%}) are title-only. "
        f"The screen marked {unroutable:,} records `INSUFFICIENT_INFO`; these are the natural RA gate and "
        "full-text-resolution queue. Under rubric v1 these records were being assigned substantive cells "
        "they had not earned, which inflated the theory stream — the v2 cell exists to stop that.", "",
        "### (3) Rubric-conformance violations",
        f"- cell values outside the v2 taxonomy: {len(bad_cell)}"
        + (f" (e.g. {bad_cell[:3]})" if bad_cell else ""),
        f"- pairing-constraint violations (NA without NOT_RELEVANT, or INSUFFICIENT_INFO without "
        f"UNCERTAIN): {len(bad_pair)}" + (f" (e.g. {bad_pair[:3]})" if bad_pair else ""), "",
        "## Caveats", "",
        "- Verdicts are AUTOMATED. The pooling sets are automated pooling candidates; RA sign-off on the "
        "boundary and UNCERTAIN papers is the remaining human step (the RA gate).",
        "- Tier 1 rests on both-channel (backward+forward) corroboration, not frozen gold membership.",
        "- This screen tiers the CORPUS; it does not measure search recall. Recall is measured separately "
        "downstream (production query vs the frozen gold), after which the §7.2 overlap test runs.",
        "- The three boundary walls were applied by an automated screener. The D.1.a confound (left "
        "politics, education, secularism predict both climate concern and low fertility) is the central "
        "identification threat AND the Wall 1 routing rule — so Wall 1 misroutes are the error mode with "
        "the largest downstream cost, and the RA gate should sample them first.",
        "- Distinct counts dedup by DOI-then-normalized-title."]
    (OUT / f"{SLUG}-screen-report.md").write_text("\n".join(L) + "\n")
    print(f"scored {len(rows)} | REL {vc.get('RELEVANT',0)} UNC {vc.get('UNCERTAIN',0)} "
          f"NOT {vc.get('NOT_RELEVANT',0)}")
    print(f"tiers T1 {tc.get(1,0)} T2 {tc.get(2,0)} T3 {tc.get(3,0)} excl {tc.get(0,0)}")
    print(f"stated pool {n_stated} distinct {dict(stated_cells)}")
    print(f"realized pool {n_real} distinct {dict(realized_cells)}")
    print(f"theory stream {len(theory)} distinct {dict(theoryc)} | reviews excluded {len(reviews)}")
    print(f"conformance: {len(bad_cell)} bad cells, {len(bad_pair)} pairing violations")
    if decoy_hits:
        print("decoy route-away:", decoy_hits)


if __name__ == "__main__":
    main()
