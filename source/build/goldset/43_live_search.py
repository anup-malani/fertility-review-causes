#!/usr/bin/env python3
"""
43_live_search.py — Part-4-full: the live OpenAlex production pull (canonical §7 move 2,
production half). Replaces the openalex_universe() stub in 22_cv_breadth.py.

Builds the two-block boolean from the frozen production query
(literature/search-logs/{slug}-production-query.json):

    ( OR of fertility-block terms )  AND  ( OR of pension/OAS-block terms )

against OpenAlex **title.search** — NOT title_and_abstract.search. The CV recall that
selected this query was measured TITLE-ONLY (the pilot's conservative lower bound), so the
faithful live operationalization searches titles; abstracts enter downstream at the Haiku/
Sonnet screen, not the search. (title_and_abstract.search on the same terms returns 251,950
because bare mined singles like "security"/"insurance"/"child" — precise as title tokens —
explode across abstracts; title.search returns ~11.7k, in line with Anup's ~6.4k baseline.)
Reports meta.count (the real universe-size
budget denominator), then cursor-paginates the whole result set with abstracts inline
(one rich select — no per-work enrichment), reconstructs abstracts from the inverted
index, dedups DOI-first then normalized-title, and runs a live gold-recall check (does the
real universe recover the frozen gold?).

Substrate (per workflow §3): project-level cache (each page cached, so a re-run resumes
free), polite mailto + inter-request sleep, a HARD page cap with graceful fail-and-resume
(the OpenAlex daily-budget 404 mode is caught and the run stops resumably, never sleeps on
Retry-After), and separate --count / full modes.

Usage:
  python3 43_live_search.py --count      # just the universe count (cheap, 1 request)
  python3 43_live_search.py              # full resumable pull
Outputs:
  literature/search-logs/{slug}-live-corpus.json     deduped records (id,doi,title,year,abstract,authors,venue)
  literature/search-logs/{slug}-live-search-log.md    universe count, pull stats, gold-recall
  cache/live_search/page_*.json                        per-page cache (resumable)
"""
import json, re, sys, time, subprocess
from pathlib import Path
from collections import OrderedDict

SLUG = "old-age-security-pension-crowdout"
HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
LOGS = REPO / "literature" / "search-logs"
CACHE = HERE / "cache" / "live_search"
CACHE.mkdir(parents=True, exist_ok=True)
MAILTO = "shravanh@uchicago.edu"
PER_PAGE = 200
MAX_PAGES = 300                 # hard cap: 60k records; fail-and-resume before this
SELECT = "id,doi,title,publication_year,authorships,primary_location,abstract_inverted_index"
SLEEP = 0.6

def curl(url, tries=4):
    """Bounded retry/backoff. Returns parsed JSON, or None only after persistent failure
    (which the caller treats as the OpenAlex daily-budget/rate mode -> fail-and-resume)."""
    for attempt in range(tries):
        r = subprocess.run(["curl", "-s", "-m", "40", "-A", f"oas-review/1.0 (mailto:{MAILTO})", url],
                           capture_output=True, text=True)
        if r.returncode == 0 and r.stdout.strip():
            try:
                d = json.loads(r.stdout)
                # a real budget/rate response carries an error field, not results
                if "error" in d and "results" not in d:
                    if attempt < tries - 1:
                        time.sleep(2 ** attempt); continue
                    return None
                return d
            except json.JSONDecodeError:
                pass
        if attempt < tries - 1:
            time.sleep(2 ** attempt)      # 1,2,4s backoff on transient timeout/blip
    return None

def clean_term(t):
    """Strip wildcards/punctuation; OpenAlex stems, so 'fertilit*'->'fertilit' etc."""
    t = t.strip().lower().rstrip("*")
    t = t.replace("-", " ")
    t = re.sub(r"\s+", " ", t).strip()
    return t

def build_group(terms):
    seen, out = set(), []
    for t in terms:
        c = clean_term(t)
        if not c or c in seen:
            continue
        seen.add(c)
        out.append(f'"{c}"' if " " in c else c)   # quote phrases
    return "(" + " OR ".join(out) + ")"

def build_query():
    q = json.load(open(LOGS / f"{SLUG}-production-query.json"))
    fert = q["fertility_block"]["backbone"] + q["fertility_block"]["mined_expansion"]
    pens = q["pension_oas_block"]["backbone"] + q["pension_oas_block"]["mined_expansion"]
    return f"{build_group(fert)} AND {build_group(pens)}"

def encode(s):
    from urllib.parse import quote
    return quote(s, safe="")

def deinvert(inv):
    if not inv:
        return ""
    positions = []
    for word, idxs in inv.items():
        for i in idxs:
            positions.append((i, word))
    positions.sort()
    return " ".join(w for _, w in positions)

def norm_title(t):
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9\s]", " ", (t or "").lower())).strip()

def main():
    count_only = "--count" in sys.argv
    query = build_query()
    base = (f"https://api.openalex.org/works?filter=title.search:{encode(query)}"
            f"&select={SELECT}&per-page={PER_PAGE}&mailto={MAILTO}")

    # universe count (cheap)
    head = curl(base + "&per-page=1")
    if not head or "meta" not in head:
        print("ERROR: no response / budget-exhausted on count request; try after UTC reset.", file=sys.stderr)
        sys.exit(2)
    universe = head["meta"]["count"]
    print(f"UNIVERSE (meta.count) = {universe:,}", file=sys.stderr)
    print(f"query = {query[:160]}...", file=sys.stderr)
    if count_only:
        (LOGS / f"{SLUG}-live-search-log.md").write_text(
            f"# Live search — universe count only\n\nUNIVERSE = {universe:,}\n\nquery:\n\n    {query}\n")
        return

    # resumable cursor pagination
    records = OrderedDict()
    cursor = "*"
    page = 0
    budget_hit = False
    while cursor and page < MAX_PAGES:
        ck = CACHE / f"page_{page:04d}.json"
        if ck.exists():
            data = json.load(open(ck))
        else:
            data = curl(base + f"&cursor={encode(cursor)}")
            if not data or "results" not in data:
                print(f"budget/error at page {page}; stopping resumably (re-run to continue).", file=sys.stderr)
                budget_hit = True
                break
            json.dump(data, open(ck, "w"))
            time.sleep(SLEEP)
        for w in data["results"]:
            wid = (w.get("id") or "").rsplit("/", 1)[-1]
            if wid:
                records[wid] = w
        cursor = data["meta"].get("next_cursor")
        page += 1
        if page % 10 == 0:
            print(f"  page {page}, {len(records)} records so far", file=sys.stderr)

    # flatten + dedup (DOI-first, then normalized title)
    by_doi, by_title, out = {}, {}, []
    dup = 0
    for wid, w in records.items():
        doi = (w.get("doi") or "").lower().replace("https://doi.org/", "") or None
        title = w.get("title") or ""
        nt = norm_title(title)
        if doi and doi in by_doi:
            dup += 1; continue
        if not doi and nt and nt in by_title:
            dup += 1; continue
        rec = {
            "paperId": wid, "doi": doi, "title": title,
            "year": w.get("publication_year"),
            "abstract": deinvert(w.get("abstract_inverted_index")),
            "authors": "; ".join(a.get("author", {}).get("display_name", "")
                                  for a in (w.get("authorships") or [])[:8]),
            "venue": ((w.get("primary_location") or {}).get("source") or {}).get("display_name"),
        }
        if doi: by_doi[doi] = wid
        if nt: by_title[nt] = wid
        out.append(rec)

    json.dump(out, open(LOGS / f"{SLUG}-live-corpus.json", "w"), indent=2, ensure_ascii=False)

    # live gold-recall check: are the frozen gold papers in the pull?
    A = json.load(open(LOGS / f"{SLUG}-tier-a-frozen.json"))
    B = json.load(open(LOGS / f"{SLUG}-tier-b-frozen.json"))
    gold_ids = {g.get("doi", "").lower().replace("https://doi.org/", "") for g in A if g.get("doi")}
    gold_ids |= {g.get("doi", "").lower().replace("https://doi.org/", "") for g in B if g.get("doi")}
    gold_ids.discard("")
    gold_titles = {norm_title(g["title"]) for g in A} | {norm_title(g["title"]) for g in B}
    pulled_dois = {r["doi"] for r in out if r["doi"]}
    pulled_titles = {norm_title(r["title"]) for r in out}
    rec_by_doi = len(gold_ids & pulled_dois)
    gold_found = sum(1 for gt in gold_titles if gt in pulled_titles)

    n_abs = sum(1 for r in out if len(r["abstract"]) > 30)
    log = [f"# Live OpenAlex production pull — {SLUG}", "",
           f"- **universe (meta.count):** {universe:,}",
           f"- **pages pulled:** {page} (cap {MAX_PAGES}); budget-hit: {budget_hit}",
           f"- **records after dedup:** {len(out):,} ({dup:,} duplicates dropped)",
           f"- **with usable abstract:** {n_abs:,} ({n_abs/max(len(out),1):.0%})", "",
           "## Live gold-recall check (does the real universe recover the frozen gold?)", "",
           f"- gold DOIs recovered in the pull: **{rec_by_doi} / {len(gold_ids)}** "
           f"({rec_by_doi/max(len(gold_ids),1):.0%})",
           f"- gold titles recovered (normalized): **{gold_found} / {len(gold_titles)}** "
           f"({gold_found/max(len(gold_titles),1):.0%})", "",
           "> This is the universe-level recall (before D1/Haiku/Sonnet screening) — the ceiling the "
           "screen funnels down from. Gold not in the universe is a query-coverage miss (feeds query "
           "revision); gold in the universe but later dropped is a screening loss.", "",
           "## Query", "", f"    {query}", "",
           "*Next: D1 deterministic rank + cutoff (44) → Haiku recall filter → Sonnet precision + "
           "estimand extraction → estimand gate + tiers.*"]
    if budget_hit:
        log.insert(3, "\n> ⚠️ **Partial pull** — budget/rate limit hit; re-run `43_live_search.py` after "
                      "the UTC reset to resume from cache (completed pages are cached).\n")
    (LOGS / f"{SLUG}-live-search-log.md").write_text("\n".join(log) + "\n")

    print(f"\nuniverse {universe:,} | pulled {len(out):,} (abs {n_abs:,}) | dups {dup:,} | "
          f"gold-recall DOI {rec_by_doi}/{len(gold_ids)} title {gold_found}/{len(gold_titles)}",
          file=sys.stderr)
    print(f"-> {SLUG}-live-corpus.json ; {SLUG}-live-search-log.md", file=sys.stderr)
    if budget_hit:
        print("PARTIAL (budget hit) — re-run to resume from cache.", file=sys.stderr)
        sys.exit(3)

if __name__ == "__main__":
    main()
