#!/usr/bin/env python3
"""
216 — A.23 anchor existence-verification gate.

TICK-075. Takes the hand-selected anchor candidates from 214/215 and the 212 seed
harvest and puts each through the mandatory existence gate before it may enter any
recall denominator. Verification is against CROSSREF, deliberately not against
OpenAlex: OpenAlex is where the candidates came from, so re-asking it would confirm
nothing. This is the standing rule from the 2026-07-08 run that found ~40% of the
frozen OAS Tier B was fabricated snowball citations.

Each record is checked for:
  * a resolving DOI in Crossref,
  * FIRST-author agreement with what we recorded (a review can list the reviewed
    author as a co-author, so membership is not enough), and
  * a title that matches after an accent-tolerant fold (the fold must transliterate,
    not shatter: a fold that maps non-ASCII to a space turned Spéder into "der").

A record that fails to resolve is `UNRESOLVED`, never `absent`. A refusal, a
timeout or a rate-limit is `ERROR`, and is not a failure of the record.

Usage: python3 source/build/goldset/216_a23_verify_anchors.py
"""
import json
import re
import subprocess
import time
import unicodedata
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "literature" / "search-logs" / "co-residence-parents-household-delay-cold-start-anchors.json"
CROSSREF = "https://api.crossref.org/works/"

TRANSLIT = {"ø": "o", "æ": "ae", "å": "a", "ß": "ss", "đ": "d", "ł": "l", "ð": "d", "þ": "th"}


def fold(s):
    """Accent-tolerant fold that TRANSLITERATES. Never maps a letter to a space."""
    if not s:
        return ""
    s = s.lower()
    s = "".join(TRANSLIT.get(c, c) for c in s)
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]+", " ", s).strip()


def jaccard(a, b):
    A, B = set(fold(a).split()), set(fold(b).split())
    return len(A & B) / len(A | B) if A and B else 0.0


def crossref(doi, tries=3):
    url = CROSSREF + urllib.parse.quote(doi, safe="")
    for attempt in range(tries):
        r = subprocess.run(["curl", "-sS", "--max-time", "60", "-H",
                            "User-Agent: fertility-review (mailto:shravanh@uchicago.edu)", url],
                           capture_output=True, text=True)
        if r.returncode != 0:
            time.sleep(4 * (attempt + 1))
            continue
        txt = r.stdout.strip()
        if txt.startswith("Resource not found"):
            return None, "NOT_IN_CROSSREF"
        try:
            return json.loads(txt)["message"], None
        except Exception:
            time.sleep(4 * (attempt + 1))
    return None, "ERROR"


# Hand-selected from 214 (broad families), 215 (targeted pulls) and 212 (C.2.c
# seed harvest). `cell` is the provisional estimand cell from the scope's §8.
CANDIDATES = [
    # --- PRIMARY_EXTENDED_COUPLE, identified: grandparental availability shocks ---
    ("10.1016/j.jpubeco.2023.104928", "Fertility and parental retirement", "PRIMARY_EXTENDED_COUPLE", "215:pension_shock", "design 8; pension eligibility as the source of variation"),
    ("10.1093/cesifo/ifu030", "Working Women and Fertility: the Role of Grandmothers' Labor Force Participation", "PRIMARY_EXTENDED_COUPLE", "215:pension_shock", "design 8"),
    ("10.1086/719161", "Stay at Home with Grandma, Mom Is Going to Work", "PRIMARY_EXTENDED_COUPLE", "215:pension_shock", "design 8"),
    ("10.1016/j.econlet.2025.112239", "The intergenerational impact of pension reforms: How grandmothers", "PRIMARY_EXTENDED_COUPLE", "215:pension_shock", "design 8"),
    ("10.1007/s10797-023-09822-9", "Grandparental childcare, family allowances and retirement policies", "PRIMARY_EXTENDED_COUPLE", "215:pension_shock", "design 8; may be theoretical"),
    ("10.2139/ssrn.2420716", "Roadblocks on the Road to Grandma's House: Fertility Consequences", "PRIMARY_EXTENDED_COUPLE", "215:pension_shock", "design 8; preprint — version-of-record check required"),
    # --- PRIMARY_EXTENDED_COUPLE, observational core ---
    ("10.1007/s10680-012-9273-2", "Grandparenting and Childbearing in the Extended Family", "PRIMARY_EXTENDED_COUPLE", "215:grandparent_childcare", ""),
    ("10.1093/esr/jcad040", "Do grandparents really matter? The effect of regular grandparental childcare", "PRIMARY_EXTENDED_COUPLE", "215:grandparent_childcare", ""),
    ("10.4054/demres.2014.31.1", "The impact of grandparental investment on mothers' fertility intentions", "PRIMARY_EXTENDED_COUPLE", "215:grandparent_childcare", ""),
    ("10.1371/journal.pone.0286496", "Grandparental childcare and second births in China", "PRIMARY_EXTENDED_COUPLE", "215:grandparent_childcare", ""),
    ("10.1007/s00181-022-02280-y", "Fertility cost, grandparental childcare, and female employment", "PRIMARY_EXTENDED_COUPLE", "215:grandparent_childcare", ""),
    ("10.1016/j.jce.2017.10.005", "Fertility, household structure, and parental labor supply", "PRIMARY_EXTENDED_COUPLE", "215:east_asia", ""),
    ("10.1007/s13524-013-0244-y", "Coresidence With Husband's Parents, Labor Supply, and Duration to First Birth", "PRIMARY_EXTENDED_COUPLE", "215:coresidence_delay", "Demography; a direct co-residence to first-birth estimate"),
    ("10.3138/jcfs.43.3.439", "Starting a Family at Your Parents' House: Multigenerational Households and Below Replacement Fertility", "PRIMARY_EXTENDED_COUPLE", "212:harvest", "spans both configurations; routing to be settled at full text"),
    ("10.1098/rspb.2011.1424", "Grandparental investment and reproductive decisions in the longitudinal 1970 British cohort study", "PRIMARY_EXTENDED_COUPLE", "214:extended_broad", ""),
    # Reclassified on reading the RESOLVED title: the gate returned "…: impacts on
    # stress and health behaviors". The outcome is not fertility, so it is not a gold
    # candidate. Kept as a decoy — a co-residence exposure with a non-fertility outcome
    # is exactly what the routing test needs.
    ("10.1016/j.socscimed.2003.10.003", "Multigenerational family structure in Japanese society", "OFF_OUTCOME", "214:extended_broad", "co-residence exposure, non-fertility outcome (stress and health behaviours) — decoy"),
    # --- PRIMARY_PRELAUNCH ---
    ("10.1553/populationyearbook2020.deb02", "Moving out the parental home and partnership formation as social determinants of low fertility", "PRIMARY_PRELAUNCH", "215:coresidence_delay", ""),
    ("10.1300/j002v42n01_03", "The Timing of Leaving the Parental Home and Its Linkages to Other Life Events", "PRIMARY_PRELAUNCH", "215:leaving_home_first_birth", ""),
    ("10.1093/esr/jcac064", "Long goodbyes: pathways of leaving home by gender and destination", "PRIMARY_PRELAUNCH", "215:southern_europe", ""),
    ("10.1002/ijpg.231", "Leaving Home in Europe: The Experience of Cohorts Born Around 1960", "LINK1_DRIVER_TO_ARRANGEMENT", "212:harvest", "Billari, Philipov, Baizán — the closest thing to the unresolved 'Baizan 2006'"),
    ("10.1007/s10680-007-9136-4", "Heterogeneity in the Transition to Adulthood", "LINK1_ARRANGEMENT_TO_UNION", "215:leaving_home_first_birth", ""),
    # --- added 2026-08-27 after the channel-5 pass (221): the emancipation family.
    # These were invisible to the exposure vocabulary the scope froze, because the
    # Southern European literature says "emancipation" where the frame said "leaving
    # home". Adding the word moves the frame from 1,012 to 1,419.
    ("10.1515/bejeap-2014-0003", "Fostering Household Formation: Evidence from a Spanish Rental Subsidy", "MIXED_PRICE_ARRANGEMENT", "221:design2_vocabB", "THE identified pre-launch study. DiD on the eligibility-age threshold of Spain's 2008 rental subsidy; outcomes are living apart from parents, living with a partner, AND childbearing -- the whole chain on one design. Wall 1 sub-ruling: shared with C.2.c."),
    ("10.1111/roiw.12122", "Youth Poverty, Employment, and Leaving the Parental Home in Europe", "LINK1_DRIVER_TO_ARRANGEMENT", "221:emancipation", ""),
    ("10.2139/ssrn.1960897", "Leaving Home and Housing Prices: The Experience of Italian Youth Emancipation", "OFF_PRICE_C2c", "221:emancipation", "price-identified; C.2.c's, and a decoy here"),
    # --- PRIMARY_PROXIMITY ---
    ("10.1080/17441730.2010.494445", "Intergenerational proximity and the fertility intentions of married adults", "PRIMARY_PROXIMITY", "215:proximity", ""),
    # --- THEORY / channel 2 ---
    ("10.2307/2807972", "Family Ties in Western Europe: Persistent Contrasts", "THEORY", "v5:seminal", "also a Wall 3 decoy"),
    ("10.1353/foc.0.0038", "On a New Schedule: Transitions to Adulthood and Family Change", "THEORY", "214:reviews", "the nearest thing to a review this frame has"),
    ("10.4054/demres.2008.19.36", "Trends in living arrangements in Europe: Convergence or divergence?", "LINK1_DRIVER_TO_ARRANGEMENT", "v5:seminal", ""),
    # --- deliberate off-cell DECOYS, for the routing test ---
    ("10.1007/s11150-016-9355-8", "The asymmetric housing wealth effect on childbirth", "OFF_PRICE_C2c", "decoy", "price-identified; C.2.c's"),
    ("10.1093/restud/rdad034", "Monetary Policy and Birth Rates: The Effect of Mortgage Rate Pass-Through on Fertility", "OFF_PRICE_C2c", "decoy", "credit terms; C.3.e's under C.2.c Wall 1"),
    ("10.2307/353569", "Race and Ethnic Variation in Norms of Filial Responsibility among Older Persons", "ELDER_SUPPORT", "decoy", "the homonym"),
    ("10.1016/j.socscimed.2019.02.027", "Coresidence with mother-in-law and maternal anemia in rural India", "ELDER_SUPPORT", "decoy", "co-residence, non-fertility outcome"),
    ("10.1007/s13524-018-0719-y", "Beyond the Nuclear Family: Trends in Children Living in Shared Households", "LINK1_DRIVER_TO_ARRANGEMENT", "decoy", "arrangement trends, no fertility estimate"),
]


def main():
    rows, counts = [], {"FOUND": 0, "UNRESOLVED": 0, "ERROR": 0}
    for doi, recorded_title, cell, provenance, note in CANDIDATES:
        msg, err = crossref(doi)
        if err == "ERROR":
            status, resolved, first_author, j = "ERROR", None, None, None
        elif err == "NOT_IN_CROSSREF" or msg is None:
            status, resolved, first_author, j = "UNRESOLVED", None, None, None
        else:
            resolved = (msg.get("title") or [None])[0]
            authors = msg.get("author") or []
            first_author = None
            for a in authors:
                if a.get("sequence") == "first" or a is authors[0]:
                    first_author = " ".join(x for x in [a.get("given"), a.get("family")] if x)
                    break
            j = round(jaccard(recorded_title, resolved or ""), 2)
            status = "FOUND"
        counts[status] += 1
        rows.append({
            "doi": doi, "recorded_title": recorded_title, "resolved_title": resolved,
            "first_author": first_author,
            "container": ((msg or {}).get("container-title") or [None])[0] if msg else None,
            "year": (((msg or {}).get("issued") or {}).get("date-parts") or [[None]])[0][0] if msg else None,
            "type": (msg or {}).get("type") if msg else None,
            "title_jaccard": j, "existence": status,
            "identity_source": "crossref",
            "provisional_cell": cell, "provenance_channel": provenance, "note": note,
            "gold_status": "gold_candidate" if cell.startswith("PRIMARY") else "not_gold",
        })
        flag = "" if j is None or j >= 0.5 else "  <-- LOW TITLE OVERLAP, check"
        print(f"{status:10s} J={str(j):>4}  {doi:38s} {(resolved or '')[:52]}{flag}")

    existing = json.loads(OUT.read_text()) if OUT.exists() else {}
    payload = {
        "meta": {
            "ticket": "TICK-075",
            "hypothesis": "A.23 co-residence-parents-household-delay",
            "status": "anchors verified through the Crossref existence gate",
            "gate": "A live Crossref record, with FIRST-author agreement and an accent-tolerant title "
                    "fold. Verification is against Crossref and not OpenAlex, which is where the "
                    "candidates came from. UNRESOLVED is not 'absent'; ERROR is not a failed record.",
            "counts": counts,
            "n_candidates": len(CANDIDATES),
        },
        "v5_seminal_candidates": existing.get("v5_seminal_candidates", []),
        "anchors": rows,
    }
    OUT.write_text(json.dumps(payload, indent=1))
    print("\n" + "  ".join(f"{k}={v}" for k, v in counts.items()))
    print(f"wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
