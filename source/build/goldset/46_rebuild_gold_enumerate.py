#!/usr/bin/env python3
"""
46_rebuild_gold_enumerate.py — rebuild the gold on existence-verified anchors (channel 2).

The de-ghosted PRIMARY cell (17) is below the §7.2 floor (30). Rebuild the primary-cell
anchor core by top-down canon enumeration WITH the mandatory existence gate that was
missing the first time: every enumerated candidate must resolve to a live OpenAlex/Crossref
record (Jaccard>=0.72 on title + author-surname + year gate) before it is admitted. A
candidate that does not resolve is REJECTED, not kept — this is the exact rule whose absence
let ghosts into the gold.

Enumeration is deliberately specified as (author, year, title) so the verifier can confirm a
real record and so the gate — not the model's memory — is the arbiter of existence. If the
model hallucinated a candidate here, the gate rejects it, by design.

Seeds carried over as already-real: the surviving DOI-bearing Tier-B PRIMARY/OFF anchors and
the Tier-A empirical core (both DOI-verified). This step ADDS verified canon anchors on top.

Outputs:
  {slug}-gold-rebuild-verified.json   newly verified anchors (real DOI, matched title)
  {slug}-gold-rebuild-rejected.json   enumerated candidates that failed the existence gate
  {slug}-gold-rebuild-log.md          counts, and the running real-PRIMARY total vs the floor
"""
import json, sys
from pathlib import Path
import importlib.util

SLUG = "old-age-security-pension-crowdout"
HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
LOGS = REPO / "literature" / "search-logs"

# Verify via Crossref (free; canon papers are DOI-registered) — OpenAlex budget is metered/dry.
spec = importlib.util.spec_from_file_location("dg8", HERE / "48_deghost_corpus_crossref.py")
dg8 = importlib.util.module_from_spec(spec); spec.loader.exec_module(dg8)

# Canon enumeration — landmark OAS/pension <-> fertility empirical + theory papers,
# each as (author, year, title, cell). The existence gate confirms or rejects; the model's
# memory is NOT trusted. cell in {PRIMARY, THEORY, OFF}.
CANDIDATES = [
    # -- empirical primary-cell (OAS/pension -> fertility) --
    ("Willis", 1980, "The old age security hypothesis and population growth", "THEORY"),
    ("Nugent", 1985, "The old-age security motive for fertility", "THEORY"),
    ("Cain", 1983, "Fertility as an adjustment to risk", "THEORY"),
    ("Cain", 1981, "Risk and insurance: perspectives on fertility and agrarian change", "PRIMARY"),
    ("Entwisle Winegarden", 1984, "Fertility and pension programs in LDCs: a model of mutual reinforcement", "PRIMARY"),
    ("Nugent Gillaspy", 1983, "Old age pensions and fertility in rural areas of less developed countries", "PRIMARY"),
    ("Rossi Godard", 2022, "The old-age security motive for fertility: evidence from the extension of social pensions in Namibia", "PRIMARY"),
    ("Billari Galasso", 2009, "What explains fertility? Evidence from Italian pension reforms", "PRIMARY"),
    ("Rendall Bahchieva", 1998, "An old-age security motive for fertility in the United States?", "PRIMARY"),
    ("Bau", 2021, "Can policy change culture? Government pension plans and traditional kinship practices", "PRIMARY"),
    ("Cigno Rosati", 1996, "Jointly determined saving and fertility behaviour: theory and estimates for Germany, Italy, UK and USA", "PRIMARY"),
    ("Cigno Casolaro Rosati", 2003, "The impact of social security on saving and fertility in Germany", "PRIMARY"),
    ("Zhang Zhang", 2004, "How does social security affect economic growth? Evidence from cross-country data", "OFF"),
    ("Boldrin De Nardi Jones", 2015, "Fertility and social security", "PRIMARY"),
    ("Ehrlich Kim", 2007, "Social security and demographic trends: theory and evidence from the international experience", "PRIMARY"),
    ("Galasso Gatti Profeta", 2009, "Investing for the old age: pensions, children and savings", "PRIMARY"),
    ("Fenge Scheubel", 2017, "Pensions and fertility: back to the roots", "PRIMARY"),
    ("Fanti Gori", 2012, "A note on endogenous fertility, child allowances and pensions", "THEORY"),
    ("van Groezen Leers Meijdam", 2003, "Social security and endogenous fertility: pensions and child allowances as siamese twins", "THEORY"),
    ("Wigger", 1999, "Pay-as-you-go financed public pensions in a model of endogenous growth and fertility", "THEORY"),
    ("Yakita", 2001, "Uncertain lifetime, fertility and social security", "THEORY"),
    ("Ehrlich Lui", 1991, "Intergenerational trade, longevity, and economic growth", "THEORY"),
    ("Boldrin Jones", 2002, "Mortality, fertility, and saving in a Malthusian economy", "THEORY"),
    ("Prinz", 1990, "Endogenous fertility, altruistic behavior across generations, and social security systems", "THEORY"),
    ("Sinn", 2004, "The pay-as-you-go pension system as fertility insurance and an enforcement device", "THEORY"),
    ("Fenge Meier", 2005, "Pensions and fertility incentives", "THEORY"),
    ("Cremer Gahvari Pestieau", 2006, "Pensions with endogenous and stochastic fertility", "THEORY"),
    ("Zhang Zhang Lee", 2001, "Mortality decline and long-run economic growth", "OFF"),
    ("Li Zhang", 2007, "Do high birth rates hamper economic growth?", "OFF"),
    ("Manuelli Seshadri", 2009, "Explaining international fertility differences", "OFF"),
    ("Raut Srinivasan", 1994, "Dynamic models of fertility, savings and investment in human capital", "THEORY"),
    ("Caldwell", 1978, "A theory of fertility: from high plateau to destabilization", "THEORY"),
    ("Jensen", 2004, "Do private transfers displace the benefits of public transfers? Evidence from South Africa", "OFF"),
    ("Edmonds", 2006, "Child labor and schooling responses to anticipated income in South Africa", "OFF"),
    ("Rosati", 1996, "Social security in a non-altruistic model with uncertainty and endogenous fertility", "THEORY"),
]

def main():
    verified, rejected, unverified = [], [], []
    for i, (auth, yr, title, cell) in enumerate(CANDIDATES):
        cr_status, hit = dg8.crossref(title, auth, yr)              # Crossref existence gate (free)
        if cr_status == "FOUND" and hit.get("doi"):
            verified.append({"enum_author": auth, "enum_year": yr, "enum_title": title,
                             "cell": cell, "doi": hit["doi"], "matched_title": hit["matched_title"],
                             "resolved_year": hit.get("year"), "source": hit["source"]})
        elif cr_status == "ABSENT":
            rejected.append({"enum_author": auth, "enum_year": yr, "enum_title": title,
                             "cell": cell, "reason": "existence gate: Crossref confirms no match"})
        else:
            unverified.append({"enum_author": auth, "enum_year": yr, "enum_title": title,
                               "cell": cell, "cr": cr_status})
        if (i + 1) % 10 == 0:
            print(f"  probed {i+1}/{len(CANDIDATES)}; {len(verified)} verified, {len(rejected)} rejected, {len(unverified)} unconfirmed", file=sys.stderr)
    if unverified:
        print(f"⚠️  {len(unverified)} candidates UNCONFIRMED (Crossref outage) — NOT rejected.", file=sys.stderr)

    json.dump(verified, open(LOGS / f"{SLUG}-gold-rebuild-verified.json", "w"), indent=2, ensure_ascii=False)
    json.dump(rejected, open(LOGS / f"{SLUG}-gold-rebuild-rejected.json", "w"), indent=2, ensure_ascii=False)

    from collections import Counter
    vc = Counter(v["cell"] for v in verified)
    # dedup verified vs surviving de-ghosted anchors (by DOI) to get NET-new
    dg_B = json.load(open(LOGS / f"{SLUG}-tier-b-deghosted.json"))
    have = {(g.get("doi") or "").lower().replace("https://doi.org/","") for g in dg_B if g.get("doi")}
    net_new = [v for v in verified if v["doi"] not in have]
    net_primary = sum(1 for v in net_new if v["cell"] == "PRIMARY")
    dg_tags = {t["id"]: t for t in json.load(open(HERE / "estimand_tierb_tags_deghosted.json"))}
    surviving_primary = sum(1 for g in dg_B if dg_tags.get(g.get("paperId"), {}).get("cell") == "PRIMARY")
    running_primary = surviving_primary + net_primary

    L = [f"# Gold rebuild — existence-gated canon enumeration (channel 2) — {SLUG}", "",
         "Every candidate must resolve to a live OpenAlex/Crossref DOI before admission — the gate "
         "whose absence admitted the ghosts. A hallucinated candidate is rejected here by design.", "",
         f"- candidates enumerated: **{len(CANDIDATES)}**",
         f"- **verified** (resolved to a real DOI): **{len(verified)}**  → PRIMARY {vc['PRIMARY']}, THEORY {vc['THEORY']}, OFF {vc['OFF']}",
         f"- **rejected** by the existence gate: **{len(rejected)}**",
         f"- net-new (not already in the de-ghosted set): **{len(net_new)}** ({net_primary} PRIMARY)", "",
         "## Running PRIMARY-cell anchor count vs the §7.2 floor", "",
         f"- surviving de-ghosted PRIMARY: {surviving_primary}",
         f"- + net-new verified PRIMARY (this channel): {net_primary}",
         f"- **running real PRIMARY total: {running_primary}**  → floor is 30 → "
         + ("**FLOOR MET**" if running_primary >= 30 else f"**still {30-running_primary} short — run channels 1 (meta-analysis lists) + 3 (existence-gated snowball)**"), ""]
    if rejected:
        L += ["## Rejected candidates (failed existence gate — model-memory misses, correctly excluded)", ""]
        for r in rejected:
            L.append(f"- {r['enum_author']} ({r['enum_year']}): {r['enum_title'][:70]}")
    (LOGS / f"{SLUG}-gold-rebuild-log.md").write_text("\n".join(L) + "\n")

    print(f"\nverified {len(verified)}/{len(CANDIDATES)} (PRIMARY {vc['PRIMARY']}), rejected {len(rejected)}", file=sys.stderr)
    print(f"net-new {len(net_new)} ({net_primary} PRIMARY) -> running real PRIMARY {running_primary}/30", file=sys.stderr)

if __name__ == "__main__":
    main()
