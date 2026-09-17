#!/usr/bin/env python3
"""
406 — assert that every number in A.6's stage-2 scope document is the number `404` measured.

Why this exists. The scope doc's provenance section claims no number in it is retyped from memory
(`generate-result-tables-never-retype`). That claim is worth nothing unless something checks it, and
the numbers were in fact hand-transcribed from a console run. This re-reads them from the JSON and
fails loudly on any mismatch, including the derived percentages and marginal gains, which are the
easiest things to get wrong by arithmetic rather than by transcription.

Run from the repo root. Exit 0 means the document agrees with the measurements.
"""
import json, pathlib, re, sys

STAMP = "2026-09-17"
A6 = pathlib.Path(f"literature/search-logs/a6-term-diagnostics-{STAMP}.json")
DOC = pathlib.Path("literature/search-logs/stigma-reduction-contraception-abortion-search-scope.md")

c = json.loads(A6.read_text())["counts"]
# Whitespace-folded, because the required phrasings are prose and markdown wraps them across lines;
# a line break inside a required sentence is not a missing sentence.
doc = re.sub(r"\s+", " ", DOC.read_text())
fails = []


def want(label, expected, note=""):
    got = c.get(label)
    if got != expected:
        fails.append(f"{label!r}: json={got} doc asserts {expected} {note}")
    return got


def in_doc(s, why):
    if s not in doc:
        fails.append(f"doc is missing {s!r} — {why}")


# --- the frame and the block decomposition -----------------------------------------------------
frame = want("reproduce A.6 pass 4 union frame (09-13 recorded 680)", 668)
want("stigma block AND outcome, object block dropped", 3292)
want("object block AND outcome, stigma block dropped", 47523)
want("stigma AND object, outcome block dropped", 4875)
want("frame with the registered construct restored", 1225)
want("frame with registered construct AND births in the outcome axis", 2338)
want("stigma block widened by ALL candidates", 1666)
want("re-check A.3 union frame (09-13 recorded 727)", 719)
want("re-check C.3.a union frame (09-13 recorded 1811)", 1808)
want("control: C.2.c housing frame (a written chapter)", 205)
want("reproduce stigma unrestricted (09-13 recorded 202130)", 202510)
want("reproduce A.6 pass 1 narrow (09-13 recorded 12)", 12)

# the multipliers quoted in the section 3 table, to one decimal place
for label, mult in [("stigma block AND outcome, object block dropped", 4.9),
                    ("stigma AND object, outcome block dropped", 7.3),
                    ("object block AND outcome, stigma block dropped", 71.1)]:
    got = round(c[label] / frame, 1)
    if got != mult:
        fails.append(f"multiplier for {label!r}: computed {got}, doc asserts {mult}")

# --- marginal gains quoted in 3A and 3B --------------------------------------------------------
GAINS = {"stigma + legitimation": 166, "stigma + normalization": 202,
         "stigma + normalisation": 27, "stigma + social acceptability": 41,
         "stigma + disapproval": 130, "stigma + moral acceptability": 2,
         "stigma + legitimacy": 53, "stigma + social norms": 274,
         "stigma + secrecy": 31, "stigma + embarrassment": 33,
         "stigma + religious opposition": 26, "stigma + husband opposition": 12,
         "stigma + opposition to family planning": 22, "stigma + social sanction": 13,
         "stigma + community disapproval": 1, "stigma + normative pressure": 6,
         "outcome + parity": 34, "outcome + births": 496,
         "outcome + completed fertility": 0, "outcome + number of children ever born": 0}
for label, gain in GAINS.items():
    if c.get(label) is None:
        fails.append(f"{label!r} missing from json")
    elif c[label] - frame != gain:
        fails.append(f"gain for {label!r}: computed {c[label]-frame}, doc asserts {gain}")

want("outcome narrow instead of wide", 601)
if c["outcome narrow instead of wide"] - frame != -67:
    fails.append("narrow-axis delta is not -67")

# object block is frozen because ALL its additions gain little, and no single one exceeds +24
if c["object block widened by ALL candidates"] - frame != 62:
    fails.append("object ALL gain is not +62")
obj_max = max(v - frame for k, v in c.items() if k.startswith("object + "))
if obj_max != 24:
    fails.append(f"largest single object gain is {obj_max}, doc asserts 24")

# --- composition of the frame ------------------------------------------------------------------
want("frame AND identified-design markers", 12)
want("frame AND qualitative markers", 189)
want("level: realized fertility", 58)
want("level: intention or desire", 21)
want("level: contraceptive use as the outcome", 122)
want("level: attitude or scale measurement", 10)
want("level without our outcome axis: contraceptive use as the outcome", 479)

# the 357 / 74.5% claim in ruling 2
lost = c["level without our outcome axis: contraceptive use as the outcome"] - \
       c["level: contraceptive use as the outcome"]
if lost != 357:
    fails.append(f"use records outside the axis: computed {lost}, doc asserts 357")
if round(100 * lost / c["level without our outcome axis: contraceptive use as the outcome"], 1) != 74.5:
    fails.append("the 74.5% share in ruling 2 does not recompute")

# --- walls, both sides, and the identified counts -----------------------------------------------
WALLS = {"A.2": (60, 5428, 1, 9.0, 1.1), "A.3": (2, 535, 0, 0.3, 0.4),
         "A.4": (57, 2121, 1, 8.5, 2.7), "A.5": (81, 5944, 3, 12.1, 1.4),
         "D.1.a": (6, 1361, 0, 0.9, 0.4), "B.5": (51, 16273, 3, 7.6, 0.3)}
for code, (ov, their, ident, pct_ours, pct_theirs) in WALLS.items():
    want(f"wall {code} overlap with our frame", ov)
    want(f"wall {code} neighbour frame", their)
    want(f"wall {code} overlap AND identified", ident)
    if round(100 * c[f"wall {code} overlap with our frame"] / frame, 1) != pct_ours:
        fails.append(f"wall {code}: % of our frame does not recompute as {pct_ours}")
    if round(100 * c[f"wall {code} overlap with our frame"] /
             c[f"wall {code} neighbour frame"], 1) != pct_theirs:
        fails.append(f"wall {code}: % of their frame does not recompute as {pct_theirs}")

# PI call 4 asserts 3 of the 5 identified wall records sit in A.5, B.5 excluded as a homonym
substantive = sum(c[f"wall {k} overlap AND identified"] for k in ["A.2", "A.3", "A.4", "A.5", "D.1.a"])
if substantive != 5 or c["wall A.5 overlap AND identified"] != 3:
    fails.append(f"PI call 4: substantive identified wall records = {substantive}, A.5 holds "
                 f"{c['wall A.5 overlap AND identified']}; doc asserts 3 of 5")

# --- homonyms -----------------------------------------------------------------------------------
for label, n, pct in [("HIV and sexual health", 148, 22.2), ("mental illness", 92, 13.8),
                      ("obesity and body weight", 19, None),
                      ("leprosy tuberculosis and infectious disease", 14, None)]:
    want(f"homonym: {label}", n)
    if pct is not None and round(100 * c[f"homonym: {label}"] / frame, 1) != pct:
        fails.append(f"homonym {label}: share does not recompute as {pct}")

# --- the required phrasings the estimand gate and the house form demand -------------------------
for s, why in [("**No production query has been run, no anchor resolved, and no record screened.**",
                "the measured-here-and-not paragraph"),
               ("A count is not an evidence base", "same paragraph"),
               ("Every clause is load-bearing", "section 1"),
               ("The reason for ruling on fertility anyway is arithmetic, not taste",
                "section 2 ruling form"),
               ("Predicted now, so that it is a prediction and not a rationalisation later",
                "section 12 pooling prediction"),
               ("generate-result-tables-never-retype", "provenance closing"),
               ("empty-cell-is-the-result", "the empty-cell commitment"),
               ("The small numbers are not reassurance", "section 8 inherited C.3.d finding")]:
    in_doc(s, why)

if fails:
    print(f"{len(fails)} MISMATCH(ES) between the scope doc and the measurements:\n", file=sys.stderr)
    for f in fails:
        print(f"  - {f}", file=sys.stderr)
    sys.exit(1)
print(f"scope doc agrees with {A6.name}: {len(GAINS)} gains, {len(WALLS)} walls (both sides), "
      f"frame {frame}, all required phrasings present")
