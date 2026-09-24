#!/usr/bin/env python3
"""
91_d2c_citation_frame.py — D.2.c (son preference), stage-3 Tier-A/Tier-B citation frame.

Mirrors 91_a14 / 65 (B.1): resolve the existence-verified cold-start anchors in OpenAlex and build the
orthogonal citation frame — backward references + forward citations — that the blinded screen classifies.

Design decisions specific to D.2.c
----------------------------------
  * FORWARD-SEED THE EMPIRICAL CORE ONLY. The son-preference theory canon (Das Gupta 1987, cited
    thousands) and the six registered-wall decoys (A.10 adult sex ratio, A.4 general abortion, A.8 parity
    stopping, C.3.c old-age security, D.2.a gender equity, A.1 child mortality) are held OUT of forward-
    seeding — their forward sets are enormous and off-estimand — but still contribute BACKWARD references
    and routing tests. Forward-seeds: differential-stopping (Ben-Porath & Welch, Clark, Arnold-Choe-Roy),
    the sex-selection substitution naturals (Ebenstein, Lin-Liu-Qian, Jayachandran), and Chung-Das Gupta
    norm intensity.
  * RESOLVE TO THE VERSION OF RECORD, NOT THE PREPRINT. Jayachandran verified to the NBER working-paper
    year (version drift); the resolver lands the most-cited OpenAlex version by title regardless.
  * BUDGET-SAFE AND RESUMABLE. Every request cached; a budget exhaustion saves state and exits 2.

LEAKAGE WALL: an anchor's own study seeds the frame here; its search vocabulary must NOT later be mined
as production-query terms for D.2.c.

Outputs:
  literature/search-logs/son-preference-cultural-anchor-resolution.json
  literature/search-logs/son-preference-cultural-tier-a.json
  literature/search-logs/son-preference-cultural-tier-b-frame.json
  literature/search-logs/son-preference-cultural-tier-ab-log.md
"""
import json, os, subprocess, sys, time

SLUG = "son-preference-cultural"
MAILTO = "shravanh@uchicago.edu"
BASE = "https://api.openalex.org/works"
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
LOGS = os.path.join(ROOT, "literature", "search-logs")
ANCHORS_JSON = os.path.join(LOGS, f"{SLUG}-cold-start-anchors.json")
CACHE = os.path.join(ROOT, "temp", "d2c-frame-cache.json")
SELECT = "id,doi,title,publication_year,abstract_inverted_index,cited_by_count,referenced_works"

FWD_PER_ANCHOR_CAP = 500
FWD_GLOBAL_CAP = 3000
TITLE_JACCARD_MIN = 0.6

sys.path.insert(0, os.path.join(ROOT, "source", "lib"))
from textnorm import norm, oa_search_safe  # noqa: E402


def _api_key():
    try:
        for line in open(os.path.join(ROOT, ".env")):
            if line.startswith("OPENALEX_API_KEY="):
                return line.split("=", 1)[1].strip().strip('"') or None
    except FileNotFoundError:
        pass
    return None


API_KEY = _api_key()
PACE = 0.2 if API_KEY else 1.2

cache = json.load(open(CACHE)) if os.path.exists(CACHE) else {}


class BudgetExhausted(Exception):
    pass


class Refused(Exception):
    pass


def _save_cache():
    os.makedirs(os.path.dirname(CACHE), exist_ok=True)
    json.dump(cache, open(CACHE, "w"), indent=0)


def oa_get(params, _retried=False):
    key = "oa::" + json.dumps(params, sort_keys=True)
    if key in cache:
        return cache[key]
    args = ["curl", "-sS", "--max-time", "120", "-G", BASE]
    for k, v in params.items():
        args += ["--data-urlencode", f"{k}={v}"]
    args += ["--data-urlencode", f"mailto={MAILTO}"]
    if API_KEY:
        args += ["--data-urlencode", f"api_key={API_KEY}"]
    r = subprocess.run(args, capture_output=True, text=True)
    if r.returncode != 0:
        raise Refused(f"curl rc={r.returncode}: {r.stderr.strip()[:160]}")
    try:
        d = json.loads(r.stdout)
    except json.JSONDecodeError:
        raise Refused(f"non-JSON body: {r.stdout[:160]!r}")
    if "error" in d:
        body = json.dumps(d)
        if "Insufficient budget" in body:
            raise BudgetExhausted(body[:200])
        if not _retried and ("Rate limit" in body or "boolean" in body):
            time.sleep(2.0)
            return oa_get(params, _retried=True)
        raise Refused(f"api error: {body[:200]}")
    cache[key] = d
    _save_cache()
    time.sleep(PACE)
    return d


def abstract_text(inv):
    if not inv:
        return ""
    positions = []
    for word, idxs in inv.items():
        for i in idxs:
            positions.append((i, word))
    positions.sort()
    return " ".join(w for _, w in positions)


def toks(s):
    return set(norm(s).split())


def jaccard(a, b):
    ta, tb = toks(a), toks(b)
    return len(ta & tb) / len(ta | tb) if ta and tb else 0.0


def resolve_anchor(title):
    safe = oa_search_safe(title).replace(",", " ")
    safe = " ".join(safe.split())
    d = oa_get({"filter": f"title.search:{safe}", "sort": "cited_by_count:desc",
                "per-page": "5", "select": SELECT})
    best, best_jac = None, 0.0
    for w in d.get("results", []):
        jac = jaccard(title, w.get("title") or "")
        if jac > best_jac:
            best, best_jac = w, jac
    return (best, best_jac) if best_jac >= TITLE_JACCARD_MIN else (None, best_jac)


def forward_cites(work_id, cap):
    short = work_id.rsplit("/", 1)[-1]
    recs, cursor = [], "*"
    while cursor and len(recs) < cap:
        d = oa_get({"filter": f"cites:{short}", "per-page": "200", "cursor": cursor, "select": SELECT})
        recs.extend(d.get("results", []))
        cursor = (d.get("meta") or {}).get("next_cursor")
        if not d.get("results"):
            break
    return recs[:cap]


def fetch_meta(ids):
    out = []
    for i in range(0, len(ids), 50):
        chunk = ids[i:i + 50]
        short = [x.rsplit("/", 1)[-1] for x in chunk]
        d = oa_get({"filter": "openalex_id:" + "|".join(short), "per-page": "50", "select": SELECT})
        out.extend(d.get("results", []))
    return out


def as_record(w, channel):
    return {"id": w.get("id"), "doi": w.get("doi"), "title": w.get("title"),
            "year": w.get("publication_year"), "cited_by_count": w.get("cited_by_count"),
            "abstract": abstract_text(w.get("abstract_inverted_index")), "source_channel": channel}


def main():
    anchors = json.load(open(ANCHORS_JSON))
    verified = [a for a in anchors if a.get("identity_verified")]
    forward_families = {"differential-stopping", "sexsel-substitution", "norm-intensity"}

    resolution, tier_a, refs_all, fwd_all = [], [], {}, {}
    anchor_ids = set()
    try:
        for a in verified:
            w, jac = resolve_anchor(a["title"])
            rec = {"title": a["title"], "cell": a["provisional_cell"], "family": a.get("family"),
                   "crossref_doi": a.get("doi"), "resolved": bool(w), "match_jaccard": round(jac, 3)}
            if w:
                rec.update(oa_id=w["id"], oa_doi=w.get("doi"), oa_year=w.get("publication_year"),
                           cited_by_count=w.get("cited_by_count"),
                           n_referenced=len(w.get("referenced_works") or []))
                anchor_ids.add(w["id"])
                for rid in (w.get("referenced_works") or []):
                    refs_all[rid] = rec.get("cell")
                is_seed = a.get("family") in forward_families
                if is_seed:
                    tier_a.append(as_record(w, "anchor_seed"))
                    rec["forward_seeded"] = True
            resolution.append(rec)

        fwd_records = []
        seed_ids = [r["oa_id"] for r in resolution if r.get("forward_seeded")]
        for sid in seed_ids:
            if sum(len(v) for v in fwd_all.values()) >= FWD_GLOBAL_CAP:
                break
            recs = forward_cites(sid, FWD_PER_ANCHOR_CAP)
            fwd_all[sid] = [w["id"] for w in recs]
            fwd_records.extend(recs)

        fwd_ids = {w["id"] for w in fwd_records}
        need_meta = [rid for rid in refs_all if rid not in fwd_ids and rid not in anchor_ids]
        back_records = fetch_meta(need_meta)
    except BudgetExhausted as e:
        _save_cache()
        print(f"\nBUDGET EXHAUSTED mid-build: {e}\nProgress cached to {CACHE}; re-run tomorrow to "
              f"resume from the cache. No partial frame written.", file=sys.stderr)
        return 2

    tier_b, seen = [], set()
    for w in fwd_records:
        if w["id"] in anchor_ids or w["id"] in seen:
            continue
        seen.add(w["id"])
        tier_b.append(as_record(w, "forward_citation"))
    for w in back_records:
        if w["id"] in anchor_ids or w["id"] in seen:
            continue
        seen.add(w["id"])
        tier_b.append(as_record(w, "backward_reference"))

    with_abstract = [r for r in tier_b if r["abstract"]]
    json.dump(resolution, open(os.path.join(LOGS, f"{SLUG}-anchor-resolution.json"), "w"), indent=2)
    json.dump(tier_a, open(os.path.join(LOGS, f"{SLUG}-tier-a.json"), "w"), indent=2)
    json.dump(tier_b, open(os.path.join(LOGS, f"{SLUG}-tier-b-frame.json"), "w"), indent=2)

    n_res = sum(1 for r in resolution if r["resolved"])
    n_fwd = sum(1 for r in tier_b if r["source_channel"] == "forward_citation")
    n_back = sum(1 for r in tier_b if r["source_channel"] == "backward_reference")
    L = ["# D.2.c Tier-A/Tier-B citation frame — build log", "",
         "Generated by `source/build/goldset/91_d2c_citation_frame.py`. Anchors resolved to the",
         "OpenAlex version of record by title (cited_by-sorted). Forward-seeded on the empirical core",
         "only; theory + wall decoys contribute backward references and routing tests only.", "",
         f"- Anchors resolved: **{n_res}/{len(verified)}** verified anchors.",
         f"- Tier A (empirical seeds): **{len(tier_a)}**.",
         f"- Tier B candidates: **{len(tier_b)}** ({n_fwd} forward, {n_back} backward); "
         f"**{len(with_abstract)}** with usable abstracts.", "",
         "## Anchor resolution", "",
         "| anchor | cell | resolved | jaccard | cited_by | refs | fwd-seed |", "|---|---|---|---|---|---|---|"]
    for r in resolution:
        L.append(f"| {r['title'][:44]} | {r['cell']} | {r['resolved']} | {r['match_jaccard']} | "
                 f"{r.get('cited_by_count','')} | {r.get('n_referenced','')} | {r.get('forward_seeded', False)} |")
    open(os.path.join(LOGS, f"{SLUG}-tier-ab-log.md"), "w").write("\n".join(L) + "\n")

    print(f"anchors resolved: {n_res}/{len(verified)}")
    print(f"Tier A seeds: {len(tier_a)}")
    print(f"Tier B: {len(tier_b)} ({n_fwd} fwd, {n_back} back); {len(with_abstract)} with abstracts")
    print(f"cache: {CACHE}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
