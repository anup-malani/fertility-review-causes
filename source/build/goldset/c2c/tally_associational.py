#!/usr/bin/env python3
"""Direction-of-association tally across the C.2.c associational stratum (TICK-056).

WHY THIS, RATHER THAN 48 MORE PDFs. The 48 outstanding records are all ASSOCIATIONAL. They cannot
enter the pooled estimates -- the chapter is explicit that they document association without
identification. What the chapter DOES claim about them is that they exist in quantity and that the
literature is dominated by them. That claim is currently unquantified in one respect that matters:
which way they point.

A vote count over the associational stratum is not a meta-analysis and must never be presented as
one. Vote counting ignores precision and sample size and is biased toward whatever is statistically
detectable. But it answers a question the chapter should answer: is the large uncontrolled literature
broadly consistent with the identified estimates, or does it point somewhere else? If it is broadly
consistent, that is weak corroboration. If it is not, the identified core is an outlier and the
chapter must say so.

Direction is read from title + abstract. Records whose direction is not stated there are counted as
UNCLEAR and reported, not dropped -- an unclear share is itself a finding about reporting practice.
"""
import csv
import json
import re
from collections import Counter

FRAME = "literature/search-logs/housing-costs-screen-pass2.json"
GATE = "extraction/housing-costs-ra-gate.csv"
OUT = "extraction/housing-costs-associational-tally.csv"

NEG = re.compile(r"(negative(ly)? (effect|impact|associat|relat|influenc)|reduc\w+ (the )?(fertility|birth|childbear)|"
                 r"(fertility|birth ?rate|childbear\w*)[^.]{0,40}(decline|decrease|lower|fall|drop|inhibit|suppress)|"
                 r"discourag\w+ (fertility|childbear|birth)|crowd(ing)?[- ]out|"
                 r"adverse (effect|influence) on (fertility|birth)|dampen)", re.I)
POS = re.compile(r"(positive(ly)? (effect|impact|associat|relat|influenc)|increas\w+ (the )?(fertility|birth|childbear|likelihood of (giving )?birth)|"
                 r"(fertility|birth ?rate|childbear\w*)[^.]{0,40}(increase|rise|higher|raise|promot|boost))", re.I)
MIXED = re.compile(r"(mixed|heterogen\w+ (effect|result)|differ\w+ by (tenure|ownership|region|group)|"
                   r"varies? (across|by)|non-?linear|threshold effect|inverted[- ]u|u-?shaped)", re.I)

gate = {r["openalex"]: r for r in csv.DictReader(open(GATE)) if r["ra_verdict"].startswith("KEEP")}
frame = {r["openalex"]: r for r in json.load(open(FRAME))}

rows = []
for wid, g in gate.items():
    rec = frame.get(wid, {})
    text = f"{g['title']} {rec.get('abstract', '')}"
    has_abs = bool(rec.get("abstract"))
    neg, pos, mixed = bool(NEG.search(text)), bool(POS.search(text)), bool(MIXED.search(text))
    if mixed or (neg and pos):
        d = "MIXED/CONDITIONAL"
    elif neg:
        d = "NEGATIVE"
    elif pos:
        d = "POSITIVE"
    else:
        d = "UNCLEAR (no direction stated)" if has_abs else "UNCLEAR (no abstract)"
    rows.append({"work_id": wid, "doi": g["doi"], "year": g["year"], "venue": g["venue"],
                 "title": g["title"], "direction": d, "has_abstract": has_abs,
                 "basis": "title+abstract"})

with open(OUT, "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
    w.writeheader()
    w.writerows(rows)

c = Counter(r["direction"] for r in rows)
print(f"associational + primary stratum tally -> {OUT}")
print(f"records: {len(rows)}\n")
for k, n in c.most_common():
    print(f"  {n:>3}  {k}")
determinate = sum(n for k, n in c.items() if not k.startswith("UNCLEAR"))
neg = c.get("NEGATIVE", 0)
print(f"\ndeterminate direction: {determinate}/{len(rows)}")
if determinate:
    print(f"of those, NEGATIVE: {neg}/{determinate} = {neg/determinate:.0%}")
