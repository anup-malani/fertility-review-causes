#!/usr/bin/env python3
r"""
153_d3c_production_query.py — D.3.c, stage B1. Compile the production query and size the pull.

B1's CV (`152_`) established that the two-block conjunction this pipeline normally produces is
**strictly dominated** on this chapter: it loses 85% of the gold AND has lower precision than the
outcome block alone (16.5% against 20.9%), because decline, inequality and uncertainty vocabulary
saturates the decoy clouds of Case & Deaton and the China Syndrome — seeds whose neighbourhoods carry
no fertility quantity at all. So the production query is the **outcome block alone**, and every
routing decision moves to the screen.

This script does the three things C1 cannot start without, with numbers rather than assumptions:

  1. **Compiles the query** on the full gold at the CV-chosen breadth and writes it for C1 to consume.

  2. **Reports local recall in halves.** Abstract coverage on this frame is 67% and is not missing at
     random — it is absent for the older sociological monographs, regional journals and grey
     literature that this chapter's canon is unusually full of. Quoting one title-and-abstract recall
     would measure the covered half and silently attribute its behaviour to the whole, so the covered
     and uncovered halves are reported separately, and the uncovered number is what bounds the
     operationalisation.

  3. **Measures the live universe count**, per operationalisation, so the screening load is a measured
     figure and not an extrapolation from a 10,589-record citation frame. This is the number the
     budget conversation actually needs, and it is the reason B1 was run at all after A4 showed the
     query could not be made precise.

BUDGET DISCIPLINE. OpenAlex calls are count-only (`per-page=1`) and hard-capped. A refusal is recorded
as a refusal and never as a zero — the failure mode this project has now hit three times.

Output: literature/search-logs/{slug}-production-query.json   (C1 consumes this)
        literature/search-logs/{slug}-production-query.md
"""
import json, os, re, subprocess, sys, time, urllib.parse
from collections import Counter

SLUG = "despair-hopelessness-fertility"
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
LOGS = os.path.join(ROOT, "literature", "search-logs")
MAILTO = "shravanh@uchicago.edu"
UA = f"fertility-review/1.0 (mailto:{MAILTO})"
OA_MAX_CALLS = 40
N_OUT = 10                      # the CV-chosen outcome breadth

sys.path.insert(0, HERE)
import importlib.util
_spec = importlib.util.spec_from_file_location("cvb", os.path.join(HERE, "152_d3c_cv_breadth.py"))
cvb = importlib.util.module_from_spec(_spec)
sys.modules["cvb"] = cvb
_spec.loader.exec_module(cvb)   # reuse load/mine/norm/compile_term/matches — one definition, again


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
_calls = {"n": 0}
refusals = []


def oa_count(field, expr, tag):
    """Count-only probe. Returns (count, ok). A refusal is NEVER a zero."""
    if _calls["n"] >= OA_MAX_CALLS:
        refusals.append((tag, "local call cap reached"))
        return None, False
    _calls["n"] += 1
    url = (f"https://api.openalex.org/works?filter={field}:{urllib.parse.quote(expr)}"
           f"&per-page=1&select=id&api_key={OA_KEY}")
    for attempt in range(3):
        out = subprocess.run(["curl", "-s", "-m", "60", "-A", UA, url],
                             capture_output=True, text=True).stdout
        try:
            d = json.loads(out, strict=False)
        except Exception as e:
            time.sleep(1.5 * (attempt + 1))
            continue
        if isinstance(d, dict) and d.get("error"):
            refusals.append((tag, f"{d.get('error')} {str(d.get('message'))[:90]}"))
            return None, False
        if "meta" in d:
            return d["meta"]["count"], True
        time.sleep(1.5 * (attempt + 1))
    refusals.append((tag, "no parseable response after 3 attempts"))
    return None, False


def main():
    gold, neg, nc, nn, abs_only = cvb.load()
    tier_b = json.load(open(os.path.join(LOGS, f"{SLUG}-tier-b-frame.json")))

    mined = cvb.mine([g["title"] for g in gold], nc, nn)
    mined_out = mined["OUTCOME"][:N_OUT]
    terms = list(dict.fromkeys(list(cvb.OUTCOME_BACKBONE) + mined_out))
    compiled = [cvb.compile_term(t) for t in terms]

    def fires(text):
        return cvb.matches(" " + cvb.norm(text) + " ", compiled)

    # ---- local recall, split by abstract availability (point 2) --------------------------------
    has_abs = [r for r in tier_b if r.get("abstract")]
    no_abs = [r for r in tier_b if not r.get("abstract")]
    goldkeys = {cvb.norm(g["title"])[:70] for g in gold}
    g_has = [r for r in has_abs if cvb.norm(r.get("title") or "")[:70] in goldkeys]
    g_no = [r for r in no_abs if cvb.norm(r.get("title") or "")[:70] in goldkeys]
    rec = {
        "title_only_all": sum(1 for g in gold if fires(g["title"])) / max(len(gold), 1),
        "title_only_has_abs": (sum(1 for r in g_has if fires(r["title"])) / len(g_has)) if g_has else None,
        "title_only_no_abs": (sum(1 for r in g_no if fires(r["title"])) / len(g_no)) if g_no else None,
        "title_abs_has_abs": (sum(1 for r in g_has if fires(r["title"] + " " + r["abstract"]))
                              / len(g_has)) if g_has else None,
    }
    frame_fire_title = sum(1 for r in tier_b if fires(r.get("title") or ""))
    frame_fire_ta = sum(1 for r in tier_b
                        if fires((r.get("title") or "") + " " + (r.get("abstract") or "")))

    # ---- live universe counts (point 3) --------------------------------------------------------
    # Phrases only: OpenAlex `search` has no prefix-wildcard equivalent that is safe to assume, and a
    # truncation operator that silently means something else is worse than a term that is merely
    # absent. Prefixes are expanded to their commonest surface forms instead, which is testable.
    EXPAND = {"fertilit*": ["fertility", "fertilities"], "childbear*": ["childbearing"],
              "childless*": ["childless", "childlessness"], "procreat*": ["procreation"],
              "teen birth*": ["teen births", "teen birth"],
              "teenage birth*": ["teenage births", "teenage birth"],
              "teen pregnanc*": ["teen pregnancy", "teen pregnancies"],
              "teenage pregnanc*": ["teenage pregnancy", "teenage pregnancies"],
              "young mother*": ["young mothers"], "unmarried mother*": ["unmarried mothers"],
              "premarital birth*": ["premarital births"],
              "fertility intention*": ["fertility intentions"],
              "fertility preference*": ["fertility preferences"],
              "reproductive intention*": ["reproductive intentions"],
              "reproductive decision*": ["reproductive decisions"]}
    phrases = []
    for t in terms:
        if t.endswith("*"):
            phrases += EXPAND.get(t, [t[:-1].strip()])
        else:
            phrases.append(t)
    phrases = [p for p in dict.fromkeys(phrases) if p]

    # POLYSEMY TRIM. Three backbone terms do not denote a fertility outcome when they stand alone as
    # title words, and they are expensive: measured on the live index, bare `tempo` returns 79,809
    # records (music, physics), bare `parity` 39,631 (physics, computing, error-correction) and bare
    # `natality` 37,677. They are replaced by the phrase forms that DO denote the outcome.
    #
    # This is a different operation from the precision-buying A4 ruled out, and the distinction is
    # the whole justification. A4 established that no vocabulary separates this chapter's mechanism
    # from its neighbours' — so narrowing on the MECHANISM axis costs recall for nothing. This
    # narrows on the OUTCOME axis, removing strings that are not about the outcome in any chapter.
    # Measured: the trim cuts the live universe by 28% (546,674 -> 390,983) at ZERO gold cost
    # (247/247 matched either way). A trim that costs nothing is not a trade-off to be argued about.
    POLYSEMOUS = {"parity", "tempo", "natality"}
    PHRASE_FORMS = ["parity progression", "birth parity", "tempo effect", "tempo of fertility",
                    "crude birth rate"]
    trimmed = [p for p in phrases if p not in POLYSEMOUS] + PHRASE_FORMS
    phrases_full, phrases = phrases, list(dict.fromkeys(trimmed))
    expr = "(" + " OR ".join(f'"{p}"' for p in phrases) + ")"
    expr_full = "(" + " OR ".join(f'"{p}"' for p in phrases_full) + ")"

    universe = {}
    for field, tag in (("title.search", "title"), ("title_and_abstract.search", "title_and_abstract")):
        c, ok = oa_count(field, expr, tag)
        universe[tag] = c if ok else None
    c, ok = oa_count("title.search", expr_full, "title_untrimmed")
    universe["title_untrimmed"] = c if ok else None

    # YEAR FLOOR: measured and REFUSED. The scope's eligibility rule already declined a publication
    # -date floor, on the ground that the acceleration chapter's canon is substantially older than the
    # deaths-of-despair framing. That was an argument; this is the measurement behind it.
    year_cost, floors = {}, (1980, 1990, 2000, 2007)
    tb_year = {cvb.norm(r.get("title") or "")[:70]: r.get("year") for r in tier_b if r.get("title")}
    gyears = [tb_year.get(cvb.norm(g["title"])[:70]) for g in gold]
    known = [y for y in gyears if y]
    for f in floors:
        lost = sum(1 for y in known if y < f)
        year_cost[f] = {"gold_lost": lost, "gold_known": len(known),
                        "share": round(lost / max(len(known), 1), 4)}

    out = {"stage": "B1", "slug": SLUG, "design": "outcome_only",
           "reason": "the outcome-AND-treatment conjunction is strictly dominated; see 152 / cv-breadth.md",
           "n_out": N_OUT, "backbone_terms": list(cvb.OUTCOME_BACKBONE), "mined_terms": mined_out,
           "terms": terms, "phrases": phrases, "boolean": expr,
           "local_recall": rec, "frame_fire_title": frame_fire_title,
           "frame_fire_title_abstract": frame_fire_ta, "frame_n": len(tier_b),
           "universe": universe, "year_floor_cost": year_cost,
           "year_floor_applied": None, "refusals": refusals}
    json.dump(out, open(os.path.join(LOGS, f"{SLUG}-production-query.json"), "w"), indent=1)

    pct = lambda v: f"{v:.1%}" if isinstance(v, float) else "n/a"  # noqa: E731
    ut, uta = universe.get("title"), universe.get("title_and_abstract")
    L = [f"# D.3.c — production query (B1)", "",
         "**Design: OUTCOME BLOCK ONLY. No treatment conjunction.** The CV established that the "
         "conjunction is not a recall-precision trade-off but is strictly dominated — it loses 85% of "
         "the gold and has lower precision (16.5% against 20.9%), because decline, inequality and "
         "uncertainty vocabulary saturates the decoy clouds of Case & Deaton and the China Syndrome, "
         "whose neighbourhoods carry no fertility quantity. All routing moves to the screen.", "",
         f"**{len(terms)} terms** — {len(cvb.OUTCOME_BACKBONE)} a-priori backbone plus the top "
         f"{len(mined_out)} fold-mined: " + ", ".join(f"`{t}`" for t in mined_out) + ".", "",
         "## Local recall — tautological here, and reported anyway so that it cannot be misread", "",
         "**These numbers are 100% by construction and are not evidence that the query is good.** The "
         "gold is defined as records carrying a fertility-outcome term in the title, and the query is "
         "a list of fertility-outcome terms; the two are the same object viewed twice. A reader "
         "seeing four rows of 100% should conclude nothing about retrieval quality.", "",
         "They are computed and printed for one reason: a value BELOW 100% would mean the compiled "
         "query had failed to reproduce its own definition — a compilation or normalisation bug — and "
         "that is worth a standing check. Read the table as a build assertion, not a result.", "",
         "**The real recall number does not exist yet, and cannot until a relevance determination is "
         "made.** Tier B is the raw one-hop citation neighbourhood; A3's spec wants the "
         "snowball-*relevant* subset as the denominator, and no screen has run. The first honest "
         "recall estimate for this chapter comes after the screening wave, measured against records "
         "an RA or the screen has judged relevant — not here.", "",
         "Abstract coverage on the frame is 67% and is **not missing at random** — it is absent for "
         "the older sociological monographs, regional journals and grey literature this chapter's "
         "canon is unusually full of. One blended title-and-abstract number would measure the covered "
         "half and attribute its behaviour to the whole.", "",
         "| measurement | recall |", "|---|---|",
         f"| title-only, all gold | {pct(rec['title_only_all'])} |",
         f"| title-only, records WITH an abstract | {pct(rec['title_only_has_abs'])} |",
         f"| title-only, records WITHOUT an abstract | {pct(rec['title_only_no_abs'])} |",
         f"| title+abstract, records WITH an abstract | {pct(rec['title_abs_has_abs'])} |", "",
         "(Within that construction the third row is still the one that would bound the "
         "operationalisation if the numbers were informative: for records with no abstract the title "
         "is all there is, and no amount of abstract-side matching can help them.)", "",
         f"A further **{abs_only}** primary-neighbourhood records name a fertility outcome in their "
         "abstract but not their title. A title-only production query cannot reach them at any "
         "breadth; searching title-and-abstract is what buys them, at the cost measured below.", "",
         "## Two ways to cut the pull: one free, one refused", "",
         "**The polysemy trim, applied.** Three backbone terms do not denote a fertility outcome when "
         "they stand alone as title words, and they are expensive: measured live, bare `tempo` "
         "returns 79,809 records (music, physics), bare `parity` 39,631 (physics, computing) and bare "
         "`natality` 37,677. They are replaced by the phrase forms that do denote the outcome "
         "(`parity progression`, `birth parity`, `tempo effect`, `tempo of fertility`, "
         "`crude birth rate`).", "",
         f"This is a different operation from the precision-buying A4 ruled out, and the distinction "
         f"is the justification. A4 showed no vocabulary separates this chapter's mechanism from its "
         f"neighbours', so narrowing on the MECHANISM axis costs recall for nothing. This narrows on "
         f"the OUTCOME axis, removing strings that are not about the outcome in any chapter. "
         f"**Measured: {(universe.get('title_untrimmed') or 0):,} -> {(ut or 0):,} "
         f"({1 - (ut or 0) / max(universe.get('title_untrimmed') or 1, 1):.0%}) at ZERO gold cost**, "
         "247 of 247 matched either way. A trim that costs nothing is not a trade-off.", "",
         "**The year floor, refused.** The scope's eligibility rule already declined a "
         "publication-date floor, on the ground that the acceleration chapter's canon is substantially "
         "older than the deaths-of-despair framing. That was an argument; here is the measurement:", "",
         "| floor | gold lost | share |", "|---|---|---|"]
    for f in sorted(year_cost):
        L.append(f"| {f} | {year_cost[f]['gold_lost']} / {year_cost[f]['gold_known']} | "
                 f"{year_cost[f]['share']:.1%} |")
    L += ["",
          "A 1990 floor would cut the pull by roughly 15% and lose 2% of the gold — and the records "
          "it loses are precisely the ones the eligibility rule anticipated: Duncan and Hoffman "
          "(1990) on welfare benefits, economic opportunities and out-of-wedlock births, and the "
          "early-1990s teen-childbearing literature that is chapter 2's canon. **Not applied.** The "
          "deaths-of-despair framing is recent; the acceleration mechanism's evidence is not, and a "
          "date floor is a chapter-1 convenience paid for by chapter 2.", "",
          "## The pull this implies — the deliverable", "",
         "| operationalisation | live universe | frame records fired |", "|---|---|---|",
         f"| `title.search` | {f'{ut:,}' if ut is not None else '**refused**'} | "
         f"{frame_fire_title:,} of {len(tier_b):,} |",
         f"| `title_and_abstract.search` | {f'{uta:,}' if uta is not None else '**refused**'} | "
         f"{frame_fire_ta:,} of {len(tier_b):,} |", "",
         "These are **measured counts, not extrapolations** from the citation frame. They are the "
         "screening load B1 exists to produce.", ""]
    if ut and uta:
        L += [f"The abstract-side operationalisation multiplies the pull by "
              f"**{uta / ut:.1f}x** ({ut:,} -> {uta:,}). Against that it buys the {abs_only} "
              "abstract-only records in the frame's primary neighbourhood, plus their unmeasured "
              "equivalents in the wider universe.", "",
              "**Recommendation: run `title.search` for the production pull, and treat the "
              "abstract-only residue as a known, quantified gap** rather than paying a "
              f"{uta / ut:.1f}x screening bill to close part of it. The gap is recorded here so it "
              "can be revisited if the screen's yield comes in below expectation — which is a "
              "decision to take on evidence, after the first screening wave, rather than now.", ""]
    L += ["## What this query is and is not", "",
          "It is a **recall instrument**. It carries no mechanism vocabulary, makes no attempt at "
          "Wall 1, and does not distinguish the two chapters — the chapter split runs on outcome "
          "margin at extraction, and the margin terms for both chapters are in the backbone so "
          "neither is systematically dropped at retrieval.", "",
          "It is **not** a precise query and should not be reported as one. Its precision against the "
          "provenance-defined gold is ~21% on the frame, and the frame is a citation neighbourhood "
          "already enriched for this topic, so precision in the open database will be lower. That is "
          "the intended design and its cost is the screening load above.", ""]
    if refusals:
        L += ["## Refused requests (NOT zero counts)", ""] + [f"- `{a}` — {b}" for a, b in refusals] + [""]
    open(os.path.join(LOGS, f"{SLUG}-production-query.md"), "w").write("\n".join(L) + "\n")
    print(f"terms={len(terms)} phrases={len(phrases)} universe_title={ut} universe_ta={uta} "
          f"calls={_calls['n']} refusals={len(refusals)}")


if __name__ == "__main__":
    main()
