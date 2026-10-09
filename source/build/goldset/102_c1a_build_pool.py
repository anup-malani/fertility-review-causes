#!/usr/bin/env python3
"""
102 (c1a) — C.1.a (TICK-098) stage-3 pool assembly.

Builds the blinded-screen pool from three sources, deduped on OpenAlex work id:
  (A) cold-start ANCHORS: ~15 seminal + CLEAN-cell empirical papers, resolved LIVE against OpenAlex by
      title (Jaccard >= 0.60 AND year within +/-1). No id is hand-typed; a miss is carried as
      verified=False for the RA, never faked (the OAS ghost-citation discipline).
  (B) CITATION frame: for every verified anchor, its OpenAlex referenced_works (backward) and the works
      that cite it (forward, cites:<id>), capped per anchor.
  (C) PRODUCTION identified core: the 101-probe recall union AND fertility outcome AND an identified-
      design marker (the ~166 records that carry an extractable causal estimate).

Abstracts are reconstructed from abstract_inverted_index. Counting/metadata only; no PDFs fetched here.
Output: literature/search-logs/income-effect-normal-good-pool.json (+ -pool-log.md).
"""
import json, os, re, subprocess, time, urllib.parse, unicodedata, sys

SLUG = "income-effect-normal-good"
MAILTO = "shravanh@uchicago.edu"
BASE = "https://api.openalex.org/works"
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
LOGS = os.path.join(ROOT, "literature", "search-logs")
OUT = os.path.join(LOGS, f"{SLUG}-pool.json")
OUT_LOG = os.path.join(LOGS, f"{SLUG}-pool-log.md")
CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "c1a_pool_cache.json")

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
    ("An Economic Analysis of Fertility", 1960, "THEORY"),
    ("Fertility Theories: Can They Explain the Negative Fertility-Income Relationship?", 2011, "THEORY"),
    ("The economics of fertility in developed countries", 1997, "THEORY"),
    ("An Economic History of Fertility in the United States: 1826-1960", 2008, "THEORY"),
    # CLEAN-cell empirical (non-labor income / wealth shocks)
    ("Do Family Wealth Shocks Affect Fertility Choices? Evidence from the Housing Market", 2013, "CLEAN_WEALTH"),
    ("House prices and birth rates: The impact of the real estate market on the decision to have a baby", 2014, "CLEAN_WEALTH"),
    ("Are Children Normal?", 2013, "CLEAN_WINDFALL"),
    ("Are Children Really Inferior Goods? Evidence from Displacement-Driven Income Shocks", 2010, "MIXED_WALL_C2E"),
    ("Male Earnings, Marriageable Men, and Nonmarital Fertility: Evidence from the Fracking Boom", 2018, "CLEAN_WINDFALL"),
    ("Wealth, Health, and Child Development: Evidence from Administrative Data on Swedish Lottery Players", 2016, "CLEAN_LOTTERY"),
    ("The Effect of Wealth on Individual and Household Labor Supply: Evidence from Swedish Lotteries", 2017, "CLEAN_LOTTERY"),
    ("The effect of a universal child benefit on conception, abortion, and household labor supply", 2013, "TRANSFER"),
    ("Financial Incentives and Fertility", 2013, "TRANSFER"),
    ("Subsidizing the Stork: New Evidence on Tax Incentives and Fertility", 2005, "TRANSFER"),
    ("The Fertility Response to the Great Recession in Europe", 2013, "CONTEXT"),
]

# Production identified-core query (mirrors 101 probe: C1A union AND outcome AND identified markers).
C1A = ('("income effect" OR "household income" OR "income elasticity" OR "permanent income" '
       'OR "wealth effect" OR "income shock" OR "cash transfer" OR "lottery")')
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
        q = urllib.parse.quote(f"{C1A} AND {OUTCOME} AND {IDENT}")
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
        f.write(f"# C.1.a pool assembly log — {time.strftime('%Y-%m-%d')}\n\n")
        f.write(f"Pool: **{len(recs)}** unique works. Anchors verified {len(verified)}/{len(ANCHORS)}. "
                f"OA (full text retrievable): **{oa}**.\n\n")
        f.write(f"By source bucket: {by_src}\n\n## Anchor resolution\n\n" + "\n".join(log) + "\n")
    print(f"\npool={len(recs)}  anchors={len(verified)}/{len(ANCHORS)}  OA={oa}")
    print(f"wrote {OUT}\nwrote {OUT_LOG}")


if __name__ == "__main__":
    main()
