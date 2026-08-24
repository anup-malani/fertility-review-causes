#!/usr/bin/env python3
"""
175_a24_make_screen_batches.py — A.24, stage D2. Prepare the semantic screen.

Inherits `164_a12_make_screen_batches.py`. Writes the screening rubric and cuts the D1 worklist into
fixed batches carrying only what a title/abstract screen is entitled to see: title, venue, year,
type, and a truncated abstract.

WITHHELD FROM THE SCREENING RECORD, deliberately:
  * the D1 score and rank, and the discovery channel — a screener who can see the blind sieve's
    output anchors on it, which collapses two independent sieves into one;
  * the `worklist_reason`. Records are in this worklist only because a bypass put them there, and a
    screener told "this came through the Wall 9 bypass" would read a technology-diffusion design into
    abstracts that say no such thing. The bypass is a retrieval decision; whether the record actually
    carries the design is what the screen is being asked;
  * D1's `union_hits`, `fert_hits`, `sexhealth_hits` and `platform_hits`, so the screener's
    `outcome_type` is an INDEPENDENT reading. See below.

`outcome_type` IS THE POINT OF THIS SCREEN, AND FOR TWO SEPARATE REASONS.

FIRST, IT MEASURES THE CHAPTER'S CENTRAL CLAIM. A.24 asserts a three-link chain and the scope found
the last link unestimated. A4 measured the shape of that gap in vocabulary — 25.6% of records in the
empirical clouds carry a union construct against 9.5% carrying a fertility quantity — but vocabulary
is not an outcome. Having the screener name the actual outcome of each record turns "the literature
reaches partnership and stops short of births" from a term-frequency observation into a count of
studies. `union_formation` and `fertility_quantity` are therefore SEPARATE values and must never be
merged into one "demographic outcome" bucket.

SECOND, IT CARRIES WALLS 4 AND 5, WHICH D1 WAS FORBIDDEN TO ENFORCE. Both are cut on OUTCOME rather
than on venue or treatment: a platform study reporting MATCHING outcomes is in (Jung et al. 2021, a
randomized field experiment) and one reporting engagement or algorithm quality is out; a dating-app
study reporting partnership is in and one reporting STI risk is out. D1 penalised both clouds only
MILDLY and on purpose — A4 measured them at 21% and 43% app vocabulary, so they share this chapter's
exposure axis heavily and a heavy term penalty would have demoted real records. The whole weight of
Walls 4 and 5 rests here, and assembly cross-checks the screener's independent reading against D1's
term-hits: agreement means the walls are enforceable at title/abstract as the scope claims,
disagreement IS their working set.

THE REVERSE-DIRECTION CELL IS NEW AND IT EXISTS BECAUSE D1 FOUND ONE. The empty cell's candidate pool
is eight records in a frame of 10,739, and one of them — "Wanting or having children predicts age
preferences in online dating" — runs the causal arrow backwards. A screener without a home for that
shape will either force it into `PRIMARY_APP_FERTILITY`, inflating a cell whose emptiness is the
chapter's headline, or discard it, losing the reverse-causality evidence the risk-of-bias stage
needs. It gets its own cell.

Output: source/build/goldset/a24_screen_batches/batch_NN.json
        literature/search-logs/{slug}-screen-rubric.md
"""
import json, os

SLUG = "dating-apps-union-formation-friction"
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
LOGS = os.path.join(ROOT, "literature", "search-logs")
WORK = os.path.join(LOGS, f"{SLUG}-screen-worklist.json")
BATCH_DIR = os.path.join(HERE, "a24_screen_batches")
OUT_RUBRIC = os.path.join(LOGS, f"{SLUG}-screen-rubric.md")

BATCH_SIZE = 60
ABSTRACT_WORDS = 70

CELLS = [
    ("PRIMARY_APP_FERTILITY",
     "Dating-app or online-dating exposure -> a FERTILITY quantity (births, TFR, completed fertility, "
     "number of children, childlessness, transition to parenthood). The cell the registry entry is "
     "about. The recon probe found no study that estimates it and A3 could not anchor it, so this "
     "cell's emptiness is a finding — which is exactly why it must not be padded. Requires the arrow "
     "to run app -> fertility."),
    ("PRIMARY_APP_UNION",
     "Dating-app or online-dating exposure -> UNION FORMATION or its quality: meeting, partnering, "
     "cohabitation, marriage, relationship stability or dissolution. The chapter's reachable spine "
     "and its causal recall denominator."),
    ("SECONDARY_TECH_UNION",
     "A TECHNOLOGY-DIFFUSION exposure (broadband, 3G, smartphone, cellular, internet access) -> a "
     "union-formation outcome. Wall 9: these abstracts will NOT say 'dating app'. Route here rather "
     "than rejecting for lacking app vocabulary."),
    ("SECONDARY_TECH_FERTILITY",
     "The same technology exposures -> a fertility quantity. Overlaps C.2.h; PI Call 2 governs which "
     "chapter may claim the magnitude, and this screen only routes."),
    ("MECHANISM_CHOICE_FRICTION",
     "Choice overload, rejection mind-set, strategic delay, commodification, gamification, swipe "
     "fatigue — with a PSYCHOLOGICAL or BEHAVIOURAL outcome (satisfaction, regret, commitment "
     "intention, fear of being single, rejection rate) rather than a demographic one. RELEVANT: it "
     "carries the mechanism section. Earns NO causal recall credit."),
    ("REVERSE_DIRECTION",
     "The arrow runs the other way: fertility desires, parental status or family intentions predict "
     "dating behaviour or partner preferences. RELEVANT and load-bearing for risk of bias — this is "
     "the reverse-causality evidence — but it is NOT evidence that apps affect fertility and must "
     "never be routed to `PRIMARY_APP_FERTILITY`."),
    ("EXPOSURE_SERIES",
     "How common app use is and how that has changed: adoption prevalence, share of couples meeting "
     "online, platform user counts, HCMST-type series. RELEVANT and load-bearing for stage 10; "
     "estimates no effect and earns NO causal recall credit."),
    ("ROUTE_C7A",
     "Marriage-market structure and assortative mating with no technology-created friction: sex "
     "ratios, education gaps, homogamy, search-and-matching theory. C.7.a's."),
    ("ROUTE_LINK3",
     "Union formation -> births, with NO technology exposure anywhere. A.7 / C.7.a own this link; "
     "A.24 imports it at synthesis and does not grade it."),
    ("ROUTE_C2H",
     "Technology -> time, attention or leisure allocation with NO partnering channel: screen time, "
     "social-media use, gaming, digital wellbeing. C.2.h's."),
    ("ROUTE_A14",
     "Coital FREQUENCY or sexual activity levels as the outcome. A.14's, and routed rather than "
     "dropped into the sexual-health bin — frequency is a proximate determinant of fertility and the "
     "sexual-health wall is about STI and risk outcomes, not about how often people have sex."),
    ("OFF_SEXHEALTH",
     "A dating-platform study whose OUTCOME is sexual health or risk: HIV, STI, PrEP, condom use, "
     "testing uptake. Wall 5. The exposure is often identical to an included record — 43% of this "
     "cloud carries app vocabulary — so only the outcome separates them."),
    ("OFF_PLATFORM_ENG",
     "A platform study whose OUTCOME is engagement, click-through, algorithm or recommender quality, "
     "or interface design. Wall 4. A platform study reporting MATCHING or partnership outcomes is "
     "NOT this — it is `PRIMARY_APP_UNION` or `MECHANISM_CHOICE_FRICTION`."),
    ("OFF_VIOLENCE",
     "Dating violence, intimate-partner violence, abuse, harassment, coercion, romance scams. Wall "
     "3. The same word sense as this chapter — courtship — and a different outcome, so no vocabulary "
     "test does this and only the outcome does."),
    ("OFF_HOMONYM_GEOCHRON",
     "'Dating' as a laboratory method: radiocarbon, luminescence, geochronology. Wall 1. Measured at "
     "0.0% on-outcome over the entire cloud, and D1 put none in its top 800 — so a record of this "
     "kind appearing here is a signal something upstream went wrong. Say so in a note."),
    ("OFF_NONHUMAN",
     "Agronomic or veterinary 'fertility': soil, crops, livestock. Wall 2. Measured at 0.1% "
     "on-outcome on a human-anchored vocabulary."),
    ("OFF_OTHER",
     "No A.24 content and no sibling-hypothesis home."),
    ("INSUFFICIENT_INFO",
     "Cannot be routed on the visible record. Pairs only with UNCERTAIN."),
]

OUTCOME_TYPES = [
    ("union_formation", "Meeting, partnering, cohabitation, marriage, relationship stability, dissolution, singlehood."),
    ("fertility_quantity", "Births, TFR, completed fertility, number of children, childlessness, transition to parenthood, fertility intentions."),
    ("both_union_and_fertility", "The record reports BOTH a partnership outcome and a fertility quantity. Expected to be rare; the count is the chapter's central number."),
    ("psychological_state", "Satisfaction, regret, self-esteem, anxiety, commitment intention, fear of being single, rejection rate."),
    ("mate_preference", "Stated or revealed preferences over partner attributes; desirability, sorting, homogamy."),
    ("sexual_behaviour", "Coital frequency, casual sex, number of partners — behaviour, not health."),
    ("sexual_health", "HIV, STI, PrEP, condom use, testing."),
    ("violence_or_abuse", "Victimisation, perpetration, harassment, coercion, scams."),
    ("platform_engagement", "Usage, engagement, matching efficiency, algorithm or recommender quality, interface design."),
    ("other", "None of the above."),
    ("unclear", "The abstract does not state an outcome."),
]


def main():
    work = json.load(open(WORK))
    os.makedirs(BATCH_DIR, exist_ok=True)
    for f in os.listdir(BATCH_DIR):
        if f.startswith("batch_"):
            os.remove(os.path.join(BATCH_DIR, f))

    n = 0
    for i in range(0, len(work), BATCH_SIZE):
        chunk = work[i:i + BATCH_SIZE]
        recs = []
        for r in chunk:
            abs_ = " ".join((r.get("abstract") or "").split()[:ABSTRACT_WORDS])
            recs.append({"id": r["id"], "year": r.get("year"), "venue": (r.get("venue") or "")[:44],
                         "type": r.get("type"), "title": r["title"], "abstract": abs_})
        n += 1
        json.dump({"batch": n, "n": len(recs), "records": recs},
                  open(os.path.join(BATCH_DIR, f"batch_{n:02d}.json"), "w"), indent=1)

    n_abs = sum(1 for r in work if r.get("abstract"))
    L = [f"# Screening rubric — {SLUG} (A.24)", "",
         "Title/abstract screen over the D1 worklist. The screener sees title, venue, year, type and "
         "a truncated abstract, and does NOT see the D1 score or rank, the discovery channel, the "
         "`worklist_reason`, or D1's term-hit lists.", "",
         "## What the screen decides", "",
         "For each record emit `{id, verdict, cell, outcome_type, note?}` where `verdict` is "
         "`RELEVANT` / `UNCERTAIN` / `NOT_RELEVANT`, `cell` is one of the cells below, and "
         "`outcome_type` is one of the outcome types below.", "",
         "## Standing instructions, each tied to something measured", "",
         "**Do NOT enforce Wall 9 — it is declared unenforceable.** The only identified estimates "
         "this chapter can reach are published under technology-diffusion vocabulary and none of "
         "them says 'dating app' anywhere a screener can see. A4 measured it: of 277 records "
         "reachable from a technology-diffusion seed, **7 carry app vocabulary at all (2.5%)**. A "
         "broadband-and-marriage-rates paper is `SECONDARY_TECH_UNION`, not `OFF_OTHER`. Rejecting a "
         "record for lacking app vocabulary is the single most damaging error available in this "
         "screen.", "",
         "**The sign is not given by the theory, and a contrary finding is still evidence.** v5 "
         "asserts apps REDUCE conversion to partnership. The best-identified evidence found so far "
         "runs the other way — Rosenfeld 2017 finds meeting online predicts FASTER transitions to "
         "marriage; Billari et al. 2019 and Kalabikhina et al. 2020 find POSITIVE broadband effects "
         "on fertility. A record finding that apps help is `PRIMARY_APP_UNION`, exactly like one "
         "finding that they hurt. Screening on the hypothesis's expected direction would manufacture "
         "the result.", "",
         "**Watch the direction of the arrow.** `REVERSE_DIRECTION` exists because the empty cell's "
         "eight-record candidate pool contains one — fertility intentions predicting dating "
         "preferences. That is evidence about reverse causality and it belongs in risk of bias. It "
         "is NOT evidence that apps affect fertility, and routing it to `PRIMARY_APP_FERTILITY` "
         "would pad the one cell whose emptiness is this chapter's headline.", "",
         "**Separate the two outcome limbs on every record.** `union_formation` and "
         "`fertility_quantity` are distinct values and `both_union_and_fertility` is a third. The "
         "chapter's central claim is that the evidence base reaches partnership and stops short of "
         "births; A4 measured the vocabulary gap at 25.6% against 9.5%, and this screen is what "
         "turns that into a count of studies. Never merge them into one demographic bucket.", "",
         "**Walls 4 and 5 are cut on OUTCOME and D1 was forbidden to enforce them.** A4 measured "
         "those clouds at 21% and 43% app vocabulary — they share this chapter's exposure axis "
         "heavily, so D1 penalised them only mildly and the whole weight rests here. A platform "
         "study reporting MATCHING outcomes is IN; one reporting engagement or algorithm quality is "
         "OUT. A dating-app study reporting PARTNERSHIP is IN; one reporting STI risk is OUT. The "
         "exposure sentence can be word-for-word identical in each pair.", "",
         "**Coital frequency goes to A.14, not into the sexual-health bin.** Frequency is a proximate "
         "determinant of fertility and belongs to a sibling hypothesis; the sexual-health wall is "
         "about STI and risk outcomes. Dropping frequency into `OFF_SEXHEALTH` silently deletes a "
         "cross-reference.", "",
         "**Tabulation is not estimation.** A record reporting how many couples now meet online is "
         "describing the exposure series. It is RELEVANT, it carries stage 10, and it earns no "
         "causal recall credit. Only `PRIMARY_*` cells do.", "",
         "**Homonyms should be absent, and their presence is a signal.** A4 counted rather than "
         "sampled — geochronology 0.0% on-outcome over 4,992 citing works, agronomy 0.1% "
         "human-anchored — and D1 put zero geochronology-term records in its top 800. If a batch "
         "contains any, something upstream has gone wrong and it is worth saying so in a `note`.", "",
         "**Defer rather than guess.** An exclusion the abstract could not support is a silent false "
         "negative and nothing downstream can recover it.", "",
         "## Cells", "", "| cell | definition |", "|---|---|"]
    for c, d in CELLS:
        L.append(f"| `{c}` | {d} |")
    L += ["", "## Outcome types", "", "| outcome_type | definition |", "|---|---|"]
    for c, d in OUTCOME_TYPES:
        L.append(f"| `{c}` | {d} |")
    L += ["", "## Verdict convention", "",
          "- `RELEVANT` — a `PRIMARY_*`, `SECONDARY_*`, `MECHANISM_*`, `REVERSE_DIRECTION` or "
          "`EXPOSURE_SERIES` cell.",
          "- `UNCERTAIN` — routing genuinely unclear on the visible record, or a Wall 9 candidate "
          "whose exposure is a technology rollout and whose design the abstract does not state. "
          "Pairs with `SECONDARY_TECH_*` or `INSUFFICIENT_INFO`.",
          "- `NOT_RELEVANT` — an `OFF_*` cell. A `ROUTE_*` cell is NOT_RELEVANT **to this chapter** "
          "and is carried by name so the sibling hypothesis inherits it rather than re-searching for "
          "it.", "",
          "## Batches", "",
          f"{n} batches of up to {BATCH_SIZE} records; **{len(work):,} records total**, "
          f"{n_abs:,} carrying an abstract ({n_abs / max(len(work), 1):.0%}). Abstracts truncated to "
          f"{ABSTRACT_WORDS} words.", "",
          f"**{len(work) - n_abs:,} records carry no abstract at all** and are screened on title, "
          "venue, year and type alone. Where that is not enough the answer is `UNCERTAIN` + "
          "`INSUFFICIENT_INFO`, not a guess."]
    open(OUT_RUBRIC, "w").write("\n".join(L) + "\n")
    print(f"records={len(work)} batches={n} with_abstract={n_abs} -> {os.path.relpath(BATCH_DIR, ROOT)}")
    print(f"-> {os.path.relpath(OUT_RUBRIC, ROOT)}")


if __name__ == "__main__":
    main()
