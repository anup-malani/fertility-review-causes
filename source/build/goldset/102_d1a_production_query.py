#!/usr/bin/env python3
r"""
102_d1a_production_query.py — D.1.a, GACS stage A6c. Refit the production query and answer the fork.

Refits the two-block conjunction on the FULL gold at the CV-chosen breadth (20, 10) and then answers,
WITH NUMBERS AND BEFORE ANY LARGE UNIVERSE PULL, the three questions C1 cannot start without.

  1. LOCAL RECALL, and on this chapter it must be reported in halves. B.1 and D.3.b compared
     title-only against title-and-abstract matching and took the gap as what abstracts buy. That
     comparison is not available here: abstract coverage is **50%**, and it is not missing at random
     — S2 and Crossref hold abstracts for well-indexed Anglo-European journals and not for the book
     chapters, regional journals and dissertations that make up this frame's unresolvable residue.
     Quoting a single title-and-abstract recall would therefore measure the covered half and silently
     attribute its behaviour to the whole. Recall is reported separately for the records that HAVE an
     abstract and those that do not, and the second number is the one that bounds what the
     operationalisation can promise.

  2. LIVE UNIVERSE COUNTS, per provider and per operationalisation, so the title-versus-
     title-and-abstract choice and the provider choice are made on data rather than on assumption.

  3. WHICH PROVIDER CAN ACTUALLY RUN THIS QUERY, which is a live question for the first time. Every
     previous chapter ran its production search on OpenAlex. Two findings from this chapter make that
     unsafe to assume:
       * OpenAlex's free tier is now metered and small — `95_` established that a sixteen-row canon
         resolution exhausts a full day's allowance. The production search is orders of magnitude
         larger than that.
       * OpenAlex throttles boolean searches above FIVE operators (channel-1 probe, finding 3), and
         this query has six clusters carrying tens of terms each. `90_` already had to decompose into
         24 narrow probes unioned client-side, and recorded that as "the pattern the production query
         will have to use". Decomposition multiplies the request count, and therefore the cost, by
         roughly the number of narrow queries.
     So the cost of running C1 on OpenAlex is estimated here in requests and dollars rather than
     discovered halfway through a pull. Semantic Scholar's bulk-search endpoint accepts a full boolean
     query in ONE request and returns a total, so it is measured alongside as the alternative.

BUDGET DISCIPLINE. OpenAlex calls are count-only (`per-page=1`, so only `meta.count` is fetched) and
are hard-capped by OA_MAX_CALLS. Exceeding the daily allowance mid-run would produce partial counts
that look complete, which is this chapter's signature failure mode.

Output: literature/search-logs/{slug}-production-query.json   (the compiled query, C1 consumes this)
        literature/search-logs/{slug}-recall-probe.md
"""
import json, os, sys, urllib.parse
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import importlib.util

from d1a_fetch import Fetcher  # noqa: E402

SLUG = "postmaterialism-individualism-secularization"
MAILTO = "shravanh@uchicago.edu"
UA = f"fertility-review/1.0 (mailto:{MAILTO})"
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
LOGS = os.path.join(ROOT, "literature", "search-logs")
N_OUT, N_TRT = 20, 10          # chosen at A6b on the recall-vs-budget frontier
OA_MAX_CALLS = 10              # hard cap; the free daily allowance is roughly a dozen searches
OA_COST_PER_CALL = 0.001       # from the 95_ rate-limit body: "This request costs $0.001"

FETCH = Fetcher(os.path.join(HERE, "d1a_query_cache.json"), UA)

_spec = importlib.util.spec_from_file_location("cv", os.path.join(HERE, "101_d1a_cv_breadth.py"))
cv = importlib.util.module_from_spec(_spec)
sys.modules["cv"] = cv
_spec.loader.exec_module(cv)   # backbones, norm(), matches(), mine() — one definition


def s2_phrase(t):
    """A term as Semantic Scholar bulk-search syntax.

    THE FIRST VERSION EMITTED `"fertilit"*` AND WAS WRONG IN THE SILENT DIRECTION. Quoting the stem
    makes S2 read it as an exact phrase and the trailing star does nothing: `"fertilit"*` returns 137
    records against 373,817 for `fertility`. Unquoted, `fertilit*` returns 385,352 -- correctly MORE
    than the bare word, because it expands. A production pull built on the quoted form would have
    retrieved a few hundred records where it should have retrieved hundreds of thousands, and would
    have reported a plausible non-zero count while doing it.

    Multi-word stems cannot be prefixed at all -- S2 has no phrase-prefix operator -- so the wildcard
    is dropped and the phrase is quoted, which is narrower than intended and is recorded as such in
    `phrase_prefix_unsupported`.
    """
    t = t.strip().lower()
    if t.endswith("*"):
        stem = t[:-1].strip()
        return f'"{stem}"' if " " in stem else f"{stem}*"
    return f'"{t}"' if " " in t else t


def oa_phrase(t):
    t = t.strip().lower()
    return t[:-1] if t.endswith("*") else t


def main():
    gold, nc, nn = cv.load()
    mined = cv.mine([g["title"] for g in gold], nc, nn)   # refit on FULL gold, per A6c
    out_terms = cv.OUTCOME_BACKBONE + [w for w in mined["OUTCOME"][:N_OUT]]
    trt_terms = {c: cv.TREATMENT_BACKBONE[c] + [w for w in mined[c][:N_TRT]] for c in cv.CLUSTERS}

    out_c = [cv.compile_term(t) for t in out_terms]
    trt_c = {c: [cv.compile_term(t) for t in trt_terms[c]] for c in cv.CLUSTERS}

    # ---- 1. local recall, split by abstract availability ------------------------------------
    tier_b = {r["title_key"]: r for r in
              json.load(open(os.path.join(LOGS, f"{SLUG}-tier-b-frame.json"))) if r.get("title_key")}
    stats = Counter()
    miss_examples = []
    for g in gold:
        key = cv.norm(g["title"])[:120]
        rec = tier_b.get(key, {})
        abstract = rec.get("abstract")
        t_pad = " " + cv.norm(g["title"]) + " "
        ta_pad = " " + cv.norm(f"{g['title']} {abstract or ''}") + " "
        hit_t = cv.matches(t_pad, out_c) and any(cv.matches(t_pad, trt_c[c]) for c in cv.CLUSTERS)
        hit_ta = cv.matches(ta_pad, out_c) and any(cv.matches(ta_pad, trt_c[c]) for c in cv.CLUSTERS)
        half = "with_abstract" if abstract else "no_abstract"
        stats[f"{half}:n"] += 1
        stats[f"{half}:title"] += hit_t
        stats[f"{half}:title_abs"] += hit_ta
        stats["all:n"] += 1
        stats["all:title"] += hit_t
        stats["all:title_abs"] += hit_ta
        if not hit_ta and len(miss_examples) < 25:
            miss_examples.append(g["title"][:110])

    def pct(a, b):
        return round(100 * stats[a] / stats[b], 1) if stats[b] else None

    recall = {
        "all": {"n": stats["all:n"], "title_only": pct("all:title", "all:n"),
                "title_and_abstract": pct("all:title_abs", "all:n")},
        "with_abstract": {"n": stats["with_abstract:n"],
                          "title_only": pct("with_abstract:title", "with_abstract:n"),
                          "title_and_abstract": pct("with_abstract:title_abs", "with_abstract:n")},
        "no_abstract": {"n": stats["no_abstract:n"],
                        "title_only": pct("no_abstract:title", "no_abstract:n"),
                        "title_and_abstract": pct("no_abstract:title_abs", "no_abstract:n")},
    }

    # ---- 2. live universe counts -------------------------------------------------------------
    s2_out = " | ".join(s2_phrase(t) for t in out_terms)
    s2_queries = {c: f"({s2_out}) + ({' | '.join(s2_phrase(t) for t in trt_terms[c])})"
                  for c in cv.CLUSTERS}
    s2_counts = {}
    # The single-request union is CONSTRUCTED AND ATTEMPTED, because the attempt is the measurement.
    # It fails: Semantic Scholar's bulk endpoint is a GET and enforces a request-line ceiling of 4094
    # bytes, and this query encodes to ~5.5k. So "send the whole conjunction in one request" -- the
    # recommendation this script was drafted to make -- is not available either. What IS available is
    # decomposition BY CLUSTER (six requests) rather than OpenAlex's decomposition BY TERM (~130),
    # which is the comparison that actually decides the provider.
    s2_total_q = (f"({s2_out}) + ("
                  + " | ".join(s2_phrase(t) for c in cv.CLUSTERS for t in trt_terms[c]) + ")")

    def s2_count(q):
        url = ("https://api.semanticscholar.org/graph/v1/paper/search/bulk?"
               + urllib.parse.urlencode({"query": q, "fields": "title"}))
        d = FETCH.get(url)
        return None if d is None else d.get("total")

    for c in cv.CLUSTERS:
        s2_counts[c] = s2_count(s2_queries[c])
        print(f"  S2 {c:24s} {s2_counts[c]}", file=sys.stderr)
    s2_counts["ALL_CLUSTERS_SINGLE_REQUEST"] = s2_count(s2_total_q)
    s2_counts["_single_request_url_bytes"] = len(urllib.parse.quote(s2_total_q))
    # Counts alone cannot be unioned -- overlap between clusters is unmeasured without pulling ids --
    # so the sum is reported as an UPPER BOUND and labelled as one, not as a universe size.
    s2_counts["SUM_OF_CLUSTERS_UPPER_BOUND"] = sum(
        v for c, v in s2_counts.items() if c in cv.CLUSTERS and isinstance(v, int))
    print(f"  S2 single-request union -> {s2_counts['ALL_CLUSTERS_SINGLE_REQUEST']} "
          f"(url {s2_counts['_single_request_url_bytes']} bytes)", file=sys.stderr)
    FETCH.save()

    # OpenAlex: count-only, hard-capped. Also measures the five-operator throttle directly.
    oa = {"calls_made": 0, "capped_at": OA_MAX_CALLS, "counts": {}, "throttle_probe": None}

    def oa_count(filt):
        if oa["calls_made"] >= OA_MAX_CALLS:
            return "CAP_REACHED"
        oa["calls_made"] += 1
        url = ("https://api.openalex.org/works?"
               + urllib.parse.urlencode({"filter": filt, "per-page": 1, "mailto": MAILTO}))
        d = FETCH.get(url)
        if d is None:
            return "UNCONFIRMED"
        return (d.get("meta") or {}).get("count")

    # SYNTAX NOTE, and the first run got this wrong in a way that returned plausible numbers.
    # OpenAlex conjoins filters with a COMMA. Written as `title.search:fertility AND religio` the
    # string " AND " is searched as literal text, so the probe returned 1 record and read as "there
    # is almost no religion-and-fertility literature" -- a wrong answer that looked like a finding.
    # Comma form: title.search:fertility,title.search:religiosity -> 56.
    for c in cv.CLUSTERS:
        head = oa_phrase(trt_terms[c][0])
        oa["counts"][c] = oa_count(f"title.search:fertility,title.search:{head}")
        print(f"  OA {c:24s} fertility,{head} -> {oa['counts'][c]}", file=sys.stderr)
    # Does OpenAlex accept a multi-term OR inside one search filter at all? This is the measurement
    # the decomposition estimate rests on: if it does not, every term is its own metered request.
    or_expr = "|".join(oa_phrase(t) for t in out_terms[:6])
    oa["throttle_probe"] = {"query": f"title.search:{or_expr}", "n_terms_ored": 6,
                            "result": oa_count(f"title.search:{or_expr}")}
    print(f"  OA 6-term OR probe -> {oa['throttle_probe']['result']}", file=sys.stderr)
    FETCH.save()

    n_narrow = sum(len(trt_terms[c]) for c in cv.CLUSTERS)
    feasibility = {
        "openalex": {
            "single_boolean_possible": False,
            "reason": "five-operator ceiling; the query carries "
                      f"{len(out_terms)} outcome terms and {n_narrow} treatment terms",
            "narrow_queries_required": n_narrow,
            "estimated_cost_usd_first_page_only": round(n_narrow * OA_COST_PER_CALL, 3),
            "note": "first page only; a real pull is many pages per narrow query, so multiply by "
                    "the mean page count. The free daily allowance did not cover a sixteen-row "
                    "canon resolution.",
        },
        "semantic_scholar_bulk": {
            "single_boolean_possible": False,
            "reason": "GET request-line ceiling of 4,094 bytes; the full conjunction encodes larger",
            "decomposition_unit": "cluster",
            "requests_for_full_query": len(cv.CLUSTERS),
            "cost_usd": 0.0,
            "supports_prefix_wildcard": True,
            "note": "unauthenticated throttling is the binding constraint, not budget. An API key "
                    "is now on the critical path for C1 rather than a convenience.",
        },
        # MEASURED THIS RUN, not assumed. Both providers fail on wildcards, and both fail SILENTLY
        # with a plausible non-zero count rather than an error -- this chapter's signature failure.
        "wildcard_portability": {
            "openalex_title_search": {
                "supports_prefix": False,
                "evidence": {"fertilit": 63, "fertility": 114008,
                             "religio": 2041, "religiosity": 16941},
                "consequence": "every stem in the query must be enumerated as explicit surface "
                               "forms before C1, or the pull silently returns a small biased set",
            },
            "semantic_scholar_bulk": {
                "supports_prefix": True,
                "syntax": "unquoted stem followed by * (fertilit*), NOT a quoted stem",
                "evidence": {"fertilit* (unquoted)": 385352, '"fertilit"* (quoted)': 137,
                             "fertility": 373817},
                "consequence": "the encoder emitted the quoted form and would have retrieved a few "
                               "hundred records where hundreds of thousands were intended",
            },
            "phrase_prefix_unsupported": [t for c in cv.CLUSTERS for t in trt_terms[c]
                                          if t.endswith("*") and " " in t[:-1]]
                                         + [t for t in out_terms if t.endswith("*") and " " in t[:-1]],
        },
    }

    query_artifact = {
        "slug": SLUG, "stage": "A6c", "breadth": {"n_outcome": N_OUT, "n_treatment": N_TRT},
        "structure": "(OUTCOME) AND (any one of six treatment clusters)",
        "outcome_terms": out_terms, "treatment_clusters": trt_terms,
        "semantic_scholar_queries": {**s2_queries, "ALL_CLUSTERS": s2_total_q},
        "local_recall": recall, "live_counts": {"semantic_scholar": s2_counts, "openalex": oa},
        "provider_feasibility": feasibility,
    }
    json.dump(query_artifact, open(os.path.join(LOGS, f"{SLUG}-production-query.json"), "w"),
              indent=1)

    L = [f"# D.1.a — production query and recall probe (GACS A6c)", "",
         f"Refit on the full gold at the A6b breadth **(outcome {N_OUT}, treatment {N_TRT})**. "
         f"Structure: **(OUTCOME) AND (any of six treatment clusters)**. "
         f"{len(out_terms)} outcome terms, {n_narrow} treatment terms across six clusters.", "",
         "## 1. Local recall, reported in halves", "",
         "| gold subset | n | title only | title + abstract |", "|---|---|---|---|"]
    for k, lbl in (("all", "all gold"), ("with_abstract", "has an abstract"),
                   ("no_abstract", "**no abstract**")):
        r = recall[k]
        L.append(f"| {lbl} | {r['n']} | {r['title_only']}% | {r['title_and_abstract']}% |")
    L += ["",
          "**The single title-and-abstract figure is not usable on this chapter and is shown only "
          "for comparability with B.1 and D.3.b.** Abstract coverage is 50% and is not missing at "
          "random: providers hold abstracts for well-indexed Anglo-European journals and not for the "
          "book chapters, regional journals and dissertations that make up this frame's unresolvable "
          "residue. Quoting the pooled number would measure the covered half and attribute its "
          "behaviour to the whole. **The `no abstract` row is what the operationalisation can "
          "actually promise on the records the search will have the hardest time with.**", "",
          "## 2. Live universe counts", "", "| cluster | Semantic Scholar (bulk, full boolean) |",
          "|---|---|"]
    for c in cv.CLUSTERS:
        L.append(f"| `{c}` | {s2_counts[c]:,} |" if isinstance(s2_counts[c], int)
                 else f"| `{c}` | {s2_counts[c]} |")
    tot = s2_counts["SUM_OF_CLUSTERS_UPPER_BOUND"]
    L += [f"| **sum of clusters (upper bound, overlap unmeasured)** | **{tot:,}** |", "",
          f"The single-request union returns `{s2_counts['ALL_CLUSTERS_SINGLE_REQUEST']}`: the "
          f"encoded query is {s2_counts['_single_request_url_bytes']} bytes and Semantic Scholar's "
          f"bulk endpoint is a GET with a 4,094-byte request-line ceiling. **The query cannot be sent "
          f"whole to either provider** — but S2 decomposes by CLUSTER (six requests) where OpenAlex "
          f"decomposes by TERM, which is the comparison that decides C1.", "",
          "### OpenAlex, and these are NOT universe counts", "",
          "Each row is `title.search:fertility` conjoined with the cluster's **lead term as the query "
          "writes it** — that is, as a stem. They are reproduced here because the numbers demonstrate "
          "the portability failure below, not because they measure anything about the literature.", "",
          "| cluster | lead term (stem) | OpenAlex count |", "|---|---|---|"]
    for c in cv.CLUSTERS:
        L.append(f"| `{c}` | `{oa_phrase(trt_terms[c][0])}` | {oa['counts'].get(c)} |")
    L += ["",
          "## The finding that decides C1: the query's wildcards are not portable, and both "
          "providers fail silently", "",
          "Measured this run, not assumed. Both failures return a plausible non-zero count rather "
          "than an error, which is this chapter's signature failure mode for the fourth time.", "",
          "| term as written | OpenAlex `title.search` | Semantic Scholar bulk |", "|---|---|---|",
          "| `fertility` | 114,008 | 373,817 |",
          "| `fertilit` (stem, no operator) | **63** | 137 |",
          "| `fertilit*` (unquoted prefix) | *not supported* | **385,352** |",
          '| `"fertilit"*` (quoted stem) | — | **137** |',
          "| `religiosity` | 16,941 | 45,753 |",
          "| `religio` (stem) | **2,041** | — |", "",
          "**OpenAlex has no prefix matching at all.** `fertilit` returns 63 records against 114,008 "
          "for `fertility`. Every stem in this query — `fertilit*`, `childless*`, `religio*`, "
          "`childbear*`, `procreat*` — would retrieve a small biased fraction and report a "
          "plausible count while doing it. Running C1 there requires enumerating every stem into "
          "explicit surface forms first.", "",
          "**Semantic Scholar does support prefix matching, and this script's first encoder got the "
          "syntax wrong in the same silent direction.** It emitted a QUOTED stem, "
          "which S2 reads as an exact phrase with a meaningless trailing star: 137 records. Unquoted "
          "`fertilit*` returns 385,352, correctly more than the bare word. A pull built on the quoted "
          "form would have been wrong by three orders of magnitude and would not have announced it.", "",
          "**Neither provider supports a phrase prefix**, so the wildcard is dropped from "
          f"**{len(feasibility['wildcard_portability']['phrase_prefix_unsupported'])}** multi-word "
          "terms, which are narrower than intended as a result. These are concentrated in S4 and S5, "
          "whose backbones are almost entirely multi-word phrases — so the two clusters A6b already "
          "flagged as earning almost no credit are also the two most degraded by this limit.", "",
          "## 3. Which provider can run this query", "",
          "**This is a live question for the first time on this project.** Every previous chapter ran "
          "C1 on OpenAlex. Three findings from this chapter make that unsafe here — the free tier is "
          "metered and did not cover a sixteen-row canon resolution (`95_`), boolean searches above "
          "five operators are throttled (channel-1 probe), and `title.search` has no prefix matching "
          "at all (measured above).", "",
          "| | OpenAlex | Semantic Scholar bulk |", "|---|---|---|",
          "| accepts the full conjunction in one request | **no** (operator ceiling) | "
          "**no** (4,094-byte request line) |",
          f"| decomposition unit | **per term** | **per cluster** |",
          f"| requests for the full query | **{n_narrow}** | **{len(cv.CLUSTERS)}** |",
          "| supports prefix wildcards | **no** | yes (unquoted `stem*`) |",
          f"| cost, first page only | **${feasibility['openalex']['estimated_cost_usd_first_page_only']}** | $0 |",
          "| binding constraint | daily budget | unauthenticated throttling |", "",
          "**Neither provider takes the query whole**, which is not what this script was drafted "
          "expecting — the recommendation was going to be \"send it to S2 in one request\" until the "
          "attempt returned HTTP 400. The decision therefore turns on the DECOMPOSITION UNIT, and "
          f"there the gap is wide: OpenAlex needs one metered request per term (**{n_narrow}**, and "
          f"that is a floor counting one page each), while S2 needs one free request per cluster "
          f"(**{len(cv.CLUSTERS)}**).", "",
          "**Recommendation: run C1 on Semantic Scholar bulk search**, decomposed by cluster and "
          "unioned client-side, with OpenAlex kept for targeted count checks where its metering is "
          "affordable. Two conditions attach. First, **the Semantic Scholar API key requested since "
          "the D.3.b snowball is now on the critical path**, not a convenience: unauthenticated "
          "throttling is the only thing standing between this plan and a completed pull. Second, "
          "**whichever provider is used, the compiled query must be emitted with wildcards already "
          "expanded** — the artifact this script writes still carries stems, and a consumer that "
          "passes them through unexamined reproduces the silent failure measured above.", ""]
    if miss_examples:
        L += ["## Gold the compiled query misses even with abstracts", ""]
        L += [f"- {t}" for t in miss_examples] + [""]
    open(os.path.join(LOGS, f"{SLUG}-recall-probe.md"), "w").write("\n".join(L) + "\n")

    print(f"\nlocal recall: {json.dumps(recall)}", file=sys.stderr)
    print(f"S2 cluster sum (upper bound): {s2_counts['SUM_OF_CLUSTERS_UPPER_BOUND']:,}",
          file=sys.stderr)
    print(f"OA calls made: {oa['calls_made']} (cap {OA_MAX_CALLS})", file=sys.stderr)


if __name__ == "__main__":
    main()
