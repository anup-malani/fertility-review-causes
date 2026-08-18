#!/usr/bin/env python3
"""
147_d3c_recon_probe.py — D.3.c (despair and hopelessness), pre-scope reconnaissance.

Runs before the scope document. Establishes from live records rather than from memory:
  (a) whether the PRIMARY estimand cell exists at all — a *measured* despair/hopelessness/
      no-future construct on the right-hand side and a fertility quantity on the left. This is the
      cell the hypothesis is named for, and the probe's job is to find out whether it is populated
      or whether the chapter will rest entirely on reduced-form place-based decline studies whose
      mechanism is asserted rather than measured;
  (b) the size of the decoy clouds. D.3.c shares its entire vocabulary with the deaths-of-despair
      MORTALITY literature, which estimates no fertility quantity at all, and with two well-populated
      siblings — C.5.a (economic uncertainty and unemployment) and D.3.a (clinical depression);
  (c) whether the reduced-form body (mass layoffs, the China shock, coal and manufacturing decline)
      is separable at title/abstract from C.5.a. It is the Wall 1 question and the chapter's central
      routing problem;
  (d) whether the OPPOSITE-SIGN literature is real and how large it is. A collapse of forward
      orientation is also the standard explanation for *early* nonmarital childbearing — nothing to
      lose, children as an available source of meaning. If that body exists, D.3.c's sign is not
      given by its own theory and the chapter cannot assume one;
  (e) whether an exposure series exists to run demographic significance against, and how the timing
      of the despair rise sits against the timing of the fertility decline;
  (f) how the works v5 lists as seminal resolve. One of the three is cited to a press release.

Discipline carried from prior runs (B.5, B.6, B.7, D.2.d, D.3.b):
  * A failed request goes in an ERROR bucket kept SEPARATE from a genuine zero-hit, and the report
    refuses to publish if the error share exceeds ERROR_ABORT_SHARE. A wrong zero would propagate
    into the scope document as "this literature does not exist".
  * HTTPS goes through curl: the interpreter on this machine has no CA bundle, so urllib fails every
    call, and it fails as a *transport* error, i.e. as a fake zero.
  * OpenAlex is called with the funded api_key from .env, never with mailto alone.
  * Named-title probes run in two passes. A zero on `title.search` means the remembered wording is
    wrong; only an empty GROUP probe means a literature is absent.

Output: literature/search-logs/despair-hopelessness-fertility-recon-probe.md
"""
import json, os, subprocess, sys, time

SLUG = "despair-hopelessness-fertility"
MAILTO = "shravanh@uchicago.edu"
UA = f"fertility-review/1.0 (mailto:{MAILTO})"
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
OUT_MD = os.path.join(ROOT, "literature", "search-logs", f"{SLUG}-recon-probe.md")
ERROR_ABORT_SHARE = 0.20
PER_PAGE = 8


def openalex_key():
    """Read the funded key from the environment, then from .env. Never log or cache the value."""
    k = os.environ.get("OPENALEX_API_KEY")
    if k:
        return k.strip()
    envp = os.path.join(ROOT, ".env")
    if os.path.exists(envp):
        for line in open(envp):
            if line.startswith("OPENALEX_API_KEY="):
                return line.split("=", 1)[1].strip()
    return ""


KEY = openalex_key()

# Vocabulary blocks. Kept as named constants because the walls are vocabulary tests and the wording
# has to be identical in the probe and in the scope document that quotes its counts.
DESPAIR = '("despair" OR "hopelessness" OR "hopeless" OR "demoralization" OR "anomie" OR "fatalism" OR "fatalistic")'
FUTURE = '("future orientation" OR "sense of the future" OR "foreshortened future" OR "expectations about the future" OR "optimism about the future" OR "pessimism about the future")'
DECLINE = '("deindustrialization" OR "economic decline" OR "left behind" OR "distressed communities" OR "plant closure" OR "mass layoff" OR "job loss" OR "China shock" OR "import competition" OR "coal" OR "Rust Belt")'
FERT = '("fertility" OR "birth rate" OR "birth rates" OR "childbearing" OR "fertility intentions" OR "childlessness" OR "total fertility rate")'
MORT = '("mortality" OR "suicide" OR "overdose" OR "drug poisoning" OR "alcoholic liver disease" OR "life expectancy")'
DEPRESS = '("depression" OR "depressive symptoms" OR "major depressive disorder" OR "anxiety")'
UNCERT = '("economic uncertainty" OR "employment uncertainty" OR "job insecurity" OR "unemployment")'
MARRIAGE = '("marriage" OR "union formation" OR "marriage rates" OR "cohabitation" OR "marriageable")'

GROUPS = [
    ("The PRIMARY cell — a measured despair construct on a fertility outcome", [
        ("despair/hopelessness AND fertility", f'title_and_abstract.search:{DESPAIR} AND {FERT}'),
        ("despair/hopelessness AND fertility intentions specifically", f'title_and_abstract.search:{DESPAIR} AND ("fertility intentions" OR "childbearing intentions" OR "desire for children" OR "reproductive intentions")'),
        ("future orientation / foreshortened future AND fertility", f'title_and_abstract.search:{FUTURE} AND {FERT}'),
        ("deaths of despair framing AND fertility", 'title_and_abstract.search:("deaths of despair" OR "despair") AND ("fertility" OR "birth rate" OR "births")'),
        ("hopelessness scale / Beck hopelessness AND reproduction", 'title_and_abstract.search:("hopelessness scale" OR "Beck Hopelessness") AND ("fertility" OR "childbearing" OR "pregnancy" OR "reproductive")'),
    ]),
    ("Decoy cloud 1 — deaths of despair, whose outcome is mortality not fertility", [
        ("deaths of despair, all", 'title_and_abstract.search:"deaths of despair"'),
        ("deaths of despair AND mortality outcomes", f'title_and_abstract.search:"deaths of despair" AND {MORT}'),
        ("despair AND mortality, broader", f'title_and_abstract.search:{DESPAIR} AND {MORT}'),
        # NOTE: a quoted phrase whose FIRST WORD is `not` is parsed by OpenAlex as a boolean NOT, and
        # the enclosing AND then returns the UNRESTRICTED count rather than an error or a zero. The
        # earlier wording here contained "not deaths of despair" and reported 831 — the count of the
        # unrestricted probe above it — where the truth is 32. The failure inflates, so it reads as a
        # large literature. Never open a search phrase with not/and/or.
        ("deaths of despair — the contested-framework literature", 'title_and_abstract.search:("deaths of despair") AND ("critique" OR "reconsidered" OR "misleading" OR "evidence against" OR "reconsidering" OR "questioned")'),
    ]),
    ("Decoy cloud 2 — the reduced-form place-based decline body (the Wall 1 problem)", [
        ("economic decline / deindustrialization AND fertility", f'title_and_abstract.search:{DECLINE} AND {FERT}'),
        ("China shock / import competition AND fertility or marriage", f'title_and_abstract.search:("China shock" OR "import competition" OR "trade shock") AND ({FERT} OR {MARRIAGE})'),
        ("mass layoff / plant closure AND fertility", f'title_and_abstract.search:("mass layoff" OR "plant closure" OR "job displacement" OR "displaced workers") AND {FERT}'),
        ("Great Recession AND fertility (the transitory-shock comparison)", f'title_and_abstract.search:("Great Recession" OR "economic crisis" OR "recession") AND {FERT}'),
        ("does the decline body NAME a despair mechanism?", f'title_and_abstract.search:{DECLINE} AND {FERT} AND {DESPAIR}'),
    ]),
    ("Wall probes — the two siblings", [
        ("C.5.a sibling — economic uncertainty / unemployment AND fertility", f'title_and_abstract.search:{UNCERT} AND {FERT}'),
        ("C.5.a overlap — uncertainty AND fertility AND despair vocabulary", f'title_and_abstract.search:{UNCERT} AND {FERT} AND {DESPAIR}'),
        ("D.3.a sibling — depression / anxiety AND fertility", f'title_and_abstract.search:{DEPRESS} AND {FERT}'),
        ("D.3.a overlap — depression AND fertility AND despair vocabulary", f'title_and_abstract.search:{DEPRESS} AND {FERT} AND {DESPAIR}'),
        ("community-level vs individual — despair measured at place level", f'title_and_abstract.search:{DESPAIR} AND ("county" OR "community" OR "neighborhood" OR "place" OR "regional" OR "area-level") AND {FERT}'),
    ]),
    ("The OPPOSITE-SIGN literature — hopelessness raising early childbearing", [
        ("no-future orientation AND teen / early childbearing", f'title_and_abstract.search:({FUTURE} OR {DESPAIR}) AND ("teenage childbearing" OR "teen pregnancy" OR "adolescent childbearing" OR "early childbearing" OR "nonmarital childbearing")'),
        ("economic despair / hopelessness as a cause of teen births", 'title_and_abstract.search:("teen childbearing" OR "teenage pregnancy" OR "nonmarital fertility") AND ("hopelessness" OR "despair" OR "bleak" OR "no future" OR "limited opportunity" OR "economic marginalization")'),
        ("Kearney-Levine class — inequality, desperation and early fertility", 'title_and_abstract.search:("income inequality" OR "economic despair" OR "opportunity") AND ("early nonmarital childbearing" OR "teen childbearing" OR "teen birth")'),
        ("children as a source of meaning under constrained futures", 'title_and_abstract.search:("meaning" OR "identity" OR "purpose" OR "motherhood") AND ("poverty" OR "disadvantage" OR "marginalized") AND ("early motherhood" OR "young mothers" OR "teenage mothers")'),
        ("future discounting / time preference AND fertility timing", 'title_and_abstract.search:("time preference" OR "discount rate" OR "future discounting" OR "present bias") AND ("fertility" OR "childbearing" OR "teen birth")'),
    ]),
    ("The proximate channel — marriage and union formation", [
        ("economic decline AND marriageability / union formation", f'title_and_abstract.search:{DECLINE} AND {MARRIAGE}'),
        ("marriageable-men / Wilson hypothesis", 'title_and_abstract.search:("marriageable men" OR "marriage market" OR "male joblessness" OR "sex ratio") AND ("marriage rates" OR "nonmarital" OR "family formation")'),
        ("retreat from marriage in the working class", 'title_and_abstract.search:("retreat from marriage" OR "working class" OR "less educated" OR "non-college") AND ("marriage" OR "family formation") AND ("decline" OR "divergence" OR "diverging")'),
    ]),
    ("Reverse causation and confounding", [
        ("childlessness / infertility causing despair or distress", f'title_and_abstract.search:("childlessness" OR "childless" OR "infertility" OR "involuntary childlessness") AND ({DESPAIR} OR "distress" OR "wellbeing")'),
        ("selective out-migration from declining places", 'title_and_abstract.search:("out-migration" OR "selective migration" OR "brain drain" OR "population loss") AND ("declining" OR "distressed" OR "rural") AND ("fertility" OR "composition" OR "selection")'),
    ]),
    ("Exposure series and timing — what demographic significance would run on", [
        ("despair indicators — trends and geography", f'title_and_abstract.search:("deaths of despair" OR "drug overdose" OR "suicide rate") AND ("trend" OR "trends" OR "geography" OR "county-level" OR "spatial")'),
        ("subjective wellbeing / life satisfaction trends by place or class", 'title_and_abstract.search:("life satisfaction" OR "subjective wellbeing" OR "happiness") AND ("trend" OR "decline") AND ("United States" OR "county" OR "education gradient")'),
        ("US fertility decline post-2007 — the phenomenon to be explained", 'title_and_abstract.search:("fertility decline" OR "birth rates" OR "fertility rates") AND ("United States" OR "US" OR "American") AND ("post-recession" OR "since 2007" OR "puzzle" OR "unexplained")'),
        ("education / class gradient in the US fertility decline", 'title_and_abstract.search:("fertility" OR "birth rates") AND ("education gradient" OR "by education" OR "less educated" OR "socioeconomic gradient") AND ("United States" OR "decline")'),
    ]),
    ("Channel 1 — prior systematic reviews", [
        ("SR/meta — economic conditions AND fertility", f'title_and_abstract.search:("systematic review" OR "meta-analysis" OR "scoping review") AND ("economic" OR "unemployment" OR "recession") AND {FERT}'),
        ("SR/meta — despair or psychological distress AND fertility", f'title_and_abstract.search:("systematic review" OR "meta-analysis" OR "scoping review") AND ({DESPAIR} OR "psychological distress" OR "mental health") AND {FERT}'),
    ]),
]

# Named candidate works. Includes v5's own seminal list, which the probe is meant to test rather than
# accept: one of the three is cited to a press-release aggregator, which is the ghost-citation class.
NAMED = [
    # v5's seminal list, as written in HYPOTHESES-v5.md D.3.c
    "Deaths of Despair and the Future of Capitalism",
    "Platt Sterling despair fertility",
    "Labor's Love Lost The Rise and Fall of the Working-Class Family in America",
    # The deaths-of-despair canon
    "Rising morbidity and mortality in midlife among white non-Hispanic Americans",
    "Mortality and morbidity in the 21st century",
    # The contest over the framework
    "Deaths of despair or drug problems",
    # The reduced-form decline canon
    "When Work Disappears Manufacturing Decline and the Falling Marriage Market Value of Young Men",
    "The China Syndrome Local Labor Market Effects of Import Competition in the United States",
    # The opposite-sign canon
    "Promises I Can Keep Why Poor Women Put Motherhood before Marriage",
    "Income inequality and early nonmarital childbearing",
    # The phenomenon
    "The Puzzle of Falling US Birth Rates since the Great Recession",
]

NAMED_RETRY = [
    "Deaths of despair and the future of capitalism Case Deaton",
    "Hopelessness and fertility intentions",
    "Despair and fertility decline United States",
    "Economic despair and the decline in US births",
    "Understanding the decline in fertility in the United States",
    "Manufacturing decline marriage market value young men",
    "Trade adjustment worker level evidence",
    "Why poor women put motherhood before marriage",
    "Teen childbearing and economic despair",
    "The economics of nonmarital childbearing and the marriage premium for children",
    "Deindustrialization and family formation",
    "County-level deaths of despair and birth rates",
    "Subjective future expectations and fertility behavior",
    "Uncertainty and fertility a review",
]

errors, results, named_results, retry_results = [], [], [], []


def oa(url):
    try:
        r = subprocess.run(["curl", "-s", "-m", "45", "-A", UA, url], capture_output=True, text=True)
        if r.returncode != 0:
            return {"__err": f"curl exit {r.returncode}"}
        return json.loads(r.stdout)
    except Exception as e:
        return {"__err": str(e)[:140]}


def rows_of(d):
    out = []
    for w in d.get("results", []):
        loc = (w.get("primary_location") or {}).get("source") or {}
        out.append(dict(title=w.get("display_name") or "", year=w.get("publication_year"),
                        cites=w.get("cited_by_count"), type=w.get("type"),
                        venue=(loc.get("display_name") or ""),
                        doi=(w.get("doi") or "").replace("https://doi.org/", "")))
    return out


def probe(filt, per_page=PER_PAGE, sort="cited_by_count:desc"):
    url = ("https://api.openalex.org/works?filter=" + filt.replace(" ", "%20").replace('"', "%22") +
           f"&per-page={per_page}&select=id,doi,display_name,publication_year,cited_by_count,type,"
           f"primary_location&sort={sort}&api_key={KEY}")
    return oa(url)


def main():
    n_req = 0
    for group, probes in GROUPS:
        for label, filt in probes:
            n_req += 1
            d = probe(filt)
            if "results" not in d:
                errors.append((label, str(d.get("__err") or d)[:160]))
            else:
                results.append((group, label, filt, d["meta"]["count"], rows_of(d)))
            time.sleep(0.2)

    for lst, sink in ((NAMED, named_results), (NAMED_RETRY, retry_results)):
        for t in lst:
            n_req += 1
            url = ("https://api.openalex.org/works?filter=title.search:" + t.replace(" ", "%20") +
                   "&per-page=5&select=id,doi,display_name,publication_year,cited_by_count,type,"
                   "primary_location&api_key=" + KEY)
            d = oa(url)
            if "results" not in d:
                errors.append((t[:45], str(d.get("__err") or d)[:160]))
            else:
                sink.append((t, d["meta"]["count"], rows_of(d)))
            time.sleep(0.2)

    share = len(errors) / max(n_req, 1)
    if share > ERROR_ABORT_SHARE:
        sys.stderr.write(f"ABORT: {len(errors)}/{n_req} requests failed ({share:.0%}). "
                         "Zero-hit counts are not trustworthy; not writing the report.\n")
        for lbl, e in errors[:12]:
            sys.stderr.write(f"  {lbl}: {e}\n")
        sys.exit(1)

    L = []
    L.append(f"# Reconnaissance probe — {SLUG}\n")
    L.append("**Hypothesis:** D.3.c (HYPOTHESES-v5.md) · **Ticket:** TICK-069\n")
    L.append(f"**Generated by:** `source/build/goldset/147_d3c_recon_probe.py`\n")
    L.append(f"**Requests:** {n_req} · **Failed:** {len(errors)} ({share:.1%}) · "
             f"**Abort threshold:** {ERROR_ABORT_SHARE:.0%}\n")
    L.append("\nEvery zero below is a genuine absence, not a refused request: failures are counted "
             "separately and the report refuses to publish above the abort threshold.\n")

    for group in [g for g, _ in GROUPS]:
        L.append(f"\n## {group}\n")
        for g, label, filt, count, rows in results:
            if g != group:
                continue
            L.append(f"\n### {label} — **n = {count:,}**\n")
            L.append(f"`{filt}`\n\n")
            if not rows:
                L.append("*(no records)*\n")
                continue
            L.append("| Cites | Year | Title | Venue |\n|---|---|---|---|\n")
            for r in rows:
                t = r["title"][:95].replace("|", "/")
                v = r["venue"][:42].replace("|", "/")
                L.append(f"| {r['cites']:,} | {r['year']} | {t} | {v} |\n")

    for header, sink in (("Named-work resolution — pass 1", named_results),
                         ("Named-work resolution — pass 2 (alternate wordings)", retry_results)):
        L.append(f"\n## {header}\n\n")
        L.append("| Query | n | Top match | Year | Cites | Type |\n|---|---|---|---|---|---|\n")
        for q, count, rows in sink:
            if rows:
                r = rows[0]
                L.append(f"| {q[:55]} | {count} | {r['title'][:70].replace('|','/')} | {r['year']} | "
                         f"{r['cites']:,} | {r['type']} |\n")
            else:
                L.append(f"| {q[:55]} | 0 | **— no match —** | | | |\n")

    if errors:
        L.append("\n## Failed requests (excluded from every count above)\n\n")
        for lbl, e in errors:
            L.append(f"- `{lbl}` — {e}\n")

    os.makedirs(os.path.dirname(OUT_MD), exist_ok=True)
    open(OUT_MD, "w").write("".join(L))
    print(f"wrote {OUT_MD}  ({n_req} requests, {len(errors)} failed)")


if __name__ == "__main__":
    main()
