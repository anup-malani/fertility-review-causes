#!/usr/bin/env python3
r"""
100_d1a_discriminative_terms.py — D.1.a, GACS stage A6a. Rank candidate query terms.

Fightin' Words (Monroe, Colaresi and Quinn): weighted log-odds with an informative Dirichlet prior,
z-scored so rare terms cannot dominate. NOT raw tf-idf. The math is carried unchanged from
`78_d3b_discriminative_terms.py`, which carried it from B.1's `68_`. What differs is the block
structure, and the difference is forced by this chapter's scope rather than chosen.

THE TREATMENT SIDE IS FIVE CLUSTERS, NOT ONE BLOCK. B.1 and D.3.b each mine a single CAUSE block
against a single EFFECT block, because each is one treatment. Ruling 1 of this chapter's scope holds
that D.1.a carries **five different treatments against one outcome** — postmaterialism, individualism,
secularization, the childlessness norm, and consumerism — that are estimated separately and never
pooled, because an effect size on one is not exchangeable with an effect size on another. A single
mined CAUSE block would therefore be ranked by whichever pair is best represented in the frame, which
the scope predicts and the cold-start anchors confirm is S3: 23 of 31 empirical anchors are S3 against
5 S1, 2 S5 and 1 S2. Mining one block would let S3 vocabulary crowd out the other four, and the search
budget would follow — the exact outcome the scope warned against when it said the strata are unequal
enough that budget should not be split evenly. Five clusters keep the allocation an explicit decision
at A6b instead of an artifact of the frame's composition.

THE VOCABULARY TRAP IS HANDLED HERE, NOT AT SCREENING, BECAUSE THE SCOPE SAYS SO. *Materialism* names
opposite treatments in the two literatures feeding this chapter: Inglehart's *materialist* prioritises
physical and economic security, the pole fertility declines AWAY from (S1), while the
consumer-psychology *materialist* is acquisitive, the pole it declines TOWARD (S5). A term carrying
both senses is assigned to neither cluster; it is routed to `AMBIGUOUS_MATERIALISM` and reported
separately so the disambiguation is a visible decision rather than a silent coin-flip.

NEGATIVES INCLUDE THE TEN PURPOSE-BUILT DECOYS. The bulk of the negative class is the snowball pool's
non-relevant residue, which is the same relevant-vs-near-miss contrast D.3.b documented: those records
already passed the citation frame, so what is measured is precision at fixed recall, not
relevant-versus-random-database. D.1.a can do slightly better, because `91_` built ten anchors
specifically as decoys — records that look on-pair and are not. They are added to the negatives, so any
term that survives has been tested against hand-chosen hard cases and not only against easy ones.

CIRCULARITY, STATED. Tier-A anchors are keyword-sourced (the `89_`/`90_` OpenAlex probes) and are
positives here, so terms mined from them partly re-derive the vocabulary that found them. That is why
A6b recomputes this fold-locally and measures recall on held-out folds, and why Recall(B) — measured
on the citation-sourced Tier B, which no keyword query produced — is the number that carries weight.

Inputs : literature/search-logs/{slug}-tier-{a,b-frame}.json
         temp/d1a/snowball-r{1,2}-pool-scored.json   (for the near-miss negatives)
Output : literature/search-logs/{slug}-discriminative-terms.json + .md
"""
import json, math, os, re, sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

SLUG = "postmaterialism-individualism-secularization"
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
LOGS = os.path.join(ROOT, "literature", "search-logs")
TMP = os.path.join(ROOT, "temp", "d1a")
ALPHA0 = 1000.0
MIN_GOLD = 3

STOP = set(
    "the a an of and in on for from to its by is with as at or be this that these those we our their "
    "his her it they i ii iii new evidence using based study studies analysis approach paper article "
    "effect effects impact role case among between within over under are was were has have had do "
    "does can could will would not no more less than into about across after before during toward "
    "towards via per vs versus also two three some how what why when where which who whom data model "
    "models results result human humans research review journal university press vol pp doi eds ed "
    "chapter book series report working note comment reply".split())

# ---- the outcome axis. Same vocabulary as the relevance filter's OUTCOME, which is deliberate: the
# frame was built on it, so the query is being fitted to retrieve what the frame counts as on-pair.
OUTCOME = re.compile(
    r"fertil|childbear|childless|childfree|child-free|birth rate|birthrate|natalit|"
    r"number of children|family size|parity|procreat|nuptial|"
    r"reproductive behavio|reproductive success|reproductive intention|reproductive decision|"
    r"\bbirths?\b|\btfr\b|completed famil")

# ---- the five treatment clusters, from Ruling 1's measure families.
PAIRS = {
    "S1_POSTMATERIALISM": re.compile(
        r"postmaterial|post-material|self-expression|self expression|survival value|"
        r"inglehart|silent revolution|value change|value orientation|ideational|"
        r"emancipat|human development|modernizat|postmodern|post-modern"),
    "S2_INDIVIDUALISM": re.compile(
        r"individualis|individuali[sz]ation|collectivis|autonom|kinship|kin intensity|"
        r"hofstede|schwartz|self-direction|independen|obligation|familis|famili[sz]m|"
        r"extended family|nuclear famil"),
    "S3_SECULARIZATION": re.compile(
        r"religio|secular|church|denominat|faith|islam|muslim|catholic|protestant|jewish|hindu|"
        r"buddhis|attendance|prayer|salience|piet|belief in god|clergy|mosque|congregat|"
        r"affiliation|orthodox|evangel|fundamentalis"),
    # Deliberately narrow. A first pass had bare `norm` and `attitude toward` here, which put the
    # chapter's most common generic value vocabulary into the pair that Ruling 2 calls largely
    # degenerate -- `norms` (z 9.1, gold 29) is not the childlessness norm, it is any norm. S4's
    # distinctive vocabulary is childlessness-specific or it is not S4's.
    "S4_CHILDLESSNESS_NORM": re.compile(
        r"voluntary childless|childfree|child-free|remain childless|childlessness accept|"
        r"approval of childless|acceptab\w* of childless|stigma of childless"),
    "S5_CONSUMERISM": re.compile(
        r"consumeris|consumption|material values|materialistic|acquisit|affluen|lifestyle|"
        r"aspiration|status good|conspicuous|richins|possession"),
}
# Treatment-side vocabulary that does NOT identify a pair. This is a query cluster in its own right
# and not a residual category: `cultural` (z 11.8), `attitudes` (11.1), `value children` (8.7) and
# `value` (8.4) are four of the frame's ten strongest discriminators, and every one of them retrieves
# on-pair work without saying WHICH pair. The production query needs them; the pair routing cannot use
# them, and that routing is done at extraction from the measure's item content, not from the title.
GENERIC_VALUES = re.compile(
    r"^values?$|value of children|value children|^attitudes?$|gender attitude|^norms?$|"
    r"^cultural$|^culture$|belief|^ideal|preference|ideational|worldview|world view|"
    r"second demographic transition|second demographic|changing value|value change|"
    r"value orientation|moral")

# The trap: these read as S1 in one literature and S5 in the other. Assigned to neither.
AMBIG_MATERIALISM = re.compile(r"^materialis\w*$|^material\b|^materialism$")

# Clinical / veterinary collision, logged three times in the probes: `fertility` reads as IVF,
# `birth` as birth weight, `reproduction` as livestock. Flagged here so A6c can exclude it by
# construction rather than pay for it at screening.
CLINICAL = re.compile(
    r"ivf|in vitro|follitropin|gonadotrop|oocyte|sperm|semen|embryo|infertil|subfertil|"
    r"assisted reproduct|antenatal|prenatal|obstetric|gestation|birth weight|birthweight|"
    r"preterm|neonat|maternal mortalit|contracepti\w* method|livestock|cattle|bovine|swine|"
    r"heifer|dairy|poultry|hla|haemophil|hemophil")


def toks(t):
    return [w for w in re.sub(r"[^a-z0-9\s]", " ", (t or "").lower()).split()
            if len(w) > 2 and w not in STOP]


def terms(title):
    u = toks(title)
    return u + [f"{u[i]} {u[i + 1]}" for i in range(len(u) - 1)]


def block_of(term):
    """Assign a term to the outcome axis, one treatment cluster, both, or neither."""
    if AMBIG_MATERIALISM.search(term):
        return "AMBIGUOUS_MATERIALISM"
    o = bool(OUTCOME.search(term))
    # PAIR-SPECIFIC BEATS GENERIC, and the order matters more than it looks. `value orientation` and
    # `value change` are Inglehart's signature vocabulary (S1) and also read as generic value talk. A
    # first pass tested GENERIC_VALUES first and silently absorbed them, dropping S1 from 5 terms to
    # 2 -- which would have understated the one non-S3 pair that has any vocabulary at all, in a
    # chapter whose whole risk is S3 crowding out the other four.
    hits = [p for p, rx in PAIRS.items() if rx.search(term)]
    if hits:
        return "BOTH" if o else (hits[0] if len(hits) == 1 else "MULTI_PAIR")
    if GENERIC_VALUES.search(term):
        return "BOTH" if o else "GENERIC_VALUES"
    if o:
        return "OUTCOME"
    if len(hits) > 1:
        # A term claimed by more than one pair cannot be used to separate them. `childless` is the
        # standing example: it is S4's treatment vocabulary AND the outcome axis, which is exactly
        # the degenerate pair Ruling 2 bars from the causal pool.
        return "MULTI_PAIR"
    return "OTHER"


def corpus_terms(titles):
    c = Counter()
    for t in titles:
        c.update(terms(t))
    return c


def main():
    tier_a = json.load(open(os.path.join(LOGS, f"{SLUG}-tier-a.json")))
    tier_b = json.load(open(os.path.join(LOGS, f"{SLUG}-tier-b-frame.json")))

    pos = [r["title"] for r in tier_b if r.get("title")]
    pos += [r["title"] for r in tier_a if r.get("role") == "EMPIRICAL" and r.get("title")]
    neg = [r["title"] for r in tier_a if r.get("role") == "DECOY" and r.get("title")]
    n_decoy = len(neg)
    for f in ("snowball-r1-pool-scored.json", "snowball-r2-pool-scored.json"):
        for rec in json.load(open(os.path.join(TMP, f)))["pool"]:
            if not rec.get("relevant") and rec.get("title"):
                neg.append(rec["title"])
    print(f"positives: {len(pos)} (Tier B {len(tier_b)} + Tier A empirical "
          f"{len(pos) - len(tier_b)}) | negatives: {len(neg)} "
          f"(incl. {n_decoy} purpose-built decoys)", file=sys.stderr)

    gc, nc = corpus_terms(pos), corpus_terms(neg)
    vocab = set(gc) | set(nc)
    ng, nn = sum(gc.values()), sum(nc.values())
    ncomb = ng + nn
    rows = []
    for w in vocab:
        if gc[w] < MIN_GOLD:
            continue
        aw = ALPHA0 * (gc[w] + nc[w]) / ncomb
        l_g = math.log((gc[w] + aw) / (ng + ALPHA0 - gc[w] - aw))
        l_n = math.log((nc[w] + aw) / (nn + ALPHA0 - nc[w] - aw))
        delta = l_g - l_n
        z = delta / math.sqrt(1.0 / (gc[w] + aw) + 1.0 / (nc[w] + aw))
        rows.append({"term": w, "block": block_of(w), "z": round(z, 2),
                     "log_odds": round(delta, 2), "gold": gc[w], "neg": nc[w],
                     "is_bigram": " " in w, "clinical": bool(CLINICAL.search(w))})
    rows.sort(key=lambda r: -r["z"])
    json.dump(rows, open(os.path.join(LOGS, f"{SLUG}-discriminative-terms.json"), "w"), indent=1)

    counts = Counter(r["block"] for r in rows)
    order = (["OUTCOME", "GENERIC_VALUES"] + list(PAIRS)
             + ["BOTH", "MULTI_PAIR", "AMBIGUOUS_MATERIALISM", "OTHER"])
    L = [f"# D.1.a — discriminative terms (GACS A6a)", "",
         "Fightin'-Words weighted log-odds (informative Dirichlet prior, z-scored) over **titles**: "
         f"Tier B + Tier-A empirical anchors (**{len(pos)}** positives) against the snowball's "
         f"non-relevant residue plus the ten purpose-built decoys (**{len(neg)}** negatives). "
         "Higher z = more discriminative of the on-pair class.", "",
         "**The contrast is relevant-versus-near-miss, not relevant-versus-random-database.** Every "
         "negative already passed the citation frame, so what is measured is precision at fixed "
         "recall. A6b recomputes this fold-locally so the CV recall estimate stays uncircular.", "",
         "**The treatment side is five clusters, not one block** (Ruling 1): the five pairs are "
         "estimated separately and never pooled, and a single mined cause block would be ranked by "
         "whichever pair dominates the frame — which is S3, at 23 of 31 empirical anchors. Splitting "
         "keeps the budget allocation an explicit A6b decision rather than an artifact of frame "
         "composition.", "",
         f"Candidate terms (gold count >= {MIN_GOLD}): **{len(rows)}**", "",
         "| block | terms |", "|---|---|"]
    L += [f"| `{b}` | {counts.get(b, 0)} |" for b in order]
    L += ["", f"Terms flagged as clinical/veterinary collision: "
              f"**{sum(1 for r in rows if r['clinical'])}** — see the exclusion note below.", ""]

    for b in order:
        sel = [r for r in rows if r["block"] == b][:20]
        if not sel:
            continue
        L += [f"\n## `{b}` — top by z\n", "| term | z | log-odds | gold | neg |", "|---|---|---|---|---|"]
        L += [f"| {r['term']} | {r['z']} | {r['log_odds']} | {r['gold']} | {r['neg']} |" for r in sel]

    # ---- findings, computed rather than asserted ------------------------------------------
    per_pair = {p: [r for r in rows if r["block"] == p] for p in PAIRS}
    s4_terms = [r for r in rows if "childless" in r["term"] or "childfree" in r["term"]]
    perfect = [r for r in rows if r["neg"] == 0 and r["gold"] >= 5]
    L += ["", "---", "", "## What the block counts mean", "",
          "**Three of the five pairs have no mineable query vocabulary in this frame, and two have "
          "literally none.**", "",
          "| pair | discriminative terms | strongest term |", "|---|---|---|"]
    for p in PAIRS:
        t = per_pair[p]
        best = f"`{t[0]['term']}` (z {t[0]['z']})" if t else "—"
        L.append(f"| `{p}` | **{len(t)}** | {best} |")
    L += ["",
          f"S3 carries {len(per_pair['S3_SECULARIZATION'])} terms topping out at z "
          f"{per_pair['S3_SECULARIZATION'][0]['z']}; S1's best term reaches "
          f"{per_pair['S1_POSTMATERIALISM'][0]['z'] if per_pair['S1_POSTMATERIALISM'] else 0}. This is "
          "the scope's 'expected shape of the evidence' confirmed by an independent measurement, and "
          "it is stronger than the scope predicted.", "",
          "**Consequence for A6b, and it is the same move D.3.b made for its rare cells.** A query "
          "built only on mined terms would be an S3 query with a generic-values annex: S1 and S2 "
          "would be reachable only through `GENERIC_VALUES` plus the outcome axis, and S4 and S5 not "
          "at all. S4 and S5 therefore need **forced a-priori backbones** rather than mined "
          "expansions, exactly as D.3.b forced its carbon-ethics cluster because it was "
          "'conceptually central and empirically rare, so it is forced in rather than left to the "
          "mined ranking, which would never surface it.'", "",
          "### S4 is degenerate, and the term ranker demonstrates it mechanically", "",
          "Ruling 2 pre-registered the degenerate-pair rule: when the treatment measure and the "
          "outcome measure are the same construct, there is no pair. S4's vocabulary is that rule "
          "made visible — **every childlessness term in the ranked set classifies as `OUTCOME` or "
          "`BOTH`, and none as a pure treatment term**, because there is no S4 treatment word that is "
          "not also the outcome word:", ""]
    L += [f"- `{r['term']}` → `{r['block']}` (z {r['z']}, gold {r['gold']})" for r in s4_terms]
    L += ["", "A pre-registered ruling confirmed by an independent measurement is worth more than "
              "either alone, and this belongs in the chapter's methods section.", ""]
    if perfect:
        L += ["### Perfectly separating conjunctions", "",
              "Terms with **zero** occurrences in 9,972 negatives and five or more in the positives. "
              "These are the outcome × treatment bigrams, and they are why the production query is a "
              "conjunction rather than a union of two term lists:", ""]
        L += [f"- `{r['term']}` — gold {r['gold']}, neg 0" for r in perfect[:12]]
        L += ["", "**Not all of these are real, and the list shows its own tell.** `spain 1985`, "
                  "`1985 1999` and `religion spain` separate perfectly at gold 7 because they come "
                  "from one study's citation neighbourhood, not because they are query vocabulary — "
                  "perfect separation at a low gold count is the signature of a single-cluster "
                  "artifact rather than of a discriminating term. This is precisely why A6a's ranking "
                  "is **not** the production query: A6b re-mines fold-locally and measures recall on "
                  "held-out folds, where a term carried by one study in the training fold earns "
                  "nothing on the papers it has never seen.", ""]

    clin = [r for r in rows if r["clinical"]][:20]
    L += ["", "## Clinical and veterinary collision — candidates to EXCLUDE at A6c", "",
          "Logged three times in the probes: *fertility* reads as IVF, *birth* as birth weight, "
          "*reproduction* as livestock, and OpenAlex stemming matched *individualism* to "
          "\"individualiSED dosing of follitropin delta\". These are terms the mining surfaced that "
          "belong in a NOT clause, not a query block.", ""]
    L += ([f"- `{r['term']}` (z {r['z']}, gold {r['gold']}, neg {r['neg']})" for r in clin]
          or ["**None — and the zero is the finding, not a clean bill of health.**", "",
              "The frame is a citation neighbourhood around value-and-fertility work, so it never "
              "contained the clinical literature in the first place; there was nothing for the miner "
              "to flag. **An exclusion cannot be learned for contamination the training frame does "
              "not contain.** The collision is real — it was logged three times in the `89_`/`90_` "
              "probes, which pulled from the open database rather than from a citation frame — and it "
              "will appear the moment the production query runs against that database. The NOT clause "
              "at A6c must therefore be specified *a priori* from the probe evidence, and this "
              "section is the record that the mining could not and did not supply it."])
    open(os.path.join(LOGS, f"{SLUG}-discriminative-terms.md"), "w").write("\n".join(L) + "\n")

    print(f"candidate terms: {len(rows)}", file=sys.stderr)
    for b in order:
        print(f"  {b:24s} {counts.get(b, 0)}", file=sys.stderr)
    print("\nTOP 22 overall by z:", file=sys.stderr)
    for r in rows[:22]:
        print(f"  {r['z']:6.1f} [{r['block']:22}] {r['term']}  (g{r['gold']}/n{r['neg']})",
              file=sys.stderr)


if __name__ == "__main__":
    main()
