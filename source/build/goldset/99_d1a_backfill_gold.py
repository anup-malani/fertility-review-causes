#!/usr/bin/env python3
"""
99_d1a_backfill_gold.py — repair two data-quality defects in the Tier-B frame before it is frozen.

Both were found by inspecting the assembled frame rather than by the assembly reporting them, which is
the same lesson this chapter keeps relearning: a count of 495 records says nothing about whether the
495 are usable.

DEFECT 1 — 27 of 495 "titles" are entire citation strings, not titles. Crossref reference lists carry
an `unstructured` field when the publisher deposited a formatted reference instead of structured
metadata, and `93_`/`96_` fall back to it. So the frame contains rows like

    "Jeffery, P., & Jeffery, R. (2000). Religion and fertility in India. Economic and Political
     Weekly, 35(35), 3253-3259."

filed as a title. This matters twice over. Term mining in A4 runs on titles, so every author surname,
journal name and page range in these strings enters the candidate vocabulary as if it were subject
matter. And the recall probe matches the production query against titles, so these records would fail
to match for reasons having nothing to do with the query's quality -- understating recall, which is
the conservative direction but is noise rather than conservatism.

DEFECT 2 — abstracts reached only 178 of 495 (36%). S2 does not hold an abstract for much of this
literature. A4 mines titles only, following D.3.b, so this does not block the next stage; it binds at
A6c, where the title-only versus title-and-abstract operationalisation is chosen on measured recall
and cannot be chosen honestly on 36% coverage.

BOTH REPAIRS RUN THROUGH CROSSREF, which holds structured metadata for records S2 does not index and
deposits JATS abstracts for a good share of this literature. All 27 citation strings are among the 110
records with no DOI, so recovering DOIs by bibliographic query fixes both problems at once.

THE MATCHING GUARD IS THE POINT OF THE SCRIPT, NOT AN ASIDE. Resolving a citation string to a DOI is
exactly the operation that manufactures ghosts if it is done loosely: "Religion and fertility" is
contained in dozens of distinct citation strings in this frame, belonging to different authors in
different decades. Matching therefore requires containment of the recovered title inside the source
string AND at least four content tokens AND an agreeing year wherever the citation string carries one
(see `d1a_titles.containment_match`). A record that fails the guard KEEPS ITS ORIGINAL STRING and is
flagged -- never dropped, never assigned a plausible-looking DOI. A3's resolution rule is that an
unresolvable record stays in the denominator keyed on title, because dropping it biases recall toward
easy-to-find papers.

Output: rewrites literature/search-logs/{slug}-tier-b-frame.json in place (idempotent, cached)
        literature/search-logs/{slug}-tier-b-backfill.md
"""
import html, json, os, re, sys, urllib.parse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from d1a_fetch import Fetcher, is_not_found  # noqa: E402
from d1a_titles import containment_match, jaccard  # noqa: E402

SLUG = "postmaterialism-individualism-secularization"
MAILTO = "shravanh@uchicago.edu"
UA = f"fertility-review/1.0 (mailto:{MAILTO})"
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
LOGS = os.path.join(ROOT, "literature", "search-logs")
FRAME = os.path.join(LOGS, f"{SLUG}-tier-b-frame.json")
OUT_MD = os.path.join(LOGS, f"{SLUG}-tier-b-backfill.md")
FETCH = Fetcher(os.path.join(HERE, "d1a_enrich_cache.json"), UA)

CIT_STRING = re.compile(r"^[A-Z][a-z]+,\s*[A-Z]\.|\(\d{4}\)\.|\d{4}\)\.|\bpp\.\s*\d|\bvol\.\s*\d|doi:",
                        re.I)


def strip_jats(a):
    """Crossref abstracts are JATS XML fragments. Return plain text, or None if nothing survives."""
    if not a:
        return None
    t = re.sub(r"<[^>]+>", " ", a)
    t = html.unescape(t)
    t = re.sub(r"\s+", " ", t).strip()
    t = re.sub(r"^(abstract|summary)\b[:.\s]*", "", t, flags=re.I).strip()
    return t or None


def cr_by_doi(doi):
    d = FETCH.get(f"https://api.crossref.org/works/{urllib.parse.quote(doi)}?mailto={MAILTO}")
    if not d or is_not_found(d) or "message" not in d:
        return None
    return d["message"]


def cr_bibliographic(s):
    url = "https://api.crossref.org/works?" + urllib.parse.urlencode(
        {"query.bibliographic": s[:400], "rows": 5, "mailto": MAILTO,
         "select": "DOI,title,issued,author,container-title,abstract,is-referenced-by-count"})
    d = FETCH.get(url)
    if not d or is_not_found(d):
        return []
    return ((d.get("message") or {}).get("items")) or []


def year_of(item):
    parts = ((item.get("issued") or {}).get("date-parts") or [[None]])[0]
    return parts[0] if parts else None


def main():
    frame = json.load(open(FRAME))
    recovered, abstracts_added, refused = [], 0, []

    # ---- pass 1: records with no DOI, resolved by bibliographic query -----------------------
    nodoi = [r for r in frame if not r.get("doi")]
    print(f"pass 1: {len(nodoi)} records without a DOI", file=sys.stderr)
    for i, r in enumerate(nodoi, 1):
        src = r["title"] or ""
        if not src.strip():
            continue
        best = None
        for item in cr_bibliographic(src):
            cand = (item.get("title") or [""])[0]
            ok, c, why = containment_match(cand, src, cand_year=year_of(item))
            if ok and (best is None or c > best[1]):
                best = (item, c, cand, why)
        if best is None:
            refused.append({"title": src[:140], "reason": "no Crossref candidate cleared the guard"})
            continue
        item, c, cand, why = best
        r["doi"] = (item.get("DOI") or "").lower() or None
        r["_recovered_title_from"] = src[:200] if CIT_STRING.search(src) else None
        r["title"] = cand
        r["year"] = r.get("year") or year_of(item)
        r["venue"] = r.get("venue") or (item.get("container-title") or [""])[0]
        r["authors"] = r.get("authors") or "; ".join(
            f"{a.get('given', '')} {a.get('family', '')}".strip() for a in (item.get("author") or []))
        r["cited_by_count"] = r.get("cited_by_count") or item.get("is-referenced-by-count")
        r["resolution"] = "CROSSREF_RECOVERED"
        if not r.get("abstract"):
            ab = strip_jats(item.get("abstract"))
            if ab:
                r["abstract"] = ab
                abstracts_added += 1
        recovered.append({"title": cand[:110], "doi": r["doi"], "containment": round(c, 2),
                          "why": why, "was_citation_string": bool(r.get("_recovered_title_from"))})
        if i % 25 == 0:
            print(f"  {i}/{len(nodoi)} — {len(recovered)} recovered", file=sys.stderr)
            FETCH.save()
    FETCH.save()

    # ---- pass 2: abstracts for everything with a DOI and no abstract ------------------------
    need = [r for r in frame if r.get("doi") and not r.get("abstract")]
    print(f"pass 2: {len(need)} records need an abstract", file=sys.stderr)
    for i, r in enumerate(need, 1):
        m = cr_by_doi(r["doi"])
        if not m:
            continue
        ab = strip_jats(m.get("abstract"))
        if ab:
            r["abstract"] = ab
            abstracts_added += 1
        if i % 50 == 0:
            print(f"  {i}/{len(need)} — {abstracts_added} abstracts added so far", file=sys.stderr)
            FETCH.save()
    FETCH.save()

    json.dump(frame, open(FRAME, "w"), indent=1)

    still_cit = [r for r in frame if CIT_STRING.search(r["title"] or "")]
    with_ab = sum(1 for r in frame if r.get("abstract"))
    with_doi = sum(1 for r in frame if r.get("doi"))
    L = ["# D.1.a — Tier-B frame backfill", "",
         "Run by `99_d1a_backfill_gold.py` against Crossref, repairing two defects found by "
         "inspecting the assembled frame rather than reported by the assembly.", "",
         "| | before | after |", "|---|---|---|",
         f"| records with a DOI | 385 | **{with_doi}** |",
         f"| records with an abstract | 178 (36%) | **{with_ab} ({100 * with_ab // len(frame)}%)** |",
         f"| titles that are really citation strings | 27 | **{len(still_cit)}** |", "",
         f"- DOIs recovered by bibliographic query: **{len(recovered)}** of "
         f"{len(nodoi)} attempted",
         f"- of those, citation strings replaced with the real title: "
         f"**{sum(1 for x in recovered if x['was_citation_string'])}**",
         f"- abstracts added: **{abstracts_added}**",
         f"- refused by the matching guard, kept title-keyed: **{len(refused)}**", "",
         "Records the guard refused are **kept in the frame and in the recall denominator**, keyed on "
         "their original string. Dropping them would bias recall toward easy-to-find papers, and "
         "assigning them a best-guess DOI is how the OAS run acquired a 40%-ghost Tier B.", ""]
    if refused:
        L += ["## Refused by the guard (sample of 15)", ""]
        L += [f"- {x['title']}  — `{x['reason']}`" for x in refused[:15]] + [""]
    if recovered:
        L += ["## Recovered (sample of 15)", ""]
        L += [f"- {x['title']}  → `{x['doi']}` (containment {x['containment']}, {x['why']})"
              for x in recovered[:15]] + [""]
    open(OUT_MD, "w").write("\n".join(L) + "\n")
    print("\n".join(L[4:20]), file=sys.stderr)
    print(f"\nwrote {FRAME}\nwrote {OUT_MD}", file=sys.stderr)


if __name__ == "__main__":
    main()
