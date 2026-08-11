#!/usr/bin/env python3
r"""
115_d1a_book_review_leads.py — D.1.a. Chase the BOOK_REVIEW_LEAD records to the books they review.

WHAT THESE ARE AND WHY THEY ARE NOT JUNK. `104_`'s first prefilter sent all 262 book reviews to
OFF_OTHER. Reading the rejected sample showed what that deleted: reviews of Jones and Grupp,
*Modernization, Value Change, and Fertility in the Soviet Union*; Yaukey, *Fertility Differences in a
Modernizing Country*; and Fukuda, *Marriage and Fertility Behaviour in Japan* -- on-pair monographs
for which the REVIEW is the only trace the pull returned. A review is not evidence, but it is a
retrieval lead, and the reviewed work is what to chase. This script does the chasing.

THE LEADS ARE MOSTLY FALSE FRIENDS, AND THAT IS THE FIRST RESULT. Of 205 leads, only 65 carry any
fertility signal at all. Seventy-one match on **"birth" in its ORIGIN sense** -- *A Book Forged in
Hell: Spinoza's Scandalous Treatise and the Birth of the Secular Age*, *The Birth of Modern Belief*,
*Religious Politics in Turkey: From the Birth of the Republic to the AKP* -- and a further 69 on
"baby boomers", "secular" or bare "values" in religion-history monographs. This is the same defect
class the prefilter already documents for `secular trend`, where 65 of 117 fires were pure
epidemiology: a demographic stem doing non-demographic work. Triaging BEFORE resolving is therefore
not an optimisation, it is what keeps the API budget off noise and the output readable.

RESOLUTION REUSES `95_`'s GRADED VERDICT, INCLUDING ITS SUBTITLE-DROP FALLBACK. Importing rather than
re-implementing matters here: `95_`'s docstring records a live false negative that Jaccard alone
produced on a canon work whose indexed title dropped its subtitle. Every resolver in this tree that
gates on Jaccard alone repeats it.

TWO GATES ARE LOOSENED ON PURPOSE, AND BOTH ARE FLAGGED RATHER THAN HIDDEN.
  (1) NO AUTHOR. 126 of 205 review titles are a bare book title with no parseable author, so the
      author gate has nothing to test. `95_.verdict()` returns `author_ok=None` there, which is
      falsy, and a silent pass would grade an unverified match exactly like a verified one. Those are
      re-labelled `RESOLVED_NOAUTHOR` -- resolved on title and year alone, a weaker claim, and the
      reader is told which one they are holding.
  (2) YEAR. `95_` uses a symmetric +/-2 for editions and reprints. A review is published AFTER the
      book, typically 0-4 years after and essentially never before, so the window here is asymmetric:
      book year in [review_year - 5, review_year + 1]. Symmetric tolerance would drop real matches on
      slow-reviewing journals and admit books that postdate their own review.

THE OUTPUT IS A COVERAGE CLAIM, SO MEMBERSHIP IS CHECKED AGAINST THE CORPUS, NOT ASSUMED. A lead is
only worth chasing if the book it names is NOT already retrieved. Each resolved monograph is tested
against the v2 live corpus by OpenAlex id; the deliverable is the set that resolves to a real book
record and is absent from the corpus.

Usage:  python3 115_d1a_book_review_leads.py [--no-network]
Output: literature/search-logs/{slug}-book-review-leads.{json,md}
        temp/d1a/lead-resolve-cache.json  (keyed on the query title, the only input to the request)
"""
import argparse, collections, importlib.util, json, os, re, subprocess, sys, time, urllib.parse
from pathlib import Path

SLUG = "postmaterialism-individualism-secularization"
HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
LOGS = REPO / "literature" / "search-logs"
CACHE = REPO / "temp" / "d1a" / "lead-resolve-cache.json"
OUT_JSON = LOGS / f"{SLUG}-book-review-leads.json"
OUT_MD = LOGS / f"{SLUG}-book-review-leads.md"

MAILTO = "shravanh@uchicago.edu"
UA = f"fertility-review/1.0 (mailto:{MAILTO})"
OA_KEY = os.environ.get("OPENALEX_API_KEY", "").strip()
BOOK_TYPES = "book|book-chapter|monograph|reference-entry"
YEAR_BACK, YEAR_FWD = 5, 1          # a review follows its book; see docstring

# --- reuse 95_'s matching helpers rather than re-deriving them ------------------------------------
spec = importlib.util.spec_from_file_location("canon95", HERE / "95_d1a_canon_reresolve.py")
c95 = importlib.util.module_from_spec(spec)
_argv, sys.argv = sys.argv, [sys.argv[0]]
spec.loader.exec_module(c95)
sys.argv = _argv

TAGS = re.compile(r"<[^>]+>")
LEADIN = re.compile(r"^\s*(book\s*reviews?|reviews?|commissioned book review)\s*[:\-—–]\s*", re.I)
IMPRINT = re.compile(r"\s*[\(\[][^)\]]*(?:\bpp\.|\$|press\b|university\b|publish|\d{4}|"
                     r"springer|routledge|palgrave|wiley|blackwell|sage|brill|elsevier|"
                     r"macmillan|harvard|princeton|oxford|cambridge)[^)\]]*[\)\]]\s*$", re.I)
PP_TAIL = re.compile(r"[.,;]?\s*\bPp?\.\s.*$", re.I)
BY_CAP = re.compile(r"^(?P<title>.+?)[.,]\s+By\s+(?P<author>[^.]+)\.", re.S)
BY_LOW = re.compile(r"^(?P<title>.+?)\s+by\s+(?P<author>[A-Z][a-z]+(?:\s+[A-Z][a-z.]+){0,3})", re.S)
AUTH_YEAR = re.compile(r"^(?P<author>[^()]{3,60}?)\s*\((?P<year>1[89]\d{2}|20\d{2})\)\s*(?P<title>.+)$")
AUTH_ITAL = re.compile(r"^(?P<author>[A-Z][^.<]{2,60}?)[.:]\s*<i>(?P<title>[^<]+)</i>")
PUB_TAIL = re.compile(r"\s*[.,]\s*(Princeton|Cambridge|Oxford|New York|London|Chicago|Berkeley|"
                      r"Springer|Routledge|Palgrave|Baltimore|Boston)\b.*$", re.I)

ORIGIN = re.compile(r"\bbirth of\b|\bbirth and (?:growth|formation)\b", re.I)
FERT = re.compile(r"fertilit|childless|childbearing|child-?free|birth ?rate|birth ?control|natalit|"
                  r"contracepti|family size|family planning|reproduct|procreat|demograph|"
                  r"population growth|baby bust|birth ?dearth|nuptialit", re.I)
# on-pair for D.1.a vs a lead that belongs to a sibling hypothesis
OFF_PAIR_OWNER = [(re.compile(r"birth ?control|contracepti|family planning", re.I), "A.3/A.6 contraception"),
                  (re.compile(r"gender|feminis|women'?s (?:education|employment)", re.I), "D.2.a gender")]


def surname(a):
    a = re.sub(r"\(.*?\)", "", a or "").strip().strip(".,")
    a = re.split(r"\s+and\s+|\s*&\s*|,\s*(?=[A-Z][a-z])", a)[0].strip()
    parts = [p for p in re.split(r"\s+", a) if p and p.lower() not in ("jr", "sr", "dr")]
    parts = [p for p in parts if len(p.strip(".,")) > 1]      # drop bare initials
    return parts[-1].strip(".,") if parts else ""


def parse(raw):
    """Review title -> (candidate book title, author surname or '', strategy)."""
    m = AUTH_ITAL.search(raw or "")
    if m:
        return m.group("title").strip(" .,"), surname(m.group("author")), "AUTHOR <i>TITLE</i>"
    t = " ".join(TAGS.sub(" ", raw or "").split())
    t = LEADIN.sub("", t)
    m = AUTH_YEAR.match(t)
    if m:
        return IMPRINT.sub("", m.group("title")).strip(" .,"), surname(m.group("author")), "AUTHOR (YEAR) TITLE"
    m = BY_CAP.match(t)
    if m:
        return m.group("title").strip(" .,"), surname(m.group("author")), "TITLE. By AUTHOR"
    m = BY_LOW.match(t)
    if m and len(m.group("title").split()) >= 3:
        return m.group("title").strip(" .,"), surname(m.group("author")), "TITLE by AUTHOR"
    t = PUB_TAIL.sub("", PP_TAIL.sub("", IMPRINT.sub("", t)))
    return t.strip(" .,"), "", "BARE_TITLE"


def triage(raw):
    if FERT.search(raw or ""):
        return "FERTILITY_SIGNAL"
    return "BIRTH_AS_ORIGIN" if ORIGIN.search(raw or "") else "NO_SIGNAL"


def load_cache():
    return json.loads(CACHE.read_text()) if CACHE.exists() else {}


NAME_STOP = {"the", "of", "and", "in", "a", "an", "to", "for", "on", "from", "with", "his", "her",
             "modern", "new", "american", "birth", "religion", "fertility", "social", "private"}


def strip_leading_name(title):
    """Drop a leading `Author.` / `Author,` / `Author:` segment, if it looks like a person.

    Journals cite reviews as `Ellen Jones and Fred W. Grupp. Modernization, Value Change, and
    Fertility in the Soviet Union` or, lowercased, `sylvia d. hoffert . Private Matters...`. Left in
    place the author tokens are sent to `title.search`, which needs the terms to be in the TITLE, and
    the query returns nothing. This produced 29 spurious no-candidates on the first pass.

    Deliberately returns a QUERY VARIANT rather than editing the parse. Telling a personal name from
    a short title is not reliably decidable -- `Private Matters: American Attitudes...` has the same
    shape as `Amar Sohal: The Muslim Secular` -- so a wrong strip must be survivable. As a variant it
    costs one extra lookup and is still gated on the full parsed title; as a parse decision it would
    silently corrupt the record.
    """
    m = re.match(r"^\s*(?P<name>[^.,:;]{2,60}?)\s*[.,:]\s+(?P<rest>.{10,})$", title or "", re.S)
    if not m:
        return None
    name, rest = m.group("name").strip(), m.group("rest").strip()
    toks = [t for t in re.split(r"\s+", name) if t]
    if not (1 <= len(toks) <= 5) or len(rest.split()) < 3:
        return None
    has_initial = any(re.fullmatch(r"[A-Za-z]\.?", t) for t in toks)
    wordy = [t for t in toks if t.lower().strip(".") not in ("and", "&")]
    looks_name = has_initial or (len(wordy) >= 2 and
                                 not any(t.lower().strip(".,") in NAME_STOP for t in wordy))
    return rest if looks_name else None


def query_variants(title):
    """Progressively shorter queries. `title.search` needs the terms to be THERE.

    The first version of this script sent the full parsed title and resolved 3 of 48, which read
    like an indexing gap and was not one. `Fertility Differences in a Modernizing Country: A Survey
    of Lebanese Couples` returns ZERO book records; drop the subtitle and it returns two, one of
    them the Yaukey monograph that motivated this whole pile. Reviewers quote the full title from
    the dust jacket; indexers frequently record only the head. This is `95_`'s subtitle problem one
    stage earlier -- a grading fallback cannot rescue a candidate the query never returned.

    Tiers are recorded, not merged: a match found only by a truncated query is a weaker claim, and
    grading still gates it on the FULL parsed title, so a short query that pulls back the wrong book
    fails on Jaccard.
    """
    full = " ".join(re.findall(r"[A-Za-z0-9']+", title))
    out = [("full", full)]
    deauth = strip_leading_name(title)
    if deauth and deauth != title:
        out.append(("deauthored", " ".join(re.findall(r"[A-Za-z0-9']+", deauth))))
        out.append(("deauthored_head",
                    " ".join(re.findall(r"[A-Za-z0-9']+", re.split(r"\s*[:—–]\s|\s+-\s+", deauth)[0]))))
    head = " ".join(re.findall(r"[A-Za-z0-9']+", re.split(r"\s*[:—–]\s|\s+-\s+", title)[0]))
    if head and head != full:
        out.append(("head", head))
    toks = full.split()
    if len(toks) > 7:
        out.append(("first7", " ".join(toks[:7])))
    seen, uniq = set(), []
    for tier, q in out:
        if q and len(q.split()) >= 2 and q not in seen:
            seen.add(q)
            uniq.append((tier, q))
    return uniq


def oa_books(title, cache):
    """OpenAlex book-type works matching `title`, trying shorter queries until one bites.

    Returns (candidates, error, tier)."""
    last_err = None
    for tier, q in query_variants(title):
        cands, err = _oa_query(q, cache)
        if err:
            last_err = err
            continue
        if cands:
            return cands, None, tier
    return [], last_err, None


def _oa_query(q, cache):
    key = f"oa-book::{q}"
    if key in cache:
        c = cache[key]
        return c.get("cands"), c.get("error")
    q = urllib.parse.quote(q[:250])
    url = (f"https://api.openalex.org/works?filter=title.search:{q},type:{BOOK_TYPES}"
           f"&select=id,title,type,publication_year,authorships,doi&per-page=5&mailto={MAILTO}")
    if OA_KEY:
        url += f"&api_key={OA_KEY}"
    p = subprocess.run(["curl", "-s", "-m", "45", "-A", UA, "-w", "\n%{http_code}", url],
                       capture_output=True, text=True)
    cands, error = None, None
    if p.returncode != 0:
        error = f"curl rc={p.returncode}"
    else:
        body, _, code = p.stdout.rpartition("\n")
        code = code.strip()
        if code != "200":
            error = f"http {code}: {body[:120]}"
        else:
            try:
                d = json.loads(body)
                cands = [{"id": r.get("id"), "title": r.get("title"), "type": r.get("type"),
                          "year": r.get("publication_year"), "doi": r.get("doi"),
                          "authors": [(a.get("author") or {}).get("display_name", "")
                                      for a in (r.get("authorships") or [])][:5]}
                         for r in d.get("results", [])]
            except Exception as e:
                error = f"parse: {e}"
    cache[key] = {"cands": cands, "error": error}
    return cands, error


def grade(cand, title, author, review_year):
    """95_'s verdict, with the author gate made explicit and the year window made asymmetric."""
    j = c95.jac(title, cand.get("title"))
    c = c95.contain(title, cand.get("title"))
    y = cand.get("year")
    year_ok = y is not None and (review_year - YEAR_BACK) <= y <= (review_year + YEAR_FWD)
    auths = cand.get("authors") or []
    have_author = bool(author) and bool(auths)
    author_ok = any(author.lower() in a.lower() for a in auths) if have_author else None

    title_ok = j >= c95.JACCARD_MIN or c >= c95.CONTAIN_MIN
    if not title_ok:
        return "UNRESOLVED", j, c
    if author_ok is False:
        return "RESOLVED_DISCREPANT", j, c
    if not year_ok:
        # OPENALEX DATES BOOKS BY THE EDITION IT INDEXED, NOT BY FIRST PUBLICATION. `Godly Seed`
        # is indexed 2017 against a 2012 review, `Fertility and Pleasure` 2017 against 2007, both at
        # containment 1.0 -- these are the right books wearing a reprint year. Rejecting them loses
        # real leads; passing them silently would let a same-titled different book through. They are
        # a THIRD state: worth an RA's eye, not worth a coverage claim.
        return "PROBABLE_YEAR_DISCREPANT", j, c
    if c >= c95.CONTAIN_MIN and j < c95.JACCARD_MIN:
        return ("RESOLVED_SUBTITLE" if author_ok else "RESOLVED_NOAUTHOR"), j, c
    return ("RESOLVED" if author_ok else "RESOLVED_NOAUTHOR"), j, c


RESOLVED_OK = ("RESOLVED", "RESOLVED_SUBTITLE", "RESOLVED_NOAUTHOR")
PROBABLE = ("PROBABLE_YEAR_DISCREPANT",)


def rank_status(st):
    return 2 if st in RESOLVED_OK else 1 if st in PROBABLE else 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-network", action="store_true", help="parse and triage only")
    args = ap.parse_args()

    pre = json.loads((LOGS / f"{SLUG}-prefilter-v2.json").read_text())
    leads = pre["retrieval_leads"]
    corpus = json.loads((LOGS / f"{SLUG}-live-corpus-v2.json").read_text())
    crecs = corpus["records"] if isinstance(corpus, dict) and "records" in corpus else corpus
    in_corpus = {str(r.get("openalex_id")) for r in crecs}

    rows = []
    for r in leads:
        ct, au, how = parse(r.get("title"))
        rows.append({"lead_id": r.get("openalex_id"), "review_year": r.get("year"),
                     "review_title": r.get("title"), "cand_title": ct, "cand_author": au,
                     "parse": how, "triage": triage(r.get("title"))})

    tri = collections.Counter(x["triage"] for x in rows)
    print("triage:", dict(tri), flush=True)

    chase = [x for x in rows if x["triage"] == "FERTILITY_SIGNAL"]
    # dedupe on the normalised token set: the same book is reviewed in several journals
    groups = {}
    for x in chase:
        k = " ".join(sorted(c95.norm(x["cand_title"])))
        groups.setdefault(k, []).append(x)
    print(f"fertility-signal leads {len(chase)} -> {len(groups)} distinct candidate books", flush=True)

    if args.no_network:
        OUT_JSON.write_text(json.dumps({"triage": dict(tri), "rows": rows}, indent=1))
        print("parse/triage only; wrote JSON")
        return 0

    cache = load_cache()
    results, errors = [], 0
    try:
        for i, (k, xs) in enumerate(sorted(groups.items()), 1):
            x = max(xs, key=lambda z: (bool(z["cand_author"]), len(z["cand_title"])))
            cands, err, tier = oa_books(x["cand_title"], cache)
            best = None
            if cands:
                def rank(st, j):
                    return (2 if st in RESOLVED_OK else 1 if st in PROBABLE else 0, j)
                for cd in cands:
                    st, j, c = grade(cd, x["cand_title"], x["cand_author"], x["review_year"] or 0)
                    if best is None or rank(st, j) > rank(best["status"], best["jaccard"]):
                        best = {"status": st, "jaccard": round(j, 2), "containment": round(c, 2), **cd}
            if err:
                errors += 1
            results.append({"cand_title": x["cand_title"], "cand_author": x["cand_author"],
                            "review_year": x["review_year"], "parse": x["parse"],
                            "n_reviews": len(xs), "review_ids": [z["lead_id"] for z in xs],
                            "error": err, "query_tier": tier, "best": best,
                            "in_corpus": bool(best and str(best.get("id")) in in_corpus)})
            if i % 10 == 0:
                print(f"  resolved {i}/{len(groups)} (errors {errors})", flush=True)
            time.sleep(0.12)
    finally:
        CACHE.parent.mkdir(parents=True, exist_ok=True)
        CACHE.write_text(json.dumps(cache, indent=1))

    if errors > 0.2 * max(len(groups), 1):
        print(f"REFUSING to write the report: {errors}/{len(groups)} lookups errored. A coverage "
              f"claim computed over failed transport is not a coverage claim.", file=sys.stderr)
        OUT_JSON.write_text(json.dumps({"triage": dict(tri), "results": results,
                                        "errors": errors, "aborted": True}, indent=1))
        return 1

    # COLLAPSE BY RESOLVED IDENTITY, NOT BY QUERY STRING. The pre-resolution dedupe groups on the
    # parsed title, so `Modernization, Value Change And Fertility In The Soviet Union` and
    # `Ellen Jones and Fred W. Grupp. Modernization, Value Change, and Fertility in the Soviet Union`
    # stay separate -- one carries author tokens. Two review styles of one book then resolve to the
    # SAME OpenAlex work and would be counted as two missing books. Yaukey and Chamie both did
    # exactly this. A coverage count that double-counts is worse than no count.
    merged = {}
    for r in results:
        b = r["best"]
        if not b or b["status"] not in RESOLVED_OK + PROBABLE:
            continue
        k = str(b["id"])
        if k in merged:
            m = merged[k]
            m["n_reviews"] += r["n_reviews"]
            m["review_ids"] = sorted(set(m["review_ids"]) | set(r["review_ids"]))
            m["merged_from"] = m.get("merged_from", []) + [r["cand_title"]]
            if rank_status(b["status"]) > rank_status(m["best"]["status"]):
                m["best"], m["cand_author"], m["query_tier"] = b, r["cand_author"] or m["cand_author"], r["query_tier"]
        else:
            merged[k] = dict(r)
    collapsed = list(merged.values())
    dupes = len([r for r in results if r["best"] and r["best"]["status"] in RESOLVED_OK + PROBABLE]) - len(collapsed)

    hit = [r for r in collapsed if r["best"]["status"] in RESOLVED_OK]
    prob = [r for r in collapsed if r["best"]["status"] in PROBABLE]
    missing = [r for r in hit if not r["in_corpus"]]
    present = [r for r in hit if r["in_corpus"]]
    unres = [r for r in results if not (r["best"] and r["best"]["status"] in RESOLVED_OK + PROBABLE)]
    for r in missing + prob:
        r["owner"] = next((o for rx, o in OFF_PAIR_OWNER if rx.search(r["cand_title"])), "D.1.a")
    by_owner = collections.Counter(r["owner"] for r in missing)

    out = {"slug": SLUG, "n_leads": len(leads), "triage": dict(tri),
           "chased": len(chase), "distinct_candidates": len(groups),
           "resolved": len(hit), "already_in_corpus": len(present),
           "missing_from_corpus": len(missing), "probable": len(prob), "unresolved": len(unres),
           "duplicate_books_collapsed": dupes,
           "missing_by_owner": dict(by_owner), "results": results}
    OUT_JSON.write_text(json.dumps(out, indent=1))

    def cite(b):
        """Show the RESOLVED record, not the query. The parsed candidate title still carries author
        prefixes and imprint fragments -- it is what we asked for, not what we found, and printing it
        in a deliverable table invites the reader to check the wrong string."""
        auths = [a for a in (b.get("authors") or []) if a]
        who = auths[0].split()[-1] if auths else "—"
        if len(auths) > 1:
            who += " et al."
        return (b.get("title") or "—"), who

    def row(r):
        b = r["best"]
        t, who = cite(b)
        return (f"| {t[:70]} | {who} | {b['year']} | {b['type']} | {b['status']} | "
                f"{r['n_reviews']} | {r.get('owner', 'D.1.a')} | {b['id'].rsplit('/', 1)[-1]} |")

    OUT_MD.write_text(f"""# D.1.a — chasing the book-review leads to the books

`104_` routed {len(leads)} on-pair book reviews to `BOOK_REVIEW_LEAD` rather than deleting them,
on the ground that a review is not evidence but is a retrieval lead. This resolves the leads to the
works they review and asks the only question that matters: **is the book already in the corpus?**

## The leads are mostly false friends

| triage | n | what it is |
|---|---|---|
| `FERTILITY_SIGNAL` | {tri.get('FERTILITY_SIGNAL', 0)} | carries a fertility, natality or family-formation term — chased below |
| `BIRTH_AS_ORIGIN` | {tri.get('BIRTH_AS_ORIGIN', 0)} | "birth" meaning genesis: *…and the Birth of the Secular Age*, *The Birth of Modern Belief* |
| `NO_SIGNAL` | {tri.get('NO_SIGNAL', 0)} | religion-history monographs caught on "baby boomers", "secular", bare "values" |

Only **{tri.get('FERTILITY_SIGNAL', 0)} of {len(leads)}** leads are plausibly on-pair. The rescue rule
that created this pile is dominated by a demographic stem doing non-demographic work — the same
defect the prefilter already records for `secular trend`, where 65 of 117 fires were epidemiology.
**The rule earned its keep anyway**: it is what preserved the Jones and Grupp, Yaukey and Fukuda
leads that motivated it. The fix is to triage on the way out, not to narrow the rescue on the way in.

## What the chase found

{len(chase)} fertility-signal leads collapse to {len(groups)} distinct candidate titles, and those
resolve to **{len(groups) - dupes} distinct books** — {dupes} pairs of differently-cited reviews turned
out to name the same work. Deduping on the citation string is not enough, because one journal prints
the author ahead of the title and another does not; the identity that counts is the resolved record.

| outcome | n |
|---|---|
| resolved to a book record | {len(hit)} |
| — of those, already in the corpus | {len(present)} |
| — of those, **missing from the corpus** | **{len(missing)}** |
| probable, year disagrees — needs an eyeball | {len(prob)} |
| unresolved (no book record found) | {len(unres)} |
| | {len(hit) + len(prob) + len(unres)} = {len(groups)} candidates − {dupes} collapsed |

### The books the search missed

| book | author | year | type | match | reviews | owner | OpenAlex |
|---|---|---|---|---|---|---|---|
{chr(10).join(row(r) for r in sorted(missing, key=lambda z: -z['n_reviews']))}

### Probable, pending a human look

OpenAlex dates a book by the edition it indexed, not by first publication, so a right book can wear
a reprint year — *Godly Seed* indexed 2017 against a 2012 review, at containment 1.0. These match on
title but not on year, and are a third state rather than a rejection or a claim.

| book | author | review yr | indexed yr | j / c | OpenAlex |
|---|---|---|---|---|---|
{chr(10).join(f"| {cite(r['best'])[0][:56]} | {cite(r['best'])[1]} | {r['review_year']} | {r['best']['year']} | {r['best']['jaccard']} / {r['best']['containment']} | {r['best']['id'].rsplit('/', 1)[-1]} |" for r in sorted(prob, key=lambda z: -z['n_reviews']))}

`RESOLVED` carries a matching author and year. **`RESOLVED_NOAUTHOR` matched on title and year
only** — {sum(1 for r in hit if r['best']['status'] == 'RESOLVED_NOAUTHOR')} of the resolutions, and a
weaker claim — because 126 of the {len(leads)} review titles are a bare book title with no parseable
author, leaving the author gate nothing to test. Those are flagged rather than promoted, since a
silent pass would grade an unverified match exactly like a verified one.

Not every missing book is a D.1.a book. Ownership is assigned from the title: contraception
monographs belong to A.3/A.6 under the rubric's own `OFF_CONTRACEPTIVE_ATTITUDE_A3_A6` cell.
By owner: {', '.join(f'{k} {v}' for k, v in by_owner.most_common()) or 'none'}.

### Unresolved, and the most important lead is among them

{len(unres)} candidates returned no book record. Some are review-essays covering four or five books
at once, which have no single title to resolve and are mostly off-pair anyway. But the pile also
contains **Jones and Grupp, *Modernization, Value Change, and Fertility in the Soviet Union*** — the
book that motivated the whole `BOOK_REVIEW_LEAD` rule. Its reviews are indexed; the monograph has no
book-type record in OpenAlex at all, checked by hand. Same for Musallam, *Sex and Society in Islam*
(three separate reviews) and Hoffert, *Private Matters*.

**This is the sixth independent hit on the books/chapters/dissertations indexing gap, and the
sharpest**: for these works the review is not merely the easiest trace in the corpus, it is the only
one that exists in the index. They cannot be retrieved by any query over OpenAlex, at any recall.
They need a library catalogue and a human.

| lead (as cited by its reviewers) | reviews |
|---|---|
{chr(10).join(f"| {r['cand_title'][:88]} | {r['n_reviews']} |" for r in sorted(unres, key=lambda z: -z['n_reviews'])[:10])}

## What this does not settle

Resolution says a book record exists and is absent from the corpus. It does not say the book reports
an extractable estimate — most monographs of this vintage do not, and several will be narrative. The
{len(missing)} rows are a **retrieval queue for the RA, not an inclusion list**, and they enter the
chapter's PRISMA flow as records identified through other sources.
""")
    print(f"\nresolved {len(hit)}/{len(groups)} | in corpus {len(present)} | MISSING {len(missing)}")
    print(f"wrote {OUT_JSON.name} and {OUT_MD.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
