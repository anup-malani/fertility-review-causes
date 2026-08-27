#!/usr/bin/env python3
"""
224 — A.23 production frame pull.

TICK-075. Pulls the adopted query (222, variant V2: cause axis without the
emancipation family) in full, with abstracts, using cursor pagination.

The frame is the screenable population. Three things it records that a bare pull
would not:

  * WHICH RECORDS ARE GOLD. Each of the 33 gated anchors is marked in place, so
    the screen's treatment of them is auditable afterwards and gold that the
    screen rejects is visible rather than lost.
  * WHETHER AN ABSTRACT EXISTS. A record with no abstract is not a record with
    nothing in it; it is a record the screen cannot see. The count is reported
    here so the no-abstract bucket is sized before screening rather than
    discovered as a residue.
  * THE SNOWBALL OVERLAP. The 3,793-record snowball pool and this frame were
    built by independent channels, so their intersection is a check on both.

Usage: python3 source/build/goldset/224_a23_pull_frame.py
"""
import json
import re
import subprocess
import time
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
LOGS = ROOT / "literature" / "search-logs"
QUERYFILE = LOGS / "co-residence-parents-household-delay-production-query.json"
ANCHORS = LOGS / "co-residence-parents-household-delay-cold-start-anchors.json"
POOL = LOGS / "co-residence-parents-household-delay-snowball-pool.json"
OUT = LOGS / "co-residence-parents-household-delay-frame.json"
API = "https://api.openalex.org/works"
SELECT = ("id,doi,title,publication_year,type,cited_by_count,primary_location,"
          "authorships,abstract_inverted_index,language")

TRANSLIT = {"ø": "o", "æ": "ae", "å": "a", "ß": "ss", "đ": "d", "ł": "l", "ð": "d", "þ": "th"}


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


def get(params, tries=4):
    args = ["curl", "-sS", "--max-time", "180", "--get", API]
    for k, v in params:
        args += ["--data-urlencode", f"{k}={v}"]
    if KEY:
        args += ["--data-urlencode", f"api_key={KEY}"]
    last = None
    for attempt in range(tries):
        r = subprocess.run(args, capture_output=True, text=True)
        if r.returncode != 0:
            last = f"curl-{r.returncode}"; time.sleep(6 * (attempt + 1)); continue
        try:
            d = json.loads(r.stdout)
        except Exception:
            last = "parse"; time.sleep(6 * (attempt + 1)); continue
        if "error" in d:
            last = str(d["error"])[:70]; time.sleep(12 * (attempt + 1)); continue
        return d, None
    return None, last


def deinvert(ii):
    if not ii:
        return None
    pos = {}
    for w, ps in ii.items():
        for p in ps:
            pos[p] = w
    return " ".join(pos[i] for i in sorted(pos))


def main():
    qdoc = json.loads(QUERYFILE.read_text())
    query = qdoc["variants"]["V2_no_emancipation"]["query"]
    expected = qdoc["variants"]["V2_no_emancipation"]["frame_size"]
    print(f"adopted query V2, expected frame {expected}\n")

    anchors = {a["doi"]: a for a in json.loads(ANCHORS.read_text())["anchors"]}
    pool_ids = {r["openalex"] for r in json.loads(POOL.read_text())}

    records, cursor, page = [], "*", 0
    while cursor:
        d, err = get([("filter", f"title_and_abstract.search:{query}"),
                      ("per-page", "200"), ("cursor", cursor), ("select", SELECT)])
        if err:
            print(f"  page {page + 1} FAILED: {err}")
            break
        page += 1
        for w in d["results"]:
            src = ((w.get("primary_location") or {}).get("source") or {})
            doi = (w.get("doi") or "").replace("https://doi.org/", "") or None
            oid = w["id"].rsplit("/", 1)[-1]
            records.append({
                "openalex": oid, "doi": doi,
                "title": w.get("title"), "norm_title": fold(w.get("title")),
                "year": w.get("publication_year"), "type": w.get("type"),
                "venue": src.get("display_name"), "language": w.get("language"),
                "cited_by": w.get("cited_by_count"),
                "authors": "; ".join(a["author"]["display_name"]
                                     for a in (w.get("authorships") or [])[:5]),
                "abstract": deinvert(w.get("abstract_inverted_index")),
                "is_anchor": doi in anchors,
                "anchor_cell": anchors.get(doi, {}).get("provisional_cell"),
                "anchor_gold": anchors.get(doi, {}).get("gold_status") == "gold_candidate",
                "in_snowball_pool": oid in pool_ids,
            })
        cursor = d["meta"].get("next_cursor")
        print(f"  page {page}: {len(records)} / {d['meta']['count']}")
        if not d["results"]:
            break

    # dedup by folded title; keep the published, most-cited survivor
    by_title, dropped = {}, []
    for r in records:
        k = r["norm_title"] or r["openalex"]
        if k not in by_title:
            by_title[k] = r
            continue
        keep, lose = sorted([by_title[k], r],
                            key=lambda x: (x["doi"] is None,
                                           "preprint" in (x["type"] or ""),
                                           -(x["cited_by"] or 0)))[0:2]
        by_title[k] = keep
        dropped.append({"dropped": lose["openalex"], "kept": keep["openalex"],
                        "title": lose["title"]})
    frame = list(by_title.values())

    n_abs = sum(1 for r in frame if r["abstract"])
    gold_in = [r for r in frame if r["anchor_gold"]]
    anchors_in = [r for r in frame if r["is_anchor"]]
    overlap = sum(1 for r in frame if r["in_snowball_pool"])

    meta = {
        "ticket": "TICK-075",
        "query_variant": "V2_no_emancipation",
        "query": query,
        "pulled": len(records), "after_dedup": len(frame),
        "duplicates_collapsed": len(dropped),
        "with_abstract": n_abs,
        "no_abstract": len(frame) - n_abs,
        "no_abstract_pct": round(100 * (len(frame) - n_abs) / max(1, len(frame)), 1),
        "gold_anchors_present": len(gold_in),
        "gold_anchors_total": sum(1 for a in json.loads(ANCHORS.read_text())["anchors"]
                                  if a["gold_status"] == "gold_candidate"),
        "all_anchors_present": len(anchors_in),
        "overlap_with_snowball_pool": overlap,
        "overlap_pct_of_frame": round(100 * overlap / max(1, len(frame)), 1),
        "note": "The no-abstract bucket is a record the screen CANNOT SEE, not an empty record. "
                "It must never take a NOT_RELEVANT verdict on absence of visible content.",
    }
    OUT.write_text(json.dumps({"meta": meta, "duplicates_collapsed": dropped,
                               "records": frame}, indent=1))
    print("\n" + json.dumps(meta, indent=1))
    print(f"\nwrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
