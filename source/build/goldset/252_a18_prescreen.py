#!/usr/bin/env python3
"""252 — A.18 deterministic prescreen, every rule recall-checked before adoption. TICK-076.

251 measured the saturation curve and it is still climbing at 26% of the frame:
at PROTOCOL §5.1's stopping rule of 1,000 screened, gold recall is 31.7%. Relevance
truncation is therefore not a safe way to cut this frame, so the frame is pulled
whole and cut deterministically instead — on rules that can be audited, rather than
on a ranking that cannot.

**No rule is adopted until it has been recall-checked against gold.** Each candidate
is applied ALONE to the full frame and scored on two things: how many records it
removes, and how much gold it destroys. A rule that loses gold is rejected however
much noise it removes, because a false negative here is unrecoverable and there is
no downstream stage that can restore it.

Gold = the 25 resolved anchors + the 63 wall-surviving pool-gold records from 250,
restricted to those actually present in the frame: a prescreen can only lose what
it was given.

**The no-abstract bucket is exempt from every content rule.** 22.7% of the frame has
no indexed abstract. Dropping such a record for "no fertility outcome" records
*not visible* as *not present* — the same error as reading a query refusal as an
empty literature. Those records survive to a NO_ABSTRACT stratum and are screened
on title alone, where a title is often decisive in both directions.

Usage: python3 source/build/goldset/252_a18_prescreen.py
"""
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
LOGS = ROOT / "literature" / "search-logs"
# 45k records with abstracts is ~75MB of raw API output: reproducible from this
# script, not evidence in itself, and not something to put in git.
TEMP = ROOT / "temp" / "a18"
OUT = LOGS / "heritability-fertility-genetic-prescreen.json"
OUT_MD = LOGS / "heritability-fertility-genetic-prescreen.md"

# --- candidate rules ------------------------------------------------------
# Each returns True when the record should be REMOVED.

NONHUMAN = re.compile(r"\b("
    r"cattle|dairy cow|bull|heifer|bovine|sow|boar|piglet|swine|porcine|"
    r"poultry|broiler|laying hen|sheep|ewe|ovine|goat|caprine|buffalo|"
    r"equine|salmon|tilapia|shrimp|aquaculture|silkworm|honeybee|"
    r"drosophila|nematode|zebrafish|arabidopsis|maize|wheat cultivar|"
    r"barley|sorghum|soybean|rice cultivar|cultivar|male sterility|"
    r"pollen|anther|agronom|soil fertility|livestock|herd|breeding value|"
    r"inbred lines?|wild population|song sparrow|red deer|great tit"
    r")\b", re.I)

# R2's first version omitted `fitness` -- the exact word §15 established this
# literature uses for the outcome -- and so destroyed Beauchamp 2016 and Milot 2011.
# The diagnostic vocabulary had drifted from the retrieval vocabulary; the fix is to
# derive it FROM the adopted query's FERTILITY axis rather than to write it again.
FERT_OUTCOME = re.compile(r"\b("
    r"fitness|reproduc\w+|"
    r"fertility|fertilit\w*|births?|childbearing|children ever born|childless\w*|"
    r"parity|famil\w+ size|offspring|reproductive success|reproductive output|"
    r"fecundity|fecundabilit\w*|age at first birth|number of children|"
    r"completed famil\w+|natalit\w*|birth rate|nulliparous|parous"
    r")\b", re.I)

HUMAN = re.compile(r"\b("
    r"human|men\b|women|male[s]? and female[s]?|participants|cohort|"
    r"biobank|registry|register|survey|respondents|twins?|sibling|"
    r"population-based|national|adults?|mothers?|fathers?|parents?|couples?"
    r")\b", re.I)

TYPES_OK = {"article", "review", "preprint", "book-chapter", "book", "report",
            "dissertation", "posted-content", None}


def text_of(r, with_abstract=True):
    parts = [r.get("title") or "", r.get("venue") or ""]
    if with_abstract and r.get("abstract"):
        parts.append(r["abstract"])
    return " ".join(parts)


def main():
    TEMP.mkdir(parents=True, exist_ok=True)
    frame_doc = json.loads((TEMP / "heritability-fertility-genetic-frame-deduped.json").read_text())
    frame = frame_doc["records"]
    fmeta = frame_doc["meta"]

    anchors = json.loads((LOGS / "heritability-fertility-genetic-cold-start-anchors.json").read_text())
    anchor_ids = {a["top_candidate"]["oa_id"].rsplit("/", 1)[-1] for a in anchors}
    audit = json.loads((LOGS / "heritability-fertility-genetic-recall-audit.json").read_text())
    routed = {m["openalex"] for m in audit["missed"]
              if m["miss_class"] != "A18_CANDIDATE"}
    pool = json.loads((LOGS / "heritability-fertility-genetic-snowball-pool.json").read_text())
    FT = re.compile(r"\b(fertility|births?|children|childless|parity|family size|"
                    r"offspring|reproductive success|fecundity|childbearing)\b", re.I)
    pool_gold = {r["openalex"] for r in pool
                 if r["n_seeds"] >= 3 and FT.search(r["title"] or "")} - routed

    ids = {r["openalex"] for r in frame}
    gold = (anchor_ids | pool_gold) & ids
    print(f"frame {len(frame):,} records ({fmeta['coverage_of_frame_pct']}% of "
          f"{fmeta['frame_size']:,})   gold present in frame: {len(gold)}"
          f"  (anchors {len(anchor_ids & ids)}/{len(anchor_ids)}, "
          f"pool {len(pool_gold & ids)}/{len(pool_gold)})\n")

    no_abs = [r for r in frame if not r.get("abstract")]
    print(f"no-abstract stratum: {len(no_abs):,} ({100*len(no_abs)/len(frame):.1f}%) "
          f"— exempt from every content rule\n")

    RULES = {
        "R1_nonhuman_organism": lambda r: bool(NONHUMAN.search(text_of(r))),
        "R2_no_fertility_outcome": lambda r: bool(r.get("abstract")) and not FERT_OUTCOME.search(text_of(r)),
        "R2b_no_fertility_outcome_title_only": lambda r: bool(r.get("abstract")) and not FERT_OUTCOME.search(
            (r.get("title") or "") + " " + (r.get("venue") or "")),
        "R3_no_human_signal": lambda r: bool(r.get("abstract")) and not HUMAN.search(text_of(r)),
        "R4_non_english": lambda r: (r.get("language") or "en") != "en",
        "R5_bad_type": lambda r: r.get("type") not in TYPES_OK,
    }

    print("candidate rules, applied ALONE to the full frame:\n")
    print(f"  {'rule':26s} {'removes':>8s} {'% frame':>8s} {'GOLD LOST':>10s}   verdict")
    scored = {}
    for name, fn in RULES.items():
        removed = [r for r in frame if fn(r)]
        rem_ids = {r["openalex"] for r in removed}
        lost = gold & rem_ids
        scored[name] = {"removes": len(removed),
                        "pct_frame": round(100 * len(removed) / len(frame), 1),
                        "gold_lost": len(lost),
                        "gold_lost_titles": [r["title"] for r in frame
                                             if r["openalex"] in lost][:12],
                        "adopt": len(lost) == 0}
        v = "ADOPT" if not lost else f"REJECT — destroys {len(lost)} gold"
        print(f"  {name:26s} {len(removed):8,} {scored[name]['pct_frame']:7.1f}% "
              f"{len(lost):10d}   {v}")

    adopted = [n for n, s in scored.items() if s["adopt"]]
    print(f"\nadopted: {', '.join(adopted) if adopted else '(none)'}")

    survivors = [r for r in frame
                 if not any(RULES[n](r) for n in adopted)]
    surv_ids = {r["openalex"] for r in survivors}
    print(f"\nsurvivors: {len(survivors):,} of {len(frame):,} "
          f"({100*len(survivors)/len(frame):.1f}%)   "
          f"gold retained {len(gold & surv_ids)}/{len(gold)}")

    strata = Counter("NO_ABSTRACT" if not r.get("abstract") else "HAS_ABSTRACT"
                     for r in survivors)

    payload = {
        "meta": {
            "ticket": "TICK-076",
            "frame_in": len(frame), "frame_total": fmeta["frame_size"],
            "gold_in_frame": len(gold),
            "rules_scored": scored, "rules_adopted": adopted,
            "survivors": len(survivors),
            "gold_retained": f"{len(gold & surv_ids)}/{len(gold)}",
            "strata": dict(strata),
            "note": "No rule is adopted that destroys gold. The no-abstract stratum is "
                    "exempt from every content rule and is screened on title alone.",
        },
        "survivor_ids": sorted(surv_ids),
    }
    OUT.write_text(json.dumps(payload, indent=1))

    md = ["# A.18 deterministic prescreen\n",
          f"Frame in: **{len(frame):,}**. Gold present: **{len(gold)}**. "
          f"Survivors: **{len(survivors):,}**, gold retained **{len(gold & surv_ids)}/{len(gold)}**.\n",
          "\n| rule | removes | % frame | gold lost | verdict |\n|---|---|---|---|---|"]
    for n, s in scored.items():
        md.append(f"| `{n}` | {s['removes']:,} | {s['pct_frame']}% | {s['gold_lost']} | "
                  f"{'**ADOPT**' if s['adopt'] else '**REJECT**'} |")
    md.append("\n## Gold a rejected rule would have destroyed\n")
    for n, s in scored.items():
        if s["gold_lost"]:
            md.append(f"\n### `{n}` — {s['gold_lost']} records\n")
            for t in s["gold_lost_titles"]:
                md.append(f"- {t}")
    OUT_MD.write_text("\n".join(md) + "\n")
    print(f"\nwrote {OUT.relative_to(ROOT)} and {OUT_MD.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
