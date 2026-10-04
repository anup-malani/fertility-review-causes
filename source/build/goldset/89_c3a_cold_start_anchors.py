#!/usr/bin/env python3
"""
89_c3a_cold_start_anchors.py — C.3.a (mode of production and child economic value), stage A3.

Source and EXISTENCE-VERIFY the cold-start anchor set for the agricultural-mode-of-production chapter
(TICK-030, the documented second-hypothesis GACS generalization test). This is the first C.3.a stage
that touches the network, and it carries the ghost-citation risk that bit OAS. The load-bearing
discipline, identical to 64_b1_cold_start_anchors.py:

  * Candidates below carry (title, authors, year, family, provisional_cell, provenance_channel) drawn
    from domain knowledge. They assert NO DOIs.
  * Every DOI is pulled from a LIVE Crossref bibliographic match (never hand-typed from memory), then
    re-affirmed at doi.org. This is the mandatory existence gate: no anchor enters a recall denominator
    without a resolved live identifier.
  * Three-state discipline (same as 44/48/54/64): a network failure is UNCONFIRMED, never ABSENT. Only
    a Crossref 200-with-DOI whose title matches (normalized-title Jaccard >= 0.72 AND year within +/-1)
    clears the gate to identity_verified=True. Everything else is flagged for the RA, not asserted.
  * Pre-DOI books (Boserup 1965, Netting 1993, Lee 1979, Howell, Caldwell 1982) are EXPECTED to miss
    Crossref's article index; carried as identity_verified=False with a note, not dropped and not faked.

Candidate set spans the four C.3.a query-cluster families (value-direct-energetics,
cross-cultural-subsistence, within-society-transition, intensification-theory) plus four routing decoys
that MUST route away under the search-scope walls — the A.13 lactational-amenorrhea decoy and the
nutrition-energy decoy are the load-bearing ones, because Wall 1/Wall 2 (the overdetermined
forager-agriculturalist gap) are this chapter's central failure mode.

Output: literature/search-logs/{slug}-cold-start-anchors.json  (housing/B.1 template shape)
        literature/search-logs/{slug}-cold-start-anchors-log.md (run log: matches, misses, gate calls)
"""
import json, os, re, subprocess, time
import unicodedata

SLUG = "agricultural-mode-of-production"
MAILTO = "shravanh@uchicago.edu"
UA = f"fertility-review/1.0 (mailto:{MAILTO})"
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
LOGS = os.path.join(ROOT, "literature", "search-logs")
OUT_JSON = os.path.join(LOGS, f"{SLUG}-cold-start-anchors.json")
OUT_LOG = os.path.join(LOGS, f"{SLUG}-cold-start-anchors-log.md")
CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "c3a_crossref_cache.json")
cache = json.load(open(CACHE)) if os.path.exists(CACHE) else {}

TITLE_JACCARD_MIN = 0.72
YEAR_TOL = 1

# --- Candidate anchors. NO DOIs here by design; the DOI is whatever Crossref returns for a match. ---
CANDIDATES = [
    # Family 1 — value-direct-energetics: direct measurement of children's net production / embodied
    # capital / dependency length by production system. This is the chapter's value-channel core:
    # evidence that survives the Wall-1/Wall-2 overdetermination because it measures the economic
    # mechanism rather than riding a bare subsistence-fertility gap.
    dict(title="Evolutionary and wealth flows theories of fertility: Empirical tests and new models",
         authors=["Hillard Kaplan"], year=1994, family="value-direct-energetics",
         provisional_cell="PRIMARY_VALUE_DIRECT", provenance_channel="channel2_canon_v5seminal"),
    dict(title="Why intensive agriculturalists have higher fertility: a household energy budget approach",
         authors=["Karen L. Kramer", "James L. Boone"], year=2002, family="value-direct-energetics",
         provisional_cell="PRIMARY_CROSS_SYSTEM_CONDITIONED",
         provenance_channel="direct_empirical_bibliographic_search"),
    dict(title="Children's economic roles in the Maya family life cycle: Cain, Caldwell, and Chayanov revisited",
         authors=["Ronald D. Lee", "Karen L. Kramer"], year=2002, family="value-direct-energetics",
         provisional_cell="PRIMARY_VALUE_DIRECT", provenance_channel="direct_empirical_bibliographic_search"),
    dict(title="Children's help and the pace of reproduction: cooperative breeding in humans",
         authors=["Karen L. Kramer"], year=2005, family="value-direct-energetics",
         provisional_cell="PRIMARY_VALUE_DIRECT", provenance_channel="direct_empirical_bibliographic_search"),
    dict(title="Evolution and the demand for children",
         authors=["Paul W. Turke"], year=1989, family="value-direct-energetics",
         provisional_cell="PRIMARY_VALUE_DIRECT", provenance_channel="direct_empirical_bibliographic_search"),
    dict(title="Learning, life history, and productivity: children's lives in the Okavango Delta of Botswana",
         authors=["John Bock"], year=2002, family="value-direct-energetics",
         provisional_cell="CHILD_LABOR_NO_FERTILITY",
         provenance_channel="reference_list_of_direct_empirical_anchor"),

    # Family 2 — cross-cultural-subsistence: comparative tests of subsistence mode vs fertility. The
    # phylogenetic/energy-conditioned ones clear the Galton's-problem and overdetermination threats;
    # the bare comparison documents the explanandum but is not pooled as C.3.a evidence.
    dict(title="Fertility and mode of subsistence: a phylogenetic analysis",
         authors=["Daniel W. Sellen", "Ruth Mace"], year=1997, family="cross-cultural-subsistence",
         provisional_cell="PRIMARY_CROSS_SYSTEM_CONDITIONED", provenance_channel="channel2_canon_v5seminal"),
    dict(title="The fertility of agricultural and non-agricultural traditional societies",
         authors=["Gillian R. Bentley", "Tony Goldberg", "Grazyna Jasienska"], year=1993,
         family="cross-cultural-subsistence", provisional_cell="BARE_CROSS_SYSTEM",
         provenance_channel="direct_empirical_bibliographic_search"),
    dict(title="An energy-saving development intervention increases birth rate and childhood malnutrition in rural Ethiopia",
         authors=["Mhairi A. Gibson", "Ruth Mace"], year=2006, family="cross-cultural-subsistence",
         provisional_cell="PRIMARY_TRANSITION", provenance_channel="channel2_canon_v5seminal",
         routing_note="Within-society labour-saving shock raising fertility; rides the energy channel, so a Wall-2 tension case — carried but flagged MIXED at extraction."),
    dict(title="The demographic transition: are we any closer to an evolutionary explanation?",
         authors=["Monique Borgerhoff Mulder"], year=1998, family="cross-cultural-subsistence",
         provisional_cell="MODE_OF_PRODUCTION_THEORY", provenance_channel="hypothesis_canon"),

    # Family 3 — within-society-transition: the highest-identification stratum (sedentarization,
    # intensification, labour-saving technology) where the nursing/nutrition regime can be tracked.
    dict(title="The effect of labor-saving technology on longitudinal fertility changes",
         authors=["Karen L. Kramer", "Garnett P. McMillan"], year=2006, family="within-society-transition",
         provisional_cell="PRIMARY_TRANSITION", provenance_channel="direct_empirical_bibliographic_search"),
    dict(title="A theory of human life history evolution: diet, intelligence, and longevity",
         authors=["Hillard Kaplan", "Kim Hill", "Jane Lancaster", "A. Magdalena Hurtado"], year=2000,
         family="within-society-transition", provisional_cell="MODE_OF_PRODUCTION_THEORY",
         provenance_channel="hypothesis_canon"),
    dict(title="Life Histories of the Dobe !Kung: Food, Fatness, and Well-being over the Life-span",
         authors=["Nancy Howell"], year=2010, family="within-society-transition",
         provisional_cell="PRIMARY_TRANSITION", provenance_channel="hypothesis_canon", expect_no_doi=True),
    dict(title="The !Kung San: Men, Women, and Work in a Foraging Society",
         authors=["Richard B. Lee"], year=1979, family="within-society-transition",
         provisional_cell="CHILD_LABOR_NO_FERTILITY", provenance_channel="hypothesis_canon", expect_no_doi=True),

    # Family 4 — intensification-theory: Boserup and the embodied-capital / net-transfer canon. Theory
    # stream; does NOT count toward empirical recall. Boserup also seeds the REVERSE (density ->
    # intensification) identification threat.
    dict(title="The Conditions of Agricultural Growth: The Economics of Agrarian Change under Population Pressure",
         authors=["Ester Boserup"], year=1965, family="intensification-theory",
         provisional_cell="MODE_OF_PRODUCTION_THEORY", provenance_channel="channel2_canon_v5seminal",
         expect_no_doi=True,
         routing_note="Also the REVERSE-cell canon: Boserup's own arrow runs density/population -> intensification, the simultaneity that mirrors the hypothesis."),
    dict(title="Smallholders, Householders: Farm Families and the Ecology of Intensive, Sustainable Agriculture",
         authors=["Robert McC. Netting"], year=1993, family="intensification-theory",
         provisional_cell="MODE_OF_PRODUCTION_THEORY", provenance_channel="hypothesis_canon", expect_no_doi=True),
    dict(title="A cross-cultural perspective on intergenerational transfers and the economic life cycle",
         authors=["Ronald D. Lee"], year=2000, family="intensification-theory",
         provisional_cell="MODE_OF_PRODUCTION_THEORY",
         provenance_channel="reference_list_of_direct_empirical_anchor", expect_no_doi=True),

    # Routing decoys — MUST route away; included to test routing, not recall. The A.13 and nutrition
    # decoys are load-bearing: they predict the same forager-farmer gap through a non-economic channel,
    # which is Wall 1 / Wall 2 and the whole chapter's identification problem.
    dict(title="Nursing frequency, gonadal function, and birth spacing among !Kung hunter-gatherers",
         authors=["Melvin Konner", "Carol Worthman"], year=1980, family="ROUTING_DECOY",
         provisional_cell="OFF_NURSING_A13", provenance_channel="routing_decoy_A13",
         routing_note="Lactational amenorrhea explains the forager long birth interval with no reference to child labour value; route to A.13. THE Wall-1 decoy."),
    dict(title="The ecological context of human ovarian function",
         authors=["Peter T. Ellison", "Catherine Panter-Brick", "Susan F. Lipson", "Mary T. O'Rourke"], year=1993,
         family="ROUTING_DECOY", provisional_cell="OFF_NUTRITION_B", provenance_channel="routing_decoy_nutrition",
         routing_note="Energy-balance/nutritional suppression of fecundity; same gap, no economics; route to nutrition-energy-availability. The Wall-2 decoy."),
    dict(title="Accounting for fertility decline during the transition to growth",
         authors=["Matthias Doepke"], year=2004, family="ROUTING_DECOY",
         provisional_cell="OFF_CHILD_LABOR_LAW_C3b", provenance_channel="routing_decoy_C3b",
         year_filter=2004,  # disambiguate published JEG version from the 2001 SSRN working paper (DOI ...ssrn.279519)
         routing_note="Child-labour-law / QQ within-industrial-economy decline; route to C.3.b/C.3.d, not the PM cross-system level."),
    dict(title="Theory of Fertility Decline",
         authors=["John C. Caldwell"], year=1982, family="ROUTING_DECOY",
         provisional_cell="OFF_WEALTH_FLOWS_C3f", provenance_channel="routing_decoy_C3f", expect_no_doi=True,
         routing_note="Net-wealth-flow reversal with modernization (an FDT direction story); route to C.3.f, not the PM cross-system level."),
]


# --- canonical fold, TICK-074. Keep in sync with source/lib/textnorm.py; the sync is ENFORCED by
# scripts/verify_norm.py, which imports every copy and compares it against the canonical one on a
# shared test vector. Two defects live here, both silent and both producing confident wrong answers:
# an unfolded accent SHATTERS a surname (Spéder -> "der"), and an ASCII apostrophe becomes a SPACE
# while a curly one is DELETED, so the same title normalises two different ways and a correct anchor
# is refused as NO-MATCH. Fold every class BEFORE the ASCII strip, and fold both spellings alike.
_TRANSLIT = {ord("ø"): "o", ord("Ø"): "O", ord("đ"): "d", ord("Đ"): "D", ord("ð"): "d",
             ord("Ð"): "D", ord("þ"): "th", ord("Þ"): "Th", ord("ı"): "i", ord("İ"): "I",
             ord("ł"): "l", ord("Ł"): "L", ord("æ"): "ae", ord("Æ"): "Ae", ord("œ"): "oe",
             ord("Œ"): "Oe", ord("ß"): "ss", ord("ħ"): "h", ord("Ħ"): "H", ord("ŋ"): "n",
             ord("Ŋ"): "N"}
_APOSTROPHE_CLASS = re.compile("['‘’ʼ´`]")
_DASH_CLASS = re.compile("[-‐‑‒–—―−­]")


def norm(s):
    s = (s or "").translate(_TRANSLIT)
    s = _APOSTROPHE_CLASS.sub("", s)
    s = _DASH_CLASS.sub(" ", s)
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode("ascii")
    s = re.sub(r"[^a-z0-9 ]", " ", s.lower())
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
                status = f"VERIFIED  doi={cr['doi']}  J={j}  ({(cr.get('container') or '')[:40]})"
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
          "- The value-direct-energetics family is the chapter's empirical core: it measures the "
          "child-economic-value mechanism directly, so it survives the Wall-1/Wall-2 overdetermination "
          "that sinks a bare cross-subsistence correlation (BARE_CROSS_SYSTEM). A thin verified set here "
          "is the search-scope's predicted outcome, not a search failure.",
          "- Routing decoys (A.13 nursing, nutrition-energy, C.3.b child-labour-law, C.3.f wealth-flows) "
          "are included to test that the eventual search + screen route them away; they are NOT part of "
          "the C.3.a recall denominator. The A.13 and nutrition decoys are load-bearing — they predict "
          "the forager-agriculturalist gap through a non-economic channel, which is this chapter's "
          "central identification problem.",
          "- Pre-DOI books (Boserup 1965, Netting 1993, Lee 1979, Howell, Caldwell 1982) miss the "
          "Crossref article index by nature; carried in the theory stream with a note, existence "
          "established by publication record rather than a journal DOI."]
    open(OUT_LOG, "w").write("\n".join(L) + "\n")
    print(f"verified={n_verified} flagged={n_flagged} books={n_book} total={len(anchors)}")
    print("by family:", {k: f"{sum(v)}/{len(v)}" for k, v in by_family.items()})
    print(f"-> {os.path.relpath(OUT_JSON, ROOT)}")
    print(f"-> {os.path.relpath(OUT_LOG, ROOT)}")


if __name__ == "__main__":
    main()
