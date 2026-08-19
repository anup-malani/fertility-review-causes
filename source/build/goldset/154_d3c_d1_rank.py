#!/usr/bin/env python3
r"""
154_d3c_d1_rank.py — D.3.c, stage D1. Deterministic ranking and budget cutoff (free).

PROTOCOL Phase D is a cascade of three sieves of rising cost: D1 deterministic (free) -> D2a Haiku
(cheap, recall-preserving) -> D2b Sonnet (expensive, precision + extraction) -> RA gate. This script
is D1, and on this chapter it is the load-bearing one: B1 sized the production pull at **390,983
records**, and what D1 removes is what the paid stages never see.

D1 IS A BUDGET CONTROL, NOT A JUDGEMENT. Its only job is to drop records that are cheaply and
confidently off-cell, and its calibration target is therefore **recall = 1.0 on the frozen gold**, not
precision. A D1 false negative is unrecoverable — nothing downstream can retrieve a record D1 threw
away — so the cutoff is chosen at the largest budget saving that still loses ZERO gold records, and
the recall-versus-budget curve is printed so the choice is visible rather than asserted.

WHAT D1 CAN AND CANNOT SCORE ON. The production query is OUTCOME-ONLY (B1: the outcome-AND-treatment
conjunction was strictly dominated), so **every record in the pull already carries a fertility-outcome
term in its title**. Outcome vocabulary therefore has near-zero discriminating power here and is not
scored. D1's signal has to come from the other axes — mechanism, treatment, and the two wall-negatives
(reverse causation, mortality-only) — read over title AND abstract, which is information the
title-only production query never saw.

THE ORTHOGONAL-CHANNEL BYPASS IS MANDATORY (PROTOCOL Phase D1). Records reached through the citation
frame — the snowball channel — **bypass the cutoff entirely** and go straight to D2a regardless of
their term score. The cutoff applies within the keyword channel only. Without this, the dumb
term-match discards exactly the orthogonal-recall records the whole architecture exists to catch, and
Recall(B) stops measuring anything. On this chapter the bypass set is the 10,589-record Tier B frame.

CALIBRATED ON THE FRAME, PROJECTED TO THE PULL, AND THE PROJECTION IS STATED. C1 has not run, so the
gold and the scoring distribution both come from the Tier B citation frame. The frame is a citation
neighbourhood and is therefore ENRICHED relative to the open-database pull: its survivor fraction is
an upper bound on the pull's, so projecting it forward is conservative in the direction that costs
money rather than recall. Re-run this script against the real pull before committing budget.

Output: literature/search-logs/{slug}-d1-rank.md
        literature/search-logs/{slug}-d1-cutoff.json   (D2a consumes this)
"""
import json, os, re, sys

SLUG = "despair-hopelessness-fertility"
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
LOGS = os.path.join(ROOT, "literature", "search-logs")
PULL_SIZE = 390_983          # B1's measured title.search universe

sys.path.insert(0, HERE)
import importlib.util
_spec = importlib.util.spec_from_file_location("cvb", os.path.join(HERE, "152_d3c_cv_breadth.py"))
cvb = importlib.util.module_from_spec(_spec)
sys.modules["cvb"] = _spec.loader.exec_module(cvb) or cvb

# ---- Scoring features. Deliberately few, deliberately transparent, and NONE of them semantic:
# D1 is allowed to be dumb, and the next two stages exist because it is.
MECHANISM = re.compile(
    r"despair|hopeless|demorali[sz]|anomie|fatalis|normless|alienat|future orientation|"
    r"foreshortened|expectations about the future|future expectations|pessimis|bleak|"
    r"left behind|meaningless|subjective well|life satisfaction|psychological distress|"
    r"depress|mental health|deaths of despair|discourag|demoralis")
TREATMENT = re.compile(
    r"deindustriali|economic decline|declining region|distressed communit|left-behind|"
    r"plant closure|mass layoff|job loss|displaced worker|import competition|china shock|"
    r"trade shock|rust belt|manufactur|coal|unemploy|recession|economic crisis|precari|"
    r"insecur|uncertain|inequalit|opportunit|poverty|disadvantag|deprivation|marginali|"
    r"social mobility|downward mobilit|welfare")
MARGIN_TIMING = re.compile(
    r"teen|adolescent|young mother|early childbearing|early motherhood|nonmarital|non-marital|"
    r"out-of-wedlock|premarital|first birth|age at first|postpone|tempo|timing")
# ---- Wall negatives. These SUBTRACT, and none of them is allowed to be decisive on its own:
# each is a lower bound on an off-cell signal, not a proof of one.
REVERSE = re.compile(
    r"infertil|subfertil|\bivf\b|in vitro fert|assisted reproduct|fertility treatment|"
    r"fertility patient|involuntary childless|oocyte|embryo transfer|icsi\b|"
    r"stigma of infertil|childless women.{0,20}distress")
MORTALITY_ONLY = re.compile(
    r"mortalit|suicide|overdose|drug poisoning|life expectancy|alcoholic liver|cirrhosis|"
    r"cause of death|years of life lost|opioid")
NONHUMAN = re.compile(
    r"\bmice\b|\bmouse\b|\brats?\b|rodent|bovine|porcine|zebrafish|drosophila|in ovo|"
    r"livestock|cattle|poultry|heifer|dairy|swine|\bewes?\b|sows?\b")
OUTCOME = re.compile(
    r"fertil|childbear|childless|birth rate|birthrate|natalit|number of children|family size|"
    r"\btfr\b|completed famil|reproductive intention|birth")


def blob(r):
    return ((r.get("title") or "") + " " + (r.get("abstract") or "")).lower()


def score(r):
    """Additive, inspectable, and reported per feature. No weights were tuned against the gold —
    they are ordinal statements of what the walls say matters, and the CUTOFF is the only thing
    calibrated. Tuning weights on the gold and then measuring recall on the same gold would make the
    recall figure meaningless."""
    b = blob(r)
    s, why = 0, []
    if MECHANISM.search(b):
        s += 3; why.append("mechanism")
    if TREATMENT.search(b):
        s += 2; why.append("treatment")
    if MARGIN_TIMING.search(b):
        s += 1; why.append("timing-margin")
    if r.get("abstract"):
        s += 1; why.append("has-abstract")
    if REVERSE.search(b) and not MECHANISM.search(b):
        s -= 2; why.append("-reverse")
    if MORTALITY_ONLY.search(b) and not OUTCOME.search(b):
        s -= 3; why.append("-mortality-only")
    if NONHUMAN.search(b):
        s -= 3; why.append("-nonhuman")
    return s, why


def main():
    tier_b = json.load(open(os.path.join(LOGS, f"{SLUG}-tier-b-frame.json")))
    gold, _neg, _nc, _nn, _abs = cvb.load()
    goldkeys = {cvb.norm(g["title"])[:70] for g in gold}

    rows = []
    for r in tier_b:
        if not r.get("title"):
            continue
        s, why = score(r)
        rows.append({"key": cvb.norm(r["title"])[:70], "score": s, "why": why,
                     "is_gold": cvb.norm(r["title"])[:70] in goldkeys})
    n_gold = sum(1 for x in rows if x["is_gold"])

    # Recall-versus-budget curve. Every distinct threshold, so the cutoff is chosen from the curve.
    curve = []
    for thr in range(min(x["score"] for x in rows), max(x["score"] for x in rows) + 1):
        keep = [x for x in rows if x["score"] >= thr]
        kg = sum(1 for x in keep if x["is_gold"])
        curve.append({"threshold": thr, "kept": len(keep), "kept_share": len(keep) / len(rows),
                      "gold_kept": kg, "gold_recall": kg / max(n_gold, 1)})

    # THE CALIBRATION RULE: the largest threshold that still keeps EVERY gold record.
    lossless = [c for c in curve if c["gold_recall"] >= 1.0]
    chosen = max(lossless, key=lambda c: c["threshold"]) if lossless else curve[0]

    projected = round(chosen["kept_share"] * PULL_SIZE)
    out = {"stage": "D1", "slug": SLUG, "threshold": chosen["threshold"],
           "frame_kept": chosen["kept"], "frame_total": len(rows),
           "kept_share": round(chosen["kept_share"], 4),
           "gold_total": n_gold, "gold_kept": chosen["gold_kept"],
           "gold_recall": chosen["gold_recall"],
           "pull_size": PULL_SIZE, "projected_survivors": projected,
           "bypass_rule": "every Tier B (citation-frame) record bypasses the cutoff; "
                          "the cutoff applies within the keyword channel only",
           "curve": curve}
    json.dump(out, open(os.path.join(LOGS, f"{SLUG}-d1-cutoff.json"), "w"), indent=1)

    L = [f"# D.3.c — D1 deterministic ranking and budget cutoff", "",
         "**D1 is a budget control, not a judgement.** Its calibration target is **recall = 1.0 on "
         "the gold**, not precision: a D1 false negative is unrecoverable, so the cutoff is the "
         "largest budget saving that loses zero gold records. The curve below is printed so that "
         "choice is visible rather than asserted.", "",
         "**Outcome vocabulary is not scored.** The production query is outcome-only, so every "
         "record in the pull already carries a fertility-outcome term in its title — it has near-zero "
         "discriminating power here. D1 scores the other axes, over title AND abstract, which is "
         "information the title-only query never saw.", "",
         "## Features", "", "| feature | weight | rationale |", "|---|---|---|",
         "| mechanism vocabulary | +3 | the chapter's own construct; rarest and most informative |",
         "| treatment vocabulary | +2 | chronic decline / opportunity / uncertainty |",
         "| timing-margin vocabulary | +1 | chapter 2's outcome margin; cheap to spot |",
         "| has an abstract | +1 | a record with an abstract is cheaper for D2a to judge correctly |",
         "| reverse causation, no mechanism | −2 | Wall 5; infertility-distress owns the instruments |",
         "| mortality terms, no outcome | −3 | Wall 4; the largest decoy cloud |",
         "| non-human | −3 | animal studies |", "",
         "No weight was tuned against the gold — they are ordinal statements of what the walls say "
         "matters. Only the CUTOFF is calibrated. Tuning weights on the gold and then measuring "
         "recall on that same gold would make the recall figure meaningless.", "",
         "## Recall versus budget", "",
         "| threshold | kept | share of frame | gold kept | gold recall |", "|---|---|---|---|---|"]
    for c in curve:
        mark = " **<- chosen**" if c["threshold"] == chosen["threshold"] else ""
        L.append(f"| {c['threshold']} | {c['kept']:,} | {c['kept_share']:.1%} | "
                 f"{c['gold_kept']}/{n_gold} | {c['gold_recall']:.1%}{mark} |")
    L += ["", f"**Chosen threshold: {chosen['threshold']}** — keeps "
              f"{chosen['kept']:,} of {len(rows):,} frame records ({chosen['kept_share']:.1%}) at "
              f"**{chosen['gold_recall']:.0%} gold recall** ({chosen['gold_kept']}/{n_gold}).", "",
          "## The orthogonal-channel bypass", "",
          "**Every record reached through the citation frame bypasses this cutoff and goes straight "
          "to D2a, whatever its term score.** The cutoff applies within the keyword channel only. "
          "Without the bypass the dumb term-match discards exactly the orthogonal-recall records the "
          "architecture exists to catch, and Recall(B) stops measuring anything. On this chapter the "
          "bypass set is the whole 10,589-record Tier B frame — a rounding error against a 390,983 "
          "pull, and the cheapest insurance in the pipeline.", "",
          "## Projection to the production pull", "",
          f"At the chosen threshold, **{chosen['kept_share']:.1%} of the frame survives**, which "
          f"projects to roughly **{projected:,} records** of the {PULL_SIZE:,}-record pull reaching "
          "D2a.", "",
          "**The projection is conservative, and states why.** The gold and the score distribution "
          "both come from the Tier B citation frame, which is a citation neighbourhood and therefore "
          "ENRICHED relative to an open-database pull: a larger share of it carries mechanism and "
          "treatment vocabulary than the pull will. The frame's survivor fraction is thus an **upper "
          "bound** on the pull's, and the error runs toward over-estimating cost rather than "
          "under-estimating recall. **Re-run this script against the real pull before committing "
          "budget** — that is a measurement C1 makes available and this one only approximates.", ""]
    open(os.path.join(LOGS, f"{SLUG}-d1-rank.md"), "w").write("\n".join(L) + "\n")
    print(f"threshold={chosen['threshold']} kept={chosen['kept']}/{len(rows)} "
          f"({chosen['kept_share']:.1%}) gold={chosen['gold_kept']}/{n_gold} "
          f"projected_survivors={projected:,}")


if __name__ == "__main__":
    main()
