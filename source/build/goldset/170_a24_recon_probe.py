#!/usr/bin/env python3
"""
170_a24_recon_probe.py — A.24 (dating apps and union-formation friction), pre-scope reconnaissance.

Runs before the scope document. Establishes from live records rather than from memory:

  (a) whether the PRIMARY estimand cell exists at all — a study that estimates the effect of dating-
      app exposure on a FERTILITY quantity (births, TFR, completed fertility, number of children).
      The prior going in is that it is empty or near-empty: A.24 is a THREE-LINK chain (app adoption
      -> union formation -> births) and the identified literature almost certainly stops at link 1.
      This is B.7's shape exactly — there, link 2 of three had ONE record — and the point of asking
      now is that the answer decides whether this chapter grades a fertility effect or an upstream
      one. If link 3 is empty the scope must say so in its first paragraph, not discover it at
      extraction;

  (b) the size and separability of the GEOCHRONOLOGY homonym. "Dating" in radiocarbon/luminescence/
      U-series usage is a pure homonym on A.12's SHELX pattern: enormous, highly cited, and lexically
      separable. Sized here, counted exactly at A4, so the carve-out from forward-seed-everything
      rests on a measurement rather than on an assumption;

  (c) whether DATING VIOLENCE is separable. Unlike the geochronology cloud this is the same word
      sense — courtship — attached to a different outcome, so it cannot be split on the word "dating"
      and needs an outcome-side wall;

  (d) whether the mechanism (choice overload / strategic delay / commodification) has ever been
      ESTIMATED against a partnership or fertility outcome, or is only asserted. D.3.c's finding was
      that a hypothesis can be unmeasured in its own treatment literature; the same risk is live here
      because the friction claim is a psychological mechanism imported into a demographic argument;

  (e) whether the SIGN is contested. v5 asserts apps reduce conversion to committed partnership. The
      best-known finding in this literature (Rosenfeld and co-authors) is that apps have DISPLACED
      other ways of meeting and now dominate couple formation, which is at least consistent with apps
      raising match formation. The theory does not give the sign, and the scope must not assume it;

  (f) whether any QUASI-EXPERIMENT exists — app entry timing, broadband or 3G rollout, smartphone
      diffusion. If identification runs entirely through the technology-diffusion instrument, A.24's
      identified variation is the SAME variation as C.2.h's, and the two chapters have to be walled
      on outcome rather than on treatment or they will double-count;

  (g) whether an exposure series exists to run demographic significance against — HCMST, Pew adoption
      series, platform user counts. The whole of stage 10 depends on one existing.

Discipline carried from prior runs (B.5, B.6, B.7, D.2.d, D.3.b, D.3.c, A.12):
  * A failed request goes in an ERROR bucket kept SEPARATE from a genuine zero-hit, and the report
    refuses to publish if the error share exceeds ERROR_ABORT_SHARE. A wrong zero would propagate
    into the scope as "this literature does not exist" and be believed.
  * HTTPS goes through curl: the interpreter on this machine has no CA bundle, so urllib fails every
    call, and it fails as a *transport* error, i.e. as a fake zero.
  * OpenAlex is called with the funded api_key from .env, never with mailto alone.
  * Named-title probes run in two passes. A zero on `title.search` means the remembered wording is
    wrong; only an empty GROUP probe means a literature is absent.
  * Query hazards are checked before a single request is spent: no phrase opening with not/and/or
    (parsed as a boolean operator; the enclosing AND then returns the UNRESTRICTED count), no `?`
    (parsed as a wildcard; 200s with a body that reads as an empty literature), no phrase whose
    meaning rests on a stopword, and — new here, from A.12's A4 — no COMMA anywhere in a filter
    value, which is fatal and which percent-encoding does not save.

Output: literature/search-logs/dating-apps-union-formation-friction-recon-probe.md
"""
import json, os, subprocess, sys, time

SLUG = "dating-apps-union-formation-friction"
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

# Vocabulary blocks. Named constants because the walls are vocabulary tests and the wording has to be
# identical in the probe and in the scope document that quotes its counts.
APPS = ('("dating app" OR "dating apps" OR "online dating" OR "internet dating" OR "mobile dating" '
        'OR "dating website" OR "dating websites" OR "dating site" OR "dating sites" OR "Tinder" '
        'OR "dating platform" OR "dating platforms" OR "swipe-based" OR "matchmaking platform")')
UNION = ('("union formation" OR "partner formation" OR "couple formation" OR "relationship formation" '
         'OR "marriage formation" OR "cohabitation" OR "partnership formation" OR "marriage rate" '
         'OR "marriage rates" OR "entry into marriage" OR "repartnering" OR "family formation")')
FERT = ('("fertility" OR "birth rate" OR "birth rates" OR "total fertility rate" OR "completed fertility" '
        'OR "childbearing" OR "number of children" OR "childlessness" OR "transition to parenthood")')
POPFERT = ('("total fertility rate" OR "completed fertility" OR "cohort fertility" OR "aggregate fertility" '
           'OR "crude birth rate" OR "period fertility" OR "fertility decline" OR "fertility rates")')
FRICTION = ('("choice overload" OR "paradox of choice" OR "excessive choice" OR "option overload" '
            'OR "search friction" OR "search frictions" OR "matching friction" OR "strategic delay" '
            'OR "choice set size")')
COMMOD = ('("commodification" OR "objectification" OR "gamification" OR "swiping" OR "swipe" '
          'OR "rejection" OR "burnout" OR "dating fatigue")')
MATE = ('("mate choice" OR "mate preferences" OR "mate selection" OR "assortative mating" '
        'OR "marriage market" OR "partner search" OR "sorting" OR "homogamy")')
GEO = ('("radiocarbon dating" OR "radiometric dating" OR "luminescence dating" OR "carbon dating" '
       'OR "uranium-series dating" OR "geochronology" OR "dendrochronology" OR "isotope dating" '
       'OR "absolute dating" OR "relative dating")')
VIOLENCE = ('("dating violence" OR "teen dating violence" OR "dating abuse" OR "intimate partner violence" '
            'OR "sexual coercion" OR "dating aggression")')
SEXHEALTH = ('("sexual risk" OR "HIV" OR "sexually transmitted" OR "condom" OR "casual sex" OR "hookup" '
             'OR "hook-up" OR "Grindr" OR "sexual health" OR "PrEP" OR "men who have sex with men")')
IDENT = ('("instrumental variable" OR "difference-in-differences" OR "natural experiment" '
         'OR "exogenous variation" OR "staggered rollout" OR "event study" OR "regression discontinuity" '
         'OR "causal effect" OR "quasi-experimental")')
TECH = ('("broadband" OR "3G" OR "smartphone" OR "smartphones" OR "internet access" OR "mobile phone" '
        'OR "high-speed internet" OR "internet diffusion" OR "mobile broadband")')
CS = ('("recommender system" OR "recommendation algorithm" OR "reciprocal recommendation" '
      'OR "machine learning" OR "user engagement" OR "app usage" OR "platform design")')

GROUPS = [
    ("Link 3 — the PRIMARY cell. Dating-app exposure estimated against a FERTILITY quantity", [
        ("dating apps AND a population fertility quantity", f'title_and_abstract.search:{APPS} AND {POPFERT}'),
        ("dating apps AND any fertility outcome", f'title_and_abstract.search:{APPS} AND {FERT}'),
        ("dating apps AND childbearing / parenthood / childlessness", f'title_and_abstract.search:{APPS} AND ("childbearing" OR "transition to parenthood" OR "childlessness" OR "number of children" OR "having children")'),
        ("dating apps AND the demographic framing", f'title_and_abstract.search:{APPS} AND ("demographic transition" OR "low fertility" OR "birth dearth" OR "population decline" OR "demography")'),
        ("online dating named as a CAUSE of fertility decline", f'title_and_abstract.search:{APPS} AND ("explains" OR "contribution to" OR "accounts for" OR "driver of" OR "cause of") AND {FERT}'),
    ]),
    ("Link 1 — dating apps AND union formation. The reachable link, and the one v5's claim rests on", [
        ("dating apps AND union formation vocabulary", f'title_and_abstract.search:{APPS} AND {UNION}'),
        ("dating apps AND how couples meet", f'title_and_abstract.search:{APPS} AND ("met online" OR "how couples meet" OR "meeting" OR "intermediary" OR "displaced" OR "met their partner")'),
        ("dating apps AND marriage / cohabitation / dissolution", f'title_and_abstract.search:{APPS} AND ("marriage" OR "married" OR "cohabiting" OR "divorce" OR "breakup" OR "relationship dissolution")'),
        ("dating apps AND relationship quality / stability / duration", f'title_and_abstract.search:{APPS} AND ("relationship quality" OR "relationship satisfaction" OR "relationship stability" OR "relationship duration" OR "commitment")'),
        ("dating apps AND singlehood / partnerlessness — the outcome v5 actually predicts", f'title_and_abstract.search:{APPS} AND ("singlehood" OR "single adults" OR "unpartnered" OR "involuntary singlehood" OR "partnerless")'),
    ]),
    ("The MECHANISM — is friction estimated against an outcome or only asserted", [
        ("dating apps AND friction vocabulary", f'title_and_abstract.search:{APPS} AND {FRICTION}'),
        ("dating apps AND commodification / gamification / swipe fatigue", f'title_and_abstract.search:{APPS} AND {COMMOD}'),
        ("choice overload tested on MATE choice at all — inside or outside apps", f'title_and_abstract.search:{FRICTION} AND ("mate" OR "romantic" OR "partner" OR "dating" OR "speed dating")'),
        ("does the friction literature ever reach a DEMOGRAPHIC outcome", f'title_and_abstract.search:{FRICTION} AND ({UNION} OR {FERT})'),
    ]),
    ("SIGN CONTEST — evidence that apps RAISE match and union formation", [
        ("dating apps AND expansion of the choice set / market thickness", f'title_and_abstract.search:{APPS} AND ("market thickness" OR "thick market" OR "choice set" OR "search cost" OR "search costs" OR "expanded")'),
        ("dating apps AND interracial / educational sorting", f'title_and_abstract.search:{APPS} AND ("interracial" OR "assortative" OR "homogamy" OR "educational sorting" OR "social integration")'),
        ("online-met couples AND marital satisfaction or stability", f'title_and_abstract.search:{APPS} AND ("marital satisfaction" OR "marital stability" OR "marital quality" OR "divorce rate" OR "breakup rate")'),
    ]),
    ("IDENTIFICATION — does any quasi-experiment exist for this exposure", [
        ("dating apps AND identification vocabulary", f'title_and_abstract.search:{APPS} AND {IDENT}'),
        ("dating apps AND technology diffusion instruments", f'title_and_abstract.search:{APPS} AND {TECH}'),
        ("technology rollout AND union formation AND identification — the C.2.h shared instrument", f'title_and_abstract.search:{TECH} AND {UNION} AND {IDENT}'),
        ("technology rollout AND fertility AND identification", f'title_and_abstract.search:{TECH} AND {FERT} AND {IDENT}'),
        ("dating apps AND descriptive platform measurement (CS literature)", f'title_and_abstract.search:{APPS} AND {CS}'),
    ]),
    ("Decoy cloud 1 — GEOCHRONOLOGY. A pure homonym on the SHELX pattern", [
        ("geochronological dating vocabulary alone", f'title_and_abstract.search:{GEO}'),
        ("geochronology AND fertility — the cross-homonym (soil fertility in archaeology)", f'title_and_abstract.search:{GEO} AND {FERT}'),
        ("dating AND archaeology / sediment / fossil", 'title_and_abstract.search:("dating") AND ("archaeological" OR "sediment" OR "fossil" OR "stratigraphy" OR "Holocene" OR "Pleistocene")'),
    ]),
    ("Decoy cloud 2 — DATING VIOLENCE. Same word sense as the target - wrong outcome", [
        ("dating violence vocabulary alone", f'title_and_abstract.search:{VIOLENCE}'),
        ("dating violence AND apps", f'title_and_abstract.search:{VIOLENCE} AND {APPS}'),
        ("dating violence AND adolescents — the bulk of the cloud", f'title_and_abstract.search:{VIOLENCE} AND ("adolescent" OR "adolescents" OR "college students" OR "youth" OR "prevention")'),
    ]),
    ("Decoy cloud 3 — SEXUAL HEALTH and risk behaviour on platforms", [
        ("dating apps AND sexual health / risk", f'title_and_abstract.search:{APPS} AND {SEXHEALTH}'),
        ("dating apps AND casual sex specifically", f'title_and_abstract.search:{APPS} AND ("casual sex" OR "hookup" OR "hook-up" OR "sociosexuality" OR "one-night")'),
    ]),
    ("Boundary — C.7.a marriage market and mate choice. Routed, not excluded", [
        ("marriage-market vocabulary AND apps", f'title_and_abstract.search:{MATE} AND {APPS}'),
        ("marriage market AND fertility — the C.7.a chapter's own territory", f'title_and_abstract.search:{MATE} AND {FERT}'),
        ("speed dating and mate preference experiments — the pre-app mechanism literature", 'title_and_abstract.search:("speed dating" OR "speed-dating") AND ("mate" OR "preferences" OR "choice" OR "attraction")'),
    ]),
    ("Exposure series for demographic significance", [
        ("How Couples Meet and Stay Together", 'title_and_abstract.search:("How Couples Meet and Stay Together" OR "HCMST")'),
        ("population-representative measurement of app adoption", f'title_and_abstract.search:{APPS} AND ("nationally representative" OR "prevalence" OR "adoption" OR "survey of adults" OR "population survey" OR "user base")'),
        ("time series of the share of couples meeting online", f'title_and_abstract.search:{APPS} AND ("trend" OR "trends" OR "over time" OR "increase" OR "share of couples" OR "proportion of couples")'),
    ]),
    ("Channel 1 — prior systematic reviews", [
        ("SR/meta AND dating apps", f'title_and_abstract.search:("systematic review" OR "meta-analysis" OR "scoping review") AND {APPS}'),
        ("SR/meta AND dating apps AND relationships or fertility", f'title_and_abstract.search:("systematic review" OR "meta-analysis" OR "scoping review") AND {APPS} AND ({UNION} OR {FERT})'),
    ]),
]

# Named candidate works. Includes v5's own seminal list, which the probe TESTS rather than accepts —
# both the ghost-citation finding and the version-of-record gate came out of assuming a remembered
# citation resolves. v5 gives three: Rosenfeld Thomas and Hausen 2019; Tyson et al. 2016; Bruch and
# Newman 2018.
NAMED = [
    "Disintermediating your friends how online dating in the United States displaces other ways of meeting",
    "A first look at user activity on tinder",
    "Aspirational pursuit of mates in online dating markets",
    "Searching for a mate the rise of the internet as a social intermediary",
    "Online dating a critical analysis from the perspective of psychological science",
    "The strength of absent ties social integration via online dating",
    "Matching and sorting in online dating",
    "Marital satisfaction and break-ups differ across on-line and off-line meeting venues",
    "Online dating and fertility",
    "Dating apps and the decline in marriage",
    "The paradox of choice in online dating",
    "Smartphones and the transition to parenthood",
]

NAMED_RETRY = [
    "Rosenfeld Thomas Hausen disintermediating friends online dating",
    "Rosenfeld Thomas searching for a mate internet social intermediary",
    "Tyson Perta Haddadi Seto first look tinder user activity",
    "Bruch Newman aspirational pursuit of mates online dating",
    "Ortega Hergovich strength of absent ties online dating",
    "Hitsch Hortacsu Ariely matching and sorting in online dating",
    "Finkel Eastwick online dating critical analysis psychological science",
    "Cacioppo marital satisfaction meeting venues online",
    "online dating market thickness marriage formation",
    "dating app use union formation panel data",
    "internet diffusion marriage rates causal evidence",
    "broadband internet fertility rates evidence",
    "How Couples Meet and Stay Together survey methodology",
    "smartphone diffusion fertility decline instrument",
    "choice overload online dating experiment",
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


def guard_syntax():
    """Fail loudly before spending requests if any probe carries a known OpenAlex query hazard.

    Each of these produced a silently wrong count in an earlier chapter: a leading boolean word
    inflates to the unrestricted count, a `?` is read as a wildcard and 200s with an empty body, and
    a comma inside a FILTER value is fatal in a way percent-encoding does not fix (A.12, script 162).
    """
    bad = []
    for group, probes in GROUPS:
        for label, filt in probes:
            if "?" in filt:
                bad.append((label, "contains '?' — parsed as a wildcard"))
            if "," in filt:
                bad.append((label, "contains a comma — fatal inside a filter value"))
            for phrase in filt.split('"')[1::2]:
                first = phrase.strip().split(" ")[0].lower()
                if first in ("not", "and", "or"):
                    bad.append((label, f"phrase opens with boolean '{first}': \"{phrase}\""))
    for t in NAMED + NAMED_RETRY:
        if "?" in t or "," in t:
            bad.append((t[:45], "named probe carries '?' or a comma"))
    if bad:
        sys.stderr.write("ABORT: query hazards found; no requests spent.\n")
        for lbl, why in bad:
            sys.stderr.write(f"  {lbl}: {why}\n")
        sys.exit(2)


def main():
    guard_syntax()
    if not KEY:
        sys.stderr.write("ABORT: no OPENALEX_API_KEY. Unfunded calls return 'Insufficient budget', "
                         "which this probe would bucket as errors and abort on anyway.\n")
        sys.exit(3)

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
    L.append("**Hypothesis:** A.24 (HYPOTHESES-v5.md) · **Ticket:** TICK-071\n")
    L.append("**Generated by:** `source/build/goldset/170_a24_recon_probe.py`\n")
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
