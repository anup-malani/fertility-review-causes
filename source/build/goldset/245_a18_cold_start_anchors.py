#!/usr/bin/env python3
"""245 — A.18 cold-start anchor resolution (TICK-076).

Resolves candidate anchors for `heritability-fertility-genetic` against OpenAlex.
Candidates are typed from the hypothesis literature and are UNVERIFIED until this
script confirms them; the point is to catch ghost citations before they enter the
scope memo.

Resolver carries the fixes the shared resolver still lacks on main:
  - _fold(): NFKD + translit before the ASCII strip, so accented names survive
    (norm-shatters-accents); apostrophes and dashes folded, not deleted
    (title-search-apostrophe-wrong-match, TICK-074).
  - FIRST-author agreement, not membership (book-canon-first-author).
  - Type vocabulary normalised across Crossref/OpenAlex (resolver-type-vocabulary-mismatch).
  - Title-stem tolerance: a candidate whose title is a PREFIX of the returned title
    (subtitle dropped by the index) is a MATCH_STEM, not a refusal
    (title-stem-indexing-defeats-resolver).
  - Every non-match is written out with the top candidate for a human read rather
    than being recorded as an absence (candidate-attribution-is-the-error).

Usage: python3 245_a18_cold_start_anchors.py [--out PATH]
"""
import json, os, re, subprocess, sys, time, unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(sys.argv[sys.argv.index("--out") + 1]) if "--out" in sys.argv else \
    ROOT / "literature/search-logs/heritability-fertility-genetic-cold-start-anchors.json"

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

def is_stem(cand, got):
    """cand's tokens are a contiguous prefix of got's — the index dropped a subtitle."""
    c, g = toks(cand), toks(got)
    return len(c) >= 4 and len(g) > len(c) and g[:len(c)] == c

def last_name(author_field: str) -> str:
    t = toks(author_field)
    return t[-1] if t else ""

# OpenAlex treats '?' as a wildcard and '!' as negation inside search values; a query
# carrying one comes back 200 with an error body that reads as an empty literature
# (openalex-wildcard-refusal + refusals-read-as-zeros). Strip them from the VALUE.
# Commas are fatal in a filter value but harmless in search= (openalex-comma-breaks-filters).
def _safe_query(v: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[?!]", " ", v)).strip()

def oa(params):
    params = {k: (_safe_query(v) if k in ("search", "title.search") else v)
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

def resolve(c):
    rec = dict(c)
    rec["queries"] = []
    best = None
    for mode in ("title.search", "search"):
        d = oa({mode: c["title"], "per-page": "5", "select": SELECT})
        rec["queries"].append({"mode": mode, "error": d.get("_error"),
                               "count": d.get("meta", {}).get("count")})
        if d.get("_error"):
            continue
        for w in d.get("results", []):
            got = w.get("display_name") or ""
            j = jaccard(c["title"], got)
            stem = is_stem(c["title"], got)
            auths = [a.get("author", {}).get("display_name", "") for a in w.get("authorships", [])]
            first_ok = bool(auths) and last_name(auths[0]) == last_name(c["first_author"])
            yr = w.get("publication_year")
            yr_ok = yr is not None and abs(yr - c["year"]) <= 1
            score = (j + (0.25 if stem else 0)) + (0.3 if first_ok else 0) + (0.2 if yr_ok else 0)
            cand = {"oa_id": w.get("id"), "doi": w.get("doi"), "title": got, "year": yr,
                    "type": w.get("type"),
                    "venue": ((w.get("primary_location") or {}).get("source") or {}).get("display_name"),
                    "authors_first": auths[0] if auths else None,
                    "cited_by": w.get("cited_by_count"),
                    "jaccard": round(j, 3), "stem": stem, "first_author_ok": first_ok,
                    "year_ok": yr_ok, "score": round(score, 3), "via": mode}
            if best is None or cand["score"] > best["score"]:
                best = cand
        if best and best["score"] >= 1.0:
            break
        time.sleep(0.2)
    rec["top_candidate"] = best
    errs = [q for q in rec["queries"] if q.get("error")]
    if best is None and len(errs) == len(rec["queries"]):
        rec["verdict"] = "QUERY_REFUSED"     # never report this as an absence
    elif best is None:
        rec["verdict"] = "NO_RESULTS"
    elif best["first_author_ok"] and (best["jaccard"] >= 0.6 or best["stem"]) and best["year_ok"]:
        rec["verdict"] = "MATCH_STEM" if best["stem"] and best["jaccard"] < 0.6 else "MATCH"
    elif best["jaccard"] >= 0.85 and best["year_ok"]:
        rec["verdict"] = "MATCH_TITLE_AUTHOR_DISAGREES"   # read which side is wrong
    else:
        rec["verdict"] = "NEEDS_HUMAN_READ"
    return rec

CAND = ROOT / "literature/search-logs/heritability-fertility-genetic-anchor-candidates.json"
CANDIDATES = json.loads(CAND.read_text())

def main():
    out = []
    for c in CANDIDATES:
        r = resolve(c)
        out.append(r)
        v = r["verdict"]
        tc = r.get("top_candidate") or {}
        print(f"{v:32s} {c['arm']:12s} {c['first_author']} {c['year']} -> "
              f"{(tc.get('title') or '(none)')[:72]} | {tc.get('venue') or ''}")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=2))
    from collections import Counter
    print("\n" + json.dumps(Counter(r["verdict"] for r in out), indent=2))
    print(f"written: {OUT}")

if __name__ == "__main__":
    main()
