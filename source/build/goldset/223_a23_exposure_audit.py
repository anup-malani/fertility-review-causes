#!/usr/bin/env python3
"""
223 — A.23 anchor exposure audit.

TICK-075. The production query's calibration (222) missed four gold candidates,
all of them extended-household. Reading their abstracts showed the query was
right and the CLASSIFICATION was wrong: none of the four contains any
co-residence language at all. Their exposure is the GRANDMOTHER'S TIME, identified
off pension and retirement-age reform, and the living arrangement never appears.

Under the "what varies" rule this chapter inherited from C.2.c, that is not A.23's
variation. A.23 owns variation in the living arrangement; the availability of
informal childcare at a given living arrangement is C.2.a's. A recall failure was
the signal, and the fix belongs in the anchor set rather than in the query.

This script re-audits every anchor on the same test, mechanically: does the
abstract contain the arrangement as an exposure, or does it not appear at all?
The verdict is proposed by the script and marked for a human read -- an abstract
can carry the arrangement as a control or a caveat rather than as the treatment,
and no regex settles that.

Usage: python3 source/build/goldset/223_a23_exposure_audit.py
"""
import json
import re
import subprocess
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
LOGS = ROOT / "literature" / "search-logs"
ANCHORS = LOGS / "co-residence-parents-household-delay-cold-start-anchors.json"
OUT = LOGS / "co-residence-parents-household-delay-exposure-audit.json"
API = "https://api.openalex.org/works"

ARRANGEMENT = re.compile(
    r"co-?resid\w*|living with (?:their |her |his )?(?:parents?|in-laws?|mother-in-law)|"
    r"live[sd]? with|living arrangement|household structure|household composition|"
    r"multigenerational|three-generation|extended household|stem family|"
    r"parental home|leaving home|left home|home-?leaving|nest|"
    r"living apart from parents|emancipation|household formation|"
    r"patrilocal|shared hous\w*|proximity to parents|distance to parents|"
    r"living near|geographic\w* proximity", re.I)
TIME_SUPPLY = re.compile(
    r"childcare|child care|retirement|pension|labou?r (?:force|supply)|"
    r"grandparental (?:investment|support|care)|availability", re.I)


def api_key():
    env = ROOT / ".env"
    if env.exists():
        for line in env.read_text().splitlines():
            if line.startswith("OPENALEX_API_KEY="):
                return line.split("=", 1)[1].strip()
    return ""


KEY = api_key()


def abstract(doi):
    args = ["curl", "-sS", "--max-time", "90", "--get", f"{API}/doi:{doi}",
            "--data-urlencode", "select=title,abstract_inverted_index"]
    if KEY:
        args += ["--data-urlencode", f"api_key={KEY}"]
    for attempt in range(3):
        r = subprocess.run(args, capture_output=True, text=True)
        if r.returncode != 0:
            time.sleep(4 * (attempt + 1)); continue
        try:
            d = json.loads(r.stdout)
        except Exception:
            time.sleep(4 * (attempt + 1)); continue
        if "error" in d:
            time.sleep(8 * (attempt + 1)); continue
        ii = d.get("abstract_inverted_index") or {}
        if not ii:
            return d.get("title"), None, "NO_ABSTRACT_INDEXED"
        pos = {}
        for w, ps in ii.items():
            for p in ps:
                pos[p] = w
        return d.get("title"), " ".join(pos[i] for i in sorted(pos)), None
    return None, None, "ERROR"


def main():
    doc = json.loads(ANCHORS.read_text())
    rows, counts = [], {"ARRANGEMENT_PRESENT": 0, "ARRANGEMENT_ABSENT": 0,
                        "NO_ABSTRACT": 0, "ERROR": 0}
    for a in doc["anchors"]:
        title, abs_text, err = abstract(a["doi"])
        blob = f"{title or ''} {abs_text or ''}"
        if err == "ERROR":
            verdict, terms = "ERROR", []
        elif err == "NO_ABSTRACT_INDEXED":
            hits = ARRANGEMENT.findall(title or "")
            verdict = "NO_ABSTRACT"
            terms = sorted(set(h.lower() for h in hits))
        else:
            terms = sorted(set(h.lower() for h in ARRANGEMENT.findall(blob)))
            verdict = "ARRANGEMENT_PRESENT" if terms else "ARRANGEMENT_ABSENT"
        counts[verdict] += 1
        rows.append({
            "doi": a["doi"], "cell_as_recorded": a["provisional_cell"],
            "gold_status_as_recorded": a["gold_status"],
            "title": a["resolved_title"] or a["recorded_title"],
            "arrangement_terms_found": terms,
            "time_supply_terms_found": sorted(set(
                h.lower() for h in TIME_SUPPLY.findall(blob))) if abs_text else [],
            "verdict": verdict,
            "proposed_action": (
                "RECLASSIFY — the living arrangement does not appear; the exposure is "
                "something else (usually grandparental time supply, which is C.2.a's)"
                if verdict == "ARRANGEMENT_ABSENT" and a["gold_status"] == "gold_candidate"
                else "keep" if verdict == "ARRANGEMENT_PRESENT" else "human read required"),
            "human_read": "",
        })
        mark = {"ARRANGEMENT_PRESENT": "ok  ", "ARRANGEMENT_ABSENT": "FLAG",
                "NO_ABSTRACT": "?   ", "ERROR": "ERR "}[verdict]
        print(f"{mark} {a['gold_status'][:4]:4s} {a['doi']:36s} {(a['resolved_title'] or '')[:44]:44s} "
              f"{','.join(terms[:3])[:40]}")

    flagged_gold = [r for r in rows if r["verdict"] == "ARRANGEMENT_ABSENT"
                    and r["gold_status_as_recorded"] == "gold_candidate"]
    OUT.write_text(json.dumps({
        "meta": {
            "ticket": "TICK-075",
            "trigger": "222's per-anchor calibration missed 4 gold anchors, all extended-household. "
                       "Reading them showed no co-residence language at all.",
            "test": "Does the arrangement appear as the exposure, or not at all? A regex cannot tell "
                    "treatment from control, so ARRANGEMENT_PRESENT still needs a human read.",
            "counts": counts,
            "gold_flagged_for_reclassification": len(flagged_gold),
        },
        "rows": rows,
    }, indent=1))
    print(f"\n{counts}")
    print(f"gold candidates flagged for reclassification: {len(flagged_gold)}")
    for r in flagged_gold:
        print(f"   {r['doi']:36s} {r['title'][:56]}")
    print(f"\nwrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
