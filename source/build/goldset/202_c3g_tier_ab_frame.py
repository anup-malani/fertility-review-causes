#!/usr/bin/env python3
"""
202_c3g_tier_ab_frame.py — C.3.g (student debt and household formation), stage A4.

Inherits `188_a17_tier_ab_frame.py` in its plumbing — retrieval, caching, the DOI-less seed recovery
with its first-author gate and self-test, the exact-rate helper for truncated pulls, and the rule
that a failed request is UNCONFIRMED rather than zero. The vocabulary and the measurements are
chapter-specific, because C.3.g's problem is not A.17's.

WHAT THIS RUN IS FOR. Tier A is the 20 anchors A3 verified; Tier B is their one-hop citation
neighbourhood, backward and forward. Every fraction below is computed AFTER retrieval and none is
applied as a filter — filtering the forward fetch by topic vocabulary would prune Tier B by distance
from the production query and make Recall(B) circular.

THE MEASUREMENT THIS RUN EXISTS TO MAKE: IS THE POLICY-VARIATION CELL REALLY EMPTY?

`200_` measured P2 — a change in debt POLICY (forgiveness, cancellation, repayment reform, loan
limits, a tuition regime) estimated against a FERTILITY outcome — as empty, and the scope makes that
the chapter's most transportable finding. But `200_` measured it THROUGH THE QUERY, and a query can
only report the absence of what its own vocabulary would reach. The citation channel is orthogonal
to the query by construction: it finds what the anchors cite and what cites them, whatever words
those works use.

So this run asks the same question through the other channel. Any Tier-B record carrying DEBT and
POLICY and FERTILITY vocabulary is a candidate the query missed, and every one is listed by title in
the log rather than counted. **If that list is non-empty, the scope's central finding is wrong and
this is where it should break.** A finding that survives a channel built to contradict it is worth
more than one confirmed by the channel that produced it.

THE SECOND MEASUREMENT: IS THE ARM ROUTING ACTUALLY VISIBLE? The scope asserts that, unlike A.17's
invisible arm split, C.3.g's routing is "largely visible at title and abstract, because the outcome
word is what distinguishes the arms". That is an assertion about vocabulary and it is checkable. For
every Tier-B record this run counts how many of the three outcome vocabularies — FERTILITY, UNION,
HOUSING — it carries. A record carrying exactly one is routable at screen. A record carrying two or
three is not, and the share carrying two or three is the price of the scope's claim. Reported either
way, including if it contradicts the scope, which is the only reason to measure it.

THE THIRD MEASUREMENT: THE ATTAINMENT CONFOUND, SIZED. The scope declares the
educational-attainment-conditioning question unenforceable at title/abstract and routes it to
full-text extraction, on the strength of 8 records at query level. This run reports the share of the
whole frame naming attainment-conditioning language. If it is a few per cent the scope is right and
the confound is a risk-of-bias domain; if it is large, part of it can be screened after all.

THE FOURTH MEASUREMENT: RECALL(A) ON THE FRAME'S OWN VOCABULARY. Would the production frame —
DEBT and (FERTILITY or UNION or HOUSING) — reach each anchor's OWN record? An anchor the frame
cannot reach is a hole, and on A.17 this test is what proved the loose-frame ruling. Here it also
prices the alternative of a fertility-only frame: any anchor reachable only through UNION or HOUSING
vocabulary is an anchor a narrower frame would lose.

WHAT IS NOT MEASURED HERE, AND WHY. C.3.g has no homonym cloud to carve out at the seed level. The
homonym problem in this chapter sits in the EXPOSURE vocabulary, not the outcome one — `"debt
burden"` alone reaches a 1,389-record sovereign-debt literature — and it was measured in `199_` and
handled by anchoring the exposure to student-specific terms. A.24's homonym-cap machinery would be
inherited weight with nothing to weigh; the cap logic is retained for truncation reporting only.

Standing discipline, unchanged: OpenAlex is called with the funded api_key from .env; an empty result
is never cached; commas never appear inside a filter VALUE (fatal, and percent-encoding does not save
it); no `?` reaches a search value (wildcard); a phrase never opens with not/and/or (parsed as a
boolean operator, and the enclosing AND then returns the UNRESTRICTED count).

SCRIPT NUMBERING: 201 is the highest in use on any branch, local or remote. This is 202.

Output: literature/search-logs/{slug}-tier-a.json
        literature/search-logs/{slug}-tier-b-frame.json
        literature/search-logs/{slug}-tier-ab-log.md
"""
import json, os, re, subprocess, sys, time
from urllib.parse import quote

SLUG = "student-debt-household-formation"
MAILTO = "shravanh@uchicago.edu"
UA = f"fertility-review/1.0 (mailto:{MAILTO})"
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
LOGS = os.path.join(ROOT, "literature", "search-logs")
ANCHORS = os.path.join(LOGS, f"{SLUG}-cold-start-anchors.json")
OUT_A = os.path.join(LOGS, f"{SLUG}-tier-a.json")
OUT_B = os.path.join(LOGS, f"{SLUG}-tier-b-frame.json")
OUT_LOG = os.path.join(LOGS, f"{SLUG}-tier-ab-log.md")
CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "c3g_frame_cache.json")
cache = json.load(open(CACHE)) if os.path.exists(CACHE) else {}

FORWARD_CAP = 5000          # per-seed budget control, NOT a judgement about the seed
PAGE = 200
SELECT = ("id,doi,display_name,publication_year,cited_by_count,type,authorships,"
          "primary_location,referenced_works,abstract_inverted_index")

# --------------------------------------------------------------------------------------------
# DIAGNOSTIC VOCABULARY. Used ONLY to compute reported fractions. If any of these lists ever feeds
# a filter on the forward pull, the Recall(B) it produces is circular. All are LOWER BOUNDS: a
# record counts only when it names the thing in its title or abstract.
# --------------------------------------------------------------------------------------------

# EXPOSURE axis. Word-boundaried and student-anchored. A bare "debt" reaches sovereign debt, and
# `199_` measured that cloud at 1,389 records for the phrase "debt burden" alone — the anchored
# vocabulary's own homonym, and the reason no unanchored liability term appears here.
DEBT_RX = re.compile(
    r"student loan|student debt|student borrow|college debt|educational debt|education debt|"
    r"education loan|tuition loan|loan for college|student indebtedness|graduate indebtedness")

# OUTCOME axis 1 — FERTILITY. The chapter's registered outcome and the direct arm's estimand.
FERT_TERMS = ("fertility", "childbearing", "first birth", "births", "birth rate", "childless",
              "number of children", "family size", "transition to parenthood", "parenthood",
              "having children", "family formation", "fecundity")

# OUTCOME axis 2 — UNION FORMATION. Chain-arm link 1. In scope because v5's claim names it.
UNION_TERMS = ("marriage", "marital", "cohabit", "union formation", "partnership formation",
               "age at marriage", "marriage timing", "getting married", "spouse")

# OUTCOME axis 3 — HOUSING AND RESIDENTIAL INDEPENDENCE. Chain-arm link 1.
HOUSE_TERMS = ("homeownership", "home ownership", "housing tenure", "first-time buyer",
               "first-time homebuyer", "home purchase", "household formation", "living with parents",
               "parental home", "coresidence", "co-residence", "residential independence",
               "leaving home", "mortgage origination", "moving out")

# IDENTIFICATION. Where the chapter's credible variation is, and the scope's finding is that it does
# NOT sit on the fertility axis.
# NOTE ON HOW THIS LIST WAS CORRECTED. Its first version carried "natural experiment",
# "quasi-experimental" and "randomi" but no bare "experiment", and it therefore scored the run's
# single most important record — *Experimental Evidence on ... Responses to Student Debt
# Forgiveness* — as NOT identified, in a table whose whole purpose was to find identified
# policy-variation studies. Measured across Tier B: 78 records name "experiment" and the original
# list missed 46 of them. The diagnostic was refuted by its own output, which is the only reason it
# was visible. `ident_vocab_selftest()` now makes a recurrence a start-up failure.
IDENT_TERMS = ("difference-in-differences", "difference in differences", "natural experiment",
               "quasi-experimental", "quasi experimental", "instrumental variable", "instrument for",
               "regression discontinuity", "regression kink", "event study", "exogenous variation",
               "causal effect", "causal impact", "randomi", "experiment", "rct",
               "synthetic control", "propensity score", "matched comparison", "control group",
               "treatment effect", "identification strategy")

# POLICY VARIATION — the P2 cell. This is the list that decides the run's headline measurement, so
# it is deliberately GENEROUS: an over-broad list makes the empty-cell finding harder to sustain,
# which is the direction an honest test should err in.
POLICY_TERMS = ("loan forgiveness", "debt forgiveness", "debt cancellation", "debt relief",
                "loan discharge", "income-driven repayment", "income driven repayment",
                "income contingent", "repayment plan", "loan limit", "borrowing limit",
                "tuition policy", "tuition-free", "tuition free", "free college", "free tuition",
                "financial aid reform", "aid policy", "pell grant", "state appropriations",
                "tuition cap", "loan program", "policy reform", "policy change")

# ATTAINMENT CONDITIONING — the confound the scope routed to full text. Measured, not assumed.
ATTAIN_TERMS = ("educational attainment", "college completion", "degree completion",
                "controlling for education", "conditional on education", "holding education",
                "college graduates", "bachelor's degree", "degree holders", "completed college")

# WALLS, for frame composition. Each was sized at query level in `199_`; here they are sized inside
# the citation neighbourhood, which is where the screen will actually meet them.
CAREER_TERMS = ("specialty choice", "career choice", "practice location", "rural practice",
                "residency program", "physician workforce", "primary care shortage", "medical student",
                "dental student", "veterinary student", "resident physician")
GENDEBT_TERMS = ("household debt", "consumer debt", "credit card", "mortgage debt", "medical debt",
                 "payday", "unsecured debt", "auto loan", "car loan")
DEFAULT_TERMS = ("loan default", "delinquen", "repayment behavio", "default rate", "loan servicing",
                 "defaulting")
PARENTPAY_TERMS = ("saving for college", "college savings", "paying for college",
                   "parental contribution", "parent plus", "parent borrow", "borrowing for a child",
                   "529 plan")
LMIC_TERMS = ("school fees", "child marriage", "sub-saharan", "low-income countries",
              "developing countries", "primary schooling", "secondary schooling")


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


def has_debt(rec):
    """Carries a STUDENT-anchored exposure term. Word-boundary matched — see DEBT_RX. A bare "debt"
    reaches the sovereign-debt literature, which `199_` measured at 1,389 records for one phrase;
    the anchored-vocabulary homonym is this chapter's version of A.17's "birth rates"."""
    return bool(DEBT_RX.search(_blob(rec)))


def has_fert(rec):
    """Carries a FERTILITY outcome. The registered estimand. LOWER BOUND."""
    return any(t in _blob(rec) for t in FERT_TERMS)


def has_union(rec):
    """Carries a UNION-FORMATION outcome — chain link 1."""
    return any(t in _blob(rec) for t in UNION_TERMS)


def has_house(rec):
    """Carries a HOUSING or residential-independence outcome — chain link 1."""
    return any(t in _blob(rec) for t in HOUSE_TERMS)


def has_ident(rec):
    """Names an identification strategy. The scope's finding is that this axis and the fertility
    axis barely intersect, and that is re-tested here on the citation channel."""
    return any(t in _blob(rec) for t in IDENT_TERMS)


def ident_vocab_selftest():
    """A diagnostic that cannot see the study shape it exists to find is worse than no diagnostic.

    Every phrase below names a real identification design that appeared in this frame. The first
    version of IDENT_TERMS matched none of the first four, and consequently reported the run's most
    important record — an EXPERIMENTAL evaluation of debt forgiveness with a family-formation
    outcome — as unidentified in the very table built to surface identified policy studies."""
    must_match = ["experimental evidence on consumption and saving",
                  "we run a field experiment", "a survey experiment on borrowers",
                  "randomized controlled trial", "difference-in-differences design",
                  "regression discontinuity at the eligibility threshold",
                  "we instrument for debt", "an event study around the reform"]
    must_not = ["an experienced practitioner", "expert opinion", "descriptive statistics only"]
    bad = [f"  MISSED: {p!r}" for p in must_match
           if not any(t in p for t in IDENT_TERMS)]
    bad += [f"  FALSE POSITIVE: {p!r}" for p in must_not
            if any(t in p for t in IDENT_TERMS)]
    if bad:
        sys.stderr.write("ABORT: identification vocabulary self-test failed; the run would report "
                         "identified studies as unidentified:\n")
        sys.stderr.write("\n".join(bad) + "\n")
        sys.exit(1)


def has_policy(rec):
    """Carries POLICY variation in debt. Deliberately generous — see POLICY_TERMS."""
    return any(t in _blob(rec) for t in POLICY_TERMS)


def has_attain(rec):
    """Names attainment conditioning — the confound the scope declared unenforceable at screen."""
    return any(t in _blob(rec) for t in ATTAIN_TERMS)


def n_outcome_axes(rec):
    """How many of the three outcome vocabularies a record carries.

    This is the scope's visibility claim expressed as a number. A record carrying exactly ONE axis
    is routable to an arm at title/abstract; a record carrying two or three is not, and has to be
    routed at full text. The share carrying >= 2 is the price of the claim that C.3.g's arm split is
    'largely visible' where A.17's was not."""
    return sum((has_fert(rec), has_union(rec), has_house(rec)))


def in_frame(rec):
    """Would the PRODUCTION frame reach this record: DEBT and (FERT or UNION or HOUSE)."""
    return has_debt(rec) and (has_fert(rec) or has_union(rec) or has_house(rec))


def in_fert_only_frame(rec):
    """Would a NARROWER, fertility-only frame reach it. The gap between this and in_frame() is what
    restricting the chapter to its registered outcome would cost at retrieval."""
    return has_debt(rec) and has_fert(rec)


def in_p2_cell(rec):
    """THE HEADLINE PREDICATE. Debt AND policy variation AND a fertility outcome — the cell `200_`
    measured as empty through the query. Every record satisfying this on the CITATION channel is a
    candidate the query could not have found, and is listed by title rather than counted."""
    return has_debt(rec) and has_policy(rec) and has_fert(rec)


def off_career(rec):
    """Wall 1 — health-professions education debt studied for career choice."""
    return any(t in _blob(rec) for t in CAREER_TERMS)


def off_gendebt(rec):
    """Wall 2 — general household liabilities (C.3.e / C.2.c)."""
    return any(t in _blob(rec) for t in GENDEBT_TERMS)


def off_default(rec):
    """Wall 3 — default and repayment behaviour."""
    return any(t in _blob(rec) for t in DEFAULT_TERMS)


def off_parentpay(rec):
    """Walls 5 and 6 — the other two balance sheets: parents saving for, or borrowing for, a
    child's tuition."""
    return any(t in _blob(rec) for t in PARENTPAY_TERMS)


def off_lmic(rec):
    """Wall 7 — LMIC school fees and child marriage. Tagged SECONDARY_LMIC, never deleted."""
    return any(t in _blob(rec) for t in LMIC_TERMS)


def exact_outcome_rate(seed_id, strict=False):
    """EXACT forward outcome rate from two count-only queries — no sampling, no cap, 2 requests.

    Run for ANY seed whose pull truncated, because a cursor-paged truncation returns the
    high-citation HEAD and not a random sample, and the head carries more outcome vocabulary than
    the tail — so a sampled rate on a capped pull flatters the diagnostic. Returns (n, total) or
    (None, None) on failure: a failed request is UNCONFIRMED, never zero.

    `strict=True` switches from the full outcome vocabulary (fertility OR union OR housing) to the
    FERTILITY-ONLY one. On this chapter that pair is the interesting one: the gap between them is
    how much of the frame is reachable only through the chain arm's outcomes.

    The phrase lists carry NO commas (fatal inside a filter value, and %2C does not save it), no
    `?` (wildcard), and no phrase opening with a boolean word.
    """
    fert_only = ("fertility", "childbearing", "first birth", "births", "childlessness",
                 "number of children", "family size", "transition to parenthood")
    all_outcomes = fert_only + ("marriage", "cohabitation", "homeownership",
                                "household formation", "housing tenure", "living with parents")
    terms = " OR ".join(f'"{t}"' for t in (fert_only if strict else all_outcomes))
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



# Written into the script after the first run and the script re-run, so the log regenerates rather
# than being hand-edited. Empty on the first pass by design.
FRAME_NOTE = """## Findings

*Written after reading the measurements above, then re-run so the log regenerates rather than being
hand-edited.*

- **THE SCOPE'S CENTRAL FINDING IS PARTLY OVERTURNED, AND THE CHANNEL BUILT TO CONTRADICT IT IS WHAT
  DID IT.** The P2 policy-variation cell is not empty. The citation channel surfaced *Experimental
  Evidence on Consumption, Saving, and Family Formation Responses to Student Debt Forgiveness* (SSRN
  2022, `10.2139/ssrn.4139814`, 1 cite, reached independently by THREE seeds) — a randomized
  evaluation of debt forgiveness with a family-formation outcome, which is precisely the study shape
  the scope declared absent from the literature.
- **Why the query missed it, diagnosed rather than guessed.** `200_`'s policy block carried
  `"loan forgiveness"` but not `"debt forgiveness"`; its outcome block carried `"family size"` but
  not `"family formation"`. Adding the first takes that cell from 5 records to 6; adding the second,
  6 to 7. The record has NO indexed abstract, so its title was the only searchable text it ever had.
  **The scope's sentence — "There is no natural experiment in student debt with a fertility outcome
  anywhere in the indexed literature" — is false as written and is corrected.** What survives is
  narrower and still worth reporting: no PUBLISHED, peer-reviewed policy-variation study with a
  fertility outcome exists, and the sole candidate is an uncited preprint that must be retrieved and
  read before any verdict.
- **The generalisable form: an empty-cell finding measured through one hand-written vocabulary block
  is a claim about the block, not about the literature.** It needs a second, orthogonal channel
  before it can be reported as a property of the field. Here the second channel cost one script and
  overturned the first channel's headline.
- **The production frame cannot reach two of its own fifteen empirical anchors, and one is the
  chapter's most-cited primary-cell work.** Nau et al. 2015 scores `debt=False, fert=False`: its
  OpenAlex record carries NO abstract, and its title says *Debt*, not *student debt*, and *baby*,
  not any term in the outcome vocabulary. *Returning to the Nest* fails the same way on the exposure
  axis despite having an abstract. This is the measured price of student-anchoring the exposure,
  which was adopted to defeat the 1,389-record sovereign-debt homonym: the anchoring that defeats
  the homonym also loses the canon. Both rules are right and they conflict; the cost is 2 of 15 and
  it is priced here rather than argued. **Operational consequence: Tier A enters the screen by hand
  and never through the frame.** That is already the practice, and this is the measurement showing
  why it must stay.
- **The identification diagnostic was refuted by its own output.** The first `IDENT_TERMS` carried
  "natural experiment", "quasi-experimental" and "randomi" but no bare "experiment", so it scored the
  run's single most important record — whose title begins *Experimental Evidence* — as NOT
  identified, inside the table built to surface identified policy studies. Across Tier B, 78 records
  name "experiment" and the original list missed 46 of them. Corrected, the count of records carrying
  debt AND a fertility outcome AND an identification strategy goes from 3 to 5.
  `ident_vocab_selftest()` makes a recurrence a start-up failure.
- **Recall(A) settles the two-arm frame decision on evidence rather than on the scope's argument.**
  The production frame reaches 13 of 21 anchors (13 of 15 empirical); a fertility-only frame reaches
  5 of 21. Eight empirical anchors — every identified study in the chapter, Mezza et al., Addo,
  Gicheva and Goodman/Isen/Yannelis among them — are reachable ONLY through the chain arm's outcome
  vocabulary. A frame restricted to the chapter's registered outcome would retrieve none of its
  identified evidence. Same ruling as A.17's loose frame, reached in a different chapter for a
  different reason.
- **The attainment confound is more visible than the scope assumed, and the scope is revised.** It
  was declared unenforceable at title/abstract on the strength of 8 records at query level. Within
  the production frame it is 11 of 39 (28.2%); across Tier B, 6.4%. That is a positive PRIOR at
  screen — the same shape as A.17's Wall 5, where "unenforceable" turned out to be "enforceable with
  an `INSUFFICIENT_INFO` bucket". It stays a full-text extraction field and a risk-of-bias domain,
  and the screen now also carries a flag.
- **The routing-visibility claim holds, on a base too small to lean on.** Within the frame the screen
  will see, 77% of records carry exactly one outcome axis and are routable; 23% carry two or three
  and must be routed at full text. The claim was asserted about vocabulary and is now measured — but
  the base is 39 records, so this is weak confirmation, and the 23% is the number to watch.
- **No seed truncated.** Every forward pull returned its full count, so no exact-rate correction was
  needed and no fraction reported here is a high-citation-head artifact. Stated because the opposite
  has bitten this project, and because a reader cannot tell the difference from the table alone.
- **The two channels barely overlap, which is what makes Recall(B) meaningful here.** Tier B is 2,071
  records and only 39 (1.9%) sit inside the production query frame. 31% depend on a decoy, review,
  exposure-series or negative-control seed alone and are droppable from any recall computation via
  `seed_ids`.
- **One more record for the screen's attention, surfaced by the corrected diagnostic:** *Does the
  Student-Loan Burden Weigh into the Decision to Start a Family?* (2011, 22 cites) carries debt, a
  fertility outcome and identification language. It was visible in `199_` under the marriage cell and
  is a direct-arm candidate, not a chain-arm one."""

def main():
    gate_selftest()             # first-author gate: survives degraded metadata AND still refuses reviewers
    ident_vocab_selftest()      # the identification list must see the designs it exists to find
    anchors = json.load(open(ANCHORS))
    verified = [a for a in anchors if a.get("identity_verified") and a.get("doi")]

    # C.3.g's cells. The split here is NOT A.17's two-arms-two-questions and NOT A.24's
    # reachable-vs-unreachable. It is between the chapter's REGISTERED estimand (direct) and a
    # neighbouring link of its own stated mechanism (chain). Both are in scope; only one is the
    # recall denominator, and they are never summed into a single figure.
    DIRECT_CELLS = {"P1_DEBT_FERTILITY", "P6_INTENTIONS"}
    CHAIN_CELLS = {"P3_MARRIAGE", "P4_HOUSING"}
    MECH_CELLS = {"P5_RESOURCE"}
    EMPIRICAL_CELLS = DIRECT_CELLS | CHAIN_CELLS

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
        # ANCHOR-LEVEL RECALL. Would the production frame reach this anchor's OWN record, and would
        # a fertility-only frame? The gap between the two columns is what narrowing the chapter to
        # its registered outcome would cost at retrieval, computed per anchor rather than argued.
        rec["self_debt"] = has_debt(w["row"])
        rec["self_fert"] = has_fert(w["row"])
        rec["self_union"] = has_union(w["row"])
        rec["self_house"] = has_house(w["row"])
        rec["self_in_frame"] = in_frame(w["row"])
        rec["self_in_fert_frame"] = in_fert_only_frame(w["row"])
        tier_a.append(rec)
        seedinfo.append((rec, w))
    json.dump(tier_a, open(OUT_A, "w"), indent=2)

    pool, log_rows = {}, []
    for rec, w in seedinfo:
        sid = rec["openalex_id"]
        cell = cell_of(rec)
        is_emp = cell in EMPIRICAL_CELLS
        back = fetch_ids(w["referenced_works"])
        # Empirical seeds are the recall spine and get an unbounded pull. Decoys, the review, the
        # exposure series and the negative control take the ordinary forward cap.
        cap = 10 ** 6 if is_emp else FORWARD_CAP
        fwd, total, truncated = citing(sid, cap)
        n = len(fwd)
        f = lambda pred: (sum(1 for r in fwd if pred(r)) / n) if n else None
        c = lambda pred: sum(1 for r in fwd if pred(r))
        exact_n, exact_tot = (exact_outcome_rate(sid) if truncated else (None, None))
        exact_s, exact_st = (exact_outcome_rate(sid, strict=True) if truncated else (None, None))
        for r in back:
            pl = pool.setdefault(r["id"], {**r, "seed_ids": [], "channels": set()})
            pl["seed_ids"].append(sid); pl["channels"].add("backward")
        for r in fwd:
            pl = pool.setdefault(r["id"], {**r, "seed_ids": [], "channels": set()})
            pl["seed_ids"].append(sid); pl["channels"].add("forward")
        log_rows.append(dict(title=rec["title"][:50], cell=cell, seed=sid, empirical=is_emp,
                             direct=cell in DIRECT_CELLS, chain=cell in CHAIN_CELLS,
                             n_back=len(back), n_fwd=n, fwd_total=total, truncated=truncated,
                             debt=f(has_debt), fert=f(has_fert), union=f(has_union),
                             house=f(has_house), ident=f(has_ident), policy=f(has_policy),
                             attain=f(has_attain),
                             frame=f(in_frame), n_frame=c(in_frame),
                             fert_frame=f(in_fert_only_frame), n_fert_frame=c(in_fert_only_frame),
                             n_p2=c(in_p2_cell),
                             career=f(off_career), gendebt=f(off_gendebt), default=f(off_default),
                             parentpay=f(off_parentpay), lmic=f(off_lmic),
                             exact_loose=exact_n, exact_total=exact_tot,
                             exact_strict=exact_s, exact_strict_total=exact_st))
        pcp = lambda v: f"{v:.0%}" if v is not None else "n/a"
        print(f"  {cell[:22]:<22} back={len(back):>4} fwd={n:>5}/{total or 0:<6} "
              f"frame={pcp(log_rows[-1]['frame']):>4} fert={pcp(log_rows[-1]['fert_frame']):>4} "
              f"P2={c(in_p2_cell):>3}  {rec['title'][:26]}")

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
    decoy_seeds = {r["openalex_id"] for r in tier_a
                   if r["provisional_cell"].startswith(("OFF_", "REVIEW", "EXPOSURE", "NEGATIVE"))}
    n_decoy_dep = sum(1 for r in tier_b if set(r["seed_ids"]) <= decoy_seeds)
    direct = [r for r in tier_a if r["provisional_cell"] in DIRECT_CELLS]
    chain = [r for r in tier_a if r["provisional_cell"] in CHAIN_CELLS]

    # ---- MEASUREMENT 1: the P2 cell, on the ORTHOGONAL channel ----
    p2_hits = [r for r in tier_b if in_p2_cell(r)]
    p2_hits.sort(key=lambda r: -(r["cited_by_count"] or 0))
    # An identified subset of those hits is the strongest version of the test: policy variation,
    # a fertility outcome AND an identification strategy named.
    p2_ident = [r for r in p2_hits if has_ident(r)]

    # ---- MEASUREMENT 2: outcome-axis multiplicity (the routing-visibility claim) ----
    axes = [n_outcome_axes(r) for r in tier_b]
    ax = {k: sum(1 for a in axes if a == k) for k in (0, 1, 2, 3)}
    ax_tot = max(len(axes), 1)
    # Restricted to records the frame would actually retrieve — the screen never sees the rest.
    in_frame_b = [r for r in tier_b if in_frame(r)]
    axes_f = [n_outcome_axes(r) for r in in_frame_b]
    axf = {k: sum(1 for a in axes_f if a == k) for k in (0, 1, 2, 3)}
    axf_tot = max(len(axes_f), 1)

    # ---- MEASUREMENT 3: the attainment confound ----
    b_attain = sum(1 for r in tier_b if has_attain(r))
    b_attain_inframe = sum(1 for r in in_frame_b if has_attain(r))

    # ---- MEASUREMENT 4: Recall(A) under both frames ----
    a_frame = sum(1 for r in tier_a if r.get("self_in_frame"))
    a_fert = sum(1 for r in tier_a if r.get("self_in_fert_frame"))
    emp_anchors = direct + chain
    ea_frame = sum(1 for r in emp_anchors if r.get("self_in_frame"))
    ea_fert = sum(1 for r in emp_anchors if r.get("self_in_fert_frame"))
    lost_by_narrowing = [r for r in emp_anchors
                         if r.get("self_in_frame") and not r.get("self_in_fert_frame")]

    b_frame = sum(1 for r in tier_b if in_frame(r))
    b_fert_frame = sum(1 for r in tier_b if in_fert_only_frame(r))
    b_ident = sum(1 for r in tier_b if has_ident(r))
    b_ident_fert = sum(1 for r in tier_b if has_ident(r) and has_fert(r) and has_debt(r))

    pc = lambda v: f"{v:.1%}" if v is not None else "n/a"
    L = [f"# A4 Tier A / Tier B citation frame — {SLUG} (C.3.g)", "",
         f"**Tier A: {len(tier_a)} seeding anchors** — {len(direct)} direct-arm "
         f"(the registered estimand), {len(chain)} chain-arm (link 1), "
         f"{len(tier_a) - len(direct) - len(chain)} mechanism, review, exposure-series, "
         f"routing-decoy or negative-control.", "",
         f"**Tier B: {len(tier_b):,} records** — one hop from those anchors, backward and forward, "
         f"deduplicated on OpenAlex id. {n_multi:,} ({n_multi / max(len(tier_b), 1):.0%}) are "
         f"reached by more than one seed; {n_abs:,} ({n_abs / max(len(tier_b), 1):.0%}) carry an "
         f"abstract; {n_decoy_dep:,} ({n_decoy_dep / max(len(tier_b), 1):.0%}) depend on a decoy, "
         f"review, exposure-series or negative-control seed alone and can be dropped from any "
         f"recall computation via `seed_ids`.", "",
         "Every fraction below is computed AFTER retrieval. None was applied as a filter — pruning "
         "the forward pull by topic vocabulary would shrink Tier B by distance from the production "
         "query and make Recall(B) circular.", "",
         "## Measurement 1 — is the P2 policy-variation cell really empty?", "",
         "`200_` measured it empty THROUGH THE QUERY. A query can only report the absence of what "
         "its own vocabulary reaches, so the same question is asked here through the citation "
         "channel, which is orthogonal to it by construction. The POLICY vocabulary used is "
         "deliberately generous — an over-broad list makes the empty-cell finding harder to "
         "sustain, which is the direction an honest test errs in.", "",
         f"**Tier-B records carrying DEBT and POLICY and FERTILITY: {len(p2_hits)}.**  "
         f"**Of those, naming an identification strategy: {len(p2_ident)}.**", ""]
    if p2_hits:
        L += ["Listed by title rather than counted, because each one is a candidate the query "
              "could not have found and has to be read:", "",
              "| Cites | Year | Title | Identified |", "|---|---|---|---|"]
        for r in p2_hits[:40]:
            L.append(f"| {r['cited_by_count'] or 0:,} | {r.get('year') or ''} | "
                     f"{r['title'][:88].replace('|', '/')} | "
                     f"{'yes' if has_ident(r) else 'no'} |")
        if len(p2_hits) > 40:
            L.append(f"| | | *... and {len(p2_hits) - 40} more, in the Tier-B JSON* | |")
        L += ["", "**These are candidates, not findings.** A record carrying all three "
              "vocabularies may still be a passing mention, a review, or an LMIC school-fee study "
              "(Wall 7). The screen decides. What matters for the scope is whether the list is "
              "empty, and it is not — so the empty-cell claim is now a claim about what SURVIVES "
              "screening, not about what exists, and the scope must be restated in those terms.", ""]
    else:
        L += ["**The list is empty.** The citation channel, searched with a deliberately generous "
              "policy vocabulary, finds no record carrying debt, policy variation and a fertility "
              "outcome together. `200_`'s query-level finding survives a channel built to "
              "contradict it, and the scope's central result stands on two independent channels "
              "rather than one.", ""]
    L += ["## Measurement 2 — is the arm routing visible at title and abstract?", "",
          "The scope asserts that C.3.g's arm split is 'largely visible' where A.17's was not, "
          "because the outcome word distinguishes the arms. A record carrying exactly ONE of the "
          "three outcome vocabularies is routable at screen; one carrying two or three is not.", "",
          "| Outcome axes carried | All Tier B | Within the production frame |", "|---|---|---|"]
    for k in (0, 1, 2, 3):
        L.append(f"| {k} | {ax[k]:,} ({ax[k] / ax_tot:.0%}) | {axf[k]:,} ({axf[k] / axf_tot:.0%}) |")
    routable = axf[1] / axf_tot
    L += ["", f"**Within the frame the screen will actually see, {routable:.0%} of records carry "
          f"exactly one outcome axis and are routable; {(axf[2] + axf[3]) / axf_tot:.0%} carry two "
          f"or three and must be routed at full text.**", "",
          "## Measurement 3 — the attainment confound, sized", "",
          f"The scope declared attainment-conditioning unenforceable at title/abstract on the "
          f"strength of 8 records at query level, and routed it to full-text extraction and a "
          f"risk-of-bias domain. Across Tier B, {b_attain:,} records "
          f"({b_attain / max(len(tier_b), 1):.1%}) name attainment-conditioning language; within "
          f"the production frame, {b_attain_inframe:,} of {len(in_frame_b):,} "
          f"({b_attain_inframe / max(len(in_frame_b), 1):.1%}).", "",
          "## Measurement 4 — Recall(A): would the frame reach its own anchors?", "",
          f"| Frame | Reaches, all {len(tier_a)} anchors | Reaches, {len(emp_anchors)} empirical |",
          "|---|---|---|",
          f"| Production: DEBT and (FERT or UNION or HOUSE) | {a_frame}/{len(tier_a)} | "
          f"{ea_frame}/{len(emp_anchors)} |",
          f"| Narrower: DEBT and FERT only | {a_fert}/{len(tier_a)} | {ea_fert}/{len(emp_anchors)} |",
          ""]
    if lost_by_narrowing:
        L += [f"**{len(lost_by_narrowing)} empirical anchors are reachable only through the chain "
              f"arm's outcome vocabulary** — a fertility-only frame loses them, and with them the "
              f"chapter's identified evidence:", ""]
        for r in lost_by_narrowing:
            L.append(f"- *{r['title'][:78]}* ({r['provisional_cell']})")
        L.append("")
    L += [f"Tier B under the production frame: {b_frame:,} records "
          f"({b_frame / max(len(tier_b), 1):.1%}); under the fertility-only frame "
          f"{b_fert_frame:,} ({b_fert_frame / max(len(tier_b), 1):.1%}). Records naming an "
          f"identification strategy: {b_ident:,}; naming one AND debt AND a fertility outcome: "
          f"**{b_ident_fert:,}** — the scope's central asymmetry, re-measured on the citation "
          f"channel.", "",
          "## Per-seed detail", "",
          "`frame` = share of the seed's forward citers the production frame would reach. "
          "`fert` = share the fertility-only frame would reach. `P2` = count carrying debt, policy "
          "and fertility together. A truncated pull is the high-citation HEAD, not a random "
          "sample, so any truncated seed also carries an EXACT count from two count-only queries.",
          "",
          "| Cell | Anchor | back | fwd | frame | fert-only | ident | policy | P2 | career | gen-debt |",
          "|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in log_rows:
        trunc = " *(trunc)*" if r["truncated"] else ""
        L.append(f"| `{r['cell']}` | {r['title'][:34]} | {r['n_back']} | "
                 f"{r['n_fwd']}/{r['fwd_total'] or 0}{trunc} | {pc(r['frame'])} | "
                 f"{pc(r['fert_frame'])} | {pc(r['ident'])} | {pc(r['policy'])} | {r['n_p2']} | "
                 f"{pc(r['career'])} | {pc(r['gendebt'])} |")
    trunc_rows = [r for r in log_rows if r["truncated"]]
    if trunc_rows:
        L += ["", "### Exact rates for truncated pulls", "",
              "| Anchor | sampled frame-rate | EXACT outcome / total | EXACT fert-only / total |",
              "|---|---|---|---|"]
        for r in trunc_rows:
            L.append(f"| {r['title'][:40]} | {pc(r['frame'])} | "
                     f"{r['exact_loose']}/{r['exact_total']} | "
                     f"{r['exact_strict']}/{r['exact_strict_total']} |")
    if recovery_report:
        L += ["", "### DOI-less anchor seed recovery", "",
              "Every anchor without a DOI gets ONE gated recovery attempt. An anchor that cannot "
              "seed is a hole in the frame and is reported as one.", "",
              "| Anchor | book | recovered | note |", "|---|---|---|---|"]
        for t, isbk, rid, note, cites in recovery_report:
            L.append(f"| {t} | {'yes' if isbk else 'no'} | {'`' + rid + '`' if rid else '**no**'} | "
                     f"{(note or '')[:60]} |")
    L += ["", "## Walls, sized inside the citation neighbourhood", "",
          "`199_` sized each wall against the whole literature. These are their sizes where the "
          "screen will actually meet them — inside the frame, not outside it.", "",
          "| Wall | Share of Tier B | Share within the production frame |", "|---|---|---|"]
    for nm, pred in (("1 — health-professions career", off_career),
                     ("2 — general household debt", off_gendebt),
                     ("3 — default and repayment", off_default),
                     ("5/6 — parents' balance sheet", off_parentpay),
                     ("7 — LMIC school fees", off_lmic)):
        a_ = sum(1 for r in tier_b if pred(r))
        b_ = sum(1 for r in in_frame_b if pred(r))
        L.append(f"| {nm} | {a_:,} ({a_ / max(len(tier_b), 1):.1%}) | "
                 f"{b_:,} ({b_ / max(len(in_frame_b), 1):.1%}) |")
    L += ["", FRAME_NOTE, ""]
    open(OUT_LOG, "w").write("\n".join(L) + "\n")
    json.dump(cache, open(CACHE, "w"), indent=0)
    print(f"\nTier A {len(tier_a)}  Tier B {len(tier_b):,}  in-frame {b_frame:,}  "
          f"P2-candidates {len(p2_hits)}  ident+fert+debt {b_ident_fert}")
    print(f"-> {os.path.relpath(OUT_A, ROOT)}")
    print(f"-> {os.path.relpath(OUT_B, ROOT)}")
    print(f"-> {os.path.relpath(OUT_LOG, ROOT)}")


if __name__ == "__main__":
    main()
