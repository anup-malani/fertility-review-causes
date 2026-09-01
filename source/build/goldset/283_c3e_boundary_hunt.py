#!/usr/bin/env python3
"""283 — C.3.e: hunt for a boundary-spanning design. TICK-077.

The composite stratum looks empty: ten hand-picked financial-access designs, and none of the
six read so far estimates a fertility outcome. But counting the studies that failed is the
weak version of the question. ONE study that puts a financial-access exposure and a fertility
outcome in the same identified design would carry the stratum by itself, and hunting for it
beats enumerating the misses.

TWO CHANNELS, scored identically, because a null is worth something only if the channels fail
for unrelated reasons:
  A. TERM channel  — the composite exposure axis x the fertility outcome axis, queried directly.
  B. PROVENANCE channel — the 3,976-record snowball pool, which was built from citations and
     owes nothing to the term vocabulary.
A study found by both is corroborated; a study found by only one tells you which channel is
weak. Overlap is reported rather than dissolved by dedup.

Scoring is on the ABSTRACT and is a triage, not a screen. The identification list includes bare
"experiment" and "experimental": an earlier chapter's IDENT list omitted them and scored a paper
titled *Experimental Evidence* as unidentified.

Usage: python3 283_c3e_boundary_hunt.py
"""
import json, re, subprocess, sys, time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
LOGS = ROOT / "literature" / "search-logs"
OUT = LOGS / "credit-constraints-boundary-hunt.json"
KEY = next((l.split("=", 1)[1].strip() for l in (ROOT / ".env").read_text().splitlines()
            if l.startswith("OPENALEX_API_KEY=")), "")
SELECT = ("id,doi,title,publication_year,type,cited_by_count,primary_location,"
          "authorships,abstract_inverted_index")


def get(params, tries=3):
    args = ["curl", "-sS", "--max-time", "150", "-G", "https://api.openalex.org/works"]
    for k, v in params:
        args += ["--data-urlencode", f"{k}={v}"]
    args += ["--data-urlencode", f"api_key={KEY}",
             "--data-urlencode", "mailto=shravanh@uchicago.edu"]
    for a in range(tries):
        r = subprocess.run(args, capture_output=True, text=True)
        if r.returncode == 0:
            try:
                d = json.loads(r.stdout)
            except json.JSONDecodeError:
                time.sleep(4 * (a + 1)); continue
            if "meta" in d and d["meta"].get("count") is not None:
                return d, None
            return None, (d.get("message") or "refused")[:100]
        time.sleep(4 * (a + 1))
    return None, "curl failed"


def abstract(w):
    inv = w.get("abstract_inverted_index")
    if not inv:
        return ""
    pos = {}
    for word, ps in inv.items():
        for p in ps:
            pos[p] = word
    return " ".join(pos[i] for i in sorted(pos))


def safe(v):
    return re.sub(r"\s+", " ", re.sub(r"[?!]", " ", v)).strip()


def phr(p):
    assert not p.lower().startswith("not "), p
    return f'"{safe(p)}"'


def blk(t):
    return "(" + " OR ".join(phr(x) for x in t) + ")"


rep = json.loads((LOGS / "credit-constraints-query-repair.json").read_text())
OUTCOME = rep["final"]["outcome_axis"]
EXPO = rep["final"]["exposure_axes"]

# Detectors run over title+abstract text, not over the query.
def rx(terms):
    return re.compile("|".join(re.escape(t).replace(r"\ ", r"\s+") for t in terms), re.I)

RX_OUT = rx(OUTCOME + ["fertility rate", "birth outcome", "children ever born",
                       "contraceptive", "pregnancy", "family planning"])
RX_COMP = rx(EXPO["composite"] + ["bank branch", "branch expansion", "financial access",
                                  "savings account", "credit program", "microcredit",
                                  "microfinance", "financial inclusion", "banked", "unbanked"])
RX_S = rx(EXPO["S"])
RX_B = rx(EXPO["B"])
# bare "experiment"/"experimental" included deliberately -- an IDENT list without them scored
# a paper titled "Experimental Evidence" as unidentified.
RX_IDENT = rx(["natural experiment", "quasi-experiment", "quasi experimental", "experiment",
               "experimental", "randomized", "randomised", "random assignment",
               "randomly assigned", "difference-in-difference", "difference in difference",
               "differences-in-differences", "instrumental variable", "instrument for",
               "regression discontinuity", "event study", "staggered", "rollout", "roll-out",
               "exogenous variation", "exogenous", "policy reform", "control group",
               "treatment and control", "panel fixed effects", "triple difference"])


def score(rec):
    t = (rec.get("title") or "") + " . " + rec.get("abstract", "")
    return {"has_outcome": bool(RX_OUT.search(t)),
            "has_composite": bool(RX_COMP.search(t)),
            "has_S": bool(RX_S.search(t)),
            "has_B": bool(RX_B.search(t)),
            "has_ident": bool(RX_IDENT.search(t)),
            "ident_terms": sorted({m.group(0).lower() for m in RX_IDENT.finditer(t)})[:6]}


def shape(w):
    src = ((w.get("primary_location") or {}).get("source") or {})
    return {"openalex": w["id"].rsplit("/", 1)[-1],
            "doi": (w.get("doi") or "").replace("https://doi.org/", "") or None,
            "title": w.get("title"), "year": w.get("publication_year"),
            "type": w.get("type"), "venue": src.get("display_name"),
            "cited_by": w.get("cited_by_count"),
            "authors": "; ".join(a["author"]["display_name"]
                                 for a in (w.get("authorships") or [])[:3]),
            "abstract": abstract(w)}


def channel_a():
    """Term channel: composite exposure x fertility outcome, paged out in full."""
    f = f"title_and_abstract.search:{blk(EXPO['composite'])} AND {blk(OUTCOME)}"
    recs, cursor = {}, "*"
    while cursor:
        d, err = get([("filter", f), ("per-page", "200"), ("cursor", cursor),
                      ("select", SELECT)])
        if err:
            print(f"  channel A FAILED: {err}", file=sys.stderr)
            break
        for w in d["results"]:
            recs[w["id"].rsplit("/", 1)[-1]] = shape(w)
        cursor = d["meta"].get("next_cursor")
        print(f"  channel A: {len(recs)}/{d['meta']['count']}")
        if not d["results"]:
            break
    return recs


def channel_b():
    """Provenance channel: hydrate abstracts for the snowball pool."""
    pool = json.loads((LOGS / "credit-constraints-snowball-pool.json").read_text())
    ids = [r["openalex"] for r in pool]
    recs = {}
    for i in range(0, len(ids), 50):
        d, err = get([("filter", "openalex_id:" + "|".join(ids[i:i + 50])),
                      ("per-page", "50"), ("select", SELECT)])
        if err:
            print(f"  channel B batch {i} FAILED: {err}", file=sys.stderr)
            continue
        for w in d["results"]:
            recs[w["id"].rsplit("/", 1)[-1]] = shape(w)
        if i % 500 == 0:
            print(f"  channel B: {len(recs)}/{len(ids)}")
    return recs


def main():
    print("channel A (term):")
    A = channel_a()
    print(f"\nchannel B (provenance):")
    B = channel_b()

    allrec = {}
    for k, v in B.items():
        v["channels"] = ["provenance"]; allrec[k] = v
    for k, v in A.items():
        if k in allrec:
            allrec[k]["channels"].append("term")
        else:
            v["channels"] = ["term"]; allrec[k] = v

    for r in allrec.values():
        r.update(score(r))

    hits = [r for r in allrec.values()
            if r["has_outcome"] and r["has_composite"] and r["has_ident"]]
    hits.sort(key=lambda r: (-(r["cited_by"] or 0)))
    no_abs = sum(1 for r in allrec.values() if not r["abstract"])

    summary = {
        "channel_A_term": len(A), "channel_B_provenance": len(B),
        "union": len(allrec), "overlap_both_channels":
            sum(1 for r in allrec.values() if len(r["channels"]) == 2),
        "records_without_abstract": no_abs,
        "composite_exposure_x_fertility_outcome":
            sum(1 for r in allrec.values() if r["has_outcome"] and r["has_composite"]),
        "…_and_identification_vocabulary": len(hits),
        "by_channel_of_the_hits": {
            "term_only": sum(1 for r in hits if r["channels"] == ["term"]),
            "provenance_only": sum(1 for r in hits if r["channels"] == ["provenance"]),
            "both": sum(1 for r in hits if len(r["channels"]) == 2)},
    }
    OUT.write_text(json.dumps({"summary": summary, "hits": hits[:120]}, indent=2))
    print("\n" + json.dumps(summary, indent=1))
    print("\nTOP CANDIDATES (composite exposure x fertility outcome x identification)\n")
    for r in hits[:25]:
        print(f"  {r['year']} [{'+'.join(r['channels'])}] cites {r['cited_by']:5d} | "
              f"{(r['title'] or '')[:88]}")
        print(f"        {r['venue']} | ident: {', '.join(r['ident_terms'])}")
    print(f"\nwritten: {OUT}")


if __name__ == "__main__":
    main()
