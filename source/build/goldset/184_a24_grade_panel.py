#!/usr/bin/env python3
"""
184_a24_grade_panel.py — A.24, stage 11. GRADE panel instrument, ratings, and adversarial re-ratings.

**READ THIS FIRST: THIS IS NOT A THREE-RATER PANEL AND MUST NOT BE RECORDED AS ONE.** PROTOCOL §5.11
asks for three INDEPENDENT raters, and prior chapters met it by having a coordinator run three
separately-instantiated agents that could not see each other's judgements. What this script produces
is one rater's ratings plus two ADVERSARIAL RE-RATINGS by the same rater, one arguing the evidence
deserves to be graded higher and one arguing lower. That is a useful discipline and it is not
independence: the same reader wrote all three, and correlated error survives the exercise untouched.
The panel requirement stays OPEN on TICK-071 and the PI packet asks for rater assignment.

What the adversarial passes are for: a single rater's main failure mode is anchoring on the rating
they formed while extracting. Forcing an argument for each neighbouring rating surfaces the specific
fact that would have to be true for that rating to be right, which is exactly what a real panel's
disagreement produces. Where an adversarial pass finds such a fact, it is recorded as a CONTINGENCY
rather than resolved.

GRADE is assigned per phenomenon and per LINK, because PI Call 1 split them: this chapter grades
technology-to-partnership and imports partnership-to-births from A.7.

Output: extraction/{slug}-grade-panel.csv
        literature/search-logs/{slug}-grade-panel.md
"""
import csv, os
from collections import Counter

SLUG = "dating-apps-union-formation-friction"
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
LOGS = os.path.join(ROOT, "literature", "search-logs")
EXTRACT = os.path.join(ROOT, "extraction")
OUT_CSV = os.path.join(EXTRACT, f"{SLUG}-grade-panel.csv")
OUT_MD = os.path.join(LOGS, f"{SLUG}-grade-panel.md")

COLS = ["phenomenon", "link", "pass", "starting_level", "risk_of_bias", "inconsistency",
        "indirectness", "imprecision", "publication_bias", "rating", "rationale"]

ROWS = [
 dict(phenomenon="SDT", link="link2_technology_to_partnership", pass_="primary",
      starting_level="Low (observational)",
      risk_of_bias="-1 (7 critical, 5 serious, none low or moderate)",
      inconsistency="-1 (direction reverses with age within the best-designed study, and differs across studies)",
      indirectness="-1 (no readable study measures the registered exposure)",
      imprecision="0 (not the binding problem; several samples are large)",
      publication_bias="undetected (too few comparable estimates to assess)",
      rating="VERY LOW",
      rationale="Three separate downgrades, each independently sufficient to move one level from an "
                "already-low starting point. The floor is reached quickly and the rating carries no "
                "information about WHICH defect is fatal, which is why the domains are reported "
                "individually rather than only as a total."),
 dict(phenomenon="SDT", link="link2_technology_to_partnership", pass_="adversarial_higher",
      starting_level="Low (observational)", risk_of_bias="-1", inconsistency="0",
      indirectness="-1", imprecision="0", publication_bias="undetected", rating="VERY LOW",
      rationale="THE ARGUMENT FOR GRADING HIGHER: the age reversal in Kolk and Billari is not "
                "inconsistency, it is a FINDING — the same coefficient function estimated in two "
                "independent data sources, for two populations, agreeing on the shape. Reading a "
                "replicated interaction as heterogeneity penalises a study for being informative. "
                "WHAT WOULD HAVE TO BE TRUE: that the other studies' directions are also age-"
                "conditional rather than contradictory, which cannot be checked because they do not "
                "report by age. CONTINGENCY RECORDED: if the four unread quasi-experimental estimates "
                "report age interactions of the same shape, inconsistency should be restored to 0 — "
                "but the rating stays VERY LOW because risk of bias and indirectness alone reach the "
                "floor."),
 dict(phenomenon="SDT", link="link2_technology_to_partnership", pass_="adversarial_lower",
      starting_level="Low (observational)", risk_of_bias="-2", inconsistency="-1", indirectness="-2",
      imprecision="0", publication_bias="suspected", rating="VERY LOW (floor)",
      rationale="THE ARGUMENT FOR GRADING LOWER: GRADE has no level below very low, so a rating "
                "cannot express that this body is worse than an ordinary very-low body — and it is. "
                "Indirectness here is not 'the evidence answers a neighbouring question' but 'no "
                "evidence answers this question at all': zero studies measure dating-app use. "
                "Publication bias is suspected rather than undetected, because a null result about a "
                "widely-discussed technology is harder to publish than a striking one. WHAT WOULD "
                "HAVE TO BE TRUE for the ordinary rating to be right: that internet access is a "
                "reasonable proxy for app use. It is not, in the direction that matters — internet "
                "access predates apps by fifteen years and is nearly universal in the populations "
                "studied. FINDING CARRIED TO THE CHAPTER: the rating floor is doing real work here "
                "and the verdict should say in words what the scale cannot."),
 dict(phenomenon="SDT", link="link3_apps_to_births", pass_="primary", starting_level="n/a",
      risk_of_bias="critical (single study; reverse causality demonstrated by its own authors)",
      inconsistency="n/a (one study)", indirectness="-1 (exposure is online meeting generally, not apps)",
      imprecision="n/a", publication_bias="n/a",
      rating="INSUFFICIENT EVIDENCE",
      rationale="Per PI Call 4 an empty or near-empty primary cell earns insufficient evidence rather "
                "than a graded finding of no effect. One study, whose authors report a reverse "
                "coefficient about three times their forward one in the same sample. A rating of very "
                "low would imply a body of evidence exists and is weak; there is not a body."),
 dict(phenomenon="SDT", link="link3_apps_to_births", pass_="adversarial_higher",
      starting_level="n/a", risk_of_bias="critical", inconsistency="n/a", indirectness="-1",
      imprecision="n/a", publication_bias="n/a", rating="VERY LOW (rejected)",
      rationale="THE ARGUMENT FOR GRADING RATHER THAN DECLINING TO: the German study is a large "
                "national panel with registered births, eight waves and extensive adjustment — better "
                "than much evidence that receives a very-low rating elsewhere in this review, and "
                "declining to grade it discards information. WHY IT IS REJECTED: the objection is "
                "about the study's quality, and the reason for not grading is the CELL's emptiness. "
                "One study cannot express a body's consistency, precision or publication bias, and "
                "three of GRADE's five domains are undefined on a single estimate. PI Call 4 settles "
                "the tie in favour of insufficient evidence."),
 dict(phenomenon="SDT", link="link3_apps_to_births", pass_="adversarial_lower",
      starting_level="n/a", risk_of_bias="critical", inconsistency="n/a", indirectness="-2",
      imprecision="n/a", publication_bias="n/a", rating="INSUFFICIENT EVIDENCE (unchanged)",
      rationale="THE ARGUMENT FOR SAYING SOMETHING STRONGER: the single study's association runs "
                "OPPOSITE to the hypothesis on both births and intentions, so a reader could ask why "
                "the chapter does not report evidence against the hypothesis rather than absence of "
                "evidence. WHY THE RATING IS UNCHANGED: one observational study with demonstrated "
                "reverse causation cannot support a finding of no effect any more than it can support "
                "a finding of an effect. The asymmetry a reader expects is not there — this is a case "
                "where the evidence is too weak to conclude in EITHER direction, and the chapter says "
                "so in §9."),
 dict(phenomenon="PM", link="n/a", pass_="primary", starting_level="n/a", risk_of_bias="n/a",
      inconsistency="n/a", indirectness="n/a", imprecision="n/a", publication_bias="n/a",
      rating="NOT APPLICABLE",
      rationale="The registry restricts A.24 to the Second Demographic Transition and the technology "
                "did not exist before it."),
 dict(phenomenon="FDT", link="n/a", pass_="primary", starting_level="n/a", risk_of_bias="n/a",
      inconsistency="n/a", indirectness="n/a", imprecision="n/a", publication_bias="n/a",
      rating="NOT APPLICABLE", rationale="As above."),
]


def main():
    with open(OUT_CSV, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=COLS)
        w.writeheader()
        for r in ROWS:
            w.writerow({k: r.get("pass_" if k == "pass" else k, "") for k in COLS})
    prim = [r for r in ROWS if r["pass_"] == "primary"]
    L = [f"# GRADE panel — {SLUG} (A.24)", "",
         "## This is not a three-rater panel", "",
         "PROTOCOL §5.11 asks for three INDEPENDENT raters. What follows is **one rater's ratings plus "
         "two adversarial re-ratings by the same rater**, one arguing the evidence deserves a higher "
         "rating and one a lower. That is a useful discipline against anchoring, and it is not "
         "independence — the same reader wrote all three and correlated error survives untouched. "
         "**The three-rater requirement stays open on TICK-071**, and the PI packet asks for rater "
         "assignment.", "",
         "## Ratings", "", "| Phenomenon | Link | Rating |", "|---|---|---|"]
    for r in prim:
        L.append(f"| {r['phenomenon']} | `{r['link']}` | **{r['rating']}** |")
    L += ["", "## Per-domain, with every downgrade named", ""]
    for r in ROWS:
        L += [f"### {r['phenomenon']} · `{r['link']}` · *{r['pass_']}* → **{r['rating']}**", "",
              f"- risk of bias: {r['risk_of_bias']}", f"- inconsistency: {r['inconsistency']}",
              f"- indirectness: {r['indirectness']}", f"- imprecision: {r['imprecision']}",
              f"- publication bias: {r['publication_bias']}", "", r["rationale"], ""]
    L += ["## What the adversarial passes changed", "",
          "Neither adversarial pass changed a rating, and both produced something the primary pass "
          "had not made explicit.", "",
          "The higher-rating argument identified a **contingency**: the age reversal in the "
          "best-designed study is a replicated interaction rather than heterogeneity, and if the four "
          "unread quasi-experimental estimates report the same shape then inconsistency should be "
          "restored to zero. The rating would not move, because risk of bias and indirectness reach "
          "the floor on their own — but the chapter should not describe that study as inconsistent "
          "evidence.", "",
          "The lower-rating argument identified a **limit of the scale**: GRADE has no level below "
          "very low, so the rating cannot express that indirectness here is not 'the evidence answers "
          "a neighbouring question' but 'no evidence answers this question at all'. The chapter's "
          "verdict says in words what the scale cannot.", ""]
    open(OUT_MD, "w").write("\n".join(L) + "\n")
    print("ratings:", {f"{r['phenomenon']}/{r['link']}": r["rating"] for r in prim})
    print(f"-> {os.path.relpath(OUT_MD, ROOT)}")


if __name__ == "__main__":
    main()
