#!/usr/bin/env python3
"""
101_d1b_ra_gate_worksheet.py — TICK-063: build the D.1.b human review gate worksheet.

The screen verdicts in `output/{slug}-screen-tiers.json` are AUTOMATED. This script emits the
worksheet a human signs off on, in strata with different urgencies, and records the sampling rule on
the face of the output so the gate is reproducible rather than an ad hoc read-through. Mirrors
`84_d3b_ra_gate_worksheet.py`; the strata differ because D.1.b's walls differ.

STRATA

  A. DECISIVE — full census, gates extraction.
     Every `DIFFUSION_INDEPENDENT_OF_STRUCTURE` record (the value-added cell: designs that separate
     ideation from structure, which is the only class that can identify this chapter's distinctive
     claim) plus every primary-cell record at `REALIZED_FERTILITY` level (the decisive outcome
     stratum). These are the studies the chapter's verdict will rest on, so none is sampled.

  B. WALL5_SCHOOLING — seeded sample of `MECHANISM_UNRESOLVED_SCHOOLING`.
     **This is the highest-value stratum in the gate and the reason it exists.** The A1 scope
     recorded in advance that a title/abstract screen CANNOT enforce Wall 5: whether a schooling
     estimate decomposes ideational content from wage returns lives in the results tables, invisible
     to an abstract. So the screen's unresolved count is an upper bound by construction, and the
     ratio of unresolved to decomposed is the chapter's expected headline number. A misroute here
     does not just mislabel a paper — it moves the headline. The RA reads full text for this stratum,
     not abstracts, because that is the only place the answer exists.

  C. TITLE_ONLY — seeded sample of the records assigned `INSUFFICIENT_INFO` by rule.
     Those records were never read by a model; the rubric's title-only policy assigned them. A census
     is meaningless (there are ~1,578 of them and the assignment was mechanical). The question worth
     answering is narrower and estimable from a sample: **what share of them would have been primary
     if an abstract had been available?** That share, applied to the stratum, is the honest statement
     of what the abstract-availability limit cost the chapter.

  D. WALL_REFERENCE — seeded samples of each sibling-routing wall, so an overturn rate can be
     reported BY WALL rather than in aggregate. D.3.b's gate overturned five of the twelve decisive
     records it examined, and the overturns clustered by wall; an aggregate rate would have hidden that.

SAMPLING RULE: deterministic throughout. Records are sorted by (year desc, paperId); census strata
take everything; sampled strata take a fixed-seed draw with the seed and n written into the log so
the same draw reproduces. No unseeded randomness anywhere.

Inputs : output/{slug}-screen-tiers.json  (or the -PARTIAL- variant, which is REFUSED — see below)
Outputs: extraction/{slug}-ra-gate.csv
         literature/search-logs/{slug}-ra-gate-log.md
"""
from __future__ import annotations

import csv, json, random, sys
from collections import Counter
from pathlib import Path

SLUG = "caldwell-wealth-flows-westernization"
ROOT = Path(__file__).resolve().parents[3]
TIERS = ROOT / "output" / f"{SLUG}-screen-tiers.json"
GATE = ROOT / "extraction" / f"{SLUG}-ra-gate.csv"
GATE_LOG = ROOT / "literature" / "search-logs" / f"{SLUG}-ra-gate-log.md"

SEED = 20260807
WALL5_SAMPLE_N = 40      # large: this stratum sets the chapter's headline ratio
TITLE_ONLY_SAMPLE_N = 60  # large enough to bound a small primary share with a usable interval
WALL_SAMPLE_N = 12        # per sibling wall, for a by-wall overturn rate

PRIMARY = {"PRIMARY_DI_BELIEF", "PRIMARY_SCHOOLING_IDEATIONAL",
           "PRIMARY_MEDIA_WESTERN_MODEL", "PRIMARY_WESTERN_CONTACT",
           "DIFFUSION_INDEPENDENT_OF_STRUCTURE"}
WALLS = ["OFF_WEALTH_FLOWS_C3f", "OFF_POSTMATERIALIST_D1a", "OFF_DIFFUSION_CHANNEL_A20",
         "OFF_FERTILITY_CONTROL_A3", "OFF_FEMALE_AUTONOMY_D2a", "OFF_SCHOOLING_ECONOMIC",
         "OFF_CULTURAL_EVOLUTION_D1c"]

COLUMNS = ["stratum", "priority", "read_level", "work_id", "doi", "year", "venue",
           "screen_verdict", "screen_cell", "outcome_level", "setting_era",
           "structural_change_held_fixed", "evidence_type", "screen_reason",
           # --- the human fills these ---
           "ra_verdict", "ra_cell", "ra_outcome_level", "ra_route_to", "agree_or_overturn",
           "mechanism_decomposed", "ra_reason", "send_to_fulltext", "ra_initials", "ra_date",
           "title"]


def row(rec, stratum, priority, read_level):
    return {"stratum": stratum, "priority": priority, "read_level": read_level,
            "work_id": rec.get("paperId", ""), "doi": rec.get("doi") or "",
            "year": rec.get("year"), "venue": rec.get("venue") or "",
            "screen_verdict": rec.get("verdict"), "screen_cell": rec.get("estimand_cell"),
            "outcome_level": rec.get("outcome_level"), "setting_era": rec.get("setting_era"),
            "structural_change_held_fixed": rec.get("structural_change_held_fixed"),
            "evidence_type": rec.get("evidence_type"),
            "screen_reason": (rec.get("reason") or "")[:300],
            "ra_verdict": "", "ra_cell": "", "ra_outcome_level": "", "ra_route_to": "",
            "agree_or_overturn": "", "mechanism_decomposed": "", "ra_reason": "",
            "send_to_fulltext": "", "ra_initials": "", "ra_date": "",
            "title": (rec.get("title") or "")[:160]}


def take(pool, n, seed_offset):
    """Deterministic draw. Sort first so the draw does not depend on dict iteration order."""
    pool = sorted(pool, key=lambda r: (-(r.get("year") or 0), r.get("paperId") or ""))
    if len(pool) <= n:
        return pool
    return random.Random(SEED + seed_offset).sample(pool, n)


def main():
    if not TIERS.exists():
        partial = ROOT / "output" / f"{SLUG}-PARTIAL-screen-tiers.json"
        if partial.exists():
            print("REFUSED: only a PARTIAL screen exists. A gate built on a partial screen would "
                  "sample strata whose membership is still changing, and its overturn rates would "
                  "be computed against a denominator that does not exist yet. Finish the screen.",
                  file=sys.stderr)
            return 1
        print(f"REFUSED: {TIERS} not found", file=sys.stderr)
        return 1
    corpus = json.loads(TIERS.read_text())

    decisive = [r for r in corpus
                if r["estimand_cell"] == "DIFFUSION_INDEPENDENT_OF_STRUCTURE"
                or (r["estimand_cell"] in PRIMARY and r["outcome_level"] == "REALIZED_FERTILITY")]
    wall5_pool = [r for r in corpus if r["estimand_cell"] == "MECHANISM_UNRESOLVED_SCHOOLING"]
    title_only_pool = [r for r in corpus if not r.get("model_screened")]
    prim_school = [r for r in corpus if r["estimand_cell"] == "PRIMARY_SCHOOLING_IDEATIONAL"]

    rows, log_strata = [], []
    for r in sorted(decisive, key=lambda r: (-(r.get("year") or 0), r.get("paperId") or "")):
        rows.append(row(r, "A_DECISIVE", 1, "full_text"))
    log_strata.append(("A_DECISIVE", len(decisive), len(decisive), "census"))

    w5 = take(wall5_pool, WALL5_SAMPLE_N, 1)
    for r in w5:
        rows.append(row(r, "B_WALL5_SCHOOLING", 1, "full_text"))
    log_strata.append(("B_WALL5_SCHOOLING", len(wall5_pool), len(w5), f"seed {SEED}+1"))

    # The primary schooling cell is small and is the other half of the headline ratio, so it is a
    # census too: the ratio moves if EITHER side is misclassified, and reading only the larger side
    # would let an inflated numerator pass unchecked.
    for r in sorted(prim_school, key=lambda r: (-(r.get("year") or 0), r.get("paperId") or "")):
        rows.append(row(r, "B2_PRIMARY_SCHOOLING", 1, "full_text"))
    log_strata.append(("B2_PRIMARY_SCHOOLING", len(prim_school), len(prim_school), "census"))

    to = take(title_only_pool, TITLE_ONLY_SAMPLE_N, 2)
    for r in to:
        rows.append(row(r, "C_TITLE_ONLY", 2, "abstract_then_full_text_if_promising"))
    log_strata.append(("C_TITLE_ONLY", len(title_only_pool), len(to), f"seed {SEED}+2"))

    for i, wall in enumerate(WALLS):
        pool = [r for r in corpus if r["estimand_cell"] == wall]
        if not pool:
            continue
        s = take(pool, WALL_SAMPLE_N, 10 + i)
        for r in s:
            rows.append(row(r, f"D_WALL_{wall}", 3, "abstract"))
        log_strata.append((f"D_WALL_{wall}", len(pool), len(s), f"seed {SEED}+{10+i}"))

    GATE.parent.mkdir(parents=True, exist_ok=True)
    with GATE.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=COLUMNS)
        w.writeheader()
        w.writerows(rows)

    n_w5, n_ps = len(wall5_pool), len(prim_school)
    ratio = 100 * n_w5 / max(1, n_w5 + n_ps)
    L = [f"# Human review gate — {SLUG} (D.1.b)", "",
         f"Worksheet: `{GATE.relative_to(ROOT)}` — **{len(rows)} rows**. Built from the completed "
         f"screen over {len(corpus):,} corpus records. Sampling is deterministic; the seed and n for "
         "every sampled stratum are below, so the same draw reproduces.", "",
         "## Strata", "", "| stratum | population | drawn | rule |", "|---|---:|---:|---|"]
    for name, pop, drawn, rule in log_strata:
        L.append(f"| `{name}` | {pop:,} | {drawn:,} | {rule} |")
    L += ["", "## What this gate is for", "",
          "**Stratum B is the point of the exercise.** The A1 scope recorded, before any screening, "
          "that a title/abstract screen cannot enforce Wall 5 — whether a schooling estimate "
          "decomposes ideational content from wage returns lives in the results tables, not the "
          "abstract. The screen therefore reports "
          f"**{n_w5} unresolved against {n_ps} decomposed ({ratio:.0f}% unresolved)**, and that "
          "figure is an upper bound *by construction*, not by caution. This stratum is read at full "
          "text because that is the only place the answer exists. Whatever share of the unresolved "
          "class turns out to decompose a mechanism after all is the correction to the chapter's "
          "headline number.",
          "",
          "Stratum B2 censuses the other side of the same ratio. A ratio moves if either side is "
          "wrong, and reading only the larger side would let an inflated numerator through.",
          "",
          "**Stratum C prices the abstract-availability limit.** Those records were assigned by rule "
          "and never read. The estimable question is what share would have been primary given an "
          "abstract; that share, applied to the stratum, is what the limit cost.",
          "",
          "**Stratum D reports overturn rates by wall, not in aggregate.** The D.3.b gate overturned "
          "five of the twelve decisive records it read and the overturns clustered by wall; an "
          "aggregate rate would have hidden which wall was failing.",
          "",
          "## Columns the human fills", "",
          "`ra_verdict`, `ra_cell`, `ra_outcome_level`, `ra_route_to`, `agree_or_overturn`, "
          "`mechanism_decomposed` (stratum B and B2 only: yes / no / cannot tell), `ra_reason`, "
          "`send_to_fulltext`, `ra_initials`, `ra_date`.", "",
          "`mechanism_decomposed` is the field the whole gate turns on. Record `cannot tell` freely — "
          "a paper whose mechanism genuinely cannot be determined from full text belongs in the "
          "unresolved class, and forcing a yes/no would manufacture the precision the chapter is "
          "trying to measure honestly.", ""]
    GATE_LOG.write_text("\n".join(L) + "\n")
    print(f"gate worksheet: {len(rows)} rows -> {GATE.relative_to(ROOT)}")
    for name, pop, drawn, rule in log_strata:
        print(f"  {name:34} {drawn:4}/{pop:<6} ({rule})")
    print(f"headline ratio as screened: {n_w5} unresolved / {n_ps} decomposed = {ratio:.0f}%")
    return 0


if __name__ == "__main__":
    sys.exit(main())
