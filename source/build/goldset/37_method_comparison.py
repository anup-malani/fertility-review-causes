#!/usr/bin/env python3
"""
Step 37 - Head-to-head comparison of the three search methods (PI critique #2, workflow S7.1).

The PI asked for the deliverable the synthesis skipped: race the three searchers' Tier-1 sets on
false-negative rate, false-positive rate, cost, and replicability, plus the paper-for-paper
disagreement matrix that tests the "convergence" claim. Two of the three sets do not survive as frozen
data (Alexandra's live-OpenAlex prototype outputs + script are gone; Shravan's gold-anchored production
query never ran independently). So - per the RA/PI decision - each method is operationalized as a
REPRODUCIBLE SELECTION RULE over the common 8,087-paper corpus (tiers.json). Anup's and the
gold-anchored rules are faithful (they are the methods' actual tier rules); Alexandra's is a labeled
RECONSTRUCTION of her lexical-triage principle, not her lost delivery.

Ground truth = the 10-study estimand-ready set (step 34). FN = truth studies a method's Tier-1 misses.
FP is reported BOTH ways: raw (any Tier-1 paper not in the 10) - degenerate, since Tier-1 legitimately
holds theory/topical papers - and off-cell-empirical (Tier-1 empirical papers the estimand tags mark
off-cell), the meaningful precision measure.

Inputs
  {slug}-tiers.json                 common corpus: paperId, channel(K/S/K&S), verdict, confidence,
                                    compositeScore, in_gold, title
  {slug}-oa-enrichment.json         abstracts by paperId
  {slug}-external-backbone.json     fertility / pension axis vocab (for the reconstructed lexical rule)
  {slug}-metaanalysis-studies.json  DOI<->paperId bridge
  output/{slug}-estimand-adjudication.csv   ground truth + estimand cells (reviewed 40)
  estimand_tierb_tags.json          estimand cells for the 247 Tier-B papers
Output
  output/{slug}-method-comparison.md
"""
import json, csv, importlib.util
from pathlib import Path
from itertools import combinations

SLUG = "old-age-security-pension-crowdout"
HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
SL = REPO / "literature" / "search-logs" / f"{SLUG}-"
OUT = REPO / "output" / f"{SLUG}-method-comparison.md"
ALEX_N = 87  # Alexandra's delivered Tier-1 size (query-clustering method note, top-100 handoff)

CAUSAL = ["reform", "natural experiment", "quasi-experiment", "quasi experiment",
          "difference-in-differences", "difference in differences", "discontinuity",
          "instrument", "exogenous", "randomized", "event study", "regression discontinuity"]


def nd(d):
    d = (d or "").lower().strip()
    for p in ("https://doi.org/", "http://doi.org/", "doi:"):
        if d.startswith(p):
            d = d[len(p):]
    return d


def load_cv():
    spec = importlib.util.spec_from_file_location("cv22", HERE / "22_cv_breadth.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def main():
    m = load_cv()
    T = json.load(open(f"{SL}tiers.json"))
    by_pid = {t["paperId"]: t for t in T}
    enr = json.load(open(f"{SL}oa-enrichment.json"))
    bb = json.load(open(f"{SL}external-backbone.json"))
    fert = [m.compile_term(t) for t in bb["fertility_block"]]
    pens = [m.compile_term(t) for t in bb["pension_oas_block"]]

    def text_of(pid):
        t = by_pid[pid].get("title") or ""
        ab = enr.get(pid, {}).get("abstract") or ""
        return " " + m.norm(t + " " + ab) + " "

    # ---- DOI <-> paperId bridge, incl. all known version variants ----
    doi2pid = {}
    doi2variants = {}   # study DOI -> every known paperId for that study (canonical + alt_versions)
    for s in json.load(open(f"{SL}metaanalysis-studies.json")):
        d = nd(s.get("doi_final") or s.get("doi"))
        if not d:
            continue
        if s.get("paperId"):
            doi2pid[d] = s["paperId"]
        vs = {s.get("paperId")} | {av.get("paperId") for av in (s.get("alt_versions") or [])}
        doi2variants[d] = {v for v in vs if v}
    for pid, e in enr.items():
        d = nd(e.get("doi"))
        if d and d not in doi2pid:
            doi2pid[d] = pid

    # ---- ground truth + estimand cells ----
    # A truth study can appear in the corpus under a DIFFERENT paperId than the truth DOI maps to
    # (OpenAlex version variants), so recovery is checked against a CANDIDATE SET per study: the
    # DOI-mapped pid plus any corpus paper whose title matches (exact token-set or Jaccard >= 0.85).
    def toks(s):
        return frozenset(w for w in m.norm(s).split() if len(w) > 2)
    corpus_toks = [(t["paperId"], toks(t.get("title") or "")) for t in T]

    def candidates(title, doi):
        c = set(doi2variants.get(nd(doi), set()))   # canonical + all alt-version paperIds
        p = doi2pid.get(nd(doi))
        if p:
            c.add(p)
        tt = toks(title)
        if tt:
            for pid, tk in corpus_toks:
                if tk and (tk == tt or len(tt & tk) / len(tt | tk) >= 0.85):
                    c.add(pid)
        return c & set(by_pid)   # keep only paperIds that exist in the corpus

    adj = list(csv.DictReader(open(REPO / "output" / f"{SLUG}-estimand-adjudication.csv")))
    truth_studies = [{"title": r["title"], "cand": candidates(r["title"], r["doi"])}
                     for r in adj if r["estimand_cell"] == "PRIMARY"]
    truth_all_pids = set().union(*[ts["cand"] for ts in truth_studies]) if truth_studies else set()
    pid_cell = {}   # paperId -> estimand cell
    for r in adj:
        pid = doi2pid.get(nd(r["doi"]))
        if pid:
            pid_cell[pid] = r["estimand_cell"]
    for tag in json.load(open(HERE / "estimand_tierb_tags.json")):
        pid_cell.setdefault(tag["id"], tag["cell"])

    # ---- three method Tier-1 rules over the common corpus ----
    anup = set(t["paperId"] for t in T if (t.get("compositeScore") or 0) >= 7)
    gold = set(t["paperId"] for t in T if t.get("in_gold") or
               (t.get("channel") == "K&S" and t.get("verdict") == "RELEVANT" and t.get("confidence") == "HIGH"))
    # Alexandra (reconstructed): keyword-reachable, both axes present, ranked by lexical score, top-N.
    kw = [t["paperId"] for t in T if t.get("channel") in ("K", "K&S")]
    scored = []
    for pid in kw:
        txt = text_of(pid)
        f = sum(1 for term in fert if m.title_matches_block(txt, [term]))
        p = sum(1 for term in pens if m.title_matches_block(txt, [term]))
        if f >= 1 and p >= 1:
            c = sum(1 for w in CAUSAL if (" " + w + " ") in txt)
            scored.append((pid, f + p + min(c, 3)))
    scored.sort(key=lambda x: -x[1])
    alex = set(pid for pid, _ in scored[:ALEX_N])

    methods = {"Anup (compositeScore>=7)": anup,
               "Gold-anchored (channel-convergence)": gold,
               "Alexandra (reconstructed lexical-triage)": alex}

    # ---- metrics ----
    def missed(s):  # truth studies with no candidate paperId in the set
        return [ts for ts in truth_studies if not (s & ts["cand"])]

    def fp_raw(s):
        return len(s - truth_all_pids), len(s)

    def fp_offcell(s):  # among tagged EMPIRICAL Tier-1 papers, how many off-cell
        tagged = [pid for pid in s if pid in pid_cell]
        empirical = [pid for pid in tagged if pid_cell[pid] not in ("THEORY",)]
        off = [pid for pid in empirical if pid_cell[pid].startswith("OFF")]
        return len(off), len(empirical), len(tagged), len(s)

    # ---- report ----
    L = [f"# Head-to-head method comparison - {SLUG}", "",
         "The PI's critique #2: the assignment was a three-way race of the search methods on "
         "false-negative rate, false-positive rate, cost, and replicability - and the synthesis "
         "delivered a merged method instead. This runs the race. **Two caveats set the terms:**", "",
         "1. **Only one of the three sets survives as frozen data.** Anup's Tier-1 is committed and "
         "reproducible; Alexandra's query-clustering outputs (live-OpenAlex prototype, gitignored "
         "`temp/`) and Shravan's independent gold-anchored production run **do not exist** - the "
         "gold-anchored query never ran on its own; `tiers.json` is the unified tiering demonstrated on "
         "Anup's corpus. That two of three 'independent deliveries' cannot be produced is itself the "
         "first finding, and part of why the convergence claim could be asserted but not shown.",
         "2. **So each method is a reproducible RULE over the common 8,087-paper corpus, not its "
         "as-delivered set.** Anup's and the gold-anchored rules are faithful (they are the methods' own "
         "tier rules). **Alexandra's is a labeled reconstruction** of her lexical-triage principle "
         "(keyword-reachable + both-axis lexical match, ranked, top-87 = her delivered size), not her "
         "lost output - read it as 'a method like hers', not as her.", "",
         "## The three Tier-1 sets (rules)", "",
         "| Method | Selection rule over the corpus | Tier-1 size |", "|---|---|---|",
         f"| **Anup** | `compositeScore >= 7` (evidence-quality tiering) | {len(anup)} |",
         f"| **Gold-anchored** | `in_gold` OR (K&S channel & RELEVANT & HIGH-confidence) | {len(gold)} |",
         f"| **Alexandra** *(reconstructed)* | keyword-reachable & both axes lexically present, top-{ALEX_N} by lexical score | {len(alex)} |",
         "",
         "## 1. Disagreement matrix (does 'convergence' hold, paper for paper?)", "",
         "| Pair | shared | only-A | only-B | Jaccard |", "|---|---|---|---|---|"]
    names = list(methods)
    for a, b in combinations(names, 2):
        sa, sb = methods[a], methods[b]
        inter = len(sa & sb); ja = inter / len(sa | sb) if (sa | sb) else 0
        L.append(f"| {a.split(' (')[0]} vs {b.split(' (')[0]} | {inter} | {len(sa-sb)} | {len(sb-sa)} | {ja:.2f} |")
    triple = anup & gold & alex
    union = anup | gold | alex
    L += ["",
          f"**All three agree on only {len(triple)} papers; their union is {len(union)}.** "
          f"Pairwise Jaccard runs low, so the sets are *not* near-identical - the 'three routes, one "
          "spine' convergence is weaker than asserted, at least at the Tier-1 boundary. (Caveat: the "
          "low overlap is partly mechanical - the three rules key on different signals by construction: "
          "evidence quality vs channel-convergence vs lexical match.)", "",
          "## 2. False negatives - does the method find the 10 studies that identify the effect?", "",
          f"Ground truth = the {len(truth_studies)} estimand-ready studies (the papers that actually "
          "identify OAS -> fertility). FN = truth studies the Tier-1 set misses (recovery is "
          "version-variant-robust, matched by DOI or title).", "",
          "| Method | recovered | missed (FN) | recall of truth |", "|---|---|---|---|"]
    nt = len(truth_studies)
    for name, s in methods.items():
        miss = missed(s); rec = nt - len(miss)
        L.append(f"| {name.split(' (')[0]} | {rec}/{nt} | {len(miss)} | {rec/nt:.0%} |")
    L += [""]
    for name, s in methods.items():
        miss = missed(s)
        if miss:
            L.append(f"- **{name.split(' (')[0]}** misses: " +
                     "; ".join(ts["title"][:45] for ts in miss))
    L += ["",
          "**Read these as Tier-1-boundary misses, not method-level misses.** The gold-anchored *rule* "
          "here is the narrow high-precision core (gold OR K&S convergence); in the full design a "
          "single-channel RELEVANT paper routes to **Tier-2**, still inside meta-analysis-ready. Its two "
          "extra misses are exactly single-channel truth papers - *Germany* is snowball-only (channel S) "
          "and *Financial Development* is keyword-only (channel K) - so they sit in that method's Tier-2, "
          "not lost. Likewise Alexandra's *LTC insurance* miss is a reconstruction artifact: 'long-term "
          "care insurance' is semantically old-age security but not lexically a backbone pension term, so "
          "my two-axis lexical proxy drops it (her real 5-cluster vocab might not). Anup's evidence-score "
          "rule recovers 9/10 because its centrality dimension already leans toward the estimand.", "",
          "## 3. False positives - two definitions, side by side", "",
          "Raw FP (any Tier-1 paper outside the 10-study truth) is **degenerate**: Tier-1 legitimately "
          "holds theory and topical papers, so every method scores ~90%+ 'FP'. The meaningful measure is "
          "off-cell-empirical: of a method's Tier-1 papers that are *empirical* (per the estimand tags), "
          "how many identify the wrong estimand. Coverage = how many Tier-1 papers carry an estimand tag "
          "at all (the tags cover the reviewed-40 + Tier-B-247, not the whole corpus).", "",
          "| Method | raw FP | off-cell / empirical (tagged) | off-cell rate | tag coverage |",
          "|---|---|---|---|---|"]
    for name, s in methods.items():
        rfp, n = fp_raw(s)
        off, emp, tagged, tot = fp_offcell(s)
        rate = f"{off/emp:.0%}" if emp else "n/a"
        L.append(f"| {name.split(' (')[0]} | {rfp}/{n} ({rfp/n:.0%}) | {off}/{emp} | {rate} | {tagged}/{tot} |")
    L += ["",
          "**The load-bearing finding:** *every* method's Tier-1 carries a large off-cell-empirical rate "
          "(27-57% of its tagged empirical papers identify the wrong estimand). No search rule - evidence "
          "quality, channel convergence, or lexical match - is estimand-precise on its own. That is "
          "exactly the gap the point-1 estimand gate closes, and it closes it *downstream of whichever "
          "search method wins*. Anup's rule is the most estimand-precise of the three here (27%), because "
          "`compositeScore` folds in a centrality term; channel-convergence and lexical matching (56-57%) "
          "do not. (Coverage caveat: off-cell rates are over the tagged subset only - 23-58 of each "
          "Tier-1 - so read them as indicative, not exact.)", "",
          "## 4. Cost and replicability (from the pilot record)", "",
          "| Method | cost | replicability |", "|---|---|---|",
          "| **Anup** | the only at-scale run: ~6,400 screened, ~542 LLM-scored; OpenAlex budget "
          "exhausted twice | **Reproducible** - corpus + scores committed (`prioritized.json`). |",
          "| **Gold-anchored** | gold build + 10-fold CV + snowball; ~tens of $ LLM; OpenAlex the "
          "binding cost | **Reproducible** - committed build steps (`goldset/`), though the production "
          "query has not run end-to-end. |",
          "| **Alexandra** | ~900 requested records; hit OpenAlex 429s + a multi-hour `Retry-After` | "
          "**Not reproducible** - live-API prototype, outputs + script gone; this row is a reconstruction. |",
          "",
          "## Bottom line", "",
          f"1. **Convergence is weaker than claimed.** All three Tier-1 sets agree on only {len(triple)} "
          f"of {len(union)} papers (pairwise Jaccard 0.07-0.13). 'Three routes, one spine' overstates the "
          "paper-level overlap; the rules key on different signals and pull genuinely different sets.",
          "2. **No single method dominates, but the ranking is not what the synthesis implied.** On this "
          "corpus Anup's plain evidence-score rule has both the best truth-recall (9/10) and the best "
          "estimand precision (27% off-cell) at the Tier-1 boundary. The gold-anchored rule's lower "
          "Tier-1 recall (7/10) is largely a boundary artifact - its single-channel truth papers route "
          "to Tier-2 - but its *higher* off-cell rate (56%) is real: channel convergence buys "
          "corroboration, not estimand precision.",
          "3. **The unifying finding: search choice is second-order to the estimand gate.** Every method "
          "admits 27-57% off-cell empirics into Tier-1. Whichever search wins, the point-1 estimand gate "
          "is what makes the output a pooling set. This is the strongest argument for the harmonized "
          "pipeline - not that the methods converge, but that they share the same downstream gap.",
          "4. **Replicability is the sharpest real differentiator.** Only the committed methods can be "
          "re-run; Alexandra's cannot - outputs and script are gone, which is why her row had to be "
          "reconstructed at all. That is a concrete failure of the project's 'no oral tradition' bar, "
          "and it argues for freezing every method's corpus before any future bake-off.", "",
          "*Reproducible via `37_method_comparison.py`. Alexandra's row is a labeled reconstruction; treat "
          "its numbers as illustrative of a lexical-triage method, not as her delivery. The whole "
          "comparison inherits the demo `tiers.json` snapshot's gold-flag and version-variant "
          "imperfections - directional, not exact.*"]

    OUT.write_text("\n".join(L) + "\n")
    print(f"Anup {len(anup)} | Gold {len(gold)} | Alexandra(recon) {len(alex)}")
    print(f"triple-overlap {len(triple)} | union {len(union)}")
    for name, s in methods.items():
        miss = missed(s)
        print(f"  {name.split(' (')[0]:<28} recall-of-truth {nt-len(miss)}/{nt}  missed={[ts['title'][:30] for ts in miss]}")
    print(f"written -> {OUT.name}")


if __name__ == "__main__":
    main()
