#!/usr/bin/env python3
"""276 — C.3.e Arm S survival probe (TICK-077, PI Call 1).

The question: C.3.c (old-age security) is already written and its chapter claims
"money in a bank, an insurance policy" among its substitutes. Wall 1 splits the asset
motive by WHICH RISK is insured — longevity to C.3.c, within-life income and health
risk to C.3.e. If the asset-motive literature is overwhelmingly old-age framed, Arm S
is C.3.c's and C.3.e is a one-arm liquidity chapter with PM and FDT out of scope.

This measures that share instead of asserting it. Every term is counted ALONE as well
as inside its block, because a block count is a block of assumptions: one dense term
can carry an axis and make an empty one look populated (frame-growth-is-not-frame-gain).

Notes carried from earlier chapters, all of which bite here:
  - a comma in a filter VALUE is fatal and %2C does NOT save it; quote the value.
  - a phrase beginning "not" parses as boolean NOT and silently returns the
    unrestricted count; none is used here, and the assertion below enforces it.
  - stopwords are dropped inside quoted phrases, so "no future"=="future".
  - `?` is a wildcard and returns a 200 whose body is an error, which reads as an
    empty literature unless meta.count is checked. oa() checks it.

Usage: python3 276_c3e_arm_s_probe.py
"""
import json, re, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "literature/search-logs/credit-constraints-arm-s-probe.json"
KEY = next((l.split("=", 1)[1].strip() for l in (ROOT / ".env").read_text().splitlines()
            if l.startswith("OPENALEX_API_KEY=")), "")
MAILTO = "shravanh@uchicago.edu"


def oa_count(filter_value):
    args = ["curl", "-s", "-G", "https://api.openalex.org/works",
            "--data-urlencode", f"filter={filter_value}",
            "--data-urlencode", "per-page=1", "--data-urlencode", "select=id",
            "--data-urlencode", f"api_key={KEY}", "--data-urlencode", f"mailto={MAILTO}"]
    r = subprocess.run(args, capture_output=True, text=True, timeout=90)
    try:
        d = json.loads(r.stdout)
    except json.JSONDecodeError:
        return None, "non-JSON body"
    if "meta" not in d or d["meta"].get("count") is None:
        return None, (d.get("message") or "query refused")[:120]
    return d["meta"]["count"], None


def phrase(p):
    assert not p.lower().startswith("not "), f"leading 'not' parses as boolean NOT: {p}"
    assert "?" not in p and "!" not in p, f"wildcard/negation char in {p}"
    return f'"{p}"'


def block(terms):
    return "(" + " OR ".join(phrase(t) for t in terms) + ")"


FERT = ["fertility", "birth rate", "childbearing", "number of children", "family size"]

AXES = {
    "oldage": ["old age security", "old-age security", "old age support", "pension",
               "retirement", "old age insurance"],
    "withinlife_risk": ["children as insurance", "insurance motive", "consumption smoothing",
                        "risk sharing", "crop insurance", "health insurance",
                        "income risk", "precautionary saving"],
    "financial_access": ["financial inclusion", "bank branch", "microfinance", "microcredit",
                         "savings account", "access to credit", "credit access",
                         "financial development"],
    "borrowing_terms": ["credit constraint", "liquidity constraint", "borrowing constraint",
                        "down payment", "loan-to-value", "mortgage credit", "credit supply",
                        "interest rate"],
}


def main():
    res = {"per_term": {}, "blocks": {}, "cross": {}}
    fert = block(FERT)

    for axis, terms in AXES.items():
        for t in terms:
            n, err = oa_count(f"title_and_abstract.search:{phrase(t)} AND {fert}")
            res["per_term"][f"{axis}::{t}"] = {"n": n, "error": err}
            print(f"  {axis:18s} {t:28s} {n if n is not None else 'ERR ' + str(err)}")
        n, err = oa_count(f"title_and_abstract.search:{block(terms)} AND {fert}")
        res["blocks"][axis] = {"n": n, "error": err}
        print(f"* BLOCK {axis:18s} {n}\n")

    # The decisive cross-tab: of the within-life-risk records, how many also carry
    # old-age vocabulary? That share is the part Wall 1 hands to C.3.c.
    for a in ("withinlife_risk", "financial_access", "borrowing_terms"):
        n, err = oa_count(
            f"title_and_abstract.search:{block(AXES[a])} AND {block(AXES['oldage'])} AND {fert}")
        tot = res["blocks"][a]["n"]
        res["cross"][f"{a}_AND_oldage"] = {"n": n, "of": tot,
                                           "share": (round(n / tot, 3) if n is not None and tot else None),
                                           "error": err}
        print(f"CROSS {a:18s} AND oldage = {n} of {tot} "
              f"({'' if not tot or n is None else str(round(100*n/tot,1)) + '%'})")

    OUT.write_text(json.dumps(res, indent=2))
    print(f"\nwritten: {OUT}")


if __name__ == "__main__":
    main()
