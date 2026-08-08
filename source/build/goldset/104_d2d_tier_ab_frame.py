#!/usr/bin/env python3
"""
104_d2d_tier_ab_frame.py — D.2.d (child-centered intensive parenting norms), stage A4.

Build the two-tier gold FRAME from the A3 cold-start anchors (GACS channels 1 + 3). Mirror of
`96_d1b_tier_ab_frame.py` / `73_d3b_tier_ab_frame.py`; SLUG, cache namespace, cell taxonomy and the
forward-seed parameters change, plus one new failure-mode guard described below.

  Tier A  = the direct-empirical seeds (the anchors themselves), resolved in OpenAlex and enriched with
            abstracts. Primary empirical recall set. Theory-canon anchors, the FDT context stream, and
            routing decoys are split out and NOT counted as Tier-A empirical.
  Tier B  = the orthogonal citation frame: backward references (all resolved anchors) + forward
            citations (forward-eligible anchors only), DOI-first/title-second deduplicated. Candidate
            frame the later screen turns into a scored Tier-B gold; NOT yet screened.

Neither tier is frozen here. This is a candidate frame.

NEW GUARD — HARD STOP ON BUDGET EXHAUSTION. OpenAlex answers an out-of-budget request with HTTP 200
  and a JSON body: {"error": "Rate limit exceeded", "message": "Insufficient budget ... Resets at
  midnight UTC"}. The inherited `get_json` correctly refuses to cache or return that payload, and
  `main()` records the anchor as deferred — which is right for a transient network fault and WRONG
  for this one. A budget error persists for hours (retryAfter ~26,000s observed 2026-08-08), so every
  anchor defers in turn and the run completes "successfully" with a near-empty Tier B and a long
  deferred list. A thin frame that looks like a result is exactly the failure the forward-seed
  transparency logging exists to prevent, so this stage now ABORTS on the first budget error and
  writes nothing.

  This was not hypothetical. During A4 preparation a keyless probe of three monograph titles returned
  budget errors that a caller rendered as "no results", and the three books were nearly recorded as
  ABSENT FROM OPENALEX when in truth the query never ran — the UNCONFIRMED-vs-ABSENT confusion the
  project's three-state discipline exists to prevent, reappearing one layer up in the caller.

  Run with a funded OPENALEX_API_KEY. `mailto` alone draws on a shared anonymous daily budget that a
  citation-frame build exhausts almost immediately.

BOOK ANCHORS CONTRIBUTE NOTHING TO THE FRAME, AND THAT IS A REPORTED LOSS. Hays 1996, Zelizer 1985 and
  Aries 1962 carry no DOI (A3: reachable only as reviews of themselves). The book-shape rule below
  refuses to resolve them by title, because for a monograph the top title match is its own review, and
  a review's reference list and citation cloud are not the book's. They are logged under
  `book_no_openalex_record`. The consequence — three of the four central theory anchors seed no part of
  Tier B — belongs in the log, not in a footnote.

FORWARD-SEED POLICY. Empirical seeds are always forward-cited. Every other anchor — theory, context,
  and routing decoy alike — is forward-cited unless cited_by_count > FWD_CLOUD_CAP. Both halves of
  that rule differ from D.1.b, and both changes are measured rather than assumed:

  The cap is 12 pages / 1,000 citations. It was set by loosening D.1.b's 10/600 on the argument that
  Lareau and Doepke-Zilibotti are cited BY the intensive-parenting literature, so their forward clouds
  would be on-topic and the main route to a corpus the estimand query cannot reach.

  THAT ARGUMENT WAS WRONG AND THE FIRST RUN MEASURED IT. Share of each seed's citing works that
  mention fertility / family size / childbearing / number of children:

      Lareau, Unequal Childhoods            2,169 citing     23 on-topic    1.1%
      Doepke-Zilibotti, Parenting With Style   345 citing     12 on-topic    3.5%
      Ishizuka, Parenting Standards            288 citing     18 on-topic    6.2%
      Ramey & Ramey, The Rug Rat Race          187 citing     26 on-topic   13.9%

  The theory canon's forward clouds are overwhelmingly OFF_OUTCOME — parenting to child development
  and parental wellbeing — exactly as the scope doc predicted and contrary to the reasoning above. The
  cap made the right call on Lareau for the wrong stated reason: it excluded 2,146 off-topic records
  to lose 23 on-topic ones. D.1.b's tighter setting would have been defensible and this loosening was
  an unmeasured hunch. Retained at 1,000 because it is now measured rather than guessed, and because
  raising it is what a thin primary cell should trigger.

  The real lesson is that citation COUNT is the wrong criterion; on-topic FRACTION is the right one.
  Note what cannot follow from that: filtering the forward fetch by fertility vocabulary would prune
  Tier B by distance from the future production query and bias Recall(B), which the leakage wall
  forbids. The fraction is a diagnostic for choosing seeds, never a filter on the frame.

  Excluded seeds are logged with their counts — a silent cap reads as "we covered everything" when it
  did not.

DECOY FORWARD-SEEDING — the inherited blanket exclusion is dropped here, on measurement. D.3.b and
  D.1.b never forward-cite a routing decoy, so that a decoy cannot import its neighbour's literature.
  On this hypothesis that rule removed the best discovery channel available. Share of each decoy's
  citing works mentioning fertility / family size / childbearing / number of children:

      Hazan & Zoabi   (Wall 2, C.2.f)      178 citing   157 on-topic   88.2%
      Miettinen et al (Wall 6, D.2.a)       36 citing    31 on-topic   86.1%
      Ishchanova      (Wall 5, C.2.a)        3 citing     2 on-topic   66.7%
      Becker & Lewis  (Wall 1, C.3.d)      505 citing   256 on-topic   50.7%
      Butz & Ward     (Wall 4, C.2.e)       13 citing     6 on-topic   46.2%
      Lawson & Mace   (REVERSE)            197 citing    58 on-topic   29.4%
      OECD            (Wall 3, C.2.b)        2 citing     0 on-topic    0.0%

  Six of seven are far denser in on-topic material than the theory canon (1.1-13.9%). That is not an
  accident of this anchor set: a decoy is chosen to sit just across a boundary wall, so its citation
  neighbourhood is exactly where the boundary cases live — and boundary cases are what the six walls
  exist to adjudicate. Excluding them left Tier B systematically thin in the papers hardest to route.

  Tier B is a frame to be SCREENED, not a gold set, and route-away material is expected in it. The
  cost is ~934 records pre-dedup over 9 pages. `seed_ids` provenance is recorded per record, so
  Recall(B) can be computed with and without decoy-seeded material as a sensitivity check — which is
  what makes this reversible rather than a one-way inflation of the frame.

  The rule is now uniform: there is no decoy special case in either direction.

LEAKAGE WALL (carried from A3): no query vocabulary is mined here. This step only builds the frame.

Budget discipline: every OpenAlex response cached; re-run resumes from cache.

Inputs : literature/search-logs/{slug}-cold-start-anchors.json
Outputs: literature/search-logs/{slug}-anchor-resolution.json
         literature/search-logs/{slug}-tier-a.json
         literature/search-logs/{slug}-tier-b-frame.json
         literature/search-logs/{slug}-tier-ab-log.md
"""
import argparse, hashlib, json, os, re, subprocess, sys, time, unicodedata
from collections import defaultdict
from pathlib import Path
from urllib.parse import quote

SLUG = "child-centeredness-intensive-parenting"
HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
LOGS = REPO / "literature" / "search-logs"
CACHE = HERE / "cache" / "d2d_tier_ab"
MAILTO = "shravanh@uchicago.edu"
SELECT = ("id,doi,title,publication_year,cited_by_count,authorships,primary_location,"
          "abstract_inverted_index,referenced_works")
PER_PAGE = 200
SLEEP = 0.35
MAX_FORWARD_PAGES = 12          # graceful hard cap per seed (2,400 works)
FWD_CLOUD_CAP = 1000            # non-empirical anchors above this are not forward-seeded
RESOLVE_SIM_MIN = 0.50

# D.2.d carries TWO theory cells plus a context cell, where D.1.b had one. All three are
# forward-capped and none is a Tier-A empirical seed.
THEORY_CELLS = {"PARENTING_NORM_THEORY", "PARENTING_NORM_CONSTRUCT",
                "FDT_SENTIMENTALIZATION_CONTEXT"}
# The four primary norm/intensity/standard cells plus the value-added COST_INDEPENDENCE cell.
# REVERSE is in scope but is context, NOT a Tier-A empirical seed; it is still backward/forward-cited
# into the frame because its citation neighborhood is on-topic — and because the reverse-causation
# literature is where this chapter's central identification threat is actually discussed.
EMPIRICAL_CELLS = {"PRIMARY_NORM_EXPOSURE", "PRIMARY_TIME_INTENSITY",
                   "PRIMARY_PERCEIVED_STANDARD", "COST_INDEPENDENCE"}


class BudgetExhausted(RuntimeError):
    """OpenAlex refused for lack of budget, not for lack of data. Distinct from RuntimeError so it
    cannot be swallowed by the per-anchor `except RuntimeError: deferred` handlers."""


def norm_title(v):
    v = unicodedata.normalize("NFKD", v or "").encode("ascii", "ignore").decode()
    v = v.lower().replace("&", " and ")
    v = re.sub(r"\s*[:\-–—]\s+.*$", "", v)  # subtitle-insensitive
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9\s]", " ", v)).strip()


def sim(a, b):
    aa, bb = set(norm_title(a).split()), set(norm_title(b).split())
    return len(aa & bb) / len(aa | bb) if aa and bb else 0.0


def deinvert(idx):
    if not idx:
        return ""
    return " ".join(w for _, w in sorted((p, w) for w, ps in idx.items() for p in ps))


def _is_budget_error(payload):
    if not isinstance(payload, dict):
        return False
    blob = f"{payload.get('error', '')} {payload.get('message', '')}".lower()
    return "insufficient budget" in blob or "rate limit exceeded" in blob


def get_json(url, refresh=False, tries=4):
    CACHE.mkdir(parents=True, exist_ok=True)
    # Hash the key-stripped URL: otherwise the cache is invalidated by a key rotation, and the secret
    # would be an input to a filename that gets committed in a directory listing.
    cache_url = re.sub(r"&api_key=[^&]*", "", url)
    path = CACHE / f"{hashlib.sha256(cache_url.encode()).hexdigest()}.json"
    if path.exists() and not refresh:
        return json.loads(path.read_text())
    for attempt in range(tries):
        r = subprocess.run(["curl", "-L", "--silent", "--show-error", "--max-time", "45", url],
                           capture_output=True, text=True)
        if r.returncode == 0 and r.stdout.strip():
            try:
                payload = json.loads(r.stdout)
                # Budget exhaustion is not transient and not a data fact. Retrying it wastes the run
                # and, worse, ends in a deferral that reads downstream as "nothing found here".
                if _is_budget_error(payload):
                    raise BudgetExhausted(payload.get("message") or "OpenAlex budget exhausted")
                if not (isinstance(payload, dict) and payload.get("error") and "results" not in payload):
                    path.write_text(json.dumps(payload))
                    time.sleep(SLEEP)
                    return payload
            except json.JSONDecodeError:
                pass
        if attempt < tries - 1:
            time.sleep(2 ** attempt)
    raise RuntimeError("OpenAlex failed after "
                       f"{tries} attempts: {re.sub(r'&api_key=[^&]*', '&api_key=REDACTED', url)[:110]}")


def _openalex_key():
    """`mailto` identifies the caller; it does not authenticate, and draws on a shared anonymous daily
    budget a citation-frame build exhausts almost immediately. Environment first, then `.env`. Never
    inline it: it must not reach a log, a cache filename, or a commit."""
    key = os.environ.get("OPENALEX_API_KEY")
    if key:
        return key.strip()
    envf = REPO / ".env"
    if envf.exists():
        for line in envf.read_text().splitlines():
            if line.startswith("OPENALEX_API_KEY="):
                return line.split("=", 1)[1].strip()
    return None


OPENALEX_KEY = _openalex_key()


def api(path):
    url = f"https://api.openalex.org/{path}{'&' if '?' in path else '?'}mailto={quote(MAILTO)}"
    if OPENALEX_KEY:
        url += f"&api_key={quote(OPENALEX_KEY)}"
    return url


def resolve(anchor, refresh=False):
    # An exact-DOI hit is authoritative: the DOI *is* the identity, so it bypasses the title floor.
    if anchor.get("doi"):
        try:
            w = get_json(api(f"works/{quote('https://doi.org/'+anchor['doi'], safe=':/')}"), refresh)
            if isinstance(w, dict) and w.get("id"):
                return w, round(sim(anchor["title"], w.get("title")), 4), "doi"
        except RuntimeError:
            if isinstance(sys.exc_info()[1], BudgetExhausted):
                raise
    q = quote(" ".join(norm_title(anchor["title"]).split()[:14]))
    try:
        cands = get_json(api(f"works?search={q}&per-page=5&select={SELECT}"), refresh).get("results", [])
    except BudgetExhausted:
        raise
    except RuntimeError:
        return None, 0.0, "error"
    # Book-shape rule, carried from A3 (decisions/2026-08-07-version-of-record-gate.md). For a
    # monograph the top title match is reliably its own review, and this title path is still an
    # argmax. On this canon that is not an edge case: Hays 1996 has SIX review records at title
    # similarity 1.0 and no monograph. A review is typed `article`, carries zero referenced_works,
    # and is credited with the book's citations — accepting one would put a review in the gold set in
    # place of the work and report a citation count the anchor does not have.
    if anchor.get("is_book"):
        cands = [w for w in cands if (w.get("type") or "") in ("book", "monograph", "edited-book")]
        if not cands:
            return None, 0.0, "book_no_openalex_record"
    scored = [(sim(anchor["title"], w.get("title")),
               -abs((anchor.get("year") or 0) - (w.get("publication_year") or 0)), w)
              for w in cands if isinstance(w, dict) and w.get("id")]
    if not scored:
        return None, 0.0, "title"
    s, _, w = max(scored, key=lambda r: (r[0], r[1]))
    return w, s, "title"


def flatten(w):
    return {"paperId": (w.get("id") or "").rsplit("/", 1)[-1],
            "doi": (w.get("doi") or "").lower().replace("https://doi.org/", "") or None,
            "title": w.get("title") or "", "year": w.get("publication_year"),
            "cited_by_count": w.get("cited_by_count"),
            "authors": "; ".join(a.get("author", {}).get("display_name", "")
                                 for a in (w.get("authorships") or [])[:12]),
            "venue": ((w.get("primary_location") or {}).get("source") or {}).get("display_name"),
            "abstract": deinvert(w.get("abstract_inverted_index"))}


def fetch_by_ids(ids, refresh=False):
    out, ids = [], sorted(set(i.rsplit("/", 1)[-1] for i in ids if i))
    for s in range(0, len(ids), 50):
        grp = "|".join(ids[s:s + 50])
        out.extend(get_json(api(f"works?filter=openalex_id:{quote(grp, safe='|')}"
                                f"&per-page=50&select={SELECT}"), refresh).get("results", []))
    return out


def fetch_forward(anchor_id, refresh=False):
    out, cursor, pages = [], "*", 0
    while cursor and pages < MAX_FORWARD_PAGES:
        data = get_json(api(f"works?filter=cites:{anchor_id}&per-page={PER_PAGE}"
                            f"&cursor={quote(cursor, safe='')}&select={SELECT}"), refresh)
        out.extend(data.get("results", []))
        cursor = (data.get("meta") or {}).get("next_cursor")
        pages += 1
    return out, pages, bool(cursor)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--refresh", action="store_true")
    args = ap.parse_args()
    if not OPENALEX_KEY:
        print("WARNING: no OPENALEX_API_KEY (env or .env). Running on the shared anonymous budget, "
              "which a citation-frame build exhausts almost immediately. The run will abort rather "
              "than emit a thin frame.", file=sys.stderr)
    anchors = json.loads((LOGS / f"{SLUG}-cold-start-anchors.json").read_text())

    resolved, unresolved, deferred = [], [], []
    for a in anchors:
        try:
            w, s, via = resolve(a, args.refresh)
        except BudgetExhausted as e:
            sys.exit(f"ABORT (budget): {e}\nNothing written. Supply a funded OPENALEX_API_KEY and "
                     f"re-run; cached responses are reused so the run resumes.")
        except RuntimeError:
            deferred.append(a["title"]); continue
        # DOI matches are authoritative; only title-search fallbacks face the similarity floor.
        if w is None or (via != "doi" and s < RESOLVE_SIM_MIN):
            unresolved.append({"title": a["title"], "similarity": round(s, 3),
                               "is_book": bool(a.get("is_book")), "via": via,
                               "provisional_cell": a.get("provisional_cell"),
                               "reason": ("no book-shaped OpenAlex record; the title path returns only "
                                          "reviews of the work, so it is refused. Carried keyed on "
                                          "title; contributes NOTHING to the frame"
                                          if via == "book_no_openalex_record"
                                          else "below title-similarity floor")})
            continue
        cell = a.get("provisional_cell")
        is_decoy = a.get("query_cluster_family") == "ROUTING_DECOY"
        is_theory = cell in THEORY_CELLS
        cb = w.get("cited_by_count") or 0
        # Empirical seeds are always forward-cited: they are the recall set. Everything else —
        # theory, context, AND routing decoys — is forward-cited unless its cloud exceeds the cap.
        # See DECOY FORWARD-SEEDING in the docstring for why decoys are no longer blanket-excluded.
        is_empirical = (cell in EMPIRICAL_CELLS) and not is_decoy
        fwd_eligible = is_empirical or cb <= FWD_CLOUD_CAP
        resolved.append({"anchor": a, "openalex": flatten(w), "title_similarity": round(s, 4),
                         "referenced_works": w.get("referenced_works") or [],
                         "is_decoy": is_decoy, "is_theory": is_theory,
                         "is_empirical_seed": (cell in EMPIRICAL_CELLS) and not is_decoy,
                         "forward_eligible": fwd_eligible})
    (LOGS / f"{SLUG}-anchor-resolution.json").write_text(
        json.dumps({"resolved": resolved, "unresolved": unresolved, "deferred": deferred},
                   indent=2, ensure_ascii=False))

    # Tier A = resolved empirical seeds, enriched.
    tier_a = []
    for it in resolved:
        if it["is_empirical_seed"]:
            rec = dict(it["openalex"])
            rec["provisional_cell"] = it["anchor"].get("provisional_cell")
            rec["query_cluster_family"] = it["anchor"].get("query_cluster_family")
            rec["provenance_channel"] = it["anchor"].get("provenance_channel")
            rec["title_similarity"] = it["title_similarity"]
            rec["gold_status"] = "tier_a_candidate_not_frozen"
            tier_a.append(rec)
    tier_a.sort(key=lambda r: (r["provisional_cell"], -(r.get("year") or 0)))
    (LOGS / f"{SLUG}-tier-a.json").write_text(json.dumps(tier_a, indent=2, ensure_ascii=False))

    # Tier B = backward (all) + forward (eligible) citation frame.
    discovered = defaultdict(lambda: {"channels": set(), "seeds": set(), "work": None})
    fwd_pages = 0
    fwd_included, fwd_excluded, capped = [], [], []
    for it in resolved:
        seed = it["openalex"]["paperId"]
        try:
            for w in fetch_by_ids(it["referenced_works"], args.refresh):
                wid = (w.get("id") or "").rsplit("/", 1)[-1]
                if wid and wid != seed:
                    discovered[wid]["channels"].add("backward_reference")
                    discovered[wid]["seeds"].add(seed); discovered[wid]["work"] = w
        except BudgetExhausted as e:
            sys.exit(f"ABORT (budget) during backward refs: {e}\nNothing further written; re-run "
                     f"with a funded key to resume from cache.")
        except RuntimeError:
            deferred.append(f"backward:{it['openalex']['title'][:40]}")
        if it["forward_eligible"]:
            try:
                fwd, pages, cap = fetch_forward(seed, args.refresh)
                fwd_pages += pages
                if cap:
                    capped.append(seed)
                fwd_included.append((it["openalex"]["title"], it["openalex"].get("cited_by_count")))
                for w in fwd:
                    wid = (w.get("id") or "").rsplit("/", 1)[-1]
                    if wid and wid != seed:
                        discovered[wid]["channels"].add("forward_citation")
                        discovered[wid]["seeds"].add(seed); discovered[wid]["work"] = w
            except BudgetExhausted as e:
                sys.exit(f"ABORT (budget) during forward cites: {e}\nNothing further written; re-run "
                         f"with a funded key to resume from cache.")
            except RuntimeError:
                deferred.append(f"forward:{it['openalex']['title'][:40]}")
        else:
            fwd_excluded.append((it["openalex"]["title"], it["openalex"].get("cited_by_count"),
                                 f"cloud {it['openalex'].get('cited_by_count')} > cap {FWD_CLOUD_CAP}"))

    anchor_ids = {it["openalex"]["paperId"] for it in resolved}
    by_doi, by_title, frame, dups = {}, {}, [], 0
    for wid, it in discovered.items():
        if wid in anchor_ids:
            continue
        rec = flatten(it["work"])
        doi, tkey = rec["doi"], norm_title(rec["title"])
        existing = by_doi.get(doi) if doi else by_title.get(tkey)
        if existing is not None:
            dups += 1
            existing["discovery_channels"] = sorted(set(existing["discovery_channels"]) | it["channels"])
            existing["seed_ids"] = sorted(set(existing["seed_ids"]) | it["seeds"])
            continue
        rec["discovery_channels"] = sorted(it["channels"])
        rec["seed_ids"] = sorted(it["seeds"])
        rec["gold_status"] = "tier_b_candidate_unscreened"
        frame.append(rec)
        if doi:
            by_doi[doi] = rec
        if tkey:
            by_title[tkey] = rec
    frame.sort(key=lambda r: (-len(r["discovery_channels"]), -(r.get("year") or 0), r["title"]))
    (LOGS / f"{SLUG}-tier-b-frame.json").write_text(json.dumps(frame, indent=2, ensure_ascii=False))

    both = sum(len(r["discovery_channels"]) > 1 for r in frame)
    absn = sum(len(r.get("abstract") or "") >= 30 for r in frame)
    L = [f"# A4 Tier-A / Tier-B frame — {SLUG} (D.2.d)", "",
         "Candidate frame, **not** screened or frozen. Two-tier GACS: Tier A = direct-empirical seeds; "
         "Tier B = orthogonal backward+forward citation frame.", "",
         f"OpenAlex auth: {'api_key present' if OPENALEX_KEY else 'MAILTO ONLY (anonymous budget)'}.", "",
         "## Tier A (empirical seeds, enriched)", "",
         f"- resolved empirical seeds: **{len(tier_a)}**",
         "", "| cell | n |", "|---|---|"]
    cells = defaultdict(int)
    for r in tier_a:
        cells[r["provisional_cell"]] += 1
    for c, n in sorted(cells.items()):
        L.append(f"| {c} | {n} |")
    L += ["", "## Anchor resolution", "",
          f"- input anchors: {len(anchors)}",
          f"- OpenAlex-resolved: {len(resolved)}",
          f"- unresolved (below sim {RESOLVE_SIM_MIN}, or book with no book-shaped record): {len(unresolved)}",
          f"- deferred (network, resume on re-run): {len(deferred)}",
          "", "## Tier B (citation frame)", "",
          f"- deduplicated candidates: **{len(frame):,}**",
          f"- found by both channels: {both:,}",
          f"- with usable abstracts: {absn:,}",
          f"- duplicates merged: {dups:,}",
          f"- forward pages requested/cached: {fwd_pages}",
          f"- seeds hitting the {MAX_FORWARD_PAGES}-page cap: {len(capped)}",
          "", "### Forward-seed policy (transparency)", "",
          f"Forward-cited anchors ({len(fwd_included)}):"]
    for t, cb in sorted(fwd_included, key=lambda x: -(x[1] or 0)):
        L.append(f"- OK {t[:60]} (cb={cb})")
    L += ["", f"Forward-EXCLUDED anchors ({len(fwd_excluded)}) — backward refs still used:"]
    for t, cb, why in sorted(fwd_excluded, key=lambda x: -(x[1] or 0)):
        L.append(f"- XX {t[:55]} (cb={cb}, {why})")
    if unresolved:
        L += ["", "## Unresolved anchors", "",
              "Book anchors below are refused deliberately: the title path returns only reviews of the "
              "work, and a review's reference list and citation cloud are not the book's. The loss is "
              "real and is recorded here rather than absorbed silently.", ""] + \
             [f"- {x['title'][:58]} (sim {x['similarity']}, {x['via']}"
              f"{', book' if x['is_book'] else ''}) — {x['provisional_cell']}" for x in unresolved]
    if deferred:
        L += ["", "## Deferred (resume on re-run)", ""] + [f"- {d}" for d in deferred]
    L += ["", "## Next gate", "",
          "Screen the whole Tier-B frame with the D.2.d rubric, routing on the six boundary walls "
          "(vs C.3.d quantity-quality, C.2.f inequality/status, C.2.b direct costs, C.2.e female wage, "
          "C.2.a childcare, D.2.a gender equity). Four of the six are NOT enforceable at "
          "title/abstract — see the enforceability table in the scope doc — so the screen assigns a "
          "provisional cell and records `ROUTING_DEFERRED_TO_FULLTEXT` rather than guessing an "
          "`OFF_*` label. Do NOT prune the frame by vocabulary distance from the future production "
          "query; that would bias Recall(B). The seven routing decoys (Becker-Lewis C.3.d, "
          "Hazan-Zoabi C.2.f, OECD C.2.b, Butz-Ward C.2.e, Ishchanova C.2.a, Miettinen D.2.a, and the "
          "Lawson-Mace REVERSE decoy) must surface as route-away at screen."]
    (LOGS / f"{SLUG}-tier-ab-log.md").write_text("\n".join(L) + "\n")
    print(f"resolved {len(resolved)}/{len(anchors)} | Tier A {len(tier_a)} | Tier B frame {len(frame)} "
          f"(both {both}, abstracts {absn}, dups {dups}) | fwd pages {fwd_pages} | "
          f"deferred {len(deferred)}", file=sys.stderr)
    if deferred:
        print(f"WARNING: {len(deferred)} deferred (network); re-run to resume", file=sys.stderr)


if __name__ == "__main__":
    main()
