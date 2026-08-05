#!/usr/bin/env python3
r"""
104_d1a_prefilter.py — D.1.a. The deterministic pre-filter that runs BEFORE the paid LLM screen.

The screen rubric (`{slug}-screen-rubric.md`) recommends dropping the clinical/veterinary collision
and the book reviews mechanically rather than paying a model to read obstetrics abstracts. This is
that filter. It is deliberately the dumbest component in the pipeline: no model, no scoring, no
threshold -- a term fires or it does not, and every drop is attributable to a named term.

THREE DESIGN RULES, EACH BOUGHT WITH A BUG THIS PROJECT ALREADY COMMITTED.

(1) DROPS MATCH ON THE TITLE ONLY. The collision is a title-vocabulary phenomenon -- `value` meeting
    `birth` inside a clinical idiom -- and it was measured on titles. Matching drops against the
    abstract would reject an on-pair religiosity paper for mentioning breastfeeding once in its
    methods. The abstract is read ONLY as rescue evidence, never as drop evidence. The asymmetry is
    the point: it can only ever keep a record, never remove one.

(2) EVERY PATTERN IS WORD-ANCHORED. `hous` inside `thousand` (C.2.c), `reproduc\w+` admitting social
    reproduction (v1), and a bare `429` matching the Unix timestamp `1429894924000` (the snowball
    transport layer) are three unanchored-substring bugs in this codebase already. Every term here is
    compiled with `\b` on both ends and the stemming is written out explicitly rather than left to a
    trailing `\w*` where it is not wanted.

(3) A RESCUE SIGNAL OVERRIDES ANY DROP TERM. A record carrying human-demographic or religious
    vocabulary is kept even when a clinical term fires, because the costs are not symmetric: a
    wrongly-kept record costs one LLM read and a wrongly-dropped record costs the study. The rescue
    vocabulary is deliberately built from DEMOGRAPHIC and RELIGIOUS words and contains no value-scale
    words -- `individualis`, `materialis` and `value` are exactly the terms OpenAlex stemming
    corrupts ("sperm individualization", "individualised dosing of follitropin delta"), so rescuing
    on them would rescue the very false positives this filter exists to remove.

WHAT THE TERM LIST IS NOT ALLOWED TO CONTAIN. `breastfeeding`, `lactation`, `postpartum` and
`birth interval` are clinical-sounding and are core proximate-determinants demography (Bongaarts).
They are listed below under REJECTED_TERMS with the records that proved it, so that a later reader
does not re-propose them. This is the fourth time on this chapter that the obvious exclusion would
have manufactured a worse false-negative class than the one it removed.

THE ACCEPTANCE GATE IS GOLD LOSS, AND IT IS ZERO. The frozen Tier A / Tier B gold is run through the
filter. Any gold record the filter drops is a demonstrated false negative and the run FAILS rather
than reporting a percentage. A pre-filter that silently thins the gold is the truncated-pull failure
in a different costume.

Usage:
  python3 104_d1a_prefilter.py            # run, write outputs, exit nonzero on gold loss
  python3 104_d1a_prefilter.py --audit    # additionally dump a per-term rejected sample for reading

Output: literature/search-logs/{slug}-prefilter.json        disposition index + attributed drops
          The queue is a list of `openalex_id`, not a copy of the records. Join it against
          `{slug}-live-corpus.json`, which stays the single record of what the pull returned.
        literature/search-logs/{slug}-prefilter-log.md      the log, incl. per-term firing table
        literature/search-logs/{slug}-prefilter-rejected-sample.md   the human read
"""
import json, os, re, sys, unicodedata
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import importlib.util

SLUG = "postmaterialism-individualism-secularization"
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
LOGS = os.path.join(ROOT, "literature", "search-logs")
# `--query v2` reads the repaired query's corpus and writes `-v2` outputs, so v1's record survives.
_V2 = "--query" in sys.argv and sys.argv[sys.argv.index("--query") + 1] == "v2"
SUF = "-v2" if _V2 else ""
CORPUS = os.path.join(LOGS, f"{SLUG}-live-corpus{SUF}.json")
OUT_JSON = os.path.join(LOGS, f"{SLUG}-prefilter{SUF}.json")
OUT_MD = os.path.join(LOGS, f"{SLUG}-prefilter-log{SUF}.md")
OUT_SAMPLE = os.path.join(LOGS, f"{SLUG}-prefilter-rejected-sample{SUF}.md")

_spec = importlib.util.spec_from_file_location("cv", os.path.join(HERE, "101_d1a_cv_breadth.py"))
cv = importlib.util.module_from_spec(_spec)
sys.modules["cv"] = cv
_spec.loader.exec_module(cv)

SAMPLE_PER_TERM = 12

# --------------------------------------------------------------------------------------------
# DROP VOCABULARY. Grouped by collision class. Each entry is a bare pattern; `\b` is added on both
# sides at compile time. Stemming is explicit -- `\w*` appears only where every extension is also
# unambiguously clinical.
# --------------------------------------------------------------------------------------------
DROP_TERMS = {
    # The ART / infertility-clinic literature. This is the collision that owns the word `fertility`
    # in medicine, and none of these words has a demographic sense.
    "ART_CLINICAL": [
        r"ivf", r"icsi", r"oocytes?", r"blastocysts?", r"embryos?", r"embryonic",
        r"spermatozoa", r"spermatid\w*", r"sperm", r"semen", r"ovarian", r"ovulation",
        r"ovulatory", r"follicles?", r"follicular", r"follitropin", r"gonadotroph?ins?",
        r"endometri\w+", r"insemination", r"cryopreservation", r"cryopreserved",
        r"azoospermi\w+", r"oligospermi\w+", r"varicocele", r"in vitro", r"in-vitro",
        r"luteal", r"progesterone", r"oestrous", r"estrous", r"cumulus", r"blastocyst",
        r"assisted reproductive technolog\w+", r"intracytoplasmic",
    ],
    # Obstetric and perinatal medicine. NOTE what is absent -- see REJECTED_TERMS.
    "OBSTETRIC": [
        r"preterm", r"neonat\w+", r"perinat\w+", r"antenatal", r"cervical", r"cervix",
        r"gestational", r"ultraso\w+", r"obstetric\w*", r"caesarean", r"cesarean",
        r"eclampsi\w+", r"placent\w+", r"amniotic", r"birth ?weight", r"apgar",
        r"intrapartum", r"trimester", r"uterocervical", r"fetal", r"foetal",
        r"stillbirths?", r"neonate", r"nulliparous women with",
    ],
    # Soil science and agronomy. NOT named in the screen rubric -- found in this script's own probe
    # of the C1 corpus. `soil fertility` is a large, entirely separate literature that shares the
    # outcome word outright.
    "AGRONOMY": [
        r"soils?", r"agronom\w+", r"fertili[sz]ers?", r"manure", r"compost\w*", r"tillage",
        r"crops?", r"cropping", r"maize", r"wheat", r"paddy", r"pasture", r"forage",
        r"horticultur\w+", r"agroforestr\w+", r"nutrient uptake", r"yields?", r"germination",
        r"seedlings?", r"biochar", r"legumes?",
    ],
    # `secular trend` is demography's term of art for a long-run trend and carries NO religious
    # content -- the screen rubric names it as a standing near-miss. It is here rather than left to
    # the screen for a precision reason and not a cost one: `secular` is THIS CHAPTER'S OWN TREATMENT
    # WORD, so these are the highest-risk false positives in the queue. A screen reading "Secular
    # changes in rates of multiple births in the United States" can route it to S3 with a fertility
    # outcome and be confidently wrong. Measured before it shipped: 117 records carry the idiom, 65
    # of them carry no religious or demographic signal whatsoever and are uniformly epidemiology
    # (lung cancer mortality, body mass index, blood pressure, unprovoked seizures, adult height).
    # The rescue is what makes this safe -- it keeps "Disputing Contraception: Muslim Reform, Secular
    # Change and Fertility", which is squarely S3.
    "SECULAR_TERM_OF_ART": [
        r"secular trends?", r"secular changes?", r"secular declines?", r"secular increases?",
        r"secular variations?",
    ],
    # Animal and laboratory biology.
    "ANIMAL_LAB": [
        r"cattle", r"bovine", r"heifers?", r"calving", r"calves", r"swine", r"porcine",
        r"sows?", r"boars?", r"poultry", r"broilers?", r"ewes?", r"rams?", r"mares?",
        r"stallions?", r"livestock", r"drosophila", r"murine", r"mice", r"rats?",
        r"zebrafish", r"knockout", r"in ?breeding depression", r"hatchability", r"buffalo\w*",
        r"goats?", r"sheep", r"stud", r"semen quality",
    ],
}

# --------------------------------------------------------------------------------------------
# TERMS DELIBERATELY REFUSED, with the record that refused them. Kept in the source so the next
# reader does not re-propose an exclusion this run already measured and rejected.
# --------------------------------------------------------------------------------------------
REJECTED_TERMS = [
    ("breastfeeding / lactation", "core proximate-determinants demography (Bongaarts), not clinical",
     "In Kenya, Modernization, Drop in Breastfeeding and Low Contraceptive Use Bring Rising "
     "Fertility"),
    ("postpartum", "postpartum insusceptibility is a proximate determinant of natural fertility",
     "Birth and Breastfeeding Dynamics in a Modernizing Indigenous Community"),
    ('the phrase "value of"', "matches 379 records of which only 118 are clinical; the rest are the "
     "Value of Children literature, which is on-pair S1/S5",
     "Changing Value of Children and Fertility Transition in Turkey"),
    ("birth interval / birth spacing", "the classic demographic spacing literature",
     "(pre-emptive: named in the scope's outcome vocabulary)"),
    ("pregnancy / pregnant", "used throughout demography for reported pregnancies and intentions",
     "(pre-emptive: would drop fertility-intention surveys wholesale)"),
    ("bare *secular* as a rescue term",
     "the religious senses are enumerated instead; `secular\\w+` silently never "
     "matches the bare word and `secular\\w*` rescues the term-of-art",
     "Secular Trends in Preterm Birth Rates (term of art) vs. Secular values and childbearing"),
]

# --------------------------------------------------------------------------------------------
# RESCUE VOCABULARY. Human-demographic and religious signal only. No value-scale words: those are
# the stemming-corrupted ones and rescuing on them would rescue the false positives.
# --------------------------------------------------------------------------------------------
RESCUE_TERMS = [
    # demographic outcome and framework vocabulary
    r"fertility transition", r"fertility decline", r"fertility differentials?",
    r"fertility intentions?", r"fertility preferences?", r"fertility behaviou?rs?",
    r"fertility rates?", r"total fertility", r"tfr", r"completed fertility",
    r"cohort fertility", r"marital fertility", r"natural fertility", r"fertility desires?",
    r"demographic transition", r"second demographic transition", r"childless\w*",
    r"family size", r"ideal number of children", r"desired number of children",
    r"value of children", r"childbearing", r"childbirth intentions?", r"nuptiality",
    r"parity progression", r"birth rates?", r"crude birth", r"population growth",
    r"population policy", r"baby boom", r"reproductive success", r"fecundit\w+",
    r"census", r"demograph\w+", r"birth order",
    # survey instruments this literature runs on
    r"world values survey", r"european values", r"european social survey",
    r"general social survey", r"demographic and health survey", r"wvs", r"evs", r"dhs",
    r"gss", r"panel study", r"longitudinal survey",
    # Religious vocabulary -- unambiguously not clinical, and S3 is the chapter's largest stratum.
    # SECULAR IS ENUMERATED RATHER THAN STEMMED, and this is the rubric's `secular trend` warning
    # made mechanical. The first version wrote `secular\w+`, which silently never matched the bare
    # word `secular` at all (it requires a trailing word character) -- so "secular values and
    # childbearing" would not have rescued. The naive repair to `secular\w*` matches "secular trends
    # in preterm birth" and "secular change in birth weight", i.e. it rescues the demographic
    # term-of-art that carries NO religious content and is explicitly not an S3 paper. Neither the
    # broken form nor its obvious fix is right; the religious senses are therefore listed out, and
    # the term-of-art idioms are blocked below.
    r"religio\w+", r"religiosity", r"seculari[sz]\w*", r"secularity", r"secularism",
    r"secular values?", r"secular societ\w+", r"secular states?", r"church\w*", r"mosques?",
    r"synagogues?",
    r"catholic\w*", r"protestant\w*", r"muslims?", r"islam\w*", r"jewish", r"judaism",
    r"hindus?", r"hinduism", r"buddhis\w+", r"denominational?", r"congregations?",
    r"piety", r"faith", r"clergy", r"theolog\w+", r"mormon\w*", r"evangelical\w*",
    r"amish", r"hutterites?", r"orthodox",
    # social-science framing
    r"moderni[sz]ation", r"moderni[sz]ing", r"contracepti\w+", r"marriage", r"marital status",
    r"cohabitation", r"divorce", r"gender roles?", r"socioeconomic", r"socio-economic",
    r"attitudes? toward", r"social norms?", r"post-?industrial", r"postmaterial\w*",
]

# Idioms that wear a rescue word without carrying its sense. `live birth rate` is IVF vocabulary
# wearing a demographic word; `secular trend` is demography's term of art for a long-run trend and
# has no religious content at all, which the screen rubric names as a standing near-miss.
RESCUE_BLOCKERS = [r"live birth rates?", r"live-birth rates?", r"clinical pregnancy rates?",
                   r"secular trends?", r"secular changes?", r"secular declines?",
                   r"secular increases?", r"secular variations?"]

BOOK_REVIEW_TYPES = {"book-review"}


def fold(s):
    """Lowercase and fold diacritics, KEEPING word boundaries.

    Deliberately not `cv.norm`, which strips to bare alphanumerics and would destroy the `\\b`
    anchors every pattern here depends on. The diacritic folding is the repair A6a made after the
    normalizer was found deleting non-ASCII outright, turning `fecondite` into `f condit` so the
    French and Spanish terms could never match.
    """
    s = unicodedata.normalize("NFKD", s or "")
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = re.sub(r"<[^>]+>", " ", s)          # OpenAlex titles carry <i>/<sub> markup
    return re.sub(r"\s+", " ", s.lower()).strip()


def compile_all(terms):
    return [(t, re.compile(r"\b" + t + r"\b", re.I)) for t in terms]


DROP_RX = {g: compile_all(ts) for g, ts in DROP_TERMS.items()}
RESCUE_RX = compile_all(RESCUE_TERMS)
BLOCK_RX = compile_all(RESCUE_BLOCKERS)


def rescue_hits(text):
    """Rescue terms present in the text, after removing the blocked idioms."""
    t = text
    for _, rx in BLOCK_RX:
        t = rx.sub(" ", t)
    return [term for term, rx in RESCUE_RX if rx.search(t)]


def classify(rec):
    """Return (disposition, rule, terms, rescued_by).

    Disposition is one of SCREEN, DROP, LEAD. Drops read the TITLE only; rescue reads title +
    abstract, because rescue can only ever keep a record.
    """
    title = fold(rec.get("title") or "")
    if not title:
        # No title is not evidence of anything. Keep and let the screen see it.
        return "SCREEN", None, [], ["no title -- kept by default"]

    rescued_all = rescue_hits(title + " " + fold(rec.get("abstract") or ""))

    if rec.get("type") in BOOK_REVIEW_TYPES:
        # A BOOK REVIEW IS NOT EVIDENCE, BUT IT IS THE ONLY TRACE OF A BOOK. The first version sent
        # all 262 straight to OFF_OTHER. Reading the rejected sample showed what that deletes:
        # reviews of Jones and Grupp's `Modernization, Value Change, and Fertility in the Soviet
        # Union`, Yaukey's `Fertility Differences in a Modernizing Country`, and Fukuda's `Marriage
        # and fertility behaviour in Japan -- Economic status and value orientation`. Those are
        # squarely on-pair monographs, and the review is the only record of them the pull returned.
        # This chapter has now hit an indexing gap on books, book chapters, dissertations and
        # non-English work FIVE separate times, and dropping the reviews would thin the corpus in
        # exactly that direction again. So an on-pair-looking review is not evidence and not junk --
        # it is a RETRIEVAL LEAD, routed to its own bucket, and the reviewed work is what to chase.
        if rescued_all:
            return "LEAD", "BOOK_REVIEW_LEAD", ["type=book-review"], rescued_all
        return "DROP", "BOOK_REVIEW", ["type=book-review"], []

    fired = [(g, t) for g, rxs in DROP_RX.items() for t, rx in rxs if rx.search(title)]
    if not fired:
        return "SCREEN", None, [], []
    if rescued_all:
        return "SCREEN", None, [f"{g}:{t}" for g, t in fired], rescued_all
    return "DROP", fired[0][0], [f"{g}:{t}" for g, t in fired], []


def gold_gate(records):
    """Run the frozen gold through the filter. Any drop is a demonstrated false negative.

    Gold records are matched into the corpus by normalized title so that the filter is tested on the
    record as the live pull actually returned it -- markup, casing and all -- rather than on the
    clean stored title.
    """
    gold, _, _ = cv.load()
    by_title = {}
    for r in records:
        if r.get("title"):
            by_title.setdefault(cv.norm(r["title"])[:70], r)
    losses, tested = [], 0
    for g in gold:
        rec = by_title.get(cv.norm(g["title"])[:70])
        if rec is None:
            continue                      # not in the corpus at all -- that is a recall question
        tested += 1
        disp, rule, terms, _ = classify(rec)
        # LEAD counts as a loss for gate purposes: a gold record must reach the screen, not a
        # retrieval worklist. The bucket exists for reviews OF books, not for the books themselves.
        if disp != "SCREEN":
            losses.append({"title": g["title"][:140], "tier": g["tier"], "pair": g.get("pair"),
                           "disposition": disp, "rule": rule, "terms": terms})
    return tested, losses


def main():
    audit = "--audit" in sys.argv
    d = json.load(open(CORPUS))
    records = d["records"]
    incomplete = d.get("incomplete_clusters") or []

    kept, dropped, leads = [], [], []
    term_fires, rescue_saves = Counter(), Counter()
    per_term_samples = {}
    for r in records:
        disp, rule, terms, rescued = classify(r)
        thin = {k: r.get(k) for k in
                ("openalex_id", "doi", "title", "year", "type", "clusters")}
        if disp == "SCREEN":
            kept.append(r)
            for t in terms:                      # fired but rescued
                rescue_saves[t] += 1
                per_term_samples.setdefault("RESCUED:" + t, []).append(r.get("title") or "")
        elif disp == "LEAD":
            leads.append({**thin, "prefilter_rule": rule, "rescued_by": rescued,
                          "prefilter_cell": "BOOK_REVIEW_LEAD"})
        else:
            dropped.append({**thin, "prefilter_rule": rule, "prefilter_terms": terms,
                            "prefilter_cell": "OFF_OTHER"})
            for t in terms:
                term_fires[t] += 1
                per_term_samples.setdefault(t, []).append(r.get("title") or "")

    tested, losses = gold_gate(records)

    # ---- outputs ---------------------------------------------------------------------------
    out = {"slug": SLUG, "stage": "C1-prefilter", "source_corpus_records": len(records),
           "source_corpus_complete": not incomplete,
           "incomplete_clusters": incomplete,
           "kept": len(kept), "dropped": len(dropped), "book_review_leads": len(leads),
           "gold_tested": tested, "gold_lost": len(losses), "gold_losses": losses,
           "term_fires": dict(term_fires.most_common()),
           "rescue_saves": dict(rescue_saves.most_common()),
           # THE QUEUE IS AN INDEX, NOT A COPY. Writing the kept records whole made this artifact
           # 14MB against the 16MB corpus it is derived from -- the same records committed twice,
           # differing only by what was removed. Downstream joins on `openalex_id` against
           # `{slug}-live-corpus.json`, which stays the single record of what the pull returned.
           "screening_queue_ids": [r["openalex_id"] for r in kept],
           "dropped_records": dropped, "retrieval_leads": leads}
    json.dump(out, open(OUT_JSON, "w"), indent=1)

    pct = 100 * len(dropped) / len(records) if records else 0
    L = ["# D.1.a — deterministic pre-filter before the LLM screen", "",
         "Removes the clinical/veterinary collision and the book reviews mechanically, so the paid "
         "screen is not spent reading obstetrics abstracts. No model, no scoring, no threshold: a "
         "named term fires or it does not, and **every drop is attributable to the term that caused "
         "it**.", ""]
    if incomplete:
        L += ["> ## ⚠ CALIBRATED ON AN INCOMPLETE CORPUS", "",
              f"> `{', '.join(incomplete)}` had not finished pulling when this ran, so the term list "
              f"is tuned on **{len(records):,}** records rather than the full universe. The counts "
              f"below will move. **This filter must be re-run and its rejected sample re-read once "
              f"C1 completes** — a filter validated at one order of magnitude has been wrong at the "
              f"next three times on this chapter.", ""]
    L += [f"- corpus in: **{len(records):,}**",
          f"- kept for screening: **{len(kept):,}**",
          f"- dropped: **{len(dropped):,}** ({pct:.1f}%)",
          f"- routed to the book-review retrieval worklist: **{len(leads):,}**",
          f"- gold records present in the corpus and run through the filter: **{tested}**",
          f"- **gold lost: {len(losses)}**" + ("  ← ACCEPTANCE GATE FAILED" if losses else
                                               "  ← gate passed"), ""]
    if losses:
        L += ["## ⚠ GOLD LOST — these are demonstrated false negatives", ""]
        L += [f"- `{x['rule']}` via `{', '.join(x['terms'])}` — {x['title']}" for x in losses]
        L += [""]
    L += ["## Design", "",
          "1. **Drops match the title only.** The collision is a title-vocabulary phenomenon. The "
          "abstract is read only as *rescue* evidence, so it can keep a record and never remove one.",
          "2. **Every pattern is word-anchored.** Three unanchored-substring bugs are already on this "
          "codebase's record (`hous` in C.2.c, `reproduc\\w+` in v1, a bare `429` matching a Unix "
          "timestamp in the transport layer).",
          "3. **Any rescue signal overrides any drop term**, because a wrongly-kept record costs one "
          "LLM read and a wrongly-dropped record costs the study. The rescue vocabulary is "
          "demographic and religious only — it contains no value-scale words, since `individualis` "
          "and `materialis` are exactly what OpenAlex stemming corrupts.", "",
          "## Terms proposed and refused, with the record that refused them", "",
          "Kept in the source so a later reader does not re-propose an exclusion this run already "
          "measured and rejected. The last row concerns the *rescue* list rather than the drop list.",
          "", "| proposed term | why it was refused | the record |", "|---|---|---|"]
    L += [f"| `{t}` | {why} | *{ex}* |" for t, why, ex in REJECTED_TERMS]
    L += ["", "## Per-term firing — what each term actually removed", "",
          "`rescued` counts records where the term fired but a demographic or religious signal kept "
          "the record anyway. **A term with a high rescue share is doing little work and carrying "
          "real risk.**", "",
          "| term | dropped | rescued | rescue share |", "|---|---|---|---|"]
    for t, n in term_fires.most_common():
        rs = rescue_saves.get(t, 0)
        share = f"{100 * rs / (n + rs):.0f}%" if (n + rs) else "—"
        L.append(f"| `{t}` | {n} | {rs} | {share} |")
    fired_only_rescued = [t for t in rescue_saves if t not in term_fires]
    if fired_only_rescued:
        L += ["", "Terms that fired but **never** caused a drop (every hit was rescued) — these are "
              "carrying no weight and are candidates for removal:", ""]
        L += [f"- `{t}` ({rescue_saves[t]} rescued)" for t in sorted(fired_only_rescued)]
    L += ["", "## Book reviews are a retrieval worklist, not a rejection class", "",
          "The first version of this filter sent all 262 book reviews to `OFF_OTHER`. Reading the "
          "rejected sample showed what that deletes — reviews of **Jones and Grupp, *Modernization, "
          "Value Change, and Fertility in the Soviet Union***, **Yaukey, *Fertility Differences in a "
          "Modernizing Country***, and **Fukuda, *Marriage and fertility behaviour in Japan — "
          "Economic status and value orientation***. Those are on-pair monographs and the review is "
          "the only trace of them the pull returned. **This chapter has hit an indexing gap on "
          "books, chapters, dissertations and non-English work five separate times**, so dropping "
          "the reviews thins the corpus in precisely the direction it is already weakest.", "",
          f"A review carrying a demographic or religious signal is therefore routed to "
          f"`BOOK_REVIEW_LEAD` — **{len(leads):,}** records. It is not evidence and does not go to "
          f"the screen; the *reviewed work* is what to chase. The remaining "
          f"{262 - len(leads) if len(leads) <= 262 else 0} carry no signal and drop.", "",
          "### The leads", ""]
    L += [f"- {(x.get('title') or '')[:150]}" for x in leads[:40]]
    if len(leads) > 40:
        L += [f"- … and {len(leads) - 40} more in `{os.path.basename(OUT_JSON)}`"]
    L += ["", "## What this filter does NOT do", "",
          "- It does not decide relevance. Everything it keeps still goes to the screen unjudged.",
          "- It does not touch title-only records. The rubric routes those to `UNCERTAIN`, and a "
          "record with no title is kept by default.",
          "- Drops are recorded with `prefilter_cell: OFF_OTHER` and the firing term, so the PRISMA "
          "count reconciles and any drop can be reversed by name.", ""]
    open(OUT_MD, "w").write("\n".join(L) + "\n")

    if audit:
        S = ["# D.1.a — pre-filter rejected sample, for reading before the filter ships", "",
             "The standing rule from the screen rubric: **any proposed exclusion gets a rejected "
             "sample read before it ships.** Aggregate counts have concealed two-directional errors "
             "on this chapter before — read the titles, not the totals.", ""]
        for t, n in term_fires.most_common():
            S += [f"## `{t}` — {n} dropped", ""]
            S += [f"- {x[:150]}" for x in per_term_samples.get(t, [])[:SAMPLE_PER_TERM]] + [""]
        S += ["---", "", "# Rescued records — the filter fired and kept them anyway", "",
              "These are the near-misses. If any of these is obviously clinical junk the rescue "
              "vocabulary is too broad; if any looks like a study, the rescue earned its place.", ""]
        for t, n in rescue_saves.most_common(25):
            S += [f"## RESCUED by a demographic signal after `{t}` fired — {n}", ""]
            S += [f"- {x[:150]}" for x in per_term_samples.get("RESCUED:" + t, [])[:6]] + [""]
        open(OUT_SAMPLE, "w").write("\n".join(S) + "\n")
        print(f"wrote {OUT_SAMPLE}", file=sys.stderr)

    print(f"in {len(records)} | kept {len(kept)} | dropped {len(dropped)} ({pct:.1f}%) | "
          f"gold tested {tested} lost {len(losses)}", file=sys.stderr)
    print(f"wrote {OUT_JSON}\nwrote {OUT_MD}", file=sys.stderr)
    if losses:
        print("GOLD LOSS -- acceptance gate FAILED, filter must not ship", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
