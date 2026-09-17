#!/usr/bin/env python3
"""
411 — A.6 (TICK-087) stage 4: record the S4_FERT_NODESIGN screen decisions and tally the screen.

What this is and is not. The `ASSIGN` table below is **authored judgment**, not a derived quantity:
every record in S4 was read (title, flags and abstract snippet) against
`stigma-reduction-contraception-abortion-screen-rubric.md` and assigned a cell by hand. The script
exists to attach those decisions to the right OpenAlex ids, to refuse to run if the ordering it
assumes has drifted, and to generate the tally — so the only retyped thing is the judgment itself
(`generate-result-tables-never-retype`).

S4 is the stratum with a normative exposure and a fertility-outcome marker but no design marker. It
is read exhaustively rather than sampled because a design the abstract does not name is exactly how
a primary-cell study would hide from `410`'s flagger.

Ordering guard. `ASSIGN` is keyed by position in the same deterministic sort `410` used
(-degree, -cited_by). A positional key is fragile, so the table carries a title prefix for every
row and the script aborts if any prefix fails to match. A silent off-by-one would mislabel 152
records.

Cell codes expand to the rubric's cells; the codes exist only to keep the table readable.
"""
import csv, json, pathlib, re, sys, unicodedata
from collections import Counter

# TICK-074's defect, hit here on first run: three guards failed only because OpenAlex titles carry
# curly apostrophes and quotes where the guard used ASCII. Fold the punctuation BEFORE comparing,
# and strip leading quote marks, or a title-prefix guard reports drift that does not exist.
_FOLD = {0x2018: "'", 0x2019: "'", 0x201a: "'", 0x201b: "'", 0x201c: '"', 0x201d: '"',
         0x201e: '"', 0x2013: "-", 0x2014: "-", 0x2015: "-", 0x2212: "-", 0x2026: "..."}


def fold(s: str) -> str:
    s = unicodedata.normalize("NFKC", s or "").translate(_FOLD)
    return re.sub(r"\s+", " ", s).strip().lstrip("\"'").lower()

LOGDIR = pathlib.Path("literature/search-logs")
STRATA = LOGDIR / "a6-screen-strata-2026-09-17.json"
CSVP = pathlib.Path("extraction/stigma-reduction-contraception-abortion-screened.csv")
LOGP = LOGDIR / "stigma-reduction-contraception-abortion-screen-log.md"

CODES = {
    "LNU": ("LINK_NORM_USE", "USE"), "CSM": ("CONTEXT_STIGMA_MEASURE", "NONE"),
    "MNS": ("MIXED_NORM_SUPPLY", "USE"), "MND": ("MIXED_NORM_DIFFUSION", "USE"),
    "MNSEC": ("MIXED_NORM_SECULAR", "USE"), "MNT": ("MIXED_NORM_TECH", "REALIZED"),
    "MNL": ("MIXED_NORM_LAW", "REALIZED"), "OHIV": ("OFF_HIV_STIGMA", "NONE"),
    "OOS": ("OFF_OTHER_STIGMA", "NONE"), "OCL": ("OFF_CLINICAL_LOSS", "NONE"),
    "OO": ("OFF_OTHER", "NONE"), "II": ("INSUFFICIENT_INFO", "REALIZED"),
}

# position: (code, title-prefix guard, note-if-any)
ASSIGN = {
    1: ("MNS", "Family Planning Programs for the 21st", ""),
    2: ("CSM", "Unmet need for family planning in developing countries", "Arabic translation of position 4; both are duplicate versions of seed Casterline 2000 that 409 could not exclude because their ids differ. TICK-084 shape."),
    3: ("OO", "Perceived abortion stigma and psychological", "Turnaway Study. Exposure is abortion denial and the outcome is psychological wellbeing, not fertility - fails rule 7 on the outcome, not on the exposure."),
    4: ("CSM", "Unmet need for family planning in developing countries", "Duplicate version of seed Casterline 2000."),
    5: ("CSM", "Obstacles to contraceptive use in Pakistan", "Duplicate version of seed Casterline 2001."),
    6: ("CSM", "Abortion Stigma Among Low", ""), 7: ("CSM", "Stigmatizing attitudes", ""),
    8: ("LNU", "FACTORS INFLUENCING THE PATTERNS", ""),
    9: ("CSM", "A scoping review on determinants", ""),
    10: ("MND", "Fertility and Social Interaction", "Kohler-style social-interaction account; A.3 owns arrival of the idea."),
    11: ("LNU", "Determinants of unmet need for family planning in rural Burkina", ""),
    12: ("II", "The Delayed Western Fertility Decline", "Fertility outcome across countries; exposure may be normative. FULL TEXT."),
    13: ("MNS", "Correlates of Contraceptive Use and Health Facility", ""),
    14: ("OO", "Randomized experimental testing", "Survey-methodology study of abortion under-reporting."),
    15: ("LNU", "Women in Cairo", ""), 16: ("CSM", "The workplace as a site", ""),
    17: ("CSM", "Birth Control and American Modernity", ""),
    18: ("CSM", "Birth Control and American Modernity", "Version pair with position 17."),
    19: ("MNS", "Knowledge and use of family planning methods", ""),
    20: ("CSM", "PROGRAMMATIC IMPLICATIONS", ""),
    21: ("LNU", "Bad girl and unmet family planning", "HIV flag is incidental; the exposure is adolescent sexual stigma."),
    22: ("CSM", "Authoritative Knowledge and Single", ""),
    23: ("LNU", "Levels, trends and reasons for unmet need", ""),
    24: ("OO", "Abortion Reporting in the United States", ""),
    25: ("LNU", "Fear, opposition, ambivalence, and omission", "The most A.6-shaped record in S4: opposition as a reason for unmet need. Outcome is use, so ruling 2 makes it link evidence."),
    26: ("CSM", "Is the KAP-Gap Real", ""), 27: ("OO", "Effect of ACASI", ""),
    28: ("CSM", "Development and Validation of a Scale", ""),
    29: ("CSM", "Misinformation, Mistrust", ""), 30: ("CSM", "Rethinking the Mantra", ""),
    31: ("II", "Regional fertility differences in Turkey", "Persistent high fertility in the southeast; exposure may be normative. FULL TEXT."),
    32: ("MND", "Cultural niche construction", "Simulation of social transmission; A.3."),
    33: ("II", "It's a Sin", "Religious beliefs, contraceptive use and long-run development - the closest thing in S4 to an identified economic estimate. Sits on wall 5 (D.1.a) and bears on PI call 5. FULL TEXT."),
    34: ("MND", "The power of women", ""),
    35: ("MNS", "Effects of family planning on fertility behaviour", "Programme effect on fertility; A.5 owns the treatment."),
    36: ("OHIV", "Community attitudes towards childbearing", ""),
    37: ("OO", "Socio-Economic Determinants of Fertility", ""),
    38: ("LNU", "Stigma surrounding contraceptive use and abortion among secondary", ""),
    39: ("OO", "Comparing reporting of abortions", ""),
    40: ("CSM", "Men's perceptions of child-bearing", ""),
    41: ("OHIV", "A new lease of life", ""),
    42: ("MNS", "Excess Fertility and Family Planning in Rwanda", ""),
    43: ("II", "Fertility Desires and Contraceptive Transition", "Title alone cannot separate desire from norm, and the outcome may be realized. FULL TEXT."),
    44: ("CSM", "Comment: Population Programs", ""), 45: ("CSM", "Mexican-American women", ""),
    46: ("MNS", "The public and private sector family planning supply", ""),
    47: ("CSM", "It was a foregone conclusion", ""),
    48: ("OO", "Research and Professional Literature", "Literature-roundup column; all five marker families fired, which is itself the signature of a non-study."),
    49: ("OO", "The Role of Economics and Education in Shaping Public Opinion", "Outcome is opinion."),
    50: ("OO", "Some data on natural fertility", "Henry 1961; natural-fertility measurement, A.8/A.14 territory."),
    51: ("OO", "STIGMA AND EVERYDAY RESISTANCE", "General stigma theory, fails rule 1."),
    52: ("OO", "The Impact of Women's Education on Fertility", ""),
    53: ("CSM", "Anthropology theorizes reproduction", ""),
    54: ("MND", "Fertility transition, conscious choice", "Coale's conscious-choice precondition; A.3."),
    55: ("CSM", "Factors influencing sexual and reproductive health of Muslim", ""),
    56: ("OO", "WOMEN'S EMPOWERMENT AND SOCIAL CONTEXT", "D.2.a."),
    57: ("MNS", "Community and health systems barriers", ""),
    58: ("LNU", "Reasons for nonuse of contraceptive methods by women", ""),
    59: ("MNS", "Barriers to family planning service use among the urban poor", ""),
    60: ("OO", "A decomposition of trends in the nonmarital", ""),
    61: ("II", "The Role of Couple Negotiation in Unmet Need", "Partner opposition as exposure AND the decision to STOP CHILDBEARING as an outcome - the one S4 record whose outcome may be parity rather than use. FULL TEXT."),
    62: ("OHIV", "The Role of HIV-Related Stigma", ""),
    63: ("CSM", "Adolescent Sexuality and Fertility in Kenya", ""),
    64: ("CSM", "Barriers to use Contraceptive Methods among Rural Young", ""),
    65: ("MND", "Social network- and community-level influences", ""),
    66: ("MND", "Social Transmission and the Spread of Modern Contraception", ""),
    67: ("MNT", "Demographic effects of the introduction of steroid", "A.2 owns the technology arrival."),
    68: ("LNU", "Gender norms and modern contraceptive use in urban Nigeria", ""),
    69: ("LNU", "The Time Dynamics of Unmet Need", ""),
    70: ("OO", "Variations in Desired Family Size", ""),
    71: ("MNS", "The Long-term Demographic Role of Community-based Family Planning", "Matlab; A.5."),
    72: ("LNU", "Getting to intent", ""),
    73: ("MNS", "Modern contraceptive use among adolescent girls and young women in Benin", ""),
    74: ("CSM", "A qualitative exploration of perceptions", ""),
    75: ("OO", "A synthetic biosocial model", ""),
    76: ("CSM", "From women", ""), 77: ("LNU", "Male partner influence", ""),
    78: ("MND", "Fertility, parental investment", ""),
    79: ("MNS", "Modern contraceptive use among women in the Asuogyaman", ""),
    80: ("LNU", "The Influence of Changes in Fertility Related Norms", "Norm change as exposure, contraceptive use as outcome - textbook LINK_NORM_USE."),
    81: ("MNS", "Factors that influence contraceptive use amongst women in Vanga", ""),
    82: ("OO", "Barriers to sexual and reproductive health care faced by transgender", ""),
    83: ("CSM", "Barriers to seeking post-abortion care", ""),
    84: ("CSM", "Passing as", ""), 85: ("CSM", "Concordance and discordance of couples", ""),
    86: ("OO", "Reimagining infertility", ""), 87: ("OO", "Is the Pace of Social Change", ""),
    88: ("OOS", "Association between cancer stigma", "Cervical-cancer screening; rule 2 homonym."),
    89: ("CSM", "A Good Abortion Is a Tragic Abortion", ""),
    90: ("CSM", "Facets of Agency", ""),
    91: ("OO", "Determinants of fertility in Malawi", ""),
    92: ("MND", "Social Networks, Social Influence, and Fertility in Germany", ""),
    93: ("LNU", "Prevalence and determinants of unmet need for family planning in Kishanganj", ""),
    94: ("CSM", "Teenage pregnancy contextualized", ""),
    95: ("CSM", "Contraceptive practice among married market men", ""),
    96: ("MNS", "Enablers and barriers of male involvement", ""),
    97: ("MNS", "Understanding", ""),
    98: ("CSM", "As a woman who watches", ""),
    99: ("LNU", "Contraceptive use in Eswatini", ""),
    100: ("MNS", "Rationale, design, and characteristics of the multimedia", ""),
    101: ("CSM", "Gender norms and family planning amongst pastoralists", ""),
    102: ("MNS", "Acceptability of a text message", ""),
    103: ("MNS", "Pengaruh Terpaan Informasi", "Indonesian; effect of family-planning information exposure on LARC intention."),
    104: ("OO", "Socio-economic characteristics, completed fertility", ""),
    105: ("CSM", "Social determinants of low fertility in Asia", ""),
    106: ("MND", "Correction: Social Transmission", "Correction notice; version pair with position 66."),
    107: ("MNSEC", "Religion and contraceptive use in Kazakhstan", "D.1.a owns religiosity as a value; bears on PI call 5."),
    108: ("MNS", "Modern contraceptive use among adolescent girls and young women in Benin", "Version pair with position 73."),
    109: ("OO", "Fertility Transition and Its Socioeconomic Impacts in China", ""),
    110: ("II", "Sex and the Single Girl", "Cultural persistence and the pill; an economics paper that may identify a norm effect separately from the technology. Sits on wall 1. FULL TEXT."),
    111: ("CSM", "LISTENING TO WOMEN", ""),
    112: ("CSM", "The Ignored Role of Men", ""),
    113: ("CSM", "Rationalization, facilitators, and impediments", ""),
    114: ("CSM", "Knowledge and Practice of Family Planning among Female Basic", ""),
    115: ("OO", "Determinants of fertility preferences among currently married", ""),
    116: ("CSM", "Changing attitudes and behaviour concerning contraception", ""),
    117: ("OO", "Fertility Change in Central Asia", ""),
    118: ("MNL", "Anti-abortion politics and changes in abortion", "A.4 owns the legal shock; also carries the B.5 clinical vocabulary."),
    119: ("CSM", "Access to basic reproductive rights", ""),
    120: ("CSM", "Access to Basic Reproductive Rights", "Version pair with position 119."),
    121: ("CSM", "Emergency contraception among young people in Uganda", ""),
    122: ("CSM", "From theories of contraceptive use to human rights", ""),
    123: ("LNU", "The Dominant Role of Community Influences", ""),
    124: ("OO", "Family planning in context", ""),
    125: ("CSM", "Awareness and acceptance of contraceptive methods", ""),
    126: ("MNS", "Acceptability and utilization of modern contraceptives", ""),
    127: ("LNU", "Dynamics of Contraceptive use in Rajasthan", ""),
    128: ("LNU", "An application of Systematic Anomalous Case Analysis", ""),
    129: ("LNU", "Does girls", ""),
    130: ("LNU", "Drivers of contraceptive non-use", ""),
    131: ("LNU", "Survey on understanding of socio-demographic factors", ""),
    132: ("CSM", "Macro-level facilitators and impediments", ""),
    133: ("MNS", "Population Campaigns", ""),
    134: ("CSM", "Understanding reproductive decisions", ""),
    135: ("OO", "Fertility Transition in China", ""),
    136: ("CSM", "Unveiling Mexico", ""),
    137: ("MND", "Exploring the Relationship Between Interpersonal Communication", ""),
    138: ("CSM", "Negotiating Reproduction", ""),
    139: ("CSM", "The Interface between Abortion Practice and Community Response in Amhara", ""),
    140: ("CSM", "The Interface between Abortion Practice and Community Response in Woldia", "Near-duplicate of position 139, different study site."),
    141: ("CSM", "Attitudes toward abortion", ""),
    142: ("CSM", "Scoping review of barriers and facilitators to vasectomy", ""),
    143: ("LNU", "UNMET NEED FOR PREVENTION", ""),
    144: ("MNS", "Family planning programs in South Asia", ""),
    145: ("CSM", "Male participation in family planning decision making", ""),
    146: ("OO", "Fertility transition across major Sub-Saharan African cities", "Proximate determinants; A.13/A.14."),
    147: ("CSM", "Reproductive Health Disparities in Latin America", ""),
    148: ("CSM", "Gender and family formation in Uttar Pradesh", ""),
    149: ("LNU", "Exploring the Individual and Interpersonal Obstructive", ""),
    150: ("CSM", "Becoming a Woman in Silence", ""),
    151: ("MNS", "A Pilot Study of the Creighton Model", ""),
    152: ("LNU", "Dynamic stagnation", "Contraceptive non-use during a fertility stall; the stall is context, the outcome is use."),
}


def main():
    d = json.loads(STRATA.read_text())
    rs = [r for r in d["records"] if r["stratum"] == "S4_FERT_NODESIGN"]
    rs.sort(key=lambda r: (-(r.get("degree") or 0), -(r.get("cited_by") or 0)))
    if len(rs) != len(ASSIGN):
        print(f"S4 has {len(rs)} records, ASSIGN has {len(ASSIGN)} — refusing to run", file=sys.stderr)
        return 2

    bad = []
    for pos, (code, guard, _note) in ASSIGN.items():
        title = fold(rs[pos - 1].get("title"))
        if not title.startswith(fold(guard)[:28]):
            bad.append(f"  pos {pos}: guard {guard[:40]!r} != title {title[:50]!r}")
    if bad:
        print("ORDERING DRIFT — the positional keys no longer match; refusing to write:",
              file=sys.stderr)
        print("\n".join(bad), file=sys.stderr)
        return 2

    existing = list(csv.DictReader(CSVP.open()))
    fields = list(existing[0].keys())
    already = {r["id"] for r in existing if r["batch"] == "2"}
    if already:
        print(f"batch 2 already present ({len(already)} rows) — regenerating the log only, "
              f"not appending", flush=True)
    rows = []
    for pos, (code, _guard, note) in sorted(ASSIGN.items()):
        r = rs[pos - 1]
        cell, outcome = CODES[code]
        fl = r.get("flags") or {}
        rows.append({
            "id": r["id"], "batch": "2", "stratum": "S4_FERT_NODESIGN",
            "read_mode": "exhaustive", "cell": cell, "outcome_level": outcome,
            "dose_unit": "NONE", "phenomenon_window": "SDT",
            "estimator_class": "OLS_ADJUSTED" if cell in
                ("LINK_NORM_USE", "MIXED_NORM_SECULAR", "MIXED_NORM_TECH", "MIXED_NORM_LAW")
                else ("QUALITATIVE" if fl.get("measure_only") else "DESCRIPTIVE"),
            "stigma_object": "ABORTION" if "abortion" in (r.get("title") or "").lower()
                else ("FAMILY_PLANNING" if "family planning" in (r.get("title") or "").lower()
                      else "CONTRACEPTION"),
            "stigma_bearer": "COMMUNITY",
            "second_read_required": "yes" if cell == "INSUFFICIENT_INFO" else "no",
            "note": note or f"S4 screen, rubric rules 1-7; cell {cell}.",
        })

    if not already:
        with CSVP.open("a", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=fields)
            for row in rows:
                w.writerow({k: row.get(k, "") for k in fields})

    allrows = list(csv.DictReader(CSVP.open()))
    tally = Counter(r["cell"] for r in allrows)
    by_stratum = Counter(r["stratum"] for r in allrows)
    primary = [r for r in allrows if r["cell"] == "PRIMARY_NORM_FERTILITY"]
    ii = [r for r in allrows if r["cell"] == "INSUFFICIENT_INFO"]

    log = [f"# A.6 screen log", "",
           "Decisions live in `extraction/stigma-reduction-contraception-abortion-screened.csv`.",
           "Cells and tags are defined by",
           "`stigma-reduction-contraception-abortion-screen-rubric.md`. Tallies below are generated",
           "by `source/build/goldset/411_a6_apply_s4_screen.py`; do not edit by hand.", "",
           "## Batch 1 — S1_DECISIVE, S2_BRIDGE, S3_DESIGN_USE (exhaustive, 12 records)", "",
           "Hand-screened and recorded directly in the CSV. The whole of S1 is one record.", "",
           "## Batch 2 — S4_FERT_NODESIGN (exhaustive, 152 records)", "",
           "Every record read on title, flags and abstract snippet. No cell was added mid-screen:",
           "the rubric's existing cells absorbed all 152, which is itself weak evidence that the",
           "rubric's cell list is adequate to this literature.", "",
           f"## Tally across {len(allrows)} screened records", "", "| cell | n |", "|---|---|"]
    for c, n in tally.most_common():
        log.append(f"| `{c}` | {n} |")
    log += ["", "| stratum | screened |", "|---|---|"]
    for s, n in sorted(by_stratum.items()):
        log.append(f"| `{s}` | {n} |")
    log += ["", f"## `PRIMARY_NORM_FERTILITY`: **{len(primary)}**", ""]
    if not primary:
        log += ["Empty. Every stratum in which a primary-cell study could appear has now been read",
                "exhaustively — S1 (exposure + design + fertility outcome), S2 (the citation",
                "bridges), S3 (exposure + design + use outcome) and S4 (exposure + fertility",
                "outcome, no design marker) — 164 records in total, and none estimates the effect of",
                "a normative exposure on realized fertility.", "",
                "This is the fifth independent channel to agree (scope §15 lists four). It is not yet",
                "a closed result: the records below are unresolved and each could in principle",
                "carry the missing estimate.", ""]
    log += [f"## `INSUFFICIENT_INFO` — full text required: **{len(ii)}**", "",
            "| id | stratum | why |", "|---|---|---|"]
    for r in ii:
        log.append(f"| `{r['id']}` | {r['stratum']} | {r['note'][:150]} |")
    log += ["", "## Not yet screened", "",
            "S5_EXPOSURE 515 (120 sampled), S6_WEAK 1,650 (60 sampled), S7_NOABSTRACT 486 (60",
            "sampled) — the sampled tail, plus both term arms from scope §14. The absence claim",
            "rests on the exhaustive strata; the sample exists to bound the chance that the",
            "flagger misrouted a primary-cell study out of them, and it has not yet been read.", ""]
    LOGP.write_text("\n".join(log) + "\n")

    print(f"{'skipped (already present)' if already else f'appended {len(rows)}'} S4 rows; CSV now {len(allrows)} records")
    print(f"PRIMARY_NORM_FERTILITY={len(primary)}  INSUFFICIENT_INFO={len(ii)}")
    print(dict(tally))
    print(f"wrote {LOGP}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
