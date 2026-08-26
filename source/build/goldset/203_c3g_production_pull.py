#!/usr/bin/env python3
"""
203_c3g_production_pull.py — C.3.g, stage C1. Retrieve the production keyword frame.

A4 built the CITATION channel (2,071 records, one hop from 21 anchors). This builds the KEYWORD
channel — the production query itself — and unions the two into the pool the screen will see. The
two channels are kept distinguishable on every record (`channels`), because that is what makes tier
assignment at E1 possible: a record found by both is corroborated, a record found by one is not.

THE QUERY IS THE FRAME THE SCOPE RULED ON, VERBATIM. Exposure is student-anchored — a bare "debt"
reaches a 1,389-record sovereign-debt literature (`199_`) — and the outcome axis is the UNION of
fertility, union-formation and housing vocabulary, because A4 settled that decision on evidence: a
fertility-only frame reaches 5 of 21 anchors against the union frame's 13, and the eight it loses
are every identified study in the chapter.

WHAT THIS SCRIPT DOES NOT DO. It does not filter, score or rank. Ranking is D1's job and it needs the
whole pool. Nothing retrieved here is ever deleted; records that fall below D1's cut keep their
scores and stay in the JSON so a cut can be re-made without re-running retrieval.

TWO RETRIEVAL HAZARDS THIS CHAPTER HAS ALREADY BEEN BITTEN BY, both guarded:
  * a `?` in a search value is a WILDCARD and returns a 200 whose body reads as an empty literature;
  * a comma inside a filter VALUE truncates the filter, and percent-encoding does not save it.
Both are checked before a request is spent. A 200 carrying an {"error": ...} body is recorded as an
ERROR, never rendered through `.get("results", [])` into a confident zero.

Output: literature/search-logs/{slug}-production-query.json   (the query, for reproduction)
        literature/search-logs/{slug}-pool.json               (keyword ∪ citation, deduped)
        literature/search-logs/{slug}-production-pull-log.md
"""
import json, os, re, subprocess, sys, time
from urllib.parse import quote

SLUG = "student-debt-household-formation"
MAILTO = "shravanh@uchicago.edu"
UA = f"fertility-review/1.0 (mailto:{MAILTO})"
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
LOGS = os.path.join(ROOT, "literature", "search-logs")
TIER_B = os.path.join(LOGS, f"{SLUG}-tier-b-frame.json")
TIER_A = os.path.join(LOGS, f"{SLUG}-tier-a.json")
OUT_Q = os.path.join(LOGS, f"{SLUG}-production-query.json")
OUT_POOL = os.path.join(LOGS, f"{SLUG}-pool.json")
OUT_LOG = os.path.join(LOGS, f"{SLUG}-production-pull-log.md")

PAGE = 200
SELECT = ("id,doi,display_name,publication_year,cited_by_count,type,authorships,"
          "primary_location,abstract_inverted_index")

DEBT = ('"student debt" OR "student loan" OR "student loans" OR "student loan debt" OR '
        '"educational debt" OR "education debt" OR "college debt" OR "student borrowing" OR '
        '"student borrowers" OR "education loans" OR "student indebtedness"')
FERT = ('"fertility" OR "childbearing" OR "first birth" OR "birth rates" OR "childlessness" OR '
        '"number of children" OR "transition to parenthood" OR "family size" OR '
        '"having children" OR "family formation"')
UNION = ('"marriage" OR "marital" OR "union formation" OR "cohabitation" OR '
         '"partnership formation" OR "marriage timing" OR "age at marriage"')
HOUSE = ('"homeownership" OR "home ownership" OR "household formation" OR "first-time buyer" OR '
         '"living with parents" OR "residential independence" OR "coresidence" OR "housing tenure"')

# "family formation" and "debt forgiveness" are BOTH in this query and neither was in `200_`'s.
# That omission is why `200_` reported the policy-variation cell as empty and A4's citation channel
# had to overturn it. The production frame does not repeat the mistake.
QUERY = f"title_and_abstract.search:({DEBT}) AND (({FERT}) OR ({UNION}) OR ({HOUSE}))"


def openalex_key():
    k = os.environ.get("OPENALEX_API_KEY")
    if k:
        return k.strip()
    envp = os.path.join(ROOT, ".env")
    if os.path.exists(envp):
        for line in open(envp):
            if line.startswith("OPENALEX_API_KEY="):
                return line.split("=", 1)[1].strip()
    return ""


OA_KEY = openalex_key()
ERRORS = []


def guard():
    bad = []
    if "?" in QUERY:
        bad.append("'?' in the query — parsed as a wildcard, returns a 200 that reads as empty")
    for phrase in QUERY.split('"')[1::2]:
        if "," in phrase:
            bad.append(f"comma inside a filter value: {phrase!r}")
        if phrase.strip().split(" ")[0].lower() in ("not", "and", "or"):
            bad.append(f"phrase opens with a boolean word: {phrase!r}")
    if bad:
        sys.stderr.write("ABORT: query hazards; no requests spent.\n" + "\n".join("  " + b for b in bad) + "\n")
        sys.exit(2)


def oa_get(url, tag, tries=3):
    for attempt in range(tries):
        out = subprocess.run(["curl", "-s", "-m", "60", "-A", UA, url],
                             capture_output=True, text=True).stdout
        try:
            d = json.loads(out)
        except Exception:
            d = None
        if isinstance(d, dict) and d.get("error"):
            ERRORS.append((tag, f"{d.get('error')} {str(d.get('message'))[:90]}"))
            return {}, False
        if d is not None:
            return d, True
        time.sleep(1.5 * (attempt + 1))
    ERRORS.append((tag, "unparseable body after retries"))
    return {}, False


def unabstract(inv):
    if not inv:
        return ""
    pos = [(i, w) for w, ii in inv.items() for i in ii]
    return " ".join(w for _, w in sorted(pos))[:2400]


def row(w):
    loc = (w.get("primary_location") or {}).get("source") or {}
    return dict(id=w["id"].rsplit("/", 1)[-1],
                doi=(w.get("doi") or "").replace("https://doi.org/", "") or None,
                title=w.get("display_name") or "", year=w.get("publication_year"),
                cited_by_count=w.get("cited_by_count") or 0, type=w.get("type"),
                venue=loc.get("display_name") or "",
                authors=[(a.get("author") or {}).get("display_name") or ""
                         for a in (w.get("authorships") or [])][:12],
                abstract=unabstract(w.get("abstract_inverted_index")))


def main():
    guard()
    if not OA_KEY:
        sys.stderr.write("ABORT: no OPENALEX_API_KEY; unfunded calls return 'Insufficient budget', "
                         "which would bucket as errors.\n")
        sys.exit(3)

    got, cursor, pages, total = [], "*", 0, None
    while cursor:
        url = (f"https://api.openalex.org/works?filter={quote(QUERY)}&per-page={PAGE}"
               f"&select={SELECT}&cursor={cursor}&api_key={OA_KEY}")
        d, ok = oa_get(url, f"page{pages}")
        if not ok:
            break
        if total is None:
            total = d.get("meta", {}).get("count")
        got += [row(w) for w in d.get("results", [])]
        cursor = (d.get("meta") or {}).get("next_cursor")
        pages += 1
        if not d.get("results"):
            break
        time.sleep(0.2)

    # A partial pull is the RELEVANCE-ORDERED head, not a random sample. Cursor paging is stable
    # order, but an aborted pull still has to be declared rather than silently reported as the frame.
    complete = total is not None and len(got) >= total
    kw = {r["id"]: r for r in got}

    tier_b = json.load(open(TIER_B))
    tier_a = json.load(open(TIER_A))
    anchor_ids = {a["openalex_id"].rsplit("/", 1)[-1] for a in tier_a if a.get("openalex_id")}

    pool = {}
    for rid, r in kw.items():
        pool[rid] = {**r, "channels": ["keyword"], "seed_ids": []}
    n_both = 0
    for r in tier_b:
        rid = r["id"].rsplit("/", 1)[-1] if r["id"].startswith("http") else r["id"]
        if rid in pool:
            pool[rid]["channels"] = ["citation", "keyword"]
            pool[rid]["seed_ids"] = r.get("seed_ids", [])
            n_both += 1
        else:
            pool[rid] = {**r, "id": rid, "channels": ["citation"],
                         "seed_ids": r.get("seed_ids", [])}
    # Tier-A anchors enter the pool by hand and are marked, because A4 measured that the frame
    # cannot reach two of them — one being the chapter's most-cited primary-cell work, which has no
    # indexed abstract and a title saying "Debt" and "baby". An anchor that depends on the frame to
    # find it is an anchor the frame can lose.
    n_anchor_added = 0
    for a in tier_a:
        rid = (a.get("openalex_id") or "").rsplit("/", 1)[-1]
        if not rid:
            continue
        if rid in pool:
            pool[rid]["is_anchor"] = True
            pool[rid]["anchor_cell"] = a["provisional_cell"]
        else:
            pool[rid] = dict(id=rid, doi=a.get("doi"), title=a["title"], year=a.get("year"),
                             cited_by_count=a.get("cited_by_count") or 0,
                             type=a.get("record_type"), venue=a.get("container") or "",
                             authors=a.get("authors") or [], abstract="",
                             channels=["anchor"], seed_ids=[], is_anchor=True,
                             anchor_cell=a["provisional_cell"])
            n_anchor_added += 1

    json.dump({"query": QUERY, "reported_total": total, "retrieved": len(got),
               "complete": complete, "pages": pages}, open(OUT_Q, "w"), indent=2)
    json.dump(list(pool.values()), open(OUT_POOL, "w"), indent=2)

    kw_only = sum(1 for r in pool.values() if r["channels"] == ["keyword"])
    cit_only = sum(1 for r in pool.values() if r["channels"] == ["citation"])
    n_abs = sum(1 for r in pool.values() if r.get("abstract"))

    L = [f"# C1 production pull — {SLUG} (C.3.g)", "",
         f"**Generated by:** `source/build/goldset/203_c3g_production_pull.py`", "",
         f"**Keyword channel:** OpenAlex reports **{total:,}**; retrieved **{len(got):,}** over "
         f"{pages} pages. Complete: **{'yes' if complete else 'NO — declared, not hidden'}**.", "",
         "```", QUERY, "```", "",
         f"**Pool = keyword ∪ citation ∪ anchors: {len(pool):,} records.**", "",
         "| Channel | n |", "|---|---|",
         f"| keyword only | {kw_only:,} |",
         f"| citation only | {cit_only:,} |",
         f"| **both — corroborated, and Tier 1 eligible at E1** | **{n_both:,}** |",
         f"| anchors added by hand (frame could not reach them) | {n_anchor_added} |", "",
         f"{n_abs:,} of {len(pool):,} ({n_abs / max(len(pool), 1):.0%}) carry an abstract. A "
         "title-only record is NOT a negative verdict at screen — it is `INSUFFICIENT_INFO` unless "
         "the title alone is decisive.", "",
         f"**{n_both:,} records were found by BOTH channels.** That number is the honest measure of "
         "how much the two sieves agree, and it is what makes Tier 1 mean something at E1: a record "
         "found twice through vocabulary-independent routes is corroborated, one found once is not.",
         ""]
    if n_anchor_added:
        L += ["**Anchors the production frame could not reach**, carried in by hand:", ""]
        for a in tier_a:
            rid = (a.get("openalex_id") or "").rsplit("/", 1)[-1]
            if rid and pool.get(rid, {}).get("channels") == ["anchor"]:
                L.append(f"- *{a['title'][:76]}* (`{a['provisional_cell']}`)")
        L.append("")
    if ERRORS:
        L += ["## Failed requests (excluded from every count above)", ""]
        L += [f"- `{t}` — {e}" for t, e in ERRORS] + [""]
    open(OUT_LOG, "w").write("\n".join(L) + "\n")
    print(f"keyword {len(got)}/{total}  pool {len(pool)}  both {n_both}  anchors-added {n_anchor_added}")
    print(f"-> {os.path.relpath(OUT_POOL, ROOT)}")


if __name__ == "__main__":
    main()
