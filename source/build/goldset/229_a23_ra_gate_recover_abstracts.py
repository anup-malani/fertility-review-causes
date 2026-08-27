#!/usr/bin/env python3
"""
229 — A.23 RA gate, step 1: recover the abstracts the screen could not see.

TICK-075. The screen report flagged its own weakest point: 165 of the 241 records
with no OpenAlex abstract were marked NOT_RELEVANT on the title alone. The rubric
allows that only when the title is decisive, and mostly it is -- but a title-only
false negative is exactly the failure this chapter has already suffered once, when a
gated anchor kept a wrong classification because the exposure audit had nothing to
read.

The right fix is not to sample the bucket and hope. It is to go and get the
abstracts from a DIFFERENT SOURCE. OpenAlex's abstract coverage is incomplete;
Crossref often holds an abstract for the same DOI, and the two are independent
enough that the gap is worth testing rather than assumed.

This script asks Crossref for every no-abstract record that has a DOI, records what
came back, and writes a re-read worklist of the records whose verdict was reached
without visible content and where content now exists. A record with no DOI, or with
no Crossref abstract either, stays in the bucket and is reported as such -- a
recovered zero and an unrecoverable one are different facts.

Usage: python3 source/build/goldset/229_a23_ra_gate_recover_abstracts.py
"""
import json
import re
import subprocess
import time
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
LOGS = ROOT / "literature" / "search-logs"
SCREENED = LOGS / "co-residence-parents-household-delay-screened.json"
OUT = LOGS / "co-residence-parents-household-delay-ra-gate-abstracts.json"
CROSSREF = "https://api.crossref.org/works/"
UA = "User-Agent: fertility-review (mailto:shravanh@uchicago.edu)"

TAG = re.compile(r"<[^>]+>")


def crossref_abstract(doi, tries=3):
    """Return (abstract or None, status). ERROR is never confused with absent."""
    url = CROSSREF + doi
    for attempt in range(tries):
        r = subprocess.run(["curl", "-sS", "--max-time", "45", "-H", UA, url],
                           capture_output=True, text=True)
        if r.returncode != 0:
            time.sleep(3 * (attempt + 1))
            continue
        txt = r.stdout.strip()
        if txt.startswith("Resource not found"):
            return None, "NOT_IN_CROSSREF"
        try:
            m = json.loads(txt)["message"]
        except Exception:
            time.sleep(3 * (attempt + 1))
            continue
        a = m.get("abstract")
        if not a:
            return None, "NO_ABSTRACT_IN_CROSSREF"
        a = TAG.sub(" ", a)
        a = re.sub(r"\s+", " ", a).strip()
        a = re.sub(r"^Abstract\s+", "", a)
        return a, "RECOVERED"
    return None, "ERROR"


def main():
    doc = json.loads(SCREENED.read_text())
    recs = doc["records"]
    bucket = [r for r in recs if not r["abstract_present"]]
    print(f"records with no OpenAlex abstract: {len(bucket)}")
    print(f"  of which marked NOT_RELEVANT on the title alone: "
          f"{sum(1 for r in bucket if r['verdict'] == 'NOT_RELEVANT')}")
    no_doi = [r for r in bucket if not r["doi"]]
    print(f"  with no DOI, so unreachable by this route: {len(no_doi)}\n")

    results, status = [], Counter()
    for i, r in enumerate(bucket, 1):
        if not r["doi"]:
            st, ab = "NO_DOI", None
        else:
            ab, st = crossref_abstract(r["doi"])
        status[st] += 1
        results.append({**{k: r[k] for k in ("openalex", "doi", "title", "year",
                                             "venue", "verdict", "route",
                                             "exposure_is_arrangement", "note")},
                        "recovery_status": st,
                        "recovered_abstract": ab})
        if i % 40 == 0:
            print(f"  {i}/{len(bucket)}  {dict(status)}")

    recovered = [x for x in results if x["recovery_status"] == "RECOVERED"]
    # The worklist: records whose verdict was reached blind and where text now exists.
    worklist = [x for x in recovered if x["verdict"] == "NOT_RELEVANT"]
    uncertain_now_readable = [x for x in recovered if x["verdict"] == "UNCERTAIN"]

    meta = {
        "ticket": "TICK-075", "stage": "RA gate step 1",
        "no_abstract_bucket": len(bucket),
        "marked_not_relevant_on_title_alone":
            sum(1 for r in bucket if r["verdict"] == "NOT_RELEVANT"),
        "recovery": dict(status),
        "recovered": len(recovered),
        "recovery_rate_pct": round(100 * len(recovered) / max(1, len(bucket)), 1),
        "re_read_worklist_not_relevant": len(worklist),
        "now_readable_uncertain": len(uncertain_now_readable),
        "still_invisible": len(bucket) - len(recovered),
        "note": "A record that stays invisible is not thereby irrelevant. The bucket is "
                "reported in three parts -- recovered, absent from Crossref, and no DOI at "
                "all -- because they carry different weight at the gate.",
    }
    OUT.write_text(json.dumps({"meta": meta, "records": results}, indent=1))
    print("\n" + json.dumps(meta, indent=1))
    print(f"\nwrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
