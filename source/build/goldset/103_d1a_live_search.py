#!/usr/bin/env python3
r"""
103_d1a_live_search.py — D.1.a, GACS stage C1. The clustered production pull.

Runs the frozen production query against OpenAlex `title.search`, one cursor-paginated request stream
per cluster, and takes the UNION across clusters. Title-only, because that is the operationalisation
A6b's cross-validation selected; abstracts enter downstream at the screen, not at the search.

THE OPERATIONALISATION IS THE POINT, AND A6c GOT IT WRONG ONCE. The A6c report first recommended
Semantic Scholar bulk search. That was reversed: S2's bulk endpoint cannot restrict matching to
titles, and terms chosen for title precision explode across abstracts -- 19x to 39x per cluster here,
498,007 records against 18,123. Pulling there would have retrieved a differently-defined corpus than
the one the CV validated. The same trap is documented in the OAS chapter's `43_live_search.py`.

NO WILDCARDS. `title.search` is stemmed, so `childless` and `childlessness` resolve to one postings
list (2,586 each). Stars are stripped; a star left in the query makes OpenAlex reject it outright.

RESUMABILITY IS NOT OPTIONAL HERE. OpenAlex's free tier is metered and small -- `95_` established
that a sixteen-row canon resolution exhausts a day's allowance. A pull of ~18k records at 200 per
page is ~90 requests and may well cross the allowance mid-run. Every page is cached under
`cache/d1a_live_search/`, the budget-exhaustion body is caught and treated as STOP-AND-RESUME rather
than as an empty page, and re-running continues where it left off at zero cost for work already done.
The failure this guards against is the one this chapter keeps meeting: a truncated pull that reports
a plausible count and reads as complete.

DEDUP IS DOI-FIRST, THEN NORMALIZED TITLE. Clusters overlap by construction -- a paper matching both
S3 and GENERIC_VALUES is returned by both streams -- so the per-cluster counts sum to an upper bound
and the union is the real corpus size. Cluster provenance is kept per record, because which clusters
retrieved a paper is the evidence A6b's sole-credit analysis was estimating.

LIVE GOLD RECALL. The pull is checked against the frozen Tier A and Tier B gold: does the real
universe actually recover the anchors the CV said it would? A6b's 92.1% Recall(B-only) was measured by
matching compiled terms against stored titles. This measures whether OpenAlex's stemmed index, its
coverage, and its title normalisation reproduce that in practice. A gap between the two is a finding
about the index rather than about the query.

Usage:
  python3 103_d1a_live_search.py --count    # per-cluster universe counts only (6 requests)
  python3 103_d1a_live_search.py            # full resumable pull

Output: literature/search-logs/{slug}-live-corpus.json
        literature/search-logs/{slug}-live-search-log.md
"""
import json, os, re, subprocess, sys, time, urllib.parse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import importlib.util

SLUG = "postmaterialism-individualism-secularization"
MAILTO = "shravanh@uchicago.edu"
UA = f"fertility-review/1.0 (mailto:{MAILTO})"

# OPENALEX_API_KEY IS THE DIFFERENCE BETWEEN THIS PULL COSTING NOTHING AND NOT RUNNING AT ALL.
# OpenAlex made keys mandatory in Feb 2026 and moved to usage-based pricing. A FREE key carries
# **$1 of usage per day**; a `title.search` request bills as a search query at $0.001 (the refusal
# body says `creditsRequired: 10`), so a free key is worth ~1,000 of them per day. This entire pull
# is ~95 page requests -- under ten cents, under a tenth of one day's free allowance.
#
# Without a key the requests fall to the unauthenticated demo tier, which is what every budget
# exhaustion on this chapter has actually been. The arithmetic only reconciles that way: 95 requests
# against a $1 allowance could never have exhausted it, and this run died at page 25 of the sixth
# cluster. `30_acquire_pass3.py` already read this variable; scripts 89-104 never did.
#
# Note also that entity lookup BY DOI OR ID IS FREE under the same pricing. The conclusion recorded
# at `95_d1a_canon_reresolve.py` that OpenAlex canon resolution is "dead, not throttled" was drawn
# unauthenticated and against title *search*; resolution by DOI costs nothing and should be retried.
OA_KEY = os.environ.get("OPENALEX_API_KEY", "").strip()
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
LOGS = os.path.join(ROOT, "literature", "search-logs")
CACHE_DIR = os.path.join(HERE, "cache", "d1a_live_search")
os.makedirs(CACHE_DIR, exist_ok=True)
PQ = os.path.join(LOGS, f"{SLUG}-production-query.json")
OUT_JSON = os.path.join(LOGS, f"{SLUG}-live-corpus.json")
OUT_MD = os.path.join(LOGS, f"{SLUG}-live-search-log.md")

PER_PAGE = 200
SLEEP = 0.6
SELECT = ("id,doi,title,publication_year,cited_by_count,authorships,primary_location,"
          "abstract_inverted_index,type,language")

_spec = importlib.util.spec_from_file_location("cv", os.path.join(HERE, "101_d1a_cv_breadth.py"))
cv = importlib.util.module_from_spec(_spec)
sys.modules["cv"] = cv
_spec.loader.exec_module(cv)


class BudgetExhausted(Exception):
    """OpenAlex refused on budget. Distinct from an empty page, and it must stay distinct."""


def oa_term(t):
    return re.sub(r"[*?]", "", (t or "").strip().lower()).strip()


def fetch(url, page_key):
    """Cached GET. Raises BudgetExhausted rather than returning an empty page."""
    cf = os.path.join(CACHE_DIR, page_key + ".json")
    if os.path.exists(cf):
        with open(cf) as fh:
            return json.load(fh)
    for attempt in range(5):
        p = subprocess.run(["curl", "-s", "-m", "90", "-A", UA, "-w", "\n%{http_code}", url],
                           capture_output=True, text=True)
        body, _, code = p.stdout.rpartition("\n")
        code = code.strip()
        if code in ("429", "503"):
            # Budget and rate limit share a status here; the body distinguishes them, and only a
            # true rate limit is worth retrying. "Insufficient budget" will not clear by waiting.
            if "insufficient budget" in body.lower() or "resets at midnight" in body.lower():
                raise BudgetExhausted(body[:300])
            time.sleep(min(3 * (2 ** attempt), 30))
            continue
        if code == "403" and "budget" in body.lower():
            raise BudgetExhausted(body[:300])
        if p.returncode == 0 and body.strip().startswith("{"):
            d = json.loads(body)
            if isinstance(d.get("error"), str) and "budget" in json.dumps(d).lower():
                raise BudgetExhausted(json.dumps(d)[:300])
            if "results" in d or "meta" in d:
                with open(cf, "w") as fh:
                    json.dump(d, fh)
                return d
        time.sleep(2 * (attempt + 1))
    return None


def unabstract(inv):
    if not inv:
        return None
    pos = {}
    for w, idxs in inv.items():
        for i in idxs:
            pos[i] = w
    return " ".join(pos[i] for i in sorted(pos)) or None


def shape(w):
    src = ((w.get("primary_location") or {}).get("source") or {})
    return {
        "openalex_id": (w.get("id") or "").rsplit("/", 1)[-1],
        "doi": (w.get("doi") or "").replace("https://doi.org/", "").lower() or None,
        "title": w.get("title"),
        "year": w.get("publication_year"),
        "cited_by_count": w.get("cited_by_count"),
        "authors": "; ".join(a["author"]["display_name"] for a in (w.get("authorships") or [])
                             if a.get("author"))[:400] or None,
        "venue": src.get("display_name") or "",
        "type": w.get("type"),
        "language": w.get("language"),
        "abstract": unabstract(w.get("abstract_inverted_index")),
    }


def build_filters(pq):
    out = "|".join(sorted({oa_term(t) for t in pq["outcome_terms"] if oa_term(t)}))
    return {c: f"title.search:{out},title.search:" +
               "|".join(sorted({oa_term(t) for t in terms if oa_term(t)}))
            for c, terms in pq["treatment_clusters"].items()}


def pull_cluster(cluster, filt, counts_only=False):
    """Cursor-paginate one cluster. Returns (records, count, pages, complete)."""
    recs, cursor, pages = [], "*", 0
    total = None
    while cursor:
        params = {"filter": filt, "per-page": 1 if counts_only else PER_PAGE,
                  "cursor": cursor, "select": "id" if counts_only else SELECT, "mailto": MAILTO}
        if OA_KEY:
            params["api_key"] = OA_KEY
        url = "https://api.openalex.org/works?" + urllib.parse.urlencode(params)
        key = f"{cluster}__{'count' if counts_only else pages}"
        try:
            d = fetch(url, key)
        except BudgetExhausted:
            # PARTIAL PROGRESS MUST SURVIVE THE EXCEPTION. The first version let BudgetExhausted
            # propagate out of the cluster loop, which discarded the 5,000 records already pulled
            # AND left the cluster out of the per-cluster table entirely -- so the report showed five
            # complete clusters and no row for the one that failed, which reads as a finished pull.
            # That is precisely the "truncated pull that looks complete" this script exists to
            # prevent, reintroduced by its own error handling.
            print(f"    {cluster}: BUDGET EXHAUSTED at page {pages} — "
                  f"{len(recs)} records kept, resumable", file=sys.stderr)
            raise BudgetExhausted(json.dumps({"cluster": cluster, "pages_done": pages,
                                              "records_kept": len(recs), "universe": total})) \
                from None
        if d is None:
            print(f"    {cluster}: page {pages} UNCONFIRMED — stopping this cluster",
                  file=sys.stderr)
            return recs, total, pages, False
        total = (d.get("meta") or {}).get("count", total)
        if counts_only:
            return [], total, 1, True
        recs.extend(shape(w) for w in (d.get("results") or []))
        pages += 1
        cursor = (d.get("meta") or {}).get("next_cursor")
        print(f"    {cluster}: page {pages}, {len(recs)}/{total}", file=sys.stderr)
        if not (d.get("results") or []):
            break
        time.sleep(SLEEP)
    return recs, total, pages, True


def main():
    counts_only = "--count" in sys.argv
    # Say which tier this run is on, out loud, before spending anything. A silent misconfiguration
    # that presents as a provider limitation is how this chapter concluded OpenAlex was unusable.
    print(f"  auth: OPENALEX_API_KEY {'SET -- $1/day free allowance' if OA_KEY else 'NOT SET'}"
          f"{'' if OA_KEY else ' -- running on the unauthenticated demo tier, which is almost'}"
          f"{'' if OA_KEY else ' certainly what every budget exhaustion here has been'}",
          file=sys.stderr)
    pq = json.load(open(PQ))
    filters = build_filters(pq)

    corpus, provenance, per_cluster, incomplete = {}, {}, {}, []
    budget_hit = None
    for cluster, filt in filters.items():
        print(f"  {cluster}", file=sys.stderr)
        try:
            recs, total, pages, complete = pull_cluster(cluster, filt, counts_only)
        except BudgetExhausted as e:
            budget_hit = f"{cluster}: {e}"
            incomplete.append(cluster)
            # Re-read the cached pages so the partial pull is recorded rather than discarded.
            recs, total, pages, complete = [], None, 0, False
            while True:
                cf = os.path.join(CACHE_DIR, f"{cluster}__{pages}.json")
                if not os.path.exists(cf):
                    break
                with open(cf) as fh:
                    d = json.load(fh)
                total = (d.get("meta") or {}).get("count", total)
                recs.extend(shape(w) for w in (d.get("results") or []))
                pages += 1
            per_cluster[cluster] = {"universe_count": total, "pulled": len(recs), "pages": pages,
                                    "complete": False}
            for r in recs:
                key = r["doi"] or ("t:" + cv.norm(r["title"])[:120])
                corpus.setdefault(key, r)
                provenance.setdefault(key, []).append(cluster)
            print(f"    kept {len(recs)} partial records from {cluster}", file=sys.stderr)
            break
        per_cluster[cluster] = {"universe_count": total, "pulled": len(recs), "pages": pages,
                                "complete": complete}
        if not complete:
            incomplete.append(cluster)
        for r in recs:
            # DOI-first, then normalized title. Preprint/version pairs share a title and not a DOI,
            # so title is the merge key of last resort, exactly as in the snowball.
            key = r["doi"] or ("t:" + cv.norm(r["title"])[:120])
            if key in corpus:
                if not corpus[key].get("abstract") and r.get("abstract"):
                    corpus[key]["abstract"] = r["abstract"]
            else:
                corpus[key] = r
            provenance.setdefault(key, []).append(cluster)

    for k, cl in provenance.items():
        corpus[k]["clusters"] = sorted(set(cl))
    records = list(corpus.values())

    # ---- live gold recall ------------------------------------------------------------------
    gold, _, _ = cv.load()
    got_titles = {cv.norm(r["title"])[:70] for r in records if r.get("title")}
    got_dois = {r["doi"] for r in records if r.get("doi")}
    tier_b = {r["title_key"]: r for r in
              json.load(open(os.path.join(LOGS, f"{SLUG}-tier-b-frame.json"))) if r.get("title_key")}
    hit = {"A_ONLY": [0, 0], "B_ONLY": [0, 0], "BOTH": [0, 0]}
    misses = []
    for g in gold:
        t = cv.norm(g["title"])[:70]
        doi = (tier_b.get(cv.norm(g["title"])[:120]) or {}).get("doi")
        found = t in got_titles or (doi and doi in got_dois)
        hit[g["tier"]][1] += 1
        hit[g["tier"]][0] += bool(found)
        if not found and len(misses) < 30:
            misses.append(g["title"][:110])
    recall_live = {k: (round(100 * v[0] / v[1], 1) if v[1] else None) for k, v in hit.items()}
    n_live = {k: v[1] for k, v in hit.items()}

    out = {"slug": SLUG, "stage": "C1", "operationalisation": "OpenAlex title.search, title-only",
           "filters": filters, "per_cluster": per_cluster,
           "union_records": len(records), "incomplete_clusters": incomplete,
           "budget_exhausted": budget_hit,
           "live_gold_recall_pct": recall_live, "live_gold_n": n_live,
           "records": records}
    json.dump(out, open(OUT_JSON, "w"), indent=1)

    sum_counts = sum(v["universe_count"] or 0 for v in per_cluster.values())
    L = [f"# D.1.a — live production pull (GACS C1)", "",
         "OpenAlex `title.search`, **title-only**, one cursor-paginated stream per cluster, union "
         "across clusters. Title-only because that is the operationalisation A6b's cross-validation "
         "selected; abstracts enter at the screen, not the search.", "",
         f"- union corpus: **{len(records):,}** distinct records",
         f"- sum of per-cluster counts: {sum_counts:,} (upper bound — clusters overlap by design)",
         f"- overlap collapsed by dedup: **{sum_counts - len(records):,}**",
         f"- incomplete clusters: **{incomplete or 'none'}**",
         f"- budget exhaustion: **{budget_hit or 'none'}**", "",
         "| cluster | universe | pulled | pages | complete |", "|---|---|---|---|---|"]
    for c, v in per_cluster.items():
        L.append(f"| `{c}` | {v['universe_count']:,} | {v['pulled']:,} | {v['pages']} | "
                 f"{'yes' if v['complete'] else '**NO**'} |")
    guard = ([] if not incomplete else [
        "", "> ## ⚠ THE PULL IS INCOMPLETE — THE RECALL FIGURES BELOW ARE NOT RESULTS", "",
        f"> `{', '.join(incomplete)}` stopped on OpenAlex budget exhaustion, and the budget resets "
        f"in roughly 23 hours (`retryAfter` 82,182s). **`GENERIC_VALUES` is the cluster A6b found "
        f"carries the most sole credit — 176 gold papers no other cluster reaches — so a partial "
        f"pull of it depresses gold recall far more than its share of records suggests.** Re-run to "
        f"resume; cached pages cost nothing. Do not quote these percentages until every cluster "
        f"reads `complete: yes`.", ""])
    L += guard
    L += ["", "## Live gold recall — does the real universe recover the frozen gold?", "",
          "A6b measured recall by matching compiled terms against stored titles. This measures "
          "whether OpenAlex's stemmed index, its coverage and its title normalisation reproduce that "
          "in practice. **A gap is a finding about the index, not about the query.**", "",
          "| gold channel | n | live recall | A6b CV recall |", "|---|---|---|---|",
          f"| A-only | {n_live['A_ONLY']} | {recall_live['A_ONLY']}% | 89.5% (partly fitted) |",
          f"| **B-only** | {n_live['B_ONLY']} | **{recall_live['B_ONLY']}%** | **92.1%** |",
          f"| both channels | {n_live['BOTH']} | {recall_live['BOTH']}% | 100% |", ""]
    if misses:
        L += ["### Gold the live pull did not return", ""] + [f"- {t}" for t in misses] + [""]
    open(OUT_MD, "w").write("\n".join(L) + "\n")
    print(f"\nunion {len(records)} records | live recall {recall_live}", file=sys.stderr)
    print(f"wrote {OUT_JSON}\nwrote {OUT_MD}", file=sys.stderr)
    if incomplete:
        print("INCOMPLETE — re-run to resume; cached pages cost nothing.", file=sys.stderr)


if __name__ == "__main__":
    main()
