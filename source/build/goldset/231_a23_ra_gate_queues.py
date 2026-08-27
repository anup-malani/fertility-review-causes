#!/usr/bin/env python3
"""
231 — A.23 RA gate, step 3: the retrieval queue and the Wall 1 packet.

TICK-075. Turns the screened frame into the two things the next stages actually need.

  1. RETRIEVAL QUEUE, priority-ordered. Full-text retrieval is the chapter's known
     bottleneck -- B.1 stalled at 20 of 95 PDFs and its pooled estimate still rests on
     five studies. So the queue is ordered by what the SYNTHESIS needs rather than by
     what is easy to fetch, and every tier is labelled with why it is there. The
     standing lesson is that a retrieval rate hides WHICH records were retrieved:
     tier composition is reported so a shortfall can be read against the cells rather
     than as one percentage.

  2. THE WALL 1 SECOND-READ PACKET. The 26 MIXED_PRICE_ARRANGEMENT records are not an
     RA routing decision. They are the open ruling: a subsidy or price change aimed at
     the arrangement is both C.2.c's treatment and A.23's target, and this cell now
     holds most of the identified evidence bearing on the registered claim. The packet
     is assembled as its own artefact so the second read can be done on evidence.

Usage: python3 source/build/goldset/231_a23_ra_gate_queues.py
"""
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
LOGS = ROOT / "literature" / "search-logs"
SCREENED = LOGS / "co-residence-parents-household-delay-screened.json"
QUEUE = LOGS / "co-residence-parents-household-delay-retrieval-queue.json"
PACKET = LOGS / "co-residence-parents-household-delay-wall1-packet.md"

PRIMARY = {"PRIMARY_PRELAUNCH", "PRIMARY_EXTENDED_COUPLE", "PRIMARY_PROXIMITY"}
LINK1 = {"LINK1_DRIVER_TO_ARRANGEMENT", "LINK1_ARRANGEMENT_TO_UNION"}


def tier(r):
    rt, vd, dg = r["route"], r["verdict"], r["design"]
    if rt == "MIXED_PRICE_ARRANGEMENT":
        return "T1_wall1_packet"
    if rt in PRIMARY and dg == "identified":
        return "T1_primary_identified"
    if rt in PRIMARY and vd == "RELEVANT":
        return "T2_primary_relevant"
    if rt in PRIMARY:
        return "T3_primary_uncertain"
    if rt in LINK1 and dg == "identified":
        return "T3_link1_identified"
    if rt == "INSUFFICIENT_INFO":
        return "T4_insufficient_resolve_at_retrieval"
    if rt in LINK1:
        return "T5_link1"
    if rt == "THEORY":
        return "T6_theory_stream"
    return "T7_not_queued"


WHY = {
    "T1_wall1_packet": "The open Wall 1 ruling. Holds most of the identified evidence "
                       "bearing on the registered claim; nothing downstream can be settled "
                       "before these are read.",
    "T1_primary_identified": "Identified designs inside a primary cell. These carry the "
                             "GRADE rating for their arm.",
    "T2_primary_relevant": "Primary-cell records the screen kept outright. The pooled or "
                           "narrative core of each arm.",
    "T3_primary_uncertain": "Primary-cell records the screen could not confirm. Their "
                            "routing is decided at full text, and the CELL BALANCE depends "
                            "on how they resolve.",
    "T3_link1_identified": "Identified designs on link 1. They cannot carry a fertility "
                           "verdict but they are the chapter's only leverage on whether the "
                           "arrangement responds to anything exogenous.",
    "T4_insufficient_resolve_at_retrieval": "Not routable on the visible record. Retrieval "
                                            "IS the screen for these.",
    "T5_link1": "Mechanism evidence for link 1. Retrieve after the primary cells.",
    "T6_theory_stream": "Theory and framing. Read, do not pool.",
    "T7_not_queued": "Routed out. Not retrieved.",
}


def main():
    doc = json.loads(SCREENED.read_text())
    recs = doc["records"]
    for r in recs:
        r["retrieval_tier"] = tier(r)

    counts = Counter(r["retrieval_tier"] for r in recs)
    queued = [r for r in recs if r["retrieval_tier"] != "T7_not_queued"]

    def slim(r):
        return {k: r[k] for k in ("openalex", "doi", "title", "year", "venue", "type",
                                  "verdict", "route", "config", "design",
                                  "anticipation_flag", "retrieval_tier", "note")}

    order = ["T1_wall1_packet", "T1_primary_identified", "T2_primary_relevant",
             "T3_primary_uncertain", "T3_link1_identified",
             "T4_insufficient_resolve_at_retrieval", "T5_link1", "T6_theory_stream"]
    queued.sort(key=lambda r: (order.index(r["retrieval_tier"]), -(r["year"] or 0)))

    cells_in_queue = Counter(r["route"] for r in queued if r["route"] in PRIMARY
                             or r["route"] == "MIXED_PRICE_ARRANGEMENT")
    no_doi = sum(1 for r in queued if not r["doi"])

    meta = {
        "ticket": "TICK-075", "stage": "RA gate step 3",
        "frame": len(recs), "queued": len(queued),
        "tiers": {k: counts.get(k, 0) for k in order},
        "tier_rationale": WHY,
        "primary_cells_in_queue": dict(cells_in_queue),
        "queued_without_a_doi": no_doi,
        "retrieval_warning": "Report retrieval as a CROSS-TAB of tier by outcome, never as "
                             "one percentage. A 70% rate that misses the identified designs "
                             "is worse than a 40% rate that gets them.",
    }
    QUEUE.write_text(json.dumps({"meta": meta, "queue": [slim(r) for r in queued]}, indent=1))
    SCREENED.write_text(json.dumps(doc, indent=1))

    # --- Wall 1 packet -----------------------------------------------------
    w1 = [r for r in recs if r["route"] == "MIXED_PRICE_ARRANGEMENT"]
    w1.sort(key=lambda r: (r["design"] != "identified", -(r["year"] or 0)))
    lines = [
        "# Wall 1 second-read packet — A.23 × C.2.c",
        "",
        "**Ticket:** TICK-075 · **Assembled:** 2026-08-27 from the completed screen "
        "(`231_a23_ra_gate_queues.py`)",
        "",
        "## Why this packet exists",
        "",
        "The scope's Wall 1 inherited C.2.c's ruling — price variation is C.2.c's, the living",
        "arrangement is A.23's — and added a sub-ruling for the case where a policy changes a",
        "price *in order to* change the arrangement. That sub-ruling was written before any",
        "such record had been found. The screen found **26**, and they now hold most of the",
        "identified evidence bearing on the registered claim.",
        "",
        "So this is no longer a boundary tidy-up. **How Wall 1 is read decides whether A.23 has",
        "an identified core at all**, and whether that core is A.23's, C.2.c's, or shared.",
        "",
        "## The three positions available",
        "",
        "1. **Strict inheritance.** Price variation is C.2.c's, full stop. A.23 keeps the",
        "   observational arrangement literature and reports that its registered claim has",
        "   almost no identified evidence. Honest, and it makes the chapter thin by",
        "   construction rather than by finding.",
        "2. **Target-based.** A policy whose TARGET is the arrangement is A.23's, whatever",
        "   instrument it uses. Gives A.23 an identified core and obliges C.2.c to hand back",
        "   records it may already have claimed.",
        "3. **Shared and non-additive** (the current sub-ruling). Both chapters report these",
        "   records, neither claims the magnitude alone, and the demographic-significance",
        "   sections say so explicitly. Consistent with the non-additivity §2 already inherited,",
        "   and the only option that does not require one chapter to lose evidence it has read.",
        "",
        "## The records",
        "",
    ]
    for r in w1:
        flag = " **[IDENTIFIED]**" if r["design"] == "identified" else ""
        lines += [f"### {r['title']}{flag}",
                  f"*{r['venue'] or 'n/a'}*, {r['year'] or 'n.d.'} · `{r['doi'] or 'no DOI'}` · "
                  f"verdict {r['verdict']}, config {r['config']}",
                  "", (r["note"] or "").strip(), ""]
    lines += [
        "## What the packet cannot settle",
        "",
        "None of these records was selected to test the wall; they were selected because they",
        "estimate something. Reading them will show how the two variables behave together —",
        "several put tenure and the arrangement in one choice set, and one instruments a price",
        "shock while estimating homeownership, household formation and fertility jointly, which",
        "is the closest thing available to a decomposition. It will not tell the review which",
        "chapter *should* own them. That remains a judgement about what the two hypotheses are",
        "for, and it is the PI's.",
    ]
    PACKET.write_text("\n".join(lines))

    print(json.dumps({k: meta[k] for k in
                      ("queued", "tiers", "primary_cells_in_queue", "queued_without_a_doi")},
                     indent=1))
    print(f"\nWall 1 packet: {len(w1)} records, "
          f"{sum(1 for r in w1 if r['design'] == 'identified')} identified")
    print(f"wrote {QUEUE.relative_to(ROOT)} and {PACKET.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
