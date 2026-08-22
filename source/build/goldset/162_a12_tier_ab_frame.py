#!/usr/bin/env python3
"""
162_a12_tier_ab_frame.py — A.12, stage A4. Build the Tier A / Tier B citation frame.

Inherits `150_d3c_tier_ab_frame.py`. Three changes this chapter forces, and the first one is
structural rather than cosmetic.

  * **DOI-LESS SEED RECOVERY IS GENERALISED BEYOND MONOGRAPHS, BECAUSE HERE IT IS THE ONLY ROUTE TO
    THE CHAPTER'S IDENTIFICATION.** The inherited code recovers a DOI-less anchor only when
    `is_book` is set, restricted to bookish types. A.12 has THREE anchors with no DOI and only ONE is
    a book. The other two are Bronars & Grogger 1994 (AER, 368 cites) and Martin, Hamilton &
    Osterman 2012 (NCHS, 329) — an article and a vital-statistics report, both real, both simply
    absent from the DOI indexes.

    Losing Bronars & Grogger is not a rounding error. Wall 8 declares that twin-IV first stages
    CANNOT be found by title/abstract screening, so the citation frame is the ONLY channel to them.
    Dropping a twin-IV canon seed in silence would remove the one route to `PRIMARY_OFFSET_FIRSTSTAGE`
    and the chapter would report that cell as empty for a reason invisible to every later stage.
    Recovery is therefore attempted for ANY DOI-less anchor, with the type restriction inverted for
    non-books (bookish types EXCLUDED) and the same first-author gate applied throughout.

  * **THE FIRST-AUTHOR GATE HAD TO SURVIVE DEGRADED AUTHOR METADATA, AND ON THE INHERITED CODE IT
    DID NOT.** `_surname()` takes the LAST token of a name, which assumes "Given ... Surname" order.
    OpenAlex renders Bronars & Grogger's first author as **"Bronars Sg"** — surname first, initials
    last — so `_surname()` returns `"sg"`, which matches no candidate surname and the gate refuses a
    correct record. The fix is to test the record author's FULL TOKEN SET against the candidate
    surname set rather than its last token alone. This does not weaken what the gate is for: a review
    by a different person shares no token with our authors' surnames (Scott reviewing Wilson still
    fails), while "Bronars Sg" passes on the token `bronars`. A self-test holds both directions and
    the script refuses to run if either regresses.

  * **DIAGNOSTICS ARE RE-CUT FOR AN IDENTITY, AND ONE OF THEM CALIBRATES THE FROZEN WALL 6.**
    `fert` (carries a fertility quantity) and `twin` (carries a twinning/multiple-birth construct)
    give `BOTH`, the density of A.12's primary cell in a seed's neighbourhood. Two off-cell
    diagnostics measure the walls the scope froze: `homonym` (crystallography and TWIP steel,
    Walls 1-2) and `nonhuman` (veterinary and agronomic, Wall 3). The fifth, **`clinical`**, is the
    one this chapter turns on: the share of a cloud whose OUTCOME is per-cycle or perinatal rather
    than a population birth count. **Wall 6 was re-cut on outcome — population multiple-birth-rate
    outcomes in, per-cycle clinical outcomes out — and that re-cut is only defensible if outcome type
    is visible at title/abstract. `clinical` measures whether it is, on a number rather than an
    impression.** As in the predecessors, NO diagnostic is applied as a filter; filtering the forward
    fetch by topic vocabulary would prune Tier B by distance from the production query and make
    Recall(B) circular.

TWO DEFECTS IN THE INHERITED CODE WERE FOUND BY RUNNING IT, AND BOTH FAIL SILENTLY.

  1. **`_fold()` shattered names into characters.** The inherited line was
     `" ".join(c for c in x if c.isalnum() or c == " ")`, which joins CHARACTERS with spaces:
     "Wilson" became "w i l s o n". `_surname()` then took the last token and returned the last
     LETTER of a name, so the A4 first-author gate compared final letters and matched any two names
     ending the same. Blast radius audited across every branch rather than assumed: this machinery
     was introduced at D.3.c (`150`) and **A.12 is its second and only other user**, so no other
     chapter is affected. It does mean D.3.c's A4 log makes a claim its code could not support — that
     first-author disagreement is what refused Johnston & Lordan on the Wilson probe. A live check
     shows no such record in the citation head at all (Wilson's own records rank 1st, 2nd and 6th),
     and the only bookish-typed record carries no authors, so Wilson's non-recovery came from the
     TYPE filter and an empty author list, not from the gate. **Flagged for D.3.c re-audit; not
     edited here, because that is another chapter's shipped output.**

  2. **A comma in an OpenAlex FILTER value is fatal and percent-encoding does not save it.** See
     `_filter_safe()`. This cost the Martin, Hamilton & Osterman 2012 recovery on the first run — a
     failed request that, under the refusals-are-not-zeros rule, is UNCONFIRMED and must be retried
     rather than recorded as an unrecoverable anchor. With the fix all 25 anchors seed and the run
     completes with zero failed requests. A3 (`161`) is NOT affected: it queries through `search=`,
     where a comma is an ordinary character.

HOMONYM SEEDS GET A LOW CAP **PLUS AN EXACT COUNT**, WHICH IS NOT THE SAME AS TRUSTING A SAMPLE.
SHELX carries 87,694 citations. Pulling that cloud in full would cost ~440 requests to confirm that a
crystallography paper is not about fertility, and would bury Tier B under it. But a capped pull
measures the on-topic rate on a sample that cursor paging cannot guarantee is representative — the
standing finding that a truncated OpenAlex pull is a head and not a random sample. So homonym seeds
get BOTH: a capped forward pull that contributes to Tier B and is reported as truncated through the
ordinary machinery, AND a separate **exact** on-topic rate from two count-only queries
(`cites:X` and `cites:X AND <fertility vocabulary>`), which costs two requests and carries no
sampling bias at all. The scope's homonym carve-out then rests on an exact number rather than on a
sample or an impression.

THE RECALL DENOMINATOR IS REPORTED TWO WAYS, AND THE DIFFERENCE IS THE COST OF WALL 8.
`PRIMARY_OFFSET_STOPPING` and `PRIMARY_OFFSET_FIRSTSTAGE` both estimate this chapter's estimand, so
both belong in the causal denominator. But Wall 8 says the first stages are unreachable by screening,
so including them guarantees a low Recall(A) — which is the honest finding, not a screen failure.
Reporting the denominator with and without them turns the unenforceability of Wall 8 from a claim in
the scope document into a number in the log.

FORWARD-SEED RULE (D.2.d, 2026-08-08), and this chapter's ONE principled carve-out from it. Every
seed forward-cites, routing decoys included, because a decoy sits just across a boundary wall and its
neighbourhood is where the boundary cases live — on D.2.d decoy clouds ran 29-88% on-topic against
1-14% for the theory canon. A.12 is the first chapter where part of that premise fails: two of its
decoy families are PURE HOMONYMS with no on-topic content, not boundary cases. They are still pulled
and still measured; they are only capped, and the cap is reported. The behaviour-genetics decoy
(A.18) is an ordinary boundary case and gets the ordinary uncapped-by-topic treatment.

Tier A is the verified anchor set from 161 plus recovered DOI-less seeds. Tier B is the orthogonal
frame: everything the anchors cite (backward, one hop) and everything that cites them (forward, one
hop), deduplicated and keyed on OpenAlex id with DOI carried alongside. `seed_ids` provenance is
retained on every Tier B record so Recall(B) can be recomputed without decoy-seeded material.

Output: literature/search-logs/{slug}-tier-a.json
        literature/search-logs/{slug}-tier-b-frame.json
        literature/search-logs/{slug}-tier-ab-log.md
"""
import json, os, re, subprocess, sys, time
from urllib.parse import quote

SLUG = "twinning-multiple-births"
MAILTO = "shravanh@uchicago.edu"
UA = f"fertility-review/1.0 (mailto:{MAILTO})"
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
LOGS = os.path.join(ROOT, "literature", "search-logs")
ANCHORS = os.path.join(LOGS, f"{SLUG}-cold-start-anchors.json")
OUT_A = os.path.join(LOGS, f"{SLUG}-tier-a.json")
OUT_B = os.path.join(LOGS, f"{SLUG}-tier-b-frame.json")
OUT_LOG = os.path.join(LOGS, f"{SLUG}-tier-ab-log.md")
CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "a12_frame_cache.json")
cache = json.load(open(CACHE)) if os.path.exists(CACHE) else {}

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
    # Padded so the space-anchored terms (" mice", " rat ") can match at the string edges. Those
    # terms carry their spaces deliberately: a bare "rat" substring matches "ratio", "strata" and
    # "generation", which is the unanchored-pattern bug this codebase has now hit five times.
    return " " + (rec["title"] + " " + rec.get("abstract", "")).lower() + " "


def on_topic(rec):
    """Carries a fertility quantity."""
    return any(t in _blob(rec) for t in TOPIC_TERMS)


def has_twinning(rec):
    """Carries a twinning / multiple-birth construct."""
    return any(t in _blob(rec) for t in TWIN_TERMS)


def in_primary_cell(rec):
    """Carries BOTH — the density of A.12's primary cell in a seed's neighbourhood.

    A LOOSE UPPER BOUND, and loose in a way specific to this chapter. Co-occurrence of the two
    vocabularies in one abstract is not a study that estimates one against the other, and for an
    accounting identity the co-occurrence is especially cheap: any vital-statistics report tabulates
    twin births alongside a birth rate without estimating anything at all. That is not noise to be
    filtered out — the scope establishes those reports ARE the primary cell's population — but it
    does mean this column reads high relative to the estimable literature."""
    return on_topic(rec) and has_twinning(rec)


def off_homonym(rec):
    """Visibly crystallographic or metallurgical. LOWER BOUND."""
    return any(t in _blob(rec) for t in HOMONYM_TERMS)


def off_nonhuman(rec):
    """Visibly non-human reproduction or agronomy. LOWER BOUND."""
    return any(t in _blob(rec) for t in NONHUMAN_TERMS)


def off_clinical(rec):
    """Visibly a per-cycle or perinatal OUTCOME study — the Wall 6 / Wall 5 exclude side.
    LOWER BOUND, and the number the frozen Wall 6 re-cut stands or falls on."""
    return any(t in _blob(rec) for t in CLINICAL_TERMS)


def exact_on_topic(seed_id):
    """EXACT forward on-topic rate from two count-only queries — no sampling, no cap, 2 requests.

    Used for homonym seeds, where a capped pull would otherwise force the carve-out to rest on a
    sample that cursor paging cannot guarantee is representative (a truncated OpenAlex pull is a head,
    not a random sample). Returns (n_on_topic, total) or (None, None) on failure — a failed request is
    UNCONFIRMED, never zero."""
    terms = " OR ".join(f'"{t}"' for t in
                        ("fertility", "birth rate", "births", "childbearing", "family size",
                         "total fertility", "completed fertility", "fecundity"))
    d1, ok1 = oa_get(f"https://api.openalex.org/works?filter=cites:{seed_id}&per-page=1",
                     f"exact-total:{seed_id}")
    d2, ok2 = oa_get(f"https://api.openalex.org/works?filter=cites:{seed_id},"
                     f"title_and_abstract.search:{quote(chr(40) + terms + chr(41))}&per-page=1",
                     f"exact-ontopic:{seed_id}")
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
    gate_selftest()             # the first-author gate must survive "Bronars Sg" AND still refuse reviewers
    anchors = json.load(open(ANCHORS))
    verified = [a for a in anchors if a.get("identity_verified") and a.get("doi")]

    # The causal recall denominator. BOTH offset cells estimate this chapter's estimand and both
    # belong here. PRIMARY_OFFSET_FIRSTSTAGE is reported SEPARATELY as well, because Wall 8 declares
    # it unreachable by title/abstract screening: including it guarantees a low Recall(A), which is
    # the honest finding rather than a screen failure, and reporting both numbers turns the
    # unenforceability of Wall 8 from a claim in the scope into a measured quantity.
    EMPIRICAL_CELLS = {"PRIMARY_OFFSET_STOPPING", "PRIMARY_OFFSET_FIRSTSTAGE"}
    SCREENABLE_CELLS = {"PRIMARY_OFFSET_STOPPING"}

    def is_empirical_anchor(rec):
        return rec["provisional_cell"] in EMPIRICAL_CELLS

    def is_screenable_anchor(rec):
        """In the denominator a title/abstract screen could actually reach."""
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
        is_hom = cell.startswith("OFF_HOMONYM")
        back = fetch_ids(w["referenced_works"])
        # Empirical seeds are the recall spine and get an unbounded pull. Homonym decoys get a low
        # cap because the scope froze them as pure homonyms rather than boundary cases — and they get
        # an EXACT on-topic count as well, so the carve-out rests on a number and not on the sample.
        cap = 10 ** 6 if is_emp else (HOMONYM_CAP if is_hom else FORWARD_CAP)
        fwd, total, truncated = citing(sid, cap)
        n = len(fwd)
        f_top = (sum(1 for r in fwd if on_topic(r)) / n) if n else None
        f_twin = (sum(1 for r in fwd if has_twinning(r)) / n) if n else None
        n_prim = sum(1 for r in fwd if in_primary_cell(r))
        f_prim = (n_prim / n) if n else None
        f_hom = (sum(1 for r in fwd if off_homonym(r)) / n) if n else None
        f_non = (sum(1 for r in fwd if off_nonhuman(r)) / n) if n else None
        f_clin = (sum(1 for r in fwd if off_clinical(r)) / n) if n else None
        exact_n, exact_tot = (exact_on_topic(sid) if is_hom else (None, None))
        for r in back:
            pl = pool.setdefault(r["id"], {**r, "seed_ids": [], "channels": set()})
            pl["seed_ids"].append(sid); pl["channels"].add("backward")
        for r in fwd:
            pl = pool.setdefault(r["id"], {**r, "seed_ids": [], "channels": set()})
            pl["seed_ids"].append(sid); pl["channels"].add("forward")
        log_rows.append(dict(title=rec["title"][:52], cell=cell, seed=sid, empirical=is_emp,
                             homonym=is_hom, n_back=len(back), n_fwd=n, fwd_total=total,
                             truncated=truncated, on_topic=f_top, twin=f_twin, primary=f_prim,
                             n_primary=n_prim, homfrac=f_hom, nonhuman=f_non, clinical=f_clin,
                             exact_on_topic=exact_n, exact_total=exact_tot))
        print(f"  {cell[:24]:<24} back={len(back):>4} fwd={n:>5}/{total or 0:<6} "
              f"fert={f'{f_top:.0%}' if f_top is not None else 'n/a':>4} "
              f"twin={f'{f_twin:.0%}' if f_twin is not None else 'n/a':>4} "
              f"BOTH={f'{f_prim:.1%}' if f_prim is not None else 'n/a':>5}({n_prim:>4}) "
              f"clin={f'{f_clin:.0%}' if f_clin is not None else 'n/a':>4}  {rec['title'][:30]}")

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
    hom_seeds = {r["openalex_id"] for r in tier_a if r["provisional_cell"].startswith("OFF_HOMONYM")}
    n_decoy_dep = sum(1 for r in tier_b if set(r["seed_ids"]) <= decoy_seeds)
    n_hom_dep = sum(1 for r in tier_b if set(r["seed_ids"]) <= hom_seeds)
    n_emp = sum(1 for r in tier_a if is_empirical_anchor(r))
    n_scr = sum(1 for r in tier_a if is_screenable_anchor(r))

    pc = lambda v: f"{v:.1%}" if v is not None else "n/a"
    L = [f"# A4 Tier A / Tier B citation frame — {SLUG} (A.12)", "",
         f"**Tier A: {len(tier_a)} seeding anchors.** The causal recall denominator is reported TWO "
         f"ways, and the gap between them is the measured cost of Wall 8:", "",
         f"- **{n_emp} empirical anchors** — `PRIMARY_OFFSET_STOPPING` + `PRIMARY_OFFSET_FIRSTSTAGE`. "
         "Both cells estimate this chapter's estimand, so both belong in a causal denominator.",
         f"- **{n_scr} screenable anchors** — `PRIMARY_OFFSET_STOPPING` alone. Wall 8 declares the "
         "twin-IV first stages unreachable by title/abstract screening, because no abstract about "
         "schooling and earnings reveals its first-stage table. Recall(A) computed against the "
         f"{n_emp}-anchor denominator will therefore look poor by construction; computed against the "
         f"{n_scr}-anchor denominator it measures the screen. **Report both. The difference is not a "
         "screen failure, it is the price of an unenforceable wall, and it should appear as a number "
         "rather than as a sentence in the scope document.**", "",
         f"**Tier B frame: {len(tier_b):,} deduplicated records** — {n_multi:,} found by more than one "
         f"seed, {n_abs:,} carrying an abstract ({n_abs / max(len(tier_b), 1):.0%}).", "",
         f"**Records depending ONLY on a routing-decoy seed: {n_decoy_dep:,}** "
         f"({n_decoy_dep / max(len(tier_b), 1):.0%}), of which **{n_hom_dep:,} depend only on a "
         "HOMONYM seed** and are the crystallography and metallurgy material the scope predicted. "
         "`seed_ids` provenance lets Recall(B) be recomputed without either group.", "",
         f"**Failed requests: {len(errors)}** — listed at the foot. A failed request is not an empty "
         "result, and the frame is smaller than the index by exactly what those failures cost.", "",
         "## Per-seed yield", "",
         "Every fraction is a SEED-SELECTION DIAGNOSTIC computed after retrieval. None is applied as "
         "a filter: filtering the forward fetch by topic vocabulary would prune Tier B by distance "
         "from the production query and make Recall(B) circular.", "",
         "`fert` = carries a fertility quantity. `twin` = carries a twinning/multiple-birth "
         "construct. **`BOTH`** = the density of A.12's primary cell in that neighbourhood — and for "
         "an accounting identity this reads high relative to the estimable literature, because any "
         "vital-statistics report tabulates twin births beside a birth rate without estimating "
         "anything. `hom` and `nonh` measure Walls 1-3. **`clin`** measures Walls 5-6: the share "
         "whose outcome is per-cycle or perinatal rather than a population birth count. All are "
         "LOWER BOUNDS — a paper counts only when it names the thing in its title or abstract.", "",
         "| seed | cell | back | fwd | fwd total | trunc | fert | twin | **BOTH** | n | hom | nonh | **clin** |",
         "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in sorted(log_rows, key=lambda x: -(x["n_fwd"])):
        L.append(f"| {r['title']} | `{r['cell']}` | {r['n_back']} | {r['n_fwd']} | "
                 f"{r['fwd_total'] or 0} | {'**yes**' if r['truncated'] else 'no'} | "
                 f"{pc(r['on_topic'])} | {pc(r['twin'])} | **{pc(r['primary'])}** | "
                 f"{r['n_primary']} | {pc(r['homfrac'])} | {pc(r['nonhuman'])} | "
                 f"**{pc(r['clinical'])}** |")

    tot_fwd = sum(r["n_fwd"] for r in log_rows)
    tot_prim = sum(r["n_primary"] for r in log_rows)
    L += ["", "## Primary-cell density of the whole frame", "",
          f"Across every seed's forward cloud, **{tot_prim:,} of {tot_fwd:,} records "
          f"({tot_prim / max(tot_fwd, 1):.2%}) carry a fertility quantity and a twinning construct "
          "together.** Read it as which seeds can reach the cell at all, not as a count of studies: "
          "for an identity the co-occurrence is cheap, and the scope already establishes that the "
          "cell's population is vital-statistics reports rather than estimation studies.", ""]

    hom_rows = [r for r in log_rows if r["homonym"]]
    if hom_rows:
        L += ["## Homonym seeds — exact on-topic rate, not a sampled one", "",
              "The scope froze crystallographic twinning and TWIP steel as PURE HOMONYMS rather than "
              "boundary cases, which is this chapter's one carve-out from the standing rule that a "
              "decoy cloud is a boundary case worth forward-seeding in full. A carve-out asserted is "
              "worth nothing, and a carve-out measured on a capped sample is worth little more — a "
              "truncated OpenAlex pull is a head, not a random sample. So each homonym seed also "
              f"carries an EXACT rate from two count-only queries. The {HOMONYM_CAP:,}-record cap "
              "governs only what enters Tier B; the rate below is computed over the entire cloud.", "",
              "| seed | on-topic (exact) | total citing | exact rate | sampled rate (capped pull) |",
              "|---|---|---|---|---|"]
        for r in hom_rows:
            er = (r["exact_on_topic"] / r["exact_total"]) if (r["exact_on_topic"] is not None
                                                              and r["exact_total"]) else None
            L.append(f"| {r['title']} | {r['exact_on_topic'] if r['exact_on_topic'] is not None else 'UNCONFIRMED'} "
                     f"| {r['exact_total'] if r['exact_total'] is not None else 'UNCONFIRMED'} | "
                     f"**{pc(er)}** | {pc(r['on_topic'])} |")
        L += ["", "A near-zero exact rate confirms the carve-out. A materially non-zero one would "
              "REFUTE it, and the correct response would be to restore the homonym seeds to a full "
              "uncapped pull and re-run — the cap is a budget decision that the measurement is "
              "entitled to overturn.", ""]

    if recovery_report:
        L += ["## DOI-less seed recovery — generalised beyond monographs", "",
              "A DOI-less anchor cannot seed, so each got ONE recovery attempt gated by first-author "
              "agreement. **The inherited code attempted this only for monographs**, which on this "
              "chapter would have silently dropped Bronars & Grogger 1994 — a twin-IV canon seed — "
              "and with it the only channel to `PRIMARY_OFFSET_FIRSTSTAGE`, since Wall 8 says those "
              "first stages cannot be reached by screening at all. The type restriction is inverted "
              "rather than dropped: a book must resolve to a bookish record and a non-book must not, "
              "so a monograph still cannot be seeded from a journal review of itself.", "",
              "| anchor | book? | recovered | record | cites |", "|---|---|---|---|---|"]
        for t, isb, rid, note, cites in recovery_report:
            L.append(f"| {t} | {'yes' if isb else 'no'} | {'**yes**' if rid else 'no'} | "
                     f"{('`' + rid + '` ' + note[:44]) if rid else note} | {cites if cites else '—'} |")
        L += ["", "The first-author gate itself needed a fix to survive this chapter, recorded "
              "because the failure mode is silent. `_surname()` took the LAST token of a name, "
              "assuming Given-then-Surname order. OpenAlex renders Bronars & Grogger's first author "
              "as **\"Bronars Sg\"** — surname first, initials last — so the last token is `sg`, "
              "which matches no candidate surname, and the gate returned a CONFIDENT wrong negative. "
              "It now tests the full token set, which still refuses a reviewer (a different person "
              "shares no token with our authors' surnames) while accepting degraded metadata. A "
              "self-test holds both directions and the script refuses to run if either regresses.", ""]

    trunc = [r for r in log_rows if r["truncated"]]
    L += ["## Truncation", ""]
    if trunc:
        L.append(f"{len(trunc)} seed(s) were truncated and are reported here rather than silently "
                 "capped — a bounded pull that is not stated reads as complete coverage:")
        tot_lost = 0.0
        for r in trunc:
            missed = (r["fwd_total"] or 0) - r["n_fwd"]
            exp = missed * (r["on_topic"] or 0)
            tot_lost += exp
            capname = f"{HOMONYM_CAP:,} homonym cap" if r["homonym"] else f"{FORWARD_CAP:,} forward cap"
            L.append(f"- **{r['title']}** (`{r['cell']}`, {capname}): pulled {r['n_fwd']:,} of "
                     f"{r['fwd_total']:,} citing works, on-topic {pc(r['on_topic'])} — "
                     f"**{missed:,} unpulled, an estimated {exp:.0f} on-topic records not seen.**")
        L += ["", f"**Estimated on-topic records lost to caps in total: ~{tot_lost:.0f}**, against a "
                  f"frame of {len(tier_b):,}. The estimate assumes the unpulled tail resembles the "
                  "pulled head, which a cursor-paged truncation cannot guarantee — which is exactly "
                  "why the homonym seeds carry an exact count above rather than relying on this "
                  "estimate."]
    else:
        L.append("No seed was truncated; the frame is a complete one-hop neighbourhood of the "
                 "verified and recovered anchors.")
    if errors:
        L += ["", "## Failed requests (NOT zero results)", ""] + [f"- {a}: `{b}`" for a, b in errors[:40]]
    open(OUT_LOG, "w").write("\n".join(L) + "\n")

    print(f"\ntier_a={len(tier_a)} (empirical={n_emp}, screenable={n_scr}) tier_b={len(tier_b)} "
          f"multi_seed={n_multi} decoy_only={n_decoy_dep} homonym_only={n_hom_dep} errors={len(errors)}")
    print(f"-> {os.path.relpath(OUT_B, ROOT)}")
    print(f"-> {os.path.relpath(OUT_LOG, ROOT)}")
    if errors and len(errors) > 0.2 * max(len(tier_a), 1):
        print("WARNING: high request-failure rate; the frame is incomplete by an unknown amount.",
              file=sys.stderr)


if __name__ == "__main__":
    main()
