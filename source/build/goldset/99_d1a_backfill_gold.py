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
    # Captured, not hardcoded: this script is idempotent and re-runs must report the real baseline.
    b0 = {"n": len(frame), "doi": sum(1 for r in frame if r.get("doi")),
          "abs": sum(1 for r in frame if r.get("abstract")),
          "cit": sum(1 for r in frame if CIT_STRING.search(r.get("title") or ""))}

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

    # ---- pass 3: re-deduplicate AFTER enrichment ---------------------------------------------
    # DEFECT 3, and it is an ordering bug rather than a data one. `98_` deduplicates on the RAW
    # snowball title and then enrichment rewrites titles to the provider's canonical form, so two
    # records that were distinct strings before enrichment become the same work after it. The frame
    # carried 95 such pairs: "Religion and fertility: the French connection" against "...The French
    # connection", "Postmodern fertility preferences: from changing value orientation to new
    # behaviour" against the American spelling, and a book indexed once with and once without its
    # "by Philip Jenkins" suffix.
    #
    # It inflates everything computed downstream of the frame -- the Tier-B count, the A6a positive
    # class, and the A6b recall denominator -- and it inflates the round-2 saturation yield, because
    # a duplicate counts as a new relevant record. Deduplicating post-enrichment is the only place
    # this can be caught: before enrichment the two strings genuinely differ.
    #
    # Provenance is MERGED rather than discarded. A record reached from two seeds is evidence about
    # the frame's connectivity, and dropping the second copy's `seen_from` would understate it.
    by_key, order = {}, []
    for r in frame:
        k = re.sub(r"\s+", " ", re.sub(r"[^a-z0-9\s]", " ", (r.get("title") or "").lower())).strip()
        if not k:
            k = f"__notitle__{len(order)}"
        if k in by_key:
            keep = by_key[k]
            keep["seen_from"] = sorted(set((keep.get("seen_from") or [])
                                           + (r.get("seen_from") or [])))
            keep["duplicate_titles"] = sorted(set(keep.get("duplicate_titles", [])
                                                  + [r.get("title")]) - {keep.get("title")})
            # Prefer the copy that actually resolved, and the richer record where both did.
            if keep["resolution"] == "TITLE_KEYED_UNRESOLVED" and r["resolution"] != keep["resolution"]:
                r["seen_from"], r["duplicate_titles"] = keep["seen_from"], keep["duplicate_titles"]
                by_key[k] = r
            elif not keep.get("abstract") and r.get("abstract"):
                keep["abstract"] = r["abstract"]
            if not keep.get("doi") and r.get("doi"):
                keep["doi"] = r["doi"]
            continue
        by_key[k] = r
        order.append(k)
    n_before = len(frame)
    frame = [by_key[k] for k in order]
    n_dupes = n_before - len(frame)
    print(f"pass 3: post-enrichment dedup removed {n_dupes} duplicate works "
          f"({n_before} -> {len(frame)})", file=sys.stderr)

    json.dump(frame, open(FRAME, "w"), indent=1)

    still_cit = [r for r in frame if CIT_STRING.search(r["title"] or "")]
    with_ab = sum(1 for r in frame if r.get("abstract"))
    with_doi = sum(1 for r in frame if r.get("doi"))
    L = ["# D.1.a — Tier-B frame backfill", "",
         "Run by `99_d1a_backfill_gold.py` against Crossref, repairing two defects found by "
         "inspecting the assembled frame rather than reported by the assembly.", "",
         "| | before | after |", "|---|---|---|",
         f"| records with a DOI | {b0['doi']} | **{with_doi}** |",
         f"| records with an abstract | {b0['abs']} ({100 * b0['abs'] // b0['n']}%) | "
         f"**{with_ab} ({100 * with_ab // len(frame)}%)** |",
         f"| titles that are really citation strings | {b0['cit']} | **{len(still_cit)}** |",
         f"| distinct works after post-enrichment dedup | {b0['n']} | **{len(frame)}** |", "",
         f"- duplicate works removed by pass 3: **{n_dupes}** — enrichment rewrites titles to the "
         f"provider's canonical form, so records that were distinct strings when `98_` deduplicated "
         f"become the same work afterwards. This inflated the Tier-B count, the A6a positive class, "
         f"the A6b recall denominator, and the round-2 saturation yield.",
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

    # `98_` rewrites the tier-A/B log from scratch on every run, so the frozen post-backfill numbers
    # have to be appended HERE or they vanish the next time 98 is run. Same binding-order point as the
    # frame itself: 98 then 99, and 99 owns the final state of both artifacts.
    ab_log = os.path.join(LOGS, f"{SLUG}-tier-ab-log.md")
    if os.path.exists(ab_log):
        with open(ab_log, "a") as fh:
            fh.write(
                "\n---\n\n## Post-backfill state (the frozen numbers)\n\n"
                f"Appended by `99_d1a_backfill_gold.py`. **Run order `98_` then `99_` is binding** — "
                f"98 rewrites this file and the frame from scratch, so 98 alone reverts everything "
                f"below. Both are cached and idempotent.\n\n"
                f"| Tier B | at assembly | frozen |\n|---|---|---|\n"
                f"| records | {b0['n']} | **{len(frame)}** |\n"
                f"| with a DOI | {b0['doi']} | **{with_doi}** |\n"
                f"| with an abstract | {b0['abs']} | **{with_ab}** "
                f"({100 * with_ab // len(frame)}%) |\n"
                f"| titles that are really citation strings | {b0['cit']} | **{len(still_cit)}** |\n\n"
                f"**{n_dupes} duplicate works removed post-enrichment.** `98_` deduplicates on the raw "
                f"snowball title and enrichment then rewrites titles to the provider's canonical form, "
                f"so records that were distinct strings at dedup time become the same work afterwards "
                f"— case variants, British against American spelling, and a book indexed once with and "
                f"once without its author suffix. This inflated the Tier-B count, the A6a positive "
                f"class, the A6b recall denominator, and the round-2 saturation yield. It can only be "
                f"caught after enrichment, because before it the two strings genuinely differ.\n\n"
                f"**{len(refused)} of {len(nodoi)} no-DOI records were refused by the resolution "
                f"guard and are kept**, keyed on their original string, because dropping them biases "
                f"recall toward easy-to-find papers. A hand read shows the residue is book chapters, "
                f"regional and non-English journals, dissertations and conference papers that Crossref "
                f"does not hold — the fourth appearance of the same indexing gap on this chapter. The "
                f"threshold is calibrated rather than merely strict: one refusal at containment 0.78 "
                f"was a different study with an almost identical title, so relaxing the bar to lift "
                f"the recovery rate would have assigned a wrong DOI.\n")
    print("\n".join(L[4:20]), file=sys.stderr)
    print(f"\nwrote {FRAME}\nwrote {OUT_MD}", file=sys.stderr)


if __name__ == "__main__":
    main()
