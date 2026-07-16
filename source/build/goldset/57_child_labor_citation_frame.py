#!/usr/bin/env python3
"""Build the orthogonal citation candidate frame for TICK-031.

This is GACS cold-start channel 3, not a relevance screen and not a frozen gold set.
It resolves the independently assembled anchors in OpenAlex, collects their backward
references and forward citations, and emits a DOI-first/title-second deduplicated frame
with paper-level discovery provenance.

Inputs:
  literature/search-logs/child-labor-laws-and-schooling-cold-start-anchors.json

Outputs:
  literature/search-logs/child-labor-laws-and-schooling-anchor-resolution.json
  literature/search-logs/child-labor-laws-and-schooling-citation-frame.json
  literature/search-logs/child-labor-laws-and-schooling-citation-frame-log.md

Each API response is cached under source/build/goldset/cache/child_labor_citation_frame.
Re-running resumes from cache. Use --refresh to ignore existing cache entries.
"""

import argparse
import hashlib
import json
import re
import subprocess
import sys
import time
import unicodedata
from collections import defaultdict
from pathlib import Path
from urllib.parse import quote

SLUG = "child-labor-laws-and-schooling"
HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
LOGS = REPO / "literature" / "search-logs"
CACHE = HERE / "cache" / "child_labor_citation_frame"
MAILTO = "zhitongz@uchicago.edu"
SELECT = "id,doi,title,publication_year,authorships,primary_location,abstract_inverted_index,referenced_works"
PER_PAGE = 200
SLEEP = 0.35
MAX_FORWARD_PAGES_PER_ANCHOR = 25  # 5,000 citing works; graceful hard cap


def norm_title(value):
    value = unicodedata.normalize("NFKD", value or "").encode("ascii", "ignore").decode()
    value = value.lower().replace("&", " and ")
    value = re.sub(r"\s*[:\-–—]\s+.*$", "", value)  # subtitle-insensitive guard
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9\s]", " ", value)).strip()


def token_similarity(a, b):
    aa, bb = set(norm_title(a).split()), set(norm_title(b).split())
    return len(aa & bb) / len(aa | bb) if aa and bb else 0.0


def deinvert(index):
    if not index:
        return ""
    words = sorted((position, word) for word, positions in index.items() for position in positions)
    return " ".join(word for _, word in words)


def cache_path(url):
    return CACHE / f"{hashlib.sha256(url.encode()).hexdigest()}.json"


def get_json(url, refresh=False, tries=4):
    CACHE.mkdir(parents=True, exist_ok=True)
    path = cache_path(url)
    if path.exists() and not refresh:
        return json.loads(path.read_text())
    for attempt in range(tries):
        result = subprocess.run(
            ["curl", "-L", "--silent", "--show-error", "--max-time", "45",
             url],
            capture_output=True, text=True,
        )
        if result.returncode == 0 and result.stdout.strip():
            try:
                payload = json.loads(result.stdout)
                if not (isinstance(payload, dict) and payload.get("error") and "results" not in payload):
                    path.write_text(json.dumps(payload))
                    time.sleep(SLEEP)
                    return payload
            except json.JSONDecodeError:
                pass
        if attempt < tries - 1:
            time.sleep(2 ** attempt)
    raise RuntimeError(f"OpenAlex request failed after {tries} attempts: {url}")


def api(path):
    joiner = "&" if "?" in path else "?"
    return f"https://api.openalex.org/{path}{joiner}mailto={quote(MAILTO)}"


def resolve_anchor(anchor, refresh=False):
    candidates = []
    if anchor.get("openalex_id"):
        try:
            candidates.append(get_json(api(f"works/{anchor['openalex_id']}"), refresh))
        except RuntimeError:
            pass
    if anchor.get("doi"):
        doi_url = f"https://doi.org/{anchor['doi']}"
        try:
            # OpenAlex accepts the DOI URL as the work identifier; preserve URL separators.
            candidates.append(get_json(api(f"works/{quote(doi_url, safe=':/')}"), refresh))
        except RuntimeError:
            pass
    if not candidates:
        # A bounded title query is more robust than sending punctuation-heavy full titles.
        query = quote(" ".join(norm_title(anchor["title"]).split()[:14]))
        data = get_json(api(f"works?search={query}&per-page=5&select={SELECT}"), refresh)
        candidates.extend(data.get("results", []))
    scored = []
    for work in candidates:
        if not isinstance(work, dict) or not work.get("id"):
            continue
        score = token_similarity(anchor["title"], work.get("title"))
        year_gap = abs((anchor.get("year") or 0) - (work.get("publication_year") or 0))
        scored.append((score, -year_gap, work))
    if not scored:
        return None, 0.0
    score, _, work = max(scored, key=lambda row: (row[0], row[1]))
    return work, score


def flatten(work):
    return {
        "paperId": (work.get("id") or "").rsplit("/", 1)[-1],
        "doi": (work.get("doi") or "").lower().replace("https://doi.org/", "") or None,
        "title": work.get("title") or "",
        "year": work.get("publication_year"),
        "authors": "; ".join(
            item.get("author", {}).get("display_name", "")
            for item in (work.get("authorships") or [])[:12]
        ),
        "venue": ((work.get("primary_location") or {}).get("source") or {}).get("display_name"),
        "abstract": deinvert(work.get("abstract_inverted_index")),
    }


def fetch_by_ids(ids, refresh=False):
    out = []
    ids = sorted(set(item.rsplit("/", 1)[-1] for item in ids if item))
    for start in range(0, len(ids), 50):
        group = "|".join(ids[start:start + 50])
        url = api(f"works?filter=openalex_id:{quote(group, safe='|')}&per-page=50&select={SELECT}")
        out.extend(get_json(url, refresh).get("results", []))
    return out


def fetch_forward(anchor_id, refresh=False):
    out, cursor, pages = [], "*", 0
    while cursor and pages < MAX_FORWARD_PAGES_PER_ANCHOR:
        path = (f"works?filter=cites:{anchor_id}&per-page={PER_PAGE}&cursor={quote(cursor, safe='')}"
                f"&select={SELECT}")
        data = get_json(api(path), refresh)
        out.extend(data.get("results", []))
        cursor = (data.get("meta") or {}).get("next_cursor")
        pages += 1
    return out, pages, bool(cursor)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--refresh", action="store_true")
    args = parser.parse_args()
    anchors = json.loads((LOGS / f"{SLUG}-cold-start-anchors.json").read_text())

    resolved, unresolved = [], []
    for anchor in anchors:
        work, score = resolve_anchor(anchor, args.refresh)
        if work is None or score < 0.50:
            unresolved.append({"title": anchor["title"], "similarity": score})
            continue
        resolved.append({
            "anchor": anchor,
            "openalex": flatten(work),
            "title_similarity": round(score, 4),
            "referenced_works": work.get("referenced_works") or [],
        })
    (LOGS / f"{SLUG}-anchor-resolution.json").write_text(
        json.dumps({"resolved": resolved, "unresolved": unresolved}, indent=2, ensure_ascii=False)
    )

    discovered = defaultdict(lambda: {"channels": set(), "seed_ids": set(), "work": None})
    forward_pages = 0
    capped_seeds = []
    for item in resolved:
        seed = item["openalex"]["paperId"]
        backward = fetch_by_ids(item["referenced_works"], args.refresh)
        forward, pages, capped = fetch_forward(seed, args.refresh)
        forward_pages += pages
        if capped:
            capped_seeds.append(seed)
        for channel, works in (("backward_reference", backward), ("forward_citation", forward)):
            for work in works:
                wid = (work.get("id") or "").rsplit("/", 1)[-1]
                if not wid or wid == seed:
                    continue
                discovered[wid]["channels"].add(channel)
                discovered[wid]["seed_ids"].add(seed)
                discovered[wid]["work"] = work

    anchor_ids = {item["openalex"]["paperId"] for item in resolved}
    by_doi, by_title, frame = {}, {}, []
    duplicates = 0
    for wid, item in discovered.items():
        if wid in anchor_ids:
            continue
        rec = flatten(item["work"])
        doi, title_key = rec["doi"], norm_title(rec["title"])
        existing = by_doi.get(doi) if doi else by_title.get(title_key)
        if existing is not None:
            duplicates += 1
            existing["discovery_channels"] = sorted(set(existing["discovery_channels"]) | item["channels"])
            existing["seed_openalex_ids"] = sorted(set(existing["seed_openalex_ids"]) | item["seed_ids"])
            continue
        rec["discovery_channels"] = sorted(item["channels"])
        rec["seed_openalex_ids"] = sorted(item["seed_ids"])
        rec["gold_status"] = "tier_b_candidate_unscreened"
        frame.append(rec)
        if doi:
            by_doi[doi] = rec
        if title_key:
            by_title[title_key] = rec
    frame.sort(key=lambda row: (-len(row["discovery_channels"]), -(row.get("year") or 0), row["title"]))
    (LOGS / f"{SLUG}-citation-frame.json").write_text(json.dumps(frame, indent=2, ensure_ascii=False))

    both = sum(len(row["discovery_channels"]) > 1 for row in frame)
    abstracts = sum(len(row.get("abstract") or "") >= 30 for row in frame)
    lines = [
        f"# Orthogonal citation frame — {SLUG}", "",
        "This is a **candidate frame**, not a screened or frozen Tier-B gold set.", "",
        f"- input anchors: {len(anchors)}",
        f"- OpenAlex-resolved anchors: {len(resolved)}",
        f"- unresolved anchors: {len(unresolved)}",
        f"- deduplicated citation candidates: {len(frame):,}",
        f"- candidates found by both backward and forward channels: {both:,}",
        f"- candidates with usable abstracts: {abstracts:,}",
        f"- duplicate records merged: {duplicates:,}",
        f"- forward pages requested/cached: {forward_pages}",
        f"- forward seeds hitting the {MAX_FORWARD_PAGES_PER_ANCHOR}-page cap: {len(capped_seeds)}",
        "", "## Next gate", "",
        "Screen the whole frame with the TICK-031 topical/estimand rubric. Papers are not selected "
        "for vocabulary distance from the future production query; doing so would bias Recall(B).",
    ]
    if unresolved:
        lines += ["", "## Unresolved anchors", ""] + [f"- {x['title']} (similarity {x['similarity']:.2f})" for x in unresolved]
    (LOGS / f"{SLUG}-citation-frame-log.md").write_text("\n".join(lines) + "\n")
    print(f"anchors {len(anchors)} -> resolved {len(resolved)}; citation frame {len(frame)}; "
          f"both-channel {both}; abstracts {abstracts}; duplicates {duplicates}", file=sys.stderr)
    if unresolved:
        print(f"WARNING: {len(unresolved)} unresolved anchors; see anchor-resolution output", file=sys.stderr)


if __name__ == "__main__":
    main()
