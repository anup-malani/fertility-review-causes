#!/usr/bin/env python3
"""
Part 4 (scaffold) — 10-fold CV over the per-block breadth vector (spec §4, §6).

Query = 2 blocks conjoined: (FERTILITY block) AND (PENSION/OLD-AGE-SECURITY block). A gold paper
is RECALLED iff its title matches BOTH blocks. Each block = the fixed external backbone (§3a)
UNION the top-N fold-local gold-mined discriminative terms (§3b) for that block, at breadth N.

Leakage discipline (the whole point of CV here):
  - backbone terms are FIXED in every fold (leakage-free; from published prior-review strings);
  - the gold-mined expansion is recomputed FROM THE TRAINING FOLDS' GOLD ONLY each fold (vs the
    fixed 4,540 on-disk NOT_RELEVANT negatives), so held-out recall never sees its own labels.

Knob = breadth vector (N_f, N_p), NOT a scalar (the blocks don't leak recall equally). We sweep a
grid, report CV held-out recall + per-block miss diagnostics + an on-disk budget proxy
(negatives matched), and locate the recall/budget frontier. The PRODUCTION query is refit on the
FULL gold at the chosen (N_f,N_p) (done in Part-4-full, after freeze).

STATUS: SCAFFOLD / DRY RUN. Runs on the current (un-frozen) gold A+B core. Matching is TITLE-only
(negatives + most Tier-B golds are title-only → keeps both sides on one footing; abstract matches
would only ADD recall, so title-only CV recall is a conservative lower bound). Real universe size
needs OpenAlex counts (openalex_universe() stub below) — wire in Part-4-full once query is frozen.

Inputs : *-tier-a-draft.json, *-tier-b-screened.json, *-external-backbone.json, *-screened.json
Output : *-cv-breadth-dryrun.json + *-cv-breadth-dryrun.md
"""
import json,re,math,random,sys
from pathlib import Path
from collections import Counter,defaultdict
LOGS=Path("/Users/shravanhari/~/Anup RA/projects/fertility-review-causes/literature/search-logs")
K_FOLDS=10; SEED=42; ALPHA0=1000.0; MIN_GOLD_FOLD=2
GRID=[0,3,6,10,15,20,30]

STOP=set("the a an of and in on for from to its by is with as at or be this that these those we our "
         "their his her it they i ii iii new evidence using based study studies analysis approach paper "
         "article effect effects impact role case among between within over under are was were has have "
         "had do does can could will would not no more less than into about across after before during "
         "toward towards via per vs versus also two three some how what why when where which who whom data "
         "model models results result".split())
def norm(s): return re.sub(r"\s+"," ",re.sub(r"[^a-z0-9\s]"," ",(s or "").lower())).strip()
def utoks(t): return [w for w in norm(t).split() if len(w)>2 and w not in STOP]
def cand_terms(title):
    u=utoks(title); return u+[f"{u[i]} {u[i+1]}" for i in range(len(u)-1)]

FERT=re.compile(r"fertil|childbear|birth|fecund|natalit|babi|child|son|daughter|offspring|family size|number of children|quantity")
PENS=re.compile(r"pension|social security|old.age|retire|annuit|provident|superannuat|insur|saving|transfer|elderly|security|welfare|payg|pay.as.you.go|intergenerational")
def block_of(term):
    f,p=bool(FERT.search(term)),bool(PENS.search(term))
    return "fertility" if (f and not p) else "pension" if (p and not f) else None  # skip both/other for block expansion

# ---------- matching ----------
def compile_term(term):
    t=term.strip().lower()
    if t.endswith("*"):
        stem=norm(t[:-1]); return ("prefix",stem)
    return ("phrase",norm(t))
def title_matches_block(ntitle_padded, compiled_terms):
    for kind,val in compiled_terms:
        if not val: continue
        if kind=="prefix":
            if re.search(r"\b"+re.escape(val),ntitle_padded): return True
        else:
            if (" "+val+" ") in ntitle_padded: return True
    return False

# ---------- fold-local discriminative mining (fightin' words; reuse step 21 logic) ----------
def neg_counts():
    scr=json.load(open(LOGS/"old-age-security-pension-crowdout-screened.json"))
    c=Counter()
    for p in scr:
        if p.get("llm_verdict")=="NOT_RELEVANT" and p.get("title"): c.update(cand_terms(p["title"]))
    return c, sum(c.values())
def mine(train_titles, nc, nn):
    gc=Counter()
    for t in train_titles: gc.update(cand_terms(t))
    ng=sum(gc.values()); vocab=set(gc)
    ncomb=ng+nn
    fert=[]; pens=[]
    for w in vocab:
        if gc[w]<MIN_GOLD_FOLD: continue
        b=block_of(w)
        if b is None: continue
        comb=gc[w]+nc.get(w,0); aw=ALPHA0*comb/ncomb
        delta=math.log((gc[w]+aw)/(ng+ALPHA0-gc[w]-aw))-math.log((nc.get(w,0)+aw)/(nn+ALPHA0-nc.get(w,0)-aw))
        z=delta/math.sqrt(1.0/(gc[w]+aw)+1.0/(nc.get(w,0)+aw))
        (fert if b=="fertility" else pens).append((w,z))
    fert.sort(key=lambda x:-x[1]); pens.sort(key=lambda x:-x[1])
    return [w for w,_ in fert],[w for w,_ in pens]

# ---------- data ----------
def load_gold():
    A=json.load(open(LOGS/"old-age-security-pension-crowdout-tier-a-draft.json"))
    B=json.load(open(LOGS/"old-age-security-pension-crowdout-tier-b-screened.json"))
    return [{"title":g["title"],"tier":"A"} for g in A]+[{"title":g["title"],"tier":"B"} for g in B]
def load_backbone():
    bb=json.load(open(LOGS/"old-age-security-pension-crowdout-external-backbone.json"))
    return [compile_term(t) for t in bb["fertility_block"]],[compile_term(t) for t in bb["pension_oas_block"]]

# ---------- CV ----------
def cv(gold, bb_f, bb_p, nc, nn, Nf, Np):
    rnd=random.Random(SEED); idx=list(range(len(gold))); rnd.shuffle(idx)
    folds=[idx[i::K_FOLDS] for i in range(K_FOLDS)]
    hit=0; tot=0; miss_f=0; miss_p=0; miss_both=0
    tier_hit={"A":0,"B":0}; tier_tot={"A":0,"B":0}   # Recall(A) vs Recall(B) — the headline
    for k in range(K_FOLDS):
        test=set(folds[k]); train=[gold[i]["title"] for i in idx if i not in test]
        mf,mp=mine(train,nc,nn)
        fterms=bb_f+[compile_term(w) for w in mf[:Nf]]
        pterms=bb_p+[compile_term(w) for w in mp[:Np]]
        for i in folds[k]:
            nt=" "+norm(gold[i]["title"])+" "; tot+=1; tr=gold[i]["tier"]; tier_tot[tr]+=1
            fok=title_matches_block(nt,fterms); pok=title_matches_block(nt,pterms)
            if fok and pok: hit+=1; tier_hit[tr]+=1
            elif not fok and not pok: miss_both+=1
            elif not fok: miss_f+=1
            else: miss_p+=1
    rA=tier_hit["A"]/tier_tot["A"] if tier_tot["A"] else 0
    rB=tier_hit["B"]/tier_tot["B"] if tier_tot["B"] else 0
    return {"Nf":Nf,"Np":Np,"recall":round(hit/tot,4),"hit":hit,"tot":tot,
            "recall_A":round(rA,4),"recall_B":round(rB,4),"bias_correction":round(rA-rB,4),
            "miss_fert_block":miss_f,"miss_pens_block":miss_p,"miss_both":miss_both}

def budget_proxy(gold, bb_f, bb_p, nc, nn, Nf, Np):
    """On-disk proxy for universe/precision cost: how many of the 4,540 NOT_RELEVANT negatives the
       FULL-gold-refit query matches. (Real universe size = OpenAlex count; see openalex_universe.)"""
    mf,mp=mine([g["title"] for g in gold],nc,nn)
    fterms=bb_f+[compile_term(w) for w in mf[:Nf]]; pterms=bb_p+[compile_term(w) for w in mp[:Np]]
    scr=json.load(open(LOGS/"old-age-security-pension-crowdout-screened.json"))
    neg=0
    for p in scr:
        if p.get("llm_verdict")!="NOT_RELEVANT" or not p.get("title"): continue
        nt=" "+norm(p["title"])+" "
        if title_matches_block(nt,fterms) and title_matches_block(nt,pterms): neg+=1
    return neg

def openalex_universe(fert_terms, pens_terms):
    """STUB for Part-4-full: build OpenAlex title_and_abstract.search Boolean
       ((f1 OR f2 ...) AND (p1 OR p2 ...)) and return meta.count. Not called in the dry run."""
    raise NotImplementedError("wire in Part-4-full after the query is frozen")

# ---- HEADLINE METRICS for Part-4-full (decided with Shravan 2026-06-29) ----
# Under def-1, Tier B is the UNBIASED sample, so:
#   PRIMARY  = Recall(B)            -- honest query recall on a representative relevant sample.
#   DIAGNOSTIC = Recall(A) - Recall(B)  -- "is the query inflated toward keyword-sourced papers?"
#               (dry run: ~0/slightly negative => NO inflation; the slight A<B is Tier A's theory canon).
#   CEILING PROBE = Recall(B | title lacks query vocab)  -- the hard-tail conditional, NOT a separate
#               def-3 tier. Operational def: a Tier-B paper is "vocab-hard" if its TITLE fails the
#               2-block query; the conditional recall = of those, how many the query recovers via
#               ABSTRACT match. *** Requires abstract matching (Part-4-full item #3); with title-only
#               it is ~0 by construction, so DO NOT report it until abstracts are wired. *** Report as a
#               BOUND, not a pinned estimate (n~38, SE~±8%; powered for gross gaps per §6, not fine tuning).
#               Caveat: even this bound is optimistic — def-1 Tier B was snowball-seeded off the keyword
#               set + screened partly on vocab, so truly vocab-disconnected papers are under-represented.
#   ALSO report Recall by empirical-vs-theory (the decision-relevant coarse cut; the sign flip showed
#               recall dies on the theory canon).
def conditional_hardtail_recall(*a, **k):
    raise NotImplementedError("Part-4-full: Recall(B | title fails 2-block query), measured via abstract match")

def main():
    gold=load_gold(); bb_f,bb_p=load_backbone(); nc,nn=neg_counts()
    print(f"gold {len(gold)} (A {sum(1 for g in gold if g['tier']=='A')}, B {sum(1 for g in gold if g['tier']=='B')}); "
          f"negatives tokens {nn}; backbone f={len(bb_f)} p={len(bb_p)}",file=sys.stderr)
    rows=[cv(gold,bb_f,bb_p,nc,nn,Nf,Np) for Nf in GRID for Np in GRID]
    # budget proxy only on the diagonal-ish frontier points (cheap subset) for the dry run
    front=sorted(rows,key=lambda r:-r["recall"])[:8]
    for r in front: r["neg_matched_proxy"]=budget_proxy(gold,bb_f,bb_p,nc,nn,r["Nf"],r["Np"])
    json.dump(rows,open(LOGS/"old-age-security-pension-crowdout-cv-breadth-dryrun.json","w"),indent=2)

    best=max(rows,key=lambda r:r["recall"])
    base=next(r for r in rows if r["Nf"]==0 and r["Np"]==0)
    L=["# Part 4 CV — breadth-vector dry run · 2026-06-29","",
       "**SCAFFOLD / DRY RUN on un-frozen gold.** 10-fold CV, title-only matching (conservative "
       "lower bound), backbone fixed + fold-local gold-mined expansion. Real universe size pending "
       "OpenAlex wiring + gold freeze.","",
       f"- gold = {len(gold)} (A+B core); negatives = 4,537 (budget proxy)",
       f"- **backbone-only recall (Nf=Np=0): {base['recall']:.1%}**  "
       f"[Recall(A) {base['recall_A']:.1%} / Recall(B) {base['recall_B']:.1%} → bias correction {base['bias_correction']:+.1%}]  "
       f"(miss fert-block {base['miss_fert_block']}, pens-block {base['miss_pens_block']}, both {base['miss_both']})",
       f"- **best grid point: Nf={best['Nf']}, Np={best['Np']} → CV recall {best['recall']:.1%}**  "
       f"[Recall(A) {best['recall_A']:.1%} / Recall(B) {best['recall_B']:.1%} → **bias correction {best['bias_correction']:+.1%}**]","",
       "> Recall(A)−Recall(B) is the vocabulary-bias correction — the headline scientific output. "
       "Tier A is keyword-sourced (optimistic); Tier B is the unbiased orthogonal sample.","",
       "## Dry-run findings (challenge spec assumptions — confirm in Part-4-full)","",
       f"1. **SIGN FLIP: Recall(A) < Recall(B)** (correction {best['bias_correction']:+.0%} at peak), not the "
       "positive value the method assumed. Driver: Tier A now carries the Part-1c theory canon "
       "(e.g. Ehrlich–Lui, Boldrin–Jones) whose titles lack surface fertility/pension vocabulary; "
       "Tier B (def-1, unbiased — NOT adversarial) is keyword-richer. Reading: the query is not "
       "inflated toward keyword-sourced papers; it slightly UNDER-recalls the abstract theory canon.",
       f"2. **The FERTILITY block binds, not pension** (held-out misses ~{best['miss_fert_block']} fert vs "
       f"~{best['miss_pens_block']} pens) — opposite of §3's 'pension is the thin block'. Much relevant work "
       "says children/sons/value-of-children/family-size, not fertility/birth. → spend fertility-block breadth.",
       "3. **Title-only ceiling ≈ 70%**, saturating near N≈20–30. Abstract matching (Part-4-full) "
       "should lift this; it's a conservative lower bound.",
       "4. **Metric decision (Shravan 2026-06-29):** under def-1, **Recall(B) is the PRIMARY** honest "
       "estimate; **Recall(A)−Recall(B) is a DIAGNOSTIC** ('is the query inflated toward keyword-sourced "
       "papers?' — here: no). The worst-case vocabulary ceiling is reported NOT as a separate def-3 tier "
       "but as **Recall(B | title fails the 2-block query), measured via ABSTRACT match** — a hard-tail "
       "conditional, reported as a BOUND (n~38, powered for gross gaps not fine tuning; needs abstract "
       "matching, so deferred to Part-4-full). Also report empirical-vs-theory recall (where the canon "
       "tail lives). Caveat: this bound is itself optimistic (Tier B snowball-seeded off the keyword set).","",
       "## Recall surface (CV held-out recall by breadth vector)","",
       "| Nf \\ Np | "+" | ".join(str(n) for n in GRID)+" |",
       "|"+"---|"*(len(GRID)+1)]
    by={(r["Nf"],r["Np"]):r["recall"] for r in rows}
    for nf in GRID:
        L.append(f"| **{nf}** | "+" | ".join(f"{by[(nf,np)]:.0%}" for np in GRID)+" |")
    L+=["","## Recall / budget frontier (top-8 recall points; neg_matched = on-disk budget proxy)","",
        "| Nf | Np | recall | Rec(A) | Rec(B) | A−B | miss-fert | miss-pens | miss-both | neg-matched |",
        "|---|---|---|---|---|---|---|---|---|---|"]
    for r in front:
        L.append(f"| {r['Nf']} | {r['Np']} | {r['recall']:.1%} | {r['recall_A']:.0%} | {r['recall_B']:.0%} | {r['bias_correction']:+.0%} | {r['miss_fert_block']} | {r['miss_pens_block']} | {r['miss_both']} | {r['neg_matched_proxy']} |")
    L+=["","## Reading the diagnostics","",
        "- If held-out misses concentrate on ONE block, move breadth budget there (that's the §6 "
        "allocation signal). - The pension/OAS block is the thin one (§3a), so expect it to bind.",
        "- Production query (Part-4-full) = refit on FULL gold at the chosen (Nf,Np); quote the CV "
        "recall here as the honest out-of-sample estimate. Real budget = OpenAlex universe count."]
    (LOGS/"old-age-security-pension-crowdout-cv-breadth-dryrun.md").write_text("\n".join(L)+"\n")

    print(f"backbone-only recall: {base['recall']:.1%}  | best {best['recall']:.1%} @ Nf={best['Nf']},Np={best['Np']}",file=sys.stderr)
    print("frontier (recall / neg-proxy):",file=sys.stderr)
    for r in front: print(f"  Nf={r['Nf']:>2} Np={r['Np']:>2}  recall {r['recall']:.1%}  neg {r['neg_matched_proxy']}  (missF {r['miss_fert_block']} missP {r['miss_pens_block']} both {r['miss_both']})",file=sys.stderr)
    print("written -> *-cv-breadth-dryrun.{json,md}",file=sys.stderr)
if __name__=="__main__": main()
