#!/usr/bin/env python3
"""338 — C.2.f: the full chain is NOT empty. Scope §4's join was a vocabulary artefact.

Scope §4 reported the mechanism's conjunction -- inequality -> required investment per child ->
fertility -- as returning ~2 records, and concluded that C.2.f should expect an empty primary cell
and an UNEVALUATED verdict. That conclusion is retracted here.

How it was found. The production-query calibration (337) put 13 control anchors in the `mechanism`
arm and recalled 2. Testing the recall mechanism against those controls showed it working (the
outcome axis alone returns each of them), so the controls genuinely lacked the arm's vocabulary.
Reading them was the fix: they are not status-competition records at all, they are SHADOW EDUCATION
and PRIVATE TUTORING records with fertility outcomes, mostly from China, South Korea and Hong Kong.

That is `empty-cell-needs-second-channel` exactly -- C.3.g's "no natural experiment exists" was two
missing words -- and `policy-literatures-indexed-in-local-vocabulary`, worth +40% of A.23's frame.
The full chain is written in the East Asian education-competition vocabulary, not in the
economics-of-inequality vocabulary §4 probed it with.

It also lands scope §7 row 7, which was pre-registered as one of only two places where the
positional mechanism separates from the return: China's 2021 "double reduction" private-tutoring ban
is a policy shock to required investment per child, with fertility outcomes attached.

`"involution"` (Chinese *neijuan*, the popular term for the competition) is REFUSED as a search term
and the refusal is recorded rather than left implicit: it returns 398 records against the fertility
axis and they are the veterinary and obstetric homonym -- uterine involution in dairy cattle, thymic
involution in pregnancy. 7,379 records intersect the uterine/thymic vocabulary. This is
`homonym-shares-outcome-vocabulary`: the homonym lives inside the outcome literature itself.
"""
import json, subprocess, sys, urllib.parse, time, datetime, pathlib

MAILTO = "shravanh@uchicago.edu"
FERT = ('("fertility" OR "childbearing" OR "birth rate" OR "total fertility rate" '
        'OR "family size" OR "number of children" OR "fertility intention")')


def _key():
    for l in open(".env"):
        if l.startswith("OPENALEX_API_KEY="):
            return l.split("=", 1)[1].strip() or None
    return None


KEY = _key()


class Refused(Exception):
    pass


def count(q, per=1):
    u = ("https://api.openalex.org/works?filter=title_and_abstract.search:"
         + urllib.parse.quote(q, safe='') + f"&per_page={per}&mailto={MAILTO}")
    if KEY:
        u += f"&api_key={KEY}"
    for _ in range(3):
        p = subprocess.run(["curl", "-s", "--max-time", "50", u], capture_output=True, text=True)
        if p.returncode != 0:
            raise Refused(f"curl {p.returncode}")
        d = json.loads(p.stdout)
        if "error" not in d:
            return d["meta"]["count"], [w.get("display_name") for w in d.get("results", [])]
        time.sleep(2.0)
    raise Refused(d.get("message", "")[:120])


PROBES = [
    ("§4's original full-chain probe, economics-of-inequality vocabulary",
     '("income inequality" OR "Gini" OR "top income share") AND '
     '("parental investment" OR "child investment" OR "educational spending") AND ' + FERT),
    ("shadow education / private tutoring / cram school × fertility",
     '("shadow education" OR "private tutoring" OR "cram school") AND ' + FERT),
    ("education competition × fertility",
     '("education competition" OR "educational competition" OR "academic competition") AND ' + FERT),
    ("tutoring ban / double reduction × fertility (scope §7 row 7)",
     '("private tutoring ban" OR "double reduction" OR "tutoring policy") AND ' + FERT),
    ("educational burden / education expenditure × fertility — HOMONYM UNCHECKED",
     '("educational burden" OR "burden of education" OR "education expenditure") AND ' + FERT),
]
REFUSED_TERMS = [
    ("involution (neijuan) × fertility — REFUSED, veterinary/obstetric homonym",
     '"involution" AND ' + FERT),
    ("involution ∩ uterine/thymic/mammary/postpartum — the homonym's size",
     '"involution" AND ("uterine" OR "thymic" OR "mammary" OR "postpartum")'),
]


def main():
    date = datetime.date.today().isoformat()
    rows, errs = [], []
    print("== the second channel ==")
    for lab, q in PROBES:
        try:
            n, _ = count(q); rows.append((lab, q, n, "kept")); print(f"  {n:>6,}  {lab}")
        except Refused as e:
            errs.append((lab, str(e))); print(f"  REFUSED {lab}: {e}", file=sys.stderr)
        time.sleep(0.3)
    print("\n== refused terms, recorded rather than left implicit ==")
    for lab, q in REFUSED_TERMS:
        try:
            n, _ = count(q); rows.append((lab, q, n, "refused")); print(f"  {n:>6,}  {lab}")
        except Refused as e:
            errs.append((lab, str(e)))
        time.sleep(0.3)
    try:
        _, titles = count('("shadow education" OR "private tutoring" OR "cram school") AND ' + FERT, per=10)
    except Refused:
        titles = []

    out = pathlib.Path("literature/search-logs")
    (out / f"c2f-second-channel-vocabulary-{date}.json").write_text(json.dumps(
        {"date": date, "script": "338_c2f_second_channel_vocabulary.py",
         "rows": [{"label": l, "query": q, "n": n, "status": s} for l, q, n, s in rows],
         "sample_titles": titles, "refused": errs}, indent=2))
    L = [f"# C.2.f second-channel vocabulary — {date}", "",
         "Generated by `source/build/goldset/338_c2f_second_channel_vocabulary.py`. Do not edit by hand.", "",
         "**Scope §4's \"the join is empty\" finding is RETRACTED.** The full chain is written in the",
         "East Asian education-competition vocabulary, which §4 did not probe.", "",
         "| n | probe | status |", "|---|---|---|"]
    L += [f"| **{n:,}** | {l} | {s} |" for l, q, n, s in rows]
    L += ["", "## Sample titles from the recovered cloud", ""]
    L += [f"- {t}" for t in titles if t]
    L += ["", "No refused requests." if not errs else "## REFUSED\n\n" +
          "\n".join(f"- {l}: {e}" for l, e in errs)]
    (out / f"c2f-second-channel-vocabulary-{date}.md").write_text("\n".join(L) + "\n")
    print(f"\nwrote literature/search-logs/c2f-second-channel-vocabulary-{date}.{{json,md}}")
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main())
