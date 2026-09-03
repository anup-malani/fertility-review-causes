#!/usr/bin/env python3
"""319 — C.2.b cold-start anchor resolution (TICK-079).

A DIRECT PORT of 307 (C.6.a), which is the only copy of this resolver carrying all four fixes
TICK-074 records PLUS the three defects C.6.a found on Easterlin's *Birth and Fortune* -- the
one-directional stem test, the first-author gate that could refuse a winner but not promote the right
record, and an early exit conditioned on a different test than the verdict. The twelve copies on
`main` carry none of it. Ported deliberately rather than re-derived.

**One new fix, found on this chapter's candidate list.** OpenAlex stores some titles with HTML
markup: this chapter's control record is indexed as `<i>'Two children to make ends meet'</i>: the
ideal family size...`. `_fold` strips non-alphanumerics to spaces, so `<i>` became the token `i` on
both ends of the string -- spurious tokens that deflate Jaccard against a clean candidate title and
break contiguous stem containment outright. Tags are now removed before folding. Reported to TICK-074
as defect 9; it is in every copy of this resolver.

Two additions carried from C.6.a.

**A DOI rung, ahead of the title rungs.** Eighteen of the thirty-two candidates were harvested from
other chapters' pools by script 317 and arrive carrying a DOI. A DOI is an exact key; putting a title
round-trip in front of it can only lose the record (`title-stem-indexing-defeats-resolver`).

**The candidate list is split into `control` and `hand`, and the two are scored separately.** The
eighteen controls are records that demonstrably exist — another chapter retrieved them, and their
titles and ids were taken from the harvest programmatically rather than retyped
(`never-hand-type-a-record-id`). A resolver failure on those is a broken resolver. The fourteen
hand-typed candidates are author-year-title
triples written from knowledge of the literature, and a failure on one of those may be a ghost
citation. Without the split, a run of NO_RESULTS is uninterpretable: it could be the tool or it could
be the literature. This is `validate-a-null-detector-on-positives` built into the candidate list
rather than bolted on afterwards.

Every fix inherited from 275:
  - `filter=title.search:"VALUE"` — `title.search` is NOT a root parameter, and every anchor script
    in this repo silently fell through to `search=` until C.3.e measured which channel produced each
    match. Double-quoting the value is what survives a comma; `%2C` does not, though the API's own
    error message recommends it.
  - `_fold()`: NFKD + translit BEFORE the ASCII strip, so accents survive; apostrophes and dashes
    folded rather than deleted (`norm-shatters-accents`, TICK-074).
  - FIRST-author agreement, not membership (`book-canon-first-author`).
  - Contiguous title-stem containment in both directions, with an ALLOWLIST of structural qualifiers
    on the suffix side — unbounded suffix containment admits "Replication data for: <title>", which
    shares the article's authors and year and so defeats both other gates.
  - A pre-colon-clause rung, because a title spanning a colon does not match as one stemmed phrase.
  - Non-study types scored below the study, never silently.
  - Every non-match written out with its top candidate for a human read: OpenAlex's own metadata is
    sometimes the error, and a NO-MATCH must never be recorded as an absence
    (`candidate-attribution-is-the-error`, `refusals-read-as-zeros`).

Usage: python3 source/build/goldset/319_c2b_cold_start_anchors.py [--out PATH]
"""
import json, os, re, subprocess, sys, time, unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(sys.argv[sys.argv.index("--out") + 1]) if "--out" in sys.argv else \
    ROOT / "literature/search-logs/child-cost-direct-cold-start-anchors.json"

def load_key():
    for line in (ROOT / ".env").read_text().splitlines():
        if line.startswith("OPENALEX_API_KEY="):
            return line.split("=", 1)[1].strip()
    return ""

KEY = load_key()
MAILTO = "shravanh@uchicago.edu"

TRANSLIT = {"ø": "o", "æ": "ae", "ß": "ss", "đ": "d", "ł": "l", "þ": "th"}

def _fold(s: str) -> str:
    s = (s or "").lower()
    # OpenAlex stores some titles with HTML markup. Stripping non-alphanumerics turns "<i>" into the
    # token "i", which deflates Jaccard and breaks contiguous stem containment. Remove tags and
    # decode the handful of entities that appear in titles BEFORE any other folding.
    s = re.sub(r"<[^>]{1,20}>", " ", s)
    for ent, ch in (("&amp;", "&"), ("&lt;", " "), ("&gt;", " "), ("&quot;", " "),
                    ("&apos;", "'"), ("&#39;", "'"), ("&nbsp;", " ")):
        s = s.replace(ent, ch)
    for k, v in TRANSLIT.items():
        s = s.replace(k, v)
    # fold punctuation that indexes drop, BEFORE the ASCII strip
    s = s.replace("’", "'").replace("‘", "'")
    s = re.sub(r"[‐-―]", "-", s)
    s = s.replace("'", "").replace("-", " ")
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = re.sub(r"[^a-z0-9 ]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()

def toks(s): return [t for t in _fold(s).split() if t]

def jaccard(a, b):
    A, B = set(toks(a)), set(toks(b))
    return len(A & B) / len(A | B) if A | B else 0.0

# Suffix containment is UNSOUND in general. It was added here to catch book chapters
# indexed as "Chapter 8 <title>", and it promptly admitted four "Replication data for:
# <title>" deposits -- which share the article's authors AND its year, so the author and
# year gates gave exactly zero protection. Named qualifiers only, as an ALLOWLIST.
STEM_PREFIX_OK = re.compile(r"^(chapter|part|section|volume)( [0-9ivxl]+)?$")


def is_stem(cand, got):
    """cand's tokens sit contiguously inside got's.

    Prefix direction (the index DROPPED a subtitle) is unrestricted.
    Suffix direction (the record ADDED a prefix) is allowed only when the added prefix is
    an allowlisted structural qualifier -- "Chapter 8", "Part II". Anything else is a
    shadow record: replication data, editorials, comments, recommendations.
    """
    c, g = toks(cand), toks(got)
    if len(c) < 4 or len(g) <= len(c):
        return False
    if g[:len(c)] == c:
        return True                      # dropped subtitle
    for i in range(1, len(g) - len(c) + 1):
        if g[i:i + len(c)] == c:
            return bool(STEM_PREFIX_OK.match(" ".join(g[:i])))
    return False


def is_stem_reversed(cand, got):
    """The MIRROR case, and the one that actually cost this chapter an anchor.

    `is_stem` tolerates the index carrying a LONGER title than the candidate. Easterlin's
    *Birth and Fortune: The Impact of Numbers on Personal Welfare* is indexed as the bare
    *Birth and fortune* -- the index has the SHORTER title -- which `is_stem` cannot see,
    so the book scored 0.33 on Jaccard while four reviews carrying its full subtitle scored
    1.00. `title-stem-indexing-defeats-resolver` had only ever been fixed in one direction.

    This direction is riskier: a short generic record title is contained in many candidates.
    So it is gated -- the caller applies it only where the FIRST-author gate passes.
    """
    c, g = toks(cand), toks(got)
    if len(g) < 3 or len(c) <= len(g):
        return False
    return c[:len(g)] == g


# An anchor is a STUDY. A data deposit, a peer review, an erratum or a paratext record can
# carry the study's exact title, authors and year, so nothing downstream distinguishes it.
# Refuse by type, and say so, rather than letting it score.
NON_STUDY_TYPES = {"dataset", "peer-review", "paratext", "editorial", "erratum",
                   "grant", "retraction", "letter", "other"}


def last_name(author_field: str) -> str:
    t = toks(author_field)
    return t[-1] if t else ""

# OpenAlex treats '?' as a wildcard and '!' as negation inside search values; a query
# carrying one comes back 200 with an error body that reads as an empty literature
# (openalex-wildcard-refusal + refusals-read-as-zeros). Strip them from the VALUE.
# Commas are fatal in a filter value but harmless in search= (openalex-comma-breaks-filters).
def _safe_query(v: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[?!]", " ", v)).strip()

# THE TITLE CHANNEL WAS DEAD. `title.search` is not a root parameter -- OpenAlex
# rejects the whole request with "title.search is not a valid parameter", so every
# resolution in this repo's anchor scripts has silently fallen through to `search=`,
# which ranks by relevance over the whole record and is much weaker. The correct form
# is filter=title.search:VALUE. Three further facts, measured here 2026-09-01:
#   - a bare comma in a filter VALUE is fatal;
#   - %2C does NOT save it -- and the API's own error message tells you to use %2C,
#     so the documented fix is wrong;
#   - wrapping the value in double quotes DOES work, and keeps phrase matching.
# So the title channel runs two rungs: quoted phrase first, then comma-stripped
# tokens (which survives an index that dropped a subtitle), then `search=` as before.
def _filter_title(v: str, quoted: bool) -> str:
    v = _safe_query(v).replace('"', " ")
    v = re.sub(r"\s+", " ", v).strip()
    if quoted:
        return f'title.search:"{v}"'
    return "title.search:" + v.replace(",", " ")


def oa(params):
    params = {k: (_safe_query(v) if k in ("search",) else v)
              for k, v in params.items()}
    args = ["curl", "-s", "-G", "https://api.openalex.org/works"]
    for k, v in params.items():
        args += ["--data-urlencode", f"{k}={v}"]
    args += ["--data-urlencode", f"api_key={KEY}", "--data-urlencode", f"mailto={MAILTO}"]
    r = subprocess.run(args, capture_output=True, text=True, timeout=90)
    if r.returncode != 0:
        return {"_error": f"curl rc={r.returncode}"}
    try:
        d = json.loads(r.stdout)
    except json.JSONDecodeError:
        # a 200 with a non-JSON body is a query-syntax refusal, not an empty literature
        return {"_error": "non-JSON body", "_body": r.stdout[:300]}
    # A refusal is JSON too. No meta.count means the query was not executed; say so
    # loudly rather than letting it fall through to "no results".
    if "meta" not in d or d.get("meta", {}).get("count") is None:
        return {"_error": "no meta.count - query refused, NOT an empty literature",
                "_body": r.stdout[:300]}
    return d

SELECT = "id,doi,display_name,publication_year,type,authorships,primary_location,cited_by_count"

def oa_by_id(oaid):
    args = ["curl", "-s", "-G", f"https://api.openalex.org/works/{oaid}",
            "--data-urlencode", f"select={SELECT}",
            "--data-urlencode", f"api_key={KEY}", "--data-urlencode", f"mailto={MAILTO}"]
    r = subprocess.run(args, capture_output=True, text=True, timeout=90)
    if r.returncode != 0:
        return {"_error": f"curl rc={r.returncode}"}
    try:
        return json.loads(r.stdout)
    except json.JSONDecodeError:
        return {"_error": "non-JSON body", "_body": r.stdout[:300]}


def resolve(c):
    rec = dict(c)
    rec["queries"] = []
    best = None
    seen_all = []

    # Inherited candidates already carry a resolved id. Round-tripping them through a
    # title query can only lose them, so fetch by id and record the live title, which
    # is how the C.2.c snapshot's staleness becomes visible instead of silent.
    if c.get("openalex"):
        w = oa_by_id(c["openalex"])
        rec["queries"].append({"mode": "by_id", "error": w.get("_error"),
                               "count": None if w.get("_error") else 1})
        if not w.get("_error"):
            got = w.get("display_name") or ""
            auths = [a.get("author", {}).get("display_name", "") for a in w.get("authorships", [])]
            rec["top_candidate"] = {
                "oa_id": w.get("id"), "doi": w.get("doi"), "title": got,
                "year": w.get("publication_year"), "type": w.get("type"),
                "venue": ((w.get("primary_location") or {}).get("source") or {}).get("display_name"),
                "authors_first": auths[0] if auths else None,
                "cited_by": w.get("cited_by_count"),
                "jaccard": round(jaccard(c["title"], got), 3),
                "stem": False, "first_author_ok": None, "year_ok": True,
                "score": 1.0, "via": "by_id"}
            rec["verdict"] = "MATCH_BY_ID"
            rec["title_drift"] = (_fold(c["title"]) != _fold(got))
            return rec

    # A DOI is an exact key. Try it before any title round-trip.
    if c.get("doi"):
        d = oa({"filter": f'doi:{c["doi"]}', "per-page": "1", "select": SELECT})
        rec["queries"].append({"mode": "doi", "error": d.get("_error"),
                               "count": d.get("meta", {}).get("count")})
        results = d.get("results") or []
        if results:
            w = results[0]
            got = w.get("display_name") or ""
            auths = [a.get("author", {}).get("display_name", "") for a in w.get("authorships", [])]
            rec["top_candidate"] = {
                "oa_id": w.get("id"), "doi": w.get("doi"), "title": got,
                "year": w.get("publication_year"), "type": w.get("type"),
                "venue": ((w.get("primary_location") or {}).get("source") or {}).get("display_name"),
                "authors_first": auths[0] if auths else None,
                "cited_by": w.get("cited_by_count"),
                "jaccard": round(jaccard(c["title"], got), 3),
                "stem": False, "first_author_ok": None, "year_ok": True,
                "score": 1.0, "via": "doi"}
            rec["verdict"] = "MATCH_BY_DOI"
            rec["title_drift"] = (_fold(c["title"]) != _fold(got))
            return rec

    head = c["title"].split(":")[0].strip()
    rungs = ["filter_title_quoted"]
    # The head rung used to require 4+ tokens. Easterlin's book has a 3-token head ("Birth and
    # Fortune") and the index carries exactly that, with the subtitle dropped -- so the rung that
    # would have found it was the one excluded by the token floor. Admit a 3-token head where a
    # first author is available to gate on; without one, keep the floor at 4.
    floor = 3 if (c.get("first_author") or "").strip() else 4
    if head and head != c["title"].strip() and len(toks(head)) >= floor:
        rungs.append("filter_title_head_quoted")
    rungs += ["filter_title_bare", "search"]
    for mode in rungs:
        if mode == "search":
            params = {"search": c["title"]}
        elif mode == "filter_title_head_quoted":
            params = {"filter": _filter_title(head, True)}
        else:
            params = {"filter": _filter_title(c["title"], mode.endswith("quoted"))}
        params.update({"per-page": "5", "select": SELECT})
        d = oa(params)
        rec["queries"].append({"mode": mode, "error": d.get("_error"),
                               "count": d.get("meta", {}).get("count")})
        if d.get("_error"):
            continue
        for w in d.get("results", []):
            got = w.get("display_name") or ""
            j = jaccard(c["title"], got)
            stem = is_stem(c["title"], got)
            auths = [a.get("author", {}).get("display_name", "") for a in w.get("authorships", [])]
            want_first = (c.get("first_author") or "").strip()
            if not want_first:
                first_ok = None          # gate not applicable, never a refusal
            else:
                first_ok = bool(auths) and last_name(auths[0]) == last_name(want_first)
            yr = w.get("publication_year")
            yr_ok = yr is not None and abs(yr - c["year"]) <= 1
            # The reversed stem is admitted only behind the first-author gate (see is_stem_reversed).
            rstem = bool(first_ok) and is_stem_reversed(c["title"], got)
            score = (j + (0.25 if (stem or rstem) else 0)) \
                + (0.3 if first_ok else 0.15 if first_ok is None else 0) + (0.2 if yr_ok else 0)
            anywhere = bool(want_first) and any(
                last_name(a) == last_name(want_first) for a in auths)
            cand = {"first_author_elsewhere_in_list": anywhere,
                    "oa_id": w.get("id"), "doi": w.get("doi"), "title": got, "year": yr,
                    "type": w.get("type"),
                    "venue": ((w.get("primary_location") or {}).get("source") or {}).get("display_name"),
                    "authors_first": auths[0] if auths else None,
                    "cited_by": w.get("cited_by_count"),
                    "jaccard": round(j, 3), "stem": stem or rstem, "stem_reversed": rstem,
                    "first_author_ok": first_ok,
                    "year_ok": yr_ok, "score": round(score, 3), "via": mode}
            cand["non_study_type"] = (w.get("type") or "").lower() in NON_STUDY_TYPES
            if cand["non_study_type"]:
                cand["score"] = round(cand["score"] - 1.0, 3)   # never outranks the study
            # Rank on the author gate FIRST. Four reviews of Easterlin's book carry its exact
            # title and list him as a co-author, so on score alone they beat the book 1.20 to
            # 0.83 and the gate could only refuse the winner -- it could not promote the right
            # record sitting in the same result set. Passing an applicable gate outranks
            # everything; failing one outranks nothing.
            seen_all.append(cand)
            rank_key = (0 if cand["first_author_ok"] is False else 1,
                        cand["score"], cand["cited_by"] or 0)
            best_key = None if best is None else (
                0 if best["first_author_ok"] is False else 1,
                best["score"], best["cited_by"] or 0)
            if best_key is None or rank_key > best_key:
                best = cand
        # Do NOT stop on a candidate the gate is going to refuse. A book review carrying the
        # reviewed book's exact title scores 1.20 and fails the first-author gate; breaking on it
        # meant the later rungs -- the ones that can actually reach the book -- never ran, and the
        # verdict was written from a record already known to be wrong. An early exit must be
        # conditioned on the SAME gate the verdict uses.
        if best and best["score"] >= 1.0 and best["first_author_ok"] is not False:
            break
        time.sleep(0.2)
    rec["top_candidate"] = best
    if best is not None:
        rec["twins"] = [s for s in seen_all
                        if s["oa_id"] != best["oa_id"] and s["jaccard"] >= 0.9
                        and s["first_author_ok"] is not False]
    errs = [q for q in rec["queries"] if q.get("error")]
    if best is None and len(errs) == len(rec["queries"]):
        rec["verdict"] = "QUERY_REFUSED"     # never report this as an absence
    elif best is None:
        rec["verdict"] = "NO_RESULTS"
    elif best.get("non_study_type"):
        rec["verdict"] = "NON_STUDY_RECORD"      # a deposit or paratext, not the study
    elif best["first_author_ok"] is not False and (best["jaccard"] >= 0.6 or best["stem"]) and best["year_ok"]:
        rec["verdict"] = "MATCH_STEM" if best["stem"] and best["jaccard"] < 0.6 else "MATCH"
    elif best["jaccard"] >= 0.9 and best["first_author_ok"] is True and not best["year_ok"]:
        # Same title, same FIRST author, different year. That is a version pair -- a working paper
        # and its journal version, or an index dating the record from the wrong one -- not a
        # different study (`version-pair-is-one-study`). Butz and Ward's AER paper is indexed at
        # 1977 carrying 438 citations while a 1979 record of the same title carries 0, so the year
        # gate refuses whichever year the candidate names. Both ids are kept: citations do not
        # follow the version of record, and a snowball seeded on one twin misses the other's
        # citing set (`citations-dont-follow-version-of-record`).
        rec["verdict"] = "MATCH_VERSION_TWIN"
    elif best["jaccard"] >= 0.85 and best["year_ok"]:
        rec["verdict"] = "MATCH_TITLE_AUTHOR_DISAGREES"   # read which side is wrong
    else:
        rec["verdict"] = "NEEDS_HUMAN_READ"
    return rec

CAND = ROOT / "literature/search-logs/child-cost-direct-anchor-candidates.json"
CANDIDATES = json.loads(CAND.read_text())

MATCHED = {"MATCH", "MATCH_STEM", "MATCH_BY_ID", "MATCH_BY_DOI", "MATCH_VERSION_TWIN"}


def main():
    out = []
    for c in CANDIDATES:
        r = resolve(c)
        out.append(r)
        tc = r.get("top_candidate") or {}
        print(f"{r['verdict']:30s} {c['source']:8s} {c['arm']:18s} {c['year']} -> "
              f"{(tc.get('title') or '(none)')[:66]} | {(tc.get('venue') or '')[:28]}")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=2))

    from collections import Counter
    print("\n" + json.dumps(Counter(r["verdict"] for r in out), indent=2))

    # The split that makes a zero interpretable.
    for src in ("control", "hand"):
        rows = [r for r in out if r["source"] == src]
        ok = [r for r in rows if r["verdict"] in MATCHED]
        print(f"\n{src:8s} {len(ok)}/{len(rows)} resolved")
        for r in rows:
            if r["verdict"] not in MATCHED:
                tc = r.get("top_candidate") or {}
                print(f"    {r['verdict']:28s} {r['title'][:56]}"
                      f"  -> top: {(tc.get('title') or '(none)')[:44]}")
    ctrl = [r for r in out if r["source"] == "control"]
    ctrl_ok = sum(1 for r in ctrl if r["verdict"] in MATCHED)
    if ctrl_ok < len(ctrl):
        print("\n*** CONTROLS DID NOT ALL RESOLVE. Read the hand-candidate failures as UNDIAGNOSED:"
              " a broken resolver and a ghost citation look identical until the controls are clean.")
    # ------------------------------------------------------------------ the log, generated
    # `generate-result-tables-never-retype`: emit from the resolved JSON, never by hand.
    from collections import Counter as _C
    L = ["# C.2.b cold-start anchors", "",
         "Generated by `source/build/goldset/319_c2b_cold_start_anchors.py`. Do not edit by hand.",
         "", f"**{sum(1 for r in out if r['verdict'] in MATCHED)}/{len(out)} resolved.**", "",
         "**The candidate list is its own control.** The `control` rows are titles and ids taken "
         "programmatically from records script 317 found in other chapters' pools, so they "
         "demonstrably exist; a failure on one is a broken resolver. The `hand` rows are "
         "author-year-title triples written from knowledge of the literature, and a failure on one "
         "of those may be a ghost citation. Without the split a run of NO_RESULTS is "
         "uninterpretable (`validate-a-null-detector-on-positives`).", ""]
    for src in ("control", "hand"):
        rows = [r for r in out if r["source"] == src]
        ok = sum(1 for r in rows if r["verdict"] in MATCHED)
        L.append(f"- `{src}`: **{ok}/{len(rows)}** resolved")
    L += ["", "## Verdicts", "", "| verdict | n |", "|---|---|"]
    L += [f"| `{k}` | {v} |" for k, v in sorted(_C(r["verdict"] for r in out).items())]
    L += ["", "## Per arm", "", "| arm | resolved | n |", "|---|---|---|"]
    for arm in sorted({r["arm"] for r in out}):
        rows = [r for r in out if r["arm"] == arm]
        L.append(f"| `{arm}` | {sum(1 for r in rows if r['verdict'] in MATCHED)} | {len(rows)} |")
    L += ["", "## Every anchor", "",
          "| src | arm | verdict | candidate | resolved to | year | cites | via |",
          "|---|---|---|---|---|---|---|---|"]
    for r in out:
        tc = r.get("top_candidate") or {}
        L.append(f"| {r['source']} | `{r['arm']}` | `{r['verdict']}` | {r['title'][:58]} | "
                 f"{(tc.get('title') or '(none)')[:58]} | {tc.get('year','')} | "
                 f"{tc.get('cited_by','')} | {tc.get('via','')} |")
    twins = [(r, t) for r in out for t in (r.get("twins") or [])]
    L += ["", "## Version twins — both ids are kept", "",
          f"**{len({r['title'] for r, _ in twins})} of {len(out)} anchors have at least one twin**, "
          f"{len(twins)} twin records in total. Citations do not follow the version of record, so a "
          "snowball seeded on one twin misses the other's citing set "
          "(`citations-dont-follow-version-of-record`).", "",
          "| anchor | kept | cites | twin | twin cites |", "|---|---|---|---|---|"]
    for r, t in twins:
        tc = r["top_candidate"]
        L.append(f"| {r['title'][:44]} | {tc['year']} | {tc['cited_by']} | {t['year']} | "
                 f"{t['cited_by']} |")
    L.append("")
    (OUT.parent / "child-cost-direct-cold-start-anchors-log.md").write_text("\n".join(L))
    print(f"\nwritten: {OUT}")


if __name__ == "__main__":
    main()
