#!/usr/bin/env python3
"""
160_a12_recon_probe.py — A.12 (twinning rates and multiple births), pre-scope reconnaissance.

Runs before the scope document. Establishes from live records rather than from memory:

  (a) whether the PRIMARY estimand cell exists at all — a study that estimates the effect of
      twinning-rate VARIATION on a POPULATION fertility quantity (TFR, CBR, completed fertility).
      The prior going in is that it is near-empty, because the mechanism is an accounting identity
      rather than a contested causal effect, and identities do not attract estimation. If that is
      right, the chapter's evidence base is a rate series plus an arithmetic computation, and the
      scope has to say so up front rather than discover it at extraction. This is the same shape as
      B.7's link-2 problem and D.3.c's mechanism problem, and it is settled here, not later;

  (b) the size of the decoy clouds, which for A.12 are larger relative to the signal than for any
      prior chapter. "Twin study", "twin registry", "twin cohort" denote a RESEARCH DESIGN in
      behaviour genetics that uses twins to decompose variance. It estimates no twinning rate and no
      fertility quantity. It shares essentially the whole vocabulary of the target literature;

  (c) whether the DETERMINANTS literature (what drives twinning rates: maternal age, parity, ART,
      ethnicity, nutrition) is separable at title/abstract from the CONSEQUENCES literature (what a
      twinning rate does to fertility). A.12 needs the second and will be flooded by the first. The
      determinants body is not a decoy in the ordinary sense — it is where the exposure series comes
      from — so it is routed, not excluded;

  (d) whether the OFFSET is real and measurable. A mechanical births-per-pregnancy uplift is an
      upper bound on the completed-fertility effect if parents of twins subsequently stop earlier.
      The twin-birth-as-instrument literature (Rosenzweig-Wolpin, Bronars-Grogger, Angrist-Lavy-
      Schlosser, Black-Devereux-Salvanes) contains exactly the estimates needed to bound this, but
      was assembled to answer quantity-quality questions and reports the offset, if at all, as a
      first-stage nuisance. Whether it is recoverable decides whether this chapter has an effect
      estimate or only an identity;

  (e) whether v5's ART clause still holds sign. v5 says ART-induced multiples "partially offset
      postponement-driven SDT declines". Single-embryo-transfer mandates (Belgium 2003, Sweden,
      Japan 2008, and broad practice change post-2010) cut ART multiple-birth rates sharply. If the
      offsetting term peaked and is now shrinking, v5's own claim is time-inverted and the chapter
      corrects the registry entry rather than rating it as written;

  (f) whether the PM arm is populated — the Yoruba/West African dizygotic literature and historical
      parish-register twinning rates — or whether PM has to be dropped to a bounded statement;

  (g) whether an exposure series exists to run demographic significance against. The Human Multiple
      Births Database is the candidate; the probe tests that it is real and citable rather than
      remembered, because the entire demographic-significance stage depends on it.

Discipline carried from prior runs (B.5, B.6, B.7, D.2.d, D.3.b, D.3.c):
  * A failed request goes in an ERROR bucket kept SEPARATE from a genuine zero-hit, and the report
    refuses to publish if the error share exceeds ERROR_ABORT_SHARE. A wrong zero would propagate
    into the scope document as "this literature does not exist".
  * HTTPS goes through curl: the interpreter on this machine has no CA bundle, so urllib fails every
    call, and it fails as a *transport* error, i.e. as a fake zero.
  * OpenAlex is called with the funded api_key from .env, never with mailto alone.
  * Named-title probes run in two passes. A zero on `title.search` means the remembered wording is
    wrong; only an empty GROUP probe means a literature is absent.
  * No search phrase opens with not/and/or (parsed as a boolean operator; the enclosing AND then
    returns the UNRESTRICTED count, which inflates rather than errors). No `?` anywhere in a search
    value (parsed as a wildcard; returns a 200 whose body reads as an empty literature). No phrase
    whose meaning rests on a stopword ("no future" is indexed as "future").

Output: literature/search-logs/twinning-multiple-births-recon-probe.md
"""
import json, os, subprocess, sys, time

SLUG = "twinning-multiple-births"
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
TWIN_RATE = '("twinning rate" OR "twinning rates" OR "twin rate" OR "multiple birth rate" OR "multiple birth rates" OR "multiple delivery rate" OR "rate of twinning" OR "twinning frequency")'
MULTIPLE = '("multiple birth" OR "multiple births" OR "twin birth" OR "twin births" OR "twinning" OR "multiple pregnancy" OR "multiple pregnancies" OR "higher order multiple")'
FERT = '("fertility" OR "birth rate" OR "birth rates" OR "total fertility rate" OR "completed fertility" OR "childbearing" OR "crude birth rate")'
POPFERT = '("total fertility rate" OR "completed fertility" OR "cohort fertility" OR "population fertility" OR "aggregate fertility" OR "crude birth rate")'
ART = '("in vitro fertilization" OR "in vitro fertilisation" OR "IVF" OR "assisted reproductive technology" OR "assisted reproduction" OR "ICSI" OR "ovulation induction" OR "ovarian stimulation")'
ESET = '("single embryo transfer" OR "elective single embryo transfer" OR "eSET" OR "embryo transfer policy" OR "number of embryos transferred")'
TWINSTUDY = '("twin study" OR "twin studies" OR "twin registry" OR "twin register" OR "twin cohort" OR "heritability" OR "monozygotic" OR "dizygotic twins reared")'
STOPPING = '("stopping behavior" OR "stopping behaviour" OR "parity progression" OR "subsequent fertility" OR "later fertility" OR "family size target" OR "fertility stopping")'
IV = '("instrumental variable" OR "instrument" OR "exogenous variation" OR "natural experiment" OR "quantity-quality" OR "quantity quality tradeoff")'
DEMOG = '("demographic" OR "demography" OR "population" OR "vital statistics" OR "registry" OR "register data")'

GROUPS = [
    ("The PRIMARY cell — twinning-rate variation estimated against a POPULATION fertility quantity", [
        ("twinning rate AND population fertility quantity", f'title_and_abstract.search:{TWIN_RATE} AND {POPFERT}'),
        ("multiple births AND total fertility rate / completed fertility", f'title_and_abstract.search:{MULTIPLE} AND {POPFERT}'),
        ("contribution OR share of multiple births to the birth rate", f'title_and_abstract.search:{MULTIPLE} AND ("contribution to" OR "share of births" OR "accounted for" OR "proportion of births" OR "decomposition")'),
        ("twinning as a DETERMINANT of fertility level, explicit", f'title_and_abstract.search:{TWIN_RATE} AND ("effect on fertility" OR "impact on fertility" OR "fertility differences" OR "explains fertility" OR "fertility variation")'),
        ("twinning AND the demographic transition framing", f'title_and_abstract.search:{MULTIPLE} AND ("demographic transition" OR "fertility decline" OR "fertility transition" OR "low fertility")'),
    ]),
    ("Decoy cloud 1 — the twin STUDY DESIGN, which estimates no twinning rate and no fertility level", [
        ("twin study / registry / heritability, all", f'title_and_abstract.search:{TWINSTUDY}'),
        ("twin design AND fertility — the lexical collision this chapter must survive", f'title_and_abstract.search:{TWINSTUDY} AND {FERT}'),
        ("heritability OF fertility measured BY twin design (this is A.18, not A.12)", f'title_and_abstract.search:{TWINSTUDY} AND ("fertility" OR "number of children" OR "reproductive behavior") AND {IV}'),
        ("does the twinning-RATE vocabulary separate from the twin-DESIGN vocabulary", f'title_and_abstract.search:{TWIN_RATE} AND {TWINSTUDY}'),
    ]),
    ("Decoy cloud 2 — obstetric and neonatal consequences OF being a multiple", [
        ("multiple birth AND neonatal / obstetric outcomes", f'title_and_abstract.search:{MULTIPLE} AND ("preterm" OR "low birth weight" OR "neonatal mortality" OR "perinatal" OR "NICU" OR "gestational age" OR "complications")'),
        ("multiple birth AND cost / health system burden", f'title_and_abstract.search:{MULTIPLE} AND ("cost" OR "costs" OR "economic burden" OR "hospital" OR "healthcare utilization")'),
        ("maternal outcomes of twin pregnancy", f'title_and_abstract.search:{MULTIPLE} AND ("maternal mortality" OR "preeclampsia" OR "caesarean" OR "cesarean" OR "maternal morbidity")'),
    ]),
    ("The DETERMINANTS body — where the exposure series comes from (routed, not excluded)", [
        ("twinning rate trends over time", f'title_and_abstract.search:{TWIN_RATE} AND ("trend" OR "trends" OR "secular trend" OR "over time" OR "increase" OR "rise" OR "decline")'),
        ("twinning rate AND maternal age / parity", f'title_and_abstract.search:{TWIN_RATE} AND ("maternal age" OR "advanced maternal age" OR "parity" OR "age at birth")'),
        ("twinning rate AND ART / ovulation induction", f'title_and_abstract.search:{TWIN_RATE} AND {ART}'),
        ("multiple birth rate AND ART, broader", f'title_and_abstract.search:{MULTIPLE} AND {ART} AND ("rate" OR "rates" OR "proportion" OR "incidence")'),
        ("twinning rate AND ethnicity / geography / cross-country variation", f'title_and_abstract.search:{TWIN_RATE} AND ("ethnic" OR "ethnicity" OR "cross-country" OR "international" OR "geographic" OR "regional variation" OR "Africa" OR "Nigeria")'),
        ("twinning rate AND nutrition / height / seasonality", f'title_and_abstract.search:{TWIN_RATE} AND ("nutrition" OR "nutritional status" OR "height" OR "body mass" OR "seasonality" OR "famine")'),
    ]),
    ("The OFFSET — does a twin birth reduce SUBSEQUENT fertility (mechanical uplift as upper bound)", [
        ("twin birth AND subsequent / later fertility", f'title_and_abstract.search:("twin birth" OR "twin first birth" OR "multiple birth") AND {STOPPING}'),
        ("twin birth as an INSTRUMENT for family size", f'title_and_abstract.search:("twin birth" OR "twins" OR "twinning") AND {IV} AND ("family size" OR "number of children" OR "sibship size" OR "fertility")'),
        ("parity targeting — do parents of twins stop earlier", f'title_and_abstract.search:("twins" OR "twin birth") AND ("desired family size" OR "target family size" OR "stopping rule" OR "parity progression ratio")'),
        ("unplanned twin birth AND completed family size", f'title_and_abstract.search:("unexpected" OR "unplanned" OR "exogenous") AND ("twin" OR "twins" OR "multiple birth") AND ("completed fertility" OR "family size" OR "number of children")'),
    ]),
    ("The ART clause — is v5's offsetting term still growing, or did eSET reverse it", [
        ("single embryo transfer policy AND multiple birth rate", f'title_and_abstract.search:{ESET} AND {MULTIPLE}'),
        ("decline in ART multiple births post-policy", f'title_and_abstract.search:{ART} AND {MULTIPLE} AND ("decline" OR "decrease" OR "reduction" OR "fell" OR "policy" OR "regulation" OR "mandate")'),
        ("ART share of all births in a population", f'title_and_abstract.search:{ART} AND ("share of births" OR "proportion of births" OR "percentage of births" OR "of all births" OR "population level")'),
        ("ART contribution to national TFR", f'title_and_abstract.search:{ART} AND {POPFERT}'),
    ]),
    ("The PM arm — is it populated, or does it reduce to a bounded statement", [
        ("historical twinning rates — parish registers / family reconstitution", f'title_and_abstract.search:{TWIN_RATE} AND ("historical" OR "parish register" OR "family reconstitution" OR "pre-industrial" OR "preindustrial" OR "nineteenth century" OR "eighteenth century")'),
        ("Yoruba / West African high dizygotic twinning", f'title_and_abstract.search:("Yoruba" OR "Nigeria" OR "West Africa" OR "Benin") AND ("twinning" OR "twin" OR "dizygotic") AND ("rate" OR "rates" OR "frequency" OR "high")'),
        ("twinning AND natural fertility populations", f'title_and_abstract.search:{MULTIPLE} AND ("natural fertility" OR "Hutterite" OR "pre-transitional" OR "historical demography")'),
        ("twin survival penalty in historical populations", f'title_and_abstract.search:("twin" OR "twins" OR "multiple birth") AND ("infant mortality" OR "child mortality" OR "survival") AND ("historical" OR "pre-industrial" OR "parish")'),
    ]),
    ("Exposure series for demographic significance", [
        ("Human Multiple Births Database", 'title_and_abstract.search:("Human Multiple Births Database" OR "multiple births database" OR "HMBD")'),
        ("cross-national twinning rate compilations", f'title_and_abstract.search:{TWIN_RATE} AND ("developed countries" OR "cross-national" OR "comparison" OR "database" OR "compilation" OR "harmonized")'),
        ("ART registry reporting — ICMART / ESHRE / SART", 'title_and_abstract.search:("ICMART" OR "ESHRE" OR "SART" OR "assisted reproductive technology surveillance") AND ("registry" OR "report" OR "surveillance" OR "monitoring")'),
    ]),
    ("Channel 1 — prior systematic reviews", [
        ("SR/meta — twinning rates", f'title_and_abstract.search:("systematic review" OR "meta-analysis" OR "scoping review") AND {TWIN_RATE}'),
        ("SR/meta — multiple birth AND ART", f'title_and_abstract.search:("systematic review" OR "meta-analysis") AND {MULTIPLE} AND {ART}'),
        ("SR/meta — twin birth AND family size or subsequent fertility", f'title_and_abstract.search:("systematic review" OR "meta-analysis") AND ("twin" OR "multiple birth") AND ("family size" OR "fertility")'),
    ]),
]

# Named candidate works. Includes v5's own seminal list, which the probe is meant to TEST rather than
# accept — the version-of-record gate and the ghost-citation finding both came out of assuming a
# remembered citation resolves.
NAMED = [
    # v5's seminal list, as written in HYPOTHESES-v5.md A.12
    "The Biology of Twinning in Man",
    "Frequency of twin births among the world populations",
    "Twinning rates in developed countries trends and explanations",
    # The modern rate canon
    "Twin peaks more twinning in humans than ever before",
    "Twinning across the developing world",
    "The rise of twin births and the role of assisted reproduction",
    # The offset / instrument canon
    "Testing the quantity quality fertility model the use of twins as a natural experiment",
    "The economic consequences of unwed motherhood using twin births as a natural experiment",
    "The more the merrier the effect of family size and birth order on children's education",
    "New evidence on the causal link between the quantity and quality of children",
    # ART and eSET
    "Elective single embryo transfer and multiple birth rates",
    "The effect of assisted reproductive technology on multiple birth rates",
]

NAMED_RETRY = [
    "Bulmer biology of twinning",
    "Pison Dadato frequency of twin births",
    "Pison Monden Smits twinning rates developed countries",
    "Monden Smits Pison twin peaks",
    "Hoekstra dizygotic twinning genetics",
    "Smits Monden twinning across Africa",
    "Rosenzweig Wolpin testing the quantity quality model",
    "Bronars Grogger economic consequences of unwed motherhood twins",
    "Black Devereux Salvanes more the merrier family size",
    "Angrist Lavy Schlosser multiple experiments for the causal link quantity quality",
    "Twinning rate secular trend United States",
    "Multiple births and the total fertility rate",
    "Contribution of assisted reproduction to national birth rates",
    "Single embryo transfer policy Belgium multiple births",
    "Twinning rate Nigeria Yoruba dizygotic",
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
    inflates to the unrestricted count, a `?` is read as a wildcard and 200s with an empty body.
    """
    bad = []
    for group, probes in GROUPS:
        for label, filt in probes:
            if "?" in filt:
                bad.append((label, "contains '?' — parsed as a wildcard"))
            for phrase in filt.split('"')[1::2]:
                first = phrase.strip().split(" ")[0].lower()
                if first in ("not", "and", "or"):
                    bad.append((label, f"phrase opens with boolean '{first}': \"{phrase}\""))
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
    L.append("**Hypothesis:** A.12 (HYPOTHESES-v5.md) · **Ticket:** TICK-070\n")
    L.append(f"**Generated by:** `source/build/goldset/160_a12_recon_probe.py`\n")
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
