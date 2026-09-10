#!/usr/bin/env python3
"""
378 — assert every number quoted in the C.3.f scope document against the logs it came from.

Why this exists. `generate-result-tables-never-retype`: A.17's hand-typed demographic-significance
table had the right offsets and the wrong baselines, and nothing caught it because nothing checked
it. A scope document is prose and cannot be generated, but the numbers embedded in it can be
ASSERTED against the JSON the scripts wrote, and the assertion re-runs whenever a log is
regenerated. Not generation — a failing test.

Run after any re-run of 304, 376 or 377. A mismatch means the scope is stale, not that the log is
wrong: the log is the record and the scope quotes it.

Three kinds of check, because the scope quotes three kinds of number:
  LOG        a count lifted straight from a script's JSON
  DERIVED    a share or difference the prose computes from two logged counts, checked as the prose
             rounds it — this is where A.17's table went wrong
  EXTERNAL   a figure quoted from another chapter's finished text (C.3.c), checked by asserting the
             string is still present in that chapter on main. A closed chapter can be revised, and a
             quotation that silently stops matching its source is the same defect one file further
             out.

Usage: python3 source/build/goldset/378_c3f_scope_number_check.py
Exit 0 = every quoted figure matches. Exit 1 = at least one does not.
"""
import json, pathlib, re, sys

LOGS = pathlib.Path("literature/search-logs")
DATE = "2026-09-10"
SCOPE = LOGS / "wealth-flows-reversal-search-scope.md"
ROUTING = LOGS / "c3f-inherited-seeds-routing.md"
C3C = pathlib.Path("output/chapters/old-age-security-pension-crowdout.md")


def load(name):
    p = LOGS / f"{name}-{DATE}.json"
    if not p.exists():
        sys.exit(f"missing log {p} — re-run the script that writes it before checking the scope")
    return json.load(open(p))


def main():
    d376 = load("c3f-term-diagnostics")
    a = {r["label"]: r["n"] for r in d376["rows"]}
    gains = {m["term"]: m["gain"] for m in d376["marginal"]}
    d377 = load("c3f-inherited-seeds")
    d304 = load("candidate-frame-probe")
    d379 = load("c3f-wall5-null-probe")
    w = {r["label"]: r["n"] for r in d379["rows"]}
    probe = {r["row"][1]: r["n"] for r in d304["homonym"] if r["row"][0] == "C.3.f"}
    union = {r["row"][0]: r["n"] for r in d304["pass4_union"]}
    sublit = {r["row"][1]: r["n"] for r in d304["pass3_sublit"] if r["row"][0] == "C.3.f"}

    FRAME = a["CONTROL C.3.f union frame (reproduces the 09-10 number: 1101)"]
    checks = []            # (kind, label, what the scope says, what the log says)

    def log(label, claimed, actual):
        checks.append(("LOG", label, claimed, actual))

    def derived(label, claimed, actual):
        checks.append(("DERIVED", label, claimed, actual))

    # ---------------------------------------------------------------- §2 the direction arms
    log("§2 frame", 1099, FRAME)
    log("§2 UPWARD", 227, a["ARM UPWARD children -> parents"])
    log("§2 UPWARD identified", 12, a["ARM UPWARD children -> parents carrying an identified design"])
    log("§2 DOWNWARD", 1168, a["ARM DOWNWARD parents -> children"])
    log("§2 DOWNWARD identified", 68,
        a["ARM DOWNWARD parents -> children carrying an identified design"])
    log("§2 NET", 166, a["ARM NET the difference and its sign"])
    log("§2 NET identified", 6, a["ARM NET the difference and its sign carrying an identified design"])
    log("§2 both directions in one record", 15, a["ARM overlap: upward AND downward in one record"])
    log("§2 net alongside a component", 20, a["ARM overlap: net AND (upward OR downward)"])

    # ---------------------------------------------------------------- §2/§4 the inherited seeds
    log("§2 inherited seeds", 28, d377["n"])
    log("§3A flag fired on", 15, d377["flag_counts"]["fertility_outcome_named"])
    routing = dict(re.findall(r"^\| `(\w+)` \| (\d+) \|", ROUTING.read_text(), re.M))
    routed = {k: int(v) for k, v in routing.items()}
    log("§2 SEED_PRIMARY", 4, routed.get("SEED_PRIMARY"))
    log("§2 OFF_OUTCOME", 6, routed.get("OFF_OUTCOME"))
    log("§2 OFF_C3c", 4, routed.get("OFF_C3c"))
    log("§2 REVERSE", 1, routed.get("REVERSE"))
    derived("§2 the routing sums to the queue", d377["n"], sum(routed.values()))

    # ---------------------------------------------------------------- §3 vocabulary
    log("§3 identified designs in frame", 18, a["FRAME carrying an identified design"])
    log("§3 accounting markers in frame", 256, a["FRAME carrying an accounting/measurement marker"])
    derived("§3 identified share of frame (1.6%)", 1.6,
            round(100 * a["FRAME carrying an identified design"] / FRAME, 1))
    for term, claimed in [("value of children", 515), ("intergenerational transfer", 284),
                          ("old age support", 205), ("old-age support", 205),
                          ("wealth flows", 74), ("National Transfer Accounts", 60),
                          ("intergenerational wealth", 33), ("filial support", 7),
                          ("life cycle deficit", 3), ("lifecycle deficit", 1),
                          ("child labour contribution", 1), ("child labor contribution", 0)]:
        log(f"§3 term alone — {term}", claimed, a[f"TERM {term}"])
    for term, claimed in [("value of children", 7083), ("intergenerational transfer", 3176),
                          ("intergenerational wealth", 528), ("filial support", 109)]:
        log(f"§3 term unrestricted — {term}", claimed, a[f"BARE {term}"])
    log("§3 frame without 'value of children'", 607, a["AXIS minus 'value of children'"])
    log("§3 frame without 'old age support' (unchanged)", 1099, a["AXIS minus 'old age support'"])
    log("§3 VOC-survey residue in frame", 191,
        a["HOMONYM VOC-survey residue INSIDE the fertility-restricted frame"])
    log("§3 genetics residue in frame", 1,
        a["HOMONYM genetics residue INSIDE the fertility-restricted frame"])
    log("§3 bequest residue in frame", 33, probe["bequest residue INSIDE the fertility-restricted frame"])
    derived("§3 bequest residue share (3.0%)", 3.0,
            round(100 * probe["bequest residue INSIDE the fertility-restricted frame"] / FRAME, 1))
    log("§3 intergenerational transfer x bequests", 364,
        probe["intergenerational transfer INTERSECT bequests and estates"])
    log("§3 wealth flows unrestricted", 237, probe["wealth flows, unrestricted"])
    log("§3 wealth flows x capital markets", 21, probe["wealth flows INTERSECT capital markets"])
    for term, claimed in [("intergenerational support", 114), ("children as investment", 19),
                          ("net cost of children", 2), ("upward transfers", 2),
                          ("downward transfers", 2), ("economic value of children", 0)]:
        log(f"§3A marginal gain — {term}", claimed, gains[term])

    # ---------------------------------------------------------------- §7 the second channel
    for label, vol, ident, cross in [
            ("pension and social-security expansion (C.3.c owns this corner)", 433, 26, 19),
            ("inheritance and land-title reform", 291, 9, 6),
            ("child labour bans and schooling supply", 46, 11, 2),
            ("filial-responsibility and family-support law", 24, 0, 0)]:
        log(f"§7 volume — {label[:38]}", vol, a[f"CHANNEL2 {label}"])
        log(f"§7 identified — {label[:38]}", ident,
            a[f"CHANNEL2 {label} carrying an identified design"])
        log(f"§7 crossover — {label[:38]}", cross,
            a[f"CHANNEL2 {label} INTERSECT the C.3.f axis (crossover)"])
    log("§7 NTA measurement literature", 425,
        a["HOMONYM National Transfer Accounts alone (measurement by construction)"])

    # ---------------------------------------------------------------- §8 the walls
    for label, ov, pct in [
            ("boundary: C.3.c old-age security (a written chapter)", 162, 15),
            ("boundary: C.2.b price of children (a drafted chapter)", 19, 1.7),
            ("boundary: C.3.a mode of production (an unstarted candidate)", 5, 0.5),
            ("boundary: D.1.b westernization (a drafted chapter)", 1, 0.1)]:
        log(f"§8 overlap — {label[10:44]}", ov, probe[label])
        derived(f"§8 share — {label[10:44]}", pct, round(100 * probe[label] / FRAME, 1)
                if pct != 15 else round(100 * probe[label] / FRAME))
    log("§8 overlap — C.3.d quantity-quality", 21,
        a["BOUNDARY C.3.d quantity-quality (a drafted chapter)"])
    derived("§8 share — C.3.d quantity-quality", 1.9,
            round(100 * a["BOUNDARY C.3.d quantity-quality (a drafted chapter)"] / FRAME, 1))
    log("§8 overlap — A.19", 1,
        a["BOUNDARY A.19 intergenerational transmission of FERTILITY (an unstarted candidate)"])
    log("§8 overlap — Alexandra's compulsory schooling", 5,
        a["BOUNDARY Alexandra's child-labour and compulsory-schooling chapter"])
    derived("§8 outcome-level share (17%)", 17,
            round(100 * a["HOMONYM VOC-survey residue INSIDE the fertility-restricted frame"] / FRAME))
    derived("§3 'value of children' share of frame (47%)", 47,
            round(100 * a["TERM value of children"] / FRAME))

    # ---------------------------------------------------------------- ranking figures from 304
    log("ticket/§1 C.3.f union frame on the probe", 1101, union["C.3.f"])
    log("ticket C.3.f core", 367, sublit["core (pass 1)"])
    log("§13 C.3.a union frame", 1811, union["C.3.a"])

    # ---------------------------------------------------------------- 379: the amended figures
    log("§8 Wall 5 — C.1.a neighbour frame", 6397, w["C.1.a neighbour frame"])
    log("§8 Wall 5 — overlap", 51, w["overlap: C.3.f AND C.1.a"])
    derived("§8 Wall 5 — share of C.3.f (4.6%)", 4.6,
            round(100 * w["overlap: C.3.f AND C.1.a"] / FRAME, 1))
    derived("§8 Wall 5 — share of C.1.a (0.8%)", 0.8,
            round(100 * w["overlap: C.3.f AND C.1.a"] / w["C.1.a neighbour frame"], 1))
    log("§8 Wall 5 — inside the identified subset", 0, w["overlap INSIDE the identified subset"])
    log("§8 Wall 5 — identified frame, reproduced from 376", 18,
        w["C.3.f frame carrying an identified design (376 got 18)"])
    log("§8 Wall 5 — remittances x income", 40, w["row 6 remittances AND C.1.a"])
    log("§8 Wall 5 — inheritance x income", 7, w["row 2 inheritance/land AND C.1.a"])
    log("§8 Wall 5 — labour demand x income", 5, w["row 5 labour-demand x child work AND C.1.a"])
    log("§7 row 5 volume", 19, w["row 5 volume"])
    log("§7 row 5 identified", 1, w["row 5 carrying an identified design"])
    log("§7 row 5 crossover", 1, w["row 5 crossover with the C.3.f axis"])
    log("§7 row 6 volume", 429, w["row 6 volume"])
    log("§7 row 6 identified", 18, w["row 6 carrying an identified design"])
    log("§7 row 6 crossover", 5, w["row 6 crossover with the C.3.f axis"])
    log("§7/§13 row 6 signed on the transfer", 6,
        w["row 6 signed on the TRANSFER (parents named as recipients)"])
    log("§7 row 4 — filial law across eight spellings", 250, w["filial-law union, unrestricted"])
    log("§7 row 4 — 'maintenance of parents' alone", 147, w["spelling 'maintenance of parents'"])
    log("§7 row 4 — with a fertility outcome", 5, w["filial-law union AND a fertility outcome"])
    log("§7 row 4 — with an identified design", 0,
        w["filial-law union AND fertility AND an identified design"])
    for label, claimed in [("pension and social-security expansion (376 measured 26)", 26),
                           ("compulsory schooling reform", 76),
                           ("cash transfer programmes", 78)]:
        log(f"§7 detector control — {label[:34]}", claimed, w[f"DETECTOR {label}"])
    for term, claimed in [("fertility", 840), ("number of children", 211), ("childbearing", 160),
                          ("family size", 160), ("birth rate", 77),
                          ("total fertility rate", 45)]:
        log(f"§3B outcome term — {term}", claimed, w[f"OUTCOME '{term}'"])
    log("§3B 'family size' x household size", 5,
        w["'family size' INTERSECT household-size vocabulary (the worry)"])
    log("§3B 'number of children' x household size", 4,
        w["'number of children' INTERSECT the same"])

    # ---------------------------------------------------------------- 380: the anchor set
    d380 = load("c3f-anchors")
    n = d380["counts"]
    log("§14 inherited confirmed", 14, n["inherited_confirmed"])
    log("§14 inherited total", 14, n["inherited_total"])
    log("§14 hand-named resolved cleanly", 12, n["resolved_ok"])
    log("§14 hand-named total", 21, n["resolved_total"])
    log("§14 recovered on pass 2", 2, n["retry_recovered"])
    log("§14 reviews caught by the author gate", 3, n["book_reviews_caught_by_author_gate"])
    log("§14 reviews caught by the shadow regex", 0, n["book_reviews_caught_by_shadow_regex"])
    versions = sum(1 for r in d380["resolved"] if r["verdict"] == "VERSION_DIFFERS")
    log("§14 usable at a different version", 2, versions)
    derived("§14 usable anchors (30)", 30,
            n["inherited_confirmed"] + n["resolved_ok"] + n["retry_recovered"] + versions)
    derived("§14 unreachable (5)", 5,
            n["book_reviews_caught_by_author_gate"] + (n["retry_total"] - n["retry_recovered"]))

    # ---------------------------------------------------------------- EXTERNAL: C.3.c's verdict
    c3c = C3C.read_text()
    external = [("§4/§5 C.3.c FDT magnitude", "0.0677 births per woman"),
                ("§4 C.3.c FDT share", "2.3% of a three-birth decline"),
                ("§4 C.3.c FDT grade", "| FDT, old-age-security motive | **VERY LOW** |"
                                       .replace(" |", " |")[:44])]
    for label, needle in external:
        checks.append(("EXTERNAL", label, needle, needle if needle in c3c else "NOT FOUND"))

    # ---------------------------------------------------------------- report
    bad = [c for c in checks if c[2] != c[3]]
    for kind, label, claimed, actual in checks:
        mark = "ok  " if claimed == actual else "FAIL"
        print(f"{mark}  {kind:8} {label:56} scope={str(claimed)[:34]:>34}  log={str(actual)[:34]}")
    print(f"\n{len(checks) - len(bad)}/{len(checks)} figures in {SCOPE.name} match their sources.")
    if bad:
        print("\nThe scope document is STALE. Update the prose to the log, not the other way "
              "round:", file=sys.stderr)
        for kind, label, claimed, actual in bad:
            print(f"  [{kind}] {label}: scope says {claimed}, source says {actual}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
