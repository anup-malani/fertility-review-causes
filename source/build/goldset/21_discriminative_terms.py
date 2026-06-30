#!/usr/bin/env python3
"""
Part 3b — discriminative term extraction (spec §5). Rank candidate query terms by how strongly
they separate the GOLD-POSITIVE set from the 4,540 on-disk screened NOT_RELEVANT negatives,
using Monroe/Colaresi/Quinn "Fightin' Words": weighted log-odds-ratio with an informative
Dirichlet prior + z-score (variance-stabilized, so rare terms don't dominate). NOT raw tf-idf.

Text basis: TITLES only (the negatives have no abstracts on disk, so titles keep the two sides
on the same footing). Unigrams + bigrams, stopword-filtered.

CAVEAT (state in writeup): the negatives already passed the PI keyword filter, so the contrast
learned is relevant-vs-NEAR-MISS, not relevant-vs-random-database. That is the discrimination we
want (precision at fixed recall) but it is not a random negative.

CV NOTE: this runs on the FULL gold set here to expose the term landscape + sanity-check the
machinery. In Part 4 the SAME function is called fold-locally (training-fold gold only) so the
CV recall estimate stays uncircular. The external backbone (3a) is separate and leakage-free.

Inputs : *-tier-a-draft.json (56) + *-tier-b-screened.json (247) [gold+]; *-screened.json NOT_RELEVANT [neg]
Output : *-discriminative-terms.json + *-discriminative-terms.md (top terms per heuristic block)
"""
import json,re,math,sys
from pathlib import Path
from collections import Counter
LOGS=Path("/Users/shravanhari/~/Anup RA/projects/fertility-review-causes/literature/search-logs")
ALPHA0=1000.0        # total mass of the informative Dirichlet prior
MIN_GOLD=3           # candidate must appear in >=3 gold titles (noise floor)
STOP=set("the a an of and in on for from to its by is with as at or be this that these those "
         "we our their his her it they i ii iii new evidence using based study studies analysis "
         "approach paper article effect effects impact role case among between within over under "
         "are was were has have had do does can could will would not no more less than into "
         "about across after before during toward towards via per vs versus also two three some "
         "how what why when where which who whom data model models results result".split())

def toks(t):
    return [w for w in re.sub(r"[^a-z0-9\s]"," ",(t or "").lower()).split() if len(w)>2 and w not in STOP]
def terms(title):
    u=toks(title); out=list(u)
    out+= [f"{u[i]} {u[i+1]}" for i in range(len(u)-1)]   # bigrams
    return out

FERT=re.compile(r"fertil|childbear|birth|fecund|natalit|babi|child|son|daughter|offspring|family size|number of children|quantity")
PENS=re.compile(r"pension|social security|old.age|retire|annuit|provident|superannuat|insur|saving|transfer|elderly|security|welfare|payg|pay.as.you.go|intergenerational")
def block_of(term):
    f,p=bool(FERT.search(term)),bool(PENS.search(term))
    return "fertility" if (f and not p) else "pension-oas" if (p and not f) else "both" if (f and p) else "other"

def corpus_terms(titles):
    c=Counter()
    for t in titles: c.update(terms(t))
    return c

def main():
    A=json.load(open(LOGS/"old-age-security-pension-crowdout-tier-a-draft.json"))
    B=json.load(open(LOGS/"old-age-security-pension-crowdout-tier-b-screened.json"))
    scr=json.load(open(LOGS/"old-age-security-pension-crowdout-screened.json"))
    gold_titles=[g["title"] for g in A]+[g["title"] for g in B]
    neg_titles=[p["title"] for p in scr if p.get("llm_verdict")=="NOT_RELEVANT" and p.get("title")]
    print(f"gold+ titles: {len(gold_titles)} | negatives: {len(neg_titles)}",file=sys.stderr)

    gc=corpus_terms(gold_titles); nc=corpus_terms(neg_titles)
    vocab=set(gc)|set(nc)
    ng=sum(gc.values()); nn=sum(nc.values())
    comb={w:gc[w]+nc[w] for w in vocab}; ncomb=ng+nn
    a0=ALPHA0;
    rows=[]
    for w in vocab:
        if gc[w]<MIN_GOLD: continue
        aw=a0*comb[w]/ncomb
        # weighted log-odds (fightin' words), 2-group
        l_g=math.log((gc[w]+aw)/(ng+a0-gc[w]-aw))
        l_n=math.log((nc[w]+aw)/(nn+a0-nc[w]-aw))
        delta=l_g-l_n
        var=1.0/(gc[w]+aw)+1.0/(nc[w]+aw)
        z=delta/math.sqrt(var)
        rows.append({"term":w,"block":block_of(w),"z":round(z,2),"log_odds":round(delta,2),
                     "gold":gc[w],"neg":nc[w],"is_bigram":" " in w})
    rows.sort(key=lambda r:-r["z"])
    json.dump(rows,open(LOGS/"old-age-security-pension-crowdout-discriminative-terms.json","w"),indent=2)

    def top(block,k=30): return [r for r in rows if r["block"]==block][:k]
    L=["# Discriminative terms (Part 3b) · 2026-06-29","",
       "Fightin'-Words weighted log-odds (informative Dirichlet prior, z-scored) over TITLES: "
       f"gold-positive ({len(gold_titles)}) vs on-disk NOT_RELEVANT ({len(neg_titles)}). Higher z = "
       "more gold-discriminative. Negatives already passed the PI keyword filter → contrast is "
       "relevant-vs-near-miss. In Part-4 CV this is recomputed fold-locally.","",
       f"Candidates (gold count ≥ {MIN_GOLD}): **{len(rows)}** terms.",""]
    for b,lbl in [("fertility","FERTILITY block"),("pension-oas","PENSION / OLD-AGE-SECURITY block"),
                  ("both","BOTH-block (fertility×pension bigrams)"),("other","OTHER (context terms)")]:
        L.append(f"\n## {lbl} — top by z\n")
        L.append("| term | z | log-odds | gold | neg |")
        L.append("|---|---|---|---|---|")
        for r in top(b,25): L.append(f"| {r['term']} | {r['z']} | {r['log_odds']} | {r['gold']} | {r['neg']} |")
    (LOGS/"old-age-security-pension-crowdout-discriminative-terms.md").write_text("\n".join(L)+"\n")

    print(f"candidate terms: {len(rows)}",file=sys.stderr)
    print("by block:",dict(Counter(r['block'] for r in rows)),file=sys.stderr)
    print("\nTOP 20 overall (z):",file=sys.stderr)
    for r in rows[:20]: print(f"  {r['z']:6.1f} [{r['block']:11}] {r['term']}  (g{r['gold']}/n{r['neg']})",file=sys.stderr)
    print("written -> *-discriminative-terms.json, *-discriminative-terms.md",file=sys.stderr)
if __name__=="__main__": main()
