#!/usr/bin/env python3
"""
65_b1_tier_ab_frame.py — B.1 (evolutionary sex drive / contraceptive decoupling), stage A4.

Build the two-tier gold FRAME from the A3 cold-start anchors (GACS channels 1 + 3):

  Tier A  = the direct-empirical seeds (the anchors themselves), resolved in OpenAlex and enriched with
            abstracts. This is the primary empirical recall set. Theory-stream anchors and routing
            decoys are split out, NOT counted as Tier-A empirical.
  Tier B  = the orthogonal citation frame: backward references (all resolved anchors) + forward
            citations (forward-eligible anchors only), DOI-first/title-second deduplicated. This is the
            candidate frame the later screen turns into a scored Tier-B gold; it is NOT yet screened.

Neither tier is frozen here. This is a candidate frame, mirroring child-labor step 57.

FORWARD-SEED POLICY (B.1-specific, documented deviation from 57's forward-cite-everything):
  B.1's anchor set is theory-heavy, and two theory anchors carry citation clouds dominated by
  non-fertility evolutionary psychology (Buss 37-cultures ~4.5k cites; Kaplan life-history ~2.0k).
  Forward-citing them would flood Tier B with off-topic works and burn the (small) OpenAlex budget.
  Rule: forward-cite an anchor UNLESS it is a routing decoy OR (cited_by_count > FWD_THEORY_CAP AND
  provisional_cell == "THEORY"). Every empirical seed is forward-cited regardless of size (incl. the
  contraception-tech routing frontier). Backward references are pulled from ALL anchors. Excluded
  forward seeds are logged with their counts for transparency — this bounds the frame, it does not
  hide anything.

Budget discipline: every OpenAlex response cached; re-run resumes from cache. A network/429 failure on
an anchor is recorded as deferred (never treated as "no citations") so a partial run resumes cleanly.

Inputs : literature/search-logs/{slug}-cold-start-anchors.json
Outputs: literature/search-logs/{slug}-anchor-resolution.json
         literature/search-logs/{slug}-tier-a.json
         literature/search-logs/{slug}-tier-b-frame.json
         literature/search-logs/{slug}-tier-ab-log.md
"""
import argparse, hashlib, json, re, subprocess, sys, time, unicodedata
from collections import defaultdict
from pathlib import Path
from urllib.parse import quote

SLUG = "evolutionary-sex-drive-contraceptive-decoupling"
HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
LOGS = REPO / "literature" / "search-logs"
CACHE = HERE / "cache" / "b1_tier_ab"
MAILTO = "shravanh@uchicago.edu"
SELECT = "id,doi,title,publication_year,cited_by_count,authorships,primary_location,abstract_inverted_index,referenced_works"
PER_PAGE = 200
SLEEP = 0.35
MAX_FORWARD_PAGES = 20          # graceful hard cap per seed (4,000 works)
FWD_THEORY_CAP = 1500           # THEORY anchors above this are not forward-seeded
RESOLVE_SIM_MIN = 0.50

THEORY_CELL = "THEORY"
EMPIRICAL_CELLS = {"PROXIMATE_ULTIMATE", "PRIMARY_DECOUPLING", "PRIMARY_DESIRE_INDEPENDENCE",
                   "MOTIVATION_DISTINCTNESS", "CONTRACEPTIVE_MEDIATION", "SEX_FERTILITY_TREND_DECOUPLING"}


def norm_title(v):
    v = unicodedata.normalize("NFKD", v or "").encode("ascii", "ignore").decode()
    v = v.lower().replace("&", " and ")
    v = re.sub(r"\s*[:\-–—]\s+.*$", "", v)  # subtitle-insensitive
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9\s]", " ", v)).strip()


def sim(a, b):
    aa, bb = set(norm_title(a).split()), set(norm_title(b).split())
    return len(aa & bb) / len(aa | bb) if aa and bb else 0.0


def deinvert(idx):
    if not idx:
        return ""
    return " ".join(w for _, w in sorted((p, w) for w, ps in idx.items() for p in ps))


def get_json(url, refresh=False, tries=4):
    CACHE.mkdir(parents=True, exist_ok=True)
    path = CACHE / f"{hashlib.sha256(url.encode()).hexdigest()}.json"
    if path.exists() and not refresh:
        return json.loads(path.read_text())
    for attempt in range(tries):
        r = subprocess.run(["curl", "-L", "--silent", "--show-error", "--max-time", "45", url],
                           capture_output=True, text=True)
        if r.returncode == 0 and r.stdout.strip():
            try:
                payload = json.loads(r.stdout)
                if not (isinstance(payload, dict) and payload.get("error") and "results" not in payload):
                    path.write_text(json.dumps(payload))
                    time.sleep(SLEEP)
                    return payload
            except json.JSONDecodeError:
                pass
        if attempt < tries - 1:
            time.sleep(2 ** attempt)
    raise RuntimeError(f"OpenAlex failed after {tries} attempts: {url[:90]}")


def api(path):
    return f"https://api.openalex.org/{path}{'&' if '?' in path else '?'}mailto={quote(MAILTO)}"


def resolve(anchor, refresh=False):
    # An exact-DOI hit is authoritative: the DOI *is* the identity, so it bypasses the title-similarity
    # floor. OpenAlex sometimes ingests a section header into the title ("REFEREED ARTICLES - ...") or
    # drops a subtitle, which would wrongly sink a correct DOI match below the floor.
    if anchor.get("doi"):
        try:
            w = get_json(api(f"works/{quote('https://doi.org/'+anchor['doi'], safe=':/')}"), refresh)
            if isinstance(w, dict) and w.get("id"):
                return w, round(sim(anchor["title"], w.get("title")), 4), "doi"
        except RuntimeError:
            pass
    q = quote(" ".join(norm_title(anchor["title"]).split()[:14]))
    try:
        cands = get_json(api(f"works?search={q}&per-page=5&select={SELECT}"), refresh).get("results", [])
    except RuntimeError:
        return None, 0.0, "error"
    scored = [(sim(anchor["title"], w.get("title")),
               -abs((anchor.get("year") or 0) - (w.get("publication_year") or 0)), w)
              for w in cands if isinstance(w, dict) and w.get("id")]
    if not scored:
        return None, 0.0, "title"
    s, _, w = max(scored, key=lambda r: (r[0], r[1]))
    return w, s, "title"


def flatten(w):
    return {"paperId": (w.get("id") or "").rsplit("/", 1)[-1],
            "doi": (w.get("doi") or "").lower().replace("https://doi.org/", "") or None,
            "title": w.get("title") or "", "year": w.get("publication_year"),
            "cited_by_count": w.get("cited_by_count"),
            "authors": "; ".join(a.get("author", {}).get("display_name", "")
                                  for a in (w.get("authorships") or [])[:12]),
            "venue": ((w.get("primary_location") or {}).get("source") or {}).get("display_name"),
            "abstract": deinvert(w.get("abstract_inverted_index"))}


def fetch_by_ids(ids, refresh=False):
    out, ids = [], sorted(set(i.rsplit("/", 1)[-1] for i in ids if i))
    for s in range(0, len(ids), 50):
        grp = "|".join(ids[s:s + 50])
        out.extend(get_json(api(f"works?filter=openalex_id:{quote(grp, safe='|')}&per-page=50&select={SELECT}"),
                            refresh).get("results", []))
    return out


def fetch_forward(anchor_id, refresh=False):
    out, cursor, pages = [], "*", 0
    while cursor and pages < MAX_FORWARD_PAGES:
        data = get_json(api(f"works?filter=cites:{anchor_id}&per-page={PER_PAGE}"
                            f"&cursor={quote(cursor, safe='')}&select={SELECT}"), refresh)
        out.extend(data.get("results", []))
        cursor = (data.get("meta") or {}).get("next_cursor")
        pages += 1
    return out, pages, bool(cursor)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--refresh", action="store_true")
    args = ap.parse_args()
    anchors = json.loads((LOGS / f"{SLUG}-cold-start-anchors.json").read_text())

    resolved, unresolved, deferred = [], [], []
    for a in anchors:
        try:
            w, s, via = resolve(a, args.refresh)
        except RuntimeError:
            deferred.append(a["title"]); continue
        # DOI matches are authoritative; only title-search fallbacks face the similarity floor.
        if w is None or (via != "doi" and s < RESOLVE_SIM_MIN):
            unresolved.append({"title": a["title"], "similarity": round(s, 3),
                               "is_book": bool(a.get("note")), "via": via})
            continue
        cell = a.get("provisional_cell")
        is_decoy = a.get("query_cluster_family") == "ROUTING_DECOY"
        is_theory = cell == THEORY_CELL
        cb = w.get("cited_by_count") or 0
        fwd_eligible = (not is_decoy) and not (is_theory and cb > FWD_THEORY_CAP)
        resolved.append({"anchor": a, "openalex": flatten(w), "title_similarity": round(s, 4),
                         "referenced_works": w.get("referenced_works") or [],
                         "is_decoy": is_decoy, "is_theory": is_theory,
                         "is_empirical_seed": (cell in EMPIRICAL_CELLS) and not is_decoy,
                         "forward_eligible": fwd_eligible})
    (LOGS / f"{SLUG}-anchor-resolution.json").write_text(
        json.dumps({"resolved": resolved, "unresolved": unresolved, "deferred": deferred},
                   indent=2, ensure_ascii=False))

    # Tier A = resolved empirical seeds, enriched.
    tier_a = []
    for it in resolved:
        if it["is_empirical_seed"]:
            rec = dict(it["openalex"])
            rec["provisional_cell"] = it["anchor"].get("provisional_cell")
            rec["query_cluster_family"] = it["anchor"].get("query_cluster_family")
            rec["provenance_channel"] = it["anchor"].get("provenance_channel")
            rec["title_similarity"] = it["title_similarity"]
            rec["gold_status"] = "tier_a_candidate_not_frozen"
            tier_a.append(rec)
    tier_a.sort(key=lambda r: (r["provisional_cell"], -(r.get("year") or 0)))
    (LOGS / f"{SLUG}-tier-a.json").write_text(json.dumps(tier_a, indent=2, ensure_ascii=False))

    # Tier B = backward (all) + forward (eligible) citation frame.
    discovered = defaultdict(lambda: {"channels": set(), "seeds": set(), "work": None})
    fwd_pages = 0
    fwd_included, fwd_excluded, capped = [], [], []
    for it in resolved:
        seed = it["openalex"]["paperId"]
        try:
            for w in fetch_by_ids(it["referenced_works"], args.refresh):
                wid = (w.get("id") or "").rsplit("/", 1)[-1]
                if wid and wid != seed:
                    discovered[wid]["channels"].add("backward_reference")
                    discovered[wid]["seeds"].add(seed); discovered[wid]["work"] = w
        except RuntimeError:
            deferred.append(f"backward:{it['openalex']['title'][:40]}")
        if it["forward_eligible"]:
            try:
                fwd, pages, cap = fetch_forward(seed, args.refresh)
                fwd_pages += pages
                if cap:
                    capped.append(seed)
                fwd_included.append((it["openalex"]["title"], it["openalex"].get("cited_by_count")))
                for w in fwd:
                    wid = (w.get("id") or "").rsplit("/", 1)[-1]
                    if wid and wid != seed:
                        discovered[wid]["channels"].add("forward_citation")
                        discovered[wid]["seeds"].add(seed); discovered[wid]["work"] = w
            except RuntimeError:
                deferred.append(f"forward:{it['openalex']['title'][:40]}")
        else:
            fwd_excluded.append((it["openalex"]["title"], it["openalex"].get("cited_by_count"),
                                 "routing_decoy" if it["is_decoy"] else "theory_cloud>cap"))

    anchor_ids = {it["openalex"]["paperId"] for it in resolved}
    by_doi, by_title, frame, dups = {}, {}, [], 0
    for wid, it in discovered.items():
        if wid in anchor_ids:
            continue
        rec = flatten(it["work"])
        doi, tkey = rec["doi"], norm_title(rec["title"])
        existing = by_doi.get(doi) if doi else by_title.get(tkey)
        if existing is not None:
            dups += 1
            existing["discovery_channels"] = sorted(set(existing["discovery_channels"]) | it["channels"])
            existing["seed_ids"] = sorted(set(existing["seed_ids"]) | it["seeds"])
            continue
        rec["discovery_channels"] = sorted(it["channels"])
        rec["seed_ids"] = sorted(it["seeds"])
        rec["gold_status"] = "tier_b_candidate_unscreened"
        frame.append(rec)
        if doi:
            by_doi[doi] = rec
        if tkey:
            by_title[tkey] = rec
    frame.sort(key=lambda r: (-len(r["discovery_channels"]), -(r.get("year") or 0), r["title"]))
    (LOGS / f"{SLUG}-tier-b-frame.json").write_text(json.dumps(frame, indent=2, ensure_ascii=False))

    both = sum(len(r["discovery_channels"]) > 1 for r in frame)
    absn = sum(len(r.get("abstract") or "") >= 30 for r in frame)
    L = [f"# A4 Tier-A / Tier-B frame — {SLUG}", "",
         "Candidate frame, **not** screened or frozen. Two-tier GACS: Tier A = direct-empirical seeds; "
         "Tier B = orthogonal backward+forward citation frame.", "",
         "## Tier A (empirical seeds, enriched)", "",
         f"- resolved empirical seeds: **{len(tier_a)}**",
         "", "| cell | n |", "|---|---|"]
    cells = defaultdict(int)
    for r in tier_a:
        cells[r["provisional_cell"]] += 1
    for c, n in sorted(cells.items()):
        L.append(f"| {c} | {n} |")
    L += ["", "## Anchor resolution", "",
          f"- input anchors: {len(anchors)}",
          f"- OpenAlex-resolved: {len(resolved)}",
          f"- unresolved (below sim {RESOLVE_SIM_MIN}): {len(unresolved)}",
          f"- deferred (network/429, resume on re-run): {len(deferred)}",
          "", "## Tier B (citation frame)", "",
          f"- deduplicated candidates: **{len(frame):,}**",
          f"- found by both channels: {both:,}",
          f"- with usable abstracts: {absn:,}",
          f"- duplicates merged: {dups:,}",
          f"- forward pages requested/cached: {fwd_pages}",
          f"- seeds hitting the {MAX_FORWARD_PAGES}-page cap: {len(capped)}",
          "", "### Forward-seed policy (transparency)", "",
          f"Forward-cited anchors ({len(fwd_included)}):"]
    for t, cb in sorted(fwd_included, key=lambda x: -(x[1] or 0)):
        L.append(f"- ✓ {t[:60]} (cb={cb})")
    L += ["", f"Forward-EXCLUDED anchors ({len(fwd_excluded)}) — backward refs still used:"]
    for t, cb, why in sorted(fwd_excluded, key=lambda x: -(x[1] or 0)):
        L.append(f"- ✗ {t[:55]} (cb={cb}, {why})")
    if unresolved:
        L += ["", "## Unresolved anchors", ""] + \
             [f"- {x['title'][:60]} (sim {x['similarity']}{', book' if x['is_book'] else ''})" for x in unresolved]
    if deferred:
        L += ["", "## Deferred (resume on re-run)", ""] + [f"- {d}" for d in deferred]
    L += ["", "## Next gate", "",
          "Screen the whole Tier-B frame with the B.1 topical/estimand rubric (routing on the frozen "
          "B.1/A.2 boundary). Do NOT prune the frame by vocabulary distance from the future production "
          "query — that would bias Recall(B). The routing decoys must surface as route-away at screen."]
    (LOGS / f"{SLUG}-tier-ab-log.md").write_text("\n".join(L) + "\n")
    print(f"resolved {len(resolved)}/{len(anchors)} | Tier A {len(tier_a)} | Tier B frame {len(frame)} "
          f"(both {both}, abstracts {absn}, dups {dups}) | fwd pages {fwd_pages} | deferred {len(deferred)}",
          file=sys.stderr)
    if deferred:
        print(f"WARNING: {len(deferred)} deferred (network); re-run to resume", file=sys.stderr)


if __name__ == "__main__":
    main()
