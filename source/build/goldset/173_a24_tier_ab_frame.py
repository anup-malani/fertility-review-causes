#!/usr/bin/env python3
"""
173_a24_tier_ab_frame.py — A.24 (dating apps and union-formation friction), stage A4.

Inherits `162_a12_tier_ab_frame.py` in its plumbing — retrieval, caching, the DOI-less seed recovery
with its inverted type restriction, the first-author gate and its self-test, and the discipline that
a failed request is UNCONFIRMED rather than zero. What changes is the diagnostic vocabulary, which is
chapter-specific by construction, and one measurement that A.12 did not need.

WHAT THIS RUN IS FOR. Tier A is the 25 anchors A3 resolved; Tier B is their one-hop citation
neighbourhood, backward and forward. The frame is what the production query will later be measured
against, so every fraction below is computed AFTER retrieval and none is applied as a filter —
filtering the forward fetch by topic vocabulary would prune Tier B by distance from the production
query and make Recall(B) circular.

THE MEASUREMENT THIS CHAPTER NEEDS AND A.12 DID NOT: WALL 9'S COST, STATED AS A FRACTION.
The scope declares Wall 9 unenforceable — the only identified estimates A.24 can reach (Bellou 2014,
Billari-Giuntella-Stella 2019, Kalabikhina et al. 2020) are published under technology-diffusion
vocabulary and never say "dating app" in a title or abstract. That is an assertion until someone
measures it. So this run reports, for the three `SECONDARY_TECH_*` seeds, the share of their forward
clouds that carries an OUTCOME (union formation or fertility) but NO app vocabulary. That share IS
the bypass's addressable population, and its size decides whether the bypass is worth building or
whether the chapter should say plainly that its identified evidence cannot be screened for.

The bypass is gated on SEED PROVENANCE plus an outcome term, with NO dating-vocabulary requirement.
A.12 established why in one run: the first version of its Wall 8 bypass required a twinning term
alongside the design vocabulary and recovered 4 records; re-gated on provenance it recovered 212. A
recovery gated on the vocabulary its own wall calls invisible re-imposes the assumption the wall
denies.

RECALL(A) IS REPORTED TWICE, AND THE GAP IS THE POINT. The causal denominator is 8 empirical anchors
(`PRIMARY_APP_*` + `SECONDARY_TECH_*`); the screenable denominator is the 5 `PRIMARY_APP_*` anchors
a title/abstract screen could actually reach. Recall(A) against 8 will look poor by construction.
Both numbers get reported, and the difference is the price of the unenforceable wall rather than a
screen failure.

A NOTE ON `PRIMARY_APP_FERTILITY`, WHICH HAS NO ANCHOR. The recon probe found eleven records at
dating-app exposure against a population fertility quantity and not one is an estimate, so the cell
the registry entry is actually about seeds nothing. It stays in the cell vocabulary with a
denominator of zero. A frame that quietly drops an empty cell cannot later show that it was empty.

HOMONYM CARVE-OUTS REST ON EXACT COUNTS, NEVER ON A SAMPLE. Geochronological "dating" is 64,276
records on the explicit vocabulary and agronomic "fertility" reached the head of two recon probes.
Both are frozen as PURE HOMONYMS rather than boundary cases, which is this chapter's one carve-out
from the standing rule that a decoy cloud is a boundary case worth seeding in full. A capped pull
cannot justify that carve-out — a truncated OpenAlex pull is the high-citation HEAD, not a random
sample — so each homonym seed also carries an EXACT outcome rate from two count-only queries over
its entire cloud. Extended here beyond A.12: ANY seed whose pull truncates gets the exact rate, not
only the homonym ones, because the sampling objection applies to every cap and not just to the ones
we chose to be suspicious of.

THE VIOLENCE DECOY IS THE CLOUD HEAD, NOT THE SEAM, AND IS SEEDED IN FULL ANYWAY. Krug et al. 2002
anchors a 43,963-record intimate-partner-violence literature that shares this chapter's word "dating"
in the SAME sense — courtship — and differs only in outcome. It is not a homonym and gets no
carve-out: it takes an ordinary forward cap and its yield is measured like any other boundary case.
The genuine Wall 3 seam is the 66 records where dating-violence and dating-app vocabulary meet, and
those are adjudicated at the screen.

Standing discipline, unchanged: OpenAlex is called with the funded api_key from .env; an empty result
is never cached; commas never appear inside a filter VALUE (fatal, and percent-encoding does not save
it); no `?` reaches a search value (wildcard); a phrase never opens with not/and/or (parsed as a
boolean operator, and the enclosing AND then returns the UNRESTRICTED count).

SCRIPT NUMBERING: 172 is the highest in use on any branch, local or remote. This is 173.

Output: literature/search-logs/{slug}-tier-a.json
        literature/search-logs/{slug}-tier-b-frame.json
        literature/search-logs/{slug}-tier-ab-log.md
"""
import json, os, re, subprocess, sys, time
from urllib.parse import quote

SLUG = "dating-apps-union-formation-friction"
MAILTO = "shravanh@uchicago.edu"
UA = f"fertility-review/1.0 (mailto:{MAILTO})"
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
LOGS = os.path.join(ROOT, "literature", "search-logs")
ANCHORS = os.path.join(LOGS, f"{SLUG}-cold-start-anchors.json")
OUT_A = os.path.join(LOGS, f"{SLUG}-tier-a.json")
OUT_B = os.path.join(LOGS, f"{SLUG}-tier-b-frame.json")
OUT_LOG = os.path.join(LOGS, f"{SLUG}-tier-ab-log.md")
CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "a24_frame_cache.json")
cache = json.load(open(CACHE)) if os.path.exists(CACHE) else {}

FORWARD_CAP = 5000          # per-seed budget control, NOT a judgement about the seed
PAGE = 200
SELECT = ("id,doi,display_name,publication_year,cited_by_count,type,authorships,"
          "primary_location,referenced_works,abstract_inverted_index")

# --------------------------------------------------------------------------------------------
# DIAGNOSTIC VOCABULARY. Every list below is used ONLY to compute reported fractions per seed. If
# any of them ever feeds a filter, the Recall(B) it produces is circular. All are LOWER BOUNDS: a
# record counts only when it names the thing in its title or abstract.
# --------------------------------------------------------------------------------------------

# EXPOSURE AXIS. The vocabulary Wall 9 says the identified literature does not carry.
#
# MATCHED WITH A WORD BOUNDARY, not as a bare substring, and the first run of this script is why.
# Under substring matching `"dating app"` fired on NINE records inside the geochronology cloud — all
# of them "luminescence dating applications" — inflating the app axis in the one cloud whose whole
# purpose is to have a zero there. It is the unanchored-pattern bug this codebase has now hit six
# times, and it is worse here than usual because it fires INSIDE a decoy family, where a small
# false-positive rate is read as evidence that the carve-out is unsafe.
#
# The other term blocks below stay on substring matching deliberately: their entries are either long
# phrases or intentional stems ("geochronolog", "agronom", "abusive"), where a boundary would break
# the match rather than sharpen it.
APP_RX = re.compile(
    r"dating apps?\b|online dating|internet dating|mobile dating|dating websites?\b"
    r"|dating sites?\b|dating platforms?\b|dating service|\btinder\b|\bgrindr\b|\bbumble\b"
    r"|\bokcupid\b|\bswip(?:e|es|ed|ing)\b|online daters?\b|met online|matchmaking")

# OUTCOME AXIS, LIMB 1 — union formation. This is the outcome A.24's reachable link actually has.
UNION_TERMS = ("union formation", "partner formation", "couple formation", "relationship formation",
               "marriage", "married", "marital", "cohabit", "partnership", "repartner",
               "family formation", "singlehood", "unpartnered", "divorce", "breakup", "break-up",
               "relationship dissolution", "romantic relationship", "pair bond", "mate selection")

# OUTCOME AXIS, LIMB 2 — fertility. Kept SEPARATE from limb 1 rather than merged, because the whole
# argument of this chapter is that the literature reaches limb 1 and stops. Merging them would hide
# the very gap the chapter exists to report.
FERT_TERMS = ("fertility", "birth rate", "births", "childbearing", "number of children",
              "childless", "total fertility", "completed fertility", "transition to parenthood",
              "fecundity", "birth intention", "family size", "parenthood")

# THE WALL 9 CHANNEL. Technology diffusion — the exposure the identified estimates actually use.
TECH_TERMS = ("broadband", " 3g", " 4g", "smartphone", "mobile phone", "internet access",
              "high-speed internet", "high speed internet", "internet diffusion", "cellular data",
              "mobile broadband", "internet use", "digital technology", "information technology")

# GEOCHRONOLOGY (Wall 1). A pure homonym: "dating" as a laboratory method.
GEOCHRON_TERMS = ("radiocarbon", "radiometric dating", "luminescence dating", "geochronolog",
                  "dendrochronolog", "stratigraph", "holocene", "pleistocene", "zircon", "u-pb",
                  "carbon dating", "quaternary", "sediment", "archaeolog", "paleo", "palaeo")

# DATING VIOLENCE / IPV (Wall 3). NOT a homonym — the same word sense, a different outcome — which
# is why it takes an ordinary cap and an ordinary routing decision.
VIOLENCE_TERMS = ("dating violence", "intimate partner violence", "dating abuse", "sexual coercion",
                  "sexual assault", "victimization", "victimisation", "perpetration", "harassment",
                  "stalking", "abusive", "gender-based violence")

# SEXUAL HEALTH (Wall 5). A fifth of the dating-app literature by the recon counts, so this wall
# does more work than any other outcome wall in the chapter.
SEXHEALTH_TERMS = ("hiv", "sexually transmitted", "condom", "syphilis", "gonorrh", "chlamyd",
                   "sexual risk", "casual sex", "hookup", "hook-up", "men who have sex with men",
                   "sexual health", "pre-exposure prophylaxis", "unprotected sex")

# PLATFORM ENGINEERING (Wall 4). The wall is cut on OUTCOME, not on venue, so this diagnostic is
# deliberately NOISY — it measures how much engineering vocabulary sits in a neighbourhood, which is
# exactly what cannot by itself decide the wall. A.12's Wall 6 established the lesson: an include-side
# anchor and an exclude-side anchor can carry the same neighbourhood vocabulary and differ only in
# what they report.
PLATFORM_TERMS = ("recommender", "recommendation algorithm", "machine learning", "deep learning",
                  "user engagement", "click-through", "platform design", "neural network",
                  "collaborative filtering", "a/b test", "field experiment on the platform")

# NON-HUMAN / AGRONOMIC FERTILITY (Wall 2). "Fertility" in the soil sense reached the head of two
# recon probes, including one restricted to dating-app vocabulary.
NONHUMAN_TERMS = ("soil fertility", "agronom", "fertilizer", "fertiliser", "biofertil", " crop ",
                  "livestock", "bovine", "ovine", " ewe", " cattle", "dairy", "maize", "rhizobact",
                  "nitrogen")

errors = []


FORWARD_CAP = 5000          # per-seed budget control, NOT a judgement about the seed
PAGE = 200
SELECT = ("id,doi,display_name,publication_year,cited_by_count,type,authorships,"
          "primary_location,referenced_works,abstract_inverted_index")

# On-topic diagnostic vocabulary. Used ONLY to compute reported fractions per seed. If any of these
# lists ever feeds a filter, the Recall(B) it produces is circular.
# Kept deliberately narrow: it asks what share of a seed's citation cloud carries a FERTILITY QUANTITY
# at all. A broader list would score the demographic seeds near 100% and stop discriminating.
TOPIC_TERMS = ("fertility", "birth rate", "births", "childbearing", "family size", "parity",
               "total fertility", "completed fertility", "cohort fertility", "childless",
               "fecundity", "birth interval", "sibship")

# TWINNING diagnostic — the mechanism leg. Jointly with TOPIC_TERMS it gives the density of A.12's
# actual primary cell. Deliberately includes the clinical vocabulary ("multiple gestation") as well
# as the demographic ("twinning rate"), because the estimand can be reported in either register and a
# diagnostic restricted to demographic wording would measure the venue rather than the construct.
TWIN_TERMS = ("twin", "twinning", "multiple birth", "multiple births", "multiple pregnanc",
              "multiple gestation", "multiple delivery", "multiple deliveries", "dizygotic",
              "monozygotic", "higher order multiple", "triplet", "quadruplet")

# HOMONYM diagnostic (Walls 1-2). Crystallographic twinning and TWinning-Induced Plasticity steel.
# The scope froze these as PURE HOMONYMS rather than boundary cases; this measures whether that is
# true instead of asserting it. Space-padded terms match at string edges — see _blob.
HOMONYM_TERMS = ("crystallograph", "crystal structure", "lattice", "shelx", "diffract",
                 "space group", "martensit", "austenit", "twip", "trip steel", "digital twin",
                 "microstructur", "dislocation", "refinement", " alloy", "stacking fault")

# NON-HUMAN diagnostic (Wall 3). Veterinary and agronomic reproduction, where "twinning" and
# "fertility" both carry their ordinary meanings but the species is wrong. A LOWER BOUND: a paper
# counts only when it names a species or an animal-science outcome.
NONHUMAN_TERMS = (" ewe", " ewes", " lamb", "ovine", "caprine", "bovine", " cattle", " cow ",
                  " cows", "heifer", " sow ", " sows", " goat", " mare", " calf", " calves",
                  "dairy", "litter size", "lambing", "soil fertility", "agronom", "livestock")

# CLINICAL-OUTCOME diagnostic (Walls 5-6). THE diagnostic this chapter turns on. The Wall 6 re-cut
# admits a transfer-protocol study when its outcome is a POPULATION multiple-birth rate and excludes
# it when the outcome is per-cycle or perinatal. That re-cut is only defensible if outcome type is
# visible at title/abstract, and this measures whether it is. A LOWER BOUND, for the same reason as
# the species floor: a paper counts only when it names such an outcome. Note "live birth rate" is
# here and "births" is in TOPIC_TERMS — a paper CAN carry both, and treating them as exclusive would
# understate the floor. The screen, not this diagnostic, adjudicates a paper carrying one of each.
CLINICAL_TERMS = ("preterm", "birth weight", "birthweight", "neonatal", "perinatal mortality",
                  "perinatal outcome", "gestational age", "ohss", "ovarian hyperstimulation",
                  "embryo transfer", "live birth rate", "pregnancy rate", "implantation rate",
                  "cumulative live birth", "caesarean", "cesarean", "nicu", "morbidity",
                  "stillbirth", "low birth weight")

errors = []
errors = []


def openalex_key():
    k = os.environ.get("OPENALEX_API_KEY")
    if k:
        return k.strip()
    envp = os.path.join(ROOT, ".env")
    if os.path.exists(envp):
        for line in open(envp):
            if line.startswith("OPENALEX_API_KEY="):
                return line.split("=", 1)[1].strip()
    return ""


OA_KEY = openalex_key()


def oa_get(url, tag, tries=3):
    """Returns (payload, ok). A transport failure is NOT an empty result: the caller must be able to
    tell 'the index holds nothing' from 'the request did not complete', or the frame quietly shrinks
    and Recall(B) is computed against a denominator that lost records to network errors."""
    full = url + (f"&api_key={OA_KEY}" if OA_KEY else f"&mailto={MAILTO}")
    for attempt in range(tries):
        r = subprocess.run(["curl", "-s", "-m", "60", "-A", UA, full], capture_output=True, text=True)
        if r.returncode == 0:
            try:
                d = json.loads(r.stdout)
                if "results" in d or "id" in d:
                    return d, True
            except Exception:
                pass
        time.sleep(1.5 * (attempt + 1))
    errors.append((tag, url.split("filter=")[-1][:90]))
    return {}, False


def unabstract(inv):
    if not inv:
        return ""
    try:
        pos = [(i, w) for w, idxs in inv.items() for i in idxs]
        return " ".join(w for _, w in sorted(pos))[:1200]
    except Exception:
        return ""


def row(w):
    loc = (w.get("primary_location") or {}).get("source") or {}
    return {"id": (w.get("id") or "").rsplit("/", 1)[-1],
            "doi": (w.get("doi") or "").replace("https://doi.org/", "") or None,
            "title": w.get("display_name") or "",
            "year": w.get("publication_year"),
            "cited_by_count": w.get("cited_by_count"),
            "type": w.get("type"),
            "venue": loc.get("display_name") or "",
            "authors": [a["author"]["display_name"] for a in (w.get("authorships") or [])][:6],
            "abstract": unabstract(w.get("abstract_inverted_index"))}


def _blob(rec):
    # Padded so the space-anchored terms (" 3g", " ewe") can match at the string edges. Those terms
    # carry their spaces deliberately: a bare "3g" substring matches "3gpp" and "log3g", and a bare
    # "ewe" matches "between" — the unanchored-pattern bug this codebase has now hit five times.
    return " " + (rec["title"] + " " + rec.get("abstract", "")).lower() + " "


def has_app(rec):
    """Carries dating-app / online-dating vocabulary. The EXPOSURE axis, and the one Wall 9 says the
    identified literature does not carry. Word-boundary matched — see APP_RX."""
    return bool(APP_RX.search(_blob(rec)))


def has_union(rec):
    """Carries a union-formation construct."""
    return any(t in _blob(rec) for t in UNION_TERMS)


def has_fert(rec):
    """Carries a fertility quantity."""
    return any(t in _blob(rec) for t in FERT_TERMS)


def has_outcome(rec):
    """Either limb of the outcome axis. Kept as a disjunction of two SEPARATELY reported limbs
    because this chapter's finding is that the literature reaches unions and stops short of births;
    a merged outcome axis would conceal exactly that."""
    return has_union(rec) or has_fert(rec)


def in_primary_cell(rec):
    """Exposure AND outcome — the density of A.24's reachable cell in a seed's neighbourhood.

    A LOOSE UPPER BOUND. Co-occurrence of app vocabulary and an outcome word in one abstract is not a
    study that estimates one against the other, and for this chapter the co-occurrence is especially
    cheap: a paper about self-presentation on Tinder that mentions "romantic relationship" in its
    framing counts here and estimates nothing."""
    return has_app(rec) and has_outcome(rec)


def has_tech(rec):
    """Carries technology-diffusion vocabulary — the channel the identified estimates run on."""
    return any(t in _blob(rec) for t in TECH_TERMS)


def wall9_shape(rec):
    """THE WALL 9 BYPASS POPULATION, measured rather than asserted.

    A record with a technology exposure and an outcome, carrying NO app vocabulary at all: exactly
    the shape of Bellou 2014, Billari et al. 2019 and Kalabikhina et al. 2020, and exactly what a
    title/abstract screen built on the app axis cannot see. The bypass admits on this shape plus seed
    provenance, and deliberately NOT on app vocabulary — requiring the wall's own vocabulary to find
    the population the wall calls invisible is the self-defeating gate A.12 measured at 4 records
    against 212."""
    return has_tech(rec) and has_outcome(rec) and not has_app(rec)


def off_geochron(rec):
    """Visibly geochronological — "dating" as a laboratory method. LOWER BOUND."""
    return any(t in _blob(rec) for t in GEOCHRON_TERMS)


def off_violence(rec):
    """Visibly a violence/abuse outcome. Same word sense as the target, different outcome."""
    return any(t in _blob(rec) for t in VIOLENCE_TERMS)


def off_sexhealth(rec):
    """Visibly a sexual-health or STI-risk outcome."""
    return any(t in _blob(rec) for t in SEXHEALTH_TERMS)


def off_platform(rec):
    """Visibly platform-engineering vocabulary. Deliberately noisy — see the term block."""
    return any(t in _blob(rec) for t in PLATFORM_TERMS)


def off_nonhuman(rec):
    """Visibly agronomic or veterinary. LOWER BOUND."""
    return any(t in _blob(rec) for t in NONHUMAN_TERMS)


def exact_outcome_rate(seed_id, human_anchored=False):
    """EXACT forward outcome rate from two count-only queries — no sampling, no cap, 2 requests.

    Used for the homonym seeds, where a capped pull would force a carve-out to rest on a sample that
    cursor paging cannot make representative, and — extended beyond A.12 — for ANY seed whose pull
    truncated, because the sampling objection applies to every cap and not only to the caps we chose
    to distrust. Returns (n_on_outcome, total) or (None, None) on failure: a failed request is
    UNCONFIRMED, never zero.

    `human_anchored` drops the bare word "fertility" and asks only for terms that cannot mean
    anything but a human demographic outcome. THE FIRST RUN OF THIS SCRIPT IS WHY IT EXISTS. The
    agronomic seed returned an exact on-outcome rate of 16.8%, which under the rule written into this
    script would REFUTE the Wall 2 carve-out and force an uncapped re-pull. It refutes nothing: the
    ordinary list contains "fertility", and in a biofertilizer cloud "fertility" means SOIL
    fertility. The 16.8% is the wall's own justification being scored as evidence against the wall.
    A homonym family that shares a word with the outcome axis cannot be measured with a vocabulary
    that contains that word, so both rates are computed and both are reported.

    The phrase list carries NO commas (fatal inside a filter value, and %2C does not save it), no
    `?` (wildcard), and no phrase opening with a boolean word.
    """
    plain = ("fertility", "birth rate", "births", "childbearing", "marriage",
             "cohabitation", "union formation", "family formation", "divorce",
             "romantic relationship")
    human = ("birth rate", "total fertility rate", "completed fertility", "childbearing",
             "marriage", "cohabitation", "union formation", "family formation", "divorce",
             "romantic relationship", "childlessness")
    terms = " OR ".join(f'"{t}"' for t in (human if human_anchored else plain))
    d1, ok1 = oa_get(f"https://api.openalex.org/works?filter=cites:{seed_id}&per-page=1",
                     f"exact-total:{seed_id}")
    d2, ok2 = oa_get(f"https://api.openalex.org/works?filter=cites:{seed_id},"
                     f"title_and_abstract.search:{quote(chr(40) + terms + chr(41))}&per-page=1",
                     f"exact-outcome:{seed_id}")
    if not (ok1 and ok2):
        return None, None
    return (d2.get("meta", {}).get("count"), d1.get("meta", {}).get("count"))


def work_by_doi(doi):
    key = f"W::{doi}"
    if key in cache:
        return cache[key]
    d, ok = oa_get(f"https://api.openalex.org/works/https://doi.org/{quote(doi)}?select={SELECT}",
                   f"work:{doi}")
    if not ok or not d.get("id"):
        return None
    cache[key] = {"row": row(d), "referenced_works": [r.rsplit("/", 1)[-1]
                                                      for r in (d.get("referenced_works") or [])]}
    json.dump(cache, open(CACHE, "w"), indent=0)
    return cache[key]


def fetch_ids(ids):
    """Batch-hydrate OpenAlex ids, 50 per request via the pipe-OR filter."""
    out, todo = [], [i for i in ids if f"R::{i}" not in cache]
    for i in range(0, len(todo), 50):
        chunk = todo[i:i + 50]
        d, ok = oa_get(f"https://api.openalex.org/works?filter=openalex_id:{'|'.join(chunk)}"
                       f"&per-page=50&select={SELECT}", f"hydrate:{chunk[0]}")
        if not ok:
            continue
        for w in d.get("results", []):
            r = row(w)
            cache[f"R::{r['id']}"] = r
        json.dump(cache, open(CACHE, "w"), indent=0)
        time.sleep(0.2)
    for i in ids:
        if f"R::{i}" in cache:
            out.append(cache[f"R::{i}"])
    return out


def citing(seed_id, cap):
    """Forward citations, cursor-paged. Returns (rows, total, truncated)."""
    key = f"C::{seed_id}::{cap}"
    if key in cache:
        return cache[key]["rows"], cache[key]["total"], cache[key]["truncated"]
    rows, cursor, total = [], "*", None
    while cursor and len(rows) < cap:
        d, ok = oa_get(f"https://api.openalex.org/works?filter=cites:{seed_id}"
                       f"&per-page={PAGE}&cursor={cursor}&select={SELECT}", f"cites:{seed_id}")
        if not ok:
            break
        total = d.get("meta", {}).get("count", total)
        rows += [row(w) for w in d.get("results", [])]
        cursor = d.get("meta", {}).get("next_cursor")
        time.sleep(0.15)
    truncated = bool(total and len(rows) < total)
    cache[key] = {"rows": rows, "total": total, "truncated": truncated}
    json.dump(cache, open(CACHE, "w"), indent=0)
    return rows, total, truncated


BOOKISH = {"book", "monograph", "edited-book", "reference-book"}


def _fold(x):
    import unicodedata as _u
    x = (x or "").translate(str.maketrans({"ø": "o", "ł": "l", "ı": "i", "ß": "ss", "æ": "ae",
                                           "đ": "d", "þ": "th", "ð": "d"}))
    x = _u.normalize("NFKD", x).encode("ascii", "ignore").decode("ascii").lower()
    # INHERITED BUG, FIXED HERE (A.12, 2026-08-22). The inherited line was
    #     " ".join(c for c in x if c.isalnum() or c == " ")
    # which joins CHARACTERS with spaces, shattering every name into single letters: "Wilson"
    # became "w i l s o n". `_surname()` then took the last token and returned the last LETTER of a
    # name, so the A4 first-author gate compared final letters and matched any two names ending in
    # the same one. Introduced at D.3.c (150) and never exercised elsewhere; see the log for the
    # blast-radius audit. Distinct from the A3 norm() accent-shattering bug — a different function
    # with a different defect in the same family, which is why fixing one did not fix the other.
    x = "".join(c if (c.isalnum() or c == " ") else " " for c in x)
    return " ".join(x.split())


def _name_tokens(n):
    """ALL tokens of a name, folded. Replaces the inherited last-token-only `_surname()`.

    The inherited version assumed "Given ... Surname" order and took the final token. OpenAlex renders
    Bronars & Grogger's first author as **"Bronars Sg"** — surname first, initials last — so the last
    token is `"sg"`, which matches no candidate surname, and the gate refused a correct record and
    with it the whole twin-IV forward channel that Wall 8 makes irreplaceable.

    Testing the full token set instead does not weaken what the gate is for. The gate exists to refuse
    a record whose first author is a DIFFERENT PERSON — a reviewer, typically — and a different
    person's name shares no token with our authors' surnames. Scott reviewing Wilson still fails;
    "Bronars Sg" passes on the token `bronars`. Same family as the norm()-shatters-accents finding:
    a name-handling assumption that is silently wrong produces a CONFIDENT wrong negative, not a
    missing-data None."""
    return {t for t in _fold(n).split() if t}


def _first_author_ok(rec_authors, cand_authors):
    """First-position author must share a token with one of the candidate's names."""
    if not rec_authors:
        return False                                   # no metadata is not agreement
    cand = set()
    for c in cand_authors:
        cand |= _name_tokens(c)
    return bool(_name_tokens(rec_authors[0]) & cand)


_GATE_SELFTEST = [
    # (record first author, candidate authors, must_pass) — both directions, real cases.
    ("Bronars Sg", ["Stephen G. Bronars", "Jeff Grogger"], True),      # degraded surname-first metadata
    ("Joyce A Martin", ["Joyce A. Martin", "Brady E. Hamilton"], True),
    ("M. G. Bulmer", ["M. G. Bulmer"], True),
    ("Daryl Michael Scott", ["William Julius Wilson"], False),         # reviewer, must still fail
    ("Kurt Benirschke", ["M. G. Bulmer"], False),                      # reviewer of Bulmer
    ("", ["M. G. Bulmer"], False),                                     # no metadata is not agreement
]


def gate_selftest():
    bad = []
    for ra, ca, want in _GATE_SELFTEST:
        got = _first_author_ok([ra] if ra else [], ca)
        if got != want:
            bad.append((ra, ca, want, got))
    if bad:
        sys.stderr.write("ABORT: first-author gate self-test failed:\n")
        for ra, ca, want, got in bad:
            sys.stderr.write(f"  {ra!r} vs {ca!r}: expected {want}, got {got}\n")
        sys.exit(1)


def _filter_safe(v):
    """Make a string safe to use as an OpenAlex FILTER VALUE.

    A COMMA IN A FILTER VALUE IS FATAL, AND PERCENT-ENCODING DOES NOT SAVE IT. Commas separate
    filters, and the API edge splits on them AFTER decoding, so `quote()` turning "," into "%2C" is
    undone before the split happens. The request is rejected outright:

        {"error": "Invalid request rejected at the API edge",
         "message": "A filter value contains an unescaped comma. Commas separate filters, so a
                     literal comma inside a value must be percent-encoded as %2C (or the whole
                     value wrapped in double quotes)."}

    — advice which, for the percent-encoding half, does not work. Found on Martin, Hamilton &
    Osterman 2012, *Three decades of twin births in the United States, 1980-2009*, whose recovery
    request failed on the first A4 run and, per the refusals-are-not-zeros rule, had to be retried
    rather than recorded as an unrecoverable anchor.

    THIS HAZARD IS SPECIFIC TO `filter=title.search:`. The A3 resolver (161) is NOT affected: it
    queries through `search=`, a top-level query parameter where a comma is an ordinary character,
    which is why A.12's several comma-bearing anchor titles all resolved at A3 and only the A4
    recovery broke. Same family as the wildcard refusal and the stopword collapse: a query-language
    rule that turns a well-formed request into a rejection the caller reads as an empty literature.

    Commas are dropped rather than the value being quoted, because quoting turns `title.search` into
    a phrase match and would interact with stopword-dropping. The comma carries no retrieval signal
    and the first-author and year gates do the discriminating."""
    return re.sub(r"\s+", " ", (v or "").replace(",", " ")).strip()


def recover_seed_id(title, authors, year, is_book):
    """ONE recovery attempt for an anchor A3 could not give a DOI, gated by first-author agreement.

    GENERALISED BEYOND MONOGRAPHS (A.12, 2026-08-22). The inherited version fired only for `is_book`
    anchors and restricted to bookish types. A.12 has three DOI-less anchors and only one is a book;
    the other two are an AER article and an NCHS vital-statistics report. Losing the AER one —
    Bronars & Grogger, a twin-IV canon seed — would delete the ONLY channel to
    `PRIMARY_OFFSET_FIRSTSTAGE`, because Wall 8 says those first stages cannot be reached by
    screening. The type restriction is therefore INVERTED for non-books rather than dropped: a book
    must resolve to a bookish record and a non-book must not, so a monograph still cannot be seeded
    from a journal review of itself.

    Returns (openalex_id, matched_title, cites) or (None, reason, None). Never guesses."""
    short = _filter_safe(title.split(":")[0])
    d, ok = oa_get(f"https://api.openalex.org/works?filter=title.search:{quote(short)}"
                   f"&per-page=10&select={SELECT}", f"recover:{short[:30]}")
    if not ok:
        return None, "request failed (UNCONFIRMED, not absent)", None
    cands = []
    for w in d.get("results", []):
        t = (w.get("type") or "")
        if is_book and t not in BOOKISH:
            continue
        if (not is_book) and t in BOOKISH:
            continue
        au = [a["author"]["display_name"] for a in (w.get("authorships") or [])]
        if not _first_author_ok(au, authors):
            continue
        if year and w.get("publication_year") and abs(w["publication_year"] - year) > 1:
            continue
        cands.append(w)
    if not cands:
        return None, ("no bookish record with first-author agreement" if is_book
                      else "no non-bookish record with first-author agreement"), None
    best = max(cands, key=lambda w: w.get("cited_by_count") or 0)
    return ((best.get("id") or "").rsplit("/", 1)[-1], best.get("display_name") or "",
            best.get("cited_by_count"))


HOMONYM_CAP = 1000          # measure, do not cover — see the docstring. Reported, never silent.


def main():
    gate_selftest()             # the first-author gate must survive degraded metadata AND still refuse reviewers
    anchors = json.load(open(ANCHORS))
    verified = [a for a in anchors if a.get("identity_verified") and a.get("doi")]

    # The causal recall denominator, reported two ways. `PRIMARY_APP_*` is what a title/abstract
    # screen built on the app axis can reach; `SECONDARY_TECH_*` is the identified evidence Wall 9
    # declares invisible to that screen. Both estimate relationships this chapter grades, so both
    # belong in a CAUSAL denominator — and reporting only the first would quietly define the
    # unenforceable wall out of existence.
    EMPIRICAL_CELLS = {"PRIMARY_APP_UNION", "PRIMARY_APP_FERTILITY",
                       "SECONDARY_TECH_UNION", "SECONDARY_TECH_FERTILITY"}
    SCREENABLE_CELLS = {"PRIMARY_APP_UNION", "PRIMARY_APP_FERTILITY"}
    HOMONYM_CELLS = {"OFF_HOMONYM_GEOCHRON", "OFF_NONHUMAN"}
    TECH_CELLS = {"SECONDARY_TECH_UNION", "SECONDARY_TECH_FERTILITY"}

    def is_empirical_anchor(rec):
        return rec["provisional_cell"] in EMPIRICAL_CELLS

    def is_screenable_anchor(rec):
        return rec["provisional_cell"] in SCREENABLE_CELLS

    # Every DOI-less anchor gets ONE gated recovery attempt, books and non-books alike. Reported
    # either way: an anchor that cannot seed is a hole in the frame and must be visible as one.
    recovery_report = []
    for a in anchors:
        if a.get("doi"):
            continue
        rid, note, cites = recover_seed_id(a["title"], a.get("authors") or [], a.get("year"),
                                           bool(a.get("is_book")))
        recovery_report.append((a["title"][:56], bool(a.get("is_book")), rid, note, cites))
        if rid:
            a["openalex_id_recovered"] = rid
            a["recovered_title"] = note
            a["recovered_cites"] = cites

    tier_a, seedinfo = [], []
    for a in verified + [x for x in anchors if x.get("openalex_id_recovered")]:
        w = work_by_doi(a["doi"]) if a.get("doi") else None
        if not w and a.get("openalex_id_recovered"):
            got = fetch_ids([a["openalex_id_recovered"]])
            if not got:
                continue
            d, ok = oa_get(f"https://api.openalex.org/works/{a['openalex_id_recovered']}"
                           f"?select={SELECT}", f"seed:{a['openalex_id_recovered']}")
            w = {"row": got[0], "referenced_works": [r.rsplit("/", 1)[-1] for r in
                                                     (d.get("referenced_works") or [])]} if ok else None
        if not w:
            continue
        rec = dict(a)
        rec["openalex_id"] = w["row"]["id"]
        rec["n_referenced"] = len(w["referenced_works"])
        rec["cited_by_count"] = w["row"]["cited_by_count"]
        tier_a.append(rec)
        seedinfo.append((rec, w))
    json.dump(tier_a, open(OUT_A, "w"), indent=2)

    pool, log_rows = {}, []
    for rec, w in seedinfo:
        sid = rec["openalex_id"]
        cell = rec["provisional_cell"]
        is_emp = is_empirical_anchor(rec)
        is_hom = cell in HOMONYM_CELLS
        is_tech = cell in TECH_CELLS
        back = fetch_ids(w["referenced_works"])
        # Empirical seeds are the recall spine and get an unbounded pull. The two homonym decoys get
        # a low cap because the scope froze them as pure homonyms rather than boundary cases — and
        # they get an EXACT rate as well, so the carve-out rests on a number. Every other decoy,
        # including the 8,514-cite violence cloud, takes the ordinary forward cap and is treated as
        # the boundary case it is.
        cap = 10 ** 6 if is_emp else (HOMONYM_CAP if is_hom else FORWARD_CAP)
        fwd, total, truncated = citing(sid, cap)
        n = len(fwd)
        f_app = (sum(1 for r in fwd if has_app(r)) / n) if n else None
        f_union = (sum(1 for r in fwd if has_union(r)) / n) if n else None
        f_fert = (sum(1 for r in fwd if has_fert(r)) / n) if n else None
        f_out = (sum(1 for r in fwd if has_outcome(r)) / n) if n else None
        n_prim = sum(1 for r in fwd if in_primary_cell(r))
        f_prim = (n_prim / n) if n else None
        n_w9 = sum(1 for r in fwd if wall9_shape(r))
        f_w9 = (n_w9 / n) if n else None
        f_geo = (sum(1 for r in fwd if off_geochron(r)) / n) if n else None
        f_vio = (sum(1 for r in fwd if off_violence(r)) / n) if n else None
        f_sex = (sum(1 for r in fwd if off_sexhealth(r)) / n) if n else None
        f_plat = (sum(1 for r in fwd if off_platform(r)) / n) if n else None
        f_non = (sum(1 for r in fwd if off_nonhuman(r)) / n) if n else None
        # Exact rate for the homonym seeds AND for anything truncated. A.12 computed it only for the
        # homonyms; the sampling objection applies to every cap, so the trigger is widened here.
        exact_n, exact_tot = (exact_outcome_rate(sid) if (is_hom or truncated) else (None, None))
        # A homonym family that shares a word with the outcome axis cannot be measured with a
        # vocabulary containing that word. Both rates are computed for those seeds and both reported.
        exact_h, exact_ht = (exact_outcome_rate(sid, human_anchored=True) if is_hom else (None, None))
        for r in back:
            pl = pool.setdefault(r["id"], {**r, "seed_ids": [], "channels": set()})
            pl["seed_ids"].append(sid); pl["channels"].add("backward")
        for r in fwd:
            pl = pool.setdefault(r["id"], {**r, "seed_ids": [], "channels": set()})
            pl["seed_ids"].append(sid); pl["channels"].add("forward")
        log_rows.append(dict(title=rec["title"][:52], cell=cell, seed=sid, empirical=is_emp,
                             homonym=is_hom, tech=is_tech, n_back=len(back), n_fwd=n,
                             fwd_total=total, truncated=truncated, app=f_app, union=f_union,
                             fert=f_fert, outcome=f_out, primary=f_prim, n_primary=n_prim,
                             wall9=f_w9, n_wall9=n_w9, geo=f_geo, vio=f_vio, sex=f_sex,
                             plat=f_plat, nonhuman=f_non,
                             exact_outcome=exact_n, exact_total=exact_tot,
                             exact_human=exact_h, exact_human_total=exact_ht))
        print(f"  {cell[:26]:<26} back={len(back):>4} fwd={n:>5}/{total or 0:<6} "
              f"app={f'{f_app:.0%}' if f_app is not None else 'n/a':>4} "
              f"out={f'{f_out:.0%}' if f_out is not None else 'n/a':>4} "
              f"BOTH={f'{f_prim:.1%}' if f_prim is not None else 'n/a':>5}({n_prim:>4}) "
              f"W9={f'{f_w9:.0%}' if f_w9 is not None else 'n/a':>4}({n_w9:>4})  {rec['title'][:28]}")

    anchor_ids = {r["openalex_id"] for r in tier_a}
    tier_b = []
    for rid, pl in pool.items():
        if rid in anchor_ids:
            continue
        pl["channels"] = sorted(pl["channels"])
        pl["seed_ids"] = sorted(set(pl["seed_ids"]))
        pl["n_seeds"] = len(pl["seed_ids"])
        tier_b.append(pl)
    tier_b.sort(key=lambda r: (-r["n_seeds"], -(r["cited_by_count"] or 0)))
    json.dump(tier_b, open(OUT_B, "w"), indent=2)

    n_multi = sum(1 for r in tier_b if r["n_seeds"] > 1)
    n_abs = sum(1 for r in tier_b if r.get("abstract"))
    decoy_seeds = {r["openalex_id"] for r in tier_a if r["provisional_cell"].startswith("OFF_")}
    hom_seeds = {r["openalex_id"] for r in tier_a if r["provisional_cell"] in HOMONYM_CELLS}
    tech_seeds = {r["openalex_id"] for r in tier_a if r["provisional_cell"] in TECH_CELLS}
    n_decoy_dep = sum(1 for r in tier_b if set(r["seed_ids"]) <= decoy_seeds)
    n_hom_dep = sum(1 for r in tier_b if set(r["seed_ids"]) <= hom_seeds)
    n_emp = sum(1 for r in tier_a if is_empirical_anchor(r))
    n_scr = sum(1 for r in tier_a if is_screenable_anchor(r))

    # ---- Wall 9, measured over the whole tech-seed neighbourhood rather than per seed ----
    tech_reach = [r for r in tier_b if set(r["seed_ids"]) & tech_seeds]
    w9_pop = [r for r in tech_reach if wall9_shape(r)]
    w9_visible = [r for r in tech_reach if has_app(r)]
    w9_share = len(w9_pop) / max(len(tech_reach), 1)
    w9_vis_share = len(w9_visible) / max(len(tech_reach), 1)

    pc = lambda v: f"{v:.1%}" if v is not None else "n/a"
    L = [f"# A4 Tier A / Tier B citation frame — {SLUG} (A.24)", "",
         f"**Tier A: {len(tier_a)} seeding anchors.** The causal recall denominator is reported TWO "
         "ways, and the gap between them is the measured cost of Wall 9:", "",
         f"- **{n_emp} empirical anchors** — `PRIMARY_APP_*` plus `SECONDARY_TECH_*`. Both groups "
         "estimate relationships this chapter grades, so both belong in a causal denominator.",
         f"- **{n_scr} screenable anchors** — `PRIMARY_APP_*` alone. Wall 9 declares the "
         "technology-diffusion estimates unreachable by a title/abstract screen built on the app "
         "axis, because none of them says 'dating app' anywhere a screener can see. Recall(A) "
         f"against the {n_emp}-anchor denominator will look poor by construction; against the "
         f"{n_scr}-anchor denominator it measures the screen. **Report both. The difference is the "
         "price of an unenforceable wall, not a screen failure.**", "",
         "`PRIMARY_APP_FERTILITY` seeds nothing and is retained with a denominator of zero. The "
         "recon probe found eleven records at app exposure against a population fertility quantity "
         "and none is an estimate, so the cell the registry entry is actually about has no anchor. A "
         "frame that quietly drops an empty cell cannot later show that it was empty.", "",
         f"**Tier B frame: {len(tier_b):,} deduplicated records** — {n_multi:,} found by more than "
         f"one seed, {n_abs:,} carrying an abstract ({n_abs / max(len(tier_b), 1):.0%}).", "",
         f"**Records depending ONLY on a routing-decoy seed: {n_decoy_dep:,}** "
         f"({n_decoy_dep / max(len(tier_b), 1):.0%}), of which **{n_hom_dep:,} depend only on a "
         "HOMONYM seed**. `seed_ids` provenance is retained on every Tier B record so Recall(B) can "
         "be recomputed without either group.", "",
         f"**Failed requests: {len(errors)}** — listed at the foot. A failed request is not an empty "
         "result, and the frame is smaller than the index by exactly what those failures cost.", "",
         "## Wall 9, measured", "",
         f"Across the **{len(tech_reach):,} records reachable from a `SECONDARY_TECH_*` seed**:", "",
         f"- **{len(w9_pop):,} ({w9_share:.1%}) carry an outcome and NO app vocabulary at all** — the "
         "bypass's addressable population, and the shape of all three identified estimates "
         "themselves.",
         f"- **{len(w9_visible):,} ({w9_vis_share:.1%}) carry app vocabulary** and are therefore the "
         "only part of this neighbourhood a screen built on the exposure axis can see.", "",
         "That ratio is Wall 9's cost as a number rather than as a sentence in the scope document. "
         "The bypass is gated on SEED PROVENANCE plus an outcome term and deliberately does NOT "
         "require app vocabulary: requiring the wall's own vocabulary to find the population the "
         "wall calls invisible is the self-defeating gate A.12 measured at 4 records against 212. "
         "The cost of that breadth is stated rather than hidden — the bypass admits "
         "technology-and-outcome papers generally, so internet-and-labour-supply and "
         "internet-and-wellbeing papers arrive beside the internet-and-marriage ones, and the screen "
         "pays one read each to reject them. Admitting a same-shaped paper that turns out not to be "
         "about partnering costs one screen read; excluding it costs a record no later stage can "
         "recover.", "",
         "## Per-seed yield", "",
         "Every fraction is a SEED-SELECTION DIAGNOSTIC computed after retrieval. None is applied as "
         "a filter: filtering the forward fetch by topic vocabulary would prune Tier B by distance "
         "from the production query and make Recall(B) circular.", "",
         "`app` = carries dating-app vocabulary (the exposure axis). `un` and `fer` are the two "
         "limbs of the outcome axis, reported separately because this chapter's finding is that the "
         "literature reaches unions and stops short of births. **`BOTH`** = app AND outcome, a loose "
         "upper bound on the reachable cell. **`W9`** = outcome AND technology exposure but NO app "
         "vocabulary — the Wall 9 bypass shape. `geo`, `vio`, `sex`, `plat` and `non` measure Walls "
         "1, 3, 5, 4 and 2. All are LOWER BOUNDS: a record counts only when it names the thing.", "",
         "| seed | cell | back | fwd | total | trunc | app | un | fer | **BOTH** | n | **W9** | n | geo | vio | sex | plat | non |",
         "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in sorted(log_rows, key=lambda x: -(x["n_fwd"])):
        L.append(f"| {r['title']} | `{r['cell']}` | {r['n_back']} | {r['n_fwd']} | "
                 f"{r['fwd_total'] or 0} | {'**yes**' if r['truncated'] else 'no'} | "
                 f"{pc(r['app'])} | {pc(r['union'])} | {pc(r['fert'])} | **{pc(r['primary'])}** | "
                 f"{r['n_primary']} | **{pc(r['wall9'])}** | {r['n_wall9']} | {pc(r['geo'])} | "
                 f"{pc(r['vio'])} | {pc(r['sex'])} | {pc(r['plat'])} | {pc(r['nonhuman'])} |")

    tot_fwd = sum(r["n_fwd"] for r in log_rows)
    tot_prim = sum(r["n_primary"] for r in log_rows)
    emp_rows = [r for r in log_rows if r["empirical"]]
    emp_fwd = sum(r["n_fwd"] for r in emp_rows)
    emp_union = sum((r["union"] or 0) * r["n_fwd"] for r in emp_rows)
    emp_fert = sum((r["fert"] or 0) * r["n_fwd"] for r in emp_rows)
    L += ["", "## Where the outcome axis stops", "",
          f"Across every seed's forward cloud, **{tot_prim:,} of {tot_fwd:,} records "
          f"({tot_prim / max(tot_fwd, 1):.2%}) carry app vocabulary and an outcome together.** Read "
          "it as which seeds can reach the cell at all, not as a count of studies.", "",
          f"Inside the {len(emp_rows)} EMPIRICAL seeds' clouds ({emp_fwd:,} records), the two limbs "
          f"of the outcome axis separate: **{emp_union / max(emp_fwd, 1):.1%} carry a union "
          f"construct and {emp_fert / max(emp_fwd, 1):.1%} carry a fertility quantity.** The gap "
          "between those two numbers is this chapter's central empirical claim, stated as a property "
          "of the literature rather than as an argument: the evidence base reaches partnership and "
          "stops.", ""]

    exact_rows = [r for r in log_rows if r["exact_outcome"] is not None or r["homonym"]]
    if exact_rows:
        L += ["## Exact outcome rates — counted, not sampled", "",
              "The scope froze geochronological 'dating' and agronomic 'fertility' as PURE HOMONYMS "
              "rather than boundary cases, which is this chapter's one carve-out from the standing "
              "rule that a decoy cloud is worth seeding in full. A carve-out asserted is worth "
              "nothing and one measured on a capped sample little more — a truncated OpenAlex pull "
              "is the high-citation HEAD, not a random sample. Each row below therefore carries an "
              "EXACT rate from two count-only queries over the seed's ENTIRE cloud. Extended beyond "
              "A.12: any TRUNCATED seed gets the exact rate too, because the sampling objection "
              "applies to every cap and not only to the ones we chose to distrust.", "",
              "| seed | cell | on-outcome (exact) | total citing | exact rate | **human-anchored** | sampled rate |",
              "|---|---|---|---|---|---|---|"]
        for r in exact_rows:
            er = (r["exact_outcome"] / r["exact_total"]) if (r["exact_outcome"] is not None
                                                             and r["exact_total"]) else None
            hr = (r["exact_human"] / r["exact_human_total"]) if (r.get("exact_human") is not None
                                                                 and r.get("exact_human_total")) else None
            L.append(f"| {r['title']} | `{r['cell']}` | "
                     f"{r['exact_outcome'] if r['exact_outcome'] is not None else 'UNCONFIRMED'} | "
                     f"{r['exact_total'] if r['exact_total'] is not None else 'UNCONFIRMED'} | "
                     f"{pc(er)} | **{pc(hr) if hr is not None else 'n/a'}** | {pc(r['outcome'])} |")
        L += ["", "**Read the human-anchored column, not the plain one, for the homonym seeds — and "
              "the difference between them is itself a finding.** The plain vocabulary contains the "
              "word \"fertility\", and in an agronomic cloud that word means SOIL fertility, so the "
              "plain rate scores Wall 2's own justification as evidence against Wall 2. A homonym "
              "family that shares a word with the outcome axis cannot be measured with a vocabulary "
              "that contains that word. A near-zero human-anchored rate confirms a carve-out; a "
              "materially non-zero one refutes it, and the response is to restore that seed to a "
              "full uncapped pull and re-run, because the cap is a budget decision the measurement "
              "is entitled to overturn.", "",
              "The violence seed shows the other half of the sampling argument: its exact rate is "
              "**lower** than its sampled rate, because a capped pull returns the high-citation "
              "HEAD and the head of an IPV literature is more likely to carry a marriage or "
              "partnership word than its tail. A cap does not merely lose records, it loses them "
              "non-randomly, in the direction that flatters the diagnostic.", ""]

    if recovery_report:
        L += ["## DOI-less seed recovery", "",
              "A DOI-less anchor cannot seed, so each got ONE recovery attempt gated by first-author "
              "agreement, with the type restriction inverted rather than dropped: a book must "
              "resolve to a bookish record and a non-book must not, so a monograph cannot be seeded "
              "from a journal review of itself. A.24 has one DOI-less anchor and it is the "
              "adversarial case — Becker's *A Treatise on the Family*, whose highest-cited record is "
              "a Population and Development Review review typed `article` and listing Becker himself "
              "as author.", "",
              "| anchor | book? | recovered | record | cites |", "|---|---|---|---|---|"]
        for t, isb, rid, note, cites in recovery_report:
            L.append(f"| {t} | {'yes' if isb else 'no'} | {'**yes**' if rid else 'no'} | "
                     f"{('`' + rid + '` ' + note[:44]) if rid else note} | {cites if cites else '—'} |")
        L += [""]

    trunc = [r for r in log_rows if r["truncated"]]
    L += ["## Truncation", ""]
    if trunc:
        L.append(f"{len(trunc)} seed(s) were truncated and are reported here rather than silently "
                 "capped — a bounded pull that is not stated reads as complete coverage:")
        tot_lost = 0.0
        for r in trunc:
            missed = (r["fwd_total"] or 0) - r["n_fwd"]
            rate = r["outcome"] or 0
            if r["exact_outcome"] is not None and r["exact_total"]:
                rate = r["exact_outcome"] / r["exact_total"]
            exp = missed * rate
            tot_lost += exp
            capname = f"{HOMONYM_CAP:,} homonym cap" if r["homonym"] else f"{FORWARD_CAP:,} forward cap"
            L.append(f"- **{r['title']}** (`{r['cell']}`, {capname}): pulled {r['n_fwd']:,} of "
                     f"{r['fwd_total']:,} citing works — **{missed:,} unpulled, an estimated "
                     f"{exp:.0f} on-outcome records not seen** (rate {rate:.1%}"
                     f"{', exact' if r['exact_outcome'] is not None else ', sampled'}).")
        L += ["", f"**Estimated on-outcome records lost to caps in total: ~{tot_lost:.0f}**, against "
                  f"a frame of {len(tier_b):,}. Where the rate is marked exact the estimate rests on "
                  "a full-cloud count rather than on the assumption that the unpulled tail resembles "
                  "the pulled head — which a cursor-paged truncation cannot guarantee."]
    else:
        L.append("No seed was truncated; the frame is a complete one-hop neighbourhood of the "
                 "verified and recovered anchors.")
    if errors:
        L += ["", "## Failed requests (NOT zero results)", ""] + [f"- {a}: `{b}`" for a, b in errors[:40]]
    open(OUT_LOG, "w").write("\n".join(L) + "\n")

    print(f"\ntier_a={len(tier_a)} (empirical={n_emp}, screenable={n_scr}) tier_b={len(tier_b)} "
          f"multi_seed={n_multi} decoy_only={n_decoy_dep} homonym_only={n_hom_dep} "
          f"wall9_pop={len(w9_pop)}/{len(tech_reach)} ({w9_share:.1%}) errors={len(errors)}")
    print(f"-> {os.path.relpath(OUT_B, ROOT)}")
    print(f"-> {os.path.relpath(OUT_LOG, ROOT)}")
    if errors and len(errors) > 0.2 * max(len(tier_a), 1):
        print("WARNING: high request-failure rate; the frame is incomplete by an unknown amount.",
              file=sys.stderr)


if __name__ == "__main__":
    main()
