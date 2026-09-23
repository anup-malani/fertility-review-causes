#!/usr/bin/env python3
"""
88 — Candidate scout for TICK-091 selection: a cheap production-frame count for the leading
genuinely-unstarted small hypotheses, to pick the smallest-first honestly BEFORE building the full
A.14 frame probe (89). Counting only, ~1 request per candidate.

This is the reconnaissance step, not the measurement. The authoritative frame measurement (with the
registered-construct completeness test and the walls) is `89_a14_frame_probe.py`; this script only
ranks candidates so the full probe is spent on the right one. Result (2026-09-23):
A.14 = 373 << B.2 4,475 < A.13 5,078 < B.3 9,442 < A.15 15,325 < B.4 21,710 < A.16 25,214.
A.14 wins by an order of magnitude; the full probe then confirmed its honest frame at 769.

Mirrors 52_c2h's count() (curl, title_and_abstract.search, refusals != zeros).
"""
import json, subprocess, urllib.parse, time, pathlib

MAILTO = "shravanh@uchicago.edu"
BASE = "https://api.openalex.org/works"
CACHE = pathlib.Path("temp/a14-candidate-scout-cache.json")


def _api_key():
    try:
        for line in open(".env"):
            if line.startswith("OPENALEX_API_KEY="):
                return line.split("=", 1)[1].strip().strip('"') or None
    except FileNotFoundError:
        pass
    return None


KEY = _api_key()
PACE = 0.25 if KEY else 1.25
cache = json.loads(CACHE.read_text()) if CACHE.exists() else {}


def count(q):
    if q in cache:
        return cache[q]
    url = (f"{BASE}?filter=title_and_abstract.search:{urllib.parse.quote(q, safe='')}"
           f"&per_page=1&mailto={MAILTO}")
    if KEY:
        url += f"&api_key={KEY}"
    p = subprocess.run(["curl", "-s", "-S", "--max-time", "60", url], capture_output=True, text=True)
    if p.returncode != 0:
        return None
    try:
        d = json.loads(p.stdout)
    except json.JSONDecodeError:
        return None
    if "error" in d:
        return None
    n = d.get("meta", {}).get("count")
    if n is not None:
        cache[q] = n
        CACHE.parent.mkdir(parents=True, exist_ok=True)
        CACHE.write_text(json.dumps(cache, indent=1, sort_keys=True))
        time.sleep(PACE)
    return n


FERT = ('("fertility" OR "childbearing" OR "birth rate" OR "total fertility rate" OR "childlessness" '
        'OR "fecundity" OR "time to pregnancy" OR "subfertility" OR "infertility")')

CANDS = {
    "A.16 paternal-age-sperm-quality":
        '("paternal age" OR "sperm count" OR "sperm quality" OR "semen quality" OR "sperm concentration" OR "male fecundity")',
    "B.4 obesity-metabolic-subfecundity":
        '("obesity" OR "body mass index" OR "metabolic syndrome" OR "overweight")',
    "A.13 breastfeeding-lactational-amenorrhea":
        '("breastfeeding" OR "lactational amenorrhea" OR "lactational amenorrhoea" OR "breast feeding")',
    "A.14 coital-frequency-fecundability":
        '("coital frequency" OR "sexual frequency" OR "frequency of intercourse" OR "coital rate")',
    "A.15 maternal-age-fecundity-decline":
        '("maternal age" OR "advanced maternal age" OR "ovarian reserve" OR "ovarian aging" OR "ovarian ageing")',
    "B.3 infectious-disease-sterility":
        '("sexually transmitted infection" OR "pelvic inflammatory disease" OR "gonorrhea" OR "gonorrhoea" OR "chlamydia" OR "tubal infertility")',
    "B.2 endocrine-disruptors":
        '("endocrine disruptor" OR "endocrine disrupting" OR "phthalate" OR "bisphenol")',
}


def main():
    print(f"api_key={bool(KEY)}  outcome axis includes fecundity/TTP/subfertility\n")
    rows = []
    for name, topic in CANDS.items():
        n = count(f"{topic} AND {FERT}")
        rows.append((name, n))
        print(f"  {('REFUSED' if n is None else format(n, ',')):>10}  {name}")
    print("\n--- ranked smallest-first ---")
    for name, n in sorted(rows, key=lambda r: (r[1] is None, r[1] if r[1] is not None else 0)):
        print(f"  {('REFUSED' if n is None else format(n, ',')):>10}  {name}")


if __name__ == "__main__":
    main()
