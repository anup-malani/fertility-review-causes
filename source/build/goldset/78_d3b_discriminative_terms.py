#!/usr/bin/env python3
"""
78_d3b_discriminative_terms.py - D.3.b (climate anxiety / eco-doomerism), stage A6a.

Direct mirror of B.1's `68_b1_discriminative_terms.py`. Only SLUG, the two block regexes, and the
reporting text differ; the Fightin' Words math is unchanged.

Rank candidate query terms by how strongly they separate the screen's RELEVANT set from its
NOT_RELEVANT near-miss negatives, using Monroe/Colaresi/Quinn "Fightin' Words": weighted log-odds
with an informative Dirichlet prior, z-scored so rare terms do not dominate. NOT raw tf-idf.

Text basis: TITLES only. The D.3.b frame carries abstracts in the batch payloads but not in the
screen-tiers output, and titles keep both sides on one footing and keep the CV recall estimate a
conservative lower bound.

Two blocks for the eventual 2-block conjunctive query (effect AND cause):
  EFFECT = fertility core PLUS the intention extension. Intention sits inside the constant effect
           axis by design (frozen decision 2 of the A1 scope: stated-intention outcomes are retained
           in the primary synthesis, flagged, and never pooled across outcome levels).
  CAUSE  = the five D.3.b cause families: the climate/eco-anxiety construct, habitability and
           future-for-children fear, carbon ethics and environmental antinatalism, eco-doom and
           pessimism, and reproductive decision-making.

LEAKAGE WALL (binding, from A3): the PLOS Climate systematic review is a channel-1 seed whose
INCLUDED STUDIES may feed anchors, but whose published SEARCH STRING must never feed query terms.
This script honours that wall structurally: every term is mined from our own screen verdicts over
our own citation frame. No term is copied from any published search string.

CAVEAT to state in the writeup: the negatives already passed the citation frame and the screen, so
the contrast is relevant-vs-NEAR-MISS (precision at fixed recall), not relevant-vs-random-database.
In A6b the same mining runs fold-locally so the CV recall estimate stays uncircular.

Inputs : output/{slug}-screen-tiers.json          (verdict per frame paper)
         literature/search-logs/{slug}-tier-a.json (the 10 empirical seeds, added to positives)
Output : literature/search-logs/{slug}-discriminative-terms.json + .md
"""
import json, re, math, sys
from pathlib import Path
from collections import Counter

SLUG = "climate-anxiety-eco-doomerism"
HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
LOGS = REPO / "literature" / "search-logs"
OUT = REPO / "output"
ALPHA0 = 1000.0
MIN_GOLD = 3

STOP = set("the a an of and in on for from to its by is with as at or be this that these those we our "
           "their his her it they i ii iii new evidence using based study studies analysis approach paper "
           "article effect effects impact role case among between within over under are was were has have "
           "had do does can could will would not no more less than into about across after before during "
           "toward towards via per vs versus also two three some how what why when where which who whom "
           "data model models results result human humans".split())

# Fertility core plus the intention extension. Intention is IN the effect axis by design.
EFFECT = re.compile(r"fertil|childbear|childless|childfree|child-free|birth rate|birthrate|natalit|"
                    r"offspring|reproducti|number of children|family size|parity|procreat|babi|"
                    r"have children|having children|child rearing|childrearing|"
                    r"intention|intent to|desire for a child|family planning intention|"
                    r"remain childless|voluntary childless")

# The five cause families from the A2 query-cluster file.
#
# NOTE: bare unigrams are listed explicitly alongside the phrases. A first run filed the strongest
# cause-side signals ("climate", "anxiety", "eco", "worries", "emotions") under OTHER, because the
# phrase patterns below only matched their bigrams. That would have starved the cause block in A6b,
# where the two-block query is assembled from these labels.
CAUSE = re.compile(
    # 0. bare cause-side unigrams (affect vocabulary + the exposure spine)
    r"\bclimate\b|\beco\b|anxiet|anxious|worri|\bworry\b|concern|emotion|feeling|"
    r"\bfear|afraid|distress|grief|guilt|hope\b|hopeless|"
    # 1. climate / eco-anxiety construct (exposure spine)
    r"climate anxiet|eco-anxiet|eco anxiet|climate worr|climate concern|climate distress|"
    r"climate emotion|climate grief|solastalgia|environmental concern|environmental worr|"
    # 2. habitability / future-for-children fear
    r"habitab|planetary|future for children|bring a child|uncertain future|climate future|"
    r"world to bring|liveab|livab|"
    # 3. carbon ethics / environmental antinatalism
    r"carbon|footprint|emission|antinatal|anti-natal|overpopulat|population ethic|"
    r"procreat\w* ethic|environmental ethic|moral|ethic|"
    # 4. eco-doom / pessimism
    r"doom|apocalyp|collapse|catastroph|existential|pessimis|dread|despair|extinction|"
    r"end of the world|crisis|"
    # 5. reproductive decision-making / motivation (carries the D.1.a wall)
    r"reproductive decision|childbearing decision|decision-making|decision making|motivation|"
    r"attitude|willingness|"
    # exposure spine, broad
    r"climate change|global warming|environment|ecolog|sustainab|green ")


def toks(t):
    return [w for w in re.sub(r"[^a-z0-9\s]", " ", (t or "").lower()).split() if len(w) > 2 and w not in STOP]


def terms(title):
    u = toks(title)
    return u + [f"{u[i]} {u[i+1]}" for i in range(len(u) - 1)]


def block_of(term):
    e, c = bool(EFFECT.search(term)), bool(CAUSE.search(term))
    return "effect" if (e and not c) else "cause" if (c and not e) else "both" if (e and c) else "other"


def corpus_terms(titles):
    c = Counter()
    for t in titles:
        c.update(terms(t))
    return c


def main():
    rows_screen = json.load(open(OUT / f"{SLUG}-screen-tiers.json"))
    seeds = json.load(open(LOGS / f"{SLUG}-tier-a.json"))
    pos_titles = [r["title"] for r in rows_screen if r["verdict"] == "RELEVANT" and r.get("title")]
    pos_titles += [s["title"] for s in seeds if s.get("title")]  # Tier-A seeds are positives too
    neg_titles = [r["title"] for r in rows_screen if r["verdict"] == "NOT_RELEVANT" and r.get("title")]
    print(f"positives: {len(pos_titles)} | negatives: {len(neg_titles)}", file=sys.stderr)

    gc, nc = corpus_terms(pos_titles), corpus_terms(neg_titles)
    vocab = set(gc) | set(nc)
    ng, nn = sum(gc.values()), sum(nc.values())
    comb = {w: gc[w] + nc[w] for w in vocab}
    ncomb = ng + nn
    rows = []
    for w in vocab:
        if gc[w] < MIN_GOLD:
            continue
        aw = ALPHA0 * comb[w] / ncomb
        l_g = math.log((gc[w] + aw) / (ng + ALPHA0 - gc[w] - aw))
        l_n = math.log((nc[w] + aw) / (nn + ALPHA0 - nc[w] - aw))
        delta = l_g - l_n
        z = delta / math.sqrt(1.0 / (gc[w] + aw) + 1.0 / (nc[w] + aw))
        rows.append({"term": w, "block": block_of(w), "z": round(z, 2), "log_odds": round(delta, 2),
                     "gold": gc[w], "neg": nc[w], "is_bigram": " " in w})
    rows.sort(key=lambda r: -r["z"])
    json.dump(rows, open(LOGS / f"{SLUG}-discriminative-terms.json", "w"), indent=2)

    def top(block, k=25):
        return [r for r in rows if r["block"] == block][:k]

    L = [f"# Discriminative terms (A6a) - {SLUG}", "",
         "Fightin'-Words weighted log-odds (informative Dirichlet prior, z-scored) over TITLES: "
         f"RELEVANT+seeds ({len(pos_titles)}) vs screen NOT_RELEVANT ({len(neg_titles)}). Higher z = more "
         "discriminative of the on-topic class. Negatives passed the citation-frame + screen, so the "
         "contrast is relevant-vs-near-miss (precision at recall). In A6b this is recomputed fold-locally "
         "for the CV.", "",
         "**Leakage wall honoured:** every term below is mined from our own screen verdicts over our own "
         "citation frame. No term is taken from the PLOS Climate review's published search string.", "",
         f"Candidate terms (gold count >= {MIN_GOLD}): **{len(rows)}**. "
         "By block: " + ", ".join(f"{b} {sum(1 for r in rows if r['block']==b)}"
                                   for b in ("effect", "cause", "both", "other")), ""]
    for b, lbl in [("effect", "EFFECT block (fertility core + intention extension)"),
                   ("cause", "CAUSE block (anxiety construct / habitability fear / carbon ethics / "
                             "eco-doom / reproductive decision)"),
                   ("both", "BOTH-block (effect x cause bigrams)"),
                   ("other", "OTHER (context terms)")]:
        L += [f"\n## {lbl} - top by z\n", "| term | z | log-odds | gold | neg |", "|---|---|---|---|---|"]
        for r in top(b, 25):
            L.append(f"| {r['term']} | {r['z']} | {r['log_odds']} | {r['gold']} | {r['neg']} |")
    (LOGS / f"{SLUG}-discriminative-terms.md").write_text("\n".join(L) + "\n")

    print(f"candidate terms: {len(rows)} | by block: {dict(Counter(r['block'] for r in rows))}", file=sys.stderr)
    print("TOP 24 overall (z):", file=sys.stderr)
    for r in rows[:24]:
        print(f"  {r['z']:6.1f} [{r['block']:6}] {r['term']}  (g{r['gold']}/n{r['neg']})", file=sys.stderr)


if __name__ == "__main__":
    main()
