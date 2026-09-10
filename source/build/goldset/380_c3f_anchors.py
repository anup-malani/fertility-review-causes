#!/usr/bin/env python3
"""
380 — C.3.f (TICK-086) stage 3: build and resolve the anchor set.

Anchors are the records the production query must retrieve. They are named BEFORE the query exists,
so that recall is measured against a set chosen on substance rather than assembled from whatever the
query happened to return.

Three sources, and the difference between them matters:

  INHERITED  the 14 usable records D.1.b routed here (10 canon + 4 primary, `377`). They already
             carry OpenAlex ids from another chapter's screen, so they are CONFIRMED by id in one
             batched request rather than resolved by title.
  HAND       21 works named from the literature by first author, year and title. These are the risky
             ones: a title recalled slightly wrong resolves to a plausible neighbour rather than to
             nothing, so every one is printed with its matched authors and year for reading. Nothing
             here is accepted on a similarity score alone.
  DECOY      one per boundary wall. A decoy that the production query retrieves is not a failure —
             `decoy-clouds-are-boundary-cases` — it is a boundary case to route. They are marked so
             that recall on anchors and leakage on decoys are never averaged.

Resolver hazards this honours, all of them recorded from earlier chapters:

  `never-hand-type-a-record-id`     — no OpenAlex id is typed here. Ids come from `377`'s JSON or
                                      from a resolved search; 8 of 8 reconstructed ids were wrong.
  `book-canon-first-author`         — four of the hand anchors are monographs, and a monograph
                                      resolves to its own REVIEWS at Jaccard 1.00. The gate is the
                                      first author, and a review can list the reviewed author as a
                                      co-author, so the check is on author POSITION.
  `shadow-record-gate`              — "Review of X", "Comment on X", editorial notices and Faculty
                                      Opinions records beat the real work on title similarity.
  `title-search-apostrophe-wrong-match` / wildcards — both handled by `textnorm.oa_search_safe`.
  `resolver-type-vocabulary-mismatch` — the type vocabulary differs between sources; type is
                                      reported, never gated on.
  `refusals-read-as-zeros`          — the shared client raises on a refusal; a NOT_FOUND here is
                                      only ever written after a successful response.

Uses `source/lib/openalex.py`, the shared client, rather than a thirteenth copy of the resolver.
Its on-disk cache means a re-run costs nothing.

Outputs literature/search-logs/c3f-anchors-<date>.{json,md}.
"""
import json, sys, datetime, pathlib, re

sys.path.insert(0, str(pathlib.Path("source/lib").resolve()))
import textnorm                                                    # noqa: E402
from openalex import OpenAlex, POOL                                # noqa: E402

LOGS = pathlib.Path("literature/search-logs")
DATE = datetime.date.today().isoformat()
SELECT = "id,doi,display_name,publication_year,type,cited_by_count,authorships"

SHADOW = re.compile(r"\b(review of|reviews of|comment on|reply to|correction to|erratum|"
                    r"editorial comment|faculty opinions|book review)\b", re.I)

# (arm, first author surname, year, expected type, title). Nothing here is an id.
# TYPE is the SECOND defence for monographs and it is not redundant with the author
# gate: on D.2.d the review CREDITED the reviewed author, so an author gate alone has
# a live hole (`anchor-resolver-book-canon`).
HAND = [
    # --- the net-flow theory canon
    ("NET/theory", "Caldwell", 1976, "ARTICLE", "Toward a Restatement of Demographic Transition Theory"),
    ("NET/theory", "Caldwell", 1978, "ARTICLE", "A Theory of Fertility: From High Plateau to Destabilization"),
    ("NET/theory", "Caldwell", 1982, "BOOK", "Theory of Fertility Decline"),
    ("NET/theory", "Kaplan", 1994, "ARTICLE",
     "Evolutionary and Wealth Flows Theories of Fertility: Empirical Tests and New Models"),
    ("NET/theory", "Turke", 1989, "ARTICLE", "Evolution and the Demand for Children"),
    # --- flow measurement, the tradition that makes the exposure observable
    ("NET/measurement", "Lee", 2011, "BOOK",
     "Population Aging and the Generational Economy: A Global Perspective"),
    ("NET/measurement", "Lee", 2010, "ARTICLE",
     "Fertility Human Capital and Economic Growth over the Demographic Transition"),
    ("NET/measurement", "Stecklov", 1997, "ARTICLE",
     "Intergenerational Resource Flows in Cote d Ivoire: Empirical Analysis of Aggregate Flows"),
    ("UPWARD", "Mueller", 1976, "ARTICLE", "The Economic Value of Children in Peasant Agriculture"),
    ("DOWNWARD", "Zelizer", 1985, "BOOK",
     "Pricing the Priceless Child: The Changing Social Value of Children"),
    ("DOWNWARD", "Lindert", 1978, "BOOK", "Fertility and Scarcity in America"),
    # --- channel 2: identified designs the theory vocabulary cannot see
    ("CH2/identified", "Bau", 2021, "ARTICLE",
     "Can Policy Change Culture? Government Pension Plans and Traditional Kinship Practices"),
    ("CH2/identified", "Edmonds", 2005, "ARTICLE", "Child Labor in the Global Economy"),
    ("CH2/identified", "Edmonds", 2005, "ARTICLE",
     "The Effect of Trade Liberalization on Child Labor"),
]

DECOY = [
    ("C.3.c old-age security", "Nugent", 1985, "ARTICLE", "The Old-Age Security Motive for Fertility"),
    ("C.3.d quantity-quality", "Becker", 1973, "ARTICLE",
     "On the Interaction between the Quantity and Quality of Children"),
    ("D.1.b developmental idealism", "Thornton", 2001, "ARTICLE",
     "The Developmental Paradigm Reading History Sideways and Family Change"),
    ("C.3.a mode of production", "Boserup", 1965, "BOOK",
     "The Conditions of Agricultural Growth: The Economics of Agrarian Change under Population Pressure"),
    ("C.1.a income and wealth shocks", "Lovenheim", 2013, "ARTICLE",
     "Do Family Wealth Shocks Affect Fertility Choices? Evidence from the Housing Market"),
    ("A.19 transmission of fertility", "Murphy", 2002, "ARTICLE",
     "The Intergenerational Transmission of Fertility in Contemporary Denmark"),
    ("C.2.b direct costs", "Lino", 2017, "ARTICLE", "Expenditures on Children by Families"),
]


def cached_get(oa, params, errors, label):
    """oa.get, memoised on disk. The shared client caches count() and page_all() but not get(),
    and at ~100 requests a day a re-run that re-buys 21 searches is a fifth of the allowance
    (`stage-output-must-survive-rerun`)."""
    key = json.dumps(["get", params], sort_keys=True)
    if key in oa.cache:
        oa.stats["hit"] += 1
        return oa.cache[key], None
    oa.stats["miss"] += 1
    d, err = oa.get(params)
    if err:
        errors.append((label, err))
        return None, err
    slim = {"results": [{k: r.get(k) for k in
                         ("id", "doi", "display_name", "publication_year", "type",
                          "cited_by_count", "authorships")} for r in d.get("results", [])]}
    oa._remember(key, slim)
    return slim, None


def first_author(rec):
    for a in rec.get("authorships", []):
        if a.get("author_position") == "first":
            return (a.get("author") or {}).get("display_name", "")
    aus = rec.get("authorships") or []
    return ((aus[0].get("author") or {}).get("display_name", "")) if aus else ""


def author_list(rec):
    return [((a.get("author") or {}).get("display_name") or "") for a in rec.get("authorships", [])]


def jaccard(a, b):
    A, B = set(textnorm.norm(a).split()), set(textnorm.norm(b).split())
    return len(A & B) / len(A | B) if A | B else 0.0


BOOKLIKE = {"book", "monograph", "reference-entry"}


def resolve(oa, surname, year, want_type, title, errors):
    """Best match for a hand-named work, with a verdict. Never returns a silent miss."""
    q = textnorm.oa_search_safe(title)
    d, err = cached_get(oa, {"search": q, "per-page": "8", "select": SELECT}, errors, title)
    if err:
        return {"verdict": "REFUSED", "error": err}
    results = d.get("results", [])
    if not results:
        return {"verdict": "NOT_FOUND", "n_candidates": 0}

    scored = []
    for r in results:
        name = r.get("display_name") or ""
        fa = first_author(r)
        surname_norm = textnorm.norm(surname)
        scored.append({
            "id": r["id"].rsplit("/", 1)[-1], "doi": r.get("doi"), "title": name,
            "year": r.get("publication_year"), "type": r.get("type"),
            "cited_by": r.get("cited_by_count"), "first_author": fa,
            "authors": author_list(r),
            "jaccard": round(jaccard(title, name), 3),
            "shadow": bool(SHADOW.search(name)),
            # book-canon-first-author: the gate is the FIRST author, not membership in the list.
            "first_author_ok": surname_norm in textnorm.norm(fa),
            "author_anywhere": any(surname_norm in textnorm.norm(a) for a in author_list(r)),
            "year_delta": (abs(r["publication_year"] - year)
                           if r.get("publication_year") else None),
        })
    live = [c for c in scored if not c["shadow"]]
    best = max(live or scored, key=lambda c: (c["jaccard"], c["first_author_ok"]))

    booklike = (best.get("type") or "") in BOOKLIKE
    if best["shadow"]:
        v = "SHADOW_ONLY"
    elif not best["first_author_ok"]:
        # `author_anywhere` and not first: the review-credits-the-reviewed-author shape.
        v = "REVIEW_OF_THE_WORK" if best["author_anywhere"] else "WRONG_AUTHOR"
    elif want_type == "BOOK" and not booklike:
        # The second defence. The author gate passed, so this is the D.2.d hole: a review that
        # credits the reviewed author, or an excerpt. Never accepted on the author check alone.
        v = "BOOK_RESOLVED_TO_NONBOOK"
    elif best["jaccard"] < 0.4:
        v = "WEAK_TITLE_MATCH"
    elif best["year_delta"] is not None and best["year_delta"] > 2:
        # Right author, right title, different year: a reissue or a later edition, not a wrong
        # record. `version-of-record-gate` — this is a version to pin, not a miss to retry.
        v = "VERSION_DIFFERS"
    else:
        v = "OK"
    return {"verdict": v, "best": best, "n_candidates": len(results),
            "n_shadow": sum(c["shadow"] for c in scored),
            "shadow_regex_caught_it": bool(best["shadow"])}


def main():
    key = ""
    try:
        for line in open(".env"):
            if line.startswith("OPENALEX_API_KEY="):
                key = line.split("=", 1)[1].strip().strip('"')
    except FileNotFoundError:
        pass
    oa = OpenAlex(key=key, mailto="shravanh@uchicago.edu",
                  cache_path="temp/c3f-anchor-cache.json")
    errors = []

    # ---------------------------------------------------------------- inherited, confirmed by id
    seeds = json.load(open(LOGS / "c3f-inherited-seeds-2026-09-10.json"))
    routing = (LOGS / "c3f-inherited-seeds-routing.md").read_text()
    keep_ids = re.findall(r"\| (W\d+) \|", routing)
    if not keep_ids:                       # the routing table lists ids in prose, not a column
        keep_ids = [r["paperId"] for r in seeds["records"]]
    print(f"\n== inherited: confirming {len(keep_ids)} ids from 377 in one batched request ==")
    d, err = oa.get({"filter": "ids.openalex:" + "|".join(keep_ids),
                     "per-page": "200", "select": SELECT})
    inherited = []
    if err:
        errors.append(("inherited id batch", err))
        print(f"  REFUSED: {err}", file=sys.stderr)
    else:
        got = {r["id"].rsplit("/", 1)[-1]: r for r in d.get("results", [])}
        for pid in keep_ids:
            r = got.get(pid)
            inherited.append({"id": pid, "confirmed": bool(r),
                              "title": (r or {}).get("display_name"),
                              "year": (r or {}).get("publication_year"),
                              "type": (r or {}).get("type"),
                              "cited_by": (r or {}).get("cited_by_count"),
                              "first_author": first_author(r) if r else None})
        n_ok = sum(c["confirmed"] for c in inherited)
        print(f"  {n_ok}/{len(keep_ids)} confirmed against OpenAlex")
        for c in inherited:
            if not c["confirmed"]:
                print(f"  MISSING  {c['id']}", file=sys.stderr)

    # ---------------------------------------------------------------- hand + decoy, resolved
    out = []
    for kind, rows in (("ANCHOR", HAND), ("DECOY", DECOY)):
        print(f"\n== {kind}: resolving {len(rows)} hand-named works ==")
        for arm, surname, year, want_type, title in rows:
            r = resolve(oa, surname, year, want_type, title, errors)
            r.update({"kind": kind, "arm": arm, "expect_author": surname,
                      "expect_year": year, "expect_type": want_type,
                      "expect_title": title})
            out.append(r)
            b = r.get("best") or {}
            print(f"  {r['verdict']:34} {surname} {year}")
            print(f"      wanted  {title[:88]}")
            if b:
                print(f"      got     {b['title'][:88]}")
                print(f"      {b['id']}  {b['year']}  {b['type']}  cites={b['cited_by']}  "
                      f"J={b['jaccard']}  first={b['first_author']}")

    # ---------------------------------------------------------------- pass 2, for genuine misses
    # NOT an author-plus-title search string: `title.search` matches the title field only, so a
    # surname inside the query is unsatisfiable by construction and returns a fake zero -- A.24
    # generated 15 of 15 that way (`named-retry-author-queries-fake-zeros`). The surname goes in
    # its own filter. Commas SEPARATE filters here; no comma appears inside a value
    # (`openalex-comma-breaks-filters`).
    MISS = {"WRONG_AUTHOR", "WEAK_TITLE_MATCH", "NOT_FOUND"}
    retried = []
    print("\n== pass 2: genuine misses retried through raw_author_name.search ==")
    for r in [x for x in out if x["verdict"] in MISS]:
        stem = " ".join(textnorm.oa_search_safe(r["expect_title"]).split(":")[0].split()[:6])
        params = {"filter": f"raw_author_name.search:{r['expect_author']},title.search:{stem}",
                  "per-page": "8", "select": SELECT}
        d2, err2 = cached_get(oa, params, errors, f"retry {r['expect_author']}")
        cands = (d2 or {}).get("results", [])
        pick = None
        if cands:
            pick = max(cands, key=lambda c: jaccard(r["expect_title"], c.get("display_name") or ""))
        entry = {"expect_author": r["expect_author"], "expect_year": r["expect_year"],
                 "expect_title": r["expect_title"], "pass1_verdict": r["verdict"],
                 "n_candidates": len(cands),
                 "best": ({"id": pick["id"].rsplit("/", 1)[-1], "title": pick.get("display_name"),
                           "year": pick.get("publication_year"), "type": pick.get("type"),
                           "cited_by": pick.get("cited_by_count"),
                           "first_author": first_author(pick),
                           "jaccard": round(jaccard(r["expect_title"],
                                                    pick.get("display_name") or ""), 3)}
                          if pick else None)}
        entry["verdict"] = ("RECOVERED" if pick and entry["best"]["jaccard"] >= 0.4
                            else "STILL_MISSING")
        retried.append(entry)
        b = entry["best"] or {}
        print(f"  {entry['verdict']:14} {r['expect_author']} {r['expect_year']}  "
              f"-> {(b.get('title') or 'nothing')[:74]}")
        if b:
            print(f"      {b.get('id')}  {b.get('year')}  {b.get('type')}  J={b.get('jaccard')}  "
                  f"first={b.get('first_author')}")

    ok = sum(1 for r in out if r["verdict"] == "OK")
    print(f"\nresolved OK: {ok}/{len(out)}   "
          f"cache hit/miss {oa.stats['hit']}/{oa.stats['miss']}   pool {POOL}")

    blob = {"date": DATE, "inherited": inherited, "resolved": out, "retried": retried,
            "errors": [{"label": l, "error": e} for l, e in errors],
            "counts": {"inherited_confirmed": sum(c["confirmed"] for c in inherited),
                       "inherited_total": len(inherited),
                       "resolved_ok": ok, "resolved_total": len(out),
                       "retry_recovered": sum(1 for r in retried if r["verdict"] == "RECOVERED"),
                       "retry_total": len(retried),
                       "book_reviews_caught_by_author_gate":
                           sum(1 for r in out if r["verdict"] in
                               ("REVIEW_OF_THE_WORK", "BOOK_RESOLVED_TO_NONBOOK")),
                       "book_reviews_caught_by_shadow_regex":
                           sum(1 for r in out if r.get("shadow_regex_caught_it"))}}
    (LOGS / f"c3f-anchors-{DATE}.json").write_text(json.dumps(blob, indent=2) + "\n")

    md = [f"# C.3.f anchors — {DATE}", "",
          "Generated by `source/build/goldset/380_c3f_anchors.py`. Do not edit by hand.", "",
          f"- inherited from `377`, confirmed by id: **{sum(c['confirmed'] for c in inherited)} of "
          f"{len(inherited)}**",
          f"- hand-named works resolved cleanly: **{ok} of {len(out)}**", "",
          "A verdict other than `OK` is a record to read, not a record to drop. `SHADOW_ONLY` and",
          "`WRONG_FIRST_AUTHOR` are the two that a similarity score alone would have accepted.", "",
          "## Hand-named anchors and decoys", "",
          "| kind | arm | wanted | verdict | resolved to | id | year | cites |",
          "|---|---|---|---|---|---|---|---|"]
    for r in out:
        b = r.get("best") or {}
        md.append(f"| {r['kind']} | {r['arm']} | {r['expect_author']} {r['expect_year']} | "
                  f"`{r['verdict']}` | {(b.get('title') or '—')[:70]} | "
                  f"`{b.get('id', '—')}` | {b.get('year', '—')} | {b.get('cited_by', '—')} |")
    md += ["", "## Inherited, confirmed by id", "",
           "| id | confirmed | title | year | cites |", "|---|---|---|---|---|"]
    for c in inherited:
        md.append(f"| `{c['id']}` | {'yes' if c['confirmed'] else '**NO**'} | "
                  f"{(c['title'] or '—')[:70]} | {c['year'] or '—'} | {c['cited_by'] or '—'} |")
    md.append("")
    (LOGS / f"c3f-anchors-{DATE}.md").write_text("\n".join(md))
    print(f"wrote c3f-anchors-{DATE}.json and .md")


main()
