#!/usr/bin/env python3
"""349 — build the C.3.d anchor candidate list: programmatic controls + the hand Tier-A canon.

Port of C.2.f's `339_c2f_anchor_candidates.py`. The list has two halves and they are scored
separately, because without the split a run of NO_RESULTS is uninterpretable
(`validate-a-null-detector-on-positives`):

  `control` — titles, years and DOIs taken PROGRAMMATICALLY out of 348's free-seed harvest. Never
      retyped: `never-hand-type-a-record-id` (8 of 8 reconstructed OpenAlex ids were wrong on an
      earlier chapter, and only ingest validation caught it). These records demonstrably exist, so a
      failure on one is a broken RESOLVER.
  `hand` — the Tier-A canon, written from knowledge of the literature. A failure on one of these may
      be a GHOST CITATION, which is a finding about the canon rather than about the code.

Controls are stratified over the free-seed terms rather than taken off the top of the list, so every
term is actually exercised and a term whose records all fail is visible. A citation-sorted or
file-order head is not the population (`citation-sorted-head-is-not-the-population`).

`direction` is carried on every candidate and is not decoration. Scope §2 rules that the FORWARD arm
(return → fertility) is C.3.d's primary cell and the BACKWARD arm (family size → child outcomes) is
mechanism evidence on link 2, never pooled. The canon below is deliberately split across both, so
resolving it and then reading that column is a direct test of §2 on the canon rather than on record
counts — the same role `outcome_is_fertility` played for C.2.f.

Output: literature/search-logs/quantity-quality-tradeoff-anchor-candidates.json
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
LOGS = ROOT / "literature" / "search-logs"
SEEDS = LOGS / "quantity-quality-tradeoff-free-seeds.json"
OUT = LOGS / "quantity-quality-tradeoff-anchor-candidates.json"

PER_TERM = 6   # controls per free-seed term

# --------------------------------------------------------------------------- the hand Tier-A canon
# `direction` follows scope §2. `outcome_is_fertility` is the direct test: a THEORY or BACKWARD
# anchor does not have fertility as its dependent variable, and the registry cites BACKWARD work as
# evidence about C.3.d.
HAND = [
    # ---- theory: the models the registry names as seminal
    dict(title="An Economic Analysis of Fertility", year=1960, first_author="Gary Becker",
         arm="theory", direction="THEORY", outcome_is_fertility=True),
    dict(title="On the Interaction between the Quantity and Quality of Children", year=1973,
         first_author="Gary Becker", arm="theory", direction="THEORY", outcome_is_fertility=True),
    dict(title="Child Endowments and the Quantity and Quality of Children", year=1976,
         first_author="Gary Becker", arm="theory", direction="THEORY", outcome_is_fertility=True),
    dict(title="Human Capital, Fertility, and Economic Growth", year=1990,
         first_author="Gary Becker", arm="theory", direction="THEORY", outcome_is_fertility=True),
    dict(title="Population, Technology, and Growth: From Malthusian Stagnation to the Demographic "
               "Transition and Beyond", year=2000, first_author="Oded Galor",
         arm="theory", direction="THEORY", outcome_is_fertility=True),
    dict(title="Natural Selection and the Origin of Economic Growth", year=2002,
         first_author="Oded Galor", arm="theory", direction="THEORY", outcome_is_fertility=True),
    dict(title="Accounting for Fertility Decline during the Transition to Growth", year=2004,
         first_author="Matthias Doepke", arm="theory", direction="THEORY", outcome_is_fertility=True),
    dict(title="The Baby Boom and Baby Bust", year=2005, first_author="Jeremy Greenwood",
         arm="theory", direction="THEORY", outcome_is_fertility=True),

    # ---- backward: family size as the exposure, child outcomes as the dependent variable.
    # This is the arm the registry cites as evidence about C.3.d and scope §2 rules is link 2.
    dict(title="Testing the Quantity-Quality Fertility Model: The Use of Twins as a Natural "
               "Experiment", year=1980, first_author="Mark Rosenzweig",
         arm="backward", direction="BACKWARD", outcome_is_fertility=False),
    dict(title="The More the Merrier? The Effect of Family Size and Birth Order on Children's "
               "Education", year=2005, first_author="Sandra Black",
         arm="backward", direction="BACKWARD", outcome_is_fertility=False),
    dict(title="The Impacts of Family Size on Investment in Child Quality", year=2006,
         first_author="Julio Caceres-Delpiano", arm="backward", direction="BACKWARD",
         outcome_is_fertility=False),
    dict(title="The Quantity-Quality Trade-off of Children in a Developing Country: Identification "
               "Using Chinese Twins", year=2008, first_author="Hongbin Li",
         arm="backward", direction="BACKWARD", outcome_is_fertility=False),
    dict(title="Multiple Experiments for the Causal Link between the Quantity and Quality of "
               "Children", year=2010, first_author="Joshua Angrist",
         arm="backward", direction="BACKWARD", outcome_is_fertility=False),

    # ---- forward: a shock to the return, fertility as the dependent variable. Scope §7 rows 1-6.
    # This is the registered estimand and the arm §3 measures at 16 records inside the frame.
    dict(title="Chronic Disease Burden and the Interaction of Education, Fertility, and Growth",
         year=2009, first_author="Hoyt Bleakley", arm="forward", direction="FORWARD",
         outcome_is_fertility=True),
    dict(title="Fertility Transitions Along the Extensive and Intensive Margins", year=2014,
         first_author="Daniel Aaronson", arm="forward", direction="FORWARD",
         outcome_is_fertility=True),
    dict(title="Human capital and the quantity-quality trade-off during the demographic "
               "transition", year=2017, first_author="Alan Fernihough",
         arm="forward", direction="FORWARD", outcome_is_fertility=True),
    dict(title="Fecundity, Fertility and the Formation of Human Capital", year=2019,
         first_author="Marc Klemp", arm="forward", direction="FORWARD",
         outcome_is_fertility=True),
]


def main():
    seeds = json.loads(SEEDS.read_text())
    recs = seeds["records"]
    terms = list(seeds["per_term"].keys())

    # Stratify controls over the free-seed terms. Prefer records a term caught ALONE, so the control
    # set exercises each term rather than re-testing whatever the broadest term also matched.
    controls, taken = [], set()
    for term in terms:
        pool = [r for r in recs if term in r["matched"] and r["id"].startswith("10.") and r["year"]]
        pool.sort(key=lambda r: (len(r["matched"]), -int(r["year"] or 0)))   # term-alone first
        n = 0
        for r in pool:
            key = r["id"].lower()
            if key in taken:
                continue
            taken.add(key)
            controls.append(dict(
                title=r["title"], year=int(r["year"]), doi=r["id"],
                first_author="", source="control", arm=f"seed:{term}",
                direction="BACKWARD" if r["backward"] else "UNKNOWN",
                outcome_is_fertility=None, seed_terms=r["matched"],
                seed_flags={k: r[k] for k in ("backward", "wall_c2e", "wall_a12", "evo", "theory")}))
            n += 1
            if n >= PER_TERM:
                break

    hand = []
    for h in HAND:
        hand.append(dict(h, source="hand", doi="", openalex="",
                         seed_terms=[], seed_flags={}))

    out = controls + hand
    OUT.write_text(json.dumps(out, indent=2) + "\n")

    print(f"{len(controls)} controls (<= {PER_TERM} per free-seed term, DOI-bearing, taken "
          f"programmatically) + {len(hand)} hand anchors = {len(out)}")
    print("\ncontrols per term:")
    for term in terms:
        n = sum(1 for c in controls if c["arm"] == f"seed:{term}")
        flag = "" if n == PER_TERM else f"   <- fewer than {PER_TERM} DOI-bearing records exist"
        print(f"  {term:26} {n}{flag}")
    print("\nhand anchors per direction:")
    for d in ("THEORY", "BACKWARD", "FORWARD"):
        rows = [h for h in hand if h["direction"] == d]
        print(f"  {d:9} {len(rows)}")
    print(f"\nwritten: {OUT}")


main()
