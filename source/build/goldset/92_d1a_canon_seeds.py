#!/usr/bin/env python3
"""
92_d1a_canon_seeds.py — D.1.a, GACS channel 2. Resolve the theory canon, and audit the v5 seminal field.

Two jobs in one pass.

JOB 1 — supply the missing snowball seeds. The channel-1/2 seeds available after 91 are six records
and they are unbalanced: four are SDT-framework statements, two are regional sub-Saharan Africa
reviews, and the values-psychology vocabulary family (Inglehart, Schwartz) has NO seed at all. The
scope predicted four barely-overlapping vocabulary families, and a snowball seeded from one of them
reaches one of them. C.2.c hit this exact failure at round 1 -- "the seed set is unbalanced (3
econ-price, 1 macro-comparative, ZERO demog-tenure)" -- and had to spend a whole round fixing it.
Fixing it before round 1 here instead.

Seeds resolved by TITLE SEARCH against OpenAlex, which is GACS channel 2 (top-down canon enumeration
with the title-matching guard), NOT channel 4. The distinction is load-bearing for Tier-B integrity:
a canon work named from the theory literature and then resolved is not a paper the production query
produced, so it does not make Recall(B) circular.

JOB 2 — audit the v5 `seminal` field. The scope records that the eight works named there are
"candidates to verify, not anchors," under the standing rule from the 2026-07-08 run. This resolves
each one and reports what is real, what is mis-cited, and what cannot be found. The D.3.b run found
the v5 seminal list carried a ghost ("Britt et al. 2025 (Genus)" did not exist; the real paper was
Puglisi/Muttarak/Vignoli), so the field has a demonstrated error rate and is checked rather than
trusted.

NOTHING here asserts a DOI. Each entry carries a title and author string taken from HYPOTHESES-v5.md
and is resolved live; a title that resolves to nothing is reported as UNRESOLVED, not invented.

Output: temp/d1a/canon-seeds.json
        literature/search-logs/{slug}-canon-seed-resolution.md
"""
import json, os, re, subprocess, sys, time, urllib.parse

SLUG = "postmaterialism-individualism-secularization"
MAILTO = "shravanh@uchicago.edu"
UA = f"fertility-review/1.0 (mailto:{MAILTO})"
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
LOGS = os.path.join(ROOT, "literature", "search-logs")
TMP = os.path.join(ROOT, "temp", "d1a")
os.makedirs(TMP, exist_ok=True)
OUT_JSON = os.path.join(TMP, "canon-seeds.json")
OUT_MD = os.path.join(LOGS, f"{SLUG}-canon-seed-resolution.md")

JACCARD_MIN = 0.55   # looser than the 0.72 identity gate: canonical books get retitled by indexers
YEAR_TOL = 2         # book editions and reprints drift

# (label, search title, expected first author, expected year, family, from_v5_seminal)
CANON = [
    # --- the v5 `seminal` field for D.1.a, verbatim from HYPOTHESES-v5.md, all to be verified ---
    ("Lesthaeghe 1983", "A century of demographic and cultural change in Western Europe",
     "Lesthaeghe", 1983, "demography-SDT", True),
    ("van de Kaa 1987", "Europe's second demographic transition", "van de Kaa", 1987,
     "demography-SDT", True),
    ("Lesthaeghe and van de Kaa 1986", "Twee demografische transities", "Lesthaeghe", 1986,
     "demography-SDT", True),
    ("Lesthaeghe and Surkyn 1988", "Cultural dynamics and economic theories of fertility change",
     "Lesthaeghe", 1988, "demography-SDT", True),
    ("Inglehart 1977", "The silent revolution: changing values and political styles among Western publics",
     "Inglehart", 1977, "values-psychology", True),
    ("Norris and Inglehart 2004", "Sacred and secular: religion and politics worldwide",
     "Norris", 2004, "values-psychology", True),
    ("Frejka and Westoff 2008", "Religion, religiousness and fertility in the US and in Europe",
     "Frejka", 2008, "sociology-of-religion", True),
    ("Hagestad and Call 2007", "Pathways to childlessness: a life course perspective",
     "Hagestad", 2007, "sociology-of-religion", True),

    # --- additional channel-2 canon, named from the theory literature to cover the missing families ---
    ("Inglehart 1997", "Modernization and postmodernization: cultural, economic, and political change in 43 societies",
     "Inglehart", 1997, "values-psychology", False),
    ("Inglehart and Baker 2000", "Modernization, cultural change, and the persistence of traditional values",
     "Inglehart", 2000, "values-psychology", False),
    ("Schwartz 1992", "Universals in the content and structure of values",
     "Schwartz", 1992, "values-psychology", False),
    ("Hofstede 1980", "Culture's consequences: international differences in work-related values",
     "Hofstede", 1980, "values-psychology", False),
    ("Alesina and Giuliano 2015", "Culture and institutions", "Alesina", 2015, "econ-of-culture", False),
    ("Enke 2019", "Kinship, cooperation, and the evolution of moral systems", "Enke", 2019,
     "econ-of-culture", False),
    ("Voas 2009", "The rise and fall of fuzzy fidelity in Europe", "Voas", 2009,
     "sociology-of-religion", False),
    ("McQuillan 2004", "When does religion influence fertility?", "McQuillan", 2004,
     "sociology-of-religion", False),
]


def norm(t):
    return set(re.findall(r"[a-z0-9]+", re.sub(r"<[^>]+>", " ", (t or "").lower())))


def jac(a, b):
    A, B = norm(a), norm(b)
    return len(A & B) / len(A | B) if A and B else 0.0


def search(title, per=8):
    url = "https://api.openalex.org/works?" + urllib.parse.urlencode(
        {"filter": f"title.search:{title}", "per-page": per,
         "sort": "cited_by_count:desc", "mailto": MAILTO})
    for _ in range(3):
        out = subprocess.run(["curl", "-s", "-m", "45", "-A", UA, url], capture_output=True, text=True)
        if out.returncode == 0 and out.stdout.strip().startswith("{"):
            try:
                d = json.loads(out.stdout)
            except Exception:  # noqa: BLE001
                break
            if "results" in d:
                return d["results"]
        time.sleep(2)
    return None


def main():
    rows = []
    for label, title, author, year, family, from_v5 in CANON:
        res = search(title)
        if res is None:
            rows.append(dict(label=label, family=family, from_v5_seminal=from_v5,
                             status="UNCONFIRMED", note="OpenAlex did not answer"))
            print(f"{label:32s} UNCONFIRMED", file=sys.stderr)
            continue
        best, bestj = None, 0.0
        for w in res:
            j = jac(title, w.get("title"))
            if j > bestj:
                best, bestj = w, j
        if best is None or bestj < JACCARD_MIN:
            rows.append(dict(label=label, family=family, from_v5_seminal=from_v5,
                             status="UNRESOLVED", best_title=(best or {}).get("title"),
                             jaccard=round(bestj, 2),
                             note="no title match above threshold -- do NOT invent an identifier"))
            print(f"{label:32s} UNRESOLVED (best J={bestj:.2f})", file=sys.stderr)
            continue
        auths = [a["author"]["display_name"] for a in (best.get("authorships") or [])]
        y = best.get("publication_year")
        author_ok = any(author.lower().split()[-1] in a.lower() for a in auths) if auths else None
        year_ok = (y is not None and abs(y - year) <= YEAR_TOL)
        st = "RESOLVED" if (author_ok and year_ok) else "RESOLVED_DISCREPANT"
        s = (best.get("primary_location") or {}).get("source") or {}
        rows.append(dict(label=label, family=family, from_v5_seminal=from_v5, status=st,
                         work_id=(best.get("id") or "").rsplit("/", 1)[-1],
                         doi=(best.get("doi") or "").replace("https://doi.org/", ""),
                         resolved_title=best.get("title"), resolved_year=y,
                         resolved_authors=auths[:5], venue=s.get("display_name") or "",
                         cited_by=best.get("cited_by_count"), jaccard=round(bestj, 2),
                         author_match=author_ok, year_match=year_ok,
                         expected_year=year))
        print(f"{label:32s} {st:20s} J={bestj:.2f} y={y} c={best.get('cited_by_count')}",
              file=sys.stderr)
        time.sleep(0.4)

    json.dump({"slug": SLUG, "rows": rows}, open(OUT_JSON, "w"), indent=1)

    v5 = [r for r in rows if r["from_v5_seminal"]]
    bad = [r for r in v5 if r["status"] not in ("RESOLVED",)]
    L = ["# D.1.a — channel-2 canon seed resolution, and the v5 `seminal` field audit", "",
         f"Run 2026-08-03 by `92_d1a_canon_seeds.py`. Title-matched live against OpenAlex "
         f"(Jaccard >= {JACCARD_MIN}, year within +/-{YEAR_TOL}).", "",
         f"- v5 seminal names checked: **{len(v5)}**; clean: **{len(v5) - len(bad)}**; "
         f"discrepant or unresolved: **{len(bad)}**",
         f"- additional channel-2 canon resolved for the under-seeded vocabulary families: "
         f"**{len([r for r in rows if not r['from_v5_seminal'] and r['status'].startswith('RESOLVED')])}**",
         "",
         "| status | label | v5? | family | resolved title | year | cites | id |",
         "|---|---|---|---|---|---|---|---|"]
    for r in rows:
        t = (r.get("resolved_title") or r.get("best_title") or "—")[:58].replace("|", "/")
        L.append(f"| {r['status']} | {r['label']} | {'yes' if r['from_v5_seminal'] else ''} | "
                 f"{r['family']} | {t} | {r.get('resolved_year', '')} | {r.get('cited_by', '')} | "
                 f"`{r.get('work_id', '')}` |")
    open(OUT_MD, "w").write("\n".join(L))
    print(f"\nwrote {OUT_JSON}\nwrote {OUT_MD}", file=sys.stderr)


if __name__ == "__main__":
    main()
