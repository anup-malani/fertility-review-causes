#!/usr/bin/env python3
"""
53_resolve_and_dedupe_pool.py — fine filter, Job 1 (dedup) + DOI resolution.

Input: the RA-signed 40-study confirmed pool (output/{slug}-pooling-set-final.json),
whose records carry only W-IDs. This step:

  1. Resolves each W-ID to a DOI, cheapest-first and OpenAlex-budget-free:
       wid_doi_map.json  ->  prioritized_doi_corrected.json  ->  title map
       (tier_a_draft + canon_resolved)  ->  guarded Crossref title search.
     Crossref hits are accepted ONLY under the C2 guard (normalized-title token
     Jaccard >= 0.80 AND, when both years are known, |dyear| <= 1) — Crossref's
     top-scored hit is frequently a *different* paper, so an unguarded accept
     would inject false DOIs. Sub-threshold -> left title-keyed (unresolved DOI).
  2. Study-level dedup (reuse 26c's logic): group by normalized DOI, then by
     normalized-title + author/year, so version variants (WP <-> published)
     collapse to one distinct study.

Deterministic given the Crossref cache (crossref_resolve_cache.json); re-runs are
free. Outputs output/{slug}-fine-resolved.json + a short report. No OpenAlex.
"""
import json, os, re, subprocess
from urllib.parse import quote

SLUG = "old-age-security-pension-crowdout"
MAILTO = "shravanh@uchicago.edu"
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
def rp(*a): return os.path.join(ROOT, *a)
GS = lambda f: rp("source", "build", "goldset", f)

def norm(t): return re.sub(r"[^a-z0-9]", "", (t or "").lower())
def toks(t): return set(re.sub(r"[^a-z0-9 ]", " ", (t or "").lower()).split())
def jacc(a, b):
    A, B = toks(a), toks(b)
    return len(A & B) / len(A | B) if (A or B) else 0.0
def clean_doi(d):
    return (d or "").lower().replace("https://doi.org/", "").replace("http://dx.doi.org/", "").strip() or None

# ---- inputs ----
pool = json.load(open(rp("output", f"{SLUG}-pooling-set-final.json")))
wid = json.load(open(GS("wid_doi_map.json")))
pri = {r["paperId"]: clean_doi(r.get("corrected_doi") or r.get("ondisk_doi"))
       for r in json.load(open(GS("prioritized_doi_corrected.json")))}
tmap = {}
for r in json.load(open(GS("tier_a_draft.json"))):
    if r.get("doi"): tmap.setdefault(norm(r["title"]), clean_doi(r["doi"]))
for r in json.load(open(GS("canon_resolved.json"))):
    if r.get("final_doi"): tmap.setdefault(norm(r["title"]), clean_doi(r["final_doi"]))

# abstract/year/author index (for the dedup author/year gate + Crossref year check)
absidx = {}
import glob
for f in glob.glob(rp("temp", "screen", "batch_*.json")):
    for r in json.load(open(f)):
        absidx[r["paperId"]] = r

# ---- Crossref (guarded, cached) ----
CACHE = GS("crossref_resolve_cache.json")
cache = json.load(open(CACHE)) if os.path.exists(CACHE) else {}
def crossref_doi(title, year):
    if title in cache:
        items = cache[title]
    else:
        try:
            out = subprocess.run(
                ["curl", "-s", "-m", "30",
                 f"https://api.crossref.org/works?query.bibliographic={quote(title, safe='')}"
                 f"&rows=5&mailto={MAILTO}"],
                capture_output=True, text=True).stdout
            items = [{"doi": clean_doi(it.get("DOI")),
                      "title": (it.get("title") or [""])[0],
                      "year": ((it.get("issued", {}).get("date-parts") or [[None]])[0] or [None])[0]}
                     for it in json.loads(out)["message"]["items"]]
        except Exception:
            items = []
        cache[title] = items
    # C2 guard: best title-Jaccard >= 0.80 AND year within 1 (if both known)
    best = None
    for it in items:
        j = jacc(title, it["title"])
        if j >= 0.80 and (not year or not it["year"] or abs(int(year) - int(it["year"])) <= 1):
            if not best or j > best[1]:
                best = (it["doi"], j)
    return best  # (doi, jaccard) or None

# ---- resolve ----
for r in pool:
    i, t = r["paperId"], r["title"]
    yr = absidx.get(i, {}).get("year")
    doi, src = None, None
    if wid.get(i):                      doi, src = clean_doi(wid[i]), "wid_doi_map"
    elif pri.get(i):                    doi, src = pri[i], "prioritized_corrected"
    elif tmap.get(norm(t)):             doi, src = tmap[norm(t)], "title_map"
    else:
        hit = crossref_doi(t, yr)
        if hit:                         doi, src = hit[0], f"crossref(J={hit[1]:.2f})"
    r["doi"] = doi
    r["resolve_source"] = src or "UNRESOLVED"
json.dump(cache, open(CACHE, "w"), ensure_ascii=False, indent=1)

# ---- study-level dedup (26c logic: DOI key, then title+author/year) ----
def auth_key(i):
    a = (absidx.get(i, {}).get("authors") or "")
    m = re.findall(r"[A-Za-z]{3,}", a)
    return m[0].lower() if m else ""

groups = {}   # key -> list of records
for r in pool:
    if r["doi"]:
        key = ("doi", r["doi"])
    else:
        key = ("tk", norm(r["title"])[:40] or r["paperId"])
    groups.setdefault(key, []).append(r)

# second pass: merge title-keyed records that share author+year+title-containment
tk = [g for k, g in groups.items() if k[0] == "tk"]
merged = 0
for i in range(len(tk)):
    for j in range(i + 1, len(tk)):
        if not tk[i] or not tk[j]:
            continue
        a, b = tk[i][0], tk[j][0]
        na, nb = norm(a["title"]), norm(b["title"])
        if (na and nb and (na in nb or nb in na)
                and auth_key(a["paperId"]) == auth_key(b["paperId"]) and auth_key(a["paperId"])):
            tk[i].extend(tk[j]); tk[j].clear(); merged += 1

distinct = []
for k, g in groups.items():
    g = [r for r in g if r]          # drop records cleared by the tk merge pass
    if not g:
        continue
    head = g[0]
    distinct.append(dict(head, dup_wids=[x["paperId"] for x in g[1:]], n_variants=len(g)))

# ---- outputs ----
resolved = sum(1 for r in pool if r["doi"])
by_src = {}
for r in pool:
    by_src[r["resolve_source"].split("(")[0]] = by_src.get(r["resolve_source"].split("(")[0], 0) + 1

json.dump(distinct, open(rp("output", f"{SLUG}-fine-resolved.json"), "w"),
          ensure_ascii=False, indent=1)

lines = [f"# Fine filter · step 53 — DOI resolution + study dedup ({SLUG})", "",
         f"Input: {len(pool)} RA-confirmed studies → **{len(distinct)} distinct** after dedup "
         f"({len(pool)-len(distinct)} variant(s) merged).", "",
         f"**DOI resolved: {resolved}/{len(pool)}** · title-keyed (no DOI): {len(pool)-resolved}", "",
         "| source | n |", "|---|---|"]
for s, n in sorted(by_src.items(), key=lambda x: -x[1]):
    lines.append(f"| {s} | {n} |")
unres = [r for r in pool if not r["doi"]]
if unres:
    lines += ["", "## Still title-keyed (need manual/live resolution)", ""]
    for r in unres:
        lines.append(f"- {(r['title'] or '')[:75]}" + ("  ·gold" if r["is_gold"] else ""))
open(rp("output", f"{SLUG}-fine-resolved.md"), "w").write("\n".join(lines) + "\n")

print(f"resolved {resolved}/{len(pool)} DOIs; {len(distinct)} distinct studies "
      f"({len(pool)-len(distinct)} merged)")
print("by source:", by_src)
print(f"still title-keyed: {len(unres)}")
print(f"wrote output/{SLUG}-fine-resolved.json / .md")
