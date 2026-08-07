#!/usr/bin/env python3
"""
100_d1b_assemble_screen.py — D.1.b, stage A5 assembler.

Collect the blinded screen verdicts, join back to the Tier-B frame (restoring the metadata and
discovery provenance the screen never saw), verify full coverage, and emit the tiered corpus, the
pooling sets, the sibling-routing queues, and the screen report. Mirrors `76_d3b_assemble_screen.py`
with four D.1.b-specific departures, each a frozen A1 decision:

  * THREE pooling sets, never one. D.1.b's outcome levels are realized fertility, stated intention or
    ideal, and family-formation behaviour, and the scope forbids pooling them. Family formation is in
    scope because the diffused package is a claim about the whole family form and its earliest
    observable effects land there — but a marriage-timing result is not evidence about births, and
    this script will not emit a file that lets it become one.

  * A FOURTH output that is not a pooling set: the Wall-5 stratum. `MECHANISM_UNRESOLVED_SCHOOLING`
    records are schooling-to-fertility estimates that decompose no mechanism. Scope call 2 keeps them
    out of every pool and reports them as a count. Their count *relative to* the primary
    schooling-ideational cell is the chapter's expected central number, so it is computed here rather
    than left for prose to assert.

  * The title-only stratum is folded in with its provenance intact. Those 1,578 records were assigned
    UNCERTAIN / INSUFFICIENT_INFO by the rubric's own title-only policy without a model call. They
    count in the frame denominator and are flagged `assigned_by: rubric_title_only_policy_not_model`
    so no downstream reader mistakes them for screened records.

  * `OFF_*` cells carry NOT_RELEVANT and still populate the sibling queues. In this taxonomy the
    verdict says whether the paper is ours and the cell says whose it is; the routing queues read the
    cell, not the verdict.

Tiers: T1 = RELEVANT and found by both citation channels; T2 = RELEVANT, single channel; T3 =
UNCERTAIN (the recall net, retained for audit, not included); excluded = NOT_RELEVANT.

Outputs (output/):
  {slug}-screen-tiers.json                     full joined and tiered corpus
  {slug}-estimand-ready-realized.json          RELEVANT, primary cell, non-review, realized fertility
  {slug}-estimand-ready-stated.json            ... stated intention or ideal
  {slug}-estimand-ready-family-formation.json  ... family-formation behaviour
  {slug}-wall5-unresolved-schooling.json       the Wall-5 denominator; never pooled
  {slug}-theory-stream.json                    DI_THEORY; separate, not empirical recall
  {slug}-routing-queues.json                   per-sibling-chapter route-away lists
  {slug}-screen-report.md
"""
import argparse, json, sys
from collections import Counter, defaultdict
from pathlib import Path

SLUG = "caldwell-wealth-flows-westernization"
HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
LOGS = REPO / "literature" / "search-logs"
OUT = REPO / "output"
OUT.mkdir(exist_ok=True)

PRIMARY = {"PRIMARY_DI_BELIEF", "PRIMARY_SCHOOLING_IDEATIONAL",
           "PRIMARY_MEDIA_WESTERN_MODEL", "PRIMARY_WESTERN_CONTACT",
           "DIFFUSION_INDEPENDENT_OF_STRUCTURE"}
THEORY = {"DI_THEORY"}
ROUTE = {"OFF_WEALTH_FLOWS_C3f": "C.3.f", "OFF_POSTMATERIALIST_D1a": "D.1.a",
         "OFF_DIFFUSION_CHANNEL_A20": "A.20", "OFF_FERTILITY_CONTROL_A3": "A.3",
         "OFF_FEMALE_AUTONOMY_D2a": "D.2.a", "OFF_SCHOOLING_ECONOMIC": "C.3.b / C.2.e",
         "OFF_CULTURAL_EVOLUTION_D1c": "D.1.c"}
LEVEL_FILES = {"REALIZED_FERTILITY": "realized",
               "STATED_INTENTION_OR_IDEAL": "stated",
               "FAMILY_FORMATION_BEHAVIOUR": "family-formation"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--allow-incomplete", action="store_true",
                    help="assemble a PARTIAL, visibly marked diagnostic from the batches screened so "
                         "far. Never a frozen corpus and never a denominator for a rate.")
    args = ap.parse_args()

    manifest = json.loads((LOGS / f"{SLUG}-screen-manifest.json").read_text())
    frame = {r["paperId"]: r for r in json.loads((REPO / manifest["source"]).read_text())}

    verdicts, missing = {}, []
    for entry in manifest["manifest"]:
        vp = REPO / entry["output"]
        if not vp.exists():
            missing.append(entry["batch"]); continue
        for rec in json.loads(vp.read_text()):
            verdicts[rec["paperId"]] = rec
    if missing and not args.allow_incomplete:
        print(f"FAIL-CLOSED: {len(missing)} batches missing: {missing[:15]}", file=sys.stderr)
        return 1

    title_only = json.loads((LOGS / f"{SLUG}-title-only-stratum.json").read_text())
    for rec in title_only:
        verdicts[rec["paperId"]] = rec

    unjoined = set(verdicts) - set(frame)
    uncovered = set(frame) - set(verdicts)
    if unjoined:
        print(f"FAIL-CLOSED: {len(unjoined)} verdicts not in frame", file=sys.stderr)
        return 1
    if uncovered and not args.allow_incomplete:
        print(f"FAIL-CLOSED: {len(uncovered)} frame records with no verdict", file=sys.stderr)
        return 1

    # Partial mode. The danger of a partial screen is not that it is incomplete — that is stated
    # everywhere below — but that its RATES look like the finished ones. A cell share computed over 65
    # of 125 batches is an estimate with sampling error; a cell share over 125 is a census. Batch
    # assignment was a deterministic shuffle (seed 1063), so the screened subset IS a random sample of
    # the abstract-bearing stratum and its rates are unbiased estimates of the whole. That is exactly
    # why they are seductive, so every artifact this mode writes carries the partial marker in its
    # filename and its header.
    partial = bool(missing or uncovered)
    suffix = "-PARTIAL" if partial else ""
    if partial:
        # Frame records in unscreened batches are dropped from the corpus rather than silently
        # counted as NOT_RELEVANT, which is the error that would make the partial look complete.
        frame = {k: v for k, v in frame.items() if k in verdicts}

    corpus = []
    for pid, v in verdicts.items():
        f = frame[pid]
        channels = f.get("discovery_channels") or []
        both = len(channels) > 1
        verdict = v["verdict"]
        tier = ("T1" if (verdict == "RELEVANT" and both) else
                "T2" if verdict == "RELEVANT" else
                "T3" if verdict == "UNCERTAIN" else "excluded")
        corpus.append({**{k: f.get(k) for k in
                          ("paperId", "doi", "title", "year", "authors", "venue",
                           "cited_by_count", "discovery_channels", "seed_ids")},
                       **{k: v.get(k) for k in
                          ("verdict", "estimand_cell", "outcome_level", "shared_with", "treatment",
                           "outcome", "structural_change_held_fixed", "setting_era",
                           "evidence_type", "reason")},
                       "tier": tier,
                       "model_screened": v.get("assigned_by") != "rubric_title_only_policy_not_model"})
    corpus.sort(key=lambda r: (r["tier"], r["estimand_cell"], -(r.get("year") or 0)))
    (OUT / f"{SLUG}{suffix}-screen-tiers.json").write_text(json.dumps(corpus, indent=2, ensure_ascii=False))

    # --- pooling sets: one per outcome level, never combined ---
    pools = defaultdict(list)
    for r in corpus:
        if (r["verdict"] == "RELEVANT" and r["estimand_cell"] in PRIMARY
                and r["evidence_type"] != "review"):
            key = LEVEL_FILES.get(r["outcome_level"])
            if key:
                pools[key].append(r)
            elif r["outcome_level"] == "MULTIPLE":
                # A paper reporting more than one level enters EVERY level's set, flagged, because
                # which of its estimates belongs where is an extraction question, not a screen one.
                for k in LEVEL_FILES.values():
                    pools[k].append({**r, "multi_level_needs_extraction_split": True})
    for key in LEVEL_FILES.values():
        (OUT / f"{SLUG}{suffix}-estimand-ready-{key}.json").write_text(
            json.dumps(pools.get(key, []), indent=2, ensure_ascii=False))

    wall5 = [r for r in corpus if r["estimand_cell"] == "MECHANISM_UNRESOLVED_SCHOOLING"]
    (OUT / f"{SLUG}{suffix}-wall5-unresolved-schooling.json").write_text(
        json.dumps(wall5, indent=2, ensure_ascii=False))
    theory = [r for r in corpus if r["estimand_cell"] in THEORY]
    (OUT / f"{SLUG}{suffix}-theory-stream.json").write_text(json.dumps(theory, indent=2, ensure_ascii=False))

    queues = defaultdict(list)
    for r in corpus:
        if r["estimand_cell"] in ROUTE:
            queues[ROUTE[r["estimand_cell"]]].append(
                {k: r[k] for k in ("paperId", "doi", "title", "year", "estimand_cell", "reason")})
    (OUT / f"{SLUG}{suffix}-routing-queues.json").write_text(
        json.dumps({k: v for k, v in sorted(queues.items())}, indent=2, ensure_ascii=False))

    # --- report ---
    cells = Counter(r["estimand_cell"] for r in corpus)
    verd = Counter(r["verdict"] for r in corpus)
    tiers = Counter(r["tier"] for r in corpus)
    screened = sum(r["model_screened"] for r in corpus)
    n_prim_school = cells["PRIMARY_SCHOOLING_IDEATIONAL"]
    n_wall5 = len(wall5)
    banner = ([f"# A5 blinded title/abstract screen — {SLUG} (D.1.b) — **PARTIAL**", "",
               f"> **THIS IS A PARTIAL SCREEN AND NOT A CORPUS.** {len(manifest['manifest'])-len(missing)} "
               f"of {len(manifest['manifest'])} batches are screened; **{len(missing)} batches "
               f"({len(uncovered):,} records) are unscreened and are excluded from every count below.**",
               ">",
               "> Batch assignment was a deterministic shuffle, so the screened batches are a random "
               "sample of the abstract-bearing stratum and the RATES below are unbiased estimates of "
               "the whole. That is what makes them dangerous: they look like finished numbers. Do not "
               "quote a count from this file as the chapter's evidence base, do not freeze it as gold, "
               "and do not use it as the denominator of a recall figure.", ""]
              if partial else
              [f"# A5 blinded title/abstract screen — {SLUG} (D.1.b)", ""])
    L = banner + [
         f"Screened corpus **{len(corpus):,}** records. **{screened:,} were model-screened**; the remaining "
         f"**{len(corpus)-screened:,}** ({100*(len(corpus)-screened)/len(corpus):.0f}%) carry no "
         "abstract and were assigned `UNCERTAIN` / `INSUFFICIENT_INFO` by the rubric's own title-only "
         "policy without a model call. They stay in the corpus and in every denominator. **Quote both "
         "numbers together; the screened count alone overstates coverage.**", "",
         "## Verdicts and tiers", "",
         "| | n |", "|---|---|"]
    for k, n in verd.most_common():
        L.append(f"| {k} | {n:,} |")
    L += ["", "| tier | n |", "|---|---|"]
    for k in ("T1", "T2", "T3", "excluded"):
        L.append(f"| {k} | {tiers.get(k,0):,} |")
    L += ["", "## Estimand cells", "", "| cell | n |", "|---|---|"]
    for k, n in cells.most_common():
        L.append(f"| `{k}` | {n:,} |")
    L += ["", "## Pooling sets (never combined)", "", "| outcome level | n |", "|---|---|"]
    for key in LEVEL_FILES.values():
        L.append(f"| {key} | {len(pools.get(key, [])):,} |")
    L += ["",
          "The three levels are reported and stored separately. A marriage-timing or nuclear-residence "
          "result is evidence for the mechanism and is not evidence about births.", "",
          "## Wall 5 — the unresolved-schooling denominator", "",
          f"- `PRIMARY_SCHOOLING_IDEATIONAL` (mechanism decomposed): **{n_prim_school}**",
          f"- `MECHANISM_UNRESOLVED_SCHOOLING` (no decomposition visible): **{n_wall5}**"]
    if n_prim_school or n_wall5:
        share = 100 * n_wall5 / max(1, n_wall5 + n_prim_school)
        L.append(f"- share of the schooling evidence that cannot be assigned a mechanism: "
                 f"**{share:.0f}%**")
    L += ["",
          "Scope call 2 keeps the unresolved class out of every pool. The ratio above is the honest "
          "statement of how much of the schooling literature can bear on this chapter at all, and it "
          "is computed from the screen rather than asserted in prose. Note the screen sees only "
          "abstracts, and a mechanism decomposition almost never appears in one, so this is an upper "
          "bound on the unresolved share — extraction is where a decomposition can actually be seen.",
          "", "## Sibling routing queues", "", "| chapter | n |", "|---|---|"]
    for k, v in sorted(queues.items()):
        L.append(f"| {k} | {len(v):,} |")
    L += ["", f"Theory stream (`DI_THEORY`): **{len(theory):,}** — separate, not counted toward "
          "empirical recall.", ""]
    (OUT / f"{SLUG}{suffix}-screen-report.md").write_text("\n".join(L) + "\n")

    print(("PARTIAL: " if partial else "") + f"corpus {len(corpus):,} (model-screened {screened:,}, title-only {len(corpus)-screened:,})")
    print("tiers:", dict(tiers))
    print("pools:", {k: len(pools.get(k, [])) for k in LEVEL_FILES.values()})
    print(f"wall5 unresolved {n_wall5} vs primary schooling {n_prim_school}; theory {len(theory)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
