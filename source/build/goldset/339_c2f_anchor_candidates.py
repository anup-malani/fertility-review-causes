#!/usr/bin/env python3
"""339 — C.2.f anchor candidate list, built rather than hand-assembled (TICK-081).

This existed twice as inline code and got it wrong twice, so it is a script now.

A POSITIVE CONTROL IS A RECORD A CORRECT QUERY SHOULD RETRIEVE. Two failures taught the definition:

  v1 required only "carries an exposure term and has a DOI". That admitted *The Nuclear Arms Race:
     An Evolutionary Perspective* and *Conspicuous Consumption: Vehicle Purchases by Non-Profits*,
     and the mechanism arm read 2/57 -- measuring the control list, not the query.
  v2 added "and a fertility word in the title". The word-boundary test on `birth` then admitted
     *Charles Frederick Worth and the birth of Haute Couture* and *Inconspicuous Consumption: Sake,
     Beer, and the Birth of the Consumer in Japan*. "Birth of X" is an idiom, not an outcome.

v3 (here) requires a fertility OUTCOME, excludes the "birth of <the|a>" idiom explicitly, and
excludes the behavioural-ecology cloud that shares both vocabularies.

ARM ASSIGNMENT IS DERIVED, NOT ASSUMED. v1 and v2 keyed the arm off the free-seed TERMS bucket, so
every shadow-education record landed in `mechanism` -- which is how the mechanism arm came to be
scored against 13 controls that contain none of its vocabulary. Arms are now assigned by which
family of terms the TITLE actually carries, most specific first:

    education-competition  >  mechanism  >  inequality-general

`education-competition` is scope §4A's recovered second channel: the full chain is written in the
East Asian education-competition vocabulary, and probing it in economics-of-inequality vocabulary
returned 2 records against 56.

Output: literature/search-logs/rising-inequality-and-status-competition-anchor-candidates.json
"""
import json, re, pathlib
from collections import Counter

LOGS = pathlib.Path("literature/search-logs")
SEEDS = LOGS / "rising-inequality-and-status-competition-free-seeds.json"

# A fertility OUTCOME. "birth of <the|a>" is an idiom for an origin story and is excluded by name.
FERT = re.compile(r"fertilit|childbear|birth rate|births\b|birth order|family size|"
                  r"number of children|children ever born|natalit|parenthood|childless|"
                  r"reproductive success|completed fertility|first birth|fertility intention", re.I)
BIRTH_IDIOM = re.compile(r"birth of (the|a|an|modern|haute|consumer)", re.I)
# Shares both this chapter's exposure vocabulary and its outcome vocabulary; scope §8.
EVO = re.compile(r"baboon|primate|forager|hunter.gatherer|sexual selection|life.history|"
                 r"\bmating\b|allomaternal|reproductive system of|free.ranging", re.I)

EDUCOMP = re.compile(r"shadow education|private tutoring|cram school|education(al)? competition|"
                     r"tutoring|educational burden|burden of education|double reduction|"
                     r"educational investment|educational expenditure", re.I)
MECH = re.compile(r"status competition|positional|relative status|social comparison|"
                  r"conspicuous consumption|relative deprivation|status anxiety|social rank|"
                  r"arms race|rat race|keeping up with|status externalit", re.I)
INEQ = re.compile(r"income inequalit|inequality|gini|top income share|income concentration|"
                  r"wage dispersion|earnings inequalit|income distribution", re.I)

HAND = [
 ("Inequality and Growth: Why Differential Fertility Matters", 2003, "de la Croix", "theory", True),
 ("Income Inequality and Early Nonmarital Childbearing", 2014, "Kearney", "fertility", True),
 ("The Economics of Fertility: A New Era", 2023, "Doepke", "theory", True),
 ("Why did rich families increase their fertility? Inequality and marketization of child care", 2018, "Bar", "fertility", True),
 ("The Rug Rat Race", 2010, "Ramey", "link1-investment", False),
 ("Investing in Children: Changes in Parental Spending on Children, 1972-2007", 2013, "Kornrich", "link1-investment", False),
 ("Income Inequality and Class Divides in Parental Investments", 2018, "Schneider", "link1-investment", False),
 ("Expenditure Cascades", 2014, "Frank", "link1-investment", False),
 ("Social Limits to Growth", 1976, "Hirsch", "positional-canon", False),
 ("Falling Behind: How Rising Inequality Harms the Middle Class", 2007, "Frank", "positional-canon", False),
 ("The Overspent American: Why We Want What We Don't Need", 1998, "Schor", "positional-canon", False),
 ("The Theory of the Leisure Class", 1899, "Veblen", "positional-canon", False),
 ("Parenting With Style: Altruism and Paternalism in Intergenerational Preference Transmission", 2017, "Doepke", "link1-investment", False),
 ("On the Interaction between the Quantity and Quality of Children", 1973, "Becker", "c3d-boundary", True),
 # §4A: the recovered channel needs hand anchors of its own, or its recall floor rests on controls
 # harvested from the same pools the query will search.
 # year corrected 2024 -> 2026 after 336 flagged NEEDS_HUMAN_READ at Jaccard 1.0: the title
 # matched exactly and the YEAR was mine, hand-typed from memory. J Pop Econ 2026.
 # candidate-attribution-is-the-error: check which side is wrong before keying an exception.
 ("The impact of shadow education expenditures on fertility rates in South Korea", 2026, "", "education-competition", True),
 ("Education Competition and Fertility Intention: Evidence from China's Private Tutoring Ban", 2024, "", "education-competition", True),
]


def doi(r):
    v = str(r.get("id") or "").replace("https://doi.org/", "").lower()
    return v if v.startswith("10.") else ""


def arm_of(title):
    if EDUCOMP.search(title): return "education-competition"
    if MECH.search(title):    return "mechanism"
    if INEQ.search(title):    return "inequality-general"
    return None


def main():
    seeds = json.loads(SEEDS.read_text())["records"]
    controls, rejected = [], Counter()
    seen = set()
    for r in seeds:
        d, title = doi(r), r["title"]
        if not d:                       rejected["no DOI"] += 1;            continue
        if not FERT.search(title):      rejected["no fertility outcome"] += 1; continue
        if BIRTH_IDIOM.search(title):   rejected["'birth of X' idiom"] += 1; continue
        if EVO.search(title):           rejected["behavioural-ecology cloud"] += 1; continue
        arm = arm_of(title)
        if arm is None:                 rejected["no exposure family in title"] += 1; continue
        if d in seen:                   rejected["duplicate DOI"] += 1;      continue
        seen.add(d)
        controls.append({"title": title, "year": int(r["year"]) if str(r["year"]).isdigit() else 0,
                         "first_author": "", "source": "control", "arm": arm, "doi": d,
                         "outcome_is_fertility": True})

    hands = [{"title": t, "year": y, "first_author": a, "source": "hand", "arm": arm,
              "outcome_is_fertility": f} for t, y, a, arm, f in HAND]
    out = controls + hands
    (LOGS / "rising-inequality-and-status-competition-anchor-candidates.json").write_text(
        json.dumps(out, indent=1) + "\n")

    print(f"controls kept {len(controls)}, hand {len(hands)}, total {len(out)}")
    print("  arms:", dict(Counter(c["arm"] for c in out)))
    print("  rejected:", dict(rejected))


if __name__ == "__main__":
    main()
