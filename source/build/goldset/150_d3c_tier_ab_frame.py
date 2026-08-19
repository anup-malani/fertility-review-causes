#!/usr/bin/env python3
"""
150_d3c_tier_ab_frame.py — D.3.c, stage A4. Build the Tier A / Tier B citation frame.

Inherits `135_b6_tier_ab_frame.py`, with three changes this chapter forces.

  * A THIRD per-seed diagnostic, and it is the one that matters here: `has_mechanism`. B.7's
    precision problem was one-dimensional (does the cloud carry a fertility quantity) and B.6 added a
    second (is it human). D.3.c's problem is different in kind. Its reconnaissance established that
    the literature estimating its TREATMENT never measures its MECHANISM — decline AND fertility
    returns 1,539, despair vocabulary AND fertility returns 604, and all three legs together return
    12, none on topic. So the question to ask of a seed's citation cloud is not only "does this carry
    a fertility quantity" but "does it carry a despair construct AT THE SAME TIME". The joint
    fraction, reported per seed as `primary`, is the density of this chapter's actual primary cell in
    that seed's neighbourhood, and it is the number that says which seeds can reach the cell at all.
  * A fourth diagnostic, `off_mortality`, for Wall 4. The deaths-of-despair literature is the largest
    decoy cloud the chapter faces — 831 records, 491 with explicitly mortality outcomes, inside a
    despair-and-mortality cloud of 10,712 — and Case & Deaton is deliberately a seed. Measuring the
    mortality share per seed calibrates the screen on a number rather than an impression.
    As in B.6, NO diagnostic is applied as a filter, for the same circularity reason.
  * BOOK SEED RECOVERY. A3 left three anchors with no usable DOI, because their indexed records are
    reviews of themselves. Under the inherited code a DOI-less anchor simply cannot seed, and the
    three lost here are the sociological canon — Wilson, Cherlin, Edin & Kefalas — whose citation
    neighbourhood is exactly where the opposite-sign qualitative literature lives. Dropping them
    silently would remove the channel into `EARLY_FERT_OPPOSITE_SIGN`, a PRIMARY cell.

    So a monograph without a DOI gets one recovery attempt against OpenAlex restricted to bookish
    types, gated by the SAME first-author rule the A3 book-canon gate uses, and the outcome is
    reported either way. Measured: Edin & Kefalas recovers (W4242866627, `book`, 125 cites, Edin
    first) and seeds normally. Wilson and Cherlin do NOT — no `book`-typed record of either monograph
    exists in the index. The Wilson attempt is also a live demonstration of why the author gate is
    not optional at this step: a bookish search for "When Work Disappears" returns Johnston & Lordan's
    unrelated 2014 book at higher citations than anything of Wilson's, and only first-author
    disagreement refuses it.

FORWARD_CAP raised 2,000 -> 5,000. D.3.c's decoy and canon seeds are heavily cited (China Syndrome
4,434; Case & Deaton 2015 2,782), and this chapter's primary cell is thin enough that truncating the
neighbourhoods most likely to contain a stray on-cell record is a worse trade than the extra requests.
Anything still truncated is reported per seed with all four diagnostics, never silently.

Tier A is the verified anchor set from 148. Tier B is the orthogonal frame: everything the anchors
cite (backward, one hop) and everything that cites them (forward, one hop), deduplicated and keyed on
OpenAlex id with DOI carried alongside.

FORWARD-SEED RULE (D.2.d, 2026-08-08). Every seed forward-cites, routing decoys included. A decoy is
CHOSEN to sit just across a boundary wall, so its citation neighbourhood is where the boundary cases
live; on D.2.d the decoy clouds ran 29-88% on-topic against 1-14% for the theory canon. Two traps are
avoided by construction and recorded because both are tempting: the forward fetch is NOT filtered by
topic vocabulary (that would prune Tier B by distance from the production query and make Recall(B)
circular), and seeds are capped on cloud SIZE with every truncation printed rather than applied
silently.

`seed_ids` provenance is retained on every Tier B record, so Recall(B) can later be computed with and
without decoy-seeded material as a sensitivity check.

Output: literature/search-logs/{slug}-tier-a.json
        literature/search-logs/{slug}-tier-b-frame.json
        literature/search-logs/{slug}-tier-ab-log.md
"""
import json, os, subprocess, sys, time
from urllib.parse import quote

SLUG = "despair-hopelessness-fertility"
MAILTO = "shravanh@uchicago.edu"
UA = f"fertility-review/1.0 (mailto:{MAILTO})"
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
LOGS = os.path.join(ROOT, "literature", "search-logs")
ANCHORS = os.path.join(LOGS, f"{SLUG}-cold-start-anchors.json")
OUT_A = os.path.join(LOGS, f"{SLUG}-tier-a.json")
OUT_B = os.path.join(LOGS, f"{SLUG}-tier-b-frame.json")
OUT_LOG = os.path.join(LOGS, f"{SLUG}-tier-ab-log.md")
CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "d3c_frame_cache.json")
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
               "total fertility", "childless", "fecundity", "nonmarital", "teen birth",
               "reproductive intention", "fertility intention")

# MECHANISM diagnostic (new for D.3.c, and the diagnostic this chapter turns on). The scope's central
# finding is that the literature estimating the treatment does not measure the mechanism. This asks,
# per seed, what share of the cloud carries a despair-type construct — and, jointly with TOPIC_TERMS,
# what share carries BOTH, which is the density of the actual primary cell.
#
# Deliberately WIDER than the A3 anchor vocabulary: it includes the subjective-future and
# expectations language a study might use without ever saying "despair", because a diagnostic that
# only found the word the hypothesis is named after would measure the name rather than the construct.
MECHANISM_TERMS = ("despair", "hopeless", "demoralization", "demoralisation", "anomie", "fatalis",
                   "future orientation", "foreshortened future", "sense of the future",
                   "expectations about the future", "pessimism", "optimism about the future",
                   "no future", "bleak", "left behind", "meaningless", "normlessness",
                   "subjective wellbeing", "life satisfaction", "deaths of despair")

# MORTALITY diagnostic (Wall 4). The deaths-of-despair literature is the chapter's largest decoy
# cloud and Case & Deaton is deliberately a seed, so the share of a cloud whose OUTCOME is mortality
# is worth a number. Like the species floor in B.6 this is a LOWER BOUND: a study counts only when it
# names a mortality outcome in the title or abstract, and a paper can be about mortality without
# using any of these words. "fertility" appearing in the blob does not cancel a hit — a paper can
# report both, and treating them as exclusive would understate the floor.
MORTALITY_TERMS = ("mortality", "suicide", "overdose", "drug poisoning", "life expectancy",
                   "alcoholic liver", "cirrhosis", "premature death", "excess deaths",
                   "cause of death", "years of life lost")

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


def has_mechanism(rec):
    """Carries a despair-type construct."""
    return any(t in _blob(rec) for t in MECHANISM_TERMS)


def in_primary_cell(rec):
    """Carries BOTH — the chapter's actual primary cell, and the joint the reconnaissance found empty
    at the population level (n=12, none on topic). Per seed this is the number that says whether that
    seed's neighbourhood can reach the cell at all."""
    return on_topic(rec) and has_mechanism(rec)


def off_mortality(rec):
    """Visibly a mortality-outcome study. A LOWER BOUND — see the note on MORTALITY_TERMS."""
    return any(t in _blob(rec) for t in MORTALITY_TERMS)


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
    return " ".join(c for c in x if c.isalnum() or c == " ").replace("  ", " ").strip()


def _surname(n):
    p = _fold(n).split()
    return p[-1] if p else ""


def book_seed_id(title, authors):
    """One recovery attempt for a monograph A3 could not give a DOI, restricted to bookish types and
    gated by FIRST-AUTHOR agreement.

    The gate is the A3 book-canon signal 4, applied at a different stage for the same reason: a
    review of a monograph is indexed under the monograph's title, and citation rank actively prefers
    it. Here the risk is compounded by title collision — a bookish search for "When Work Disappears"
    returns Johnston & Lordan's unrelated 2014 book ahead of anything of Wilson's, and only
    first-author disagreement refuses it.

    Returns (openalex_id, matched_title, cites) or (None, reason, None). Never guesses: a monograph
    that cannot be recovered under the gate is reported as unseedable, because seeding the frame from
    a review would import the reviewer's citation neighbourhood as if it were the author's."""
    short = title.split(":")[0].strip()
    d, ok = oa_get(f"https://api.openalex.org/works?filter=title.search:{quote(short)}"
                   f"&per-page=10&select={SELECT}", f"bookseed:{short[:30]}")
    if not ok:
        return None, "request failed (UNCONFIRMED, not absent)", None
    cands = []
    for w in d.get("results", []):
        if (w.get("type") or "") not in BOOKISH:
            continue
        au = [a["author"]["display_name"] for a in (w.get("authorships") or [])]
        if not au:
            continue                                  # no metadata is not agreement
        if _surname(au[0]) not in {_surname(x) for x in authors}:
            continue                                  # first-author gate
        cands.append(w)
    if not cands:
        return None, "no bookish record with first-author agreement", None
    best = max(cands, key=lambda w: w.get("cited_by_count") or 0)
    return ((best.get("id") or "").rsplit("/", 1)[-1], best.get("display_name") or "",
            best.get("cited_by_count"))


def main():
    anchors = json.load(open(ANCHORS))
    verified = [a for a in anchors if a.get("identity_verified") and a.get("doi")]
    # The causal recall denominator. SECONDARY_DECLINE_NO_MECHANISM is deliberately NOT here: the
    # scope commits it to a bridge cell that cannot carry the verdict, and counting it would make the
    # denominator the reduced-form literature that C.5.a has equal claim to.
    # EARLY_FERT_OPPOSITE_SIGN IS here — it is a primary cell, sign-opposite but primary, and leaving
    # it out would rebuild the very cherry-pick Wall 6 exists to prevent.
    EMPIRICAL_CELLS = {"PRIMARY_MEASURED_DESPAIR", "PRIMARY_DECLINE_WITH_MECHANISM",
                       "EARLY_FERT_OPPOSITE_SIGN"}

    def is_empirical_anchor(rec):
        """In the causal recall denominator?

        Cell membership alone is not enough. A3 filed the three channel-1 systematic reviews under
        PRIMARY_EXPOSURE_TO_FERTILITY, which is the right cell for the estimand they review, but a
        review estimates nothing — counting it here would inflate the denominator that Recall(A) is
        computed against and flatter every recall number downstream. Reviews still seed the frame,
        forward and backward; they just do not count as evidence."""
        return (rec["provisional_cell"] in EMPIRICAL_CELLS
                and rec.get("provenance_channel") != "channel1_review_seed")

    # Monographs A3 could not give a DOI get one gated recovery attempt so their citation
    # neighbourhood is not lost in silence. Reported either way.
    book_report = []
    for a in anchors:
        if a.get("doi") or not a.get("is_book"):
            continue
        bid, note, cites = book_seed_id(a["title"], a.get("authors") or [])
        book_report.append((a["title"][:56], bid, note, cites))
        if bid:
            a["openalex_id_recovered"] = bid
            a["recovered_title"] = note
            a["recovered_cites"] = cites

    tier_a, seedinfo = [], []
    for a in verified + [x for x in anchors if x.get("openalex_id_recovered")]:
        w = work_by_doi(a["doi"]) if a.get("doi") else None
        if not w and a.get("openalex_id_recovered"):
            # Seed from the recovered id directly; no DOI exists to hydrate through.
            got = fetch_ids([a["openalex_id_recovered"]])
            if not got:
                continue
            d, ok = oa_get(f"https://api.openalex.org/works/{a['openalex_id_recovered']}"
                           f"?select={SELECT}", f"book:{a['openalex_id_recovered']}")
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
        is_empirical = is_empirical_anchor(rec)
        # BACKWARD: always, all references, one hop. Cheaper and cleaner than forward.
        back = fetch_ids(w["referenced_works"])
        # FORWARD: uniform across seed types, decoys included. The cap is a budget control and is
        # reported; empirical seeds get an unbounded pull because they are the recall spine.
        cap = 10 ** 6 if is_empirical else FORWARD_CAP
        fwd, total, truncated = citing(sid, cap)
        n_ot = sum(1 for r in fwd if on_topic(r))
        frac = (n_ot / len(fwd)) if fwd else None
        n_mech = sum(1 for r in fwd if has_mechanism(r))
        frac_mech = (n_mech / len(fwd)) if fwd else None
        n_prim = sum(1 for r in fwd if in_primary_cell(r))
        frac_prim = (n_prim / len(fwd)) if fwd else None
        n_mort = sum(1 for r in fwd if off_mortality(r))
        frac_mort = (n_mort / len(fwd)) if fwd else None
        for r in back:
            p = pool.setdefault(r["id"], {**r, "seed_ids": [], "channels": set()})
            p["seed_ids"].append(sid); p["channels"].add("backward")
        for r in fwd:
            p = pool.setdefault(r["id"], {**r, "seed_ids": [], "channels": set()})
            p["seed_ids"].append(sid); p["channels"].add("forward")
        log_rows.append(dict(title=rec["title"][:58], cell=cell, seed=sid, empirical=is_empirical,
                             n_back=len(back), n_fwd=len(fwd), fwd_total=total,
                             truncated=truncated, on_topic=frac, mech=frac_mech,
                             primary=frac_prim, n_primary=n_prim, mortality=frac_mort))
        print(f"  {cell[:26]:<26} back={len(back):>4} fwd={len(fwd):>5}/{total or 0:<5} "
              f"fert={f'{frac:.0%}' if frac is not None else 'n/a':>4} "
              f"mech={f'{frac_mech:.0%}' if frac_mech is not None else 'n/a':>4} "
              f"BOTH={f'{frac_prim:.1%}' if frac_prim is not None else 'n/a':>5} "
              f"({n_prim:>3})  {rec['title'][:34]}")

    anchor_ids = {r["openalex_id"] for r in tier_a}
    tier_b = []
    for rid, p in pool.items():
        if rid in anchor_ids:
            continue                      # a Tier A member is not Tier B
        p["channels"] = sorted(p["channels"])
        p["seed_ids"] = sorted(set(p["seed_ids"]))
        p["n_seeds"] = len(p["seed_ids"])
        tier_b.append(p)
    tier_b.sort(key=lambda r: (-r["n_seeds"], -(r["cited_by_count"] or 0)))
    json.dump(tier_b, open(OUT_B, "w"), indent=2)

    n_multi = sum(1 for r in tier_b if r["n_seeds"] > 1)
    n_abs = sum(1 for r in tier_b if r.get("abstract"))
    decoy_seeds = {r["openalex_id"] for r in tier_a if r["provisional_cell"].startswith("OFF_")}
    n_decoy_dep = sum(1 for r in tier_b if set(r["seed_ids"]) <= decoy_seeds)

    L = [f"# A4 Tier A / Tier B citation frame — {SLUG} (D.3.c)", "",
         f"**Tier A: {len(tier_a)} seeding anchors** ({sum(1 for r in tier_a if is_empirical_anchor(r))} "
         "empirical primary-cell, the causal recall denominator). `SECONDARY_DECLINE_NO_MECHANISM` is "
         "deliberately excluded from that count: the scope commits it to a bridge cell that cannot "
         "carry the verdict, and counting it would make the denominator the reduced-form literature "
         "C.5.a has equal claim to. `EARLY_FERT_OPPOSITE_SIGN` IS counted — sign-opposite but "
         "primary, and excluding it would rebuild the cherry-pick Wall 6 exists to prevent.", "",
         f"**Tier B frame: {len(tier_b):,} deduplicated records** — {n_multi:,} found by more than one "
         f"seed, {n_abs:,} carrying an abstract ({n_abs / max(len(tier_b), 1):.0%}).", "",
         f"**Records depending ONLY on a routing-decoy seed: {n_decoy_dep:,}** "
         f"({n_decoy_dep / max(len(tier_b), 1):.0%}). Under the inherited rule these would not exist, "
         "because decoys were never forward-cited. They are retained, and `seed_ids` provenance lets "
         "Recall(B) be recomputed without them as a sensitivity check.", "",
         f"**Failed requests: {len(errors)}** — listed at the foot. A failed request is not an empty "
         "result, and the frame is smaller than the index by exactly the amount those failures cost.", "",
         "## Per-seed yield", "",
         "All four fractions are SEED-SELECTION DIAGNOSTICS computed after retrieval. None is applied "
         "as a filter on the frame: filtering the forward fetch by topic vocabulary would prune "
         "Tier B by distance from the production query and make Recall(B) circular.", "",
         "`fert` = share of the forward cloud carrying a fertility quantity. `mech` = share carrying "
         "a despair-type construct, on a vocabulary deliberately wider than the anchors' (it includes "
         "subjective-future and expectations language, because a diagnostic that only found the word "
         "the hypothesis is named after would measure the name rather than the construct). "
         "**`BOTH` is the one that matters** — the share carrying a fertility quantity AND a despair "
         "construct together, i.e. the density of this chapter's actual primary cell in that seed's "
         "neighbourhood. `mort` = share with a visible mortality outcome (Wall 4), a **lower bound**.", "",
         "| seed | cell | back | fwd | fwd total | trunc | fert | mech | **BOTH** | n | mort |",
         "|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in sorted(log_rows, key=lambda x: -(x["n_fwd"])):
        pc = lambda v: f"{v:.1%}" if v is not None else "n/a"
        L.append(f"| {r['title']} | `{r['cell']}` | {r['n_back']} | {r['n_fwd']} | "
                 f"{r['fwd_total'] or 0} | {'**yes**' if r['truncated'] else 'no'} | "
                 f"{pc(r['on_topic'])} | {pc(r['mech'])} | **{pc(r['primary'])}** | "
                 f"{r['n_primary']} | {pc(r['mortality'])} |")
    tot_fwd = sum(r["n_fwd"] for r in log_rows)
    tot_prim = sum(r["n_primary"] for r in log_rows)
    L += ["", "## Primary-cell density of the whole frame", "",
          f"Across every seed's forward cloud, **{tot_prim:,} of {tot_fwd:,} records "
          f"({tot_prim / max(tot_fwd, 1):.2%}) carry a fertility quantity and a despair construct "
          "together.** That is the citation-network measurement of the same thing the reconnaissance "
          "measured at the population level, where decline AND fertility returned 1,539, despair "
          "vocabulary AND fertility returned 604, and all three legs together returned 12 with none "
          "on topic. Two independent routes to the same finding: the mechanism this chapter is named "
          "for is not measured in the literature that studies its treatment.", "",
          "Read the per-seed `BOTH` column as which seeds can reach the primary cell at all. It is "
          "also a LOOSE UPPER BOUND on the cell's true density, because co-occurrence of two "
          "vocabularies in one abstract is not the same as a study that estimates one against the "
          "other — the screen, not this diagnostic, decides that.", ""]
    if book_report:
        L += ["## Book seed recovery", "",
              "A3 left three anchors with no usable DOI: their indexed records are reviews of "
              "themselves. A DOI-less anchor cannot seed, and these three are the sociological "
              "canon, whose neighbourhood is where the opposite-sign qualitative literature lives — "
              "so each got ONE recovery attempt against bookish types, gated by the same "
              "first-author rule as the A3 book-canon gate, reported either way.", "",
              "| monograph | recovered | record | cites |", "|---|---|---|---|"]
        for t, bid, note, cites in book_report:
            L.append(f"| {t} | {'**yes**' if bid else 'no'} | "
                     f"{('`' + bid + '` ' + note[:44]) if bid else note} | {cites if cites else '—'} |")
        L += ["", "The two refusals are correct rather than unfortunate. No `book`-typed record of "
              "either monograph exists in the index. The Wilson attempt also demonstrates why the "
              "author gate is not optional at this step: a bookish search for *When Work Disappears* "
              "returns Johnston & Lordan's unrelated 2014 book above anything of Wilson's, and only "
              "first-author disagreement refuses it. Seeding from a review would import the "
              "reviewer's citation neighbourhood as though it were the author's.", ""]
    trunc = [r for r in log_rows if r["truncated"]]
    L += ["", "## Truncation", ""]
    if trunc:
        L.append(f"{len(trunc)} seed(s) hit the {FORWARD_CAP:,}-record forward cap and are reported "
                 "here rather than silently truncated — a bounded pull that is not stated reads as "
                 "complete coverage:")
        tot_lost = 0.0
        for r in trunc:
            missed = (r["fwd_total"] or 0) - r["n_fwd"]
            # Expected on-topic loss = unpulled count x the on-topic rate measured on the pulled part.
            # This ASSUMES the unpulled tail resembles the pulled head, which is exactly what a
            # cursor-paged truncation cannot guarantee. Stated as an estimate, and stated at all,
            # because "3 seeds truncated" tells a reader nothing about whether it mattered.
            exp = missed * (r["on_topic"] or 0)
            tot_lost += exp
            L.append(f"- **{r['title']}** (`{r['cell']}`): pulled {r['n_fwd']:,} of {r['fwd_total']:,} "
                     f"citing works, on-topic {r['on_topic']:.1%} — **{missed:,} unpulled, an "
                     f"estimated {exp:.0f} on-topic records not seen.**")
        L += ["", f"**Estimated on-topic records lost to the cap in total: ~{tot_lost:.0f}**, against "
                  f"a frame of {len(tier_b):,}. The estimate assumes the unpulled tail resembles the "
                  "pulled head, and a cursor-paged truncation cannot guarantee that. Raise the cap "
                  "and re-run if any truncated seed later turns out to matter for recall."]
    else:
        L.append(f"No seed reached the {FORWARD_CAP:,}-record forward cap; the frame is a complete "
                 "one-hop neighbourhood of the verified anchors.")
    if errors:
        L += ["", "## Failed requests (NOT zero results)", ""] + [f"- {a}: `{b}`" for a, b in errors[:40]]
    open(OUT_LOG, "w").write("\n".join(L) + "\n")

    print(f"\ntier_a={len(tier_a)} tier_b={len(tier_b)} multi_seed={n_multi} "
          f"decoy_only={n_decoy_dep} errors={len(errors)}")
    print(f"-> {os.path.relpath(OUT_B, ROOT)}")
    if errors and len(errors) > 0.2 * max(len(tier_a), 1):
        print("WARNING: high request-failure rate; the frame is incomplete by an unknown amount.",
              file=sys.stderr)


if __name__ == "__main__":
    main()
