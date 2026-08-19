#!/usr/bin/env python3
r"""
151_d3c_discriminative_terms.py — D.3.c, stage A4. Rank candidate query terms.

Fightin' Words (Monroe, Colaresi and Quinn): weighted log-odds with an informative Dirichlet prior,
z-scored so rare terms cannot dominate. NOT raw tf-idf. The math is carried unchanged from
`100_d1a_discriminative_terms.py`, which carried it from D.3.b's `78_` and B.1's `68_`. What differs
is the LABEL, and the difference is forced by this chapter rather than chosen.

THE LABEL IS CITATION PROVENANCE, NOT VOCABULARY. Every earlier chapter could take its positive class
from records that look relevant. D.3.c cannot, and the reason is the chapter's central finding: the
primary cell is defined by a despair construct co-occurring with a fertility quantity, so labelling
positives by that co-occurrence and then mining the vocabulary that separates them would rediscover
the words used to draw the line. The frame gives a label that owes nothing to any word in it:

    POSITIVE = a Tier B record reached by at least one PRIMARY-cell anchor's citation neighbourhood
    NEGATIVE = a Tier B record reached only by anchors that sit ACROSS a boundary wall

Nothing in that partition reads the record's text, so the terms it yields are an honest answer to the
question the walls actually pose: **is there vocabulary that separates the primary anchors'
neighbourhood from the decoys' neighbourhood at all?**

THAT QUESTION HAS A CONSEQUENCE EITHER WAY, WHICH IS WHY IT IS WORTH ASKING THIS WAY. The scope
declares Wall 1 (D.3.c vs C.5.a) unenforceable at title and abstract, on the reasoning that
chronic-versus-transitory and mechanism-measured-or-asserted both live in the design rather than the
summary. That was an argument. This is a measurement of the same claim: if the strongest
discriminators between the two neighbourhoods are weak, or are topic words rather than mechanism
words, the declaration is confirmed by evidence and the screen's over-inclusive design is justified
rather than merely asserted. If strong mechanism discriminators DO appear, the scope is wrong and
Wall 1 should be attempted at screening after all. Either way the scope stops resting on judgement.

NEGATIVES ARE NEAR-MISSES BY CONSTRUCTION, not a random database sample. Every negative already
passed the citation frame — it is cited by, or cites, an anchor chosen to sit one wall away. So what
is measured is precision at fixed recall, the same contrast D.3.b and D.1.a documented, and the z
scores are not comparable to a relevant-versus-random-corpus ranking.

MINED ON TITLE **AND ABSTRACT**, unlike D.1.a's title-only pass. This chapter's discriminator is a
mechanism construct, and a despair measure is named in an abstract far more often than in a title —
mining titles alone would measure which literature writes its mechanism into its title, which is a
fact about house style. The share of frame records carrying an abstract is measured and reported in the output, not
asserted here.

CIRCULARITY, STATED. The Tier A anchors were sourced partly through keyword probes at A3, so terms
mined from their neighbourhoods partly re-derive the vocabulary that found them. That is why B1
recomputes fold-locally and measures recall on held-out folds, and why Recall(B) — measured on the
citation-sourced Tier B, which no keyword query produced — is the number that carries weight.

Inputs : literature/search-logs/{slug}-tier-{a,b-frame}.json
Output : literature/search-logs/{slug}-discriminative-terms.json + .md
"""
import json, math, os, re, sys
from collections import Counter

SLUG = "despair-hopelessness-fertility"
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
LOGS = os.path.join(ROOT, "literature", "search-logs")
ALPHA0 = 1000.0
MIN_GOLD = 4

# Cells whose citation neighbourhood defines the POSITIVE class. PRIMARY_ACCELERATION is here for the
# same reason it is in the recall denominator: under the Call 1 ruling it is chapter 2's primary cell,
# not chapter 1's opposite sign. Excluding it would mine a vocabulary that finds only
# despair-lowers-fertility work — the cherry-pick Wall 6 exists to prevent — and would do it
# invisibly, inside the query, where no later stage could see it.
PRIMARY_CELLS = {"PRIMARY_MEASURED_DESPAIR", "PRIMARY_DECLINE_WITH_MECHANISM",
                 "PRIMARY_ACCELERATION"}

STOP = set(
    "the a an of and in on for from to its by is with as at or be this that these those we our their "
    "his her it they i ii iii new evidence using based study studies analysis approach paper article "
    "effect effects impact role case among between within over under are was were has have had do "
    "does can could will would not no more less than into about across after before during toward "
    "towards via per vs versus also two three some how what why when where which who whom data model "
    "models results result human humans research review journal university press vol pp doi eds ed "
    "chapter book series report working note comment reply been being had were will may might one "
    "first second third such other others both each many much most least well however therefore "
    "thus while although though because since given find finds found show shows shown suggest "
    "suggests use used uses associated association significant significantly higher lower increase "
    "increased decrease decreased change changes level levels rate rates high low large small "
    "years year age aged time times group groups sample samples population populations country "
    "countries national state states area areas".split())

# ---- the four axes this chapter routes on. Same vocabularies as the A4 frame diagnostics, on
# purpose: the frame was built and measured on them, so the query is being fitted to retrieve what
# the frame counts as on-cell, and a term's block here means the same thing it meant there.
MECHANISM = re.compile(
    r"despair|hopeless|demorali[sz]|anomie|fatalis|normless|alienat|"
    r"future orientation|foreshortened|expectations about|pessimis|optimis|"
    r"bleak|left behind|meaningless|subjective wellbeing|subjective well-being|"
    r"life satisfaction|deaths of despair|discourag")
OUTCOME = re.compile(
    r"fertil|childbear|childless|childfree|child-free|birth rate|birthrate|natalit|"
    r"number of children|family size|parity|nuptial|\bbirths?\b|\btfr\b|completed famil|"
    r"teen birth|nonmarital|non-marital|out-of-wedlock|reproductive intention")
TREATMENT = re.compile(
    r"deindustriali|economic decline|distressed|plant closure|mass layoff|job loss|"
    r"displaced worker|import competition|china shock|trade shock|rust belt|"
    r"manufactur|unemploy|labor market|labour market|recession|precari|insecur|uncertain|"
    r"downward mobilit|inequalit|disadvantag|deprivation|poverty")
MORTALITY = re.compile(
    r"mortalit|suicide|overdose|drug poisoning|life expectancy|alcoholic liver|cirrhosis|"
    r"premature death|excess death|cause of death|years of life lost|opioid|addiction")
# Wall 5. Infertility-distress vocabulary is the standing threat: it owns the validated hopelessness
# instruments, so it will surface as "mechanism + outcome" and look like the primary cell.
REVERSE = re.compile(
    r"infertil|subfertil|ivf|in vitro|assisted reproduct|art treatment|involuntary childless|"
    r"fertility treatment|fertility patient|oocyte|embryo|stigma of infertil")


def toks(t):
    # Numeric and mostly-numeric tokens are dropped. They are not query terms: the first run ranked
    # the bare token `233` eighth overall (z 20.6, 115 positive occurrences), which is a fragment of
    # volume/page/identifier text that survived into abstracts. A term list is fed to a production
    # query, so a token that cannot be searched for is worse than useless — it looks like a finding.
    out = []
    for w in re.sub(r"[^a-z0-9\s]", " ", (t or "").lower()).split():
        if len(w) <= 2 or w in STOP:
            continue
        if sum(c.isdigit() for c in w) * 2 >= len(w):
            continue
        out.append(w)
    return out


def terms(text):
    u = toks(text)
    return u + [f"{u[i]} {u[i + 1]}" for i in range(len(u) - 1)]


def block_of(term):
    """Assign a term to an axis. Order matters and is argued, not incidental."""
    # REVERSE first. Its vocabulary overlaps both MECHANISM and OUTCOME by construction — that is
    # exactly what makes Wall 5 dangerous — so testing it later would let `hopelessness infertility`
    # be filed as a mechanism term and enter the query as if it retrieved the primary cell.
    if REVERSE.search(term):
        return "REVERSE_WALL5"
    if MORTALITY.search(term):
        return "MORTALITY_WALL4"
    m, o, t = bool(MECHANISM.search(term)), bool(OUTCOME.search(term)), bool(TREATMENT.search(term))
    if m and o:
        return "MECHANISM_AND_OUTCOME"      # the primary cell's own vocabulary
    if m:
        return "MECHANISM"
    if o and t:
        return "TREATMENT_AND_OUTCOME"      # the reduced-form body: C.5.a has equal claim
    if o:
        return "OUTCOME"
    if t:
        return "TREATMENT"
    return "OTHER"


def corpus_terms(docs):
    c = Counter()
    for d in docs:
        c.update(terms(d))
    return c


def main():
    tier_a = json.load(open(os.path.join(LOGS, f"{SLUG}-tier-a.json")))
    tier_b = json.load(open(os.path.join(LOGS, f"{SLUG}-tier-b-frame.json")))

    primary_seeds = {a.get("openalex_id") for a in tier_a
                     if a.get("provisional_cell") in PRIMARY_CELLS and a.get("openalex_id")}
    if not primary_seeds:
        sys.exit("ABORT: no primary-cell seed ids; the label would be empty.")

    def doc(r):
        return (r.get("title") or "") + " " + (r.get("abstract") or "")

    pos = [doc(r) for r in tier_b if set(r.get("seed_ids") or []) & primary_seeds]
    neg = [doc(r) for r in tier_b if not (set(r.get("seed_ids") or []) & primary_seeds)]
    n_abs = sum(1 for r in tier_b if r.get("abstract"))
    print(f"primary seeds: {len(primary_seeds)} | positives: {len(pos)} | negatives: {len(neg)} "
          f"| abstracts: {n_abs}/{len(tier_b)} ({n_abs / max(len(tier_b), 1):.0%})", file=sys.stderr)

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
                     "is_bigram": " " in w})
    rows.sort(key=lambda r: -r["z"])
    json.dump(rows, open(os.path.join(LOGS, f"{SLUG}-discriminative-terms.json"), "w"), indent=1)

    counts = Counter(r["block"] for r in rows)
    order = ["MECHANISM_AND_OUTCOME", "MECHANISM", "OUTCOME", "TREATMENT_AND_OUTCOME", "TREATMENT",
             "REVERSE_WALL5", "MORTALITY_WALL4", "OTHER"]
    top = rows[:40]
    mech_in_top = [r for r in top if r["block"] in ("MECHANISM", "MECHANISM_AND_OUTCOME")]

    L = [f"# D.3.c — discriminative terms (A4)", "",
         "Fightin'-Words weighted log-odds (informative Dirichlet prior, z-scored) over **title and "
         f"abstract**: **{len(pos):,}** positives against **{len(neg):,}** negatives. Higher z = more "
         "discriminative of the primary-anchor neighbourhood.", "",
         "**The label is citation provenance, not vocabulary.** A positive is a Tier B record reached "
         "by at least one PRIMARY-cell anchor; a negative is reached only by anchors sitting across a "
         "boundary wall. Nothing in that partition reads the record's text. Labelling by the "
         "despair-and-fertility co-occurrence instead would have mined the words used to draw the "
         "line — which in a chapter whose primary cell IS a co-occurrence is not a subtle circularity "
         "but the whole result.", "",
         "**The contrast is relevant-versus-near-miss.** Every negative already passed the citation "
         "frame, so this measures precision at fixed recall; the z scores are not comparable to a "
         "relevant-versus-random-corpus ranking. B1 recomputes fold-locally so the CV recall estimate "
         "stays uncircular.", "",
         f"Abstracts present for **{n_abs:,} of {len(tier_b):,}** frame records "
         f"({n_abs / max(len(tier_b), 1):.0%}); mining titles alone would measure which literature "
         "writes its mechanism into its title, which is a fact about house style.", "",
         f"Candidate terms (positive count >= {MIN_GOLD}): **{len(rows):,}**", "",
         "| block | terms |", "|---|---|"]
    L += [f"| `{b}` | {counts.get(b, 0)} |" for b in order]
    L.append("")

    for b in order:
        sel = [r for r in rows if r["block"] == b][:15]
        if not sel:
            continue
        L += [f"\n## `{b}` — top by z\n", "| term | z | log-odds | pos | neg |", "|---|---|---|---|---|"]
        L += [f"| {r['term']} | {r['z']} | {r['log_odds']} | {r['gold']} | {r['neg']} |" for r in sel]

    L += ["", "---", "", "## Does any vocabulary separate the primary cell from the walls?", "",
          "This is the question A4 was run to answer, and the scope's declaration that Wall 1 is "
          "unenforceable at title and abstract stands or falls on it.", "",
          f"**Of the 40 strongest discriminators, {len(mech_in_top)} carry mechanism vocabulary.**", ""]
    if mech_in_top:
        L += ["| term | block | z | pos | neg |", "|---|---|---|---|---|"]
        L += [f"| {r['term']} | `{r['block']}` | {r['z']} | {r['gold']} | {r['neg']} |"
              for r in mech_in_top]
    else:
        L.append("None. Every one of the forty strongest discriminators is topic, treatment or "
                 "outcome vocabulary.")
    # The hypothesis's own name-word, looked up rather than assumed. Computed because the sign is
    # the finding and a hardcoded sentence would not survive a re-run on a different frame.
    by_term = {r["term"]: r for r in rows}
    named = [by_term[t] for t in ("despair", "hopelessness", "hopeless", "anomie") if t in by_term]
    if named:
        L += ["", "### The words the hypothesis is named after", "",
              "| term | z | pos | neg |", "|---|---|---|---|"]
        L += [f"| `{r['term']}` | **{r['z']}** | {r['gold']} | {r['neg']} |" for r in named]
        d = by_term.get("despair")
        if d and d["z"] < 0:
            L += ["", f"**`despair` is NEGATIVELY discriminative: z {d['z']}, {d['gold']} occurrences "
                  f"in the primary-anchor neighbourhood against {d['neg']:,} in the walls'.** The word "
                  "this hypothesis is named for is a marker of the literature it must be separated "
                  "FROM — the deaths-of-despair mortality corpus — and putting it in a production "
                  "query would pull the search toward the largest decoy cloud the chapter faces "
                  "(Wall 4) and away from its primary cell. The one precise mechanism term the frame "
                  "offers is `future orientation` (z "
                  f"{by_term['future orientation']['z'] if 'future orientation' in by_term else 'n/a'}"
                  ", " + (f"{by_term['future orientation']['gold']} positive occurrences and "
                          f"{by_term['future orientation']['neg']} negative"
                          if "future orientation" in by_term else "n/a") + "), which is perfectly "
                  "precise and far too rare to carry a query.", ""]

    geo = [r for r in rows[:40] if r["term"] in
           ("hungary", "bulgaria", "europe", "european", "romania", "poland", "czech", "russia")]
    if geo:
        L += ["", f"**And the strongest non-topic discriminators are place names**: "
              + ", ".join(f"`{r['term']}` (z {r['z']})" for r in geo) + ". The positive class is the "
              "post-communist anomie family, so what most distinguishes the primary neighbourhood "
              "from the walls is WHERE its studies were done. A query fitted on this would learn to "
              "retrieve Central European demography rather than despair research — which is Call 5's "
              "transportability problem appearing inside the query itself, before any synthesis "
              "decision is taken.", ""]
    L += ["", "**Read this against what the walls need.** A term that separates the primary "
          "neighbourhood by naming its TOPIC — fertility, intentions, a country, a survey — retrieves "
          "the right literature and does nothing to route within it. Only mechanism vocabulary can do "
          "Wall 1's work, because Wall 1 is the distinction between a despair mechanism and an "
          "uncertainty mechanism over the same treatment and the same outcome. The count above is "
          "therefore the measurement, not the term list itself.", ""]
    open(os.path.join(LOGS, f"{SLUG}-discriminative-terms.md"), "w").write("\n".join(L) + "\n")
    print(f"terms={len(rows)} mech_in_top40={len(mech_in_top)} "
          f"-> literature/search-logs/{SLUG}-discriminative-terms.md")


if __name__ == "__main__":
    main()
