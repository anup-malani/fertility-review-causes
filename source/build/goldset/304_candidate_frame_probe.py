#!/usr/bin/env python3
"""304 — frame-size probe over the unstarted hypotheses, to pick the next chapter.

Why this exists
---------------
"Work the next smallest hypothesis" needs a number attached to "smallest". TICK-075 sized A.23 with
a one-shot OpenAlex probe and recorded the result only in prose; this script makes the same decision
reproducible and re-runnable as chapters close and the unstarted set shrinks.

Four passes, and the reason for each
------------------------------------
1. NARROW  — one tight phrase block per candidate, intersected with a shared fertility outcome axis.
2. WIDE    — a deliberately looser axis for the candidates that came out small in pass 1. A thin
             count is as often a thin word list as a thin literature (`empty-cell-needs-second-
             channel`). Pass 1 alone ranked A.6 first at 12 records; pass 2 moved it to 686 and moved
             C.2.h from 141 to 4,484. Ranking on one vocabulary picks the wrong chapter.
3. SUBLIT  — each sub-literature of the finalists queried ALONE, so a vocabulary that contributes
             nothing is visible rather than hidden inside an OR block (`advance-the-baseline-when-
             accepting-terms`).
4. UNION   — the deduplicated union frame per finalist. This is the number that ranks them.
Plus a HOMONYM pass: candidate vocabularies that are known to be shared with an unrelated literature
are measured against the outcome axis, so the contamination is a number and not a worry.

Guarded OpenAlex hazards: no commas inside filter values, no phrase beginning with "not", no "?"
wildcards, and a known-positive control so a run of zeros reads as a broken probe rather than as an
empty literature (`validate-a-null-detector-on-positives`).

Outputs
-------
literature/search-logs/candidate-frame-probe-<date>.json   every count, with the axis that produced it
literature/search-logs/candidate-frame-probe-<date>.md     the ranking table, generated from that JSON

Usage: python3 source/build/goldset/304_candidate_frame_probe.py [--date YYYY-MM-DD]
"""
import argparse
import json
import subprocess
import sys
import time
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
LOGS = ROOT / "literature" / "search-logs"
KEY = next((l.split("=", 1)[1].strip() for l in (ROOT / ".env").read_text().splitlines()
            if l.startswith("OPENALEX_API_KEY=")), "")
MAILTO = "shravanh@uchicago.edu"

# Held identical across candidates in passes 1-2 so the counts are comparable.
OUTCOME = '("fertility" OR "childbearing" OR "birth rate" OR "total fertility rate")'
# Passes 3-4 widen it; the finalists are compared only against each other.
OUTCOME_WIDE = ('("fertility" OR "childbearing" OR "birth rate" OR "total fertility rate" '
                'OR "family size" OR "number of children")')

# ---------------------------------------------------------------- pass 1: every unstarted candidate
NARROW = [
 ("A.6",  "stigma-reduction-contraception-abortion",
  '("abortion stigma" OR "contraceptive stigma" OR "contraception stigma" OR "family planning stigma")'),
 ("A.8",  "parity-progression-stopping-behavior",
  '("parity progression" OR "stopping behaviour" OR "stopping behavior" OR "birth spacing" OR "birth interval")'),
 ("A.9",  "population-age-structure-momentum",
  '("population momentum" OR "demographic momentum" OR "population age structure")'),
 ("A.13", "breastfeeding-lactational-amenorrhea",
  '("lactational amenorrhea" OR "lactational amenorrhoea" OR "postpartum amenorrhea" OR "breastfeeding duration")'),
 ("A.14", "coital-frequency-biological",
  '("coital frequency" OR "sexual frequency" OR "frequency of intercourse" OR "sexual inactivity")'),
 ("A.16", "paternal-age-sperm-quality",
  '("sperm count" OR "semen quality" OR "sperm quality" OR "sperm concentration" OR "paternal age")'),
 ("A.19", "intergenerational-transmission-fertility",
  '("intergenerational transmission of fertility" OR "intergenerational fertility correlation" OR "fertility transmission")'),
 ("A.20", "cultural-diffusion-mechanisms",
  '("cultural diffusion" OR "social learning" OR "social contagion" OR "peer effects")'),
 ("B.2",  "endocrine-disruptors-environmental-toxins",
  '("endocrine disruptor" OR "endocrine disrupting chemical" OR "bisphenol" OR "phthalate" OR "pesticide exposure")'),
 ("B.3",  "infectious-disease-sterility",
  '("sexually transmitted infection" OR "pelvic inflammatory disease" OR "infertility belt" OR "chlamydia" OR "gonorrhea")'),
 ("B.4",  "obesity-metabolic-subfecundity",
  '("obesity" OR "body mass index" OR "metabolic syndrome")'),
 ("C.2.a","childcare-availability-cost",
  '("childcare cost" OR "child care cost" OR "childcare availability" OR "childcare subsidy" OR "daycare")'),
 ("C.2.d","tax-and-transfer-pronatalism",
  '("child allowance" OR "baby bonus" OR "child benefit" OR "parental leave" OR "child tax credit")'),
 ("C.2.f","rising-inequality-and-status-competition",
  '("income inequality" OR "status competition" OR "positional competition" OR "relative status")'),
 ("C.2.h","digital-leisure-substitution",
  '("screen time" OR "video games" OR "social media use" OR "smartphone use" OR "digital leisure" OR "internet use")'),
 ("C.3.a","agricultural-mode-of-production",
  '("mode of production" OR "agricultural household" OR "peasant household" OR "farm household")'),
 ("C.3.d","quantity-quality-tradeoff",
  '("quantity-quality" OR "quantity quality tradeoff" OR "child quality")'),
 ("C.3.f","wealth-flows-reversal",
  '("wealth flows" OR "intergenerational transfer" OR "intergenerational wealth")'),
 ("C.4.a","land-and-resource-constraints-malthusian",
  '("land constraints" OR "land scarcity" OR "Malthusian" OR "land availability")'),
 ("C.6.a","easterlin-relative-income",
  '("relative income hypothesis" OR "Easterlin hypothesis" OR "relative cohort size" OR "cohort size")'),
 ("D.1.c","cultural-evolution-demographic-transition",
  '("cultural evolution" OR "cultural transmission" OR "gene-culture coevolution")'),
 ("D.1.d","nationalism-pronatalist-ideology",
  '("pronatalist" OR "pronatalism" OR "natalist policy" OR "nationalist ideology")'),
 ("D.2.c","son-preference-cultural",
  '("son preference" OR "sex selection" OR "missing women")'),
 ("D.3.a","mental-health-anxiety-epidemic",
  '("mental health" OR "anxiety disorder" OR "depression" OR "psychological distress")'),
]

# ------------------------------------------------- pass 2: a second vocabulary for the small end
WIDE = [
 ("A.6",  '("stigma" OR "taboo" OR "social disapproval" OR "shame") AND ("contraception" OR "contraceptive" OR "abortion" OR "family planning")'),
 ("A.9",  '("population momentum" OR "demographic momentum" OR "age structure" OR "age composition" OR "tempo effect" OR "compositional change")'),
 ("A.13", '("breastfeeding" OR "breast feeding" OR "lactation" OR "amenorrhea" OR "amenorrhoea" OR "weaning" OR "suckling")'),
 ("A.14", '("coital frequency" OR "sexual frequency" OR "sexual activity" OR "sexual behaviour" OR "sexual behavior" OR "sexual abstinence" OR "fecundability")'),
 ("A.19", '("intergenerational transmission" OR "intergenerational correlation" OR "intergenerational continuity" OR "mother-daughter") AND ("family size" OR "number of children" OR "fertility preferences" OR "fertility")'),
 ("A.20", '("diffusion" OR "social learning" OR "social network" OR "peer effect" OR "social influence" OR "ideational change")'),
 ("C.2.a",'("childcare" OR "child care" OR "day care" OR "daycare" OR "kindergarten" OR "preschool" OR "creche" OR "nursery school")'),
 ("C.2.h",'("screen time" OR "video game" OR "social media" OR "smartphone" OR "internet" OR "television" OR "leisure time" OR "time use")'),
 ("C.3.f",'("wealth flows" OR "intergenerational transfer" OR "net transfers" OR "child cost" OR "value of children" OR "old age support")'),
 ("C.6.a",'("Easterlin" OR "relative income" OR "cohort size" OR "cohort crowding" OR "baby boom")'),
 ("D.1.c",'("cultural evolution" OR "cultural transmission" OR "gene-culture" OR "evolutionary demography" OR "natural selection" OR "reproductive success" OR "fitness")'),
 ("D.1.d",'("pronatalist" OR "pronatalism" OR "natalism" OR "nationalism" OR "population policy" OR "demographic anxiety" OR "great replacement")'),
]

# --------------------------------- pass 3: each sub-literature of the finalists, queried on its own
SUBLIT = [
 ("A.19", "core (pass 1)", '("intergenerational transmission of fertility" OR "intergenerational fertility correlation" OR "fertility transmission")'),
 ("A.19", "epidemiological / immigrant", '("second-generation immigrants" OR "immigrant fertility" OR "country of origin culture" OR "epidemiological approach")'),
 ("A.19", "sibship / family-size lineage", '("sibship size" OR "family size of origin" OR "parental family size" OR "number of siblings")'),
 ("A.19", "multigenerational registers", '("multigenerational" OR "three generations" OR "grandparents" OR "lineage")'),
 ("A.19", "socialization of preferences", '("fertility preferences" OR "ideal family size" OR "family size preferences") AND ("parents" OR "socialization" OR "transmitted")'),
 ("C.3.f", "core (pass 1)", '("wealth flows" OR "intergenerational transfer" OR "intergenerational wealth")'),
 ("C.3.f", "NTA / lifecycle deficit", '("National Transfer Accounts" OR "lifecycle deficit" OR "life cycle deficit" OR "generational accounts")'),
 ("C.3.f", "child economic contribution", '("child labour contribution" OR "child labor contribution" OR "children economic value" OR "value of children" OR "cost of children")'),
 ("C.3.f", "upward support", '("old age support" OR "old-age support" OR "filial support" OR "remittances to parents" OR "parental support in old age")'),
]

# ------------------------------------------------------ pass 4: the union frame that does the ranking
UNION = [
 ("A.6",   '("abortion stigma" OR "contraceptive stigma" OR "contraception stigma" OR "family planning stigma" OR "stigma" OR "taboo" OR "social disapproval" OR "moral opposition") AND ("contraception" OR "contraceptive" OR "abortion" OR "family planning" OR "birth control")'),
 ("A.19",  '("intergenerational transmission of fertility" OR "intergenerational fertility correlation" OR "fertility transmission" OR "second-generation immigrants" OR "immigrant fertility" OR "epidemiological approach" OR "sibship size" OR "parental family size" OR "family size of origin" OR "number of siblings" OR "ideal family size" OR "fertility preferences")'),
 ("C.3.f", '("wealth flows" OR "intergenerational transfer" OR "intergenerational wealth" OR "National Transfer Accounts" OR "lifecycle deficit" OR "life cycle deficit" OR "child labour contribution" OR "child labor contribution" OR "value of children" OR "old age support" OR "old-age support" OR "filial support")'),
 ("C.6.a", '("Easterlin" OR "relative income" OR "cohort size" OR "cohort crowding" OR "relative cohort")'),
]

# ---------------------------------------------------- homonym: shared vocabulary, unrelated literature
HOMONYM = [
 ("C.6.a", "Easterlin paradox, unrestricted", '"Easterlin paradox"', None),
 ("C.6.a", "Easterlin paradox INTERSECT fertility", '"Easterlin paradox"', OUTCOME_WIDE),
 ("C.6.a", "relative income INTERSECT well-being", '("relative income") AND ("happiness" OR "life satisfaction" OR "subjective well-being")', None),
 ("C.6.a", "relative income INTERSECT fertility", '("relative income")', OUTCOME_WIDE),
]

# A hypothesis with a chapter already written. A run where this returns 0 is a broken probe.
CONTROL = ('C.3.e (chapter written)', '("credit constraint" OR "liquidity constraint")', OUTCOME)


def count(axis, outcome=None):
    """Records matching axis (AND outcome, if given) in title or abstract. (count, error)."""
    q = f"{axis} AND {outcome}" if outcome else axis
    args = ["curl", "-sS", "--max-time", "120", "-G", "https://api.openalex.org/works",
            "--data-urlencode", f"filter=title_and_abstract.search:{q}",
            "--data-urlencode", "per-page=1",
            "--data-urlencode", f"api_key={KEY}",
            "--data-urlencode", f"mailto={MAILTO}"]
    r = subprocess.run(args, capture_output=True, text=True)
    try:
        d = json.loads(r.stdout)
    except json.JSONDecodeError:
        return None, f"non-JSON response: {r.stdout[:160]}"
    if "meta" not in d:
        return None, f"API error: {json.dumps(d)[:200]}"
    return d["meta"]["count"], None


def run(rows, outcome):
    out = []
    for row in rows:
        axis = row[-1]
        n, err = count(axis, outcome)
        out.append({"row": row[:-1], "axis": axis, "n": n, "err": err})
        label = " / ".join(str(x) for x in row[:-1])
        print(f"  {label:52} {n!s:>8}  {err or ''}", flush=True)
        time.sleep(0.35)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", default=date.today().isoformat())
    args = ap.parse_args()

    if not KEY:
        sys.exit("no OPENALEX_API_KEY in .env — an unauthenticated run is budget-limited and its "
                 "zeros are not evidence")

    print("CONTROL (a hypothesis known to have a literature):")
    ctrl, ctrl_err = count(CONTROL[1], CONTROL[2])
    print(f"  {CONTROL[0]:52} {ctrl!s:>8}  {ctrl_err or ''}")
    if not ctrl:
        sys.exit("control returned 0 or failed — the probe is broken; do not read the passes below "
                 "as literature sizes")

    print("\nPASS 1 — narrow axis, every unstarted candidate:")
    p1 = run(NARROW, OUTCOME)
    print("\nPASS 2 — second vocabulary, the small end of pass 1:")
    p2 = run(WIDE, OUTCOME)
    print("\nPASS 3 — sub-literatures of the finalists, each alone:")
    p3 = run(SUBLIT, OUTCOME_WIDE)
    print("\nPASS 4 — deduplicated union frame, the finalists:")
    p4 = run(UNION, OUTCOME_WIDE)
    print("\nHOMONYM — shared vocabulary against an unrelated literature:")
    hm = []
    for code, label, axis, outcome in HOMONYM:
        n, err = count(axis, outcome)
        hm.append({"row": [code, label], "axis": axis, "outcome": outcome, "n": n, "err": err})
        print(f"  {code} / {label:46} {n!s:>8}  {err or ''}")
        time.sleep(0.35)

    blob = {"date": args.date, "outcome_axis": OUTCOME, "outcome_axis_wide": OUTCOME_WIDE,
            "control": {"label": CONTROL[0], "n": ctrl},
            "pass1_narrow": p1, "pass2_wide": p2, "pass3_sublit": p3,
            "pass4_union": p4, "homonym": hm}
    jf = LOGS / f"candidate-frame-probe-{args.date}.json"
    jf.write_text(json.dumps(blob, indent=2) + "\n")

    # The ranking table is GENERATED from the counts above, never retyped.
    wide = {r["row"][0]: r["n"] for r in p2}
    union = {r["row"][0]: r["n"] for r in p4}
    slug = {c: s for c, s, _ in NARROW}
    lines = [f"# Candidate frame probe — {args.date}", "",
             "Generated by `source/build/goldset/304_candidate_frame_probe.py`. Do not edit by hand;",
             "re-run the script. Counts are OpenAlex `title_and_abstract.search` record counts, not",
             "screened pools — they rank candidates, they do not size a finished evidence base.", "",
             f"Control, {CONTROL[0]}: **{ctrl}**. A zero here would mean a broken probe, not an empty",
             "literature.", "",
             "The two blocks are NOT comparable. A candidate carried through pass 4 has a frame",
             "bracketed on three vocabularies; a pass-1-only candidate has a single narrow axis, and",
             "that number is a LOWER BOUND. Pass 1 put A.6 at 12 and its union frame is 675. Never",
             "rank across the blocks without widening the lower block first.", "",
             "## Bracketed — ranked on the union frame", "",
             "| code | slug | narrow | second vocabulary | union frame |",
             "|---|---|---|---|---|"]
    for r in sorted((r for r in p1 if r["row"][0] in union), key=lambda r: union[r["row"][0]]):
        c = r["row"][0]
        lines.append(f"| {c} | `{slug[c]}` | {r['n']} | {wide.get(c, '—')} | **{union[c]}** |")
    lines += ["", "## Not bracketed — narrow axis only, each a lower bound", "",
              "| code | slug | narrow (lower bound) | second vocabulary |", "|---|---|---|---|"]
    for r in sorted((r for r in p1 if r["row"][0] not in union),
                    key=lambda r: wide.get(r["row"][0]) or r["n"] or 10**9):
        c = r["row"][0]
        lines.append(f"| {c} | `{slug[c]}` | {r['n']} | {wide.get(c, '—')} |")
    lines += ["", "## Sub-literatures of the finalists, each queried alone", "",
              "| code | sub-literature | n |", "|---|---|---|"]
    lines += [f"| {r['row'][0]} | {r['row'][1]} | {r['n']} |" for r in p3]
    lines += ["", "## Homonym check", "",
              "| code | query | n |", "|---|---|---|"]
    lines += [f"| {r['row'][0]} | {r['row'][1]} | {r['n']} |" for r in hm]
    lines.append("")
    (LOGS / f"candidate-frame-probe-{args.date}.md").write_text("\n".join(lines))
    print(f"\nwrote {jf.name} and candidate-frame-probe-{args.date}.md")


main()
