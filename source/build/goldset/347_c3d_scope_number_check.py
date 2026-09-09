#!/usr/bin/env python3
"""
347 — assert every number quoted in the C.3.d scope document against the logs it came from.

Why this exists. `generate-result-tables-never-retype`: A.17's hand-typed demographic-significance
table had the right offsets and the wrong baselines, and nothing caught it because nothing checked
it. A scope document is prose and cannot be fully generated, but the numbers embedded in it can be
ASSERTED against the JSON the scripts wrote, and that assertion can be re-run whenever a log is
regenerated. This is the cheap half of that lesson: not generation, but a failing test.

Run it after any re-run of 344, 345 or 346. A mismatch means the scope is stale, not that the log
is wrong -- the log is the record, the scope quotes it.

Usage: python3 source/build/goldset/347_c3d_scope_number_check.py
Exit 0 = every quoted figure matches. Exit 1 = at least one does not.
"""
import json, pathlib, sys

LOGS = pathlib.Path("literature/search-logs")
DATE = "2026-09-09"
SCOPE = LOGS / "quantity-quality-tradeoff-search-scope.md"


def rows(name):
    p = LOGS / f"{name}-{DATE}.json"
    if not p.exists():
        sys.exit(f"missing log {p} — re-run the script that writes it before checking the scope")
    d = json.load(open(p))
    return d, {r["label"]: r["n"] for r in d["rows"]}


def main():
    d344, a = rows("c3d-term-diagnostics")
    d345, b = rows("c3d-outcome-axis")
    d346, c = rows("c3d-forward-channel-walls")

    # (what the scope says, the value it says, where that value must come from)
    checks = [
        ("§1/§3 frame", 762, b["CONTROL C.3.d frame (344's baseline: 762)"]),
        ("§3 quantity-quality", 494, a["TERM quantity-quality"]),
        ("§3 child quality", 243, a["TERM child quality"]),
        ("§3 quantity quality tradeoff", 95, a["TERM quantity quality tradeoff"]),
        ("§3 child investment", 40, a["TERM child investment"]),
        ("§3 human capital of children", 31, a["TERM human capital of children"]),
        ("§3 sibsize", 27, a["TERM sibsize"]),
        ("§3 bare quantity-quality", 8154, a["BARE quantity-quality"]),
        ("§3 bare child quality", 793, a["BARE child quality"]),
        ("§3 bare quantity quality tradeoff", 162, a["BARE quantity quality tradeoff"]),
        ("§3 bare child investment", 125, a["BARE child investment"]),
        ("§3 bare human capital of children", 182, a["BARE human capital of children"]),
        ("§3 bare sibsize", 69, a["BARE sibsize"]),
        ("§3 dropping child quality costs", 176, 762 - a["AXIS minus 'child quality'"]),
        ("§3 dropping child investment costs", 30, 762 - a["AXIS minus 'child investment'"]),
        ("§3 non-human residue in frame", 43,
         b["non-human residue INSIDE the fertility-restricted frame"]),
        ("§3 outcome term 'fertility'", 616, b["OUTCOME fertility"]),
        ("§3 its non-human share", 42, b["OUTCOME fertility -- non-human marked"]),
        ("§2 forward arm as 345 measured it", 8,
         b["FORWARD with a returns-to-skill exposure attached"]),
        ("§2 backward arm", 200, b["BACKWARD axis AND child-outcome vocabulary"]),
        ("§2 carrying both outcomes", 98, b["BOTH axis AND fertility AND child-outcome"]),
        ("§2 backward with identified design", 35,
         b["BACKWARD with an identified family-size design attached"]),
        ("§3/§4 twins x child outcomes outside the axis", 1562,
         b["the family-size-shock literature that does NOT use C.3.d vocabulary, backward"]),
        ("§3 family-size-shock records", 4690,
         a["ESTIMAND family-size shocks (twins / sex composition)"]),
        ("§3 …of which use a C.3.d term", 61,
         a["ESTIMAND family-size shocks (twins / sex composition) INTERSECT the C.3.d axis"]),
        ("§2/§3 forward arm on ch1 inside the frame", 16,
         c["CHANNEL 1 forward arm, inside the C.3.d frame (345 got 8)"]),
        ("§3 forward arm on ch1 unrestricted", 231,
         c["CHANNEL 1 forward arm, NOT restricted to the C.3.d frame"]),
        ("§3 channel-2 axis x fertility", 770, c["channel-2 axis AND fertility"]),
        ("§3 …of which in the C.3.d frame", 15,
         c["channel-2 axis AND fertility AND the C.3.d frame"]),
        ("§3 …of which in channel-1 vocabulary", 8,
         c["channel-2 axis AND fertility AND channel-1 vocabulary"]),
        ("§7 …carrying an identified-design marker", 35,
         c["channel-2 axis AND fertility AND an identified-design marker"]),
        ("§13/ruling 3 SBTC on its own vocabulary", 9,
         b["SBTC2 that same axis AND a fertility outcome"]),
        ("§13/ruling 3 demand for skill", 24, b["SBTC2 demand for skill AND fertility"]),
        ("§13/ruling 3 as unified growth", 85,
         b["SBTC2 unified growth framing of the same shock"]),
        ("§13/ruling 3 as a trade shock", 88,
         b["SBTC2 trade shock as the skill shock AND fertility"]),
    ]

    # §7 volumes and §3A marginal gains, read straight out of the structured blocks.
    ch2 = {x["label"]: x for x in d346["channel2"]}
    for label, claimed in [("trade / import competition", 88),
                           ("technology adoption / automation exposure", 27),
                           ("schooling supply expansion", 188),
                           ("historical industrialization and human capital", 275),
                           ("local labour-demand shocks to skill", 23),
                           ("occupational structure / white-collar shift", 329)]:
        checks.append((f"§7 volume — {label}", claimed, ch2[label]["arm"]))
    for label, claimed in [("trade / import competition", 0),
                           ("technology adoption / automation exposure", 0),
                           ("schooling supply expansion", 2),
                           ("historical industrialization and human capital", 11),
                           ("local labour-demand shocks to skill", 1),
                           ("occupational structure / white-collar shift", 3)]:
        checks.append((f"§7 ch1 crossover — {label}", claimed, ch2[label]["overlap_ch1"]))

    walls = {w["label"].split(" --")[0].split(" -- ")[0]: w for w in d346["walls"]}
    for key, nb, ov in [
            ("C.2.f reference standard", 718, 9),
            ("C.2.e female wage / opportunity cost of mother's time", 1738, 13),
            ("C.2.b direct cost of children", 326, 12),
            ("C.1.a income effect", 421, 20),
            ("A.1 child mortality and replacement", 7416, 38),
            ("A.12 twinning as an accounting identity (drafted) vs as an instrument", 5550, 60),
            ("Alexandra's compulsory schooling / child labour laws", 364, 6),
            ("C.3.f wealth flows / value of children", 859, 11),
            ("D.2.d intensive parenting norms", 40, 0)]:
        w = next(v for k, v in walls.items() if k.startswith(key[:28]))
        checks.append((f"§8 wall {key[:34]} — neighbour frame", nb, w["neighbour_frame"]))
        checks.append((f"§8 wall {key[:34]} — overlap", ov, w["overlap"]))

    gains = {m["term"]: m["gain"] for m in d344["marginal"]}
    for term, claimed in [("parental investment", 332), ("human capital investment", 306),
                          ("investment in children", 182), ("sibship size", 182),
                          ("quality-quantity", 138), ("resource dilution", 62),
                          ("family size and educational attainment", 42),
                          ("child human capital", 14), ("dilution of resources", 2),
                          ("education-fertility tradeoff", 0)]:
        checks.append((f"§3A marginal gain — {term}", claimed, gains[term]))

    bad = [(l, s, a_) for l, s, a_ in checks if s != a_]
    for l, s, a_ in checks:
        print(f"{'ok  ' if s == a_ else 'FAIL'}  {l:58} scope={s:>6}  log={a_:>6}")
    print(f"\n{len(checks) - len(bad)}/{len(checks)} figures in {SCOPE.name} match their logs.")
    if bad:
        print("\nThe scope document is STALE. Update the prose to the log, not the other way round:",
              file=sys.stderr)
        for l, s, a_ in bad:
            print(f"  {l}: scope says {s}, log says {a_}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
