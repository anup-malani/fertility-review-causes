#!/usr/bin/env python3
"""
95_d1a_canon_reresolve.py — re-resolve the D.1.a channel-2 canon off Crossref and Semantic Scholar.

WHY THIS EXISTS, AND IT IS NOT THE REASON THE TICKET PREDICTED. The round-1 log recorded six
UNCONFIRMED rows in 92 as OpenAlex budget exhaustion and instructed the next session to "re-run after
the OpenAlex reset before drawing any conclusion about the two unresolved names." That re-run was
attempted first and returned UNCONFIRMED on all sixteen rows. The budget HAD reset; it is simply too
small to run the resolver:

    {"error":"Rate limit exceeded","message":"Insufficient budget. This request costs $0.001 but you
     only have $0.0002 remaining. Resets at midnight UTC", "dailyRemainingUsd":0.0002}

A single-work fetch by ID succeeds, a title search costs $0.001, and the daily free allowance does not
cover sixteen of them. So the finding is sharper than "OpenAlex moved to a metered budget", which is
what round 1 concluded: **the free tier can no longer support channel-2 canon resolution at all**, and
no amount of waiting fixes it. Every chapter's resolver has to move off OpenAlex title search, not
just this one's. 92 is left intact as the record of what OpenAlex answered while it still could.

TWO PROVIDERS, AND THE SECOND ONE IS NOT REDUNDANCY. Every row is re-resolved against BOTH Crossref
(`query.bibliographic`) and Semantic Scholar (`search/match`), including the four rows 92 already
marked RESOLVED. Two independently-sourced resolvers agreeing on an identifier is materially better
evidence than one asserting it, and this chapter has already been burned once in each direction:
92 caught Schwartz 1992 resolving to the wrong paper entirely, and the round-1 seed table asserted a
DOI for a work that has none. Cross-provider agreement is reported as its own field.

IT ALSO PRODUCES THE THING ROUND 2 ACTUALLY NEEDS. Forward citations come from Semantic Scholar, which
keys on paperId or DOI. van de Kaa 1987 -- the most-cited SDT statement in the field, and the seed
whose hand-typed DOI cost round 1 its entire forward neighbourhood -- carries NO registered DOI, so
there is no DOI to type correctly. S2 `search/match` resolves it to a paperId. That is the whole fix
for the round-1 seed error: seeds are emitted here, from resolver output, and 96 reads this file.

NOTHING HERE ASSERTS AN IDENTIFIER. Each row carries a title, first author and year taken from
HYPOTHESES-v5.md or the theory literature, and is resolved live. Three states are kept distinct and
they mean different things: UNRESOLVED (both providers answered, neither matched -- evidence about the
work), UNCONFIRMED (a provider did not answer -- evidence about the network), RESOLVED_DISCREPANT
(matched, but the author or year disagrees -- resolved to something, possibly not the right thing).

Output: temp/d1a/canon-seeds-reresolved.json
        literature/search-logs/{slug}-canon-reresolution.md
"""
import json, os, re, subprocess, sys, time, urllib.parse

SLUG = "postmaterialism-individualism-secularization"
MAILTO = "shravanh@uchicago.edu"
UA = f"fertility-review/1.0 (mailto:{MAILTO})"
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
LOGS = os.path.join(ROOT, "literature", "search-logs")
TMP = os.path.join(ROOT, "temp", "d1a")
os.makedirs(TMP, exist_ok=True)
IN_JSON = os.path.join(TMP, "canon-seeds.json")
OUT_JSON = os.path.join(TMP, "canon-seeds-reresolved.json")
OUT_MD = os.path.join(LOGS, f"{SLUG}-canon-reresolution.md")
CACHE_PATH = os.path.join(HERE, "d1a_reresolve_cache.json")
cache = json.load(open(CACHE_PATH)) if os.path.exists(CACHE_PATH) else {}

JACCARD_MIN = 0.55   # same as 92: canonical books get retitled by indexers
CONTAIN_MIN = 0.90   # subtitle-drop fallback, see verdict() -- this one caught a live false negative
YEAR_TOL = 2         # book editions and reprints drift
S2_SLEEP = 1.8       # unauthenticated S2 throttles hard; an API key is requested and not yet held

# (label, search title, expected first author, expected year) — carried verbatim from 92's CANON so
# the two runs are comparable row for row. Families and the v5 flag are read from 92's output.
QUERIES = {
    "Lesthaeghe 1983": ("A century of demographic and cultural change in Western Europe", "Lesthaeghe", 1983),
    "van de Kaa 1987": ("Europe's second demographic transition", "van de Kaa", 1987),
    "Lesthaeghe and van de Kaa 1986": ("Twee demografische transities", "Lesthaeghe", 1986),
    "Lesthaeghe and Surkyn 1988": ("Cultural dynamics and economic theories of fertility change", "Lesthaeghe", 1988),
    "Inglehart 1977": ("The silent revolution: changing values and political styles among Western publics", "Inglehart", 1977),
    "Norris and Inglehart 2004": ("Sacred and secular: religion and politics worldwide", "Norris", 2004),
    "Frejka and Westoff 2008": ("Religion, religiousness and fertility in the US and in Europe", "Frejka", 2008),
    "Hagestad and Call 2007": ("Pathways to childlessness: a life course perspective", "Hagestad", 2007),
    "Inglehart 1997": ("Modernization and postmodernization: cultural, economic, and political change in 43 societies", "Inglehart", 1997),
    "Inglehart and Baker 2000": ("Modernization, cultural change, and the persistence of traditional values", "Inglehart", 2000),
    "Schwartz 1992": ("Universals in the content and structure of values", "Schwartz", 1992),
    "Hofstede 1980": ("Culture's consequences: international differences in work-related values", "Hofstede", 1980),
    "Alesina and Giuliano 2015": ("Culture and institutions", "Alesina", 2015),
    "Enke 2019": ("Kinship, cooperation, and the evolution of moral systems", "Enke", 2019),
    "Voas 2009": ("The rise and fall of fuzzy fidelity in Europe", "Voas", 2009),
    "McQuillan 2004": ("When does religion influence fertility?", "McQuillan", 2004),
}


def norm(t):
    return set(re.findall(r"[a-z0-9]+", re.sub(r"<[^>]+>", " ", (t or "").lower())))


def jac(a, b):
    A, B = norm(a), norm(b)
    return len(A & B) / len(A | B) if A and B else 0.0


def contain(a, b):
    """Containment: how much of the SHORTER title the two share. Jaccard's blind spot, see below."""
    A, B = norm(a), norm(b)
    return len(A & B) / min(len(A), len(B)) if A and B else 0.0


def get(url, tries=4, sleep=1.5):
    key = f"g::{url}"
    if key in cache:
        return cache[key]
    for a in range(tries):
        out = subprocess.run(["curl", "-s", "-m", "50", "-A", UA, url], capture_output=True, text=True)
        if out.returncode == 0 and out.stdout.strip().startswith("{"):
            try:
                d = json.loads(out.stdout)
            except Exception:  # noqa: BLE001
                time.sleep(sleep * (a + 2)); continue
            # S2 answers a genuine no-match with an `error` body, which is an ANSWER, not a failure.
            # Collapsing the two would relabel "this work does not exist" as "the network was down".
            if isinstance(d.get("error"), str) and "not found" in d["error"].lower():
                cache[key] = {"__nomatch__": True}
                return cache[key]
            if "error" in d or d.get("message") == "Too Many Requests":
                time.sleep(sleep * (a + 2) * 2); continue
            cache[key] = d
            return d
        time.sleep(sleep * (a + 2))
    return None


def verdict(cand, title, author, year):
    """Grade a candidate against the expected title/author/year. Returns (status, jaccard, containment).

    THE CONTAINMENT FALLBACK IS NOT DEFENSIVE CODING; IT CAUGHT A REAL AND PROPAGATING FALSE NEGATIVE.
    Jaccard divides by the UNION, so a short title queried with a subtitle the index dropped is
    penalised in proportion to the subtitle's length. Hagestad and Call 2007 -- a name from the v5
    `seminal` field -- was queried as "Pathways to childlessness: a life course perspective" and is
    indexed by Crossref as "Pathways to Childlessness". Four extra query tokens against three shared
    ones gives J = 0.43, under the 0.55 gate, so the first pass reported UNRESOLVED on a record whose
    BOTH author surnames and whose year matched exactly, carrying 82 citations and a live DOI.

    That would have been recorded as a second v5 seminal name that does not exist. It is instead a
    property of the metric: containment of the shorter title is 1.0. The gate is therefore Jaccard OR
    (containment AND author AND year), and the two are kept as separate STATES rather than merged,
    because a subtitle-drop match is a slightly weaker claim than a full title match and the reader
    should see which one they are being handed.

    Every chapter's resolver in this tree gates on Jaccard alone and will false-negative the same way
    on any canon work whose indexed title dropped a subtitle. Worth propagating, same as the
    false-ghost fix in 91.
    """
    j = jac(title, cand.get("title"))
    c = contain(title, cand.get("title"))
    auths = cand.get("authors") or []
    author_ok = any(author.lower().split()[-1] in a.lower() for a in auths) if auths else None
    y = cand.get("year")
    year_ok = (y is not None and abs(y - year) <= YEAR_TOL)
    if j < JACCARD_MIN:
        if c >= CONTAIN_MIN and author_ok and year_ok:
            return "RESOLVED_SUBTITLE", j, c
        return "UNRESOLVED", j, c
    return ("RESOLVED" if (author_ok and year_ok) else "RESOLVED_DISCREPANT"), j, c


def resolved(status):
    """Statuses that name a specific work with matching author and year. DISCREPANT is not one."""
    return status in ("RESOLVED", "RESOLVED_SUBTITLE")


def crossref(title):
    sel = "DOI,title,issued,author,container-title,is-referenced-by-count"
    url = ("https://api.crossref.org/works?" + urllib.parse.urlencode(
        {"query.bibliographic": title, "rows": 5, "select": sel, "mailto": MAILTO}))
    d = get(url)
    if d is None:
        return None
    items = ((d.get("message") or {}).get("items")) or []
    best, bestj = None, -1.0
    for it in items:
        t = (it.get("title") or [""])[0]
        j = jac(title, t)
        if j > bestj:
            issued = ((it.get("issued") or {}).get("date-parts") or [[None]])[0]
            best, bestj = {
                "title": t, "year": issued[0] if issued else None,
                "doi": (it.get("DOI") or "").lower(),
                "authors": [f"{a.get('given', '')} {a.get('family', '')}".strip()
                            for a in (it.get("author") or [])][:5],
                "venue": (it.get("container-title") or [""])[0],
                "cited_by": it.get("is-referenced-by-count"),
            }, j
    return best


def s2(title):
    url = ("https://api.semanticscholar.org/graph/v1/paper/search/match?" + urllib.parse.urlencode(
        {"query": title, "fields": "title,year,venue,externalIds,citationCount,authors"}))
    d = get(url, sleep=S2_SLEEP)
    if d is None:
        return None
    if d.get("__nomatch__"):
        return {"__nomatch__": True}
    data = d.get("data") or []
    if not data:
        return {"__nomatch__": True}
    p = data[0]
    ext = p.get("externalIds") or {}
    return {"title": p.get("title"), "year": p.get("year"),
            "doi": (ext.get("DOI") or "").lower() or None,
            "s2id": p.get("paperId"), "pmid": ext.get("PubMed"),
            "authors": [a.get("name", "") for a in (p.get("authors") or [])][:5],
            "venue": p.get("venue") or "", "cited_by": p.get("citationCount")}


def main():
    prior = {r["label"]: r for r in json.load(open(IN_JSON))["rows"]}
    rows = []
    for label, (title, author, year) in QUERIES.items():
        p = prior.get(label, {})
        row = {"label": label, "family": p.get("family"), "from_v5_seminal": p.get("from_v5_seminal"),
               "openalex_status_92": p.get("status"), "openalex_doi_92": p.get("doi") or None}

        for name, fn in (("crossref", crossref), ("s2", s2)):
            cand = fn(title)
            if cand is None:
                row[name] = {"status": "UNCONFIRMED", "note": "provider did not answer"}
            elif cand.get("__nomatch__"):
                row[name] = {"status": "UNRESOLVED", "note": "provider answered, no title match"}
            else:
                st, j, c = verdict(cand, title, author, year)
                row[name] = {"status": st, "jaccard": round(j, 2), "containment": round(c, 2), **cand}
            time.sleep(0.5 if name == "crossref" else S2_SLEEP)

        # AGREEMENT IS ONLY MEANINGFUL BETWEEN TWO PROVIDERS THAT BOTH RESOLVED. The first pass
        # compared DOIs whenever both providers returned one, regardless of status, and so reported
        # Inglehart 1977 as a provider DISAGREEMENT when what actually happened is that Crossref
        # matched a book's front-matter component titled "BIBLIOGRAPHY" at Jaccard 0.0 and was
        # correctly rejected. A rejected candidate's DOI is not a provider's opinion.
        cr, s2r = row["crossref"], row["s2"]
        cd = cr.get("doi") if resolved(cr["status"]) else None
        sd = s2r.get("doi") if resolved(s2r["status"]) else None
        if resolved(cr["status"]) and resolved(s2r["status"]):
            if cd and sd and cd != sd:
                # Same work, two registered DOIs, citations split across them -- the NBER/SSRN twin
                # problem from the C.2.c run, here inside the canon seed table itself. Inglehart and
                # Baker 2000 is JSTOR 10.2307/2657288 (2,454 cites) and SAGE
                # 10.1177/000312240006500103 (5,379 cites), one ASR article. Seed BOTH: dropping
                # either loses whatever fraction of the forward neighbourhood cites that version.
                row["provider_agreement"] = ("TWIN_DOI" if jac(cr.get("title"), s2r.get("title")) >= 0.9
                                             else "DISAGREE")
            else:
                row["provider_agreement"] = "AGREE" if (cd and sd) else "AGREE_NO_DOI"
        elif resolved(cr["status"]) or resolved(s2r["status"]):
            row["provider_agreement"] = "SINGLE_PROVIDER"
        else:
            row["provider_agreement"] = "NEITHER"

        # Seedable identifiers, in the order the snowball can use them. Forward citations come from
        # S2, so a paperId is worth more than a DOI here; van de Kaa 1987 has a paperId and no DOI at
        # all. A row that resolved to nothing emits null, never a plausible-looking string.
        row["seed_s2id"] = s2r.get("s2id") if resolved(s2r["status"]) else None
        row["seed_doi"] = cd or sd
        row["seed_doi_alt"] = sd if (cd and sd and cd != sd) else None
        row["seedable"] = bool(row["seed_s2id"] or row["seed_doi"])
        rows.append(row)
        print(f"{label:32s} cr={row['crossref']['status']:20s} s2={row['s2']['status']:20s} "
              f"{row['provider_agreement']}", file=sys.stderr)
        json.dump(cache, open(CACHE_PATH, "w"))

    json.dump({"slug": SLUG, "rows": rows}, open(OUT_JSON, "w"), indent=1)

    agree = [r for r in rows if r["provider_agreement"] in ("AGREE", "AGREE_NO_DOI")]
    twin = [r for r in rows if r["provider_agreement"] == "TWIN_DOI"]
    single = [r for r in rows if r["provider_agreement"] == "SINGLE_PROVIDER"]
    neither = [r for r in rows if r["provider_agreement"] == "NEITHER"]
    seedable = [r for r in rows if r["seedable"]]
    subtitle = [r for r in rows if "RESOLVED_SUBTITLE" in (r["crossref"]["status"], r["s2"]["status"])]
    L = ["# D.1.a — channel-2 canon re-resolution, off Crossref and Semantic Scholar", "",
         "Run 2026-08-04 by `95_d1a_canon_reresolve.py`. Supersedes the OpenAlex resolution in `92_`",
         "for seeding purposes; 92's output is kept as the record of what OpenAlex answered while the",
         "free tier could still answer. Every row is re-resolved against BOTH providers, including the",
         "four 92 had already marked RESOLVED, because two independently-sourced resolvers agreeing on",
         "an identifier is better evidence than one asserting it.", "",
         f"- rows re-resolved: **{len(rows)}**",
         f"- both providers resolved and agree: **{len(agree)}**",
         f"- same work, two registered DOIs, citations split (`TWIN_DOI`, seed both): **{len(twin)}**",
         f"- one provider resolved, the other did not: **{len(single)}**",
         f"- neither provider resolved: **{len(neither)}**",
         f"- rescued by the subtitle-drop fallback that Jaccard alone false-negatived: **{len(subtitle)}**",
         f"- carry a seedable identifier from a provider that actually resolved: **{len(seedable)}**", "",
         "`RESOLVED_DISCREPANT` rows are NOT seedable and are not counted above: the provider matched a",
         "title but the author or year disagrees, which means it resolved to *something*, not",
         "necessarily to the right thing.", "",
         "| label | v5? | Crossref | S2 | agreement | 92 (OpenAlex) | seed id |",
         "|---|---|---|---|---|---|---|"]
    for r in rows:
        sid = r["seed_s2id"] or r["seed_doi"] or "—"
        L.append(f"| {r['label']} | {'yes' if r['from_v5_seminal'] else ''} | {r['crossref']['status']} "
                 f"| {r['s2']['status']} | {r['provider_agreement']} | {r['openalex_status_92']} | "
                 f"`{str(sid)[:44]}` |")
    open(OUT_MD, "w").write("\n".join(L) + "\n")
    print(f"\nagree={len(agree)} twin={len(twin)} single={len(single)} neither={len(neither)} "
          f"subtitle_rescued={len(subtitle)} seedable={len(seedable)}", file=sys.stderr)
    print(f"wrote {OUT_JSON}\nwrote {OUT_MD}", file=sys.stderr)


if __name__ == "__main__":
    main()
