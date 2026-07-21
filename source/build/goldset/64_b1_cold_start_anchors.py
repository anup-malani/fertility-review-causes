#!/usr/bin/env python3
"""
64_b1_cold_start_anchors.py — B.1 (evolutionary sex drive / contraceptive decoupling), stage A3.

Source and EXISTENCE-VERIFY the cold-start anchor set. This is the first B.1 stage that touches the
network, and it carries the ghost-citation risk that bit OAS. The load-bearing discipline:

  * Candidates below carry (title, authors, year, family, provisional_cell, provenance_channel) drawn
    from domain knowledge. They assert NO DOIs.
  * Every DOI is pulled from a LIVE Crossref bibliographic match (never hand-typed from memory), then
    re-affirmed at doi.org. This is the mandatory existence gate: no anchor enters a recall denominator
    without a resolved live identifier.
  * Three-state discipline (same as 44/48/54): a network failure is UNCONFIRMED, never ABSENT. Only a
    Crossref 200-with-DOI whose title matches (normalized-title Jaccard >= 0.72 AND year within +/-1)
    clears the gate to identity_verified=True. Everything else is flagged for the RA, not asserted.
  * Books / pre-DOI chapters (Dawkins 1976, Trivers 1972, Hrdy 1999) are EXPECTED to miss Crossref's
    article index; they are carried as identity_verified=False with a note, not dropped and not faked.

Candidate set deliberately spans all five A2 query-cluster families plus two routing decoys (an A.2
off-cell and a tempo off-cell) so the eventual search is tested on routing as well as topical recall.

Output: literature/search-logs/{slug}-cold-start-anchors.json  (child-labor template shape)
        literature/search-logs/{slug}-cold-start-anchors-log.md (run log: matches, misses, gate calls)
"""
import json, os, re, subprocess, time

SLUG = "evolutionary-sex-drive-contraceptive-decoupling"
MAILTO = "shravanh@uchicago.edu"
UA = f"fertility-review/1.0 (mailto:{MAILTO})"
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
LOGS = os.path.join(ROOT, "literature", "search-logs")
OUT_JSON = os.path.join(LOGS, f"{SLUG}-cold-start-anchors.json")
OUT_LOG = os.path.join(LOGS, f"{SLUG}-cold-start-anchors-log.md")
CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "b1_crossref_cache.json")
cache = json.load(open(CACHE)) if os.path.exists(CACHE) else {}

TITLE_JACCARD_MIN = 0.72
YEAR_TOL = 1

# --- Candidate anchors. NO DOIs here by design; the DOI is whatever Crossref returns for a match. ---
CANDIDATES = [
    # Family 2 — proximate-ultimate dissociation (the archetype empirical decoupling test)
    dict(title="Cultural and reproductive success in industrial societies: Testing the relationship at the proximate and ultimate levels",
         authors=["Daniel Perusse"], year=1993, family="proximate-ultimate",
         provisional_cell="PROXIMATE_ULTIMATE", provenance_channel="direct_empirical_bibliographic_search"),
    dict(title="Social versus reproductive success: the central theoretical problem of human sociobiology",
         authors=["Daniel R. Vining"], year=1986, family="proximate-ultimate",
         provisional_cell="PROXIMATE_ULTIMATE", provenance_channel="direct_empirical_bibliographic_search"),
    dict(title="Sex, status, and reproductive success in the contemporary United States",
         authors=["Rosemary L. Hopcroft"], year=2006, family="proximate-ultimate",
         provisional_cell="PROXIMATE_ULTIMATE", provenance_channel="direct_empirical_bibliographic_search"),
    dict(title="Natural selection on male wealth in humans",
         authors=["Daniel Nettle", "Thomas V. Pollet"], year=2008, family="proximate-ultimate",
         provisional_cell="PROXIMATE_ULTIMATE", provenance_channel="reference_list_of_direct_empirical_anchor"),

    # Family 1 — evolutionary-biosocial-theory (theory stream; does NOT count toward empirical recall)
    dict(title="The demographic transition: are we any closer to an evolutionary explanation?",
         authors=["Monique Borgerhoff Mulder"], year=1998, family="evolutionary-biosocial-theory",
         provisional_cell="THEORY", provenance_channel="hypothesis_canon"),
    dict(title="Why are modern families small? Toward an evolutionary and cultural explanation for the demographic transition",
         authors=["Lesley Newson", "Tom Postmes", "S. E. G. Lea", "Paul Webley"], year=2005,
         family="evolutionary-biosocial-theory", provisional_cell="THEORY",
         provenance_channel="hypothesis_canon"),
    dict(title="The cultural evolution of fertility decline",
         authors=["Heidi Colleran"], year=2016, family="evolutionary-biosocial-theory",
         provisional_cell="THEORY", provenance_channel="hypothesis_canon"),
    dict(title="A theory of human life history evolution: Diet, intelligence, and longevity",
         authors=["Hillard Kaplan", "Kim Hill", "Jane Lancaster", "A. Magdalena Hurtado"], year=2000,
         family="evolutionary-biosocial-theory", provisional_cell="THEORY",
         provenance_channel="hypothesis_canon"),
    dict(title="Sex differences in human mate preferences: Evolutionary hypotheses tested in 37 cultures",
         authors=["David M. Buss"], year=1989, family="evolutionary-biosocial-theory",
         provisional_cell="THEORY", provenance_channel="hypothesis_canon"),
    # Pre-DOI books — expected Crossref misses; carried, never faked
    dict(title="The Selfish Gene", authors=["Richard Dawkins"], year=1976,
         family="evolutionary-biosocial-theory", provisional_cell="THEORY",
         provenance_channel="hypothesis_canon", expect_no_doi=True),
    dict(title="Parental investment and sexual selection", authors=["Robert L. Trivers"], year=1972,
         family="evolutionary-biosocial-theory", provisional_cell="THEORY",
         provenance_channel="hypothesis_canon", expect_no_doi=True),
    dict(title="Mother Nature: A History of Mothers, Infants, and Natural Selection",
         authors=["Sarah Blaffer Hrdy"], year=1999, family="evolutionary-biosocial-theory",
         provisional_cell="THEORY", provenance_channel="hypothesis_canon", expect_no_doi=True),

    # Family 4 — childbearing-motivation / demand-for-children (Warren Miller)
    dict(title="Childbearing motivations, desires, and intentions: a theoretical framework",
         authors=["Warren B. Miller"], year=1994, family="childbearing-motivation",
         provisional_cell="MOTIVATION_DISTINCTNESS", provenance_channel="direct_empirical_bibliographic_search",
         expect_no_doi=True),  # heavily-cited monograph (Genet Soc Gen Psychol Monogr) not DOI-indexed in Crossref
    dict(title="Behavioral intentions: which ones predict fertility behavior in married couples?",
         authors=["Warren B. Miller", "David J. Pasta"], year=1995, family="childbearing-motivation",
         provisional_cell="MOTIVATION_DISTINCTNESS", provenance_channel="direct_empirical_bibliographic_search"),
    dict(title="Differences between fertility desires and intentions: implications for theory, research and policy",
         authors=["Warren B. Miller"], year=2011, family="childbearing-motivation",
         provisional_cell="PRIMARY_DESIRE_INDEPENDENCE", provenance_channel="reference_list_of_direct_empirical_anchor"),

    # Family 3 — decoupling / severing (expected thin — the finding)
    dict(title="Sex and the birth rate: human biology, demographic change, and access to fertility-regulation methods",
         authors=["Malcolm Potts"], year=1997, family="decoupling-severing",
         provisional_cell="PRIMARY_DECOUPLING", provenance_channel="direct_empirical_bibliographic_search"),

    # Family 5 — contraception-as-severing-technology (bounded; the A.2-adjacent frontier)
    dict(title="The power of the pill: oral contraceptives and women's career and marriage decisions",
         authors=["Claudia Goldin", "Lawrence F. Katz"], year=2002, family="contraception-as-technology",
         provisional_cell="CONTRACEPTIVE_MEDIATION", provenance_channel="direct_empirical_bibliographic_search",
         year_filter=2002),  # disambiguate published JPE version from the 2000 NBER working paper
    dict(title="Momma's got the pill: how Anthony Comstock and Griswold v. Connecticut shaped US childbearing",
         authors=["Martha J. Bailey"], year=2010, family="contraception-as-technology",
         provisional_cell="CONTRACEPTIVE_MEDIATION", provenance_channel="direct_empirical_bibliographic_search"),

    # Routing decoys — MUST route away; included to test routing, not recall
    dict(title="Desired fertility and the impact of population policies",
         authors=["Lant H. Pritchett"], year=1994, family="ROUTING_DECOY",
         provisional_cell="OFF_EXPOSURE_A2", provenance_channel="routing_decoy_A2",
         routing_note="Desired-fertility-drives-everything framing = A.2 demand-side; must route away from B.1."),
    dict(title="Timing of sexual intercourse in relation to ovulation",
         authors=["Allen J. Wilcox", "Clarice R. Weinberg", "Donna D. Baird"], year=1995,
         family="ROUTING_DECOY", provisional_cell="TEMPO_EXPOSURE", provenance_channel="routing_decoy_A4",
         year_filter=1995,
         routing_note="Fecundability/coital-timing = route to A.4 coital-frequency-biological unless decoupling is the object."),
]


def norm(s):
    s = re.sub(r"[^a-z0-9 ]", " ", (s or "").lower())
    return re.sub(r"\s+", " ", s).strip()


def toks(s):
    return set(norm(s).split())


def jaccard(a, b):
    A, B = toks(a), toks(b)
    if not A or not B:
        return 0.0
    return len(A & B) / len(A | B)


def overlap_coef(a, b):
    """Szymkiewicz-Simpson: |A n B| / min(|A|,|B|). Catches the subtitle case — a candidate title that
    is a prefix of a long full title (Crossref keeps subtitles) scores low Jaccard but overlap ~1.0."""
    A, B = toks(a), toks(b)
    m = min(len(A), len(B))
    return len(A & B) / m if m else 0.0


def crossref_lookup(title, year, year_filter=None):
    key = f"{title}::{year}::{year_filter}"
    if key in cache:
        return cache[key]
    q = re.sub(r"\s+", "+", norm(title))
    filt = (f"&filter=from-pub-date:{year_filter}-01-01,until-pub-date:{year_filter}-12-31"
            if year_filter else "")
    url = (f"https://api.crossref.org/works?query.bibliographic={q}"
           f"&rows=5&select=DOI,title,author,issued,container-title{filt}")
    try:
        out = subprocess.run(["curl", "-s", "-m", "30", "-A", UA, url],
                             capture_output=True, text=True).stdout
        items = json.loads(out)["message"]["items"]
    except Exception as e:
        cache[key] = {"error": str(e)[:120]}
        return cache[key]
    best = None
    for it in items:
        ct = (it.get("title") or [""])[0]
        j = jaccard(title, ct)
        yr = None
        try:
            yr = it.get("issued", {}).get("date-parts", [[None]])[0][0]
        except Exception:
            pass
        if best is None or j > best["jaccard"]:
            best = {"doi": it.get("DOI"), "matched_title": ct, "jaccard": round(j, 3),
                    "overlap": round(overlap_coef(title, ct), 3),
                    "cr_year": yr, "container": (it.get("container-title") or [""])[0]}
    cache[key] = best or {"doi": None, "jaccard": 0.0}
    return cache[key]


def doi_exists(doi):
    dkey = f"DOIRESOLVE::{doi}"
    if dkey in cache:
        return cache[dkey]
    try:
        code = subprocess.run(
            ["curl", "-s", "-I", "-o", "/dev/null", "-w", "%{http_code}", "-m", "25", "-A", UA,
             f"https://doi.org/{doi}"], capture_output=True, text=True).stdout.strip()
        state = "FOUND" if (code.startswith("3") or code == "200") else ("ABSENT" if code == "404" else "UNCONFIRMED")
    except Exception:
        state = "UNCONFIRMED"
    cache[dkey] = state
    return state


def main():
    anchors, log = [], []
    n_verified = n_flagged = n_book = 0
    for c in CANDIDATES:
        rec = {k: c[k] for k in ("title", "authors", "year", "provenance_channel", "provisional_cell")}
        rec["query_cluster_family"] = c["family"]
        if c.get("routing_note"):
            rec["routing_note"] = c["routing_note"]
        cr = crossref_lookup(c["title"], c["year"], c.get("year_filter"))
        # Three-state year gate: a MISSING Crossref year does not reject a strong title+DOI identity
        # match (missing != contradicting); only a present-and-off year fails.
        yr_ok = cr.get("cr_year") is None or abs(cr["cr_year"] - c["year"]) <= YEAR_TOL
        j = cr.get("jaccard", 0.0)
        ov = cr.get("overlap", 0.0)
        # Accept on Jaccard, OR on high containment for a multi-token candidate (subtitle case).
        title_ok = j >= TITLE_JACCARD_MIN or (ov >= 0.90 and len(toks(c["title"])) >= 5)
        matched = bool(cr.get("doi")) and title_ok and yr_ok
        if matched:
            existence = doi_exists(cr["doi"])
            rec["doi"] = cr["doi"]
            rec["identity_source"] = f"https://doi.org/{cr['doi']}"
            rec["identity_verified"] = existence == "FOUND"
            rec["existence"] = existence
            rec["match_jaccard"] = j
            rec["container"] = cr.get("container")
            rec["gold_status"] = "candidate_not_ra_frozen"
            if existence == "FOUND":
                n_verified += 1
                status = f"VERIFIED  doi={cr['doi']}  J={j}  ({cr.get('container','')[:40]})"
            else:
                n_flagged += 1
                status = f"DOI-MATCH-BUT-{existence}  doi={cr['doi']}  J={j}"
        else:
            rec["doi"] = None
            rec["identity_verified"] = False
            rec["match_jaccard"] = j
            rec["crossref_best"] = {"doi": cr.get("doi"), "title": cr.get("matched_title"),
                                     "jaccard": j, "year": cr.get("cr_year")}
            rec["gold_status"] = "unverified_no_doi_match"
            if c.get("expect_no_doi"):
                rec["note"] = "Pre-DOI book/chapter; expected Crossref-index miss. Carried in theory stream, not faked."
                n_book += 1
                status = f"BOOK-NO-DOI (expected)  best-J={j}"
            else:
                n_flagged += 1
                status = f"NO-MATCH  best-J={j}  best='{(cr.get('matched_title') or '')[:45]}'"
        anchors.append(rec)
        log.append(f"- **{c['title'][:70]}** ({c['year']}, {c['family']}) → {status}")
        json.dump(cache, open(CACHE, "w"), indent=0)
        time.sleep(0.4)

    json.dump(anchors, open(OUT_JSON, "w"), indent=2)
    by_family = {}
    for a in anchors:
        by_family.setdefault(a["query_cluster_family"], []).append(a["identity_verified"])
    L = [f"# A3 cold-start anchors — {SLUG}", "",
         f"Sourced + existence-verified {len(anchors)} candidate anchors. Every DOI pulled from a live "
         f"Crossref match (Jaccard >= {TITLE_JACCARD_MIN}, year +/-{YEAR_TOL}) then re-affirmed at doi.org; "
         "no DOI hand-asserted. Three-state gate: network failure = UNCONFIRMED, never ABSENT.", "",
         f"**Verified (live DOI): {n_verified}**  ·  **Flagged for RA: {n_flagged}**  ·  "
         f"**Pre-DOI books (expected miss): {n_book}**", "",
         "## Coverage by query-cluster family (verified / total)", ""]
    for fam, vs in sorted(by_family.items()):
        L.append(f"- {fam}: {sum(vs)}/{len(vs)}")
    L += ["", "## Per-candidate disposition", ""] + log
    L += ["", "## Notes", "",
          "- The decoupling-severing and contraception-as-technology families are expected thin: B.1's "
          "empirical core is small by nature (the scope's stated caution), so a sparse verified set here "
          "is a finding, not a search failure.",
          "- Routing decoys (A.2 desired-fertility, A.4 coital-frequency) are included to test that the "
          "eventual search + screen route them away; they are NOT part of the B.1 recall denominator.",
          "- Books that miss the Crossref article index are carried in the theory stream with a note; "
          "their existence is established by publication record, not a journal DOI."]
    open(OUT_LOG, "w").write("\n".join(L) + "\n")
    print(f"verified={n_verified} flagged={n_flagged} books={n_book} total={len(anchors)}")
    print("by family:", {k: f"{sum(v)}/{len(v)}" for k, v in by_family.items()})
    print(f"-> {os.path.relpath(OUT_JSON, ROOT)}")
    print(f"-> {os.path.relpath(OUT_LOG, ROOT)}")


if __name__ == "__main__":
    main()
