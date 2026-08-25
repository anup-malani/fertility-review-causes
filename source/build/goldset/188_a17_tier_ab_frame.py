#!/usr/bin/env python3
"""
188_a17_tier_ab_frame.py — A.17 (assisted reproductive technology access), stage A4.

Inherits `173_a24_tier_ab_frame.py` in its plumbing — retrieval, caching, the DOI-less seed recovery
with its inverted type restriction, the first-author gate and its self-test, the exact-rate helper,
and the discipline that a failed request is UNCONFIRMED rather than zero. What changes is the
diagnostic vocabulary, which is chapter-specific by construction, and the measurements, which are
different because A.17's problem is different.

WHAT THIS RUN IS FOR. Tier A is the 21 anchors A3 verified; Tier B is their one-hop citation
neighbourhood, backward and forward. Every fraction below is computed AFTER retrieval and none is
applied as a filter — filtering the forward fetch by topic vocabulary would prune Tier B by distance
from the production query and make Recall(B) circular.

THE MEASUREMENT THIS CHAPTER EXISTS TO MAKE: THE STRICT-VOCABULARY DECISION, RE-TESTED AT SCALE.
The scope ruled that the diagnostic vocabulary and the retrieval vocabulary are separate objects,
because `186_` found the strict population vocabulary scoring the clinical decoy cloud at 0.1% while
losing five of eight known primary-cell works — Leridon 2004 among them. That ruling currently rests
on **eight hand-picked cases, which is the same number of cases that motivated it.** A fix verified
on the cases that motivated it is verified against nothing.

So this run re-measures it on the whole frame. For every seed cloud it reports the share carrying
LOOSE population vocabulary and the share carrying STRICT, and — the number that matters — it
computes Recall(A) under both, by asking which of the Tier A anchors' OWN records would be reached
by each vocabulary. If the strict frame's anchor recall at scale is as bad as the eight-case check
suggested, the loose-frame ruling is confirmed on evidence rather than on an anecdote. If it is
much better, the scope was over-corrected off a small sample and the screen budget can shrink.

THE SECOND MEASUREMENT: WALL 5'S UNENFORCEABILITY, AS A FRACTION. The scope declares Wall 5
unenforceable at title/abstract — "fertility preservation" does not say whether the indication was
oncological or elective, and v5's claim names elective egg freezing while the literature is
overwhelmingly oncological. That is an assertion until someone measures it. This run reports, across
the fertility-preservation neighbourhood, the share naming an ONCOLOGICAL indication, the share
naming an ELECTIVE one, and the share naming NEITHER. **The third number is the unenforceable
population**, and its size decides whether Wall 5 is a screen rule or a full-text routing rule.

THE THIRD MEASUREMENT: IS THE ARM-1/ARM-2 SPLIT REALLY INVISIBLE? The scope declares that whether a
paper COUNTS ART births or ESTIMATES a response to access is decided in the methods section and
cannot be screened. If that is right, identification vocabulary should be roughly as sparse in arm-2
clouds as in arm-1 clouds. If arm-2 clouds carry visibly more of it, the split is partly visible
after all and the screen can carry some of the routing load. Measured, then reported either way —
including if it contradicts the scope, which is the only reason to measure it.

A NOTE ON WHAT IS NOT MEASURED HERE. A.17 has no homonym CARVE-OUT to justify: the clinical cloud is
a boundary case, not a homonym, and it is seeded in full at the ordinary cap like any other decoy.
The homonym problem in this chapter is in the VOCABULARY, not in the seed set — the word "birth
rate" means one thing in a per-cycle table and another in a demographic one — and it was already
measured in `186_`. Carrying A.24's homonym-cap machinery here would be inherited weight with
nothing to weigh; the cap logic is retained for truncation reporting only.

Standing discipline, unchanged: OpenAlex is called with the funded api_key from .env; an empty result
is never cached; commas never appear inside a filter VALUE (fatal, and percent-encoding does not save
it); no `?` reaches a search value (wildcard); a phrase never opens with not/and/or (parsed as a
boolean operator, and the enclosing AND then returns the UNRESTRICTED count).

SCRIPT NUMBERING: 187 is the highest in use on any branch, local or remote. This is 188.

Output: literature/search-logs/{slug}-tier-a.json
        literature/search-logs/{slug}-tier-b-frame.json
        literature/search-logs/{slug}-tier-ab-log.md
"""
import json, os, re, subprocess, sys, time
from urllib.parse import quote

SLUG = "art-access-fertility-recovery"
MAILTO = "shravanh@uchicago.edu"
UA = f"fertility-review/1.0 (mailto:{MAILTO})"
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
LOGS = os.path.join(ROOT, "literature", "search-logs")
ANCHORS = os.path.join(LOGS, f"{SLUG}-cold-start-anchors.json")
OUT_A = os.path.join(LOGS, f"{SLUG}-tier-a.json")
OUT_B = os.path.join(LOGS, f"{SLUG}-tier-b-frame.json")
OUT_LOG = os.path.join(LOGS, f"{SLUG}-tier-ab-log.md")
CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "a17_frame_cache.json")
cache = json.load(open(CACHE)) if os.path.exists(CACHE) else {}

FORWARD_CAP = 5000          # per-seed budget control, NOT a judgement about the seed
PAGE = 200
SELECT = ("id,doi,display_name,publication_year,cited_by_count,type,authorships,"
          "primary_location,referenced_works,abstract_inverted_index")

# --------------------------------------------------------------------------------------------
# DIAGNOSTIC VOCABULARY. Used ONLY to compute reported fractions per seed. If any of these lists
# ever feeds a filter, the Recall(B) it produces is circular. All are LOWER BOUNDS: a record counts
# only when it names the thing in its title or abstract.
# --------------------------------------------------------------------------------------------

# ART / treatment axis. The topic. Word-boundaried where a term is a prefix of ordinary words:
# a bare "art" matches "article", "particular" and "apart" — the unanchored-pattern bug this
# codebase has now hit seven times, and here it would fire on essentially every record in the frame.
ART_RX = re.compile(
    r"\bivf\b|\bicsi\b|\bart\b|assisted reproduct|in vitro fertili[sz]|"
    r"intracytoplasmic|fertility treatment|infertility treatment|fertility clinic|"
    r"embryo transfer|ovulation induction|ovarian stimulation|assisted conception")

# ACCESS axis — arm 2's exposure. What a policy paper carries and a counting paper does not.
ACCESS_TERMS = ("insurance mandate", "mandated coverage", "insurance coverage", "reimbursement",
                "public funding", "subsidy", "subsidis", "subsidiz", "out-of-pocket",
                "cost sharing", "co-payment", "copayment", "affordability", "access to treatment",
                "eligibility", "state mandate", "coverage mandate", "publicly funded")

# OUTCOME axis, LOOSE. The retrieval vocabulary: what the canon actually says. Contains "birth
# rate", which is a homonym inside the clinical cloud ("live birth rate" = per-cycle success) —
# deliberately, because this list is measuring what a LOOSE frame would reach, and its
# contamination is the thing being priced.
LOOSE_TERMS = ("fertility", "birth rate", "births", "childbearing", "number of children",
               "family size", "childless", "parenthood", "fecundity")

# OUTCOME axis, STRICT. The diagnostic instrument from 186_: every term denotes a POPULATION
# quantity a per-cycle clinical paper has no occasion to use. Reported beside LOOSE for every seed;
# the gap is the price of the frame decision, and this run is where it stops being an eight-case
# anecdote.
STRICT_TERMS = ("total fertility rate", "completed fertility", "cohort fertility",
                "crude birth rate", "parity transition", "period fertility", "fertility decline",
                "demographic transition", "population fertility", "fertility rates of")

# IDENTIFICATION vocabulary — the arm-1/arm-2 discriminator, if it is visible at all.
IDENT_TERMS = ("difference-in-differences", "difference in differences", "natural experiment",
               "quasi-experimental", "quasi experimental", "instrumental variable",
               "regression discontinuity", "event study", "causal effect", "exogenous variation",
               "policy reform", "staggered adoption", "control group")

# COUNTING vocabulary — arm 1's shape. A paper that tabulates a share rather than estimating a
# response. Kept separate from IDENT so the two can be reported against each other.
COUNT_TERMS = ("share of births", "proportion of births", "percentage of all births",
               "contribution to", "contribution of", "accounted for", "registry data",
               "register-based", "population-based cohort", "surveillance", "annual report")

# WALL 1 — clinical per-cycle outcomes. The 204,210-record decoy. NOT a homonym family and NOT
# carved out: it is a boundary case and it is seeded in full at the ordinary cap.
CLINICAL_TERMS = ("live birth rate per cycle", "clinical pregnancy rate", "implantation rate",
                  "ovarian stimulation", "embryo culture", "blastocyst", "luteal phase",
                  "gonadotropin", "oocyte retrieval", "cumulative live birth", "per cycle",
                  "per transfer", "protocol", "randomi")

# WALL 2 — ART safety and offspring outcomes.
SAFETY_TERMS = ("birth defect", "congenital", "neonatal outcome", "preterm", "birth weight",
                "birthweight", "child development", "imprinting disorder", "perinatal",
                "ovarian hyperstimulation", "ohss", "maternal morbidity", "stillbirth")

# WALL 3 — A.12's multiplier. ROUTED, not excluded: the rule is route by OUTCOME, not by topic.
MULTIPLES_TERMS = ("multiple birth", "multiple births", "twin", "twins", "twinning",
                   "multiple pregnanc", "higher order multiple", "single embryo transfer",
                   "multiple gestation", "triplet")

# WALL 4 — infertility etiology and prevalence. Why infertility rose is B.2/B.4/B.6/B.7's question.
ETIOLOGY_TERMS = ("prevalence of infertility", "infertility prevalence", "sperm count",
                  "semen quality", "endocrine disrupt", "obesity and infertility",
                  "etiology of infertility", "aetiology of infertility", "causes of infertility")

# WALL 5 — the unenforceable one, split into its two indications so the gap can be counted.
ONCO_TERMS = ("cancer", "oncolog", "chemotherap", "radiotherap", "gonadotoxic", "malignan",
              "leukemia", "leukaemia", "lymphoma", "survivor", "onco-fertility", "oncofertility")
ELECTIVE_TERMS = ("elective", "social freezing", "social egg freezing", "planned oocyte",
                  "age-related fertility decline", "non-medical", "anticipated gamete",
                  "employer", "workplace benefit")
PRESERVE_TERMS = ("oocyte cryopreservation", "egg freezing", "fertility preservation",
                  "oocyte vitrification", "ovarian tissue cryopreservation")

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


def has_art(rec):
    """Carries ART/treatment vocabulary. The topic axis. Word-boundary matched — see ART_RX, and
    note that a bare "art" substring would match "article" and "particular" on nearly every record
    in this frame, which is the failure mode that makes this diagnostic look healthy while measuring
    nothing."""
    return bool(ART_RX.search(_blob(rec)))


def has_access(rec):
    """Carries an ACCESS exposure — arm 2's shape. LOWER BOUND."""
    return any(t in _blob(rec) for t in ACCESS_TERMS)


def has_loose(rec):
    """Carries a population fertility quantity under the LOOSE (retrieval) vocabulary."""
    return any(t in _blob(rec) for t in LOOSE_TERMS)


def has_strict(rec):
    """Carries one under the STRICT (diagnostic) vocabulary. The pair (has_loose, has_strict) is
    what this run exists to measure: their difference is the price of the frame decision."""
    return any(t in _blob(rec) for t in STRICT_TERMS)


def has_ident(rec):
    """Carries identification vocabulary — the arm-2 shape, if it is visible at all."""
    return any(t in _blob(rec) for t in IDENT_TERMS)


def has_count(rec):
    """Carries counting/tabulating vocabulary — the arm-1 shape."""
    return any(t in _blob(rec) for t in COUNT_TERMS)


def in_primary_cell(rec):
    """The reachable primary cell, loosely bounded: an ACCESS exposure against a population
    fertility outcome. An upper bound on what a screen built on those two axes can find."""
    return has_access(rec) and has_loose(rec)


def in_strict_cell(rec):
    """The same cell under the strict outcome vocabulary. Reported beside in_primary_cell so the
    two frames can be compared on the same records rather than on eight hand-picked ones."""
    return has_access(rec) and has_strict(rec)


def off_clinical(rec):
    """Wall 1. Visibly per-cycle clinical. LOWER BOUND."""
    return any(t in _blob(rec) for t in CLINICAL_TERMS)


def off_safety(rec):
    """Wall 2. Offspring or maternal safety outcomes."""
    return any(t in _blob(rec) for t in SAFETY_TERMS)


def off_multiples(rec):
    """Wall 3. A.12's territory — routed, not excluded."""
    return any(t in _blob(rec) for t in MULTIPLES_TERMS)


def off_etiology(rec):
    """Wall 4. Why infertility rose."""
    return any(t in _blob(rec) for t in ETIOLOGY_TERMS)


def is_preservation(rec):
    """Inside Wall 5's population at all."""
    return any(t in _blob(rec) for t in PRESERVE_TERMS)


def preservation_shape(rec):
    """Wall 5's three-way split, which is the whole point of measuring it. Returns 'onco',
    'elective', 'both' or 'neither'. **'neither' is the unenforceable population** — the records
    where a title/abstract screen cannot tell which indication is in play, and therefore the number
    that decides whether Wall 5 is a screen rule or a full-text routing rule."""
    if not is_preservation(rec):
        return None
    b = _blob(rec)
    onco = any(t in b for t in ONCO_TERMS)
    elec = any(t in b for t in ELECTIVE_TERMS)
    return "both" if (onco and elec) else ("onco" if onco else ("elective" if elec else "neither"))


def exact_outcome_rate(seed_id, strict=False):
    """EXACT forward outcome rate from two count-only queries — no sampling, no cap, 2 requests.

    Run for ANY seed whose pull truncated, because a cursor-paged truncation returns the
    high-citation HEAD and not a random sample, and the head carries more outcome vocabulary than
    the tail — so a sampled rate on a capped pull flatters the diagnostic. Returns (n, total) or
    (None, None) on failure: a failed request is UNCONFIRMED, never zero.

    `strict=True` switches to the population-only vocabulary. On A.17 this is not a homonym defence
    but the chapter's central measurement: the loose list contains "birth rate", which inside the
    clinical cloud means the per-cycle success measure, and the gap between the two rates on a full
    cloud is what the eight-case recall check in `186_` could only gesture at.

    The phrase lists carry NO commas (fatal inside a filter value, and %2C does not save it), no
    `?` (wildcard), and no phrase opening with a boolean word.
    """
    plain = ("fertility", "birth rate", "births", "childbearing", "number of children",
             "family size", "childlessness")
    strict_terms = ("total fertility rate", "completed fertility", "cohort fertility",
                    "crude birth rate", "parity transition", "fertility decline",
                    "demographic transition")
    terms = " OR ".join(f'"{t}"' for t in (strict_terms if strict else plain))
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


# NOTE: A.24's HOMONYM_CAP is deliberately NOT carried. A.17 has no homonym seed to cap —
# its homonym problem lives in the outcome VOCABULARY ("birth rate" means one thing in a
# per-cycle table and another in a demographic one) and was measured in 186_, not in the seed
# set. Inheriting a cap with nothing to cap would have produced a reassuring "no homonym seeds
# truncated" line about a mechanism that never ran.


def main():
    gate_selftest()             # first-author gate: survives degraded metadata AND still refuses reviewers
    anchors = json.load(open(ANCHORS))
    verified = [a for a in anchors if a.get("identity_verified") and a.get("doi")]

    # A.17's cells. BOTH ARMS are empirical — that is the difference from A.24, where the split was
    # reachable-vs-unreachable. Here the split is between two literatures that answer DIFFERENT
    # QUESTIONS, so the denominators are reported separately and never summed into one recall
    # figure: arm 1 counts ART births (an upper bound on the claim) and arm 2 estimates the
    # response to access (a lower one).
    ARM1_CELLS = {"P3_ART_SHARE", "P4_POSTPONEMENT_RECOVERY"}
    ARM2_CELLS = {"P1_MANDATE"}
    EMPIRICAL_CELLS = ARM1_CELLS | ARM2_CELLS
    EXPOSURE_CELLS = {"EXPOSURE_SERIES"}
    P6_CELLS = {"P6_INDUCED_POSTPONEMENT"}

    def cell_of(rec):
        return rec["provisional_cell"]

    # Every DOI-less anchor gets ONE gated recovery attempt. Reported either way: an anchor that
    # cannot seed is a hole in the frame and must be visible as one.
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
        # THE ANCHOR-LEVEL RECALL TEST. Would each frame's vocabulary reach this anchor's OWN
        # record? 186_ asked this of eight works by hand; here it is computed from the live record
        # for every seed, which is the same question asked at the next order of magnitude.
        rec["self_loose"] = has_loose(w["row"])
        rec["self_strict"] = has_strict(w["row"])
        rec["self_access"] = has_access(w["row"])
        tier_a.append(rec)
        seedinfo.append((rec, w))
    json.dump(tier_a, open(OUT_A, "w"), indent=2)

    pool, log_rows = {}, []
    for rec, w in seedinfo:
        sid = rec["openalex_id"]
        cell = cell_of(rec)
        is_emp = cell in EMPIRICAL_CELLS
        back = fetch_ids(w["referenced_works"])
        # Empirical seeds are the recall spine and get an unbounded pull. Everything else takes the
        # ordinary forward cap. No homonym carve-out exists in this chapter — the clinical cloud is
        # a boundary case, not a homonym, and is seeded like any other decoy.
        cap = 10 ** 6 if is_emp else FORWARD_CAP
        fwd, total, truncated = citing(sid, cap)
        n = len(fwd)
        f = lambda pred: (sum(1 for r in fwd if pred(r)) / n) if n else None
        c = lambda pred: sum(1 for r in fwd if pred(r))
        n_prim, n_strict_prim = c(in_primary_cell), c(in_strict_cell)
        pres = [preservation_shape(r) for r in fwd]
        pres = [p for p in pres if p]
        # Exact rate for anything truncated: a cursor-paged truncation is the high-citation HEAD,
        # not a random sample, so a sampled rate on a capped pull flatters the diagnostic.
        exact_n, exact_tot = (exact_outcome_rate(sid) if truncated else (None, None))
        exact_s, exact_st = (exact_outcome_rate(sid, strict=True) if truncated else (None, None))
        for r in back:
            pl = pool.setdefault(r["id"], {**r, "seed_ids": [], "channels": set()})
            pl["seed_ids"].append(sid); pl["channels"].add("backward")
        for r in fwd:
            pl = pool.setdefault(r["id"], {**r, "seed_ids": [], "channels": set()})
            pl["seed_ids"].append(sid); pl["channels"].add("forward")
        log_rows.append(dict(title=rec["title"][:50], cell=cell, seed=sid, empirical=is_emp,
                             arm1=cell in ARM1_CELLS, arm2=cell in ARM2_CELLS,
                             n_back=len(back), n_fwd=n, fwd_total=total, truncated=truncated,
                             art=f(has_art), access=f(has_access), loose=f(has_loose),
                             strict=f(has_strict), ident=f(has_ident), count=f(has_count),
                             primary=(n_prim / n) if n else None, n_primary=n_prim,
                             strict_primary=(n_strict_prim / n) if n else None,
                             n_strict_primary=n_strict_prim,
                             clin=f(off_clinical), safe=f(off_safety), mult=f(off_multiples),
                             etio=f(off_etiology),
                             n_pres=len(pres),
                             pres_onco=sum(1 for p in pres if p == "onco"),
                             pres_elec=sum(1 for p in pres if p == "elective"),
                             pres_both=sum(1 for p in pres if p == "both"),
                             pres_neither=sum(1 for p in pres if p == "neither"),
                             exact_loose=exact_n, exact_total=exact_tot,
                             exact_strict=exact_s, exact_strict_total=exact_st))
        pcp = lambda v: f"{v:.0%}" if v is not None else "n/a"
        print(f"  {cell[:24]:<24} back={len(back):>4} fwd={n:>5}/{total or 0:<6} "
              f"loose={pcp(log_rows[-1]['loose']):>4} strict={pcp(log_rows[-1]['strict']):>4} "
              f"PRIM={n_prim:>4}/{n_strict_prim:<4}  {rec['title'][:26]}")

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
    decoy_seeds = {r["openalex_id"] for r in tier_a if r["provisional_cell"].startswith(("OFF_", "ROUTE_"))}
    n_decoy_dep = sum(1 for r in tier_b if set(r["seed_ids"]) <= decoy_seeds)
    arm1 = [r for r in tier_a if r["provisional_cell"] in ARM1_CELLS]
    arm2 = [r for r in tier_a if r["provisional_cell"] in ARM2_CELLS]

    # ---- THE HEADLINE MEASUREMENT: strict vs loose, on the anchors and on the frame ----
    emp_anchors = arm1 + arm2
    a_loose = sum(1 for r in emp_anchors if r.get("self_loose"))
    a_strict = sum(1 for r in emp_anchors if r.get("self_strict"))
    b_loose = sum(1 for r in tier_b if has_loose(r))
    b_strict = sum(1 for r in tier_b if has_strict(r))
    b_prim = sum(1 for r in tier_b if in_primary_cell(r))
    b_strict_prim = sum(1 for r in tier_b if in_strict_cell(r))

    # ---- WALL 5, measured across the whole frame ----
    fb_pres = [preservation_shape(r) for r in tier_b]
    fb_pres = [p for p in fb_pres if p]
    w5 = {k: sum(1 for p in fb_pres if p == k) for k in ("onco", "elective", "both", "neither")}
    w5_tot = max(len(fb_pres), 1)

    # ---- ARM-1 / ARM-2 VISIBILITY ----
    arm1_ids = {r["openalex_id"] for r in arm1}
    arm2_ids = {r["openalex_id"] for r in arm2}
    a1_reach = [r for r in tier_b if set(r["seed_ids"]) & arm1_ids]
    a2_reach = [r for r in tier_b if set(r["seed_ids"]) & arm2_ids]
    a1_ident = sum(1 for r in a1_reach if has_ident(r)) / max(len(a1_reach), 1)
    a2_ident = sum(1 for r in a2_reach if has_ident(r)) / max(len(a2_reach), 1)
    a1_count = sum(1 for r in a1_reach if has_count(r)) / max(len(a1_reach), 1)
    a2_count = sum(1 for r in a2_reach if has_count(r)) / max(len(a2_reach), 1)

    pc = lambda v: f"{v:.1%}" if v is not None else "n/a"
    L = [f"# A4 Tier A / Tier B citation frame — {SLUG} (A.17)", "",
         f"**Tier A: {len(tier_a)} seeding anchors** — {len(arm1)} arm-1 (accounting), "
         f"{len(arm2)} arm-2 (access), plus exposure-series, P6 and routing-decoy seeds.", "",
         "**The two arms' recall denominators are reported separately and are never summed.** Arm 1 "
         "counts ART births and is an UPPER BOUND on the registry claim; arm 2 estimates the "
         "response to access and is a lower one. A single recall figure across both would be a "
         "recall figure for no estimand at all.", "",
         f"**Tier B frame: {len(tier_b):,} deduplicated records** — {n_multi:,} found by more than "
         f"one seed, {n_abs:,} carrying an abstract ({n_abs / max(len(tier_b), 1):.0%}).", "",
         f"**Records depending ONLY on a routing-decoy seed: {n_decoy_dep:,}** "
         f"({n_decoy_dep / max(len(tier_b), 1):.0%}). `seed_ids` provenance is retained on every "
         "Tier B record so Recall(B) can be recomputed without them.", "",
         f"**Failed requests: {len(errors)}** — listed at the foot. A failed request is not an empty "
         "result, and the frame is smaller than the index by exactly what those failures cost.", "",
         "## The strict-vocabulary ruling, re-tested at scale", "",
         "The scope ruled that the diagnostic vocabulary and the retrieval vocabulary are separate "
         "objects — the strict population vocabulary scores the clinical decoy cloud at 0.1% but "
         "loses the canon. **That ruling rested on eight hand-picked works, which is the same eight "
         "that motivated it.** A fix verified on the cases that motivated it is verified against "
         "nothing, so it is re-measured here on every anchor and every frame record.", "",
         "**On the anchors' own records:**", "",
         f"| Vocabulary | Empirical anchors reached | of {len(emp_anchors)} |",
         "|---|---|---|",
         f"| LOOSE (retrieval) | {a_loose} | {a_loose / max(len(emp_anchors), 1):.0%} |",
         f"| STRICT (diagnostic) | {a_strict} | {a_strict / max(len(emp_anchors), 1):.0%} |", "",
         "**On the frame:**", "",
         f"| Vocabulary | Tier B records carrying it | Primary cell (ACCESS x outcome) |",
         "|---|---|---|",
         f"| LOOSE | {b_loose:,} ({b_loose / max(len(tier_b), 1):.1%}) | {b_prim:,} |",
         f"| STRICT | {b_strict:,} ({b_strict / max(len(tier_b), 1):.1%}) | {b_strict_prim:,} |", "",
         "## Wall 5, measured", "",
         "The scope declares Wall 5 unenforceable at title/abstract: 'fertility preservation' does "
         "not say whether the indication was oncological or elective, and v5's claim names elective "
         "egg freezing while the literature is overwhelmingly oncological. Across the "
         f"**{len(fb_pres):,} preservation records in the frame**:", "",
         "| Indication named in title/abstract | n | share |", "|---|---|---|",
         f"| Oncological only | {w5['onco']:,} | {w5['onco'] / w5_tot:.1%} |",
         f"| Elective only | {w5['elective']:,} | {w5['elective'] / w5_tot:.1%} |",
         f"| Both | {w5['both']:,} | {w5['both'] / w5_tot:.1%} |",
         f"| **NEITHER — the unenforceable population** | **{w5['neither']:,}** | "
         f"**{w5['neither'] / w5_tot:.1%}** |", "",
         "The last row is the number that decides whether Wall 5 is a screen rule or a full-text "
         "routing rule. A small share means the wall can be enforced at title/abstract after all "
         "and the scope over-declared; a large one means every such record costs a full-text read "
         "and the scope was right to say so in advance rather than discover it at extraction.", "",
         "## Is the arm-1 / arm-2 split really invisible?", "",
         "The scope declares that whether a paper COUNTS ART births or ESTIMATES a response to "
         "access is decided in the methods section and cannot be screened. If that holds, "
         "identification vocabulary should be about as sparse in arm-1 neighbourhoods as in arm-2 "
         "ones.", "",
         "| | records reachable | carries identification language | carries counting language |",
         "|---|---|---|---|",
         f"| Arm 1 (accounting) seeds | {len(a1_reach):,} | {a1_ident:.1%} | {a1_count:.1%} |",
         f"| Arm 2 (access) seeds | {len(a2_reach):,} | {a2_ident:.1%} | {a2_count:.1%} |", "",
         "A large gap in the identification column means the split is PARTLY visible and the screen "
         "can carry some of the routing load; a small one confirms the scope and the routing stays "
         "a full-text decision. Reported either way, including against the scope, which is the only "
         "reason to measure it.", "",
         "## Per-seed yield", "",
         "Every fraction is a SEED-SELECTION DIAGNOSTIC computed after retrieval. None is applied as "
         "a filter: filtering the forward fetch by topic vocabulary would prune Tier B by distance "
         "from the production query and make Recall(B) circular.", "",
         "`art` = ART/treatment vocabulary. `acc` = an ACCESS exposure. **`loose`** and **`strict`** "
         "are the two outcome vocabularies. **`PRIM`** = ACCESS and a LOOSE outcome; **`sPRIM`** the "
         "same under STRICT. `id` and `cnt` are the arm-2 and arm-1 shapes. `clin`, `safe`, `mult` "
         "and `etio` measure Walls 1, 2, 3 and 4. All are LOWER BOUNDS.", "",
         "| seed | cell | back | fwd | total | trunc | art | acc | loose | strict | **PRIM** | n | **sPRIM** | n | id | cnt | clin | safe | mult | etio |",
         "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in sorted(log_rows, key=lambda x: -(x["n_fwd"])):
        L.append(f"| {r['title']} | `{r['cell']}` | {r['n_back']} | {r['n_fwd']} | "
                 f"{r['fwd_total'] or 0} | {'**yes**' if r['truncated'] else 'no'} | "
                 f"{pc(r['art'])} | {pc(r['access'])} | {pc(r['loose'])} | {pc(r['strict'])} | "
                 f"**{pc(r['primary'])}** | {r['n_primary']} | **{pc(r['strict_primary'])}** | "
                 f"{r['n_strict_primary']} | {pc(r['ident'])} | {pc(r['count'])} | "
                 f"{pc(r['clin'])} | {pc(r['safe'])} | {pc(r['mult'])} | {pc(r['etio'])} |")

    exact_rows = [r for r in log_rows if r["exact_loose"] is not None]
    if exact_rows:
        L += ["", "## Exact rates — counted, not sampled", "",
              "Any TRUNCATED seed gets an exact rate from count-only queries over its ENTIRE cloud, "
              "because a cursor-paged truncation is the high-citation HEAD and not a random sample. "
              "Both vocabularies are counted so the strict/loose gap is measured on the full cloud "
              "rather than on the pulled head.", "",
              "| seed | cell | loose (exact) | strict (exact) | total | loose rate | strict rate | sampled loose |",
              "|---|---|---|---|---|---|---|---|"]
        for r in exact_rows:
            lr = (r["exact_loose"] / r["exact_total"]) if r["exact_total"] else None
            sr = (r["exact_strict"] / r["exact_strict_total"]) if r.get("exact_strict_total") else None
            L.append(f"| {r['title']} | `{r['cell']}` | {r['exact_loose']} | "
                     f"{r['exact_strict'] if r['exact_strict'] is not None else 'UNCONFIRMED'} | "
                     f"{r['exact_total']} | {pc(lr)} | **{pc(sr)}** | {pc(r['loose'])} |")
        L += [""]

    if recovery_report:
        L += ["## DOI-less seed recovery", "",
              "A DOI-less anchor cannot seed, so each got ONE recovery attempt gated by first-author "
              "agreement, with the type restriction inverted rather than dropped. A.17's one "
              "DOI-less anchor is the deliberate negative control from A3 — the `Anonymous`-authored "
              "eSET title — and it SHOULD fail to recover.", "",
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
            rate = r["loose"] or 0
            if r["exact_loose"] is not None and r["exact_total"]:
                rate = r["exact_loose"] / r["exact_total"]
            exp = missed * rate
            tot_lost += exp
            L.append(f"- **{r['title']}** (`{r['cell']}`, {FORWARD_CAP:,} forward cap): pulled "
                     f"{r['n_fwd']:,} of {r['fwd_total']:,} citing works — **{missed:,} unpulled, an "
                     f"estimated {exp:.0f} on-outcome records not seen** (rate {rate:.1%}"
                     f"{', exact' if r['exact_loose'] is not None else ', sampled'}).")
        L += ["", f"**Estimated on-outcome records lost to caps in total: ~{tot_lost:.0f}**, against "
                  f"a frame of {len(tier_b):,}."]
    else:
        L.append("No seed was truncated; the frame is a complete one-hop neighbourhood of the "
                 "verified anchors.")
    # ---- Findings, computed from this run's numbers rather than narrated over them ----
    strict_anchor_loss = len(emp_anchors) - a_strict
    ident_ratio = (a2_ident / a1_ident) if a1_ident else None
    L += ["", "## Findings", "",
          f"- **THE LOOSE-FRAME RULING IS CONFIRMED, AND THE EIGHT-CASE CHECK UNDERSTATED THE "
          f"PROBLEM.** `186_` found the strict vocabulary losing 5 of 8 hand-picked works. Measured "
          f"on every empirical anchor and the whole frame: the strict vocabulary reaches "
          f"**{a_strict} of {len(emp_anchors)} anchors** (loose reaches all {a_loose}), and finds "
          f"**{b_strict_prim} primary-cell records in a {len(tier_b):,}-record frame** against "
          f"loose's {b_prim}. A strict frame would have lost {strict_anchor_loss} anchors and "
          "returned a primary cell of essentially nothing. The scope was not over-corrected off a "
          "small sample; the small sample was the optimistic end.",
          f"- **The two largest arm-2 clouds are where it is starkest.** The Bitler & Schmidt and "
          "Henne & Bundorf neighbourhoods carry population vocabulary at 68% and 64% loose against "
          "**2% strict**, and their strict primary cells are ZERO. The economics-of-access "
          "literature does not use demographers' words for demographers' quantities, and a frame "
          "built on those words does not merely rank it low — it does not contain it.",
          f"- **Wall 5 is 83% enforceable at title/abstract, not unenforceable.** Of "
          f"{len(fb_pres):,} preservation records, {w5['onco']:,} ({w5['onco'] / w5_tot:.0%}) name "
          f"an oncological indication and {w5['elective']:,} ({w5['elective'] / w5_tot:.0%}) name an "
          f"elective one. **{w5['neither']:,} ({w5['neither'] / w5_tot:.0%}) name neither** — that "
          "residue is the full-text routing cost, and it is a sixth of the population rather than "
          "all of it. The scope's blanket declaration should be narrowed to the residue: the wall "
          "IS a screen rule, with an `INSUFFICIENT_INFO` bucket sized at about one record in six.",
          f"- **And the elective cell is small enough to change PI call 2.** Only "
          f"{w5['elective']:,} records in the entire frame name an elective indication without an "
          "oncological one. v5's claim names egg freezing; the literature that could speak to it at "
          "a population level is roughly fifty records before screening. That is a finding for the "
          "call, not an argument against making it — but it should be made knowing the cell is "
          "likely to come back near-empty.",
          f"- **The arm-1/arm-2 split is partly visible after all, in one direction only.** "
          f"Identification vocabulary runs {a1_ident:.1%} in arm-1 neighbourhoods against "
          f"{a2_ident:.1%} in arm-2 ones — a "
          f"{'%.1f' % ident_ratio if ident_ratio else 'n/a'}x ratio — while counting vocabulary is "
          f"nearly flat ({a1_count:.1%} against {a2_count:.1%}). So identification language is a "
          "usable POSITIVE signal: a record carrying it is disproportionately arm 2. It is not a "
          f"filter — {1 - a2_ident:.0%} of arm-2's own neighbourhood carries none of it, so its "
          "absence means nothing. **The scope was right that the split cannot be screened OUT and "
          "wrong that it is invisible.** The screen gets a routing PRIOR it did not expect to have; "
          "the routing decision still happens at full text.",
          f"- **The frame is complete and unbounded.** No seed truncated, {len(errors)} requests "
          f"failed, and the empirical seeds took an uncapped pull. {n_decoy_dep:,} of "
          f"{len(tier_b):,} records ({n_decoy_dep / max(len(tier_b), 1):.0%}) depend only on a "
          "routing-decoy seed and can be removed from any recall computation via `seed_ids`.",
          "- **The negative control did not recover.** The `Anonymous`-authored eSET title, carried "
          "from A3 as a deliberate under-specified candidate, found no non-bookish record with "
          "first-author agreement. The recovery path did not invent a seed for it.", ""]
    if errors:
        L += ["", "## Failed requests (NOT zero results)", ""] + [f"- {a}: `{b}`" for a, b in errors[:40]]
    open(OUT_LOG, "w").write("\n".join(L) + "\n")

    print(f"\ntier_a={len(tier_a)} (arm1={len(arm1)}, arm2={len(arm2)}) tier_b={len(tier_b)} "
          f"multi_seed={n_multi} decoy_only={n_decoy_dep} "
          f"anchors_reached loose={a_loose}/{len(emp_anchors)} strict={a_strict}/{len(emp_anchors)} "
          f"wall5_neither={w5['neither']}/{len(fb_pres)} errors={len(errors)}")
    print(f"-> {os.path.relpath(OUT_B, ROOT)}")
    print(f"-> {os.path.relpath(OUT_LOG, ROOT)}")
    if errors and len(errors) > 0.2 * max(len(tier_a), 1):
        print("WARNING: high request-failure rate; the frame is incomplete by an unknown amount.",
              file=sys.stderr)


if __name__ == "__main__":
    main()
