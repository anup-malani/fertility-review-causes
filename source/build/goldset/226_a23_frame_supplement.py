#!/usr/bin/env python3
"""
226 — A.23 frame supplement: the two records the query provably misses.

TICK-075. The independent-channel recall check (225) found the production query
reaches 10 of the 12 snowball-pool records that look on-topic on their titles, and
misses two. Both are missed for the same reason: they word the exposure as
"household structure" or "living arrangement", which are not in the cause axis.

THE OBVIOUS FIX WAS MEASURED AND REJECTED. Adding that family to the axis:

    V2 (adopted)                                1,711
    V2 + living-arrangement family              3,151
    the family alone, not reachable by V2       1,440
    the same, qualified with parents/young adult  504

and reading the additions shows why. "Living arrangement" and "household structure"
are generic demographic terms: the 1,440 are ageing cohort profiles, single-parent
families, marital dissolution, children's living arrangements with one parent versus
two. Even the qualified 504 is dominated by them. That is an 84% frame expansion, or
a 29% one, buying two records — a precision cost the screen would pay for almost no
gold.

So the two records are added to the frame BY HAND, from an independent channel, with
their provenance recorded. This is auditable in a way a silently widened axis is not:
the frame's own metadata says which records the boolean query did not produce.

Usage: python3 source/build/goldset/226_a23_frame_supplement.py
"""
import json
import re
import subprocess
import time
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
LOGS = ROOT / "literature" / "search-logs"
FRAME = LOGS / "co-residence-parents-household-delay-frame.json"
API = "https://api.openalex.org/works"
CROSSREF = "https://api.crossref.org/works/"
SELECT = ("id,doi,title,publication_year,type,cited_by_count,primary_location,"
          "authorships,abstract_inverted_index,language")

TRANSLIT = {"ø": "o", "æ": "ae", "å": "a", "ß": "ss", "đ": "d", "ł": "l", "ð": "d", "þ": "th"}

SUPPLEMENT = [
    ("10.1086/451997",
     "Household structure as the exposure. Missed because the axis has no "
     "'household structure' term; adding one costs 1,440 off-construct records."),
    ("10.7454/jessd.v6i1.1145",
     "Living arrangement and homeownership against fertility intention. Same reason."),
]


def api_key():
    env = ROOT / ".env"
    if env.exists():
        for line in env.read_text().splitlines():
            if line.startswith("OPENALEX_API_KEY="):
                return line.split("=", 1)[1].strip()
    return ""


KEY = api_key()


def fold(s):
    if not s:
        return ""
    s = s.lower()
    s = "".join(TRANSLIT.get(c, c) for c in s)
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]+", " ", s).strip()


def curl_json(args, tries=3):
    for attempt in range(tries):
        r = subprocess.run(args, capture_output=True, text=True)
        if r.returncode != 0:
            time.sleep(4 * (attempt + 1)); continue
        if r.stdout.strip().startswith("Resource not found"):
            return None
        try:
            return json.loads(r.stdout)
        except Exception:
            time.sleep(4 * (attempt + 1))
    return None


def deinvert(ii):
    if not ii:
        return None
    pos = {}
    for w, ps in ii.items():
        for p in ps:
            pos[p] = w
    return " ".join(pos[i] for i in sorted(pos))


def main():
    doc = json.loads(FRAME.read_text())
    have = {r["doi"] for r in doc["records"] if r["doi"]}
    added, failed = [], []

    for doi, why in SUPPLEMENT:
        if doi in have:
            print(f"  already in frame: {doi}")
            continue
        # existence gate first, against Crossref
        cr = curl_json(["curl", "-sS", "--max-time", "60", "-H",
                        "User-Agent: fertility-review (mailto:shravanh@uchicago.edu)",
                        CROSSREF + doi])
        if not cr:
            failed.append({"doi": doi, "reason": "failed the Crossref existence gate"})
            print(f"  UNRESOLVED (not added): {doi}")
            continue
        args = ["curl", "-sS", "--max-time", "90", "--get", f"{API}/doi:{doi}",
                "--data-urlencode", f"select={SELECT}"]
        if KEY:
            args += ["--data-urlencode", f"api_key={KEY}"]
        w = curl_json(args)
        if not w or "error" in w:
            failed.append({"doi": doi, "reason": "no OpenAlex record"})
            print(f"  no OpenAlex record (not added): {doi}")
            continue
        src = ((w.get("primary_location") or {}).get("source") or {})
        rec = {
            "openalex": w["id"].rsplit("/", 1)[-1], "doi": doi,
            "title": w.get("title"), "norm_title": fold(w.get("title")),
            "year": w.get("publication_year"), "type": w.get("type"),
            "venue": src.get("display_name"), "language": w.get("language"),
            "cited_by": w.get("cited_by_count"),
            "authors": "; ".join(a["author"]["display_name"]
                                 for a in (w.get("authorships") or [])[:5]),
            "abstract": deinvert(w.get("abstract_inverted_index")),
            "is_anchor": False, "anchor_cell": None, "anchor_gold": False,
            "in_snowball_pool": True,
            "hand_added": True,
            "hand_added_reason": why,
            "hand_added_channel": "snowball pool, via the 225 independent-channel recall check",
        }
        doc["records"].append(rec)
        added.append({"doi": doi, "title": rec["title"], "crossref_title":
                      (cr["message"].get("title") or [None])[0]})
        print(f"  added: {doi}  {(rec['title'] or '')[:60]}")

    for r in doc["records"]:
        r.setdefault("hand_added", False)

    doc["meta"]["hand_added"] = len(added)
    doc["meta"]["hand_added_detail"] = added
    doc["meta"]["hand_add_failures"] = failed
    doc["meta"]["after_dedup"] = len(doc["records"])
    doc["meta"]["axis_expansion_measured_and_rejected"] = {
        "candidate_family": '"living arrangement" / "living arrangements" / '
                            '"household structure" / "household composition"',
        "frame_if_added": 3151, "frame_adopted": 1711,
        "records_added_alone": 1440, "qualified_variant": 504,
        "gold_gained": 0, "records_recovered": len(added),
        "decision": "REJECTED as an axis term; the two records are hand-added instead. The family "
                    "is generic demography -- children's living arrangements, elderly living "
                    "arrangements, single-parent families -- not A.23's construct.",
    }
    FRAME.write_text(json.dumps(doc, indent=1))
    print(f"\nframe now {len(doc['records'])} records "
          f"({len(added)} hand-added, {len(failed)} failed)")
    print(f"wrote {FRAME.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
