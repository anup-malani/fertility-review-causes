#!/usr/bin/env python3
"""
202 (c2e) — C.2.e (TICK-099) stage-3 pool assembly.

Builds the blinded-screen pool from three sources, deduped on OpenAlex work id:
  (A) cold-start ANCHORS: ~15 seminal + CLEAN-cell empirical papers, resolved LIVE against OpenAlex by
      title (Jaccard >= 0.60 AND year within +/-1). No id is hand-typed; a miss is carried as
      verified=False for the RA, never faked (the OAS ghost-citation discipline).
  (B) CITATION frame: for every verified anchor, its OpenAlex referenced_works (backward) and the works
      that cite it (forward, cites:<id>), capped per anchor.
  (C) PRODUCTION identified core: the 201-probe recall union AND fertility outcome AND an identified-
      design marker (the ~211 records that carry an extractable causal estimate).

Abstracts are reconstructed from abstract_inverted_index. Counting/metadata only; no PDFs fetched here.
Output: literature/search-logs/female-wage-opportunity-cost-pool.json (+ -pool-log.md).
"""
import json, os, re, subprocess, time, urllib.parse, unicodedata, sys

SLUG = "female-wage-opportunity-cost"
MAILTO = "shravanh@uchicago.edu"
BASE = "https://api.openalex.org/works"
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
LOGS = os.path.join(ROOT, "literature", "search-logs")
OUT = os.path.join(LOGS, f"{SLUG}-pool.json")
OUT_LOG = os.path.join(LOGS, f"{SLUG}-pool-log.md")
CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "c2e_pool_cache.json")

CITERS_PER_ANCHOR = 120   # forward citation cap per anchor
JACCARD_MIN, YEAR_TOL = 0.60, 1


def api_key():
    try:
        for ln in open(os.path.join(ROOT, ".env")):
            if ln.startswith("OPENALEX_API_KEY="):
                return ln.split("=", 1)[1].strip().strip('"') or None
    except FileNotFoundError:
        pass
    return None


KEY = api_key()
PACE = 0.2 if KEY else 1.2
cache = json.load(open(CACHE)) if os.path.exists(CACHE) else {}


def _norm(s):
    s = unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9 ]", " ", s)


def jaccard(a, b):
    A, B = set(_norm(a).split()), set(_norm(b).split())
    return len(A & B) / len(A | B) if A | B else 0.0


def get(url):
    if url in cache:
        return cache[url]
    u = url + ("&" if "?" in url else "?") + f"mailto={MAILTO}"
    if KEY:
        u += f"&api_key={KEY}"
    p = subprocess.run(["curl", "-s", "-S", "--max-time", "90", u], capture_output=True, text=True)
    if p.returncode != 0:
        raise RuntimeError(f"curl exit {p.returncode}")
    d = json.loads(p.stdout)
    cache[url] = d
    json.dump(cache, open(CACHE, "w"))
    time.sleep(PACE)
    return d


def abstract(rec):
    idx = rec.get("abstract_inverted_index")
    if not idx:
        return ""
    pos = {}
    for w, ps in idx.items():
        for p in ps:
            pos[p] = w
    return " ".join(pos[i] for i in sorted(pos))[:2000]


def slim(rec, source):
    return dict(id=rec["id"].rsplit("/", 1)[-1], title=rec.get("title") or "",
                year=rec.get("publication_year"), doi=(rec.get("doi") or "").replace("https://doi.org/", ""),
                cited_by=rec.get("cited_by_count"), source=source,
                oa=(rec.get("open_access") or {}).get("is_oa"),
                oa_url=(rec.get("open_access") or {}).get("oa_url"),
                abstract=abstract(rec))


ANCHORS = [
    # seminal / theory (do NOT count toward empirical recall)
    ("A Theory of the Allocation of Time", 1965, "THEORY"),              # Becker
    ("A New Approach to the Economic Theory of Fertility Behavior", 1973, "THEORY"),  # Willis
    ("Market Prices, Opportunity Costs, and Income Effects", 1963, "THEORY"),  # Mincer
    ("Female Labor Supply: A Survey", 1986, "THEORY"),                   # Killingsworth & Heckman
    ("The U-Shaped Female Labor Force Function in Economic Development and Economic History", 1994, "THEORY"),  # Goldin
    # CLEAN-cell empirical (wage / price-of-time / labor-demand shocks)
    ("The Emergence of Countercyclical U.S. Fertility", 1979, "CLEAN_WAGE"),  # Butz & Ward
    ("Changing World Prices, Women's Wages, and the Fertility Transition: Sweden, 1860-1910", 1985, "CLEAN_WAGE"),  # Schultz
    ("The relationship between wages and income and the timing and spacing of births: evidence from Swedish longitudinal data", 1990, "CLEAN_WAGE"),  # Heckman & Walker
    ("The Career Costs of Children", 2017, "CLEAN_PRICE_OF_TIME"),       # Adda, Dustmann, Stevens
    ("Manufacturing Growth and the Lives of Bangladeshi Women", 2015, "CLEAN_LABOR_DEMAND"),  # Heath & Mobarak
    ("Do Labor Market Opportunities Affect Young Women's Work and Family Decisions? Experimental Evidence from India", 2012, "CLEAN_LABOR_DEMAND"),  # Jensen
    ("The Baby Boom and World War II: A Macroeconomic Analysis", 2015, "CLEAN_LABOR_DEMAND"),  # Doepke, Hazan, Maoz
    ("The Power of the Pill: Oral Contraceptives and Women's Career and Marriage Decisions", 2002, "CONTEXT"),  # Goldin & Katz
    # MIXED / wall anchors
    ("When Work Disappears: Manufacturing Decline and the Falling Marriage Market Value of Young Men", 2019, "MIXED_WALL_C1A"),  # Autor, Dorn, Hanson
    ("Children and Their Parents' Labor Supply: Evidence from Exogenous Variation in Family Size", 1998, "REVERSE_WALL"),  # Angrist & Evans
]

# Production identified-core query (mirrors 201 probe: C2E union AND outcome AND identified markers).
C2E = ('("female wage" OR "female wages" OR "women\'s wages" OR "opportunity cost of time" '
       'OR "female labor force participation" OR "female labour force participation" '
       'OR "female labor supply" OR "female labour supply" OR "women\'s employment" '
       'OR "maternal employment" OR "substitution effect" OR "price of time" '
       'OR "returns to schooling" OR "gender wage gap" OR "minimum wage" OR "trade shock")')
OUTCOME = ('("fertility" OR "childbearing" OR "birth rate" OR "total fertility rate" '
           'OR "childlessness" OR "fecundity")')
IDENT = ('("instrumental variable" OR "difference-in-differences" OR "differences-in-differences" '
         'OR "natural experiment" OR "regression discontinuity" OR "randomized controlled trial" '
         'OR "event study" OR "synthetic control")')


def search_anchor(title, year):
    q = urllib.parse.quote(title)
    d = get(f"{BASE}?filter=title.search:{q}&per_page=5")
    best, bj = None, 0.0
    for rec in d.get("results", []):
        j = jaccard(title, rec.get("title") or "")
        if j > bj and (rec.get("publication_year") and abs(rec["publication_year"] - year) <= YEAR_TOL):
            best, bj = rec, j
    return (best, bj) if bj >= JACCARD_MIN else (None, bj)


def fetch_full(wid):
    return get(f"{BASE}/{wid}")


def main():
    pool, log = {}, []
    verified = []
    print("A — resolving anchors", flush=True)
    for title, year, cell in ANCHORS:
        rec, j = search_anchor(title, year)
        if rec:
            s = slim(rec, f"anchor:{cell}")
            pool[s["id"]] = s
            verified.append((s["id"], title, cell, rec))
            print(f"  ok  j={j:.2f}  {s['year']}  {s['title'][:70]}", flush=True)
            log.append(f"- OK (j={j:.2f}) [{cell}] {s['year']} — {s['title']}  doi:{s['doi']}")
        else:
            print(f"  MISS j={j:.2f}  {title[:70]}", flush=True)
            log.append(f"- MISS (best j={j:.2f}) [{cell}] {year} — {title}  (carried for RA, not faked)")

    print("B — citation frame (backward refs + forward citers)", flush=True)
    for wid, title, cell, rec in verified:
        for rid in (rec.get("referenced_works") or [])[:60]:
            rid2 = rid.rsplit("/", 1)[-1]
            if rid2 not in pool:
                try:
                    pool[rid2] = slim(fetch_full(rid2), "cite:backward")
                except Exception:
                    pass
        try:
            d = get(f"{BASE}?filter=cites:{wid}&per_page={CITERS_PER_ANCHOR}&sort=cited_by_count:desc")
            for r in d.get("results", []):
                s = slim(r, "cite:forward")
                pool.setdefault(s["id"], s)
        except Exception:
            pass
        print(f"  cited {title[:50]} -> pool now {len(pool)}", flush=True)

    print("C — production identified core (paginated)", flush=True)
    cursor = "*"
    coreN = 0
    while cursor:
        q = urllib.parse.quote(f"{C2E} AND {OUTCOME} AND {IDENT}")
        d = get(f"{BASE}?filter=title_and_abstract.search:{q}&per_page=200&cursor={cursor}")
        for r in d.get("results", []):
            s = slim(r, "production:identified")
            if s["id"] not in pool:
                pool[s["id"]] = s
            coreN += 1
        cursor = (d.get("meta") or {}).get("next_cursor")
        if not d.get("results"):
            break
    print(f"  production identified core records seen: {coreN}", flush=True)

    recs = list(pool.values())
    json.dump({"slug": SLUG, "generated": time.strftime("%Y-%m-%d"), "n": len(recs),
               "anchors_verified": len(verified), "anchors_total": len(ANCHORS),
               "records": recs}, open(OUT, "w"), indent=1)
    by_src = {}
    for r in recs:
        by_src[r["source"].split(":")[0]] = by_src.get(r["source"].split(":")[0], 0) + 1
    oa = sum(1 for r in recs if r["oa"])
    with open(OUT_LOG, "w") as f:
        f.write(f"# C.2.e pool assembly log — {time.strftime('%Y-%m-%d')}\n\n")
        f.write(f"Pool: **{len(recs)}** unique works. Anchors verified {len(verified)}/{len(ANCHORS)}. "
                f"OA (full text retrievable): **{oa}**.\n\n")
        f.write(f"By source bucket: {by_src}\n\n## Anchor resolution\n\n" + "\n".join(log) + "\n")
    print(f"\npool={len(recs)}  anchors={len(verified)}/{len(ANCHORS)}  OA={oa}")
    print(f"wrote {OUT}\nwrote {OUT_LOG}")


if __name__ == "__main__":
    main()
