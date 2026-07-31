#!/usr/bin/env python3
"""Effect-size extraction for the C.2.c identified core (TICK-055, pass 2).

Every figure below is read from the paper's OWN text AND checked to be the paper's OWN estimate
rather than a number it quotes from someone else. Both halves of that rule earned their keep:

- the 2021 HPR proceedings paper cites Dettling & Kearney as "6 percent" where D&K's own text says
  **5 percent**; and
- pass 2 of this extraction initially recorded "+1.28% to +2.11% per $12,000" as Daysal et al.'s
  estimate. It is their **footnote 4 summarising prior US literature**. Their actual result is
  +0.27 pp / +2.32% per 100,000 DKK. Caught during the preprint-vs-published reconciliation.

Being inside the right PDF is not sufficient. The number must also be the authors' own.

Sign convention (scope doc, pooling rule): oriented per unit INCREASE in the housing price/wealth
measure. Tenure channels are recorded separately and are NEVER combined.
"""
import csv

# work_id: list of effects. Each: (channel, treatment_unit, estimate, outcome, poolable, note)
EFFECTS = {
    "W3024244835": [
        ("cost_renter", "+$10,000 MSA house price", "-2.4%", "fertility rate, non-owners", "yes",
         "Verified at source."),
        ("wealth_owner", "+$10,000 MSA house price", "+5.0%", "fertility rate, owners", "yes",
         "Verified at source. NB the 2021 HPR proceedings paper misquotes this as 6%."),
        ("aggregate", "+$10,000 MSA house price", "+0.8%", "fertility rate, net at mean US ownership",
         "no (composition)", "Explicitly a composition-weighted net; secondary per the pooling rule."),
    ],
    "W3121393843": [
        ("aggregate", "+$10,000 lagged house price", "+2.0% odds of birth", "odds of a birth, pooled cross-section",
         "no (not tenure-split)", "Canada."),
        ("aggregate", "+$10,000 lagged house price", "+11.8% odds of birth", "odds of a birth, panel IV",
         "no (not tenure-split)", "Panel IV specification, col (3). Positive overall."),
    ],
    "W3023795878": [
        ("aggregate", "+1% housing price", "-0.94 pp", "probability of having a child", "no (not tenure-split)",
         "China. Robustness range 0.82-1.24 pp."),
    ],
    "W3037455063": [
        ("wealth_owner", "+100,000 DKK (~$12,000) home price", "+0.27 pp (= +2.32% vs mean)",
         "likelihood of giving birth, women 20-44 who own a home", "yes",
         "Denmark, population registers. RECONCILED 2026-07-31: the published JPubE abstract reports the "
         "identical headline (0.27 pp / 2.32%), so the preprint is usable FOR THIS ESTIMATE. Subsidiary "
         "specifications were not reconciled. CORRECTION: an earlier version of this table recorded "
         "'+1.28% to +2.11% per $12,000' as Daysal's estimate -- that is footnote 4 summarising PRIOR US "
         "literature (Lovenheim & Mumford, Dettling & Kearney), not their result."),
    ],
    "W4399107829": [
        ("aggregate", "+10% real house prices", "-0.030 births/woman (10th pctile of fertility)",
         "TFR", "no (quantile-varying)",
         "Global panel 1870-2012. Effect varies across the fertility distribution, so a single pooled "
         "coefficient would misrepresent it. THE ONLY IDENTIFIED FDT-PERIOD ESTIMATE."),
    ],
    "W4400391089": [
        ("wealth_owner", "+1% housing wealth", "+0.18%", "fertility rate", "yes",
         "RD design, China. Policy impact on wealth raises fertility likelihood by 7.3%."),
    ],
    "W4395680672": [
        ("cost_prospective_buyer", "+10% urban house price", "-0.88 births per 1,000",
         "crude birth rate", "yes", "Semi-elasticity 8.8. Implies ~2.46m fewer births, ~10.4% of the "
         "aggregate post-treatment birth decline. SSRN preprint, no published version."),
    ],
    "W7171437109": [
        ("credit_access", "housing-provident-fund credit easing (2014)", "+2.73 pp (= +20.8% over a 0.1314 baseline)",
         "probability of a new child", "NO - ROUTED TO C.3.e",
         "BOUNDARY CALL RESOLVED 2026-07-31, routed OUT of C.2.c. The reform 'expanded access by lowering "
         "down payment ratios, reducing interest rates, and raising loan ceilings'; the paper's own framing "
         "is 'improved access to preferential housing loans' and 'supporting groups facing credit "
         "constraints'. House prices do not vary -- credit terms do. Under the 2026-07-31 ruling C.3.e owns "
         "liquidity/credit variation. Flagged TO C.3.e as a strong quasi-experimental study for that "
         "chapter; it is not a C.2.c price estimate."),
    ],
    "W3144108245": [
        ("aggregate", "HPR policy (DiD)", "birth rate -5.45 'unit' (units not defined)", "birth rate",
         "NO - QUALITY", "Conference proceedings (Atlantis Press), not peer-reviewed. Authors describe "
         "their own coefficients as 'unlikely and ambiguous' and call for replication 'to draw a more "
         "accurate and unbiased result'. Units undefined. RECOMMEND DEMOTION from the identified core."),
    ],
    "W4308203433": [
        ("cost_rent", "public rental housing residence (not assignment)", "direction mixed; see note",
         "birth interval (tempo)", "no (associational; tempo outcome)",
         "OCR'd via macOS Vision. Finds delayed move-in produced a catch-up effect among non-resident "
         "households but delayed childbirth among public-rental households, and that second-birth intervals "
         "shortened sharply after moving in. No selection correction, so not an identified estimate. "
         "Outcome is a birth INTERVAL -- tempo, not quantum -- so it cannot pool with the quantum estimates "
         "in any case."),
    ],
}

study = {r["work_id"]: r for r in csv.DictReader(open("extraction/housing-costs-study-extraction.csv"))}
out = "extraction/housing-costs-effects.csv"
with open(out, "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["work_id", "doi", "year", "short_cite", "id_strength_confirmed", "channel",
                "treatment_unit", "estimate", "outcome", "poolable", "note",
                "source", "extracted_by", "extracted_date"])
    for wid, effs in EFFECTS.items():
        s = study.get(wid, {})
        cite = (s.get("title", "")[:44] + "…") if s.get("title") else wid
        for ch, tu, est, oc, pool, note in effs:
            w.writerow([wid, s.get("doi", ""), s.get("year", ""), cite,
                        s.get("id_strength_confirmed", ""), ch, tu, est, oc, pool, note,
                        "paper's own text", "Shravan/Claude", "2026-07-31"])

rows = list(csv.DictReader(open(out)))
from collections import Counter
print(f"effects table -> {out}")
print(f"effect rows: {len(rows)} across {len(EFFECTS)} studies\n")
print("poolable:", dict(Counter(r["poolable"] for r in rows)))
print("channel :", dict(Counter(r["channel"] for r in rows)))
