#!/usr/bin/env python3
"""
91_a13_citation_frame.py — A.13 (breastfeeding and lactational amenorrhea), stage-3 Tier-A/Tier-B frame.

Mirrors 91_a19 / 91_d1d: resolve the existence-verified cold-start anchors in OpenAlex and build the
orthogonal citation frame — backward references + forward citations — that the blinded screen classifies.

Design decisions specific to A.13
---------------------------------
  * FORWARD-SEED THE BREASTFEEDING-SPECIFIC EMPIRICAL CORE, keyed on the PRIMARY cell. The forward-seed
    anchors are the three breastfeeding-specific identified designs: the LAM-efficacy / amenorrhea
    design (Kennedy & Visness 1992 -> LAM_EFFICACY), the natural-fertility birth-spacing study
    (Konner & Worthman 1980 -> BIRTH_INTERVAL), and the suckling-prolactin mechanism study
    (Howie & McNeilly 1982 -> SUCKLING_MECHANISM). The Bongaarts 1978 FRAMEWORK paper and the
    Bongaarts & Potter 1983 book are HELD OUT of forward-seeding: their citers span every proximate
    determinant (mortality, marriage, contraception, abstinence), not breastfeeding specifically, so
    forward-seeding them would flood the frame with cross-determinant noise. They contribute BACKWARD
    references only. The six wall decoys (A.2 contraception, A.22 energy-balance, A.14 abstinence,
    A.1 infant-mortality, A.15 fecundity, the infant-health HOMONYM — notably Victora 2016, which is
    cited by thousands of infant-health papers) likewise contribute backward references and routing
    tests only, never forward seeds.
  * DOI-FIRST RESOLUTION. Anchors resolve by their existence-verified DOI first, falling back to a
    cited_by-sorted title.search — robust against a more-cited off-title paper capturing the resolver.
  * BUDGET-SAFE AND RESUMABLE. Every request cached; a budget exhaustion saves state and exits 2.

LEAKAGE WALL: an anchor's own study seeds the frame here; its search vocabulary must NOT later be mined
as production-query terms for A.13.

Outputs:
  literature/search-logs/breastfeeding-lactational-amenorrhea-anchor-resolution.json
  literature/search-logs/breastfeeding-lactational-amenorrhea-tier-a.json
  literature/search-logs/breastfeeding-lactational-amenorrhea-tier-b-frame.json
  literature/search-logs/breastfeeding-lactational-amenorrhea-tier-ab-log.md
"""
import json, os, subprocess, sys, time

SLUG = "breastfeeding-lactational-amenorrhea"
MAILTO = "shravanh@uchicago.edu"
BASE = "https://api.openalex.org/works"
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
LOGS = os.path.join(ROOT, "literature", "search-logs")
ANCHORS_JSON = os.path.join(LOGS, f"{SLUG}-cold-start-anchors.json")
CACHE = os.path.join(ROOT, "temp", "a13-frame-cache.json")
SELECT = "id,doi,title,publication_year,abstract_inverted_index,cited_by_count,referenced_works"

FWD_PER_ANCHOR_CAP = 800
FWD_GLOBAL_CAP = 3000
TITLE_JACCARD_MIN = 0.6
FORWARD_SEED_CELLS = {"LAM_EFFICACY", "BIRTH_INTERVAL", "SUCKLING_MECHANISM"}

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


def resolve_anchor(title, doi=None):
    # DOI-first: the anchor step already existence-verified the DOI, so a doi filter is the most robust
    # resolver and avoids the cited_by-sorted title.search landing a more-cited off-title paper.
    if doi:
        clean = doi.replace("https://doi.org/", "").strip()
        try:
            d = oa_get({"filter": f"doi:{clean}", "per-page": "1", "select": SELECT})
            hits = d.get("results", [])
            if hits:
                return hits[0], jaccard(title, hits[0].get("title") or "")
        except Refused:
            pass
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

    resolution, tier_a, refs_all, fwd_all = [], [], {}, {}
    anchor_ids = set()
    try:
        for a in verified:
            w, jac = resolve_anchor(a["title"], a.get("doi"))
            rec = {"title": a["title"], "cell": a["provisional_cell"], "family": a.get("family"),
                   "crossref_doi": a.get("doi"), "resolved": bool(w), "match_jaccard": round(jac, 3)}
            if w:
                rec.update(oa_id=w["id"], oa_doi=w.get("doi"), oa_year=w.get("publication_year"),
                           cited_by_count=w.get("cited_by_count"),
                           n_referenced=len(w.get("referenced_works") or []))
                anchor_ids.add(w["id"])
                for rid in (w.get("referenced_works") or []):
                    refs_all[rid] = rec.get("cell")
                is_seed = a.get("provisional_cell") in FORWARD_SEED_CELLS
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
    L = ["# A.13 Tier-A/Tier-B citation frame — build log", "",
         "Generated by `source/build/goldset/91_a13_citation_frame.py`. Anchors resolved to the",
         "OpenAlex version of record DOI-first (cited_by-sorted title.search fallback). Forward-seeded",
         "on the breastfeeding-specific empirical core only (LAM_EFFICACY, BIRTH_INTERVAL,",
         "SUCKLING_MECHANISM); the Bongaarts framework paper + book and the six wall decoys contribute",
         "backward references and routing tests only (their citers span all proximate determinants or,",
         "for Victora 2016, the infant-health literature).", "",
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
