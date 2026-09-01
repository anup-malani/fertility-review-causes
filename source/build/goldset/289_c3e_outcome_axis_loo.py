#!/usr/bin/env python3
"""289 — C.3.e: leave-one-out on the OUTCOME axis. TICK-077.

278 calibrated the three exposure axes term by term and accepted the outcome axis as a block.
That gap is expensive: `parity` is in the outcome axis for birth parity, and `interest rate` is
in Arm B's exposure axis, so **"interest rate parity" satisfies both axes with a single phrase**.
Arm B's frame is 4,291 records with `parity` and 1,073 without -- 75% of the arm is a homonym,
and the arm-seeded round 3 came back as a reading list on uncovered interest parity.

An axis accepted as a block is a block of assumptions. This runs the same test the exposure axes
got: for each outcome term, what frame does it contribute, and what gold is lost without it.

Usage: python3 289_c3e_outcome_axis_loo.py
"""
import importlib.util, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
LOGS = ROOT / "literature" / "search-logs"
GOLD = ROOT / "source" / "build" / "goldset"

spec = importlib.util.spec_from_file_location("m283", GOLD / "283_c3e_boundary_hunt.py")
m = importlib.util.module_from_spec(spec)
sys.modules["m283"] = m
spec.loader.exec_module(m)
get, blk, phr = m.get, m.blk, m.phr

rep = json.loads((LOGS / "credit-constraints-query-repair.json").read_text())
OUTCOME = rep["final"]["outcome_axis"]
EXPO = rep["final"]["exposure_axes"]
ALLEXPO = [t for v in EXPO.values() for t in v]

anchors = json.loads((LOGS / "credit-constraints-cold-start-anchors.json").read_text())
ids = {a["key"]: a["top_candidate"]["oa_id"].rsplit("/", 1)[-1] for a in anchors}
role = {a["key"]: a.get("role", "anchor") for a in anchors}
gold = {k: v for k, v in ids.items() if role[k] != "decoy"}

# Candidate replacements for a term that is pulling a homonym: the demographic senses,
# which cannot be satisfied by an exchange-rate paper.
REPLACEMENTS = ["birth parity", "parity progression", "parity-specific", "higher-order birth"]


def count(f):
    d, e = get([("filter", f), ("per-page", "1"), ("select", "id")])
    return None if e else d["meta"]["count"]


def recalled(f, want):
    hit, keys = set(), list(want)
    for i in range(0, len(keys), 40):
        b = keys[i:i + 40]
        d, e = get([("filter", "openalex_id:" + "|".join(want[k] for k in b) + "," + f),
                    ("per-page", "40"), ("select", "id")])
        if e:
            raise SystemExit(e)
        got = {w["id"].rsplit("/", 1)[-1] for w in d["results"]}
        hit |= {k for k in b if want[k] in got}
    return hit


def frame(out, expo=ALLEXPO):
    return f"title_and_abstract.search:{blk(expo)} AND {blk(out)}"


base_n = count(frame(OUTCOME))
base_hit = recalled(frame(OUTCOME), gold)
print(f"BASELINE: frame {base_n}, gold {len(base_hit)}/{len(gold)}\n")
print(f"  {'outcome term':24s} {'adds':>7s} {'alone':>7s}  gold lost if dropped")
rows = []
for t in OUTCOME:
    rest = [x for x in OUTCOME if x != t]
    n2 = count(frame(rest))
    h2 = recalled(frame(rest), gold)
    alone = count(f"title_and_abstract.search:{blk(ALLEXPO)} AND {phr(t)}")
    lost = sorted(base_hit - h2)
    rows.append({"term": t, "frame_added": base_n - n2 if None not in (base_n, n2) else None,
                 "term_alone": alone, "gold_lost": lost})
    print(f"  {t:24s} {str(base_n - n2):>7s} {str(alone):>7s}  {','.join(lost) or '-'}")

print("\nreplacements for the homonym term, each tested alone:")
reps = []
for t in REPLACEMENTS:
    alone = count(f"title_and_abstract.search:{blk(ALLEXPO)} AND {phr(t)}")
    keep = [x for x in OUTCOME if x != "parity"] + [t]
    h = recalled(frame(keep), gold)
    reps.append({"term": t, "alone": alone, "gold": len(h)})
    print(f"  {t:24s} alone {str(alone):>6s}   gold with it {len(h)}/{len(gold)}")

repaired = [x for x in OUTCOME if x != "parity"]
n_rep = count(frame(repaired))
h_rep = recalled(frame(repaired), gold)
print(f"\nREPAIRED outcome axis (drop 'parity'): frame {n_rep} (was {base_n}), "
      f"gold {len(h_rep)}/{len(gold)} (was {len(base_hit)})")
print(f"  gold lost: {', '.join(sorted(base_hit - h_rep)) or 'none'}")

out = {"baseline": {"frame": base_n, "gold": len(base_hit)}, "leave_one_out": rows,
       "replacements": reps,
       "repaired": {"outcome_axis": repaired, "frame": n_rep, "gold": len(h_rep),
                    "gold_lost": sorted(base_hit - h_rep)}}
(LOGS / "credit-constraints-outcome-axis-loo.json").write_text(json.dumps(out, indent=2))
print("\nwritten: credit-constraints-outcome-axis-loo.json")
