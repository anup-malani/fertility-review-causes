#!/usr/bin/env python3
"""
204_c3g_d1_rank.py — C.3.g, stage D1. Deterministic ranking and the cut into a screen worklist.

Collapses version duplicates on normalized title, scores the axes plus demotions, then builds the
worklist. Nothing is ever deleted: every record keeps its score, rank, hit lists and the reason it
did or did not make the worklist, so the cut can be re-made without re-running retrieval.

THE EXPOSURE AXIS IS SCORED HERE, UNLIKE A.17. A.17 could not score its exposure because the frame
was pulled entirely from ART seeds, making ART vocabulary ambient. C.3.g's pool is 83% citation
channel, one hop from anchors whose own topics include occupational choice, loan default and
parental retirement saving — so student-debt vocabulary is genuinely discriminating here rather than
universal, and the cross-axis AND does real work.

WHAT DISCRIMINATES: THREE OUTCOME AXES, SCORED SEPARATELY AND KEPT APART.
A4 settled that the chapter needs the union of fertility, union-formation and housing vocabulary —
a fertility-only frame reaches 5 of 21 anchors against 13, losing every identified study. But the
three axes mean different things to this chapter: FERTILITY is the registered estimand, UNION and
HOUSING are link 1 of a chain whose link 2 belongs to other chapters. They are scored separately,
their hits are kept apart on every record, and fertility is weighted highest — a ranker that cannot
tell the chapter's own outcome from its neighbour's would sort the chain arm to the top and call it
precision.

IDENTIFICATION GETS A REAL BONUS AND POLICY GETS A LARGER ONE. A4 measured only 5 records in the
whole citation neighbourhood carrying debt AND fertility AND identification, and exactly one P2
candidate. When a cell is that thin, the ranking cannot afford to bury a member of it, and a bonus
firing on a fraction of a per cent cannot distort anything else.

DEMOTION WEIGHTS COME FROM A4's IN-FRAME MEASUREMENTS, NOT FROM THE QUERY-LEVEL SIZES:
  * WALL 1 (health-professions career) is the heaviest. It is the largest body sharing this
    chapter's exposure vocabulary and its overlap with a fertility outcome is 19 records at query
    level. But it is DEMOTED, NEVER DROPPED: the overlap is real and in scope by the
    route-by-outcome rule, and two of its members report childbearing decisions directly.
  * WALL 3 (default and repayment) next: 706 records at query level, 3 of them touching fertility.
  * WALLS 2, 5/6 and 7 take lighter weights — each is small in-frame, and Wall 7 in particular
    contains a genuine quasi-experiment (Bhuwania et al.) that must stay visible to be routed out
    deliberately rather than lost.

BYPASSES — populations where a miss cannot be recovered downstream, and which therefore skip the
score cut entirely. Per-bypass yield is reported at assembly, because the standing rule from A.12 is
that an inherited bypass which has stopped paying gets retired rather than carried forever.

Output: literature/search-logs/{slug}-d1-ranked.json
        literature/search-logs/{slug}-d1-log.md
"""
import json, os, re, sys, unicodedata
from collections import Counter

SLUG = "student-debt-household-formation"
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
LOGS = os.path.join(ROOT, "literature", "search-logs")
POOL = os.path.join(LOGS, f"{SLUG}-pool.json")
OUT = os.path.join(LOGS, f"{SLUG}-d1-ranked.json")
OUT_LOG = os.path.join(LOGS, f"{SLUG}-d1-log.md")

# Punctuation classes folded BEFORE the ASCII strip, apostrophes deleted and dashes spaced. This is
# the fix from `201_`: without it "Can't" and "Can’t" normalise to different token counts, which
# here would ALSO split a version-duplicate pair instead of collapsing it.
_APOS = re.compile("['‘’ʼ´`]")
_DASH = re.compile("[-‐‑‒–—―−­]")


def norm(s):
    s = _APOS.sub("", s or "")
    s = _DASH.sub(" ", s)
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode("ascii")
    s = re.sub(r"[^a-z0-9 ]", " ", s.lower())
    return re.sub(r"\s+", " ", s).strip()


DEBT_RX = re.compile(
    r"student loan|student debt|student borrow|college debt|educational debt|education debt|"
    r"education loan|tuition loan|loan for college|student indebtedness|graduate indebtedness")
FERT_TERMS = ("fertility", "childbearing", "first birth", "births", "birth rate", "childless",
              "number of children", "family size", "transition to parenthood", "parenthood",
              "having children", "family formation", "fecundity")
UNION_TERMS = ("marriage", "marital", "cohabit", "union formation", "partnership formation",
               "age at marriage", "marriage timing", "getting married")
HOUSE_TERMS = ("homeownership", "home ownership", "housing tenure", "first-time buyer",
               "first-time homebuyer", "home purchase", "household formation", "living with parents",
               "parental home", "coresidence", "co-residence", "residential independence",
               "leaving home", "mortgage origination")
IDENT_TERMS = ("difference-in-differences", "difference in differences", "natural experiment",
               "quasi-experimental", "quasi experimental", "instrumental variable", "instrument for",
               "regression discontinuity", "regression kink", "event study", "exogenous variation",
               "causal effect", "causal impact", "randomi", "experiment", "rct",
               "synthetic control", "propensity score", "treatment effect", "identification strategy")
POLICY_TERMS = ("loan forgiveness", "debt forgiveness", "debt cancellation", "debt relief",
                "loan discharge", "income-driven repayment", "income driven repayment",
                "income contingent", "repayment plan", "loan limit", "borrowing limit",
                "tuition policy", "tuition-free", "tuition free", "free college", "free tuition",
                "financial aid reform", "pell grant", "state appropriations", "loan program")
ATTAIN_TERMS = ("educational attainment", "college completion", "degree completion",
                "controlling for education", "conditional on education", "holding education",
                "college graduates", "bachelor's degree", "degree holders", "completed college")
CAREER_TERMS = ("specialty choice", "career choice", "practice location", "rural practice",
                "residency program", "physician workforce", "primary care shortage", "medical student",
                "dental student", "veterinary student", "resident physician", "medical school")
GENDEBT_TERMS = ("household debt", "consumer debt", "credit card", "mortgage debt", "medical debt",
                 "payday", "unsecured debt", "auto loan")
DEFAULT_TERMS = ("loan default", "delinquen", "repayment behavio", "default rate", "loan servicing",
                 "defaulting")
PARENTPAY_TERMS = ("saving for college", "college savings", "paying for college",
                   "parental contribution", "parent plus", "parent borrow", "529 plan")
LMIC_TERMS = ("school fees", "child marriage", "sub-saharan", "low-income countries",
              "developing countries", "primary schooling")

W = dict(debt=6, fert=5, union=3, house=3, ident=3, policy=4, attain=1,
         career=-6, gendebt=-3, default=-4, parentpay=-3, lmic=-3)
SCORE_CUT = 8          # re-cuttable: nothing below it is deleted, only left off the worklist


def hits(blob, terms):
    return [t for t in terms if t in blob]


def main():
    pool = json.load(open(POOL))

    # ---- version-duplicate collapse on normalized title ----
    by_title, order = {}, []
    for r in pool:
        k = norm(r["title"])
        if not k:
            k = r["id"]
        if k in by_title:
            keep = by_title[k]
            # Prefer the record with an abstract, then the higher citation count. A version pair
            # where one copy is a bare preprint stub and the other the indexed article should
            # collapse onto the one a screener can actually read.
            better = (bool(r.get("abstract")), r.get("cited_by_count") or 0) > \
                     (bool(keep.get("abstract")), keep.get("cited_by_count") or 0)
            merged_ch = sorted(set(keep.get("channels", [])) | set(r.get("channels", [])))
            target = r if better else keep
            other = keep if better else r
            target = dict(target)
            target["channels"] = merged_ch
            target["is_anchor"] = bool(keep.get("is_anchor") or r.get("is_anchor"))
            target["anchor_cell"] = keep.get("anchor_cell") or r.get("anchor_cell")
            target.setdefault("collapsed_ids", [])
            target["collapsed_ids"] = sorted(set(target["collapsed_ids"] +
                                                 (other.get("collapsed_ids") or []) + [other["id"]]))
            by_title[k] = target
        else:
            by_title[k] = r
            order.append(k)
    collapsed = len(pool) - len(by_title)
    recs = [by_title[k] for k in order]

    for r in recs:
        blob = " " + (r["title"] + " " + (r.get("abstract") or "")).lower() + " "
        r["debt_hits"] = sorted(set(m.group(0) for m in DEBT_RX.finditer(blob)))
        r["fert_hits"] = hits(blob, FERT_TERMS)
        r["union_hits"] = hits(blob, UNION_TERMS)
        r["house_hits"] = hits(blob, HOUSE_TERMS)
        r["ident_hits"] = hits(blob, IDENT_TERMS)
        r["policy_hits"] = hits(blob, POLICY_TERMS)
        r["attain_hits"] = hits(blob, ATTAIN_TERMS)
        r["career_hits"] = hits(blob, CAREER_TERMS)
        r["gendebt_hits"] = hits(blob, GENDEBT_TERMS)
        r["default_hits"] = hits(blob, DEFAULT_TERMS)
        r["parentpay_hits"] = hits(blob, PARENTPAY_TERMS)
        r["lmic_hits"] = hits(blob, LMIC_TERMS)
        r["has_abstract"] = bool(r.get("abstract"))
        s = 0
        s += W["debt"] if r["debt_hits"] else 0
        s += W["fert"] if r["fert_hits"] else 0
        s += W["union"] if r["union_hits"] else 0
        s += W["house"] if r["house_hits"] else 0
        s += W["ident"] if r["ident_hits"] else 0
        s += W["policy"] if r["policy_hits"] else 0
        s += W["attain"] if r["attain_hits"] else 0
        for k in ("career", "gendebt", "default", "parentpay", "lmic"):
            if r[f"{k}_hits"]:
                s += W[k]
        r["d1_score"] = s

    recs.sort(key=lambda r: (-r["d1_score"], -(r.get("cited_by_count") or 0)))
    for i, r in enumerate(recs, 1):
        r["d1_rank"] = i

    # ---- worklist: the score cut, plus bypasses where a miss is unrecoverable ----
    for r in recs:
        reasons = []
        if r["d1_score"] >= SCORE_CUT:
            reasons.append("score_cut")
        if r.get("is_anchor"):
            reasons.append("bypass_anchor")
        if "keyword" in r.get("channels", []):
            # The scope promised to screen the query frame WHOLE — it is 401 records and screening
            # cost has never been this project's binding constraint. Screening it whole is also what
            # makes Recall(B) against the citation channel interpretable.
            reasons.append("bypass_keyword_frame")
        if len(r.get("channels", [])) > 1:
            reasons.append("bypass_both_channels")
        if r["debt_hits"] and r["policy_hits"] and r["fert_hits"]:
            # The P2 cell. A4 found exactly one member and the scope's central claim turns on it.
            reasons.append("bypass_p2_cell")
        if r["debt_hits"] and r["ident_hits"] and r["fert_hits"]:
            reasons.append("bypass_identified_fertility")
        if not r["has_abstract"] and DEBT_RX.search(" " + r["title"].lower() + " "):
            # A title-only record naming the exposure cannot be judged on an abstract it does not
            # have. Dropping it on a low score converts missing metadata into negative evidence —
            # and this is not hypothetical here: the chapter's most-cited primary-cell anchor,
            # Nau et al., has no indexed abstract.
            reasons.append("bypass_title_only_exposure")
        r["worklist_reason"] = reasons
        r["in_worklist"] = bool(reasons)

    work = [r for r in recs if r["in_worklist"]]
    json.dump(recs, open(OUT, "w"), indent=2)

    byp = Counter()
    for r in work:
        for reason in r["worklist_reason"]:
            byp[reason] += 1
    only = Counter()
    for r in work:
        if len(r["worklist_reason"]) == 1:
            only[r["worklist_reason"][0]] += 1

    n_abs = sum(1 for r in work if r["has_abstract"])
    dist = Counter(r["d1_score"] for r in recs)

    L = [f"# D1 deterministic ranking — {SLUG} (C.3.g)", "",
         f"**Generated by:** `source/build/goldset/204_c3g_d1_rank.py`", "",
         f"Pool {len(pool):,} records; **{collapsed:,} version duplicates collapsed** on normalized "
         f"title, leaving **{len(recs):,}**. The normalizer carries `201_`'s punctuation fix — "
         "without it an ASCII and a curly apostrophe fold to different token counts, which here "
         "would SPLIT a duplicate pair instead of collapsing it.", "",
         f"**Worklist: {len(work):,} records** ({len(work) / max(len(recs), 1):.0%} of the pool). "
         f"Nothing is deleted — every record below the cut keeps its score, rank and hit lists in "
         f"`{os.path.basename(OUT)}` and the cut can be re-made without re-running retrieval.", "",
         f"{n_abs:,} of {len(work):,} worklist records ({n_abs / max(len(work), 1):.0%}) carry an "
         "abstract.", "",
         "## Worklist composition", "",
         "A record can qualify several ways. The second column is what would be LOST if that route "
         "were removed — the number for which it is the only reason.", "",
         "| Route | Records | Sole reason |", "|---|---|---|"]
    for k, v in byp.most_common():
        L.append(f"| `{k}` | {v:,} | {only.get(k, 0):,} |")
    L += ["", "## Score distribution", "",
          "| Score | Records | In worklist |", "|---|---|---|"]
    for sc in sorted(dist, reverse=True):
        inw = sum(1 for r in recs if r["d1_score"] == sc and r["in_worklist"])
        L.append(f"| {sc} | {dist[sc]:,} | {inw:,} |")
    L += ["", f"Cut at **{SCORE_CUT}**. The cut alone would take "
          f"{sum(1 for r in recs if r['d1_score'] >= SCORE_CUT):,} records; the bypasses add "
          f"{len(work) - sum(1 for r in recs if r['d1_score'] >= SCORE_CUT):,} more that the blind "
          "sieve would have missed.", "",
          "## What the ranker is NOT doing", "",
          "It is semantically blind. It cannot tell a study that ESTIMATES a debt effect on births "
          "from one that mentions both in a literature review, and it cannot tell the direct arm "
          "from the chain arm — it can only tell which outcome VOCABULARY a record carries. Both "
          "distinctions are the screen's job, and D1's score is deliberately withheld from the "
          "screener so the two sieves stay independent.", ""]
    open(OUT_LOG, "w").write("\n".join(L) + "\n")
    print(f"pool {len(pool)} -> {len(recs)} after collapsing {collapsed}; worklist {len(work)}")
    print("bypass counts:", dict(byp))


if __name__ == "__main__":
    main()
